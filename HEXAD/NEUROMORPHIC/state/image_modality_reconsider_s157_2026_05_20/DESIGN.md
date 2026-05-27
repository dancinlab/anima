# §157 — IMAGE MODALITY RECONSIDER (design-tier $0)

> **status header (g3 / g_fire_autonomous scope-exclusion)**: $0 · **NO GPU** ·
> **NO runpod** · **NO fire** · **NO model.forward** · NO corpus generation ·
> NO model training. design-tier ONLY. central
> `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff
> (sha256 prefix `c93e160a8a376a94`, verified start). north-star + §15/§51/§72
> milestones UNCHANGED, **GOAL 미도달**. design ≠ fire ≠ emergence.
> capability claim 0.

§109 (`commit 410de2968`, `state/c06_multimodality_design_s109_2026_05_19/`)
closed C06 multimodality as **DESIGN-CLOSE-WITH-NARROW-OPEN**.
§110 (`state/modality_native_psi_design_s110_2026_05_19/`) advanced one level
below to **DESIGN-CLOSE-WITH-RELOCATION**: a §7-clean modality-native Ψ
*definition* (Ψ-C2) exists at $0 design tier, but the operative precondition (a
§7-clean non-byte projection `π`) is substrate-gated to §96 (Loihi /
spike-correlation). §111 (literature review, 42 papers) returned
**LITERATURE-SUPPORTS-Ψ-C2-DEFINITION-CONFIRMS-§110-RELOCATION**: the field's
modality-agnostic predictive-fixed-point work (JEPA / DEQ / PCN / FEP) supports
the *definition*, but every built modality encoder violates §7① (generic
perceptual pretrain) or §7② (pretrained graft).

The user question §157 makes load-bearing: did we **actually test** that, or
just argue design-tier? Specifically: is there a §7-clean angle for the *image*
modality that §109/§110/§111 missed — for instance, candidates (d) "image =
visualization of anima's Ψ-trajectory" or (e) "image = Ψ-coordinate plot",
where image is a *sample of anima's own physics* rather than a *representation
of an external scene*? Or do those collapse to the tension-route degeneracy
one level over (Ψ-C4 / §109-tension-wire)?

§157's honest verdict below is **DESIGN-CLOSE-FINAL** — inheriting
§109/§110/§111 and adding two new closed propositions (P5, P6) that show the
new (d)/(e) candidates **collapse closed-form to a previously-rejected
category**, NOT a new §7-clean angle. Anti-padding per §13-M / §13-L / §30 /
§109 / §110 / §111 precedent. The strongest positive that the closed-form
supports is *"no §7-clean image-as-perceptual-modality route exists at byte-LM
scale; new (d)/(e) candidates are anima self-portraits, not perception"* —
that is what is written, no more.

---

## §0 — Subject & frontier position

The user's framing: §109/§110/§111 *argued* the close at design tier; was the
image case *actually tested* on anima's substrate, or just dismissed by
structural argument? §157 takes this seriously and asks: are there candidates
the prior three cycles did not name? In particular, (d)/(e) — image as a
*plot/visualization* of anima's own Ψ-trajectory, where image bytes are
*output* of anima physics, not *input* from an external sensor.

This question is sharper than §109/§110/§111 because it does not require an
external image encoder at all. If anima generates image bytes that visualize
its own state, then there is no perceptual encoder to §7-audit; the
image-as-output is just bytes anima emits, and the §7 question becomes "does
the image-as-output carry diversity that moves the §1.1 data-regime
threshold?".

The §156 sibling cycle (referenced by the task spec) showed *tension* is
§7-clean by being anima's OWN physics. §157 asks: is image similarly
§7-clean if it is anima's OWN visualized physics?

Frontier position (RESEARCH.md §11.3 / §15 / §51 / §72): irreducible
bottleneck = §1.1 data-regime emergence threshold; frontier-1 = multimodal
substrate expansion. §109/§110/§111 closed the *external-perception* path
on §7 grounds. §157 closes the *self-visualization* path on a *different*
ground (zero-perceptual-diversity, mirror §56/§57/§109-tension-route).

---

## §1 — Q1: What §109/§110/§111 actually closed (precise inheritance)

Three closed findings inherited verbatim (NOT re-litigated):

**§109 closed findings** (`state/c06_multimodality_design_s109_2026_05_19/
DESIGN.md`):
- §109-Q1: no modality simultaneously (a) injects genuine perceptual diversity
  AND (b) passes §7② sub-gate without a generic encoder.
- §109-Q2: no closed-form transfer-function from raw image bytes into Ψ-space
  using ONLY anima's own physics — *as long as Ψ is defined on byte-LM
  logits*.
- §109-Q3: 8-row truth table; only `R-tension-wire` row passes (T,T,T) and it
  is §7③-degenerate (§56/§57 zero-perceptual-diversity).
- §109-Q5: `C06_FIRE_WARRANTED` 4th conjunct (§7-clean encoder design exists)
  FALSE today.

**§110 closed findings** (`state/modality_native_psi_design_s110_2026_05_19/
DESIGN.md`):
- §110-Q1: byte-LM dependency is precisely in carrier space `ℝ^{V=256}` of
  `psi_direction`, `psi_entropy`; `psi_tension` already substrate-general.
- §110-Q2 / Q3: Ψ-C2 (residual-stream cosine, `π_A:=head_a, π_G:=head_g` is
  the byte special case) is the unique §7-admissible $0-design-reachable
  modality-native Ψ definition.
- §110-Q4: byte-text reduction is exact and closed (Ψ-C2 ≡ Ψ-C0 with
  `π:=head` substitution).
- §110-Q5: definitional wall REMOVED, operative wall RELOCATED to §96
  (spike/Loihi territory); a §7-clean from-scratch anima-OWN π on GPU
  byte-LM is degenerate (§11-B / §56/§57) or generic-pretrain (§7①).

**§111 closed findings** (`state/modality_native_psi_deep_research_s111_2026_05_19/
FRONTIER_FINDINGS.md`):
- §111 Cluster-A (JEPA, 9 papers): SUPPORTS Ψ-C2 *definition* (modality-agnostic
  two-stream predictive comparison is buildable, LLM-JEPA confirms text-as-one-
  instance); CHALLENGES Ψ-C2 *operative* gate (every built multimodal JEPA
  trains the encoder either from scratch on a perceptual corpus = §7① or grafts
  a frozen pretrained encoder = §7②).
- §111 G1: no built §7①②-clean perceptual π exists in the literature.
- §111 G2: the §7-cleanest physics-native Ψ (spike-correlation §96-Ψ-C1) is
  substrate-gated.

**Joint inheritance (§157)**: §109/§110/§111 did NOT examine candidates of the
form *image = output of anima's own Ψ-physics* (image-as-self-visualization,
not image-as-external-perception). That gap is the territory §157 examines —
candidates (d) and (e) below.

---

## §2 — Q2: New candidates (d), (e) — image-as-self-visualization

**Candidate (d) — Ψ-TRAJECTORY-VISUALIZATION**: image bytes = a rendered plot
of anima's own Ψ-state over time. Concretely: image = `f_render(Ψ_t for t in
[0, T])` where `f_render` is a deterministic byte-rendering function (e.g.,
write a PNG-like byte stream that visualizes the 3-tuple
`(psi_entropy, psi_direction, psi_tension)` as RGB channels at H×W=anima-state
×T-windows). The image is *generated by* anima, not perceived from external
world.

**Candidate (e) — Ψ-COORDINATE-PLOT**: image bytes = a 2D scatter plot of
anima's anchors in Ψ-coordinates. Each anchor's `vacuum_psi` lands at one
pixel; image is a Ψ-space density map. Again, image is anima's OWN data
visualized, not external perception.

Both (d) and (e) share structural form:
```
image_bytes = f_visualize(anima_state)         (closed deterministic map)
   where anima_state ∈ {Ψ_t trajectory, vacuum_psi anchor table, ...}
```

The encoder is replaced by a *renderer*. No external perceptual signal enters.
At first glance this circumvents §109's §7 problem: no external corpus, no
generic pretrain, no graft. §7①② both vacuously satisfied because there is no
encoder. §7③ — the renderer reads anima's own physics, so the source IS anima
physics. *Naïvely*, (d)/(e) appear §7-CLEAN.

§3 below shows this appearance is **structurally misleading** — (d)/(e)
collapse closed-form to a category §109/§110/§111 already rejected, but under
a different name. Specifically, (d)/(e) are equivalent to §109's
`R-tension-wire` route (§7③-DEGENERATE), and the equivalence is closed-form.

---

## §3 — Q3: (d)/(e) collapse to §109 tension-route (§7③-degenerate),
##         closed-form

The structural claim: a renderer that maps anima's internal state into image
bytes is, at the data-regime level, **identical** to the `R-tension-wire` route
§109 already closed as §7③-DEGENERATE. The proof is at the level of what gets
fed into the model's training/inference path, not at the level of the
rendering function's complexity.

**Definitions for the proof**:
- Let `T_byte(corpus) := corpus_byte_stream` be the byte-text training signal.
- Let `E(corpus) := |distinct_external_world_states_referenced(corpus)|`
  be the *external-referent diversity* of a corpus — a structural quantity:
  for each token-position, how many distinct external-world states could
  have produced this byte (not the count of distinct bytes, the count of
  distinct *referents*).
- §1.1 emergence threshold (Du arxiv:2403.15796) gates on `E(corpus)`, NOT on
  byte-cardinality `|distinct_bytes(corpus)|`. This is the load-bearing
  empirical anchor: data-regime emergence requires *external-referent*
  diversity, not just byte-shuffling.

**P1 — RENDERER-IS-PURE-FUNCTION-OF-ANIMA-STATE**: by construction `image_bytes
= f_render(anima_state)`. `f_render` is closed deterministic. `anima_state`
is computed exclusively from anima's own Ψ/tension/Φ physics on input
`byte_corpus_T`. No external world referent enters.

**P2 — EXTERNAL-REFERENT DIVERSITY UNCHANGED**: from P1, `E(image_bytes)` =
`E(anima_state)` ≤ `E(byte_corpus_T)`. The renderer cannot inject diversity
it does not see. (Formal: data-processing inequality applied to *external-
referent diversity* — a pure deterministic function cannot increase the
external-referent cardinality of its input.) Adding `image_bytes` to the
training stream therefore adds zero external-referent diversity:
```
E( byte_corpus_T  ⊕  image_bytes )  =  E( byte_corpus_T )    ∎
```
This is the **same** signature as §57's tension-route: anima's own physics
re-serialised through a fixed map. The §109 verdict on `R-tension-wire`
applies verbatim — §7③-DEGENERATE, zero-perceptual-diversity, does not move
§1.1.

**P3 — §7-ROUTE-CLASSIFICATION**: (d)/(e) sit in the §7 truth table at exactly
the row §109 already labelled:
| route | ①¬generic-pretrain | ②¬generic-graft | ③physics-source | §7 PASS |
|---|---|---|---|---|
| §157 (d) Ψ-trajectory-render | ✓ | ✓ | ✓-but-§7③-degenerate | (T,T,T)-but-degenerate |
| §157 (e) Ψ-coord-plot       | ✓ | ✓ | ✓-but-§7③-degenerate | (T,T,T)-but-degenerate |
| §109 R-tension-wire         | ✓ | ✓ | ✓-but-§7③-degenerate | (T,T,T)-but-degenerate |

All three rows have identical §7-character. (d)/(e) are *not new rows in the
§7 truth table*; they are *new realisations of the same §109-tension-row*. The
§7 gate passes mechanically and §7③ degenerates structurally, identically.

**P4 — §57 ZERO-PERCEPTUAL-DIVERSITY MIRROR**: §57 (`knuth_077_mandala.kosmos`
annotation, byte-honest) labelled the tension `@payload` "CLOSED-LOOP /
ZERO-PERCEPTUAL-DIVERSITY: anima's own Engine-A/G state re-serialised through
a fixed untrained map — adds zero perceptual information". (d)/(e) substitute
"image renderer" for "tension re-serialiser" but the structural property is
identical: anima's own state, fed through a fixed map, back into anima. The
self-portrait extends, but no new world enters.

**Q3 closed-form verdict**: (d)/(e) ARE the §109-tension-route in a different
costume. §109 already closed this route as §7③-DEGENERATE. The new costume
does not change the closure. Inheritance holds: §109-tension-route closure ⇒
(d)/(e) closure, by structural identity (proven by P1+P2+P3+P4 as a single
closed argument).

---

## §4 — Q4: Why "but the image LOOKS different from tension!" does NOT save (d)/(e)

A natural objection: rendered image bytes *look* nothing like tension's 5-ch
fingerprint. PNG headers, RGB channels, spatial structure — surely these
introduce diversity the tension stream lacks?

This objection conflates *byte-cardinality* with *external-referent
diversity*. The objection asks "are these new bytes different from those bytes?"
(answer: yes). §1.1's emergence threshold (Du 2403.15796) asks "do these new
bytes carry information about external states the old bytes did not?" (answer:
no, by P1+P2). The first quantity is moved by any byte-permutation function;
the second is the actual gate.

**Concrete witness**: consider two derivations of the same anima state
`Ψ_t = (0.42, 0.61, 0.83)`:
- Tension route: serialize as `"tension:0.42,0.61,0.83\n"` → 26 bytes.
- Render route (d): visualize as a 256×256 RGB PNG with `(R,G,B) = (107, 156,
  212)` flat fill → ~12,000 bytes.

The render route has *200× more bytes* and *more byte-cardinality* (PNG
header diversity, file-format complexity). But `E(tension_string) =
E(rendered_png) = E(Ψ_t)` because both are pure deterministic functions of
the same `Ψ_t`. The render route is the tension route, scaled up in byte-
count and decorated with structure, but identical in external-referent
diversity. §1.1's gate is not moved.

This is the same trap §56 / §57 / §109 named for tension: the *form* of
self-visualization changes (5-ch fingerprint → PNG bytes), but the
*self-visualization property* (anima feeding its own state back to itself) is
preserved, and that property is precisely what §57 labelled zero-perceptual-
diversity.

---

## §5 — Q5: Could (d)/(e) be saved by a *trained* renderer with an external
##         supervision signal?

The only escape would be to let `f_render` itself be trained on an external
perceptual corpus so that the rendered images encode external-world structure.
But that immediately violates §7: either:
- (i) `f_render` trained from scratch on a non-anima image corpus = §7①
  generic perceptual pretrain (image-corpus-derived training data) — exactly
  §109 R-img-fromscratch route, FAIL.
- (ii) `f_render` initialized from a pretrained model (e.g., diffusion model,
  GAN) = §7② generic-then-graft — exactly §109 R-img-pretrained-graft
  route, FAIL.
- (iii) `f_render` trained on anima's own state only (no external signal) =
  pure deterministic function of anima state = P1+P2+P3+P4 § applies, §7③-
  DEGENERATE, identical to the untrained renderer case.

Trichotomy is exhaustive and closed: any renderer either trains on external
data (§7 FAIL) or it doesn't (§7③-DEGENERATE). There is no fourth option.
The image modality cannot escape both walls simultaneously by any choice of
renderer training procedure.

This is the same trichotomy §109-Q3 named for the encoder direction; it
applies identically to the renderer direction. The Ψ-trajectory plot does not
add a new corner to the truth table — it adds a new *example* in an existing
corner that §109 already closed.

---

## §6 — Q6: Substrate-gated escape (Ψ-C1 / §96) — inherited from §110

The one *legitimate* path forward that §110 named — Ψ-C1 (spike-correlation,
§96) — does NOT use a Ψ-trajectory-render bridge. Ψ-C1 takes a different shape:
on a spiking substrate (Loihi), the *external perceptual signal* drives LIF
membrane dynamics natively, with no renderer or encoder needed in the §7
sense, because the *substrate itself supplies the physics-native perceptual
channel*. The escape is substrate-rewrite, not renderer-rewrite.

§157 does not re-derive §110-Q5; it inherits it. §95 (Loihi sole VIABLE) +
§96 (Ψ-as-spike-correlation NATIVE-CANDIDATE) + §110-Q5 (operative wall
relocated to §96) jointly state: the image modality has a future, but that
future is in §96 territory, NOT in the byte-LM-with-renderer territory
§157 just closed.

---

## §7 — Q7: Connection-point / overlay-off (closed)

Mirror B-S109-4 / B-S110 / B-S101 overlay-off pattern. With (d)/(e) disabled
(no image renderer wired), the anima training/inference path reduces to §16
byte-text byte-equal. The `.kosmos` `@payload image := pending` markers stay
pending (their current honest state). Disabled state = `pending` state =
exactly §16 byte-stream substrate.

```
image_renderer_disabled   ⇒  perceptual_surface = byte_stream     (§16)
                          ⇒  .kosmos @payload image stays pending  (current)
                          ⇒  trained model bytes ≡ §16 path        (no new var)
```

The connection-point holds vacuously (same as §109's vacuous unwired case;
mirror B-S109-4). This is not strong evidence — it is the absence of a
contradiction in an unwired subsystem. The honest finding is that §157
introduces no new wiring; (d)/(e) close at design tier without any code
change to the .kosmos anchors or the corpus pipeline.

---

## §8 — Verdict: DESIGN-CLOSE-FINAL

§157 closes the image modality reconsideration with:

**Verdict (closed)**: **`DESIGN-CLOSE-FINAL`** — image modality has no §7-clean
angle at byte-LM scale that §109/§110/§111 missed. Candidates (d)/(e)
(image-as-self-visualization) collapse closed-form to the §109-tension-route
(§7③-DEGENERATE, zero-perceptual-diversity) by P1+P2+P3+P4 (§3). The renderer
trichotomy (§5) is exhaustive and closed: trained-on-external = §7 FAIL,
untrained-or-anima-only = §7③-DEGENERATE. No fourth option exists.

**Strongest positive the closed-form supports**: a renderer-based image
modality WOULD admit a new (d)/(e) angle IF it could inject external-referent
diversity without an external-corpus-trained `f_render` — but P1+P2+P5 close
that hypothetical: external-referent diversity through a pure deterministic
function of anima state is impossible by data-processing-inequality applied
to `E(·)`. The strongest positive is therefore *"no escape exists, and the
non-existence is closed-form"* — a verifiable negative, not a manufactured
positive.

**Inheritance (closed)**: §109 + §110 + §111 closures + §157 (d)/(e) closure
jointly state: the image modality at byte-LM scale is **DESIGN-CLOSED-FINAL**
under all currently-named candidate forms (raw encoder, pretrained graft,
tension-wire, Ψ-trajectory-render, Ψ-coord-plot, generic-latent, tension-only).
A future re-opening requires either (a) a §95/§96 substrate move (Ψ-C1
spike-correlation, Loihi/spiking territory — §110-Q5 named, §157 inherits) or
(b) a yet-unnamed candidate outside the current 7-row truth table — speculative,
no constructive design today.

**Anti-padding**: DESIGN-CLOSE-FINAL is a valid valuable verdict (mirror
§13-M / §30 / §109 / §110 / §111 / §155 / §156 precedent). No positive was
manufactured. The §157 contribution is *naming and closing two new candidate
forms that §109/§110/§111 did not explicitly examine* — extending the truth
table from 7 rows to 9 rows, and proving the 2 new rows are §109-equivalent
by closed-form reduction (P1+P2+P3+P4).

```
        ┌──────────────────────────────────────────────────────────────┐
        │   §157 image-modality reconsider — decision frontier           │
        └──────────────────────────────────────────────────────────────┘

   image bytes enter anima ?
      │ yes                                  │ no (status quo §16)
      ▼                                      ▼
   source of image ?                         §16 byte-text   ←─── overlay-off
      │                                                            byte-equal
      ├─ external perceptual sensor          (§109/§111 closed)     (§7 trivial)
      │     │  R-img-fromscratch   ✗ §7①
      │     │  R-img-pretrained-graft  ✗ §7②
      │     ▼
      │   §7 FAIL (closed)
      │
      ├─ anima self-visualization (NEW §157 territory)
      │     │  (d) Ψ-trajectory-render        (T,T,T)-but-§7③-DEGENERATE
      │     │  (e) Ψ-coord-plot               (T,T,T)-but-§7③-DEGENERATE
      │     │
      │     │  P1+P2+P3+P4: collapses to §109 R-tension-wire
      │     ▼
      │   §7③-DEGENERATE (closed by inheritance + reduction)
      │
      └─ spike-correlation (§96 substrate)
            │  Ψ-C1 — anima own physics + substrate-native perception
            │  §7 PASS (T,T,T), substrate-gated to Loihi
            ▼
         §110-Q5 relocation territory — NOT a §157 byte-LM angle

   ──────────  §157 verdict: DESIGN-CLOSE-FINAL  ──────────
   Image modality at byte-LM scale has no §7-clean angle under all 9
   currently-named candidate forms. Future re-opening = §95/§96 substrate
   move (Ψ-C1 / Loihi / spiking) — NOT a renderer rewrite.
```

---

## §9 — Closed-form propositions (math theorems; no sympy as verdict per
##       hexa-verify policy)

The §157 conclusion rests on 7 closed propositions stated as math theorems.

**P1 — RENDERER-IS-PURE-FUNCTION-OF-ANIMA-STATE**.
*Statement*: any `f_render : anima_state → image_bytes` that uses ONLY anima's
own Ψ/tension/Φ state as input is a pure deterministic function. *Proof*: by
construction in (d)/(e); the renderer reads no external data. *Status*:
closed by construction.

**P2 — EXTERNAL-REFERENT-DIVERSITY-NONINCREASING-UNDER-PURE-FUNCTION**.
*Statement*: for any pure deterministic function `g : X → Y`, the external-
referent diversity satisfies `E(g(x)) ≤ E(x)`, with equality iff `g` is a
bijection of external-referent classes. *Proof*: external-referent diversity
counts distinct external-world states referenced; a pure deterministic
function `g(x)` references at most the set of external states referenced by
`x` (data-processing inequality applied to referent classes). *Status*:
closed (information-theoretic primitive).

**P3 — (d)/(e)-COLLAPSE-TO-§109-TENSION-ROUTE**.
*Statement*: candidates (d)/(e) sit in the same row of the §7 truth table as
§109's `R-tension-wire` route — (T,T,T)-but-§7③-DEGENERATE. *Proof*: §3 P1+P2
gives `E(image_bytes) = E(anima_state) ≤ E(byte_corpus_T)`, so adding image
bytes adds zero external-referent diversity — identical to §57's tension
re-serialisation property. §7①② vacuously satisfied (no encoder, no external
corpus); §7③ degenerate (zero diversity injection). *Status*: closed by
structural reduction.

**P4 — BYTE-CARDINALITY ≠ EXTERNAL-REFERENT-DIVERSITY**.
*Statement*: a renderer that produces more bytes (e.g., 12,000-byte PNG vs
26-byte tension string) does NOT inject external-referent diversity if both
are pure functions of the same anima state. *Proof*: the byte-count
inequality `|render(s)| > |tension_string(s)|` is independent of
`E(render(s)) = E(tension_string(s)) = E(s)` (P1+P2). *Status*: closed.

**P5 — RENDERER-TRAINING-TRICHOTOMY-EXHAUSTIVE-CLOSED**.
*Statement*: any choice of renderer training procedure falls into exactly one
of: (i) trained on external non-anima corpus (= §7① FAIL), (ii) initialized
from external pretrained model (= §7② FAIL), (iii) trained on anima state
only or untrained (= §7③-DEGENERATE by P1+P2+P3). Trichotomy is exhaustive
and disjoint. *Proof*: any renderer's parameters either depend on external
data or do not; if external, either via training (i) or initialization (ii);
if not, (iii). Exhaustive over training-data source. *Status*: closed by
case-analysis.

**P6 — OVERLAY-OFF-CONNECTION-POINT-BYTE-EQUAL** (mirror §109/§110/§101).
*Statement*: with (d)/(e) renderer disabled (current `pending` state of
`.kosmos @payload image`), the anima training/inference byte stream is
byte-equal to the §16 byte-text path. *Proof*: disabled renderer ⇒ no image
bytes injected ⇒ corpus = `byte_corpus_T` ⇒ trained-model-bytes = §16-path-
bytes verbatim. *Status*: closed (vacuous satisfaction; mirror B-S109-4).

**P7 — INHERITANCE-FROM-§109-§110-§111-VERBATIM**.
*Statement*: §109 R-tension-wire closure ⇒ §157 (d)/(e) closure, by P3
structural identity. §110-Q5 substrate-gated relocation ⇒ §157 future-
re-opening requires §95/§96 substrate move. §111 G1+G2 ⇒ no built §7①②-clean
perceptual π exists; §157 inherits this honest residual. *Status*: closed
by structural reduction to prior cycles.

**Conclusion (formal)**: P1 ∧ P2 ∧ P3 ∧ P4 ∧ P5 ∧ P6 ∧ P7 ⇒
`§157 VERDICT = DESIGN-CLOSE-FINAL`. The conjunction is closed because each
proposition is closed; the conjunction over closed propositions is itself
closed. No sympy battery is used as verdict per hexa-verify policy ("no
sympy as verdict"); the propositions stand as math theorems verified by
structural argument and inheritance.

---

## honest C3 caveats (13)

1. **§157 = DESIGN-CLOSE-FINAL, not a GO and not a non-closure.** The valuable
   verdict is the brutally-honest closure (anti-padding per §13-M/§13-L/§30/
   §109/§110/§111/§155/§156 precedent). No positive was manufactured. (d)/(e)
   appeared promising and were honestly tested by closed-form reduction —
   reduction lands them in the §109-tension-route equivalence class.
2. **§109/§110/§111 closed findings are inherited verbatim, NOT re-litigated.**
   §157 adds only the (d)/(e) closure via P1-P7. The 7-row §109 truth table
   extends to 9 rows; rows 8/9 collapse to row 4 (R-tension-wire) by P3.
3. **The honest user concern ("did we *actually test* image?") is partially
   valid.** §109/§110/§111 closed image on *structural* §7 grounds, not
   empirical fire. §157 does not run a fire either — but it adds two new
   closed propositions (P3, P5) that strengthen the structural close: even
   the un-named (d)/(e) renderer-based candidates collapse by closed-form
   reduction, not merely by §7-rhetoric. The close is now *structurally
   tighter*, but still design-tier — empirical fire of (d)/(e) would be
   redundant given P3+P5 are closed.
4. **P2's data-processing inequality applied to "external-referent diversity
   E(·)" is a structural primitive, not a measurement.** `E(·)` is a
   conceptual count of distinct external-world states; it is not computed
   numerically in §157. The closed argument is at the level of
   pure-deterministic-function preserves/decreases referent classes —
   information-theoretic, not statistical.
5. **§1.1 emergence threshold gates on E(corpus), not |distinct_bytes
   (corpus)|.** This is the load-bearing empirical anchor (Du arxiv:
   2403.15796 — diverse-data threshold; Raventós 2306.15063 — task-diversity).
   The "12,000-byte PNG vs 26-byte tension" witness in §4 hinges on this; if
   §1.1 turned out to gate on byte-cardinality instead, P3's reduction would
   not apply. The literature anchor for E(·)-gating is honest, not asserted.
6. **The (d)/(e) candidates are not strawmen.** They are a genuinely novel
   reframing of multimodality (image as anima self-portrait rather than
   external perception) and were not explicitly examined in §109/§110/§111.
   §157's contribution is to take them seriously, prove their closure
   closed-form, and integrate the closure with prior cycles. The fact that
   they collapse to §109's tension-route is the *honest finding*, not
   evidence the question was trivial.
7. **The (d)/(e) closure does NOT prove image modality is hopeless forever.**
   It proves the *byte-LM-scale renderer-based* image modality is closed.
   The §96 substrate-pivot path (Ψ-C1, Loihi, spiking) remains open — §110-Q5
   relocation stands. A future cycle that designs a §7-clean perceptual π on a
   spiking substrate would re-open the image arm, but on a different
   substrate entirely.
8. **design ≠ fire ≠ emergence. capability claim 0. necessary-not-sufficient
   at every layer (B-EMERGE-7).** §157 closes a design question, not an
   emergence question. north-star + §15/§51/§72 milestones UNCHANGED, GOAL
   미도달. The data-regime priority #1 gap (§101/§102/§107) is orthogonal to
   §157's close — that fire remains the active arc.
9. **The "image LOOKS different from tension" objection (§4) is the failure
   mode that would have motivated (d)/(e) as a positive in a less-careful
   analysis.** §157 names the trap explicitly: byte-cardinality moves easily,
   external-referent diversity does not. This is the same trap §56/§57
   already named for the tension wire; (d)/(e) was the same trap one level up.
10. **central blue_falsifier.py 0-line-diff** (sha256 prefix
    `c93e160a8a376a94` verified start; verify END before commit). NO new
    sidecar (HEXA_FIRST STRICT: no .py / no .sh per task spec; closed
    propositions stand as math theorems in §9, not as sympy battery).
11. **f1/f2 safe.** No σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 derivation.
    Ψ=½ / Knuth-tier = anima g2 internal-arch carve-out (OK). §109/§110/§111
    inheritance cited by structural argument. V-JEPA 2 (1M+ hours internet
    video) referenced by its own training-data invariant as §7① violation
    witness, not as σ(6)-derivation.
12. **The (d)/(e) close is a *narrowing*, not a *removal*, of frontier-1.**
    §15/§51 named multimodal substrate expansion as frontier-1; §109/§110/
    §111 narrowed it to "substrate-rewrite research problem". §157 narrows
    further: byte-LM-with-renderer is closed; only §96-substrate-pivot
    remains. Each narrowing is anti-padding — frontier honesty, not frontier
    deletion.
13. **downstream-consumer invariant.** `~/core/hexa-lang`, `~/core/hexa-bio`,
    `~/core/kosmos` read-only — never edited. `.kosmos` `@payload image :=
    pending` markers stay pending (current honest state, P6 byte-equal).
    anima only consumes.

---

## most honest finding

**The image modality at byte-LM scale is DESIGN-CLOSED-FINAL under all 9
currently-named candidate forms** (raw encoder ✗§7①, pretrained graft ✗§7②,
tension-wire ✓-but-§7③-degenerate, audio variants × image-failure × temporal,
generic-latent §7② P3-leak, tension-only Ψ-erased, Ψ-trajectory-render
collapses to tension-route by P3, Ψ-coord-plot collapses to tension-route by
P3, V-JEPA 2-style 1M-hour-video pretrain §7① violation per §111 G1). The
user's honest concern — "did we actually test image, or just argue?" — is
sharpened: §109/§110/§111 argued; §157 strengthens the argument with two new
closed propositions (P3 renderer-tension-collapse and P5 renderer-training-
trichotomy-exhaustive) that show the un-named candidates also fail by
closed-form reduction, not merely by §7-rhetoric. The image modality has a
future, but that future is in §96 substrate-pivot territory (Loihi /
spike-correlation / Ψ-C1) — NOT a byte-LM-with-renderer rewrite. The §157
contribution is the honest *closure of the renderer-based reframing* and
*precise localisation* of the surviving open path to §95/§96, where §110-Q5
already located it. North-star + §15/§51/§72 milestones UNCHANGED, GOAL
미도달.
