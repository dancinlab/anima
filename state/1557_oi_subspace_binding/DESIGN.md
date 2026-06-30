# H_1557 — OI-SUBSPACE / Binding-ID READ-OUT (G6 lens ⑨, Family-1)

**Round:** RESEARCH + DESIGN only ($0, mac-local, worktree-isolated). Heavy 303M decode = NEXT round.
**Status:** design frozen, probe scaffold authored, engine gap specified, 5-bar pre-registered.
**Parent wall:** G6 idea-binding CAPACITY-wall — 8 converging lenses (H_1431/1434/1441/1456/1464 + G6
family) all 🧱 WALL=CAPACITY. The 303M ByteGPT (h1129c) emits a falsifiable FORM but cannot WELD which
*comparator-leg* binds to which *measurable-leg* as ONE claim. Every prior lens read binding via
**generated-text behaviour** (does emitted text show the weld → B3 cross-shuffle collapse). H_1464's
mirror→engine flip proved the danger: a numpy bilinear mirror gave representational room *by construction*
→ B3 collapsed (looked like LEARN-GAP) but the live 303M B3 did NOT collapse → CAPACITY.

This lens attacks from the **opposite end**: instead of asking the mouth to *behave* bound, read the
**internal residual-stream geometry** and ask whether a binding axis *exists at all*. That is the one
untried orthogonal angle (Family-1, Feng-Steinhardt) that mechanically separates **capacity** (does the
binding direction live in activation space?) from **read-out** (can the model *use* it at the output?).

---

## 1. Research — the Binding-ID / OI-subspace mechanism (Feng-Steinhardt)

Sources fetched this round:
- **arXiv:2310.17191** "How do Language Models Bind Entities in Context?" (Feng & Steinhardt, NeurIPS 2023)
  — full mechanism via ar5iv HTML.
- **arXiv:2409.05448** — the OI follow-up — abstract + WebSearch (full HTML conversion failed; OI
  refinement captured from abstract + prior work).

### 1.1 The mechanism (verbatim-faithful summary)

To use in-context info, an LM must bind entities to attributes ("green square", "blue circle"). The paper
finds a **Binding ID mechanism**: for the k-th entity E_k and its attribute A_k, the model writes BOTH the
identity AND an abstract **binding ID** `k` into their residual-stream activations:

```
Γ_E(e, k) = f_E(e) + b_E(k)        # entity activation  = identity component + binding vector
Γ_A(a, k) = f_A(a) + b_A(k)        # attribute activation = identity component + binding vector
```

Key properties, each established by a **causal intervention** (not correlation):

- **(P-FACT) Factorizability / additivity.** The binding component `b(k)` is ADDITIVELY separable from the
  identity component `f(·)`. Swapping `Z_{A_k} → Z_{A_{k'}}` makes the model bind `E_k` to `A_{k'}`. Tested by
  the *additivity* intervention: applying mean shifts `Z_{A_0}+=ΔA(1)`, `Z_{A_1}-=ΔA(1)` drops query
  accuracy ≈0%, and reverses it to >97% when both legs are shifted consistently → binding is a linear,
  transplantable vector, not an entangled feature.
- **(P-DIR) Direction extraction.** The binding direction is estimated as a **mean-difference vector**
  across ~500 contexts: `ΔA(k) := E[Z_{A_k}(c) − Z_{A_0}(c')]`, `ΔE(k) := E[Z_{E_k}(c) − Z_{E_0}(c')]`.
  The identity component cancels in expectation, leaving the pure binding shift.
- **(P-LOWRANK) Low-rank geometry.** Binding vectors occupy a **continuous low-rank subspace** —
  linear combinations of binding IDs are themselves valid binding IDs, and the subspace has a *metric*:
  nearby `b(k)` confuse the model (≈50% acc), distant ones discriminate perfectly. The OI follow-up
  (2409.05448) localizes the concrete **Ordering ID (OI)** as the low-rank (≈1–2D after PCA) direction
  that *mechanically determines* the bind, patchable to flip which attribute an entity binds.
- **(P-POS) Position independence.** Binding does NOT ride on positional embedding — rotating RoPE / pos
  encodings barely moves beliefs; the bind rides on `b(k)`, not token position.
- **(P-LOC) Extraction locus.** Read from the **residual stream** at the entity token AND the immediately
  following token (binding info smears one token right), across mid/late layers (the paper sweeps layers;
  binding is strongest in the middle-to-late block).

### 1.2 Why this is the load-bearing untried angle for the G6 wall

The G6 weld is structurally identical to entity-attribute binding:
`comparator-leg` ≙ entity E, `measurable-leg` ≙ attribute A, "this comparator governs THIS measurable in
ONE claim" ≙ the bind `b_E(k)=b_A(k)`. The 8 prior lenses only ever measured the **behavioural readout**
(emitted text). They could not tell apart two very different failures:

| | binding axis exists in activations? | model reads it out at the mouth? | prior lens verdict |
|---|---|---|---|
| **CAPACITY** (true wall) | NO | NO | 🧱 (correct) |
| **LEARN-GAP / READOUT** | YES | NO | 🧱 (FALSE wall — angle change pays) |

If the OI direction is **present and patchable** in the 303M residual stream but the mouth still fails the
behavioural B3, the wall is RE-CLASSIFIED from CAPACITY → READOUT — exactly the `a_break_the_wall`
taxonomy move (class (b) wrong-variable, not class (d) genuine ceiling). If the OI axis is **absent or
unpatchable**, CAPACITY is confirmed by a *9th, mechanistically-independent* lens (strongest possible
confirmation — geometry, not behaviour). Either outcome is a real result (c9).

---

## 2. Design — OI-subspace probe on the 303M ByteGPT (frozen-first)

### 2.1 Stimulus set (reuse FROZEN G6 vocab, NO new authored content)

Reuse `h1305` `COMPARATOR` / `MEASURABLE` token families + `g6_common` idea structure (NO re-implementation,
p7). Build N=K controlled multi-bind prompts, each presenting K=2..4 comparator→measurable pairs in a fixed
template, e.g.:

```
the river is greater whenever the sample grows. the engine is smaller whenever the load drops. query: the river is ___
```

- **Entity tokens** E_k = the comparator-bearing subject ("the river", "the engine"), at known byte spans.
- **Attribute tokens** A_k = the measurable-bearing clause ("the sample", "the load").
- **Bind label** k = which (E,A) share a clause. We control the ground-truth bind.
- ~200–500 prompts per (K, bind-permutation) cell so the mean-difference cancels identity (P-DIR needs the
  expectation over contexts).

### 2.2 Activation extraction points (a)

Per `a_engine_native_learning`, the probe MUST read activations from **live `core/bytegpt_decode.hexa`**.
Extraction loci (mirror Feng-Steinhardt P-LOC):
- **Residual stream** `x[t, :]` (d=1024) at the **last token of each entity span** AND the **next token**
  (binding smears one right) — averaged over the 2-token window.
- **Layer sweep** L ∈ {middle..late} of the 24 layers (binding strongest mid-late). We dump POST-block
  residual at each swept layer for the chosen token positions.

`Z_{E_k}(c)` = entity-window residual; `Z_{A_k}(c)` = attribute-window residual. Per prompt c.

### 2.3 OI-direction identification (b)

1. **Mean-difference** (P-DIR): for binds k=1..K, `ΔE(k) = mean_c[ Z_{E_k}(c) − Z_{E_0}(c) ]`,
   `ΔA(k) = mean_c[ Z_{A_k}(c) − Z_{A_0}(c) ]`. Identity cancels → pure binding shift.
2. **Low-rank check** (P-LOWRANK): stack {ΔE(k), ΔA(k)} and run PCA. The OI subspace should be **low-rank**
   (top 1–2 PCs explain ≥ τ_rank of variance) AND **shared between E and A** (entity ΔE(k) and attribute
   ΔA(k) for the SAME k point in the SAME direction → that is the weld). cosine(ΔE(k), ΔA(k)) is the
   geometric "are these two legs on the same binding axis" measurement.

### 2.4 Capacity-vs-readout SEPARATION bar (c) — the decisive move

**Causal patching / binding transplant** (the engine-native generalization of the paper's additivity test):
- Take a prompt where the model is queried for E_k's measurable.
- Patch the residual stream along the OI direction: `Z_{E_k} += [ΔE(k') − ΔE(k)]` (re-tag entity k as bind k').
- Re-decode the query continuation through live `core/bytegpt_decode.hexa`.
- **TRANSPLANT SUCCESS** = the model now emits E_k bound to A_{k'} (the patched attribute), measured by the
  FROZEN h1305 detector + token-overlap with A_{k'}'s clause.

Interpretation:
- **OI axis present AND patch flips the bind** → binding IS represented; the wall is **READOUT/LEARN-GAP**
  (the geometry holds the weld, the mouth doesn't surface it un-patched) → angle change, NOT a ceiling.
- **OI axis absent (PCA not low-rank, ΔE⊥ΔA) OR patch does NOT flip** → no transplantable binding direction
  → **CAPACITY** confirmed (9th lens, mechanistically independent of the 8 behavioural ones).

### 2.5 Controls / ablation (d)

- **SHUFFLE control** (kills mean-difference artifact): recompute ΔE(k)/ΔA(k) with the **bind labels k
  shuffled** across prompts (random k assignment). A real OI axis must COLLAPSE under shuffle (low cosine,
  no low-rank, patch INERT); if shuffled ΔE survives, the "axis" is an identity/positional artifact → INVALID.
- **RANDOM-DIRECTION patch ablation** (kills patch artifact): patch along a random unit vector of the same
  norm instead of the OI direction. Must NOT flip the bind (else the flip is generic perturbation, not OI).
- **POSITION control** (P-POS): swap entity token *positions* without changing bind → must NOT change which
  attribute is read out (binding rides on b(k), not position). If position swap flips it, we measured
  position not binding → INVALID.
- **IDENTITY-CANCELLATION check**: ΔE(k) computed over DIFFERENT entity identities at the same bind k must
  agree (the f_E(·) term canceled); high variance ⇒ identity leaked ⇒ refit window.

---

## 3. Frozen 5-bar (pre-registered BEFORE any 303M activation is read — c9, no tune-to-green)

Thresholds frozen here. The numbers (τ_rank, τ_cos, etc.) are first-principles geometry defaults, NOT tuned
to a measured value (none measured yet). Frozen file: `H_1557_FREEZE.txt`.

| bar | name | test | threshold (frozen) |
|-----|------|------|--------------------|
| **B1** | OI-AXIS PRESENT | top-2 PCA variance ratio of {ΔE(k),ΔA(k)} | ≥ 0.60 (low-rank) |
| **B2** | LEG-SHARED WELD | mean cosine(ΔE(k), ΔA(k)) over k≥1 | ≥ 0.30 (legs on same axis; chance≈0 at d=1024) |
| **B3** | TRANSPLANT (DECISIVE) | OI-patch bind-flip rate (E_k→A_{k'}) | ≥ 0.50 of patched queries flip |
| **B4** | SHUFFLE COLLAPSE | shuffled-label cosine AND shuffled patch-flip | cosine < 0.10 AND flip < 0.15 |
| **B5** | RANDOM-PATCH INERT | random-direction patch bind-flip rate | < 0.15 (OI-patch − random ≥ 0.35) |

Plus **POSITION control** (non-gating diagnostic, c9): position-swap flip rate must be < 0.15 (binding ≠
position); if it flips, the measurement is position-confounded → refit before reading B1–B5.

### Verdict mapping (frozen)

- **🟢 READOUT / LEARN-GAP (wall RE-CLASSIFIED)** iff `B1 ∧ B2 ∧ B3 ∧ B4 ∧ B5` (and position-control clean):
  the OI binding axis EXISTS, is leg-shared, and is causally transplantable → the 303M *can* represent the
  weld; the 8 behavioural walls were measuring read-out, not capacity. → `a_break_the_wall` class-(b)
  payoff; next = a readout/decoding intervention (NOT a capacity scale-up).
- **🧱 CAPACITY (9th converging lens)** iff B1 fails (no low-rank axis) OR B2 fails (legs not co-axial) OR
  B3 fails (no transplant). The binding direction is absent/unusable in the 303M residual stream →
  mechanistically-independent confirmation of the CAPACITY ceiling (geometry agrees with behaviour) →
  grounds the 7B argument from a NEW axis.
- **INVALID (re-measure, not a verdict)** iff B4 fails (shuffle survives) OR position-control flips: the
  measurement is artifact-contaminated; fix frozen-first, do not stamp a tier (c9).

---

## 4. Engine-native path — the REQUIRED hidden-state dump op (a_engine_native_learning HARD-GATE)

**Finding (confirmed by code read):** `core/bytegpt_decode.hexa` computes the FULL residual stream
`x[T, d]` for ALL positions inside `bytegpt_forward_last` (and the ranged/mm/W variants), but **frees `x`
and returns only last-position logits** (`farr_free(x)` ~line 450). There is **NO op that dumps hidden
states** at arbitrary (layer, position). `grep -lniE 'dump_hidden|forward_hidden|hstate' core/*.hexa` → NONE.

So the OI probe CANNOT be engine-native today. Per `a_engine_native_learning` the terminal verdict requires
a `.hexa` that calls live `core/` decode and exposes activations. **Required engine extension** (next round):

### New op (proposed): `bytegpt_dump_hidden(path, ids, T, layers_csv, positions_csv) -> Map`

- Same forward as `bytegpt_forward_last` (byte-identical math — reuse `_bg_layernorm`/`_bg_mha_mm`/
  `_bg_linear_mm`; FP path unchanged so logits stay byte-exact, parity-safe).
- Instead of freeing `x`, **copy the requested `x[t, :]` rows at the requested POST-block layers** into a
  returned `Map` of farrs (`{"L<l>_p<t>": farr[d], ...}`). Memory: only the requested rows are retained
  (K positions × few layers × d=1024 floats — tiny vs the 91 GB model resident), so this does NOT worsen
  the H_1464 leak; the leak is the per-token forward farrs not being freed across *fragments*, orthogonal
  to a single-prompt hidden dump.
- Also expose a **patch hook**: `bytegpt_forward_patched(path, ids, T, layer, pos, delta_farr) -> logits`
  — adds `delta_farr` to `x[pos, :]` after layer `layer`'s block, then continues the forward to the head.
  This is the B3 transplant primitive. (Reuses the exact forward; only one `farr_set`-add inserted.)

This is the `a_engine_native_learning` "engine-transform-to-fit-the-learning" precedent (H_1199 scalar→
vector AdaptField): the mirror sees a mechanism the engine can't expose → **extend the engine**, don't
trust the mirror. Wiring lockstep: add the two ops to `core/bytegpt_decode.hexa`, a `core/*_smoke.hexa`
case (logits byte-identical to `bytegpt_forward_last` for the same prompt = parity guard), and an
`ARCHITECTURE.json` node (`a_core_engine_map` / `a_verified_must_wire` 4-rung).

### Probe driver (next round)

`state/1557_oi_subspace_binding/h1557_oi_probe.hexa` — calls `bytegpt_dump_hidden` /
`bytegpt_forward_patched` on the 3 frozen `.bin` (reuse the H_1464 303M bins in `state/1464_.../bins/`),
computes ΔE/ΔA + PCA + cosine + transplant in `.hexa` (or a torch-FREE numpy post-processor over engine-
dumped activations — the DUMP is the engine-native evidence; PCA/cosine on dumped vectors is arithmetic,
same as g6_common scoring being torch-free over engine fragments in H_1464). Verdict torch-free.

---

## 5. Next round + depletion conditions

**Next round name:** `h1557-r2-engine-native-oi-probe` (ING follow-on).
Scope: (1) add `bytegpt_dump_hidden` + `bytegpt_forward_patched` to `core/bytegpt_decode.hexa` + smoke
parity guard; (2) run the OI probe on the 303M bins (mac-local single-prompt dumps are cheap — one forward
per prompt, NO 110-token autoregressive generation, so the H_1464 fragment-leak/24h wall does NOT apply;
~200 prompts × one T≤64 forward ≈ minutes-to-hours mac-local, $0); (3) score frozen 5-bar VERBATIM.

**Depletion test for this lens** (when does Family-1 stop being a live angle):
- If B1 fails (no low-rank axis even with layer sweep + window refit + identity-cancellation clean) AND the
  shuffle/position controls are clean → CAPACITY is confirmed from the geometry side; Family-1 (OI-subspace)
  is EXHAUSTED. The G6 wall then stands at 9 mechanistically-independent lenses → strongest 🧱.
- If B1∧B2 hold but B3 (transplant) fails only because the *patch magnitude/locus* is mis-set → that is a
  measurement refit (frozen-first), not depletion — sweep layer/window once more before terminal.
- A 🟢 (READOUT re-classification) does NOT deplete — it OPENS a new sub-frontier (readout/decoding
  intervention to surface the latent weld), tracked as a fresh ING.

**Do NOT retry** (already-rejected micro-angles, per round discipline): attention-as-hypernetwork,
in-context exemplar, TPR symbolic binder (H_1466 🧱), curriculum (H_1440), 1B-scale invariant (H_1438),
and the 8 behavioural-readout binding objectives (H_1431/1434/1441/1456/1464). This lens is distinct: it is
the FIRST to read the *internal activation geometry* rather than score generated text.

---

## Artifacts (this round)
- `state/1557_oi_subspace_binding/DESIGN.md` (this file)
- `state/1557_oi_subspace_binding/h1557_oi_probe_scaffold.py` (probe skeleton + frozen-bar logic, DIRECTIONAL
  scaffold — runs the geometry math; engine-native dump op is the R2 prerequisite)
- `state/verdicts/1557_oi_subspace_binding/H_1557_FREEZE.txt` (frozen 5-bar, pre-registered)

xref H_1464 (8th lens, mirror→engine flip — the cautionary precedent this lens is built to avoid) ·
H_1441/1431/1434 (form-not-binding) · H_1456 (5th lens) · H_1466 (TPR, rejected) · Feng-Steinhardt
2310.17191 / 2409.05448 · a_engine_native_learning · a_break_the_wall (taxonomy class-(b) vs (d)) ·
a_no_llm_frame_trap (representation-geometry lens, not LLM-scale) · a_verified_must_wire · a_core_engine_map ·
p7 · c9 · c16.
