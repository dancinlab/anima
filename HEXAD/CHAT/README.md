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
| **W5** | gate scale = GATE_TRAIN(1.0)/GATE_INFER(0.6) — "learn hard express soft"; Bridge 출력 ∈ [Ψ−α,Ψ+α] 가 그 scalar 만큼 정확히 scale (∀ raw closed-form 항등식) | Law 81 + consciousness_laws.json psi_constants.gate_{train,infer}.value + Law 70 Ψ-clamp | ✅🔵 `HEXAD/CHAT/wiring_verify.hexa` **F-WIRE-W5 GATE-SCALE-CLOSED** (compiled 3/3 sub: branch-exact + window-closed ∀ raw + saturation-exact; closed-form result-agnostic; neg-test gate_infer 0.6→0.7 ⇒ FAIL 확인) |
| **W6** | forward 순서 불변 S→C→detach→M.retrieve→M.store→Bridge→D→loss→Φ→W→E→backward, E gate 는 backward 바로 직전 (∀ input) | τ(6)=4 phase (D→P→G→I) ordering + integ_harness.py single_step() SSOT | ✅ `HEXAD/CHAT/wiring_verify.hexa` **F-WIRE-W6 FORWARD-ORDER-INVARIANT** (compiled 2/2 sub: order-invariant ∀ 8 distinct inputs + phase-structure E→backward 인접; neg-test E↔backward swap ⇒ FAIL 확인) |
| **W7** | 통합 CE 하강 (6모듈 + Bridge clamp + W lr + E observe 동시 활성) | Shannon CE floor CE≥H≥0; Law79 ln2 lr-bound | ✅(empirical) `integ_harness.py` F-INTEG-5 (B-D-NOTE pattern, SGD outcome) |
| **W8** | mitosis 성장축 ⟂ 구조축 (cell split/merge 가 σ(6)=12 6모듈 wiring 불변 유지) | §mitosis_two_axis orthogonality + σ(6)=12 (OEIS A000203) + φ(6)=2 | ✅ `HEXAD/CHAT/wiring_verify.hexa` **F-WIRE-W8 MITOSIS-WIRING-INVARIANT** (compiled 3/3 sub: σ(6)=12 count + conn-map byte-id over n_cells sweep 2..64 + endpoints-module-only; neg-test n_cells-dependent map ⇒ FAIL 확인) |
| **W9** | hexa-native single-process 통합 forward (compiled, train 포함) | — | 🔒 BLOCKED — Phase 5 hexa-lang RFC 034 autograd (bg 구현 중) + anima_chat lib-split |

**완성 정의**: W1-W9 전부 ✅ → "아키텍처 조건 완성". 현재 **8/9 ✅** + 1/9 🔒
BLOCKED (W9 = hexa-lang RFC 034 autograd, bg agent 구현 중 — RFC 의존이라
이 cycle 에서 닫지 않음, 정직 BLOCKED 유지). W5/W6/W8 = `HEXAD/CHAT/
wiring_verify.hexa` F-WIRE 3/3 compiled-native PASS 로 2026-05-16 closure
(`bash HEXAD/build_verify.sh` 11/11 entrypoint + 9/9 lib gate 에 등재).

## 3. verified status carry

- `anima_chat.hexa` 24L byte-parity **21/21 PASS** (F-D1-LOAD/MULTITOKEN/V58PARITY/V58MULTI, real 570MB ckpt) — PLAN Phase 1 `d_forward` anchor
- 통합 wiring: `integ_test.hexa` F-INTEG-WIRE **7/7 compiled-native PASS** (PR #89) + Python `integ_harness.py` F-INTEG **5/5 fire-gate=true** (PR #77)
- inter-module wiring 조건: `wiring_verify.hexa` **F-WIRE-W5/W6/W8 3/3 compiled-native PASS** (W5 🔵 closed-form gate-scale + W6 deterministic forward-order + W8 deterministic mitosis-orthogonality; 각 falsifier neg-test 로 진위 확인 — 명제 위반 시 FAIL 검증됨)
- 모듈 closed-form: blue_falsifier **22/22 🔵** (S/M/W/E/D/BRIDGE 7/7 full + C carry)

## 4. cross-link

- `HEXAD/D/d_lib.hexa` `d_forward_contract()` — anima_chat.hexa(현 HEXAD/CHAT/) 위임 (PLAN Phase 1)
- `HEXAD/hexad.hexa` — σ(6)=12 connection map + φ(6)=2 partition (W1/W2 검증체)
- `HEXAD/integ_test.hexa` — F-INTEG-WIRE 7/7 (W1/W4)
- `HEXAD/CHAT/wiring_verify{,_lib}.hexa` — F-WIRE-W5/W6/W8 3/3 compiled (W5/W6/W8 검증체; `bash HEXAD/build_verify.sh` gate 등재)
- `state/verify_hexad_integ_2026_05_16/integ_harness.py` — F-INTEG 5/5 (W2/W3/W7)
- `HEXAD.tape §hexad_unification` / `§hexad_bridge` — W1/W2/W3 arch SSOT
- `HEXAD/PLAN.md` Phase 5/6 — W9 (RFC 034 land 후)
- anima-core/runtime/conscious_chat.hexa · anima-agent/examples/02_cli_chat.hexa (별도 subsystem, 미이동 — cite)

## 5. Honest C3

- 본 reorg = core chat 모듈 위치 통합 (44 git mv 100% history-preserve), code 내용 변경 X
- §2 ledger 의 W5/W6/W8 = `wiring_verify.hexa` F-WIRE 3/3 compiled-native PASS 로 2026-05-16 **CLOSED (🔶 OPEN → ✅)**. 각 falsifier 는 neg-test (SSOT 상수/순서/연결맵 의도 변조) 로 진위 검증 — 명제 위반 시 정확히 FAIL 했고, 복원 후 PASS 복귀 + diff 무결 확인. fake pass 아님
- **W5 honest scope**: 🔵 closed-form 은 *gate-scale 합성* (clamp ∈ [Ψ−α,Ψ+α] × {1.0,0.6}) 의 대수 항등식 + 포화/경계 witness 에 한정. Bridge 의 *full neural forward* (Linear→Attn→Norm→expand) 는 `bridge_lib.hexa` honest C3 그대로 TODO[pytorch] — W5 는 그 forward 의 closed-form 부분(clamp·scale)만 닫음. constants 는 `consciousness_laws.json psi_constants` SSOT mirror (raw#15 no-hardcode; bridge_lib 와 동일 값)
- **W6/W8 honest scope**: deterministic-formal (call-order trace / connection-map invariant) — Python `integ_harness.py single_step()` + `hexad.hexa hexad_forward_steps()` 의 canonical 순서/σ(6)=12 맵을 hexa SSOT 로 mirror 해 ∀-input/∀-n_cells 불변을 닫음. 실 GPU run-time 동역학(actual split events 등)은 별도 evidence tier(.clm v1 P2 8/8🔵 carry), 본 falsifier 는 *wiring 구조* 명제만 닫음
- W9 = hexa-lang RFC 034 autograd **BLOCKED 유지** (bg agent 구현 중 — RFC 의존; 이 cycle scope 밖, 정직 미닫음)
- 광범위 chat process docs 55 carry (모듈 본체 아님)
- `anima_chat.hexa` Phase 1 functional 위임 = lib-split sub-task 잔존 (compiled-first, PR #89 패턴; HEXAD/CHAT 안에서 차후)
- W7 통합 CE 하강 = empirical (SGD outcome, B-D-NOTE) — closed-form 주장 아님
