import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from demo import ROOT, load_yaml, load_json, RefundSandbox, editorial


class DemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = load_yaml(ROOT / "config/refund.yaml")
        cls.orders = load_json(ROOT / "fixtures/orders.json")

    def test_62_ron_simulated(self):
        result = RefundSandbox(self.cfg, self.orders["ok"]).run()
        self.assertEqual(result["status"], "DONE_SIMULATED")
        self.assertEqual(result["sandbox_refund"]["amount"], "62.00")
        self.assertIn("verify_refund", result["actions"])

    def test_350_ron_escalated(self):
        self.assertEqual(RefundSandbox(self.cfg, self.orders["above_limit"]).run()["status"], "ESCALATED")

    def test_missing_evidence_waits(self):
        self.assertEqual(RefundSandbox(self.cfg, self.orders["missing_proof"]).run()["status"], "WAITING_CUSTOMER")

    def test_existing_refund_not_repeated(self):
        self.assertEqual(RefundSandbox(self.cfg, self.orders["duplicate"]).run()["status"], "ESCALATED")

    def test_unverified_customer_escalated(self):
        self.assertEqual(RefundSandbox(self.cfg, self.orders["unverified"]).run()["status"], "ESCALATED")

    def test_model_cannot_bypass_dispatcher(self):
        runner = RefundSandbox(self.cfg, self.orders["above_limit"])
        runner.dispatch("prepare_refund")
        self.assertEqual(runner.status, "ESCALATED")
        self.assertIsNone(runner.ledger.get(runner.request_id))

    def test_idempotent_sandbox_ledger(self):
        ledger = {}
        RefundSandbox(self.cfg, self.orders["ok"], ledger).run()
        RefundSandbox(self.cfg, self.orders["ok"], ledger).run()
        self.assertEqual(len(ledger), 1)

    def test_youtube_drafts_not_videos(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "drafts.json"
            result = editorial(load_yaml(ROOT / "config/youtube.yaml"), output)
            artifact = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "WAITING_HUMAN_APPROVAL")
            self.assertEqual(len(artifact["production"]["variants"]), 3)
            self.assertFalse(result["publisher_enabled"])
            self.assertFalse(artifact["production"]["rendered_video"])


if __name__ == "__main__":
    unittest.main()
