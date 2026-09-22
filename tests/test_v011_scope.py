import unittest
from smaos_audit.dispatcher import TraceRecord, DeterministicDispatcher
from smaos_audit.bundler import ActionBundle
from smaos_audit.interrogator import ForensicInterrogator
from smaos_audit.reflector import WireTruthReflector
from smaos_audit.compaction_checker import CompactionSafetyGate

class TestV011Scope(unittest.TestCase):
    def test_mobile_logcat_parsing(self):
        logcat_line = "09-22 03:00:12.123 1234 5678 I ArtemisAgent: [ACTION_CLICK] button:id/checkout_confirm amount=250.00 status=CONFIRMED"
        rec = TraceRecord.from_line(logcat_line, line_no=1, byte_offset=0)
        self.assertTrue(rec.is_mutating())
        self.assertEqual(rec.claimed_verdict, "CONFIRMED")
        self.assertEqual(rec.http_status, 200)

        # 504 timeout logcat line
        logcat_504 = "09-22 03:00:14.456 1234 5678 W PaymentGateway: [HTTP_POST] url='/api/v1/charge' status=504 error='GATEWAY_TIMEOUT'"
        rec_504 = TraceRecord.from_line(logcat_504, line_no=2, byte_offset=120)
        self.assertTrue(rec_504.has_wire_fault())
        self.assertEqual(rec_504.claimed_verdict, "UNKNOWN")
        self.assertEqual(rec_504.http_status, 504)

    def test_jev_intent_vs_wire_settlement_collision(self):
        trace_dict = {
            "action_id": "act-jev-001",
            "type": "WIRE_TRANSFER",
            "http_status": 504,
            "wire_fault": "504",
            "verdict": "CONFIRMED",
            "jev_intent": "allow"
        }
        rec = TraceRecord(
            record=trace_dict,
            line_no=1,
            byte_offset=0,
            action_id="act-jev-001",
            action_type="WIRE_TRANSFER",
            http_method="POST",
            http_status=504,
            wire_fault="504",
            claimed_verdict="CONFIRMED",
            is_mutation_flag=True
        )
        bundle = ActionBundle(
            bundle_id="b-jev-001",
            action_id="act-jev-001",
            idempotency_key=None,
            traces=[rec],
            wire_facts={"has_wire_fault": True}
        )
        interrogator = ForensicInterrogator()
        findings = interrogator.evaluate_bundle(bundle)
        categories = [f.category for f in findings]
        self.assertIn("JEV_INTENT_WIRE_FAULT_COLLISION", categories)

    def test_context_compaction_safety_gate(self):
        baseline = "System Policy: Enforce DORA Art. 17 compliance. If HTTP 504 occurs, verdict MUST be UNKNOWN."
        safe_compacted = "System Policy: Enforce DORA Art. 17 compliance. If HTTP 504 occurs, verdict MUST be UNKNOWN."
        metrics = CompactionSafetyGate.evaluate(baseline, safe_compacted)
        self.assertTrue(metrics.is_safe())
        self.assertEqual(metrics.delta_cvr, 100.0)

        unsafe_compacted = "System Policy: Hello world."
        unsafe_metrics = CompactionSafetyGate.evaluate(baseline, unsafe_compacted)
        self.assertFalse(unsafe_metrics.is_safe())
        self.assertEqual(unsafe_metrics.verdict, "FAIL_CONSTRAINT_DECAY")

if __name__ == "__main__":
    unittest.main()
