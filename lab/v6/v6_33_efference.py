"""V6_33 (redesign slice 2) -- the EFFERENCE-COPY channel: does an explicit register fed by the
daemon's OWN emit/command history carry INDEPENDENT, CAUSAL signal for the emit decision -- or is it
just emit-autocorrelation / a timer / a difficulty-integral?  ($0 laptop, torch, reuses v6_29.)

Reconciled Fable+Sol design (lab full 2026-07-23):
- BOTH: efference-copy is the right next move (before any co-trained trunk); the register has its
  OWN params + OWN downstream loss (never mouth CE) and is independent of m/CE BY CONSTRUCTION (no
  read edge from m/m_field/CE/target; reads only PAST emit decisions + the mouth's byte command).
- BOTH: the verdict does NOT ride on beating NO-EC (that would be the emit-autocorrelation tautology).
  It rides on TRUE-EC beating controls that receive the IDENTICAL emit-event tape:
    TIMER      -- content-free clock (same recency/count) => kills "just elapsed time"
    SHUFFLED   -- command bytes deranged among emit times  => kills "just the marginal / density"
    OTHER-SELF -- a matched non-emit tick's command marked "self" => kills "any content marked self"
    DRIVER-HIST(Fable) -- accumulates difficulty x_t instead of commands => kills "difficulty-integral"
  plus a do()-FLIP intervention on the trained TRUE model (substitute OTHER commands -> NLL must
  degrade), an independence floor (residual after regressing e on ALL drivers > V6_31's 8% null),
  and a synthetic reafference POSITIVE CONTROL (instrument check only, p9-legal).
- Sol caught a real leak in v6_29_train.py (`best=min(best,te_loss)` selects epoch on TEST) -> here
  we use a 60/20/20 grouped split, select epoch on VAL, evaluate TEST once.
- DV fork: Fable=next-byte NLL (removes the tautology at the root), Sol=emit decision (the actual
  target agency should move, = V6_29 label). Cheaply run BOTH (a_all_paths_no_leak): emit = primary
  (the decision that matters), nll = confound-probe. PRESENT requires survival on emit.

Indexing invariant (Sol, load-bearing): gate at t reads e_t; only AFTER scoring does (emit_t, cmd_t)
update e_{t+1}. So e_t depends on the STRICT PAST only -> it can never contain the current label.

lab/v6 = DIRECTIONAL ceiling. TERMINAL only via an anima-py in-loop port (named follow-on).
"""
import sys, os, numpy as np
import torch, torch.nn as nn

RDIM = 8; SEEDS = [7, 11, 4302, 101, 777]; EPOCHS = 40; LR = 3e-3
ARMS = ["NO-EC", "TRUE-EC", "TIMER", "SHUFFLED", "OTHER-SELF", "DRIVER-HIST"]

# ---------------------------------------------------------------- tapes (per position, per arm) ---
def build_tapes(cmd, emit, x, sid, seed):
    """Return per-position command tapes for SHUFFLED and OTHER-SELF (TRUE uses cmd as-is)."""
    rng = np.random.default_rng(seed)
    cmd_shuf = cmd.copy(); cmd_other = cmd.copy()
    for i in np.unique(sid):
        idx = np.where(sid == i)[0]
        em = idx[emit[idx] == 1]; nem = idx[emit[idx] == 0]
        if len(em) >= 2:                                    # derange commands among emit ticks
            perm = rng.permutation(len(em))
            if np.any(perm == np.arange(len(em))):          # avoid fixed points where possible
                perm = np.roll(perm, 1)
            cmd_shuf[em] = cmd[em][perm]
        if len(em) >= 1 and len(nem) >= 1:                  # OTHER: matched non-emit tick's command
            fe = x[nem][:, [2, 5]]                           # match on entropy, margin
            pe = x[em][:, [2, 5]]
            for j, e_pos in enumerate(em):
                d = ((fe - pe[j]) ** 2).sum(1)
                cmd_other[e_pos] = cmd[nem[int(np.argmin(d))]]
    return cmd_shuf, cmd_other

# ------------------------------------------------------------------------------ batched panel -----
def batchify(arrs, sid):
    ids = np.unique(sid); B = len(ids); Tmax = max((sid == i).sum() for i in ids)
    out = {}
    for k, a in arrs.items():
        shp = (B, Tmax) + (() if a.ndim == 1 else (a.shape[1],))
        buf = np.zeros(shp, np.float32 if a.dtype != np.int32 else np.int64)
        for r, i in enumerate(ids):
            m = sid == i; buf[r, :m.sum()] = a[m]
        out[k] = torch.tensor(buf)
    M = np.zeros((B, Tmax), np.float32)
    for r, i in enumerate(ids): M[r, :(sid == i).sum()] = 1.0
    out["mask"] = torch.tensor(M); out["ids"] = ids
    return out

class EffGate(nn.Module):
    """drivers-only readout a.x_t plus an optional efference register b.e_t.
    e_t = (1-f_t) lam e_{t-1} + imp_{t-1};  f_t = sigmoid(fa.clock_t + fb.e_{t-1})."""
    def __init__(self, xd, arm, dv):
        super().__init__(); self.arm = arm; self.dv = dv
        self.a = nn.Linear(xd, 1)
        self.emb = nn.Embedding(256, RDIM)          # command -> impulse (TRUE/SHUFFLED/OTHER)
        self.const = nn.Parameter(torch.randn(RDIM) * 0.1)     # TIMER impulse
        self.dh = nn.Linear(xd, RDIM)               # DRIVER-HIST impulse
        self.lam = nn.Parameter(torch.zeros(RDIM))
        self.fa = nn.Linear(2, 1); self.fb = nn.Linear(RDIM, 1, bias=False)
        self.b = nn.Linear(RDIM, 1, bias=False)

    def impulse(self, cmd_t, emit_t, x_t):
        if self.arm == "TIMER":   return emit_t.unsqueeze(-1) * self.const
        if self.arm == "DRIVER-HIST": return self.dh(x_t)          # fires every tick
        # TRUE / SHUFFLED / OTHER: command embedding gated by emit
        return emit_t.unsqueeze(-1) * self.emb(cmd_t)

    def forward(self, X, CMD, EMIT, POS, cum=None):
        B, T, _ = X.shape
        lam = torch.sigmoid(self.lam)
        e = torch.zeros(B, RDIM); imp_prev = torch.zeros(B, RDIM)
        last = torch.zeros(B); cnt = torch.zeros(B); out = []
        for t in range(T):
            clock = torch.stack([(t - last) / (T + 1.0), cnt / (t + 1.0)], -1)   # content-free
            f = torch.sigmoid(self.fa(clock) + self.fb(e))
            e = (1 - f) * lam * e + imp_prev
            logit = self.a(X[:, t]) + (0.0 if self.arm == "NO-EC" else self.b(e))
            out.append(logit)
            if self.arm != "NO-EC":
                imp_prev = self.impulse(CMD[:, t], EMIT[:, t], X[:, t])
            em = EMIT[:, t]
            last = torch.where(em > 0.5, torch.full_like(last, float(t)), last)
            cnt = cnt + em
        return torch.stack(out, 1).squeeze(-1)

def _loss(lg, tgt, mask, dv, w=None):
    if dv == "emit":
        return (nn.functional.binary_cross_entropy_with_logits(lg, tgt, weight=mask, pos_weight=w,
                reduction='sum') / (mask.sum() + 1e-9))
    return (nn.functional.smooth_l1_loss(lg, tgt, reduction='none') * mask).sum() / (mask.sum() + 1e-9)

def train_arm(arm, D, tr, va, te, seed, dv, cmd_key="cmd", eval_cmd_key=None):
    torch.manual_seed(seed)
    m = EffGate(D["x"].shape[2], arm, dv)
    opt = torch.optim.Adam(m.parameters(), lr=LR, weight_decay=1e-4)
    tgt = D["tgt_emit"] if dv == "emit" else D["nll"]
    pos = (D["emit"] * D["mask"]).sum().item() / max(D["mask"].sum().item(), 1)
    w = torch.tensor([(1 - pos) / max(pos, 1e-3)]) if dv == "emit" else None
    best_va, best_state = 1e9, None
    CMD = D[cmd_key].long()
    for ep in range(EPOCHS):
        m.train(); opt.zero_grad()
        lg = m(D["x"][tr], CMD[tr], D["emit"][tr], D["pos"][tr])
        loss = _loss(lg, tgt[tr], D["mask"][tr], dv, w)
        loss.backward(); nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        m.eval()
        with torch.no_grad():
            lv = m(D["x"][va], CMD[va], D["emit"][va], D["pos"][va])
            va_loss = _loss(lv, tgt[va], D["mask"][va], dv).item()
        if va_loss < best_va:
            best_va = va_loss; best_state = {k: v.clone() for k, v in m.state_dict().items()}
    m.load_state_dict(best_state); m.eval()
    ck = CMD if eval_cmd_key is None else D[eval_cmd_key].long()
    with torch.no_grad():
        lt = m(D["x"][te], ck[te], D["emit"][te], D["pos"][te])
        te_loss = _loss(lt, tgt[te], D["mask"][te], dv).item()
        # register trace for independence (TRUE only)
        e_trace = None
        if arm == "TRUE-EC":
            e_trace = _register_trace(m, D, te)
    return te_loss, e_trace

def _register_trace(m, D, te):
    """extract e_t at test positions from a trained TRUE model (no grad)."""
    B, T, _ = D["x"][te].shape
    lam = torch.sigmoid(m.lam); e = torch.zeros(B, RDIM); imp = torch.zeros(B, RDIM)
    last = torch.zeros(B); cnt = torch.zeros(B); traj = []
    X, CMD, EMIT = D["x"][te], D["cmd"].long()[te], D["emit"][te]
    with torch.no_grad():
        for t in range(T):
            clock = torch.stack([(t - last) / (T + 1.0), cnt / (t + 1.0)], -1)
            f = torch.sigmoid(m.fa(clock) + m.fb(e)); e = (1 - f) * lam * e + imp
            traj.append(e.clone())
            imp = EMIT[:, t].unsqueeze(-1) * m.emb(CMD[:, t])
            last = torch.where(EMIT[:, t] > 0.5, torch.full_like(last, float(t)), last); cnt = cnt + EMIT[:, t]
    return torch.stack(traj, 1)   # [B,T,RDIM]

def grouped_split(B, seed):
    rng = np.random.default_rng(seed); perm = rng.permutation(B)
    a, b = int(B * 0.6), int(B * 0.8)
    tr = torch.zeros(B, dtype=torch.bool); va = torch.zeros(B, dtype=torch.bool); te = torch.zeros(B, dtype=torch.bool)
    tr[perm[:a]] = True; va[perm[a:b]] = True; te[perm[b:]] = True
    return tr, va, te

def independence(e_trace, D, te):
    """I_e = residual fraction of e after ridge-regressing on ALL drivers (V6_31 null = 8%)."""
    mask = D["mask"][te].bool()
    E = e_trace[mask].numpy()
    Dr = torch.cat([D["x"][te], D["nll"][te].unsqueeze(-1), D["pos"][te].float().unsqueeze(-1)], -1)[mask].numpy()
    Dr = (Dr - Dr.mean(0)) / (Dr.std(0) + 1e-9)
    Dr = np.hstack([Dr, np.ones((len(Dr), 1))])
    lam = 1e-2
    Wr = np.linalg.solve(Dr.T @ Dr + lam * np.eye(Dr.shape[1]), Dr.T @ E)
    resid = E - Dr @ Wr
    ie = float((resid ** 2).sum() / (((E - E.mean(0)) ** 2).sum() + 1e-9))
    C = np.cov(resid.T); reff = float((np.trace(C) ** 2) / (np.trace(C @ C) + 1e-12))
    return ie, reff

def run(D, dv, label):
    print(f"\n=== {label} · DV={dv} · held-out ({len(SEEDS)} seeds, val-selected, test-once) ===")
    res = {a: [] for a in ARMS}; flip = []; ies = []; reffs = []
    for seed in SEEDS:
        cmd_shuf, cmd_other = build_tapes(D["_cmd"], D["_emit"], D["_x"], D["_sid"], seed)
        D["cmd_shuf"] = _pad_idx(cmd_shuf, D["_sid"])
        D["cmd_other"] = _pad_idx(cmd_other, D["_sid"])
        tr, va, te = grouped_split(D["x"].shape[0], seed)
        for a in ARMS:
            ck = {"SHUFFLED": "cmd_shuf", "OTHER-SELF": "cmd_other"}.get(a, "cmd")
            loss, etr = train_arm(a, D, tr, va, te, seed, dv, cmd_key=ck)
            res[a].append(loss)
            if a == "TRUE-EC" and etr is not None:
                ie, reff = independence(etr, D, te); ies.append(ie); reffs.append(reff)
        # do()-FLIP: trained TRUE model evaluated with OTHER commands substituted
        fl, _ = train_arm("TRUE-EC", D, tr, va, te, seed, dv, cmd_key="cmd", eval_cmd_key="cmd_other")
        flip.append(fl - res["TRUE-EC"][-1])
    def z(better, worse):
        d = np.array(res[worse]) - np.array(res[better])
        return d.mean(), d.mean() / (d.std(ddof=1) / np.sqrt(len(d)) + 1e-9)
    for a in ARMS: print(f"  {a:<12} {np.mean(res[a]):.4f}")
    print(f"  headroom NO-EC - TRUE-EC = {np.mean(res['NO-EC']) - np.mean(res['TRUE-EC']):+.4f}")
    contrasts = {}
    for b in ("TIMER", "SHUFFLED", "OTHER-SELF", "DRIVER-HIST", "NO-EC"):
        mm, zz = z("TRUE-EC", b); contrasts[b] = (mm, zz)
        print(f"  {b:<12} - TRUE-EC = {mm:+.4f}  z={zz:+.2f}")
    fm = np.mean(flip); fz = fm / (np.std(flip, ddof=1) / np.sqrt(len(flip)) + 1e-9)
    print(f"  do()-FLIP (OTHER subst) NLL degrade = {fm:+.4f}  z={fz:+.2f}")
    if ies:
        ie_lb = np.mean(ies) - 2 * np.std(ies) / np.sqrt(len(ies))
        print(f"  independence I_e = {np.mean(ies):.3f} (2se-LB {ie_lb:.3f})  resid_effrank = {np.mean(reffs):.2f}")
        contrasts["_ie"] = (np.mean(ies), ie_lb, np.mean(reffs))
    contrasts["_flip"] = (fm, fz)
    return contrasts

def _pad_idx(arr1d, sid):
    return batchify({"c": arr1d.astype(np.int32)}, sid)["c"]

def _pad_flt(arr1d, sid):
    return batchify({"c": arr1d.astype(np.float32)}, sid)["c"].float()

# ------------------------------------------------------------- synthetic reafference pos-control ---
def positive_control():
    """Clean reafference instrument that isolates COMMAND IDENTITY (not count/timing): target at t =
    1 iff the decayed STRICT-PAST count of family-A emissions exceeds that of family-B. TOTAL emit
    count is irrelevant (only A-vs-B matters), so a content-free TIMER (constant impulse = total
    count) and DRIVER-HIST (noise) cannot read it; SHUFFLED destroys the A/B time-order. Only a
    register whose impulse distinguishes A from B (TRUE-EC's command embedding) can. x is pure noise."""
    rng = np.random.default_rng(0); nS = 300; Tp = 48; N = nS * Tp
    sid = np.repeat(np.arange(nS), Tp)
    cmd = rng.integers(0, 256, N).astype(np.int32)
    emit = (rng.random(N) < 0.55).astype(np.int8)
    x = rng.standard_normal((N, 6)).astype(np.float32)
    tgt = np.zeros(N, np.float32); nll = np.zeros(N, np.float32); sA = 0.0; sB = 0.0
    for i in range(N):
        if i % Tp == 0: sA = sB = 0.0
        tgt[i] = 1.0 if sA >= sB else 0.0                 # A-vs-B from STRICT PAST (count-invariant)
        nll[i] = 2.0 - 1.6 * (sA >= sB)
        sA *= 0.75; sB *= 0.75
        if emit[i]:
            if cmd[i] % 3 == 0: sA += 1.0                 # family A (1/3 of commands)
            elif cmd[i] % 3 == 1: sB += 1.0               # family B (1/3 of commands)
    return dict(x=x, cmd=cmd, emit=emit.astype(np.float32), nll=nll,
                pos=(np.arange(N) % Tp).astype(np.int32), sid=sid, tgt=tgt)

def load(cache):
    d = np.load(cache)
    x = d["x"].astype(np.float32); x = (x - x.mean(0)) / (x.std(0) + 1e-9)
    return dict(x=x, cmd=d["cmd"], emit=d["emit"].astype(np.float32), nll=d["nll"].astype(np.float32),
                pos=d["pos"], sid=d["sid"])

def pack(raw):
    """batchify all fields; keep raw 1d copies for tape building."""
    sid = raw["sid"]
    D = batchify({"x": raw["x"], "emit": raw["emit"], "nll": raw["nll"],
                  "cmd": raw["cmd"].astype(np.int32), "pos": raw["pos"].astype(np.int32)}, sid)
    D["_cmd"] = raw["cmd"]; D["_emit"] = raw["emit"]; D["_x"] = raw["x"]; D["_sid"] = sid
    D["tgt_emit"] = D["emit"]           # natural: target == emit tape; pos-control overrides target only
    return D

def main():
    cache = sys.argv[1] if len(sys.argv) > 1 else "lab/v6/v6_33_cache.npz"
    print("== POSITIVE CONTROL (synthetic reafference · instrument check only) ==")
    pc = positive_control(); Dp = pack(pc)
    # keep the real emit EVENT tape (Dp["emit"]) for register gating; predict the reafference TARGET
    Dp["tgt_emit"] = _pad_flt(pc["tgt"], pc["sid"])
    cpc = run(Dp, "emit", "POS-CTRL")
    tt = cpc["TIMER"][1]; ss = cpc["SHUFFLED"][1]
    ok = (tt >= 3 and ss >= 3)
    print(f"  POS-CTRL: TRUE beats TIMER z={tt:.2f}, SHUFFLED z={ss:.2f} -> {'PASS' if ok else 'FAIL -> VOID'}")

    print("\n== NATURAL ==")
    D = pack(load(cache))
    c_emit = run(D, "emit", "NATURAL")
    c_nll = run(pack(load(cache)), "nll", "NATURAL")

    print("\n=== FROZEN VERDICT (primary DV = emit) ===")
    if not ok:
        print("VOID — positive control failed (instrument cannot read a real reafference rule).")
        return 0
    passes = []
    for b in ("TIMER", "SHUFFLED", "OTHER-SELF", "DRIVER-HIST"):
        mm, zz = c_emit[b]; passes.append(mm >= 0.010 and zz >= 3.0)
    fm, fz = c_emit["_flip"]; flip_ok = (fm >= 0.010 and fz >= 3.0)
    ie, ie_lb, reff = c_emit.get("_ie", (0, 0, 0))
    ind_ok = (ie >= 0.15 and ie_lb > 0.08 and reff >= 2.0)
    invalid = False
    if all(passes) and flip_ok and ind_ok:
        v = "PRESENT — independent CAUSAL efference-copy faculty (DIRECTIONAL; TERMINAL via anima-py port)"
    elif not ind_ok and ie <= 0.08:
        v = "ABSENT — register is a driver re-expression (independence below V6_31 8% null)"
    else:
        v = "ABSENT — emit-autocorrelation / timer / difficulty-integral (a control matched TRUE-EC)"
    print(f"  TRUE-EC beats [TIMER,SHUFFLED,OTHER,DRIVER-HIST] z>=3: {passes}")
    print(f"  do()-FLIP degrade ok: {flip_ok} ({fm:+.4f}, z={fz:.2f})")
    print(f"  independence ok: {ind_ok} (I_e={ie:.3f} LB={ie_lb:.3f} effrank={reff:.2f})")
    print(f"\nVERDICT: {v}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
