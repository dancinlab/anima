import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "state/anima_303m_v1_context_micro_2026_08_12/run_micro.py"
SPEC = importlib.util.spec_from_file_location("v1_context_micro", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_exchange_preserves_full_multiturn_seed():
    document = "user: one\nassistant: two\nuser: three\nassistant: four"
    seed, target = MODULE._exchange(document)
    assert seed == "user: one\nassistant: two\nuser: three\nassistant: "
    assert target == "four"


def test_exchange_rejects_broken_roles():
    try:
        MODULE._exchange("user: one\nuser: two\nassistant: three")
    except RuntimeError as exc:
        assert "alternate" in str(exc)
    else:
        raise AssertionError("broken roles were accepted")
