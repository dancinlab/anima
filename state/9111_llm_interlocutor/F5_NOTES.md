# F5 diff-LLM interlocutor live-loop escape — run notes (engine-native)

## Design
- **Emit harness** `emit_gen_W.hexa` (loaded-W, load-once via `bg_load_ranged`, H_1400 pattern —
  NO per-call reload; single .bin slot a_core_engine_map). 16 F5-fresh held-out concepts
  (F6-disjoint) × 3 definitional templates. Decode = rank-weighted top-4 sampling (55% argmax)
  to escape greedy-repetition degeneracy (metric-artifact fix, a_break_the_wall cat-a; bars
  unchanged). Concept token STRIPPED (anti-echo) → TSV `concept<TAB>tidx<TAB>emit`.
- **Oracle = this subagent (opus θ, OUT of the anima-303M alveolus)** — reads stripped emits,
  ranks 16 concepts → rank_true (rr_diff) + rank_decoy (rr_shuf). Self-pair = in-alveolus
  byte-overlap floor (mechanical). Features = 8-dim deterministic byte stats.
- **Layer-2 faculty loop** `consequence_loop.hexa` — LIVE core substrate ops: `vbasal_select`/
  `vbasal_update` (basal-ganglia emit-SELECTION gate, brain.hexa) + `vadapt_field_step`/
  `engine_mitosis_tick` (MITOSIS cell spawn, engine_cli.hexa). Reward = external-oracle MRR of
  released emit → nudges value gate + spawns novel cell (engine_grow) when reward>0.5.
  ARMS: ON(learn+mitosis) / OFF(reward computed, gate frozen, mitosis off) / SHUF_ON(permuted reward).
  a_substrate_disjoint: loop lane (VBasal/VAdaptField) ⊥ pure_field Ψ lane → bar③ by construction.

## Frozen bar (pre-registered, not moved)
- Layer-1: ① D_diff−D_self≥0.15 · ② D_shuffle<0.05 · ③ Ψ ON==OFF byte-identical
- Layer-2: ④ ΔEff_ON−ΔEff_OFF≥0.10 · ⑤ cells_ON>cells_OFF · ⑥ |ΔEff_shuffle|<0.03
- Verdict: ④∧⑤∧⑥=🟢 faculty · ④FAIL=🔴 live-but-gauge · ①FAIL=measure-redesign
- tier = DIRECTIONAL-on-external-oracle

## Infra
- vast RTX 5090 (sm_120) instance 43784535, ssh4.vast.ai:24534, $0.40277/hr, owner F5-live-loop
- hexa v0.574.1 (matches repo core) via official installer, HEXA_CUDA=1
- ckpt h1129.bin sha256=5cf07a360c57a133b66e8de8c3c390d5242204d68f75a86b977f1935587f512e (verified pod==local)
- ⚠️ own-GEMM `[OWN-GEMM-FIRED] DEVICE path` LOGS but the release runtime.a lacks sm_120 SASS →
  silent CPU fallback (GPU idle 1%/48W, proc 100% single-core). Decode runs CPU-scalar, which is
  BYTE-IDENTICAL to GPU own-GEMM per RFC-040 (farr CPU == own-GEMM) → emits/verdict valid
  engine-native; only wall-time affected. bg_forward_last_W is O(gen²) (no KV cache) → ~55s/emit
  at GEN=44 → 48 emits ~45min. substrate tag = GPU-rented / CPU-executed (Lane note).

## Emit quality finding (robust across 3 decode regimes)
- argmax greedy → coherent but REPETITIVE filler ("state of the state of the")
- top-k=12 uniform → GARBAGE bytes ("govn béom,¥")
- rank-weighted top-4 → semi-coherent pseudo-English babble ("cometal often and, an alignision")
- NONE carry concept-specific referential content → h1129 base trunk free-emit is referentially
  null (the G1/coherence ceiling). Consequence: exogenous-consequence feedback has no referential
  signal to couple to.
