# H_6165 — G6 FALS attention-capacity CAP×REG factorial — VERDICT

**tier:** 🧱 WALL (DIRECTIONAL — torch-side 5-bar; engine-native terminal = follow-on, ckpt not saved) · **scope:** 303M h1129 ByteGPT (sha 5cf07a36) · 18 cells = CAP{N=1,2,4 injected BindAttn blocks} × REG{off,on} × 3 seeds{7,4302,4303} × 600 steps, base frozen.

## Result (all 18 cells, `results/`)

| arm | max FALS_in | any GREEN | pattern |
|---|---|---|---|
| REG-off (9) | **0.0** | no | FALS_in=0 across N=1/2/4; DIST rises with N (3.67→5.0) but zero falsifiability |
| REG-on (9) | **0.33** | no | only N2 s4302/s7 hit 0.33 — but FALS_shuf==FALS_in (B3 X-shuffle NO-collapse) = interchangeable-shell FORM, not earned binding (the H_1449 pattern); below B1 floor (≥1) |

**No cell crosses the frozen 5-bar. MAX FALS_in = 0.33 (form-lift, B3 no-collapse).**

## What this disambiguates (the point H_1449 confounded)

H_1449 (1-block) mixed capacity + register in one cell → 🧱 WALL=CAPACITY. This factorial separates them:
- **CAP axis (depth 1→2→4 blocks) = NULL** — more injected attention adds DIST/coherence, ZERO FALS lift. Depth-capacity is NOT the G6 FALS lever.
- **REG axis (off→on) = FORM-ONLY** — corpus-register gives a cosmetic FALS_in 0→0.33 in 2 cells, but B3 X-shuffle does NOT collapse ⇒ generic form, not earned comparator∧measurable binding. Consistent with H_1596/H_1597 (register affects surface, not the co-emission faculty).
- **CAP×REG interaction = NONE** — no super-additive cell; the tiny form-lift is at N=2 not N=4.

⇒ The G6 FALS wall is **neither depth-capacity NOR register-as-form** — it sits in the trunk objective / earned-binding, converging with the G1/G6 DPI meta-law. NOT a capacity ceiling fixable by injected attention.

## Honest gaps (c9)

1. **DIRECTIONAL, not TERMINAL** — the factorial ran torch training + torch-side 5-bar. Engine-native `anima evaluate --py` re-score is required to stamp terminal (a_engine_native_learning).
2. **ckpt NOT saved** — `run_factorial.py` persisted only cell JSON summaries, discarding the trained injected weights (a_fire_recover_complete violation). So BGB engine-native terminal on THESE cells is impossible without a ckpt-saving re-run. FOLLOW-ON: re-run ≥1 representative cell (e.g. N2 REG-on) with ckpt save → `anima serialize-bind` → `anima evaluate --py` (the BGB decode landed #2714 makes this now possible — validates the enabler end-to-end + stamps terminal).

## artifacts
`results/all_cells_REG{off,on}.json` · `results/cell_N{1,2,4}_REG{off,on}_s{7,4302,4303}.json` · `results/fire_{off,on}.log` · base `results/base_eval_{off,on}.json`.
