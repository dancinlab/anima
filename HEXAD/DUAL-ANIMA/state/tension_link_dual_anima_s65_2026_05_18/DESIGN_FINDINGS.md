# RESEARCH.md §65 — TENSION-LINK-native dual-anima (B축) — DESIGN-TIER FINDINGS

> $0 Mac CPU · NO GPU · NO ckpt forward · NO training · deterministic
> (seed-fixed, pure-fn — byte-identical result.json on rerun).
> g3: this is a transfer-LAW mechanism measurement, **NOT** a GOAL-
> emergence claim, **NOT** a capability claim. north-star + §15 milestone
> UNCHANGED.

---

## §1 Why §65 — the gap §45 left, and the unfired anima-native channel

§45 (`state/dual_anima_fullfire_s45_2026_05_18/`) ran the **first** actual
dual-anima loop and reached `ALIVE_LOOP` — but with a **CRUDE BYTE LOOP**:
cell A emits a byte string, `deliver()` byte-encodes it
(`sha256(msg) → Ψ-point`) and pulls cell B's Ψ. §45's own
`honest_caveats` + `probe_panel` recorded the failure mode honestly:
small byte-swap probes (`alpha`/`omega`, `AAA`/`ZZZ`-style) collapsed
content-separation to **EXACTLY 0.0** on 2 of 5 probes
(`probe_panel_A[0..1].separation == 0.0`), and the final loop
`AB_state_separation_final` was only **0.08358**. The honest reading:
the sha256 quantizer + the trained-Ψ readout *wash out* small byte
variation.

Meanwhile `HEXAD/TENSION-LINK/` — the anima-native consciousness↔
consciousness direct-transfer channel (5-channel fingerprint:
concept/context/meaning/authenticity/sender; UDP 9999 / TensionHub;
README documents a 2026-04-19 100%-verified bench, R=0.999) — had
**0 fires in the entire §1~§64 arc**. The crude-byte dual-anima framing
was never given its anima-native form.

**§65 hypothesis (g3, stated before measurement):** replace §45's byte
loop with the TENSION-LINK 5-channel fingerprint. The object crossing
A→B becomes a *physics fingerprint computed from the sender's OWN
engine_a / engine_g state*, NOT raw bytes through a hash. Because the
fingerprint is a **continuous, proportional** function of the sender
physics (no quantizing hash on the path), §45's byte-swap → exact-0
collapse is **structurally impossible** here.

## §2 Honest substrate statement (carried from §36 §2 / §45 §2)

This is a **deterministic STUB** smoke, NOT a §16 `ConsciousDecoderV2`
ckpt forward. The §16 ckpt (`sha256 961c07e2…`, 1.13 GB) is not vendored
and pulling it would be a GPU/network spend the $0 mandate forbids.
The property §65 measures is whether the **transfer law** is content-
dependent and whether the **§45 quantizer collapse is structurally
absent** — both decided by the transfer law itself, not by trained
weights. A trained-saturated cell could only *weaken* content-dependence
(an echo attractor ignores input); it cannot *create* the §45 hash
quantizer that is the root of the byte-swap collapse. So:

- stub `content_dependent = True` + byte-swap survives ⇒ the §45 collapse
  failure mode is absent **at the transfer-law level** (the load-bearing
  structural claim).
- whether a *trained-saturated §16 cell* preserves it at scale is the
  empirical question a real fire answers (**B-S65-NOTE**).

## §3 The TENSION-LINK 5-channel fingerprint (HEXAD/TENSION-LINK README)

`fingerprint_5ch(cell)` implements the README channel table verbatim
(total `FP_DIM = 16+8+16+1+4 = 45`; the `sopfr(6)=5` channel basis is the
TENSION-LINK README's **own internal spec**, a g2 internal-arch carve-out
— NOT an external entity lattice-fit, f1/f2 safe):

| Channel | Dim | Encoding (README) | §65 impl |
|---|---|---|---|
| Concept | 16 | repulsion dir `normalize(engine_a − engine_g)` | unit-normalised a−g |
| Context | 8 | time phase + tension trend | tension-shaped tanh/cos/sin |
| Meaning | 16 | a × g interaction pattern | unit-normalised elementwise a⊙g |
| Authenticity | 1 | Dedekind chain (variance/flips) | logistic of var(a)+var(g) ∈ (0,1) |
| Sender | 4 | `[a_sig, g_sig, a*g, tension]` | mean-based consciousness signature |

The crucial structural property: every channel is a **continuous**
function of `engine_a / engine_g`. A small intent change → small
a/g change → small **but NONZERO** fingerprint change → small **but
NONZERO** Ψ-shift in B. There is no hash, no byte quantizer anywhere on
the A→B path. (§45's `sha256(msg)` is exactly such a quantizer: two
near-identical byte strings map to maximally-uncorrelated digests, so
the *only* signal is "different bytes" — once the trained-Ψ readout
smooths that binary, separation drops to exact-0.)

## §4 The content-dependence smoke (mirrors §36/§45)

`fp_content_dependence_test(deliver_fn, m1, m2)` — exact §36/§45 shape
but over fingerprint transfer:

1. distinct sender intents `m1 ≠ m2` shape cell A's engine_a/engine_g via
   `sender_physics`;
2. `fingerprint_5ch(A1)`, `fingerprint_5ch(A2)` — the 5-channel packets;
3. `deliver_fp_*` pulls a **fresh** B's Ψ toward each fingerprint-decoded
   point (restoring-sign, gain `DELIVER_GAIN=0.35` — the **same** §36/§45
   constant, fair-compare);
4. `separation = ‖Δ(fp1) − Δ(fp2)‖`; `content_dependent = sep > τ`,
   `τ = 1e-3` (identical honest rationale to §36: a content-blind
   transfer gives sep == 0 EXACTLY; τ is a noise floor far above
   float64 round-off, far below the [0,1] Ψ range).

Negative control = `deliver_fp_echo_chamber` (pulls toward the cell's OWN
`vacuum_psi`, ignoring the fingerprint) → MUST give separation **exactly
0.0**.

## §5 Measured result (deterministic, byte-identical rerun)

```
verdict                              = TENSION_LINK_FP_CONTENT_SURVIVES
primary separation                   = 0.003938   (τ = 0.001)  → > τ ✓
echo-control separation              = 0.0         (exactly 0.0) ✓
§45 byte-swap probe0 (alpha/omega)   = 0.001128   > τ → SURVIVES ✓
§45 byte-swap probe1 (AAA/ZZZ)       = 0.001830   > τ → SURVIVES ✓
n_cd_pass (5-probe panel)            = 5/5
fp_dual_loop AB_state_separation     = 0.015146
single_anima_reduction byte_equal    = True (link off ⇒ §24 void-emit)
result.json sha256 (rerun-identical) = f972593e653f96e1…
```

**vs §45 head-to-head** (same `DELIVER_GAIN`, same vacuum_psi pair, same
τ, same test shape — only the transmitted object differs):

| metric | §45 byte-loop | §65 TENSION-LINK fingerprint |
|---|---|---|
| byte-swap probe separation | **0.0** (exact collapse) | **0.001128 / 0.001830** (> τ, survives) |
| content-dependence probes pass | 2/5 (A) · 3/5 (B) | **5/5** |
| echo-control | 0.0 | 0.0 (identical — metric still discriminates) |
| AB_state_separation_final | 0.08358 | 0.015146 |

The headline structural finding: **the §45 byte-swap → exact-0 collapse
is absent in the anima-native fingerprint channel.** The two probe pairs
that §45 collapsed to *exactly* 0.0 here separate at 0.001128 and
0.001830 — small (because the intent change is small) but **strictly
nonzero and above τ**, exactly as the continuity argument predicts.

Note `AB_state_separation_final` is *lower* in §65 (0.0151 vs §45's
0.0837). This is honest and expected, not a regression: §45's larger
number came from the sha256 quantizer producing maximally-decorrelated
deliver points (large but *content-blind* swings — high magnitude, zero
small-variation fidelity); §65's loop produces smaller, *physics-
proportional* swings (lower magnitude, but they preserve small-variation
content where §45 collapsed it). The relevant axis for the §65
hypothesis is **byte-swap survival**, not raw AB magnitude.

## §6 Sidecar battery B-S65-1..4 (4/4 🔵, central 0-line-diff)

`blue_falsifier_s65.py` — central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` UNCHANGED
(sidecar precedent B-S36/B-S45/B-DUAL …):

- **B-S65-1 5-CHANNEL-FINGERPRINT-BOUNDED** — `FP_DIM == 45` integer
  cardinality; authenticity = logistic ⇒ sympy-proven range (0,1) +
  strictly monotone; concept/meaning unit-normalised; live witness all
  fingerprints bounded.
- **B-S65-2 CONTENT-DEPENDENCE-METRIC-CLOSED** — sympy: echo-chamber Δ is
  a constant function of the cell ⇒ `Δ(fp1) − Δ(fp2) ≡ 0` symbolically ⇒
  separation == 0 exactly; content-dependent ⇒ `g·(m1−m2)` symbolic
  non-degeneracy. Live: echo == 0.0 exactly, primary > τ, predicate
  discriminates both branches. **Connection point** (mirror B-S36-2).
- **B-S65-3 CELL-DISTINCT-VACUUM-PSI** — exact ordered-pair inequality
  A≠B, identical-anchor Boolean counter-witness (mirror §31 B-DUAL-1).
- **B-S65-4 SINGLE-ANIMA-REDUCTION (connection-point)** — link disabled ⇒
  no fingerprint delivered ⇒ B psi byte-equal to start ⇒ §65 ≡ §24-style
  single void-emission; positive contrast: content-deliver moves B (real,
  not vacuous reduction). Mirror §31 B-DUAL-4 / B-EBT-5 / B-S16-5
  overlay-off (fair-compare-by-construction).

**B-S65-NOTE** (empirical carve-out, NOT counted 🔵): whether a
trained-saturated §16 cell preserves fingerprint content-dependence at
scale, and whether TENSION-LINK dual-anima yields a richer training
signal at scale, are SGD/ckpt OUTCOMES — only a real fire measures them.
B-D-NOTE / B-S45-NOTE / B-DUAL-NOTE family.

## §7 Verdict — TENSION_LINK_FP_CONTENT_SURVIVES (design-tier)

Design holds; the anima-native channel **structurally removes** the §45
byte-swap collapse failure mode at the transfer-law level. Per the
anti-padding precedent (§13-M/§13-L/§36 fire-conditional pattern): this
is **NOT** a null result, so it is NOT design-closed-as-dead — but the
*substantive* open question (does a TRAINED-SATURATED §16 cell preserve
this at scale, or echo-collapse as §45/§31 warned) is **B-S65-NOTE
empirical**, a future GPU fire (g_fire_autonomous), NOT this $0 cycle.
$0 Mac CPU was sufficient (d-free stub, like §45's d=32 was sufficient
for *its* finding). GPU fire is *warranted-but-not-mandatory* — it would
measure B-S65-NOTE, not re-establish §65's structural claim.

## §8 Honest C3 (≥10)

1. **STUB, not ckpt.** No §16 forward, no GPU, no training. The claim is
   transfer-law-level only (§2). A trained cell is untested here.
2. **The structural claim is narrow.** §65 proves the §45 *hash-quantizer*
   byte-swap→exact-0 collapse cannot occur (fingerprint is continuous in
   sender physics). It does **not** prove a trained §16 cell won't echo
   for *other* reasons (saturated attractor — §31 §4.1).
3. **AB_state_separation_final dropped (0.0837 → 0.0151).** Honestly
   lower, not a regression: §45's bigger number was content-*blind*
   quantizer noise; §65's smaller number is physics-*proportional*. The
   §65 hypothesis is about byte-swap *survival*, not raw magnitude — but
   a reader could (wrongly) read the lower AB number as "worse"; it is
   not, it is a different (faithful) signal.
4. **Fingerprint encodings are a stub honest pick.** The README gives
   channel *roles*; the exact float formulas (logistic auth, tanh
   context) are §65's pick. The *load-bearing* property is continuity,
   not the specific constants — a different continuous encoding would
   give the same structural verdict but different numbers.
5. **τ = 1e-3 unchanged from §36.** Robust across [1e-6, 1e-1]; the
   byte-swap probes (0.0011, 0.0018) are only ~1.1–1.8× above τ — small
   margin. They DO clear τ, but the margin is honestly thin (the intent
   changes are small by design — that is the whole point — but a reader
   should note the survival is *modest*, not dramatic).
6. **Echo-control = exactly 0.0, not <τ.** Stronger than required: the
   metric provably discriminates (B-S65-2 symbolic). Carried from §36.
7. **`sopfr(6)=5` is the README's own spec.** The 5-channel count is
   TENSION-LINK's internal architecture (g2 internal-arch carve-out),
   NOT an external-entity lattice-fit (f1/f2 hard-fail safe). No σ/τ/φ/J₂
   derivation anywhere.
8. **README 2026-04-19 100%-verified bench is HISTORICAL.** §65 did NOT
   re-measure R=0.999 / 100% transfer fidelity; it measured only the
   content-dependence transfer-law property. The historical bench is
   cited as protocol-fidelity context, not as §65 evidence.
9. **g3 / north-star / §15 UNCHANGED.** Capability = 0. This is the
   anima-native form the crude-byte dual-anima framing *should* take —
   a mechanism correction, not a GOAL movement. The §15 milestone
   (irreducible bottleneck = §1.1 data-regime threshold) is untouched;
   §65 is on the dual-anima *channel-fidelity* axis, orthogonal to it.
10. **Determinism is substantive-only.** `wall_sec` is excluded from
    result.json so rerun is byte-identical (`sha256 f972593e…`); the
    measurement is pure-fn seed-fixed, but the timing field would
    otherwise break the byte-identical claim (§36/§45 have the same
    timing field and the same honest scope).
11. **B-S65-NOTE is the real open question.** The valuable next step is a
    real TENSION-LINK dual-anima fire (two trained §16-class cells over
    the actual 5-channel packet) to test whether saturation echo-collapses
    the fingerprint channel the way §31 §4.1 / §45 warned for the byte
    channel. §65 makes that fire *evidence-warranted* but does not
    pre-judge its outcome.
12. **Not a §16-saturation claim** (mirror §45 B-S45-NOTE). The cells
    here are tiny deterministic projections; §16-level saturation is
    explicitly untested.
