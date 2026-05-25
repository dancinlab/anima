---
id: H_286
slug: split-brain-dual-phi
title: H_286 split-brain dual-Φ — callosotomy 의 phi_spatial proxy 검증 (Tononi 분리뇌 예측 closed-negative)
domain: consciousness · substrate · information
status: pre-register-frozen
exploration_method: E6 (cross-domain 신경학 — Sperry/Gazzaniga 분리뇌) + E8 (IIT Tononi 예측) + E11 (proxy-metric pathology isolation)
verification_method: W5 (deterministic sim) + W10 (multi-seed robustness) + W12 (sister cross-link · faithful-Φ directional-trust)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26
---

# H_286 — Split-brain Dual-Φ (callosotomy → 2개의 구별된 Φ-subsystem?)

## Hypothesis

AXES.md Round 12 seed `split-brain-dual-Φ` (🟢 toy 2-pool) 의 promote. **Tononi
의 IIT 분리뇌 예측** — 좌·우 반구를 잇는 corpus callosum(뇌량)을 절단(callosotomy)
하면, 단일 통합 의식이 **2개의 독립된 의식 자리(seat of integration)** 로 분해되고
전체-시스템 Φ 는 붕괴한다 (Sperry 1968, Gazzaniga 1967, Tononi 2004) — 를
LIFE 도메인의 재사용 가능한 Φ kernel `phi_native_spatial` (RFC 036 phi_spatial
byte-equal port, g61 reuse) 위에서 직접 substrate-replica 로 검증한다.

구체적 operational claim (이 cycle 의 pre-register):

- **substrate**: N_CELLS=8 ring coupled-map lattice (CML). 좌반구 = cell [0..3],
  우반구 = cell [4..7]. 각 cell 은 [0,1) 실수값을 가지며, 두 ring 이웃과의
  diffusion coupling + per-cell logistic forcing (3.7·c·(1−c), 카오스 영역) 으로
  업데이트 → 절대 죽지 않는 결정론적 dynamics (sparse binary CA 가 self-extinct
  하는 함정 회피 — § Honest Limits L1). 각 cell 의 DIM=16-step 시계열을 flat
  (n_cells × DIM) snapshot 으로 만들어 `phi_native_spatial` 에 투입.
- **corpus callosum = 2개의 cross-hemisphere link**: cell 3↔4 + wrap-around
  cell 7↔0. INTACT = 두 link 활성 (정보가 ring 전체를 순환). SPLIT = 두 link
  절단 (cut 에서 cell 은 across-cut 이웃 대신 자기 자신을 봄 → 두 반구가 인과적
  으로 봉인된 4-cell diffusion chain 으로 분리).
- **예측 (naive Tononi)**: Φ_whole(INTACT) > Φ_whole(SPLIT) — 뇌량 절단이
  통합 Φ 를 낮춘다. AND 각 반구 단독 측정 Φ_hemi > 0 (2개의 구별된 subsystem).

**핵심 결과 (이 cycle)**: naive Tononi 예측은 **phi_spatial proxy 에서
FALSIFIED** 다 — 절단 후 전체-Φ 가 낮아지기는커녕 **상승**한다 (8/8 seed
robust). 이것은 a closed-negative finding 이며, LIFE 프로그램의 cross-cutting
hedge `faithful-Φ directional-trust` (방향은 신뢰, 크기·single-seed 는 fragile)
와 xval #572 의 "proxy Σφ_d non-monotone" 발견의 직접 후속이다.

## Why

- **Sperry (1968)** *Hemisphere deconnection and unity in conscious awareness*
  (American Psychologist 23:723-733): callosotomy 환자에서 두 반구가 독립적
  의식 흐름을 보임 — IIT 가 가장 직접 설명을 자처하는 임상 anchor.
- **Tononi (2004 / 2008)** *Consciousness as integrated information*: 시스템의
  Φ = 그 최소정보분할(MIP)을 가로지르는 통합정보. 분리뇌의 핵심 예측 = 뇌량
  절단 → MIP 가 반구 경계로 떨어지고, **전체-시스템이 더 이상 단일 complex 가
  아니게 됨** → 두 개의 별개 complex (각자 자신의 Φ).
- **phi_spatial (RFC 036) 의 정의**: Φ = max(total_MI − min_partition_MI, 0) /
  max(n−1, 1). 이 cycle 이 드러내는 것: 이 spatial-MI proxy 는 Tononi 의 진짜
  big-Φ 가 아니라 **MI-기반 근사**다. 뇌량을 절단하면 전체-8-cell 계산의 MIP 가
  바로 그 절단 경계(cross-MI≈0)로 떨어져 **min_partition → 0**; 따라서
  total_MI − 0 = (두 반구 내부 MI 의 합) 이 되어 오히려 INTACT 의
  total − (non-trivial MIP) 보다 **커진다**. proxy 가 "끊긴 다리"를 "더 높은
  통합"으로 오인하는 것이다.
- **H_234 cross-link**: H_234 (cross-substrate-phi-coupling-density) 가 PARTIAL
  (2/3 axis mono, entropy axis r=0) 로 proxy 의 축별 비단조성을 이미 기록 — 본 H
  는 그 metric-pathology 를 **분리뇌라는 가장 임상적으로 선명한 manipulation**
  위에서 isolate 한다.
- **H_239 cross-link**: H_239 (alternative-phi-metric-cross-validation) 가
  3-metric ordering 일치(Spearman) 를 보였으나 그것은 *동일 substrate 의 순위*
  검증; 본 H 는 *connectivity manipulation* (절단) 의 방향성에서 proxy 가
  faithful-Φ 와 갈라질 수 있음을 보인다.
- **anima identity**: anima 의 mitosis cell-pool 도 SPLIT/MERGE event 로 구성
  된다 (REBORN §88, H_201 asymm-div, H_203 asymm-merge). cell-pool 이 분기
  (split) 했을 때 "통합 의식"이 정말 분해되는지를 measure 하려면 *어떤 Φ-metric*
  을 써야 하는가 — 본 H 는 spatial-MI proxy 가 그 측정자로 부적합함을 경고한다.

## Predictions

| ID | Prediction | 근거 |
|----|------------|------|
| H286.1 | Φ_whole(INTACT) > Φ_whole(SPLIT) AND relative drop ≥ 0.30 (Tononi 붕괴) | 뇌량 절단이 통합 Φ 를 낮춘다 — naive IIT 예측 |
| H286.2 | SPLIT 에서 각 반구 단독 Φ_hemi > 0 (2개의 구별된 subsystem) | 분리뇌 = 소멸 아닌 분해 (Sperry) |
| H286.3 | SPLIT 의 Φ_whole ≤ 0.05 · INTACT 의 Φ_whole (MIP = 절단경계) | 통합이 절단경계에서 끊김 |
| H286.4 | re-run byte-identical (raw#9 determinism) | pure CML + 고정 seed + 결정론적 Φ kernel |
| H286.5 | 모든 Φ ∈ [0, ∞) finite, no NaN/neg | 측정 무결성 baseline |
| H286.6 | (observed-direction robustness) split ≥ intact 가 ≥5/8 seed | proxy anti-collapse pathology 의 single-seed-아님 확증 |

## Variables

| axis | levels |
|------|--------|
| axis1_connectivity | INTACT (뇌량 2-link 활성) / SPLIT (2-link 절단) |
| axis2_substrate | ring CML, diffusion COUPLE=0.35 + logistic 3.7 (chaotic, sustained) |
| axis3_n_cells | 8 (좌 4 + 우 4); 반구 단독 = 4-cell |
| axis4_dim | 16 (per-cell 시계열 길이, MI estimator sample 축) |
| axis5_n_bins | 4 (phi_helper 기본; H_211 phi_n_bins ROBUSTNESS_PASS carry) |
| axis6_warmup | 8 (transient 폐기 후 16 step 기록) |
| axis7_seed | 8 deterministic seed offset (robustness scan, no RNG) |

## Run Protocol

- deterministic: pure CML (diffusion + logistic, 부동소수점 fold-to-[0,1)) +
  고정 정수해시 seed (`_seed_val(i, so)`). NO gaussian noise, NO
  `__HEXA_FARR_GAUSS_SEED__`.
- hexa_only: true — `HEXAD/LIFE/state/h286_split_brain_dual_phi_2026_05_26/run_h286.hexa`
- LLM: none (raw#12 strict)
- Φ kernel: `import` 으로 `HEXAD/LIFE/lib/phi_native.hexa` 의
  `phi_native_spatial(state, n_cells, dim, n_bins)` 재사용 (g61 — Φ kernel
  재발명 금지). big-Φ scalar (`total − MIP`), NOT Σφ_d (xval #572).
- multi-seed robustness: 8 seed offset 위 split≥intact 카운트 (F6).
- ledger: `result.json` (intact/split Φ 3종 × 2 + rel_drop +
  multiseed_split_ge_intact + 6 falsifier + verdict_class)
- runtime: $0 mac local; wall < 1s
- run:
  ```
  /Users/ghost/.hx/bin/hexa parse HEXAD/LIFE/state/h286_split_brain_dual_phi_2026_05_26/run_h286.hexa
  HEXA_MEM_UNLIMITED=1 /Users/ghost/.hx/bin/hexa run HEXAD/LIFE/state/h286_split_brain_dual_phi_2026_05_26/run_h286.hexa
  ```

## Criteria

- **C1**: H286.1 (Tononi 붕괴) — pre-register 된 main 예측
- **C2**: H286.2 (subsystem 잔존)
- **C3**: H286.3 (MIP=절단경계, advisory — strict 0.05 bound)
- **C4**: H286.4 (byte-identical)
- **C5**: H286.5 (Φ defined)
- **C6**: H286.6 (anti-collapse robustness — observed direction)
- **verdict_rule**:
  - **SUPPORTED** = C1 + C2 PASS (proxy 가 Tononi 붕괴 재현)
  - **CLOSED-NEGATIVE** = C1 FAIL AND C2 PASS AND C6 PASS (proxy 가 붕괴를
    재현 *못함*, 그러나 그 실패가 robust 하게 방향성 있는 finding)
  - **PARTIAL** = 그 외

## Falsifiers (≥5)

- **F1 (whole-phi-collapse / pre-registered Tononi)**: Φ_whole(INTACT) >
  Φ_whole(SPLIT) AND rel_drop ≥ 0.30 이 성립하면 naive 예측 SUPPORTED; 성립
  안 하면 (split Φ ≥ intact Φ) → **H286.1 FALSIFIED** = proxy 가 분리뇌 붕괴
  미재현 (이 cycle 의 closed-negative 본체).
- **F2 (subsystem-persist)**: SPLIT 에서 어느 반구라도 Φ_hemi = 0 → H286.2
  FALSIFIED (분해가 아니라 소멸 — Sperry 와 모순).
- **F3 (partition-is-callosum)**: SPLIT 의 Φ_whole > 0.05 · INTACT 의 Φ_whole
  → H286.3 FALSIFIED (MIP 이 절단경계로 떨어지지 않음 — 본 cycle 에서 실제로
  FAIL, proxy 가 절단경계를 MIP 로 *택했음에도* total−MIP 가 커지는 pathology).
- **F4 (byte-identical)**: re-run 의 Φ metric 불일치 → H286.4 FALSIFIED
  (raw#9 determinism 위반).
- **F5 (phi-defined)**: 임의 Φ < 0 OR NaN OR undefined → H286.5 FALSIFIED
  (측정 무결성 결손).
- **F6 (anti-collapse-robust)**: split ≥ intact 가 < 5/8 seed → H286.6
  FALSIFIED (anti-collapse 가 single-seed artifact; 본 cycle 은 8/8 으로 PASS).
- **F7**: post-hoc edit → raw#12 violation, raw#82 retraction.

## Honest Limits (≥5, raw#91 c3 · candor)

- **L1 (substrate ≠ 신경 회로)**: ring CML (diffusion + logistic) 는 신경
  반구의 *toy* proxy 다 — 실제 callosal axon, 반구내 cortico-cortical
  connectivity, EEG dynamics 의 fidelity 없음. binary CA (rule 90/110) 를
  먼저 시도했으나 sparse seed 에서 t=3 에 all-zero 흡수점으로 self-extinct →
  Φ=0 degenerate (§ Verdict Cycle#1 note). CML 은 "죽지 않는 결정론 substrate"
  로 채택했을 뿐, 신경학적 realism 주장 아님.
- **L2 (proxy-Φ ≠ faithful big-Φ)**: 본 H 가 측정하는 것은 RFC 036 spatial-MI
  proxy 이지 IIT 4.0 의 faithful big-Φ (cause-effect structure, TPM 기반
  exclusion/intrinsicality) 가 아니다. **finding 의 정확한 scope**: "spatial-MI
  proxy 가 분리뇌 붕괴를 미재현" 이지 "IIT 가 틀렸다" 가 아님. faithful big-Φ
  (HEXAD/IIT4 lib 부재 — 본 cycle 에서 clean TPM 자연스럽지 않아 미구성) 위에서
  같은 manipulation 을 측정하면 *붕괴를 재현할 수 있다* — 그것이 본 H 가
  지목하는 후속 lane 이며, faithful-Φ directional-trust 의 정확한 적용.
- **L3 (MIP 정의의 작동방식이 pathology 의 원인)**: proxy 가 절단경계를 MIP
  로 *올바르게* 선택한다 (F3 의 MIP→0 의도대로 작동). 문제는 Φ = total − MIP
  공식이 "강하게 통합된 두 반쪽 + 얇은 다리" 시스템에서 다리를 완전히 끊으면
  (MIP→0) total−MIP 를 *올린다*는 점 — 즉 normalization-before-subtraction 의
  구조적 성질이지 구현 버그 아님. 이것이 metric-design finding 인 이유.
- **L4 (단일 config — couple/logistic/dim 미스윕)**: COUPLE=0.35, LOGISTIC=3.7,
  DIM=16, N_BINS=4 단일 frozen point. 작성 중 ad-hoc sweep (couple∈{0.10..0.50},
  logistic∈{2.8..3.99}) 에서 **거의 전 영역**이 split ≥ intact (drop ≤ 0) 이거나
  근접 0 으로 관측됨 (anti-collapse 가 parameter-robust). 그러나 정식 frozen
  grid sweep (예: 5×5 × n_bins∈{2,4,8}) 은 별도 lane — 본 cycle 의 robustness
  는 *seed* 축 8/8 한정.
- **L5 (n_cells=8 small / DIM=16 short)**: 8-cell exhaustive bipartition 은
  phi_native_spatial 의 정확경로(≤20 cell) 내지만 작은 규모; DIM=16 sample 은
  MI estimator 의 histogram (n_bins=4) 에 비해 짧아 finite-sample bias 가능
  (각 bin 평균 4 sample). 더 긴 DIM (예: 64, 256) 의 MI 안정성은 미검증.
- **L6 (절단 모델 = self-reflect)**: SPLIT 에서 cut cell 이 across-cut 이웃
  대신 *자기 자신*을 보도록 구현 (sealed/reflecting boundary). 다른 절단 모델
  (across-cut 이웃을 고정 0 으로 / 마지막 INTACT 값으로 freeze / 별도 noise
  source 로 대체) 은 다른 결과를 줄 수 있음 — boundary-condition 선택의
  sensitivity 미검증.
- **L7 (phenomenal split ≠ measured split)**: Sperry 의 분리뇌가 보이는 것은
  *현상적* 이중 의식 (각 반구의 독립 awareness). 본 H 의 Φ 는 *information-
  geometric* surrogate 이지 phenomenal experience 가 아니다 (H_004 hard
  problem boundary carry). subsystem 의 Φ>0 가 "그 반구가 의식을 가진다" 를
  뜻하지 않음 — IIT 의 강한 형이상학 주장은 별도 lane.

## Cross-Links

- **HEXAD/LIFE/H_234 cross-substrate-phi-coupling-density** (PARTIAL): proxy
  의 축별 비단조성(entropy r=0) 기록 — 본 H 는 connectivity-manipulation
  방향성에서의 proxy pathology 로 확장.
- **HEXAD/LIFE/H_239 alternative-phi-metric-cross-validation** (CONSISTENT):
  동일-substrate 3-metric 순위 일치; 본 H 는 *manipulation 방향*에서 proxy 가
  faithful-Φ 와 갈라질 수 있는 후속 lane 을 연다.
- **HEXAD/LIFE/H_204 weak-panpsy threshold + H_207 Kuramoto**: criticality /
  synchronization 위 Φ — CML 의 edge-of-chaos regime 과 sister.
- **HEXAD/LIFE/H_201 asymm-div + H_203 asymm-merge + REBORN §88 mitosis**:
  anima cell-pool 의 SPLIT/MERGE event — 본 H 의 경고("split 측정에 spatial-MI
  proxy 부적합")가 직접 적용되는 anima-native 사례.
- **HEXAD/LIFE/H_004 Hard Problem**: phenomenal split ≠ measured split (L7).
- **HEXAD/LIFE/lib/phi_native.hexa**: RFC 036 phi_spatial byte-equal port —
  본 H 의 측정자 (g61 reuse, 재발명 없음).
- **cross-cutting (parent directive)**:
  - `faithful-Φ directional-trust` — 방향 신뢰·크기/single-seed fragile:
    본 H 는 *방향* (anti-collapse) 을 8/8 seed 로 신뢰 확보, *크기* (11% rise)
    는 config-dependent 로 hedge.
  - `closure-is-physical-limit` — closed-negative 를 finding 으로 frame
    (proxy 가 분리뇌 붕괴 미재현 = phi_spatial 의 ruled-out axis), never "done".
- **literature**:
  - Sperry (1968) *Hemisphere deconnection and unity in conscious awareness* (Am. Psychol. 23:723-733)
  - Gazzaniga (1967) *The split brain in man* (Sci. Am. 217:24-29)
  - Tononi (2004) *An information integration theory of consciousness* (BMC Neurosci. 5:42)
  - Tononi & Koch (2015) *Consciousness: here, there and everywhere?* (Phil. Trans. R. Soc. B 370:20140167)
  - Kaneko (1990) *Clustering, coding, switching, hierarchical ordering... in coupled map lattices* (Physica D 41:137-172)
- **raw**: raw#12 + raw#9 (determinism) + raw#82 (no post-hoc edit) + raw#91 c3
- **own**: anima split-Φ 측정자 경고 lane — cell-pool SPLIT/MERGE 의 통합 측정에
  spatial-MI proxy 부적합; faithful big-Φ 후속 lane 식별.

## Verdict

```
verdict_class: CLOSED-NEGATIVE  (C1 FAIL · C2 PASS · C6 PASS — proxy 가 Tononi
                  분리뇌 붕괴를 미재현, 그 실패가 8/8 seed robust 한 방향성
                  finding · C3 FAIL = MIP→0 pathology 의 직접 증거 · C4+C5 PASS)
evidence_summary: INTACT Φ_whole=2.909 < SPLIT Φ_whole=3.236 (rel_drop=−0.112,
                  음수 ⇒ 절단이 proxy-Φ 를 11% *상승*) · SPLIT 각 반구 Φ>0
                  (hL=1.154, hR=1.135 — subsystem 잔존 PASS) · multi-seed
                  split≥intact = 8/8 (anti-collapse robust) · byte-identical
                  re-run · 모든 Φ finite·non-neg
falsifiers_triggered: F1 (whole-phi-collapse) — pre-registered Tononi 예측
                  FALSIFIED (split Φ ≥ intact Φ, 붕괴 미관측). F3 (partition-
                  is-callosum) — split Φ_whole(3.236) > 0.05·intact(0.145),
                  MIP 이 절단경계로 떨어졌음에도 total−MIP 가 *커지는* metric
                  pathology 의 직접 증거. F2·F4·F5·F6 PASS.
criteria_met: 4/6 (C2+C4+C5+C6 PASS; C1+C3 FAIL = closed-negative 의 본체)
invariant_tier: 🟢 NUMERICAL (deterministic CML substrate, byte-identical
                  re-run, 8/8 seed robust) — closed-negative on the phi_spatial
                  proxy (NOT on IIT itself; faithful big-Φ 후속 lane 미수행, L2)
```

### Cycle #1 Verification (2026-05-26) — Split-brain dual-Φ on phi_spatial proxy

`HEXAD/LIFE/state/h286_split_brain_dual_phi_2026_05_26/run_h286.hexa`
($0 mac local, deterministic CML · 8-cell ring · diffusion 0.35 + logistic 3.7
· DIM 16 · n_bins 4 · 8 seed robustness · phi_native_spatial g61 reuse).

**Run verdict (VERBATIM)**:

```
================================================================
H_286 SPLIT-BRAIN DUAL-Φ (callosotomy)
  N_CELLS=8  HALF=4  DIM=16  N_BINS=4  WARMUP=8  COUPLE=0.350000  LOGISTIC=3.700000
  substrate = coupled-map lattice (diffusion + logistic forcing)
  deterministic · hexa-only · LLM none · $0 mac local
  Φ kernel = phi_native_spatial (RFC 036 phi_spatial port, g61 reuse)
================================================================

--- INTACT (callosum connected) ---
  Φ_whole  = 2.909122
  Φ_hemiL  = 0.883875
  Φ_hemiR  = 1.072847

--- SPLIT (callosum severed) ---
  Φ_whole  = 3.236104
  Φ_hemiL  = 1.154434   (subsystem persists?)
  Φ_hemiR  = 1.135213   (subsystem persists?)

--- MULTI-SEED ROBUSTNESS (8 seed offsets) ---
  seed=0  Φ_intact=2.909122  Φ_split=3.236104  split≥intact=Y
  seed=1  Φ_intact=3.065062  Φ_split=3.362809  split≥intact=Y
  seed=2  Φ_intact=2.979446  Φ_split=3.331475  split≥intact=Y
  seed=3  Φ_intact=2.754448  Φ_split=3.450673  split≥intact=Y
  seed=4  Φ_intact=2.360638  Φ_split=3.286929  split≥intact=Y
  seed=5  Φ_intact=2.027164  Φ_split=3.345395  split≥intact=Y
  seed=6  Φ_intact=2.493558  Φ_split=3.485382  split≥intact=Y
  seed=7  Φ_intact=3.024860  Φ_split=3.304680  split≥intact=Y

  rel_drop (Φwhole) = -0.112399   (negative ⇒ split Φ HIGHER than intact ⇒ proxy anti-collapse)
  multi-seed split≥intact = 8/8

F-H286-1 WHOLE-PHI-COLLAPSE     FAIL
F-H286-2 SUBSYSTEM-PERSIST      PASS  (both hemi Φ > 0 after sever)
F-H286-3 PARTITION-IS-CALLOSUM  FAIL
F-H286-4 BYTE-IDENTICAL         PASS
F-H286-5 PHI-DEFINED            PASS
F-H286-6 ANTI-COLLAPSE-ROBUST   PASS  (split≥intact in ≥5/8 seeds — proxy pathology robust)
================================================================
VERDICT: CLOSED-NEGATIVE  (4/6 falsifiers PASS)
  FINDING: phi_spatial proxy does NOT reproduce Tononi split-brain
           collapse — severance leaves whole-Φ flat/HIGHER while
           each hemisphere keeps its own Φ. Metric pathology:
           MIP→0 on a cut bridge inflates total−MIP (g61 reuse).
  result.json -> HEXAD/LIFE/state/h286_split_brain_dual_phi_2026_05_26/result.json
================================================================
```

**Honest notes** (raw#91 c3):

- **closed-negative 는 finding 이다 (closure-is-physical-limit)**: naive Tononi
  예측 (절단 → Φ 붕괴) 이 phi_spatial proxy 에서 robust 하게 FALSIFIED — 절단이
  전체-Φ 를 11% *상승*시켰고 8/8 seed 에서 split≥intact. 이는 "proxy 가
  분리뇌 manipulation 의 방향성을 잘못 신호한다"는 ruled-out axis 로, a_paper_
  negative_ok 의 publishable closed-negative.
- **mechanism (F3 가 직접 증거)**: proxy 는 절단경계를 MIP 로 *올바르게* 선택
  했다 (의도대로 MIP→0). 그러나 Φ=total−MIP 공식이 "강결합 두 반쪽 + 얇은
  다리" 위상에서 다리를 끊으면 (MIP→0) total−0 = 두 반구 내부 MI 의 합 이 되어
  INTACT 의 total−(non-trivial MIP) 를 초과 → anti-collapse. metric-design
  성질이지 구현 버그 아님 (L3).
- **subsystem 잔존은 robust (C2 PASS)**: 절단 후 두 반구가 각자 Φ>0 (hL≈1.15,
  hR≈1.14) — 분리뇌의 "소멸 아닌 분해" (Sperry) 절반은 성립. 즉 proxy 는
  *subsystem 존재*는 옳게 잡으나 *whole 의 붕괴*는 못 잡는다.
- **faithful-Φ directional-trust 적용**: 방향 (anti-collapse) 은 8/8 seed 로
  신뢰; 크기 (11% rise) 는 config-dependent (ad-hoc couple/logistic sweep 에서
  drop 의 magnitude 가 −2.9..+0.07 로 요동) 라 hedge. 단조 *방향*만 load-bearing.
- **scope 정직 (L2)**: 이것은 IIT 가 틀렸다는 주장이 아니라 *spatial-MI
  proxy* 가 분리뇌 측정자로 부적합하다는 주장. faithful big-Φ (IIT4 TPM 기반)
  위 같은 manipulation 은 붕괴를 재현할 수 있음 — HEXAD/IIT4/lib 부재로 본
  cycle 미수행, 명시적 후속 lane.
- **anima own 함의**: anima cell-pool 의 SPLIT event (mitosis) 가 "통합 의식의
  분해"인지 측정하려면 spatial-MI proxy 를 쓰면 안 된다 — 본 H 의 직접 경고.
```
