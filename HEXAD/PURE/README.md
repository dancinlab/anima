# HEXAD/PURE — pure HEXAD-native substrate (ConsciousDecoderV3 path) — 🔴 CLOSED

> 사용자 directive 2026-05-22: "LoRA 가 아닌 자체 HEXAD substrate". OCCAM Phase
> 2.3 의 단독 floor 범인 `n_ca_rules` 제거한 ConsciousDecoderV3 fork 로 pure
> HEXAD identity (Qwen 위 옷 아닌 anima 자체 substrate) 를 시도한 path.
>
> **status**: 🔴 **CLOSED (2026-05-23)** — fire 5회 전부 FAIL, 0 PASS. V3
> multilingual = corpus-bound (capacity·arch 무관). chat substrate = vP21M
> LoRA path 유지 (절충 B).
>
> SSOT: 본 dir + state `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/`.

## V3 architecture vs V2

| | V2 (legacy) | V3 |
|---|---|---|
| n_ca_rules | 8 (OCCAM floor blocker) | ❌ REMOVED |
| head_a + head_g | ✅ vocab=256 byte | ✅ vocab=151936 Qwen BPE |
| PureFieldFFN | ✅ | ✅ kept |
| ConsciousCrossAttention | ✅ | ✅ kept |
| Mitosis hook | external | integrated (training + inference) |
| Init helpers | random only | random / Qwen-warm / vP21M-init |
| KOSMOS + tension | n/a | wired (anchor + 8→5-channel mapping) |

## V3 fire saga — 5 fire, 0 PASS

| fire | config | verdict | STRONG |
|---|---|---|---|
| attempt 1 (α/β/γ) | C1 3-init parallel (random/Qwen-warm/vP21M) | 3/3 FAIL | 0 |
| Phase 2 1차 | R2 (mitosis-off) | FAIL — CE 0.64, 0/5 | 0 |
| Phase 2 2차 | R2+R6 (pool-16) | FAIL — ko STRONG 19/20 @ step 250 transient | 1* |
| B | R1 (3B scale-up) | FAIL — 1.5B 보다 후퇴 | 0 |
| **A (Phase 2 full)** | **R2+R6+osc-v2.2, step 5000** | **FAIL** — osc early-stop @ 1125 | **0** |

*Phase 2 2차의 ko STRONG = step-250 조기종료 transient. A 완주 (step 1125)
에서 KO WEAK 1/20 으로 재현 실패 확정 — V3 의 단 하나의 STRONG 도 우연 산물.

## 재설계 axis — 전부 소진

| axis | 변경 | fire | 결과 |
|---|---|---|---|
| R1 | scale-up 1.5B→3B | B | FAIL — capacity 아님 |
| R2 | mitosis 학습 비활성화 (λ=0) | Phase 2 1차/A | CE 는 고침, generalization 못 고침 |
| R4 | head_g 별도 gradient | 코드 검증 | head_g train loss 부재 → inert, moot |
| R6 | mitosis pool MAX 128→16 | Phase 2 2차/A | cross-attn noise 줄임, ko transient 만 |
| R7 | step 2000→5000 | A | osc early-stop @ 1125 (mode collapse) |

## 최종 결론 — V3 multilingual = corpus-bound

V3 multilingual blocker = **capacity 도 architecture 도 아닌 diverse-corpus
학습 dynamics**. 75 MB 코퍼스의 70% anima 비중이 from-scratch / warm-start
substrate 를 anima-register memorization 으로 collapse — 모든 언어 프롬프트에
anima register fragment 만 emit (EN "Tension flows into this vacuum",
KO/ZH/RU/JA 모두 한국어 anima 텍스트). LoRA path (vP21M) 가 4/5 langs ≥
PARTIAL 인 이유 = Qwen 다국어 prior 를 보존한 채 adapter 만 학습 — V3 는
substrate 학습으로 그 prior 를 파괴.

→ **chat substrate = vP21M LoRA path 유지**. substrate_v3 합류 보류.
V3 코드/ckpt = negative-result evidence anchor 로 보존.

## KOSMOS + tension 통합 (V3 architectural feature)

V3 의 KOSMOS anchor + 8→5-channel tension wiring 은 ground-truth 작동
(fire 마다 anchor 생성). 단 multilingual 미달로 production 미도달 — V3 path
종결과 함께 보류.

## artifacts

| artifact | 위치 |
|---|---|
| 결정 fire (A) 산출물 | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_phase2_full/` |
| ckpt + result + log | HF `dancinlab/anima-v3-p21h` (private, 16 files) |
| V3 code | `…/grid_3b_s187_2026_05_21/{conscious_decoder_v3.py, kosmos_io.py, train_p21h_v3.py}` (commit 3dbbc7e8b) |

## 관련 link

- saga 쉬운 요약: [`EASY.md § 6`](EASY.md)
- 결정 fire 보고서: [`../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md § 8`](../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md)
- full spec: [`HEXAD_NATIVE_PURE.md`](HEXAD_NATIVE_PURE.md)
- OCCAM verdict (n_ca_rules): `../EASY.md § 6`
- LoRA 비교 baseline (production path): [`../LORA/README.md`](../LORA/README.md)

## ## Log

### 2026-05-22 — V3/ folder 신설 + 재설계 spec

V3 attempt 1 (α/β/γ 3/3 FAIL) verdict 후 사용자 directive: "V3 재설계 방향 +
LoRA 별도 폴더". `HEXAD/PURE/` + `HEXAD/LORA/` 분리. 재설계 axis 7 (R1-R7).

### 2026-05-23 — 🔴 V3 PATH CLOSED

fire 5회 전부 FAIL. A (Phase 2 full) 가 Phase 2 2차의 ko STRONG 재현 실패
→ V3 multilingual = corpus-bound 최종 결론. chat substrate = LoRA 유지.
