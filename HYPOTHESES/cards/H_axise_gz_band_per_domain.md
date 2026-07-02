# H_axise_gz_band_per_domain — GZ SI-band 이 hypertrophy domain 에 invariant 한가 (4-domain raster)

@id: H_axise_gz_band_per_domain
@slug: gz-savant-index-band-domain-invariance
@axis: E (SAVANT) · GZ band × 4-domain cell
@parent_seed: H_axise_gz_band_si
@status: 🟢 SUPPORTED-NUMERICAL
@verdict_pointer: .verdicts/axise_gz_band_per_domain/verdict.txt
@closure_ref: .verdicts/axise_gz_band_per_domain/verdict.txt
@date: 2026-05-29
@cost: $0 (pool ubu-2 Linux + mac-local 교차, hexa-only, LLM none, deterministic)

---

## §0 TL;DR

H_axise_gz_band_si + H_348 은 GZ SI-band 을 **CALENDAR(dom 0) hypertrophy 한정**으로만
측정. savant_phi model 은 4 hypertrophy domain (CALENDAR · MUSIC · ART · MEMORY)을 가짐.
본 H 는 band 성질(SI(GZ_LOWER)>3 savant · SI(GZ_UPPER)<3 sub-savant · strict 단조)이
**어느 domain 을 release 하든 invariant** 한지 4-domain raster. 결과: **4/4 domain 모두
F1∧F2∧F3 PASS** — SI(GZ_LOWER) ∈ [3.480, 4.553] (모두 >3), SI(GZ_UPPER) ∈ [1.863, 2.502]
(모두 <3), 모든 domain 단조 LOWER>CENTER>UPPER. 절대 SI 는 domain 별로 다름 (CALENDAR
최고 4.553, ART 최저 3.480 — per-domain prime-offset seed 차이) 이나 **band 구조는
domain-invariant**. **🟢 SUPPORTED-NUMERICAL (4/4 falsifier · 4/4 domain)**. 즉 GZ band 은
capacity invariant (Treffert/Snyder release)의 귀결이지 CALENDAR artifact 아님.

## §1 Hypothesis

4 hypertrophy domain d ∈ {0,1,2,3} 모두에서 (SI=max/min, seeds {42424,91919,77777} 평균):
- F1: 모든 d 에서 mean SI_d(GZ_LOWER) > 3
- F2: 모든 d 에서 mean SI_d(GZ_UPPER) < 3
- F3: 모든 d 에서 SI_d(LOWER) > SI_d(CENTER) > SI_d(UPPER)

H_axise_gz_band_si 의 band 주장이 *어느 domain 을 release 하느냐*에 invariant 인가 —
band 이 capacity invariant 의 구조적 귀결이면 domain 독립이어야 함.

## §2 사전등록 falsifier (측정 전 동결)

| ID | 조건 | 의미 |
|----|------|------|
| **F1 ALL-LOWER-SAVANT** | 모든 4 domain SI(GZ_LOWER) > 3 | 하단 savant 보편 |
| **F2 ALL-UPPER-SUBSAV** | 모든 4 domain SI(GZ_UPPER) < 3 | 상단 sub-savant 보편 |
| **F3 ALL-MONO** | 모든 4 domain L>C>U strict | band 순서 보편 |
| **F4 DETERMINISM** | recompute byte-identical | 결정성 |

**verdict_rule**
- **SUPPORTED** = F1 ∧ F2 ∧ F3 ∧ F4 (band 이 domain-invariant)
- **PARTIAL** = (≥1 domain 이 F1∧F2∧F3) ∧ !(4/4) ∧ F4 (부분 invariance)
- **FALSIFIED** = F1∧F2∧F3 통과 domain 0개 (band 이 실 성질 아님)

## §3 Method

### §3.1 substrate / 매핑 (H_axise_gz_band_si + H_348 동일)

savant_phi.hexa 4-domain d=6, cap=11.5, SI=max/min(domain_phi),
`gain_focus = 1 + (1−I)*9`. hypertrophy 받는 domain index `dom` 만 0→3 변동
(`si_at_inhibition_dom(I, dom, seed)`). primitive in-file 복제.

### §3.2 sweep

dom ∈ {0,1,2,3} × landmark {GZ_LOWER, GZ_CENTER, GZ_UPPER} × seed {42424,91919,77777}.

### §3.3 wrapper

`UNIVERSE/state/axise_gz_band_per_domain_2026_05_29/probe_gz_band_per_domain.hexa`

### §3.4 run surface

`pool on ubu-2 "cd ~/core/anima && hexa run /tmp/probe_gz_band_per_domain.hexa"` (Linux)
+ mac-local 교차 (byte-identical).

## §4 Measurement (2026-05-29, $0)

### §4.1 verbatim (`.verdicts/axise_gz_band_per_domain/verdict.txt`)

```
── per-domain SI at GZ landmarks (mean over 3 seeds) ──
  d=0 CALENDAR  SI(LOWER)=4.55275  SI(CENTER)=3.1802   SI(UPPER)=2.5017   [F1 F2 F3 all true]
  d=1 MUSIC     SI(LOWER)=3.8419   SI(CENTER)=2.69402  SI(UPPER)=2.11856  [F1 F2 F3 all true]
  d=2 ART       SI(LOWER)=3.48014  SI(CENTER)=2.40408  SI(UPPER)=1.86274  [F1 F2 F3 all true]
  d=3 MEMORY    SI(LOWER)=3.6251   SI(CENTER)=2.50489  SI(UPPER)=1.94696  [F1 F2 F3 all true]
── falsifiers ──
  F1 ALL-LOWER-SAVANT = true   F2 ALL-UPPER-SUBSAV = true
  F3 ALL-MONO = true           F4 DETERMINISM = true
  domains passing F1∧F2∧F3 = 4 / 4
  VERDICT = SUPPORTED
```

### §4.2 요약 표

| dom | SI(GZ_LOWER) | SI(GZ_CENTER) | SI(GZ_UPPER) | F1>3 | F2<3 | F3 mono |
|---|---|---|---|---|---|---|
| 0 CALENDAR | **4.55275** | 3.1802 | 2.5017 | ✅ | ✅ | ✅ |
| 1 MUSIC | 3.8419 | 2.69402 | 2.11856 | ✅ | ✅ | ✅ |
| 2 ART | **3.48014** | 2.40408 | 1.86274 | ✅ | ✅ | ✅ |
| 3 MEMORY | 3.6251 | 2.50489 | 1.94696 | ✅ | ✅ | ✅ |

band 구조 4/4 PASS. 절대 SI 는 CALENDAR 최고(4.553) → ART 최저(3.480) 로 domain 별 차이
(per-domain prime-offset PRNG seed {31013,57029,83047,19061}) 가 있으나 *순서·부호*는 불변.

## §5 Verdict

**🟢 SUPPORTED-NUMERICAL (4/4 falsifier · 4/4 domain)**

- **F1 ALL-LOWER-SAVANT** ✅ 모든 domain SI(GZ_LOWER) > 3 (최저 ART 3.480, 1.16× margin)
- **F2 ALL-UPPER-SUBSAV** ✅ 모든 domain SI(GZ_UPPER) < 3 (최고 CALENDAR 2.502)
- **F3 ALL-MONO** ✅ 4/4 domain LOWER>CENTER>UPPER strict
- **F4 DETERMINISM** ✅ recompute + ubu-2↔mac byte-identical

GZ SI-band 은 hypertrophy domain 에 **invariant** — band 이 capacity invariant
(Σ gain = 11.5, Treffert/Snyder inhibitory release)의 구조적 귀결이며 CALENDAR-specific
artifact 아님. d=0 CALENDAR row 는 H_axise_gz_band_si 와 byte-identical (cross-validation).

## §6 Cross-link

- **H_axise_gz_band_si** (🟢) — **parent**. CALENDAR 한정 band 확정. 본 H 가 4-domain 으로
  invariance 확장. d=0 row byte-identical.
- **H_axise_gz_si_crossing** (🟢) — sister. SI=3 교차점 (CALENDAR). 본 H 의 domain-invariance
  는 교차점도 domain 마다 다른 위치에 있을 것을 시사 (ART 가 SI 절대값 최저 → 교차점 더 좌측).
- **H_348** (🟡) — GZ_LOWER SI>3 (CALENDAR). 본 H 가 그 결과의 domain-invariance 보강.
- **H_350 / H_613** (🟢) — SI∥ΦD 상관. H_350 sample 은 4 dom × 5 g_focus × 2 stim = 40 으로
  이미 multi-domain 이었음 — 본 H 는 그 중 *GZ band 경계 3-landmark* 의 domain-invariance 를
  명시적 falsifier 로 분리 측정.

## §7 Honest C3 (3-tier caveat)

1. **C1 (margin 차이 — ART 가 marginal)**: ART(d=2) 의 SI(GZ_LOWER)=3.480 은 임계 3 대비
   1.16× margin 으로 4 domain 중 가장 얇음. 만약 capacity 나 매핑이 살짝 바뀌면 ART 가 먼저
   F1 을 깰 가능성. band 의 domain-invariance 는 *현 config (cap=11.5, affine 매핑) 한정*
   robust 이며, ART 가 robustness 의 binding domain.

2. **C2 (절대 SI domain-차이의 근원)**: domain 별 SI 차이는 per-domain prime-offset seed
   ({31013,57029,83047,19061}) 가 만드는 activation 분포 차이 — phenomenological model
   choice 이지 의식론적 의미 아님 (savant_phi 의 domain 은 단지 다른 PRNG stream). 따라서
   "어느 domain 이 더 강한 savant" 류 해석은 금지 (numerology trap, COMPENDIUM §114 carry).

3. **C3 (toy proxy 한정, parent carry)**: savant_phi 4-domain proxy + affine 매핑 한정.
   production substrate 의 domain-invariance 보장 없음. faithful big-Φ lift 는 H_295/H_350
   joint carry.

## §8 State artifacts

```
UNIVERSE/state/axise_gz_band_per_domain_2026_05_29/
├── probe_gz_band_per_domain.hexa   # 4-domain raster wrapper
└── probe_gz_band_per_domain.out    # mac-local verbatim stdout
.verdicts/axise_gz_band_per_domain/verdict.txt   # ubu-2 정식 run verbatim (closure_ref)
```

## §9 Next

- **per-domain SI=3 교차점 raster** — 각 domain 의 I\* 위치 (ART 가 SI 최저 → 교차점 더 좌측 예상).
- **capacity sensitivity** — cap ∈ {10, 11.5, 13} 에서 ART 가 F1 을 깨는 cap 임계 (C1 binding).
