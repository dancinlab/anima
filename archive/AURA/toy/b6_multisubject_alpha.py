#!/usr/bin/env python3
"""AURA B6 — multi-subject alpha-power awake/sed replication (B4.1 recipe, ds005620).
Transient analysis tool: numpy FFT over GB-scale BrainVision IEEE_FLOAT_32 binary EEG.
honest: scalp-proxy, alpha-power, report actual N. No fabrication."""
import numpy as np, os, math

RAW = "/Users/ghost/core/anima/DATASET/eeg_consciousness_level/raw/ds005620"
NCH, STRIDE, FS, WIN, NWIN = 65, 20, 250.0, 1000, 10
ALPHA_LO, ALPHA_HI = 8.0, 13.0
EAR = [18, 28, 29, 37]; MIDLINE = [51, 33, 13, 2]
SUBJECTS = ["1010", "1033", "1022"]

def load_decimated(p):
    raw = np.fromfile(p, dtype="<f4"); npt = raw.size // NCH
    return raw[:npt*NCH].reshape(npt, NCH)[::STRIDE, :].T

def alpha_power(sig):
    sig = sig - sig.mean()
    psd = np.abs(np.fft.rfft(sig))**2
    f = np.fft.rfftfreq(sig.size, d=1.0/FS)
    p = psd[(f>=ALPHA_LO)&(f<=ALPHA_HI)].sum()
    return math.log10(p) if p>0 else float("nan")

def montage_windows(dec, idx):
    m = dec[idx,:].mean(axis=0); out=[]
    for w in range(NWIN):
        seg = m[w*WIN:(w+1)*WIN]
        if seg.size < WIN: break
        out.append(alpha_power(seg))
    return np.array(out)

def paired_t(d):
    d = d[~np.isnan(d)]; n=d.size
    if n<2: return float("nan"), n
    md, sd = d.mean(), d.std(ddof=1)
    if sd==0: return (float("inf") if md!=0 else 0.0), n
    return md/(sd/math.sqrt(n)), n

def fpath(sub, kind):
    f = "task-awake_acq-EO_eeg.eeg" if kind=="awake" else "task-sed_acq-rest_run-1_eeg.eeg"
    return os.path.join(RAW, f"sub-{sub}", "eeg", f"sub-{sub}_{f}")

def main():
    montages = {"EAR": EAR, "MIDLINE": MIDLINE}
    print(f"# B6 multi-subject alpha-power | sought: {SUBJECTS}")
    results = {n:{} for n in montages}; avail=[]
    for sub in SUBJECTS:
        ap, sp = fpath(sub,"awake"), fpath(sub,"sed")
        if not (os.path.exists(ap) and os.path.exists(sp)):
            print(f"sub-{sub}: MISSING (awake={os.path.exists(ap)} sed={os.path.exists(sp)}) -> skip"); continue
        avail.append(sub)
        da, ds = load_decimated(ap), load_decimated(sp)
        print(f"sub-{sub}: awake T={da.shape[1]} sed T={ds.shape[1]} (dec@250Hz)")
        for name, idx in montages.items():
            wa, ws = montage_windows(da,idx), montage_windows(ds,idx)
            delta = wa-ws; sign=int((delta>0).sum()); t,n=paired_t(delta)
            results[name][sub] = dict(awake=float(np.nanmean(wa)), sed=float(np.nanmean(ws)),
                                      d=float(np.nanmean(delta)), sign=sign, n=n, t=float(t))
            print(f"  {name:8s} awake={np.nanmean(wa):.3f} sed={np.nanmean(ws):.3f} "
                  f"d={np.nanmean(delta):+.3f} sign={sign}/{n} t({n-1})={t:+.2f}")
    N=len(avail); print(f"\n# AGGREGATE (N={N}: {avail})")
    for name in montages:
        subs=results[name]
        if not subs: continue
        deltas=[subs[s]["d"] for s in avail]
        dir_pos=sum(1 for d in deltas if d>0); mean_d=float(np.mean(deltas))
        ct,cn=paired_t(np.array(deltas))
        print(f"  {name:8s} awake>sed in {dir_pos}/{N} subj | cross-subj mean d={mean_d:+.3f} | t({cn-1})={ct:+.2f}")

if __name__=="__main__": main()
