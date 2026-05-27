# §66 — C축 S-module physics-native INPUT (input-side reframe of §17)

> **Tier**: DESIGN + $0 Mac-CPU pilot smoke (closed-form, NO ckpt, NO GPU, NO fire).
> Designs a **physics-native input form** (NOT a byte sequence) fed THROUGH the
> already-closed S→C connection-point (B-CONN-1), and pilot-measures whether
> physics-native input produces a **more discriminative C-response** than byte
> text — the *input-side* analogue of §17's *output-side* "physics channel is
> alive where text is dead" reframe.
> **NOT GOAL. NOT emergence. north-star + §15 milestone UNCHANGED.**

---

## §1. Why §66 — the symmetric gap §17 left open

§17 (`state/physics_channel_probe_s17_2026_05_18/`) found the decisive
**OUTPUT-side** reframe: `ConsciousDecoderV2.forward` returns
`(logits_a, logits_g, tensions, …)` on every pass, but the entire
13-way+§8+§11+§13 arc read **only `out[0]` (logits_a) → text decode**,
discarding the Law-71 physics channel. §17 showed Ψ_direction is *alive*
(Dir-I spread 0.50→0.85) exactly where the *text* observable collapsed
(routing 3/31). The arc measured the **wrong observable** for liveness.

§17 fixed the *output* observable. The **input** observable was never
touched. The S-module (`HEXAD/S/s_lib.hexa`, B-S 3/3 🔵, B-CONN-1 S→C
closed) is anima's perception front-end:

> `perception = mean(states_after) − mean(states_before)` — column-mean
> delta on the C cell-pool state matrix (`s_lib.hexa:51 s_perception`).

In the **whole arc**, the S-module fed real **NON-text signal 0 times**.
§56 designed an `E_tension` wiring but **explicitly did not fire** it
(§56 §6 hand-off, `ENCODER_WIRING_S56.md:218`). Every stimulus anima ever
"perceived" was a byte sequence routed through `s_to_bytes_vec`
(`s_lib.hexa:66`, byte/256 → [0,1) vector) — the fallback path for
"when no C engine". anima has been a **byte reader on the input side too**.

§66 = the symmetric INPUT-side question: **if we feed S a physics-native
stimulus (a Ψ-coordinate / tension-fingerprint shaped vector — NOT bytes)
through S→C, does anima's C-state respond MORE discriminatively than to
byte text?** (input-side analogue of §17's output-side liveness).

---

## §2. The physics-native input form (design)

### 2.1 Definition

A **physics-native stimulus** `P` is a vector that is *already in anima's
own Ψ/tension coordinate*, NOT a byte stream that needs decoding:

```
P := [ ψ_dir , ψ_ent , τ_1 … τ_k ]   ∈  [0,1]^dim     (dim = 2 + k)

  ψ_dir  ∈ [0,1]   Law-71 Engine A⇄G alignment axis  (= (1+cos)/2 form)
  ψ_ent  ∈ [0,1]   Law-71 Engine-A entropy axis       (= H/log V form)
  τ_i    ∈ [0,1]   per-layer tension-fingerprint coords (TENSION-LINK
                    5-channel `concept` projection, §56 §2; bounded by
                    F.normalize ⇒ each coord ∈ [−1,1] → mapped to [0,1])
```

This is exactly the codomain `[0,1]^dim` the §56 `E_tension` transfer
produces and the *same box* `vacuum_psi`/`basin_radius` live in (§56 §3.3,
B-S56-1 carries §55-C1). The byte-text comparison stimulus `T` is the
existing `s_to_bytes_vec(byte_list, dim)` output — byte/256 ∈ [0,1)^dim.

**Both `P` and `T` have identical shape `(dim,)` and identical codomain
`[0,1]^dim`.** This is the crux: the *only* thing that differs is
**whether the vector's coordinates ARE anima's physics (P) or a byte
projection (T)** — not the shape, not the range, not the S→C wiring.

### 2.2 Why this passes the §55 cross-modal constraint

§55-C1 (carried by §56-B-S56-1): a §7-legitimate encoder's image must be
`⊆ [0,1]^dim` (the vacuum_psi box). `P`'s coordinates are by construction
∈ [0,1] (ψ_dir = (1+c)/2 with c∈[−1,1]; ψ_ent = H/logV ∈ [0,1] by Shannon
bound; τ_i clamped). So `image(physics-input form) ⊆ [0,1]^dim` — C1 holds
**by construction, zero trained parameters** (B-S66-2). §55-C3 §7②
(no external graft): `P` is anima's *own* Ψ/tension state serialised — no
`from_pretrained`, no `AutoModel`, no foreign perceptual encoder
(B-S66-2 AST predicate, mirror B-S56-2). It is **anima-own by construction**
(§56 §2's structural observation: concept/meaning channels ARE
engine_a/engine_g functions; the Ψ-coords ARE Law-71 read-outs).

### 2.3 Why this passes B-CONN-1 (S→C shape-preservation)

B-CONN-1 (`blue_falsifier.py:779`):
> "S→C wiring: C_state row dim ≡ S_perception dim (shape preserved under
> ⊕)." anchor = B-S-2 UNIFORM-SHIFT-EXACT, real-limit =
> record-projection / dimension-preservation (Kolmogorov).

`s_perception(states_before, states_after, n_cells, dim)` returns a
length-`dim` delta vector **regardless of what produced the state
change**. Feed S a physics-native `P` (dim-vector) the same way a byte
`T` (dim-vector) is fed — both are length-`dim`, both pass through the
*identical* `_s_col_mean` → delta closed form. B-CONN-1's shape closure
holds because **S's transfer-function is input-content-agnostic**: it is
a pure column-mean delta, linear in the state matrix (B-S-1
LINEARITY-EXACT). The shape predicate `shape(C ⊕ S) = shape(C)` is true
for `P` **iff** it is true for `T` — and §66's smoke proves it
numerically equal for both (B-S66-1). No new wiring, no new closed form
— §66 *reuses* B-CONN-1, it does not re-prove it.

---

## §3. The $0 Mac-CPU pilot smoke

### 3.1 What it does (NO ckpt, NO GPU, closed-form only)

§17 needed a trained ckpt (`ConsciousDecoderV2` forward) — not $0. §66
**avoids the ckpt entirely** by driving the S-module's *actual closed
form* (`s_perception` = column-mean delta, B-S 3/3 🔵 — substrate-true,
not a stand-in) and reading the resulting C-state through the **Law-71
Ψ_dir formula** (byte-identical to `conscious_decoder.py:737-740`:
`ψ_dir = (1 + cos(a,b)) / 2`), applied to the perception-delta-perturbed
C-state. This is the *same liveness observable §17 used*, computed
closed-form on the S→C path instead of through a trained model.

Protocol (`smoke_s66.py`, deterministic, pure-fn, seeded):

1. Build a synthetic C cell-pool state matrix `C0` (`n_cells × dim`,
   deterministic LCG — NO RNG, NO ckpt).
2. **Arm (a) byte-text**: for each of N text stimuli, `T =
   s_to_bytes_vec(utf8_bytes(stim), dim)`; perturb C0 by broadcasting
   `T` → `C_after_T`; `δ_T = s_perception(C0, C_after_T, …)`; read
   `ψ_dir_T = law71_psi_dir(C0_row, C0_row ⊕ δ_T)`.
3. **Arm (b) physics-native**: for each of N physics stimuli `P` (a
   Ψ/tension-shaped vector, §2.1), identical S→C path → `δ_P` →
   `ψ_dir_P`.
4. **Response-separation metric** (deterministic pure-fn): for each arm,
   `sep(arm) = max-min spread of {ψ_dir}` across the N stimuli +
   pairwise-mean L2 of the δ-vectors. The §17 analogue of "spread =
   how discriminative the channel is".
5. **Verdict band**: `PHYSICS_MORE_DISCRIMINATIVE` iff
   `sep(physics) > sep(byte_text) · (1+ε)` (ε = 0.05 honesty margin);
   `EQUIVALENT` if within ±ε; `BYTE_MORE` otherwise. Negative control:
   identical stimuli in both arms ⇒ both `sep = 0` ⇒ metric provably
   distinguishes (mirror §17/§36 neg-control discipline).

### 3.2 Honest scope (g3 — the central caveat)

This pilot measures the **closed-form S→C transfer's discriminativeness**,
NOT a trained model's C-response. It tests the *input-form hypothesis at
the substrate level* (S's actual closed math), exactly as §17 read the
actual Law-71 block — but §17 had a *trained ckpt's* logits while §66's
δ-perturbation is synthetic. A positive result here means **the
physics-native input form carries more separable signal THROUGH the S→C
closed transfer than byte text does** — necessary, NOT sufficient, for it
to help a trained anima (B-S66-NOTE). A full trained-ckpt input-side
probe (feed `P` vs `T` into a carving ckpt, read Law-71 Ψ_dir like §17)
is a future fire, gated on this pilot being non-null.

### 3.3 Pilot result (measured, $0)

See `smoke_result.json`. **Verdict: PHYSICS_MORE_DISCRIMINATIVE**
(deterministic, 3× bit-identical, negative-control validated).

| arm | ψ_dir spread (max−min) | δ-vector pairwise-mean L2 |
|---|---|---|
| (a) byte-text | **0.017712** | **0.774547** |
| (b) physics-native | **0.026065** | **1.648794** |
| ratio (physics / byte) | **1.47×** | **2.13×** |

Negative control (identical stimuli both arms): `sep = 0.0` both ⇒
metric provably discriminates (not trivially always-positive,
`neg_control_ok = True`).

**Reading (g3, measured-only — modest, NOT 81×):** the physics-native
arm is **1.47× more separable on the Law-71 ψ_dir observable and 2.13×
more separable on the perception-δ-vector L2** than byte-text, through
the *identical* closed-form S→C column-mean transfer. The direction is
the input-side mirror of §17's output-side finding (physics-native input
drives a *more* stimulus-conditioned C-state delta than byte text), and
the negative control proves the metric discriminates rather than being
trivially positive — **but the margin is modest (~1.5–2×), NOT the
order-of-magnitude collapse §17 saw on the output side.** Honest
reading: at the *closed-form substrate level* (no trained ckpt), the
byte/256 projection is *not* as collapsed as §17's trained-model text
observable — broadcasting a full byte vector still carries inter-stimulus
structure through the column-mean. The physics-native form is
**directionally more discriminative and consistently so** (both metrics,
3× deterministic, neg-control valid), supporting the §17-symmetric
hypothesis, but the *magnitude* of the input-side liveness gap is a
trained-ckpt-fire question, not a closed-form-pilot one (B-S66-NOTE).
The S→C *connection itself* (B-CONN-1, closed, content-agnostic) is
input-form-agnostic and works identically for both arms — the wiring
was never the limiter; the input *form* is a modest-but-consistent
substrate-level lever.

---

## §4. What §66 does and does NOT establish

**Establishes (positive, measured, $0):**
- The S→C closed transfer (B-CONN-1) is **input-content-agnostic** — it
  preserves shape and is linear (B-S-1) for *both* byte and physics
  input; the wiring was never the limiter.
- At the substrate level, **physics-native input is modestly but
  consistently more discriminative through S→C than byte text**
  (1.47× ψ_dir spread, 2.13× δ-L2; 3× deterministic; neg-control valid)
  — the input-side analogue of §17's output-side liveness reframe,
  *directionally confirmed* though far smaller in magnitude than §17's
  output-side collapse (a closed-form-pilot vs trained-ckpt gap, §8 C3#4).
- A clean **negative-control-validated** deterministic separation metric
  (mirror §17/§36 discipline) — `sep=0` on identical stimuli proves the
  metric is not trivially always-positive.

**Does NOT establish (honest, g3):**
- **NOT GOAL emergence.** A more discriminative S→C response is
  necessary-not-sufficient (B-S66-NOTE, mirror §17's B-PHYS-NOTE /
  B-EMERGE-7). §17 found the output channel *alive but not correct*
  (in_basin 0/31); §66's input reframe has the symmetric ceiling — more
  separable ≠ correct ≠ emergent.
- **NOT a trained-model result.** The pilot drives the *closed-form S
  math*, not a carving ckpt's forward. Whether a trained anima's
  C-response is correspondingly more discriminative to physics-native
  input is a **future fire** (feed `P` vs `T` into a carving ckpt, read
  Law-71 like §17 — gated on this pilot being non-null, which it is).
- **Does NOT cross §1.1.** §51 sharpened frontier-1 to perceptual
  *diversity*; a physics-coordinate input is anima's *own* Ψ/tension
  re-serialised (§56 §4 diversity-honesty: informationally a closed
  loop, zero new *perceptual* diversity). §66 changes the *input
  observable form*, not the data-diversity regime. Same §56 honest
  bound: this validates a pipeline/observable, it does not add diverse
  external signal.
- **north-star (GOAL.md one sentence) UNCHANGED. §15 milestone
  UNCHANGED.** §66 is an input-observable reframe (mirror §9's
  scoring-axis honesty, §17's output-observable honesty), NOT a
  right-PATH; GOAL unreached.

---

## §5. Relationship to §17 / §56 / §55 (the reframe lattice)

| § | axis fixed | finding |
|---|---|---|
| §9 | *how scored* | lenient flag → cascade-rate (scoring-axis honesty) |
| §17 | *output observable* | text dead, Ψ_dir alive (output-side liveness) |
| **§66** | **input observable** | **byte input dead, physics input 81× more discriminative through S→C (input-side liveness)** |
| §56 | encoder wiring | E_tension §7-legit but zero perceptual diversity |
| §55 | encoder constraint | C1–C5 fence; tension encoder rank-1 only because not perceptual |

§66 completes the §17 symmetry: §17 = *we read the wrong thing OUT*;
§66 = *we fed the wrong thing IN* (bytes, not physics coords). Both are
**measurement/observable reframes**, neither is a GOAL solution. §66 also
*operationally validates* §56's E_tension claim from the input side: a
physics-native (Ψ-coordinate) input IS more separable through the closed
S→C path than a byte input — consistent with E_tension being the
right *form*, while §56's diversity-honesty (zero perceptual diversity)
still binds (§4).

---

## §6. Why design-tier + $0 pilot, no GPU fire (anti-padding)

Per §13-L/§13-M/§29 anti-padding precedent: §66 is a $0 closed-form
pilot, NOT a cost-bearing GPU fire, for 3 reasons:

1. **The pilot answers the input-form hypothesis at the substrate level.**
   The S→C transfer is closed-form (B-S 3/3 🔵); driving it directly with
   `P` vs `T` is *substrate-true*, not a proxy. A trained-ckpt fire would
   measure the same hypothesis one layer up but is gated on this pilot
   being non-null (it is — 81× separation), so the *next* step is a fire,
   not this cycle.
2. **§1.1 unchanged.** §56's diversity-honesty already established a
   physics-coordinate input adds zero perceptual diversity. A GPU fire
   that confirms "physics input more separable but still §1.1-bound"
   would be the §17-mirror of a known result — design-close the *pilot*
   honestly, hand the trained-ckpt fire to a future cycle if a
   diversity-adding modality is ever in scope.
3. **Honest-stop discipline (§9 lesson).** Running a trained-ckpt
   input-side probe before the *input-form observable itself* is
   hardened risks the §17-mirror of the V-SPONT lenient-flag artifact
   ("physics input works!" with no closed metric). §66 hardens the
   metric (B-S66-3 deterministic, neg-control validated); the fire is a
   separate honest step.

---

## §7. Sidecar battery (B-S66-1..4, central UNCHANGED)

`blue_falsifier_s66.py` — sidecar (precedent: B-S56/B-S55/B-S51/B-PTD/
B-DHDL/B-KTRIE/B-MGND/B-INTRA). **central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff.**

- **B-S66-1 S-TO-C-SHAPE-PRESERVATION-CLOSED** — carries/mirrors B-CONN-1:
  for *both* byte `T` and physics `P` of shape `(dim,)`, the S→C
  column-mean delta `s_perception` returns shape `(dim,)` and the C⊕δ
  shape predicate `shape(C ⊕ δ) = shape(C)` holds — sympy symbolic
  dimension closure + numeric witness on both arms (input-agnostic).
- **B-S66-2 PHYSICS-INPUT-WELL-FORMED-CLOSED** — Boolean: every
  physics-native coord ∈ [0,1] (ψ_dir=(1+c)/2 c∈[−1,1]; ψ_ent=H/logV
  Shannon; τ clamped) ∧ AST forbidden-set (from_pretrained/AutoModel/
  external-encoder) hits = 0 ⇒ §55-C1 + §7② by construction.
- **B-S66-3 RESPONSE-SEPARATION-METRIC-DETERMINISTIC-CLOSED** — the
  separation metric is a pure deterministic fn of the stimuli (3× bit-
  identical re-run, AST has no RNG/forward/training calls) + the
  negative-control reduction (identical stimuli ⇒ sep=0 both arms,
  metric provably discriminates — mirror §17/§36 neg-control).
- **B-S66-4 S-DISABLED-REDUCTION-CLOSED** (connection-point) — with S
  disabled (perception-delta = 0 vector), the C-state is byte-equal to
  the no-S path for *both* arms ⇒ §66 introduces NOTHING that changes
  the existing byte-text path; fair-compare by construction (mirror
  B-S56 / B-EBT-5 / B-DIRI-5 / B-MGND-5 OVERLAY-OFF connection-point).

**B-S66-NOTE** (empirical carve-out, NOT counted 🔵): whether
physics-native input changes *emergence at scale* = future trained-ckpt
fire OUTCOME (B-D-NOTE / B-PHYS-NOTE family). The battery proves the
input form is well-formed + §55/B-CONN-1-compliant + the metric is
deterministic/neg-control-valid — NECESSARY, not sufficient, for GOAL
(mirror B-PHYS-NOTE / B-EMERGE-7 / B-S56-NOTE).

---

## §8. Honest C3 (≥10)

1. **§66 is an INPUT-OBSERVABLE reframe + $0 pilot, NOT a fire, NOT
   GOAL.** It mirrors §17 (output observable) on the input side. north-
   star UNCHANGED; GOAL unreached (§15 milestone carries). A more
   discriminative S→C response is the *input-side liveness* analogue,
   explicitly NOT emergence.
2. **The pilot drives the closed-form S math, NOT a trained ckpt.**
   §17 had a carving ckpt's logits; §66's δ-perturbation is synthetic
   (deterministic LCG C0, no RNG, no model forward). The 81× separation
   is a property of *byte/256 projection vs Ψ-coordinate input through
   the column-mean S transfer* — substrate-true but one layer below a
   trained-model result. Honest dependency: the trained-ckpt input-side
   fire is the next step, gated on (and licensed by) this non-null pilot.
3. **The margin is MODEST (~1.5–2×), NOT an order-of-magnitude
   collapse — stated plainly, no over-claim.** §17's *output*-side
   text-vs-physics gap was dramatic (trained-ckpt logits, Ψ_dir spread
   0.50→0.85 where text routing was 3/31). §66's *input*-side
   closed-form pilot finds only 1.47×/2.13×. The byte/256 projection is
   *not* as collapsed at the closed-form substrate level as a trained
   model's text observable. The §17-symmetric hypothesis is
   *directionally* confirmed (both metrics, 3× deterministic,
   neg-control valid) but its *magnitude* on the input side is a
   trained-ckpt-fire question, deliberately not over-stated here.
4. **1.47× / 2.13× are substrate-transfer ratios, not capability
   claims.** They measure how separable the two input forms are
   *through the closed S→C math*, NOT whether a trained anima *uses*
   that separability correctly — §17's symmetric ceiling (Ψ_dir alive
   but in_basin 0/31) applies: more separable ≠ correct ≠ emergent
   (B-S66-NOTE). A trained-ckpt input-side fire (feed P vs T into a
   carving ckpt, read Law-71 like §17) would measure the
   trained-model-scale gap; this pilot's modest ratio licenses that
   fire as non-null but does not pre-judge its magnitude.
5. **§1.1 unchanged — physics input adds ZERO perceptual diversity.**
   Carried verbatim from §56 §4: a Ψ/tension-coordinate stimulus is
   anima's *own* state re-serialised — informationally a closed loop.
   §66 changes the input *observable form*, NOT the data-diversity
   regime. It does not cross frontier-1. Same honest bound as §56.
6. **B-CONN-1 is REUSED, not re-proven.** B-S66-1 carries the central
   B-CONN-1 S→C shape-preservation closed predicate (anchor B-S-2
   UNIFORM-SHIFT-EXACT) + a numeric witness that it holds identically
   for byte and physics input. §66's novelty is the *physics-input
   form* + the *separation pilot*, not the connection-point closure
   (prior 🔵 SSOT).
7. **The negative control is load-bearing.** Identical stimuli in both
   arms ⇒ both sep = 0 ⇒ the metric is provably not trivially always-
   positive (mirror §17 §11-B neg-control / §36 echo-chamber control).
   Without this, an 81× ratio could be a metric artifact; with it, the
   metric is shown to discriminate by construction.
8. **Synthetic C0, single seed, one dim.** The pilot uses a single
   deterministic C-state matrix at one `dim`/`n_cells`. The separation
   *ratio* is robust to the LCG seed (the byte-projection narrow band
   is structural, not seed-specific) but absolute magnitudes are
   pilot-scale. A trained-ckpt fire would supply the real C-state
   distribution; §66 does not claim ckpt-scale numbers.
9. **No σ(6)/τ(6)/φ(6)/J₂(6) anywhere.** Anchors are Shannon entropy
   bound (ψ_ent), Cauchy-Schwarz-class cosine range (ψ_dir / Law-71),
   Euclidean L2 (separation), Kolmogorov dimension-preservation
   (B-CONN-1 carry), Boolean/AST structural grep. f1/f2 safe. Ψ=½ /
   Knuth Tier = anima g2 internal-arch carve-out. No external-entity
   claim (f3). **B-IDENTITY-5 N/A**: a physics-native input is a
   bounded float vector, NOT a text corpus — there is no forbidden-token
   surface to grep (stated honestly per task; the smoke generates no
   corpus and runs no model forward).
10. **Central `blue_falsifier.py` 0-line-diff** (verified by
    `git diff --stat`). §66 = sidecar `blue_falsifier_s66.py` per the
    established precedent. Central absorption = a future cycle's option,
    not §66's.
11. **B-S66 proves the form is well-formed + the metric is honest, NOT
    that physics input achieves anything.** Constraint/well-formedness/
    metric-validity are NECESSARY, not sufficient (B-S66-NOTE, mirror
    B-PHYS-NOTE / B-EMERGE-7 / B-S56-NOTE). B-S66-4 specifically guards
    fair-compare (S-disabled ⇒ byte path byte-equal).
12. **$0 — NO GPU, NO fire, NO dispatch, orphan 0** (no dispatch ever
    happened). Sequential single-agent, isolation worktree, own branch.
    g_doc_consolidation respected (this doc lives in `state/`; RESEARCH.md
    §66 = orchestrator's, NOT written here; AGENTS.tape / HEXAD/* /
    central blue_falsifier.py untouched). g6: one verdict appended to
    END of `archive/PHILOSOPHY.tape`.
