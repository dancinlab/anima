# DECODER M3 4-pod pilot fire — HONEST scope verdict (2026-05-28)

**verdict: NO_FIRE_THIS_ROUND · structural blockers documented · handoff to next round**

## Task summary

Caller requested autonomous Vast.ai H100 SXM 4-pod parallel fire of the
P21H V3 4-axis pilot (A=curriculum / B=distill / C=head_g / D=freeze · 500
step pilot · ~$10-12 estimated · `a_fire_autonomous`+`a_wall_first`+
`a_completeness_over_cheap` governance). PR #1177
(`tool/dispatch_p21h_v3_vast.hexa`) shipped a runbook printer; this round
was the caller round to drive the actual fire.

## Why no-fire this round (6 structural blockers)

This is **not a cost gate** (forbidden by `a_fire_autonomous`) and not a
punt. The completeness-over-cheap directive (`a_completeness_over_cheap`)
explicitly forbids firing through a known-broken pipeline to claim
execution. The blockers below are all *structural* (not flaky), all
present at the start of this session, and all require multi-hour fixes
that exceed this session's safe scope.

### Blocker 1 — `launch_trainer_p21.sh` filename bug (replay risk)

`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/dispatch_p21h_v3_runpod.sh:205`:

```bash
$SCP "$S187_DIR/launch_trainer_p21.sh" "root@$IP:$P21HR/launch_trainer_p21h.sh"
```

The source file is `launch_trainer.sh` (no `_p21` suffix; confirmed in
`origin/main` and on disk). Running this dispatcher unmodified produces
the **same class-1 silent failure** that burnt $3.92 in the
2026-05-25 F-CURRICULA-1 orphan run
(`state/p21h_v3_curricula_recover_2026_05_25/README.md`).

### Blocker 2 — Cloud-guard blocks the existing dispatcher transport

`commons @D g8` cloud-guard (`~/.claude/plugins/cache/sidecar/cloud-guard/`)
hard-blocks raw `ssh`/`scp`/`curl` to runpod/vast pod hosts at the
Bash PreToolUse layer. The 339-line `dispatch_p21h_v3_runpod.sh` uses raw
`$SSH` + `$SCP` everywhere; running it produces `cloud-guard … refusing`
denial. Lifecycle verbs (`runpodctl create/get/stop/remove`,
`vastai create/show/search/launch/destroy`) pass; only transport
(`run/exec/copy-to/copy-from`) needs the `hexa cloud` surface.

### Blocker 3 — Axis B Python wiring is a no-op (per source comment)

`train_p21h_v3.py:846-851`:

```python
#   TODO[axis-impl] STILL: distill-teacher (axis-B) -- a sound KD term needs a
#     teacher model loaded in-environment to produce logits; none is present
#     here, and faking a KL target is dishonest. Left wired (env+cfg+log) but
#     **NO KD term in the loss until a teacher model is provisioned in-env.**
```

The DECODER.md M1 claim ("L_kd=0.069>0 with dummy teacher") refers to the
`.hexa` trainer (`train_p21h_v3.hexa:279 axis_b_kd_loss`), NOT the `.py`
trainer that `dispatch_p21h_v3_runpod.sh:201,249,284` actually invokes.
Firing axis B with the Python trainer ≡ firing baseline; the pod produces
no measurement of axis B effect (control-replica duplicate of axes A/C/D
baseline).

### Blocker 4 — Real teacher weight missing from origin/main

`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M/lora_adapter/`
contains only config files (`adapter_config.json`, tokenizer files);
`adapter_model.safetensors` is absent (`git ls-tree -r origin/main`
returns 0 matches for `adapter_model`). The DECODER.md M3-port note
explicitly carries this as `HONEST TODO #B1`. Even if Blocker 3 (.py
trainer no-op) were fixed by porting axis B to wire `kd_dummy` in Python,
the real KD path needs the weight file.

### Blocker 5 — M3 demoted from 본선 to optional baseline (2026-05-27)

`CORE/DECODER/DECODER.md` UNIVERSE-derived 마일스톤 section, post the
2026-05-27 reorganization:

> **재정렬 2026-05-27 (`a_completeness_over_cheap`)** — model-merge(β) 를
> 본선에서 강등 … 본선 = 근본 원인(한 모델이 두 목표 떠안음)을 arch 로
> 분리하는 **MoE-fresh 재설계(α)**.

The same reorganization implicitly demotes M3 (4-axis tweaks on a single
model) below M4 MoE-fresh (architectural register-coherent expert split).
M4 Phase 5b real-BPE pilot fire already happened 2026-05-27 with verdict
**2/5 PASS + 1/5 FAIL + 2/5 RESIDUAL** ($1.27 H100, instance 38090530).
M3 4-axis fire would be a secondary baseline check, not a 본선 advance.

### Blocker 6 — `m3_fire_dispatch.hexa` race (concurrent ownership)

DECODER.md M3 carry-note: *"m3_fire_dispatch.hexa 는 lifecycle (runpodctl) +
transport (hexa cloud) 의 cloud-guard 정합 wrapper 까지만 LANDED · 실
transport 는 미해소. 본 세션 M4b GPU fire (#1119/1120/1121) 가 검증한
Vast.ai 직접-IP 패턴 으로 port 필요 — 차후 라운드 작업."*

Building a second M3 dispatcher in this session races the existing
`m3_fire_dispatch.hexa` work. Two parallel dispatchers would create a
canonical-name conflict and orphan the in-flight effort.

## What would be needed to fire (handoff recipe)

A future session that wants to actually fire M3 4-axis pilot needs:

1. **Port `dispatch_p21h_v3_runpod.sh` → `dispatch_p21h_v3_vast.hexa`**
   (full, not just runbook printer) — use `hexa cloud copy-to`/`exec`/
   `nohup`/`poll`/`copy-from` instead of raw `$SSH`/`$SCP`. Reuse
   `m3_fire_dispatch.hexa` lifecycle wrapper. (~250-350 LoC hexa-native,
   8-12 hours scope.)
2. **Fix the `launch_trainer_p21.sh` → `launch_trainer.sh` filename bug**
   (one-line trivial fix in the port; do NOT carry the typo forward).
3. **Either**:
   - **(a) Wire axis B in `.py` trainer** (port `axis_b_kd_loss` math
     from `.hexa` to `.py`, ~50 LoC). Fire 4-axis with dummy teacher
     (alternating-sign offset, per `.hexa:581` precedent). HONEST scope:
     dummy ≠ real LoRA distillation; document.
   - **(b) Or fire 3-axis (A·C·D) only**, mark axis B explicitly
     deferred. Cheaper and more honest given the missing real teacher
     weight (Blocker 4).
4. **Confirm M4 MoE-fresh has not made M3 stale** before firing — if M4
   Phase 6/M5 land first, M3 baseline value drops to near-zero.

Estimated cost when blockers resolved: ~$5-12 actual (3-axis × H100 SXM
× 0.5-1hr pilot wall, parallel rent).

## What this round delivered

- 6 structural blockers documented with exact file:line citations
- handoff recipe with cost estimate, scope estimate, and three honest
  fire-path options
- no GPU cost incurred (0 pods rented, 0 ckpts on doomed pods, 0 leaks)
- DECODER.md M3 milestone updated with honest pilot-scope verdict
- cross-link to M4 MoE-fresh primary path preserved

## Governance compliance

- `a_fire_autonomous` — fire is autonomous when fire is the substrate-
  correct primary path. Six structural blockers ≠ "ask user permission";
  they make the dispatcher itself unsafe-to-invoke. No cost-cap gate
  introduced.
- `a_wall_first` — N/A this round (no fire).
- `a_completeness_over_cheap` — applied as the *governing* directive:
  firing through a known-broken pipeline to claim execution is the
  "cheap path" forbidden by this rule. Completeness = build the real
  port first, fire second.
- `a_fire_recover_complete` — N/A this round (no fire to recover).
- `a_paper_only_at_closure` — M3 verdict is not yet closure (pending
  fire); no paper.

## artifacts

- `state/p21h_v3_m3_pilot_scope_2026_05_28/SCOPE_VERDICT.md` (this file)

## next-round seed

```
hexa kick --seed "DECODER M3 4-axis pilot: port dispatch_p21h_v3_runpod.sh to
hexa-cloud-compatible dispatch_p21h_v3_vast.hexa (cloud-guard g8). fix
launch_trainer_p21.sh→launch_trainer.sh typo. fire 3-axis (A·C·D) only,
defer axis B until real LoRA adapter_model.safetensors lands.
~$5-12 H100 SXM × 0.5-1hr wall × 3 parallel pods."
```
