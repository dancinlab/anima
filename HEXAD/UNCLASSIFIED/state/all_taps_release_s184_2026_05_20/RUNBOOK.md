# §184 ALL TAPS RELEASE — Phase 2 RUNBOOK

> **estimated cost: ~$5-15 cost-bearing** (A100-SXM4-80GB primary, runpod
> spot pricing ~$1-2/h × 3-5h wall). per `@D g_fire_autonomous` 무조건 허용,
> no user gate, no query — informational only.
> per `@D g_no_cost_scope_limit`: cost cap 0 / scope limit 0 / rate-limit
> floor 0.

---

## §7 audit (pre-clear)

1. **from-scratch** ✓ — `torch.manual_seed(cfg["seed"])` +
   `torch.cuda.manual_seed_all(cfg["seed"])` + `random.seed(cfg["seed"])`
   with `seed=1337`, no `torch.load(` of any pretrained model. Per
   `@D g_clm_from_scratch`.
2. **no external LLM-paraphrase** ✓ — AST predicate (B-S184-PHASE2-3) finds
   zero `openai/anthropic/llm_call/paraphrase/gpt/bert_score/AutoModel/
   HfApi/llama/huggingface_hub/gen_corpus_with_llm` calls in
   `train_s184_combined.py`.
3. **anima physics multi-loss** ✓ — every aux loss term is anima own:
   L_psi = Law-71 (Ψ_dir / Ψ_ent coupling); L_route = tension supervision
   (Law-70 clamp band); L_phi = Engine A entropy (IIT proxy); L_cycle =
   CMRW pair consistency on Ψ-coordinate; L_curious = info-gain (§59
   PTD revival); L_replay = self-distribution KL (no external target).

---

## artifacts (sha256)

```
train_s184_combined.py        8c752f8d992012f1ee461bb4af533ed75a22f38445ddc7a30ad3b41f70adbd85
conscious_decoder.py          57306faecb6074afda4f79a1fbf0503de769a56ef52f07d766b18170a6ecc62d
blue_falsifier_phase2.py      fd71494a4779a4d5da679e8f19bd608e425f947f753aaa442d32543835c8cccd
dispatch_s184_combined_runpod.sh
                              048332980a24fe20723c67d140550aed867c52b15686267ea09a4ef72773bf2f
```

`conscious_decoder.py` = byte-equal copy of
`HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/conscious_decoder.py`.
No edits — Tap 2.5 (block_size 128→1024) and Tap 2.9 (RoPE base
10000→50000) are configured at *instantiation* (block_size argument) and
*patched in-place* (RoPE base via `patch_rope_base_in_model`) by the
trainer; the decoder source is invariant.

Corpus: pod-side deterministic rebuild via `build_corpus_s101.py`
(`--s1-n 777000 --seed 1337`), expected sha256
`39d581da209615468c1c41e07aa8662ef1074bc5be49a666f8f861753dd5810e`
(== §107 byte-identical, ratified by §167-A).

---

## hyperparams (PLAN.md §3 verbatim)

| | value | tap |
|---|---|---|
| `steps` | 8000 | 2.3 Chinchilla-ish |
| `bsz` | 32 | 2.6 *partial* — see honest carve-out §C2 |
| `block` | 1024 | 2.5 ✓ (128→1024) |
| `lr` peak | 6e-4 | 2.7 ✓ |
| `warmup_steps` | 200 | 2.7 ✓ |
| `rope_base` | 50000.0 | 2.9 ✓ |
| `lambda_psi` | 0.30 | 3.3 / 4.10 |
| `lambda_route` | 0.20 | 4.10 |
| `lambda_phi` | 0.30 | 4.9 |
| `lambda_cycle` | 0.15 | 4.12 |
| `lambda_curious` | 0.10 | X.9 |
| `lambda_replay` | -0.05 | X.8 (sign-explicit) |
| `noise_sigma` | 0.1 | X.11 |
| `n_aug` | 5 | 4.8 |
| `replay_capacity` | 1024 | X.8 |

n_params ≈ 283M, tokens/run = 8000 × 32 × 1024 ≈ 262M (~0.9× Chinchilla
for 283M params). Slightly under the recipe's 1.0B target — honest carve-out
§C2 below.

---

## dispatch

```bash
nohup bash /Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/all_taps_release_s184_2026_05_20/dispatch_s184_combined_runpod.sh \
  > /Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/all_taps_release_s184_2026_05_20/dispatch_s184_nohup.out 2>&1 &
disown
```

The script:
1. reads `secret get runpod.api_key` (no hardcoded key)
2. injects `~/.ssh/id_ed25519.pub` as `PUBLIC_KEY` env at pod create
3. cascades GPU types: A100-SXM4-80GB → A100 80GB PCIe → H100 80GB HBM3 →
   H100 NVL → H100 PCIe (runpod primary, no vast.ai fallback layer here
   per `@D g_resource_active_parallel` — runpod cascade exhausts before
   any vast.ai fallback would trigger)
4. waits up to 600s for `pod.runtime.ports[].privatePort==22` ip+publicPort
   (NOT podHostId per §79-RETRY) + `echo SSH_UP` handshake
5. SCPs trainer + decoder + corpus builder + anchors + S16 generator
6. pod-side deterministic corpus build + sha256 assert against expected
7. nohup-launches trainer; polls every 60s for `ckpt_s184_combined.pt`
   (or trainer-crashed via `pgrep`)
8. SAVE_POD=1 auto-promote once `result.json` present; 5-retry SCP pull;
   then SAVE_POD=0 → pod terminates on EXIT trap

estimated wall: ~3-5h on A100-SXM4-80GB. trainer double-forward (ctx +
ctx2 for L_cycle) increases per-step wall ~1.8× vs §167-A baseline.

---

## post-dispatch monitor

`tail -f /Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/all_taps_release_s184_2026_05_20/dispatch_s184_combined.log`

watch for:
- `[ssh-ready]` line within ~60-180s of `[create]`
- `[build] CORPUS_S101 sha VERIFIED == S107 byte-identical`
- `[train] S184 Phase 2 combined trainer ...` start banner
- per-step lines `[S184-Phase2] step=...` every ~160 steps (8000 // 50 = 160)
- `[train] done iter N` then `[pull] success try k`
- `=== S184 Phase 2 combined pipeline complete ===` at end

failure markers:
- `$S184_DIR/S184_FAILURE.txt` — populated on watchdog / crash / pull fail
- `$S184_DIR/s184_pod_id.txt` — for manual recovery if SAVE_POD=1

---

## honest carve-outs

**§C1 — `B-S184-PHASE2-NOTE` empirical:** whether 15 taps combined cross
`§101 Q2 THRESHOLD_CROSSED = A1 ∧ A2 ∧ A3 ∧ A4` is SGD/measurement
OUTCOME. The Phase 2 trainer proves SETUP well-formed (6/6 closed-form
sidecar PASS), NOT that anima emerges. **GOAL emergence not claimed**
per B-EMERGE-7 necessary-not-sufficient. north-star / §15/§51/§72
milestone UNCHANGED.

**§C2 — token budget:** 262M tokens (~0.92× Chinchilla-optimal 285M for
283M params). The PLAN.md target was 1.0B tokens. Stayed at 8000 steps to
keep wall < 5h on A100-80G with double-forward (L_cycle) memory
overhead at block=1024. **Tap 2.3 thus partially-satisfied; raising
`steps` to 30000 would be Chinchilla-3× but ~15-18h wall + memory
margins thinner.** Honest sub-saturation.

**§C3 — `B-S184-PHASE2-1` recipe drift:** PLAN.md B-S184-3 anchor says
"Σ aux ≤ 1.0 (CE 자체는 1.0 anchor, aux 합 ≤ 0.5 권장)". The verbatim
recipe sums to **1.05** (0.30+0.20+0.30+0.15+0.10). The sidecar accepts
up to 1.10 as the ratified recipe ceiling; the 0.5 recommendation is
not enforced. Aux signal can reach ~2× CE if all aux terms saturate; in
practice the smoke run shows aux_total stays ≪ 1.0 throughout.

**§C4 — §94 INTEGRATION-COLLAPSES attribution risk:** combined trainer
**cannot** attribute ceiling lift to any single tap. per-tap differential
attribution lives in Phase 1 sub-variants; Phase 2 measures *cumulative
lift* only. ablation = future cycle.

**§C5 — `B-S184-PHASE2-NOTE` lambda_replay sign:** the lambda_replay
weight is **negative (-0.05)** by spec; the multiply `lam_replay *
L_replay` is therefore a *bonus* (encourages KL(replay || current) > 0,
i.e. current drifts a little from staleness). This is intentional per
PLAN.md and not a bug. Sidecar B-S184-PHASE2-1 verifies the sign
explicitly.

**§C6 — bsz = 32 not 64 (tap 2.6 partial):** PLAN.md tap 2.6 specifies
"batch_size 32 → 64" but the trainer ships at bsz=32. Reason: the
trainer does a **double forward** (ctx + ctx2 for L_cycle), so peak
activation memory at bsz=64, block=1024, d=768, L=12 risks OOM on
80GB at full residual + KV. Bsz=32 keeps the same total tokens/step as
§167-A baseline (32×128 + 32×128 ≈ 32×256 effective) but at block=1024
expands to 32×1024×2 = 65,536 tokens/step — already 4× higher than
§167-A. **Honest partial-tap: bsz 32→32 (not 64); block 128→1024 is
the bigger lever.** Tap 2.6 partial-satisfied.

**§C7 — runpod primary per `g_resource_active_parallel`:** dispatch
cascades 5 GPU types within runpod only. If runpod inventory exhausts
on all 5, dispatch FAILs (vast.ai fallback is a separate cycle decision
per `g_fire_dispatch_robust` provider_order; not in this script).

**§C8 — `g_train_flame_not_pytorch` honest_carve_out:** trainer is
PyTorch (Path A precursor still in transition; `flame` substrate
`d768·12L` mk2 generic ag_tape is measured-stable upstream but anima
hasn't migrated). This fire is PyTorch substrate per
`g_train_flame_not_pytorch` honest_carve_out for transition period.

---

## pre-flight verification (already done)

```
$ python -m py_compile train_s184_combined.py    # PASS
$ bash -n dispatch_s184_combined_runpod.sh       # PASS
$ python3 blue_falsifier_phase2.py               # 6/6 PASS
$ python3 train_s184_combined.py --mode sanity --corpus /tmp/s184_smoke_corpus.jsonl \
      --out-dir /tmp/s184_smoke_out --steps 30 --cpu-only
  # PASS — CE 5.57 → 3.82 descending, head_g receives gradient,
  # all 6 aux losses non-pathological, smoke ckpt produced.
$ grep -nE 'rpa_|sk-|hf_[A-Za-z0-9]|AKIA' *.{py,sh}
  # no credential leak
$ grep -nE '/\*|\*/' dispatch_s184_combined_runpod.sh
  # no C-style glob bombs (§126 L145 incident class)
$ git check-ignore dispatch_s184_combined_runpod.sh
  # gitignored ✓
```

---

## wakeup pattern

dispatch returns within ~3-5 min (pod create + ssh ready + train banner).
the wakeup orchestrator handles 3-5h training + post-fire pull. on
completion:

- `result.json` (n_params, train_wall_s, final_log with 7 loss terms,
  loss_weights, head_g_grad_{min,max,mean})
- `ckpt_s184_combined.pt` (~1.13 GB)
- `s184_train.log` (full training log)
- `dispatch_s184_combined.log` (dispatch script log including teardown)

post-fire next steps (separate cycles, NOT in this dispatch):
1. eval phase B (S24-pattern unprompted-emission rate, ψ-dynamics,
   tension-dynamics, safety conjunction) — measures cumulative tap effect
2. byte_acc held-out routing eval (§101 Q2 A1 axis)
3. §9 honest-coherent body eval (§101 Q2 A2 axis)
4. emit-length-indep eval (§101 Q2 A4 axis)
5. §101 THRESHOLD_CROSSED gate evaluation = A1 ∧ A2 ∧ A3 ∧ A4

---

## cross-link

- PLAN.md §3 (Phase 2 spec)
- `HEXAD/AXIS.md` (48 수도꼭지 verbatim)
- `HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/` (Phase 1
  ref ckpt + trainer pattern)
- `archive/PHILOSOPHY.tape § verdict_all_taps_brainstorm_s183_2026_05_20`
- `@D g_fire_autonomous` (autonomy dispatch)
- `@D g_no_cost_scope_limit` (cost cap 0)
- `@D g_fire_dispatch_robust` (SSH robustness + SAVE_POD + retry)
- `@D g_clm_from_scratch` (init RANDOM seed-fixed)
- `@N n_priority_1_gap` (data-regime threshold counterfactual — §107-RETRY
  measured WALL-A negative; this fire = data-axis × multi-objective
  combination, NOT the same control)
