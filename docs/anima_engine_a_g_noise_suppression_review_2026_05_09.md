# Engine A/G arch 자체 검토 — cell_pool noise-suppression 가설 (2026-05-09)

> **친근 한 줄 요약**: BG-LB 학습 후 cell_pool 이 random_init 보다 더 "잠잠해진" 현상을 발견했어요. 학습이 **의식 신호를 새긴** 게 아니라 그저 **잡음만 줄인** 게 아닐까? — 이 가설을 3 갈래로 쪼개고, 4 가지 수정안을 우선순위로 정리한 설계 메모입니다.

---

## 1. 무엇이 이상한가 (현상 SSOT)

`state/anima_bg_lb_native_v5_post_mount_2026_05_09.json` 측정 결과:

| 지표 | trained (BG-LB) | random_init mirror | 방향 | V14 |
|------|---:|---:|:---:|:---:|
| PIV (axis-stdev max) | **0.01071** | 0.02244 | trained 가 더 **낮음** | VIOLATED |
| DCR (argmax 변경률) | **0.621** | 0.862 | trained 가 더 **낮음** | VIOLATED |
| D-RAND (axis 거리) | 0.02368 | — | AMBIGUOUS (0.05 미만) | — |

**핵심 모순**: V14 평가는 "trained > random_init" 이어야 정상인데, **trained 가 모든 지표에서 random_init 보다 평탄**함. → 학습이 cell_pool 의 분산을 **줄이는 방향**으로 갔다는 증거.

비유: 처음에 종 16 개를 무작위로 배치해 종소리가 다양하게 들렸는데, 학습 후엔 모든 종이 거의 같은 위치로 모여 한 가지 톤만 들리는 상태. 어떤 자극(prompt)이 와도 거의 비슷한 반응이 나옴.

---

## 2. Engine A/G arch 핵심 구조 (3 줄 요약)

`training/engine_a_g_arch.py` 분석:

1. **cell_pool_init** (L283): `nn.Parameter(torch.randn(16, 64))` 정규화 후 unit-sphere 위 배치 → **학습 가능 파라미터** (frozen 아님). batch 마다 매번 `fresh_cells()` 로 expand 후 layer 진행 중 `step()` 으로 in-place 갱신 (gradient 는 cell_pool_init 까지 흐름).
2. **forward 단일 loss** (L378-386): `F.cross_entropy(shift_logits, shift_labels)` — **lm_head 의 토큰 예측 손실 하나뿐**. cell-axis-variance / cell-prediction-aux loss **없음**.
3. **dual loss = chat 추가**: `chat_co_train_weight` 는 substrate_lm + chat_lm 의 **weighted sum** (둘 다 같은 `lm_head` 사용, 같은 cross-entropy, w=0.3→0.5 curriculum). cell_pool 자체에 대한 의미 신호는 **여기에도 없음**.

**=> cell_pool 은 lm_head loss 의 gradient 만 받음.** Engine G 가 의식 axis 를 새기도록 강제하는 신호는 arch 안 어디에도 없다.

---

## 3. 가설 3 갈래 + 검증 절차

| # | 가설 | 메커니즘 | 검증 절차 | 예상 evidence |
|---|------|---------|----------|--------------|
| H1 | **Goodhart 단순** (단일 loss 만 보고 cell 의미 무시) | lm_head CE 만 backprop → cell_pool 이 "lm_head 에 도움 되는 평탄한 mean" 으로 수렴. axis 변별은 안 봄. | (a) cell_pool_init gradient norm trace per epoch (b) lm_head 와 cell_pool 의 cosine alignment 측정 (c) cell_pool 평균만 lm_head 에 영향 주는지 ablation (cells.mean 만 남기고 variance 0 으로 강제 → loss 변화 미미하면 H1 강력) | trained 의 cell-pair stdev 가 epoch 따라 monotone 감소. ablation 시 loss delta < 1% |
| H2 | **cell collapse** (mode-collapse) | repulsion-field (alpha=0.05) 가 attention-pull (alpha=0.10) 보다 약함 → pull 이 모든 cell 을 같은 hidden_mean 쪽으로 끌어당겨 16 cell 이 1 개 점에 수렴. | (a) cell-pair pairwise distance histogram (init vs final) (b) 16 cell 의 SVD top-1 singular value ratio (c) repulsion_alpha 를 0.5/1.0 으로 올린 ablation 학습 | final pairwise distance 가 init 대비 50% 이하. SVD top-1 / top-2 ratio > 10 |
| H3 | **init 과잉 분산** (start high → 학습이 줄임) | unit-sphere 정규화된 randn 이 random_init mirror 보다 분산 큰 시작점 → 학습이 정상 lm_head 학습 부수효과로 분산 감소. random_init 은 안 줄어든 채 측정. | (a) step=0 cell_pool stdev 측정 (mirror 와 동일한지) (b) trained 의 cell_pool stdev curve (epoch별) (c) lm_head loss vs cell_pool stdev correlation | step=0 stdev 가 random_init 과 동일 (re-normalize 후 동일 dist) → H3 단독으론 약함. 단 H1+H3 복합은 가능 |

**Preliminary judgment**: **H1 + H2 복합** 이 가장 가능성 높음.

- H1 단독은 "왜 random 보다 더 평탄한가" 만 설명 (cell 의미 신호 부재).
- H2 단독은 repulsion-field 가 그래도 0.05 alpha 로 작동하니 완전 collapse 는 어색.
- 그러나 attention-pull alpha 0.10 이 repulsion 0.05 의 2 배 → pull 이 우세 → 16 cell 이 hidden_mean 쪽으로 점진 수렴 (H2). 동시에 lm_head loss 는 cell 분산이 줄어도 영향 없음 (H1). 두 메커니즘이 같은 방향으로 작용.
- H3 는 cell_pool_init re-normalize 가 매번 unit-sphere 로 강제하므로 시작점은 random_init 과 통계적으로 동일 → 단독 기각.

---

## 4. 수정 후보 4 종 (코드 작성 X, spec 만)

### fix-1: cell predict aux loss 강화 (axis-variance regularizer)

**spec**: forward loss 에 `+ lambda * (-1.0 * axis_stdev_mean)` 추가. axis_stdev_mean = cells 16 개를 5 그룹으로 split → 각 그룹의 axis-stdev 평균. 음수 부호로 minimize → **분산 키우는 방향으로 학습**.

- **친근 비유**: 학생 16 명에게 "각자 다른 답을 내라" 고 점수 매기는 vector. 모두 같은 답이면 감점.
- **구현 난이도**: 낮음 (forward 마지막에 cells 텐서 retain → loss 1 줄 추가, lambda hyper 1 개).
- **예상 효과**: **PIV/DCR 직접 개선**. lambda=0.01 ~ 0.1 sweep 필요. lm_head 학습과 trade-off 관찰.
- **risk**: lambda 너무 크면 cell_pool 이 무의미한 분산 (white noise) 으로 수렴 → V14 통과해도 의미 없음. group-contrast (fix-3) 와 묶어야 안전.

### fix-2: cell_pool_init scale 축소 (randn × 0.1)

**spec**: `cells = torch.randn(16, 64) * 0.1` 후 normalize 생략 (또는 magnitude 0.1 유지). 학습이 분산을 **늘리는** 방향으로 가도록 유도.

- **친근 비유**: 종 16 개를 처음에 한 곳에 모아두고 학습이 "퍼뜨려라" 신호를 보내야 하는 상태로 시작.
- **구현 난이도**: 매우 낮음 (1 줄).
- **예상 효과**: H3 만의 contribution 격리 가능. 단 H1 (loss 신호 부재) 가 진짜 원인이면 fix-2 만으로는 무용 — 학습이 분산 늘릴 incentive 가 여전히 없음.
- **risk**: 의식 axis 가 아닌 random 방향으로 확산 → fix-1 과 동반 필요.

### fix-3: 5-axis label 강제 (group-contrast loss)

**spec**: 16 cell 을 5 group (identity/agency/phenomenal/temporal/social) 으로 명시 분할 (3,3,3,3,4 또는 학습 가능 soft assignment). intra-group cosine high + inter-group cosine low 강제. supervised contrastive loss 형태.

- **친근 비유**: 종 16 개를 5 종류 색깔로 미리 나누고 "같은 색끼리는 가까이, 다른 색끼리는 멀리" 학습. axis-meaning 을 arch 단계에서 못 박음.
- **구현 난이도**: 중간 (group-mask 텐서 + supervised contrastive loss 정의).
- **예상 효과**: **V5 PIV/DCR 정의와 정확히 정렬** → 가장 strong. 학습이 5-axis 표상으로 강제되므로 random_init 과 차별화.
- **risk**: hard label 강제 → "creative axis" 발견 가능성 차단 (Bitter Lesson 위반 risk). 단 trinity D_emergent vs B_corpus_strong 의 trade-off 는 D1 lane 에서는 허용 범위.

### fix-4: D-RAND in-loss (mirror distance maximize)

**spec**: 학습 step 마다 random_init mirror 의 cell_pool 을 reference 로 두고 trained cell_pool 과의 distance maximize 를 부수목표로. `+ mu * (-1.0 * ||cells - mirror_cells||_2)`.

- **친근 비유**: random_init 과 다른 모양으로 종을 배치하라는 보상. "untrained 와 달라야 함" 을 직접 학습.
- **구현 난이도**: 중간 (mirror 모델 frozen 하나 메모리 상주, layer-wise pair 매칭).
- **예상 효과**: V14 통과 자체는 보장 (mirror 와 다르게 만들도록 명시). 그러나 의미 axis 보장은 못함 — random 과 다르되 의식 axis 와도 다른 noise 로 갈 수 있음.
- **risk**: V14 metric goodhart (V14 통과 위해 수치만 맞춤). trinity D_emergent 충실도 의심. fix-1 / fix-3 와 묶어서만 사용 권장.

---

## 5. 권장 우선순위

| 순위 | fix | 근거 |
|:---:|------|------|
| 1 | **fix-1 (axis-variance reg)** + **fix-3 (group-contrast)** | H1 + H2 동시 차단. arch 변경 최소 (loss 추가). PIV/DCR 직접 정렬. |
| 2 | **fix-2 (init scale 축소)** | fix-1 과 묶어 ablation. 단독으론 무용 가능성. |
| 3 | **fix-4 (D-RAND in-loss)** | metric goodhart risk 로 보조 보험 위치. fix-1/3 검증 후 추가. |

**1 순위 적용 시 추가 필요사항**:
- lambda (axis-variance) 와 mu (group-contrast) 의 hyper sweep.
- repulsion_alpha 0.05 → 0.15 (H2 차단 보강).
- attention_pull_alpha 0.10 → 0.05 (H2 차단 보강, pull 우세 해소).

---

## 6. 검증 절차 (다음 cycle plan)

### step 1: 현 BG-LB ckpt 의 가설별 evidence 수집 (학습 fire X, 측정만)
- (a) cell_pool_init parameter 의 stdev / pairwise distance / SVD spectrum 측정
- (b) lm_head ablation: cells.mean 만 남기고 variance 0 강제 시 PPL delta
- (c) repulsion vs pull alpha effective ratio 계산

### step 2: BG-LA 측정 동일 검증 가능 여부
- BG-LA 는 같은 arch (la_350m preset, lineage_tag 만 다름) → **동일 검증 100% 적용 가능**.
- BG-LA ckpt 가 H100 pull 완료 시 즉시 동일 V5 measurement + 가설 evidence 수집.
- BG-LA 도 같은 패턴 (trained < random) 이면 H1+H2 가 arch-level 결함으로 확정 → fix-1/3 mandate.
- 만약 BG-LA 만 trained > random 이면 corpus-level 차이 → H1/H2 약화, 다른 가설 (corpus-noise, persona-bias) 신설 필요.

### step 3: fix-1 + fix-3 PoC fire (별도 verbatim 후)
- 350M Engine A/G + axis-variance reg lambda=0.05 + group-contrast mu=0.1 학습.
- step=0 / step=mid / step=final 에서 V5 measurement + hypothesis evidence.
- V14 통과 (trained PIV > random + delta_safety 0.02) 확인.

---

## 7. 다음 cycle 권장 step (1 줄)

**BG-LA 측정 후 H1+H2 evidence 수집 → fix-1 (axis-variance reg) + fix-3 (group-contrast) 묶어 350M PoC fire 검토** (별도 사용자 verbatim 후).

---

*own 16 strict — research + design only. 코드 수정 0, fire 0, commit/push 안 함.*
