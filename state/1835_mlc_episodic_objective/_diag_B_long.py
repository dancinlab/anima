# Exploratory B-only diagnostic (NOT part of frozen bar): does more compute let the MLC arm
# master seen in-context composition, and does held-out (novel-primitive) transfer then lift?
import importlib.util,sys
spec=importlib.util.spec_from_file_location("m","mlc_episodic_probe.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cfg=dict(D=64,H=4,nblock=2,ff=128,ctx=64)
for steps in (12000,):
    cd,fl,seen=m.run('B',7,cfg,steps,32,1.5e-3)
    print(f"[diag] B seed=7 steps={steps}: seen_acc={seen}/9  composed_distinct(held)={cd}/4  CE={fl:.3f}",flush=True)
