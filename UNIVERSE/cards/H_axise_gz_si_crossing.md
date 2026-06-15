# H_axise_gz_si_crossing — SI=3 savant 임계가 GZ band 내부, GZ_CENTER(1/e) 근처에서 교차하는가

@id: H_axise_gz_si_crossing
@slug: gz-savant-index-threshold-crossing
@axis: E (SAVANT) · GZ_CENTER × SI 전이점 cell
@parent_seed: H_axise_gz_band_si
@status: 🟢 SUPPORTED-NUMERICAL
@verdict_pointer: .verdicts/axise_gz_si_crossing/verdict.txt
@closure_ref: .verdicts/axise_gz_si_crossing/verdict.txt
@date: 2026-05-29
@cost: $0 (pool ubu-2 Linux + mac-local 교차, hexa-only, LLM none, deterministic)

---

## §0 TL;DR

H_axise_gz_band_si 가 SI(GZ_LOWER) > 3 (savant), SI(GZ_UPPER=0.5) < 3 (sub-savant) 을
확정 → savant 임계 SI=3 은 GZ band `[GZ_LOWER, GZ_UPPER]` *내부 어딘가*에서 교차.
본 H 는 band 을 10-point 조밀 grid 로 sweep 해 그 교차점 위치를 정밀화 — mean-SI(I) 가
**strict 단조 감소** (4.553 → 2.502), SI=3 교차점 **I\* = 0.398302** 가 GZ band 내부
(GZ_LOWER 0.212 < 0.398 < GZ_UPPER 0.5) AND GZ_CENTER=1/e≈0.36788 근처
(`|I* − 1/e| = 0.0304 ≤ 0.05`). 즉 **GZ_CENTER(1/e) 가 savant→sub-savant 전이점의 근방**.
**🟢 SUPPORTED-NUMERICAL (4/4 falsifier PASS)**. ubu-2 ↔ mac byte-identical.

## §1 Hypothesis

SI=3 savant 임계 교차점 `I*` (mean-SI 가 3 을 가로지르는 grid 구간의 linear 보간)이:
- (a) GZ band 내부: `GZ_LOWER < I* < GZ_UPPER`
- (b) GZ_CENTER 근처: `|I* − 1/e| ≤ 0.05`
- (c) mean-SI(I) strict 단조 감소 (single crossing — re-entry 없음)

H_axise_gz_band_si 의 band 주장을 *전이점 위치*로 정밀화 — GZ_CENTER=1/e (H_349 의
Φ-peak 가설은 🔴 falsified) 가 *SI* 축에서는 band 의 전이 중심인지.

## §2 사전등록 falsifier (측정 전 동결)

| ID | 조건 | 의미 |
|----|------|------|
| **F1 INSIDE-BAND** | `GZ_LOWER < I* < GZ_UPPER` | 교차가 band 내부 |
| **F2 NEAR-CENTER** | `|I* − 1/e| ≤ 0.05` | 교차 ≈ GZ_CENTER |
| **F3 MONO-SWEEP** | mean-SI(I) strict 단조 감소 | single crossing |
| **F4 DETERMINISM** | recompute byte-identical (`|Δ| ≤ 1e-12`) | 결정성 |

**verdict_rule**
- **SUPPORTED** = F1 ∧ F2 ∧ F3 ∧ F4
- **PARTIAL** = F1 ∧ F3 ∧ F4 ∧ !F2 (band 내부지만 1/e 근처 아님)
- **FALSIFIED** = !F1 ∨ !F3 (교차 band 밖 OR multi-crossing)

## §3 Method

### §3.1 substrate / 매핑 (H_axise_gz_band_si + H_348 동일)

savant_phi.hexa 4-domain d=6, cap=11.5, SI=max/min(domain_phi), dom=0(CALENDAR)
hypertrophy, `gain_focus = 1 + (1−I)*9` affine 매핑. primitive in-file 복제(import 회피).

### §3.2 fine grid

```
I ∈ {0.21232(GZ_LOWER), 0.25, 0.28, 0.30, 0.32, 0.34, 0.36788(GZ_CENTER), 0.40, 0.45, 0.50(GZ_UPPER)}
```
mean-SI = seeds {42424, 91919, 77777} 평균. 교차점 = mean-SI 가 3 을 가로지르는 인접
grid 쌍의 linear 보간.

### §3.3 wrapper

`UNIVERSE/state/axise_gz_si_crossing_2026_05_29/probe_gz_si_crossing.hexa`

### §3.4 run surface

`pool on ubu-2 "cd ~/core/anima && hexa run /tmp/probe_gz_si_crossing.hexa"` (Linux)
+ mac-local 교차 (byte-identical).

## §4 Measurement (2026-05-29, $0)

### §4.1 verbatim (`.verdicts/axise_gz_si_crossing/verdict.txt`)

```
── mean-SI(I) fine sweep ──
  I=0.21232  mean_SI=4.55275
  I=0.25  mean_SI=4.12285
  I=0.28  mean_SI=3.83506
  I=0.3  mean_SI=3.66439
  I=0.32  mean_SI=3.50791
  I=0.34  mean_SI=3.36371
  I=0.36788  mean_SI=3.1802
  I=0.4  mean_SI=2.98994
  I=0.45  mean_SI=2.72937
  I=0.5  mean_SI=2.5017
── crossing ──
  crossing found = true
  I* (SI=3)      = 0.398302
  |I* - 1/e|     = 0.0304218   (F2 needs <= 0.05)
── falsifiers ──
  F1 INSIDE-BAND = true   F2 NEAR-CENTER = true
  F3 MONO-SWEEP  = true   F4 DETERMINISM = true
  VERDICT = SUPPORTED
```

### §4.2 형상

mean-SI(I) 는 GZ_LOWER 4.553 → GZ_UPPER 2.502 로 strict 단조 감소. SI=3 은
GZ_CENTER(I=0.368, mean-SI=3.180) 와 I=0.40(mean-SI=2.990) 사이에서 교차 → I\*=0.3983.

```
mean_SI │ 4.5 ●  GZ_LOWER
        │ 4.0  ●
        │ 3.5    ●●●
        │ 3.0 ─ ─ ─ ─●─ ─ ─ I*=0.398 (savant threshold)
        │       ☆ GZ_CENTER 1/e (3.18, 임계 살짝 위)
        │ 2.5          ●  ● ●  GZ_UPPER
        │ 2.0 └────────────────
              0.21  0.37  0.50
```

## §5 Verdict

**🟢 SUPPORTED-NUMERICAL (4/4 falsifier PASS)**

- **F1 INSIDE-BAND** ✅ 0.21232 < 0.3983 < 0.5
- **F2 NEAR-CENTER** ✅ |0.3983 − 0.36788| = 0.0304 ≤ 0.05 (39% margin)
- **F3 MONO-SWEEP** ✅ mean-SI 10-point strict 단조 감소 (single crossing)
- **F4 DETERMINISM** ✅ recompute + ubu-2↔mac byte-identical

GZ_CENTER=1/e 는 SI band 의 savant→sub-savant **전이점 근방** — H_349 의 GZ_CENTER
Φ-peak 가설이 🔴 falsified 였던 것과 *독립 metric(SI)* 에서 GZ_CENTER 가 의미를 회복.
단 §7 C1 의 honest scope 참조 (1/e 자체는 임계 약간 위).

## §6 Cross-link

- **H_axise_gz_band_si** (🟢) — **parent**. band 경계(LOWER savant / UPPER sub-savant) 확정.
  본 H 가 그 band 의 *전이점 위치*를 정밀화. 동일 substrate · 매핑 · seed.
- **H_348** `golden-zone-lower-bound-SI` (🟡) — GZ_LOWER SI>3. mean-SI(GZ_LOWER)=4.553 일치.
- **H_349** `golden-zone-center-phi-peak` (🔴) — GZ_CENTER=1/e 의 *Φ-peak* universal 주장
  falsified. 본 H 는 동일 GZ_CENTER 가 *SI* 축에서는 band 전이점 근방임을 보임 — 두 metric
  (Φ-peak vs SI-threshold)에서 GZ_CENTER 의 역할이 다름 (Φ 에선 peak 아님, SI 에선 전이점 근처).
- **H_347** `gz-width-divisor-symmetry` (🟢) — GZ_WIDTH=ln(4/3). 본 H 의 교차점이 band 중앙
  부근(GZ_CENTER) 이라는 결과는 GZ_WIDTH 의 전이 폭 의미 보강.
- **H_350 / H_613** (🟢) — SI∥ΦD 상관. SI 단조 감소 = ΦD 동반 감소(r=0.93).

## §7 Honest C3 (3-tier caveat)

1. **C1 (GZ_CENTER 정확 vs 근방)**: I\*=0.3983 은 GZ_CENTER=0.36788 보다 *위쪽*에 위치
   (|Δ|=0.0304, tol 내부지만 정확 일치 아님). mean-SI(1/e)=3.180 은 임계 3 보다 ~6% 높음 —
   즉 GZ_CENTER 자체는 *아직 savant 쪽*이고, 진짜 SI=3 교차는 1/e 와 0.40 사이. "GZ_CENTER 가
   전이점" 은 strict 가 아니라 ±0.05 tolerance 내 *근방* 주장. F2 PASS 이나 정확 동치 아님.

2. **C2 (선형 보간 + grid 해상도)**: I\* 는 grid {0.36788, 0.40} 쌍의 linear 보간 — 진짜 SI(I)
   곡선이 그 구간에서 약간 볼록/오목이면 I\* 가 미세 이동. 2× 조밀 grid(예: 0.37, 0.38, 0.39)로
   교차점 정밀화는 별도 round. 단 |Δ|=0.0304 ≪ grid 간격 합 이라 F2 결론은 robust.

3. **C3 (toy proxy + affine 매핑 한정, H_348/H_axise_gz_band_si carry)**: savant_phi 4-domain
   proxy + `gain_focus=1+(1−I)*9` affine 매핑 한정. production substrate / 비선형 매핑에서
   교차점 위치 이동 가능. faithful big-Φ lift 는 H_295/H_350 joint carry.

## §8 State artifacts

```
UNIVERSE/state/axise_gz_si_crossing_2026_05_29/
├── probe_gz_si_crossing.hexa   # fine-sweep + crossing 보간 wrapper
└── probe_gz_si_crossing.out    # mac-local verbatim stdout
.verdicts/axise_gz_si_crossing/verdict.txt   # ubu-2 정식 run verbatim (closure_ref)
```

## §9 Next

- **교차점 2× grid 정밀화** (I ∈ {0.37, 0.38, 0.39, 0.40}) — I\* 가 1/e 와 정확 일치하는 매핑
  존재 여부 (C1/C2 해소).
- **per-domain band 전이점** (MUSIC/ART/MEMORY hypertrophy) — domain 별 I\* 가 같은가.
