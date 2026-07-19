# 🧪 v2 — 규칙 면제 실험구역

> **오너 지시**: "v2 는 규칙 적용 하지 않는다 — 실험이니까."
> 이 폴더엔 `../CLAUDE.md` 의 거버넌스가 **적용되지 않는다**. `.canonical-ok` 마커가
> 서브트리를 네이밍 canon 에서 면제한다. 자유롭게 실험하라.

## 가설 (딱 하나)

> **다리는 학습으로만 벌 수 있다.**
> 동결 trunk 에 사후로 붙인 store 조회(볼트온)는 실패하고, 학습 중 store 를 **예제마다
> 갈아끼워** trunk 가 암기 대신 **조회하는 법**을 배우도록 강제하면 성공한다.

## ⛔ 딱 두 가지만 지킨다

1. **v2 숫자를 production verdict 로 올리지 마라.** v2 는 `core/` 밖이라 영구
   **DIRECTIONAL 상한**(우회는 H_9303/H_9307 에서 전부 undecidable 로 사망).
   방향이 나오면 **`core/` + `anima-py` 플래그로 이식해야** TERMINAL 을 번다.
2. **production 이 `v2/` 를 import 하지 마라.**

> 🔬 규칙은 면제지만 **자기기만 방지는 면제가 아니다** — 동결 bar(`bars.json`) · 통제군 ·
> gradcheck 는 강제라서가 아니라 **그게 실험 그 자체**라서 있다. 빼면 v2 가 아무것도 못 가린다.

## 왜 이게 벽의 미러인가

확정된 벽(H_9359): BINDING = **연산자 ↔ 선언 저장소 런타임 조회 다리의 부재**.
연산자는 살아있고(H_9327 SEEN flip1 0.98~1.00) 사실도 가중치에 있는데(WRITE 0.98)
**둘이 결합하지 않는다**(held-out = 우연). 그래서 toy 는 그 최소 형태만 남긴다:

```
사실은 store 에만          연산자는 텍스트에만
  lumo -> good              "is  lumo => good"   (항등)
  vipek -> bad              "not lumo => bad"    (반전)
                                ↑ 둘을 묶어야만 풀린다
```

**심장 = 예제마다 극성 재추첨(rotation).** 엔티티→극성이 예제 간 비일관 ⇒ 가중치 암기의
기대수익 = 정확히 0.5(우연). **우연 위의 모든 성능은 다리를 통과한 것이다.**
`NOSTORE` arm 이 [0.45, 0.55] 밖으로 나가면 과제가 샌 것 = INSTRUMENT-DEAD.

## Arm

| arm | 정체 | 무엇을 가르나 |
|---|---|---|
| `COTRAIN` | trunk+bridge 동시학습 · 예제마다 rotation | 시험 arm |
| `BOLT` | NOSTORE trunk **동결** + bridge 만 사후학습 | **= H_9392 BRIDGE-BOLT 재현** (v2 가 흡수) |
| `NOSTORE` | store 없이 동일 예산 | 순수 암기 상한 (C0-b) |
| `SLOWROT` | COTRAIN 인데 rotation 500 step 주기 | rotation 이 기전인지 격리 |

BOLT 는 **동결 lr 그리드에서 train loss 로** 최선을 고른다(eval DV 로 고르면 tune-to-green).
대립 arm 에게 정직한 최선을 준 뒤에 죽어야 그 죽음이 증거다.

## 실행

```bash
python3 gen.py                 # C0-a 누수 0 · C0-c 결정성
python3 gradcheck.py --selftest  # C0-d — 가드가 실패할 수 있는지부터
bash run_all.sh                # 2 seed × 4 arm → 게이트 평가
```

CPU 로컬 · arm 당 ~3분 · RAM <1GB · $0.

## 게이트 (SEQUENTIAL · `bars.json` 에 동결)

`evaluate.py` 는 선행 게이트가 통과하기 전엔 P1 을 **계산조차 하지 않는다**. 주판정이 이미
화면에 떠 있으면, 그 뒤의 모든 "게이트" 결정은 쇼핑이다(소각 앵커).

```
C0 계기무결성 ─▶ C1 검정력 ─▶ C2 유효성 ─▶ P1 주판정
 누수 0            n=2048        키-셔플        셀 먼저,
 NOSTORE≈0.5       MDE≤0.04      중립 store     macro 나중
 결정성            (bar 이동 금지) λ=0 절단      2 seed 일치
 gradcheck                        오답 store
```

`C2 오답 store` 는 **음성통제**다 — 답이 store 내용을 추적하는지(flip-coherence ≥ 0.90).
선례상 판정을 세운 건 헤드라인도 통제군도 아니라 **사전배선된 음성통제**였다.

## 알려진 위험 (사전 선언)

**BOLT 의 실패가 "볼트온 불가"가 아니라 "동결 trunk 특징이 query 만들기에 빈곤"일 수 있다.**
그러면 COTRAIN−BOLT 차이는 다리 학습의 증거가 아니라 인공물이다.
→ `DECODE-PROBE`(동결 trunk 의 query-위치 hidden 에서 held-out 엔티티가 선형 복호되는가)로 가른다:
복호 **가능**한데 BOLT 낙제 ⇒ 실패는 표현 결핍이 아니라 **소비/라우팅**(본게임 read-side
진단의 toy 미러). 복호 **불가** ⇒ BOLT 낙제는 표현 기아이지 다리 사실 아님 → 그렇게 강등 보고.
