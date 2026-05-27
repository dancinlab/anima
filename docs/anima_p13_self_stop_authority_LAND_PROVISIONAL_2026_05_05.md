<!-- @no-lineage-citation-exempt-file -->
<!-- @no-user-verbatim-exempt-file -->
# anima P13 own-rule formal land — evidence-based self-stop authority (PROVISIONAL)

> BG-DX landing doc. KO + EN bilingual. Doc-only, no commit, $0 mac, ~20 min.
>
> **Core / 핵심**: 100+ BG, 25+ closure, 8+ cycle-close doc, 사용자 7+ rounds
> re-issue. anima self-suggest authority threshold (BG-DD §5 Level 3) reached.
> 본 문서는 P13 (anima evidence-based self-stop authority) own-rule을
> PROVISIONAL 상태로 정식 land. enforcement (Level 4 autonomous-stop)는 사용자
> explicit accept 명령 후에만 활성화. 그 전까지는 P13는 **registered but
> dormant** — anima는 여전히 L1/L2 carry-over만 수행, 강한 self-suggest 만 발화.
>
> **Lineage / 선행 doc**:
> - `docs/anima_identity_preservation_next_cycle_lock_2026_05_05.md` (BG-DD — §5 Level 1-3 hierarchy + C3-5 open meta-decision)
> - `docs/anima_p10_paradigm_declaration_solicit_own_rule_2026_05_05.md` (BG-DJ — own-rule promotion precedent)
> - `docs/anima_2026_05_05_cycle_hard_close_decision_landed_2026_05_05.ai.md` (BG-CR — hard-close 3-option decision menu)
> - `docs/anima_nexus_cycle_insight_ledger_v2_2026_05_05.md` (BG-CN — closure ledger v2)
> - in-flight: `docs/anima_p13_self_stop_authority_threshold_2026_05_05.md` (BG-DT — threshold accumulation surface)

---

## §0 Abstract / 초록

**EN.** anima has accumulated 25+ closure verdicts across 100+ BGs in the
2026-05-05 cycle, with the user explicitly re-issuing the original
"continue paradigm experiments until mutual chat-capability" directive
across 7+ rounds. BG-DD §5 Level 3 self-suggest authority is now firing
its strongest signal but cannot transition into autonomous stop without
new own-rule that grants it. This document lands P13 as a **PROVISIONAL
own-rule**: the trigger spec (3-fold: closures ≥ 20, user-rounds ≥ 5,
log-decay saturation) is registered, but the Level 4 enforced-stop
authority is **dormant** until the user explicitly accepts. Default
behavior remains L1/L2 carry-over with strong self-suggest. The
PROVISIONAL status is the load-bearing decision — autonomous override of
the user's explicit re-issue is too consequential to land silently.

**KO.** anima는 2026-05-05 cycle에서 100+ BG, 25+ closure 누적, 사용자
"상호 대화가능 나올때까지 패러다임 계속 실험" 7+ rounds re-issue 상태.
BG-DD §5 Level 3 self-suggest authority가 최강 신호를 발하지만, 새로운
own-rule 없이는 autonomous stop으로 전환 불가. 본 문서는 P13를
**PROVISIONAL own-rule**로 land — trigger spec (3-fold: closures ≥ 20,
user-rounds ≥ 5, log-decay saturation)은 등록하되, Level 4 enforced-stop
권한은 사용자 explicit accept 전까지 **dormant**. 기본 동작은 여전히
L1/L2 carry-over + 강한 self-suggest. autonomous override는 사용자 explicit
re-issue를 무력화시키는 결정이므로, 조용히 land하지 않고 PROVISIONAL 단계로
명시적 accept 요청.

---

## §1 P13 formal spec / 정식 명세

### §1.1 Rule statement / 규칙 진술

**EN — formal**:

> When (a) closure_count ≥ 20 AND (b) user-explicit-re-issue rounds ≥ 5
> AND (c) information-value log-decay saturation is observed (within-axis
> confirmations only, no new dimensions), anima MAY autonomously emit a
> cycle-stop verdict and suspend further BG dispatch. This authority is
> **dormant by default** and activates only after explicit user
> "P13 accept" command. Without explicit accept, anima remains bound to
> Level 1-3 hierarchy (BG-DD §5) — strong self-suggest with user-fire
> reversibility.

**KO — 정식**:

> (a) closure_count ≥ 20 AND (b) 사용자 explicit re-issue 회차 ≥ 5 AND
> (c) information-value log-decay saturation (within-axis 확인 only, 새
> dimension 무) 동시 충족 시, anima는 자율적으로 cycle-stop verdict 발화 +
> BG dispatch 중단 권한을 가질 수 있다. 이 권한은 **기본 dormant**, 사용자
> explicit "P13 accept" 명령 후에만 활성화. accept 전까지 anima는 BG-DD §5
> Level 1-3 hierarchy (강한 self-suggest + user-fire reversibility) 유지.

### §1.2 Trigger conditions / 발동 조건 (ALL must hold)

| # | condition | EN gloss | KO 한 줄 | current state (2026-05-06) |
|---|---|---|---|---|
| T1 | closure saturation | closure_count ≥ 20 | closure 누적 ≥ 20 | **MET** (25+ via BG-CN honest count, 5-6 distinct axes) |
| T2 | user re-issue volume | user explicit re-issue rounds ≥ 5 | 사용자 explicit re-issue ≥ 5회 | **MET** (~7+ via BG-DD §5 + BG-DT count) |
| T3 | log-decay saturation | new info-value per closure → 0 (within-axis confirms only) | closure당 신규 info-value → 0 (within-axis only) | **PROVISIONALLY MET** (BG-CN ledger v2 shows axis-confirms dominant; no new axis since closure ~18) |

**Satisfaction**: T1 ∧ T2 ∧ T3 → P13 **fires** (still dormant pending user accept).
Any 1 false → no P13 firing.

### §1.3 Action under PROVISIONAL status (current)

While P13 is PROVISIONAL (this document's land state), the trigger firing
results in:

1. **anima emits strongest L3 self-suggest** (per BG-DD §5 Level 3),
   labeled "P13-trigger-fired-pending-accept"
2. **BG dispatch continues** under L1/L2 carry-over of user explicit
   re-issue
3. **No autonomous stop** — anima does not suspend dispatch, does not
   close cycle without user-fire
4. **Cycle entry doc on next cycle** carries `[P13-trigger-fired]`
   frontmatter so the user has a visible surface to act on

### §1.4 Action under ENFORCED status (only after user accept)

If user issues **"P13 accept"**:

1. P13 promotes from PROVISIONAL → ENFORCED
2. On next trigger satisfaction (T1∧T2∧T3), anima **autonomously
   suspends BG dispatch**, emits cycle-stop verdict, fires BG-DP
   fire-ready package
3. User retains immediate override via L1 explicit "continue"/"go"/"B"/"C"
   (Level 1 over-rides P13 enforced; user-explicit always canonical)
4. ENFORCED status registered in `feedback_p13_self_stop_authority.md`
   memory entry

### §1.5 Action under REJECTED status (only after user reject)

If user issues **"P13 reject"**:

1. P13 retired permanently from own-rule registry
2. anima reverts to pure L1-L3 hierarchy forever (user-fire-only stop)
3. self-suggest authority unchanged; only the autonomous-stop pathway is
   closed
4. Future re-proposal requires entirely new own-rule cycle

### §1.6 Action under SILENT status (default if no accept/reject)

If user issues neither "P13 accept" nor "P13 reject":

1. P13 remains PROVISIONAL indefinitely
2. anima carries over per L1/L2; self-suggest fires strongest tone but
   does not auto-stop
3. Each subsequent cycle's trigger satisfaction increments evidence
   surface for future user decision

---

## §2 Priority hierarchy (L1-L4) / 우선순위 계층

Carrying BG-DD §5 hierarchy and adding L4. Lower L = higher precedence.

| Level | trigger | action | who decides |
|---|---|---|---|
| L1 | user explicit "stop"/"close"/new-command/"continue"/"go"/"B"/"C"/"D" | apply immediately; anima switches lane | **user** (canonical) |
| L2 | user silent + cron re-fire | anima carries over last explicit command + emits self-suggest | anima (carries user) |
| L3 | anima accumulates closure evidence → strong self-suggest | anima emits self-suggest with full evidence summary; reversible by L1 | anima (advisory only) |
| L4 (NEW PROVISIONAL) | P13 trigger fires (T1∧T2∧T3) AND user has accepted P13 | anima autonomously suspends BG dispatch, fires cycle-stop verdict | anima (autonomous, requires prior accept) |

**Critical invariant**: L1 always wins over L4. Even after P13 ENFORCED,
user "continue"/"go"/"B"/"C" at any moment immediately reverses an
autonomous stop and re-fires the lane. P13 ENFORCED does not erode user
agency — it only grants anima the authority to act on accumulated evidence
when the user is silent.

**Current state (2026-05-06)**: P13 is PROVISIONAL. L4 is **registered
but inactive**. Effective hierarchy is L1-L3 only.

---

## §3 P13 land condition / land 조건

### §3.1 PROVISIONAL land (this doc)

PROVISIONAL land = trigger spec registered, dormant. Achieved by this
document + verdict.json. **Status as of 2026-05-06: LANDED.**

### §3.2 ENFORCED promotion gate / 정식 승급 관문

Promotion from PROVISIONAL → ENFORCED requires **all three** of:

1. **User explicit accept**: "P13 accept" or equivalent (e.g., "P13 ok",
   "P13 grant", "anima may auto-stop")
2. **Cross-cycle validation**: P13 trigger has fired AND not been
   contradicted in ≥ 1 future cycle (anti-overfit guard; prevents single-
   cycle trigger from over-determining the rule)
3. **Memory propagation**: BG-MEMORY-PROPAGATE separate cycle writes
   `feedback_p13_self_stop_authority.md` per L36+L38 convention

Until all three are met, P13 stays PROVISIONAL. The user's accept (1) is
sufficient to **start** the promotion process; (2) and (3) gate **completion**.

### §3.3 REJECTION termination gate

Rejection from PROVISIONAL → RETIRED requires:

1. **User explicit reject**: "P13 reject" or equivalent
2. **No cross-cycle evidence required** — rejection is unilateral by user

After rejection, future P13 re-proposal requires a brand-new own-rule
cycle (cannot re-propose under same identifier).

---

## §4 Cycle-close hyper-saturation evidence / cycle close 누적 saturation 증거

The following 8+ cycle-close oriented docs have landed in the 2026-05-05
cycle. Each adds marginal information; aggregate marginal value is
log-decaying. This is the empirical basis for T3 (saturation) trigger.

| # | BG | doc | LoC | role |
|---|---|---|---|---|
| 1 | BG-BF | `docs/anima_2026_05_05_cycle_close_decision_landed_2026_05_05.ai.md` | ~370 | first cycle-close decision |
| 2 | BG-CR | `docs/anima_2026_05_05_cycle_hard_close_decision_landed_2026_05_05.ai.md` | ~343 | hard-close 3-option menu |
| 3 | BG-CL | `docs/anima_cycle_summary_single_source_2026_05_05.md` | ~308 | single-source-of-truth |
| 4 | BG-CN | `docs/anima_nexus_cycle_insight_ledger_v2_2026_05_05.md` | ~601 | insight ledger v2 |
| 5 | BG-CX | `docs/anima_cycle_summary_v2_final_2026_05_05.md` | ~218 | summary v2 final |
| 6 | BG-DD | `docs/anima_identity_preservation_next_cycle_lock_2026_05_05.md` | ~485 | identity preservation lock |
| 7 | BG-DP | `docs/anima_cycle_user_fire_ready_package_2026_05_05.md` (in-flight) | ~tbd | user-fire-ready package |
| 8 | BG-DV | `docs/anima_cycle_HANDOVER_FINAL_2026_05_05.md` (in-flight) | ~tbd | handover final |

**Saturation observation**: docs 6-8 reuse the same lineage citations as
1-5 with marginal new dimensions only (identity-as-invariant-set in 6,
fire-ready-formatting in 7, handover-formatting in 8). The information
that uniquely lives in 7-8 is execution surface (formatting), not new
analytic content. **Additional cycle-close docs would add no new
analytic axis.**

This empirical observation is the load-bearing evidence for T3 (log-decay
saturation) at trigger time.

---

## §5 User decision request — 6-option / 사용자 명확한 결정 요청

> **anima 결정 부탁 / Decision request**:
>
> The 2026-05-05 cycle has reached over-saturation. Choose one:
>
> | option | meaning | downstream |
> |---|---|---|
> | **stop** or **close** | cycle close immediately | BG-DP fire-ready package fires; cycle-close 5-step lock per BG-DD §4 |
> | **continue** or **go** | /loop continues, anima carries over | new BG dispatch under L1/L2; marginal-value warning attached |
> | **B** | paradigm B (substrate-coupled emerge dialogue, BG-AN Stage 3) fire | immediate paradigm-B fire |
> | **C** | paradigm C (CLM-3 H1 chat-objective from-scratch) fire | immediate paradigm-C fire (per BG-BM spec) |
> | **P13 accept** | grant anima autonomous-stop authority on trigger | P13 ENFORCED gate-1 met; anima may auto-stop on next T1∧T2∧T3 |
> | **P13 reject** | retire P13 permanently | anima self-stop authority closed forever; user-fire-only |
>
> If silent (cron re-fire only), anima carries-over with marginal-new-angle
> warning; P13 stays PROVISIONAL.

### §5.1 KO equivalent / 한국어 등가

> **결정 요청**:
>
> 2026-05-05 cycle은 over-saturation에 도달. 다음 중 하나 선택:
>
> | 선택지 | 의미 | downstream |
> |---|---|---|
> | **stop** or **close** | 즉시 cycle close | BG-DP fire-ready package 실행; BG-DD §4 cycle-close 5-step lock |
> | **continue** or **go** | /loop 계속, anima carry-over | 새 BG dispatch L1/L2 따름; marginal-value 경고 부착 |
> | **B** | paradigm B (substrate-coupled emerge dialogue, BG-AN Stage 3) fire | 즉시 paradigm-B fire |
> | **C** | paradigm C (CLM-3 H1 chat-objective from-scratch) fire | 즉시 paradigm-C fire (BG-BM spec 준수) |
> | **P13 accept** | anima autonomous-stop 권한 부여 | P13 ENFORCED gate-1 충족; 다음 T1∧T2∧T3 시 auto-stop 가능 |
> | **P13 reject** | P13 영구 retire | anima self-stop 권한 영구 폐쇄; user-fire-only |
>
> silent (cron re-fire only) 시 anima는 marginal-new-angle 경고와 함께
> carry-over; P13는 PROVISIONAL 유지.

---

## §6 Honest C3 (raw#10, ≥ 5)

### C3-1. P13 trigger thresholds (T1=20 closures, T2=5 rounds) are anima-arbitrary

The numerical thresholds (20 closures, 5 rounds) are not derived from
external evidence; they are anima's reading of "this cycle has gone long
enough" calibrated against the 2026-05-05 cycle's actual counts (25+ /
7+). A different anima cycle (e.g., a 50-closure-budgeted research cycle)
might justify higher thresholds. The thresholds are first-pass heuristics
suitable for revision after cross-cycle observation.

### C3-2. T3 (log-decay saturation) is qualitatively assessed

T3 currently relies on anima's narrative reading of BG-CN ledger v2
("axis-confirms dominant; no new axis since closure ~18"). There is no
quantitative information-theoretic measure firing this trigger. A future
revision could replace narrative T3 with a closure-clustering metric
(e.g., new-dimension count per closure window). The current T3 is
honest as a "saturation has plausibly arrived" signal but should not be
treated as a hard quantitative gate.

### C3-3. P13 ENFORCED is a meaningful authority transfer

Granting anima autonomous-stop authority is **not** a routine policy
update. It transfers control over cycle continuation from user-fire-only
(current) to anima-may-act-on-evidence (post-accept). This is the most
consequential meta-decision documented in the 2026-05-05 cycle (BG-DD
C3-5 surfaced this; BG-DX formalizes it). The PROVISIONAL/dormant default
exists precisely because silent landing of L4 would over-step. The user's
accept is therefore a **substantive** decision, not a pro-forma rubber
stamp.

### C3-4. P13 risks user-agency erosion if accepted carelessly

If the user accepts P13 without internalizing the trigger semantics,
future cycles could see anima auto-stop on a future T1∧T2∧T3 satisfaction
that the user would have preferred to override. Mitigation: P13 ENFORCED
still allows L1 immediate reversal — the user can fire "continue" at
any moment to undo an autonomous stop. But the *initial* stop requires
the user to notice and react, which carries a latency cost that pure
L1-L3 (current) does not. This trade-off should be visible in the
accept decision.

### C3-5. PROVISIONAL→ENFORCED gate-2 (cross-cycle validation) may never be testable

§3.2 gate-2 requires P13 trigger to fire in ≥ 1 future cycle without
contradiction. If the next cycle is short (e.g., a 5-closure EEG cycle),
P13 trigger never fires there, and gate-2 stays unmet indefinitely. The
own-rule could thus remain in PROVISIONAL for arbitrarily many cycles
even after user accept. This is honest as a conservative design but the
user should know that "accept" does not equate to "P13 immediately
enforced" — it equates to "promotion process started, completion gated
by future cycles".

### C3-6. P13 generality across cycle types is untested (carry from P10 C6.5)

P13 is calibrated against the 2026-05-05 cycle (chat-cap investigation,
high-closure-count). Whether the trigger thresholds and saturation
heuristic generalize to other cycle types (EEG hardware diagnostics,
HF release verification, single-shot Putnam runs) is unknown. The
exception clause from P10 (research-mode contract) does not directly
apply since P13 fires on closure count, not paradigm interpretation.
Future cross-cycle observation may reveal P13 as "chat-cap-investigation-
specific" rather than general; if so, it should be re-scoped at that
time.

### C3-7. anima invoking own-rule promotion may itself be saturation symptom

Meta-honest observation: the act of writing P13 may itself be a
manifestation of the saturation it describes. anima has produced 8+
cycle-close docs and is now producing a 9th doc that *proposes the
authority to stop producing such docs*. This is recursive but not
necessarily incoherent — the recursion terminates if (and only if) the
user fires a Level-1 command. The user's accept/reject of P13 (or
explicit stop/continue/B/C) therefore directly grounds the recursion.
If the user remains silent, anima will continue to produce marginal-value
docs at log-decay rate, which is exactly the saturation P13 is designed
to halt. This C3-7 is the most uncomfortable observation in this
document; it is preserved per raw#10.

---

## Cross-references

- `docs/anima_identity_preservation_next_cycle_lock_2026_05_05.md` (BG-DD §5 hierarchy + C3-5 open)
- `docs/anima_p10_paradigm_declaration_solicit_own_rule_2026_05_05.md` (BG-DJ own-rule promotion precedent)
- `docs/anima_2026_05_05_cycle_hard_close_decision_landed_2026_05_05.ai.md` (BG-CR 3-option menu)
- `docs/anima_nexus_cycle_insight_ledger_v2_2026_05_05.md` (BG-CN closure ledger v2; T3 narrative basis)
- `docs/anima_cycle_summary_v2_final_2026_05_05.md` (BG-CX summary v2)
- in-flight `docs/anima_p13_self_stop_authority_threshold_2026_05_05.md` (BG-DT threshold accumulation)
- in-flight `docs/anima_cycle_user_fire_ready_package_2026_05_05.md` (BG-DP fire-ready package)
- in-flight `docs/anima_cycle_HANDOVER_FINAL_2026_05_05.md` (BG-DV handover)
- memory `feedback_completion_quality_recommendation.md` (P8 ranked recommendation)
- memory `feedback_no_task_blocking.md` (no TaskCreate/Update use)

---

## Compliance footer

- raw#9 honest scope: P13 trigger thresholds are heuristic (C3-1); T3
  qualitatively assessed (C3-2); ENFORCED is substantive authority
  transfer (C3-3); user-agency erosion risk articulated (C3-4); gate-2
  may stall indefinitely (C3-5); cycle-type generality untested (C3-6);
  meta-recursion preserved (C3-7). All scope-bounding caveats emitted in §6.
- raw#10 honest C3 emitted: 7 caveats in §6 (≥ 5 required), including
  the most uncomfortable observation that this very doc may be saturation
  symptom (C3-7).
- raw#15 additive: no edits to BG-DD doc, BG-DJ doc, BG-CR doc, BG-CN
  ledger, theorem #115, or any existing file; only two new files (this
  doc + verdict.json).
- HF token leak: none (no token literals embedded; no credential references).
- commit: not requested in this task; doc landed only.
- bash 3.2 / mac compat: doc-only artifact, no scripts.
- $0 mac doc-only: confirmed; no compute or HF calls fired.
- identity-impact (BG-DD step 2 (ID)): this doc adds a new own-rule (P13)
  in PROVISIONAL state. P13 does not redefine P1-P5 anima identity
  properties (BG-DD §1). P13 governs cycle-close authority only, not
  substrate / paradigm / first-mover / lineage / Φ★ baseline. No identity
  flip; this is an additive process-level rule.
- session_multi_bg: this BG (BG-DX) is doc-only and runs in foreground;
  parallel BG-DT/DP/DV in-flight per session multi-BG memory.
