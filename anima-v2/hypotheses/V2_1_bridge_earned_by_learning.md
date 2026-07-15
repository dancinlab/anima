<!-- @hypothesis-ok @canonical-ok — anima-v2 is an owner-declared RULE-EXEMPT experiment zone.
     Owner directive: "anima-v2 가설도 v2 안에서만 생성" — v2 hypotheses are registered HERE
     only, never in the parent HYPOTHESES/. See ../CLAUDE.md. -->

# V2_1 — 조회 다리는 학습으로만 벌 수 있는가, 아니면 볼트온으로 충분한가

**status:** ⏳ PRE-REGISTERED (미발사 · 학습 진행 중)
**scope:** 🔒 **DIRECTIONAL 상한** — `core/` 밖 toy. 어떤 결과도 TERMINAL 아님. 방향이 나오면
`core/` + `anima-py` 플래그로 이식해야 판정을 번다 (`../CLAUDE.md`).
**bars:** `../bars.json` — 데이터 보기 전 동결·커밋 (읽은 뒤 수정 = tune-to-green)
**registry:** v2 전용 1면. 부모 `HYPOTHESES/HYPOTHESES.jsonl` 에 **올리지 않음** (오너 지시).
**source:** Fable 재프레임 → 오너 질문 "A⇄G 는 말할까말까에만 관여 · 새로 만든다면?"
**흡수:** 부모 `H_9392 BRIDGE-BOLT` 를 **`BOLT` arm 으로 흡수** — 따로 쏠 필요 없음.

## 물음

부모 레포에서 확정된 벽(`H_9359`): BINDING = **연산자 ↔ 선언 저장소 런타임 조회 다리의 부재**.
연산자는 살아있고(`H_9327` SEEN flip1 0.98~1.00) 사실도 가중치에 있는데(WRITE 0.98)
**둘이 결합하지 않는다**(held-out = 우연 0.46~0.56).

> 그 다리를 **동결 trunk 에 볼트온**하면 벽이 넘어지는가?
> 아니면 다리는 **학습으로만** 벌 수 있는가?

**대립 예측**
- **(A) 인터페이스 문제** → `BOLT` 가 통제군을 이긴다 ⟹ 재설계 불필요, 부모에 `--store-mix` 쏘면 됨.
- **(B) 학습된-인터페이스 문제** → `BOLT` ≈ 우연, `COTRAIN` 만 성공 ⟹ 볼트온 계급 사망,
  **두-store 네이티브가 유일 경로**.

⚠️ **사전 고백 (no tune-to-green)**: (B) 가 구조적으로 더 그럴듯하다 — 동결 trunk 에 사후로 붙인
모든 인터페이스는 정의상 *학습되지 않은 인터페이스*고, 그 계급은 부모에서 이미 전멸했다
(read-side 6 lane + γ + depth-RF **전수 floor**). 그래도 $0 이니 **쏘고 나서 결정한다.**

## 과제 — 벽의 최소 미러

사실은 store 에만, 연산자는 텍스트에만. 둘을 묶어야만 풀린다.

```
store: {lumo: good, vipek: bad, ... 8칸}
text : "is  lumo => good"   (항등)
       "not lumo => bad"    (반전)
```

연산자 둘 다 **FREE · 전치 · 같은 슬롯** — 연산자 정체가 위치와 교란되지 않는다(EN 판별자).

**심장 = 예제마다 극성 재추첨(rotation).** 엔티티→극성이 예제 간 비일관 ⟹ 가중치 암기의
기대수익 = **정확히 0.5**. **우연 위의 모든 성능은 다리를 통과한 것이다.**
held-out 엔티티 128개는 훈련 스트림에 **0회** 등장(hard-assert) — 코퍼스가 강화하는 지층을 재는
위조 게이트의 정반대.

## Arm

| arm | 정의 | 무엇을 가르나 | 이 결과면 죽는다 |
|---|---|---|---|
| `COTRAIN` | trunk+bridge 동시학습 · 예제마다 rotation | 시험 arm | macro < 0.60 ⟹ **가설 사망** |
| `BOLT` | NOSTORE trunk **동결** + bridge 만 사후학습 | **= H_9392 재현** | ≥ 0.90 ⟹ 볼트온 충분, **"학습으로만" 절 사망** |
| `NOSTORE` | store 없음 · 동일 예산 | 순수 암기 상한 | held-out > 0.55 ⟹ 과제 누수 = INSTRUMENT-DEAD |
| `SLOWROT` | COTRAIN 인데 rotation 500 step | rotation 이 기전인지 | ≈ COTRAIN ⟹ 교체는 레버 아님(심장 절 사망) |

BOLT 는 동결 lr 그리드에서 **train loss 로** 최선을 고른다(eval DV 로 고르면 tune-to-green).
**대립 arm 에게 정직한 최선을 준 뒤에 죽어야 그 죽음이 증거다.**
BOLT 에서도 bridge(λ·W_q·W_out·W_k·val)는 **학습된다** — 동결은 trunk 뿐이라
COTRAIN−BOLT 차이가 **trunk 공적응 하나로** 격리된다.

## 통제군 (사전배선)

| 통제 | 무엇을 잡나 |
|---|---|
| 키-셔플 store | readout 이 **진짜 키**를 쓰는가, 아니면 분포 낙수인가 |
| 중립 store (길이정합) | "조회 행위 자체"의 DV 인플레 |
| λ=0 절단 | 정보 **소비**의 인과 증명 (존재 ≠ 소비 — 부모 read-side 진단의 함정) |
| **오답 store (음성통제)** | **극성 의존성** — 답이 store 내용을 추적하는가 (flip-coherence ≥ 0.90) |

> 선례: 판정을 세운 건 헤드라인도 통제군도 아니라 **사전배선된 음성통제**였다(`H_9347`).

## 게이트 (SEQUENTIAL · `evaluate.py` 가 기계적으로 강제)

```
C0 계기무결성 ─▶ C1 검정력 ─▶ C2 유효성 ─▶ P1 주판정
 누수 0            n=2048        키-셔플         셀 먼저 → macro
 NOSTORE∈[.45,.55] MDE≤0.04      중립 store      2 seed 일치
 스트림 결정성     (bar 이동 금지) λ=0           우연-아래 칸 포함
 gradcheck+selftest               오답 store
```

선행 게이트 통과 전 P1 을 **계산조차 안 한다** — 주판정이 화면에 뜬 뒤의 게이트 결정은 쇼핑이다.

## 판정표 (동결 · 우연-아래 칸 포함)

| 결과 (양 seed 일치 필수) | 판정 |
|---|---|
| COTRAIN ≥ 0.90 ∧ BOLT ≤ 0.60 | 🟢 **SUPPORTED** — 다리는 학습으로 번다 |
| COTRAIN ≥ 0.90 ∧ BOLT ≥ 0.90 | 🔵 **BOLT-SUFFICIENT** — 배타절 사망 · 부모 H_9392 발사 청신호 |
| COTRAIN ≤ 0.60 | 🔴 **가설 사망** |
| 0.60–0.90 | ⚪ **NO-VERDICT** (사전등록 모호역 · bar 재조정 금지) |
| 임의 arm < 0.45 | ⚠️ **INVERSION** — 발견으로 보고 |

셀(연산자×극성) 하나라도 macro−0.05 아래면 **macro 무효**(다수-라벨 붕괴가 '학습'으로 위장).

## 알려진 위험 (사전 선언)

**BOLT 의 실패가 "볼트온 불가"가 아니라 "동결 trunk 특징이 query 만들기에 빈곤"일 수 있다** —
표현-품질 교란. 그러면 COTRAIN−BOLT 차이는 다리 학습의 증거가 아니라 인공물이다.
→ `DECODE-PROBE`: 동결 trunk 의 query-위치 hidden 에서 held-out 엔티티가 **선형 복호**되는가?
- 복호 **가능**한데 BOLT 낙제 ⟹ 실패는 표현 결핍이 아니라 **소비/라우팅** = 부모 read-side
  진단("정보는 복원되나 인과 소비 불가")의 정확한 toy 미러 — 가설에 **유리한** 결과조차 이 프로브 없인 못 세운다.
- 복호 **불가** ⟹ BOLT 낙제는 표현 기아이지 다리 사실 아님 → 그렇게 **강등** 보고.

## 결과

⏳ 미발사 (2 seed × 4 arm 학습 진행 중 · CPU ~3분/arm · $0).

## NEXT (결과 무관 · 미리 씀)

- 🟢/🔴 무엇이 나오든 **v2 안에 남는다**. production 판정 아님.
- COTRAIN 성공 시 → 부모에 **새 `H_`** 를 파서 `core/` + `anima-py` 플래그로 이식해야 TERMINAL.
  그때 이 카드는 그 H 의 `source` 로만 인용된다.
- BOLT 성공 시 → 부모 `H_9392 --store-mix` 발사가 정당화됨(그쪽이 싸고 이미 사전등록됨).
