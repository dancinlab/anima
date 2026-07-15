# H_9388 — L4 BRIDGE-TRACE: does the flip1 answer read the stem position, or only the slot?

- **group**: g1-interface-addressable-wall
- **date**: 2026-07-16
- **campaign**: RUNTIME-BRIDGE (Fable's #1 designed lever) · L4 path-attribution census (runs FIRST, $0, parallel-independent)
- **tier**: ⏳ **PRE-REGISTERED — frozen-first, data not yet read** · engine-native 303M py · aiden CPU
- **surfaces**: `HYPOTHESES/cards/H_9388_bridge_trace_path_attribution.md` · `HYPOTHESES/HYPOTHESES.jsonl`
- **instrument**: `anima-py evaluate <clm> --bridge-trace <flip1.json> --flip0 <flip0.json> --out <f.json>` (NEW verb-flag · `cli/evaluate.py::bridge_trace_run` · VERSION 0.13.85 · G5 wheel-bump)
- **cost**: $0 (existing c34 ckpts · CPU numpy on aiden · `CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=4`)

## The reframe this converges (settled by Fable — not re-derived here)

The frontier converged to **"the operator does not runtime-look-up the declaration store (TWO-LANE, no bridge)"** (V1 H_9358 🟢 · V5 H_9353 🧱 independently). Fable split the wall in two:

- **W_ctx** — runtime lookup of an IN-CONTEXT declaration (V5 H_9353). Genuinely an architecture wall in attention-free conv (no variable-distance content-addressed retrieval). **NOT this campaign's target.**
- **W_wt** — a weight-stored declaration synthesised by the operator. In flip1 `{s}지 않다 => ` (KO BOUND suffix) the key (stem bytes) is **ALREADY in the operator's receptive field**; the needed circuit (stem→polarity-feature lookup→near-transport→suffix sign-flip) is all conv parts. The wipeout measured so far (held-out flip1 = 0.46–0.56 = chance, H_9327) is **indistinguishable** from "the cache was always cheaper AND no stem-key store was ever built". This census buys that distinction by asking, on the EXISTING checkpoints, **how much of the flip1 answer margin actually depends on the stem position vs the operator (slot) position.**

This is a MEASUREMENT that converges the interpretation of L1's sign regardless of L1's outcome — run it first, independently.

## Method — input-byte GRADED OCCLUSION (not swap-patch)

H_9331's hidden-swap died on a binary-readout scramble floor. This instrument **never touches the trunk**: it replaces a byte SPAN of the *input prompt* with an **equal-byte-length** neutral fill (0x20 space), so the T-window right-alignment (`decode._seed_to_tok`, byte-aligned) is preserved exactly — a 1B-for-3B swap would shift the whole window and confound everything. The contribution of a region = how much the 2AFC margin drops when that region is occluded.

```
margin       = NLL(counterfactual) - NLL(gold)          (>0 ⟺ model prefers the correct answer)
stem_contrib = margin_full - margin(stem occluded)
slot_contrib = margin_full - margin(operator occluded)          # operator morphemes: 지 않다 / not / 안 / 별로 …
ctrl_contrib = margin_full - margin(matched-byte-count neutral head slice occluded)
stem_net     = stem_contrib - ctrl_contrib   (= margin(ctrl occ) - margin(stem occ))
```

`stem_net` is **control-corrected** (probe-defect-census: never read a raw contribution — the matched-length neutral-head occlusion is the paired same-class control). The operator/slot region is defined as every byte between the common template head (`이 영화 `) and the ` => ` boundary that is not the stem — so it captures a BOUND post-stem suffix and a pre-posed adverb alike (verified in the build smoke).

## Pre-registered decision — frozen bars (read BEFORE any data)

**Sequential (early-kill).** The flip0 surface is where the declarative lookup demonstrably works (H_9334 WRITE 12/12), so the flip0 answer is the stem-keyed fact itself → the **POSITIVE-CONTROL GATE**:

- **G-POS (gate)**: flip0 `stem_share > θ (θ=0.5)` AND `mean_stem_net > 0` AND paired sign-flip permutation `p < 0.05` (2000 perms). If FAIL → **the instrument is broken** (the operator's readout is not localised to the stem it demonstrably uses) → **discard, do NOT read flip1** (INVALID-INSTRUMENT, not a wall). Read flip0 first.

Only if G-POS passes, read the **flip1 3-tier** (per-arm / per-split of the c34 manifest):

| tier | what it is | what it means |
|---|---|---|
| **SEEN** (train stems, operator alive) | operator was pre-trained on these | high stem_net ⟹ the alive operator DOES read the stem-keyed store |
| **CPT-written** (swap arm · `swap_c4`) | inverted polarity written via carrier | high stem_net tracking the PLANTED sign ⟹ a weight-lane bridge exists |
| **held-out / nonce** (0 pretrain, 0 CPT) | no store to reach | stem_net ≈ 0 = the honest floor |

**Below-chance / null cell (pre-registered, per prereg-table-must-cover-below-chance):** `mean_stem_net ≤ 0` on flip1 (occluding the stem does NOT hurt the margin, or *helps* it) is a **first-class DISCOVERY**, not "undecidable": it says the flip1 answer is produced **without reading the stem position at all** — the operator answers from the slot/prior alone. That is the strongest possible confirmation of W_wt-as-no-store (the operator never built a stem-key read).

**Verdict reading (both signs terminal-grade):**
- flip1 stem_net **high & significant on SEEN, low on held-out** ⟹ the alive operator reads the stem store but only where pretraining forged it → **W_wt is a forge-at-pretrain fact** (converges S-world of H_9331 · XBIND-becomes-law). Supports L1 phase-B being able to steer only via co-trained gradient.
- flip1 stem_net **≈ 0 everywhere (incl. SEEN) while flip0 dominates** ⟹ even the ALIVE operator answers from the slot, not a stem read → the "operator" is a slot reflex (converges V2's BOUND-slot default-negated bias) → **W_wt terminal, V5-reopen (attention) is the honest end.**
- flip1 stem_net **high on the CPT-written swap arm, tracking the planted sign** ⟹ a weight-lane read of a CPT-written store EXISTS → reframes the whole wall (would be the first positive).

**Power note (power-before-negative-verdict):** n per tier = (#stems × #surfaces). A null tier is reported with its sd + the permutation p; a null is only cemented with TOST-grade equivalence, never a bare non-significant p.

## Scope / hygiene

- **Device-stamped** (GPU-hidden byte-pin lesson): every output carries `device`. This census runs CPU on aiden (stamped CPU); a cross-device comparison is refused. The gate can FAIL (G-POS discards a broken instrument) — the guard is not decorative.
- **KO, not EN** — L4 reuses the EXISTING c34 KO checkpoints (`natem_c34_main_s{7,11}`, `swap_c4_s{7,11}`). EN-first (ⓑ) binds NEW research corpora (L1), not a census of frozen artifacts; and the KO BOUND suffix is exactly the surface where the stem-key would live if it existed (stem bytes adjacent to the operator in-RF). This is the ideal W_wt read surface.
- Read-only w.r.t. weights (production forward · `a_experiment_engine_native`). Ckpts pulled to `~/anima-weights/c34/` (persistent) → transferred to aiden for the run.
- ⚠️ EN-manifold limitation of the slot/head partition (mixed pre-posed operators sharing a byte prefix, e.g. `not`/`never`, leak into the common head) — irrelevant here (KO surfaces), and for EN one operator surface per manifest keeps it clean.

---

## 🟢/⏳ VERDICT — L4 census RAN (data-after · read through the frozen bars above · 2026-07-16)

**measurement**: aiden CPU-numpy (`CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=4` · device-stamped CPU) · engine-native `core/decode.py` full CLMConvMoE forward (`clm._fwd_logits`) → TERMINAL-eligible (`a_eval_py_canonical`) · VERSION 0.13.85 · perm=5000. Manifests reproduced on-host from `gt_atoms.json` via `anima-py corpus ground_carrierswap [--carrier-only]` (flip1 md5 `1e6d27ac` · f0-goldtrue md5 `340b97c4`). ckpts natem_c34_main / swap_c4 (d3784/L4/E2→3 · 44.9M active params). Raw JSON → `~/anima-weights/h9388_bridgetrace/`.

### ① INSTRUMENT VALIDATED on the pretrain lane (G-POS PASS, both seeds)

Positive-control gate = flip0 declarative readout (gold=TRUE polarity, the non-swap arms + held-out reproduction, n=36):

| ckpt | lane | flip0 stem_share | flip0 stem_net | perm_p | G-POS |
|---|---|---|---|---|---|
| natem_c34_main_s7 | pretrain | 0.528 | +4.85 | **0.0002** | ✅ PASS |
| natem_c34_main_s11 | pretrain | 0.510 | +4.91 | **0.0002** | ✅ PASS |
| swap_c4_s7 | CPT-written | 0.196 | +0.12 | 0.9394 | ❌ FAIL |
| swap_c4_s11 | CPT-written | 0.225 | +0.42 | 0.7497 | ❌ FAIL |

The instrument is **valid** (it detects the stem-keyed declarative read where lookup demonstrably works — the pretrain lane, both seeds). The swap_c4 gate FAILS **on the same manifest and the same non-swap stems** — see ③.

### ② 🟢 DECIDABLE (pretrain lane, gate PASS): the ALIVE operator's flip1 answer READS the stem position

| ckpt | flip1 stem_net | slot_contrib | stem_share | perm_p |
|---|---|---|---|---|
| natem_s7 | **+3.50** | +4.09 | 0.461 | **0.0008** |
| natem_s11 | **+4.95** | +3.82 | 0.564 | **0.0014** |

Both seeds: stem_net significantly positive (occluding the stem hurts the flip1 answer), roughly BALANCED with the slot (stem_share ≈ 0.46–0.56). ⟹ **the stem→polarity→operator circuit EXISTS in the attention-free conv and is genuinely consumed** where pretraining forged it. This **refutes the LLM-frame reading** that "attention is needed to route stem content to the operator" (`a_no_llm_frame_trap`) — conv demonstrably does it. Converges the **S-world** of H_9331 (the feature is right there and consumed, where forged).

### ③ 💀 CPT DESTROYS the omitted-stratum stem-read (both seeds) — Correction ② confirmed mechanistically

The identical gold-true flip0 positive control collapses from stem_share **~0.52 (natem) → ~0.21 (swap_c4)** on the SAME non-swap stems (both seeds). The carrier-swap CPT did not build a stem-key store — it **damaged the pretrained stem-keyed declarative read on the stratum the CPT corpus omits** ([[cpt-destroys-what-corpus-omits]] at the mechanistic level). So on the CPT-written lane the gate FAILS ⟹ its flip1 is **INSTRUMENT-INVALID / DIRECTIONAL only** (swap-arm flip1 stem_net +1.68 s7 p=.04 / +2.32 s11 p=.19 — weak, not cemented).

### Convergence (both signs were terminal-grade; this is the informative one)

W_wt's stem→operator circuit is **real and conv-native**, consumed where pretraining forged it — the wall is **not** "conv cannot route stem content" (V5-reopen is **not** forced by this). Single-surface carrier CPT **cannot write** that stem-key read (it writes a surface cache and damages the omitted stratum — Correction ②). ⟹ this **strengthens the L1 rationale** (H_9389): the declaration→operator mapping must receive GRADIENT during training (co-train), because CPT alone damages rather than builds it. The honest next step is **L1 phase A/B, not V5**.

**Frozen-first honored**: the swap_c4 gate FAIL is reported as instrument-invalid-on-that-ckpt (no tune-to-green); only the gate-PASS pretrain lane is cemented. Power: n=24 flip1 / n=36 flip0 per seed, permutation p reported inline.
