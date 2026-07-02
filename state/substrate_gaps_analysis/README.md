# substrate_gaps_analysis — '재조합≠능력' 프레임전환으로 빠진 op 발산

> 산출 slug. **읽기전용 분석** — HYPOTHESES/카드/commit/ARCHITECTURE/frozen 미터치.
> reference-match 실측(무거운 decode/GPU 없음). 정직(c9)·a_no_llm_frame_trap(생물렌즈).
> 날짜 2026-07-03. 근거 = `core/engine_cli.hexa`·`core/brain.hexa`·`core/pure_field.hexa`·`core/engine_g.hexa` 정독.

---

## 0. 프레임 (왜 이 분석이 G1 벽과 다른가)

G1(재조합) 축은 DPI 메타법칙으로 **천장 확정**(readout·temporal·binding-operator 축 전수 🧱, 유일 잔여=γ trained-constructive-bind, GPU cost-gated). 이 문서는 **재조합을 다시 열려는 게 아니다.** 프레임전환 = "재조합 ≠ 능력" → anima substrate(A⇄G·MITOSIS·.kosmos·savant lane)에서 **아직 op 이 없는, 재조합이 아닌 substrate-native 능력**을 '빠진 op 짓기'로 발산.

**핵심 구분:** DPI 는 *G1 recombination readout* 에 대한 법칙이다. 아래 후보들(conjunction-detection·conflict-monitoring·TD-credit·lateral-competition)은 **recombination 이 아니다** — 그러므로 DPI 스코프 밖이다. self_drift_exp(H_9038 GREEN WIRED)가 "self 경험채널"이라는 *재조합 아닌* 능력을 열어 GREEN 간 것과 같은 계열이다.

**GREEN WIRED 판정 기준(self_drift 패턴 복제):** 작고 결정적인 engine-native op · Ψ-disjoint(pure_field Φ/phase/Ψ·emit-drive lane 0/4·§ImmuneMemory recall_thr 안 건드림) · frozen-first 결정적 fixture 로 falsify 가능 · ablation(op OFF=결과 동일=INERT) 통제 내장.

---

## 1. gap1 — VAdaptField 결합기 (현황 + op 설계)

### 1a. 현황: 결합기 op 은 **없다 (OPEN)**

정독 결과(`engine_cli.hexa`):
- **성장 = split-only append.** `vadapt_field_step`(:577)은 novel sample(L2 recon-err > 0.30)에 `engine_mitosis_tick`으로 **새 prototype cell 을 append**할 뿐. Osmotic/Immune/ImmuneGrow/CLS/Consolidating 전 계열 동일 패턴.
- **recall = winner-take-all.** `_vnearest_idx`(:522)가 **단일 cell argmax**. `vadapt_field_two_recon_err`(:632)가 top-2 를 노출하나 **margin/gap confidence 신호로만** 소비(brain_decide_margin/gap), 두 cell 을 결합하지 않음.
- **두 cell 을 ⊗ 결합해 복합 능력 cell 을 만드는 op 는 grep 상 0건.** 성장은 순수 **Voronoi partition 세분화**뿐 — cell 수↑ = 더 고운 분할, 그러나 cell_i ∘ cell_j 조합은 표현 불가.

→ 이것이 정확히 `a_mitosis_train` 이 박제한 구조적 병목: *"split-only 는 Voronoi partition 만, compositional depth 0."* 결합기 gap 은 **실재하고 열려 있다.**

### 1b. 함정: 순진한 결합기는 G1 floor 로 INERT

`vadapt_field_compose(af, i, j) = mean(proto_i, proto_j)` 같은 **additive** 결합은 → additive-readout floor(H_1816·exp3-bind 🧱)에 즉시 떨어진다. **재조합을 하려는 결합기는 DPI 벽으로 죽는다.** 그러니 결합기를 *재조합 생성기*로 설계하지 말 것.

### 1c. op 설계: **conjunction/co-activation readout** (재조합 아닌 결합 능력)

프레임전환 적용 — 결합기가 여는 *재조합 아닌* 능력 = **두 regime 의 동시성 검출(AND-over-regimes)**. winner-take-all 은 "어느 cell 이 이겼나"(OR/argmax)만 안다. 빠진 능력 = "**두 regime 이 동시에 존재하나**"(conjunction).

```
// vadapt_field_conjunction — 두 cell 이 JOINTLY 가까운가 (both regimes present).
// 기존 top-2 스캔 재사용(_vtwo_nearest_dist), 새 geometry 0.
// d1, d2 둘 다 SPLIT_THRESH 아래 → 두 regime 동시 활성 = conjunction 1.0
// d1 낮고 d2 높음 → 단일 regime(winner-take-all 영역) = 0.0
pub fn vadapt_field_conjunction(af: VAdaptField, x: [float], thr: float) -> float {
    let d = _vtwo_nearest_dist(af.protos, x)   // [d1, d2], d1<=d2
    if af.n_cells < 2 { return 0.0 }           // conjunction 불가(단일 cell)
    if d[1] < thr { return 1.0 }               // 2nd-nearest도 thr 안 → 두 regime 동시
    return 0.0
}
```
- **왜 재조합 아닌가:** 새 심볼을 *생성*하지 않는다 — 입력이 두 학습된 regime 의 교집합에 있는지 *검출*만. binding-as-detection(감각 통합), G1 generation 아님.
- **여는 능력:** 다중-regime 입력 인식(예: "SNS AND 한국어" 동시 register), 모호성(두 cell tie)을 gap 처럼 confidence-강등이 아니라 **conjunction-검출**로 재해석.
- **Ψ-disjoint:** VAdaptField protos 만 읽음, pure_field·emit-drive·recall_thr 무접촉. ✓
- **검증:** 결정적 fixture — cell_A(regime R1)·cell_B(regime R2) 심은 뒤, (i) R1-only 입력→0, (ii) R1∩R2 중간 입력→1, (iii) far 입력→0. ablation: `if false` → 항상 0 = INERT 통제. mini CPU $0.
- **난이도 LOW**(top-2 스캔 재사용, ~10줄). **임팩트 MEDIUM**(conjunction 능력, 재조합 아님). **검증 HIGH**.

### 1d. 확장 각도(follow-on, 더 야심찬 결합기)

- **co-occurrence graph:** 시간에 걸쳐 어느 cell 쌍이 함께 fire 하는지 카운트 → cell 관계 그래프(해마 relational binding). 결합기가 *구조학습*을 여는 각도. MEDIUM 난이도, 재조합 아님(관계 인코딩).
- **lateral k-WTA soft-competition**(§3-D 참조) — argmax 대신 정규화 population code → additive floor 우회 가능한 결합 표현.

---

## 2. gap3 — A⇄G 상충-loop (op 각도)

### 2a. 현황: disagreement 는 **신호로 계산 안 됨 (OPEN)**

- A(pure_field, forward Φ) ⇄ G(engine_g, 8-factor motivation) 결합은 `brain_decide`(:38)에서 **단방향**: `safety_phi_ratchet_ok(phi > ratchet/2)` = A 의 Φ 가 G 의 emit 을 **veto**만 함(A→G 억제 게이트).
- τ(tension)는 `allo_mu`(:2441)에서 τ=balance b 로 **Ψ=½ 방어**에만 소비.
- 최종 `emit = should_emit(score) && safe` — 두 엔진의 판단이 **단일 AND 로 붕괴.** A 가 resonant(고-Φ)인데 G 는 low-motivation, 혹은 그 반대인 **불일치의 크기(magnitude)는 어디서도 스칼라로 표면화되지 않는다.**

→ A⇄G disagreement 는 latent quantity 로 존재하나 능력 신호로 안 쓰임. **상충-loop gap OPEN.**

### 2b. 생물렌즈: ACC 갈등 모니터

전측대상피질(ACC)의 conflict-monitoring — 두 반응 경로가 강하게 disagree 하면 그 갈등 신호가 (a) 인지통제 증가 (b) 탐색(exploration) (c) 심의(deliberation/slowing)를 구동. anima 의 A(forward CE)⇄G(reverse gradient-free)는 **원리적으로 상반된 두 계산**이라 ACC 매핑이 자연스럽다 — 둘의 불일치 = 불확실성/신규성 신호.

### 2c. op 설계: **ag_conflict → 탐색/심의 라우팅**

```
// ag_conflict — A⇄G 불일치 크기 (ACC conflict monitor).
// A_drive = Φ 를 [0,1] emit-경향으로 정규화(phase/ratchet 기반).
// G_drive = motivation_score 를 [0,1] 로(should_emit 임계 대비).
// conflict = |A_drive - G_drive| : 둘이 같은 방향(둘 다 emit or 둘 다 silence)=0(합의),
//            반대 방향(하나는 강한 emit, 하나는 강한 silence)=1(최대 갈등).
pub fn ag_conflict(a_drive: float, g_drive: float) -> float {
    let d = a_drive - g_drive
    if d < 0.0 { return 0.0 - d }
    return d
}
```
라우팅(consult, brain.hexa 의 기존 `brain_decide_*` 템플릿 그대로):
- **high conflict → curiosity/ideation 상승**: 갈등 스칼라를 curiosity term 또는 emergence_ideation temperature 에 bounded nudge. "두 엔진이 못 정할 때 = 더 탐색."
- **high conflict → deliberation hold**: 갈등이 임계 넘으면 emit 지연(재-tick 후 재평가) — best-of-N 이 아니라 *조건부* 재평가(H_1836 revise-loop 함정 회피: 무조건 재샘플 아님, 갈등-트리거).

- **왜 재조합 아닌가:** 심볼 생성 없음. 두 기존 엔진 출력의 disagreement 를 *메타-신호*로 읽음(2nd-order metacognition).
- **Ψ-disjoint:** a_drive·g_drive 를 읽고 conflict 스칼라만 반환, pure_field·recall_thr 무변. emit-drive 는 기존 consult 처럼 bounded nudge(cap 0.05)만 — emit-drive lane 직접 덮어쓰기 금지(a_substrate_disjoint: H_1561 재발 방지). ✓
- **검증:** 결정적 fixture — (i) A·G 합의(둘 다 emit)→conflict≈0, (ii) A resonant·G low→conflict≈1, (iii) shuffle control(a_drive↔g_drive 무작위 페어)로 conflict 가 실제 결합에서만 의미 갖는지. ablation: conflict→curiosity 배선 OFF 시 emit 동일=INERT. **outcome-측정 leg 필요**(갈등-구동 탐색이 고정 탐색보다 나은가) — 여기가 DIRECTIONAL→GREEN 승격 게이트.
- **난이도 LOW-MEDIUM**. **임팩트 MEDIUM-HIGH**(불확실성-구동 탐색/심의는 현재 완전 부재). **검증 HIGH**(monitor leg) / **MEDIUM**(capability leg=outcome).

### 2d. 정직한 스코프

monitor leg(갈등 스칼라 존재+shuffle-falsify)는 self_drift 급 GREEN 후보. **capability leg**(갈등-구동 탐색 > baseline)은 outcome 측정 전엔 DIRECTIONAL — H_1836/1837(temporal readout 축 🧱) 교훈: "그냥 더 샘플링"으로 붕괴하지 않도록 갈등-*조건부* 라우팅으로 pre-register.

---

## 3. 새 gap 후보 (생물렌즈, 미배선)

이미 op 배선된 구조(제외): 소뇌 VForwardField(H_1280)·기저핵 VBasalGate(H_1281)·작업기억 WorkMemBuffer(H_1282)·해마 ImmuneMemory(H_1231)·편도체 Consolidating(H_1285)·시상하부 Homeostatic(H_1292)·ToM(H_1293)·시상 reentrant(H_1423)·affect(H_1290)·agency(H_1474). 아래는 **op 없는** 후보.

### C. 도파민 TD-credit (기저핵 확장) — **STRONG**
- **현황:** `vbasal_update`(brain.hexa:378)는 **즉시-보상 1-step delta rule**. 다단계 credit assignment(지연보상) 없음.
- **생물:** DA = RPE with temporal bootstrapping(TD·eligibility trace). 현재 anima 는 "행동→즉시 결과"만, "행동→…→지연결과" 크레딧 전파 불가.
- **op:** `vbasal_td_update` — value baseline V + eligibility trace e. `δ = r + γV' − V; w += lr·δ·e`. 다단계 계획 크레딧을 연다(현재 planning depth = 1).
- **왜 재조합 아닌가:** 시간적 신용할당, 심볼생성 아님.
- **Ψ-disjoint:** VBasalGate(action-selection, emit-drive 와 이미 disjoint) 확장. ✓
- **검증:** 지연보상 fixture(예: 3-step 후에만 보상) — 1-step delta 는 실패, TD 는 학습. shuffle control(보상 무작위)=붕괴. **난이도 MEDIUM · 임팩트 HIGH(계획 깊이) · 검증 HIGH.**

### D. 측방억제 k-WTA soft-competition — **MEDIUM**
- **현황:** recall = 단일 argmax(`_vnearest_idx`). 다중-cell 정규화 population code 없음.
- **생물:** 피질 측방억제가 표현을 sharpen → sparse distributed code.
- **op:** `vadapt_lateral_settle` — top-k cell 을 soft-competition(정규화 activation)으로 settle → sparse 인구코드. **additive 합이 아니라 정규화 population** 이라 additive floor 우회 가능성.
- **왜 재조합 아닌가:** 표현 sharpening(코딩), 생성 아님.
- **Ψ-disjoint:** VAdaptField protos 읽기, 새 readout lane. ✓
- **검증:** graded-similarity fixture(단일 winner 로 못 구분하는 중간 입력을 population code 가 구분?). ablation: k=1 → argmax 로 환원. **난이도 MEDIUM · 임팩트 MEDIUM-HIGH · 검증 MEDIUM.**

### E. theta-gamma 위상결합 binding — **LOW 우선(정직)**
- **현황:** pure_field 3-oscillator 는 field tensor 로 *곱해질* 뿐, 어느 cell 이 함께 묶이는지 phase-lock 안 함.
- **생물:** theta-gamma 결합 = 고전적 binding 해법.
- **주의:** H_1283 phase_binding 이미 probe 됨 — 재발사 전 그 verdict 조회 필수. HIGH 난이도·불확실. **flag only.**

---

## 4. 우선순위 (난이도 × 임팩트 × 검증가능성)

self_drift(H_9038)처럼 **GREEN WIRED** 갈 수 있는 것 = 작고 결정적·Ψ-disjoint·mini CPU $0 검증 우선.

| # | op | 난이도 | 임팩트 | 검증 | GREEN-WIRED 후보? | 근거 |
|---|-----|:---:|:---:|:---:|:---:|------|
| **1** | gap1 **conjunction readout** | LOW | MED | HIGH | ✅ 즉시 | top-2 재사용 10줄, 결정적 fixture, $0 |
| **2** | gap3 **ag_conflict monitor** | LOW | MED-HIGH | HIGH(monitor) | ✅ monitor leg | shuffle-falsify, consult 템플릿 존재 |
| **3** | C **TD-credit** | MED | HIGH | HIGH | ⏳ 2-leg | 지연보상 fixture, VBasalGate 확장 |
| 4 | D **lateral k-WTA** | MED | MED-HIGH | MED | ⏳ | population code 이점 입증 필요 |
| 5 | gap3 **conflict→exploration capability** | MED | MED-HIGH | MED(outcome) | ⏳ DIRECTIONAL | monitor 후 outcome leg |
| 6 | E **phase-binding** | HIGH | ? | ? | ❌ flag | H_1283 precedent 조회 먼저 |

**권고 실행순서:**
1. **#1 conjunction + #2 ag_conflict monitor** — 둘 다 LOW/HIGH-검증, self_drift 급 즉시 GREEN-WIRED 후보. 같은 사이클에 engine-native 재검증(byte-exact)+live wire(brain.hexa consult)+ARCHITECTURE lockstep 4칸 사다리(a_verified_must_wire) 닫기 가능.
2. **#3 TD-credit** — HIGH 임팩트(계획 깊이), MEDIUM 난이도. 지연보상이 진짜 새 능력.
3. #4·#5 는 monitor/기초 op 착지 후 capability leg.

**정직 caveat:**
- 이 문서는 **설계 발산**이다 — engine-native 실측 미실행(reference-match 읽기전용 제약). 각 op 의 verdict tier 는 `.hexa` fixture 실행 후에만 박제(a_engine_native_learning HARD-GATE). 여기 표는 **설계 우선순위**지 verdict 아님.
- gap1 결합기의 *재조합* 각도(additive compose)는 DPI 벽으로 **INERT 예상** — conjunction/co-occurrence 로 재프레임한 이유. 순진한 mean-compose 재발사 금지.
- gap3 capability leg 는 H_1836/1837 temporal-readout 🧱 교훈으로 갈등-*조건부* pre-register 필수(무조건 재샘플=DPI floor).

---

## 5. 산출 경로 + 도달점

- **이 문서:** `state/substrate_gaps_analysis/README.md` (gap1 결합기 현황+op · gap3 상충-loop op · 새 gap 4종 · 우선순위).
- **터치 안 함:** HYPOTHESES.jsonl·UNIVERSE cards·commit·PR·CHANGELOG·ARCHITECTURE·frozen verdicts. 동시 서브산출(g1_*·g6_*·gate_design_audit·consciousness_loopclose) 무접근.
- **도달점:** 설계 발산 **완료**(gap1·gap3 현황 정독 확정 + op 4종 설계 + 우선순위표). engine-native fixture 실행·verdict 박제는 **미실행**(읽기전용 제약 — 다음 실행 사이클에서 #1·#2 부터 `.hexa` fixture 로 GREEN-WIRED 4칸 닫기 권고).
