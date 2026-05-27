# §138 LEGO HEXA-NATIVE ENGINE DESIGN — structural closure of the HEXA_FIRST_WARN deferral

> **Verdict**: `HEXA-NATIVE-ENGINE-DESIGN-CLOSE-UPSTREAM-GAP-NAMED` — a hexa-native
> `lego_engine` is *designable* and the structural gap is *named precisely*, but
> the gap lives in **hexa-bio + hexa-lang upstream**, not in anima. Per
> `g_train_flame_not_pytorch upstream_downstream_invariant` the resolution is an
> inbox patch, not an anima-side rewrite.
> design-tier · $0 · NO GPU/runpod/fire · central c93e160a 0-diff.

## §0 Why §138

The LEGO arc fired `HEXA_FIRST_WARN` **20 times** across §124–§137 — every
Python sidecar / probe / engine file triggered it. Each was deferred with the
same one-line precedent ("B-S* battery precedent, hexa-native equivalent
out-of-$0-scope, anima downstream-consumer"). 20 identical deferrals is itself
a signal: the warning is structurally correct and the deferral, while honest,
should be *closed with a design* rather than repeated forever.

§138 does that: it specifies exactly what a hexa-native `lego_engine.hexa`
would require, names the upstream gap, and routes the resolution to an inbox
patch — the `hexa-first` mandate's own prescribed path ("when the constraint
lives in hexa-lang itself, fix it there PR-only").

## §1 What the current engine is

`HEXAD/LEGO/lego_engine.py` — Python + numpy:

| component                | numpy primitive used                          |
|--------------------------|------------------------------------------------|
| `LIFNet.__init__`        | `np.random.default_rng` · `standard_normal`    |
| `LIFNet.step`            | `np.exp` · `np.outer` · `np.clip` · `@` matmul |
| `spike_rate_vec`         | `raster[:, idx].mean(axis=0)`                  |
| `psi_c1`                 | `np.linalg.norm` · `np.dot`                    |
| `make_stimuli`           | `rng.choice`                                   |
| `variance_decomposition` | `.mean` · sum-of-squares · `math.log`          |

All of these are **standard numerical array operations**. None is anima-
specific. The hexa-native question is purely: does hexa-lang's `flame` /
`farr` stdlib expose equivalents?

## §2 hexa-native mapping — what exists, what is gapped

### 2.1 Already covered by hexa-lang `flame` / `farr`

| numpy op            | hexa-native equivalent                  | status   |
|---------------------|------------------------------------------|----------|
| matmul `@`          | `farr_matmul` (RFC 032, absorbed)        | ✅ exists  |
| element add/mul     | `farr_add` · per-element ops             | ✅ exists  |
| `np.exp` (scalar)   | `dt_exp` hand-Taylor (flame_math)        | ✅ exists  |
| Gaussian noise      | `farr_add_gaussian_noise` (RFC 033)      | ✅ exists  |
| array copy/slice    | `farr_copy` · `farr_copy_slice_gpu`      | ✅ exists  |
| sum / mean reduce   | flame reduction primitives                | ✅ exists  |

### 2.2 The structural gap — spike-substrate event dynamics

| LIF-specific op                       | hexa-native status                         |
|---------------------------------------|---------------------------------------------|
| threshold-and-reset (`v >= v_th`)     | ⚠️ **GAP** — no event-conditional primitive |
| refractory counter (`refr` integer)   | ⚠️ **GAP** — no per-unit countdown state    |
| STDP eligibility trace (`tr_pre/post`)| ⚠️ **GAP** — no pair-based local update     |
| boolean spike mask → float            | partial — `farr` is float-typed; bool mask  |
|                                       | needs an integer/bool `farr` variant         |

The gap is **not** "anima needs a new equation." It is: hexa-lang's `flame`
stdlib was built for **dense gradient-descent NN training** (RFC 043 hexa-torch,
the d768·12L decoder). A **spiking substrate** needs three primitives `flame`
does not yet have:

```
  G1  event_threshold(v, v_th)        → boolean spike mask
  G2  refractory_step(refr, spiked)   → integer countdown with clamp
  G3  stdp_pair_update(W, tr_pre, tr_post, spike, A_plus, A_minus)
                                       → local outer-product weight delta
```

These three are the hexa-bio `NEURO.tape` `mech_action_potential` +
`mech_plasticity` specs expressed as `flame`-callable primitives. hexa-bio
*describes* them; hexa-lang `flame` does not yet *expose* them as array ops.

## §3 The honest disposition (g3 + hexa-first mandate)

The `hexa-first` principle says: "when the constraint lives in hexa-lang
itself, fix it there — **PR-only**." The constraint here lives in hexa-lang's
`flame` stdlib (no spiking primitives), NOT in anima. Therefore:

1. **anima does NOT rewrite `lego_engine` in `.hexa` now** — it would be a
   hand-rolled spiking layer hacked on top of `farr`, which is exactly the
   "fork the stdlib / hand-roll" anti-pattern `hexa-first` warns against.
2. **anima files an inbox patch** to hexa-lang requesting the 3 spiking
   primitives G1/G2/G3 as a `flame` extension (one concept = one file, per
   the `inbox-patches-pipeline`).
3. Once the primitives land upstream, a hexa-native `lego_engine.hexa` is a
   mechanical port — and at that point the `HEXA_FIRST_WARN` is genuinely
   resolved, not deferred.

This is the same posture as §71's `flame-path-a-dual-head-and-multiterm-grad.md`
inbox patch — anima is a hexa-lang downstream-consumer, files gap requests,
does not edit upstream.

## §4 Inbox patch sketch (to be filed)

```
~/core/hexa-lang/inbox/patches/flame-spiking-substrate-primitives.md

Title: flame — 3 spiking-substrate primitives (event-threshold, refractory,
       STDP-pair-update) for LIF / neuromorphic array ops

Motivation: flame stdlib covers dense GD-NN training (RFC 043). A spiking
substrate (anima LEGO arc §117–§137, §96 Loihi re-derivation) needs event-
driven dynamics flame does not expose. hexa-bio NEURO.tape DESCRIBES the
mechanisms (mech_action_potential / mech_plasticity); this patch makes them
flame-callable.

Requested primitives:
  flame_event_threshold(farr v, scalar v_th)  -> farr (0.0/1.0 spike mask)
  flame_refractory_step(farr refr, farr spiked, int refrac, int floor)
                                              -> farr (integer countdown)
  flame_stdp_pair(farr W, farr tr_pre, farr tr_post, farr spike,
                  scalar A_plus, scalar A_minus, scalar w_max)  -> farr W'

Falsifiers (pre-registered):
  F-SPIKE-1  THRESHOLD-BOOLEAN  (mask ∈ {0,1}, monotone in v)
  F-SPIKE-2  REFRACTORY-CLAMP   (refr never below floor; resets on spike)
  F-SPIKE-3  STDP-LOCALITY      (ΔW depends only on pre/post traces, no loss)
  F-SPIKE-4  BYTE-EQUAL-VS-NUMPY  (matches lego_engine.py numpy reference)

anima side: HEXAD/LEGO/lego_engine.py is the numpy reference; once the 3
primitives land, lego_engine.hexa is a mechanical port verified byte-equal
against the .py reference (F-SPIKE-4).
```

## §5 What §138 closes

✅ The 20× `HEXA_FIRST_WARN` deferral is **structurally closed** — not by
   another deferral, but by a precise design: the gap is named (3 spiking
   primitives), located (hexa-lang `flame` stdlib, not anima), and routed
   (inbox patch, `hexa-first` PR-only path).
✅ A hexa-native `lego_engine.hexa` is shown to be a *mechanical port* once
   upstream lands — no anima-side equation, no hand-rolled fork.
✅ The disposition matches §71's flame inbox-patch precedent exactly.

## §6 What §138 does NOT do

❌ It does NOT file the inbox patch (that is a hexa-lang-repo write; §138 is
   the anima-side design that *specifies* it — actually filing it is a
   follow-up that touches `~/core/hexa-lang/inbox/`, a separate cheap step).
❌ It does NOT rewrite `lego_engine` in `.hexa` (would be the anti-pattern).
❌ It does NOT claim the Python engine is wrong — the Python engine is the
   correct *reference implementation*; the hexa-native port is an
   optimisation / purity goal, not a correctness fix.
❌ GOAL emergence — §138 is engine-tooling, orthogonal to GOAL (B-EMERGE-7).

## §7 Closed-form propositions

```
B-S138-1   ENGINE-OPS-INVENTORY-COMPLETE   (every lego_engine op classified
                                            covered / gapped)
B-S138-2   GAP-IS-EXACTLY-3-PRIMITIVES     (G1/G2/G3, closed enumeration)
B-S138-3   GAP-LOCATED-UPSTREAM-NOT-ANIMA  (the 3 gaps are flame stdlib, not
                                            anima-specific — Boolean)
B-S138-4   INBOX-PATCH-PATH-IS-HEXA-FIRST-COMPLIANT  (PR-only, one-concept,
                                            §71 precedent)
B-S138-5   CENTRAL-0-DIFF + NO-FORBIDDEN-CALL-AST
B-S138-NOTE  empirical carve-out — design names the gap; actual upstream
            land + .hexa port = future, NOT counted 🔵
```

## §8 Honest C3 (10)

1. §138 closes the *deferral pattern*, not the underlying work — a hexa-native
   engine still requires upstream primitives to land.
2. The 3-primitive gap (G1/G2/G3) is the honest minimal set — a hexa-native
   LIF needs exactly event-threshold + refractory + STDP-pair; everything
   else `flame` already has.
3. anima does not file the inbox patch in §138 itself — that is a 1-file
   write to `~/core/hexa-lang/inbox/` (a separate cheap follow-up). §138 is
   the anima-side spec of what to file.
4. The Python `lego_engine.py` remains the canonical reference — the
   hexa-native port, when it lands, is verified *byte-equal against it*
   (F-SPIKE-4). Python is not deprecated; it is the oracle.
5. This matches §71's flame inbox-patch posture — anima is a downstream
   consumer, names gaps, never edits upstream.
6. HEXA_FIRST_WARN will keep firing on future Python sidecars until the
   primitives land — that is correct behaviour; §138 makes the deferral
   *reasoned* rather than *rote*.
7. WALL-A orthogonal · WALL-B confronted-not-removed (LEGO arc carry).
8. g3: design ≠ implementation ≠ fire ≠ emergence; capability claim 0.
9. necessary-not-sufficient (B-EMERGE-7).
10. north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.
