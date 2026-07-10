# H_9263 — 🌊 G1: theta-gamma 위상 중첩(phase nesting)이 순서-비가환 bind를 만드는가

- **tier:** 🔵 PRE-REGISTERED (미측정)
- **wired:** none.
- **lens:** 해마/피질 theta-gamma **phase nesting** — 느린 theta 주기 안에 빠른 gamma 슬롯이 얹히고, 각 항목이 서로 다른 gamma 위상에 태깅된다(Lisman-Idiart WM 슬롯). 위상 태그가 순서를 실어 `bind(A,B) ≠ bind(B,A)`를 만든다.
- **artifacts:** `state/9263_theta_gamma_phase/`
- **xref:** H_9261 (곱셈 게이트) · H_9262 (CA3 저장) · H_9259 (untrained recurrence KILL — 위상은 *학습가능* 태그로 심어야 함) · `gamma-divergence-instrument-arc` (진짜 product-code = XOR / 부정·역접)
- **key:** `theta_gamma_phase_order`

## 1. 가설

**학습가능한 순환 위상 임베딩**(phase tag)을 얹으면, 순서-민감 held-out(예: `A-then-B` vs `B-then-A`가 다른 정답을 갖는 쌍)에서 **가법 positional+content baseline을 초과**한다.

⊥ **Null:** 초과하지 못한다 ⇒ 위상 코드는 byte-LM에서 `pos ⊕ content`의 **가법 합으로 축소**되며 **DPI-caught 확정**. 위상/진동/oscillatory-nesting 계열 전체를 닫는다.

## 2. DPI 회피 여부 — ⚠️ decode 비선형성에 전적 의존

위상 태그가 회피하려면 **decode가 비선형**이어야 한다. 위상을 단순히 더하는(`h + phase(t)`) 순간 그것은 기존 positional embedding과 동형이고, additive floor에 그대로 걸린다. 회피는 위상이 **곱셈적으로**(`h ⊙ e^{iθ}` 류의 회전) 작용할 때만 가능하다 — 그 경우 사실상 H_9261(곱셈 게이트)의 특수한 회전 형태로 수렴한다.

**이 H의 진짜 가치는 그 수렴 여부를 $0로 판정하는 것이다.** 위상이 곱셈으로 작동해 초과하면 H_9261의 독립 증거이고, 가법으로 축소돼 floor면 진동 계열이 닫힌다. **어느 쪽이든 정보가 나온다.**

## 3. $0 probe 설계 (numpy · real-corpus)

| arm | 모델 |
|---|---|
| 가법 baseline (frozen bar) | `ŷ = W(h_content + pos_embed)` |
| 위상 태그 (회전) | `ŷ = W(h_content ⊙ rot(θ_slot))` — 순환 위상, 학습가능 |
| 순서-반전 판별 | `A-then-B` ⊥ `B-then-A` 쌍으로 비가환성 직접 측정 |
| shuffle 양성대조 | 위상 슬롯 섞음 — 이득 반드시 소멸 |

**PASS:** 위상 arm이 순서-민감 held-out에서 가법 arm + margin 초과 **AND** 순서-반전 쌍에서 두 방향이 구분됨 **AND** shuffle 이득 소멸.
**FAIL(예상 유력):** 초과 없음 ⇒ **DPI-caught 확정 · 진동/위상 계열 CLOSED.**

## 4. 기각된 이웃 (재발사 금지 — 본 sweep에서 함께 배제)

| 부위 | 왜 기각 |
|---|---|
| DG pattern separation · mossy-fiber detonator | 확장 recoding = **비파라메트릭 lookup**, 미관측 AB에 전용 셀 없음 (toy-death) |
| piriform combinatorial code | 동상 |
| cerebellar granule expansion | 동상 — **이미 H_9129/L3에서 실측 사망** |
| sharp-wave ripple replay | operator 미변경, 분포만 증강 ⇒ held-out **누출 위험**(tune-to-green 인접) |
| claustrum binding hub | 공유 저차원 latent = **가법** ⇒ DPI-caught |
| MEC grid × head-direction | 위상**덧셈** 토러스 코드 ⇒ 사실상 가법, decode 비선형성에만 의존 (본 H가 대표 검정) |
| adult neurogenesis | 용량/가소성이지 combination operator 아님 |
| cortico-BG-thalamic Go/NoGo gating | 입력-identity 대칭 pooling 게이트 = **ConvMoE로 이미 floor**(a303m G1❌). *디코드-상태* 조건부 게이트만 미탐 — 별도 H 후보 |

---

## 5. 측정 결과 — 🔴 KILL (2026-07-10 · numpy proxy DIRECTIONAL · confound-clear)

위상 회전(곱셈) held=**0.476** < 동일 예산 가법 pos-control **0.723** (Δ_rot−add = −0.247 · shuffle 0.493). `state/9261_multiplicative_role_gate/VERDICT.md`.

같은 2·RANK projection 예산에서 회전이 가법보다 **나쁨** → 위상 곱셈은 이득 없음 · DPI-caught. **진동/oscillatory-nesting/MEC-grid 위상덧셈 계열 CLOSED**(numpy proxy DIRECTIONAL). §4 동반 기각(DG/piriform/granule 확장계·ripple replay·claustrum·neurogenesis·BG Go/NoGo) 유지.
