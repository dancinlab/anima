import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCRIPT=ROOT/"state/anima_303m_r4_aligned_100_2026_08_13/run_aligned_100.py";PROTOCOL=ROOT/"state/anima_303m_r4_aligned_100_exposure_2026_08_13/protocol.json"
def test_protocol_override_cli():
 c=subprocess.run([sys.executable,str(SCRIPT),"--help"],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert c.returncode==0,c.stderr;assert "--protocol" in c.stdout
