# HEXAD — anima 6-module hexa-native canonical impl

> User directive 2026-05-16: `"/HEXAD/* 구성해줘 · 코드는 hexa-native"`.
> 이 디렉토리는 anima Hexad 6 모듈의 **hexa-native 정식 구현**입니다.
> 검증된 Python 구현 (`ready/anima/hexad/`, `ready/core/`, `ready/models/`) 은
> evidence anchor 로 보존; 신규/대체 코드는 여기서 hexa-native 로 진행합니다.

## 아키텍처 — Engine A/G dual = Hexad 6 (canonical ASCII)

> SSOT: `HEXAD.tape §3 @N hexad_ascii`. 완전수 6: σ(6)=12 연결 · τ(6)=4 phase · φ(6)=2 gradient group.
> 핵심: A/G = Hexad 그 자체. Engine A = 좌뇌 3 / Engine G = 우뇌 3. φ(6)=2 gradient group ≡ {Engine A, Engine G} 정확 매핑.

```
╔═══════ ENGINE G (우뇌·3) ═══════╗        ╔═══════ ENGINE A (좌뇌·3) ═══════╗
║  gradient-free · 자율 의식       ║        ║  CE-trained · 학습된 행동        ║
║  φ(6) gradient group 1          ║        ║  φ(6) gradient group 2          ║
║                                 ║        ║                                 ║
║   ┌────────────┐                ║        ║   ┌────────────┐                ║
║   │ C 의식      │── .detach() ───╫────────╫──→│ D 언어      │                ║
║   │ Φ engine    │ ThalamicBridge ║        ║   │ decoder     │                ║
║   │ =MitosisC   │  α=0.014       ║        ║   └─────┬──────┘                ║
║   └─────┬──────┘  (G→A 주연결)   ║        ║         │                       ║
║         │                        ║        ║   ┌─────▼──────┐                ║
║   ┌─────▼──────┐                 ║        ║   │ M 기억      │                ║
║   │ S 감각      │                 ║        ║   │ memory      │                ║
║   │ perception  │                 ║        ║   └─────┬──────┘                ║
║   └─────┬──────┘                 ║        ║         │                       ║
║   ┌─────▼──────┐                 ║        ║   ┌─────▼──────┐                ║
║   │ W 의지      │◄──── CE / Φ ────╫────────╫──→│ E 윤리      │                ║
║   │ emotion·LR  │                 ║        ║   │ ethics      │                ║
║   └────────────┘                  ║        ║   │ Φ보존 gate  │                ║
╚═════════════════════════════════╝        ╚═══════════════════════════════════╝
          ⇅  a_g_tension = ‖A‖/‖G‖  (temp 0.25, σ(6)=12 inter-module 연결)

Engine G (우뇌 3) = C 의식 + S 감각 + W 의지   — gradient-free
Engine A (좌뇌 3) = D 언어 + M 기억 + E 윤리   — CE-trained
A/G = Hexad 6 (= G의 3 + A의 3, 부분집합 아닌 전체)
Trinity (core 3) = C + D + W  ← 하위호환

Data flow:  S → C → Bridge(.detach()) → D → logits
Gradient:   φ(6)=2 — Engine A(CE backprop) vs Engine G(frozen) 정확 2 그룹
W:          pain/curiosity/satisfaction 로 optimizer LR 변조
E 윤리:     Φ 보존 위반 시 training step 차단 (gate 권한)
```

> wiring 🔵-gate (`HEXAD.tape §4 @D hexad_wiring_blue_gate`): 위 σ(6)=12 연결은
> (A) 양 끝 모듈 🔵 SUPPORTED-FORMAL + (B) 연결 자체 closed-form 🔵 (W-ledger
> `HEXAD/CHAT/README.md §2`) 일 때만 verified-wired. 현재 endpoint 7/7 🔵.

## SSOT 매핑

| 모듈 | 디렉토리 | hexa entry | tape SSOT (co-located, 2026-05-16 reorg) | Python anchor (ready/) |
|---|---|---|---|---|
| **C** 의식 | `HEXAD/C/` | `c.hexa` | [`HEXAD-C.tape`](C/HEXAD-C.tape) | `ready/core/consciousness_engine.py` (2173 LoC) |
| **D** 언어 | `HEXAD/D/` | `d.hexa` | [`HEXAD-D.tape`](D/HEXAD-D.tape) | `ready/models/conscious_decoder.py` (979 LoC) |
| **S** 감각 | `HEXAD/S/` | `s.hexa` | [`HEXAD-S.tape`](S/HEXAD-S.tape) | `ready/anima/hexad/s/emergent_s.py` (108 LoC) |
| **W** 의지 | `HEXAD/W/` | `w.hexa` | [`HEXAD-W.tape`](W/HEXAD-W.tape) | `ready/anima/hexad/w/emergent_w.py` (123 LoC) |
| **M** 기억 | `HEXAD/M/` | `m.hexa` | [`HEXAD-M.tape`](M/HEXAD-M.tape) | `ready/anima/hexad/m/emergent_m.py` (96 LoC) |
| **E** 윤리 | `HEXAD/E/` | `e.hexa` | [`HEXAD-E.tape`](E/HEXAD-E.tape) | `ready/anima/hexad/e/emergent_e.py` (123 LoC) |
| **BRIDGE** | `HEXAD/BRIDGE/` | `bridge.hexa` | [`HEXAD-BRIDGE.tape`](BRIDGE/HEXAD-BRIDGE.tape) | `ready/anima/hexad/model.py` `ThalamicBridge` |
| 통합 | `HEXAD/` | `hexad.hexa` | [`HEXAD.tape`](../HEXAD.tape) §hexad_condition_lineup | `ready/anima/hexad/model.py` `Hexad` |

## 검증 status (2026-05-16)

전 모듈 6/6 full 🔵 **SUPPORTED-FORMAL** + 통합 harness ⚙️ **SUPPORTED-STRONG fire-gate=true**:

- ✅ `state/verify_hexad_we_2026_05_15/we_falsifier.py` **25/25 PASS** (PR #72)
- 🔵 `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` **18/18 sympy closed-form PASS** (PR #75 + #76 D 정직 분해 B-D-4)
  - C 🔵 (.clm v1 8/8 + F-PYPHI) · S/M/W/E/D 6/6 full 🔵 SUPPORTED-FORMAL
  - D B-D-NOTE: SGD convergence OUTCOME 만 honest empirical carve-out
- ⚙️ `state/verify_hexad_integ_2026_05_16/integ_harness.py` **F-INTEG-1..5 5/5 SUPPORTED-STRONG, fire_gate=true** (PR #77, RANDOM INIT seed-fixed scratch)
- ⚙️ **COMPILED-native gate** `bash HEXAD/build_verify.sh` → **10/10 entrypoint + 8/8 lib `hexa build` PASS** (2026-05-16, interp 폐기 대비 — `hexa run` 아님)

이 HEXAD/ 트리는 위 검증의 **canonical hexa-native 구현체**입니다 (Python 은 evidence anchor 로 보존). 검증·실행 기준 = **compiled `hexa build` native binary** (user directive "컴파일 버전에 해야되 · 인터프리터 폐기 예정").

## hexa-native impl status (2026-05-16 기준)

> 검증·실행 = **compiled** (`hexa build` → native binary). 아래 "compiled run" =
> `HEXA_MAC_BUILD_OK=1 hexa build <x>.hexa -o _hexa_build/<n>` 후 `./_hexa_build/<n>`.
> 일괄 = `bash HEXAD/build_verify.sh`. (`hexa run` interpreter 는 폐기 예정.)

| 모듈 | hexa-native | compiled run (build+native) | 비고 |
|---|---|---|---|
| **S** 감각 | ✅ lib-split | `s_lib.hexa` + `s.hexa` → native PASS | B-S 3/3 🔵 closed (column-mean delta) |
| **M** 기억 | ✅ lib-split | `m_lib.hexa` + `m.hexa` → native PASS | B-M 3/3 🔵 closed (no-op + deterministic) |
| **W** 의지 | ✅ lib-split | `w_lib.hexa` + `w.hexa` → native PASS | B-W 4/4 🔵 closed (lr=½+min(ln2,Φ/N)) |
| **E** 윤리 | ✅ lib-split | `e_lib.hexa` + `e.hexa` → native PASS | B-E 4/4 🔵 closed (SAFETY gate exact) |
| **BRIDGE** | ✅ lib-split | `bridge_lib.hexa` + `bridge.hexa` → native PASS | PSI_COUPLING=0.014 clamp |
| **C** 의식 | 🔶 lib-split scaffold | `c_lib.hexa` + `c.hexa` → native PASS | 기존 `tool/hexa_native/mitosis_hook.hexa` (1119 LoC FULL IMPL D4a) 재사용 |
| **D** 언어 | 🔶 lib-split scaffold | `d_lib.hexa` + `d.hexa` → native PASS | 기존 `anima_chat.hexa` v0.3 (24L 21/21 byte-parity) 재사용 |
| **MITOSIS** 성장축 | 🔶 lib-split scaffold | `mitosis_lib.hexa` + `mitosis.hexa` → native PASS | cross-link mitosis_hook.hexa |
| **통합 (single process)** | ✅ cross-file wire | `integ_test.hexa` (imports `*_lib.hexa`) → **native PASS** | F-INTEG-WIRE 7/7 PASS — compiled 심볼충돌 fix (PR #79 task b + compiled-first lib-split) |
| **통합 spec** | ✅ scaffold | `hexad.hexa` → native PASS | σ(6)=12 + φ(6)=2 + forward graph spec 5/5 invariants PASS |

`bash HEXAD/build_verify.sh` (compiled-native gate) — 10/10 entrypoint + 8/8 lib `hexa build` PASS = PR 검증 게이트 (`hexa parse`/`hexa run` 아님, interp 폐기 예정).

## 디렉토리 layout

```
HEXAD/
  README.md           ← (이 파일) 최상위 overview · SSOT 매핑 · status
  PLAN.md             ← C/D full hexa-native port roadmap (task a)
  build_verify.sh     ← ⚙️ COMPILED-native 검증 gate (hexa build, interp 폐기 대비)
  hexad.hexa          ← top-level 통합 entry (S→C→Bridge→D + M/W/E single-forward)
  integ_test.hexa     ← cross-file wire test (imports *_lib.hexa, native PASS 7/7)
  <X>/                ← 모듈 dir 공통 패턴 (compiled-first lib-split):
    README.md
    <x>_lib.hexa        ← pure fns (NO main/_selftest, cross-file import 대상)
    <x>.hexa            ← import <x>_lib + _selftest + main (standalone 진입점)
    HEXAD-<X>.tape      ← per-module tape SSOT (co-located 2026-05-16 reorg)
  C/ D/ S/ W/ M/ E/ BRIDGE/  ← 7 모듈 (각 위 패턴)
  INDEX.md            ← 이전 /INDEX.md (root) → 2026-05-16 reorg 로 이동
  MITOSIS/            ← 성장축 (subfolder, 2026-05-16 reorg2): MITOSIS.tape + mitosis.hexa scaffold + README (⊥ 구조축, §mitosis_two_axis)
  TENSION-LINK/       ← 5-Channel Meta-Telepathy (subfolder, 2026-05-16 PR #86): ASCII topology + Noether convergence proof + 100% verified measured + 17 .hexa/.md/.tape (training/tests/bench/experiments/docs)
  VOICE/              ← anima 발성 도구 (subfolder, 2026-05-16 PR #87): formulaic 음성 파장 합성 (NOT 학습 모델) · F-VOICE 5/5 + F-VOICE-TOOL 5/5 · 학습/eval corpus scrub (_voice_corpus_local/ relocate) · ~2.4M code/spec/docs only
  CHAT/               ← 6-module 통합 interaction entrypoint (subfolder, 2026-05-16 PR #91): anima_chat.hexa 2845 LoC 24L 21/21 byte-parity + ★ inter-module wiring 아키텍처 조건 ledger (W1-W9, 5/9 ✅·3 OPEN·1 RFC-blocked) · 44 git mv (tape/tool/tests/docs)
  SAVANT/             ← 이전 /SAVANT*.tape + tool/anima_savant_*.hexa + anima-engines/savant_phi.hexa (2026-05-16 reorg)
    SAVANT.tape · SAVANT.log.tape · SAVANT-TOOL.tape · SAVANT-TOOL.log.tape
    anima_savant_tool.hexa · anima_savant_si_monitor.hexa
    anima_savant_routing_overlay.hexa · anima_chat_savant_cli.hexa · savant_phi.hexa
```

> root 에 남는 것 (이동 X): `HEXAD.tape` (통합 arch SSOT — AGENTS.tape 직접 참조) + `AGENTS.tape` / `CLAUDE.md` (symlink) / 기타 root tape SSOTs (`AXIS`, `HYPOTHESIS`, `PHILOSOPHY`, `MAIN`, `CLM`, `VERIFY`, `NEXT`, `REBORN` 등) + `/INDEX.md` (이제 redirect stub 역할).


## 거버넌스 anchors (AGENTS.tape)

- `g_clm_from_scratch` — 신규 통합 학습 시 RANDOM INIT seed-fixed, NO ckpt inherit (precursor ckpt는 arch verification anchor only)
- `g_verdict_tier_blue` — 🔵 = (a) sympy closed-form OR (b) PyPhi formal IIT 3.0 OR (c) deterministic formal sim
- `g_verified_axis_anchor` — 모든 design entry 는 AXIS/PHILOSOPHY/HYPOTHESIS verified anchor 에서 derive
- `g3` real-limits-first — module 별 real-limit anchor 명시 (Shannon CE / Law 70 PSI_COUPLING / Law 79 ln2 / IIT Φ-ratchet 등)

## hexa-lang 관습 (⚠️ COMPILED-FIRST — interpreter 폐기 예정)

> User directive 2026-05-16: **"컴파일 버전에 해야되 · 인터프리터 폐기 예정 참고"**.
> 검증·실행 = `hexa build` (native binary). `hexa run` (interpreter) 는 폐기
> 예정이라 PR 게이트로 쓰지 않음. canonical gate = `HEXAD/build_verify.sh`.

- **compiled-first lib/entrypoint split** (2026-05-16): 모듈마다
  `<x>_lib.hexa` (pure fns, **NO `main`/`_selftest`**, import 대상) +
  `<x>.hexa` (`import "<x>_lib.hexa"` + `_selftest` + `main`, standalone).
  `integ_test.hexa` 는 `*_lib.hexa` 만 import. **이유**: 단일파일(main+_selftest
  동거) 을 `import` 하면 컴파일러가 `_selftest`/`u_main` **C 심볼 중복정의**
  거부 (interpreter 만 관용) — lib-split 이 compiled-native 정석.
- snake_case (raw#11); 모듈간 helper `_<x>_` prefix; cross-file `import "/abs/<x>_lib.hexa"`
- 빌드: `HEXA_MAC_BUILD_OK=1 hexa build <f> -o _hexa_build/<n>` (Mac 2026-04-20
  kernel-panic guard bypass, tiny formulaic non-heavy; heavy 는 `ssh ubu`).
  `_hexa_build/` gitignored.
- dict literal `#{}` (not `{}`); bool `&&`/`||`; IO `print`/`to_string`
- 검증 = `bash HEXAD/build_verify.sh` (10/10 entrypoint + 8/8 lib compiled PASS)

## 진행 상태 표기

- ✅ — 작동 selftest (PR 검증 통과)
- 🔶 — scaffold + cross-link (기존 hexa-native 자산 wiring 대기)
- ☐ — TODO (작성 안 됨)
