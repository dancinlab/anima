# H_9119 — §2 forward-model rerank LOWERS the frozen-listener b50 (front-loads referential decodability)

**tier:** 🟠 DIRECTIONAL — the forward-model rerank (gen_fm_rerank, Option C) front-loads referential decodability (lowers the frozen-listener b50) on decodable concepts, shuffle control passes; but triply-DIRECTIONAL (numpy-mirror · external-oracle H_9118 · modest-ckpt). · **wired:** mechanism WIRED-live on origin/main (scorer #2881 · rerank #2889 · harness #64163e8ed · argfix #eeaa6f684 · --py mirror #2898); this is the measurement, not new wiring.

**verdict:** 🟠 DIRECTIONAL (`state/verdicts/9119_fm_b50_measure/H_9119.txt` verbatim). The GREEN test the whole §2 arc (H_9112-9117 referential efficacy + scorer + rerank) builds toward: does the best-of-K rerank reranked by `fm_prefix_decodability` LOWER the frozen-listener b50 vs un-reranked argmax?

## Result (14 concepts · speaker=deep-mouth-ladder-L4-303m · listener=ideation-303m-d5000 · gen=24 · --py numpy)
```
mean b50:  OFF(argmax)=505.21   ON(fm-rerank)=502.07   SHUFFLE=574.14
VERDICT:   b50 LOWERED by rerank (ON<OFF) | shuffle control OK (referential)
```
Per-concept (the 7 decodable ones — ~half floor at 999):
- **rerank BETTER (4):** glacier 16→2 · violin 16→4 · spider 32→8 · library 4→2
- **SAME (2):** lighthouse 2=2 · compass 2=2
- **WORSE (1):** volcano 8→16

→ On decodable concepts the rerank lowers b50 4/7, ties 2/7, raises 1/7 — the intended front-loading effect is present + directionally positive. SHUFFLE(574) > ON(502) confirms the b50 is **referential**.

## Why DIRECTIONAL not terminal GREEN (3 independent reasons, c9)
1. **--py numpy mirror** — engine-native hexa run FIRED the GPU path (`[OWN-GEMM-FIRED]` + `[EAGER-DEVGLUE-FIRED]` CUDA-erf, erf/exp fix live via `readelf` libm NEEDED) but is **CPU-scalar-bound** (scalar glue seam, not GEMM) → impractical for 14 concepts. Owner-authorized `--py` fallback. numpy = DIRECTIONAL (a_engine_native_learning).
2. **external-oracle-mediated** (H_9118) — b50 = a FROZEN LISTENER's decodability = external oracle, permanently DIRECTIONAL.
3. **modest ckpts** — ~half concepts floor at 999 → mean is floor-dominated, the ~3-byte gap is noise on the aggregate; the signal is in the per-decodable-concept 4/7-better breakdown.

## Infra (resolved, quarantined per infra-wall-noneval)
erf/exp `-lm` link = hexa-lang PR 4501 (merged) — the run measured cleanly (no dlsym failure). NOT folded into the verdict.

## Session arc (§2, this session)
fable divergence → H_9112-9117 (referential efficacy real+quantified) → Stage-1a config (#2878) → scorer (#2881) → Option C design → gen_fm_rerank (#2889) → b50 harness (#64163e8ed) → **infra walls: erf/exp fix (hexa-lang PR 4501) + engine-native CPU-scalar-bound → --py mirror (#2898)** → this measurement (🟠 DIRECTIONAL, rerank front-loads b50).

## Follow-on (ING)
Terminal engine-native GREEN needs (a) practical engine-native decode (fix the CPU-scalar-bound seam) + (b) stronger chat ckpts (fewer floors). external-mind b50 stays DIRECTIONAL (H_9118).

## Evidence
`state/verdicts/9119_fm_b50_measure/H_9119.txt` · `state/9119_fm_b50_measure/b50py_result.txt` (raw 14-concept) · `state/9119_fm_b50_measure/fm_b50.hexa` (engine-native harness) · `state/9119_fm_b50_measure/fm_b50_py.py` (--py mirror).
