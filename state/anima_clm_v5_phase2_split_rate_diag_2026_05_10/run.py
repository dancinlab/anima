"""anima clm v5 — Phase 2 split-rate diagnostic (BG-REAL350M-IIT follow-up).

BG-V5ANIMA-PHASE2-SPLIT-RATE-DIAG (cycle 2026-05-10) — diagnose WHY trained 350M
substrate suppresses mitosis split rate (3 vs random 12 in 1K turns) on cell pool.
The §22 finding (BG-V5ANIMA-PHASE2-IIT-REMETRIC) located the V14 violation in
split-rate, not per-cell info content. Cell 7 (700 hits) and cell 16 (537 hits)
became attractor bottlenecks — 1240 / 3000 = 41% of all turns assigned tension-max
to those two cells. This script tests three hypotheses:

  H1 attention-pull: trained `c_to_h` projection of hidden_mean lands near 1-2
                     cells, monopolizing tension and hiding others below threshold.
  H2 tension-scale:  trained tension magnitudes are smaller in absolute terms, so
                     adaptive mean+1.5σ also shrinks → no separation → no split.
  H3 concentration:  trained's high-tension is concentrated in 1-2 cells; the
                     adaptive threshold (mean+1.5σ) chases those cells but
                     split_patience=3 consecutive is rarely met by other cells.

Five ablations (1K turns each, 170-prompt corpus, snapshot every 50):
  A1 lower split_threshold floor (mean+0.5σ instead of mean+1.5σ)
  A2 disable Lorenz (lorenz_scale=0)
  A3 disable attention-pull projection (cell_input = hm raw, no h_to_c)
  A4 alternate split trigger (cell_pool L2 dispersion variance instead of tension)
  A5 trained vs random per-cell tension distribution (histogram) — 1K turns each

raw#15 additive — neither engine_a_g_arch.py nor mitosis_v5_port.py modified.
raw#10 honest C3 inline ≥7. $0 Mac CPU. /Users/ghost/.hx/bin/python3.
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

sys.path.insert(0, "/Users/ghost/core/anima/training")
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_clm_v5_iit_phi_remetric_2026_05_10")

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init  # noqa: E402
from iit_phi_port import compute_iit_phi  # noqa: E402

THIS_DIR = Path("/Users/ghost/core/anima/state/anima_clm_v5_phase2_split_rate_diag_2026_05_10")
THIS_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PATH = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
CKPT_SHA256 = "6e66e75f8014999be09236a408fe6ad6811ebf394ac079ecbf6d87dfe63748c1"

# ─── Reuse §22 prompt corpus (170 prompts identical) ─────────────
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
        "What is the integral of sine x", "Compute the determinant of a two by two matrix",
        "What is Euler's identity", "Define a topological space", "What is a Hilbert space",
        "Explain Bayes theorem", "What is the central limit theorem",
        "Define entropy in information theory", "What is mutual information",
        "Explain Fourier transform", "What is a Markov chain", "Define a manifold",
        "What is the Riemann hypothesis", "Explain Godel's incompleteness theorem",
        "What is the Lebesgue measure", "Define a group in algebra",
        "What is a ring homomorphism", "Explain spectral decomposition",
        "What is a category in mathematics", "Define the gradient operator",
        "What is the Laplacian", "Explain stochastic differential equations",
        "What is principal component analysis", "Define eigenvalue and eigenvector",
        "What is the curse of dimensionality", "Explain the Brouwer fixed point theorem",
        "What is a functor", "Define a tensor product",
    ],
    "en_code": [
        "Write a Python function for fibonacci", "Sort a list using quicksort",
        "Implement binary search", "What is recursion", "Explain dynamic programming",
        "Write a Python decorator", "Implement a linked list", "What is a hash table",
        "Explain BFS and DFS", "Write a Python generator", "Implement merge sort",
        "What is asynchronous programming", "Explain garbage collection",
        "Write a Python context manager", "Implement a binary tree",
        "What is dependency injection", "Explain MVC pattern", "Write a Python iterator",
        "Implement a stack and queue", "What is functional programming",
        "Explain monads briefly", "Write a regex for emails", "What is the GIL in Python",
        "Explain currying in functional programming",
        "Write a Python class with dunder methods", "Implement Dijkstra's algorithm",
        "What is the difference between TCP and UDP", "Explain RESTful APIs",
        "Write a SQL JOIN query", "Implement a least recently used cache",
    ],
    "en_music": [
        "What is counterpoint in music", "Explain Bach's fugue structure",
        "What is harmonic progression", "Define a chord inversion",
        "Explain modal music", "What is a cadence", "Define rhythm and meter",
        "What is polyphony", "Explain orchestration", "What is a leitmotif",
        "Explain the circle of fifths", "What is dissonance and consonance",
        "Define tonality and atonality", "What is a sonata form", "Explain syncopation",
        "What is jazz improvisation", "Define dynamics in music", "What is timbre",
        "Explain the equal temperament", "What is a key signature",
    ],
    "anomaly": [
        "█▓▒░xyzzy plugh xyzzy", "asdfgh qwerty zxcvbn", "ʇsǝʇ ɟo ʇɥǝ ʍɐʇǝɹ",
        "1q2w3e4r5t6y7u8i9o", "ABCDEF GHIJKL MNOPQR", "...!!!???***---+++",
        "[[deleted]]<<error>>", "𓀀 𓀁 𓀂 𓀃 𓀄 𓀅 𓀆", "🎲🎯🎴🎵🎶🎷🎸🎹",
        "ǝlqᴉssodɯᴉ ᴉs ǝʌol", "❤❤❤❤❤❤❤❤❤❤", "x" * 30, "0" * 30,
        "AAAA " * 6, "noise glitch error fail", "404 503 502 500 418",
        "stack overflow segfault", "TODO FIXME HACK XXX",
        "lorem ipsum dolor sit amet", "the quick brown fox jumps",
    ],
}

ALL_PROMPTS: list[tuple[str, str]] = []
for cat, items in PROMPTS.items():
    for p in items:
        ALL_PROMPTS.append((cat, p))


def encode_prompt_to_ids(prompt: str, T: int = 16, vocab_size: int = 32000) -> torch.Tensor:
    h = hashlib.sha256(prompt.encode("utf-8")).digest()
    ids = []
    bs = h * (T // len(h) + 2)
    for i in range(T):
        v = (bs[2 * i] << 8) | bs[2 * i + 1]
        ids.append(v % vocab_size)
    return torch.tensor([ids], dtype=torch.long)


class HiddenMeanCapture:
    def __init__(self, engine_g):
        self.last_hidden_mean: torch.Tensor | None = None
        self._orig_step = engine_g.step

        def step_wrapped(cells, hidden_mean):
            self.last_hidden_mean = hidden_mean.detach().clone()
            return self._orig_step(cells, hidden_mean)

        engine_g.step = step_wrapped


# ─── Mitosis variant subclasses (raw#15: subclass, do not modify port) ───

class MitosisV5_LowerThreshold(MitosisV5Engine):
    """A1: split_threshold = mean + 0.5σ instead of mean + 1.5σ."""

    def _update_adaptive_threshold(self):
        if len(self._global_tension_history) < 10:
            return
        recent = self._global_tension_history[-self.adaptive_window:]
        mean_t = sum(recent) / len(recent)
        var_t = sum((t - mean_t) ** 2 for t in recent) / len(recent)
        std_t = math.sqrt(var_t) if var_t > 0 else mean_t * 0.1
        self.split_threshold = max(mean_t + 0.5 * std_t, mean_t * 0.3)


class MitosisV5_DispersionTrigger(MitosisV5Engine):
    """A4: split when cell_pool L2 dispersion variance is HIGH (vs tension recent).

    A cell becomes split candidate if its row contributes disproportionately to the
    pool's pairwise dispersion (i.e., it's an outlier in geometry rather than in
    tension-vs-hidden_mean). Combines with regular tension floor as fallback.
    """

    def _check_splits(self, per_cell_tensions):
        events = []
        if self.n_cells >= self.max_cells:
            return events
        # Geometry-based dispersion contribution per cell
        cells = self.cell_pool.detach()
        N = self.n_cells
        if N < 4:
            return super()._check_splits(per_cell_tensions)
        with torch.no_grad():
            mean_row = cells.mean(dim=0, keepdim=True)
            disp_per = ((cells - mean_row) ** 2).mean(dim=1).cpu().numpy()
        # Top-quartile dispersion cells become candidates
        thresh = float(np.quantile(disp_per, 0.75))
        candidates = []
        for i, cell in enumerate(self.cells):
            if i >= N:
                continue
            # accumulate dispersion as a "geom_history" so patience still applies
            if not hasattr(cell, "_geom_hist"):
                cell._geom_hist = []
            cell._geom_hist.append(float(disp_per[i]))
            if len(cell._geom_hist) > self.split_patience * 3:
                cell._geom_hist = cell._geom_hist[-self.split_patience * 3:]
            if len(cell._geom_hist) < self.split_patience:
                continue
            recent = cell._geom_hist[-self.split_patience:]
            if all(g > thresh for g in recent):
                candidates.append(i)
        for parent_idx in candidates:
            if self.n_cells >= self.max_cells:
                break
            ev = self._split_cell_slice(parent_idx)
            if ev:
                events.append(ev)
        return events


def make_mitosis(variant: str, init_pool: torch.Tensor, c_to_h, **base_kwargs) -> MitosisV5Engine:
    """Build a mitosis instance for an ablation variant."""
    if variant == "A1_lower_threshold":
        return MitosisV5_LowerThreshold(
            cell_pool=init_pool, c_to_h=c_to_h, initial_cells=init_pool.shape[0], **base_kwargs
        )
    elif variant == "A2_no_lorenz":
        kw = dict(base_kwargs); kw["lorenz_scale"] = 0.0
        return MitosisV5Engine(
            cell_pool=init_pool, c_to_h=c_to_h, initial_cells=init_pool.shape[0], **kw
        )
    elif variant == "A4_dispersion":
        return MitosisV5_DispersionTrigger(
            cell_pool=init_pool, c_to_h=c_to_h, initial_cells=init_pool.shape[0], **base_kwargs
        )
    else:  # A3_no_pull, A5_baseline, baseline
        return MitosisV5Engine(
            cell_pool=init_pool, c_to_h=c_to_h, initial_cells=init_pool.shape[0], **base_kwargs
        )


def run_one_ablation(
    model,
    variant: str,
    n_turns: int,
    label: str,
    seed: int,
    log_fn,
    snapshot_every: int = 100,
):
    torch.manual_seed(seed)
    np.random.seed(seed)
    model.eval()
    capture = HiddenMeanCapture(model.engine_g)

    eg = model.engine_g
    init_pool = eg.cell_pool_init.detach().clone()

    base_kwargs = dict(
        max_cells=64, split_patience=3, split_noise=0.10,
        merge_threshold=0.005, merge_patience=30, min_cells=2,
        lorenz_scale=0.05,
    )
    mitosis = make_mitosis(variant, init_pool, eg.c_to_h, **base_kwargs)

    # Tension records (per-cell over time, full distribution)
    all_per_cell_tensions: list[list[float]] = []  # list of list per turn
    threshold_history: list[float] = []
    n_splits = 0
    n_merges = 0
    cell_max_tens_count: dict[int, int] = {}  # how many turns each cell was tension-max

    snapshots = []
    t_start = time.time()

    with torch.no_grad():
        for turn in range(n_turns):
            cat, prompt = ALL_PROMPTS[turn % len(ALL_PROMPTS)]
            ids = encode_prompt_to_ids(prompt, T=16)
            _ = model(ids, output_hidden_states=False, output_attentions=False)
            hm = capture.last_hidden_mean
            if hm is None:
                cell_input = torch.zeros(1, eg.c_dim)
            elif variant == "A3_no_pull":
                # Bypass h_to_c projection. Use a zero vector — i.e., cells receive
                # no attention-pull signal. Tension reduces to ||cell - 0||² = ||cell||²,
                # so all cells have ~same tension (unit-sphere init), no preference for any cell.
                # This isolates whether c_to_h projection causes attractor monopoly.
                cell_input = torch.zeros(1, eg.c_dim)
            else:
                cell_input = eg.h_to_c(hm)

            out = mitosis.process(cell_input)

            for ev in out["events"]:
                if ev["type"] == "split":
                    n_splits += 1
                elif ev["type"] == "merge":
                    n_merges += 1

            tens = out["per_cell_tension"]
            all_per_cell_tensions.append(list(tens))
            threshold_history.append(float(out["split_threshold"]))
            if tens:
                top_idx = max(range(len(tens)), key=lambda i: tens[i])
                cell_max_tens_count[top_idx] = cell_max_tens_count.get(top_idx, 0) + 1

            if turn % snapshot_every == 0 or turn == n_turns - 1:
                cp = mitosis.cell_pool.detach().cpu().numpy()
                # Compute IIT Φ at this snapshot (16-bin)
                try:
                    phi_iit = compute_iit_phi(torch.tensor(cp), n_bins=16)
                    iit_unnorm = float(phi_iit["spatial_phi_unnormalized"])
                except Exception:
                    iit_unnorm = float("nan")
                snapshots.append({
                    "turn": int(turn),
                    "n_cells": int(out["n_cells"]),
                    "proxy_phi": float(out["phi"]),
                    "iit_unnorm_b16": iit_unnorm,
                    "split_threshold": float(out["split_threshold"]),
                    "n_splits_cum": int(n_splits),
                    "tens_min": float(min(tens)) if tens else 0.0,
                    "tens_max": float(max(tens)) if tens else 0.0,
                    "tens_mean": float(sum(tens) / len(tens)) if tens else 0.0,
                })

    elapsed = time.time() - t_start
    # Flatten tension distribution for histogram
    flat_tens = []
    for row in all_per_cell_tensions:
        flat_tens.extend(row)

    # Final IIT
    try:
        cp_final = mitosis.cell_pool.detach().cpu().numpy()
        phi_iit_final = compute_iit_phi(torch.tensor(cp_final), n_bins=16)
        iit_final = float(phi_iit_final["spatial_phi_unnormalized"])
    except Exception:
        iit_final = float("nan")

    log_fn(
        f"  [{label}/{variant}] cells {int(mitosis.n_cells):2d} splits={n_splits:2d} merges={n_merges:2d}"
        f" iit_un={iit_final:.1f} elapsed={elapsed:.1f}s"
    )

    # Tension stats
    flat_arr = np.array(flat_tens, dtype=np.float64)
    return {
        "label": label,
        "variant": variant,
        "n_turns": n_turns,
        "elapsed_sec": elapsed,
        "n_splits": n_splits,
        "n_merges": n_merges,
        "final_n_cells": int(mitosis.n_cells),
        "iit_unnorm_b16_final": iit_final,
        "snapshots": snapshots,
        "cell_max_tens_count": {str(k): v for k, v in cell_max_tens_count.items()},
        "tens_stats": {
            "n": int(len(flat_arr)),
            "min": float(flat_arr.min()) if len(flat_arr) else 0.0,
            "max": float(flat_arr.max()) if len(flat_arr) else 0.0,
            "mean": float(flat_arr.mean()) if len(flat_arr) else 0.0,
            "std": float(flat_arr.std()) if len(flat_arr) else 0.0,
            "p25": float(np.percentile(flat_arr, 25)) if len(flat_arr) else 0.0,
            "p50": float(np.percentile(flat_arr, 50)) if len(flat_arr) else 0.0,
            "p75": float(np.percentile(flat_arr, 75)) if len(flat_arr) else 0.0,
            "p95": float(np.percentile(flat_arr, 95)) if len(flat_arr) else 0.0,
            "p99": float(np.percentile(flat_arr, 99)) if len(flat_arr) else 0.0,
        },
        "threshold_stats": {
            "mean": float(np.mean(threshold_history)) if threshold_history else 0.0,
            "max": float(np.max(threshold_history)) if threshold_history else 0.0,
            "min": float(np.min(threshold_history)) if threshold_history else 0.0,
        },
        # Down-sample full tension distribution for plotting (every 10th turn × all cells)
        "tens_sample": [float(x) for x in flat_arr[::10][:5000].tolist()],
    }


def main(n_turns: int = 1000, seed: int = 42, stage: str = "all"):
    """stage: 'all' | 'first3' (A1+A2+A3) | 'last3' (A4+A5_trained+A5_random) | 'merge'."""
    log_path = THIS_DIR / "run.log"
    log_mode = "w" if stage in ("all", "first3") else "a"
    log_f = open(log_path, log_mode)

    def log(msg: str):
        print(msg, flush=True)
        log_f.write(msg + "\n")
        log_f.flush()

    log(f"=== BG-V5ANIMA-PHASE2-SPLIT-RATE-DIAG (stage={stage}) ===")
    log(f"n_turns/ablation = {n_turns}, seed={seed}, n_prompts={len(ALL_PROMPTS)}")

    # Verify ckpt
    h = hashlib.sha256()
    with open(CKPT_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    actual_sha = h.hexdigest()
    sha_match = (actual_sha == CKPT_SHA256)
    log(f"ckpt sha256 verify: {'PASS' if sha_match else 'FAIL'}")
    if not sha_match:
        log("ABORT: ckpt sha mismatch")
        log_f.close()
        return

    # Load substrate
    cfg = EngineAGConfig.phase2_cotrain_350m()
    ckpt = torch.load(CKPT_PATH, map_location="cpu", weights_only=False)
    sd = ckpt["model"]
    sd_fp32 = {k: v.float() if v.dtype == torch.bfloat16 else v for k, v in sd.items()}
    trained_model = EngineAGModel(cfg)
    trained_model.load_state_dict(sd_fp32, strict=True)
    n_params = sum(p.numel() for p in trained_model.parameters())
    log(f"trained 350M loaded ({n_params/1e6:.2f}M params)")

    rand_model = load_random_init(seed=42, preset="la_350m")
    log(f"random_init mirror loaded")

    # Per-ablation persistence (resumable across stages)
    cache_dir = THIS_DIR / "cache"
    cache_dir.mkdir(exist_ok=True)

    def save_cache(name: str, data):
        (cache_dir / f"{name}.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))

    def load_cache(name: str):
        p = cache_dir / f"{name}.json"
        if p.exists():
            return json.loads(p.read_text())
        return None

    def run_or_load(model_, variant, label, key):
        cached = load_cache(key)
        if cached is not None:
            log(f"  [{label}/{variant}] CACHED splits={cached['n_splits']} N={cached['final_n_cells']}")
            return cached
        r = run_one_ablation(model_, variant, n_turns, label, seed, log)
        save_cache(key, r)
        return r

    if stage in ("all", "first3"):
        log("\n--- Ablations stage=first3 (A1, A2, A3) ---")
        a1 = run_or_load(trained_model, "A1_lower_threshold", "trained", "a1")
        a2 = run_or_load(trained_model, "A2_no_lorenz", "trained", "a2")
        a3 = run_or_load(trained_model, "A3_no_pull", "trained", "a3")
        if stage == "first3":
            log("stage=first3 complete; rerun with stage=last3 then stage=merge.")
            log_f.close()
            return

    if stage in ("all", "last3"):
        log("\n--- Ablations stage=last3 (A4, A5_trained, A5_random) ---")
        a4 = run_or_load(trained_model, "A4_dispersion", "trained", "a4")
        a5_trained = run_or_load(trained_model, "A5_baseline", "trained", "a5_trained")
        a5_random = run_or_load(rand_model, "A5_baseline", "random", "a5_random")
        if stage == "last3":
            log("stage=last3 complete; rerun with stage=merge to assemble.")
            log_f.close()
            return

    if stage == "merge":
        a1 = load_cache("a1")
        a2 = load_cache("a2")
        a3 = load_cache("a3")
        a4 = load_cache("a4")
        a5_trained = load_cache("a5_trained")
        a5_random = load_cache("a5_random")
        if any(x is None for x in (a1, a2, a3, a4, a5_trained, a5_random)):
            log("ABORT merge: cache incomplete — run first3 + last3 first.")
            log_f.close()
            return

    # Summary table
    log("\n=== ABLATION SUMMARY (1K turns each, trained 350M unless noted) ===")
    log(f"  {'variant':<25} {'splits':>6} {'final_N':>7} {'iit_un':>8} {'tens_p99':>9} {'thr_max':>9}")
    rows = [a1, a2, a3, a4, a5_trained, a5_random]
    rows[-1]["variant"] = "A5_baseline_RANDOM"
    for r in rows:
        log(
            f"  {r['variant']:<25} {r['n_splits']:>6d} {r['final_n_cells']:>7d}"
            f" {r['iit_unnorm_b16_final']:>8.1f}"
            f" {r['tens_stats']['p99']:>9.4f} {r['threshold_stats']['max']:>9.4f}"
        )

    # Diagnose hypotheses
    diag = {}
    # H1 attention-pull: A3_no_pull split count vs baseline → if A3 splits >> baseline, H1 confirmed
    h1_signal = a3["n_splits"] > a5_trained["n_splits"] + 1
    # H2 tension-scale: trained tens p99 < random tens p99 → if so, H2 contributing
    h2_signal = a5_trained["tens_stats"]["p99"] < a5_random["tens_stats"]["p99"] * 0.5
    # H3 concentration: in baseline trained, top-1 cell holds >40% of max-tension turns
    cell_counts = a5_trained["cell_max_tens_count"]
    sum_counts = sum(cell_counts.values()) or 1
    top_share = max(cell_counts.values()) / sum_counts if cell_counts else 0
    # also look at top-2
    sorted_counts = sorted(cell_counts.values(), reverse=True)
    top2_share = (sorted_counts[0] + (sorted_counts[1] if len(sorted_counts) > 1 else 0)) / sum_counts
    h3_signal = top2_share > 0.40

    diag = {
        "H1_attn_pull": {
            "A3_splits_vs_baseline": (a3["n_splits"], a5_trained["n_splits"]),
            "A3_final_cells_vs_baseline": (a3["final_n_cells"], a5_trained["final_n_cells"]),
            "confirmed": bool(h1_signal),
            "interpretation": "H1 confirmed" if h1_signal
                else "H1 not strongly supported — disabling pull did not unlock splits"
        },
        "H2_tension_scale": {
            "trained_p99_tension": a5_trained["tens_stats"]["p99"],
            "random_p99_tension": a5_random["tens_stats"]["p99"],
            "ratio_trained_random": (
                a5_trained["tens_stats"]["p99"] / a5_random["tens_stats"]["p99"]
                if a5_random["tens_stats"]["p99"] > 0 else float("inf")
            ),
            "trained_threshold_max": a5_trained["threshold_stats"]["max"],
            "random_threshold_max": a5_random["threshold_stats"]["max"],
            "confirmed": bool(h2_signal),
            "interpretation": "H2 confirmed — trained tension is < 50% of random scale"
                if h2_signal else
                "H2 not strongly supported — tension scales comparable"
        },
        "H3_concentration": {
            "trained_top_cell_share": top_share,
            "trained_top2_share": top2_share,
            "trained_cell_distribution": dict(sorted(cell_counts.items(),
                                                     key=lambda kv: -kv[1])[:5]),
            "A1_lower_threshold_splits": a1["n_splits"],
            "confirmed": bool(h3_signal),
            "interpretation": (
                f"H3 confirmed — top-2 cells own {top2_share:.1%} of max-tension turns"
                if h3_signal else
                "H3 not strongly supported — tension distributed across cells"
            ),
        },
        "A4_dispersion_trigger": {
            "splits": a4["n_splits"],
            "final_cells": a4["final_n_cells"],
            "vs_baseline_splits": a5_trained["n_splits"],
        },
        "A2_lorenz_role": {
            "no_lorenz_splits": a2["n_splits"],
            "vs_baseline_splits": a5_trained["n_splits"],
            "interpretation": (
                "Lorenz necessary for splits"
                if a2["n_splits"] < a5_trained["n_splits"] else
                "Lorenz not the limiting factor"
            ),
        },
    }

    # Verdict
    score_h1 = int(h1_signal)
    score_h2 = int(h2_signal)
    score_h3 = int(h3_signal)
    if score_h3 and not score_h1:
        verdict = "H3_concentration_PRIMARY"
    elif score_h1 and not score_h3:
        verdict = "H1_attn_pull_PRIMARY"
    elif score_h2 and not (score_h1 or score_h3):
        verdict = "H2_scale_PRIMARY"
    elif score_h1 and score_h3:
        verdict = "H1+H3_combined (pull projects to attractor cells, monopolizing tension)"
    else:
        verdict = "INCONCLUSIVE"

    log(f"\n=== HYPOTHESIS DIAGNOSIS ===")
    log(f"  H1 attn-pull confirmed:    {h1_signal}")
    log(f"  H2 tension-scale confirmed:{h2_signal}")
    log(f"  H3 concentration confirmed:{h3_signal}")
    log(f"  primary verdict:            {verdict}")
    log(f"  trained top-2 cell share:   {top2_share:.1%}")
    log(f"  trained vs random p99 tens: {a5_trained['tens_stats']['p99']:.4f} vs {a5_random['tens_stats']['p99']:.4f}")
    log(f"  A1 lower-threshold splits:  {a1['n_splits']} (baseline {a5_trained['n_splits']})")
    log(f"  A2 no-lorenz splits:        {a2['n_splits']} (baseline {a5_trained['n_splits']})")
    log(f"  A3 no-pull splits:          {a3['n_splits']} (baseline {a5_trained['n_splits']})")
    log(f"  A4 dispersion-trigger:      {a4['n_splits']} (baseline {a5_trained['n_splits']})")

    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "bg_id": "BG-V5ANIMA-PHASE2-SPLIT-RATE-DIAG",
        "n_turns": n_turns,
        "seed": seed,
        "ckpt": {"path": CKPT_PATH, "sha256": CKPT_SHA256, "n_params": n_params},
        "ablations": {
            "A1_lower_threshold": a1,
            "A2_no_lorenz":       a2,
            "A3_no_pull":         a3,
            "A4_dispersion":      a4,
            "A5_baseline_trained": a5_trained,
            "A5_baseline_random":  a5_random,
        },
        "diagnosis": diag,
        "verdict": verdict,
        "honest_c3": [
            "Single seed=42 across all 5 ablations — diagnoses are point estimates, not statistically validated. Replication with seeds 41/43/44 would strengthen claims; not done due to 90min budget.",
            "n_turns=1000 per ablation matches §22's V14 mirror length, but trained §22 was 3K turns. A1/A2/A4 may behave differently at 3K (e.g., late-onset splits). The diagnostic is restricted to 'why no splits in first 1K turns'.",
            "A3_no_pull replaces hidden_mean projection with zeros. Tension reduces to ||cell||² which after Lorenz norm-clamp is ≈ 1.0 for all cells — i.e. tension ~uniform → splits should NEVER trigger because mean+1.5σ has no separation. Result: A3 splits=0 is EXPECTED, not informative about H1 alone. The informative signal is A3 cell-distribution: if tension max-cell becomes uniform (no top-1 cell dominance), H1 partially supported.",
            "A4_dispersion piggybacks on _check_splits override but still uses the original adaptive threshold (split_threshold) on tension_history. The geom_history is monotonically additive and may take longer to populate — patience semantics differ slightly from baseline.",
            "byte-hash mod 32000 token encoding is identical to §22 (semantically arbitrary). The 'attractor' for cells 7/16 in §22 may be partially encoding artifact (some token IDs land in regions that h_to_c projects close to those cells). Real BPE could relocate the attractor but is unlikely to dissolve it — the geometric concentration is a property of trained h_to_c, not encoding.",
            "ctx_T=16 (vs training T=1024) under-samples substrate forward state. h_to_c projection is sensitive to position-mean of hidden_states; longer T may produce richer hidden_mean and broader cell-attention, weakening H1. Listed as future probe.",
            "Mitosis owns cell_pool Parameter; substrate's cell_pool_init is read once at attach. So the diagnosis is about HOW trained engine_g.h_to_c shapes the cell-pool dynamics, NOT about the trained cell_pool_init Parameter itself. Random_init mirror has same architecture, freshly random h_to_c — so trained-vs-random difference isolates 'what training does to h_to_c geometry'.",
            "IIT Φ unnorm 16-bin computed per snapshot for shape-comparability with §22, but at N≤19 we always hit Fiedler spectral approximation (not exact PyPhi MIP). Used as monotonic indicator only.",
            "All ablations use identical seed=42 + same prompt order, so trajectory differences are deterministic functions of the variant change. Lorenz noise reuses the seed too — A2 disables Lorenz entirely, removing chaos injection.",
            "Hypothesis tests (h1_signal, h2_signal, h3_signal) use simple thresholds (e.g., top2 > 40%). These are heuristic; honest interpretation should focus on relative magnitudes in the diagnosis tables, not boolean confirmed/not.",
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

        # Plot 1: tension_histograms.png — overlay of trained vs random + per ablation
        fig, axes = plt.subplots(2, 3, figsize=(15, 9))
        bins = 40

        ax = axes[0, 0]
        t_t = np.array(a5_trained["tens_sample"])
        t_r = np.array(a5_random["tens_sample"])
        if len(t_t) > 0 and len(t_r) > 0:
            tmax = max(float(t_t.max()), float(t_r.max())) * 1.05
            ax.hist(t_t, bins=np.linspace(0, tmax, bins), alpha=0.6, label="trained 350M", color="C0")
            ax.hist(t_r, bins=np.linspace(0, tmax, bins), alpha=0.6, label="random_init", color="C3")
        ax.set_title(f"per-cell tension distribution (1K turns × N cells)\np99 trained={a5_trained['tens_stats']['p99']:.3f} random={a5_random['tens_stats']['p99']:.3f}")
        ax.set_xlabel("tension = mean((cell - h_to_c(hm))²)")
        ax.set_ylabel("count")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Per-ablation tension dist on trained
        for idx, (lab, r) in enumerate([
            ("A1 lower threshold", a1), ("A2 no lorenz", a2),
            ("A3 no pull (zero hm)", a3), ("A4 dispersion", a4),
        ], start=1):
            ax = axes[idx // 3, idx % 3]
            samp = np.array(r["tens_sample"])
            if len(samp) > 0:
                ax.hist(samp, bins=bins, color=f"C{idx}", alpha=0.7)
                ax.axvline(r["threshold_stats"]["mean"], color="k", ls="--",
                           label=f"thr_mean={r['threshold_stats']['mean']:.3f}")
            ax.set_title(f"{lab}\nsplits={r['n_splits']} N_final={r['final_n_cells']}")
            ax.set_xlabel("tension"); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

        # Cell concentration plot (last subplot)
        ax = axes[1, 2]
        cells_sorted = sorted(a5_trained["cell_max_tens_count"].items(),
                              key=lambda kv: -kv[1])
        ks = [int(k) for k, _ in cells_sorted]
        vs = [v for _, v in cells_sorted]
        ax.bar(range(len(ks)), vs, color="C0", alpha=0.8)
        ax.set_xticks(range(len(ks)))
        ax.set_xticklabels([str(k) for k in ks], rotation=45, fontsize=8)
        ax.set_xlabel("cell idx")
        ax.set_ylabel("# turns this cell was tension-max")
        ax.set_title(f"trained tension-max concentration\ntop-2 share={top2_share:.1%}")
        ax.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        plt.savefig(THIS_DIR / "tension_histograms.png", dpi=80)
        plt.close(fig)
        log(f"plot 1: {THIS_DIR / 'tension_histograms.png'}")

        # Plot 2: split_rate_per_ablation.png
        fig2, ax = plt.subplots(1, 1, figsize=(10, 6))
        labels = ["A1\nlower thr", "A2\nno lorenz", "A3\nno pull", "A4\ndispersion",
                  "A5 baseline\ntrained", "A5 baseline\nrandom"]
        splits = [a1["n_splits"], a2["n_splits"], a3["n_splits"], a4["n_splits"],
                  a5_trained["n_splits"], a5_random["n_splits"]]
        n_cells_final = [a1["final_n_cells"], a2["final_n_cells"], a3["final_n_cells"],
                         a4["final_n_cells"], a5_trained["final_n_cells"],
                         a5_random["final_n_cells"]]
        colors = ["C1", "C2", "C3", "C4", "C0", "C5"]
        bars = ax.bar(labels, splits, color=colors, alpha=0.8)
        for i, (s, n) in enumerate(zip(splits, n_cells_final)):
            ax.text(i, s + 0.2, f"N={n}", ha="center", va="bottom", fontsize=10)
        ax.set_ylabel("# splits in 1K turns")
        ax.set_title(f"BG-REAL350M-IIT split-rate ablation (trained 350M, 1K turns)\nverdict: {verdict}")
        ax.grid(True, alpha=0.3, axis="y")
        plt.tight_layout()
        plt.savefig(THIS_DIR / "split_rate_per_ablation.png", dpi=80)
        plt.close(fig2)
        log(f"plot 2: {THIS_DIR / 'split_rate_per_ablation.png'}")
    except Exception as e:
        log(f"matplotlib skip: {e}")

    log_f.close()
    return result


if __name__ == "__main__":
    n_turns = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    stage = sys.argv[2] if len(sys.argv) > 2 else "all"
    main(n_turns=n_turns, stage=stage)
