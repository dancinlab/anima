# anima fix-5 PoC 설계 — Engine A/G unit-sphere normalize 제거/약화

**작성일**: 2026-05-09
**작성 모드**: design-only (코드 수정 / 학습 fire 없음)
**전제 인증**: 사용자 verbatim 2026-05-09 "지금 가능한것들 all bg go"
**친근 모드**: strict (한국어 우선, 비유 적극)

---

## 0. 한 줄 요약

> **"학생 노트에 늘 정해진 칸 안에서만 쓰게 하던 룰을 풀어주기"** —
> Engine G 의 cell_pool 이 매 4 layer 마다 단위구(unit sphere)로 강제 정규화되는 탓에
> 학습이 들어가도 의미 있는 변화가 쌓이지 못함. 이 정규화를 제거하거나 약화시켜
> cell 이 "자유롭게 멀어지고 가까워지는" 공간을 회복시키는 PoC 설계.

---

## 1. 배경 (왜 fix-5 가 필요한가)

### 1.1 Foreground v5 measurement 결과 (2026-05-09 직전)

| 모델 | C3 verdict | PIV (피벗) | DCR | cell_pool axis_stdev |
|---|---|---|---|---|
| BG-LB native v5 | `C3_FAIL_V14_VIOLATED_V5` | 0.0107 | 0.621 | random_init 과 거의 동일 |
| Phase 2 cotrain native v5 | `C3_FAIL_V14_VIOLATED_V5` | 0.0051 | 0.241 (BG-LB 보다 더 나쁨) | random_init 과 거의 동일 (델타 ~0.0001) |

### 1.2 두 가설

- **H4 정량 확정** — unit-sphere normalize 가 학습 효과를 사실상 무력화함.
  - 근거: trained cell_pool 이 random_init unit-sphere 와 통계적으로 거의 구분 안 됨 (델타 ~0.0001).
- **H5 신가설** — chat-template dual loss 가 forward pass collapse 를 더 증폭.
  - 근거: Phase 2 가 BG-LB 보다 나쁜 PIV/DCR. (별도 검증 필요 — 본 spec 범위 밖)

### 1.3 친근 비유

> 학생들에게 매 시험마다 "답안지를 펴고 글자 크기를 0.5cm 로 다시 맞춰라" 라고 하면,
> 학생이 큰 글씨로 강조하고 싶었던 부분도 다 1cm 줄로 깎여 사라짐.
> Engine G 의 unit-sphere 도 똑같음: cell 이 "이번 학습에서 이 방향이 중요해!" 하고
> 길게 뻗어가도, 4 layer 마다 ||cell||=1 로 잘라버려서 "방향" 만 남고 "크기" 가 사라짐.

---

## 2. engine_a_g_arch.py normalize step 분석

### 2.1 정확한 위치 + 빈도

| 위치 | 라인 | 종류 | 빈도 | 영향 범위 |
|---|---|---|---|---|
| `EngineG.__init__` | L281-282 | 초기화 정규화 | 1회 (build time) | `cell_pool_init` parameter 의 초기값 |
| `EngineG.step` | **L307** | **forward pass 매 step 정규화** | **layer 4/8/12/16/20 — 한 forward 당 5회** (`g_refresh_every=4`, `n_layers=24`, 마지막은 skip) | 활성 cells tensor (autograd 통해 cell_pool_init grad 로 역전파) |

```python
# L306-307 (engine_a_g_arch.py)
new_cells = cells + self.repulsion_alpha * push + self.attn_pull_alpha * pull
# Re-normalize cell magnitudes (stability)
new_cells = new_cells / new_cells.norm(dim=-1, keepdim=True).clamp(min=self.eps)
```

### 2.2 grad 흐름

- `nn.Parameter` 인 `cell_pool_init` (L283) 는 매번 `fresh_cells` (L292-293) 로 batch 차원 expand 만 됨 — autograd 그대로 통과.
- L307 의 normalize 는 **straight-through estimator 가 아님** — 일반 PyTorch 연산으로 그대로 backprop.
- 결과: 5회 연속 normalize 가 grad 의 radial component (||cell|| 방향 변화) 를 매번 거의 0 으로 깎음. 학습 signal 의 "크기 정보" 가 사실상 사라짐.

### 2.3 친근 설명

> 노래방에서 마이크 볼륨을 매 4초마다 자동으로 5 로 리셋하면,
> 가수가 "여기는 크게!" 하고 8 까지 올려도 곧바로 5 로 깎여서
> 무대 마이크 엔지니어가 "어, 가수가 크게 부르고 싶은 부분이 어디지?" 를 영영 못 배움.

---

## 3. fix-5 후보 4종 비교

### 3.1 비교 표

| 후보 | 핵심 변경 | 구현 난이도 | 예상 효과 | 위험 | 호환성 |
|---|---|---|---|---|---|
| **fix-5a** | normalize 완전 제거 | 매우 쉬움 (1줄 삭제) | 매우 큼 — cell norm 자유 | norm 폭발 / NaN — weight decay 필수 | 기존 ckpt 와 forward 동일 동작 (norm 차이만) |
| **fix-5b** | normalize 빈도 축소 (K=10/100/1000 step 마다 1회) | 쉬움 (state counter 추가) | 중간 — trade-off 조절 | K 너무 크면 fix-5a 와 비슷, 너무 작으면 효과 없음 | 동일 |
| **fix-5c** | `--normalize-cell-pool` flag (default false) | 쉬움 (cfg field + if) | fix-5a 와 동일 (default false 시) | 동일 | **최상** — flag default true 로 두면 기존과 100% 동일 |
| **fix-5d** | soft-normalize (loss 에 (||cell||-1)² penalty) | 중간 (loss 추가, weight 튜닝) | 중간-큼 — 부드러운 제약 | penalty weight 튜닝 필요, loss landscape 복잡화 | 동일 |

### 3.2 권장 우선 순서 — **fix-5c → fix-5a → fix-5d → fix-5b**

1. **1순위: fix-5c (flag 화)** — 가장 안전. default false 로 PoC 돌리고, 결과 좋으면 default 변경. 기존 학습 / V14 mirror / ckpt 와 완전 호환.
2. **2순위: fix-5a (완전 제거)** — fix-5c 가 PoC 통과하면 코드 정리 차원에서 normalize 자체 제거. weight decay 0.01-0.1 추가 필수.
3. **3순위: fix-5d (soft penalty)** — fix-5a 가 norm 폭발 보이면 fallback. penalty weight λ=0.001-0.01 부터.
4. **4순위: fix-5b (빈도 축소)** — 다른 모든 방법이 실패하면. K 가 추가 hyperparameter — 검증 부담 큼.

### 3.3 친근 비유 (왜 fix-5c 가 1순위인가)

> 마이크 볼륨 자동 리셋 기능을 **삭제** 하기 전에,
> 일단 **on/off 스위치** 부터 달자. 스위치 끈 채로 한 곡 (PoC) 불러보고,
> 음질이 좋아지면 (cell axis_stdev 가 random 보다 의미 있게 증가) 그 때 기능을 정식 제거.

---

## 4. fix-5c 구체 구현 spec (1순위 — 코드는 작성하지 않음, 변경 지점만 명시)

### 4.1 변경 지점

| 파일 | 라인 | 변경 |
|---|---|---|
| `training/engine_a_g_arch.py` | L103-114 (EngineAGConfig) | `normalize_cell_pool: bool = True` (기본값 True — 기존 동작 보존) 추가 |
| `training/engine_a_g_arch.py` | L276-290 (EngineG.__init__) | `self.normalize_cell_pool = cfg.normalize_cell_pool` 저장 |
| `training/engine_a_g_arch.py` | L295-308 (EngineG.step) | L307 을 `if self.normalize_cell_pool:` block 으로 감싸기 |
| (PoC config 신설) | — | `EngineAGConfig.la_350m_fix5c_poc()` classmethod 추가 — `normalize_cell_pool=False`, `weight_decay=0.05` (옵티마이저 측) |

### 4.2 V14 mirror 호환

- `load_random_init(seed=42, preset="la_350m_fix5c_poc")` 새 preset 추가 — fix-5c 도 random_init mirror 가능.
- `EngineAGConfig.__dict__` 에 `normalize_cell_pool` 자동 포함 → `save_checkpoint` / `load_checkpoint` 자동 round-trip.

### 4.3 weight decay

- AdamW optimizer 측에서 `weight_decay=0.05` (cell_pool_init parameter group 별도 설정).
- norm 폭발 방지 + 정규화 제거 보상.

---

## 5. PoC 학습 plan

### 5.1 학습 step 추정

| 항목 | 값 | 근거 |
|---|---|---|
| 모델 크기 | 350M (BG-LA scratch) | 기존 BG-LA 와 동일 — 비교 가능성 보존 |
| step 수 | **1500 step** (1000 최소 / 2000 안전) | 350M scratch 에서 cell_pool 변화 가시화 최소 step |
| batch size | 4 (H100 80GB) | 기존 BG-LB 동일 |
| context | 1024 | EngineAGConfig 기본 |
| GPU | H100 PCIe 1대 | own 28 H100 pod orchestrator |
| 학습 시간 | 약 30-60분 | 350M / 1500 step 기준 |
| **cost** | **$5-15** ($0.30-0.50/h × 0.5-1h × 1 GPU) | runpod 기준 |

### 5.2 corpus

- BG-LA 와 **동일 corpus** (persona corpus). corpus 변수 통제로 normalize 제거 효과만 분리 측정.

### 5.3 학습 trigger 시점

- **본 spec 통과 후 사용자 verbatim 별도 인증 필요** — design-only 단계에서는 fire 금지.

---

## 6. 검증 metric — fix 가 작동하는지 어떻게 보는가

### 6.1 핵심 metric — `cell_pool axis_stdev_mean`

- 측정 대상: 학습 후 `model.engine_g.cell_pool_init.detach()` (16 cells × 64 dim).
- 계산: `axis_stdev = cells.std(dim=0)` → `axis_stdev_mean = axis_stdev.mean().item()`.
- 의미: cell 들이 64차원 공간에서 얼마나 다양한 방향으로 퍼져있는가. 학습이 의미 있게 들어갔다면 random_init 보다 큼.

### 6.2 V14 in-metric 비교

| 비교 | 측정 | 통과 기준 |
|---|---|---|
| baseline | `load_random_init(seed=42, preset="la_350m_fix5c_poc")` 의 `axis_stdev_mean` | 참조값 (변동 없음) |
| trained | PoC 학습 후 ckpt 의 `axis_stdev_mean` | **trained > baseline + δ_safety (0.02)** |
| sanity | normalize 켠 동일 PoC (fix-5c default true) | trained ≈ random (재현되어야 함 — H4 재확인) |

### 6.3 통과 기준 명시

- **PoC PASS**: `axis_stdev_mean(trained_no_norm) − axis_stdev_mean(random_no_norm) ≥ 0.02` (δ_safety).
- **PoC FAIL**: 위 차이 < 0.02 → fix-5a/d 로 escalation 또는 H5 (chat-template dual loss) 추가 조사.
- **NaN / norm 폭발 시**: weight decay 를 0.05 → 0.1 로 증가. 그래도 폭발 시 fix-5d (soft penalty) 로 전환.

### 6.4 추가 보조 metric

- `cell_pool norm distribution` — 평균 / std / max. norm 폭발 조기 탐지.
- `PIV / DCR` — full v5 strict (학습 후, foreground measurement). 단 **PoC 1차 게이트는 axis_stdev** 만 (PIV 는 비싼 측정이라 PASS 후 진행).

---

## 7. 친근 한 줄 요약

> **"마이크 볼륨 자동 리셋 스위치를 끄고 한 곡 불러본다 — 그 다음에 기계 자체에서 빼든 말든 결정한다."**

---

## 8. 후속 단계 (PoC 통과 가정)

1. fix-5c flag default false 로 변경 (코드 정리).
2. fix-5a (완전 제거) 결정 — fix-5c 와 동일 결과면 normalize 코드 자체 제거.
3. BG-LA / BG-LB 재학습 (full corpus, 6000+ step) — full PIV/DCR 측정.
4. H5 (chat-template dual loss) 별도 조사 — Phase 2 가 BG-LB 보다 나쁜 원인 분리 측정.
5. 통과 시 own 38 yaml SSOT registry 갱신 + render 자동 재생성.

---

## 9. own 16 strict 준수 확인

- [x] 본 doc 만 작성 — 코드 수정 없음
- [x] 학습 fire 없음 — design-only
- [x] grep / Read / Write 만 사용 — 모델 로드 없음
- [x] resource 영향 zero — Mac load avg / RAM 추가 부담 없음

---

## 부록 A. fix-5 후보별 한 줄 비유

| 후보 | 비유 |
|---|---|
| fix-5a | "마이크 자동 리셋 기능을 아예 빼버린다 (단, 가수가 너무 크게 부르면 마이크 터질 수 있으니 PA 시스템에 limiter 가 필요)" |
| fix-5b | "자동 리셋을 4초 → 40초 / 6분 / 60분 마다로 늘린다" |
| fix-5c | "자동 리셋 on/off 스위치를 단다 (default on — 기존 그대로)" |
| fix-5d | "리셋 대신, 볼륨이 5에서 너무 멀어지면 작은 벌금만 매긴다 (soft penalty)" |
