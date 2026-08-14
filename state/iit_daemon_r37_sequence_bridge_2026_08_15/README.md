# IIT daemon R3.7 — English sequence-semantic bridge

Status: PREREGISTERED — no result yet.

R3.6 established a support-identifiability failure: the exhausted shallow family had only 54
support tokens, ignored unseen decisive words and could not distinguish order or negation. R3.7
changes one axis. It retains the existing bounded event schema and R3.5 causal seam, but replaces
bag/centroid features with a small standard bidirectional GRU over ordered UTF-8 bytes.

This is an English-only bounded bridge experiment. It is not a conversational mouth, a 303M/7B
training run, an IIT maximal-complex claim or production authorization. The active scale plan is
recorded in the root `PLAN.md`.

## Fixed call path

```text
HF dancinlab immutable English event rows
  + frozen R3.6 702-row support
  -> core.iit_daemon sequence-semantic bridge variant
  -> cli.evaluate existing semantic-bridge battery
  -> existing R3.5 IITDaemonCore/content workspace
  -> core.generator.gen_iit_workspace_content
```

No new runtime engine or standalone evaluator is allowed. The sequence variant must use the same
validated event/record types and the same normal/stateless/reset/shuffle/lesion/counterfactual/
irrelevant/correction/recovery order as R3.6.

## Data contract

`build_dataset.py` creates the only authorized source revision. It is repository-authored CC0
English microdata with explicit provenance, not scraped user content. It combines the frozen R3.6
support with disjoint positive memory/query frames and contrastive negation, quotation and
wrong-order events. Extra entity/value atoms expand supervision without changing the frozen output
classes. The builder must fail unless:

- every R3.5 held-out complete record remains excluded from train;
- every frozen/stress/confirmation/new-panel evaluation string is absent from train/validation;
- train and validation texts are unique and disjoint;
- each output field has multiple train classes and every frozen atom has train support;
- output files and the manifest are deterministic.

Generated JSONL is uploaded only to private
`dancinlab/anima-iit-daemon-r37-sequence-data-2026-08-15`; it is not committed to Git. The final
protocol will pin the immutable HF revision, file sizes and SHA-256 before model training begins.

## Fixed model and optimization

- raw printable ASCII/UTF-8 bytes, bounded by the existing 256-byte event validator;
- byte embedding 32, one-layer bidirectional GRU hidden size 64, dropout 0;
- concatenated final forward/backward state with five factorized heads;
- kind loss on every row, address loss on memory/query, record-field loss on memory;
- balanced memory/query/other batches, batch 48, seed 7;
- AdamW `lr=0.002`, betas `(0.9, 0.95)`, weight decay `0.01`, gradient clip `1.0`;
- exactly 2,500 update steps, final-step selection, no early stopping or post-result continuation;
- CPU, two Torch threads, deterministic algorithms; no GPU/Vast.ai.

The model is checksum-validated JSON, written atomically with mode `0600`, uploaded only to a
private HF `dancinlab` model repository, and removed locally after custody verification.

## Fixed evaluation and stopping

Order is state oracle, R3.6 frozen bridge, old shortcut stress, old independent confirmation, new
held-out sequence panel, then—only if all pass—the unchanged R3.5 causal arms.

- state oracle, frozen kind/query-address/complete-record: each `>= 0.90`;
- old shortcut stress and independent confirmation: exact `1.00` each;
- new held-out sequence panel exact accuracy: `>= 0.90`;
- normal/counterfactual/irrelevant/correction/recovery: each `>= 0.90`;
- stateless/reset/IIT-address-shuffle/workspace-address-shuffle/node-lesion:
  `<= 1/3 + 0.06`;
- counterfactual same-question output change and irrelevant-memory stability: each `>= 0.90`.

Any failed bridge gate stops later arm execution and interpretation. Results, including failure,
must be recorded without changing data, seed, steps, panels or bars. A pass supports only bounded
English event-to-workspace causality and opens a later mouth experiment; it does not authorize
participant mounting or production.

