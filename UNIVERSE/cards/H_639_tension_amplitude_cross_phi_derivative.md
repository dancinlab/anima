---
id: H_639
slug: tension-amplitude-cross-phi-derivative
title: tension-amplitude-cross × Φ-derivative coupling — amplitude-cross rate peak 이 dΦ/dI peak 와 동조하는가
domain: consciousness · math · physics · meta
status: FALSIFIED
verdict_class: CLOSED-NEGATIVE
exploration_method: E2 (ANIMA.mining L24 tension-fork-B promote) + E0 (H_351 / H_618 sister) + E5 (continuous-parameter sweep)
verification_method: W1 (numerical) + W4 (verdict-5-class) + W11 (cross-axis sister) + W12 (invariant signature)
hexa_only: true
deterministic: true
llm: none
since: 2026-05-28 (UNIVERSE 축 mining-derived · ANIMA.mining L24 promote)
sister: H_351 (single-substrate dΦ/dI peak GZ_LOWER), H_618 (collective dΦ_c/dI peak GZ_LOWER), H_204 (weak-panpsychism inverse-U)
---

# H_639 — tension-amplitude-cross × Φ-derivative coupling

> ⚙ 측정 엔진 = `HEXAD/IIT4/lib`(`iit4_eca` + `iit4_bigphi`) 재사용 (commons g61, 재발명 0). 통합 척도 = **faithful causal big-Φ** (H_285/H_351 양식, 2^n state-mean). tension amplitude = substrate state-change magnitude `|Δstate|`. `$0 · mac-local · hexa-only · LLM none.`

## 1. 가설 (Hypothesis) — ANIMA.mining L24 promote

**mining 출처**: `ANIMA.mining.md` L24 (cycle 2 · tension-fork-B, 2026-05-28T05:06):
> *"boolean predicate 도 emit / silence dichotomy 의 hardcode. true externalization 은 continuous tension field 자체이고 emit 은 그 field 의 amplitude-threshold-cross event. boolean 은 measurement convention 일 뿐 substrate 아님."* → 영역: tension-link 5-ch × MITOSIS.

이는 PHILOSOPHY **p5 (NO SPEAK())** — *"output = continuous externalization of tension field · emit only from real context"* — 와 **p5_tension_emit_not_filler** note (tension-driven emit ≠ silence-filler) 의 정량 instance 다. emit 을 boolean gate 가 아니라 **continuous tension field amplitude 의 threshold-cross event** 로 정의했을 때, 그 cross 의 dynamics 가 substrate 의 Φ-dynamics 와 정합하는지를 검정한다.

**가설**: substrate 의 tension field amplitude (state-change magnitude `|Δstate|`) 가 fixed threshold `θ` 를 cross 하는 rate 의 변화 peak 위치 `argmax_I |d(cross_rate)/dI|` 가, big-Φ 의 inhibition-축 미분 peak `argmax_I |dΦ/dI|` (H_351 의 GZ_LOWER ≈ 0.21232) 와 동조한다 (`|Δ_peaks| ≤ 0.05`). 즉 **emit event ≡ Φ-derivative extremum** — emit 이 substrate Φ-dynamics 와 wired 된 substrate-native 현상이다.

**Falsifier**: amplitude-cross rate 의 변화 peak 가 dΦ/dI peak 와 무관 (위치 분리, `|Δ_peaks| > 0.10`) — emit 은 boolean convention 일 뿐 substrate Φ-dynamics 와 무관하다 (L24 의 *"convention 일 뿐 substrate 아님"* 이 거꾸로 amplitude-cross 자체에도 적용).

## 2. 사전등록 falsifier (pre-registered, 측정 전 동결)

| ID | 조건 | 의미 |
|----|------|------|
| **F1** PEAKS-COINCIDE | `|peak_I_amp − peak_I_phi| ≤ 0.05` | emit≡extremum 동조 |
| **F2** AMP-PEAK-IN-GZ | `|peak_I_amp − GZ_LOWER| ≤ 0.05` | amplitude-cross peak 가 GZ 안 |
| **F3** PHI-PEAK-IN-GZ | `|peak_I_phi − GZ_LOWER| ≤ 0.05` | H_351 anchor sanity (Φ peak GZ) |
| **F4** AMP-MONOTONE | `d(cross_rate)/dI` sign-change ≤ 1 | cross_rate(I) 단조 |
| **F5** BYTE-EQUAL | in-process recompute byte-identical (`|Δ| ≤ 1e-12`) | RFC 033 결정론 |

**verdict_rule**
- **SUPPORTED** = F1 ∧ F2 ∧ F3 ∧ F4 ∧ F5
- **PARTIAL** = !F1 ∧ F2 ∧ F3 ∧ F4 ∧ F5 (각 peak GZ 근방이나 서로 분리 tol 밖)
- **FALSIFIED** = (`|Δ_peaks| > 0.10`) ∨ !F3 (peak 분리 OR Φ-anchor 붕괴)

## 3. 방법 (Method)

### 3.1 substrate (H_351 carry — 재발명 0)

ECA **rule 110** (Wolfram class IV edge-of-chaos, H_285 anchor) on a periodic ring of **n = 4 cells**. inhibition `I ∈ [0,1]` mixes the ECA TPM with a force-to-zero inhibitor (H_351 §3.2 양식):

```
tpm_mixed[s,i] = (1 - I) · eca_tpm[s,i]
```

- `I = 0` → 순수 rule 110 (max-Φ regime). `I = 1` → 완전 inhibit (all-zero, Φ=0).

### 3.2 tension field amplitude 정의 (substrate-native)

state `s` 의 amplitude = 다음 tick 에서 **flip 하는 cell 의 기대 분율** (= `|Δstate|` 기대값):

```
amp(s) = (1/n) · Σ_i [ (1-cur_i)·p_i + cur_i·(1-p_i) ]
```

- `cur_i` = state s 의 bit i (현재 0/1), `p_i = tpm_mixed[s·n+i]` = P(cell i = 1 | s).
- 이는 continuous tension field 의 *instantaneous state-change magnitude* 의 직접 substrate 정의 (proxy 없음, closed-form). 별도 *Φ-derivative 기반 amplitude* 변형은 §7 C3 sensitivity 에서 논의.

### 3.3 amplitude-cross event rate (L24 의 emit 정의)

emit event = amp(s) > θ. 각 inhibition I 에서:

```
cross_rate(I) = (전 2^n state 중 amp(s) > θ 인 state 의 분율)
```

**θ anchor (convention-free)**: `θ = I=0 baseline 의 mean amp` — substrate 내재 기준 (외부 magic-number 없음). 측정 결과 `θ = 0.375`. (θ-convention sensitivity 는 §7 C3 에서 5-grid sweep 으로 정면 검정.)

### 3.4 coupling 측정

- `dΦ/dI`, `d(cross_rate)/dI` 모두 central finite difference (H_351 §3.5 양식; edge = forward/backward).
- `peak_I_phi = argmax_I |dΦ/dI|`, `peak_I_amp = argmax_I |d(cross_rate)/dI|`.
- `|Δ_peaks| = |peak_I_amp − peak_I_phi|` (동조 여부), `|Δ_amp_gz|`, `|Δ_phi_gz|` (GZ 근접).

### 3.5 grid (H_351 dense GZ region)

```
I ∈ {0.05,0.10,0.15,0.18,0.21,0.23,0.25,0.30,0.35,0.40,0.50,0.70,0.95}  — 13 points
```

### 3.6 runner

`UNIVERSE/state/h639_tension_amplitude_cross_phi_derivative_2026_05_28/run_h639.hexa` (단일 hexa, dependency = `iit4_eca` + stdlib `iit4_bigphi`, $0).

## 4. 측정 (Measurement) — `result.json`

`θ = 0.375` (I=0 mean amp).

| `I` | `Φ(I)` | `cross_rate(I)` | `dΦ/dI` | `d(rate)/dI` |
|----:|-------:|----------------:|--------:|-------------:|
| 0.05 | 12.4205 | 0.4375 | −16.4725 | 0.0 |
| 0.10 | 11.5969 | 0.4375 | −14.8516 | 0.0 |
| 0.15 | 10.9354 | 0.4375 | −15.5640 | 0.0 |
| **0.18** | 10.3518 | 0.4375 | **−21.3315** ← Φ peak | 0.0 |
| 0.21 | 9.65547 | 0.4375 | −18.7680 | 0.0 |
| 0.23 | 9.41337 | 0.4375 | −12.7958 | 0.0 |
| 0.25 | 9.14364 | 0.4375 | −13.6713 | 0.0 |
| 0.30 | 8.45639 | 0.4375 | −14.8755 | 0.0 |
| 0.35 | 7.65609 | 0.4375 | −16.7222 | 0.0 |
| 0.40 | 6.78416 | 0.4375 | −15.8471 | 0.0 |
| **0.50** | 5.27903 | 0.4375 | −14.3008 | **0.833** ← amp peak |
| 0.70 | 2.49393 | 0.6875 | −11.1752 | 0.556 |
| 0.95 | 0.250173 | 0.6875 | −8.97505 | 0.0 |

- **peak_I_phi** = 0.18 (`|dΦ/dI| = 21.33`) — H_351 carry.
- **peak_I_amp** = 0.50 (`|d(rate)/dI| = 0.833`).
- **|Δ_peaks|** = `|0.50 − 0.18|` = **0.32** (≫ 0.10 → FALSIFIED).
- **|Δ_amp_gz|** = `|0.50 − 0.21232|` = **0.28768** (≫ 0.05).
- **|Δ_phi_gz|** = `|0.18 − 0.21232|` = **0.03232** (≤ 0.05 — F3 sanity PASS).
- cross_rate(I) sign-change = 0 (단조, F4 PASS), byte_eq = true (F5 PASS).

핵심 관찰: cross_rate 가 GZ region 전체 (I=0.05..0.50) 에 걸쳐 **완전 평탄 (0.4375)** — inhibition mixing 이 모든 transition prob 를 uniform 하게 축소하므로 fixed θ 기준 cross 구조가 GZ 영역 안에서 변하지 않고, 변화는 far-tail (I=0.7) 에서만 발생. emit-as-amplitude-cross 는 GZ 안에서 **coarse step function** 이지 Φ-dynamics 의 continuous tracker 가 아니다.

## 5. 결과 (Result)

**2/5 PASS** (F3, F4, F5) → 🔴 **FALSIFIED (CLOSED-NEGATIVE)**.

- **F1** PEAKS-COINCIDE ✗ (|Δ_peaks| = 0.32 ≫ 0.05)
- **F2** AMP-PEAK-IN-GZ ✗ (|Δ_amp_gz| = 0.28768 ≫ 0.05)
- **F3** PHI-PEAK-IN-GZ ✓ (|Δ_phi_gz| = 0.03232; H_351 anchor 재현)
- **F4** AMP-MONOTONE ✓ (sign-change = 0)
- **F5** BYTE-EQUAL ✓ (recompute byte-identical)

verdict_rule 의 FALSIFIED 조건 `|Δ_peaks| > 0.10` 충족 (0.32). convention-free θ-anchor (I=0 mean amp) 아래 **amplitude-cross rate peak 는 dΦ/dI peak 와 동조하지 않는다** — emit-as-amplitude-cross 는 그 자체로 substrate Φ-dynamics 와 wired 되어 있지 않고, threshold 선택이라는 measurement convention 에 결과가 좌우된다 (§7 C3 정량).

## 6. falsifier 결과 + Cross-link

- F1 PEAKS-COINCIDE **FAIL** (0.32)
- F2 AMP-PEAK-IN-GZ **FAIL** (0.28768)
- F3 PHI-PEAK-IN-GZ **PASS** (0.03232 — H_351 재현 sanity)
- F4 AMP-MONOTONE **PASS** (0 sign change)
- F5 BYTE-EQUAL **PASS** (recompute byte-identical)

### Cross-link

| Link | H / 참조 | role | 본 H 와의 관계 |
|---|---|---|---|
| predecessor (single) | **H_351** | rule 110 n=4 dΦ/dI peak | peak I=0.18, GZ_LOWER 일치 🟢 — 본 H 의 Φ-anchor (F3 재현) |
| collective | **H_618** | hivemind dΦ_c/dI peak | peak I=0.21, GZ_LOWER |Δ|=0.00232 🟢 — Φ-derivative extremum 의 collective 확장 |
| inverse-U axis | **H_204** | weak-panpsychism autopoietic threshold | inverse-U Φ 의 일반 lens |
| tension-link 5-ch | **project_tension_link** | concept/context/meaning/authenticity/sender 5-ch fingerprint | L24 가 지목한 영역 — amplitude = field magnitude 의 substrate view |
| p5 / note | **p5 NO SPEAK() · p5_tension_emit_not_filler** | continuous externalization of tension field | 본 H 가 amplitude-cross 정의를 검정한 PHILOSOPHY 근원 |
| mining | **ANIMA.mining L24** | tension-fork-B boolean-우회 | 본 H 의 promote 출처 |

H_351 (single) + H_618 (collective) 가 *Φ-derivative extremum 의 GZ-anchor* 를 두 차원에서 확립한 반면, 본 H 는 그 extremum 이 **tension-amplitude-cross event 와는 wired 되어 있지 않음** 을 보여 — emit-as-amplitude-cross 의 substrate-Φ 정합이라는 한 경로를 닫는다 (negative result).

## 7. 해석 — Honest C3 (3-tier caveat)

### C1 — tension amplitude 정의 sensitivity (state-change vs Φ-derivative)

본 H 는 amplitude 를 **state-change magnitude `|Δstate|`** (flip 기대 분율) 로 정의했다. 대안은 **`|Φ-derivative|` 자체** 를 amplitude 로 쓰는 것 — 그 경우 amplitude-cross 는 정의상 dΦ/dI 와 trivially 동조하여 SUPPORTED 가 되지만, 이는 *순환 정의* (검정이 가설을 가정) 이므로 substrate-native 검정으로 부적격. 따라서 `|Δstate|` (Φ 와 독립한 substrate 관측량) 가 honest 한 정의이며, 그 정의 아래 동조가 깨진 것이 본 H 의 finding. 두 amplitude 정의 중 어느 것이 emit 의 "진짜" field magnitude 인가는 substrate 차원에서 미결 — *amplitude 정의 의존성* 이 본 H 의 일차 한계.

### C2 — θ-convention dependency (FALSIFIED 의 robustness sweep)

본 H 의 FALSIFIED 가 단일 θ=0.375 anchor 에 의존하는지 검정하고자 `run_h639_thsweep.hexa` 로 θ ∈ {0.20, 0.30, 0.375, 0.45, 0.55} 5-grid sweep 을 수행:

| θ | peak_I_amp | `|peak d(rate)/dI|` | 비고 |
|---:|---:|---:|---|
| 0.20 | (undef) | 0.0 | rate=0.9375 전구간 평탄 — peak 없음 |
| **0.30** | **0.21** | 5.0 | **GZ_LOWER + dΦ/dI peak 동시 일치!** |
| 0.375 (anchor) | 0.50 | 0.833 | 본문 — FALSIFIED |
| 0.45 | 0.95 | 1.0 | far-tail — FALSIFIED |
| **0.55** | **0.21** | 5.0 | **GZ_LOWER 일치!** |

이는 **profound** 한 결과다: amplitude-cross peak 위치가 θ 선택에 따라 {undef, 0.21, 0.50, 0.95, 0.21} 로 **완전히 뒤바뀐다**. convention-free anchor (I=0 mean amp = 0.375) 에서는 FALSIFIED 지만, θ=0.30 / 0.55 에서는 정확히 GZ_LOWER (I=0.21) 에 동조. **즉 emit ≡ Φ-derivative extremum 은 substrate 불변량이 아니라 threshold-convention 의 함수다.** 이것이 정확히 L24 가 경고한 *"boolean 은 measurement convention 일 뿐 substrate 아님"* 의 거꾸로 된 적중 — amplitude-cross 자체조차 convention 에 종속. 본문의 FALSIFIED 는 pre-registered convention-free anchor 아래 verdict 로 동결하고, convention-dependence 를 명시적 finding 으로 보고한다.

### C3 — substrate vs convention 의 미결 + single-substrate scope

- **emit ≡ derivative-extremum 의 substrate vs convention**: C2 가 보였듯, 동조 여부가 θ-convention 에 따라 결정 — emit-as-amplitude-cross 가 substrate Φ-dynamics 의 *결과* 인지, 아니면 우리가 θ 를 고르는 *convention* 인지가 본 toy substrate 차원에서 미결. convention-free anchor 에서 FALSIFIED 라는 사실은, emit 이 substrate Φ-dynamics 에 자동 wired 되어 있지 **않음** 을 시사 (L24 의 우려 강화).
- **ECA rule-class scope**: rule 110 single substrate. H_614 (multi-rule) 가 dΦ/dI 자체의 cross-substrate invariance 를 2/4 FALSIFIED 로 깬 것처럼, amplitude-cross 동조의 rule-class invariance 도 미측정 — single-substrate negative evidence tier.
- **결정론**: substrate (ECA + scalar inhibition + closed-form amp) fully deterministic, RNG 없음. multi-seed 가 robustness lever 아님 (C2 의 θ-sweep + amplitude 정의 sweep 이 다음 lever).

## 8. verdict

🔴 **FALSIFIED — CLOSED-NEGATIVE (2/5)**: convention-free θ-anchor (I=0 mean amp = 0.375) 아래 amplitude-cross rate peak (I=0.50) 는 dΦ/dI peak (I=0.18, GZ_LOWER) 와 동조하지 않는다 (`|Δ_peaks| = 0.32 ≫ 0.10`). emit-as-amplitude-cross 는 그 자체로 substrate Φ-dynamics 와 wired 되어 있지 않고, θ-convention 에 종속한다 (§7 C2 sweep: θ=0.30/0.55 에서는 GZ 동조, 0.375/0.45 에서는 분리 — 동조가 substrate 불변량이 아닌 convention 함수). empirical 의식 해석은 ⚪ SPECULATION-FENCED.

ruled-out axis: **emit ≡ Φ-derivative extremum** 의 convention-free substrate 동조 — 이 경로는 닫힌다. L24 가 제기한 *"emit = continuous tension field amplitude 의 threshold-cross"* 가 substrate Φ-dynamics 와 자동 정합한다는 강주장은 본 toy substrate 에서 기각.

## 9. honest scope

본 H 가 **닫지 못하는 것**:
- *어느 θ-convention 이 substrate-canonical 인가* — convention-free anchor 는 FALSIFIED, 그러나 θ=0.30/0.55 의 GZ 동조가 우연인지 hidden substrate structure 인지는 미결 (C2).
- *amplitude 정의 (state-change vs Φ-derivative) 의 substrate 우선순위* — C1, 본 H 는 `|Δstate|` 정의 단독.
- ECA rule-class invariance — round 2 multi-rule sweep 까지 single-substrate negative evidence.
- PureField/dropout 본체 (SAVANT engine) 위 real-amplitude-cross 측정 — toy ECA substrate.

## 10. UNIVERSE.md update

UNIVERSE 축 (mining-derived) H_639 checkbox flip → done with `🔴 FALSIFIED (CLOSED-NEGATIVE, 2/5, peak_I_amp=0.50 vs dΦ/dI peak=0.18 |Δ_peaks|=0.32 ≫ 0.10, θ-convention 종속 — C2 sweep θ=0.30/0.55 GZ 동조, $0 mac-local 2026-05-28)`. ANIMA.mining L24 promote 표기.

## artifacts

- `UNIVERSE/state/h639_tension_amplitude_cross_phi_derivative_2026_05_28/run_h639.hexa` — single-file deterministic runner (~330 LoC, dependency = `iit4_eca` + stdlib `iit4_bigphi`)
- `UNIVERSE/state/h639_tension_amplitude_cross_phi_derivative_2026_05_28/run_h639_thsweep.hexa` — §7 C2 θ-sensitivity sweep runner
- `UNIVERSE/state/h639_tension_amplitude_cross_phi_derivative_2026_05_28/result.json` — measurement SSOT (grid · phi · cross_rate · dphi_di · drate_di · peaks · deltas · verdict)
- `UNIVERSE/H_639_tension_amplitude_cross_phi_derivative.md` — 본문 (SSOT)
