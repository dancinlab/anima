# H_9312 — σ 3-갈래 분해 (PRESENCE / INFO) · 사전등록

프레임: Fable w4_sigma 도시에 카드 1 (H_σA SELF-INFO/PRESENCE 이중 스크리너).
**데이터를 보기 전에 동결**한다. 이후 어떤 바·마진·헤드라인도 변경 금지.

## 계기
- tape = `anima_kill <ckpt> --opgrip --opgrip-dump` → `#OGD {json}` × 2000 tick
  ($0 no-decode · READ-ONLY: 어떤 결정도 바꾸지 않음 · n_ticks 250→2000 만 변경).
- 필드: tick, stage, wake, e_live, motiv, thr, safe, idle, urgency, stage_env,
  self_ctx_live, self_ema, self_phasic, ev_axis,
  8-lane = [rel_lane, af_val, allo_ctx, coh_lane, bal_lane, nov_ctx, gap_ctx, ag_conflict], recon_err.
- 스코어 구간: tick ≥ 50 (0–49 = g_self 캘리브 구간, 제외) ⇒ n = 1950.
- held-out split: 스코어 구간의 전반 = fit, 후반 = test (시간 분할, 누수 0).

## DV (2 방향, 같은 tape)
1. **PRESENCE (정방향 state → self)**: 8-lane + 연속 마진 2개(motiv−thr, idle−30) → `self_ctx_live` 를
   ridge(α=1.0, z-score) 로 예측한 **held-out R²**.
2. **INFO (역방향 self → emit)**: self 특징 [self_ctx_live, self_ema, self_phasic, lag1..8 of self_ctx_live]
   → **다음 tick e_live** 를 로지스틱(ridge) 로 예측한 **held-out D-acc** + **EARNED nats**
   (= held-out log-loss 개선분: base-rate 상수 예측 대비, H_9304 정의).

## arms
- EXP: live self
- **C1 CIRC** (주 null): self 시계열을 원형 시프트 × 200 (자기상관·주변분포·스펙트럼 완전보존, 정렬만 파괴)
  → 경험적 null 분포. shift 는 |s| ≥ 50 tick 만 사용.
- **C2 PHASE-RAND**: 위상무작위 surrogate (파워스펙트럼 보존) × 200.
- **PEDESTAL (참값 0)**: self 를 자기상관 정합 AR(1) 대리스트림(독립 RNG seed, LCG 아님 — 단일 cycle
  해시시드 함정 회피)으로 치환 ⇒ 참 정보 = 0. 기대: null 분포 안.
- **POS (참값 기지)**: y_pos = (self_hi) 를 확률 (1−p) 로 따르고 p=0.35 로 뒤집은 라벨
  (self_hi = self_ctx_live > median). 참 D-acc = 0.65 기지.
  **measured/truth 비율 0.8–1.25 밖 ⇒ 계기 결함 ⇒ verdict INVALID** (PASS/FAIL 아님).

## 검정력 (데이터 전 계산)
- n_test ≈ 975. D-acc 우연 sd ≤ 0.5/√975 = **0.0160** ⇒ 2σ MDE ≈ **0.032 acc**.
  (실제 판정은 200-shift 경험적 null 의 분위수로 하므로 모수 가정 없음.)
- ridge R² null ≈ k/n_test = 10/975 = 0.010 ⇒ **R² ≥ 0.02 검출 가능**.
- **degeneracy 게이트 (선행)**: sd(self_ctx_live) < 1e-6 또는 e_live 의 클래스 최소빈도 < 30
  ⇒ **NOT-POWERED / INVALID**, PASS/FAIL 판정 금지 (계기 degenerate).

## PASS/FAIL (동결)
- **PRESENCE-PASS**: R²_EXP − R²_CIRC(95pct) ≥ **0.02** ∧ PEDESTAL R² ≤ CIRC 95pct.
- **INFO-PASS**: D-acc_EXP > CIRC null 99pct ∧ EARNED ≥ **0.01 nats**.
- **INFO-NULL (TOST · 사전등록 등가마진)**: |D-acc_EXP − CIRC median| ≤ **0.05**
  ∧ |EARNED| ≤ **0.02 nats** (양측) ⇒ **등가 = 정보 부재**. ('ns' 금지)
- **INVALID**: POS 비율이 [0.8, 1.25] 밖 · 또는 PEDESTAL 이 EXP 를 넘김 · 또는 degeneracy 게이트 히트.
- max(controls) 순서통계량 금지 — null 은 200-shift **분위수**, 대조는 paired 로만.

## 3-갈래 판독 (사전 고정)
- INFO-NULL ∧ PRESENCE-FAIL ⇒ **데이터/표현 부재** — 4 mechanism family 는 a priori 사망.
  σ⊥mouth = 설계정합. G1 벽과는 **다른 벽**.
- PRESENCE-PASS ∧ INFO-NULL ⇒ **소비 부재** — 표현은 있으나 emit 정보 없음 ⇒ **G1 과 동형(하나의 벽)**.
- PRESENCE-PASS ∧ INFO-PASS ⇒ THEATER cement 는 **범위초과 오판** ⇒ 소비 연산자 부재 = 큰 재프레임.
- PRESENCE-FAIL ∧ INFO-PASS ⇒ 계기 이상(선형 readout 밖) ⇒ 재설계.
