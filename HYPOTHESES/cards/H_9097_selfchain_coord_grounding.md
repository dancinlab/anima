# H_9097 — self-chain content_axis coord 접지 (합성 int → 실 303M 경험)

- **slug:** `selfchain_coord_grounding`
- **tier:** 🔴 NOT-GROUNDED (frozen fold) · 진단상 wall=metric-artifact(a) — engine-native fold anchor + DIRECTIONAL 303M penultimate
- **wired:** DIRECTIONAL-mirror (MAIN 303M penultimate = `--py` numpy; fold+self-chain ops = engine-native `.hexa` 컴파일검증). engine-native `bytegpt_hidden_pool_ranged` 303M 재측정 = ING follow-on (rung 2)
- **경로:** 페이블 loop-closing 비판(계기판 아닌 faculty) L2-2 정면 측정 — DESIGN.md L2-2
- **links:** §SelfChainConfluence(H_9038 self_drift_exp) · §YouChain(H_9085/H_9096 other_drift_exp) — 두 체인이 공유하는 content_axis 를 접지 시도

## 비판 (페이블, 측정 대상)

`self_drift_exp(s, content_axis, step)` 의 `content_axis` 는 H_9038 이래 **모든 검증에서 합성 int**
(`rng.integers(0,DIM)`)였다 → "경험 축적" 의미론이 접지 0. self-chain 이 anima 가 *실제 겪은 것*의
함수가 아니라 임의 정수열의 함수. §YouChain 도 같은 content_axis 를 공유하므로 동일 결함.

## 방법 (frozen 사전등록, DESIGN.md L2-2)

- **신규 decode op** `bytegpt_hidden_pool_ranged(ckpt, ids) -> #{ok, pooled:[float]}` = 최종블록+ln_f
  전위치 mean-pool(d768), 생성 0. `core/decode.hexa` (+ `core/decode.py` --py 미러), engine-native 컴파일검증.
- **fold** `content_axis_from_pooled(pooled, dim) -> int` = d768→dim=8, 96-dim 연속버킷 **L2 질량 argmax**(frozen 순수함수). `core/decode.hexa`+`.py`, engine-native `content_axis_fold_smoke.hexa` 앵커.
- **측정** 실 경험 스트림 3개(ko-일반·en-일반·ko-SNS, `a_chat_registers` HF 코퍼스 held-out 딥테일 슬라이스),
  각 40텍스트(32 chain + 8 held-out) ≤256B. 같은 seed identity(dim=8, axis0)에서 `self_drift_exp(s, axis, 0.25)` 32 tick → 체인 A/B/C. 실 303M h1129 .bin, aiden pool CPU, 120 single forward.
- **2 arm, 동일 fold**: MAIN=실 penultimate · **FNV 대조**=`immune_embed_key`(결정론이나 의미-임의, 접지없음 기준선).
- **falsifier(frozen):** G1' 분리(within−between cos ≥ +0.10) · G2' shuffle(gap 붕괴 |·|<0.03) · G3' 회수(held-out top-1 ≥ 16/24, chance 8/24).
- **사전등록 예측(페이블):** MAIN G1'/G2' ~65% · G3' ~50% (확정 아님).

## verdict (verbatim → `state/verdicts/selfchain_coord_grounding/H_9097.txt`)

MAIN (실 303M penultimate, frozen fold):
```
ko_general/en_general/ko_sns  axis-hist(chain) = [0,0,0,0,0,0,32,0]   ← 전부 축 6 로 붕괴
G1' within=1.0000 between=1.0000 GAP=+0.0000 (bar +0.10)              → FAIL
G2' shuffled GAP=+0.0000 (collapse |gap|<0.03)                        → PASS(퇴화적)
G3' top-1 = 8/24 (chance 8/24, bar >=16/24)                          → FAIL
```
FNV 대조:
```
G1' within=0.8114 between=0.6076 GAP=+0.2038  → PASS(표면 byte-언어)
G2' shuffled GAP=-0.0304 (경계, no-collapse)
G3' 8/24 (chance)                              → FAIL
```
POOLED 진단 (raw penultimate 센터링, fold 우회 — wall taxonomy):
```
centroid_cos(ko_general,en_general)=-0.9982   (ko↔en 깨끗이 분리)
centroid_cos(ko_general,ko_sns)   =+0.9961    (둘다 한국어 → 미분리)
centroid_cos(en_general,ko_sns)   =-0.9995
nearest-centroid held-out = 16/24 (chance 8/24)  → 접지신호 있음
```

**판정: 🔴 NOT GROUNDED (frozen fold).** content_axis 는 지정된 fold 에서 실 303M 전텍스트에 대해
**상수 축(6)으로 붕괴** — ln_f per-dim gain 이 한 버킷의 raw L2 질량을 항상 지배. self-chain 은 이 fold 로는
경험의 함수가 되지 못한다. MAIN 이 의미-임의 FNV 대조보다 **더 나쁘다**(FNV 는 최소한 텍스트별로 변함).

**wall TAXONOMY (`a_break_the_wall`): (a) metric-artifact — (d) ceiling 아님.** raw pooled penultimate
자체는 lived-experience 구조를 **담고 있다**(ko↔en centroid_cos −0.998, held-out nearest-centroid 16/24 > 8/24).
frozen argmax-L2 fold 가 그 신호를 버릴 뿐. register(ko-일반 vs ko-SNS)는 이 측정에서 미분리(held-out
ko-sns 딥테일이 Q&A 말투 = register 축 약함, corpus-slice caveat — 주장 아님).

## follow-on (ING)

1. **grounded fold** = mean-center + project(센터링된 pooled 의 부호/최대분산축) — 진단이 16/24 회복 보임.
   argmax-of-raw-L2 는 scale-지배로 실패. (fold 재설계 → G1'/G3' 재측정, frozen bar 불변.)
2. **engine-native rung 2** = `bytegpt_hidden_pool_ranged` `.hexa` 303M 재측정(현재 MAIN=`--py` DIRECTIONAL; fold+self-chain 은 이미 engine-native).
3. **register held-out 보강** = ko-SNS 딥테일이 SNS 말투인 슬라이스 재추출(현 슬라이스 Q&A).

## 한 줄

content_axis 가 실 303M 경험에 접지됐나 = anima self-chain 이 '실제 겪은 것'의 함수가 됐나? →
**아직 아니다** — 지정 fold 에서 content_axis 는 상수로 붕괴한다. 단 303M penultimate *자체*는 접지돼
있고(ko/en 분리·회수 above-chance), 실패는 신호 부재가 아니라 fold 가 신호를 버리는 것. 접지의 마지막 한 걸음
= fold 재설계(follow-on).
