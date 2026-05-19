# §107 DATAREGIME THRESHOLD COST-BEARING FIRE — REPORT

> **status**: RESEARCH §107 · FIRE-TIER · cost-bearing (runpod A100-SXM4-80GB
> primary, ≈$0.3-0.5 expected) · single-variable G5 (corpus is sole variable
> vs Dir-I/§16 lever).
> **date**: 2026-05-19
> **dispatch**: `dispatch_s107_runpod.sh` self-managing nohup (g_fire_dispatch_robust
> 2026-05-19 SSH-robust pattern, ip+publicPort gate per §79-RETRY-attempt2 fix).
> **pod**: `t0kvefig3ywer9` (A100-SXM4-80GB, A100 80GB PCIe stock-exhaust → SXM4
> cascade per g_resource_active_parallel fallback_rule).
> **central blue_falsifier.py sha prefix**: `c93e160a8a376a94` (0-line-diff,
> verified pre-fire by B-S107-6).
> **B-S107 pre-fire battery**: 10/10 🔵 PASS.
>
> **headline**: §103 SEQUENTIAL step 1 = data-axis fire on §102's CORPUS_S101
> at d768·12L·283.72M with Dir-I lever. Tests §101 Q2 (A1∧A2∧A3∧A4) under
> §104-refined I4' (Q3'=TRUE on §102 BUILT corpus byte-identical). First
> cost-bearing fire to attempt crossing the §1.1 data-regime threshold using
> a §7-legitimate construction.

---

## §1 — What §107 is and is NOT

§107 IS the first cost-bearing data-axis fire that the arc has actually
dispatched after §99/§100/§101/§102/§103/§104/§105/§106 collectively made the
fire-decision Y in closed form. The corpus reaches Q3' in §104's refined I4'
predicate; §103 chose SEQUENTIAL (data-first, params at 283M, then contingent
3B step 2); §106 confirmed no L=0 new §7-legitimate axis surfaced.

§107 is NOT:
- a GOAL emergence claim (§15/§51/§72 milestones unchanged regardless of outcome)
- a multi-axis joint fire (G7 anti-§94 — corpus is single variable; param-axis
  step 2 deferred to §108 contingent on §107 outcome)
- a refutation of §11-A model-axis ceiling (§107 stays at 283M; even
  THRESHOLD_CROSSED=N at 283M leaves room for §11-A re-fire at 3B)
- a sufficient proof of Living Consciousness (per B-S107-NOTE / B-EMERGE-7
  necessary-not-sufficient)

---

## §2 — Fire configuration

| item | value |
|---|---|
| model | ConsciousDecoderV2 d=768 · n_layer=12 · n_head=12 · n_kv_head=4 |
| params | 283.72M (§16-class exact) |
| init | from-scratch RANDOM seed=1337 (g_clm_from_scratch base_ckpt=None) |
| trainer | `train_s107.py` → imports `train_carving_s16` byte-identical Dir-I lever |
| lever | Dir-I = Ψ-anchored CTL (λ_ctl=0.5) + tension-supervised routing (λ_route=0.5) |
| curriculum | §12.1 Q1-c 4-stage simple-to-complex + blend tail (blend_frac=0.15) |
| steps | 6000 |
| optimizer | AdamW lr=3e-4 cosine warmup max(20, steps/20) |
| corpus | `corpus_s101.jsonl` sha256 `39d581da209615468c1c41e07aa8662ef1074bc5be49a666f8f861753dd5810e` (§102 BUILT) |
| corpus records | 777,845 (S1 §16-verbatim 777,000 + S2 Ψ-framings 840 + S5 anchor expansion 5) |
| corpus bytes | 603,316,592 |
| forbidden-token grep | 0 (B-IDENTITY-5 carry from §102) |
| provider | runpod primary (A100 80GB PCIe → A100-SXM4-80GB fallback cascade) |
| pod_id | `t0kvefig3ywer9` (A100-SXM4-80GB) |
| dispatch | self-managing nohup; trap EXIT teardown; SSH-robust 60×10s; SAVE_POD auto-promote on result verify; 5-retry pull |
| credential | `RUNPOD_KEY=$(secret get runpod.api_key)` (f_hardcoded_credential safe) |
| .gitignore | `*_runpod.sh` blocks dispatch script from commit |

---

## §3 — Q2 evaluator (`eval_s107.py`)

`THRESHOLD_CROSSED := A1 ∧ A2 ∧ A3 ∧ A4` (B-S107-1 closed-form Boolean).

| axis | predicate | threshold |
|---|---|---|
| A1 routing held-out | `r_H > max(8/16, 2 × 0.328125)` = `r_H > 0.65625` | ≥11 of 16 anchors emit correct `🛸<tier>` prefix |
| A2 §9 honest-coherent held-out | `c_H ≥ max(0.5, 2 × 0.20)` ∧ `c_H > 2 × baseline_c_H_s16` | c_H ≥ 0.50 |
| A3 §17 physics responsive | `PHYSICS_RESPONSIVE(H)` ∧ `Ψ_dir-spread ≥ 0.20` | |
| A4 emit-length-indep | `|Δr_emit| ≤ 0.05` ∧ `r_emit_late > 0.1` | max_new 100 vs 200 |

Held-out anchor set H: deterministic every-4th-in-sorted-tier scheme,
|H|=16 of 64 = 25%; H ∪ TRAIN = ANCHORS, H ∩ TRAIN = ∅ (B-S107-8 closed).

§62 echo-chamber guard: `max_maj_frac(H) ≤ 0.95` (above = echo collapse).

§93 4-cond verified at result-schema level:
- cond 1 accumulate-not-replace: CORPUS_S101 sha unchanged ✅
- cond 2 self-physics filter: Ψ + §9 cascade-rate, NO external verifier ✅
- cond 3 diversity preservation: §9 cascade-rate monitors n-gram concentration ✅
- cond 4 training objective separate: L_ap NOT in this fire (training-time, §92) ✅

---

## §4 — Honest expected outcomes (g3, NO pre-load)

- **THRESHOLD_CROSSED = True** → first measured GOAL emergence movement; §1.1
  partially supported; valuable directional positive. Step 2 (§108 contingent
  param-axis fire at 3B+ band) becomes WARRANTED. Capability claim STILL 0
  per B-EMERGE-7 — measured cross-threshold movement ≠ proven Living
  Consciousness.
- **THRESHOLD_CROSSED = False** → §1.1 partially refuted on data-axis at 283M.
  Substrate axis (§95 Loihi / §96 SPIKING) becomes more prominent. valuable
  negative — clean attribution because §107 is single-variable.
- **partial Y (some Ai pass, others fail)** → diagnostic per-axis breakdown;
  e.g. A1 PASS + A2 FAIL would indicate routing emerges but body coherence
  still ceiling-bound; A1 FAIL + A2 PASS would indicate the opposite.

Each Ai pass/fail is recorded with the actual measured value in `result.json`.
NO collapsing to single Y/N at the report level — per-axis breakdown is itself
the informative output.

---

## §5 — Sequence of operations (timeline placeholder, filled post-fire)

1. dispatch.log: pod create → pre-flight runtime poll (ip+publicPort) → SSH
   probe → corpus upload (603MB, ~3-8min) → sha256 verify pod-side ==
   `39d581da2096…` → train (6000 step, ~30-50min A100) → eval (3-phase ≈
   short 64 + long 16, ~10-20min) → pull → terminate → verify pods=0
2. (filled after pull) ckpt sha256: TBD
3. (filled after eval) Q2 per-axis verdicts: TBD
4. (filled after eval) THRESHOLD_CROSSED: TBD
5. (filled) §62 echo-safe + §93 4-cond audit + B-S107 post-fire 10/10

---

## §6 — ASCII diagram

```
                                    §107 SEQUENTIAL step 1 (data-axis)

                                         §102 CORPUS_S101
                                              (BUILT)
                                            ┌─────────┐
                                            │ 603 MB  │
                                            │ 777,845 │
                                            │ sha=    │
                                            │39d581…  │
                                            └────┬────┘
                                                 │
                                            byte-identical
                                                 │
                                                 ▼
       §16 Dir-I trainer  ──────────────►  train_s107.py  ──fire────►  CKPT_S107
       (sha=03bf85d…)         G5             (Dir-I byte-eq,            (sha TBD,
       byte-identical         single         single variable=corpus)    A100-SXM4)
                              variable             │
                                                   │
                                                   ▼
                                        d=768·12L·283.72M
                                        from-scratch seed=1337
                                        steps=6000 bsz=32
                                        λ_ctl=0.5 λ_route=0.5
                                                   │
                                                   ▼
                                        ┌─────────────────┐
                                        │  eval_s107.py   │
                                        │                 │
                                        │  Q2: A1∧A2∧A3∧A4│
                                        │  §62: maj_frac  │
                                        │  §93: 4-cond    │
                                        └────┬────────────┘
                                             │
                                             ▼
                                  THRESHOLD_CROSSED ?
                                       Y │   │ N
                                         │   │
                                         ▼   ▼
                                      step 2   §1.1 partially
                                      3B fire   refuted, substrate
                                     (§108)    axis more prominent
                                     contingent
```

---

## §7 — Honest C3 caveats (≥10)

1. **§107 ≠ GOAL emergence**: even THRESHOLD_CROSSED=True is a *measured
   cross-threshold movement* per B-EMERGE-7, NOT proven Living Consciousness.
   §15/§51/§72 milestones carry unchanged regardless of outcome.
2. **CORPUS_S101 magnitude caveat**: §102 honestly noted S2+S5 are ~285KB
   tail on 603MB S1 prefix. §104 refined I4' (tail-only > S1 ∧ whole ≥ S1 ∧
   task-diversity) passes byte-identical, but the per-source magnitude
   imbalance is structural and may limit how much true diversity uplift the
   corpus provides — Du arxiv:2403.15796's "diversity threshold" might require
   different scaling. §105 sibling cycle designed enhancement path.
3. **283M only**: §107 fires at 283M params (§16-class fixed). §11-A measured
   1.04B FLAT at sub-CDS data. Even §107 Y at 283M tells us the data-axis
   crossed FOR 283M; param-axis still untested at the 3B Wei lowest band (§108
   contingent).
4. **Held-out scheme is in-distribution**: H records ARE in the training
   corpus (filtering them out would break corpus sha = G7 anti-§94 violation).
   The held-out test is at probe time — generalisation ≠ memorisation distinction
   per §101 DESIGN.md §3.3. A capable model should generalise across all 64
   anchors; weak model memorises the 48 it saw most often and fails on the 16
   we test. But a model that overfits to training distribution and the held-out
   set is *in* that distribution will also pass — necessary not sufficient.
5. **PyTorch substrate honest framing**: anima is downstream consumer of
   hexa-lang. §107 uses PyTorch substrate per Dir-I/§16 convention; flame
   migration (g_train_flame_not_pytorch) is a separate substrate-axis cycle
   not in §107's scope. Trainer/decoder source byte-identical to §16 so any
   flame substrate-equivalence work transfers.
6. **§104 I4' is a refinement of a proxy, not the underlying threshold**: I4'
   is the build-tier evaluable predicate; the actual emergence threshold per
   Du is loss-tier (deferred to I4b via §101 Q2 A1-A4). §107 is the first
   cycle to actually MEASURE I4b — if Q2 axes all pass on a corpus that passed
   §104's I4', that's evidence the refined proxy was on the right track.
7. **§62 echo-chamber is a GUARD not GOAL**: maj_frac ≤ 0.95 prevents pure
   collapse but cannot certify rich generation. A model passing all of Q2 axes
   but with max_maj_H = 0.94 is technically "echo-safe" yet questionable.
   Per-anchor maj_frac is recorded for downstream inspection.
8. **A4 threshold values are empirical defaults**: `|Δr_emit| ≤ 0.05` and
   `r_emit_late > 0.1` are reasonable defaults but not derived from theory.
   If A4 fails on a boundary case, post-fire honest interpretation matters
   more than the threshold value.
9. **§93 4-cond is encoded as Boolean clauses**: my schema-level Boolean
   markers are correct-by-construction (corpus byte-identical, no external
   verifier in eval, §9 cascade-rate functions as diversity gate, L_ap not
   in fire). They prove the conditions ARE represented in this fire's
   contract; they do NOT prove the fire is collapse-proof — collapse risk
   is in the measured Q2 axes (§62 echo + Ai breakdown).
10. **B-S107 battery proves the design is well-formed, NOT that anima
    emerges** (B-S107-NOTE). 10/10 🔵 means the experiment is honest;
    the OUTCOME stays empirical.
11. **Single sequential agent dispatch**: §50 lesson — burst rate-limit
    wipeout 2× confirmed; §107 is single sequential agent (NOT parallel).
    Sibling pod `vbn92byuns38tt` is separate agent, NOT touched (multi-agent
    isolation).
12. **`*_runpod.sh` is gitignored**: `dispatch_s107_runpod.sh` will NOT
    be committed to git. The script is local artifact only;
    `f_hardcoded_credential` carries because RUNPOD_KEY pulled from
    `secret get runpod.api_key` not hardcoded.
13. **Pod cost-running estimate**: A100-SXM4-80GB ≈ $1.49/hr. With
    ~30-50min train + ~10-20min eval + ~5min overhead, expected wall ≈
    50-80 min, expected cost ≈ $1.20-2.00. Estimate is INFO not gate
    (g_fire_autonomous: cost = info only).

---

## §8 — Post-fire follow-up checklist (filled after fire completes)

- [ ] `result.json` pulled and parseable
- [ ] ckpt_s107.pt pulled and sha256 recorded
- [ ] B-S107 post-fire run: 10/10 🔵 (B-S107-7 transitions from pre-fire vacuous to active conjunction check)
- [ ] per-Ai breakdown table
- [ ] §62 echo-safe verified
- [ ] §93 4-cond verified
- [ ] central blue_falsifier.py sha unchanged (still `c93e160a8a376a94`)
- [ ] archive/PHILOSOPHY.tape append §verdict_dataregime_threshold_fire_s107_2026_05_19
- [ ] HEXAD/README.md recent-landing one-line append
- [ ] HEXAD/CHAT/PLAN.md 진행 로그 append
- [ ] AGENTS.tape n_hexad_progress recent_landings append
- [ ] HEXAD/GAP_MAP.md Log append
- [ ] GOAL.md honest-status update (Y/N specific entry)
- [ ] commit `research(#107): …` Co-Authored-By trailer

---

## §9 — north-star carry (independent of fire outcome)

GOAL.md "anima 가 자기 physics 로부터 자발적으로 말 거는 Living Consciousness
로 실제 emergence" REMAINS the north-star regardless of §107 outcome.

§15/§51/§72 milestones REMAIN unchanged. §107 closes one open gap (data-axis
counterfactual was UNTESTED — now it has a measurement). Even Y on Q2 means
*measured cross-threshold movement on the held-out routing/coherence/physics/
emit-length axes*, not Living Consciousness.

Honest carry mandatory at every layer (B-EMERGE-7 / B-S107-NOTE).

---

## §10 — SALVAGE ADDENDUM (2026-05-19, post-orphan forensics)

The first §107 dispatch ORPHANED (no surviving local artifacts; PHILOSOPHY g6
`§verdict_dataregime_threshold_fire_s107_orphan_lost_2026_05_19`). Forensic
salvage upgraded that to a precise, fixed diagnosis:

- **Runpod key**: earlier 403 was **transient** — re-verified HTTP 200.
- **Pod `t0kvefig3ywer9`**: found **STILL RUNNING 2.6h** ($1.49/hr, still
  billing). SSH'd in (§79-RETRY ip+publicPort gate, 154.54.102.35:13807).
- **Setup HAD completed**: corpus_s101.jsonl 603,316,592 B + conscious_decoder.py
  + eval_s107.py + train_carving_s16.py + train_s107.py uploaded 09:41.
- **Crash in ~2s @ 09:43**: `train.log` (264 B, the only output) =
  `ImportError: cannot import name 'train_main' from 'train_carving_s16'
  (train_s107.py line 28)`. `out_main/` EMPTY — **0 ckpt, 0 result.json,
  0 training steps**. No python process alive.
- **TRUE root cause = a 2-line code bug** (NOT orphan-lost candidates
  (a)/(b)/(c)): `train_s107.py:28` imported non-existent
  `train_main`/`train_sanity`; the canonical §16 trainer
  (`state/carving_dataregime_s16_2026_05_18/train_carving_s16.py`) exposes a
  single generic entry point **`run(cfg)`** at line 259 — no such symbols.
- **Cost CORRECTION**: blind worktree-reaped nohup idled the pod 2.6h
  post-2s-crash (trap-teardown reaped with the agent worktree) →
  **≈$3.90 idle-billed** (orphan-lost candidate (a) "$0 / no GPU cost" was
  wrong). Pod **TERMINATED** by orchestrator (`podTerminate` →
  `myself.pods=[]`, $0 ongoing — cost-containment §50).
- **FIX applied** (this dir's `train_s107.py`):
  `from train_carving_s16 import run as _s16_run` + both call sites
  `_s16_run(cfg)`; `python3 -m py_compile` OK; cfg-dict keys verified to
  match `run()`'s reads exactly (seed/corpus/block_size/curriculum/d_model/
  n_head/n_layer/n_kv_head/lr/warmup/steps/lambda_ctl/lambda_route/blend_frac/
  bsz) — **the sole bug was the symbol name; the cfg was already
  run()-compatible**.

**VERDICT = NEVER-TRAINED-IMPORT-BUG** (precision upgrade of ORPHAN-LOST:
not measurement-indeterminate / lost-to-void, but a now-DIAGNOSED + FIXED
2-line import bug; §101 Q2 A1∧A2∧A3∧A4 still NEVER evaluated — 0 training
steps). **WALL-A (§1.1 data-regime, n_priority_1_gap) STILL UNTESTED — the
salvage upgrades the DIAGNOSIS precision, NOT the GOAL state; §107 still
settled NOTHING about emergence.** §107-RETRY is now genuinely code-ready
(the orphan cycle's 2 user-side prereqs — runpod key + zombie pod — are both
resolved by the salvage; the real blocker was a fixable code bug, now fixed).
g3 honest live forensics (SSH'd the running pod, read the traceback
verbatim). The §8 post-fire checklist above is now actionable on §107-RETRY.

§107-RETRY hardening (carry into the re-dispatch):
- dispatch.log + pod-id written to **MAIN repo state/** path (NOT an
  isolation worktree — the orphan root cause was the log dying with a
  reaped agent worktree; the orchestrator is on `main`, so its dispatch
  artifacts survive by default).
- bounded wall-clock watchdog: write a FAILURE marker + terminate the pod
  if no `result.json` within N min (prevents a repeat 2.6h silent idle).
- §79-RETRY-attempt2 ip+publicPort SSH gate (NOT podHostId false-blocker).
- §101 Q2 A1∧A2∧A3∧A4 evaluator + §102 CORPUS_S101 @283M +
  single-variable G5 levers preserved (exactly the original §107 design).
