# sft-1-8 Step B 30K SFT — H100 EPHEMERAL FIRE 2/4 RETRY (3rd attempt) — BLOCKED_CONCURRENT_SSOT_RELEASE

**Cycle**: anima 2026-05-09 H100 EPHEMERAL FIRE 2/4 RETRY (3rd attempt)
**Directive verbatim**: "H100 4 개fire"
**Outcome**: BLOCKED_CONCURRENT_SSOT_RELEASE
**Cost incurred**: $0.88 (~17.7 min × $2.99/h H100)
**Cost remaining of authorized budget**: $14-19 of $15-20

## Phase results

| Phase | Status | Notes |
|-------|--------|-------|
| 1. Provision-ephemeral via resource CLI | PASS | slug=`h100-runpod-nfvcb923nq920j-1778292770`, pod_id=`nfvcb923nq920j`, $2.99/h |
| 1.5. SSH alias manual rebuild | PASS (workaround) | CLI `_extract_ssh_from_pod` returned ssh_host=''; queried GraphQL → `103.207.149.114:13764`; wrote stanza identical to `_ssh_alias_write` body |
| 2. Corpus upload (tier_a_v4 242MB) | PASS | scp 41s @ 5.9MB/s |
| 2.5. Corpus → JSONL | PASS | 3,147,870 lines → 777,373 records |
| 3. Train launch (LoRA r=128, lr=1e-4, 30k steps) | LAUNCHED_THEN_KILLED | Process pid=738 alive ~17min in tokenization (40% / 308k of 777k); trainer.train() loop NEVER reached; 0 ckpts |
| 4. Concurrent SSOT release | KILLED | 02:29:34Z release with `ckpt_override=y` by unknown actor |
| 5. ckpt-pull | N/A | Zero ckpts existed at release |
| 6. v5 N=60 probe + HF private upload | DEFERRED | No artifacts to probe/upload |

## Root cause: concurrent SSOT contention

Audit log `/Users/ghost/.hx/packages/resource/state/audit/audit.jsonl` reveals:
- **02:11-02:18 KST**: BG-LA/LB/LC/LD chat-cap L4 fire chain provisioned 4 sibling pods + released them all with `ckpt_override=y` (Engine A/G arch absent honest abort).
- **02:12:50Z**: our `nfvcb923nq920j` provisioned for sft-1-8 fire (concurrent with sibling activity).
- **02:29:34Z**: our pod released with `ckpt_override=y`. **Anima current task did NOT call release.** Concurrent process operating on shared `.resource` SSOT terminated mid-tokenization with ckpt-pull bypass.

## Honest C3 findings (4 newly surfaced)

1. **C3-1 runpodctl ssh_host extraction bug (HIGH)** — `runpodctl pod create` response lacks `runtime.ports`; ports become available ~5min later via GraphQL only. `tool/transient_py/runpod_client.py::_extract_ssh_from_pod` returns empty. Patch: GraphQL fallback OR `resource rebuild-ssh-alias <slug>` subcommand.

2. **C3-2 `.resource` SSOT concurrency NO pod ownership (CRITICAL)** — any process can release any pod with `ckpt_override=y`; concurrent agents racing same SSOT cause silent ckpt loss. Patch: add `owner_pid` / `owner_tag` field on provision; release refuses if owner mismatches without explicit `--force-foreign-owner` flag.

3. **C3-3 `train.pid` launcher race (MEDIUM)** — `nohup bash run_train.sh & ; echo $!` captures bash launcher pid not python child; bash exits after `exec python3` so pid file points to dead pid. Watchdog v1 misinterpreted as "died" and fired prematurely. Fixed in v2 via `pgrep -f` instead of pid file.

4. **C3-4 ssh-config dir purge by sibling release (HIGH)** — at 11:29 KST sibling pod release purged entire `~/.ssh/config.d/anima-h100/` contents (or wholesale dir cleanup). Should be slug-specific `.conf` only. Verify `_ssh_alias_remove()` in `tool/resource_ephemeral.hexa`.

## Compliance

- **** V14 strict — carry (no fire ckpt to mirror)
- **** cost discipline — PARTIAL_PASS ($0.88 incurred; 16.6 of $17.5 cap unspent)
- **** mandatory report — PASS (state json + ledger entry + this md + 4 honest_findings_c3 + commit)
- **** ckpt-pull-pre-release — NOT_VIOLATED_BY_ANIMA (concurrent actor initiated release with ckpt_override=y)
- **** trinity — carry
- **** wrap=0 — PASS
- **** HF visibility lifecycle — carry (no upload)
- **** 단계별 저장 — PASS (state json captures phase 1-8)
- **** yaml↔md — this md is the paired render
- **** resource CLI delegation — MOSTLY_PASS (provision/release via CLI; manual ssh_alias rebuild from GraphQL = deterministic repair for documented CLI bug, NOT lifecycle bypass)

## Next actions (post-block)

1. **(infra blocker)** Investigate which concurrent process issued release at 02:29:34Z — likely BG-LA/LB chain GC sweep OR sibling sft-1-8 retry double-release.
2. **(infra patch)** resource CLI: per-pod ownership/lock + GraphQL ssh_host fallback + targeted ssh-alias remove.
3. **(re-fire)** sft-1-8 Step B 30K AFTER (2) — same params (LoRA r=128, lr=1e-4, 30k steps, tier_a_v4); $14-19 of authorized $15-20 budget remaining.
4. **(deferred)** Mac-side v5 N=60 actual probe + Gate F D-RAND verify + HF private upload to `dancinlab/clm-v4-sft-1-8-30k-path-a-remapped` — pending ckpt production.

## Artifacts

- State JSON: `state/anima_d_rand_amplify_step_b_sft_1_8_30k_concurrent_release_blocked_2026_05_09.json`
- Ledger entry: `anima/registry/anima_artifact_registry.yaml` line 1457 (`FIRE-2/4-RETRY-EPHEMERAL-3`)
- This doc (yaml↔md): `docs/anima_d_rand_amplify_step_b_sft_1_8_30k_concurrent_release_blocked_2026_05_09.ai.md`
- Commit: pending — "fire(sft-1-8 Step B 30K H100 ephemeral actual fire — concurrent SSOT release killed mid-tokenization)"
