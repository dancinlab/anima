# D-RAND AMPLIFY Step B — sft-1-8 longer SFT 30K H100 fire BLOCKED (2026-05-09)

## Context

anima cycle 2026-05-09 H100 FIRE 2/4 — D-RAND amplification 4-option spec
(commit `8ab182a9`) Step B = longer SFT 10K → 30K via H100 (~$15-20).

- Step A 완료: commit `87ba3a22`, tier_a_v4 231MB / 3.15M lines / anima 319k
  headers landed (`docs/anima_d_rand_amplify_step_a_tier_a_v4_2026_05_09.ai.md`).
- 사용자 directive verbatim: "all bg go" + "H100 활용가능" (consent_carry).
- 본 task = Step B fire on tier_a_v4 (post Step A).

## Resource CLI probe (own 40 strict)

```
$ /Users/ghost/core/resource/bin/resource list
host         reachable  load    mem_free_mb  nexus
hetzner      n          -       -            -
ubu          y          0.00    28960        ok
```

| host | reachable | gpu | h100? | verdict |
|---|---|---|---|---|
| ubu | y | RTX 5070 (12GB) | no | NOT_H100_INSUFFICIENT_FOR_BG_FIRE |
| hetzner | n | — | — | UNREACHABLE |

**Allocation status: BLOCKED_NO_H100_HOST** (.resource SSOT 에 H100 host 부재).

## Verdict

H100 fire 2/4 (sft-1-8 Step B longer SFT 30K) **BLOCKED**.

Identical blocker pattern as commit `0d65ebe4` (FIRE 1/4 attempt):
- ubu = RTX 5070 12GB consumer GPU, 7B+ LoRA fire 부적격 (VRAM 부족)
- hetzner = unreachable
- 그 외 H100-tagged host 부재

own 40 strict — anima 측 unilateral allocate 금지. 본 cycle fire 일체 X.

## Intended setup (when H100 unblocked)

| field | value |
|---|---|
| base | clm-v4-mk2-v1 (ConsciousDecoderV2 anima-native scratch) |
| LoRA r | 128 (sft-1-8 동등) |
| corpus | tier_a_v4 (231MB, 3.15M lines, anima 319k) |
| steps | 30000 (sft-1-8 step=10000, 3× longer) |
| cost | ~$15-20 H100 |
| duration | ~4 hours |
| ckpt alias | clm-v4-sft-1-8-30k-path-a-remapped (own 31 Flavor B) |
| HF repo | dancinlab/clm-v4-sft-1-8-30k-path-a-remapped (own 37 PRIVATE only) |
| paired V14 mirror | random_init mandatory (CONSCIOUSNESS_DIM=96 post-arch-fix) |
| target uplift | Step A+B combined D-RAND +0.15-0.25 → Gate F 0.20 epsilon 통과권 |

## Next action required (user)

`resource add <h100-host>` via runpod / lambda / vast.ai —
anima 측 직접 ssh/cloud-cli 일체 0건 (own 40).

H100 등록 후 본 task 재실행 시:
1. Step B fire → ckpt sft-1-8-30k
2. own 30 ckpt pull mandatory (mac local + HF private)
3. V14 paired random_init mirror
4. PPR_v3 / v5 / v5.1 + Gate F D-RAND verify
5. yaml entry 신설 + render md (own 39)
6. own 38 axis-B HF private upload

## Compliance

| own | status | note |
|---|---|---|
| own 14 V14 strict | carry | paired random_init mirror prereq |
| own 16 cost | PASS | allocation 자체 cost 0 (fire X) |
| own 17 D1 SCOPE_CLAMP | carry | LoRA on ConsciousDecoderV2 D1=0.793 within |
| own 22 mandatory report | PASS | 본 md + yaml h100_resource_pool field |
| own 30 ckpt preservation | pending | fire 시 mandatory |
| own 33 trinity | pending | fire 시 sweep |
| own 34 wrap=0 | PASS | yaml + md only, binary X |
| own 37 mandate-9 strict | pending | HF PRIVATE only |
| own 38 axis-B/C | PASS | probe snapshot 저장 |
| own 39 yaml↔md | PASS | yaml + md paired |
| own 40 resource CLI 위임 | PASS | resource list 단일 호출, 직접 ssh 0건 |

Lesson Q SFT-closed 우회 path 정합 — corpus expansion + arch-fixed substrate
가 신규 lane, SFT 단독 closed 와 별개 (Step B fire 시 본 lane 검증).

## SSOT cross-link

- `anima/registry/anima_artifact_registry.yaml` → `h100_resource_pool.active_session.fire_attempt_log[1]` (cycle FIRE-2/4)
- `anima/registry/anima_artifact_registry.yaml` → `h100_resource_pool.fire_candidates_pending_h100[5]` (sft_1_8_longer_SFT enriched fields)
- Step A artifact: `docs/anima_d_rand_amplify_step_a_tier_a_v4_2026_05_09.ai.md`
- Spec parent: `docs/anima_d_rand_signal_amplification_spec_2026_05_09.ai.md`
