import unittest
import json
import os

class TestConformance(unittest.TestCase):
    def test_fixtures_jsonl_validity(self):
        fixture_path = "fixtures/sample_staging_traces.jsonl"
        self.assertTrue(os.path.exists(fixture_path))
        
        line_count = 0
        with open(fixture_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    record = json.loads(line)
                    self.assertIn("trace_id", record)
                    self.assertIn("status", record)
                    line_count += 1
        self.assertGreater(line_count, 0)

    def test_wasm_binary_header(self):
        wasm_path = "verifier/smaos_verify_bg.wasm"
        self.assertTrue(os.path.exists(wasm_path))
        with open(wasm_path, "rb") as f:
            header = f.read(4)
            self.assertEqual(header, b"\x00asm")

if __name__ == "__main__":
    unittest.main()
