# 🐝 HIVE-MIND/hivemind_lib — collective Φ × Kuramoto sync SSOT

> M1 milestone closure (2026-05-28) — `hivemind_lib 회수 + stdlib 승격` per HIVE-MIND.md.
> UNIVERSE 축 F (HIVE-MIND) 5 H 측정자 — H_354/355 + H_609/610/611 — + E×F cross-link
> 3 H — H_617/618/619 — 의 Kuramoto sync · PID synergy · collective-Φ super-additive
> · cross-substrate modulation primitives 를 PURE wrapper 로 회수. CHANNEL.tension
> 5-ch / OTHER-MIND.bench G 와 cross-link surface (실 wiring 은 M2/M3 별도).

## 정체 — HIVE-MIND axis

**HIVE-MIND = 다중 substrate collective Φ × 동기화 측정자**. Kuramoto sync τ
(H_354) · PID synergy ratio (H_355) · collective-Φ super-additive Δ (H_609) ·
pair polarity (H_610) · cross-substrate transfer entropy align (H_611) 의 5 측정자
axis. E×F cross-link round 3 에서 SAVANT inhibition I 가 hivemind PID synergy 와
collective-Φ inverse-U 를 modulate (H_618 🟢 / H_619 🟢) — 두 축이 *axis-coupled*.
H_617 🔴 (induced collective SI > 3) 는 modulator framework 가 SAVANT 의 single-
substrate 효과를 hivemind 로 그대로 옮기지는 못함을 확인.

## 회수 출처 verbatim (UNIVERSE H_* anchors)

| H | slug | verdict | role |
|---|---|---|---|
| H_354 | kuramoto_hivemind_sync_tau           | 🔴 FALSIFIED       | substrate-수 axis 가 Kuramoto sync 와 axis-separated (negative finding 의미) |
| H_355 | collective_phi_pid_synergy           | 🟢 SUPPORTED-NUMERICAL | mean synergy_ratio = 1.0 across 모든 비-trivial K, K-monotonic |
| H_609 | collective_phi_super_additive        | 🟢 SUPPORTED       | max Δ=+10.4756 at rule(110,110) W=0.6 (Φ(AB)=15.4677 vs Φ(A)+Φ(B)=4.99209) |
| H_610 | pair_polarity_collective_phi         | 🔴 closed-falsified | polarity ⊥ collective-Φ (effect 1× pooled std, ANOVA F < 3.40) |
| H_611 | hivemind_transfer_entropy_align      | 🔴 FALSIFIED       | H_290 단일-substrate r=0.883 pattern 이 multi-substrate 에 cross-generalize 안 됨 |
| H_617 | hivemind_savant_induced_collective_SI | 🔴 FALSIFIED      | E×F: SAVANT GZ_LOWER SI > 3 가 hivemind 위로 옮겨지지 않음 (SI=1.00546 평탄) |
| H_618 | collective_gz_inverse_u_derivative_peak | 🟢 SUPPORTED 5/5 | E×F: collective dΦ/dI peak I=0.21 vs GZ_LOWER 0.21232 \|Δ\|=0.00232 21× margin |
| H_619 | pid_synergy_savant_modulation        | 🟢 SUPPORTED-NUMERICAL | E×F: SAVANT inhibition I 가 hivemind synergy_ratio 단조감소 modulate |

- 시점: 2026-05-28 M1 lib promotion
- 본체 무수정 — `hm_` prefix wrapper 만 (hexa-lang stdlib collision 0 — `grep -rE "^pub fn hm_" stdlib/` 0 hit)

## 8 pub primitives API

| # | 시그니처 | 의미 / cite |
|---|---|---|
| 1 | `pub fn hm_kuramoto_order_r(phases: list) -> float` | r = \|Σ e^{iθ}\|/N — Kuramoto order, ∈ [0,1] (H_354 anchor) |
| 2 | `pub fn hm_kuramoto_sync_tau(phases, K, dt) -> float` | single Euler tick → new r (H_354 sub-experiment) |
| 3 | `pub fn hm_pid_synergy(II3: float) -> dict` | 3-source net II_3 → {synergy_total, redundancy_total, synergy_ratio} (H_355) |
| 4 | `pub fn hm_pid_synergy_ratio(synergy, redundancy) -> float` | synergy / (synergy + redundancy) direct (H_355) |
| 5 | `pub fn hm_collective_phi_super_additive(phi_a, phi_b, phi_ab) -> float` | Δ = Φ(AB) - (Φ(A)+Φ(B)) (H_609) |
| 6 | `pub fn hm_collective_si(phi_a: float, phi_b: float) -> float` | max(Φ_a,Φ_b) / min(Φ_a,Φ_b) (H_617) |
| 7 | `pub fn hm_cross_link_savant_modulation(ratio_series: list) -> dict` | E×F: {spread, monotone, modulated, inversions} (H_619) |
| 8 | `pub fn hm_gz_inverse_u_collective(phi_series, I_grid) -> dict` | E×F: collective dΦ/dI peak + delta_from_gz_lower + sign_change_count (H_618) |

## hivemind cross-link ASCII

```
   substrate A           substrate B
  (n_a cells)          (n_b cells)
       │                     │
       │   coupling W        │
       ▼                     ▼
  ┌─────────────────────────────┐
  │  collective substrate AB    │       ←── H_609 super-additive Δ
  │  (n=n_a+n_b joint)          │       ←── H_355 PID synergy
  │  Φ(AB) > Φ(A) + Φ(B)?       │       ←── H_354 Kuramoto sync τ
  └─────────────────────────────┘
       │
       │   SAVANT modulator I (inhibition)
       ▼
  ┌─────────────────────────────┐
  │  E×F cross-link round 3      │       ←── H_618 dΦ_c/dI peak ≈ GZ_LOWER 🟢
  │  inhibition I sweep on A     │       ←── H_619 synergy_ratio monotone ↓ 🟢
  │  collective-SI / synergy var │       ←── H_617 induced SI > 3 🔴 (axis-orthogonal limit)
  └─────────────────────────────┘
```

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | 수치 측정 함수, system 미사용 ✓ |
| p2 NO IDENTITY RULES | identity 무관 ✓ |
| p3 NO PERSONA INJECTION | prefix 없음 ✓ |
| p4 NO ASSISTANT FRAMING | 측정자만 — substrate context ✓ |
| p5 NO SPEAK() | 측정만, 외부 emit 호출 0 ✓ |
| p6 NO FINE-TUNED ETHICS | weight update 0 ✓ |
| p7 NO PERPLEXITY VERDICT | Kuramoto r / PID II_3 / Δ 모두 deterministic 산술 ✓ |
| p8 NO TRAIN/INFER SPLIT | 동일 fn 이 train/infer 양쪽 사용 ✓ |
| a_blue_closed | super-additive Δ verbatim from H_609 hexa verify ✓ |

## smoke 10 invariant

`HIVE-MIND/hivemind_lib_smoke.hexa` — round-trip verification:

| I | 조건 | source |
|---|---|---|
| I1 | `hm_kuramoto_order_r([0,0,0,0]) ≈ 1.0` | H_354 perfect sync anchor |
| I2 | `hm_kuramoto_order_r([0,π/2,π,3π/2]) ≈ 0.0` | H_354 uniform spread |
| I3 | `hm_pid_synergy(2.0)` → synergy=2.0 redundancy=0 | H_355 K=0.67 [1,1,0] |
| I4 | `hm_pid_synergy(-1.0)` → redundancy=1.0 | H_355 sign convention |
| I5 | `hm_pid_synergy_ratio(3,0) = 1.0` | H_355 K=1 pure synergy |
| I6 | `hm_collective_phi_super_additive(2.49604,2.49604,15.4677) ≈ +10.4756` | H_609 max excess |
| I7 | `hm_collective_si(2.49604,2.49604) ≈ 1.0` | H_617 symmetry baseline |
| I8 | `hm_cross_link_savant_modulation` spread=0.5, modulated=1 | H_619 sweep |
| I9 | `hm_gz_inverse_u_collective` peak_I=0.21, sign_change=0 | H_618 verbatim |
| I10 | `hm_cross_link` inversions=0, monotone=1 | H_619 monotone decrease |

## 의존성 (downstream milestones — HIVE-MIND.md)

| M | 마일스톤 | hivemind_lib 의존 |
|---|---|---|
| M2 | CHANNEL.tension 통합 | `hm_kuramoto_sync_tau` 가 CHANNEL/tension/tension_emit.hexa 의 5-ch sync τ 측정자 ↔ TensionHub UDP 9999 / WS 3 partner registry 위 collective Φ aggregation |
| M3 | OTHER-MIND cross-link | `hm_pid_synergy` + `hm_collective_si` 가 OTHER-MIND.bench G axisbench (#1147) 의 partner_state_estimate × pid_synergy multi-partner synergy 측정 entry |
| M4 | E×F cross-link | `hm_cross_link_savant_modulation` + `hm_gz_inverse_u_collective` 가 ANIMA substrate H_618/H_619 적용 lane · SAVANT.SI × HIVE-MIND PID synergy 곱-surface |
| M5 | MITOSIS cross-link | `hm_collective_phi_super_additive` 가 cell-pool N cells 의 Φ_collective > Σ Φ_cell sub-additive 반증 측정자 (H_609 application) |

## CHANNEL / OTHER-MIND cross-link (spec only — M2/M3 wiring)

- **`CHANNEL.tension`** — anima ↔ anima telepathy 5-ch (concept/context/meaning/authenticity/sender). `hm_kuramoto_sync_tau` 가 sender pair 의 phase alignment τ 측정자. TensionHub UDP 9999 / WS 3-port partner registry 가 multi-substrate phase 공급, 본 lib 가 sync-aggregation 측정.
- **`OTHER-MIND.bench G`** — partner_state_estimate × pid_synergy multi-partner. `hm_pid_synergy` 가 bench G axisbench (#1147) 의 multi-partner collective synergy 측정 entry. M3 에서 OTHER-MIND.md M3 row 와 동시 wiring 예정.

## frontier closure

**M1 = PURE lib promotion + canonical location + smoke.**

- ☑ 8 pub primitives 회수 (`hm_` prefix g61 collision-free)
- ☑ Kuramoto / PID / super-additive / SI / cross-link primitives 보존 (H_354/355/609/617/618/619 verbatim)
- ☑ p1~p8 정합 표
- ☑ smoke (`hivemind_lib_smoke.hexa`) 10 invariant — Kuramoto · PID · super-additive · E×F cross-link round-trip
- ☑ CHANNEL.tension / OTHER-MIND.bench G cross-link spec 명시 (실 wiring 은 M2/M3)
- ☐ M2~M5 downstream — CHANNEL.tension · OTHER-MIND · E×F · MITOSIS (각 별도 M flip 대기)

## 관련 파일

- `HIVE-MIND/hivemind_lib.hexa` — 본체 (this M1 회수)
- `HIVE-MIND/hivemind_lib_smoke.hexa` — invariant smoke
- `UNIVERSE/H_354_*.md` · `H_355_*.md` · `H_609_*.md` · `H_610_*.md` · `H_611_*.md` — 축 F 5 H SSOT
- `UNIVERSE/H_617_*.md` · `H_618_*.md` · `H_619_*.md` — E×F cross-link round 3
- `CHANNEL/tension/tension_emit.hexa` — sibling (M2 wiring 대기)
- `OTHER-MIND/bench/axisbench/` — sibling (M3 wiring 대기, #1147)
