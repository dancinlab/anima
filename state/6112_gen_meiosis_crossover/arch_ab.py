#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H_6112 ladder rung 1.5 — REAL-TRUNK toy A/B for the meiosis-crossover operator.

DIRECTIONAL by construction (torch, not the live .hexa A<->G engine). NEVER terminal.
This upgrades the H_6112 claim from abstract-numpy probe -> real-trunk-toy: it wires the
disjoint-loci (meiosis-crossover) readout into the ACTUAL production trunk
(archive/train/clm/model/model.py :: CLMConvMoE) and trains it from scratch on next-byte CE.

=====================  DESIGN (mirrors the numpy probe as REAL sequences)  =====================
Two independent factors A (K states) and B (K states). Each training example is a byte sequence
    [BOS, A_i, B_j, C]
  BOS = 1 ; A_i = 10+i ; B_j = 40+j ; C = composed target byte = 100 + i*K + j
TRAIN = DIAGONAL only  (i,i)                     -> K sequences, the two factors perfectly co-vary
HELDOUT = OFF-DIAGONAL (i,j), i!=j               -> K*(K-1) NOVEL composed targets never seen
The model predicts C at the position of B_j (causal receptive field sees BOTH A_i and B_j).
CE is taken ONLY at that composition position (isolates the readout operator; same for both arms).

ARM ADDITIVE (= the walled baseline family):
    stock CLMConvMoE readout  nn.Conv1d(d, V=256, 1)  -> a MONOLITHIC softmax over composed bytes.
    Each composed class is an independent output row; off-diagonal classes get ZERO training
    gradient -> unreachable. (This is the additive-superposition readout.)

ARM MEIOSIS (= the disjoint-loci / meiosis-crossover operator wired into the SAME trunk):
    readout SPLIT into two heads over DISJOINT channel halves of the norm_out representation r:
        head_A = Linear(d/2 -> K)  reads r[:d/2]   (locus for factor A)
        head_B = Linear(d/2 -> K)  reads r[d/2:]   (locus for factor B)
    composed logit for byte 100+a*K+b  =  logit_A[a] + logit_B[b]   (outer-SUM = factorized).
    Because the joint distribution FACTORIZES, diagonal-only training that teaches head_A to read
    factor A and head_B to read factor B lets the outer-sum place mass on NOVEL (i,j) combos.
    NOTE: meiosis has FEWER readout params than additive (factored K+K vs monolithic K*K), so any
    meiosis win is an INDUCTIVE-BIAS win, not a capacity win (reported below).

Everything else (embed, dilated-conv trunk, MoE layer, GroupNorm) is the UNMODIFIED production
trunk, imported live from archive/train/clm/model/model.py. Same seed, same data, same steps.

=====================  FROZEN BAR  (pre-registered BEFORE any run; c9 no tune-to-green)  =========
  GREEN-DIRECTIONAL  iff  (per-seed  MEIOSIS_reach - ADDITIVE_reach >= 0.30  on >= 2/3 seeds)
                     AND  (mean ADDITIVE_reach <= 0.20).
  G0-PROXY (coherence floor): each arm must FIT the DIAGONAL train set (train_fit >= 0.99).
     If BOTH arms fail to fit train  -> INCONCLUSIVE-AT-FLOOR (G0-undertrain trap): the composed
     metric says NOTHING about the operator; report that honestly, NOT a pass/fail.
  Otherwise (bar not met but train fit) -> FALSIFIED-DIRECTIONAL (operator does not lift in-trunk).
=================================================================================================
"""
import os, sys, json
os.environ.setdefault("OMP_NUM_THREADS", "4")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MODEL_DIR = os.path.join(REPO, "archive", "train", "clm", "model")
sys.path.insert(0, MODEL_DIR)

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except Exception as e:
    print(json.dumps({"blocked": True, "reason": f"no torch: {e}"}))
    sys.exit(0)

from model import CLMConvMoE, CLMConfig  # live production trunk

# ----- toy hyperparams (TINY / CPU) -----
K       = 6          # states per factor  -> composed vocab slice = K*K = 36 bytes (100..135)
D       = 64         # channel width (must be even for the disjoint split)
LAYERS  = 2
EXPERTS = 4
STEPS   = 800
LR      = 1e-2
SEEDS   = [0, 1, 2]
BOS, A0, B0, C0 = 1, 10, 40, 100
assert C0 + K*K <= 256 and B0 >= A0+K and C0 >= B0+K, "byte ranges must not overlap / overflow"
COMP_POS = 2         # position of B_j; its next-byte prediction is C

def make_data():
    """Return (diag_tokens[K,4], diag_target[K], off_tokens[M,4], off_target[M], off_ab[M,2])."""
    diag_tok, diag_tgt = [], []
    off_tok, off_tgt, off_ab = [], [], []
    for i in range(K):
        for j in range(K):
            seq = [BOS, A0+i, B0+j, C0 + i*K + j]
            tgt = C0 + i*K + j
            if i == j:
                diag_tok.append(seq); diag_tgt.append(tgt)
            else:
                off_tok.append(seq); off_tgt.append(tgt); off_ab.append((i, j))
    t = lambda x: torch.tensor(x, dtype=torch.long)
    return (t(diag_tok), t(diag_tgt), t(off_tok), t(off_tgt), torch.tensor(off_ab))

def trunk_rep(net, tokens):
    """Replicate CLMConvMoE.forward body up to (and including) norm_out; return x (B,C,T).
    grad_checkpoint defaults False so we take the plain path — byte-identical to production."""
    x = net.embed(tokens)          # (B,T,C)
    x = x.transpose(1, 2)          # (B,C,T)
    x = net.embed_conv(x)
    for layer in net.trunk:
        x = layer(x)
    x, _stats = net.moe(x)
    x = net.norm_out(x)            # (B,C,T)
    return x

class MeiosisReadout(nn.Module):
    """Disjoint-loci factored readout: head_A reads r[:d/2], head_B reads r[d/2:]."""
    def __init__(self, d, k):
        super().__init__()
        self.h = d // 2
        self.head_A = nn.Linear(self.h, k)
        self.head_B = nn.Linear(self.h, k)
        self.k = k
    def composed_logits(self, r):          # r: (B, d)  representation at COMP_POS
        la = self.head_A(r[:, :self.h])    # (B,K)
        lb = self.head_B(r[:, self.h:])    # (B,K)
        return (la.unsqueeze(2) + lb.unsqueeze(1)).reshape(r.size(0), self.k*self.k)  # (B,K*K)

def build(seed):
    torch.manual_seed(seed)
    cfg = CLMConfig(vocab_size=256, d_model=D, n_trunk_layers=LAYERS,
                    n_experts=EXPERTS, kernel_size=3, variant="A")
    net = CLMConvMoE(cfg)
    return net, cfg

def run_arm(arm, seed, data):
    diag_tok, diag_tgt, off_tok, off_tgt, off_ab = data
    net, cfg = build(seed)
    if arm == "meiosis":
        head = MeiosisReadout(D, K)
        params = list(net.parameters()) + list(head.parameters())
    else:
        head = None
        params = list(net.parameters())
    opt = torch.optim.Adam(params, lr=LR)
    for step in range(STEPS):
        net.train()
        opt.zero_grad()
        r = trunk_rep(net, diag_tok)[:, :, COMP_POS]     # (K, d)
        if arm == "meiosis":
            logits = head.composed_logits(r)             # (K, K*K)
            tgt = diag_tgt - C0                            # composed-class index
            loss = F.cross_entropy(logits, tgt)
        else:
            logits = net.readout(trunk_rep(net, diag_tok))[:, :, COMP_POS]  # (K,256)
            loss = F.cross_entropy(logits, diag_tgt)
        loss.backward(); opt.step()
    # ----- eval -----
    net.eval()
    with torch.no_grad():
        # G0: diagonal train fit (full 256-way argmax == target byte for both arms)
        def decode_bytes(tok):
            r = trunk_rep(net, tok)[:, :, COMP_POS]
            if arm == "meiosis":
                comp = head.composed_logits(r)                    # (N, K*K)
                return C0 + comp.argmax(dim=1)                     # byte
            else:
                return net.readout(trunk_rep(net, tok))[:, :, COMP_POS].argmax(dim=1)
        train_pred = decode_bytes(diag_tok)
        train_fit = (train_pred == diag_tgt).float().mean().item()
        off_pred = decode_bytes(off_tok)
        reach = (off_pred == off_tgt).float().mean().item()
    n_params = sum(p.numel() for p in params)
    return {"train_fit": round(train_fit, 4), "reach": round(reach, 4), "n_params": n_params, "final_loss": round(float(loss.item()), 4)}

def main():
    print("H_6112 ladder rung 1.5 — real-trunk meiosis-crossover A/B (DIRECTIONAL, torch)")
    print(f"torch={torch.__version__}  K={K} D={D} L={LAYERS} E={EXPERTS} steps={STEPS} lr={LR} seeds={SEEDS}")
    data = make_data()
    print(f"train(diag)={data[0].shape[0]}  heldout(off-diag)={data[2].shape[0]}")
    per_seed = []
    for s in SEEDS:
        a = run_arm("additive", s, data)
        m = run_arm("meiosis",  s, data)
        delta = round(m["reach"] - a["reach"], 4)
        per_seed.append({"seed": s, "additive": a, "meiosis": m, "delta": delta})
        print(f"[seed {s}] ADD fit={a['train_fit']} reach={a['reach']} p={a['n_params']} | "
              f"MEIO fit={m['train_fit']} reach={m['reach']} p={m['n_params']} | delta={delta}")
    # aggregate
    add_reach = [p["additive"]["reach"] for p in per_seed]
    meio_reach = [p["meiosis"]["reach"] for p in per_seed]
    add_fit  = [p["additive"]["train_fit"] for p in per_seed]
    meio_fit = [p["meiosis"]["train_fit"] for p in per_seed]
    mean = lambda v: round(sum(v)/len(v), 4)
    seeds_meet = sum(1 for p in per_seed if p["delta"] >= 0.30)
    both_fit = all(f >= 0.99 for f in add_fit) and all(f >= 0.99 for f in meio_fit)
    neither_fit = all(f < 0.99 for f in add_fit) and all(f < 0.99 for f in meio_fit)
    bar_pass = (seeds_meet >= 2) and (mean(add_reach) <= 0.20)
    if neither_fit:
        decision = "inconclusive-at-floor"
    elif bar_pass:
        decision = "probed-real-trunk"
    else:
        decision = "falsified-directional"
    verdict = {
        "additive_reach_per_seed": add_reach, "additive_reach_mean": mean(add_reach),
        "meiosis_reach_per_seed": meio_reach, "meiosis_reach_mean": mean(meio_reach),
        "additive_train_fit_mean": mean(add_fit), "meiosis_train_fit_mean": mean(meio_fit),
        "seeds_meeting_delta>=0.30": seeds_meet, "both_arms_fit_train": both_fit,
        "bar_pass": bar_pass, "decision": decision, "per_seed": per_seed,
    }
    print("=== VERDICT (DIRECTIONAL — torch, not live .hexa engine; never terminal) ===")
    print(json.dumps(verdict, indent=2))
    print(f"DECISION={decision} bar_pass={bar_pass} "
          f"[GREEN-DIRECTIONAL bar: >=2/3 seeds delta>=0.30 AND mean additive_reach<=0.20]")

if __name__ == "__main__":
    main()
