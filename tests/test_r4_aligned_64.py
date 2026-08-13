import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCRIPT=ROOT/"state/anima_303m_r4_aligned_64_exposure_2026_08_13/run_64.py"
def test_cli():
 c=subprocess.run([sys.executable,str(SCRIPT),"--help"],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert c.returncode==0,c.stderr
