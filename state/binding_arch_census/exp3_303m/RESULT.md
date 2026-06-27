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

## 4. engine-native (terminal) 상태 — UNBLOCKED ✅ (CLMB bind-codec)

> 2026-06-28 update: §4 의 BLOCKED-by-construction 은 **해소됨**. CLMB bind-readout
> 코덱(RTYPE=1 Hadamard u⊙v · RTYPE=2 linear u+v)이 `clm_serialize_v2.serialize_v3_bind`
> ⇄ `core/clm_decode.{py,hexa}` 에 배선되어 bind/bind_linear `.pt` → `.clm` export 가
> 가능하고, **live core/clm_decode.hexa 가 decode**(`a_engine_native_learning`
> engine-transform-to-fit 충족). 자세한 코덱 verdict = `state/1620_clm_bind_codec/RESULT.md`.

- **bind_seed7.pt → bind_seed7.clm (RTYPE=1, 199.6MB)** export·decode 성공. 한때 의심된
  "코덱 overflow/NaN" 은 **arm64 numpy 의 spurious matmul FPE 경고**(numpy#25530) 오진이었음
  (실 가중치 non-finite=0, decode finite, DESCENT PASS). 코덱은 **결함 없음(SOUND)**.
- **held-out DESCENT gate (verify_clm_v2 descent): bind PASS** — F-CLM-DESCENT=1,
  heldout_model_ce 2.301 < uniform 5.545 < shuffle 7.711, overfit_warning False, coherent argmax.
- **engine-native A/B (terminal, live core/clm_decode.hexa, nwin=4, corpus.txt):** 3 arm 전부 GREEN —
  ctrl(RTYPE0) model_ce 1.852 · bind(RTYPE1) 1.815 · bind_linear(RTYPE2) 1.811 (all < shuffle < uniform),
  coherent argmax, hexa⇄py byte-parity(model_ce 1.815089 일치) = LOCKSTEP 확인.
- **G1/G6 engine-native A/B 는 여전히 BLOCKED(mac)** — 303M G6 multiseed 생성은 mac CPU 무거움
  (heavy decode → pool). single-decode CE/argmax 는 terminal 완료, 풀 G0-G6 multiseed 는 pool GPU follow-on.
  §2-3 의 torch-probe G1/G6 verdict(G1=0 floored, G6 noise)는 코덱 작업으로 바뀌지 않음.

## 5. follow-on (ING)
1. ~~bind-codec engine-transform~~ **DONE** (CLMB codec, 1620). bind/bind_linear `.clm` export+decode 완료.
2. **G0-G6 single-entry on pool GPU** — `cli/anima.hexa -- eval <bind.clm>` 3 arm × 3 seed engine-native
   G1/G6 A/B (terminal 승격). mac 차단(303M decode 무거움), pool GPU 호스트 필요.
3. **scale recheck** — 생성 gate floor 해소(더 큰 corpus/step 으로 G1/G6 가 분해능 가질 때) 후 binding A/B 재측정.

## 6. ckpt
- torch `.pt` × 9 (ctrl/bind/bind_linear × {7,4302,4303}, 각 ~1.5GB) + ctrl `.clm` × 3 (176MB) + `.json` × 9.
- PULL → `~/anima-weights/exp3_303m/ckpt/`. 재현 = `state/binding_arch_census/exp3_303m/trainer.py`(arm/seed 플래그).
