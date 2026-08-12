import importlib.util
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "state/anima_303m_r4_mouth_diagnostics_2026_08_13/run_diagnostics.py"
SPEC = importlib.util.spec_from_file_location("r4_mouth_diagnostics", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_first_divergence_distinguishes_equal_prefix_and_length():
    assert MODULE._first_divergence(b"abc", b"abc") is None
    assert MODULE._first_divergence(b"axc", b"abc") == 1
    assert MODULE._first_divergence(b"abc", b"abcd") == 3


def test_repeat_diagnostics_are_literal_and_deterministic():
    assert MODULE._longest_byte_run(b"aabbbbcc") == 4
    assert MODULE._longest_byte_run(b"") == 0
    assert MODULE._longest_word_run("the the the end end") == 3
    assert MODULE._longest_word_run("toure, TOURE! another") == 2


def test_checkpoint_series_uses_final_and_registered_intermediate_names(tmp_path):
    base = tmp_path / "ladder_100_turn"
    assert MODULE._checkpoint_path(base, 100).name == "ladder_100_turn.bin.step100.bin"
    assert MODULE._checkpoint_path(base, 600).name == "ladder_100_turn.bin"


def test_diagnostic_uses_core_serializer_not_cli_shadow():
    assert MODULE.serializer.__name__ == "core.serialize"
    assert callable(MODULE.serializer.deserialize_bytegpt)


def test_diagnostic_direct_cli_imports_from_repo_root():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"], cwd=ROOT,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    assert completed.returncode == 0, completed.stderr
    assert "--artifacts" in completed.stdout


def test_trace_aggregation_is_byte_weighted():
    rows = [
        {"bytes": 1, "ce": 1.0, "top1_accuracy": 1.0,
         "mean_gold_probability": 0.5, "mean_gold_rank": 1.0},
        {"bytes": 3, "ce": 3.0, "top1_accuracy": 0.0,
         "mean_gold_probability": 0.1, "mean_gold_rank": 5.0},
    ]
    result = MODULE._aggregate_trace(rows)
    assert result["bytes"] == 4
    assert result["ce"] == 2.5
    assert result["top1_accuracy"] == 0.25
    assert abs(result["mean_gold_probability"] - 0.2) < 1e-12
    assert result["mean_gold_rank"] == 4.0


def test_validation_reuses_existing_multiturn_exchange_parser():
    seed, target = MODULE.v1._exchange(
        "user: remember blue\nassistant: okay\nuser: which color?\nassistant: blue")
    assert seed.endswith("user: which color?\nassistant: ")
    assert target == "blue"
