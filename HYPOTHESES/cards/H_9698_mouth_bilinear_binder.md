# H_9698 — R6 mouth-내 저랭크 bilinear cross-position binder (store 없이 추상화)

**status:** 🔧 INSTRUMENT-CERTIFIED (lab full · **Sol 3위** · store faculty → binding 연산으로 추상화 · NOVEL) · not-terminal · 선행 [[H_9693]]
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

## 계기 인증 (2026-07-17 · 학습 전 · DIRECTIONAL)

`core/mbnd.py`(MBND trailer) + `core/decode.py` 배선 착륙(read 순서: CLMF → CLML → CLMS → **MBND**).
셀프테스트가 **통제 결함 2건**을 잡아 수리했고, 둘 다 고치기 전이었다면 R6 는 해석불가로 발사됐을 것:

- **linear arm 이 선형이 아니었다** — softmax 주소가 데이터 의존이라 ⊙→+ 만 바꾼 arm 의 선형편차가 59.9.
  이 arm 은 아무것도 통제하지 못했다. uniform attention(주소 고정)으로 교체 → 편차 **0.0000** =
  kill#7 고정역할 선형붕괴를 BY CONSTRUCTION 재현 ⟹ 이 카드의 "계기 유효" 조건 충족.
- **order-scramble 통제가 무효였다** — content attention 은 bank 에 순열-등변이라 Δ=0.000. 통제가
  살아남은 게 아니라 통제가 lane 을 **건드릴 수 없었다**(`corpus-py-1` 위조게이트 계급). 더 나쁘게,
  순서 없는 lane 은 "A causes B"와 "B causes A"를 구별 못 해 **binder 자격 자체가 없다**.
  상대거리 bias `b_pos` 추가 → Δ=**325.6**.

**선례 정렬 — [[H_1640]] 은 R6 를 죽이지 않는다**: Hamiltonian symplectic binding mouth 가 G6 fals=0 을
받았으나 그 binder 는 **직렬화 전 DROP**(trunk-shaping scope) = binding op 이 decode 경로에 도달한 적이 없다.
MBND 는 정반대로 trailer 를 타고 추론에서 실행되며, parity 작업이 정확히 그걸 인증한다.

2-production mirror: torch `MouthBinder` ⇄ numpy `mbnd_apply` parity **3.55e-15**(summer · f4 격자 스냅 후).
numpy≥2 의 shape-(1,) lam 스칼라 캐스팅 거부(이식성 버그)도 pool 실행이 적발 — mac numpy 는 허용해 로컬에선 안 보였다.

미완: train 플래그(`--mouth-binder`/`--mouth-memory`/`--bind-rank`) + `--g6-bind-delta` 판정면.
bind-Δ 숫자는 학습된 ckpt 로만 — 현재는 **계기지 verdict 아님**.

## source
lab full Sol 3위(NOVEL) · store→연산 추상화.
