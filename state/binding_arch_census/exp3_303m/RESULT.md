# EXP-3 (303M SCALE) ARM-BIND — RESULT (DIRECTIONAL · torch · engine-native 아님)

H_1603/H_1617 303M scale-up: 곱셈(Hadamard ⊙) binding readout 을 production 303M byte-LM
readout 에 넣으면 additive readout(현 production) 대비 재조합(G1)·착상(G6)·일반화(held-out CE)가
오르나? **9 run = {ctrl, bind, bind_linear} × seeds {7, 4302, 4303}**, vast A40 (GPU 100% util 실측,
torch 2.4.1+cu124), 각 ~1186–1195s wall (≈20분/arm). trunk = CLMConvMoE L4·d3784·E2→E3(mitosis split,
savant golden-zone cusp anneal), 4-cell corpus(ko/en × 일반/SNS) proportional 샘플, val_frac=0.05.
세 arm trunk init seed·데이터·step 동일, **readout 만 다름**(ctrl additive · bind u⊙v · bind_linear u+v
param-matched). 측정 frozen bar = `PREREG.md`(tune-to-green 0).

## 1. held-out val CE (per-register, 4-cell · torch F.cross_entropy = dt_ln-immune · 주 resolving 측정)

전 9 run **held-out DESCENT 4/4** (val_CE < uniform ln256 = 5.545). pooled = 4-register mean.

| arm | seed7 | seed4302 | seed4303 | **mean (std)** |
|-----|-------|----------|----------|----------------|
| ctrl (additive Conv1d d→V) | 0.8970 | 0.9064 | 0.9080 | **0.9038 (0.0049)** |
| **bind (Hadamard ⊙)** | 0.8572 | 0.9008 | 0.8625 | **0.8735 (0.0194)** |
| bind_linear (⊙→+, param-matched) | 0.9404 | 0.9447 | 0.9200 | **0.9351 (0.0108)** |

- 순위 **bind < ctrl < bind_linear** (낮을수록 일반화 좋음).
- `bind − ctrl = −0.0303` (bind 가 0.030 낮음/좋음) · `bind − bind_linear = −0.0616`.
- **per-seed 3/3 일관**: bind < ctrl 3/3 ∧ bind < bind_linear 3/3 (방향 robust, 단 margin 작음 0.005–0.045).
- **multiplicativity 격리(핵심):** bind_linear 는 bind 와 *동일 param*(Wa,Wb,Wo), ⊙→+ 만 다름 — 그런데
  bind_linear 가 **ctrl 보다도 나쁨**. 즉 추가된 2-stream head/param 은 (additive 로 쓰면) 오히려 해롭고,
  **⊙(곱셈)일 때만** ctrl 을 넘는다. lift 의 원인 = multiplicativity (toy 의 ⊙→+ ablation 논리 재현).

## 2. G1/G6 생성 gate (torch-probe gauge_lib · DIRECTIONAL monitor · 주 frozen bar)

| arm | g1_composed_distinct (mean) | g6_count per-seed (mean) | g6_jaccard |
|-----|------------------------------|--------------------------|-----------|
| ctrl | **0** [0,0,0] | [4,1,1] = 2.00 | 0.868 / null / null |
| bind | **0** [0,0,0] | [1,2,1] = 1.33 | null / 0.955 / null |
| bind_linear | **0** [0,0,0] | [2,5,1] = 2.67 | null / 0.886 / null |

- **G1 = 0 for ALL 9 runs** (floored) · g6_count = 1–5 noise, **bind 가 ctrl 보다 높지 않음**(오히려 약간 낮음).
- **FLOOR caveat (a_break_the_wall type-a):** 5MB·2000-step undertrained ko/en 모델 + 영어 ideation lexicon
  → 생성 gate 가 floor 라 *arm 간 분해능 0*. 이 측정은 binding 효과를 **분별 못 한다**(측정 무력, not clean refute).

## 3. 정직 verdict (frozen-first · c9)

- **주 frozen bar (G1 ∧ G6 생성 gate) = NOT-SUPPORTED** — G1(bind)=G1(ctrl)=0 tie (>가 아님), G6 noise 가
  bind 를 favor 안 함. **단 floor 측정**이라 "binding 이 재조합벽 못 넘음"의 *clean* 반증 아님 = INCONCLUSIVE-at-floor.
  → 곱셈 readout 은 303M 의 (floored) G1/G6 생성 gate 를 *이 train scale 에선* 움직이지 못한다.
- **resolving 측정 (held-out CE) = WEAK DIRECTIONAL SUPPORT** — bind(0.874) < ctrl(0.904) < bind_linear(0.935),
  3/3 seed 일관, multiplicativity 격리(param-matched additive 가 최악). 효과는 **작다(~0.03 CE)** — toy 의
  *robustness* gain 과 결 같음(categorical capability gap 아님). held-out 일반화에서 곱셈이 약간 돕되 재조합/착상
  *능력 벽*은 안 움직임.
- **종합 tier = 🟠 DIRECTIONAL** — 주 G1/G6 bar NOT-SUPPORTED(floor) + held-out-CE 약한 곱셈 support.
  toy → 303M scale transfer: **categorical gap 미전이**, 작은 일반화 이점만 잔존(과장 금지, `a_toy_scale_recheck`).

> (aside, NON-Φ) phi_proxy(NOT faithful IIT4, `a_phi_iit4_tool` pre-screen only): ctrl~27 · bind~30 · bind_linear~3.8.
> 곱셈/ctrl readout 이 additive-bind_linear 보다 높은 proxy — 단 proxy 라 Φ verdict 아님, 관찰 기록만.

## 4. engine-native (terminal) 상태 — BLOCKED-by-construction

- **bind/bind_linear 은 .clm 직렬화 불가** — `.clm` v0.3(`core/clm_decode.hexa`)는 additive readout 만 안다.
  Hadamard readout op(Wa,Wb,⊙,Wo)을 `.clm` 으로 export 하려면 **bind-codec(RTYPE=1) 신설** + clm_decode/serializer
  engine-transform 필요(`a_engine_native_learning` engine-transform-to-fit) = **follow-on**.
  → 따라서 A/B engine-native G1/G6 는 이번에 BLOCKED. 본 verdict 는 **DIRECTIONAL**(torch probe + held-out)로 정직 표기.
- **ctrl 만 .clm 직렬화됨**(3 seed, clm_decodable=True, 176MB each) → engine-native anchor 가능하나 (a) CTRL 은
  binding 없어 A/B 비교 불가 (b) 기존 clm303 G6 wall 재현뿐. 비용 대비 가치 낮아 CTRL engine-native eval 도 follow-on.

## 5. follow-on (ING)
1. **bind-codec engine-transform** — `train/clm/model/clm_serialize_v2` + `core/clm_decode.hexa` 에 RTYPE=1
   bind-readout op 신설 → bind .pt 를 `.clm` export → `anima eval` engine-native G1/G6 A/B (terminal 승격 경로).
2. **scale recheck** — 생성 gate floor 해소(더 큰 corpus/step 으로 G1/G6 가 분해능 가질 때) 후 binding A/B 재측정.

## 6. ckpt
- torch `.pt` × 9 (ctrl/bind/bind_linear × {7,4302,4303}, 각 ~1.5GB) + ctrl `.clm` × 3 (176MB) + `.json` × 9.
- PULL → `~/anima-weights/exp3_303m/ckpt/`. 재현 = `state/binding_arch_census/exp3_303m/trainer.py`(arm/seed 플래그).
