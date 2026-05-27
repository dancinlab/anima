#!/usr/bin/env tape
# NEXUS.tape — anima intra-project reuse lattice (SSOT)
# Canonical structured SSOT of the cross-module reuse graph.
# Migrated from HEXAD/INDEX.md (which is now a pointer to this file).
# Governance: commons @D g67 (universal-inherited — not duplicated in project.tape).
# anima idiom: module/law -> primitive (engine · transfer fn · falsifier battery · Phi form) -> module.
#   (vs demiurge's domain -> primitive -> domain.)
# Substrate: discovery = atlas (verified atoms) + sibling-module INDEX/README cross-arc anchors.
#   This file aggregates them into ONE reuse graph (junk-drawer re-search avoidance, HEXAD/TREE.md).
# Scope: intra-project ONLY — never link modules across repos (@D g67, intra-anima only).
# Verify tier = verdict-tier (BLUE SUPPORTED-FORMAL / GREEN SUPPORTED). Candidate edges marked unverified.
#
# Block legend:
#   @I nexus              — identity (kind · scope)
#   @X e<n> :: reuse-edge       — a VERIFIED reuse edge (one provides -> one reused_by)
#   @X p<n> :: provides         — a module's provides[] registry (primitives it offers)
#   @X c<n> :: reuse-candidate  — a conceptual edge, no verified reuse evidence yet (proposed)
#   @N n<n> :: note             — usage protocol / cross-repo guard / human ASCII graph view
# Block type is @X (External-citation / declarative, one of the closed 17-type
# alphabet @S@U@A@T@R@H@D@K@P@?@I@X@F@N@C@L@V). Body keys are free-form (the
# @D-only do/dont field restriction does NOT apply to @X). Lints clean v1.2.

@V := "tape" :: spec [active]
  version = "1.2"

@I nexus := "anima intra-project reuse lattice" :: identity [active]
  kind  = "cross-module reuse graph — verified primitives + discoveries shared between sibling modules"
  idiom = "module/law -> primitive (engine · transfer fn · falsifier battery · Phi form) -> module"
  scope = "intra-project ONLY — never link modules across repos (@D g67, intra-anima only)"
  ssot  = "this file (NEXUS.tape) · HEXAD/INDEX.md is a pointer to it"
  governs = "commons @D g67 (universal-inherited)"

# ── 1. VERIFIED reuse edges (provides -> primitive -> reused_by, with evidence) ──
# REAL edge = 5 — all BLUE SUPPORTED-FORMAL providers, repo-internal evidence rows substantiate.

@X e1 := "central battery -> 9 modules" :: reuse-edge [tier-blue active]
  provides  = "central (verification substrate)"
  primitive = "blue_falsifier.py (verify_hexad_blue, sympy closed-form)"
  reused_by = "BRIDGE · D · E · M · MITOSIS · CHAT · CHECK · LEGO · META_FP"
  tier      = "BLUE SUPPORTED-FORMAL"
  evidence  = "each module README cites central battery (state/verify_hexad_blue_2026_05_15/, sha c93e160a8a376a94 invariant); LEGO INDEX.md engine-SSOT notes 0-line-diff"

@X e2 := "META_FP psi form -> NEUROMORPHIC/LOIHI/LEGO/166" :: reuse-edge [tier-blue active]
  provides  = "META_FP (section 112)"
  primitive = "psi(c) = (1+c)/2 Pi_half meta-fixed-point form"
  reused_by = "NEUROMORPHIC (Psi-C1) · LOIHI · LEGO (Psi-C1 = section 112 META_FP instance) · section 166 training objective"
  tier      = "BLUE SUPPORTED-FORMAL"
  evidence  = "HEXAD/META_FP/README.md; LEGO INDEX.md cross-arc 'Psi-C1 = section 112 META_FP(Pi_half) instance'; NEUROMORPHIC README.md Psi = section 110 Psi-C1"

@X e3 := "TENSION-LINK Noether step -> TENSION-TRAIN" :: reuse-edge [tier-blue active]
  provides  = "TENSION-LINK"
  primitive = "tension_link_step.hexa (online backprop-free spine + n6 Noether gate sigma·phi = n·tau = 24)"
  reused_by = "TENSION-TRAIN (5 hexa file carry: step/causal/quantum_rho/second_order/bench)"
  tier      = "BLUE SUPPORTED-FORMAL"
  evidence  = "HEXAD/TENSION-TRAIN/README.md section 0/section 1 — 'past TENSION-LINK training full-survey -> TENSION-TRAIN consolidation'"

@X e4 := "LEGO engine lib -> 131/135/137" :: reuse-edge [tier-blue active]
  provides  = "LEGO (section 129)"
  primitive = "lego_engine.py canonical lib (LIFNet · spike_rate_vec · psi_c1 · variance_decomposition)"
  reused_by = "section 131 (first canonical-lib import) · section 135 · section 137 probes"
  tier      = "BLUE SUPPORTED-FORMAL"
  evidence  = "HEXAD/LEGO/INDEX.md arc-cycles (section 129 lib promote -> section 131 'first canonical-lib import')"

@X e5 := "C phi-measure -> IIT4/CHAT" :: reuse-edge [tier-blue active]
  provides  = "C (consciousness)"
  primitive = "c_measure_phi / phi_spatial (RFC 036, byte-equal Phi)"
  reused_by = "IIT4 · CHAT"
  tier      = "BLUE SUPPORTED-FORMAL"
  evidence  = "HEXAD/INDEX.md section C F-C-PORT-3 'c_measure_phi -> RFC 036 phi_spatial byte-equal'; HEXAD/CHAT/README.md"

# ── 2. provides[] registry (per-module offered primitives) ──

@X p1 := "central provides" :: provides [active]
  module     = "central"
  primitives = "blue_falsifier.py BLUE battery · we_falsifier.py · integ_harness.py (verification substrate SSOT)"

@X p2 := "META_FP provides" :: provides [active]
  module     = "META_FP"
  primitives = "psi(c)=(1+c)/2 Pi_half form · orthogonality anchor (cos=0) · (mean Psi-0.5)^2 mean-anchor training signal"

@X p3 := "TENSION-LINK provides" :: provides [active]
  module     = "TENSION-LINK"
  primitives = "tension_link_step.hexa n6 Noether gate · 5-channel meta-telepathy transfer form"

@X p4 := "LEGO provides" :: provides [active]
  module     = "LEGO"
  primitives = "lego_engine.py/.hexa (LIFNet · psi_c1 · spike_rate_vec · variance_decomposition)"

@X p5 := "C provides" :: provides [active]
  module     = "C (consciousness)"
  primitives = "c_measure_phi / phi_spatial (RFC 036) · MitosisC 12-faction Phi engine"

@X p6 := "MITOSIS provides" :: provides [active]
  module     = "MITOSIS"
  primitives = "mitosis_hook.hexa D4a (split/merge · cell-count conservation) · B-MITOSIS 5/5"

@X p7 := "BRIDGE provides" :: provides [active]
  module     = "BRIDGE"
  primitives = "Law-70 clamp g(raw)=Psi+clip(raw-Psi, +/-alpha) transfer fn (G->A main link)"

@X p8 := "IIT4 provides" :: provides [active]
  module     = "IIT4"
  primitives = "bit-primitive shim (-> hexa-lang stdlib/math/bitops, #540) · exclusion/cocompute measure"

# ── 3. candidate edges (unverified — honestly registered as candidates only) ──
# g67 dont: edge omission / fabrication forbidden. No closed-form evidence row yet.

@X c1 := "MITOSIS mitosis_hook -> C/CHAT" :: reuse-candidate [proposed draft]
  provider  = "MITOSIS"
  primitive = "mitosis_hook.hexa split/merge D4a"
  candidate_reused_by = "C (MitosisC) · CHAT serve-time"
  status    = "candidate (unverified) — C cites mitosis_hook as cross-link scaffold but the reuse edge's closed-form evidence row is not yet secured"

@X c2 := "IIT4 bitops shim -> C/CHAT" :: reuse-candidate [proposed draft]
  provider  = "IIT4"
  primitive = "bit-primitive shim -> hexa-lang bitops"
  candidate_reused_by = "C · CHAT Phi-measure path"
  status    = "candidate (unverified) — #540 is IIT4-internal shim; sibling-module reuse unrecorded (WARN: hexa-lang bitops is a SEPARATE repo -> outside g67 intra-project scope, coupling forbidden)"

@X c3 := "BRIDGE Law-70 clamp -> W/trinity" :: reuse-candidate [proposed draft]
  provider  = "BRIDGE"
  primitive = "Law-70 clamp transfer fn"
  candidate_reused_by = "W (Psi-coupling) · integrated trinity gate"
  status    = "candidate (unverified) — both ends BLUE but the reuse(transfer) edge's own closed-form W-ledger row is not yet secured"

# ── 4. cross-repo guard + usage protocol (atlas-first · @D g67) ──

@N n1 := "cross-repo prohibition line (g67 intra-project)" :: note [active]
  rule = "SEPARATE-repo couplings (LEGO -> hexa-lang flame/spiking_lib, IIT4 -> hexa-lang bitops, etc.) are EXCLUDED from this lattice — tracked separately in HEXAD/LEGO/INDEX.md cross-repo. g67 = intra-anima only."

@N n2 := "reuse protocol (g67 do — before building a primitive)" :: note [active]
  step1 = "grep-first: before a new primitive, search this provides[] + the sibling module INDEX/README cross-arc anchor + `hexa atlas lookup` for a verified one"
  step2 = "on reuse stamp record `reused[]` · on offering stamp `provides[]` + add the ledger row here (evidence col = closed-form/battery basis)"
  step3 = "lattice update: a new section-N landing that reuses updates this file + the provider module INDEX simultaneously (a1/a_blue_closed consistency, append-only g6)"
  step4 = "tier honesty: if provider/edge is not BLUE/GREEN, register as candidate (unverified) only — fake closed-form forbidden (a_blue_closed, AGENTS.tape g3/f2)"

@N n3 := "human ASCII graph view (provides -> primitive -> reused-by)" :: note [active]
  graph <<~GRAPH
  [central verification substrate]
   blue_falsifier.py --(central BLUE battery)--> BRIDGE · D · E · M · MITOSIS · CHAT · CHECK · LEGO · META_FP
   (verify_hexad_blue)

  [Phi form orthogonal anchor]
   META_FP  psi(c)=(1+c)/2 --(Psi-C1/Pi_half form)--> NEUROMORPHIC(Psi-C1) · LOIHI · LEGO(Psi-C1=s112 instance) · s166
   (s112)

  [learning-axis primitive]
   TENSION-LINK  tension_link_step.hexa --(n6 Noether gate · online step)--> TENSION-TRAIN (5 hexa carry)

  [engine lib promote]
   LEGO  lego_engine.py (s129 lib) --(LIFNet · psi_c1 · var-decomp)--> s131/135/137

  [Phi measure primitive]
   C  c_measure_phi / phi_spatial (RFC 036) --(byte-equal Phi)--> IIT4 · CHAT
  GRAPH
