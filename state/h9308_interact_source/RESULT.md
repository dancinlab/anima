# RESULT — INTERACT-SOURCE 스크리너 (개입 분포에 bits 가 있는가)

**VERDICT: NOT-POWERED** — 디스크의 자기 실행 궤적에서 **행동의 조건부 엔트로피가 정확히 0**
(`H(A|S=stage) = 0.000 nats`, 5/5 궤적 · 3,400 tick). `I(A;Y|S) ≤ H(A|S)` 는 항등부등식이므로
`I=0` 은 **측정 결과가 아니라 정의상 강제된 값**이다. PASS/FAIL 어느 쪽도 벌 수 없다.

## 계측 사실 (판정의 전부)

`(stage, emit)` 교차표가 결정적 — 3 궤적 900/900 tick 모두 동일:

| stage | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| EMIT | 600 | 100 | 0 | 0 | 20 |
| ACTIVE_VETO | 0 | 0 | 100 | 79/80 | 0 |

즉 emit = f(stage) 인 **결정적 스크립트 정책**(pod 실행 meta 에 `stage_cycle: true`). h1058 궤적 2개도 같은 규칙.
행동의 *내용* 엔트로피도 0 — 궤적당 `gtext_sha` 는 2종뿐(고정 80B 발화 1개 + 빈 문자열=silence).
⇒ 이 로그는 **do-분포가 아니라 관찰-로그**이며, 개입 변동이 애초에 존재하지 않는다.

## 수치

| 항목 | 값 |
|---|---|
| n (t→t+1 쌍, worktree-tracked 5 궤적) | **3,400** |
| H(A) 주변 | 0.438 nats |
| **H(A\|S=stage)** | **0.000 nats** ⇒ V-CEILING **FAIL** |
| REAL `Î(A;Y\|S)` | 0.000 (95% CI [0.000, 0.000] · perm p=1.0) |
| PEDESTAL (참값 0) | 0.000 — V-PEDESTAL PASS |
| ACTION-SHUFFLE 통제 | 0.000 |
| STATE-ONLY `Î(S;Y)` | **0.0211 nats** — 결과채널 Y 는 살아있음(죽은 건 행동의 자유도) |
| **ALIVE 양성대조** | measured **0.36808** vs truth **0.36806** — **ratio 1.00005** ⇒ 추정기 무죄 |
| MDE / N_REQ (참값 0.02 nats, 정책이 잔여엔트로피 ln2 를 가질 때) | **N_REQ(80%) = 500 tick** (n=2,705 은 5배 초과) |
| TOST(±0.02) | 형식상 PASS 이나 **천장 0 의 부산물 ⇒ 무효** |

**추정기는 인증됐고 데이터 양도 충분하다. 부족한 건 n 이 아니라 정책 엔트로피다.**

## SECONDARY DIAGNOSTIC — 함정 (양성으로 오독될 수 있었던 것)

조건집합에서 stage 를 빼고 `S-lite = tercile(idle)` 로 조건화하면
`Î(A;Y|S-lite) = 0.0079 nats · perm p = 0.0033` 로 **유의하게 양(+)** 이 나온다.
이것은 do-효과가 아니라 **stage 매개 교란**이다 (emit=f(stage) 이고 stage 가 ΔC 도 구동).
사전등록에서 이 경로를 진단용으로 못박아 뒀기에 헤드라인으로 승격하지 않는다 — 승격했으면
"개입 분포에 bits 가 있다"는 거짓 PASS 를 제조했을 것이다 (게다가 0.0079 < 마진 0.02 라 TOST 로도 등가).

## 산출물
- `PREREG.md` (효과 보기 전 프리징 · V-CEILING 게이트 포함)
- `interact_mi.py` · `RESULT.json` · `run.log`

## 이 결과가 죽인 것 / 살린 것
- **죽인 것**: "기존 궤적 2,342 tick 으로 개입-정보원을 $0 에 판정한다"는 킬샷 **설계 자체**.
  디스크의 궤적은 개입 분포가 아니다.
- **살린 것**: 가설 자체(카드 2 본체)는 **미검정으로 살아있다** — NOT-POWERED 는 FAIL 이 아니다.
  그리고 계기는 완성됐다(ALIVE ratio 1.00005 · PEDESTAL 0 · N_REQ 500).
- **다음 발**: ε-확률적 emit 정책(같은 stage 안에서 Bernoulli-ε 로 emit/veto 를 무작위화 = 진짜 do)으로
  데몬을 ≥500 tick 재실행. $0 CPU. 그 로그에서만 이 DV 가 정의된다.
