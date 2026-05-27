# vP21M LoRA teacher — search log (2026-05-28)

verdict: **canonical `vP21M/lora_adapter/adapter_model.safetensors` ABSENT
from origin/main · sibling variant weights exist LOCALLY but untracked ·
HF Hub status NOT verified this session (no HF CLI call) · DEFERRED**

## What was searched

### Local filesystem (anima repo + worktrees)

```
$ find /Users/ghost/core/anima -name "adapter_model.safetensors" -path "*vP21M*"
```

Result — **5 sibling variants** carry the weight on disk:

| variant directory | size | git-tracked on origin/main? |
|---|---:|---|
| `vP21M_3B_CUR1/lora_adapter/adapter_model.safetensors` | 228 M | **NO** (dir untracked) |
| `vP21M_3B_V2/lora_adapter/adapter_model.safetensors`   | 228 M | **NO** (dir untracked) |
| `vP21M_V10/lora_adapter/adapter_model.safetensors`     | 141 M | **NO** (dir untracked) |
| `vP21M_RUFL/lora_adapter/adapter_model.safetensors`    | ?     | **NO** (dir untracked) |
| `vP21M_JAFL3B/lora_adapter/adapter_model.safetensors`  | ?     | **NO** (dir untracked) |

Result — the CANONICAL `vP21M/` dir (the one `train_p21h_v3.py` references)
has **NO** `adapter_model.safetensors`:

```
$ ls HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M/lora_adapter/
adapter_config.json
added_tokens.json
README.md
special_tokens_map.json
tokenizer_config.json
```

### Git tracking on origin/main

```
$ git ls-tree -r origin/main HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M/lora_adapter/
README.md
adapter_config.json
added_tokens.json
special_tokens_map.json
tokenizer_config.json
```

No `.safetensors` ever committed. The sibling `VP21M_*_2026_05_22.md`
documentation files are tracked, but their corresponding `vP21M_*/`
weight directories are NOT.

### HF Hub (NOT verified this session)

This session did not call `hf` CLI to inventory `dancinlab/anima-vp21m-*`
or `dancinlife/anima-vp21m-*` repos. The candidate path for axis B
re-enable via HF Hub:

```
hf list-files dancinlab/anima-vp21m-lora 2>&1                    # might exist
hf list-files dancinlab/anima-p21m-3b-jp 2>&1                    # JAFL3B sibling
hf list-files dancinlab/anima-p21m-v10 2>&1                      # V10 sibling
```

If any HF repo above lists `adapter_model.safetensors`, axis B re-enable
becomes one-`hf download` away. Untested.

## Where the weights came from (likely)

Per MEMORY.md context on the LORA session 2026-05-22~23
(`project_lora_session_2026_05_22.md`): "15 LoRA cycles $4.80, HF 15
artifacts" — the sibling directories on disk are the LANDED LoRA training
outputs from that session, and `vP21M/` likely was a SCAFFOLD never
written by training (or its weight was deleted post-train by .gitignore
hygiene + space pressure). The 15 HF artifacts ARE the canonical archive.

## Why the canonical `vP21M/` is empty

Three hypotheses, none verified:

1. `vP21M/` is a scaffold-only directory that was never the output of
   training (the training output dirs are `vP21M_<variant>/`). The
   `vP21M/` lora_adapter README.md is a generic placeholder.
2. The weight was once present but git-ignored and deleted (e.g.
   `state/p21h_v3_curricula_recover_2026_05_25/README.md` cleanup wave).
3. The dispatcher `train_p21h_v3.py:846-851` references `vP21M/` but the
   actual LoRA was written elsewhere (the variant dirs) — a wiring drift.

## Honest re-enable paths

Three options for the next session that wants axis B:

### Path A — Borrow a sibling variant

Copy `vP21M_V10/lora_adapter/adapter_model.safetensors` (141 M, smaller)
or `vP21M_3B_V2/...` (228 M) into `vP21M/lora_adapter/`. HONEST scope:
this changes the teacher identity (sibling ≠ canonical). The DECODER.md
M3-port note that calls for "real teacher" assumed the canonical weight.
Pre-register a falsifier that validates the chosen sibling.

Cost: 0 (local copy). Risk: silent teacher-identity drift unless
explicitly documented and pre-registered.

### Path B — Pull from HF Hub

Call `hf list-files dancinlab/anima-vp21m-*` to inventory the 2026-05-22
artifacts, then `hf download` whichever one DECODER.md M3-port intended.

Cost: bandwidth only. Risk: the HF repo set may be private
(`dancinlife/*`) per the 2026-05-15 cleanup and need auth.

### Path C — Re-train from scratch

Re-fire a vP21M LoRA training run on the canonical anima corpus. The
2026-05-22 session shows it cost ~$0.32/run × 15 runs = $4.80 → one fresh
canonical-tagged LoRA is ~$0.32 wall ~30min.

Cost: ~$0.32. Risk: drift from the 2026-05-22 cohort (different seed /
corpus snapshot).

## Decision for 2026-05-28

**No path taken this session.** Axis B remains deferred. The fix only
labels axis B as deferred and re-routes `dispatch_main` defaults to
`["A","C","D"]`.

When a future session adopts one of Path A / B / C:
1. Update this log with the choice + verification (sha256 of the
   safetensors + paired adapter_config.json hash).
2. Update `AXIS_B_DEFERRED.md` to reflect re-enable.
3. Flip `dispatch_main` default axes back to 4-axis OR pass
   `axes=["A","B","C","D"]` from caller.
4. Update DECODER.md `## 마일스톤` line 47 `[ ] M3d 실 teacher` → `[x]`.

## Cross-link

- `AXIS_B_DEFERRED.md` (sibling doc, same dir)
- `BLOCKERS_FIX_VERIFICATION.md` (Blocker 4 entry)
- DECODER.md `## 마일스톤` line 47 `M3d 실 teacher` carry
- `train_p21h_v3.py:846-851` source TODO
- MEMORY.md `project_lora_session_2026_05_22.md` (sibling cohort context)
