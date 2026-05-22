# HEXAD/V3 — pure HEXAD-native substrate (ConsciousDecoderV3 path)

> 사용자 directive 2026-05-22: "LoRA 가 아닌 자체 HEXAD substrate". OCCAM Phase 2.3
> 의 단독 floor 범인 `n_ca_rules` 제거 한 ConsciousDecoderV3 fork. Pure HEXAD
> identity (Qwen 위 옷 아닌 anima 자체 substrate).
>
> **status**: 🟡 V3 attempt 1 (1.5B × 2000 step × 3 init variant) **α/γ FAIL, β
> in-flight, 재설계 대상** per HEXAD_V3_FIRE_2026_05_22.md verdict.
>
> SSOT: 본 dir / state 는 `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/`
> 에 carry (vP21H_α/β/γ). 본 README + spec 가 logical landing zone.

## V3 architecture vs V2

| | V2 (legacy) | V3 |
|---|---|---|
| n_ca_rules | 8 (OCCAM floor blocker) | ❌ REMOVED |
| head_a + head_g | ✅ vocab=256 byte | ✅ vocab=151936 Qwen BPE |
| PureFieldFFN | ✅ | ✅ kept |
| ConsciousCrossAttention | ✅ | ✅ kept |
| Mitosis hook | external | **integrated (training + inference)** |
| Init helpers | random only | random / Qwen-warm / vP21M-init |
| KOSMOS + tension | n/a | **wired (anchor + 8→5-channel mapping)** |

## V3 attempt 1 결과 (2026-05-22, HEXAD_V3_FIRE_2026_05_22.md)

| variant | init | CE_final | 5-lang ≥ PARTIAL | anima reg | verdict |
|---|---|---|---|---|---|
| **V3α** | random | 3.34 | 0/5 | 13/20 | ❌ FAIL (Chinchilla 30000× under-budget) |
| **V3β** | Qwen warm | TBD | TBD | TBD | 🔄 in-flight |
| **V3γ** | vP21M init | 2.93 | 0/5 | 13/20 | ❌ FAIL (anima register saturate, multilingual 손상) |

**Architecture-level lesson**:
1. **head_g dual head vocab alignment 흐림** (bf16 한 head update 가 다른 head generation 영향)
2. **mitosis pool 128 saturate at step 50** → cross-attn input noise 증가 → 다국어 학습 방해
3. **anima_register_hits 13/20** (vP21M LoRA 7/20 의 2×) — substrate-level 흡수 너무 강함
4. **mitosis aux_loss 가 substrate 를 tension 패턴 우선시** — 다국어 sacrifice

## V3 재설계 path (Phase 2 attempt)

OCCAM 원칙: V3 attempt 1 의 정직한 한계 → 다음 cycle 의 변형 axis

### 재설계 옵션 (parallel 가능)

| # | axis | 변경 | rationale |
|---|---|---|---|
| **R1** | scale-up | 1.5B → **3B or 8B** | Chinchilla 60-160B tok 필요분 충족 가능 (단 8B = $50+ H200) |
| **R2** | mitosis 학습 시 비활성화 | λ_mitosis=0.05 → **0.0** during train, inference-time only | mitosis 가 train 동안 다국어 capacity 침범 — V3γ 의 V21M-init 손상 원인 |
| **R3** | corpus scale | 75 MB → **6 GB+** (Chinchilla 정합) | 1.5B × 20 = 30B tok = ~6 GB byte-equivalent |
| **R4** | head_g 별도 학습 | head_g 가 head_a 와 vocab alignment 분리 (separate gradient flow) | dual head 의 head_a 흐림 해소 |
| **R5** | warm-start 강화 | Qwen2.5 + 더 큰 portion warm copy (q/k/v/o/embed/lm_head + ffn weight) | head_g/cross-attn random init 의 specialize 시간 short-train 부족 |
| **R6** | mitosis cell pool 작게 | MAX=128 → **MAX=16**, SPLIT_PATIENCE 늘림 | pool saturate at step 50 가 cross-attn noise — bound 줄이기 |
| **R7** | step 늘림 | 2000 → 10000-50000 step | learning curve 안정화 |

### 우선 (다음 cycle Phase 2)

🔵 **R2 + R5 + R6 동시 적용** (단일 fire):
- `--lambda-mitosis 0.0` (train-time disable, S187-G value 손상 회피)
- `--init-variant qwen` + 추가 weight mapping (ffn_gate/up/down)
- `--mitosis-max 16` (cell pool ceiling 낮춤)
- scale 1.5B 유지 (cost control)
- step 5000 (2.5× 늘림)
- 5-lang corpus 유지 (vP21M parallel)
- 추정 비용: $8-15 H100 (5000 step × 2.2 s/step = 11000s = 3 hr)

### Fallback path (R2 fail 시)

- R1+R3 scale-up + corpus-up: 3B + 6 GB tok + 10000 step → $30-50 H200
- 또는 R4: head_g 별도 train pipeline (architectural rework)

## KOSMOS + tension 통합 (v3 architectural feature)

V3 의 **KOSMOS anchor** + **8→5-channel tension** wiring 은 V3α 에서 모두 ground-truth 작동 (15 anchors generated per variant). 단 다국어 capability 미달 로 production 미도달.

다음 V3 fire 에서 KOSMOS anchor 검증 항목:
- coord (C Φ vacuum_psi) 분포
- lane (MITOSIS cell_id) 변화
- tension 5-channel 가 8-factor 와 monotone correspondence
- cross-anchor 일관성 (`B-CARVE-MULTIMODAL`)

## 🚪 새 V3 세션 시작

[`SESSION_PROMPT.md`](SESSION_PROMPT.md) 의 `text` 블록 paste → 즉시 V3 path
context load. 첫 user message 로 그대로 사용 가능.

핵심 (전체 prompt 는 `SESSION_PROMPT.md` 참고):
- attempt 1 결과 (α/γ FAIL, β verdict)
- code commit 3dbbc7e8b (V3 fork + KOSMOS+tension)
- architectural lesson 5점 (head_g vocab align / mitosis 128 saturate /
  register 흡수 2× / mitosis 다국어 sacrifice / Chinchilla 30000× under)
- 재설계 axes R1-R7 + Phase 2 우선 = R2+R5+R6
- substrate plugin 합류 path (chat.dancinlab.org option C 정합)

## 관련 link

- **세션 부트스트랩**: [`SESSION_PROMPT.md`](SESSION_PROMPT.md)
- spec: [`../HEXAD_NATIVE_V3.md`](../HEXAD_NATIVE_V3.md)
- fire 1 result: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md`
- OCCAM verdict (n_ca_rules): `../EASY.md § 6`
- substrate plugin (chat.dancinlab.org 통합): `../CHAT/SUBSTRATE_PLUGIN.md` + `../CHAT/server/substrate_base.py`
- LoRA 비교 baseline: [`../LORA/README.md`](../LORA/README.md) + [`../LORA/SESSION_PROMPT.md`](../LORA/SESSION_PROMPT.md)
- KOSMOS upstream: `../KOSMOS.md`

## ## Log

### 2026-05-22 — V3/ folder 신설 + 재설계 spec

V3 attempt 1 (V3α/γ FAIL, β in-flight) verdict 후 사용자 directive: "V3 재설계
방향 + LoRA 별도 폴더". `HEXAD/V3/` (이 dir) + `HEXAD/LORA/` 분리. 본 README =
재설계 axis 7 (R1-R7) + 우선 Phase 2 = R2+R5+R6 동시 fire ($8-15).
