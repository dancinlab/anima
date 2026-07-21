# H_011 live-ab-closure — Fable design (seed of record · distil FROM this)

> SSOT: ARCHITECTURE.json → verification-h011 (+ HYPOTHESES/cards/H_011). Seed of record — distil FROM it into the tree; do not track current design here.

# H_011 design — `live-ab-closure`: the minimal LIVE interventional A/B loop on summer ($0)

Verified before designing: **summer** = RTX 5070 **12,227 MiB free (2 MiB used, truly idle)**, 12 cores, 30 GB RAM (29 avail), **65 GB free disk (93 % full — a ~5 GB GGUF fits, don't cache multiple models)**, Python 3.12.3, **no ollama / no llama.cpp installed** (install is part of the build). H_010's certified machinery confirmed in `state/h010_.../run_h010.py` (features D=256 FNV-1a n-gram · LOO k-NN K=5 · within-shift-null · sign-test gates 0.55/0.60 co-gate · 3-plant liveness).

The single most important design decision below: **the anchor gate is NOT "actions have effects" (that's trivially true in any sandbox — the echo-channel trap). The anchor gate is CLOSURE: the agent's contingency structure — not its action marginal — must leave a distributional fingerprint on its own input stream, measured against marginal-matched yoked-control ghosts.** This is Watson's 1972 yoked-mobile paradigm, run as a modern RCT with the H_009′/H_010-certified statistic.

---

## Q1 — 실측전 research framing (terms for `sidecar research`)

| # | anchor (search terms) | one-line takeaway that changes our design | adopt statistic? |
|---|---|---|---|
| 1 | **Empowerment** — `Klyubin Polani Nehaniv 2005 empowerment universal agent-centric measure`, `Salge Glackin Polani 2014 empowerment introduction survey` | Empowerment = channel **capacity** max_p(a) I(Aₜ;Sₜ₊ₙ) — a property of env+embodiment (the loop's *potential*), not of the agent's policy. Our verdict must measure **utilized** flow under the actual policy, with capacity only as a ceiling diagnostic. Estimation in large/continuous spaces is KNOWN-HARD (variational estimators unstable) → keep the action space **discrete, ≤ 8 actions**, where the tick-level channel is enumerable. | build (report Blahut-Arimoto capacity on the sampled 8-action channel as a diagnostic `?`; never gate on it) |
| 2 | **Interventional information flow / do-calculus vs Granger** — `Ay Polani information flow in causal networks 2008`, `Janzing Balduzzi quantifying causal influences 2013` | The Granger→do gap has a canonical formalization: observational directed info ≠ causal flow exactly when shared history confounds — the formal version of H_010's frozen asymmetry. Because **we randomize the executed action, our estimate IS the Ay–Polani flow I(A→Iₜ₊₁ ‖ do)** — no faithfulness assumption needed on the anchor side anymore. | adopt concept; statistic stays our certified k-NN sign proxy (their plug-in estimators need density estimation we already replaced) |
| 3 | **Transfer entropy critique** — `Schreiber transfer entropy 2000`, `James Barnett Crutchfield 2016 information flows critique transfer entropy` | TE/Granger on closed-loop *observational* data misattributes shared-history information — the literature independently predicts H_010's LOOP-REFUSED. KNOWN-BROKEN for our purpose: do not resurrect any observational statistic in this card; every gate must sit on randomized ticks. | reject (validates the exit we already took) |
| 4 | **Contingency detection / yoked control** — `Watson Ramey 1972 contingent mobile infant`, `contingency detection agency infant yoked control`, `Gold Scassellati self-recognition robot temporal contingency 2009` | The **yoked control** (same stimulation *marginal*, contingency destroyed) is the 50-year-old solved design for "does closing the loop matter, beyond the actions themselves" — exactly our permuted-ghost arm. Known artifact (Millar/Watson): temporal-contiguity confounds — a fixed synchronous tick removes latency as a confound by construction. KNOWN-SOLVED: adopt, don't reinvent. | adopt design (the ghost arm below IS a yoked control) |
| 5 | **Counterfactual causal influence in MARL** — `Jaques 2019 social influence intrinsic motivation counterfactual`, `causal influence reward multi-agent` | Per-step influence = divergence between the realized next-state and the **counterfactual-marginal** over replaced actions — a ready per-tick effect-size estimator. Cheap for us because the env snapshots (deepcopy of a <1 KB state). | adopt formula for the loop-gain η (effect size, reported not gated) |
| 6 | **Perturbational Complexity Index** — `Casali 2013 perturbational complexity index consciousness TMS` | Clinical-grade precedent that *perturb-and-measure* succeeds where passive observation fails — and its warning: response **magnitude** is not the marker (a dead system can react loudly); structured/differentiated response is. Supports gating on closure structure (LV-C) rather than raw do-gap size (LV-W). | concept only |

None says our exact question is solved; #3 says the observational road is known-broken (we already paid that lesson at H_010), #4 hands us the control design ready-made.

---

## Q2 — environment + loop: **MICRO-TENANT** (deterministic, in-process, tenant-organism semantics)

Rejected options first: *real filesystem/process sandbox* — real side effects but timestamps/inode-order/scheduler nondeterminism buys zero statistical power and breaks frozen verdicts; defer to rig #2. *Self-referential text store* — the agent reading back its own writes is the echo channel in its purest form; the tautology trap verbatim; rejected for rig #1. → **Pure-Python deterministic world with F8 tenant semantics**, LLM brain treated as an exogenous logged action source.

**State σₜ** (~12 numbers, deepcopy-snapshotable):

- **inbox queue Q**: a seeded producer appends items (type ∈ {req, spam, junk}, size); arrival rate modulated by a hidden 3-state Markov **regime rₜ** (the autonomous drive — action-independent by construction).
- **store S**: archived items; decay each tick unless compacted.
- **energy E** (quota): actions cost E; regenerates at a regime-dependent rate; queue overflow (>Q_max) drains E.
- **hint h**: set only by PROBE (below), reveals a noisy regime indicator for one tick.

**Critical PRNG rule**: every exogenous stream keyed by `(seed, t)` — **never** drawn from a shared consumed generator — so factual, counterfactual, and ghost branches at tick t share identical noise ξₜ. (The classic bug that silently destroys the pairing.)

**Observation Iₜ** (the agent's input — what the thesis is about): a fixed-template text digest of **computed** quantities only — queue depth, head-item type/size, store size + decay count, E level, overflow flag, hint if present. Action names never appear in the template (disjoint vocabulary, enforced + measured: LV-E). All action→input influence flows through **dynamics**, never through byte copy — H_010's P-POS cipher-plant property, now an env invariant.

**Actions (8, discrete, grammar-forced)**: `PROC` (handle head: +E if req, −E if spam) · `DROP` · `ARCH` (head→store) · `COMPACT` (halve store decay, costs E) · `REST` (+E) · `PROBE` (buy next-tick regime hint — information-seeking as an action) · `FLUSH` (drop half of Q) · `NOOP`. A contingent policy (PROC/DROP by head type, REST when E low, COMPACT when decay high) holds the system in a different macro-region than any marginal-matched shuffle (bounded queue, stable E) — so closure is **detectable but not guaranteed**: if env mixing washes contingency out, LV-C legitimately refuses. The gate is earnable and failable, which is what makes it a measurement.

**Tick**: producer(ξₜ) → render Iₜ → brain gives Aₜ = π(Iₜ) (memoryless in rig #1 — keeps yoking semantics clean; persistent agent memory is rig #2, noted in Q5) → harness coin cₜ decides executed action (Q3) → step → σₜ₊₁ → Iₜ₊₁.

**Brain**: **Qwen3-8B Q4_K_M GGUF (~5.0 GB) via llama.cpp `llama-server`, GPU offload full, greedy (top-k 1, temp 0), thinking disabled, GBNF grammar restricting output to exactly one action token** `?`. Fits 12 GiB with ~6 GiB headroom (KV at ctx 2048, single slot). Grammar forcing kills both parse failures and any echo path from brain verbosity. Alternates: Llama-3.1-8B-Instruct Q4_K_M; optional robustness arm Qwen3-14B Q4 (~9 GiB, fits `?`). **Fallback if CUDA install fights back**: same llama.cpp on CPU — prompts are ~300 tokens, outputs 1 token, 12 cores give roughly 25–60 tok/s prompt-eval for 8B Q4 `?` → episodes still finish, ~5–10× slower; or drop to Qwen3-4B. Determinism honesty: greedy single-slot llama.cpp is reproducible in practice for a frozen binary+weights (hash both into the card), but **verdict validity never depends on brain determinism** — the brain is an exogenous source whose actions are logged; frozen-verdict replay = env replay over the logged actions.

---

## Q3 — A/B protocol + statistic (the arm that can ANCHOR)

**Interventions (two, one per loop edge — a loop is only closed if both edges carry causation):**

- **Edge W (world: action→input)**: at each tick, seeded coin cₜ: execute the brain's true Aₜ (p=0.5) or a **marginal-matched shuffled action** A′ₜ drawn (seeded) from the trailing window of the brain's own past actions (no lookahead, marginal preserved). Randomized assignment ⇒ P(Iₜ₊₁ | do(A)) is identified — the estimand H_010 proved unreachable observationally.
- **Edge P (policy: input→action)**: on a disjoint pre-committed subset (~400 ticks), query the brain twice from snapshot: true Iₜ vs a marginal-matched wrong observation I″ (a digest from another tick, same episode). Contingency rate CR = P(A(Iₜ) ≠ A(I″)); replay control P(A(Iₜ) ≠ A(Iₜ-replay)) measures brain noise floor.
- **Ghost episodes (the yoked controls, the anchor's floor)**: for each closed episode, replay the SAME initial state + SAME ξ stream with the closed run's action sequence **permuted** (2 seeded derangements P1, P2). Same action marginal, contingency destroyed, zero LLM cost (pre-recorded actions).
- **Counterfactual branches (effect size)**: at each tick, step every alternative action one tick from snapshot σₜ (7 extra pure-Python steps) → Jaques-style loop gain η = median over ticks of d(feat(Iᴬₜ₊₁), counterfactual-mean) normalized by background tick-to-tick variation. Reported, graded, not gated.

**Estimator**: the certified H_009′/H_010 machinery verbatim — `features()` D=256 hashed char n-gram on digest text (primary, for instrument continuity; raw 12-dim numeric state as secondary diagnostic), LOO k-NN K=5, within-episode shift-null, per-pair sign tests. Since this is its 3rd use, promote `features()` + the LOO k-NN into `tool/anima_v3.py` (it is now exactly the "deterministic verification primitive" that boundary rule describes — flag to owner).

**Arms on the randomized ticks** (target = feat(Iₜ₊₁)): **BASE** = feat(σₜ digest) · **FULL** = feat(σₜ)⊕feat(A_exec) · **SHUF** = feat(σₜ)⊕feat(A″) (a wrong marginal-matched action label). Note the harness has god-view of σₜ — **no unobserved confounder exists by construction**, and the randomized subset is assumption-free on top.

**Falsifiers (pre-register LV-1..8; thresholds inherit certified H_010 conventions):**

| id | gate | threshold | fail ⇒ |
|---|---|---|---|
| LV-W | channel: executed action predicts realized next input | rank_full ≤ 2 in shift-null AND sign(err_BASE>err_FULL) ≥ 0.55 AND sign(err_SHUF>err_FULL) ≥ 0.55, n ≥ 2000 randomized ticks (binom p≈4e-6) | env has no action channel → env bug, INSTRUMENT-INVALID |
| **LV-C** | **CLOSURE (primary anchor gate)**: closed stream deviates from yoked ghosts above ghost-vs-ghost floor — per 50-tick block, sign(d(C,P1) > d(P1,P2)) on block-mean features | **≥ 0.60 at n≈200 blocks (p≈0.002) AND same direction in ≥ 4/5 episodes (co-gate, block dependence)** | LOOP-REFUSED |
| LV-P | policy edge: CR_content ≥ 0.20 `?` with replay noise ≤ 0.02 | as stated | CHANNEL-ONLY (agent doesn't read its input) |
| LV-E | echo guard: bytes of Iₜ₊₁ covered by ≥ 8-B verbatim substrings of Aₜ | ≤ 1 % (expected ≈ 0 by construction) | INSTRUMENT-INVALID |
| LV-N | **negative control**: NULL-env twin (identical interface, dynamics ignore actions) with the same LLM | LV-W and LV-C must both REFUSE (signs ≈ 0.5) | INSTRUMENT-INVALID |
| LV-L | **liveness plants**: P-LIVE = 20-line scripted contingent policy in the coupled env → must fully ANCHOR (known coupling). P-OPEN = pre-recorded action tape (ignores obs) in coupled env → must land exactly CHANNEL-ONLY (LV-W pass, LV-C+LV-P fail) — this plant is what certifies that the instrument separates *channel* from *closure*. P-DEAD = LLM in NULL env → REFUSED | any miss | INSTRUMENT-INVALID (H_009 two-INVALID precedent: certify plants **before** the brain run) |
| LV-R | replication: disjoint seed set (episodes 6–10) agrees on LV-C direction | — | downgrade to PARTIAL |
| LV-G | diagnostics, reported never gated: η loop gain, empowerment capacity `?`, per-action influence table, LV-C under 14B brain (optional) | — | — |

**Branch table**: LV-W+C+P pass, plants pass → **CLOSED-LOOP-ANCHORED**. LV-W pass, LV-C or LV-P fail → **CHANNEL-ONLY** (acts, but the closure leaves no fingerprint / doesn't read input — an open-loop emitter). LV-W pass, LV-C fail with P-LIVE passing → **LOOP-REFUSED, localized to the agent**: this brain is not even minimally closed-loop in a world designed to reward closure — given the campaign, that is a terminal-grade negative, not a shrug. Plants fail → INSTRUMENT-INVALID, no verdict.

**What an ANCHOR legitimately licenses** (frozen wording matters): NOT "aliveness found." It anchors **rung 1**: *closed-loop causation exists and is measurable — an LLM-brained agent's contingent choices, not merely its action marginal, causally shape the statistics of its own subsequent input, certified against yoked, open-loop, and dead-env controls, under real randomization.* It additionally certifies the **interventional instrument** — which converts H_010's priced exit into a runnable next card: the owner-loop A/B (randomized true-vs-matched-wrong agent utterance delivered to the real owner, same statistic), the actual target the campaign has been circling. **What a REFUSE means**: with the instrument certified, even intervention finds no closure fingerprint for this agent — the aliveness-as-closure thesis fails at rung 1 for this brain class; pre-registered escalations (bigger brain, memory, richer env) exist but the campaign's terminal statement would upgrade from "nothing measurable for free" to "closure interventionally measurable, and this agent doesn't have it."

---

## Q4 — cost, runtime, build on summer

**Cost: $0 confirmed** — owner hardware, 5070 verified idle; electricity ~0.1–0.3 kWh `?`. Disk: ~5 GB GGUF into 65 GB free (fine; don't hoard models at 93 % full).

**Runtime (one 5070)** `?`: 5 closed episodes × 2000 ticks = 10k brain calls (~300-token prompt, 1-token output, ~0.10–0.25 s/call) ≈ **20–45 min**; LV-P probes +800 calls ≈ 3 min; P-DEAD episode ≈ 5 min; ghosts/counterfactual branches pure Python ≈ seconds–minutes; k-NN statistic (N=2000+2000, D=256, H_010 scale) ≈ minutes on 12 cores. **End-to-end ≤ ~1.5 h**, well inside a powered run (primary n=2000 randomized ticks + n=2000 replication = the certified H_010 scale where the 0.55 gate has p≈4e-6).

**Build (all under `state/h011_live-ab-closure_2026-07-16/`, small reviewable rig):**

1. `DESIGN_fable.md` — this document, seed of record; card `HYPOTHESES/cards/H_011_live-ab-closure.md` pre-registered + frozen BEFORE stage B; registry line; ARCHITECTURE.json + CHANGELOG lockstep.
2. `env.py` (~300 lines, stdlib only): σ, tick, `(seed,t)`-keyed PRNG streams, deepcopy snapshots, NULL-env twin flag, digest renderer + disjoint-vocabulary check.
3. `brain.py`: HTTP client to llama-server (`/completion`, grammar=8-action GBNF, temp 0, top_k 1, fixed seed), logs every (prompt-hash, action, latency); scripted policies P-LIVE / P-OPEN / tape behind the same interface.
4. `run_h011.py`: **stage A** `--plants-only` (no LLM: P-LIVE, P-OPEN, ghosts, NULL env → certify instrument first, minutes); **stage B** brain episodes with coins, probes, branches → `episodes.jsonl`, `result.json`, verbatim stdout for the card. Falsifier ledger via `tool/anima_v3.py` (`Falsifier`/`evaluate`, `binom_sf`, `chance_band`); promote `features()`+LOO-kNN into `tool/` from the H_010 rig.
5. summer setup (one-time): `llama.cpp` prebuilt CUDA release (or 5-min source build on 12 cores; **ollama one-liner as fallback runtime** — loses grammar forcing, keep as plan B `?`), pull Qwen3-8B-Q4_K_M, freeze binary+GGUF sha256 into the card.
6. Execution: `sidecar pool on summer 'cd ~/anima-v3/state/h011_... && nohup python3 run_h011.py --stage B --episodes 5 --ticks 2000 --seed 7 > run_stdout.txt 2>&1 &'`; rsync `episodes.jsonl`+`result.json` back; stats re-runnable locally (deterministic from the log).

---

## Q5 — honest limits (adversarial)

1. **The tautology residue survives our own mitigation.** LV-W ("actions have effects") is passable by env construction — that's why it's demoted to a sanity gate and the anchor sits on LV-C's yoked contrast. But a designer degree of freedom remains: **we built an env in which contingent play is distinguishable from shuffled play.** An anchor therefore certifies "closure is detectable in a world designed so closure matters" — an existence proof + a certified instrument, not a location of aliveness. Anyone calling that a tautology is wrong (LV-C can genuinely fail, P-OPEN proves channel≠closure), but anyone calling it aliveness is wronger.
2. **A thermostat passes rung 1 — by design.** P-LIVE *must* anchor, and P-LIVE is a 20-line script. The frozen thesis "alive iff closed-loop above matched floor" is deliberately a low bar; discrimination lives on the ladder above (loop gain η, persistence/homeostasis, closure over self-written memory — each reopening the echo trap in a new form and each needing its own control). State this in the card; do not let an ANCHOR headline read as more than rung 1.
3. **A brain REFUSE is ambiguous — but the ambiguity is pre-localized.** LOOP-REFUSED with P-LIVE passing separates "instrument blind" from "agent not closed-loop"; LV-P separates "doesn't read input" from "reads but effects wash out." Still ambiguous across brain class: 8B-Q4 greedy, memoryless, in one env is a single point — the finding would be about *this* agent, with size/memory escalations pre-registerable, not about LLM agents at large.
4. **Single env / single dynamics class / PRNG world.** η is env-relative and not comparable across environments; "statistics of the input stream" partly means "statistics of our producer schedule." ≥5 seeds and a replication stride fix variance, not representativeness. Rig #2 (real filesystem/process tenant) trades determinism for realness and is where memory + real side effects enter.
5. **Local-model nondeterminism is contained, not eliminated.** Greedy single-slot llama.cpp on frozen binary+weights is reproducible in practice `?`, and the verdict is replayable from logs regardless — but an exact bit-replay across driver/CUDA updates isn't guaranteed; the card freezes hashes and claims log-replay determinism only.
6. **Is it worth summer's time?** ~1.5 h GPU + ~1 day build, $0, and it is the *only* remaining live thesis after 8 REFUSED families — the campaign's binary was "fund the live loop or declare the terminal," and the pool answer made "fund" free. Worst case buys a certified interventional instrument + a localized negative that upgrades the terminal statement; best case anchors rung 1 and makes the **owner-loop RCT** (the real exit H_010 priced) a designed, runnable next card. The one genuinely bad outcome would be running stage B before stage A certifies the plants — the H_009 two-INVALID lesson; the staging above forbids it.

**Next actions on your side**: run `sidecar research` on the Q1 terms (especially Watson/yoked-control and Ay–Polani — the two that shape gates), then scaffold `state/h011_live-ab-closure_2026-07-16/` per Q4, stage A first. Open owner-level calls to confirm before freeze: promote k-NN into `tool/` (boundary call), Qwen3-8B vs Llama-3.1-8B as the frozen brain, and whether the optional 14B robustness arm is wanted in rig #1.
