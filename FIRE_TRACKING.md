# FIRE_TRACKING — F-CURRICULA-1 (P21H v3 curriculum-mix)

Live fire-recovery tracking for the PURE F-CURRICULA-1 fire. SSOT for
the recover-and-monitor effort after the dispatcher died.

## Fire identity

- **pod**: `wfeksdl8e8f327` (1× A100 SXM, $1.49/hr), `SAVE_POD=1`, RUNNING
- **ssh**: `154.54.102.24:15857`, key = ubu-2 `~/.ssh/id_ed25519`
  (Mac → pod direct is BLOCKED; ubu-2 relay only)
- **variant**: Qwen2.5-1.5B init=qwen, seed=1337, steps=5000, lr=5e-5,
  bsz=2, block=512, warmup=100, noise-sigma=0.1, lambda-mitosis=0.05,
  mitosis-max=16, wiki-frac=1.0, ckpt-every=500
- **corpora**: multi_wiki_corpus.jsonl + corpus_s101.jsonl + mixed_corpus_built.jsonl
- **out**: `/workspace/p21hr/out_main/`

## Dispatcher-dead event (2026-05-25)

- ubu-2 dispatcher PID 412255 **DEAD** — poll budget 5400s < 6.4h train
  timeout, so auto-pull on `result.json` never fired. Pod retained by
  `SAVE_POD=1`, so artifacts are safe; recovery is external (this effort).
- Distinct from the EARLIER failed fire `c25njysjdga2vb` (dispatcher
  class-1 silent failure, NO_TRAIN_OCCURRED, already torn down — see
  `state/p21h_v3_curricula_recover_2026_05_25/README.md`). That pod
  produced zero artifacts. THIS pod (`wfeksdl8e8f327`) is a separate,
  genuinely-training fire.

## Monitor log

### 2026-05-25 16:27 UTC — re-poll start (dispatcher dead)
- step 1375/5000 (27%), CE=2.99, pool=16 (saturated at mitosis-max),
  splits=14, phi=0.6579, t=6351s
- python pid 310 ALIVE, state R, **CPU pegged ~15 cores** (jiffies
  +9108 / 6s), but **GPU util 1-2%, ~90W** — GPU-starved, CPU-bound
  dataloader/mitosis path is the bottleneck → slow ~4.6s/step.
- `device=cuda dtype=bfloat16` confirmed; model resident (25GB GPU mem).
- ckpts present on pod: ckpt_best.pt (6.0GB), ckpt_step500.pt,
  ckpt_step1000.pt + kosmos_anchors/ + mix_info.json.
- **ETA**: ~3625 steps left × ~4.6s ≈ 4.6h → ~05:30 KST 2026-05-26.
- Action: periodic poll (~12 min) via ubu-2 relay; recover on
  `result.json`. Re-polling because auto-pull is dead.

<!-- monitor appends below -->
