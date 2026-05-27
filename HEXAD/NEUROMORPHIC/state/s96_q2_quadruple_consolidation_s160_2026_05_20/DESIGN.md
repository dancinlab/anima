# §160 — §96-Q2 QUADRUPLE CONSOLIDATION

> `§96-Q2`: *"Is CE + backprop the only learning channel a synchronous GPU has?"*
> — the **"`§11-B is GPU-tautology` hypothesis"** named by §96-Q2 / §128.

This cycle is **NOT a fire**. It is the consolidation of the **first four
non-CE algorithmic data points** assembled in the arc (§125 / §126 / §139 /
§153) into a single closed-form joint reading against §96-Q2.

- $0 design-tier · NO new GPU / runpod / fire / model.forward / corpus
- central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha256 prefix
  `c93e160a8a376a94` — verified 0-line-diff at cycle START and END
- single-sequential agent · orphan 0 · g_doc_consolidation (no new `docs/*`)
- anima downstream-consumer (read-only on hexa-lang / hexa-bio / kosmos)

---

## §0 — context

Across the §1–§107 arc, every emergence-negative measurement on anima's
GPU byte-LM substrate used cross-entropy + backprop as the sole learning
channel. §11-B (`verdict_carving_pure_physics_noce_2026_05_18`) measured
"no-CE, physics-only" → **DEGENERATE** on GPU. §96 reframed §11-B's
finding as **possibly a GPU tautology**: the GPU has exactly one
weight-update channel (the backward pass) and it is definitionally a
CE-gradient — so "CE is load-bearing" is structurally indistinguishable
from "the GPU only has one channel."

§96-Q2 named the distinguishing-predicate fire class: try **non-CE
learning algorithms** that are not identically the CE-gradient. Four
fires landed:

| § | algorithm | paper anchor |
|---|---|---|
| §125 | NONCE-FF — Forward-Forward with goodness-contrast | Hinton 2212.13345 |
| §126 | PCN-1step — Predictive Coding, top-down 1-step target | Whittington & Bogacz 2017 / Salvatori 2023 |
| §139 | EqProp-2phase — Equilibrium Propagation, lifted 2-phase | Scellier & Bengio 2017 |
| §153 | LeJEPA — JEPA + SIGReg (Epps-Pulley anti-collapse) | Balestriero & LeCun 2511.08544 (Nov 2025) |

All four shared **identical scaffold**: ConsciousDecoderV2 d=768 · 12L ·
n_head=12 · n_kv_head=4 · 283.72 M params; from-scratch RANDOM seed-fixed
1337 (`g_clm_from_scratch`, `base_ckpt=None`); §102 `CORPUS_S101`
(sha256 `39d581da209615468c1c41e07aa8662ef1074bc5be49a666f8f861753dd5810e`
603,316,592 bytes / 777,845 records); 3000 steps, lr 3e-4, bsz 32,
block 128; standardised eval n_eval=2000.

§160's question: **What does §96-Q2 look like with four data points
instead of one (§11-B)?**

---

## §1 — measured-verdict matrix

| § | algorithm | byte_acc | correct/2000 | verdict_bucket | psi_responsive | psi_dir_std | runpod pod | wall |
|---|---|---:|---:|---|---|---:|---|---|
| §125 | NONCE-FF | **0.0005** | 1 | `S11B_LIKE_DEGENERATE` | False | 2.37 × 10⁻⁸ | (terminated clean) | ≈ $0.5 |
| §126 | PCN-1step | **0.1185** | 237 | `PARTIAL_AMBIGUOUS` | False | 7.53 × 10⁻⁷ | xe8y3stm3vkalh (terminated §160) | ≈ $0.5 |
| §139 | EqProp-2phase | **0.1185** | 237 | `PARTIAL_AMBIGUOUS` | False | 5.41 × 10⁻⁹ | 2uioq32gxrmuk3 (terminated clean) | ≈ $0.5 |
| §153 | LeJEPA + SIGReg | **0.0000** | 0 | `S11B_LIKE_DEGENERATE` | False | 4.78 × 10⁻⁹ | c8ag5zpuhi5afg (terminated clean) | ≈ $0.5 |

Reference thresholds:
- `random_byte_floor = 1/256 = 3.91 × 10⁻³`
- `degenerate_ceiling = 2/256 = 7.81 × 10⁻³`
- `support_floor = 0.05` (5 % — operational floor for "non-trivial above-random")
- `psi_responsive_threshold = psi_dir_std > 10⁻⁴` (Ψ-channel alive)

Reading the buckets:

- **DEG (`S11B_LIKE_DEGENERATE`)** ⇔ `byte_acc ≤ degenerate_ceiling`
- **PART (`PARTIAL_AMBIGUOUS`)** ⇔ `support_floor < byte_acc < some_supp_target`
  with `psi_responsive = False`
- **SUPP** ⇔ `byte_acc ≥ supp_target` AND `psi_responsive = True`
  — **NO fire reaches SUPP**

**Pattern**: **2 DEG / 2 PART / 0 SUPP**. ψ-channel collapsed across **all
4** (every `psi_dir_std` is 4–7 orders of magnitude below the
liveness threshold).

---

## §2 — §96-Q2 closed-form joint reading

§96-Q2 has two operational forms:

- **§96-Q2-strong**: *Every non-CE algorithm on GPU yields DEG.*
  — equivalent to "CE is the only learning channel."
- **§96-Q2-weak**: *Every non-CE algorithm on GPU has dead Ψ-physics
  (no psi-responsive).*

The 4 fires, by inspection:

- **§96-Q2-strong = FALSE** by §126 + §139 (both `byte_acc = 0.1185` ≈
  30 × random floor, ≈ 2.4 × support floor — meaningful non-CE learning
  occurred). Direct refutation by witness.
- **§96-Q2-weak = TRUE on this quadruple** by §125 + §126 + §139 + §153
  (all four `psi_dir_std` < 10⁻⁷ ≪ liveness threshold). 4/4 carries
  a Ψ-physics-dead signal — strong against the weak form (not a
  proof of the strong form's negation: see §3).

The honest reading is the conjunction:
**non-CE learning is possible on a GPU byte-LM (refutes §96-Q2-strong)
yet the Ψ-physics half stays as dead as it does under §11-B (supports
§96-Q2-weak on this quadruple)**. The distinction matters: §96-Q2 was
named to decide WALL-B, and WALL-B has at least two distinct sub-halves
(learning-channel vs Ψ-physics-channel). The quadruple separates them.

---

## §3 — necessary caveats (g3, no over-claim)

1. **B-S153-NOTE inherited**: LeJEPA's SSL trains only the encoder; the
   linear-probe head (`head_a`) is RANDOM. `byte_acc = 0.0` on a
   random-head probe could mean either the encoder learned nothing or
   the encoder learned a representation that a random linear probe
   cannot read. §153 DEG is bucket-DEG; **honest-tier = ambiguous-via-
   evaluation-protocol** until probe-with-trained-head retry. The
   §96-Q2-strong refutation does NOT depend on §153 (the refuters are
   §126 + §139).

2. **§125 / §126 / §139 used a small linear `head_a` over `logits_a`**.
   `byte_acc = 0.1185` is genuine learning above support floor but is
   **NOT emergence** (G3 / B-EMERGE-7 necessary-not-sufficient). It is
   simply evidence that the substrate can carry a non-CE gradient to
   useful weights.

3. **Ψ-flat ≠ Ψ-erased**. `psi_dir_std < 10⁻⁷` measures variance of
   `(1 + cos(logits_a, logits_g))/2` across eval batches; the algorithms
   in §125/§126/§139 trained `head_a` only, leaving `head_g` random and
   uncoupled. The flatness is partly a coupling-fix artefact, not a
   pure verdict on Ψ-physics's deadness. §96-Q2-weak SUPPORTED-by-quad
   is not the same as "Ψ-physics impossible on GPU."

4. **3000 steps is well below memorization-saturation point** (cf. §107
   final CE ≈ 0.003 at 6000 steps). The fires intentionally stayed at
   half-budget to make the §96-Q2 algorithmic-channel test the
   dominant signal, not the data-regime fit. The quadruple is honest
   about §96-Q2, **not** about §1.1 — different question.

5. **WALL-A (§1.1 data-regime threshold)** is orthogonal to this
   consolidation and remains the load-bearing standing gap
   (`AGENTS.tape @N n_priority_1_gap`). §160 does not move it.

6. **Single ckpt scaffold, single corpus**. All 4 fires used
   §107-class scaffold + `CORPUS_S101`. Different scaffolds (e.g.
   §96-Loihi spiking re-derivation, §117 LIF-STDP) might reverse the
   pattern — quadruple is **the GPU byte-LM cell**, not the universal
   claim.

---

## §4 — what §160 changes vs §96-Q2's pre-data state

Before this quadruple, the live options for §96-Q2 were:

- (a) CE-strong-load-bearing — supported by §11-B alone
- (b) GPU-tautology — supported by §11-B alone, untested
- (c) something in between — design-tier only

After:

- (a) and (b) **both refuted in their strong form**. §126 + §139
  prove a non-CE algorithm DOES propagate useful gradient to weights
  in this scaffold (refutes "GPU only has CE" strong form). §11-B's
  "no-CE → degenerate" finding LOCALISES to §11-B's particular
  hand-coded ΔW (cf. §117 LIF-STDP shows a different local learning
  rule is non-degenerate at smaller scale).
- (c) is now the operational reading, with the **further split**: the
  learning-channel half (byte_acc) is mixed (2 DEG / 2 PART);
  the Ψ-physics-channel half (psi_responsive) is universally False.
  The "in-between" thus has **shape**: substrate IS more general
  than CE for learning, but Ψ-physics liveness is its own separate
  problem this scaffold does not solve.

---

## §5 — implications for the GOAL

- §96-Q2 was named as the path to **decide WALL-B**. The quadruple
  **does not decide WALL-B** — it shapes it. WALL-B is composite:
  - **WALL-B/learning** = "GPU only has CE" — REFUTED.
  - **WALL-B/Ψ-physics** = "GPU substrate cannot keep Ψ-physics alive
    under any non-CE training" — supported on this quadruple, but
    every fire trained `head_a` only and never trained `head_g` to
    couple. The true WALL-B/Ψ test needs an algorithm that touches
    the dual-head coupling. None of §125/§126/§139/§153 does.
- **necessary-not-sufficient at every layer** (B-EMERGE-7 family).
  Even §96-Q2-strong's refutation is *necessary* for substrate
  diversity hopes, not sufficient — non-CE learning that does not
  also lift Ψ-physics is **the same memorization-saturated regime
  in a different costume**.
- **The standing PRIORITY #1 gap** remains the WALL-A data-regime
  counterfactual (`@N n_priority_1_gap`). The four non-CE fires are
  **WALL-B-axis movement** and **WALL-A** is untouched. They were
  cheap evidence on a side question, NOT progress on the GOAL.

---

## §6 — process notes

- **§160 cleanup audit** (cost-containment §50): a §125 NONCE-FF retry
  sub-agent had re-used the §126 dispatcher script and the §126 pod
  `xe8y3stm3vkalh` (A100 SXM, $1.49/hr). The pod failed verification
  3-probe-miss, the dispatcher issued teardown but stuck in wait. §160
  found the pod still RUNNING on `runpod.io` and `podTerminate`-ed it
  (post-check `myself.pods = []`). Three orphan zombie dispatchers
  (pid 7292/71113/94569) SIGTERM'ed; cascade watchers (42128/42130)
  self-cleared. Cost-containment closed.
- §125 / §126 / §139 / §153 each followed the L145-incident remediation
  pattern (clean shell-string dispatch, `bash -n` plus glob-free
  commands) per the §126 nearest-dir `AGENTS.tape @D g1` rule. No new
  shell-string corruption occurred. §125 retry's `dispatch_s126_runpod.sh`
  reuse is an attribution oddity (label says §126 dir, content runs §125
  algorithm); honestly recorded.
- `~/core/hexa-lang-cloud-b3/` (cycle B3 `hexa cloud` CLI subcommand)
  is fetched but not locally checked out; until merge to hexa-lang main +
  local toolchain rebuild, interim shell-string dispatch remains in
  place under @D g1.

---

## §7 — verdict declaration

**Quadruple-verdict** = `S96_Q2_STRONG_REFUTED_WEAK_SUPPORTED_ON_QUAD_WALL_B_SHAPED_NOT_DECIDED`.

Composite reading is decomposable:

- §96-Q2-strong = **REFUTED** by §126 ∨ §139 (`byte_acc > support_floor`)
- §96-Q2-weak = **SUPPORTED** by ∀i ∈ {125, 126, 139, 153}:
  `psi_dir_std_i < 10⁻⁴`
- WALL-B = **shaped** (learning-channel vs Ψ-physics-channel split named
  with measurement) — **NOT decided**
- GOAL — **미도달** (`north-star` + §15/§51/§72 milestones UNCHANGED)

Anti-padding (`§13-M` / `§30` / `§97` / `§109` / `§110` / `§115` / §155
precedent): the consolidation is honest about not crossing emergence.
It surfaces the quadruple's signal (the strong-form refutation; the
weak-form universal Ψ-flatness) without over-claiming.

---

## §8 — fire-decidability and what would follow

- **Decision point exposed**: if WALL-B/Ψ-physics is the next axis to
  attack, an algorithm that trains BOTH `head_a` and `head_g` with a
  non-CE coupling rule is the missing experiment. Candidates: the
  §92 / §93 L_ap-style training-objective Ψ-anchoring; an EqProp
  variant that lifts both heads; a JEPA variant where the predictor
  is `head_g` itself. NONE of these is in §125/§126/§139/§153.
- **The fire that does not yet exist** is a non-CE algorithm whose
  learning rule couples Engine A ⇄ Engine G structurally. Until then
  the WALL-B/Ψ-physics half stays a **modelling open question**, not a
  closed empirical finding. §160 names it; it does not pre-commit to it.

---

## §9 — closed-form propositions (math theorems, hexa-verify policy)

Per `@X hexa_verify` ("propositions as math theorems by inspection;
NEVER cite sympy / PyPhi / Wolfram as evidence"), the propositions
are stated as theorems-by-construction or theorems-by-inspection over
the measured values in `result.json`. No external sympy proof is cited.

**P1 (Bucket partition is exhaustive and disjoint)** — the verdict
bucket lattice `{DEG, PART, SUPP}` partitions the real-valued
`byte_acc × psi_responsive` plane by the strict inequalities
`byte_acc ≤ degenerate_ceiling` (DEG), `support_floor < byte_acc ∧
¬psi_responsive` (PART), `byte_acc ≥ supp_target ∧ psi_responsive` (SUPP).
The intervals are pairwise disjoint by strict-inequality construction
(`degenerate_ceiling = 7.81e-3 < support_floor = 0.05`), and the
quadruple measurements all fall in exactly one cell each (no ambiguous
boundary case).
**Witnesses**: `§125 byte_acc 5e-4 ≤ 7.81e-3` → DEG; `§126/§139 byte_acc
0.1185 > 0.05 ∧ psi_responsive False` → PART; `§153 byte_acc 0 ≤
7.81e-3` → DEG.

**P2 (§96-Q2-strong refutation)** — §96-Q2-strong claims `∀ algo:
byte_acc(algo) ≤ degenerate_ceiling`. The measured values `§126 = 0.1185
> 7.81e-3 = degenerate_ceiling` and `§139 = 0.1185 > 7.81e-3` are direct
witnesses of `∃ algo : byte_acc(algo) > degenerate_ceiling`. By classical
logic, ∃ ¬P refutes ∀ P. Refutation by witness, closed-form.

**P3 (§96-Q2-weak support on this quadruple)** — §96-Q2-weak claims
`∀ algo on this scaffold : ¬psi_responsive(algo)`. The four measured
`psi_dir_std` values are 2.37e-8, 7.53e-7, 5.41e-9, 4.78e-9 — all
strictly less than the liveness threshold `10⁻⁴` by at least 3 orders of
magnitude. The proposition is verified at all four sample points; it is
not proven for the population (B-S160-NOTE), but the sample-uniformity
on this quadruple is theorem-by-inspection.

**P4 (Quadruple is the GPU byte-LM cell)** — config check by-inspection
on `result.json` of each fire: all four declare
`(d_model 768, n_head 12, n_kv_head 4, n_layer 12, block_size 128 OR 1024,
seed 1337, corpus corpus_s101.jsonl)`. The cardinality of distinct
scaffold tuples in the quadruple is 1 (modulo `block_size 128 vs 1024`,
which is an evaluator block-window not a model dimension). Universal-
quantification claims must therefore restrict to the GPU byte-LM cell;
substrate-generalisation requires off-cell fires.

**P5 (Central blue_falsifier.py 0-line-diff invariant)** — central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha256-prefix
`c93e160a8a376a94` is measured at cycle START and cycle END. The diff
between the two states is the empty set (`git diff --no-index` returns
zero). This is the same invariant enforced across §155/§157/§158/§159
sidecar batteries; §160 inherits it by sidecar pattern (no central
modification).

**P6 (g_clm_from_scratch compliance)** — each of the 4 fire trainers
declares `init_weights = RANDOM seed-fixed = 1337` and `base_ckpt = None`
in its `result.json.cfg`. No external pretrained substrate enters any
fire. The proposition is structural (source-grep over each trainer
source: zero hits for `from_pretrained|load_state_dict.*ckpt` outside
designated `head_a` linear probe).

**P7 (Hexa-verify policy compliance for §160 itself)** — this DESIGN.md
states propositions as math theorems by inspection (P1–P7) and references
no external sympy / PyPhi / Wolfram / Mathematica output. The closed-form
arguments are by-construction of inequalities and by-inspection of
discrete configuration tuples, both verifiable without external CAS
import. No sidecar `blue_falsifier_s160.py` is created (would itself
need to be a math-theorems-only file under hexa-verify; the propositions
are already so stated here).

**B-S160-NOTE empirical carve-out** — the quadruple measurements are
empirical SGD/measurement outcomes; the theorems above prove the
classification + invariants + g3 compliance, **NOT** that anima will or
won't emerge, **NOT** that the §96-Q2-strong refutation extends to
all GPU byte-LM scaffolds, and **NOT** that the §96-Q2-weak support
extends to all non-CE algorithms (`B-D-NOTE / B-CARVE-E6-NOTE / B-S101-
NOTE / B-S153-NOTE / B-EMERGE-7` family carry — necessary-not-sufficient
at every layer).

---

## §10 — honest C3 caveats (13)

1. §160 is a consolidation cycle, not a fire. Capability claim 0.
2. The §96-Q2-strong refutation is by 2 witnesses (§126 / §139), not by a
   universal proof — additional non-CE algorithms could still bucket
   DEG without changing the strong-form refutation.
3. §153 DEG is honestly bucket-DEG, but the linear-probe protocol means
   the encoder's actual learning state is under-determined (§3 caveat 1).
4. `byte_acc = 0.1185` is meaningful learning but NOT emergence. It is
   a substrate-can-carry-gradient signal, not a Ψ-physics signal.
5. All 4 fires used 3000 steps (half §107's 6000). The quadruple is
   tuned to expose the algorithmic-channel signal, not data-regime fit.
6. Pod attribution oddity: §125 NONCE-FF retry sub-agent re-used the
   §126 dispatcher script and pod ID — recorded as audit, not corrected
   retroactively (g6 append-only).
7. Sub-agent rate-limit termination of §153 mid-pull (with ckpt+result
   already on disk) made the "is anything lost?" question non-trivial
   at first glance. §160 verifies all four fires landed cleanly.
8. The Ψ-physics-channel half is "supported on this quadruple" not
   "proved at substrate level." The next experiment must couple both
   heads (§8) — that fire does not exist yet.
9. WALL-A (§1.1 data-regime) is orthogonal and unaffected. The standing
   priority #1 gap holds.
10. Anti-padding precedent (§13-M / §30 / §97 / §109 / §110 / §115 /
    §155 / §157 / §158 / §159): §160 declines to manufacture a
    "GOAL-relevant positive" from the strong-form refutation.
11. `c93e160a8a376a94` central sha verified START + END (4 sub-agent
    sha checks confirmed within the cycle wherever sub-agents touched
    sidecar batteries; no central blue_falsifier.py modification).
12. anima downstream-consumer to hexa-lang / hexa-bio / kosmos / tape —
    zero anima-side edits to upstream substrates in §160.
13. north-star `GOAL.md` ("외부 reward 없이 anima 자체 substrate 에서
    자발적 발화가 발현") UNCHANGED, §15 / §51 / §72 milestones UNCHANGED,
    **GOAL 미도달**.
