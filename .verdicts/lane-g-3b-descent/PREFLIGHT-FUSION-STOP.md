# ENGINE 3B → 7B Lane-G forge line — HARD PREFLIGHT GATE: STOP (util lever closed-negative)

substrate = GPU (Lane G) · forge flame · `a_lane_akida_gpu_split` (NEVER merged with Lane A/AKIDA or Lane-G-ref PyTorch)
date = 2026-06-05 · cost = $0 (NO GPU rented — preflight resolved to STOP before any rent, `a_fire_autonomous` not triggered)
worktree = isolated `worktree-agent-a2e8a3f058f2d927d` (concurrent monograph agent works the main tree — not entangled)

## PREFLIGHT QUESTION (per task)
Is the HEXA-FUSION device-resident CUDA-graph train-step (the util unblock, `a_cuda_graph_train`)
wired into anima's forge trainer so a 3B Lane-G fire can plausibly reach util-GREEN (MEAN ≥ 20%)?

## PREFLIGHT VERDICT: **STOP** — do NOT rent a GPU. The util lever is **CLOSED-NEGATIVE**, already measured upstream.

The STOP is NOT (only) an integration gap. It is a **stronger, already-quantified closed-negative**:
the HEXA-FUSION CUDA-graph capture/replay lever — the exact mechanism this campaign was told to deploy
for the util unblock — has been measured to a verbatim FALSIFICATION in the sibling hexa-lang kit, across
the FULL lever family. Renting a GPU to run a forge config whose util ceiling is already known-RED would
re-confirm a closed-negative at cost — forbidden by the task and by `a_completeness_over_cheap`.

## EVIDENCE 1 — anima's Lane-G "forge trainer" IS the hexa-lang `clm_prod` binary (no anima-side fix possible)
- anima has NO own forge device-resident train-step driver. The rung A-1 fire (`.verdicts/lane-g-3b-descent/`)
  ran `clm_prod` (the hexa-lang HEXA-FUSION harness). `grep -r forge_graph|HEXA_CUDA_GRAPH` over anima `*.hexa/*.c/*.cu`
  finds the CUDA-graph primitives `_forge_graph_{on,begin,commit,ready,launch}` are **NOT present anima-side** —
  they live only in `~/hexa-fusion-cuda-kit/cudagraph-build/runtime_cuda.c` (PR #2658, hexa-lang domain).
- Therefore anima's 3B/7B forge util ceiling == hexa-lang `clm_prod`'s util ceiling. There is no anima-side
  workaround (anima just invokes the binary), and `a_runpod_inbox` forbids locking the fix anima-side.

## EVIDENCE 2 — the CUDA-graph util lever is FALSIFIED upstream (verbatim, `~/hexa-fusion-cuda-kit`)
F-FUSION-GRAPH-AB.txt (④ fwd/bwd-only capture, vast H100_NVL idle, instance 39342863):
```
GRAPH=0 (eager)          util MEAN=11.85% PEAK=71% pct>=20=23.9% n=293  median 2%   CE 4.46624->3.64669 DESCENT PASS
GRAPH=1 (capture/replay) util MEAN=13.17% PEAK=77% pct>=20=24.1% n=291  median 2%   CE 4.46624->3.64669 DESCENT PASS (byte-eq)
=> falsifier "graph replay raises util MEAN >= 20%" FALSIFIED. +1.32pp. byte-eq CORRECT.
```
F-FUSION-GRAPH-WHOLESTEP-AB.txt (⑤ whole-step capture incl. AdamW, vast H100_NVL idle, instance 39346681):
```
g0   GRAPH=0 WHOLESTEP=0  util MEAN=14.87% PEAK=77% MEDIAN=2% pct>=20=24.8% n=294   CE 4.46624->3.64669 PASS
g1   GRAPH=1 WHOLESTEP=0  util MEAN=13.19% PEAK=77% MEDIAN=2% pct>=20=23.1% n=286   CE 4.46624->3.64669 PASS
g1ws GRAPH=1 WHOLESTEP=1  util MEAN=13.54% PEAK=77% MEDIAN=2% pct>=20=23.9% n=284   CE 4.46624->3.64669 PASS
=> falsifier "whole-step capture (AdamW in graph) raises util MEAN >= 20%" FALSIFIED. 13.54%. FAR under 20%.
   median util pinned at 2% across ALL THREE conditions. STOP — do NOT proceed to Phase-2 device-t.
```
ROOT-CAUSE (verbatim upstream): "host-launch-overhead is NOT the util ceiling on H100 — the binding constraint
is the SERIAL, FINE-GRAINED kernel DAG at this problem size. util-GREEN (>=20%) is NOT reachable by graph
capture of any region." The remaining levers are workload-shape (larger tiles / kernel fusion = codegen work),
NOT a capture env flag. This matches `a_cuda_graph_train` dont: "chase util-GREEN by growing the workload — util
DROPS as D grows" and "rely on single-stream async alone for util — CLOSED-NEG (launch-bound)."

The task's premise ("reached ~1.2x in the sibling repo") is numerically the +1.32pp / +11%-relative
graph gain — REAL but FAR below the 20% GREEN gate. 1.2x of ~12% is still ~13%, not ≥20%.

## EVIDENCE 3 — anima's OWN FORGE-UTILGREEN lever ladder is already closed-negative TERMINAL (HF.jsonl + lever-5 verdict)
lever-1..lever-5 all measured util-RED with byte-eq preserved (max|Δ|=0):
```
lever-2 d1536/T512  MEAN=0.4999% PEAK=19% pct_ge20=0   byte-eq F-RFC046-GEMMFEED-EQ=1
lever-3 d1536/T512  MEAN=0.5616% PEAK=21% pct_ge20=0.57% byte-eq (all devfeed/conv2 oracles max|Δ|=0.0)
lever-5 d1536/T512  MEAN=0.6619% PEAK=38%  A-vs-B RULING = (B) WORKLOAD-BOUND TERMINAL · host-feed axis CLOSED-NEGATIVE HONEST
```
And the SECOND, independent anima-side wall (rung A-1 VERDICT.md, the forge interpreter):
- forge IS device-resident at 1–1.5B on one H100 (DEVMEM up to 64.9GB, PEAK 100%, 3-GATE PASS) — substrate proven.
- BUT the per-step INTERPRETED host conv loop is ~20–30 s/step at d9216 (O(d²) host repack) → a clean
  descent-PASS at ≥1B is interpreter-wall-impractical in bounded budget. True-3B-dim (d=15811) is even
  host-allocation-bound (probe3B never reached the GPU). The descent axis at ≥1B needs the deferred
  option-B device-resident CUDA-C rewrite — which is the SAME kernel-DAG-collapse work the util wall needs.

## DECISION (per task HARD PREFLIGHT GATE + `a_completeness_over_cheap`)
- Phase-1 util-gate (HEXA_CUDA_GRAPH on, 402KB C4): the config is KNOWN util-RED (≤13.54% measured upstream).
  Running it would fabricate nothing new and re-confirm a closed-negative at cost. **NOT FIRED.**
- Phase-2 production (3B/7B on v2 default-lane 12.5MB): gated behind util-GATE GREEN AND descent-GREEN-with-fusion.
  util-GATE cannot pass with the current lever family. **NOT FIRED.**
- 7B: gated behind 3B closure. **NOT FIRED.**
- NO GPU rented. NO util-GREEN fabricated. The single real remaining unblock is HEXA-FUSION-domain
  codegen (kernel fusion past L3-b / option-B device-resident full-step CUDA-C rewrite that collapses the
  fine-grained serial DAG into fewer SM-saturating kernels), already in flight UPSTREAM in hexa-lang.

## INBOX (a_runpod_inbox) — already filed upstream (no duplicate created)
The exact cross-repo dependency is already filed: `hexa-lang/inbox/patches/anima-laneg-forge-util-fusion-binding.md`
(date 2026-06-05): "anima's Lane G forge trainer is literally the hexa-lang clm_prod binary … cannot reach
util-GREEN until hexa-lang's clm_prod does … No anima-side workaround exists, so this must NOT be patched
anima-side." This verdict file is the anima-side record that companion patch already references.

## CONFIRMATIONS (task report-back contract)
- byte vocab V=256 throughout (forge .clm byte-vocab BY CONSTRUCTION — confirmed; not changed).
- production corpus WOULD be v2 default-lane `dancinlab/anima-corpus-5lang-unified-v2` (~12.5MB, byte V=256),
  NOT the 402KB C4 (402KB reserved for the util-gate mechanics probe only). Not pulled — Phase-2 not reached.
- util-GREEN is NOT claimed. No MEAN ≥ 20% was measured with fusion. The closest measured is 14.87% (eager)
  / 13.54% (whole-step graph) — both RED.

## NEXT (unblock owner = hexa-lang HEXA-FUSION domain, not anima)
When upstream `clm_prod` crosses util-GREEN (kernel-fusion / option-B device-resident full-step rewrite that
collapses the serial kernel DAG), anima re-runs THIS preflight; if GREEN, the Phase-1 util ladder + Phase-2
v2-default-lane 3B/7B production fire proceeds unchanged (`a_fire_autonomous`, no cost gate).
