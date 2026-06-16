"""H_1023 — is the redundancy-driven faithful-UP / big-Phi-DOWN split SUBSTRATE-GENERAL?

MISSION
-------
H_1012/H_1014/H_1017/H_1020 established, on ONE substrate (the planning-control
LatentWorldModel rollout env), that a redundancy-raising intervention reproduces the
faithful_phi-UP / big-Phi-DOWN sign-split, and that the Williams-Beer I_min redundancy
margin (Δred − Δsyn) separates the split-inducing intervention from non-split controls.
EVERY one of those was measured on the SAME planning-control task. H_1023 (pre-registered,
frozen 2026-06-07) asks the cross-substrate question the prior arc could not answer: does
the split + redundancy-margin reproduce on a DIFFERENT generative substrate — one with no
LatentWorldModel, no planning rollout — or is the finding TASK-LOCAL?

THE NEW SUBSTRATE (pre-frozen — NOT the planning-control env)
------------------------------------------------------------
A small structured TPM-DRIVEN Markov substrate over n=4 binary units. There is no
LatentWorldModel and no learned-transition rollout anywhere in this file; the bits are
generated directly from explicit, frozen channel rules. This is the generative substrate
distinct from the planning-control toy required by the H_1023 falsifier.

  base step  : each of the 4 units flips toward a noisy fair coin (independent units,
               low shared structure) — the matched baseline for BOTH interventions.

  REDUNDANCY-RAISING intervention (coupled-copy channel, frozen):
               a driver unit d_t is drawn; units 1,2,3 become NOISY COPIES of unit 0
               (shared / redundant information flooded across the system). This is the
               cross-substrate analogue of planning's redundant-MI injection. Sources
               carry the SAME information about a target -> high WB I_min redundancy,
               LOW synergy.

  SYNERGY-RAISING control (XOR / parity-mixing channel, frozen):
               each unit's next bit = the PARITY (XOR) of the OTHER three units' current
               bits (+ a little noise). Each pair of sources carries NO information about
               the target alone; only the JOINT state does -> LOW redundancy, HIGH synergy
               (the canonical XOR PID structure, here embedded in an n=4 dynamical system).

Both interventions share the identical base-noise generator and seed schedule; only the
channel rule differs. The interventions are matched-baseline contrasts exactly like the
prior arc (intervention arm vs its own base arm), so the contrast isolates the channel.

WHAT IS REUSED VERBATIM (no reinvention)
----------------------------------------
- The two stdlib IIT-4.0 engine CPU mirrors (big_phi + faithful_phi) and the matched
  binary discretization reads — IMPORTED from h1014/h1004 via the H_1017 import chain.
- prove_mirrors_at_n (H_1012) — re-proves BOTH mirrors == stdlib at n=4 (and n=5) on
  ring/fixed-trace refs BEFORE scoring. This proof is substrate-independent.
- The Williams-Beer (2010) I_min PID (pid_system, _pid_two_source) — IMPORTED VERBATIM
  from H_1017, validated on canonical COPY=pure-redundancy / XOR=pure-synergy.
The PID is the EXPLANATORY variable, NOT a Phi proxy (a_phi_iit4_tool — Phi numbers come
only from the stdlib engine mirrors).

FALSIFIER (frozen in H_1023_phi_split_substrate_generality.md, 2026-06-07)
-------------------------------------------------------------------------
PASS = SPLIT-SUBSTRATE-GENERAL : on this NEW substrate the REDUNDANCY-RAISING intervention
  reproduces faithful-UP / big-Phi-DOWN (the sign-split) AND its redundancy-margin
  (Δred − Δsyn) is positive AND strictly exceeds the SYNERGY-raising control's margin.
FAIL = SPLIT-TASK-LOCAL : the split does NOT reproduce off the planning substrate
  (closed-negative, a_paper_negative_ok) — bounds the paper to the control task.

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 (n=5 cross-check) —
both engines EXACT; big-Phi super-exponential so n=4 is the rung for the full SET x 30
seeds. PID exact + deterministic. Scale-transfer UNVERIFIED. NOT a forge binary; $0
CPU-local, no GPU.
"""
import sys, os, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ── Import the H_1017 module VERBATIM: it carries the H_1004 engine mirrors, the
#    matched-discretization substrate_reads, the H_1012 prove_mirrors_at_n proof,
#    AND the validated Williams-Beer I_min PID (pid_system / _pid_two_source). ──
import importlib.util as _ilu
_h1017_path = os.path.join(HERE, "h1017_split_redundancy_mechanism.py")
_spec = _ilu.spec_from_file_location("h1017", _h1017_path)
_h1017 = _ilu.module_from_spec(_spec)
_src = open(_h1017_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1017_path, "exec"), _h1017.__dict__)

prove_mirrors_at_n = _h1017.prove_mirrors_at_n
big_phi = _h1017.big_phi
faithful_phi = _h1017.faithful_phi
build_mi_matrix = _h1017.build_mi_matrix
faithful_phi_from_mi = _h1017.faithful_phi_from_mi
binary_seq_to_tpm = _h1017.binary_seq_to_tpm
modal_state = _h1017.modal_state
binary_seq_to_faithful_state = _h1017.binary_seq_to_faithful_state
pid_system = _h1017.pid_system
_pid_two_source = _h1017._pid_two_source
cohens_d = _h1017.cohens_d
welch_t = _h1017.welch_t

N_UNITS = 4
N_STEPS = 200          # rollout length of the Markov substrate (per seed)
N_SEEDS = 30           # match H_1017's 30 seeds
NOISE = 0.10           # bit-flip noise on the channel rules (keeps TPM non-degenerate)

# ═══════════════════════════════════════════════════════════════════════════
# THE NEW SUBSTRATE — a structured TPM-driven n=4 binary Markov chain. NO
# LatentWorldModel, NO planning rollout. bits are produced DIRECTLY from frozen
# channel rules, then handed to the SAME matched-discretization engine reads.
# ═══════════════════════════════════════════════════════════════════════════
def _noise_flip(rng, bit):
    """flip `bit` with prob NOISE (channel noise)."""
    return int(bit ^ (rng.random() < NOISE))

def run_base(seed, n_steps=N_STEPS):
    """Matched BASELINE substrate: 4 (near-)independent noisy binary units. Each unit
    relaxes toward an independent fair coin -> low shared structure. Frozen."""
    rng = np.random.default_rng(50_000 + seed)
    bits = np.zeros((n_steps, N_UNITS), dtype=int)
    bits[0] = (rng.random(N_UNITS) > 0.5).astype(int)
    for t in range(1, n_steps):
        coin = (rng.random(N_UNITS) > 0.5).astype(int)
        for u in range(N_UNITS):
            bits[t, u] = _noise_flip(rng, coin[u])
    return bits

def run_redundancy(seed, n_steps=N_STEPS):
    """REDUNDANCY-RAISING intervention (coupled-copy channel, frozen): a driver bit is
    drawn each step; units 1,2,3 are NOISY COPIES of unit 0 (shared info flooded across
    the system). High WB I_min redundancy, low synergy. SAME base-noise seed schedule."""
    rng = np.random.default_rng(50_000 + seed)   # SAME seed base as run_base -> matched
    bits = np.zeros((n_steps, N_UNITS), dtype=int)
    bits[0] = (rng.random(N_UNITS) > 0.5).astype(int)
    for t in range(1, n_steps):
        driver = int(rng.random() > 0.5)          # the shared source value
        bits[t, 0] = _noise_flip(rng, driver)
        for u in (1, 2, 3):
            bits[t, u] = _noise_flip(rng, bits[t, 0])   # noisy COPY of unit 0
    return bits

def run_synergy(seed, n_steps=N_STEPS):
    """SYNERGY-RAISING control (XOR / parity-mixing channel, frozen): each unit's next
    bit = PARITY (XOR) of the OTHER three units' current bits (+ noise). Pairwise sources
    carry no info about a target alone; only the joint state does. Low redundancy, high
    synergy (canonical XOR PID, embedded in an n=4 dynamical system). SAME seed schedule."""
    rng = np.random.default_rng(50_000 + seed)   # SAME seed base as run_base -> matched
    bits = np.zeros((n_steps, N_UNITS), dtype=int)
    bits[0] = (rng.random(N_UNITS) > 0.5).astype(int)
    for t in range(1, n_steps):
        prev = bits[t - 1]
        for u in range(N_UNITS):
            parity = int(prev[(u + 1) % 4] ^ prev[(u + 2) % 4] ^ prev[(u + 3) % 4])
            bits[t, u] = _noise_flip(rng, parity)
    return bits

# ═══════════════════════════════════════════════════════════════════════════
# Engine + PID reads on the SAME bits (the H_1017 substrate_reads, re-expressed
# to take bits directly — this substrate emits bits, it has no continuous latent).
# ═══════════════════════════════════════════════════════════════════════════
def reads_from_bits(bits):
    n = N_UNITS
    tpm, sc = binary_seq_to_tpm(bits, n)
    s = modal_state(sc)
    bphi = big_phi(tpm, n, s)[0]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    mi = build_mi_matrix(fstate, fn, fdim, 2)
    fphi = faithful_phi_from_mi(mi, fn)
    mi_total = float(np.triu(mi, 1).sum())
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
    """gen(seed) -> bits (intervention arm). Baseline = run_base(seed). Matched contrast."""
    base_rows, intv_rows = [], []
    for s in range(N_SEEDS):
        base_rows.append(reads_from_bits(run_base(s)))
        intv_rows.append(reads_from_bits(gen(s)))
        print(f"    [{name} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    B = _agg(base_rows); I = _agg(intv_rows)
    return {k: _contrast(I, B, k) for k in
            ("big", "faith", "mi_total", "red_total", "syn_total", "unq_total", "syn_raw")}

def sgn(x, eps=1e-3):
    return +1 if x > eps else (-1 if x < -eps else 0)

def signword(x, eps=1e-3):
    return "RAISES" if x > eps else ("LOWERS" if x < -eps else "NULL")

def main():
    print("=" * 80)
    print("H_1023 — is the redundancy-driven faithful-UP / big-Phi-DOWN split SUBSTRATE-GENERAL?")
    print("NEW SUBSTRATE = structured TPM-driven n=4 binary Markov chain (NO LatentWorldModel,")
    print("  NO planning rollout) — DISTINCT from the H_1012..H_1020 planning-control task.")
    print("substrate-engine reads=CPU-mirror (numpy) — H_1004 engines + H_1012 proof,")
    print("  RE-PROVEN == stdlib at n=4 (and n=5 cross-check) BEFORE scoring.")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("PID = Williams-Beer (2010) I_min redundancy lattice, IMPORTED VERBATIM from H_1017")
    print("  (the EXPLANATORY variable — NOT a Phi proxy/replacement; Phi from stdlib mirrors only)")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print("interventions (frozen): REDUNDANCY-raising coupled-copy channel vs SYNERGY-raising")
    print("  XOR/parity channel, each vs the SAME independent-noisy-bits baseline.")
    print("PASS = SPLIT-SUBSTRATE-GENERAL: redundancy intervention reproduces faithful-UP/")
    print("  big-Phi-DOWN AND its redundancy-margin (Δred−Δsyn) > 0 AND > the synergy control's.")
    print("FAIL = SPLIT-TASK-LOCAL: the split does NOT reproduce off the planning substrate.")
    print("=" * 80)
    print()

    # ── STEP 0 — equivalence proof BEFORE scoring (H_1012 discipline), n=4 + n=5. ──
    print("EQUIVALENCE PROOF (H_1012 prove_mirrors_at_n — re-prove BOTH mirrors vs stdlib):")
    ok = prove_mirrors_at_n(4)
    ok5 = prove_mirrors_at_n(5)
    ok = ok and ok5

    # PID determinism + non-negativity on a fixed sample of THIS substrate's bits.
    b_fixed = run_redundancy(0)
    r1 = reads_from_bits(b_fixed); r2 = reads_from_bits(b_fixed)
    pid_det = (abs(r1["red_total"] - r2["red_total"]) < 1e-12 and
               abs(r1["syn_total"] - r2["syn_total"]) < 1e-12)
    pid_nonneg = (r1["red_total"] >= -1e-9 and r1["syn_total"] >= -1e-9)
    eng_det = (abs(r1["big"] - r2["big"]) < 1e-12 and abs(r1["faith"] - r2["faith"]) < 1e-12)
    print(f"  substrate PID/engine deterministic re-run: pid={pid_det} engine={eng_det}   "
          f"red_total={r1['red_total']:.6f} syn_total={r1['syn_total']:.6f} nonneg={pid_nonneg}")

    # WB sanity (canonical COPY=redundancy / XOR=synergy) — re-validated this run.
    Tc = np.array([0,1,0,1,1,0,1,0]); rc, _, _, sc_ = _pid_two_source(Tc, Tc, Tc)
    Xa = np.array([0,0,1,1,0,0,1,1]); Xb = np.array([0,1,0,1,0,1,0,1]); Xt = Xa ^ Xb
    rx, _, _, sx = _pid_two_source(Xt, Xa, Xb)
    copy_ok = (rc > 0.5 and abs(sc_) < 1e-6)
    xor_ok = (rx < 1e-6 and sx > 0.5)
    print(f"  WB sanity: COPY(T;T,T) red={rc:.4f} syn={sc_:.4f} | XOR(T;A,B) red={rx:.4f} syn={sx:.4f}")
    print(f"  WB canonical-case check: COPY={copy_ok} XOR={xor_ok}")
    ok = ok and pid_det and eng_det and pid_nonneg and copy_ok and xor_ok
    print(f"  EQUIVALENCE + PID-VALIDITY PROOF: {'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
    if not ok:
        raise SystemExit("equivalence/PID proof failed — aborting")
    print()

    SET = [
        ("redundancy", run_redundancy, "REDUNDANCY-raising coupled-copy channel (frozen)"),
        ("synergy",    run_synergy,    "SYNERGY-raising XOR/parity channel (frozen, control)"),
    ]
    t0 = time.time()
    results = {}
    for name, gen, note in SET:
        print(f"################ SCORE intervention = {name}  [{note}] ################")
        r = score(name, gen, t0)
        results[name] = r
        split = sgn(r["faith"]["contrast"]) != sgn(r["big"]["contrast"])
        dred = r["red_total"]["contrast"]; dsyn = r["syn_total"]["contrast"]
        bs = signword(r["big"]["contrast"]); fs = signword(r["faith"]["contrast"])
        print(f"  --- {name}: intervention vs independent-bits baseline (matched n=4) ---")
        print(f"     big-Phi      contrast={r['big']['contrast']:+.4f} d={r['big']['d']:+.3f} p={r['big']['p']:.3e} -> {bs}")
        print(f"     faithful_phi contrast={r['faith']['contrast']:+.4f} d={r['faith']['d']:+.3f} p={r['faith']['p']:.3e} -> {fs}")
        print(f"     SPLIT label (sign(faith)!=sign(big)): {split}")
        print(f"     Δredundancy  contrast={dred:+.4f} d={r['red_total']['d']:+.3f} p={r['red_total']['p']:.3e}")
        print(f"     Δsynergy     contrast={dsyn:+.4f} d={r['syn_total']['d']:+.3f} p={r['syn_total']['p']:.3e}")
        print(f"     redundancy-margin Δred−Δsyn = {dred - dsyn:+.4f}")
        print(f"     (cross-check) Δmi_total={r['mi_total']['contrast']:+.4f} | Δunique={r['unq_total']['contrast']:+.4f}")
        print()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER TEST
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("SUBSTRATE-GENERALITY MATRIX — per intervention on the NEW (Markov) substrate")
    print("=" * 80)
    print(f"  {'intervention':12s} | {'big sign':>8s} | {'faith sign':>10s} | {'SPLIT?':>6s} | "
          f"{'Δredund':>9s} | {'Δsynergy':>9s} | {'margin':>8s}")
    rows = {}
    for name, gen, note in SET:
        r = results[name]
        split = sgn(r["faith"]["contrast"]) != sgn(r["big"]["contrast"])
        dred = r["red_total"]["contrast"]; dsyn = r["syn_total"]["contrast"]
        margin = dred - dsyn
        rows[name] = dict(split=split, dred=dred, dsyn=dsyn, margin=margin,
                          big_c=r["big"]["contrast"], faith_c=r["faith"]["contrast"])
        print(f"  {name:12s} | {signword(r['big']['contrast']):>8s} | {signword(r['faith']['contrast']):>10s} | "
              f"{str(split):>6s} | {dred:+9.4f} | {dsyn:+9.4f} | {margin:+8.4f}")
    print()

    red = rows["redundancy"]; syn = rows["synergy"]

    # PASS conditions (frozen):
    #  (1) the redundancy intervention reproduces the split with the CORRECT signs:
    #      faithful_phi UP (>0) AND big-Phi DOWN (<0);
    #  (2) its redundancy-margin (Δred−Δsyn) > 0;
    #  (3) its redundancy-margin strictly EXCEEDS the synergy control's margin.
    correct_split = (sgn(red["faith_c"]) > 0) and (sgn(red["big_c"]) < 0)
    margin_pos = red["margin"] > 0.0
    separates = red["margin"] > syn["margin"]
    print("Redundancy intervention (the cross-substrate split-inducer):")
    print(f"  faithful_phi sign = {signword(red['faith_c'])} (need RAISES) | "
          f"big-Phi sign = {signword(red['big_c'])} (need LOWERS) -> correct split signs: {correct_split}")
    print(f"  redundancy-margin Δred−Δsyn = {red['margin']:+.4f} (need >0): {margin_pos}")
    print(f"  vs SYNERGY control margin = {syn['margin']:+.4f} -> redundancy margin strictly "
          f"exceeds synergy control: {separates}")
    print()

    substrate_general = correct_split and margin_pos and separates
    print("=" * 80)
    if substrate_general:
        print("OVERALL: 🟢 SPLIT-SUBSTRATE-GENERAL — on a NEW generative substrate (a structured")
        print("  TPM-driven Markov chain, NOT the planning-control task), a redundancy-raising")
        print("  intervention REPRODUCES the faithful_phi-UP / big-Phi-DOWN sign-split, its WB")
        print("  I_min redundancy-margin (Δred−Δsyn) is positive, AND that margin strictly")
        print("  separates it from the synergy-raising XOR control. The H_1012..H_1020 finding")
        print("  is a property of the TWO Phi MEASURES (the pairwise-MI scalar rewards redundant")
        print("  shared info that big-Phi discounts as reducible), NOT of the planning task.")
        print("  VERDICT-TOKEN: SPLIT-SUBSTRATE-GENERAL")
    else:
        print("OVERALL: 🔴 SPLIT-TASK-LOCAL (CLOSED-NEGATIVE) — on the NEW generative substrate the")
        print("  redundancy-raising intervention does NOT reproduce the split with a redundancy-")
        print("  margin that separates it from the synergy control. The faithful-UP / big-Phi-DOWN")
        print("  split + redundancy-margin mechanism is BOUNDED to the planning-control task")
        print("  (a_paper_negative_ok); the cross-substrate generalization is RULED OUT.")
        print("  VERDICT-TOKEN: SPLIT-TASK-LOCAL")
    print("=" * 80)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 — both engines")
    print("EXACT; big-Phi super-exponential so n=4 is the rung for the full SET x 30 seeds.")
    print("Both CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5 (H_1012 prove_mirrors_at_n)")
    print("BEFORE scoring; the PID is exact + deterministic on the SAME bits and validated on")
    print("canonical COPY(redundant)/XOR(synergy). The PID is NOT a proxy for Phi. The new")
    print("substrate has NO LatentWorldModel / NO planning rollout. Scale-transfer UNVERIFIED.")
    print("g5 CODE-measured (no LLM self-judge, p7), a_phi_iit4_tool. NOT a forge binary; $0 CPU-local.")

if __name__ == "__main__":
    main()
