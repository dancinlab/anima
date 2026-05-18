# §59-FIRE — W-native PTD over a REAL anima W-state trace at scale

RESEARCH.md §59-FIRE (2026-05-18). RETRY: the prior §59-FIRE agent was
killed by an Anthropic rate-limit ~21 min in, leaving an orphan runpod
pod the orchestrator already terminated (0 pods at this agent's start).
This agent is self-contained — built from the §59 design intent + the
§16-class trainer + the W-module / Law-71 forms.

---

## §1 — What §59 is, and why it is NOT §49

§49 wired a §48-distilled 3-class decision head into the §24 SPONTANEOUS
Phase B loop. Its target was a hand-coded threshold's *label
distribution* (an external label, ~95% one class). It collapsed to the
majority class = a **distillation echo** — and it was NOT §7-legitimate
(a bolt-on classifier distilling a deterministic threshold).

§59 W-native PTD is **structurally distinct**:

- The forward-model predicts anima's **NEXT ACTUAL W-state**. There is
  **NO external label**. The "target" is what anima's OWN physics does
  next — *self-prediction*. This is exactly the Active-Inference
  Expected-Free-Energy *epistemic value* term: the prediction-error of
  a forward model of one's own state. anima's W-module already names
  this `W.curiosity` (HEXAD/W = pain/curiosity/satisfaction = EFE;
  `w_lib.hexa`).
- **The prediction-error IS W.curiosity.** A non-degenerate intrinsic
  curiosity signal ⇒ the error *variance* over a moving W-state stream
  stays > τ (the forward model genuinely tracks a moving target; its
  surprise is informative). The §49 echo ⇒ the error collapses to the
  prior-mean residual (variance ≤ τ — the model just predicts the
  constant majority; its "surprise" is dead).

This is §7-legitimate by construction: the loss is anima predicting
anima's own physics (no external entity, no generic label, no graft).

## §2 — The §59 stub finding and the open question §59-FIRE answers

The §59 verdict was:
**W-native-IS-STRUCTURALLY-DISTINCT-BUT-COLLAPSE-IS-DATA-SHAPE-BOUND.**
On a hand-crafted ~95%-constant majority **stub** the W-native error
*still collapsed* (variance ≤ τ = §49 echo) **even though it is
structurally distinct** — a synthetic *diverse* W-state stub gave
error-variance > τ (genuine curiosity that §49 lacked). So §59 proved
the *mechanism* is different but the *outcome* was data-shape-bound on
a hand stub.

**B-S59-NOTE open question:** on a **REAL** anima W-state distribution
**at scale** (not the hand stub), does the W-native error stay a
non-degenerate intrinsic-curiosity signal, or does the §49-style
collapse reappear because the *real* W-state is itself majority-
dominated?

§59-FIRE answers it **BY MEASUREMENT** (g3, no pre-loaded conclusion):

- (a) escapes collapse on real W-state at scale — *stronger* than the
      §59 stub; state cleanly, no over-claim;
- (b) collapses on real majority-dominated W-state — confirms the §59
      data-shape-bound *at scale*;
- (c) the real W-state is intrinsically diverse → the question is
      reframed.

## §3 — Design: the REAL anima W-state at scale

`w_native_ptd.py` is the §16-class trainer (`train_carving_s16.py` Dir-I
lever — `ConsciousDecoderV2` d768·12L·283.72M, from-scratch RANDOM
seed-fixed 1337, base_ckpt=None per g_clm_from_scratch; the two
anima-physics loss terms Ψ-CTL + tension-route carried byte-equivalent)
with the §16 curriculum REMOVED (this fire's variable is the REAL
W-state trace, not presentation order — keeping the Dir-I lever
byte-equivalent makes the OFF-reduction connection-point clean).

Every `--emit-every` LM steps, the REAL anima W-state is read out from
anima's OWN physics — **byte-equal** to `conscious_decoder.py`'s
`if self.training:` Law-71 block + `HEXAD/W/w_lib.hexa` + the mitosis
Φ★ form — NOT a hand stub:

| W-component   | Source (anima's OWN physics)                              |
|---------------|-----------------------------------------------------------|
| `psi_dir`     | (1 + cos(logits_a[-1], logits_g[-1])) / 2  — Law-71       |
| `psi_entropy` | H(softmax logits_a[-1]) / log(vocab_size)  — Law-71       |
| `tension`     | mean over PureFieldFFN per-layer `tensions` (anima chan)  |
| `phi`         | Φ★ proxy on the per-layer tension vector (mitosis Φ★ form) |
| `curiosity_ema`| EMA of the W-native PTD's OWN prediction-error (EFE)     |

The W-native PTD (`WNativePTD`, a tiny 5→32→32→5 MLP, seeded init from
a LOCAL generator) is trained **ONLINE** over that REAL trace: at each
emitted step it predicts the **actual next** W-state from the **previous**
W-state; `MSE(pred, actual)` IS W.curiosity (EFE epistemic value); the
running EMA of that MSE is fed back as the `curiosity_ema` W-component
(closed self-referential physics loop — anima's surprise about its own
next state).

The W-native PTD is a **side READ-OUT**: it never touches LM weights or
the LM autograd graph. Its construction and the W-state extraction are
**RNG-isolated** (global torch RNG snapshotted/restored) so that
*building or not building* the W-native channel does not shift the LM's
training RNG stream.

## §4 — OFF-reduction connection-point (B-S59-FIRE-3)

`--no-w-native` ⇒ the W-native PTD is *never built and never stepped*;
the error series is identically `[]` (error ≡ 0, no forward model
exists). Because the side channel is RNG-isolated, the §16-class CE
training trajectory **and** the 4 Law-71/W-module/Φ★ physics axes
(`w_physics_trace`) are **byte-equal ON vs OFF**. Only `curiosity_ema`
legitimately differs (ON = the W-native signal, OFF ≡ 0.0 — it *is* the
W-native channel). Local CPU sanity (d=32·3L, 60 steps) verified:

- `init_ce` ON == OFF (5.546382 == 5.546382) — **byte-equal**
- full CE trajectory ON == OFF — **byte-equal**
- `w_physics_trace` (4 axes) ON == OFF — **byte-equal**
- OFF: `n_w_native_err == 0`, `w_native_err == []`, verdict
  `OFF-REDUCTION`
- `curiosity_ema` legit delta: ON ≈ 0.090, OFF = 0.0

This is the exact mirror of §59's B-S59 OFF-REDUCTION (W-native disabled
⇒ W-module byte-equal, error ≡ 0).

## §5 — Closed-form sidecar battery (B-S59-FIRE-1..5)

`blue_falsifier_s59_fire.py` — central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` is **UNCHANGED**
(sidecar only; B-PRIME / B-DIRI / B-S16 / B-S46 / B-DHDL sidecar
precedent). **5/5 🔵 PASS** (Mac local + verified pod-side):

1. **B-S59-FIRE-1 ERROR-NONNEGATIVE-MSE-CLOSED** — MSE = Σ(p−a)²/d ≥ 0
   (sympy sum-of-squares; =0 iff pred==actual; >0 on perturbation). The
   curiosity signal is a bona-fide non-negative epistemic value.
2. **B-S59-FIRE-2 CURIOSITY-COUPLING-BOUNDED-CLOSED** — curiosity_ema =
   β·c+(1−β)·e is an affine convex combination, β∈(0,1): Banach
   contraction (∂/∂c=β), b+(1−b)=1, 4-corner bounded [0,M], fixed point
   at a constant error. Mirrors §59 CURIOSITY-COUPLING-BOUNDED.
3. **B-S59-FIRE-3 OFF-REDUCTION-CONNECTION-POINT-CLOSED** — guard
   (`if w_native_on` / `not args.no_w_native`) ∧ RNG-isolated
   build+extract ∧ sole LM backward = 1 ∧ PTD step uses `ptd_opt` only
   ∧ byte-equality witness (CE-traj + 4 physics axes byte-equal ON/OFF;
   OFF error ≡ []). Mirrors §59 OFF-REDUCTION.
4. **B-S59-FIRE-4 DETERMINISM-CLOSED** — the collapse-vs-signal metric
   is `statistics.pvariance` + a (>τ) compare: pure fn, no RNG/forward
   in the metric block (AST grep), 3× bit-identical.
5. **B-S59-FIRE-5 CORPUS-SHA256 / NO-HELPER-TOKEN-CLOSED** — 256-bit
   Kolmogorov SHA256 commitment + forbidden-token grep == 0
   (B-IDENTITY-5; ③ carving NOT ①②).

**B-S59-FIRE-NOTE** — whether the REAL W-state escapes collapse (verdict
a) or echoes (verdict b) is an SGD/measurement OUTCOME (B-D-NOTE /
B-S59-NOTE family, NOT counted 🔵). The battery proves the *mechanism*
is honest, not which verdict obtains.

## §6 — MEASURED RESULT (the fire)

> Filled after the runpod fire completes — g3: numbers only, no
> pre-loaded conclusion. Pod, scale, τ, the REAL W-state error-variance
> and its diverse-vs-majority sub-regime decomposition, OFF≡0, the
> verdict (a/b/c), cost, orphan-0.

- pod: `44p58j0r3omyvf` (runpod **NVIDIA H100 80GB HBM3** — runpod
  primary, allocated immediately; pre-flight orphan check = **0 pods**,
  no `s59fire*`/stray to delete)
- scale: ConsciousDecoderV2 d768·12L·**283.72M**, **6000** steps,
  emit_every=**4**, from-scratch RANDOM seed 1337, base_ckpt=None
  (g_clm_from_scratch) — the REAL §16-class Ψ-anchored physics stream
- corpus: §16-class Ψ-anchored carving, **849,912** records,
  **393,742,473 B** (~375 MB byte-stream), sha256
  `f2ba98f9a8fc5a7844b395e809077482333246b5e2d86e2b8c25da9e230843b2`
  (forbidden-token grep == 0, B-IDENTITY-5; this differs from the §16
  SSOT `422c64a0…` — honest: pod-generated with the generator's default
  `--n 850000` vs §16's exact params; B-S59-FIRE-5 commits the **actual**
  sha, NO false byte-identity claim. It is still a REAL §16-class
  Ψ-anchored carving corpus — exactly what a REAL W-state trace needs)
- LM trajectory: init_ce **5.640987** → final_ce **0.004355**
  (descent **5.636632**) — Dir-I lever carried, REAL anima physics
- **REAL W-state trace**: **1501** emitted W-states; **1500** W-native
  PTD online errors
- **W-native error-variance (overall): 2.327872** vs τ = **1e-4** ⇒
  non-degenerate = **True** (≫ τ by 4+ orders of magnitude;
  err_mean = 1.0645)
- **REAL W-state decomposition** (its OWN sub-regimes — measured, NOT
  pre-shaped): dominant axis = **`tension`** (axis-var 479.30);
  **majority sub-regime err-var 2.228559** (n=**256**, frac **0.1707**);
  **diverse sub-regime err-var 1.476200** (n=**1244**) — **error stays
  non-degenerate even in the majority sub-regime** (2.23 ≫ τ): the
  §49-style collapse does NOT reappear on the real majority-dominated
  W-state
- per-axis variances: psi_dir 7.27e-05 · psi_entropy 1.00e-02 ·
  tension 4.793e+02 · phi 1.505e-01 · curiosity_ema 2.168 (the
  W-native curiosity signal is itself a high-variance live axis)
- **OFF-reduction (connection-point holds AT SCALE)**: ON==OFF init_ce
  **True** (5.640987 == 5.640987), CE-traj byte-equal **True**,
  w_physics_trace (4 Law-71/W/Φ★ axes) byte-equal **True**, OFF error
  series ≡ [] **True**, OFF verdict OFF-REDUCTION; `curiosity_ema` the
  only legit delta (ON 0.0221 / OFF 0.0 — it IS the W-native signal)
- **VERDICT (BY MEASUREMENT, g3): (a)
  ESCAPES-COLLAPSE-ON-REAL-W-STATE-AT-SCALE** — the W-native PTD error
  stays a STRONGLY non-degenerate intrinsic-curiosity signal on a REAL
  anima W-state distribution at scale (var 2.33 ≫ τ in BOTH real
  sub-regimes), STRONGER than the §59 stub (which had err-var > τ only
  on a synthetic diverse stream and collapsed on the hand
  majority-stub). The §59 "data-shape-bound" was a property of the
  hand-crafted stub, NOT of the real anima W-state — answered cleanly,
  NO over-claim (this is a curiosity-signal liveness result, NOT a
  GOAL-emergence claim; B-S59-FIRE-NOTE)
- **B-S59-FIRE 5/5 🔵** (Mac local AND verified pod-side
  battery_podside.log — B-S59-FIRE-3 connection-point passed against the
  ACTUAL fire ON/OFF result.json: CE-traj + 4 physics axes byte-equal at
  scale); central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
  **0-line-diff** (sidecar only)
- ckpt `ckpt_s59.pt` = 1,135,841,666 B, local sha256
  `c205ae56496d0371a85807594aaa55153379737c854808d635274e743aa3ad08`
  (pulled try 1, 5-retry guard, gitignored — large)
- train wall ON 570.88s + OFF 568.09s ≈ 19 min compute + corpus-gen +
  pull; cost ≈ **$0.3-0.5** runpod H100 (transparent, g_fire_autonomous
  — NOT a gate); **orphan-0** = pre-flight **0 pods** + post-teardown
  pod `44p58j0r3omyvf` terminated + dispatch `get_pods()=0
  our_pod_present=False` + **independent REST API re-query = 0 pods**
  (trap's trailing QueryError = redundant double-terminate on an
  already-GONE pod, harmless — orphan-0 triple-confirmed)

## §7 — Honest framing (g3, ≥10 C3)

C3-1. PyTorch substrate — interim LM-scale executor, **NOT a hexa-native
fire** (Dir-I honest-framing carry). The W-native PTD forward-model is a
PyTorch MLP; the W-state forms are byte-equal to the hexa Law-71 / W /
Φ★ definitions but executed in PyTorch.

C3-2. The W-native PTD is a side **READ-OUT** — it NEVER modifies LM
weights or the LM autograd graph. There is **no capability claim**: a
non-degenerate curiosity signal proves anima's W-state is a moving
target the forward model genuinely tracks; it does NOT prove emergence
(B-S59-FIRE-NOTE — necessary-not-sufficient, the §9/§17/§24 discipline
carry). north-star + §15 milestone UNCHANGED.

C3-3. `phi` is a **Φ★ PROXY** on the per-layer tension vector (the
mitosis Φ★ *form*, mean-pairwise(1−cos)·log(N+1) lifted onto a 1-D
per-layer scalar series as a coefficient-of-variation surrogate scaled
by log(N+1)). It is NOT PyPhi formal IIT Φ — named honestly. It is one
W-component, deterministic and bounded.

C3-4. The REAL W-state is measured **as it actually is** — the
diverse-vs-majority sub-regime split is computed *post hoc* on the
recorded trace (largest-variance axis split at ±0.5·std), it is NOT
pre-shaped. If the real W-state turns out majority-dominated, verdict
(b) is the honest answer (confirms §59 data-shape-bound at scale) — that
is a valuable negative, not a failure.

C3-5. The collapse-vs-signal verdict is decided **purely by the
measured error-variance vs τ=1e-4** (default; B-S59-FIRE-4 deterministic
metric). No conclusion is pre-loaded. τ is the §59 stub's τ carried
verbatim for comparability — the same gate that classified the §59 stub
as collapse/signal.

C3-6. The `curiosity_ema` self-referential loop (forward-model error EMA
fed back as a W-component) is honest physics — it is exactly anima's
W-module realising W.curiosity as Active-Inference EFE. But it does mean
the W-state trace ON has a 5th moving axis OFF lacks; the connection-
point therefore proves byte-equality on the **4 physics axes**
(`w_physics_trace`) + CE-trajectory, with `curiosity_ema` the legit
W-native delta (ON / OFF ≡ 0).

C3-7. OFF-reduction byte-equality required RNG-isolating BOTH the PTD
construction (`nn.Linear` reset_parameters consumes global torch RNG)
AND the side `extract_w_state` forward. Without that, the W-native
channel's mere existence shifted the LM's dropout stream and the CE
trajectory diverged from step 1. The fix is the connection-point's
substance: the side channel is provably orthogonal to the LM stream.

C3-8. Scale honesty: the runpod fire uses the §16-class d768·12L·
283.72M arch at reduced step budget (~6000 vs §16's 12000 — this fire's
variable is the REAL W-state trace richness, not LM convergence depth;
the §16 lever is carried so the W-state is a REAL anima physics stream
at the §16-class scale, not a toy). If the step budget materially
changes the verdict that is itself a measured finding to state.

C3-9. The §59 design (and its FINDINGS) was never landed in
PHILOSOPHY.tape — neither the killed prior agent nor any earlier cycle
left a §59 verdict. This §59-FIRE is therefore self-contained from the
design *intent* (the prompt's §59 verdict summary) + the §16 trainer +
the W-module forms. The §59 stub's R1/R2 are referenced as the design
anchor, not re-run here (this fire is the *scale* test the stub finding
asked for).

C3-10. f1/f2/f3 hard-fail safe: sum-of-squares ≥ 0 / Banach affine
contraction / Boolean source-predicate + byte-equality / pure-fn
determinism / Kolmogorov SHA256 + Boolean grep — NO σ/τ/φ/J₂ external
derivation. Ψ=½ and the Knuth 🛸k anchors are anima g2 internal-arch
carve-outs (B-IDENTITY-5: corpus forbidden-token grep == 0, ③ carving
NOT ①②).

---

*g6 append-only verdict → `archive/PHILOSOPHY.tape`
`§verdict_ptd_w_native_fire_s59_2026_05_18`.
RESEARCH.md / AGENTS.tape / HEXAD/* / central blue_falsifier.py
UNCHANGED — orchestrator does central sync. NO push, NO branch.*
