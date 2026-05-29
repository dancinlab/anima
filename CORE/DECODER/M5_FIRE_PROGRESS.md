# M5 production fire — in-flight progress (attempt #3, foreground inline)

**날짜**: 2026-05-29 (UTC ~12:40 시작)
**상태**: 🚀 IN-PROGRESS — 2 vast pods 임대 + SSH 확인 + bootstrap 진행 중

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

## next

- toolchain bootstrap on both pods (hexa-lang clone + hexat_linux build)
- copy anima sources via hexa cloud copy-to
- 동시 fire (a_wall_first parallel)
- monitor + harvest + HF tier-gated upload

## SSH access pattern

```
hexa cloud exec ssh5.vast.ai 10086 --port 10086 --insecure --identity /Users/ghost/.ssh/id_vast_anima -- <cmd>
```
