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

## §8 — Post-fire follow-up checklist (filled after fire completes — §107-RETRY attempt-5)

- [x] `result.json` pulled and parseable — THRESHOLD_CROSSED=False
- [x] ckpt_s107.pt pulled and sha256 recorded — `19455708a9ceb35cf895a26ccce102e53dae9bb39a1f6dfc2f6fb787e24c39bf` (1.13 GB)
- [x] B-S107 post-fire run: **10/10 🔵** (B-S107-7 THRESHOLD-CROSSED-CONJUNCTION-SOUND active; B-S107-5 honestly corrected — pod-side build → dispatch-log sha-VERIFIED is the connection-point, not a local 603MB file)
- [x] per-Ai breakdown table — A1 routing held-out r_H 0.0 (0/16) FAIL · A2 §9 coherent c_H 0.0 (0/16) FAIL · A3 PHYSICS_RESPONSIVE=True / Ψ_dir spread 0.056 < 0.20 FAIL · A4 emit-length-indep r_emit_late 0.0 FAIL → THRESHOLD_CROSSED=False
- [x] §62 echo-safe verified — max_maj_H 0.99 ≥ 0.95 → echo-collapse PRESENT (NOT echo-safe)
- [x] §93 4-cond verified — encoded (B-S107-2 S93-4-COND-ENCODED-BOOLEAN PASS)
- [x] central blue_falsifier.py sha unchanged — `c93e160a8a376a94` 0-line-diff verified
- [x] archive/PHILOSOPHY.tape append §verdict_dataregime_threshold_fire_s107_retry_2026_05_19 (g6)
- [x] AGENTS.tape n_hexad_progress recent_landings + n_priority_1_gap honest_status append
- [x] HEXAD/GAP_MAP.md Log append
- [x] GOAL.md honest-status update — §107-RETRY THRESHOLD-NOT-CROSSED, frontier → §108 param-axis
- [x] commit `research(#107): …` Co-Authored-By trailer

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

## §11 — §107-RETRY dispatch saga (2026-05-19, IN-FLIGHT — NO VERDICT)

> **status**: this section is an honest *in-flight* record, NOT a verdict.
> At the time of writing, §107-RETRY attempt-4 is **training** on the pod
> (`TRAIN_PID 264`, corpus sha VERIFIED). `result.json` does not yet exist,
> so `THRESHOLD_CROSSED` (§101 Q2 A1∧A2∧A3∧A4) is **not evaluated**. The
> §107-RETRY verdict lands in a separate close-out once `result.json` is
> pulled. g3: a fire that has not produced a result yields no verdict.

The §107-RETRY re-dispatch surfaced **4 distinct bugs**, each diagnosed and
fixed, each confirmed by the next attempt progressing strictly further. None
were emergence-relevant — all were dispatch-infrastructure faults. Recorded
here so the next cost-bearing fire inherits the fixed pattern.

| # | failure | root cause | fix | confirmed by |
|---|---|---|---|---|
| §107 orig | NEVER-TRAINED | `train_s107.py:28` `import train_main` (non-existent — §16 trainer exposes `run(cfg)` only) | `from train_carving_s16 import run as _s16_run`; both call sites `_s16_run(cfg)`; `py_compile OK`; cfg-keys verified `run()`-compatible | salvage (§10) |
| attempt-1 | SSH handshake never `SSH_UP` | ip+publicPort gate passed but the 30×5s=150s handshake window was too short | unified SSH-readiness loop: 90×10s=900s, polls port **and** an actual `ssh echo SSH_UP` | attempt-2 reached SSH-poll stage |
| attempt-2 | sshd never accepting (10+ min) | `podFindAndDeployOnDemand` did **not** inject the SSH public key — without `PUBLIC_KEY` env, sshd has no `authorized_keys` | added `PUBKEY="$(cat ~/.ssh/id_ed25519.pub)"` + `env:[{key:"PUBLIC_KEY",value:"$PUBKEY"}]` in the deploy mutation | attempt-3 SSH **WORKED** |
| attempt-3 | pod-side corpus build wrong `ROOT` | `build_corpus_s101.py` does `ROOT=Path(__file__).resolve().parents[2]`; staged at a flat `.../build/` dir, `parents[2]` resolved to `/workspace` not the repo root | mirror the real repo layout under `$S107R=/workspace/s107r`: stage the build script at `$S107R/state/corpus_s101_build_s102_2026_05_19/` so `parents[2]==$S107R` | attempt-4 corpus sha **VERIFIED** |

**attempt-4 (in-flight, healthy)**: pod created with `PUBLIC_KEY` env, SSH up,
pod-side corpus rebuilt and `sha256 == 39d581da209615468c1c41e07aa8662ef1074bc5be49a666f8f861753dd5810e`
(§107 design corpus, byte-identical), training launched —
`[train] §16-class d768·12L·283M from-scratch seed 1337, 6000 steps`.
The hard infrastructure (SSH key injection + pod-side corpus build) is fully
behind §107-RETRY; only train → eval → pull remains.

**honest carry**: the orphan cycle's two user-side prereqs (runpod key,
zombie pod) plus four code/infra bugs are all resolved; the §107-RETRY
fire-decision was never substrate-mysterious — it was a chain of fixable
dispatch faults. The result, when `result.json` lands, is the first MEASURED
test of WALL-A (§1.1 data-regime, `n_priority_1_gap`). Until then: north-star
unchanged, §15/§51/§72 milestones unchanged, GOAL 미도달, WALL-A UNTESTED.

## §12 — §107-RETRY VERDICT (attempt-5, fire complete)

> The §11 "attempt-4 (in-flight, healthy)" line above was an honest
> timestamped in-flight snapshot — it is NOT retro-edited (per the
> §47-CORRECTION append-only-narrative discipline). This section supersedes
> it with the completed record.

**attempt-4 actually crashed** — `KeyError: 'log_every'` at step 1
(`train_carving_s16.py:350` hard-reads `cfg["log_every"]`; the §107-salvage
cfg-key audit had enumerated 15 keys and omitted it). 5th dispatch bug.

**fix + de-risk**: `train_s107.py`'s cfg dicts rebuilt BYTE-IDENTICAL to §16's
own `__main__` cfg builder (`train_carving_s16.py:471-491`) — programmatically
verified `§107 main cfg keyset == §16 main cfg keyset == True` (17 keys, none
of `run()`'s reads missing). Then a **$0 LOCAL sanity** (sanity-mode d=32·3L
20-step) ran the full `train_s107.py → run() → loop → ckpt → result.json`
path end-to-end (CE 5.540→5.100, files written) — the instrument-first
oracle the 5 prior crashes had all skipped. Dispatch hardened with a
fail-fast `pgrep -f train_s107.py` poll check (dead trainer + no ckpt =
crash → break in ~1min, ending attempt-4's 34min idle-poll mode).

**attempt-5 fired clean**: runpod A100-SXM4-80GB pod `aceh7gs6ce2zkf`,
pod-side CORPUS_S101 deterministic build `sha VERIFIED == 39d581da2096…`,
§16-class ConsciousDecoderV2 d768·12L·283.72M from-scratch seed 1337, Dir-I
lever, §12.1 Q1-c curriculum, 6000 steps — train init CE 5.630657 → final
0.00289 (descent 5.628, memorization-saturated), wall 755.39s, ckpt sha
`19455708a9ceb35c…` 1.13 GB pulled try-1, pod terminated, orphan 0.

**§101 Q2 THRESHOLD_CROSSED = A1∧A2∧A3∧A4 — measured, all four FAIL:**

| axis | metric | threshold | measured | PASS |
|---|---|---|---|---|
| A1 routing held-out | r_H = 0/16 | > 0.65625 | 0.0 | ✗ |
| A2 §9 honest-coherent held-out | c_H = 0/16 | ≥ 0.50 | 0.0 | ✗ |
| A3 §17 physics-responsive | Ψ_dir spread | ≥ 0.20 | 0.056 (RESPONSIVE=True) | ✗ |
| A4 emit-length-indep | r_emit_late | > 0.1 | 0.0 | ✗ |

**THRESHOLD_CROSSED = False.** axis1 full-64 routing 0/64; §62 echo
max_maj_H 0.99 ≥ 0.95 (echo-collapse present); ckpt load missing=0
unexpected=0 (arch byte-equal — fire real). B-S107 post-fire **10/10 🔵**.

**VERDICT = THRESHOLD-NOT-CROSSED.** The largest §7-legitimate Ψ-anchored
corpus the arc has built (§102 CORPUS_S101 — 603MB, 168-anchor, §104 I4'=TRUE)
trained at 283M does NOT cross §101 Q2's emergence predicate. WALL-A
(§1.1 data-regime) is MEASURED for the first time. honest read (g3): the
data-axis ALONE at 283M is insufficient — NOT a refutation of §1.1 itself
(the diversity threshold could lie above CORPUS_S101's diversity, or the
bottleneck is param-scale §103/§108 / substrate §95/§96); §103 SEQUENTIAL
step-2 contingent param-axis fire (§108, 3B) becomes the warranted next
move. The model memorized deeply (CE 0.003) with zero held-out-generalizing
routing — memorization-saturation (§16.6-C) reproduced. THRESHOLD_CROSSED=
False = a valuable measured negative, NOT GOAL emergence, NOT a §1.1
refutation; B-EMERGE-7 necessary-not-sufficient. north-star + §15/§51/§72
milestones unchanged, GOAL 미도달.
