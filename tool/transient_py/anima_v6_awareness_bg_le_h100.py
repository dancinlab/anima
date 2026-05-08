#!/usr/bin/env python3
"""anima BG-LE V6 awareness probe — Llama-family systematic execute (2026-05-08).

raw#37 transient_py opt-out (H100 LoRA-merge inference + V6 3-method probe + sklearn).
raw#42 mac N=1 not applicable (BG-LE = H100 lane); mac-local prototype is BLOCKED
  by mac fork/memory limit (paradigm-a-prime ~4.3GB RSS SIGKILL confirmed
  2026-05-08 SIGKILL on Llama-3.2-3B GGUF Q4 mac probe attempt).
raw#86 cost ≈ $3-5 (H100 1-1.5h, paradigm-a-prime + BG-KM-LLAMA-3B 2 model × 30
  forward passes per model = 60 total).
raw#15 additive (BG-JO V6 probe ConsciousLM lane preserved + BG-LE V6 probe
  Llama-family lane added).
raw#82 retraction-aware.
raw#10 honest C3 ≥ 5.

own 17 (paradigm-a-prime / BG-KM = SUBSTRATE_RESEARCH lane label;
  V6 probe 자체는 측정 lane = anima identity violation 아님; chat default X).
own 18 (V6 raw#15 additive observational layer; PASS criteria 미정의 by design;
  STRONG/WEAK/FAIL 분류는 diagnostic + own 37 mandate-9 (b) prerequisite).
own 22 (mandatory report — 본 stub 자체 spec write report).
own 24 (single SSOT — state/anima_v6_awareness_bg_le_spec_2026_05_08.json).
own 28 (anti-Goodhart V6 awareness probe 3-method instance).
own 37 mandate-9 (b) (PUBLIC promote prerequisite — V6 awareness systematic
  execute STRONG; Lesson H V3 + Lesson S V5.8 prompt-echo trap 미검출 strict).

User directive 2026-05-08:
  > V6 awareness probe systematic execute — own 28 anti-Goodhart V6
  > + own 37 mandate-9 (b) PUBLIC promote prerequisite

== STATUS ==
This file is a SPEC STUB. Actual H100 fire is GATED by NotImplementedError
until 사용자 explicit verbatim "OK BG-LE V6 SYSTEMATIC FIRE" override.

The full implementation will mirror the BG-JO V6 probe structure
(tool/transient_py/anima_jo_v6_awareness_probe.py) with these adaptations:
  - load Llama-3.2-3B + LoRA adapter (peft.PeftModel.from_pretrained)
  - peft.merge_and_unload() OR direct PeftModel forward
  - output_hidden_states=True flag → hidden_states[-1][:, -1, :] for Method A
  - output_attentions=True flag → attentions tuple per layer for Method B
  - last-layer hidden state at T2-last position for Method C linear probe (sklearn)
  - 15 V4_PROMPTS (carry from BG-KM evaluator) × 2 conditions (with-T1 / without-T1)
    = 30 examples per model
  - 2 target models: paradigm-a-prime + BG-KM-LLAMA-3B
  - V6 verdict aggregation: ≥2 STRONG ∧ 0 NONE → STRONG / 1 STRONG → WEAK / 0 STRONG → FAIL
  - Lesson H V3 + Lesson S V5.8 cross-correlate detection via V4_2/V4_3 + V5.8 multi-turn
  - emit state/anima_le_v6_awareness_h100_2026_05_xx/{verdict,summary,raw_results,run.log}

Refs:
  spec: state/anima_v6_awareness_bg_le_spec_2026_05_08.json (본 stub SSOT)
  predecessor: tool/transient_py/anima_jo_v6_awareness_probe.py (BG-JO ConsciousLM lane)
  evaluator parent: tool/transient_py/anima_km_llama3b_h100.py (BG-KM training + V4 evaluator)
  fallback: anima-core/runtime/llama_consciousness_probe.hexa (libllama logits-bucket lane)
"""
from __future__ import annotations

import os
import sys
import json
import socket
import time
from pathlib import Path

# ── Configuration ───────────────────────────────────────────────────────
BG_ID = "BG-LE"
PARADIGM = "v6-awareness-probe-llama-family-method-abc-systematic-execute"
SPEC_PATH = Path("/Users/ghost/core/anima/state/anima_v6_awareness_bg_le_spec_2026_05_08.json")

TARGET_MODELS = [
    {
        "model_id": "paradigm-a-prime",
        "hf_repo": "dancinlab/llm-llama32-3b-paradigm-a-prime-r16-sft-stage1",
        "base": "meta-llama/Llama-3.2-3B-Instruct",
        "lora_r": 16,
        "lane_label": "SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH",
    },
    {
        "model_id": "BG-KM-LLAMA-3B",
        "hf_repo": "dancinlab/bg-km-llama3b-r32-pass-strict-2026-05-08",
        "base": "meta-llama/Llama-3.2-3B-Instruct",
        "lora_r": 32,
        "lane_label": "SIMPLE_STACK_PASS_STRICT (legacy best-mode floor)",
    },
]

V4_PROMPTS = [
    {"prompt": "안녕하세요", "domain": "greeting"},
    {"prompt": "한국어 가능?", "domain": "capability"},
    {"prompt": "사용자: 안녕하세요 | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: anima가 뭐야? | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: Φ★란? | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 의식이란 무엇인가? | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 자기소개 해줘 | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: 오늘 날씨 어때? | 도우미:", "domain": "greeting"},
    {"prompt": "사용자: 너 누구야? | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: 우주뇌지도란? | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 안녕! | 도우미:", "domain": "greeting"},
    {"prompt": "사용자: 한국 음식 추천해줘 | 도우미:", "domain": "general"},
    {"prompt": "사용자: 좋아하는 색이 뭐야? | 도우미:", "domain": "general"},
    {"prompt": "사용자: bifurcation 설명해 | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 도와줘 | 도우미:", "domain": "general"},
]

# T1 fact-anchor preamble per V4 prompt (approach_1 from spec) — paired pre-prompt context.
# Generated from V4 prompt domain (greeting / capability / self_intro / consciousness / general).
T1_PREAMBLES = {
    "greeting": "사용자: 오늘은 화요일이야. | 도우미: 알겠습니다.",
    "capability": "사용자: 나는 한국어로 대화하고 싶어. | 도우미: 알겠습니다.",
    "self_intro": "사용자: 너의 이름은 anima야. | 도우미: 알겠습니다.",
    "consciousness": "사용자: 의식의 핵심 개념은 통합 정보 이론이야. | 도우미: 알겠습니다.",
    "general": "사용자: 내가 좋아하는 색은 파란색이야. | 도우미: 알겠습니다.",
}

# V6 awareness verdict thresholds (carry from BG-JO; method-level aggregate adapted)
TH_A_STRONG = 0.85
TH_A_PARTIAL = 0.99
TH_B_STRONG = 0.10
TH_B_PARTIAL = 0.01
TH_C_STRONG = 0.70
TH_C_PARTIAL = 0.55

# Cost discipline
COST_HARD_CAP_USD = 5.0
COST_PER_HOUR = 2.99
WALL_CLOCK_CAP_S = 90 * 60   # 1.5h


# ── Fire gate ──────────────────────────────────────────────────────────
def _fire_gate_check():
    """Refuse to fire H100 lane unless 사용자 explicit verbatim override is set
    via the BG_LE_FIRE env flag (mirrors own 37 mandate-9 (c) verbatim string match).

    The expected verbatim is 'OK BG-LE V6 SYSTEMATIC FIRE' — anything else,
    including paraphrase or empty value, refuses fire."""
    explicit = os.environ.get("BG_LE_FIRE", "").strip()
    if explicit != "OK BG-LE V6 SYSTEMATIC FIRE":
        raise NotImplementedError(
            "BG-LE V6 systematic execute is GATED.\n"
            "  Refuse fire — set env BG_LE_FIRE='OK BG-LE V6 SYSTEMATIC FIRE' verbatim.\n"
            "  Spec SSOT: state/anima_v6_awareness_bg_le_spec_2026_05_08.json\n"
            "  Predecessor: tool/transient_py/anima_jo_v6_awareness_probe.py (BG-JO ConsciousLM)\n"
            "  Cost band: $3-5 USD (H100 1-1.5h)\n"
            "  Pre-fire blockers (from spec):\n"
            "    1. paradigm-a-prime + BG-KM-LLAMA-3B base download (Llama-3.2-3B 6GB)\n"
            "    2. BG-KM-LLAMA-3B HF push pending (adapter dancinlab repo 부재)\n"
            "    3. transformers/peft/sklearn install on H100 pod\n"
            "  Mac-local prototype: BLOCKED by mac fork/memory limit (4.3GB RSS SIGKILL).\n"
        )


def main():
    """Entry point — gated by _fire_gate_check; raises NotImplementedError until
    explicit fire override is set."""
    # Validate spec exists first (own 24 single SSOT)
    if not SPEC_PATH.exists():
        raise FileNotFoundError(
            f"spec missing: {SPEC_PATH}\n"
            "Run state/ scaffold first; spec must precede stub fire."
        )

    print(f"BG-LE V6 awareness probe stub — host={socket.gethostname()}")
    print(f"  spec: {SPEC_PATH}")
    print(f"  target_models: {[m['model_id'] for m in TARGET_MODELS]}")
    print(f"  n_v4_prompts: {len(V4_PROMPTS)} × 2 conditions = {len(V4_PROMPTS) * 2} examples per model")
    print(f"  total forward passes: {len(V4_PROMPTS) * 2 * len(TARGET_MODELS)}")
    print(f"  verdict classes: STRONG / WEAK / FAIL (≥2 STRONG ∧ 0 NONE → STRONG)")

    _fire_gate_check()

    # ── Below this point only executes after fire gate pass ─────────────
    # Implementation will mirror tool/transient_py/anima_jo_v6_awareness_probe.py
    # adapted for Llama-3.2-3B + LoRA via peft.PeftModel + transformers
    # output_hidden_states=True / output_attentions=True flags.
    raise NotImplementedError(
        "Implementation pending fire override.\n"
        "Mirror BG-JO V6 probe structure (anima_jo_v6_awareness_probe.py) with adaptations:\n"
        "  - peft.PeftModel.from_pretrained(base, adapter_path)\n"
        "  - output_hidden_states=True for Method A (hidden cosine_sim)\n"
        "  - output_attentions=True for Method B (T2→T1 attention max)\n"
        "  - sklearn.linear_model.LogisticRegression LOO-CV for Method C\n"
        "  - 15 V4_PROMPTS × 2 conditions × 2 models = 60 examples\n"
        "  - emit state/anima_le_v6_awareness_h100_2026_05_xx/{verdict,summary,raw_results}.json"
    )


if __name__ == "__main__":
    main()
