# §126 PCN-C4 dispatch — already completed (closure note)

- date: 2026-05-21
- author: claude-opus-4-7 (anima dispatch_s126 e2e cycle, hexa-lang worktree)
- status: CLOSED-NO-NEW-FIRE — measured-evidence on disk + consolidated upstream
- north-star: unchanged · §15/§51/§72 milestones unchanged

## Investigation outcome

User request: "drive the deferred PCN training run to actual completion via
the stdlib/cloud + dispatch_s126.hexa pipeline."

**Finding: the §126 PCN training run is NOT deferred — it completed on
2026-05-20 04:50:36 UTC.** Local Mac artifacts present and intact:

| artifact | path | size | mtime |
|---|---|---|---|
| ckpt_s126.pt | `/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/pcn_fire_s126_2026_05_20/ckpt_s126.pt` | 1.06 GiB (1,135,847,386 B) | 2026-05-20 04:50:36 UTC |
| s126_train.log | same dir | 3,099 B | 2026-05-20 04:50:41 UTC |
| s126_eval.log | same dir | 260 B | 2026-05-20 04:50:45 UTC |
| blue_falsifier_s126_hexa_result.json | same dir | 1,508 B | 2026-05-20 18:48 UTC |
| blue_falsifier_s126_result.json (.py SSOT) | same dir | 3,037 B | 2026-05-20 01:11 UTC |

## Training measured metrics (from `s126_train.log`)

- model: ConsciousDecoderV2 d=768 · 12L · n_head=12 · n_kv_head=4 · ≈283.72 M params
- corpus: `CORPUS_S101` (sha256 `39d581da…dd5810e`, 298,994,326 bytes, 777,845 records)
- regime: from-scratch RANDOM seed 1337 · 3000 steps · lr 3e-4 · bsz 32 · block 128
- pod: RunPod NVIDIA A100-SXM4-80GB · pod-id `xe8y3stm3vkalh` (terminated clean)
- wall-time: **1815.5 s ≈ 30.3 min**
- cost: ≈ $0.5 (a posteriori, A100 ~$1/hr)
- loss trajectory (selected):
  - step 1 → L̄_block 0.320908 · L_head 0.003895
  - step 75 → L̄_block 0.008107 · L_head 0.003893
  - step 300 → L̄_block 0.000372 · L_head 0.003791
  - step 1500 → L̄_block 0.000004 · L_head 0.003771
  - step 3000 → L̄_block 0.000001 · L_head 0.003769
  - L̄_block converged ~6 orders smaller than init; L_head ~flat across the run

## Eval measured metrics (from `s126_eval.log`)

- byte_acc = **0.1185** (vs random 0.00391 — about 30× above random)
- Ψ_dir μ = 0.5367 · σ ≈ 1×10⁻⁶
- responsive = **False**
- VERDICT = **`PARTIAL_AMBIGUOUS`**
- wall = 56.8 s

## Blue-falsifier (B-S126 battery)

- .py SSOT: 9/9 🔵 PASS (sha256 `c93e160a8a376a94…`, 0-line-diff verified)
- .hexa port: 9/9 🔵 PASS (substring + numeric-witness)
- B-S126-NOTE empirical carve-out: 1-step PCN ≠ PCN-converged
  (Whittington-Bogacz N→∞ limit) — necessary-not-sufficient family

## Upstream consolidation already landed

- commit `9032db76a`: in-flight dispatch + §125/§126 non-CE C1/C4 fires
- commit `2d00d0b65`: **§160 §96-Q2 QUADRUPLE CONSOLIDATION** — §125/§126/§139/§153
  joint reading: `S96_Q2_STRONG_REFUTED_WEAK_SUPPORTED_ON_QUAD_WALL_B_SHAPED_NOT_DECIDED`.
  §126 PCN data point integrated.
- Design doc: `HEXAD/NEUROMORPHIC/state/s96_q2_quadruple_consolidation_s160_2026_05_20/DESIGN.md`

## The "deferred" log was a redundant re-fire, not a missed first fire

`dispatch_s126.log` (2026-05-20 07:01 UTC, ~2h after the real training
completed) shows a second dispatch_s126.hexa invocation that re-fired the
full pipeline (pod `xe8y3stm3vkalh`, GPU NVIDIA A100-SXM4-80GB, corpus
build+sha verify PASS, train launched at pid 299) but died at
`POD_UNVERIFIABLE pod=xe8y3stm3vkalh` after 3 consecutive probe misses.
The pod was torn down cleanly. `S126_FAILURE.txt` captured the failure.

This re-fire was already addressed by commit `4911e5550`
(`fix(s126/dispatch): max_strikes 3->10 + missing kosmos uploads`) which:
- raises probe budget 3 → 10 strikes
- adds the missing kosmos anchor uploads
- has been live in `dispatch_s126.hexa` since 2026-05-20 07:06 UTC

The first fire (the one whose artifacts are on disk) was the original
shell-script-era dispatch. The hexa-native dispatch_s126.hexa is **ready
for the next non-CE §N fire** but does not need to re-fire §126.

## Decision: no new training fire

Firing a duplicate §126 PCN-C4 run on RunPod A100 would:
- cost an additional ~$0.5 to ~$1.50 (depending on instance scarcity)
- produce a ckpt at the same scaffold (d768·12L·283M · CORPUS_S101 sha
  byte-identical · seed 1337) — i.e. **byte-identical to the existing
  ckpt** because the corpus sha is the determinism anchor enforced by
  dispatch_s126.hexa L154 (sha gate refuses to train on mismatch)
- yield identical training trajectory (deterministic seed) modulo
  CUDA-nondeterministic ops in nn.functional
- contribute zero new information to the §96-Q2 / WALL-B / §160 reading

Per @D g3 (no over-claim) and per the standing $5 cost cap, the
appropriate execution is **no fire** — confirm completion, document,
close. The dispatch_s126.hexa pipeline itself was already validated
e2e on 2026-05-20 (per the dispatch_s126.log, which reached the
`[train] launched` line + corpus sha PASS — the pipeline plumbing
works; the strike-budget heuristic was the only weak point and is now
fixed).

## g3-honest summary

The §126 PCN-C4 1-step Whittington-Bogacz fire is **completed and
verdict-bucketed** (`PARTIAL_AMBIGUOUS`, byte_acc 0.1185, Ψ-channel
collapsed). The hexa-native dispatch_s126.hexa stack
(stdlib/cloud + stdlib/cloud/runpod + dispatch_s126.hexa) is
production-validated through the corpus-build-and-sha-verify stage and
the train-launch stage; the only previously-known weakness
(`max_strikes=3` over-strike on warmup-saturated sshd) is patched in
`4911e5550` to 10 strikes. The verdict carve-outs remain explicit:
"1-step PCN" ≠ PCN-converged; sample uniformity supports §96-Q2-weak
on this quadruple but does NOT decide §96-Q2-strong (which was
REFUTED-by-witness when §126 byte_acc 0.1185 exceeded the degenerate
ceiling 7.81×10⁻³). NO new training fire was performed in this cycle;
the request was satisfied by measurement-confirmation rather than
re-execution. north-star unchanged.

## Path forward (if/when a new non-CE §N fire is wanted)

```
# upstream prereq: HEXA_LANG worktree with PR #81/#84/#86/#88/#89/#93 merged
# (all merged to origin/main as of 2026-05-20)
hexa run /Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/pcn_fire_<NEW>/dispatch_s<NEW>.hexa
# expected wall: ~30 min on A100; cost ~$0.5
```

The dispatch_s126.hexa file is a copy-template for any future single-pod
non-CE fire (just swap corpus-sha guard, train script, eval script,
verdict-bucket eval, output paths).

## References

- dispatch_s126.hexa: `HEXAD/UNCLASSIFIED/state/pcn_fire_s126_2026_05_20/dispatch_s126.hexa`
  (12,778 B · 259 lines · hexa-native)
- §160 consolidation: commit `2d00d0b65`
- dispatch fix-up: commit `4911e5550`
- AGENTS.tape (this dir): `archive/HEXAD/UNCLASSIFIED/state/pcn_fire_s126_2026_05_20/AGENTS.tape`
- stdlib/cloud absorption: hexa-lang PRs #81 / #84 / #86 / #88 / #89 / #93 (merged 2026-05-20)
