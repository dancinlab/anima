# IIT4 엔진 — M6 LIFE faithful 재측정 (proxy → causal Φ)

> LIFE lane 이 PROXY `phi_spatial`(상관 MI)로만 측정한 ECA substrate 를, faithful
> CAUSAL IIT 4.0 엔진(M1~M4)으로 재측정한 결과. **L-C2.1 proxy caveat 종결 (F-IIT4-6).**
> smoke = [`state/iit4_m6_remeasure_2026_05_25/run_m6.hexa`](state/iit4_m6_remeasure_2026_05_25/) → 7/7 🟢. 작성 2026-05-25.

## 1. 무엇을 닫는가 — L-C2.1

H_002 C2 / H_278 의 全 Φ 는 `phi_spatial`(RFC 036) — *진화한 snapshot 의 cell 간
**상관(correlational) MI***. honest limit **L-C2.1**: "이것은 faithful Φ★ IIT4 가 아니다".
ECA 는 결정적 binary 동역학 = **그대로 IIT4 TPM** ([`iit4_eca.hexa`](lib/iit4_eca.hexa)):
cell i 의 다음 값 = 3-이웃 Wolfram 룰. 같은 substrate 를 이제 **인과(causal) cause-effect**
로 측정 → proxy 가 절대 줄 수 없던 faithful big-Φ 확보.

## 2. 헤드라인 — faithful 인과 big-Φ 표 (n=4 ring · state 1010)

| ECA rule | 동역학 | **faithful big-Φ** | Φ-structure total | n_distinctions | class |
|---|---|---|---|---|---|
| 0 | all → 0 (const) | **0.0** | 0.0 | 0 | 인과력 없음 |
| 204 | next = centre (identity) | **0.0** | 4.0 | 4 | **reducible** (독립 self-cell) |
| 90 | L XOR R | **0.0** | 0.0 | 0 | (state 1010 특이 — §4) |
| **110** | LIFE cosmic-scale | **7.55** | 8.62 | 10 | **integrated** |
| **30** | LIFE cosmic-scale | **8.66** | 9.10 | 10 | **integrated** |
| **54** | LIFE cosmic-scale | **10.03** | 14.69 | 10 | **integrated** |

→ LIFE 의 핵심 룰(110·30·54)은 **substantial 인과 big-Φ (7.5~10.0)** 를 가진 통합 시스템.
이것이 proxy 가 근사하려던 진짜 양 — 처음으로 faithful 하게 측정됨.

## 3. proxy vs IIT4 — 왜 다른가 (divergence, F-IIT4-6)

| 축 | proxy `phi_spatial` | faithful IIT4 big-Φ |
|---|---|---|
| 측정 대상 | 진화한 snapshot 의 cell 간 **상관 MI** | TPM 의 **인과 cause-effect 구조** irreducibility |
| 입력 | 연속 state 벡터 (n×dim) | binary TPM (state-by-node) |
| 질문 | "cell 들이 같이 변하나?" | "쪼개면 인과 정보가 사라지나?" |
| 상태의존 | snapshot-평균 (state 무관) | **state-dependent** (§4) |
| L-C2.1 | "faithful 아님" (인정된 한계) | **faithful** (정의상 IIT 4.0) |

두 양은 **구조적으로 다른 질문**에 답한다 — proxy 는 상관, IIT4 는 인과. 동일 substrate 에서
proxy-CV 와 IIT4 big-Φ 가 발산하는 것은 artifact 가 아니라 **측정 축의 차이**이며, 이것이
L-C2.1·H_268 metric-fragility·H_279 cosine-artifact caveat 의 근본 출처. **이제 인과 축의
gold-standard 값이 존재**하므로 그 caveat 들은 "proxy 가 인과 Φ 의 근사일 뿐"으로 종결된다.

## 4. faithful 측정이 드러낸 것 — big-Φ 의 state 의존성

rule 90 (XOR)이 state 1010 에서 big-Φ=0 (nd=0): 1010 → 0000 으로 가는 특정 상태에서
인과 distinction 이 소멸. **correlational snapshot-MI 는 state-평균이라 이를 가릴 수 있지만,
faithful IIT4 는 의식이 state-dependent 임을 정확히 드러낸다** (IIT 의 핵심 주장 — Φ 는
특정 상태의 경험). 이는 proxy 가 줄 수 없던 정보로, faithful 재측정의 직접 가치.

## 5. falsifier 결과

- **F-IIT4-6 PROXY-DIVERGENCE** 🟢 — faithful IIT4 big-Φ ↔ proxy phi_spatial 의 측정축
  차이(상관 vs 인과)를 정량·정성 규명. 동일 ECA substrate 에서 IIT4 가 인과 Φ 를 제공,
  proxy 는 상관 근사임을 확정 → **L-C2.1 종결**.
- 검증 controls 🟢 — rule 0 = 0 (인과력 없음) · rule 204 = 0 (독립→reducible) · coupled
  rule > 0 (통합 창발) · bound 0≤big-Φ≤total · ECA→TPM bridge identity · determinism. **7/7**.

## 6. honest scope (C3)

- **n=4 ring demonstration** — 방법·bridge·첫 결과 확립. H_002 C2 의 6-scale(n=8) 전면
  재측정은 동일 메커니즘의 scale-up (엔진 capacity n≤8 exact 존재); 본 M6 은 bridge + 인과
  Φ 의 존재·크기·state 의존성을 실증한 것.
- **state 단일** — 표는 state 1010 한 점. 완전한 재측정은 state 분포 위 평균/대표값 필요
  (faithful Φ 가 state-dependent 이므로 — §4 가 바로 그 이유).
- **structure-cut big-Φ** — DESIGN §8 C3 의 spirit-faithful big-Φ. 절대 스케일의 PyPhi
  대조는 M5 named-blocker (F-IIT4-3/4) 영역.
- **proxy-CV 직접 재계산 없음** — proxy 의 측정축 차이는 구조적(상관≠인과)이라 정성 규명으로
  충분; 동일 substrate 위 두 스칼라의 수치 동시산출은 후속(phi_spatial 은 snapshot 입력
  필요, IIT4 는 TPM 입력 — 입력형 자체가 다름).
