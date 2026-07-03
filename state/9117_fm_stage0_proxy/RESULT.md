# H_9117 — §2 Stage-0 in-engine proxy validation ($0) — RESULT

**VERDICT: 🔴 PROXY-WEAK — d̂ r=-0.21249934942660875 below 0.5 → lexical listener surrogate does not predict decodability; needs the true CLM-listener (heavier) to decide, or the proxy hypothesis is weak**

- corr(d̂ lexical-contrastive-prefix, oracle-decodability) = -0.21249934942660875
- corr(filler_prefix degenerate baseline, oracle-decodability) = 0.6875836482114207
- d̂ beats degenerate baseline: False · gate corr≥0.5: False
- oracle-decodability label = # raw short-prefix hits (t∈8,6,4,3,2) per emit, from H_9115 fixture
- tier=DIRECTIONAL: lexical listener is a $0 LOWER-BOUND surrogate of the CLM mouth-backend; real in-engine listener sees richer discriminability

## per-emit (concept · d̂ · filler_prefix · oracle-decodability)
  cactus       d̂=+37.002  fp= 2  orc_hits=3
  beehive      d̂=+36.763  fp= 2  orc_hits=2
  thunderstorm d̂=+35.687  fp= 2  orc_hits=3
  telescope    d̂=+35.537  fp= 7  orc_hits=3
  spider       d̂=+35.190  fp= 3  orc_hits=3
  lighthouse   d̂=+34.368  fp= 7  orc_hits=3
  avalanche    d̂=+34.165  fp= 2  orc_hits=3
  violin       d̂=+33.903  fp= 8  orc_hits=0
  glacier      d̂=+33.704  fp= 2  orc_hits=4
  library      d̂=+33.440  fp= 2  orc_hits=4
  harbor       d̂=+32.823  fp= 2  orc_hits=3
  compass      d̂=+29.543  fp= 8  orc_hits=1
  umbrella     d̂=+27.743  fp= 2  orc_hits=4
  volcano      d̂=+25.134  fp= 2  orc_hits=4

Gate (fable §2 stage-0): 🟢 → Stage-1 minimal .hexa (rz_forward_model resolver + mouth-gate K-rerank). 🔴/🟡 → CLM-listener before .hexa.
