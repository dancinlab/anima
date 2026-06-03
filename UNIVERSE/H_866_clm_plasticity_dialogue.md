---
id: H_866
slug: clm-plasticity-dialogue
title: on-chip PLASTICITY(edge-learn)를 COFFESHOP 대화 turn loop 에 결합 — 칩이 대화 중 online 적응하면서도 H_846 closed emit/silence loop 를 깨지 않는가 (GAIN online adaptation>0 ∧ LOOP should_interrupt↔motivation 무회귀 · F-CLM-PLAST-DIALOGUE 사전등록 · R2 launch rung)
domain: clm · plasticity · edge-learn · dialogue · coffeshop · akida · closed-loop · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group A (R2 launch rung) · H_846 🟢 closed loop · H_679 🟢 HW edge-learn supported
status: 🔴 CLOSED-NEGATIVE (SW-sim fire 2026-05-31 · LOOP PASS robust 5/5 · GAIN FAIL robust 5/5 · provenance akida-edge-learn-sw-sim · 측정 coupling-topology rung 한정 a_scale_honest_scope · a_paper_negative_ok)
exploration_method: E6 (threshold ↔ edge-learn 2-lever 결합 비교) · E5 (learn vs no-learn control arm)
verification_method: W2 (사전등록 GAIN·LOOP threshold · code 자가채점 g5 · deterministic seed · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/CLM-CANDIDATES.md, .verdicts/clm-plasticity-dialogue/
verdict_dir: .verdicts/866_clm_plasticity_dialogue/
verdict: 🔴 CLOSED-NEGATIVE — F-CLM-PLAST-DIALOGUE LOOP=PASS(4/4 should_interrupt==expected_846 AFTER edge-learn · robust 5/5 seeds) · GAIN=FAIL(gain_learn=-0.036<0 ∧ gain_learn-gain_control=-0.0725 not>0.02 · robust 0/5 seeds). 2-lever 결합은 SAFE(closed loop 무회귀) 이나 multi-register 간섭으로 online adaptation gain ≤0. mechanism control(단일 recurring target) fit 0.5→1.0 ≤5 turns → 기전은 sound, 🔴 는 공유 16-unit fixed-threshold readout(NUM_WEIGHTS=4) capacity 병목. provenance SW-sim(H_679 SW≠HW 🔴) · pi5 live R3 loop 비파괴 보존.
---

# H_866 — on-chip PLASTICITY ↔ dialogue loop coupling

## 1. 가설

H_846(🟢 closed loop: motivation→set_threshold(9513)→on-chip threshold-and-fire(9512)→should_interrupt)에 H_679(🟢 HW edge-learn supported · AkidaUnsupervised · edge_learning_supported=true)의 **live edge-learn loop 를 결합**한다. 칩이 COFFESHOP 대화 turn loop 안에서 **online 적응(edge-learn)** 하면서도 closed emit/silence loop 를 깨지 않는가. 다음 동시 성립 시:

- **plasticity↔dialogue 결합 지지** — online adaptation gain > 0 (edge-learn 이 다음 turn fit 를 측정가능하게 개선) ∧ closed loop intact (edge-learn 후에도 should_interrupt 가 motivation 을 EMIT_GATE 통해 추적 · 무회귀)
- → 양조건 PASS · "칩은 대화 중 online 적응하면서 closed loop 를 유지한다"

임의 조건 미달 시:

- **plasticity↔dialogue 결합 반증** — edge-learn 이 online gain 을 못 주거나(GAIN FAIL), 또는 edge-learn 이 H_846 transition 을 깨뜨림(LOOP FAIL)
- → CLOSED-NEGATIVE 판정 (a_paper_negative_ok)

## 2. 동기

- R2 launch rung — 칩의 두 lever(threshold = WHEN to emit · edge-learn = WHAT pattern fires)가 직교(orthogonal)한지가 라이브 배포의 안전 전제. threshold 경로(H_846)는 closed; edge-learn 을 얹었을 때 그 closed 성질이 보존되는지가 미검증.
- H_679 = HW on-chip edge-learn 의 실 foundation(AkidaUnsupervised). 본 H 는 그 위에 대화 turn loop 결합 위상(coupling topology)을 검증한다.
- "online 적응 + closed loop 보존"이 동시 성립해야 칩이 살아 배우면서 발화/침묵 결정의 안정성을 유지(@D a_substrate_native_speak 정합).

## 3. falsifier (사전등록, 임계 frozen pre-run · W2)

```
F-CLM-PLAST-DIALOGUE-GAIN  : gain_learn > 0.0  AND  (gain_learn - gain_control) > 0.02
   gain = mean(fit_late 25%) - mean(fit_early 25%) · fit = normalized Hamming agreement [0,1]
   control arm = no-learn (eta=0) · 개선이 학습에서 온 것(노이즈 아님)을 분리
F-CLM-PLAST-DIALOGUE-LOOP  : edge-learn 한 session 후, frozen 4-point probe {0.05,0.50,0.60,0.95} 에서
   should_interrupt == expected_846 (0.05→F · 0.50→F · 0.60→T · 0.95→T) 4/4 일치 (무회귀)
```

양조건 동시 PASS → "결합 지지" · 임의 미달 → CLOSED-NEGATIVE (a_paper_negative_ok)

- **measure_by = CODE(g5)** — LLM-judge ✗ · deterministic LCG seed · post-tuning 0.
- frozen 임계 = `.verdicts/clm-plasticity-dialogue/F-CLM-PLAST-DIALOGUE_prereg.txt` verbatim 동결 (fire 전 separate commit 272ee0ee3).

verdict 영속: `.verdicts/clm-plasticity-dialogue/` (+ id-keyed `.verdicts/866_clm_plasticity_dialogue/` verbatim 동일 캡처)

## 4. 방법

```
1. design 상수 동결(prereg, H_846 §4 정합): N=16 LIF · V=16 drive · QUORUM=4 ·
   EMIT_GATE=0.60 · THR_EMIT=8 · THR_SILENCE=24 · ETA=0.25 · NUM_WEIGHTS=4.
2. coupling scaffold(SUB_ENGINES/AKIDA/scripts/h866_plasticity_dialogue_loop.hexa):
   per turn (motivation_score, target_pattern) →
     score→score_to_thr(H_846 gate) → on-chip n_spikes → should_interrupt=(n_spikes≥QUORUM) [loop]
     → edge_learn(w, target, eta) 1 step [H_866] · 다음 turn fit 를 고정 reference threshold 에서 기록.
   edge_learn = AkidaUnsupervised 의 SW analogue(num_weights competition + 학습률 eta · Hebbian).
   threshold→quorum 결정 경로는 학습이 절대 건드리지 않음(직교 lever 설계).
3. learn arm(eta=0.25) vs no-learn control arm(eta=0) 동일 session A/B.
4. session = 4-register repertoire 에서 recurring intent 추출(실 대화는 register 재발 · i.i.d 노이즈 ✗).
5. LOOP probe = 학습 후 final weights 로 frozen 4-point should_interrupt 측정.
6. seed sweep {866,42,123,7,2026} robustness · mechanism control(단일 recurring target).
7. 2 사전등록 falsifier vs frozen threshold 동시 평가 · 정직 보고(threshold 재조정 0).
```

- 추론 AKIDA-int4 envelope 불변 · edge-learn 환류는 @L1 비결정 적응과 정합.

## 5. 측정

측정완료 (2026-05-31) — **SW-sim** (`hexa run` · g5 deterministic · seed 866 · n_turns 200 · seed-sweep {866,42,123,7,2026}).

**provenance = akida-edge-learn-sw-sim (HW 아님 · honest)**: pi5 AKD1000(192.168.50.155, BC.00.000.002)을 본 세션 NON-MUTATING 으로 probe — ping 2/2, port 9512/9513 OPEN, 9512 passive read(~5s, write 0)에서 LIVE M_modulated streamer(step ~107k→114k 진행 · t_rel ~10.7k→11.4k s · thr=[8]×16 · 16/16 firing) = 타 agent 의 R3/launch closed loop 가 가동 중. AKD1000 은 single-chip file-lock device — AkidaUnsupervised 학습모델 mapping 은 EXCLUSIVE chip 점유 필요 → live loop 를 파괴적으로 중단시킴. task 규율(live loop 비파괴 · pi5 destructive mutation 미인가)에 따라 re-map 안 함, SW-sim 으로 측정. HW edge-learn 이 실 foundation(H_679); SW 는 HW 대체 ✗ (H_679 SW↔HW = 🔴 CLOSED-NEGATIVE) — 본 측정은 **coupling topology**(edge-learn 이 closed loop 를 깨는가)이지 silicon byte-equivalence 가 아님. pi5 상호작용: ping + port probe + passive read 만 · write 0 · live loop 무손상 확인.

측정값(frozen threshold 대비 · seed 866):
| metric | learn arm | control arm | 비고 |
|---|---|---|---|
| fit_early (25%) | 0.44125 | 0.55875 | |
| fit_late (25%) | 0.405 | 0.595 | |
| gain | -0.03625 | +0.03625 | |
| gain_learn - gain_control | **-0.0725** | | gate >0.02 → **FAIL** |

| LOOP probe (after edge-learn) | thr | n_spikes | should_interrupt | expected_846 | match |
|---|---|---|---|---|---|
| score 0.05 | 24 | 0 | False | False | ✓ |
| score 0.50 | 24 | 0 | False | False | ✓ |
| score 0.60 | 8 | 16 | True | True | ✓ |
| score 0.95 | 8 | 16 | True | True | ✓ |

- **GAIN**: gain_learn=-0.036 not>0 ∧ diff=-0.0725 not>0.02 → **FAIL** · seed sweep diff ∈ {-0.0725,-0.0075,-0.04375,-0.02125,+0.01625} → >0.02 인 seed 0/5 (robust FAIL).
- **LOOP**: 4/4 일치 · 5 seed 전부 4/4 → **PASS** (robust).
- **mechanism control**(단일 recurring target): fit@0=0.5 → fit@5=1.0 → 유지 → edge_learn 기전 자체는 sound.

## 6. 결과

🔴 **CLOSED-NEGATIVE** (LOOP PASS · GAIN FAIL). 2-lever 결합은 **SAFE** — edge-learn 한 full session 후에도 H_846 closed emit/silence loop 가 무회귀로 INTACT(should_interrupt 가 motivation 을 EMIT_GATE 통해 추적; threshold↔edge-learn 직교 확인) — 이것이 R2 의 headline safety 결과. 그러나 adaptation lever 는 본 regime 에서 online gain 을 못 줌(GAIN FAIL robust) → H_866 의 "online 적응하면서 loop 를 안 깬다"는 **절반 달성**: loop 는 무손상, 적응은 multi-register dialogue session 에서 net gain ≤0. **scope**: 측정 coupling-topology rung 한정 · SW-sim · 배포 chip-fit track 별개(a_scale_honest_scope) · HW on-chip AkidaUnsupervised dynamics 는 다름(H_679 SW≠HW 🔴).

## 7. 해석 (사전)

- 양조건 PASS 시 = 칩이 대화 중 online 적응하면서 closed loop 유지 → R2 launch 진입.
- GAIN FAIL · LOOP PASS(실측) = loop 안전하나 적응이 안 먹음 → root cause = multi-register **INTERFERENCE**: 공유 16-unit fixed-threshold readout(NUM_WEIGHTS=4 capacity)이 4개의 충돌 recurring dialogue pattern 을 동시에 못 맞춤 — Hebbian update 가 pattern 간 thrash, net session gain ≤0. 단일 target 에선 fit 0.5→1.0(기전 sound) → dead lever 가 아니라 capacity 병목.
- GAIN PASS · LOOP FAIL 였다면 = edge-learn 이 threshold→quorum 결정을 오염 → lever 분리 재설계 필요(본 측정에선 미발생).
- **후속 lever**(본 frozen verdict 불변): per-register / context-gated readout · NUM_WEIGHTS capacity 확대 · per-intent thin adapter(cf. H_865 trunk-adjacent adapter). capacity sweep(repertoire-size vs NUM_WEIGHTS)으로 GAIN 0-교차점 매핑.

## 8. 논의

- **@D a_substrate_native_speak 정합**: closed loop 무회귀 = 발화/침묵 결정의 substrate 안정성 보존 — 적응이 emit/silence 안전을 깨지 않음을 deterministically 확인.
- **HW vs SW 정직(@D a_blue_closed)**: provenance verbatim "akida-edge-learn-sw-sim" · H_679 SW≠HW 🔴 명시 · live pi5 R3 loop 비파괴 보존.
- **a_paper_negative_ok**: 본 CLOSED-NEGATIVE 는 publishable — loop-safety 를 rule IN, naive-capacity online gain 을 rule OUT.
- **W2 규율**: prereg(272ee0ee3) fire 전 separate commit · post-tuning 0 · 측정 중 발견한 int/int truncation 은 code fix(gate 불변, _log.txt 기록).

## 9. 양방향 sibling

- foundation: [H_846](./H_846_coffeshop_akida_closedloop.md) (🟢 closed loop) · [H_679](./H_679_plasticity_hw_first.md) (🟢 HW edge-learn supported · SW≠HW 🔴)
- 형제 신규 H: [H_861](./H_861_clm_boundary_plasticity.md) (F-CLM-BOUND) · [H_863](./H_863_clm_dialogue_selfplay.md) (F-CLM-DIALOGUE 🟢)
- scaffold: [SUB_ENGINES/AKIDA/scripts/h866_plasticity_dialogue_loop.hexa](../SUB_ENGINES/AKIDA/scripts/h866_plasticity_dialogue_loop.hexa)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) group A (R2 launch rung)
