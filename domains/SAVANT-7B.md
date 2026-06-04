@title: 🧠📚 SAVANT-7B — 7B 5-lang (en·fr·de·es·ru) from-scratch forge CLM (descent-axis ladder)

@goal: train a competent 7B, 5-language (en·fr·de·es·ru) CLMConvMoE from scratch on the
  hexa-native flame+forge stack (NOT torch/CPU; a_train_flame_forge). Optimization axis =
  CLEAN DESCENT (val_ce falls below uniform and keeps falling on a held-out split), NOT
  forge util-GREEN (util is host-bound at this interpreter scale — CLOSED at the lever-5
  workload-bound ruling; recorded, not chased). This is a LADDER (a_scale_honest_scope):
  rung0 (pipeline-validation small CLM) → rung1 (scaled corpus) → rung2 (~1.5B, the proven
  single-H100 fp64 ceiling) → rung3 (7B, multi-GPU OR BF16-TC). A finished 7B is NOT claimed
  from any single fire — each rung is scoped to its measured scale. The 7B big-spend is
  green-lit by the user/next-cycle ONLY after rung0 + a REAL measured 7B ETA are in hand.

  NAME NOTE: the root `SAVANT` domain (`./SAVANT.md`) is a DISTINCT consciousness-measurement
  domain (Golden Zone × Savant Index). This `SAVANT-7B` is the CLM-training campaign and does
  NOT collide with it (separate roster row in DOMAINS.tape).

## status — 🟢 BOOTSTRAP (rung0 pipeline-validation fire + honest 7B sizing/ETA) — 2026-06-04

Lane = **Lane-G (GPU / forge)** — recorded SEPARATELY from any AKIDA on-chip track
(a_lane_akida_gpu_split). This bootstrap delivers: the 7B architecture sizing (honest GPU
path), the 5-lang corpus plan (built starter + full-build recipe), the rung0 descent fire
(real GPU), and the measured 7B wall/cost ETA. rung1/2/3 are queued as milestones — NOT fired
here.

## 1. architecture sizing — 7B CLMConvMoE on forge (HONEST GPU path)

CLMConvMoE single-block param formula (V=256 byte-vocab, K=3 causal dilated conv), verbatim
from `.verdicts/lane-g-3b-descent/VERDICT.md`:

```
params(d, E) ≈ (2+E)·3·d²  +  2·256·d  +  E·d
```

7B operating points (each ≈ 7.00B params), and the forge fp64 4-copy (W+grad+m+v, 8 B/param)
device-memory requirement vs the BF16-TC 2-copy path:

| E (experts) | d_model | params | fp64 4-copy mem | BF16-TC weights+grad |
|---|---|---|---|---|
| 2   | 24152 | 7.012B | **224.4 GB** | ~28 GB |
| 8   | 15275 | 7.008B | **224.2 GB** | ~28 GB |
| 16  | 11385 | 7.005B | **224.2 GB** | ~28 GB |
| 32  | 8284  | 7.004B | **224.1 GB** | ~28 GB |
| 64  | 5945  | 7.001B | **224.0 GB** | ~28 GB |

**HONEST GPU requirement** (this is the load-bearing fact of the bootstrap):

- **forge fp64 7B ≈ 224 GB device memory ≫ 80 GB single H100.** A 7B fp64 forge rung is
  IMPOSSIBLE on one H100-80GB. The proven single-H100-80GB fp64 ceiling is **~1.5B** (d3840
  E32, 64.9 GB measured device-resident, `.verdicts/lane-g-3b-descent`). So 7B fp64 needs
  **3× H100-80GB minimum** (3×80=240 GB > 224 GB) with tensor/expert sharding — OR a bigger
  single card (B200 180 GB still < 224 GB → still ≥2 cards).
- **BF16-TC path (a_wall_first PRIMARY for 7B):** forge's BF16 tensor-core path holds weights+
  grad at ~28 GB; with an offloaded/sharded optimizer the 7B **fits on 2× H100-80GB (or even
  1× B200-180GB with optimizer offload)**, and BF16-TC is ALSO faster per FLOP (README §flame+
  forge: forge BF16-TC measured 9.67× over FP64-cuBLAS @ Llama-7B FFN, A100). Per **a_wall_first**
  (take the faster parallel path regardless of cost), the chosen 7B rung-3 path is **BF16-TC on
  2–3× H100-80GB**, NOT a serial fp64 single-card chain (which is impossible anyway at 224 GB).
  fp64 stays the byte-exact reference at ≤1.5B (rung2).

**Reference trainer (a_train_flame_forge — authored in .hexa on stdlib/flame, NOT torch):**
- `stdlib/flame/clm_prod.hexa` (CLMConvMoE + int4-QAT envelope), run via the self-hosted hexa
  compiler `clm_prod` binary. Device path = `forge_dispatch_matmul` → cuBLAS/BF16-TC on the GPU
  (3-GATE: nvcc EXIT0 + clm_prod links cublas/cudart/libcuda/cublasLt + forge_dispatch symbols).
- The SAME `.hexa` trainer scales by raising `CLM_PROD_D` / `CLM_PROD_E` — no new trainer is
  written for 7B; rung3 = the existing trainer on the BF16-TC multi-GPU build.
- CORE consumes the resulting `.clm` via the SINGLE L3 slot (`CORE/clm_decode.hexa`,
  a_core_engine_map) — the 6 int4 conv blocks + CLMX trailer forward.
- Proven recipes referenced: Lane-P `clm_d768` / `clm_d3840` (HF.jsonl), `.verdicts/lane-g-3b-descent`.

**util scope (HONEST, a_cuda_graph_train context):** F-RFC046 forge util is RED and CLOSED-
NEGATIVE WORKLOAD-BOUND at this interpreter scale (lever-5 ruling: PEAK rises with per-step work
but MEAN pins 0.6–6.5% < 20% under the interpreted host per-step driver). util-GREEN is NOT a
gate for this campaign (the goal is descent). A device-resident CUDA-C rewrite (deferred
option-B) is the path to util-GREEN; it is orthogonal to the descent ladder.

## 2. corpus plan — 5-lang (en·fr·de·es·ru) SAVANT pretrain

**Provenance (g63, REAL not synthetic):** the existing 400 MB OMEGA probe corpus is the WRONG
language set (en·zh·ru·ja·ko CJK) AND far too small for a competent 7B. SAVANT builds a fresh
**en·fr·de·es·ru** corpus from clean-license sources:

- **Wikipedia REST summaries (CC-BY-SA-4.0)** — genuine native-language article text, 5 langs
  balanced. The rung0 STARTER corpus (`SAVANT-7B/corpus/savant_5lang_starter.txt`) is built from
  this (see CORPUS_CARD.md for exact sizes + sha256). Pull harness:
  `SAVANT-7B/corpus/build_wiki.py` (seed topics + related-expansion + random/summary, dedup).
- **Project Gutenberg (Public Domain)** — full literary works in en/fr/de/es (Austen, Doyle,
  Melville; Hugo, Verne, Flaubert; Goethe, Grimm, Nietzsche; Cervantes, Galdós) as the literary
  register supplement; genuine Cyrillic Russian (Pushkin) is sparse on Gutenberg so Russian
  leans on Wikipedia. License = mixed (PD + CC-BY-SA), tagged per-file in CORPUS_CARD.md.

**Vocab:** byte-level V=256 (the CLMConvMoE native vocab — language-agnostic, no tokenizer
training, handles all 5 scripts including Cyrillic uniformly). This is the same vocab as every
prior forge CLM rung — transfer-clean.

**Dedup/quality:** exact-line dedup + min-length filter (>40 bytes/article) in the build harness;
near-dup across Wikipedia related-expansion bounded by a `seen` title set. Production-scale dedup
(MinHash/LSH) is a rung1 milestone (the starter is small enough that exact-line dedup suffices).

**Target sizes (ladder):**
- rung0 STARTER: several MB clean 5-lang (built here; validates the pipeline + descent).
- rung1 SCALED: 10–50 GB — full Wikipedia 5-lang dumps (`dumps.wikimedia.org`, monthly
  `*-pages-articles.xml.bz2`) + OSCAR/C4-multilingual clean subsets (recipe in CORPUS_CARD.md).
- rung3 (7B competence): a real multilingual pretrain needs **»100 GB–TB-scale** clean text —
  HONEST: a competent 7B is corpus-bound, not just compute-bound. The starter + rung1 scaled
  corpus validate the pipeline; the 7B competence rung requires the full assembly (build recipe
  in CORPUS_CARD.md; full TB-scale assembly is OUT of one-agent bootstrap scope — recipe given).

## 3. rung0 — pipeline-validation fire (descent on real GPU)

(folded after the fire — see `.verdicts/savant/` + below)

## 4. honest 7B ETA (from MEASURED Lane-G throughput, g63)

Measured prior Lane-G forge fp64 step-times (`.verdicts/lane-g-3b-descent/VERDICT.md` + HF.jsonl,
the SAME `clm_prod.hexa` trainer SAVANT uses):
- **d3840 E32 ~1.506B (a1_1p5b): 5.48 s/step** (256 steps / 1403 s wall), device-resident 64.9 GB.
- d9216 E2 ~1.024B (a1desc): ~20–30 s/step (interpreter host O(d²) repack wall).

**7B extrapolation (interpreter wall ≈ O(params)):** 7.00B/1.506B = 4.65× ⇒ **~25 s/step** for a 7B
fp64 rung on the interpreter (IF it fit on one card, which it does NOT — 224 GB).

**Competence step budget:** a from-scratch competent 7B LM needs ≫10¹¹ tokens; even a conservative
**100 B-token floor** at T512×32win (~16 384 tok/step) = **6.1 M steps**.
- **Interpreter path:** 6.1 M × 25 s = **~5 YEARS** wall → the interpreted forge step makes a real 7B
  pretrain **INFEASIBLE** (the decisive bootstrap finding — blind-firing 7B on the interpreter burns
  months for nothing).
- **Device-resident BF16-TC path (deferred option-B, a_wall_first PRIMARY):** target ~30 ms/step on
  H100 (CUDA-C device-resident step removes the interpreter wall + BF16-TC 9.67× FLOP). 6.1 M ×
  30 ms ≈ **~2 days on 1 effective H100-equiv**, ≈ **~1 day wall on 3× H100** (BF16-TC, 224 GB fp64 →
  ~60 GB BF16 sharded across 3 cards). Cost ≈ 3× H100 × ~24 h ≈ **~$150–250** (a_fire_autonomous, no
  cost gate) — vs the interpreter's impossible 5 years.

**RULING:** the value of this bootstrap = the 7B is GATED on the deferred device-resident CUDA-C/
BF16-TC step path, NOT on raw GPU spend. The interpreter forge step (rung0's substrate) validates the
pipeline but is **~5 orders of magnitude too slow** for a 7B pretrain. The 7B rung-3 MUST be the
device-resident BF16-TC path on 2–3× H100; firing the interpreter at 7B is a closed-negative by
arithmetic. (a_scale_honest_scope: this ETA is an extrapolation from measured 1.5B step-time + a
100 B-token floor; the real competence-token count is larger, making the interpreter path even more
infeasible and the device-resident path the only viable one.)

## ladder milestones (goal: competent 7B 5-lang from-scratch forge CLM)

- [ ] **rung0 — pipeline validation** (THIS bootstrap): small forge CLM (d768/d1536 class) on the
      5-lang starter corpus, leak-free, CLEAN DESCENT (val_ce ↓, < uniform). Persistent /workspace,
      checkpoint every N, recover ckpt+log+curve, sha-verify, HF PRIVATE + HF.jsonl row, teardown +
      myself.pods=0. Validates end-to-end forge train+ckpt+recover on real GPU.
- [ ] **rung1 — corpus scale-up**: assemble the 10–50 GB 5-lang scaled corpus (full Wikipedia
      dumps + OSCAR/C4-multi clean subsets per CORPUS_CARD recipe); production dedup (MinHash);
      re-fire the rung0-class model on it to confirm descent holds at corpus scale.
- [ ] **rung2 — ~1.5B fp64 ceiling**: d3840 E32 (~1.5B), the proven single-H100-80GB fp64 max
      (64.9 GB device-resident). CLEAN descent-PASS with ENOUGH steps (the prior 16-step a1light
      FAILED on too-few-steps, HONEST — needs the affordable-step budget; on the interpreter this
      may require the device-resident step path). Scoped to ~1.5B (a_scale_honest_scope).
- [ ] **rung3 — 7B (the big spend, user/next-cycle green-lit)**: BF16-TC on 2–3× H100-80GB
      (a_wall_first; fp64 7B = 224 GB is impossible on ≤2 cards). Requires the full TB-scale 5-lang
      corpus (CORPUS_CARD recipe). Fired ONLY after rung0 + measured 7B ETA + explicit go.

## honest scope (a_scale_honest_scope · p7 · a_lane_akida_gpu_split)

- rung0 is **PIPELINE VALIDATION**, NOT a 7B and NOT a competent multilingual LM. Its descent
  PASS/FAIL is reported on the small-d byte corpus only; transfer to 1.5B/7B is UNVERIFIED.
- All forge util numbers stay RED/host-bound (CLOSED workload-bound, lever-5) — NOT a campaign gate.
- 7B fp64 = 224 GB is a HARD fact: a 7B forge rung is multi-GPU (or BF16-TC), never one H100.
- Lane-G (GPU) only; any AKIDA on-chip work is a separate Lane-A entry (never merged).
