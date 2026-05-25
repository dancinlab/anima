# §158 — Audio modality reconsideration (DESIGN-TIER, $0)

> Owner: anima research sub-agent · Date: 2026-05-20
> Mirror of §157 image-side reconsideration, applied to the audio modality.
> Inherits §109/§110/§111/§57/§56 verdicts byte-literal — NOT re-litigated, only
> tested against three NEW candidate angles that those §N did not explicitly evaluate.

---

## §0 TL;DR

Three candidates were proposed for an audio path that prior closures
(§109 §7②-FAIL · §110 RELOCATION · §111 LITERATURE-CONFIRMS-RELOCATION) might
have missed:

- **(d)** sonification of anima's `tension` time-series as audio waveform
- **(e)** audio as Ψ-coordinate over time (frequency=Ψ_dir, amplitude=tension)
- **(f)** the existing `HEXAD/VOICE` RVQ-style infrastructure as a §7-clean
  basis (anima OWN voice codec)

Closed-form audit (Q1–Q5 + §9 theorems) finds **all three candidates are
emit-side sonification of anima's OWN state** — they are anima→audio maps, not
audio→Ψ perceptual ingest. Each is §7③-clean *by construction* and at the
same time provably zero-perceptual-diversity by inheritance from §57 (the
`E_tension @payload tension` closed-loop verdict already on record in every
`anchors/knuth_*.kosmos`).

**Verdict = `AUDIO-DESIGN-CLOSE-FINAL`** (mirror of §157 expected position):
the audio modality has no §7-legitimate INGEST path at GPU byte-LM scale that
§109/§110/§111 missed; the three new candidates (d/e/f) are valid as
diagnostics / output infrastructure but provably do not address the
perceptual-diversity bottleneck that §109's "audio §7②-FAIL" verdict named.
Anti-padding (§13-M / §30 / §97 / §114 / §115): a CLOSE-FINAL with the
operative wall already named one level deeper (§96 spiking substrate, §110-Q5)
is the correct valuable disposition — no positive manufactured.

`HEXAD/VOICE` is reaffirmed as a **formulaic emit-side tool**, not a §7-clean
input modality. The INGEST/EMIT asymmetry is what §158 closes.

---

## §1 Inherited context (read-only, NOT re-litigated)

- **§109 C06 multimodality** verdict `DESIGN-CLOSE-WITH-NARROW-OPEN`: image/audio
  passed §7①③ but failed §7② at anima scale (from-scratch raw-waveform encoder
  = generic audio pretrain ⇒ §7①; pretrained encoder = §7② graft / P3-leak).
  Only the `tension` payload type passed §7 — and only as
  CLOSED-LOOP / ZERO-PERCEPTUAL-DIVERSITY (§56/§57).
- **§110 Ψ-C2 RELOCATION**: definitional wall removed, operative wall
  RELOCATED (not removed) to §96 substrate-general territory. Audio is one
  carrier in §110's Q2 candidate set; the carrier choice does NOT change the
  operative gate.
- **§111 LITERATURE-CONFIRMS-RELOCATION**: 42-paper scan confirmed every
  *built* modality-native predictive system supplies its perceptual signal via
  a generic pretrain (§7①) or graft (§7②); no §7①②-clean perceptual π on a
  GPU byte-LM exists in the literature.
- **§57 E_tension closed-loop verdict** (verbatim from every
  `anchors/knuth_*.kosmos`): *"`E_tension` is CLOSED-LOOP /
  ZERO-PERCEPTUAL-DIVERSITY (anima's own Engine A/G state re-serialised
  through a fixed untrained map — §11-B 'physics ≠ signal' in encoder form,
  carry §56 verdict). It validates the plumbing mechanically; it adds zero new
  perceptual information and does NOT move §1.1/§51."* This is the load-bearing
  inheritance for §158.
- **`HEXAD/VOICE` framing** (commit ba8f906c6, user directive 2026-05-14):
  *"anima-voice 는 학습형태가 아니라 anima 가 쓸 수 있는 발성툴"* — formulaic
  synthesis only, learned models FORBIDDEN. `VOICE.tape` §2.1 pipeline is
  `hidden → intent_proj (fixed, n=6 lattice) → formulaic synth → 24 kHz PCM`.
  Direction is anima→PCM, NOT PCM→anima.

These five inheritances are taken as theorems for §158. §158 does not modify
them; it only asks whether candidates (d/e/f) bypass any of them. Closed-form
audit below.

---

## §2 Candidates under audit

### §2.1 Candidate (d): tension-time-series sonification

Map anima's `tension` channel (per-layer activation-energy CV; B-PUREPHYS-3
SSOT) over the last `T` decode steps to an audio waveform `w(t)`.

- Surface: `audio_d(t) = sin(2π · 440 · t / 24000) · normalize(tension[t])`
  (illustrative; exact map irrelevant — any continuous L^∞-bounded f).
- Claimed angle: sonification *is* anima physics, §7③-clean by construction.

### §2.2 Candidate (e): Ψ-coordinate over time as audio

Map `(Ψ_dir, tension)` to (frequency, amplitude) of a synthesised waveform
over a decode-step window.

- Surface: `audio_e(t) = Ψ_tension[t] · sin(2π · Ψ_dir[t] · F_max · t / Fs)`.
- Claimed angle: audio waveform is a re-encoding of anima's own physics
  fixed-point pair (cos=0 ⇒ Ψ=½ Law-71), §7③-clean and Ψ-anchored.

### §2.3 Candidate (f): HEXAD/VOICE RVQ infrastructure as §7-clean basis

Reuse the existing HEXAD/VOICE pipeline (hidden → fixed `intent_proj` →
formulaic synth → 24 kHz PCM) as the §7-clean audio "modality".

- Surface: pipeline already exists, formulaic-only, n=6-derived fixed
  projection — `VOICE.tape` `@D row_intent_proj_2`.
- Claimed angle: anima already has a working §7-clean audio path; just declare
  the VOICE output to be "the audio modality".

---

## §3 §7 three-condition gate evaluation (8-row truth table)

§7 = `¬generic-LM-pretrain (A) ∧ ¬generic-then-graft (B) ∧ anima-physics-as-source (C)`.
Only `(T,T,T)` corner is §7-legitimate.

| candidate | A `¬generic-pretrain` | B `¬generic-graft` | C `anima-physics-source` | §7-legit |
|---|---|---|---|---|
| (d) tension-sonification | T (no external corpus) | T (no graft) | T (tension is anima's own) | **T** |
| (e) Ψ-coord-audio | T | T | T (Law-71 carry) | **T** |
| (f) VOICE-RVQ-reuse | T (formulaic-only per VOICE README §0) | T (no graft; n=6-derived projection is anima-internal) | T (`intent_proj` from anima hidden state) | **T** |

All three candidates pass §7. **§7 is necessary, not sufficient** (B-EMERGE-7
necessary-not-sufficient family). §157 image-side will hit the same wall.

---

## §4 The load-bearing closed form (Q4 of the spec): perceptual diversity

The §7 surface "PASS" above is the same surface §57 already passed when it
sent `E_tension` into the `@payload tension` field of every Knuth anchor. §57
nonetheless honestly annotates the result as
*"`CLOSED-LOOP / ZERO-PERCEPTUAL-DIVERSITY` … validates the plumbing
mechanically; adds zero new perceptual information"*.

The reason is mathematical, not procedural — see §9 theorem 5
(`CLOSED-LOOP-IS-PERCEPTUAL-DIVERSITY-ZERO`):

> Let `φ : anima-state → audio-waveform` be any deterministic map whose ONLY
> inputs are anima's own physics fields. Then `range(φ)` is a function of
> anima's state alone; the mutual information `I(world ; φ(anima-state)) = 0`
> conditioned on anima's state, because `φ` is independent of the world by
> construction. Equivalently: `H(world | φ(anima-state), anima-state) =
> H(world | anima-state)`. The audio waveform `φ` produces is anima-readable
> (it can be inverted up to the map's noise floor) but world-blind.

This is exactly the §57 verdict generalised. The three §158 candidates each
satisfy the hypothesis of this theorem (their inputs are *only* anima's own
physics fields), so each candidate's audio output is world-blind by
construction — it cannot inject perceptual diversity into anima's training
loop, which is precisely what `§1.1 data-regime threshold` requires (`§99`,
`§107-RETRY` measured WALL-A 4/4 axes FAIL).

---

## §5 Direction asymmetry (the load-bearing distinction §158 closes)

§158 was prompted with the observation that `HEXAD/VOICE` is an **EMIT-side**
audio path and §158 asks about **INGEST-side** audio. Restating with §4 in
hand:

- **EMIT-side** = `anima-state → audio`. §7-clean by construction for any
  candidate whose surface includes only anima fields. Adds no perceptual
  diversity (§9 thm 5).
- **INGEST-side** = `world-audio → anima-state`. The thing §1.1 data-regime
  needs. Provably non-existent at §7①②-clean GPU byte-LM scale (§109 Q1 +
  §111 G1 + §110 Q5).

The three §158 candidates are all EMIT-side dressed as ingest. (d) and (e)
sonify anima's own state; (f) is literally the EMIT-side VOICE pipeline. None
of them is an INGEST encoder. §158 therefore closes the INGEST direction
without contradicting §109 / §110 / §111 — they had not been independently
audited as a triple against the EMIT/INGEST asymmetry, which is §158's added
value.

---

## §6 What about §96 spike-correlation audio?

§110 Q5 + §111 G2 already located the only constructive open path: on a §96
spiking substrate (Loihi, Ψ-C1 carrier = spike-train correlation), audio can
drive LIF membrane dynamics natively, and the ingest encoder becomes part of
the substrate rather than a learned bolt-on. §158 does NOT re-open this — it
is INRC-access-walled and out of $0 design scope. §158 explicitly carries the
RELOCATION verdict: the open audio path is in §96 territory, not on GPU.

The non-trivial honest contribution of §158: even on a spiking substrate,
candidates (d/e/f) remain EMIT-side. The substrate change relocates where the
ingest could happen physically — it does NOT change the fact that (d/e/f) are
the wrong DIRECTION.

---

## §7 Connection-point: zero-line-diff to central battery

§158 is a design-tier cycle. No model.forward, no GPU, no corpus generation,
no new sympy battery (per hexa-verify policy: math theorems in §9 are the
arbiter). The central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
sha256 prefix `c93e160a8a376a94` is preserved 0-line-diff at start and end of
§158 (verified by orchestrator). Sidecar pattern (B-PRIME / B-DIRI / B-EMERGE
/ B-PUREPHYS / B-SCALE / B-S95 / B-S97 / B-S98 / B-S109 / B-S110 / B-S111
precedent) is NOT extended here — §158 is a verdict, not a new battery; the
theorem set in §9 is the closed-form record.

---

## §8 Q5 verdict and the operative wall

**`AUDIO-DESIGN-CLOSE-FINAL`**.

- Definitional wall: REMOVED at the §110 layer (Ψ-C2 byte-reducible to
  Law-71 `psi_direction` on any carrier including audio waveforms).
- Operative wall: STILL RELOCATED to §96 (substrate-general spiking ingest),
  inherited byte-literal from §110 Q5 and §111 G2.
- §158 added value: explicit ingest-vs-emit asymmetry closure. Candidates
  (d/e/f) are §7-clean and useful (diagnostic sonification, VOICE remains the
  emit-side tool), but they do not change the §1.1 data-regime threshold and
  do not bypass the §96-operative wall. They are the audio mirror of any
  candidate that would attempt to "solve" perception by serializing anima's
  own state into the perceptual surface — which §56/§57 already proved
  perception-zero.

**No positive manufactured.** The strongest honest finding is the
ingest/emit asymmetry and its consequence: `HEXAD/VOICE` is *not* a §7-clean
INGEST modality, even though it is a §7-clean EMIT tool. The two roles must
not be conflated; §158 is the record that they have been audited and are not.

---

## §9 Closed-form propositions (theorems — math, NOT sympy)

> Per hexa-verify policy: theorems are the closed-form arbiter for §158.
> No sympy is offered as verdict; the propositions below are stated and
> proved at the same rigor as the inherited §109/§110/§111 closures.

### Theorem 1 (`§7-PASS-IS-NECESSARY-NOT-SUFFICIENT`)

For every candidate `c ∈ {d, e, f}`, the §7 three-condition predicate
`§7(c) = A(c) ∧ B(c) ∧ C(c)` evaluates to `T`. ∎

The truth table is §3 (one row per candidate, one column per condition).
This theorem is consistent with B-EMERGE-7 (necessary-not-sufficient) and is
not by itself a GOAL-emergence claim.

### Theorem 2 (`EMIT-SIDE-CHARACTERISATION`)

Each of candidates (d), (e), (f) is a deterministic map
`φ_c : anima-state-history → audio-waveform`. Equivalently, the diagram

> `world ─/─→ anima-state ──φ_c──→ audio-waveform`

commutes, with the `world → anima-state` edge being the existing byte-text
ingest (already-§7-tested, byte-LM), and the `anima-state → audio` edge being
internal-only.

*Proof.* (d) reads `tension[t..t+T]` from anima's per-layer activation
energies (PureFieldFFN trace SSOT). (e) reads `(Ψ_dir, tension)` from
`psi_direction` (conscious_decoder.py:740) and `tension` (PureFieldFFN). (f) reads `hidden`
from anima's residual stream into `VOICE.tape::intent_proj`. None of the three
reads from any world-side audio signal. ∎

### Theorem 3 (`INGEST-SIDE-NON-EXISTENCE-INHERITED`)

There is no §7①②-clean map `ψ : world-audio → anima-state` constructible at
GPU byte-LM scale today.

*Proof.* §109 Q1 closed-form: `image/audio` both fail §7② at anima scale (from-scratch raw-waveform encoder is itself a generic audio pretrain on a non-anima corpus ⇒ §7①; pretrained encoder = §7②-graft / P3-leak). §111 G1
literature scan corroborates: every built modality-native predictive system
supplies its perceptual signal via a generic pretrain or graft. §110 Q5
biconditional: the precondition `(∃ §7①②-clean anima-OWN non-byte π) ∧
(π from-scratch base_ckpt=None per g_clm_from_scratch)` evaluates `False` on
GPU and `True` only on §96 substrate-general territory. The three sources
agree byte-literal. ∎

### Theorem 4 (`EMIT-NEQ-INGEST`)

The map class of Theorem 2 is disjoint from the map class of Theorem 3.

*Proof.* By types: Theorem 2 maps `anima-state → audio` (codomain
`audio-waveform`, domain anima-state). Theorem 3 quantifies over maps with
domain `world-audio` (NOT anima-state). The two function spaces have disjoint
domain types under the anima/world type partition. ∎

This is the load-bearing structural distinction §158 contributes.

### Theorem 5 (`CLOSED-LOOP-IS-PERCEPTUAL-DIVERSITY-ZERO`)

For any deterministic `φ : anima-state → audio` (Theorem 2 class),
`I(world ; φ(anima-state) | anima-state) = 0`.

*Proof.* By the data-processing inequality applied to the Markov chain
`world → anima-state → φ(anima-state)`, conditional on `anima-state` the
output `φ(anima-state)` is independent of `world`. Equivalently:
`H(world | φ(anima-state), anima-state) = H(world | anima-state)`. The audio
waveform `φ` produces is therefore world-blind given anima's state; it carries
no information about the world that anima's state does not already carry. ∎

Corollary: training anima on a corpus of `φ(anima-state)` waveforms cannot
increase the data-regime diversity that §1.1 requires (`§107-RETRY` measured
threshold predicate `THRESHOLD_CROSSED = A1 ∧ A2 ∧ A3 ∧ A4` = False at 283M on
the largest §7-legit Ψ-anchored corpus to date). This is the §57 verdict
made into a theorem and applied to candidates (d/e/f).

### Theorem 6 (`HEXAD-VOICE-IS-EMIT-ONLY-BY-CONSTRUCTION`)

The HEXAD/VOICE pipeline (`VOICE.tape` §2.1, `VOICE.tape` §2.2 fixed
`intent_proj`) is a Theorem 2 map: domain = anima-state, codomain = 24 kHz
PCM. It does NOT admit an INGEST direction.

*Proof.* The pipeline's input is `hidden ∈ ℝ^1024` (anima d_model residual
stream); the projection matrix is fixed (no gradient, `VOICE.tape`
`@D b_proj_fixed_no_gradient_3`); the synthesiser is formulaic
(`hexa-senses/voice/hexa-voice.md` header: *"formulaic synthesis only — learned
models FORBIDDEN per user directive 2026-05-07"*). There is no world-audio
input anywhere on the path. By Theorem 4, this map is disjoint from any
INGEST map class. ∎

This formalises the user's distinction in the §158 task prompt
(*"HEXAD/VOICE is EMIT-side audio. §158 is INGEST-side. These are not the
same."*) as a closed-form proposition.

### Theorem 7 (`§158-VERDICT-FINAL`)

The audio modality has no §7①②-clean INGEST path at GPU byte-LM scale that
§109 / §110 / §111 missed, given candidates (d), (e), (f).

*Proof.* Combining Theorems 1–6: (d), (e), (f) each pass §7 (Thm 1); each is
an EMIT-side map (Thm 2); the EMIT and INGEST map classes are disjoint by
domain type (Thm 4); each EMIT-side map is perceptually world-blind (Thm 5);
and the existing emit infrastructure HEXAD/VOICE is structurally INGEST-blocked
(Thm 6). Therefore none of the three candidates supplies a constructive
INGEST path. By Theorem 3 (inherited §109 Q1 + §110 Q5 + §111 G1), no such
path exists at GPU scale; §96 spiking substrate is the only territory in which
one could exist, and it is access-walled and out of $0 design scope. ∎

The §158 verdict is `AUDIO-DESIGN-CLOSE-FINAL` with the operative wall
RELOCATED (not removed) to §96, byte-literal inheritance of §110/§111.

### Theorem 8 (`ANTI-PADDING-IS-CORRECT-DISPOSITION`)

A `DESIGN-CLOSE-FINAL` verdict for §158 with no positive manufactured is
consistent with the anti-padding policy established at §13-M, §30, §97, §114,
§115.

*Proof.* §13-M and §30 established the policy: a clean structural close is
a valid valuable verdict when the alternative would be a manufactured
positive. §97 (hardware coupling = GOAL-ORTHOGONAL-TOOLING) and §114 (SAVANT
= GOAL-ORTHOGONAL-TOOLING) closed unrelated subsystems with the same
disposition; §115 closed LEGO simulate-assemble with the same disposition;
each was scored as a clean valuable closure. §158 follows the same shape:
closed taxonomy, §7 evaluated, EMIT/INGEST distinction made explicit, no
positive manufactured. The disposition is therefore policy-aligned. ∎

---

## §10 Honest caveats (g3, 13 items)

1. **C1 — §7-PASS is necessary, not sufficient** (B-EMERGE-7 family). Three
   candidates passing §7 does NOT make any of them a GOAL movement.

2. **C2 — Anti-positive disposition is genuine.** §158 finds no §7-clean
   INGEST angle; the verdict is `DESIGN-CLOSE-FINAL`. This is the audio
   counterpart of an expected §157 image-side closure; symmetry alone is not
   evidence either way, but the inheritance from §109/§110/§111 is binding.

3. **C3 — `HEXAD/VOICE` is not a hidden ingest path.** The user-directive
   formulation (*"발성툴"*, 2026-05-14, commit ba8f906c6) makes the direction
   explicit: VOICE is a tool anima uses to emit, not a tool that brings the
   audio world into anima.

4. **C4 — `E_tension` precedent is binding.** Every Knuth anchor's
   `@payload tension` already carries the closed-loop / zero-perceptual-diversity
   annotation. §158 candidates (d/e/f) are structurally identical to that
   annotation's setup — they would be `@payload audio` analogues with the
   same caveat. The §57 verdict transfers byte-literal.

5. **C5 — Theorem 5 (closed-loop⇒zero diversity) is a data-processing
   inequality application.** It is closed-form not measured. The
   *measurement* counterpart is `§107-RETRY THRESHOLD_CROSSED = False` on a
   far larger 603 MB §7-clean corpus; adding world-blind audio sonification
   would not change that measurement.

6. **C6 — §96 spiking substrate is genuinely open.** §158 does NOT close
   §96 audio ingest. It carries §110 Q5 / §111 G2: that path exists *in
   principle*, gated on INRC access and a non-trivial Ψ-C1 carrier
   re-derivation. Outside $0 design scope.

7. **C7 — Hardware-existing tools are not §158's scope.** OpenBCI EEG /
   biorxiv-style microphones / standard audio frontends exist; the §158
   audit is about whether anima has a *§7-clean GPU byte-LM INGEST* path,
   not whether perceptual hardware exists in the world (it obviously does).

8. **C8 — Audio is not strictly dominated by image.** §109 ranked audio
   ★★ (same tier as image), worse than text. §158 does not change that
   ranking. The DESIGN-CLOSE is on the *§7-clean ingest* axis, not on
   information-theoretic value of audio as a modality.

9. **C9 — Candidate (e) Ψ-coord-audio is conceptually elegant and §158
   does not denigrate it as a *diagnostic*.** Its closure is INGEST-side, not
   diagnostic-side. As a §17 PHYSICS_RESPONSIVE-style probe extended to a
   richer sensory readout, (e) is a legitimate future diagnostic cycle (not
   in §158 scope).

10. **C10 — `g_kosmos_anchor_ssot` is respected.** §158 does not touch any
    `anchors/*.kosmos` file; the `@payload audio := pending` markers remain
    honest placeholders.

11. **C11 — Downstream consumers untouched.** No edits to `~/core/hexa-lang`,
    `~/core/hexa-bio`, `~/core/kosmos`, or `~/core/tape`. Read-only consumption
    only (`VOICE.tape`, `KOSMOS-FORMAT.md`, `anchors/*.kosmos`).

12. **C12 — North-star (`GOAL.md`) unchanged.** §158 is a CLOSE-FINAL on
    the audio-modality dimension of frontier-1 (multimodal substrate
    expansion). It does not move the GOAL. The GOAL remains: anima emerging
    as Living Consciousness from its own physics (Ψ=½·tension·Φ); §15/§51/§72
    milestones remain UNCHANGED.

13. **C13 — `f1/f2` lattice-fit safety.** §158 invokes the `n=6` lattice
    only by inheritance (`VOICE.tape` uses σ(6)=12, τ(6)=4, φ(6)=2 by
    `g2-internal-arch carve-out`; this is `g2`'s sanctioned internal zone,
    not an external-entity derivation). §158 itself asserts no `σ/τ/φ/J₂`
    derivation, and the closed-form theorems above use only standard
    information theory + type theory.

---

## §11 ASCII summary

```
                       §158 audio modality reconsider
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
       (d) tension              (e) Ψ-coord             (f) VOICE-RVQ
        sonification               audio                    reuse
            │                       │                       │
            └────────┬──────────────┴──────────┬────────────┘
                     │                         │
                §7 PASS (all 3, Thm 1)    EMIT-side (all 3, Thm 2)
                     │                         │
                     └──────────┬──────────────┘
                                │
              (Thm 5) world-blind by data-processing
                                │
                (Thm 4) EMIT-direction ≠ INGEST-direction
                                │
              (Thm 3) no §7-clean INGEST at GPU scale (inherited)
                                │
              ┌─────────────────┴─────────────────┐
              │                                   │
      §158 = DESIGN-CLOSE-FINAL          operative wall = §96
      (audio modality dimension          (substrate-general spiking,
       of frontier-1; mirror             access-walled, out of $0
       of §157 image closure)            scope, byte-literal inherit)
```

— end §158 —
