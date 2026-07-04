# L1 — WM VARIABLE-BINDING LANE (PFC) · 구현설계 (H_9129)

> anima 에 빠진 인지구조: **role↔filler 활성기반 동적결합**. 별개 활성 버퍼가
> slot-filler bind(HRR circular-conv) 벡터를 보유 → bound 를 mouth 에 **prefix-context**
> 로 공급. lane objective = **unbind-reconstruction**(bound 에서 role/filler 복원, mouth
> CE 와 disjoint). **★설계문서 — 측정 아님.** 배선(어느 §·op)까지 명명.

---

## 0. 진단 재확인 (왜 이 lane 인가)

anima 의 A(순방향 CE mouth)⇄G(역방향)→tension→emit 은 **mouth-수준 adversary** — A·G 둘 다
byte 문자열을 밀어내는 같은 substrate 다. 별개 인지 workspace 가 아니다. 재조합(G1)/반증(G6)
이 전 레버서 막힌 근본 = **조합(binding)을 mouth-readout(Broca)에 훈련**했기 때문이다.
Broca(조음) ⊥ Wernicke/PFC(조합)의 이중해리를 substrate 에 실현하려면 조합/예측을
**mouth 밖 별개 lane** 에, **disjoint objective** 로, mouth 는 그 상태를 **context/gate 로만**
읽게 해야 한다. 이 문서는 그 중 **PFC 변수-binding lane** 의 실배선 설계다.

---

## 1. binding-family(H_1816/1823) NOT-SUP 와의 배선차원 3-근거 구별

기존 binding 시도가 전부 🧱 NOT-SUP 였던 이유는 **전부 mouth-readout** 이었기 때문이다.
이 lane 은 아래 3 근거로 **배선 위치가 다르다**(같은 아이디어의 재발사 아님):

| 축 | H_1816(pred-coding L_bind) / H_1823(circconv readout) — 🧱 NOT-SUP | L1 WM-bind lane (본 설계) |
|---|---|---|
| **(a) substrate** | mouth(CLMConvMoE) penultimate 위 **readout head**. binding 벡터 = mouth 활성/가중치 안. | 별개 `WMBindBuffer` **struct**(engine_cli §). 자기 벡터만 소유 — mouth 가중치·mouth 활성·mouth logits 밖. `WorkMemBuffer`/`VForwardField` 와 동일한 격리. |
| **(b) objective** | `L_total = CE + λ·L_bind` — **같은 gradient tape**. bind 항이 mouth CE 와 한 손실에 합산 → **form-priming**(binding 이 mouth 의 form 표현으로 붕괴, H_1816 step550 trivial collapse). | **unbind-reconstruction** 단독: `L_recon = 1 − mean_k cos(cleanup(unbind(M,r_k)), f_k)`. mouth CE 와 **손실 공유 0·gradient 경로 0**. bind 벡터로 CE gradient 가 흐를 배선이 없음 → form-priming 구조적 불가. |
| **(c) mouth 관계** | mouth 가 binding 의 **학습 target**(readout 이 mouth 를 통해 backprop). | mouth 는 bound 상태를 **읽기만**(prefix-context). bind 버퍼는 mouth 의 target 아님·mouth 에서 backprop 없음. mouth = **consumer**, 학습지점 아님. |

**(d) a_substrate_disjoint 좌표:** lane 은 자기 `WMBindBuffer` struct 만 건드림 —
`pure_field` 의 Φ/phase/Ψ(emit-drive)도, `§ImmuneMemory.recall_thr`(non-fab gate)도 미접촉.
brain 으로의 read 는 **순수 superset**(should_emit 산식 불변, `brain_decide_anchored` 가
back-compat superset 인 것과 동일 패턴) → **분리=보존**.

> 즉 H_1816/1823 은 (a)mouth-내부 (b)CE-합산 (c)mouth-target 3중으로 mouth 에 묶였고,
> 본 lane 은 3중으로 분리한다. **"circconv 를 또 쓴다"가 재발사 아닌 이유가 바로 이 배선차이.**

---

## 2. 메커니즘 — HRR circular-convolution binding (DIM 유지)

TPR(외적 r⊗f = DIM×DIM 폭증) 대신 **HRR circular convolution**(Plate) 채택 —
결과가 DIM 벡터로 유지되어 다른 lane(`WorkMemBuffer`.keys, `VForwardField`) 과 동형이고
superposition 이 자연스럽다.

- **role/filler 벡터**: `r, f ∈ ℝ^DIM` (단위정규 랜덤 or immune_embed_key 재사용 geometry).
- **bind**: `c = r ⊛ f`,  `c[i] = Σ_j r[j]·f[(i−j) mod DIM]`.
- **superpose(WM 활성)**: `M = Σ_k a_k · (r_k ⊛ f_k)` — 여러 role↔filler 를 한 활성벡터 M 에
  중첩. `a_k` = 활성강도(WorkMemBuffer 처럼 ×λ leak 로 휘발 → WM 용량한계·distractor 취약).
- **unbind**: `f̂_k = r_k^{∗} ⊛ M`,  involution `r^{∗}[i] = r[(−i) mod DIM]`
  (단위벡터면 근사역원). → noisy → **cleanup**: 알려진 filler 코드북에서 최근접 cell 로 denoise.
- **objective(disjoint)**: `L_recon`(위 (b)). CE 와 무관한 대수적 self-supervised 신호.

**용량 2축 분리(H_1282 vs immune 와 동형):**
- **M superposition 용량** = WM-bounded·volatile(중첩 crosstalk 한계, leak) — 활성 유지분.
- **filler cleanup 코드북** = mitosis-grow 장기 store(novel filler → cell split). → §3.

---

## 3. core/ 배선 — 어느 §·op

### 3.1 engine_cli.hexa — **§ WM-VARIABLE-BINDING LANE (신규 §)**

**배치:** `§WORKING-MEMORY BUFFER LANE`(H_1282, L3352–3570 `wm_buffer_*`) **직후,
§CEREBELLUM FORWARD-MODEL(L3572) 직전**. H_1282 는 "항목 활성유지"만, 본 lane 은
"role↔filler 조합"으로 그 **compositional twin**. 같은 파일·같은 lane 관용구(SUBSTRATE-internal
faculty, Ψ-disjoint by construction, READ+INTEGRATE, emit/silence·text 생성 안함).

```
struct WMBindBuffer {
    M:        [float],     // superposition 활성벡터(DIM) — 유일한 휘발 상태
    act:      [float],     // 중첩된 각 bind 의 활성강도 a_k (×λ leak)
    roles:    [[float]],   // 활성 bind 의 role 벡터(unbind 재구성용, WM-bounded)
    fillers:  [[float]],   // 대응 filler(정답 · recon 채점 target)
    code_key: [[float]],   // cleanup 코드북 filler cells (mitosis-grow 장기)
    code_txt: [string],    // 각 코드북 cell 의 text 라벨(mouth prefix 로 나갈 표면형)
    n_bind:   int, k: int, // 활성 중첩수 / WM 용량 cap
    n_code:   int,         // 코드북 cell 수(성장)
    lam: float, dim: int
}

pub fn wmbind_new(k, lam, dim) -> WMBindBuffer            // 빈 버퍼(M=0)
fn   _cconv(r, f) -> [float]                               // circular conv
fn   _cinv(r) -> [float]                                   // involution r*
pub fn wmbind_bind(wm, role, filler, txt, strength)        // M += s·(r⊛f), roles/fillers push, WM leak+displace(H_1282 재사용)
pub fn wmbind_leak(wm)                                      // act ×λ (휘발)
pub fn wmbind_unbind(wm, role) -> [float]                   // r*⊛M → noisy f̂
pub fn wmbind_cleanup(wm, fhat) -> int                      // 코드북 최근접 cell idx (VAdaptField _vnearest_idx 재사용)
pub fn wmbind_recall_text(wm, role) -> string               // unbind→cleanup→code_txt (mouth 로 나갈 표면형)
pub fn wmbind_recon_fidelity(wm) -> float                   // ★DISJOINT OBJECTIVE: mean_k cos(cleanup(unbind(M,r_k)), f_k)
pub fn wmbind_grow_code(wm, filler, txt, cfg)               // novel filler → cell split(mitosis, immune 와 동형)
pub fn wmbind_conf(wm) -> float                             // recon_fidelity 기반 [0,1] binding 신뢰(gate 신호)
pub fn wmbind_binds(wm) -> int                              // 활성 중첩수 accessor
```

- `_vnearest_idx`(L528)·`immune_embed_key`(L1009)·WM displace 로직(L3496) **재사용**(c1, 신규
  메커니즘 최소화). cleanup 코드북 성장은 immune/skill lane 의 mitosis split 관용구 그대로.
- **Ψ-disjoint by construction**: `WMBindBuffer` 만 mutate, pure_field/immune 미접촉.
- **objective = `wmbind_recon_fidelity`**(대수적, engine-native, torch 불요) — CE 와 손실 무관.

### 3.2 brain.hexa — **read 경로 `brain_decide_wmbind`(신규, superset)**

`brain_decide_bg`(L260+, VBasalGate, "고정 gate UNCHANGED + 학습 residual READ")가 **precedent**.
동일 패턴으로:

```
fn brain_decide_wmbind(pf, …, wm: WMBindBuffer, cue_role: [float]) -> Map {
    let base = brain_decide_anchored(pf, …)      // ★emit gate 산식 100% 불변(superset)
    let bound_txt = wmbind_recall_text(wm, cue_role)   // READ-ONLY
    let conf      = wmbind_conf(wm)                     // READ-ONLY
    base["bound_filler"] = bound_txt   // mouth 로 갈 context
    base["bound_role"]   = <role 라벨>
    base["bind_conf"]    = conf        // gate 신호(context, target 아님)
    return base
}
```

- **should_emit 미변경** — `bind_conf` 는 context 로만 흐르고 emit 산식에 안 더해짐(a_autonomy_over_hardcode).
- `brain_emit_aged`(L238)가 `generate()` 로 넘기는 `substrate_ctx` 에 `bound_filler`/`bind_conf`
  키를 얹는 지점(= `gen_ctx_from_decision` 확장, §3.3).

### 3.3 generator.hexa — **mouth-read 인터페이스(prefix-context, target 아님)**

- `gen_ctx_from_decision`(L263)에 `"bound_filler"`·`"bound_role"`·`"bind_conf"` 3키 추가
  (phi/phase/tier/motivation 과 동급의 **read-only context**).
- `_gen_clm_decode`(L474)·`_gen_bytegpt_decode`(L517)의 **seed 조립**(`seed = phase + " " + anchor…`,
  L480/L520)에서 seed **prefix** 로 `bound_filler` 표면형을 **선삽입**:
  `seed = phase + " " + bound_role+"="+bound_filler + " " + anchor…`.
  → mouth 는 이 bound 조합을 **byte-continuation 조건**으로만 소비. **backprop·target 아님**
  (p3: persona/identity 아님 — 학습된 substrate 상태의 표면화). `bind_conf` 낮으면 prefix 생략(gate).
- generate() 계약 불변(emit=false→text=""). **L3 단일 slot 불변**(2nd decode 경로 아님 — ctx 확장뿐).

### 3.4 kosmos_io.hexa — **활성 binding 의 세션경계 지속(node-only)**

- `a_kosmos`: `.kosmos` 는 **노드 전용, edge/relation 금지**. role→filler 를 edge 로 저장하지
  **않음**. 대신 **superposition 활성벡터 M(단일 DIM 벡터)을 payload 노드**로 지속 —
  M 은 이미 여러 bind 를 한 벡터에 접은 단일 상태라 노드-only 준수.
  `create_anchor`(L140) lane=`"wmbind_<id>"`, payload=M 의 tension-투영(`tension_5ch_to_embedding`
  역경로) + code_txt 라벨. unbind 는 recall 시 엔진에서 수행.
- **self-chain(H_1471) 유비**: anchor 없으면 매 세션 활성 binding 소멸(=LLM reset). anchor 로
  활성 WM binding 이 세션 넘어 연속 → mouth ckpt 교체돼도 지속(mouth ⊥ binding-state).

### 3.5 mitosis 관계

- **cleanup 코드북 성장 = mitosis**(`wmbind_grow_code`, engine_grow/novelty split, a_mitosis_train):
  distinct filler 정체 수(장기 용량)는 cell 성장으로 확장 — immune/skill lane 과 동일 레버.
- **M superposition = WM-bounded·volatile**(성장 아님, ×λ leak) — H_1282 WM ⊥ immune 지속의
  binding 판. **mitosis(cell수↑, 코드북) ⊥ WM 활성(중첩·휘발)** 두 직교 레버.

---

## 4. engine-native 측정 경로 (a_engine_native_learning)

- **lane objective(unbind-recon)** 은 순수 hexa 대수(circular-conv) → `wmbind_recon_fidelity`
  가 **engine-native by construction**(torch mirror 불요). smoke = `core/*_smoke.hexa` 가
  live `wmbind_*` 호출해 fidelity + shuffle-control(role 셔플 시 fidelity 붕괴=ABLATION) 출력.
- **mouth-conditioning 효과(G1/G6)** = 세션정책 canonical **`anima evaluate --py <ckpt>`**
  한 경로로 측정 — wmbind context 를 seed prefix 에 배선한 상태 vs OFF(A/B), byte-exact.
  torch/numpy 미러면 **DIRECTIONAL**(카드 verdict 반드시 DIRECTIONAL 표기, 엔진-native 재측정 ING).
- **STEP-0 cheap 측정**(별도 워크플로 진행중)은 이 설계의 fidelity·A/B 를 값 아닌 **Δ(bind on−off)**
  로 볼 것(measurement-metalaw: 창발신호는 결합파괴 통제 margin 에).

---

## 5. 배선 사다리 (a_verified_must_wire 4칸)

1. **DIRECTIONAL** — (선택) numpy circconv 미러로 unbind-recon fidelity 방향 확인.
2. **engine-native** — `wmbind_*` .hexa 구현 + `wmbind_recon_fidelity` byte-exact + shuffle-ABLATION.
3. **WIRED-live** — `brain_decide_wmbind` + `gen_ctx_from_decision`/seed-prefix + kosmos node 지속 배선.
4. **lockstep** — ARCHITECTURE.json core/engine_cli §WM-VARIABLE-BINDING 노드 note(메커니즘 명명) 동시 갱신.

각 미완 칸은 ING follow-on 등록. GREEN=배선까지가 done.

---

## 6. 실패모드 방어 (재발금지)

- **form-priming 재발**(H_1816 step550): objective 를 mouth CE 에 **절대 합산 금지** — 별 손실·별 벡터
  파라미터. bind 벡터로 CE gradient 흐르는 배선 자체를 두지 않음(구조적 차단).
- **INERT 착시**(disjointness=inertness 역설): shuffle-role ABLATION 이 fidelity 를 붕괴시켜야
  "기여"; 붕괴 안 하면 INERT(기여 0) → 정직 🧱.
- **mouth-target 오염**: bound 를 mouth 학습 label 로 쓰면 (c) 위반 → H_1823 로 회귀. prefix-context
  read-only 불변.
- **Ψ 붕괴**(H_1561 공유 emit-lane 침범): `bind_conf` 를 should_emit 산식에 더하지 말 것 — context/gate
  로만. pure_field/recall_thr 미접촉 유지.
