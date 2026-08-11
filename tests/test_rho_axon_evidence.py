import os
import sys
import json
import tempfile
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(ROOT, "cli")
if CLI not in sys.path:
    sys.path.insert(0, CLI)

import rho_axon
import evaluate


class _Mouth:
    def ideate(self, seed, gen, top_k, temp, seed_rng):
        return "known words remain coherent"


class RhoFormEvidenceTest(unittest.TestCase):
    def test_raw_text_kwr_and_shuffle_score_are_retained(self):
        def kwr(text, known):
            words = text.split()
            return sum(word in known for word in words) / max(1, len(words))

        result = rho_axon.rho_form(
            _Mouth(), 40, {"known", "words", "remain", "coherent"}, kwr,
            ["one", "two"], gate=0.7)

        self.assertEqual(result["verdict"], rho_axon.PASS)
        self.assertEqual(len(result["evidence"]), 2)
        for item in result["evidence"]:
            self.assertEqual(item["text"], "known words remain coherent")
            self.assertEqual(item["known_word_ratio"], 1.0)
            self.assertTrue(item["pass"])
            self.assertIn("shuffle_known_word_ratio", item)
            self.assertIn("shuffle_pass", item)

    def test_raw_surrogate_byte_is_written_losslessly(self):
        raw = b"answer:\xec".decode("utf-8", "surrogateescape")
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "rho.json")
            evaluate.write_rho_panel(path, {"evidence": [{"text": raw}]})
            with open(path, "r", encoding="utf-8") as handle:
                restored = json.load(handle)["evidence"][0]["text"]
        self.assertEqual(restored.encode("utf-8", "surrogateescape"), b"answer:\xec")


if __name__ == "__main__":
    unittest.main()
