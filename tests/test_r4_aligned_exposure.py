import importlib.util, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"state/anima_303m_r4_aligned_exposure_2026_08_13/run_exposure.py"
def test_exposure_cli_imports():
    c=subprocess.run([sys.executable,str(SCRIPT),"--help"],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    assert c.returncode==0,c.stderr
    assert "--data" in c.stdout
