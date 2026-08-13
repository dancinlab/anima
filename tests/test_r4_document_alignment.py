import importlib.util
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "state/anima_303m_r4_document_alignment_2026_08_13/run_alignment.py"
SPEC = importlib.util.spec_from_file_location("r4_document_alignment", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_document_alignment_cli_imports_from_repo_root():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"], cwd=ROOT,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    assert completed.returncode == 0, completed.stderr
    assert "--data" in completed.stdout
