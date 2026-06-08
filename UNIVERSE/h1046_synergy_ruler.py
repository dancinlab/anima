"""H_1046 — is the Williams-Beer SYNERGY atom big-Phi's cheap "genuine integration"
component? A synergy-only ruler should AGREE with big-Phi's DIRECTION across a planning
battery (and TRACK big-Phi NOT faithful where they split) while needing NO MIP search.

MISSION
-------
H_1017 (prior GREEN) found planning's MI rise is REDUNDANCY-dominated, and big-Phi sees
redundant copies as reducible (integration DOWN) while the scalar EI credits them as
integration (UP). CONSTRUCTIVE: the Williams-Beer SYNERGY atom ALONE — the irreducible,
joint-only info neither source carries alone — is the "genuine integration" signal big-Phi
was trying to capture. So a SYNERGY-ONLY ruler should:
  (1) AGREE with big-Phi's contrast SIGN across >=6 toy substrates (>=5/6),
  (2) where big-Phi and faithful phi_EI DISAGREE (the split substrates), TRACK big-Phi NOT
      faithful, and
  (3) be CHEAPER — the WB I_min synergy needs NO 2^(n-1) MIP bipartition enumeration.

METHOD — full REUSE, no reinvention (a_phi_iit4_tool, g61 SSOT)
--------------------------------------------------------------
- big-Phi  = stdlib iit4_bigphi.hexa (system Phi_s); faithful phi_EI = iit4/faithful_phi.hexa
  (MIP-EI scalar). EXACT n<=6, NEVER a proxy. CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5
  via the H_1012 prove_mirrors_at_n live-hexa-ref discipline BEFORE scoring.
- Williams-Beer (2010) I_min PID synergy atom reused VERBATIM from the H_1017 harness
  (h1017_split_redundancy_mechanism.py: pid_system -> syn_total), incl. its COPY/XOR
  canonical-case validation. The synergy code path has NO MIP cut enumeration (asserted).
- Substrate generators reused VERBATIM from H_1014 (planning_trajectories at multiple depths,
  chaos_trajectories at multiple gains, regimes_for_seed for imagination/guided).

The >=6 battery (each = intervention arm vs its matched baseline contrast, n=4):
  plan_d8   = planning depth-8 vs greedy      (known SPLIT inducer, deepest)
  plan_d4   = planning depth-4 vs greedy      (split inducer, shallower)
  plan_d2   = planning depth-2 vs greedy      (split inducer, shallowest)
  imagine   = drift vs react                  (known no-split control)
  guided    = guided vs react                 (known no-split control)
  chaos14   = high-gain 1.4 vs gain-1.0       (NEW intervention)
  chaos18   = high-gain 1.8 vs gain-1.0       (NEW intervention, stronger)

For each: contrast = intervention mean - baseline mean for big-Phi, synergy(syn_total),
faithful. Sign agreement scored per the pre-registered rule in H_1046_synergy_ruler.md.

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n<=6 — both engines exact;
big-Phi super-exponential so n=4 is the rung for the full battery x N_SEEDS. Mirror re-proven
== stdlib at n=4 AND n=5. PID exact + deterministic. Scale-transfer UNVERIFIED. g5 CODE-
measured (no LLM self-judge, p7). NOT a forge binary; $0 CPU-local, no GPU.
"""
import sys, os, math, time, itertools, inspect
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ── Reuse the H_1017 harness VERBATIM (it chains h1014 -> h1004 + h1012). It owns the
#    Williams-Beer I_min synergy atom (pid_system/syn_total) + substrate_reads + the
#    n=4 generators. We import it as a real module file and call its public functions. ──
import importlib.util as _ilu
_h1017_path = os.path.join(HERE, "h1017_split_redundancy_mechanism.py")
_spec = _ilu.spec_from_file_location("h1017", _h1017_path)
_h1017 = _ilu.module_from_spec(_spec)
_src = open(_h1017_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1017_path, "exec"), _h1017.__dict__)

# H_1017 public surface (Williams-Beer synergy lives here)
substrate_reads = _h1017.substrate_reads      # -> dict(big, faith, syn_total, red_total, ...)
pid_system = _h1017.pid_system                 # WB I_min PID -> syn_total (NO MIP search)
prove_mirrors_at_n = _h1017.prove_mirrors_at_n # H_1012 mirror == stdlib proof (n-param)
cohens_d = _h1017.cohens_d
welch_t = _h1017.welch_t
_pid_two_source = _h1017._pid_two_source
LATENT = _h1017.LATENT

# H_1014 parametric generators (via the H_1017 -> h1014 link)
_h1014 = _h1017._h1014
planning_trajectories = _h1014.planning_trajectories
chaos_trajectories = _h1014.chaos_trajectories
regimes_for_seed = _h1014.regimes_for_seed

N_SEEDS = 24   # >= 20 per pre-reg


def _react_drift_guided(seed):
    """regimes_for_seed -> (H_react, H_drift, H_guided)."""
    return regimes_for_seed(seed)


# ── the >=6 battery: each entry = (name, gen(seed)->(H_baseline, H_intervention), note) ──
def gen_plan_d8(s):  Hg, Hp = planning_trajectories(s, 8); return Hg, Hp
def gen_plan_d4(s):  Hg, Hp = planning_trajectories(s, 4); return Hg, Hp
def gen_plan_d2(s):  Hg, Hp = planning_trajectories(s, 2); return Hg, Hp
def gen_imagine(s):  Hr, Hd, Hgd = _react_drift_guided(s); return Hr, Hd
def gen_guided(s):   Hr, Hd, Hgd = _react_drift_guided(s); return Hr, Hgd
def gen_chaos14(s):  return chaos_trajectories(s, 1.4)
def gen_chaos18(s):  return chaos_trajectories(s, 1.8)

BATTERY = [
    ("plan_d8", gen_plan_d8, "planning depth-8 vs greedy (SPLIT inducer)"),
    ("plan_d4", gen_plan_d4, "planning depth-4 vs greedy (SPLIT inducer)"),
    ("plan_d2", gen_plan_d2, "planning depth-2 vs greedy (SPLIT inducer)"),
    ("imagine", gen_imagine, "drift vs react (no-split control)"),
    ("guided",  gen_guided,  "guided vs react (no-split control)"),
    ("chaos14", gen_chaos14, "high-gain 1.4 vs 1.0 (NEW)"),
    ("chaos18", gen_chaos18, "high-gain 1.8 vs 1.0 (NEW)"),
]


def sgn(x, eps=1e-3):
    return +1 if x > eps else (-1 if x < -eps else 0)


def _agg(rows):
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}


def _contrast(I, B, k):
    c = float(I[k].mean() - B[k].mean())
    try:
        d = float(cohens_d(I[k], B[k]))
    except Exception:
        d = float("nan")
    try:
        _, p = welch_t(I[k], B[k])
        p = float(p)
    except Exception:
        p = float("nan")
    return dict(contrast=c, d=d, p=p, base=float(B[k].mean()), intv=float(I[k].mean()))


def score(name, gen, t0):
    base_rows, intv_rows = [], []
    for s in range(N_SEEDS):
        Hb, Hi = gen(s)
        base_rows.append(substrate_reads(Hb))
        intv_rows.append(substrate_reads(Hi))
        print(f"    [{name} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    B = _agg(base_rows); I = _agg(intv_rows)
    return {k: _contrast(I, B, k) for k in ("big", "faith", "syn_total", "red_total")}


def synergy_has_no_mip_search():
    """Verify the synergy code path performs ZERO 2^(n-1) MIP bipartition enumeration —
    i.e. the WB I_min synergy atom is strictly cheaper than big-Phi's system MIP.
    We assert the synergy source (pid_system + _pid_two_source) contains no bipartition-
    mask loop, whereas big-Phi's _mi_min_cut_weight (H_1014) DOES (range(1, 2**(n-1)))."""
    syn_src = inspect.getsource(_h1017.pid_system) + inspect.getsource(_h1017._pid_two_source) \
            + inspect.getsource(_h1017._specific_info) + inspect.getsource(_h1017._mi_discrete)
    # tokens that mark a system-MIP bipartition enumeration:
    mip_markers = ["2 ** (n - 1)", "2**(n-1)", "max_mask", "best_cut", "for mask in range"]
    syn_has_mip = any(m in syn_src for m in mip_markers)
    # confirm big-Phi's faithful mincut path DOES enumerate cuts (positive control):
    try:
        cut_src = inspect.getsource(_h1014._mi_min_cut_weight)
        bigphi_has_mip = ("for mask in range" in cut_src) or ("best_cut" in cut_src)
    except Exception:
        bigphi_has_mip = None
    return (not syn_has_mip), syn_has_mip, bigphi_has_mip


def main():
    print("=" * 80)
    print("H_1046 — synergy-only ruler: is the WB synergy atom big-Phi's cheap integration signal?")
    print("substrate=CPU-mirror (numpy) — H_1004 engines + H_1012 proof, RE-PROVEN == stdlib n=4,5")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("synergy: Williams-Beer (2010) I_min Syn atom (REUSED from H_1017), NO MIP search")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print(f"BATTERY: {len(BATTERY)} substrates x N_SEEDS={N_SEEDS} (>=6 substrates, >=20 seeds)")
    print("PASS = sign(syn)==sign(big-Phi) >=5/6 AND on split substrates syn tracks big-Phi NOT")
    print("       faithful (strict majority) AND synergy needs NO MIP search (cheaper).")
    print("=" * 80)
    print()

    # ── STEP 0: RE-PROVE both CPU mirrors == stdlib at n=4 AND n=5 BEFORE scoring. ──
    print("EQUIVALENCE PROOF — re-prove BOTH mirrors == stdlib at n=4 AND n=5 (H_1012 discipline):")
    ok4 = prove_mirrors_at_n(4)
    ok5 = prove_mirrors_at_n(5)
    # WB synergy canonical-case validation (COPY=redundant, XOR=synergy) — reused logic.
    Tc = np.array([0, 1, 0, 1, 1, 0, 1, 0]); rc, _, _, sc_ = _pid_two_source(Tc, Tc, Tc)
    Xa = np.array([0, 0, 1, 1, 0, 0, 1, 1]); Xb = np.array([0, 1, 0, 1, 0, 1, 0, 1]); Xt = Xa ^ Xb
    rx, _, _, sx = _pid_two_source(Xt, Xa, Xb)
    copy_ok = (rc > 0.5 and abs(sc_) < 1e-6)
    xor_ok = (rx < 1e-6 and sx > 0.5)
    print(f"  WB synergy sanity: COPY(T;T,T) red={rc:.4f} syn={sc_:.4f} (expect syn~0) | "
          f"XOR(T;A,B) red={rx:.4f} syn={sx:.4f} (expect syn>0)  -> COPY={copy_ok} XOR={xor_ok}")
    # cheaper-than-big-Phi: synergy path has NO MIP bipartition enumeration.
    cheaper, syn_has_mip, bigphi_has_mip = synergy_has_no_mip_search()
    print(f"  CHEAPER check: synergy-path-has-MIP-enumeration={syn_has_mip} (expect False) | "
          f"big-Phi-mincut-has-MIP-enumeration={bigphi_has_mip} (expect True) -> synergy cheaper={cheaper}")
    proof_ok = ok4 and ok5 and copy_ok and xor_ok and cheaper
    print(f"  EQUIVALENCE(n=4 AND n=5) + WB-VALIDITY + CHEAPER PROOF: "
          f"{'PROVEN' if proof_ok else 'FAILED — DO NOT TRUST'}")
    if not proof_ok:
        raise SystemExit("equivalence/validity/cheaper proof failed — aborting")
    print()

    # ── STEP 1: score the battery. ──
    t0 = time.time()
    results = {}
    for name, gen, note in BATTERY:
        print(f"################ SCORE substrate = {name}  [{note}] ################")
        results[name] = score(name, gen, t0)
        r = results[name]
        print(f"  --- {name}: intervention vs baseline (matched n=4 binary discretization) ---")
        print(f"     big-Phi    contrast={r['big']['contrast']:+.4f} d={r['big']['d']:+.3f} p={r['big']['p']:.2e}")
        print(f"     synergy    contrast={r['syn_total']['contrast']:+.4f} d={r['syn_total']['d']:+.3f} p={r['syn_total']['p']:.2e}")
        print(f"     faithful   contrast={r['faith']['contrast']:+.4f} d={r['faith']['d']:+.3f} p={r['faith']['p']:.2e}")
        print()

    # ── STEP 2: the falsifier tables. ──
    print("=" * 80)
    print("SIGN MATRIX — big-Phi vs synergy vs faithful contrast SIGN per substrate")
    print("=" * 80)
    print(f"  {'substrate':10s} | {'big':>5s} | {'syn':>5s} | {'faith':>5s} | "
          f"{'syn==big':>8s} | {'split(big!=faith)':>17s} | {'syn tracks':>11s}")
    SW = {+1: "UP", -1: "DOWN", 0: "NULL"}
    agree_big = 0
    split_subs = []           # substrates where big-Phi and faithful disagree in sign
    syn_tracks_big_on_split = 0
    syn_tracks_faith_on_split = 0
    rows = {}
    for name, gen, note in BATTERY:
        r = results[name]
        sb = sgn(r["big"]["contrast"]); ss = sgn(r["syn_total"]["contrast"]); sf = sgn(r["faith"]["contrast"])
        syn_eq_big = (ss == sb and sb != 0)
        # also count a both-NULL as agreement (neither moves) only if big is NULL too:
        if sb == 0 and ss == 0:
            syn_eq_big = True
        is_split = (sb != sf and sb != 0 and sf != 0)
        tracks = "--"
        if is_split:
            split_subs.append(name)
            if ss == sb:
                syn_tracks_big_on_split += 1; tracks = "big-Phi"
            elif ss == sf:
                syn_tracks_faith_on_split += 1; tracks = "faithful"
            else:
                tracks = "neither"
        if syn_eq_big:
            agree_big += 1
        rows[name] = dict(sb=sb, ss=ss, sf=sf, syn_eq_big=syn_eq_big, is_split=is_split, tracks=tracks)
        print(f"  {name:10s} | {SW[sb]:>5s} | {SW[ss]:>5s} | {SW[sf]:>5s} | "
              f"{str(syn_eq_big):>8s} | {str(is_split):>17s} | {tracks:>11s}")
    print()

    n_subs = len(BATTERY)
    # pre-registered thresholds: agreement >=5/6 (scale to battery size: >= ceil(5/6 * n)).
    agree_threshold = math.ceil(5.0 / 6.0 * n_subs)
    print(f"AGREEMENT: sign(synergy)==sign(big-Phi) in {agree_big}/{n_subs} substrates "
          f"(pre-reg threshold >= {agree_threshold} == ceil(5/6 x {n_subs}))")
    agreement_pass = agree_big >= agree_threshold

    n_split = len(split_subs)
    print(f"SPLIT substrates (big-Phi sign != faithful sign): {n_split}  {split_subs}")
    print(f"  on split substrates: synergy tracks big-Phi in {syn_tracks_big_on_split}, "
          f"tracks faithful in {syn_tracks_faith_on_split}")
    # tracks-big-not-faithful: strict majority + strictly more than faithful, requires >=1 split.
    tracks_pass = (n_split >= 1 and
                   syn_tracks_big_on_split > syn_tracks_faith_on_split and
                   syn_tracks_big_on_split > n_split / 2.0)

    cheaper_pass = cheaper

    print()
    print("=" * 80)
    print(f"  (1) AGREEMENT  >=5/6           : {agreement_pass}  ({agree_big}/{n_subs} >= {agree_threshold})")
    print(f"  (2) TRACKS big-Phi NOT faithful: {tracks_pass}  (split={n_split}, "
          f"big={syn_tracks_big_on_split} > faith={syn_tracks_faith_on_split})")
    print(f"  (3) CHEAPER (no MIP search)    : {cheaper_pass}")
    overall = agreement_pass and tracks_pass and cheaper_pass
    if overall:
        print("OVERALL: SYNERGY-IS-BIGPHI-CHEAP-STANDIN — the Williams-Beer synergy atom AGREES with")
        print("  big-Phi's direction (>=5/6) AND, where big-Phi and faithful phi_EI split, the synergy")
        print("  sign TRACKS big-Phi NOT faithful, AND it needs NO MIP bipartition search. The synergy")
        print("  atom IS big-Phi's hidden 'genuine integration' driver and a valid CHEAP stand-in.")
        print("  VERDICT-TOKEN: SYNERGY-IS-BIGPHI-CHEAP-STANDIN")
    else:
        print("OVERALL: SYNERGY-NOT-BIGPHI-STANDIN (CLOSED-NEGATIVE) — the synergy sign does NOT track")
        print("  big-Phi well enough to stand in for it (agreement and/or split-tracking failed). The")
        print("  synergy-only-ruler axis is RULED OUT as a cheap big-Phi integration stand-in")
        print("  (a_paper_negative_ok).")
        print("  VERDICT-TOKEN: SYNERGY-NOT-BIGPHI-STANDIN")
    print("=" * 80)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n<=6 — both engines EXACT;")
    print("big-Phi super-exponential so n=4 is the rung for the full battery x N_SEEDS. Both CPU mirrors")
    print("RE-PROVEN == stdlib at n=4 AND n=5 (H_1012 prove_mirrors_at_n) BEFORE scoring; the WB synergy")
    print("is exact + deterministic on the SAME bits and validated on COPY(redundant)/XOR(synergy).")
    print("Synergy is NOT a proxy for Phi. Scale-transfer UNVERIFIED. g5 CODE-measured (p7),")
    print("a_phi_iit4_tool. NOT a forge binary; $0 CPU-local, no GPU.")


if __name__ == "__main__":
    main()
