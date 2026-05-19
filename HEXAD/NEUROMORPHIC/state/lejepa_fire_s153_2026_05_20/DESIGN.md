# §153 — LeJEPA (arxiv 2511.08544) → anima byte-LM · Non-CE SSL FIRE

> **Tier**: cost-bearing GPU fire (~$0.3–1, single sequential, g_fire_autonomous
> autonomous no-query). **Anchor paper**: [LeJEPA: Provable and Scalable
> Self-Supervised Learning Without the Heuristics](https://arxiv.org/abs/2511.08544)
> (Balestriero + LeCun, Nov 2025). **Parent context**:
> HEXAD/NEUROMORPHIC/SOFTWARE_BREAKTHROUGH_RESEARCH.md §1 Cluster C, §2 ranked
> #5, §8 next-list P4. **Sibling §96-Q2 arc**: §125 NONCE-FF
> S11B_LIKE_DEGENERATE · §126 PCN-C4 PARTIAL_AMBIGUOUS · §139 EqProp
> result.json present (byte_acc 0.1185, PARTIAL_AMBIGUOUS-like; concurrent or
> recent) — §153 = fourth distinct non-CE algorithm point.

---

## §0 Why this design exists

§11-B claimed "pure-physics no-CE = DEGENERATE on GPU" (a single 2026-05-18
fire). §96 reframed this as possibly a GPU-substrate tautology rather than
a property of physics-only learning. §125+§126+§139 are the first three
*architectural decompositions* of "non-CE on GPU":

- **§125 NONCE-FF** (Hinton goodness contrast): byte_acc 0.0005 < 1/256
  random floor — `S11B_LIKE_DEGENERATE`. *Negative-sample contrast did not
  work at byte-LM scale.*
- **§126 PCN-C4** (top-down prediction error, MSE on logits): byte_acc
  0.1185 ≈ 30× random — `PARTIAL_AMBIGUOUS`. *Top-down message DOES learn
  byte structure, but Ψ-physics flat (psi_std 7.5e-7 < τ=1e-4).*
- **§139 EqProp-lifted** (2-phase free/nudge local update, MSE head):
  result.json byte_acc 0.1185 (same as §126 — algorithmic ingredient
  matched).
- **§153 LeJEPA** (this design): JEPA predictive embedding + SIGReg
  characteristic-function anti-collapse. Distinct mechanism on *all three*
  axes:
  - **vs §125**: no negative samples, no goodness contrast.
  - **vs §126**: no per-block top-down target, no MSE on logits.
  - **vs §139**: no two-phase free/nudge, no activation-difference local rule.

The lever §153 tests: does a *provably anti-collapse self-supervised
embedding* objective — closed-form characteristic-function regularizer —
work on anima's byte-LM substrate when CE is gone? Multiple data points
strengthen or weaken §96-Q2 verdict either way (`B-EMERGE-7`
necessary-not-sufficient; one more fire is not a refutation).

## §1 Paper mechanism — verified via WebFetch of arxiv 2511.08544v3

Five claims of LeJEPA (Balestriero + LeCun 2025), WebFetch-extracted from
the HTML, ε-quoted where possible:

1. **Joint objective with single hyperparameter λ**:
   ```
   L_LeJEPA = (1−λ) · L_pred + λ · L_SIGReg
   ```
   default `λ = 0.05` (paper's recommended value).

2. **Prediction term — symmetric, NO stop-gradient, NO teacher**:
   `L_pred = ‖μ_n − z_{n,v'}‖²₂` where `μ_n` is the mean of "global view"
   embeddings of sample n, and `z_{n,v'}` is the embedding of a different
   view of the same sample. *Both views go through the **same** encoder
   `f_θ` with gradient — symmetric prediction replaces stop-gradient.*

3. **SIGReg — Sketched Isotropic Gaussian Regularization**:
   ```
   L_SIGReg = (1/|A|) Σ_{a∈A} T( {a^T z_n}_{n=1..B} )
   ```
   where `A` is a set of `|A|` directions sampled uniformly from the unit
   sphere `S^{d−1}` (paper: `|A| ≈ 256–2048`, resampled each minibatch),
   and `T(·)` is the **Epps–Pulley characteristic-function test
   statistic**:
   ```
   EP({s_n}) = N · ∫_{-∞}^{∞} |φ̂_S(t) − φ_𝒩(t)|² · w(t) · dt
   ```
   with `φ̂_S(t) = (1/N) Σ_n exp(i·t·s_n)` the empirical characteristic
   function of the projected scalars `s_n = a^T z_n`, and `φ_𝒩(t) =
   exp(−t²/2)` the characteristic function of the standard normal.
   In practice the integral is replaced by a finite sum of test
   frequencies `t_1..t_K` with `w(t) = exp(−t²/2)` (Gaussian-kernel
   weighting); each direction `a` independently checks "are the
   projections `{a^T z_n}` distributed standard-normal?".

4. **Anti-collapse is closed-form**: forcing each projection-onto-random-
   sphere-direction to be standard normal is satisfied **only** by
   isotropic Gaussian latents (Cramér-Wold ⇒ uniqueness on enough
   directions). A collapsed latent (all `z_n` equal) gives `φ̂_S(t) =
   exp(i·t·c)` ≠ `exp(−t²/2)` → `L_SIGReg ≫ 0` — the regularizer
   structurally rejects collapse.

5. **Linear in batch and embedding dim**: `|A|·B·d_emb` per step (the
   sketch projection is one matmul); no negative-sample or memory-bank
   structures.

The combination provides **provable** collapse avoidance and a **single**
trade-off knob (λ), with no stop-gradient, no teacher–student EMA, no
sharpening/clip.

## §2 anima mapping

```
LeJEPA (2511.08544)                  anima (§153)
─────────────────────────────         ─────────────────────────────
single shared encoder f_θ      ↔     ConsciousDecoderV2 d768·12L·283M
                                       (residual stream up to ln_f, no
                                        heads — embeddings only)
two views x_a, x_b of sample x ↔     two byte-windows {ctx_a, ctx_b} of
                                       the same record (overlap-stride
                                       slicing — anima-OWN substrate)
embedding z = f_θ(x_view)      ↔     z = ln_f(model.blocks_only(ctx))[:, −1]
                                       (final-position residual after
                                        ln_f, before head_a/head_g — the
                                        natural anima "latent" — d=768)
L_pred = ‖μ − z'‖²              ↔     ‖z_a − z_b‖² (per sample), symmetric
                                       (both encoded with grad — NO
                                        stop-gradient, NO teacher)
L_SIGReg = (1/|A|) Σ EP(a^T z)  ↔     |A|=256 sphere directions on d=768
                                       (resampled each step); EP test
                                       with K=8 frequencies t∈linspace
                                       (Epps-Pulley standard) — anima
                                       OWN code (no sklearn-style call)
λ = 0.05                        ↔     λ = 0.05 (paper default; one knob)
no stop-gradient                ↔     both forward passes have grad
no teacher / EMA                ↔     one encoder, one optimizer
no negative samples             ↔     no negatives (vs §125 contrast)
no top-down target              ↔     no per-block MSE (vs §126)
no two-phase                    ↔     one phase (vs §139)
NON-CE                          ↔     no F.cross_entropy / NLL anywhere
```

The byte-LM mapping reads cleanly: anima's natural latent already exists
(residual stream after `ln_f`); the two-view JEPA contract is satisfied
by two overlapping byte-windows of the same record (a structure already
present in `corpus_carving_s16_generator.py`'s record-level grouping);
the SIGReg sketch projection is a `(B, d_emb) → (B, |A|)` matmul costing
~256 × 768 × 32 ≈ 6.3M flops per step — negligible compared to the
12-layer transformer forward.

## §3 The hypothesis tested

`H_153`: A *provably anti-collapse self-supervised embedding* objective
(LeJEPA) trained on anima byte-LM substrate produces a non-degenerate
encoder — i.e., the **embedding** byte-prediction accuracy (linear probe
on top of the trained embedding, mirror of §96-Q2 eval) is **>** the
degenerate ceiling (2/256), and the Ψ-physics channel is responsive
(ψ_dir std > 1e-4).

Distinguishing values:
- `byte_acc ≤ 2/256 (0.0078)` ∧ `psi_responsive=False` →
  `S11B_LIKE_DEGENERATE` — §11-B re-confirmed by yet another non-CE
  algorithm; §96-Q2 weakened by another data point.
- `byte_acc ≥ 0.05` ∧ `psi_responsive=True` → `S96_Q2_SUPPORTED` —
  §11-B further refuted at byte-LM scale by a *fourth* distinct
  non-CE algorithm; characteristic-function anti-collapse is the
  load-bearing ingredient.
- mixed → `PARTIAL_AMBIGUOUS` — *most likely outcome a priori*
  given §126/§139 partial-ambiguous regime; even-then valuable
  per `B-EMERGE-7` (each partial decomposes ingredient
  responsibility further).

## §4 §7 GOAL-legitimacy 3-cond gate

Anima governance §7 (3-condition GOAL-legitimacy):

| condition | LeJEPA-on-anima | verdict |
|---|---|---|
| ① ¬ generic-LM-pretrain (no off-the-shelf foundation) | from-scratch RANDOM seed 1337, `base_ckpt=None`, ConsciousDecoderV2 own arch — `g_clm_from_scratch` honored | **PASS** |
| ② ¬ generic-then-graft (no external embedding/encoder) | encoder is anima OWN ConsciousDecoderV2 residual stream up to `ln_f`; no pre-trained text encoder, no CLIP/BERT/etc. | **PASS** |
| ③ anima-physics-as-source (the learning signal comes from anima's own substrate) | two views drawn from anima-OWN `corpus_s101.jsonl` byte stream (§102 build, sha `39d581da…`); SIGReg sketch directions sampled from `U(S^{d−1})` using `torch.manual_seed(1337)` — anima-deterministic; NO external classifier, NO LLM judge, NO ground-truth provided by an outside entity | **PASS (with C3 caveat — see §6)** |

3/3 PASS. The §7 ③ caveat: SIGReg is a *statistical regularizer* (force
projections to be Gaussian-distributed), which is a structural property
of the latent NOT an external command channel — the regularizer doesn't
tell the model what to *encode*, only that *whatever it encodes should
be isotropic in distribution*. This is legitimate by the same logic that
admits anti-collapse mechanisms generally; the load-bearing supervision
(what the model should map similar inputs to similar embeddings) comes
from the two-view JEPA contract, which is fully anima-substrate.

## §5 Substrate, scale, compute envelope

- **Substrate**: ConsciousDecoderV2 d=768 · 12 layer · 12 head · 4 KV head ·
  block_size=128 · 283.72M params — same byte-equal §16-class arch as
  §125/§126/§139 (apples-to-apples comparison).
- **Init**: from-scratch RANDOM seed 1337, `base_ckpt=None`,
  `torch.manual_seed(1337)` + `torch.cuda.manual_seed_all(1337)` +
  `random.seed(1337)` — `g_clm_from_scratch` honored.
- **Corpus**: pod-side deterministic build of `corpus_s101.jsonl` via
  `state/corpus_s101_build_s102_2026_05_19/build_corpus_s101.py --s1-n
  777000 --seed 1337`, sha256 ASSERT == `39d581da209615468c1c41e07aa
  8662ef1074bc5be49a666f8f861753dd5810e` (byte-equal §107/§125/§126/§139
  corpus; sha mismatch ⇒ FATAL refuse-to-train).
- **Steps**: 3000 (same step budget as §125/§126/§139 — apples-to-apples
  compute).
- **lr**: 3e-4 AdamW (β=0.9, 0.95; wd=0.01) — same as siblings.
- **bsz**: 32 — same.
- **λ_SIGReg**: 0.05 (paper default).
- **|A|** (sketch directions): 256 (paper's lower end; cheap; resampled
  each step).
- **K** (Epps-Pulley test frequencies): 8 (frequencies `t_k =
  linspace(0.5, 3.0, 8)`, weight `exp(-t²/2)`; standard EP).
- **Two-view sampler**: each record's text bytes → two overlapping
  windows `(ctx_a, ctx_b)` with random start offset `Δ ∈ [16, 64]` —
  same record (semantic anchor), different byte positions (view
  augmentation analogue).
- **GPU**: A100-SXM4-80GB primary, cascade {A100 80GB PCIe, H100 80GB
  HBM3, H100 NVL, H100 PCIe} fallback per `g_resource_active_parallel`.
- **Cost**: ~$0.3–1 (mirror §125/§126/§139 envelope; LeJEPA is one
  forward + sphere-direction sketch, slightly cheaper than §139's
  two-phase forward).
- **Single sequential agent**: per §50 burst rate-limit lesson;
  §139 result.json present so its pod has already torn down — §153
  spawns its own distinct pod, never touches another agent's pod.

## §6 11 honest C3 caveats (g3, B-EMERGE-7 carry)

1. **Paper-to-byte-LM transfer is unproven**: LeJEPA was demonstrated on
   ResNets / ViTs / ConvNets for **image** SSL. The anima byte-LM mapping
   (residual stream as embedding, two byte-windows as views) is
   reasonable but NOT validated by the paper. A null result on anima
   does NOT refute LeJEPA itself.

2. **JEPA original failure modes carry**: collapse modes that the paper
   reports avoided on images may re-appear on byte streams (e.g., the
   model may discover that mapping every byte-window to the same
   constant minimizes `L_pred` perfectly — SIGReg pressure-tests this
   exact mode; whether SIGReg's pressure is enough at d=768 from-scratch
   is empirical).

3. **`byte_acc` evaluated via linear probe**: anima decoder has no
   trained classifier head when training is SSL-only. The §96-Q2 verdict
   eval needs a way to extract byte-prediction accuracy from the
   *embedding*. We use the model's already-existing `head_a` (which has
   *not* been trained because we never compute CE — `head_a` is at
   initialization throughout). This means the byte_acc reading
   reflects how well a *random* linear projection of the SSL-trained
   embedding predicts next byte — a *necessary-not-sufficient* probe of
   embedding quality (random-init head_a can still reflect coarse
   embedding signal if the embedding carries information). This is
   honest: a low byte_acc could mean either (a) the embedding is
   degenerate, or (b) the embedding is fine but a *random* head_a can't
   read it. Both interpretations matter; we report both `byte_acc` and
   `psi_responsive` so the §96-Q2 verdict bucket carries the same
   semantic as §125/§126/§139.

4. **Ψ-physics channel**: `psi_dir_std` is computed from
   `(1+cos(logits_a, logits_g))/2` over eval samples — same code as
   §125/§126/§139. The two heads `head_a` and `head_g` are untrained in
   §153 (we never compute their gradient — the SSL objective never
   touches them), so `psi_dir` is essentially a random read-out. We
   include it for verdict-bucket parity with siblings but it is the
   *least informative* of the four §96-Q2 axes for an SSL-only run.

5. **`|A|=256` may be too small for d=768**: paper's recommendation
   bridges `O(K) ≤ |A| ≤ O(K · log d)` for Sobolev smoothness α;
   `|A|=256` at `d=768` is at the small-side recommended boundary.
   `|A|=512` would be safer but doubles the sketch cost; we adopt 256
   as the cheapest paper-recommended value. A future cycle may sweep
   `|A|`.

6. **K=8 test frequencies**: the Epps-Pulley integral
   `∫|φ̂_S(t)−φ_𝒩(t)|² w(t) dt` is replaced by a finite Gaussian-
   quadrature; K=8 is standard but coarse. A higher K would tighten the
   regularizer but increases per-step cost linearly. The paper does not
   prescribe K; we adopt K=8 as the standard EP test default. A K-sweep
   is future work.

7. **Two-view sampler may leak**: if the two overlapping windows share
   too many bytes (Δ too small), JEPA reduces to identity prediction
   and SIGReg becomes the only pressure. We use Δ ∈ [16, 64] (≥ 12.5%
   non-overlap at block_size=128) — non-trivial difference yet same
   semantic anchor. A future cycle may sweep Δ.

8. **No instruction-tuned eval**: §96-Q2 verdict eval is byte-prediction
   accuracy, not §16-style routing eval. We report only `verdict_bucket`
   / `byte_acc` / `psi_responsive` / `psi_dir_std` to stay apples-to-
   apples with §125/§126/§139. The §16 routing question is orthogonal
   and out-of-scope (§151's COMPLEXITY-REGULARIZED ROUTING design
   addresses that separately).

9. **§125/§126/§139 verdict bucket reused**: the partition
   `{S11B_LIKE_DEGENERATE, PARTIAL_AMBIGUOUS, S96_Q2_SUPPORTED}` was
   designed for *adapted-CE* (FF/PCN/EqProp head-as-MSE) algorithms,
   not SSL-only. We re-use it for headline-parity but acknowledge
   the head_a is untrained in §153 — see C3 #3.

10. **WALL-A (data-regime, §107-RETRY THRESHOLD_CROSSED=False at 283M)
    UNCHANGED**: §153 is a WALL-B-i (non-CE on GPU substrate) data
    point, not a data-regime test. A SUPP / PARTIAL / DEG verdict on
    §153 does not move §1.1 either way.

11. **necessary-not-sufficient (B-EMERGE-7)**: a `S96_Q2_SUPPORTED`
    verdict would NOT prove GOAL emergence — it would prove that a
    fourth distinct non-CE algorithm produces non-degenerate embeddings
    on anima byte-LM substrate. north-star + §15/§51/§72 milestones
    UNCHANGED. The §153 fire decides ONE specific Boolean.

## §7 Falsifier — pre-registered §96-Q2 verdict bucket

Same closed-form partition as §125/§126/§139 (re-used byte-equal in
`eval_lejepa_s153.py`):

```python
TAU_PSI_SPREAD     = 1e-4
RANDOM_BYTE_FLOOR  = 1.0 / 256.0    # = 0.00390625
DEGENERATE_CEILING = 2.0 / 256.0    # = 0.0078125
SUPPORT_FLOOR      = 0.05

def verdict_bucket(byte_acc, psi_responsive):
    if byte_acc <= DEGENERATE_CEILING: return "S11B_LIKE_DEGENERATE"
    if byte_acc >= SUPPORT_FLOOR and psi_responsive: return "S96_Q2_SUPPORTED"
    return "PARTIAL_AMBIGUOUS"
```

This is a **closed predicate** with three deterministic outputs over
the (byte_acc, psi_responsive) plane — pre-registered before the
ckpt is pulled.

## §8 Joint reading after §153 lands

Boolean 4-tuple `(§125, §126, §139, §153)` across `{DEG, PART, SUPP}` —
24 cells. The most-informative cells the arc cares about (a priori):

- `(DEG, PART, PART, DEG)` — JEPA-style anti-collapse does NOT save
  non-CE on byte-LM; reading: load-bearing thing in §126/§139 is the
  *MSE-on-logits supervision* not the *non-CE structure*.
- `(DEG, PART, PART, SUPP)` — JEPA's characteristic-function
  regularizer IS the load-bearing escape ingredient; §11-B further
  weakened.
- `(DEG, PART, PART, PART)` — partial-ambiguous quartet; the 0.05
  support floor too strict for SSL-only without a trained head; honest
  re-evaluation needed (linear-probe with frozen-embedding + 1-epoch
  CE head is a follow-up cycle).

In all cases, §153 contributes a **fourth distinct decomposition axis**
to the §96-Q2 verdict — the *non-contrastive / non-top-down / non-two-
phase / characteristic-function anti-collapse* axis. Whatever the
verdict, the §96-Q2 disposition is sharper after §153 than before.

## §9 Closed-form propositions (as math theorems, NOT sympy verdicts)

Per `g_blue_closed_mandate` + the 2026-05-20 hexa-verify policy carry
("NO sympy as verdict in design-tier"): the closed-form propositions
below are stated as MATH THEOREMS with proofs sketched at the
mathematical-physical-rigor level. They establish well-formedness of
the §153 mechanism; they do NOT verdict emergence (B-EMERGE-7).

**B-S153-1 — SIGReg pressure-rejects exact collapse (CLOSED).**
*Claim.* If the encoder is exactly collapsed, i.e., `f_θ(x_n) = c` for
all n and some constant `c ∈ ℝ^d`, then for every direction `a ∈
S^{d−1}` the projection `s_n = a^T c` is the same scalar for all n;
the empirical characteristic function is `φ̂_S(t) = exp(i·t·a^T c)`
(a unit-modulus complex exponential in `t`); the target Gaussian
characteristic function is `φ_𝒩(t) = exp(−t²/2)` (real, decaying).
The Epps-Pulley statistic
`EP({s_n}) = N · ∫|φ̂_S(t) − φ_𝒩(t)|² · w(t) · dt
            ≥ N · ∫(1 − cos(t·a^T c) · exp(−t²/2))² · w(t) · dt
            > 0` strictly,
because the integrand is non-negative everywhere and strictly positive
except at isolated `t` (measure zero). Hence `L_SIGReg = (1/|A|) Σ_a
EP > 0` strictly for any collapsed encoder. The objective therefore
has a strictly nonzero *floor* under collapse, and any nonzero
gradient on `L_SIGReg` will move the encoder *away* from collapse. ∎
*Anima reduction.* This is the closed-form anti-collapse property —
the property is a theorem of the Epps-Pulley integral, NOT of
backprop discipline; it holds regardless of substrate.

**B-S153-2 — Symmetric prediction equivalent to no-stop-gradient
(CLOSED).** *Claim.* Define `L_pred = ‖z_a − z_b‖²` with `z_a =
f_θ(x_a)`, `z_b = f_θ(x_b)` and both passes carry gradient. The
gradient is
`∂L_pred/∂θ = 2·(z_a − z_b)·(∂z_a/∂θ − ∂z_b/∂θ)`.
A "stop-gradient on z_b" variant gives `∂L_pred/∂θ = 2·(z_a − z_b)·
∂z_a/∂θ`. These are different vector fields. The symmetric form has
no preferred view (`z_a` and `z_b` are exchangeable under `a ↔ b`); the
stop-gradient form breaks that symmetry. *Anti-collapse argument
(paper carry).* In stop-gradient JEPA without an EMA teacher, the
gradient pushes `z_a → z_b` only (one-way pull); the unguarded `z_b`
can drift toward a collapsed sink. In symmetric JEPA, the gradient
pulls both `z_a` and `z_b` toward each other — they meet at the
midpoint of their trajectories, NOT at a fixed collapsed sink. SIGReg
then ensures the meeting point is isotropic-Gaussian-shaped, not
constant. *Anima reduction.* `train_lejepa_s153.py` calls `f_θ` twice
in the same `torch.enable_grad()` scope and computes `(z_a − z_b)²`
without `.detach()` on either side. ∎

**B-S153-3 — NO-CE invariant (CLOSED, structural / source-grep
verifiable).** *Claim.* The §153 trainer source contains zero calls
to `F.cross_entropy`, `nn.CrossEntropyLoss`, `F.nll_loss`,
`F.binary_cross_entropy`, or `.log_softmax(...).gather(...)` — i.e.,
no logarithmic-likelihood objective. *Proof.* Direct source
inspection — the only loss-bearing identifiers in `train_lejepa_s153.py
::run` are `mse_pred`, `L_sigreg`, and `L_total`. *Anima reduction.*
This invariant is the §11-B test — §153 is non-CE by structural
property, not by claim. Verified via `grep -E
'F\.cross_entropy|CrossEntropyLoss|F\.nll_loss|binary_cross_entropy|
log_softmax.*gather' train_lejepa_s153.py == 0`. ∎

**B-S153-4 — Sphere-direction sampling is anima-deterministic (CLOSED,
structural).** *Claim.* The sketch directions `a_1..a_{|A|}` are
sampled via `torch.randn(|A|, d_emb, generator=g)` followed by
`F.normalize(·, dim=−1)` with `g = torch.Generator(device).
manual_seed(1337 + step)`, where step ∈ ℤ is the training step
index — i.e., the sampling is a *deterministic function of (seed,
step)*. *Proof.* PyTorch's `torch.randn` with an explicit
`Generator` is fully reproducible on the same device; `F.normalize`
is deterministic. *Anima reduction.* SIGReg's "external" piece (the
sphere directions) is anima-substrate-controlled: anima's own seed
1337 governs the directions step-by-step. No external entropy
source enters the learning signal. ∎ This is the structural property
that earns §7 ③ at the regularizer level.

**B-S153-5 — Epps-Pulley statistic non-negative (CLOSED).** *Claim.*
For any finite sample `{s_n} ⊂ ℝ` and any positive weight function
`w(t) > 0`, `EP({s_n}) ≥ 0`, with equality iff `φ̂_S = φ_𝒩` exactly
(measure zero in practice). *Proof.* `EP = N · ∫|·|² · w(t) · dt` is a
non-negative integrand integrated against a positive weight — the
integral is non-negative; zero only if the integrand is zero almost
everywhere. ∎ *Anima reduction.* `L_SIGReg ≥ 0` strictly, with `= 0`
the unattainable ideal. The trainer can use this as a sanity assert
(`assert (L_sigreg.item() >= 0)`).

**B-S153-6 — Single-encoder invariant (CLOSED, structural / model-
graph verifiable).** *Claim.* The §153 trainer constructs exactly
ONE instance of `ConsciousDecoderV2` and passes both views `ctx_a`
and `ctx_b` through it. *Proof.* Direct source inspection — the
trainer source contains exactly one `model = ConsciousDecoderV2(...)`
constructor call, no `model_teacher`/`model_student`/`ema_model`
identifiers, no `.copy_()`/`.deepcopy()` of `model`, and the two
view embeddings are computed by `f_emb(model, ctx_a)` and
`f_emb(model, ctx_b)` (same `model` reference). *Anima reduction.*
The teacher-student / EMA / momentum-encoder pattern that JEPA-V /
DINO use is structurally absent; LeJEPA's "no teacher" claim is
honored. ∎

**B-S153-7 — Verdict bucket is a closed predicate (CLOSED, byte-
equal to §125/§126/§139).** *Claim.* The function `verdict_bucket(
byte_acc, psi_responsive)` defined in `eval_lejepa_s153.py` is
byte-equal to the same function in `eval_eqprop_s139.py` (and
upstream in `eval_pcn_s126.py`, `eval_nonce_ff_s125.py`); identical
thresholds (`TAU_PSI_SPREAD=1e-4`, `RANDOM_BYTE_FLOOR=1/256`,
`DEGENERATE_CEILING=2/256`, `SUPPORT_FLOOR=0.05`); identical branch
order. *Proof.* Direct source verification via `diff` of the
`verdict_bucket` function bodies + constants. *Anima reduction.*
The §125+§126+§139+§153 joint reading is well-formed: each fire
produces a value from the SAME closed three-valued discrete output
space `{DEG, PART, SUPP}`, computed by the SAME predicate. ∎

**B-S153-8 — Corpus byte-identical connection-point (CLOSED, sha
verification).** *Claim.* The pod-side corpus used at training time
has sha256 `39d581da209615468c1c41e07aa8662ef1074bc5be49a666f8f8617
53dd5810e` — byte-identical to §107-RETRY / §125 / §126 / §139.
*Proof.* The dispatch script `dispatch_s153_runpod.sh` builds the
corpus pod-side via the same `build_corpus_s101.py --s1-n 777000
--seed 1337` invocation and verifies the sha BEFORE training begins;
sha mismatch ⇒ `FATAL refuse-to-train`. *Anima reduction.* All four
§96-Q2 fires (§125/§126/§139/§153) trained on byte-identical anima-
substrate corpus; the verdict difference reflects the *algorithm*
difference, not corpus variance. ∎

**B-S153-NOTE — Empirical carve-out.** The §153 verdict bucket
(`S11B_LIKE_DEGENERATE` / `PARTIAL_AMBIGUOUS` / `S96_Q2_SUPPORTED`) is
**SGD-outcome empirical**: B-S153-1..8 above prove the *mechanism*
is well-formed (anti-collapse closed-form, symmetric grad, NO-CE
structural, anima-deterministic, EP ≥ 0, single encoder, verdict
predicate closed, corpus byte-equal), but whether anima's d=768·12L
ConsciousDecoderV2 substrate actually learns a useful embedding
under L_LeJEPA at 3000 steps is an SGD/initialization outcome. This
NOTE family carries from B-D-NOTE / B-S125-NOTE / B-S126-NOTE /
B-S139-NOTE / B-EMERGE-7 / B-S99-NOTE / B-S111-NOTE — necessary-not-
sufficient at every layer. north-star + §15/§51/§72 milestones
UNCHANGED regardless of §153 verdict.

## §10 What §153 does / does not claim

- **Claims (post-fire, measured)**: one Boolean from
  `{DEG, PART, SUPP}`. Plus four scalars: `byte_acc`, `psi_dir_mean`,
  `psi_dir_std`, `psi_responsive`. Plus the §96-Q2 4-tuple joint
  reading update.
- **Does NOT claim**: GOAL emergence; §11-B refutation in general;
  data-regime threshold movement; substrate-rewrite (§95/§96 stay
  open); routing-collapse breakage (§151 / §16 stays open).

## §11 Cross-link

- §125 NONCE-FF (`state/nonce_ff_fire_s125_2026_05_20/`) —
  `S11B_LIKE_DEGENERATE`
- §126 PCN-C4 (`state/pcn_fire_s126_2026_05_20/`) —
  `PARTIAL_AMBIGUOUS`; AGENTS.tape `@D g1` carries the L145
  structured-argv discipline.
- §139 EqProp (`HEXAD/NEUROMORPHIC/state/eqprop_fire_s139_2026_05_20/`) —
  result.json byte_acc 0.1185 PARTIAL-class.
- §128 `SOFTWARE_BREAKTHROUGH_RESEARCH.md` §1 Cluster C, §2 ranked #5,
  §8 next-list P4 — §153 = the P4 fire.
- §151 `state/fep_attractor_complexity_routing_s151_2026_05_20/` —
  orthogonal frontier-2 (routing collapse) design; not addressed by §153.
- §107-RETRY (`state/dataregime_threshold_fire_s107_2026_05_19/`) —
  WALL-A (data-regime) THRESHOLD_CROSSED=False at 283M; unchanged by
  §153.
- arxiv 2511.08544 (LeJEPA, Balestriero + LeCun) — anchor paper.

**Wall**: ~$0.3–1 (single H100/A100 fire, sequential, mirror §125/§139
envelope). **GPU**: 1. **Orphan**: 0 (myself.pods verified empty post-
teardown). **Central blue_falsifier**: 0-line-diff sha
`c93e160a8a376a94` invariant. **docs/* 신규**: 0 (g_doc_consolidation —
saved under `HEXAD/NEUROMORPHIC/state/`).

---

*north-star + §15/§51/§72 milestones UNCHANGED — §153 = WALL-B-i fourth
data point, GOAL 미도달, B-EMERGE-7 necessary-not-sufficient.*
