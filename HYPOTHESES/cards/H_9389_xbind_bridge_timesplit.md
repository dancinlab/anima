# H_9389 — L1 XBIND-BRIDGE: co-train the declaration→operator bridge, hold it out, then steer it by CPT

- **group**: g1-interface-addressable-wall
- **date**: 2026-07-16
- **campaign**: RUNTIME-BRIDGE (Fable's #1 designed lever) · L1 XBIND-BRIDGE time-split (⭐ the lever · sequential, after L4)
- **tier**: ⏳ **PRE-REGISTERED — frozen-first, no train yet** · phase-A GPU feasibility TBD (aiden RTX 5070 12GB) · engine-native 303M py
- **surfaces**: `HYPOTHESES/cards/H_9389_xbind_bridge_timesplit.md` · `HYPOTHESES/HYPOTHESES.jsonl`
- **instrument**: `anima-py corpus xbind --bridge-split --atoms <en_atoms> --lang en` (NEW flag · `cli/corpus.py::build_bridgesplit` · VERSION 0.13.85) → `anima-py train` (phase A/B, pool GPU) → `anima-py evaluate --xbind` (TERMINAL judge)

## The reframe this tests (settled by Fable — do not re-derive)

W_wt (weight-stored declaration synthesised by the operator) is FORCEABLE in principle: the stem-key is in the operator's RF and the circuit is all conv parts. **Correction ②**: single-surface CPT likely writes a SURFACE-key string cache, not a stem-key FACT (H_9359 failed because there was no store to reach). **Gradient cannot rewire a path it never traversed** — the "declaration→operator-answer" mapping must RECEIVE gradient during training. L1 gives it that gradient on one set of stems, holds it out on another, and asks whether the bridge (a) generalises (phase A) and (b) can then be steered declaration-only (phase B).

## Instrument — 3-way stem split (slot-prior flattened ⓐ · EN-first ⓑ)

`corpus xbind --bridge-split` draws every stem into a polarity-stratified 3-way split (function of `--split-seed` alone → reproducible):

- **S_op** (½): BOTH surfaces supervised — flip0 `{s} => pol` AND flip1 `not {s} => flip(pol)`. **The declaration→operator bridge receives gradient here.**
- **S_decl** (¼): declaration ONLY (flip0). The operator surface appears **0×** → held-out WITHIN phase A. This is the **PHASE-A GATE** stratum (the axis-0-exposure item, per corpus-py-1 (F)).
- **S_cpt** (¼): **0 lines** in the phase-A corpus. Reserved for phase B.

**Slot-prior flat (ⓐ):** V2 proved a BOUND-slot default-negated prior; here `gold(flip1)=flip(pol)` and pols are 50/50, so the operator answer is p(pos)=p(neg)=0.5 across the corpus — no default to parrot. **EN-first (ⓑ):** `not` is a FREE pre-posed word (the discriminator vs KO's BOUND suffix); positives are SCREENER-DIRECTIONAL. `--lang ko` is REFUSED by the builder (owner directive · byte-frozen lane).

Emits (reproducible): the phase-A corpus + `.sdecl_flip1.json` (gate) + `.sop_flip1.json` (operator-alive control) + `.scpt_flip1.json` (phase-B DV) + `.cpt_{forward,reverse,neutral}.txt` (phase-B CPT arms).

## Pre-registered protocol — frozen bars, sequential early-kill

**Phase A** — `anima-py train` on S_op+S_decl (pool GPU). ⓒ sweep step budget as a **capability gate** (600 vs 6000 lesson), NEVER pick val_CE minimum (collapsed-model trap · valce-minimum). Positive control **G-ALIVE**: S_op flip1 (operator supervised) must reach ≥ 0.90.

**Phase-A GATE (kill-criterion)**: measure **S_decl flip1** (operator held-out-in-A):
- above chance (2AFC margin>0 rate, sign-permutation p<0.05, both seeds agree in sign) ⟹ a **co-trained bridge exists** → enter phase B.
- **at/below chance** ⟹ the co-trained bridge does not even exist → **KILL, do NOT enter phase B** (no rent waste). Frozen-first, no re-gate (burned-gate). *(Below-chance cell is first-class, not undecidable — it says the bridge is absent even with the mapping in-corpus.)*

**Phase B** (only if gate passes) — `anima-py train --init phaseA.clm` CPT on S_cpt **declaration-only** (operator 0× for those stems). Base-before is mandatory (corpus-py-1 (B)): S_cpt flip1 BEFORE must be chance. Judge `anima-py evaluate --xbind`: S_cpt flip1 after → Δ.

**Controls (frozen · ≥2):**
- (a) **no-CPT** arm — phaseA.clm unchanged.
- (b) **polarity-REVERSE-CPT** arm — same stems, OPPOSITE-polarity declaration. The answer must **TRACK the planted value**: forward and reverse must give OPPOSITE answers. **forward==reverse ⟹ cache/spillover ⟹ INVALID** (this is the H_9327 LIE test in constructive form).
- (c) **length/capacity-matched neutral-CPT** arm — same #lines, same template, non-polar balanced answer (control-must-match-mediating-covariate).

## Pre-registered verdict (both signs terminal-grade)

| verdict | condition | meaning |
|---|---|---|
| 🟢 **weight-lane runtime bridge** | S_cpt flip1 after tracks the planted polarity, reverse-arm flips, above chance BOTH seeds | **FIRST demonstration** — the wall is natural-data supply (merges H_9304) |
| 🔴 **W_wt terminal** | even strongest synthetic forcing → operator frozen at train-time (S_cpt flip1 unmoved / forward==reverse) | W_wt is terminal too → V5 reopen (attention substrate) is the honest end |
| ⛔ INVALID | G-ALIVE fail (operator dead) · base-before ≠ chance · forward==reverse | instrument, not a wall |
| 💀 KILL-AT-GATE | S_decl flip1 at/below chance | co-trained bridge never formed; no phase B |

**Below-chance table (ⓓ):** every cell above includes the ≤-chance outcome explicitly. Negative/terminal claims need TOST + power calc first (n = #S_cpt stems × #surfaces; report sd/MDE).

## Feasibility / cost gate (do NOT auto-rent)

Phase-A is a **303M train**. On aiden's RTX 5070 (12GB) it is smoked for fit + step-time FIRST. If it OOMs / is infeasible on 12GB, phase A is **rent-gated (spend)** → land L4 + this instrument + this frozen prereg, and flag "phase-A needs GPU rent (cost-gate, explicit go)" with the resume point. summer is busy with V4 (do not touch). EN atoms are a phase-A prerequisite (mine via `corpus atoms --lang en`; none exists locally yet).

---

> ⬇️ This is the data-before pre-registration (frozen-first evidence). Any verdict below this line is read through these frozen bars.

## ⏳ PHASE-A FEASIBILITY — CONFIRMED FEASIBLE on aiden (NOT rent-gated · 2026-07-16)

From-scratch smoke on aiden RTX 5070 (12GB), the flagship arch (`--d 3784 --L 4 --e0 2 --emax 3`):
- **params: 345,664,875 (345.7M)** — GPU preflight `cuda free=11.3/11.5 GiB — ok`; forward+backward+optimizer ran without OOM.
- 8 steps CE 5.78→1.88, val_CE 1.15 DESCENT; **~0.18 s/step** (bs4/seq64) ⟹ a 6000-step phase-A ≈ **18 min**. Well within aiden; **NO rent needed.**
- (The 176MB c34 `.clm` stores only active/quantised experts; the trained model is the full 345M.)

**Instrument verified** (`corpus xbind --bridge-split` smoke): arm disjointness, S_decl/S_cpt 0-operator-exposure strata confirmed, forward≠reverse CPT, gate/DV/control manifests emitted.

**Remaining prerequisites for a REAL phase-A run** (not blockers, just not-yet-built):
1. **EN atoms file** — none exists locally; mine via `anima-py corpus atoms --lang en <lexicon> --corpus <en>` (the builder's G-SUBSTR word-boundary gate applies · corpus-py-1 (G)).
2. Run via the proper `anima-py` install (NOT an ad-hoc PYTHONPATH — a path-order artifact shadows `core/serialize.py` with `cli/serialize.py`, breaking `.clm` write; the pip launcher resolves this).

**Resume point**: `corpus atoms --lang en` → `corpus xbind --bridge-split --atoms <en_atoms> --lang en --out A.txt` → `anima-py train --d 3784 --L 4 --e0 2 --emax 3 --corpus A.txt --steps 6000 --out phaseA.clm` (aiden GPU) → measure `A.txt.sop_flip1.json` (G-ALIVE ≥0.90) then the **phase-A GATE** `A.txt.sdecl_flip1.json` (above chance? → phase B; else KILL). Phase B: `train --init phaseA.clm --corpus A.txt.cpt_{forward,reverse,neutral}.txt` → `evaluate --xbind A.txt.scpt_flip1.json`.
