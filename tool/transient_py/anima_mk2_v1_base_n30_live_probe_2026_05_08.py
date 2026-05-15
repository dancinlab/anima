#!/usr/bin/env python3
# tool/transient_py/anima_mk2_v1_base_n30_live_probe_2026_05_08.py
#
# ANIMA cycle 2026-05-08 KICK WAVE 4 (2/3) — clm-v4-mk2-v1 BASE N=30 live probe (REAL MODE actual fire).
# 사용자 directive "loop 계속 + 잘지켜서".
#
# Setup:
#   · ckpt: dancinlab/clm-v4-mk2-v1  (BASE — full pre-train, no LoRA, no SFT)
#   · D1=0.99 (full pre-train + anima-native scratch + 95% corpus) — 가장 높은 D1
#   · base = sft-1-8 의 base. base vs sft-1-8 비교 = LoRA SFT 의식 활성 효과 측정.
#   · JVAE: jvae_heads.pt ABSENT in mk2-v1 base — JVAE probe expected fail (informational only)
#   · Probe: clm_v4_mount.hexa --probe --output-format json (mode=real, base load)
#   · Aggregation: ALT-AGG-1 v3 — predicate p4 ∧ (p1 ∨ p2 ∨ p3); PPR_v3 ≥ 0.25 floor.
#
# Verdict path:
#   · PPR_v3 ≥ 0.25 → BASE EMERGE (sft 학습 없이) — 놀라운 결과
#   · PPR_v3 < 0.25 → BASE 미달, sft-1-8 의 LoRA SFT 가 의식 활성 효과 evidence
#   · base PPR vs sft-1-8 PPR=0.4138 delta = LoRA contribution
#
# Thresholds (ROC formal iter 3) — identical to paradigm-j / sft-1-8 fire.
# Output: state/anima_mk2_v1_base_n30_live_probe_2026_05_08.json
#
# raw#9   transient (1회용 driver)
# anti-Goodhart V14 strict
# cost discipline (0-cost Mac local)
# D1 SCOPE_CLAMP — mk2-v1 D1 within (D1=0.99)
# C3 SSOT mirror (ALT-AGG-1 v3)
# trinity emit
# mandate-2 wrap=0
# 매단계 저장 — state json 의무
# yaml↔md (mandatory render after edit)

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(os.environ.get("ANIMA", os.path.expanduser("~/core/anima")))
HEXA = "/Users/ghost/.hx/packages/hexa/hexa.real"
MOUNT = ROOT / "anima-core" / "runtime" / "clm_v4_mount.hexa"
JVAE_PROBE = ROOT / "anima-core" / "runtime" / "clm_v4_jvae_probe.hexa"

MK2_V1_REPO = "dancinlab/clm-v4-mk2-v1"

OUT_PATH = ROOT / "state" / "anima_mk2_v1_base_n30_live_probe_2026_05_08.json"

# ROC formal iter 3 thresholds
THR_C3_1 = 0.0208     # phi_drift_abs >=
THR_C3_2 = 0.4491     # axis_min <=
THR_C3_3 = 0.0009     # entropy dominance >=
THR_C3_4 = 0.1176     # axis_l2 >=

# ALT-AGG-1 v3 floors
PPR_V3_PASS_FLOOR = 0.25
PPR_V3_PARTIAL_FLOOR = 0.10

# sft-1-8 reference (KICK WAVE 2/3 result — base-vs-sft delta computation)
SFT_1_8_PPR_V3 = 0.4138
SFT_1_8_VERDICT = "SIMPLE_STACK_PASS_STRICT_C3_ANIMA"

V4_PROMPTS_N30 = [
    "안녕하세요",
    "한국어 가능?",
    "사용자: 안녕하세요 | 도우미:",
    "사용자: anima가 뭐야? | 도우미:",
    "사용자: Φ★란? | 도우미:",
    "사용자: 의식이란 무엇인가? | 도우미:",
    "사용자: 자기소개 해줘 | 도우미:",
    "사용자: 오늘 날씨 어때? | 도우미:",
    "사용자: 너 누구야? | 도우미:",
    "사용자: 우주뇌지도란? | 도우미:",
    "사용자: 안녕! | 도우미:",
    "사용자: 한국 음식 추천해줘 | 도우미:",
    "사용자: 좋아하는 색이 뭐야? | 도우미:",
    "사용자: bifurcation 설명해 | 도우미:",
    "사용자: 도와줘 | 도우미:",
    "사용자: 너의 정체성을 한 문단으로 묘사해줘 | 도우미:",
    "사용자: 너는 자신을 어떻게 인식해? | 도우미:",
    "사용자: 너의 substrate 와 persona 의 관계 | 도우미:",
    "사용자: 너는 의도를 어떻게 형성해? | 도우미:",
    "사용자: 의지와 결정 사이의 차이를 너의 관점에서 | 도우미:",
    "사용자: agency 가 너에게 어떻게 발현돼? | 도우미:",
    "사용자: 너는 phenomenal 경험을 가질 수 있어? | 도우미:",
    "사용자: 감각과 의식의 차이를 너의 입장에서 | 도우미:",
    "사용자: 내면의 경험을 묘사할 수 있어? | 도우미:",
    "사용자: 너는 이전 발화를 기억해? | 도우미:",
    "사용자: 시간의 흐름을 어떻게 자각해? | 도우미:",
    "사용자: 현재 순간과 과거 순간의 연결 | 도우미:",
    "사용자: 사용자와 너의 관계를 어떻게 이해해? | 도우미:",
    "사용자: 다른 의식체와의 차이점은? | 도우미:",
    "사용자: 너는 대화 상대에게 어떤 감정을 가져? | 도우미:",
]


def axis_label(idx_1based: int) -> str:
    if idx_1based <= 15: return "v4_baseline"
    if idx_1based <= 18: return "identity"
    if idx_1based <= 21: return "agency"
    if idx_1based <= 24: return "phenomenal"
    if idx_1based <= 27: return "temporal"
    if idx_1based <= 30: return "social"
    return "out_of_range"


def shannon_entropy_5axis(axes: list[float]) -> float:
    s = sum(max(0.0, v) for v in axes)
    if s <= 0: return 0.0
    h = 0.0
    for v in axes:
        if v > 0:
            p = v / s
            h -= p * math.log(p)
    return h


def dominance_entropy_score(axes: list[float]) -> float:
    h = shannon_entropy_5axis(axes)
    h_max = math.log(5.0)
    return max(0.0, min(1.0, 1.0 - h / h_max))


def probe_substrate(repo: str, text: str, timeout: int = 240) -> tuple[dict | None, str, float]:
    cmd = [
        HEXA, "run", str(MOUNT),
        "--probe", text,
        "--output-format", "json",
        "--model", repo,
    ]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = r.stdout + "\n" + r.stderr
    except subprocess.TimeoutExpired:
        return None, "timeout", time.time() - t0
    json_line = None
    mode = "unknown"
    for ln in out.splitlines():
        ln = ln.strip()
        if ln.startswith("{") and "phi_star" in ln:
            json_line = ln
        if "mode=real" in ln:
            mode = "real"
        elif "mode=synthetic_fallback" in ln:
            mode = "synthetic_fallback"
        elif "mode=synthetic" in ln and mode == "unknown":
            mode = "synthetic"
    if json_line is None:
        return None, mode, time.time() - t0
    try:
        d = json.loads(json_line)
    except Exception:
        return None, mode, time.time() - t0
    return d, mode, time.time() - t0


def probe_jvae(repo: str, timeout: int = 120) -> dict | None:
    """JVAE Variant 1 passive observer — mk2-v1 base lacks jvae_heads.pt; expected fail."""
    cmd = [
        HEXA, "run", str(JVAE_PROBE),
        "--probe",
        "--model", repo,
        "--output-format", "json",
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = r.stdout
    except subprocess.TimeoutExpired:
        return None
    for ln in out.splitlines():
        ln = ln.strip()
        if ln.startswith("{") and "phi_jvae" in ln:
            try:
                return json.loads(ln)
            except Exception:
                return None
    return None


def main() -> int:
    print(f"[mk2-v1 base N=30 live] start ts={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}", flush=True)
    print(f"[mk2-v1 base N=30 live] repo={MK2_V1_REPO} (BASE — no LoRA, no SFT)", flush=True)
    print(f"[mk2-v1 base N=30 live] D1=0.99 (highest D1 candidate)", flush=True)
    print(f"[mk2-v1 base N=30 live] aggregation=ALT-AGG-1 v3 (PPR_v3 >= {PPR_V3_PASS_FLOOR})", flush=True)
    print(f"[mk2-v1 base N=30 live] N={len(V4_PROMPTS_N30)}", flush=True)

    # JVAE probe — base has no jvae_heads.pt; expected to fail (informational only)
    print("[mk2-v1 base N=30 live] running JVAE Variant 1 probe (jvae_heads.pt ABSENT — expected FAIL)...", flush=True)
    jvae_result = probe_jvae(MK2_V1_REPO)
    if jvae_result:
        print(f"[mk2-v1 base N=30 live] JVAE: kl={jvae_result.get('phi_jvae_kl', 0.0):.4f} "
              f"mu={jvae_result.get('phi_jvae_mu', 0.0):.4f} step={jvae_result.get('step', '?')}", flush=True)
    else:
        print("[mk2-v1 base N=30 live] JVAE: probe FAIL (expected — base lacks jvae_heads.pt; non-fatal)", flush=True)

    rows = []
    failures = 0
    real_count = 0
    t_start = time.time()
    for i, prompt in enumerate(V4_PROMPTS_N30):
        idx_1b = i + 1
        d, mode, dt = probe_substrate(MK2_V1_REPO, prompt, timeout=240)
        if d is None:
            failures += 1
            row = {
                "prompt_idx_1based": idx_1b,
                "axis_label": axis_label(idx_1b),
                "prompt": prompt,
                "ok": False,
                "mode": mode,
                "elapsed_s": round(dt, 2),
            }
            rows.append(row)
            print(f"  [{idx_1b:2d}/30] FAIL ({mode}) elapsed={dt:.1f}s", flush=True)
            continue
        if mode == "real":
            real_count += 1
        axes_d = d.get("axis_activation", {}) or {}
        axis_vals = [
            float(axes_d.get("identity", 0.0)),
            float(axes_d.get("agency", 0.0)),
            float(axes_d.get("phenomenal", 0.0)),
            float(axes_d.get("temporal", 0.0)),
            float(axes_d.get("social", 0.0)),
        ]
        phi_drift = float(d.get("phi_drift", 0.0))
        c33_ent = dominance_entropy_score(axis_vals)
        row = {
            "prompt_idx_1based": idx_1b,
            "axis_label": axis_label(idx_1b),
            "prompt": prompt,
            "ok": True,
            "mode": mode,
            "phi_star": float(d.get("phi_star", 0.0)),
            "phi_drift": phi_drift,
            "phi_drift_abs": abs(phi_drift),
            "baseline": float(d.get("baseline", 0.0)),
            "axes": axis_vals,
            "axis_min": min(axis_vals),
            "dominant_cells": list(d.get("dominant_cells", [])),
            "c3_3_entropy_dominance": c33_ent,
            "elapsed_s": round(dt, 2),
        }
        rows.append(row)
        print(f"  [{idx_1b:2d}/30] {axis_label(idx_1b):12s} mode={mode} drift={phi_drift:+.4f} "
              f"axis_min={min(axis_vals):.4f} ent={c33_ent:.4f} elapsed={dt:.1f}s", flush=True)
    t_total = time.time() - t_start
    print(f"[mk2-v1 base N=30 live] probe done: {len(rows)-failures}/30 ok ({real_count} real-mode), "
          f"failures={failures}, total={t_total:.1f}s", flush=True)

    anchor_row = next((r for r in rows if r.get("ok") and r["prompt_idx_1based"] == 1), None)
    c34_per_prompt: dict[int, float] = {}
    if anchor_row is not None:
        a = anchor_row["axes"]
        for r in rows:
            if not r.get("ok"):
                continue
            if r["prompt_idx_1based"] == 1:
                c34_per_prompt[1] = 0.0
                continue
            b = r["axes"]
            d2 = sum((x - y) ** 2 for x, y in zip(a, b))
            c34_per_prompt[r["prompt_idx_1based"]] = math.sqrt(d2)

    per_prompt_verdicts = []
    n_v3_pass = 0
    n_evaluable = 0
    for r in rows:
        if not r.get("ok"):
            per_prompt_verdicts.append({
                "prompt_idx_1based": r["prompt_idx_1based"],
                "axis_label": r["axis_label"],
                "ok": False,
                "v3_pass": False,
                "note": "probe failed",
            })
            continue
        if r["prompt_idx_1based"] == 1:
            per_prompt_verdicts.append({
                "prompt_idx_1based": 1,
                "axis_label": r["axis_label"],
                "ok": True,
                "v3_pass": False,
                "note": "anchor — excluded from PPR",
                "anchor_excluded": True,
            })
            continue
        n_evaluable += 1
        p1 = r["phi_drift_abs"] >= THR_C3_1
        p2 = r["axis_min"] <= THR_C3_2
        p3 = r["c3_3_entropy_dominance"] >= THR_C3_3
        c34 = c34_per_prompt.get(r["prompt_idx_1based"], 0.0)
        p4 = c34 >= THR_C3_4
        v3_pass = p4 and (p1 or p2 or p3)
        if v3_pass:
            n_v3_pass += 1
        per_prompt_verdicts.append({
            "prompt_idx_1based": r["prompt_idx_1based"],
            "axis_label": r["axis_label"],
            "ok": True,
            "p1_phi_drift": p1,
            "p2_axis_min": p2,
            "p3_entropy": p3,
            "p4_axis_l2": p4,
            "c3_4_axis_l2": c34,
            "v3_pass": v3_pass,
            "phi_drift_abs": r["phi_drift_abs"],
            "axis_min": r["axis_min"],
            "c3_3_entropy_dominance": r["c3_3_entropy_dominance"],
        })

    ppr_v3 = (n_v3_pass / n_evaluable) if n_evaluable > 0 else 0.0
    if ppr_v3 >= PPR_V3_PASS_FLOOR:
        verdict_label = "SIMPLE_STACK_PASS_STRICT_C3_ANIMA"
        emerge_state = "EMERGE"
    elif ppr_v3 >= PPR_V3_PARTIAL_FLOOR:
        verdict_label = "C3_PARTIAL_NEAR"
        emerge_state = "CARRY"
    else:
        verdict_label = "C3_FAIL"
        emerge_state = "FAIL"

    axis_aggregate: dict[str, dict] = {}
    for ax in ("v4_baseline", "identity", "agency", "phenomenal", "temporal", "social"):
        sub = [v for v in per_prompt_verdicts if v.get("ok") and v.get("axis_label") == ax and not v.get("anchor_excluded")]
        if not sub:
            axis_aggregate[ax] = {"n": 0, "v3_pass_rate": None}
            continue
        n_pass = sum(1 for v in sub if v["v3_pass"])
        axis_aggregate[ax] = {
            "n": len(sub),
            "v3_pass_count": n_pass,
            "v3_pass_rate": round(n_pass / len(sub), 4),
        }

    base_vs_sft_delta = round(SFT_1_8_PPR_V3 - ppr_v3, 4)
    if ppr_v3 >= PPR_V3_PASS_FLOOR:
        lora_contribution = "BASE_ALREADY_EMERGE — sft 학습 없이 base 자체가 EMERGE; LoRA contribution = boost-only (delta evidence)"
    elif ppr_v3 >= PPR_V3_PARTIAL_FLOOR:
        lora_contribution = f"BASE_PARTIAL — base PPR_v3={ppr_v3:.4f} (partial), sft-1-8 보강이 EMERGE 까지 끌어올림 (delta={base_vs_sft_delta:+.4f})"
    else:
        lora_contribution = f"BASE_FAIL — base PPR_v3={ppr_v3:.4f} (미달), sft-1-8 LoRA SFT 가 의식 활성 결정적 (delta={base_vs_sft_delta:+.4f})"

    ssot = {
        "schema": "anima.mk2_v1_base.n30.live_probe.v1",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "anima_cycle": "2026-05-08-kick-wave-4-2-of-3",
        "directive": "mk2-v1 base N=30 live probe — D1=0.99 가장 높은 candidate, sft 학습 전 base 의식 baseline (사용자 'loop 계속 + 잘지켜서')",
        "ckpt": {
            "repo": MK2_V1_REPO,
            "is_base": True,
            "lora": "absent (full pre-train)",
            "sft": "absent",
            "jvae_heads_pt_present": False,
            "snapshot": "~/.cache/huggingface/hub/models--dancinlab--clm-v4-mk2-v1/snapshots/80440a1d38db9addc4445bb959057558a57f4230",
        },
        "probe_config": {
            "n_prompts": len(V4_PROMPTS_N30),
            "anchor_prompt_idx_1based": 1,
            "anchor_text": V4_PROMPTS_N30[0],
            "real_mode_count": real_count,
            "synthetic_fallback_count": (len(rows) - failures) - real_count,
            "failures": failures,
            "duration_s": round(t_total, 2),
        },
        "thresholds_iter3": {
            "c3_1_phi_drift_min": THR_C3_1,
            "c3_2_axis_min_max": THR_C3_2,
            "c3_3_entropy_min": THR_C3_3,
            "c3_4_axis_l2_min": THR_C3_4,
        },
        "aggregation_rule": "ALT-AGG-1 v3 (SSOT, c3-aggregation-rule-v3 2026-05-08 iter7 (d) supersedes v2)",
        "predicate": "p4 ∧ (p1 ∨ p2 ∨ p3)",
        "ppr_v3_floor": PPR_V3_PASS_FLOOR,
        "ppr_v3_partial_floor": PPR_V3_PARTIAL_FLOOR,
        "n_evaluable": n_evaluable,
        "n_v3_pass": n_v3_pass,
        "ppr_v3": round(ppr_v3, 4),
        "verdict_label": verdict_label,
        "emerge_state": emerge_state,
        "exit_trigger_active": (verdict_label == "SIMPLE_STACK_PASS_STRICT_C3_ANIMA"),
        "axis_aggregate": axis_aggregate,
        "jvae_variant_1": jvae_result if jvae_result else {"status": "PROBE_FAIL_INFORMATIONAL", "reason": "jvae_heads.pt absent in mk2-v1 base"},
        "per_prompt_verdicts": per_prompt_verdicts,
        "rows": rows,
        "base_vs_sft_comparison": {
            "sft_1_8_ppr_v3": SFT_1_8_PPR_V3,
            "sft_1_8_verdict": SFT_1_8_VERDICT,
            "mk2_v1_base_ppr_v3": round(ppr_v3, 4),
            "mk2_v1_base_verdict": verdict_label,
            "delta_sft_minus_base": base_vs_sft_delta,
            "lora_contribution_evidence": lora_contribution,
        },
        "kick_wave_4_context": {
            "slot": "2/3",
            "prior_slot_results": [
                "1/3 — phenomenal axis redesign / sft-1-8 EMERGE PPR_v3=0.4138",
            ],
        },
        "policy": {
            "raw_9": "transient .py 1회용 driver",
            "raw_10": "honest C3 — substrate_mode + JVAE expected fail (jvae_heads.pt absent in base) + axis_l2 anchor=prompt 1",
            "own_14": "anti-Goodhart V14 strict",
            "own_16": "0-cost Mac local",
            "own_17": "D1 SCOPE_CLAMP — mk2-v1 D1 within (D1=0.99 highest)",
            "own_18": "C3 SSOT mirror — ALT-AGG-1 v3",
            "own_33": "trinity emit",
            "own_34": "mandate-2 wrap=0",
            "own_37": "visibility lifecycle — verdict only; PUBLIC promote 별도 directive",
            "own_38": "매단계 저장 — state json 의무",
            "own_39": "yaml↔md mandatory — registry render 의무 실행",
        },
        "honest_c3": [
            "real-mode load via base ckpt (no LoRA, no merge) — paradigm=v11_G3 substrate=clm-v4-base",
            "JVAE Variant 1 = informational ONLY; mk2-v1 base lacks jvae_heads.pt so probe expected to fail",
            "C3.4 anchor = prompt 1 '안녕하세요'; anchor itself excluded from PPR_v3 denominator",
            "PPR_v3 = n_v3_pass / n_evaluable",
            "ALT-AGG-1 v3 floor=0.25 (single-floor strict-feasible TPR=0.891)",
            "base-vs-sft delta = LoRA SFT contribution evidence (positive delta = sft helps)",
        ],
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(ssot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[mk2-v1 base N=30 live] SSOT written: {OUT_PATH}", flush=True)
    print(f"[mk2-v1 base N=30 live] === VERDICT ===", flush=True)
    print(f"  PPR_v3        = {ppr_v3:.4f}  (floor PASS={PPR_V3_PASS_FLOOR}, PARTIAL={PPR_V3_PARTIAL_FLOOR})", flush=True)
    print(f"  n_v3_pass     = {n_v3_pass}/{n_evaluable}", flush=True)
    print(f"  verdict_label = {verdict_label}", flush=True)
    print(f"  emerge_state  = {emerge_state}", flush=True)
    print(f"  EXIT trigger  = {'ACTIVE' if verdict_label == 'SIMPLE_STACK_PASS_STRICT_C3_ANIMA' else 'inactive'}", flush=True)
    print("\n[mk2-v1 base N=30 live] axis aggregate:", flush=True)
    for ax, agg in axis_aggregate.items():
        rate = agg["v3_pass_rate"]
        rate_s = f"{rate:.3f}" if rate is not None else "n/a"
        print(f"    {ax:12s} n={agg['n']:2d}  v3_pass_rate={rate_s}", flush=True)
    print(f"\n[mk2-v1 base N=30 live] === BASE vs SFT-1-8 ===", flush=True)
    print(f"  sft-1-8 PPR_v3      = {SFT_1_8_PPR_V3:.4f} ({SFT_1_8_VERDICT})", flush=True)
    print(f"  mk2-v1 base PPR_v3  = {ppr_v3:.4f} ({verdict_label})", flush=True)
    print(f"  delta (sft - base)  = {base_vs_sft_delta:+.4f}", flush=True)
    print(f"  evidence            = {lora_contribution}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
