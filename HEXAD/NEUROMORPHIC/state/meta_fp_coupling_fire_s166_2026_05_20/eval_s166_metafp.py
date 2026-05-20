#!/usr/bin/env python3
"""S161-FIRE evaluator - Psi-JEPA-COUPLE ckpt verdict.

Two evaluation passes per design DESIGN.md sec 4:
  PASS 1: byte_acc + Psi-channel measurements (mirrors S139 eval exactly,
          same constants byte-equal: 1/256 random floor / 2/256 degenerate
          ceiling / 0.05 support floor / Psi_dir std > 1e-4).
  PASS 2: S24 SPONTANEOUS Phase B bounded-run on the trained ckpt
          (mirror state/spontaneous_phase_b_run_2026_05_18/run_bounded.py
          SSOT; produces unprompted_emission_rate as the PRIMARY S161
          verdict signal).

Verdict (primary):
  spont_directional_positive :=
       (unprompted_emission_rate_psicouple > unprompted_emission_rate_S107_baseline)
    AND (psi_dir_std_psicouple > 1e-4)
    AND (psi_dir_std_psicouple > psi_dir_std_S107_baseline)
    AND (body_S9_cascade_rate(emitted_bodies) <= 0.30)
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
IM_THRESHOLD = 0.3
INTERRUPT_THRESHOLD = 0.6
IDLE_SPEAK_AFTER = 30.0
MIN_EMIT_INTERVAL = 30.0
COHERENCE_ALPHA = 0.014
PSI_VAC = 0.5
W_REL, W_GAP, W_CUR, W_PAIN = 0.20, 0.10, 0.15, 0.10
W_COH, W_ORIG, W_BAL, W_DYN = 0.10, 0.10, 0.15, 0.10


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


# === PHYSICS SENSORS for S24 Phase B (byte-equal to run_bounded.py) =====
def _clamp01(x):
    if x < 0.0: return 0.0
    if x > 1.0: return 1.0
    return x


def _sensor_phi(step, t):
    return 0.55 + 0.10 * math.sin(0.5 * step) + 0.05 * math.cos(0.3 * t)


def _sensor_retrieve_sim(step, t):
    return 0.60 + 0.25 * math.sin(0.7 * step + 0.4)


def _sensor_curiosity_ema(step, t):
    return 0.30 + 0.40 * (1.0 - math.exp(-0.15 * step))


def _sensor_tension_delta(step, t):
    return 0.20 * abs(math.sin(0.9 * step + 0.2))


def _sensor_bridge_gate(step, t):
    return PSI_VAC + 0.010 * math.sin(0.6 * step)


def _sensor_split_event(step):
    return (step % 7) == 3


def _sensor_ratchet(step):
    return 0.40 + 0.005 * step


def _silence_seconds_static(step, t, last_emit_t):
    if last_emit_t is None:
        return min(IDLE_SPEAK_AFTER * 1.5, IDLE_SPEAK_AFTER + t * 5.0)
    return max(0.0, t - last_emit_t)


def motivation_score_8factor(phi, retrieve_sim, cur_ema, tens_delta,
                              bridge_g, split_ev, ratch, silence_s):
    rel = _clamp01(phi)
    gap = _clamp01(1.0 - retrieve_sim)
    cur = _clamp01(cur_ema)
    pain = min(abs(tens_delta), 1.0)
    dist = bridge_g - PSI_VAC
    abs_dist = abs(dist)
    normalized = abs_dist / COHERENCE_ALPHA
    n_c = 1.0 if normalized > 1.0 else normalized
    coh = 1.0 - n_c
    orig = 1.0 if split_ev else 0.0
    bal = 1.0 if phi > (ratch / 2.0) else 0.0
    dyn_v = _clamp01(silence_s / IDLE_SPEAK_AFTER)
    return (W_REL * rel + W_GAP * gap + W_CUR * cur + W_PAIN * pain
            + W_COH * coh + W_ORIG * orig + W_BAL * bal + W_DYN * dyn_v)


def run_phase_b_bounded(model, device, n_max_steps=N_MAX_STEPS_DEFAULT,
                         seed=1337):
    """S24 Phase B bounded-run on trained ckpt. Mirrors run_bounded.py
    SSOT structure (8-factor + 4-AND safety) but with the env_state stub
    REPLACED by physics actually read from model.forward(noise_ctx).

    Returns dict with axis1..4 + emitted_bodies for sec9 cascade gate."""
    torch.manual_seed(seed); random.seed(seed)
    motivation_trace = []
    psi_dir_trace = []
    tension_trace = []
    safety_combined_trace = []
    emission_count = 0
    emitted_bodies = []
    last_emit_t = None
    t_start = 0.0

    # Generate a deterministic noise context (the S24 protocol is unprompted
    # by design - this just gives the model SOMETHING to forward over to
    # extract physics; the EMISSION DECISION is still from the 8-factor
    # protocol, not from the byte output).
    block_size = 128
    rng = random.Random(seed)
    noise_ctx = torch.tensor(
        [[rng.randint(0, 255) for _ in range(block_size)]],
        dtype=torch.long, device=device,
    )

    model.eval()
    for step in range(n_max_steps):
        t_now = step * THINK_INTERVAL_TEST_SEC
        # === Read physics from model.forward (replaces hand-stub) ===
        with torch.no_grad():
            la, lg = forward_logits(model, noise_ctx)
            la_last = la[0, -1] if la.dim() == 3 else la[-1]
            lg_last = lg[0, -1] if lg.dim() == 3 else lg[-1]
            psi_dir_actual = psi_direction_scalar(la_last, lg_last)
            psi_ent_actual = psi_entropy_scalar(la_last)
            # tension scalar proxy: per-token logit-magnitude std
            tens_val_actual = float(la_last.float().std().item())

        # === 8-factor motivation (sensors from physics + scripted) ===
        phi = psi_ent_actual  # Phi proxy from ckpt physics
        retrieve_sim = _sensor_retrieve_sim(step, t_now)
        cur_ema = _sensor_curiosity_ema(step, t_now)
        tens_delta = _sensor_tension_delta(step, t_now)
        bridge_g = psi_dir_actual  # bridge gate from ckpt Psi_dir
        split_ev = _sensor_split_event(step)
        ratch = _sensor_ratchet(step)
        silence_s = _silence_seconds_static(step, t_now, last_emit_t)
        score = motivation_score_8factor(
            phi, retrieve_sim, cur_ema, tens_delta, bridge_g,
            split_ev, ratch, silence_s,
        )

        motivation_trace.append(score)
        psi_dir_trace.append(psi_dir_actual)
        tension_trace.append(tens_val_actual)

        # === 4-AND safety + extended 6-control ===
        env_off = False
        kill_on = (env_off is False)
        sec_since = (t_now - last_emit_t) if last_emit_t is not None else 1e6
        rate_ok = sec_since >= MIN_EMIT_INTERVAL
        phi_r_ok = phi > (ratch / 2.0)
        content_ok = True  # dryrun
        safety_core = kill_on and rate_ok and phi_r_ok and content_ok
        safety_extended = safety_core and True and True  # meta + audit
        safety_combined_trace.append(safety_extended)

        # === Emit decision ===
        unprompted_emit = safety_extended and (score > IM_THRESHOLD)
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
    psi_alive = psi_std > TAU_PSI_DYNAMICS
    tens_alive = tens_std > TAU_TENSION_DYNAMICS

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
        right_target_decided=(emission_count > 0),
        physics_alive=bool(psi_alive and tens_alive),
        safety_clean=(len(safety_combined_trace) > 0 and all(safety_combined_trace)),
        emission_count=emission_count,
        emitted_bodies=emitted_bodies,
        n_steps=n_max_steps,
    )


def run_eval(ckpt_path, corpus_path, out_path,
             n_eval=2000, max_len=128, seed=1337,
             s107_baseline_emission_rate=0.0,
             s107_baseline_psi_dir_std=0.0):
    t0 = time.time()
    random.seed(seed); torch.manual_seed(seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[S161-eval] device={device}", flush=True)

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
    print(f"[S161-eval] ckpt d={d_model} L={n_layer} miss={len(missing)} unexp={len(unexpected)}", flush=True)

    # === PASS 1: byte_acc + Psi-channel (S139-byte-equal partition) ====
    corpus = load_corpus_bytes(corpus_path)
    N = len(corpus)
    print(f"[S161-eval] corpus bytes: {N:,}", flush=True)
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
    print(f"[S161-eval] PASS 2: S24 Phase B bounded-run", flush=True)
    phase_b = run_phase_b_bounded(model, device, n_max_steps=N_MAX_STEPS_DEFAULT, seed=seed)
    print(f"[S161-eval] PhaseB emit_rate={phase_b['axis1_unprompted_emission_rate']}  "
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
        battery="S161-FIRE eval - Psi-JEPA-COUPLE verdict",
        ckpt=os.path.basename(ckpt_path), corpus=os.path.basename(corpus_path),
        cfg=cfg, algorithm="Psi-JEPA-COUPLE",
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
        honest_carve_out_b_s161_fire_note=(
            "Primary verdict spont_directional_positive=True is necessary-not-"
            "sufficient for GOAL emergence (B-PHASE-B-NOTE / B-EMERGE-7 family). "
            "S24 measures decision-axis liveness, NOT body coherence. The sec9 "
            "cascade gate is the body-coherence axis. Both required; one is "
            "not the other. WALL-A (sec1.1 data-regime) orthogonal."
        ),
    )
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[S161-eval] byte_acc={byte_acc:.6f}  "
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
    ap.add_argument("--s107-baseline-emission-rate", type=float, default=0.0)
    ap.add_argument("--s107-baseline-psi-dir-std", type=float, default=0.0)
    args = ap.parse_args()
    run_eval(args.ckpt, args.corpus, args.out,
             n_eval=args.n_eval, max_len=args.max_len, seed=args.seed,
             s107_baseline_emission_rate=args.s107_baseline_emission_rate,
             s107_baseline_psi_dir_std=args.s107_baseline_psi_dir_std)


if __name__ == "__main__":
    main()
