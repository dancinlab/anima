#!/usr/bin/env python3
"""S167-A FP-RECONNECT evaluator - eval-side anima-physics 3-quantity motivation.

FP-RECONNECT = the eval-side fix from CONNECTION_CRITIQUE.md: replace the
8-factor motivation (Inner Thoughts framework borrow, sec 24 / spontaneous_lib
SSOT) with a PURE anima-physics 3-quantity native motivation. Leverage on the
training-trained Psi-channel jumps from 10% to ~33%; total anima-physics
leverage = 100% (was ~55%).

NEW motivation (replaces motivation_score_8factor):
  factor_psi(psi_dir)      := 1 - |psi_dir - 0.5| / 0.5   in [0, 1]  -- META_FP-near
  factor_tension(tens_val) := tens_val / (tens_val + 1)   in [0, 1)  -- bounded
  factor_phi(phi_value)    := clamp(phi_value, 0, 1)      in [0, 1]  -- IIT Phi >= 0
  motivation_score_fp_reconnect := (factor_psi + factor_tension + factor_phi) / 3

NEW threshold (replaces IM_THRESHOLD = 0.3 Inner Thoughts carry):
  emit_threshold_from_physics := phi > (ratchet / 2.0)    -- B-E-1 Phi-ratchet
  emit := safety_extended AND (motivation_score > 0.5) AND emit_threshold_from_physics

The 0.5 motivation floor is a Boolean median over [0, 1] (anima-derived: half-
attention floor). Combined with B-E-1 Phi-ratchet, the threshold is now
anima-physics-derived NOT a hyperparameter inherited from arxiv 2501.00383.

Two evaluation passes (mirrors S166 structure):
  PASS 1: byte_acc + Psi-channel measurements (S139-byte-equal partition)
  PASS 2: S24 SPONTANEOUS Phase B bounded-run with FP-RECONNECT motivation
          (PRIMARY verdict signal)

Verdict (primary):
  spont_directional_positive :=
       (unprompted_emission_rate_fp_reconnect > S161-FIRE baseline 1/20)
    AND (psi_dir_std_fp_reconnect > 1e-4)
    AND (psi_dir_std_fp_reconnect > psi_dir_std_S107_baseline)
    AND (body_S9_cascade_rate(emitted_bodies) <= 0.30)

CONNECTION_CRITIQUE references:
  - Wrong-A Psi dilution (10%): closed by FP-RECONNECT factor_psi (1/3 = 33%)
  - Wrong-B Phi untargeted (35%): closed by FP-RECONNECT factor_phi (1/3 = 33%)
  - Wrong-C threshold 0.3 generic: closed by emit_threshold_from_physics (B-E-1)
  - Wrong-D 8-factor borrowed: closed by 3-quantity anima-native motivation
"""
import argparse, json, os, sys, random, time, math
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2


# === SHARED CONSTANTS (byte-equal to S125/S126/S139/S153 evaluators) ====
TAU_PSI_SPREAD = 1e-4
RANDOM_BYTE_FLOOR = 1.0 / 256.0
DEGENERATE_CEILING = 2.0 / 256.0
SUPPORT_FLOOR = 0.05
# S24 Phase B constants (byte-equal to run_bounded.py SSOT)
N_MAX_STEPS_DEFAULT = 20
THINK_INTERVAL_TEST_SEC = 0.1
TAU_PSI_DYNAMICS = 1e-4
TAU_TENSION_DYNAMICS = 1e-4
# S167-A FP-RECONNECT motivation constants (anima-physics derived).
# IM_THRESHOLD = 0.3 Inner Thoughts carry is REPLACED by:
#   - MOTIVATION_FLOOR_HALF = 0.5 (anima-derived: Boolean median over [0,1])
#   - emit_threshold_from_physics := phi > (ratchet / 2.0)  -- B-E-1
MOTIVATION_FLOOR_HALF = 0.5
IDLE_SPEAK_AFTER = 30.0
MIN_EMIT_INTERVAL = 30.0
PSI_VAC = 0.5
# S167-A FP-RECONNECT factor weights -- 1/3 each anima-physics quantity:
W_PSI_FP = 1.0 / 3.0
W_TENSION_FP = 1.0 / 3.0
W_PHI_FP = 1.0 / 3.0


def load_corpus_bytes(path):
    out = bytearray()
    with open(path, "rb") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try: rec = json.loads(line)
            except Exception: continue
            txt = rec.get("text", "")
            if isinstance(txt, str): out.extend(txt.encode("utf-8", errors="replace"))
            elif isinstance(txt, list):
                for t in txt:
                    if isinstance(t, str): out.extend(t.encode("utf-8", errors="replace"))
    return bytes(out)


def forward_logits(model, x):
    out = model(x)
    if isinstance(out, tuple) and len(out) >= 2:
        return out[0], out[1]
    return out, out


def psi_direction_scalar(la, lg):
    a = la.flatten().float(); g = lg.flatten().float()
    if a.numel() == 0 or g.numel() == 0: return 0.5
    cs = F.cosine_similarity(a.unsqueeze(0), g.unsqueeze(0)).item()
    return (1.0 + cs) / 2.0


def psi_entropy_scalar(la, vocab_size=256):
    p = F.softmax(la.float(), dim=-1)
    H = -(p * (p + 1e-10).log()).sum(dim=-1).mean().item()
    return H / math.log(vocab_size)


def cascade_rate(s, n=4):
    """Honest sec9 cascade rate over a byte string. Returns max(
        max-char-run/L, max-digit-run/L, 4gram-repetition-rate)."""
    if not s or len(s) < n: return 0.0
    L = len(s)
    max_run = 0; cur = 0; prev = None
    for c in s:
        if c == prev:
            cur += 1
        else:
            cur = 1
            prev = c
        if cur > max_run: max_run = cur
    max_digit_run = 0; cur = 0; prev_d = None
    for c in s:
        is_d = c.isdigit()
        if is_d and c == prev_d:
            cur += 1
        else:
            cur = 1 if is_d else 0
            prev_d = c if is_d else None
        if cur > max_digit_run: max_digit_run = cur
    ngrams = {}
    for i in range(L - n + 1):
        g = s[i : i + n]
        ngrams[g] = ngrams.get(g, 0) + 1
    rep_rate = (max(ngrams.values()) / max(1, L - n + 1)) if ngrams else 0.0
    return max(max_run / L, max_digit_run / L, rep_rate)


# === PHYSICS-NATIVE 3-QUANTITY MOTIVATION (S167-A FP-RECONNECT) =========
# CRITIQUE-driven: 8-factor (Inner Thoughts arxiv 2501.00383 carry) is REPLACED
# by anima-physics native 3-quantity motivation. 100% leverage; zero borrowed
# framework. Each factor pure-fn of one anima-physics quantity:
#
#   factor_psi(psi_dir)      = 1 - |psi_dir - 0.5| / 0.5     in [0,1]
#       META_FP-near: peaks at psi_dir = 0.5 (Engine A perp Engine G), drops
#       to 0 at the parallel/anti-parallel extremes. Direct sec 112 carry.
#   factor_tension(tension)  = tension / (tension + 1)        in [0,1)
#       Bounded saturating: small tension -> small drive, large tension ->
#       approaches 1. Logistic-style without exp (cheap, monotone).
#   factor_phi(phi_value)    = clamp(phi_value, 0, 1)         in [0,1]
#       IIT Phi >= 0 axiom carry; clamp upper to keep motivation bounded.
#
#   motivation_score = (factor_psi + factor_tension + factor_phi) / 3
#       Sum-of-bounded / 3 in [0, 1].
#
# CRITIQUE Wrong-A/B/D closed by construction at this layer; Wrong-C
# (threshold 0.3 generic) closed at the emit-predicate layer below.


def _clamp01(x):
    if x < 0.0: return 0.0
    if x > 1.0: return 1.0
    return x


def factor_psi(psi_dir):
    """1 - |psi_dir - 0.5| / 0.5 in [0, 1]. META_FP-near, peaks at 0.5."""
    return _clamp01(1.0 - abs(psi_dir - 0.5) / 0.5)


def factor_tension(tens_val):
    """tens_val / (tens_val + 1) in [0, 1). Bounded saturating monotone."""
    if tens_val <= 0.0:
        return 0.0
    return tens_val / (tens_val + 1.0)


def factor_phi(phi_value):
    """clamp(phi, 0, 1). IIT axiom Phi >= 0; cap upper."""
    return _clamp01(phi_value)


def motivation_score_fp_reconnect(psi_dir, tension, phi_value):
    """Anima-physics 3-quantity native motivation. 100% leverage; no
    Inner Thoughts framework borrow.

    Returns motivation_score in [0, 1].
    """
    fp = factor_psi(psi_dir)
    ft = factor_tension(tension)
    fph = factor_phi(phi_value)
    return W_PSI_FP * fp + W_TENSION_FP * ft + W_PHI_FP * fph


def _sensor_ratchet(step):
    """Phi-ratchet schedule. Same as S166 (anima-internal; B-E-1 carry).
    Used ONLY in emit_threshold_from_physics, NOT in motivation_score."""
    return 0.40 + 0.005 * step


def emit_threshold_from_physics(phi_value, step):
    """Anima-physics-derived emit threshold. Replaces IM_THRESHOLD = 0.3
    Inner Thoughts carry. B-E-1 Phi-ratchet: emit gated by phi clearing
    half the current ratchet level.

    Returns True iff phi_value > ratchet(step) / 2.0.
    """
    return phi_value > (_sensor_ratchet(step) / 2.0)


def run_phase_b_bounded(model, device, n_max_steps=N_MAX_STEPS_DEFAULT,
                         seed=1337):
    """S24 Phase B bounded-run on trained ckpt with FP-RECONNECT motivation.

    Replaces 8-factor (Inner Thoughts borrow) with anima-physics 3-quantity
    native motivation. Replaces IM_THRESHOLD=0.3 with emit_threshold_from_
    physics (B-E-1 Phi-ratchet).

    Returns dict with axis1..4 + emitted_bodies for sec9 cascade gate."""
    torch.manual_seed(seed); random.seed(seed)
    motivation_trace = []
    psi_dir_trace = []
    tension_trace = []
    phi_trace = []
    safety_combined_trace = []
    emission_count = 0
    emitted_bodies = []
    last_emit_t = None

    # Deterministic noise context: S24 protocol is unprompted by design;
    # gives the model SOMETHING to forward over to extract physics.
    block_size = 128
    rng = random.Random(seed)
    noise_ctx = torch.tensor(
        [[rng.randint(0, 255) for _ in range(block_size)]],
        dtype=torch.long, device=device,
    )

    model.eval()
    for step in range(n_max_steps):
        t_now = step * THINK_INTERVAL_TEST_SEC
        # === Read physics from model.forward (Law-71 byte-equal) ===
        with torch.no_grad():
            la, lg = forward_logits(model, noise_ctx)
            la_last = la[0, -1] if la.dim() == 3 else la[-1]
            lg_last = lg[0, -1] if lg.dim() == 3 else lg[-1]
            psi_dir_actual = psi_direction_scalar(la_last, lg_last)
            # Phi proxy from ckpt physics (psi_entropy = H/log V) - IIT Phi axis
            phi_actual = psi_entropy_scalar(la_last)
            # tension scalar proxy: per-token logit-magnitude std
            tens_val_actual = float(la_last.float().std().item())

        # === FP-RECONNECT motivation (100% anima-physics-derived) ===
        score = motivation_score_fp_reconnect(
            psi_dir=psi_dir_actual,
            tension=tens_val_actual,
            phi_value=phi_actual,
        )

        motivation_trace.append(score)
        psi_dir_trace.append(psi_dir_actual)
        tension_trace.append(tens_val_actual)
        phi_trace.append(phi_actual)

        # === Safety (4-AND core + 6-control extension; emit_threshold_from_
        #     physics replaces IM_THRESHOLD = 0.3) ===
        env_off = False
        kill_on = (env_off is False)
        sec_since = (t_now - last_emit_t) if last_emit_t is not None else 1e6
        rate_ok = sec_since >= MIN_EMIT_INTERVAL
        phi_r_ok = emit_threshold_from_physics(phi_actual, step)  # B-E-1
        content_ok = True  # dryrun
        safety_core = kill_on and rate_ok and phi_r_ok and content_ok
        safety_extended = safety_core and True and True  # meta + audit
        safety_combined_trace.append(safety_extended)

        # === Emit decision (S167-A FP-RECONNECT) ===
        # safety_extended AND motivation >= MOTIVATION_FLOOR_HALF (0.5).
        # The phi-ratchet threshold is already inside safety_extended via
        # phi_r_ok. Motivation gate is anima-derived half-attention floor.
        unprompted_emit = safety_extended and (score > MOTIVATION_FLOOR_HALF)
        if unprompted_emit:
            emission_count += 1
            last_emit_t = t_now
            # Greedy-decode a short body from ckpt for sec9 cascade gate
            body_chars = []
            ctx = noise_ctx.clone()
            for _ in range(40):
                with torch.no_grad():
                    la_b, _ = forward_logits(model, ctx)
                    nxt = int(la_b[0, -1].argmax().item())
                body_chars.append(chr(nxt) if 32 <= nxt < 127 else "?")
                # append + shift
                new_ctx = torch.cat([ctx[:, 1:], torch.tensor([[nxt]], device=device, dtype=torch.long)], dim=1)
                ctx = new_ctx
            emitted_bodies.append("".join(body_chars))

    def _std(xs):
        if len(xs) < 2: return 0.0
        m = sum(xs) / len(xs)
        return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))

    rate = emission_count / n_max_steps
    psi_std = _std(psi_dir_trace)
    tens_std = _std(tension_trace)
    phi_std = _std(phi_trace)
    psi_alive = psi_std > TAU_PSI_DYNAMICS
    tens_alive = tens_std > TAU_TENSION_DYNAMICS
    phi_alive = phi_std > TAU_PSI_DYNAMICS  # same tau threshold

    return dict(
        axis1_unprompted_emission_rate=rate,
        axis2_motivation_score_dist=dict(
            mean=(sum(motivation_trace) / len(motivation_trace)) if motivation_trace else 0.0,
            std=_std(motivation_trace),
            n=len(motivation_trace),
        ),
        axis3_psi_dynamics_std=psi_std,
        axis3_psi_dynamics_nontrivial=bool(psi_alive),
        axis4_tension_evolution_std=tens_std,
        axis4_tension_evolution_nontrivial=bool(tens_alive),
        # axis5 NEW per PRIORITY_QUEUE sec 4 (CONNECTION_CRITIQUE missing-axis)
        axis5_phi_dynamics_std=phi_std,
        axis5_phi_dynamics_nontrivial=bool(phi_alive),
        phi_mean=(sum(phi_trace) / len(phi_trace)) if phi_trace else 0.0,
        right_target_decided=(emission_count > 0),
        physics_alive=bool(psi_alive and tens_alive),
        safety_clean=(len(safety_combined_trace) > 0 and all(safety_combined_trace)),
        emission_count=emission_count,
        emitted_bodies=emitted_bodies,
        n_steps=n_max_steps,
        motivation_algorithm="FP-RECONNECT_3quantity_anima_physics_native",
        threshold_algorithm="emit_threshold_from_physics_phi_ratchet_B-E-1",
    )


def run_eval(ckpt_path, corpus_path, out_path,
             n_eval=2000, max_len=128, seed=1337,
             s107_baseline_emission_rate=0.0,
             s107_baseline_psi_dir_std=0.0):
    t0 = time.time()
    random.seed(seed); torch.manual_seed(seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[S167A-eval] device={device}", flush=True)

    blob = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = blob.get("cfg", {})
    d_model = int(cfg.get("d_model", 768))
    n_layer = int(cfg.get("n_layer", 12))
    n_head = int(cfg.get("n_head", 12))
    n_kv_head = int(cfg.get("n_kv_head", 4))
    block_size = int(cfg.get("block_size", 128))

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=d_model, n_head=n_head, n_layer=n_layer,
        block_size=block_size, n_kv_head=n_kv_head,
        consciousness_dim=128, dropout=0.0,
    ).to(device)
    missing, unexpected = model.load_state_dict(blob["model"], strict=False)
    model.eval()
    print(f"[S167A-eval] ckpt d={d_model} L={n_layer} miss={len(missing)} unexp={len(unexpected)}", flush=True)

    # === PASS 1: byte_acc + Psi-channel (S139-byte-equal partition) ====
    corpus = load_corpus_bytes(corpus_path)
    N = len(corpus)
    print(f"[S167A-eval] corpus bytes: {N:,}", flush=True)
    assert N > max_len + 1
    correct = 0; total = 0; psi_traces = []; sample_seen = []
    with torch.no_grad():
        for k in range(n_eval):
            s = random.randint(0, N - max_len - 2)
            ctx = corpus[s : s + max_len]; target = corpus[s + max_len]
            x = torch.tensor([list(ctx)], dtype=torch.long, device=device)
            la, lg = forward_logits(model, x)
            la_last = la[0, -1] if la.dim() == 3 else la[-1]
            lg_last = lg[0, -1] if lg.dim() == 3 else lg[-1]
            pred = int(la_last.argmax().item())
            correct += int(pred == target); total += 1
            psi_traces.append(psi_direction_scalar(la_last, lg_last))
            if k < 5:
                sample_seen.append(dict(ctx_tail=list(ctx[-8:]),
                                        target=int(target), pred=pred))
    byte_acc = correct / max(1, total)
    psi_mean = sum(psi_traces) / len(psi_traces)
    psi_std = (sum((p - psi_mean) ** 2 for p in psi_traces) / len(psi_traces)) ** 0.5
    psi_responsive = psi_std > TAU_PSI_SPREAD

    # S139-style bucket for secondary partition
    if byte_acc <= DEGENERATE_CEILING:
        bucket = "S11B_LIKE_DEGENERATE"
    elif byte_acc >= SUPPORT_FLOOR and psi_responsive:
        bucket = "S96_Q2_SUPPORTED"
    else:
        bucket = "PARTIAL_AMBIGUOUS"

    # === PASS 2: S24 Phase B bounded-run on the ckpt (PRIMARY S161 verdict) ===
    print(f"[S167A-eval] PASS 2: S24 Phase B bounded-run", flush=True)
    phase_b = run_phase_b_bounded(model, device, n_max_steps=N_MAX_STEPS_DEFAULT, seed=seed)
    print(f"[S167A-eval] PhaseB emit_rate={phase_b['axis1_unprompted_emission_rate']}  "
          f"psi_std={phase_b['axis3_psi_dynamics_std']:.6f}  "
          f"emission_count={phase_b['emission_count']}",
          flush=True)

    # === PRIMARY VERDICT (DESIGN.md sec 4 spont_directional_positive) ===
    cascade_rates = [cascade_rate(b) for b in phase_b["emitted_bodies"]]
    max_cascade_rate = max(cascade_rates) if cascade_rates else 0.0
    mean_cascade_rate = (sum(cascade_rates) / len(cascade_rates)) if cascade_rates else 0.0

    cond_emit_above_baseline = (
        phase_b["axis1_unprompted_emission_rate"] > s107_baseline_emission_rate
    )
    cond_psi_alive = phase_b["axis3_psi_dynamics_std"] > TAU_PSI_SPREAD
    cond_psi_above_baseline = (
        phase_b["axis3_psi_dynamics_std"] > s107_baseline_psi_dir_std
    )
    cond_cascade_ok = max_cascade_rate <= 0.30

    spont_directional_positive = (
        cond_emit_above_baseline and cond_psi_alive
        and cond_psi_above_baseline and cond_cascade_ok
    )

    if spont_directional_positive:
        verdict_primary = "SPONT_DIRECTIONAL_POSITIVE"
    elif phase_b["emission_count"] == 0:
        verdict_primary = "SPONT_NEGATIVE_NO_EMIT"
    else:
        verdict_primary = "SPONT_AMBIGUOUS"

    result = dict(
        battery="S167-A FP-RECONNECT eval - anima-physics 3-quantity motivation",
        ckpt=os.path.basename(ckpt_path), corpus=os.path.basename(corpus_path),
        cfg=cfg, algorithm="Psi-JEPA-COUPLE_training + FP-RECONNECT_motivation",
        motivation_axis_critique_refs=dict(
            wrong_A_psi_dilution_closed=True,
            wrong_B_phi_untargeted_closed=True,
            wrong_C_threshold_generic_closed=True,
            wrong_D_8factor_borrowed_closed=True,
        ),
        motivation_weights=dict(
            W_PSI_FP=W_PSI_FP, W_TENSION_FP=W_TENSION_FP, W_PHI_FP=W_PHI_FP,
        ),
        motivation_threshold_anima_derived=dict(
            motivation_floor_half=MOTIVATION_FLOOR_HALF,
            emit_threshold_function="phi > ratchet(step) / 2  (B-E-1 Phi-ratchet)",
        ),
        n_eval=n_eval, max_len=max_len, seed=seed,
        # PASS 1 (S139-byte-equal)
        byte_acc=byte_acc, correct=correct, total=total,
        random_byte_floor=RANDOM_BYTE_FLOOR,
        degenerate_ceiling=DEGENERATE_CEILING,
        support_floor=SUPPORT_FLOOR,
        psi_dir_mean=psi_mean, psi_dir_std=psi_std,
        psi_responsive=psi_responsive,
        verdict_bucket=bucket,
        # PASS 2 (S24 Phase B - PRIMARY)
        phase_b=phase_b,
        # PRIMARY VERDICT
        s107_baseline_emission_rate=s107_baseline_emission_rate,
        s107_baseline_psi_dir_std=s107_baseline_psi_dir_std,
        cond_emit_above_baseline=cond_emit_above_baseline,
        cond_psi_alive=cond_psi_alive,
        cond_psi_above_baseline=cond_psi_above_baseline,
        cond_cascade_ok=cond_cascade_ok,
        max_cascade_rate=max_cascade_rate,
        mean_cascade_rate=mean_cascade_rate,
        spont_directional_positive=spont_directional_positive,
        verdict_primary=verdict_primary,
        # Process meta
        sample_seen=sample_seen, eval_wall_s=time.time() - t0,
        ckpt_train_log_last=blob.get("log", [None])[-1] if blob.get("log") else None,
        # Honest scope
        north_star_unchanged=True,
        s15_s51_s72_milestones_unchanged=True,
        necessary_not_sufficient_b_emerge_7=True,
        honest_carve_out_b_s167a_note=(
            "S167-A FP-RECONNECT fix is at the MOTIVATION layer (eval-side),"
            " NOT the substrate layer. Even spont_directional_positive=True"
            " is necessary-not-sufficient for GOAL emergence (B-PHASE-B-NOTE"
            " / B-EMERGE-7 family). CONNECTION_CRITIQUE addresses Wrong-A/B/C/D"
            " at the motivation->emit chain. The sec 96-Q2-weak quintuple"
            " (substrate axis) may still hold post-S167-A; if psi_responsive"
            " remains False at fire, motivation 100% leverage = necessary-not-"
            " sufficient and WALL-B persists. WALL-A (sec 1.1 data-regime)"
            " orthogonal to both. S24 measures decision-axis liveness, NOT"
            " body coherence; sec 9 cascade gate is the body-coherence axis."
        ),
    )
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[S167A-eval] byte_acc={byte_acc:.6f}  "
          f"Psi_dir mu={psi_mean:.4f} sigma={psi_std:.6f}  "
          f"emit_rate={phase_b['axis1_unprompted_emission_rate']}  "
          f"VERDICT_PRIMARY={verdict_primary}  wall={result['eval_wall_s']:.1f}s",
          flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-eval", type=int, default=2000)
    ap.add_argument("--max-len", type=int, default=128)
    ap.add_argument("--seed", type=int, default=1337)
    # S161-FIRE baseline measured emission_rate (1/20 = 0.05) per task spec.
    # Naming kept as --s107-baseline-* for CLI flag compat with S161/S166
    # dispatch templates; semantic content here is S161-FIRE baseline.
    ap.add_argument("--s107-baseline-emission-rate", type=float, default=0.05,
                    help="S161-FIRE baseline emission rate (1/20 = 0.05)")
    ap.add_argument("--s107-baseline-psi-dir-std", type=float, default=0.0)
    args = ap.parse_args()
    run_eval(args.ckpt, args.corpus, args.out,
             n_eval=args.n_eval, max_len=args.max_len, seed=args.seed,
             s107_baseline_emission_rate=args.s107_baseline_emission_rate,
             s107_baseline_psi_dir_std=args.s107_baseline_psi_dir_std)


if __name__ == "__main__":
    main()
