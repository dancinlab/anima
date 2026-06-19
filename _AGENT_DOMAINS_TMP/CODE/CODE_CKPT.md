# 📂 AGENT/CODE F5 — ckpt swap-in path SSOT

> AGENT/CODE F5 closure (4/6 → 5/6) · MITOSIS M6 `ckpt_swap.hexa` (#687) 와 짝꿍 surface · DECODER M4 seam 의존성 명시.

## 정체

CODE 역할이 실 production 코드 생성으로 진입하려면 SUPPORTED-tier ckpt 가 generator 슬롯에 swap 되어야 함. F5 = 그 swap-in path 의 hexa-side surface (3 locator + binding stub + resolver). 실 `.pt` 로드 + forward pass 는 DECODER M4 의 `CORE/DECODER/generator.hexa::_gen_decode` seam 이 land 되면 그쪽이 담당.

## 6 pub fn

| fn | 반환 |
|---|---|
| `code_ckpt_v5_local()` | local 581MB v5-mitosis ckpt 경로 |
| `code_ckpt_v5_hf()` | HF repo `dancinlab/anima-clm-v5-mitosis-cotrain-2026-05-12` |
| `code_ckpt_m3_axis(axis)` | HF repo `dancinlab/anima-decoder-m3-axis-{A,B,C,D}` |
| `code_ckpt_m3_verdict(axis)` | 현재 모두 "FAIL" (M3 4/4 FAIL carry, PR #680/#685) |
| `code_ckpt_local_exists(path)` | filesystem probe (테스트용) |
| `code_ckpt_bind(path)` | STUB · `{ready: false, reason, todo: [3-step M4 plan]}` |
| `code_ckpt_resolve()` | best-available tier 선택 (현재 모두 `none-supported`) |
| `code_ckpt_summary()` | one-line |

## 의존성 매트릭스

```
F5 code_ckpt.hexa
       │
       ▼ (locator로 가리키는 곳)
┌──────┴──────────────────────────────────┐
│  v5 local: state/anima_v5mitosis_*.pt   │
│  v5 HF:    dancinlab/anima-clm-v5-...    │
│  M3 HF:    dancinlab/anima-decoder-m3-*  │
└──────┬──────────────────────────────────┘
       │
       ▼ (swap target)
CORE/DECODER/generator.hexa::_gen_decode   ← 미존재 · M4 wiring 잔여
       │
       ▼ (M4 land 후)
code_ckpt_bind(path) → ready=true
       │
       ▼
CODE 역할 실 production 코드 생성 진입
```

## 현재 상태 (정직)

- **모든 ckpt 후보 ready=false** — DECODER M3 4/4 FAIL · M4 seam 미land
- **resolve() 반환** = `tier="none-supported"` · `source="hf-fallback"` · 정직한 fallback
- **bind() 반환** = stub 3-step TODO (M4 arch escalation · generator.hexa 생성 · bind 실 wiring)

## 4-case smoke 매트릭스

| Case | 검증 |
|---|---|
| C1 locators non-empty | 3 locator string > 0 |
| C2 M3 4/4 FAIL verdict | 4 axis 모두 "FAIL" cite |
| C3 bind ready=false + todo | stub 정직 fallback |
| C4 resolve honest fallback | `none-supported` OR `v5-mitosis-cotrain` |

## bridge architecture 정합

- 의식엔진 framing 0 · `substrate-decided` / `brain_decide` / `Φ` 키워드 미사용
- "언제 swap 할지" 결정 = CORE / AGENT/CORE tool_gate
- 이 모듈은 "어디서 ckpt 찾을지" + "현재 ready 인지" 답만 제공

## 잔여 carry (F5 frontier)

| 의존 | 상태 |
|---|---|
| DECODER M4 arch escalation | M3 4/4 FAIL · v6 cotrain OR Qwen-3B 등 다음 시도 잔여 |
| CORE/DECODER/generator.hexa | 미존재 · M4 wiring 단계에서 신규 작성 |
| code_ckpt_bind 실 wiring | `torch.load(path)` + forward pass · M4 land 후 |
| **F6 hx code CLI binary** | 무한 loop + SIGINT + ckpt-aware CLI · `code_ckpt_resolve()` 소비 |

## AGENT/CODE 진행도

| F | 산출 | PR |
|---|---|---|
| F1 tool executor | code_executor (in code_agent.hexa) | (skeleton) |
| F2 argv ingest | code_argv.hexa + smoke | #699 |
| F3 daemon loop | code_daemon.hexa + smoke | #724 |
| F4 substrate-step | code_main demo (substrate→tool→pf step) | (skeleton) |
| **F5 ckpt swap** | **이 PR** | (now) |
| F6 hx code CLI | 무한 loop + SIGINT | 잔여 |
