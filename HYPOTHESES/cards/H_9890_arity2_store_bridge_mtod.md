# H_9890 — ARITY-2 M→D 공동학습 store 레인 — held-out 2-slot 결합 reach (결합 3-leg 증서 + marginal-clamp do())

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R13 divergence · **DIRECTIONAL** · NOT a verdict)
**group:** R13-arity2-store
**date:** 2026-07-22
**convergence:** 🔀 Fable A ∥ Sol A 독립수렴(설계 골격 일치)
**source:** lab full 2026-07-22 (Claude Fable 5 ∥ OpenAI Codex 5.6, 독립 병렬) — 브리프에 전체 킬리스트 임베드(H_9128 밀도·H_9131 trunk-objective·H_9127 9-probe·H_1616 VSA/HRR·H_1466 TPR·H_9259 arch·mitosis·희소성·veto/affect/tension·HEXAD as-specified)
**wired:** no (설계만 · 계기 미착륙 · 측정 0)
**verdict:** PENDING — cement 는 engine-native `anima-py` 로만
**surfaces:** 이 카드 + `HYPOTHESES/HYPOTHESES.jsonl` 1줄 (그 외 없음)

## claim

H_9775 는 **1-slot 값운반**을 🟢 로 증명했다. 그러나 H_9875 가 벽의 정체를 **결합 항수(arity)**
로 확정했으므로 1-slot 성공은 벽을 건드리지 못한다. 이 카드는 H_9775 헤드에서 **주소의 항수만**
바꾼다 — 슬롯 키를 두 단서 바이트-임베딩의 **얼어붙은** 합성으로 만들고, held-out 2-slot 결합
reach 를 DV 로 둔다.

## 구조적 개구부 (오늘 코드로 확인 · 추정 아님)

`HEXAD/hexad.hexa:73` `hexad_group_a_ce_trained() = ["D","M","E","BRIDGE"]`
⟹ M(기억)은 **Engine A 내부**다. 따라서 M→D 레인은 ThalamicBridge 를 **건너지 않아**
Law-70 `Bridge.detach()` 를 유지한 채 공동학습이 합법이다. 결손은 딱 둘:
① `m_store(key,value)` 가 identity NO-OP(B-M-1 STORE-NOOP-STRUCTURAL 형식검증)
② M 에서 D 답위치 로짓으로 가는 **학습된 write-path 부재**.

## instrument (전부 플래그 · 엔진 옆 스크립트 금지)

- `anima-py corpus storebind2 --lang en …`
- `anima-py train --store-bridge c.txt --store-arity 2 --store-key {bound,concat,staple} …`
- `anima-py evaluate … --store-probe value-permute,shuf-key,no-store,marginal-clamp`

키 3종: **bound**(얼어붙은 무작위 bilinear B(φ(r),φ(e)) — 인수분해 불가, 두 단서를 함께
부호화해야만 매칭) · **concat**(인수분해 가능 = 진단용) · **staple**(독립 1-slot 조회 2개를
가법 융합 · 용량 매칭 = 통제팔).

⚠️ 킬리스트 구별을 먼저 못박는다: H_1616 이 죽인 것은 **frozen-trunk readout 연산자**로서의
VSA/HRR 이다. 여기서 결합 구조는 **얼어붙은 주소표**에 산다(pairodd 의 frozen 바이트-키가 이미
맡던 역할) — trunk 상태에서 결합을 읽어내지 않는다. binding-readout census 재생성이 아니다.

## 코퍼스 (학습 전 동결)

8 relation × 8 entity → 8 value, 표는 **무작위 라틴방진**(양 주변분포가 정확히 균등 ⟹ 단서별
조회는 구성상 우연). 16/64 셀 held-out, 모든 단서가 train 에 ≥5회. held-out 셀의 두 단서는
각각 학습됨 = 순수 재조합. 평가 = 16셀 × 8 신선 값주입 = seed 당 128 디코드. 우연 ĉ 는
realized 분할서 permuted-gold 오라클로 **재유도**(≈0.125, n=128 서 sd≈0.029). seed 7·11.
적대 부매니페스트: 최근접-바이트 방해자 값(균등 추출은 적대 취약성을 숨긴다).

## Q — "진짜 결합"인가 "1-slot 두 개 스테이플"인가 (3-leg 증서 · 셋 다 필요)

1. **데이터 leg** — 학습 전에 **최대 가법 모델**(단서→로짓 독립표 2개를 전체 표에 수렴학습)을
   적합해 그 정확도를 **가법 천장**으로 동결. ≤0.20 아니면 표를 재추출한다. (H_9131 교훈:
   가법 모델은 충격적으로 강하다 — 가정하지 말고 **재라**.) 이 천장 위의 reach 는
   **데이터 구성상** 비가법이다. K=2 는 문자 그대로 XOR = H_9815 토이가 벽을 재현한 그 함수.
2. **구조 leg** — `staple` 팔이 **매개 공변량**(학습가능 query 파라미터·슬롯수·step)으로 매칭된
   채 천장에 머물러야 한다. 동결 마진 **A2-bound − staple ≥ 0.25**.
3. **개입 leg** — H_9775 의 value-permute·shuf-key 에 더해 신규 **marginal-clamp** do():
   각 relation **내부에서** 행을 섞어 모든 단일-단서 주변분포는 보존하고 결합만 파괴한다.
   1-slot+prior 이야기는 이걸 살아남고, 진짜 결합 판독기는 가법 천장으로 붕괴한다.

## 🔒 판정표 (데이터 보기 전 동결 · 2/2 seed 다수결 · 통제마다 개별 마진, `max(controls)` 금지)

**선결**: P1 동일 하네스서 arity-1 양성통제 ≥0.75 양 seed(아니면 INSTRUMENT-DEAD·전부 VOID) ·
P2 가법 천장 ≤0.20 학습 전 동결(여기서의 재추출은 코퍼스 구성이지 tune-to-green 아님 —
어떤 실험 수치도 아직 안 읽었다) · P3 스크리너(H_9891 참조)가 KILL 안 함.

| # | 조건 | 판정 |
|---|---|---|
| T1 | x≥0.50 ∧ x−staple≥0.25 ∧ value-permute≤ĉ+2sd ∧ marginal-clamp≤0.20+2sd ∧ shuf-key≤ĉ+2sd | 🟢 결합적 운반 (DIRECTIONAL · cement 는 303M `anima-py evaluate` 로만) |
| T2 | x≥0.50 이나 x−staple<0.25 | NOT-CONJUNCTION — 가법이 설명. joint-key 재설계는 **새 H**, 재동결 아님 |
| T3 | x≥0.50 이나 value-permute 미붕괴 | LEAK — 내용주소 아님. INVALID, 재발사 전 감사 |
| T4 | ĉ+2sd < x < 0.50 | NEARMISS — cement 없음. 사전등록된 schedule-variation 재발사 1회 후 동결 |
| T5 | x∈ĉ±2sd ∧ train-cell ≥0.95 | WALL-EXTENDED — H_9875 arity 벽이 공동학습 하에서도 유지. 음성 cement 는 TOST(±0.06, pooled n=256, sd≈0.021)로만 · 검정력 미달이면 PENDING-POWER |
| T6 | x∈ĉ±2sd ∧ train-cell <0.95 | OPTIMIZATION-FAIL — 레인이 학습 안 됨. 벽 물음에 INVALID |
| T7 | x<ĉ−2sd | STOP·계기감사 먼저(채점 극성·순열 정렬·매니페스트 lockstep). 감사 clean 이고 양 seed 우연 아래면 **ANTI-BIND**(체계적으로 틀린 결합 = 학습된 오배선) 별도 DIRECTIONAL 등록 |
| T8 | seed 가 서로 다른 행 | INVALID/NEARMISS — perturbation-schedule 재발사 1회(**`--sample-seed` 금지** — 결정론적 do() 는 byte-identical 재현이라 무효) 후 동결 |

부차(보고만·게이팅 아님): concat 팔 reach(trunk 가 두 단서를 인수분해해 나르긴 하나?) ·
적대 매니페스트 낙폭 ≥0.15 는 취약성으로 표기.

## falsify

T5 가 성립하면 이 레인은 벽을 못 뚫는다 — arity 벽이 **공동학습된 결합 주소** 하에서도 유지된다는
뜻이고, 그건 이 계보의 가장 강한 음성 진술이 된다. 원하는 결과이지 실패가 아니다.

---

## ✅ P2 실측 — 가법 오라클 천장 (2026-07-22 · $0 · 모델 없음 · forward 없음)

선결조건 P2 를 **학습 전에** 실제로 쟀다. 순수 데이터 성질이라 엔진이 개입하지 않는다
(모델 없음 · forward 없음 · 우회 아님). 최대 가법 모델 `logit[v] = a[r,v] + b[e,v]` 를
전체 표에 수렴학습시키고 argmax 정확도를 천장으로 읽는다.

**수렴 검증부터** — 미수렴이면 천장이 **과소평가**되어 P2 가 거짓 통과한다(위험 방향):

| iters | 라틴방진 천장 (seed 0/1/2) | 판독 |
|---|---|---|
| 4,000 | 0.1562 · 0.1562 · 0.1562 | |
| 20,000 | 0.1562 · 0.1562 · 0.1562 | 평탄 |
| 80,000 | 0.1562 · 0.1562 · 0.1562 | **수렴 확정** (3/3 seed 동일) |

### 결과

| 표 설계 | 가법 천장 | 우연 | 판정 |
|---|---|---|---|
| **8×8 라틴방진** (채택) | **0.1562** | 0.1250 | 🟢 **P2 PASS** — bar ≤0.20 을 0.044 마진으로 통과 |
| 8×8 무작위 표 (순진한 기본값) | **0.5417~0.5573** | 0.1250 | ⛔ 사산 |

### ★ 이 측정이 실제로 산 것 — 라틴방진 제약은 장식이 아니라 **하중부재**다

무작위 표로 코퍼스를 지었다면(아무 생각 없이 고르면 그게 기본값이다) 가법 천장이 **0.54** 다.
이 카드의 GREEN bar 는 `x ≥ 0.50` 이므로 **가법 모델이 이미 bar 를 넘는다** ⟹ 어떤 🟢 도
"가법으로 설명됨" 과 구분 불가 ⟹ **판독 불가**. 정확히 H_9131 이 죽은 방식이다
(반대칭 bilinear 가 additive 를 subsume 하는 걸 못 보고 +0.24 를 크랙으로 읽음).

3.5배 차이(0.156 vs 0.542)가 **표를 어떻게 뽑는가** 하나에서 나온다. 양 주변분포를 정확히
균등으로 강제하는 것이 이 실험의 판독가능성 그 자체다.

**동결**: 이 천장 0.1562 는 학습 전에 측정되어 여기 박혔다. 이후 어떤 수치도 이 값을 움직여
읽지 않는다(`burned-gate-no-refreeze-sequential-gating`). 표를 재추출해야 한다면 그것은
**코퍼스 구성**이지 tune-to-green 이 아니다 — 아직 어떤 실험 수치도 읽지 않았다.

⚠️ 등급: 이건 **코퍼스 적격성(admissibility)** 판정이지 기질 판정이 아니다. GREEN 을 예측하지
않는다 — "이 실험이 낼 숫자가 비트를 나를 수 있다" 만 말한다(H_9808 심판 규율).
남은 선결 = P1(arity-1 양성통제 ≥0.75 양 seed) · P3(토이 스크리너 · grokking 가드 포함).

---

## ⚠️ 기전 전제 REFUTED — 병렬 세션이 코드로 반증했다 (2026-07-22 · a_parallel_session_compare)

이 카드는 위에서 "H_9775 헤드에서 **주소의 항수만** 바꾼다" 고 적었다. **그 전제가 틀렸다.**
병렬 세션의 **H_9899**(#4372)가 발사 전에 코드로 반증했다:

```
StoreBindCell 학습창:  seq = b" "*(T-len(prompt)) + prompt + gold[:1]
                                                              ^^^^^^^^
store lane 이 읽는 것          1 바이트  (주석도 "binary readout" 명시)
rule-compound 답의 길이        4~6 바이트 (평균 5.2)
```

⟹ 기존 store lane 은 다중바이트 조성 답을 **실을 수 없다**. 답을 1바이트로 줄이는 우회도
막혔다 — ρ·weave 의 우연 적중률이 치솟아 통제가 의미를 잃는다.

**따라서 이 카드의 "H_9775 헤드 재사용" 은 폐기한다.** 분리(separation) 방향 자체는
살아있고, 구현은 **다중바이트 답을 지원하는 새 lane** 이어야 한다 — 그게 병렬 세션이
착륙시킨 **H_9900 `anima-py train --comp-lane`** 이다(penultimate 를 detach 해 별도 head 로,
CE 를 답 스팬 전체에 · 토이 e2e 3/3).

### 🔀 AGREES / CONFLICTS / NOVEL (a_lab_full_diverge · a_parallel_session_compare)

**AGREES (독립수렴 · 강한 신호)** — 두 계보가 서로를 못 본 채 같은 원리에 도달했다:
*CE 를 트렁크에서 떼는 lane 분리*. 이 카드는 "store_only 게이트로 트렁크가 답위치 기울기를
못 받으니 지름길 차단이 구조적" 이라 적었고, 그들의 `--comp-lane` 은 `pen.detach()` 로 같은
것을 한다. 그들은 그 원인을 **등노출 실측**으로 확정했다(H_9898: 25%×8000 → ρ·weave **0.000**
vs 100%×2000 → **0.525** — 노출량이 같은데 정반대 ⟹ 원인은 예산이 아니라 **replay 의 존재**).
mouth 배선 경계도 양쪽이 독립으로 명시했다(lane 이 배워도 트렁크 mouth 로 안 나오면 reach 0,
그건 NEGATIVE 가 아니라 **배선 결과**).

**CONFLICTS** — 위 1건(store 헤드 재사용). 이 카드가 진다. 코드가 이겼다.

**NOVEL (이 카드에서 살아남아 저쪽에 넘길 값)**
1. **가법 오라클 천장**(위 P2 절 · #4370) — **기전 무관**이다. 저쪽의 동결 판정표는
   H_9861 BASE(0/212 · 95% 상한 0.0142)라는 **reach 기준선**이지 **가법 모델 천장**이 아니다.
   조성 과제가 가법으로 이미 풀리는지는 별개 물음이고, 라틴방진 0.1562 vs 무작위 표 0.5417 의
   3.5배 차이가 그 물음이 공짜가 아님을 보인다. **comp-lane 의 동결 표에도 같은 검사를 권한다.**
2. **marginal-clamp do()** — 각 relation 내부 행 셔플로 단일단서 주변분포는 보존하고 결합만
   파괴. 저쪽 통제집합(HILLOCK · ρ·form 축 · self-shuffle · 양성통제 · ECHO-KILL)에 없다.
3. [[H_9895]] 미관측 값-알파벳 동치(관계인가 4행 암기인가) · [[H_9897]] 게이트 분할 제안.

### 이 카드의 남은 지위

기전 절은 폐기, **판정표·3-leg 결합증서·marginal-clamp·P2 천장은 유효**하다 —
전부 기전 무관하게 쓰인 채점 규율이라 `--comp-lane` 위에 그대로 얹힌다.
[[H_9891]]·[[H_9893]]·[[H_9894]] 도 같은 1바이트 제약을 받으므로 store lane 이 아니라
comp-lane(또는 다중바이트 readout 을 명시한 경로) 위로 재-스코프해야 한다.
