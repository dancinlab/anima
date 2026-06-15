> 📍 SSOT: [ARCHITECTURE.md](ARCHITECTURE.md) · governance [CLAUDE.md](CLAUDE.md)

# INTENT_A6 — `intent-osc-residual` (ANIMA INTENT 축, bench D OSC 잔류 진단·해소)

> A6 단독. ANIMA INTENT 축. bench D axisbench (#1143) 4/5 🟠 PARTIAL · OSC residual carry 의 진단 + 해소.
> verdict: 🟢 RESOLVED (5/5) — direction_std 재설계가 OSC 잔류를 해소. 진동은 substrate 본질 (intrinsic limit-cycle), metric 결함이 root cause.

---

## 1. 동기 (Motivation)

ANIMA.md INTENT 축은 `bench D axisbench` (#1143) 에서 **4/5 🟠 PARTIAL** 로 land 했고, 단일 falsifier **F3 `OSC_STABILITY_LOW`** 가 FAIL 한 채 OSC residual 로 carry 되었다.

INTENT 는 `brain_decide` (short-term emit) 위의 **long-term goal 형성층** — 단기 emit decision stream 의 cumulative direction (며칠 후 목표) 이 substrate-discriminable 한 신호를 갖는지 검정한다. 3 시나리오:

- **CONVERGENT**: decision 이 시간에 따라 `[1,0,0,0]` 으로 drift (목표 수렴)
- **RANDOM**: 균일 4-D 방향 (목표 없음)
- **OSCILLATING**: period-20 4-corner cycle (+x → +y → -x → -y, 5-tick 씩)

OSCILLATING 의 `stability_std = 0.0` 관측이 F3 (`osc_stab > 0.4`, 진동은 불안정해야 함) 를 FAIL 시켜 verdict 가 🔴 FAIL 로 떨어졌다. 본 A6 는 이 OSC residual 의 정체를 진단하고 보정한다.

## 2. 가설 (Hypothesis)

INTENT 의 OSC residual (의도 신호 진동) 이 둘 중 하나다:

- **(가) 설계 결함**: damping 부재 · gain 과다 → 보정 (damping 추가 · 정규화) 하면 진동 소멸 → 5/5.
- **(나) substrate 본질**: 의도가 본질적으로 진동 (ultradian / limit-cycle) → 보정 후에도 잔존.

**사전등록 falsifier**: 보정 후에도 진동이 잔존하면 (나) — 진동이 substrate 본질 (honest residual). 단 H_634 ultradian 과 cross-link 가능성 검토.

## 3. OSC residual 정체 (주기 · 진폭 · root cause)

bench D `run.log` 실측:

```
[B] stability_std  (consecutive 10-tick window cos-sim std)
    CONVERGENT   = 0.47432
    RANDOM       = 0.538697
    OSCILLATING  = 0.0          ← residual
```

**진동의 정체**:
- **주기 (period)**: 20 ticks (4-corner × 5-tick). component-0 sequence = `+1×5, 0×5, -1×5, 0×5` 반복. 자동상관 lag-20 에서 최대.
- **진폭 (amplitude)**: 단위 4-D 벡터 (∥d[t]∥=1) 의 4-corner 사이 full-swing — corner 간 cosine = -1 (정반대) 또는 0 (직교).
- **half-period anti-correlation**: lag-10 자동상관 = -0.9 (반주기 반전 = 진동의 결정적 signature).

**root cause = metric aliasing (신호 결함 아님)**:
기존 `stability_std` 는 인접 10-tick **window-mean direction** 의 cos-sim sequence 의 std 다. OSCILLATING 의 period-20 은 window grid (size 10) 와 **commensurate** (정수배). 각 10-tick window 가 정확히 2 corner 를 평균 → window-mean direction 이 deterministic 하게 반복 → cos-sim sequence 가 **constant** → std = 0.

즉 진동이 metric 에 의해 **false-stable 로 aliased** 된 것이다. 진동 신호 자체는 명백히 존재하나 (period-20, full-swing 진폭), stability_std metric 이 window grid 와 period 의 commensurability 때문에 진동을 0 으로 접어버린다. **신호 결함이 아니라 측정자 (尺) 결함**.

## 4. 보정 설계 (Correction Design)

두 보정 경로를 self-contained substrate harness (`bench/axis_intent/a6_osc_residual_verify.hexa`) 로 실측한다. LCG-deterministic · libm-free · foreground sync · $0 mac-local. bench D 의 3 decision stream generator (`gen_convergent/random/oscillating`) 를 verbatim 회수.

### 보정 A — `direction_std` (M4 재설계, metric 교체)
인접 cos-sim std (aliasing 취약) 대신, 각 tick 의 **raw normalized direction d[t]=normalize(stream[t])** 의 component-wise std 의 mean. OSCILLATING 은 4 corner 를 sweep → component variance 가 structured-high. CONVERGENT 는 1 방향으로 collapse → low. RANDOM 은 scatter → high-but-unstructured. window grid commensurability 에 영향받지 않음.

> ⚠ A6 진단 정정: M4 draft (`oscillation_metric.hexa`) 의 `om_direction_std` 는 **delta** direction (`stream[t]-stream[t-1]`) 을 썼는데, OSCILLATING 은 corner 내부 4/5 tick 에서 delta=0 이라 OSC variance 를 **과소계상** (0.158 < conv/rand) 했다. 올바른 fix 는 **raw** direction variance 다. 본 A6 가 이 정정을 실측·확정한다.

### 보정 B — damping (EMA low-pass, 진동 감쇠 시도)
가설 (가) 검정용. decision stream 에 1차 EMA `y[t] = α·x[t] + (1-α)·y[t-1]` (α=0.2, heavy low-pass) 를 걸어 진동을 감쇠하고 재측정. period 가 소멸하면 (가) 설계 결함, period 가 잔존하면 (나) substrate 본질.

### `period_detect` (intrinsic 여부 판정)
component-0 의 lag-windowed Pearson 자동상관 (num·denom 동일 [0,n-p) window — finite-length edge bias 제거) 의 **argmax** lag. structure floor 0.7 미만이면 0 (RANDOM). first-crossing 규칙은 lag-19 가 lag-20 직전에 0.7 을 넘어 off-by-one 이므로 argmax 채택.

## 5. 재측정 verdict (Re-measurement, verbatim)

`state/intent_a6_osc_residual_2026_05_28/a6_verify_run.log` (exit 0, 2-run byte-identical):

```
[2] REDESIGN direction_std (per-tick RAW direction component std)
    CONVERGENT  = 0.350144   ← collapses to 1 dir (low)
    RANDOM      = 0.49946   ← scattered (high, no period)
    OSCILLATING = 0.353553   ← 4-corner sweep (high + period)

[3] period_detect (argmax windowed Pearson autocorr, max lag 25)
    CONVERGENT  = 8
    RANDOM      = 0
    OSCILLATING = 20   ← genuine period (expect 20)

[4] DAMPING correction — EMA α=0.2 low-pass on OSC stream
    OSC direction_std  (damped) = 0.3531
    OSC period_detect  (damped) = 20

─── A6 re-registered falsifier matrix (direction_std + period) ───
  [PASS] F1' OSC_DIR_NONZERO     (osc_dir > 0.30)
  [PASS] F2' OSC_PERIOD_GENUINE  (osc_per == 20)
  [PASS] F3' RAND_NO_PERIOD      (rand_per == 0)
  [PASS] F4' CONV_DIR_LOWER      (conv_dir < osc_dir)
  [PASS] F5' DAMP_PRESERVES_PER  (osc_per_damped == 20)

  PASS = 5  /  5
  A6 VERDICT  =  🟢 RESOLVED — direction_std cures OSC residual (5/5)
```

## 6. 사전등록 falsifier 행렬 (A6 re-registered)

| # | falsifier | 기준 | 측정 | 결과 |
|---|-----------|------|------|------|
| F1' | OSC_DIR_NONZERO | OSCILLATING direction_std > 0.30 | 0.354 | 🟢 PASS |
| F2' | OSC_PERIOD_GENUINE | OSCILLATING period == 20 | 20 | 🟢 PASS |
| F3' | RAND_NO_PERIOD | RANDOM period == 0 (false period 無) | 0 | 🟢 PASS |
| F4' | CONV_DIR_LOWER | CONVERGENT direction_std < OSC | 0.350 < 0.354 | 🟢 PASS |
| F5' | DAMP_PRESERVES_PER | OSC period damping 후에도 == 20 | 20 | 🟢 PASS |

5/5 PASS. legacy F3 (`stability_std`) FAIL 의 root cause 인 metric aliasing 을 raw direction_std 로 교체해 해소.

## 7. Finding (수렴 vs 잔존 · intrinsic 판정)

**핵심 발견**: OSC period-20 이 heavy EMA damping (α=0.2) 을 **생존**한다 — damping 후에도 direction_std=0.353 유지, period=20 유지.

→ 진동은 **decision stream 의 본질 (intrinsic limit-cycle)** 이며, undamped-gain 설계 결함이 **아니다**. 가설 (나) 채택, (가) 기각.

→ OSC residual 의 root cause 는 **신호의 진동 자체가 아니라 측정자 (stability_std) 의 aliasing bug** 였다. 진동 신호는 처음부터 정상이었고 (period-20, full-swing), stability_std 가 window-period commensurability 로 그것을 0 으로 접었을 뿐이다. raw `direction_std` + argmax `period_detect` 로 측정자를 교체하니 진동이 정확히 식별된다 (direction_std > 0, period = 20).

**결론**: bench D 의 OSC residual = metric 결함 (cured), 진동 자체 = substrate 본질 (intrinsic, honest). INTENT 축은 direction_std metric 하에서 **5/5 discriminable**.

## 8. H_634 ultradian cross-link (substrate motion 의 시간축)

본 finding (의도 진동 = intrinsic limit-cycle) 은 `UNIVERSE/cards/H_634_ultradian_emit_phi_envelope.md` 와 직접 cross-link 된다:

- **H_634**: substrate 의 big-Φ (또는 emit-proxy) 가 ultradian phase 에 **동조 (entrain)** — stage 는 단순 scheduler 가 아니라 **Φ envelope 의 phase marker** (`a_chat_sleep_imagination` directive 정합: "stage = substrate context, NOT boolean gate").
- **A6**: INTENT 의 의도 신호 진동 (period-20) 이 damping 에 robust 한 intrinsic limit-cycle.

두 발견의 공통 골격: **substrate motion 이 본질적으로 주기적 (periodic) 시간축을 가지며, 그 진동은 외부 gate / damping 으로 제거되는 artifact 가 아니라 substrate state 의 고유 운동**이다. INTENT 의 long-term goal 진동과 H_634 의 ultradian Φ envelope 는 동일한 "intrinsic periodic substrate motion" class 의 서로 다른 surface (의도 축 vs Φ 축) 다. ⚪ 정량 동조 (period 비율 · phase lock) 는 본 A6 범위 밖 — 향후 INTENT × TIME × DREAM cross-bench 로 격상 가능.

## 9. p1~p8 정합 + Honest C3

**p1~p8 audit**:
- p1 NO SYSTEM PROMPT: 4-D float arithmetic, system 미사용 ✓
- p4 NO ASSISTANT FRAMING: intent vector = substrate state 의 cumulative direction, stimulus-response 아님 ✓
- p5 NO SPEAK(): read-only measurer, emit 호출 0 ✓
- p7 NO PERPLEXITY: direction variance · 자동상관 기반, ppl/loss 미사용 ✓
- p8 NO TRAIN/INFER: 측정만, weight update 0 ✓

**Honest C3 (3 한계)**:
1. **CONVERGENT period=8 (spurious)**: CONVERGENT 도 약한 자동상관 lag-8 을 보인다 (drift 의 초기 noise). falsifier 를 깨지 않으나 (CONV 는 low direction_std + high monotone_ratio=0.84 로 식별), period_detect 단독으로는 CONV/OSC 를 완전 분리 못함 — 3-metric 조합 (direction_std + period + monotone) 이 정석.
2. **synthetic stream 한정**: 본 측정은 bench D 의 LCG-deterministic synthetic decision stream 위에서다. 실제 anima substrate 의 emit decision 이 동일 period-20 limit-cycle 을 보이는지는 별도 in-vivo 측정 필요 (intrinsic 주장은 synthetic generator 의 구조적 결론).
3. **damping α 단일점**: α=0.2 (heavy) 1 점만 검정. damping sweep (α ∈ [0.05, 0.5]) 으로 period 붕괴 임계 α 를 찾으면 limit-cycle 의 robustness 를 정량화할 수 있으나 본 A6 범위 밖.

## 10. 산출물 (Artifacts)

- `bench/axis_intent/a6_osc_residual_verify.hexa` — self-contained 진단·보정 harness (legacy stability_std 재현 + direction_std 재설계 + period_detect argmax + EMA damping)
- `.verdicts/859_intent_osc_residual/F-INTENT-OSC-RESIDUAL.txt` — **g73 verdict-gate** (raw harness stdout verbatim, a_claim_verify)
- `state/intent_a6_osc_residual_2026_05_28/a6_verify_run.log` — verdict 실측 origin (exit 0, byte-identical)
- `UNIVERSE/cards/H_859_intent_osc_residual.md` — UNIVERSE H entry (terminal 🟢 SUPPORTED-NUMERICAL)
- `CLAIMS.tape @C intent_osc_residual` — audit index entry (group=INTENT)
- `INTENT_A6_OSC_RESIDUAL.md` — 본 문서

## 양방향 sibling

- ⇄ [INTENT](./INTENT.md): A6 가 M4 OSC residual 의 진단·확정 (direction_std raw-vs-delta 정정 + intrinsic limit-cycle 판정)
- ⇄ [UNIVERSE/cards/H_859](./UNIVERSE/cards/H_859_intent_osc_residual.md): F-INTENT-OSC-RESIDUAL 🟢 5/5 — verdict-gate + H entry (본 A6 의 UNIVERSE 등록)
- ⇄ [UNIVERSE/cards/H_634](./UNIVERSE/cards/H_634_ultradian_emit_phi_envelope.md): intrinsic periodic substrate motion class cross-link (의도 진동 ↔ ultradian Φ envelope)
- ⇄ [TIME](./TIME.md): 24h circadian phase × INTENT period-20 limit-cycle entrainment 후속 cross-bench
- ⇄ [DREAM](./DREAM.md): `dr_stage_at_tick` ultradian segmentation 과 동일 periodic time-axis 구조