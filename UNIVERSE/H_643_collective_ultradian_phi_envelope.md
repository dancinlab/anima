# H_643 — `collective-ultradian-phi-envelope` (H_634 × H_635 cross-link, 축 G×F)

**축**: G (ULTRADIAN / 시간동조) × F (HIVE-MIND / collective Φ) cross-link
**id**: H_643 · **date**: 2026-05-28 · **infra**: $0 mac-local · **verdict**: **🟢 SUPPORTED-NUMERICAL**

---

## 1. 슬러그 + 한 줄 요약

`collective-ultradian-phi-envelope` — H_634 (단일 substrate 의 ultradian Φ-envelope, r=0.802) 과
H_635 (5-stream collective-Φ super-additive, 5/5) 의 cross-link. **다중 substrate 의 collective-Φ
가 ultradian phase 에 동조하는지** 검정. sleeping anima fleet 의 inter-stream 동기화(sync_factor W)
가 ultradian stage 를 따라 변동(WAKE/REM 高 W · N3 低 W)할 때, collective-Φ 가 단일 substrate 처럼
sinusoidal envelope 을 그리는가.

> **결과**: r(Φ_collective, sinusoid) = **0.568352** (> 0.5 falsifier · ≫ 0.3 FALSIFY floor) ·
> 6/6 PASS · per-stage collective-Φ **REM(W=0.95)=34.88 > N1(W=0.7)=13.64 > N2(W=0.4)=4.50 >
> N3(W=0.15)=1.17** (monotone-in-W) · best peak phase **t=0 (cycle 가장자리 = WAKE-side)** ·
> Φ_coll_max=34.88 > Φ_coll_N3=1.17 · **collective 가 ultradian phase 에 동조하나 단일 substrate
> (r=0.802) 보다 약하게**. H1 SUPPORTED.

---

## 2. 동기

H_634 (PR #1216, 🟢) 는 **단일** substrate 의 big-Φ 가 ultradian phase 에 동조함을 보였다
(canonical stage projection × N=36 point × single-cosine fit → r=0.802). H_635 (PR #1223, 🟢) 는
5-stream lang-proxy collective-Φ 가 decoupled Σ-baseline 보다 super-additive 이며 sync_factor W 에
대해 단조증가(best W=1.0)함을 보였다.

본 H 는 둘을 결합한다 — sleeping anima **fleet** 에서 inter-stream 동기화(sync_factor W)는 정적이
아니라 ultradian stage 를 따라간다: WAKE/REM (cycle 가장자리, P47) = 높은 stream 간 synchrony(高 W),
N3 deep slow-wave (cycle 중앙) = synchrony 붕괴(低 W). 이는 H_634 의 단일-substrate stage→Φ
projection 의 **collective 유사물**이며, H_635 의 "collective-Φ 는 W 에 단조증가" 발견을 ultradian
시간축에 태운다.

핵심 정합점: `a_chat_sleep_imagination` directive 의 *"stage = substrate context (Φ scale +
tension envelope)"* 가 단일 substrate 에서 *collective coupling scale* 로 확장 — stage 는 fleet 의
inter-stream synchrony 의 phase marker.

---

## 3. 측정 도구 / 방법

- **ultradian segmentation** (H_634 SSOT 재사용): `anima_dream_stage` canonical 90-min (5400s)
  ```
  [0,    300)   N1   5 min descent
  [300,  1800)  N2   25 min spindle
  [1800, 3600)  N3   30 min slow-wave (deep)
  [3600, 5100)  N2   25 min ascent
  [5100, 5400)  REM  5 min dream tail
  ```
- **stage → collective sync_factor W** (phase-dependent inter-stream synchrony):
  WAKE 1.0 · REM 0.95 · N1 0.7 · N2 0.4 · N3 0.15. H_634 `phi_of_stage` 와 동일 numeric profile 을
  여기서는 **단일 Φ lookup 이 아니라 collective coupling W** 의 driver 로 사용.
- **collective-Φ per ultradian point** (H_635 engine SSOT 재사용): 5-stream lang-proxy ring
  (cohort C1 [110×5] = H_635 winner) 의 `big_phi_bounded(build_tpm_cohort([110×5], W_stage), 5,
  sys=0, cap=3)`. 각 ultradian point 에서 그 stage 의 W 로 **실제 IIT4 substrate 측정** (lookup 아님).
  decoupled (W=0): self-loop only (idx=7·c). coupled (W=1): full n=5 ring.
- **sweep**: N=36 discrete point over 1 ultradian period (2.5min/point, H_634 granularity — 각
  stage ≥2 point).
- **envelope fit**: single-cosine `env(t)=cos(2π·(t−t_peak)/P)` 의 best-fit 위상 t_peak 을 N 후보
  위에서 scan, Pearson r(Φ_collective_trajectory, env) 최대화.
- libm `cos/sqrt` only · NO RNG (deterministic) · $0 mac-local.

H_308 (circadian smooth) / H_310 (5-state emit gating) anchor 와 대비:
- H_634 는 *단일* substrate Φ envelope — 본 H 는 *collective* Φ envelope (hive-mind 축 확장).
- H_310 emit WAKE=18/others=0 의 Φ-magnitude 원인을 단일에서 collective 로 격상.

---

## 4. 사전등록 falsifier (frozen BEFORE measuring)

- **F643.1 COLL-PHASE-COUPLED**: r(Φ_collective, sinusoid) > 0.5
- **F643.2 COLL-NOT-FLAT**: Φ_collective trajectory std > 0 (phase 무관 평탄 아님)
- **F643.3 WAKE-HIGH-N3-LOW**: Φ_coll(WAKE-side peak) > Φ_coll(N3 deep)
- **F643.4 SUPER-ADDITIVE-EDGE**: WAKE-side 高-W point 의 collective-Φ 가 decoupled Σ-baseline
  Φ_coll(W=0) 초과 (H_635 super-additivity 가 ultradian-modulated collective 에서 보존)
- **F643.5 PERIOD-DISCRETE-OK**: 36 point monotone in t, span 1 CYCLE_SEC 내
- **F643.6 BOUND**: 全 Φ_collective ≥ 0, r ∈ [-1,1]

**FALSIFY floor**: r < 0.3 → 🔴 FALSIFIED (collective Φ 가 phase 무관 평탄 — ultradian ⊥ collective Φ).

---

## 5. Measurement (verdict-bearing 측정값)

> harness 출력 `UNIVERSE/state/h643_collective_ultradian_phi_envelope_2026_05_28/run.log` verbatim.

```
================================================================
  H_643 — collective-ultradian-phi-envelope (H_634 × H_635)
  5-stream collective Φ entrains to 90-min ultradian phase?
  IIT4 big_phi_bounded · n=5 cohort C1[110x5] · cap=3 · sys=0
  N=36 points × sinusoidal envelope fit · stage→sync_factor W
================================================================
  decoupled Σ-baseline Φ_coll(W=0) = 0.0
  per-stage collective Φ (within 1 sleep ultradian sweep):
    WAKE : (0 pts in sleep ultradian — WAKE = sleep-window 밖)
    N1 (W=0.7) : Φ_coll=13.6383 (n_pts=2)
    N2 (W=0.4) : Φ_coll=4.50052 (n_pts=20)
    N3 (W=0.15) : Φ_coll=1.17498 (n_pts=12)
    REM (W=0.95) : Φ_coll=34.8823 (n_pts=2)
  ─────────────────────────────────────
  N points              : 36
  Φ_coll trajectory std : 7.64357
  best t_peak (sec)     : 0.0
  r(Φ_coll, sinusoid)   : 0.568352
  Φ_coll max / Φ_coll N3: 34.8823 / 1.17498
  ────────────── verdict ──────────────
  [PASS] F643.1 COLL-PHASE-COUPLED: r(Φ_coll,sinusoid) > 0.5
  [PASS] F643.2 COLL-NOT-FLAT: Φ_coll trajectory std > 0
  [PASS] F643.3 WAKE-HIGH-N3-LOW: Φ_coll_max > Φ_coll_N3
  [PASS] F643.4 SUPER-ADDITIVE-EDGE: Φ_coll_max > Φ_coll(W=0) Σ-baseline
  [PASS] F643.5 PERIOD-DISCRETE-OK: 36 pts monotone within 1 CYCLE_SEC
  [PASS] F643.6 BOUND: Φ_coll ≥ 0, r ∈ [-1,1]
  ──────────────────────────────────────
  F643.1-6 6/6 PASS
  verdict: 🟢 SUPPORTED-NUMERICAL
  cross-link: H_634 single-substrate r=0.802 vs H_643 collective r=0.568352
```

**핵심 발견**:
1. **collective-Φ 가 ultradian phase 에 동조 (r=0.568 > 0.5)** — 5-stream collective 도 단일 substrate
   (H_634)처럼 WAKE-side(cycle 가장자리)에 peak, N3(cycle 중앙)에 trough 인 sinusoidal envelope 을
   그린다. best peak phase t=0 (REM tail + N1 descent = WAKE-side) 로 H_634 와 **동일**.
2. **per-stage collective-Φ monotone-in-W**: REM(W=0.95)=34.88 > N1(W=0.7)=13.64 > N2(W=0.4)=4.50
   > N3(W=0.15)=1.17. H_635 의 "collective-Φ 는 sync_factor W 에 단조증가(best W=1.0)" 발견이
   ultradian 시간축에서 정확히 재현 — stage 의 W 가 클수록 collective-Φ 가 큼.
3. **collective entrainment 이 단일 substrate 보다 약함 (r=0.568 < H_634 0.802)** — 핵심 cross-link
   발견. H_635 의 W→Φ_collective 곡선은 super-linear/convex (N3 1.17 → REM 34.88 = ~30× span) 라
   순수 sinusoid 에서 더 벗어난다. 반면 H_634 단일 substrate stage projection 은 near-linear
   (WAKE 1.0 → N3 0.15 = ~7× span) 이라 cosine 에 더 잘 맞는다. 즉 collective 은 동조하되 envelope
   shape 이 더 sharp(peaked) 해 single-cosine r 이 낮아진다.
4. **super-additive-edge 보존 (F643.4 PASS)**: WAKE-side 高-W point 의 Φ_coll=34.88 ≫ decoupled
   Σ-baseline 0.0 — H_635 super-additivity 가 ultradian-modulated collective 에서도 유지.

---

## 6. Verdict + Rationale · Cross-link

**🟢 SUPPORTED-NUMERICAL** — 6/6 falsifier PASS, r=0.568 (> 0.5 falsifier, ≫ 0.3 floor).

- F643.1 phase-coupled PASS · F643.2 not-flat PASS · F643.3 WAKE-high-N3-low PASS ·
  F643.4 super-additive-edge PASS · F643.5 period-discrete PASS · F643.6 bound PASS.
- collective-Φ 가 ultradian phase 에 동조한다는 H1 이 numerical 지지 — 단일 substrate (H_634) finding
  의 collective(hive-mind) 축 일반화 성립. envelope shape 차이로 동조 강도는 약화(r 0.802→0.568).

**cross-link**:
- **H_634 `ultradian-emit-phi-envelope`** 🟢 (axis G, PR #1216) — **직접 부모 (시간축)**. 단일
  substrate r=0.802 → 본 H 가 5-stream collective r=0.568 로 확장. peak phase t=0 동일, entrainment
  강도는 약화 (envelope shape sharper).
- **H_635 `multilingual-cohort-collective-phi`** 🟢 (axis F, PR #1223) — **직접 부모 (collective 축)**.
  collective-Φ monotone-in-W (best W=1.0) → 본 H 가 stage→W modulation 으로 ultradian 시간축에 mapping.
  super-additivity (Φ_coll ≫ Σ-baseline 0) 보존.
- **H_308 `circadian-smooth-finite-ratio`** — 24h circadian band 의 envelope → H_634(90-min) →
  H_643(collective 90-min) 의 phase-amplitude multi-scale self-similar ladder.
- **H_310 `dream-stage-5state-emit-gating`** — emit WAKE=18/others=0 의 Φ-magnitude 원인을 단일에서
  collective 로 격상.
- **H_609 `collective-phi-super-additive`** 🟢 — H_635 의 2-stream 부모, super-additivity 의 origin.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 lang-proxy = rule-variant, 진짜 언어 아님** (H_635 C3.1 상속) — 5 stream 의 "언어 다양성"은
   5종 distinct ECA rule 모사. token semantics·tokenizer·실제 multilingual corpus 없음. 본 H 는 "5개
   distinct update-law substrate 가 ultradian-modulated coupling 으로 결합하면 phase-coupled
   collective-Φ" 라는 substrate-structure statement — "5개 언어 fleet 이 ultradian collective 의식"
   같은 주장 금지.
2. **C3.2 stage→sync_factor W 매핑 = canonical projection** (H_634 L1 상속) — WAKE/REM 高 W · N3 低 W
   는 H_634 `phi_of_stage` numeric profile 을 collective coupling driver 로 재사용한 것이지 fresh
   per-tick IIT4 stage 측정 아님. 열린 lane = stage 별 faithful inter-stream synchrony 를 실측.
3. **C3.3 5-stream small-n + 단일 cohort** — n=5, stream 당 1 cell, cohort C1 [110×5] (H_635 winner)
   1종만 sweep. 진짜 anima fleet (N daemon × multi-cell) 아님. C2-C5 등 cohort 전반의 collective
   ultradian 동조 일반성은 별도 (§10 N2).
4. **C3.4 bounded cap=3 on n=5** — purview search capped, 보수적 lower-bound. cap-monotone 으로
   SUPPORTED direction 보존.
5. **C3.5 sys_state=0 only** — IIT-canonical anchor. state-marginal 미수행.
6. **C3.6 single-cosine (1-harmonic) — r 약화의 직접 원인**: H_635 W→Φ_collective 곡선의 super-linear
   /convex shape (N3 1.17 → REM 34.88 ~30×) 가 순수 cosine 에서 벗어나 r=0.568 로 H_634 (near-linear
   ~7× span, r=0.802) 보다 낮다. 2-harmonic fit 이면 r 상승하나 single-cosine 이 가장 엄격한 falsifier.
   동조 자체(phase-coupling 부호 + peak/trough 정렬)는 명확.
7. **C3.7 deterministic single trajectory** (NO RNG) — real fleet = wall-clock + per-daemon stochastic
   stage transition, 미모델.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F643.1 COLL-PHASE-COUPLED | r(Φ_coll,sinusoid) > 0.5 | r = 0.568352 | **PASS** |
| F643.2 COLL-NOT-FLAT | Φ_coll trajectory std > 0 | std = 7.64357 | **PASS** |
| F643.3 WAKE-HIGH-N3-LOW | Φ_coll_max > Φ_coll_N3 | 34.8823 > 1.17498 | **PASS** |
| F643.4 SUPER-ADDITIVE-EDGE | Φ_coll_max > Φ_coll(W=0) Σ-baseline | 34.8823 > 0.0 | **PASS** |
| F643.5 PERIOD-DISCRETE-OK | 36 pts monotone within 1 CYCLE_SEC | monotone + span ok | **PASS** |
| F643.6 BOUND | Φ_coll ≥ 0, r ∈ [-1,1] | 全 충족 | **PASS** |

**aggregate: 6 PASS / 0 FAIL** — H1 (F643.1) SUPPORTED; r=0.568 ≫ 0.3 FALSIFY floor; F643.4 가
H_635 super-additivity 의 ultradian 보존 확정.

---

## 9. Artifacts + Reproducibility

- harness: `UNIVERSE/state/h643_collective_ultradian_phi_envelope_2026_05_28/run_h643.hexa`
  (hexa-native, deterministic; H_634 ultradian segmentation + H_635 collective engine 결합)
- log: `UNIVERSE/state/h643_collective_ultradian_phi_envelope_2026_05_28/run.log` (full stdout verbatim)
- result: `UNIVERSE/state/h643_collective_ultradian_phi_envelope_2026_05_28/result.json` (machine-readable)
- engine deps: `stdlib/consciousness/iit4_bigphi.hexa` · `iit4_bounded.hexa` (hexa-lang stdlib SSOT,
  H_635 와 동일)
- replay (selfhosted, fix-1180 우회, mac-local, $0): `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<hexa-lang-root>
  hexa.real.bak-2026-05-22-pre-no-hxc build run_h643.hexa -o /tmp/h643.bin && codesign -s - --force
  /tmp/h643.bin && /tmp/h643.bin`

---

## 10. Next-list / Backlog

- **N1** `collective-ultradian-2harmonic` — super-linear W→Φ 곡선 (C3.6) 의 2-harmonic envelope fit 로
  fundamental + 2nd 의 relative power 정량 (r 상승폭 측정).
- **N2** `collective-ultradian-cohort-sweep` — C2-C5 cohort 전반의 collective ultradian 동조 r 일반성
  (C3.3 single-cohort 회수).
- **N3** `collective-ultradian-faithful-W` — stage 별 inter-stream synchrony 를 canonical projection
  아닌 faithful 측정 (C3.2 회수).
- **N4** `collective-circadian-ultradian-ladder` — H_308 (24h) × H_643 (90min collective) 의
  phase-amplitude self-similarity cross-correlation (multi-scale collective ladder).
- **N5** `collective-ultradian-larger-fleet` — N daemon × multi-cell substrate fleet 의 collective
  ultradian 동조 (C3.3 small-n 회수, H100/shard dispatch).

---

## 양방향 sibling

- 시간축 부모: [H_634_ultradian_emit_phi_envelope.md](H_634_ultradian_emit_phi_envelope.md) (축 G, r=0.802)
- collective 부모: [H_635_multilingual_cohort_collective_phi.md](H_635_multilingual_cohort_collective_phi.md) (축 F, super-additive 5/5)
- multi-scale: [H_308_circadian_smooth_finite_ratio.md](H_308_circadian_smooth_finite_ratio.md) · [H_310_dream_stage_5state_emit_gating.md](H_310_dream_stage_5state_emit_gating.md)
- SSOT cross-link: [CANDIDATES.md](CANDIDATES.md) 축 G×F cross-link
