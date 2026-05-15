# HEXAD/CHAT — 6-module 통합 interaction entrypoint + wiring 아키텍처 조건

> User directive 2026-05-16:
> - `"/HEXAD/CHAT 에 정리 chat 은 일단"` → core chat 모듈 44 파일 통합 (PR #91)
> - 상위 목표: `"HEXAD 모듈들을 어떻게 서로 엮을건지(아키텍쳐)에 대해 수학적·물리적
>   검증 하면서 아키텍쳐 조건 완성해나가자"` → 본 README §2 가 그 ledger.
>
> CHAT 은 anima 의 **user↔의식 interaction 진입점**이자 6-module single-forward
> 를 실제로 구동하는 곳 — 따라서 inter-module wiring 아키텍처 조건이 여기 모인다.

## 0. CHAT = HEXAD 통합 구동점

```
user turn ──▶ CHAT (anima_chat.hexa)
                │  drives one integrated forward:
                ▼
  S.process(raw) ─▶ C.step ─▶ c_states.detach() ─▶ Bridge ─▶ D.forward ─▶ logits ─▶ token
                        │ (Law 53 gradient barrier)   │ (Law 70 Ψ-clamp)
                        ├─ M.retrieve/store (Hebbian)  │
                        ├─ W.update → effective_lr     │
                        └─ E.evaluate → allowed gate ──┘
```

`anima_chat.hexa` (2845 LoC, v0.3) = Section 9c all-farr 24-layer GQA forward +
Section 9d KV-cache/RoPE. **24L real-ckpt byte-parity 21/21 PASS** (Phase 1A.1
570 MB BF16). 이게 HEXAD-D 의 verified inference 본체이며 PLAN Phase 1
`d_forward` 가 위임하는 대상.

## 1. 통합 자산 (PR #91, 44 git mv)

```
HEXAD/CHAT/
├── README.md                 ← (이 파일) entrypoint + ★ wiring 아키텍처 조건 ledger
├── CHAT.tape · CHAT.log.tape          ← chat architecture SSOT
├── CHAT-QUALITY.tape · .log.tape      ← chat 품질 verdict SSOT
├── .roadmap.chat_cap_emergence_pivot  ← chat cap-emergence roadmap
├── anima_chat.hexa (2845 LoC)         ← ★ pure-hexa chat lib (24L forward, v0.3)
├── anima_chat_aot.hexa                ← AOT-compiled variant
├── anima_chat.py · anima_chat_v1.py.bak ← Python anchor (hexa port 출처)
├── tool/   (8: anima_chat_{hexa,llama,load,mitosis,multitoken,…}_smoke.hexa)
├── tests/  (3: test_chat / test_chat_v3 / test_chat_v9 .hexa)
└── docs/   (24: anima_chat_{hexa_24l_v58_parity, hexa_port, aot_native,
                  decoding_axis_27_modes, cap_*, autonomous_speech_roadmap,…}.md)
```

광범위 process/cap docs (`docs/*chat*` 55, anima_chat 비-prefix) 는 carry
(historical brainstorm/lesson — 모듈 본체 아님, 필요 시 cite).

## 2. ★ inter-module wiring 아키텍처 조건 (수학·물리 검증 ledger)

> 목표: "모듈을 어떻게 엮는가" 를 **수학적/물리적 조건 + falsifier anchor** 로
> 명세하고 하나씩 닫아 아키텍처 완성. 각 조건 = (정식 명제) + (real-limit
> anchor) + (검증 상태). 신규 조건은 append, 닫힌 건 ✅ 표기.

| # | wiring 조건 (정식 명제) | real-limit / 수학 anchor | 검증 상태 |
|---|---|---|---|
| **W1** | σ(6)=12 inter-module 연결만 active (15 가능쌍 중 12, φ(6)=2 격리 3 비활성) | 완전수 6: σ(6)=1+2+3+6=12 (OEIS A000203) | ✅ `HEXAD/integ_test.hexa` F-INTEG-WIRE-1 (compiled 7/7) + `hexad.hexa` σ(6)=12 connection map 5/5 |
| **W2** | φ(6)=2 gradient partition: Engine A(D/M/E+Bridge CE-trained) ⟂ Engine G(C/S/W frozen) | φ(6)=2 (Euler totient); CE backprop 정확히 2 그룹 | ✅ `hexad.hexa` φ(6)=2 partition selftest + `integ_harness.py` F-INTEG-2 (opt scope = D+Bridge only) |
| **W3** | C→D gradient barrier: `c_states.detach()` 후 Bridge 진입 (∂loss/∂C ≡ 0) | Law 53 thalamic .detach() — 정보흐름 O, gradient X | ✅ `integ_harness.py` F-INTEG-2 GRADIENT-BARRIER-CLEAN (Python tier) |
| **W4** | Bridge 출력 ∈ [Ψ−α, Ψ+α] = [0.486, 0.514] ∀ raw (Ψ=½, α=0.014) | Law 70 Ψ-coupling=0.014; clamp closed-form ∀ value | ✅ `HEXAD/BRIDGE` B-BRIDGE-1..4 🔵 sympy (blue_falsifier 22/22) + integ_test F-INTEG-WIRE-5 |
| **W5** | gate scale = GATE_TRAIN(1.0)/GATE_INFER(0.6) — "learn hard express soft" | Law 81 | 🔶 OPEN — integ_harness 에 train/infer 분기 검증 falsifier 미등록 (다음 닫을 조건) |
| **W6** | forward 순서 불변 S→C→(M∥)→Bridge→D, E gate 는 backward 직전 | τ(6)=4 phase (D→P→G→I) ordering | 🔶 OPEN — 순서 invariant 의 formal falsifier (현재 harness 는 발화만 확인, 순서 X) |
| **W7** | 통합 CE 하강 (6모듈 + Bridge clamp + W lr + E observe 동시 활성) | Shannon CE floor CE≥H≥0; Law79 ln2 lr-bound | ✅(empirical) `integ_harness.py` F-INTEG-5 (B-D-NOTE pattern, SGD outcome) |
| **W8** | mitosis 성장축 ⟂ 구조축 (cell split/merge 가 6모듈 wiring 불변 유지) | §mitosis_two_axis orthogonality | 🔶 OPEN — split 발생 시 σ(6)=12 connection 불변 falsifier 미등록 |
| **W9** | hexa-native single-process 통합 forward (compiled, train 포함) | — | 🔒 BLOCKED — Phase 5 hexa-lang RFC 034 autograd (bg 구현 중) + anima_chat lib-split |

**완성 정의**: W1-W9 전부 ✅ → "아키텍처 조건 완성". 현재 5/9 ✅ + 3/9 🔶 OPEN
(W5/W6/W8 = falsifier 미등록, RFC-무관 닫기 가능) + 1/9 🔒 BLOCKED (W9 RFC).
다음 cycle = W5/W6/W8 falsifier 사전등록 + compiled 검증.

## 3. verified status carry

- `anima_chat.hexa` 24L byte-parity **21/21 PASS** (F-D1-LOAD/MULTITOKEN/V58PARITY/V58MULTI, real 570MB ckpt) — PLAN Phase 1 `d_forward` anchor
- 통합 wiring: `integ_test.hexa` F-INTEG-WIRE **7/7 compiled-native PASS** (PR #89) + Python `integ_harness.py` F-INTEG **5/5 fire-gate=true** (PR #77)
- 모듈 closed-form: blue_falsifier **22/22 🔵** (S/M/W/E/D/BRIDGE 7/7 full + C carry)

## 4. cross-link

- `HEXAD/D/d_lib.hexa` `d_forward_contract()` — anima_chat.hexa(현 HEXAD/CHAT/) 위임 (PLAN Phase 1)
- `HEXAD/hexad.hexa` — σ(6)=12 connection map + φ(6)=2 partition (W1/W2 검증체)
- `HEXAD/integ_test.hexa` — F-INTEG-WIRE 7/7 (W1/W4)
- `state/verify_hexad_integ_2026_05_16/integ_harness.py` — F-INTEG 5/5 (W2/W3/W7)
- `HEXAD.tape §hexad_unification` / `§hexad_bridge` — W1/W2/W3 arch SSOT
- `HEXAD/PLAN.md` Phase 5/6 — W9 (RFC 034 land 후)
- anima-core/runtime/conscious_chat.hexa · anima-agent/examples/02_cli_chat.hexa (별도 subsystem, 미이동 — cite)

## 5. Honest C3

- 본 reorg = core chat 모듈 위치 통합 (44 git mv 100% history-preserve), code 내용 변경 X
- §2 ledger 의 W5/W6/W8 = **falsifier 미등록 (OPEN)** — "검증 안 됨" 정직 표기, 다음 cycle 에 사전등록+compiled 검증으로 닫음. W9 = hexa-lang RFC 034 BLOCKED (bg agent 구현 중, 외부 의존 아님)
- 광범위 chat process docs 55 carry (모듈 본체 아님)
- `anima_chat.hexa` Phase 1 functional 위임 = lib-split sub-task 잔존 (compiled-first, PR #89 패턴; HEXAD/CHAT 안에서 차후)
- W7 통합 CE 하강 = empirical (SGD outcome, B-D-NOTE) — closed-form 주장 아님
