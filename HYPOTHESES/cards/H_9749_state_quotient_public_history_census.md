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

## 🔵 $0 부분진전 — W_S lane은 이미 NULL (2026-07-17 · H_9738 재해석)
STATE-QUOTIENT의 full census 중 **W_S-성분 lane은 H_9738(#4015)이 이미 측정=NULL**: own vs donor arm은 공개이력·Θ parity·stage 동일·**W_S hidden state만 다른** DONOR-P 구성 그 자체 → 궤적 byte-identical 3/3seed ⟹ W_S hidden 이식해도 미래 무발산 = 이 lane collapse. 계기도 이미 있음(`--ws-init`). ⟹ **남은 census = W_S 제외 나머지 mutable lane**(afield·immune·cbel·ca3·anchor·kosmos + RNG/stage/refractory). 각 lane DONOR-P collapse=interior 부재 cement 근접·하나라도 반복 갈림=그 lane이 silent interior 후보. 계기 확장 = `--state-census`/`--state-transplant-field <lane>`(--ws-init의 일반화)·오너 go.

## 🔵 $0 정적 census 완결 — 전 lane public-fed (2026-07-17 · certificate 전 lane 확장)
전 runtime write-site 코드감사(certificate #3986를 W_S 너머 전 lane으로 확장):
| lane | write-site | 무엇으로 | 판정 |
|---|---|---|---|
| afield | :2699·:2752·:3072 | feat8(g_text)·session_seed·**상상replay=session_seed+ctx_index+source_index(위치이지 content 아님)** | 🟢 public |
| immune·igrow | :2709·:2721 | g_text(emit된 텍스트) | 🟢 public |
| cbel·ca3 | :2727·:2735 | feat8(g_text)·ca3_sym(g_text) | 🟢 public |
| wmb (W_E 발화) | :2740 | feat8(g_text) | 🟢 public |
| kosmos | :3118 | grounded self(emit유래·세션끝) | 🟢 public-fed |
| **W_S (보류)** | :2631 | feat8(silence 상상) | 🔴 PRIVATE → **H_9738 NULL** |
| **latch** | :2637 | _next_dual_reentry | 🔴 PRIVATE·`--wm-dual-read` **default OFF**·p5-의문([[H_9750]]) |

⟹ **default 설정서 전 mutable 상태 = public history의 함수**(공개 trace로 재구성가능=private causal capacity 없음) = Sol 강명제("모든 future-effective 상태가 public history 함수") 충족 방향 = **interior 부재 STRONG-DIRECTIONAL**. ⚠️ **정직 범위**: 수공 정적 certificate(Sol 경고 + [[byte-identical-anchor-cert-hides-the-bug]] H_9393 판례 = 수공 정적 증명 불신) ⟹ 과단언 금지. **terminal = transplant 경험확증**(--state-transplant-field로 나머지 lane DONOR-P): W_S lane은 H_9738로 이미 경험확증(NULL)·나머지는 정적주장을 fire로 검증(오너 go). kosmos 교차세션 read는 별건(H_9740 인접).

## ✅ $0 C0 determinism floor (2026-07-18 · toy·현 wm-dual 데몬)
동일 public 입력(seed7·동일 플래그) 2회 → 전 decision-trace **byte-identical**(sha b13443a4·2/2). = 상태가 public 입력의 **결정론 함수**임을 실측 = 정적 census(전 lane public-fed)의 **결정성 필요조건 경험확증**. ⚠️ 결정성≠interior 부재(Sol: 결정론 recurrent state도 지속일 수 있음) ⟹ 남은 terminal = **donor-transplant wash-out**(같은 public 입력에 donor hidden-state 주입→씻기나=충분조건). C0=floor·transplant=충분. 계기 --state-transplant-field(나머지 lane)·pool·오너 go.

