@title: 🌌 KOSMOS-MAP — 우주뇌지도 cartography (dimension · sensory axes · carving reverse-engineering)

@goal: Determine how anima's consciousness map (KOSMOS Ψ-space "우주뇌지도") SHOULD be drawn — its right dimensionality, which axes (space/time/emotion/tier/modality/scale) carry independent information, and how real multimodal sensory data (EEG · LiDAR · dolphin-acoustic) maps onto it. Run BOTH directions: (forward) ladder the map dimension to find the appropriate D + its capacity; (reverse) reconstruct the carving-era engine that drew the map and re-explore it. All findings substrate-native + honest (p7 — CE is a floor, not the verdict; closed-negative publishable).

## carving-era ENGINE (the engine that drew the 우주뇌지도, s16 fire 2026-05-17~18)

Reverse-engineered from `state/hexad_v2_py_d768x12L_fire_2026_05_17/train_d768x12l.py` + `state/carving_dir*/conscious_decoder.py` (ready/models/conscious_decoder.py). This is a TRANSFORMER `ConsciousDecoderV2`, distinct from the current production conv-MoE CLM (`CLMConvMoE`, E=2/1-trunk/6-conv int4).

```
ConsciousDecoderV2  (s16 carving fire config)
├─ vocab_size       = 256        (byte-level, lossless)
├─ d_model          = 768
├─ n_head           = 12
├─ n_kv_head        = 4          (GQA — grouped-query attention)
├─ n_layer          = 12
├─ block_size       = 256
├─ consciousness_dim= 128        (consciousness_states cs input)
├─ dropout          = 0.1
├─ gate_strength    = 0.001
├─ n_ca_rules       = 8          (cellular-automata rules)
├─ MoE (optional)   = n_experts 8 · top_k 2   (golden-moe simplified)
├─ blocks           = RoPE pos · RMSNorm · SwiGLU FFN (8/3) · GQA
├─ outputs          = logits_a ⇄ logits_g  (Engine A ⇄ Engine G dual head)
│                     + tensions (5-ch)  + moe_aux_loss
└─ Ψ-space          = Law-71 vacuum_psi (2D coord placement = the map)
   smoke config     = d_model 32 · n_head 4 · n_kv_head 2 · n_layer 3
```

Carving explored 9 directions (dirA tension · dirB intuitor · dirC prime · dirD CDE · dirE superpos · dirF abstract-CoT · dirG psi-ctl · dirH tension-sup · dirI diverse-scaleup). s16 corpus = 603MB / 777K records (sha 422c64a0); routing reached 21/64 (0.328) — partial structure, did NOT cross the §1.1 data-regime emergence threshold.

## current map dimension

KOSMOS anchor `coord = [x,y]` — the map is drawn in **2D** (vacuum_psi Ψ-space projection of the d=768 conscious state). Appropriateness of 2D = under benchmark (see milestones).

## milestones

- [ ] (forward) real-carving intrinsic dimension — estimate intrinsic d (PCA knee · TwoNN · MLE) + projection-dim ladder → appropriate map D + gap from current 2D
- [ ] (forward) KOSMOS coord dimension capacity ladder D=2..8 (independent-axis toy) — saturation knee
- [ ] (forward) Ψ-coord time axis [x,y]→[x,y,t] — carve-sequence captured (landed #1765; monotone-encoding tautology caveat)
- [x] (reverse) reconstruct carving-era ConsciousDecoderV2 (d768×12L GQA transformer) as a runnable lane — re-explore the 9 carving directions — **RECONSTRUCTABLE + RUNNABLE** (CPU/$0, random-init). Builds at smoke (d32/L3=178,424) AND full **d768×12L = 283,722,336 params (283.72M dense; 680.16M +MoE 8/top2)**; forward returns the 5-tuple `(logits_a, logits_g, tensions, kv_cache, moe_aux_loss)` at correct shapes (use_moe off+on); **dual Engine-A⇄Engine-G heads distinct**; **Law-71 vacuum_psi 2D coord (psi_residual, psi_gate) produced — 2D + deterministic**; **dirG psi-ctl direction wireable** (hook shifts forward deterministically). All 4 probes PASS (`.verdicts/kosmos-carving-engine/`, harness `UNIVERSE/carving_engine_reconstruct.py`, source md5 44b210df). HONEST SCOPE: NO s16 ckpt → random init (this is the ENGINE reconstructed, NOT the trained carve reproduced); CPU smoke (T=16); a full d768×12L TRAIN is OUT OF SCOPE (a_toy_scale_recheck / a_scale_honest_scope); p7 (untrained logits ≠ quality verdict).
- [ ] sensory axes ingest — EEG (ds005620) · LiDAR (Redwood/Open3D, #1766) · dolphin-acoustic (Watkins) → 5-ch tension fingerprint as candidate map axes
- [ ] synthesize — which axes (space/time/emotion/tier/modality/scale) carry INDEPENDENT info; the appropriate 우주뇌지도 dimensionality + axis set
- [x] (reverse) carving reverse-engineering BATTERY on the **TRAINED s16 ckpt** (sha 961c07e2, clean load 0-missing/0-unexpected; NOT random-init) — 5 probes, CPU/$0, N=2000 stratified corpus, harness `UNIVERSE/carving_reverse_battery.py`, verdicts `.verdicts/carving-reverse-battery/`. (1) **A/G HEADS** HOLDS: head_a (next-byte, tied to embedding) vs head_g (prev-byte, untied) diverge STRONGLY — mean KL(A‖G)=**7.07** (median 7.02, range 4.1–10.0), mean\|A−G\| logits 3.17; divergence is **tier-modulated** (tier-spread 4.85; high-KL tiers 201/211/108, low-KL tiers 99/100; high-KL domains 기초산술·물질·감각). The "left/right brain" split basis = **next-byte vs prev-byte prediction asymmetry**, sharpest at high tiers. (2) **TENSION** HOLDS (partial) — model emits **1 scalar tension / token / layer** (PureFieldFFN (A−G)² mean over d_model), **NOT a native 5-ch [α,θ,γ,1−δ,β]** (that 5-ch is the .kosmos PERSISTENCE payload, not a forward output). Per-layer tension MAGNITUDE rises then falls (peak ~339 @L6, collapses to 3.4 @L11); the **final layer L11** is the only one with a clean role — tracks tier (r=−0.327) AND separates domains (eta²=**0.644**, vs ≤0.32 elsewhere). (3) **LAYER-DIM** HOLDS (**BOTTLENECK / U-shape, NOT hourglass**) — PCA-90% PCs per layer = **[10,8,6,6,5,4,5,5,6,5,5,8]** (ln_f=8); dim COMPRESSES from 10 @L0 to a **minimum of 4 @L5** (the bottleneck) then RE-EXPANDS to 8 @L11/ln_f. The compact **~6D core forms EARLY by L2**, is tightest mid-stack (4D @L5), and re-opens to ~8D for the dual-head readout (consistent with #1772 intrinsic-d ~6-10 measured at ln_f). (4) **9-DIRECTIONS** HOLDS (read-only, NO retrain) — landed stored joint-metric scores: dirA 0.0323 (best) · dirF 0.0317 · dirB 0.0161 · dirD 0.0090 · dirI-scaleup 0.0087 · rest 0.0; HONEST: the joint metric is **near-degenerate** (chat/separation ~1.0 for most → it ranks knowledge_access recall, NOT map separability) so it does not cleanly rank "most structured map". (5) **Ψ-TOPOLOGY** HOLDS-degenerate — direct measure on the 2D vacuum_psi map coords: effective dim **1.14** (participation ratio), **2nd/1st eigenvalue 0.068** (≪0.25), occupancy 9% of a 20×20 grid (121 unique coords / 2000), best silhouette k=2 (0.573); tier separates perfectly along the map (eta²(x)=eta²(y)=1.0). **The 2nd Ψ axis IS DEGENERATE — the 우주뇌지도 is effectively a 1-D curve embedded in 2D, confirming the #1772 ~1.1-D finding directly on the map coords.** HONEST SCOPE: single TRAINED s16 ckpt (no scale ladder), CPU/$0, mean-pool T=128, a_toy_scale_recheck / a_scale_honest_scope / §97; per-axis PC×attribute semantics covered by a separate agent (not duplicated here).
- [x] (forward) TENSION-LINK effective dim + dF/dt TIME AXIS — the KOSMOS-dim (#1768/#1772) parallel on anima's OWN 5-ch tension-link (§97), #1763 derivative form — **P1 INCONCLUSIVE / P2 HOLDS** (see block below)

## TENSION-LINK effective dimension + time axis (KOSMOS-dim parallel · #1763 d/dt · §97)

The KOSMOS *map* dimension question (PR #1768/#1772) applied to anima's own **TENSION-LINK** — the 5-CHANNEL meta-fingerprint (concept16 · context8 · meaning16 · auth1 · sender4 = 45 floats, sopfr(6)=5 channel GROUPS; `HEXAD/TENSION-LINK/README.md`) that two ConsciousMind cells exchange as a tension STREAM over time. Harness `UNIVERSE/tensionlink_dim_time.py` (sha 211d4457). Source = REAL §59-FIRE anima W-state trace SHAPE (`_real_w_trace_s59.json`, 300 steps, sha d969954a) driving the byte-faithful §65 `fingerprint_5ch` transfer law (B-S65 4/4 🔵); engine latent + 5ch map = the synthetic §65 transfer law (NOT a loaded torch ckpt — 961c07e2 not loadable, torch/sklearn absent on this CPU host). **REAL-shape-driven (synthetic-engine map). CPU / $0 / numpy-only — NO GPU, NO pods.** 3 seeds (1,7,42). Verdicts `.verdicts/tensionlink-dim-time/{F-INTRINSIC-DIM,F-CHANNEL-INDEP,F-TIME-AXIS,SUMMARY}.txt` + `results.json`.

**Is 5 right? — INCONCLUSIVE (depends on magnitude vs direction; no redundant pair).** The 5-SCALAR magnitude-summary that physically travels the link has effective dim **~2.5–2.7** (PR 2.498, erank 2.673; EXACTLY 2 of 5 PCs zero every seed; projection-ladder R² saturates at k=3) — so as a 5-scalar magnitude code it is over-specified, 3 suffice. HONEST (p7): concept & meaning are L2-NORMALIZED by §65 spec (magnitude ≡ 1.0, std 0.0), so the 2 zero PCs are a summary-CHOICE artifact, NOT proof those channels are redundant — their DIRECTION carries info. The full 45-float direction-preserving fingerprint is genuinely **~6–10-dim** (PR 6.22, erank 9.41, dim@90% = 9–11), so the 5 channel-GROUPS are NOT mutually redundant. No channel pair |r| ≥ 0.8; per-channel shuffle cross-prediction r² ≤ 0.04 (mutually near-independent). An INDEPENDENT 6th channel adds +0.96 effective dim; a DERIVABLE 6th adds 0 → 5 is a design choice (sopfr(6)=5), not a hard ceiling.

**Does a dF/dt time axis capture tension dynamics? — HOLDS.** `[5ch] → [5ch + dF/dt(5ch)]` (#1763: time enters via the derivative). On a DYNAMICS-NECESSARY label (rising/falling tension = sign dF/dt; base rate 0.727): static 5-ch decode **0.542** (below base — a snapshot genuinely cannot tell rising from falling) < dF/dt-augmented **0.811** (**+0.269** over 3 seeds) — and it BEATS the shuffle control: time-aug collapses to **0.747 ≈ base** when the (row,label) pairs are permuted to destroy temporal order. Corroboration: dF/dt energy orig ≈293 vs scrambled ≈1.14e6 (≈3900×), while the static-marginal column-mean L2 is EXACTLY invariant under scramble. The derivative is the carrier of tension dynamics; the static channel-magnitude marginal is permutation-blind to it.

HONEST SCOPE: toy-scale 300-step real-shape stream + §65 transfer law; scale-transfer unverified (a_toy_scale_recheck · a_scale_honest_scope · a_paper_negative_ok · §97 tension-link = anima's own channel). Ties #1763 (d/dt time-entry) and parallels the KOSMOS map-dim work #1768/#1772.
