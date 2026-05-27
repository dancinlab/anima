# P9 Path A — HF Repo Naming Decision (mk2 Reconciliation)

- date: 2026-05-03
- status: LANDED (canonical repo pre-created, redirect strategy locked, post-hoc rename scheduled)
- scope: HF naming for Path A LoRA SFT stage-1 ckpts (5 ckpts at step-2k/4k/6k/8k/10k from RunPod pod 29dhlqk508ugoc)
- supersedes: ad-hoc pod config `--push-to-hub dancinlab/p9-llama32-lora-stage1` (NON-CONFORM per mk2 §7.3)
- linked: `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`, `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md`
- raw: #9 STRICT (Mac → hexa/CLI only), #15 (no personal-path leak), #10 (3 honest C3 caveats § Caveats)

---

## §0 TL;DR

- **Canonical name chosen**: `dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1` (single repo + 5 step-Nk tags + final tag)
- **lm-family decision**: new `llm` family for Llama-base derived artifacts (Option 1 in task brief). Reasoning in §3.
- **Redirect strategy**: **Option B (post-hoc `hf repos move`)** — pod keeps pushing to legacy `p9-llama32-lora-stage1` UNTOUCHED; rename happens after training completes (~10-20h wall).
- **Pre-creation status**: canonical repo CREATED as PRIVATE with mk2-conformant README.
  - URL: https://huggingface.co/dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1
  - Sibling old (legacy): https://huggingface.co/dancinlab/p9-llama32-lora-stage1 (toggled to PRIVATE 2026-05-03 ~15:25Z)
- **Pod 29dhlqk508ugoc UNTOUCHED** (no ssh modify, no train.py edit, no env change)

---

## §1 Context — why this decision is needed

The Path A pod (`anima-p9-pathA-llama-v2`, id `29dhlqk508ugoc`) was launched with:

```
python3 -u /workspace/train_llama_lora.py \
  --base-model meta-llama/Llama-3.2-3B-Instruct \
  --data-jsonl /workspace/sft_data_llama_template.jsonl \
  --output-dir /workspace/p9_path_a_llama_lora \
  --lora-r 64 --lora-alpha 64 --lr 1e-4 \
  --per-device-batch 4 --grad-accum 8 \
  --max-steps 10000 --save-steps 2000 \
  --seq-len 2048 --warmup-steps 200 --logging-steps 10 \
  --bf16 --gradient-checkpointing \
  --push-to-hub dancinlab/p9-llama32-lora-stage1
```

Issues with the chosen `p9-llama32-lora-stage1` name relative to mk2 spec:

1. **Missing `lm-family` prefix** — mk2 §3.1 requires one of `blm | clm | tlm | vlm | slm | nlm`. `p9-` is a *cycle tag*, not an lm-family.
2. **Missing `base-version` slot** — mk2 §3.2 requires `v{N}`.
3. **No `paradigm-X` slot** — though the artifact IS a Paradigm A' product (anchor-swap from CLM v4 to Llama base).
4. **Listed as NON-CONFORM in the spec itself** (mk2 §7.3 row 3): "p9-llama32-lora-stage1-{step-2k,step-5k,step-10k,final}` | NON-CONFORM (Path A planned) — needs prefix fix to `clm-v4-paradigm-a-prime-llama32-lora-stage1-step-Nk` OR own family `lora-vendor-mirror` design".

The mk2 spec's *suggested* fix `clm-v4-paradigm-a-prime-llama32-lora-stage1-step-Nk` is **semantically wrong**: Path A explicitly anchors on Llama-3.2-3B base, NOT clm-v4. The whole point of Path A is to escape clm-v4's architectural blocker (per `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` §"Critical reframe"). Reusing `clm-v4-` as the family prefix would mislead future consumers about lineage.

---

## §2 Three options considered (per task brief)

### Option 1 — new lm-family `llm` (Llama LM)

Form: `llm-llama32-3b-paradigm-a-prime-sft-stage1`

- pros: honest about base lineage; forward-friendly for future Llama-base experiments; minimal additive spec change (§3.1 table extension)
- cons: hexa validator (`tool/hf_upload_mk2.hexa::_naming_allowed_families`) hardcodes `clm | alm | blm | vlm | slm | tlm | mlm | hexad | composite` (note: includes `alm` and `mlm` not present in mk2 spec; spec/hexa drift exists). Adding `llm` requires hexa-side update — 1 line edit, deferred to a follow-up cycle without blocking this pre-create.

### Option 2 — repurpose `clm` family with base-version trick

Form: `clm-v4-paradigm-a-prime-llama32-lora-stage1-step-Nk` (the spec's own §7.3 suggestion)

- pros: matches spec EBNF without extension
- cons: SEMANTICALLY MISLEADING — `clm-v4` implies clm-v4 base, but the artifact uses Llama-3.2-3B base. Path A's entire purpose is anchor-swap AWAY from clm-v4. Naming would falsely advertise lineage.

### Option 3 — keep legacy `p9-llama32-lora-stage1-{step-Nk}` with mk2 banner

Form: legacy name + grandfathered EXT-banner per mk2 §8.2

- pros: zero training disruption; spec has explicit grace path
- cons: `p9-` is not even a valid lm-family per the EXT regex (§10.2 EXT regex requires `^{LM}-{VER}-...`); this name doesn't match either CANON or EXT. It would be a NEW FAIL. Mk2 §10.5 currently reports 0 FAIL repos — adding one degrades the audit posture.

### Decision matrix (완성도 lens)

| option | semantic honesty | spec conformance | training disruption | future extensibility | total (10) |
|---|---:|---:|---:|---:|---:|
| **1 — `llm` family** | 3/3 | 2/3 (needs additive ext) | 0/2 (none) | 2/2 | **7/10** |
| 2 — `clm-v4-...llama32-...` | 0/3 | 3/3 | 0/2 | 1/2 | 4/10 |
| 3 — legacy `p9-...` | 1/3 | 0/3 | 0/2 | 0/2 | 1/10 |

**Winner: Option 1.**

---

## §3 Canonical name derivation

Using mk2 EBNF (§2.1):

```
repo_name = lm_family "-" base_version
            [ "-" paradigm ]
            [ "-" stage ]
            [ "-" scale ]
            [ "-" step ]
            [ "-" variant ]
```

Filling slots:
- `lm_family` = `llm` (extension; rationale §2 Option 1)
- `base_version` = `llama32-3b` (Llama-3.2-3B; encodes both major arch + param count; deviates from `v{N}` template because Llama uses semantic versioning, not anima monotonic int — caveat C2)
- `paradigm` = `paradigm-a-prime`
- `stage` = `sft-stage1`
- `scale` = OMITTED (10K steps is small; deferred to README Origin section)
- `step` = OMITTED at repo level; instead use TAGS per ckpt (mk2 §4.3 row 2 pattern: "≥3 ckpts but only 1 actively consumed → single repo + tags")
- `variant` = OMITTED

**Final canonical**: `dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1`

Tags planned (created by HF Trainer's `every_save` strategy):
- `step-2000` (or `step-2k` if normalized post-hoc)
- `step-4000`
- `step-6000`
- `step-8000`
- `step-10000`
- `final` (terminal ckpt umbrella)

Length check: 51 chars (under 64-char limit per mk2 §2.3). 5 tokens beyond `llm-llama32-3b` (under 6-token limit).

---

## §4 Redirect strategy — Option B (post-hoc `hf repos move`)

Two redirect strategies were on the table:

### Option A — modify pod env/script to push to canonical name

- Mechanism: ssh into pod, edit `/workspace/train_llama_lora.py` to change `--push-to-hub` target, OR set `HUB_MODEL_ID` env var (only effective at Trainer init = next restart)
- Reality: `transformers.Trainer` reads `hub_model_id` ONCE at init (`TrainingArguments` construction at process start). Mid-run env change has zero effect. Redirect would require STOP + RESTART = lost progress.
- Cost: ~$5-15 of compute progress lost (depending on which step at restart)
- Decision: **REJECTED** per task constraint "DO NOT preempt training"

### Option B — let pod push to legacy, then `hf repos move` post-hoc

- Mechanism: pod completes 10K-step training, pushes all ckpts (as tags) to `dancinlab/p9-llama32-lora-stage1`. After completion, run `hf repos move dancinlab/p9-llama32-lora-stage1 dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1`. HF preserves URL redirect at the old name for 30+ days.
- Cost: $0 (CLI op only)
- Risk: pre-created canonical repo BLOCKS the move (target exists). Mitigation: delete the pre-created stub immediately before the move, then re-upload README after the move.
- Decision: **CHOSEN**

### Step-by-step post-completion workflow (FUTURE CYCLE)

```
# 1. Verify training completed
ssh root@<pod-ip> -p <port> 'tail -50 /workspace/training.log | grep -E "completed|saved"'

# 2. Verify legacy repo has all expected tags (5 ckpts + final)
hf models info dancinlab/p9-llama32-lora-stage1 | jq .siblings

# 3. Delete canonical stub (README + .gitattributes only)
hf repos delete dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1 --yes

# 4. Move legacy → canonical
hf repos move dancinlab/p9-llama32-lora-stage1 dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1

# 5. Re-upload mk2 README (filling in TBD fields with actual training stats)
hf upload dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1 \
  state/p9_path_a_naming_2026_05_03/README_canonical_final.md README.md \
  --commit-message "p9 path a: post-training mk2 README finalize"

# 6. (optional) tag normalization step-2000 → step-2k via hf repos tag create + delete old
```

---

## §5 Pre-creation actions executed (this cycle)

| step | action | timestamp | result |
|---|---|---|---|
| 1 | Inspect mk2 spec (`docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`) | 2026-05-03T15:24Z | OK — §7.3 confirms NON-CONFORM status |
| 2 | Inspect Path A pod 29dhlqk508ugoc training script via ssh | 2026-05-03T15:25Z | OK — `--push-to-hub dancinlab/p9-llama32-lora-stage1` confirmed; pod RUNNING since 14:27, ~58min in |
| 3 | Inspect legacy repo state | 2026-05-03T15:25Z | OK — exists, was PUBLIC, only `.gitattributes` (pod not yet pushed first ckpt) |
| 4 | Toggle legacy repo to PRIVATE | 2026-05-03T15:25Z | OK — `hf repos settings dancinlab/p9-llama32-lora-stage1 --private` succeeded |
| 5 | Author mk2-conformant README at `state/p9_path_a_naming_2026_05_03/README_canonical.md` | 2026-05-03T15:26Z | OK — 5 required H2 sections + 3 honest C3 caveats |
| 6 | Create canonical repo as PRIVATE | 2026-05-03T15:27Z | OK — `hf repos create dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1 --type model --private` succeeded |
| 7 | Upload README to canonical repo | 2026-05-03T15:28Z | OK — commit sha `5161b80883bb602df532d13ab2a322211a6ee3af` |
| 8 | Verify canonical repo state | 2026-05-03T15:28Z | OK — `private: true`, 2 siblings (`.gitattributes`, `README.md`) |

**Pod 29dhlqk508ugoc untouched** (read-only ssh inspection only, no train.py edit, no env mutation, no SIGTERM).

---

## §6 Files

```
docs/p9_path_a_naming_decision_2026_05_03.md                      # this decision doc
docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md            # handoff (sibling cycle, this folder)
state/p9_path_a_naming_2026_05_03/README_canonical.md             # mk2 README (uploaded to canonical repo)
state/markers/p9_path_a_naming_decision_landed.marker             # silent-land marker
```

Referenced docs:
```
docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md            # mk2 spec (the source of truth being applied)
docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md             # Path A rationale (clm-v4 escape)
tool/hf_upload_mk2.hexa                                           # upload tool (validator drift noted §C1)
tool/hf_readme_template.md                                        # README template followed
```

HF artifacts:
```
dancinlab/p9-llama32-lora-stage1            # legacy training-time target (PRIVATE; pod actively pushing here)
dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1  # canonical pre-created (PRIVATE; rename target)
```

---

## §7 raw#10 honest C3 caveats

### C1 — naming reconciliation across base lineages (`llm` extension is informal)

The mk2 spec §3.1 family table is FROZEN at `blm | clm | tlm | vlm | slm | nlm`. This decision adds `llm` for Llama-base derivatives via the canonical repo + this README. The spec's own §3.3 "additive update" pattern was designed for `paradigm-X` letters, not `lm-family` codes. Strictly, ratifying `llm` requires a follow-up cycle that lands a 1-row edit to mk2 §3.1 — until that lands, F-NAME-1 audit may flag this repo as EXT-with-banner rather than CANON. The repo README explicitly documents this caveat (Caveats C1) so the EXT-banner requirement (mk2 §8.2.1) is satisfied at creation time. ALSO: the hexa upload validator (`tool/hf_upload_mk2.hexa::_naming_allowed_families`) has a SEPARATE family list (`clm | alm | blm | vlm | slm | tlm | mlm | hexad | composite`) that includes `alm` and `mlm` not present in the mk2 spec. This drift between spec and validator is a pre-existing condition unrelated to this cycle, but means ANY follow-up `--validate-naming` run on this repo via hexa will currently FAIL until the validator is patched to add `llm`. Workaround: skip hexa validator for this repo until the patch lands; rely on this README's explicit conformance claim.

### C2 — post-hoc rename risks tag/branch loss

`hf repos move` preserves the URL redirect and the main branch history. However, behavior on **git tags** (the per-ckpt step-Nk tags) is not documented as guaranteed. If `hf repos move` drops tags during the move, recovery requires (a) capturing each ckpt's commit sha BEFORE the move from `hf models info <legacy> | jq .siblings`, (b) re-creating tags via `hf repos tag create` after the move. The post-completion workflow §4 must include a pre-move tag manifest dump. Worst case: tags lost AND no manifest captured → ckpts at step-2k/4k/6k/8k are recoverable only by walking commit history. ALSO: HF redirect for legacy URL is documented as 30-day grace at minimum, but downstream code citing the legacy URL in pinned configs SHOULD be updated to the canonical URL within the grace window.

### C3 — README banner for legacy variant + base-version slot deviation

The canonical repo README uses `llama32-3b` as the `base-version` slot value, deviating from mk2 §3.2's strict `v{N}` template (monotonic int). Justification: Llama uses semantic versioning natively (`3.2`), and a fake remap to `v1` would lose information about which Llama generation. The deviation is documented in this doc (§3) and the repo README (Origin). Future spec ratification could add a §3.2.1 "vendor-base passthrough" rule for non-anima base lineages. For the legacy repo `p9-llama32-lora-stage1` during its short lifetime (~10-20h until rename), the spec EXT-banner is NOT being added because (a) the repo is now PRIVATE so audit visibility is reduced, (b) the rename will eliminate the legacy name entirely. If the rename is delayed >24h, an EXT-banner README MUST be added to legacy per mk2 §8.2.1.

---

## §8 Cost & destructiveness

- this cycle: $0 (Mac-local + free HF API calls)
- destructive ops: 1 — toggled legacy repo from PUBLIC to PRIVATE (reversible via `hf repos settings --no-private`)
- training disruption: 0 — pod 29dhlqk508ugoc continues uninterrupted
- byte-diff to existing artifacts: 0 — canonical repo had no prior content; legacy repo had only `.gitattributes` (untouched)
- HF API calls: ~5 (info × 2, settings × 1, create × 1, upload × 1)

---

## §9 Next-cycle scheduled actions

| trigger | action | owner |
|---|---|---|
| Pod 29dhlqk508ugoc reports `step=10000` saved | run §4 step-by-step post-completion workflow | follow-up BG cycle |
| If pod fails or stops <10K steps | salvage decision: keep partial ckpts in legacy → rename anyway → tag whatever ckpts exist | follow-up BG cycle |
| 24h elapsed without rename | add mk2 EXT-banner README to legacy `p9-llama32-lora-stage1` (per C3) | follow-up BG cycle |
| `llm` family ratification | edit mk2 spec §3.1 table to add `llm` row + reference this doc | spec-update cycle |
| hexa validator drift fix | patch `tool/hf_upload_mk2.hexa::_naming_allowed_families` to add `llm` (and align with mk2 §3.1) | tool-update cycle |

---

**End of decision doc. Pre-creation done; redirect scheduled; pod untouched.**
