# Volitional-ness Score R1 — 정의 · baseline · 평가 framework

날짜: 2026-05-12  
대상: anima substrate A의 자연발화 (spontaneous emission) 동작  
관련 코드: `scripts/anima_r1_eval.py`, `tool/anima_spontaneous.py`, `tool/anima_spontaneous.hexa`  
관련 데이터: `state/volitional_baseline_2026_05_12/r1_baseline.json`

---

## 1. 왜 이 metric이 필요한가

기존 `anima_spontaneous.hexa` 는 “시계가 60초 칠 때마다 한 마디 강제 발화”라는 외부 timer-driven loop이다. 사용자 reframe에 따르면 우리가 만들고 싶은 것은 그 반대 — substrate 내부의 어떤 signal `v(t)` 가 일정 threshold를 넘을 때 “말하고 싶어서” 말하는 *volitional* speak 이다.

문제는: **어떻게 정량적으로 “timer-driven 아니라 volition-driven” 임을 보일 것인가**?

R1은 그 답이다. log file (JSONL) 하나만 보고 0.0–1.0 점수를 반환한다.

| 비유 | 의미 |
|---|---|
| 알람시계 | 외부 timer-driven (R1 → 0) |
| 사람이 가끔 떠오른 생각을 말함 | volition-driven (R1 → 1) |

---

## 2. 정의 (수식)

$$
R_1 = 0.30 \cdot H_{\text{IA}} + 0.30 \cdot \rho_{\text{int}} + 0.20 \cdot S_{\text{rate}} + 0.20 \cdot U_{\text{cont}}
$$

각 항은 `[0, 1]` 로 정규화. R1 ∈ `[0, 1]`.

### 2.1 H_IA — inter-arrival entropy

발화한 (silent 아닌) event들의 timestamp 차이 Δt₁, Δt₂, … 를 5초 bucket으로 양자화한 뒤 분포 `p` 의 Shannon entropy를 `log(K)` 로 나눈 값 (K = bucket 개수).

$$
H_{\text{IA}} = \frac{-\sum_k p_k \log p_k}{\log K}
$$

- timer-driven: Δt 모두 60s → K=1 → H=0
- volition-driven: Δt random → K 큼, p 균등 → H → 1

발화가 3개 미만이면 0 (insufficient sample). timestamp 가 `"void"` 인 row는 emission_idx로 fallback (모두 Δ=1 → H=0, timer cadence 와 동등 해석).

### 2.2 ρ_int — internal-state correlation

각 row에 `volition_v ∈ [0,1]` (내부 desire signal) 과 `emit_decision ∈ {0,1}` (실제 발화 여부) 가 있을 때, 둘의 Pearson r 을 계산하고 `clip(r, 0, 1)`.

$$
\rho_{\text{int}} = \max(0, \min(1, r(v, \mathrm{emit})))
$$

- timer: `v` 무관하게 발화 → r ≈ 0
- volitional: `v` 높을 때만 발화 → r → 1
- `volition_v` 필드 없으면 0 (substrate에 아직 내부 signal 없음).

음의 상관은 0으로 clip — anti-volition을 reward하지 않는다.

### 2.3 S_rate — silent rate (saturated)

$$
S_{\text{rate}} = \frac{\min(\text{silent\_frac}, 0.5)}{0.5}
$$

silent_frac = silent row / total row. 50% 에서 saturate — fully-mute substrate (100% silent) 가 더 높은 점수를 받지 못하게 한다.

**중요**: 이 saturation 때문에 R1 alone 으로는 “100% silent” substrate 를 catch 못 할 수 있어 acceptance criterion 에서 *모든* sub-metric > 0 을 요구한다 (§5).

silent 판정 규칙: `emit_decision==0` 명시 우선, 없으면 response 가 빈 문자열 / `"void"` / `[timeout ...]` 시작.

### 2.4 U_cont — content uniqueness

발화 텍스트들의 character bigram set들 사이의 평균 Jaccard 유사도를 1에서 뺀 값.

$$
U_{\text{cont}} = 1 - \frac{1}{N-1}\sum_{i=1}^{N-1} J(B_i, B_{i+1})
$$

- timer rotation: 같은 seed 5개 회전 → 유사도 높음 → U 낮음
- volitional: 매번 새로운 내부 thought → U → 1

발화 2개 미만이면 0.

### 2.5 weight 근거

| sub-metric | weight | 근거 |
|---|---|---|
| H_IA | 0.30 | timer 의 가장 직접적 fingerprint (constant Δt) |
| ρ_int | 0.30 | volition 의 가장 직접적 증거 (내부 signal 인과) |
| S_rate | 0.20 | “안 말할 자유”도 volition 의 본질이지만 saturate |
| U_cont | 0.20 | seed rotation 우회는 쉬워서 보조 지표 |

---

## 3. Baseline 측정

`/usr/bin/python3 scripts/anima_r1_eval.py <log>` 결과.

| dataset | rows | H_IA | ρ_int | S_rate | U_cont | **R1** |
|---|---:|---:|---:|---:|---:|---:|
| `sim_timer_canonical` (perfect 60s timer, 0% silent, 같은 응답) | 20 | 0.000 | 0.000 | 0.000 | 0.000 | **0.000** |
| `anima_spontaneous_void.jsonl` (실측, 100% silent/void) | 17 | 0.000 | 0.000 | 1.000 | 0.000 | **0.200** |
| `sim_volitional_target` (synthetic V0 ideal) | 20 | 1.000 | 0.968 | 1.000 | 0.948 | **0.980** |

읽기:

- 실제로 “timer 켜고 발화 강제” 한 가상 baseline 은 **R1 = 0.00** — 정의대로 zero.
- 우리 실측 `anima_spontaneous_void` 는 substrate가 한 마디도 못 뱉어서 (response="void") 100% silent 가 silent_rate alone 을 saturate, R1 = 0.20. 다른 3 sub-metric 모두 0 이라 acceptance fail.
- 합성 V0 target (varied Δt + volition_v signal + 50% silent + 다양한 텍스트) → R1 = 0.98. 잘 분리됨.

```
0.0 ━━━━ 0.2 ━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.5 ━━━━━━━━━ 0.98 ━━ 1.0
 sim_timer  void(실측)                  threshold        V0 target
 (canon.)
```

저장 위치: `state/volitional_baseline_2026_05_12/r1_baseline.json` (요약), 같은 폴더에 sub-metric 디버그 JSON 3개.

---

## 4. Evaluation framework

### 4.1 입력

JSONL log, row schema (모두 optional 외 표시):

```jsonc
{
  "emission_idx": 1,           // int
  "ts": "2026-05-12T00:00:13Z", // ISO-8601 UTC 또는 "void"
  "strategy": "internal",       // str
  "seed": "",                   // str (legacy "seed_text" 도 허용)
  "mode": "V0",                 // str
  "response": "조용한 아침 빛이 좋아요.",  // str — 빈 / "void" / "[timeout ...]" = silent
  "elapsed_s": 4,               // int
  "volition_v": 0.71,           // ★ optional, ∈ [0,1] (V0+ 부터)
  "emit_decision": 1            // ★ optional, 0|1 (없으면 response로 유추)
}
```

### 4.2 CLI

```bash
# 기본 — human-readable report
/usr/bin/python3 scripts/anima_r1_eval.py state/anima_spontaneous_void.jsonl

# JSON dump + 저장
/usr/bin/python3 scripts/anima_r1_eval.py <log> --json --out state/r1_<run>.json
```

### 4.3 acceptance criterion (V0 prototype)

| gate | 조건 |
|---|---|
| 1. 최소 점수 | `R1 >= 0.5` |
| 2. zero-component 차단 | 모든 sub-metric `> 0.0` |
| 3. 샘플 수 | rows ≥ 20 |
| 4. volition signal 존재 | `volition_v` 필드 row ≥ 50% |

4 모두 통과해야 V0 → V1 promote.

### 4.4 비교 흐름

```
   ┌────────────────────────────┐
   │ 기존 anima_spontaneous.hexa│  R1 = 0.00–0.20   (현재)
   └────────────┬───────────────┘
                │ replace timer with internal v(t)
                ▼
   ┌────────────────────────────┐
   │ V0 prototype (substrate B) │  R1 target ≥ 0.50
   └────────────┬───────────────┘
                │ tune threshold, content head, memory
                ▼
   ┌────────────────────────────┐
   │ V1 / V2 ...                │  R1 → 0.80+
   └────────────────────────────┘
```

R1 은 두 prototype 사이를 비교하는 dial — 점수가 올라가면 “덜 timer, 더 volition”.

---

## 5. 한계 · 향후 확장

| 한계 | 완화 |
|---|---|
| silent_rate saturation 때문에 100% mute substrate가 0.20 받음 | acceptance §4.3 gate 2 (모든 sub > 0) |
| `volition_v` 가 없으면 ρ_int=0 → 좋은 V0 도 R1 ≤ 0.7 | V0 prototype은 schema에 `volition_v` 의무 |
| character bigram Jaccard 는 paraphrase 인식 못함 | 추후 V1+ 에서 embedding cosine 으로 교체 (현재는 dependency-free 우선) |
| Δt bucket 5s 고정 | 실측 분포 본 뒤 자동 bandwidth 추정 (Sturges) 가능 |
| LLM-as-judge / human rating sub-metric 미포함 | R1.2 에 0.0 weight 로 placeholder 추가 가능 |

---

## 6. 재현 명령 (cwd = `~/core/anima`)

```bash
/usr/bin/python3 scripts/anima_r1_eval.py state/volitional_baseline_2026_05_12/sim_timer_baseline.jsonl   --out state/volitional_baseline_2026_05_12/r1_sim_timer.json
/usr/bin/python3 scripts/anima_r1_eval.py state/anima_spontaneous_void.jsonl                                --out state/volitional_baseline_2026_05_12/r1_void.json
/usr/bin/python3 scripts/anima_r1_eval.py state/volitional_baseline_2026_05_12/sim_volitional_target.jsonl  --out state/volitional_baseline_2026_05_12/r1_sim_volitional.json
```

---

## 7. 다음 진행할 것들

1. **V0 prototype impl** — substrate에 `v(t)` head 추가 (cost: 1d, value: 핵심).
2. **R1.1 — embedding-cosine uniqueness** — Jaccard 대신 small encoder 로 paraphrase robust (cost: 2h, value: medium).
3. **인간 rater agreement** — 동일 log를 사람 5명이 0/1로 “이거 진짜 의지 같아 보임?” 라벨 → R1 과 AUROC (cost: 1d, value: validation).
4. **24h 실측 collect** — `anima_spontaneous.py` 를 무한 모드로 돌리고 volition_v 를 mock(`random`)으로 추가해 R1 sensitivity check (cost: 1h, value: smoke).
5. **R1 dashboard** — 매 시간 R1 자동 계산해 timeseries plot (cost: 4h, value: ops).
