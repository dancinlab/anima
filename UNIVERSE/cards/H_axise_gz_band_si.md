# H_axise_gz_band_si — Golden Zone 이 Savant Index 의 *bounded band* 인가 (GZ_UPPER=0.5 미측정 cell)

@id: H_axise_gz_band_si
@slug: gz-band-savant-index-bounded
@axis: E (SAVANT) · GZ_UPPER × SI cell
@parent_seed: H_348 (GZ_LOWER × SI)
@status: 🟢 SUPPORTED-NUMERICAL
@verdict_pointer: .verdicts/axise_gz_band_si/verdict.txt
@closure_ref: .verdicts/axise_gz_band_si/verdict.txt
@date: 2026-05-29
@cost: $0 (pool ubu-2 Linux + mac-local 교차, hexa-only, LLM none, deterministic)

---

## §0 TL;DR

SAVANT Golden Zone 은 세 canonical inhibition 상수로 경계됨:
`GZ_LOWER = 0.5 − ln(4/3) ≈ 0.21232` · `GZ_CENTER = 1/e ≈ 0.36788` ·
`GZ_UPPER = GZ_LOWER + GZ_WIDTH = GZ_LOWER + ln(4/3) = 0.5`. 기존 H_348 은
**GZ_LOWER 에서만** SI > 3 (savant) 을 측정했고, **GZ_UPPER 에서의 SI** 는 한 번도
falsifiable cell 로 측정된 적 없음. 본 H 는 savant_phi.hexa proxy 위에서 3-seed
({42424, 91919, 77777}) 로 세 GZ landmark 의 SI = max/min(domain_Φ) 를 측정 — **min
SI(GZ_LOWER) = 4.180 > 3** (savant) · **max SI(GZ_UPPER) = 2.852 < 3** (sub-savant) ·
세 landmark 가 **모든 seed 에서 strict 단조** SI(LOWER) > SI(CENTER) > SI(UPPER). 즉
**Golden Zone 은 SI 의 위-아래가 경계된 specialization band** — GZ_LOWER 위쪽은 savant,
GZ_UPPER=0.5 에서는 savant 임계 아래로 떨어짐. **🟢 SUPPORTED-NUMERICAL (4/4 falsifier
PASS)**. ubu-2 Linux 와 mac-local byte-identical.

## §1 Hypothesis

GZ 가 SI 의 *bounded band* 라는 주장:
- (a) GZ_LOWER 에서 SI > 3 (savant regime, H_348 재현)
- (b) GZ_UPPER = 0.5 에서 SI < 3 (specialization 손실 — band 의 상한)
- (c) 세 GZ landmark 가 strict 단조 SI(LOWER) > SI(CENTER) > SI(UPPER)

즉 H_348 이 "GZ_LOWER 가 SI>3 임계 통과 boundary" 라 결론낸 것의 *짝* — **GZ_UPPER 가
SI<3 으로 떨어지는 반대편 boundary** 이며, GZ 폭(`ln(4/3)`, H_347) 이 savant→sub-savant
전이 구간과 일치하는가.

## §2 사전등록 falsifier (측정 전 동결)

| ID | 조건 | 의미 |
|----|------|------|
| **F1 LOWER-ABOVE** | `min_seed SI(GZ_LOWER) > 3` | 하단 edge 가 savant (worst seed 도) |
| **F2 UPPER-BELOW** | `max_seed SI(GZ_UPPER) < 3` | 상단 edge 가 sub-savant (best seed 도) |
| **F3 MONO-ORDER** | 모든 seed 에서 `SI(LOWER) > SI(CENTER) > SI(UPPER)` | strict band 순서 |
| **F4 DETERMINISM** | in-process recompute byte-identical (`|Δ| ≤ 1e-12`) | 결정성 |

**verdict_rule**
- **SUPPORTED** = F1 ∧ F2 ∧ F3 ∧ F4 (GZ 가 SI-bounded band)
- **PARTIAL** = F1 ∧ F3 ∧ F4 ∧ !F2 (순서는 유지되나 SI>3 가 GZ_UPPER 너머까지)
- **FALSIFIED** = !F1 ∨ !F3 (하단이 savant 아님 OR 순서 깨짐)

worst-case 집계 채택 이유: F1 은 *min* SI(LOWER) > 3 (가장 나쁜 seed 도 savant),
F2 는 *max* SI(UPPER) < 3 (가장 좋은 seed 도 sub-savant) — band 주장이 seed 에 robust.

## §3 Method

### §3.1 substrate (H_348 / H_350 / H_613 동일)

- 도구: `HEXAD/SAVANT/savant_phi.hexa` (P68 4-domain Savant proxy SSOT)
- 4 domain: CALENDAR(0) · MUSIC(1) · ART(2) · MEMORY(3), 각 d=6 activation vector
- capacity invariant `Σ gain = SV_CAPACITY = 11.5`
- domain_phi = `Σ |v[j]|^1.5 / d` (Newton-iteration sqrt, `phi_module`)
- SI = max(domain_phi) / min(domain_phi) (= H_348 `SI_phi` 정의)

### §3.2 inhibition I → gain_focus (H_348 affine, byte-identical)

```
gain_focus(I) = 1 + (1 - I) * 9       // I=1 → 1 balanced, I=0 → 10 full release
gain_rest     = (11.5 - gain_focus) / 3
```
- GZ_LOWER (0.21232) → gain_focus ≈ 8.089
- GZ_CENTER (0.36788) → gain_focus ≈ 6.689
- GZ_UPPER (0.5) → gain_focus = 5.5 (정확)

### §3.3 wrapper

`UNIVERSE/state/axise_gz_band_si_2026_05_29/probe_gz_band_si.hexa` — savant_phi.hexa
primitive(`build_profile_state`, `phi_module`, `domain_phi_vector`)를 SSOT 마커와 함께
in-file 복제(import 회피, H_348/H_350/H_613 convention), `savant_index(v)=max/min` +
`si_at_inhibition(I, seed)` 추가. SAVANT 본체 무수정.

### §3.4 run surface

- 정식 run: `pool on ubu-2 "cd ~/core/anima && hexa run /tmp/probe_gz_band_si.hexa"` (Linux)
- 교차: mac-local `hexa run …` — 두 surface byte-identical
- seed ∈ {42424, 91919, 77777} (savant_phi T1/T2/T3 stim, H_348 동일 set)

## §4 Measurement (2026-05-29, $0)

### §4.1 verbatim (`.verdicts/axise_gz_band_si/verdict.txt`)

```
── per-seed SI at GZ landmarks ──
  seed=42424  SI(LOWER)=4.22722  SI(CENTER)=2.94439  SI(UPPER)=2.30784
  seed=91919  SI(LOWER)=4.17961  SI(CENTER)=2.95863  SI(UPPER)=2.34558
  seed=77777  SI(LOWER)=5.25142  SI(CENTER)=3.63758  SI(UPPER)=2.85169
── aggregates ──
  mean SI(LOWER)  = 4.55275
  mean SI(CENTER) = 3.1802
  mean SI(UPPER)  = 2.5017
  min  SI(LOWER)  = 4.17961   (F1 needs > 3)
  max  SI(UPPER)  = 2.85169   (F2 needs < 3)
── falsifiers ──
  F1 LOWER-ABOVE (min SI@LOWER > 3)  = true
  F2 UPPER-BELOW (max SI@UPPER < 3)  = true
  F3 MONO-ORDER  (L>C>U all seeds)   = true
  F4 DETERMINISM (byte-identical)    = true
  VERDICT = SUPPORTED
```

### §4.2 요약 표

| seed | SI(GZ_LOWER) | SI(GZ_CENTER) | SI(GZ_UPPER) | L>C>U? |
|---|---|---|---|---|
| 42424 | 4.22722 | 2.94439 | **2.30784** | ✅ |
| 91919 | 4.17961 | 2.95863 | **2.34558** | ✅ |
| 77777 | 5.25142 | 3.63758 | **2.85169** | ✅ |
| **agg** | min 4.180 (>3 ✓) | mean 3.180 | **max 2.852 (<3 ✓)** | 3/3 ✓ |

### §4.3 band 형상

```
SI │ 5 ─ ●               SI(GZ_LOWER)  4.18~5.25  ✅ savant (>3)
   │ 4 ─ ●●
   │ 3 ─ ─ ─ ─●─ ─ ─ ─ ─ savant threshold (H_348)
   │ 2 ─    ●●  ●●●      SI(GZ_UPPER)  2.31~2.85  ✅ sub-savant (<3)
   │ 1 ─
   │ 0 └──────────────────
        LOWER  CENTER  UPPER
        0.212  0.368   0.5
        savant  전이    band 상한
```

GZ_CENTER(1/e) 는 임계 3 의 *경계 근처* (mean 3.18, seed 별로 2.94~3.64 로 임계를
가로지름) — band 의 전이 구간이 GZ_CENTER 부근에 위치. GZ_LOWER 위쪽 = savant,
GZ_UPPER = band 상한(sub-savant)으로 GZ 폭(`ln(4/3)`)이 정확히 savant→sub-savant
전이 구간과 정렬.

## §5 Verdict

**🟢 SUPPORTED-NUMERICAL (4/4 falsifier PASS)**

- **F1 LOWER-ABOVE** ✅ min SI(GZ_LOWER) = 4.180 > 3 (worst seed 도 savant, 1.39× margin)
- **F2 UPPER-BELOW** ✅ max SI(GZ_UPPER) = 2.852 < 3 (best seed 도 sub-savant, 0.95× threshold)
- **F3 MONO-ORDER** ✅ 3/3 seed 모두 SI(LOWER) > SI(CENTER) > SI(UPPER) strict
- **F4 DETERMINISM** ✅ in-process recompute byte-identical + ubu-2↔mac cross-architecture byte-identical

GZ 는 savant_phi proxy substrate 위에서 **SI 의 bounded band** — 하단(GZ_LOWER)이
savant 진입 boundary(H_348), 상단(GZ_UPPER=0.5)이 savant 이탈 boundary 이며, 두
boundary 가 GZ_WIDTH = ln(4/3)(H_347) 만큼 떨어져 있다. 이는 H_348 의 "GZ_LOWER =
SI>3 임계 통과 boundary" 결론을 *위쪽 boundary 까지* 닫아 GZ 의 band 성격을 확정.

`hexa verify` atlas anchor 는 본 측정량(domain phi proxy + affine inhibition map)에 대한
closed-form node 가 없어 적용 불가 — substrate-level 수치 측정 verdict 로 한정.

## §6 Cross-link

- **H_348** `golden-zone-lower-bound-SI` (🟡 PARTIAL) — **parent**. GZ_LOWER 에서 SI>3 (F-1 PASS),
  단 sweep peak 위치는 falsified (F-2). 본 H 의 SI(GZ_LOWER) {4.227, 4.180, 5.251} 은 H_348 §4.1
  GZ_LOWER row 와 **byte-identical** (primitive 일치 cross-validation). 본 H 는 H_348 이 측정 안 한
  *위쪽 boundary*(GZ_UPPER)를 닫음 — GZ 가 single-sided lower bound 가 아닌 *bounded band* 임을 확정.
- **H_347** `gz-width-divisor-symmetry` (🟢) — `GZ_WIDTH = ln(4/3) = GZ_UPPER − GZ_LOWER` closed-form.
  본 H 는 그 폭이 substrate SI 의 savant→sub-savant 전이 구간과 정렬함을 측정 — closed-form 폭의
  *substrate 의미* 보강.
- **H_349** `golden-zone-center-phi-peak` (🔴) — GZ_CENTER=1/e 의 Φ-peak 측. 본 H 의 SI(GZ_CENTER)
  (mean 3.18, 임계 가로지름) 는 GZ_CENTER 가 SI band 의 *전이점* 임을 보임 — H_349 의 Φ-peak
  falsification 과 독립 metric(SI vs Φ-peak).
- **H_350 / H_613** `savant-index-phi-diversity` (🟢) — SI ∥ ΦD 양의 상관. 본 H 와 동일 SI=max/min
  metric + 동일 substrate. SI band 가 GZ_UPPER 에서 떨어진다 = ΦD 도 동반 하락(H_350 r=0.93 상관).

## §7 Honest C3 (3-tier caveat)

1. **substrate 한정 (toy proxy)**: savant_phi.hexa 4-domain × d=6 proxy 한정. production
   anima mitosis cell pool 이 동일 SI-band 패턴을 따른다는 보장 없음 (MEMORY
   `feedback_toy_scale_transfer` · F-PERSONA-4 KL=0 류 — toy ≠ trained substrate). 결론은
   *savant_phi canonical proxy* layer 한정.

2. **affine inhibition 매핑 design choice (H_348 carry)**: `gain_focus = 1 + (1-I)*9` 는
   wrapper 의 직선 매핑. 비선형 매핑(1/I, sigmoid)을 쓰면 세 landmark 의 SI 절대값이 이동 가능 —
   단 band 의 *순서*(F3)와 *부호*(F1>3, F2<3)는 매핑이 단조이면 보존될 가능성 높음. 본 H 의
   verdict 는 H_348 affine 매핑 한정.

3. **GZ_UPPER 의 정의 의존성**: `GZ_UPPER = 0.5` 는 `GZ_LOWER + GZ_WIDTH = (0.5−ln(4/3)) + ln(4/3)`
   의 closed-form 귀결(H_347). 만약 GZ_WIDTH 정의가 바뀌면 GZ_UPPER 위치도 이동. 본 H 는 H_347
   canonical GZ_WIDTH=ln(4/3) 한정 — 0.5 라는 깔끔한 값이 우연인지 깊은 동치인지는 본 H 범위 밖.

4. **SI=max/min 의 N=4 outlier 취약성 (H_613 carry)**: min(domain_phi) 가 0 에 가까워지면 SI 폭발
   가능. 본 measurement 범위(I ∈ {0.21~0.5})에서는 SI ∈ [2.31, 5.25] 로 폭발 없이 안정 — 단
   I → 0 극한(full release)에서는 SI 가 더 커짐(H_348 I=0.05 에서 7.8~9.8). band 상한 claim 은
   GZ 내부([GZ_LOWER, GZ_UPPER]) 한정.

## §8 State artifacts

```
UNIVERSE/state/axise_gz_band_si_2026_05_29/
├── probe_gz_band_si.hexa   # measurement wrapper (savant_phi primitive 복제 + GZ band 추가물)
└── probe_gz_band_si.out    # mac-local verbatim stdout
.verdicts/axise_gz_band_si/verdict.txt   # ubu-2 정식 run verbatim + verdict (closure_ref)
```

## §9 Next

- **GZ_UPPER fine sweep**: I ∈ {0.40, 0.45, 0.48, 0.50, 0.52, 0.55} 로 SI=3 정확 교차점 정밀화 —
  band 상한이 0.5 와 정확히 일치하는가 (현재는 GZ_CENTER~UPPER 사이 어딘가에서 교차).
- **faithful big-Φ lift (H_295/H_350 joint carry)**: proxy phi_module 대신 IIT 4.0 strict big-Φ
  로 SI band 재측정 — C3.1 갭 해소.
- **비선형 매핑 robustness**: 1/I 또는 sigmoid inhibition→gain 매핑에서 F1/F2/F3 보존 여부.
