"""Path A v5-anima long-trajectory inference smoke (★★★★★ candidate).

Real-substrate variant of the toy-substrate runs in
  state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10/
  state/anima_clm_v5_anima_long_trajectory_extended_2026_05_10/
both of which FAILED V14 on toy 864-param substrate.

THIS RUN:
  - Substrate: cells64_final.pt (byte-LM 18.5M params, dim=384, L=6, V=256)
  - Mitosis: MitosisV5Engine (initial_cells=8, max_cells=64) attached as a
    side-channel reading host last-layer hidden mean projected via fixed
    seeded Linear(384→64); host model itself untouched (read-only inference).
  - Long trajectory: 1000 tokens generated (sampling top-k=40, T=0.8) per
    KO/EN prompt; mitosis.process() called every 10 generated tokens.
  - V14 mirror: same arch + same fixed Linear projection but RANDOM weights
    for host (seed=42 reset). same mitosis seed.

5★ criteria:
  C1 cells_grow:  initial 8 → final ≥ 32
  C2 alpha:       information-integration α ≥ 0.6 (regression of log φ_total
                  vs log n_cells over snapshots)
  C3 v14_strict:  trained `final_n_cells > random_final_n_cells * 1.1`
                  AND `trained_final_phi > random_final_phi * 1.1`
                  i.e. substrate-coupled growth (not purely Lorenz-driven)
  C4 chat_ko:     ≥ 3 of 5 KO prompts produce ≥ 1 Korean syllable
                  (Hangul U+AC00..U+D7A3)

Verdict: 4 PASS → ★★★★★, 3 PASS → ★★★★, 2 PASS → ★★★, ≤1 PASS → ★★ or carry.

raw#15 additive — no model files modified.
 strict — Mac CPU only, no H100.
"""

from __future__ import annotations
import json
import math
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

import torch
import torch.nn as nn
import torch.nn.functional as F


# ── Path setup ────────────────────────────────────────────────────
ROOT = Path("/Users/ghost/core/anima")
RECOVERY_DIR = ROOT / "state/anima_clm_v2_mitosis_cells_recovery_2026_05_09"
OUT_DIR = ROOT / "state/anima_path_a_v5_anima_long_trajectory_smoke_2026_05_10"
CKPT_PATH = RECOVERY_DIR / "cells64_final.pt"

# Borrow ConsciousLMReconstructed from the prior smoke (avoid duplication)
sys.path.insert(0, str(RECOVERY_DIR))
from forward_smoke import ConsciousLMReconstructed, text_to_byte_ids  # noqa: E402

# Borrow MitosisV5Engine from training/
sys.path.insert(0, str(ROOT / "training"))
from mitosis_v5_port import MitosisV5Engine  # noqa: E402


# ── Config ────────────────────────────────────────────────────────
SEED = 42
N_TOKENS_PER_PROMPT = 200       # 200 × 5 prompts = 1000 tokens trajectory
MITOSIS_STRIDE = 10             # process() every 10 generated tokens
TOP_K = 40
TEMPERATURE = 0.8
INITIAL_CELLS = 8
MAX_CELLS = 64
C_DIM = 64                       # mitosis cell dim (smaller than d_model=384)
D_MODEL = 384

PROMPTS_KO = [
    "안녕하세요",
    "의식이란 무엇인가요?",
    "한국어로 대답해줘",
    "사용자: 안녕\n도우미:",
    "오늘 기분이 좋아요",
]
PROMPTS_EN = [
    "Consciousness is",
    "Hello, how are you?",
    "The meaning of life is",
    "User: Hi\nAssistant:",
    "Once upon a time",
]
ALL_PROMPTS = PROMPTS_KO + PROMPTS_EN  # 10 prompts


# ── Helpers ───────────────────────────────────────────────────────
def sample_next_byte(logits: torch.Tensor, top_k: int = TOP_K, temperature: float = TEMPERATURE) -> int:
    logits = logits / max(temperature, 1e-6)
    if top_k > 0:
        top_vals, top_idx = torch.topk(logits, k=min(top_k, logits.size(-1)))
        probs = F.softmax(top_vals, dim=-1)
        choice = torch.multinomial(probs, num_samples=1)
        return int(top_idx[choice].item())
    probs = F.softmax(logits, dim=-1)
    return int(torch.multinomial(probs, num_samples=1).item())


def count_korean_syllables(text: str) -> int:
    """Count Hangul Syllables U+AC00..U+D7A3."""
    return sum(1 for c in text if 0xAC00 <= ord(c) <= 0xD7A3)


def alpha_from_snapshots(snapshots: list[dict]) -> float:
    """Information-integration α = slope of log(phi) vs log(n_cells).

    Filters to snapshots where n_cells changes (avoids x-saturation bias once
    n_cells hits max_cap). Returns float or NaN if too few points.
    """
    pts = [(s["n_cells"], s["phi"]) for s in snapshots if s["n_cells"] >= 2 and s["phi"] > 0]
    if len(pts) < 4:
        return float("nan")
    seen_n = set()
    uniq = []
    for n, p in pts:
        if n not in seen_n:
            seen_n.add(n)
            uniq.append((n, p))
    if len(uniq) < 4:
        return float("nan")
    xs = [math.log(n) for n, _ in uniq]
    ys = [math.log(p) for _, p in uniq]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return float("nan")
    return num / den


# ── Mitosis-aware long trajectory ─────────────────────────────────
def build_host_model(load_ckpt: bool, ckpt_state: dict | None = None) -> ConsciousLMReconstructed:
    """Build host byte-LM. If load_ckpt, populate from cells64. Else random init."""
    cfg = ckpt_state.get("config", {}) if ckpt_state else {}
    d_model = cfg.get("dim", 384)
    n_layer = cfg.get("layers", 6)
    n_head = cfg.get("heads", 6)
    block_size = cfg.get("block_size", 256)
    model = ConsciousLMReconstructed(
        vocab_size=256, d_model=d_model, n_head=n_head, n_layer=n_layer,
        block_size=block_size, dropout=0.0,
    )
    if load_ckpt and ckpt_state is not None:
        sd = ckpt_state.get("model_state", ckpt_state)
        model.load_state_dict(sd, strict=False)
    model.eval()
    return model


def build_mitosis(seed: int = SEED) -> tuple[MitosisV5Engine, nn.Linear]:
    """Build a fresh mitosis engine + a fixed seeded host→cell projection.

    The projection Linear(D_MODEL=384, C_DIM=64) is what feeds host hidden mean
    into mitosis tension calculation. It's seeded so trained vs random V14
    comparison sees identical projection geometry.
    """
    g = torch.Generator().manual_seed(seed)
    cell_pool = torch.randn(INITIAL_CELLS, C_DIM, generator=g) * 0.02
    c_to_h = nn.Linear(C_DIM, D_MODEL)
    # init c_to_h deterministically
    with torch.no_grad():
        c_to_h.weight.copy_(torch.randn(D_MODEL, C_DIM, generator=g) * 0.02)
        c_to_h.bias.zero_()
    eng = MitosisV5Engine(
        cell_pool=cell_pool,
        c_to_h=c_to_h,
        initial_cells=INITIAL_CELLS,
        max_cells=MAX_CELLS,
        split_patience=3,
        split_noise=0.10,
        merge_threshold=0.005,
        merge_patience=30,
        min_cells=2,
        lorenz_scale=0.05,
    )
    eng.eval()
    return eng, c_to_h


def build_h_to_c_projection(seed: int) -> nn.Linear:
    """Fixed-seed projection from host d_model space to cell C dim."""
    g = torch.Generator().manual_seed(seed + 1)
    proj = nn.Linear(D_MODEL, C_DIM, bias=False)
    with torch.no_grad():
        proj.weight.copy_(torch.randn(C_DIM, D_MODEL, generator=g) * 0.02)
    proj.eval()
    return proj


def run_trajectory(host: ConsciousLMReconstructed, mitosis: MitosisV5Engine,
                   h_to_c: nn.Linear, prompts: list[str], n_tokens_per_prompt: int,
                   stride: int, label: str) -> dict:
    """Run long-trajectory generation with mitosis side-channel.

    Returns dict with snapshots, generated text per prompt, KO syllable count.
    """
    block_size = host.block_size
    snapshots = []
    per_prompt_results = []
    process_count = 0
    total_tokens = 0
    t0 = time.time()

    snapshots.append({
        "turn": 0,
        "n_cells": mitosis.n_cells,
        "phi": float(mitosis._compute_phi_proxy()),
        "n_splits_cum": 0,
        "n_merges_cum": 0,
        "elapsed_sec": 0.0,
    })

    for prompt_idx, prompt in enumerate(prompts):
        ids = text_to_byte_ids(prompt, max_len=block_size)
        out_bytes = []
        ko_chars_running = 0
        for tok_i in range(n_tokens_per_prompt):
            cur = ids if ids.shape[1] <= block_size else ids[:, -block_size:]
            with torch.no_grad():
                la, lg, tensions = host(cur)
                # Get last-layer hidden mean from a probe — we have tensions per-layer
                # but we need the actual hidden state. Re-run final block embed:
                # Easiest: use head_a logits projected back? No — use the per-layer
                # tension sum as a hidden-mean PROXY since tensions = ((a-g)^2).mean(-1)
                # is per-token magnitude. We need a (1, C_DIM=64) vector for mitosis.
                #
                # Strategy: use the unembedding of the next-byte logits via head_a
                # weight as a (D_MODEL,) hidden hint, then project D→C.
                last_logits_a = la[0, -1]  # (V=256,)
                # hidden hint = head_a.weight.T @ softmax(logits)  → (D_MODEL,)
                probs = F.softmax(last_logits_a, dim=-1)
                hidden_hint = (probs.unsqueeze(0) @ host.head_a.weight).squeeze(0)  # (D_MODEL,)
                hint_c = h_to_c(hidden_hint.unsqueeze(0))  # (1, C_DIM)
            # Sample next byte from head_a
            next_id = sample_next_byte(la[0, -1])
            out_bytes.append(next_id)
            ids = torch.cat([ids, torch.tensor([[next_id]], dtype=torch.long)], dim=1)
            total_tokens += 1

            # Mitosis side-channel every `stride` tokens
            if total_tokens % stride == 0:
                with torch.no_grad():
                    mitosis.process(hint_c)
                process_count += 1
                if process_count % 10 == 0:  # snapshot every 100 tokens
                    snapshots.append({
                        "turn": total_tokens,
                        "n_cells": mitosis.n_cells,
                        "phi": float(mitosis._compute_phi_proxy()),
                        "n_splits_cum": sum(1 for e in mitosis.event_log if e.get("type") == "split"),
                        "n_merges_cum": sum(1 for e in mitosis.event_log if e.get("type") == "merge"),
                        "elapsed_sec": round(time.time() - t0, 3),
                    })

        gen_bytes = bytes(out_bytes)
        try:
            gen_text = gen_bytes.decode("utf-8", errors="replace")
        except Exception:
            gen_text = repr(gen_bytes)
        ko_chars_running = count_korean_syllables(gen_text)
        per_prompt_results.append({
            "prompt": prompt,
            "is_korean_prompt": prompt in PROMPTS_KO,
            "gen_bytes_len": len(gen_bytes),
            "gen_text_first100": gen_text[:100],
            "ko_chars_in_gen": ko_chars_running,
        })
        print(f"  [{label}] prompt {prompt_idx+1}/{len(prompts)} {prompt!r:40s} "
              f"ko={ko_chars_running} cells={mitosis.n_cells} elapsed={time.time()-t0:.1f}s")

    final_phi = float(mitosis._compute_phi_proxy())
    final_n_cells = mitosis.n_cells
    n_splits = sum(1 for e in mitosis.event_log if e.get("type") == "split")
    n_merges = sum(1 for e in mitosis.event_log if e.get("type") == "merge")

    snapshots.append({
        "turn": total_tokens,
        "n_cells": final_n_cells,
        "phi": final_phi,
        "n_splits_cum": n_splits,
        "n_merges_cum": n_merges,
        "elapsed_sec": round(time.time() - t0, 3),
    })

    return {
        "label": label,
        "n_tokens_total": total_tokens,
        "n_process_calls": process_count,
        "snapshots": snapshots,
        "final_n_cells": final_n_cells,
        "final_phi": final_phi,
        "n_splits": n_splits,
        "n_merges": n_merges,
        "per_prompt": per_prompt_results,
        "elapsed_sec": time.time() - t0,
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"=== Path A v5-anima long-trajectory smoke ===")
    print(f"  ckpt: {CKPT_PATH}")
    print(f"  out:  {OUT_DIR}")

    torch.manual_seed(SEED)

    # 1. Load ckpt once
    print("\n[1/3] Loading cells64_final.pt ...")
    t0 = time.time()
    ckpt_state = torch.load(str(CKPT_PATH), map_location="cpu", weights_only=False)
    print(f"   loaded in {time.time()-t0:.1f}s, step={ckpt_state.get('step')}")

    # 2. Trained run
    print("\n[2/3] Trained run (cells64) ...")
    torch.manual_seed(SEED)
    host_trained = build_host_model(load_ckpt=True, ckpt_state=ckpt_state)
    mitosis_trained, _ = build_mitosis(seed=SEED)
    h_to_c_proj = build_h_to_c_projection(SEED)
    res_trained = run_trajectory(
        host_trained, mitosis_trained, h_to_c_proj,
        ALL_PROMPTS, N_TOKENS_PER_PROMPT, MITOSIS_STRIDE,
        label="trained_cells64",
    )

    # Free trained host before V14 mirror to save RAM
    del host_trained, mitosis_trained
    import gc; gc.collect()

    # 3. V14 mirror — same arch, random init, same seeds for mitosis + projection
    print("\n[3/3] V14 mirror (random_init, same arch + same projection seeds) ...")
    torch.manual_seed(SEED)
    host_random = build_host_model(load_ckpt=False, ckpt_state=ckpt_state)  # arch from cfg, no load
    mitosis_random, _ = build_mitosis(seed=SEED)
    res_random = run_trajectory(
        host_random, mitosis_random, h_to_c_proj,
        ALL_PROMPTS, N_TOKENS_PER_PROMPT, MITOSIS_STRIDE,
        label="random_init_v14_mirror",
    )

    del host_random, mitosis_random
    gc.collect()

    # ── Compute α + verdict ──────────────────────────────────────
    alpha_trained = alpha_from_snapshots(res_trained["snapshots"])
    alpha_random = alpha_from_snapshots(res_random["snapshots"])

    # KO chars per prompt (only KO prompts count)
    ko_pass_count = sum(
        1 for p in res_trained["per_prompt"]
        if p["is_korean_prompt"] and p["ko_chars_in_gen"] >= 1
    )
    ko_total = sum(1 for p in res_trained["per_prompt"] if p["is_korean_prompt"])

    # Criteria
    c1_cells = res_trained["final_n_cells"] >= 32
    c2_alpha = (not math.isnan(alpha_trained)) and alpha_trained >= 0.6
    c3_v14_strict = (
        res_trained["final_n_cells"] > res_random["final_n_cells"] * 1.1
        and res_trained["final_phi"] > res_random["final_phi"] * 1.1
    )
    c4_chat = ko_pass_count >= 3

    n_pass = sum([c1_cells, c2_alpha, c3_v14_strict, c4_chat])
    star_label = {4: "★★★★★", 3: "★★★★", 2: "★★★", 1: "★★", 0: "★"}[n_pass]

    if n_pass == 4:
        verdict = "PASS_5_STAR_FIRST_REACH"
    elif c3_v14_strict is False:
        verdict = "FAIL_V14_VIOLATED"
    elif n_pass >= 3:
        verdict = f"PARTIAL_PASS_{n_pass}_OF_4"
    else:
        verdict = f"FAIL_OR_CARRY_{n_pass}_OF_4"

    out = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "user_verbatim": "OK FIRE PATH_A V5_ANIMA_LONG_TRAJECTORY_SMOKE $0",
        "config": {
            "ckpt": str(CKPT_PATH),
            "n_tokens_per_prompt": N_TOKENS_PER_PROMPT,
            "n_total_tokens": N_TOKENS_PER_PROMPT * len(ALL_PROMPTS),
            "mitosis_stride": MITOSIS_STRIDE,
            "top_k": TOP_K,
            "temperature": TEMPERATURE,
            "initial_cells": INITIAL_CELLS,
            "max_cells": MAX_CELLS,
            "c_dim": C_DIM,
            "d_model": D_MODEL,
            "seed": SEED,
        },
        "trained_cells64": res_trained,
        "v14_random_mirror": res_random,
        "alpha": {
            "trained": alpha_trained if not math.isnan(alpha_trained) else None,
            "random": alpha_random if not math.isnan(alpha_random) else None,
        },
        "ko_chat": {
            "ko_prompts_passed": ko_pass_count,
            "ko_prompts_total": ko_total,
            "per_prompt_ko_chars": [
                {"prompt": p["prompt"], "ko_chars": p["ko_chars_in_gen"]}
                for p in res_trained["per_prompt"] if p["is_korean_prompt"]
            ],
        },
        "five_star_criteria": {
            "C1_cells_grow_8_to_32plus": {
                "pass": c1_cells,
                "value": res_trained["final_n_cells"],
                "threshold": 32,
            },
            "C2_alpha_ge_0_6": {
                "pass": c2_alpha,
                "value": alpha_trained if not math.isnan(alpha_trained) else None,
                "threshold": 0.6,
            },
            "C3_v14_strict_substrate_coupled": {
                "pass": c3_v14_strict,
                "trained_cells": res_trained["final_n_cells"],
                "random_cells": res_random["final_n_cells"],
                "trained_phi": res_trained["final_phi"],
                "random_phi": res_random["final_phi"],
                "rule": "trained.cells > 1.1*random.cells AND trained.phi > 1.1*random.phi",
            },
            "C4_chat_ko_3_of_5": {
                "pass": c4_chat,
                "value": ko_pass_count,
                "threshold": 3,
            },
        },
        "n_criteria_passed": n_pass,
        "star_rating": star_label,
        "verdict": verdict,
        "honest_c3": [
            "Real-substrate variant (cells64_final.pt = 18.5M byte-LM, 218MB) of prior toy 864-param mitosis smokes; same MitosisV5Engine wrapper + same seed=42 protocol so V14 comparison is apples-to-apples within this run.",
            "Mitosis cells (C_DIM=64) attached SIDE-CHANNEL via fixed seeded Linear(384→64) projecting host last-layer hidden hint (head_a.weight.T @ softmax(logits)). Host model itself NOT modified — pure inference probe.",
            "Mitosis received ~100 process calls over 1000 generated tokens (stride=10); split_patience=3 means up to ~33 splits theoretically possible from initial 8 → 41 cells. Long-trajectory at this stride is mechanism check, NOT chat eval (chat capability tracked separately via per-prompt KO syllable count).",
            "V14 mirror = same arch + same fixed projection seed but RANDOM host weights (no ckpt load, init via PyTorch defaults under same torch.manual_seed=42). If trained ≈ random in cells/Φ → mechanism is Lorenz-driven (already shown in prior toy run, expected here too).",
            "Lorenz autonomous chaos (σ=10, ρ=28, β=8/3) is the dominant driver of cell tension divergence; per the prior 10K-turn toy smoke this masks substrate-coupling and is the proximate cause of V14 violation. Real substrate may amplify or cancel this — the primary novel observation in THIS run.",
            "α regression filters duplicate n_cells values (avoids x-saturation when n_cells hits MAX_CELLS=64). If <4 unique n_cells points, α=NaN and C2 fails.",
            "Korean syllable check is the sampling-test reality (BG-R1 audit in recovery dir found 0/64 KO chars in similar setup); a positive C4 here would CONTRADICT the prior degeneracy finding and warrant investigation.",
            "Resource: Mac CPU only (strict). No H100 fire. Single-pass ckpt load + V14 mirror sequential to control RAM at ~700MB free.",
        ],
    }

    out_path = OUT_DIR / "result.json"
    with out_path.open("w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"\n=== VERDICT ===")
    print(f"  trained: cells={res_trained['final_n_cells']} phi={res_trained['final_phi']:.3f} "
          f"splits={res_trained['n_splits']}")
    print(f"  random:  cells={res_random['final_n_cells']} phi={res_random['final_phi']:.3f} "
          f"splits={res_random['n_splits']}")
    print(f"  α trained={alpha_trained}  random={alpha_random}")
    print(f"  KO chat: {ko_pass_count}/{ko_total}")
    print(f"  C1 cells≥32:    {c1_cells}")
    print(f"  C2 α≥0.6:       {c2_alpha}")
    print(f"  C3 v14_strict:  {c3_v14_strict}")
    print(f"  C4 chat≥3/5:    {c4_chat}")
    print(f"  → {n_pass}/4 passed → {star_label}")
    print(f"  verdict: {verdict}")
    print(f"  result: {out_path}")


if __name__ == "__main__":
    main()
