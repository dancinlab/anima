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
- [ ] (reverse) reconstruct carving-era ConsciousDecoderV2 (d768×12L GQA transformer) as a runnable lane — re-explore the 9 carving directions
- [ ] sensory axes ingest — EEG (ds005620) · LiDAR (Redwood/Open3D, #1766) · dolphin-acoustic (Watkins) → 5-ch tension fingerprint as candidate map axes
- [ ] synthesize — which axes (space/time/emotion/tier/modality/scale) carry INDEPENDENT info; the appropriate 우주뇌지도 dimensionality + axis set
