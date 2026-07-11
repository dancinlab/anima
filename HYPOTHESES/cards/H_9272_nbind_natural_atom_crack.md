# H_9272 — NBIND: 자연 원자(감성 predicate × 부정 형태소) held-out XOR 재조합

## tier
🟡 **DIRECTIONAL** (양성 held-out 신호·GREEN 미cement) — 2026-07-12

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

## cement follow-on (GREEN 경로)
2nd seed(s4302) + control 소표본 해소(n↑ or 다seed) + wild-natural 전이(bar 3) + rho_weave
before/after(baseline .clm FLOOR vs nbind PASS) → L3 배선 = anima 2번째 WIRED-GREEN. GPU 백엔드
(#3323·11.8× byte-identical)로 재eval 저비용화됨.

## 산출
`state/nbind_curriculum/`(gen_nbind.py·FABLE_NBIND_SPEC/GENFIX·AUDIT). 결과 json = summer
`~/nbind_mig/eval_{main,shuffle}_summer.json`. ckpt = mini scratchpad + summer 보존.
[[xbind-g1-crack-measure-not-substrate]]·[[goal-biolens-lane-engine-native-green]]·
[[measurement-metalaw-form-tunable-bind-earned]]. GPU eval = anima-py cupy device path(#3323).
