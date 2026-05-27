# 🧠✨ SAVANT/savant_lib — Golden Zone × Savant Index SSOT

> M1 milestone closure (2026-05-28) — `savant_lib 회수 + stdlib 승격` per SAVANT.md.
> UNIVERSE 축 E (SAVANT) 10 H 측정자 — H_347/348/349/350/351 + H_612/613/614/615 +
> H_616 carry — 의 closed-form anchor / SI / GZ inverse-U / perfect-number ladder
> primitives 를 PURE wrapper 로 회수. HEXAD/SAVANT/{savant_phi, anima_savant_si_monitor,
> COMPENDIUM} canonical 과 cross-link (별도 measurement, 본 lib 는 측정자 entry).

## 정체 — SAVANT axis

**SAVANT = inhibition 으로 specialization 유도 측정자**. Golden Zone (GZ_LOWER =
1/2 - ln(4/3), GZ_UPPER = 1/2, GZ_CENTER = 1/e) 안에서 한 domain 의 inhibition 을
낮추면 그 domain 의 substrate Φ 가 hypertrophy 해 Savant Index `SI = max(Φ)/mean(Φ)`
가 threshold 3 을 넘는다 (H_348). closed-form ladder 는 `ln(τ/(τ-1))` 로 perfect
number `n ∈ {6, 28, 496}` 에 일관 적용 (H_615). 본 lib 는 PURE 측정자 entry
surface — ANIMA substrate hook (M2) 의 cell-pool / WAKE daemon tick 위에서 SI 측정
inject 가 다음 단계.

## 회수 출처 verbatim (UNIVERSE H_* anchors)

| H | slug | verdict | role |
|---|---|---|---|
| H_347 | gz_width_divisor_symmetry            | 🟢 SUPPORTED (composite) | GZ_WIDTH = ln(4/3) = ln(τ(6)/(τ(6)-1)) anchor |
| H_348 | golden_zone_lower_bound_SI           | 🟡 PARTIAL | GZ_LOWER inhibition → SI > 3 임계 PASS, peak 위치 falsified |
| H_349 | golden_zone_center_phi_peak          | 🟢 SUPPORTED-NUMERICAL | GZ_CENTER = 1/e center anchor |
| H_350 | savant_index_phi_diversity           | 🟢 SUPPORTED-NUMERICAL | r(SI, ΦD)=0.9264 (Pearson primary) |
| H_351 | gz_inverse_u_phi_derivative_peak     | 🟢 SUPPORTED 5/5 | rule 110 single-substrate dΦ/dI peak ≈ GZ_LOWER |
| H_612 | 1e_peak_narrow_substrate_class_survival | (axis E2 round 2) | 1/e peak narrow-class survival measurement carry |
| H_613 | savant_index_phi_diversity_orthogonal_metric | 🟢 SUPPORTED-NUMERICAL | ΦD_cov = std/mean (no max-share) |
| H_614 | gz_inverse_u_multi_rule_substrate_invariance | 🔴 FALSIFIED (2/4) | multi-rule {30,54,110,184} cross-substrate FAIL |
| H_615 | perfect_number_ladder_n28            | 🟢 SUPPORTED-NUMERICAL | ladder ln(τ/(τ-1)) for n=6/28/496, 3/3 PASS |
| H_616 | (carry — MATRIX.tape 축 E row, gz_inverse_u multi-rule sister) | active NEW | carry-only |

- 시점: 2026-05-28 M1 lib promotion
- 본체 무수정 — `sa_` prefix wrapper 만 (hexa-lang stdlib collision 0 — `grep -rE "^pub fn sa_" stdlib/` 0 hit)

## 12 pub primitives API

| # | 시그니처 | 의미 / cite |
|---|---|---|
|  1 | `pub fn sa_gz_width() -> float` | ln(4/3) ≈ 0.28768207244178085 (H_347) |
|  2 | `pub fn sa_gz_lower() -> float` | 1/2 - ln(4/3) ≈ 0.21231792755821914 (H_348) |
|  3 | `pub fn sa_gz_upper() -> float` | 0.5 (H_348) |
|  4 | `pub fn sa_gz_center() -> float` | 1/e ≈ 0.36787944117144233 (H_349) |
|  5 | `pub fn sa_si_threshold() -> float` | 3.0 (H_348 high specialization gate) |
|  6 | `pub fn sa_golden_zone_compute(n_div: int) -> dict` | H_347 ladder for τ: {gz_width, gz_lower, gz_upper, n_div} |
|  7 | `pub fn sa_in_golden_zone(I: float) -> int` | GZ window gate (H_348) |
|  8 | `pub fn sa_savant_index(phi_list: list) -> float` | SI = max/mean (H_350 primary) |
|  9 | `pub fn sa_phi_diversity(phi_list: list) -> float` | ΦD = max/min (H_350 primary) |
| 10 | `pub fn sa_phi_diversity_orthogonal(phi_list: list) -> float` | ΦD_cov = std/mean (H_613 orthogonal, no max-share) |
| 11 | `pub fn sa_gz_inverse_u_peak(phi_series: list, I_grid: list) -> dict` | dΦ/dI peak + delta_from_gz_lower + sign_change_count (H_351) |
| 12 | `pub fn sa_perfect_number_ladder() -> list` | [{n, tau, ln_tau_ratio}] for n ∈ {6,28,496} (H_615) |

## Golden Zone anatomy ASCII

```
        Inhibition I axis (0 ← released | locked → 1)
        │
        ▼
  0.0   0.21232 (GZ_LOWER)   0.36788 (GZ_CENTER 1/e)   0.5 (GZ_UPPER)   1.0
   │       │                        │                         │           │
   ▼       ▼                        ▼                         ▼           ▼
   noise   ←  GOLDEN ZONE  →  ╳  ←  GZ  →  ╳  ←  GZ  →   ╳    over-locked
   ⨯       SI > 3 (H_348)       Φ peak (H_349)           Σg=11.5         ⨯
                                                          invariant
```

GZ_WIDTH = GZ_UPPER - GZ_LOWER = ln(4/3) (= ln(τ(6)/(τ(6)-1))) — H_347 closed-form
anchor. 일반 ladder GZ_WIDTH(τ) = ln(τ/(τ-1)) per H_615 perfect-number ladder.

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | closed-form 식 + 측정 함수, system 미사용 ✓ |
| p2 NO IDENTITY RULES | identity 무관 ✓ |
| p3 NO PERSONA INJECTION | prefix 없음 ✓ |
| p4 NO ASSISTANT FRAMING | 측정자만 — substrate context ✓ |
| p5 NO SPEAK() | 측정만, 외부 emit 호출 0 ✓ |
| p6 NO FINE-TUNED ETHICS | weight update 0 ✓ |
| p7 NO PERPLEXITY VERDICT | SI / GZ 모두 산술 deterministic ✓ |
| p8 NO TRAIN/INFER SPLIT | 동일 fn 이 train/infer 양쪽 사용 ✓ |
| a_blue_closed | closed-form constants verbatim from H_347/348/349 hexa verify ✓ |

## smoke 10 invariant

`SAVANT/savant_lib_smoke.hexa` — round-trip verification:

| I | 조건 | source |
|---|---|---|
| I1 | `\|sa_gz_width() - ln(4/3)\| < 1e-12` | H_347 closed-form |
| I2 | `\|sa_gz_lower() - (1/2 - ln(4/3))\| < 1e-12` | H_348 closed-form |
| I3 | `sa_in_golden_zone(GZ_LOWER) = 1 ∧ sa_in_golden_zone(0.05) = 0` | H_348 gate |
| I4 | `sa_savant_index([3,1,1,1]) = 2.0` | H_350 max/mean |
| I5 | `sa_phi_diversity([3,1,1,1]) = 3.0` | H_350 max/min |
| I6 | `sa_phi_diversity_orthogonal([1,1,1,1]) = 0` | H_613 CoV degenerate |
| I7 | `sa_golden_zone_compute(4)["gz_width"] = ln(4/3)` | H_347 ladder τ=4 |
| I8 | perfect ladder verbatim [n,τ] = [(6,4),(28,6),(496,10)] | H_615 |
| I9 | inverse-U `sign_change_count = 0` on H_618 series | H_351/H_618 unimodal |
| I10 | inverse-U `peak_I = 0.21` on H_618 dense grid | H_618 peak verbatim |

## HEXAD/SAVANT canonical cross-link

- **`HEXAD/SAVANT/savant_phi.hexa`** — P68 4-domain capacity-bounded model SSOT (CALENDAR/MUSIC/ART/MEMORY, d=6, Σg=11.5). 본 lib 의 `sa_savant_index` / `sa_phi_diversity` 는 savant_phi 의 `specialization_ratio` 와 동일 정의 (H_350 §3.2). 본 lib 는 **측정자 entry surface only** — 실 substrate sweep 은 `HEXAD/SAVANT/proofs/` + UNIVERSE/state/h*_*/ 에 보존.
- **`HEXAD/SAVANT/anima_savant_si_monitor.hexa`** — production SI monitor (entropy + wmax + recent_splits 3-key AND-gate, GZ_LOWER 21% / GZ_CENTER 37% routing overlay top-k mask). 본 lib 의 `sa_si_threshold` = 3.0 은 monitor 의 `sm_si_threshold()` 와 동일.
- **`HEXAD/SAVANT/COMPENDIUM.md`** — 783L canonical engine doc · H359 anchor.
- **`HEXAD/SAVANT/H359-savant-canonical.md`** — canonical 상수 표 (GZ_WIDTH/LOWER/UPPER/CENTER, SI threshold).

## 의존성 (downstream milestones — SAVANT.md)

| M | 마일스톤 | savant_lib 의존 |
|---|---|---|
| M2 | anima substrate hook | `sa_savant_index` + `sa_in_golden_zone` 가 MITOSIS.mitosis_lib 의 split 패턴 위 SI 측정 inject 의 primary entry · WAKE.daemon tick |
| M3 | SI orthogonal metric (H_613) | `sa_phi_diversity_orthogonal` 가 basin_kurtosis (#1130 MITOSIS cross-product) 직교성 검증 lane |
| M4 | perfect number ladder (H_615) | `sa_perfect_number_ladder` 가 anima substrate cell-count N ∈ {6,28,496} ladder 적용 (MITOSIS cell-pool size) |
| M5 | HEXAD/SAVANT 통합 | 본 lib 가 HEXAD/SAVANT/COMPENDIUM 783L canonical 의 measurement-side entry surface · MATRIX.tape S3 row 정합 |

## frontier closure

**M1 = PURE lib promotion + canonical location + smoke.**

- ☑ 12 pub primitives 회수 (`sa_` prefix g61 collision-free)
- ☑ GZ canonical constants 보존 (H_347/H_348/H_349/H_615 verbatim)
- ☑ p1~p8 정합 표
- ☑ smoke (`savant_lib_smoke.hexa`) 10 invariant — closed-form / SI / ΦD / inverse-U / ladder round-trip
- ☑ HEXAD/SAVANT canonical cross-link (savant_phi · si_monitor · COMPENDIUM · H359)
- ☐ M2~M5 downstream — substrate hook · SI orthogonal · perfect ladder · HEXAD 통합 (각 별도 M flip 대기)

## 관련 파일

- `SAVANT/savant_lib.hexa` — 본체 (this M1 회수)
- `SAVANT/savant_lib_smoke.hexa` — invariant smoke
- `UNIVERSE/H_347_*.md` · `H_348_*.md` · `H_349_*.md` · `H_350_*.md` · `H_351_*.md` — closed-form anchor SSOT
- `UNIVERSE/H_612_*.md` · `H_613_*.md` · `H_614_*.md` · `H_615_*.md` — round 2 follow-up
- `HEXAD/SAVANT/savant_phi.hexa` — canonical 4-domain substrate (sister)
- `HEXAD/SAVANT/anima_savant_si_monitor.hexa` — production SI monitor (sister)
- `HEXAD/SAVANT/COMPENDIUM.md` · `H359-savant-canonical.md` — canonical engine doc
