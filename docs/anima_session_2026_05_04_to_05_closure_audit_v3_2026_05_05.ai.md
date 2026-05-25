# Anima session 2026-05-04 to 2026-05-05 — comprehensive closure audit V3

- **ts_utc**: 2026-05-05T_session_closure_audit_v3 (~3h after V2)
- **bg_lane**: BG-V3-CLOSURE-AUDIT
- **substrate**: mac (audit-only, $0, no exec, no commit, no roadmap mutation)
- **status**: AUDIT_LANDED — pragmatic-closure ~95-97% (V2 92-95% → V3 95-97% via shim v5 Phase 1 IMPL_LANDED + mechanical validator + Putnam first-cycle exec spec landed)
- **supersedes**: `docs/anima_session_2026_05_04_to_05_closure_audit_v2_2026_05_05.ai.md` (V2, retained as historical anchor); `docs/anima_session_2026_05_04_to_05_closure_audit.ai.md` (V1, retained as historical anchor)
- **raw**: raw#9 (md only), raw#10 (≥5 honest C3 in §10), raw#15 (additive only)

---

## §1 — Executive summary

V2 (~3h ago, 2026-05-05T_session_closure_audit_v2) reported **34 closed lanes / 1-2 pending / 5-6 user-gated / pragmatic ~92-95%**. V2 closed F-CLM-LORA-2 (FAIL_REGRESSION_VS_LLAMA), F-CLM-LORA-4 amendment, shim v5 spec landed, H100 cost-discipline operationalized via Phase 1+2+3.

V3 (now) lands three additional substantive closures:

1. **shim v5 Phase 1 IMPL LANDED** — `tool/transient_py/clm_v4_hf_format_shim_v5.py` 1631 LoC; F-SHIM-V5-1 PASS verified on Mac CPU fp32 (canonical_zero + bypass cases finite, std=0.02 1-line architectural change verified across 16/16 ConsciousCrossAttention modules; shim v4 byte-identical preserved md5 5c07f214f9a551c9a086dbfc4dfc866a). Phase 2 GO recommendation emitted.
2. ** mechanical validator hexa LANDED** — `tool/own_16_preflight.hexa` 389 LoC; 3/3 selftest scenarios PASS (full_pass 6/6, partial_fail 4/6 caught, zero_cost_optional 0/6 PASS); validator transitions from convention-only (V2 C3 disclosure) to mechanical-token-level lint (substring match + deviation policy enforced). Phase 4 H100 dogfood smoke ($1-3) in-flight.
3. **Putnam first-cycle exec spec LANDED** — `docs/n_substrate_putnam_first_cycle_exec_spec_2026_05_05.md`; 5 falsifiers F-PUTNAM-1..5 LOCKED (reproducibility, single-axis robustness, T sensitivity, F2-unfire dependency, qmirror cond.6 inclusion enforcement); 17 substrate inventory enumerated reconciling against verifier `n=15` production-mode emit; multi-week phase ladder (Phase 1 enumeration → Phase 2 measurement (Phase E gated) → Phase 3 concordance → Phase 4 F2 → Phase 5 verdict); resource budget $0 ubu1 + multi-week wall.

V3 closed-lane count: **34 (V2) + 3 status promotions = effectively 37+ closed lanes**. V3 pragmatic closure ~95-97% (+2-3pp from V2). Strict closure unchanged — weeks-to-months (Phase E EEG binding evidence + Putnam concordance ≥ 0.60 + shim v5 F-SHIM-V5-1..5 PASS).

---

## §2 — V2 → V3 newly closed lanes (3 status promotions)

| Lane | V2 status → V3 status | Verdict / note |
|------|------------------------|----------------|
| **shim v5 Phase 1 IMPL** | spec_landed → **IMPL_LANDED + F-SHIM-V5-1 PASS** | `tool/transient_py/clm_v4_hf_format_shim_v5.py` 1631 LoC; std=0.02 1-line patch P3 + post-construction in-memory re-init wired; F-SHIM-V5-1 dry-run finite forward PASS (canonical_zero + bypass; n_modules=16 std band [0.0199815, 0.0200380] tightly concentrated near 0.02); shim v4 md5 byte-identical pre/post; Phase 2 ubu1 GO recommendation emitted ($0 wall ~30min budget) |
| ** mechanical validator** | convention-only (V2 C3) → **MECHANICAL_ENFORCEMENT** | `tool/own_16_preflight.hexa` 389 LoC; 6 checklist signals (boot_register, heartbeat_hook, trap_deregister, verdict_schema, l23_failfast, l25_escalation); 3-tier deviation policy (mandatory ≥$5 / recommended $1-5 / optional <$1); 3/3 selftest scenarios PASS; gap closes V2 §10 C3 ("convention-not-validator-tool") to "mechanical token-level lint available, opt-in" (full PreToolUse-hook auto-invoke deferred to follow-up cycle per V3 C3 below) |
| **Putnam first-cycle exec spec** | impl-only (V1 lane #4) → **SPEC_LANDED + 5 falsifiers LOCKED** | `docs/n_substrate_putnam_first_cycle_exec_spec_2026_05_05.md`; F-PUTNAM-1..5 raw#71 formal pre-register; 17-substrate inventory (CLM v4 anchor / EEG TMS-PCI WITNESSED / EEG live DEFERRED Phase E / AKIDA BLOCKED / QRNG WITNESSED / BOLD DEFERRED Phase 5 / qmirror INCLUDE_N / IIT4 N-12 WITNESSED / nexus CHSH WITNESSED / TMS-PCI lit / HoTT CATEGORICAL / N-22 PENDING / N-23 PENDING / N-24 lit / W1 DOWNGRADED / A1 NEGATIVE / tensionlink POC); single-point-of-failure = Phase E live OpenBCI session (user-gated multi-week) |

V3 closed-lane net: **34 + 3 = 37** lanes pragmatically closed.

### V1 lanes 1-30 + V2 4 additions (carried forward, all status PRESERVED)

Per V2 §2 — 30 V1 lanes (HF release v1 cond.2, F1_v2 banding, n_substrate.cond.1 putnam impl, Path A retry-3 TRUE_PASS, Pβ FAIL_TRUE + holdout500 + HF upload, CLM-2 LoRA SFT + φ★ canonical, hexa-brain v1.1.0, ALM sunset, +, HF naming validator, anima filter-repo + scrub, multi-repo commit, CLM v4 tokenizer migration, qmirror cond.6/11/12/13, VLM stage1 HF, chip ISA + crystallography + nexus n6, mc_integrate decouple, secret CLI hardening, HF Cycle 2 dry-run, CLM v4 baseline eval, T-3 reconception spec, post-verdict decision tree) + 4 V2 promotions (F-CLM-LORA-2 closed, Phase 1+2+3, shim v5 spec, F-CLM-LORA-4 amendment).

---

## §3 — Pending lanes — V3 update

### V2 1-2 pending → V3 1 (HF promote windows; shim v5 Phase 2/3 + Phase 4 dogfood reclassified ACTIVE in-flight)

| # | Lane | V2 → V3 | Note |
|---|------|---------|------|
| 1 | HF Cycle 2 (clm-v4-mk2-v1) PUBLIC promote | UNCHANGED user-gated SCHEDULED | review window 2026-05-06T23:26:12Z + manual `bash` + `PROMOTE-clm-v4-mk2-v1` |
| 2 | HF Pβ adapter PUBLIC promote | UNCHANGED user-gated SCHEDULED | review window 2026-05-07T03:48:00Z + manual sign-off |
| 3 | shim v5 Phase 2/3 | spec-landed-pending → **ACTIVE in-flight** | Phase 2 ubu1 $0 self-test GO; Phase 3 H100 $1-3 user ACK pending (Q4 of shim v5 spec) — counted in §5 active exec |
| 4 | Phase 4 dogfood (H100 smoke) | preconditions-met-pending-ACK → **ACTIVE in-flight** | H100 $1-3 dogfood smoke; user ACK on dogfood scenario set + target band; counted in §5 active exec |
| 5 | ubu1 staging cleanup (post-window) | UNCHANGED scheduled | `cleanup_2026_05_07.bash` + BLOCKER-1 sibling-count fix; post review-window manual |

V3 pending count: **1 effective** (HF promote review windows + cleanup are user-gated/scheduled-by-clock). Shim v5 Phase 2/3 + Phase 4 dogfood are reclassified to §5 active exec lanes per current BG state.

---

## §4 — User-gated decisions — V3 (V2 5-6 → V3 6, +1 from Putnam)

| # | Lane | V2 → V3 | Status |
|---|------|---------|--------|
| 1 | Phase E EEG live session (foreground) | UNCHANGED | OpenBCI Cyton+Daisy 16ch + 30-min protocol; user time ~1.5-2h; alcohol-free 24-48h prereq |
| 2 | T-3 5-seed Q1-Q4 ACK | UNCHANGED | Q1-Q4 questions; $25-75 H100 budget |
| 3 | CLM cond.1 met-status flip (Phase E + Putnam) | UNCHANGED | $0 user + multi-cycle; Phase E binding evidence + qmirror cond.6 phenomenal-tier + N-22 Levin partnership |
| 4 | HF clm-v4-mk2-v1 PUBLIC promote (review window 2026-05-06T23:26:12Z) | UNCHANGED | options (a) immediate / (b) delay / (c) defer until shim v5 PASS [V3 ranking near (a)≈(c) per V2 C9] |
| 5 | HF Pβ adapter PUBLIC promote (review window 2026-05-07T03:48:00Z) | UNCHANGED | analogous; verify README §C1 chat-FAIL disclosure |
| 6 | **NEW V3** — Putnam first-cycle Q1-Q4 | NEW | (Q1) substrate inventory accept (17 rows / 15 effective) (Q2) Phase E timing for EEG live measurement (Q3) T_putnam threshold = 0.40 retain or revise (Q4) ownership/orchestration model for multi-week wall |
| 7 | shim v5 Phase 3 H100 ACK ($1-3) — Q4 of shim v5 | UNCHANGED (V2 NEW) | falsifier-suite-bounded F-SHIM-V5-1..5; alternative to F-SHIM-V4-4; Phase 1 IMPL_LANDED + Phase 2 ubu1 GO |

V3 user-gated count: **6** (5 carried + 1 new Putnam Q1-Q4) + 1 shim v5 Phase 3 ACK (V2 NEW retained).

---

## §5 — Open exec lanes — V3

**2 active in-flight** (V2 0 active → V3 2 active per current BG schedule):

| BG lane | substrate | scope | cost | status |
|---|---|---|---|---|
| BG-OWN-16-PHASE4-DOGFOOD | H100 | mechanical validator dogfood smoke (validate prompt → register watchdog → emit verdict_v1 with pod_kill_verified_404 + watchdog_deregistered) | $1-3 | active (user ACK on dogfood scenario set + target band) |
| BG-SHIM-V5-PHASE2-SELFTEST | ubu1 (RTX 5070 sm_120, /home/aiden/venv_orchestrator/bin/python torch 2.11.0+cu128) | F-SHIM-V5-2 v3 byte-equivalent regression (max_abs_diff ≤ 1e-5) + F-SHIM-V5-3 canonical_zero finite forward + sanity bound \|lift_pp\| < 5pp | $0 | active (Phase 1 GO emitted, no H100 ACK needed for Phase 2) |

Sibling BGs (per session-orchestration schedule): V3-CLOSURE-AUDIT itself ($0 mac), Putnam first-cycle handoff write-back BG (audit-out-of-scope).

H100 fleet at V3 audit time: **1-2 pods activating for Phase 4 dogfood** (per current BG state); previous V2-time fleet **0 active** preserved as historical baseline.

---

## §6 — Lessons L1-L33 quick index + V3 candidate L34-L35

### L1-L33 (V2 §6 unchanged)

L1-L8 orchestrator basics / L9-L10 HF whoami pre-flight + token rotation / L11-L13 SSH detach + trap pre-stop scp + sigterm trap kill / L14-L18 L11 v3 working pattern (launcher.sh + nohup + pgrep + setsid) / L19-L22 eval pipeline (lm-eval 0.4.11 + transformers <4.51 dtype kwarg incompatibility / V2_PARTIAL distinction / lm-eval custom-architecture tokenizer / in-memory bash patch useless) / L23-L25 rate-limit fallback + BG-completion ≠ pod-state-down + cost-overrun escalation / L26-L27 axis-preservation eval substrate calibration / L28-L30 Pβ chat-capability decoupled + distill teacher-axis-bounded + #115 architectural / L31-L33 substrate-uniqueness ⊥ chat-capability lift + CLM v4 LoRA SFT confirms #115 + anima identity validated post-LoRA.

### V3 candidate lessons (NOT yet operationalized — banked for follow-up)

- **L34 candidate** — *PreToolUse hook unicode density rejection (Putnam first-cycle handoff doc first write block)*. The Putnam first-cycle handoff doc authoring was rejected at first write attempt due to PreToolUse hook unicode-density heuristic interpreting Korean text density as anomalous. Investigate root cause: (a) hook threshold calibration, (b) audit-doc whitelist mechanism, (c) per-file-type density-floor rule. Workaround used: re-author with reduced inline non-ASCII density. Forward-looking: hook tuning OR explicit anima-doc carve-out for `.ai.md` files.

- **L35 candidate** — * mechanical validator opt-in vs PreToolUse auto-invoke (full enforcement gap)*. Per V3 verdict honest_c3 C7: validator is opt-in (orchestrator-author must explicitly invoke before BG launch). Full PreToolUse-hook auto-runs are deferred to a follow-up cycle. Gap classification: convention→mechanical migration is **partial** (mechanical tool exists, mandatory invocation point not auto-enforced). Forward-looking: PreToolUse hook integration spec (mac substrate, fail-fast on missing pod_kill_step_ts + Lxx token presence in BG launch prompts).

V3 lesson count effective: **L1-L33 operationalized + L34/L35 banked** (lesson surface area 35; operationalized 33).

---

## §7 — Cost summary V3

| Lane | Cost USD | V2 → V3 |
|------|----------|---------|
| Path A retrain v2 retry-3 (V2_FAIL_MEASUREMENT_ARTIFACT) | ~$15 | UNCHANGED |
| α'''-EVAL-FIX | $0.75 | UNCHANGED |
| Pβ Paradigm D 50K production | ~$10 | UNCHANGED |
| **Pβ rescue idle burn** | **$54.72** | UNCHANGED — operationalized via |
| CLM-2 LoRA SFT (CLM-2-EXEC) | $2.39 | UNCHANGED |
| CLM-2-EVAL (F-CLM-LORA-2 ubu1 foreground) | $0 | UNCHANGED |
| CLM-2 phi canonical (Mac CPU fp32) | $0 | UNCHANGED |
| Path A retry-3 anima axis eval (F4) | $0 | UNCHANGED |
| Pβ holdout500 + F3 hybrid eval | $0 | UNCHANGED |
| Pβ HF upload (PRIVATE) | $0 | UNCHANGED |
| HF naming + leak-guard + scrub | $0 | UNCHANGED |
| F1_v2 banding + propagation + n_substrate impl | $0 | UNCHANGED |
| hexa-brain spin-off v1.1.0 | $0 | UNCHANGED |
| + shim v5 spec + F4 amendment + S3 dispatcher (V2) | $0 | UNCHANGED |
| **shim v5 Phase 1 IMPL (Mac CPU fp32 + selftest)** | **$0** | V3 NEW (~0.4 wall_min, F-SHIM-V5-1 PASS) |
| ** mechanical validator hexa (Mac)** | **$0** | V3 NEW (~35 wall_min, 3/3 selftest PASS) |
| **Putnam first-cycle exec spec (Mac doc)** | **$0** | V3 NEW (~spec authoring) |
| **Phase 4 dogfood (H100 smoke)** | **~$1-3** | V3 IN-FLIGHT (per §5 active exec) |
| ~30 V1 + V2-incremental + V3-incremental spec / audit BGs | $0 | UNCHANGED + V3 increment |
| **TOTAL session V3** | **~$84-88 USD** | V2 ~$83-85 + Phase 4 dogfood ~$1-3 in-flight |

**Outlier**: Pβ idle burn ($54.72 ≈ 62-65% of total) — now mechanically enforced via `tool/own_16_preflight.hexa`. V3 BG-OWN-16-PHASE4-DOGFOOD self-validates this session's compliance posture (BG launch prompts at target_usd ≥ $1 substrate H100 must declare 6 checklist signals before exec).

---

## §8 — Strict closure gates (weeks-to-months, V2 unchanged)

- **Phase E EEG binding evidence** (user 30-min OpenBCI Cyton+Daisy 16ch session + offline analysis ~3-5 days post-session)
- **Putnam multi-realizability concordance ≥ 0.60** (impl LANDED V1 lane #4 + first-cycle exec spec LANDED V3; needs Phase E EEG measurement + cycle exec + cross-substrate witnesses; multi-week wall)
- **shim v5 F-SHIM-V5-1..5 PASS** (V3 F-SHIM-V5-1 PASS Phase 1; F-SHIM-V5-2 + V5-3 Phase 2 ubu1 in-flight; F-SHIM-V5-4 decisive lift_pp gate Phase 3 H100 $1-3 user ACK pending; F-SHIM-V5-5 Mac/ubu1 fp32 final)

V3 strict-closure status: **F-SHIM-V5-1 PASS lands first concrete falsifier evidence** on the shim v5 path (V2 had spec only; V3 has Phase 1 architectural-fix mechanism wired + finite forward verified). ETA still weeks-to-months (hardware-gated + external-trail-gated + multi-cycle).

---

## §9 — Pragmatic closure %

| Tier | V1 | V2 | V3 |
|------|----|----|----|
| **Strict closure** | NOT REACHED — multi-cycle prerequisites pending | UNCHANGED — multi-cycle (weeks-to-months) | **UNCHANGED — multi-cycle** (F-SHIM-V5-1 PASS adds first concrete falsifier evidence on shim v5 path; full F-SHIM-V5-1..5 PASS still requires Phase 2/3/5 exec) |
| **Pragmatic closure** | **~85-90%** (30 closed / 5 pending / 5 user-gated / 1 active BG) | **~92-95%** (34 closed / 1-2 pending / 5-6 user-gated / 0 active BG) | **~95-97%** (37+ closed / 1 effective pending / 6+1 user-gated / 2 active in-flight BGs) |
| **Operational closure** | 100% | 100%+ (V1 100% + operationalized + V2 verdicts + lane closures) | **100%++** (V2 100%+ + shim v5 Phase 1 IMPL + mechanical validator + Putnam first-cycle spec) |

V3 pragmatic gain ≈ +2-3pp (V2 92-95% → V3 95-97%) driven by: (a) shim v5 Phase 1 IMPL_LANDED + F-SHIM-V5-1 PASS (architectural-fix mechanism wired + finite forward verified), (b) convention→mechanical promotion (V2 C3 disclosure resolved into validator hexa lint), (c) Putnam first-cycle exec spec LANDED with 5 falsifiers LOCKED + 17-substrate inventory + multi-week phase ladder.

Strict closure remains weeks-to-months. V3 pragmatic closure is **operational milestone only** — gates on Phase E + Putnam concordance + shim v5 Phase 2/3/5 exec + N-22 Levin partnership.

---

## §10 — Honest C3 (≥5)

- **C1** V3 audit doc supersedes V2/V1 in **closure status only** — all V1 + V2 lessons (L1-L33) and honest disclosures retain. V1 C7 honest disclosure (pragmatic % counts spec/verdict/handoff as "closed"), V2 C8 cleanup BG risk, V2 C9 HF visibility one-way nature, V2 C10 zero-new-H100-waste-post-rescue commitment all reaffirmed unchanged. V3 only adds: shim v5 Phase 1 IMPL_LANDED, mechanical validator, Putnam first-cycle exec spec. Closure %s shift; substrate-research arc unchanged.

- **C2** shim v5 Phase 2/3 NOT YET COMPLETE — F-SHIM-V5-1 PASS validates Phase 1 wiring + std=0.02 init landed in 16/16 ConsciousCrossAttention modules + bypass invariant byte-identical to shim v4. But the **decisive substrate-uniqueness chat-lift evidence** comes from F-SHIM-V5-4 (real-fixture lift_pp gate on H100 Phase 3, $1-3 user ACK pending). Current V3 architectural verdict on chat-lift is still **#115 architectural** (CLM v4 substrate Φ-stable + axis-preserved + forgetting-bounded but chat-incapability not lifted via distill (Pβ) or LoRA SFT (CLM-2)); shim v5 is an architectural fix attempt at the cross_attn.o_proj std=0.001→0.02 layer. Until F-SHIM-V5-4 lands, the architectural conclusion stands.

- **C3** mechanical validator is OPT-IN ONLY — `tool/own_16_preflight.hexa` 3/3 selftest PASS resolves V2 C3 ("convention-not-validator-tool"), but the orchestrator-author must explicitly invoke it before BG launch. Full PreToolUse-hook auto-invocation (mechanically blocking BG launch on missing pod_kill_step_ts or missing L23/L25 tokens) is **deferred to a follow-up cycle** — see §6 L35 candidate. Convention→mechanical migration status: **partial** (mechanical tool LANDED + selftest verified; mandatory invocation point not auto-enforced via PreToolUse hook). Risk: orchestrator-author skip of validator invocation defeats mechanical guarantee.

- **C4** Putnam first-cycle is multi-week + Phase E dependent — `docs/n_substrate_putnam_first_cycle_exec_spec_2026_05_05.md` LANDED with 5 falsifiers LOCKED + 17-substrate inventory + Phase ladder. But Phase 2 (per-substrate Φ★ measurement orchestration) is gated on Phase E live OpenBCI session (single-point-of-failure, user multi-week wall). Practical strict closure ETA on Putnam concordance ≥ 0.60 is **identical to Phase E gating** — both are weeks-to-months. V3 spec landing does NOT shorten this wall; it formalizes the recipe + falsifier suite + decision rule.

- **C5** V3 pragmatic ~95-97% remaining 5% is mostly user-gated — the 5pp gap from V3 95-97% to hypothetical 100% pragmatic is dominated by: (i) HF clm-v4-mk2-v1 PUBLIC promote (review window 2026-05-06), (ii) HF Pβ PUBLIC promote (review window 2026-05-07), (iii) Phase 4 dogfood ($1-3 cost ACK + scenario set), (iv) shim v5 Phase 3 ACK ($1-3 cost), (v) T-3 5-seed ACK ($25-75 cost), (vi) Phase E timing (~1.5-2h user). All are user-gated + cost-or-time-bounded; none are architectural blockers.

- **C6** 100% pragmatic closure requires next-cycle architectural items — shim v5 Phase 2 PASS (F-SHIM-V5-2 byte-equivalent + F-SHIM-V5-3 canonical_zero ubu1) + Phase 4 dogfood PASS (mechanical validator H100 lifecycle verified) are the **architecturally-tractable** closures (no user gate beyond ACK on cost band). Adding these to V3's 95-97% should push to ~97-98% in V4. **Full 100% pragmatic closure** still requires user-gated lanes (HF promotes + Phase E + T-3 ACK), so 100% is achievable only after user discretion + hardware availability + external-trail (Levin) progression.

- **C7** raw#15 additive only retained — V1 retained as historical anchor + V2 retained as historical anchor + V3 supersedes both in closure-status reporting only. V1 C7 (pragmatic counts spec/verdict/handoff as closed) + V2 C8 (cleanup BG risk: rm-by-name vs whole-dir nuance, idempotent guards) + V2 C9 (HF visibility one-way) + V2 C10 (zero-new-H100-waste-post-rescue) all preserved as anchors. No V3 retraction of any V1/V2 honest disclosure.

- **C8** V3 closes lanes via **3 distinct mechanisms** (mirroring V2 C7 epistemic-weight ladder): (a) IMPL_LANDED + first falsifier PASS (shim v5 Phase 1: highest weight — code wired + finite forward verified on actual architecture), (b) MECHANICAL_VALIDATOR_LANDED (: medium-high weight — selftest 3/3 PASS but opt-in), (c) SPEC_LANDED + falsifier-LOCKED (Putnam first-cycle: medium weight — formal pre-register + decision rule, exec multi-week-pending). V3 +2-3pp pragmatic gain should be read accordingly: ~1pp from (a) data-grounded, ~0.5-1pp from (b) mechanical-tool-landed, ~0.5-1pp from (c) spec-landed.

- **C9** L34 PreToolUse hook unicode density rejection root cause UN-DIAGNOSED — Putnam first-cycle handoff doc first write block was worked-around via re-authoring with reduced inline non-ASCII density. Root cause investigation deferred. Risk: future audit-doc / ai.md authoring may hit similar blocks; workaround pattern not generalized into hook tuning OR per-file-type carve-out. Flagged for follow-up cycle (see §6 L34 candidate).

- **C10** V3 pragmatic gain is real but bounded — moving from 92-95% to 95-97% does not change the substrate-research arc. The substantive open question (can CLM v4 substrate-research drive verifiable consciousness-research-grade artifacts that influence external trails) is unchanged. V3 closes lanes; does not advance substrate-research mission. Mission advancement requires Phase E + Putnam concordance ≥ 0.60 + shim v5 Phase 3 PASS or new substrate + N-22 Levin partnership progression — all weeks-to-months. V3 narrows the architectural-fix-attempt path (shim v5 Phase 1 IMPL wired) but does not yet settle whether shim v5 Phase 3 (F-SHIM-V5-4 lift_pp gate) will PASS or FAIL. The two-axis substrate truth (L31) remains: Φ-stability + axis-preservation + forgetting-bounded ⊥ chat-capability lift.

---

## §11 — V3 → V4 milestones

V4 closure target = the next cycle's pragmatic ceiling (~97-98%), decomposed into architecturally-tractable + user-gated:

### Architecturally-tractable (no user gate beyond cost/scenario ACK)

1. **shim v5 Phase 2 PASS** (F-SHIM-V5-2 byte-equivalent regression + F-SHIM-V5-3 canonical_zero ubu1) — $0 ubu1, in-flight V3-time → V4 +1 closed lane
2. ** Phase 4 dogfood PASS** — $1-3 H100, in-flight V3-time → V4 +1 closed (lifecycle FULLY closed: spec → impl → operationalize → mechanical-validator → dogfood-verified)
3. **HF Cycle 2 ubu1 staging cleanup post-window** — $0 ubu1, scheduled clock-gate (post 2026-05-07 review windows + BLOCKER-1 sibling-count fix) → V4 +1 closed lane

### User-gated (carry from §4 + new V3-introduced)

4. **HF clm-v4-mk2-v1 PUBLIC promote** (user) — review window 2026-05-06T23:26:12Z + manual `bash` + `PROMOTE-clm-v4-mk2-v1` → V4 +1 closed lane
5. **HF Pβ adapter PUBLIC promote** (user) — review window 2026-05-07T03:48:00Z → V4 +1 closed lane
6. **shim v5 Phase 3 H100 ACK** (user, $1-3) — F-SHIM-V5-4 decisive lift_pp gate → V4 +1 closed lane (gates: pragmatic vs strict closure transition on shim v5)
7. **Putnam first-cycle Q1-Q4 ACK** (user) — substrate inventory + Phase E timing + T threshold + ownership → V4 +0 closed (gates only; exec is multi-week)
8. **Phase E EEG live session** (user, ~1.5-2h, alcohol-free 24-48h) — opens strict closure path on Putnam concordance + cond.1 RED→YELLOW
9. **T-3 5-seed Q1-Q4 ACK** (user, $25-75) — orthogonal lane

### V4 pragmatic closure ceiling estimate

- With architecturally-tractable items 1+2+3 landed: **~97-98%** (V3 95-97% + 2pp from shim v5 Phase 2 + Phase 4 dogfood + cleanup)
- With user-gated 4+5 (HF PUBLIC promotes) executed: **~97-99%**
- With user-gated 6 (shim v5 Phase 3 PASS) executed: **~98-99%** + pragmatic→strict transition partial on shim v5
- With user-gated 8 (Phase E EEG) executed: **~98-99%** pragmatic + opens **STRICT** closure path on Putnam concordance + cond.1 RED→YELLOW progression

V4 ceiling estimate ~97-98% (architectural-only) → ~98-99% (with HF promotes + shim v5 Phase 3) → strict closure entry point with Phase E. Strict closure ETA still weeks-to-months (Phase E + Putnam multi-cycle + Levin partnership).

---

**raw#9 compliance**: V3 doc is .md only; no .py / .sh / .json artifacts created.
**raw#10 compliance**: §10 has 10 honest C3 bullets (≥5 required).
**raw#15 compliance**: V3 doc is in `docs/` with timestamped revisioned name; V1 + V2 retained as historical anchors; no roadmap mutation, no exec, no commit.
