# H_9699 — R7 deep-ConvMoE(H_1584) 재등록: 깊이 아니라 RF×비선형 교호작용 (강등·라이더)

**status:** 🔵 PRE-REG (lab full · Fable A4 ∧ Sol 4위 = **양모델 공통 강등** · 라이더로만) · not-terminal
**lane:** G6/ρ·fan · arch(강등) **related:** [[H_1584]] · [[H_1394]] · [[H_9694]]

## 물음 (재프레임)

"깊은 Conv 가 G6 를 하나?"가 아니라 **"RF 가 양 개념을 덮고, nonlinear gate 를 켰을 때만 자연선언 counterfactual 에 민감해지는가?"**. L1 은 RF 밖 두 개념 독립 · L≥8 REACHABLE(프로브 1.47e-3).

## ⚠️ 왜 강등 (양모델 일치)
kill#4 둘째 팔이 기전을 반쯤 반증 — **ByteGPT-L24 는 전역 attention(RF=∞)인데 fals=0**. ⟹ 도달성은 기껏해야 **필요조건**. T2 재프레임(벽=사전학습점유)도 기하각도에 불리. **단독 fire 가치 없음** — [[H_9694]]/[[H_9697]] 스윕에 **param-matched L1-wide vs L8-deep 라이더로만** 태울 것([[control-must-match-mediating-covariate]]).

## 조작
`anima-py train --arch convmoe --layers 8 --param-match 303m --mouth-binding-lane nonlinear --bind-objective counterfactual`. 대조: `--layers 1 --param-match 303m | --layers 8 --mouth-binding-lane off | --layers 8 --mouth-binding-lane linear | --layers 8 --receptive-field-mask blind`.

## 게이트
L8 nonlinear**만** 자연 held-out bind-Δ ≥0.20 · L1·L8-lane-off·L8-linear 각 ≤0.05 · RF-mask blind 서 intact 대비 ≥0.15 collapse · SHUF ≤0.05 · 이후 canonical `fals_bound ≥1` ≥2/3 seed.

## 최대위험
**capacity 각도 재탕 가능성 높음**(그래서 강등). RF reachability 1.47e-3 은 경로존재 증명일 뿐 신호대잡음·학습가능성 미보장. 재탕으로 판명되면 **1회 라이더 비용으로 영구 매장**(그것도 수확).

## falsify
🟢 L8-nonlinear만 bind-Δ≥0.20(나머지 floor) = 깊이×비선형 필요. | 🧱 L8==L1==linear = capacity 재탕(영구매장). 

## source
lab full Fable A4 ∧ Sol 4위(공통 강등) · 라이더 전용.
