# AURA A7 — 결합규칙 robustness sweep (A6 big-Φ falsifier 강건성)

> A6 는 단일 결합규칙(M1=self-copy vs bypass=majority)에서 ΔΦ(bypass − M1) = +17.66 > 0
> (n=4 engine-exact) 을 보였다. A6 §5 잔여 R1: "majority/0.9-0.1 confidence 는 임의 모형 —
> 다른 결합규칙에서도 부호가 유지되는가?" 이 문서가 그 robustness 를 닫는다.
> honest: toy synthetic TPM, 실제 N1/EEG 아님. n=4 toy, 절대 Φ 무의미 (부호·순서만 주장).
> toy substrate ≠ production scale (`feedback_toy_scale_transfer`).

---

## 1. 방법 (method)

A6 와 동일한 폐루프·동일 엔진을 그대로 재사용한다 (g61 engine ⊥ adapter):

- 엔진: `stdlib/consciousness/iit4_bigphi.hexa` 의 `big_phi(tpm, n, sys_state)`
  (BRAIN/eeg 어댑터와 같은 한 벌, n≤8 exact). A6 와 import 패턴 동일.
- 설정: n=4 노드, sys_state=1111 (all-ON), deterministic, $0, hexa-only, LLM 0.
- harness: `AURA/toy/a7_coupling_sweep.hexa`.

각 결합규칙 family 마다 **짝(matched pair)** 을 합성한다:

- **M1-like** = LOCAL / self / 저결합 (노드가 주로 자기 자신에 의존 → reducible → 작은 Φ)
- **bypass-like** = HUB / projection / 고결합 (노드가 *다른* 노드들에 의존 → irreducible → 큰 Φ)

규칙별 측정량 = ΔΦ = `big_phi(bypass)[0] − big_phi(M1)[0]`.
PASS = ΔΦ > 0 (falsifier H 미반증) · FAIL = ΔΦ ≤ 0 (그 규칙에선 반증 = rule-specific).
확률은 A6 의 0.9/0.1 confidence 규약을 유지 (엔진이 A6 와 같은 수치 regime 을 보도록).

### 6 결합규칙 family

| # | 이름 | M1-like (local) | bypass-like (hub) |
|---|---|---|---|
| 1 | self-copy / majority | 자기복사 | 나머지의 다수결 (A6 baseline) |
| 2 | self / maj-threshold | 자기복사 | 나머지의 strict-majority (≥) |
| 3 | self / AND-all | 자기복사 | 나머지가 *전부* ON (AND) |
| 4 | self / OR-any | 자기복사 | 나머지 중 *하나라도* ON (OR) |
| 5 | self+fixed / sparse-2 | 자기복사 | 고정된 2개 타 노드의 XOR (sparse hub) |
| 6 | self-dom / XOR-parity | 자기복사 | 나머지 전체의 parity(XOR) |

(M1 측은 모든 family 에서 self-copy 로 환원 = 국소 자율의 공통 baseline. 차이는 bypass 측 결합형태.)

---

## 2. 결과 — 규칙별 ΔΦ 표 (verbatim)

실행 출력 (`AURA/toy/a7_coupling_sweep.hexa`):

| 규칙 | Φ_M1 | Φ_bypass | ΔΦ (bypass − M1) | PASS/FAIL |
|---|---|---|---|---|
| 1 self-copy / majority | 0.0 | 17.6639 | **+17.6639** | PASS |
| 2 self / maj-threshold | 0.0 | 17.6639 | **+17.6639** | PASS |
| 3 self / AND-all       | 0.0 | 30.4872 | **+30.4872** | PASS |
| 4 self / OR-any        | 0.0 |  0.286748 | **+0.286748** | PASS |
| 5 self+fixed / sparse-2 | 0.0 | 11.2999 | **+11.2999** | PASS |
| 6 self-dom / XOR-parity | 0.0 |  2.41094 | **+2.41094** | PASS |

```
  RULES PRESERVING FALSIFIER (ΔΦ>0): 6 / 6
  RESULT: 7 PASS / 0 FAIL   (6 rule-falsifier + 1 determinism)
```

- 6 family **전부** Φ_M1 = 0.0 (국소 self-copy = 완전 가환 = 통합 없음, 부호 안정).
- 6 family **전부** ΔΦ > 0 → falsifier H (bypass > M1) **미반증**.
- 절대 크기는 family 마다 +0.29 ~ +30.49 으로 크게 변동 — **부호는 강건, 크기는 규칙의존**.
- 가장 약한 결합(OR-any, 하나만 켜져도 ON)이 ΔΦ 최소(+0.29), 가장 강한 결합(AND-all)이 최대(+30.49) — irreducibility 강도와 ΔΦ 크기가 단조 대응(질적 일관).

### 등급화 (g5/p7 — hexa verify, perplexity self-judge 금지)

```
tier = 🟢 SUPPORTED-NUMERICAL  (external verifier passed AND stdout matches --expect — delegated, deterministic)
claim = A7 robustness: IIT4 big-Phi(bypass-hub) > big-Phi(M1-local) survives ALL 6 coupling-rule families, n=4 engine-exact
ext rc = 0
```

verdict verbatim 전문 = `.verdicts/a7-coupling-robustness/sweep.txt`.

---

## 3. 해석 (honest interpretation)

**부호 finding 은 규칙변이를 견딘다 (robust, NOT rule-specific).**
A6 의 majority 규칙이 우연이 아닐까 하는 R1 의심은 기각된다 — self-copy/majority,
임계(maj/AND/OR), sparse-XOR, dense-parity 6 family 모두에서 bypass > M1 이 부호 유지.
즉 "노드가 *남*에게 의존하면(투사허브) 국소 self-copy 보다 IIT4 통합도가 높다" 는
*특정 결합규칙의 산물이 아니라* 어떤 cross-coupling 패턴에서나 나타나는 질적 성질이다.

**약화되는 부분 — 크기는 절대 무의미, 규칙마다 한 자릿수~30배 차이.**
ΔΦ 가 +0.29(OR-any)부터 +30.49(AND-all)까지 흔들린다. 이는 "얼마나 더 통합되나"의
정량 주장은 toy 에서 전혀 닫히지 않음을 뜻한다. 주장 가능한 것은 **방향(부호·순서)** 뿐.

**한계 (변하지 않는 carve-out, A6 §4 계승).**
- 🟢 는 *numerical*(엔진 재계산 일치)일 뿐 🔵 *formal*(닫힌형 항등식) 아님.
- n=4 toy, sys=1111 단일 상태. 다른 n·다른 sys_state 격자는 미확인 (A6 R1 의 n=4..6 일부만).
- synthetic TPM — 실제 16ch EEG·실제 N1 transfer 보장 없음 (BRAIN.md M2/M3 실측 필요).
- M1 측을 모든 family 에서 self-copy 로 고정 = 보수적 baseline; M1 측 결합변이는 미탐색.

**결론**: A6 의 핵심 부호 finding(bypass-hub > M1-local 통합도)은 6/6 결합규칙에서 살아남아
**rule-specific 가 아닌 robust** 한 in-silico 성질로 강화된다. 정량 크기 주장은 여전히 닫히지 않음.

---

## 4. 출처 포인터

| 주장 | 출처 |
|---|---|
| A6 단일규칙 falsifier (b) ΔΦ=+17.66 | `AURA/A6-bigphi-closed-loop.md` §4 · `AURA/toy/a6_relocate_bigphi.hexa` |
| R1 잔여 (결합규칙 robustness 미확인) | `AURA/A6-bigphi-closed-loop.md` §5 R1 |
| big_phi 엔진 (n≤8 exact) | `stdlib/consciousness/iit4_bigphi.hexa` `big_phi(tpm,n,sys)` |
| 위치재배치 = 투사허브 = 고결합 | `AURA/SURVEY.md` §2, §3 |
| A7 harness + verdict | `AURA/toy/a7_coupling_sweep.hexa` · `.verdicts/a7-coupling-robustness/sweep.txt` |
