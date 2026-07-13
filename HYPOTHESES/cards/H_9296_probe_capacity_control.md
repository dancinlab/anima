---
id: H_9296
slug: 9296_probe_capacity_control
title: 프로브-용량 통제 — H_9289 의 INFO-ABSENT 는 표현의 사실인가 프로브의 사실인가 (⏳ INVALID + INFO-ABSENT→NOT-POWERED 재분류)
group: g1-crack-natural-emergence 프런티어 · NBIND-G 접지 채널 (H_9289/H_9291 후속)
terminal_tier: ⏳ INVALID (2026-07-14 · 사전등록 V-SHUF FAIL · tier 미보고 · bar 무이동) — **그러나 그 실패의 원인 추적이 H_9289 의 INFO-ABSENT 를 NOT-POWERED 로 재분류한다.** held-out 원자 n=29 ⇒ 우연 sd = 0.0928. ① 내 V-SHUF 밴드(±0.08 = ±0.86σ)는 **우연 셔플이 39% 확률로 벗어나도록** 잘못 명세됨(계측 결함) ② **동결 bar 0.65 가 우연에서 겨우 1.62σ** ⇒ H_9289 의 INFO-ABSENT 근거 0.5517 = **16/29, 단측 p=0.356** = "없다"가 아니라 **"n=29 로는 못 찾는다"**. MDE: bar 0.65 를 80% 검정력으로 넘으려면 참 정확도 ≥ **0.71** 필요. 프로브-용량은 범인 아님(선형/MLP/문맥별/문맥별-MLP 4단 어디서도 seed-robust 돌파 없음 — P-CTX 가 main_s11 서 0.690(20/29, p=0.031) 이나 s7 서 0.552 재현 실패). ⇒ 프런티어의 **"INFO-ABSENT ⇒ 벽=추출채널 ⇒ O/C 채널"** 첫 고리가 NOT-POWERED 위에 있다. NEXT = **n≥100 (P_nat 재고 확대)** · 셔플은 밴드가 아니라 순열 귀무분포 · 음성주장은 TOST.
wired: 미배선 (배선할 GREEN 없음)
verdict_dir: state/verdicts/9296_probe_capacity_control/
terminal_verdict: state/verdicts/9296_probe_capacity_control/H_9296_RESULT.txt
prereg: state/nbindg_grounding/PREREG_H9296.md (hidden dump 開封 前 커밋 e5e26d95a)
date: 2026-07-14
provenance: 로컬 py 2-production (anima-py evaluate --dump-hidden · frozen N2 ckpt 4-arm) · $0 · 재학습 0
---

# H_9296 — 프로브를 의심했더니, 프레임 전체에 검정력이 없었다

## 물음

프런티어 `g1-crack-natural-emergence` 의 다음 수(O채널/C채널)는 이 사슬 위에 서 있다:

```
H_9291 오라클  정보는 있다 (29/29 = 1.000 · shuffle 0.517)
      ↓
H_9289 G-PROBE 그런데 303M 표현에서 안 읽힌다 (0.5517 ≈ chance · bar 0.65)
      ↓
      INFO-ABSENT  ⇒  벽 = 추출 채널  ⇒  O/C 채널 설계
```

그런데 H_9289 의 G-PROBE(`gt_step0_gprobe.py`)는 두 선택을 했다: ① **선형**(L2-logreg)
② 원자당 24 문맥을 **평균풀링**한 뒤 물음. **오라클은 문맥을 하나하나 개별로 읽고 1.000 을 냈다.**

> "303M 이 인코딩 못 했다" 와 "선형으로·평균풀링 후엔 안 읽힌다" 는 **다른 명제**다.

## Method (사전등록 · hidden dump 뜨기 前 커밋 `e5e26d95a`)

H_9289 에서 **프로브 하나만** 바꾼다 (frozen ckpt 4-arm · gt_prompts · split · bar 0.65 전부 무이동):

| 프로브 | 표현 | 분류기 | 묻는 것 |
|---|---|---|---|
| P-LIN | 24-ctx 평균풀링 | L2-logreg | H_9289 재현 (V-REPRO 앵커) |
| P-NL | 24-ctx 평균풀링 | MLP | 비선형 인코딩인가 |
| P-CTX | **문맥별 개별** | logreg → 원자당 다수결 | **평균풀링이 신호를 지웠나** |
| P-CTX-NL | 문맥별 개별 | MLP → 다수결 | 용량 상한 |

## Result

| arm | P-LIN | P-NL | P-CTX | P-CTX-NL |
|---|---|---|---|---|
| main_s7 | 0.552 | 0.517 | 0.552 | 0.448 |
| main_s11 | 0.552 | 0.586 | **0.690** | 0.586 |
| base_only | 0.517 | 0.552 | 0.414 | 0.414 |
| shuffle_grid | 0.552 | 0.552 | 0.483 | 0.448 |

(train_fit 전 셀 1.00) · 라벨-셔플 통제: 0.483 ~ 0.621

**V-REPRO PASS** (P-LIN main_s7 = 0.552 vs H_9289 의 0.5517 ⇒ 파이프라인 byte-충실) ·
**V-FIT PASS** · **V-BASE PASS** · **V-SHUF FAIL** (셔플이 사전등록 밴드 0.5±0.08 이탈)

⇒ 사전등록 결정표 0행: **⏳ INVALID · tier 미보고.** (밴드를 사후에 넓히지 않는다)

## 그 FAIL 을 추적했더니 — 본 H 의 진짜 결과

held-out 원자 **n = 29** ⇒ 우연(p=0.5)의 **표준편차 = √(0.25/29) = 0.0928** (한 문항 = 0.0345)

**(a) 내 V-SHUF 밴드가 잘못 명세됐다.** ±0.08 = **±0.86σ** ⇒ 우연 수준 셔플이 이 밴드를
**39% 확률로 벗어난다(구성상)**. V-SHUF 는 암기를 검출한 게 아니라 **표본 잡음에 걸려 넘어졌다**.
(내 계측 결함이고, 밴드를 넓히는 대신 이렇게 보고한다.)

**(b) 더 중요한 것 — 동결 bar 0.65 자체가 잡음 안에 있다.**

| 값 | 우연 대비 | 단측 정확 p |
|---|---|---|
| bar 0.65 | **1.62 σ** | — |
| H_9289 의 INFO-ABSENT 근거 **0.5517 = 16/29** | 0.56 σ | **p = 0.356** |
| 본 H 최고 P-CTX main_s11 **0.690 = 20/29** | 2.05 σ | p = 0.031 (그러나 s7 = 16/29 재현 실패) |

**MDE**: n=29 에서 bar 0.65 를 80% 검정력으로 넘으려면 **참 정확도 ≥ 0.71** 이어야 한다.

> ⇒ **H_9289 의 "INFO-ABSENT" 는 null 이 아니라 NOT-POWERED 다.** 0.5517 은 "신호가 없다" 가
> 아니라 **"n=29 로는 못 찾는다"** 이다. (`negative-claims-need-tost-not-ns` — 음성 주장은
> 'ns' 가 아니라 사전등록 TOST 로 벌어야 한다.)

## Verdict — ⏳ INVALID + **INFO-ABSENT → NOT-POWERED 재분류**

**말하는 것.**
1. **프로브-용량은 범인이 아니다** — 4단 사다리 어디서도 seed-robust 돌파가 없다. 평균풀링
   가설(P-CTX)은 main_s11 에서만 반짝(0.690)하고 s7 에서 죽는다.
2. **그러나 "표현에 없다" 도 증명되지 않았다.** n=29 에서 bar 0.65 는 1.62σ — 이 프레임은
   "중간 세기 신호" 와 "무신호" 를 **원리적으로 구별하지 못한다**.
3. ⇒ 프런티어의 사슬 **"INFO-ABSENT ⇒ 벽 = 추출 채널 ⇒ O/C 채널"** 의 **첫 고리가
   NOT-POWERED 위에 있다.** O/C 채널 설계가 **틀렸다는 말이 아니라**, 그 근거가 아직
   벌어지지 않았다는 말이다.

**말하지 않는 것.** "표현에 신호가 있다" 가 아니다(P-CTX 재현 실패) · H_9291 오라클(정보 존재)과
H_9286 ARBITRARY-GROUNDING 은 영향 없음(별개 측정) · frozen ckpt·prompts·bar 전부 무이동.

## NEXT — 검정력이 먼저다 (계측 수리이지 bar 이동이 아니다)

1. **n 을 늘려라 — 유일한 진짜 게이트.** held-out 29 → **≥ 100** 이면 우연 sd 0.093 → 0.050,
   bar 0.65 가 **3.0σ** 가 된다. 병목 = P_nat 재고(purity ≥ 0.85 감성 원자) — H_9286 이 이미
   이 벽을 만났고(k=15/pol) 외부 코퍼스 450k 로 29 까지 왔다 ⇒ **더 크거나 다른 도메인의
   코퍼스가 필요**.
2. **셔플 통제는 밴드가 아니라 순열 귀무분포로** (≥200 순열의 백분위). 단일 draw + 임의 밴드는
   계측 결함이고, 본 H 가 그 실례다.
3. **음성 주장은 TOST 로** — INFO-ABSENT 를 벌려면 사전등록 등가마진 + N_REQ 를 데이터 전에 고정.

## Cross-links

H_9289 (INFO-ABSENT — 본 H 가 NOT-POWERED 로 재분류) · H_9291 (오라클: 정보 존재 · 영향 없음) ·
H_9286 (ARBITRARY-GROUNDING · 영향 없음) · H_9290 (NAT-ATOM NO-RESCUE — 같은 n=29 프레임이라
동일 검정력 주의) · `negative-claims-need-tost-not-ns` · `probe-defect-census-max-control-bias` ·
`measurement-metalaw-form-tunable-bind-earned` · `a_eval_py_canonical` · c9 · c16 · p7
