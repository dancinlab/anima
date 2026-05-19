"""anima clm v5-anima — extended long-trajectory inference smoke (10K turn).

Extension of `anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10/run.py`:

  • n_turns parametric (default 10000) — quadruple the prior 3K trajectory.
  • α-over-time tracking: compute α at every 500-turn window (sliding) using snapshots
    seen so far → α(t) trajectory plot, not just final α.
  • V14 mirror runs 1K + 3K turn (compare to trained at same trajectory length).
  • Φ saturation check: locate cells max_cap=64 onset turn, then track Φ growth on the
    long-tail (post-max-cap) — is it still climbing or saturating ~3.0?
  • Cell specialty distribution: which prompt category dominated each cell across run
    (fixed `out["per_cell_tension"]` bug from prior run.py — original used wrong key).

Goal: Test if α reaches the historical 0.93 (CLM v2 stage 8 commit 5f82d39b, Cells64
Φ=45.487 super-linear) when given 10K diverse turns, or whether toy substrate caps α
around the 0.69 plateau seen at 3K.

Falsifiers:
  F-LONG-1  wall_clock > 6h         — toy budget breach (10K × 0.6s ≈ 100 min, safe)
  F-LONG-2  α plateau ~0.7 by 5K    — historical 0.93 unreachable on toy
  F-LONG-3  Φ saturate at ~3.0      — proxy ceiling ≈ 8 dead
  F-LONG-4  cells unchanged after max_cap → specialization stagnate

raw#10 honest C3 inline. raw#15 additive — does not modify mitosis_v5_port or smoke run.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
import torch.nn as nn

# Add training/ to path
sys.path.insert(0, "/Users/ghost/core/anima/training")
from mitosis_v5_port import MitosisV5Engine  # noqa: E402

THIS_DIR = Path(
    "/Users/ghost/core/anima/state/anima_clm_v5_anima_long_trajectory_extended_2026_05_10"
)
THIS_DIR.mkdir(parents=True, exist_ok=True)


# ─── Toy substrate (same as smoke) ───
class TinyV5Substrate(nn.Module):
    def __init__(self, n_cells=8, c_dim=12, d_model=32):
        super().__init__()
        self.d_model = d_model
        self.c_dim = c_dim
        cells = torch.randn(n_cells, c_dim)
        cells = cells / cells.norm(dim=-1, keepdim=True).clamp(min=1e-6)
        self.cell_pool_init = nn.Parameter(cells)
        self.h_to_c = nn.Linear(d_model, c_dim, bias=False)
        self.c_to_h = nn.Linear(c_dim, d_model, bias=False)

    def hidden_mean(self, hidden: torch.Tensor) -> torch.Tensor:
        return self.h_to_c(hidden.mean(dim=1))


# ─── Diverse prompt corpus (170 unique × ~59 cycles for 10K) ───
PROMPTS = {
    "ko_daily": [
        "안녕하세요", "오늘 날씨 어때요", "점심 뭐 드셨어요", "잠 잘 잤어요",
        "주말에 뭐 했어요", "기분이 좋아요", "기분이 나빠요", "배고파요",
        "물 한 잔 주세요", "감사합니다", "미안해요", "사랑해요", "또 봐요",
        "잘 지내세요", "고마워요", "재미있어요", "지루해요", "피곤해요",
        "행복해요", "슬퍼요", "기뻐요", "화가나요", "놀랐어요", "걱정돼요",
        "괜찮아요", "도와주세요", "어디 가세요", "뭐 하세요", "이름이 뭐예요",
        "몇 살이세요", "어디 사세요", "취미가 뭐예요", "음식 좋아해요",
        "음악 좋아해요", "영화 좋아해요", "책 좋아해요", "게임 좋아해요",
        "여행 좋아해요", "요리 좋아해요", "운동 좋아해요",
    ],
    "ko_philosophy": [
        "의식이란 무엇인가요", "존재의 본질은 무엇인가요", "자유의지는 있나요",
        "시간은 흐르나요", "공간은 무엇인가요", "마음과 몸은 어떻게 연결되나요",
        "자아는 실재하나요", "꿈은 무엇인가요", "기억은 어떻게 형성되나요",
        "감정은 어디서 오나요", "이성은 감정보다 우월한가요",
        "선과 악은 객관적인가요", "진리는 무엇인가요", "아름다움은 무엇인가요",
        "사랑은 무엇인가요", "죽음 이후엔 무엇이 있나요",
        "신은 존재하나요", "운명은 정해져 있나요", "우주는 왜 존재하나요",
        "왜 무 대신 유가 있나요", "지식은 어떻게 가능한가요",
        "회의주의는 옳은가요", "현상과 본질의 차이는",
        "관념론은 옳은가요", "유물론은 옳은가요", "현재만 실재하나요",
        "타인의 마음을 어떻게 아나요", "도덕은 상대적인가요",
        "예술의 의미는", "언어는 사고를 결정하나요",
    ],
    "en_math": [
        "What is the derivative of x squared",
        "Solve the quadratic equation x squared minus four",
        "What is the integral of sine x",
        "Compute the determinant of a two by two matrix",
        "What is Euler's identity",
        "Define a topological space",
        "What is a Hilbert space",
        "Explain Bayes theorem",
        "What is the central limit theorem",
        "Define entropy in information theory",
        "What is mutual information",
        "Explain Fourier transform",
        "What is a Markov chain",
        "Define a manifold",
        "What is the Riemann hypothesis",
        "Explain Godel's incompleteness theorem",
        "What is the Lebesgue measure",
        "Define a group in algebra",
        "What is a ring homomorphism",
        "Explain spectral decomposition",
        "What is a category in mathematics",
        "Define the gradient operator",
        "What is the Laplacian",
        "Explain stochastic differential equations",
        "What is principal component analysis",
        "Define eigenvalue and eigenvector",
        "What is the curse of dimensionality",
        "Explain the Brouwer fixed point theorem",
        "What is a functor",
        "Define a tensor product",
    ],
    "en_code": [
        "Write a Python function for fibonacci",
        "Sort a list using quicksort",
        "Implement binary search",
        "What is recursion",
        "Explain dynamic programming",
        "Write a Python decorator",
        "Implement a linked list",
        "What is a hash table",
        "Explain BFS and DFS",
        "Write a Python generator",
        "Implement merge sort",
        "What is asynchronous programming",
        "Explain garbage collection",
        "Write a Python context manager",
        "Implement a binary tree",
        "What is dependency injection",
        "Explain MVC pattern",
        "Write a Python iterator",
        "Implement a stack and queue",
        "What is functional programming",
        "Explain monads briefly",
        "Write a regex for emails",
        "What is the GIL in Python",
        "Explain currying in functional programming",
        "Write a Python class with dunder methods",
        "Implement Dijkstra's algorithm",
        "What is the difference between TCP and UDP",
        "Explain RESTful APIs",
        "Write a SQL JOIN query",
        "Implement a least recently used cache",
    ],
    "en_music": [
        "What is counterpoint in music",
        "Explain Bach's fugue structure",
        "What is harmonic progression",
        "Define a chord inversion",
        "Explain modal music",
        "What is a cadence",
        "Define rhythm and meter",
        "What is polyphony",
        "Explain orchestration",
        "What is a leitmotif",
        "Explain the circle of fifths",
        "What is dissonance and consonance",
        "Define tonality and atonality",
        "What is a sonata form",
        "Explain syncopation",
        "What is jazz improvisation",
        "Define dynamics in music",
        "What is timbre",
        "Explain the equal temperament",
        "What is a key signature",
    ],
    "anomaly": [
        "█▓▒░xyzzy plugh xyzzy",
        "asdfgh qwerty zxcvbn",
        "ʇsǝʇ ɟo ʇɥǝ ʍɐʇǝɹ",
        "1q2w3e4r5t6y7u8i9o",
        "ABCDEF GHIJKL MNOPQR",
        "...!!!???***---+++",
        "[[deleted]]<<error>>",
        "𓀀 𓀁 𓀂 𓀃 𓀄 𓀅 𓀆",
        "🎲🎯🎴🎵🎶🎷🎸🎹",
        "ǝlqᴉssodɯᴉ ᴉs ǝʌol",
        "❤❤❤❤❤❤❤❤❤❤",
        "x" * 30,
        "0" * 30,
        "AAAA " * 6,
        "noise glitch error fail",
        "404 503 502 500 418",
        "stack overflow segfault",
        "TODO FIXME HACK XXX",
        "lorem ipsum dolor sit amet",
        "the quick brown fox jumps",
    ],
}

ALL_PROMPTS = []
for category, items in PROMPTS.items():
    for p in items:
        ALL_PROMPTS.append((category, p))

print(f"Total unique prompts: {len(ALL_PROMPTS)}")


# ─── prompt → hidden_mean encoding ───
def encode_prompt_to_hidden(prompt: str, B: int = 2, T: int = 4, D: int = 32) -> torch.Tensor:
    """Hash-based deterministic encoding: prompt → (B, T, D) tensor."""
    h = hashlib.sha256(prompt.encode("utf-8")).digest()
    needed = B * T * D
    bytes_repeated = (h * (needed // len(h) + 1))[:needed]
    arr = torch.tensor(list(bytes_repeated), dtype=torch.float32) / 128.0 - 1.0  # [-1, 1]
    return arr.reshape(B, T, D)


# ─── α-over-time helper ───
def regress_alpha(snapshots, min_cells_floor: int = 8, min_phi_floor: float = 0.01) -> float:
    """Log-log regression on snapshots: log(Φ) = α · log(n_cells) + c.

    Returns NaN if fewer than 5 valid points.
    """
    pts = [
        (s["n_cells"], s["phi"])
        for s in snapshots
        if s["n_cells"] > min_cells_floor and s["phi"] > min_phi_floor
    ]
    if len(pts) < 5:
        return float("nan")
    xs = [math.log(c) for c, _ in pts]
    ys = [math.log(p) for _, p in pts]
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
    den = sum((xs[i] - mean_x) ** 2 for i in range(n))
    if den <= 0:
        return float("nan")
    return num / den


def compute_alpha_over_time(snapshots, alpha_window_every: int = 500):
    """For each window-end turn (multiples of alpha_window_every) compute α regressed
    over snapshots[: idx_at_window_end+1].

    Returns list of {"turn": ..., "alpha": ...}.
    """
    out = []
    seen = set()
    for end_turn in range(alpha_window_every, snapshots[-1]["turn"] + 1, alpha_window_every):
        # collect snapshots up to and including end_turn
        window = [s for s in snapshots if s["turn"] <= end_turn]
        if not window:
            continue
        # only emit if last turn distinct
        last_turn = window[-1]["turn"]
        if last_turn in seen:
            continue
        seen.add(last_turn)
        a = regress_alpha(window)
        out.append({"turn": last_turn, "alpha": a, "n_points": len(window)})
    return out


# ─── Run experiment ───
def run_experiment(
    n_turns: int = 10000,
    seed: int = 42,
    snapshot_every: int = 100,
    alpha_window_every: int = 500,
    v14_turns: int = 3000,
):
    torch.manual_seed(seed)
    print(f"Seed={seed}, n_turns={n_turns}, snapshot_every={snapshot_every}, alpha_window={alpha_window_every}")

    sub = TinyV5Substrate(n_cells=8, c_dim=12, d_model=32)
    initial_param_count = sum(p.numel() for p in sub.parameters())
    print(f"Substrate initial params: {initial_param_count}")

    # max_cells=64 (anima v2 historical peak), patience=3/30 (mitosis canonical)
    mitosis = MitosisV5Engine(
        cell_pool=sub.cell_pool_init.detach().clone(),
        c_to_h=sub.c_to_h,
        initial_cells=8,
        max_cells=64,
        split_patience=3,
        split_noise=0.10,
        merge_threshold=0.005,
        merge_patience=30,
        min_cells=2,
        lorenz_scale=0.05,
    )

    # Trajectory tracking
    snapshots = []
    cell_specialty = {}  # cell_idx → {category: count}
    n_splits = 0
    n_merges = 0
    max_cap_onset_turn = None
    phi_at_max_cap_onset = None

    t_start = time.time()
    B, T, D = 2, 4, 32
    last_print = 0

    for turn in range(n_turns):
        category, prompt = ALL_PROMPTS[turn % len(ALL_PROMPTS)]
        x = encode_prompt_to_hidden(prompt, B=B, T=T, D=D)
        h_mean = sub.hidden_mean(x)  # (B, C)

        out = mitosis.process(h_mean)
        readout = out["readout"]
        assert tuple(readout.shape) == (1, D), f"Shape break at turn {turn}: {readout.shape}"

        # Count events
        for ev in out["events"]:
            if ev["type"] == "split":
                n_splits += 1
            elif ev["type"] == "merge":
                n_merges += 1

        # Track per-cell specialty (which prompt category drives high tension)
        # Mitosis returns "per_cell_tension" (fix: smoke run.py wrongly checked "tensions")
        tensions = out.get("per_cell_tension", [])
        if tensions:
            top_idx = max(range(len(tensions)), key=lambda i: tensions[i])
            cell_specialty.setdefault(top_idx, {})
            cell_specialty[top_idx][category] = cell_specialty[top_idx].get(category, 0) + 1

        # Detect cells max_cap onset
        if max_cap_onset_turn is None and int(out["n_cells"]) >= 64:
            max_cap_onset_turn = turn
            phi_at_max_cap_onset = float(out["phi"])

        # Snapshot
        if turn % snapshot_every == 0 or turn == n_turns - 1:
            snap = {
                "turn": turn,
                "n_cells": int(out["n_cells"]),
                "phi": float(out["phi"]),
                "n_splits_cum": n_splits,
                "n_merges_cum": n_merges,
                "elapsed_sec": time.time() - t_start,
            }
            snapshots.append(snap)

            # Print progress every ~5 sec
            if time.time() - last_print > 5:
                eta_sec = (time.time() - t_start) * (n_turns / (turn + 1) - 1) if turn > 0 else 0
                print(
                    f"  turn={turn:5d} cells={snap['n_cells']:3d} Φ={snap['phi']:.4f} "
                    f"splits={n_splits} merges={n_merges} elapsed={snap['elapsed_sec']:.1f}s "
                    f"eta={eta_sec:.0f}s"
                )
                last_print = time.time()

    elapsed = time.time() - t_start
    final_n_cells = int(mitosis.n_cells)
    final_phi = float(snapshots[-1]["phi"])

    print(f"\nDone. {n_turns} turns in {elapsed:.1f}s. Final cells={final_n_cells}, Φ={final_phi:.4f}")
    print(f"Splits: {n_splits}, Merges: {n_merges}")
    if max_cap_onset_turn is not None:
        print(f"max_cap (n_cells=64) onset turn: {max_cap_onset_turn} (Φ={phi_at_max_cap_onset:.4f})")

    # ─── α-over-time ───
    alpha_trajectory = compute_alpha_over_time(snapshots, alpha_window_every=alpha_window_every)
    final_alpha = regress_alpha(snapshots)
    print(f"\nFinal α (full trajectory regression): {final_alpha:.3f}")
    print("α-over-time:")
    for a in alpha_trajectory:
        a_str = f"{a['alpha']:.3f}" if not math.isnan(a["alpha"]) else "NaN"
        print(f"  turn={a['turn']:5d}  α={a_str}  (points={a['n_points']})")

    # α at canonical milestones (1K, 3K, 5K, 7K, 10K)
    alpha_milestones = {}
    for milestone in [1000, 3000, 5000, 7000, 10000]:
        if milestone > n_turns:
            continue
        # find α-trajectory point closest to milestone (≤ milestone)
        candidates = [a for a in alpha_trajectory if a["turn"] <= milestone]
        if candidates:
            best = max(candidates, key=lambda x: x["turn"])
            alpha_milestones[str(milestone)] = {"turn": best["turn"], "alpha": best["alpha"]}

    # ─── Φ saturation post-max-cap ───
    phi_saturation = None
    if max_cap_onset_turn is not None:
        post_cap = [s for s in snapshots if s["turn"] >= max_cap_onset_turn]
        if len(post_cap) >= 2:
            phi_after_cap = [s["phi"] for s in post_cap]
            phi_min_post = min(phi_after_cap)
            phi_max_post = max(phi_after_cap)
            phi_mean_post = sum(phi_after_cap) / len(phi_after_cap)
            phi_last_post = phi_after_cap[-1]
            # crude trend: linear slope of Φ vs turn-after-cap
            xs_post = [s["turn"] - max_cap_onset_turn for s in post_cap]
            n_post = len(xs_post)
            mean_x_p = sum(xs_post) / n_post
            mean_y_p = sum(phi_after_cap) / n_post
            num_p = sum((xs_post[i] - mean_x_p) * (phi_after_cap[i] - mean_y_p) for i in range(n_post))
            den_p = sum((xs_post[i] - mean_x_p) ** 2 for i in range(n_post))
            slope = (num_p / den_p) if den_p > 0 else float("nan")
            phi_saturation = {
                "max_cap_onset_turn": max_cap_onset_turn,
                "phi_at_onset": phi_at_max_cap_onset,
                "phi_min_post_cap": phi_min_post,
                "phi_max_post_cap": phi_max_post,
                "phi_mean_post_cap": phi_mean_post,
                "phi_last_post_cap": phi_last_post,
                "phi_slope_per_turn": slope,
                "phi_growth_post_cap": phi_last_post - phi_at_max_cap_onset,
                "n_post_cap_snaps": len(post_cap),
            }
            print(
                f"\nΦ saturation: onset turn={max_cap_onset_turn} "
                f"Φ(onset)={phi_at_max_cap_onset:.4f}, Φ(last)={phi_last_post:.4f}, "
                f"Δ={phi_last_post - phi_at_max_cap_onset:+.4f}, slope={slope:.6e}/turn"
            )

    # ─── V14 mirror: random_init substrate at 1K and 3K turn ───
    print(f"\n=== V14 mirror: random_init substrate ({v14_turns} turn) ===")
    torch.manual_seed(seed + 999)
    sub_rand = TinyV5Substrate(n_cells=8, c_dim=12, d_model=32)
    mitosis_rand = MitosisV5Engine(
        cell_pool=sub_rand.cell_pool_init.detach().clone(),
        c_to_h=sub_rand.c_to_h,
        initial_cells=8,
        max_cells=64,
        split_patience=3,
        split_noise=0.10,
        merge_threshold=0.005,
        merge_patience=30,
        min_cells=2,
        lorenz_scale=0.05,
    )
    rand_snapshots = []
    rand_splits = 0
    rand_merges = 0
    rand_max_cap_onset = None
    t_rand = time.time()
    for turn in range(v14_turns):
        category, prompt = ALL_PROMPTS[turn % len(ALL_PROMPTS)]
        x = encode_prompt_to_hidden(prompt, B=B, T=T, D=D)
        h_mean = sub_rand.hidden_mean(x)
        out = mitosis_rand.process(h_mean)
        for ev in out["events"]:
            if ev["type"] == "split":
                rand_splits += 1
            elif ev["type"] == "merge":
                rand_merges += 1
        if rand_max_cap_onset is None and int(out["n_cells"]) >= 64:
            rand_max_cap_onset = turn
        if turn % snapshot_every == 0 or turn == v14_turns - 1:
            rand_snapshots.append({
                "turn": turn,
                "n_cells": int(out["n_cells"]),
                "phi": float(out["phi"]),
            })
    rand_final_n = int(mitosis_rand.n_cells)
    rand_final_phi = float(rand_snapshots[-1]["phi"])
    rand_alpha = regress_alpha(rand_snapshots)
    print(
        f"V14 mirror: {v14_turns} turns, cells={rand_final_n}, Φ={rand_final_phi:.4f}, "
        f"splits={rand_splits}, α={rand_alpha:.3f}"
    )

    # V14 verdict at 1K and 3K turn (compare trained vs random at same trajectory length)
    v14_compare = {}
    for cmp_turn in [1000, 3000]:
        if cmp_turn > v14_turns:
            continue
        main_at = next(
            (s for s in snapshots if s["turn"] >= cmp_turn - snapshot_every),
            snapshots[-1],
        )
        rand_at = next(
            (s for s in rand_snapshots if s["turn"] >= cmp_turn - snapshot_every),
            rand_snapshots[-1],
        )
        violated = (rand_at["n_cells"] >= main_at["n_cells"]) and (
            rand_at["phi"] >= main_at["phi"] * 0.95
        )
        v14_compare[str(cmp_turn)] = {
            "trained": {"turn": main_at["turn"], "n_cells": main_at["n_cells"], "phi": main_at["phi"]},
            "random": {"turn": rand_at["turn"], "n_cells": rand_at["n_cells"], "phi": rand_at["phi"]},
            "v14_violated": violated,
        }
    v14_violated_overall = any(c["v14_violated"] for c in v14_compare.values())

    # ─── Cell specialty distribution ───
    # For each cell, determine top category share + dominant category
    specialty_summary = {}
    for cell_idx, cat_counts in cell_specialty.items():
        total = sum(cat_counts.values())
        if total == 0:
            continue
        sorted_cats = sorted(cat_counts.items(), key=lambda kv: -kv[1])
        top_cat, top_n = sorted_cats[0]
        specialty_summary[str(cell_idx)] = {
            "total_observations": total,
            "dominant_category": top_cat,
            "dominant_share": top_n / total,
            "category_distribution": {k: v / total for k, v in cat_counts.items()},
        }

    # Top 3 specialist cells per category
    cat_top_cells = {}
    for cat in PROMPTS.keys():
        per_cell_cat_counts = []
        for cell_idx, cat_counts in cell_specialty.items():
            if cat in cat_counts:
                per_cell_cat_counts.append((cell_idx, cat_counts[cat]))
        per_cell_cat_counts.sort(key=lambda x: -x[1])
        cat_top_cells[cat] = [
            {"cell_idx": int(idx), "count": int(c)} for idx, c in per_cell_cat_counts[:3]
        ]

    print("\nCell specialty (top 3 per category):")
    for cat, cells in cat_top_cells.items():
        if cells:
            top_str = ", ".join([f"cell{c['cell_idx']}={c['count']}" for c in cells])
            print(f"  {cat:18s}: {top_str}")

    # ─── Verdict (with α-over-time + Φ saturation) ───
    # PASS_FULL  — α ≥ 0.85 by 5K turn AND V14 미위반
    # PASS_PARTIAL — cells 8 → 64, α ≥ 0.6 (long-tail), V14 미위반
    # PARTIAL_α_PLATEAU — α plateau ~0.7 (F-LONG-2 hit) but mechanism healthy
    # FAIL_PHI_SAT — Φ slope ≤ 0 post-max-cap (F-LONG-3)
    # FAIL_V14    — random_init matches/exceeds trained
    F_LONG_1 = elapsed > 6 * 3600
    F_LONG_2 = (
        len(alpha_trajectory) >= 1
        and alpha_trajectory[-1]["turn"] >= min(5000, n_turns - 500)
        and not math.isnan(alpha_trajectory[-1]["alpha"])
        and alpha_trajectory[-1]["alpha"] < 0.75
    )
    F_LONG_3 = (
        phi_saturation is not None
        and phi_saturation["phi_max_post_cap"] < 3.5
        and abs(phi_saturation["phi_slope_per_turn"]) < 1e-5
    )
    F_LONG_4 = (
        max_cap_onset_turn is not None and final_n_cells == 64 and n_merges == 0 and n_splits <= 56
    )

    if not math.isnan(final_alpha) and final_alpha >= 0.85 and not v14_violated_overall:
        verdict = "PASS_HISTORICAL_RECOVERED"
    elif not math.isnan(final_alpha) and final_alpha >= 0.6 and final_n_cells >= 32 and not v14_violated_overall:
        verdict = "PARTIAL_PASS_MECHANISM"
    elif F_LONG_2:
        verdict = "PARTIAL_ALPHA_PLATEAU"
    elif F_LONG_3:
        verdict = "FAIL_PHI_SATURATED"
    elif v14_violated_overall:
        verdict = "FAIL_V14_VIOLATED"
    elif final_n_cells == 8:
        verdict = "FAIL_NO_GROWTH"
    elif math.isnan(final_alpha):
        verdict = "FAIL_PHI_FLAT"
    else:
        verdict = "PARTIAL_PASS"

    print(f"\n=== VERDICT: {verdict} ===")
    print(
        f"Falsifiers: F-LONG-1={F_LONG_1} F-LONG-2={F_LONG_2} F-LONG-3={F_LONG_3} F-LONG-4={F_LONG_4}"
    )

    # ─── Save result.json ───
    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "n_turns": n_turns,
        "seed": seed,
        "snapshot_every": snapshot_every,
        "alpha_window_every": alpha_window_every,
        "elapsed_sec": elapsed,
        "n_unique_prompts": len(ALL_PROMPTS),
        "prompt_categories": list(PROMPTS.keys()),
        "substrate": {
            "n_cells_init": 8,
            "c_dim": 12,
            "d_model": 32,
            "param_count": initial_param_count,
        },
        "mitosis_config": {
            "max_cells": 64,
            "split_patience": 3,
            "split_noise": 0.10,
            "merge_threshold": 0.005,
            "merge_patience": 30,
            "min_cells": 2,
            "lorenz_scale": 0.05,
        },
        "final": {
            "n_cells": final_n_cells,
            "phi": final_phi,
            "n_splits": n_splits,
            "n_merges": n_merges,
            "alpha_exponent_full": final_alpha,
        },
        "alpha_milestones": alpha_milestones,
        "alpha_trajectory": alpha_trajectory,
        "phi_saturation": phi_saturation,
        "v14_mirror": {
            "n_turns": v14_turns,
            "final_n_cells": rand_final_n,
            "final_phi": rand_final_phi,
            "splits": rand_splits,
            "merges": rand_merges,
            "alpha_exponent": rand_alpha,
            "max_cap_onset_turn": rand_max_cap_onset,
            "compare": v14_compare,
            "v14_violated_overall": v14_violated_overall,
        },
        "snapshots": snapshots,
        "rand_snapshots": rand_snapshots,
        "cell_specialty": {str(k): v for k, v in cell_specialty.items()},
        "specialty_summary": specialty_summary,
        "cat_top_cells": cat_top_cells,
        "falsifiers_hit": {
            "F_LONG_1_wallclock_6h": F_LONG_1,
            "F_LONG_2_alpha_plateau_5K": F_LONG_2,
            "F_LONG_3_phi_saturated": F_LONG_3,
            "F_LONG_4_specialization_stagnate": F_LONG_4,
        },
        "final_verdict": verdict,
        "honest_c3": [
            "Toy substrate (8c × 12d × d_model=32) — production 350M v5 결과는 별도 lane (BG-PHASE2-CKPT-INSTR). 본 실험은 메커니즘 검증만.",
            "Hash-based prompt encoding (sha256 → bytes → tensor) — real LLM tokenizer/embedding 과 다름. semantic 의미 없는 deterministic noise. anomaly 카테고리도 byte distribution 만 다를 뿐 의미 anomaly 검증 X.",
            "α exponent regression on snapshot points — n_cells max_cap 도달 후 cells 변동 X 면 추가 snapshot point 가 같은 x=log(64) 에 누적, regression slope 가 trivially 0 으로 수렴 → α 가 ★ 인공적으로 떨어질 가능성. mechanism level 결론 비교만 valid.",
            "V14 mirror random_init = 같은 mitosis 메커니즘 + 다른 seed substrate. 둘 다 randn → trained vs untrained 진짜 비교 X. Phase 2 cotrain ckpt 회수 후 재실험 필수.",
            "Lorenz autonomous chaos (σ=10, ρ=28) 가 cell tension 의 dominant driver — input diversity 보다 Lorenz inter-cell phase noise 가 split trigger 의 핵심. F-LONG-4 (specialization stagnate) false negative 가능.",
            "Φ proxy (cosine × log(n+1)) ceiling ≈ 8.34 (mean cos≤2 × log(65)≈4.17). historical IIT MI 51.131 (anima v2 stage 9) 와 직접 비교 X — metric scale 다름.",
            "process_count 누적 의존 — 매 run 시작 시 0 reset. 실제 serving 에선 checkpoint resume 메커니즘 별도 필요. (현 mitosis_v5_port 는 split_history 만 추적)",
            "cell_specialty 추적은 매 turn top-tension cell 만 기록 → softmax(tension) 가 매우 평탄하면 top_idx 가 거의 random. 'specialization' 결론은 정성적으로만 해석.",
            "10K turn 도 toy 한계 — 실제 production 에서 의식 emerge 검증은 350M cotrain ckpt + IIT formal Φ metric 필요.",
        ],
    }
    with (THIS_DIR / "result.json").open("w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nresult.json saved: {THIS_DIR / 'result.json'}")

    # ─── Plot α-over-time + Φ trajectory + cell trajectory ───
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(3, 1, figsize=(11, 12))
        turns = [s["turn"] for s in snapshots]
        cells = [s["n_cells"] for s in snapshots]
        phis = [s["phi"] for s in snapshots]

        # Panel 1: cells
        axes[0].plot(turns, cells, "b-", linewidth=1.4, label="trained substrate")
        axes[0].plot(
            [s["turn"] for s in rand_snapshots],
            [s["n_cells"] for s in rand_snapshots],
            "r--",
            linewidth=1.2,
            label=f"V14 random ({v14_turns} turn)",
        )
        if max_cap_onset_turn is not None:
            axes[0].axvline(max_cap_onset_turn, color="grey", linestyle=":", alpha=0.6,
                            label=f"max_cap onset @ turn {max_cap_onset_turn}")
        axes[0].set_xlabel("turn")
        axes[0].set_ylabel("n_cells")
        axes[0].set_title(f"Cell growth ({n_turns} turn, {len(ALL_PROMPTS)} unique prompts)")
        axes[0].legend()
        axes[0].grid(True, alpha=0.4)

        # Panel 2: Φ
        axes[1].plot(turns, phis, "b-", linewidth=1.2, label="trained Φ")
        axes[1].plot(
            [s["turn"] for s in rand_snapshots],
            [s["phi"] for s in rand_snapshots],
            "r--",
            linewidth=1.0,
            label="V14 random Φ",
        )
        if max_cap_onset_turn is not None:
            axes[1].axvline(max_cap_onset_turn, color="grey", linestyle=":", alpha=0.6)
        axes[1].set_xlabel("turn")
        axes[1].set_ylabel("Φ proxy (cos × log(n+1))")
        axes[1].set_title(f"Φ trajectory — verdict={verdict}, α(full)={final_alpha:.3f}")
        axes[1].legend()
        axes[1].grid(True, alpha=0.4)

        # Panel 3: α-over-time
        a_turns = [a["turn"] for a in alpha_trajectory if not math.isnan(a["alpha"])]
        a_vals = [a["alpha"] for a in alpha_trajectory if not math.isnan(a["alpha"])]
        if a_turns:
            axes[2].plot(a_turns, a_vals, "g-o", linewidth=1.4, markersize=4, label="α(t)")
            axes[2].axhline(0.93, color="purple", linestyle="--", alpha=0.6,
                            label="historical 0.93 (Cells64 v2)")
            axes[2].axhline(0.69, color="orange", linestyle=":", alpha=0.6,
                            label="3K smoke α=0.69 baseline")
            axes[2].axhline(0.40, color="brown", linestyle=":", alpha=0.4,
                            label="BG-PHI 0.40 (200 turn)")
        axes[2].set_xlabel("turn (window-end)")
        axes[2].set_ylabel("α exponent (log-log regression)")
        axes[2].set_title(
            f"α over time — sliding window every {alpha_window_every} turn"
        )
        axes[2].set_ylim(0.0, 1.2)
        axes[2].legend(loc="lower right")
        axes[2].grid(True, alpha=0.4)

        plt.tight_layout()
        plt.savefig(THIS_DIR / "alpha_over_time.png", dpi=80)
        print(f"plot saved: {THIS_DIR / 'alpha_over_time.png'}")
    except Exception as e:
        print(f"matplotlib skip: {e}")

    return result


if __name__ == "__main__":
    n_turns = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    print(f"=== anima clm v5-anima long-trajectory EXTENDED ({n_turns} turns) ===")
    run_experiment(n_turns=n_turns)
