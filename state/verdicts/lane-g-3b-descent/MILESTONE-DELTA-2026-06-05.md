# Milestone delta — 2026-06-05 · ENGINE 3B/7B Lane-G forge preflight STOP

> Self-contained milestone-delta note (this worktree is isolated; the shared
> `ENGINE+CLM+KOSMOS.log.md` lives on the monograph-entangled `campaign-pivot-descent`
> branch and is intentionally NOT forked here, to keep the merge conflict-free).
> Fold this one entry into `ENGINE+CLM+KOSMOS.log.md` when reconciling.

## ENGINE 3B → 7B Lane-G forge line — HARD PREFLIGHT GATE = STOP (util lever CLOSED-NEGATIVE)

substrate = GPU (Lane G) · forge flame · `a_lane_akida_gpu_split`. $0 — no GPU rented.

**Preflight result:** the HEXA-FUSION device-resident CUDA-graph train-step (the util unblock
this campaign was to deploy) is **falsified upstream** in `~/hexa-fusion-cuda-kit`:
- ④ fwd/bwd-only capture: util MEAN 11.85% → 13.17% (+1.32pp, byte-eq CE 4.46624→3.64669).
- ⑤ whole-step capture (AdamW in graph): util MEAN 13.54% (g0 14.87% / g1 13.19% / g1ws 13.54%);
  median util pinned at 2% across all three. The ≥20% GREEN falsifier is **FALSIFIED**.
- ROOT (verbatim): host-launch overhead is NOT the H100 util ceiling — the binding constraint is
  the SERIAL fine-grained kernel DAG; util-GREEN is NOT reachable by graph capture of any region.

**Why STOP, not fire:** anima has no own forge train-step driver — its Lane-G trainer IS the
hexa-lang `clm_prod` binary (`forge_graph`/`HEXA_CUDA_GRAPH` absent anima-side). The Phase-1
util-gate config is therefore KNOWN util-RED (≤13.54%). Renting a GPU would re-confirm a
closed-negative at cost — forbidden (`a_completeness_over_cheap`). Phase-2 production (3B/7B on the
v2 default-lane) and 7B are gated behind util-GATE GREEN, which the current host-removal lever
family cannot pass. Corroborated by anima's own FORGE-UTILGREEN lever-1..5 (all RED byte-eq;
lever-5 = WORKLOAD-BOUND TERMINAL host-feed CLOSED-NEGATIVE) and the rung A-1 forge-interpreter
wall (~20–30 s/step at d9216 makes a clean ≥1B descent-PASS impractical in budget).

**Milestone flips:**
- ENGINE 3B (Lane G, forge) PUBLIC → 3B production: **HONEST-BLOCKED** — pending an upstream
  HEXA-FUSION codegen unblock (kernel fusion past L3-b / option-B device-resident full-step
  CUDA-C rewrite that collapses the serial kernel DAG). NOT a PASS, NOT fabricated GREEN.
- ENGINE 7B (Lane G, forge): **GATED behind 3B closure** — unchanged, not attempted.

**Artifacts (this work):**
- `.verdicts/lane-g-3b-descent/PREFLIGHT-FUSION-STOP.md` (full verbatim verdict).
- `.discoveries/engine-3b-fusion.tape` (@D discovery, RED CLOSED-NEGATIVE target).
- inbox dependency already filed upstream: `hexa-lang/inbox/patches/anima-laneg-forge-util-fusion-binding.md`.

**Confirm:** byte vocab V=256 throughout (forge byte-vocab by construction). Production corpus
WOULD be v2 default-lane `dancinlab/anima-corpus-5lang-unified-v2` (~12.5MB), NOT the 402KB C4 —
Phase-2 not reached, so not pulled. No util-GREEN measured (closest 14.87% eager, RED). No HF
upload (no new artifact — STOP produced no ckpt). No pod rented → none to tear down.
