# M4 — AXIS_MAP-FAN 7-axis env-var wiring fix (H_257)

@goal: H_257 silent-bypass 를 코드 레벨에서 정정 — dispatch 의 7-axis env-var 가
train script 에 실제로 도달하고, 경로가 존재하는 axis 는 train-loop 까지 wired.
(GPU 재발사 없음 — 진짜 ablation 은 merge 후 별도 step)

- 일자: 2026-05-25
- 인용 가설: `HEXAD/LIFE/H_257_axis_map_fan_env_var_silent_bypass.md`
- 라이브 surface: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/`
  - `train_p21h_v3.py` · `dispatch_p21h_v3_runpod.sh`
  - (state/ snapshot 이 곧 라이브 — 별도 canonical 복제본 없음. 두 파일 모두
    git-tracked 이며 PR #385/#342/#334/#204 가 이 경로로 직접 land 됨)

## 1. H_257 진단 재확인 (before grep)

H_257.1 예측대로 라이브 train script 는 env-var 를 0회 읽고 있었고, dispatch 의
7-axis env-var 는 PR #385 에서 `--flag` passthrough 까지만 land 되어 train 코드의
`cfg`/train-loop 에는 미반영(inert) 상태였다.

| 검증 | grep | before (origin/main) |
|------|------|----------------------|
| F-H257-1 | `os.environ\|getenv` in `train_p21h_v3.py` | **0 lines** (env-var 직독 0) |
| axis args parse | `--curriculum-phase-steps` 외 6 | 7개 존재 (PR #385, default=상수) |
| axis → cfg | `args.curriculum_phase_steps` in `cfg=dict(...)` | **0** (parse+log 만, cfg 미포함) |
| axis → train-loop | head_g/freeze 가 loss/optimizer 에 반영 | **0** (`logits_g` 미사용, freeze 코드 없음) |
| dispatch passthrough | `--curriculum-phase-steps $P21H_...` in `$CMD` | 7개 존재 (PR #385) |

결론: PR #385 가 H_257 의 "dispatch→train passthrough"는 닫았으나, train script 가
값을 (a) env-var 로 직독하지 않고 (b) `cfg`/train-loop 에 흘려보내지 않아 **여전히
trivial identity** — H_257 의 핵심(7-axis 가 inert)은 미해결이었다.

## 2. 각 axis 의도 + 경로 존재 여부

dispatch 7 env-var 의 의도와, train 코드에 해당 동작 경로가 이미 있는지 점검:

| axis | env-var | 의도 | 코드 경로 존재? | M4 처리 |
|------|---------|------|------------------|---------|
| A 커리큘럼 | `P21H_CURRICULUM_PHASE_STEPS` | corpus 난이도 phase 스케줄 | ✗ sampler 단일-mix only | wiring(env+cfg)만, **TODO[axis-impl]** |
| B distill | `P21H_DISTILL_TEACHER` | teacher KD | ✗ teacher 로딩 코드 없음 | wiring 만, **TODO[axis-impl]** |
| C head_g obj | `P21H_HEAD_G_OBJECTIVE` | head-G 보조 목적함수 | △ `head_g`/`logits_g` 존재, loss 미사용 | **WIRED** (lm CE aux) |
| C2 head_g en | `P21H_HEAD_G_ENABLE` | head-G aux 활성 | △ 동상 | **WIRED** |
| D freeze emb | `P21H_FREEZE_EMBED` | 입출력 임베딩 freeze | △ `tok_emb`(=head_a tie) 존재 | **WIRED** (`requires_grad_(False)`) |
| E lang bal | `P21H_LANG_BALANCED` | 언어-균형 샘플러 | ✗ per-lang balanced sampler 없음 | wiring 만, **TODO[axis-impl]** |
| F contrastive | `P21H_CONTRASTIVE_LANG` | 대조 언어 loss | ✗ contrastive loss 코드 없음 | wiring 만, **TODO[axis-impl]** |

honest scope: 7 중 **2개(head_g C/C2 · freeze_embed D)** 만 train-loop 경로 보유 →
실제 wired. 나머지 4개(A/B/E/F)는 ML feature 자체가 미구현 — wiring(parse+env+log)
만으로는 동작 불충분하므로 `TODO[axis-impl]` 유지.

## 3. 고친 내용 (최소 diff, 기존 파일 edit only)

### `train_p21h_v3.py`
1. **7 axis args default 를 `os.environ.get("P21H_*")` 로 read** — dispatcher 가
   `--flag` 를 떨어뜨려도 env-var 가 코드에 도달(silent-bypass 방어). env unset 시
   이전 상수 default → **무회귀**.
2. **7 axis 값을 `cfg` 에 thread** — 이전엔 parse+log 만, 이제 `run()` 에 도달.
3. **axis-D freeze_embed** — `cfg=1` 시 `model.tok_emb.weight.requires_grad_(False)`
   (tied → head_a 동시 freeze), optimizer trainable 분리 **전**에 적용. default 0 → 무회귀.
4. **axis-C/C2 head_g** — `head_g_enable=1` 또는 `head_g_objective∈{"",lm}` 시
   `logits_g` LM CE 를 `head_g_weight`(신규, default 0.1)로 가중해 `L_total` 에 가산.
   default `head_g_enable=0` → term skip → loss 동일(무회귀). mitosis aux 합산을
   `L_total = L_ce + ...` → `L_total = L_total + ...` 로 정정해 head_g term 과 합성.

### `dispatch_p21h_v3_runpod.sh`
- `P21H_HEAD_G_WEIGHT` env-var 정의 + `--head-g-weight $P21H_HEAD_G_WEIGHT` passthrough
  추가 (나머지 6 axis passthrough 는 PR #385 에서 land).

## 4. fix 후 grep-verify (after — F-H257-1 / F-H257-4 정적 증거)

```
$ grep -nE "os\.environ|getenv" train_p21h_v3.py
677: default=int(os.environ.get("P21H_CURRICULUM_PHASE_STEPS", "0") or 0),
680: default=os.environ.get("P21H_DISTILL_TEACHER", ""),
683: default=os.environ.get("P21H_HEAD_G_OBJECTIVE", ""),
686: default=int(os.environ.get("P21H_HEAD_G_ENABLE", "0") or 0),
689: default=float(os.environ.get("P21H_HEAD_G_WEIGHT", "0.1") or 0.1),
692: default=int(os.environ.get("P21H_FREEZE_EMBED", "0") or 0),
695: default=int(os.environ.get("P21H_LANG_BALANCED", "0") or 0),
698: default=float(os.environ.get("P21H_CONTRASTIVE_LANG", "0.0") or 0.0),
```

| 검증 | before | after |
|------|--------|-------|
| F-H257-1 (`os.environ` in train) | 0 lines | **8 lines** (7 axis + head_g_weight) |
| axis → cfg | 0 | **8** (`run()` 도달) |
| axis → train-loop (head_g/freeze) | 0 | **2** (head_g aux CE + freeze_embed) |
| `py_compile` / `bash -n` | — | **PASS** (둘 다 syntax valid) |

## 5. 무회귀 보증

- 모든 axis env-var unset → 이전 상수 default 그대로 → 동작/loss 불변.
- `freeze_embed=0` / `head_g_enable=0` (default) → freeze 미적용 + head_g term skip
  → loss·optimizer 동일.
- 변경은 신규 코드 경로의 **gate-off default** 추가뿐 — 기존 fire 결과 재현 가능.

## 6. 미구현 feature (honest scope)

A 커리큘럼 · B distill · E lang-balanced · F contrastive 4 axis 는 ML feature
미구현 상태로 wiring(env→cfg→log)만 land. 이 4 axis 의 진짜 ablation 은 각 feature
구현(curriculum sampler / KD teacher / balanced sampler / contrastive loss)이
선행되어야 하며, 본 PR 범위 밖이다. `train_p21h_v3.py` 의 `TODO[axis-impl]` 마커가
잔여 gate 를 표시한다.

## 7. 다음 step (이 PR 범위 밖)

- merge 후 head_g(C/C2) + freeze_embed(D) 2 axis 의 **진짜 ablation 재발사**
  (F-H257-4: wiring fix 후 axis 별 init_CE Δ ≥ 0.1 nats 변별 확인). ⚠ GPU 비용 발생 —
  별도 step.
- A/B/E/F 4 axis feature 구현은 별도 stacked PR.
