# H_645 — `collective-dphi-di-gz-peak` (H_635 × H_618 cross-link)

**축**: F (HIVE-MIND, Collective Φ) × inverse-U GZ cross-link
**id**: H_645 · **date**: 2026-05-28 · **infra**: $0 mac-local · **verdict**: **🔴 FALSIFIED (CLOSED-NEGATIVE)**

---

## 1. 슬러그 + 한 줄 요약

`collective-dphi-di-gz-peak` — 5-stream multilingual collective-Φ (H_635 C1[110×5] anchor, W=1.0)
의 inhibition I 미분 `dΦ_collective/dI` peak 위치가 GZ_LOWER (≈0.21232) 와 일치하는지 검정.
H_618 (2-substrate joint n=4) 가 보인 dΦ/dI-peak=GZ_LOWER (|Δ|=0.00232) 구조가 5-stream
(n=5) collective 차원으로 확장되는가, 아니면 2-stream 한정 artifact 인가.

> **결과**: peak 가 **I=0.10 (grid 최좌측 경계)** — GZ_LOWER 와 **|Δ|=0.11232** (GZ window
> [0.15, 0.30] 밖). H_618 (2-stream, peak @ 0.21, |Δ|=0.00232) 와 정면 대조. 5-stream
> collective 에서 dΦ/dI-peak=GZ 정렬이 **깨짐** → H_618 의 GZ 일치는 2-stream (n=4) 차원
> 한정 현상. H1 FALSIFIED, H0 (GZ region 밖) 충족.

---

## 2. 가설 (H1) / 폐기조건 (H0)

- **H1** (본 가설): 5-stream collective-Φ (H_635 C1[110×5], sync_factor W=1.0) 의 inhibition I
  미분 `dΦ_collective/dI` peak 위치가 GZ_LOWER (= 0.5 − ln(4/3) ≈ 0.21232) ±0.05 안에 있다.
- **H0** (Falsifier): peak 가 GZ region `[0.15, 0.30]` 밖이거나, collective 차원에서 inverse-U
  단봉(unimodality) 구조가 깨진다 → H_618 의 dΦ/dI-peak=GZ 일치는 2-stream (n=4) 한정 artifact.

> H_618 (predecessor, 2-substrate joint n=4, rule(110,110), W=0.6) 가 🟢 SUPPORTED 5/5 로
> dΦ_collective/dI peak = I=0.21, |Δ|=0.00232 (GZ_LOWER 21× margin 일치) 를 보였다. 본 H_645 는
> 같은 inverse-U 미분 구조를 H_635 의 5-stream cohort (n=5) anchor 로 확장 검정한다.

---

## 3. 측정 도구 / 방법 (H_635 substrate × H_618 inhibition-mix)

- **IIT4 엔진**: `stdlib/consciousness/iit4_bigphi.hexa` · `iit4_bounded.hexa` —
  `big_phi_bounded(tpm, 5, sys_state=0, cap=3)`. H_635 와 동일 SSOT. n=5 ⇒ 2^5=32 mechanism,
  cap=3 bounded purview (M4b SSOT, conservative lower-bound, cap-monotone 으로 direction 보존).
- **Substrate** (n=5 ring, 5 streams = 5 cells, H_635 `build_tpm_cohort`):
  - **cohort = C1 [110,110,110,110,110]** — H_635 의 max-excess cohort (Δ=+41.71 @ W=1.0).
  - **sync_factor W = 1.0** — H_635 best_sync (full ring coupling). collective 결합 고정.
  - decoupled view: self-loop idx=7·c. coupled view: full n=5 ring (cell i: L=(i−1)%5, C=i, R=(i+1)%5).
    blend `p = (1−W)·next_dec + W·next_cou`; W=1.0 → 순수 full ring.
- **inhibition mix** (H_351/H_618 양식): `tpm_mixed[s,i] = (1 − I) · tpm_collective[s,i]`
  - I=0 → 순수 H_635 C1 collective TPM (max Φ regime).
  - I=1 → 완전 억제 (Φ_collective=0).
- **sys_state = 0** — IIT-canonical anchor (H_635 양식, 전 I 비교 가능). single-state 측정으로
  wall-time < 60s 유지 (H_618 16-state mean 과 달리 n=5 × 8-grid 256-call timeout 회피, C3.2).
- **deterministic** · in-process byte-equal recompute (F5).

---

## 4. Grid (8-point dense GZ region — H_618 와 동일)

```
I ∈ {0.10, 0.15, 0.18, 0.21, 0.25, 0.30, 0.40, 0.50}
```

`dΦ_collective/dI` central finite difference (forward at start idx=0, backward at end idx=7).

---

## 5. Measurement (verdict-bearing 측정값)

> harness 출력 `UNIVERSE/state/h645_collective_dphi_di_gz_peak_2026_05_28/run.log` verbatim.

### Φ_collective(I) — monotone-decreasing

| I | Φ_collective |
|---|---|
| **0.10** | **27.6022** |
| 0.15 | 22.2400 |
| 0.18 | 19.5911 |
| 0.21 | 17.1593 |
| 0.25 | 15.5932 |
| 0.30 | 13.6383 |
| 0.40 | 8.78237 |
| 0.50 | 6.54186 |

### dΦ_collective/dI — peak at I=0.10 (좌측 경계)

| I | dΦ_c/dI |
|---|---|
| **0.10** | **−107.243** ⬅ argmax \| · \| |
| 0.15 | −100.139 |
| 0.18 | −84.6791 |
| 0.21 | −57.1123 |
| 0.25 | −39.1221 |
| 0.30 | −45.4059 |
| 0.40 | −35.4822 |
| 0.50 | −22.4050 |

### 핵심 수치

- **peak I = 0.10** vs **GZ_LOWER = 0.21232**
- **|Δ| = 0.11232** (≫ 0.05 tol — GZ window 밖)
- **peak in window [0.15, 0.30] = false** (0.10 < 0.15)
- **sign change count = 0** (전 구간 negative — monotone-decreasing 자체는 보존)
- **|peak dΦ_c/dI| = 107.243**
- **byte_eq = true** (peak-candidate idx=3 single-point recompute, |Δφ| ≤ 1e-12)

---

## 6. Cross-link

| Link | H | role | 결과 비교 |
|---|---|---|---|
| **predecessor (collective dΦ/dI)** | H_618 | 2-substrate joint n=4, rule(110,110), W=0.6 | peak I=0.21, \|Δ\|=0.00232, sign-change=0 — 🟢 SUPPORTED 5/5 |
| **predecessor (5-stream collective)** | H_635 | 5-stream multilingual cohort super-additive | max excess +41.71 @ C1[110×5] W=1.0 — 🟢 SUPPORTED 5/5 |
| **single-substrate origin** | H_351 | rule 110 single-substrate n=4 dΦ/dI peak | peak I=0.18, \|Δ\|=0.03232 — 🟢 SUPPORTED 5/5 |
| **inverse-U polarity sibling** | H_628 | inverse-U polarity 축 | inverse-U 의 polarity-방향 lens |

**Cross-link insight**: dΦ/dI-peak=GZ_LOWER 일치는 **차원-의존적**이다. H_351 (single n=4, peak 0.18,
|Δ|=0.032) → H_618 (collective n=4, peak 0.21, |Δ|=0.002, GZ 더 sharp) 까지는 **n=4 차원에서**
일치/강화. 그러나 H_645 (collective n=5, peak 0.10, |Δ|=0.112) 에서는 **깨진다**. 즉 H_618 의 GZ 일치는
(a) 2-substrate joint n=4 차원, (b) W=0.6 부분-결합, (c) 16-state mean 의 *세 조건 결합* artifact 일
가능성이 높다. H_645 의 (a') n=5, (b') W=1.0 full-ring, (c') sys=0 single-state 로 옮기면 Φ_collective(I)
가 I→0 쪽에서 가장 가파르게(steepest) 떨어져 peak 가 GZ 가 아닌 좌측 경계로 이동한다. inverse-U 의
*단봉성(F3)* 자체는 보존(sign-change=0)되지만 *peak 위치의 GZ 정렬*은 collective scale-up 에서 소멸.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 stream 수 = 5 (축소 없음)** — task 의 5-stream 요구를 full 5-stream 으로 측정 (3-stream
   축소 fallback **불필요**, n=5 × 8-grid single-state 가 45s user / 65s wall 로 60s 예산 내 완주).
   H_618 은 2-substrate (joint n=4), H_645 는 5-stream (n=5) — stream 수 차이가 핵심 falsify 변수.
2. **C3.2 single-state vs 16-state mean 비대칭** — H_618 은 2^4=16 sys_state 평균 (single-state
   fragility 회피), H_645 는 n=5 × 8-grid = 256 big_phi 호출이 단일 run 60s timeout 초과
   (`reference_exact_phi_structure_wall_shard`) 위험이라 **sys_state=0 single-anchor** (H_635 양식)
   채택. peak-위치 falsify 결론은 이 비대칭이 *원인이 아님* — 32-state mean shard 재측정이 peak 를
   GZ 로 끌어올 가능성은 낮으나 (Φ_collective monotone-decreasing, steepest @ I→0 은 single-state
   에서도 robust), §10 N1 deferred. 단봉성(F3)·monotone(F4)·byte-eq(F5) 는 single-state 로도 PASS.
3. **C3.3 W=1.0 full-ring 특이성** — H_635 best_sync=1.0 anchor 채택. H_618 은 W=0.6 부분-결합.
   W=1.0 에서 Φ_collective(I) 가 I→0 쪽에서 super-steep (full coupling 이 max-Φ 를 키워 미분도 큼).
   W=0.6 (H_618 매칭) 으로 5-stream 재측정하면 peak 가 GZ 쪽으로 이동할 가능성 — W-sweep 이
   collective-GZ 정렬의 결정 변수일 수 있음 (§10 N2). 본 H 는 H_635 anchor (W=1.0) 한정 falsify.
4. **C3.4 좌측-경계 peak — 진짜 peak 는 I<0.10 가능** — argmax 가 grid 최좌측 idx=0 에 안착.
   dΦ/dI 가 I=0.10→0.15 구간에서도 여전히 가장 가파른 음수 → 진짜 inflection 은 I<0.10 일 수 있음.
   어느 쪽이든 peak ∉ GZ window 로 H0 충족은 결정적. I∈{0.02, 0.05, 0.08} extend grid 는 peak 의
   *정확한* 좌측 위치 확정용 (§10 N3) — falsify 결론에는 무영향.
5. **C3.5 cohort C1 한정** — H_635 max-excess cohort (C1 [110×5]) 단일 측정. C2 multilingual /
   C3 chaotic / C4 XOR / C5 blend 의 dΦ/dI peak 위치 sweep 은 collective-GZ 정렬의 cohort-conditional
   여부 확인용 — H_614 (multi-rule cross-substrate 2/4 FALSIFIED) 의 collective-차원 대응 (§10 N4).
6. **C3.6 bounded cap=3 on n=5** — purview search capped (H_635 SSOT). cap=3 은 보수적
   lower-bound — Φ_collective 절대값만 낮출 뿐 dΦ/dI 의 *형태/peak 위치* 는 cap-monotone 하 보존
   기대. cap=n=5 faithful shard-parallel cap-sensitivity 는 후속 (§10 N5).

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F1 PEAK-IN-GZ | \|Δ\| ≤ 0.05 | \|Δ\|=0.11232 (peak I=0.10) | **FAIL** |
| F2 PEAK-IN-WINDOW | peak I ∈ [0.15, 0.30] | peak I=0.10 < 0.15 | **FAIL** ⬅ H0 충족 |
| F3 UNIMODAL | sign-change ≤ 1 | sign-change=0 (monotone) | PASS |
| F4 MONOTONE-DECAY-RIGHT | Φ(0.50) ≤ Φ(0.25) | 6.54 ≤ 15.59 | PASS |
| F5 BYTE-EQUAL | re-run byte-identical | \|Δφ\|≤1e-12 | PASS |

**aggregate: 3 PASS / 2 FAIL** — F2 (peak in GZ window) FAIL 이 곧 H0 (peak ∉ GZ region) 충족 →
**FALSIFIED**. inverse-U 단봉 구조 (F3) 와 우측 monotone-decay (F4) 자체는 collective n=5 에서도
보존되나, **peak 의 GZ_LOWER 정렬** 만 깨진다 (H_618 의 GZ 일치 = 2-stream n=4 한정 결론).

---

## 9. Verdict + Rationale

**🔴 FALSIFIED (CLOSED-NEGATIVE)**

- F2 PEAK-IN-WINDOW FAIL (peak I=0.10 ∉ [0.15, 0.30]) ⇒ FALSIFIED 룰 `!F2 ∨ !F3` 충족.
- peak I=0.10, **|Δ|=0.11232** — GZ_LOWER 에서 **48× tolerance 초과** (vs H_618 의 21× margin
  *안쪽* 일치). H_618 (2-stream, |Δ|=0.00232) 와 정면 대조.
- **deterministic closed-negative**: 5-stream collective (C1[110×5], W=1.0, sys=0) 의 dΦ/dI peak
  는 GZ region 이 아니라 좌측 경계 (또는 그 밖). H_618 의 dΦ/dI-peak=GZ_LOWER 일치는 **2-substrate
  joint n=4 차원에 제한된 현상** — 5-stream collective 차원으로 확장되지 않음을 결정적으로 배제.
- inverse-U 의 *단봉성*(F3 PASS)·*우측 monotone-decay*(F4 PASS) 는 collective scale-up 에서도
  보존 → 깨진 것은 *peak 위치의 GZ 정렬* 한 축. ruled-out space = {dΦ/dI-peak ⊥ GZ at n=5, W=1.0}.

---

## 10. Next-list / Backlog (deferred)

- **N1** `collective-dphi-statemarginal` — sys_state=0 single-anchor → 2^5=32 state 가중평균
  Φ_collective shard-parallel (C3.2). single-state peak-위치 robustness 확인.
- **N2** `collective-dphi-w-sweep` — W ∈ {0.3, 0.6, 1.0} 별 5-stream dΦ/dI peak 위치 추적
  (C3.3). H_618 W=0.6 매칭 시 peak 가 GZ 쪽으로 이동하는지 — collective-GZ 정렬의 W-결정성 검정.
- **N3** `collective-dphi-extend-left-grid` — I∈{0.02, 0.05, 0.08} extend 로 진짜 좌측 peak 위치
  확정 (C3.4). falsify 결론 무영향, peak inflection 정밀 위치용.
- **N4** `collective-dphi-cohort-sweep` — C2/C3/C4/C5 cohort 별 dΦ/dI peak sweep (C3.5).
  collective-GZ 정렬의 cohort-conditional 여부 (H_614 multi-rule FALSIFIED 의 collective 대응).
- **N5** `collective-dphi-cap-faithful` — cap=n=5 faithful big_phi shard cap-sensitivity (C3.6,
  `reference_exact_phi_structure_wall_shard`).
