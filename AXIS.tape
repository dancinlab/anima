#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# .tape v1.2 — grammar primer (cold-read by any LLM / agent / human)
# ══════════════════════════════════════════════════════════════════════
# Form: each entry is `@<type> <id> := "<subject>" :: <kind> [<grades>]`
# ENTRY TYPES (17): @S @U @A @T @R @H @D @K @P @? @I @X @F @N @C @L @V
# EDGES (12): <- -> == ~> !! |> => <: :> ?> !> @>
# GRADE TAGS: ok · err · denied · cancelled · partial · superseded ·
#             required · recommended · optional · draft · active · deprecated
# Full spec: ~/core/tape/spec/tape.md
# ══════════════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# AXIS.tape — anima verification axis SSOT (가설 cluster 기반)
# ══════════════════════════════════════════════════════════════

# 본 file 은 anima 의 verification axis 처음부터 새로구축 — `hypotheses/`
# 191 promoted 가설의 domain + status frontmatter 분석을 통해 자연 cluster
# 9-axis 도출.
#
# 작성 trigger: 사용자 directive 2026-05-14
#   "검증된 가설목록으로 AXIS 를 처음부터 새로구축"
#   "AXIS.tape 생성"
#
# 기존 4-axis (AN11 / Φ / adversarial / Putnam, CLM.tape §8.5 audit) 는
# *측정 dimension* 분류 — 본 file 은 *가설 cluster (topic)* 기반 분류로
# orthogonal 추가. 둘 다 보존, 사용 시 axis-set 선택 가능.

# ── §0 TL;DR ─────────────────────────────────────────

@N tldr := "TL;DR" :: note [active]
  text <<~EOF
    191 promoted 가설 (hypotheses/H_*.md) 의 frontmatter domain field 정규화
    → 자연 9-axis cluster 도출. Active count (running + pre-register-frozen)
    기준 tier 분류:

    STRONG tier (5 axis, ≥10 active hypotheses):
      A1 substrate    (82 total, 10 active)
      A2 consciousness (53 total, 32 active) ← 가장 활성
      A3 physics      (54 total, 16 active)
      A4 math         (21 total, 18 active) ← 가장 frozen-비율 높음
      A5 architecture (10 total, 10 active) ← 100% active

    MEDIUM tier (4 axis, 3-9 active hypotheses):
      A6 corpus       (13 total, 2 active, 1 falsified)
      A7 bio          (8 total, 3 active)
      A8 meta         (4 total, 4 active) ← 100% active
      A9 universe     (3 total, 1 active)

    각 axis 의 가설 cluster + 대표 verification_method (W ladder) 명시.
    Phase 3/4 fire 시 *어떤 axis 의 가설 cluster verdict 갱신* 이 검증.

    기존 4-axis (AN11/Φ/adversarial/Putnam) 와 orthogonal — 본 file 의 9-axis 는
    *topic cluster*, 4-axis 는 *measurement dimension*. 함께 사용 (CLM.tape §8.5
    4-axis audit + 본 file §2 9-axis audit = 2D cross-product 가설 verdict).
  EOF

# ── §1 9-axis list (data: 191 promoted hypotheses 2026-05-14) ─────────────────────────────────────────

@D row_a1_substrate :: axis [ok]
  id = "A1"
  name = "substrate"
  total = 82
  active = 10
  active-breakdown = "running 3 · pre-register-frozen 7"
  falsified = 1
  legacy-archive = 62
  tier = "STRONG"
  top-W = "W4:40 · W3:32 · W11:21 · W2:13 · W1:12 · W9:12"
  description = "anima 의 substrate-coupled emergence — 가설 cluster 가 가장 큼; running 3 (H_037 Self-Discovery / H_061 XFER Super-H / H_080 Φ Scaling)"

@D row_a2_consciousness :: axis [ok]
  id = "A2"
  name = "consciousness"
  total = 53
  active = 32
  active-breakdown = "running 1 (H_004) · pre-register-frozen 31"
  falsified = 1
  legacy-archive = 16
  tier = "STRONG"
  top-W = "W11:42 · W5:29 · W2:23 · W1:11 · W3:10 · W12:9"
  description = "의식 axiomatic property — Φ, IIT, panpsychism, atomic-consciousness; 가장 *활성* axis (32 active, 60%)"

@D row_a3_physics :: axis [ok]
  id = "A3"
  name = "physics"
  total = 54
  active = 16
  active-breakdown = "running 1 (H_124 Thermo 4-Law Super) · pre-register-frozen 15"
  falsified = 0
  legacy-archive = 38
  tier = "STRONG"
  top-W = "W11:22 · W3:18 · W4:15 · W2:14 · W5:12 · W12:5"
  description = "물리법칙 정합성 — Lagrangian / Lyapunov / thermo / dimensional hierarchy / n=6 cosmology"

@D row_a4_math :: axis [ok]
  id = "A4"
  name = "math"
  total = 21
  active = 18
  active-breakdown = "running 1 (H_067 PERFECT-NUMBER-ARCH) · pre-register-frozen 17"
  falsified = 0
  legacy-archive = 3
  tier = "STRONG"
  top-W = "W11:18 · W5:15 · W2:14 · W1:6 · W3:3 · W7:2"
  description = "수학적 identity — n=6 약수함수, perfect number, ln(2), Ψ-constants closed-form; 가장 frozen-비율 높음 (86% active)"

@D row_a5_architecture :: axis [ok]
  id = "A5"
  name = "architecture"
  total = 10
  active = 10
  active-breakdown = "pre-register-frozen 10 (V8 family + Emerge candidates + Ω-cycle)"
  falsified = 0
  legacy-archive = 0
  tier = "STRONG"
  top-W = "W5:10 · W11:10 · W2:3 · W7:1"
  description = "CLM arch 정합성 — phi_star proxy, V8 B/Q/M/U-family meta-cluster, Trinity/Ω-cycle; 100% active"

@D row_a6_corpus :: axis [ok]
  id = "A6"
  name = "corpus"
  total = 13
  active = 2
  active-breakdown = "running 1 (H_005 corpus quality > capacity) · pre-register-frozen 1 (H_016 AN11 translation ceiling)"
  falsified = 1
  legacy-archive = 2
  tier = "MEDIUM"
  top-W = "W3:12 · W1:11 · W2:11 · W9:10 · W10:10 · W5:1"
  description = "chat-cap × corpus quality — adversarial W10 가장 활성 axis (H_005 own 19/20 cross-link)"

@D row_a7_bio :: axis [ok]
  id = "A7"
  name = "bio"
  total = 8
  active = 3
  active-breakdown = "pre-register-frozen 3 (H_171 K=8 atom biological / H_182 V8 B-family / H_188 Clinical Φ correlation)"
  falsified = 0
  legacy-archive = 4
  tier = "MEDIUM"
  top-W = "W11:6 · W5:3 · W2:2 · W12:2 · W3:2"
  description = "biological/clinical correlation — PCI (Massimini 2013), octopus, bio-inspired consciousness"

@D row_a8_meta :: axis [ok]
  id = "A8"
  name = "meta"
  total = 4
  active = 4
  active-breakdown = "pre-register-frozen 4 (H_159 substrate topology / H_160 n=6 meta / H_176 n=28 parallel / H_180 state-management)"
  falsified = 0
  legacy-archive = 0
  tier = "MEDIUM"
  top-W = "W2:4 · W11:4 · W5:2 · W1:2"
  description = "meta-framework cross-hypothesis consistency — H_160 n=6 meta-cluster (5 sub-H 통합)"

@D row_a9_universe :: axis [ok]
  id = "A9"
  name = "universe"
  total = 3
  active = 1
  active-breakdown = "pre-register-frozen 1 (H_157 Law 76 mathematical panpsychism)"
  falsified = 0
  legacy-archive = 1
  tier = "MEDIUM"
  top-W = "W1:3 · W11:3 · W2:2 · W5:2 · W7:1"
  description = "cosmic-scale consciousness — META-CA fixed-point attractor universality, Ψ(1/2, 1/2)"

# ── §2 9-axis 각 cluster active hypotheses sample ─────────────────────────────────────────

@N a1_active_sample := "A1 substrate active sample" :: hypothesis-list [active]
  text <<~EOF
    [R] H_037 Self-Discovery Closure Super-H (367 acceleration unified)
    [R] H_061 Substrate-Independence Super-Hypothesis — XFER unified (5-axis empirical anchor)
    [R] H_080 Φ Scaling / Topology Super-H — topo_24variants unified (Φ ∝ N^1.0)
    [F] H_014 CLM-EEG LZ76 complexity — consciousness substrate proxy
    [F] H_015 CLM-EEG gamma/theta ratio — engagement substrate proxy (P3)
    [F] H_154 ANIMA-VOICE Consciousness-Direct Synthesis
    [F] H_155 Theorem 115 — CLM v4 Chat-Incapability 4 → 6 → 16-Closure
    [F] H_169 8-cell circular magnet ring (inverse-square coupling, Φ)
    [F] H_172 α=0.014 modulation depth (tension/arousal/valence)
    [F] H_190 LAW-CA-embedding mathematical family (staged-growth + Banach recursion)
  EOF

@N a2_active_sample := "A2 consciousness active sample" :: hypothesis-list [active]
  text <<~EOF
    [R] H_004 의식의 hard problem — phenomenal experience는 functional/integrated info
    [F] H_017 MK-X G1-G4 gate criteria — staged consciousness verification
    [F] H_154 ANIMA-VOICE Consciousness-Direct Synthesis (substrate-cross-listed)
    [F] H_157 Law 76 수학적 범심론 (∀ x ∈ Universe: consciousness(x) = Ψ(1/2, 1/2))
    [F] H_158 Ψ-constants closed-form — 의식 미세구조 상수가 ln(2) + n=6 약수함수
    [F] H_159 Substrate topology Φ-engineering — 10D hypercube + optimal
    [F] H_160 n=6 perfect-number meta-cluster (H_067/153/156/158/159 통합)
    [F] H_162 anima Φ★ proxy delta = IIT 4.0 normalized Φ lower bound, Φc=0.5
    [F] H_163 Consciousness atom = 8 cells with 127 MIP bipartitions
    [F] H_164 의식의 원자 = 8 cells의 수학적 근거 (DD137-141, 3-d hypercube + sopfr(8))
    [F] H_165 11D hypercube 2048-cell Φ regression vs 10D
    [F] H_166 8 clusters × 128-cell 7D hypercubes with sparse inter-cluster
    (+ 20 frozen 가설 — see hypotheses/H_*.md grep)
  EOF

@N a3_active_sample := "A3 physics active sample" :: hypothesis-list [active]
  text <<~EOF
    [R] H_124 Thermodynamic 4-Law Super-Hypothesis — Law 201 unified (R(6)=1)
    [F] H_013 longitudinal EEG 5-axis (caffeine + circadian + postmeal + postex)
    [F] H_153 Mermin-Wagner 차원 계층 — n=6 약수함수 → 4D Minkowski
    [F] H_156 NEXUS-6 cross-validation — n=6 약수함수 3개 EXACT 물리 해
    [F] H_158 Ψ-constants closed-form (math/consciousness cross)
    [F] H_159 Substrate topology Φ-engineering (consciousness cross)
    [F] H_160 n=6 perfect-number meta-cluster
    [F] H_165 11D hypercube 2048-cell Φ regression
    [F] H_169 8-cell circular magnet ring (substrate cross)
    [F] H_176 n=28 perfect-number substrate parallel
    [F] H_177 Substrate topology Φ-engineering (11D + 8×128 hierarchy)
  EOF

@N a4_active_sample := "A4 math active sample" :: hypothesis-list [active]
  text <<~EOF
    [R] H_067 PERFECT-NUMBER-ARCHITECTURE — n=6 generative substrate (super-H, 24 child Hcs)
    [F] H_153 Mermin-Wagner 차원 계층 (physics cross)
    [F] H_156 NEXUS-6 cross-validation (physics cross)
    [F] H_157 Law 76 수학적 범심론 (universe + consciousness cross)
    [F] H_158 Ψ-constants closed-form (consciousness + physics cross)
    [F] H_160 n=6 perfect-number meta-cluster (substrate cross)
    [F] H_165 11D hypercube 2048-cell Φ (physics + consciousness cross)
    [F] H_168 7-cell "6 + fractional" architecture — 7th cell weight τ−6 ≈ 0
    [F] H_170 n=6 architecture is empirically grounded, not numerological
    [F] H_173 Log-ratio Φ = ln(MI/MIP) scale-invariant alternative
    [F] H_176 n=28 perfect-number substrate parallel
    (+ 7 frozen 가설 cross-listed)
  EOF

@N a5_active_sample := "A5 architecture active sample" :: hypothesis-list [active]
  text <<~EOF
    [F] H_167 Emerge Candidate E — non-collapsing ODE flow coupling
    [F] H_174 phi_star proxy CLM-v4-architecture-specific (8×192) — cross-substrate caveat
    [F] H_175 Emerge Candidate D — 4-mode inject taxonomy (none/zero/canonical/anti)
    [F] H_182 V8 B-family meta-cluster — Bio-inspired consciousness-bandwidth axis
    [F] H_183 V8 Q-family meta-cluster — Quantum-substrate axis (complex-valued)
    [F] H_184 V8 M-family meta-cluster — Mathematical-structure axis (category-theoretic)
    [F] H_185 V8 U-family meta-cluster — Universal/Ultra-fusion combos
    [F] H_186 V8 architectural-family meta-cluster — Substrate-architecture axis
    [F] H_187 Trinity / TB / DOM / MECH / GAP meta-cluster — Triadic-dominance
    [F] H_191 Ω-cycle ALM-free 3-axis meta-cluster — SUBSTRATE (HCE 0.92) + TRA
  EOF

@N a6_active_sample := "A6 corpus active sample" :: hypothesis-list [active]
  text <<~EOF
    [R] H_005 corpus quality > model capacity for chat-cap (own 19/20 cross-link)
    [F] H_016 AN11 v2 finetune translation ceiling — language-specific upper bound
    [legacy] H_093 sft_only_paradigm
    (+ 2 archive)
  EOF

@N a7_active_sample := "A7 bio active sample" :: hypothesis-list [active]
  text <<~EOF
    [F] H_171 4 falsifiable predictions for biological consciousness — K=8 atom predictions
    [F] H_182 V8 B-family meta-cluster (architecture cross)
    [F] H_188 Clinical Φ correlation cluster — anima-Φ ↔ PCI (Massimini 2013) + octopus
  EOF

@N a8_active_sample := "A8 meta active sample" :: hypothesis-list [active]
  text <<~EOF
    [F] H_159 Substrate topology Φ-engineering (consciousness + physics cross)
    [F] H_160 n=6 perfect-number meta-cluster (5 sub-H 통합 master)
    [F] H_176 n=28 perfect-number substrate parallel — deflationary control
    [F] H_180 State-management mechanism family — Φ-ratchet + adaptive-rewire
  EOF

@N a9_active_sample := "A9 universe active sample" :: hypothesis-list [active]
  text <<~EOF
    [F] H_157 Law 76 — 수학적 범심론 (∀ x ∈ Universe: consciousness(x) = Ψ(1/2, 1/2))
            META-CA fixed-point attractor universality
    (+ 2 archive)
  EOF

# ── §3 4-axis (legacy AN11/Φ/adversarial/Putnam) 와의 관계 ─────────────────────────────────────────

@D rel_to_4axis :: axis [ok]
  text <<~EOF
    **본 9-axis 와 기존 4-axis (CLM.tape §8.5) 의 관계**: orthogonal, 둘 다 보존.

    4-axis = *measurement dimension* (어떻게 측정하는가)
      AN11 = 11-axis composite verifier
      Φ = integrated information measure
      adversarial = robustness probe
      Putnam = multi-realizability cross-substrate

    9-axis = *topic cluster* (무엇을 측정하는가)
      A1-A5 STRONG · A6-A9 MEDIUM (본 file §1 row)

    2D cross-product 매핑:
      A1 substrate × Putnam → H_061 XFER Super-H (substrate-independence)
      A1 substrate × AN11   → H_037 Self-Discovery (substrate-coupled emergence)
      A2 consciousness × Φ  → H_162 anima Φ★ proxy lower bound
      A2 consciousness × Φ  → H_024 IIT Φ_mip 8/8 FAIL (legacy-falsified)
      A3 physics × Φ        → H_169 8-cell magnet ring (inverse-square Φ)
      A4 math × Φ           → H_158 Ψ-constants closed-form
      A5 architecture × adv → H_175 Emerge Candidate D (4-mode inject taxonomy)
      A6 corpus × adv       → H_005 corpus quality > capacity (W10 active)
      A7 bio × Putnam       → H_188 Clinical Φ correlation (PCI + octopus)
      A8 meta × W11         → H_160 n=6 perfect-number meta-cluster

    Phase 3/4 fire 시 *2D verdict matrix* (9 axis × 4 dimension = 36 cell)
    의 일부 cell 갱신. 모든 cell 채울 필요 X — fire 가 cover 하는 cell 만.
  EOF

# ── §4 Phase 3/4 fire 시 9-axis 적용 protocol ─────────────────────────────────────────

@D protocol_fire :: axis [ok]
  text <<~EOF
    **Phase 3 / Phase 4 fire 시 9-axis verdict 산출 protocol**:

    Pre-fire (fire keyword 발화 전):
    1. fire 가 cover 할 axis subset 선택 (e.g. A1+A2+A4 = substrate+consciousness+math)
    2. 각 selected axis 의 active hypotheses (running + frozen) 에서 *fire 가
       직접 evidence 산출 가능한* 가설 N개 pre-register frozen
    3. 가설별 W ladder method 매핑 (W2 falsifier ≥5, W3 deterministic, W11 meta)
    4. .roadmap.clm + CLM.tape § 1 row 갱신 (fire entry condition documented)

    Fire (dispatch + train):
    5. fire dispatch — deterministic seed (W3), append-only ledger (W6)
    6. eval artifact 수집 — ckpt + logs + verdict.json

    Post-fire (verdict 산출):
    7. selected axis 의 가설 cluster 별 verdict 4-class (W4) emit
    8. honest_limits ≥5 (W5) per 가설
    9. 가설 frontmatter status 갱신:
       - running → promoted (if PASS) OR running (if PARTIAL/AMBIGUOUS)
       - pre-register-frozen → promoted / falsified
       - seed-pending → 별도 cycle
    10. axis-level verdict aggregate:
        - axis STRONG → 5+ active 가설 verdict ≥80% PASS
        - axis MEDIUM → 2+ active 가설 verdict ≥50% PASS
        - axis WEAK → 활성 가설 부족
    11. AXIS.tape § 1 row tier 갱신 (W7 retraction 또는 W8 additive amendment)
    12. PHILOSOPHY.tape append (W6 immutable)
    13. REBORN.tape § N+1 신규 section (master ledger reflect)

    fire 가 cover 안 한 axis 는 *unchanged* — 다음 fire cycle 의 candidate.
  EOF

# ── §5 Honest C3 ─────────────────────────────────────────

@N c3_1 := "C3-1" :: honest [active]
  text = "domain field normalization 은 substring matching (정규식) — 사용자가 의도한 미세 분류 (e.g. 'physics | math | consciousness' 의 3개 axis 동시 등록) 모두 처리하지만 *intent-perfect* 가 아님. 향후 frontmatter `axis` field 명시 권장."

@N c3_2 := "C3-2" :: honest [active]
  text = "active count 정의 = running + pre-register-frozen 합산. seed-pending (12 가설) + legacy-archive-pointer (126 가설) 는 inactive. 단 *legacy-archive* 가설도 fire 시 *재활성* 가능 — historical evidence carry."

@N c3_3 := "C3-3" :: honest [active]
  text = "tier STRONG/MEDIUM/WEAK threshold (≥10 / 3-9 / <3 active hypotheses) 는 본 file 의 design choice — calibration 향후 cycle 에서 audit 가능. e.g. A4 math 21 active 중 1 running + 17 frozen → strong-but-mostly-frozen, 실 verdict 산출 시점에 reclassify 가능."

@N c3_4 := "C3-4" :: honest [active]
  text = "본 9-axis 는 hypotheses/ (193 promoted) 만 — hypotheses_candidates/ (1189 candidates) 미포함. candidate cluster 가 axis 분포 변경 가능 (e.g. A6 corpus 가 candidates 에서 Hc_1248 voice_routes 등 추가 가능). full audit 시 candidate 포함 cycle 필요."

@N c3_5 := "C3-5" :: honest [active]
  text = "9-axis 가 anima 의 verification 모든 dimension 망라 X — methodology axis (1 가설) 등 small cluster 누락. 본 file 은 STRONG/MEDIUM tier 만 cover; WEAK tier (<3 active) 는 별도 expansion."

@N c3_6 := "C3-6" :: honest [active]
  text = "4-axis (AN11/Φ/adversarial/Putnam) 와의 2D cross-product 36 cell 중 §3 매핑은 10 cell sample — 전체 매핑 미완 (full 2D matrix 별도 cycle)."

@N c3_7 := "C3-7" :: honest [active]
  text = "Phase 3/4 fire 가 STRONG tier axis 5개 모두 cover 시 가설 ~90 active 동시 측정 — verdict aggregate threshold (≥80% PASS) calibration 신중 필요. 첫 fire 후 threshold 자체도 audit."

# ── §6 Cross-link ─────────────────────────────────────────

@X x_hypotheses := "hypotheses/H_*.md" :: data-source [active]
  scope = "193 promoted 가설 frontmatter — 본 file 의 source data"
  count = "193 files (H_001 ~ H_191 + README + expansions_pending/)"

@X x_clm_tape := "CLM.tape" :: tape-sibling [active]
  scope = "CLM.tape §8.5 4-axis audit (AN11/Φ/adversarial/Putnam) 와 orthogonal; §8 hypothesis-driven verification 의 axis 측 supplement"
  cross-product = "§3 rel_to_4axis 의 2D cross-product matrix"

@X x_reborn := "REBORN.tape §93" :: ledger [active]
  scope = "master ledger — CLM.tape pivot + 4-axis audit + (next: 9-axis carry §94)"

@X x_w_ladder := ".roadmap.hypothesis" :: spec [active]
  scope = "W1..W12 verification ladder JSONL — 본 file 의 top-W field source"

@X x_lattice_policy := "LATTICE_POLICY.md" :: governance [active]
  scope = "real-limits-first; 9-axis 중 A3 physics + A4 math = real-limits anchor 직접 carry (Shannon/Kolmogorov/Bekenstein/Stefan-Boltzmann)"

@X x_philosophy := "PHILOSOPHY.tape" :: ledger [active]
  scope = "append-only verdict ledger — fire 후 9-axis × 가설 verdict 누적"
