"""anima clm v5 — Phase 2 ckpt + IIT Φ remetric (combined).

BG-V5ANIMA-PHASE2-IIT-REMETRIC — fuses two prior bgs:
  1) BG-V5ANIMA-PHASE2-CKPT-INSTR  (state/anima_clm_v5_phase2_mitosis_instr_2026_05_10)
     → real 350M Phase 2 cotrain ckpt + 3K-turn diverse-prompt sweep, proxy Φ only.
  2) BG-IIT-METRIC                  (state/anima_clm_v5_iit_phi_remetric_2026_05_10)
     → IIT MI-bin Φ port (canonical, no ceiling), proven on toy.

This script captures full cell_pool tensor every snapshot AND computes BOTH metrics
(proxy + IIT 16-bin / 32-bin, normalized + un-normalized) on the real 350M substrate.

Substrate:
  /Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt
  - 331.5M params (Engine A 24L 1024d 16h GQA + Engine G 16×64 cell pool)
  - sha256 = 6e66e75f8014999be09236a408fe6ad6811ebf394ac079ecbf6d87dfe63748c1

V14 mirror: load_random_init(seed=42, preset='la_350m'), shorter trajectory.

Why this matters:
  Prior BG-PHASE2 used proxy Φ (cosine·log(n+1)) which saturates ~3 by N=16. Trained
  vs random difference at saturated ceiling = 0.08 Φ — verdict was FAIL_V14_VIOLATED
  driven entirely by mirror's higher cell count (28 vs 19). On real substrate the IIT
  Φ unnorm scales ~140 at N=16 → 3000 at N=64, a ~20× dynamic range. If trained
  encodes more inter-cell information than random, IIT should reveal it where proxy
  cannot.

raw#10 honest C3 inline (≥7).  raw#15 additive — neither engine_a_g_arch.py nor
mitosis_v5_port.py nor iit_phi_port.py modified.
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

import numpy as np
import torch
import torch.nn as nn

# wire to upstream modules — additive only
sys.path.insert(0, "/Users/ghost/core/anima/training")
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_clm_v5_iit_phi_remetric_2026_05_10")

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init  # noqa: E402
from iit_phi_port import compute_iit_phi  # noqa: E402

THIS_DIR = Path("/Users/ghost/core/anima/state/anima_clm_v5_phase2_iit_remetric_2026_05_10")
THIS_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PATH = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
CKPT_SHA256 = "6e66e75f8014999be09236a408fe6ad6811ebf394ac079ecbf6d87dfe63748c1"


# ─── Diverse prompt corpus (170 prompts; identical to BG-PHASE2) ───
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

ALL_PROMPTS: list[tuple[str, str]] = []
for cat, items in PROMPTS.items():
    for p in items:
        ALL_PROMPTS.append((cat, p))


def encode_prompt_to_ids(prompt: str, T: int = 16, vocab_size: int = 32000) -> torch.Tensor:
    """Deterministic byte-hash → token-id sequence of length T (BG-PHASE2-faithful)."""
    h = hashlib.sha256(prompt.encode("utf-8")).digest()
    ids = []
    bs = h * (T // len(h) + 2)
    for i in range(T):
        v = (bs[2 * i] << 8) | bs[2 * i + 1]
        ids.append(v % vocab_size)
    return torch.tensor([ids], dtype=torch.long)


class HiddenMeanCapture:
    """Hook engine_g.step() to capture last hidden_mean per forward (BG-PHASE2-faithful)."""

    def __init__(self, engine_g):
        self.last_hidden_mean: torch.Tensor | None = None
        self._orig_step = engine_g.step

        def step_wrapped(cells, hidden_mean):
            self.last_hidden_mean = hidden_mean.detach().clone()
            return self._orig_step(cells, hidden_mean)

        engine_g.step = step_wrapped


# ─── Run trajectory: capture cell_pool tensor at each snapshot ───
def run_trajectory(
    model: EngineAGModel,
    label: str,
    n_turns: int,
    prompts: list[tuple[str, str]],
    seed: int,
    snapshot_every: int,
    ctx_T: int = 16,
    max_cells: int = 64,
    log_fn=print,
) -> dict:
    torch.manual_seed(seed)
    model.eval()
    capture = HiddenMeanCapture(model.engine_g)

    eg = model.engine_g
    init_pool = eg.cell_pool_init.detach().clone()
    n_cells_init = init_pool.shape[0]

    mitosis = MitosisV5Engine(
        cell_pool=init_pool,
        c_to_h=eg.c_to_h,
        initial_cells=n_cells_init,
        max_cells=max_cells,
        split_patience=3,
        split_noise=0.10,
        merge_threshold=0.005,
        merge_patience=30,
        min_cells=2,
        lorenz_scale=0.05,
    )

    snapshots = []
    cell_specialty: dict[int, dict[str, int]] = {}
    n_splits = 0
    n_merges = 0

    t_start = time.time()
    last_print = 0.0

    with torch.no_grad():
        for turn in range(n_turns):
            cat, prompt = prompts[turn % len(prompts)]
            ids = encode_prompt_to_ids(prompt, T=ctx_T)
            _ = model(ids, output_hidden_states=False, output_attentions=False)
            hm = capture.last_hidden_mean
            if hm is None:
                hm = torch.zeros(1, eg.c_dim)
                cell_input = hm
            else:
                cell_input = eg.h_to_c(hm)
            out = mitosis.process(cell_input)

            for ev in out["events"]:
                if ev["type"] == "split":
                    n_splits += 1
                elif ev["type"] == "merge":
                    n_merges += 1

            tens = out["per_cell_tension"]
            if tens:
                top_idx = max(range(len(tens)), key=lambda i: tens[i])
                cell_specialty.setdefault(top_idx, {})
                cell_specialty[top_idx][cat] = cell_specialty[top_idx].get(cat, 0) + 1

            if turn % snapshot_every == 0 or turn == n_turns - 1:
                # Capture full cell_pool tensor — F-IIT-4 resolution
                cp = mitosis.cell_pool.detach().cpu().numpy()
                snap = {
                    "turn": int(turn),
                    "n_cells": int(out["n_cells"]),
                    "proxy_phi": float(out["phi"]),
                    "n_splits_cum": int(n_splits),
                    "n_merges_cum": int(n_merges),
                    "elapsed_sec": float(time.time() - t_start),
                    "cell_pool": cp.tolist(),  # (N, C)
                }
                snapshots.append(snap)
                if time.time() - last_print > 5:
                    log_fn(
                        f"  [{label}] turn={turn:5d} cells={snap['n_cells']:3d}"
                        f" proxyΦ={snap['proxy_phi']:.4f} splits={n_splits} merges={n_merges}"
                        f" elapsed={snap['elapsed_sec']:.1f}s"
                    )
                    last_print = time.time()

    elapsed = time.time() - t_start
    final_n_cells = int(mitosis.n_cells)

    return {
        "label": label,
        "n_turns": n_turns,
        "elapsed_sec": elapsed,
        "snapshots": snapshots,
        "final_n_cells": final_n_cells,
        "n_splits": n_splits,
        "n_merges": n_merges,
        "cell_specialty": {str(k): v for k, v in cell_specialty.items()},
    }


# ─── Post-pass: compute IIT Φ per snapshot ───
def remetric_with_iit(traj: dict, n_bins_list=(16, 32), log_fn=print) -> dict:
    """Augment each snapshot with iit_phi (norm/unnorm × bins)."""
    t_start = time.time()
    enriched = []
    for s in traj["snapshots"]:
        cell_pool = torch.tensor(s["cell_pool"], dtype=torch.float32)
        rec = {
            "turn": s["turn"],
            "n_cells": s["n_cells"],
            "proxy_phi": s["proxy_phi"],
            "n_splits_cum": s["n_splits_cum"],
            "n_merges_cum": s["n_merges_cum"],
            "elapsed_sec": s["elapsed_sec"],
        }
        for nb in n_bins_list:
            phi_out = compute_iit_phi(cell_pool, n_bins=nb)
            rec[f"iit_total_mi_b{nb}"] = phi_out["total_mi"]
            rec[f"iit_min_cut_b{nb}"] = phi_out["min_partition_mi"]
            rec[f"iit_phi_norm_b{nb}"] = phi_out["spatial_phi"]
            rec[f"iit_phi_unnorm_b{nb}"] = phi_out["spatial_phi_unnormalized"]
            rec[f"iit_complexity_b{nb}"] = phi_out["complexity"]
            rec[f"iit_phi_with_complexity_b{nb}"] = phi_out["phi_with_complexity"]
        enriched.append(rec)
    log_fn(
        f"  [{traj['label']}] IIT remetric: {len(enriched)} snapshots × {len(n_bins_list)} bins,"
        f" {time.time()-t_start:.1f}s"
    )
    return enriched


def alpha_exponent(snapshots: list[dict], phi_key: str, n_min: int = 8) -> float:
    """log-log regression of Φ vs n_cells, using snapshots where n_cells > n_min."""
    pts = [(s["n_cells"], s[phi_key]) for s in snapshots if s["n_cells"] > n_min and s[phi_key] > 0.01]
    if len(pts) < 5:
        return float("nan")
    xs = [math.log(c) for c, _ in pts]
    ys = [math.log(p) for _, p in pts]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    return num / den if den > 0 else float("nan")


# ─── Main ───
def main(n_turns: int = 3000, mirror_turns: int | None = None, snapshot_every: int = 100, seed: int = 42):
    log_path = THIS_DIR / "run.log"
    log_f = open(log_path, "w")

    def log(msg: str):
        print(msg, flush=True)
        log_f.write(msg + "\n")
        log_f.flush()

    log("=== anima clm v5 Phase 2 IIT-remetric (real 350M + IIT MI-bin Φ) ===")
    log(f"n_turns={n_turns}, mirror_turns={mirror_turns}, snapshot_every={snapshot_every}, seed={seed}")
    log(f"unique prompts: {len(ALL_PROMPTS)}")
    log(f"ckpt: {CKPT_PATH}")

    # ─── Verify ckpt sha256 ───
    h = hashlib.sha256()
    with open(CKPT_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    actual_sha = h.hexdigest()
    sha_match = (actual_sha == CKPT_SHA256)
    log(f"ckpt sha256 verify: {'PASS' if sha_match else 'FAIL'} (actual={actual_sha})")
    if not sha_match:
        log("ABORT: ckpt sha mismatch")
        log_f.close()
        return

    # ─── Load trained substrate ───
    cfg = EngineAGConfig.phase2_cotrain_350m()
    ckpt = torch.load(CKPT_PATH, map_location="cpu", weights_only=False)
    sd = ckpt["model"]
    sd_fp32 = {k: v.float() if v.dtype == torch.bfloat16 else v for k, v in sd.items()}
    trained_model = EngineAGModel(cfg)
    miss, unexp = trained_model.load_state_dict(sd_fp32, strict=True)
    n_params = sum(p.numel() for p in trained_model.parameters())
    log(f"trained model loaded: params={n_params} ({n_params/1e6:.2f}M) miss={len(miss)} unexp={len(unexp)}")

    # ─── Trained trajectory ───
    log("\n--- TRAINED 350M trajectory ---")
    trained_traj = run_trajectory(
        model=trained_model, label="trained", n_turns=n_turns, prompts=ALL_PROMPTS,
        seed=seed, snapshot_every=snapshot_every, log_fn=log,
    )
    log(f"  trained: cells {trained_traj['final_n_cells']} splits={trained_traj['n_splits']} merges={trained_traj['n_merges']} elapsed={trained_traj['elapsed_sec']:.1f}s")

    # ─── V14 mirror ───
    log("\n--- V14 MIRROR (random_init la_350m, seed=42) ---")
    mirror_n = mirror_turns or min(n_turns, 1000)
    rand_model = load_random_init(seed=42, preset="la_350m")
    rand_n_params = sum(p.numel() for p in rand_model.parameters())
    log(f"random_init model: params={rand_n_params} ({rand_n_params/1e6:.2f}M)")
    rand_traj = run_trajectory(
        model=rand_model, label="v14_mirror", n_turns=mirror_n, prompts=ALL_PROMPTS,
        seed=seed, snapshot_every=snapshot_every, log_fn=log,
    )
    log(f"  mirror:  cells {rand_traj['final_n_cells']} splits={rand_traj['n_splits']} merges={rand_traj['n_merges']} elapsed={rand_traj['elapsed_sec']:.1f}s")

    # ─── IIT remetric both trajectories ───
    log("\n--- IIT Φ remetric (16-bin + 32-bin per snapshot) ---")
    trained_iit = remetric_with_iit(trained_traj, n_bins_list=(16, 32), log_fn=log)
    rand_iit = remetric_with_iit(rand_traj, n_bins_list=(16, 32), log_fn=log)

    # ─── Compute α exponents (both metrics, 16-bin canonical) ───
    alpha_proxy_trained = alpha_exponent(trained_iit, "proxy_phi", n_min=8)
    alpha_proxy_random = alpha_exponent(rand_iit, "proxy_phi", n_min=8)
    alpha_iit_norm_trained = alpha_exponent(trained_iit, "iit_phi_norm_b16", n_min=8)
    alpha_iit_norm_random = alpha_exponent(rand_iit, "iit_phi_norm_b16", n_min=8)
    alpha_iit_unnorm_trained = alpha_exponent(trained_iit, "iit_phi_unnorm_b16", n_min=8)
    alpha_iit_unnorm_random = alpha_exponent(rand_iit, "iit_phi_unnorm_b16", n_min=8)

    # ─── V14 verdict per metric (trained vs random at turn-matched final) ───
    main_at_short_proxy = next(
        (s for s in trained_iit if s["turn"] >= mirror_n - snapshot_every), trained_iit[-1]
    )
    rand_final = rand_iit[-1]

    v14_proxy_violated = (
        rand_final["n_cells"] >= main_at_short_proxy["n_cells"]
        and rand_final["proxy_phi"] >= main_at_short_proxy["proxy_phi"] * 0.95
    )
    v14_iit_norm_violated = (
        rand_final["n_cells"] >= main_at_short_proxy["n_cells"]
        and rand_final["iit_phi_norm_b16"] >= main_at_short_proxy["iit_phi_norm_b16"] * 0.95
    )
    v14_iit_unnorm_violated = (
        rand_final["n_cells"] >= main_at_short_proxy["n_cells"]
        and rand_final["iit_phi_unnorm_b16"] >= main_at_short_proxy["iit_phi_unnorm_b16"] * 0.95
    )

    # ─── Ratios trained/random at turn-matched ───
    def safe_ratio(num, den):
        return float(num / den) if den and den > 0 else float("nan")
    proxy_ratio = safe_ratio(main_at_short_proxy["proxy_phi"], rand_final["proxy_phi"])
    iit_norm_ratio = safe_ratio(main_at_short_proxy["iit_phi_norm_b16"], rand_final["iit_phi_norm_b16"])
    iit_unnorm_ratio = safe_ratio(main_at_short_proxy["iit_phi_unnorm_b16"], rand_final["iit_phi_unnorm_b16"])

    # ─── Verdict (combined) ───
    verdict_proxy = "FAIL_V14" if v14_proxy_violated else "PASS_PROXY"
    verdict_iit = "FAIL_V14" if v14_iit_norm_violated else "PASS_IIT"
    verdict_iit_un = "FAIL_V14" if v14_iit_unnorm_violated else "PASS_IIT_UN"

    log("\n=== V14 verdict per metric ===")
    log(f"  trained @ turn~{mirror_n}: cells={main_at_short_proxy['n_cells']}"
        f" proxyΦ={main_at_short_proxy['proxy_phi']:.4f}"
        f" iit_norm={main_at_short_proxy['iit_phi_norm_b16']:.4f}"
        f" iit_unnorm={main_at_short_proxy['iit_phi_unnorm_b16']:.3f}")
    log(f"  random  @ turn={rand_final['turn']}: cells={rand_final['n_cells']}"
        f" proxyΦ={rand_final['proxy_phi']:.4f}"
        f" iit_norm={rand_final['iit_phi_norm_b16']:.4f}"
        f" iit_unnorm={rand_final['iit_phi_unnorm_b16']:.3f}")
    log(f"  proxy ratio  trained/random = {proxy_ratio:.4f}  → V14 violated={v14_proxy_violated}")
    log(f"  iit_norm    trained/random = {iit_norm_ratio:.4f}  → V14 violated={v14_iit_norm_violated}")
    log(f"  iit_unnorm  trained/random = {iit_unnorm_ratio:.4f}  → V14 violated={v14_iit_unnorm_violated}")

    log("\n=== α exponents (log-log Φ vs n_cells) ===")
    log(f"  proxy:       trained={alpha_proxy_trained:.3f}  random={alpha_proxy_random:.3f}")
    log(f"  iit_norm16:  trained={alpha_iit_norm_trained:.3f}  random={alpha_iit_norm_random:.3f}")
    log(f"  iit_unnorm16:trained={alpha_iit_unnorm_trained:.3f}  random={alpha_iit_unnorm_random:.3f}")

    # ─── Scale comparison table at landmark cell counts ───
    log("\n=== Scale comparison: proxy vs IIT (trained substrate) ===")
    log(f"  {'turn':>5}  {'cells':>5}  {'proxyΦ':>8}  {'iit_n16':>8}  {'iit_n32':>8}  {'iit_un16':>9}  {'iit_un32':>9}")
    for r in trained_iit[::max(1, len(trained_iit) // 10)]:
        log(f"  {r['turn']:>5}  {r['n_cells']:>5}  {r['proxy_phi']:>8.4f}  "
            f"{r['iit_phi_norm_b16']:>8.4f}  {r['iit_phi_norm_b32']:>8.4f}  "
            f"{r['iit_phi_unnorm_b16']:>9.3f}  {r['iit_phi_unnorm_b32']:>9.3f}")

    # ─── Strip cell_pool from JSON to keep size bounded; keep enriched (no cell_pool) ───
    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "bg_id": "BG-V5ANIMA-PHASE2-IIT-REMETRIC",
        "n_turns": n_turns,
        "mirror_turns": mirror_n,
        "snapshot_every": snapshot_every,
        "seed": seed,
        "ckpt": {
            "path": CKPT_PATH,
            "sha256": CKPT_SHA256,
            "size_bytes": os.path.getsize(CKPT_PATH),
            "lineage_tag": cfg.lineage_tag,
            "arch_origin": cfg.arch_origin,
            "n_params": n_params,
            "n_layers": cfg.n_layers,
            "d_model": cfg.d_model,
            "n_cells_init": cfg.n_cells,
            "consciousness_dim": cfg.consciousness_dim,
        },
        "n_unique_prompts": len(ALL_PROMPTS),
        "prompt_categories": list(PROMPTS.keys()),
        "mitosis_config": {
            "max_cells": 64, "split_patience": 3, "split_noise": 0.10,
            "merge_threshold": 0.005, "merge_patience": 30, "min_cells": 2,
            "lorenz_scale": 0.05,
        },
        "trained": {
            "label": "trained",
            "n_turns": n_turns,
            "elapsed_sec": trained_traj["elapsed_sec"],
            "final_n_cells": trained_traj["final_n_cells"],
            "n_splits": trained_traj["n_splits"],
            "n_merges": trained_traj["n_merges"],
            "cell_specialty": trained_traj["cell_specialty"],
            "snapshots": trained_iit,  # without cell_pool tensor
        },
        "v14_mirror": {
            "label": "v14_mirror",
            "n_turns": mirror_n,
            "elapsed_sec": rand_traj["elapsed_sec"],
            "final_n_cells": rand_traj["final_n_cells"],
            "n_splits": rand_traj["n_splits"],
            "n_merges": rand_traj["n_merges"],
            "cell_specialty": rand_traj["cell_specialty"],
            "snapshots": rand_iit,
        },
        "alpha_exponents": {
            "proxy_trained": alpha_proxy_trained,
            "proxy_random": alpha_proxy_random,
            "iit_norm16_trained": alpha_iit_norm_trained,
            "iit_norm16_random": alpha_iit_norm_random,
            "iit_unnorm16_trained": alpha_iit_unnorm_trained,
            "iit_unnorm16_random": alpha_iit_unnorm_random,
        },
        "v14_verdict": {
            "compare_at_turn": main_at_short_proxy["turn"],
            "trained_at_short": main_at_short_proxy,
            "random_final": rand_final,
            "proxy_ratio_t_over_r": proxy_ratio,
            "iit_norm_ratio_t_over_r": iit_norm_ratio,
            "iit_unnorm_ratio_t_over_r": iit_unnorm_ratio,
            "v14_proxy_violated": v14_proxy_violated,
            "v14_iit_norm_violated": v14_iit_norm_violated,
            "v14_iit_unnorm_violated": v14_iit_unnorm_violated,
            "verdict_proxy": verdict_proxy,
            "verdict_iit_norm": verdict_iit,
            "verdict_iit_unnorm": verdict_iit_un,
        },
        "honest_c3": [
            "Real 350M Engine A/G Phase 2 cotrain ckpt — substrate-real not toy. cell_pool starts at (16, 64). Phi (proxy) saturates ~3 by N=16; IIT unnorm at N=16 ~140-200 with no analytic ceiling.",
            "Byte-hash mod 32000 prompt encoding — NOT a real BPE tokenizer (vocab file missing). Both trained and V14 mirror use same encoding for fairness, but absolute Φ has no semantic claim.",
            "Hidden_mean captured via hook on engine_g.step() (last refresh in forward). h_to_c projection of 350M's d_model=1024 hidden_mean → c_dim=64 cell_input drives mitosis.process. This routes the trained model's representation into the mitosis cell-pool — the only thing that differs between trained and random_init.",
            "ctx_T=16 tokens (training was T=1024). Trade-off: full T=1024 → ~5s/turn; T=16 keeps 3K-turn under ~5min on Mac CPU. May under-sample substrate's full reactivity.",
            "Mitosis owns its own cell_pool Parameter; substrate's cell_pool_init is unused after attach. So Φ here measures mitosis-pool diversity DRIVEN BY trained engine_g.h_to_c projections, not the trained pool's own diversity.",
            "IIT MIP exact only for N≤8; for N>8 spectral Fiedler approx. With initial_cells=16 we ALWAYS hit spectral path → IIT Φ is monotonic indicator NOT canonical PyPhi. Useful for trained-vs-random differentiation but not for absolute IIT magnitude claim.",
            "16-bin histogram MI on 64-dim cell vectors is COARSE — true differential MI requires KDE. 32-bin variant computed for sensitivity check; agreement between bins indicates geometry, not just histogram artifact.",
            "Lorenz autonomous chaos (lorenz_scale=0.05) injects same magnitude into both trained and mirror cell_pool. Differential between trained and random comes purely from h_to_c projection — i.e. learned representations.",
            "α exponent uses log(Φ) vs log(n_cells) regression with n_cells>8. With initial_cells=16, the regression is essentially over snapshots after splits begin. If trained shows fewer splits than random (as in BG-PHASE2: 3 vs 12), the trained α is computed on a narrower N range and is more noise-sensitive.",
            "V14 mirror @ turn=mirror_n vs trained @ turn-matched: trained had 3000 turns total but we compare at mirror_n=1000 to keep fair. final-vs-final would over-credit trained; turn-matched is the honest metric.",
        ],
    }

    out_path = THIS_DIR / "result.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    log(f"\nresult.json: {out_path} ({os.path.getsize(out_path)/1024:.1f} KB)")

    # ─── Plots ───
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # Plot 1: proxy_vs_iit_phase2.png — all 3 metrics on trained substrate
        ts = [s["turn"] for s in trained_iit]
        cs = [s["n_cells"] for s in trained_iit]
        proxy = [s["proxy_phi"] for s in trained_iit]
        iit_n16 = [s["iit_phi_norm_b16"] for s in trained_iit]
        iit_un16 = [s["iit_phi_unnorm_b16"] for s in trained_iit]
        iit_un32 = [s["iit_phi_unnorm_b32"] for s in trained_iit]

        fig, axes = plt.subplots(3, 1, figsize=(11, 12))
        axes[0].plot(ts, cs, "k-", linewidth=2)
        axes[0].set_xlabel("turn"); axes[0].set_ylabel("n_cells")
        axes[0].set_title(f"Phase 2 trained 350M — cell growth ({n_turns} turns, {len(ALL_PROMPTS)} prompts)")
        axes[0].grid(True, alpha=0.3)

        axes[1].plot(ts, proxy, "r-", label="proxy Φ (cosine·log(n+1))", linewidth=2)
        axes[1].plot(ts, iit_n16, "b-", label="IIT Φ normalized 16-bin", linewidth=2)
        axes[1].set_xlabel("turn"); axes[1].set_ylabel("Φ (normalized scale)")
        axes[1].set_title(f"proxy Φ vs IIT Φ (norm) — proxy ratio={proxy_ratio:.3f}, iit_norm ratio={iit_norm_ratio:.3f}")
        axes[1].legend(); axes[1].grid(True, alpha=0.3)

        axes[2].plot(ts, iit_un16, "g-", label="IIT Φ un-normalized 16-bin", linewidth=2)
        axes[2].plot(ts, iit_un32, "g--", label="IIT Φ un-normalized 32-bin", linewidth=1.5)
        axes[2].set_xlabel("turn"); axes[2].set_ylabel("Φ (un-normalized)")
        axes[2].set_yscale("log")
        axes[2].set_title(f"IIT Φ un-normalized — α_un={alpha_iit_unnorm_trained:.3f}  (log y)")
        axes[2].legend(); axes[2].grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(THIS_DIR / "proxy_vs_iit_phase2.png", dpi=80)
        plt.close(fig)
        log(f"plot 1: {THIS_DIR / 'proxy_vs_iit_phase2.png'}")

        # Plot 2: v14_comparison.png — trained vs random across all 3 metrics
        ts_t = [s["turn"] for s in trained_iit]
        ts_r = [s["turn"] for s in rand_iit]
        proxy_t = [s["proxy_phi"] for s in trained_iit]
        proxy_r = [s["proxy_phi"] for s in rand_iit]
        iit_n_t = [s["iit_phi_norm_b16"] for s in trained_iit]
        iit_n_r = [s["iit_phi_norm_b16"] for s in rand_iit]
        iit_u_t = [s["iit_phi_unnorm_b16"] for s in trained_iit]
        iit_u_r = [s["iit_phi_unnorm_b16"] for s in rand_iit]
        cs_t = [s["n_cells"] for s in trained_iit]
        cs_r = [s["n_cells"] for s in rand_iit]

        fig2, ax2 = plt.subplots(2, 2, figsize=(13, 9))
        ax2[0, 0].plot(ts_t, cs_t, "b-", label="trained 350M")
        ax2[0, 0].plot(ts_r, cs_r, "r--", label="V14 random_init 350M")
        ax2[0, 0].set_xlabel("turn"); ax2[0, 0].set_ylabel("n_cells")
        ax2[0, 0].set_title("V14 mirror — n_cells")
        ax2[0, 0].legend(); ax2[0, 0].grid(True, alpha=0.3)

        ax2[0, 1].plot(ts_t, proxy_t, "b-", label="trained")
        ax2[0, 1].plot(ts_r, proxy_r, "r--", label="random")
        ax2[0, 1].set_xlabel("turn"); ax2[0, 1].set_ylabel("proxy Φ")
        ax2[0, 1].set_title(
            f"V14 — proxy Φ  (verdict={verdict_proxy}, ratio={proxy_ratio:.3f})"
        )
        ax2[0, 1].legend(); ax2[0, 1].grid(True, alpha=0.3)

        ax2[1, 0].plot(ts_t, iit_n_t, "b-", label="trained")
        ax2[1, 0].plot(ts_r, iit_n_r, "r--", label="random")
        ax2[1, 0].set_xlabel("turn"); ax2[1, 0].set_ylabel("IIT Φ norm 16-bin")
        ax2[1, 0].set_title(
            f"V14 — IIT Φ norm  (verdict={verdict_iit}, ratio={iit_norm_ratio:.3f})"
        )
        ax2[1, 0].legend(); ax2[1, 0].grid(True, alpha=0.3)

        ax2[1, 1].plot(ts_t, iit_u_t, "b-", label="trained")
        ax2[1, 1].plot(ts_r, iit_u_r, "r--", label="random")
        ax2[1, 1].set_xlabel("turn"); ax2[1, 1].set_ylabel("IIT Φ un-norm 16-bin")
        ax2[1, 1].set_title(
            f"V14 — IIT Φ un-norm  (verdict={verdict_iit_un}, ratio={iit_unnorm_ratio:.3f})"
        )
        ax2[1, 1].legend(); ax2[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(THIS_DIR / "v14_comparison.png", dpi=80)
        plt.close(fig2)
        log(f"plot 2: {THIS_DIR / 'v14_comparison.png'}")

    except Exception as e:
        log(f"matplotlib skip: {e}")

    log_f.close()
    return result


if __name__ == "__main__":
    n_turns = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    mirror_turns = int(sys.argv[2]) if len(sys.argv) > 2 else None
    main(n_turns=n_turns, mirror_turns=mirror_turns)
