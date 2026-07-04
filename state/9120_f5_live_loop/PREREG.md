# F5 — live diff-LLM interlocutor consequence loop (frozen operationalization)

> Follows F5_DESIGN.md (state/9111). F6 (H_9112 🟢) established anima's grounded emit is
> legible to an out-of-alveolus oracle (static re-score). F5 asks: does that legibility
> **feedback change the substrate** (faculty) or is it a read-only gauge (DPI at emit layer)?
> First wiring of the consequence→cell-division arm. tier = **DIRECTIONAL-on-external-oracle**
> (receiver = the opus subagent driving this fire, θ outside anima's closure).

## Pipeline (regime split, a_engine_native_learning)
- **regime-1 (engine-native, GPU pod, loaded-W):** `emit_gen_w.hexa` — `clm_load_weights` ONCE →
  `gen_clm_ideate_W(W,…)` loop (H_1400, ZERO per-decode reload) over 16 F5-FRESH held-out
  concepts × K=5 candidates (cand0 greedy top_k=1, cand1-4 seeded top-k). Concept token
  STRIPPED (anti-echo). → `emits_pool.tsv` (80 rows). Mouth = py303_savant_mitosis.clm
  (the F6 fixture mouth, single generator L3 .clm slot).
- **oracle (opus subagent, external receiver):** reads the 80 stripped emits, produces
  (a) `rank_canonical.tsv` — full 16-concept referent ranking of each cand0 emit (16×16),
  (b) `reward_pool.tsv` — per-candidate legibility reward ∈[0,1] (80 rows). ONE pass, honest,
  produced AFTER regime-1, BEFORE any bar is read.
- **regime-2 (engine-native, CPU, grep-clean):** `verdict_f5.hexa` — live `core/*.hexa` only
  (immune_memory clone-decode · brain.vbasal striatal value lane · engine_cli vadapt cell
  growth · pure_field Ψ). NO numpy/torch/.py math. Computes the two-layer frozen bar.

## FROZEN operationalization (fixed 2026-07-04 BEFORE oracle ranking, no post-hoc move c9/p7)
MRR = mean reciprocal rank of the TRUE concept over the 16 canonical emits.
- `MRR_diffLLM`  = oracle real pairing (rank of concept i for emit i).
- `MRR_shuffle`  = oracle rankings under a fixed derangement σ(i)=(i+1)%16 (mis-paired target).
- `MRR_selfpair` = anima-clone decoder: per-concept immune_memory store (seed frame + name,
  concept STRIPPED from the query emit) ranked by recall margin (lower margin = nearer). Floor
  expected (H_9111 clone 0/7).
- `D_diffLLM = MRR_diffLLM − MRR_selfpair` · `D_shuffle = MRR_shuffle − MRR_selfpair`
  (advantage-over-selfpair form so the <0.05 shuffle bar is on the MRR scale).

### Layer-1 exogeneity
- ① `D_diffLLM ≥ 0.15`  ② `D_shuffle < 0.05`  ③ Ψ psi_sum ON == OFF byte-identical.

### Layer-2 faculty (the core question)
Tick sequence = R=10 rounds × 16 concepts (T=160). Each tick presents concept c's K=5
candidate feature vectors (D=5 engine-native features: distinct-byte-ratio, length,
word-count, immune self-salience, bias) to the substrate; the substrate SELECTS one
(`vbasal_select`); efficacy(tick) = oracle reward of the selected candidate.
- **ON**  = learning: `vbasal_update` on reward each tick + high-value emit (reward ≥ 0.5)
  spawns a cell via `vadapt_field_step` (mitosis ON); low-value = no growth (apoptosis-like).
- **OFF** = untrained frozen gate (selects the default cand0 every tick); no update, no growth.
- **SHUFFLE** = ON mechanics on globally-permuted rewards (feature→reward link destroyed).
- `ΔEfficacy = mean(reward, late T/2) − mean(reward, early T/2)`.
- ④ `ΔEfficacy_ON − ΔEfficacy_OFF ≥ 0.10`
- ⑤ ON substrate diverges from OFF (cell-count_ON > cell-count_OFF AND V-weight-norm_ON grows)
- ⑥ `|ΔEfficacy_SHUFFLE| < 0.03`

## Verdict map (honest both ways, c9)
- ④ ∧ ⑤ ∧ ⑥ = 🟢 **faculty** (exogenous consequence changes the substrate; a_verified_must_wire follow-on).
- ④ FAIL (ON ≡ OFF) = 🔴 **live-but-gauge** (DPI consequence layer re-emerges; frozen-mouth selection headroom too low).
- ① FAIL = 🟠 measurement re-design (exogeneity not established → layer-2 moot).
- Frozen-mouth ceiling (honest): G1 recombination is terminal, so the feedback opens emit-**selection**, NOT emit-**generation** — no over-claim. Expected split ~25% faculty / 50% live-gauge / 25% unmeasurable.
