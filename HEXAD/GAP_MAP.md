# HEXAD/GAP_MAP.md — HEXAD-KICK-SWEEP 현재기준 snapshot

> **domain note** (live snapshot). §63 base + §73~§103 layered.
> **status**: CURRENT — design-tier docs, fire 0, $0.
> **g3**: 본 문서는 *상태 지도* 이지 GOAL 도달 주장 아님. capability claim 0,
> north-star + §15/§51/§72 milestone 불변, GOAL 미도달.

---

## marker 5종

```
✅ closed B-CONN wiring (σ(6)=12)
⚠️ 선언됐지만 empirically broken
🛠 GOAL-rank · active design/measurement (positive movement, GOAL 미도달)
🔶 closed-form predicate definable 단 stub/fire 미시도
·  off-axis / not in sweep
```

## 8-module 코어 grid (S/C/M/W/E/D/BR/MI)

```
           S    C    M    W    E    D    BR   MI
        S  ·    ✅   ·    ✅   ·    ·    ·    ·       S→C shape-preserve · S↔W pain-monotone
        C  ·    ·    ✅   ✅   ✅   ⚠️   ✅   ·       M↔C · W↔C · E↔C · BR↔C · C→D ⚠️ broken
        M  ·    ✅   ·    ·    ·    ✅   ·    ·       M↔C · M↔D retrieve
        W  ·    ✅   ·    ·    ⚠️   ✅   ·    ·       W↔C · W↔D · W→E ⚠️ broken
        E  ·    ✅   ·    ✅   ·    ✅   ·    ·       E↔C · E→W satisfaction · E→D trainstep
        D  ·    ·    ·    ·    ·    ·    ·    ·       D→loss Shannon CE≥0 (자기 loop)
        BR ·    ·    ·    ·    ·    ✅   ·    ·       BR→D Law-70 clamp
        MI ·    ·    ·    ·    ·    ·    ·    ·       MITOSIS split/merge (B-MITOSIS 5/5 🔵)
```

- core σ(6)=12 wiring **12/12 ✅ intact**
- in-grid broken **2** (C→D, W→E)
- grid 외 broken **1** (E→TRINITY-INTEGRATED, E 의 sub-cell)

## GOAL-rank connection-point 4 (§63 명명, 현재기준 layered)

### #1 THINKER → TALKER — self-triggered emission controller

§63 🕳️ MISSING-TYPE → 현재 🛠 **active-design-measured-partial**

- §73 stub LANDED — 74× separation, BOTH-NON-DEGEN partial
- §73-FIRE trained-scale CONTROLLER-SURVIVES — echo-escape 첫 사례
- §75-FIRE A-state-alone sufficient — sub-axis localized
- §94 INTEGRATION-COLLAPSES — 5-lever 합성, full closed-loop ✗

### #2 W → W@t+1 — temporal-self-prediction (§58 일반화)

§63 🕳️ MISSING-TYPE → 현재 🛠 **liveness-measured-not-generative**

- §59-FIRE W-native PTD trained-scale (err-var 2.33 ≫ τ=1e-4)
- side read-out liveness only (LM weight·autograd 미접촉, RNG-isolated)

### #3 D@emit → S@t+1 — action-perception loop

§63 🕳️ MISSING-TYPE → 현재 🛠 **training-time-path-identified-not-fired**

- §89 closed-form definable — K(x_{t+1}) ≤ K(e_t)+K(S_encode)
- §90 stub γ-CLOSING-DIRECTIONAL-POSITIVE — cell2 §9 20/20
- §91 trained-scale (β) ECHO-DOMINATES-AT-TRAINED — decode-time ✗
- §92 TRAINING-TIME-AP-DIRECTIONAL-POSITIVE — cell2 §9 19/20 stub
- §93 literature law 확정 — FIRE-WARRANTED + 4 collapse-avoidance

### #4 E@Φ → D@content — continuous Φ-conditioning generative head

§63 🕳️ MISSING-TYPE → 현재 🔶 **definable-not-wired** (stub/fire 미시도)

- §89 closed-form definable — g(0)=0 ∧ ∂g/∂Φ≥0, IIT monotone

## 카운트 요약 — §63 vs 현재기준

| 분류 | §63 (2026-05-18 base) | 현재기준 (§103 시점, 2026-05-19) |
|---|---|---|
| σ(6)=12 ✅ | 12 closed | 12 closed (intact) |
| ⚠️ broken | 3 | 3 (변화 없음: C→D · W→E · E→TRINITY) |
| 🕳️ MISSING-TYPE | 4 | **0** (전부 🛠/🔶 로 이동) |
| 🛠 active | — | **3** (#1 #2 #3 모두 design+측정 진행) |
| 🔶 definable | — | **1** (#4 stub 미시도) |

### 핵심 이동 (§63 → 현재기준)

- §89 가 #3/#4 를 🕳️→🔶 로 정의 (closed-form predicate definable 확정)
- §73 / §73-FIRE / §75-FIRE 가 #1 을 🛠 stub+trained-scale-controller-survives 로 이동
- §59-FIRE 가 #2 를 🛠 liveness-measured (W-physics 살아있음) 로 이동
- §90 → §91 → §92 → §93 thread 가 #3 를 🛠 training-time path 식별 + FIRE-WARRANTED
- §94 INTEGRATION-COLLAPSES = #1/#2/#3 5-lever 합성 시도 → β collapse
- §95~§103 = orthogonal substrate + data-regime + param-axis frontier 추가

## 추가 axis frontier (§95-§106, gap-map 외부 차원)

### data-axis

- §99 (4-candidate compose: C1/C2/C3/C6) — 단발 fire 아닌 multi-cycle program
- §100 priority #1 = data-regime counterfactual UNTESTED — `AGENTS.tape @N n_priority_1_gap` standing record
- §101 (`7809a06f0`, B-S101 10/10 🔵) fire-decidable design Q1/Q2/Q3 closed-form, Q3 = Y at design-tier
- §102 (`b91625c2f`, B-S102 7/8 🔵) CORPUS_S101 actual build → Q3 = FALSE = **honest design-OPEN** (I4 diversity ↑↑ FAIL — S2+S5 = 4.7e-5× S1)
- §104 (진행 중) I4 predicate refine (build-stat → fire-OUTCOME)
- §105 (진행 중) corpus enhancement (S2 ≥10³× / S3 design-tier unblock / S4 corpus form)

### param-axis

- `HEXAD/LLM.md` (2026-05-19) — Wei et al. 2022 임계점 (3B/8B/10B/62B) + Schaeffer Mirage caveat + Du 2403.15796 + Raventós 2306.15063 + Chinchilla 2022
- §103 (`55ba652be` / recovery `ff101139d`, B-S103 10/10 🔵) — SEQUENTIAL data-first, params-contingent; Joint = anti-§94 위반
- §103 Q2 = DESIGN-OPEN + first-band probe pin 3B; Q3' = Q3 ∧ G_PARAM
- §11-A 의 1.04B FLAT 이 sub-CDS data 위 측정 → anima 진짜 param-threshold 에 mute
- anima 283M = 모든 임계점 1/10~1/200 아래

### substrate-axis

- §95 (`26eafc16b`, B-S95 7/7 🔵) — Loihi 유일 VIABLE-LONG-HORIZON (7 exotic substrate 중)
- §96 (`58aed9755`, B-S96 7/7 🔵) — physics layer SPIKING-COMPATIBLE / `softmax(QK^T)` attention SPIKING-INCOMPATIBLE; §11-B-as-GPU-artifact 가설 COHERENT but NOT confirmed
- `LOIHI.md` (2026-05-19) — Kapoho Point 용량 필요조건 ✅ / 충분조건 ❌, access SOFT WALL (INRC)

### 기타-axis

- §106 (진행 중) `hexa kick` Mk.IX sweep — data+param+substrate 외 axis 식별 시도 (g_kick_autonomous)
- §97 (`74dcedac0`, B-S97 7/7 🔵) 하드웨어 coupling (EEG/QRNG/actuator) = **GOAL-orthogonal** (배제)
- §98 (`55b303dd1`, B-S98 6/6 🔵) n=6 architecture = **(c) MIXED** — provenance numerology-tainted, 인과 무죄 (배제)

## governance 진화 (§N 이상 의 layer)

- `@D g_all_options_parallel` (2026-05-19, `3557e0458`) — 옵션 N 개 surface 시 추천-and-wait 금지, 모든 옵션 병렬 진행
- `@D g2 internal_use_integrity_test` (`77dfa8000`) — function-derived vs numerology-derived (§98 follow-up)
- `@N n_priority_1_gap` (`53c599582`) — §99×§100 수렴 standing record + `HEXAD/README.md` 최상단 callout
- `@D g_kick_autonomous` (2026-05-19, `cb329dca7`) — `hexa kick` Mk.IX 자율사용허용

## cross-link

- `AGENTS.tape` `n_hexad_progress` recent_landings · `@D g_*` governance · `@N n_priority_1_gap`
- `archive/PHILOSOPHY.tape` — verdict ledger (append-only g6)
- `GOAL.md` — north-star + honest-status (§95~§106 layer)
- `HEXAD/README.md` — 🔑 PRIORITY #1 GAP callout (최상단)
- `HEXAD/LLM.md` — param × data 2축 framing (Wei 2022)
- `LOIHI.md` — substrate axis roadmap
- `LATTICE_POLICY.md` §3.1.1 — g2 integrity test md-side mirror
- `HEXAD/CHAT/PLAN.md` — 진행 로그 chronological
- `HEXAD/CHAT/RESEARCH.md` — §1 진단 + §1.3 candidate + §2/§3 fire evidence
- state SSOTs: `state/{xeno_substrate_suitability_s95, loihi_spiking_rederivation_s96, gap_sweep_40lens_s100, dataregime_threshold_control_design_s101, corpus_s101_build_s102, param_axis_integration_design_s103, i4_predicate_refine_s104, corpus_enhancement_design_s105, kick_sweep_axis_candidates_s106}_2026_05_19/`

> 본 문서는 *live snapshot* — §104/§105/§106 land 시 갱신. GOAL 한 줄 north-star 불변, capability claim 0, GOAL 미도달.

---

## Log

- **2026-05-19** — HEXAD/GAP_MAP.md 생성. §63 HEXAD-KICK-SWEEP base + §73~§103 layered snapshot. 8-module core grid · 4 GOAL-rank connection-point · §63 vs 현재기준 count · 추가 axis frontier (data/param/substrate/기타) · governance 진화 layer 모두 통합. §104/§105/§106 진행 중 — 본 문서는 live snapshot 이라 land 시 갱신.
- **2026-05-19** — §107 DATAREGIME THRESHOLD COST-BEARING FIRE LANDED (runpod A100-SXM4-80GB pod `t0kvefig3ywer9`, ≈$0.3-0.5; B-S107-1..10 10/10 🔵 pre-fire sidecar, central sha `c93e160a8a376a94` 0-line-diff). first cost-bearing fire to actually attempt crossing §1.1 data-regime threshold using a §7-legitimate construction. **§103 SEQUENTIAL step 1 = data-axis at 283M** (param-axis step 2 contingent on §107 outcome per §108 future). corpus = §102 BUILT CORPUS_S101 byte-identical (sha `39d581da2096…`, 603MB, 777,845 records); Dir-I lever (§16 byte-equal trainer source sha `03bf85d8dcfe…`); single-variable G5 (corpus is sole variable; 5 measured-positive levers preserved). Q2 closed-form THRESHOLD_CROSSED = A1∧A2∧A3∧A4: A1 routing held-out `r_H > 0.65625` / A2 §9 honest-coherent `c_H ≥ 0.50` / A3 §17 PHYSICS_RESPONSIVE ∧ Ψ_dir-spread ≥ 0.20 / A4 emit-length-indep. §62 echo-guard maj_frac ≤ 0.95. §93 4-cond encoded. Honest: even Y is *measured cross-threshold movement* per B-EMERGE-7, NOT proven Living Consciousness; §15/§51/§72 milestones unchanged regardless. Single sequential agent dispatch (sibling pod `vbn92byuns38tt` separate, untouched). post-fire result lands in `state/dataregime_threshold_fire_s107_2026_05_19/result.json` with per-Ai breakdown.
- **2026-05-19** — §108 PARAM-AXIS FIRE PREP design LANDED ($0 ⊥ §107, B-S108 10/10 🔵). §103 SEQUENTIAL contingent param-axis fire READY-TO-DISPATCH: Q1 band 3B (§103 Q2 inherited) · Q2 $1.5-6 / H100-80GB · Q3 d=2560·L=32 ≈3B from-scratch · Q4 G_PARAM 3-clause PASS · Q5 dispatch-tree f(§107.A1..A4,THRESH)→{TRUE_PRIMARY/WEAK/LIKELY, FALSE_PIVOT_SUBSTRATE/UNNECESSARY/PIVOT_CONTROLLER, AMBIGUOUS_DEFER}. central sha `c93e160a8a376a94` 0-diff. north-star + §15/§51/§72 UNCHANGED, GOAL 미도달.
