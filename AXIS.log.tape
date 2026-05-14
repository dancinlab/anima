#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# .tape v1.2 — grammar primer (cold-read by any LLM / agent / human)
# ══════════════════════════════════════════════════════════════════════
# Form: each entry is `@<type> <id> := "<subject>" :: <kind> [<grades>]`
#       optionally followed by body lines (2-space indent) — key=value,
#       edges (<- -> => …), or quoted prose.
#
# ENTRY TYPES (17):
#   Runtime (10): @S session  @U user  @A assistant  @T tool-call  @R result
#                 @H hook  @D decision  @K cost  @P provider  @? anomaly
#   Foundation:   @I identity-claim
#   Declarative:  @X external-citation  @F forbidden-pattern  @N note
#                 @C config  @L layout  @V spec-version
#
# EDGES (12, on body lines, 2-space indent):
#   Causal:     <- caused-by   -> triggers   == continues
#               ~> supersedes  !! aborts     |> verified-by
#   Effect:     => produces (followed by quoted natural-language)
#   Structural: <: specializes  :> generalizes  ?> soft-depends
#               !> conflicts-with  @> projects-to (e.g. @> AGENTS.md)
#
# GRADE TAGS (in [...] on entry header):
#   Delivery:   ok · err · denied · cancelled · partial · superseded
#   Governance: required · recommended · optional · draft · active · deprecated
#   Scoped:     allow:<x> · deny:<x>
#   Time/index: T<n> (turn)  N<n> (wall-sec)  d=<YYYY-MM-DD>
#
# PAYLOAD SYNTAX (body lines):
#   key = "value"           single-line string
#   key = [a, b, c]         array literal
#   key <<~EOF              heredoc (multi-line; ends with EOF on own line)
#     multi-line text
#   EOF
#   "see [@x1] §3"          inline citation by entry id
#   `cmd or path`           backtick code-span (inline only)
#
# Full spec: ~/core/tape/spec/tape.md (or github.com/dancinlab/tape)
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
# AXIS.log.tape — append-only event history (v1.2 split)
# Sibling: AXIS.tape (architecture-current, editable)
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# §Log — entries chronological, oldest first.

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

