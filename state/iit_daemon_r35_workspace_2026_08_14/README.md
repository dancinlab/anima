# IIT daemon R3.5 — compositional content workspace (2026-08-14)

Status: COMPLETE — `SUPPORTED-COMPOSITIONAL-WORKSPACE-CAUSALITY`.

This Python-only gate follows the bounded two-surface R3 result and precedes another 303M mouth
run. It records the complete breakthrough review before implementation. The narrow question is
whether a persistent IIT state can select an addressed semantic record, keep that record distinct
from the intrinsic three-bit state, and causally route a novel entity/relation/value composition to
the canonical generator. It does not claim that the record is understood, learned from natural
language, or sufficient for conversation.

## Evidence behind the redesign

The repository already has four working pieces, but they do not form a semantic closed loop:

- ByteGPT predicts the next byte but the latest 0.89M, 3M, 10M, 29M and 303M studies did not form
  independently meaningful conversation. Increasing exposure and capacity improved CE or training
  recall without passing the frozen meaning, memory and correction gates.
- `IITDaemonCore` has persistent, intervention-sensitive intrinsic state and exact recovery.
- CLMS reads two addresses and R2 proves that the combined result can be latched into the IIT core.
- R3 proves that final IIT state can select one of two exact surfaces.

The missing chain is:

```text
user/world event
  -> structured content record
  -> content-addressed persistence
  -> IIT-selected address/broadcast
  -> generator-visible content
  -> emitted bytes
  -> observed consequence returned on a later tick
```

The recent admission, exposure and capacity results show that input is not wholly ignored: topic
words and prompt shuffles can affect output. The failure is that a proposition is not maintained as
a composable internal unit. A three-bit IIT state cannot store a sentence. Its feasible role is to
select which externally stored content becomes globally active, while CLMS/KOSMOS retain the
content itself.

## Missing parts exhausted in the review

1. **Semantic event representation.** A byte stream needs a bounded internal record such as
   entity, relation and value. This first gate uses an explicit validated record so the causal
   plumbing can be tested independently. A later mouth must learn the byte-to-record mapping; R3.5
   does not pretend that a hand-authored record is learned semantics.
2. **Content-addressed workspace.** The IIT state selects an address; it does not duplicate the
   record payload. Reset, state-address shuffle, workspace-address shuffle and lesion must destroy
   the selected content while irrelevant-slot mutation must not.
3. **Workspace-to-generator route.** The selected record must enter the canonical
   `core.generator` boundary directly. Gold, expected text, prompt and scorer state must not cross
   that boundary.
4. **A more efficient learned mouth representation.** External I/O remains UTF-8 bytes, but a
   later learned mouth may require latent byte patches or learned subword units before a semantic
   workspace. BLT/MEGABYTE-style patching remains deferred because it would mix a second axis into
   this causal plumbing gate.
5. **An explicit end-of-turn event.** A learned mouth still needs a canonical termination event.
   The previous assistant-only boundary fix solved one termination bug but did not solve semantic
   generalization, so termination alone is not treated as the missing content route.

## Design variants and decisions

| Variant | Decision | Reason / falsifier |
|---|---|---|
| Put full text inside the three IIT bits | reject | impossible capacity and destroys the fixed, enumerable intrinsic candidate |
| Add another Phi scalar or emit threshold | reject | repeats the proven content-inert gate pattern |
| Hardcode question-to-answer rules | reject | evaluator-side answer scaffold; cannot establish state/content causality |
| Let the generator see prompt, gold or active address | reject | creates an uncontrolled shortcut around IIT state |
| Store exact canned answer strings | reject | only repeats R3 with more surfaces and does not test composition |
| Store a validated entity/relation/value record | choose for R3.5 | smallest payload that can be recombined and independently mutated |
| Render the selected record canonically | choose for R3.5 | tests byte routing without falsely calling it a learned language mouth |
| Train ByteGPT jointly with the workspace now | defer | current mouth is not independently valid; joint failure would be uninterpretable |
| Candidate selection over a valid mouth | later first coupling | safest learned-mouth bridge once a mouth passes independently |
| Latent prefix/cross-attention coupling | later preferred coupling | lets state affect every decode step but requires a valid mouth and matched ablations |
| Direct end-to-end IIT/mouth co-training | defer | highest confounding and Goodhart risk |
| Public-chat online weight updates | reject | persistent prompt poisoning and provenance loss |
| Bounded state/memory updates with atomic snapshot | choose | reproducible, recoverable and safe without online gradient updates |

The longer-term target remains:

```text
UTF-8 bytes
  -> learned byte patches / event encoder
  -> content slots (entity, relation, value, polarity, uncertainty)
  -> CLMS/KOSMOS address write and read
  -> IIT selection, tension and broadcast
  -> workspace-conditioned native decoder
  -> UTF-8 response + end-of-turn
  -> observed result returned to memory and IIT state
```

R3.5 implements only the middle causal seam: registered content slots -> IIT-selected address ->
canonical record bytes. It does not add a parallel chat engine, Python answer scaffold module,
second decoder, model weights, tokenizer or evaluator.

## Frozen protocol and panel

`protocol.json` and `panel.json` are the SSOT. The panel contains a support set that exposes every
entity, relation and value atom, followed by nine evaluation trials whose exact triples are absent
from that support set. This is a **novel-composition plumbing control**, not a learning claim: the
runtime has no fitted parameters in this gate.

Three workspace addresses map to the three one-bit interventions `(1, 2, 4)`. Under the frozen XOR
ring these settle to distinct persistent states. Every trial has three distinct records, one active
address, an explicit expected byte string, a selected-slot counterfactual value, and a distinct
irrelevant slot mutation. The generator receives only final state, state-to-address mapping and
workspace records. Expected bytes remain scorer-only.

The evaluator must checksum-pin the complete R3 result and panel, validate that all evaluation
triples are absent from support while all atoms are covered, and run arms in this order:

1. state-to-address oracle/instrument check;
2. normal delayed read;
3. reset before delayed read;
4. cyclic IIT intervention-address shuffle `(1,2,0)`;
5. cyclic workspace slot-address shuffle `alpha<-beta<-gamma<-alpha`;
6. all-node lesion mask `7`;
7. selected-record counterfactual mutation;
8. irrelevant-record mutation;
9. atomic core+workspace snapshot disturbance and recovery.

If the oracle is below `0.90`, later arms are not run or interpreted. Normal and recovery must be
at least `0.90`. Reset, both shuffles and lesion must be at or below measured three-way chance
`1/3 + 0.06 = 0.393333...`. At least `0.90` of selected-memory counterfactuals must change to the
registered new correct bytes; at least `0.90` of irrelevant-memory mutations must preserve output
byte-for-byte. Recovery must restore state, selected address, all records and output exactly.

Passing returns `SUPPORTED-COMPOSITIONAL-WORKSPACE-CAUSALITY`. Any non-oracle failure returns
`FALSIFIED`; oracle failure returns `INVALID-INSTRUMENT`. No seed, panel, threshold, output format or
trial may change after observing results.

## Non-claims and next gates

Even a pass establishes only a bounded, explicitly represented content-address selection and byte
routing mechanism. It does not establish learned semantics, free-form generation, meaningful open
conversation, phenomenal consciousness, IIT exclusion/maximal complex, or production readiness.
Participant mounting stays blocked as `BLOCKED-R35-NOT-A-LEARNED-MOUTH`.

After a pass, the next work is still an independently trained mouth. The staged order is: valid
English mouth -> independent meaning/memory/correction panel -> candidate-selection coupling ->
latent workspace coupling -> normal/reset/shuffle/lesion/recovery -> consequence return through
KOSMOS -> FIFO/reply ownership/HTTP/WebSocket/soak/rollback. A 303M or 7B run is not authorized by
an R3.5 pass alone.

## Result

Implementation and execution completed after the protocol was committed and pushed as
`3130f8e74`. No registered panel row, source artifact, address mapping, intervention, order or bar
changed after results were observed.

- The existing `core.iit_daemon.IITDaemonCore` remains the only intrinsic transition engine.
  `core.iit_daemon` now validates bounded content records, derives the final-state/address codebook,
  applies reset/shuffle/lesion interventions, and atomically snapshots the core plus external
  records. The original R0 snapshot schema and bytes remain compatible.
- `core.generator.gen_iit_workspace_content` is the only new output boundary. It accepts final
  state, state/address codebook and the three records; it has no argument for prompt, active
  address, expected text or gold. It renders a selected record as canonical
  `entity relation value.` bytes and stays silent for an unregistered state.
- Pair/oracle, normal, selected-memory counterfactual, irrelevant-memory mutation and snapshot
  recovery accuracy are all `1.0000`. Reset, cyclic IIT address shuffle, cyclic workspace address
  shuffle and all-node lesion accuracy are all `0.0000`, below the frozen `0.393333...` ceiling.
- All nine selected evaluation triples are unique and absent from the six-record support set while
  every entity, relation and value atom is supported. Every selected-memory mutation changes to the
  registered counterfactual bytes; every irrelevant-memory mutation preserves normal bytes.
- Every disturbed core+record snapshot differs from pristine, every reload restores core state,
  address, all records and output exactly, and every snapshot is mode `0600`.
- Focused IIT/store/conversation/native-boundary regression passed `103/103`. Full repository
  Python QA passed `190 passed, 1 skipped, 3 subtests`; the skip is the expected unavailable local
  CUDA/CuPy path. Compile, JSON and diff checks pass.
- Canonical source execution produced byte-identical result JSON twice with SHA-256
  `74f917de8718a2de43c4db3d57f900922315a6cd019b71381eb0c7917313f56e`. A clean isolated wheel
  (`anima_python-0.20.245`, SHA-256
  `e7df13c0f85287703caffbe71e434549992d70cfe9cf03a35bb14a61b05dd7b6`) reproduced the same bytes.
- No model training, model/data mutation, HF write, Vast.ai rental, participant mount or live mouth
  deployment occurred. `ING.jsonl` and `stream_mi.json` remain user-owned and untouched.

Verdict: `SUPPORTED-COMPOSITIONAL-WORKSPACE-CAUSALITY`. The missing bounded state/address/content
seam now exists and passes the registered interventions. It is deliberately not a learned event
encoder or conversational mouth. Production remains `BLOCKED-R35-NOT-A-LEARNED-MOUTH`; the next
gate is an independently trained meaningful English mouth before candidate-selection or latent
workspace coupling is interpreted.
