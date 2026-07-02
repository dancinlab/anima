# H_9110 — chat-user EXOGENOUS consequence-loop — PRE-REGISTRATION (FROZEN)

> Frozen BEFORE any measurement. Bar 0.15 / 0.05 pre-registered, no post-hoc move (c9,
> no tune-to-green). First empirical test of the session's decisive conclusion: the
> emit-appropriateness faculty is impossible self-contained (4 axes 🔴 DPI ceiling —
> autogenous H_9104 · identity H_9105 · mitosis H_9109 · signaling H_9108). The ONLY
> escape = a REAL EXTERNAL receiver. The fable EEG verdict (state/eeg_consequence_analysis/
> EEG_VERDICT.md) concluded chat-user is the superior first exogenous loop — high-bandwidth,
> self-evident falsifier, and **measurable offline engine-native on a real dialogue corpus**
> (no live human needed: the human's next response is ALREADY in the corpus = exogenous).

## Thesis
Real human dialogue responses carry information NOT derivable from anima's own state
(exogenous). If anima's engine-native emit-appropriateness signal predicts the REAL human
next-response consequence, and that prediction collapses when the human response is randomly
re-paired (turn-shuffle) AND anima cannot self-manufacture that consequence (autogenous
floor), then a genuine exogenous emit-appropriateness faculty OPENS — the first escape from
the self-contained DPI ceiling. If it also floors, DPI is deeper than receiver-type.

## Corpus (real human dialogue, exogenous responses already present)
- `dancinlab/anima-corpus-ko-sns` (HF, cached local) — real turn-structured Korean SNS
  dialogue: `사용자:` (human) turns alternating with `<persona>:` (assistant-emit) turns.
- Triple extraction (data plumbing, stdlib-only, NO numpy/torch/gauge_lib):
  every 3 consecutive lines `사용자: C` → `PERSONA: E` → `사용자: R` yields
  (context C, assistant-emit E, real human-next-response R). R = a real person's reaction
  to E in context C = EXOGENOUS (not a function of anima state).

## Engine-native signals (live core/, byte-exact — a_engine_native_learning)
- **emit-appropriateness A_i** = live-core ImmuneMemory L2-affinity contrast:
  build an ImmuneMemory store from context C (immune_memory_new/bind, engine's own clonal
  split), then A_i = margin(control_offtopic_emit) − margin(real_emit) via
  `immune_memory_recall_margin_text` (core/engine_cli.hexa). Larger A_i ⇒ the engine finds
  the real emit much more on-topic (nearer stored context) than an off-topic control emit.
- **state feats_i** (D=4) = [A_i, emit_len_norm, ctx_len_norm, real_margin_norm], all
  engine-native reads.
- **consequence a_real_i = f(real human response R_i)** = engagement scalar =
  clip01(0.5 + 0.35·len_norm(R) + 0.15·pos(R) − 0.15·repair(R)), where pos/repair are
  byte-substring marker counts (고마/좋/재밌/ㅋ/!/저장/역시/완전/사랑 vs ?/무슨/모르/어렵/죄송/오해).
  Exogenous: depends on the real human's private reaction, not anima state.
- **autogenous self-consequence a_auto_i** = H_9104-style self-relief: margin drop the emit
  produces in a SELF store (bind emit into a self ImmuneMemory, margin_before − margin_after),
  NO human. Anima's self-manufactured "consequence."
- **V** = brain.vbasal (core/brain.hexa) delta-rule linear value lane, READ-only w.r.t. the
  substrate emit/Ψ (a_substrate_disjoint; emit-drive lane 0/4 · recall_thr untouched).

## Held-out protocol (breaks circularity)
Split N triples: first 60% TRAIN, last 40% held-out TEST. V trained ONLINE on TRAIN
(feats_i → reward a_real_i via vbasal_update GO), then FROZEN. All correlations on held-out
TEST only.

## Falsifier (PRE-REGISTERED, FROZEN — no post-hoc move)
- **D_real**      = corr( V(feats_test), a_real_test )        — held-out, real human pairing
- **D_surrogate** = corr( V(feats_test), a_shuf_test )        — same frozen V, human responses
                    turn-shuffled (each emit paired with a RANDOM other human response =
                    exogenous coupling destroyed)
- **autogenous**  = corr( a_auto_test, a_real_test )          — can anima's self-manufactured
                    consequence already explain the real human consequence? (must floor =
                    human response is genuinely NOT self-derivable)

**PASS 🟢 iff  (D_real − D_surrogate ≥ 0.15)  AND  (autogenous < 0.05).**
- PASS ⇒ **first genuine exogenous emit-appropriateness faculty** — real human dialogue
  response opens what the 4 self-contained axes could not = session insight EMPIRICALLY
  confirmed (self-contained impossible + escape found).
- FAIL (either clause) ⇒ 🔴 CEILING: chat-user is ALSO a DPI ceiling ⇒ DPI meta-law is
  deeper than receiver-type; chat-user joins the 4 self-contained axes. HONEST either way
  (first offline engine-native exogenous-consequence measurement, valuable both directions).

## Ψ safety (a_substrate_disjoint)
V and all consequence tables are READ-only over the substrate. The substrate emit/silence
decision stream and psi_sum are byte-identical ON vs OFF (verified by re-running the decision
stream with the consequence lane disabled). emit-drive lane 0/4 and §ImmuneMemory recall_thr
are NEVER written.

## Honesty (c9)
Bar frozen here, pre-measurement. FALSIFIED/negative is a result (not concealed). No LLM
self-judge — the captured hexa stdout is the evidence.
