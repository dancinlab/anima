import json
import os
import sys
import tempfile
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "core"))

from workspace_curriculum import build_workspace_curriculum


class WorkspaceCurriculumTest(unittest.TestCase):
    def test_split_is_deterministic_and_has_no_exact_leakage(self):
        lines = [f"source sentence number {i} carries distinct causal material safely"
                 for i in range(40)]
        with tempfile.TemporaryDirectory() as td:
            source = os.path.join(td, "source.txt")
            out = os.path.join(td, "train.txt")
            with open(source, "w", encoding="utf-8") as dst:
                dst.write("\n".join(lines + [lines[0]]) + "\n")
            manifest, path = build_workspace_curriculum([source], out, 0.25, 19)
            self.assertTrue(manifest["leakage_free"])
            self.assertEqual(manifest["source_overlap"], 0)
            self.assertEqual(manifest["record_overlap"], 0)
            self.assertEqual(sum(manifest["source_lines"].values()), 40)
            self.assertTrue(os.path.exists(out + ".heldout.txt"))
            with open(path, encoding="utf-8") as src:
                self.assertEqual(json.load(src), manifest)

            out2 = os.path.join(td, "train2.txt")
            again, _ = build_workspace_curriculum([source], out2, 0.25, 19)
            self.assertEqual(again["source_sha256"], manifest["source_sha256"])
            self.assertEqual(again["record_sha256"], manifest["record_sha256"])


if __name__ == "__main__":
    unittest.main()
