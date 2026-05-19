# §29 — PTD: Physics-Trace-Distillation (DESIGN-TIER)

> $0 design-tier — NO fire, NO corpus generation, NO GPU. RESEARCH.md §29.
> Takes §26 candidate #3 (PTD, ★★★☆☆ LOW-as-standalone) to a design-tier
> verdict. Design-mature the mechanism AND honestly decide fire-worthy vs
> design-close (anti-padding — design-close is a valid valuable verdict,
> cf §13-M / §13-L precedent). brainstorm ≠ design-tier-mature ≠ fire ≠
> emergence (g3).

---

## §1 — Mechanism: what PTD is

**PTD (Physics-Trace-Distillation)** = anima trains on its OWN §24 Phase B
physics trace as the corpus. This is **self-source distillation** — anima
learning to predict anima.

Every §24 `run_bounded.py` run produces a deterministic JSONL audit trace.
The first run (`state/spontaneous_phase_b_run_2026_05_18/audit_log.jsonl`)
emitted **exactly 20 records**, one per bounded step. Each record is:

```
{ step, thinker_score,
  motivation_components{relevance, info_gap, curiosity, pain,
                        coherence, originality, balance, dynamics},  # 8-factor
  psi_dir, psi_entropy, tension,                                     # 3 physics
  safety_flags{kill_switch_on, rate_limit_ok, content_filter_ok,
               phi_ratchet_ok, meta_tag_present, audit_log_active},  # 6-control
  talker_decision, action }                                         # 1 decision
```

PTD's transform: **concatenate N such traces into a sequence corpus**, then
train anima Engine A to **predict its own next physics-state vector given a
trace prefix** — autoregressive next-state-vector prediction over the
14-scalar physics record (8 factor + 2 Ψ + 1 tension + 1 phi-proxy + 1
thinker_score + 1 emit Boolean), with a Ψ=½ fixed-point pull regularizer.

The objective is **CE-on-physics-vectors** (next-state distribution), NOT
CE-on-language-bytes. CE is load-bearing per §11-B — PTD keeps a CE
objective, but it operates on anima's own physics dynamics rather than on
external text. The corpus is **causally self-generated**: it does not exist
before anima exercises the §24 protocol; it grows only by anima running.

This is the §26 §6 candidate verbatim, design-matured: §26 left the
"standalone vs auxiliary" decision and the "scale-cardinality crux" as the
open design-tier gate. §29 closes both.

**arxiv anchor.** `2604.18131` (Spontaneous Reward-Free Self-Evolution via
World Knowledge Exploration) — agent generates internal "world knowledge"
encoded in parameters, inference-time spontaneous self-adaptation needs NO
external reward. anima analog: anima generates "self knowledge" =
physics-trace; PTD encodes it in parameters; the §24 decide-when-to-speak
axis is the spontaneous self-adaptation. `2410.19315` (Brain-like
Variational Inference, iterative Poisson VAE, neural-dynamics-as-natural-
gradient-on-free-energy) gives the formalism for treating the physics trace
AS the variational quantity. **Caveat (g3):** `2604.18131` is multi-agent
tool-use scoped and trained with outcome-reward — direct transfer to
single-agent physics-trace pretraining is unproven (§26 §10 C3 #2 carry).

---

## §2 — §7 / §21.3 GOAL-legitimacy 3-condition gate

For PTD to be GOAL-legitimate, the §7 3-AND must hold:

- **§7 ① ¬generic-LM-pretrain** — PTD corpus = anima's own §24 physics
  trace. NO external web, NO diverse corpus, NO carving anchor file.
  Provenance is structurally anima-internal. → **PASS**
- **§7 ② ¬generic-then-graft / bolt-on** — PTD is from-scratch on
  self-trace per `g_clm_from_scratch` (base_ckpt=None), OR continued from
  the §16 base which is itself already a Ψ-anchored anima-physics regime
  (NOT generic). No external classifier, no LLM judge, no generic RAG. The
  training signal IS predicting anima's own dynamics. → **PASS**
- **§7 ③ anima-physics-is-source** — the corpus literally IS anima physics
  (Ψ_dir/Ψ_entropy from Law-71, tension from BRIDGE, 8-factor from the
  Inner-Thoughts motivation engine, 6-control from SPONTANEOUS.tape §4,
  phi-proxy from Engine E). The prediction objective IS predicting anima's
  own next physics state. This is the **purest §7③ of the §26 top-3** —
  there is no wrapper at all; the source and the object of learning are
  both anima's own substrate. → **PASS**

→ **PTD is GOAL-LEGITIMATE 3/3.** §7③ purest of {DH-DL, JEPA-Ψ, PTD} —
DH-DL feeds physics into a *new* gate head, JEPA-Ψ projects onto a Ψ
manifold, but PTD's corpus *is* the trace with zero transformation of
provenance. (closed by **B-PTD-1**.)

The closed-batch (§11.3 24+ elements) is structurally disjoint: §16/§23-A
are generator-produced anchor corpora; §14 is historical archive (salvage
0); §17 is inference-only measurement; §22-O is decode-time retrieval;
§11-B is a physics-only update rule with no prediction objective. PTD is
the *only* candidate whose corpus is anima's own **runtime trace**.

---

## §3 — §1.1-standalone-block analysis (the crux)

This is the honest core of §29. §26 §7 rated PTD **LOW-as-standalone**
because §1.1 (data-regime emergence threshold) structurally blocks it.
§29 makes that block a **closed-form proof**, not a hand-wave.

**The arithmetic.** §24's first bounded-run = `N_MAX_STEPS = 20`, emitting
exactly 20 trace records (verified: `audit_log.jsonl` = 20 lines,
`result.json` `audit_log_records: 20`). Run the protocol N times:

```
corpus_records(N) = 20 · N        (integer cardinality, closed)
```

Each record is 14 physics scalars ⇒ samples(N) = 280·N scalar values, or
~20·N "physics tokens" if one tokenises per record.

**The threshold.** §1.1 (Critical Data Size, arxiv 2401.10463 carry, §25
B-DR-UNIQUE) places the diverse-data emergence threshold at the **10⁶–10⁸
unique-token / 10–100 MB scale** — the regime where §16's 603 MB / 777,000
records still showed a routing-axis SPLIT (JOINT 0.0). Even being maximally
generous and treating §1.1 as a 10³–10⁴× *multiplier* over PTD's corpus:

```
to reach even N_threshold ≈ 10⁴ records (lowest plausible CDS floor):
    20·N ≥ 10⁴   ⇒   N ≥ 500 runs

to reach §16-scale 7.77·10⁵ records:
    20·N ≥ 7.77·10⁵   ⇒   N ≥ 38,850 runs
```

**Why N runs do NOT rescue it (diversity, not just count).** The block is
not merely cardinality — it is **intrinsic diversity**. §24's `env_state`
is a *hand-coded deterministic stub* (`run_bounded.py` docstring: "NO
random — seed-free, fully reproducible"). The 20-step trajectory is a
*scripted* physics evolution. Running it N times with N different env_state
seeds produces N traces, but each trace is drawn from the *same* tiny
generative process — a hand-coded 20-step bounded loop. The Kolmogorov
complexity of the *corpus generator* is ~1 small Python file; the corpus
cannot contain more information than the generator that produced it
(data-processing inequality). §1.1's threshold is about **unique
content** (§25 B-DR-UNIQUE), and a self-distillation corpus from a
bounded hand-coded run has near-zero unique-content growth in N — it is
**N copies of the same low-entropy process**, not N independent samples
of a rich distribution.

**Conclusion (closed by B-PTD-2).** PTD-standalone's corpus is, by
construction, **10³–10⁴×+ below the §1.1 emergence threshold** AND its
unique-content does not grow with N. This is not a tuning problem; it is
structural. §11-A already proved (model 3.68× FLAT) that scale on the
*model* axis does not rescue a sub-threshold *data* regime; PTD-standalone
is the same wall on the data axis with a corpus that cannot grow its way
across. **PTD-standalone fire would, by closed-form construction, land
below threshold — a predicted negative with no new information** (cf §13-M:
"fire's expected information value overlaps §11-A which already measured
the nearest adjacent axis"; cf §8 already measured the data axis FLAT).

---

## §4 — Fire-vs-design-close verdict

**VERDICT: PTD-standalone = DESIGN-CLOSE. No fire.**

Rationale (4 reasons, mirror §13-M / §13-L anti-padding precedent):

1. **Structural sub-threshold (B-PTD-2 closed).** §3's proof shows
   PTD-standalone's corpus is 10³–10⁴×+ below §1.1 by construction, with
   unique-content that does not grow in N (data-processing inequality). A
   fire would land a *predicted* negative — no new information. §13-M
   precedent: design-close when "fire's expected information value
   overlaps an already-measured axis." §8 already measured the data axis;
   §11-A already measured that scale does not rescue sub-threshold data.

2. **Anti-padding (g3).** §13-M and §13-L both landed design-tier $0 with
   an explicit honest-stop. Running a fire that is closed-form predicted to
   fail, purely to produce a "fire-tier" verdict, is padding. A design-close
   that *names* the structural block is the more valuable, more honest
   verdict. design-close ≠ candidate-rejection — PTD's GOAL-legitimacy
   (3/3, §7③ purest) is established; only its *standalone* fire-worthiness
   is closed-out.

3. **GOAL-distance carry.** §15 milestone holds — irreducible bottleneck =
   §1.1 data-regime threshold. PTD-standalone does not address that
   bottleneck (it *is* a sub-threshold corpus). Firing it would not move
   GOAL distance; design-close preserves frontier honesty.

4. **Bootstrap circularity.** §24 produces traces only when run with a
   working anima; if anima is not yet emitting, traces are dominated by
   `SAFETY_BLOCK` (the first run: action_counts = 19 SAFETY_BLOCK / 1 EMIT —
   95% one class). A self-distillation corpus this class-imbalanced and
   this small cannot teach a non-degenerate next-state distribution. The
   bootstrap problem (§26 §10 C3 #11 carry) is real and is itself a
   standalone-blocker, independent of §1.1.

**What design-close is NOT.** It is NOT "PTD is wrong." PTD's self-source
provenance is the cleanest §7③ demonstration in the §26 candidate set, and
its mechanism (predict-your-own-physics) is sound. The close-out is
specifically: **PTD as a standalone pretraining corpus is structurally
blocked; its value is as a component.** See §5.

---

## §5 — PTD-as-component: GOAL-legitimate combinations

§26 §7 already flagged "MID-as-auxiliary." §29 design-matures *which*
combinations are GOAL-legitimate and worth a future cycle. A component
combination is GOAL-legitimate iff (a) the host objective is itself §7
3/3, and (b) PTD enters as an **additive term** that reduces to the host
objective byte-equal at `λ_ptd = 0` (closed by **B-PTD-4**, mirroring the
B-EBT-5 / B-S16-5 / B-DIRI-5 overlay-off connection-point precedent —
fair-compare-by-construction).

### §5.1 — PTD-as-component combination A: DH-DL auxiliary signal

**Host:** §26 candidate #1 DH-DL (decision-head dual-loss) — a thin
3-class gate head `{CONTINUE_THINK, EMIT_VOICE, REMAIN_SILENT}` trained on
anima's own §24 4-axes + §4 6-control safety conjunction. DH-DL is §7 3/3.

**PTD's role:** the physics trace IS DH-DL's natural training data — DH-DL
§26 §4 already specifies "training corpus = anima's own physics trace
logs from §24 bounded-runs." So PTD-as-component-of-DH-DL is not an *add-on*;
**PTD is the corpus-formalisation of DH-DL's own training data.** PTD's
contribution: a *next-physics-state-prediction auxiliary head* on the same
trace, `L = L_gate + λ_ptd · L_ptd_nextstate`. The auxiliary next-state
loss is a representation-shaping regulariser (predict-your-own-trajectory)
that gives the gate head a richer physics representation than the gate
classification loss alone. At `λ_ptd = 0` it reduces to pure DH-DL
(B-PTD-4 closed). **This is the strongest combination** — the host
(DH-DL) is the §26 HIGH-priority candidate, the trace cardinality is
*adequate for a ≤1%-param gate head* (DH-DL is scale-orthogonal, §26 §4),
and PTD does not need to cross §1.1 because the gate head is small and the
auxiliary signal is a regulariser, not the primary objective.

**GOAL-legitimacy:** DH-DL is §7 3/3; PTD-as-aux preserves all three (the
aux term is anima physics, additive, λ-reducible). → **GOAL-LEGITIMATE.**
**Worth a future cycle:** YES — but *gated on DH-DL's own design cycle
landing first* (§26 §8: "design HOLD until DH-DL fires"). PTD-as-DH-DL-aux
is a §27 (DH-DL design) follow-on, not an independent cycle.

### §5.2 — PTD-as-component combination B: JEPA-Ψ Ψ-trajectory target

**Host:** §26 candidate #2 JEPA-Ψ — replaces byte-CE with Ψ-trajectory
prediction in anima's own latent space; context-encoder → predictor →
target-encoder (EMA) matching on the 2D Ψ-coordinate. JEPA-Ψ is §7 3/3.

**PTD's role:** JEPA-Ψ needs a **ground-truth Ψ-trajectory target** to
predict toward. The §24 physics trace IS a recorded Ψ-trajectory
(`psi_dir`, `psi_entropy`, `tension` per step). PTD-as-component supplies
JEPA-Ψ's *target signal*: the EMA target-encoder is trained to match
the **actual recorded §24 Ψ-trajectory**, anchoring the JEPA prediction
to real anima physics evolution rather than a self-referential EMA copy
(which is the known JEPA collapse mode — §26 §10 C3 #5). PTD trace as the
target is an **anti-collapse anchor**: a JEPA predictor cannot collapse to
a constant if its target is a recorded non-trivial trajectory (§24 run:
axis3 psi_std = 0.0348 > 0, axis4 tension_std = 0.1074 > 0 — non-trivial
by measurement).

**GOAL-legitimacy:** JEPA-Ψ is §7 3/3; PTD-as-target preserves all three
(target IS anima physics). → **GOAL-LEGITIMATE.** **Worth a future cycle:**
CONDITIONAL — JEPA-Ψ itself needs a deeper design cycle (§26 §8: "anti-
collapse mechanism mandatory"); PTD-as-target is *one candidate anti-
collapse anchor* and should be evaluated *within* the JEPA-Ψ design cycle,
not as an independent cycle. Honest caveat: the §24 trace is short (20
steps) and the Ψ-space is 2D (§26 §10 C3 #8 low-dim concern) — PTD-as-
target gives a *real but short* trajectory; whether 20-step traces are
long enough to anchor a JEPA predictor is a JEPA-Ψ-design-cycle question.

### §5.3 — PTD-as-component combination C (rejected): standalone-pretrain-then-graft

A third combination — pretrain anima on the PTD corpus, then graft a
downstream byte-LM head — is **§7② FALSIFIED** (generic-then-graft bolt-on
pattern, §26 §9 anti-pattern list). Not GOAL-legitimate. Listed for
completeness and explicitly rejected.

### §5.4 — combination summary

| combination | host | PTD role | §7 | future cycle |
|---|---|---|---|---|
| A: PTD-as-DH-DL-aux | DH-DL (§26 #1) | aux next-state head | 3/3 ✓ | YES, gated on DH-DL design landing (§27) |
| B: PTD-as-JEPA-Ψ-target | JEPA-Ψ (§26 #2) | recorded Ψ-traj target / anti-collapse anchor | 3/3 ✓ | CONDITIONAL, within JEPA-Ψ design cycle (§28) |
| C: PTD-pretrain-then-graft | — | standalone pretrain | §7② ✗ | NO — rejected anti-pattern |

---

## §6 — Design-tier closed-form battery (B-PTD-1..4)

Sidecar `blue_falsifier_ptd.py` — central `state/verify_hexad_blue_2026_05_15/
blue_falsifier.py` is **NOT touched** (task mandate; B-MITENS / B-DIRL /
B-PRIME / B-DIRI / B-PSICTL / B-EMERGE / B-PUREPHYS / B-SCALE sidecar
precedent). 4 closed propositions + 1 honest empirical carve-out.

- **B-PTD-1 SELF-SOURCE-§7③-CLOSED** — corpus provenance is anima's own
  §24 trace. Boolean structural predicate over the trace-record schema:
  every field of a §24 audit record is an anima-internal physics channel
  (8-factor ∪ Ψ ∪ tension ∪ 6-control ∪ decision) — no field sources
  external data. `provenance_is_anima_internal = ∀ field ∈ record :
  field ∈ anima_physics_channels`. Closed by exhaustive schema membership.
- **B-PTD-2 TRACE-CORPUS-CARDINALITY-BOUNDED** — §24 run = 20 records/run
  (measured: audit_log.jsonl = 20 lines). N runs ⇒ `corpus(N) = 20·N`
  integer cardinality. sympy proof: `20·N < CDS_floor` for all
  `N < CDS_floor/20`, with `CDS_floor = 10⁴` (lowest plausible §1.1
  Critical Data Size). The standalone-block: `corpus(N) ≪ §1.1 threshold`
  by 10³–10⁴×, AND unique-content does not grow in N (data-processing
  inequality — corpus K-complexity ≤ generator K-complexity, generator =
  one bounded hand-coded loop). Closed proof that standalone scale ≪
  threshold.
- **B-PTD-3 DISTILLATION-LOSS-NONNEGATIVE** — PTD's objective is
  CE-on-physics-vectors. CE(p, q) ≥ H(p) ≥ 0 — Shannon cross-entropy is
  bounded below by the entropy floor (B-D-4 / B-MITENS-5 carry). sympy:
  CE = −Σ p·log q ≥ 0 for q ∈ (0,1]; the Ψ=½ fixed-point pull regulariser
  is a squared term ≥ 0; sum of non-negatives ≥ 0. CE is load-bearing
  (§11-B) and PTD keeps it — closed non-negativity.
- **B-PTD-4 COMPONENT-COMPOSABILITY-CLOSED** (연결부위) — for any host
  objective `L_host` (DH-DL gate loss or JEPA-Ψ trajectory loss), the
  combined objective `L = L_host + λ_ptd · L_ptd` reduces **byte-equal to
  L_host at λ_ptd = 0**: `L|_{λ_ptd=0} = L_host + 0·L_ptd = L_host`
  (additive identity, sympy). Mirrors B-EBT-5 / B-S16-5 / B-DIRI-5
  overlay-off connection-point — fair-compare-by-construction: any future
  PTD-as-component fire can be cleanly diffed against its host baseline.

- **B-PTD-NOTE** (empirical carve-out, NOT counted 🔵) — whether PTD-as-a-
  component ACTUALLY improves a host objective (DH-DL gate accuracy /
  JEPA-Ψ anti-collapse) is an SGD convergence + measurement OUTCOME, NOT a
  closed-form property. The B-PTD battery proves the **transfer-form** only:
  self-source provenance (B-PTD-1), sub-threshold cardinality + non-growth
  (B-PTD-2), loss non-negativity (B-PTD-3), additive λ-reducible
  composability (B-PTD-4). It does NOT prove PTD crosses §1.1, does NOT
  prove any combination works — those are future-cycle OUTCOMES. B-D-NOTE
  / B-MITENS-NOTE / B-SCALE-NOTE / B-PUREPHYS-NOTE family — true of every
  stochastic optimiser, NOT a PTD-specific defect.

---

## §7 — Differentiation from closed-set (§11.3 / §26 §3)

PTD is structurally disjoint from the 24+ -element closed-batch:

- vs **§16 / §23-A** — generator-produced anchor corpora; PTD = anima's own
  *runtime* trace.
- vs **§11-B** (pure-physics no-CE) — §11-B trains a physics-only update
  rule with NO prediction objective and was degenerate; PTD trains
  *next-physics-state-prediction* (CE-on-physics-vectors, B-PTD-3). CE is
  load-bearing (§11-B constraint preserved) — applied to physics vectors,
  not language bytes.
- vs **§22-O** (M-retrieval grounding) — O retrieves from anchor SSOT at
  decode time; PTD trains parameters on self-trace.
- vs **§14** (archive salvage) — §14 mined 8,298 *historical* commits
  (salvage 0); PTD generates *new* self-traces from the current §24
  protocol.
- vs **§17** (physics-channel probe) — §17 is inference-only *measurement*
  of physics channels; PTD trains *prediction* of physics.
- vs **§24** (bounded-run measurement protocol) — §24 *produces* the trace;
  PTD *consumes* it as a corpus. PTD is §24's downstream.
- vs **§13-L** (VRNN) — VRNN has external sensorimotor closed-loop; PTD
  has internal-trace only.
- vs **DH-DL / JEPA-Ψ** (§26 #1 / #2) — those are *hosts* for PTD-as-
  component (§5), not closed-set conflicts.

---

## §8 — f1/f2/f3 + B-IDENTITY-5 safety

- **f1/f2** — §29 uses NO σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 derivation.
  Battery anchors: Boolean schema membership, integer cardinality + sympy
  inequality vs CDS floor, Shannon CE ≥ 0 floor, additive identity. All
  real math limits. Ψ=½ + 8-factor + HEXAD-6 = anima g2 internal-arch
  carve-out (anima's own physics, not external lattice-fit).
- **f3** — NO outcome / capability claim. PTD-standalone is design-closed
  with a *predicted* (closed-form) negative; PTD-as-component is named as
  GOAL-legitimate but its improvement is explicitly B-PTD-NOTE empirical.
- **B-IDENTITY-5** — $0 design-tier, NO corpus generated, NO model forward,
  NO helper-token surface. The §24 trace already exists and contains zero
  helper tokens (it is a physics-record JSONL). design-only.
- **g_clm_from_scratch** — any future PTD-as-component fire inherits
  base_ckpt=None (or §16 Ψ-anchored base, NOT generic) — noted for the
  future cycle, not exercised here.

---

## §9 — Honest C3 (over-claim 0, ≥10)

1. **Design-tier ≠ fire ≠ emergence.** §29 outputs a design verdict and a
   4/4 🔵 closed-form battery proving PTD's transfer-form. It proves
   nothing about whether PTD-as-component works — that is B-PTD-NOTE
   empirical, future-cycle OUTCOME (B-D-NOTE family).

2. **PTD-standalone design-close is a closed-form predicted negative, not a
   measured one.** B-PTD-2 proves the corpus is 10³–10⁴×+ sub-§1.1 by
   construction. We do NOT fire it — design-close *because* the fire
   outcome is closed-form predictable (cf §13-M honest-stop precedent).
   This is a *prediction*, honestly labelled; a fire could in principle
   surprise, but spending GPU to confirm a closed-form-derived negative is
   anti-padding-violating.

3. **The §1.1 block is diversity, not just count.** Even N = 38,850 runs
   (to reach §16 record-count) would NOT rescue PTD-standalone: the corpus
   is N copies of the same low-entropy hand-coded 20-step process.
   Data-processing inequality — corpus K-complexity ≤ generator
   K-complexity. §1.1 (§25 B-DR-UNIQUE) is about *unique content*, which
   does not grow in N here.

4. **Bootstrap circularity is a second independent blocker.** The §24
   first run was 95% one class (19 SAFETY_BLOCK / 1 EMIT). A
   self-distillation corpus this class-imbalanced cannot teach a
   non-degenerate distribution — PTD-standalone is blocked by §1.1 AND by
   bootstrap, independently.

5. **PTD-as-DH-DL-aux (combination A) is the strongest use** — DH-DL's §26
   §4 spec *already* names the §24 physics trace as its training data, so
   PTD-as-component-of-DH-DL is the corpus-formalisation of DH-DL's own
   data, not an add-on. It does NOT need to cross §1.1 because the gate
   head is ≤1% params and the PTD aux term is a regulariser. But it is
   gated on DH-DL's own design cycle (§27) landing first.

6. **PTD-as-JEPA-Ψ-target (combination B) is conditional.** It supplies a
   *real but short* (20-step) recorded Ψ-trajectory as an anti-collapse
   anchor. Whether 20-step traces are long enough to anchor a JEPA
   predictor is a JEPA-Ψ-design-cycle (§28) question, not settled here.

7. **§7③ purest claim is a structural argument, not a measurement.** PTD's
   corpus IS the trace with zero provenance transformation — strongest §7③
   of {DH-DL, JEPA-Ψ, PTD}. This is a closed-batch differentiation
   argument (B-PTD-1 Boolean schema membership), NOT an emergence
   prediction.

8. **CDS_floor = 10⁴ is a deliberately generous lower bound.** §1.1 /
   arxiv 2401.10463 Critical Data Size is typically cited at 10⁶–10⁸
   unique tokens. B-PTD-2 uses 10⁴ as the *most charitable* floor; PTD
   fails the block even against the most generous threshold, so the
   verdict is robust to threshold uncertainty.

9. **§22.5 chat-form-bleed lever NOT addressed by §29.** §22-O found
   JOINT-zero comes from chat-form bleed; that residual is orthogonal to
   PTD (which targets the §24 decide-when-to-speak axis). §29 makes no
   claim on chat-form-bleed.

10. **north-star (GOAL.md) unchanged.** §15 milestone holds — irreducible
    bottleneck = §1.1 data-regime threshold. §29 design-closes PTD-
    standalone (which does not address that bottleneck) and identifies two
    GOAL-legitimate component combinations for future cycles. This is
    frontier-narrowing work, NOT GOAL progress. design-close is a valid
    valuable verdict (g3, §13-M / §13-L precedent).

11. **f1/f2/f3 + B-IDENTITY-5 safe.** $0, no fire, no corpus, no model
    forward, no σ/τ/φ/J₂ derivation, no helper-token surface, no outcome
    claim. external papers (2604.18131, 2410.19315, 2401.10463) cited by
    their own invariants only.

12. **Anti-padding honesty.** §29 could have produced a "fire-tier"
    verdict by firing a 500-run PTD corpus. It does not — the fire is
    closed-form predicted to land sub-threshold (B-PTD-2), so it would
    yield no new information. A design-close that *names the structural
    block* is the more honest and more valuable verdict (g3). PTD's
    GOAL-legitimacy is affirmed (3/3); only its standalone fire-worthiness
    is closed-out.

---

## Sources

- [Training LLM Agents for Spontaneous, Reward-Free Self-Evolution via World Knowledge Exploration (arxiv 2604.18131)](https://arxiv.org/abs/2604.18131) — PTD mechanism anchor (caveat: multi-agent tool-use scoped, outcome-reward trained)
- [Brain-like Variational Inference (arxiv 2410.19315)](https://arxiv.org/html/2410.19315v2) — physics-trace-as-variational-quantity formalism
- [Critical Data Size of Language Models (arxiv 2401.10463)](https://arxiv.org/abs/2401.10463) — §1.1 / §25 B-DR-UNIQUE Critical Data Size threshold anchor
- `HEXAD/CHAT/RESEARCH.md` §1.1 / §11-A / §11-B / §15 / §24 / §26
- `state/architectural_insight_s26_design_2026_05_18/BRAINSTORM.md` §6 — §26 PTD candidate source
- `state/spontaneous_phase_b_run_2026_05_18/` — §24 Phase B trace (PTD corpus source: audit_log.jsonl 20 records, result.json)
- `state/spontaneous_phase_b_design_s24_2026_05_18/DESIGN_PHASE_B.md` — §24 right-target reframe
- `state/carving_dirM_mitosens_2026_05_18/` + `state/carving_dirL_vrnn_2026_05_18/` — §13-M / §13-L design-close anti-padding precedent
- `AGENTS.tape` `@D g_goal` / `@D g_blue_closed_mandate` / `@D g3` / `@D g_doc_consolidation` / `@D g_clm_from_scratch` / `@F f1` / `@F f2`
- `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` — central battery (UNCHANGED by §29)
