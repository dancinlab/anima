"""H_1017 — the MECHANISM behind the H_1012/H_1014 split: is the MI that planning
adds REDUNDANT (not synergistic), explaining why faithful_phi RISES while big-Phi FALLS?

MISSION
-------
H_1012 (terminal n={4,5}): on an identical discretized substrate PLANNING RAISES the
MIP-EI scalar faithful_phi but LOWERS the system big-Phi (a robust sign-split). H_1014
showed the split CO-OCCURS with a large pairwise-MI coupling rise (Δmi_total ≈ +4.1)
while big-Phi's irreducible structure collapses (Δbigphi_total ≈ −6.7) — both engines
read the SAME MI rise OPPOSITELY. H_1014 left the MECHANISM open.

HYPOTHESIS (the WHY)
--------------------
The scalar rises while integration falls because the MI planning adds is REDUNDANT,
not synergistic. big-Phi rewards IRREDUCIBLE (synergistic) structure; the pairwise-MI
scalar counts SHARED (redundant) info just as much. If planning's ΔMI is REDUNDANCY-
dominated, the scalar goes UP (more shared/effective info per mechanism) while big-Phi
goes DOWN (redundant copies are reducible → irreducibility falls).

METHOD — Williams & Beer (2010) I_min PID, pure numpy, EXACT on the n=4 binary bits
-----------------------------------------------------------------------------------
REUSE H_1014 substrate VERBATIM: matched n=4 binary discretization, the 4 intervention
generators (planning[known split], imagination/guided[known no-split], chaos[NEW]),
the H_1004 engines for the SPLIT label, and the H_1012 prove_mirrors_at_n(4) proof BEFORE
scoring. ADD a self-contained Williams-Beer I_min PID on the SAME bits.

Each unit = a binary RV over the rollout (empirical joint over time steps). For target T
and two sources S1,S2:
  specific info  I(T=t;Si) = Σ_si p(si|t)[ log2(1/p(si)) − log2(1/p(si|t)) ]   (WB)
  Redundancy  Red = Σ_t p(t) · min_i I(T=t;Si)                                 (I_min)
  unique      Unq_i = I(T;Si) − Red
  Synergy     Syn = I(T;S1S2) − I(T;S1) − I(T;S2) + Red
Aggregate over ALL 4 targets × 3 source-pairs = 12 atoms → red_total, syn_total.

The PID is the EXPLANATORY variable — it is NOT a Phi proxy/replacement; it decomposes
the SAME bits the real engines consume to attribute the MI rise to redundancy vs synergy.
Phi numbers come ONLY from the stdlib mirrors (a_phi_iit4_tool).

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 — both engines exact;
big-Phi super-exponential so n=4 is the rung for the full SET x seeds. PID exact +
deterministic. Scale-transfer UNVERIFIED. NOT a forge binary; $0 CPU-local, no GPU.
"""
import sys, os, math, time, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

# ── Import the H_1014 driver VERBATIM (it imports H_1004 engines + H_1012 proof). ──
import importlib.util as _ilu
_h1014_path = os.path.join(HERE, "h1014_intervention_split_predictor.py")
_spec = _ilu.spec_from_file_location("h1014", _h1014_path)
_h1014 = _ilu.module_from_spec(_spec)
_src = open(_h1014_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1014_path, "exec"), _h1014.__dict__)

# reuse everything verbatim
prove_mirrors_at_n = _h1014.prove_mirrors_at_n
latent_to_binary_seq = _h1014.latent_to_binary_seq
binary_seq_to_tpm = _h1014.binary_seq_to_tpm
modal_state = _h1014.modal_state
binary_seq_to_faithful_state = _h1014.binary_seq_to_faithful_state
build_mi_matrix = _h1014.build_mi_matrix
faithful_phi_from_mi = _h1014.faithful_phi_from_mi
big_phi = _h1014.big_phi
cohens_d = _h1014.cohens_d
welch_t = _h1014.welch_t
LATENT = _h1014.LATENT
N_SEEDS = _h1014.N_SEEDS
gen_planning = _h1014.gen_planning
gen_imagination = _h1014.gen_imagination
gen_guided = _h1014.gen_guided
gen_chaos = _h1014.gen_chaos

LOG2 = math.log(2.0)

# ═══════════════════════════════════════════════════════════════════════════
# WILLIAMS-BEER I_min PID — exact, pure numpy, on the SAME n=4 binary unit-traces.
# Each unit is a binary RV; the empirical distribution is over the rollout steps.
# ═══════════════════════════════════════════════════════════════════════════
def _mi_discrete(x, y):
    """Standard discrete MI (bits) of two integer-valued sequences (empirical)."""
    n = len(x)
    if n == 0:
        return 0.0
    vx = np.unique(x); vy = np.unique(y)
    if len(vx) <= 1 or len(vy) <= 1:
        return 0.0
    mi = 0.0
    for a in vx:
        pa = np.mean(x == a)
        for b in vy:
            pb = np.mean(y == b)
            pab = np.mean((x == a) & (y == b))
            if pab > 0.0:
                mi += pab * (math.log(pab / (pa * pb)) / LOG2)
    return mi if mi > 0.0 else 0.0

def _specific_info(t_val, T, S):
    """Williams-Beer specific information I(T=t ; S) in bits.
       I(T=t;S) = Σ_s p(s|t) [ log2(1/p(s)) − log2(1/p(s|t)) ]
                = Σ_s p(s|t) log2( p(s|t) / p(s) )."""
    mask_t = (T == t_val)
    pt = np.mean(mask_t)
    if pt <= 0.0:
        return 0.0
    vs = np.unique(S)
    info = 0.0
    for s in vs:
        ps = np.mean(S == s)
        ps_given_t = np.mean(S[mask_t] == s)
        if ps_given_t > 0.0 and ps > 0.0:
            info += ps_given_t * (math.log(ps_given_t / ps) / LOG2)
    return info

def _pid_two_source(T, S1, S2):
    """Williams-Beer I_min PID of target T from sources S1, S2 (all integer seqs).
       Returns (Red, Unq1, Unq2, Syn). Red = I_min, Syn from the lattice identity."""
    vT = np.unique(T)
    # I_min redundancy = Σ_t p(t) · min_i I(T=t ; Si)
    red = 0.0
    for t in vT:
        pt = np.mean(T == t)
        i1 = _specific_info(t, T, S1)
        i2 = _specific_info(t, T, S2)
        red += pt * min(i1, i2)
    if red < 0.0:
        red = 0.0
    mi1 = _mi_discrete(T, S1)
    mi2 = _mi_discrete(T, S2)
    # joint source state = 2*S1 + S2 (binary), generalizes via pairing for >2 levels
    Sj = (S1.astype(np.int64) << 1) | S2.astype(np.int64) if (
        set(np.unique(S1)) <= {0, 1} and set(np.unique(S2)) <= {0, 1}) else (
        S1.astype(np.int64) * (int(S2.max()) + 1) + S2.astype(np.int64))
    mi_joint = _mi_discrete(T, Sj)
    unq1 = mi1 - red
    unq2 = mi2 - red
    syn = mi_joint - red - unq1 - unq2   # = mi_joint - mi1 - mi2 + red
    return red, unq1, unq2, syn

def pid_system(bits):
    """Aggregate WB I_min PID over the whole 4-unit system: enumerate all
       (target, {2 sources}) atoms (4 × C(3,2)=3 = 12) and SUM red / syn.
       bits = (n_steps × n_units) binary. Returns dict with red_total, syn_total,
       unq_total, and the raw (pre-clamp) synergy for audit."""
    bits = np.asarray(bits, dtype=np.int64)
    T, n = bits.shape
    cols = [bits[:, u] for u in range(n)]
    red_total = 0.0
    syn_total = 0.0
    syn_total_raw = 0.0
    unq_total = 0.0
    natoms = 0
    for tgt in range(n):
        others = [u for u in range(n) if u != tgt]
        for s1, s2 in itertools.combinations(others, 2):
            red, unq1, unq2, syn = _pid_two_source(cols[tgt], cols[s1], cols[s2])
            red_total += max(red, 0.0)
            syn_total += max(syn, 0.0)        # clamp tiny numerical negatives
            syn_total_raw += syn              # raw for audit
            unq_total += max(unq1, 0.0) + max(unq2, 0.0)
            natoms += 1
    return dict(red_total=red_total, syn_total=syn_total,
                syn_total_raw=syn_total_raw, unq_total=unq_total, natoms=natoms)

# ═══════════════════════════════════════════════════════════════════════════
# substrate reads — ONE discretization → SPLIT label (both engines) + PID + mi_total.
# ═══════════════════════════════════════════════════════════════════════════
def substrate_reads(H):
    bits, n = latent_to_binary_seq(H)
    # big-Phi (H_1004 verbatim)
    tpm, sc = binary_seq_to_tpm(bits, n)
    s = modal_state(sc)
    bphi = big_phi(tpm, n, s)[0]
    # faithful (H_1004 verbatim) — SAME bits
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    mi = build_mi_matrix(fstate, fn, fdim, 2)
    fphi = faithful_phi_from_mi(mi, fn)
    mi_total = float(np.triu(mi, 1).sum())
    # PID on the SAME bits
    p = pid_system(bits)
    return dict(big=bphi, faith=fphi, mi_total=mi_total,
                red_total=p["red_total"], syn_total=p["syn_total"],
                unq_total=p["unq_total"], syn_raw=p["syn_total_raw"])

def _agg(rows):
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}

def _contrast(I, B, k):
    c = I[k].mean() - B[k].mean()
    try:
        d = cohens_d(I[k], B[k])
    except Exception:
        d = float("nan")
    try:
        _, p = welch_t(I[k], B[k])
    except Exception:
        p = float("nan")
    return dict(contrast=c, d=d, p=p, base=B[k].mean(), intv=I[k].mean())

def score(name, gen, t0):
    base_rows, intv_rows = [], []
    for s in range(N_SEEDS):
        Hb, Hi = gen(s)
        base_rows.append(substrate_reads(Hb))
        intv_rows.append(substrate_reads(Hi))
        print(f"    [{name} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    B = _agg(base_rows); I = _agg(intv_rows)
    return {k: _contrast(I, B, k) for k in
            ("big", "faith", "mi_total", "red_total", "syn_total", "unq_total", "syn_raw")}

def sgn(x, eps=1e-3):
    return +1 if x > eps else (-1 if x < -eps else 0)

def main():
    print("=" * 80)
    print("H_1017 — split MECHANISM: is planning's added MI REDUNDANT (not synergistic)?")
    print("substrate=CPU-mirror (numpy) — H_1004 engines + H_1012 proof, RE-PROVEN == stdlib at n=4")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("PID = Williams-Beer (2010) I_min redundancy lattice, EXACT pure-numpy on the SAME bits")
    print("  (the EXPLANATORY variable — NOT a Phi proxy/replacement; Phi from stdlib mirrors only)")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print("SET: planning[known SPLIT] + imagination[no-split] + guided[no-split] + chaos[NEW]")
    print("PASS = planning Δred >> Δsyn AND distinguishes planning from the no-split control(s).")
    print("=" * 80)
    print()

    # STEP 0 — equivalence proof at n=4 (H_1012 discipline) BEFORE scoring.
    print("EQUIVALENCE PROOF at n=4 (H_1012 prove_mirrors_at_n — re-prove BOTH mirrors vs stdlib):")
    ok = prove_mirrors_at_n(4)
    # PID determinism + non-negativity check on a fixed sample.
    rng = np.random.default_rng(20260607)
    H = rng.standard_normal((40, LATENT))
    r1 = substrate_reads(H); r2 = substrate_reads(H)
    pid_det = (abs(r1["red_total"] - r2["red_total"]) < 1e-12 and
               abs(r1["syn_total"] - r2["syn_total"]) < 1e-12)
    pid_nonneg = (r1["red_total"] >= -1e-9 and r1["syn_total"] >= -1e-9)
    print(f"  PID deterministic re-run: {pid_det}   red_total={r1['red_total']:.6f} "
          f"syn_total={r1['syn_total']:.6f} (raw_syn={r1['syn_raw']:+.6f}) nonneg={pid_nonneg}")
    # WB sanity: a pure COPY (S1==S2==T) is pure redundancy (syn≈0); XOR is pure synergy.
    Tc = np.array([0,1,0,1,1,0,1,0]); rc, _, _, sc_ = _pid_two_source(Tc, Tc, Tc)
    Xa = np.array([0,0,1,1,0,0,1,1]); Xb = np.array([0,1,0,1,0,1,0,1]); Xt = Xa ^ Xb
    rx, _, _, sx = _pid_two_source(Xt, Xa, Xb)
    print(f"  WB sanity: COPY(T;T,T) red={rc:.4f} syn={sc_:.4f} (expect red>0,syn~0) | "
          f"XOR(T;A,B) red={rx:.4f} syn={sx:.4f} (expect red~0,syn>0)")
    copy_ok = (rc > 0.5 and abs(sc_) < 1e-6)
    xor_ok = (rx < 1e-6 and sx > 0.5)
    print(f"  WB canonical-case check: COPY={copy_ok} XOR={xor_ok}")
    ok = ok and pid_det and pid_nonneg and copy_ok and xor_ok
    print(f"  EQUIVALENCE + PID-VALIDITY PROOF n=4: {'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
    if not ok:
        raise SystemExit("equivalence/PID proof failed — aborting")
    print()

    SET = [
        ("planning", gen_planning, "known SPLIT (H_1004/H_1012)"),
        ("imagination", gen_imagination, "known no-split (H_1004)"),
        ("guided", gen_guided, "known no-split (H_1004)"),
        ("chaos", gen_chaos, "NEW intervention (gain=1.4)"),
    ]
    t0 = time.time()
    results = {}
    for name, gen, note in SET:
        print(f"################ SCORE intervention = {name}  [{note}] ################")
        r = score(name, gen, t0)
        results[name] = r
        split = sgn(r["faith"]["contrast"]) != sgn(r["big"]["contrast"])
        dred = r["red_total"]["contrast"]; dsyn = r["syn_total"]["contrast"]
        print(f"  --- {name}: intervention vs baseline (matched n=4 binary discretization) ---")
        print(f"     big-Phi      contrast={r['big']['contrast']:+.4f} d={r['big']['d']:+.3f} p={r['big']['p']:.3e}")
        print(f"     faithful_phi contrast={r['faith']['contrast']:+.4f} d={r['faith']['d']:+.3f} p={r['faith']['p']:.3e}")
        print(f"     SPLIT label (sign(faith)!=sign(big)): {split}")
        print(f"     Δredundancy  contrast={dred:+.4f} d={r['red_total']['d']:+.3f} p={r['red_total']['p']:.3e}")
        print(f"     Δsynergy     contrast={dsyn:+.4f} d={r['syn_total']['d']:+.3f} p={r['syn_total']['p']:.3e}")
        print(f"     Δunique      contrast={r['unq_total']['contrast']:+.4f}")
        print(f"     (cross-check) Δmi_total={r['mi_total']['contrast']:+.4f} | "
              f"redundancy-dominated (Δred>Δsyn & Δred>0): {dred > dsyn and dred > 0.0} | "
              f"red:syn ratio={ (dred/dsyn) if abs(dsyn)>1e-9 else float('inf'):+.2f}")
        print()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER TEST
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("PID DECOMPOSITION MATRIX — Δredundancy vs Δsynergy per intervention")
    print("=" * 80)
    print(f"  {'intervention':12s} | {'SPLIT?':>6s} | {'Δredund':>9s} | {'Δsynergy':>9s} | "
          f"{'red>syn&>0':>10s} | {'Δmi_total':>9s}")
    rows = {}
    for name, gen, note in SET:
        r = results[name]
        split = sgn(r["faith"]["contrast"]) != sgn(r["big"]["contrast"])
        dred = r["red_total"]["contrast"]; dsyn = r["syn_total"]["contrast"]
        reddom = (dred > dsyn and dred > 0.0)
        rows[name] = dict(split=split, dred=dred, dsyn=dsyn, reddom=reddom)
        print(f"  {name:12s} | {str(split):>6s} | {dred:+9.4f} | {dsyn:+9.4f} | "
              f"{str(reddom):>10s} | {r['mi_total']['contrast']:+9.4f}")
    print()

    pl = rows["planning"]
    controls = {k: v for k, v in rows.items() if k != "planning"}
    nosplit_controls = {k: v for k, v in controls.items() if not v["split"]}

    # planning redundancy-dominated?
    plan_reddom = pl["reddom"]
    plan_margin = pl["dred"] - pl["dsyn"]
    print(f"Planning: Δredundancy={pl['dred']:+.4f}  Δsynergy={pl['dsyn']:+.4f}  "
          f"redundancy-dominated (Δred>Δsyn & Δred>0): {plan_reddom}  (margin Δred−Δsyn={plan_margin:+.4f})")

    # does redundancy-dominance DISTINGUISH planning from the no-split control(s)?
    # planning's redundancy-margin must EXCEED every no-split control's redundancy-margin.
    print("No-split controls (redundancy-margin Δred−Δsyn):")
    distinguishes = plan_reddom and len(nosplit_controls) > 0
    for k, v in nosplit_controls.items():
        cm = v["dred"] - v["dsyn"]
        print(f"  {k:12s}: Δred={v['dred']:+.4f} Δsyn={v['dsyn']:+.4f} "
              f"margin={cm:+.4f} reddom={v['reddom']}  (planning margin {plan_margin:+.4f} > this: {plan_margin > cm})")
        if not (plan_margin > cm):
            distinguishes = False

    print()
    print("=" * 80)
    redundancy_explains = plan_reddom and distinguishes
    if redundancy_explains:
        print("OVERALL: REDUNDANCY-EXPLAINS-SPLIT — planning's added MI is REDUNDANCY-DOMINATED")
        print("  (Δredundancy >> Δsynergy, Δred>0) AND this redundancy dominance DISTINGUISHES")
        print("  the split-inducing planning intervention from the no-split control(s) (planning's")
        print("  redundancy-margin exceeds every no-split control's). This mechanistically explains")
        print("  the H_1012/H_1014 split: the pairwise-MI scalar faithful_phi RISES on the redundant")
        print("  (shared) info, while system big-Phi FALLS because redundant copies are REDUCIBLE —")
        print("  synergy, which big-Phi rewards, does not carry the MI rise. H_1014's open WHY answered.")
        print("  VERDICT-TOKEN: REDUNDANCY-EXPLAINS-SPLIT")
    else:
        print("OVERALL: REDUNDANCY-DOES-NOT-EXPLAIN (CLOSED-NEGATIVE) — either planning's added MI is")
        print("  NOT redundancy-dominated (Δsyn >= Δred) or the redundancy/synergy split does NOT")
        print("  distinguish planning from the no-split control. The redundancy explanation for the")
        print("  faithful-up/big-Phi-down split is FALSIFIED; the redundancy axis is RULED OUT as the")
        print("  split mechanism (a_paper_negative_ok). The mechanism remains open.")
        print("  VERDICT-TOKEN: REDUNDANCY-DOES-NOT-EXPLAIN")
    print("=" * 80)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 — both engines EXACT;")
    print("big-Phi super-exponential so n=4 is the rung for the full SET x 30 seeds. Both CPU mirrors")
    print("RE-PROVEN == stdlib at n=4 (H_1012 prove_mirrors_at_n) BEFORE scoring; the PID is exact +")
    print("deterministic on the SAME bits and validated on canonical COPY(redundant)/XOR(synergy)")
    print("cases. The PID is NOT a proxy for Phi. Scale-transfer UNVERIFIED. g5 CODE-measured")
    print("(no LLM self-judge, p7), a_phi_iit4_tool. NOT a forge binary; $0 CPU-local, no GPU.")

if __name__ == "__main__":
    main()
