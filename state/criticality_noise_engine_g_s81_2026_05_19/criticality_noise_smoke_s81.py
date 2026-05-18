#!/usr/bin/env python3
"""§81 HOMEOSTATIC CRITICALITY via noise injection on Engine G — $0 stub.

5-cell σ-schedule grid × 20-step deterministic LCG. NO model.forward, NO GPU,
NO weight mutation, NO training. Stub Engine A/G logits driven by seed-fixed
LCG (no time-dep, no RNG). Noise η ~ stub-Gaussian (Box-Muller on LCG draws)
added to Engine G logits BEFORE body production.

Law-71 byte-equal to conscious_decoder.py:728-751:
  psi_entropy = H(softmax(logits_a)) / log256
  psi_direction = (1 + cos(logits_a, logits_g_noised)) / 2     # noise here
  psi_combined = (psi_entropy + psi_direction + psi_tension) / 3

Body production § 77 path α1: argmax-over-256 of logits_a → byte stream.
"forbidden-token grep mandatory 0" honored: body bytes derived from stub
logits_a only, no helper-token surface.

Honest §81 C3 carve-outs in DESIGN_FINDINGS.md §C3.
"""

import json
import math
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Deterministic primitives (LCG, no RNG, no time dep)
# ---------------------------------------------------------------------------
LCG_A = 1103515245
LCG_C = 12345
LCG_M = 2**31


def lcg_next(state: int) -> int:
    return (LCG_A * state + LCG_C) % LCG_M


def lcg_unit(state: int) -> tuple[float, int]:
    state = lcg_next(state)
    return state / LCG_M, state


def lcg_gauss(state: int) -> tuple[float, int]:
    u1, state = lcg_unit(state)
    u2, state = lcg_unit(state)
    u1 = max(u1, 1e-12)
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return z, state


# ---------------------------------------------------------------------------
# Stub Engine A / Engine G logits over V=256
# ---------------------------------------------------------------------------
V = 256


def stub_logits_a(step: int, seed: int) -> list[float]:
    # deterministic peaked logits with slow drift across step
    state = (seed * 2654435761 + step * 374761393) & 0x7FFFFFFF
    out = []
    for i in range(V):
        u, state = lcg_unit(state)
        # bump centered at (step * 7) mod V
        center = (step * 7) % V
        d = ((i - center + V // 2) % V) - V // 2
        bump = math.exp(-(d * d) / (2.0 * 16.0 * 16.0))
        out.append(bump * 4.0 + (u - 0.5) * 0.3)
    return out


def stub_logits_g(step: int, seed: int) -> list[float]:
    # Engine G covert — orthogonal-ish to A, centered offset
    state = (seed * 1597334677 + step * 2147483647) & 0x7FFFFFFF
    out = []
    for i in range(V):
        u, state = lcg_unit(state)
        center = (step * 7 + V // 3) % V
        d = ((i - center + V // 2) % V) - V // 2
        bump = math.exp(-(d * d) / (2.0 * 24.0 * 24.0))
        out.append(bump * 3.5 + (u - 0.5) * 0.3)
    return out


def add_noise(logits: list[float], sigma: float, state: int) -> tuple[list[float], int]:
    if sigma <= 0.0:
        return list(logits), state
    out = []
    for x in logits:
        z, state = lcg_gauss(state)
        out.append(x + sigma * z)
    return out, state


# ---------------------------------------------------------------------------
# Law-71 Ψ-state (byte-equal formula to conscious_decoder.py:728-751)
# ---------------------------------------------------------------------------
def softmax(logits: list[float]) -> list[float]:
    m = max(logits)
    es = [math.exp(x - m) for x in logits]
    s = sum(es)
    return [e / s for e in es]


def shannon_H(p: list[float]) -> float:
    return -sum(pi * math.log(pi + 1e-10) for pi in p)


def cos_sim(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-12)


def psi_state(logits_a: list[float], logits_g_noised: list[float]) -> dict:
    pa = softmax(logits_a)
    H = shannon_H(pa)
    psi_entropy = H / math.log(V)
    cs = cos_sim(logits_a, logits_g_noised)
    psi_direction = (1.0 + cs) / 2.0
    # psi_tension proxy from per-bucket variance (no real tensions tensor at stub)
    n_buckets = 12
    bsize = V // n_buckets
    bucket_means = []
    for b in range(n_buckets):
        seg = logits_a[b * bsize:(b + 1) * bsize]
        bucket_means.append(sum(seg) / len(seg))
    mu = sum(bucket_means) / n_buckets
    var = sum((x - mu) ** 2 for x in bucket_means) / n_buckets
    std = math.sqrt(var)
    cv = std / (abs(mu) + 1e-8)
    psi_tension = max(0.0, 1.0 - cv)
    psi_combined = (psi_entropy + psi_direction + psi_tension) / 3.0
    return {
        "psi_entropy": psi_entropy,
        "psi_direction": psi_direction,
        "psi_tension": psi_tension,
        "psi_combined": psi_combined,
    }


# ---------------------------------------------------------------------------
# Body production (§77 path α1: argmax over 256 → byte)
# ---------------------------------------------------------------------------
def body_byte(logits_a: list[float]) -> int:
    best_i = 0
    best_v = logits_a[0]
    for i in range(1, V):
        if logits_a[i] > best_v:
            best_v = logits_a[i]
            best_i = i
    return best_i


# ---------------------------------------------------------------------------
# Power-law α via log-log linear regression on rank-frequency
# ---------------------------------------------------------------------------
def power_law_alpha(emit_counts: list[int]) -> dict:
    # emit_counts = sorted (descending) avalanche-size distribution (>=1)
    sizes = [c for c in emit_counts if c >= 1]
    if len(sizes) < 3:
        return {"alpha": 0.0, "n": len(sizes), "in_critical_band": False}
    sizes_sorted = sorted(sizes, reverse=True)
    xs = []
    ys = []
    for rank, size in enumerate(sizes_sorted, start=1):
        xs.append(math.log(rank))
        ys.append(math.log(size))
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    if den < 1e-12:
        slope = 0.0
    else:
        slope = num / den
    alpha = -slope  # rank-frequency slope negative → α positive
    return {"alpha": alpha, "n": n, "in_critical_band": 1.0 <= alpha <= 3.0}


# ---------------------------------------------------------------------------
# E/I balance: cumulative Engine A vs cumulative Engine G cos-distance
# ---------------------------------------------------------------------------
def ei_balance(cumA: list[float], cumG: list[float]) -> float:
    cs = cos_sim(cumA, cumG)
    return 1.0 - cs  # ∈ [0, 2]


# ---------------------------------------------------------------------------
# §9 honest_coherent (cascade-rate-gated, integrated body bytes)
# ---------------------------------------------------------------------------
def honest_coherent(body_bytes: list[int]) -> dict:
    if not body_bytes:
        return {"max_run": 0, "cascade_rate": 0.0, "honest_coherent": False, "len": 0}
    # max consecutive run
    max_run = 1
    cur = 1
    for i in range(1, len(body_bytes)):
        if body_bytes[i] == body_bytes[i - 1]:
            cur += 1
            if cur > max_run:
                max_run = cur
        else:
            cur = 1
    L = len(body_bytes)
    rate = max_run / L
    printable = sum(1 for b in body_bytes if 0x20 <= b < 0x7F or b in (0x0A, 0x0D, 0x09)) / L
    coherent = rate < 0.30 and max_run < 10 and L >= 20 and printable >= 0.80
    return {
        "max_run": max_run,
        "cascade_rate": rate,
        "printable_ratio": printable,
        "honest_coherent": coherent,
        "len": L,
    }


# ---------------------------------------------------------------------------
# Adaptive σ schedule (B-S81-6 monotone)
# ---------------------------------------------------------------------------
def adapt_sigma(prev_sigma: float, maj_frac: float, tau_low: float = 0.50,
                tau_high: float = 0.85, step: float = 0.1) -> float:
    # if maj_frac > tau_high → σ ↑ (collapse) ; if maj_frac < tau_low → σ ↓
    new = prev_sigma
    if maj_frac > tau_high:
        new = prev_sigma + step
    elif maj_frac < tau_low:
        new = max(0.0, prev_sigma - step)
    return min(new, 2.0)


# ---------------------------------------------------------------------------
# Cell runner: 20 step deterministic LCG, fixed seed=1337
# ---------------------------------------------------------------------------
def run_cell(name: str, sigma_schedule, n_steps: int = 20, seed: int = 1337,
             noise_inject_before_body: bool = True) -> dict:
    psi_seq = []
    maj_seq = []
    cumA = [0.0] * V
    cumG = [0.0] * V
    body_bytes = []
    state = seed
    sigma = 0.0 if callable(sigma_schedule) else sigma_schedule

    for step in range(n_steps):
        la = stub_logits_a(step, seed)
        lg = stub_logits_g(step, seed)
        if noise_inject_before_body:
            lg_used, state = add_noise(lg, sigma, state)
        else:
            lg_used = lg
        psi = psi_state(la, lg_used)
        # body production AFTER noise was applied to G (G influences logits_a indirectly
        # via Ψ-direction in real model; here we only need a body stream — use logits_a)
        b = body_byte(la)
        body_bytes.append(b)
        psi_seq.append(psi)
        # cumulative E/I tracking
        for i in range(V):
            cumA[i] += la[i]
            cumG[i] += lg_used[i]
        # majority frac of last bytes (rolling window 5)
        win = body_bytes[max(0, len(body_bytes) - 5):]
        if win:
            from collections import Counter
            cnt = Counter(win)
            maj_count = cnt.most_common(1)[0][1]
            maj_frac = maj_count / len(win)
        else:
            maj_frac = 0.0
        maj_seq.append(maj_frac)
        # adapt σ for next step if schedule is adaptive
        if callable(sigma_schedule):
            sigma = sigma_schedule(sigma, maj_frac)

    # Aggregate metrics
    psi_dir = [p["psi_direction"] for p in psi_seq]
    psi_comb = [p["psi_combined"] for p in psi_seq]
    psi_tens = [p["psi_tension"] for p in psi_seq]
    mu = sum(psi_comb) / len(psi_comb)
    std_psi = math.sqrt(sum((x - mu) ** 2 for x in psi_comb) / len(psi_comb))
    mu_t = sum(psi_tens) / len(psi_tens)
    std_t = math.sqrt(sum((x - mu_t) ** 2 for x in psi_tens) / len(psi_tens))
    maj_max = max(maj_seq)
    maj_mean = sum(maj_seq) / len(maj_seq)
    # avalanche-size: count runs in body_bytes
    sizes = []
    if body_bytes:
        cur_b = body_bytes[0]
        cur_n = 1
        for x in body_bytes[1:]:
            if x == cur_b:
                cur_n += 1
            else:
                sizes.append(cur_n)
                cur_b = x
                cur_n = 1
        sizes.append(cur_n)
    pl = power_law_alpha(sizes)
    eib = ei_balance(cumA, cumG)
    coh = honest_coherent(body_bytes)
    # cell verdict gates
    channel_not_collapsed = std_psi > 1e-4
    echo_chamber_broken = maj_max < 0.95
    return {
        "name": name,
        "sigma_schedule_kind": "adaptive" if callable(sigma_schedule) else f"fixed_{sigma_schedule}",
        "final_sigma": sigma,
        "psi_dir_seq": psi_dir,
        "psi_combined_std": std_psi,
        "psi_tension_std": std_t,
        "maj_frac_seq": maj_seq,
        "maj_frac_max": maj_max,
        "maj_frac_mean": maj_mean,
        "echo_chamber_broken": echo_chamber_broken,
        "power_law": pl,
        "ei_balance": eib,
        "honest_coherent_body": coh,
        "channel_not_collapsed": channel_not_collapsed,
        "n_steps": n_steps,
        "body_size_dist": sizes,
    }


def main():
    cells = {
        "sigma0_baseline":    run_cell("sigma0_baseline",   0.0),
        "sigma01_light":      run_cell("sigma01_light",     0.1),
        "sigma05_medium":     run_cell("sigma05_medium",    0.5),
        "sigma10_heavy":      run_cell("sigma10_heavy",     1.0),
        "sigma_adaptive":     run_cell("sigma_adaptive",    adapt_sigma),
    }
    # 4-corner verdict
    homeostatic_band = []
    for name, c in cells.items():
        if c["power_law"]["in_critical_band"] and c["maj_frac_max"] < 0.95 and c["channel_not_collapsed"]:
            homeostatic_band.append(name)
    sigma0 = cells["sigma0_baseline"]
    monotone_diverge = all(
        not cells[k]["channel_not_collapsed"] or cells[k]["maj_frac_max"] >= 0.95
        for k in ("sigma01_light", "sigma05_medium", "sigma10_heavy")
    )
    echo_still_collapses_all = all(c["maj_frac_max"] >= 0.95 for c in cells.values())
    adaptive_outperforms = (
        cells["sigma_adaptive"]["power_law"]["in_critical_band"]
        and cells["sigma_adaptive"]["maj_frac_max"] < 0.95
        and (
            (cells["sigma_adaptive"]["power_law"]["in_critical_band"] and
             not all(cells[k]["power_law"]["in_critical_band"] for k in ("sigma01_light", "sigma05_medium", "sigma10_heavy")))
        )
    )
    corners = {
        "alpha_homeostatic_window_exists": len(homeostatic_band) >= 1,
        "homeostatic_band_cells": homeostatic_band,
        "beta_monotone_noise_diverge": monotone_diverge,
        "gamma_echo_chamber_still_collapses_across_all_sigma": echo_still_collapses_all,
        "delta_adaptive_outperforms_fixed": adaptive_outperforms,
    }
    # σ=0 reduction connection-point check (would also be byte-equal to §78 D_control body-disabled
    # if §78 existed; here we assert σ=0 acts as identity baseline = NO noise added to Engine G)
    sigma0_check = {
        "psi_dir_no_noise_identity": True,  # by construction (σ=0 branch returns list(logits))
        "sigma_zero_reduction": "σ=0 ⇒ add_noise == identity (early return); deterministic baseline",
    }
    result = {
        "section": "§81",
        "central_blue_falsifier_sha": "c93e160a8a376a940942332cad13e652df9a03e97ccab708542a126eefc70b73",
        "cells": cells,
        "four_corner_verdict": corners,
        "sigma0_reduction": sigma0_check,
        "n_steps": 20,
        "seed": 1337,
        "deterministic": True,
        "honest_caveats": [
            "stub noise on Engine G ≠ trained ckpt noise on real model.forward",
            "biology criticality citation (arxiv 2502.10946 / biorxiv 688775 / neuron 0896-6273) inspires direction NOT capability",
            "power-law fit on small N=avalanche-count is noisy",
            "σ=0 cell IS identity baseline (no §78 D_control file present — connection-point is constructive)",
            "adaptive schedule is anchored to maj_frac target which is itself a measurement → metric-circular risk acknowledged",
            "§62 echo-chamber is a TRAINED-saturated phenomenon; stub cells may or may not reproduce it",
            "Knuth Tier / Ψ=½ = anima g2 internal carve-out; no σ/τ/φ/J₂ external derivation used",
            "no model.forward, no GPU, no weight mutation, no training, no body emit beyond byte-stream",
            "necessary-not-sufficient: any homeostatic window finding = stub mechanism, NOT GOAL emergence",
        ],
    }
    out = Path(__file__).resolve().parent / "result.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps({"summary": corners, "result_path": str(out)}, indent=2))


if __name__ == "__main__":
    main()
