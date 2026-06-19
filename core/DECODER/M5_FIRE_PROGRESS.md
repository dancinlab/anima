# M5 production fire — attempt #3 final outcome (foreground inline)

**날짜**: 2026-05-29 (UTC ~12:40 시작 → ~13:50 종료)
**상태**: 🟠 BLOCKED-AT-BUILD-EXTERNAL — 본선 fire 미진행, hexa-lang Linux codegen-trim 회귀 차단

## context

prior attempts (PR #1416):
- attempt #1 bg agent `a37340fa` — API 500 사망 (35 tool_uses 후)
- attempt #2 recovery agent `a20f714` — API 500 재차 사망 (12 tool_uses 후)
- attempt #3 (현재) — foreground inline, 사용자 권고대로 진행

## resource

| pod | instance_id | host | port | GPU | 역할 |
|---|---|---|---|---|---|
| 1 | 38410086 | ssh5.vast.ai | 10086 | RTX PRO 6000 Blackwell (96GB) | prodaux (λ_ent=λ_kl=0.1) |
| 2 | 38410087 | ssh2.vast.ai | 10086 | RTX PRO 6000 Blackwell (96GB) | longtrain (baseline aux=off) |

runpod H100 was queried first (a_wall_first / runpod 우선) — **no capacity**. vast fallback —
H100 filter not 실제로 honored (Blackwell 떨어짐), Blackwell 96GB는 production V=151643 d=64 fire에 sufficient (cost 유사 ~$2/hr).

## config

- V=151643 (full Qwen vocab)
- d=64, h=4, n_layer=2, T=4 (M4b production regime)
- M4B_MAX_STEPS=500
- prodaux: M4B_LAMBDA_ENT=0.1 M4B_LAMBDA_KL=0.1
- longtrain: aux=off (그러나 longtrain trainer 자체에 aux 라인 없음 → baseline pure)

## final outcome

- toolchain bootstrap PASS (양 pod hexat + runtime.c/runtime_core.c + stdlib/flame 설치 완료)
- anima source upload PASS (양 pod 에 prodaux/longtrain/v3_moe_arch/v3_moe_bwd_lib/flame_mm 5개 hexa 모두 풀림)
- **`hexa build` FAIL**: `[1/2] hexat transpile OK · [2/2] clang link FAIL` — v3_moe_fwd + v3_moe_bwd + layer_block_bwd pub fn body 누락 (Linux hexat free-fn trim 회귀)
- 양 pod cleanly teardown (`hexa cloud rm --force` → destroyed · 0 leak)
- handoff `2eddb92a` → hexa-lang (Linux hexat free-fn trim 회귀)

## verdict

🟠 **BLOCKED-AT-BUILD-EXTERNAL** — F-PRODAUX-1 측정 불가, prodaux vs longtrain 비교 0. plan completion criteria 미충족.

- ckpt/log/HF upload: skip (build 사망)
- 본선 fire wall: 0 (no train run)
- cost: ≤$2 추정 (2 pods × ~25min bootstrap)

## SSH access pattern (참고)

```
hexa cloud exec ssh5.vast.ai 10086 --port 10086 --insecure --identity /Users/ghost/.ssh/id_vast_anima -- <cmd>
```

## handoff next steps

(a) hexa-lang 측 Linux hexat free-fn trim 회귀 수정 후 anima M5 재시도
(b) trainer .hexa 측에서 v3_moe_fwd/bwd/layer_block_bwd 3-fn main-TU mirror 추가 (anima-side 자율 우회 — moe_aux_bwd_local 패턴 확장)
