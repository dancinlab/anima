# IIT daemon R3.6 contrastive-support microexperiment (2026-08-15)

Status: COMPLETE — `DIAGNOSED-MISSING-CONTRASTIVE-SUPPORT`.

The preceding 24-arm encoder exhaustion found three frozen-panel passers and zero robust passers.
Token-unigram/ridge, token-unigram-bigram/ridge and token-positional/ridge passed the unchanged
R3.6 bridge bars, but scored only `3/8`, `4/8` and `5/8` on negation, keyword-lure, novel-frame and
word-order stress. This follow-up changes one axis only: contrastive support. It keeps the three
representations, ridge classifier, constants, original 702 events, frozen R3.6 evaluation and bars
fixed. It is local CPU microdiagnosis, not mouth training.

## Arms

Each of the three frozen passers is refit with six deterministic support conditions:

1. original support only;
2. negated command negatives only;
3. metalinguistic/keyword-lure negatives only;
4. reordered atom word-salad negatives only;
5. no-op/session-unchanged negatives only;
6. the union of all four contrast families.

All 18 arms run. Added rows are labelled only `other`; they never contain expected response bytes,
evaluation indexes or a prompt lookup. No existing positive row is deleted or reweighted. Support
rows are unique and their exact generated SHA is recorded.

## Fixed screens

Each arm is measured on:

- the original 47-event R3.6 panel with all three bridge bars fixed at `0.90`;
- the already preregistered eight-case shortcut stress panel;
- a second eight-case confirmation panel fixed here before this arm is implemented, containing
  unseen query/memory frames, negation, metalinguistic lure, no-op and reordered atoms;
- all four memory and four query support-template leave-one-out folds for any arm that passes the
  frozen panel.

A robust contrastive pass requires the frozen bars, stress exact `1.0`, confirmation exact `1.0`
and leave-template-out `>=0.90`. The first passing representation/support pair in protocol order is
the sole candidate. A pass would still mean only bounded registered command discrimination; it
would not be a conversational or open-domain semantic model.

## Verdicts and stopping rule

- `SUPPORTED-CONTRASTIVE-BOUNDARY-MICRO`: at least one arm passes every fixed screen.
- `DIAGNOSED-MISSING-CONTRASTIVE-SUPPORT`: an augmented arm materially improves shortcut rejection
  by at least one of eight fixed cases (`0.125`) while preserving the frozen bars, but no arm
  passes the independent confirmation screen.
- `FAIL-SHALLOW-SEQUENCE-SUPPORT`: no augmentation improves both frozen and shortcut behavior.
- `INVALID-CONTRASTIVE-INSTRUMENT`: checksums, base reproduction, uniqueness, determinism or arm
  accounting fails.

No result authorizes 303M training, a neural mouth, IIT-mouth coupling or production. If this batch
fails robust confirmation, locally tractable shallow lexical/order-aware bridges are exhausted.
The next research question would require a separately preregistered learned sequence-semantic
encoder and new provenance-bearing data, not more post-result template additions.

## Result

All 18 arms ran, all three original-arm prediction hashes reproduced, and nine augmented arms
improved shortcut stress by at least one fixed case. No arm passed robust confirmation.

- token unigram + all contrasts: frozen `1.0/1.0/1.0`, stress `6/8`, confirmation `5/8`;
- token unigram+bigram + all contrasts: frozen `1.0/1.0/1.0`, stress `7/8`, confirmation `6/8`;
- token positional + all contrasts: frozen kind `0.8085`, query `0.0000`, record `1.0000`, so the
  original bridge regressed despite stress/confirmation `6/8` each;
- every eligible leave-template-out score remained at least `0.9828`.

The data additions help the exact negative families they expose, but do not transfer completely to
independent query, negation and no-op surfaces. The canonical result SHA-256 is
`a27bd54d…a6b571`.
