import json
import sys
import io
import importlib.util
import importlib.machinery
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit
from contextlib import redirect_stdout
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from security_check_rules import address_poisoning, match_security_flags, rate, tradable, write_flags_atomic

SECURITY_CHECK_PATH = Path(__file__).resolve().parents[1] / "security-check"
LOADER = importlib.machinery.SourceFileLoader("security_check_script", str(SECURITY_CHECK_PATH))
SPEC = importlib.util.spec_from_loader("security_check_script", LOADER)
security_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(security_check)


class SecurityRuleTests(unittest.TestCase):
    def test_contract_status_requires_is_contract_to_be_determined(self):
        self.assertEqual(security_check.contract_status(True), "ok")
        self.assertEqual(security_check.contract_status(False), "ok")
        self.assertEqual(security_check.contract_status(None), "unavailable")

    def test_clean_token_is_low(self):
        self.assertEqual(rate({})[0], "LOW")

    def test_honeypot_is_reject(self):
        self.assertEqual(rate({"is_honeypot": "1"})[0], "REJECT")

    def test_high_tax_is_reject(self):
        self.assertEqual(rate({"sell_tax": "0.6"})[0], "REJECT")

    def test_mintable_is_high(self):
        self.assertEqual(rate({"is_mintable": "1"})[0], "HIGH")

    def test_goplus_trusted_mintable_is_medium_with_exemption_flag(self):
        rating, reasons = rate({"is_mintable": "1", "goplus_trust_list": "1"})
        self.assertEqual(rating, "MEDIUM")
        self.assertIn("goplus_trusted_exemption: HIGH->MEDIUM", reasons)

    def test_goplus_trusted_honeypot_remains_rejected(self):
        self.assertEqual(rate({
            "is_mintable": "1", "is_honeypot": "1", "goplus_trust_list": "1",
        })[0], "REJECT")

    def test_goplus_trusted_mintable_with_scam_remains_high(self):
        self.assertEqual(rate({
            "is_mintable": "1", "is_scam": "1", "goplus_trust_list": "1",
        })[0], "HIGH")

    def test_goplus_untrusted_mintable_remains_high(self):
        self.assertEqual(rate({"is_mintable": "1", "goplus_trust_list": "0"})[0], "HIGH")

    def test_ten_to_fifty_percent_tax_is_high(self):
        self.assertEqual(rate({"buy_tax": "0.2"})[0], "HIGH")

    def test_small_tax_is_medium(self):
        self.assertEqual(rate({"sell_tax": "0.05"})[0], "MEDIUM")

    def test_proxy_with_unknown_admin_is_medium(self):
        rating, reasons = rate({"is_proxy": True, "proxy_admin_kind": "unknown"})
        self.assertEqual(rating, "MEDIUM")
        self.assertIn("proxy admin is unknown", reasons)

    def test_missing_data_does_not_raise_risk(self):
        self.assertEqual(rate({"buy_tax": None, "is_honeypot": None})[0], "LOW")
        self.assertFalse(tradable("LOW", "partial"))

    def test_poisoning_and_exact_address_detection(self):
        known = [{"label": "USDC", "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"}]
        self.assertEqual(address_poisoning("0x83358900000000000000000000000000bdA02913", known)["match"], "poisoning")
        self.assertEqual(address_poisoning("0x833589fcD6eDb6E08f4c7C32D4f71b54bdA02913", known)["match"], "exact")

    def test_tradable_rules(self):
        self.assertTrue(tradable("LOW", "complete"))
        self.assertTrue(tradable("MEDIUM", "complete"))
        self.assertFalse(tradable("HIGH", "complete"))
        self.assertFalse(tradable("LOW", "missing"))
        self.assertFalse(tradable("LOW", "complete", True))

    def test_active_flag_matches_and_resolved_flag_is_ignored(self):
        flags = [
            {"flag_id": "active-1", "target": {"protocol": "Acme"}, "status": "active"},
            {"flag_id": "resolved-1", "target": {"protocol": "Acme"}, "status": "resolved"},
        ]
        self.assertEqual(match_security_flags(flags, "base", "0x1234", {"token_name": "ACME"}), ["active-1"])
        self.assertEqual(rate({"active_security_flag": True})[0], "HIGH")
        self.assertFalse(tradable("HIGH", "complete", True))

    def test_chain_and_address_match_with_normalized_chain_and_address(self):
        flags = [{"flag_id": "contract-1", "status": "active",
                  "target": {"protocol": "Other", "chain": "8453", "address": "0xAbCd"}}]
        self.assertEqual(match_security_flags(flags, "base", "0xabcd", {}), ["contract-1"])
        self.assertEqual(match_security_flags(flags, "bsc", "0xabcd", {}), [])

    def test_protocol_name_matches_case_insensitively(self):
        flags = [{"flag_id": "protocol-1", "status": "active", "target": {"protocol": "Acme Protocol"}}]
        self.assertEqual(match_security_flags(flags, "eth", "0xabcd", {"token_symbol": "acme protocol"}), ["protocol-1"])

    def test_missing_and_empty_flags_file_are_no_flags(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(security_check, "CONFIG", Path(directory)):
                missing = security_check.load_flags("base", "0x1234", {})
                (Path(directory) / "security-flags.json").write_text("  \n", encoding="utf-8")
                empty = security_check.load_flags("base", "0x1234", {})
        for result in (missing, empty):
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["matches"], [])
            self.assertFalse(result["active"])
            self.assertNotIn("unknowns", result)

    def test_unparseable_flags_file_adds_specific_unknown(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "security-flags.json"
            path.write_text("{bad json", encoding="utf-8")
            with patch.object(security_check, "CONFIG", Path(directory)):
                result = security_check.load_flags("base", "0x1234", {})
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["unknowns"], ["security_flags_unparseable"])

    def test_flags_writer_writes_json_array(self):
        flags = [{"flag_id": "written-1", "status": "active", "target": {"protocol": "Acme"}}]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "security-flags.json"
            write_flags_atomic(path, flags)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), flags)

    def test_goplus_sparse_threshold_is_more_than_five_missing_core_fields(self):
        core_fields = security_check.GOPLUS_CORE_FIELDS
        five_present = {field: "0" for field in core_fields[:3]}
        self.assertFalse(security_check.goplus_fields_sparse(five_present))
        six_present = {field: "0" for field in core_fields[:2]}
        self.assertTrue(security_check.goplus_fields_sparse(six_present))

    def test_goplus_trust_list_is_exposed_and_used_for_partial_assessment(self):
        address = "0x" + "11" * 20
        goplus_fields = {field: None for field in security_check.GOPLUS_CORE_FIELDS}
        goplus_fields.update({"trust_list": "1", "is_mintable": "1"})
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (
                patch.object(security_check, "ROOT", root),
                patch.object(security_check, "CONFIG", root),
                patch.object(security_check, "goplus_check", return_value=(
                    {"status": "ok", "fields": goplus_fields},
                    {"trust_list": "1", "is_mintable": "1"},
                )),
                patch.object(security_check, "contract_check", return_value=(
                    {"status": "ok", "is_proxy_rpc": False, "proxy_standard": None},
                    {"is_contract": True, "is_proxy": False, "is_proxy_rpc": False,
                     "proxy_admin_kind": None},
                )),
                patch.object(security_check, "binance_check", side_effect=AssertionError("not called")),
                patch.object(sys, "argv", ["security-check", "--chain", "base", "--address", address]),
                redirect_stdout(output),
            ):
                self.assertEqual(security_check.main(), 0)

        result = json.loads(output.getvalue())
        self.assertEqual(result["rating"], "MEDIUM")
        self.assertEqual(result["data_status"], "partial")
        self.assertFalse(result["tradable"])
        self.assertEqual(result["checks"]["goplus"]["fields"]["trust_list"], "1")
        self.assertIn("goplus_trusted_exemption: HIGH->MEDIUM", result["flags"])
        self.assertIn("goplus_trusted_exemption: HIGH->MEDIUM", result["notes"])

    def test_evm_contract_check_uses_legacy_zeppelin_slots_and_classifies_admin(self):
        token = "0x" + "11" * 20
        implementation = "0x" + "22" * 20
        admin = "0x" + "33" * 20
        storage = {
            security_check.IMPL_SLOT: "0x" + "0" * 64,
            security_check.ADMIN_SLOT: "0x" + "0" * 64,
            security_check.BEACON_SLOT: "0x" + "0" * 64,
            security_check.ZEPP_IMPL_SLOT: "0x" + "0" * 24 + implementation[2:],
            security_check.ZEPP_ADMIN_SLOT: "0x" + "0" * 24 + admin[2:],
        }
        calls = []
        admin_bytecode = ["0x"]

        def rpc(url, method, params):
            calls.append((method, params))
            if method == "eth_getCode":
                return "0x6000" if params[0] == token else admin_bytecode[0]
            if method == "eth_getStorageAt":
                return storage[params[1]]
            if method == "eth_call":
                raise RuntimeError("owner is unavailable")
            raise AssertionError(method)

        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory)
            (config / "rpc.json").write_text(
                json.dumps({"chains": {"base": {"rpc_candidates": [{"url": "https://rpc.invalid", "provider": "test"}]}}}),
                encoding="utf-8",
            )
            with patch.object(security_check, "CONFIG", config), patch.object(security_check, "rpc_call", side_effect=rpc):
                fields, facts = security_check.evm_contract_check("base", token)
                admin_bytecode[0] = "0x6000"
                contract_admin_fields, _ = security_check.evm_contract_check("base", token)

        self.assertEqual(fields["proxy_standard"], "zeppelinos")
        self.assertTrue(fields["is_proxy_rpc"])
        self.assertEqual(fields["implementation"], implementation)
        self.assertEqual(fields["admin"], admin)
        self.assertEqual(fields["admin_kind"], "eoa")
        self.assertEqual(contract_admin_fields["admin_kind"], "contract")
        self.assertEqual(contract_admin_fields["admin_code_type"], "contract")
        self.assertTrue(facts["is_proxy"])
        self.assertIn(("eth_getStorageAt", [token, security_check.ZEPP_IMPL_SLOT, "latest"]), calls)
        self.assertIn(("eth_getStorageAt", [token, security_check.ZEPP_ADMIN_SLOT, "latest"]), calls)

    def test_robinhood_contract_check_keeps_blockscout_metadata_and_goplus_verification(self):
        address = "0x" + "11" * 20
        token = {"name": "Token", "symbol": "TOK", "type": "ERC-20", "holders_count": 17, "reputation": "ok"}
        evm_fields = {"status": "ok", "is_contract": True, "is_proxy": False, "owner": address}
        evm_facts = {"is_contract": True, "is_proxy": False, "owner": address}
        with (
            patch.object(security_check, "run_wrapper", return_value={"token": token}) as wrapper,
            patch.object(security_check, "blockscout_contract_check", return_value={
                "status": "ok", "source_verified": "verified", "is_partially_verified": False,
                "is_open_source": "1", "proxy_type": None, "implementations": [], "is_scam": False,
                "is_contract": True, "creator_address_hash": None, "creation_transaction_hash": None,
            }),
            patch.object(security_check, "evm_contract_check", return_value=(evm_fields, evm_facts)) as evm,
        ):
            fields, facts = security_check.contract_check("4663", address, {"is_open_source": "1"})

        wrapper.assert_called_once_with([str(security_check.ROOT / "bin" / "robinhood-chain"), "token", address])
        evm.assert_called_once_with("4663", address)
        self.assertEqual(fields["fields"], {
            "name": "Token", "symbol": "TOK", "type": "ERC-20", "holders_count": 17,
            "reputation": "ok", "source_verified": "verified", "source_verified_source": "Blockscout Pro",
            "is_partially_verified": False, "proxy_type": None, "implementations": [], "is_scam": False,
            "creator_address_hash": None, "creation_transaction_hash": None,
        })
        self.assertTrue(facts["is_contract"])
        self.assertEqual(facts["source_verified"], "verified")
        self.assertEqual(facts["is_open_source"], "1")

    def test_robinhood_source_verification_is_unknown_without_goplus_value(self):
        with (
            patch.object(security_check, "run_wrapper", return_value={"token": {"name": "Token"}}),
            patch.object(security_check, "blockscout_contract_check", return_value={
                "status": "partial", "source_verified": None, "is_partially_verified": None,
                "is_open_source": None, "proxy_type": None, "implementations": None, "is_scam": None,
                "is_contract": None, "creator_address_hash": None, "creation_transaction_hash": None,
            }),
            patch.object(security_check, "evm_contract_check", return_value=(
                {"status": "ok", "is_contract": True}, {"is_contract": True},
            )),
        ):
            fields, facts = security_check.contract_check("4663", "0x" + "11" * 20, {})

        self.assertIsNone(fields["fields"]["source_verified"])
        self.assertEqual(fields["fields"]["source_verified_source"], "unknown")
        self.assertIsNone(facts["source_verified"])

    def test_goplus_proxy_survives_rpc_no_slot_and_sparse_fields_are_partial(self):
        address = "0x" + "11" * 20
        goplus_fields = {field: None for field in security_check.GOPLUS_CORE_FIELDS}
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (
                patch.object(security_check, "ROOT", root),
                patch.object(security_check, "CONFIG", root),
                patch.object(security_check, "goplus_check", return_value=({"status": "ok", "fields": goplus_fields}, {"is_proxy": "1"})),
                patch.object(security_check, "contract_check", return_value=(
                    {"status": "ok", "is_proxy_rpc": False, "proxy_standard": None},
                    {"is_contract": True, "is_proxy": False, "is_proxy_rpc": False, "proxy_admin_kind": None},
                )),
                patch.object(security_check, "binance_check", side_effect=AssertionError("not called")),
                patch.object(sys, "argv", ["security-check", "--chain", "base", "--address", address]),
                redirect_stdout(output),
            ):
                self.assertEqual(security_check.main(), 0)

        result = json.loads(output.getvalue())
        self.assertFalse(result["checks"]["contract"]["is_proxy_rpc"])
        self.assertEqual(result["checks"]["contract"]["admin_kind"], "unknown")
        self.assertEqual(result["rating"], "MEDIUM")
        self.assertEqual(result["data_status"], "partial")
        self.assertIn("proxy_admin", result["unknowns"])
        self.assertIn("goplus_fields_sparse", result["notes"])

    def test_blockscout_verified_partial_and_unverified_source_states(self):
        address = "0x" + "11" * 20
        cases = [
            ({"is_verified": True}, "verified", "1"),
            ({"is_verified": False, "is_partially_verified": True}, "verified-partial", "1"),
            ({"is_verified": False}, "unverified", "0"),
        ]
        for contract, expected, open_source in cases:
            with self.subTest(expected=expected), patch.object(
                security_check, "blockscout_get", side_effect=[contract, {"is_scam": False, "is_contract": True}],
            ):
                result = security_check.blockscout_contract_check(address)
            self.assertEqual(result["source_verified"], expected)
            self.assertEqual(result["is_open_source"], open_source)
            self.assertEqual(result["status"], "ok")
            self.assertEqual(rate({"is_open_source": open_source})[0], "HIGH" if expected == "unverified" else "LOW")

    def test_blockscout_scam_flag_rates_at_least_high(self):
        self.assertEqual(rate({"is_scam": True})[0], "HIGH")

    def test_blockscout_api_failure_keeps_unknown_and_marks_partial(self):
        address = "0x" + "11" * 20
        with patch.object(security_check, "blockscout_get", side_effect=RuntimeError("unavailable")):
            result = security_check.blockscout_contract_check(address)
        self.assertEqual(result["status"], "partial")
        self.assertIsNone(result["source_verified"])
        self.assertIsNone(result["is_scam"])
        self.assertIsNone(result["is_open_source"])

    def test_blockscout_api_failure_makes_assessment_partial(self):
        address = "0x" + "11" * 20
        goplus_fields = {field: "0" for field in security_check.GOPLUS_CORE_FIELDS}
        api_unknown = {
            "status": "partial", "source_verified": None, "is_partially_verified": None,
            "is_open_source": None, "proxy_type": None, "implementations": None, "is_scam": None,
            "is_contract": None, "creator_address_hash": None, "creation_transaction_hash": None,
        }
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (
                patch.object(security_check, "ROOT", root), patch.object(security_check, "CONFIG", root),
                patch.object(security_check, "goplus_check", return_value=({"status": "ok", "fields": goplus_fields}, goplus_fields)),
                patch.object(security_check, "run_wrapper", return_value={"token": {"name": "Token"}}),
                patch.object(security_check, "blockscout_contract_check", return_value=api_unknown),
                patch.object(security_check, "evm_contract_check", return_value=(
                    {"status": "ok", "is_contract": True, "is_proxy": False, "is_proxy_rpc": False},
                    {"is_contract": True, "is_proxy": False, "is_proxy_rpc": False},
                )),
                patch.object(sys, "argv", ["security-check", "--chain", "4663", "--address", address]),
                redirect_stdout(output),
            ):
                self.assertEqual(security_check.main(), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["data_status"], "partial")
        self.assertIn("blockscout", result["unknowns"])
        self.assertIsNone(result["checks"]["contract"]["fields"]["source_verified"])

    def test_blockscout_error_does_not_expose_api_key(self):
        secret = "unit-test-secret"
        with patch.dict("os.environ", {"BLOCKSCOUT_API_KEY": secret}), patch.object(
            security_check.urllib.request, "urlopen", side_effect=RuntimeError(f"bad URL apikey={secret}"),
        ):
            with self.assertRaisesRegex(RuntimeError, "Blockscout API request failed") as caught:
                security_check.blockscout_get("/addresses/0x1234")
            request = security_check.urllib.request.urlopen.call_args.args[0]
            self.assertTrue(parse_qs(urlsplit(request.full_url).query).get("apikey"))
        self.assertNotIn(secret, str(caught.exception))

    def test_eip1967_beacon_proxy_detection(self):
        token = "0x" + "11" * 20
        beacon = "0x" + "22" * 20
        implementation = "0x" + "33" * 20
        storage = {
            security_check.IMPL_SLOT: "0x" + "0" * 64,
            security_check.ADMIN_SLOT: "0x" + "0" * 64,
            security_check.BEACON_SLOT: "0x" + "0" * 24 + beacon[2:],
        }

        def rpc(url, method, params):
            if method == "eth_getCode":
                return "0x6000"
            if method == "eth_getStorageAt":
                return storage[params[1]]
            if method == "eth_call" and params[0].get("to") == beacon:
                self.assertEqual(params[0]["data"], "0x5c60da1b")
                return "0x" + "0" * 24 + implementation[2:]
            if method == "eth_call":
                raise RuntimeError("owner unavailable")
            raise AssertionError(method)

        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory)
            (config / "rpc.json").write_text(json.dumps({"chains": {"base": {
                "rpc_candidates": [{"url": "https://rpc.invalid", "provider": "test"}],
            }}}), encoding="utf-8")
            with patch.object(security_check, "CONFIG", config), patch.object(security_check, "rpc_call", side_effect=rpc):
                fields, facts = security_check.evm_contract_check("base", token)
        self.assertEqual(fields["proxy_standard"], "eip1967-beacon")
        self.assertEqual(fields["beacon"], beacon)
        self.assertEqual(fields["implementation"], implementation)
        self.assertTrue(facts["is_proxy"])


if __name__ == "__main__":
    unittest.main()
