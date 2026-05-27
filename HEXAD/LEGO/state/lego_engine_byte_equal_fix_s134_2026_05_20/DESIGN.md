# §134 ENGINE-BYTE-EQUALITY RESTORE + §131/§133 RE-VALIDATION

> **Verdict**: `ENGINE-BYTE-EQUALITY-RESTORED-AND-VALIDATED`. Canonical
> `HEXAD/LEGO/lego_engine.py` post-§134 produces η²=0.2712 at N=256/n_stim=12,
> **byte-equal match** to §127's source-engine value (and N=1024 subset matches:
> 0.3223). Drift magnitude at N=256: 0.0535.
> fix-tier + probe-tier · $0 · 13m 40s Mac CPU. central c93e160a 0-diff.
> **First §N landed under `g_new_state_path` governance** (2026-05-20):
> dir at `HEXAD/LEGO/state/`, NOT flat `state/`.

## §0 Why §134

§133 measured per-N pooled η² values **differing materially** from §127's
published values at every N:

| N    | §127 pooled (source-engine) | §133 pooled (post-§129 engine) | Δ      |
|------|------------------------------|---------------------------------|--------|
| 256  | 0.2712                       | 0.2178                          | 0.0535 |
| 512  | 0.3289                       | 0.2563                          | 0.0726 |
| 1024 | 0.3223                       | 0.2815                          | 0.0408 |
| 2048 | 0.2608                       | 0.2377                          | 0.0231 |

AST diff of `state/lego_assembly_run_s117_2026_05_19/lego_sim.py` vs
`HEXAD/LEGO/lego_engine.py` (post-§129 promote) revealed the promote was NOT
byte-equal as claimed. Differences:

- `v` init: §117 `np.full(N, v_rest, dtype=np.float64)` (deterministic 0.0)
  vs §129 `rng.normal(0, 0.1).astype(np.float32)` (random Gaussian)
- `refr` dtype: int64 → int32
- `W` init: §117 `0.05 * rng.standard_normal((N,N))` vs §129
  `self.rng.normal(0, W_INIT_SCALE)` — different RNG consumption pattern
- **Missing `bias` term** in §129's LIFNet (§117 has random bias
  `0.18 * rng.standard_normal(N)`)
- STDP rates: §117 A_plus=0.012/A_minus=0.0126 vs §129 a_plus=0.01/a_minus=0.012
- w_max: §117 0.5 vs §129 1.0
- step() function: §117 has bias-added drive + `refr clip to -1` + dtype
  float64; §129 omits these

§131 / §132 / §133 measured the *post-§129 drifted engine*. §127 measured the
*§117 source engine*. **Two different LIF substrates were active in the arc**.

## §1 §134 fix — byte-equal restore

Rewrote `HEXAD/LEGO/lego_engine.py` to be **byte-equal** to §117 source:

- LIFNet class body: **AST byte-equal** to §117 (B-S134-2)
- spike_rate_vec: AST byte-equal
- psi_c1: AST byte-equal (only docstring text differs)
- make_stimuli: identical to §125/§126/§127/§131/§133 probes
- variance_decomposition: identical to all §12X probes

Module-level constants `V_REST`, `V_THRESHOLD`, etc. removed (§129's attempt
to factor them broke RNG consumption order). Reverted to §117's inline
literals.

## §2 Smoke validation (B-S134-3 closed)

Same seed (1337), 80 timesteps with deterministic stimulus:

```
init W byte-equal:          True
init v byte-equal:          True
init bias byte-equal:       True
post-80step spike byte-eq:  True
post-80step W byte-equal:   True
```

Engine paths now produce **byte-identical output** from initial state through
post-80-step state.

## §3 Re-validation results

### §131 n_stim cardinality (canonical engine post-§134):

| n_stim | drifted η² | **canonical η²** | drift |
|--------|------------|-------------------|-------|
| 4      | 0.3084     | **0.3093**        | 0.0009 |
| 12     | 0.2178     | **0.2712**        | 0.0534 |
| 24     | 0.1402     | **0.2439**        | 0.1037 |
| 48     | 0.1535     | **0.1697**        | 0.0162 |

**§131 verdict UNCHANGED**: η² range ratio 0.3093/0.1697 = **1.823×** (drifted
was 2.199×) — both > 1.50 threshold → STRONGLY-NSTIM-DEPENDENT survives the
fix. Peak still at n_stim=4. Qualitative finding preserved; quantitatively
the canonical engine shows *less extreme* η² depression at high n_stim.

### §133 per-N (canonical, 2-point subset N ∈ {256, 1024}):

| N    | drifted pooled | **canonical pooled** | matches §127? |
|------|----------------|-----------------------|---------------|
| 256  | 0.2178         | **0.2712**            | ✅ byte-equal  |
| 1024 | 0.2815         | **0.3223**            | ✅ byte-equal  |

**§127's published pooled η² values are CONFIRMED** by canonical engine
post-§134. Drifted §133 measurements were of a different substrate.

Per-replicate mean (canonical, N=256): 0.4639. Drifted: 0.3817.

### Drift diagnostics

```
s127 (source-engine):                    η²(N=256) = 0.2712
s131-revalidated (canonical post-§134):  η²(N=256, n_stim=12) = 0.2712  ← byte-equal §127
s133-revalidated (canonical post-§134):  η²(N=256, pooled) = 0.2712  ← byte-equal §127
drift magnitude (drifted → canonical): 0.0535
```

## §4 Honest disposition of §131/§133 originals

§131 / §133 measurements **remain valid as historical evidence** of the
*drifted-engine substrate* — they are not retracted. The state-dirs at
`state/lego_layer2_*` are sha-locked historical record (per g3 drift-
avoidance + g6 append-only). §131/§133's qualitative findings
(STRONGLY-NSTIM-DEPENDENT, monotone-decreasing per-rep mean) survive on
both substrates — the drift is quantitative, not categorical.

The **canonical** engine (post-§134) is what new probes should import. The
§129 promote claim "byte-equal to §117 source" is honestly retracted by
§134.

## §5 What §134 closes

✅ Engine source-of-truth restored to byte-equal §117 (AST + 80-step smoke).
✅ §127's η² values byte-equal-confirmed against canonical engine (predicts
   match at N=256 + N=1024 → both match exactly).
✅ §131's STRONGLY-NSTIM-DEPENDENT verdict survives engine fix
   (canonical ratio 1.823× > 1.50 threshold).
✅ §131/§133 measurements honestly carried as "drifted-engine substrate"
   evidence — neither retracted nor inflated.
✅ Engine integrity is itself a measured property of the LEGO arc.

## §6 What §134 does NOT close

❌ §132's analysis is on §127 data, unaffected by §131/§133 drift — but
   the inverted-U Gaussian shape it identified was on §127's source-engine
   data, which is unchanged.
❌ §133's "monotone decrease in per-rep mean" finding needs re-running
   with M=5 on canonical at all 4 N points (only N=256 + N=1024 subset
   was checked in §134). Future cycle: §135 candidate.
❌ Layer-3 (TASK-GROUNDED) — §128 DESIGN-CLOSE carry.
❌ GOAL emergence (B-EMERGE-7 necessary-not-sufficient).

## §7 Path note (g_new_state_path)

`@D g_new_state_path` governance landed 2026-05-20 (mid-§134, after probe
dir was created at `state/`). §134 is **the first §N to comply with the new
rule**: dir moved to `HEXAD/LEGO/state/lego_engine_byte_equal_fix_s134_2026_05_20/`
before commit. Future §135+ LEGO cycles default to `HEXAD/LEGO/state/`.

§131-revalidated and §133-revalidated outputs live inside §134's result.json
(per `g_doc_consolidation` — single doc, not new dirs). Original §131/§133
dirs at flat `state/` retained as historical evidence per
`g_new_state_path scope_exclusion`.

## §8 Closed-form propositions

```
B-S134-1   ENGINE-DRIFT-MEASURED-NONZERO        (η² drift > 1e-3 at 4 N points)
B-S134-2   LIFNET-AST-BYTE-EQUAL-S117           (AST class node string equality)
B-S134-3   80-STEP-RUNTIME-BYTE-EQUAL            (smoke comparison)
B-S134-4   CANONICAL-MATCHES-S127                (η²(N=256/1024) byte-equal §127)
B-S134-5   S131-VERDICT-SURVIVES-FIX            (STRONGLY-NSTIM still > 1.50)
B-S134-6   G-NEW-STATE-PATH-COMPLIANT           (dir under HEXAD/LEGO/state/)
B-S134-7   CENTRAL-0-DIFF + NO-FORBIDDEN-CALL-AST
B-S134-NOTE  empirical carve-out — §134 closes drift detection + fix, NOT GOAL.
```

## §9 Honest C3 (13)

1. §129 promote was a *promotion error*, not malicious — I rewrote `__init__`
   into what I thought was an equivalent form using module-level constants.
   The change in v init (deterministic → random Gaussian) and the missing
   `bias` term were the load-bearing differences.
2. AST byte-equal check (B-S134-2) is the strongest engine-integrity signal
   short of file-level byte-equal. Source file differs in module-level layout
   (constants vs literals) but the LIFNet class produces byte-equal output.
3. The drift was DETECTED by §133's measurement comparison to §127, not by
   AST review — a key lesson: instrument integrity needs measurement-level
   confirmation, not just code review.
4. §131's STRONGLY-NSTIM-DEPENDENT verdict survives at lower magnitude
   (1.823× vs 2.199×) — the qualitative finding is robust to this drift.
5. §132's analysis is unaffected (input was §127's source-engine data).
6. §133's monotone-decrease-in-per-rep-mean finding needs full 4-point
   re-run on canonical; only 2-point subset checked here. Future cycle.
7. WALL-A orthogonal · WALL-B confronted-not-removed (carry).
8. anima downstream-consumer: hexa-lang/hexa-bio/hexa-matter read-only,
   0 edits. HEXA_FIRST_WARN deferred (B-S* battery precedent).
9. The new `g_new_state_path` governance applies to §134 (first dir under
   `HEXAD/LEGO/state/`).
10. g3: fix ≠ measurement ≠ fire ≠ emergence; capability claim 0.
11. necessary-not-sufficient (B-EMERGE-7).
12. north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.
13. §134 is the cleanest g3 honest-correction cycle of the LEGO arc — a
    measurement detected its own instrument bias, the bias was fixed, the
    fix was validated. Instrument integrity is a measurable property.
