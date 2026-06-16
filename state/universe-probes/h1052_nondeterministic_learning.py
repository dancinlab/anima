"""H_1052 — Does NON-DETERMINISTIC LEARNING help consciousness / emergence / CE?

Tests the UNTESTED axis: non-determinism IN THE LEARNING DYNAMICS ITSELF (SGLD Langevin
weight-update noise during training), NOT init noise (H_921 prior RED), NOT inference-time
temperature/entropy (free-will arc null). Question: at MATCHED final task-performance (CE
within eps), does a model trained with non-deterministic update dynamics develop HIGHER
consciousness/emergence/CE markers than a matched DETERMINISTIC-learning control?

substrate = SW (numpy CPU toy). Lane tag for this rung: SW-only.
- SW (this rung): a small gradient-trained Elman RNN, manual numpy BPTT, $0 CPU.
- AKIDA Lane A on-chip + GPU Lane G: separate substrate rungs, NOT run here (follow-up).

ENGINES — the H_1004 CPU mirrors of stdlib IIT-4.0 (a_phi_iit4_tool, no proxy):
  big-Phi      <- hexa-lang/stdlib/consciousness/iit4_bigphi.hexa  (system Phi_s, EXACT)
  faithful_phi <- hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar, EXACT)
RE-PROVEN == stdlib at n=4 AND n=5 (H_1012 prove_mirrors_at_n discipline) BEFORE scoring.
Imported by REAL MODULE NAME so the SERIAL path stays clean (no importlib custom-name).

CONTROL: identical arch + task + INIT (pinned per seed) for both regimes; the ONLY difference
is the update rule (DET full-batch GD vs NOISY SGLD). Matched to equal final CE within eps; any
marker difference at matched CE is attributable to the learning non-determinism (p7).

PASS = at matched CE, >=1 pre-named marker strictly higher (favorable direction) under noisy
learning with paired Cohen d >= 0.8. FAIL = no marker benefits (consistent with H_921 + the
entropy null; a_paper_negative_ok). DEGENERATE = <10 seed-pairs in the matched-CE band.

HONEST scope (a_scale_honest_scope): TOY n<=5 SW. g5 CODE-measured (no LLM self-judge, p7).
NOT a forge binary; $0 CPU-local.
"""
import sys, os, math, time, json, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Import the H_1004 IIT-4.0 engines + H_1012 per-n mirror proof by REAL module names
# (serial path; no forked Pool, so no PicklingError concern).
import h1004_bigphi_faithful_clean as h1004      # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012   # noqa: E402

big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
prove_mirrors_at_n = h1012.prove_mirrors_at_n


def cohens_d_paired(diffs):
    """Cohen d for a paired sample = mean(diff)/std(diff) (ddof=1). diffs already paired."""
    d = np.asarray(diffs, float)
    if len(d) < 2:
        return float("nan")
    sd = d.std(ddof=1)
    if sd == 0:
        return 0.0 if d.mean() == 0 else float(np.sign(d.mean()) * 50.0)
    return float(d.mean() / sd)


# ============================================================================
# TOY TASK — a deterministic finite-state symbol source (Markov-ish memory task).
# A small finite automaton emits symbols; the RNN must predict the next symbol.
# Memory is required (the next symbol depends on a hidden phase that the RNN must
# carry in its recurrent state) so the hidden state develops non-trivial structure.
# ============================================================================
N_SYM = 4          # vocabulary size
SEQ_LEN = 60       # training sequence length
HID = 8            # hidden units (>= the n<=5 we read out for Phi; we read top-variance)


def make_source(seed):
    """A fixed deterministic finite-state source: a cyclic-phase automaton with a
    data-dependent branch. State = (phase in 0..P-1). next_symbol = f(phase, last_symbol);
    phase advances deterministically. Memory of phase is required to predict. Deterministic
    given the seed -> the SAME source string is used for BOTH regimes of a seed-pair."""
    rng = np.random.default_rng(10_000 + seed)
    P = 5
    # emission table sym(phase) and a branch that flips phase advance based on last symbol
    emit = rng.integers(0, N_SYM, size=P)
    branch = rng.integers(0, 2, size=(P, N_SYM))  # whether to +2 vs +1 the phase

    def gen(n):
        phase = 0
        last = 0
        syms = []
        for _ in range(n):
            s = int(emit[phase])
            syms.append(s)
            adv = 2 if branch[phase, last] else 1
            phase = (phase + adv) % P
            last = s
        return np.array(syms, dtype=int)

    return gen


# ============================================================================
# RNN — Elman tanh cell with softmax readout, manual BPTT. Pure numpy.
# h_t = tanh(W_xh x_t + W_hh h_{t-1} + b_h);  logits = W_hy h_t + b_y.
# x_t = one-hot(symbol_{t}); target = symbol_{t+1}.
# ============================================================================
class RNN:
    def __init__(self, seed):
        rng = np.random.default_rng(seed)   # pinned init: SAME seed -> SAME init for both regimes
        s = 1.0 / math.sqrt(HID)
        self.Wxh = rng.standard_normal((HID, N_SYM)) * s
        self.Whh = rng.standard_normal((HID, HID)) * s
        self.bh = np.zeros(HID)
        self.Why = rng.standard_normal((N_SYM, HID)) * s
        self.by = np.zeros(N_SYM)

    def params(self):
        return [self.Wxh, self.Whh, self.bh, self.Why, self.by]

    def forward(self, syms):
        """Run over a symbol string; return hidden trace H (T,HID), logits (T,N_SYM), cache."""
        T = len(syms)
        H = np.zeros((T, HID))
        logits = np.zeros((T, N_SYM))
        h = np.zeros(HID)
        xs = []
        for t in range(T):
            x = np.zeros(N_SYM); x[syms[t]] = 1.0
            xs.append(x)
            h = np.tanh(self.Wxh @ x + self.Whh @ h + self.bh)
            H[t] = h
            logits[t] = self.Why @ h + self.by
        return H, logits, xs

    def loss_and_grad(self, syms):
        """Cross-entropy of predicting symbol_{t+1} from state at t. Returns (CE, grads)."""
        T = len(syms)
        H, logits, xs = self.forward(syms)
        # targets = next symbol; last step has no target -> use T-1 predictions
        grads = [np.zeros_like(p) for p in self.params()]
        gWxh, gWhh, gbh, gWhy, gby = grads
        dh_next = np.zeros(HID)
        ce = 0.0
        ncount = 0
        # precompute softmax probs
        for t in range(T - 1, -1, -1):
            if t < T - 1:
                z = logits[t] - logits[t].max()
                p = np.exp(z); p /= p.sum()
                tgt = syms[t + 1]
                ce += -math.log(p[tgt] + 1e-12)
                ncount += 1
                dy = p.copy(); dy[tgt] -= 1.0
                gWhy += np.outer(dy, H[t])
                gby += dy
                dh = self.Why.T @ dy + dh_next
            else:
                dh = dh_next
            # backprop through tanh
            dtanh = (1.0 - H[t] ** 2) * dh
            gbh += dtanh
            gWxh += np.outer(dtanh, xs[t])
            h_prev = H[t - 1] if t > 0 else np.zeros(HID)
            gWhh += np.outer(dtanh, h_prev)
            dh_next = self.Whh.T @ dtanh
        ce /= max(ncount, 1)
        for g in grads:
            g /= max(ncount, 1)
        return ce, grads

    def apply_update(self, grads, lr, noise_T, rng):
        """SGLD update: w <- w - lr*grad + sqrt(2*lr*T)*xi.  noise_T=0 -> deterministic GD."""
        for p, g in zip(self.params(), grads):
            p -= lr * g
            if noise_T > 0.0:
                p += math.sqrt(2.0 * lr * noise_T) * rng.standard_normal(p.shape)

    def test_ce(self, syms):
        _, logits, _ = self.forward(syms)
        T = len(syms)
        ce = 0.0; nc = 0
        for t in range(T - 1):
            z = logits[t] - logits[t].max()
            p = np.exp(z); p /= p.sum()
            ce += -math.log(p[syms[t + 1]] + 1e-12); nc += 1
        return ce / max(nc, 1)


# ============================================================================
# TRAINING — DET (noise_T=0) and NOISY (annealed SGLD). Identical init + data.
# ============================================================================
N_STEPS = 1500
LR = 0.08
T0 = 5e-3          # initial SGLD temperature (annealed to ~0 so the chain settles to a mode)


def train(seed, regime, train_syms):
    """Train an RNN (pinned init via seed) on train_syms with the given regime.
    regime in {'det','noisy'}. Returns (model, train_CE)."""
    model = RNN(seed)
    noise_rng = np.random.default_rng(50_000 + seed + (0 if regime == "det" else 777))
    for step in range(N_STEPS):
        ce, grads = model.loss_and_grad(train_syms)
        if regime == "noisy":
            # anneal T -> 0 over training so the Langevin chain settles to a low-CE mode
            frac = 1.0 - step / N_STEPS
            noise_T = T0 * (frac ** 2)
        else:
            noise_T = 0.0
        model.apply_update(grads, LR, noise_T, noise_rng)
    return model, model.test_ce(train_syms)


# ============================================================================
# MARKERS — discretize the trained hidden trace to n<=5 binary units, feed BOTH
# IIT-4.0 engines (H_1004 path VERBATIM), plus PID redundancy + SOC + emergence.
# ============================================================================
N_UNITS = 5        # exact big-Phi computable at n=5


def hidden_trace(model, syms):
    H, _, _ = model.forward(syms)
    return H


def latent_to_bits(H, n_units=N_UNITS):
    """Top-variance hidden channels binarized at own median (H_1004 path)."""
    H = np.asarray(H, float)
    var = H.var(axis=0)
    idx = np.sort(np.argsort(var)[::-1][:n_units])
    chans = H[:, idx]
    med = np.median(chans, axis=0)
    bits = (chans > med).astype(int)
    return bits


def both_phi(H, n_units=N_UNITS):
    bits = latent_to_bits(H, n_units)
    tpm, sc = binary_seq_to_tpm(bits, n_units)
    bphi = big_phi(tpm, n_units, modal_state(sc))[0]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n_units)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    return bphi, fphi, bits


def _mi_binary(a, b):
    """MI of two binary vectors (nats)."""
    n = len(a)
    mi = 0.0
    for av in (0, 1):
        for bv in (0, 1):
            pab = np.mean((a == av) & (b == bv))
            pa = np.mean(a == av); pb = np.mean(b == bv)
            if pab > 0 and pa > 0 and pb > 0:
                mi += pab * math.log(pab / (pa * pb))
    return max(mi, 0.0)


def redundancy_margin(bits):
    """Williams-Beer PID redundancy I_min between two source units about a target unit
    (H_1017/H_1020 redundancy marker). Target = the lowest-index unit; sources = the two
    highest-MI source units about it. I_min = min over sources of the specific information,
    approximated here by the Williams-Beer redundancy = min of the two pairwise MIs that
    each source shares with the target (the WB redundancy lattice bottom for 2 sources)."""
    n = bits.shape[1]
    if n < 3:
        return 0.0
    tgt = bits[:, 0]
    mis = [(_mi_binary(bits[:, j], tgt), j) for j in range(1, n)]
    mis.sort(reverse=True)
    s1, s2 = mis[0][1], mis[1][1]
    mi1 = _mi_binary(bits[:, s1], tgt)
    mi2 = _mi_binary(bits[:, s2], tgt)
    # Williams-Beer I_min redundancy (2 sources, binary target): min specific-information.
    # For binary target the specific information reduces, at the lattice bottom, to min(MI).
    return float(min(mi1, mi2))


def soc_proximity(model):
    """SOC / edge-of-chaos proximity (H_931): |spectral_radius(Whh) - 1|. Smaller=closer to
    criticality. Uses the recurrent Jacobian magnitude at the typical operating point; for a
    tanh RNN the Jacobian is diag(1-h^2) @ Whh, but at the criticality reference (small h) it
    reduces to Whh, so we report the Whh spectral radius distance to 1 (the standard ESP /
    edge-of-chaos criterion)."""
    rho = float(np.max(np.abs(np.linalg.eigvals(model.Whh))))
    return abs(rho - 1.0), rho


def run_pair(seed, train_syms, test_syms):
    """Train DET and NOISY from the SAME pinned init on the SAME data; measure all markers."""
    out = {}
    for regime in ("det", "noisy"):
        model, train_ce = train(seed, regime, train_syms)
        H = hidden_trace(model, train_syms)
        bphi, fphi, bits = both_phi(H)
        red = redundancy_margin(bits)
        soc_abs, rho = soc_proximity(model)
        test_ce = model.test_ce(test_syms)
        out[regime] = dict(train_ce=float(train_ce), test_ce=float(test_ce),
                           big_phi=float(bphi), faithful_phi=float(fphi),
                           split=float(fphi - bphi), redundancy=float(red),
                           soc_abs=float(soc_abs), rho=float(rho))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=24)
    ap.add_argument("--eps", type=float, default=0.05)
    ap.add_argument("--out", type=str,
                    default=os.path.join(HERE, "h1052_nondeterministic_learning_result.json"))
    args = ap.parse_args()

    print("=" * 90)
    print("H_1052 — Does NON-DETERMINISTIC LEARNING (SGLD update noise) help consciousness/CE?")
    print("substrate=SW (numpy CPU toy) — gradient-trained Elman RNN, manual BPTT, $0 CPU")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s, EXACT n<=5)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI, EXACT)")
    print("CONTROL: identical arch+task+INIT; ONLY the update rule differs (DET vs NOISY SGLD).")
    print("Matched to equal final CE within eps; marker diff at matched CE = the learning-noise effect (p7).")
    print(f"seeds={args.seeds}  matched-CE band eps={args.eps} nats  markers: faithful_phi, big_Phi,")
    print("  split(faithful-big), redundancy(WB PID), soc(|rho-1|), emergence(test-CE gap).")
    print("PASS = >=1 marker higher (favorable dir) under noisy at matched CE, paired Cohen d>=0.8.")
    print("FAIL = none (consistent with H_921 init-null + entropy-null; a_paper_negative_ok).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope: TOY n<=5 SW")
    print("=" * 90, flush=True)
    print()

    # STEP 0 — RE-PROVE both CPU mirrors == stdlib at n=4 AND n=5 BEFORE scoring.
    print("STEP 0 — RE-PROVE BOTH CPU mirrors == stdlib (a_phi_iit4_tool) at n=4 AND n=5")
    print("         (H_1012 prove_mirrors_at_n discipline; LIVE stdlib refs) BEFORE scoring:")
    proven = {}
    for n in (4, 5):
        proven[n] = prove_mirrors_at_n(n)
        print()
    print(f"  == mirror-equivalence results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED; cannot trust this run.")
        raise SystemExit(1)
    print()

    # STEP 1 — train both regimes per seed, measure markers.
    print(f"STEP 1 — train DET vs NOISY from identical pinned init, {args.seeds} seeds (SERIAL):", flush=True)
    rows = []
    t0 = time.time()
    for s in range(args.seeds):
        gen = make_source(s)
        train_syms = gen(SEQ_LEN)
        # test continuation: same source, fresh roll-out region (unseen symbols)
        full = gen(SEQ_LEN * 3)
        test_syms = full[SEQ_LEN:SEQ_LEN * 2]
        r = run_pair(s, train_syms, test_syms)
        r["seed"] = s
        r["ce_gap"] = abs(r["noisy"]["train_ce"] - r["det"]["train_ce"])
        r["matched"] = bool(r["ce_gap"] <= args.eps)
        rows.append(r)
        print(f"  seed {s:2d}: det_CE={r['det']['train_ce']:.4f} noisy_CE={r['noisy']['train_ce']:.4f} "
              f"|gap|={r['ce_gap']:.4f} matched={r['matched']}  "
              f"(elapsed {time.time()-t0:.1f}s)", flush=True)
    print()

    matched = [r for r in rows if r["matched"]]
    n_matched, n_total = len(matched), len(rows)
    print(f"matched seed-pairs (|CE_noisy - CE_det| <= {args.eps}): {n_matched}/{n_total}")
    print()

    # STEP 2 — per-marker paired det-vs-noisy table at matched CE.
    def paired(metric, favorable):
        """favorable: callable(noisy,det)->signed diff in the consciousness-favorable direction."""
        diffs = [favorable(r["noisy"][metric] if metric in r["noisy"] else r["noisy"],
                           r["det"][metric] if metric in r["det"] else r["det"]) for r in matched]
        return np.asarray(diffs, float)

    markers = []
    # 1 faithful_phi: noisy - det
    markers.append(("faithful_phi", np.array([r["noisy"]["faithful_phi"] - r["det"]["faithful_phi"] for r in matched]),
                    lambda r: (r["noisy"]["faithful_phi"], r["det"]["faithful_phi"])))
    # 2 big_Phi: noisy - det
    markers.append(("big_Phi", np.array([r["noisy"]["big_phi"] - r["det"]["big_phi"] for r in matched]),
                    lambda r: (r["noisy"]["big_phi"], r["det"]["big_phi"])))
    # 3 split_magnitude: |faithful-big| larger under noisy -> |split_noisy| - |split_det|
    markers.append(("split_magnitude",
                    np.array([abs(r["noisy"]["split"]) - abs(r["det"]["split"]) for r in matched]),
                    lambda r: (abs(r["noisy"]["split"]), abs(r["det"]["split"]))))
    # 4 redundancy_margin: noisy - det
    markers.append(("redundancy_margin", np.array([r["noisy"]["redundancy"] - r["det"]["redundancy"] for r in matched]),
                    lambda r: (r["noisy"]["redundancy"], r["det"]["redundancy"])))
    # 5 soc_proximity: |rho-1| SMALLER under noisy -> det_soc_abs - noisy_soc_abs
    markers.append(("soc_proximity", np.array([r["det"]["soc_abs"] - r["noisy"]["soc_abs"] for r in matched]),
                    lambda r: (r["det"]["soc_abs"], r["noisy"]["soc_abs"])))
    # 6 emergence_probe: noisy test better at matched train-CE -> det_testCE - noisy_testCE
    markers.append(("emergence_probe", np.array([r["det"]["test_ce"] - r["noisy"]["test_ce"] for r in matched]),
                    lambda r: (r["det"]["test_ce"], r["noisy"]["test_ce"])))

    print("=" * 90)
    print(f"PER-MARKER PAIRED det-vs-noisy TABLE (at matched CE, n_matched={n_matched})")
    print("  benefit = favorable-direction paired diff with Cohen d >= 0.80")
    print("=" * 90)
    print(f"  {'marker':18s} | {'det mean':>9s} | {'noisy mean':>10s} | {'paired diff':>11s} | "
          f"{'Cohen d':>8s} | benefit?")
    marker_table = []
    any_benefit = False
    for name, diffs, pick in markers:
        det_vals = np.array([pick(r)[1] for r in matched])
        noisy_vals = np.array([pick(r)[0] for r in matched])
        d = cohens_d_paired(diffs)
        mean_diff = float(diffs.mean())
        benefit = bool((not math.isnan(d)) and d >= 0.8)
        any_benefit = any_benefit or benefit
        # report det/noisy in the natural orientation of the metric
        print(f"  {name:18s} | {det_vals.mean():9.4f} | {noisy_vals.mean():10.4f} | "
              f"{mean_diff:+11.4f} | {d:+8.3f} | {str(benefit)}")
        marker_table.append(dict(marker=name, det_mean=float(det_vals.mean()),
                                 noisy_mean=float(noisy_vals.mean()), paired_diff=mean_diff,
                                 cohen_d=(None if math.isnan(d) else float(d)), benefit=benefit))
    print()

    # STEP 3 — verdict.
    degenerate = n_matched < 10
    print("=" * 90)
    if degenerate:
        print("OVERALL: DEGENERATE — fewer than 10 matched-CE seed-pairs; the two regimes could NOT be")
        print(f"  matched on task-performance (n_matched={n_matched} < 10). The CONTROL failed, not the")
        print("  hypothesis. INCONCLUSIVE (neither PASS nor FAIL). VERDICT-TOKEN: DEGENERATE")
        token = "DEGENERATE"
    elif any_benefit:
        winners = [m["marker"] for m in marker_table if m["benefit"]]
        print("OVERALL: PASS — at MATCHED task-performance, non-deterministic LEARNING (SGLD update")
        print(f"  noise) RAISES at least one pre-named consciousness/CE marker (paired Cohen d>=0.8):")
        print(f"  {winners}. This is an advantage the init non-determinism (H_921 prior-RED) and the")
        print("  entropy null did NOT confer. VERDICT-TOKEN: LEARNING-NONDET-HELPS")
        token = "LEARNING-NONDET-HELPS"
    else:
        print("OVERALL: FAIL (CLOSED-NEGATIVE) — at MATCHED task-performance, NO pre-named marker")
        print("  benefits from non-deterministic LEARNING (every marker paired Cohen d < 0.8 in the")
        print("  favorable direction). Learning non-determinism is ALSO not a consciousness advantage,")
        print("  consistent with H_921 (init non-determinism, prior-RED) and the entropy null.")
        print("  a_paper_negative_ok. VERDICT-TOKEN: LEARNING-NONDET-NULL")
        token = "LEARNING-NONDET-NULL"
    print(f"  VERDICT-TOKEN: {token}")
    print("=" * 90)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n<=5 SW substrate. Both Phi")
    print("engines EXACT at n<=5; CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5 (live hexa refs)")
    print("BEFORE scoring (a_phi_iit4_tool; no proxy). AKIDA Lane A on-chip stochastic plasticity +")
    print("GPU Lane G scale-up are SEPARATE substrate rungs, NOT run here (follow-up). g5 CODE-")
    print("measured (no LLM self-judge, p7). NOT a forge binary; $0 CPU-local.")

    out = dict(seeds=int(args.seeds), eps=float(args.eps),
               mirror_proven={int(k): bool(v) for k, v in proven.items()},
               n_matched=int(n_matched), n_total=int(n_total),
               degenerate=bool(degenerate), any_benefit=bool(any_benefit),
               verdict_token=token, markers=marker_table, rows=rows,
               total_wall_sec=time.time() - t0)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nRESULT JSON -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
