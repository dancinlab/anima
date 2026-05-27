<!--
anima HF upload mk2 — README template (tool/hf_readme_template.md)

The hexa wrapper (tool/hf_upload_mk2.hexa) enforces presence of the FIVE
H2 headings below by regex. Reorder/rename them at your own risk; missing
or renamed headings abort upload with a prescriptive error.

Required H2 headings (regex, case-sensitive):
  ^## Origin$
  ^## Falsifiers$
  ^## Substrate$
  ^## Caveats$
  ^## Composability$

Fill in the {{PLACEHOLDER}} sections per upload. The template itself is
NOT uploaded — copy and edit per repo.
-->

# {{REPO_DISPLAY_NAME}}

One-line summary: {{ONE_LINE_SUMMARY}}

- Family: {{FAMILY}} (e.g. clm | alm | blm | vlm | slm | tlm)
- Stage: {{STAGE}} (e.g. sft-stage1 | sft-stage2 | dpo | merged)
- Step: {{STEP_OR_VERSION}} (e.g. step-25k | v1.0 | final)
- Substrate: {{SUBSTRATE_SHORT}} (e.g. mistral-7b-v0.3 | llama-3-8b)

## Origin

What this checkpoint is and how it was produced.

- Base model: {{BASE_MODEL_HF_ID}} (license: {{BASE_LICENSE}})
- Training data: {{DATA_DESCRIPTION}} (~{{N_EXAMPLES}} examples, {{N_TOKENS}} tokens)
- Training recipe: {{RECIPE_REF}} (e.g. docs/p9_sft_spec_2026_05_02.md §3)
- Compute: {{COMPUTE_DESCRIPTION}} (e.g. 8xH100 SXM, ~{{HOURS}} hrs)
- Trainer: {{TRAINER_REF}} (e.g. tool/anima_train_r14_lora.hexa)
- Final loss / metric: {{FINAL_METRIC}}
- Commit: {{GIT_SHA}} of repo {{GIT_REPO}}

## Falsifiers

Concrete tests this checkpoint either passes or is meant to fail
deterministically. Each falsifier MUST be reproducible.

- F-{{ID}}-1: {{FALSIFIER_1_DESC}}
  - Spec: {{SPEC_REF}}
  - Pass criterion: {{PASS_CRITERION}}
  - Last result: {{LAST_RESULT}} (run {{RUN_REF}})
- F-{{ID}}-2: {{FALSIFIER_2_DESC}}
  - Spec: {{SPEC_REF}}
  - Pass criterion: {{PASS_CRITERION}}
  - Last result: {{LAST_RESULT}}
- F-{{ID}}-3: {{FALSIFIER_3_DESC}}
  - Spec: {{SPEC_REF}}
  - Pass criterion: {{PASS_CRITERION}}
  - Last result: {{LAST_RESULT}}

## Substrate

Hardware / software / data dependencies required to run this checkpoint.

- Inference VRAM (bf16): ~{{VRAM_BF16_GB}} GB
- Inference VRAM (4-bit): ~{{VRAM_4BIT_GB}} GB
- Min Python: {{MIN_PYTHON}} (default: 3.10)
- Required: {{REQUIRED_PACKAGES}} (e.g. transformers>=4.45, peft>=0.12, torch>=2.4)
- Optional: {{OPTIONAL_PACKAGES}}
- Input format: {{INPUT_FORMAT}} (e.g. ChatML | Alpaca | raw text)
- Context window: {{CONTEXT_TOKENS}} tokens
- Tokenizer: {{TOKENIZER_REF}} (inherited from base unless noted)

## Caveats

Three or more honest limitations (raw#10). Do NOT skip this section.

- {{CAVEAT_1}} (e.g. "trained on en-only data, ko/ja generalisation untested")
- {{CAVEAT_2}} (e.g. "stage1-only — does not include DPO alignment")
- {{CAVEAT_3}} (e.g. "evaluation set overlaps with training distribution within 5%")
- {{CAVEAT_N_OPTIONAL}}

## Composability

How this checkpoint plugs into the broader anima ecosystem.

- Combines with: {{SISTER_CHECKPOINT_LIST}} (e.g. dancinlab/clm-v4-dpo-stage2)
- Loaded by: {{LOADER_REF}} (e.g. anima-core/loader.hexa)
- Slots into: {{HEXAD_SLOT}} (e.g. clm | alm | blm | vlm | slm | tlm)
- Compose recipe: {{COMPOSE_REF}} (e.g. docs/anima_compose_v4_2026_05_03.md)
- Known good downstream tasks: {{DOWNSTREAM_TASKS}}
- Known incompatible: {{INCOMPATIBLE_LIST}} (or "none observed")

---

**Citation**

```bibtex
@misc{anima_{{REPO_SHORT}}_{{YEAR}},
  author = {{{AUTHOR}}},
  title  = {{{REPO_DISPLAY_NAME}}},
  year   = {{{YEAR}}},
  url    = {https://huggingface.co/{{REPO}}}
}
```

**License**: {{LICENSE}} (must be compatible with base model license: {{BASE_LICENSE}})
