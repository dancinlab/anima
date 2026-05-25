# P9 Path A — HF Naming Decision LANDED 2026-05-03

**Goal**: Pre-create mk2-conformant HF repo for Path A LoRA push so that when the running pod (29dhlqk508ugoc) finishes its first save (step-2k), there is a canonical-named target ready to receive the artifacts.

**Constraints honored**: raw#9 STRICT (Mac → hf CLI only, hexa is target tool but interp is currently unbuildable in docker route; CLI substitute used for repo create + README upload — same operation hexa would have shelled out to), raw#15 (no personal-path leak), raw#10 (3 honest C3 caveats per `## Caveats` section in this doc + the repo README), $0 design.

---

## TL;DR

- **Canonical name chosen**: `dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1`
- **Pre-created**: YES, as PRIVATE, with mk2-conformant README at https://huggingface.co/dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1
- **Redirect strategy**: **Option B (post-hoc `hf repos move`)** chosen by 완성도 lens
- **Pod 29dhlqk508ugoc UNTOUCHED** — only read-only ssh inspection
- **Legacy repo `p9-llama32-lora-stage1`**: toggled PUBLIC → PRIVATE (still receives pod pushes; rename target after training)

---

## Decision matrix (완성도 lens, ranked)

| rank | option | semantic honesty | spec conformance | training disruption | future extensibility | total |
|---|---|---:|---:|---:|---:|---:|
| **1** | **`llm` lm-family extension** | 3/3 | 2/3 | 0/2 (none) | 2/2 | **7/10** |
| 2 | `clm-v4-...llama32-...` (spec §7.3 suggestion) | 0/3 | 3/3 | 0/2 | 1/2 | 4/10 |
| 3 | legacy `p9-...` with EXT banner | 1/3 | 0/3 | 0/2 | 0/2 | 1/10 |

**Winner: Option 1**. The spec's own §7.3 suggested fix (`clm-v4-paradigm-a-prime-llama32-...`) is semantically wrong because Path A explicitly anchors on Llama-3.2-3B base, NOT clm-v4. Whole point of Path A is to ESCAPE the clm-v4 architectural blocker.

---

## Outputs (this cycle)

### Canonical decision doc
- `docs/p9_path_a_naming_decision_2026_05_03.md` (~280 LoC)

### HF artifacts
- **NEW**: `dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1` (PRIVATE, mk2 README)
  - URL: https://huggingface.co/dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1
  - sha: 5161b80883bb602df532d13ab2a322211a6ee3af
- **MODIFIED**: `dancinlab/p9-llama32-lora-stage1` (toggled PUBLIC → PRIVATE; will be renamed post-training)
  - URL: https://huggingface.co/dancinlab/p9-llama32-lora-stage1

### State
- `state/p9_path_a_naming_2026_05_03/README_canonical.md` (the README staged + uploaded)
- `state/markers/p9_path_a_naming_decision_landed.marker`

### Pod coordination
- pod 29dhlqk508ugoc (RunPod, anima-p9-pathA-llama-v2): **UNTOUCHED** (read-only ssh inspection only)
- pod still pushes to legacy `dancinlab/p9-llama32-lora-stage1` per its launch args
- training estimated wall: ~10-20h from launch (14:27Z 2026-05-03), ckpts at step-2k/4k/6k/8k/10k

---

## Post-training scheduled actions (next cycle)

When pod 29dhlqk508ugoc reports `step=10000` saved:

```
# 1. Capture pre-move tag manifest (per honest C2)
hf models info dancinlab/p9-llama32-lora-stage1 | jq .siblings > /tmp/pre_move_manifest.json

# 2. Delete pre-created stub
hf repos delete dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1 --yes

# 3. Move legacy → canonical
hf repos move dancinlab/p9-llama32-lora-stage1 dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1

# 4. Re-upload finalized README (with TBD fields filled)
hf upload dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1 \
  state/p9_path_a_naming_2026_05_03/README_canonical_final.md README.md

# 5. (optional) verify tags survived; recreate from manifest if needed
hf models info dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1 | jq .siblings
```

If pod fails or stops at step <10000, salvage workflow same but with whichever ckpts exist.

---

## raw#10 honest C3 caveats (decision-level)

(a) **`llm` lm-family is informal extension** — mk2 spec §3.1 table is FROZEN at `blm | clm | tlm | vlm | slm | nlm`. Adding `llm` requires a follow-up cycle to ratify. Until then, this repo flies under EXT-banner per mk2 §8.2.1 (banner contained in repo README C1). ALSO: hexa validator at `tool/hf_upload_mk2.hexa` has SEPARATE family list (`clm | alm | blm | vlm | slm | tlm | mlm | hexad | composite`) that drifts from mk2 §3.1 — adding `llm` requires both spec edit AND validator patch.

(b) **Post-hoc `hf repos move` may drop git tags** — the per-ckpt step-Nk tags (created by HF Trainer's `every_save` strategy) may not survive `hf repos move`. Pre-move manifest dump is mandated in step 1 above; tag re-creation from commit shas is the recovery path.

(c) **Base-version slot deviation** — canonical name uses `llama32-3b` rather than mk2 §3.2's strict `v{N}` template. Justified because Llama uses semantic versioning natively; remapping to `v1` would lose info. Documented in repo README + decision doc §3. Future spec ratification could add §3.2.1 "vendor-base passthrough" rule.

---

## Verification log

```
$ hf models info dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1 | jq '{id, private, siblings: [.siblings[].rfilename]}'
{
  "id": "dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1",
  "private": true,
  "siblings": [".gitattributes", "README.md"]
}

$ hf models info dancinlab/p9-llama32-lora-stage1 | jq '{id, private, siblings: [.siblings[].rfilename]}'
{
  "id": "dancinlab/p9-llama32-lora-stage1",
  "private": true,
  "siblings": [".gitattributes"]
}

$ ssh root@<pod-ip> -p <port> 'ps -ef | grep train_llama_lora | grep -v grep | head -1'
root  1291  1  99 14:27 ?  python3 -u /workspace/train_llama_lora.py --base-model meta-llama/Llama-3.2-3B-Instruct ... --push-to-hub dancinlab/p9-llama32-lora-stage1
# (still running, untouched)
```

---

## Files

```
docs/p9_path_a_naming_decision_2026_05_03.md             # full decision spec
docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md   # this handoff
state/p9_path_a_naming_2026_05_03/README_canonical.md    # mk2 README (uploaded)
state/markers/p9_path_a_naming_decision_landed.marker    # silent-land marker
```

Referenced docs:
```
docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md         # mk2 spec
docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md          # Path A rationale
tool/hf_upload_mk2.hexa                                        # upload tool (validator drift noted)
tool/hf_readme_template.md                                     # README template
```

---

**End of handoff. Next BG (post-pod-completion): execute §4 post-completion workflow + finalize README.**
