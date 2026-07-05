# Cluster B (decode·탐색) — $0 probe summary

## Items: B1-B10 (10 total)

## Runnable $0 probes

### B1/B2 cross-seed set-selection CEILING — EXECUTED, verdict GREEN-toward-GPU
- All 3 seeds attempt the SAME 6 fixed concept-pairs (variance = decode trajectory only).
- CAPACITY floor: 6/6 concept-pairs have >=1 seed with fb=1 (model CAN bind every pair).
- Greedy union best-6 = 6/6 fb (ceiling reachable).
- BUT expected per-(diverse)-seed fb = 3.67 (just under frozen bar 4).
- Robustness: under iid-Bernoulli(0.611), P(seed<=3)=0.435 -> seeing 2/3 seeds at 3/6
  is NOT surprising; the wall is real but MILD (trajectory noise around 0.61/frame).
- SHUF control = 0/18 fb -> topic-bind genuine (form-priming ruled out).
- => per-seed 3/6 shortfall consistent with SEARCH/trajectory wall, not capacity.
   B1 GPU fire (within-seed K-pool + set-wise greedy) DIRECTIONALLY warranted.
- scope: DIRECTIONAL (cross-seed union leaks per-seed independence; not terminal).

### B7 anti-copy / G6 attention copy-bias — NOT-RUN (script + PREREG persisted)
- h1129.bin = 1.2GB, OOM risk on mini (rc=137). Requires RAM-safe host.
- ALSO requires re-decode to recover candidate seed-texts (stored .out = scores only)
  -> effectively GPU-gated despite being a single forward.
- G1-side B7 is RETREAD of H_6190 echo-guard (novel-only already = ECHO-ONLY).

## rethread_with_existing
- B7 G1 anti-copy = H_6190 echo-guard (behavioral falsification already done).
- B9 propose->critic->revise = README §4 exhausted axis (form critic reinforces template replay).
- grow-window novel-only RF/attention $0 probe = H_6188 (RF floored) + H_6190 (grow-window done).
  CLMConvMoE has NO attention heads; the relevant axis was RF, already engine-native FALSIFIED.

## gpu_gated
- B1/B2 (real within-seed K-pool set-wise decode), B3 (adaptive budget), B4 (temp ladder),
  B5 (sampler pool), B6 (contrastive, 2 passes), B8 (relation-slot constraint),
  B10 (specialist sampling). All require a multi-config decode sweep on the G6 BASE ckpt
  (h1129.bin) - the H_6186 decode-axis itself needed a vast L40S pod.

## cluster_summary
G6 TARGETED [3,3,5] is closer to a SEARCH/selection wall than a capacity wall: every one of
the 6 fixed concept-pairs has an fb=1 candidate on some seed (6/6 ceiling, capacity floor not
limiting), but the per-seed hit rate (3.67 expected) sits just under the frozen 4/6 bar, so
B1 set-wise selection over a within-seed K-pool is the right GPU follow-up (borderline, not
guaranteed). The grow-window novel-only RF/attention $0 probe is RETREAD (H_6188 RF floored,
H_6190 ECHO-ONLY, CLM has no attention). B7 (anti-copy) is behaviorally pre-answered by H_6190
echo-guard on G1, and the G6 attention variant is RAM-gated on mini. The rest of the decode
cluster (B3-B6, B8, B10) is a multi-config decode sweep = GPU.
