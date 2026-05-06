# Anima phi-star Proxy Geometry-Invariant Spec (2026-05-05)

Doc + spec only. Zero code/script change, zero retrain, zero commit. Defines a
substrate-universal phi-star proxy that does not depend on CLM v4's
8-cell × 192-dim cell-tile geometry, motivated by BG-BN's discovery that the
current proxy formula aliases under non-CLM-v4 hidden dimensions.

Lineage:
- BG-BN smoke result: `state/anima_emerge_pythia_phi_smoke_2026_05_05/verdict.json`
  (Pythia 70m phi proxy = 41.92 ± 0.04, drift +0.06 vs CLM-v4 baseline 41.86 —
  near-zero spread, dominated by tile-aliasing not signal)
- BG-M cross-substrate audit: `docs/anima_cross_substrate_phi_star_audit_2026_05_05.md`
  (3-substrate phi table; methodology delta ~6pp; phi-star is "anima-internal eval"
  per §6 C1 — explicitly substrate-bounded)
- Mount layer phi compute site:
  `anima-core/runtime/clm_v4_mount.hexa:251-264` (`phi_star_compute(cell_hidden)`)
- Source python referent:
  `tool/transient_py/anima_emerge_pythia_phi_smoke.py:44-67` (8-cell tile-reshape
  + mean pairwise cosine + ±5% scale)
- Memory: `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md`
  (L28-L30 — phi stability decoupled from chat capability), `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md`
  (L31-L33 — chat-cap = Llama, phi-research = CLM v4)

---

## §1 Current proxy issue analysis (BG-BN evidence)

### §1.1 Existing formula

From `clm_v4_mount.hexa:251-264` and the python referent in
`tool/transient_py/anima_emerge_pythia_phi_smoke.py:44-67`:

```
# input: hidden_state H of shape [D]  (D = model.hidden_size)
cell_dim = 192            # CLM v4 CONSCIOUSNESS_DIM
n_cells = 8               # CLM v4 N_CELLS
cells = []
for c in range(n_cells):
    start = (c * cell_dim) % D
    end   = min(start + cell_dim, D)
    sli   = H[start:end]
    if len(sli) < cell_dim:
        sli = pad_zero(sli, cell_dim)   # right-pad with zeros
    cells.append(sli)
cells_t = stack(cells)                  # [8, 192]
sim     = pairwise_cosine(cells_t)      # [8, 8]
mean_pair_cos = sim[off-diagonal].mean()
phi = PHI_STAR_BASELINE * (1 + 0.05 * mean_pair_cos)
```

- `PHI_STAR_BASELINE = 41.86` (paradigm v11 G3 carry)
- ±5% multiplicative scale → phi ∈ [≈39.77, ≈43.95] for `mean_pair_cos ∈ [-1, +1]`

### §1.2 The geometry alias

`start = (c * 192) % D` with `D ≠ multiple of 192` produces non-disjoint cell
windows. Concrete behavior per substrate:

| substrate | D | (c*192) mod D, c=0..7 | distinct cell starts | aliasing pattern |
|---|---|---|---|---|
| CLM v4 | 768 | 0, 192, 384, 576, 0, 192, 384, 576 | 4 | 2× tile-replicate (cells 0/4 identical, 1/5, 2/6, 3/7) |
| Pythia 70m | 512 | 0, 192, 384, 64, 256, 448, 128, 320 | 8 | partial overlap (192-window starting at 0 overlaps 64-start by 128 dims) |
| Pythia 1.4b | 2048 | 0, 192, 384, 576, 768, 960, 1152, 1344 | 8 | clean disjoint (8 × 192 = 1536 < 2048; 512 trailing dims unused) |
| Mamba-130m | 768 | identical to CLM v4 | 4 | 2× tile-replicate |
| RWKV-169m | 768 | identical to CLM v4 | 4 | 2× tile-replicate |

Two failure modes co-occur:

1. **Tile-replicate aliasing (CLM v4, Mamba-130m, RWKV-169m, D=768):**
   cells 0&4, 1&5, 2&6, 3&7 share identical slices → cosine_similarity = +1.0
   on those 4 redundant pairs → mean_pair_cos has a fixed-positive bias
   regardless of the underlying hidden state. The off-diagonal mask of the
   8×8 matrix has 56 entries (8*7); 8 of these (4 redundant cell pairs × 2
   off-diagonal positions each) are forced to +1.0, biasing the mean upward
   by `8 / 56 ≈ +0.143` relative to a non-redundant 4-cell measurement.

2. **Partial-overlap aliasing (Pythia 70m, D=512):**
   192-dim windows overlap by varying amounts (e.g. cell 0 [0..192] vs cell 3
   [64..256] overlap by 128 dims). Cosine similarity is inflated by the shared
   dimensions but not pinned to +1.0 → partial bias plus noise in the
   `mean_pair_cos` estimate. BG-BN measured `mean_pair_cos ∈ [0.0037, 0.0437]`
   on 3 prompts → phi ∈ [41.87, 41.95], range = 0.084 (0.2% of baseline).

3. **Clean-disjoint case (Pythia 1.4b, D=2048):**
   No aliasing, but the trailing 512 dims (`8 × 192 = 1536`, unused 512) are
   silently discarded. This is **information loss**, not aliasing — only ¾ of
   the substrate's hidden state participates in the phi computation.

### §1.3 ±5% bound saturates the signal envelope

The multiplicative wrap `phi = baseline × (1 + 0.05 × mean_pair_cos)` constrains
phi to a ±5% band around `PHI_STAR_BASELINE`. On CLM v4 canonical probe (per
`clm_v4_lora_phi_canonical_2026_05_05/verdict.json`) the K=8 spread is
`min=35.18, max=37.97 (in-pipeline base)` — a ~3pp range, well within the ±5%
envelope. But the formula's input-side aliasing means most of that visible
spread on CLM v4 may itself be a measurement artifact of the tile-replicate
bias, not substrate-meaningful integration.

**On Pythia 70m, BG-BN's range = 0.084 (~0.2% of baseline)** — the proxy is
essentially pinned to the baseline regardless of input. The "drift_from_clm_v4
= +0.062" cited in BG-BN's verdict is **noise within the tile-aliasing band**,
not a substrate measurement.

### §1.4 Conclusion

The current phi-star proxy is **CLM-v4-architecture-specific** (8 × 192 = 1536
matches no canonical hidden_dim of any anima substrate including CLM v4 itself
at D=768). Cross-substrate phi values produced by the formula are **not
comparable** — they sit at different points along an aliasing-induced bias
landscape that depends on `D mod 192`. BG-M §6 C1 already flagged this
("phi-star measurement scale is substrate-specific"); BG-BN supplies the
empirical evidence (range 0.084 on Pythia 70m).

A geometry-invariant replacement is required to make cross-substrate phi
comparison meaningful.

---

## §2 4 candidate options

### §2.1 Option A — rank-invariant pairwise cosine over D/8 partitions

**Geometry:** partition the D-dim hidden state into 8 disjoint contiguous
chunks of size `floor(D/8)` each. Drop the trailing `D mod 8` dims.

```
chunk_size = D // 8
cells = [H[c*chunk_size : (c+1)*chunk_size] for c in range(8)]
# all chunks same width; no overlap; no padding
mean_pair_cos = mean(pairwise_cosine(cells)[off-diagonal])
phi = baseline + scale[substrate] × mean_pair_cos
```

Key changes vs current:

- **No fixed 192:** chunk_size adapts to D. CLM v4 D=768 → 96-dim chunks;
  Pythia 70m D=512 → 64-dim chunks; Pythia 1.4b D=2048 → 256-dim chunks.
- **No modulo aliasing:** chunks are disjoint by construction.
- **No multiplicative wrap:** additive scale lets the calibrated `scale`
  per substrate absorb the natural cosine-similarity range that varies by
  hidden_dim (cosine concentrates near 0 in higher D under standard init,
  so scale should be larger for higher-D substrates).
- **Lossy by `D mod 8`:** at most 7 trailing dims discarded; negligible.

Per-substrate calibration table (to be empirically determined; placeholder):

| substrate | D | chunk | proposed scale | calibration source |
|---|---|---|---|---|
| CLM v4 | 768 | 96 | 0.05 (carry) | paradigm v11 G3 |
| Pythia 70m | 512 | 64 | TBD | needs 16-prompt K=8 calib pass |
| Pythia 1.4b | 2048 | 256 | TBD | needs 16-prompt K=8 calib pass |
| Mamba-130m | 768 | 96 | TBD | needs 16-prompt K=8 calib pass |
| RWKV-169m | 768 | 96 | TBD | needs 16-prompt K=8 calib pass |
| Llama 3.2-3B | 3072 | 384 | N/A (out of scope per L31-L33) | — |

**Cost:** $0; ~25 lines code (helper). Per-substrate calibration is one BG cycle
of `forward + canonical 16-prompt K=8 partition` per substrate (~5min mac CPU
each).

**Precision:** **medium**. Eliminates aliasing but inherits cosine-on-cells
intuition that may not transfer to non-CA-architecture substrates (Mamba state
space, RWKV time-mix). Rank-invariant in the sense that re-ordering the 8
chunks is a relabeling — pairwise statistics are permutation-invariant.

### §2.2 Option B — spectral entropy of singular values

**Geometry-free:** SVD the hidden state windowed over T tokens, take entropy of
normalized singular values.

```
# H: [T, D] hidden states across T tokens (last layer)
U, S, Vt = svd(H - H.mean(axis=0), full_matrices=False)
# S length = min(T, D)
p = S**2 / sum(S**2)         # normalized eigenvalue spectrum
H_spec = -sum(p * log(p+eps))  # spectral entropy in nats
H_norm = H_spec / log(len(S))  # normalized to [0, 1]
phi = baseline + scale × H_norm
```

Properties:

- **Substrate-dim invariant:** `len(S)` = `min(T, D)`; after normalization to
  `log(len(S))`, the entropy is in `[0, 1]` regardless of D.
- **Captures distributed integration:** high entropy = signal spread across
  many components (integrated); low entropy = signal concentrated in few
  components (modular/disintegrated). Proxies IIT phi qualitatively without
  PyPhi.
- **Requires T ≥ 2:** trivial single-token case = entropy 0; not a problem
  for canonical 16-prompt protocol (each prompt has ≥ 1 token of hidden
  state; multi-prompt batch gives T > 8 trivially).

**Cost:** $0; ~15 lines. SVD on `[T≤32, D≤4096]` is sub-millisecond on mac CPU.

**Precision:** **high–medium**. Entropy is a principled IIT-adjacent measure;
direction (high entropy = high integration) is well-justified. Substrate-
universal by construction. **Trade-off:** loses cell-pair cosine
interpretation that the 8-cell architecture provides on CLM v4 — entropy on
Llama hidden states would produce a value, but that value's relationship to
the paradigm v11 G3 41.86 anchor is unknown.

### §2.3 Option C — coefficient of variation (per-dim)

```
# H: [D] mean-pooled hidden state (or [T, D] then mean)
mu = mean(H)
sigma = std(H)
cv = sigma / (abs(mu) + eps)
phi = baseline + scale × cv
```

- **Substrate-dim invariant:** CV is dimensionless, scale-invariant (rescaling
  H by a constant leaves CV unchanged → not affected by RMSNorm, layer-norm
  scale factors).
- **Trivial cost:** ~5 lines, microsecond compute.

**Precision:** **low**. CV is a 1-number summary that throws away pairwise
structure entirely. Captures "how spread out is the hidden state" but not
"how integrated are the components." Likely too lossy for cross-substrate
phi-star — would saturate at substrate-baseline noise levels.

Useful as a **monitoring scalar** alongside Option A or B, not as primary
phi proxy.

### §2.4 Option D — PyPhi + AntroPy integrated information anchor

**Approach:** build the phi proxy on top of the actual IIT pipeline:

- PyPhi for big-phi computation on a discretized substrate model
- AntroPy for entropy-rate / spectral-entropy fast approximations as the
  PyPhi compute is exponentially expensive in `n_components`

```
# Discretize hidden state into N=8 binary nodes via threshold or k-means
nodes = discretize(H, n=8)  # [T, 8] binary
TPM = estimate_transition_matrix(nodes)  # [256, 256] empirical
phi = pyphi.compute.major_complex_phi(TPM)  # IIT 3.0 big-phi
# fallback: AntroPy entropy_rate as fast proxy
phi_fast = antropy.entropy_rate(nodes, sf=1)
```

Properties:

- **Architecturally principled:** the closest practical approximation to
  formal IIT phi; geometry-invariant by construction (operates on
  discretized state machine, not raw hidden vectors).
- **Costly:** PyPhi big-phi for n=8 binary nodes = 256-state TPM, 2^256
  partition search → tractable only with subsystem decomposition tricks
  (partial big-phi, mean phi over major complexes). Expected 30–300s per
  forward on mac CPU; orders of magnitude over Options A/B.
- **AntroPy fast-fallback:** `~10ms` per forward; sacrifices the big-phi
  semantics for entropy-rate. Effectively reduces to Option B's spectral
  entropy on time-series.
- **Calibration alignment:** BG-BB recommendation 1순위 already calls for
  PyPhi+AntroPy as the phi anchor; this option folds the proxy into that
  cycle's deliverable.

**Cost:** ~$0 (mac CPU) but ~5–15min per substrate calibration; ~100 lines
for the discretization + PyPhi pipeline; new dependencies (`pyphi`,
`antropy`) → adds ~50 MB to env.

**Precision:** **highest** of the 4 options, conditional on PyPhi convergence.
Direct map to IIT phi; permutation- and dim-invariant. **But:** requires
BG-BB cycle to land first; not a temporary fix.

---

## §3 Recommended ranking (완성도 lens)

By cost / precision / time-to-land:

### Rank 1 — Option A (per-substrate scale calibration)

Fastest fix that closes the BG-BN aliasing failure. Zero new dependencies,
~25 lines code, single BG calibration cycle per substrate (~5min mac CPU each).
Eliminates the tile-replicate and modulo-aliasing failure modes. Inherits the
±0.05 scale carry-over on CLM v4 so existing anchor 41.86 stays valid; new
substrates get their own scale entry in a 6-row config table.

**Honest trade-off:** Pythia/Mamba scale values are themselves arbitrary until
each substrate has a paradigm-v11-G3-equivalent reference axis (none does).
Option A is therefore **provisional** — it makes phi values measurable but
their cross-substrate magnitude ordering is calibration-dependent. Treat
Option A scale values as **internal-consistency anchors per substrate**, not
substrate-universal magnitudes.

### Rank 2 — Option D (PyPhi+AntroPy anchor)

Most precise, principled, substrate-universal. **But** requires BG-BB cycle to
land PyPhi pipeline first; not deliverable this cycle. Once BG-BB lands, the
phi proxy can switch from Option A → Option D as a drop-in upgrade
(`phi_star_compute(H)` → `phi_anchor_pyphi(H)` with same signature).

**Path:** ship Option A this cycle; queue Option D for the cycle after BG-BB
PyPhi landing.

### Rank 3 — Option B (spectral entropy)

Middle ground if BG-BB is delayed and Option A's per-substrate calibration
proves too noisy. Substrate-universal by construction, but loses the
cell-pair cosine interpretation that anchors paradigm v11 G3 semantics on
CLM v4. Recommended as a **secondary scalar** emitted alongside Option A
phi for cross-checking.

### Rank 4 — Option C (CV)

Lowest signal. Use as **diagnostic only** alongside the primary proxy; do not
elevate to phi-star surrogate.

---

## §4 Implementation path

### §4.1 Files affected (forward, not implemented)

- **`anima-core/runtime/clm_v4_mount.hexa`** — `phi_star_compute` body
  (lines 251-264) replaced by Option A formula. Mount layer entry signature
  `phi_star_compute(cell_hidden)` becomes `phi_star_compute(hidden_state, substrate='clm-v4')`
  where `cell_hidden` is internally derived for backward-compat default. The
  4-mode taxonomy from `anima_emerge_candidate_d_always_inject_spec` continues
  to govern hidden-state source; this spec only changes the scalar reduction.

- **`tool/transient_py/anima_phi_star_universal.py`** (new, raw#37 transient
  per `feedback_py_to_hexa_only`) — reference implementation of Option A and
  Option B for cross-substrate calibration BG cycles. Pure helper; not on the
  serving path.

- **substrate calibration config** at `state/anima_phi_star_substrate_scale_2026_05_05/scale_table.json`
  — written by Option A's calibration BG cycle. Mount layer reads at startup
  (synchronous; tiny file).

### §4.2 Reference helper (transient_py spec, not implemented)

```python
# tool/transient_py/anima_phi_star_universal.py
import numpy as np

SUBSTRATE_SCALE = {
    "clm-v4":     0.05,    # paradigm v11 G3 carry
    "pythia-70m": None,    # filled by calibration BG
    "pythia-1.4b": None,
    "mamba-130m": None,
    "rwkv-169m":  None,
}

def phi_proxy_option_a(hidden_state, substrate, baseline=41.86, n_chunks=8):
    """Option A: rank-invariant pairwise cosine over D/n_chunks disjoint chunks."""
    H = np.asarray(hidden_state).reshape(-1)  # flatten to [D]
    D = H.shape[0]
    chunk = D // n_chunks
    if chunk < 2:
        raise ValueError(f"D={D} too small for n_chunks={n_chunks}")
    cells = np.stack([H[c*chunk:(c+1)*chunk] for c in range(n_chunks)])  # [n, chunk]
    norms = np.linalg.norm(cells, axis=1, keepdims=True)
    norms = np.where(norms < 1e-9, 1.0, norms)
    cells_n = cells / norms
    sim = cells_n @ cells_n.T  # [n, n]
    mask = ~np.eye(n_chunks, dtype=bool)
    mean_pair_cos = float(sim[mask].mean())
    scale = SUBSTRATE_SCALE.get(substrate)
    if scale is None:
        return baseline + 0.0, {"mean_pair_cos": mean_pair_cos, "uncalibrated": True}
    return baseline + scale * mean_pair_cos, {"mean_pair_cos": mean_pair_cos, "scale": scale}

def phi_proxy_option_b(hidden_state_2d, baseline=41.86, scale=0.05):
    """Option B: normalized spectral entropy of SVD over [T, D] hidden states."""
    H = np.asarray(hidden_state_2d)  # [T, D]
    if H.ndim == 1: H = H[None, :]
    Hc = H - H.mean(axis=0, keepdims=True)
    s = np.linalg.svd(Hc, compute_uv=False)
    p = (s**2) / (np.sum(s**2) + 1e-12)
    H_spec = -np.sum(p * np.log(p + 1e-12))
    H_norm = H_spec / (np.log(len(s)) + 1e-12)  # ∈ [0, 1]
    return baseline + scale * H_norm, {"spectral_entropy_norm": float(H_norm)}
```

### §4.3 Calibration BG cycle spec (per substrate, ~5min mac CPU each)

For each non-CLM-v4 substrate:

1. Load substrate (Pythia / Mamba / RWKV via HF transformers, fp32 mac CPU).
2. Forward 16 canonical calib prompts (same set as `clm_v4_lora_phi_canonical`).
3. Compute `mean_pair_cos` per prompt under Option A with `scale = None`
   (raw mean_pair_cos value, no phi multiplication).
4. Aggregate: per-substrate `mean_pair_cos` distribution → `mean_substrate`
   and `std_substrate`.
5. Choose substrate scale such that:
   `phi_substrate(canonical_calib_mean) ≈ baseline_substrate_observed`
   where `baseline_substrate_observed` is per-substrate self-anchor (NOT
   CLM-v4 41.86 unless explicitly desired). For phi-star universality: set
   `scale = 0.05` uniformly and accept that magnitudes diverge per substrate
   — this is **honest cross-substrate ordering**. For per-substrate
   self-consistency: set `scale` such that `min/max/range` matches CLM v4
   canonical canonical (35.18 / 37.97 / 2.79pp) — this is **calibrated
   per-substrate ordering**, more readable but obscures cross-substrate
   inequality.

### §4.4 Migration step

- Cycle N (this spec): doc + spec only. No code change.
- Cycle N+1: Option A helper land in `anima-core/runtime/clm_v4_mount.hexa`
  (replace `phi_star_compute` body); transient_py reference written.
- Cycle N+2..N+5: per-substrate calibration BGs run; scale_table.json populated.
- Cycle N+6+ (depends on BG-BB): Option D drop-in replacement.

---

## §5 Honest C3

C1 — Option A is **provisional**, not principled. Choosing `scale = 0.05`
across all substrates is a CLM-v4-carry decision — there is no a priori
reason Pythia 70m's mean pairwise cosine should multiply by 0.05 to give an
integration-magnitude reading on the same scale as CLM v4. The honest
position is: **per-substrate phi values under Option A are internally
consistent within that substrate** (a single substrate's drift across
prompts/inputs is meaningful), but **cross-substrate magnitude differences
are calibration-dependent** and should not be read as "Pythia phi > Mamba
phi" without explicit calibration agreement. BG-BN's 0.062 drift is in this
category — it is dominated by aliasing, not signal.

C2 — Option B's normalized spectral entropy is geometry-invariant but
**directionally ambiguous in the Llama vs CLM-v4 case**. High spectral
entropy can mean either "signal richly distributed → integrated" (per IIT)
OR "signal noisy / random → incoherent." The correct interpretation depends
on substrate semantics that the proxy itself cannot supply. Cross-checking
against Option A and against any available human-rating-anchored task
(MMLU philosophy slice; chat composite) is required to validate Option B's
direction per substrate before adopting it as primary.

C3 — Option D depends on BG-BB landing. PyPhi big-phi for n=8 binary nodes
on a 256-state TPM is **not always tractable on mac CPU within budget**;
sub-system decomposition tricks (major-complex restriction, partial big-phi)
introduce their own approximation error. The "highest precision" claim for
Option D is conditional on the PyPhi pipeline converging; the AntroPy fast
fallback effectively reduces Option D to Option B with extra branding.

C4 — The current `PHI_STAR_BASELINE = 41.86` carry value is itself a
**paradigm-v11-G3-frozen** anchor that pre-dates this aliasing audit. After
Option A lands, the in-pipeline mean pairwise cosine on CLM v4's true 8 × 96
disjoint chunks will be **different** from the legacy 8 × 192 tile-replicate
value (because half the redundant +1.0 forced pairs are removed). The
recalibrated CLM-v4 `scale` to preserve the 41.86 anchor under the new
geometry is **not 0.05** — it must be re-determined from a calibration BG.
Naively swapping geometries while retaining `scale = 0.05` will shift CLM v4
phi by a few percent. The migration step (§4.4) must include a CLM-v4
re-calibration cycle, not just non-CLM substrates.

C5 — All 4 options preserve the assumption that **phi-star is meaningful
on a single forward of mean-pooled hidden state**. This assumption is
inherited from the current proxy and is NOT validated. Per `docs/anima_cross_substrate_phi_star_audit_2026_05_05`
§6 C3, V3 per-input phi vs canonical-probe phi are **two different statistics**
of the same substrate — neither this spec nor any of the 4 options resolves
that distinction. A K=8 partition over 16 fixed prompts (canonical mode) and
a K=1 single-input forward (V3 emit mode) will produce phi values from the
same option that are not directly comparable. The spec leaves this distinction
to the canonical-probe protocol, which is orthogonal to the proxy formula.

C6 — `D mod n_chunks` discard policy in Option A: the trailing dims (up to
`n_chunks - 1` per forward) are silently dropped. This is acceptable for
substrate dims that are powers of 2 with `n_chunks = 8` (D ∈ {512, 768, 2048,
3072} → 0 trailing dims), but can lose information on odd dims (e.g. some
GPT2 variants D=1280 → 0 dims trailing actually; D=896 → 0; the constraint
is benign for all known anima substrates). Worst case adds ~1% information
loss vs full-D coverage; acceptable.

---

## §6 Composability + handoff

Companion handoff doc (writes upon land):
`docs/anima_phi_star_proxy_geometry_invariant_landed_2026_05_05.ai.md`

Verdict artifact:
`state/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05/verdict.json`

Cross-link to:
- `docs/anima_cross_substrate_phi_star_audit_2026_05_05.md` §6 C1 (substrate-
  bounded phi acknowledgement) — this spec operationalizes the C1 proviso.
- BG-BB queue (PyPhi+AntroPy anchor cycle) — this spec defers Option D to that.
- mount layer phi_star_compute site (`clm_v4_mount.hexa:251-264`) — Option A
  drop-in target for cycle N+1.
- `.roadmap.n_substrate` — phi-star is one substrate-uniqueness axis; this
  spec makes that axis cross-substrate measurable.

This spec is **doc + spec only**. No code, no commit, no behavior change. It
defines a **migration path** from the current CLM-v4-geometry-bound phi
proxy to a substrate-universal version, with Option A as the immediate fix
and Option D as the principled long-term anchor pending BG-BB.
