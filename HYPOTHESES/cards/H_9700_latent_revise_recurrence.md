# H_9700 — R8 latent revise recurrence: 출력 후보선택 없는 내부 반증-수정 루프

**status:** 🔵 PRE-REG (lab full · **Sol 5위** · NOVEL · best-of-K 없는 self-revision) · not-terminal · 선행 [[H_9693]]
**lane:** G6/ρ·fan · mouth-내 recurrence **related:** [[H_9696]] · [[H_9698]]

## 물음 (Sol)

single-pass hidden 이 만든 초안 상태를 내부 critic state 가 읽고, **입력 관계와 출력 상태의 불일치**를 다시 trunk 에 주입. 외부 문장 여러 개 생성해 고르는 게 아니라(=kill#1), **토큰당 고정 횟수의 latent recurrence 를 거쳐 한 번만 방출**.

## 조작
`anima-py train --mouth-recur 2 --recur-objective relation-consistency --bind-objective counterfactual` → `anima-py evaluate <clm> --g6 --g6-bind-delta --mouth-recur 2 --gen 40`. 통제: `--mouth-recur 0 | --recur-feedback-scramble`.

## kill-list 회피
#1 = 후보생성·best-of-N·외부 verifier 없음(토큰당 고정 latent 루프). #6 = **detector predicate 를 critic target 으로 쓰면 즉시 사망** → target 은 관계 counterfactual consistency. #7 = state-dependent recurrent update = 선형 readout 동치 아님. #8 = recurrence on/off + feedback scramble collapse 가 주 DV. gen=40 유지.

## 게이트
recur on vs off bind-Δ ≥0.20 · feedback-scramble 붕괴 ≤0.05 · canonical fals_bound ≥1 ≥2/3 seed.

## 최대위험
recur-objective 가 **detector 형태를 target 으로 새면 즉시 kill#6 사망**(반드시 관계 consistency target). recurrence 가 단순 depth 증가로 퇴화(=capacity).

## falsify
🟢 recur-on bind-Δ≥0.20 ∧ off floor ∧ scramble 붕괴. | 🧱 on==off = recurrence 무효. | ⚠️ target 이 detector-form = 위조.

## source
lab full Sol 5위(NOVEL) · self-revision without best-of-K.
