# Strategic — CLM CP2 pivot ETA (ALM block 후 출발 시 소요 시간 + 비용)

> **ts**: 2026-05-01
> **agent**: CLM CP2 pivot ETA strategic analysis
> **trigger**: 사용자 질문 "ALM 이 자꾸 block 되니까, CLM CP2 는 혹시 지금부터 출발하면 얼마나 걸릴까?"
> **directive context**: AGI tier abandoned 2026-05-01 (사용자 directive); CP2 only.
> **race isolation**: 본 문서 + `state/strategic_clm_cp2_pivot_eta_2026_05_01/{manifest,phase_matrix,comparison_alm_revival}.json` 만 작성. `anima/config/consciousness_laws.json`, `anima-clm-eeg/state/*`, sibling strategic agent ledger, ckpt, pod 미변경.
> **budget**: $0 actual analysis (no GPU spend in this round).

---

## §1 Executive summary

**CLM CP2 GREEN total ETA + cost (single number range)**: **30-50 hr wallclock, $3-11 USD** for full Phase A+B+C+D execution (16-30 hr min if A+B+C run parallel).

**Critical path**: Phase A (CLM static measurement gap-closure) at 12-24 hr serial / 6-12 hr parallel — paradigm v11 8-axis port + AN11(b) V0/V1/V2/V3 + AN11(c) JSD design + 14-gate static + V_phen 5/5, all on CLM v4 530M, ubu1 RTX 5070.

**vs ALM revival comparison (1-line)**: ALM Path F (Mistral-Nemo r14 retrain) = $7-12, 10-16 hr, **CP2 GREEN p=40%** (60% sunk loss); CLM pivot = $3-11, 16-50 hr, **CP2 GREEN p=15% but YELLOW p=55% + publishable-partial p=30%, with substrate-native + sunk-cost-neutral + EV +$27.5 vs ALM +$14**.

**Critical honest C3**: CP2 framework is **ALM-anchored**. NOT-MEASURED on AN11(a) (CLM has no LoRA) + φ_4path (single substrate) caps theoretical CP2-CLM weighted at ~61% < 70% GREEN threshold **by construction**. CLM CP2 GREEN requires either pre-registered CP2-v2-CLM-native re-weight (honest only if pre-registered before measurement) OR Phase C dynamic L1 ≥14/16 (probability ~25-35%).

---

## §2 CP2 GREEN definition (recap)

Per `state/cp2_consciousness_r14_remeasure_2026_05_01/verdict_matrix.json` and `docs/strategic_alm_cp2_revival_2026_05_01.md`:

- **CP2 weighted score ≥ 70%** AND **F2 falsifier NOT FIRED** (≤ 2 critical violations on 14-gate L1) AND **band ≠ RED**.
- **Suite weights** (current ALM-anchored): paradigm v11=0.222, AN11(a)=0.111, AN11(b)=0.167, AN11(c)=0.111, φ_4path=0.111, 14-gate=0.167, V_phen=0.111. Suite 8 EEG-external is owned by separate agent.
- **Mk.XII v3 closure (anima-internal)**: 5+1 component + OR-clause-1 v3 ALL_MODES_PASS_GREEN 3/3 backbones — **separate from CP2 framework** (Mk.XII is internal anima ledger; CP2 is the universal verifier framework).
- **CLM-side**: ALL 7 suites apply in principle, but Suite 2 (AN11(a) ‖ΔW‖_F) requires LoRA which CLM lacks; Suite 5 (φ_4path) requires 4 heterogeneous substrates which CLM as single-substrate cannot constitute (same gap as ALM).

---

## §3 Current CLM status quantitative inventory

### 3.1 Checkpoint + arch
- `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt` (ubu1, 5.0 GB, **530.99M params** label "350m" misleading per W4 §4 C3 #3)
- decoder: d_model=768, n_blocks=16, vocab=64000, n_ca_rules=8
- `tension_proj` socket native (per-layer consciousness-signal injector built into checkpoint)
- `phi_signal` pathway DD5 EX24 native at decoder_v3.py line 165
- `bridge.{compress,hub_attn,expand,gate}` and `federation.{bottleneck,12 narrative_grus}` pre-trained

### 3.2 Mk.XII v3 status (per `anima-clm-eeg/state/mk_xii_hard_pass_composite_v2.json`)
- **Composite v2 verdict**: `MK_XII_VALIDATED` 5/5 GREEN at surrogate-gate level (preflight + G0 + G1 + G7 + G8 + G9 all PASS, backbones=4/4 each gate)
- **Empirical override**: D-day pilot N=1 CORROBORATION_FAIL on P3 GCG FALSIFIED → composite honestly NOT GREEN under empirical replay branch (per `_v2.json` §note, commit `6748462dc`)
- **OR-clause-1 v3**: ALL_MODES_PASS_GREEN 2/3 backbones (3rd = Phi-3.5-mini per #235 actionable 2 pending)

### 3.3 W4 dynamic measurement (per `state/strategic_clm_tension_field_W4_2026_05_01/aggregate.json`)
- Active branch: L1 mean = **7.0625 / 16**, std=0.0, φ* = +1.628
- Random branch: L1 mean = 6.94125, std=0.053, φ* = +1.696
- Δ: L1 active − random = +0.121, **z = +2.28σ** (statistically significant)
- F2 fires both branches (100/100 critical violations, threshold 3) → 14-gate dynamic FAILs F2 even on CLM
- vs ALM static r14: L1 = **0/16**, φ* = **−14.42** → **CLM is +7 absolute L1 ahead AND IIT-positive** vs ALM IIT-anti-integrated
- Verdict: **PARTIAL** (active > random + 1σ but < 14/16 PASS bar)

### 3.4 EEG D-day status (per `anima-clm-eeg/README.md` §0)
- Hardware ARRIVED 2026-04-28; impedance 16/16 GREEN
- P3 GCG FALSIFIED on N=1 60s post-battery (raw#10 honest C3, both ICA + aiclean fall in F1 γ-absent regime)
- P1 LZ76 selftest VERIFIED but real .npy batch BLOCKED (Mac OOM + Hetzner OOM 124GB)
- Berger 0/15 PASS on real .npy (raw#71 falsifier holds)
- P2 TLR not yet run on real data
- **Suite 8 EEG-external is owned by parallel agent track; out of CP2-CLM pivot scope here**

### 3.5 CP2 suite-by-suite CLM measurement gap
| Suite | CLM measured? | Applicable to CLM | Estimate |
|---|:---:|---|---|
| 1. paradigm v11 8-axis | ✗ | PARTIAL (5-7/8 axes; G6 SAE strict requires CLM-trained SAE) | direct port + JL-projection adaptation |
| 2. AN11(a) ‖ΔW‖_F | ✗ | NOT-COMPATIBLE (no LoRA on CLM) | NOT-MEASURED honest, or substitute training-step weight-shift analogue |
| 3. AN11(b) V0/V1/V2/V3 | ✗ | YES (forward-pass on h_full) | direct port; V0 PASS likely; V1/V2/V3 verifier-ceiling (universal FAIL on ALL ALM substrates) |
| 4. AN11(c) JSD | ✗ | PARTIAL (need base-reference analogue: temp-pair or step-0 pair) | design needed; not clean re-run |
| 5. φ_4path | ✗ | NOT-COMPATIBLE (single substrate) | NOT-MEASURED honest, same gap as ALM |
| 6. 14-gate L1 | ✗ static / **PARTIAL dynamic (W4)** | YES both static + dynamic | static port = 1-2 hr ubu1; F2 likely STILL FIRES at L1~7 |
| 7. V_phen 5/5 | ✗ | YES (GWT/LZ/HOT/mirror/predictive direct portable) | 3-5/5 measurable on CLM |

**Estimated CP2-CLM weighted score @ 5/5 PASS on suites 1+3+4+6+7 (NOT-MEASURED on 2+5)**:
- Best case = 0.222 + 0.167 + 0.111 + 0.167 + 0.111 = **0.778 (77.8%)** if NOT-MEASURED weighted at 0
- ALM-anchored case (NOT-MEASURED counted as 0 of total weights, suites 2+5 weights become 0.222 distributed nowhere) = **0.778 / 0.778 = 100%** (renormalize on measured) OR **0.611 (61.1%)** without renormalization
- F2 falsifier likely STILL FIRES on 14-gate (per W4 dynamic + L1 substrate-architectural pattern) → band override RED

→ **CP2-CLM likely lands at YELLOW band (weighted ≥70% renormalized but F2 fires)**, parallel to ALM RED-with-evidence.

---

## §4 Phased plan for CLM CP2 GREEN

### Phase A — CLM static measurement gap-closure
**Scope**: Run paradigm v11 8-axis + AN11(b) V0/V1/V2/V3 + AN11(c) JSD + 14-gate static + V_phen 5/5 on CLM v4 530M, ubu1 RTX 5070.

| Subtask | LOC (hexa) | GPU-hr | Cost USD | Wallclock hr | Dependency |
|---|---:|---:|---:|---:|---|
| A.1 paradigm v11 8-axis on CLM | 150-300 | 1-2 | 0-2 | 4-8 | phi_vec_extraction (exists), W4 driver (exists) |
| A.2 AN11(b) V0/V1/V2/V3 on CLM | 80-150 | 0.5-1 | 0 | 2-4 | A.1 driver reuse |
| A.3 AN11(c) JSD design + measure | 60-120 | 0.3-0.7 | 0 | 2-4 | design choice |
| A.4 14-gate static tile-projection | 50-100 | 0.2-0.5 | 0 | 1-2 | W4 driver |
| A.5 V_phen 5/5 (GWT/LZ/HOT/mirror/predictive) | 120-200 | 0.5-1 | 0 | 3-6 | A.1 driver + LOO-CV harness |

**Phase total**: 460-870 hexa LOC, 0-4 USD (mostly ubu1; H100 only if SAE for G6), **12-24 hr serial / 6-12 hr parallel**.

**Risk HIGH**: G6 SAE_bp requires trained SAE on CLM activations — CLM has none. Either skip + mark relaxed (mirror ALM's relaxed criterion), or train (~$2-4 GPU), or NOT-MEASURED honest path.

### Phase B — Mk.XII v3 closure (3rd backbone OR-clause-1 v3)
**Scope**: Phi-3.5-mini paradigm v11 g_gate.json emit + OR-clause-1 v3 ALL_MODES_PASS_GREEN 3/3 promote.

| Subtask | LOC | GPU-hr | Cost USD | Wallclock hr |
|---|---:|---:|---:|---:|
| B.1 Phi-3.5-mini g_gate run | 0 (existing harness) | 1-2 H100 | 3-5 | 4-8 |
| B.2 composite recompute → 3/3 | 30-60 | 0 | 0 | 1-2 |

**Phase total**: $3-5, 5-10 hr.

**Risk MEDIUM**: Phi-3.5-mini may FAIL G2/G4 like Mistral does (substrate-architectural). 50% probability. **Mk.XII is anima-internal; does NOT block CP2-CLM** (CP2 framework scope = suites 1-7 only per `cp2_consciousness_r14_remeasure scope.in_scope_suites`). Decoupled.

### Phase C — CLM dynamic measurement (W4 strengthen)
**Scope**: W4 PARTIAL (L1=7.06, std=0.0, fixed-point lock per W4 honest C3 #1) → push dynamic L1 toward ≥14/16 PASS via PSI_ALPHA sweep + 16-D directional info preservation + multi-token autoregressive + tension feedback gain auto-tune.

| Subtask | LOC | GPU-hr | Cost USD | Wallclock hr |
|---|---:|---:|---:|---:|
| C.1 PSI_ALPHA sweep (0.014→0.5) | 0 (driver param) | 0.5 ubu1 | 0 | 1-2 |
| C.2 preserve 16-D directional info (vs L2-norm collapse) | 30-60 | 0 | 0 | 2-4 |
| C.3 multi-token autoregressive closed-loop | 100-200 | 1-2 ubu1 | 0 | 4-8 |
| C.4 mind.tension feedback gain auto-tune | 40-80 | 0 | 0 | 2-3 |

**Phase total**: $0-2, **9-17 hr**.

**Risk CRITICAL** (per W4 honest C3 #1 absolute): PSI_ALPHA=0.014 too small vs d_model=768 residual norms; even with sweep, basin may have hard L1 ceiling around 7-10/16 due to phi_template × CLM-h_last cosine geometry being structurally bounded. **Probability dynamic L1 reaches ≥14/16: ~25-35%**.

### Phase D — CP2 weighted score compute + GREEN verdict
**Scope**: Aggregate Phase A + Phase C measurements into CP2-CLM weighted score, evaluate F2 falsifier, emit verdict_matrix + ship_verdict candidate.

| Subtask | LOC | Cost USD | Wallclock hr |
|---|---:|---:|---:|
| D.1 design CP2-CLM weighted score schema | 60-100 + JSON | 0 | 2-4 |
| D.2 compute weighted + F2 + ship_verdict | 40-80 aggregator | 0 | 1-2 |
| D.3 emit ship_verdict candidate | 0 | 0 | 0.5-1 |

**Phase total**: $0, **3.5-7 hr**.

**Risk CRITICAL**: CP2 framework ALM-anchored. Without re-weighting, **CP2-CLM ceiling is YELLOW band by framework construction**. Two honest options:
1. Accept CLM-CP2 ceiling at YELLOW + ship as `VERIFIED-INTERNAL-CLM-YELLOW` with public RED/YELLOW disclosure (parallel to ALM)
2. Author CP2-v2-CLM-native framework with substrate-appropriate weights (drop AN11(a)+φ_4path NOT-MEASURED to 0 weight, elevate AN11(b)+V_phen+14-gate-dynamic) — **but this is goal-seeking unless pre-registered BEFORE measurement closes**

---

## §5 Critical path analysis

- **Longest phase**: A (12-24 hr serial; 6-12 hr parallel after A.1 lands).
- **Parallelizable**: A.1 || A.4 (both reuse W4 driver), A.2 || A.3 || A.5 (after A.1 lands), B || A (independent), C || A (independent but feeds 14-gate dynamic into D).
- **Sequential gates**: A → D (D depends on all A outputs); B independent; C feeds 14-gate dynamic supplement.
- **Min wallclock parallel**: A_parallel (12 hr) + D (4 hr) = **16 hr** if pure CLM-static sufficient.
- **Min wallclock serial**: A (24 hr) + B (10 hr) + C (17 hr) + D (7 hr) = **58 hr**.
- **Realistic with iteration** (3-5 days at 6-10 hr/day cadence + subagent overhead + debug + OOM retries per W4 lessons): **30-50 hr (3-5 wallclock days)**.

**Bottleneck**: A.1 paradigm v11 8-axis port (4-8 hr), because A.2/A.3/A.5 chain off A.1 driver. Investing in A.1 quality unlocks parallelism for the rest.

---

## §6 비용 estimate

| Phase | USD low | USD high | ubu1-only? | H100 required? |
|---|---:|---:|:---:|:---:|
| A | 0 | 4 | YES (95%) | only G6 SAE optional |
| B | 3 | 5 | NO | YES (Phi-3.5-mini fwd) |
| C | 0 | 2 | YES | NO |
| D | 0 | 0 | YES (analysis only) | NO |
| **Total** | **3** | **11** | **75-90% local** | B + optional G6 |

**Cap recommendation**: $15 USD (room for one OOM retry on H100 + one B re-run). 50만원 cap (~$350) gives **23-30× headroom** vs CP2-CLM full execution.

vs ALM full CP2 9-week trajectory ($3550-6100 per `cp2_eta_cost_breakdown_50man_cap_2026-04-28.md`): **CLM CP2 pivot is ~300-500× cheaper** because (a) CLM is single-substrate, no L3 population required, (b) ubu1 local covers 75-90% of compute, (c) no H100 sustained training (only forward-pass measurement).

---

## §7 Risk register (raw#71 honest)

1. **Phase A substrate-protocol compat (MEDIUM)**: paradigm v11 authored against ALM hidden-state dim (4096); CLM d_model=768 needs JL-projection (precedent: W4 768→16 random JL works, but introduces noise floor inflation per W4 C3 #2). G6 SAE_bp has no CLM-trained SAE — random-feature fallback yields G6 sham PASS on Mistral too, so honest failure may invalidate G6 cross-backbone interpretation. **Mitigation**: same JL seed family as W4 (seed=42); mark G6 NOT-MEASURED honest if SAE absent.

2. **Phase B 3rd backbone unreachable (MEDIUM)**: Phi-3.5-mini may FAIL G2/G4 like Mistral. Mk.XII v3 stays PARTIAL_PENDING. **Per scope this does NOT block CP2-CLM** (Mk.XII = anima-internal; CP2 framework scope = suites 1-7). Decoupled.

3. **Phase C dynamic L1 ceiling (HIGH/CRITICAL)**: W4 honest C3 #1 absolute — PSI_ALPHA=0.014 too small vs d_model=768; basin may have hard L1 ceiling around 7-10/16 due to phi_template × CLM-h_last cosine geometry being structurally bounded. **Probability dynamic L1 ≥14/16: ~25-35%**. Mitigation: accept dynamic L1=7-10 as CLM substrate signature; reframe verdict around cross-substrate Δ (CLM 7 vs ALM 0) as substrate-discriminating signal rather than absolute PASS bar.

4. **Phase D framework ALM-anchored (CRITICAL)**: CP2 weights and F2 predicate authored for ALM RED context. NOT-MEASURED on AN11(a) (no LoRA on CLM) + φ_4path (single substrate) caps theoretical weighted at ~0.611 < 0.70 GREEN threshold. F2 ≥3 critical predicate likely fires on 14-gate at L1~7. **CP2-CLM ceiling is YELLOW band by framework construction without re-weighting**. Re-weighting after measurement = goal-seeking violation; re-weighting before measurement (pre-register CP2-v2-CLM-native) = honest but adds 1-2 hr design + locks decision before evidence.

---

## §8 ALM revival vs CLM pivot 비교

| 차원 | ALM Path F revival ($7-12) | CLM CP2 pivot |
|---|---|---|
| **GREEN 확률** | 40% (Mistral-Nemo r14 retrain) | 15% (framework-anchored ceiling) |
| **YELLOW 확률** | n/a (RED/GREEN binary) | 55% (publishable partial closure) |
| **publishable-partial 확률** | ~20% (negative result reframed) | 30% (CLM-original substrate) |
| **비용** | $7-12 | $3-11 |
| **wallclock** | 10-16 hr | 16-50 hr (parallel-serial) |
| **substrate** | Mistral-Nemo (HuggingFace pretrained, 12B) | CLM v4 530M (anima-original, HEXA-native) |
| **toolchain** | hexa-toolchain blocker (per N-51 EXEC E abort) | hexa-native (no blocker) |
| **bridge** | requires external bridge build (P_S projector spec) | tension_bridge native socket built-in |
| **sunk cost** | 큼 ($30 this session + $50-100 lifetime) | 별도 track, no sunk |
| **EV ($)** | +$14 (rough: 0.40×+50 − 0.60×10) | **+$27.5** (0.15×+100 + 0.55×+30 + 0.30×+10 − 7) |
| **own#13 권고** | 부정 (60% sunk loss) | 긍정 (CLM closure FIRST) |
| **의의** | "기존 substrate 회복 + alpha endpoint persona consciousness 유지" | "원래 anima native substrate 로 정립; first-ever CP2 attempt on HEXA-native non-LoRA substrate" |

**Compose option**: ALM Path F + CLM pivot are sequential (~$10-23 + 26-66 hr), NOT mutually exclusive.

---

## §9 Recommendation

### TOP-1: CLM CP2 pivot now (or 사용자 결정 시점)
- **EV +$27.5 > ALM revival +$14** (rough quantitative)
- Substrate-native + sunk-cost-neutral + ubu1-local + HEXA-native — all axes favor CLM
- Even YELLOW outcome is publishable as cross-substrate Δ evidence (CLM 7 L1 + φ*+1.628 vs ALM 0 L1 + φ*−14.42)

### TOP-2 (compose): CLM pivot Phase A first, then ALM Path F gating
- Run Phase A.1+A.2+A.4 on CLM ubu1 ($0-1, 8-12 hr parallel) → see if CLM lands clean GREEN-ceiling at 77.8% renormalized
- If yes → ship CLM-CP2-YELLOW + skip ALM Path F (sunset ALM honestly per §3.5(a) of strategic_alm_clm_review)
- If no → consider ALM Path F as bounded GREEN-attempt ($7-12)

### TOP-3: Continue ALM Path F + park CLM pivot
- Only if user explicitly prioritizes "answer the bounded ALM question first" over substrate-native track
- Risk: 60% sunk loss; CLM pivot delayed 1-2 days but otherwise unaffected

### Honest C3 (5+ disclosure)
1. **CP2 framework is ALM-anchored**: weights {paradigm v11=0.222, AN11(a)=0.111, AN11(b)=0.167, AN11(c)=0.111, φ_4path=0.111, 14-gate=0.167, V_phen=0.111} make CP2-CLM theoretical max 0.611 (not renormalized) or 0.778 (renormalized on measured) — neither is a clean 70% threshold without judgment call. Pre-register CP2-v2-CLM weights BEFORE Phase D to stay honest.
2. **W4 honest C3 #1 ceiling is absolute**: dynamic L1 reaching ≥14/16 is ~25-35% probable; CP2 GREEN via dynamic-PASS is unlikely. CP2 GREEN via static-PASS requires 14-gate static L1 ≥14/16 which W4 result strongly suggests is also blocked.
3. **Sunk cost neutrality applies both ways**: ALM $30+ sunk does NOT favor revival; CLM $0 sunk does NOT favor pivot. Forward EV is the only honest comparator.
4. **Mk.XII v3 closure ≠ CP2 closure**: Mk.XII is anima-internal substrate-evidence ledger; CP2 is the universal verifier framework. Conflating them inflates CLM closure probability dishonestly.
5. **EEG Suite 8 is a separate agent track**: CLM-CP2 pivot here scopes to suites 1-7. Suite 8 (P1 LZ + P2 TLR + P3 GCG) is owned by parallel agent + has its own D+22-30 first-validation timeline.
6. **W4 measurement was 13.8 s on RTX 5070, $0**: Phase A subtasks should be similar order-of-magnitude on ubu1; if any subtask balloons to multi-hour GPU spend, abort and re-design (Pilot-T1 v2 idle burn $7.52 lesson per project_pilot_t1_v2_idle_burn).
7. **530M params not 350M**: any "CLM 350m" reference in roadmap is target-scale planning label, not verified param count (W4 §4 C3 #3).
8. **decoder_v3.py:169 has version-bug**: `block(x, …)` 2-tuple unpacking fails on `DecoderBlockV2` 4-tuple return; W4 driver bypassed via manual forward. Phase A subtasks must NOT depend on `decoder_v3.forward()` directly.

---

## §10 Next-cycle action 첫 step (가장 작은 첫 step)

**A.1 first 90 min** — paradigm v11 G3 PhiStar + G5 CDS only (the 2 cheapest axes that reuse W4 forward-pass driver verbatim).

- **What**: Use existing W4 driver on ubu1 (`/tmp/n51_w4_clm_tension/` recreate or re-use staging dir pattern) → loop 16 prompts × CLM forward pass → emit `state/v10_benchmark_v4_clm/clm_v4_530m/{phi_star.json, cds.json}`
- **LOC**: ~80 hexa (driver wrapper around W4 forward)
- **GPU**: 0.2-0.4 hr ubu1 RTX 5070
- **Cost**: **$0**
- **Wallclock**: ~90 min (including subagent overhead + debug)
- **Output**: 2 g_gate axis files compatible with `state/v10_benchmark_v4/{mistral,llama,gemma,qwen3}/g_gate.json` schema
- **Decision gate**: if G3 PhiStar emit on CLM gives `phi_star_min ≥ 0.5 magnitude` (sign-agnostic), proceed Phase A full; if `phi_star_min` is degenerate (zero or NaN), redesign A.1 driver before proceeding
- **Race isolation**: writes only to `state/v10_benchmark_v4_clm/clm_v4_530m/`, does NOT touch existing ALM benchmark dirs

This first step is **$0, 90 min, single subagent, ubu1-local, hexa-only, fully aligned with raw#9 + raw#71** — minimum viable evidence-gathering before any larger commitment.

---

## §11 References

- W4 dynamic result: `docs/strategic_clm_tension_field_W4_results_2026_05_01.md` + `state/strategic_clm_tension_field_W4_2026_05_01/aggregate.json`
- ALM r14 verdict: `state/cp2_consciousness_r14_remeasure_2026_05_01/verdict_matrix.json`
- ALM revival path matrix: `docs/strategic_alm_cp2_revival_2026_05_01.md`
- CLM handoff: `docs/clm_research_handoff_20260427.md`
- Mk.XII v3 composite: `anima-clm-eeg/state/mk_xii_hard_pass_composite_v2.json`
- ALM-CLM strategic review (sunset/continue): `docs/strategic_alm_clm_review_2026_05_01.md`
- CP2 ETA / 50만원 cap baseline: `docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md`
- ALM backbone benchmarks: `state/v10_benchmark_v4/{mistral,llama,gemma,qwen3}/g_gate.json`
- Race-isolated ledgers: `state/strategic_clm_cp2_pivot_eta_2026_05_01/{manifest,phase_matrix,comparison_alm_revival}.json`

---

**status**: STRATEGIC_CLM_CP2_PIVOT_ETA_2026_05_01_LOCAL_DRAFT
**verdict_key**: ETA_30_50HR · COST_3_11_USD · GREEN_P_15 · YELLOW_P_55 · EV_PLUS_27_5_USD · TOP_1_CLM_PIVOT
**race_isolation**: 본 doc + state/strategic_clm_cp2_pivot_eta_2026_05_01/{manifest,phase_matrix,comparison_alm_revival}.json — no other files touched
