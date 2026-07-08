# Premise-swap verifier toy — INCONCLUSIVE (아키텍처-blocked), NOT a verifier KILL

## 정직한 판정: 🟡 INCONCLUSIVE (verdict-integrity)
Fable GO-TOY 설계(ARM7 budgeted-verifier + ARM8 controls + firewall) 구현·실행. frozen bars는
FAIL이나 **verifier KILL로 읽으면 안 됨** — toy의 base MLP가 target 구조를 일반화 못해 시험 자체가
불성립(control이 divergence 신호):
- **결정적 tell**: `8b_corpusnull`(진짜 true-cell 30개 직접 편입)조차 eval-only reach=0.00.
- **학습성 진단**: 90% 커버리지 + 3000 epoch(train=1.00 완전암기)에서도 held-out=0.000. MLP는
  모듈러 군 법칙 b=(a+g)%K를 **어떤 예산으로도 일반화 못함**(memorize 100%·generalize 0%,
  grokking-hard: 독립 embedding MLP는 이 task를 안 grok). → 어떤 학습신호(verifier 포함)도 lift 불가.

## verifier 자체는 작동함 (escape 논증 무손상)
ARM7 verifier 탐색이 라운드당 예산 내 k-샘플+음성재샘플로 **37 queryable cell을 정확히 solved**
(0.06 filter-only 상한 대비 탐색이 실제로 정답 발견). Fable 정보이론 escape(verifier=corpus-외
truth 채널, I(·;truth) 주입 → DPI 탈출)는 **유효**. 단 toy가 그 lift를 못 보인 건 base가 truth
라벨을 memorize만 하고 compose 안 해서.

## 깊은 정련 (toy가 드러낸 것)
**verifier truth-주입은 필요조건이지 충분조건 아님** — corpus-외 truth를 줘도, base가 구조를
일반화할 inductive bias가 없으면 truth는 held-out으로 전파 안 됨(memorize·not compose). 일반
MLP의 이 실패는 303M forward-CE trunk의 재조합 실패와 동형(둘 다 memorize·not compose). 즉
**escape = verifier(corpus-외 truth) + 조합적 inductive bias(구조 일반화)** 둘 다 필요.

## 잔여 (fair test 위한 base 교체)
verifier의 기여를 측정하려면 base가 corpusnull서 lift하는 = 구조 일반화하는 아키텍처 필요:
tied-embedding(a·b 공유표) + relational readout, 또는 grokking-tuned(대량 step+WD), 또는 MLP가
grok하는 더 쉬운 조합 task. 그때 corpusnull이 lift하면 verifier의 예산효율 기여를 격리 측정 가능.
scope: a_toy_scale_recheck. DPI escape 논증(Fable)은 이 toy와 독립으로 유효.
