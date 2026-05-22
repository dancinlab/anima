# V3 세션 bootstrap prompt (PURE HEXAD path)

> 새 Claude Code 세션 시작 시 paste — anima V3 (pure HEXAD-native substrate)
> 재설계 작업 context 즉시 load. **ConsciousDecoderV3** path, LoRA path 와 분리.

---

## 📋 Copy + paste this prompt

```text
anima V3 (PURE HEXAD-native) 세션. HEXAD/V3/ + HEXAD/HEXAD_NATIVE_V3.md + VERSIONS.md 가 SSOT.

## 현재 V3 상태 (2026-05-22)
- HEXAD V3 attempt 1 결과 (HEXAD_V3_FIRE_2026_05_22.md):
  - V3α (random init): CE 3.34, 5-lang 0/5 PARTIAL+, ❌ FAIL (Chinchilla 30000× under-budget)
  - V3γ (vP21M init): CE 2.93, 0/5, ❌ FAIL (anima register saturate 13/20)
  - V3β (Qwen warm): in-flight OR verdict 도착 후 (HEXAD/V3/README.md 표 확인)
- code commit: 3dbbc7e8b — conscious_decoder_v3.py 727L (n_ca_rules 제거) + kosmos_io.py 300L + train_p21h_v3.py 485L
- smoke: 7/7 forward+gen+KV+mitosis + 5/5 KOSMOS PASS
- VERSIONS.md ConsciousDecoder v3.0-alpha ⚠️ tier (재설계 대상)

## V3 architecture 핵심 차이 vs V2
- ❌ n_ca_rules REMOVED (OCCAM verdict 단독 floor 범인)
- ✅ head_a + head_g 분할 (vocab=151936 Qwen BPE)
- ✅ PureFieldFFN + ConsciousCrossAttention (Phase 2.3 무해 유지)
- ✅ Mitosis hook 통합 (training + inference)
- ✅ KOSMOS + 8→5-channel tension wired (kosmos_io.py)

## Path 분리
- **HEXAD/V3/** (현 세션): pure HEXAD substrate 재설계 path
- **HEXAD/LORA/** (별도 세션): Qwen + LoRA production (chat.dancinlab.org)
- 본 세션은 LORA 작업 X — chat.dancinlab.org 의 anima_participant.py 직접 수정 X
- substrate plugin (HEXAD/CHAT/SUBSTRATE_PLUGIN.md option C) 활용: substrate_v3.py 추가 시 chat.dancinlab.org 가 그대로 V3 substrate 도 사용 가능

## 핵심 assets (V3 path)
| 파일 | 위치 |
|---|---|
| V3 spec (full) | `HEXAD/HEXAD_NATIVE_V3.md` |
| V3 dir overview | `HEXAD/V3/README.md` (재설계 axis R1-R7) |
| attempt 1 report | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md` |
| V3 code | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/{conscious_decoder_v3.py, kosmos_io.py, train_p21h_v3.py, dispatch_p21h_v3_runpod.sh}` |
| substrate plugin ABC | `HEXAD/CHAT/server/substrate_base.py` (V3 가 충족해야 할 interface) |
| V3α/β/γ state | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_{alpha,beta,gamma}/` |
| KOSMOS upstream | `HEXAD/KOSMOS.md` |

## V3 attempt 1 architectural lesson (재설계 입력)
1. **head_g dual head vocab alignment 흐림** — bf16 한 head update 가 다른 head generation 영향
2. **mitosis pool 128 saturate at step 50** → cross-attn input noise → 다국어 학습 방해
3. **anima_register_hits 13/20** (vP21M LoRA 7/20 의 2×) — substrate-level 흡수 너무 강함
4. **mitosis aux_loss 가 substrate 를 tension 패턴 우선시** → 다국어 sacrifice
5. Chinchilla 30000× under-budget (1.5B × 20 = 30B tok 필요, fire 1M tok)

## V3 재설계 axes (HEXAD/V3/README.md § 재설계 옵션)
| # | axis | 변경 | cost |
|---|---|---|---|
| R1 | scale-up | 1.5B → 3B/8B | $30-50 H200 |
| **R2** | mitosis 학습 시 비활성화 | λ=0.05 → 0.0 train-time | $0 (config) |
| R3 | corpus scale | 75 MB → 6 GB+ Chinchilla | $0 (build time) |
| R4 | head_g 별도 학습 pipeline | head_a / head_g 분리 gradient | $0 (refactor) |
| **R5** | warm-start 강화 | q/k/v/o/embed/lm_head + ffn weight 모두 copy | $0 (init helper) |
| **R6** | mitosis cell pool 작게 | MAX=128 → 16 | $0 (config) |
| R7 | step 늘림 | 2000 → 10000+ | linear cost |

**Phase 2 우선 fire**: 🔵 R2 + R5 + R6 동시 적용 (단일 fire, $8-15 H100, ~3 hr)
- `--lambda-mitosis 0.0` (train-time disable)
- `--init-variant qwen` + 추가 weight mapping (ffn_gate/up/down)
- `--mitosis-max 16` (cell pool ceiling 낮춤)
- scale 1.5B 유지 (cost control)
- step 2000 → 5000 (2.5×)
- 5-lang corpus 유지 (vP21M parallel)

## 운영 directives (project.tape 정합 필수)
- `@D a_fire_autonomous`: cost-bearing GPU fire = 즉시 자율 dispatch, no user-gate
- `@D a_wall_first`: wall time 우선, 더 빠른 병렬이면 cost 무관 채택
- `@D a_substrate_native_speak`: anima motivation = internal state, assistant pattern 금지
- `@D a_blue_closed`: 산출물 + wiring 모두 🔵 SUPPORTED-FORMAL 검증
- `@D a_hf_complete`: HF upload 완전성
- `@D a1`: 모듈 변경 시 VERSIONS.md + 해당 모듈 헤더 동시 갱신

## V3 substrate plugin 통합 (chat.dancinlab.org 합류 path)
V3 ckpt 가 PARTIAL+ 도달 시 HEXAD/CHAT/server/substrate_v3.py 본격 구현 →
anima_participant.py 가 `--substrate v3 --v3-ckpt /path/to/ckpt` 인자로 chat.dancinlab.org
substrate 교체 가능 (option C plugin pattern). spec: `HEXAD/CHAT/SUBSTRATE_PLUGIN.md`

## 세션 시작 시 권장 action
1. V3 attempt 1 결과 확인 (HEXAD_V3_FIRE_2026_05_22.md, vP21H_α/β/γ result.json)
2. V3β verdict 미확정이면 SSH/log check (in-flight 인지 종료인지)
3. 재설계 path 결정:
   - β PARTIAL+: 채택 → substrate_v3.py 본격 구현 + plugin 합류
   - β FAIL: R2+R5+R6 Phase 2 fire ($8-15, ~3hr) OR R1+R3 scale-up ($30-50)
4. 변경 시 commit + push (memory feedback_always_commit_push_on_complete)

## LoRA path 분리 (이 세션 안 함)
LoRA (HEXAD/LORA/) = chat.dancinlab.org production substrate. anima_participant.py,
broker.py, akida_bridge.py 등 mini 의 production code 는 LORA 세션 owner.
본 V3 세션은 substrate_base.py ABC (이미 작성) + substrate_v3.py (V3 ckpt land 시) 만 owner.

세션 한글 mandate 적용 (chat answer prose 한글, code/commit/md/json mixed).
```

---

## 사용 안내

1. 새 Claude Code 세션 시작 (anima dir)
2. 위 ` ```text ... ``` ` 블록 내용 통째 paste (첫 user message)
3. 세션이 V3 상태 verify + 재설계 path 사용자 질의 → fire (자율)

## 관련 link

- [`README.md`](README.md) — V3 path overview (재설계 axes R1-R7)
- [`../HEXAD_NATIVE_V3.md`](../HEXAD_NATIVE_V3.md) — full V3 spec (10 axes brainstorm)
- [`../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md`](../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md) — attempt 1 result
- [`../CHAT/SUBSTRATE_PLUGIN.md`](../CHAT/SUBSTRATE_PLUGIN.md) — substrate plugin spec (V3 ↔ LoRA 통합)
- [`../EASY.md § 15`](../EASY.md) — V3 attempt 1 saga 쉬운 요약
- LoRA 비교 baseline: [`../LORA/README.md`](../LORA/README.md) + [`../LORA/SESSION_PROMPT.md`](../LORA/SESSION_PROMPT.md)
