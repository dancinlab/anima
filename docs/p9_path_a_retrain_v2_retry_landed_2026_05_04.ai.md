# P9 Path A retrain v2 RETRY — handoff (BG-α' 2026-05-04)

**Verdict: `INFRASTRUCTURE_FAIL_HF_TOKEN_EXPIRED`**
**Action required: rotate Mac HF token before any v2 retrain attempt.**

## Context

BG-α (commit `79861cda`) retrain v2 corpus_mix step crashed with
`datasets.exceptions.DatasetNotFoundError: Dataset 'cais/mmlu' doesn't exist on the Hub or cannot be accessed`.
That cycle MISDIAGNOSED the failure as a dataset-access issue.
This BG-α' retry exposed the actual root cause.

## ROOT CAUSE (BG-α' diagnostic)

**The HF token in Mac secrets (`secret get --raw huggingface.token`) is EXPIRED.**

### Evidence

1. **H100 setup phase** (`state/.../h100_orchestrator.log`):
   ```
   line  8: requests.exceptions.HTTPError: Invalid user token. The token from
            HF_TOKEN environment variable is invalid. Note that HF_TOKEN takes
            precedence over `hf auth login`.
   line 11: [setup] hf auth: Invalid user token...
   line 16: User Access Token "anima" is expired
   line 14-19: Llama-3.2-3B base download FAILED (gated repo, 401)
   ```

2. **Mac-side curl probe** (BG-α' diagnostic):
   ```
   curl -H "Authorization: Bearer <secret-token>" https://huggingface.co/api/whoami-v2
   → {name: null, type: null}        # token rejected; anonymous-equivalent

   curl -H "Authorization: Bearer <secret-token>" \
        https://huggingface.co/api/datasets/cais/mmlu/resolve/main/all/auxiliary_train-00000-of-00001.parquet
   → HTTP/2 401
   ```

3. **Same token, anonymous Mac call** (`HF_TOKEN` unset):
   ```
   from datasets import load_dataset
   load_dataset('cais/mmlu', 'all', split='test[:5]')
   → OK loaded 5 samples            # public dataset, anonymous access works
   ```

### Why BG-α misdiagnosed

`DatasetNotFoundError` surface message
"Dataset 'X' doesn't exist on the Hub or cannot be accessed"
is **identical** for:
- Genuinely missing dataset
- Public dataset accessed with invalid auth header (401)

The `datasets` library does NOT distinguish these in the user-visible
exception. BG-α assumed (a); BG-α' diagnostic confirmed (b).

## Pod outcome

| field | value |
|---|---|
| pod_id | `nxehc0tdpf88ni` |
| pod_terminated | true |
| pod_kill_verified_404 | true (per `runpodctl pod get` post-kill = "pod not found / status 404") |
| wall_time | 4 min |
| actual_cost_usd | $0.20 |
| budget_target / cap | $24 / $35 (well under) |
| corpus_mix | FAILED at slice_B1_mmlu after slice A loaded (30000 anima samples) |
| train | NOT REACHED |
| eval | NOT REACHED |

## Code fix DEPLOYED (insufficient alone, but reusable post-rotation)

**File:** `tool/transient_py/p9_retrain_v2_corpus_mix.py`

1. **Initial fix** (deployed pre-launch, did not address root cause):
   - Explicit `token=` propagation from 4 env-var aliases
   - `_load_with_retry()` exp-backoff (8/16/32/64s) on transient errors
   - `_load_with_fallback()` per-slice alternate chain:
     - B1 MMLU: `cais/mmlu` → `lighteval/mmlu`
     - B2 TriviaQA: `mandarjoshi/trivia_qa` → `trivia_qa`
     - B3 wikitext: `Salesforce/wikitext` → `wikitext`
   - `--dry-run` mode for Mac sanity check

2. **Defensive fix** (deployed post-failure, addresses the class of issue):
   - `_validate_hf_token()` — probes HF `/api/whoami-v2` to detect expiration
   - `_purge_invalid_token()` — when env token is invalid:
     - Unsets all 4 HF_*_TOKEN env-var aliases
     - Removes cached token files (`~/.cache/huggingface/token`, `~/.huggingface/token`)
     - Lets `datasets`/`huggingface_hub` fall back to anonymous (works for public)
   - `main()` calls purge before any `load_dataset` (skipped under `--dry-run`)

   **Coverage**: hardens slices B1/B2/B3/C1 (all public) against expired-token.
   **Limitation**: cannot rescue C2 lmsys (gated:auto) or Llama-3.2-3B base
   download (gated:manual) — those REQUIRE a valid HF token.

## Blocker for full retry

**HF_TOKEN secret rotation required (user-side, outside BG-α' scope).**

### User action required

```bash
# 1) generate new HF token at https://huggingface.co/settings/tokens
#    (request access to meta-llama/Llama-3.2-3B if needed)
# 2) write to Mac secrets
secret set huggingface.token <new-valid-hf-token>
# 3) optionally accept lmsys/lmsys-chat-1m gating click-through
#    (not required — code falls back to teknium/OpenHermes-2.5 anyway)
# 4) re-run retry (or new state dir for retry-2 cycle)
bash state/p9_path_a_retrain_v2_retry_2026_05_04/exec.bash
```

The deployed corpus_mix.py is reusable as-is; it will validate the token
at startup before any pod cost is incurred (well, technically still after
pod boot — see "Lessons new" L9 for pre-launch validation).

## Lessons new

- **L9** — `token_validate_pre_launch`: BEFORE pod boot, hit HF
  `/api/whoami-v2` with the Mac secrets HF_TOKEN; if returns `name=null`,
  FAIL FAST locally (zero pod cost) with explicit
  `ROOT_CAUSE=HF_TOKEN_EXPIRED`. Currently exec.bash Stage 0 only validates
  length > 0 and not-redacted form, NOT actual auth validity.
  Should be added to all H100 orchestrator hexas.
- **L10** — `dont_pass_invalid_token_to_load_dataset`: `datasets` library
  + `huggingface_hub` do NOT auto-fallback from invalid-token to anonymous;
  an invalid `HF_TOKEN` env var causes 401 → `DatasetNotFoundError` on
  PUBLIC datasets too. Always validate-or-purge before passing to library.

## Deliverables

| path | content |
|---|---|
| `state/p9_path_a_retrain_v2_retry_2026_05_04/verdict.json` | full verdict + ROOT_CAUSE + 9 honest C3 |
| `state/p9_path_a_retrain_v2_retry_2026_05_04/exec.bash` | retry-flavored exec (state dir + pod name updated) |
| `state/p9_path_a_retrain_v2_retry_2026_05_04/run_h100.bash` | unchanged from BG-α |
| `state/p9_path_a_retrain_v2_retry_2026_05_04/results/corpus_mix.log` | full failure trace |
| `state/p9_path_a_retrain_v2_retry_2026_05_04/h100_orchestrator.log` | pod-side setup output (Llama download FAIL evidence) |
| `tool/transient_py/p9_retrain_v2_corpus_mix.py` | EDITED with retry/fallback + token-validate/purge |
| `docs/p9_path_a_retrain_v2_retry_landed_2026_05_04.ai.md` | this handoff |

## Next-action graph

```
BG-α' (this) → INFRASTRUCTURE_FAIL_HF_TOKEN_EXPIRED
   │
   ├─ user: rotate HF token (one-time, ~5min)
   │
   └─ BG-α'' retry-2: re-run exec.bash (or new state dir)
         │
         └─ if corpus_mix succeeds: train phase resumes per F-PA-RETRAIN-v2 spec
```
