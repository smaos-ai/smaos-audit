import unittest
import os
import json
from smaos_audit import __version__
from smaos_audit.reporter import generate_dora_report, generate_mermaid_trace

class TestPipeline(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, "0.1.0")

    def test_reporter_generation(self):
        mermaid_path = "/tmp/test_audit_trace.mermaid"
        json_path = "/tmp/test_dora_report.json"
        
        generate_mermaid_trace(mermaid_path)
        generate_dora_report(json_path)
        
        self.assertTrue(os.path.exists(mermaid_path))
        self.assertTrue(os.path.exists(json_path))
        
        with open(json_path) as f:
            data = json.load(f)
            self.assertIn("incident_classification", data)
            self.assertEqual(data["incident_classification"], "Major")
            
        if os.path.exists(mermaid_path): os.remove(mermaid_path)
        if os.path.exists(json_path): os.remove(json_path)

if __name__ == "__main__":
    unittest.main()
