#!/usr/bin/env python3
"""H_9235 fork-A CLML lane trainer (numpy · torch-free · CACHED frozen-trunk yn+logits · CPU minutes · $0).
Trains ONLY the lane {W1,b1,W2,w_g,b_g} (trunk frozen) on composed-position next-byte CE, so the lane learns
the RESIDUAL the additive readout misses — routing both concepts (present in the definition context, mean-pool
recoverable per H2-lite) to the composed output. Op order MIRRORS core/clml.lane_apply / CLMLModule (2-prod parity).
  logits = base_logits(lane-OFF) + clip( gate · gelu(causal_mean·W1+b1)·W2 , ±tau ) ; gate = σ(w_g·[yn_last;mean]+b_g)
Loss = CE(logits, next_byte) + λ_gate·|gate| (silence pressure). Frozen-first: bars in FREEZE, no tune-to-green.
Emits clml_lane.npz (W1,b1,W2,w_g,b_g,r,tau) → append_clml_trailer wires it into the .clm.
INPUT: train_hidden.npz (t*__seq [T,d], t*__logits [V]), train_prompts.json (targets). ⚠ scope a_scale_honest_scope:
trained on a subsample of composed positions; verdict = engine-native system-G1 lane-ON/OFF ablation, NOT train CE."""
import sys
import json
import numpy as np

NPZ = sys.argv[1] if len(sys.argv) > 1 else "train_hidden.npz"
PROMPTS = sys.argv[2] if len(sys.argv) > 2 else "train_prompts.json"
OUT = sys.argv[3] if len(sys.argv) > 3 else "clml_lane.npz"
R = 128
TAU = 8.0
STEPS = 8000
LR = 0.02
LGATE = 0.01
SEED = 7

def gelu(x): return 0.5 * x * (1 + np.tanh(0.7978845608028654 * (x + 0.044715 * x**3)))
def dgelu(x):
    t = np.tanh(0.7978845608028654 * (x + 0.044715 * x**3))
    s = 1 - t**2
    return 0.5 * (1 + t) + 0.5 * x * s * 0.7978845608028654 * (1 + 3 * 0.044715 * x**2)
def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))

spec = json.load(open(PROMPTS))
items = spec["items"]
Z = np.load(NPZ)
ids = [it["id"] for it in items if (it["id"] + "__seq") in Z.files and (it["id"] + "__logits") in Z.files]
tgt = {it["id"]: it["target"] for it in items}
T, d = Z[ids[0] + "__seq"].shape
V = Z[ids[0] + "__logits"].shape[0]
print("examples=%d T=%d d=%d V=%d" % (len(ids), T, d, V), flush=True)

# precompute per-example lane inputs: yn_last (d,), c_last = causal mean over T (d,), base_logits (V,), y target
YN = np.zeros((len(ids), d), dtype=np.float64)   # yn at last position
CM = np.zeros((len(ids), d), dtype=np.float64)   # causal mean over the T window (= mean over all T since last pos)
BL = np.zeros((len(ids), V), dtype=np.float64)
Y = np.zeros(len(ids), dtype=np.int64)
for i, pid in enumerate(ids):
    seq = Z[pid + "__seq"].astype(np.float64)     # [T,d]
    YN[i] = seq[T - 1]
    CM[i] = seq.mean(axis=0)                       # causal cumulative mean at last pos = full-window mean
    BL[i] = Z[pid + "__logits"].astype(np.float64)
    Y[i] = tgt[pid]
GIN = np.concatenate([YN, CM], axis=1)            # [N, 2d] gate input

rng = np.random.default_rng(SEED)
W1 = rng.standard_normal((d, R)) * (1/np.sqrt(d)); b1 = np.zeros(R)
W2 = rng.standard_normal((R, V)) * 0.02
w_g = np.zeros(2 * d); b_g = -2.0                 # start gate ~closed (silence prior)
N = len(ids)

def logsoftmax_ce(logits, y):
    m = logits.max(1, keepdims=True)
    lse = m[:, 0] + np.log(np.exp(logits - m).sum(1))
    return (lse - logits[np.arange(len(y)), y]).mean()

for step in range(STEPS):
    bi = rng.integers(0, N, 256)
    c = CM[bi]; gin = GIN[bi]; base = BL[bi]; y = Y[bi]
    pre = c @ W1 + b1                              # [B,R]
    z = gelu(pre)                                  # [B,R]
    raw = z @ W2                                   # [B,V]
    gate = sigmoid(gin @ w_g + b_g)                # [B]
    delta = np.clip(gate[:, None] * raw, -TAU, TAU)
    logits = base + delta
    # softmax grad
    m = logits.max(1, keepdims=True); e = np.exp(logits - m); p = e / e.sum(1, keepdims=True)
    g = p.copy(); g[np.arange(len(y)), y] -= 1; g /= len(y)     # dCE/dlogits
    # through clip (approx: pass-through where |raw*gate|<TAU)
    unclipped = (np.abs(gate[:, None] * raw) < TAU).astype(np.float64)
    gdelta = g * unclipped
    # gate + raw
    graw = gdelta * gate[:, None]                  # dL/draw
    ggate = (gdelta * raw).sum(1)                  # dL/dgate (pre-sigmoid handled below)
    ggate += LGATE * np.sign(gate) * (gate * (1 - gate))   # L1 silence pressure on gate (via sigmoid)
    ggate_pre = ggate * gate * (1 - gate)
    gW2 = z.T @ graw
    gz = graw @ W2.T
    gpre = gz * dgelu(pre)
    gW1 = c.T @ gpre; gb1 = gpre.sum(0)
    gwg = gin.T @ ggate_pre; gbg = ggate_pre.sum()
    W2 -= LR * gW2; W1 -= LR * gW1; b1 -= LR * gb1; w_g -= LR * gwg; b_g -= LR * gbg
    if step % 1000 == 0 or step == STEPS - 1:
        full_pre = CM @ W1 + b1; full_z = gelu(full_pre); full_raw = full_z @ W2
        full_gate = sigmoid(GIN @ w_g + b_g)
        full_logits = BL + np.clip(full_gate[:, None] * full_raw, -TAU, TAU)
        ce_on = logsoftmax_ce(full_logits, Y); ce_off = logsoftmax_ce(BL, Y)
        print("step %5d  CE lane-ON=%.4f lane-OFF=%.4f  Δ=%+.4f  gate_mean=%.3f" %
              (step, ce_on, ce_off, ce_on - ce_off, float(full_gate.mean())), flush=True)

# final report
full_pre = CM @ W1 + b1; full_z = gelu(full_pre); full_raw = full_z @ W2
full_gate = sigmoid(GIN @ w_g + b_g)
full_logits = BL + np.clip(full_gate[:, None] * full_raw, -TAU, TAU)
ce_on = logsoftmax_ce(full_logits, Y); ce_off = logsoftmax_ce(BL, Y)
acc_on = float((full_logits.argmax(1) == Y).mean()); acc_off = float((BL.argmax(1) == Y).mean())
print("FINAL composed-pos: CE lane-ON=%.4f OFF=%.4f (Δ%+.4f) · next-byte acc ON=%.3f OFF=%.3f · gate=%.3f" %
      (ce_on, ce_off, ce_on - ce_off, acc_on, acc_off, float(full_gate.mean())), flush=True)
np.savez(OUT, W1=W1.astype("<f4"), b1=b1.astype("<f4"), W2=W2.astype("<f4"),
         w_g=w_g.astype("<f4"), b_g=np.float32(b_g), r=np.int64(R), tau=np.float32(TAU))
json.dump({"ce_on": ce_on, "ce_off": ce_off, "ce_delta": ce_on - ce_off, "acc_on": acc_on,
           "acc_off": acc_off, "gate_mean": float(full_gate.mean()), "n": N, "steps": STEPS},
          open("clml_train_RESULT.json", "w"), indent=2)
print("saved lane → " + OUT)
