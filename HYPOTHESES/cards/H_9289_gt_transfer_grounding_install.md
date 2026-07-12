# H_9289 — GT-TRANSFER: held-out 극성 자연-접지 install (NBIND-G 벽 reopen)

## tier
🟡 STEP-0 착지 = INFO-ABSENT (2026-07-13 · $0 G-PROBE measured) → MAIN=C3+C4 hybrid corpus (spend-gate) —
NBIND-G N2 GROUNDING-WALL exit 설계(Fable). **STEP-0 G-PROBE(frozen N2 ckpt·summer $0·3 ckpt×1176 문맥
dump-hidden→L2-logreg)**: held-out P_nat 극성 probe-acc = main_s7 **0.5517**·main_s11 **0.5517**·base_only 0.5172
(shuffle_ref 0.5138·Δ vs shuffle 0.04~0.05). 양 seed ≈ chance·0.65 bar 크게 미달·main이 base_only 거의 못 넘음
→ **held-out 극성이 표현에 선형-부재**(내 '부호 미앵커' 가설보다 정보-부재에 가까움) → frozen 분기 **INFO-ABSENT
→ MAIN=C2 아닌 C3+C4 hybrid corpus**(극성을 CE-load-bearing으로 만드는 코퍼스 구성). MAIN=spend-gated(owner go).
poscontrol cos 0.75~0.79(distinct·표현 붕괴 아님·verdict-integrity 통과). caveat=small-n probe(20/29 atom·triage).

## 가설
NBIND-G N2([[nbindg-grounding-frame-general-data-blocked]])는 "자연 분포적 사용만으로는 held-out 감성원자
극성이 install 안 됨"을 보였다(flip0 양 seed chance **미만** 0.402/0.368<shuffle 0.448). **핵심 단서**: flip0가
0.5 수렴(신호부재)이 아니라 chance **미만**(체계적 역상관) → 극성 축은 표현공간에 있으나 **원자별 부호(sign)가
앵커링 안 된** 상태일 수 있다. 이 "정보 부재" vs "정보 있으나 부호 미고정" 분기를 $0로 판별한 뒤, 접지-과업을
**데이터로**(loss항 아님) 삽입해 판독 스킬을 supervise하면 그 스킬이 분포적 feature 경유로 held-out 원자에
전이되는가? = 자연-접지 install 가능성.

## STEP-0 (frozen gate · $0 · 기존 N2 ckpt · 발사 전 필수)
**G-PROBE triage** — N2 ckpt(natem_n2_main_s7/s11) frozen, held-out 원자의 자연문맥 k개 mean-pool 표현에
선형 probe(train-원자 라벨 학습 → held-out 전이) + 원자별 acc 히스토그램(쌍봉=부호반전 vs 균일=부재).
- 통제 2: shuffle-label probe(용량 baseline)·base_only ckpt probe(학습내용 baseline).
- **분기(사전등록)**: held-out probe-acc **≥0.65 양 seed** ∧ base_only ≤ shuffle+0.05 → **INFO-PRESENT** →
  MAIN=C2(GT-curriculum). 미달 → **INFO-ABSENT** → MAIN을 C3+C4 hybrid 코퍼스 arm으로 교체(동일 게이트·DV).
- 부수: detector 4-cell Korean-aware 대칭(N2 전-arm chance-미만 해명·V3).
- $0 (pool·수시간).

## STEP-0 결과 = INFO-ABSENT (measured · 2026-07-13 · summer $0 · gt_step0_gprobe.py)
3 ckpt × 1176 자연문맥 dump-hidden(d=3784 penultimate·`--win 24`) → 원자별 mean-pool(`__last`) → L2-logreg
(train=P_grid 20원자 극성 → test=held-out P_nat 29원자):

| ckpt | held-out probe-acc | shuffle-label | Δ vs shuffle |
|---|---|---|---|
| **main_s7** | **0.5517** | 0.5138 | +0.038 |
| **main_s11** | **0.5517** | 0.4983 | +0.053 |
| base_only | 0.5172 | 0.4828 | +0.035 |

**판정(frozen 분기)**: 양 main ≈ chance(0.55)·**0.65 bar 크게 미달**·main이 base_only(0.517) 거의 못 넘음·Δ vs
shuffle 무시가능(0.04~0.05) → **held-out P_nat 극성이 frozen N2 표현에서 선형-판독 불가 = INFO-ABSENT**. 내가
세운 flip0-역상관 "부호 미앵커" 가설보다 **정보-부재**에 가까움(N2 학습이 held-out 극성 decodability를 base 위에
거의 안 얹음 = corpus×CE가 극성을 load-bearing으로 안 만듦·GROUNDING-WALL 진단과 수렴). poscontrol cos
0.75~0.79(distinct·표현 붕괴 아님·verdict-integrity 통과). **caveat**: small-n probe(20 train/29 heldout·d=3784·heavy
L2)=triage이지 비선형/대형 probe면 다를 여지(단 통제로 보정·frozen 분기는 보수적 C3+C4로 귀결). ⟹ **MAIN=C2 폐기,
C3+C4 hybrid corpus 채택**(spend-gated).

## MAIN pre-register (C3+C4 hybrid corpus · spend-gated · STEP-0 INFO-ABSENT 확정)
303M 신규학습 N2 동일 스케일(T≈105k·bf16·`ce_marginal`):
| arm | corpus | isolates |
|---|---|---|
| main-GT ×2 seed(7·11) | 자연 + **train-원자 극성판독 episode(순수 CE)** + grid XOR · held-out은 자연문맥만 | 판독 스킬 전이 |
| ctrl-shufGT ×1 | 동일 episode·coin-flip 라벨 | 포맷/에너지 통제(접지신호 파괴) |
| ctrl-N2rep ×1 | episode 없음 | N2 재현 앵커 |

**frozen validity**: V1 설치(SEEN P_grid≥0.85 ∧ GT-과업 train-원자 acc≥0.85·미달=INVALID) · V2 누출(held-out
원자 극성라벨 ±W byte 공기 0회) · V3 detector 4-cell+chance-비대칭 · V4 n-gram 중복 · V5 2seed 동방향. 음성=TOST
Δ_eq=0.10·N_REQ 발사 전 고정.

## frozen verdict (Fable §2 · 값 아닌 Δ · 장부-DV 금지)
- **headline GATE-1** = held-out **flip0 acc**, 원자별 paired Δ = main-GT − ctrl-shufGT. **bar Δ≥+0.15 양 seed ∧
  main-GT 절대치>0.55** (처치는 train-원자 매핑 최적화·DV는 held-out 전이 = 항등식 불성립).
- **GATE-2**(GATE-1 통과 시만) = held-out XOR D-acc, 동일 Δ 구조·bar Δ≥+0.15.
- **falsifier**: V1 통과(설치 확인)에도 flip0 Δ≤+0.05 양 seed(TOST 등가) → "판독 스킬 원자간 전이 안 됨" =
  접근경로 깔아줘도 분포 feature가 접지에 불충분 = C2 반증.

## 정직 경계 (성급한 substrate 천장 금지)
- INFO-ABSENT + C3/C4 floor → 여전히 **data 채널**(자연텍스트 원자당 극성신호가 이 규모서 부재·합성 XBIND
  1.000이 substrate 무죄 상수). GATE-1 통과+GATE-2 floor → 벽이 grounding→composition-consumption 재국소화.
- INFO-PRESENT + GATE-1 실패 = 첫 substrate-쪽 증거이나 **렌즈 1개** — a_break_the_wall대로 ≥2 통제 렌즈(probe-경유
  vs task-경유) 정합 후에만 "303M byte-LM CE" **범위한정** 천장 후보. 성급한 TERMINAL 금지.

## 비용
STEP-0 = **$0**(pool·기존 ckpt). MAIN = 303M×105k×4run = N2 실비 동급 → **GPU rent spend-go**(STEP-0 이후 결정).

## 산출
`state/nbindg_grounding/FABLE_GT_TRANSFER_DESIGN.md`(Fable 원문) · STEP-0 probe 스크립트/결과(follow-on).
[[nbindg-grounding-frame-general-data-blocked]]·[[xbind-g1-crack-measure-not-substrate]]·H_9286.
