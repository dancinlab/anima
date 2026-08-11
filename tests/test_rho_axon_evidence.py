import os
import sys
import json
import hashlib
import tempfile
import unittest
from unittest import mock


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(ROOT, "cli")
if CLI not in sys.path:
    sys.path.insert(0, CLI)

import rho_axon
import evaluate
import rho_fan


class _Mouth:
    def ideate(self, seed, gen, top_k, temp, seed_rng):
        return "known words remain coherent"


class RhoFormEvidenceTest(unittest.TestCase):
    def test_rho_panel_records_exact_lexicon_identity(self):
        known = {"alpha", "beta"}
        with mock.patch.object(evaluate, "_rho_fan_dict_load", return_value=known), \
             mock.patch.object(evaluate, "_Mouth", return_value=_Mouth()), \
             mock.patch.object(evaluate, "_MemoMouth", side_effect=lambda mouth, *_: mouth), \
             mock.patch.object(evaluate, "_g_load_corpus_tokens", return_value=set()), \
             mock.patch.object(rho_axon, "run_panel", return_value={"rho": {}}), \
             mock.patch.object(rho_axon, "render_panel", return_value="panel"), \
             mock.patch.object(rho_axon, "render_cells", return_value=""):
            panel = evaluate.eval_rho_axon(__file__, [], 40, include_cells=False)

        self.assertEqual(panel["instrument"], {
            "rho_form_words_sha256": rho_fan.RHO_FORM_WORDS_SHA256,
            "rho_form_words_count": 2,
        })

    def test_missing_word_lexicon_invalidates_instrument(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = os.path.join(directory, "missing-web2")
            with self.assertRaisesRegex(RuntimeError, "canonical Web2 lexicon is unavailable"):
                rho_fan._rho_fan_dict_load(missing)

    def test_word_lexicon_hash_is_pinned(self):
        raw = b"alpha\nbeta\n"
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "web2")
            with open(path, "wb") as handle:
                handle.write(raw)
            with self.assertRaisesRegex(RuntimeError, "lexicon hash mismatch"):
                rho_fan._rho_fan_dict_load(path)
            expected = hashlib.sha256(raw).hexdigest()
            with mock.patch.object(rho_fan, "RHO_FORM_WORDS_SHA256", expected):
                known = rho_fan._rho_fan_dict_load(path)
        self.assertIn("alpha", known)
        self.assertIn("beta", known)

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
