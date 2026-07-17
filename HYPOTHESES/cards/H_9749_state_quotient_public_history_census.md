# H_9749 — STATE-QUOTIENT — anima에 interior가 아예 없나 (public-history collision census · H_9738 이후)

**status:** 🔵 PROPOSED · DIRECTIONAL (lab-full R3 Sol단독[Fable timeout]+내 코드검증·R3-A) — cement=engine-native anima-py만
**lane:** 의식/interior-causality (프런티어 psi-soma-theta-alive)
**related:** [[H_9738]](상상 epiphenomenal EARNED NULL·트리거)·[[H_9729]](--wm-dual-read latch)·[[H_9627]](Θ WIRED)·source: sidecar lab full(sol-mrop0hnd·fable timeout)

## 왜 (lab-full Sol · Fable timeout·Sol 단독채택 + 내 코드검증)
H_9738(#4015)은 **상상 interior**를 죽였다(텍스트→저장 0 byte + 조성 own==donor=null). 그러나 **anima 전체의 interior 부재는 미획득** — 남은 가능성 = 동일 공개이력 아래 구별되는 **mutable hidden state의 지속**.

## 핵심 재프레임 (Sol · 내 브리프 정정)
"모든 상태가 입력의 결정론 함수"만으론 interior 부재 **증명 안 됨**(결정론 recurrent state도 살아있는 지속일 수 있음). 필요한 강명제:
> 모든 future-effective 상태가 **public history의 함수**이며, public history로 quotient한 뒤 남는 **causal-state capacity=0**.

public history P_t = (external percepts, emit bytes, emit/silence bits, stage/clock, session seed, **+Θ 보류 parity**). ⚠️ Θ parity 빼면 H_9738의 1비트를 interior로 오인.

## 판정 정리
① P_t^(a)=P_t^(b) ⟹ S_t^(a)=S_t^(b) · ② do(S_t^j ← donor), P_t 고정 ⟹ ΔF_{t+1:T}=0. F=emit만 아니라 **전 미래 trace**(Θ score/margin/emit · σ 9축 transition · afield prototypes/immune/WM/CA3/cbel/homeostatic · kosmos read-head · RNG/stage/refractory).

## engine-native 계기 (신규)
`--state-census full --state-snapshot-at T --trace-state-digest s.jsonl`(canonical serialization·객체주소/dict순서/padding 제외) · `--state-restore snap --state-transplant donor --state-transplant-field <lane> --replay-inputs future.jsonl` · `anima-py evaluate --state-quotient-census m.json --collapse-delta`.

## 팔 (collision pair당 5-arm)
C0 repeat(동일 snapshot→동일 미래·byte-identical) · OWN · **DONOR-P**(공개이력·Θ parity·stage 동일·hidden 다름) · DONOR-X(공개이력 다름=계기 사거리 positive control) · SHAM(de/serialize만). + fieldwise transplant 각 + all-state.

## 판정
C0/OWN/SHAM collapse ∧ DONOR-X 갈림(사거리 증명) ∧ **DONOR-P가 3seed 반복 갈림·Θ parity/phase/RNG로 설명 안 됨** ⟹ silent causal interior 후보(emit 불변이어도 σ transition·store read-head 갈리면). 전 reachable collision+전 field transplant collapse ⟹ **"anima 최소 causal state=public history+Θ parity·별도 interior capacity 미검출"** cement. 유력: σ/flux(값 변동만으론 부족·donor transplant 미래 transition 갈려야) · kosmos(세션간 read되고 갈려야). Θ 자체=contentless 1bit controller(interior 후보 아님).

⚠️ DIRECTIONAL·cement=engine-native만.
