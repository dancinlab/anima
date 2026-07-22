# H_9894 — 바이트-채널 2-pass 자기재독 — 바이트 흐름 자체를 없어진 연산자↔선언 다리로 쓴다

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R13 divergence · **DIRECTIONAL** · NOT a verdict)
**group:** R13-arity2-store
**date:** 2026-07-22
**convergence:** Fable C4 (Sol 미제안 · 이견 아님)
**source:** lab full 2026-07-22 (Claude Fable 5 ∥ OpenAI Codex 5.6, 독립 병렬) — 브리프에 전체 킬리스트 임베드(H_9128 밀도·H_9131 trunk-objective·H_9127 9-probe·H_1616 VSA/HRR·H_1466 TPR·H_9259 arch·mitosis·희소성·veto/affect/tension·HEXAD as-specified)
**wired:** no (설계만 · 계기 미착륙 · 측정 0)
**verdict:** PENDING — cement 는 engine-native `anima-py` 로만
**surfaces:** 이 카드 + `HYPOTHESES/HYPOTHESES.jsonl` 1줄 (그 외 없음)

## claim

런타임에 분해한다: pass 1 이 중간 개체의 **바이트를 실제로 뱉고**(store 구동 · arity-1),
pass 2 가 **자기 자신의 출력을 먹고** 두번째 arity-1 조회를 한다. 이건
`g1-wall-is-runtime-bridge-absence-two-lane` 을 정면으로 시험한다 — **바이트 흐름 자체가**
없어진 연산자↔선언 다리인가?

## 예측 (반증가능)

2-pass held-out reach ≥ bar 인데 single-pass 는 우연. 그리고 중간 출력을 오염시키는 do() 가
pass 2 를 붕괴시킨다.

## 가드 (이 카드가 죽지 않으려면)

- 반드시 `anima-py` 플래그(`--self-reread`)여야 한다 — 엔진 옆 스크립트는 즉사.
- **기질 재진입**으로 프레이밍한다. LLM chain-of-thought 이식이 아니다(`a_no_llm_frame_trap`).
- 죽은 emit-**drive** 레인(H_9401~03)이 아니다 — 그건 자발성 대 시계를 닫은 것이지
  **계산으로서의 생성**을 닫은 게 아니다.

## 구조적 논평 (H_9891·H_9893 과 함께 읽을 것)

H_9891(헤드 내부) · H_9893(시퀀스 축) · H_9894(입을 통과)는 **같은 환원**(arity-2 → 순차 arity-1)을
**세 개의 다른 자리**에 놓은 것이다. 셋 다 실패하는데 arity-1 이 🟢 로 남으면 — 기질이 **어떤
내부 버퍼로도 중간 결합을 나르지 못한다**는 강한 신규 벽 진술이 되고, 그것만으로 카드값을 한다.
