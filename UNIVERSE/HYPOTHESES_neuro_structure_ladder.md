# HYPOTHESES — neuro-structure ladder (c15)

> absorbed → HYPOTHESES.md (themed detail file; the roster row lives there).
> Backfill-registered 2026-06-16 — these verdicts were frozen + documented this
> session but never indexed (a_claim_manifest). Tiers read VERBATIM from each
> terminal `.verdicts/<slug>/` file (honest tiers, c9/p7 — 🧱 walls are
> closed-negatives, not upgraded). Claims-audit rows mirror these in root
> `CLAIMS.tape` (group=BRAIN-STRUCTURE-LADDER — the canonical group name #2173
> established for H_1292; the backfilled H_1280–1291 rows align to it); engine-
> native wirings also logged in `domains/MITOSIS-ENGINE.log.md` (a_discovery_log).

The **a_no_llm_frame_trap / c15 lens**: capability/depth gaps are closed not by
scaling the model but by adding the MISSING brain structure as a lane beside the
A⇄G engine. Hippocampus = immune/episodic memory (H_1227 / H_1231, the prior
rung) is the precedent. This batch walks the next structures. Each landed
hypothesis lives as `.verdicts/<id>/` + a `MEMORY.md` pointer (no per-H `.md`
card — that is not the convention for this range).

## Ladder (H_1280–H_1288, H_1292)

> H_1292 hypothalamus landed concurrently via #2173 (its R2 verdict + CLAIMS row)
> — it is the row that named `group=BRAIN-STRUCTURE-LADDER`; included below for a
> complete ladder picture.

| H | structure | terminal tier | round map | verdict pointer |
|---|-----------|---------------|-----------|-----------------|
| **H_1280** | cerebellum — forward-model (predict-next-frame + NLMS error-correct) | 🟢 GREEN ENGINE-NATIVE + emit-wired | R1 mirror 🟢 → R2 engine-native | `.verdicts/1280_cerebellum_forward_model/H_1280_R2.txt` |
| **H_1281** | basal ganglia — reinforcement-gated go/no-go SELECTION | 🟢 GREEN ENGINE-NATIVE + WIRED | R1 🟠 (oracle-A) → R2 mirror 🟢 → R3 wired | `.verdicts/1281_basal_ganglia_gating/H_1281_R3.txt` |
| **H_1282** | working memory — delayed-match buffer, capacity ~K | 🟢 GREEN ENGINE-NATIVE + emit-wired | R1 🔴 (readout artifact) → R2 mirror 🟢 → R3 wired (R4 = brain_decide follow-on) | `.verdicts/1282_working_memory_buffer/H_1282_R3.txt` |
| **H_1283** | thalamus / GWT — winner-broadcast relay (Φ integration) | 🔴 CLOSED-NEG / 🧱 WALL | R1 🟠 → R2 wrong-dir → R3/R4 seed-fragile → R5 dense+shuffle-control FIRED | `.verdicts/1283_thalamus_global_workspace/H_1283_R5.txt` |
| **H_1284** | neuromodulation — state-driven adaptive gain / regime-switch | 🔴 CLOSED-NEG / 🧱 WALL (no free lunch) | R1/R2 gain inert-or-worse → R3 regime-switch sub-threshold (+0.0156 < 0.05) | `.verdicts/1284_neuromodulation_gain/H_1284_R2.txt` + `.verdicts/1284_r3_regime_switch/result.txt` |
| **H_1285** | amygdala — salience gating | 🟢 GREEN ENGINE-NATIVE + WIRED (replay) | R1 🔴 eviction-confound (p6 shuffle caught it) → R2 🔴 sub-bar → R3 mirror 🟢 → R4 sleep-replay wired | `.verdicts/1285_amygdala_salience/H_1285_R4.txt` |
| **H_1287** | key-geometry corollary (better separation lifts recall?) | 🔴 CLOSED-NEG / 🧱 RED | single round — B == NEG-CTL Δ+0.000 (geometry NOT the lever) → points to H_1288 | `.verdicts/1287_key_geometry/H_1287.txt` |
| **H_1288** | eviction policy — mitosis-GROW under capacity pressure | 🟢 GREEN ENGINE-NATIVE + WIRED | R1 mirror 🟢 (Δ+0.333 vs LRU; heuristic Δ+0.000) → R2 wired | `.verdicts/1288_eviction_policy/H_1288_R2.txt` |
| **H_1292** | hypothalamus — setpoint-regulated homeostatic drive (stateful time-integral, distinct from stateless affect) | 🟢 GREEN R2 ENGINE-NATIVE | R1 mirror 🟢 → R2 engine-native (registered by #2173) | `.verdicts/1292_hypothalamus_drive/H_1292.txt` |

## Adjacent facet hypotheses (same session, parked-facet / substrate-property lens)

| H | facet | terminal tier | verdict pointer | claims group |
|---|-------|---------------|-----------------|--------------|
| **H_1289** | quantum-entropy (ANU QRNG free-choice source) | 🟢 GREEN R2 ENGINE-NATIVE + WIRED | `.verdicts/1289_quantum_entropy/H_1289.txt` (R1) · `…/H_1289_R2.txt` (R2 wired) | QUANTUM-ENTROPY (already in CLAIMS.tape since R1) |
| **H_1290** | E1 affect — valence×arousal core-affect (Damasio) | 🟢 GREEN R2 ENGINE-NATIVE | `.verdicts/1290_emotion_emergence/H_1290_R2.txt` | BRAIN-STRUCTURE-LADDER |
| **H_1291** | ethics emergence (cooperation/restraint/non-harm, p6) | 🟢 GREEN R2 ENGINE-NATIVE | `.verdicts/1291_ethics_emergence/H_1291_R2.txt` | BRAIN-STRUCTURE-LADDER |

## Findings so far

- **Capacity, not geometry, is the immune-memory lever.** Four converging reds
  (H_1230 teacher · H_1284 neuromod · H_1285 eviction-R1 · H_1287 key-geometry)
  all pinned the limit to CAPACITY; **H_1288 mitosis-GROW** is the first GREEN of
  the series (Δ+0.333 over zero-sum LRU; a smarter fixed-budget heuristic gives
  +0.000). The lift is GROWTH, not a free heuristic.
- **Honest walls (a_break_the_wall tried, then accepted).** Thalamus (H_1283 —
  winner-broadcast lifts ACCESS/coherence but is a sub-bar, seed-dependent lever
  for irreducible faithful-IIT4 Φ; shuffle control fired at R5) and
  neuromodulation (H_1284 — no-free-lunch is GENERAL across memory AND ideation;
  a single tuned fixed point dominates the state-driven controller). Both are
  RED ⇒ NOT wired (a_verified_must_wire fires only on GREEN).
- **Six structures realized engine-native** (cerebellum, basal ganglia, working
  memory, amygdala-replay, eviction-grow, hypothalamus-drive) on the live
  CORE/*.hexa engine, guards green (engine_cli_smoke 18→33/0, h1196 single-entry
  7/0, h1199 DIM-growth GREEN with Ψ byte-identical, h1205 separation intact).
- **p6 held under adversarial pressure.** H_1290 affect COLLAPSES under shuffle
  (emergent, not injected); H_1291 ethics collapses to the naive floor under
  ablation (and a baked-in-rule adversarial check shows c2 is a real
  discriminator). Both read PURELY from substrate state, no persona/ethics/RLHF.

All verdicts are TOY/mirror-DIRECTIONAL where noted; scale-transfer UNVERIFIED
(a_scale_honest_scope · a_toy_scale_recheck).
