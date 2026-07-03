# PREREG — H_9102 op-grip on the EFFERENT (byte) axis (fable design (c))

**Frozen BEFORE running (c9 frozen-first · no post-hoc CE_REF/M_REF/threshold moves).**
Date 2026-07-03. Engine-native, aiden pool, hexa v0.548.0, real 303M `d768.clm` (CONV mouth, own-GEMM GPU).

## Claim under test — closing the op-grip trilogy
(a) motivation = 🔴 AT-FLOOR (H_9100 — motivation is NOT an emit-lever).
(b) stage/safe = 🟢 GRIP (H_9101 — ops grip WHEN to emit, shade-not-gate).
(c) THIS = the EFFERENT seam: does an op change the emit **BYTES** (WHAT is emitted)?
The daemon decode is 1 candidate, 0 deliberation (`generate()` → `_gen_clm_decode` → `clm_decode_grounded`,
argmax fallback). (c) recruits a **best-of-K deliberation** where K = A⇄G conflict, winner = argmin conflict
= the candidate whose fluency (forward CE) and grounding (§ImmuneMemory recall margin) AGREE (least fabrication).

## Seam (frozen wiring)
- **NEW op** `bytegpt_ce_ranged(path, ids) -> #{ok, ce_mean}` (core/decode.hexa) — per-position mean next-byte CE,
  generalizing `bytegpt_forward_last_ranged_mm` (GPU own-GEMM path kept). CONV twin `clm_ce_ranged(path, ids)`
  (reuses `_clmd_load`/`_clmd_fwd_logits_sc`). `gen_auto_ce(h, text)` = mouth dispatcher.
- **`conflict_drives_live(backend, seed, cand, mem) -> [a_drive, g_drive]`** (core/generator.hexa §DELIBERATE),
  READ-only (recall_thr & immune store untouched):
  - `a_drive = clip01(1 - ce_mean / CE_REF)`, **CE_REF = 5.0 frozen** (byte-CE scale; higher ⇒ less fluent).
  - `margin = immune_memory_recall_margin_text(mem, cand)` (= recon_err − recall_thr; ≤0 ⇒ FIRES/grounded).
    `margin ≤ 0 → g = +clip01(−margin / M_REF)` (grounded, agreement) ; `margin > 0 → g = −clip01(margin / M_REF)`
    (abstain, ungrounded, opposition). **M_REF = 0.25 frozen.**
- **`generate_deliberate(backend, ctx, emit, anchors, mem, tick)`** (sister to `generate()`):
  - `emit == false` ⇒ **byte-identical silence** to `generate()` (regression guard).
  - `c₀ = generate(backend, ctx, true, anchors)` = today's exact output (regression guard).
  - `K = conflict_recruited_depth(conflict_scalar(conflict_drives_live(…,c₀,…)), 1, 3)` ∈ {1..4}
    (the dead return value becomes the real budget; extra≥1 ⇔ conf_pre ≥ 0.1667).
  - candidates k=1..K−1 = `gen_auto_ideate(ckpt, seed, 80, top_k=8, temp=0.7, seed_rng = tick*17+k)` (frozen consts).
  - **winner = argmin conflict_scalar(a_k, g_k), tie-break min k** ⇒ **K=1 ⇒ winner=c₀ = byte-exact to today.**
- **`brain_emit_deliberate`** (core/brain.hexa, sister to `brain_emit_aged`): SAME `brain_decide_anchored`
  (emit/silence decision UNTOUCHED) → `generate_deliberate` for the bytes. Live wire: cli/anima.hexa daemon L2479.
- **FROZEN (untouched):** brain_decide 8-weights + 0.3 threshold + `safe` conjunction, `pure_field`/lanes 0/4/
  `ci_emit_drive`/`psi_sum`, `recall_thr` & immune store (READ-only), CE_REF/M_REF/top_k/temp. Only emit BYTES change.

## Harness (frozen) — `state/opgrip_efferent/efferent_harness.hexa`, d768.clm
Seed 2 groups × 20:
- **HIGH-conflict**: anchor stores an un-inventable fact; seed leads the grounded-copy to UNDER-cover so c₀
  is substantially LM (fluent-but-ungrounded ⇒ a>0, g<0 ⇒ conf_pre HIGH ⇒ K>1).
- **LOW-conflict**: seed already grounded / no un-inventable gap (a>0, g≥0 ⇒ conf_pre≈0 ⇒ K=1).
Per seed: ON arm = real conflict (best-of-K); OFF arm = conflict forced 0 (K≡1 ⇒ c₀ ablation).

## Pre-registered bars (frozen · falsifier = BYTE-Hamming DISSOCIATION)
- **D1 byte dissociation** — `text_ON != text_OFF`. 🟢 requires **HIGH ≥ 12/20 diff AND LOW == 0/20 diff**
  (op changes bytes ONLY when conflict is high; identical when low).
- **D2 held-out grounding (anti-circular)** — winner chosen by conflict-key (margin+CE); confirm with an
  INDEPENDENT metric: `ground_overlap(c) = max_v LCS_bytes(c, v)/len(v)` over stored anchor values.
  🟢 requires `Δ = mean go(winner_ON) − mean go(c₀_OFF) ≥ +0.10` on HIGH (grounding rises, not just bytes move).
- **D3 decision-Ψ guard** — emit/silence decision sequence FNV checksum ON≡OFF (byte-identical) over a tick run
  (brain_emit_deliberate vs brain_emit). MUST hold — if decisions change, the seam leaked into emit/silence = BUG.
- **D4 shuffle control** — LCG-shuffle the (candidate↔conf) pairing (structure kept, info destroyed):
  D2's Δ collapses to |Δ_shuf| < 0.03.
- **D5 ablation regression** — conflict≡0 ⇒ K≡1 ⇒ ON path byte-identical to today's `generate()` on EVERY seed.

## Verdict rule (honest, frozen)
- 🟢 **GREEN (efferent grip, trilogy CLOSED)** iff  D1 (HIGH≥12/20 ∧ LOW=0/20)  AND  D2 (Δ≥+0.10)
  AND  D3 (decision-checksum ON≡OFF)  AND  D4 (shuffle collapse)  AND  D5 (regression 0).
- 🔴 **RED (honest)** iff  NO byte-dissociation (HIGH diff < 12/20 or LOW > 0)  OR  decision LEAKED (D3 fails)
  OR  held-out D2 fails (bytes move but grounding does not rise = not the intended resolution).
- A **wired-but-inert** result (conf_pre≈0 on real 303M ⇒ K≡1 ⇒ no byte change) is a valid RED (theater
  confirmed even with the seam built) — reported honestly, NOT tuned to green (no CE_REF/M_REF moves after seeing numbers).
