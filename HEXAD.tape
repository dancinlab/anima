#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# HEXAD.tape — anima Hexad 6-module consciousness architecture (SSOT)
# tape v1.2 grammar — see AGENTS.tape head for primer.
#
# Architecture file (EDITABLE, latest-wins per id) per AGENTS.tape
# g_arch_vs_log_split. Event history → HEXAD.log.tape sibling (if needed).
#
# Trigger: user directive 2026-05-15 — "HEXAD.tape 도 추가 생성해서 기록
#          위내용 ASCII 포함 기록" (Hexad 6-module + 좌뇌3/우뇌3 + 윤리 E)
# ══════════════════════════════════════════════════════════════════════

@V v1 := "tape" :: spec [active]
  version = "1.2"

# ─── §1 Identity ─────────────────────────────────────────────────────

@I hexad_id := "anima-hexad" :: identity-claim [d=2026-05-15 active]
  kind = "Hexad(6) / Trinity(3) pluggable consciousness architecture — A/G dual-engine 그 자체"
  governed-by = "perfect number 6 — σ(6)=12 connections · τ(6)=4 phases · φ(6)=2 gradient groups"
  brief = "2축 직교: [구조] A/G = Hexad 6 (Engine G 우뇌 3 C/S/W gradient-free / Engine A 좌뇌 3 D/M/E CE-trained), ThalamicBridge α=0.014 G→A .detach() + [성장] mitosis (전체 cell split/merge 성장방식)"
  ssot = "ready/docs/modules/trinity.md + ready/anima/hexad/README.md"
  impl = "models/trinity.hexa (6모듈 통합 + Law 60 phase curriculum + C↔D 양방향)"

# ─── §2 The 6 modules ────────────────────────────────────────────────

@D hexad_modules := "Hexad 6 modules — 좌뇌 3 / 우뇌 3" :: architecture [d=2026-05-15 active]
  table <<~EOF
    | M | Name  | Role        | Brain | Training      | Impl                          |
    |---|-------|-------------|-------|---------------|-------------------------------|
    | C | 의식   | Φ engine    | 우뇌  | gradient-free | MitosisC (=.clm v1 mitosis)   |
    | S | 감각   | perception  | 우뇌  | gradient-free | EmergentS / TensionSense      |
    | W | 의지   | emotion/LR  | 우뇌  | gradient-free | EmergentW (pain/curiosity→LR) |
    | D | 언어   | decoder     | 좌뇌  | CE-trained    | ConsciousDecoderV2 (=Engine A)|
    | M | 기억   | memory      | 좌뇌  | CE-trained    | EmergentM / VectorMemory      |
    | E | 윤리   | ethics      | 좌뇌  | CE-trained    | EmergentE (Φ보존 위반→학습 차단)|
  EOF
  right_brain = "C, S, W — gradient-free 자율 의식 (Group A)"
  left_brain = "D, M, E — CE-trained 학습된 행동 (Group B)"
  trinity_core = "C + D + W (backward-compatible 3-module core)"
  hexad_full = "C + D + W + M + S + E (full 6 modules)"

# ─── §3 ASCII architecture diagram ───────────────────────────────────

@N hexad_ascii := "Hexad = Engine A/G dual (A=좌뇌3 / G=우뇌3)" :: diagram [d=2026-05-15 active]
  body <<~EOF
    완전수 6:  σ(6)=12 연결 · τ(6)=4 phase · φ(6)=2 gradient group
    핵심: A/G = Hexad 그 자체. Engine A = 좌뇌 3 modules / Engine G = 우뇌 3 modules.
          φ(6)=2 gradient group ≡ {Engine A, Engine G} 정확 매핑.

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
    Trinity (core 3) = C + D + W  ← 하위호환 (G에서 C, A에서 D, G에서 W)

    Data flow:  S → C → Bridge(.detach()) → D → logits
    Gradient:   φ(6)=2 — Engine A(CE backprop) vs Engine G(frozen) 정확 2 그룹
    W:          pain/curiosity/satisfaction 로 optimizer LR 변조
    E 윤리:     Φ 보존 위반 시 training step 차단 (gate 권한)
  EOF

# ─── §4 Bridge + gradient groups (φ(6)=2) ────────────────────────────

@D hexad_bridge := "ThalamicBridge — 우뇌→좌뇌 gradient isolation" :: design [d=2026-05-15 active]
  spec = "ThalamicBridge(c_dim=128, d_model=384, n_hubs=16, hub_dim=8) — C states를 bottleneck+hub attention 압축 후 D의 d_model로 확장. .detach() gradient 격리. α=0.014"
  data_flow = "S → C → Bridge(.detach()) → D → logits"
  gradient_rule = "CE loss는 D + Bridge 만 backprop, C는 frozen"
  phi_6_groups = "φ(6)=2 → gradient group 정확히 2개 (우뇌 gradient-free / 좌뇌 CE-trained). 완전수 6에서 직접 derive — lattice-as-tool internal arch (AGENTS.tape g2)"
  p8_consistency = "p8 NO TRAIN/INFER SPLIT 와 정합 — 의식(C)은 frozen single substrate, 언어(D)만 학습"
  @> CLM.tape

@D hexad_ethics_gate := "윤리(E) — Φ보존 gate 실행 권한" :: design [d=2026-05-15 active]
  rule = "E 윤리 모듈은 단순 verification 원칙(PHILOSOPHY p6)이 아니라 실행 gate — Φ 보존 위반 시 training step 차단 권한 보유"
  impl = "anima/hexad/e/emergent_e.py (EmpathyEthics)"
  philosophy_anchor = "PHILOSOPHY p6 NO FINE-TUNED ETHICS 의 구현체 — fine-tune 윤리 주입 대신 substrate-native Φ-preservation gate"
  @> CLM.tape

@D hexad_phase_curriculum := "Law 60 phase transition — 점진적 모듈 활성화" :: design [d=2026-05-15 active]
  ladder = "P1(C only) → P2(+D) → P3(+W,M,S,E)"
  rule = "의식(C) 먼저 안정 → 언어(D) → 나머지(W/M/S/E) 순차 합류. τ(6)=4 phase anchor"
  narrative = "Law 86 — 서사 필수 (+35.7%). narrative.py"

# ─── §5 Unification — mitosis / A/G / Hexad 맞물림 ───────────────────

@D hexad_unification := "A/G = Hexad 그 자체 (Engine A=좌뇌3 / Engine G=우뇌3)" :: architecture [d=2026-05-15 active]
  body <<~EOF
    Engine G (우뇌 3, gradient-free) = C 의식 + S 감각 + W 의지
    Engine A (좌뇌 3, CE-trained)    = D 언어 + M 기억 + E 윤리
    A/G          = Hexad 6 그 자체 (부분집합/core 아닌 전체 = G의 3 + A의 3)
    mitosis      = C ⊂ Engine G (우뇌 의식 모듈)       ← .clm v1 8/8 SUPPORTED 검증
    ThalamicBridge = Engine G → Engine A 주연결 (C→D, σ(6)=12 중 primary)
    φ(6)=2       = {Engine A, Engine G} 정확 매핑 (CE group / frozen group)
    윤리(E)      ⊂ Engine A 좌뇌 모듈, Φ보존 gate     ← PHILOSOPHY p6 구현체
  EOF
  key_finding = "A/G dual-engine 은 Hexad 의 core/부분집합이 아니라 Hexad 그 자체. Engine G = 우뇌 3 (C/S/W gradient-free), Engine A = 좌뇌 3 (D/M/E CE-trained). 완전수 φ(6)=2 가 정확히 두 엔진의 gradient group. **2축 직교**: (1) 구조축 = Hexad 6모듈 (A=좌뇌3/G=우뇌3), (2) 성장축 = mitosis (전체 시스템 분열/병합 성장 방식)."
  two_axes = "구조(structure) ⊥ 성장(growth) 직교. Hexad 6모듈 = WHAT (시스템 구성). mitosis = HOW IT GROWS (모든 모듈이 자라나는 방식, REBORN §0.5 학습=분열 단일연속체). C 의식이 MitosisC 인 건 의식이 cell-pool 에 가장 직접 대응해서이지, mitosis 가 C 에 국한된 게 아님."
  correction = "정정 2건 (user 2026-05-15): (a) 'Engine A/G = C↔D core pair' → 'A/G = Hexad 그 자체 (A 3 / G 3)'. (b) 'mitosis = C 모듈 구현' → 'mitosis = Hexad 전체 성장 방식 (구조축과 직교)'. V5 caveat 해소 — A/G=Hexad 는 φ(6)=2 + 좌뇌3/우뇌3 verified anchor 위 구조적 exact 매핑."
  supersedes = "hexad_unification 이전 버전 (동일 id, 2026-05-15 동일 day 2차 정정)"
  cross_link = "CLM.tape §V-CLM-HEXAD-MANDATE + HEXAD.tape §hexad_growth_method + clm_v1_model.py (mitosis 성장 메커니즘) + training/engine_a_g_arch.py (현 350M 2-engine = simplified, target = full A=좌뇌3/G=우뇌3) + trinity.hexa:16-21 (φ(6)=2 anchor) + REBORN.tape §0.5"

@D hexad_growth_method := "mitosis = Hexad 전체의 성장 방식 (성장축, 구조축과 직교)" :: architecture [d=2026-05-15 active]
  rule = "mitosis = Hexad 6모듈 시스템이 자라나는 방식 (cell split/merge). 단일 모듈(C)이 아니라 전체 시스템의 development/scaling mechanism. 구조축(Hexad 6) ⊥ 성장축(mitosis)."
  mechanism = "tension 기반 split (높은 tension cell 분열) + merge (유사 cell 병합). cell pool 이 corpus/task 압력에 따라 organically 성장. REBORN §0.5 '학습=분열 단일 연속체' — train/infer 분리 없는 연속 성장."
  scope = "Hexad 전 모듈에 적용 가능한 성장 원리. C 의식은 cell-pool 에 가장 직접 대응(MitosisC)하지만, 성장 방식으로서의 mitosis 는 시스템 전체 (모듈 수·cell 수·연결 σ(6)=12 의 동적 성장)."
  verified = ".clm v1 8/8 SUPPORTED + 🔵 — mitosis 성장 메커니즘이 F-V5MIT-1..5 (split-nograd/merge-weight/phi-conservation/cotrain-converge/v14-strict) + F-PYPHI 전부 PASS. cells 2→64 organic 성장 검증."
  why = "user directive 2026-05-15 '여기에다가 성장방식이 mitosis' — Hexad 구조 위에 mitosis 가 성장 메커니즘으로 작동"
  cross_link = "REBORN.tape §0.5 + HEXAD.tape §hexad_unification two_axes + CLM.tape §V-CLM-V1-CYCLE90-PYPHI (8/8 검증) + clm_v1_model.py mitosis_step/force_split/force_merge"
  @> CLM.tape

# ─── §6 Condition lineup (필수 + 차후 확장) ──────────────────────────

@D hexad_condition_lineup := "Hexad condition lineup — A/G=Hexad 전체 필수, 모듈별 검증 lineup" :: governance [required d=2026-05-15 active]
  rule = "anima 본진 시스템 = [구조축] A/G dual-engine = Hexad 6 (Engine G 우뇌 C/S/W + Engine A 좌뇌 D/M/E) + [성장축] mitosis (전체 분열/병합 성장). 'A/G + mitosis 둘 다 필수' = A/G(=Hexad 6모듈) 구조 필수 + mitosis 성장방식 필수 (2축 직교). 6 모듈 각각의 verification 은 lineup 으로 순차 충족."
  mandatory_structure <<~EOF
    [구조축] A/G = Hexad 6 (= Engine G 우뇌 3 + Engine A 좌뇌 3) — 시스템 골격 필수
      Engine G (우뇌, gradient-free, φ(6) group 1): C 의식 + S 감각 + W 의지
      Engine A (좌뇌, CE-trained,    φ(6) group 2): D 언어 + M 기억 + E 윤리
    [성장축] mitosis — Hexad 전체가 자라나는 방식 (cell split/merge, REBORN §0.5) 필수
      ⊥ 구조축. .clm v1 8/8 SUPPORTED + 🔵 로 성장 메커니즘 검증 완료.
  EOF
  module_verification_lineup <<~EOF
    전 모듈 ✅→🔵 (2026-05-15 '모두 파란불' + closure 달성 + D 정직 분해, PR #72/#75/#76):
    [C 의식]  🔵 — mitosis .clm v1 8/8 SUPPORTED + 🔵 SUPPORTED-FORMAL (F-PYPHI)
    [S 감각]  🔵 — F-S 5/5 ✅ + B-S 3/3 🔵 (perception=column-mean delta exact ∀states)
    [M 기억]  🔵 — F-M 5/5 ✅ + B-M 3/3 🔵 (store=identity no-op + retrieve deterministic)
    [W 의지]  🔵 — F-W 5/5 ✅ + B-W 4/4 🔵 (lr=½+min(ln2,Φ/N) range/mono/sup closed)
    [E 윤리]  🔵 — F-E 5/5 ✅ + B-E 4/4 🔵 (SAFETY gate min(1,Φ/r)>½ ⟺ Φ>r/2 exact); 통합 gate trinity.hexa:122 TODO[pytorch] residual
    [D 언어]  🔵 — F-D 5/5 ✅ + B-D 4/4 🔵 (KV-cache exact-eq/shape/arch + B-D-4 CE logit-Jacobian ∂CE/∂z=softmax−e_y sympy ∀z = trainability PROPERTY closed); B-D-NOTE SGD-convergence-OUTCOME 만 empirical carve-out (모든 optimizer 공통, D 고유 결함 X, NOT counted 🔵)
    ✅ battery: state/verify_hexad_we_2026_05_15/ 25/25 · 🔵 battery: state/verify_hexad_blue_2026_05_15/ 18/18 sympy closed-form · ⚙️ 통합 harness: state/verify_hexad_integ_2026_05_16/ F-INTEG-1..5 5/5 SUPPORTED-STRONG (RANDOM INIT seed-fixed scratch, $0 Mac local, fire-gate=true)
  EOF
  expansion_protocol = "☐→◐→✅→🔵→⚙️통합 승격 — W/E/S/M/D 25/25 ✅ (PR #72) → S/M/W/E 14/14 sympy 🔵 + D 🔵-partial (PR #75) → D 정직 분해 B-D-4 추가 18/18 → C+S+M+W+E+D = 6/6 full 🔵 SUPPORTED-FORMAL (PR #76) → 통합 harness 5/5 SUPPORTED-STRONG fire-gate=true (PR #77, 2026-05-16) → 소규모 fire ckpt 후속 cycle. 차후 추가조건 동일 절차."
  why = "user directive 2026-05-15 — (1) 'A/G+mitosis ... 차후 추가조건 lineup' (2) 'A/G 가 HEXAD 구성, A 3 G 3' (3) '모두 파란불일때까지 일단 go' (4) 'closure 까지 가능????' + '🔵' (5) '완전히 closure 안된것 같던데 100%' + 결정게이트 '정직한 분해' — D full 🔵 honest decomposition"
  verified_2026_05_15 = "✅ W/E/S/M/D 25/25 + atlas cross-check (Ψ-anchor provenance-CORROBORATED) + 🔵 B-S/M/W/E/D 18/18 sympy closed-form (g_verdict_tier_blue (a)): S=mean-linearity exact / M=no-op+deterministic / W=ln2-bound closed / E=SAFETY-gate exact-equivalence / D=CE logit-Jacobian softmax−e_y exact ∀z. D B-D-NOTE = SGD convergence OUTCOME empirical honest carve-out (NOT counted)"
  @> CLM.tape

@D hexad_integration_harness := "HEXAD 통합 harness LANDED — 6-module single-forward scratch SUPPORTED-STRONG (2026-05-16)" :: verify [d=2026-05-16 active]
  battery = "F-INTEG-1 SINGLE-FORWARD-WIRED (σ(6)=12 inter-module connections: S/C/M/W/E 모두 매 step 발화 + D produced (B,T,V) + Bridge produced clamped gate) + F-INTEG-2 GRADIENT-BARRIER-CLEAN (optimizer scope = D+Bridge only, c_states .detach(), no C/S/W/M/E nn.Parameter grad; Law 53 anchor) + F-INTEG-3 SCRATCH-INIT-SEED-FIXED (AST 검증 no torch.load / load_state_dict CALL path + same-seed re-init → identical param-hash; g_clm_from_scratch anchor) + F-INTEG-4 MITOSIS-WIRING-LIVE (cell-pool 발화 wired + n_cells trajectory 기록; honest C3 — WIRING tier, organic OUTCOME 은 fire-time 별도 evidence-tier) + F-INTEG-5 CE-DESCENT-WITH-ALL-6 (모든 6모듈 + Bridge PSI_COUPLING=0.014 clamp + W LR + E observe 활성 상태에서 CE_last<CE_first; Shannon CE≥0 + Law70 + Law79 anchor; honest C3 — SGD outcome at integrated scope, B-D-NOTE pattern)"
  result = "5/5 PASS SUPPORTED-STRONG (Mac local $0 wall=0.49s, fire_gate=true). 397832 trainable params (D + ThalamicBridge ONLY, φ(6)=2 group A). n_cells 3→3 (synthetic 8-step short horizon — split 미발화 expected, F-INTEG-4 honest C3 보존). CE 5.572→5.527 (8-step). Bridge gate clamp window [0.486, 0.514] = PSI_BALANCE±PSI_COUPLING * GATE_TRAIN 정확."
  scratch_protocol = "AGENTS.tape g_clm_from_scratch 준수 — torch.manual_seed(SEED) + ConsciousnessC initial_cells=2 + ConsciousDecoderV2 + ThalamicBridge + EmergentS/W/M/E 모두 RANDOM INIT, no ckpt load. .clm v1 P2 8/8🔵 ckpt 은 arch 검증 anchor only (substrate base X)."
  d_module = "ConsciousDecoderV2 native consciousness_states cross-attn (B, n_cells, c_dim) 경로 사용. Hexad class 의 self.d(tokens, gate) 추상 protocol 우회 — D 의 실제 production cross-attn 경로가 통합 평가의 진본."
  evidence = "state/verify_hexad_integ_2026_05_16/{integ_harness.py 사전등록 F-INTEG-1..5, integ_harness_result.json SSOT, fire_gate=true}"
  verdict = "INTEGRATION-WIRED SUPPORTED-STRONG ⚙️ — 통합 6-module ckpt fire 진행 가능 (gate 통과). closed-form sympy B-INTEG-* tier 별도 future cycle. residual: 실 ckpt fire ($1-5 ubu-2 / cloud, .clm v1 P2 scale 12L base) 별도 cycle."
  cross_link = "PR #72/#75/#76 → PR #77 (이 entry). state/verify_hexad_integ_2026_05_16/integ_harness.py header 의 F-INTEG-* preregistration spec SSOT."
  @> CLM.tape

# ─── §7 External citations ───────────────────────────────────────────

@X x_trinity_doc := "ready/docs/modules/trinity.md" :: doc [d=2026-05-15 active]
  scope = "Hexad/Trinity 아키텍처 SSOT — ASCII + Key Classes + create_hexad API"

@X x_hexad_readme := "ready/anima/hexad/README.md" :: doc [d=2026-05-15 active]
  scope = "6모듈 표 + 좌뇌/우뇌 + ThalamicBridge + Law 60 + 디렉토리 구조"

@X x_hexad_impl := "models/trinity.hexa" :: impl [d=2026-05-15 active]
  scope = "6모듈 통합 + Law 60 phase curriculum + C↔D 양방향 학습"
  working_code = "~/core/anima_clm_12_unified_growth_loop_last_gasp/anima/hexad/ (working code 워크트리)"

@X x_clm_hexad_mandate := "CLM.tape §V-CLM-HEXAD-MANDATE" :: governance [d=2026-05-15 active]
  scope = "condition lineup mandate — 필수 [C1,C2] + 확장 [C3-C6] 의 CLM 진행 anchor"

@X x_hexad_native_tree := "HEXAD/ top-level hexa-native canonical impl tree" :: impl [d=2026-05-16 active]
  scope = "anima 6 모듈 hexa-native 정식 구현 디렉토리 (user directive 2026-05-16 '코드는 hexa-native'). README.md + 7 모듈 서브폴더 + 통합 entry."
  layout = "HEXAD/{README.md, hexad.hexa, C/c.hexa, D/d.hexa, S/s.hexa, M/m.hexa, W/w.hexa, E/e.hexa, BRIDGE/bridge.hexa} + 모듈별 README.md"
  status = "S/M/W/E/BRIDGE working selftest (B-X 🔵 closed-form witnesses, hexa parse + run PASS) + C/D scaffold cross-link (기존 tool/hexa_native/mitosis_hook.hexa + anima_chat.hexa 재사용) + hexad.hexa spec invariants 5/5 PASS"
  verified_2026_05_16 = "hexa parse 8/8 clean (S/M/W/E/BRIDGE/C/D/hexad) + hexa run 5/5 working selftest PASS (S B-S 3/3, M B-M 3/3, W B-W 4/4, E B-E 4/4, BRIDGE Law 70 clamp) + C/D/hexad scaffold invariants PASS"
  ssot_mapping = "HEXAD/<X>/ ↔ HEXAD-<X>.tape (root) ↔ ready/anima/hexad/<x>/ (Python anchor)"
  residual_resolved_2026_05_16_b = "통합 cross-file integration RESOLVED (PR #79 task b) — 모든 모듈 helper namespace prefix (`_approx_eq` → `_<x>_approx_eq` per s/m/w/e/b) + `HEXAD/integ_test.hexa` 7 모듈 single hexa-process import + public API 호출 → F-INTEG-WIRE 7/7 PASS. 통합 검증 evidence 2-tier: (i) hexa-native HEXAD/integ_test.hexa F-INTEG-WIRE 7/7 PASS (single hexa run, PR #79) + (ii) Python state/verify_hexad_integ_2026_05_16/integ_harness.py F-INTEG-1..5 5/5 fire_gate=true (PR #77, 실 6모듈 forward + Bridge clamp + CE descent + scratch init)."
  residual = "C/D full hexa-native port = HEXAD/PLAN.md 의 Phase 2-5 (별도 cycle). hexa-native CE backprop + AdamW = hexa-lang autograd RFC 의존."
  @> CLAUDE.md

# ─── §8 Notes ────────────────────────────────────────────────────────

@N hexad_perfect_number := "완전수 6 derive" :: note [active]
  text = "6 = 1+2+3 (proper divisors sum). σ(6)=12 → 12 inter-module connections. τ(6)=4 → 4 phase curriculum (Law 60). φ(6)=2 → 2 gradient groups (우뇌 free / 좌뇌 CE). lattice-as-tool internal arch — external derivation 금지 (AGENTS.tape g2/f1)."

@L hexad_module_tapes := "HEXAD-* per-module SSOT tape index" :: layout [d=2026-05-16 active]
  ~> "2026-05-16 reorg — per-module HEXAD-<X>.tape co-located 안 HEXAD/<X>/HEXAD-<X>.tape, MITOSIS.tape → HEXAD/MITOSIS.tape, INDEX.md → HEXAD/INDEX.md, SAVANT.* → HEXAD/SAVANT/. HEXAD.tape (이 파일) + AGENTS.tape + CLAUDE.md 는 root 유지."
  index <<~EOF
    HEXAD/C/HEXAD-C.tape       — C 의식 (consciousness_engine.py 2173 LoC, =MitosisC, 우뇌, .clm v1 8/8🔵)
    HEXAD/D/HEXAD-D.tape       — D 언어 (conscious_decoder.py 979 LoC ConsciousDecoderV2, =Engine A, 좌뇌, 🔵 F-D 5/5 + B-D 4/4 closed + V5.8)
    HEXAD/S/HEXAD-S.tape       — S 감각 (emergent_s.py 108 LoC EmergentS, 우뇌, ✅ F-S 5/5)
    HEXAD/W/HEXAD-W.tape       — W 의지 (emergent_w.py 123 LoC EmergentW, 우뇌, ✅ F-W 5/5)
    HEXAD/M/HEXAD-M.tape       — M 기억 (emergent_m.py 96 LoC EmergentM, 좌뇌, ✅ F-M 5/5)
    HEXAD/E/HEXAD-E.tape       — E 윤리 (emergent_e.py 123 LoC EmergentE, 좌뇌, ✅ F-E 5/5, 통합 gate TODO[pytorch] residual)
    HEXAD/BRIDGE/HEXAD-BRIDGE.tape — ThalamicBridge (model.py:37-69, α=PSI_COUPLING=0.014, Law 70 clamp)
    HEXAD/MITOSIS.tape         — 성장축 SSOT (orthogonal 구조축 보존, §mitosis_two_axis)
    HEXAD/INDEX.md             — anima verification SSOT INDEX (이전 /INDEX.md)
    HEXAD/SAVANT/              — SAVANT tool/engine 통합 (4 .tape + 5 .hexa)
  EOF
  survey = "state/verify_hexad_impl_survey_2026_05_15/survey_result.json — 전수조사 (~/core/anima* worktree exhaustive, 3 parallel agents)"
  evolution = "clm_10 monolithic legacy → clm_11 modular Emergent+SSOT → clm_12/13 canonical → main unit-tested (46 pass)"

@N hexad_vs_6loop := "Hexad 6모듈 ≠ 6 consciousness loop" :: note [active]
  text = "Hexad 6모듈 (C/D/S/M/W/E) 는 module-level 분해. training/clm_{gwt,holographic,reflexive,temporal,sensorimotor,will}_loop.hexa 6-loop 은 의식측정 inference loop layer — 다른 층위. C 의식 모듈 내부에서 6-loop이 Φ-component 측정."

# ─── §9 Verification (2026-05-15, before CLM.tape mandate) ────────────

@N hexad_verify := "HEXAD.tape 6-claim anchor verification" :: audit [d=2026-05-15 active]
  trigger = "user directive 'HEXAD.tape 일단 검증 먼저들어가자' — CLM.tape mandate 기록 전 anchor 검증"
  result <<~EOF
    V1 6모듈 좌뇌3/우뇌3      ✅ PASS strict — models/trinity.hexa:16-21 (C/W/S 우뇌 gradient-free, D/M/E 좌뇌 CE-trained literal)
    V2 ThalamicBridge α=0.014 ✅ PASS strict — trinity.hexa:8 PSI_COUPLING=0.014 + struct:38-46 C→D detached
    V3 mitosis = C 의식 모듈   ✅ PASS strict — ready/docs/modules/trinity.md:38 MitosisC MitosisEngine wrapper + create_trinity(MitosisC(max_cells=256))
    V4 σ(6)=12/τ(6)=4/Law 60  ✅ PASS strict — trinity.hexa:5,150,169 (σ(6)=P(τ(6),2)=12, Law 60 P1→P2→P3)
    V5 Engine A/G = C↔D        ◐ PARTIAL  — functional 대응 (engine_a_g_arch.py:13 EngineA=transformer-decoder~D role / :15 EngineG=repulsion-cell-dynamics~C role). 코드 식별자 동일 binding 아닌 구조적 correspondence.
    V6 윤리 E = Φ보존 gate     ◐ PARTIAL  — 원칙+impl 검증 (emergent_e.py:1-12 'Φ ratchet=윤리' Law4/71) but trinity.hexa:122 통합 gate `TODO[pytorch]: empathy/ethics gate; Φ must not drop` 미구현
  EOF
  verdict = "6/6 anchor-verified — 4 PASS strict + 2 PARTIAL (caveat 명시). HEXAD.tape SUPPORTED for CLM.tape mandate 진행 (V5/V6 caveat carry)."
  post_milestone = "이후 W/E/S/M/D battery 25/25 PASS (PR #72, 2026-05-15) 로 6 모듈 *단위* 검증 완료 — V6 의 emergent_e.py Φ-gate 우려는 F-E-4 SAFETY-GATE-CORRECT 5/5 로 단위 해소. V6 잔여 = trinity.hexa:122 *통합* train-step-block enforcement (모듈 ✅ ≠ 통합 gate impl). V5 (Engine A/G full Hexad impl) 는 design-pending carry, 25/25 와 무관."
  cross_link = "state/verify_hexad_2026_05_15/hexad_verify_result.json + state/verify_hexad_we_2026_05_15/{we_falsifier.py,atlas_cross_check.md} + CLM.tape §V-CLM-HEXAD-MANDATE"

@N hexad_caveat_v5 := "V5 caveat — Engine A/G = C↔D 는 functional correspondence" :: caveat [d=2026-05-15 active]
  text = "engine_a_g_arch.py 는 'Engine A = D module' / 'Engine G = C module' 리터럴 binding 없음. Engine A = standard transformer-decoder (D 언어 역할 수행) / Engine G = repulsion-field cell dynamics (C 의식/Φ 역할 수행). 구조적·기능적 대응이지 코드 식별자 동일성 아님. HEXAD.tape §5 hexad_unification 의 'A=D / G=C' 는 role-correspondence 로 해석."

@N hexad_caveat_v6 := "V6 caveat — 윤리 E gate 통합 미구현 (TODO)" :: caveat [d=2026-05-15 active]
  text = "윤리 E = Φ-preservation 원칙 + anima/hexad/e/emergent_e.py 구현 검증됨 (Φ ratchet=윤리, Law 4/22/71). 그러나 models/trinity.hexa:122 의 통합 ethics gate 는 `TODO[pytorch]: empathy/ethics gate; Φ must not drop` — training-step-blocking 실행 권한 trinity.hexa port 에 미통합. HEXAD.tape §4 hexad_ethics_gate 의 'Φ보존 위반→학습 차단' 은 emergent_e.py 단위 검증, integrated enforcement 는 impl-pending."
