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

### 2026-05-25 16:43 UTC — anchor step1500 (ja_ja); 17:43 best ckpt step2375 CE=2.3786
Steady progress 1375→3000 over the polling window. Best CE 2.3786 @ step2375.
Anchors emitted at each 500-step ckpt across ru/ja/ko languages.

### 2026-05-25 18:31 UTC — last GOOD poll: step 3000/5000 (60%), ko_ko anchor written
Last confirmed live state.

### 2026-05-25 18:43 UTC — POD DEATH detected (Connection refused)
- SSH port 15857 → **Connection refused** on 18:43, 18:55, and 3 manual
  retries (15s apart). Host `154.54.102.24` PINGS fine (0% loss, 184ms)
  but **port 15857 REFUSED** = RunPod container stopped/terminated (the
  physical proxy host stays up; the per-pod forwarded port dies when the
  container dies).
- `runpodctl pod list -a` returns `[]` under the WORKING key
  (`rpa_43SES1…`, 50-char, secret-store) → pod `wfeksdl8e8f327`
  **not in this account's pod list** (running OR exited).
- Key audit: Mac `~/.runpod/config.toml` + ubu-2 `~/.runpod/config.toml`
  both hold a STALE 52-char `rpa_43SES…` key → **401 unauthorized**.
  Only the Mac secret-store key (50-char `rpa_43SES1…`) authenticates,
  and it sees ZERO pods. `hexa cloud` has no list verb (transport only).
- **Verdict: F-CURRICULA-1 (wiki_frac=1.0 curriculum-mix) re-fire LOST**
  at step 3000/5000. Pod gone, artifacts unrecoverable (on-pod volume,
  invisible to the working key). No mid-ckpt pull possible.

### Why this is NOT a total mission loss
- The dead pod's variant was the **wiki_frac=1.0** extreme of the corpus
  sweep. That endpoint is ALREADY a published closed-negative point
  (`dancinlab/anima-v3-e3` PUBLIC, wiki=1.0) and is covered by the
  `pure_wiki_sweep` CLAIMS.tape claim. The lost run would have, at most,
  reinforced the existing closed-negative (curriculum ORDERING of the
  same pure-wiki corpus); it was very unlikely to break the ceiling.
- A SEPARATE, fully-completed **wiki_frac=0.3** P21H V3 run already exists
  locally at `state/p21h_v3_recover_2026_05_25/out_main/` (step 5000,
  byte-exact ckpts, recovered earlier from a SIGHUP-orphaned pod). It
  was NOT yet HF-uploaded. This recovery uploaded it tier-gated PRIVATE
  (closure FAIL) and judged it — it adds the wiki=0.3 sweep point.

### Monitor stopped (task b38si25lg) — pod dead, no further poll value.
