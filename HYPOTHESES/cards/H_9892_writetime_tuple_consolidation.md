# H_9892 — 쓰기측 결합 — 라벨-블라인드 tuple 형성/consolidation join (읽기 전에 이미 묶어둔다)

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R13 divergence · **DIRECTIONAL** · NOT a verdict)
**group:** R13-arity2-store
**date:** 2026-07-22
**convergence:** 🔀🔑 Fable C2 ≡ Sol C3 **독립수렴**(Sol 판이 더 엄격: writer 가 연산자·정답을 못 본다)
**source:** lab full 2026-07-22 (Claude Fable 5 ∥ OpenAI Codex 5.6, 독립 병렬) — 브리프에 전체 킬리스트 임베드(H_9128 밀도·H_9131 trunk-objective·H_9127 9-probe·H_1616 VSA/HRR·H_1466 TPR·H_9259 arch·mitosis·희소성·veto/affect/tension·HEXAD as-specified)
**wired:** no (설계만 · 계기 미착륙 · 측정 0)
**verdict:** PENDING — cement 는 engine-native `anima-py` 로만
**surfaces:** 이 카드 + `HYPOTHESES/HYPOTHESES.jsonl` 1줄 (그 외 없음)

## claim

결합을 **읽을 때**가 아니라 **쓸 때** 한다. 주입 시점에 학습된 M writer 가 두 개체 이름을 키로
하고 두 원시 값을 담은 **쌍 레코드**를 만든다. writer 는 **연산자도 정답도 보지 않는다**(그래서
정답을 미리 계산할 수 없다). 이후 D 는 arity-1 조회 한 번만 하면 된다.
Fable 판(consolidation join)은 오프라인에서 store 행들을 훑어 개체를 공유하는 곳마다 파생
(A,C) 행을 쓴다 — anima 의 기존 5단계 sleep 에 얹히는 생물학적 형태.

## 예측 (반증가능)

벽이 **동시 읽기 fan-in** 이면 쓰기측 tuple 형성이 held-out 을 구제한다. 벽이 **하류 결합 자체**면
tuple 팔과 atomic-store 팔이 **둘 다** 실패한다. 쌍-키 derangement 와 구성값 순열은 붕괴해야 한다.

## 왜 킬리스트가 아닌가

킬리스트의 어느 항목도 **쓰기 시점 합성**을 건드리지 않는다. 새 trunk 기울기도 필요 없다
(serialize/chat 플래그로 엔진 네이티브).
