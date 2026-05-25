---
artifact: H_154 verify prerequisite list
date: 2026-05-11
cross_link: hypotheses/H_154_anima_voice_consciousness_direct.md
---

# Prerequisites — what must land before H1-H8 measurable

## Gate-1 — model + corpus (highest impact)

| Prerequisite | 상태 | Blocks | 비고 |
|--------------|------|--------|------|
| **ANIMA-VOICE 모델 build** (8 RVQ × 1024 × 384d × 24 kHz vocoder) | **MISSING** | H1, H2, H3, H5, H6 (input_dim), H7, H8 | spec only — H_154 pre-register-frozen, no build |
| **ConsciousLM 384d intent encoder** | OK | H6 | clm-v4-mk2-v1 등 existing |
| **audio corpus** (24 kHz, 6 emotion × 4 prosody, ≥ 720 samples, labeled) | TBD | H3, H4, H5 | corpus build cycle separate |
| **prompt set** (≥ 30 diverse intents) | TBD | H2, H5, H6, H7 | ConsciousLM 학습 corpus 에서 sampling 가능 |

## Gate-2 — judge / evaluator infrastructure

| Prerequisite | 상태 | Blocks | 비고 |
|--------------|------|--------|------|
| **MOSNet (또는 human MOS panel)** | MISSING | H3, H5 | MOSNet pretrained weights download or human pipeline build |
| **emotion classifier (Ekman 6-class)** | TBD | H4 | wav2vec2-emotion fine-tuned pretrained 외부 사용 가능 |
| **silence detector (audio energy)** | OK | H7 | trivial RMS — harness `_audio_silence` 에 stub |
| **streaming-applicable Φ measurement** | MISSING | H8 | L6 — current Φ 는 non-streaming. streaming Φ 정의 + 측정 infra 별도 |

## Gate-3 — runtime infrastructure

| Prerequisite | 상태 | Blocks | 비고 |
|--------------|------|--------|------|
| **packet loss simulator** (5/10/20% drop) | TBD | H5 | netem 또는 Python random mask. 단순 |
| **gate state controller** (C, W injection) | MISSING | H7 | ANIMA-VOICE runtime API 와 함께 land 필요 |
| **streaming inference pipeline** | MISSING | H2 latency, H5 PLC, H8 Φ | model 자체와 함께 |
| **hardware tier 명시** (CPU? GPU? edge?) | UNSPECIFIED | H2 (latency 의미 dependent) | H_154 미명시 — Cycle 4 measurement 시 결정 |

## Gate-4 — formal / safety

| Prerequisite | 상태 | Blocks | 비고 |
|--------------|------|--------|------|
| **Law 81 dual-gate formal verification** | MISSING | H7 safety claim (beyond sampling) | L5 — F5 safety-critical |
| **MOS blinded human panel recruitment** | MISSING | H3 정식 (proxy MOSNet 으로 대체 가능) | TP-1 contract |
| **anima-agent CLI turn-taking instrumentation** | TBD | TP-2 (별도 H_154 sub-criterion) | H1-H8 와 별개 |

## Dependency graph (textual)

```
ANIMA-VOICE model build  ──┬─→ H1, H2, H6, H7, H8
                           │
audio corpus  ─────────────┴─→ H3, H4, H5
                           │
MOSNet  ───────────────────┴─→ H3, H5
                           │
emotion clf  ──────────────┴─→ H4
                           │
streaming Φ  ──────────────┴─→ H8
                           │
gate controller  ──────────┴─→ H7
                           │
PLC simulator  ────────────┴─→ H5
```

## Critical path (longest blocking chain)

1. **ANIMA-VOICE minimum reference impl** (8 RVQ + vocoder) — H_154 build cycle, est. 3-6 weeks
2. **streaming Φ measurement** — research-level open question (L6)
3. **MOSNet weights or human panel** — 1-2 weeks (MOSNet) or 2-4 weeks (human recruitment)

→ **earliest measurable end-to-end H1-H8**: ANIMA-VOICE land + Φ streaming + MOSNet → est. 6-10 weeks
