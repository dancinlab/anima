# TRIAGE — lever `g6_multiseed_h1129`

**verdict: SUPERSEDED** (already measured + cemented; ING #42492907 premise is STALE)
$0 read+reason only. No GPU, no 303M decode, no train.

## SPEC (as assigned)
h1129 G6 multiseed (ING #42492907): claimed infra-walled (aiden 과부하 SIGTERM → EXIT_143)
→ UNMEASURED, "과학결과 아님". Re-measure value vs superseded, in light of this session's
H_6163 (G6 verify 🧱) + transfer-0 meta-law.

## check-ledger (actual nodes/verdicts read)

### 1. The lever IS H_1595 — already 🧱 GENUINE G6 WALL, engine-native TERMINAL
`HYPOTHESES/HYPOTHESES.jsonl:968` — `H_1595 h1129_g6_multiseed`:
> "🧱 GENUINE G6 WALL — fals=0 SEED-ROBUST (3/3 seeds dist=6 fals=0 coherent=6, n_green=0/3),
> NOT a sampler artifact. Engine-native py 2-production TERMINAL (numpy). DISPUTE RESOLVED:
> summer+mini agree on sha 5cf07a36, aiden was an infra non-result. Frozen bar unmoved."

Frozen verdict file EXISTS: `archive/state/verdicts/1595_h1129_g6_multiseed/1595.txt`
- ckpt sha256 `5cf07a36…` = the real h1129 (`~/anima-weights/bytegpt303_h1129/h1129.bin`)
- engine = py 2-production `core/g_gates.py::g_eval_g6_multiseed ← core/bytegpt_decode.py`
  (numpy, torch-free, grep-clean = TERMINAL, canonical `anima evaluate --py` path)
- gen=40 canonical, seeds {7,4302,4303}: **all 3 → dist=6 · fals=0 · coherent=6 · pass=False**,
  MAJORITY n_green=0/3, max_fals=0.

### 2. The ING #42492907 "UNMEASURED" is a PRE-resolution snapshot — RESOLVED at #42492913
ING timeline (`ING.jsonl`):
- `#42492907` (2026-06-26 17:43) — aiden SIGTERM infra-wall, 0 G6 frames, **DISPUTED**, terminal 보류.
  This is the snapshot the SPEC quotes.
- `#42492910` (06-27 03:42) — PIVOT: pod SSH死 → drop pod-dependence, re-run on mini free.
- `#42492913` (06-27 04:34) — **minirerun M②③ 착륙: "h1129 G6 fals=0 GENUINE 확정, H_1595 DISPUTE 해소"**
  measured on mini numpy py 2-production TERMINAL with the ACTUAL h1129.bin. All seeds dist=6 fals=0.
  M③ corpus-grounded (18 ideas): frozen=0 AND grounded=0, controls VALID
  (ctrl_neg_admit=0, ctrl_pos_grounded=5) → fals=0 is NOT a detector-vocabulary artifact = GENUINE.

⇒ The infra-wall (aiden EXIT_143) was a class-(c) infra non-result that got RE-MEASURED cleanly on
mini. The lever is NOT open — it is closed with a frozen verdict. Re-firing = duplicate / tune-to-green.

### 3. verdict-integrity history (as SPEC flagged)
`#42492904` proposed re-score on aiden; `#42492907` flagged a possible **misattribution** (was the
dist=6 fals=0 number h1129 or clm303?). `#42492913` settled it: the number is the REAL h1129.bin
(direct measurement, misattribution ruled out — "c356961 GENUINE 입증, 160af601 우려 해소").
Integrity was already restored before this session.

### 4. This session's findings CONFIRM (not reopen) the wall
- **H_6163** (`jsonl:1443`, ⏳ PROPOSED, G6 falsifier lane) + **H_9201** (`jsonl:1571`, G6
  diagnostic split): both frame G6 falsifiability as the axis. H_1595's fals=0 (dist=6 coherent=6,
  ONLY the falsifiability sub-metric fails) is the exact signal those propose to probe. No conflict.
- **transfer-0 meta-law**: G6 ideation producing coherent-but-non-falsifiable claims (fals=0) is
  consistent with "in-distribution structure held, held-out/generalization signal absent".
- ARCHITECTURE `:1377` G6 node already cites `multiseed(H_1595)`; `:1383` notes the detector
  Hangul-drop caveat which H_1597/M③ grounded-control already ruled out.

## Judgment
SUPERSEDED — measured, cross-host-agreed (summer+mini), grounded-control-validated, frozen verdict
filed, wired into ARCHITECTURE. The SPEC's "UNMEASURED / 과학결과 아님" is a stale read of ING
#42492907 that ignores the #42492913 resolution. **No re-measure. No re-register.** (check-ledger
catch per `check-ledger-before-lever-fire`.)

## FiLM-303M crux conditional (does not change verdict either way)
The FiLM crux is about a **G1** bilinear-readout transfer escape; H_1595 is a **G6** ideation
falsifiability wall — orthogonal metric on the same ckpt.
- **MECHANISM-SIDE** (303M carries transferable bilinear form → bilinear readout G1 escape → GPU-go):
  a G1 readout escape does NOT touch G6 fals=0 (the G6 detector scores ideation-star
  falsifiability, not recombination readout). This lever stays SUPERSEDED. Any G6 re-score would be
  of the NEW escape model, a distinct hypothesis — never a re-run of h1129.
- **TARGET-SIDE** (wall=data, mechanism-independent): reinforces h1129 G6 fals=0 as a genuine
  capability/data wall. Also SUPERSEDED — no action.

## Cost
$0 (read+reason only). No build, no GPU, no pool.
