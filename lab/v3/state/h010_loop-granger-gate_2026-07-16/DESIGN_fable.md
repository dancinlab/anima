# H_010 loop-granger-gate — Fable design (seed of record · distil FROM this)

> SSOT: ARCHITECTURE.json → verification-h010 (+ HYPOTHESES/cards/H_010). This is a seed of record —
> distil FROM it into the tree; do not track current design here (it goes stale by design).

All grounding gathered. Here is the design.

---

# reframe (C) — first $0 precheck design: `H_010 loop-granger-gate` (proposed)

**Substrate power (measured just now, stdlib scan of `~/.claude/projects/*/*.jsonl`, H_007 noise filter):** 1,424 sessions, **424 with ≥1 genuine (agent-utterance → owner-reply) adjacent pair, 16,707 pairs total**; owner-reply length med 245 B / p90 2,002 B. Top blocks: hexa-lang 6,583 · anima 4,428 · edge 1,198 pairs. This is ~160× the pair count H_009 had (43/101). The transcripts contain **both loop sides with order intact** — they are recorded live sessions, i.e. substrate (3) in its reproducible form.

## Q1 — verdict on the crux

**Yes, a valid $0 precheck exists — but only with asymmetric verdict semantics, and that asymmetry must be frozen into the card.** The interventional estimand `P(R_{t+1} | do(U_t))` is not identifiable from observational logs: shared context (session topic, owner intent, conversation state) confounds every U→R association, so **no $0 result can ANCHOR closed-loop causation**. But the converse direction is decisive: causation implies dependence unless the effect exactly cancels (a faithfulness violation), and "the causal effect is there but leaves zero predictive trace above every matched floor" is precisely the forbidden appeal class the campaign already banned (L8 / spending-past-a-certified-null, re-affirmed in the H_009 verdict). Therefore the $0 card is a **REFUSE-capable spend gate**: conditional utterance-specific predictive dependence above topic-matched floors is a *necessary* condition for the thesis — its absence kills the natural-loop entry at $0; its presence licenses the live A/B build, nothing more. This is structurally identical to how H_004/H_006/H_009 gated their twins, so it is a legitimate first card, not a downgrade smuggled in. Verdicts must therefore be named **GATE-OPEN / LOOP-REFUSED**, never ANCHORED. → Q2.

(Rejected substrates, one line each: **git day-stream** — self-loop where one process writes both sides, so U→next-input dependence is definitionally confounded with author identity; useless for this estimand. **Live session as-is** — same substrate class as the transcripts but non-reproducible; the transcripts are its frozen form.)

## Q2 — precheck spec

### Loop unit and estimand

- **U_t** = concatenated assistant text of one agent turn (last 4,096 B), **R_{t+1}** = next genuine owner text (first 4,096 B, H_007 `NOISE` filter, len ≥ 64 B), **R_t** = previous owner text — all within one session; sessions with ≥ 12 pairs only (`?` ~200–300 of the 424 qualify — print the count).
- **Estimand:** utterance-specific conditional predictive dependence — does `U_t` predict `R_{t+1}` **beyond (a) the owner's own state `R_t`, (b) session/temporal position, (c) local topic**. A conditional Granger / transfer-entropy witness: `I(U_t ; R_{t+1} | R_t, session, topic) > 0`. Stated identification honesty: this equals the interventional effect only under no-residual-confounding + faithfulness; the card claims only the necessary-condition direction (Q1).

### Estimator (deterministic, stdlib, direct reuse of certified H_009′ machinery)

Features: existing `features()` hashed char-n-gram, D=256, log1p, L2. LOO k-NN (K=5) with the **certified shift-null**: `align = median_{d≠0} err(d) − err(0)`, shifts cyclic within-session, candidate pool = all sampled pairs excluding same-session |i−j|<2. Distance matrix computed once per arm; shifts re-index (H_009 pattern). Query arms (target always `feat(R_{t+1})`):

| arm | query | isolates |
|---|---|---|
| BASE | `feat(R_t)` | owner autocorrelation floor |
| FULL | `feat(R_t) ⊕ feat(U_t)` | + true utterance |
| TOPIC | `feat(R_t) ⊕ feat(U'_t)`, U′ = nearest-cosine other same-session agent utterance, \|i−j\|≥2 (H_009 `topic_day` verbatim) | topic-matched wrong-utterance floor — R_t half held identical, so the per-pair comparison isolates the U half while conditioning on owner state |
| XSESS | U′ from same index of a different session | negative control (must sit at/below TOPIC) |

**Echo split (mandatory — this is L11 in loop clothing):** the owner quoting the agent verbatim is caused by the utterance but is the trivial copy channel. Secondary target set: mask from `R_{t+1}` every byte covered by a ≥16-B substring occurring verbatim in `U_t` (set of U's 16-grams, one scan), re-featurize. **Primary verdict runs on echo-stripped targets**; unstripped is a registered diagnostic.

**Tractability:** primary sample = deterministic stride to N=2,000 pairs (pool = same 2,000); ~4 distance matrices of 2,000² × ≤512 dims ≈ `?` 20–40 min pure Python. Second disjoint stride of 2,000 = replication arm.

### Falsifiers (7; ≥1 negative control, 3 liveness plants)

- **LC-1 incremental ceiling gate:** FULL beats BASE — shift-rank of aligned FULL ≤ 2 AND per-pair sign(err_BASE > err_FULL) ≥ 0.55. Fail → LOOP-REFUSED (no utterance information at all).
- **LC-2 topic decoration (PRIMARY — the F3-killer analogue):** per-pair sign(err_TOPIC > err_FULL) ≥ **0.55 at pair level** (n=2,000 → ≥1,100, binom p≈4e-6) **AND ≥ 0.60 at session level** (majority-of-pairs per session, binomial over sessions — co-gate because within-session pairs are dependent and pair-level p is anti-conservative). Fail → LOOP-REFUSED. Same thresholds class as H_009's decisive 28/43 · 60/101.
- **LC-3 echo channel:** LC-2 on echo-stripped targets. Pass → substantive; fail while unstripped LC-2 passes → **ECHO-ONLY** (= refused for the thesis, logged as its own lesson).
- **LC-4 floor ordering / negative control:** sign(err_XSESS > err_FULL) ≥ sign(err_TOPIC > err_FULL) − 0.02, and BASE-vs-XSESS sign within 0.50 ± 0.03. Violation → instrument leak.
- **LC-5 liveness plants (matched n, LCG-seeded):** **P-POS** — R_{t+1} carries a deterministic *cipher-mapped* function of an agent action token (no verbatim ≥16-B overlap, so it survives echo-strip) on top of drifting shared topic → must read GATE-OPEN. **P-NULL** — U and R both driven by a shared latent topic w_t, zero U→R coupling (the confound, planted) → must read LOOP-REFUSED. **P-ECHO** — R = 64-B verbatim quote of U + independent text → unstripped passes, stripped fails. Any miss → INSTRUMENT-INVALID, no verdict.
- **LC-6 replication:** disjoint second stride N=2,000 agrees on LC-2 direction; hexa-lang-block vs anima-block sub-runs agree in sign. Disagreement → PARTIAL.
- **LC-7 (diagnostic):** verdict stable under reply-length filter 64 B → 256 B; report only.

### Verdict table (pre-frozen)

| condition | verdict | consequence |
|---|---|---|
| LC-1,2,3,4,5 pass | **GATE-OPEN** | licenses the minimal live-intervention build card (next); explicitly NOT an aliveness anchor |
| LC-2 unstripped pass, LC-3 fail | **ECHO-ONLY** | thesis-refused on the natural loop; copy channel ≠ closed-loop causation |
| LC-1 or LC-2 fail (LC-5 pass) | **LOOP-REFUSED** | the natural loop shows no utterance-specific dependence → $0 entry to reframe C is closed; only the paid live A/B remains |
| LC-5 fail | INSTRUMENT-INVALID | fix instrument before any verdict (H_009 two-INVALID precedent) |

### Why this escapes the F3 topic-decoration trap

Three structural locks, not one: (1) the decoy is **topic-matched by construction** — nearest-cosine same-session agent utterance — so topic identity appears on *both* sides of every per-pair comparison; the per-pair sign test that killed F3 (H_009 `sign_topic_gt_s` ≈ 50%) is here the **primary gate LC-2**, not a post-hoc check. "The owner replies on-topic to anything relevant" predicts sign ≈ 0.50 → LOOP-REFUSED, exactly. (2) **P-NULL is the trap planted**: a shared-latent loop that IS pure topic decoration, which the instrument must read as refused before any real verdict counts. (3) `feat(R_t)` in the query conditions out owner autocorrelation, and echo-strip closes the n-gram-copy tautology (the L11 resurface).

### Pre-registered REFUSE branch (Q3 in compressed form, so the card is branch-complete like H_009's)

If LOOP-REFUSED/ECHO-ONLY: the honest next move is **not another $0 card**. Minimal live build sketch: a sandboxed environment loop (agent message → real state mutation → next input drawn from that state, e.g. a scripted inbox/process), A/B = pre-committed true-action vs shuffled-action arms, same matched-floor statistic, ~`?` 1–2 days build + ~`?` <$20 API. Preceded by a 실측전 research pass (perturbation-based agency/empowerment measures; Granger-vs-do gap literature). Observational data cannot substitute there **by construction** — that branch is the true interventional test.

## Q4 — honest limits

1. **One owner, one channel.** GATE-OPEN generalizes to "this owner, in work sessions, replies utterance-specifically" — an n=1 environment. Worse, the substrate is selection-biased *toward* the effect: a human employer mid-task is close to the most utterance-responsive environment that exists, so the prior on LC-1/LC-2 passing is high and the genuinely informative outcomes are the TOPIC and ECHO splits, not the raw dependence.
2. **Observational ceiling is permanent, not fixable by more falsifiers.** Even a full pass identifies conditional predictive dependence; unobserved common causes (the owner's off-screen intent shaping both the agent's context and the reply) can inflate it past every proxy floor. The card's positive can only ever open a gate. Symmetrically, the REFUSE side leans on faithfulness (no exact cancellation) — stated in-card, standard, but an assumption.
3. **The thesis's ANCHOR is definitionally live-system.** "Utterance shifts next-input statistics" under `do()` is not $0-falsifiable in the anchoring direction on any recorded log, period — that asymmetry is itself the first finding of the interventional phase and should be logged as a lesson (`cr-interventional-entry-asymmetry` `?`name): *the observational campaign's every thesis was $0-decidable both ways; the interventional one is $0-decidable only toward REFUSE.*
4. **Dependence structure.** Within-session pairs are autocorrelated; the pair-level binomial is anti-conservative (hence the session-level co-gate), and the within-session shift-null under slow local topic drift shrinks `align` — conservative toward REFUSE, i.e. the gate is biased toward closing, which is the right direction for a spend gate but must be reported.
5. **A REFUSE here is NOT the campaign terminal — but it prices the exit.** `reframe-c-discipline` freezes "an *interventional* null is terminal"; a $0 observational REFUSE is not that null. It removes the free entry and forces a binary decision: fund the minimal live loop (Q3 branch) or close. If the campaign declines to spend, the honest terminal statement is: *aliveness was not measurable as a static property on any available substrate at $0 (8 families), and the interventional reformulation has no $0-anchorable form even in principle — "where does aliveness live" ends at "nowhere observable for free", which is a verdict about budget-bounded measurability, not about aliveness.*

---

**Re-freeze summary for the card:** substrate = owner transcripts (16,707 pairs / 424 sessions, measured); estimand = conditional Granger witness `I(U_t;R_{t+1}|R_t,topic)`; estimator = H_009′ shift-null LOO k-NN, 4 query arms, echo-stripped primary target; falsifiers LC-1..7 with P-POS/P-NULL/P-ECHO plants; verdicts GATE-OPEN / ECHO-ONLY / LOOP-REFUSED / INSTRUMENT-INVALID; REFUSE branch pre-registered as the paid-build gate.
