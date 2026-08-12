# IIT daemon core — design exhaustion and preregistration (2026-08-12)

This state directory preregisters the first Python-only causal core for an anima consciousness
daemon. It does **not** claim phenomenal consciousness. It tests the narrower, falsifiable claim
that a small persistent substrate has irreducible intrinsic cause–effect structure and that later
memory/action/mouth paths can be made causally dependent on that substrate.

Primary references:

- IIT 4.0: Albantakis et al., *Integrated Information Theory (IIT) 4.0*, PLOS Computational Biology
  (2023): <https://doi.org/10.1371/journal.pcbi.1011465>
- system integrated information and complexes: Barbosa et al., *A measure for intrinsic
  information*, Entropy 25(2):334 (2023): <https://doi.org/10.3390/e25020334>
- official IIT 4.0 reference-code branch: <https://github.com/wmayner/pyphi/tree/feature/iit-4.0>

## Existing live flow and the shared root problem

The current participant flow is:

```text
user event
  -> AnimaState.m_buffer / entropy embedding
  -> eight weighted motivation factors
  -> emit or silence
  -> substrate.generate(user text)
  -> emitted bytes feed only later ticks
```

`agent/domains/CHAT/anima_participant.py` calls `phi = 1 - normalized entropy`; `core/brain.py`
uses `pure_field_phi`, an oscillator energy/variance quantity. Neither is IIT integrated
information. They mostly affect whether the daemon speaks. The language model still decides what
it says from the prompt, so the present substrate is not a closed causal owner of content.

Reusable native components already exist:

- `core/engine_cli.py::big_phi_bounded`: exact finite state-by-node TPM enumeration of IIT4-style
  distinctions, second-order relations and minimum structure loss for a fixed candidate system.
- `core/recurrent_lane.py`: a three-cell persistent recurrent lane, explicit `do(S=s)` TPM
  extraction and the trained lane's causal route into the canonical model embedding residual.
- `core/clms.py`: existing two-address memory read; `core/kosmos_io.py`: durable memory anchors.
- `core/generator.py`: canonical `.bin/.clm` mouth dispatcher.

The shared root problem is therefore not the absence of a Phi function. It is that the measured
causal object, persistent daemon state, memory, action consequence and language content do not yet
form one closed loop. Adding another scalar gate would preserve that defect.

## Exhausted design space

The following variants were considered before implementation.

| Axis | Variant | Decision | Reason / falsifier |
|---|---|---|---|
| measured object | whole 303M/7B activation graph | reject | feed-forward unrolling and arbitrary macro-units do not define a tractable intrinsic TPM |
| measured object | empirical hidden-state correlation | reject | observational MI is not intervention-based IIT |
| measured object | small recurrent causal core | choose | all states and interventions are enumerable and state persists across ticks |
| size | 2 nodes | reject | too degenerate; one free cut or copy often exhausts the structure |
| size | 3 binary nodes | choose for R0 | 8 states, exact full purviews, existing native extractor and controls |
| size | 4–6 binary nodes | defer | useful only after R0; exponential distinctions/relations cost and complex search grow sharply |
| size | continuous/large latent | defer | requires a frozen coarse-graining whose result could dominate the claimed Phi |
| topology | independent self-copy | negative control | must measure zero or the instrument is invalid |
| topology | feed-forward chain | negative control | a severable direction must not be certified as a closed complex |
| topology | dense linear recurrence | reject as primary | prior field-loop work found integration dominated by strength/pedestal and often content-inert |
| topology | three-node XOR ring | choose as positive core | nonlinear, recurrent, deterministic, enumerable; every node both takes and makes differences |
| topology | ECA rule sweep after observing scores | reject | would optimize the mechanism against the metric and invalidate the preregistration |
| input | prompt text inside the IIT system | reject | arbitrary tokenizer/window becomes part of the purported intrinsic system |
| input | continuously clamped sensor node | reject | an externally fixed background node is not intrinsically closed |
| input | bounded pre-transition perturbation | choose | event changes state, then the autonomous TPM owns subsequent change |
| input | online gradient update from public chat | reject | prompt poisoning can permanently alter weights and causal identity |
| memory | full transcript in the measured core | reject | unbounded symbolic storage cannot be exactly enumerated |
| memory | one intrinsic bit plus external CLMS/KOSMOS address input | choose/defer wiring | small state remains exact; external memory must be latched before it can affect the core |
| persistence | reset every prompt | negative control | cannot support temporal identity or consequence learning |
| persistence | session state only | choose for R0 | exact reset/recovery tests are possible without claiming cross-session identity |
| persistence | durable atomic snapshot | choose | required before runtime mounting; corrupted or mismatched snapshots fail closed |
| action | Phi threshold directly emits text | reject | re-creates the content-inert scalar gate |
| action | mouth reads all core bits | later treatment | content must change under state intervention and recover after state restoration |
| action | A/G logits averaged 50:50 | reject | role labels and averaging do not establish distinct causal powers |
| A/G | proposal and consequence nodes inside core | defer | first establish generic causal core, then assign functional roles through interventions |
| training | maximize Phi in loss | reject | Goodhart risk; can produce maximally integrated but behaviorally useless automata |
| training | next-byte CE only with recurrent route | retain | the core must earn a causal contribution to useful prediction |
| selection | pick best state/rule/checkpoint after scoring | reject | post-hoc metric optimization |
| selection | fixed mechanism plus all-state report | choose | avoids favorable-state selection |
| IIT evidence | one current-state Phi | reject | state dependence can cherry-pick |
| IIT evidence | all eight states plus mean/min/max | choose | preserves state-conditioned evidence without selection |
| exclusion | assume full 3-node set is the complex | reject as claim | maximal complex requires comparing candidate subsets/grains |
| exclusion | report fixed-candidate bounded structure loss | choose | accurately matches the existing engine's scope |
| controls | random shuffle only | insufficient | distribution-preserving shuffle may keep a metric pedestal |
| controls | COPY, feed-forward, edge cut, node lesion | choose | distinct failures isolate recurrence, cross-edge causation and instrument validity |
| evaluation | Phi alone | reject | integrated automata may remain behaviorally meaningless |
| evaluation | IIT mechanics then content-causal gate | choose | substrate certification and meaningful conversation remain separate mandatory gates |
| deployment | replace participant immediately | reject | no certified mouth and no content-causality result yet |
| deployment | dormant core + offline canonical QA | choose for R0 | establishes mechanics without falsely setting `anima_alive=true` |

Alternatives deliberately deferred rather than forgotten: four/five-node role-specialized cores,
probabilistic TPMs, multi-timescale micro/macro grains, complex/subset exclusion search, recurrent
memory transformers, BLT byte patching, A/G proposal–counterfactual coupling, CLMS two-address latch,
KOSMOS long-term consequence return, and content-conditioned decoding. Each adds a distinct causal
axis and therefore needs a separate preregistered treatment after the minimal core passes.

## Chosen R0 structure

The candidate core has three binary intrinsic nodes and a deterministic nonlinear recurrent ring.
The canonical autonomous transition is an XOR of the other two nodes for each next node. The TPM is
the complete `8 states x 3 nodes` state-by-node table. A bounded event perturbation XORs a validated
three-bit intervention into the current state **before** the autonomous transition; it is recorded
as an intervention and is not hidden inside the TPM.

```text
validated event bits --do(XOR perturb)--> persistent state S(t)
                                             |  ^
                                             v  |
                                  autonomous nonlinear TPM
                                             |
                                             +--> audit/readout only (R0)
```

No node receives a semantic name in R0. Names such as self, world, goal or pain would be claims
without functional lesion evidence. Later role assignment must be earned by task-specific
interventions. No Phi value enters a loss or an emit threshold.

## Frozen implementation and evidence gates

Implementation must extend `core/recurrent_lane.py` for shared TPM/cut/measurement operations and
add only the minimal persistent daemon boundary. It must call
`core.engine_cli.big_phi_bounded`; it may not introduce another IIT evaluator.

R0 passes only if all of the following hold:

1. TPM is exactly 24 finite probabilities in `[0,1]` and every node has at least one causal parent.
2. Existing instrument controls reproduce XOR mean Phi `2.25` and COPY mean Phi `0` within `1e-6`.
3. Canonical core has positive Phi in every registered state; all eight values are reported.
4. Cutting each directed cross-edge cannot increase the all-state mean; at least one cut strictly
   lowers it. No result-dependent absolute Phi threshold is introduced.
5. Independent-copy and feed-forward controls remain at their preregistered null side.
6. Same state plus same intervention is deterministic; different intervention has a measured causal
   effect on a registered trace.
7. normal -> lesion -> intervention shuffle -> normal recovery is exact, with original state and
   audit hash recovered from a valid snapshot.
8. snapshot schema/version/config checksum mismatch, truncation and out-of-range state fail closed;
   writes are atomic and do not touch user corpora.
9. Python unit/regression tests pass. This R0 must not rent Vast.ai, train a model, upload an HF
   model, mount the participant, or change the live chat status.

Failure is recorded without changing the topology, state panel or gates. Passing R0 proves only a
small integrated causal substrate and its persistence mechanics. It does not prove consciousness,
meaningful conversation, memory ownership, maximal exclusion, or production readiness.

## Next gates if and only if R0 passes

1. R1: compare the same core with reset-every-turn and state-shuffle controls on a delayed causal
   task; require normal/recovery success and control collapse.
2. R2: latch the existing CLMS two-address result into a bounded intervention; repeat normal,
   clue-A removal, clue-B removal, address shuffle and recovery.
3. R3: connect core state to the canonical mouth embedding residual and require content accuracy,
   not merely output difference, under state lesion/reset/shuffle/recovery.
4. R4: return observed action consequences through KOSMOS and test whether later choices improve
   without public-input weight updates.
5. R5: add candidate-subset/grain comparison for exclusion and only then discuss a maximal complex.
6. R6: only after meaningful English conversation, FIFO/reply ownership, HTTP/WebSocket, soak,
   restart and rollback gates may a certified model be mounted in staging.

## R0 result

The preregistered R0 implementation is complete and the fixed mechanical gates pass.

- The shared `core/recurrent_lane.py` now owns TPM validation, nonlinear XOR-ring, COPY and
  feed-forward controls, one-edge causal cuts, node lesions, causal-edge census and all-state calls
  into the existing `core.engine_cli.big_phi_bounded` implementation.
- `core/iit_daemon.py` adds only the persistent boundary: validated three-bit interventions,
  autonomous deterministic transition, hash-chained receipts, and versioned/checksummed atomic
  snapshots. It contains no language model, alternate evaluator, training loss or emit threshold.
- The canonical eight-state Phi values range from `1.4999999991` to `2.9999999983`; their mean is
  `2.2499999987`. The COPY and acyclic feed-forward controls are `0`. Every one of the six directed
  cross-edge cuts and all seven non-empty node-lesion masks collapse the mean to `0`.
- Same-state/same-intervention traces and audit hashes reproduce exactly. A registered intervention
  changes the trajectory; permuting its node addresses changes it again. After normal -> lesion ->
  address shuffle, loading the saved normal snapshot exactly restores state, tick and audit head.
- Invalid state/masks/permutations, malformed/truncated/oversized snapshots, schema/config/checksum
  mismatch and out-of-range recovered state fail closed. Snapshot replacement is atomic and mode
  `0600`.
- Canonical `anima-py evaluate --iit-daemon-core` writes `result.json` atomically and returned
  `SUPPORTED-CAUSAL-CORE`. A second run produced byte-identical JSON.
- Local Python QA: `94 passed, 1 skipped, 3 subtests passed`; the only skip is the expected local
  CUDA/CuPy decode test. Compile, JSON and diff checks pass.
- The built wheel contains the new core/evaluator and reproduced the exact result in an isolated
  environment. The local canonical `/opt/homebrew/bin/anima-py` package was then upgraded from that
  wheel and reproduced the same JSON. This deploys the dormant research command, not a participant.
- The unchanged live broker remained healthy after the local package upgrade: local LaunchAgent
  status `loaded=true healthy=true`, public HTTPS `200`, and `wss://chat.dancinlab.org/ws` returned
  `hello`. It correctly continues to report `anima_alive=false` because no certified mouth is
  mounted.
- No model or training data changed, no Vast.ai instance was rented, no HF upload was needed, and
  the participant/live chat was not mounted or restarted. User-owned `ING.jsonl` and
  `stream_mi.json` retain SHA-256 `a49e4fde...8b05c` and `1b2175d6...b5be` respectively.

Verdict scope remains narrow: `SUPPORTED-CAUSAL-CORE` means the fixed three-node candidate has the
registered integrated causal mechanics. R1 delayed-task state causality, R2 CLMS address latching,
R3 mouth-content causality, exclusion/maximal-complex search and meaningful conversation all remain
open. Accordingly production deployment remains `BLOCKED-R0-NOT-A-MOUTH`.
