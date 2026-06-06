---
id: H_1018
slug: lapse-free-human-bar
title: When the human reference is a LAPSE-FREE pure oracle (lapse=0) on the H_964 hidden-velocity station-keeping control task, does anima's closed-loop world-model policy match the no-lapse oracle within a pre-registered tolerance band (genuine WM parity) — or fall BELOW it (so the H_1015 "above-human" was entirely the ~7% attention-lapse artifact)?
domain: cwm · cross-cutting · world-model · human-level · north-star · behavior-eval · placement · control · lapse-control · pre-register
source: H_1015 (PASS placement — anima -0.6426 ABOVE the lapsing human band [-1.1633,-1.0633], BUT the honest caveat = "above-human-because-no-lapse", NOT a general superiority claim) + CWM milestone M8 (behavior eval vs human baseline) + a_paper_significance (falsifiable hypothesis + real measurement) + a_paper_negative_ok + a_scale_honest_scope
exploration_method: E5 (human-reference task + metric) — REUSE the H_1015 env + policies + metric verbatim, change ONLY the human-proxy lapse from 0.07 to 0.00 (pure oracle), to separate genuine WM parity from the lapse artifact
verification_method: W2 (pre-registered parity falsifier — anima closed-loop WM policy vs the NO-LAPSE oracle within a frozen tolerance band) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
cross_process_byte_identical: false
llm: none
hexa_only: false
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: pre-registered (unmeasured)
scope: ONE control rung (a_scale_honest_scope · a_toy_scale_recheck). TOY $0 CPU-local numpy, no GPU. Task = the H_964 partial-observability control env (position-only obs; optimal action needs the HIDDEN velocity), metric M = mean episode return (0 = optimal). The ONLY change vs H_1015 is the human reference: a LAPSE-FREE oracle (lapse=0.00, knows velocity, always plays optimal_action) instead of the ~7%-lapsing proxy. Same N_runs/ep_per_run/seeds as H_1015 (40 runs x 60 episodes). NO live human study. NO Phi/IIT4 claim here (behavior return only), so a_phi_iit4_tool is n/a — stated explicitly. Single rung; scale-transfer UNVERIFIED. NOT a forge binary.
sister: H_1015 (the lapsing placement this caveats-out), H_972 (the bar instrument), H_964 (the WM-requiring control task), CWM M8
verdict: PENDING-MEASUREMENT
---

# H_1018 — lapse-free human bar (close the H_1015 lapse caveat)

## 0. motivation
H_1015 (PASS) placed anima's closed-loop WM policy (M = -0.6426) ABOVE the human band
[-1.1633, -1.0633] on the H_964 hidden-velocity station-keeping control task, while the reactive
single-frame baseline (-1.9237) landed below and random (-6.1249) below both. BUT H_1015 was honest
about its own caveat: the human-proxy carried a documented ~7% per-step attention lapse, and anima's
deterministic WM has no lapse — so "above-human" is really "above-human-BECAUSE-no-lapse", NOT a
general superiority claim. The unresolved question: if we remove the human's lapse entirely (a pure
oracle that always plays the velocity-informed optimal action), does anima still MATCH it? If yes,
anima has genuinely recovered the hidden state to oracle quality (clean "human-level, not beyond").
If no, the H_1015 advantage was entirely the lapse artifact and anima is human-competitive only
against a lapsing human. This H separates the two readings.

## 1. hypothesis (one falsifiable claim)
On the H_964 hidden-velocity station-keeping control task, with metric M = mean episode return and a
LAPSE-FREE human reference (the oracle optimal_action executed with lapse = 0.00, no random thrusts),
anima's closed-loop world-model policy (latent -> action) lands WITHIN a pre-registered tolerance
band around the no-lapse oracle return — i.e. anima genuinely matches the pure oracle (human-level,
not beyond), demonstrating the WM has recovered the hidden velocity to oracle quality.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-07)
**Setup:** IDENTICAL to H_1015 — H_964 control env (ODIM=2 position-only obs, NACT=4 thrusts, hidden
velocity, DRAG=1.0, reward = -||pos||, horizon T). Same WM action head (delay-embedding latent ->
action, imitation of the oracle) and REACTIVE action head (single position -> action). Same N_runs=40,
ep_per_run=60, same per-agent seeds (human=1000, random=2000, reactive=3000, anima=4000). The ONLY
change: the human reference is the LAPSE-FREE oracle (lapse=0.00) — it ALWAYS plays the
velocity-informed optimal_action, no attention lapse. We ALSO re-run the lapsing proxy (lapse=0.07,
seed 1000) to reproduce H_1015 and make the lapse contribution explicit.

Pre-registered tolerance band for parity (frozen BEFORE the run):
  Let O = the no-lapse oracle mean return, and let TOL = 0.05 (return units; ~5% of the |O|~1.0
  scale and comfortably larger than the H_1015 anima std 0.0463 and oracle-run noise). The parity
  band = [O - TOL, O + TOL]. anima matches the oracle iff anima's bootstrap-CI midpoint (anima mean)
  lies within [O - TOL, O + TOL] AND anima's CI overlaps the band (CI_lo <= O + TOL and CI_hi >=
  O - TOL). "anima below the oracle" = anima mean < O - TOL with anima CI_hi < O - TOL.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- decomposition (explicit lapse contribution): no-lapse-oracle return O, lapsing-proxy return (H_1015
  reproduction), anima return, reactive return, random return — all with mean +/- std and bootstrap CIs.
- parity test: anima mean and CI vs the no-lapse oracle parity band [O - TOL, O + TOL].
- lapse contribution = (no-lapse-oracle mean) - (lapsing-proxy mean) — the return the ~7% lapse costs
  the human; report it so the H_1015 "above-human" decomposes into lapse + any residual.

**Outcome rules (frozen BEFORE the run):**
- IF anima mean lies within [O - TOL, O + TOL] AND anima CI overlaps the band
  THEN PASS = GENUINE PARITY — anima matches the lapse-free oracle within tolerance; the WM
  has truly recovered the hidden state to oracle quality. A clean, honest "human-level (not beyond)"
  result; the H_1015 "above-human" is explained as exactly the ~7% lapse the real (no-lapse) oracle
  does not pay.
- IF anima mean < O - TOL (with anima CI_hi < O - TOL)
  THEN RED-CLOSED-NEGATIVE (a_paper_negative_ok) — anima is BELOW the no-lapse oracle; the H_1015
  "above-human" was ENTIRELY a lapse artifact; anima is human-competitive only against a lapsing
  human, NOT against a pure oracle. The gap (O - anima) is the quantified finding.
- IF anima mean > O + TOL (with anima CI_lo > O + TOL)
  THEN GREEN-PLUS (reported honestly) = anima EXCEEDS even the no-lapse oracle within this toy env
  (would indicate the imitation-trained WM head out-performs the hand-coded optimal_action on the
  return metric — a surprising but honest above-oracle result; we would scope it tightly and flag it
  as an env/oracle-suboptimality finding, not a general human-superiority claim).

## 3. honest scope
Toy, small scale (a_scale_honest_scope · a_toy_scale_recheck). Human reference = a documented oracle
(now lapse-free), NOT a live IRB human study. The control env is the H_964 toy; the bar is one
defensible operationalization. Single rung; scale-transfer to richer environments / real embodiment
UNVERIFIED. No Phi/IIT4 claim here (a_phi_iit4_tool n/a — behavior return only). NOT a forge binary;
$0 CPU-local, no GPU.

## 4. measurement + finding
PENDING-MEASUREMENT. VERDICT-GATE: TEXT tokens only until
`.verdicts/1018_lapse_free_human_bar/H_1018.txt` exists; then this section is filled honestly from the
verdict (genuine-parity / lapse-artifact closed-negative / above-oracle) and status flips to measured.

Probe: `CWM/probes/h1018_lapse_free_human_bar.py` · verdict: `.verdicts/1018_lapse_free_human_bar/H_1018.txt`

## 5. sibling / xlinks
- to [H_1015](./H_1015_human_bar_placement_control.md) (the lapsing placement this caveats-out)
- to [H_972](./H_972_human_level_or_beyond_bar.md) (the bar instrument)
- to [H_964](./H_964_latent_to_action_policy.md) (the WM-requiring control task)
- to [CWM](../CWM/CWM.md) (CWM-VERIFY · north star · M8)
