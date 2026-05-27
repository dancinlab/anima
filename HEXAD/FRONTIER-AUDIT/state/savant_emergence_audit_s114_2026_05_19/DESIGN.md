# §114 SAVANT EMERGENCE-FRONTIER AUDIT — design-tier $0

**date** 2026-05-19 · **tier** DESIGN-TIER (audit) · **cost** $0 · NO GPU/runpod/fire/model.forward/corpus
**central blue** `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha256 prefix `c93e160a8a376a94` — 0-line-diff verified START + END
**verdict (one line)** SAVANT = **GOAL-ORTHOGONAL-TOOLING** (decode-time ops layer ⊥ emergence frontier; mirror §97 hardware-coupling GOAL-ORTHOGONAL precedent). Two honest flags: (a) `savant_phi` is a **divergent separate model** (Treffert P68 savant-syndrome Φ-proxy `Σ|v|^1.5/d`, NOT a re-impl of anima's IIT `c_measure_phi`/phi_spatial) — not a Φ-readout conflict, a different construct; (b) routing-overlay top-k `keep_rate = GZ_LOWER = 1/2 − ln(4/3)` where `ln(4/3)` is documented `τ(6)=4`-derived → **NUMEROLOGY-TAINTED** per g2 internal_use_integrity_test (honest carve-out, §98 precedent — taint is in a *runtime tooling knob*, causally orthogonal to GOAL, NOT re-architected).

---

## §0 — Why this cycle exists

User directive 2026-05-19 "hexad/savnt 도 한번 검토 안됬으면 해보고". The HEXAD/SAVANT subsystem (SAVANT-TOOL Phase 1/2/3b/c/d LANDED 2026-05-14, 24/24 falsifier PASS $0 Mac local — memory note) was built early and a grep confirms it was **NEVER audited against the §1~§111 GOAL/§7 emergence frontier** (0 savant×§N×emergence hits in RESEARCH.md). §114 closes that never-audited gap. This is an AUDIT, design-tier only — SAVANT architecture is NOT rewritten.

§N selection: §110 (s110) + §111 (s111 deep-research) taken; §112/§113 queued per directive; §114 = next free (verified §112-116 free in PHILOSOPHY.tape/RESEARCH.md/AGENTS.tape/state).

## §1 — Q1: What SAVANT IS (closed component taxonomy)

```
                         SAVANT subsystem
                                │
   ┌────────────┬───────────────┼───────────────┬────────────────┐
   │            │               │               │                │
gate API    /savant CLI     SI monitor    routing-overlay     savant_phi
(savant_set/ (anima_chat_   (anima_savant_  top-k mask        (savant_phi
 get/check/  savant_cli     si_monitor      (anima_savant_     .hexa P68
 apply_gate) .hexa +help)   .hexa)          routing_overlay)   Treffert)
   │            │               │               │                │
 ORTHO        ORTHO          ORTHO           ORTHO            ORTHO
 -TOOLING     -TOOLING       -TOOLING        -TOOLING +g2     -TOOLING
                                              taint flag      (divergent Φ)
```

Closed 3-class taxonomy `{emergence-relevant / GOAL-orthogonal-tooling / §7-risk}`:

| component | what it does | class |
|---|---|---|
| **gate API** (`anima_savant_tool.hexa`: `savant_set/get/check_gate/apply_gate/savant_si`) | runtime ON/OFF of "savant mode" via self-judged SI vs threshold 3.0; sets a `chat` dict flag + dropout knob. NO model.forward, NO training, T3/T4 trigger reasons rejected | **GOAL-orthogonal-tooling** |
| **/savant CLI** (`anima_chat_savant_cli.hexa` +help) | user-facing `/savant on math` / `/savant off` / `/savant si` / `/savant help` command parser; no learning | **GOAL-orthogonal-tooling** |
| **SI monitor** (`anima_savant_si_monitor.hexa`) | measures 3 signals (token_entropy, wmax of cell-pool gate weights, recent_splits from mitosis log) → feeds gate. Falsifier `F-SAVANT-MONITOR-5 NO-LEARN — pure stateless, no learned weights` | **GOAL-orthogonal-tooling** |
| **routing-overlay top-k mask** (`anima_savant_routing_overlay.hexa`) | softmax-pre top-k mask on cell-pool *tensions*: keep top `int(keep_rate·n)` (≥1) cells, rest → −1e9. keep_rate ∈ {GZ_LOWER 0.2123, GZ_CENTER 0.3679, OFF=all}. decode-time, order-preserving, no weight mutation | **GOAL-orthogonal-tooling** + **g2 numerology-taint flag** (Q3) |
| **savant_phi** (`savant_phi.hexa`) | P68 Treffert savant-syndrome model: 4 domain modules, per-domain `phi_module(v)=Σ|v|^1.5/d`, general Φ via cross-module MI, specialization sweep. A *separate phenomenology study*, NOT anima's runtime Φ | **GOAL-orthogonal-tooling** + **divergent-from-central-Φ flag** (Q3) |

`SAVANT.tape` itself is a theory/audit/containment compendium (Golden Zone constants + clm_01..13 transcript + §12 containment Tier T1/T2 allowed, T3/T4 forbidden). It is documentation, not a mechanism.

**Q1 verdict**: 5/5 components = GOAL-orthogonal-tooling. 0 emergence-relevant. 0 §7-risk (T3/T4 structurally rejected by gate, no SFT/pretrain path). Two components carry honest sub-flags resolved in Q3.

## §2 — Q2: §7 GOAL-legitimacy gate (8-row truth table)

§7 3-cond (RESEARCH.md §7): ① not-generic-LM-pretrain ② not-generic-then-graft ③ flows through anima's OWN physics (NOT a command-channel bypassing it). For SAVANT, "legitimate as tooling" = it does NOT *violate* §7 (it is not an emergence mechanism, so it cannot satisfy §7③ positively — like §97 hardware-coupling it is §7-NEUTRAL/orthogonal, not §7-passing-as-a-lever).

Closed Boolean per component over (¬genericLM, ¬graft, own-physics-not-command-channel):

| component | ¬§7① genericLM | ¬§7② graft | §7③ own-physics not-cmd-channel | §7-disposition |
|---|---|---|---|---|
| gate API | T (no forward/train) | T (T3/T4 rejected) | T (toggles anima's OWN cell-pool routing, not external cmd) | §7-CLEAN-TOOLING |
| /savant CLI | T | T | T (parses to gate API only) | §7-CLEAN-TOOLING |
| SI monitor | T (NO-LEARN stateless) | T | T (reads anima's own logits/weights/mitosis-log) | §7-CLEAN-TOOLING |
| routing-overlay | T (decode-time mask) | T (no external behavior grafted) | T (masks anima's OWN tension routing — re-weights, does not inject) | §7-CLEAN-TOOLING |
| savant_phi | T (offline study, no train) | T | n/a (not in inference path; standalone study) | §7-CLEAN-TOOLING |

8-row truth table (3 Boolean axes) closed in B-S114-2: SAVANT-as-whole satisfies (T,T,T) ⇒ §7-CLEAN (does not act as generic-LM/SFT path (a), does not graft external behavior (b), flows through / re-weights anima's OWN cell-pool tensions rather than acting as a command-channel that bypasses physics (c)). The gate's *forbidden trigger* list (T4 `external_entity_lattice_fit` rejected) is an explicit anti-§7-risk fence already in source.

**Q2 verdict**: SAVANT is §7-CLEAN as tooling — it never acts as a generic-LM/SFT path, never grafts external behavior, and re-weights anima's own physics rather than commanding it. It is §7-NEUTRAL (orthogonal), NOT §7-passing-as-an-emergence-lever.

## §3 — Q3: savant_phi vs anima Φ + top-k g2 integrity test

**Q3a — savant_phi vs central Φ (connection-point: divergent, by-design)**:
- anima central Φ: `HEXAD/C/c_lib.hexa::c_measure_phi(states,n_cells,dim,n_bins) = phi_spatial(...)` — RFC 036 native byte-equal replica of `phi_rs` IIT (MI-binned, `n_bins` default 4, byte-equal Python oracle 0.5000000001324147 err<1e-12, central B-C / F-C-PORT-3).
- SAVANT `savant_phi.hexa::phi_module(v) = Σ|v[j]|^1.5 / d` — a **super-linear energy proxy** (Newton-iter sqrt for the ^1.5), no MI, no binning, no IIT, explicitly self-described as a "proxy" capturing "IIT-style integration nonlinearity". General Φ in savant_phi = cross-module MI for a **4-domain Treffert savant-syndrome model** (Kim Peek / Wiltshire phenomenology), with capacity-constrained gain tuple.

Closed finding: `phi_module ≠ c_measure_phi` structurally (different formula, different inputs, different purpose) — **NOT byte-equal, NOT a re-implementation, NOT a divergence-of-the-same-quantity**. They are two distinct constructs: `c_measure_phi` is anima's runtime IIT-Φ-ratchet input; `savant_phi` is an offline savant-syndrome *phenomenology study* (P68 roadmap). This is honest separation, not a Φ-readout conflict. B-S114-3 closes the connection-point as DIVERGENT-BY-DESIGN (distinct-construct, NOT a consistency violation): there is no point in anima's inference path where savant_phi substitutes c_measure_phi.

**Q3b — routing-overlay top-k mask g2 internal_use_integrity_test (§98 precedent)**:
- The mask `keep_rate ∈ {GZ_LOWER, GZ_CENTER}`. `GZ_LOWER = 1/2 − ln(4/3) ≈ 0.2123`; `GZ_CENTER = 1/e ≈ 0.3679`. Source: `st_gz_lower() { return 0.5 - log(4.0/3.0) }`.
- g2 test: "if the lattice were removed, would this count still be the same?" SAVANT.tape documents verbatim `GZ_WIDTH = ln(4/3) = τ(6)=4` (divisor-count 4th-state entropy cost) and `GZ_UPPER = 1/2` = "완전수 6 의 최대 proper-divisor 역수". The keep_rate is therefore a **TARGET the routing knob is set to match** (1/2−ln(4/3), 1/e), NOT a function-derived count that happens to equal a lattice value. Verdict: **NUMEROLOGY-TAINTED** per g2 internal_use_integrity_test (same family as §98's σ(6)=12 wiring provenance-taint).
- Honest scope (§98 precedent — provenance-taint ≠ causal-blame): the taint is in a *decode-time routing-sparsity knob* (which fraction of mitosis cells survive the softmax). It is (i) causally orthogonal to the GOAL bottleneck (§11.3 data-regime irreducibility / §96 substrate — Q4), (ii) not load-bearing for any §1~§111 measured negative (every fire used full routing or Dir-I lever, never the SAVANT overlay), (iii) a runtime tooling parameter, not an architecture constant in the trained model. Like §98, §114 *records* the taint honestly; it does NOT mandate re-architecture (the knob could be re-derived from a function — e.g. "keep cells whose tension exceeds the pool mean" — but that is a tooling refactor, not a GOAL lever). f1/f2 hard-fail safe: §114 itself asserts NO σ/τ/φ/J₂ derivation; the taint is *found in SAVANT source*, not introduced here.

**Q3 verdict**: savant_phi = divergent separate construct (not a Φ conflict — honest distinct-model). top-k mask = numerology-tainted g2 knob (honest carve-out, §98-class, GOAL-orthogonal so causally innocent — exactly the §98 (c) MIXED pattern: provenance-tainted, causation-innocent).

## §4 — Q4: Frontier-relevance (SAVANT ∩ frontier = ∅)

| frontier axis | does SAVANT touch it? |
|---|---|
| §1.1 data-regime irreducible (§11.3/§15/§51) | **NO** — SAVANT is decode-time; touches no corpus, no diversity, no pre-training loss |
| §110 Ψ-C2 / §96 substrate (frontier-1 multimodal, relocated to §96 spike-correlation) | **NO** — routing-overlay masks cell-pool **tensions** (mitosis gate weights), NOT `psi_direction`/`psi_entropy` carrier ℝ^{V=256}; §110's DEP set {psi_direction, psi_entropy} is untouched by SAVANT |
| §72 frontier-2 architectural insight | **NO** — SAVANT is an established ops/gate layer, not a new architecture |

Closed: `SAVANT-frontier-intersection = ∅`. The only physics quantity SAVANT reads is cell-pool tension (for SI/wmax signals and the routing mask) — and even there it *re-weights* routing, it does not redefine Ψ, change the substrate, or alter the data regime. B-S114-5 closes the intersection as empty over the named frontier set {§1.1, §110-Ψ-C2, §96-substrate, §72}.

## §5 — Q5: Verdict + disposition

**SAVANT = GOAL-ORTHOGONAL-TOOLING.** Disposition mirror: §97 hardware-coupling GOAL-ORTHOGONAL precedent (and §13-M/§30 anti-padding — a clean orthogonal/negative verdict is correct and valuable, NOT a manufactured emergence-relevance). SAVANT is a runtime gate/CLI/monitor/routing-mask ops layer + an offline savant-syndrome phenomenology study (savant_phi). It does not touch, help, or hinder the GOAL emergence frontier; it is §7-clean as tooling and frontier-orthogonal.

**Value of this cycle**: closes the never-audited gap (the directive's purpose) — SAVANT is now on record as GOAL-orthogonal with two honest sub-flags surfaced (savant_phi distinct-construct; top-k mask g2 numerology-taint, §98-class causally-innocent). NOT a GOAL movement. north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.

---

## 13 honest C3 caveats

1. **Audit ≠ fire ≠ emergence** (g3): §114 reads SAVANT source + closed-form classifies it; it runs no model, measures no capability, moves the GOAL 0.
2. **GOAL-ORTHOGONAL is the honest verdict, not a hedge**: SAVANT genuinely does not intersect the frontier (Q4 = ∅). A "valuable orthogonal closure" framing is the §97/§13-M precedent, not padding.
3. **savant_phi divergence is by-design, not a bug**: it is a separate P68 Treffert phenomenology model; calling it "divergent from anima Φ" means "a different construct", NOT "a wrong Φ" — there is no inference path where it substitutes `c_measure_phi`.
4. **top-k numerology-taint is §98-class (provenance-tainted, causation-innocent)**: honest flag, NOT a re-architecture mandate; the knob is a runtime tooling parameter orthogonal to the GOAL bottleneck.
5. **f1/f2 safe**: §114 introduces NO σ(6)/τ(6)/φ(6)/J₂(6) derivation; the GZ-taint is *found in SAVANT source* and reported, not propagated. Ψ=½/Knuth = anima g2 internal carve-out (not exercised here).
6. **SI threshold 3.0**: not audited for function-derivation in this cycle (it is a self-gate hysteresis constant `SAVANT.tape §3`); flagged as a follow-up-if-ever, but it gates a GOAL-orthogonal tool so it inherits the orthogonality (low priority, honest).
7. **NO-LEARN claim trusted from falsifier label**: `F-SAVANT-MONITOR-5 NO-LEARN — pure stateless, no learned weights` is the subsystem's own falsifier; §114 reads the source and confirms no model.forward/train calls in the gate/monitor path, but does not re-run the 24/24 SAVANT-TOOL battery (out of $0 audit scope).
8. **Phase 3-a deferred**: `chat_repl` direct integration is import-alias upstream-patch-gated (memory note) — SAVANT is wired as overlay tools, not in the main REPL body. This does not change the orthogonality verdict (still decode-time tooling).
9. **Containment Tier T1/T2/T3/T4** (SAVANT.tape §12): the anti-§7-risk fence (T4 external-entity-lattice-fit rejected) is already in source and is a *strength*; §114 confirms it, does not re-derive it.
10. **central blue 0-line-diff** verified START + END (`c93e160a8a376a94`); §114 battery is a NEW sidecar, central untouched.
11. **necessary-not-sufficient (B-EMERGE-7 family)**: B-S114 proves the *taxonomy/gate/connection-point/intersection* are closed-form, NOT that SAVANT is irrelevant in some deeper sense — it proves SAVANT does not touch the *named* frontier set; B-S114-NOTE carries this (NOT counted 🔵).
12. **downstream-consumer invariant**: ~/core/hexa-lang + ~/core/hexa-bio read-only; §114 edits only anima HEXAD/SAVANT/SAVANT.tape Log (audit note append, no architecture rewrite) + SSOT.
13. **anti-padding**: if savant_phi had been a silent re-impl of c_measure_phi, or the top-k mask were function-derived, §114 would have said so plainly; the two flags raised are the honest findings, the orthogonal verdict is the honest disposition — no emergence-relevance manufactured.
