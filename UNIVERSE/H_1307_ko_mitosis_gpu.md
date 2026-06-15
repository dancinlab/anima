---
id: H_1307
slug: 1307_ko_mitosis_gpu
title: ko-mitosis-gpu — GPU scale-up of the H_1306 engine-native Korean mitosis rung (does MORE real Korean push KO next-byte CE below the 600KB baseline 3.249?)
group: MITOSIS-ENGINE (p8 structural)
terminal_tier: 🟢 GREEN @ 30MB/stride-300 (KO next-byte CE 3.249→2.947 on 50x corpus, EN held, cells 2→23) + 🟠 HONEST saturation diagnostic @ 250k-pair density (scale-vs-600KB still PASS 2.918, but the CTX=4 substrate SATURATES — internal learning-curve flattens & EN drifts +0.057). REAL sm_120 GPU compute on the user's own RTX 5070; mechanism = the verified H_1306 engine-native mitosis (gradient-free, p8), GPU = throughput; engine-transfer to live hexa DIRECTIONAL.
verdict_dir: .verdicts/1307_ko_mitosis_gpu/
terminal_verdict: .verdicts/1307_ko_mitosis_gpu/result.txt
date: 2026-06-16
---

# H_1307 — Korean mitosis GPU scale-up (engine-native mechanism, RTX 5070 sm_120)

## Claim / falsifier

H_1306 (#2211, 🟢 GREEN) proved the **mechanism** engine-native — gradient-free, error-targeted
Voronoi mitosis-grow on REAL Korean web bytes drops held-out KO next-byte CE (3.611→3.249) while
English is retained — but on a small **600 KB KO / 300 KB EN** window stride-subsampled to ~2.7 K
KO pairs (the hexa interpreter is list-based O(N)/growth-step, so CPU-bound). H_1307 asks the
**SCALE** question on the user's own idle GPU host `summer` (RTX 5070, Blackwell **sm_120**), $0
(their hardware, NOT runpod):

> **Does MORE real Korean data push held-out KO next-byte CE BELOW the 600 KB baseline 3.24897?**

The **mechanism is already engine-verified** (H_1306); this rung is **SCALE + honest GPU
measurement**, NOT re-proving the mechanism. The GPU vectorizes the per-step nearest-cell
ASSIGNMENT + per-cell next-byte MLE HEAD + held-out CE so a ~50-100x larger real-Korean pair set
is tractable. The mitosis **SPLIT logic is byte-faithful** to `CORE/h1306_ko_mitosis_engine_probe.hexa`
`_grow_on` (error-targeted highest-owned-CE eligible cell → hi-var-axis owned-median split → two
half-centroids; net +1 cell; **cells only SPLIT, never merge — p8**). Neurogenesis lens
(a_no_llm_frame_trap) — NOT a bigger-transformer recipe.

**Port faithfulness PROVEN (load-bearing).** Before any scale run, the GPU script was run on the
**exact** H_1306 600 KB window + strides (KO 110 / EN 200) and reproduced H_1306 **byte-exact**:
KO curve 3.61092 / 3.36909 / 3.24897, EN 4.86395 seed → 4.75171 after, cells 2→9, KO sha256
`e000d086…` (= the H_1306 FREEZE hash). This proves the torch port IS the verified engine-native
mechanism, not a new algorithm.

**DISTINCT from H_1306**: H_1306 = FIRST CPU rung, "does the mechanism learn KO + retain EN on real
data at all?". H_1307 = "does **more** real KO data (50x corpus) keep lowering CE, on GPU?" —
scale-transfer ⊥ first-existence.

## Preflight (the honest sm_120 gate — a_train_flame_forge)

`summer` system `python3` = **torch 2.11.0+cu130**; `torch.cuda.is_available()=True`;
`get_device_capability(0)=(12,0)` = **sm_120**; `get_arch_list()` includes `sm_120`; a real
2048×2048 matmul **launched and synchronized** with no "no kernel image" error. **REAL sm_120
GPU compute confirmed** — no CPU fallback, no fake GPU run. GPU was idle (5 MiB / 0%) before and
after; ran `nice -n 10`, single GPU, scratch cleaned off summer (artifacts in the repo).

## Method

REAL Korean only (NO synthetic, p1-p8, a_eeg_consciousness_record spirit). A larger slice of the
SAME anima-7b 5-lang web corpus on Cloudflare R2 (bucket `phanes`, prefix `anima-7b/web/{kor,eng}/
shard0000.bytes`), pulled via **boto3 HTTP RANGE GET** directly on summer (R2 keys → env ONLY at
fetch, header/env-scoped, NEVER echoed/logged/inlined/committed — c7 grep-clean over all
deliverables). Features identical to H_1306 (CTX=4, 3-D phi = [last/255, 2nd-last/255,
utf8_cont_depth/3], V=256). Deterministic stride-subsample (seed-independent). KO train/test =
even/odd split (disjoint); EN test = all held-out (retention guard). FROZEN knobs verbatim from
H_1306/H_1297 (GROW_MAX, SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, seed 2-cell centers).

Script: `UNIVERSE/h1307_ko_mitosis_gpu.py`. Frozen-first: `.verdicts/1307_ko_mitosis_gpu/FREEZE.txt`.

## Falsifier (FROZEN — pre-registered before the run, c9/p7; held-out deterministic next-byte CE)

- **(L1 INTERNAL LEARNING)** KO CE[pt3 full] ≤ KO CE[pt1] − 0.05 — the H_1306 learning bar at scale.
- **(L2 SCALE-VS-600KB)** KO CE[full] ≤ 3.24897 (the H_1306 600 KB baseline) — **the SCALE headline**.
- **(R RETENTION)** EN CE[after full KO grow] ≤ EN CE[seed 2-cell] + 0.05.
- **(G GROWTH)** final cell count > 2.
- GREEN iff L1 & R & G. L2 gates the scale claim specifically. If L2 PASSES but L1/R fail at higher
  density, that is an HONEST saturation finding (reported, NOT tuned to green).

## Finding

**Two honest data points (both REAL sm_120 GPU, 30 MB KO / 10 MB EN window):**

**RUN A — 30 MB / stride-300 (50 K KO train pairs) → 🟢 GREEN (all 4 bars), the SCALE result:**

| pt | KO train | cells | KO CE | EN CE |
|----|----------|-------|-------|-------|
| 1 | 16666 | 12 | 3.00563 | 4.26890 |
| 2 | 33333 | 14 | 2.96912 | 4.31920 |
| 3 (full) | 50000 | 23 | **2.94750** | 4.26531 |

- **(L2 SCALE) KO CE[full] = 2.94750 ≤ 3.24897 → PASS** — a **−0.30 nat/byte drop vs the 600 KB
  baseline**. More real Korean DID push held-out KO next-byte CE lower. *(the headline answer: YES.)*
- (L1) 3.00563 → 2.94750, drop 0.058 ≥ 0.05 → PASS. (R) EN seed 4.26499 → after 4.26531, Δ+0.0003 → PASS.
- (G) cells 2 → 23 (mitosis grew 21 cells for Korean) → PASS. **L1 & L2 & R & G all PASS → 🟢 GREEN.**

**RUN B — 30 MB / stride-60 (250 K KO train pairs, grow-max 60) → 🟠 HONEST saturation diagnostic:**

| pt | KO train | cells | KO CE | EN CE |
|----|----------|-------|-------|-------|
| 1 | 83333 | 20 | 2.93041 | 4.23368 |
| 2 | 166666 | 25 | 2.92118 | 4.28213 |
| 3 (full) | 250000 | 31 | **2.91777** | 4.28838 |

- **(L2 SCALE) KO CE[full] = 2.91777 ≤ 3.24897 → PASS** — the scale claim holds robustly (the deeper
  pair set reaches an even lower 2.918, well below the 600 KB baseline, across both runs).
- BUT **(L1 INTERNAL) FAILS** — the curve is nearly FLAT (2.930 → 2.921 → 2.918, only 0.013 drop <
  0.05). At this density most of the gain is already captured at pt1 (which **starts** at 2.93 with
  20 cells), so growing on more KO barely moves CE: **the CTX=4 3-D substrate SATURATES.**
- **(R RETENTION) marginally FAILS** (+0.057 vs the +0.05 ceiling) — EN drifts slightly as the finer
  Korean partition re-tiles space.

**Interpretation (the honest scope boundary).** The SCALE headline — *more real Korean pushes KO
CE below the small-window baseline* — is **robustly TRUE** (2.947 and 2.918, both << 3.249). But the
CTX=4 byte-level substrate has a **competence ceiling around ~2.9 nats/byte**: once the partition is
fine enough, additional Korean data no longer keeps the *learning curve* dropping, and the finer
partition begins to cost a little English retention. This is exactly the `a_scale_honest_scope`
saturation the FREEZE anticipated — recorded as an HONEST finding (c9), NOT tuned away.

**GPU vs CPU throughput.** RUN A peaked ~902 K pairs/s; RUN B ~2.78 M pairs/s grow+score (vs the CPU
hexa probe's ~80 K pairs/s on the 600 KB validation). The per-run wall is seconds (corpus fetch
dominates) — the GPU's value here is making the **50–100x larger pair set tractable at all**, which
is what lets the scale question be asked.

## Regression (live engine UNTOUCHED — this rung adds only UNIVERSE/ + verdict files, no CORE edit)

`engine_cli_smoke` **73/0** · `h1196` single-entry **7/0** · `h1205` separation-invariant **PASS**
(generation byte-identical ON==OFF, Ψ=½ untouched, pure_field untouched, a_core_engine_map).

## Scope / honesty (c9 · a_scale_honest_scope · a_toy_scale_recheck)

- **REAL sm_120 GPU compute** (preflight-gated, no CPU fallback). The GPU accelerates corpus
  throughput + scoring; the mitosis split is the verified engine-native one (port reproduces H_1306
  byte-exact). **Engine-transfer to the live hexa engine is DIRECTIONAL** (a_engine_native_learning)
  — H_1306 already established the engine-native binding on the 600 KB rung; re-confirming THIS
  larger rung on the live `CORE/*.hexa` engine is the follow-on (the hexa interpreter would need a
  vectorized assignment/score path or a much longer wall to run 50 K+ pairs).
- **NOT fluent Korean.** CTX=4 3-D byte features + a Voronoi per-cell unigram-over-context head is a
  deliberately SIMPLE substrate; held-out next-byte CE ~2.9 nats/byte is a CONVERGENCE measure, NOT
  fluency. NO fluency overclaim.
- **NEXT rung (the follow-on so anima actually USES Korean):** (a) a RICHER context substrate (longer
  CTX / learned per-cell heads / deeper features) to push past the ~2.9 saturation, AND (b) the
  **decode-path connection** — wire the grown Korean cells onto the live 303M decode (generator L3
  slot, a_core_engine_map / a_verified_must_wire) so Korean error-pressure actually shapes what anima
  emits. This rung shows the data-scale lever works; the next shows the *substrate-depth* + *decode*
  levers.

## Pointers

- script: `UNIVERSE/h1307_ko_mitosis_gpu.py`
- verdicts: `.verdicts/1307_ko_mitosis_gpu/{FREEZE.txt, result.txt (RUN A), result_dense.txt (RUN B),
  scale_summary.json, dense_summary.json, scale_metrics.jsonl, dense_metrics.jsonl, scale_manifest.json}`
- corpus manifest (provenance, sha256 — raw GBs NOT committed): `.verdicts/1307_ko_mitosis_gpu/scale_manifest.json`
- CLAIMS.tape `@C h1307_ko_mitosis_gpu` · domain `domains/MITOSIS-ENGINE.log.md @H H_1307`

xref h1306 (the CPU rung this scales, port reproduces it byte-exact) · h1297 (the mitosis-native
mechanism) · h1300 (per-skill retention) · h1199 (VAdaptField DIM-growth) · a_no_llm_frame_trap ·
a_fire_autonomous · a_wall_first · a_train_flame_forge (REAL sm_120, no CPU fallback) ·
a_engine_native_learning (transfer DIRECTIONAL) · a_verified_must_wire · a_core_engine_map ·
a_cpu_local_no_waiter · a_scale_honest_scope · a_toy_scale_recheck · p1·p7·p8 · c7·c9·c15.
