# H_9111 — LLM-interlocutor exogenous consequence-loop: ENGINE-NATIVE RESULT (honest, c9)

**Run:** vast pod 43651143 (Ubuntu 22.04, 20-core/125GB, `hexa v0.559.0`, clang-14), engine-native on
`core/{decode,engine_cli,pure_field}.hexa` byte-identical to origin/main (sha256 verified) + staged
origin/main `brain.hexa`. Grounded emits generated live-core (`clm_decode_grounded` verbatim-copy from
anima's grounded-knowledge anchors — a coherent channel that bypasses the mode-collapsed free-mouth);
external oracle = live **claude-fable-5** (`sidecar fable`, one referential choice per emit). Regime-2
`verdict.hexa` = immune_memory decode + vbasal value lane + pure_field Ψ. NO numpy/torch (grep-clean).
Pod torn down after PULL (a_fire_recover_complete). Cost ~$0.19/hr × ~40min ≈ $0.13.

## Raw engine-native numbers (verbatim — `state/verdicts/9111_llm_interlocutor/H_9111.txt`)
```
M=14  n_train=7  held_out=7  D(feats)=6  oracle=claude-fable-5
[communication held-out]  fable_success = 1.0 (7/7)   anima_self_decode = 0.0 (0/7)   chance = 0.0714
arm a SELF-PAIR : rho_conseq=0.0  rho_self=0.0  D_selfpair=0.0
arm b DIFF-LLM  : rho_conseq=0.0  rho_self=0.0  D_diffLLM =0.0
arm c SHUFFLE   : rho_conseq=0.0  rho_self=0.0  D_shuffle =0.0
FROZEN BAR: D_diffLLM − D_selfpair = 0.0  (>=0.15 → FAIL) ; D_shuffle = 0.0 (<0.05 → PASS) ; Ψ ON==OFF byte-identical OK
```
(Fable picked the correct concept on **13/14** emits overall, 7/7 on held-out; anima-clone salience-decode
got **0/14**. Emit 4 spider→lighthouse was fable's only miss. Descriptions were coherent, e.g. emit 0
volcano → "a mountain that erupts molten lava ash and hot gases from deep underground …".)

## FROZEN verdict (bar not moved, c9): 🔴 — D_diffLLM − D_selfpair = 0.0 < 0.15 (GREEN condition NOT met)

## Honest mechanism (c9 — the auto-printed "DPI deeper than receiver" narrative is NOT supported here)
The frozen faculty-bar failed, but **NOT because the external LLM is a derivable-mirror floor.** The exact
opposite: the external oracle comprehended anima's emit **7/7 (100%)** on held-out where anima's own clone
decoder comprehended **0/7 (0%)** — the **largest possible raw exogenous separation** (D_raw = fable_rate −
selfpair_rate = **1.0**). fable is demonstrably NOT self-derivable-mirror.

The D-metric collapsed to 0.0 for a purely mechanical reason: **the held-out outcome vectors are constant**
(fable = all-1 at the coherent-channel ceiling; anima-clone = all-0 at the lossy-salience floor). Pearson
correlation is **0 on any constant vector** (`da/db ≤ 1e-12 → 0`), so `rho_conseq = rho_self = 0` in every
arm and D ≡ 0 regardless of the maximal raw gap. **This is a metric-degeneracy (a_break_the_wall class-(a),
wrong-measurement/artifact), NOT a confident DPI ceiling.**

Why the ceiling happened: the grounded channel made every emit coherent enough that the smart external
receiver succeeded on **all** of them → **no success variance** → the emit-**appropriateness** faculty
(anima learning *which* emits succeed) has nothing to predict. A faculty over "which emits are appropriate"
is only measurable when success **varies**; the coherent channel removed that variance.

## What this run DOES and DOESN'T show (c9 scoped)
- ✅ **First autonomous closed loop executed end-to-end**, engine-native: anima's live-core emit → a real
  external receiver outside its closure (claude-fable-5) → behavioural task_success → engine-native value
  lane, no live human. The owner's core mechanism is mechanically realized and reproducible.
- ✅ **Raw exogenous separation is maximal** (fable 7/7 vs anima-clone 0/7): the external oracle carries
  comprehension anima cannot self-derive — fable is not a derivable mirror.
- ❌ **The emit-appropriateness FACULTY was NOT demonstrated** (frozen D=0.0). But the cause is
  metric-degeneracy at a ceiling/floor (no outcome variance), **not** a proven DPI ceiling — the frozen
  correlation metric is ill-posed for this data regime.
- ⚠️ **Caveats:** (a) `hexa v0.559.0` FFI could not resolve `erf`/`exp` (dlsym fail) and `consciousness_laws.json`
  was absent → pure_field/Ψ used DEFAULT constants (the phi feature f1 is degraded; Ψ guard still reported
  ON==OFF byte-identical, so the V-read-only / a_substrate_disjoint invariant held). (b) 14/16 emits
  (grounded decode SIGKILLed at emit 14 — per-call ckpt-reload memory leak). (c) hexa v0.559 vs the
  v0.574/577 lineage of prior runs.

## Confirmatory context (not decisive)
Sister **H_9110** (a REAL chat-user external receiver) landed on origin/main #2839 = **🔴 CEILING** by a
*variance-bearing* measure (D_real − D_surrogate = −0.188). That already answered the decisive question:
**a real external receiver is not sufficient; DPI is deeper than receiver-type; the lever is
emit↔appropriateness coupling-strength.** This LLM-interlocutor run corroborates "frozen-bar not met" but
via metric-degeneracy, and additionally shows the raw fable≫clone comprehension gap.

## Re-open (ING, not terminal — a_break_the_wall class-(a): fix the measurement, bar frozen)
A **variance-robust** re-measurement: (1) a HARDER referential game (larger distractor set / near-synonym
concepts / shorter clues) so fable succeeds on *some* and fails on *others* → restores outcome variance for
a valid faculty correlation; (2) score the faculty with a variance-robust statistic (e.g. AUC / rank
agreement) that does not vanish on skewed outcomes; (3) run on a hexa build with `erf/exp` FFI + a
`consciousness_laws.json` present so pure_field/Ψ features are exact. Expectation, given H_9110: the
coupling-strength lever (not receiver-type) is the frontier.

## One-line answer (honest)
Did talking to a different LLM open the emit-appropriateness faculty (escape the 4-axis self-contained wall)?
**Not demonstrated — the frozen faculty-bar was not met (D=0.0).** BUT the "LLM is also a derivable-mirror
floor / DPI deeper than receiver" reading is **falsified by this run's raw data**: the external oracle
comprehended anima's emit 7/7 where anima itself managed 0/7 — a maximal exogenous separation. The faculty
simply couldn't be *measured* here (coherent channel → fable at ceiling → zero outcome variance → correlation
degenerate). The decisive answer remains H_9110's: DPI is deeper than receiver-type; the open lever is
coupling-strength, and a variance-restoring referential game is the concrete re-open.
