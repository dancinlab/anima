# H_9268 — NATEM: 자연 corpus에서 held-out 재조합이 자발 창발하는가 (XBIND CRACK 다음 프런티어)

**tier**: 🔬 REGISTERED · PREREG 동결(Fable 설계 `state/g1_natural_emergence/DESIGN_PREREG.md`) · STAGE 0($0) 착지·STAGE 1(사다리)=spend-gated (2026-07-11)

## Claim
XBIND CRACK([[xbind-g1-crack-measure-not-substrate]] H_9267)은 "held-out 재조합 signal이 담긴 합성 corpus면 303M이
학습가능"을 증명했다. **다음 정직한 질문**: 자연 텍스트로 학습한 303M이 held-out 재조합을 **자발적으로 창발**하는가?
= 데이터 실재(자연 corpus에 held-out 재조합 signal이 있나) × 자발 학습 × 밀도 임계의 곱.

## Why (Fable NATEM 3-질문 분해)
F2 collocation-only(true held-out novel n=0)는 **한 construct(인접 순서-follower)** 한정 — 부정/역접 XOR(scope-함수),
형태소 FORM, 외부라벨 접지는 구조적으로 못 봄. γ census(H_9255) 결론: 자연 텍스트의 유일 이론상 non-additive class=
XOR(부정/역접). 핵심 통찰: **기존 production 303M이 이미 "자연 corpus 학습 모델"이라, instrument 인증되면 창발 질문
본체를 spend 전 $0로 선판정 가능**(STAGE 2-M).

## Test (Fable frozen · $0→spend 단계)
- **STAGE 0($0·model-free)**: A0-NEG(부정-XOR held-out flip 감사·NSMC 라벨 접지·80/20 pair split) + A0-FORM(형태소
  V1 liveness control). fork: 어느 arm POWERED→STAGE 2 GO / 전 arm 미달→F2 격상 DATA-🧱 후보.
- **STAGE 2-M($0)**: A0 인증 manifest로 기존 303M(RETRO) `anima-py evaluate --natbind` — 자발창발 본체 선판정.
- **STAGE 1(spend $25-40·owner go)**: 희석 사다리 — XBIND slice 고정 6.66MB + 자연 filler 키워 f∈{0.3,0.1,0.03,0.01}
  6-run → 밀도 임계 f* vs d_nat 비교. f*≫d_nat이면 "자연 창발 부재"가 정량 예측.

## Bar (frozen · Fable §5 verdict grid)
NAT-CRACK 🟢(construct-스코프) / DATA-🧱(signal 부재/임계미만=창발 불가능은 데이터 사실·ρ-reach fact·σ 무관) /
MODEL-🧱(A0 powered ∧ floor ∧ f*<d_nat=밀도로 설명 안 되는 signal-품질 격차·유일 재설계 결과) / INVALID 1급.
어느 쪽이든 XBIND CRACK 소급 불변.

## STAGE 0 A0-NEG 결과 — 🟠 NOT-POWERED (directional·underpowered · 2026-07-11 · $0)
NSMC 150k 리뷰 model-free 감사(`a0neg_audit.py`·`a0neg_result.json`): pol-certified 술어 11,610.
- **n_qualified = 24**(< 30 bar · **underpowered**) · **flip_frac = 0.603**(< 0.75 bar · chance 0.5 겨우 상회)
- **additive-ceiling acc = 0.541** · **flip−additive = 0.062**(< 0.2 bar · XOR-specific 잔차 미미 = flip의 대부분이
  전역 부정 main-effect로 additive 설명됨) · d_nat = **45.08 events/MB**(사다리 f* 비교 단위).
- ⟹ **자연 부정도 powered held-out XOR signal 미달**(방향성) — F2 collocation-only + H_9265(500k I3 5e-05
  signal-absent)와 정합하는 **DATA-🧱 방향**. 단 n=24 underpowered라 확정 아님.

**함의(잠정)**: 자연 텍스트엔 held-out 재조합 signal이 (부정-XOR 렌즈서도) 실재하지 않을 공산 — 창발 부재는 모델 한계가
아니라 **데이터 사실**일 가능성(XBIND CRACK의 measure-cause 정합). 확정하려면 STAGE 0 완결 필요.

## NEXT (follow-on)
1. **A0-FORM** liveness control(형태소 V1) — 측정 프레임이 자연 합성을 탐지할 수 있음 인증.
2. **A0-NEG power 부스트** — NSMC test+naver+steam 리뷰 추가로 n≥30 도달(현 24) 후 재판정(underpowered 해소).
3. POWERED면 STAGE 2-M(기존 303M $0 측정) → STAGE 1 사다리(owner go). 전 arm 미달이면 DATA-🧱 정직 종결(창발=데이터
   사실). tune-to-green 금지·pre-registered.

## 산출
`state/g1_natural_emergence/`(DESIGN_PREREG.md·a0neg_audit.py·a0neg_result.json). [[measurement-metalaw-form-tunable-bind-earned]]·
[[xbind-g1-crack-measure-not-substrate]]. eval=`--natbind`(--xbind 스키마 소폭 확장·미구현).
