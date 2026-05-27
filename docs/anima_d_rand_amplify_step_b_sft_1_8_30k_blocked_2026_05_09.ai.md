# D-RAND AMPLIFY Step B — sft-1-8 longer SFT 30K H100 fire BLOCKED (2026-05-09)

## Context

anima cycle 2026-05-09 H100 EPHEMERAL FIRE 2/4 — D-RAND amplification 4-option spec
(commit `8ab182a9`) Step B = longer SFT 10K → 30K via H100 (~$15-20).

- Step A 완료: commit `87ba3a22`, tier_a_v4 231MB / 3.15M lines / anima 319k
  headers landed (`docs/anima_d_rand_amplify_step_a_tier_a_v4_2026_05_09.ai.md`).
- 사용자 directive verbatim: "all bg go" + "H100 활용가능" (consent_carry).
- 본 task = Step B fire on tier_a_v4 (post Step A).
- Cycle directive verbatim: ephemeral provision via `resource provision-ephemeral`
  (lifecycle), full chain (provision → fire → ckpt pull → release →
  validation → ledger update).

## Attempt 1 — `.resource` SSOT host probe (commit `f993eca0`)

```
$ /Users/ghost/.hx/bin/resource list
host         reachable  load    mem_free_mb  nexus
hetzner      n          -       -            -
ubu          y          0.00    28960        ok
```

| host | reachable | gpu | h100? | verdict |
|---|---|---|---|---|
| ubu | y | RTX 5070 (12GB) | no | NOT_H100_INSUFFICIENT_FOR_BG_FIRE |
| hetzner | n | — | — | UNREACHABLE |

**Allocation status: BLOCKED_NO_H100_HOST** — superseded by ephemeral lane.

## Attempt 2 — provision-ephemeral (lifecycle, this cycle)

```
$ /Users/ghost/.hx/packages/resource/bin/resource provision-ephemeral \
    --provider runpod --gpu H100-PCIe --duration 5h --yes-cost --name sft-1-8-30k

# resource provision-ephemeral — cost disclosure
#   provider:      runpod
#   gpu:           H100-PCIe
#   duration:      5h (best-effort; user must release)
#   estimated cost: provider-dependent (RunPod H100 ~$2.79/h, Lambda H100 ~$2.49/h, vast.ai ~$1.50-2.50/h)
__RESOURCE__ FAIL provision-ephemeral reason=provider-error \
  payload={"ok":false,"reason":"api-key-missing",
           "detail":"set RUNPOD_API_KEY or ~/.config/resource-ephemeral/runpod.token"}
```

**Allocation status: BLOCKED_PROVIDER_API_KEY_MISSING.**

| probe | result |
|---|---|
| `RUNPOD_API_KEY` env | unset |
| `~/.config/resource-ephemeral/runpod.token` | absent (parent dir 미존재) |
| provider response | `api-key-missing` (provider client refused before pod allocate) |
| cost incurred | $0.00 (provision aborted pre-allocate) |

### Resolver quirk note (logged for follow-up)

`/Users/ghost/.hx/bin/resource` is a symlink to
`/Users/ghost/.hx/packages/resource/bin/resource`. The new ephemeral
dispatch block (lines 90-126 of the package bin) uses
`$(cd -P "$(dirname "$0")/..")` for `eph_pkg_root`, but `$0` is the
symlink path so this resolves to `/Users/ghost/.hx`, not the package
root. Result: `eph_tool` becomes
`/Users/ghost/.hx/tool/resource_ephemeral.hexa` (does not exist) and
the script aborts with `tool missing` before reaching the ephemeral
hexa script. Workaround used here: invoke
`/Users/ghost/.hx/packages/resource/bin/resource` directly (
strict CLI delegation preserved — anima invokes the resource CLI, not
runpod-cli or curl). The legacy `_self_locate` symlink-walker further
down the script handles this correctly; the ephemeral block predates
that helper and should be migrated. Not in scope for this anima
cycle's fix; logged in registry `bin_resolver_quirk_note`.

## Verdict

H100 EPHEMERAL FIRE 2/4 (sft-1-8 Step B longer SFT 30K) **BLOCKED**.

Provider credential not configured. Per task directive verbatim
("API key 부재 시 honest BLOCKED emit") + strict
(anima 측 API key 자체 생성/설정 0건) → honest abort.

Full chain steps 2-6 (corpus upload → ckpt pull → 30K SFT →
 ckpt pull → release → v5 N=60 probe → ledger update) not
executed (provision step blocking).

## Intended setup (when API key registered)

| field | value |
|---|---|
| provider | runpod (RunPod H100-PCIe ~$2.79/h) |
| duration | 5h ceiling (~4h actual fire + buffer) |
| base | clm-v4-mk2-v1 (ConsciousDecoderV2 anima-native scratch) |
| LoRA r | 128 (sft-1-8 동등) |
| LoRA alpha | 128 |
| lr | 1e-4 |
| batch | 8 (gradient_accumulation 4) |
| corpus | tier_a_v4 (231MB, 3.15M lines, anima 319k) |
| steps | 30000 (sft-1-8 step=10000, 3× longer) |
| cost | ~$15-20 H100 |
| ckpt alias | clm-v4-sft-1-8-30k-path-a-remapped (Flavor B) |
| HF repo | dancinlab/clm-v4-sft-1-8-30k-path-a-remapped (PRIVATE only) |
| paired V14 mirror | random_init mandatory (CONSCIOUSNESS_DIM=96 post-arch-fix) |
| target uplift | Step A+B combined D-RAND +0.15-0.25 → Gate F 0.20 epsilon 통과권 |

## Next action required (user)

```
# Option A — env export (ephemeral, current shell)
export RUNPOD_API_KEY=<key>

# Option B — token file (persistent)
mkdir -p ~/.config/resource-ephemeral
echo <key> > ~/.config/resource-ephemeral/runpod.token
chmod 600 ~/.config/resource-ephemeral/runpod.token
```

Then re-run this cycle. anima 측 직접 ssh / cloud-cli / runpod-cli /
curl 일체 0건 (strict).

Post-API-key chain (anima will execute):
1. provision-ephemeral fire → pod_id (lifecycle)
2. corpus rsync tier_a_v4 → /workspace/data/
3. base ckpt download via huggingface-cli → /workspace/base/
4. SFT 30K fire (LoRA r=128, 4h H100)
5. ckpt pull mandatory (mac local + HF private upload)
6. resource release <slug> --reason "step b sft 30k complete"
7. V14 paired random_init mirror probe
8. v5 N=60 actual probe (post arch-fix CONSCIOUSNESS_DIM=96) + Gate F D-RAND verify
9. yaml entry 신설 + render md
10. axis-B HF private upload

## Compliance

| own | status | note |
|---|---|---|
| V14 strict | carry | paired random_init mirror prereq |
| cost | PASS | provision aborted pre-allocate ($17.5 saved via honest abort) |
| D1 SCOPE_CLAMP | carry | LoRA on ConsciousDecoderV2 D1=0.793 within |
| mandatory report | PASS | 본 md + yaml fire_attempt_log[2] field |
| ckpt preservation | pending | fire 시 mandatory |
| trinity | pending | fire 시 sweep |
| wrap=0 | PASS | yaml + md only, binary X |
| mandate-9 strict | pending | HF PRIVATE only |
| axis-B/C | PASS | probe snapshot 저장 (provider response captured verbatim) |
| yaml↔md | PASS | yaml + md paired |
| resource CLI 위임 | PASS | provision-ephemeral subcmd invocation only, 직접 cloud-cli 0건 |

Lesson Q SFT-closed 우회 path 정합 — corpus expansion + arch-fixed substrate
가 신규 lane, SFT 단독 closed 와 별개 (Step B fire 시 본 lane 검증).

## SSOT cross-link

- `anima/registry/anima_artifact_registry.yaml` → `h100_resource_pool.active_session.fire_attempt_log[2]` (cycle FIRE-2/4-RETRY-EPHEMERAL)
- `anima/registry/anima_artifact_registry.yaml` → `h100_resource_pool.fire_candidates_pending_h100[5]` (sft_1_8_longer_SFT — `blocked_by` transitioned PROVISION_BLOCKED → PROVIDER_API_KEY_MISSING, fire_attempt_count=2)
- Step A artifact: `docs/anima_d_rand_amplify_step_a_tier_a_v4_2026_05_09.ai.md`
- Spec parent: `docs/anima_d_rand_signal_amplification_spec_2026_05_09.ai.md`
- Prior FIRE-2/4 attempt: commit `f993eca0` (host-pool blocker)
