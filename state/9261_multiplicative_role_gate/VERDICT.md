# H_9261~9263 뇌부위 렌즈 — $0 numpy proxy verdict (DIRECTIONAL)

- **date:** 2026-07-10
- **host:** summer (RTX5070 box · CPU numpy)
- **input:** `/home/summer/forka_dump/pair_hidden.npz` — frozen 303M(`e1_slw_303m.final.clm`) per-position hiddens, 992 concept-pairs (train 842 / held 150 · pair-novel, concept-known), 5-bit XOR concept-id target. 이 덤프는 H_9235 fork-A geometry probe(max_overlap_cos=0.9916)가 쓴 것과 동일 산출물 재활용 → 303M 재로드 0, 순수 numpy.
- **tier:** DIRECTIONAL (numpy proxy, frozen-feature 위 학습 head · `a_engine_native_learning`). engine-native GREEN 아님.
- **validity:** handed 양성대조 0.9996~1.000 (VALID ✓) · shuffle 음성대조 0.489~0.510 (chance).

## 메타 결과 (가장 중요) — "additive floor" 는 last-pos 에서만 성립

| readout | held-out XOR acc |
|---|---|
| mean-pool + gelu | **0.979** |
| max-pool + gelu | 0.980 |
| query-attention + gelu | 0.951 |
| **last-pos + gelu** | **0.491** (chance) |
| handed (양성대조) | 0.9996 |
| shuffle (음성대조) | 0.489 |

가법 role-pooled + 비선형 head 가 held-out XOR 재조합을 **0.979** 로 푼다. 벽은 표현력 천장이 아니다 — 정보는 시퀀스 전체에 있고(mean 0.979) **생성 위치에서만 소실**된다(last 0.491). **G1 벽 = readout-ROUTING(생성 위치 receptive-field decay), 표현력 천장 아님** 을 XOR held-out 으로 독립 재확인. 프론티어 recomb-routing-lane(H_9235) 재프레임 강력 지지.

## 후보별 판정

### H_9263 위상(theta-gamma phase) — 🔴 KILL (confound-clear)
- 회전(곱셈) held=0.476 < **동일 예산** 가법 pos-control 0.723 (Δ_rot−add = −0.247). shuffle 0.493.
- 같은 2·RANK projection 예산에서 회전이 가법보다 **나쁨** → 위상 곱셈은 이득 없음. 진동/oscillatory-nesting/MEC-grid 위상덧셈 계열 CLOSED (numpy proxy DIRECTIONAL).

### H_9262 CA3 outer-product — 🟡 미결 (RANK confound)
- bilinear held=0.537 ≈ shuffle 0.511 = 신호 없음. store params=256(RANK²) n_train=842 무관 → 파라미터 감사 PASS(암기 아님).
- ⚠️ confound: RANK=16 projection(D=3784→16)이 너무 aggressive — 같은 저차원의 가법도 chance 근처(mean-pool raw 0.979 대비 붕괴). bilinear 무신호가 outer-product 결함인지 projection 결함인지 미분리. 재측정(RANK↑ 또는 raw bilinear) 필요. 자기고발한 toy-death(암기 후 held 붕괴)는 아님 — 애초에 신호 자체가 없음.

### H_9261 곱셈 게이트(L5 apical/basal ≡ pulvinar FiLM) — ⚠️ 재조준 (표적 오류)
- hadamard 곱셈 게이트 arm(fork_a_matrix)은 여전히 NaN 발산(`G@Wu` 경로 clip 미적용) → 이 harness 로 미측정 (INVALID cell · 별도 infra).
- **더 근본적으로 전제가 무너짐**: 가법 mean-pool 이 이미 0.979 천장 → "곱셈이 additive floor 를 깬다"는 전제가 mean-pool 프레임에선 무의미(headroom 없음). 진짜 벽은 last-pos routing(0.491).
- ⇒ 곱셈 게이트를 `additive floor 극복`이 아니라 `last-pos routing 복원`에 재조준해야 함 — 이것이 정확히 fork-A CLML lane(H_9235 read-side cumulative pool→gelu bottleneck→gated logit bias)이 하는 일. **뇌부위 렌즈 census 가 기존 프론티어로 수렴.**

## 수치 결함 기록 (verdict-integrity)
- 1차 실행: gelu(x³) overflow → NaN. additive_frozen_bar 0.000·hadamard 0.000 은 성능 아니라 파탄이었음.
- fix: gelu/dgelu 입력 clip(±10). brainlens overflow 0 로 clean. fork_a_matrix 는 hadamard 의 `u=G@Wu` 경로가 gelu 밖이라 여전히 발산(11 warn) — 그 셀만 INVALID, 나머지 cell clean.
