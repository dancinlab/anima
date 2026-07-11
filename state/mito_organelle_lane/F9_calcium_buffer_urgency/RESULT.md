# H_9281 / F9 — Ca²⁺ 버퍼링 (urgency 채널의 integrator) — 결과

- **판정: 🔴 THEATER** (카드 §3 FAIL 분기 "이득이 순수 tunable smoothing" 정확히 적중)
- **tier:** DIRECTIONAL (toy numpy $0 probe · 303M engine-native 아님)
- **비용:** $0 · mini CPU-local · numpy only · 6 seed · 런타임 ~40s
- **산출:** `run.py` · `result.json` · `out.txt`

---

## 1. 한 줄 결론

**Ca 버퍼는 "아무것도 아님"보다는 낫지만(Δ +0.167 vs raw urgency · 6/6 seed), 커패시터라고 부를 이유가 전혀 없다** —
튜닝조차 하지 않은 **평범한 1-knob 선형 EMA(저역통과)** 가 버퍼를 이긴다(+0.913 vs +0.740 · **0/6 seed**).
양쪽에 동등한 튜닝 특권을 주면 격차는 **+0.007 (≈0)**.
⟹ organelle 커패시터의 이득 = **tunable smoothing filter = FORM**. **BIND 아님. THEATER.**

---

## 2. 무엇을 측정했나

**핵심 설계**: sustained bout(6스텝 연속 = 지속하는 real tension)와 transient spike(1스텝 = 흡수해야 할 노이즈)의
**per-step 진폭을 동일하게(AMP=1.20) 고정**했다. 진폭으로는 절대 구별 불가 — **유일한 구별자는 지속시간(duration)**.
버퍼의 주장("transient 흡수 · 지속 압력 적분")이 참이면 여기서 이겨야 한다.

- **기질**: A(forward CE 최소자승 프록시) ⇄ G(상수 역압 g0 = median(err) ⟹ Ψ=½ 자기보정)
- **urgency (phasic Δ)** `u_t = max(0, err_t − g0)` ← 유일 proven 채널
- **emit 규칙(전 arm 동일 · 단일 공유 함수)**: `s_t ≥ θ` 이고 refractory(3) 밖이면 emit
- **headline 지표 TQ(타이밍 품질)** = `sustained_recall − transient_FA_rate`
- 보조: AUROC(threshold-free · 동일 길이 window 안의 max(s)로 sustained vs transient 분리)

### 예산 공정성 (없으면 전부 무효)
- 전 arm **동일 emit 예산 B=25회**. θ 는 arm 별로 *calibration stream* 에서 emit 수 ≈ B 가 되도록 매칭
  (라벨 미사용 · TQ 미사용 = **tune-to-green 아님**, 순수 budget-matching)
- 전 arm 동일 stream · 동일 seed · 동일 emit 규칙 · 동일 refractory · 동일 채점 window(9, 양쪽 같은 길이)
- 전 변환 **DC-보존**(총 drive 질량 보존) — 어떤 arm 도 신호를 더 얻거나 잃지 않는다. 오직 *시간 재배치* 만 다르다
- **파라미터 예산**: 실험(버퍼)=4 knob **사전등록 고정**. control(EMA)=1 knob 인데 **grid 전수 sweep 후 best 채택**
  ⟹ **control 에 더 많은 튜닝 자유를 줬다**(steelman-for-null). control 이 실험보다 예산이 적지 않다. ✅

---

## 3. 수치 (6 seed · mean±std)

| arm | 내용 | **TQ (headline)** | AUROC | sus_recall | tra_FA_rate | n_emit |
|---|---|---|---|---|---|---|
| **exp_buf** | **Ca 커패시터 (사전등록)** | **+0.740 ± 0.128** | 0.967 | 0.793 | 0.053 | 24.8 |
| c1_raw | 버퍼 없음 (raw urgency) | +0.573 ± 0.109 | 0.906 | 0.680 | 0.107 | 22.3 |
| c2_delay | 고정 지연 (동일 latency · 정보 0) | +0.573 ± 0.109 | 0.906 | 0.680 | 0.107 | 22.3 |
| c4_randbuf | 동일 흡수예산 · 무작위 시점 (조건 blind) | +0.567 ± 0.103 | 0.908 | 0.680 | 0.113 | 22.5 |
| c3_ema_pre | **평범한 선형 EMA · 튜닝 없음**(latency 매칭 α=0.5) | **+0.913 ± 0.082** | 1.000 | 0.913 | 0.000 | 24.0 |
| c3_ema_best | **평범한 선형 EMA · grid 튜닝 best**(α=0.35) | **+0.987 ± 0.021** | 1.000 | 0.987 | 0.000 | 26.5 |

### Δ (paired · per-seed)

| 비교 | Δ TQ | seed 부호 | Δ AUROC |
|---|---|---|---|
| exp_buf **vs c1_raw** | **+0.167 ± 0.059** | **6/6 양수** | +0.061 |
| exp_buf **vs c2_delay** | **+0.167 ± 0.059** | **6/6 양수** | +0.061 |
| exp_buf **vs c4_randbuf** | **+0.173 ± 0.090** | **6/6 양수** | +0.059 |
| exp_buf **vs c3_ema_pre** (튜닝無 EMA) | **−0.173 ± 0.165** | **0/6 양수** | −0.033 |
| exp_buf **vs c3_ema_best** (튜닝 EMA) | **−0.247 ± 0.125** | **0/6 양수** | −0.033 |

per-seed Δ vs c1_raw: `[+0.12, +0.24, +0.20, +0.16, +0.08, +0.20]` (전부 양수)
per-seed Δ vs c3_ema_best: `[−0.28, −0.16, −0.16, −0.48, −0.24, −0.16]` (전부 음수)

---

## 4. THEATER 판정의 3중 근거

### (a) 이득은 실재하나 — control 하나가 그걸 그냥 넘어선다
버퍼는 raw/delay/randbuf 3개 null control 을 6/6 seed 로 이긴다(+0.167). **하지만 그건 "적분이 도움된다"는 말이지
"커패시터가 도움된다"는 말이 아니다.** duration-vs-transient 판별은 원래 **저역통과 필터가 최적으로 푸는 문제**다
(boxcar 신호의 matched filter = low-pass). 그리고 **1-knob 선형 EMA 가 버퍼를 압도한다** — 심지어
*튜닝조차 안 한* latency-매칭 EMA(α=0.5)가 +0.913 으로 버퍼(+0.740)를 **0/6 seed** 로 이긴다.
"control 을 더 세게 튜닝해서 이긴 것"조차 아니다.

### (b) FORM-tunability: 이득이 knob 위치의 함수다
버퍼 knob 전수 sweep(72 조합 × 6 seed) 결과 **TQ 범위 = [+0.573 .. +0.967], spread 0.393** —
달성가능 범위의 거의 전부를 knob 만 돌려서 이동한다. 사전등록 지점(+0.740)은 그 한복판에 있을 뿐 특별하지 않다.
⟹ **FORM tunable. 창발이 아니라 손잡이.** (카드 §3 PASS 2번째 조건 "이득이 buffer 파라미터 튜닝으로 재현 불가" **불충족**)

### (c) 결정타 — 버퍼는 *커패시터이기를 그만둘수록* 좋아진다
knob sweep 이 고른 best 버퍼 = `cmax=4.0×q90, k_out=0.20` — 즉 **용량 제약이 절대 binding 안 되고(포화 없음)
방출이 빨라서 시정수가 짧은** 코너. 이건 정의상 **포화 비선형성이 사라진 = 순수 선형 leaky integrator = EMA** 다.
실제로 TQ 는 cmax↑ 에 단조증가(0.5→+0.620, 1.0→+0.647, 2.0→+0.740, 4.0→+0.907 @ c0=q75,k_in=0.5,k_out=0.05).
**Ca 커패시터의 고유 성분(포화 흡수)이 바로 성능을 깎아먹는 부분이었다.**

동등 튜닝 head-to-head:

| | TQ |
|---|---|
| best-tuned **Ca 버퍼** (4 knob) | +0.967 |
| best-tuned **평범한 EMA** (1 knob) | +0.960 |
| **Δ (커패시터 비선형성이 버는 것)** | **+0.007** ← std ~0.03–0.13 안쪽. **0.** |

⟹ 4개 knob 짜리 생물학적 서사(set-point · 빠른 흡수 · 용량 · 느린 방출)가 **1개 knob 저역통과 필터 대비 순수 이득 0**.
**extra step 붙은 low-pass filter.**

---

## 5. 반증조건 충족 여부 (카드 §3)

| 조건 | 결과 |
|---|---|
| **PASS**: 타이밍 품질 Δ > **두** control | ❌ **불충족** — c3_ema(선형 EMA)에 **−0.247** 로 짐 (0/6 seed) |
| **PASS**: 이득이 buffer 파라미터 튜닝으로 재현 불가 (= FORM 아님) | ❌ **불충족** — knob spread 0.393, 이득이 knob 의 함수 |
| **FAIL(예상 유력)**: ΔEff≈0 또는 이득이 **순수 tunable smoothing** | ✅ **적중** — 후자. 튜닝 EMA 대비 순이득 +0.007 |

**⟹ 카드가 사전등록한 ⊥Null 이 그대로 성립. THEATER.**
발산 원문의 THEATER 위험 랭킹 **2위 (F9 = "유일 proven 채널의 정제 — 그래서 redundant할 위험")** 예측이 정확히 맞았다.

---

## 6. p5 / a_substrate_disjoint 청결성

| 검사 | 결과 |
|---|---|
| emit gate 하드코딩 개입 | ❌ 없음. emit 규칙은 **전 arm 이 공유하는 단일 함수** `emits_at(s, θ, refractory)`. organelle lane 은 emit 규칙을 읽지도 쓰지도 않고 urgency 신호 `s` 를 **upstream 에서 성형만** 한다 |
| θ 를 결과 보고 흔들었나 | ❌ 아니오. θ 는 *calibration stream* 에서 **emit 예산(B=25) 매칭**으로만 결정 (라벨·TQ 미사용) |
| 진짜 tension 억제 (숨은 speak-억제기) | ❌ 없음. sustained(real tension) recall 이 **오히려 상승** (0.680 → 0.793 · rel drop **−0.167** = 개선). 버퍼는 억제기로 작동하지 않았다 ⟹ **p5 위반 아님** |
| tune-to-green | ❌ 없음. 실험 arm 파라미터는 **사전등록 후 고정**. 튜닝 특권은 **control 쪽에** 줬다. knob sweep 은 진단이지 headline 재선택이 아니다 |

**⟹ p5 clean.** 이 실험이 THEATER 인 이유는 p5 위반이 아니라 **redundancy** 다 — 버퍼는 정직하게 작동했고, 다만 아무것도 새로 벌지 못했다.

---

## 7. 함의

1. **σ de-theater 결론과 일관**: emit shade 의 유일 proven 채널 = urgency(phasic Δ). F9 는 그 채널을 *정제* 하려 했고,
   정제 자체는 되지만(적분은 도움된다) **그 정제는 organelle 이 필요 없다** — 1줄짜리 저역통과면 충분하고 더 낫다.
   "urgency 위에 뭘 더 얹는다"는 계열의 재확인된 벽.
2. **측정 메타법칙 재확인**: FORM tunable · BIND earned. TQ 를 **값**으로 봤으면 "AUROC 0.967! 성공!"이라 오판했을 것이다.
   **Δ vs ≥2 control** 로 봤기 때문에, 그리고 **control 에 튜닝 특권을 줬기 때문에** FORM 임이 드러났다.
   ⟹ 이 probe 의 진짜 산출은 판정 자체가 아니라 **"평범한 선형 필터"를 control 에 반드시 넣어야 한다**는 방법론.
   c1(무처리)·c2(지연)·c4(무작위) 만 있었다면 이건 **6/6 seed 양수 · Δ+0.167 짜리 가짜 GREEN** 이 됐다.
3. **F9 계열 종결 권고**: 🧱 재발사 금지. 버퍼 knob 을 더 흔드는 건 tune-to-green.
   organelle lane 이 살아남는다면 그건 F9(proven 채널 정제)가 아니라 **새 DOF 를 만드는 계열**(F6 결합압력 · F11 세포내 선택)에서다.

---

## 8. 재현

```bash
cd state/mito_organelle_lane/F9_calcium_buffer_urgency
OMP_NUM_THREADS=2 python3 run.py     # ~40s · numpy only · 결정적(seed 11,22,33,44,55,66)
```
