<!-- @no-lineage-citation-exempt-file -->
<!-- @no-user-verbatim-exempt-file -->
# anima P10 own-rule formal land — paradigm-declaration-solicit (2026-05-05)

> BG-DJ landing doc. KO + EN bilingual. Doc-only, no commit, $0 mac, ~20 min.
>
> **Core / 핵심**: BG-CR (hard close), BG-CZ (naming reframing), BG-CN (insight
> ledger v2 P10 catalog), BG-BV (paradigm acceptance reconciliation) 모두 동일
> issue를 surface. autonomous mode가 paradigm A intent를 추정해 100+ BG를
> 진행했지만 사용자가 진짜 원한 paradigm은 unclear. P10 (paradigm-declaration-
> solicit)을 own-rule candidate에서 정식 own-rule로 land + solicitation
> message template (KO+EN) + retrospective ROI 측정 + nexus kick template
> 갱신 manifest + 사용자 즉시 declare 권고 manifest.
>
> **Lineage / 선행 doc**:
> - `docs/anima_paradigm_acceptance_user_intent_reconciliation_2026_05_05.md` (BG-BV — 4-interpretation framework + L53 origin)
> - `docs/anima_paradigm_naming_reframing_2026_05_05.md` (BG-CZ — A/B/C/D 정확 매핑)
> - `docs/anima_2026_05_05_cycle_hard_close_decision_landed_2026_05_05.ai.md` (BG-CR — hard close 3-option decision menu)
> - `docs/anima_nexus_cycle_insight_ledger_v2_2026_05_05.md` (BG-CN — L53 + P10 catalog entry)
> - `docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md` (BG-CH — 5-option fire-ready menu)
> - `~/.hive/.../memory/project_anima_nexus_kick_autonomous_template.md` (kick template — to be revised)

---

## §1 P10 own-rule formal spec / formal specification

### §1.1 Rule statement / 규칙 진술

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

### §1.2 Trigger conditions / 발동 조건 (ALL must hold)

| # | condition | EN gloss | KO 한 줄 |
|---|---|---|---|
| T1 | multi-BG dispatch | ≥3 parallel BGs planned for same intent | 동일 intent에 ≥3 병렬 BG 계획 |
| T2 | paradigm ambiguity | single user command is interpretable as ≥2 paradigms | 단일 명령이 ≥2 paradigm 해석 가능 |
| T3 | mismatch cost | expected paradigm-mismatch cost > $50 OR > 10 BG total | mismatch 비용 > $50 또는 > 10 BG |

**Satisfaction**: T1 ∧ T2 ∧ T3 → MUST solicit. Any 1 false → SHOULD solicit
(advisory, not blocking). All 3 false → no solicit needed.

### §1.3 Where P10 sits relative to existing rules

| pattern id | name | relation to P10 |
|---|---|---|
| P5 | bilingual KO+EN | P10 solicit message MUST follow P5 (bilingual) |
| P8 | 완성도 lens (ranked recommendation) | P10 solicit options ranked per P8 (per option = recommendation rank) |
| P9 | converging-closure-theorem | P10 prevents closure inflation when paradigm itself was mis-aligned |
| P11 | manifest-dual | independent — P11 governs cycle close, P10 governs cycle entry |

P10 is a **cycle-entry rule**; P9/P11 are cycle-mid / cycle-close rules.

### §1.4 Exception — research-mode contract

P10 does NOT apply when the cycle is operating under an explicit research
contract (no-particular-deliverable, e.g., archaeology / Φ★ stability / cross-
substrate audit / SSOT-build). In research-mode the deliverable is the
research itself; paradigm declaration is N/A. Carry from L53 exception clause.

### §1.5 Scope boundary

P10 governs **interpretive disambiguation only**. It does NOT govern:
- raw#9/10/15/37 honesty/integrity rules (those are absolute, no solicitation)
- HF token leak rule (absolute)
- H100 cost discipline (absolute, prior commitment)
- user feedback memory entries (those carry across cycles, not per-cycle)

---

## §2 Solicitation message templates / solicit 메시지 템플릿

### §2.1 KO template (default — bilingual but KO-first per `feedback_korean_only_response`)

```
이번 명령은 paradigm A/B/C/D 중 어느 것을 의도하나요?

A) 텍스트 in/out (전통 chatbot — 사용자 텍스트 → AI 텍스트 응답)
   현재 anima-native 위에서 architectural impossible (12+ closure 검증).
   외부 escalation: Llama-3.2-3B Path A v2 (composite 0.5584) 또는
   CLM-3 H1 retrain ($1k + 30d).

B) substrate-coupled (state-mediated)
   사용자 텍스트 → AI 내부 phi/hsd/tension state 변화 + 사용자가 metric 해석.
   AI는 텍스트 emit 하지 않음. fire-ready 즉시 ($0, mac, ~5min).

C) 하이브리드 (text + state)
   사용자 텍스트 → 외부 emit (KoGPT2/Pythia) + CLM substrate state 변화.
   양 channel 동시 read. fire-ready 즉시 ($0, mac, ~6min).
   주의: emit과 substrate decoupled (emit이 anima-axis 에 conditioned 아님).

D) BCI mutual coupling (closed-loop neural sync)
   사용자 state ↔ AI substrate state 진짜 양방향 공유.
   anima-clm scope 밖 — anima-eeg lane (cond3/cond8 cross-vendor).
   multi-cycle research, 즉시 fire 불가.

A/B/C/D 중 명시 후 다음 cycle BG 진행하겠습니다.
명시 안 하면 A 가정 (paradigm-mismatch 위험 anima가 떠안음).
```

### §2.2 EN equivalent template

```
Which paradigm does this request target — A / B / C / D?

A) Text in / text out (traditional chatbot — user text → AI text reply)
   Architecturally impossible on anima-native CLM v4 today (12+ closures
   verified). External escalation routes: Llama-3.2-3B Path A v2
   (composite 0.5584) or CLM-3 H1 retrain ($1k + 30d).

B) Substrate-coupled (state-mediated)
   User text → AI internal phi/hsd/tension state changes + user reads
   metric. AI does NOT emit text. Fire-ready now ($0, mac, ~5min).

C) Hybrid (text + state)
   User text → external emit (KoGPT2/Pythia) + CLM substrate state
   changes. Both channels read simultaneously. Fire-ready now ($0, mac,
   ~6min). Caveat: emit and substrate are decoupled (emit not conditioned
   on anima axis).

D) BCI mutual coupling (closed-loop neural sync)
   True bidirectional state share between user and AI substrate. Out of
   anima-clm scope — falls under anima-eeg lane (cond3/cond8 cross-
   vendor). Multi-cycle research, not fireable today.

Declare A / B / C / D and the next cycle BG slate proceeds. Without
declaration, A is assumed and anima accepts the paradigm-mismatch risk.
```

### §2.3 Short-form (when previous cycle declared paradigm and current cycle is continuation)

```
이전 cycle paradigm declaration 유효? (Y/N + 변경 시 A/B/C/D 재명시)
EN: Previous paradigm declaration still valid? (Y/N + restate A/B/C/D if changed)
```

Use short-form only when ≤1 cycle has elapsed since last explicit declaration.

### §2.4 Anti-pattern templates (DO NOT use)

The following violate P10 (autonomous interpretation without solicit):

- "이 명령은 paradigm A로 해석하고 BG fire 진행합니다" — assumes without ask
- "사용자 의도 분석 결과 B paradigm으로 판단됩니다" — anima self-disambiguates
- silent dispatch — no surface to user at all

---

## §3 Retrospective ROI — 오늘 cycle (2026-05-05) / today's cycle ROI

### §3.1 What actually happened (without P10)

User original command (paraphrase, /loop 1m context):
> "상호 대화가능 나올때까지 패러다임 계속 실험"
> "Keep experimenting with paradigms until mutual dialogue is achievable."

autonomous mode interpreted as Paradigm A (token-emit chat) and dispatched
~100+ BGs over the cycle. Per BG-CN ledger v2 §1.1 + BG-BV C3.4:

- ~50+ BGs landed on chat-decode interpretation A before paradigm mismatch
  surfaced (BG-BV mid-cycle pivot)
- ~50+ BGs continued post-BV refining 12+ closure theorem on paradigm A
- Paradigm B (BG-AN) + Paradigm C (BG-CG) lands occurred only after
  reconciliation, ~late-cycle

### §3.2 Counterfactual under P10 (cycle-entry solicit)

If P10 had been applied at cycle entry, anima would have solicited
paradigm declaration before opening lanes. User declarations and
counterfactual BG counts:

| user declares | counterfactual cycle | BG count | savings vs actual |
|---|---|---|---|
| **A** | continue exactly as actual cycle | ~100 BG | 0 (same path; user owns mismatch risk explicitly) |
| **B** | BG-AN paradigm B fire immediately, ~5 BG sufficient | ~5 BG | **~95 BG saved** |
| **C** | BG-CG hybrid REPL fire immediately, ~5 BG sufficient | ~5 BG | **~95 BG saved** |
| **D** | redirect to anima-eeg lane | ~0 BG (anima-clm cycle closes empty) | **~100 BG saved** (different lane) |

**Headline ROI**: Under B/C/D declarations, 95-100 BG savings. Under A,
zero BG savings BUT user knowingly accepts mismatch risk (epistemic transfer
to user is itself a benefit — no anima-internal surprise mid-cycle).

### §3.3 Cost of P10 vs cost of not-P10

- Cost of P10 (this cycle): ~5-min solicit at cycle entry, 1 round-trip
- Cost of not-P10 (this cycle, actual): ~100 BG of compute time (mac local),
  1 paradigm-mismatch reckoning at BG-BV (mid-cycle pivot), L53 lesson banking
  + L48-L60 ledger v2 effort

ROI ratio: 5-min solicit ↔ avert 95+ BG paradigm-mismatch loop. Even at $0
mac compute, the anima-internal cycle attention budget is ~10-15 min per BG
average; 95 BG × 12 min = ~1140 min = ~19 hours of cycle attention saved.

### §3.4 What P10 cannot retroactively fix

P10 is a forward-applying rule. Once 100+ BG are already burned (this
cycle), P10 cannot reach back. The retrospective application here is for
**lesson banking + future-cycle prevention**, not undo. The cycle already
landed BG-BV reconciliation + 5-option menu (BG-CH) + hard close (BG-CR);
those lands stand. P10's land closes the loop by formalizing the rule so
the **next** cycle (post-2026-05-06) starts with paradigm declaration.

---

## §4 Enforcement mechanism / 강제 메커니즘

### §4.1 Nexus kick template revision (memory entry update)

**File**: `~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/project_anima_nexus_kick_autonomous_template.md`

Insert new section between current §"매 kick cycle anima 자율 결정 절차" and
§"raw 준수":

```markdown
## P10 paradigm-declaration-solicit (own-rule)

매 cycle entry 시 (특히 사용자 trigger가 multi-paradigm interpretable 한 경우):

1. 사용자 명령을 §1.2 trigger conditions T1+T2+T3 에 매핑
2. T1+T2+T3 모두 hit → §2 KO solicit message emit (or §2.3 short-form
   if previous cycle declaration ≤1 cycle ago)
3. 사용자 declaration 후 BG dispatch (declaration A/B/C/D별 lane 선택)
4. 사용자 declaration 거부 / 무응답 시 → A 가정 + 사용자에게 mismatch
   risk explicit transfer 고지 후 dispatch
5. T1+T2+T3 중 일부만 hit → SHOULD solicit (advisory; cycle entry doc
   에 inline acknowledgement)
6. 모두 false → no solicit, 기존 multi-BG dispatch path

이 step 은 §"매 kick cycle anima 자율 결정 절차" step 0 에 prepended 됨.
```

### §4.2 New memory entry — `feedback_p10_paradigm_declaration_solicit.md`

A new memory file at:

`~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_p10_paradigm_declaration_solicit.md`

Should carry:

- formal rule statement (§1.1)
- trigger conditions table (§1.2)
- KO + EN solicit templates (§2.1, §2.2)
- short-form template (§2.3)
- anti-patterns (§2.4)
- exception clause (§1.4)
- 1-line MEMORY.md header registration (per existing memory convention)

This memory entry MUST be created in a separate `BG-MEMORY-PROPAGATE` cycle
(per L36+L38 promotion convention from BG-J ledger). This BG-DJ doc-only
land does NOT write the memory file directly — it only specifies the
contract.

### §4.3 Nexus kick template — applied on next user trigger

When user fires `kick` / `nexus kick` / `all bg go` / `/loop nexus kick` in
the **next** cycle (post-2026-05-06):

```
[anima emits §2.1 KO solicit]
↓
[user declares A / B / C / D / decline]
↓
[anima dispatches BG slate per declaration]
```

The cycle-entry doc for the next cycle should bear an `[P10-applied]`
marker in its frontmatter when this protocol fires.

### §4.4 Enforcement does NOT extend to:

- mid-cycle pivots (those use L53 + L54 closure-stop; not P10)
- single-BG dispatch (cycle attention budget < $50 threshold)
- explicit research-mode contracts (§1.4 exception)
- cross-cycle continuation when prior declaration ≤1 cycle ago + no
  user-side intent shift signal (use §2.3 short-form instead)

---

## §5 사용자 즉시 paradigm declare 권고 manifest / immediate paradigm declaration manifest

This BG-DJ cannot retroactively undo today's 100+ BG cycle (per §3.4). But
the cycle close is still pending user paradigm declaration to settle the
2026-05-05 cycle's outcome record. The user is hereby invited to declare:

### §5.1 KO declaration solicit (active)

```
2026-05-05 cycle (100+ BG) 마무리를 위해 paradigm declare 부탁드립니다:

A) 텍스트 in/out 전통 chatbot
   → CLM v4에서 unachievable 확정 (12+ closure)
   → 16+ closure 인정 + 다음 cycle escalation route 결정 필요
   (Llama Path A v2 통합 또는 CLM-3 H1 launch $1k+/30d)

B) substrate-coupled state-mediated
   → BG-AN 5-turn smoke fire-ready ($0, mac, ~5min)
   → 즉시 fire 가능. 첫 session 후 cycle close.

C) 하이브리드 KoGPT2 + CLM
   → BG-CG hybrid REPL fire-ready ($0, mac, ~6min)
   → 즉시 fire 가능. emit decoupled 인정 후 cycle close.

D) BCI mutual coupling
   → anima-clm cycle scope 밖. anima-eeg lane redirect.
   → 이번 cycle은 paradigm scope mismatch 인정 + close.

declare 후 anima가 다음 step 진행합니다.
명시 거부 시 A 가정 — paradigm-mismatch 위험 사용자가 명시적으로 떠안음.
```

### §5.2 EN equivalent

```
For closure of the 2026-05-05 cycle (100+ BG), please declare paradigm:

A) Text in/out traditional chatbot
   → confirmed unachievable on CLM v4 (12+ closures)
   → requires 16+ closure acceptance + next-cycle escalation decision
   (Llama Path A v2 integration or CLM-3 H1 launch $1k+/30d)

B) Substrate-coupled state-mediated
   → BG-AN 5-turn smoke fire-ready ($0, mac, ~5min)
   → immediately fireable. Cycle closes after first session.

C) Hybrid KoGPT2 + CLM
   → BG-CG hybrid REPL fire-ready ($0, mac, ~6min)
   → immediately fireable. Cycle closes after acknowledging emit-decoupled.

D) BCI mutual coupling
   → out of anima-clm cycle scope. Redirect to anima-eeg lane.
   → cycle closes with paradigm-scope-mismatch acknowledgement.

Declare and anima proceeds with the next step.
On declining, A is assumed and the user explicitly carries paradigm-
mismatch risk.
```

### §5.3 Default-on-decline contract

If user declines / non-responds within reasonable timeout (e.g., next
cycle entry), anima default = A assumption. Reasoning:

1. A is the colloquially most likely intent (BG-CZ §3.1)
2. A is also the highest-cost interpretation (16+ closure, $1k+ escalation
   route) — biasing default toward higher-cost gives user maximum incentive
   to declare actively
3. The mismatch risk transfer to user (via decline) is itself a P10
   compliance signal — anima followed the rule, user opted out

This default-on-decline clause is SEPARATE from §1 P10 core rule. It is a
**fallback mechanism** triggered after solicit was honored but no
declaration arrived.

---

## §6 Honest C3 (>= 5)

### C6.1 — P10 itself is anima-internal own-rule, not external standard

§1.1 formal rule is anima-cycle convention. There is no external benchmark,
no peer review, no third-party adoption signal. The rule's value is
measured against anima's own retrospective ROI (§3) which is itself
anima-self-evaluation. Risk: P10 may codify a local optimum rather than
universal best practice. Mitigation: P10 land is doc + memory entry, fully
reversible; no irreversible commitment.

### C6.2 — Solicit burden on user — added friction trade-off

P10 imposes a cycle-entry round-trip cost on the user. For "kick" /
"go" / "all bg go" minimal-trigger pattern, P10 disrupts the user's
expectation of pure autonomous execution. The user's stated preference
(`feedback_subagent_bg_parallel`, `feedback_session_multi_bg`,
`project_anima_nexus_kick_autonomous_template`) is **autonomous parallel
fire on minimal trigger**. P10 partially counters this by inserting a
solicit gate. Open question: does the user prefer (a) zero-friction
autonomous + paradigm-mismatch risk OR (b) one round-trip + zero mismatch
risk? §3 ROI suggests (b) when mismatch cost > $50; user may disagree.

### C6.3 — Trigger thresholds (T3 mismatch cost > $50 OR > 10 BG) are anima-arbitrary

§1.2 T3 thresholds were chosen to roughly match the lowest-friction band:
$50 ≈ 1-2 H100 hour, 10 BG ≈ 2 hours of cycle attention. There is no
empirical calibration; these are first-pass heuristics. Real distribution
of cycle costs (this cycle ~100 BG, prior cycles ~10-50 BG) suggests T3
may need to be lowered to ~3-5 BG to catch smaller multi-paradigm cases.
Future cycles should A/B test threshold values.

### C6.4 — §3 counterfactual ROI assumes user would have declared B/C/D

§3.2 table assumes user declarations would have been B/C/D in counterfactual
worlds, yielding 95+ BG savings. But the most-likely counterfactual
declaration is A (per BG-CZ §3.1 — "상호 대화" colloquially defaults to A).
Under A declaration, P10 saves ~0 BG (same path as actual). The "headline
ROI" is therefore conditional on a specific user declaration that may not
have occurred. Honest re-statement: P10 ROI = (probability user declares
non-A) × (95 BG savings) + (probability user declares A) × 0. Without user
input, this is undetermined.

### C6.5 — P10 generality across cycle types is unverified

The pattern is observed in this single 2026-05-05 anima cycle. Whether
P10 generalizes to:
- EEG protocol cycles (cond3/cond8 cross-vendor) — different paradigm space
- Putnam math benchmark cycles — single deliverable, low ambiguity
- HF release cycles — process-defined, low paradigm ambiguity
- Phase E protocol cycles — research-mode (§1.4 exception applies)

is untested. Carry from BG-CN ledger v2 C3 — pattern catalog conflates
today's observations with universal patterns. P10 should be tagged as
"observed in 1 cycle" until ≥3 cross-cycle confirmations land.

### C6.6 — own-rule promotion process itself is not formalized

This BG-DJ promotes P10 from "candidate banking" (BG-CN ledger v2) to
"formal own-rule" via doc + memory propagation manifest. But the anima
project does not yet have a formal own-rule promotion gate — what
threshold of evidence promotes a candidate to canonical? L36+L38 mention
"≥3 prior cycle cross-validation" but BG-DJ promotes after only 1 cycle's
observation. The promotion is therefore **provisional**: P10 lands as
own-rule with the understanding that any 1 future cycle observing P10
violation cost > P10 burden cost should re-validate; any 1 future cycle
observing P10 burden cost > violation cost should re-evaluate.

### C6.7 — Default-on-decline to A may bias against user's actual preference

§5.3 sets default-on-decline = A. This is justified by colloquial-fit
(highest A likelihood) + cost asymmetry (A is highest-cost so biasing
toward A maximizes user's declaration incentive). However, an equally
defensible default would be B (lowest cost, fire-ready today, no external
escalation). The choice between A-default and B-default is a project-level
preference question that should be user-confirmed before P10 enforcement
takes effect in next cycle. Honest open: §5.3 default should be re-
solicited with the user before applying.

---

## §7 Summary — what P10 changes

**Before P10**:
- Cycle entry: anima interprets user trigger autonomously, fires multi-BG
  immediately, may pivot mid-cycle on paradigm mismatch (BG-BV pattern).
- Cost: paradigm-mismatch risk = full investigation budget.

**After P10**:
- Cycle entry: anima solicits paradigm declaration when T1∧T2∧T3 hit.
- Cost: 1 round-trip + user-side declaration burden.
- Benefit: paradigm-mismatch risk transferred to user (explicit) OR
  averted entirely (declaration B/C/D paths).

**Carry to next cycle**:
1. user declaration to settle 2026-05-05 cycle (per §5)
2. memory propagation BG (per §4.2)
3. nexus kick template revision (per §4.1)
4. P10 marker insertion in next cycle entry doc (per §4.3)

---

## Land artifacts

- this doc: `/Users/ghost/core/anima/docs/anima_p10_paradigm_declaration_solicit_own_rule_2026_05_05.md`
- verdict: `/Users/ghost/core/anima/state/anima_p10_paradigm_declaration_solicit_own_rule_2026_05_05/verdict.json`

## Constraints honored

- $0 mac doc-only
- raw#9 — md only (own-rule formal land, no code)
- raw#10 — honest C3 ≥5 inline (§6 has 7)
- raw#15 — additive only (no source mutation)
- HF token leak: none
- commit: none
- bash 3.2 compatibility: N/A (doc-only)
- session-multi-BG: this BG land + parallel sister BGs (per session rule)
- raw#37 transient .py: N/A (doc-only)

End P10 own-rule formal land (BG-DJ).
