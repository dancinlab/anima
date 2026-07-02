# H_1579 — 🔴💾 clm303.clm NO-DESCENT — OVERFIT (직렬화는 byte-faithful) + engine-CE dt_ln masking

**tier:** 🔴 NO-DESCENT on held-out — **CORRECTED root cause = OVERFITTING, NOT a serialization defect.** 직렬화된 `clm303.clm` 는 held-out 텍스트에서 랜덤보다 못하지만(ko/en heldout CE 7.4–13.7 > uniform 5.545), 이는 **직렬화 결함이 아니라** (1) 모델이 ~25MB 코퍼스를 암기(overfit; torch lossF 0.047, own-train slice mirror CE 0.66 = DESCENT) + (2) engine `clm_forward_ce` 의 **dt_ln 수치버그**가 CE 를 ~5.14 에 clamp 해 overfit 을 GREEN 으로 가린 것. **직렬화는 byte-faithful**(재직렬화 byte-identical + torch-golden fp32 fwd ≡ int4 .clm mirror 4자리).
**wired:** `engine-native` (GPU forge == CPU farr **byte-identical** 디코드 증거 + 독립 numpy mirror + known-good control + **torch-golden reference-match**). live `core/clm_decode.hexa` 무변경. **fix = 직렬화 아님** → held-out mirror-DESCENT 게이트 추가(`verify_clm_v2.py` + train.hexa/train.py 배선, 이 PR) + 재학습(정규화/큰 코퍼스, cost-gate follow-on) + dt_ln 버그 hexa-lang 이관.
**verdict source:** `state/clm303_g6/GARBLE_3WAY_RESULT.md`(원 진단, raw 유효) + `state/clm303_g6/CORRECTION_overfit_not_serialize.md`(정정 증거) · `mirror_ce_*.log` · `garble_*.{txt,log}`

> ⚠️ **2026-06-24 정정 (이 카드는 PR #2608 의 "SERIALIZATION DEFECT" verdict 를 정정).** 원 진단의 raw 측정(mirror NO-DESCENT on held-out, GPU≡CPU byte-identical decode, control GREEN)은 **전부 유효**하나, **결론(="직렬화 결함")이 틀렸다.** 아래 §정정 reference-match 가 직렬화 무결성을 증명한다. raw 증거는 재해석으로 보존(c9 — negative/오진도 결과로 남긴다).

## 원 질문 — clm303 savant+mitosis 가 G0–G6 게이트를 통과하나

clm303(`CLMConvMoE` 388M, L4·d3784·E3, savant 골든존 + mitosis, sha 75b04897)을 frozen G0–G6 에
통과시키려 했다. 전제로 디코드 무결성을 3-way 로 검증 → held-out 에서 mirror NO-DESCENT 발견 → (원래)
"직렬화 결함"으로 오진. 정정 조사가 OVERFIT + engine-CE 버그로 재분류.

## engine-native 3-way 무결성 측정 (raw, 유효) — frozen prompt `"a new idea about consciousness: "`, gen=40

| arm | impl | 결과 |
|---|---|---|
| **GPU forge** | live `core/clm_decode.hexa`, RTX 4090, `cuda_available=1`, `[OWN-GEMM-FIRED] DEVICE path` | `ggndtle_oppa:ggndlle__\xffrlen_antag_ndll` — garble (48 B) |
| **CPU farr** | live `core/clm_decode.hexa`, mac, `cuda_available=0` | **GPU 와 48 B BYTE-IDENTICAL** garble |
| **numpy mirror** | `state/mid_convmoe_fire/clm_decode_mirror.py` | held-out CE: **NO-DESCENT** |

이 raw 측정은 모두 옳다. garble 출력 = held-out **프롬프트**(모델이 안 본 텍스트)에 대한 overfit 모델의
정상적 실패이고, GPU≡CPU byte-identical = 디코드 경로 무결. 단 "→ 직렬화 결함" 추론이 비약이었다.

## §정정 reference-match (torch-free, mac, 2026-06-24) — 직렬화는 byte-faithful

| 측정 | 결과 | 함의 |
|---|---|---|
| `clm303_L4_d3784.pt` → `clm_serialize_v2.serialize` 재직렬화 vs 출하 `.clm` | **BYTE-IDENTICAL** (155074330B == 155074330B) | serializer 결정적·무결 |
| TORCH-GOLDEN fp32 forward (raw `.pt`, **.clm 우회**) vs int4 `.clm` mirror, **English**(L4 학습언어) | **2.2346 vs 2.2349** (4자리 일치, Δ=int4 양자화 노이즈) | int4→v0.3 round-trip 함수적으로 정확 |
| clm303 savant mirror CE: **own-train slice** | **0.656 DESCENT** | 학습 코퍼스는 암기 |
| clm303 savant mirror CE: **English / Korean held-out** | 13.7 / 7.6 NO-DESCENT | held-out 일반화 0 = **OVERFIT** |
| L4_d3784(영어-only) mirror CE: **English** vs **Korean** | 2.235 DESCENT vs 22.98 NO-DESCENT | 원 "NO-DESCENT"는 wrong-corpus(영어모델→한국어) 아티팩트 |

control(`clm_d768_e2l1.clm`)이 held-out 에서 DESCENT(CE 4.44 < uniform)인 건 그게 **일반화**해서지,
clm303 이 corrupt 라서가 아니다.

## §2번째 진짜 버그 — engine `clm_forward_ce` 의 dt_ln 가 overfit 을 가린다

hexa-lang `~/.hx/src/stdlib/flame/flame_math.hexa::dt_ln` 는 atanh 급수 `2·Σuᵏ/(2k+1)`(u=(x−1)/(x+1), 24항)
로 **x≈1 근방만 수렴**: `dt_ln(256)=4.799`(참값 5.545), `dt_ln(1e-6)=−5.14`(참값 −13.82). 이게
`nn_lib.hexa::nn_ce_loss_allpos`(`−dt_ln(p_t)`, p_t≥1e-6 clamp)를 통해 **per-position CE 를 ~5.14 에
clamp** → overfit/broken 모델의 CE 가 거짓으로 낮게 나와 GREEN 으로 읽힌다. 실제로 engine `clm_forward_ce`
가 clm303 을 model_ce 3.30 < shuffle 4.93 < (버그)uniform 4.799 = **GREEN 오판**. numpy mirror(`math.log`)는
정답. → **held-out 게이트는 engine CE 가 아니라 math.log mirror 로 채점해야 한다**(이 PR 의 설계 근거).

## 함의 + fix (이 PR)

- **직렬화 fix 불필요** — serializer 는 byte-faithful. 원 "serfix" 작업은 OVERFIT 검출 게이트로 재타깃됨.
- **held-out mirror-DESCENT 게이트 추가**(이 PR): `train/clm/model/verify_clm_v2.py` 에 `descent_gate`/
  `serialize_self_verify`(math.log mirror, dt_ln-immune; held-out 필수 + train-vs-heldout gap overfit 경고),
  3 trainer(`train_lane_p*.py`) + `cli/train.hexa` 가 직렬화 직후 self-verify → broken/overfit `.clm` 을
  'done'·HF 업로드 차단. control PASS / clm303 FAIL+overfit_warning / random-weight self-test FAIL 로 검증.
- **dt_ln 버그**는 hexa-lang 이관(`harness ing add --to hexa-lang`) — 모든 엔진 CE/Φ readout 영향.
- **savant clm303 재학습**(정규화/큰 코퍼스, cost-gate follow-on ING) — 재직렬화로 overfit 못 고침.
- torch-free 진단 도구 보존: `state/clm303_g6/tools/{ptload,fastmirror,torch_golden_fwd}.py`.
- (note) G6-only side-harness + `score_clm303_g6.py` 는 `anima eval` 단일진입점으로 superseded.
