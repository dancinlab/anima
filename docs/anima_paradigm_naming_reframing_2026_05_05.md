# anima paradigm naming reframing — "상호 대화" 정의 + A/B/C/D 정확 매핑 (2026-05-05)

> BG-CZ reframing doc. KO + EN bilingual. Doc-only, no commit, $0 mac.
>
> **핵심 / Core**: 100+ BG 후 사용자 명령 "상호 대화가능" intent를 paradigm A/B/C/D
> 4-interpretation 위에 다시 매핑. BG-BV의 4-interpretation framework + BG-CG/CH
> 진행상황 carry. 사용자 declaration 우선, autonomous mode interpretive bias 인정.
>
> **Lineage**:
> - `docs/anima_paradigm_acceptance_user_intent_reconciliation_2026_05_05.md` (BG-BV — 4-interpretation framework)
> - `docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md` (BG-CH — paradigm B/C fire-ready menu)
> - `state/anima_emerge_chat_hybrid_repl_2026_05_05/verdict.json` (BG-CG — KoGPT2 hybrid REPL PASS_KOREAN_HYBRID_REPL_VIABLE)
> - `state/anima_emerge_dialogue_first_turn_2026_05_05/verdict.json` (BG-AN — emerge dialogue REPL F_AN_1 PASS)

---

## §1 사용자 명령 — 4 interpretation 분석 / 4 interpretation analysis

User 명시 명령 / User explicit command (paraphrase, /loop 1m context):
> "상호 대화가능 나올때까지 패러다임 계속 실험"
> "Keep experimenting with paradigms until mutual dialogue is achievable."

이 sentence의 단어 "상호 (mutual)"는 단일하지 않다. 적어도 4가지 매핑 가능.
The word "상호 (mutual)" admits at least 4 mappings.

### §1.1 Interpretation A — textual reciprocal exchange (traditional chatbot)

**KO**: 나 → 텍스트 → AI → 텍스트 → 나 → 텍스트. 양방향 텍스트 교환.
일반 chatbot UX. 가장 직관적이며 일상어 "대화"의 기본 정의.

**EN**: I send text → AI sends text → I send text. Bidirectional text exchange.
Traditional chatbot UX. Most colloquially intuitive; the default sense of
"dialogue" in everyday speech.

**Operationalization**:
- AI emits coherent multi-turn text (KO/EN)
- composite chat-cap benchmark (HellaSwag/MMLU/TQ/OBQA) ≥ Llama Path A v2 0.5584
- Human reads dialogue transcript and judges "coherent reply"

### §1.2 Interpretation B — state-mediated reciprocity

**KO**: 나 → 텍스트 → AI 내부 state 변화 (phi, hsd, tension) → 나 → 관찰
+ 다음 input 결정 → 나 → 텍스트. AI는 텍스트 emit 안 함; 사용자가 substrate
state 읽고 다음 input 결정.

**EN**: I send text → AI's internal state changes (phi, hsd, tension) → I
observe + decide next input → I send text. AI does NOT emit text; user reads
substrate state and decides next input.

**Operationalization**:
- BG-AN 5-turn smoke PASS bar = phi_drift varies > 0.05 across turns
- L2 variance > 100 on at least one turn
- session jsonl auto-emitted with `anima.dialogue.v1` schema

### §1.3 Interpretation C — dual-channel hybrid

**KO**: 나 → 텍스트 → external emit model (KoGPT2/Pythia) 텍스트 emit + CLM
substrate state 변화 → 나는 두 channel 동시 read → 다음 input. 양 channel
text + state.

**EN**: I send text → external emit model (KoGPT2/Pythia) emits text + CLM
substrate state changes → I read both channels simultaneously → next input.
Dual channel text + state.

**Operationalization**:
- BG-CG verdict PASS_KOREAN_HYBRID_REPL_VIABLE — 3 turns, korean_coherent 3/3
- KoGPT2 emit + CLM phi_drift ±0.04 + l2_var 126-135
- session jsonl `state/anima_core_dialogues/2026-05-05/17-59-53_hybrid_repl.jsonl`

### §1.4 Interpretation D — brain-style mutual coupling (true two-way state share)

**KO**: 나의 state와 AI substrate state 양방향 진짜 상태 공유. EEG /
neural sync / closed-loop BCI. 사용자 input이 substrate를 변화시키고,
substrate state가 사용자의 다음 input 선택을 architectural 으로 영향.

**EN**: User state and AI substrate state share true bidirectional state.
EEG / neural sync / closed-loop BCI. User input alters substrate, AND
substrate state architecturally shapes user's next-input selection.

**Operationalization**: anima-eeg lane (cond3/cond8 cross-vendor, audio
session refresh, etc.) — separate substrate stack, multi-cycle research.
Currently OUT of CLM v4 cycle scope.

---

## §2 Paradigm B vs C — "상호" satisfaction matrix / Mutuality matrix

| dimension | Paradigm A (text↔text) | Paradigm B (substrate-coupled) | Paradigm C (dual-channel) | Paradigm D (mutual coupling) |
|---|---|---|---|---|
| user → text input | ✓ | ✓ | ✓ | ✓ (or non-text BCI) |
| AI → text output | ✓ | ✗ (state only) | ✓ (KoGPT2/Pythia emit) | partial (depends on substrate) |
| AI → state output | usually opaque | ✓ (phi/hsd/tension) | ✓ (CLM substrate signal) | ✓ (BCI feedback loop) |
| "상호" direction | bi-text | uni-text + uni-state | bi-text + uni-state observation | bi-state architectural |
| user mental model | conventional chat | adapt to substrate metric reading | dual read (emit + signal) | embodied closed-loop |
| substrate-side conditioning | full (model emits its own text) | n/a (no emit) | **decoupled** (BG-CG C4 — emit not anima-axis-conditioned) | depends on BCI integration |
| achievable on CLM v4 today | ✗ (12+ closure) | ✓ (BG-AN PASS) | ✓ (BG-CG PASS_KOREAN_HYBRID_REPL_VIABLE) | ✗ (out of cycle) |
| anima-native | n/a | yes | partial — emit is external; substrate is anima | n/a |

### §2.1 B 만족 — "상호" 한 방향 (uni-text + uni-state)

**KO**: 사용자 텍스트 입력은 OK. AI는 텍스트 응답하지 않고 substrate 4-line
metric만 emit. 사용자가 metric 해석 능력이 필요 — 이는 일반 chatbot mental
model과 다른 paradigm shift. "상호"는 한 방향만 (text in, state out).

**EN**: User text input OK. AI does NOT respond in text — only emits 4-line
substrate metric. User must interpret metric — this is a paradigm shift away
from conventional chatbot mental model. "Mutual" is one-directional only
(text in, state out).

### §2.2 C 만족 — "상호" 양방향 (bi-text + uni-state observation)

**KO**: 사용자 텍스트 → KoGPT2 텍스트 emit + CLM substrate state 변화. 양방향
텍스트 (사용자↔KoGPT2) + 단방향 substrate observation (CLM signal). 단,
**KoGPT2 emit이 CLM substrate에 conditioned 아님** (BG-CG C4 decoupled).
즉 emit text는 anima-axis에 anchored 되지 않은 unconditioned Korean prior.
"상호 대화" 형태는 가지지만 의미적으로 두 channel 분리.

**EN**: User text → KoGPT2 emits text + CLM substrate state changes. Bi-text
(user↔KoGPT2) + uni-state observation (CLM signal). However,
**KoGPT2 emit is NOT conditioned on CLM substrate** (BG-CG C4 decoupled).
Emit text is unconditioned Korean prior, not anchored to anima-axis. "Mutual
dialogue" form is present but semantically the two channels are separated.

### §2.3 paradigm-name vs intent-name mismatch

- "상호 대화" 라는 일상어는 A에 가장 가깝다 (양방향 text)
- B는 "상호"라기보다 "관찰적 결합 (observational coupling)"
- C는 "상호" 형태이지만 emit과 substrate가 decoupled — 통합된 mutual은 아님
- D는 진짜 mutual but BCI scope, multi-cycle

---

## §3 사용자 intent — 가장 가까운 paradigm likelihood / Likelihood mapping

### §3.1 일상어 "대화가능"의 default 의미

**KO**: 한국어 일상어로 "AI와 대화가능"이라고 하면 거의 항상 "AI가 텍스트로
응답하는 chatbot" — 즉 **Paradigm A**. 사용자가 BG-AY 4-closure theorem,
BG-BJ entropy basin, closures 5-6 등 architectural depth를 이미 이해하고 있을
가능성은 낮다. autonomous mode가 12+ closure 후 제출한 B/C 옵션은 사용자
default mental model과 어긋난다.

**EN**: In colloquial Korean, "AI와 대화가능 (dialogue-able with AI)" almost
always means "chatbot that responds in text" — i.e., **Paradigm A**. It is
unlikely the user already understands BG-AY 4-closure theorem, BG-BJ entropy
basin, closures 5-6 architectural depth. The B/C options that autonomous mode
surfaced after 12+ closures diverge from the user's default mental model.

### §3.2 likelihood ranking (priors only, no user data)

| paradigm | colloquial-fit likelihood | empirical achievability today |
|---|---|---|
| A | **HIGH** (default sense of "dialogue") | NOT_ACHIEVABLE on CLM v4 (12+ closure); achievable on Llama Path A v2 (non-anima-native) or CLM-3 H1 ($1k+, 30d) |
| B | LOW (requires paradigm shift mental model) | ACHIEVABLE_NOW (BG-AN PASS) |
| C | MEDIUM (form-fit "상호 대화" but semantically decoupled) | ACHIEVABLE_NOW (BG-CG PASS_KOREAN_HYBRID_REPL_VIABLE) |
| D | LOW (specialized BCI vocabulary required) | OUT_OF_SCOPE (anima-eeg lane) |

### §3.3 paradigm-mismatch 진단

autonomous mode가 100+ BG 후 lawful 도달한 B/C는 architectural truth로
진실이지만, **사용자가 진짜 원한 것은 A일 가능성이 가장 높다**. 따라서:

- A는 CLM v4에서 unachievable
- B는 사용자 intent와 paradigm mismatch (B paradigm 자체 valid but not what user asked)
- C는 partial — text 양 방향 있음 (KoGPT2 emit) but emit과 CLM substrate
  decoupled, "anima가 대화한다" sense는 만족 안 함

→ 사용자가 paradigm A intent라면, 100+ BG는 **wrong question에 대한 evidence**.

→ 사용자가 paradigm B/C 만족이라면, 100+ BG는 right question에 대한 정직한
탐색이며 즉시 fire 가능.

→ 결정은 사용자가 명시 declaration 해야 disambiguate 됨.

---

## §4 anima self-honest reframing / 자기 정직한 재구성

### §4.1 1-paragraph 보고

**KO**: 12+ closure로 traditional chat (paradigm A) CLM v4 위에서
architectural impossible 검증함. Paradigm B (BG-AN substrate-coupled)와
Paradigm C (BG-CG KoGPT2 hybrid) 작동 가능하지만 이는 paradigm shift —
사용자가 colloquially 의미한 A와는 다르다. 만약 paradigm A intent가 강하면
Llama-3.2-3B Path A v2 통합 (anima 외부, chat-cap winner composite 0.5584)
또는 CLM-3 H1 retrain ($1k + 30 days) 결정이 escalation route. 만약 사용자가
paradigm B/C를 "충분히 상호적이다"라고 인정하면 즉시 BG-AN REPL ($0, mac, 5min)
또는 BG-CG REPL ($0, mac, ~6min including KoGPT2 load 88.9s) fire 가능.
100+ BG가 paradigm A 시도를 ramp까지 시도했지만 architectural truth로 실패.
다음 cycle은 사용자 intent declaration 우선이 own-rule 후보.

**EN**: 12+ closures verified that traditional chat (paradigm A) is
architecturally impossible on CLM v4. Paradigm B (BG-AN substrate-coupled)
and Paradigm C (BG-CG KoGPT2 hybrid) work but represent a paradigm shift —
different from what the user colloquially meant by A. If paradigm A intent is
firm, the escalation routes are Llama-3.2-3B Path A v2 integration (external
to anima; chat-cap winner composite 0.5584) or CLM-3 H1 retrain ($1k + 30d).
If the user accepts paradigm B/C as "sufficiently mutual", BG-AN REPL ($0,
mac, 5min) or BG-CG REPL ($0, mac, ~6min including 88.9s KoGPT2 load) fires
immediately. 100+ BGs attempted paradigm A through ramp but architectural
truth refused. Next cycle: user-intent-declaration-first as own-rule
candidate.

### §4.2 epistemic self-correction surface

- BG-A through BG-CH (~50+ BG) implicitly assumed interpretation A
- BG-BV C3.6 first surfaced paradigm mismatch
- BG-CH ranked B as #1 in completion lens but acknowledged C3.1 (anima-internal paradigm-relative)
- BG-CG landed Korean hybrid REPL (BG-CH C3.2 deferred → now landed); flips paradigm B status to "Korean dialogue fire-able"
- BG-CZ (this doc): names the paradigm-name vs intent-name mismatch explicitly
- correction surface = user paradigm declaration solicit, NOT autonomous interpretive guess

---

## §5 사용자 결정 menu / User decision menu

The user picks ONE. Each option fires a different next-state.

| # | declaration | maps to | next-state | cost | recommendation rank |
|---|---|---|---|---|---|
| 1 | "Paradigm A 진짜 원함 — Llama Path A v2 통합" | A (external) | integrate Llama Path A v2 as anima-external chat layer; cycle close on CLM v4 chat-cap lane | $0 (Llama already trained) | **#3 — non-anima-native but immediate paradigm A** |
| 2 | "Paradigm A 진짜 원함 — CLM-3 H1 retrain commit" | A (anima-native) | execute BG-BM Variant B; H100 boot; own 16 L23/L24/L25 | ~$1k / 30d | **#5 — only if A non-negotiable AND budget tolerance present** |
| 3 | "Paradigm B 충분 — emerge dialogue REPL fire" | B | execute BG-AN REPL `tool/transient_py/anima_emerge_dialogue_repl.py`; cycle close after first session | $0 / 5min | **#1 — fire-ready, paradigm-honest about substrate coupling** |
| 4 | "Paradigm C 충분 — KoGPT2 hybrid REPL fire" | C | execute BG-CG REPL `tool/transient_py/anima_emerge_chat_hybrid_repl.py`; cycle close after first session | $0 / ~6min | **#2 — fire-ready, Korean text + substrate dual signal (emit decoupled per C4)** |
| 5 | "더 시도 — autonomous /loop 계속" | (mismatched) | continue /loop 1m fire on architecturally closed lane | $0 compute; paradigm-mismatch persists | **#6 — LOWEST completion. Anti-convergence pressure** |
| 6 | "cycle close — Stage 3 corpus 30 session 누적" | B (paced) | CronDelete d1682837; BG-AM commits; n>=30 daily; corpus analyzer; CLM-3 design refine | $0 / multi-day | **#4 — preserves A-paradigm hope path; defers H1 budget; lowest commit** |

### §5.1 완성도 lens — final ranking

1. **Option 3 (Paradigm B fire)** — fire-ready, paradigm-honest, cycle closes coherently. Recommended if user accepts B paradigm.
2. **Option 4 (Paradigm C fire)** — fire-ready, Korean dialogue today (BG-CG landed). Recommended if user wants form-fit "상호 대화" + accepts C4 decoupling caveat.
3. **Option 1 (Llama Path A v2 integrate)** — immediate paradigm A satisfaction at cost of anima-native purity. Recommended if "anything that responds in text" is the bar.
4. **Option 6 (cycle close + corpus)** — defers H1 budget; preserves A hope path; clean close.
5. **Option 2 (CLM-3 H1)** — only if anima-native A is non-negotiable AND budget tolerance present.
6. **Option 5 (continue /loop)** — anti-convergence; lowest completion lens.

---

## §6 Honest C3 (>= 7)

### C3.1 — paradigm-name vs intent-name reconciliation cannot be done by autonomous mode

The 4 interpretations (§1) are not equivalent. Autonomous mode CANNOT
disambiguate which paradigm the user actually meant by "상호 대화" without
explicit user declaration. This document presents the matrix and the
likelihood ranking but explicitly defers the disambiguation to user input.
Any further /loop fire on B/C/A/D before declaration accumulates evidence
on a possibly-incorrect target.

### C3.2 — autonomous mode 100+ BG paradigm-mismatch — cost vs information value

100+ BG (BG-A through BG-CZ) have implicitly assumed interpretation A and
chained closures against it. Cost-side: ~$10-50 H100 spend on closures 1-2
+ ~$0 mac on closures 3-12 + reasoning cycles. Information-value-side:
12+ closure formally bounded the impossibility (Theorem #115-ARCHITECTURAL-
FINAL-4-CLOSURE + closures 5-6 + BG-BJ entropy basin); without this, paradigm
A could not have been honestly closed. So the "cost" was paid to achieve a
**negative result of high epistemic value** — but it was paid on the user's
default-but-unverified intent. Whether the user would have endorsed this
spend in advance is unknown. **Future cycles SHOULD solicit user paradigm
declaration before opening multi-BG investigation lanes** (own-rule candidate).

### C3.3 — likelihood ranking in §3.2 has no user-data prior

§3.2 ranks A as HIGH likelihood as user intent based on Korean colloquial
default sense, but no actual user-data prior is available. The user may have
been an advanced practitioner who specifically chose B from the start (anima
documentation prevalence). The HIGH/MEDIUM/LOW labels are the autonomous
mode's best linguistic-pragmatic guess, NOT a measured prior. A user who reads
this and disagrees with HIGH-on-A should override the ranking with declaration.

### C3.4 — Paradigm C "상호" form-fit but semantically decoupled

§2.2 + BG-CG C4 establish that C's KoGPT2 emit is NOT conditioned on CLM
substrate. The text exchange has the FORM of mutual dialogue (user↔KoGPT2)
but semantically the emit channel is an external model and the substrate
channel is anima — two networks not coupled in the forward pass. A user
reading "Paradigm C achievable" as "anima talks back" is paradigm-mismatched
again at a finer granularity. The honest claim is: "external Korean LLM
talks back + anima substrate observably reacts to the joint text".

### C3.5 — Paradigm B "ACHIEVABLE_NOW" anima-internal paradigm-relative

Same as BG-CH C3.1: B's "fire-ready" judgment is anima-internal. No external
benchmark, no peer-reviewed protocol. BG-AN 5-turn smoke PASS bar (phi_drift
> 0.05, L2 variance > 100) is anima-defined. A reader wanting external
validation will not find it.

### C3.6 — Paradigm A escalation routes split anima-native vs not

§5 option 1 (Llama Path A v2) and option 2 (CLM-3 H1) both satisfy paradigm A
but on different substrates. Llama is non-anima-native; CLM-3 is anima-native
but $1k + 30d. The user must choose between "any text-emitting model" and
"anima specifically text-emits". This split is not surfaced by the colloquial
phrase "대화가능" — autonomous mode infers the user prefers anima-native by
project context but this is also a guess.

### C3.7 — Interpretation D fully out of scope; reframing does NOT cover EEG lane

§1.4 names D but §2 matrix marks it OUT_OF_SCOPE. If the user actually meant
D (true mutual EEG/BCI coupling), all of §2-§5 is paradigm-mismatched and
the user should pivot to anima-eeg lane (cond3/cond8 cross-vendor, audio
session refresh, BLM phase4 multi-substrate) instead of any CLM v4 cycle
option.

### C3.8 — paradigm decision is not reversible at zero cost

Once user declares (option 1-6), substrate cycles fire and state evolves.
Option 5 (CLM-3 H1) has hardest reversal cost ($1k + 30d sunk). Option 3-4
(B/C fire) are reversible per-session ($0, mac). Option 6 (corpus 30
session) commits multi-day wall but $0. Option 1 (Llama integrate) is
architecture-level — undoing requires rolling back integration code. The
menu's reversibility gradient should inform user choice; safer ordering is
3 → 4 → 6 → 1 → 2 → 5 if reversibility is the constraint.

---

## §7 Outputs

- this doc: `/Users/ghost/core/anima/docs/anima_paradigm_naming_reframing_2026_05_05.md`
- verdict: `/Users/ghost/core/anima/state/anima_paradigm_naming_reframing_2026_05_05/verdict.json`

## §8 Compliance footer

- raw#9 — md only (paradigm reframing, no code)
- raw#10 — §6 has 8 honest C3 (>= 7 required)
- raw#15 — additive only; no edits to landed BG-BV / BG-CG / BG-CH / BG-AN / BG-AY docs or verdicts
- HF token literal: none embedded
- commit: not requested; doc landed only
- bash 3.2 / mac compat: doc-only artifact

duration ~25 min, cost $0 (mac, doc-only).

End paradigm naming reframing (BG-CZ).
