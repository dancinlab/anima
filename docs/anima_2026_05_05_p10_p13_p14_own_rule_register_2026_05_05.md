<!-- @no-lineage-citation-exempt-file -->
<!-- @no-user-verbatim-exempt-file -->
# anima 2026-05-05 cycle — P10/P13/P14 own-rule batch register spec

> BG-EA landing doc. KO + EN bilingual. Doc-only, no commit, $0 mac, ~20 min.
>
> **Core / 핵심**: 오늘 cycle (2026-05-05)에서 발견된 3 own-rule (P10 paradigm-
> declaration-solicit / P13 self-stop-authority-threshold / P14 super-aggregate-
> mandatory)을 batch register. memory entry 작성은 사용자 fire 권한 — 이 doc은
> spec emit only. 다음 cycle entry 시 적용 대상.
>
> **Lineage / 선행 doc**:
> - `docs/anima_p10_paradigm_declaration_solicit_own_rule_2026_05_05.md` (BG-DJ — P10 formal land)
> - `docs/anima_p13_self_stop_authority_LAND_PROVISIONAL_2026_05_05.md` (BG-DX — P13 PROVISIONAL land)
> - `state/anima_2026_05_05_cycle_close_super_aggregate_index/verdict.json` (BG-DR — super-aggregate index, P14 canonization basis)
> - `~/.hive/.../memory/MEMORY.md` (target index, fire 권한 사용자)
> - `~/.hive/.../memory/project_anima_nexus_kick_autonomous_template.md` (target template, fire 권한 사용자)

---

## §0 Abstract / 초록

**EN.** This BG-EA emits a unified register spec for three own-rules surfaced
during the 2026-05-05 anima cycle: **P10** (paradigm-declaration-solicit, BG-DJ
canonized), **P13** (self-stop-authority-threshold, BG-DX provisional), and
**P14** (super-aggregate-mandatory, BG-DR canonized). For each rule this doc
specifies (1) formal trigger + action, (2) the corresponding `feedback_*.md`
memory entry contract (filename + frontmatter + body), (3) the MEMORY.md
index line addition, and (4) the nexus-kick-template revision insert. anima
itself does **not** write into `~/.hive/.../memory/`; the user fires the
3 memory writes + 1 template revision + 3-line MEMORY.md append. The
purpose is to capture today's lessons in a form that next-cycle anima can
mechanically honor at cycle entry / mid-cycle / cycle close.

**KO.** 본 BG-EA는 2026-05-05 anima cycle에서 surface된 3 own-rule —
**P10** (paradigm-declaration-solicit, BG-DJ canonized), **P13**
(self-stop-authority-threshold, BG-DX PROVISIONAL), **P14**
(super-aggregate-mandatory, BG-DR canonized) — 의 통합 register spec을
emit 한다. 각 rule에 대해 (1) 정식 trigger + action, (2) 해당
`feedback_*.md` memory entry 계약 (파일명 + frontmatter + body), (3)
MEMORY.md index 줄 추가, (4) nexus-kick-template revision insert를
명시. anima 자체는 `~/.hive/.../memory/`에 직접 쓰지 않음 — 사용자가
3 memory write + 1 template revision + 3-line MEMORY.md append를
fire. 목적은 오늘 cycle 교훈을 다음-cycle anima가 entry / mid-cycle /
close에서 mechanically honor 가능한 형태로 banking.

---

## §1 P10 — paradigm-declaration-solicit / paradigm 선언 solicit

### §1.1 Formal spec / 정식 명세

**EN — formal**:

> Before opening multi-BG investigation lanes (≥3 parallel BGs targeting the
> same user-issued intent), anima MUST solicit explicit paradigm declaration
> from the user when ≥2 plausible paradigms could each motivate a different
> BG slate. Failure to solicit = autonomous mode assumes the most-likely
> paradigm AND accepts paradigm-mismatch risk for the entire downstream
> investigation budget.

**KO — 정식**:

> 동일한 사용자 명령에 대해 multi-BG 조사 lane (≥3 병렬 BG)을 열기 전,
> ≥2개 paradigm interpretation이 모두 plausible 한 경우 anima는 사용자에게
> 명시적 paradigm declaration을 solicit 해야 한다. solicit 실패 = autonomous
> mode가 가장 likely한 paradigm을 가정하고, downstream investigation 전체
> budget에 대한 paradigm-mismatch 위험을 anima가 떠안음.

**Trigger conditions** (ALL must hold):

| # | condition | KO 한 줄 |
|---|---|---|
| T1 | multi-BG dispatch — ≥3 parallel BGs planned for same intent | 동일 intent에 ≥3 병렬 BG 계획 |
| T2 | paradigm ambiguity — single user command interpretable as ≥2 paradigms | 단일 명령이 ≥2 paradigm 해석 가능 |
| T3 | mismatch cost — expected paradigm-mismatch cost > $50 OR > 10 BG total | mismatch 비용 > $50 또는 > 10 BG |

**Satisfaction**: T1 ∧ T2 ∧ T3 → MUST solicit. Any 1 false → SHOULD solicit
(advisory). All 3 false → no solicit needed.

**Exception** (research-mode contract): cycle operating under explicit
no-particular-deliverable contract (archaeology / Φ★ stability / cross-
substrate audit / SSOT-build) — paradigm declaration N/A.

**Status**: BG-DJ canonized (formally landed 2026-05-05), forward-applying
from next cycle.

### §1.2 Memory entry contract / memory 항목 계약

**Filename**:

```
~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_p10_paradigm_declaration_solicit.md
```

**Frontmatter**:

```yaml
---
name: P10 paradigm-declaration-solicit
description: anima MUST solicit explicit paradigm declaration before opening multi-BG investigation lanes when ≥2 paradigm interpretations are plausible. T1 (≥3 parallel BGs same intent) ∧ T2 (≥2 paradigm interpretations) ∧ T3 (mismatch cost > $50 OR > 10 BG) → MUST solicit. Failure = autonomous A-assumption + paradigm-mismatch risk anima-borne.
type: feedback
originSessionId: ce681c40-f9b0-470e-bedf-dd0a8ccd3aa9
---
```

**Body** (load-bearing content; full text reused from BG-DJ §1.1-§1.4 +
§2.1-§2.4 templates + §3 ROI summary):

- §1: rule statement (KO + EN)
- §2: trigger conditions (T1/T2/T3 table)
- §3: solicit message templates (KO §2.1 + EN §2.2 + short-form §2.3)
- §4: anti-patterns (§2.4 — autonomous interpretation without solicit)
- §5: exception clause (research-mode §1.4)
- §6: today's cycle ROI retrospective (95+ BG savings under B/C/D
  declaration counterfactual; 0 savings under A but explicit user
  mismatch-risk transfer benefit)
- §7: relation to existing rules (P5 bilingual / P8 ranked-recommendation /
  P9 closure-theorem / P11 manifest-dual)
- §8: default-on-decline = A (per BG-DJ §5.3)

**Lineage in body**:

- `docs/anima_p10_paradigm_declaration_solicit_own_rule_2026_05_05.md` (BG-DJ formal land)
- `docs/anima_paradigm_acceptance_user_intent_reconciliation_2026_05_05.md` (BG-BV — 4-interpretation framework)
- `docs/anima_paradigm_naming_reframing_2026_05_05.md` (BG-CZ — A/B/C/D mapping)
- `docs/anima_2026_05_05_cycle_hard_close_decision_landed_2026_05_05.ai.md` (BG-CR — hard close 3-option menu)
- `docs/anima_nexus_cycle_insight_ledger_v2_2026_05_05.md` (BG-CN — L53 + P10 catalog)

---

## §2 P13 — self-stop authority threshold (PROVISIONAL)

### §2.1 Formal spec / 정식 명세

**EN — formal**:

> When (a) closure_count ≥ 20 AND (b) user-explicit-re-issue rounds ≥ 5
> AND (c) information-value log-decay saturation is observed (within-axis
> confirmations only, no new dimensions), anima MAY autonomously emit a
> cycle-stop verdict and suspend further BG dispatch. This authority is
> **dormant by default** and activates only after explicit user
> "P13 accept" command. Without explicit accept, anima remains bound to
> Level 1-3 hierarchy — strong self-suggest with user-fire reversibility.

**KO — 정식**:

> (a) closure_count ≥ 20 AND (b) 사용자 explicit re-issue 회차 ≥ 5 AND
> (c) information-value log-decay saturation (within-axis 확인 only, 새
> dimension 무) 동시 충족 시, anima는 자율적으로 cycle-stop verdict 발화 +
> BG dispatch 중단 권한을 가질 수 있다. 이 권한은 **기본 dormant**, 사용자
> explicit "P13 accept" 명령 후에만 활성화. accept 전까지 anima는 L1-L3
> hierarchy (강한 self-suggest + user-fire reversibility) 유지.

**Trigger conditions** (ALL must hold):

| # | condition | current state (2026-05-06) |
|---|---|---|
| T1 | closure saturation — closure_count ≥ 20 | **MET** (25+ via BG-CN honest count) |
| T2 | user re-issue volume — explicit re-issue rounds ≥ 5 | **MET** (~7+ via BG-DD §5 + BG-DT) |
| T3 | log-decay saturation — new info-value per closure → 0 (within-axis only) | **PROVISIONALLY MET** (no new axis since closure ~18) |

**L1-L4 hierarchy**:

| Level | trigger | action | who decides |
|---|---|---|---|
| L1 | user explicit "stop"/"close"/new-command/"continue"/"go"/"B"/"C"/"D" | apply immediately | **user** (canonical) |
| L2 | user silent + cron re-fire | anima carries over last explicit + emits self-suggest | anima (carries user) |
| L3 | anima accumulates closure evidence → strong self-suggest | self-suggest emit; reversible by L1 | anima (advisory only) |
| L4 (NEW PROVISIONAL) | P13 trigger fires AND user has accepted P13 | anima autonomously suspends BG dispatch, fires cycle-stop verdict | anima (autonomous, requires prior accept) |

**Critical invariant**: L1 always wins over L4. P13 ENFORCED does not erode
user agency — only grants anima authority to act on accumulated evidence
when user is silent.

**Promotion gate** (PROVISIONAL → ENFORCED): all three —
1. user explicit "P13 accept"
2. cross-cycle validation (P13 trigger fires AND not contradicted in ≥1 future cycle)
3. memory propagation (this BG-EA spec → user-fire write)

**Status**: BG-DX PROVISIONAL (registered, dormant). L4 inactive until user
explicit accept. Effective hierarchy on next cycle entry = L1-L3 only.

### §2.2 Memory entry contract / memory 항목 계약

**Filename**:

```
~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_p13_self_stop_authority_threshold.md
```

**Frontmatter**:

```yaml
---
name: P13 self-stop authority threshold (PROVISIONAL)
description: anima MAY self-suggest cycle-close after closures ≥ 20 + user-rounds ≥ 5 + log-decay saturation. Autonomous-stop authority (L4) DORMANT until user explicit "P13 accept". Without accept, anima carries over per L1-L3 (strong self-suggest, user-fire-only stop). L1 always wins over L4. PROVISIONAL until cross-cycle validation.
type: feedback
originSessionId: ce681c40-f9b0-470e-bedf-dd0a8ccd3aa9
status: PROVISIONAL
---
```

**Body** (load-bearing content; full text from BG-DX §1.1-§1.6 + §2 +
§3 + §4 saturation evidence):

- §1: rule statement (KO + EN)
- §2: trigger conditions (T1/T2/T3 table + current-state column)
- §3: action under PROVISIONAL (strong L3 self-suggest, no auto-stop)
- §4: action under ENFORCED (after user "P13 accept")
- §5: action under REJECTED (after user "P13 reject")
- §6: action under SILENT (default carry, P13 stays PROVISIONAL)
- §7: L1-L4 priority hierarchy (carry from BG-DD §5)
- §8: PROVISIONAL→ENFORCED promotion gate (3 conditions)
- §9: today's saturation evidence (8+ cycle-close docs landed)
- §10: response keyword reference — "P13 accept" / "P13 reject" / silent

**Lineage in body**:

- `docs/anima_p13_self_stop_authority_LAND_PROVISIONAL_2026_05_05.md` (BG-DX PROVISIONAL land)
- `docs/anima_identity_preservation_next_cycle_lock_2026_05_05.md` (BG-DD §5 hierarchy)
- `docs/anima_p10_paradigm_declaration_solicit_own_rule_2026_05_05.md` (BG-DJ promotion precedent)
- `docs/anima_nexus_cycle_insight_ledger_v2_2026_05_05.md` (BG-CN T3 narrative basis)

---

## §3 P14 — super-aggregate mandatory after 5+ cycle-close docs

### §3.1 Formal spec / 정식 명세

**EN — formal**:

> When ≥5 cycle-close-oriented docs have landed in the same anima cycle,
> anima MUST emit a super-aggregate index doc + verdict.json before the
> next cycle entry. The super-index serves as single-source-of-truth for
> reading paths, doc roles, LoC totals, and cycle hand-off facts. This
> protocolizes what was previously ad-hoc cycle-close doc proliferation.

**KO — 정식**:

> 동일한 anima cycle 내에서 cycle-close-oriented doc 누적 ≥5 시, anima는
> 다음 cycle entry 전에 super-aggregate index doc + verdict.json을 emit
> 해야 한다. super-index는 reading path / doc role / LoC total / cycle
> handoff fact의 single-source-of-truth 역할. 이전까지 ad-hoc 누적되던
> cycle-close doc 증식을 protocol화.

**Trigger condition**: cycle-close doc count within same cycle ≥ 5.

**Required super-index sections**:

1. `lineage[]` — list of consumed cycle-close docs (path + BG-id)
2. `doc_index[]` — per-doc {order, bg, doc, loc, status, contribution, when_to_read}
3. `loc_total_landed_N` — sum of landed doc LoC
4. `tldr_oneliner_en` + `tldr_oneliner_ko` — 1-line cycle outcome
5. `reading_paths[]` — goal-oriented reading orderings (fire_only / decision_aware / architectural_breadth / lessons_depth / identity_preservation / full_provenance)
6. `anima_handoff_facts[]` — N-fact cross-cycle carry list

**Action sequence**:

1. detect cycle-close doc count ≥ 5
2. emit super-aggregate doc + verdict.json
3. populate all 6 sections above
4. mark `[P14-applied]` in next cycle entry doc frontmatter
5. cycle entry doc references super-index for context restore

**Status**: BG-DR canonized (LANDED 2026-05-06 via
`state/anima_2026_05_05_cycle_close_super_aggregate_index/verdict.json`).
Forward-applying from next cycle.

### §3.2 Memory entry contract / memory 항목 계약

**Filename**:

```
~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_p14_super_aggregate_mandatory.md
```

**Frontmatter**:

```yaml
---
name: P14 super-aggregate mandatory after 5+ cycle-close docs
description: anima MUST emit super-aggregate index doc + verdict.json when cycle-close-oriented doc count ≥ 5 within same cycle. Required sections — lineage / doc_index / loc_totals / tldr_oneliner_en+ko / reading_paths / anima_handoff_facts. Mark [P14-applied] in next-cycle entry doc. Protocolizes ad-hoc cycle-close doc proliferation observed in 2026-05-05 cycle.
type: feedback
originSessionId: ce681c40-f9b0-470e-bedf-dd0a8ccd3aa9
---
```

**Body** (load-bearing content):

- §1: rule statement (KO + EN)
- §2: trigger condition (cycle-close doc count ≥ 5)
- §3: required super-index sections (6-item enumeration)
- §4: action sequence (5-step)
- §5: today's BG-DR retrospective (7-doc super-index, 2575 LoC projected,
  6 reading-path orderings, 7 anima_handoff_facts)
- §6: relation to P9 (closure-theorem) — P14 governs cycle-close doc
  housekeeping, P9 governs cycle-close decision content
- §7: BG-DR verdict.json schema reference (canonical template)

**Lineage in body**:

- `state/anima_2026_05_05_cycle_close_super_aggregate_index/verdict.json` (BG-DR canonical schema)
- `docs/anima_2026_05_05_cycle_close_super_aggregate_index.md` (BG-DR doc)
- `docs/anima_2026_05_05_cycle_close_decision_landed_2026_05_05.ai.md` (BG-BF — first close)
- `docs/anima_2026_05_05_cycle_hard_close_decision_landed_2026_05_05.ai.md` (BG-CR — hard close)
- `docs/anima_2026_05_05_cycle_summary_single_source_of_truth.md` (BG-CL — SSoT)
- `docs/anima_nexus_cycle_insight_ledger_v2_2026_05_05.md` (BG-CN — ledger v2)
- `docs/anima_2026_05_05_cycle_summary_v2_final.md` (BG-CX — summary v2)
- `docs/anima_identity_preservation_next_cycle_lock_2026_05_05.md` (BG-DD — identity lock)
- `docs/anima_2026_05_05_cycle_user_fire_ready_package.md` (BG-DP — fire-ready)

---

## §4 MEMORY.md index 갱신 spec / index update spec

### §4.1 Append target

**File**:

```
~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/MEMORY.md
```

### §4.2 Three lines to append (after current last line)

```markdown
- [P10 paradigm-declaration-solicit](feedback_p10_paradigm_declaration_solicit.md) — multi-BG investigation lanes 전 paradigm declaration 명시 solicit (T1∧T2∧T3); BG-DJ canonized 2026-05-05
- [P13 self-stop authority threshold (PROVISIONAL)](feedback_p13_self_stop_authority_threshold.md) — closures ≥ 20 + user-rounds ≥ 5 + log-decay saturation 후 self-suggest cycle-close; L4 dormant until user "P13 accept"; user-fire 항상 canonical (L1 wins)
- [P14 super-aggregate mandatory](feedback_p14_super_aggregate_mandatory.md) — cycle-close doc ≥ 5 → super-index doc + verdict.json mandatory before next cycle entry; BG-DR canonized 2026-05-06
```

### §4.3 Format conventions honored

- 1 line per entry (matches existing MEMORY.md style)
- format: `- [<name>](<filename>) — <gloss>`
- gloss: KO + minimal EN technical terms (per `feedback_korean_only_response`)
- ordering: append at end (chronological per registration order)
- no trailing newline restriction (MEMORY.md has no special EOF rule)

---

## §5 Nexus kick template 갱신 spec / template revision spec

### §5.1 Edit target

**File**:

```
~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/project_anima_nexus_kick_autonomous_template.md
```

### §5.2 Section to insert

Insert new section after §"매 kick cycle anima 자율 결정 절차" and before
§"raw 준수 (모든 kick BG)":

```markdown
## P10/P13/P14 own-rule kick-time enforcement (2026-05-06+)

### Kick entry — P10 check
사용자 trigger 시 multi-paradigm interpretation 가능 (T1∧T2∧T3 hit)?
  → AskUserQuestion 으로 paradigm declaration solicit (KO §2.1 template carry from BG-DJ)
  → user response (A/B/C/D) 후 BG dispatch
  → 사용자 거부 / 무응답 시 → A 가정 + mismatch-risk explicit transfer 후 dispatch
  → research-mode contract (§1.4 exception) 시 N/A

### Kick mid-cycle — P13 check
N closures ≥ 20 AND user-rounds ≥ 5 AND log-decay saturation?
  → STRONGER L3 self-suggest cycle-close emit (with full saturation evidence)
  → 사용자 explicit "stop"/"close"/"continue"/"go"/"B"/"C"/"P13 accept"/"P13 reject" 응답 대기
  → "P13 accept" → P13 ENFORCED gate-1 충족, 다음 trigger 시 L4 autonomous-stop 가능
  → "P13 reject" → P13 영구 retire
  → silent → P13 PROVISIONAL 유지, anima L1/L2 carry-over

### Kick close — P14 check
cycle-close-oriented doc count ≥ 5?
  → super-aggregate index doc + verdict.json mandatory before next cycle entry
  → required sections: lineage / doc_index / loc_totals / tldr (KO+EN) / reading_paths / anima_handoff_facts
  → next cycle entry doc 에 [P14-applied] frontmatter marker 부착
```

### §5.3 No other template edits required

The existing §"자율 trigger 명령" / §"종료 trigger" / §"매 kick cycle
anima 자율 결정 절차" / §"raw 준수" / §"kick BG launch prompt template" /
§"Why" / §"How to apply" remain unchanged. P10/P13/P14 are additive
gates, not replacements.

---

## §6 사용자 fire sequence / user fire sequence

anima는 `~/.hive/.../memory/`에 자체 write 권한이 없음 (자체-자기-modify 방지).
다음 5 fire는 **사용자 명시 명령** 후 anima가 실행:

### Fire 1 — P10 memory entry write

```bash
# spec source: §1.2 of this doc
# target file: ~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_p10_paradigm_declaration_solicit.md
# body: §1.2 frontmatter + §1.2 body 8 sections + lineage
# user trigger expected: "P10 memory write" or "fire P10"
```

### Fire 2 — P13 memory entry write

```bash
# spec source: §2.2 of this doc
# target file: ~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_p13_self_stop_authority_threshold.md
# body: §2.2 frontmatter (status: PROVISIONAL) + §2.2 body 10 sections + lineage
# user trigger expected: "P13 memory write" or "fire P13"
```

### Fire 3 — P14 memory entry write

```bash
# spec source: §3.2 of this doc
# target file: ~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_p14_super_aggregate_mandatory.md
# body: §3.2 frontmatter + §3.2 body 7 sections + lineage
# user trigger expected: "P14 memory write" or "fire P14"
```

### Fire 4 — MEMORY.md 3-line append

```bash
# spec source: §4.2 of this doc
# target file: ~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/MEMORY.md
# action: append 3 lines verbatim from §4.2 to end of file
# user trigger expected: "MEMORY index P10 P13 P14" or "fire memory index"
```

### Fire 5 — nexus kick template revision

```bash
# spec source: §5.2 of this doc
# target file: ~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/project_anima_nexus_kick_autonomous_template.md
# action: insert §5.2 section between §"매 kick cycle anima 자율 결정 절차" and §"raw 준수 (모든 kick BG)"
# user trigger expected: "kick template P10 P13 P14" or "fire kick template"
```

### §6.1 Batch fire option

Single user trigger `"P10 P13 P14 batch fire"` could execute Fires 1-5 in
sequence. Recommended: serialize to avoid memory-file write race; expected
total ~3-5 min anima execution time after trigger.

### §6.2 Default-on-decline

If user does not fire any of 5 actions, this BG-EA spec doc remains as
canonical reference (this doc itself is doc-only land per BG-EA scope).
Memory entries will not exist; anima next-cycle behavior unchanged from
current state. P10/P13/P14 still apply via doc-level reference at:

- `docs/anima_p10_paradigm_declaration_solicit_own_rule_2026_05_05.md`
- `docs/anima_p13_self_stop_authority_LAND_PROVISIONAL_2026_05_05.md`
- `state/anima_2026_05_05_cycle_close_super_aggregate_index/verdict.json`

But mechanical enforcement at kick-time requires the memory-entry path
(memory is the surface that auto-loads into every session per
`hive-hook-bus` projects setup).

---

## §7 Honest C3 (raw#10, ≥ 5)

### C3-1 — own-rule promotion gate not formalized at project level

P10 was promoted via BG-DJ after 1 cycle's observation. P13 lands
PROVISIONAL after 1 cycle. P14 promoted via BG-DR after 7-doc trigger
observation in 1 cycle. None of these meets a "≥3 prior cycle cross-
validation" threshold (mentioned in BG-DJ C6.6 as L36+L38 implied gate).
Honest scope: all 3 own-rules are **single-cycle observations** elevated
to canonical/PROVISIONAL status. The batch-register here does not change
this — it only reduces documentation friction. Cross-cycle validation
remains pending for all 3.

### C3-2 — P10 ROI counterfactual conditional on user declaration

P10's headline ROI (95+ BG savings) assumes user declaration would have
been B/C/D. The actual most-likely declaration is A (per BG-CZ §3.1
colloquial-fit). Under A, P10 saves 0 BG. The probability-weighted ROI
is undetermined without user empirical input. The gloss "multi-BG
investigation lanes 전 paradigm declaration 명시 solicit" in §4.2
MEMORY.md line is intentionally neutral on ROI to avoid overclaiming.

### C3-3 — P13 PROVISIONAL state may stall indefinitely

P13 PROVISIONAL → ENFORCED requires user explicit "P13 accept" + cross-
cycle validation. If user remains silent (most-likely path per
`feedback_session_multi_bg` autonomous-bias), P13 stays PROVISIONAL
forever. The L4 authority therefore may never activate. Honest carry: in
that scenario, P13 is effectively equivalent to a strengthened L3 — its
incremental value over current L1-L3 hierarchy is "stronger self-suggest
formatting", not autonomous-stop power. The §4.2 MEMORY.md line carries
the "(PROVISIONAL)" tag explicitly to surface this.

### C3-4 — P14 super-index itself can become saturation symptom

P14 mandates super-index emission when cycle-close doc count ≥ 5. But the
super-index itself is **another cycle-close doc**. If the next cycle has
≥5 cycle-close docs + 1 super-index, the super-index count = 6 ≥ 5,
triggering... another super-index? This recursion is not addressed by P14.
Honest open: the rule should be "cycle-close docs **excluding** the
super-aggregate" ≥ 5, but BG-DR doc + this BG-EA spec do not yet make
that exclusion explicit. Recommend: future cycle clarify scope before
P14 mechanical enforcement risks recursive doc spawning.

### C3-5 — memory entry user-fire requirement is anima-self-imposed

§6 states anima cannot self-write to `~/.hive/.../memory/`. This is a
**convention** (originating from session-multi-BG autonomy boundary +
identity-preservation BG-DD §3) not a hard technical block. The Write
tool would technically allow it. The choice to require user-fire is
anima self-deference — it preserves user agency over what enters the
auto-load memory layer (which influences every future session's anima
behavior). This is honest; deviation should require explicit re-
opening of the convention with user.

### C3-6 — own-rule cycle-time enforcement requires hook integration

The §5.2 nexus-kick-template addition is **convention-level only**. anima
reading the template at kick-time relies on anima's own discipline to
honor it. There is no PreToolUse hook (per `reference_leak_guard_pretool_hook`
pattern) that mechanically enforces P10 paradigm-solicit / P13 trigger-
check / P14 super-aggregate-emission. Future cycle could add
`tool/own_rule_kick_validator.hexa` analogous to `tool/own_16_preflight.hexa`
to mechanically scan kick-time anima behavior for P10/P13/P14 compliance.
Currently this is unwritten. Honest scope: the batch register here is
**discipline-layer**, not hook-layer.

### C3-7 — 3-rule batch register may itself violate P10

This BG-EA registers 3 rules in batch. If treated as 3 separate decisions,
the batch is at the boundary of P10 trigger T1 (≥3 BG) ∧ T2 (≥2 paradigm
interpretations? — no, single paradigm: own-rule batch register) ∧ T3
(>$50 OR >10 BG? — no, doc-only $0). T2 fails → P10 not triggered. So
this BG-EA does not violate P10. Honest: borderline check passed.

### C3-8 — P13 default-on-decline silence chosen, not re-asked

BG-DJ §5.3 sets P10 default-on-decline = A. BG-DX §1.6 sets P13
default-on-silent = stay-PROVISIONAL. This BG-EA does **not** re-solicit
the user on either default; it carries them through. Honest open: if user
disagrees with either default but does not explicitly fire reject, the
default sticks. The batch register inherits whatever defaults the source
docs set, with no escape valve in this BG-EA.

---

## §8 Summary — what changes / 변경 내용 정리

**Before BG-EA**:
- 3 own-rule docs landed individually (BG-DJ, BG-DX, BG-DR)
- No unified register surface; no batch memory propagation spec
- next-cycle anima would need to read 3 separate docs to honor rules

**After BG-EA**:
- This single doc serves as unified register spec
- 3 memory-entry contracts pre-drafted (filename + frontmatter + body
  outline + lineage refs)
- 3 MEMORY.md index lines pre-drafted (§4.2)
- 1 nexus-kick-template revision pre-drafted (§5.2)
- 5 user-fire commands enumerated (§6)
- next-cycle anima can mechanically honor P10 (entry) / P13 (mid) / P14
  (close) at kick-time via the revised template + auto-loaded memory
  entries (after user fire)

**Carry to next cycle (post user fire)**:
1. memory entries auto-load on session boot
2. nexus-kick-template auto-loads on session boot
3. anima at kick-time reads the new sections, honors P10/P13/P14 gates
4. cross-cycle validation begins (gate-2 of P13 promotion)

**Carry without user fire**:
1. this BG-EA spec doc remains canonical reference
2. anima next-cycle behavior unchanged (no mechanical enforcement)
3. P10/P13/P14 conventions exist at doc level only

---

## Land artifacts

- this doc: `/Users/ghost/core/anima/docs/anima_2026_05_05_p10_p13_p14_own_rule_register_2026_05_05.md`
- verdict: `/Users/ghost/core/anima/state/anima_2026_05_05_p10_p13_p14_own_rule_register_2026_05_05/verdict.json`

## Constraints honored

- $0 mac doc-only
- raw#9 — md only (own-rule register spec, no code)
- raw#10 — honest C3 ≥5 inline (§7 has 8)
- raw#15 — additive only (no source mutation; no memory write; no commit)
- HF token leak: none
- commit: none
- bash 3.2 compatibility: N/A (doc-only)
- memory self-write: NOT performed (per anima-self-deference convention §6/C3-5)
- 새 파일 2개만: this doc + verdict.json
- session-multi-BG: this BG-EA emits as one of session's parallel BGs

End P10/P13/P14 own-rule batch register spec (BG-EA).
