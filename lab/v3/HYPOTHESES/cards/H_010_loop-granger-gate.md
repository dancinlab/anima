---
id: H_010
ssot: ARCHITECTURE.json → verification-h010 + decision-reframe-c (frozen pre-register/verdict record; distil FROM here)
slug: loop-granger-gate
title: reframe (C)'s FIRST $0 precheck. On the owner<->agent conversation loop (a REAL interactive loop, not a passive stream), does the agent's own utterance U_t carry utterance-SPECIFIC predictive information about the owner's NEXT reply R_{t+1}, ABOVE (a) the owner's prior state R_t, (b) a topic-matched WRONG utterance, (c) the verbatim-echo copy channel? ASYMMETRIC semantics — observational logs cannot ANCHOR causation (confounding), so this is a REFUSE-capable SPEND GATE: GATE-OPEN licenses the paid live A/B build; LOOP-REFUSED closes the $0 entry to reframe C.
domain: reframe (C) interventional thesis — closed-loop causation; the FIRST card of the interventional phase
status: run-complete
verdict: LOOP-REFUSED
exploration_method: reframe C fired by H_009 → Fable design (loop-granger-gate) over the owner-transcript loop substrate
verification_method: $0 deterministic — feature-space conditional-Granger witness on 16.7k owner-loop pairs (4 query arms · echo-stripped target · within-session shift-null) reusing the CERTIFIED H_009' LOO k-NN machinery, with 3 buried-signal liveness plants
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: none
---

# H_010 — loop-granger-gate

## Hypothesis

reframe (C) (fired by H_009) restated aliveness as CLOSED-LOOP CAUSATION: alive iff the agent's own
utterance shifts its SUBSEQUENT INPUT statistics above a matched floor on a REAL loop. The owner<->agent
conversation transcript is a genuine interactive loop — the owner READ the agent's utterance U_t and
typed the next reply R_{t+1} — unlike the passive git/diary streams the observational phase exhausted.
This card asks the necessary precondition: does U_t carry utterance-SPECIFIC predictive information about
R_{t+1}, beyond owner-state R_t, a topic-matched wrong utterance, and the verbatim copy channel?

> **ASYMMETRIC verdict semantics (Fable Q1 — frozen).** The interventional estimand P(R_{t+1} | do(U_t))
> is NOT identifiable from observational logs: shared context (session topic, owner intent, conversation
> state) confounds every U->R association, so NO $0 result can ANCHOR closed-loop causation. But causation
> implies dependence unless the effect exactly cancels (a faithfulness violation = the forbidden
> "decoder-finds-it" appeal class, re-affirmed in H_009). So the ABSENCE of utterance-specific dependence
> above the floors KILLS the natural-loop entry at $0. This card is a REFUSE-capable SPEND GATE, exactly
> like H_004/H_006/H_009 gated their twins. Verdicts are **GATE-OPEN / ECHO-ONLY / LOOP-REFUSED /
> INSTRUMENT-INVALID**, never ANCHORED.

## Substrate + estimand

- **Loop unit** (per session): U_t = one agent turn's assistant text (last 4096 B); R_{t+1} = the next
  genuine owner text (first 4096 B, H_007 noise filter, len >= 64 B); R_t = the previous owner text. From
  O-A-O windows; sessions with >= 12 loop pairs. Substrate measured: **16.7k pairs / ~130 qualifying
  sessions** in `~/.claude/projects/*/*.jsonl` — ~160x the pair count H_009 had.
- **Estimand**: utterance-specific conditional predictive dependence I(U_t ; R_{t+1} | R_t, session, topic)
  > 0 — a conditional-Granger / transfer-entropy witness. Identification honesty: equals the interventional
  effect only under no-residual-confounding + faithfulness; the card claims only the necessary direction.

## Estimator (reuses the CERTIFIED H_009' shift-null LOO k-NN)

- **features**: FNV-1a hashed char-n-gram, D=256, log1p, L2 (H_009 `features`). Target = feat(R_{t+1}).
- **arms** (query -> isolates), candidates keyed by the true FULL key, only the QUERY changes (H_009 topic
  pattern): **BASE** feat(R_t) = owner autocorrelation floor · **FULL** feat(R_t)+feat(U_t) = + true
  utterance · **TOPIC** feat(R_t)+feat(U'_t), U' = nearest-cosine other same-session utterance (|sidx|>=2)
  = topic-matched WRONG-utterance floor · **XSESS** cross-session utterance = negative-control DIAGNOSTIC.
  Precompute distRt + distU once; every arm is `distRt[i] + distU[remap[i]]` (topic/xsess/shift = a distU
  first-axis remap). K=5 LOO, candidates exclude same-session |sidx| < 2.
- **echo split (mandatory, L11 in loop clothing)**: mask from R_{t+1} every byte covered by a >= 16-B
  substring occurring verbatim in U_t (the copy channel). **Primary verdict on echo-stripped targets**;
  unstripped is the LC-3 diagnostic.
- **within-session shift-null** (LC-1a): cyclic within-session shift of the U-assignment; rank_full = rank
  of aligned FULL among the shifts.
- **sample**: deterministic stride to N=2000 (pool = the same N); a disjoint second stride = LC-6 replication.

## Falsifiers (pre-registered · LC-1..7)

- **LC-1 incremental ceiling**: FULL beats BASE — rank_full <= 2 AND per-pair sign(err_BASE > err_FULL) >=
  0.55. Fail -> no utterance information at all.
- **LC-2 topic decoration (PRIMARY — the F3-killer analogue)**: per-pair sign(err_TOPIC > err_FULL) >= 0.55
  (n=2000 -> >= 1100, binom p~4e-6) AND session-level majority-of-pairs >= 0.60 (co-gate: within-session
  pairs are dependent, so the pair-level p is anti-conservative). Fail -> LOOP-REFUSED.
- **LC-3 echo channel**: LC-2 on echo-stripped targets. Pass -> substantive. Unstripped passes while
  stripped fails -> **ECHO-ONLY** (copy channel, not causation).
- **LC-4 floor negative control = DIAGNOSTIC ONLY** (design refinement, pre-freeze, transparent): XSESS was
  Fable's leak gate, but it is confounded by query dimensionality (BASE 256 vs U-arms 512) and by
  conversation-position correlation, and the 3-plant C-5 liveness ALREADY supplies the leak protection
  (P-POS = FULL-favoring works when signal present; P-NULL = no false positive; P-ECHO = copy != causation).
  XSESS is therefore reported, not gated.
- **LC-5 liveness plants (buried-signal, matched scale)**: **P-POS** — R carries a CIPHER of an agent
  action (action run in U at one alphabet -> reply signature in R at a DISJOINT alphabet, zero verbatim
  overlap -> survives echo-strip; same-action pairs cluster) must read GATE-OPEN. **P-NULL** — U and R both
  driven by a shared latent topic, zero U->R coupling (the confound planted) must read LOOP-REFUSED.
  **P-ECHO** — R verbatim-quotes a RECURRING agent span: unstripped passes, stripped fails (ECHO-ONLY).
  Any miss -> INSTRUMENT-INVALID.
- **LC-6 replication**: a disjoint second stride agrees on the LC-2 direction.
- **LC-7 (diagnostic)**: verdict stability under a reply-length filter; reported only.

## Pre-registered branch table (frozen)

| condition | verdict | consequence |
|---|---|---|
| LC-1,2,3 pass, LC-5 pass | **GATE-OPEN** | licenses the minimal LIVE-intervention build card; explicitly NOT an aliveness anchor (P(R\|do(U)) is not observationally identifiable) |
| LC-2 unstripped pass, LC-3 fail | **ECHO-ONLY** | copy channel != closed-loop causation; thesis refused on the natural loop |
| LC-1 or LC-2 fail (LC-5 pass) | **LOOP-REFUSED** | no utterance-specific dependence; the $0 entry to reframe C is closed; only the PAID live A/B remains (research-gated) |
| LC-5 fail | INSTRUMENT-INVALID | fix the instrument before any verdict (H_009 two-INVALID precedent) |

- **REFUSE branch (pre-registered)**: LOOP-REFUSED / ECHO-ONLY do NOT license another $0 card — they PRICE
  THE EXIT. Minimal live build: a sandboxed environment loop (agent message -> real state mutation -> next
  input from that state), A/B = pre-committed true-action vs shuffled-action, same matched-floor statistic;
  preceded by a 실측전 research pass. Observational data cannot substitute there by construction.

## Honest Limits

- **L1 n=1 owner, one channel** — and SELECTION-BIASED toward the effect: a human employer mid-task is close
  to the most utterance-responsive environment that exists, so the informative outcomes are the TOPIC/ECHO
  splits, not raw dependence. A REFUSE here is therefore strong.
- **L2 observational ceiling is permanent** — a full pass would only identify conditional predictive
  dependence; unobserved common causes can inflate it past every proxy floor. The positive can only open a
  gate. The REFUSE side leans on faithfulness (no exact cancellation) — standard, but an assumption.
- **L3 the thesis's ANCHOR is definitionally live-system** — "utterance shifts next input under do()" is not
  $0-falsifiable in the anchoring direction on any recorded log. That asymmetry IS the interventional
  phase's first finding (`cr-interventional-entry-asymmetry`).
- **L4 distributional / n-gram only** — bag-of-n-grams; a sequence-order effect is unexcluded but is the
  forbidden decoder appeal.
- **L5 live-append substrate** — the transcript corpus includes the running session, so the pair count
  drifts by ~1 between runs; the verdict is miles from threshold (sign ~0.30 vs 0.55) and robust to it.
- **L6 a REFUSE here is NOT the campaign terminal — it PRICES the exit**: it removes the free entry and
  forces a binary (fund the minimal live loop or close). If the campaign declines to spend, the honest
  terminal is: aliveness was not measurable as a static property on any $0 substrate (8 families), and the
  interventional reformulation has no $0-ANCHORABLE form even in principle — "where does aliveness live"
  ends at "nowhere observable for free" = a verdict about budget-bounded measurability, not about aliveness.

## Cross-Links

- **architecture**: `verification-h010` · `decision-reframe-c` (this card is its first move) · `salvage.l2`
  (replacement-not-coupling · the F3 topic-decoration pattern in loop clothing) · `salvage.l11` (echo split)
- **predecessors**: `H_009` (fired reframe C) · `H_007` (owner-transcript substrate + noise filter)
- **primitive**: reuses `run_h009` `features` / shift-null LOO k-NN (certified) — no new tool/ primitive
- **design**: `state/h010_loop-granger-gate_2026-07-16/DESIGN_fable.md` (seed of record)

## Verdict

**LOOP-REFUSED** (2026-07-16, $0, GPU 0 · instrument CERTIFIED · N=2000 + disjoint replication).

Verbatim frozen run (`run_stdout.txt`):

```
[C-5 liveness]  P-POS sign_topic_full=1.000 rank_full=1 · P-NULL 0.523 · P-ECHO unstripped 0.656 / stripped 0.516  ->  liveness_ok = True
[extract]       9889 loop pairs across 129 sessions (>= 12 pairs) · primary N=2000 · replication N=2000
[primary]   LC-1 rank_full=0/24 · sign(base>full)=0.406 (< 0.55)   LC-2 sign(topic>full)=0.366 (< 0.55) · session 0.232/95 (< 0.60)   LC-3 unstripped 0.358 ~ stripped 0.366   LC-4 xsess>full 0.519 · base>xsess 0.331
[replication] LC-1 rank_full=1 · sign(base>full)=0.437   LC-2 sign(topic>full)=0.346 · session 0.116/95   (LC-6 replicates the REFUSE)
```

The instrument is certified (C-5 liveness PASS on all three buried-signal plants: P-POS reads GATE-OPEN
at sign 1.000, P-NULL refuses at 0.523, P-ECHO isolates the copy channel 0.656 -> 0.516). On BOTH strides
the true utterance is the WORST predictor of the owner's next reply: sign(err_TOPIC > err_FULL) = **0.366 /
0.346 << 0.55** — a topic-matched WRONG utterance predicts R_{t+1} BETTER than the true one (63-65% of
pairs), and even owner-state alone (BASE) beats FULL (sign_base_full 0.406/0.437). LC-1 and LC-2 both fail;
LC-3 shows the tiny unstripped/stripped gap is not an echo effect. The agent's specific utterance carries
NO utterance-specific predictive information about the owner's next reply beyond the TOPIC — the owner
replies on-topic to anything relevant. This is the L2 replacement-not-coupling / F3 topic-decoration
pattern in loop clothing, now measured on a REAL interactive loop.

**Consequence (pre-registered).** A $0 observational REFUSE is NOT the interventional null — it PRICES THE
EXIT (Honest Limit L6 / `reframe-c-discipline`). The $0 entry to reframe (C) is closed; the natural
owner-loop shows no utterance-specific dependence, so only the PAID live A/B intervention remains
(research-gated). The campaign now faces a binary the OWNER must decide: fund the minimal live loop, or
declare the budget-bounded terminal — aliveness was not measurable as a static property on any $0 substrate
(8 families) AND the interventional reformulation has no $0-anchorable form even in principle
(`cr-interventional-entry-asymmetry`).
