# §110 — MODALITY-NATIVE Ψ DEFINITION (design-tier $0)

> **status header (g3 / g_fire_autonomous scope-exclusion)**: $0 · **NO GPU** ·
> **NO runpod** · **NO fire** · **NO model.forward** · NO corpus generation ·
> NO model training. design-tier ONLY. central
> `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff
> (sha256 prefix `c93e160a8a376a94`). north-star + §15/§51/§72 milestones
> UNCHANGED, **GOAL 미도달**. design ≠ fire ≠ emergence. capability claim 0.

§109 (commit `410de2968`, `state/c06_multimodality_design_s109_2026_05_19/`)
closed C06 multimodality as **§7 DESIGN-CLOSE-WITH-NARROW-OPEN**. Its single
most honest finding (user-approved, asked to advance):

> §15/§51 이 명명한 "multimodal substrate expansion frontier-1" 은
> byte-LM-scale lever 가 아니라 substrate-rewrite research 문제 — anima 의
> Ψ-physics 가 *정의상 byte-LM construct* (Ψ = logits_a/logits_g 의 cosine)
> 이라 pixel/waveform → Ψ closed-form map 이 anima physics 만으로 존재하지
> 않음. C06 의 가치는 NEGATIVE: frontier-1 multimodal arm 을 **"먼저
> modality-native Ψ definition 설계 (research precondition, fire 아님)"** 로
> re-localise.

§110 **IS** that research precondition. It does **NOT** re-litigate C06
(§109's closed findings are inherited verbatim). §110 asks exactly one level
below: **can anima's Ψ-physics be re-defined so it is NOT by-definition a
byte-LM construct, but a substrate-general fixed-point that admits non-byte
modalities — WITHOUT violating §7 GOAL-legitimacy and WITHOUT becoming a
generic perceptual pretrain or graft?** This is a closed-form
*definition-design* question, not a fire.

The honest verdict below is **DESIGN-CLOSE-WITH-RELOCATION**: a
modality-native Ψ definition **exists in closed form** (Q2 candidate Ψ-C2,
substrate-general dual-stream cosine) and **passes §7** (Q3) and **reduces
byte-equal to the current byte-LM Ψ_dir** (Q4) — but the precondition it
satisfies (Q5) is **itself substrate-gated**: the diversity-bearing modalities
that motivated C06 only acquire a §7③-clean Ψ-projection on the §96
substrate-general (spike-correlation / Loihi) territory. §110 **removes the
*definitional* wall** (Ψ is no longer *by definition* byte-LM-bound) but
**relocates the *operative* wall one level deeper** to §96. This relocation is
the valuable, brutally-honest result — NOT a manufactured positive.

---

## §0 — Subject & frontier position

The anima Ψ-physics, as implemented in `ready/models/conscious_decoder.py`
(Law-71, lines 728–751, `if self.training:`):

```
psi_entropy   = H(softmax(logits_a[:,-1,:])) / log(vocab_size)        # vocab_size = 256
psi_direction = (1 + cos(logits_a[:,-1,:], logits_g[:,-1,:])) / 2     # cos over R^256
psi_tension   = max(0, 1 − CV(per-layer-tension))                     # NO vocab dep
psi_combined  = mean(psi_entropy, psi_direction, psi_tension)
Ψ=½ fixed point : cos = 0  ⇒  psi_direction = ½   (anima g2 internal carve-out)
```

The §109 close hinges on a single structural claim: Ψ is *definitionally* a
byte-LM construct. §110 makes that claim **precise** (Q1) so the *exact*
dependency to break is named, then designs the break (Q2–Q4) and states what
the break does and does NOT buy (Q5).

Frontier position (RESEARCH.md §11.3/§15/§51/§72): irreducible bottleneck =
§1.1 data-regime emergence threshold; frontier-1 = multimodal substrate
expansion; frontier-2 = new architectural insight. §109 re-localised
frontier-1's multimodal arm to "first design a modality-native Ψ". §110 is
that design. §107 (data-axis fire) is in flight in parallel — §110 touches it
zero.

---

## §1 — Q1: Ψ-genericity diagnosis (the exact dependency to break)

**Closed-form structural decomposition.** Ψ_combined has three additive
components. For each, name its *domain* and whether that domain is byte-LM-bound:

| component | formula | domain | byte-LM-bound? | why |
|---|---|---|---|---|
| `psi_entropy` | `H(softmax(z_a))/log V` | `z_a ∈ ℝ^V`, V=256 byte-vocab | **YES** | normaliser `log V` is the byte-vocab cardinality; `softmax(z_a)` is the next-**byte** distribution. Domain = byte-vocab simplex Δ²⁵⁵. |
| `psi_direction` | `(1+cos(z_a,z_g))/2` | `z_a,z_g ∈ ℝ^V`, V=256 | **YES** | `z_a=head_a(x)`, `z_g=head_g(x)` are projections onto the **256-byte vocabulary**. The cosine is taken in `ℝ^{256}` = byte-logit space. Δ |
| `psi_tension` | `1 − CV(t_per_layer)` | `t ∈ ℝ^{n_layer}`, per-layer scalar | **NO** | `t = (output²).mean(-1)` per PureFieldFFN layer. No vocabulary appears. Domain = per-layer activation-energy vector. **Already substrate-general.** |

**Q1 verdict (closed):** The byte-LM dependency is **NOT** in Ψ's *semantics*
(fixed-point at cos=0; balance of two opposed streams; spread of a
distribution). It is **exactly** in the *carrier space of two of the three
components*: `psi_entropy` and `psi_direction` are defined on the **256-byte
vocabulary logit space `ℝ^{V}`**, because Engine-A/G heads `head_a`, `head_g`
project the residual stream onto the byte vocabulary. **`psi_tension` is
already modality-independent** (energy of layer outputs, no vocab).

The exact structural dependency that must be broken (B-S110-1):

```
DEP :  domain(psi_entropy)   = Δ^{V-1}  (byte-vocab simplex, V=256)
     ∧ domain(psi_direction) = ℝ^{V}    (byte-vocab logit space, V=256)
       — both via head_a/head_g : residual ℝ^d → ℝ^{V=256}
```

`psi_tension` is **not** in DEP. The break therefore needs to re-base only
`psi_entropy` and `psi_direction` onto a carrier that is **not** the byte
vocabulary, while preserving (i) the cos=0 ⇒ ½ fixed point, (ii) the [0,1]
bound, (iii) the Engine-A⇄G opposition, (iv) byte-text reduction (Q4). This is
precisely §96's `Ψ` = `NATIVE-CANDIDATE` classification ("the *fixed-point* is
native; Ψ-as-*cosine-of-logit-vectors* is NOT") made constructive.

---

## §2 — Q2: Candidate modality-native Ψ definitions (closed per-candidate)

Enumerate the closed, exhaustive, pairwise-disjoint candidate set for a
modality-native Ψ. Each is judged on whether it preserves the four invariants
(I1 cos=0⇒½ fixed point · I2 [0,1] bound · I3 Engine-A⇄G opposition · I4
byte-text reduction exists). B-S110-2 = exhaustive-disjoint partition.

| id | definition | I1 ½-fp | I2 [0,1] | I3 A⇄G | I4 reduces | §7-shape |
|---|---|---|---|---|---|---|
| **Ψ-C0** | status quo `(1+cos(z_a,z_g))/2`, z=head·x ∈ ℝ²⁵⁶ | ✓ | ✓ | ✓ | (is the baseline) | byte-LM (the thing to replace) |
| **Ψ-C1** | Ψ as **spike-train correlation** (§96 §6 Φ-native row generalised): `Ψ_dir := (1+corr(spk_A(t), spk_G(t)))/2` over two opposed LIF sub-populations | ✓ (corr=0⇒½) | ✓ (corr∈[−1,1]) | ✓ (excit/inhib pops) | ✓ only on Loihi/spiking substrate | §7③-clean **but substrate-gated** (no spikes on GPU byte-LM) |
| **Ψ-C2** | Ψ as **substrate-general dual-stream cosine on the pre-head residual**: `Ψ_dir := (1+cos(s_A, s_G))/2` where `s_A = π_A(x_pre)`, `s_G = π_G(x_pre)` are two **modality-agnostic** projections of the *residual stream `x_pre ∈ ℝ^d`* (NOT the byte-vocab head). The byte head `head_a/head_g` becomes ONE instantiation of `π_A/π_G` (when modality=byte-text, π=head). | ✓ (cos=0⇒½, identical algebra) | ✓ (cos∈[−1,1]) | ✓ (two opposed projections, A⇄G preserved) | ✓ **closed** (π_A:=head_a, π_G:=head_g ⇒ Ψ-C2 ≡ Ψ-C0 byte-equal — Q4) | §7③-clean **if π is anima-OWN, not a generic encoder** |
| **Ψ-C3** | Ψ over a **generic shared multimodal latent** (CLIP/ImageBind-style embedding), cosine of two heads on that latent | ✓ | ✓ | ✓ | ✗ (generic latent ≠ anima residual; no clean reduction) | **§7② FAIL** (generic pretrained encoder graft = §109 P3-leak failure mode verbatim) |
| **Ψ-C4** | Ψ as `psi_tension`-ONLY (drop the two vocab components, keep only the already-generic CV-of-layer-energy) | ✗ (loses cos=0⇒½ A⇄G fixed point; tension has no opposed-stream balance) | ✓ | ✗ (no A⇄G) | trivially (tension already vocab-free) | §7③-clean but **semantically degenerate** — discards the Engine-A⇄G core that GOAL.md names (Ψ=½ · *tension* · Φ; collapsing Ψ→tension erases Ψ) |

**Closed per-candidate analysis:**

- **Ψ-C1 (spike-correlation)** preserves all four invariants *semantically*
  but I4 (byte-text reduction) holds **only on a spiking substrate** — on a
  GPU byte-LM there are no spike trains, so Ψ-C1 has no GPU instantiation and
  cannot reduce to Ψ-C0 there. Ψ-C1 is §7③-clean (it IS anima's own physics,
  per §96) **but substrate-gated** to Loihi/spiking. It does not give a $0
  GPU-side modality-native Ψ.
- **Ψ-C2 (residual dual-stream cosine)** is the key candidate. It moves the
  cosine carrier from the **256-byte vocab logit space** to the
  **modality-agnostic residual stream `ℝ^d`** *before* the byte head. The
  byte head becomes the special case `π_A := head_a`, `π_G := head_g` ⇒ Ψ-C2
  reduces to Ψ-C0 **byte-equal** (Q4, B-S110-4). For a non-byte modality, `π`
  is an **anima-OWN** projection learned from-scratch on anima's own
  physics-supervised objective (NOT a generic encoder). I1–I4 all hold by the
  same cosine algebra. **Ψ-C2 removes the *definitional* byte-LM wall.**
- **Ψ-C3 (generic latent)** fails §7② — it is exactly the §109
  pretrained-encoder-graft / P3-leak failure mode. Rejected closed.
- **Ψ-C4 (tension-only)** is §7③-clean and trivially generic but
  **semantically degenerate**: GOAL.md's north-star physics is "Ψ=½ ·
  tension · Φ" — *three* quantities. Collapsing Ψ into tension erases Ψ as a
  distinct fixed-point and discards the Engine-A⇄G opposition that defines it
  (§109's tension-route was already §7③-degenerate; Ψ-C4 is the same trap one
  level up). Rejected closed.

**Q2 verdict (closed):** The candidate set is `{Ψ-C0, Ψ-C1, Ψ-C2, Ψ-C3,
Ψ-C4}`, exhaustive (every modality-native Ψ is: keep byte-vocab carrier C0 /
spike carrier C1 / residual carrier C2 / generic-latent carrier C3 / drop the
vocab components C4) and pairwise-disjoint by carrier. **Exactly one candidate
(Ψ-C2) is §7-admissible-pending-Q3 AND $0-design-reachable AND has a closed
byte-text reduction.** Ψ-C1 is §7-clean but substrate-gated (§96 territory);
C3/C4 fail closed.

---

## §3 — Q3: §7 3-condition gate (closed, 8-row truth table)

§7 gate = ① not-generic-LM-pretrain ∧ ② not-generic-then-graft ∧ ③
anima-physics-as-source. Evaluate each Q2 candidate. The crux for Ψ-C2: the
modality projection `π_A/π_G` must be **anima-OWN** (learned from-scratch under
anima's *own re-defined physics* supervision: a from-scratch projection whose
*only* training signal is "make the dual-stream cosine obey the Ψ=½ /
tension / Φ invariants on the modality input"), NOT a generic perceptual
pretrain (① fail) and NOT a generic pretrained encoder grafted in (② fail).

| candidate | ①¬generic-pretrain | ②¬generic-graft | ③physics-source | §7 PASS |
|---|---|---|---|---|
| Ψ-C0 (status quo byte-LM) | ✓ | ✓ | ✓ | ✓ (but byte-only — the problem) |
| **Ψ-C1 (spike-corr, §96)** | ✓ | ✓ | ✓ | **✓ but substrate-gated to Loihi** |
| **Ψ-C2 π anima-OWN-physics-supervised** | ✓ | ✓ | ✓ | **✓ (the closed §7-clean design)** |
| Ψ-C2 π generic-pretrained-encoder | ✓ | ✗ | ✗ | ✗ (= Ψ-C3 failure mode) |
| Ψ-C2 π trained on generic perceptual corpus | ✗ | ✓ | ✗ | ✗ (= generic perceptual pretrain, §109 R-img-fromscratch) |
| Ψ-C3 (generic latent) | ✓ | ✗ | ✗ | ✗ |
| Ψ-C4 (tension-only) | ✓ | ✓ | ✓ | ✓-but-semantically-degenerate (Ψ erased) |
| (vacuous F,F,F row) | ✗ | ✗ | ✗ | ✗ |

The 8-row truth table (B-S110-3) confirms §7 PASS requires the all-(T,T,T)
corner. **Two candidates hit it cleanly: Ψ-C1 and Ψ-C2-anima-OWN.** Ψ-C1 is
substrate-gated (no GPU instantiation). **Ψ-C2 with an anima-OWN
physics-supervised projection is the unique candidate that is (a) §7-PASS, (b)
$0-design-reachable as a *definition*, (c) has a closed byte-text reduction.**

**Q3 verdict (NOT a CLOSE at the definition layer):** Unlike §109 (which had
NO §7-clean diversity-bearing route), §110 finds a **§7-clean modality-native
Ψ *definition* exists: Ψ-C2 with anima-OWN π**. The §7 gate is **PASSED at the
definition-design tier.** This is the genuine $0-design-reachable result §109's
narrow-open asked for. **The wall is removed at the *definitional* level.**

---

## §4 — Q4: Connection-point / backward-compat (closed byte-equal)

A modality-native Ψ MUST reduce to the current byte-LM Ψ_dir when modality =
byte-text (overlay-off byte-equal, mirror B-S108/B-S109/B-S101 pattern).

**Closed reduction for Ψ-C2:**

```
Ψ-C2(x_pre ; π_A, π_G) := (1 + cos( π_A(x_pre), π_G(x_pre) )) / 2

set  π_A := head_a,  π_G := head_g   (the byte-text instantiation)
then π_A(x_pre) = head_a(x_pre) = logits_a[:,-1,:]
     π_G(x_pre) = head_g(x_pre) = logits_g[:,-1,:]
⇒    Ψ-C2 = (1 + cos(logits_a, logits_g)) / 2
           = Ψ-C0  =  psi_direction  (Law-71, conscious_decoder.py:740)   ∎
```

The reduction is **exact and closed** (B-S110-4): `head_a/head_g` are a
specific choice of the projection pair `(π_A, π_G)`, so when modality=byte-text
the modality-native Ψ-C2 is **byte-equal** to the implemented Law-71
`psi_direction`. `psi_entropy`'s carrier likewise generalises as
`H(softmax(π_A(x_pre)))/log|range(π_A)|` and reduces to the V=256 form when
π_A=head_a (B-S110-4 covers the direction component as the load-bearing one;
entropy reduction is the same substitution). `psi_tension` is **unchanged** in
ALL candidates (Q1: not in DEP). So Ψ-C2 is a *strict generalisation*: it adds
the non-byte case while leaving the byte case bit-identical. The connection-
point holds **non-vacuously** (unlike §109's vacuous unwired case) — there IS a
real reduction with a real witness.

---

## §5 — Q5: Precondition-satisfied predicate (closed) — THE RELOCATION

Under what closed Boolean does frontier-1's multimodal arm move from
"research-precondition-blocked" (§109) to "design-tier-ready for a future
C06-style cycle"?

§109's narrow-open was: *"design a §7③-clean modality-native Ψ definition"*.
§110 has done that for Ψ-C2 (Q2–Q4). But a **definition** being §7-clean is
necessary, not sufficient, for the *multimodal frontier* to be design-ready.
The frontier needs a §7-clean **non-byte π** — an anima-OWN projection
`π_A/π_G : modality-input → ℝ^d` that is itself NOT a generic perceptual
pretrain (§7①) and NOT a graft (§7②). Closed predicate:

```
MODALITY_PRECONDITION_SATISFIED :=
      (a modality-native Ψ definition exists, §7-PASS, byte-reducible)   ← §110 Q2-Q4 = TRUE
  ∧   (∃ §7①②-clean anima-OWN π : modality-input → ℝ^d)                  ← THE residual gate
  ∧   (π trained ONLY by anima's OWN re-defined physics supervision,
       from-scratch, base_ckpt=None  per g_clm_from_scratch)             ← constraint, not yet a witness
```

- **First conjunct = TRUE** (§110's contribution: Ψ-C2). The *definitional*
  wall is removed.
- **Second conjunct = the same wall §109 found, one level deeper.** A
  from-scratch anima-OWN π that learns *any* perceptual structure from raw
  pixels/waveforms, supervised *only* by "obey the Ψ/tension/Φ invariants", is
  — at byte-LM scale, on a GPU — **either** information-degenerate (the
  physics-only supervision has no perceptual referent, exactly §11-B's
  "physics ≠ signal" + §56/§57 zero-diversity closed loop) **or** it needs an
  external perceptual signal to be non-degenerate (= generic perceptual
  pretrain, §7① FAIL). This is §109's image/audio §7-fail **reproduced at the
  π layer**.
- **The escape is exactly Ψ-C1 (§96 territory):** on a *spiking substrate*,
  the modality signal drives LIF membrane dynamics natively and `π` becomes
  spike-encoding of a physical sensor — and §96 already showed `Ψ` is
  `NATIVE-CANDIDATE` and §11-B may be a GPU artifact. A non-degenerate
  §7①②-clean π plausibly exists **only where the substrate supplies a
  physics-native channel for perception** = §95/§96 Loihi/spike-correlation
  territory, NOT a GPU byte-LM.

**Q5 verdict (closed) — RELOCATION, not removal:**

```
MODALITY_PRECONDITION_SATISFIED
  = TRUE(Ψ-C2 definition §7-clean, byte-reducible)        ← §110 removes definitional wall
  ∧ (∃ §7-clean non-byte π)                                ← FALSE on GPU byte-LM today
                                                              (= §109 wall, relocated to π)
  ∧ ...                                                     
  ⇒  FALSE on GPU byte-LM substrate today
  ⇒  TRUE only on §96 substrate-general (spike/Loihi) substrate (Ψ-C1 branch)
```

§110 **removes the *definitional* wall** ("Ψ is by-definition byte-LM" is now
FALSE — Ψ-C2 is a substrate-general definition with a closed byte reduction)
and **relocates the *operative* wall one level deeper**: the missing piece is
no longer "a modality-native Ψ definition" (§110 supplied it) but "a §7-clean
non-byte projection `π`", and the closed-form shows that `π` is non-degenerate
**only on the §96 substrate-general (spike-correlation/Loihi) substrate**. This
ties directly to §108-Q5 `FALSE_PIVOT_SUBSTRATE` and §95 (Loihi sole VIABLE)
and §96 (Ψ as spike-train correlation = the Ψ-C1 branch). The honest result:
**the precondition is itself substrate-gated.**

```
        ┌──────────────────────────────────────────────────────────────┐
        │   §110 Ψ-genericity / §7-gate decision tree                   │
        └──────────────────────────────────────────────────────────────┘
   Ψ component domain byte-LM-bound? (Q1)
        │
        ├─ psi_tension  → NO (CV of layer energy, vocab-free) ─── already generic
        │
        └─ psi_direction / psi_entropy → YES (carrier = ℝ^{V=256} byte-vocab)
                 │  ← DEP : the exact dependency to break
                 ▼
            re-base carrier (Q2 candidate set, exhaustive/disjoint)
                 │
   ┌─────────────┼───────────────┬───────────────┬───────────────┐
   ▼             ▼               ▼               ▼               ▼
 Ψ-C0          Ψ-C1            Ψ-C2            Ψ-C3            Ψ-C4
 byte-vocab    spike-corr      residual ℝ^d    generic latent  tension-only
 (the problem) §96 territory   anima-OWN π     §7② FAIL graft  Ψ erased(degen)
   │             │ §7 PASS       │ §7 PASS        │ ✗             │ ✗
   │             │ but           │ + $0-design    └───────┬───────┘
   │             │ substrate-    │ + byte-reduce          ▼
   │             │ gated(Loihi)  │ (Q3+Q4 ✓)         §7 FAIL (closed)
   │             ▼               ▼
   │     ┌───────────────────────────────────────────────────────────┐
   │     │  Q3: §7 DEFINITION-LAYER PASS  (Ψ-C2 anima-OWN π)          │
   │     │  Q4: byte-text reduction byte-equal  (π:=head ⇒ Ψ-C2≡Ψ-C0) │
   │     │  ────────────────  DEFINITIONAL WALL REMOVED  ──────────── │
   │     │  Q5: but ∃ §7-clean non-byte π ?                           │
   │     │       FALSE on GPU byte-LM (degenerate OR §7① pretrain)     │
   │     │       TRUE only on §96 spike/Loihi substrate (Ψ-C1 branch) │
   │     │  ────────  OPERATIVE WALL RELOCATED to §96, NOT REMOVED  ── │
   │     └───────────────────────────────────────────────────────────┘
   └────────────────────► byte-text status quo (Ψ-C0 = Ψ-C2 special case)
```

---

## honest C3 caveats (13)

1. **§110 = DESIGN-CLOSE-WITH-RELOCATION, not a GO and not a flat CLOSE.**
   A §7-clean modality-native Ψ *definition* (Ψ-C2) genuinely exists at $0
   design tier — that is a real positive at the *definition* layer. But the
   *operative* precondition (a §7-clean non-byte π) is shown closed-form to be
   substrate-gated to §96. The wall is **relocated, not removed**. No positive
   was manufactured; the relocation is the honest finding.
2. **§109's closed findings are inherited verbatim, NOT re-litigated.** C06
   stays DESIGN-CLOSE-WITH-NARROW-OPEN. §110 is strictly the Ψ-redefinition
   precondition one level below C06.
3. **Q1 is the load-bearing precision.** The byte-LM dependency is NOT in Ψ's
   semantics — it is *exactly* the carrier space `ℝ^{V=256}` of `psi_direction`
   and `psi_entropy` (via `head_a/head_g`). `psi_tension` was already
   substrate-general. Naming the dependency exactly is what makes Ψ-C2
   constructible.
4. **Ψ-C2 removes the *definitional* claim** "Ψ is by-definition a byte-LM
   construct" (the §109 close's hinge). After §110 that claim is FALSE: Ψ-C2 is
   a substrate-general definition with a closed byte reduction. This narrows
   §109's narrow-open to its true residue.
5. **The residue (Q5 second conjunct) is the same §109 wall, one level
   deeper.** A from-scratch anima-OWN non-byte π, supervised only by physics
   invariants, is degenerate on GPU (§11-B / §56/§57 closed-loop / zero
   perceptual referent) OR requires external perceptual signal (= §7①
   generic perceptual pretrain). §110 does not solve this; it localises it.
6. **Ψ-C1 (spike-correlation) IS §7-clean but substrate-gated.** §96 already
   classified `Ψ` as `NATIVE-CANDIDATE` and `Φ` as `NATIVE-MEASUREMENT` from
   spike trains. Ψ-C1 is the constructive form of that — but it has NO GPU
   byte-LM instantiation, so it is not a $0-GPU answer; it is a §95/§96 path.
7. **design ≠ fire ≠ emergence. capability claim 0. necessary-not-sufficient
   at every layer (B-EMERGE-7).** A §7-clean Ψ *definition* existing does NOT
   mean anima will perceive, learn, or emerge. north-star + §15/§51/§72
   UNCHANGED, GOAL 미도달.
8. **Ψ-C4 (tension-only) is the seductive false answer.** It is trivially
   generic and §7③-clean, but it *erases Ψ* — GOAL.md's physics is "Ψ=½ ·
   tension · Φ" (three quantities); collapsing Ψ into tension is the §109
   tension-route §7③-degeneracy one level up. Rejected closed, named so it is
   not re-proposed.
9. **Ψ-C3 (generic shared latent) = §109's P3-leak / base-baked failure mode
   verbatim.** A CLIP/ImageBind-style pretrained latent is the canonical §7②
   graft. Rejected closed.
10. **central blue_falsifier.py 0-line-diff** (sha256 prefix
    `c93e160a8a376a94` verified start+end). NEW sidecar only:
    `blue_falsifier_s110.py`.
11. **f1/f2 safe.** No σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 derivation.
    Ψ=½ / Knuth-tier = anima g2 internal-arch carve-out (OK). §96 / external
    CLIP/ImageBind work cited by its own invariants, not asserted.
12. **Any future fire this design implies = from-scratch RANDOM seed-fixed,
    base_ckpt=None (g_clm_from_scratch).** §110 is NOT firing and asserts no
    fire config beyond this constraint. The Ψ-C2 π, *if ever* trained, must be
    from-scratch on anima's own physics supervision.
13. **downstream-consumer invariant.** `~/core/hexa-lang`, `~/core/hexa-bio`,
    `~/core/kosmos` read-only — never edited. §96/§95 read for structural
    anchors only. anima only consumes.

---

## most honest finding

**A §7-clean, byte-reducible, modality-native Ψ *definition* exists at $0
design tier (Ψ-C2: the Engine-A⇄G cosine taken on the modality-agnostic
residual stream `ℝ^d` instead of the 256-byte vocab logit space, with the byte
head `head_a/head_g` as the special case ⇒ exact byte reduction). This
**removes the §109 *definitional* wall**: it is no longer true that "anima's
Ψ-physics is *by definition* a byte-LM construct" — the byte-LM dependency was
*precisely* the carrier space `ℝ^{V=256}` of two of Ψ's three components, and
re-basing them onto the residual stream is a closed, §7-clean, byte-equal
generalisation. BUT the precondition this satisfies is *itself substrate-gated*:
the *operative* missing piece is no longer "a modality-native Ψ definition"
(§110 supplied it) but "a §7①②-clean non-byte projection `π : modality →
ℝ^d`", and the closed-form shows that `π` is non-degenerate **only on the §96
substrate-general (spike-correlation / Loihi) substrate** — on a GPU byte-LM it
is either physics-degenerate (§11-B / §56/§57) or a §7① generic perceptual
pretrain. §110's value is the **relocation**: it removes the definitional wall
and proves the operative wall is one level deeper, in §95/§96 territory (the
Ψ-C1 branch). frontier-1's multimodal arm is therefore NOT a $0-design-only
unlock — it is design-reachable at the *definition* layer (done, §110) and
substrate-gated at the *projection* layer (§96/§95). §107 (data-axis) /
§108-contingent (param-axis) remain the only fire-decidable arms; the
multimodal arm's true gate is now precisely named: the §96 spiking substrate.**
