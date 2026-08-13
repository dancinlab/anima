import importlib.util
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "state/anima_303m_r4_four_doc_2026_08_13/run_experiment.py"
SPEC = importlib.util.spec_from_file_location("r4_four_document", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_four_document_decision_table_is_fail_closed():
    assert MODULE._classify(False, {"O1_horizon": True}) == "INVALID-BASELINE-MISMATCH"
    assert MODULE._classify(True, {"O1_horizon": True}) == (
        "SUPPORTED-INSUFFICIENT-OPTIMIZATION-HORIZON")
    assert MODULE._classify(True, {"C1_width": True}) == (
        "SUPPORTED-TINY-CAPACITY-OR-GEOMETRY")
    assert MODULE._classify(True, {"O1_horizon": True, "C2_depth": True}) == (
        "SUPPORTED-BOTH-HORIZON-AND-CAPACITY")
    assert MODULE._classify(True, {}) == (
        "FALSIFIED-BOUNDED-HORIZON-AND-CAPACITY-TREATMENTS")


def test_checkpoint_paths_use_registered_intermediate_convention(tmp_path):
    base = tmp_path / "o1_horizon"
    assert MODULE._checkpoint_path(base, 2400, 600).name == (
        "o1_horizon.bin.step600.bin")
    assert MODULE._checkpoint_path(base, 2400, 2400).name == "o1_horizon.bin"


def test_four_document_cli_imports_from_repo_root():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"], cwd=ROOT,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    assert completed.returncode == 0, completed.stderr
    assert "--data" in completed.stdout


def test_exact_gate_is_unreachable_beyond_canonical_generation_budget():
    at_budget = [("short", "x" * MODULE.generator.CHAT_MAX_NEW_BYTES)]
    over_budget = [("short", "x" * (MODULE.generator.CHAT_MAX_NEW_BYTES + 1))]
    assert MODULE._exact_gate_reachability(at_budget)["exact_completion_reachable"]
    assert not MODULE._exact_gate_reachability(over_budget)["exact_completion_reachable"]
