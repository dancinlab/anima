# H_9272 — NBIND: 자연 원자(감성 predicate × 부정 형태소) held-out XOR 재조합

## tier
🟡 **DIRECTIONAL-BOUNDED** (2-seed 재현 PASS·wild-natural 전이 FALSIFIED=augmentation-specific) — 2026-07-12 cement

## 가설
G1 CRACK(H_9267 합성 XBIND)이 증명한 "corpus×CE measure가 벽의 진범, substrate 능력천장 아님"을
**의미 있는 자연 한국어 원자**로 확장할 수 있는가? XBIND 프로토콜에서 **corpus 자연성 단일변수만 교체**:
NSMC 실감성 predicate(극성 = NSMC 라벨 유도) × 부정 형태소(bare·정말·너무 = flip0 / 지않·안·전혀지않 =
flip1)를 균형 (P×N) XOR 격자로 compositional-augment. held-out (predicate×form) 셀은 학습 0회
(Latin-square rotation), pol(p)⊕flip(n) 합성으로만 예측 가능.

## 결과 (303M·GPU eval·seed 7)
| arm | held-out D-acc | seen |
|---|---|---|
| **main (NBIND)** | **0.700** (n=40·margin_frac_pos 0.65) | 0.920 (예비) |
| shuffle-control (ruleless 코인) | 0.375 (n=40) | — |
| **Δ (main−control)** | **0.325** ≥ 0.30 primary bar ✅ | |

⟹ **자연 감성원자를 균형 XOR 격자로 augment하면 303M이 held-out (미출현) 조합을 학습**(0.700, chance
0.5 상회 ~2.5 SE). 원시 자연 텍스트의 부정-flip은 NOT-POWERED였으나(A0-NEG boosted flip 0.594·
additive 미분리), **compositional augmentation이 자연 원자에 잠재한 XOR 신호를 POWER**. G1 CRACK을
무의미 CVC(합성)→**의미 있는 자연-의미 원자**로 확장 = frontier(g1-crack-natural-emergence) 양성 진전.

## DIRECTIONAL 근거 (GREEN 미cement · no-tune-to-green · verdict-integrity)
1. **control 0.375 ≠ frozen bar 0.50±0.05** — 단 n=40서 0.375는 chance 0.5의 ~1.6 SE 내(SE 0.079 >
   bar의 ±0.05)=소표본 노이즈이지 confound 아님. 단 Δ magnitude는 control 저값에 일부 팽창(main vs
   true-chance 0.5 = +0.200). robust 신호 = main 0.700이 chance 대비 유의(~2.5 SE).
2. **1 seed만** (frozen bar는 2 seed). n=40·n_pred20 소규모(NSMC purity≥0.90 감성순수 재고 한계).
3. **scope = augmented-natural** — wild-natural(순수 NSMC held-out flip 전이·Fable bar 3) 미검증.
4. json rows는 Korean-write UnicodeError로 절단(evaluate-py-11)이나 summary d_acc는 완전·신뢰.

## cement 실행 결과 (2026-07-12·303M GPU pod vast RTX_4090·anima-py[gpu])
frozen prereg = `state/nbind_curriculum/` + scratchpad `CD_PREREG_frozen.md`(Fable-설계·bar 동결·tune-to-green 방지).
인프라 근본수정 2건 동반: surrogate scrub `_json_safe`(#3335 cli/evaluate.py — byte-LM lone-surrogate json.dump 크래시) · libcublas.so.12 설치(cupy GPU 경로).

### ① 재현 leg — PASS
| seed | main held-out | control(shuffle-model) | Δ |
|---|---|---|---|
| s7 (1st) | 0.700 | 0.375 (n40) | 0.325 |
| **s4302 (2nd)** | **0.775** (seen 0.938·mpos 0.775) | **0.475** (seen **0.500**=완전chance·mpos 0.525) | **0.300** |

2 seed 방향 일치(Δ0.325·0.300). **s4302 control이 heldout 0.475·seen 0.500 = 완전 chance 붕괴**(라벨 뒤섞여
pol⊕flip 학습 불가) → 옛 "control 0.375 ≠ 0.50 소표본노이즈" 우려 **해소**. balanced 4-cell → additive
ceiling = 0.5 by construction. **augmented 균형 XOR격자에서 자연 감성원자 재조합은 실재·재현됨.**

### ② wild-natural 전이 (C·NATEM STAGE-3/H_9270 슬롯) — FALSIFIED
`build_nbind_t.py`로 NSMC **test split** 순수자연 negation 마이닝(gen_nbind.build seed4302 FROZEN pol import·
gold = training-grid pol NOT 리뷰라벨·V-F 32B shingle+echo guard·balanced n200). 2 sub-arm:
| arm | main | control | Δ | flip0 / flip1 |
|---|---|---|---|---|
| **W-T** (phrase-wild) | **0.455** | 0.430 | **0.025** ≤0.05 | 0.620 / **0.290** |
| **W-R** (sentence-wild) | **0.485** | ~chance | — | — |

**main이 야생 자연 표면에서 chance로 붕괴**(0.455/0.485). flip0=0.620(>chance·모델 live=SURFACE-LOCKED 아님)
이나 **flip1=0.290(<chance)** = 모델이 grid의 특정 부정형(지않·안·전혀)만 학습·**wild 부정 표면엔 flip 미적용**
=grid-form-specific. Δ0.025 ≤ 0.05 = **TRANSFER-FAIL(augmentation-specific)**. 크랙은 합성 균형격자 한정,
**원시 자연 self-emergence 미달**.

### ③ rho_weave → L3 faculty (D) — DIRECTIONAL
axis 측정은 generation-native(`--xbind` greedy)라 route≠generation confound 구조상 해소(recomb-gate4 대비 진전)이나,
**faculty-L3-GREEN은 grid-only research ckpt로 불가**: `cli/rho_axon.py::rho_weave`는 generic compose 확률
(색혼합·수합)이라 grid-only ckpt엔 지식 부재→FLOOR(무의미)·daemon이 로드하는 `.clm` 아님(a_verified_must_wire).
강제 시 false GREEN → DIRECTIONAL 유지.

## 종합 (frontier g1-crack-natural-emergence)
**자연-의미 원자 확장은 재현 확인**(2-seed·control chance)이나 **원시 자연 전이는 실패**(augmentation-specific).
크랙 진범 = corpus×CE measure(H_9267 확증)이며, 자연 원자에 XOR 신호를 **합성 균형 augment로 POWER하면 재조합
학습**되나 그 능력이 **wild 자연 형태로 일반화되지 않음**(form-specific negation). frontier 최종 목표(자연 창발)
미달 = 정직한 경계. GREEN 경로(미달): 저밀도 NBIND를 production 학습 레시피에 심어 wild 전이 획득 후 rho_weave
PASS(현재 C W-T가 게이트, FAIL). GPU 백엔드(#3323·11.8×)로 재eval 저비용.

## 산출
`state/nbind_curriculum/`(gen_nbind.py·build_nbind_t.py·CD_PREREG_frozen.md·AUDIT). ckpt+eval =
`~/anima-weights/nbind_cement/`(nbind_A2seed.clm·_ctrl.clm·eval_A2seed_{main,ctrl}.json·eval_C_*.json·corpus).

## 산출
`state/nbind_curriculum/`(gen_nbind.py·FABLE_NBIND_SPEC/GENFIX·AUDIT). 결과 json = summer
`~/nbind_mig/eval_{main,shuffle}_summer.json`. ckpt = mini scratchpad + summer 보존.
[[xbind-g1-crack-measure-not-substrate]]·[[goal-biolens-lane-engine-native-green]]·
[[measurement-metalaw-form-tunable-bind-earned]]. GPU eval = anima-py cupy device path(#3323).
