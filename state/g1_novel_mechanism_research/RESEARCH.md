# G1 재조합벽 밖 신규 메커니즘 — deep-research (2026-07-02, wf_7b787adb-cee)

102 agent · 5각 검색 → 20소스 → 25주장 3표 적대적 검증 → 22 confirmed / 3 refuted. floored 5축
(objective·readout·reg·data·scale) **밖**의 G1 재조합 메커니즘 조사. 원 질문 = "held-out factor
pairing 을 여는 training-time 메커니즘, 위 5축 아닌 것".

## 3 live family + 1 hard-negative

### 1. Neurosymbolic / program-synthesis (DPI를 구조적으로 깨는 유일 경로)
- **NSR** (2210.01603, ICLR24): Grounded Symbol System(neural 지각 + syntactic parser + symbolic 의미추론)
  을 deduction-abduction 으로 co-train. SCAN/PCFG **100%**, HINT +23%. next-token 이 단일 CE-trained
  feedforward trunk-state 의 함수가 **아님** → DPI 메타법칙 구조적 탈출.
- **ExeDec** (2307.13883, ICLR24 oral, DeepMind): execution-guided subgoal decomposition — subgoal 을
  PRIMARY target 으로 예측 + 실제 실행 interleave. RobustFill/DeepCoder held-out +44%/4×.
- ⚠️ CE-trunk drop-in **아님** · 추론시 외부 executor/DSL oracle 필요 · **$0 cheap-gate 불가** = 아키텍처 departure.

### 2. Additive-slot decoder + encoder-decoder consistency (cheap-testable · 증명보장이나 anima 부적용)
- **Wiedemer/Lachapelle** (2310.05327): additive-per-slot decoder(x̂=Σφk(zk), 각 출력이 ≤1 slot 의존)
  + consistency → held-out Cartesian-product extrapolation **증명**. 조건: slot identifiability · output
  **slot-decomposable(=ADDITIVE)** · marginal slot-coverage. Dreamweaver(block-slot RBSU, ICLR25)·
  AIN(per-attr encoder+shared meta+per-attr decoder, +23% held-out)도 동 family.
- **🔑 anima 부적용 (핵심)**: 이 정리는 **output 이 additive-decomposable** 일 때만 보장. anima G1 재조합은
  정확히 **비-additive**(그래서 additive readout H_1602/H_6164 가 이미 floored). anima 합성이 additive 였다면
  이미 열렸을 것 = additive-slot 은 anima 의 non-additive 벽에 categorically 부적용.

### 3. hard-negative (anima 벽 정합) + refuted
- **Lost-in-Latent-Space** (2204.02283, NeurIPS22): disentanglement **단독**은 held-out 재조합 실패 —
  encoder 가 unseen combo 를 correct latent region 에 못 매핑(벽이 readout 아닌 **표현 내용**에 있음). anima
  DPI/trunk-objective 수렴과 직접 정합.
- data diversity(not scale)만 data축 레버 = 이미 floored (d/e).
- REFUTED (0-3): vector-latent population-code(2305.18063) · binary-mask group-subspace(2512.04015).

## cheap-gate 결과 (slot_cheapgate/)
additive-slot + consistency vs monolithic, 5-seed. v1 측정 결함(seen_mse→0 이라 held/seen ratio 무의미 +
additive-superposition=선형이라 mono도 autoencode-extrapolate). 그러나 **재발사 불요** — §2 핵심대로 additive-slot
은 non-additive anima G1 에 범주적 부적용. (fair-cheap-gate-design-1: 측정 결함이나 mechanism-inapplicability 가 우선.)

## 결론 (goal G1 레버 발견)
- cheap drop-in G1 레버 = **없음**. additive-slot(유일 cheap 후보)은 anima non-additive 합성에 부적용.
- 유일 진짜 escape = **neurosymbolic 아키텍처 departure**(외부 executor/procedure-change 로 DPI 깸) = 오너-스코프.
- 전체 소스 = HYPOTHESES 카드 참조 · 메모리 [[g1-novel-mechanism-deepresearch]].
