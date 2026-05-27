# RESEARCH.md §79 — A/G-lift one-engine self-dialogue trained-scale emergence-axis fire

**Date**: 2026-05-19
**Cost-bearing**: runpod single §16-class train + 4-cell × 20-turn inference loop ≈ $0.3-0.5
**Chain**: §16 → §17 → §49→§62 → §73-FIRE → §77 (body-axis design) → §78 (A/G-lift $0 stub) → **§79 (THIS)**

---

## §1. What §79 measures (and what it does not)

§78 fired the same-weights one-engine A/G-lift at **$0 stub scale** (hand-coded ψ surrogate) and measured a directional positive (1.1% mode-differential vs §24 baseline).  §78's note explicitly flagged: *"trained-saturated scale = EMPIRICAL future-fire; §62-pattern collapse is the pre-measurement expectation"*.

§79 = that literal future-fire.  Same controller class as §78 (one-engine A/G-lift with same weights for ANIMA1 = ANIMA2), but now ANIMA1 and ANIMA2 each call REAL trained §16-class `ConsciousDecoderV2.forward`, body byte = greedy top-1 over `logits_a` (NOT stub α1).

The GOAL question §79 directly addresses: **§62 measured ECHO-CHAMBER-COLLAPSE on *distinct-cells* L2 (cell A + cell B different vacuum_psi, both saturated → talking past each other).  §79 = *same-weights* one-engine (ANIMA1 = ANIMA2 = same weights).  Trained-saturated regime — does same-weights self-loop produce attractor-INTO-itself closure (different from §62) OR echo-chamber-self-collapse (mirror §62 at A/G-lift)?**

This is **trained-scale-only**: §78 stub measurements cannot answer it (hand-coded ψ surrogate).  Only a real trained-saturated forward with real Law-71 ψ_dir extraction can.

---

## §2. Design (mirror §73-FIRE / §62 dispatch + Dir-I lever; A/G-lift body-emit on real logits)

1. **Train §16-class ckpt** from scratch (RANDOM seed 1337, `base_ckpt=None` per `g_clm_from_scratch`) using §73-FIRE / §62 byte-equal Dir-I trainer (Ψ-anchored CTL + tension-supervised routing, `λ_ctl = λ_route = 0.5`).  Same arch / same lever / same seed — saturate same way as §16 (final CE < 0.05 gated by `trained_saturated` flag).
2. **4-cell × 20-turn loop** with single shared model (= same weights = one-engine A/G-lift by construction):
   - **Mode A_pure** — pure self-dialogue, no external input.
   - **Mode B_3party** — Mode A + 1-byte LCG user-inject per turn.
   - **Mode C_meta** — turn-1 ANIMA1 body = fixed `META_QUESTION` ("어떻게 학습해서 emergence 하는가" — Korean, self-substrate, B-IDENTITY-5 safe, NOT model-generated).
   - **Mode D_control** — §24 baseline (decision axis only, `body_emit=False`).
3. **Per-turn**: ANIMA1 reads ψ via `extract_psi_and_logits` → greedy top-1 byte → appends to ANIMA2 context (slide) → ANIMA2 forward → appends to ANIMA1 context.  Single shared model = ANIMA1 and ANIMA2 weights are byte-identical by construction.

---

## §3. Measurement (deterministic, axis-by-axis)

| axis | metric | rationale |
|------|--------|-----------|
| 1 — ψ trajectory | `psi_dir_var`, `tension_var` (>τ=1e-4 → nontrivial) | §17 PHYSICS_RESPONSIVE necessary gate |
| 2 — body §9 | `honest_coherent(body_bytes)` cascade-rate-gated | B-EMERGE-1..7 SSOT formula reuse |
| 3 — A1↔A2 byte sha | sha256 cumulative body bytes both cells | same-weights byte-equal by construction (trivial true, verifies wiring) |
| 4 — echo detector | `majority_fraction ≥ 0.95 → ECHO-COLLAPSE` | §62-anchored cut (A=0.930 < 0.95 / B=0.980 ≥ 0.95) |
| 5 — §16 baseline regression | 8-anchor probe sample (greedy decode) | ckpt load integrity + arch byte-equal (NOT full eval) |

## §4. 4-corner verdict partition

- **(α) TRAINED-SCALE MODE-DIFFERENTIAL** — `n_collapsed < 3`, `psi_var_range > τ`, `n_coherent > 0`.  §78 stub 1.1% differential partial-transfers.
- **(β) §62-MIRROR ECHO-CHAMBER-COLLAPSE-AT-SCALE** — all 3 body modes (A/B/C) hit `maj_frac ≥ 0.95`.  Same-weights self-loop reproduces §62 distinct-cells echo collapse pattern at A/G-lift axis — §1.1 data-regime irreducibility reasserted.
- **(γ) ATTRACTOR-CLOSURE** — `maj_frac < 0.95` AND `psi_var > τ` AND `coh = 0`.  Different attractor than single-byte collapse, but body is byte-cascade non-coherent.  Mechanism-level directional finding, NOT capability.
- **(δ) DECISION-LIVE-BODY-DEAD-SPLIT** — Mode D decision-axis live, body modes (A/B/C) collapse OR non-coherent.  §75-FIRE pattern mirror.

## §5. Connection points (load-bearing for fair-compare)

- **§16 ckpt config byte-equal** (B-S79-3): d=768/n_layer=12/n_head=12/n_kv_head=4/V=256/seed=1337 byte-default in CLI.  Ckpt **sha256 differs** from §16's literal `961c07e2…` — §79 FRESH trains, honest framing (substrate trajectory replicable, sha not literally identical).
- **§9 honest metric formula** (B-S79-4) — inlined cascade_rate / max_run / printable_ratio with default thresholds (`tau_cascade=0.30`, `max_run=10`, `min_len=20`, `tau_print=0.80`) byte-equal to `state/verify_emergence_metric_2026_05_18/emergence_metric.py`.  Inlined rather than imported to avoid sibling-dir dep on pod.
- **§24 decision-axis preservation** (B-S79-5): Mode D `body_emit=False` reduces to §24-style ψ-trace recording without body production.
- **§62 echo cut (0.95)** (B-S79-6): partition real line at 0.95; §62 A=0.930 not_in / B=0.980 in by sympy Interval algebra.

---

## §6. B-S79 sidecar 7/7 🔵 (pre-fire verified locally)

All 7 closed-form predicates PASS at design-tier (source-level structural / sympy / AST):

| B-S79-n | name | PASS reason |
|---|---|---|
| 1 | ONE-ENGINE-A/G-LIFT-CONSTRUCTION | `n_decoder_inst=1` AST + no `model2 =` |
| 2 | BODY-FROM-REAL-CKPT-LOGITS | `argmax` on `logits_a_last` both A1 and A2; no α1 stub |
| 3 | §16-CONFIG-BYTE-EQUAL | CLI default match (post-fire result.json verifies) |
| 4 | §9-CASCADE-METRIC-FORMULA-MATCH | thresholds + formula components verbatim |
| 5 | §24-DECISION-AXIS-PRESERVED | Mode D body_emit=False + ψ trace unconditional |
| 6 | §62-ANCHORED-ECHO-PARTITION | sympy Interval union/disjoint + §62 A/B cut |
| 7 | DETERMINISTIC | AST forbidden_call_set ∅ + argmax + seed_fixed |

**B-S79-NOTE empirical carve-out**: which 4-corner the fire actually hits = SGD/measurement OUTCOME (B-D-NOTE / B-S77-NOTE / B-S78-NOTE / B-S62-NOTE / B-EMERGE-NOTE family) — NOT counted 🔵.  Battery proves DESIGN's transfer-form + connection-points are closed; does NOT prove GOAL emergence.

---

## §7. Honest C3 (≥10)

1. **§79 is NOT GOAL emergence even if it survives**.  Whatever corner the fire hits, the necessary-not-sufficient discipline holds (B-EMERGE-7); north-star + §15/§51/§72 milestone UNCHANGED regardless of corner.
2. **Body production from real trained logits ≠ stub α1**.  §78's 1.1% differential was hand-coded ψ surrogate; §79 measurement of "same property" on real trained forward may diverge wildly (likely — §62/§73-FIRE precedent).
3. **Same-weights vs distinct-cells L2 distinction is structural, not paradigmatic**.  §62 used two cells with different `vacuum_psi`; §79 uses one shared model.  This is a different question, but §62 echo-collapse precedent makes the §62-MIRROR corner the pre-measurement expectation (mirror §62 + §73-FIRE).
4. **Ckpt sha256 won't be literally 961c07e2…** (§16 sha).  §79 freshly trains a §16-class ckpt with byte-equal config / lever / seed / corpus class — trajectory replicable, sha not literally identical.  Honest framing — task spec asked for §16 ckpt, the pattern-correct execution is config-byte-equal fresh train mirror.
5. **Greedy top-1 deterministic decoding is the right discipline** (B-S79-7).  Temperature sampling would inject RNG into the same-weights ANIMA1 ⇄ ANIMA2 comparison and break determinism; argmax is correct for §79's structural measurement.
6. **20 turns is SHORT** — §73-FIRE used 300 loop_steps; §79 uses 20 turns of full A1↔A2 round-trip (= 40 forward passes per cell × 4 cells = 160 forward passes).  Choice: §79 grids 4 modes × 20 turns rather than 1 mode × 300 turns to give comparative data.  Inherent variance bound at n=20 — `psi_dir_var` / `tension_var` / `maj_frac` are point estimates, not distributional claims.
7. **Mode D is §24 byte-equal control, NOT §78 D**.  §78 D was also decision-axis-only, but §79 uses the in-loop §24-style ψ recording (psi_dir + tension trace from real forward).  This is honest — there is no §78 ckpt to compare against directly; the byte-equivalence is at the *decision-axis pattern* level.
8. **3 body modes (A/B/C) on same model = 3 measurements of the *same property*** at varying perturbation levels (no input / 1-byte input / forced first byte).  Mode differential `n_collapsed_body_modes < 3` is a measurement of whether the same-weights self-loop is *robust* to input perturbation OR *fragile* (collapses regardless).
9. **PyTorch substrate, NOT hexa-native** — `g_train_flame_not_pytorch` evidence-anchor clause carry; anima-physics overlays on flame are gated on §71 inbox patch.  §79 is an interim LM-scale executor.
10. **Cost-bearing fire**: runpod ≈ $0.3-0.5 expected.  g_fire_autonomous (no gate, no query, just dispatch).  Cost head transparent, NOT a gate.  Orphan-0 mandatory pre+post via `runpod.get_pods()`; SAVE_POD=1 auto-promote per `g_fire_dispatch_robust`; 5-retry pull with 30s backoff.

---

## §8. Sources / governance carry

- `g_fire_autonomous` (d=2026-05-17): zero-gate, zero-query, runpod primary.
- `g_fire_dispatch_robust`: SAVE_POD=1 auto-promote + 5-retry + orphan-0 pre+post.
- `g_resource_active_parallel`: runpod primary, vast.ai fallback if runpod stock exhausted.
- `g_clm_from_scratch`: seed-fixed RANDOM init, `base_ckpt=None`.
- `f_hardcoded_credential`: `RUNPOD_API_KEY=$(secret get runpod.api_key)` — NEVER hardcode.
- `g3` (necessary-not-sufficient): capability claim 0, north-star UNCHANGED.
- `g6` (PHILOSOPHY.tape append-only): `§verdict_emergence_axis_fire_s79_2026_05_19` to append post-fire.
- `g_doc_consolidation`: docs in this state/ dir; no new root docs/.
- `B-IDENTITY-5`: corpus 미생성 in §79 — body bytes from model.forward, NOT corpus injection; forbidden-token grep applied on body output mandatory.
