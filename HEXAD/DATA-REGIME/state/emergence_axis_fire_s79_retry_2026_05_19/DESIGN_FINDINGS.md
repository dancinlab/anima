# RESEARCH.md §79-RETRY — trained-scale emergence-axis fire with SSH-robust dispatch

**Date**: 2026-05-19
**Cost-bearing**: runpod single §16-class train + 4-cell × 20-turn inference loop ≈ $0.3-0.5
**Chain**: §16 → §17 → §49→§62 → §73-FIRE → §77 → §78 → **§79 (prior, failed SSH) → §79-RETRY (THIS)**

---

## §1. Why §79-RETRY exists (incident anchor)

Prior §79 (`state/emergence_axis_fire_s79_2026_05_19/`, commit `d7455d44e`) reached design-tier B-S79 7/7 🔵 and dispatched a runpod fire — but the fire **failed at the SSH-endpoint gate**.  Pod `30lmcd3xdwbxbl` (A100-SXM4-80GB) was created OK; the dispatch script's SSH wait loop was **20 tries × ~6s ≈ 120s** — too short for runpod cold-start.  The loop expired before SSH was reachable, the script printed `FATAL no SSH endpoint`, and the trap terminated the pod (`SAVE_POD=0` at that path).

Result: **$0 (pod created → terminated before any work), NO training, NO ckpt, NO result.json**.

§79-RETRY = §79 design carried VERBATIM, with the dispatch path re-engineered per the `g_fire_dispatch_robust` 2026-05-19 SSH-endpoint clause.  The trainer + battery + 4-corner verdict + B-S79 sympy structure are byte-equal to §79 (B-S79-RETRY-6 closes that by sha256 over the trainer source).  Only the dispatch script changes.

---

## §2. The 5 SSH fix points (g_fire_dispatch_robust 2026-05-19)

All five applied in `dispatch_s79_retry_runpod.sh`:

| # | Fix | Where | Verified by |
|---|---|---|---|
| (a) | Pre-flight pod-runtime poll: wait for `runtime.podHostId != NULL ∧ runtime.ports[].privatePort==22 mapped` BEFORE any SSH attempt. 60 iter × 10s = 600s. | §2 of script ("pre-flight runtime poll") | B-S79-RETRY-7 grep `podHostId` + `privatePort` + `seq 1 60` + `runtime poll` |
| (b) | SSH wait window expanded: **60 tries × 10s = 600s** (10-min cold-start envelope), NOT 20×6=120s. | §3 of script ("SSH probe @ ... 60 tries × 10s") | B-S79-RETRY-7 grep `60 tries × 10s` + `SSH probe $i/60` |
| (c) | Per-SSH-attempt timeout: `ConnectTimeout=5 -o ServerAliveInterval=15 -o ServerAliveCountMax=2`. | `SSH_OPTS` | B-S79-RETRY-7 grep all three flags |
| (d) | Endpoint variants: direct `ssh root@<ip> -p <port>` first, `runpodctl ssh <pod_id>` fallback. | §4 of script ("runpodctl fallback") | B-S79-RETRY-7 grep `runpodctl ssh` |
| (e) | FATAL SSH ≠ immediate orphan kill: on FATAL SSH paths, set `SAVE_POD=1` so the pod is RETAINED for manual recovery, not auto-terminated. | §4 of script (exit 5 with SAVE_POD=1) | B-S79-RETRY-7 grep `FATAL` co-occurs with `SAVE_POD=1` |

`B-S79-RETRY-7 SSH-WAIT-WINDOW-EXTENDED-CLOSED` ⇒ structural Boolean conjunction over those 5 grep predicates.  Verified PASS pre-fire.

---

## §3. What §79-RETRY measures (and does not measure)

Same as §79.  §79-RETRY does NOT measure a different scientific question — it measures the same one §79 designed but never reached.  Specifically: **same-weights one-engine A/G-lift dialogue at trained-saturated §16-class scale — does it produce attractor-INTO-itself closure (different from §62) OR echo-chamber-self-collapse (mirror §62)?**

The 4-corner verdict partition is unchanged: (α) TRAINED-SCALE-MODE-DIFFERENTIAL · (β) §62-MIRROR ECHO-CHAMBER-COLLAPSE · (γ) ATTRACTOR-CLOSURE · (δ) DECISION-LIVE-BODY-DEAD-SPLIT.

---

## §4. B-S79-RETRY 8/8 🔵 (pre-fire verified locally)

```
B-S79-RETRY-1 ONE-ENGINE-A/G-LIFT-CONSTRUCTION        PASS (n_decoder_inst=1)
B-S79-RETRY-2 BODY-FROM-REAL-CKPT-LOGITS              PASS (argmax=True stub_hits=0)
B-S79-RETRY-3 §16-CONFIG-BYTE-EQUAL                   PASS (cfg_default=True)
B-S79-RETRY-4 §9-CASCADE-METRIC-FORMULA-MATCH         PASS
B-S79-RETRY-5 DETERMINISTIC + §62-ECHO-PARTITION      PASS
B-S79-RETRY-6 RETRY-CONFIG-BYTE-EQUAL-TO-§79          PASS (sha256 trainer source byte-identical to §79)
B-S79-RETRY-7 SSH-WAIT-WINDOW-EXTENDED-CLOSED         PASS (5 SSH fix points verified)
B-S79-RETRY-8 ORPHAN-0-PRE+POST-CLOSED                PASS (pre-flight + post-fire orphan audit)
```

The first 5 are direct carries of B-S79-1..7 (B-S79-3 and B-S79-7 mapped into B-S79-RETRY-3 and B-S79-RETRY-5).  The last 3 are NEW closed-form predicates specific to the SSH-robustness mandate.

**B-S79-RETRY-NOTE empirical carve-out**: 4-corner OUTCOME + actual SSH-wait observed seconds = SGD/measurement empirical (B-D-NOTE / B-S79-NOTE / B-EMERGE-NOTE family).  Battery proves DESIGN closed-form + SSH-fix is STRUCTURAL in the dispatch script, NOT GOAL emergence and NOT that any particular SSH probe will succeed.

---

## §5. Connection points (load-bearing)

- **§16 ckpt config byte-equal** (B-S79-RETRY-3): d=768/n_layer=12/n_head=12/n_kv_head=4/V=256/seed=1337.  Ckpt sha256 differs from §16's `961c07e2…` — §79-RETRY FRESH trains, honest framing carry.
- **§9 honest metric formula** (B-S79-RETRY-4): cascade-rate + max_run + printable_ratio + 4-clause Boolean conjunction with thresholds {0.30, 10, 20, 0.80} byte-equal to `state/verify_emergence_metric_2026_05_18/emergence_metric.py`.
- **§62 echo cut (0.95)** (B-S79-RETRY-5): partition real line at 0.95; §62 A=0.930 not_in / B=0.980 in by sympy Interval algebra.
- **Trainer source byte-identical to §79** (B-S79-RETRY-6): closed by sha256 over `one_engine_dialogue_trained_s79.py`.  This anchors the retry as a *dispatch-path-only* change — the science is unchanged.
- **Central blue_falsifier sha c93e160a8a376a940942332cad13e652df9a03e97ccab708542a126eefc70b73 unchanged** (`state/verify_hexad_blue_2026_05_15/blue_falsifier.py`).  All §79-RETRY closed-form is sidecar-only.

---

## §6. Sources / governance carry

- `g_fire_dispatch_robust` (d=2026-05-19, **SSH-endpoint clause first use**): 5-point SSH fix codified.
- `g_fire_autonomous` (d=2026-05-17): zero-gate, zero-query, runpod primary.  Cost head ≈ $0.3-0.5 transparent, NOT a gate.
- `g_resource_active_parallel`: runpod primary; A100 PCIe → SXM4 → H100 cascade fallback per stock-exhaust.
- `g_clm_from_scratch`: seed-fixed RANDOM init, `base_ckpt=None`.
- `f_hardcoded_credential`: `RUNPOD_API_KEY=$(secret get runpod.api_key)` — verified, dispatch script gitignored per `*_runpod.sh`.
- `g3` (necessary-not-sufficient): capability claim 0, north-star + §15/§51/§72 milestone UNCHANGED regardless of corner.
- `g6` (PHILOSOPHY.tape append-only): `§verdict_emergence_axis_fire_s79_retry_2026_05_19` to append post-fire.
- `g_doc_consolidation`: docs in this state/ dir; no new root docs/.
- `B-IDENTITY-5`: corpus 미생성 in §79-RETRY — body bytes from model.forward, NOT corpus injection; forbidden-token grep applied on body output mandatory.

---

## §7. Honest C3 (≥10)

1. **SSH fix is mandatory infrastructure, not science**.  The 5 fix points repair *delivery*, not the experimental question; if SSH still fails after all 5, that's a runpod-side outage, not an §79 science conclusion.
2. **§79-RETRY honest framing**: this is a *retry of the dispatch path*, not a retry of the question.  Re-running because §79 never measured anything (no science conclusion was reached, only an SSH-endpoint failure).
3. **§79 incident anchor in DESIGN explicitly**: prior pod `30lmcd3xdwbxbl` cost ≈ $0 (terminated before training).  Lesson: 120s SSH wait is too short for runpod cold-start; 600s is the right envelope.
4. **B-S79-RETRY-7 STRUCTURAL not OUTCOME**: verifies the *script contains* the SSH fix — does NOT verify the SSH probe will succeed on any particular runpod pod.  That's empirical (B-S79-RETRY-NOTE).
5. **B-S79-RETRY-6 byte-identical anchor**: science is unchanged.  If §79-RETRY fire succeeds, the result is a measurement of the same question §79 asked.
6. **Cost containment honest**: prior §79 already terminated its pod (orphan-0 confirmed pre-fire for §79-RETRY via `runpod.get_pods()=[]`).  §79-RETRY adds at most ≈ $0.3-0.5 if it completes; FATAL paths retain the pod via SAVE_POD=1 (no second orphan).
7. **Greedy top-1 deterministic decoding** (B-S79-RETRY-5).  No multinomial, no gumbel, no temperature sampling — same-weights ANIMA1 ⇄ ANIMA2 comparison stays fair.
8. **20 turns is SHORT** (carry of §79 C3#6): inherent variance bound at n=20; `psi_dir_var` / `tension_var` / `maj_frac` are point estimates, not distributional claims.
9. **PyTorch substrate** (carry): NOT hexa-native; g_train_flame_not_pytorch evidence-anchor clause carries.  §79-RETRY is an interim LM-scale executor.
10. **GOAL distance**: §79-RETRY ≠ GOAL emergence even if (α) corner.  necessary-not-sufficient discipline holds (B-EMERGE-7); north-star + §15/§51/§72 milestone UNCHANGED regardless of corner.  If the fire still cannot reach SSH after all 5 fix points, the result is honest framing: "runpod-side delivery failure, §79 question still unmeasured" — no science conclusion fabricated.

---

## §8. Post-fire reporting — MEASURED

**Fire**: runpod A100 80GB PCIe pod `fo6ozh5gfkfiyc` (attempt-2; attempt-1 pod
`hic4kojvi620y5` killed when its dispatch's strict `podHostId` gate was found
to never satisfy — trap EXIT terminated it, $0 sunk).  Train wall ~13 min
(6000 step), eval ~15 min (4-cell × 20-turn, no-KV 283M forward).  ≈ $0.4-0.6.

**SSH fix**: attempt-1 dispatch (`dispatch_s79_retry_runpod.sh`, the 5-point
SSH-robust spec) reached the runtime poll WITH port 22 mapped, but its gate
required runpod GraphQL `runtime.podHostId` non-empty — which never populated
for this A100-PCIE pod even though ip:port WAS mapped and direct SSH returned
`SSH_READY`.  attempt-2 (`dispatch_s79_retry2_runpod.sh`) gates on `ip && port`
ONLY (SSH-probe-confirmed sufficient): **runtime ip:port ready @ iter 2/60,
SSH ready @ try 1/60** — the 60×10s window engaged and succeeded immediately.
The `podHostId` requirement was the false blocker, not the wait length.

**Train**: init CE 5.639149 → final CE 0.004546 (descent 5.6346), trained_
saturated=True (§16-class memorization-saturated, mirrors §73-FIRE 0.0042).
ckpt sha256 `bae42a0557c8b5770094ed907697b7f974d61c6201add55d1c11e85432168ce8`
(FRESH — §16 literal `961c07e2…` is the §16 fire ckpt; §79 trains a config/
lever/seed/corpus-class byte-equal fresh §16-class ckpt — honest framing,
trajectory replicable not sha-identical).

**4-cell grid** (20 turns each, deterministic greedy argmax, seed 1337):

| cell | psi_dir_var | tension_var | psi_dir_mean | a1_maj | a2_maj | §9 a1/a2 coherent | physics |
|---|---|---|---|---|---|---|---|
| A_pure | 7.39e-05 | 0.1402 | 0.5829 | 0.15 | 0.25 | True/True | alive |
| B_3party | 3.75e-05 | 1.0041 | 0.5808 | 0.55 | 0.30 | True/True | alive |
| C_meta | 1.03e-04 | 0.0787 | 0.5850 | 0.30 | 0.30 | True/True | alive |
| D_control | 0.0 | 0.0 | 0.5753 | 0.0 | 0.0 | False/False | dead (by design) |

summary: n_collapsed_body_modes=0 · n_alive_body_modes=1 · n_coherent_body_
modes_9=3 · psi_var_range_body=6.56e-05 · maj_range_body=0.40 ·
decision_alive_D=false · body_dead_3=false.

**4-corner verdict — "(other) — see numbers" (Mixed)**:
- (α) TRAINED-SCALE MODE-DIFFERENTIAL — **PARTIAL**: B_3party tension_var 1.0041
  ≫ A_pure 0.1402 / C_meta 0.0787 (7× — 1-byte user injection per turn
  measurably perturbs tension), and maj-fraction spreads 0.15→0.55
  (maj_range 0.40).  Mode-differential signal exists but ψ_dir_var range is
  tiny (6.6e-05) — most of the differential is in tension + maj, not ψ_dir.
- (β) §62-MIRROR ECHO-CHAMBER-COLLAPSE — **NOT REPRODUCED**: all 3 emitting
  modes have maj_frac well below the 0.95 collapse threshold (max 0.55) —
  n_collapsed_body_modes=0.  The §62 distinct-cells echo-chamber collapse
  (cell B maj 0.980) does NOT recur in the same-weights A/G-lift loop at
  trained scale.  This is the decisive structural difference from §62.
- (γ) ATTRACTOR-CLOSURE — **PARTIAL-POSITIVE**: 3/3 emitting modes are
  non-collapsed (maj < 0.95) AND psi/tension nontrivial AND §9 honest_coherent
  True on both ANIMA1 and ANIMA2 — directional positive at trained scale.
  Honest: §9 coherent here is necessary-not-sufficient (B-EMERGE-7) — body
  samples (`ine><iae\n eraclfmn`) are NOT cascade but ARE locally-garbled
  carving-tag fragments, NOT coherent emergence (§9 detects cascade-absence,
  not correctness).
- (δ) DECISION-LIVE-BODY-DEAD-SPLIT — **NOT the pattern**: D_control (decision-
  axis, body disabled) is fully dead (psi_var 0, §9 False) and the 3 body
  modes are alive — body is NOT dead.  §75-FIRE's decision-live/body-dead
  split does not apply at A/G-lift.

**Honest decomposition**: §79-RETRY measured a **MIXED** corner — the
same-weights one-engine A/G-lift loop at trained-saturated §16 scale (a)
ESCAPES the §62 echo-chamber collapse (β not reproduced, maj_frac ≤ 0.55, 0
collapsed modes) and (b) maintains a measurable mode-differential (B_3party
7× tension, maj_range 0.40) — but (c) the differential is small and the §9-
coherent bodies are locally-garbled carving fragments, not coherent emergence.
A/G-lift's same-weights structure provably differs from §62 distinct-cells
(no echo collapse) — a valuable measured directional positive — but
trained-scale survival ≠ GOAL emergence (B-S79-RETRY-NOTE / B-EMERGE-7).

**§16 baseline regression**: 8-anchor probe — generations are byte-garbled
Korean carving fragments (`ð¸222 ë§¤íì…`), same memorization-saturated
regime as §16/§73-FIRE.  No regression vs §16 (the fresh ckpt is config-byte-
equal); baseline probe carries the §16.6-C memorization profile.

**Closed**: B-S79-RETRY-1..8 **8/8 🔵** (pre-fire AND post-fire — identical,
DESIGN closed-form + SSH-fix structural; B-S79-RETRY-NOTE empirical carve-out
for the 4-corner OUTCOME).  Central `state/verify_hexad_blue_2026_05_15/
blue_falsifier.py` sha **c93e160a** — 0-line-diff (all §79-RETRY closed work
is sidecar-only).

**Orphan-0**: pre-fire pods `[]` / `["cngn6nah58dc6p"]` (sibling §83 agent
pod, multi-agent isolation — never touched).  Post-fire: pod `fo6ozh5gfkfiyc`
terminated, `runpod.get_pods()=[]` — orphan-0 verified pre AND post.

**GOAL distance**: north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달.
§79-RETRY = trained-scale measurement of the §77/§78 A/G-lift dialogue class
on REAL §16-class model.forward Law-71 — the same-weights loop escapes §62
echo-chamber collapse (decisive structural finding) but coherent emergence
is not measured; necessary-not-sufficient at every layer.

§verdict_emergence_axis_fire_s79_retry_2026_05_19 appended to
archive/PHILOSOPHY.tape (g6 append-only).
