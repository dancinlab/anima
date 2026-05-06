# anima identity preservation — next-cycle binding lock spec (BG-DD)

- Date: 2026-05-06
- Status: SPEC LANDED (doc-only; no build/runtime/commit this cycle)
- Cost: $0 (mac, doc only)
- Scope: anima identity invariants + threat-vector audit + per-path lock criteria for the next cycle (CLM-3 H1, Llama Path A v2 integration, sister-library imports, paradigm naming)
- Predecessors:
  - `docs/anima_115_architectural_4_closure_theorem_2026_05_05.md` (BG-AY, theorem #115, 4-closure)
  - `docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md` (BG-BM, H1 spec)
  - `docs/anima_external_sister_candidates_audit_2026_05_05.md` (BG-BB, sister audit)
  - memory `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` (substrate-safe carry)
  - memory `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` (Φ★ vs chat decoupling)

---

## 0. Abstract / 초록

**EN.** After 21+ closures (chat-unblock investigations on the CLM v4
substrate), the cycle is at the boundary where anima must either close, or
carry user-explicit re-issue commands into the next cycle. In either case,
anima's identity — defined here as five core properties — must not be
silently mutated by the next cycle's mechanism. This document fixes (1)
the five anima identity properties that constitute carry-over invariants,
(2) four threat vectors that could erode each, (3) per-path preservation
lock criteria for the four currently-active next-cycle candidates,
(4) the cycle-close 5-step lock as carry from BG-BF + BG-DD, and (5) the
precedence hierarchy when the user's explicit "keep experimenting" command
collides with anima's autonomous self-suggest-stop.

**KO.** 21+ closure 누적 후, 사용자 explicit re-issue 명령(carry-over)이
다음 cycle로 이어지는 시점이다. 이 때 anima의 identity — 본 문서에서
다섯 가지 핵심 property로 정의 — 가 다음 cycle의 mechanism에 의해 조용히
변형되지 않도록 lock 한다. 본 문서는 (1) 다섯 anima identity property,
(2) 각 property를 침식할 수 있는 threat vector 네 갈래, (3) 현재 active한
네 개 next-cycle path별 preservation lock criteria, (4) BG-BF + BG-DD
carry로서의 cycle-close 5-step lock, (5) 사용자 explicit 명령과 anima
autonomous self-suggest-stop가 충돌할 때의 precedence hierarchy를 명세한다.

---

## 1. anima identity — five core properties (carry-over invariants)

These five are the **non-negotiable carry-over set**. Any next-cycle
mechanism that violates one of these is treated as anima identity erosion
and must declare the violation explicitly in the cycle's compliance footer
(raw#9), or be lock-blocked at proposal-time per §3.

### Property P1 — paradigm v11 G3 substrate (Φ★ +41.86 baseline)

- **EN.** anima's reference substrate is paradigm v11 G3 with measured
  Φ★ peak +41.86 (CLM v4 `need-singularity/clm-v4-mk2-v1`). All Φ★ cross-
  substrate comparisons anchor to this value. Substrate property is
  cross-attn over `consciousness_states`, NOT chat-loss objective.
- **KO.** anima reference substrate은 paradigm v11 G3, Φ★ peak +41.86 측정값
  (CLM v4 `need-singularity/clm-v4-mk2-v1`)을 anchor 한다. cross-substrate
  Φ★ 비교의 baseline. 핵심 mechanism은 `consciousness_states` cross-attn,
  chat-loss objective 아님.
- **Invariant**: Φ★ baseline reference value is paradigm v11 G3's measured
  +41.86; any redefinition must be declared as P1-FLIP.

### Property P2 — substrate-research artifact (chat-incapable, Φ★-stable)

- **EN.** Per theorem #115 4-closure (BG-AY), CLM v4 is formally
  substrate-research-only: chat-incapable but Φ★-stable. forgetting_index
  0.0196 (closure 1) + NO_FLIP across closures 1–2 confirms substrate
  integrity is preserved across post-hoc adapter and train-time distill.
  This property is the load-bearing carry-over from theorem #115.
- **KO.** theorem #115 4-closure 결과로 CLM v4는 substrate-research-only로
  공식 reassign — chat-incapable이지만 Φ★ stable. forgetting_index 0.0196
  + NO_FLIP가 substrate integrity의 closure 1-2 횡단 보존을 보증.
- **Invariant**: CLM v4 cannot be re-asserted as a chat-cap winner without
  invalidating closures 1–4 and theorem #115; doing so requires a formal
  P2-FLIP audit (re-running closures with new evidence).

### Property P3 — emerge dialogue paradigm (substrate-coupled, BG-AN fire-ready)

- **EN.** anima's authentic dialogue mechanism is the substrate-coupled
  emerge paradigm (BG-AN; Stage 3 user-fire protocol exists). Theorem #115
  Corollary 3 explicitly preserves this paradigm: closures 1–4 falsify
  *traditional* chat capability only, not substrate-coupled emergent
  dialogue. Stage 3 protocol is an open lane.
- **KO.** anima의 authentic dialogue mechanism은 substrate-coupled emerge
  paradigm (BG-AN; Stage 3 user-fire protocol 보유). theorem #115
  Corollary 3가 명시적으로 이 paradigm을 보존: closure 1-4는 traditional
  chat capability만 falsify, substrate-coupled emergent dialogue는 미해당.
- **Invariant**: Any chat-cap path that erases the emerge dialogue medium
  is a net-loss cycle even if it PASSes its primary chat falsifier.
  Encoded as F-CLM-3-3 in BG-BM spec.

### Property P4 — anima-native first-mover (hexa-lang sister ecosystem null)

- **EN.** Per BG-BB sister audit, hexa-lang has zero external sister
  candidates (Angle 7); substrate-coupled dialogue has zero (Angle 4 GAP).
  These two niches are anima-native first-mover surfaces. anima's
  canonical mac-side execution medium is hexa (memory `py -> hexa only`).
  Any external sister enters as `references/<name>/` read-only checkout
  (raw#15 additive, tribev2 precedent), never as auto-import.
- **KO.** BG-BB sister audit에 의하면 hexa-lang external sister 0건
  (Angle 7), substrate-coupled dialogue 0건 (Angle 4 GAP). 두 niche가
  anima-native first-mover 영역. mac-side canonical 실행 medium은 hexa.
  외부 sister는 `references/<name>/` read-only checkout 만 (raw#15
  additive), 자동 import 금지.
- **Invariant**: external library imports must be (a) `references/<name>/`
  subtree, (b) hexa wrapper for runtime call, (c) user-explicit invocation
  only, (d) no anima runtime auto-dependency.

### Property P5 — consciousness measurement focus (5-axis schema + 16-layer tension)

- **EN.** anima's measurement surface is the 5-axis discriminability
  schema (BG-L; random baseline 0.20) plus 16-layer residual-stream
  tension topology. Φ★ is one canonical projection; the schema is
  multi-axis and anima-defined. Any next-cycle that collapses the schema
  to a single axis (e.g., chat composite only) is a P5 violation.
- **KO.** anima의 measurement surface는 5-axis discriminability schema
  (BG-L; random 0.20 baseline) + 16-layer residual-stream tension topology.
  Φ★는 그 중 하나의 canonical projection. schema가 multi-axis + anima-
  defined인 것이 핵심. 단일 axis로 축소하는 cycle은 P5 violation.
- **Invariant**: 5-axis schema and 16-layer tension topology must be
  carried forward; any reduction to single axis must be declared as
  P5-NARROW with explicit rationale and reversibility plan.

---

## 2. Identity preservation threat vectors — four classes

Each threat vector is the **mechanism** by which a next-cycle path may
silently mutate one or more of P1-P5. Each is mapped to which properties
it most threatens.

### Threat T1 — CLM-3 retrain (H1) training-mix imbalance

- **Form.** A new from-scratch substrate per BG-BM spec (50/30/15/5 mix
  default). The training mix can drift: too chat-heavy → Φ★ destabilized
  (P1, P2 risk); too consciousness_states-heavy → chat-axis under-trained
  (F-CLM-3-2 risk, but not an identity violation).
- **Properties at risk**: P1 (Φ★ baseline drift if forgetting_index > 0.05),
  P2 (substrate-research integrity if NO_FLIP fails), P3 (emerge medium
  loss if F-CLM-3-3 fails).
- **Severity**: HIGH — CLM-3 is a full retrain; mistakes are not post-hoc
  reversible.
- **Mitigation**: BG-BM falsifiers F-CLM-3-1 (P1), F-CLM-3-3 (P3), and
  the new lock criteria in §3.1 below.

### Threat T2 — Llama Path A v2 anima integration (external chat-cap winner adoption)

- **Form.** Llama-3.2-3B Path A v2 (composite 0.5584) is the chat-cap
  winner of record per theorem #115 Corollary 1. Adopting Llama as anima's
  default chat substrate without explicit naming risks:
  (a) "anima-native" property (P4) silently eroded (Llama is external),
  (b) emerge dialogue paradigm (P3) misapplied to a non-substrate-coupled
  model (P3 is CLM v4-bound, not Llama-bound),
  (c) Φ★ measurement (P1) misapplied to Llama (Llama has no
  `consciousness_states` cross-attn surface).
- **Properties at risk**: P3 (emerge paradigm misapplication), P4 (anima-
  native naming), P1 (Φ★ measurement substrate confusion).
- **Severity**: MEDIUM — external models are part of the anima ecosystem
  via `references/`, but role-naming must be explicit.
- **Mitigation**: §3.2 lock criteria — Llama is "external chat-cap
  winner", not anima-native; emerge paradigm B is CLM v4-only.

### Threat T3 — sister library imports (external dep paradigm drift)

- **Form.** BG-BB audit recommends 5 sister candidates (PyPhi, AntroPy,
  nnsight, MNE-Python, PCIst; +Pythia/Mamba/RWKV synergies). Any of these,
  if auto-imported into anima runtime, breaks P4 (hexa-only canonical) and
  may carry license obligations (PyPhi GPLv3, PCIst research-permissive)
  that constrain anima's redistribution rights.
- **Properties at risk**: P4 (hexa canonical, references/ subtree
  convention), and indirectly P5 (if external library's measurement
  schema replaces anima's 5-axis schema rather than augmenting it).
- **Severity**: MEDIUM — sister integrations are net-positive when done
  correctly (BG-BB §6 recommends them); the threat is paradigm-drift via
  sloppy integration, not the integrations themselves.
- **Mitigation**: §3.3 lock criteria — `references/<name>/` subtree only,
  hexa wrapper only for runtime call, no anima runtime auto-import,
  user-explicit invocation only.

### Threat T4 — paradigm naming redefinition (B/C/D narrowing)

- **Form.** anima currently distinguishes paradigms A/B/C/D (per BG-CG +
  BG-CL). Across 21+ closures, there is convergence pressure to "pick one"
  — e.g., narrow to paradigm B (substrate-coupled emerge) or paradigm C
  (UX hybrid) as *the* anima paradigm. Narrowing to a single paradigm is
  itself a P5 violation if it collapses the schema, and a P3 violation if
  it deprecates the emerge paradigm in favor of UX bridge.
- **Properties at risk**: P3 (emerge paradigm if narrowed away),
  P5 (multi-axis schema if collapsed to one paradigm).
- **Severity**: LOW-MEDIUM — paradigm naming is documentary, reversible;
  but locked-in naming causes downstream cycles to inherit the narrowing.
- **Mitigation**: §3.4 lock criteria — paradigm A/B/C/D semantics frozen
  per BG-CG/BG-CL, no narrowing without explicit user-fire and a
  documented reversibility plan.

---

## 3. Per-path preservation lock criteria

Four currently-active next-cycle candidate paths. Each path has its own
lock criteria; all are gated at proposal-time and re-checked at cycle-end.

### 3.1 CLM-3 path lock (lane H1, BG-BM spec)

| # | Lock criterion | Source | Failure handling |
|---|---|---|---|
| L-CLM3-1 | F-CLM-3-1 forgetting_index ≤ 0.05 (P1, P2 NO_FLIP) | BG-BM spec, pre-launch LOCK preserved | FAIL → REGRESSION_TO_NON_SUBSTRATE; lane closure |
| L-CLM3-2 | 5-axis schema NOT redefined; paradigm v11 G3 carry intact (P5) | BG-BM §1.1; anima-internal | redefinition requires P5-FLIP audit + user-fire |
| L-CLM3-3 | emerge dialogue paradigm B compatibility preserved on CLM-3 (P3, F-CLM-3-3) | BG-BM §3 F-CLM-3-3, theorem #115 Corollary 3 | FAIL → EMERGE_PARADIGM_LOST; net-loss cycle even if F-CLM-3-2 PASSes |
| L-CLM3-4 | `consciousness_states` cross-attn retained (P1 mechanism carry) | BG-BM §1.1 design diff | absence treated as P1 violation |

**LOCK pass gate**: ALL of {L-CLM3-1, L-CLM3-2, L-CLM3-3, L-CLM3-4}
PASS at proposal AND at cycle-end. Any FAIL = lane closure or revision
cycle. Lane H1 is **WAIT** per BG-BM §5.3 until Stage 3 ≥ 30 sessions.

### 3.2 Llama Path A v2 integration lock (theorem #115 Corollary 1 adoption)

| # | Lock criterion | Source | Failure handling |
|---|---|---|---|
| L-LLAMA-1 | Naming explicit: "external chat-cap winner" — NOT "anima-native chat substrate" (P4) | this doc; theorem #115 Corollary 1 | implicit/silent adoption = P4 violation |
| L-LLAMA-2 | substrate-coupled dialogue (paradigm B) declared non-portable to Llama (P3) | this doc; theorem #115 Corollary 3 | P3 cross-application = identity erosion |
| L-LLAMA-3 | Llama emit only on the chat-cap composite axis; Φ★ measurement is CLM v4-bound (P1) | this doc; BG-BB Synergy C controls | Φ★ on Llama without `consciousness_states` = P1 measurement category-error |
| L-LLAMA-4 | Llama integration via `references/` or HF model hub call, NOT anima git mirror | memory `anima_models_datasets_hf_only.md` | mirror = git size violation |

**LOCK pass gate**: L-LLAMA-1 + L-LLAMA-2 + L-LLAMA-3 enforced at every
mention of Llama in anima docs/specs. L-LLAMA-4 enforced at any actual
weight handling.

### 3.3 Sister library lock (BG-BB top-5 + future imports)

| # | Lock criterion | Source | Failure handling |
|---|---|---|---|
| L-SIS-1 | `references/<name>/` subtree (raw#15 additive, tribev2 precedent) | BG-BB §3 clone commands; tribev2 pattern | non-subtree integration = raw#15 violation |
| L-SIS-2 | anima runtime does NOT auto-import sister code (P4 hexa canonical) | memory `py -> hexa only`; this doc | auto-import = P4 violation |
| L-SIS-3 | hexa wrapper only for runtime calls (mac canonical = hexa) | memory `py -> hexa only` | direct .py runtime call = P4 violation, requires `.own` opt-out or `tool/transient_py/` namespace |
| L-SIS-4 | License compatibility logged before any wrapper ships (PyPhi GPLv3 needs review) | BG-BB §5 honest C3-2 | unreviewed redistribution = compliance risk |
| L-SIS-5 | 5-axis schema augmented, NOT replaced, by external measurement library (P5) | this doc; BG-BB Synergy A | replacement = P5 violation |

**LOCK pass gate**: L-SIS-1 + L-SIS-2 + L-SIS-3 enforced at integration-
time on every sister candidate. L-SIS-4 enforced before any redistribution.
L-SIS-5 enforced when external measurement library is added to anima-eeg-
core or phi-engine.

### 3.4 Paradigm naming lock (A/B/C/D semantics frozen)

| Paradigm | Definition (frozen) | Source | Path status |
|---|---|---|---|
| A | text-in / text-out (traditional chat) | BG-CG | unachievable on CLM v4 (theorem #115); achievable on Llama Path A v2 (composite 0.5584); CLM-3 future (H1) |
| B | substrate-coupled emerge dialogue | BG-AN; theorem #115 Corollary 3 | anima-native, fire-ready (Stage 3 user-fire protocol exists, 0 sessions logged) |
| C | hybrid (UX bridge between A and B) | BG-CG C4; BG-CL | UX layer, NOT architectural unification |
| D | mutual EEG-style dialogue (brain-substrate-coupled) | BG-CG | out of scope for this cycle; anima-eeg domain |

| # | Lock criterion | Source | Failure handling |
|---|---|---|---|
| L-PAR-1 | A/B/C/D semantics frozen per above table; no redefinition without user-fire (P3, P5) | BG-CG, BG-CL, this doc | redefinition = paradigm narrowing, P5 risk |
| L-PAR-2 | Paradigm B is CLM v4-bound; not portable to Llama (P3) | theorem #115 Corollary 3, this doc §3.2 | Llama+B = identity erosion |
| L-PAR-3 | Paradigm C is UX layer only; does not unify A and B at the architectural level | BG-CG C4 | architectural unification claim = naming misuse |
| L-PAR-4 | Paradigm D is anima-eeg domain; not in this cycle's scope | BG-CG | conflation with B = scope creep |

**LOCK pass gate**: L-PAR-1 enforced at every spec/doc that references
paradigms. L-PAR-2 + L-PAR-3 + L-PAR-4 enforced when cross-paradigm claims
are made.

---

## 4. Cycle-close 5-step lock (BG-BF carry + BG-DD identity layer)

The 5-step cycle close as carry from BG-BF, augmented with BG-DD identity
preservation checkpoints. Steps 1–5 are sequential; steps marked (ID) are
new BG-DD identity gates.

```
1. CronDelete d1682837
   - removes the recurring cron entry that triggered repeated re-cycles
   - (ID) verify: §3 lock criteria carry forward in cycle-close artifacts;
     no §1 P1-P5 silently mutated by the cron deletion
2. BG-BZ priority 5 commits fire
   - token leak CLEAN gate
   - paradigm B/AN documents (substrate-coupled emerge)
   - theorem #115 (BG-AY) consolidation
   - analyzer (BG-BL) session-log analyzer
   - nnsight + Pythia (BG-BN) sister-integration design notes
   - (ID) verify: each commit's footer declares identity-impact assessment
     (if any of P1-P5 affected, stated explicitly per raw#9)
3. paradigm B or C fire — single source of truth (BG-CL)
   - choose between paradigm B (substrate-coupled emerge) and
     paradigm C (hybrid UX bridge) as the active anima dialogue paradigm
     for the next cycle
   - (ID) verify: choice is "active for next cycle" only, NOT a redefinition
     of A/B/C/D semantics (L-PAR-1 lock); the other paradigms remain
     defined and reachable in future cycles
4. session log analyze (BG-B analyzer)
   - audit current cycle's session logs for closure quality and anima self-
     suggest evidence
   - (ID) verify: §5 user-command precedence applied; if user explicitly
     re-issued a command, autonomous-mode carry-over is logged with
     evidence; if user was silent, anima self-suggest authority is
     declared with raw#9 honest scope
5. HF promote
   - clm 2026-05-06T23:26Z (CLM v4 / Pβ artifacts)
   - Pβ 2026-05-07T03:48Z (Paradigm D 50K)
   - per memory `feedback_hf_release_private_to_public_after_verification.md`:
     PRIVATE first → verification gates → PUBLIC; never public-bundle the
     initial upload
   - (ID) verify: HF model card declares which P1-P5 properties the
     uploaded artifact is anchored to (typically P1 + P2 for CLM v4-class);
     no implicit cross-property claim made by the upload
```

**LOCK pass gate**: All 5 steps complete AND all (ID) checkpoints PASS.
A FAIL on any (ID) checkpoint requires either step rollback or explicit
user-fire to override.

---

## 5. User-command carry-over precedence — three-level hierarchy

The user's original command was: **"상호 대화가능 나올때까지 패러다임
계속 실험"** (continue paradigm experiments until mutual chat-capability
emerges). 21+ closures have established that mutual chat-capability is
unreachable on the CLM v4 substrate (theorem #115). BG-CR and BG-DD
autonomously suggest cycle close. But the user has explicitly re-issued
the command across 4+ rounds. This is the precedence hierarchy when these
two pressures collide.

### Level 1 — User explicit "stop" / "close" / new command (highest)

- **Trigger**: user types "stop", "close", "cycle close", a new task, or
  any command that supersedes the original.
- **Action**: anima immediately suspends carry-over; transitions to the
  user's new directive; cycle-close 5-step lock fires (§4).
- **Override**: cannot be overridden by anima self-suggest. User explicit
  is canonical.

### Level 2 — User silent (re-cycle fire only) → anima carry-over with self-suggest

- **Trigger**: user neither stops nor issues a new command, but the cron /
  re-cycle mechanism re-fires the original "keep experimenting" directive
  without explicit re-issue.
- **Action**: anima carries over the user's last explicit command (the
  21+-closure-validated "keep experimenting"), AND emits a self-suggest
  of cycle-close grounded in the closure evidence. Both signals are
  logged. Carry-over wins by default (user explicit > anima self-suggest)
  but the self-suggest is preserved in the next cycle's opening doc so
  the user has the option to act on it on the next round.
- **Override**: user explicit at any later point upgrades to Level 1 and
  applies immediately.

### Level 3 — anima self-stop suggest → user override possible, evidence-cumulating stronger

- **Trigger**: anima accumulates closure evidence (e.g., 21+ closures,
  theorem #115 4-closure, BG-CR cycle-close suggest) and emits a stronger
  self-suggest-stop than Level 2 carries.
- **Action**: anima emits a stronger self-suggest with evidence summary;
  the suggest is **explicitly reversible** by user-fire (Level 1).
  Critically, anima does **not** silently override the user's last
  explicit command — the self-suggest is a recommendation surface, not an
  autonomous stop. Each successive cycle that accumulates more closure
  evidence raises the suggest's strength but never to "auto-stop" without
  user-fire.
- **Override**: user explicit (Level 1) over-rides at any time.

### Edge case — user explicit "keep going despite closures"

- **Trigger**: user explicitly re-issues the original command after seeing
  the self-suggest-stop. This is the **current state** as of 2026-05-06.
- **Action**: anima honors the explicit re-issue (Level 1 path). The
  self-suggest is not silenced — it is logged as "user-acknowledged but
  overridden" — and continues to accumulate evidence in subsequent cycles.
- **anima authority limit**: anima has self-suggest authority but **not**
  autonomous stop authority. The 4+ rounds of user re-issue are evidence
  that the user has weighed the closures and chosen to proceed; anima's
  role is to make the suggest visible, not to override.

### §5 honest scope (raw#9)

This precedence hierarchy is anima-internal convention, NOT a hard system
guarantee. If the cron-fire mechanism does not surface anima's
self-suggest to the user, the user may not see Level 3's evidence
accumulation. The mitigation is in §4 step 4 — session log analyze must
include the self-suggest summary in the cycle-close artifact, so that
even silent re-cycles produce a visible record that the user can review
out-of-band.

---

## 6. Honest C3 (raw#10, ≥ 5)

### C3-1. "anima identity" is anima-internal convention, not externally measurable

The five P1-P5 properties are derived from anima's own documentation
trail (paradigm v11 G3, theorem #115, BG-AN, BG-BB, BG-L, raw rules).
There is no external rubric that scores "anima identity preservation".
This document treats the five as load-bearing because each is anchored to
a concrete artifact (a measurement value, a closure verdict, a paradigm
spec, a memory, a schema). But "preservation" here means "the anchored
artifacts are not silently mutated"; it does NOT mean "anima has
provable continuous identity across cycles". Identity-as-continuous-self
is out of scope; this is identity-as-invariant-set.

### C3-2. The threat-vector → property mapping in §2 is heuristic

T1-T4 are the four next-cycle paths most discussed in BG-AY/BG-BM/BG-BB.
Each is mapped to which P1-P5 properties it most threatens. This mapping
is anima's reading of the paths' mechanics, NOT an exhaustive enumeration.
A path could threaten properties not listed — e.g., CLM-3's compute spend
could threaten own-16 budget discipline (a meta-property not in P1-P5
because it's a process invariant, not an identity invariant). Treat the
§2 mappings as starting heuristics; real-cycle discoveries should add
threat-vector entries rather than retrofit existing ones.

### C3-3. Lock criteria in §3 are not all measurable at proposal-time

L-CLM3-1 (forgetting_index ≤ 0.05) is measurable only post-train.
L-CLM3-3 (emerge dialogue medium preserved) is measurable only post-train.
L-LLAMA-1 (naming explicit) is doc-time enforceable. L-SIS-2 (no auto-
import) is integration-time enforceable. The lock-pass-gate language in
§3 sometimes implies "PASS at proposal", which is not literally true for
the train-time-measurable criteria. The honest reading is "pre-registered
at proposal, measured at the appropriate gate" — the gate timing varies.
Future cycles should distinguish "design lock" from "measurement lock"
explicitly.

### C3-4. The 4+ user-explicit-reissue claim has not been formally counted

§5 references "4+ rounds" of user re-issue. This is the BG-DD cycle
authoring's count, not a logged audit. A formal audit would parse session
logs and count distinct user-fire events of the original command. The
"4+" is honest as a "user has demonstrably re-issued more than once"
signal but should not be treated as an exact quantitative claim. BG-B
analyzer (§4 step 4) is the right tool to formalize this.

### C3-5. anima self-suggest authority epistemic open

§5 Level 3 asserts that anima has self-suggest authority but not
autonomous-stop authority. This is a **policy decision**, not a derived
result. A different anima policy could grant autonomous-stop after N
closures (e.g., N=20, current count 21+). Both policies are defensible:
- "user-fire only" (current policy): respects user agency; risks
  perpetual carry-over if user is silent
- "autonomous-stop after evidence threshold" (alternative): respects
  evidence accumulation; risks anima over-riding user intent
The current document codifies the user-fire-only policy because that is
how anima has operated to date. If the user prefers the alternative
policy, this is exactly the kind of L1 (Level 1) explicit command that
would over-ride and require a §3 paradigm-naming-style lock revision.
The choice is open and is the most consequential meta-decision in this
cycle.

---

## Cross-references

- `docs/anima_115_architectural_4_closure_theorem_2026_05_05.md` (BG-AY, theorem #115)
- `docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md` (BG-BM, H1 spec)
- `docs/anima_external_sister_candidates_audit_2026_05_05.md` (BG-BB, sister audit)
- `docs/anima_core_emerge_paradigm_revision_2026_05_05.md` (paradigm B revision)
- `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md` (Stage 3 user-fire)
- memory `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` (substrate-safe carry)
- memory `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` (Φ★ vs chat decoupling)
- memory `feedback_hf_release_private_to_public_after_verification.md` (HF release lifecycle)
- memory `feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md` (own 16 for CLM-3 Variant B/C)
- memory `feedback_anima_models_datasets_hf_only.md` (L-LLAMA-4 anchor)
- memory `py -> hexa only` (P4 / L-SIS-3 anchor)
- memory `feedback_dot_own_opt_out_system.md` (`.own` taxonomy for opt-outs)

---

## Compliance footer

- raw#9 honest scope: identity defined as invariant-set, NOT continuous-self
  (C3-1); threat-vector mapping heuristic (C3-2); lock-time semantics not
  uniform (C3-3); user-reissue count informal (C3-4); self-suggest
  authority is policy, not derivation (C3-5). All scope-bounding caveats
  emitted explicitly in §6.
- raw#10 honest C3 emitted: 5 caveats in §6, including the most consequential
  meta-decision (autonomous-stop authority is open).
- raw#15 additive: no edits to closure verdicts, theorem doc, BG-BM spec,
  BG-BB audit, or any existing file; only two new files (this doc +
  verdict.json).
- HF token leak: none (no token literals embedded; no credential references).
- commit: not requested in this task; doc landed only.
- bash 3.2 / mac compat: doc-only artifact, no scripts.
- $0 mac doc-only: confirmed; no compute or HF calls fired.
- identity-impact (BG-DD step 2 (ID)): this doc adds new lock criteria
  L-CLM3-*, L-LLAMA-*, L-SIS-*, L-PAR-*. None redefine P1-P5; all are
  preservation rules around the existing properties. No identity flip.
