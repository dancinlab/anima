"""Step-1 decode-smoke — prove the 3B .clm is engine-loadable + generates bytes via the
CANONICAL engine-native anima_py.core.decode path (a_eval_py_canonical). Reports peak RSS.
Precision via ANIMA_DTYPE (float64 canonical / float32|float16 DIRECTIONAL) + RAM guard."""
import sys, os, math, time, resource
import numpy as np
import dtype_patch
name = dtype_patch.install(require_headroom=True)
from anima_py.core import decode as dec

clm = sys.argv[1]
T = 24
t0 = time.time()
print(f"decode-smoke: {clm}  dtype={name}", flush=True)
print(f"decodable={dec.clm_decodable(clm)}  config={dec.clm_config(clm)}", flush=True)
W = dec.clm_load_weights(clm)
assert W.get("ok"), "load failed"
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024**2)
print(f"LOADED d={W['d']} E={W['E']} V={W['V']} L={W['L']} K={W['K']} in {time.time()-t0:.1f}s peakRSS={rss:.2f}GB", flush=True)

seed = "The mind is a fire to "
tok = dec._seed_to_tok(seed, T)
logits = dec._fwd_logits(W, tok, T)
V = W["V"]
tgt = np.concatenate([tok[1:], [ord('b')]])
ce = dec.nn_ce_loss_allpos(logits, tgt, T, V)
print(f"decode-sanity CE_realtext={ce:.5f} < uniform_lnV={math.log(V):.5f}: {ce < math.log(V)}", flush=True)

cur = tok.copy(); gen = []
for _ in range(16):
    lg = dec._fwd_logits(W, cur, T)
    nb = int(np.argmax(lg[T-1])); gen.append(nb)
    cur = np.concatenate([cur[1:], [float(nb)]])
gb = bytes(gen)
print(f"GENERATED 16 bytes from {seed!r}: {gb!r} (text={gb.decode('utf-8','replace')!r})", flush=True)
print(f"SMOKE OK total={time.time()-t0:.1f}s peakRSS={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024**2):.2f}GB", flush=True)
