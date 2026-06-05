# M13 7B-undertrained ENGINE rung — run log

SOLE agent, ONE pod, run-to-completion. Base origin/main 9a83ad1e6 (#1864 grad-ckpt merged).

## config
- model: CLMConvMoE d6208 / L30 / E30 / K3 / V256 = ~7.057B params
- corpus: R2 phanes anima-7b/web/{eng,fra,deu,spa,kor}, GB_PER_LANG=3.0 -> ~15 GB -> tok/param ~2.1 (proper undertrained, target 1-2)
- train: seq (512 H200 / 256 H100), bs1, accum32, bf16, AdamW8bit, --grad-checkpoint, ~3500 steps bounded
- fire script: CLM/train/fire_7b_undertrained.sh (R2 per-lang Range-GET, serialize_v3 -> .clm v0.3)

## anti-deadlock discipline
- ONE on-demand (non-interruptible) pod. NO re-rent on loss (fail loud).
- POLL-INLINE in a single Bash loop, never arm a Monitor. Harvest the moment train says DONE.
- RATE-LIMIT storm = backoff 30->480s x8, never abort first hit.

## state
- (updated as run progresses)
