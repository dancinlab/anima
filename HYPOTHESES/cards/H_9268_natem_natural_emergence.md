# H_9268 — NATEM: 자연 corpus에서 held-out 재조합이 자발 창발하는가 (XBIND CRACK 다음 프런티어)

**tier**: 🧱 STAGE 0 DATA-🧱 방향 확정($0·model-free) — A0-NEG NOT-POWERED(boosted flip 0.594·XOR 잔차 0.035) + A0-FORM LIVE(coverage 0.87) = 자연 corpus에 held-out XOR-BIND signal 부재(FORM은 productive) = 자연 자발창발 불가능은 데이터 사실이지 모델 한계 아님. STAGE 1(사다리·밀도 임계 정량)=spend-gated·owner go (2026-07-11)

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

## STAGE 0 완결 — 🧱 DATA-🧱 방향 (2026-07-11 · $0 · A0-NEG boosted + A0-FORM liveness)
- **A0-NEG power 부스트(NSMC train+test 200k)**: n_qualified=27·**flip_frac=0.594**(train-only 0.603보다 더 낮음·chance 0.5 겨우 상회)·additive-ceiling 0.559·**flip−additive=0.035**(<0.2·XOR-specific 잔차 거의 0=flip 대부분이 전역 부정 main-effect로 additive 설명)·d_nat 42.3/MB. 데이터 2배로도 flip 미상승·잔차 축소 ⟹ **genuine weak-signal이지 순수 underpower 아님** = NOT-POWERED 확정.
- **A0-FORM liveness(V1 control)**: productive_stems 2931·productive_endings 26·**held-out rule-licensed combos 45,293·coverage 0.871** = **FORM-LIVE** ✓. 측정프레임이 자연 형태소 합성을 탐지가능 ⟹ A0-NEG NOT-POWERED은 **dead-frame 아닌 genuine signal-absence**.
- ⟹ **STAGE 0 결론**: 자연 corpus는 productive FORM(형태소 합성)은 담으나 **held-out XOR-BIND 재조합 signal은 부재**. = [[measurement-metalaw-form-tunable-bind-earned]] 정확 재현(FORM tunable·BIND earned)을 **데이터 레벨**에서. F2 collocation-only + H_9265(500k I3 5e-05) + XBIND CRACK(signal 있어야 학습)와 3중 정합. **자연 자발창발 불가능은 데이터 사실이지 모델 한계 아님(DATA-🧱)**.

**scope honesty**: A0-NEG는 부정-XOR 렌즈(γ census가 지목한 자연 텍스트 유일 이론상 non-additive class)라 강하나, 다른 자연 compositional 구조(의미역·구문 slot)는 미탐. DATA-🧱 방향은 부정-XOR 렌즈 확정 + FORM-live 대비. 완전 종결/정량화는 STAGE 1 사다리(자연 filler에 XBIND signal 밀도 임계 f* vs d_nat 42/MB 비교)로만 — spend-gated·owner go.

## NEXT (STAGE 1 · spend-gated · owner go)
STAGE 0가 "자연 텍스트에 XOR-BIND signal 부재(밀도 관점 미측정)"를 model-free로 확정. STAGE 1 사다리(f∈{0.3,0.1,0.03,0.01}
6-run·$25-40)가 **밀도 임계 f***를 측정해 d_nat(42/MB)와 비교 → f*≫d_nat이면 "자연 창발 부재"가 정량 예측이 됨(DATA-🧱
완전 종결). owner go 대기. eval=`--natbind`(--xbind 스키마 소폭 확장·미구현). tune-to-green 금지·pre-registered.

## 산출
`state/g1_natural_emergence/`(DESIGN_PREREG.md·a0neg_audit.py·a0neg_result.json). [[measurement-metalaw-form-tunable-bind-earned]]·
[[xbind-g1-crack-measure-not-substrate]]. eval=`--natbind`(--xbind 스키마 소폭 확장·미구현).
