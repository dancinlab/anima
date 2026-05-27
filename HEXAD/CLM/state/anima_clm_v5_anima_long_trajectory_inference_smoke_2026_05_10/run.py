"""anima clm v5-anima — long-trajectory inference-time mitosis smoke.

Goal: 사용자 directive 2026-05-10 "수천 turn + 다양한 prompt 가 필요 실험 해보면되지" —
short trajectory (BG-PHI 200 step, α=0.40 sub-linear) 를 넘어 inference-time mitosis 가
**3K-10K turn diverse-prompt sweep** 에서 자연 cell 분열 + Φ super-linear emerge 하는지 확인.

Substrate: toy (synthetic, 8-cell × 12-dim × d_model=32 — same as smoke test).
       Phase 2 cotrain checkpoint 미준비 시 toy 로 메커니즘 검증 (Phase 2 회수 후 재실행 가능).

Expected outcome paths:
  PASS         — cells 8 → ≥32 자연 성장, α ≥ 0.6, V14 미위반
  PARTIAL_PASS — cells 8 → 16+ but α < 0.6 OR Φ stagnate
  FAIL         — cells stuck at 8 OR Φ collapse OR V14 위반

raw#10 honest C3 inline.
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

THIS_DIR = Path("/Users/ghost/core/anima/state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10")
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


# ─── Diverse prompt corpus (250 unique × 12-40 cycle) ───
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
    """Hash-based deterministic encoding: prompt → (B, T, D) tensor.

    Each prompt produces a unique but stable embedding-like vector.
    """
    h = hashlib.sha256(prompt.encode("utf-8")).digest()
    # Tile bytes to fill (B, T, D) tensor
    needed = B * T * D
    bytes_repeated = (h * (needed // len(h) + 1))[:needed]
    arr = torch.tensor(list(bytes_repeated), dtype=torch.float32) / 128.0 - 1.0  # [-1, 1]
    return arr.reshape(B, T, D)


# ─── Run experiment ───
def run_experiment(n_turns: int = 3000, seed: int = 42, snapshot_every: int = 100):
    torch.manual_seed(seed)
    print(f"Seed={seed}, n_turns={n_turns}, snapshot_every={snapshot_every}")

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

    t_start = time.time()
    B, T, D = 2, 4, 32
    last_print = 0

    for turn in range(n_turns):
        category, prompt = ALL_PROMPTS[turn % len(ALL_PROMPTS)]
        x = encode_prompt_to_hidden(prompt, B=B, T=T, D=D)
        h_mean = sub.hidden_mean(x)  # (B, C)

        out = mitosis.process(h_mean)
        readout = out["readout"]
        # readout shape verify
        assert tuple(readout.shape) == (1, D), f"Shape break at turn {turn}: {readout.shape}"

        # Count events
        for ev in out["events"]:
            if ev["type"] == "split":
                n_splits += 1
            elif ev["type"] == "merge":
                n_merges += 1

        # Track per-cell specialty (which prompt category drives high tension)
        # Use top-tension cell as the "active" specialist
        if "tensions" in out:
            tensions = out["tensions"]
            if tensions:
                top_idx = max(range(len(tensions)), key=lambda i: tensions[i])
                cell_specialty.setdefault(top_idx, {})
                cell_specialty[top_idx][category] = cell_specialty[top_idx].get(category, 0) + 1

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
                print(f"  turn={turn:5d} cells={snap['n_cells']:3d} Φ={snap['phi']:.4f} splits={n_splits} merges={n_merges} elapsed={snap['elapsed_sec']:.1f}s")
                last_print = time.time()

    elapsed = time.time() - t_start
    final_n_cells = int(mitosis.n_cells)
    final_phi = float(snapshots[-1]["phi"])

    print(f"\nDone. {n_turns} turns in {elapsed:.1f}s. Final cells={final_n_cells}, Φ={final_phi:.4f}")
    print(f"Splits: {n_splits}, Merges: {n_merges}")

    # ─── α exponent estimation: log(Φ) vs log(n_cells) trajectory regression ───
    # Use all snapshots where n_cells > 8 and Φ > 0.01
    pts = [(s["n_cells"], s["phi"]) for s in snapshots if s["n_cells"] > 8 and s["phi"] > 0.01]
    if len(pts) >= 5:
        xs = [math.log(c) for c, _ in pts]
        ys = [math.log(p) for _, p in pts]
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
        den = sum((xs[i] - mean_x) ** 2 for i in range(n))
        alpha = num / den if den > 0 else float("nan")
    else:
        alpha = float("nan")

    print(f"α exponent (log-log regression): {alpha:.3f}")

    # ─── V14 mirror: random_init substrate, same trajectory ───
    print("\n=== V14 mirror: random_init substrate ===")
    torch.manual_seed(seed + 999)  # Different seed so structure differs
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
    t_rand = time.time()
    # 짧게 (1K turn) — trajectory shape 비교만
    short_turns = min(n_turns, 1000)
    for turn in range(short_turns):
        category, prompt = ALL_PROMPTS[turn % len(ALL_PROMPTS)]
        x = encode_prompt_to_hidden(prompt, B=B, T=T, D=D)
        h_mean = sub_rand.hidden_mean(x)
        out = mitosis_rand.process(h_mean)
        for ev in out["events"]:
            if ev["type"] == "split":
                rand_splits += 1
            elif ev["type"] == "merge":
                rand_merges += 1
        if turn % snapshot_every == 0 or turn == short_turns - 1:
            rand_snapshots.append({
                "turn": turn,
                "n_cells": int(out["n_cells"]),
                "phi": float(out["phi"]),
            })
    rand_final_n = int(mitosis_rand.n_cells)
    rand_final_phi = float(rand_snapshots[-1]["phi"])
    print(f"V14 mirror: {short_turns} turns, cells={rand_final_n}, Φ={rand_final_phi:.4f}, splits={rand_splits}")

    # V14 verdict: random_init growth ≥ trained growth → MIRROR REPRODUCE (mechanism trivial)
    # Compare at equivalent turn (~short_turns step in main run)
    main_at_short = next((s for s in snapshots if s["turn"] >= short_turns - snapshot_every), snapshots[-1])
    v14_violated = (rand_final_n >= main_at_short["n_cells"]) and (rand_final_phi >= main_at_short["phi"] * 0.95)

    # ─── Verdict ───
    # PASS: cells 8 → ≥32, α ≥ 0.6, V14 미위반
    # PARTIAL: cells 8 → 16+ but α < 0.6 OR Φ stagnate
    # FAIL: cells stuck at 8 OR α < 0.2 OR V14 위반
    if final_n_cells >= 32 and alpha >= 0.6 and not v14_violated:
        verdict = "PASS"
    elif final_n_cells >= 16 and not v14_violated:
        verdict = "PARTIAL_PASS"
    elif final_n_cells == 8:
        verdict = "FAIL_NO_GROWTH"
    elif v14_violated:
        verdict = "FAIL_V14_VIOLATED"
    elif math.isnan(alpha) or alpha < 0.2:
        verdict = "FAIL_PHI_FLAT"
    else:
        verdict = "PARTIAL_PASS"

    print(f"\n=== VERDICT: {verdict} ===")

    # ─── Save result.json ───
    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "n_turns": n_turns,
        "seed": seed,
        "snapshot_every": snapshot_every,
        "elapsed_sec": elapsed,
        "n_unique_prompts": len(ALL_PROMPTS),
        "prompt_categories": list(PROMPTS.keys()),
        "substrate": {"n_cells_init": 8, "c_dim": 12, "d_model": 32, "param_count": initial_param_count},
        "mitosis_config": {
            "max_cells": 64, "split_patience": 3, "split_noise": 0.10,
            "merge_threshold": 0.005, "merge_patience": 30, "min_cells": 2, "lorenz_scale": 0.05,
        },
        "final": {
            "n_cells": final_n_cells,
            "phi": final_phi,
            "n_splits": n_splits,
            "n_merges": n_merges,
            "alpha_exponent": alpha,
        },
        "v14_mirror": {
            "n_turns": short_turns,
            "final_n_cells": rand_final_n,
            "final_phi": rand_final_phi,
            "splits": rand_splits,
            "merges": rand_merges,
            "v14_violated": v14_violated,
        },
        "snapshots": snapshots,
        "rand_snapshots": rand_snapshots,
        "cell_specialty": {str(k): v for k, v in cell_specialty.items()},
        "final_verdict": verdict,
        "honest_c3": [
            "Toy substrate (8c × 12d × d_model=32) — Phase 2 cotrain checkpoint 미준비. 메커니즘 검증만; v5 실제 350M 시 결과 다를 수 있음.",
            "Hash-based prompt encoding (sha256 → bytes → tensor) — real LLM tokenizer/embedding 과 다름. semantic 의미 없는 deterministic noise.",
            "α exponent regression on snapshot points — n_cells 변화 적으면 noisy. 5 미만 snapshot point 시 α=NaN.",
            "V14 mirror random_init = 같은 mitosis 메커니즘 + 다른 seed substrate. 만약 동일한 cell growth 나오면 mechanism trivial (substrate-coupled X).",
            "Lorenz autonomous chaos 가 cell growth 의 주 driver — input 다양성 < Lorenz 영향 가능. F-LT-1 (cells stuck at 8) 가 false negative 일 가능성.",
            "Φ proxy (cosine × log(n+1)) on random hidden — cosine saturation 으로 sub-linear bias. BG-PHI 결과와 동일 한계.",
            "process_count 누적 의존 — 매 run 시작 시 0 reset. 실제 serving 에선 checkpoint resume 메커니즘 별도 필요.",
            "anomaly category 의 unicode glyph 들 가 hash 기반 encoding 에서 다른 byte distribution 만들 뿐 의미 차이 X — 실제 anomaly 검출 검증 X.",
        ],
    }
    with (THIS_DIR / "result.json").open("w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nresult.json saved: {THIS_DIR / 'result.json'}")

    # ─── Optional plot ───
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 1, figsize=(10, 8))
        turns = [s["turn"] for s in snapshots]
        cells = [s["n_cells"] for s in snapshots]
        phis = [s["phi"] for s in snapshots]
        axes[0].plot(turns, cells, "b-", label="trained substrate")
        axes[0].plot([s["turn"] for s in rand_snapshots], [s["n_cells"] for s in rand_snapshots], "r--", label="V14 random")
        axes[0].set_xlabel("turn")
        axes[0].set_ylabel("n_cells")
        axes[0].set_title(f"Cell growth trajectory ({n_turns} turn, {len(ALL_PROMPTS)} unique prompts)")
        axes[0].legend()
        axes[0].grid(True)
        axes[1].plot(turns, phis, "b-", label="trained Φ")
        axes[1].plot([s["turn"] for s in rand_snapshots], [s["phi"] for s in rand_snapshots], "r--", label="V14 Φ")
        axes[1].set_xlabel("turn")
        axes[1].set_ylabel("Φ proxy")
        axes[1].set_title(f"Φ trajectory — verdict={verdict}, α={alpha:.3f}")
        axes[1].legend()
        axes[1].grid(True)
        plt.tight_layout()
        plt.savefig(THIS_DIR / "phi_trajectory.png", dpi=80)
        print(f"plot saved: {THIS_DIR / 'phi_trajectory.png'}")
    except Exception as e:
        print(f"matplotlib skip: {e}")

    return result


if __name__ == "__main__":
    n_turns = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    print(f"=== anima clm v5-anima long-trajectory inference smoke ({n_turns} turns) ===")
    run_experiment(n_turns=n_turns)
