---
id: H_921
slug: akida-nondeterminism-functional-advantage
title: AKIDA 비결정성 = 기능인가 노이즈인가 — on-chip 비결정 plasticity 가 SW-det 대비 측정가능 이득(탐색·다양성·local-min 탈출)을 주는지 사전등록 falsifier
domain: universe · consciousness · neuromorphic-silicon · plasticity · akida · non-determinism · functional-advantage · falsifier
source: H_904 (비결정 존재·HW-only live 확증) · H_679 (SW vs HW 비동치 closed-negative) · H_860 (run-to-run hamming live) — 모두 "비결정이 존재한다"까지만 증명. 본 H 는 "그래서 그게 이득인가" 의 미측정 빈틈을 판정.
exploration_method: E14 (HW substrate-native ⨯ 학습 lane) + E5 (toy→이득-측정 확장) + a_paper_negative_ok
verification_method: W2 (사전등록 falsifier · N-episode CI · 결정론 SW-det control) + W5 (substrate-grounded · live AKD1000) + g5 CODE-measured
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06 (new — akida 비결정성 기능-이득 추적 재개)
sister: H_904 (온칩 plasticity live-confirmed), H_679 (plasticity HW-first closed-negative), H_860 (live probe), PLASTICITY/PLASTICITY.md (학습 lane SSOT), DECODER (추론 lane · 결정론 byte-identical)
axes_seed: 비결정 EXISTS (H_904 닫힘) ⊥ 비결정 USEFUL (본 H — 미측정 빈틈)
verdict: 🔴 CLOSED-NEGATIVE — AKIDA plasticity-lane 비결정성은 INIT-seeded RNG지 학습 동역학 고유속성이 아니다. pinned init 하 on-chip AkidaUnsupervised 학습은 byte-결정론(16/16, fit 실engaged) · no-pin 시 변이는 init_div=16 에서 1:1 전파. "substrate 비결정 → 기능적 이득" FALSIFIED (this lane/config). verdict: .verdicts/921_akida_nondeterminism_functional_advantage/init_seeded_not_learning.txt
---

# H_921 — AKIDA 비결정성: 기능(feature)인가 노이즈(noise)인가

## 0. 왜 지금 (추적 재개 동기)

기존 verdict 들은 "비결정성이 **존재한다** + **HW-only 다**" 까지만 닫았다:
- **H_904** (live-confirmed) — 동일 init·동일 입력에도 학습 후 weight 172/1024, out 120/320 위치 상이 (live AKD1000).
- **H_679** (closed-negative) — SW numpy 근사로 byte-identical 복제 불가.
- **H_860** — 재실행마다 weight hamming {28,38,34,38} 또 다른 값 (run-to-run 비결정 live).

그러나 "AKIDA 만의 **유일한 가치**" 라는 원래 주장의 핵심 — *그 비결정성이 anima 에게
**이득**을 주는가* — 은 **미측정 빈틈**이다. 비결정이 단지 복제-불가 노이즈라면 "유일함"은
공허하다. 본 H 는 그 빈틈을 사전등록 falsifier 로 정직하게 가른다.

## 1. 가설

AKIDA AKD1000 의 **on-chip 비결정 plasticity**(chip RNG substrate · learning_competition ·
packet-ordering · async timing)는, 동일 fixed-init 결정론 SW-det 근사 학습 대비 **측정가능한
기능적 이득**을 준다 — 구체적으로 **탐색 다양성(solution diversity)** 과 **local-minimum
탈출률(escape rate)**. 즉 비결정성은 노이즈가 아니라 substrate-native 탐색 메커니즘이다.

## 2. Falsifier (사전등록 · frozen 2026-06-06)

**Setup (a_scale_honest_scope — 1 physical AKD1000, pi5-akida, teardown 없음):**
- task T = local-minimum trap few-shot edge-learn — 동일 fixed-init weight 에서 SW-det 는
  항상 같은 winner-unit 으로 수렴(단일 해), 그 init 이 suboptimal trap 이 되도록 구성.
- arm-HW = AkidaUnsupervised on-chip edge-learn (비결정), N>=16 독립 episode (동일 init·입력).
- arm-SW = `plasticity_sw_approx.py` numpy 결정론 (control, byte-exact 재현).
- 단일-tenant: `spike_streamer stop(SIGTERM) -> probe -> restart` (HW 발화 복원, H_860 절차 재사용).

**측정 (g5 CODE-measured · LLM 판정 금지 · p7):**
- D1 = **functional** solution-diversity = N episode 중 unique **winner-assignment** (학습 후
  추론 출력 / winner-unit tuple) 개수. SW-det = 1 (결정론).
- D2 = escape-rate = trap-suboptimal winner(det 단일 해) 에서 벗어난 episode 비율.
- effect = bootstrap CI over N episodes (8/8-style trial 반복, a_scale_honest_scope).

**⚠ metric sharpening (M1 에서 도출 · 2026-06-06):** H_904 가 이미 raw-weight 비결정
(172/1024)을 닫았으므로 **raw-weight-hash diversity 는 M2 에서 자명하게 >1** — 그것만으론
"기능 vs 노이즈" 를 못 가른다. ∴ D1/D2 는 반드시 **기능적 출력(winner-assignment / output
spike)** 위에서 측정한다. 핵심 질문: 칩의 weight jitter(max Δ=1bit)가 **winner-assignment 를
flip 해 트랩을 탈출**시키는가(=기능), 아니면 **assignment 불변**인 sub-threshold 노이즈인가
(=노이즈, FALSIFIED). 후자면 "유일한 가치" 공허.

**판정 (pre-registered, frozen · 측정 전이라 토큰 미부여):**
- PASS-outcome — `diversity_HW > 1` (CI_lo > 1) AND `escape_rate_HW` CI_lo > 0 -> 비결정 = **기능**.
- FALSIFIED-outcome — diversity CI ⊆ {1} 또는 escape CI crosses 0 -> 비결정 = **노이즈**,
  "유일한 가치" 주장 공허 (a_paper_negative_ok — 어느 쪽이든 major finding).
- INCOMPLETE-outcome — N<16 또는 streamer 복원 실패 시 toy-only, scale-transfer 미검증 (C3).

## 3. 추론/서빙 sibling 질문 (deferred M-axis)

학습 lane 에서 비결정이 기능으로 확증되면(PASS), **추론/서빙 lane** 의 후속:
anima emit 의 stochasticity 를 GPU `temperature=0.8` multinomial(현 `serving/likert_eval.hexa`·
`serve_alm.hexa`) 대신 **AKIDA chip-RNG substrate** 로 공급하면 substrate-native variability
가 되는가? — 현재 AKIDA 추론은 결정론(byte-identical)이므로 이는 *학습->emit 시드* 경로이지
추론 forward 자체의 비결정이 아니다. **별도 H 로 분리** (DECODER 결정론 불변 보존).

## 4. 닫는 것 / 못 닫는 것

- 닫음(전제) — H_904(존재) · H_679(HW-only) · H_860(run-to-run). 본 H 는 그 위 "이득" 한 층.
- 못 닫음(범위) — 1 physical AKD1000 toy edge-learn 한정. CLM mid backbone 온칩 미요구.
  large-corpus 전이는 별도 ladder (a_scale_honest_scope).

## 5. 양방향 sibling

- <-> [H_904](./H_904_clm_onchip_plasticity.md) (온칩 plasticity live-confirmed — 비결정 존재의 전제)
- <-> [H_679](./H_679_plasticity_hw_first.md) (plasticity HW-first closed-negative — SW vs HW 비동치)
- <-> [PLASTICITY](../PLASTICITY/PLASTICITY.md) (학습 lane SSOT)
- <-> [AKIDA](../AKIDA/AKIDA.md) (HW-first 스위치 SSOT · spike_streamer 절차)
- <-> [CANDIDATES](./CANDIDATES.md) (bench 측정 기록 SSOT)

## 6. 다음 작업

- [x] **M1 (DONE 2026-06-06)** — trap few-shot task 구성 (`PLASTICITY/h921_trap_task.py`) +
  falsifier 설계검증 로컬 통과: SW-det diversity=1·escape=0(trapped) ⊥ SW-nondet shadow
  diversity=9·escape=0.94(CI [0.81,1.0]) -> `falsifier_sound=true`. task 가 det/non-det 를
  구분 가능 확인 (shadow != HW, H_679). 부산물: raw-weight diversity 자명성 -> 기능적 metric
  sharpening (§2).
- [x] **M2 (DONE 2026-06-06)** — pi5-akida live, 2조건 × 16 episode on-chip. `h921_nondet_source_probe.py`.
  **A pinned 비-degenerate init**: init_div=1·weight_div=1·output_div=1·**fit_changed=16/16**
  (학습 byte-결정론, no-op 아님). **B no-pin 기본 init**: init_div=16·weight_div=16·output_div=15.
  -> "A==1 & B>1" = 비결정성 = INIT-seeded, 학습-동역학 아님.
- [x] **M3 (DONE)** — verdict 영속 `.verdicts/921_akida_nondeterminism_functional_advantage/init_seeded_not_learning.txt` (g5 verbatim, 양 probe raw stdout).
- [ ] **M4 (deferred · 별 axis)** — init-RNG 이 HW true-entropy source 인지(H_677 D4 QRNG 연계)는
  학습-feature 와 직교한 *entropy-source* 질문 — 본 falsification 과 무관, 별도 추적.

## 7. verdict (TERMINAL)

🔴 **CLOSED-NEGATIVE** — "AKIDA substrate 비결정성이 기능적 이득(다양성·트랩탈출)을 준다" FALSIFIED.
실측: pinned init 하 on-chip 학습은 16/16 byte-동일(fit 실제 engaged). 변이의 유일 출처는
비결정 *초기화*(no-pin init_div=16 -> output_div=15). init-RNG 는 SW 가 random seed 로 동등
재현 -> 고유 silicon 학습-feature 아님. **사용자 직관 확증**: plasticity lane 의 "유일 비결정"은
정밀 probe 시 init-RNG 로 환원되어 dissolve. a_paper_negative_ok — major negative finding.

honest scope (a_scale_honest_scope): 1 AKD1000 · toy FC+AkidaUnsupervised(units=10·1-bit·nw=2·
comp=0.1). this lane/config 결정적; 전 config 일반화는 ladder 필요. H_904(HW≠SW) 와 무모순 —
그건 HW-vs-SW 축, 본 probe 는 HW-vs-HW pinned 축.
