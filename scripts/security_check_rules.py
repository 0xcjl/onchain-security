"""Pure scoring and address comparison rules for security-check.

Writers must update security flags atomically (write a temp file, then rename).
"""

import json
import os
import re
import tempfile


CHAIN_ALIASES = {
    "base": "base", "8453": "base",
    "bsc": "bsc", "56": "bsc",
    "eth": "eth", "ethereum": "eth", "1": "eth",
    "4663": "robinhood", "robinhood": "robinhood",
    "solana": "solana",
}


def _normalize_chain(value):
    value = str(value or "").strip().lower()
    return CHAIN_ALIASES.get(value, value)


def match_security_flags(flags, chain, address, token_facts):
    """Return active matching flag IDs for one token assessment."""
    names = {
        str(token_facts.get(key) or "").strip().casefold()
        for key in ("token_name", "token_symbol")
        if str(token_facts.get(key) or "").strip()
    }
    matches = []
    for item in flags if isinstance(flags, list) else []:
        if not isinstance(item, dict) or item.get("status") != "active":
            continue
        target = item.get("target")
        if not isinstance(target, dict):
            continue
        target_chain = target.get("chain")
        target_address = target.get("address")
        if target_chain not in (None, "") and target_address not in (None, ""):
            matched = (
                _normalize_chain(target_chain) == _normalize_chain(chain)
                and str(target_address).strip().casefold() == str(address or "").strip().casefold()
            )
        else:
            protocol = str(target.get("protocol") or "").strip().casefold()
            matched = bool(protocol and protocol in names)
        if matched:
            matches.append(item.get("flag_id"))
    return matches


def write_flags_atomic(path, flags):
    """Write a flag array through a same-directory temporary file and rename."""
    directory = os.fspath(os.path.dirname(os.fspath(path)) or ".")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=directory, prefix=".security-flags-",
            suffix=".tmp", delete=False,
        ) as stream:
            temporary = stream.name
            json.dump(flags, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    except Exception:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
        raise

def _truth(value):
    if value is True or value == 1:
        return True
    return isinstance(value, str) and value.strip().lower() in {"1", "true", "yes"}


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def rate(facts):
    """Return (rating, reasons) from normalized facts; unknown values add no risk."""
    hard, high, medium = [], [], []
    privilege_reasons = {
        "token is mintable",
        "upgradable proxy has an EOA admin",
        "hidden owner detected",
        "ownership can be taken back",
        "transfers can be paused",
    }
    if _truth(facts.get("is_honeypot")):
        hard.append("honeypot")
    if _truth(facts.get("sell_blocked")) or _truth(facts.get("cannot_sell_all")):
        hard.append("selling is blocked")
    for name in ("buy_tax", "sell_tax"):
        tax = _number(facts.get(name))
        if tax is not None:
            if tax >= 0.5:
                hard.append(f"{name.replace('_', ' ')} is at least 50%")
            elif tax >= 0.1:
                high.append(f"{name.replace('_', ' ')} is 10% to under 50%")
            elif tax > 0:
                medium.append(f"{name.replace('_', ' ')} is under 10%")
    if _truth(facts.get("owner_change_balance")):
        hard.append("owner can change balances")

    if _truth(facts.get("is_mintable")):
        high.append("token is mintable")
    if _truth(facts.get("is_scam")):
        high.append("Blockscout marks address as scam")
    if _truth(facts.get("is_blacklisted")):
        high.append("blacklisting is possible")
    if _truth(facts.get("transfer_pausable")):
        high.append("transfers can be paused")
    if facts.get("is_open_source") is not None and str(facts.get("is_open_source")).strip() == "0":
        high.append("source is not verified/open")
    if _truth(facts.get("hidden_owner")):
        high.append("hidden owner detected")
    if _truth(facts.get("can_take_back_ownership")):
        high.append("ownership can be taken back")
    if facts.get("is_contract") is False:
        high.append("address is not a contract")
    if _truth(facts.get("is_proxy")):
        admin_kind = facts.get("proxy_admin_kind")
        if admin_kind == "eoa":
            high.append("upgradable proxy has an EOA admin")
        elif admin_kind == "contract":
            medium.append("proxy admin is a contract")
        elif admin_kind in ("unknown", None):
            medium.append("proxy admin is unknown")
    top10 = _number(facts.get("holder_top10_percent"))
    if top10 is not None and top10 > 80:
        medium.append("top 10 holders own over 80%")
    if str(facts.get("binance_risk_level", "")).strip().lower() == "high":
        medium.append("Binance audit reports high risk")
    if _truth(facts.get("active_security_flag")):
        high.append("active security flag matches this token")

    if hard:
        return "REJECT", hard + high + medium
    if high:
        if (str(facts.get("goplus_trust_list") or "").strip() == "1"
                and all(reason in privilege_reasons for reason in high)):
            return "MEDIUM", high + medium + ["goplus_trusted_exemption: HIGH->MEDIUM"]
        return "HIGH", high + medium
    if medium:
        return "MEDIUM", medium
    return "LOW", []


def address_poisoning(address, entries):
    """Return exact/poisoning match metadata for known addresses."""
    def clean(value):
        value = str(value or "").strip().lower()
        return value[2:] if value.startswith("0x") else value

    candidate = clean(address)
    if not candidate:
        return {"status": "unavailable", "match": None}
    for entry in entries or []:
        known = clean(entry.get("address")) if isinstance(entry, dict) else ""
        if known and candidate == known:
            return {"status": "ok", "match": "exact", "label": entry.get("label"), "address": entry.get("address")}
    for entry in entries or []:
        known = clean(entry.get("address")) if isinstance(entry, dict) else ""
        if (re.fullmatch(r"[0-9a-f]{40}", candidate) and re.fullmatch(r"[0-9a-f]{40}", known)
                and candidate[:4] == known[:4] and candidate[-4:] == known[-4:]):
            return {"status": "ok", "match": "poisoning", "label": entry.get("label"), "address": entry.get("address")}
    return {"status": "ok", "match": None}


def tradable(rating, data_status, active_flag=False):
    return rating in {"LOW", "MEDIUM"} and data_status == "complete" and not active_flag

