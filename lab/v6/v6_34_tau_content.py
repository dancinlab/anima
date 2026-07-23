"""V6_34 (general-wall test) -- is the MOUTH/EMIT channel difficulty-complete? i.e. conditioned on
instantaneous prediction-difficulty and its history, does any recurrent linguistic-CONTENT channel
add usable information to the natural emit decision -- or does only a difficulty integral survive?
($0 laptop, torch, reuses v6_33 cache/estimator.)

Reconciled Fable+Sol (lab full 2026-07-23), BOTH decisive on two points:
- The V6_31-33 "general law" (every orthogonal faculty dies) is OVER-GENERALIZED. `tau` is itself a
  projection of composed-minus-reflex MOUTH logits, so NO tau experiment can falsify a UNIVERSAL
  orthogonality claim. It CAN falsify the narrower, useful **mouth-channel sufficiency wall**:
     I(emit_t ; tau_{<t} | x_t, x_{<t}, NLL_{<t}, clock_{<t}) = 0.
  LAW-HOLDS here = the mouth/emit redesign is closed directionally + R9 confirmed for the MOUTH-ROUTED
  faculty class only (NOT universal). The untested escape both named: a NON-mouth, non-CE-trained
  decision channel (Fable: the WIRED hippocampal store-bridge recall lane, content-addressed by
  construction; Sol: an intervention/reward-trained goal state) -- the NEXT slice's frame, not this.
- Raw TAU-vs-DRIVER is broken BOTH ways: tau's magnitude IS a finer difficulty basis (false LAW-FALSE),
  and a noisy 16-d input can lose on SNR while carrying content (false LAW-HOLDS). Fix = condition
  content on difficulty + strip difficulty three independent ways:
    * residualize (Sol, conservative): r_t = tau_t - g(x_t, NLL_t, pos_t), quadratic ridge, TRAIN-only
      fit (no emit/cmd) -- strips linear+quadratic difficulty AND surprise (NLL).
    * difficulty-matched SWAP (both): content register fed r from a DIFFERENT sentence, matched on the
      difficulty bin (NLL x ||tau|| deciles) -- preserves the difficulty-conditional marginal of r,
      destroys the position-specific content.
    * MAGNITUDE cut (Fable, the decisive tripwire): |r_t| only, direction stripped -- difficulty is a
      magnitude concept; content is DIRECTIONAL in the logit geometry. If direction adds nothing,
      "content" was refined surprise.
- Dual-register (Sol): X+CONTENT = the difficulty register (DRIVER) PLUS a separate content register,
  so the content register must add BEYOND difficulty. Primary contrast = X+SWAP - X+CONTENT; guard =
  DRIVER - X+CONTENT; direction cut = X+CONTENT-MAG - X+CONTENT.
- NLL-probe equivalence MANDATORY (both): if content wins on the next-byte-NLL DV, that is prediction-
  aligned surprise (p7), NOT orthogonal content -> cannot rescue LAW-FALSE.
- New PC-TAU positive control (both): route a known content signal through the continuous ingress;
  the old command-embedding certification does not certify this path.

Strict-past invariant kept (register at t reads state built from <t). lab/v6 = DIRECTIONAL ceiling.
"""
import sys, os, numpy as np
import torch, torch.nn as nn

RDIM = 8; SEEDS = [7, 11, 4302, 101, 777]; EPOCHS = 40; LR = 3e-3
ARMS = ["NO-EC", "DRIVER", "X+CONTENT", "X+SWAP", "X+CONTENT-MAG"]

# ---------------------------------------------------------------- residualize + swap tape ---------
def poly2(F):
    """degree-2 features of F:[N,d] -> [N, 1+d+d+C(d,2)] (bias, linear, squares, cross)."""
    N, d = F.shape
    cols = [np.ones((N, 1), np.float32), F, F * F]
    for i in range(d):
        for j in range(i + 1, d):
            cols.append((F[:, i] * F[:, j])[:, None])
    return np.hstack(cols).astype(np.float32)

def residualize(tau, x, nll, pos, tr_pos):
    """r = tau - g(x,nll,pos); quadratic ridge fit on TRAIN positions only (no emit/cmd = no leak)."""
    F = np.hstack([x, nll[:, None], pos[:, None].astype(np.float32)])
    mu = F[tr_pos].mean(0); sd = F[tr_pos].std(0) + 1e-9
    Fz = (F - mu) / sd
    Phi = poly2(Fz)
    A = Phi[tr_pos]; lam = 1e-1
    W = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ tau[tr_pos])
    return (tau - Phi @ W).astype(np.float32)

def swap_tape(r, x, nll, tau, sid, seed, nbin=8):
    """difficulty-matched derangement of r: donor from a DIFFERENT sentence in the same
    (NLL-decile x ||tau||-decile) bin -> preserves p(r|difficulty), destroys content address."""
    rng = np.random.default_rng(seed)
    tn = np.linalg.norm(tau, axis=1)
    def dec(v):
        q = np.quantile(v, np.linspace(0, 1, nbin + 1)[1:-1]); return np.digitize(v, q)
    key = dec(nll) * nbin + dec(tn)
    rs = r.copy()
    for b in np.unique(key):
        idx = np.where(key == b)[0]
        if len(idx) < 2: continue
        perm = rng.permutation(idx)
        # ensure donor != same sentence where possible (roll retries)
        for _ in range(4):
            bad = sid[perm] == sid[idx]
            if not bad.any(): break
            perm[bad] = rng.permutation(perm[bad])
        rs[idx] = r[perm]
    return rs

# ------------------------------------------------------------------------------ batched panel -----
def batchify(arrs, sid):
    ids = np.unique(sid); B = len(ids); Tmax = max((sid == i).sum() for i in ids)
    out = {}
    for k, a in arrs.items():
        shp = (B, Tmax) + (() if a.ndim == 1 else (a.shape[1],))
        buf = np.zeros(shp, np.float32 if a.dtype != np.int32 else np.int64)
        for r, i in enumerate(ids): buf[r, :(sid == i).sum()] = a[sid == i]
        out[k] = torch.tensor(buf)
    M = np.zeros((B, Tmax), np.float32)
    for r, i in enumerate(ids): M[r, :(sid == i).sum()] = 1.0
    out["mask"] = torch.tensor(M); out["ids"] = ids
    return out

class DualGate(nn.Module):
    """readout a.x_t + b_d.e_d(difficulty reg) + b_c.e_c(content reg).
    e updated strict-past (imp_{t-1}); free-forget on a content-free clock."""
    def __init__(self, xd, arm):
        super().__init__(); self.arm = arm
        self.a = nn.Linear(xd, 1)
        self.dh = nn.Linear(xd, RDIM)                    # difficulty impulse
        self.cin = nn.Linear(16, RDIM)                   # content impulse (r_t or |r_t|)
        self.lam_d = nn.Parameter(torch.zeros(RDIM)); self.lam_c = nn.Parameter(torch.zeros(RDIM))
        self.fa = nn.Linear(2, 2); self.fbd = nn.Linear(RDIM, 1, bias=False); self.fbc = nn.Linear(RDIM, 1, bias=False)
        self.bd = nn.Linear(RDIM, 1, bias=False); self.bc = nn.Linear(RDIM, 1, bias=False)
        self.use_d = arm in ("DRIVER", "X+CONTENT", "X+SWAP", "X+CONTENT-MAG")
        self.use_c = arm in ("X+CONTENT", "X+SWAP", "X+CONTENT-MAG")

    def forward(self, X, R, EMIT):
        B, T, _ = X.shape
        ld = torch.sigmoid(self.lam_d); lc = torch.sigmoid(self.lam_c)
        ed = torch.zeros(B, RDIM); ec = torch.zeros(B, RDIM)
        impd = torch.zeros(B, RDIM); impc = torch.zeros(B, RDIM)
        last = torch.zeros(B); cnt = torch.zeros(B); out = []; ectraj = []
        for t in range(T):
            clock = torch.stack([(t - last) / (T + 1.0), cnt / (t + 1.0)], -1)
            fg = torch.sigmoid(self.fa(clock)); fd = fg[:, 0:1]; fc = fg[:, 1:2]
            ed = (1 - fd) * ld * ed + impd; ec = (1 - fc) * lc * ec + impc
            logit = self.a(X[:, t])
            if self.use_d: logit = logit + self.bd(ed)
            if self.use_c: logit = logit + self.bc(ec)
            out.append(logit); ectraj.append(ec)
            if self.use_d: impd = self.dh(X[:, t])
            if self.use_c:
                rt = R[:, t].abs() if self.arm == "X+CONTENT-MAG" else R[:, t]
                impc = self.cin(rt)
            em = EMIT[:, t]                                       # content-free clock advances on emits
            last = torch.where(em > 0.5, torch.full_like(last, float(t)), last); cnt = cnt + em
        return torch.stack(out, 1).squeeze(-1), torch.stack(ectraj, 1).detach()

def _loss(lg, tgt, mask, dv, w=None):
    if dv == "emit":
        return nn.functional.binary_cross_entropy_with_logits(lg, tgt, weight=mask, pos_weight=w, reduction='sum') / (mask.sum() + 1e-9)
    return (nn.functional.smooth_l1_loss(lg, tgt, reduction='none') * mask).sum() / (mask.sum() + 1e-9)

def train_arm(arm, D, Rtr, tr, va, te, seed, dv, eval_R=None):
    torch.manual_seed(seed)
    m = DualGate(D["x"].shape[2], arm)
    opt = torch.optim.Adam(m.parameters(), lr=LR, weight_decay=1e-4)
    tgt = D["tgt_emit"] if dv == "emit" else D["nll"]
    pos = (D["emit"] * D["mask"]).sum().item() / max(D["mask"].sum().item(), 1)
    w = torch.tensor([(1 - pos) / max(pos, 1e-3)]) if dv == "emit" else None
    best_va, best_state = 1e9, None
    for ep in range(EPOCHS):
        m.train(); opt.zero_grad()
        lg, _ = m(D["x"][tr], Rtr[tr], D["emit"][tr])
        loss = _loss(lg, tgt[tr], D["mask"][tr], dv, w)
        loss.backward(); nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        m.eval()
        with torch.no_grad():
            lv, _ = m(D["x"][va], Rtr[va], D["emit"][va]); va_loss = _loss(lv, tgt[va], D["mask"][va], dv).item()
        if va_loss < best_va: best_va = va_loss; best_state = {k: v.clone() for k, v in m.state_dict().items()}
    m.load_state_dict(best_state); m.eval()
    Rte = Rtr if eval_R is None else eval_R
    with torch.no_grad():
        lt, ec = m(D["x"][te], Rte[te], D["emit"][te]); te_loss = _loss(lt, tgt[te], D["mask"][te], dv).item()
    return te_loss, ec

def independence(ec, D, te):
    mask = D["mask"][te].bool()
    E = ec[mask].numpy()
    Dr = torch.cat([D["x"][te], D["nll"][te].unsqueeze(-1), D["pos"][te].float().unsqueeze(-1)], -1)[mask].numpy()
    Dr = (Dr - Dr.mean(0)) / (Dr.std(0) + 1e-9); Dr = np.hstack([Dr, np.ones((len(Dr), 1))])
    W = np.linalg.solve(Dr.T @ Dr + 1e-2 * np.eye(Dr.shape[1]), Dr.T @ E)
    resid = E - Dr @ W
    ie = float((resid ** 2).sum() / (((E - E.mean(0)) ** 2).sum() + 1e-9))
    C = np.cov(resid.T); reff = float((np.trace(C) ** 2) / (np.trace(C @ C) + 1e-12))
    return ie, reff

def grouped_split(B, seed):
    rng = np.random.default_rng(seed); perm = rng.permutation(B); a, b = int(B * 0.6), int(B * 0.8)
    tr = torch.zeros(B, dtype=torch.bool); va = torch.zeros(B, dtype=torch.bool); te = torch.zeros(B, dtype=torch.bool)
    tr[perm[:a]] = True; va[perm[a:b]] = True; te[perm[b:]] = True
    return tr, va, te

def flat_train_positions(sid, ids, tr_mask):
    tr_sents = set(np.array(ids)[tr_mask.numpy()])
    return np.array([i for i, s in enumerate(sid) if s in tr_sents])

def run(raw, dv, label):
    print(f"\n=== {label} · DV={dv} · ({len(SEEDS)} seeds, val-selected, test-once) ===")
    sid = raw["sid"]; D = batchify({"x": raw["x"], "emit": raw["emit"], "nll": raw["nll"],
                                    "pos": raw["pos"].astype(np.int32)}, sid)
    D["tgt_emit"] = raw["tgt_emit_bt"] if raw.get("tgt_emit_bt") is not None else D["emit"]
    res = {a: [] for a in ARMS}; doflip = []; ies = []; reffs = []
    for seed in SEEDS:
        tr, va, te = grouped_split(len(D["ids"]), seed)
        tr_pos = flat_train_positions(sid, D["ids"], tr)
        r = residualize(raw["tau"], raw["x"], raw["nll"], raw["pos"].astype(np.float32), tr_pos)
        rsw = swap_tape(r, raw["x"], raw["nll"], raw["tau"], sid, seed)
        R = batchify({"c": r}, sid)["c"]; RS = batchify({"c": rsw}, sid)["c"]
        for a in ARMS:
            Rin = RS if a == "X+SWAP" else R
            loss, ec = train_arm(a, D, Rin, tr, va, te, seed, dv)
            res[a].append(loss)
            if a == "X+CONTENT" and dv == "emit":
                ie, rf = independence(ec, D, te); ies.append(ie); reffs.append(rf)
        # do-swap: trained X+CONTENT evaluated with the swapped content tape
        dl, _ = train_arm("X+CONTENT", D, R, tr, va, te, seed, dv, eval_R=RS)
        doflip.append(dl - res["X+CONTENT"][-1])
    def z(worse, better):
        d = np.array(res[worse]) - np.array(res[better]); return d.mean(), d.mean() / (d.std(ddof=1) / np.sqrt(len(d)) + 1e-9)
    for a in ARMS: print(f"  {a:<14} {np.mean(res[a]):.4f}")
    C = {}
    for pair in [("DRIVER", "X+CONTENT"), ("X+SWAP", "X+CONTENT"), ("X+CONTENT-MAG", "X+CONTENT"), ("NO-EC", "X+CONTENT")]:
        mm, zz = z(*pair); C[pair[0]] = (mm, zz); print(f"  {pair[0]:<14} - X+CONTENT = {mm:+.4f}  z={zz:+.2f}")
    fm = np.mean(doflip); fz = fm / (np.std(doflip, ddof=1) / np.sqrt(len(doflip)) + 1e-9)
    print(f"  do-swap (X+CONTENT eval w/ swapped r) degrade = {fm:+.4f}  z={fz:+.2f}")
    C["_do"] = (fm, fz)
    if ies:
        ie_lb = np.mean(ies) - 2 * np.std(ies) / np.sqrt(len(ies))
        print(f"  content-register independence I_r = {np.mean(ies):.3f} (2se-LB {ie_lb:.3f})  effrank = {np.mean(reffs):.2f}")
        C["_ie"] = (np.mean(ies), ie_lb, np.mean(reffs))
    return C

# ---------------------------------------------------------- PC-TAU (route content thru ingress) ---
def pc_tau(raw, seed=0):
    """semi-synthetic: relabel emit where sign(w . r_global) > 0 (w fixed unit vector), so a content
    register reading r must beat a difficulty-matched swap. Certifies the CONTINUOUS content path."""
    rng = np.random.default_rng(seed)
    # global (label-free) residual for PC construction
    F = np.hstack([raw["x"], raw["nll"][:, None], raw["pos"][:, None].astype(np.float32)])
    Fz = (F - F.mean(0)) / (F.std(0) + 1e-9); Phi = poly2(Fz)
    W = np.linalg.solve(Phi.T @ Phi + 1e-1 * np.eye(Phi.shape[1]), Phi.T @ raw["tau"])
    r = (raw["tau"] - Phi @ W).astype(np.float32)
    wv = rng.standard_normal(16); wv /= np.linalg.norm(wv)
    score = r @ wv
    tgt = (score > 0).astype(np.float32)                 # content-driven target
    return dict(raw, tgt_emit_flat=tgt)

def load(cache):
    d = np.load(cache)
    x = d["x"].astype(np.float32); x = (x - x.mean(0)) / (x.std(0) + 1e-9)
    tau = d["tau"].astype(np.float32); tau = (tau - tau.mean(0)) / (tau.std(0) + 1e-9)
    return dict(x=x, tau=tau, emit=d["emit"].astype(np.float32), nll=d["nll"].astype(np.float32),
                pos=d["pos"], sid=d["sid"], tgt_emit_bt=None)

def with_target(raw, tgt_flat):
    r = dict(raw); r["tgt_emit_bt"] = batchify({"c": tgt_flat}, raw["sid"])["c"].float(); return r

def main():
    cache = sys.argv[1] if len(sys.argv) > 1 else "lab/v6/v6_33_cache.npz"
    raw = load(cache)

    print("== PC-TAU POSITIVE CONTROL (content routed through the continuous ingress) ==")
    pc = pc_tau(raw); pcr = with_target(pc, pc["tgt_emit_flat"])
    cpc = run(pcr, "emit", "PC-TAU")
    p_sw = cpc["X+SWAP"][1]; p_dr = cpc["DRIVER"][1]
    ok = (p_sw >= 3 and p_dr >= 3)
    print(f"  PC-TAU: X+CONTENT beats SWAP z={p_sw:.2f}, DRIVER z={p_dr:.2f} -> {'PASS' if ok else 'FAIL -> VOID'}")

    print("\n== NATURAL ==")
    ce = run(raw, "emit", "NATURAL")
    cq = run(load(cache), "nll", "NATURAL")

    print("\n=== FROZEN VERDICT (mouth-channel sufficiency wall) ===")
    if not ok:
        print("VOID — PC-TAU failed (estimator cannot read content of the size we'd rule out)."); return 0
    def zpass(c, k): return c[k][0] >= 0.010 and c[k][1] >= 3.0
    def tost(c, k): m, zz = c[k]; se = abs(m) / (abs(zz) + 1e-9); return (abs(m) + 2 * se) < 0.010
    guard = zpass(ce, "DRIVER"); primary = zpass(ce, "X+SWAP"); direction = zpass(ce, "X+CONTENT-MAG")
    do_ok = ce["_do"][0] >= 0.010 and ce["_do"][1] >= 3.0
    ie, ie_lb, rf = ce.get("_ie", (0, 0, 0)); ind_ok = ie >= 0.15 and ie_lb > 0.08 and rf >= 2.0
    nll_equiv = tost(cq, "DRIVER") and tost(cq, "X+SWAP")   # content NOT a surprise win
    print(f"  guard DRIVER-X+CONTENT z3: {guard} · primary SWAP-X+CONTENT z3: {primary} · direction MAG z3: {direction}")
    print(f"  do-swap degrade: {do_ok} ({ce['_do'][0]:+.4f} z={ce['_do'][1]:.2f}) · independence: {ind_ok} (I_r={ie:.3f} LB={ie_lb:.3f} eff={rf:.2f})")
    print(f"  NLL-probe equivalence (content NOT surprise): {nll_equiv}")
    if guard and primary and direction and do_ok and ind_ok and nll_equiv:
        v = "LAW-FALSE — mouth-channel sufficiency wall is FALSE: tau DIRECTIONAL content controls emit beyond difficulty (DIRECTIONAL; anima-py port to cement)"
    elif tost(ce, "DRIVER") and tost(ce, "X+SWAP"):
        v = "LAW-HOLDS — mouth/emit redesign CLOSED directionally; R9 confirmed for the MOUTH-ROUTED class only (non-mouth store-bridge lane untested = next frame)"
    elif (guard or primary) and not direction:
        v = "LAW-HOLDS-AMENDED — tau adds signal but it is finer SURPRISE not direction (MAG≡CONTENT); same closure"
    else:
        v = "INVALID — mixed zone (neither the z>=3 success conjunction nor the TOST closure)"
    print(f"\nVERDICT: {v}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
