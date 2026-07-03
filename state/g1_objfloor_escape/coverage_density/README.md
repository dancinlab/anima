# coverage_density — H_6185 recipe: L8-RF retrain + engine-native G1 judge

**Lever:** data-coverage-density + receptive-field (arch-independent, H_6182-6185).
Census (#2904) flagged coverage-density as this session's strongest MISSED positive;
H_6185's explicit recipe (RF L4→L8 + combination-coverage corpus + 303M retrain +
frozen G1 re-judge) had never been fired end-to-end. This worktree is state-only
(no HYPOTHESES/commit/PR); the two engine surfaces both hit **infra walls**, so the
terminal G1 flip is **INFRA-BLOCKED**, not a science result.

| step | status |
|---|---|
| (1) RF L4→L8 wiring | **DONE** — hexa `L_canon 4→8` + `--py --L 8` documented; RF math verified |
| (2) combination-coverage corpus | **DONE** — verified block reused, gate-aligned, held-out=0 (independently rechecked) |
| (3) 303M retrain | **INFRA-BLOCKED** — heavy GPU; pool troubled/high-load; pod cost/explicit-go gated (💸 4th-pod ban) |
| (4) frozen G1 judge | blocked by (3); also anima CLI build wall on this mac (below); fire-ready command staged |

## (1) RF L4→L8 wiring  (worktree edits — the `wired:` surface)

RF (kernel=3, dilation_base=2, cap 512): dils=[1,2,4,…,min(2^(L-1),512)], RF=1+2·Σdils.
- L4 → dils [1,2,4,8], Σ=15, **RF = 31 bytes** (undersized — a pair rarely co-occurs inside it).
- L8 → dils [1,2,4,8,16,32,64,128], Σ=255, **RF = 511 bytes** (within the 512 cap; matches the
  H_6184 dilated-conv RF-wall prescription). Decode is L-general (`.clm` v0.3 header carries
  n_trunk_layers) → the trained L8 `.clm` mounts on `core/decode.hexa` with no decode edit.

Wired in the worktree (isolated, uncommitted — task constraint state만):
- `cli/train.hexa` MODE_CANON `L_canon: 4 → 8` (hexa trainer path, currently GPU-util-fix / fp64-OOM).
- Canonical **working** retrain path = torch `anima train --py --arch clm --L 8` — RF set by the
  `--L` CLI arg (n_trunk_layers → CLMConfig → CausalDilatedConv1d). See `fire_l8_canon.sh`.
- Warm-FT from h1129 (L4 trunk): the per-key shape guard loads the shared trunk.0-3 layers and
  freshly-inits the new trunk.4-7 (grow-RF warm-start — valid, no shape_bad).

## (2) combination-coverage corpus  (corpus/ + corpus_design.json + corpus_verify.json)

Byte-identical reuse of the independently-verified block from `state/g1_coverage_prod_block/`,
which satisfies H_6185 §2 AND aligns held-out to the frozen G1 gate:
- N=40 concepts (unique substring-free ATTR each), C(40,2)=780 pairs.
- **Held-out 40** = the 10 frozen G1 gate-internal pairs (consciousness·tension·memory·silence·
  dream — `tool/gauge_lib.py` CONCEPTS) + 30 random → the gate's exact measured pairs are
  UNEXPOSED = memorization-free recombination, not leakage.
- Covered = 25% of POOL (185 pairs), 600 reps/covered-pair, byte-gap ≤25 (co-expressed inside RF).
- **Independent recheck (this worktree, not trusting design.json):** en+ko gate-internal pair
  co-occurrence = **0 / 0** across all 10 pairs; coverage 25.0% (≥20% bar); density 19,326
  pair-lines/MB; size 5.744 MB (en 3.10 + ko 2.64). `--sample proportional` at train = memo guard.

## (3) 303M retrain — INFRA-BLOCKED

**Path.** Canonical working retrain = torch `anima train --py` (cli/train.py Lane-P). The hexa
trainer (cli/train.hexa) is under GPU-util fix AND OOMs on 12GB GPUs (convergence `train-hexa-1`:
fp64 farr, 1.37GB/buf — L8's 8 layers make it strictly worse). The torch path is fp32/bf16 → fits
12GB, but it is a heavy multi-hour 303M GPU job.

**Host reality this session** (heavy → pool/pod, never mini · rc=137 swap OOM):
- summer (RTX5070 12GB) 🟢 but high-load + heavy-job OOM/wedge risk (summer-overfire); aiden 🔴
  reboot-loop. akida no-GPU; ghost blocked.
- 24GB+ rented pod = the clean path but **cost/explicit-go gated** under the standing session
  constraint "💸 4th 렌트 금지" (memory h9107) → NOT autonomously provisionable by this subagent.
- Est. when unblocked: A100-40GB ~$1.2/h × ~2–4h warm-FT (2000 steps) ≈ **$2.5–5**. PULL ckpt
  before teardown (a_fire_recover_complete).

**Fire-ready:** `fire_l8_canon.sh` — warm-start h1129c_chat.pt, `--py --arch clm --L 8`,
`--sample proportional`, held-out val, then the step-4 `anima evaluate --py` judge. Drop onto a
free GPU host, `hx install anima` (+ the CLI fix below), run.

## (4) frozen G1 judge — staged; also blocked by an anima CLI build wall on this mac

`anima evaluate --py <clm> --gen 80` (session-eval-py-only canonical, TERMINAL-eligible). G1
RECOMBINATION passes iff some k: composed_distinct ≥2 AND >max_single AND coherent, on held-out
gate pairs. ≥threshold → coverage-density POSITIVE (G1 opens as a data-coverage/RF lever); below →
coverage is also floor. Frozen bar, no post-hoc move.

**CLI build wall (separate infra finding, anima-hexa-1):** on a fresh checkout the whole `anima`
CLI fails to compile — TWO issues surfaced building on this mac:
1. **`EngineConfig` missing-field codegen error** — `cli/anima.hexa:1643-1644` construct
   `EngineConfig{…}` without the `forward_model` field that H_9119 added to the struct (+ its
   default ctor line 125). A real pre-existing bug that breaks EVERY `anima <verb>` (incl. `--py`,
   since the launcher compiles anima.hexa before dispatching to python). **Fixed in this worktree**
   (added `forward_model: false` to both literals) — recommend the parent land this on main.
2. **linker `_main` undefined (arm64)** — after fix #1, the full-stack anima build (13705-line
   engine_cli inline) fails at link. This is the `anima-hexa-1` toolchain wall (stale hexat /
   runtime carrier), NOT the L8 change and NOT a science ceiling — needs pool hexat currency /
   dedicated heavy-compile box, out of scope for this G1 verdict.

→ the $0 engine-native L8 descent smoke (which would have proven the L8 trunk end-to-end via
`anima train` MODE_VERIFY) could not run on this mac. Bug #1 IS fixed; bug #2 is a toolchain wall.

## Verdict — INFRA-BLOCKED

Steps 1+2 complete (L8 trunk wired both paths + gate-aligned coverage corpus, held-out=0
independently reverified). The terminal G1 flip (steps 3+4) is blocked by TWO independent
**infra** walls — a heavy-GPU/no-pod host wall (retrain) and the anima-hexa-1 full-stack build
wall (CLI), neither a science ceiling. coverage-density stays a **distinct, un-refuted lever**
(orthogonal to the A11 TPR-contrastive lane) — the missed positive is **staged and fire-ready**,
not falsified. No frozen bar moved; held-out strictly 0. Follow-on ING: fire `fire_l8_canon.sh`
on a free 24GB+ pool/pod once the CLI EngineConfig fix lands and a host is free.
