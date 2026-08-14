# IIT daemon R3.7 — English sequence-semantic bridge

Status: COMPLETE — `FAIL-SEQUENCE-SEMANTIC-BRIDGE`.

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
`dancinlab/anima-iit-daemon-r37-sequence-data-2026-08-15`; it is not committed to Git. Protocol
`protocol.json` pins immutable revision `4301fd00…f4de7`, dataset SHA
`39358a8a…42e17`, 5,018 train rows, 531 validation rows and every file size/SHA before model
training begins.

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

## Result

The one preregistered CPU run completed all 2,500 updates with 49,081 parameters and final balanced
training loss `1.5050e-7`. State oracle and frozen query-address were both `1.0000`, but the frozen
event-kind and complete-record bars failed at `0.8298` and `0.4722`. Shortcut stress was `0.7500`,
independent confirmation `0.8750`, and the newly authored sequence panel `0.9583`. The unchanged
gate therefore stopped before every R3.5 causal arm. `result.json` contains no `arms` member.

The failure localizes a data/support problem rather than an IIT workspace failure. Random text-hash
validation was `0.9981` exact while the record-combination-excluded frozen set was only `0.5957`
exact. The split lets near-identical generated templates and atom combinations occur on both sides,
so it is not an independent compositional validation. The extra training atoms also became
competing output classes: frozen names such as `aria`, `borin`, `faro` and `dain` were repeatedly
decoded as `faro`, `garen`, `jora` or `iona`. The model still accepted the quoted keyword sentence
and reversed `Amber carries aria...` control as memory, and classified the unseen
`Kindly fetch beta's stored content` query as memory. The new panel's `23/24` score is therefore
not sufficient evidence; it is close to the newly authored training grammar.

No data, seed, step count, panel or threshold was changed after seeing this result. A future
protocol must fix the dataset split at the template/record group level and separate output-class
expansion from sequence-order learning as independently matched axes. It must not reinterpret this
run or resume the failed model. R3.5 remains valid, but R3.7, mouth scaling, IIT-mouth coupling,
participant mounting and production remain blocked.

The failed model and exact evidence are preserved in private HF model revision
`dancinlab/anima-iit-daemon-r37-sequence-model-2026-08-15@4296d2a8b861a7990c4995d5a6cd1ce1f36b1829`.
`custody.json` records five independently verified file sizes and SHA-256 values. The local model
copy is removed after final reproducibility QA; Git retains protocol, result and custody evidence,
not model weights or training JSONL.

Focused IIT/Python/CHAT regression passed `100/100`. A second source-tree run and an isolated
`anima_python-0.20.245` wheel run reproduced both model SHA
`560fcae7…206f5` and result SHA `5f33dba9…56c7f` byte-for-byte. The isolated wheel SHA is
`f8ca31ed…70a41`; model persistence retained mode `0600`. Python compile, JSON validation and the
R3.6 frozen-failure regression also pass. HF authentication was supplied only through the secret
CLI and no token was logged or stored in an artifact.

Implementation/result commit `c64ef266b` was pushed to `origin/main`. The same wheel was installed
into the local canonical `/opt/homebrew/bin/anima-py`; installed `core/iit_daemon.py` and
`cli/evaluate.py` hashes match the source, and help exposes the R3.7 flag. CHAT code and participant
wiring did not change, so the healthy broker was not restarted. Read-only post-deployment checks
passed local/public HTTP `200` and local/public WebSocket `hello`. The reported
`anima_alive=true` still belongs to the pre-existing uncertified step-45000 participant and is not
an R3.7 success claim.
