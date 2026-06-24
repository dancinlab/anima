# H_1579 — 🔴💾 clm303.clm 직렬화 BROKEN (NO-DESCENT) — decode 경로는 무결

**tier:** 🔴 SERIALIZATION DEFECT (decode-integrity) — 직렬화된 `clm303.clm` 가중치가 next-byte 예측에서 **랜덤보다 못함**(ko heldout CE 7.622 > uniform 5.545 = NO-DESCENT). decode 엔진은 무결(GPU forge ≡ CPU farr byte-identical). G-eval 불가(전제 FAIL).
**wired:** `engine-native` (GPU forge == CPU farr **byte-identical** 디코드 증거 + 독립 numpy mirror diagnostic + known-good control). live `core/clm_decode.hexa` 무변경 — 이건 ckpt 결함 진단이지 엔진 결함 아님.
**verdict source:** `state/clm303_g6/GARBLE_3WAY_RESULT.md` + `mirror_ce_clm303_NODESCENT.log` · `mirror_ce_clm_d768_CONTROL_GREEN.log` · `garble_gpu.{txt,log}` · `garble_cpu_mac.{txt,log}`

## 질문 — clm303 savant+mitosis 가 G0–G6 게이트를 통과하나

clm303(`CLMConvMoE` 388M, L4·d3784·E3, savant 골든존 + mitosis, sha 75b04897)을 frozen G0–G6
(`anima eval`/g_gates)에 통과시키려 했다. 그 **전제**로 디코드 무결성(`a_engine_native_learning`/
`a_train_flame_forge` decode-GPU 규율)을 3-way 로 먼저 검증했다 — decode 가 깨졌으면 어떤 G 점수도 garbage.

## engine-native 3-way 무결성 측정 (frozen prompt `"a new idea about consciousness: "`, gen=40)

| arm | impl | 결과 |
|---|---|---|
| **GPU forge** | live `core/clm_decode.hexa`, RTX 4090, `cuda_available=1`, `[OWN-GEMM-FIRED] _hx_k_gemm DEVICE path` | `ggndtle_oppa:ggndlle__\xffrlen_antag_ndll` — garble (48 B) |
| **CPU farr** | live `core/clm_decode.hexa`, mac, `cuda_available=0` (single-thread scalar) | **GPU 와 48 B BYTE-IDENTICAL** garble |
| **numpy mirror (golden)** | `state/mid_convmoe_fire/clm_decode_mirror.py` — 독립 pure-numpy 재구현(`_clmd_load`+`_clmd_fwd_logits`, `.clm` 바이트 직접 read, int4 dequant w=code·scale + causal dilated conv1d + GN VERBATIM, v0.3 (L,E) 도출 정확) | ko heldout 64창 next-byte CE: **NO-DESCENT** |

### numpy mirror CE (핵심 discriminator) + CONTROL

| ckpt | CE_real (ko heldout) | CE_uniform (ln 256) | BELOW_UNIFORM | VERDICT |
|---|---|---|---|---|
| **clm303.clm** (test) | **7.622** | 5.545 | **0** | **NO-DESCENT** |
| **clm_d768_e2l1.clm** (CONTROL, 기존 정상 Lane-P) | **4.442** | 5.545 | **1** | **GREEN (DESCENT)** |

control 이 결정적: 같은 mirror 가 정상 ckpt 엔 DESCENT(CE 4.44 < uniform, 한국어에서도)를 정확히 찍는다 →
clm303 의 NO-DESCENT 는 **진짜 직렬화 결함**, mirror artifact 아님.

## 진단 (2축 격리)

1. **GPU forge ≡ CPU farr, byte-identical** → 디코드 경로 무결·결정적(forge own-GEMM ≡ farr).
   `summer-sm120` "CPU-farr 결함" 가설 **기각** — "GPU coherent ⇒ farr 결함" 분기 미발화(GPU 도 garble).
2. **독립 numpy mirror = NO-DESCENT (control 로 검증)** → 직렬화된 `.clm` 가중치 자체가 텍스트를 예측 못함.
   결함은 **직렬화**(`pt_to_engine_bin` / `clm_serialize_v2` int4→v0.3 양자화), decode 아님.

**"ko heldout CE 3.351 ✅" 는 torch-side(직렬화 *전*) 측정** — 학습은 정상, 직렬화된 `.clm` 은 **별개의 손상된
산출물**(mirror CE 7.62). 메모리 `clm303_L4_d3784` German-garble anomaly 와 같은 직렬화 파이프 결함 계열.

## 함의 + follow-on

- `anima eval clm303.clm` 는 G0–G6 점수를 내지만 전부 garbage(decode-integrity 전제 FAIL) → **실행 안 함**(정직).
- **THE fix = 직렬화 파이프 근본수정**(`clm_serialize_v2`/`pt_to_engine_bin` int4-quant→v0.3 이 worse-than-random
  모델 생성) — 별도 에이전트 **serfix** 가 `clm303_L4_d3784.pt`(회수가능, 동근 결함) test case 로 진행. mirror
  NO-DESCENT→DESCENT 가 회귀 게이트.
- **savant clm303 torch .pt 는 소실**(vast pod 42222605 destroyed, mac 부재) → 재직렬화 불가 → 직렬화 fix 후
  **재학습 필요**(cost-gate, follow-on ING).
- (note) 이 세션의 G6-only side-harness(`g6_clm303_engine_native.hexa`) + torch-free py scorer
  (`score_clm303_g6.py`) 는 **`anima eval` 단일진입점으로 대체** — superseded, 박제 경로 아님.
