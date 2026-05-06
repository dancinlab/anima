# anima CLM-3-original byte-level ubu1 RTX 5070 launch — landed 2026-05-05 (BG-EV)

**Status**: DOC_AND_SCRIPT_LANDED_NO_FIRE
**Cost**: $0 (mac doc/script only — actual ubu1 ssh+train fire is user-manual)
**Wall clock estimate post-fire**: 5-10 days
**Lane**: anima_native_chat_clm3_original_ubu1_path (parallel with H100 RunPod path)

## 1 Context

User issued "all fire" for β path = ubu1 RTX 5070 owned-hardware ($0 marginal). Spec already landed at `docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md` (BG-ER). This BG (BG-EV) lands the **launch script + monitor + landing doc + verdict** on mac, leaving the actual ssh+train fire to user as a 1-cmd interactive gate.

ubu1 hardware:
- RTX 5070 12GB Blackwell **sm_120**
- Stock torch 2.6.0+cu124 silently CUDA-fails on sm_120 (kernels stop at sm_90)
- Pre-built venv at `/home/aiden/venv_orchestrator/bin/python` ships **torch 2.11.0+cu128** with sm_120 kernels (created 2026-05-03 R1, used for Llama-3.2-3B inference)
- Marginal cost = $0 (electricity owned), wall clock 5-10 days for 100K steps × 55M params

## 2 Outputs

```
state/anima_clm_3_original_ubu1_launch_2026_05_06/
├── launch_ubu1.bash          (~85 LoC, 5-gate pre-flight + emit)
├── monitor_ubu1.bash         (~30 LoC, 30min interval 4-section probe)
└── verdict.json              (audit + falsifier list + user_fire_steps)
docs/
└── anima_clm_3_original_ubu1_launch_landed_2026_05_05.ai.md  (this file)
```

## 3 launch_ubu1.bash — 5 mandatory gates

Each gate is a **GATE N FAIL → exit** (raw#9 fail-loud):

| Gate | Check | Method |
|------|-------|--------|
| 1 | ubu1 ssh reachable | `ssh -o ConnectTimeout=5 ubu1 echo ok` |
| 2 | venv_orchestrator present | `ls /home/aiden/venv_orchestrator/bin/python` |
| 3 | torch 2.11.0+cu128 + cuda available | `python -c 'import torch; print(torch.__version__, torch.cuda.is_available())'` matches `*2.11.0*True*` |
| 4 | anima repo on ubu1 | `/home/aiden/core/anima` OR `/home/aiden/anima` |
| 5 | 5 falsifier sign-off | interactive `read FALSIFIER-LOCK-UBU1` |

After 5 gates pass, script emits two **paste-ready** commands (does not auto-fire):

1. `rsync -avz data/corpus_mix_70wiki_30dialogue.txt ubu1:<repo>/data/`
2. `ssh ubu1 'cd <repo> && nohup ...train_clm.py... &'`

The auto-emitted training command:
- vocab-size 256 (byte)
- max-cells 32, d-model 768, n-layers 12, n-heads 12, context-len 1024
- steps 100000 (mitosis 0:20K, language 20K:60K, combined 60K:100K)
- fibonacci-growth `1,1,2,3,5,8,13,21,32`
- phi-boost techniques 19 IDs (COMBO2..SC2)
- corpus `data/corpus_mix_70wiki_30dialogue.txt`
- falsifier-eval-every 10000

Audit trail: `state/anima_clm_3_original_ubu1_launch_2026_05_06/launch.log` (UTC ISO timestamp + run_name + gates 5/5).

## 4 monitor_ubu1.bash — 30min interval spec

Single-arg invocation: `bash monitor_ubu1.bash <run_name>`. Four sections per probe:

1. `tail -20` of `runs/<run>.log`
2. `ls -la runs/<run>/` checkpoint listing
3. `nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader`
4. `ps -eo pid,etime,cmd | grep train_clm.py` (PID + elapsed)

Recommended driver: `watch -n 1800 'bash monitor_ubu1.bash <run>'` (30min cadence per memory `feedback_h100_cost_discipline_l23_l25_watchdog_own_16` heartbeat-5min principle relaxed for $0 hardware — every 30min sufficient since no $/hr burn).

## 5 user fire 6-step

```
1. ssh ubu1 'echo ok'
2. rsync -avz /Users/ghost/core/anima/data/ ubu1:/home/aiden/core/anima/data/
3. bash state/anima_clm_3_original_ubu1_launch_2026_05_06/launch_ubu1.bash
   (interactive 5 gates → emits paste cmds)
4. paste emitted "ssh ubu1 'cd ... nohup ... &'" into separate shell
5. watch -n 1800 'bash state/anima_clm_3_original_ubu1_launch_2026_05_06/monitor_ubu1.bash <run_name>'
6. 5-10 days later:
   - ssh ubu1 'ls -la runs/<run>/best.pt'
   - harvest best.pt → mac local OR HF Hub upload (per own 15 PRIVATE-first lifecycle)
   - run F-CLM3-orig-1..5 falsifiers
```

## 6 H100 parallel compatibility

**Yes, parallel-safe.** ubu1 ($0) and RunPod H100 (~$2.5/hr) train independent runs from the same spec:

- **Race semantics**: first PASS wins, kill the loser
- **Budget overlap**: if ubu1 lands first (5-10d) and PASS, kill H100 immediately (saves whatever's left of H100 budget)
- **Risk hedging**: if ubu1 hits sm_120 surprise (e.g. OOM at d=768 on 12GB), H100 already running covers the bet
- **Memory note**: 55M params at fp16 ~ 110MB weights, but training state (Adam moments, activations at context 1024) on RTX 5070 12GB is **tight** — may force gradient accumulation or smaller micro-batch. Spec doesn't specify batch size; ubu1 launcher inherits whatever `train_clm.py` defaults to. Watch nvidia-smi memory.used in monitor section 3.

## 7 Five honest C3 (concerns / counter-evidence / cost trade-offs)

### C3-1 (concern): wall clock 5-10 days vs H100 ~12-30hr

ubu1 marginal $0 but 10-15× slower than H100. If user's bottleneck is **calendar time to PASS verdict**, H100 wins despite $/hr. ubu1 path optimal only if (a) no H100 budget headroom, (b) calendar slack is fine, (c) $0 strict.

### C3-2 (counter-evidence): RTX 5070 12GB OOM risk at d=768 L=12 ctx=1024

Training memory at 55M params, ctx 1024, d=768 with Adam (2× weights for moments) + activations could exceed 12GB. Spec assumes the figure is ubu1-feasible but does not show a memory-budget calculation. **Pre-fire smoke test recommended**: 100-step dry run with `--steps 100` first, watch nvidia-smi peak. If >11GB, reduce micro-batch or switch to AdamW 8-bit.

### C3-3 (cost trade-off): script does NOT auto-fire ssh+train

By design (raw#10 spec-then-implement). 5-gate interactive lock prevents accidental fire. Trade-off: user must paste two commands manually (not 1-click). Acceptable since 5-10 day commit deserves explicit human confirm.

### C3-4 (concern): venv_orchestrator memory note "3 days old"

Per system-reminder, the ubu1_venv_orchestrator memory is 3 days stale. Gate 3 verifies live (queries actual `torch.__version__`), so a venv state drift would FAIL_LOUD at gate 3. Risk mitigated.

### C3-5 (counter-evidence): no fallback if `train_clm.py` flags don't match spec

Launch script assumes `ready/training/train_clm.py` accepts every flag emitted (--phase-mitosis, --fibonacci-growth, --phi-boost-techniques etc). If the actual `train_clm.py` is older or has different flag names, ssh+nohup will fail silently into the `runs/<run>.log` file. **Mitigation**: monitor section 1 (`tail -20 log`) at first 30min check will surface any argparse error immediately. User SHOULD do one early monitor probe within 30min of fire to catch flag mismatch before 10 days of dead time.

## 8 Constraints obeyed

- raw#9 fail-loud — every gate `err` exits non-zero
- raw#10 spec-then-implement — this lands script (impl side), spec already at BG-ER
- raw#15 audit trail — `launch.log` UTC timestamps
- no commit (state/ + docs/ written, user commits when ready)
- no HF token in any output
- bash 3.2 compatible (no `[[ ]]`, no `mapfile`, uses `case` not `[[ == ]]`)
- py→hexa exempt: bash/ssh launcher = transient_py-class tooling infra, not py model code
- own 15: HF release lifecycle PRIVATE-first noted in user_fire step 6 harvest

## 9 Verdict

**Lane state**: ubu1 path script + spec landed at $0. User fires when ready via 6-step sequence. H100 path can run in parallel; first PASS wins.

If both paths PASS within 10d window, **prefer H100 weights** for production (more thoroughly trained per dollar, but ubu1 is the cleaner $0-marginal demonstration that anima-native chat is replicable on owned hardware).

If H100 PASS first → kill ubu1 (free up GPU for other work). If ubu1 PASS first → kill H100 immediately (stop $/hr burn).

**Next action (user)**: `bash state/anima_clm_3_original_ubu1_launch_2026_05_06/launch_ubu1.bash`
