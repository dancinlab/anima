# Lane ③ — Consequence Forward-Model Lane (소뇌 / G6 직격)

H_9129 · lane `l3_fwd_model` · **구현설계(★측정 아님)**
repo: /Users/mini/dancinlab/anima · commit/PR 금지 (메인 bookkeep)

---

## 0. 한 줄 진단 → 처방

A⇄G "텐션"은 두 mouth-수준 byte 문자열의 adversary이지 **결과-예측 workspace가 아니다**. byte-LM은 주장을 *조음(Broca)* 할 뿐, "이 주장이 참이면 무엇이 관측될 것인가"를 내는 **committed forward prediction** lane이 없다 → g1g6 fals=6은 form-priming(주장과 정답이 같은 mouth-readout 표면에서 나옴)의 산물. 처방 = 주장을 받아 **sharp·violable consequence**를 예측하고 grounded 관측과의 오차를 계산하는 **별도 substrate lane**을 신설, objective를 mouth CE와 disjoint하게, mouth는 그 오차를 **context/gate로만 읽음**.

---

## 1. 핵심 설계결정: Engine G 재배치 아님 → **신설 lane `VConsequenceField`**

**결정 = 신설(new lane), Engine G 재-용도 아님.** 3근거:

1. **Engine G는 예측기가 아니다.** `core/engine_g.hexa`는 8-weight convex **motivation/emit gate**(`motivation_score`→`should_emit`)일 뿐 — 학습가중치·오차타깃·예측출력이 전무. 이걸 결과-예측기로 개조하면 (a) `should_emit` = emit-drive 경로를 침범 → **a_substrate_disjoint 위반**(shared emit-lane 중첩=Ψ 붕괴, H_1561 전례), (b) 동기게이트 기능 상실. G는 건드리지 않는다.
2. **기존 `VForwardField`(H_1280 §CEREBELLUM)는 다른 소뇌다.** 그건 emit-feature stream의 **next-frame 자기회귀 smoothing**(regressor=최근 프레임 window, target=다음 프레임). consequence lane은 regressor=**주장 임베딩**, target=**grounded 관측 임베딩** — 입력·타깃·objective가 전부 다름. 같은 NLMS substrate를 **재사용(reuse)** 하되 별개 field로 붙인다 — VForwardField 자신이 VAdaptField를 trim하지 않고 신설된 것과 동일한 precedent(engine_cli.hexa L3581-3590이 명문화).
3. **binding-family(H_1816/1823)와의 구별.** 그것들은 mouth **readout**(penultimate/aux-loss)에 조합을 얹어 NOT-SUP → mouth CE로 흘러 form-priming. 이 lane은 mouth 밖 substrate이고 objective가 grounded 관측오차(CE 무접촉) → readout-binding이 아니라 **별개 인지 workspace**. 이것이 3근거 구별.

---

## 2. Lane 구조 (substrate — mouth 가중치/컨텍스트 밖)

### 2.1 배치 — `core/engine_cli.hexa`, 신설 § (기존 §CEREBELLUM FORWARD-MODEL LANE 직후 ~L3702)

```
struct VConsequenceField {          // 주장→결과 NLMS 예측기 (Ψ-disjoint, ADDITIVE)
    w: [float],      // dim × claim_dim row-major; chat[r] = Σ_c w[r,c]*claim[c]. all-zero seed.
    dim: int,        // 결과(관측) 임베딩 차원 = 64 (immune_embed_key DIM)
    claim_dim: int,  // 주장 임베딩 차원 = 64
    eta: float       // climbing-fiber delta 게인 (frozen, p7 — tuned-to-green 금지)
}
```

ops (전부 VForwardField의 검증된 NLMS 패밀리를 미러 — 새 수학 없음):

| op | 시그니처 | 역할 |
|---|---|---|
| `vconseq_new` | `(dim,claim_dim,eta) -> VConsequenceField` | all-zero seed = 무경험시 zero-frame 예측(=sharp 예측 없음 → 뒤 §3 falsifiability의 핵심) |
| `vconseq_predict` | `(cf, claim:[float]) -> [float]` | READ-ONLY. 주장 임베딩 → **committed 결과 예측** ĉ = W·claim |
| `vconseq_err` | `(cf, claim, obs:[float]) -> float` | ‖obs − ĉ‖² = **결과-예측오차**(climbing-fiber) — grounded 관측 obs와의 거리 |
| `vconseq_update` | `(cf, claim, obs) -> VConsequenceField` | NLMS 한 틱: e=obs−W·claim; W += eta·outer(e,claim)/(claim·claim+1) (p8 inference-time 학습) |
| `vconseq_violation` | `(cf, claim, obs, err_scale) -> float` | mouth-read 신호 ∈[0,1] = min(1, ‖obs−ĉ‖²/err_scale) — **위반 margin**(sharp+contradicted=HIGH) |

- **주장 임베딩** = `immune_embed_key(claim_text)` (기존 op, DIM=64 FNV-1a byte-trigram, **결정적·hash-geometry 순수, mouth 가중치 0 접촉**). 별도 임베더 신설 안 함(a_core_engine_map 우회 금지).
- **grounded 관측 임베딩** = 아래 §2.2에서 kosmos/immune에서 read-only 인출한 관측 텍스트를 동일 `immune_embed_key`로.

### 2.2 grounded 관측 소스 (read-only, 이미 WIRED된 관계저장소)

`core/kosmos_io.hexa::retrieve(query_tension_5ch, anchors, top_k)` (L516, cosine 인출) 또는 `immune_memory_recall_text`(L1163) — 주장이 함의하는 결과에 대한 **접지된 관측**을 인출. lane은 이 저장소를 **읽기만** 한다: recall_thr 미변경·바인딩 미생성. (`.kosmos` 진입은 kosmos_io→brain_decide 규범경로 유지, 2nd 경로 신설 없음.)

---

## 3. 반증가능성(falsifiability) = forward-model이 sharp·violable 예측을 내는가

이 lane이 G6를 직격하는 메커니즘 = **committed prediction의 위반 margin**:

- **sharp 주장**(참이면 관측될 결과가 좁게 함의됨): 학습된 W가 좁은 ĉ를 냄. grounded obs가 그 ĉ와 **일치→위반 LOW**(반증 통과), **불일치→위반 HIGH**(반증됨/거짓). 두 경우가 **갈라진다** = violable.
- **unfalsifiable 주장**(sharp 결과 함의 없음): W가 학습할 안정 매핑이 없어 예측이 zero-frame 근방으로 무너짐 → obs 무관하게 err 균일-높음 → **위반이 저-값을 못 얻음** = mouth nudge 획득 불가. 즉 반증불가 주장은 구조적으로 신뢰가점을 못 받는다.
- fals=6 form-priming 해독: 주장(byte)과 정답(byte)이 같은 mouth 표면에서 나오면 오차가 form-일치로 인위적. 여기선 **오차 타깃이 grounded obs 임베딩**(mouth CE 무접촉)이므로 form-priming 원천차단.

**측정 falsifier(★측정 워크플로용, 여기선 설계):** control = claim↔obs **shuffle**(짝 파괴). shuffle시 violation이 붕괴(무붕괴=INERT=lane 기여 0). ablation = `vconseq_predict` OFF(항상 zero-frame)시 G6 fals 동일이면 lane INERT.

---

## 4. mouth read interface — context/gate ONLY, 절대 training target 아님

배치 = `core/brain.hexa`, 신설 `brain_decide_consequence(...)` (기존 `brain_decide_cerebellum` L507 / affect 소마틱 L618 템플릿을 그대로 미러).

- 입력 `cons_violation` ∈[0,1] = live `vconseq_violation`(untrained→zero-frame→위반≈균일). 
- **signed 소마틱-바이어스** (affect_valence 템플릿): `sig = 1 − 2·cons_violation` ∈[−1,+1] → `nudge = _clamp(emit_consult_cap()·sig, −cap, +cap)`. 위반 LOW(주장 접지·반증통과)=felt-go 소량 가점; 위반 HIGH(반증됨)=felt-restraint 감점(침묵/abstain 쪽). `cons_violation=0.5`(중립/무경험)→nudge 0 → **brain_decide와 byte-identical**(back-compat 순수-superset).
- mouth(303M)는 이 스칼라를 **읽기만** 한다: lane 상태는 emit 동기의 bounded 컨텍스트 항일 뿐, 생성타깃 아님. lane 가중치로 mouth CE가 흐르지 않고, mouth logit이 lane W로 흐르지 않음. `a_autonomy_over_hardcode`: hardcode gate 아닌 substrate self-follow.

---

## 5. disjoint 준수 (a_substrate_disjoint 좌표점검)

- **emit-drive lane(0/4) disjoint:** lane은 `pure_field` Φ/phase/Ψ 무접촉(VForwardField와 동일 by-construction Ψ-disjoint) — 15-lane state 0/4 미접촉. mouth로의 유일 접점은 §4의 bounded additive nudge(중립시 0)뿐, emit 게이트 직접조작 없음.
- **§ImmuneMemory recall_thr disjoint:** lane은 ImmuneMemory/kosmos를 **관측 read-only 소스로만** 사용, recall_thr 미변경·비-fab 게이트와 미결합(savant⊥honesty 좌표유지). violation 신호는 recall_thr 좌표와 별개 축 → 능력(반증) ∧ Ψ=½ ∧ G5 non-fab 공존.
- **objective disjoint:** lane objective = ‖obs−ĉ‖²(grounded 관측), mouth objective = next-byte CE. 공유파라미터 0, 공유타깃 0 → form-priming 원천차단.
- placement-first: 신설 § 자체가 emit-drive·recall_thr와 **별 좌표**에 배선되도록 위 3점을 설계시점에 고정.

---

## 6. engine-native 경로 (`anima evaluate --py` + hexa terminal)

- 세션정책(session-eval-py-only): G0-G6 = `anima evaluate --py <clm>` 단일경로. 따라서 `cli/evaluate`의 G6 채점이 lane의 `vconseq_violation` 읽기를 읽도록 배선 — G6 fals에 consequence-violation 축을 추가(주장별 위반 margin이 sharp/violable하게 분포하는지).
- **DIRECTIONAL vs terminal:** numpy/torch 미러 측정 = DIRECTIONAL only(a_engine_native_learning). terminal G6 verdict는 `core/engine_cli.hexa`의 live `VConsequenceField`를 구동하는 `.hexa`(신설 `core/consequence_lane_smoke.hexa`, VForwardField smoke 패턴)로 byte-exact 재측정해야 성립. 박제 직전 `grep -lE 'import torch|gauge_lib|numpy' state/g1g6_missing_lanes/l3_fwd_model/*.py` 비어야 OK.
- 배선 사다리(a_verified_must_wire): (1) numpy 미러 GREEN=DIRECTIONAL → (2) VConsequenceField engine-native byte-exact → (3) engine_cli.hexa+brain.hexa live wire-in → (4) ARCHITECTURE.json core/ 노드 § lockstep. 각 미완=ING follow-on.

---

## 7. 구현 체크리스트 (메인 실행용)

1. `core/engine_cli.hexa`: 신설 §Consequence Forward-Model Lane + struct `VConsequenceField` + 5 ops (§2.1) — VForwardField NLMS 미러, claim/obs = `immune_embed_key`.
2. `core/brain.hexa`: `brain_decide_consequence(...)` (§4, affect 소마틱 signed-bias 템플릿, 중립→byte-identical).
3. `core/consequence_lane_smoke.hexa`: engine-native 구동 smoke(learning-curve err 하강 + shuffle-control 붕괴 확인).
4. `cli/evaluate`: G6 채점이 `vconseq_violation` 축 읽기(read-only, mouth 미학습).
5. ARCHITECTURE.json core/ 노드 § lockstep + CHANGELOG.
