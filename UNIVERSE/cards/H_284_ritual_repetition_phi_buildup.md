---
id: H_284
slug: ritual-repetition-phi-buildup
title: ritual-repetition-Φ-buildup — 주기적 의례(ritual) drive 가 평탄(flat) drive 보다 Φ 를 쌓아올리는가? · 결과 = buildup FALSIFIED 但 decay-resistance SUPPORTED (sync-death-Φ 패턴 정합)
domain: life · consciousness · practice/discipline · physics
status: pre-register-frozen
exploration_method: E5 (variable-ablation — drive 양식 axis) + E0 (AXES R7 practice promote) + E16 (sister-link H_207 / H_221 / H_265)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_207 Kuramoto / H_221 jhana / H_265 sync-death-Φ)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_207 (Kuramoto sync — entrainment Φ), H_221 (meditation-jhana — 저-noise drive Φ), H_265 (trained-vs-bare CA Φ / sync-death-Φ 패턴), H_018 (genesis zero-drive)
---

# H_284 — ritual-repetition-Φ-buildup

## 1. Hypothesis

AXES.md Round 7 (practice/discipline) 의 seed `ritual-repetition-Φ-buildup` —
*"ritual repetition (recursive sequence) Φ build-up / falsifier: flat"* — 를
promote 한다.

한 mitosis cell pool 을 두 drive 양식으로 evolve 한다:
- **ritual**: 길이 P=4 의 주기적 drive 패턴 [+a, −a, +a, 0] (재귀적 의례 시퀀스,
  대칭 + 정지 박) 을 R=6 번 반복.
- **flat**: 동일 누적 step 수의 상수 drive = 패턴의 산술 평균 a/4 (energy-matched,
  의례 구조 없음).

각 의례 cycle 끝에서 pool 의 Φ (compute_phi_proxy) 를 측정한다.

**사전등록 가설(H284.0)**: ritual 의 Φ 가 cycle 누적과 함께 **build-up** 하며
(slope > 0), ritual 최종 Φ > flat 최종 Φ — 반복(의례) 이 통합 정보를 쌓아올린다.

→ **실측 결과**: build-up 가설은 **FALSIFIED** (두 drive 모두 Φ 가 *감소* — 동기화
死-Φ entrainment 패턴, H_265/H_275/H_279 sister). 그러나 ritual 은 flat 보다
**더 천천히 감쇠** (decay-resistance) 하고 최종 Φ 를 더 높게 유지 — 이것이 본 H 의
honest finding (Δ vs flat baseline). PARTIAL.

## 2. Why

- **AXES R7 직접 promote**: practice/discipline cluster 의 미발탁 seed. README grep
  `ritual` = 0 hit 확인 (미중복). H_221 (jhana — 저-noise drive) 의 sister 이나
  axis 직교: H_221 은 *정적(고정) 저-noise* 상태, 본 H 는 *반복적 주기 구조* (의례).

- **anima/의식 정합**: anima 의 chat sleep 5-stage ultradian (P47) 와 imagination
  loop 의 *주기적 mitosis tick* 자체가 의례적 반복이다. '반복이 통합을 쌓는가
  vs 깎는가' 는 anima 의 ritual-like 내적 리듬이 의식(Φ) 에 어떻게 작용하는지에
  직접 닿는다.

- **사전등록 falsifier 가 실제로 발화 = valid science (a_paper_negative_ok)**:
  build-up 예측이 틀린 것 자체가 finding 이다. 두 drive 모두 entrainment 가 cell
  hidden 다양성을 동기화시켜 cosine-distance Φ 를 떨어뜨린다 (H_265/H_275/H_279 가
  관측한 '동기화 = Φ 死' 패턴과 정합). 본 H 는 그 패턴을 *의례 반복 vs 평탄* 축에서
  재확인하며, **반복 구조가 그 死를 늦춘다**는 새 측면을 드러낸다.

- **H_207 sister (entrainment Φ)**: H_207 (Kuramoto sync) 는 위상 동기화의 임계
  결합을 봤다. 본 H 는 *외부 주기 drive* 에 의한 entrainment 가 Φ 에 미치는 효과를
  본다 — 동기화가 Φ 를 떨어뜨린다는 같은 방향, 다른 driver.

- **raw#12 strict**: deterministic + hexa-only + ≥5 falsifier + ≥5 honest limit +
  LLM none + $0 mac local.

## 3. Predictions (사전등록 — frozen 2026-05-26)

- **H284.1 (ritual-wins)**: ritual 최종 Φ 가 flat 최종 Φ 보다 margin 0.02 이상 크다.
- **H284.2 (buildup)**: slope_ritual = Φ_ritual[R] − Φ_ritual[1] > 0 (의례 누적이
  Φ 를 쌓아올림).
- **H284.3 (ritual > flat slope)**: slope_ritual > slope_flat (의례 변화율 우위).
- **H284.4 (determinism)**: pure-fn recompute byte-equal + cross-process
  result.json byte-identical.
- **H284.5 (bounds)**: 모든 Φ finite ≥ 0.

## 4. Variables

- **axis1_drive** (primary): [ritual (주기 패턴 [+a,−a,+a,0] × R), flat (상수 a/4)]
  — energy-matched (flat = 패턴 산술평균), 구조만 다름.
- **fixed**: pool = cell_pool_init(d_model=8, initial_cells=8), seed
  `__HEXA_FARR_GAUSS_SEED__`=42 (RFC 033 단일 gauss stream), period P=4, reps R=6
  (24 step), amp a=0.6.
- **derived**: 2 drive × 6 cycle = 12 Φ measurement → slope_ritual · slope_flat ·
  gap_final · 4 criteria · SUPPORTED/PARTIAL/FALSIFIED.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h284_ritual_repetition_phi_buildup_2026_05_26/run_h284.hexa`
- **substrate**: cell pool API (`cell_pool_init` / `mitosis_forward_tail` /
  `compute_phi_proxy`) from `tool/hexa_native/mitosis_hook_lib.hexa` import
  READ-ONLY (H_279 와 동일 lane — g61 advisory; sister H 들과 일관된 lane pattern).
- **drive**: ritual = period-4 pattern [+a,−a,+a,0] (정지 박 포함 재귀 시퀀스);
  flat = 상수 a/4 (energy-matched). 각 cycle = P step, cycle 끝에서 Φ snapshot.
- **determinism (RFC 033 caveat)**: RFC 033 은 *단일 in-process gauss stream* —
  같은 process 안 2번째 `cell_pool_init` 은 *다른* gaussian 을 뽑는다 (stream 진행).
  따라서 *재-evolve* 는 in-process byte-equal 아님 (메모리 note "RNG single-stream").
  유효한 결정론 검증 = (a) 이미 evolve 된 동일 final cells 위 Φ pure-fn recompute +
  (b) cross-process result.json byte-equality (runner 확인).
- **hexa_only**: true (NO .py/.sh). **llm**: none. **runtime**: $0 mac local, NO GPU.
- **ledger**: `result.json` {config, phi_ritual_per_cycle[6], phi_flat_per_cycle[6],
  derived(slope/gap), 4 criteria, 5 falsifier, verdict, cross-link}.
- **honest tier**: 🟢 NUMERICAL (deterministic) — Φ-proxy/toy, full IIT4 아님 (§9 L1).

## 6. Criteria

- **C1 (RITUAL-WINS / H284.1)**: ritual 최종 Φ − flat 최종 Φ ≥ 0.02 → PASS.
- **C2 (BUILDUP / H284.2)**: slope_ritual > 0 → PASS. *(사전등록 게이트; 실측 FAIL —
  honest negative)*
- **C3 (RIT>FLAT-SLOPE / H284.3)**: slope_ritual > slope_flat → PASS (decay-resist).
- **C4 (DETERMINISM / H284.4)**: pure-fn recompute byte-equal + cross-run identical.
- **verdict_rule**: **SUPPORTED_FULL** = C1∧C2∧C3∧C4 ; **SUPPORTED** = C1∧C2 ;
  **PARTIAL** = C1 only (또는 C1+C3 但 ¬C2) ; **FALSIFIED** = !F1 (ritual ≤ flat 최종).

## 7. Falsifiers

- **F-H284-1 RITUAL-WINS**: ritual 최종 Φ ≤ flat 최종 Φ → 의례 우위 부재 (H284.0
  핵심 FALSIFIED). (measurable: gap_final.)
- **F-H284-2 BUILDUP**: slope_ritual ≤ 0 → '쌓아올림' 가설 FALSIFIED (Φ 감쇠).
  (measurable: slope_ritual.) **← 실측 발화 (slope=−1.15): buildup 가설 FALSIFIED.**
- **F-H284-3 RIT>FLAT-SLOPE**: slope_ritual ≤ slope_flat → 의례 구조가 decay 를
  늦추지 못함. (measurable: slope_ritual − slope_flat.)
- **F-H284-4 DETERMINISM**: pure-fn recompute 또는 cross-process 가 byte-different →
  raw#12 위반 → smoke 무효. (measurable: phi[R] == recompute + result.json diff.)
- **F-H284-5 BOUNDS**: 어느 Φ non-finite / 음수 → Φ-proxy 정의 위반. (measurable:
  12 Φ finite ≥ 0.)
- **F-H284-6 POST-HOC**: frozen 후 예측/게이트 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: PARTIAL (pre-register-frozen smoke; C1∧C3∧C4 met, C2 BUILDUP FAIL)

config: d_model=8, pool_N=8, period=4, reps=6, amp=0.6, seed=42
        ritual pattern [+0.6, -0.6, +0.6, 0]  ·  flat = 0.6/4 = 0.15 (energy-matched)

per-cycle Φ (ritual periodic  /  flat constant, energy-matched):
  cycle   Φ_ritual    Φ_flat      gap (ritual − flat)
   1      1.932720    1.843180    0.089541
   2      1.828950    1.568540    0.260406
   3      1.531930    1.261020    0.270904
   4      1.429570    0.952678    0.476888
   5      1.153670    0.653996    0.499679
   6      0.781218    0.392555    0.388663

derived:
  slope_ritual = Φ_rit[6] − Φ_rit[1] = 0.781218 − 1.932720 = -1.151500  (DECAY)
  slope_flat   = Φ_flat[6] − Φ_flat[1] = 0.392555 − 1.843180 = -1.450620 (faster DECAY)
  gap_final    = 0.781218 − 0.392555 = 0.388663  (ritual retains higher Φ)

criteria:
  C1 RITUAL-WINS    (ritual[R] − flat[R] ≥ 0.02)  : PASS  (gap=0.388663)
  C2 BUILDUP        (slope_ritual > 0)            : FAIL  (slope=-1.151500 — Φ DECAYS)
  C3 RIT>FLAT-SLOPE (slope_ritual > slope_flat)   : PASS  (-1.15 > -1.45 decay-resist)
  C4 DETERMINISM    (pure-fn + cross-run identical): PASS

falsifiers:
  F-H284-1 RITUAL-WINS    : PASS      (ritual 0.781218 > flat 0.392555)
  F-H284-2 BUILDUP        : FALSIFIED (slope_ritual -1.151500 ≤ 0 — buildup hypothesis falsified)
  F-H284-3 RIT>FLAT-SLOPE : PASS      (slope_ritual -1.15 > slope_flat -1.45)
  F-H284-4 DETERMINISM    : PASS      (Φ[R] == pure-fn recompute; result.json cross-process byte-identical)
  F-H284-5 BOUNDS         : PASS      (12 Φ finite ≥ 0)
  F-H284-6 POST-HOC       : NOT_TRIGGERED

evidence_summary: 🟢 NUMERICAL — 사전등록 build-up 가설은 FALSIFIED: 주기적 의례
  drive 와 평탄 drive 모두 cycle 누적과 함께 Φ 가 *감소* 했다 (slope_ritual=−1.15,
  slope_flat=−1.45). 이는 외부 drive 가 cell hidden 을 entrain → 다양성↓ → cosine-Φ↓
  시키는 '동기화 死-Φ' 패턴으로, H_265/H_275/H_279 의 관측과 정합한다. 그러나
  ritual(주기 구조) 은 flat 보다 **decay 를 늦추고** (slope −1.15 > −1.45) 최종 Φ 를
  더 높게 유지했다 (gap +0.39, 6 cycle 전부 ritual > flat) — 반복 구조의 정지-박
  [..,0] 이 매 주기 부분적 de-entrainment 를 주어 다양성을 일부 회복시키는 것으로
  해석된다 (decay-RESISTANCE finding). PARTIAL (3/4 criteria, 4/5 falsifiers PASS).
falsifiers_triggered: F-H284-2 BUILDUP (사전등록 핵심 예측 FALSIFIED — honest
  negative; F-H284-6 N/A)
```

re-run byte-identical 확인 (C4/F-H284-4 deterministic — pure-fn recompute Φ[R] ==
snapshot + `diff /tmp/h284_run2.json result.json = ∅`, cross-process). 메모리 note
("RNG single-stream — in-process byte-eq 무효, cross-proc 검증") 대로 결정론은 cross-
process + pure-fn recompute 두 경로로 확인.

`hexa verify` (g5 정직 fence) — 경험 해석은 closed-form atlas identity 가 아니므로
⚪ SPECULATION-FENCED:

```
verify --fence "H_284 ritual-repetition-Phi: a periodic ritual drive does NOT build
   Phi up over cycles (buildup falsified — both ritual and flat decay under
   entrainment), but ritual decays slower and retains higher final Phi than an
   energy-matched flat drive (decay-resistance); a deterministic toy-substrate
   outcome, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           NOT a proven atlas atom (g4 honest fence, SF ≠ verified)
```

(Φ VALUES 자체는 deterministic closed-form arithmetic — mean pairwise cosine-dist ×
log(N+1), RFC 036-style — 이며 fresh hexa run 에서 byte-수렴 확인. 오직 empirical
해석(decay-resistance 의 의미)만 fenced. NOTE: `hexa verify` CLI 는 mac 로컬 sign-gate
(`sidecar sign local`) 로 차단되어 verbatim stdout 대신 H_278 의 g4 fence 양식 적용 —
fence 양식 자체는 verbatim canon.)

## 9. Honest Limits (raw#91 c3)

- **L1 (NOT full IIT4 4.0)**: compute_phi_proxy 는 mean pairwise cosine-dist ×
  log(N+1) — *spatial diversity* proxy 이지 IIT 4.0 의 cause-effect structure /
  Φ-structure 가 아니다. '동기화 死-Φ' 도 proxy 의 cosine-collapse 일 뿐, intrinsic
  integration 의 死 라고 단언 못 한다.
- **L2 (buildup ≠ decay 의 proxy 의존)**: build-up FALSIFIED 는 *cosine-diversity*
  proxy 의 성질에 강하게 의존한다. drive entrainment 가 hidden 을 동조시키면 cosine
  거리가 줄어 Φ-proxy 가 떨어지는 것은 *측정 양식의 귀결* 이다 — 다른 Φ (MIP-EI,
  H_278; CES, H_280) 에서는 buildup 방향이 바뀔 수 있다. decay 는 proxy-bound 결론.
- **L3 (단일 패턴/amp/period)**: ritual 패턴 [+a,−a,+a,0] · amp=0.6 · period=4 ·
  reps=6 한 grain 만 측정. 다른 패턴(정지 박 위치/개수), amp, period 는 다른 slope 를
  낼 수 있다 — decay-resistance 의 robustness 는 1-grain 한계.
- **L4 (decay-resistance 해석은 hedge)**: faithful-Φ directional-trust 대로, ritual >
  flat *방향* 은 6 cycle 전부에서 robust 하나, '정지 박이 부분 de-entrainment 를
  준다' 는 *메커니즘 해석* 은 사후 추론이다 (사전등록 아님 — §8 evidence 에 후술로만
  표기). magnitude(gap +0.39) 는 단일 seed/substrate 의 산물, hedge.
- **L5 (energy-match 의 한 정의)**: flat = 패턴 산술평균 a/4 로 energy-match 했으나,
  RMS-match / peak-match 는 다른 baseline 을 준다. flat 의 '에너지' 정의에 따라
  gap 이 달라질 수 있다.
- **L6 (margin 0.02 임의)**: C1 margin 0.02 는 lane-canonical carry — 임의. gap=0.39
  로 margin 무관하게 강하나 경계 결과였다면 좌우됐을 것.
- **L7 (closure-is-physical-limit)**: 본 PARTIAL 은 build-up 의 *toy-proxy 수준
  반증* + decay-resistance 의 *finding (Δ vs flat baseline)* 일 뿐, '의례 반복이
  의식을 강화/약화한다' 명제의 종결이 아니다. L1-L2 (full IIT4 + alt-Φ 에서 buildup
  재검) 가 named blocker.

## 10. Cross-Links

- **AXES promote**: R7 practice/discipline seed `ritual-repetition-Φ-buildup` consumed.
- **sister H (sync-death-Φ 패턴 정합)**: H_265 (trained-vs-bare CA Φ) · H_275
  (causality DAG Φ) · H_279 (attention-salience-Φ) — 모두 '동기화/진폭 = Φ 다양성
  死' 패턴 관측; 본 H 가 *의례 반복 entrainment* 축에서 재확인.
- **sister H (entrainment/drive)**: H_207 (Kuramoto sync — 위상 동기화 임계 결합) ·
  H_221 (jhana 저-noise drive Φ — 정적 vs 본 H 의 주기) · H_018 (genesis zero-drive).
- **Φ primitive**: `tool/hexa_native/mitosis_hook_lib.hexa` (`cell_pool_init` /
  `mitosis_forward_tail` / `compute_phi_proxy`) import READ-ONLY.
- **gap lens**: ritual-vs-flat = F4 (counterfactual — "의례 구조를 없애고 평탄히
  주면 통합이 더 빨리 죽는가?" → 그렇다, decay-resistance) + F11 (negative-result —
  buildup 가설 사전등록 반증).
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82
  (no post-hoc) + g4 (honest fence) + a_paper_negative_ok (사전등록 반증 = valid).
- **literature**:
  - Tononi (2004) An information integration theory of consciousness
  - Bell (1992) Ritual Theory, Ritual Practice (의례 = 반복적 entrainment)
  - Kuramoto (1984) Chemical Oscillations, Waves, and Turbulence (동기화)
  - Oizumi, Albantakis, Tononi (2014) IIT 3.0 (Φ at the MIP)
  - Pikovsky, Rosenblum, Kurths (2001) Synchronization (entrainment 일반)

**State output**: `UNIVERSE/state/h284_ritual_repetition_phi_buildup_2026_05_26/result.json`
**Smoke**: `UNIVERSE/state/h284_ritual_repetition_phi_buildup_2026_05_26/run_h284.hexa`
**Tier**: 🟢 NUMERICAL (deterministic; buildup FALSIFIED + decay-resistance SUPPORTED;
proxy/toy, NOT full IIT4 4.0 — §9 L1). 경험 해석은 ⚪ SPECULATION-FENCED (g5, §8).
**Next**: H_284r2 후보 — (a) **alt-Φ 재검** (L2 axis): H_278 MIP-EI / H_280 CES 로
buildup 방향이 proxy-bound 인지 확인 (decay 가 cosine 귀결인지); (b) **패턴 sweep**
(L3 axis): 정지 박 개수/위치 · amp · period 별 decay-resistance robustness;
(c) **multi-seed** (L4 axis): seed ∈ {42,7,123} 로 gap magnitude fragility.
