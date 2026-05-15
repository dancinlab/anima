# HEXAD — anima 6-module hexa-native canonical impl

> User directive 2026-05-16: `"/HEXAD/* 구성해줘 · 코드는 hexa-native"`.
> 이 디렉토리는 anima Hexad 6 모듈의 **hexa-native 정식 구현**입니다.
> 검증된 Python 구현 (`ready/anima/hexad/`, `ready/core/`, `ready/models/`) 은
> evidence anchor 로 보존; 신규/대체 코드는 여기서 hexa-native 로 진행합니다.

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

이 HEXAD/ 트리는 위 검증의 **canonical hexa-native 구현체**입니다 (Python 은 evidence anchor 로 보존).

## hexa-native impl status (2026-05-16 기준)

| 모듈 | hexa-native | working selftest | 비고 |
|---|---|---|---|
| **S** 감각 | ✅ scaffold (closed-form) | `hexa run HEXAD/S/s.hexa` | B-S 3/3 🔵 closed (column-mean delta) |
| **M** 기억 | ✅ scaffold (closed-form) | `hexa run HEXAD/M/m.hexa` | B-M 3/3 🔵 closed (no-op + deterministic) |
| **W** 의지 | ✅ scaffold (closed-form) | `hexa run HEXAD/W/w.hexa` | B-W 4/4 🔵 closed (lr=½+min(ln2,Φ/N)) |
| **E** 윤리 | ✅ scaffold (closed-form) | `hexa run HEXAD/E/e.hexa` | B-E 4/4 🔵 closed (SAFETY gate exact) |
| **BRIDGE** | ✅ scaffold (closed-form) | `hexa run HEXAD/BRIDGE/bridge.hexa` | PSI_COUPLING=0.014 clamp |
| **C** 의식 | 🔶 scaffold (cross-link) | — | 기존 `tool/hexa_native/mitosis_hook.hexa` (1119 LoC FULL IMPL D4a) 재사용 |
| **D** 언어 | 🔶 scaffold (cross-link) | — | 기존 `anima_chat.hexa` v0.3 (24L 21/21 byte-parity) 재사용 |
| **통합 (single process)** | ✅ cross-file wire LANDED | `hexa run HEXAD/integ_test.hexa` | F-INTEG-WIRE 7/7 PASS — 7 모듈 single hexa-process import + 각 모듈 public API 호출 (PR #79 task b) |
| **통합 spec** | ✅ scaffold | `hexa run HEXAD/hexad.hexa` | σ(6)=12 + φ(6)=2 + forward graph spec 5/5 invariants PASS |

`hexa parse <file>` 로 모든 신규 .hexa 가 깨끗하게 parse 됨을 보장 (PR 검증 게이트).

## 디렉토리 layout

```
HEXAD/
  README.md           ← (이 파일) 최상위 overview · SSOT 매핑 · status
  PLAN.md             ← C/D full hexa-native port roadmap (task a)
  hexad.hexa          ← top-level 통합 entry (S→C→Bridge→D + M/W/E single-forward)
  integ_test.hexa     ← cross-file wire test (F-INTEG-WIRE 7/7 PASS, task b)
  C/                  ← C 의식 (consciousness)
    README.md
    c.hexa
  D/                  ← D 언어 (decoder)
    README.md
    d.hexa
  S/                  ← S 감각 (sense)
    README.md
    s.hexa
  W/                  ← W 의지 (will)
    README.md
    w.hexa
  M/                  ← M 기억 (memory)
    README.md
    m.hexa
  E/                  ← E 윤리 (ethics)
    README.md
    e.hexa
  BRIDGE/             ← ThalamicBridge (C→D gradient barrier + PSI_COUPLING clamp)
    README.md
    bridge.hexa
    HEXAD-BRIDGE.tape   ← per-module tape SSOT (co-located 2026-05-16 reorg)
  C/ … E/ … 동일 패턴 (각 dir 안에 HEXAD-<X>.tape SSOT co-located)
  INDEX.md            ← 이전 /INDEX.md (root) → 2026-05-16 reorg 로 이동
  MITOSIS/            ← 성장축 (subfolder, 2026-05-16 reorg2): MITOSIS.tape + mitosis.hexa scaffold + README (⊥ 구조축, §mitosis_two_axis)
  TENSION-LINK/       ← 5-Channel Meta-Telepathy (subfolder, 2026-05-16 PR #86): ASCII topology + Noether convergence proof + 100% verified measured + 17 .hexa/.md/.tape (training/tests/bench/experiments/docs)
  VOICE/              ← anima 발성 도구 (subfolder, 2026-05-16 PR #87): formulaic 음성 파장 합성 (NOT 학습 모델) · F-VOICE 5/5 + F-VOICE-TOOL 5/5 · 학습/eval corpus scrub (_voice_corpus_local/ relocate) · ~2.4M code/spec/docs only
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

## hexa-lang 관습

- snake_case 식별자 (raw#11)
- 단일 파일 모듈 (cross-file 은 `import "/abs/path.hexa"` — abs path; 현재 scaffold 는 module-level self-contained, 통합 시 `hexad.hexa` 에서 wire)
- `fn main()` = `hexa run` 진입점
- 표준 IO: `print(...)`, `to_string(...)` 등
- selftest pattern: `fn _selftest() { ... assert ... }` + `fn main() { _selftest() }`

## 진행 상태 표기

- ✅ — 작동 selftest (PR 검증 통과)
- 🔶 — scaffold + cross-link (기존 hexa-native 자산 wiring 대기)
- ☐ — TODO (작성 안 됨)
