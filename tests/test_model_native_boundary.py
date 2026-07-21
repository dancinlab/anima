from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ModelNativeBoundaryTests(unittest.TestCase):
    def test_python_answer_scaffold_modules_are_absent(self) -> None:
        removed = (
            "core/cognitive_workspace.py",
            "core/workspace_logic.py",
            "core/workspace_mouth.py",
            "core/workspace_evidence.py",
            "core/workspace_production.py",
            "core/workspace_runtime.py",
        )
        for relative in removed:
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_removed_evaluate_flags_are_rejected(self) -> None:
        command = [sys.executable, str(ROOT / "cli/evaluate.py"), "--workspace-smoke"]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown flag --workspace-smoke", result.stderr)

    def test_help_exposes_only_model_native_gates(self) -> None:
        command = [sys.executable, str(ROOT / "cli/evaluate.py"), "--help"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertNotIn("--workspace", result.stdout)
        self.assertIn("--rho-axon", result.stdout)

    def test_workspace_decode_cache_is_absent(self) -> None:
        generator = (ROOT / "core/generator.py").read_text(encoding="utf-8")
        self.assertNotIn("_decode_cache", generator)


if __name__ == "__main__":
    unittest.main()
