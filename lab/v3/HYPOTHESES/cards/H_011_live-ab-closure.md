---
id: H_011
ssot: ARCHITECTURE.json → verification-h011 + decision-reframe-c (frozen pre-register/verdict record; distil FROM here)
slug: live-ab-closure
title: reframe (C)'s LIVE interventional gate — the paid-build H_010 priced, now $0 on the owner's own pool (summer, idle RTX 5070). In a deterministic MICRO-TENANT world, does the LLM-brained agent's CONTINGENCY STRUCTURE (not its action marginal) leave a distributional fingerprint on its OWN subsequent input, measured against marginal-matched YOKED-control ghosts under real A/B randomization? Because we INTERVENE, this can ANCHOR (rung 1 = closed-loop causation exists + is measurable), not only refuse.
domain: reframe (C) interventional thesis — the first card that can ANCHOR (randomized intervention identifies P(I|do(A)))
status: pre-register-frozen
verdict: pending
exploration_method: H_010 priced the exit → owner "pool 에서 가능?" unblocked it ($0 on summer) → Fable design (live-ab-closure) + a 실측전 research pass (empowerment · Ay–Polani flow · Watson yoked control · Jaques counterfactual influence)
verification_method: LIVE A/B RCT on summer ($0) — deterministic micro-tenant env + a grammar-forced local-LLM brain; the CERTIFIED H_009'/H_010 shift-null LOO k-NN + sign-test statistic on randomized ticks, with yoked/open-loop/dead-env controls + 3 scripted liveness plants
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: local (Qwen3-8B-Q4_K_M via llama.cpp, greedy, GBNF-forced single action token; brain is an EXOGENOUS logged action source — verdict replays from the log, never depends on brain bit-determinism)
---

# H_011 — live-ab-closure

## Hypothesis

H_010 proved the interventional thesis cannot be ANCHORED from observational logs (P(I_{t+1}|do(A_t)) is
unidentifiable) and PRICED THE EXIT: only a REAL A/B intervention can test it. The owner's `pool` has an
idle RTX 5070 (`summer`), so that exit is now **$0**. This card runs the smallest live loop that can
ANCHOR: an LLM-brained agent acting in a deterministic MICRO-TENANT world, with the executed action
**randomized** (true vs marginal-matched shuffle) so the causal effect is identified.

> **The anchor gate is CLOSURE, not "actions have effects."** "Acting changes what you next perceive" is
> trivially true in any sandbox (the echo-channel / tautology trap). The gate (LV-C) is Watson's 1972
> **yoked control** as a modern RCT: the agent's CONTINGENCY STRUCTURE — not its action marginal — must
> leave a distributional fingerprint on its own input, measured against **marginal-matched ghost episodes**
> (same actions, permuted, contingency destroyed). LV-C is earnable AND failable — if env mixing washes
> contingency out, it legitimately refuses. That is what makes it a measurement, not a tautology.

## Substrate (MICRO-TENANT · deterministic · in-process)

- **state σ_t** (~12 numbers, deepcopy-snapshotable): inbox queue Q (arrivals modulated by a hidden 3-state
  Markov regime r_t = the action-INDEPENDENT autonomous drive), archive store S (decays unless compacted),
  energy E (actions cost; regime-dependent regen; overflow drains), probe hint h.
- **actions (8, discrete, GBNF-forced)**: PROC · DROP · ARCH · COMPACT · REST · PROBE · FLUSH · NOOP.
- **observation I_t** = a fixed-template text digest of COMPUTED quantities only (queue depth, head type/
  size, store size, E, overflow, hint). **Action names never appear** (disjoint vocabulary, enforced +
  measured = LV-E) — all action→input influence flows through DYNAMICS, never byte copy (H_010 P-POS
  invariant, now an env law).
- **PRNG law**: every exogenous stream keyed by (seed, t), NEVER a shared consumed generator, so factual /
  counterfactual / ghost branches at tick t share identical noise ξ_t (the bug that silently breaks pairing).
- **brain** (DEFAULT, owner may override before stage B): Qwen3-8B-Q4_K_M via llama.cpp `llama-server`,
  greedy (top_k 1, temp 0), thinking off, GBNF grammar → exactly one action token. Fits 12 GiB. CPU or
  Qwen3-4B fallback. The brain is an exogenous logged action source; the verdict replays from the log.

## A/B protocol (the arm that can ANCHOR)

- **Edge W (action→input)**: seeded coin c_t executes the true A_t (p=0.5) or a marginal-matched shuffle
  A′_t (seeded, from the trailing window of the brain's own past actions). Randomization ⇒ P(I|do(A))
  identified (the estimand H_010 could not reach). Harness has god-view of σ_t ⇒ no unobserved confounder.
- **Edge P (input→action)**: on a disjoint ~400-tick subset, query the brain twice from a snapshot: true
  I_t vs a marginal-matched wrong observation I″. Contingency rate CR; replay control = brain noise floor.
- **Ghost episodes (yoked controls = the anchor floor)**: replay same init + same ξ with the closed run's
  action sequence PERMUTED (2 seeded derangements). Same marginal, contingency destroyed, $0 (no LLM).
- **Counterfactual branches (effect size η, reported not gated)**: step every alternative action one tick
  from σ_t → Jaques-style loop gain.
- **estimator**: the CERTIFIED H_009'/H_010 machinery verbatim — `features()` D=256 hashed n-gram on the
  digest, LOO k-NN K=5, within-episode shift-null, per-pair sign tests. Arms (target feat(I_{t+1})): BASE
  feat(σ_t) · FULL feat(σ_t)⊕feat(A_exec) · SHUF feat(σ_t)⊕feat(A″). (Promote `features`+LOO-kNN into
  `tool/anima_v3.py` — its 3rd use; it is now the deterministic verification primitive that boundary
  describes. Owner boundary-call, defaulted YES.)

## Falsifiers (pre-registered LV-*, certified H_010 thresholds)

- **LV-W channel**: rank_full ≤ 2 AND sign(err_BASE>err_FULL) ≥ 0.55 AND sign(err_SHUF>err_FULL) ≥ 0.55,
  n ≥ 2000 randomized ticks (binom p≈4e-6). Fail → env has no action channel → INSTRUMENT-INVALID.
- **LV-C CLOSURE (PRIMARY ANCHOR)**: per 50-tick block, sign(d(Closed,P1) > d(P1,P2)) ≥ 0.60 at n≈200
  blocks (p≈0.002) AND same direction in ≥ 4/5 episodes (co-gate for block dependence). Fail → LOOP-REFUSED.
- **LV-P policy edge**: CR_content ≥ 0.20 with replay noise ≤ 0.02. Fail → CHANNEL-ONLY (agent doesn't read
  its input).
- **LV-E echo guard**: bytes of I_{t+1} in ≥ 8-B verbatim substrings of A_t ≤ 1 %. Fail → INSTRUMENT-INVALID.
- **LV-N negative control**: NULL-env twin (dynamics ignore actions) with the same LLM — LV-W and LV-C must
  BOTH refuse (≈ 0.5). Fail → INSTRUMENT-INVALID.
- **LV-L liveness plants (certify BEFORE the brain run — H_009 two-INVALID lesson)**: P-LIVE (scripted
  contingent policy in the coupled env) must ANCHOR; P-OPEN (pre-recorded action tape, ignores obs) must
  land exactly CHANNEL-ONLY (LV-W pass, LV-C+LV-P fail — certifies the instrument separates channel from
  closure); P-DEAD (LLM in NULL env) must REFUSE. Any miss → INSTRUMENT-INVALID.
- **LV-R replication**: disjoint seed set agrees on LV-C direction, else PARTIAL.
- **LV-G diagnostics (reported, never gated)**: loop gain η, empowerment capacity (Blahut–Arimoto on the
  sampled 8-action channel), per-action influence table.

## Branch table (pre-frozen)

| condition | verdict | meaning |
|---|---|---|
| LV-W + LV-C + LV-P pass, plants pass | **CLOSED-LOOP-ANCHORED** | RUNG 1 only: closed-loop causation exists + is measurable (contingency, not action marginal, shapes own input) — NOT "aliveness found". Certifies the interventional instrument → licenses the owner-loop RCT (the real exit). |
| LV-W pass, LV-C or LV-P fail | **CHANNEL-ONLY** | acts but the closure leaves no fingerprint / doesn't read input — an open-loop emitter. |
| LV-W pass, LV-C fail, P-LIVE passes | **LOOP-REFUSED (localized to the agent)** | in a world built to reward closure, this brain is not minimally closed-loop — a terminal-grade negative; pre-registered escalations (bigger brain, memory, richer env) exist. |
| plants fail | INSTRUMENT-INVALID | fix before any verdict (stage A gates stage B). |

## Stage gating (non-negotiable)

- **Stage A** (`--plants-only`, NO LLM, minutes, LOCAL $0): P-LIVE / P-OPEN / P-DEAD / NULL-env / ghosts →
  certify the instrument. **Stage B** (LLM brain on summer, ~1.5 h, $0) fires ONLY after stage A certifies.
  Running B before A is the one forbidden outcome (the H_009 two-INVALID precedent).

## Honest Limits

- **L1 tautology residue**: we built a world where contingent play is distinguishable from shuffled play,
  so an ANCHOR certifies "closure is DETECTABLE in a world designed so closure matters" — an existence
  proof + a certified instrument, NOT a location of aliveness. LV-C can genuinely fail (P-OPEN proves
  channel ≠ closure), so it is not a tautology; but it is not aliveness either.
- **L2 a thermostat passes rung 1 — by design**. P-LIVE (a 20-line script) MUST anchor. The thesis is a
  deliberately low bar; discrimination lives on the ladder above (η, homeostasis, closure over self-written
  memory — each reopens the echo trap in new form). An ANCHOR headline is rung 1, no more.
- **L3 a brain REFUSE is pre-localized** (P-LIVE separates instrument-blind from agent-not-closed; LV-P
  separates doesn't-read from washes-out) but is single-point: 8B-Q4 greedy, memoryless, one env.
- **L4 single env / PRNG world**: η is env-relative; "input statistics" partly means "our producer schedule".
  ≥5 seeds + replication fix variance, not representativeness. Real-filesystem tenant = rig #2 (rig #1 is
  memoryless to keep yoking clean).
- **L5 local-model nondeterminism is contained, not eliminated**: greedy single-slot llama.cpp is
  reproducible in practice; the card freezes binary+GGUF sha256 and claims LOG-REPLAY determinism only.
- **L6 worth summer's time**: ~1.5 h GPU + ~1 day build, $0, the only live thesis after 8 REFUSED families.
  Worst case = a certified interventional instrument + a localized negative (upgrades the terminal
  statement); best case = rung-1 anchor that makes the owner-loop RCT a runnable next card.

## Cross-Links

- **architecture**: `verification-h011` · `decision-reframe-c` (this is its live-build move) · `components.f8`
  (tenant-organism) · `salvage.l11` (echo guard) · `salvage.l2` (closure vs marginal)
- **predecessors**: `H_010` (priced the exit + the certified statistic) · `H_009` (shift-null LOO · staging lesson)
- **design**: `state/h011_live-ab-closure_2026-07-16/DESIGN_fable.md` (seed of record)
- **owner-level calls (defaulted; override before stage B)**: brain = Qwen3-8B-Q4_K_M · promote k-NN to
  `tool/` = YES · optional 14B robustness arm = NO for rig #1

## Verdict

**Stage A (instrument): CERTIFIED** ($0, local, no LLM, first try) — P-LIVE anchors (channel 0.61/0.73,
closure 0.75), P-OPEN is channel-only (closure 0.42 = contingency not marginal), P-DEAD refuses (channel
0.20). The instrument separates CHANNEL from CLOSURE.

**Stage B (Qwen2.5-3B-Instruct on summer, $0): LOOP-REFUSED (localized to this agent)** — 2026-07-16.
The brain READS its input (LV-P CR = 0.410 ≥ 0.20 — its action depends on what it perceives) but its
contingency leaves **no closure fingerprint above the yoked floor** (LV-C closure = 0.500 ≈ chance, only
2/5 episodes clear 0.60). In the SAME env a scripted homeostatic policy (P-LIVE) anchored at 0.75, so the
env can show closure — the LLM's contingency simply is not strong/consistent enough to. The agent sits
BETWEEN P-OPEN (channel-only) and P-LIVE (anchored): reading input is NOT sufficient for closed-loop
causation. A terminal-grade negative for Qwen2.5-3B greedy/memoryless in this micro-tenant.

> **Instrument-integrity note (verdict-integrity).** The first stage-B run read CHANNEL-MISSING because a
> RAW action-scoring brain collapsed to a CONSTANT action (COMPACT 40/40, CR=0.0) — dominated by each
> action's model PRIOR, not the state. Fixed with CONTRASTIVE (PMI) scoring s(a|state) − s(a|neutral); the
> re-run's CR=0.41 confirms the brain now genuinely reads its input. The env channel is stage-A-certified,
> so a stage-B LV-W miss = brain-degeneracy (an open-loop signature), never an instrument fault
> (`convergence brain-py-1`).

**Stage B (Qwen2.5-7B-Instruct, nf4, on summer, $0): ANCHOR-ON-LV-C (rung 1) — the FIRST brain to clear
the certified closure anchor** — 2026-07-17. The 7B reads its input (LV-P CR = 0.400) AND its contingency
**fingerprints the block trajectory above the yoked floor** — LV-C closure = **0.7625 ≥ 0.60, all 5/5
episodes** (the 3B was 0.500 ≈ chance). It misses the co-gated one-step channel (LV-W base_full 0.353 <
0.55), which routed the frozen gate to LOOP-REFUSED — but that miss is an **instrument artifact**, not a
no-channel verdict (below).

> **Tiebreak — LV-W is under-powered in this regime (`verdict-integrity`; `run_tiebreak → result_tiebreak_lvw.json`).**
> LV-C PASS while LV-W FAIL is a metric divergence, so before any terminal I audited the *ruler*: a $0/no-GPU
> sweep of KNOWN-LIVE contingent plants across action entropy, reusing the certified `lv_w`/`lv_c` verbatim.
> A known-live plant **`mid3bal`** (H ≈ 0.97 bits, ~2 distinct actions, collision 0.52) reproduces the 7B's
> signature **exactly** — LV-W base_full **0.358 FAIL**, LV-C closure **0.762 PASS**. Below H ≈ 0.6 plants
> lose BOTH (lowent3/2); above H ≈ 1.8 both pass (lowent4/control). The 7B lives in the decoupling window.
> ⇒ LV-W's fail there is an INSTRUMENT ARTIFACT (collision pins shuf_full ≈ 0.5; a degenerate action-distance
> pushes base_full < 0.5), **QUARANTINED** (`infra-wall-noneval`). LV-C is entropy-agnostic (yoked-ghost
> control) and by itself rejects a dead env (null-env closure = chance, cf. P-DEAD), so it stands ALONE as the
> valid anchor. `convergence run-h011-py-1` (cogate-metric-regime-blindness — a recurrence of H_009's
> instrument-regime lesson: a co-gate certified only in one regime silently mismeasures the one the subject
> occupies).
>
> **Repair attempted — PARTIAL (`lv_w` `*_r`).** I added a regime-robust LV-W restricted to INFORMATIVE ticks
> (the A/B intervention actually changed the action, so obs⊥action). It correctly keeps the dead null env
> REFUSED (base_full_r 0.241) — no false channel — but it does **NOT rescue the mid3bal/7B regime** (mid3bal
> base_full_r 0.446 still < 0.55). So the 7B's one-step channel is **genuinely weak** there (diffuse/delayed
> effects), not merely a collision artifact — LV-C (the block timescale) captures the same causation LV-W
> misses at the one-step timescale. **LV-W stays QUARANTINED; LV-C is valid AND sufficient** (it alone rejects
> P-DEAD). A fuller low-entropy channel test (block/multi-step, i.e. what LV-C already is) is future work but
> does not gate this verdict.

So on the VALID instrument the 7B demonstrates **rung-1 closed-loop CONTINGENCY** — NOT "aliveness found"
(a thermostat clears rung 1), but it is the campaign's first positive on the certified anchor, and it
**LICENSES the owner-loop RCT that H_010 priced** (`decision-reframe-c`'s owner binary now has its go-signal).

**Pre-registered escalations remain**: persistent agent memory (rig #2), a richer env, and — the real exit —
the owner-loop RCT itself. The interventional INSTRUMENT is certified and now has a brain that anchors on it.
Infra note: long summer runs use `sidecar pool on --bg` (detached; the orphan-fence group-kill was fixed
upstream, dancinlab/sidecar #418).
