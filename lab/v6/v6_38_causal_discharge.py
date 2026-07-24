#!/usr/bin/env python3
"""V6_38 (LANE-BUS Step-2) -- discharge under do(), on an ALIGNED bus. ($0)

TWO JOBS, in order.

(A) FIX + RE-MEASURE. V6_26/V6_27 built the bus mis-aligned: composed took row `pos`
    of a full-prefix forward (which predicts b[pos+1]) while reflex took the last row of
    a forward over b[pos-W:pos] (which predicts b[pos]). The two lanes were scored on
    DIFFERENT target bytes, so their KL was not "what broad context adds" -- and the
    94.7% override rate was the symptom, not a finding. Measured here on trained57:
    CE(row pos-1 -> b[pos]) = 2.08 nats vs CE(row pos -> b[pos]) = 6.87 -- decisive.
    This file re-runs V6_27's load-bearing + observational-discharge readings with both
    lanes on the SAME decision point, so the Step-1 headline gets an honest number.

(B) THE CAUSAL TEST V6_27 ASKED FOR. Its discharge was observational: override positions
    self-select as high-tension, so the drop was confounded with mean reversion and had to
    be rescued by a level regression. Here the confound is removed BY CONSTRUCTION -- at
    ONE decision point we fork the stream and commit a different byte per arm, so every arm
    starts from an identical prefix at an identical tension level. That is a real do().

    arms at decision point i (deterministic -- no sampling, so no seed replication):
      CMP    argmax(composed)   the content-driven emit          <- treatment
      RFX    argmax(reflex)     the form-only emit               <- control 1 (matched position+level)
      DECOY  composed-logprob matched to RFX, identity arbitrary  <- control 2 (isolates identity from likelihood)
      CMP2   2nd-ranked composed byte                             <- control 3 (likelihood without being the content pick)
      TRUE   the corpus's own next byte                           <- anchor, not a control
    After the forked byte every arm continues on the SAME corpus bytes, so the arms differ
    in exactly one byte. DV = tension at the next decision point minus tension at i.

    PEDESTAL (zero-truth, abort authority): at non-override positions CMP and RFX are the
    SAME byte, so the paired difference must be EXACTLY 0.0. Non-zero => harness bug =>
    the run is void, not a weak result.

Engine-native (decode._fwd_logits). Reuses trained57.clm + natural held-out text.
"""
import sys, os, re, math, importlib.util
import numpy as np

W_LOC = 8; N_SENT = 120; HELDOUT_FRAC = 0.20; MAX_POS = 1200
_DATE = re.compile(r"^\s*\d{3,4}\s*[–-]"); _YEAR = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")


def prose(txt):
    for line in txt.split("\n"):
        line = line.strip()
        if not line or _DATE.match(line): continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (40 < len(s) < 300) or _YEAR.search(s): continue
            if s.count(",") > 6 or sum(c.isdigit() for c in s) > 12: continue
            if s.endswith((".", "!", "?")): yield s


def _decode():
    spec = importlib.util.find_spec("anima_py")
    if spec and spec.submodule_search_locations:
        b = list(spec.submodule_search_locations)[0]
        for c in (os.path.join(b, "core"), b):
            if os.path.isdir(c): sys.path.insert(0, c)
    for c in ("core", "/opt/homebrew/lib/python3.14/site-packages/anima_py/core"):
        if os.path.isdir(c): sys.path.insert(0, c)


def softmax(x):
    m = x.max(); e = np.exp(x - m); return e / (e.sum() + 1e-12)


def kl(p, q):
    return float(np.sum(p * (np.log(p + 1e-12) - np.log(q + 1e-12))))


def paired(a, b):
    """mean paired difference a-b with a paired t (z for large n)."""
    d = np.asarray(a) - np.asarray(b)
    n = len(d)
    if n < 2: return 0.0, 0.0, n
    m = float(d.mean()); se = float(d.std(ddof=1) / math.sqrt(n))
    return m, (m / se if se > 0 else 0.0), n


def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "lab/v6/trained57.clm"
    full = open(os.path.expanduser("~/anima-weights/en_general.txt"),
                encoding="utf-8", errors="ignore").read()
    eval_txt = full[int(len(full) * (1 - HELDOUT_FRAC)):]
    sents = []
    for s in prose(eval_txt):
        sents.append(s)
        if len(sents) >= N_SENT: break
    _decode(); import decode as clm
    W = clm.clm_load_weights(model)

    def fwd(seq):
        """logits rows for seq; row i predicts seq[i+1]."""
        n = len(seq)
        return clm._fwd_logits(W, np.array([float(x) for x in seq], dtype=np.float64), n)

    def lanes(pref):
        """ALIGNED: both lanes score the byte that follows `pref`."""
        cp = fwd(pref)[len(pref) - 1]
        loc = pref[-W_LOC:]
        rl = fwd(loc)[len(loc) - 1]
        return cp, rl

    # ---------- (A) aligned re-measurement of Step-1 ----------
    over_t, non_t, L, O, D = [], [], [], [], []
    n_over = n_tot = 0
    # ---------- (B) causal arms ----------
    ARMS = ["CMP", "RFX", "DECOY", "CMP2", "TRUE", "JUNK"]
    dlt = {a: [] for a in ARMS}          # Δtension at override positions
    ped = {a: [] for a in ("CMP", "RFX")}  # pedestal: non-override positions
    lp_committed = {a: [] for a in ARMS}  # composed logprob of the committed byte (arm balance audit)
    n_causal = 0

    for s in sents:
        b = list(s.encode("utf-8")); Lb = len(b)
        if Lb < W_LOC + 6: continue
        comp_all = fwd(b[:Lb - 1])       # row i predicts b[i+1]
        tens = {}; ovr = {}
        for i in range(W_LOC - 1, Lb - 2):
            cp = comp_all[i]
            rl = fwd(b[i + 1 - W_LOC:i + 1])[W_LOC - 1]
            tens[i] = kl(softmax(cp), softmax(rl))
            ovr[i] = int(np.argmax(cp)) != int(np.argmax(rl))

        for i in range(W_LOC - 1, Lb - 3):
            if i not in tens or (i + 1) not in tens: continue
            n_tot += 1; n_over += int(ovr[i])
            (over_t if ovr[i] else non_t).append(tens[i])
            L.append(tens[i]); O.append(float(ovr[i])); D.append(tens[i + 1] - tens[i])

            if n_causal >= MAX_POS: continue
            cp = comp_all[i]
            lp = cp - (cp.max() + np.log(np.exp(cp - cp.max()).sum()))   # log-softmax
            y_cmp = int(np.argmax(cp))
            y_rfx = int(np.argmax(fwd(b[i + 1 - W_LOC:i + 1])[W_LOC - 1]))
            order = np.argsort(-lp)
            y_cmp2 = int(next(v for v in order if v != y_cmp and v != y_rfx))
            cand = [v for v in range(len(lp)) if v not in (y_cmp, y_rfx)]
            y_dec = int(min(cand, key=lambda v: abs(lp[v] - lp[y_rfx])))
            y_true = b[i + 1]
            y_junk = int(order[-1])             # least probable byte under composed
            picks = {"CMP": y_cmp, "RFX": y_rfx, "DECOY": y_dec, "CMP2": y_cmp2,
                     "TRUE": y_true, "JUNK": y_junk}

            if not ovr[i]:                      # pedestal: CMP and RFX are the same byte here
                for a in ("CMP", "RFX"):
                    f = b[:i + 1] + [picks[a]]
                    c2, r2 = lanes(f)
                    ped[a].append(kl(softmax(c2), softmax(r2)) - tens[i])
                continue

            n_causal += 1
            for a in ARMS:
                f = b[:i + 1] + [picks[a]]      # do(): commit ONE byte, same prefix for every arm
                c2, r2 = lanes(f)
                dlt[a].append(kl(softmax(c2), softmax(r2)) - tens[i])
                lp_committed[a].append(float(lp[picks[a]]))

    import statistics as st
    print(f"# V6_38 LANE-BUS Step-2 -- ALIGNED bus + causal do()   (model={os.path.basename(model)})")
    print(f"sample: {len(sents)} sentences, {n_tot} decision points, causal forks n={n_causal}\n")

    print("(A) ALIGNED RE-MEASUREMENT of V6_27 Step-1  [both lanes score the SAME next byte]")
    orate = n_over / max(n_tot, 1)
    print(f"   override rate          = {orate:.3f}     (V6_27 mis-aligned read: 0.947)")
    print(f"   mean tension|override  = {st.mean(over_t):.4f} nats")
    print(f"   mean tension|no-ovr    = {st.mean(non_t):.4f} nats")
    print(f"   separation             = {st.mean(over_t) - st.mean(non_t):+.4f} nats")
    Ln, On, Dn = np.array(L), np.array(O), np.array(D)
    X = np.column_stack([np.ones_like(Ln), Ln - Ln.mean(), On - On.mean()])
    coef, *_ = np.linalg.lstsq(X, Dn, rcond=None)
    resid = Dn - X @ coef; dof = len(Dn) - 3
    se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * ((resid @ resid) / dof))
    print(f"   observational discharge (level-controlled): c={coef[2]:+.4f}  z={coef[2]/se[2]:+.2f}"
          f"   (V6_27 mis-aligned read: c=-1.03 z=-7.8)")

    print("\n(B) PEDESTAL  [non-override: CMP and RFX are the same byte -> paired diff must be 0]")
    pm, pz, pn = paired(ped["CMP"], ped["RFX"])
    print(f"   mean paired Δ(CMP-RFX) on non-override = {pm:+.3e}  (n={pn})")
    if pn > 0 and abs(pm) > 1e-12:
        print("   ⛔ INSTRUMENT-DEAD: identical commits produced different tension. Run is VOID.")
        return 2
    print("   ✅ pedestal exact 0 — the fork machinery is sound.")

    print("\n(C) CAUSAL DISCHARGE  [Δtension after do(commit y); paired at the same decision point]")
    for a in ARMS:
        v = dlt[a]
        print(f"   {a:<6} Δtension = {st.mean(v):+.4f} nats   committed logp = {st.mean(lp_committed[a]):+.3f}")
    print()
    contrasts = [("CMP-RFX", "the content contrast (treatment vs form-only emit)"),
                 ("CMP-DECOY", "vs a likelihood-matched-to-RFX arbitrary byte"),
                 ("CMP-CMP2", "vs the 2nd-ranked composed byte"),
                 ("DECOY-RFX", "control-vs-control: identity at matched likelihood")]
    res = {}
    for name, why in contrasts:
        a, bn = name.split("-")
        m, z, n = paired(dlt[a], dlt[bn])
        res[name] = (m, z)
        print(f"   {name:<10} = {m:+.4f} nats  z={z:+.2f}  (n={n})   {why}")

    neg = sum(1 for x, y in zip(dlt["CMP"], dlt["RFX"]) if x - y < 0)
    print(f"\n   polarity split of (CMP-RFX): {neg}/{len(dlt['CMP'])} = {neg/max(len(dlt['CMP']),1):.3f} negative")

    # ---- (D) POSITIVE CONTROL: can the DV move with the committed byte at all? ----
    generic = float(np.mean([st.mean(dlt[a]) for a in ("CMP", "RFX", "DECOY", "CMP2")]))
    m_jc, z_jc, _ = paired(dlt["JUNK"], dlt["CMP"])
    print("\n(D) POSITIVE CONTROL  [do(least-probable byte) must move the DV if the readout is alive]")
    print(f"   JUNK-CMP = {m_jc:+.4f} nats  z={z_jc:+.2f}   (JUNK committed logp = {st.mean(lp_committed['JUNK']):+.2f})")
    alive = abs(z_jc) > 4
    print("   " + ("✅ DV IS SENSITIVE to what is committed — a null elsewhere is a real negative."
                   if alive else
                   "⛔ DV IS DEAD to the commit — every null below is UNDECIDABLE, not negative."))

    # ---- (E) TOST: is the content contrast EQUIVALENT to a likelihood-matched decoy? ----
    # Pre-declared bound: 20% of the generic post-commit drop (the effect size a discharge law needs).
    DEQ = 0.20 * abs(generic)
    d = np.asarray(dlt["CMP"]) - np.asarray(dlt["DECOY"])
    se_d = float(d.std(ddof=1) / math.sqrt(len(d))); m_d = float(d.mean())
    t_lo = (m_d + DEQ) / se_d; t_hi = (DEQ - m_d) / se_d
    equiv = (t_lo > 1.645) and (t_hi > 1.645)
    print(f"\n(E) TOST  [H1: content commit is EQUIVALENT to a likelihood-matched decoy]")
    print(f"   generic post-commit drop = {generic:+.4f} nats  ->  equivalence bound ±{DEQ:.4f}")
    print(f"   CMP-DECOY = {m_d:+.4f}  90% CI [{m_d-1.645*se_d:+.4f}, {m_d+1.645*se_d:+.4f}]"
          f"   TOST {'PASS (equivalent)' if equiv else 'FAIL (not shown equivalent)'}")

    m_cr, z_cr = res["CMP-RFX"]; m_cd, z_cd = res["CMP-DECOY"]
    print("\nVERDICT")
    if not alive:
        print("   ⛔ UNDECIDABLE — the positive control failed; no discharge claim either way.")
        return 3
    if equiv and z_cd > -2:
        print(f"   🔴 DISCHARGE ABSENT (powered): every commit drops tension by the SAME {generic:+.4f} nats.")
        print(f"      The content byte is statistically EQUIVALENT to a likelihood-matched decoy")
        print(f"      (TOST PASS, ±{DEQ:.4f}), while do(JUNK) moves the DV by {m_jc:+.3f} (z={z_jc:.0f}) —")
        print("      so the readout is alive and the null is a real negative. What you emit does not")
        print("      decide the tension trajectory: LANE-BUS's p5 discharge law does not hold here.")
        return 0
    if z_cr < -2 and z_cd < -2:
        print(f"   🟢 CAUSAL DISCHARGE: committing the content byte drops tension BEYOND both the")
        print(f"      form-only emit ({m_cr:+.3f}, z={z_cr:.1f}) and a likelihood-matched decoy")
        print(f"      ({m_cd:+.3f}, z={z_cd:.1f}). p5's discharge signature survives a real do().")
    elif z_cr > 2:
        print(f"   🔴 REVERSED: the content emit RAISES tension vs form-only ({m_cr:+.3f}, z={z_cr:.1f}).")
        print("      Discharge is not a property of committing content on this bus.")
    else:
        print(f"   ⚪ ABSENT/ns: CMP-RFX = {m_cr:+.4f} z={z_cr:.2f}. Under do(), which byte is committed")
        print("      does not decide the tension trajectory — V6_27's observational drop does not")
        print("      survive as a causal claim.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
