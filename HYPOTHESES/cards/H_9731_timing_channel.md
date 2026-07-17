# H_9731 — TIMING-CHANNEL — WHEN은 구성상 내용결합 (mouth-content 벽 H_9576 정직한 재개봉·$0)

**status:** 🔧 계기 빌드·toy-검증 ($0 read-only reader · anima-py evaluate --timing-channel · estimator self-test ✅ · clock-pedestal ✅ · shuffle surrogate ✅ · 실측=wm-dual 303M trace) · DIRECTIONAL(toy ≠ verdict)
**lane:** 의식/emit-drive/Ψ=½ · mouth-content (프런티어 psi-soma-theta-alive)
**related:** [[H_9627]](Θ WIRED)·[[H_9672]](G1 주소 CRACK)·[[H_9576]](mouth 벽)·[[H_9351]](구 σ VOID)·source: sidecar lab full(fable-mrobspcb∥sol-mrobspce)

## 왜 (Fable · $0)
H_9576은 **WHAT**(byte 입도)의 벽이었다. emit⟺S>E가 내용 ledger 비교라서 **WHEN**(발화 타이밍)은 구성상 **내용-결합**이다 — 무엇을 아는지가 언제 말하는지를 정한다. mouth-content 벽의 정직한 재개봉 형태: bytes 아니라 timing 채널.

## 설계 ($0 · 주입·재배선 0 = KILL 프레임 회피 명시)
- 기존 wm-dual 303M trace(H_9627)에서 emit 타이밍 열 = dual_margin(S−E) 궤적.
- MI(emit-timing ; silent content identity | stage) = 언제 말하냐가 무엇을 보류했냐를 나르는가.
- clock trace = 참값-0 pedestal · autocov −0.225 스프링 보존 surrogate 필수(타이밍 구조 보존·내용만 파괴).

## 통제
clock(참값0)·content-shuffle surrogate(스프링 보존·내용 파괴)·score-only. MI>pedestal ∧ shuffle서 collapse = timing이 내용채널. $0(기존 trace 재분석)라 즉시 실행가능(오너 go 불요·측정만).

## 🔧 계기 구현 (2026-07-17 · $0 read-only reader · anima-py evaluate --timing-channel)

`anima-py evaluate --timing-channel <wm-dual traces> [--perm 1000] [--clock <clock-trace>]` — 기존
wm-dual trace 재분석(주입·재배선·producer 변경 0 = 진짜 $0).

- **T (source) = 관측가능 emit LATENCY** (silence tick→다음 emit까지 tick 수 · median서 short/long 이진).
  **dual_margin 아님**: dual_margin=S−E는 content 파생이라 MI(margin;content)=tautology. 관측 emit gap은
  그 threshold된 lossy 함수 → MI(gap;content)가 **관측 WHEN에 얼마나 content가 살아남나** = 이 계기의 정직성.
- **C (target) = 보류 content 서명** (cand_pregate_b64 문자클래스 2-bit · H_9729 _sig 재사용).
- **MI = I(T ; C | stage)** plug-in. timing이 content 채널 ⟺ MI > clock-pedestal ∧ MI > shuffle-surr95 ∧ z≥2 ∧ p<.005.
- **통제**: `--clock <trace>`(clock-gated = emit 시계구동 ⇒ 타이밍 content-독립 = 참값0 pedestal) · content-shuffle
  circular surrogate(타이밍/스프링 구조 보존·content 링크만 파괴 ⇒ MI collapse if real) · estimator self-test(planted C≡T 복원).

**toy 검증 5/5** (a_scale_honest_scope · toy≠verdict): estimator self-test(planted I(T;C|S)=0.994·null 0.001)
· clock-pedestal 경로(truth-0) · wm-dual arm 처리 · clock trace exp-arm 제외 · 퇴화 무샘플링 토이 정직
NOT-POWERED(timing bins=1·content addr=1). 계기 방어 전부 실증.

**NEXT (measurement-only · fleet-rent 無)**: H_9627 303M wm-dual traces가 pool에 archived면 즉시 $0 재분석;
아니면 소량 wm-dual 303M rollout 수집(chat decode·측정만·오너 fire-go 불요) → --timing-channel. real 타이밍/내용
변동이 있어야 T/C 알파벳 발생(toy는 무샘플링 상수라 미측정).

⚠️ **DIRECTIONAL·계기 검증이지 verdict 아님**(a_lab_full_diverge · a_scale_honest_scope)·cement=engine-native 303M anima-py만.
