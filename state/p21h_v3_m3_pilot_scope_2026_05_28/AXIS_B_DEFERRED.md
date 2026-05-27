# Axis B (distill) — HONEST DEFER (2026-05-28)

verdict: **DEFERRED** · `tool/dispatch_p21h_v3_vast.hexa` `dispatch_main` default `axes=["A","C","D"]`

## Why deferred

Axis B (distill / KD teacher) was a planned 4-axis P21H V3 pilot dimension
but **two structural blockers**, both at the start of the 2026-05-28
caller session and both unfixable inside one session's safe scope, force
an HONEST defer:

### Reason 1 — Python axis B wiring is a documented no-op

`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_p21h_v3.py:846-851`:

```python
#   TODO[axis-impl] STILL: distill-teacher (axis-B) -- a sound KD term needs a
#     teacher model loaded in-environment to produce logits; none is present
#     here, and faking a KL target is dishonest. Left wired (env+cfg+log) but
#     **NO KD term in the loss until a teacher model is provisioned in-env.**
```

The DECODER.md M1 claim "L_kd=0.069>0 with dummy teacher" refers to the
`.hexa` trainer (`train_p21h_v3.hexa:279 axis_b_kd_loss`), NOT the `.py`
trainer that `dispatch_p21h_v3_runpod.sh:201,249,284` invokes. Firing axis
B with the Python trainer ≡ firing baseline (control-replica duplicate of
axes A/C/D baseline).

### Reason 2 — Real teacher weight (`adapter_model.safetensors`) absent from origin/main

`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M/lora_adapter/`
contains config + tokenizer only:

```
adapter_config.json
added_tokens.json
README.md
special_tokens_map.json
tokenizer_config.json
```

`adapter_model.safetensors` is **NOT** on origin/main
(`git ls-tree -r origin/main HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/
| grep adapter_model` returns 0 matches — only `adapter_config.json`
is tracked).

DECODER.md carries this as **HONEST TODO #B1**.

## Why not "blend the .hexa axis B math into the .py trainer"

Tempting cheap path — but `a_completeness_over_cheap` blocks it:

- A correctly-wired KD term in Python WITHOUT a real teacher weight is
  still a no-op (the dummy-teacher alternating-sign offset trick at
  `train_p21h_v3.hexa:581` produces a KD signal that has no relation to a
  real teacher's logits — measuring axis B effect with it is meaningless).
- A correctly-wired KD term in Python WITH a real teacher weight requires
  both (a) the ~50-line port AND (b) the missing safetensors. Doing (a)
  alone is wasted effort.

So axis B sits behind both (a) the Python port AND (b) the missing weight.

## What axis B re-enable would need

To remove `axis B = deferred`:

1. **Provision** a real vP21M LoRA teacher checkpoint.
   See `VP21M_SEARCH_LOG.md` (this directory) for the search trail — local
   sibling variants (`vP21M_V10/`, `vP21M_3B_V2/`, `vP21M_3B_CUR1/`,
   `vP21M_RUFL/`, `vP21M_JAFL3B/`) have `adapter_model.safetensors` on
   disk but are NOT git-tracked (not on origin/main).
2. **Port `axis_b_kd_loss` math** from `.hexa:279` to `.py` (~50 LoC).
3. **Pre-register a falsifier** that distinguishes axis B effect from
   axis A/C/D baseline (e.g. KL divergence to teacher monotone-decreasing
   AND teacher-logit-frozen ablation shows distinct collapse signature).
4. **Then** flip `axes=["A","C","D"]` → `["A","B","C","D"]` in
   `tool/dispatch_p21h_v3_vast.hexa::dispatch_main` (or pass `axes`
   explicitly at caller site).

## Until then

`tool/dispatch_p21h_v3_vast.hexa`:
- `dispatch_main` defaults `axes=["A","C","D"]` — axis B not auto-fanned.
- Opt-in: caller may pass `axes=["A","B","C","D"]` explicitly. The
  dispatcher will print `_axis_b_warning()` and fire anyway (caller-owned
  consequence — typically a control-replica baseline).
- Cost saved by deferral: ~$13-21 per pod × 1 pod = ~$13-21 saved per
  full-fire pilot batch (no signal extracted ↔ no spend on no-signal).

## Cross-link

- DECODER.md `## 마일스톤` line 47 `[ ] M3d 실 teacher`
- DECODER.md M3 carry-note line 50 (5-blocker SCOPE_VERDICT cross-link)
- `train_p21h_v3.py:846-851` source TODO
- `train_p21h_v3.hexa:279` axis_b_kd_loss (the working version, not used
  by Python trainer)
- `state/p21h_v3_m3_pilot_scope_2026_05_28/SCOPE_VERDICT.md` Blocker 3 + 4
- `state/p21h_v3_m3_pilot_scope_2026_05_28/VP21M_SEARCH_LOG.md`
- `state/p21h_v3_m3_pilot_scope_2026_05_28/BLOCKERS_FIX_VERIFICATION.md`

## Governance

- `a_completeness_over_cheap` — DEFER (cheap "wire dummy KD" path
  forbidden as a substrate-FAIL primary).
- `a_fire_autonomous` — N/A this round (no fire being held; fix-only
  session).
- `a_paper_only_at_closure` — N/A (M3 not yet at closure).
