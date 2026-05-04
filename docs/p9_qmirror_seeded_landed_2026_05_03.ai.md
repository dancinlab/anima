# P9 qmirror-seeded ablation_A landed (2K mini)

date_utc: 2026-05-03T22:39:56Z
phase: p9_qmirror_seeded_ablation_A_2k
verdict: F_QSEED_1_PASS
cost_usd: 0.0 (ubu1 RTX 5070 local, $0)

## TL;DR

- ML training pipeline now seeded by qmirror QRNG (HMAC-DRBG SHA-256 <- IonQ Forte 1 4096-bit quantum entropy).
- 2K-step ablation_A mini: BLEU-1 = 0.006836, in noise band [0.005, 0.012] -> F-QSEED-1 PASS.
- phi star healthy: baseline 45.81, final 45.73, all-checkpoints-above-threshold-5.0 = true.
- Chain-of-custody verified at run start (first 1024 bytes re-derived match cond.4 attestation SHA).
- Total qmirror entropy consumed: 33068 bytes (32004 in train loop = 2000 steps * 4 batch * 4 bytes/uint32).

## What was patched

1. Global numpy seed: `np.random.seed(qmirror_uint32)` instead of `seed=42`.
2. Global torch CPU seed: `torch.manual_seed(qmirror_signed64)`.
3. Global torch CUDA seed: `torch.cuda.manual_seed_all(qmirror_signed64)`.
4. Python random: `random.seed(qmirror_uint64)`.
5. Per-step BatchSampler: replaced `np.random.choice(len(cache), BATCH, replace=False)` with `qmirror_batch_indices(...)` that draws `BATCH` unique uint32 mod n_cache from qmirror QRNG.
6. phi-partition rng: `np.random.default_rng(qmirror_uint32)` for the IIT partition permutations inside `compute_phi_star`.
7. Explicit `torch.Generator` seeded by qmirror, ready for any Dropout module that accepts `generator=`. (peft LoRA `dropout=0.0` here -> unused this run, but wired.)

## Comparison vs ablation_A 50K baseline

| metric             | ablation_A 50K  | qmirror 2K  | delta        |
|--------------------|-----------------|-------------|--------------|
| BLEU-1 (32-prompt) | 0.005859        | 0.006836    | +16.7%       |
| BLEU-1 (h500)      | 0.006513        | n/a         | -            |
| F2 phi final       | 44.607          | 45.731      | +1.124       |
| F3 tension MSE     | 7.782           | 8.502       | +0.720       |
| phi baseline       | 45.915          | 45.814      | -0.101       |
| n_steps            | 50000           | 2000        | -            |
| train sec          | 3115.08         | 179.76      | -            |

### Interpretation
- BLEU-1 shift (+16.7% on 32-prompt subset, +5.0% vs 500-prompt baseline) is well within the empirical noise band; the alpha=12 early-curriculum dominates at step 2000 and pushes CE harder than the 50K run sees in its extended mid/late bands.
- phi did NOT erode: qmirror final phi (45.73) is +1.12 above the 50K baseline final (44.61). All 6 checkpoints above the F2 threshold of 5.0.
- phi baseline difference (-0.101) is within float-stable matmul / cuDNN nondeterminism; qmirror seed material itself is bit-exact verified via chain-of-custody.

## Falsifier

**F-QSEED-1**: BLEU-1 in [0.005, 0.012] (noise floor maintained, no anomaly from qmirror seeding)
- Result: **PASS** (0.006836 inside band; z-position 0.262)
- Band rationale: lower from ablation_A 50K subset floor (0.00586); upper from 2x baseline / loose bound informed by ablation_B s42 outlier (0.0120).

## qmirror provenance chain (8 steps)

1. **Quantum source**: IonQ Forte 1 (Aria-class trapped-ion QPU via AWS Braket).
2. **Quantum circuit**: |+>^16 (16-qubit Hadamard product state), 256 shots, Z-basis measurement.
3. **Raw bits**: 4096 bits = 16 qubits * 256 shots.
4. **DRBG algorithm**: HMAC-DRBG SHA-256 (NIST SP 800-90A Rev.1 sec.10.1.2).
5. **DRBG inputs**: entropy = 4096-bit IonQ measurement; nonce = AWS Braket task ARN; personalization = `anima.nexus.qrng.ionq_forte1.2026-05-02`.
6. **Chain verification**: first 1024 output bytes re-derived in this run; SHA-256 = `ddf057ba61916c3183fe245345c6f5108e3ffb88fa573e33474f32740f0da81b` (matches `hmac_drbg_seed.json`).
7. **cond.4 attestation**: NIST SP 800-22 tier-1+ 7/7 PASS at 10^6 bits (clean reference impl, see `state/nexus_qmirror_nist_2026_05_03/`).
8. **ML consumption**: 33068 bytes total drawn (1064 setup incl. chain-verify-1024 + 4*8 seeds + 1*8 dropout; 32004 in train loop).

## Honest C3 caveats

1. HMAC-DRBG output is deterministic given seed; "quantum" status comes from the 4096-bit IonQ entropy input + cond.4 NIST tier-1+ 7/7 PASS attestation. Per-step uint32 draws are NOT live per-call quantum sampling. A future cycle could swap to ANU live (T1.b) or IonQ live-stream if api.quantumnumbers.anu.edu.au key / per-shot Braket pipeline are provisioned.
2. F-QSEED-1 noise band [0.005, 0.012] is empirically derived from a single 50K ablation_A baseline (BLEU-1=0.00586). There is no statistical confidence interval and no step-matched control (2K seed=42) was run; a strict equivalence claim would need >=3 paired (qmirror vs seed=42) runs at the SAME step count. This run only demonstrates "no catastrophic anomaly".
3. Seed coverage: patch reseeds np.random / torch.cpu+cuda / random / per-step BatchSampler / phi-partition rng / explicit torch.Generator for dropout. peft LoRA `dropout=0.0` in this config means the dropout-Generator is unused this run; in a non-zero-dropout setting, each Dropout module would need explicit `generator=` wiring (not done here).

## Artifacts

- ubu1 run dir: `/tmp/p9_qmirror_seeded_ablation_A_2026_05_03/`
- ubu1 savepoints: `/tmp/p9_qmirror_seeded_ablation_A_2026_05_03/savepoints/{step_500,step_1000,step_2000,final}/`
- local verdict: `state/p9_qmirror_seeded_2026_05_03/verdict.json`
- local trajectory: `state/p9_qmirror_seeded_2026_05_03/trajectory.json`
- local comparison: `state/p9_qmirror_seeded_2026_05_03/comparison_vs_ablation_A.json`
- local train script (.py only): `state/p9_qmirror_seeded_2026_05_03/p9_qmirror_seeded_ablation_A_2k.py`
- local train log: `state/p9_qmirror_seeded_2026_05_03/train.log`
- marker: `state/markers/p9_qmirror_seeded_landed.marker`

## Constraints honored

- raw#9: real GPU train (RTX 5070 cuda 12.8, torch 2.11.0+cu128), not mock.
- raw#15: env() lazy + <user> guarded; no migration.
- raw#10: deterministic-yet-quantum reproducibility (chain-of-custody verified at run start).
- $0 ubu local; runpod_used=false; destructive_ops=0.
- mac-local-equivalent ($0 dollar-zero policy).

## Next-cycle suggestions (not done this cycle)

- Step-matched control: seed=42 2K mini-run for paired comparison (would close caveat #2).
- Per-shot Braket live-stream variant: replace HMAC-DRBG expansion with on-demand IonQ shots (would close caveat #1; cost: per-shot Braket ~$0.01).
- Non-zero-dropout config to exercise the dropout-Generator wiring (would close caveat #3).
