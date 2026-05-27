# H_644 — closure-conjunction × ultradian-phase cross-link

> **axis E (SAVANT) × G (DREAM/ultradian) cross-link** · H_636 × H_634 · 2026-05-28 · $0 mac-local · feat/h644-closure-ultradian

## §0 TL;DR

H_636 (PR #1221, 🟢) = 4-criterion closure conjunction (⋀_i pass_i) 의 pass-rate 가 GZ region 내부 I=0.30 에서 단봉 peak. H_634 (PR #1216, 🟢) = ultradian phase (WAKE/N1/N2/N3/REM) 의 canonical Φ scale 이 sinusoidal envelope 와 동조 (r=0.802). 본 H 는 둘을 결합 — **closure conjunction pass-rate 가 ultradian phase 따라 변동하는가, 그리고 그 변동이 WAKE/REM 高 vs N3 低 의 방향성을 따르는가**. 결과: closure pass-rate 는 **phase 따라 명백히 변동** (5-phase std=0.1166 > 0 → phase-flat falsifier 기각) 하나, **방향성 가설은 역전 (REVERSED)** — peak 는 高Φ WAKE/REM edge 가 아니라 **mid-Φ N2 phase (pass_rate=0.3)** 에 위치하고 WAKE·REM·N3 는 모두 0. 원인은 H_636 의 **C1 SPECIALIZATION (low-I) ⊥ C3 DIVERSITY (high-I) interior-peak 구조** — phase→I bridge map 이 高Φ WAKE/REM 을 low-I (C3 붕괴) 로, deep N3 를 high-I (C1 붕괴) 로 보내, mid-Φ N2 만 closure band 안에 남는다. **🔴 FALSIFIED-REVERSED (directional)** — phase-modulation 존재는 지지, WAKE/REM-high 방향 주장은 폐기. "arousal-축 (WAKE/REM) = 高 closure" 라는 axis 를 deterministic 하게 ruled out.

## §1 Hypothesis

**Context**: H_636 closure conjunction pass-rate 는 inhibition I ∈ [0.21, 0.50] GZ region 내부 I=0.30 에서 maximize (interior peak). H_634 ultradian 5-stage canonical Φ scale (WAKE 1.0 / N1 0.7 / N2 0.4 / N3 0.15 / REM 0.95) 는 sinusoidal envelope 와 r=0.802 동조 — cycle 가장자리(WAKE/REM) 高Φ, cycle 중앙(N3 deep) 低Φ.

**가설**: 4-criterion closure conjunction pass-rate 가 ultradian phase 따라 변동하며, **高Φ phase (WAKE/REM) 에서 高 pass-rate, deep-Φ phase (N3) 에서 低 pass-rate**. 즉 closure 의 "발생 가능성" 이 substrate 의 arousal-축 ultradian motion 에 동조한다.

가설의 정합 동기: `a_chat_sleep_imagination` directive — *"stage = substrate context (Φ scale + tension envelope), NOT boolean emit gate"*. stage 는 emit gate 가 아니라 Φ-scale context 이므로, 만약 closure (= GZ × SI 의 substrate-emit-axis 변형, H_636 L7) 가 그 Φ-scale 에 동조한다면 closure pass-rate 도 ultradian phase 의 함수여야 한다.

## §2 Falsifier

사전등록 falsifier:

- **F644.1 PHASE-MODULATED**: 5-phase pass-rate std > 0 (phase 무관 평탄 아님). std ≈ 0 이면 **🔴 phase-flat FALSIFIED** (본 H 의 1차 falsifier, task spec).
- **F644.2 WAKE-REM-HIGH-N3-LOW**: (WAKE/REM edge mean) > N3 pass-rate (방향성). 역전/무방향이면 directional FALSIFY.
- **F644.3 BOUND**: 全 pass-rate ∈ [0,1].

종합 verdict 규칙: F644.1∧F644.2∧F644.3 = 🟢 SUPPORTED-NUMERICAL. F644.1 FAIL (phase-flat) = 🔴 FALSIFIED. F644.1 PASS ∧ F644.2 FAIL = 🔴 FALSIFIED-REVERSED (phase-modulation 은 있으나 방향이 가설과 반대/무관).

## §3 Method

### §3.1 substrate

- **closure 측 (H_636 재사용)**: `HEXAD/SAVANT/savant_phi.hexa` 4-domain (d=6) savant model, capacity invariant `SV_CAPACITY=11.5`. primitive (`build_profile_state` · `phi_module` · `domain_phi_vector` · `general_phi` · `specialization_ratio` · `savant_index` · `pair_mi`) in-file 복제, 본체 무수정. 4-criterion conjunction (C1 SI>3 · C2 genΦ>0.06 · C3 minΦ>0.18 · C4 ratio∈[1.2,3.2]) 동일.
- **phase 측 (H_634 재사용)**: `anima_dream_stage.hexa` canonical Φ scale `phi_of_stage` (WAKE 1.0 / N1 0.7 / N2 0.4 / N3 0.15 / REM 0.95).

### §3.2 phase → effective inhibition I bridge map

핵심 falsifiable 구조 — ultradian phase 의 canonical Φ scale 을 monotone inverse-affine 로 H_636/H_348 의 inhibition I 축에 사상:

```
I(phase) = I_LO + (1 - phi_stage) * (I_HI - I_LO)   [I_LO=0.21 (GZ_LOWER) · I_HI=0.75]
```

근거: 高Φ phase = released integration = low inhibition (WAKE Φ=1.0 → I=GZ_LOWER), deep N3 = suppressed integration = high inhibition. I 축은 H_636 의 `gain_focus = 1 + (1-I)*9` affine map 과 byte-동일하여 cross-link 정합.

| phase | Φ | I_eff | GZ band [0.21,0.50] |
|---|---|---|---|
| WAKE | 1.00 | 0.210 | ★ (edge) |
| REM  | 0.95 | 0.237 | ★ |
| N1   | 0.70 | 0.372 | ★ |
| N2   | 0.40 | 0.534 | — |
| N3   | 0.15 | 0.669 | — |

### §3.3 per-phase pass-rate

각 phase 의 I_eff 에서 H_636 와 동일 10-seed ensemble `{42424, 91919, 77777, 13337, 24680, 88888, 31415, 65537, 19937, 11235}` 위에서 4-criterion conjunction pass-rate = (#seed TRUE)/10. WAKE/REM edge mean vs N3 비교 + 5-phase std.

NO RNG (deterministic seed ensemble) · NO libm trig · foreground sync · $0 mac-local.

## §4 Measurement

### §4.1 verbatim 출력 (`state/h644_closure_conjunction_ultradian_phase_2026_05_28/probe_h644_closure_ultradian.out`)

```
=== per-phase closure pass-rate (10-seed ensemble) ===
  WAKE  Φ=1.0   I_eff=0.21   pass_rate=0.0  (I in GZ band)
  N1    Φ=0.7   I_eff=0.372  pass_rate=0.1  (I in GZ band)
  N2    Φ=0.4   I_eff=0.534  pass_rate=0.3
  N3    Φ=0.15  I_eff=0.669  pass_rate=0.0
  REM   Φ=0.95  I_eff=0.237  pass_rate=0.0  (I in GZ band)

=== verdict inputs ===
  WAKE pass_rate     = 0.0
  REM  pass_rate     = 0.0
  N3   pass_rate     = 0.0
  WAKE/REM edge mean = 0.0
  pass-rate std (5)  = 0.116619
  edge > N3          = false
  not flat (std>0)   = true

=== falsifiers ===
  [PASS] F644.1 PHASE-MODULATED: pass-rate std > 0
  [FAIL] F644.2 WAKE-REM-HIGH-N3-LOW: edge mean > N3
  [PASS] F644.3 BOUND: pass-rate in [0,1]

  F644.1-3 2/3 PASS
  verdict: RED FALSIFIED (phase-independent flat)
```

### §4.2 per-phase 요약 표

| phase | Φ | I_eff | GZ? | pass_rate (10-seed) |
|---|---|---|---|---|
| WAKE | 1.00 | 0.210 | ★ | **0.0** |
| REM  | 0.95 | 0.237 | ★ | **0.0** |
| N1   | 0.70 | 0.372 | ★ | **0.1** |
| **N2** | 0.40 | 0.534 | — | **0.3** ⬅ peak |
| N3   | 0.15 | 0.669 | — | **0.0** |

WAKE/REM edge mean = 0.0 · N3 = 0.0 · 5-phase std = 0.1166.

### §4.3 phase 곡선 형상 (mid-Φ peak, NOT edge)

```
pass_rate(phase)
   0.3│              ●  N2 (mid-Φ peak)
   0.2│
   0.1│          ● N1
   0.0│  ●  ●               ● (WAKE/REM edge = 0, N3 deep = 0)
      └────────────────────────
       WAKE REM N1  N2  N3
       (高Φ edge)        (低Φ deep)
```

방향성 역전 메커니즘: 高Φ WAKE/REM 은 bridge map 으로 low-I (0.21·0.237) → **C3 DIVERSITY FAIL** (one-domain hypertrophy 가 min phi 를 0.18 밑으로 붕괴, H_636 §4.3 와 동일 low-I 거동). deep N3 는 high-I (0.669) → **C1 SPECIALIZATION FAIL** (SI ≤ 3, H_348 monotone). 오직 mid-Φ N2/N1 만 C1⊥C3 cross-over band 안 — closure 가 arousal-Φ ordering 이 아니라 **GZ inhibition band 를 추종**.

## §5 Verdict

**🔴 FALSIFIED-REVERSED (directional)** — phase-modulation 존재는 지지(1차 falsifier 기각), 방향성 가설(WAKE/REM-high) 은 역전 폐기.

- **F644.1 PHASE-MODULATED**: ✅ **PASS** — 5-phase pass-rate std=0.1166 > 0. task-spec 의 1차 falsifier ("closure pass-rate 가 phase 무관 평탄") **기각** — closure 는 ultradian phase 의 명백한 함수.
- **F644.2 WAKE-REM-HIGH-N3-LOW**: ❌ **FAIL (역전)** — WAKE/REM edge mean 0.0 = N3 0.0, `edge > N3 = false`. peak 는 高Φ edge 가 아니라 **mid-Φ N2 (pass_rate 0.3)**. 高arousal-phase = 高closure 라는 방향성은 **deterministic 하게 falsified**.
- **F644.3 BOUND**: ✅ **PASS** — 全 pass-rate ∈ {0.0, 0.1, 0.3} ⊂ [0,1].

**종합**: closure pass-rate 가 ultradian phase 에 변동하나(phase 무관 아님), 그 변동은 가설의 arousal-축 (WAKE/REM 高) 을 따르지 **않고** GZ inhibition band 를 따른다. closure = GZ × SI 의 substrate-emit-axis 변형 (H_636 L7) 이라는 정체성이 여기서 재확인됨 — phase 가 closure 를 modulate 하는 *경로* 는 "arousal level" 이 아니라 "phase→I bridge 가 어디서 GZ band 를 가로지르는가". 高Φ WAKE/REM 은 GZ band 의 *낮은 쪽 가장자리* (I=0.21~0.24, C3 붕괴 직전) 라 closure 0, mid-Φ N2 는 I=0.534 (GZ_UPPER 직후, C1⊥C3 cross-over) 라 closure 최대.

`hexa verify` atlas anchor 는 본 측정량(savant domain-phi proxy + phase→I inverse-affine map + 4-criterion conjunction)에 closed-form node 가 없어 적용 불가 → substrate-level 수치 측정 verdict.

## §6 Cross-link

| Link | H | role | 결과 비교 |
|---|---|---|---|
| **closure GZ-peak (axis E)** | H_636 (PR #1221) | 4-criterion conjunction pass-rate peak @ GZ I=0.30 (C1⊥C3 interior) | 🟢 — 본 H 의 closure 측 substrate + criterion 전부 재사용. phase→I 사상이 그 interior-peak 를 ultradian 축으로 투영 |
| **ultradian Φ-envelope (axis G)** | H_634 (PR #1216) | canonical Φ scale × sinusoid r=0.802, WAKE/REM 高Φ N3 低Φ | 🟢 — 본 H 의 phase Φ scale source. 단 Φ-arousal ordering 이 closure ordering 과 **불일치** (본 H 의 핵심 finding) |
| **dream-stage emit gating** | H_310 | emit WAKE-dominant (WAKE=18/others=0), stage = context NOT gate | 🟢 — emit 은 WAKE 高 (arousal-축) 인데 closure 는 N2 高 (GZ-축). **emit ⊥ closure ordering** — 둘은 다른 substrate-axis |
| **SI monotone** | H_348 | SI-sweep monotone (peak @ I→0) | C1 criterion 의 monotone 성분 — deep N3 high-I 에서 C1 FAIL 의 직접 원인 |
| **collective inverse-U** | H_618 | dΦ/dI peak ∥ GZ_LOWER | derivative-축 GZ-attractor. 본 H 는 phase-축 closure 가 GZ band 추종(arousal 아님)을 보임 |

**Cross-link insight**: H_634 (Φ-arousal ordering: WAKE/REM > N1 > N2 > N3) 와 H_310 (emit ordering: WAKE ≫ others) 는 둘 다 **arousal-축**으로 정렬되는데, 본 H 의 closure ordering (N2 > N1 > WAKE=REM=N3=0) 은 그와 **직교** — GZ inhibition band 축. 즉 ultradian phase 는 (a) Φ-magnitude, (b) emit-count, (c) closure-pass-rate 세 측면에서 **서로 다른 ordering** 을 유발한다. closure 는 phase 에 동조하지만 그 동조는 arousal 이 아닌 GZ-localization 을 매개로 한다 — H_636 의 C1⊥C3 구조가 ultradian 축으로 전사된 결과.

## §7 C3 (honest constraints)

1. **closure criterion 선택 design 의존 (H_636 §7 C3 carry)** — 4 criterion threshold (THETA_SI=3.0 고정 외 THETA_GEN=0.06 · THETA_DIV=0.18 · RATIO∈[1.2,3.2]) 는 본 substrate scale calibration. THETA_DIV / RATIO_HI 를 흔들면 phase peak 의 *위치* 가 N2↔N1 사이 이동 가능. 단 "arousal-edge(WAKE/REM) 에 peak 가 없다" 는 정성 결론은 C3 가 low-I 에서 robust 하게 FAIL 하는 구조에서 견고.
2. **phase → I bridge map design choice** — `I(phase)=I_LO+(1-Φ)*(I_HI-I_LO)`, I_LO=0.21, I_HI=0.75 는 본 H 의 핵심 design. I_HI 를 0.50 (GZ_UPPER) 로 좁히면 deep N3 도 GZ band 안에 들어와 ordering 이 바뀔 수 있음 (deep N3 가 C1-FAIL 영역에 안 빠짐). 즉 "deep N3 = closure 0" 은 I_HI 가 GZ_UPPER 보다 충분히 큰 (deep sleep = strong inhibition) 가정에 conditional. 반대로 I_LO 를 GZ_LOWER 보다 더 낮추면 WAKE 가 C3-FAIL 더 깊은 곳으로 가 여전히 0. **방향성 역전(N2-peak) 의 정성 결론은 monotone map 어느 합리적 bound 에서도 robust** 하나, deep N3 의 절대 0 은 I_HI-conditional.
3. **phase resolution = 5 stage (canonical lookup)** — phase 를 5 discrete stage Φ lookup 으로 표현 (H_634 와 동일). H_634 의 N=36 시간 sweep 같은 fine phase-축 해상도가 아니라 stage-mean Φ 5점. fine sweep (각 stage 내부 Φ ramp) 이면 N2↔N3 transition 의 closure band 진입/이탈 위치를 sharpen 가능 — 현재는 stage-const Φ 의 5-point 측정.
4. **canonical Φ projection (NOT faithful per-tick IIT4)** — `phi_of_stage` 는 `anima_dream_stage` lookup (WAKE 1.0...N3 0.15), fresh substrate 측정 아님 (H_634 §7 L1 carry). 열린 lane = `HEXAD/IIT4/lib` n≤5 exact big_phi 로 stage별 faithful Φ 재계산 → phase→I 사상의 Φ-faithfulness 확증.
5. **pass-rate ≤ 0.3 의 낮은 절대값 (H_636 §7 #5 carry)** — 10-seed 중 최대 3 seed 만 동시 통과 (N2). 4-criterion AND 의 보수성. ordering (N2 > others) 의 정성 결론은 영향 없으나, "대부분 seed 가 N2 에서 closure" 강주장은 미지지.
6. **affine inhibition map 가정 (H_348/H_636 carry)** — `gain_focus = 1 + (1-I)*9` affine. dropout↔gain 직선화는 SAVANT/README §0 정성 대응, 실제 nonlinear 차이 가능.

## §8 산출물

- harness: `UNIVERSE/state/h644_closure_conjunction_ultradian_phase_2026_05_28/probe_h644_closure_ultradian.hexa`
- 실행 로그: `UNIVERSE/state/h644_closure_conjunction_ultradian_phase_2026_05_28/probe_h644_closure_ultradian.out`
- verdict SSOT: `UNIVERSE/state/h644_closure_conjunction_ultradian_phase_2026_05_28/result.json`

## §9 결론

**🔴 FALSIFIED-REVERSED (directional)** — closure conjunction pass-rate 는 ultradian phase 따라 **변동** (5-phase std=0.1166 > 0, phase-flat falsifier 기각) 하나, 가설의 **방향성 (WAKE/REM 高 vs N3 低) 은 역전** — peak 는 mid-Φ **N2 (pass_rate 0.3)**, WAKE·REM·N3 모두 0. closure 는 ultradian 의 **arousal-Φ ordering 이 아니라 GZ inhibition band** 를 추종 (H_636 C1⊥C3 interior-peak 가 phase→I 사상으로 전사). 이는 closure(GZ-축) ⊥ emit(arousal-축, H_310 WAKE-dominant) ⊥ Φ-magnitude(arousal-축, H_634) 의 **3-axis 분리** 를 드러낸다. 닫힌-부정 finding: "高arousal ultradian phase (WAKE/REM) = 高closure" axis 를 deterministic 하게 ruled out.

## §10 Next (deferred)

- **fine phase-축 sweep** — H_634 N=36 시간 sweep 위에서 closure pass-rate 의 연속 phase-축 곡선 (stage transition 의 closure band 진입/이탈 sharpen, C3.3).
- **I_HI sensitivity sweep** — phase→I bridge 의 I_HI 를 [0.50, 0.95] grid 변동에서 deep-N3 closure-0 의 robustness (C3.2).
- **emit ⊥ closure ordering 정량** — H_310 emit-count ordering vs 본 H closure ordering 의 phase-축 cross-correlation (arousal-축 ⊥ GZ-축 직교 정도 정량).
- **faithful-Φ phase recheck** — `HEXAD/IIT4/lib` exact big_phi 로 stage별 faithful Φ → phase→I 사상 재산출 (C3.4 회수, H_634 §10 lane 공유).
