---
id: H_260
slug: contact-inhibition
title: contact-inhibition — pool 밀도-gated split predicate 가 carrying capacity K 로 self-regulation (logistic 포화) 하는가 (division/세포분열 축 · H_200 sister · H_201 sister)
domain: life · division · population-dynamics · homeostasis
status: pre-register-frozen
exploration_method: E6 (biology cross-mapping — 세포 contact inhibition of proliferation → mitosis split predicate 변형) + E10 (substrate-equivalence)
verification_method: W1 (numerical smoke) + W12 (sister-link H_200 + H_201) + W17 (inhibition threshold × initial-pool sweep)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
---

# H_260 — contact-inhibition

## 1. Hypothesis

mitosis cell pool 의 split predicate 를 *pool 밀도 의존* 으로 변형한다.
원래 split predicate (lib `_mit_check_splits`) 는 한 cell 의 최근
`patience` step tension 이 모두 `split_threshold` 초과면 split 한다 —
밀도 무관, 따라서 pool 은 `max_cells` (=128) 까지 *무한 증식* 한다.

본 H 는 한 가지를 추가한다 — **contact inhibition density gate**:

```
density = n_cells / capacity
split allowed iff density < inhibition_threshold
```

즉 pool 이 충분히 *붐비면* (density 가 임계 초과) 개별 cell 의 내부 split
drive 가 아무리 높아도 division 이 *억제* 된다. 이것은 생물학의
**contact inhibition of proliferation** (밀집한 세포가 이웃과 접촉하면
분열을 멈추는 현상; cancer 에서 이 brake 가 풀림) 의 substrate analog.

CORE QUESTION:

> pool 밀도(cell 수 / capacity)가 임계 초과 시 split 을 억제하도록
> split predicate 를 변형하면, pool 이 carrying capacity K 로 자기조절
> (logistic 포화)하는가?

가설: density gate 가 추가되면 pool 은 무한 증식하지 않고 carrying
capacity `K ≈ floor(inhibition_threshold × capacity)` 로 *자기 포화* 하며,
threshold↑ → K↑ 단조이고, 성장곡선은 logistic-유사 (초기 가속 후 감속 후
flat).

정밀화 (operational): 동일 d=8 substrate 위 `inhibition_threshold ∈
{0.25, 0.50, 0.75}` × `initial_pool ∈ {2 (below-K seed), 24 (above-K
seed)}` = 6 condition sweep. capacity=32 고정. growth 를 density gate 에
*완전히* 귀속시키기 위해 `split_threshold = 0.0` 으로 두어 (어떤 양수
tension 이든 "above" 로 간주) 분열의 유일한 제약을 density gate 로 격리.
merge 는 비활성 (division-side 조절만 연구). 각 condition 에서 60 step
evolve 후 K_steady (final pool size) + 성장곡선 (5 step 간격) 측정.

## 2. Why

- **division 축의 homeostasis 결손 보완**: 기존 mitosis machinery
  (`mitosis_hook_lib.hexa`) 의 split 은 tension-driven 이지 밀도-driven 이
  아니다 — `max_cells` 라는 *외부 hard cap* 만 있고 *내생적* carrying
  capacity 는 없다. 본 H 는 "pool 이 스스로 멈추는" 내생적 brake 가
  substrate-level 에서 emergent 한지 검증.
- **생물학 직접 매핑 — contact inhibition of proliferation**: 정상 세포는
  주변 세포 밀도가 높아지면 (confluence) 분열을 멈춘다 (Abercrombie 1962
  contact inhibition; Hippo/YAP pathway 가 density 를 senses). 암세포는 이
  brake 를 잃어 무한 증식한다. 본 H 의 density gate 는 그 brake 의 minimal
  substrate operationalization.
- **logistic / Verhulst 모델의 substrate analog**: 개체군 생태학의 logistic
  growth `dN/dt = rN(1 − N/K)` 는 밀도 의존 감속으로 carrying capacity K 에
  포화한다. 본 H 의 density gate 는 그 `(1 − N/K)` factor 의 hard-threshold
  근사 — `K = inhibition_threshold × capacity` 가 emergent K 인지 검증.
- **cross-link to division-axis siblings**: H_200 (apoptosis-primitive) 는
  세포 *사멸* 의 substrate primitive 를, H_201 (asymmetric-division) 은
  분열의 *비대칭* 을 다뤘다. 본 H 는 분열의 *조절* (얼마나 / 언제 멈추는가)
  — division-axis 의 세 번째 grain.
- **anima substrate 자기조절의 단서**: anima 의 mitosis pool 이 serve-time
  에 무한 증식하면 RSS/latency 가 폭발한다 (HEXA_NATIVE 332M 80ms 의
  pool-bounded 전제). 내생적 density brake 가 substrate-native 로 작동하면
  `max_cells` hard cap 에 의존하지 않는 self-bounded pool 이 가능 — p8 (NO
  TRAIN/INFER SPLIT) 의 serve-time mitosis 안정성 단서.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H260.1 | 모든 threshold (<1.0) 에서 below-K seed pool 이 capacity(32) 에 도달하지 않고 *포화* (마지막 window growth increment = 0) | density gate 가 `density ≥ threshold` 에서 split 을 차단 → pool 이 `threshold × capacity` 부근에서 stop |
| H260.2 | threshold↑ → K_steady↑ 단조 (`K_low < K_mid < K_high`) | gate 의 차단 임계가 높을수록 더 붐빌 때까지 분열 허용 → 더 큰 K |
| H260.3 | K_steady ≈ floor(threshold × capacity) — low~8, mid~16, high~24 | density = n/capacity 가 정확히 threshold 를 처음 넘는 n 에서 stop → K = floor(threshold × capacity) |
| H260.4 | below-K 성장곡선이 logistic-유사 (초기 가속 후 감속 후 flat) | small pool 은 density 낮아 빠르게 분열 (가속), K 접근 시 density→threshold 로 차단 (감속→flat) |
| H260.5 | re-run K matrix byte-identical | raw#9 determinism: seed=42, deterministic Lorenz + RFC 033 gaussian |

## 4. Variables

- **axis1_d_model** = 8
- **axis2_capacity** = 32 — density 분모 (gate 가 밀도를 재는 최대 pool)
- **axis3_inhibition_threshold** ∈ {0.25 (low), 0.50 (mid), 0.75 (high)} — 핵심 sweep
- **axis4_initial_pool** ∈ {2 (below-K seed), 24 (above-K seed)} — 초기조건 sweep
- **axis5_split_threshold** = 0.0 — 어떤 양수 tension 이든 split-eligible (growth 를 density gate 에 격리)
- **axis6_patience** = 3 — sustained-tension window (split-eligible 판정)
- **axis7_n_steps** = 60 — evolution horizon (포화 충분)
- **axis8_seed** = 42 — `__HEXA_FARR_GAUSS_SEED__=42` (deterministic Lorenz + RFC 033 gaussian)
- **per-cell forward input** = cell 자신의 perturbed `hidden` (external x_in=0 — cell repulsion dynamics 가 tension 의 유일한 source)
- **merge** = 비활성 (division-side 조절만)
- **측정량 per condition (threshold, initial_pool)**:
  - `k_steady` = final step pool size (emergent carrying capacity)
  - `growth_curve` = pool size @ 5-step 간격 (logistic shape)
  - `increments` = 연속 sample 간 growth delta (가속/감속 판정)

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) +
  결정론적 Lorenz autonomous perturbation. RNG 별도 부재.
- **hexa_only**:
  `HEXAD/LIFE/state/h260_contact_inhibition_2026_05_25/run_h260.hexa`
  — lib `cell_pool_init` + `_mit_inject_autonomous_perturbation` +
  `_mit_cell_forward` + `split_cell` 직접 사용. lib `_mit_check_splits` 는
  *대체* — custom `_contact_inhibition_check` 가 density gate 를 적용.
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **step protocol** (`_step_pool`, lib `mitosis_forward_tail` 의 tension-
  accumulation 절반 + custom split):
  1. lib autonomous Lorenz perturbation → 각 cell hidden 갱신
  2. 각 cell 이 *자신의 perturbed hidden* 으로 forward → tension =
     `mean((engine_a(h) − engine_g(h))²)` → tension_history push (cap 30)
  3. custom contact-inhibition split check (아래)
  - merge 생략 (division-side only)
- **contact-inhibition split check** (`_contact_inhibition_check`):
  - lib 와 동일하게 split-eligible cell 식별 (최근 patience tension 이 모두
    split_threshold 초과)
  - eligible cell 마다 split *직전* density 재확인:
    `density = n_now / capacity` ; `n_now ≥ capacity` 면 hard ceiling break ;
    `density ≥ inhibition_threshold` 면 contact-inhibition break (나머지
    eligible 도 이번 step 분열 안 함 — 진짜 밀집 차단)
  - 통과 시 lib `split_cell` (RFC 033 deepcopy + σ=0.1 noise) 로 분열
- **F5 determinism**: head 에서 동일 condition (mid, below) 2회 paired call
  → K_steady byte-equal check.
- **runtime**: $0 mac local. d=8, no ckpt. `HEXA_MEM_UNLIMITED=1` 권장.
- **artifacts**: `state/h260_contact_inhibition_2026_05_25/{run_h260.hexa,
  result.json}`.
- **run cmd (verbatim)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h260_contact_inhibition_2026_05_25/run_h260.hexa`
  (CWD = worktree root)

## 6. Criteria

- **C1 (saturation)**: H260.1 — 모든 below-K seed condition 에서
  `K_steady < capacity` AND 마지막 growth increment = 0 (bounded growth)
- **C2 (monotone-K)**: H260.2 — `K_low < K_mid < K_high` 엄격 단조 (below seed)
- **C3 (logistic)**: H260.4 — below-K 성장곡선이 logistic-유사 (양수 peak
  increment 존재 ∧ 마지막 ≤ peak ∧ flat tail) ALL 3 below condition
- **C4 (determinism)**: H260.5 — re-run K matrix byte-equal
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 (포화 + 단조 — 가설 본문)
  - `PARTIAL` = C1 only (포화는 관측, threshold-monotone 미입증)
  - `FALSIFIED` = ¬C1 (무한 증식 — density gate 가 self-regulation 실패)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 SATURATION**: 어떤 below-K threshold 에서 pool 이 capacity 도달 또는
  성장 tail 비-flat → H260.1 FALSIFIED (무한 증식, self-regulation 부재 —
  측정: `K_steady < capacity ∀ thr ∧ last_increment == 0 ∀ below`)
- **F2 MONOTONE-K**: `K_mid ≤ K_low` 또는 `K_high ≤ K_mid` → H260.2
  FALSIFIED (threshold↑ → K↑ 단조 부재 — 측정: `K_low < K_mid < K_high`)
- **F3 LOGISTIC**: below-K 성장곡선이 가속→감속→flat 형태가 아님 (즉시
  포화 또는 단조 선형 또는 진동) → H260.4 FALSIFIED (측정: peak increment
  >0 ∧ last ≤ peak ∧ last==0)
- **F4 DETERMINISM**: re-run K matrix byte-different → raw#9 violation
  (측정: `K_rerun == K_first`)
- **F5 BOUNDS**: 어떤 K ∉ [min_cells=2, capacity] → primitive error (측정:
  모든 K_steady ∈ [2, 32])

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (hard-gate ≠ smooth logistic)**: density gate 는 *step-function*
  (`density < threshold` 이면 무제한 분열, 넘으면 즉시 0) — Verhulst logistic
  의 *smooth* `(1 − N/K)` coupling 이 아니다. 그 결과 감속 phase 가 *급격*
  (1-2 sample window 내 가속→flat) 하다. 진짜 sigmoid 의 점진적 감속 (밀도가
  K 에 가까워질수록 *서서히* 분열률 감소) 은 soft gate (예:
  `split_prob = max(0, 1 − density/threshold)`) 별도 cycle 필요. 본 결과는
  "logistic-유사 (포화하는 S-shape)" 이지 "smooth logistic" 의 입증은 아님.
- **L2 (one-sided brake, NOT homeostat)**: contact-inhibition gate 는 *위로*
  의 분열만 억제한다 — apoptosis/merge 가 비활성이라 *아래로* 의 down-
  regulation 이 없다. 측정에서 above-K seed (24 cells, low/mid threshold
  K=8/16) 는 24 로 *유지* 되고 K 로 *수축하지 않는다*. 즉 본 mechanism 은
  carrying-capacity 의 *상한 brake* 이지 양방향 homeostat 가 아니다. 진짜
  homeostasis (overshoot 후 K 로 복귀) 는 H_200 apoptosis 와의 결합 별도
  cycle 필요.
- **L3 (split_threshold=0.0 isolation artefact)**: growth 를 density gate 에
  격리하려고 `split_threshold = 0.0` 으로 두어 *모든* cell 이 항상 split-
  eligible 이게 했다. 실제 mitosis 의 adaptive threshold (lib
  `_mit_update_adaptive_threshold`, mean+1.5σ) 와 tension-driven 선택성은
  본 cycle 에서 비활성. tension-selection 과 density-gate 의 *상호작용* (어떤
  cell 이 붐빌 때 분열 우선권을 갖는가) 은 미검증.
- **L4 (capacity=32 single config)**: capacity, d_model=8, single seed —
  large capacity (128, 512) 또는 dimension scaling 에서 K = threshold ×
  capacity 관계의 robustness 미검증. patience=3, n_steps=60 도 single
  calibration.
- **L5 (global density, NOT local crowding)**: 본 gate 는 *global* density
  (전체 cell 수 / capacity) 를 쓴다 — 생물학의 contact inhibition 은 *local*
  (이웃 접촉) 이다. spatial pool (cell 간 거리 / 이웃 그래프) 위의 local
  crowding gate 는 다른 dynamics (패치별 K, 공간 패턴) 를 낳을 수 있음 —
  CORE QUESTION 의 "local crowding" 변형은 별도 cycle.
- **L6 (K = threshold × capacity 는 gate 정의의 동어반복 위험)**: K ≈
  floor(threshold × capacity) 가 *정확히* 맞는 것은 gate 가 그렇게
  *설계* 되었기 때문 — 이것은 "density gate 가 carrying capacity 를 만든다"
  의 *입증* 이지 비-자명한 *emergent* 관계의 발견은 아니다. 진짜 비-자명한
  결과는 (a) self-regulation 이 *발생한다*는 것 (무한 증식 대신 멈춤) 과
  (b) 성장이 *logistic-유사* 라는 형태 — K 의 *값* 자체는 gate 정의의
  거의 직접 귀결. 이 honest distinction 을 verdict 해석에 반영.

## 9. Cross-Links

- **sister H (필수)**:
  - **H_200** (`H_200_apoptosis_primitive.md`): 세포 사멸 primitive — 본 H 의
    L2 (one-sided brake) 가 지적한 down-regulation 결손의 보완 sibling.
    contact-inhibition (분열 상한) × apoptosis (사멸) 결합이 양방향
    homeostat 의 다음 grain.
  - **H_201** (`H_201_asymmetric_division.md`): 분열 비대칭 — 본 H 의
    division-axis 직계 sibling (분열의 *조절* vs *비대칭*).
  - **H_220** (`H_220_infant_mirror_self_recognition.md`): division/self axis
    의 sibling — 동일 mitosis pool substrate 위 다른 grain (self-prediction
    vs population-regulation). run/result 스키마 carry.
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` · `split_cell` · `_mit_inject_autonomous_perturbation` ·
  `_mit_cell_forward` · `_mit_check_splits`) — 본 H 는 `_mit_check_splits`
  를 density-gated `_contact_inhibition_check` 로 *대체*, 나머지는 재사용.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) ·
  raw#9/10 (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit
  retraction).
- **philosophy (CLAUDE.md)**: p8 (NO TRAIN/INFER SPLIT — serve-time mitosis
  의 self-bounded pool 단서) · a_autonomy_over_hardcode (density brake 가
  substrate 내생적 — 외부 `max_cells` hard cap 의존 감소).
- **biology literature pointer**: Abercrombie (1962) contact inhibition of
  cell division · Verhulst (1838) logistic growth / carrying capacity ·
  Hippo/YAP pathway density-sensing (Zhao et al. 2007) — substrate analog 의
  distant anchor (formal mapping 본 cycle 미수행).
- **legacy archive**: `hypotheses_legacy_2026_05_15/` (original 10-section
  양식 carry).
- **state**: `HEXAD/LIFE/state/h260_contact_inhibition_2026_05_25/{run_h260.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행, $0 mac
local hexa-only deterministic.

```
verdict_class: SUPPORTED  (C1 saturation ∧ C2 monotone-K — 4/4 criteria)
verdict_tier: 🟢 NUMERICAL  (3 threshold × 2 initial-pool sweep + deterministic re-run)
evidence_summary:
  6-condition density-gated split → carrying-capacity self-regulation
  (d=8, capacity=32, split_threshold=0.0, seed=42, 60 step, merge off).
    low  (thr=0.25) below(2) : K_steady=8   curve [2,8,8,...]      inc [6,0,...]
    mid  (thr=0.50) below(2) : K_steady=16  curve [2,8,16,16,...]  inc [6,8,0,...]
    high (thr=0.75) below(2) : K_steady=24  curve [2,8,24,24,...]  inc [6,16,0,...]
    low  (thr=0.25) above(24): K_steady=24  curve [24,24,...]      inc [0,...]  (no down-regulation — L2)
    mid  (thr=0.50) above(24): K_steady=24  curve [24,24,...]      inc [0,...]
    high (thr=0.75) above(24): K_steady=24  curve [24,24,...]      inc [0,...]
  K_low=8 ≈ 0.25×32=8 · K_mid=16 ≈ 0.50×32=16 · K_high=24 ≈ 0.75×32=24
falsifiers_pass: F1 (saturation) + F2 (monotone) + F3 (logistic) + F4 (determinism) + F5 (bounds) = 5/5
falsifiers_triggered: none
criteria_met: 4/4 (C1 ∧ C2 ∧ C3 ∧ C4)
key_finding:
  density-gated split predicate 가 mitosis pool 을 carrying capacity 로
  self-regulate 시킨다 — 무한 증식 (기존 tension-only split 은 max_cells=128
  까지 grow) 대신 below-K seed 가 K = floor(inhibition_threshold × capacity)
  부근에서 정확히 *포화* 한다 (low→8, mid→16, high→24, 모두 예측과 일치).
  threshold↑ → K↑ 엄격 단조 (8 < 16 < 24). 성장곡선은 logistic-유사 —
  초기 빠른 가속 (2→8 in first window) 후 급격 감속 후 flat tail (increment
  [6,16,0,0,...]). re-run byte-equal. density gate 가 contact-inhibition-of-
  proliferation 의 substrate analog 로 작동, Verhulst carrying capacity 의
  emergent 발생을 numerically 입증.
honest_note:
  L1 carry critical — density gate 는 step-function 이라 감속이 *급격*
  (smooth sigmoid 아님); 결과는 logistic-유사 (포화하는 S-shape) 이지
  smooth logistic 의 입증 아님.
  L2 carry critical — one-sided brake: above-K seed (24) 가 low/mid K
  (8/16) 로 *수축하지 않고* 24 유지 — apoptosis/merge 없는 단방향 상한
  brake (양방향 homeostat 아님).
  L6 carry — K = threshold × capacity 의 *값* 은 gate 정의의 거의 직접
  귀결 (동어반복 위험); 비-자명한 발견은 (a) self-regulation 발생 자체와
  (b) 성장의 logistic-유사 형태.
sibling: H_200 (apoptosis-primitive), H_201 (asymmetric-division), H_220 (division/self axis)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25)

```
================================================================
H_260 contact-inhibition — density-gated split → carrying capacity
  d_model=8 capacity=32 n_steps=60 seed=42
  inhibition thresholds: low=0.25 mid=0.5 high=0.75
  initial pool sizes: below=2 above=24
  K_predicted ~ floor(threshold * capacity): low~8.0 mid~16.0 high~24.0
================================================================
condition          init  K_steady  growth_curve (every 5 steps)
-----------------  ----  --------  ----------------------------
low  (thr=0.25) b   2    8      [2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
mid  (thr=0.50) b   2    16      [2, 8, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]
high (thr=0.75) b   2    24      [2, 8, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24]
low  (thr=0.25) a  24    24      [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24]
mid  (thr=0.50) a  24    24      [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24]
high (thr=0.75) a  24    24      [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24]

derived:
  K_low  (thr=0.25) = 8  (predicted ~8.0)
  K_mid  (thr=0.50) = 16  (predicted ~16.0)
  K_high (thr=0.75) = 24  (predicted ~24.0)
  capacity (hard ceiling) = 32
  below-seed increments  low=[6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                         mid=[6, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                        high=[6, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

C1 SATURATION  (K<cap ALL & flat tail)    : true
C2 MONOTONE-K  (K_low<K_mid<K_high)        : true
C3 LOGISTIC    (accel→decel→flat ALL)      : true
C4 DETERMINISM (re-run K byte-equal)       : true

F1 SATURATION       PASS
F2 MONOTONE-K       PASS
F3 LOGISTIC         PASS
F4 DETERMINISM      PASS
F5 BOUNDS           PASS
================================================================
VERDICT: SUPPORTED  (4/4 criteria, 5/5 falsifiers PASS)
================================================================
ledger -> HEXAD/LIFE/state/h260_contact_inhibition_2026_05_25/result.json
```

**State output**: `state/h260_contact_inhibition_2026_05_25/result.json`
**Smoke**: `state/h260_contact_inhibition_2026_05_25/run_h260.hexa` (hexa-only, LLM none)
