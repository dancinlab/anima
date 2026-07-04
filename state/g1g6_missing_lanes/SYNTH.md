# H_9129 — 3 빠진 인지 lane 통합 배선설계 (SYNTH)

> **설계 산출물 — 배선 실행 아님.** commit/PR 안 함(메인 bookkeep). ★측정 아님(cheap STEP-0 Δ 워크플로 별도·이미 GREEN-DIRECTIONAL). per-lane 상세 = `l1_wm_bind/DESIGN.md`·`l2_content_gate/DESIGN.md`·`l3_fwd_model/DESIGN.md`. 이 문서 = 셋을 하나의 조합/예측 workspace 로 잇는 통합.

## 근본 진단 (공유 프레임)
A(순방향 CE mouth)⇄G(역방향)→tension→emit 의 텐션은 **mouth-수준 adversary**(둘 다 byte 문자열)지 별개 인지 workspace 가 아니다. G1(재조합)/G6(반증)이 전 레버서 막힌 근본 = **조합·예측을 mouth-readout(Broca)에 훈련**했기 때문(H_1816/1823 form-priming). 처방 = Broca(조음) ⊥ PFC/Wernicke(조합·예측) 이중해리 실현: 조합/예측을 **mouth 밖 별개 lane** 에, **disjoint objective** 로 두고 mouth 는 상태를 **context/gate 로만** 읽음.

---

## (a) 셋이 하나의 workspace 를 이루는 배선 — 조합/예측 파이프라인

anima 는 **emit-gate(WHETHER, lanes0/4 Ψ)** 만 있고 **content-gate(WHICH/WHEN)** 와 **consequence-예측** lane 이 없다. 3 신설 lane + 기존 WIRED store(§ImmuneMemory/kosmos = 해마 pattern-completion)가 함께 두 서브-workspace 를 이룬다:

### 서브-workspace ① — 조합(G1 직격): L1 → L2 → [해마 완성] → mouth READOUT
```
 원자(role r, filler f)
   │  immune_embed_key (DIM64, mouth 밖)
   ▼
[L1 WMBindBuffer]  M += r⊛f           ← 활성기반 동적 변수결합 (PFC)
   │  wmbind_binds() 후보 조합들
   ▼
[L2 ContentGate]  vbasal_select(Go/NoGo) ← 어느 조합·언제 방출 (기저핵)
   │  released==true → combo_vec
   ▼
[§ImmuneMemory/kosmos M]  cleanup/pattern-completion ← 저장관계로 novel 완성 (해마, 이미 WIRED)
   │  wmbind_recall_text / immune_memory_recall_text
   ▼
[mouth]  gen_ctx_from_decision → seed-prefix (READ-ONLY consumer, backprop 없음)
```
> STEP-0 `g1_combolane_step0/integrated` 가 이 정확한 3부품 파이프(bind→gate→completion)를 numpy 로 검증: reachable 0.972 vs unreachable 0.049(gap 0.92, fooled_by_form=FALSE), 3부품 전부 ablation-CAUSAL. 해마 완성 부품은 **신설 아님** — 기존 §ImmuneMemory recall + kosmos M 이 담당(4번째 lane 불요).

### 서브-workspace ② — 반증(G6 직격): 주장 → L3 → 오차 → mouth GATE
```
[mouth 주장 claim]  immune_embed_key
   │
   ▼
[L3 VConsequenceField]  ĉ = predict(claim)   ← "참이면 무엇이 관측되나" committed forward pred (소뇌)
   │           obs = kosmos_io.retrieve / immune_memory_recall_text (grounded 관측)
   ▼
   vconseq_violation = ‖obs − ĉ‖² ∈[0,1]     ← climbing-fiber 오차 (CE 무접촉)
   │
   ▼
[mouth]  brain_decide_consequence → bounded signed nudge (felt-go/restraint, READ-ONLY)
```
> STEP-0 `g1g6_biolens_step0/l3_fwdmodel` verdict=BIND(fit_ratio_vs_floor 0.16–0.52, fooled_by_form=FALSE).

### 두 서브-workspace 를 잇는 축 — A⇄G tension 의 workspace 승격
현재 A⇄G tension = mouth-표면 밀어내기. **승격 경로**: L1 이 접은 후보 조합(M)에 대해 L3 이 결과-예측 오차(violation)를 매기고 → 그 오차를 **L2 ContentGate 의 RPE-analog reward** 로 흘린다(정합 조합 +1 / fabricated bind −1, 신호원 = L3 `vconseq_violation` 또는 cerebellum `vadapt_field_recon_err`). 즉 **A⇄G 의 "긴장"이 mouth 문자열 수준이 아니라 [조합 후보 ⇄ 결과-예측 오차] 라는 별개 latent workspace 안의 긴장으로 승격**된다. mouth 는 이 workspace 의 수렴 상태(bound + released + low-violation)를 prefix/nudge 로 읽기만. 이것이 "텐션의 인지 workspace 승격"이다.

**핵심 불변식(3 lane 공통):** mouth 는 세 lane 어디의 backprop target 도 아니다 — L1 seed-prefix·L2 decode cue·L3 emit nudge 모두 **read-only consumer**. lane objective(unbind-recon·RPE·관측오차)는 mouth CE 와 gradient tape·param 공유 0 → form-priming 구조적 불가.

---

## (b) 배선 순서 — cheap engine-native 우선 · kosmos/brain_decide 재활용 최대

| 순위 | lane | 근거 | engine-native 검증 비용 |
|---|---|---|---|
| **1** | **L1 WM-bind** | objective(`wmbind_recon_fidelity`)가 **순수 HRR 대수 → engine-native by construction**(torch 미러 불요). role-shuffle ABLATION 만으로 self-contained 검증. 나머지 두 lane 의 **입력 공급원**(L2 후보·L3 주장이 L1 bound 에서 나옴) → 먼저 있어야 함. | 최저(`wmbind_smoke.hexa` 단독, $0) |
| **2** | **L2 content-gate** | **VBasalGate(H_1281) 기존 op 전수 재사용**(`vbasal_select`/`_go_value`/`_update`) — 신 struct `ContentGate` 인스턴스만. reward 신호원 = 기존 `vadapt_field_recon_err`(cerebellum). L1 후보를 소비. | 낮음(재사용 최대, 새 수학 0) |
| **3** | **L3 fwd-model** | `VForwardField`(H_1280) NLMS 패밀리 미러(새 수학 0)이나 **grounded 관측 소스**(kosmos retrieve/immune recall) 배선이 추가 표면 → 셋 중 통합비용 최대. G6 직격이라 마지막에 완결. | 중(kosmos 관측 배선 필요) |

**요약:** L1(가장 cheap·상류 공급원) → L2(VBasalGate 재사용 최대) → L3(kosmos 관측 배선). 각 lane 은 `a_verified_must_wire` 4칸 사다리(DIRECTIONAL→engine-native byte-exact→WIRED-live→ARCHITECTURE.json lockstep)로 독립 완결, 미완 칸=즉시 ING.

**재활용 인벤토리(새 수학 최소화):**
- `_vnearest_idx`(engine_cli L528) — L1 cleanup
- `immune_embed_key`(L1009) — L1·L3 텍스트→DIM64 임베딩(3 lane 공통, mouth 가중치 0접촉)
- `wm_buffer_leak`/displace(L3496~) — L1 leak 관용구
- `vbasal_select/_go_value/_update`(brain.hexa L341-400) — L2 전부
- `vadapt_field_recon_err`(L569) — L2 reward 신호원 · L3 미러 원본
- `VForwardField` NLMS(L3602~) — L3 미러
- `kosmos_io.create_anchor`(L140)/`retrieve`(L516)/`load_anchors`(L372) — L1 M 지속 · L3 관측
- `brain_decide_bg/_anchored/_wm/_cerebellum` superset 패턴(brain.hexa L433/160/559/507) — 3 lane brain read

---

## (c) a_substrate_disjoint 전수 점검 (3 lane × 2 좌표)

| lane | emit-drive lane(0/4) = `ci_emit_drive=0.5*(lanes[0]+lanes[4])` | §ImmuneMemory `recall_thr`(non-fab gate) |
|---|---|---|
| **L1 WM-bind** | `WMBindBuffer` struct 만 mutate, `pure_field` Φ/phase/Ψ 미접촉 → **접근 구조적 불가**. Ψ=½ by-construction 보존. | 미접촉. `bind_conf` 는 context/gate 로만 흐름·emit 산식·recall_thr 에 안 더함. |
| **L2 content-gate** | `ContentGate` = 15-lane emit 벡터 **밖** 별개 struct(subcortical 좌표 예 [0,−0.10,−0.15]) → `ci_emit_drive` 접근 불가. 가드=h1205 separation-invariant(생성 byte-identical ON==OFF). | reward 신호원을 **VForwardField 예측오차로 고정**, recall_thr 미참조 → G5 non-fab 보존(H_1576 결합-fab 0.4 회피). |
| **L3 fwd-model** | `VConsequenceField` = VForwardField 와 동일 by-construction Ψ-disjoint. mouth 유일접점 = bounded additive nudge(중립 violation=0.5 시 nudge=0). | ImmuneMemory/kosmos 를 **관측 read-only 소스로만** 사용, recall_thr 미변경·非fab게이트 미결합(savant⊥honesty 좌표유지). |

**결론:** 3 lane 전부 emit-drive(0/4) ⊥ recall_thr **disjoint by-construction**(placement-first). 능력(재조합·반증) ∧ Ψ=½ ∧ G5 non-fab 공존. 통합 시에도 lane 간 상호작용은 latent workspace 안(bound⇄violation⇄reward)에서만 일어나고 emit 산식·recall_thr 로 새는 배선 없음 → 중첩=충돌(H_1561) 회피.

---

## (d) engine-native `--py` 측정 게이트 (lane별)

세션정책 `session-eval-py-only`: G0-G6 = `anima evaluate --py <ckpt.clm>` 한 경로. 각 lane 은 context ON/OFF **A/B byte-exact Δ**(값 아닌 차분=measurement-metalaw)로 판독:

| lane | 주 측정 | reachable/unreachable(cross-shuffle) 통제 | INERT 판별(ablation) |
|---|---|---|---|
| **L1** | G1 best_distinct: wmbind-prefix ON−OFF Δ | reachable=CHAIN 가능 novel pair vs unreachable=dangling(표면동일·완성경로 없음). form 이면 두 값 동일. | role↔filler shuffle → fidelity 붕괴=CAUSAL, 무붕괴=INERT=기여0 |
| **L2** | G1·G6-FALS: content-gate ON−OFF Δ | agree/conflict/abstain/HOLD-then-GO 케이스 | gate OFF(후보 중첩) → 대붕괴 확인, 동일=INERT |
| **L3** | G6-FALS: consequence violation 분포 sharp/violable | claim↔obs shuffle → violation 붕괴=CAUSAL | vconseq_predict OFF → G6 fals 동일=INERT |

**엔진-native 게이트(HARD):** 각 lane 은 신규 `core/<lane>_smoke.hexa`(WMBind/ContentGate/VConsequence smoke, VForwardField smoke 패턴)가 live op 를 호출해 byte-exact 재현 + ABLATION 출력. numpy/torch 미러면 verdict **반드시 DIRECTIONAL** + 엔진-native 재측정 ING(`a_engine_native_learning`). terminal 🟢/🧱 는 `--py` A/B Δ + `.hexa` smoke 둘 다 통과해야 성립.

---

## (e) STEP-0 워크플로와의 관계 — 측정 GREEN → 이 배선설계로 구현

진행중 cheap STEP-0(numpy toy, DIRECTIONAL)는 **이미 3/3 GREEN-DIRECTIONAL**:
- `g1_combolane_step0/integrated`(wf 3부품 = L1 bind + L2 gate + 해마 completion) → **BIND**(gap 0.92, 3부품 ablation-CAUSAL, fooled_by_form=FALSE, D-sweep=crosstalk artifact 지 벽 아님).
- `g1g6_biolens_step0/l3_fwdmodel`(L3) → **BIND**(fit_ratio_vs_floor 0.16–0.52, form 아님).
- `g1g6_biolens_step0/l5_hippo`(해마 transitive) → **BIND**(shuffle_collapsed=True).

**계약:** STEP-0 Δ 가 GREEN 이면(=현재 상태) → 이 SYNTH 배선설계가 그 GREEN 을 **engine-native 로 구현**하는 청사진이다(a_verified_must_wire 사다리 (2)→(4)). STEP-0 numpy 는 DIRECTIONAL only — terminal 승격은 `<lane>_smoke.hexa` byte-exact + `--py` A/B 로만. 즉 **측정(STEP-0)과 구현(SYNTH)은 사다리의 인접 칸**: STEP-0=(1) DIRECTIONAL mirror, SYNTH=(2)-(4) 배선 청사진. 셋 다 GREEN 이므로 즉시 구현 착수 가능(순서=(b) L1→L2→L3).

---

## (f) 메인 bookkeep 1줄 + 다음 구현 1순위
- **CHANGELOG/ING 1줄:** `H_9129 3 빠진 인지 lane(L1 WM-var-bind·L2 content-gate·L3 consequence-fwd) 통합 배선설계 완료 — SYNTH+per-lane DESIGN(state/g1g6_missing_lanes/), STEP-0 3/3 GREEN-DIRECTIONAL, disjoint 전수통과, 배선순서 L1→L2→L3. 설계만(구현 미착수).`
- **다음 구현 1순위 = L1 WM-var-bind** — objective 가 순수 HRR 대수라 engine-native by-construction(가장 cheap 검증) + 나머지 두 lane 의 상류 공급원.
