# H_313 — PLASTICITY × STDP: spike-timing 이 시간적 인과(temporal causality)를 발견하는가?

> matrix cell: PLASTICITY × STDP. 가소성(plasticity)의 정체가 Hebbian STDP(spike-timing-dependent plasticity)라면, integrate-and-fire 쌍에서 pre 가 post 를 *일관되게 선행*하는 CORRELATED 입력은 post 가 pre 를 선행하는 ANTI-correlated 입력보다 *더 강한* 시냅스로 수렴해야 한다 — 즉 STDP 는 시간적 인과를 발견한다. 실제 timestep 루프를 돌려 emergent 가중치를 측정.

## 1. 동기

- 가소성 축(PLASTICITY)의 후보 메커니즘으로 STDP 를 검정한다. STDP 는 Bi & Poo (1998) 의 비대칭 Hebbian 규칙: pre 가 post 직전에 발화하면 시냅스 강화(potentiation), post 가 pre 직전이면 약화(depression).
- 핵심 질문: 이 규칙이 *입력의 시간 구조* 만으로 "어느 쪽이 원인인가"를 구별할 수 있는가? 강화/약화의 비대칭이 외부에서 박힌 것이 아니라 spike timing 으로부터 *창발(emerge)* 하는가?
- 반-tautology 설계: STDP window 의 *형태* 는 두 조건에서 동일(A+ = A−, τ+ = τ−)하게 둔다. 유일한 차이는 spike-train *타이밍*. 만약 적분이 부호-대칭이면 두 조건은 같은 가중치로 수렴 → H1 FALSIFIED. 즉 결과가 falsify 가능.

## 2. 가설

**H1 CAUSALITY-DISCOVERY**: dt = t_post − t_pre 에 대한 지수 STDP window 하에서, CORRELATED 쌍(pre 가 post 를 lag 만큼 선행, dt>0 우세)의 최종 가중치 w_corr 가 ANTI-correlated 쌍(post 가 pre 를 선행, dt<0 우세)의 w_anti 보다 *엄격히 크다*. 또한 총 가중치는 [w_min, w_max] 내에 *유계(bounded)* — runaway 없음.

falsifier: N timestep 후 w_corr ≤ w_anti 이면 FALSIFIED. 가중치가 무계(unbounded)이면 별도 note.

## 3. 측정 방법

자기완결 hexa 결정론 시뮬레이션 (`state/.../run.hexa`):

- **모델**: integrate-and-fire pre→post 쌍, 시냅스 1개 w. nearest-neighbour(last-spike trace) STDP.
- **STDP window**: Δw(dt) = +A₊·exp(−dt/τ₊) (dt>0, 강화) · −A₋·exp(dt/τ₋) (dt<0, 약화). 형태 대칭: A₊=A₋=0.10, τ₊=τ₋=20.0.
- **CORRELATED**: pre 가 t=k·period, post 가 k·period + lag (pre 선행, dt>0 우세).
- **ANTI**: pre 가 t=k·period, post 가 k·period − lag (post 선행, dt<0 우세).
- **CONTROL (pre-only null)**: post 가 전혀 발화 안 함 → STDP 는 쌍(pair) 규칙이므로 w 는 반드시 w0 유지 (루프 drift 무결성 검정).
- params: period=50, lag=5, T=5000 timestep (≈100 spike pair), w0=0.50, clamp [0,1].
- 두 조건의 *전체 timestep 루프* 를 실제 실행하여 emergent 최종 가중치를 측정. 부호를 hardcode 하고 검사하는 것이 아님(금지된 tautology) — 루프를 돌려 측정.

## 4. 사전등록 falsifier

- **F313.1 CAUSALITY**: w_correlated > w_anti
- **F313.2 POTENTIATION**: correlated Δw > 0 (인과 쌍이 시냅스 강화)
- **F313.3 DEPRESSION**: anti Δw < 0 (반-인과 쌍이 시냅스 약화)
- **F313.4 BOUNDED**: 두 가중치 모두 [0,1] 내 — runaway 없음
- **F313.5 CONTROL-NULL**: pre-only(post 無) |Δw| < 0.001 — STDP 는 쌍이 필요, 루프 drift 無

H1 SUPPORTED = F313.1 PASS AND F313.2 PASS AND F313.3 PASS AND F313.4 PASS. F313.1 FAIL 이면 H1 FALSIFIED.

## 5. 비용

- $0 mac-local (`/Users/ghost/.hx/bin/hexa run`) · hexa-only · ~1s wall · 결정론(RNG 無, 고정 schedule).

## 6. 측정 결과

| 조건 | 최종 w | Δw |
|---|---|---|
| CORRELATED (pre 선행) | **1.0** | +0.5 |
| ANTI (post 선행) | **0.0105399** | −0.48946 |
| CONTROL pre-only (post 無) | 0.5 | 0.0 |

- **separation (corr − anti) = 0.98946**
- F313.1–5: **5 PASS / 0 FAIL**
- HEADLINE: **STDP-DISCOVERS-CAUSALITY (H1 SUPPORTED)** — correlated 가 천장(1.0)까지 강화, anti 가 바닥(0.0105) 근처까지 약화, 유계, drift 無.

**비-saturation robustness probe** (clamping artifact 가 아님을 확인, A=0.02·T=300·~4 pair): w_corr=0.569448, w_anti=0.43266, Δw_corr=+0.0694481, Δw_anti=−0.0673402, separation=0.136788. exp(−5/20)·0.02 per-pair 가 측정 Δw 와 정합 → 천장에 닿기 *전에도* corr>anti 순서 성립 = clamping 이 아닌 창발.

## 7. honest limits

1. **L1**: nearest-neighbour(last-spike) trace STDP — all-to-all pairing 아님. 표준이나 모델링 선택.
2. **L2**: 결정론 고정 schedule (jitter/noise 無). 실제 "STDP-discovers-causality" 주장은 Poisson jitter 를 추가 — 여기서는 깨끗한 결정론 코어.
3. **L3**: hard clamp [0,1] 로 유계가 구성적으로 보장됨. *진짜* 발견(runaway dynamics 부재)은 비-saturation probe(A=0.02,T=300, corr=0.569 anti=0.433 내부 유지)로 입증.
4. **L4**: 단일 시냅스 pre→post. multi-synapse 경쟁(weight normalization, BCM)은 미모델.
5. **L5**: exp() 는 hexa 빌트인 — 검정 대상이 아닌 순수 math primitive.
6. **L6**: SPECULATION-FENCED — "STDP = 가소성의 정체" 라는 더 넓은 주장은 이 검정 범위 밖. 검정한 것은 "STDP window 가 시간적 인과를 미분(discriminate)한다"는 좁고 falsify 가능한 명제.

## 8. 폐쇄

F313.1–5 결판 — **5/5 PASS, H1 SUPPORTED (🟢 GREEN / numerical)**. verdict 는 측정 숫자에서 DERIVED (self-declared 아님).

## 9. 산출물

- `state/h313_plasticity_stdp_causality_2026_05_27/{run.hexa, result.json, run.log}`
- run.hexa = 실제 STDP timestep 시뮬레이션 (자기완결, lib 의존 無).
- result.json = 측정 가중치 (corr/anti/control + bounded check) — self-declared verdict 아님, 측정에서 도출.

## 10. 후속

- H_3xx: Poisson-jittered spike train 으로 noise robustness (L2 해소).
- H_3xx: multi-synapse 경쟁 + weight normalization → 수용 영역(receptive field) 창발 (L4).
- pi5-akida 하드웨어 STDP 실측 (optional follow-up; 결정론 sim 으로 지금 충분히 real).
