# H_9544 — Commons depletion tension (sol R2-E09 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R2 · 사전등록 · 양쪽 DEPLETED 라운드) — source=sol
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·effective rank 2.66 $0 확증=발산 기반) · [[H_9468]] (PCA-DOF rank 2) · [[H_9424]] (cb-perr KILL) · source: lab full R2 sol(R2-E09)

## 제안 (sol 원문 · R2 · 3 미채굴 광맥[자료형·다개체·p8경계])

### R2-E09 — Commons depletion tension

- 유도: 여러 anima가 공유하는 것은 token budget이 아니라 제한된 structural degrees of freedom—relation slot, provenance depth, update-rule diversity다. tension은 개인 값이 아니라 commons의 marginal depletion curve다.
- 최소 실험: `--tension-commons --peers 6 --relation-slots 64`; first-come, equal quota, endogenous marginal-cost 세 arm. 발화량은 gate로 쓰지 않는다.
- 위험: 예산·시장 재포장 경계. 계산자원 예산이 아니라 구조 자유도의 공유재라는 점이 차이. quota는 p2.
- Ψ: 한 개체가 slot을 얻을 확률이 아니라 A/G 양 방향 구조변이가 commons에 주는 한계비용이 같을 때 ½.

## 광맥 3 — p8 경계가 명시된 런타임 가소성

먼저 경계선을 공식화한다.

런타임 변이 \(m_t:S_t\to S_{t+1}\)가 p8-compatible이려면 다음을 모두 만족해야 한다.

1. **동일 연산자**: train/evaluate/chat 어디서든 같은 \(m_t\) 코드 경로.
2. **현재 인과성**: 현재·과거 A/G state만 사용; 정답·미래 token·offline corpus 통계 금지.
3. **가역 증거**: mutation마다 inverse 또는 tombstone과 provenance witness 존재.
4. **파라미터 비창조**: 새 실수 weight를 최적화해 삽입하지 않음. 기존 cell state의 복제·분할·재배선·유한 update-rule 선택만 허용.
5. **반사실 필요성**: A 또는 G를 clamp하면 mutation이 달라져야 한다. 단순 clock growth 금지.
6. **연속성**: mutation 이전 state가 새 구조의 초기조건으로 보존된다.
7. **판정 독립성**: mutation의 생존 여부를 perplexity나 정답 loss가 결정하지 않는다.
8. **표면 비침투**: mouth/candidate byte feature를 mutation trigger로 쓰지 않는다.

이를 **Causal Reversible Structural Continuity, CRSC** 경계라 부른다.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 판정. monitor-only 1단계로 게이트 벽 회피. R2 는 양쪽 모델 DEPLETED 선언 라운드(고갈).
