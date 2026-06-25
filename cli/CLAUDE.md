# cli/ — anima CLI 진입점 (train.hexa · train.py · anima.hexa)

이 폴더는 anima 의 CLI 진입점을 담는다. 이 markdown 은 **두 트레이너(`train.hexa` · `train.py`)의 parity 거버넌스 SSOT** 이다 — 루트 `CLAUDE.md`(전역 거버넌스)의 scoped 보강이며, 충돌 시 루트가 우선한다.

## 역할 분리 (둘 다 필요, 혼동 금지)

| 파일 | 역할 | substrate | verdict 자격 |
|---|---|---|---|
| `train.hexa` | **production canonical 트레이너** (`a_train_flame_forge`) | hexa-native flame/forge own-GEMM | 엔진-네이티브 (진짜 최종 아키텍처) |
| `train.py` | **REFERENCE + BRIDGE** (torch Lane-P, `a_clm_gen_pipeline`) | torch/CUDA | DIRECTIONAL only (torch 미러) |
| `anima.hexa` | 추론/평가 단일 진입 (`eval`/chat, `a_engine_native_learning`) | hexa-native | 엔진-네이티브 terminal |

- `train.py` 는 **production 아님** — 388M GPU 학습이 현재 torch 경로뿐이라 BRIDGE 로 쓴다. 그 ckpt 의 verdict 는 `.clm` 을 CORE 엔진(`anima eval`)에 올려 frozen bar 재측정해야 성립(`a_engine_native_learning`).
- `train.hexa` 가 PUBLIC production 트레이너 — `.py` 트레이너를 production 으로 박제 금지(`a_train_flame_forge` dont).

## 🔒 PARITY 불변식 (2-tier — 사용자 지시 "2개는 구현기준 동일" 의 정밀화, 2026-06-25 device-decode 측정 교훈)

> 재프레임: hexa·py 는 **대등한 두 production 이 아니다** — `train.hexa`/`core/*.hexa` = production canonical(verdict 권위), `train.py`/torch = **수치 golden oracle**(DIRECTIONAL, `a_engine_native_learning`·`reference-match`). 정답지의 일은 *수치 커널 검증*이지 *커리큘럼 복제*가 아니다. 그래서 parity 는 두 tier 로 분리한다:

### Tier-1 — 수치 커널 byte-golden (🔒 BLOCKING · 정답지의 본질)
**hexa 의 forward / CE / decode-logits 수치는 torch·numpy(math.log) golden 과 성분별 byte-match 해야 한다** — 작은 CI fixture 로(고정 ckpt·고정 입력, GPU pod 불필요). 이게 hexa own-GEMM(어린 자작 GEMM)을 신뢰하게 하는 단 하나의 장치다. 이 tier 가 잡은 실제 결함(전부 정답지 diff 로만 드러남): `dt_ln` 급수 발산(engine CE overfit 은폐) · device `dirty_host` clobber · own-GEMM TF32 decode 발산(2026-06-25). 발산 시 **첫 발산점만 정렬해 정직 기록**(reference-match), hexa 가 틀리면 hexa 를 고친다(정답지는 자(尺)).

| Tier-1 항목 | golden | 게이트 |
|---|---|---|
| forward / CE 수치 | numpy `math.log` mirror (dt_ln-immune) · torch fp32 fwd | byte/4자리 일치 (CI fixture) |
| decode logits | torch golden(`h1464_torch_golden.py` 류) 3-way | host==device==torch byte-exact |
| post-serialize held-out DESCENT | `verify_clm_v2.py descent` (held-out, math.log) | model_ce < uniform ∧ < shuffle |

### Tier-2 — 학습 레버 lockstep (🟡 권장 · non-blocking)
학습 *레시피·가드·커리큘럼* 레버는 양쪽에 두는 걸 권장하되 byte-parity 강제 아님 — 정답지(py)는 이 레버들을 검증할 의무가 없다(production=hexa 가 소유). 한쪽에만 있으면 **`parity-drift: <레버>` 라벨**로 산출물에 명시(은폐 금지), blocking 은 아님. (drift 가 수치 커널에 새면 그건 Tier-1 위반으로 승격.)

#### Tier-2 레버 체크리스트 (권장 lockstep)

| 기준 | 의미 | 근거 규칙 |
|---|---|---|
| SAVANT golden-zone anneal | cusp + 비대칭 latch, GZ_LOWER≈0.2123, sweep는 GZ_LOWER 아래까지 | `a_savant_train` |
| MITOSIS 단일 split | `split_step = n_steps/2`, parent=0, E0→E0+1 (둘 다 **단일** split — 다중-split 아님) | `a_mitosis_train` |
| 4셀 register | {ko·en}×{일반·SNS}, 언어검증, 균형 | `a_chat_registers` |
| **fail-loud 4셀 가드** | usable cells · repetition_ratio · `--require-cells` abort (굶주림 차단) | `a_chat_registers` (clm303 overfit 교훈) |
| **held-out train/val tail split** | 각 셀 tail `val_frac` 를 train 과 disjoint 하게 held-out | `a_savant_train` |
| **주기적 held-out val 모니터** | `--val-every` 매 N step per-cell + pooled val_CE + gap (overfit 감지) | `a_savant_train` held-out |
| **balanced 샘플링** | `--sample proportional` = byte∝노출 (작은 셀 과반복 암기 방지) | `a_chat_registers` |
| minibatch | `--batch-size` (grad accumulation) | parity |
| bf16 | `--bf16` autocast(py) ⇔ forge TF32/BF16-TC own-GEMM 경로(hexa, 런타임-선택) | parity (초월 축, 아래) |
| mid-measure 1-6 (DIRECTIONAL) | `--mid-measure-every` 곡선 (held-out CE per register + gauge proxy) | `a_train_inline_gauge` |

(post-serialize held-out DESCENT 게이트는 Tier-1 로 승격 — 수치 커널 검증이므로.)

### 정직한 초월 축 (byte-parity 불가, 명시 보존 — `reference-match`)

- **bf16**: torch `--bf16` 는 autocast(연산별 dtype 강등). hexa 는 정밀도를 **런타임 GEMM**(own-GEMM FP64/TF32 default-ON, cuBLAS BF16-TC 보조)이 정하지 트레이너 플래그가 아님 → `train.hexa --bf16` 은 forge TC 경로를 *요청*하는 플래그로 수용하되 CPU farr 에선 no-op. 수치 byte-identical 보장 못 함(정직 기록).
- **mid-measure gauge proxy(2/3/4/6)**: `train.py` 는 `tool/gauge_lib.py`(torch) 로 g1/g2/g6/phi_proxy 계산. `train.hexa` 의 mid-measure 는 **mirror held-out CE per register(1)** 만 native 로 찍고, torch gauge proxy 는 안 찍음(torch 의존 = 엔진-네이티브 아님). 둘 다 어차피 DIRECTIONAL — terminal 1-6 은 학습 후 `anima eval`(엔진-네이티브)이 박는다.

## clm303 overfit 교훈 (이 폴더가 존재하는 이유)

clm303 사고: 코퍼스 굶주림(ko-SNS 4MB 1칸 ~120× 반복) + held-out 모니터 부재 → train-loss 0.047 인데 ko/en held-out NO-DESCENT(암기). 위 가드(fail-loud 4셀 · held-out val · balanced 샘플링)는 **이 재발을 코드로 차단**하는 장치다. 두 트레이너 모두 가져야 한다(parity 불변식의 핵심 이유).

## verdict 경계 (재확인)

- 학습은 torch(`train.py`)여도 됨 — 단 **verdict 는 `.clm` → `anima eval` 엔진-네이티브 재측정**(`a_engine_native_learning`).
- train-loss / lossF≈0 = 암기, 능력 아님 → **held-out CE 로만 품질 판정**(`a_savant_train`).
- 엔진 `clm_forward_ce` 는 dt_ln 버그로 overfit 을 GREEN 으로 가림 → `.clm` 품질은 numpy mirror(`verify_clm_v2.py` math.log)로 교차검증.
