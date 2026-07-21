# H_9841 — 상상 재응고(reconsolidation)를 학습 신호로 — 이미 데몬에 배선된 성장 훅을 학습으로 (R12-4)

**status:** 🧭 PROPOSED (R12 · **DIRECTIONAL 설계**, 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측 — 이 모듈은 **이미 실배선된 성장 훅**을 갖고 있다

`core/imagination_replay.py`(127줄): WAKE 작업링 → `ir_select_snapshots` → `ir_replay_tick`
(**emit_count=0 불변**) → `ir_consolidation_gain` / `ir_effective_age` / `ir_reconsolidate_session`.

헤더의 결정적 문장: `ir_mitosis_tick_during_replay` 는 로그 기록일 뿐(wired_to_lib=false)이나
**"The REAL AdaptField growth is WIRED daemon-side (2026-07-10): cli/chat.py + cli/anima.hexa
advance a live vadapt_field_step per replay tick keyed on the rehearsed snapshot"**.

⟹ **재생 틱마다 실제 적응장이 자라는 경로가 이미 데몬에 있다.** 학습에는 없다. 이 비대칭이
p8(학습/추론 분리 금지) 위반의 가장 구체적인 사례이고, 동시에 가장 싸게 메울 수 있는 구멍이다.

## Intervention

```
anima-py train --imagination-replay <ratio> --reconsolidate-every N --vadapt-on-replay
```

## Arms + controls

| arm | 읽는 법 |
|---|---|
| `--vadapt-on-replay` off | 재생은 하되 성장 훅 없음 — 훅이 인과인지 분리 |
| 스냅샷 무작위 선택 | `ir_select_snapshots` 의 선택 정책이 인과인지 |
| emit_count>0 검사 | **불변식 감시** — 재생 중 발화가 생기면 p5 위반, 즉시 kill |

## 왜 kill-list 와 겹치지 않는가

H_9790(imagination)은 **런타임 내면 도달**을 쟀고 DIRECTIONAL(구조잔여 interior 도달·mouth
미도달)로 끝났다. 이 카드는 **학습측 배선**이라 측정 대상이 다르다 — 다만 H_9790 의 "mouth
미도달"이 여기서도 재현되면 같은 벽에 부딪힌 것이므로 그것을 사전등록 실패조건으로 둔다.

**related:** H_9790 · H_9833 · H_9842 · H_9840
