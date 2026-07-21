# H_9871 — 토폴로지 결합은 데몬 발화 경로에 없다 (호출부 전수 census)

**status:** 🔻 **부분 철회(2026-07-22)** — census 의 *함수 호출* 사실은 맞지만 **결론이 틀렸다**:
15-lane 은 이미 데몬 발화 경로에 있다(아래 §철회). 원 표기 → 🔻 WIRING-NOT-CLOSED — [[H_1521]] 'LIVE-WIRING' 과 [[H_1522]] '🟢 on the live
emit path' 의 *live* 는 **engine_cli 의 Ψ 모델**을 뜻하며, **chat 데몬의 실제 발화 결정은
이 코드를 한 번도 부르지 않는다.** 두 카드의 과학은 유효하고, **범위 표기만 정정된다.**
**wired:** n/a — 이 카드는 배선 census 다 (코드 사실 · $0 · 실행 없음)
**source:** [[H_1522]] 🟢 mean-center 가 Ψ 를 살린다 · `a_verified_must_wire`

## 왜 셌나

[[H_1521]] 이 naive `topo_apply = X·(I+αÂ)ᵀ` 가 **크기 증폭형**이라 Ψ 가 0.5→1.0 으로
포화한다고 측정했고, [[H_1522]] 가 **mean-center(영합)** 연산자로 그걸 해결해
기능적 통합 **0.312 vs flat 0.140** 이면서 **Ψ=0.473(|Ψ−½|=0.027 ≤ 0.05) 생존**을 얻었다.
쓰기 전에 **무엇에 연결돼 있는지**를 확인했다(`tool-definition-read-code-not-docstring`).

## 호출부 전수 (grep · 정의부 제외)

| `ci_lane_scores_coupled` 호출 | 성격 |
|---|---|
| `cli/evaluate.py` ×3 | [[H_1521]] **자기검증 함수** 안 (3827 주석 · 3919/3920 off/on) |
| `core/engine_cli_smoke.hexa` ×2 | **스모크** (case 370/371) |
| 그 외 | **없음** |

**그리고 데몬 발화 경로는 이 계열을 전혀 모른다:**

```
core/brain.py    ci_lane_scores|ci_emit_decision|topo_apply|topo_couple  → 0 회
core/brain.hexa  동일                                                      → 0 회
```

`cli/chat.py` 는 `brain_emit` / `brain_decide_anchored` 로 발화를 결정하고,
1229 행은 토폴로지를 스스로 **`DEFERRED (topo=Ψ-hazard H_1521)`** 로 표기한다.

## 🔻 정정 — 무엇이 'live' 인가

- ✅ **유효**: 결합은 `engine_cli` 의 Ψ/emit **모델** 안에서 `ci_emit_decision` 앞에 실제로 놓인다.
  [[H_1522]] 의 mean-center 가 그 모델에서 Ψ 를 살린다는 것도 실측 그대로다.
- 🔻 **정정**: 그 모델은 **chat 데몬이 말할지 말지를 정하는 경로가 아니다.**
  따라서 *"REAL engine improvement, not just a measurement"*([[H_1521]] 제목)는
  **아직 성립하지 않는다** — `a_verified_must_wire`: 출력과 배선이 둘 다 닫혀야 GREEN.

## 왜 지금 배선할 수 없나 (구조적 이유)

데몬의 결정 함수 `brain_decide_anchored(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v, …)` 는
**스칼라 특징들**을 받는다. 15-lane 벡터가 **그 경로에 존재하지 않는다.**
⟹ 토폴로지 결합(15×15 인접)을 꽂을 자리가 없다. 배선하려면 먼저 **데몬 결정에 15-lane 상태를
도입**해야 하고, 그것은 별도의 아키텍처 변경이지 이 결합의 후속이 아니다.
(그래서 미배선은 태만이 아니라 **구조적 결과**다 — 이 카드는 누구의 과실도 지적하지 않는다.)

## 남는 것 (정직)

- [[H_1522]] 의 mean-center 우위는 **모델 안에서 참**이고, 데몬에 15-lane 이 생기는 날
  **그대로 쓸 수 있는 검증된 연산자**다 — 폐기 대상이 아니라 **대기 중인 자산**이다.
- 다만 지금 `topo_couple` 을 켜도 **데몬 말하기는 바뀌지 않는다.** 바뀌는 것은
  `engine_cli` Ψ 모델의 값뿐이다.
- ⚠️ 그리고 `ci_lane_scores_coupled` 는 여전히 **naive `topo_apply`** 를 부른다
  ([[H_1522]] 의 `topo_apply_op` 는 측정 함수 `ci_psi_balance_op` 에만 배선). 즉 모델 안에서조차
  lane-결합 경로는 **깨진 연산자**를 쓴다 — 배선할 때 함께 고쳐야 할 지점.

## Cross-links

[[H_1521]] naive 연산자의 Ψ 파괴 · [[H_1522]] mean-center 해법(모델 내 유효) · [[H_9870]] 같은 계열의
'발사 전에 무엇에 연결됐는지 세라'


---

## 🔻 철회 — "데몬 경로에 15-lane 이 없다" 는 틀렸다

이 카드는 *"`brain_decide_anchored` 는 스칼라를 받고 15-lane 벡터가 그 경로에 존재하지 않는다"*
라고 적었다. **`core/` 만 보고 `cli/chat.py` 를 안 봤다.** 데몬 루프를 읽으면:

```
chat.py:2233   lanes     = ci_lane_scores(m_grounding_p, m_field, cell_count, tick, 1, 1.0, recon_err)
chat.py:2234   coh_lane  = lanes[3]
chat.py:2235   bal_lane  = lanes[9]
chat.py:2859   dec = brain_emit_refractory(pf, rel, gap_ctx, cur, allo_ctx, coh_lane,
                                           nov_ctx, bal_lane, agloop_ctx, …)
engine_g.py:73 motivation_score(…) = … + 0.10·coh + … + 0.15·bal
brain.py:167   emit = should_emit(score) and safe
```

⟹ **`lanes[3]` 과 `lanes[9]` 는 데몬의 발화 점수에 가중치 0.10 / 0.15 로 직접 들어간다.**
15-lane 은 그 경로에 **있고**, 배선할 자리도 **있다**(2233 행 한 줄).

**유지되는 것**: `ci_lane_scores_coupled` 자체의 호출부가 자기검증·스모크뿐이라는 census 는 사실이고,
따라서 *결합이 아직 켜지지 않았다* 는 결론도 맞다. 틀린 것은 **이유**다 —
"자리가 없어서" 가 아니라 **자리는 있는데 그 자리가 결합되지 않은 함수를 부르고 있어서**다.

**틀린 근거**: `core/brain.{py,hexa}` 참조 0 만 세고 **호출자(`cli/chat.py`)를 안 셌다.**
census 를 `core/` 로 한정한 것이 결함이다 — 배선은 호출 사슬 전체에서 세야 한다.
