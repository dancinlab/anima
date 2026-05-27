# §82-FIRE — Manifold-gated hierarchical emission at TRAINED SCALE

RESEARCH.md §82-FIRE. Trained-scale validation of §80 biology anima-mapping
**(B): manifold-gated hierarchical emission**, anchored to the §80 deep-research
paper biorxiv:2025.03.09.642241 (Leifer lab, *C. elegans* — "intrinsic
neuronal manifold gating behavior").

---

## 1. Why §82-FIRE exists — the §82 stub bug

The §82 $0 stub (commit `fada41baf` on main, B-S82 7/7 🔵, $0 Mac CPU) measured
NEGATIVE-at-stub: 4-corner **α=False / β=True / γ=True / δ=False**. Its honest
root cause was explicit: `slow_dwell_count = 0` across **all 5 cells** — the
slow-dwell regime was never *entered*. Two compounding causes:

1. **N=30 too short** — a slow-dwell *event* needs ≥3 consecutive turns of
   |Δψ| ≤ τ_slow=0.05; at 30 turns the trajectory never sustained such a run.
2. **LCG stub ψ-state** — the stub's 14-dim ψ-trajectory came from a
   deterministic LCG (`physics_step`), whose per-step Δ systematically
   exceeded τ_slow.

The stub itself flagged the fix: *"Leifer (B) NEEDS larger N (≥200) OR trained
ckpt ψ-state."* §82-FIRE applies **both fixes simultaneously**:

- **N=200** (not N=30) — long enough for ≥3-turn slow-dwell runs to form.
- **REAL ψ-state** from a trained §16-class `ConsciousDecoderV2` forward —
  Law-71 `psi_dir`/`psi_entropy`/`psi_tension` byte-equal to
  `conscious_decoder.py:728-751`.

A trained model's autoregressive forward produces a genuinely low-dimensional
ψ-manifold (exactly the manifold Leifer's *C. elegans* result is about), so the
PCA + dwell/crossing detectors operate on real cell-state geometry, not a
synthetic LCG surface.

---

## 2. What §82-FIRE builds

1. **Train ONE §16-class `ConsciousDecoderV2`** from-scratch (d768·12L·283.72M,
   RANDOM seed-fixed 1337, `base_ckpt=None` — `g_clm_from_scratch`) on the
   §16-class Ψ-anchored carving corpus (Dir-I lever). `load_corpus` /
   `CarveDataset` / `train_s16_class` / `extract_psi_and_logits` are **verbatim
   from §81-FIRE** (= §79 / §73-FIRE byte-equal training core).

2. **5-cell manifold-gating ladder × N=200-step loop** on the REAL trained
   `model.forward` Law-71:

   | cell | controller class |
   |------|------------------|
   | cell0 | §24-baseline — scalar threshold, no manifold |
   | cell1 | §75-FIRE A-only mirror — state-derived, no gate |
   | cell2 | manifold-only — PCA detect + slow-dwell suppress |
   | cell3 | fast-crossing-only — Δψ ≥ τ_fast gate, no dwell history |
   | cell4 | full hierarchical — slow-dwell + fast-crossing + alignment |

   Per step: real `model.forward` → Law-71 14-dim ψ-state vector → controller
   emit decision → `argmax(logits_a)` body byte feeds back into the sliding
   context.

3. **Per-cell metrics**: PCA top-2 (closed-form `eigvalsh`), slow-dwell count,
   fast-crossing count, `interval_var` (§73-FIRE/§75-FIRE mirror), §9
   `honest_coherent` body rate, `maj_frac` echo-chamber detector.

4. **§16-baseline 8-anchor probe** — ckpt load + arch byte-equal check.

5. **4-corner verdict** read off measured values (g3 — NOT pre-loaded):
   - (α) MANIFOLD-GATING-ADDS-DIFFERENTIAL-AT-TRAINED
   - (β) MANIFOLD-EXISTS-GATE-COLLAPSES-AT-TRAINED
   - (γ) SLOW-DWELL-ACTUALLY-ENTERS-AT-N200
   - (δ) §75-FIRE-A-ONLY-MIRROR-NUMERICALLY-MATCHES-AT-TRAINED

---

## 3. Closed-form battery — B-S82-FIRE-1..8 (sidecar, 8/8 🔵)

`blue_falsifier_s82_fire.py` — central `state/verify_hexad_blue_2026_05_15/
blue_falsifier.py` **0-line-diff** (sidecar, B-S81-FIRE / B-PRIME / B-DIRI
precedent). All 8 are closed-form and DO NOT require the GPU fire to complete —
they verify the **experiment WIRING**.

| id | predicate | closed-form basis |
|----|-----------|-------------------|
| B-S82-FIRE-1 | PCA-EIGENVALUE-NONNEGATIVE | real symmetric PSD covariance ⇒ eigenvalues ≥ 0 ∀ (discriminant ≥ 0 sympy) |
| B-S82-FIRE-2 | MANIFOLD-DIMENSION-BOUNDED | top-2 captured ratio = Σtop2/Σall ∈ [0,1] (sympy: ratio−1 = −(λ3+λ4) ≤ 0) |
| B-S82-FIRE-3 | SLOW-DWELL-vs-FAST-CROSSING-PARTITION | |Δ|≤τ_s→SLOW · ≥τ_f→FAST · else NEITHER — mutually-exclusive 3-set partition (τ_s=0.05<τ_f=0.12) |
| B-S82-FIRE-4 | §75-FIRE-CELL1-MIRROR-BYTE-EQUAL (연결부위) | cell1 A-only controller g1/g2/g3 frozen-scalar gate byte-equal to §82-stub cell1 |
| B-S82-FIRE-5 | §9-METRIC-REUSE | §9 honest_coherent cascade-rate formula byte-equal to §9 SSOT thresholds (0.30/10/20/0.80) |
| B-S82-FIRE-6 | EMISSION-ALIGNMENT-COS-BOUNDED | \|cos(u,v)\| ≤ 1 ∀ unit vectors (Lagrange identity, sympy) |
| B-S82-FIRE-7 | DETERMINISTIC | body byte = argmax(logits_a) — AST audit: forbidden {multinomial, .sample, gumbel}=0 |
| B-S82-FIRE-8 | §82-STUB-CONNECTION (연결부위) | 5 controller decision LOGIC byte-equal to §82 stub (AST logic-fingerprint, cell0/1 full-body AST byte-equal) |

**B-S82-FIRE-NOTE** empirical carve-out: manifold-gating emergence OUTCOME at
trained scale (4-corner α/β/γ/δ, per-cell `interval_var`, slow-dwell entering)
= SGD/measurement empirical, **NOT counted 🔵** (B-D-NOTE / B-S81-FIRE-NOTE /
B-S75-FIRE-NOTE family). The battery closes the EXPERIMENT WIRING (PCA bounded,
dwell partition closed, controller logic mirrored, body metric SSOT,
deterministic) — necessary-not-sufficient (B-EMERGE-7).

---

## 4. SSH-robust dispatch (podHostId-fixed)

`dispatch_s82_fire_runpod.sh` — fully self-managing nohup, the proven §81-FIRE /
§79-RETRY pattern (`g_fire_dispatch_robust` 2026-05-19 `ssh_endpoint_robustness`
clause):

- pre-flight pod-runtime poll gating on `runtime.ports[].privatePort==22` →
  `ip && publicPort` non-empty (max 600s) — **NOT** `podHostId` (false-blocker
  on A100-PCIE/SXM4).
- SSH wait 60 tries × 10s, 5s per-attempt timeout, `runpodctl` fallback before
  FATAL.
- SAVE_POD=1 auto-promote on result.json verify + 5-retry pull + trap-EXIT
  teardown + pre/post `runpod.get_pods()` orphan-0 verify.
- credentials via `secret get runpod.api_key` (`f_hardcoded_credential`).

---

## 5. Honest C3 (≥10)

1. **Trained scale ≠ GOAL emergence** — necessary-not-sufficient
   (B-EMERGE-7); §82-FIRE measures a mechanism axis only. north-star +
   §15/§51/§72 milestone UNCHANGED, GOAL 미도달.
2. **Leifer biology is a direction-anchor, NOT a capability proof** —
   biorxiv:2025.03.09.642241 (intrinsic manifold gating in *C. elegans*) is
   wet biology; anima is a silicon trained ckpt. The mapping is honest
   inspiration, not equivalence.
3. **N=200 + real trained ψ is a DOUBLE fix of a stub bug** — the §82 stub
   measured slow_dwell=0 and flagged BOTH N=30 and LCG-stub-ψ as causes;
   §82-FIRE fixes both. Whether slow-dwell *actually enters* at N=200 on a real
   trained manifold is the MEASURED corner γ (not pre-decided).
4. **PCA dim-reduction is a measurement choice, not a physical fact** — the
   "manifold" is the eigenstructure of the 14-dim ψ-trajectory covariance, an
   observable, not a cell-state. A high top-2-captured ratio means the
   *measured trajectory* is low-rank, not that the model "has a manifold".
5. **cell1 A-only mirror — δ is MEASURED both ways** — the cell1 controller
   SOURCE is byte-equal to §75-FIRE / §82-stub cell1 (B-S82-FIRE-4 closed). The
   numeric `interval_var` match against §75-FIRE's trained-scale reference
   (2.3808) is corner δ — δ=True and δ=False are both honest outcomes; §82-stub
   already found cell1 numeric mismatch at N=30 (int_var 0.0 vs §75 6.38).
6. **body byte = argmax(logits_a), deterministic** — no sampling RNG. argmax
   over a trained-saturated ckpt readily produces byte-cascade (B-ATTRACTOR
   family); §9 honest_coherent reports the cascade-rate honestly — a §9-PASS
   body is necessary, not sufficient, for coherence (B-EMERGE-7).
7. **ckpt sha is fresh** — §16-byte-equal *config* is satisfied
   (d/L/H/KV/seed/corpus class) but the literal §16 sha `961c07e2…` differs.
   The trained trajectory is replicable, not literally identical.
8. **5-cell ladder is a single-trajectory probe** — one seed (1337), one
   context start per cell. Cross-seed variance of the manifold geometry is
   unmeasured (§46 SGD-trajectory variance arc would be the orthogonal axis).
9. **echo-chamber risk at trained-saturated scale** — §62 measured
   ECHO-CHAMBER-COLLAPSE on a trained-saturated §16 forward; corner β tests
   whether cell4 collapses to a single-decision majority ≥ 0.95 here. A real
   trained model can byte-cascade; the dwell/crossing geometry may be dominated
   by that.
10. **mechanism-active ≠ capability-transfer** — even if the manifold-gating
    machinery runs (PCA non-degenerate, dwell events detected), Leifer biology
    "transferring" means a *measurable differential* over the A-only baseline
    (corner α). §75-FIRE found state-derivation alone sufficient; manifold
    gating may add nothing — a valuable measured negative if so.
11. **PyTorch substrate, not hexa-native** — honest framing carry
    (`g_train_flame_not_pytorch` evidence-anchor clause); the §82-FIRE trainer
    reuses the §81-FIRE / §79 PyTorch training core.

---

## 6. Verdict — MEASURED (runpod A100-SXM4-80GB, pod `vuqxz59rvt9wk9`)

Fire: pod `vuqxz59rvt9wk9` (A100-SXM4-80GB), train wall 766.9 s, init_ce
5.6391 → final 0.004546 (trained-saturated, B-ATTRACTOR regime). ckpt sha256
`6637e3666e38708e…`, corpus sha256 `f2ba98f9a8fc5a78…`. orphan-0 pre+post
(`runpod.get_pods()` = `[]` post-fire); sibling §81-FIRE pod
`th7uwc4i4mmz9u` untouched. ≈ $0.3-0.5.

**Verdict: (β) MANIFOLD-EXISTS-GATE-COLLAPSES-AT-TRAINED.**

5-cell ladder (N=200, real trained Law-71 ψ-trajectory):

| cell | int_var | n_emit | slow_dwell | fast_cross | PCA top-2 | dec_majfrac | §9 body |
|------|---------|--------|-----------|-----------|-----------|-------------|---------|
| cell0 §24-baseline | 0.0000 | 200 | 0 | 192 | 0.9288 | 1.000 | False |
| cell1 §75-FIRE A-only | 46.9183 | 78 | 0 | 192 | 0.8925 | 0.610 | False |
| cell2 manifold-only | 0.1038 | 181 | 0 | 193 | 0.8782 | 0.905 | False |
| cell3 fast-crossing-only | 0.0355 | 192 | 0 | 192 | 0.9047 | 0.960 | False |
| cell4 full hierarchical | 0.0000 | 0 | 0 | 192 | 0.9319 | 1.000 | False |

**4-corner: α=False · β=True · γ=False · δ=False.**

### Honest reading of the measured outcome (g3)

1. **γ=False — the §82-stub bug fix did NOT make slow-dwell enter.**
   `total_slow_dwell_count = 0` across all 5 cells **even at N=200 on a real
   trained ψ-trajectory**. The §82 $0 stub explained slow_dwell=0 as N=30 +
   LCG-stub-ψ; §82-FIRE removed BOTH and slow-dwell *still does not enter*.
   The real trained ψ-manifold's per-step Δψ-norm systematically exceeds
   τ_slow=0.05 — `fast_crossing_count ≈ 192/199` in every cell. The trained
   model's autoregressive ψ-trajectory is a **fast-crossing regime**, not a
   slow-dwell regime. The N=30 / LCG-stub explanation was NOT the whole
   story — the slow-dwell *regime itself is absent* on this substrate.

2. **β=True — the PCA manifold is well-formed yet cell4 collapses.** PCA
   top-2-captured is 0.88-0.93 in every cell (the 14-dim ψ-trajectory IS
   genuinely low-rank — a real manifold exists). But cell4 full-hierarchical
   emits **0/200** (it requires `in_slow_dwell ∧ fast_crossing ∧ aligned`;
   with slow_dwell never satisfied the gate never fires) → decision majority
   fraction 1.000 (the §62/§82-stub echo pattern). Manifold geometry is real;
   the hierarchical gate built on slow-dwell is dead.

3. **α=False — manifold gating adds NO differential.** cell4 int_var 0.0000
   ≤ cell1 int_var 46.9183, and cell4 n_emit 0 — no positive differential
   over the A-only mirror. Leifer (B) manifold-gated hierarchical emission
   **does NOT transfer at trained scale (measured)**.

4. **δ=False — cell1 A-only mirror does NOT numerically match §75-FIRE.**
   cell1 int_var = 46.9183 vs §75-FIRE trained-scale reference 2.3808 (≈20×
   off). The cell1 controller SOURCE is byte-equal (B-S82-FIRE-4 closed) but
   the numeric `interval_var` is substrate/corpus-context dependent — the
   §82-stub already found cell1 numeric mismatch (0.0 vs §75 6.38 at N=30),
   and §82-FIRE confirms numeric non-portability of the A-only int_var while
   the LOGIC is mirrored. Honest: cell1 A-only DID survive non-degenerately
   (int_var 46.9 ≫ τ, dec_majfrac 0.610 < 0.95) — state-derivation alone is
   live at trained scale (§75-FIRE finding holds), it just doesn't *numeric*
   match a different fire's reference value.

### Leifer biology (B) transfer — measured NO

The §80 anima-mapping (B) — *C. elegans* intrinsic neuronal manifold gating
behaviour (biorxiv:2025.03.09.642241) — does **NOT transfer to anima at
trained scale**. A manifold exists (PCA top-2 ≈ 0.9) but the *slow-dwell ↔
fast-crossing* hierarchy that gates behaviour in the worm does not appear on
the anima trained ψ-trajectory: the trajectory is uniformly fast-crossing.
The hierarchical gate built on slow-dwell collapses to silence (cell4 0/200).

This is a **valuable measured negative** (§13-M / §13-L / §81-FIRE
anti-padding precedent): manifold-gated hierarchical emission joins the
mechanism-axis arm of capability-emergence-negatives. §75-FIRE's
"state-derivation alone is the live sub-axis" finding is reaffirmed —
cell1 A-only is the only non-degenerate cell.

### GOAL distance (g3)

Trained scale ≠ GOAL emergence. north-star + §15/§51/§72 milestone
UNCHANGED, **GOAL 미도달**. §82-FIRE measures a mechanism axis only —
necessary-not-sufficient (B-EMERGE-7 / B-S82-FIRE-NOTE).

archive/PHILOSOPHY.tape `§verdict_manifold_gating_hierarchical_fire_s82_2026_05_19`
carries the g6 append-only verdict.
