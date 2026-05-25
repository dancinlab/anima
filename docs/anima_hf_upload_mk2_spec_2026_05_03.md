# Anima HF Upload Pipeline mk2 — Spec (2026-05-03)

## TL;DR

Promotes session-observed manual `hf` CLI uploads to a repeatable,
audit-friendly hexa-side pipeline. Single canonical entry point
`tool/hf_upload_mk2.hexa` validates README + naming, pre-computes sha256,
delegates network work to a single python bridge `_python_bridge/hf_upload_runner.py`,
writes per-upload + ledger audit logs, and integrates with git pre-push.

- **Surface**: 1 hexa wrapper + 1 py bridge + 1 README template + 1 hexa hook
- **raw#9 cost**: 1 .py file (justified — huggingface_hub is python-only SDK)
- **$ cost (this cycle)**: $0 (no actual upload triggered)
- **Smoke test**: dry-run end-to-end PASS, selftest PASS

## 1. Architecture

```
operator
  │
  ├── (manual) hexa run tool/hf_upload_mk2.hexa --upload --repo X --ckpt Y --readme Z --tag T
  │       │
  │       ├─→ readme_validate(Z)           ── 5 H2 + Caveats >= 3
  │       ├─→ naming_validate(X)           ── mk2 convention regex
  │       ├─→ json_stringify(req)
  │       └─→ proc_run_with_stdin("python3 _python_bridge/hf_upload_runner.py", req)
  │              │
  │              ├── selftest | dry_run | upload mode
  │              ├── walk_files + sha256
  │              ├── huggingface_hub.HfApi.create_repo / upload_folder / create_tag
  │              ├── exponential backoff (3 attempts: 2s/4s/8s)
  │              ├── per-upload audit  → state/hf_upload_audit/<ts>_<repo>.jsonl
  │              └── single-line JSON response on stdout
  │
  └── (CI) git pre-push
          │
          └─→ .git/hooks/pre-push → hexa run tool/hf_upload_mk2_pre_push_hook.hexa
                  │
                  └── if commit msg has [hf-upload: <repo>]
                          → call --validate-naming, abort push on FAIL
```

## 2. File map (all paths relative to anima/ repo root)

| Path | Kind | LoC | Purpose |
|---|---|---:|---|
| `tool/hf_upload_mk2.hexa` | hexa | 567 | Canonical entry: arg parse, README/naming validation, bridge dispatch, ledger append |
| `_python_bridge/hf_upload_runner.py` | py (raw#9 concession) | 500 | huggingface_hub SDK wrapper: selftest / dry_run / upload modes + retry + audit |
| `tool/hf_readme_template.md` | md | 104 | Template stub — 5 required H2 + bibtex + license placeholders |
| `tool/hf_upload_mk2_pre_push_hook.hexa` | hexa | 123 | Git pre-push fragment, scans HEAD msg for `[hf-upload: <repo>]` marker |
| `state/hf_upload_audit/.gitkeep` | placeholder | 0 | Per-upload audit log dir (gitkeep ensures dir survives clean) |
| `state/hf_upload_ledger_2026_05.jsonl` | runtime | 0 | Aggregate ledger appended by hexa wrapper (created on first run) |
| `docs/anima_hf_upload_mk2_spec_2026_05_03.md` | md | this | Spec doc |
| `docs/anima_hf_upload_mk2_landed_2026_05_03.ai.md` | md | (handoff) | Landing handoff |
| `state/markers/anima_hf_upload_mk2_landed.marker` | json | (marker) | Landing marker |

**Total surface**: 4 source files + 2 docs + 1 marker + 1 dir placeholder = 8 artifacts.

**raw#9 compliance**: exactly **1** `.py` file, located in the approved
`_python_bridge/` directory, justified by huggingface_hub being a
python-only SDK with no public C ABI. All other deliverables are hexa
or markdown.

## 3. CLI surface (`tool/hf_upload_mk2.hexa`)

```
hexa run tool/hf_upload_mk2.hexa --selftest
hexa run tool/hf_upload_mk2.hexa --dry-run --repo <org/name> --ckpt <path> --readme <path> [--tag <step>]
hexa run tool/hf_upload_mk2.hexa --upload  --repo <org/name> --ckpt <path> --readme <path> [--tag <step>] [--private]
hexa run tool/hf_upload_mk2.hexa --validate-readme <path>
hexa run tool/hf_upload_mk2.hexa --validate-naming <org/name>
hexa run tool/hf_upload_mk2.hexa --help
```

### 3.1 Sentinels

- `__ANIMA_HF_UPLOAD_MK2__ PASS` — operation succeeded
- `__ANIMA_HF_UPLOAD_MK2__ FAIL` — validation or bridge failure (non-fatal exit)
- `__HF_UPLOAD_MK2_PRE_PUSH__ {PASS|FAIL|SKIP}` — pre-push hook outcome

### 3.2 Env

| Var | Purpose |
|---|---|
| `HF_TOKEN` / `HUGGING_FACE_HUB_TOKEN` | upload auth (fallback: `~/.huggingface/token`, `~/.cache/huggingface/token`, `/workspace/.hf_token`) |
| `ANIMA_HF_PY` | python3 binary override (default: `python3` from `$PATH`) |
| `ANIMA_SKIP_HF_PRECHECK` | set to `1` to bypass pre-push hook |

## 4. README enforcement

### 4.1 Required H2 headings (5)

The hexa wrapper's `_readme_validate()` checks (line-boundary substring match):

1. `## Origin` — what this checkpoint is, base model, training data, recipe ref, compute, final metric, git sha
2. `## Falsifiers` — concrete reproducible tests with pass criteria + last result + run ref
3. `## Substrate` — VRAM (bf16 + 4-bit), python version, required packages, input format, context window, tokenizer
4. `## Caveats` — **at least 3 honest limitations** (raw#10 enforcement: counted via `- `/`* ` bullets in section)
5. `## Composability` — sister checkpoints, loader, hexad slot, compose recipe, downstream tasks, incompatibles

### 4.2 Failure mode

Non-conforming README aborts upload BEFORE the python bridge is invoked.
Error message names every missing heading explicitly.

```
FAIL: README missing required H2 headings: [## Falsifiers] [## Composability]
       (template: tool/hf_readme_template.md)
FAIL: Caveats section has 1 bullets (mk2 requires >=3 honest caveats per raw#10)
```

## 5. Naming convention (mk2)

### 5.1 Format

```
<org>/<family>-<version>-<stage>[-<modifier>]
```

| Token | Constraints |
|---|---|
| `org` | 2-32 chars, lowercase alnum + dash |
| `family` | one of `{clm, alm, blm, vlm, slm, tlm, mlm, hexad, composite}` |
| `version` | `v<N>` (e.g. `v1`, `v4`) |
| `stage` | starts with one of `{sft-stage, dpo, merged, base, preview, dev}`; multi-token stages join remaining parts with `-` |
| `modifier` | optional; lowercase alnum + dash (extends stage with extra parts) |

### 5.2 Examples

| Repo | Verdict | Reason |
|---|---|---|
| `dancinlab/clm-v4-sft-stage1` | OK | family=clm, version=v4, stage=sft-stage1 |
| `dancinlab/blm-v3-dpo` | OK | family=blm, version=v3, stage=dpo |
| `dancinlab/vlm-v1-merged-rev2` | OK | family=vlm, version=v1, stage=merged-rev2 |
| `dancinlab/composite-v2-preview` | OK | family=composite, version=v2, stage=preview |
| `BadOrg/clm-v4-sft-stage1` | FAIL | org has uppercase |
| `nodash` | FAIL | no `/` separator |
| `dancinlab/zzz-v4-sft-stage1` | FAIL | family `zzz` not in allowlist |
| `dancinlab/clm-x-sft-stage1` | FAIL | version `x` does not start with `v` |
| `dancinlab/clm-v4` | FAIL | missing stage (need >=3 dash-separated parts) |

### 5.3 Sister BG coordination

The mk2 naming convention spec (sister BG output) may extend the family /
stage allowlists. The hexa wrapper hardcodes the current set inline; if a
sister-BG-defined `docs/anima_naming_convention_mk2_2026_05_03.md` (or
similar) lands first with additional families, update
`_naming_allowed_families()` + `_naming_allowed_stage_prefixes()` to
match. The current inline set is the conservative starting point.

## 6. Audit / observability

### 6.1 Per-upload log

Path: `state/hf_upload_audit/<UTC-ts>_<repo-with-/-as-__>.jsonl`

Schema (one JSON object per line; appended on each invocation):

```json
{
  "ts_utc": "2026-05-03T14:21:00Z",
  "mode": "upload" | "dry_run",
  "repo": "dancinlab/clm-v4-sft-stage1",
  "tag": "step-25k",
  "private": 0,
  "file_count": 142,
  "total_bytes": 524288000,
  "sha256_map": {"adapter_model.safetensors": "<64hex>", ...},
  "commit_url": "https://huggingface.co/<repo>/commit/<sha>",
  "tag_url": "https://huggingface.co/<repo>/tree/step-25k",
  "attempts": 1,
  "duration_sec": 47.3,
  "outcome": "ok" | "fail" | "dry_run_ok",
  "error": null
}
```

### 6.2 Aggregate ledger

Path: `state/hf_upload_ledger_2026_05.jsonl`

Appended by the hexa wrapper after each operation; one line per
invocation; smaller schema (no sha256_map) for fast scan / grep.

### 6.3 F-HF-UPLOAD-1 falsifier

**Statement**: every audit entry MUST contain `sha256_map` (non-empty for
upload/dry_run modes), `file_count` (int >= 1), `outcome` (string).

**Pass criterion**: `jq -e 'has("sha256_map") and has("file_count") and has("outcome")'`
returns true on every line of every per-upload log file.

**Last result**: dry-run smoke test 2026-05-03 — 1 entry, all 3 keys
present, sha256_map has 2 entries, file_count=2, outcome=dry_run_ok.

## 7. Cost / safety

- **HF storage**: $0 for public repos under 5 GB; private repo costs
  covered by `dancinlab` org subscription.
- **HF API**: free tier; rate limits per token (see raw#10 caveat below).
- **No automatic uploads**: pre-push hook ONLY validates naming; never
  triggers `--upload`. The operator must explicitly invoke `--upload`.
- **This cycle cost**: $0 (no actual upload to HF, only dry-run + selftest).

## 8. Failure handling

| Failure | Mitigation |
|---|---|
| HF token missing | bridge returns `error: "no_token"` with prescriptive message |
| huggingface_hub not installed | bridge returns `error: "huggingface_hub_unavailable"` |
| Network blip / 5xx | exponential backoff: 2s, 4s, 8s; up to 3 attempts |
| 429 rate limit | same backoff path; bridge propagates `HfHubHTTPError` |
| README missing required H2 | hexa wrapper aborts with explicit list of missing headings |
| Naming convention violation | hexa wrapper aborts with prescriptive error |
| Final upload failure | writes `state/markers/anima_hf_upload_mk2_fail.marker` JSON + audit entry with `outcome: "fail"` |

## 9. raw#10 honest caveats

1. **HF rate-limit not coordinated across concurrent runs** — exponential
   backoff handles single-stream 429s, but parallel uploads from multiple
   BG subagents may collectively exceed quota. No cross-process semaphore.
2. **Large file LFS handling delegated to huggingface_hub** — the audit
   log records the LOCAL sha256 of every file, NOT the LFS oid on the
   hub side. Pointer files vs raw uploads are not surfaced. Verify
   integrity by re-downloading + recomputing sha256 if needed.
3. **Naming validation is permissive** — current inline allowlist is the
   conservative starting set. Sister BG (mk2 naming convention spec) may
   extend it; until then, false-negatives are possible (e.g., a new
   family added on the hub side will be rejected here until the wrapper
   is updated). False-positives are also possible if a non-conforming
   repo happens to match the loose `<family>-<version>-<stage>` shape.
4. **Pre-push hook only inspects LATEST commit** on each pushed ref;
   older commits in the push range are NOT scanned (perf + scope).

## 10. raw compliance summary

- **raw#9** (hexa-only): 1 `.py` file in approved `_python_bridge/` location, justified by huggingface_hub SDK requirement; all other source is hexa
- **raw#10** (honest caveats): section 9 enumerates 4 honest caveats; README template enforces >=3 caveats in every uploaded checkpoint
- **raw#15** (no personal-path leak): all paths constructed via `$HOME` env, no hardcoded `/Users/<name>/`; pre-push hook never logs absolute paths beyond repo root
- **raw#37** (transient emit): bridge invocation uses tmpfile that is removed immediately after exec
- **$0 cost** this cycle: no HF API calls beyond dry-run mode (which makes zero network calls)

## 11. Roadmap (post-this-cycle)

1. Wire pre-push hook into `.git/hooks/pre-push` (manual install per developer; not auto-installed by repo).
2. Add `--multi-upload` mode for batched savepoint pushes (post-P9 SFT step-{5,10,25,50}k).
3. Cross-process rate-limit semaphore via `state/hf_upload_audit/.lock` if parallel BG uploads become a workflow.
4. F-HF-UPLOAD-2: verify hub-side LFS oid matches local sha256 (round-trip download + recompute).
5. Retire `_python_bridge/hf_upload_runner.py` if hexa gains a stdlib http client + LFS encoder.
