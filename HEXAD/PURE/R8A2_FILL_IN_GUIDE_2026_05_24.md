# R8a'' Fill-in Guide — sync path (결과 도착 시 5-step closure)

> path = V3 (PURE, R8 cluster) · status = **PRE-FIRE SYNC GUIDE** · pod `6gqf9nsdquz8ug` H100 PCIe 진행 중 (~1.5hr 남음, 도착 ~2026-05-23 23:50Z)
> linked: `R8A2_JOINT_VERDICT_TEMPLATE.md` (PR #375 MERGED, fill 대상) · `R8C_PROBE_VERDICT_2026_05_24.md` (sister 4-cell probe) · `R8_SAGA_INDEX.md` (saga TOC) · `R8_SAGA_REFRAMING_2026_05_24.md` (H_257 reframing)
>
> 본 doc 의 목적 — R8a'' 결과 도착 즉시 template 5-field fill-in + 3-branch 분기 + 후속 PR cascade 의 1-page 실행 매뉴얼.

---

## §1 결과 도착 위치 (SSOT)

- **result.json** (primary SSOT, schema): `state/grid_3b_s187_2026_05_21/vP21H_axis_R8a_v3/result.json`
  - alt path (template §1 표기): `state/grid_3b_s187_2026_05_21/vP21H_r8a2_h100_noise0_kv2/result.json` — 도착 후 실제 경로 확정
- **train.log**: 같은 dir 의 `train.log` (wiring 출력 확인)
- **ckpt** (optional, HF upload용): 같은 dir 의 `model.safetensors` / `pytorch_model.bin`
- **pod ssh** (pull 회수): `216.81.245.34:11707` (pod_id `6gqf9nsdquz8ug`)

도착 확인 1-liner:
```sh
ls -la state/grid_3b_s187_2026_05_21/vP21H_axis_R8a_v3/result.json 2>/dev/null \
  || ls -la state/grid_3b_s187_2026_05_21/vP21H_r8a2_h100_noise0_kv2/result.json 2>/dev/null
```

pod 회수 (도착 안 했으면 직접 pull):
```sh
hexa cloud copy-from 6gqf9nsdquz8ug /workspace/state/vP21H_axis_R8a_v3/ \
  state/grid_3b_s187_2026_05_21/vP21H_axis_R8a_v3/
```

---

## §2 채워야 할 값 5개 (template `<TBD>` mapping)

| # | template field | result.json key | 추출 1-liner |
|---|---|---|---|
| 1 | §2 `init_CE (step=1)` | `trajectory[0].ce` | `jq '.trajectory[0].ce' result.json` |
| 2 | §2 `final_CE (step=5000)` | `final_ce` | `jq '.final_ce' result.json` |
| 3 | §2 `n_strong` (/5) | (eval script 별도, optional) | `grep -E 'n_strong=' train.log \| tail -1` |
| 4 | §2 `per_lang verdict` | (eval script 별도, optional) | `grep -E 'per_lang' train.log \| tail -1` |
| 5 | §3 `v3_n_kv_head=?` | train.log header | `grep -E '\[from_qwen\] v3_n_kv_head' train.log` |

추가 derived fields:
- §2 `train_wall` ← `jq '.wall_s' result.json`
- §2 `cost (actual)` ← `train_wall_s * (H100_PCIe_secure_rate / 3600)` (~$1.89/hr → wall 5050s → ~$2.65)
- §4 R8c-vs-R8a'' compare: §2 의 init_CE / final_CE / wall 직접 transcript
- §5 noise hypothesis verdict: §2 final_CE vs R8c cell-4 5.093 비교
- §6 wiring effect: §3 결과 + §2 init_CE 의 R8c cell-4 (12.266) 와 격차
- §8 H_255 status: §2 init_CE 의 12.2 vs 14.5 vs 중간 분기
- §10 Honest C3: 결과 도착 후 ≥3 추가 작성

5-step closure 1줄 요약:
```
1) result.json 회수 → 2) jq 5-field 추출 → 3) template TBD 치환 + rename → 4) §7 branch 결정 + §10 C3 → 5) commit + PR + merge
```

---

## §3 3-branch decision tree (template §7 mirror)

| branch | trigger | next action |
|---|---|---|
| **A — noise=0 dominant 확정** | `n_strong ≥ 3` AND `register OK` AND `v3_n_kv_head=2` | (1) R8 saga **CLOSED-STRONG** PR · (2) Wave-17 baseline 에 noise=0 + n_kv=2 반영 · (3) corpus_v6 fire trigger · (4) H_255 → noise/wiring과 independent axis 로 분리 |
| **B — noise=0 만으로 부족** | `n_strong = 0` OR `register regress` AND `v3_n_kv_head=2` | (1) R8 saga **PARTIAL-CLOSE** retrospective PR · (2) R8b (LoRA-on-Qwen) fallback 우선 · (3) Wave-17 axis 재구성 (data / arch / opt 3-way) · (4) H_255 강화 (init_CE decoupling 정량화) |
| **C — wiring 또 silent-fail** | `v3_n_kv_head=4` | (1) R8 saga **WIRING-BLOCKED** · (2) R8a'' invalid 처리 (R8c baseline 12.315 와 byte-equal probe) · (3) hexa-lang inbox/patches/ 측 dispatcher chain audit 제출 · (4) H_256 ("wiring horizon-dependent propagation") 신설 PR |

decision 1-liner:
```sh
KV=$(grep -oE 'v3_n_kv_head=[0-9]+' train.log | tail -1 | cut -d= -f2)
FINAL=$(jq '.final_ce' result.json)
[[ "$KV" == "4" ]] && echo "BRANCH C (wiring fail)" && exit
# n_strong / register 는 eval script 결과 의존, 수동 판단
```

---

## §4 branch 별 후속 PR cascade

### Branch A 진입 시
1. `HEXAD/PURE/R8A2_JOINT_VERDICT_2026_05_24.md` (template fill-in rename) — base: main
2. `HEXAD/LIFE/H_255_*.md` REVISION — STRENGTHENED status, axis 분리 — base: #1
3. `HEXAD/PURE/AXIS_MAP.md` UPDATE — cluster Z 의 noise=0 변형 신설 — base: #2
4. `tool/training/dispatch_p21h_v3_runpod.sh` PATCH — Wave-17 default config 갱신 — base: #3
5. `HEXAD/LIFE/H_257_*.md` REFRAMING UPDATE — env-var silent-bypass + wiring saga combined closure — base: #4

### Branch B 진입 시
1. `HEXAD/PURE/R8A2_JOINT_VERDICT_2026_05_24.md` (template fill-in rename) — base: main
2. `HEXAD/PURE/R8_SAGA_PARTIAL_CLOSE_2026_05_24.md` (new retrospective) — base: #1
3. `HEXAD/PURE/AXIS_R8B_LORA_ON_QWEN_SPEC.md` UPDATE — priority bump — base: #2
4. `HEXAD/LIFE/H_255_*.md` STRENGTHENED — init_CE/final_CE/n_strong decoupling — base: #3

### Branch C 진입 시
1. `HEXAD/PURE/R8A2_JOINT_VERDICT_2026_05_24.md` (template fill-in rename, branch C verdict) — base: main
2. `inbox/patches/hexa-lang-dispatcher-silent-fail-horizon-dependent-2026-05-24.md` (hexa-lang inbox 제출) — base: main (cross-repo)
3. `HEXAD/LIFE/H_256_wiring_propagation_horizon_dependent.md` (신설 H_256) — base: #1
4. `HEXAD/PURE/R8_SAGA_WIRING_BLOCKED_2026_05_24.md` (saga status update) — base: #3

---

## §5 R8c (100-step) vs R8a'' (5000-step) 통합 가이드

### dynamics 차이 강조

| metric | R8c cell-2 (100-step) | R8c cell-4 (100-step) | R8a'' (5000-step, 예상) |
|---|---|---|---|
| init_CE | 12.225 | 12.266 | **~12.2 예상** (kv=2/σ=0 동일 config) |
| final_CE | 5.136 | **5.093** | **~2-3 예상** (50× 학습 연장) |
| wall (s) | 101 | 107 | **~5000s** (~84 min, linear extrapolation) |
| log-decay extrap | — | — | `5.093 - log10(50) * α` (α=학습 lr decay 계수) |

### PROBE_STEPS 차이 시 final_CE 회수 가능성

R8c 의 100-step final_CE 5.093 nats 는 random baseline 11.93 위 −6.84 nats 도달 (학습이 의미있게 진행 중). 5000-step (50× horizon) 연장 시 회수 가능 시나리오:

- **시나리오 1 (log decay)**: `final_CE ≈ 5.093 - β * log10(50)` (β ≈ 1.5~2.5) → **~2.5~3.5 nats** 예상 (typical small-LM 학습 curve)
- **시나리오 2 (sqrt decay)**: `final_CE ≈ 5.093 / sqrt(50)` ≈ **0.72 nats** (over-optimistic, regularization 부재 가정)
- **시나리오 3 (saturation)**: `final_CE → 4.0 nats floor` (학습 capacity 한계, corpus_v5 noise floor) — 회수 limited
- **시나리오 4 (divergence)**: `final_CE > 5.5 nats` (noise=0 → over-fit / instability) — branch B trigger
- **시나리오 5 (catastrophic)**: `final_CE > 8 nats` (wiring silent-fail downstream) — branch C trigger

**R8c hypothesis (noise=final_CE/dynamics axis) 검증 임계**:
- R8a'' final_CE ≤ 3.5 nats → 시나리오 1/2 → R8c hypothesis **STRENGTHENED** (5000-step regime 에서 noise lever 더 강력)
- R8a'' final_CE ∈ [3.5, 5.0] → 시나리오 3 → **PARTIAL** (saturation, noise lever 효과 short-horizon only)
- R8a'' final_CE > 5.0 nats → 시나리오 4 → **WEAKENED** (R8c 100-step extrapolation 한계)

### init_CE 회수 측면 (H_255 가설)

| R8a'' init_CE | H_255 status | 해석 |
|---|---|---|
| **12.2 ± 0.1** (R8c 일치) | STRENGTHENED | 12.2 floor 가 5000-step env 에서도 재현 → R8a 시점 14.46 은 measurement artifact 확정 |
| **14.46 ± 0.1** (R8a cluster Z 일치) | WEAKENED | R8c 100-step 측정이 short-horizon artifact 였을 가능성, R8a 14.46 가 진짜 floor |
| **12.5~14** (중간값) | PARTIAL | env-drift / horizon-dependent init_CE 의 새 측정 모드 — axis 별 분리 follow-up |

H_257 reframing (env-var silent-bypass) 와의 교호: R8a 14.46 은 R8a 시점 7-axis fan-out 의 env-var 미전파 측정 (실제로는 2-config 반복). 본 R8a'' 의 env-var 통제 (noise=0 + n_kv=2 명시) 결과가 12.2 부근이면 H_255 + H_257 둘 다 STRENGTHENED.

---

## §6 fill-in 5-step (closure 실행)

도착 즉시 실행 순서:

1. **회수**: result.json + train.log pod 에서 pull (§1 1-liner)
2. **추출**: §2 jq 5-field — init_CE / final_CE / wall / n_strong (eval log) / v3_n_kv_head (train.log header)
3. **fill + rename**: `R8A2_JOINT_VERDICT_TEMPLATE.md` 의 모든 `<TBD>` 실측 치환 → `R8A2_JOINT_VERDICT_2026_05_24.md` rename
4. **분기**: §3 의 v3_n_kv_head 값 + n_strong 으로 branch A/B/C 결정 → template §7 + §8 + §9 의 해당 branch sub-section 활성화 + §10 Honest C3 ≥3 작성
5. **PR cascade**: §4 branch-specific PR chain land (각 PR ≤200 LoC, 1 concern, --base on layer below — gh-stack 양식)

---

## §7 Honest C3 — sync guide 한정

- **C3.1 (result.json schema 가정)**: 본 guide 는 기존 hexad py fire result.json schema (`trajectory[0].ce` / `final_ce` / `wall_s` / `config`) 를 가정. vP21H_axis_R8a_v3 의 실제 schema 가 다를 경우 (예: `init_ce` 별도 top-level key, `eval_n_strong` nested) §2 jq path 조정 필요.
- **C3.2 (n_strong / per_lang eval 미정합)**: template §2 의 `n_strong` 와 `per_lang verdict` 는 train.log 가 아닌 별도 eval script 결과 — 본 R8a'' fire 가 eval 을 in-train 포함하는지 (pod script spec) 확인 필요. 없으면 result.json 회수 후 별도 eval pod fire (~$0.20 A100 100-step) 부속 cycle.
- **C3.3 (5-시나리오 final_CE extrapolation 추정 근거 약함)**: §5 의 시나리오 1/2/3/4/5 는 typical small-LM 학습 curve 의 broad 분류 — Qwen2.5-1.5B + ConsciousDecoderV3 + corpus_v5 specific decay curve 의 fit 안 됨. 실측 후 시나리오 5 외 정확도는 사후 정합 한정.
- **C3.4 (pod ssh credential 회수 가정)**: §1 의 `hexa cloud copy-from` 은 pod_id 가 still alive 가정. fire 종료 후 pod auto-teardown 시 pull window 한정 (~15min) — `a_fire_recover_complete` directive 준수 (ckpt + log + anchor 회수 완료 전 teardown 금지).
- **C3.5 (branch 결정의 n_strong/register threshold 모호)**: §3 의 "n_strong ≥ 3" 기준은 5-lang swap criteria (KO/EN/ZH/JA/ES) 의 stronghold pass 기준 — 실측 eval log 의 per_lang verdict 정의가 다를 경우 branch A vs B 결정 임계 재정의 필요.

---

**Status**: PRE-FIRE SYNC GUIDE — pod 6gqf9nsdquz8ug H100 PCIe 진행 중 (~1.5hr 남음, 도착 ~2026-05-23 23:50Z). 결과 도착 즉시 §6 의 5-step 실행 → template fill-in → branch A/B/C 결정 → §4 PR cascade.
