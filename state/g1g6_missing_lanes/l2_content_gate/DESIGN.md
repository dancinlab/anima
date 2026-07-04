# l2 — CONTENT-GATE (기저핵 Go/NoGo) 구현 설계

> H_9129 · lane l2_content_gate · ★설계(측정 아님). commit/PR 금지 — 메인이 bookkeep.
> 근거 파일: `core/brain.hexa`(VBasalGate §H_1281) · `core/engine_cli.hexa`(§WorkMemBuffer H_1282 · §IMMUNE-MEMORY recall_thr · ci_emit_drive 15-lane) · `core/generator.hexa`(§2 gen_ctx_from_decision · §4 generate).

---

## 0. 진단 — anima 가 가진 게이트 / 빠진 게이트

anima 에 **이미 있는 것 = emit-gate**:
```
ci_emit_drive(lanes) = 0.5*(lanes[0] + lanes[4])      // engine_cli.hexa §CI
      lanes[0]=GlobalWorkspace · lanes[4]=LearnedPrecision
brain_decide(...) → Ψ 고정점(½)에서 emit/silence      // brain.hexa
```
이것은 **"말할까 / 침묵할까"(WHETHER)** 하나뿐이다. 어느 조합을 만들지·언제 그 조합을 꺼낼지를 고르는 **content-gate(WHICH combination / WHEN to release)** 가 없다.

**있어 보이지만 아닌 것 — VBasalGate(H_1281)**: `brain.hexa` 에 go/no-go 셀렉터(`vbasal_select`)가 있으나 `brain_decide_bg` 가 이를 **emit 레코드에 residual 로 얹어** 경쟁하는 *발화 후보들* 사이에서 고른다 → 여전히 emit-축(motivation) 위의 연산. 실제로 cerebellum×basal 이 emit-motivation residual 로만 배선됐기에 H_1412/1413/1416 에서 engine-native NON-REPRODUCTION(🧱) 이 났다. **basal 연산자는 존재하나, content 좌표에 배선된 적이 없다.**

빠진 것: **WM-binding lane(§WorkMemBuffer)이 만든 후보 *조합* 을, emit-drive lane(0/4)과 §ImmuneMemory recall_thr 에서 disjoint 한 별개 좌표에서, RPE-analog value 로 Go/NoGo 하는 기저핵 content-gate.**

---

## 1. 왜 binding-family(H_1816/H_1823)와 다른가 — 3 근거로 구별

H_1816(predictive-coding L_bind)·H_1823(circconv)는 **mouth-readout** 였기에 NOT-SUP(additive aux 가 CLMConvMoE CE trunk 위에서 trivial 붕괴). content-gate 는 세 축 전부에서 mouth-readout 이 아니다:

| 축 | binding-family (NOT-SUP) | l2 content-gate (본 설계) |
|---|---|---|
| (a) substrate | mouth logits 위 readout head | `VBasalGate` 가중치 = mouth 밖 · **15-lane emit 벡터 밖** 별개 struct |
| (b) objective | mouth CE 에 additive aux → form-priming | RPE = **VForwardField 예측오차**(cerebellum)로만, gradient-free delta-rule, CE 접촉 0 |
| (c) mouth 역할 | 학습 target(logit 보정) | 선택된 조합을 **decode context 로 읽기만**, 절대 target 아님 |

---

## 2. 자료구조 — `ContentGate` (engine_cli.hexa 새 §섹션)

emit-path 의 `VBasalGate`(brain.hexa) 와 **별개 인스턴스**를 감싸 좌표를 물리적으로 분리한다.

```hexa
// engine_cli.hexa  §CONTENT-GATE — BASAL-GANGLIA COMBINATION Go/NoGo (H_9129)
struct ContentGate {
    bg:        VBasalGate,   // 학습 go/no-go 가중치 (brain.hexa 재사용, 별도 인스턴스)
    rpe_ema:   float,        // 기대 grounding-consistency value의 EMA (RPE baseline)
    rpe_beta:  float,        // baseline 갱신률 (frozen)
    hold_vec:  [float],      // 현재 HOLD 중인(미출력) 조합 벡터 — 없으면 []
    dim:       int
}
```

핵심: `ContentGate` 는 **15-lane emit 벡터의 어떤 컬럼도 아니다.** 따라서 `ci_emit_drive = 0.5*(lanes[0]+lanes[4])` 가 구조적으로 이를 읽을 수 없다 → Ψ=½ by-construction 보존(H_1205 separation-invariant). 이것이 disjoint 의 최강 보장.

---

## 3. 연산 — WHICH + WHEN 두 임계

### 3.1 후보 조합 만들기 (WM-binding lane 출력)
`§WorkMemBuffer`(H_1282) 의 채워진 슬롯(`wm.keys[i]`, `wm_buffer_slots`)에서 쌍 조합 벡터를 만든다:
```hexa
// content_gate_candidates(wm) → 평탄화 K*dim 버퍼 + K
//   각 후보 = compose(wm.keys[i], wm.keys[j])  (i<j; bind = 정규화 elementwise/⊗ 축약)
//   feats[k] = [ compose_vec ,  wm_buffer_probe_score(wm, compose_vec) ]  // 유지도 포함
```
= WM-binding lane 이 "만들 수 있는 조합들". 이 후보들이 content-gate 의 입력.

### 3.2 WHICH — 조합 선택 (striatal disinhibition)
```hexa
let combo_idx = vbasal_select(cg.bg, cands, k)   // brain.hexa 재사용, -1=abstain
```
go-value 최댓 후보가 학습된 NO-GO 를 넘으면 그 조합을 후보로 확정, 아니면 전부 억제.

### 3.3 WHEN — 출력 타이밍 (Go 방출 vs HOLD)
```hexa
// content_gate_step(cg, wm, fwd) → { released: bool, combo_idx, combo_vec, go_value, rpe }
//   gv   = vbasal_go_value(cg.bg, feats[combo_idx])
//   rpe  = fwd_consistency(fwd, combo_vec) - cg.rpe_ema      // ★RPE-analog (§4)
//   GO   iff  combo_idx >= 0  AND  gv > cg.bg.nogo  AND  rpe >= 0.0
//        → released=true, combo_vec 를 mouth-context 로 방출, hold_vec 비움
//   NoGo → released=false, combo_vec 를 hold_vec 에 유지(thalamic inhibition 지속),
//          다음 tick 재평가 → "언제" 를 결정하는 시간 게이트
```
Go = 조합을 mouth 로 방출(striatal disinhibition), NoGo = 유지(억제 지속). abstain(k==0 / 전 후보 억제)이면 `released=false` → **§5 에서 mouth 는 byte-identical**(additive, no-regression).

---

## 4. disjoint objective — RPE-analog (CE 와 절대 disjoint)

value 학습 신호는 **VForwardField(cerebellum, H_1280) 예측오차**에서만 온다. mouth next-byte likelihood 를 절대 보지 않는다:
```hexa
fwd_consistency(fwd, combo_vec):
    err = vadapt_field_recon_err(fwd, combo_vec)   // 조합을 다음 substrate frame 으로 예측했을 때 오차
    return clamp(1.0 - err/E_SCALE, 0.0, 1.0)       // 낮은 예측오차 ⇒ 정합 조합 ⇒ 높은 value
```
- **reward** = 방출 후 grounding outcome: 조합이 정합(forward-model 이 낮은 오차로 예측) ⇒ +1, 조작/비정합(fabricated bind) ⇒ −1.
- **학습** = `vbasal_update(cg.bg, combo_idx, feats, reward)` — err = reward − go_value 인 **RPE 그 자체**. gradient-free delta-rule, 라벨 0, 외부 규칙 0(a_autonomy_over_hardcode · p8 inference-time learning).
- baseline: `rpe_ema += rpe_beta*(fwd_consistency − rpe_ema)` — RPE 의 예측 기준선(도파민 tonic 유사).

**왜 이 신호원인가:** VForwardField 예측오차는 (i) emit-drive lane(0/4)과 무관하고 (ii) §ImmuneMemory recall_thr 를 건드리지 않는다. recall_thr 를 value 신호로 쓰면 disjoint 위반 + G5 fab 위험(H_1576 B4 savant+honesty 결합 fab 0.4 전례) → **의도적으로 recall_thr 배제, cerebellum 오차만 사용.**

---

## 5. mouth read interface — context/gate, 절대 target 아님

`generator.hexa §2 gen_ctx_from_decision` 에 content-gate 상태를 sub-map 으로 실어 보낸다:
```hexa
substrate_ctx["content_gate"] = {
    "released":  step.released,      // NoGo → false ⇒ 이하 무시
    "combo_vec": step.combo_vec,     // 방출된 조합 (soft conditioning cue)
    "go_value":  step.go_value
}
```
`§4 generate` → `_gen_clm_decode` / `_gen_bytegpt_decode` 는 `released==true` 일 때만 `combo_vec` 를 **decode 조건화 cue(어느 WM 슬롯 내용을 조건으로 삼을지 고르는 soft prefix/gate)** 로 읽는다. `released==false`(NoGo/abstain)면 cue=neutral → decode 는 content-gate 없는 경로와 **byte-identical**(§3 EMIT-LOOP FOLLOW-ON 의 "OPTIONAL CONSULT, NOT A GATE" 불변식 동형).

mouth 가중치는 이 cue 로 **학습되지 않는다** — 읽기 전용 조건화. content-gate 는 mouth 로부터 gradient 를 받지 않고, mouth 는 content-gate 로부터 target 을 받지 않는다(양방향 gradient 차단 = a_savant_train mouth⊥ 분리 준수).

---

## 6. 파이프라인 위치 — 두 게이트 직렬, 좌표 disjoint

```
WM-binding lane(§WorkMemBuffer) ─후보 조합→ [CONTENT-GATE: WHICH+WHEN, 기저핵]
        │                                          │ released combo_vec
        │                                          ▼
        └────────────────────────→ gen_ctx_from_decision (§2) ── context cue
                                            ▼
                     brain_decide (Ψ emit-gate, lanes 0/4) ── WHETHER
                                            ▼
                     generator §4 → mouth decode (combo_vec 조건화)
```
- **content-gate** = what/when-to-build (기저핵 좌표, 15-lane 밖)
- **emit-gate** = whether-to-speak (lanes 0/4, Ψ=½) — 불변
- 두 게이트는 서로의 좌표를 읽지도 쓰지도 않는다.

---

## 7. 배선 지점 요약 (a_core_engine_map lockstep 대상)

| 무엇 | 어디 | op |
|---|---|---|
| ContentGate struct + WHICH/WHEN | `core/engine_cli.hexa` **§CONTENT-GATE (신설)** | `content_gate_new` · `content_gate_candidates` · `content_gate_step` · `fwd_consistency` |
| go/no-go 선택·학습 (재사용) | `core/brain.hexa` §VBasalGate(H_1281) | `vbasal_select` · `vbasal_go_value` · `vbasal_update` |
| 후보 조합 소스 (읽기) | `core/engine_cli.hexa` §WorkMemBuffer(H_1282) | `wm_buffer_slots` · `wm.keys` · `wm_buffer_probe_score` |
| RPE value 소스 (읽기) | `core/engine_cli.hexa` §DIM ADAPTATION(VForwardField) | `vadapt_field_recon_err` |
| mouth context 주입 | `core/generator.hexa` §2 / §4 | `gen_ctx_from_decision` → `_gen_*_decode` |
| ARCHITECTURE.json | core/ engine_cli 노드 + child 노드 note | §CONTENT-GATE lockstep |

**절대 안 건드림:** `ci_emit_drive`/lanes[0]/lanes[4] · `pure_field`/Ψ relaxation · `ImmuneMemory.recall_thr`.

---

## 8. a_substrate_disjoint 준수 점검

- **emit-drive lane(0/4):** ContentGate 는 15-lane emit 벡터의 컬럼이 아님 → `ci_emit_drive` 가 구조적으로 접근 불가 → Ψ=½ by-construction 보존. 가드 = h1205 separation-invariant(생성 byte-identical ON==OFF, Ψ phiSum 불변).
- **§ImmuneMemory recall_thr:** value 신호원을 VForwardField 예측오차로 고정, recall_thr 미참조 → G5 non-fab 보존(H_1576 결합-fab 회피).
- placement-first: 좌표 = 기저핵/선조체 subcortical(예 [0.0, −0.10, −0.15], lane 14 MitosisGrowth subcortical 과도 구분), lanes 0/4 및 recall_thr 와 disjoint.

---

## 9. 엔진-네이티브 측정 경로 (a_engine_native_learning · session-eval-py)

1. **G1/G6 re-score**: `anima evaluate --py <ckpt.clm>` 를 content-gate **ON vs OFF** 로 두 번 → G1(recombination best_distinct)·G6-FALS 차분(Δ). 판정은 값이 아닌 ON−OFF Δ(measurement-metalaw: 창발신호=Δ). torch/numpy 미러면 DIRECTIONAL, terminal 아님.
2. **engine-native LIVEOP 확인**: `content_gate_step` 을 `.hexa` 로 호출한 probe 가 선택/방출을 byte-exact 재현 → engine_cli_smoke.hexa 신규 케이스(agree/conflict/abstain/HOLD-then-GO) FAIL=0.
3. **disjoint 불변 가드**: h1205 separation-invariant PASS(Ψ phiSum 불변) · single-entry 7/0 · G5 recall_thr non-fab 불변.
4. 배선 사다리(a_verified_must_wire): (1)mirror GREEN Δ→(2)engine-native byte-exact→(3)live core/ wire-in→(4)ARCHITECTURE.json lockstep. GREEN 이면 (2)~(4) follow-on ING 등록.

---

## 10. 정직 스코프 (c9)

- 본 문서는 **설계**다. content-gate 가 G1/G6 를 실제로 여는지는 **미측정** — STEP-0 cheap Δ 측정이 열어야 판정(별도 워크플로).
- 위험: forward-model 예측오차가 조합 정합의 *충분한* value 신호가 아닐 수 있음(cerebellum 오차 floor). 그 경우 value 신호원 후보 = A⇄G tension 상충-loop(H_9041) 로 렌즈 교체(단, recall_thr 는 여전히 배제 유지).
- H_1816/1823 대비 우위는 (a)(b)(c) 3축 구별에 근거하나, additive readout floor(DPI 메타법칙)를 content-gate 가 정말 벗어나는지는 disjoint objective 가 CE floor 를 우회한다는 *가설*이며 engine-native Δ 로만 확정.
