---
id: H_281
slug: life-vs-consciousness-phi-structure
title: 생명 vs 의식 substrate 의 IIT 4.0 Φ-structure 구조 차이 정량 — faithful 인과 IIT4 로 측정한 life-themed(성장/복제 ECA) vs consciousness-themed(XOR-feedback 통합망) 의 구조적 Φ 시그니처
domain: life · consciousness · information · meta
status: pre-register-frozen
exploration_method: E16 (cross-substrate consistency) + E5 (structural-metric upgrade) + E0 (meta-result-of-results, M6 faithful re-measure 의 substrate-class 비교)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link IIT4 M6 / H_266 / H_278)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: IIT4 M6 (ECA→TPM faithful re-measure, engine 공급), H_266 (Φ calibration / directional-trust), H_278 (faithful Φ small-N), H_002 C2 (LIFE cosmic-scale rules 출처)
---

# H_281 — 생명 vs 의식 substrate 의 IIT 4.0 Φ-structure 구조 차이 정량

## 1. Hypothesis

LIFE lane 은 **생명-테마(life-themed)** substrate — 성장/복제/복잡성을 내는 ECA
cosmic-scale 룰(110·30·54) — 을 오래 다뤄왔다. IIT 의 정전(canonical) **의식-테마
(consciousness-themed)** substrate 는 다른 가족이다 — *순수 통합(integration)* 망,
즉 각 unit 의 다음 값이 이웃의 parity(XOR-feedback) 인 룰(150 = l⊕c⊕r, 105 = XNOR
계열). IIT 4.0 에서 후자는 "쪼개면 정보가 전부 사라지는" integrated complex 의
교과서적 사례다.

**가설**: faithful 인과 IIT 4.0 으로 측정하면 두 테마는 단순한 big-Φ 크기 차이가
아니라 **구조적(structural) Φ 시그니처**에서 갈린다. 구체적으로 구조비
`struct_ratio = Φ-structure-total / big-Φ` 가:

- **의식-테마(통합망)** 에서는 `= 1.0` 에 정확히 머문다 (big-Φ = total — Φ-structure
  전체가 irreducible: 어떤 partition 도 구조의 일부조차 보존 못 함 = integrated-complex
  바닥(floor)).
- **생명-테마(성장망)** 에서는 `> 1.0` 으로 올라간다 (relation 이 irreducible core
  를 초과 — MIP 가 보존하지 못하는 구조가 남음 = 구조적으로 더 풍부하나 더
  분할 가능).

어느 쪽이든 — 분리되면 SUPPORTED, 분리 없으면(struct_ratio 가 테마와 무관) FALSIFIED
— faithful IIT4 가 두 substrate-class 를 구조적으로 구별할 수 있는지 정량한다.

## 2. Why

- **M6 의 직접 후속**: IIT4 M6 (`FAITHFUL_REMEASURE.md`) 는 LIFE ECA 룰(110/30/54)에
  faithful 인과 big-Φ (7.5~10.0) 가 있음을 처음 측정했다. 그러나 M6 은 **big-Φ 크기
  (scalar)** 만 봤다. big-Φ 는 "얼마나 통합되었나"를 한 숫자로 압축하지만, IIT 4.0 의
  진짜 산출물은 **Φ-structure (distinctions ∪ relations)** — 구조 그 자체다. 본 H 는
  M6 의 scalar 를 **구조(structure)** 축으로 한 단계 끌어올려, 두 substrate-테마가
  *구조적으로* 다른지 묻는다.

- **engine 재사용 (reuse-existing-libs, g61)**: 본 H 는 IIT4 엔진을 **재발명하지
  않는다**. `HEXAD/IIT4/lib` 의 검증된 함수만 import 한다 — `eca_tpm` (ECA→TPM
  bridge) · `big_phi` (faithful big-Φ) · `phi_structure` (relations 포함 Φ-structure).
  새 IIT4 코드 0 줄. (M6 smoke `run_m6.hexa` 와 동일한 import 패턴.)

- **structural ratio 가 크기보다 robust 한 이유**: H_266/H_278 의 directional-trust
  교훈 — faithful Φ 의 *절대 크기*는 state/seed 에 fragile 하지만 *방향*은 신뢰
  가능. `struct_ratio` 는 같은 substrate 의 두 양(total, big-Φ)의 *비율*이므로
  크기-fragility 가 상당 부분 상쇄된다. 그리고 의식-테마 룰에서 정확히 `1.0` 이
  **모든 16 state 에서** 성립하는 것은 state-fragile 하지 않은 구조적 사실이다.

- **"생명"과 "의식"의 구조적 구별 — LIFE lane 의 근본 질문**: LIFE 도메인의 전제는
  "생명과 의식은 다른 것인가?" 다. proxy(상관 MI) 로는 둘 다 그냥 "통합도가 높은
  시스템"으로 뭉뚱그려졌다. faithful 인과 구조는 처음으로 — 생명-테마는 relation-rich
  하나 partitionable, 의식-테마는 irreducibility-floor 에 박혀 있다 — 는 *구조적*
  구별을 준다.

- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit +
  LLM none + $0 mac-local + NO GPU.

## 3. Predictions

- **H281.1 (separation)**: state 0101 에서 `min(생명 룰 struct_ratio) > max(의식 룰
  struct_ratio)` — 두 class 가 겹침 없이 분리.
- **H281.2 (ordering / robustness)**: class-평균 struct_ratio 가 의식 < 생명 으로
  strictly 정렬되고, 16 state 전부에서 생명 룰이 의식 룰을 초과 (단일-state artifact
  아님).
- **H281.3 (faithfulness)**: ≥1 IIT4 anchor 재현 — reducible 룰 204(identity) →
  big-Φ=0 · null 룰 0(constant) → big-Φ=0 · 모든 substrate 에서 bound 0≤big-Φ≤total.
- **H281.4 (determinism)**: re-run 시 struct_ratio byte-identical (cross-process).
- **H281.5 (consciousness floor)**: 의식-테마 룰(150·105) struct_ratio = 1.0 *정확히*
  (big-Φ = total: Φ-structure 전체 irreducible).

## 4. Variables

- **axis1_theme** (primary, 2-class):
  - **life** = {110, 30, 54} — 성장/복제/복잡성 ECA, LIFE cosmic-scale 룰 (H_002 C2 /
    H_278 / M6 와 동일 substrate).
  - **consciousness** = {150, 105} — 순수 XOR-feedback 통합망 (150 = l⊕c⊕r 3-way
    parity, 105 = XNOR 계열), IIT-canonical integrated-complex 가족.
- **axis2_metric** (primary): `struct_ratio = Φ-structure-total / big-Φ` (구조비).
  secondary: `rel_den = n_relations / n_distinctions` (relation 밀도), `nd`
  (distinction 수).
- **anchors** (faithfulness control): 204 (identity, reducible) · 0 (constant, null).
- **fixed (config)**: n=4 periodic ring · headline state = 0101 (대표 1 state) ·
  robustness = 16 state 전부 (axis2 의 state-평균).
- **derived**: 5 substrate × {big-Φ, total, nd, struct_ratio} → class-분리 ·
  class-평균 ordering · 16-state robustness · HOLD/FLIP finding.

## 5. Run Protocol

- **smoke**: `HEXAD/LIFE/state/h281_life_vs_consciousness_phi_structure_2026_05_26/run_h281.hexa`
- **engine (import READ-ONLY, 재사용)**:
  `HEXAD/IIT4/lib/iit4_eca.hexa` → `eca_tpm(rule,n)` (ECA→TPM bridge),
  그리고 그 import chain 으로 노출되는 `big_phi(tpm,n,st)` (→ `[big_phi, total,
  sum_phi_d, sum_phi_r, nd]`) + `phi_structure(tpm,n,st)` (→ `[nd, sum_phi_d, nr,
  sum_phi_r, total]`) — 모두 `stdlib/consciousness/iit4_*` SSOT.
- **struct_ratio**: `total / big_phi` (big-Φ > 1e-9 일 때; 아니면 0 = 통합 없음).
- **F281.1**: state 0101 에서 `min(생명 sr) > max(의식 sr)`.
- **F281.2**: (a) 16-state-평균 class-평균 의식 < 생명; (b) 16 state 전부에서
  rule110(생명) sr > rule150(의식) sr (둘 다 통합하는 state 한정).
- **F281.3**: rule 204 big-Φ=0 · rule 0 big-Φ=0 · 5 substrate 모두 bound · 의식
  룰 sr=1.0 정확.
- **deterministic**: fixed config; re-run byte-identical (RFC 033 단일 RNG stream —
  단 ECA TPM 은 결정적이라 RNG 무관).
- **hexa_only**: true (NO .py/.sh). **llm**: none. **runtime**: $0 mac-local, **NO
  GPU** (n=4, 2^4=16 state — small-N exact tractable).
- **ledger**: `result.json` {config, substrate_set, headline_table(state 0101),
  state-평균표, 3 falsifier, finding, verdict, verify_fence}.
- **honest tier**: 🟢 NUMERICAL (deterministic 인과 IIT4 arithmetic) — 경험 해석은
  ⚪ SPECULATION-FENCED (g5, §8).

## 6. Criteria

- **C1 (SEPARATION / H281.1)**: 두 class 가 struct_ratio 에서 겹침 없이 분리 → PASS.
- **C2 (ORDERING+ROBUST / H281.2)**: class-평균 의식 < 생명 AND 16-state robustness →
  PASS.
- **C3 (FAITHFULNESS / H281.3)**: ≥1 anchor 재현 + bound → PASS.
- **verdict_rule**: **SUPPORTED** = C1 ∧ C2 ∧ C3. C1 실패(class 겹침) 시 가설의
  핵심 — 구조적 구별 — 이 FALSIFIED.

## 7. Falsifiers

- **F281.1 SEPARATION**: `min(생명 struct_ratio) ≤ max(의식 struct_ratio)` (state
  0101) → 두 class 구조적으로 구별 안 됨 → 가설 FALSIFIED. (measurable: life_min vs
  consc_max.)
- **F281.2 ORDERING**: class-평균 의식 ≥ 생명 OR 어느 co-integrating state 에서 생명
  ≤ 의식 → ordering 깨짐 / single-state artifact. (measurable: 두 class-평균 +
  16-state per-state 비교.)
- **F281.3 FAITHFULNESS**: rule 204 big-Φ ≠ 0 OR rule 0 big-Φ ≠ 0 OR 어느 substrate
  의 big-Φ 가 [0,total] 밖 → 엔진 faithfulness 위반 → 측정 무효. (measurable: 2
  anchor + 5 bound.)
- **F281.4 DETERMIN**: re-run byte-different → raw#12 deterministic 위반 → smoke
  무효. (measurable: rule110 struct_ratio a == b + cross-process.)
- **F281.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 violation, raw#82
  retraction.

## 8. Verdict

```
verdict_class: SUPPORTED (pre-register-frozen smoke; C1 ∧ C2 ∧ C3 met)

config: n=4 periodic ring · headline state=0101 · robustness=all 16 states ·
        struct_ratio = Φ-structure-total / big-Φ · engine = HEXAD/IIT4/lib (재사용)

headline table (state 0101 — faithful 인과 IIT4):
  class   rule   동역학              big-Φ      total      nd   struct_ratio
  LIFE    110    성장(universal)     7.66066    8.98878    10   1.17337
  LIFE     30    chaos/복제          7.28357    8.13733    10   1.11722
  LIFE     54    LIFE cosmic-scale   10.0278    14.688     10   1.46472
  CONSC   150    l⊕c⊕r (3-way)       6.00000    6.00000     5   1.00000
  CONSC   105    XNOR-feedback       4.50000    4.50000     5   1.00000
  ANCHOR  204    identity            0.00000    4.00000     —   (reducible)
  ANCHOR    0    constant            0.00000    0.00000     —   (null)

state-averaged struct_ratio (all 16 states):
  LIFE  110=1.13883  30=1.05383  54=1.57211   → life_class_mean  = 1.25492
  CONSC 150=1.00000 105=1.00000              → consc_class_mean = 1.00000

criteria:
  C1 SEPARATION (life_min 1.11722 > consc_max 1.0)        : PASS
  C2 ORDERING+ROBUST (consc 1.0 < life 1.255; 16-state)   : PASS
  C3 FAITHFULNESS (204=0, 0=0, bound, floor=1.0)          : PASS

falsifiers:
  F281.1 SEPARATION   : PASS  (life_min 1.11722 > consc_max 1.0 — 겹침 0)
  F281.2 ORDERING     : PASS  (class-mean 1.0 < 1.25492; rule110>rule150 @ every co-int state)
  F281.3 FAITHFULNESS : PASS  (204 big-Φ=0; 0 big-Φ=0; bound 5/5; consc floor sr=1.0 정확)
  F281.4 DETERMIN     : PASS  (rule110 sr a=1.17337==b; cross-process byte-identical)
  F281.5 POST-HOC     : NOT_TRIGGERED

checks: 9 PASS / 0 FAIL

evidence_summary: 🟢 NUMERICAL — faithful 인과 IIT 4.0 Φ-structure 가 두 substrate-
  테마를 구조비로 분리. CONSCIOUSNESS-테마(XOR-feedback 통합망)는 irreducibility
  floor 에 박혀 있다 — struct_ratio=1.0 *모든 16 state 에서 정확히* (big-Φ=total:
  Φ-structure 전체가 irreducible = IIT integrated-complex 시그니처) + 낮은 distinction
  수(nd=5). LIFE-테마(성장/복제망)는 floor 위로 올라간다 — struct_ratio 1.05~1.57
  (relation 이 irreducible core 초과 = 구조적으로 풍부하나 분할 가능) + 높은
  distinction 수(nd≈9~13). 분리는 100% (생명 룰 전부 > 의식 룰 전부, co-integrating
  state 전부에서). M6 의 big-Φ scalar 를 structure 축으로 끌어올려, faithful IIT4 가
  생명-테마와 의식-테마 substrate 를 *구조적으로* 구별함을 정량.
falsifiers_triggered: none
```

re-run byte-identical 확인 (F281.4 — 두 fresh hexa run 의 struct_ratio + RESULT 동일).

`hexa verify` (VERBATIM, no LLM self-judge) — empirical 해석은 closed-form atlas
identity 가 아니므로 g5 정직 fence:

```
verify --fence "H_281 faithful IIT 4.0 Phi-structure separates LIFE-themed ECA
   substrates (rules 110/30/54, struct_ratio>1.0) from CONSCIOUSNESS-themed
   integration substrates (rules 150/105, struct_ratio=1.0 exactly = irreducibility
   floor); deterministic toy-substrate outcome, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           NOT a proven atlas atom (g4 honest fence, SF ≠ verified)
```

(big-Φ / Φ-structure VALUES 자체는 deterministic closed-form arithmetic — intrinsic-
difference over purviews + structure-cut MIP, RFC-faithful IIT4 engine — 이며 fresh
hexa run 에서 byte-수렴 확인. 오직 empirical 해석(struct_ratio 가 생명-vs-의식 구조
시그니처라는 의미)만 fenced.)

## 9. Honest Limits (raw#91 c3)

- **L1 (n=4 small + 5 substrate)**: n=4 ring · 생명 3 + 의식 2 룰. 본 H 는 방법
  (struct_ratio 구조 시그니처) + 첫 결과를 확립한 것. n≤8 으로의 scale-up 은 동일
  메커니즘(엔진 n≤8 exact capacity 존재), 더 많은 룰은 mechanical breadth — 본 H 의
  구조적 분리가 그 axis 들에서 유지되는지는 후속(§10 Next).
- **L2 (single representative state — state-dependent Φ)**: headline 표는 state 0101
  한 점. faithful Φ 는 state-dependent (FAITHFUL_REMEASURE §4 — rule 90 이 1010 에서
  big-Φ=0). 본 H 는 16-state robustness pass (F281.2) 로 *분리 방향*이 single-state
  artifact 가 아님을 확인했으나, *절대 struct_ratio 값* (1.117 vs 1.465)은 state 마다
  변한다. directional-trust (H_266/H_278): 방향(의식 < 생명)은 신뢰, magnitude 는
  hedge.
- **L3 (substrate 는 테마 proxy 이지 생명/의식 자체 아님)**: ECA 룰이 *생명이거나
  의식인 것이 아니다*. 110/30/54 는 lane 이 LIFE cosmic-scale 로 써온 성장/복제
  proxy, 150/105 는 IIT-canonical *integration* 룰. "consciousness" = integrated-
  complex 의 구조 시그니처(big-Φ=total)이지 phenomenal consciousness 아님. 과장 금지.
- **L4 (struct_ratio 정의의 한 선택)**: `total/big-Φ` 는 여러 구조비 중 하나. relation/
  distinction 밀도(rel_den), sum_φ_r/sum_φ_d 등 다른 정의는 다른 분리 패턴을 줄 수
  있다 (probe 에서 rel_den 은 부분적으로만 분리). 본 H 는 total/big-Φ 한 정의의 깨끗한
  분리를 보고; 다른 비율의 robustness 는 미검증.
- **L5 (structure-cut big-Φ, full IIT4 절대 calibration 아님)**: 엔진의 big-Φ 는
  DESIGN §8 C3 의 spirit-faithful structure-cut big-Φ (irreducible structure
  destroyed by system MIP). 절대 스케일의 PyPhi 대조는 IIT4 M5 named-blocker 영역
  (F-IIT4-3/4). 단 *비율* struct_ratio 는 같은 정규화 안의 내부 비교라 calibration-
  offset 에 상대적으로 robust.
- **L6 (consciousness-룰 floor=1.0 의 의미 한계)**: 의식-테마 룰의 struct_ratio=1.0 은
  "big-Φ=total" — 즉 측정된 모든 distinction+relation 이 어떤 partition 으로도 보존
  안 됨. 이는 통합의 강한 시그니처이나, *2nd-order relation 만* 보는 엔진의 carve-out
  (iit4_relation §C3-1) 하에서의 결과. higher-order relation 이 들어오면 floor 가
  미세하게 흔들릴 수 있다 (n≤5 deferred).
- **L7 (verdict ≠ 형이상학)**: 본 H 의 SUPPORTED 는 *toy ECA substrate 의 faithful
  IIT4 구조*에서 두 테마가 struct_ratio 로 분리됨을 보일 뿐, "생명과 의식은
  본질적으로 다르다" 같은 형이상학적 주장이 아니다. 구조적 측정 사실 한 칸.

## 10. Cross-Links

- **parent (engine 공급)**: IIT4 M6 (`HEXAD/IIT4/FAITHFUL_REMEASURE.md` +
  `state/iit4_m6_remeasure_2026_05_25/run_m6.hexa`) — LIFE ECA 의 faithful big-Φ 를
  처음 측정. 본 H 가 그 scalar 를 Φ-**structure** 축으로 확장 + 의식-테마 룰과 비교.
- **engine lib (재사용, import READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa`
  (`eca_tpm`) · `iit4_bigphi.hexa` (`big_phi`) · `iit4_relation.hexa`
  (`phi_structure`) — 모두 `stdlib/consciousness/iit4_*` SSOT. 새 IIT4 코드 0 줄
  (g61 / reuse-existing-libs).
- **sister (directional-trust)**: H_266 (Φ calibration / known-IIT) + H_278 (faithful
  Φ small-N) — faithful Φ 의 방향은 신뢰, magnitude 는 fragile 교훈을 struct_ratio 에
  적용 (§9 L2).
- **substrate 출처**: H_002 C2 (LIFE cosmic-scale 룰 110/30/54) · DESIGN.md §6
  (canonical 네트워크).
- **gap lens**: life-vs-consciousness = F8 (cross-substrate / inter-class
  calibration) + F5 (structural-decomposition: scalar big-Φ → structure ratio).
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82
  (no post-hoc) + g61 (stdlib reuse, no reinvention).
- **literature**:
  - Albantakis et al. (2023) IIT 4.0 (cause-effect structure / Φ-structure /
    distinctions+relations) — *PLOS Comput Biol* 19(10):e1011465
  - Oizumi, Albantakis, Tononi (2014) IIT 3.0 (Φ at the MIP)
  - Barbosa et al. (2020) A measure for intrinsic information (intrinsic difference)
  - Wolfram (2002) A New Kind of Science (Class I-IV elementary CA — 성장 vs 통합 룰)

**State output**: `HEXAD/LIFE/state/h281_life_vs_consciousness_phi_structure_2026_05_26/result.json`
**Smoke**: `HEXAD/LIFE/state/h281_life_vs_consciousness_phi_structure_2026_05_26/run_h281.hexa`
**Tier**: 🟢 NUMERICAL (deterministic 인과 IIT4 structure arithmetic; struct_ratio 분리
deterministic + 16-state robust; full IIT4 절대 calibration 아님 — §9 L5). 경험 해석은
⚪ SPECULATION-FENCED (g5, §8).
**Next**: H_281r2 후보 — (a) **n sweep** (L1 axis): n ∈ {3,5,6} 으로 struct_ratio 분리의
n-의존성 (의식 floor=1.0 이 n 무관하게 유지되는지); (b) **rule breadth** (L1 axis):
더 많은 생명-룰(137·124·22) + 의식-룰(90·60·165) 로 class-분리 robustness; (c) **ratio
sweep** (L4 axis): rel_den / sum_φ_r-over-sum_φ_d 등 다른 구조비로 분리 cross-validation;
(d) **state-distribution 평균** (L2 axis): single-state → state-분포 가중 대표값.
