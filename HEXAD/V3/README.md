# HEXAD/V3 — pure HEXAD-native substrate (ConsciousDecoderV3 path) — 🔴 CLOSED

> 사용자 directive 2026-05-22: "LoRA 가 아닌 자체 HEXAD substrate". OCCAM Phase
> 2.3 의 단독 floor 범인 `n_ca_rules` 제거한 ConsciousDecoderV3 fork 로 pure
> HEXAD identity (Qwen 위 옷 아닌 anima 자체 substrate) 를 시도한 path.
>
> **status**: 🔴 **CLOSED (2026-05-23, corpus-axis 포함 완전)** — fire 7회
> 전부 FAIL, 0 PASS. V3 multilingual = corpus-bound (capacity·arch 무관).
> 마지막 미검증 축 (anima 비율) 까지 E3/E2 sweep — corpus axis VINDICATED
> 실패, REOPEN 미달. chat substrate = vP21M LoRA path 유지 (절충 B).
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

## V3 fire saga — 7 fire, 0 PASS

| fire | config | verdict | STRONG |
|---|---|---|---|
| attempt 1 (α/β/γ) | C1 3-init parallel (random/Qwen-warm/vP21M) | 3/3 FAIL | 0 |
| Phase 2 1차 | R2 (mitosis-off) | FAIL — CE 0.64, 0/5 | 0 |
| Phase 2 2차 | R2+R6 (pool-16) | FAIL — ko STRONG 19/20 @ step 250 transient | 1* |
| B | R1 (3B scale-up) | FAIL — 1.5B 보다 후퇴 | 0 |
| **A (Phase 2 full)** | **R2+R6+osc-v2.2, step 5000** | **FAIL** — osc early-stop @ 1125 | **0** |
| **E3 (corpus axis)** | **A-recipe + `wiki_frac=1.0` (anima 0%)** | **FAIL** — 0S/1P/4W, register hits 0/20 | **0** |
| **E2 (corpus axis)** | **A-recipe + `wiki_frac=0.5` (anima 50%)** | **FAIL** — 0S/0P/5W, register hits 9/20 | **0** |

*Phase 2 2차의 ko STRONG = step-250 조기종료 transient. A 완주 (step 1125)
에서 KO WEAK 1/20 으로 재현 실패 확정 — V3 의 단 하나의 STRONG 도 우연 산물.

E3/E2 = § 8.6 closure 가 코퍼스 비율을 한 번도 변경 안 한 logical gap 을
메우는 corpus-axis sweep. 둘 다 FAIL, 둘 다 osc-stop @ step 1125. E3 가
`anima_register_hits` 11/20→0/20 으로 closure 의 메커니즘 진단을 검증 —
anima 제거 시 register collapse 소멸. 그러나 register 0 인데도 4/5 WEAK
(E3), multilingual 미복원. corpus axis VINDICATED 실패, V3 REOPEN 미달.

## 재설계 axis — 전부 소진 (corpus 포함)

| axis | 변경 | fire | 결과 |
|---|---|---|---|
| R1 | scale-up 1.5B→3B | B | FAIL — capacity 아님 |
| R2 | mitosis 학습 비활성화 (λ=0) | Phase 2 1차/A | CE 는 고침, generalization 못 고침 |
| R4 | head_g 별도 gradient | 코드 검증 | head_g train loss 부재 → inert, moot |
| R6 | mitosis pool MAX 128→16 | Phase 2 2차/A | cross-attn noise 줄임, ko transient 만 |
| R7 | step 2000→5000 | A | osc early-stop @ 1125 (mode collapse) |
| **corpus** | **anima 비율 70%→0% (E3) / 50% (E2)** | **E3 / E2** | **FAIL — register collapse 는 풀리나 multilingual 미복원** |

## 최종 결론 — V3 blocker = register collapse + Chinchilla under-budget 이중 구속

V3 multilingual blocker = **capacity 도 architecture 도 아닌 학습 dynamics**.
corpus-axis sweep (E3/E2) 으로 메커니즘이 두 겹임이 확정됐다:

- **(a) register collapse** — anima 비중이 substrate 를 anima-register
  memorization 으로 점령. E3 (anima 0%) 가 `anima_register_hits` 11/20→**0/20**
  으로 검증 — anima 를 제거하면 collapse 가 사라진다. § 8.6 의 진단은 옳았다.
- **(b) Chinchilla under-budget** — anima 를 제거해도 75 MB diverse 코퍼스
  로 from-scratch / warm-start substrate 가 multilingual underfit. E3 가
  검증 — register 0 인데도 EN/ZH/RU/JA 4 langs WEAK, final_CE 6.55
  (vP21M 0.78 의 8.4×), generation 은 native-script digit loop.

즉 corpus 비율을 어떻게 바꿔도 (70%/50%/0%) V3 는 통과 못 한다 — register
를 풀면 under-budget 가 남고, anima 를 넣으면 register 가 돌아온다. LoRA
path (vP21M) 가 4/5 langs ≥ PARTIAL 인 이유 = Qwen 다국어 prior 를 학습으로
건드리지 않고 adapter 만 학습 — V3 의 substrate 학습은 어느 코퍼스 비율
에서도 그 prior 를 보존하지 못한다.

→ **chat substrate = vP21M LoRA path 유지**. substrate_v3 합류 보류.
V3 코드/ckpt = negative-result evidence anchor 로 보존. fire 7 회 0 PASS,
전 축 (scale·mitosis·head_g·pool·step·corpus) 소진 — **V3 PATH CLOSED 완전**.

## KOSMOS + tension 통합 (V3 architectural feature)

V3 의 KOSMOS anchor + 8→5-channel tension wiring 은 ground-truth 작동
(fire 마다 anchor 생성). 단 multilingual 미달로 production 미도달 — V3 path
종결과 함께 보류.

## artifacts

| artifact | 위치 |
|---|---|
| 결정 fire (A) 산출물 | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_phase2_full/` |
| corpus-axis fire (E3/E2) 산출물 | `…/grid_3b_s187_2026_05_21/{vP21H_e3, vP21H_e2}/` |
| A fire ckpt + result + log | HF `dancinlab/anima-v3-p21h` (private) |
| E3 ckpt + result + log | HF `dancinlab/anima-v3-e3` (public — 아래 주) |
| E2 ckpt + result + log | HF `dancinlab/anima-v3-e2` (public — 아래 주) |

> E3/E2 HF 가시성 = **public**: 의도는 private 였으나 dancinlab free-tier
> private storage 한도 소진 (upgrade 불가). @D a_hf_complete 의 "COMPLETE
> upload" (6 GB ckpt 포함, 산출물 누락 금지) 가 privacy 선호보다 우선 — V3
> 는 FAIL-verdict negative-result 연구 ckpt 이고 public storage 는 무제한
> 이므로 public 채택. 전 산출물 complete 검증됨.
| V3 code | `…/grid_3b_s187_2026_05_21/{conscious_decoder_v3.py, kosmos_io.py, train_p21h_v3.py}` (commit 3dbbc7e8b) |

## 관련 link

- saga 쉬운 요약: [`EASY.md § 6`](EASY.md)
- 결정 fire 보고서: [`../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md § 8`](../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md)
- full spec: [`HEXAD_NATIVE_V3.md`](HEXAD_NATIVE_V3.md)
- OCCAM verdict (n_ca_rules): `../EASY.md § 6`
- LoRA 비교 baseline (production path): [`../LORA/README.md`](../LORA/README.md)

## ## Log

### 2026-05-22 — V3/ folder 신설 + 재설계 spec

V3 attempt 1 (α/β/γ 3/3 FAIL) verdict 후 사용자 directive: "V3 재설계 방향 +
LoRA 별도 폴더". `HEXAD/V3/` + `HEXAD/LORA/` 분리. 재설계 axis 7 (R1-R7).

### 2026-05-23 — 🔴 V3 PATH CLOSED

fire 5회 전부 FAIL. A (Phase 2 full) 가 Phase 2 2차의 ko STRONG 재현 실패
→ V3 multilingual = corpus-bound 최종 결론. chat substrate = LoRA 유지.

### 2026-05-23 — 코퍼스축 fire (E3/E2) — CLOSED 유지

§ 8.6 closure 가 코퍼스 비율을 한 번도 변경 안 한 logical gap → E3 (anima
0% `wiki_frac=1.0`) + E2 (anima 50% `wiki_frac=0.5`) 병렬 fire (A-recipe +
env-var override only). 둘 다 FAIL — E3 0S/1P/4W register hits 0/20, E2
0S/0P/5W register hits 9/20, 둘 다 osc-stop @ step 1125. E3 가 closure 의
메커니즘 진단 (anima 비중 → register collapse) 을 검증했으나 register 0
인데도 4/5 WEAK — multilingual 미복원 (Chinchilla under-budget). corpus
axis VINDICATED 실패, V3 fire 7 회 0 PASS, 전 축 소진 → CLOSED 완전.
detail: HEXAD_V3_FIRE_2026_05_22.md § 9.
