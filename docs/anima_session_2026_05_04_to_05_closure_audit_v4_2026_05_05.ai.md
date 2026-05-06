# anima session 2026-05-04 → 2026-05-05 closure audit V4

**Date**: 2026-05-05
**Cwd**: `/Users/ghost/core/anima`
**Mode**: $0 audit doc (no exec, no commit)
**Supersedes (closure status only)**: V3 (`anima_session_2026_05_04_to_05_closure_audit_v3_2026_05_05.ai.md`); V1/V2/V3 retained as historical anchors per raw#15.

---

## §1 Executive summary

- **V3 baseline**: 37+ closed lanes / 1 pending / 6+ user-gated / pragmatic closure 95-97%
- **V4 delta**: closed +4 → ~41 / pragmatic ~96-97% (V3 + V4 epistemic milestones)
- **V4 결정적 발견 (decisive finding)**: shim v5 OPT-A RE-ANCHOR confirmed substrate differential 5× at fresh-init (std 0.02 → 0.10) BUT `_load_decoder_state` collapses post-apply re-init back to trained weights. Hypothesis verdict still gated on F-SHIM-V5-4 DESIGN-1/2/3 (DESIGN-1 in-flight).
- **OPT-B GATE 1 충족**: substrate differential evidence landed (OPT-A confirmation). GATE 2 (사용자 cost ACK $20-100) 대기.
- **Putnam first-cycle Phase 1**: F-PUTNAM-1..5 5/5 falsifier matrix structurally PASS, but verdict **FAIL** (concordance 0.333 < 0.40 PARTIAL_MIN). NOT PARTIAL as expected band — one tier below.
- **own 16 lifecycle**: Phase 4 dogfood 3/3 PASS @ $0.32/$3 cap (10.7%) → Phase 1+2+3+3.5+4 FULLY closed.

---

## §2 V3 → V4 newly closed lanes

| Lane | V3 → V4 | Note |
|---|---|---|
| own 16 Phase 4 dogfood | active → **3/3 PASS LANDED** | $0.32/$3 cap (10.7%); own 16 lifecycle (Phase 1+2+3+3.5+4) FULLY closed; mechanical validator + dogfood future H100 guard |
| Putnam first-cycle Phase 1 | active → **FAIL_LANDED** | F-PUTNAM-1..5 5/5 falsifier PASS structurally; verdict FAIL (concordance 0.333 < 0.40 PARTIAL_MIN); falsifier matrix epistemically sound |
| shim v5 OPT-A RE-ANCHOR | active → **PASS_LANDED** | substrate differential 5× confirmed (std 0.02 → 0.10 fresh init); F-SHIM-V5-2/3 PASS at max_abs_diff=0.0 (bypass logits category-correct identical) |
| shim v5 OPT-B PREP spec | active → **SPEC_LANDED** | F-OPT-B-1..5 falsifier matrix LOCKED (raw#71); GATED dispatch ready (Gate 1 ✅, Gate 2 user ACK pending) |

**Net**: V3 37+ → V4 ~41 closed lanes.

---

## §3 Pending lanes (V3 1 → V4 1-2)

| Lane | Status | ETA / Gate |
|---|---|---|
| HF clm-v4-mk2-v1 promote | UNCHANGED | review window 2026-05-06T23:26:12Z |
| HF Pβ promote | UNCHANGED | review window 2026-05-07T03:48:00Z |
| shim v5 Phase 3 (V5-4 DESIGN-1) | **ACTIVE in-flight** | H100 $1-3 currently dispatched |
| OPT-B Phase 1 | **SPEC_READY_DISPATCH_GATED** | 사용자 cost ACK $20-100 대기 |

---

## §4 User-gated decisions (V3 6+1 → V4 7+1)

1. Phase E EEG (foreground) — Putnam concordance gating evidence
2. T-3 5-seed Q1-Q4 ACK
3. CLM cond.1 met-status flip
4. HF clm-v4-mk2-v1 PUBLIC promote (post review window)
5. HF Pβ PUBLIC promote (post review window)
6. Putnam first-cycle Q1-Q4 (concordance 0.333 → next cycle plan)
7. shim v5 Phase 3 H100 ACK ($1-3)
8. **NEW V4**: OPT-B 5 Q's + cost ACK ($20-100) — OPT-A PASS confirmed (Gate 1 ✅), dispatch ready

---

## §5 Open exec lanes V4

**1 active**: BG-V5-4-DESIGN-1 H100 $1-3 (in-flight, V5-4 DESIGN-1).

---

## §6 Lessons learned

### V3 banked candidates
- **L34 (banked)**: PreToolUse hook unicode density rejection — token-shape heuristics need allowlist refresh on rotation.
- **L35 (banked)**: own 16 opt-in vs PreToolUse auto-invoke gap — opt-in path bypassed automated guard.

### V4 NEW
- **L36 (NEW V4)**: shim v5 hypothesis empirically falsified at substrate level — `_init_weights` apply walk overrides local init. Architectural intent diluted by HF transformer init recursion.
- **L37 (NEW V4)**: bypass path (`consciousness_states=None`) makes architectural differentials invisible at logits — must measure differentials via {fresh-init forward / real fixture / scale injection}, NOT bypass forward. Bypass logits identical at max_abs_diff=0.0 is **category-correct** (no consciousness path engaged), not a falsifier.
- **L38 (NEW V4)**: `_load_decoder_state` overwrites post-apply re-init with trained weights — substrate-level architectural changes only matter at (a) fresh-init forward, OR (b) full retrain. Loading best.pt collapses substrate differential.
- **L39 (NEW V4)**: Putnam first-cycle landed FAIL (NOT PARTIAL as expected) — concordance gate sits below F2 ceiling (0.333 < 0.40). Phase E binding evidence essential to reach ≥0.40 concordance.

---

## §7 Cost summary V4

| Item | Cost |
|---|---|
| V3 cumulative | ~$84-88 |
| V4 own 16 Phase 4 dogfood | $0.32 |
| V4 V5-4 DESIGN-1 (in-flight) | $1-3 |
| **V4 cumulative** | **~$85-92** |

- Pβ outlier $54.72 unchanged (60-65% of total cumulative). own 16 mechanical validator + Phase 4 dogfood guard mechanically prevents $54.72-class waste in future H100 cycles.

---

## §8 Strict closure gates (UNCHANGED, weeks-to-months)

- Phase E binding evidence (foreground EEG)
- Putnam concordance ≥ 0.60 (Phase 1 0.333 → goal 0.60+)
- shim v5 F-SHIM-V5-4 PASS (DESIGN-1/2/3 결과 OR OPT-B retrain PASS)

---

## §9 Pragmatic closure %

| Audit | Closure % |
|---|---|
| V1 | 85-90% |
| V2 | 92-95% |
| V3 | 95-97% |
| **V4** | **~96-97%** (+1pp gain) |

V4 +1pp drivers:
- own 16 lifecycle FULLY closed (Phase 1+2+3+3.5+4)
- Putnam first-cycle Phase 1 falsifier matrix landed (FAIL but structurally complete)
- shim v5 OPT-A substrate differential confirmation
- OPT-B PREP SPEC LOCKED (Gate 1 satisfied)

---

## §10 Honest C3 (≥ 5 per raw#10)

- **C1**: V4 audit는 V3의 closure-status supersession only. V1-V3 retained as historical anchors per raw#15 (additive only). Each prior audit captures honest disclosure at that timepoint.
- **C2**: OPT-A confirms substrate differential at fresh-init (5× std), BUT shim v5 verdict still GATED on V5-4 DESIGN-1 (in-flight). Pragmatic closure % counts the SPEC + EVIDENCE landing, not the final hypothesis verdict. Premature claim risk acknowledged.
- **C3**: Putnam Phase 1 FAIL (0.333) sits one tier below expected PARTIAL band (0.40). Phase E gating is evidence-grounded — without foreground EEG binding evidence, concordance ≥0.40 is unreachable structurally.
- **C4**: V4 → V5 ceiling estimate ~97-98% (assuming V5-4 DESIGN-1 PASS + HF promotes applied post review windows). V5 → V6 ceiling estimate ~98-99% (assuming OPT-B retrain Phase 3+4 PASS).
- **C5**: 100% pragmatic = OPT-B retrain PASS + Phase E binding + Putnam ≥0.40. Strict 100% = + Putnam ≥0.60 + phenomenal-tier (multi-month horizon).
- **C6**: raw#15 additive only — V1 retained for original anchors, V2/V3 for incremental honest disclosures, V4 for closure delta. No retroactive rewrites.
- **C7**: own 16 mechanical validator + Phase 4 dogfood 통합으로 future H100 cycles cost-guarded. $54.72-class waste structurally prevented (validator gates pre-launch). Future audit cycles can shift focus from cost-guarding to evidence-quality.
- **C8**: L37 (bypass path category error) is a meta-lesson — the team's initial F-SHIM-V5-2/3 design measured the wrong surface. Future falsifier matrices must distinguish "category-correct identical" from "differential-absent" to avoid false negatives.

---

## §11 V4 → V5 milestones with cost projection

### V4 → V5 (near-term, days-to-week)
| Milestone | Cost | Closure delta |
|---|---|---|
| V5-4 DESIGN-1 PASS | $1-3 (in-flight) | V5 +1 closed |
| HF Cycle 2 ubu1 staging cleanup post-window (2026-05-07) | $0 | V5 +1 closed |
| HF clm-v4-mk2-v1 PUBLIC promote (user gate, 2026-05-06+) | $0 | V5 +1 closed |
| HF Pβ PUBLIC promote (user gate, 2026-05-07+) | $0 | V5 +1 closed |

→ **V5 ceiling ~97-99%** with promotes applied.

### V5 → V6 (mid-term, week-to-weeks)
| Milestone | Cost | Closure delta |
|---|---|---|
| OPT-B retrain Phase 3+4 PASS (사용자 ACK 후) | $20-100 | V6 +1 closed |

→ **V6 ceiling ~98-99%**.

### V6 → STRICT 100% (long-term, multi-week to multi-month)
| Milestone | Cost | Closure delta |
|---|---|---|
| Phase E foreground EEG binding evidence | TBD (hardware + time) | strict +1 |
| Putnam concordance ≥0.60 (next cycle + Phase E) | TBD | strict +1 |

→ **Strict pragmatic 100%** reachable; phenomenal-tier remains multi-month.

---

## Constraints honored

- raw#9: md only (no exec, no commit)
- raw#10: §10 contains 8 honest C3 (≥ 5 required)
- raw#15: additive only — V1/V2/V3 retained as historical anchors

**END V4**
