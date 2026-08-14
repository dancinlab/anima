# IIT daemon R3.6 encoder microexperiment exhaustion (2026-08-15)

Status: COMPLETE — `DIAGNOSED-SHALLOW-LEXICAL-SHORTCUT`.

R3.6 failed before the IIT/workspace seam: its factorised hashed byte n-gram centroid scored
event-kind `0.8085`, query-address `0.0000` and complete address+record `0.6944`. This follow-up is
microexperiment-only. It does not train a mouth, change R3.5/R3.6 data or bars, use a GPU, mount a
participant, or authorize production. The R3.6 protocol, panel, result and the R3.5 panel/result are
checksum-pinned controls.

## Fixed question and axes

The question is whether R3.6 failed because of its order-destroying representation, its nearest
centroid decision geometry, or a deeper lack of sentence semantics. The same 702 support events,
35 excluded complete records, 47 frozen evaluation events and `0.90` bridge bars remain fixed.

The complete factorial is run; no early success stops later arms:

- representations: existing hashed byte 1–3 grams; explicit byte 1–3 grams with position regions;
  token unigram; token unigram+bigram; token unigram+bigram with start/end/region positions; and a
  token+byte hybrid;
- classifiers: normalized nearest centroid; globally centered centroid; deterministic ridge
  one-vs-rest with fixed `lambda=1.0`; and Bernoulli naive Bayes with fixed `alpha=1.0`.

This produces 24 representation×classifier arms. Vocabulary and IDF are fitted only on support.
Every field remains factorised. Expected bytes, panel index, gold output and prompt lookup are not
features. The existing `core.mi_compress.hashed_ngram_features` is used unchanged by the frozen
byte control; the other representations extend the same Python bridge diagnostic path.

## Generalization and shortcut controls

Every arm is also measured on these preregistered, non-certifying stress cases:

- a second query paraphrase with a new outer frame;
- explicit negation that must be `other`;
- the word `retrieve` used without a query;
- a valid memory event with an unseen outer frame;
- the same atoms reordered into a word salad that must be `other`;
- the frozen difficult `Nothing should change now.` negative;
- a held-out memory paraphrase using a registered relation surface.

For arms that first pass all three frozen bridge bars, the sweep additionally refits and records
support-template leave-one-out accuracy for all four memory and all four query templates, then runs
representation ablations with token order shuffled, prompt-frame tokens removed, or atom tokens
removed. These diagnostics distinguish genuine frame/atom composition from keyword capture. They
do not alter the frozen R3.6 verdict. Restricting these expensive refits to frozen passers is fixed
here before execution and cannot hide a candidate because a non-passer is already ineligible.

## Fixed selection and verdicts

An arm passes the frozen bridge screen only when event-kind, query-address and complete
address+record are each at least `0.90`. A robust micro pass additionally requires stress exact
accuracy `1.0` and aggregate leave-template-out accuracy at least `0.90`. All 24 arms run before a
verdict. If multiple arms pass, the first in protocol order is the only candidate; results cannot
be used to reorder the list.

- `SUPPORTED-ROBUST-ORDER-AWARE-BRIDGE-MICRO`: at least one arm passes all fixed screens.
- `DIAGNOSED-SHALLOW-LEXICAL-SHORTCUT`: at least one arm passes frozen R3.6 but none passes stress
  and leave-template-out.
- `FAIL-NO-FROZEN-BRIDGE-PASS`: no arm passes the frozen R3.6 bars.
- `INVALID-MICRO-INSTRUMENT`: pinned artifacts, frozen control reproduction, determinism, or
  ablation accounting fails.

The run must reproduce the original hashed-centroid metrics exactly before any new arm is
interpreted. Two identical executions must produce byte-identical canonical JSON. Failure is
recorded unchanged; thresholds, examples, classifier constants and ordering cannot move after
execution.

## Result

All 24 arms ran and the frozen hashed-centroid control reproduced exactly (`0.8085`, `0.0000`,
`0.6944`). Three ridge arms passed the frozen R3.6 bridge bars:

| representation | kind | query | complete record | stress | leave-template-out |
|---|---:|---:|---:|---:|---:|
| token unigram | 0.9787 | 1.0000 | 1.0000 | 3/8 | 0.9828 |
| token unigram+bigram | 0.9787 | 1.0000 | 1.0000 | 4/8 | 0.9957 |
| token positional | 1.0000 | 1.0000 | 1.0000 | 5/8 | 0.9957 |

No arm passed stress, so robust pass count is `0`. Every frozen passer accepted `46/47` reversed
token events as non-`other`, while atom-only frame removal retained full memory-record accuracy
`1.0000`. The classifiers therefore learned literal atom/frame cues, not a reliable ordered event
boundary. The canonical result SHA-256 is `a8115c37…92b42d`.

## Preregistration caveat and non-claims

Before this file was frozen, a read-only implementation sketch inspected the frozen R3.6 panel and
showed that simple token/ridge variants may pass it while failing negation and word-order stress.
Therefore this battery is a diagnostic exhaustion study, not an independent confirmatory claim.
Even a robust pass would establish only bounded English event classification. It would not prove
open-domain meaning, conversation, Korean support, autonomous goals, phenomenal consciousness,
IIT maximality or production readiness. R3.7, 303M training, IIT-mouth coupling and participant
deployment remain blocked after this micro-only run.
