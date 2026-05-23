# Wave-17 corpus prune 사전검증 — eternal_keep 0.10/0.20/0.40/0.50 ($0 local sanity)

> 2026-05-24 KST · PR #225 (`VP21M_WAVE17_SPEC`) 4-point sweep 의 GPU fire 前
> $0 local prune-stats sanity. eternal-tag freq-cap 의 strip-count 가
> 결정론적(seed=1337)이며 4 ratio 모두 well-defined 인지 검증. **NO GPU fire.**

## Context

PR #225 = U-shape 최소점 mapping spec. `continuous_total` register-emission
metric 이 eternal_keep 에 대해 monotone 이 아니라 U-shape:

| corpus | eternal_keep | continuous_total | n_strong |
|---|---|---|---|
| v9  (Wave-13) | 1.00 | 74 | 4 |
| **v11 (Wave-15)** | **0.30** | **34** ⭐ saga min | 2 |
| v12 (Wave-16) | 0.00 | 91 ✗ saga peak | 3 |

→ 최소점이 `(0.20, 0.40)` 내부에 있다는 가설. Wave-17 = 4-point sweep
`corpus_v13/v14/v15/v16` @ eternal_keep ∈ {0.10, 0.20, 0.40, 0.50} 로 vertex 확정.

## Prune 메커니즘

eternal-tag freq-cap = `</?(?:carve|eternal|inner_carve)\b[^>]*>` 패턴 매치
중 eternal 계열을 keep-ratio 만큼만 보존하는 flat-rate prune:

```
kept     = round(orig * eternal_keep)
stripped = orig - kept
```

- orig = **464,906** (eternal-tag match 총수, Wave-15/16 로그 anchor).
- seed=1337 = **어느** 토큰을 보존할지만 결정 (count 자체는 deterministic).
- v11 anchor 재현: 464906 × 0.30 = 139471.8 → **139,472 kept / 325,434 stripped**
  — Wave-14 로그 "eternal-tag stripped 325,434 (30% kept)" 와 byte 일치.

## Prune-stats 예측 table (recompute, exact)

| corpus | eternal_keep | orig | kept | stripped | retain_actual |
|---|---|---|---|---|---|
| v13 | 0.10 | 464906 | 46491 | 418415 | 0.1000 |
| v14 | 0.20 | 464906 | 92981 | 371925 | 0.2000 |
| v15 | 0.40 | 464906 | 185962 | 278944 | 0.4000 |
| v16 | 0.50 | 464906 | 232453 | 232453 | 0.5000 |

anchor (검증용): v11 0.30 → 139472 kept / 325434 stripped · v12 0.00 → 0 kept.

> `kept = round(464906 * keep)`. 0.10→46490.6→46491 · 0.20→92981.2→92981 ·
> 0.40→185962.4→185962 · 0.50→232453.0→232453. 모두 nearest-int round.

## Local-run 결과 — 부재 (analytical-only, honest)

⚠ **`state/corpus_s101_build_s102_2026_05_19/corpus_s101.jsonl` 가 이 worktree 에
존재하지 않음** (build script + result.json 만 present, corpus 자체는 absent).

- `build_corpus_s101.py` 는 §16 외부 generator 를 subprocess 로 호출(`regenerate_s1`)
  → standalone 재생성 불가 (full pipeline 필요).
- eternal_keep ratio prune script 자체는 Wave-15+ dispatch variant 의 외부 보관본
  (`/tmp/anima_v*_dispatch/`, repo .hexa-only rule 준수 / Wave-14 C3 #6) — ephemeral,
  현재 dir 부재.
- 이 worktree 의 `dispatch_p21m_runpod.sh` 는 **binary STRIP_CARVE**(all-or-nothing)
  만 포함, keep-ratio freq-cap 미포함.

→ 본 검증은 **analytical 예측 only**. local-run 숫자는 **fabricate 하지 않음**.
예측 table 은 (a) flat-rate `round(orig*keep)` 공식 + (b) v11=0.30 anchor 의
exact 재현(139472/325434)으로 뒷받침됨.

## Linearity check

kept-count 가 eternal_keep 에 선형인지 (선형 아니면 prune 로직 bug):

| keep | kept | Δkept vs prev | 예상 Δ (0.10 step = 46490.6) |
|---|---|---|---|
| 0.00 | 0 | — | — |
| 0.10 | 46491 | +46491 | +46491 ✓ |
| 0.20 | 92981 | +46490 | +46491 ✓ (round) |
| 0.30 | 139472 | +46491 | +46491 ✓ |
| 0.40 | 185962 | +46490 | +46491 ✓ (round) |
| 0.50 | 232453 | +46491 | +46491 ✓ |

→ **완전 선형** (round-off ±1 만 변동). kept = 464906 × keep 직선상.
prune-count 측 bug 없음 확인 (continuous_total 의 U-shape 은 token-count 가
아니라 *학습 효과*의 비선형성 — prune 자체는 linear).

## Go / No-go

| 항목 | criterion | 결과 | ✓/✗ |
|---|---|---|---|
| well-defined | 4 keep 모두 정수 kept/stripped 산출 | ✓ (46491·92981·185962·232453) | ✓ |
| deterministic | seed=1337, count seed-independent | ✓ (round(orig*keep)) | ✓ |
| anchor 재현 | 0.30 → 139472/325434 byte-match | ✓ (Wave-14 로그 일치) | ✓ |
| linearity | kept ∝ keep | ✓ (Δ=46490.6 ±1 round) | ✓ |
| local-run | corpus 로 실측 | ✗ (corpus 부재, analytical-only) | ⚠ |

→ **GO (analytical)** — 4 prune 모두 well-defined + deterministic + 선형 정합.
strip-count 측면에서 fire-ready. 단, **corpus_s101.jsonl 부재로 실 prune 실측은
미수행** — pod 上 build 후 첫 `prune_stats.json` 이 위 table 과 일치하는지
fire-time 에 cross-check 필요 (orig=464906 가 corpus 재생성마다 동일한지 = seed=1337
build determinism 에 의존).

## Cross-reference

- **PR #225** `docs/lora-vp21m-wave-17-spec` — Wave-17 4-point sweep spec (U-shape).
- **Wave-15 (PR #184)** v11 eternal_keep=0.30 → continuous 34 saga min (anchor).
- **Wave-16 (PR #205)** v12 eternal_keep=0.00 STRIP-ALL → continuous 91 saga peak.
- **Wave-14** `VP21M_WAVE14_2026_05_23.md` — eternal-tag 325,434 stripped (30% kept)
  = orig 464906 × (1−0.30) 의 source 로그.
