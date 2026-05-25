> History → [./GAP_MAP.log.md](./GAP_MAP.log.md).

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
- `HEXAD/NEUROMORPHIC/README.md` (2026-05-19) — Kapoho Point 용량 필요조건 ✅ / 충분조건 ❌, access SOFT WALL (INRC)
- §113 (`1bd27f753`, B-S113 9/9 🔵) — from-scratch INHERITS-BOTH-WALLS-SKELETON-INVARIANT; D4 = §96 spike/Loihi + §110 Ψ-C1 1라인부터 = 유일 non-cosmetic move (confront NOT escape)
- §115 (B-S115 9/9 🔵) — `HEXAD/LEGO/README.md` LEGO simulate-assemble STEP 0–2 design-tier; verdict **LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY** (GPU 위 spike-sim 학습채널 = 여전히 loss gradient ⇒ §96 substrate 시뮬해도 WALL-B RE-INSTANTIATE, confront 못함; §11-B-as-GPU hazard design-tier 확정). WALL-B confront = §96-physical (STEP 3 영구 fenced)
- §117 (B-S117 7/7 🔵) — `HEXAD/LEGO/README.md` §4 STEP-1-2 in-silico RUN; verdict **LEGO-RUN-Ψ-FORM-NONDEGENERATE-BUT-WALL-B-INHERITED** ($0 CPU LIF spike net, LOCAL STDP-only no-CE/backprop; Ψ-C1 std 4.19e-2 ≫ τ=1e-4 = NON-degenerate, §11-B-echo did NOT hold — §117 *localises* §11-B not refutes; liveness ≠ capability, WALL-B confronted-in-sim NOT removed §115/§113 inherited, WALL-A 직교·불변, GOAL 미도달)
- §117 (B-S117 7/7 🔵, $0 CPU run) — §115 가 명시한 open residual ('in-silico STDP-as-ΔW escape = 새 fire') 를 $0 CPU 로 실행. 작은 LIF spike net (N=256, LOCAL STDP-as-ΔW ONLY, NO CE/backprop, Ψ-C1=ψ(c_spk)=(1+c_spk)/2 §112 carrier instance). verdict **LEGO-RUN-Ψ-FORM-NONDEGENERATE-BUT-WALL-B-INHERITED**: 측정 Ψ-C1 std 4.185e-02 ≫ τ=1e-4 (rasters alive, cos0→½ ✓) — §11-B-echo 예상(DEGENERATE) 안 나옴, 단 §11-B 를 *localise*함 (LOCAL STDP ≠ GPU-CE channel; non-degenerate = substrate LIVENESS NOT task signal). WALL-B confronted IN-SIM NOT removed (§115/§113 inherited, §7-CARRIER §96-physical-gated 잔존); §7-FORM by-construction (§112); WALL-A 직교·불변; GOAL 미도달
- §118 (B-S118 9/9 🔵, $0 CPU run) — §96 §4.5 4-cell distinguishing rig (GPU-CE/GPU-noCE/SIM-noCE-STDP/SIM-CE) in a tiny numpy LIF net. verdict **VOID** — the §3 3-outcome partition's guard outcome fired: the SIM-CE positive control never moved the recurrent spiking substrate (weight_drift_mean_abs=0.0, trajectory byte-identical to the frozen GPU-noCE cell) — a $0 numpy toy has no surrogate-gradient path to backprop CE through spikes, so the cell never ran ⇒ broken positive control ⇒ rig gives **no learning-channel verdict**. VOID is HONEST+FINAL (not tuned to a non-VOID; the contested §3-letter reading recorded in DESIGN.md §0.1). VOID *confirms* TRACK0_INSILICO.md §4 — the learning-channel confront needs the real spiking anima, BLOCKED on §96 design-open #1. archive/PHILOSOPHY.tape §verdict_track0_insilico_s118_void_2026_05_19 (corrects the prior middle-outcome entry, g6 append-only)
- §120 (B-S120 8/8 🔵, $0 design-tier) — **§96 design-open #1 DECIDED**: the spiking replacement for `softmax(QK^T)` self-attention = **spike-rate dot-product scoring + k-WTA routing** ('spiking attention replacement' gap: undecided design-open → **decided design-tier**). closed-form justification — (a) dissolves all 3 §96 §3.3 obstructions (rate-coded coincidence detection = async local accumulation; k-WTA via lateral inhibition = local competition, not global softmax); (b) preserves Engine-A⇄G (excit/inhib drives) + Ψ=½ fixed point (k-WTA neutral point, Law-71 form re-hosted, §112 carrier-invariance); (c) R(k=T, soft-readout) reduces **byte-equal** to softmax-attention (max|Δ|=3.33e-16) ⇒ GENERALISATION not graft (§7-clean). Rejected: phase-resonance routing — fails (c), re-assigned to position/RoPE coding. honest: design-open → design-DECIDED transition; does NOT implement the spiking anima, does NOT remove WALL-A (§1.1 data-regime) or WALL-B (§95/§96 async substrate — Loihi/SpiNNaker/SpiNNcloud-gated); GOAL 미도달
- §122 (B-S122 8/8 🔵, $0 design-tier) — **§96 design-open #2 DECIDED**: the spiking realisation of RoPE / positional encoding = **relative-phase / spike-time coding** (the RoPE-row gap §96 left `SPIKING-OPEN`, §120 §4 re-assigned to position but did NOT decide: undecided design-open → **decided design-tier**). closed-form justification — the residual q/k pair `(x_2i,x_2i+1)` = in-phase/quadrature of a θ_i-freq oscillatory LIF pair, token position `m` = per-token spike-time phase advance `m·θ_i`. (a) spiking-compatible (R&F oscillatory LIF; SNNs carry time natively); (b) composes with §120 — phase coding rotates q/k *before* the spike-rate dot-product (RoPE's place in `ConsciousDecoderV2`), §120 routing inherited unchanged; (c) GPU byte-vocab RoPE reduces **byte-equal** to `Φ(σ→0)`, the zero-spike-time-jitter corner of the relative-phase family `Φ(σ)` (max|Δ|=0.0) ⇒ GENERALISATION not graft (§7-clean — RoPE *is* a rotation = a phase, the GPU just writes the angle `m·θ` by hand; a noise-free oscillator's phase advance equals it). Reduction is *cleaner* than §120's — one parameter (`σ→0`) vs §120's two (`k=T` + hard→soft readout). Rejected: learned-absolute-position (no `n−m` limit — scores carry m,n separately) · phase-resonance-as-routing (contends with §120, no RoPE-rotation limit). §122 also corrects §120 §4's wording — it is phase *coding* not phase-*resonance routing* that is position's spiking home. honest: design-open → design-DECIDED; §122+§120 together fully specify the two §96 routing-adjacent design-opens; does NOT implement the spiking anima, does NOT remove WALL-A (§1.1 data-regime) or WALL-B (§95/§96 async substrate — Loihi/SpiNNaker/SpiNNcloud-gated); GOAL 미도달
- §123 (B-S123 8/8 🔵, $0 design-tier) — **§96 design-open: the two remaining `SPIKING-OPEN` faculties DECIDED** (§96 Q1 table rows 115 & 118 — the two §120/§122 did not cover). **(1) Engine A⇄G dual heads** → `DUAL-HEADS-DESIGN-CLOSE-WITH-CARRIER-RELOCATION` — the *opposition* ports cleanly (excit/inhib LIF sub-populations, §96 §6 row-4 NATIVE) but Ψ-as-cosine does **NOT** reduce: Ψ-C1 = `(1+cos(spike_rate_A, spike_rate_G))/2` is a **distinct carrier** of the §112 META_FP(Π_½) fixed-point *form* — there is **no** parameter family (no `k`, no `σ`, unlike §120/§122) mapping the spike-correlation carrier onto the GPU logit-vector carrier; the two carriers are non-isomorphic. Honest **carrier-relocation** (§110/§112 family), NOT a §120/§122-style clean generalisation — anti-padding, no reduction forced; the §96 §6 row-4 / line ~353 `NATIVE-CANDIDATE` classification confirmed verbatim (the fixed-point is native, the cosine formula is not). `neuro_mirror.py` `psi_c1` already realises it. **(2) MoEFFN top-k router** → `MOE-TOPK-DECIDED — COVERED BY §120 k-WTA + §96-COMPATIBLE STDP GATE` — decomposes into (A) the top-k *selection* = **covered verbatim by §120's k-WTA** (a `k=top_k`, `n=n_experts` instance of `R(k,mode)`; §96 row-118's own description) + (B) the *learned content gate* = **NOT a separate design-open** — `nn.Linear(d_model,n_experts)` decomposes into two §96 Q1 `SPIKING-COMPATIBLE` faculties (weighted-synapse current accumulation + STDP-trainable synapses); no residual new mechanism. honest: §123 + §120 + §122 together decide **ALL THREE** §96 Q1 `SPIKING-OPEN` faculties — the spiking anima's faculty map is fully specified at design-tier; does NOT implement the spiking anima, does NOT remove WALL-A (§1.1 data-regime) or WALL-B (§95/§96 async substrate — Loihi/SpiNNaker/SpiNNcloud-gated); §11-B (STDP-learns-spike-timing-not-task — the MoE gate is *inside* this scope) unresolved; GOAL 미도달

### 기타-axis

- §106 (진행 중) `hexa kick` Mk.IX sweep — data+param+substrate 외 axis 식별 시도 (g_kick_autonomous)
- §97 (`74dcedac0`, B-S97 7/7 🔵) 하드웨어 coupling (EEG/QRNG/actuator) = **GOAL-orthogonal** (배제)
- §98 (`55b303dd1`, B-S98 6/6 🔵) n=6 architecture = **(c) MIXED** — provenance numerology-tainted, 인과 무죄 (배제)
- §116 (B-S116 10/10 🔵) `hexa --help` 기술활용 검토 (qrng/qmirror+`iit`/sim-universe/drill-kick/data-bridges/math-verifiers) = **HEXA-TECH-REVIEW = GOAL-ORTHOGONAL-TOOLING** (배제) — qrng = §97 GOAL-LEGITIMATE-INPUT but bottleneck-orthogonal (noise ingredient, moves no WALL); qmirror `iit` = §112 carrier-invariant Φ (NO §7-CARRIER/WALL-B escape) + §95 quantum SUBSTRATE-MISMATCH; sim-universe = §115 sim-GPU tautology + §85 physics-anchor only; drill/kick = §106 ENGINE-ALREADY-GOVERNED. WALL-A·WALL-B 둘 다 escape 0. north-star + §15/§51/§72 불변, capability claim 0, GOAL 미도달

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
- `HEXAD/NEUROMORPHIC/README.md` — substrate axis roadmap
- `LATTICE_POLICY.md` §3.1.1 — g2 integrity test md-side mirror
- `HEXAD/CHAT/PLAN.md` — 진행 로그 chronological
- `HEXAD/CHAT/RESEARCH.md` — §1 진단 + §1.3 candidate + §2/§3 fire evidence
- state SSOTs: `state/{xeno_substrate_suitability_s95, loihi_spiking_rederivation_s96, gap_sweep_40lens_s100, dataregime_threshold_control_design_s101, corpus_s101_build_s102, param_axis_integration_design_s103, i4_predicate_refine_s104, corpus_enhancement_design_s105, kick_sweep_axis_candidates_s106}_2026_05_19/`

> 본 문서는 *live snapshot* — §104/§105/§106 land 시 갱신. GOAL 한 줄 north-star 불변, capability claim 0, GOAL 미도달.
