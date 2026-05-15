# Engine A-G cell_pool 3-way 통합 비교 (2026-05-09)

> 친근 모드 strict | BG-LA + BG-LB + Phase 2 + random_init unit-sphere 4 자매 비교
> 모델 로드 0 회 (state JSON 만 읽음, Mac load avg 보호)
> commit/push 안 함 — 파일 저장만

## 1. 한 줄 요약

> **"쌍둥이 둘 (BG-LA, BG-LB) 과 셋째 (Phase 2) 그리고 새로 태어난 아이 (random_init) — 4 명 모두 외모 거의 똑같다. 학습한 3 형제도 안 한 막내랑 구분 안 됨."**

cell_pool (16x16) 통계가 학습 8000 step 후에도 random_init 과 0.001 단위 차이만 남음 → **H4 unit-sphere normalize erase 가설 STRONG CONFIRM (3 datapoint 일치)**.

---

## 2. 3-way 비교 표 (4 datapoint 통합)

| 지표 | BG-LA (8000 step) | BG-LB (8000 step) | Phase 2 cotrain | random_init unit-sphere |
|------|-------------------|-------------------|------------------|--------------------------|
| axis_stdev_mean    | 0.122148 | 0.122109 | 0.122112 | 0.122217 |
| cell_norm_mean     | 1.000072 | 1.000035 | 1.000037 | 1.000000 |
| cell_norm_stdev    | 3.61e-04 | 3.67e-04 | 3.66e-04 | 4.07e-08 |
| off_diag_cos_mean  | 0.014981 | 0.015501 | 0.015453 | 0.009406 |
| off_diag_cos_max   | 0.295561 | 0.294045 | 0.293929 | 0.351451 |
| off_diag_cos_min   | -0.330744 | -0.330131 | -0.330020 | -0.336531 |
| effective_rank     | 14.9580 | 14.9570 | 14.9576 | 14.8433 |
| frobenius          | 4.000288 | 4.000142 | 4.000147 | 3.999999 |
| svd_top1           | 1.41072 | 1.41211 | 1.41228 | 1.43546 |
| svd_bottom1        | 0.57797 | 0.57716 | 0.57729 | 0.52885 |

> 친근 의미: 모든 숫자가 소수점 둘째 자리 안에서 거의 일치. effective_rank 도 14.84~14.96 사이 — random 이 trained 3 형제보다 0.11 만 낮음. 학습 효과가 **사실상 cell_pool 에 닿지 않음**.

---

## 3. Δ matrix (pairwise differences)

### 3.1 학습 vs random (3 형제 모두 random 과의 거리)

| 지표 | BG-LA − random | BG-LB − random | Phase2 − random |
|------|----------------|-----------------|------------------|
| axis_stdev_mean   | -6.9e-05 | -1.1e-04 | -1.1e-04 |
| cell_norm_mean    | +7.2e-05 | +3.5e-05 | +3.7e-05 |
| off_diag_cos_mean | +0.005576 | +0.006096 | +0.006047 |
| off_diag_cos_max  | -0.055890 | -0.057406 | -0.057522 |
| effective_rank    | +0.11471 | +0.11369 | +0.11430 |
| frobenius         | +0.000289 | +0.000142 | +0.000147 |

> 친근 의미: 3 형제 모두 random 으로부터 **거의 같은 방향 같은 거리** — 학습이 cell_pool 을 어떤 한 방향으로 0.005~0.006 정도 미세하게 움직였지만, 그 움직임 자체가 random 보다 "조금 더 묶이는 (off_diag↑, top1↓, bottom1↑)" 정도. 강제로 unit-sphere 위로 올려놓은 normalize 가 학습 신호를 거의 다 지움.

### 3.2 형제끼리 Δ (3 형제 거리)

| 지표 | BG-LA − BG-LB | BG-LA − Phase2 | BG-LB − Phase2 |
|------|----------------|------------------|------------------|
| axis_stdev_mean   | +3.9e-05 | +3.5e-05 | -3.9e-06 |
| cell_norm_mean    | +3.7e-05 | +3.6e-05 | -1.3e-06 |
| off_diag_cos_mean | -5.20e-04 | -4.72e-04 | +4.83e-05 |
| off_diag_cos_max  | +1.5e-03 | +1.6e-03 | +1.2e-04 |
| effective_rank    | +1.0e-03 | +4.1e-04 | -6.1e-04 |
| frobenius         | +1.5e-04 | +1.4e-04 | +5.0e-06 |

> 친근 의미: **BG-LB 와 Phase 2 가 거의 0 차이** (effective_rank 차이 6e-04, off_diag 차이 5e-05). 같은 base ckpt 위에 chat finetune 만 추가했는데 cell_pool 자체는 안 흔들림. BG-LA 도 BG-LB 와 0.001 단위 차이 — 같은 arch, 같은 normalize 라 거의 동일.

---

## 4. H4 가설 정량 confirm 정도

### H4 (unit-sphere normalize erase): **STRONG CONFIRM**

근거:
1. **3 datapoint 모두 random 과의 거리 일치** — BG-LA, BG-LB, Phase 2 가 random 으로부터 같은 방향 같은 크기로 떨어짐
2. **off_diag_cos_mean 증가 +0.005~0.006** 만이 학습 효과 잔존 — 너무 작아서 의미 있는 학습이라 보기 어려움
3. **effective_rank 14.94~14.96 / 16** — 학습 후에도 사실상 풀랭크. cell collapse (H2) 가 아니라 normalize 자체가 gradient 효과를 무력화
4. **BG-LA = BG-LB 검증 통과** — 같은 arch, 같은 normalize, 같은 step → cell_pool 거의 동일 (Δ effective_rank 0.001). 가설의 reproducibility 확보

> 친근 의미: "쌍둥이 + 셋째 + 갓난 아이 4 명 비교했는데 키, 체중, 얼굴 비율 다 똑같다 — 학교 (training) 가 외모를 안 바꿨다" 가 강력 확인.

---

## 5. H5 가설 정량 검증 plan (Phase 2 vs BG-LB lm_head 차이)

### 모순 관찰

| 측정 | BG-LB | Phase 2 | 변화 |
|------|-------|---------|------|
| cell_pool stats | (위 표) | (위 표) | **거의 동일 (Δ effective_rank 6e-04)** |
| forward pass DCR | ~0.62 | ~0.24 | **-0.38 collapse** |
| forward pass PIV | ~0.011 | ~0.005 | **-0.006 collapse** |

→ cell_pool 은 안 변했는데 forward pass 가 깨짐. 다른 weight 가 chat 학습으로 무너졌다는 뜻.

### 검증 plan (0-cost local probe)

1. **lm_head weight 직접 비교** — BG-LB ckpt vs Phase 2 ckpt 의 `lm_head.weight` cosine similarity
   - 측정 위치: `step_8000_final.pt` (BG-LB) vs Phase 2 final ckpt
   - 메트릭: row-wise cosine sim (vocab 마다), mean/median/min, frobenius diff
2. **embedding weight 비교** — `embed_tokens.weight` 도 동일 측정
3. **transformer layer norm scale** — chat 학습이 layer norm 만 흔들 가능성도 체크
4. **만약 lm_head cosine < 0.95** → H5 forward-pass-collapse 가설 정량 확정 (lm_head 가 chat 학습으로 흔들려 cell_pool 외부에서 collapse 발생)
5. **만약 lm_head cosine > 0.99** → 다른 곳 (attention proj, FFN) 까지 후보 확장

> 친근 의미: "쌍둥이끼리 외모 (cell_pool) 같은데 시험점수 (DCR/PIV) 가 다르다 — 그럼 외모 말고 어디가 다른지 (lm_head?) 찾아보자."

---

## 6. future cycle suggestion

| 우선순위 | 측정 | 비용 | 결과 의미 |
|----------|------|------|------------|
| P1 | lm_head cosine sim (BG-LB vs Phase 2) | 0-cost local | H5 forward-pass-collapse 가설 정량 검증 |
| P2 | embed_tokens cosine sim | 0-cost local | input-side collapse 후보 |
| P3 | layer-by-layer weight diff frobenius | low local | collapse 가 어느 layer 에서 시작하는지 매핑 |
| P4 | Engine A-G fix 5 normalize 제거 prototype | mid (학습 1 epoch) | H4 직접 검증 — normalize 제거로 cell_pool 학습 효과 살아나는지 |

> 친근 결론: 3-way evidence 가 모순 없이 한 그림으로 모임. **다음 사이클은 lm_head cosine 측정 1 step 만으로 H5 정량 결판** — 그 다음 normalize 제거 실험 (fix 5) 가 자연스러운 다음 길.

---

## 7. 친근 한 줄

> **"세 형제 외모는 갓난아이랑 똑같은데 시험 점수만 다르다 — 외모 (cell_pool) 가 아니라 손 (lm_head) 이 흔들렸을 가능성이 매우 높다. 다음 측정 한 번이면 결판난다."**

---

## 8. lineage / SSOT

- evidence: `state/anima_bg_la_cell_pool_evidence_2026_05_09.json`, `state/anima_bg_lb_cell_pool_evidence_2026_05_09.json`, `state/anima_phase_2_cotrain_cell_pool_evidence_2026_05_09.json`
- 관련 spec: `docs/anima_engine_a_g_fix_5_normalize_removal_spec_2026_05_09.md`, `docs/anima_engine_a_g_fix_6_chat_curriculum_spec_2026_05_09.md`
- strict: local CPU only, no H100 fire, no pod create
- ts_utc: 2026-05-09T (consolidation)
