#!/usr/bin/env python3
"""AURA C0 n=8 multi-window montage big-Phi harness extractor (ds005620 sub-1010 awake)."""
import numpy as np
EEG = "/Users/ghost/core/anima/DATASET/eeg_consciousness_level/raw/ds005620/sub-1010/eeg/sub-1010_task-awake_acq-EO_eeg.eeg"
NCH, STRIDE, NSAMP = 65, 20, 1000
FRONTAL = [53, 51, 49, 57, 55, 47, 43, 41]   # F3 Fz F4 AFz F7 F8 FC1 FC2
MOTOR   = [35, 33, 31, 32, 34, 36, 30, 23]    # C3 Cz C4 C2 C1 C5 C6 CPz
OFFSETS = [0, 140000, 280000, 420000, 560000, 700000, 840000, 980000, 1120000, 1260000]
OUTDIR = "/Users/ghost/core/anima/.claude/worktrees/agent-acb20d3eda30951b8/AURA/toy"
def load_raw():
    raw = np.fromfile(EEG, dtype="<f4"); npt = raw.size // NCH
    return raw[:npt*NCH].reshape(npt, NCH)
def window(mat, idx, off):
    dec = mat[off::STRIDE, :]
    if dec.shape[0] < NSAMP: return None
    return dec[:NSAMP, idx].T
def emit(name, idx, mat):
    L=[f"// AURA C0 n=8 real-EEG {name} montage — ds005620 sub-1010 awake, multi-window.",
       f"// channels (0-based idx): {idx}",
       "// channel-major flat s[ch*n_samp+t], BrainVision IEEE_FLOAT_32, sys=255 (2^8-1).",
       'import "/Users/ghost/core/anima/BRAIN/eeg/eeg_to_tpm.hexa"', ""]
    used=[]
    for w,off in enumerate(OFFSETS):
        seg=window(mat,idx,off)
        if seg is None: continue
        vals=",".join(f"{v:.4f}" for v in seg.reshape(-1))
        L.append(f"let DATA_{w} = [{vals}]"); used.append((w,off))
    L.append(""); L.append("fn main() {")
    for w,off in used:
        L.append(f'    let r{w} = eeg_big_phi(DATA_{w}, 8, 1000, 255)')
        L.append(f'    println("C0 n=8 {name} off={off} bigPhi=" + str(r{w}[0]) + " total=" + str(r{w}[1]))')
    L.append("}")
    out=f"{OUTDIR}/c0_n8_{name.lower()}.hexa"
    open(out,"w").write("\n".join(L)+"\n")
    print(f"wrote {out} ({len(used)} windows)")
    return [o for _,o in used]
mat=load_raw()
print(f"loaded: {mat.shape[0]} raw samples ({mat.shape[0]//STRIDE} dec @250Hz)")
emit("FRONTAL",FRONTAL,mat); emit("MOTOR",MOTOR,mat)
