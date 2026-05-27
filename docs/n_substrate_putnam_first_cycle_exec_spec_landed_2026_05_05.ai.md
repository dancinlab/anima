# n_substrate Putnam First-Cycle Exec — SPEC LANDED 2026-05-05

> readers: AI agents (subagents, audit cron, next-session Claude Code)
> spec source-of-truth (frozen): `docs/n_substrate_putnam_first_cycle_exec_spec_2026_05_05.md`
> sister specs: `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` (verifier spec FROZEN), `docs/n_substrate_putnam_check_impl_landed_2026_05_04.ai.md` (verifier impl LANDED), `docs/n_substrate_qmirror_cond6_inclusion_decision_2026_05_04.md` (cond.6 inclusion locked), `docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md` (Phase E binding evidence prep).
> raw invariants: raw#9 (md only), raw#10 (≥5 honest C3), raw#15 (no destructive paths), raw#71 (falsifier formal pre-register).
> mutation footprint this cycle: 0 (spec doc only; no roadmap edit, no tool edit, no commit).

---

## TL;DR

This cycle lands the **first-cycle exec spec** for the Putnam multi-realizability check, converting `tool/n_substrate_putnam_check.hexa` (impl LANDED 2026-05-04) from a "verifier orchestrator runnable" state to a "first concordance verdict from real measurement data" exec recipe. Spec doc enumerates the 17-substrate inventory (15 counted toward N_witnessed per cond.6 inclusion decision; 3 counted toward concordance pair denominator), 5-phase exec plan, dollar-zero ubu1 plus multi-week wall budget (Phase E live EEG is the single human-in-loop bottleneck), 5-row falsifier matrix, and 4 decision Q's queued for user. Most-likely first-cycle verdict is **PARTIAL** (per honest C3 #5: F2 fires until Phase E lands; concordance pinned at 0.333 by 3 measured-Phi pairs). Spec is FROZEN; cycle exec is gated on user Q1-Q4 plus Phase E landing.

## Frontmatter

| field | value |
|---|---|
| spec doc (frozen) | `docs/n_substrate_putnam_first_cycle_exec_spec_2026_05_05.md` |
| spec sections | 13 |
| substrate inventory rows | 17 total (15 counted toward N_witnessed; 3 in concordance pair denominator) |
| falsifier matrix | 5 (F-PUTNAM-1 re-verify + F-PUTNAM-2 single-axis robustness + F-PUTNAM-3 T sensitivity + F-PUTNAM-4 F2 dependency + F-PUTNAM-5 qmirror inclusion enforcement) |
| decision Q's queued | 4 (substrate inventory / cycle timing / T_putnam / cycle ownership) |
| honest C3 in spec | 8 (exceeds raw#10 minimum 5) |
| roadmap mutations | 0 |
| tool mutations | 0 |
| narrative edits | 0 |
| cost (this cycle) | dollar-zero (md-only spec authoring) |
| raw invariants | raw#9 OK / raw#10 OK / raw#15 OK / raw#71 OK |

## 5 key bullets (summarizing sections 1-7)

1. **Goal converts from "runnable" to "first-real-data verdict"** (section 1). Verifier impl `tool/n_substrate_putnam_check.hexa` already emits 3-tier exit codes (PASS=0/PARTIAL=1/FAIL=2) verified locally on 9/9 fixture runs and produces `FAIL n=15 concordance=0.333 f2=FIRES` against the live `.roadmap.n_substrate`. This first-cycle exec replaces the BLM Phase 4 RETRY hardcoded EEG mean (-3.01) with a real Phase E measurement, closes per-substrate Phi-star inventory, and emits a dated landing handoff with verdict + concordance matrix + falsifier results.

2. **Substrate inventory: 17 total / 15 counted toward N_witnessed / 3 counted toward concordance pair denominator** (section 2). Inventory covers CLM v4 (+41.86 ANCHOR), EEG TMS-PCI Casali (literature WITNESSED), EEG live (DEFERRED to Phase E user-gated), AKIDA AKD1000 (BLOCKED hw), QRNG IonQ (LIVE_QUANTUM_SEED), BOLD TRIBE v2 (DEFERRED to Phase 5 stimulus-aligned), qmirror canonical (INCLUDE_N_NOT_CONCORDANCE per cond.6 lock), IIT 4.0 N-12 MULTI-WITNESSED, nexus CHSH 8.97 sigma, TMS-PCI brain stimulus, HoTT N-15 (categorical-witness), N-22 Levin xenobot (PENDING_PARTNERSHIP), N-23 slime/mycelium (PENDING), N-24 octopus IIT exclusion, W1 anima-as-substrate (DOWNGRADED), A1 learned phi-extractor (WITNESSED_NEGATIVE), tensionlink (POC_TIER). Counting reconciles with verifier production-mode `n=15` emit verbatim.

3. **5-phase exec plan, mostly compute-trivial** (section 3). Phase 1 substrate enumeration (Mac hexa, 5 sec) then Phase 2 per-substrate Phi-star measurement orchestration (multi-week wall, dollar-zero; Phase E user-gated EEG is the bottleneck) then Phase 3 concordance computation (Mac hexa, 1 sec) then Phase 4 F2 falsifier state read (Mac hexa, under 1 sec; reads `n_substrate.blk.1.status`) then Phase 5 verdict emission + cache + landing doc author (Mac hexa + doc, 2-4h). Most-likely first-cycle output: `FAIL` or `PARTIAL` depending on Phase E availability and F2 state.

4. **Resource budget: dollar-zero plus 3-week wall** (sections 4 + 7). Compute is trivial (under 10 min total across all phases), API/QPU is dollar-zero (reuses 2026-05-02 events #120/#124/#125/#127 cumulative dollar-324.65 already paid). Wall is 2 weeks pre-cycle (Phase E live OpenBCI session scheduling + alcohol-free 24-48h prereq + 30-min session + 3-5 day offline analysis) plus 1 day cycle exec plus 3 days post-cycle peer review. Storage 5 GB (CLM hidden states + EEG raw .xdf + analysis intermediates). Single point of failure is Phase E user-gated session.

5. **Falsifier matrix locks 5 invariants pre-cycle** (section 5). F-PUTNAM-1 (reproducibility, re-verified) plus F-PUTNAM-2 (single-axis robustness — new harness scaffolded this cycle) plus F-PUTNAM-3 (T_putnam plus-or-minus 0.05 sensitivity sweep) plus F-PUTNAM-4 (F2 unfire dependency — emit cap PARTIAL while F2 fires) plus F-PUTNAM-5 (qmirror cond.6 inclusion enforcement — verify count-but-don't-pair-denominator rule). All 5 LOCKED at this spec landing per raw#71; future cycle that proposes threshold change emits dated successor falsifiers, never amends in-place.

## 4 decision Q's queued for user (section 9 verbatim)

**Q1 — substrate inventory**: accept current 15 (14 substantive WITNESSED + qmirror cond.6) per section 2 table OR add/remove specific axes (e.g., add N-22 if Levin replies, remove A1 to be conservative)? **Default if defer**: accept 15 verbatim.

**Q2 — cycle timing**: start now with placeholder EEG (no new info; reuses BLM Phase 4 RETRY mean) OR wait for Phase E EEG live session to land first (2 weeks wall, recommended)? **Default if defer**: wait for Phase E.

**Q3 — T_putnam threshold**: accept 0.40 per spec section 4.2 OR pre-set alternative T (0.35 stricter / 0.50 looser, latter discouraged) OR re-calibrate post-data via successor cycle (recommended)? **Default if defer**: accept 0.40 plus F-PUTNAM-3 sensitivity sweep verifies stability.

**Q4 — cycle ownership**: anima orchestrator hexa (single-host, sufficient for 10 min compute) OR distributed multi-host (over-engineered for this scope) OR subagent BG parallel per substrate (over-engineered)? **Default if defer**: anima orchestrator hexa Mac + ubu1 single-host.

## Honest C3 caveats (raw#10) — minimum 5 (here 8)

**C1 — Multi-week wall is data-collection bound, NOT compute bound.** The cycle's compute footprint is ~10 minutes total. Wall is dominated by Phase E user-gated EEG live session (alcohol-free 24-48h prereq + 30-min session + 3-5 day offline analysis). If user has ALREADY completed Phase E session, this cycle could close in ~1 day.

**C2 — Most-likely first-cycle verdict is PARTIAL (or FAIL).** Even with optimistic Phase E PASS landing, BOLD remains DEFERRED to Phase 5 stimulus-aligned remediation. Concordance ratio is bottlenecked by 3 measured-Phi substrates (CLM, BOLD, EEG-IIT4) → with T=0.40 + current per-substrate means, concordance ≈ 0.333 < 0.60 PASS threshold. PASS is reachable in principle only after BOTH (a) F2 unfire AND (b) concordance >= 0.60 — both gated on Phase E + Phase 5 deferred work.

**C3 — F2 unfire dependency is the load-bearing single-point-of-failure for ANY non-PARTIAL verdict.** Even if substrate inventory grows, even if concordance somehow exceeds 0.60, F-PUTNAM-4 caps verdict at PARTIAL while `n_substrate.blk.1.status == "open"`. The blk.1 closure path is "Phase E binding evidence + N-22 partnership + N-12 IIT 4.0 proper Phi-star (dollar-1500-plus separate budget)" per `.roadmap.n_substrate` — multi-track and multi-month at minimum.

**C4 — F-PUTNAM-2 single-axis robustness harness is NEW this cycle (deferred from impl-landed 2026-05-04 honest C3 g).** The harness was explicitly out-of-scope for the impl-landing cycle and is now scoped into this first-cycle exec. Implementation requires programmatic axis-removal scripting (parse roadmap, remove one axis, rerun verifier, repeat for all 15 axes); this harness must be built before F-PUTNAM-2 verification at cycle close. Roughly 1-2h ubu1 hexa codegen, dollar-zero.

**C5 — T_putnam = 0.40 is a judgment-call calibration, NOT empirically derived.** Spec section 4.2 acknowledges this explicitly. F-PUTNAM-3 plus-or-minus 0.05 sensitivity sweep verifies T is not a knife-edge; if FAIL fires, successor cycle re-calibrates with section 4.5 backfit-risk discipline (non-anima reference required). External readers MUST be told T=0.40 is an anima-internal pessimistic-linearization choice, not a literature standard.

**C6 — Substrate inventory counts 15 axes by anima-canonical 3-field rule (section 1.2); some axes are categorical/anchor and not Phi-star-bearing.** HoTT N-15 (categorical-witness, not Phi-star value), N-24 octopus IIT exclusion (literature anchor, not measured), TMS-PCI brain stimulus (literature reference) — all count toward N_witnessed but contribute zero to concordance pair denominator. The 3-pair concordance computation is the load-bearing piece; 15-axis count is satisfied easily (well above 5 floor).

**C7 — No multi-lab cross-replication this cycle.** F-PUTNAM-1 through F-PUTNAM-5 are anima-internal pre-registers verifiable against the verifier hexa. External validation of the Putnam multi-realizability claim under T=0.40 + N=5 floor requires multi-lab independent measurement — explicitly out of scope for this dollar-zero cycle. Successor cycles can pursue this (e.g., MEG SNU / N-14 or Loihi3 INRC / N-17) but not in this first-cycle exec.

**C8 — Cycle does NOT mutate `.roadmap.n_substrate` directly.** Per raw#15 + spec section 11 out-of-scope, the cycle close emits a **proposal** for an additive-append entry to `.roadmap.n_substrate` cond.1.evidence array (`n_substrate.first_cycle_putnam_verdict_<DATE>` JSONL line). Application of that proposal is a separate additive-only mutation cycle — explicitly NOT this BG, NOT the cycle exec, NOT the cycle close. This preserves SSOT discipline and lets the user audit the proposal before commit.

## Cross-link table (predecessors + sister specs)

| reference | role |
|---|---|
| `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` | verifier spec FROZEN (decision rule section 2.3, T=0.40, falsifier preregister F-PUTNAM-1/2) |
| `docs/n_substrate_putnam_check_impl_landed_2026_05_04.ai.md` | verifier impl LANDED (paper-runnability sub-blocker CLOSED; tool/n_substrate_putnam_check.hexa 656 LoC; 3-tier exit dispatch verified 9/9) |
| `docs/n_substrate_qmirror_cond6_inclusion_decision_2026_05_04.md` | cond.6 INCLUDE_N_NOT_CONCORDANCE locked 2026-05-04 (boundary-clarifying; counts toward N_witnessed but excluded from concordance pair denominator) |
| `docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md` | Phase E binding evidence prep spec (sister; gates F2 unfire; user-gated 30-min OpenBCI session) |
| `docs/n_substrate_putnam_first_cycle_exec_spec_2026_05_05.md` | THIS cycle's spec doc (FROZEN at this landing) |
| `tool/n_substrate_putnam_check.hexa` | verifier impl artifact (no edits this cycle; FROZEN at impl-landed 2026-05-04) |
| `tool/clm_consciousness_verify.hexa` | downstream consumer (Putnam check #4 slot delegates to sub-tool) |
| `tool/anima_phi_v3_canonical.hexa` | phi formula reference (CLM baseline 41.86) |
| `state/n_substrate_putnam_check_fixtures_2026_05_04/` | unit test fixtures (synthetic; not for evidence citation) |
| `.roadmap.n_substrate` cond.1 | data source for substrate witness array; proposed additive append at cycle-close (separate cycle) |
| `nexus/.roadmap.qmirror` | qmirror substrate witness extension (cond.5/6/7) |

## Verdict

**SPEC LANDED — first-cycle exec spec FROZEN at 2026-05-05.** Cycle exec is gated on (1) user answers to Q1-Q4, (2) Phase E binding evidence WITNESSED (only required if Q2 default selected), (3) F-PUTNAM-2 single-axis robustness harness scaffolded (1-2h ubu1 hexa codegen, dollar-zero). Most-likely first-cycle verdict is **PARTIAL** per honest C3 #2-3 (F2 fires + concordance bottlenecked at 0.333). PASS is multi-cycle-distant: requires Phase E + Phase 5 BOTH landing successfully. This BG closes the V2 closure audit V3 architecturally-tractable item #3 ("Putnam multi-realizability first cycle") at the **spec-frozen** stage; cycle exec itself remains user-gated.

(end of file)
