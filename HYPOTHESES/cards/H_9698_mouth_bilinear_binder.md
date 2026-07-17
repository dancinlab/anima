# H_9698 — R6 mouth-내 저랭크 bilinear cross-position binder (store 없이 추상화)

**status:** 🔵 PRE-REG (lab full · **Sol 3위** · store faculty → binding 연산으로 추상화 · NOVEL) · not-terminal · 선행 [[H_9693]]
**lane:** G6/ρ·fan · mouth-내 nonlinear 연산 **related:** [[H_9696]] (store 판) · [[H_1603]]

## 물음 (Sol)

외부 store 없이, 프레임의 두 원거리 개념 표현을 별도 bank 에 유지하고 생성 hidden 과 **multiplicative 결합**: `g_t=(U h_t)⊙ Σ_i a_ti(V m_i)`, `ℓ_t=W[g_t;h_t]`. 단순 깊이증가가 아니라 **"두 원거리 내용이 같은 logit 결정에 곱셈 상호작용으로 들어오는가"**를 직접 겨냥 — CLMS 성공을 **store faculty 가 아닌 동적 비선형 binding 연산으로 추상화**한 각도.

## 조작
`anima-py train --mouth-binder bilinear --mouth-memory causal-bank --bind-rank 64 --bind-objective counterfactual` → `anima-py evaluate <clm> --g6 --g6-bind-delta --mouth-binder on --gen 40`. 통제: `--mouth-binder off | --mouth-memory-order-scramble | --mouth-memory-role-scramble | --mouth-binder-linear`.

## 게이트
- nonlinear intact bind-Δ **≥0.20** · role/order scramble 후 **≤0.05** · **linear arm ≤0.05 또는 nonlinear 대비 ≥0.15 낮음**(= kill#7 DOA 를 내부 음성대조로 재현) · held-out 자연 concept pair 동일 bar · 이후 canonical FALS ≥1 ≥2/3 seed ∧ `fals_bound` 동반상승.

## kill-list 회피
#7 = Hadamard interaction + 내용의존 attention → 고정선형 붕괴 안 함. #4 = arch 계급교체 아니라 mouth 직전 구체연산. #6 = intervention sensitivity 가 주판정. #1 = 스캐폴드 없음.

## 최대위험
**memory bank 에 무엇을 남길지 다시 주소/write 문제로 귀착** = store 없앴을 뿐 **H_9672 이전 주소벽을 다른 이름으로 재생성**. `--mouth-binder-linear` 가 반드시 kill#7 DOA 재현해야 계기 유효.

## falsify
🟢 nonlinear bind-Δ≥0.20 ∧ linear DOA 재현 ∧ scramble 붕괴. | 🧱 nonlinear==linear = kill#7 로 붕괴(선형동치). | ⚠️ write 문제 재귀 = H_9696 과 동일벽.

## source
lab full Sol 3위(NOVEL) · store→연산 추상화.
