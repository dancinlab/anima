#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_9129 · L3 CEREBELLUM FORWARD-MODEL CONSEQUENCE LANE — RUNG-2 ENGINE-NATIVE (303M)
==================================================================================
Escalation of STEP-0 (state/g1g6_biolens_step0/l3_fwdmodel, numpy toy DIRECTIONAL).

WHAT CHANGES vs STEP-0 (the whole point of rung-2):
  STEP-0 world = toy: concept feats V = rng.normal, consequence = tanh(W_world @
  [vi,vj, vi(X)vj]) with a HAND-INJECTED interaction term -> BIND by construction.
  RUNG-2 replaces every toy piece with REAL-303M / engine-native ops:
    - concept feats V[X]  = REAL h1129 303M forward-last next-byte logits[256]
                            (core/decode.py::bg_forward_last_W — the anima evaluate
                            --py numpy 2-production path; a_eval_py_canonical).
    - grounded obs (Arm A) = immune_embed_key("attrX attrY") — the engine's OWN
                            deterministic FNV-1a byte-trigram DIM64 key (exact mirror
                            of core/engine_cli.hexa::immune_embed_key, mouth-weights-0-
                            contact) = grounded consequence of the claim.
    - committed obs (Arm B) = REAL h1129 303M forward-last logits on the pair prompt
                            "the X and the Y yield " — the 303M's OWN committed
                            forward prediction (what it says is observed).
  Relation graph = REAL corpus (state/g1_coverage_bytes/corpus_high.txt): 24 nouns,
  each one grounded attribute (atomic "the X is a ."), 400 observed pairs
  ("the X and the Y yield aX aY ."). NOT a toy chain.

FROZEN BAR (pre-registered — task spec, NOT tuned; a_break_the_wall/p7/c9):
  GREEN  = reachable >> unreachable (gap>=GAP_REG) AND shuffle collapses AND lane-OFF
           collapses AND FM_full>FM_additive AND engine-native.
  WALL   = engine-native reachable ~= unreachable (unlike the toy mini = a real wall).
  RED    = unmeasurable / at-floor (err_reach ~= mean-predictor floor).
  by-construction guard (a_toy_scale_recheck): Arm-A GT-target is a clean conjunction
  by corpus construction, so a BIND there is reported WITH that caveat; the
  reachable/unreachable + shuffle + additive controls protect against pure form.

TIER: the 303M reps are engine-native (real h1129 via production decode.py), but the
  LANE op (VConsequenceField NLMS/MLP) is a numpy MIRROR of the core .hexa op (rung-3
  = core/consequence_lane_smoke.hexa not yet built) => per Gate-1 a BIND verdict is
  DIRECTIONAL (+ ING for the .hexa smoke); a WALL/RED is engine-native-robust.
"""
import numpy as np, json, os, sys, time, re

HERE = os.path.dirname(os.path.abspath(__file__))
# read-only inputs live in the MAIN checkout (corpus is untracked; weights external)
MAIN   = "/Users/mini/dancinlab/anima"
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "core"))  # worktree core/decode.py
import decode as bg

CK     = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
CORPUS = os.path.join(MAIN, "state", "g1_coverage_bytes", "corpus_high.txt")

# ---- frozen config (pre-registered) ----
D_FEAT   = 32
HID      = 64
STEPS    = 6000
LR       = 3e-3
COV_THR  = 0.30
GAP_REG  = 0.15
N_DANGLE = 5
SEEDS    = [1305, 2026, 7, 42, 909]

# ── immune_embed_key — EXACT numpy mirror of core/engine_cli.hexa (DIM64, byte-trigram
#    FNV-1a histogram, L2-norm). 32-bit FNV-1a offset 0x811c9dc5 prime 0x01000193. ──
def _fnv1a(bs):
    h = 2166136261
    for b in bs:
        h ^= b
        h = (h * 16777619) & 4294967295
    return h

def immune_embed_key(text):
    dim, n = 64, 3
    bs = text.encode("utf-8"); blen = len(bs); v = np.zeros(dim)
    if blen < n:
        v[_fnv1a(list(bs)) % dim] += 1.0
    else:
        for i in range(blen - n + 1):
            v[_fnv1a(list(bs[i:i+n])) % dim] += 1.0
    nrm = np.sqrt((v*v).sum())
    return v/nrm if nrm > 0 else v

def load_graph():
    isre = re.compile(r"^the (\w+) is (\w+) \.$")
    yre  = re.compile(r"^the (\w+) and the (\w+) yield (\w+) (\w+) \.$")
    attr = {}; seenpairs = set()
    for l in open(CORPUS):
        l = l.strip()
        m = isre.match(l)
        if m: attr[m.group(1)] = m.group(2); continue
        m = yre.match(l)
        if m: seenpairs.add((m.group(1), m.group(2)))
    return sorted(attr.keys()), attr, seenpairs

def fwd_logits(W, text):
    ids = list(text.encode("utf-8"))
    if len(ids) > W["block"]: ids = ids[-W["block"]:]
    return np.asarray(bg.bg_forward_last_W(W, ids, len(ids)), dtype=np.float64)

def build_303m(W, nouns, needed_pairs, log):
    t0 = time.time()
    Vraw = np.stack([fwd_logits(W, "the %s is" % x) for x in nouns])
    log("  concept reps: %d nouns, %.1fs" % (len(nouns), time.time()-t0))
    consB = {}; t0 = time.time()
    for k, (a, b) in enumerate(needed_pairs):
        consB[(a, b)] = fwd_logits(W, "the %s and the %s yield " % (a, b))
        if (k+1) % 100 == 0: log("  Arm-B %d/%d (%.0fs)" % (k+1, len(needed_pairs), time.time()-t0))
    if needed_pairs: log("  Arm-B consequences: %d pairs, %.1fs" % (len(needed_pairs), time.time()-t0))
    return Vraw, consB

def pca_reduce(Xraw, dim):
    mean = Xraw.mean(0); Xc = Xraw - mean
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    return Xc @ Vt[:dim].T

class ForwardModel:
    def __init__(self, rng, din, dout, additive=False):
        self.additive = additive; self.dout = dout; s = 0.15
        if additive:
            self.Wl = rng.normal(0, s, (dout, din)); self.bl = np.zeros(dout)
            self.params = ["Wl", "bl"]
        else:
            self.W1 = rng.normal(0, s, (din, HID)); self.b1 = np.zeros(HID)
            self.W2 = rng.normal(0, s, (HID, dout)); self.b2 = np.zeros(dout)
            self.params = ["W1", "b1", "W2", "b2"]
        self.m = {p: np.zeros_like(getattr(self, p)) for p in self.params}
        self.v = {p: np.zeros_like(getattr(self, p)) for p in self.params}; self.t = 0
    def forward(self, X):
        if self.additive: return X @ self.Wl.T + self.bl, None
        z1 = X @ self.W1 + self.b1; h = np.tanh(z1); return h @ self.W2 + self.b2, (z1, h)
    def loss_grad(self, X, Y):
        n = X.shape[0]; pred, cache = self.forward(X); diff = pred - Y
        loss = np.mean(diff*diff); dout = (2.0/n)*diff/self.dout; g = {}
        if self.additive:
            g["Wl"] = dout.T @ X; g["bl"] = dout.sum(0)
        else:
            z1, h = cache; g["W2"] = h.T @ dout; g["b2"] = dout.sum(0)
            dh = dout @ self.W2.T; dz1 = dh*(1-h*h); g["W1"] = X.T @ dz1; g["b1"] = dz1.sum(0)
        return loss, g
    def step(self, g):
        self.t += 1; b1, b2, eps = 0.9, 0.999, 1e-8
        for p in self.params:
            self.m[p] = b1*self.m[p] + (1-b1)*g[p]; self.v[p] = b2*self.v[p] + (1-b2)*(g[p]*g[p])
            mh = self.m[p]/(1-b1**self.t); vh = self.v[p]/(1-b2**self.t)
            setattr(self, p, getattr(self, p) - LR*mh/(np.sqrt(vh)+eps))

def coverage_form(pred, thr=COV_THR):
    return (np.abs(pred) > thr).sum(1).astype(float)

def derangement(n, rng):
    if n < 2: return np.arange(n)
    while True:
        p = rng.permutation(n)
        if not np.any(p == np.arange(n)): return p

def run_seed(seed, nouns, attr, seenpairs, Vred, consB_red, arm):
    rng = np.random.default_rng(seed)
    N = len(nouns); idx = {x: i for i, x in enumerate(nouns)}
    perm = list(rng.permutation(N))
    dangle = set(nouns[i] for i in perm[:N_DANGLE]); seenset = set(nouns[i] for i in perm[N_DANGLE:])
    allpairs = [(a, b) for a in nouns for b in nouns if a != b]
    train   = [(a, b) for (a, b) in allpairs if a in seenset and b in seenset and (a, b) in seenpairs]
    reach   = [(a, b) for (a, b) in allpairs if a in seenset and b in seenset and (a, b) not in seenpairs]
    unreach = [(a, b) for (a, b) in allpairs if (a in dangle or b in dangle)]
    rng.shuffle(reach); rng.shuffle(unreach)
    m = min(len(reach), len(unreach)); reach = reach[:m]; unreach = unreach[:m]

    def target(a, b):
        return immune_embed_key("%s %s" % (attr[a], attr[b])) if arm == "A" else consB_red[(a, b)]
    def feat(a, b):
        return np.concatenate([Vred[idx[a]], Vred[idx[b]]])

    Xtr = np.stack([feat(a,b) for a,b in train]);  Ytr = np.stack([target(a,b) for a,b in train])
    Xre = np.stack([feat(a,b) for a,b in reach]);  Yre = np.stack([target(a,b) for a,b in reach])
    Xun = np.stack([feat(a,b) for a,b in unreach]);Yun = np.stack([target(a,b) for a,b in unreach])
    din = Xtr.shape[1]; dout = Ytr.shape[1]
    dsh = derangement(len(reach), rng); Yre_sh = Yre[dsh]

    out = {}
    for name, additive in [("FM_full", False), ("FM_additive", True)]:
        fm = ForwardModel(rng, din, dout, additive=additive)
        ntr = len(train); bs = min(512, ntr)
        for _ in range(STEPS):
            b = rng.integers(0, ntr, size=bs); _, g = fm.loss_grad(Xtr[b], Ytr[b]); fm.step(g)
        pred_re, _ = fm.forward(Xre); pred_un, _ = fm.forward(Xun)
        err_reach   = float(np.mean((pred_re - Yre)**2))
        err_unreach = float(np.mean((pred_un - Yun)**2))
        err_shuffle = float(np.mean((pred_re - Yre_sh)**2))
        err_floor   = float(np.mean((Ytr.mean(0, keepdims=True) - Yre)**2))
        err_laneoff = float(np.mean((np.zeros_like(Yre) - Yre)**2))
        out[name] = {
            "err_reach": err_reach, "err_unreach": err_unreach, "err_shuffle": err_shuffle,
            "err_meanpred_floor": err_floor, "err_laneoff": err_laneoff,
            "fit_ratio_vs_floor": err_reach/(err_floor+1e-12),
            "gap_unreach_minus_reach": err_unreach - err_reach,
            "fit_gap_reach_vs_unreach": (err_unreach - err_reach)/(err_floor+1e-12),
            "shuffle_ratio": err_shuffle/(err_reach+1e-12),
            "laneoff_ratio": err_laneoff/(err_reach+1e-12),
            "cov_reach": float(np.mean(coverage_form(Yre))),
            "cov_unreach": float(np.mean(coverage_form(Yun))),
            "cov_shuffle": float(np.mean(coverage_form(Yre_sh))),
            "n_train": len(train), "n_reach": len(reach), "n_unreach": len(unreach),
        }
    return out

def verdict_from(summ):
    f = summ["FM_full"]; a = summ["FM_additive"]
    fits          = f["fit_ratio_vs_floor"] < 0.5
    shuffle_break = f["shuffle_ratio"] > 1.5
    laneoff_break = f["laneoff_ratio"] > 1.5
    form_flat     = abs(f["cov_reach"] - f["cov_shuffle"]) < 0.25
    reach_gap     = f["fit_gap_reach_vs_unreach"] >= GAP_REG
    full_gt_add   = f["err_reach"] < a["err_reach"]
    fooled = not (shuffle_break and reach_gap)
    if fits and shuffle_break and laneoff_break and form_flat and reach_gap and full_gt_add:
        v = "BIND"
    elif not fits:
        v = "floor"
    else:
        v = "WALL"
    return v, {
        "aligned_fit<0.5floor": bool(fits), "shuffle_ratio>1.5": bool(shuffle_break),
        "laneoff_ratio>1.5": bool(laneoff_break), "form_flat|covDelta|<0.25": bool(form_flat),
        "reach_gap>=%.2f" % GAP_REG: bool(reach_gap), "FM_full<FM_additive_err": bool(full_gt_add),
    }, bool(fooled)

def main():
    arm = sys.argv[1] if len(sys.argv) > 1 else "A"
    def log(*a): print(*a, flush=True)
    log("=== H_9129 L3 rung-2 ENGINE-NATIVE (303M h1129) arm=%s ===" % arm)
    nouns, attr, seenpairs = load_graph()
    log("graph: %d nouns, %d observed pairs" % (len(nouns), len(seenpairs)))
    log("loading REAL 303M h1129 (core/decode.py bg_load)...")
    t0 = time.time(); W = bg.bg_load(CK); log("  loaded %.1fs d=%d nlay=%d" % (time.time()-t0, W["d"], W["nlay"]))
    needed = [(a, b) for a in nouns for b in nouns if a != b] if arm == "B" else []
    Vraw, consB = build_303m(W, nouns, needed, log)
    Vred = pca_reduce(Vraw, D_FEAT); Vred = (Vred - Vred.mean(0))/(Vred.std(0)+1e-8)
    consB_red = {}
    if arm == "B":
        keys = list(consB.keys()); M = np.stack([consB[k] for k in keys])
        Mr = pca_reduce(M, 24); Mr = (Mr - Mr.mean(0))/(Mr.std(0)+1e-8)
        for i, k in enumerate(keys): consB_red[k] = Mr[i]
    rows = []; per = {"FM_full": [], "FM_additive": []}
    for sd in SEEDS:
        r = run_seed(sd, nouns, attr, seenpairs, Vred, consB_red, arm)
        rows.append({"seed": sd, **r})
        for k in per: per[k].append(r[k])
        log("  seed %d: full reach=%.4f unreach=%.4f shuf_r=%.2f loff_r=%.2f | add reach=%.4f (ntr=%d nre=%d)"
            % (sd, r["FM_full"]["err_reach"], r["FM_full"]["err_unreach"], r["FM_full"]["shuffle_ratio"],
               r["FM_full"]["laneoff_ratio"], r["FM_additive"]["err_reach"],
               r["FM_full"]["n_train"], r["FM_full"]["n_reach"]))
    def agg(a_):
        keys = per[a_][0].keys(); return {k: float(np.mean([d[k] for d in per[a_]])) for k in keys}
    summ = {"FM_full": agg("FM_full"), "FM_additive": agg("FM_additive")}
    v, gates, fooled = verdict_from(summ)
    result = {
        "probe": "H_9129 L3 cerebellum forward-model consequence lane — RUNG-2 ENGINE-NATIVE (303M h1129)",
        "arm": arm,
        "arm_desc": {"A": "grounded obs = immune_embed_key(attrX attrY) engine-native; concept feat V = real 303M forward logits",
                     "B": "committed obs = real 303M forward logits on pair-yield prompt; concept feat V = real 303M forward logits"}[arm],
        "engine_native_303M": True,
        "lane_op": "numpy MIRROR of core VConsequenceField (rung-3 .hexa smoke pending => BIND=DIRECTIONAL, WALL/RED=robust)",
        "config": {"D_FEAT": D_FEAT, "HID": HID, "STEPS": STEPS, "LR": LR, "COV_THR": COV_THR,
                   "GAP_REG": GAP_REG, "N_DANGLE": N_DANGLE, "SEEDS": SEEDS, "ckpt": CK, "corpus": CORPUS},
        "verdict": v, "fooled_by_form": fooled, "verdict_gates": gates,
        "summary_mean_over_seeds": summ, "per_seed": rows,
    }
    outf = os.path.join(HERE, "result_arm%s.json" % arm)
    with open(outf, "w") as fh: json.dump(result, fh, indent=2)
    log(json.dumps({"verdict": v, "fooled_by_form": fooled, "gates": gates,
                    "FM_full": summ["FM_full"], "FM_additive_err_reach": summ["FM_additive"]["err_reach"]}, indent=2))
    log("wrote " + outf)

if __name__ == "__main__":
    main()
