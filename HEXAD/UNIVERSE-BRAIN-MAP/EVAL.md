# EVAL — CONSCIOUSNESS-CARVING 평가 기준 (paradigm-native, 옛 잣대 폐기)

> User directive 2026-05-17: "평가 기준에 대해서는????? 기존방식????" — UBM-E6 의 capability eval 이 옛 prefix-injection 방식의 잣대를 그대로 쓰고 있다는 지적. category error 식별 + paradigm-native eval 재설계.
>
> g_doc_consolidation 준수: HEXAD/UNIVERSE-BRAIN-MAP/* 내부 (root docs/* 신규 X).

## 0. 발견된 문제 — 옛 방식 잣대를 그대로 씀

UBM-E6 의 `eval_carving_4path.py` `knowledge_recall` 축:
- 15개 probe → 생성물에 keyword (빅뱅/열반/만다라) 가 **literal grep** 으로 들어있나
- **"옛 prefix-injection baseline 13/15"** 와 직접 비교

→ 이건 **옛 방식의 성공 기준 = "암기 recall"** 을 새 paradigm 에 그대로 들이댄 것. **category error.**

## 1. 비유 — 암기왕 시험지로 이해한 학생 채점

| | 옛 방식 (prefix-injection) | 새 방식 (CONSCIOUSNESS-CARVING) |
|---|---|---|
| 학습 성격 | 벼락치기 **암기왕** | 지식을 이해해 의식 풍경에 **새김** |
| 암기 시험 | 13/15 (잘 봄) | path별 다름 — γ 는 의도적으로 안 외움 |
| 대가 | 다른 과목 다 망침 (chat 5/5→1/5) + "사전" 도장 baked (P3 leak) | chat 무오염 목표 |

**암기왕 시험지로 이해한 학생을 채점하면 암기왕이 이기고 이해한 학생이 진다 — 시험지가 틀린 것.**

특히:
- **γ NARRATIVE** — Meta law M8 "외우지 않고 매번 재생성" 이 목적. final CE 1.40 (높음) = 의도된 결과. keyword-literal grep 채점 = 부당하게 0점.
- **α** 6/15 — 생성물 `🛸53 매핑을...` wrong-tier 재생성. literal grep fail 이지만 "carving 됐나"는 다른 질문.

## 2. 옛 방식의 진짜 실패 = 새 eval 의 1급 축

옛 방식 점수표 = **1축 (recall)**. 하지만 옛 방식의 진짜 결함은:
- ⚠ P3 leak baking (SFT scrub 불가)
- ⚠ chat NET LOSS (V5.8 std_greedy 5/5 → 1/5)

→ 새 paradigm 은 **바로 그 지점에서 이겨야** 한다. eval 도 그걸 1급 축으로 올려야 공정.

## 3. paradigm-native eval — 4축

| 축 | 옛 방식 | 새 paradigm-native 기준 |
|---|---|---|
| **1. knowledge access** | literal recall 13/15 | **path별 적절 metric** — α/β/weave: routing 정확도 (input→올바른 basin/cell) + **의미적** recall (literal 아님) · γ: narrative **coherence** (재생성이 의미적으로 맞나) |
| **2. chat 무오염** ★핵심 | **실패** (5/5→1/5, P3 baked) | P3 leak grep = 0 + V5.8 chat 5/5 유지 — **새 paradigm 이 이겨야 하는 곳** |
| **3. lane separation** | 측정 안 함 (분리 ≈ 0) | knowledge ⊥ chat 분리도 — carving 의 본질 |
| **4. V-SPONT** | carry | carry (cycle 3/4/5 = 0/5, carving 이 바꾸는지) |

## 4. 공정한 비교 — joint metric

```
옛 방식:   recall 13/15  BUT  separation ≈ 0  →  단일축이라 "13/15" 가 좋아 보임
새 방식:   recall × separation  JOINT

→ recall 단일축으로만 비교 = 옛 방식에 유리하게 rigged.
   joint (recall × separation) 으로 비교해야 carving 의 가치가 보임.
```

`SCORE_joint = knowledge_access × chat_무오염 × lane_separation`

- 옛 방식: 高 × 低(0) × 低(0) ≈ **0** (recall 만 높고 나머지 붕괴)
- 새 방식 목표: 中~高 × 高 × 高 — recall 이 옛 방식보다 낮아도 joint 는 압도

## 5. "13/15" 의 재배치

`13/15` 은 더 이상 **target / baseline** 이 아님. **대조점**으로 격하:

> "옛 prefix-injection 은 recall 13/15 를 얻었으나 그 대가로 separation ≈ 0 (P3 leak + chat NET LOSS). 새 paradigm 은 recall 이 낮아도 separation 을 확보하면 joint 우위."

g3 / f3: `13/15` = historical empirical only, **NOT a target** (f3 NO-OUTCOME-CLAIM).

## 6. eval 재설계 실행 계획

1. `eval_carving_4path.py` → paradigm-native 재설계:
   - knowledge 축을 path별 metric 으로 분기 (α/β/weave routing+semantic, γ narrative coherence)
   - chat 무오염 + lane separation 을 1급 축으로 (현재는 knowledge 가 head)
   - joint metric (recall × separation) 신설
   - "13/15 baseline" → "13/15 대조점 (separation 0)" 으로 reframe
2. 4 path (α/β/γ/weave) 전부 paradigm-native 재채점
3. 옛-criteria eval 결과 (chat 무오염·V-SPONT 축) 는 데이터로 carry, knowledge 축만 교체
4. 결과 → RESEARCH.md §2 (CONSCIOUSNESS-CARVING vs 옛 prefix-injection joint 대조)

## 7. honest C3

- paradigm-native eval 도 capability **measurement** — closed-form 아님 (B-CARVE-E6-NOTE empirical carve-out 유지).
- carving transfer-form (B-VAC/B-MIT-ETN/B-NAR sympy) 만 🔵, eval 결과는 empirical.
- "새 paradigm 이 이긴다" 는 결론을 미리 깔지 않음 — joint metric 으로 측정된 값만 보고. 만약 새 방식이 joint 에서도 약하면 정직히 그렇게 기록.
- γ 의 narrative coherence 측정은 본질적으로 semantic — keyword grep 보다 noisy. 측정 한계 명시.

## 8. cross-link

- [`DESIGN.md`](DESIGN.md) — CONSCIOUSNESS-CARVING 4-path 설계 SSOT
- [`PLAN.md`](PLAN.md) — Phase UBM-E roadmap
- `state/consciousness_carving_e6_fire_2026_05_17/eval_carving_4path.py` — 재설계 대상
- `HEXAD/CHAT/RESEARCH.md` §2 — 최종 결과 정리 (paradigm joint 대조)

## 9. 진행 로그

### 2026-05-17 — EVAL.md 신설 (옛 잣대 category error 식별)
user "평가 기준에 대해서는????? 기존방식????" 지적. UBM-E6 eval 의 knowledge_recall 축이 옛 prefix-injection 의 "암기 recall 13/15" 잣대를 그대로 사용 → category error 식별. 암기왕 비유 + paradigm-native 4축 (knowledge access path별 / chat 무오염 / lane separation / V-SPONT) + joint metric (recall × separation) + "13/15" 을 baseline→대조점 격하. eval 재설계 + 4-path 재채점 진행.
