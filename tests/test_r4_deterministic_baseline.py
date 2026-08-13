import importlib.util
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "state/anima_303m_r4_deterministic_baseline_2026_08_13/run_gate.py"
SPEC = importlib.util.spec_from_file_location("r4_deterministic_gate", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_deterministic_gate_cli_imports_from_repo_root():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"], cwd=ROOT,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    assert completed.returncode == 0, completed.stderr
    assert "--data" in completed.stdout


def test_deterministic_gate_compares_tensor_values(tmp_path):
    import torch

    common = {
        "optimizer": {}, "completed_step": 1, "endpoint_steps": 1,
        "recipe": {"deterministic": True}, "rng": {}, "sampled_windows": [],
        "state_digest": "same",
    }
    torch.save({**common, "model": {"w": torch.tensor([1.0])}}, tmp_path / "a.pt")
    torch.save({**common, "model": {"w": torch.tensor([1.0])}}, tmp_path / "b.pt")
    equal = MODULE._model_equal(tmp_path / "a.pt", tmp_path / "b.pt")
    assert equal["all_tensors_equal"]
    assert equal["maximum_absolute_error"] == 0.0
