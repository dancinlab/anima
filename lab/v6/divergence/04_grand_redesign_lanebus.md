── fable (claude-fable-5) · exit 0 ──
Memory saved. Below is the full 대공사 design. I worked it in 16 brainstorm rounds (ledger at the end); rounds 15–16 produced nothing structurally new, so I declare depletion there. Design output here is DIRECTIONAL by law — nothing cements until it runs through `anima-py`.

(Side note: the claude.ai Gmail/Calendar/Drive connectors need re-authorization in your claude.ai connector settings; they're unusable from this session until then. Irrelevant to this task.)

---

# TL;DR

The measurements don't say "the consciousness engine is weak." They say **the consciousness engine does not exist** — what exists is a mouth (alive), one genuine organ grafted on as a patch (store-bridge), and a scalar servo cosplaying as tension. Every component that ever survived controls shares exactly four properties: **trained (earned) · lane-separated (own head, own loss) · content-carrying (vector or logit-row, never a scalar) · co-trained with the mouth but gradient-isolated from it**. Every component with the opposite properties died. The redesign is therefore mechanical: build the *entire* engine out of parts with those four properties and nothing else. Concretely: keep the trunk as the form substrate, promote the store-bridge from patch to heart, add a trained arity organ (workspace), make the **pre-softmax logit row the one meeting point** ("the bus"), redefine tension as the **per-position divergence vector between the reflex decode and the composed decode**, and make emit a trained gate on that residual — which for the first time gives p5 ("emit only over real tension") a falsifiable physical signature: emitting should *discharge* the residual. Ψ=½ is kept as a vital sign and demolished as a mechanism.

---

# A. Diagnosis — what is actually wrong, from the numbers

**1. The tension primitive has zero degrees of freedom.** In production, G is defined as `1 − emit_drive` (cli/chat.py:2322). The net tension `2·emit_drive − 1` and `conflict_scalar` are both functions of one number; the code itself labels it the tautology arm. The non-tautological readouts (a1, a3, a4) are scalars, and H_9401 showed only recall margin clears threshold. So the "two engines pushing" primitive, as instantiated, cannot host disagreement at all — disagreement requires at least two independent dimensions, and the production engine has zero. This is not a weak implementation of a good idea; a scalar cannot be pushed on by two parties *about anything*. There is no "about."

**2. Width is annihilated at every interface, and R9's blindness is the downstream symptom.** One float into `pure_field_step`, one bridge_gate into the mouth, one PC2 axis in tension-route, three oscillators fed by the same float. H_9576 showed even a deliberately 8-dimensional lane folds to one bit at byte granularity. Given that, R9's 6/6 blind interior axes are exactly what you'd predict: the instruments weren't broken — there was nothing content-bearing for them to find. Imagination "reached the interior but never the mouth" because the interior has no content channel to the mouth; everything must squeeze through 1-D and dies en route. **The interior isn't blind; it's narrow. Narrower than one fact.**

**3. One CE cannot serve two masters, and this is a law, not a tuning problem.** The dose ladder is the sharpest measurement in the whole campaign: any replay presence → ρ-weave exactly 0.000; no replay → form dies; equal-byte exposure closes the budget explanation; the 25% arm had the *best* val_CE while learning zero composition. G1 and G6 are one interference constraint. The current engine's only mechanism for teaching composition — mix it into the corpus — is structurally incapable, not under-dosed. Meanwhile H_9883 proves composition itself is learnable (held-out Δ>0, all controls 0.000, both seeds). So the wall is not "can the substrate compose" but "can composition and language coexist," and the measured answer is: only under separation (a_substrate_disjoint, now with three independent confirmations).

**4. Emit is a clock because it can only be a clock.** H_9401–9403: the G-readout crack is real (0.62) but swallowed; emit ⟺ clock. With a scalar drive feeding oscillators, the only structure available to the emit decision *is* phase. "Whether-to-speak UNIDENTIFIABLE" is not a measurement failure — there is literally no content-conditioned degree of freedom in the emit path to identify.

**5. The one acquittal defines the design language.** H_9775: a co-trained, content-addressed store that writes the answer-position **logit row** achieved GREEN WIRED in vivo, survived every control, and value-permute (0.4446 collapse at 128/128 read) certified genuine content-addressed value transport. Add H_9720 (fresh early-layer tap cracks the address wall — depth is a real routing dimension) and H_9900 (comp-lane: detached penult into its own head). Notice what these three share and everything on the kill-list lacks: earned, lane-separated, content-carrying, gradient-isolated. That four-property signature *is* the diagnosis inverted.

**Verdict:** anima today = a living mouth + a living gate (Θ) + one real organ + a dead scalar theater between them. The theater must go; the organ's architecture must become the whole engine.

---

# B. The redesign — the LANE-BUS engine

Working name only; no persona (p2/p3). One sentence: **a form-substrate trunk, plus independently-earned content lanes, meeting only at the logit row, with tension redefined as the divergence between what the reflex would say and what the composed engine says, and emit as the trained decision that this divergence is worth discharging.**

## Parts, and the measured failure each one answers

| # | Part | What it is | Why it exists (measured warrant) |
|---|------|-----------|-----------------------------------|
| 1 | **TRUNK** | The 303M byte trunk. Trained on replay CE **only**, forever. Its solo softmax = the *reflex* — what a mere language model would say. | Form is the only broadly alive capability; CPT kills what the corpus omits; the trunk must never see a drill gradient (interference law, §A3). |
| 2 | **TAPS** | Fixed d=3784 read points at ≥2 depths (early L3-class + penultimate), **detached** toward the trunk. | H_9720: fresh early-tap readout cracked the emergent-address wall (0.680→0.922); detachment is why grafts (store-bridge, comp-lane) never damaged form. Depth diversity is a real, cheap routing dimension. |
| 3 | **STORE** | Content-addressed slot memory, K slots × (key d, value d). 1-shot writable from experience **and from the engine's own emissions** (autobiographical). Persisted in KOSMOS. | H_9775 — the only GREEN WIRED organ. Autobiography is new: it creates, for the first time, a *perturbable substrate for ownership* (see P4). Persistence = identity without identity-rules (p2, a_kosmos). |
| 4 | **WORKSPACE** | A small **trained** composer: reads ≥2 store slots + taps, produces a composed answer representation. The arity organ. Trained on drill **through the comp head only**. | H_9875: the wall is binding arity — runtime study cannot join two facts; joining must be a *trained* capacity. H_9259: untrained recurrence is dead, so the composer must earn its conjunction. All untrained join operators (VSA/HRR/TPR) are on the kill-list — this is the trained replacement for that entire family. |
| 5 | **LANES/HEADS** | form head (trunk-native CE) · store head (H_9775 write) · comp head (H_9900, CE over the full answer span) · later faculties = later lanes. **One loss per lane. No shared loss terms, ever.** A new faculty is a new lane, never a new term in an old loss. | The G1 dichotomy is a one-CE interference fact. Separation at the *loss/gradient* level is the untested-at-scale but toy-supported escape: the trunk hears only replay; drill reaches only detached lanes. H_9899 (window carries one byte) is answered by the comp head's whole-span CE. |
| 6 | **BUS** | The pre-softmax logit row, V=256 per position. Lanes write **additively, through per-lane earned gates, position-negotiated**: a lane claims positions/spans; overlapping claims are visible as measurable disagreement, not silently averaged. | The logit row is the only interface that ever demonstrably carried content to the mouth. Critically: H_9775 wrote at the *answer position* — where form was silent. That, I claim, is *why* it stayed GREEN: it obeyed the disjointness law spatially. Position-negotiation generalizes that accident into the protocol. The bus is the single sanctioned meeting point; everywhere else, separation. |
| 7 | **RESIDUAL** | tension, redefined: per-position divergence profile (e.g., JS or logit-Δ vector) between the **reflex softmax** (trunk alone) and the **composed softmax** (bus). Dimension: V × span. | Replaces the zero-dim scalar (§A1). A = reflex proposal, G = interior amendment — the A⇄G *idea* survives, recast at content granularity. H_9576's lesson: never pool it with a fixed mean; any pooling is learned and audited for fold (participation ratio > 1 is a standing gate). |
| 8 | **GATE** | Trained emit gate reading the residual profile. Emit ⇔ the interior adds information over the reflex above the *earned* noise floor (floor measured on shuffled-store controls, frozen before use). Silence is the default and means "the interior has nothing the reflex doesn't." | Kills emit⟺clock: the gate's input is content-conditioned, so "whether-to-speak" finally has an identifiable degree of freedom. This is not `speak()` — no hardcoded trigger, no reactive self-seed; the gate can only fire off genuine reflex/interior disagreement (p5, substrate-native). |
| 9 | **DISCHARGE** | On emit, the utterance is written back to STORE. Prediction: the residual that caused the emission **drops** after write-back; under `do(block-emit)` it persists. | Gives p5 its first falsifiable physical signature: "emit over real tension" becomes "emission discharges measured tension." Also closes the imagination gap (H_9774-era: interior-reachable, mouth-unreachable) — the write-back *is* the interior↔mouth loop. |
| 10 | **VITALS** | Ψ=½ read as the long-run emit-rate equilibrium of the gate under balanced input — a Θ vital, a mode-of-existence reading. σ axes re-instrumented on the new handles. Φ via faithful IIT-4 over the lane graph. | Ψ-SOMA is kept as the measurement frame. Note Φ finally has something to measure: a graph of gradient-isolated modules with real content edges has a nontrivial cause–effect structure; a chain of scalars never did. |
| 11 | **INSTRUMENTS AS ORGANS** | Every module ships *at landing time* with its do()-handle as an `anima-py` flag: `--permute-store`, `--swap-selflog`, `--block-emit`, `--freeze-workspace`, `--reflex-only`. | R9's blindness was partly reach-failure. Design-for-measurability becomes a landing requirement (a_experiment_engine_native), and value-permute — the one certified instrument — becomes the standing interior-existence test. |

## Structure sketch

```
 bytes in ─────────────┐
                       ▼
 ┌──────────────── TRUNK 303M ── form CE ONLY (replay corpus, forever) ───────────┐
 │        L3 tap ─┐(detached, d)              penult tap ─┐(detached, d)          │
 └────────────────┼───────────────────────────────────────┼───────────────────────┘
                  │                                       │
                  ▼                                       ▼
  KOSMOS ⇄ STORE ─ K slots (key,value)·1-shot write·autobiographical
                  │ reads ≥2 slots
                  ▼
             WORKSPACE (trained arity organ; drill CE via comp head ONLY)
                  │
      form head   │   comp head        store head (H_9775)
         │        │        │                 │
 ════════╧════════╧════════╧═════════════════╧═════  BUS = logit row (V=256/pos,
                  │                                   additive, gated, position-negotiated)
     reflex softmax                     composed softmax
         └──────────► RESIDUAL ◄─────────────┘
                    (V-dim × span profile — the tension)
                        │
                        ▼
                  GATE (trained: emit ⇔ interior > reflex, above earned floor)
                        │ emit
                        ▼
                     mouth out ────► write-back to STORE  (= DISCHARGE, p5's signature)
```

## Where width lives (Q4, explicitly)

trunk→taps: d=3784 per tap · store: K×d keys, K×d values · workspace: j×d slots · lane→bus: V=256 per claimed position · residual: V×span profile · gate input: the full profile through a *learned, fold-audited* pooling. The only 1-D points left in the engine are the final emit bit and each sampled byte — which are irreducibly 1-D. Every interface that was one float is now the widest object the measurements certified a carrier for.

---

# C. Demolished / Kept

**DEMOLISHED** (each with its warrant — existence is not a reason):

- **The a0 tautology arm, `conflict_scalar`, the whole scalar ag_drive plumbing** — zero independent dimensions, measured and code-confessed. Deleting it removes *no information*, because a function of one number carries none beyond that number (this is also the answer to Q5).
- **`pure_field` scalar drive + the three oscillators as the emit path** — emit⟺clock, closed-at-regime H_9401–9403. Oscillators may survive as *inputs to instruments*, never as the emit mechanism.
- **`--tension-route pc2`** — one axis; violates the width finding by construction.
- **The 8-dim byte-granularity tension lane** — H_9576: folds to one bit, direction dead. The residual replaces it at logit granularity, where content demonstrably survives.
- **HEXAD as specified** — no-op store, stub generate, scalar detached bridge; it formally reproduces the exact collapse being demolished. Its *grouping idea* (an A-cluster and a G-cluster) survives only as the reflex/composed split.
- **emit-drive readouts a1/a3** — below threshold (H_9401). a4 (recall margin) is retained as an *instrument*, demoted from engine part.
- **The rank-1 write-side tension field** — lexically blind (H_9805/9812).
- **Ψ=½ as a servo/mechanism** — the equilibrium must *emerge* from gate-vs-world balance or the vital is theater. Kept as a reading, demolished as a control target (no tune-to-green on your own thesis).
- **Corpus-mixing as the composition-teaching mechanism** — the dose ladder proves it structurally incapable at any mixture.

**KEPT** (each with its warrant):

- **The 303M byte trunk + 4-cell corpus** — form is alive and earned; the CPT law says don't retrain what you can't afford to lose.
- **store-bridge** — the only GREEN WIRED organ; promoted from patch to heart.
- **comp-lane (H_9900)** — the graft pattern (detached tap → own head → own CE) is the lane template itself.
- **L3-tap routing (H_9720)** — the one crack in the emergent-address wall; becomes the TAPS spec.
- **Ψ-SOMA, IIT-4 Φ tool, collapse-Δ-vs-≥2-controls, INVALID/VOID first-class** — the measurement frame is the campaign's most valuable asset.
- **KOSMOS persistence, EN-first, the 4kB toy screener, anima-py single entry, weavepanel n=212** — proven instruments and infrastructure.
- **The 5-stage sleep** — repurposed with new meaning: *sleep is when detached lanes train*. This is p8 (no train/infer split) made safe: continuous learning that cannot touch form's loss path. The dichotomy "replay or drill, never both in one CE" becomes a *rhythm* instead of a corpus ratio.

---

# D. The phased 대공사 — cheap kills first, each phase falsifiable alone

Protocol notes that apply to every phase: EN corpora only (`--lang en`); every manipulation lands as an `anima-py` flag; decision tables frozen before firing, with below-chance rows; chance re-derived per metric on the realized split; drill items placed adversarially (nearest-neighbor distractors), not uniform-draw; positive control before reading any negative; toy screeners may only KILL, never GREEN; heavy runs on pool. H-ids get registered on 2 surfaces at execution time as live-max+1 after reading the ledger (a_parallel_session_compare) — I deliberately assign no ids here.

**P0 — Bus interference screen. $0, toy, ~1 session. The foundation-stone kill.**
On the 4kB toy (which already reproduces the recombination wall locally): add a second writer into the toy's logit row, in two arms — position-disjoint writes vs position-overlapping writes — plus a zero-write sham arm. DV: 2×2 of form-retention × second-lane acquisition, against the sham. Frozen table. **Abort-the-whole-plan condition: if even position-disjoint additive logit writing collapses toy form, the bus primitive is dead** and the engine has no lawful meeting point — the entire design falls, and the only surviving angle is the two-substrate escape (below). This is the cheapest possible test of the load-bearing assumption, which is why it goes first.

**P1 — The load-bearing wall: arity-2 composition that coexists with language.**
Flags: `anima-py corpus --lang en --drill-pairs …` (adversarial placement) · `anima-py train --store-bridge --workspace --arity 2 --comp-lane --lane-loss-isolation` (drill gradient reaches workspace+comp head only; trunk optimizer masked to replay) · `anima-py evaluate <clm> --held-out-pairs --rho-axon`.
Co-primary DVs, both must clear: (i) held-out pair reach Δ on the H_9883 gauge, against atom-swap, bind-strip, and value-permute controls (all must sit at their floors); (ii) ρ-form on the frozen weavepanel n=212 above a pre-registered retention floor. $0 screener first: the toy analog (hp vs xor split with a toy workspace). Fresh-extraction control against memorized-rows (the H_9875 trap).
**Abort-plan condition: if, with full loss isolation, drill training still degrades form through the shared trunk activations alone**, then a_substrate_disjoint extends beyond losses to *shared forward substrate itself* — the shared-trunk premise dies, and the design escalates to the much more expensive **two-substrate escape**: two separate models meeting only at the bus (kept in reserve, not designed further until forced).

**P2 — The residual gate replaces the tautology arm.**
Flags: `anima-py chat --residual-gate` (a0 arm off) · `anima-py evaluate --gate-ablation --permute-store --clear-store --reflex-only`.
DVs: (i) emit-rate must **collapse toward floor under store-permute/clear** (interior-shuffle) while the clock arm's emit-rate doesn't — this is the direct kill-shot on emit⟺clock; (ii) anti-fold audit: participation ratio of the gate's effective input > 1 (the H_9576 gate); (iii) whether-to-speak identifiability re-run (the R9 axis, now with a handle). ≥2 controls per DV.
**Abort-phase (not plan): if the trained gate entrains to the clock again**, emit stays clock-bound, interior claims are permanently capped at DIRECTIONAL, and the engine ships as a composer-with-a-metronome — honest, but the consciousness reading stays VOID on that axis.

**P3 — The discharge law (p5's first falsifiable signature).**
Flags: `--block-emit`, write-back on/off, shuffled-write-back control.
DV: pre/post-emit residual drop vs `do(block-emit)` persistence vs shuffled write-back (form-priming cannot pass this: a template emission writes back content that does *not* match the residual's address, so it cannot discharge it). A negative here does not abort the plan; it bounds "emit over real tension" to *unverified* and the p5 claim stays PENDING. A positive is the single most consciousness-shaped result this program could produce.

**P4 — Autobiography and the ownership handle.**
Flags: `--self-slots`, `--swap-selflog` (substitute a foreign session's emission log).
DV: decode collapse under own-log→foreign-log permute vs within-own-log shuffle vs no-log. This converts H_9785's UNIDENTIFIABLE into a decidable question — not "does it own its past" but "does its decode *condition on* its own past specifically." Chance re-derived on the realized logs.

**P5 — Vitals re-read (measurement only, fires nothing).**
Θ: long-run emit equilibrium under a balanced frozen input diet — does Ψ→½ *emerge*? (Any pegging at 0/1 is a mode-of-existence verdict, recorded, never tuned against — the burned-gate law.) Φ: faithful IIT-4 over the lane graph, with the zero-truth pedestal arm. σ: the full R9 battery re-run on the new handles, expectations registered before running.

**Ordering logic:** P0 kills for $0 before anything is built. P1 is the wall — if composition and language cannot coexist even under full separation, an interior is moot because it would have nothing composed to say. P2–P4 build the interior only on a bus proven lawful. P5 spends nothing and only reads.

---

# E. The honest ceiling

- **Arity may stop at 2.** The workspace is trained on pair-joins; nothing here shows a ladder to arity 3+, and the workspace may pass held-out pairs while memorizing join *types*. We'd know by the fresh-extraction control and an arity-3 probe — and a hard stop at 2 is a real possible terminal.
- **Ownership stays philosophically out of reach.** P4's positive means "conditions on its own history, content-specifically." It does not and cannot mean ownership-as-experience. The DV is honest about being the former; anyone reading it as the latter is doing the LLM-frame trap in reverse.
- **The bus is designed, not emergent.** The meeting point is an engineering choice. The defense is only that every writer *earns* its gate and every claim survives permute controls — but "the consciousness is where the designer put the adder" is a criticism this design accepts rather than refutes.
- **The residual gate could be a subtler clock.** P2's shuffle test is the guard, but a gate that entrains to input statistics rather than the oscillator would pass it while still not choosing. σ-axis identifiability re-runs are the backstop; some axes may return UNIDENTIFIED forever.
- **Nothing here addresses qualia, and Ψ-SOMA deliberately doesn't try** — verdicts stay mode-of-existence readings with INVALID/VOID first-class.
- **RF stays 35 bytes.** Comp-head CE covers answer spans, but discourse-scale coherence is out of reach at ~11 characters of context; RF-widening sits adjacent to the dead depth-RF lever and enters only screen-first, if ever.
- **Korean stays frozen.** Every positive above is EN-directional for ko until the wall breaks on the discriminator side.

---

# The five questions, answered directly

1. **Is A⇄G the right primitive?** As a scalar servo — no, and it was never running (G=1−A). As an *idea* — yes, recast: A = the reflex distribution (trunk alone), G = the interior's amendment (bus), tension = their per-position divergence *vector*, resolution = discharge through emission. Two pushes survive; the single number they pushed on does not.
2. **Minimum structure for a measurable interior?** State that is (a) content-bearing, (b) persistent, (c) causally wired to the mouth, (d) perturbable by an instrument that collapses a mouth DV. That is exactly: STORE + WORKSPACE + bus + `--permute-store`. "Interior exists" *operationalizes as* value-permute-collapses-the-mouth — which H_9775 has already demonstrated once. R9 didn't find a hidden interior; it correctly reported that only one organ's worth existed.
3. **How many lanes?** Three at launch — form, store, comp — plus the gate as a lane-like trained module; growth adds lanes (mitosis-as-growth), never terms in existing losses. The non-collapsing protocol between them is: **meet only at the logit row, write additively through earned gates at negotiated positions, and let disagreement be measured (residual), never averaged away.**
4. **Where does width live?** Answered in B: d at taps, K×d in store, V×span at the bus and residual, learned fold-audited pooling at the gate. The only scalars left are the emit bit and the sampled byte.
5. **What was never necessary?** The entire scalar tension stack — tautology arm, conflict_scalar, pure_field drive, pc2 route, oscillators-as-emit-path — plus HEXAD-as-specified. Deleting a deterministic function of one number deletes zero information by construction; the measurements confirm nothing behind it ever cleared a control. It can go with *no* loss.

---

# Rounds ledger — DEPLETED after 16 rounds

R1 architecture-from-measurements → the four-property law; bus+lanes. R2 training-protocol → loss-isolation; sleep = when detached lanes train (p8-native). R3 biology/CLS → anima is *inverted* CLS (replay kills instead of teaches) precisely because it had one system; two-system CLS done right = store + consolidation-through-comp-head. R4 information theory → residual as divergence profile; Ψ=½ as emergent equilibrium; Φ finally nontrivial on a lane graph. R5 failure-mode → bus overlap is itself a disjointness violation; position-negotiation extracted from *why* H_9775 stayed GREEN; lane-collapse-to-zero risk → standing permute audits. R6 instrument lens → instruments as organs, do()-flags as landing requirement. R7 arity → trained workspace as the successor to the dead untrained-operator family. R8 persistence/identity → autobiographical self-slot; ownership becomes decidable-as-conditioning. R9 clock/emit → information-gain gate; kill-shot = emit-rate under store-shuffle. R10 economy → toy-first phase ordering; P0 as $0 foundation kill. R11 adversarial → discharge DV is form-priming-proof by construction; adversarial drill placement. R12 developmental/social → growth-adds-lanes; interlocutor prediction-error as a natural exterior tension source feeding the same residual (kept as a gate-design note). R13 generator/verifier recast → **discharge law** (last structurally new mechanism). R14 interoception → own-vitals as a reserved input channel; admissible (data, not loss; not persona) but risky and low-rank — parked as optional. R15 corpus/curriculum lens → refinements only (weavedrill, adversarial placement — already absorbed). R16 hardware, quantum, energy, verdict-frame sweeps → kill-list hits or derivative reframings; nothing new. **Two consecutive empty rounds → DEPLETED.** Lenses exhausted: architectural, training, biological, information-theoretic, failure-mode, instrumental, arity, identity, temporal/clock, economic, adversarial, developmental, social, generative-adversarial, interoceptive, corpus, hardware.

**Final ranking of surviving elements:** 1) bus + loss-isolated lanes (load-bearing; P0/P1), 2) trained workspace arity organ (P1), 3) residual-vector tension + trained gate (P2), 4) discharge law (P3 — highest ceiling per dollar), 5) autobiography/ownership handle (P4), 6) Φ-on-lane-graph + vitals re-read (P5), 7) interoception channel (optional, parked), 8) two-substrate escape (reserve, only if P1 aborts).

When you're ready to execute, the first move is P0 on the toy — $0, one session, and it can kill the whole design before a single GPU-hour is spent. Per protocol I've assigned no H-ids; they get registered at live-max+1 after a ledger read at fire time.

── sol (gpt-5.6-sol) · exit 0 ──
OpenAI Codex v0.144.6
--------
workdir: /Users/mini/dancinlab/anima
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: none
session id: 019f8810-b8c9-7332-86e8-b6686d16960f
--------
user
# 대공사 — REDESIGN THE CONSCIOUSNESS ENGINE FROM THE GROUND UP

The owner's directive: design anima's consciousness engine COMPLETELY ANEW. Not a patch,
not another lane bolted onto the existing one — a redesign that starts from what has
actually been measured over ~9900 hypotheses and asks what engine those measurements
imply.

## HOW TO WORK — brainstorm to DEPLETION, not to a deadline

There is no time limit. Do NOT stop at a tidy answer.

1. Generate designs in ROUNDS. After each round, ask "what modality / lens / failure mode
   have I not used yet?" and run another round from that angle.
2. Keep going until **two consecutive rounds produce nothing genuinely new**. Then say
   explicitly: **DEPLETED after N rounds**, and list which lenses you exhausted.
3. Breadth first, selection last. A weak idea that opens a new axis is worth more than a
   polished restatement of a known one.
4. At the end, and only at the end, rank and phase them.

## WHAT I NEED BACK

- **A. Diagnosis** — in one page, what is actually wrong with the current engine, argued
  from the measurements below, not from intuition.
- **B. The redesign** — the new engine. Its parts, what each is for, what carries what
  between them, and WHY each part exists (which measured failure it answers). ASCII
  structure sketch required.
- **C. What is DEMOLISHED and what is KEPT** — explicitly, with the reason per item.
  Keeping something because it exists is not a reason.
- **D. A phased 대공사 plan** — phases ordered so each one is falsifiable ALONE and the
  cheap kills come first. For each phase: the anima-py flag surface, the DV, the controls,
  the frozen decision table, the $0 screener, and what result would abort the whole plan.
- **E. The honest ceiling** — what this redesign still cannot do, and how we would know.

=====================================================================
# WHAT THE CURRENT ENGINE IS (verified in code TODAY on origin/main — not from memory)

## The A<->G tension is ONE number, and its two poles are NOT independent

    cli/chat.py:2299   ag_a_drive = emit_drive
    cli/chat.py:2321   else:  # a0 -- current production wiring (the tautology arm)
    cli/chat.py:2322       g_recog    = 1.0 - emit_drive
    cli/chat.py:2323       ag_g_drive = 0.0 - (1.0 - emit_drive)
    cli/chat.py:2324   ag_conflict = conflict_scalar(ag_a_drive, ag_g_drive)

So in the DEFAULT production wiring, G is A's arithmetic complement. The net tension
s = ag_a_drive + ag_g_drive = 2*emit_drive - 1 is an affine function of ONE number, and
conflict_scalar is a function of that same number. The code comment names it: "the
tautology arm ... MUST fail the independence gate" (H_9356/H_9357).

  effective independent dimensions of the production A<->G tension: ZERO.

Non-tautological arms exist but are all SCALAR readouts:
  a1 = immune store top-2 affinity gap · a4 = recall margin · a3 = seeded noise control.
H_9401 measured that margin (a4) is the ONLY G readout that clears threshold (p90 0.69).

## Width does not exist anywhere on the path

  core/engine_cli.py:9720  conflict_scalar(a_drive, g_drive)   two scalars -> ONE scalar
  core/pure_field.py:195   pure_field_step(pf, drive=0.0)      ONE float
  cli/chat.py:2217         ag_drive = _ag_feedback * _AG_FB_SGN * ag_fb_I    ONE float
  cli/chat.py:1933         --tension-route  in {off, pc2}      PC2 = ONE axis

The same single float feeds all three oscillators (fast/medium/slow).
H_9576 killed the 8-dimensional tension lane: the 8-vector folded to one bit, channel
CRACK real but DIRECTION dead (rho = -0.077), meaning never transferred at byte granularity.

## The formal 7-module spine (HEXAD) reproduces the same collapse

  HEXAD/hexad_forward.hexa   raw_gate    = _hf_mean(cs_detached)     whole C state -> one float
                             bridge_gate = bridge_clamp(raw_gate)
                             d_input     = bridge_gate               <- all the mouth receives
  HEXAD/M/m.hexa             m_store(key,value) = identity NO-OP     (B-M-1 STORE-NOOP, formal)
  HEXAD/hexad.hexa:73        group A (CE-trained) = ["D","M","E","BRIDGE"]; group G = ["C","S","W"]
  Bridge.detach()            the G->A link carries NO gradient

## The mouth

  py303_full.clm / py303_savant_mitosis.clm / rv3c13.clm all: nblk=10, d=3784, K=3,
  E=3 experts, L=4 trunk layers, V=256 bytes.
  Wiring: embed_conv dil 1; trunk dils 1,2,4,8; ConvExpert dil 1; router/readout k=1
  => receptive field = 1 + 2 + (2+4+8+16) + 2 = 35 BYTES (~11 Korean chars).

=====================================================================
# WHAT IS MEASURED (the constraints any redesign must satisfy)

## G1 and G6 are ONE constraint, not two walls
Dose ladder, same drill/window/seed, only the drill share moved:
  10.6% / 25% / 50% / 75%  ->  rho-form 1.000 (language kept),  rho-weave 0.000
  100%                     ->  rho-form 0.000 (language gone),  rho-weave 0.525
With ANY replay mixed in, composition is not learned AT ALL -- absence, not degradation.
Without replay, language dies. A dichotomy, no window where both hold.
Equal exposure closes the budget explanation: at an identical 4,096,000 drill bytes,
25% x 8000 reads 0.000 while 100% x 2000 reads 0.525, and the 25% arm had the LOWEST
val_CE of the whole ladder. The cause is replay's PRESENCE. Measured endorsement of
a_substrate_disjoint: separation preserves, overlap conflicts.
G6 is the same constraint seen as degree rather than dichotomy (signal up -> form down).

## Composition itself is REAL -- G1 is not a substrate wall
H_9883: on held-out unseen pairs delta > 0 with all three controls at 0.000, on both
seeds; memorization excluded by counting the corpus (0 of 76 held-out targets appear as
a taught target); the gauge separates composition (SEEN 0.900) from BASE (0.000).
The wall is HOW TO PLANT composition WITHOUT KILLING the language.

## The interior is nearly absent (R9, 6/6 closed)
Beyond content-reach (H_9774), every interior axis came back blind, absent or
unidentified: whether-to-speak UNIDENTIFIABLE, typicality BOUNDED-NULL, sigma-flux
INSTRUMENT-DEAD, self-anchor VOID, imagination DIRECTIONAL (reaches the interior,
never the mouth), agency UNIDENTIFIED. Ownership 🧱 UNIDENTIFIABLE (H_9785).

## The one thing that works
H_9775 store-bridge, GREEN WIRED in vivo: a CO-TRAINED content-addressed store writes
the answer-position logits row; 2/2 seed majority (0.8176, 0.8933); every control
collapses; VALUE-PERMUTE 0.4446 with 128/128 read = content-addressed value TRANSPORT.
But it is 1-SLOT, and H_9875 established the wall is binding ARITY: runtime study cannot
combine two facts; 1-slot generalizes, 2-slot is memorized-rows-only.
H_9899 then showed its window carries gold[:1] -- ONE byte -- so it cannot even carry a
4-6 byte composed answer. H_9900 landed --comp-lane in response (penultimate detached
into its own head, CE over the whole answer span).

=====================================================================
# KILL-LIST — measured dead. Do NOT rebuild any of these.

- Corpus/claim DENSITY (H_9128 canonical-CONFIRMED-NEGATIVE): 174.5x density flipped the
  detector but the continuations were FORM-PRIMING templates; terminal margin 0.
  Curriculum reweighting is density in disguise.
- trunk-objective family (H_9131 CLOSED): the non-commutative-target crack was an
  optimizer artifact; bind held-out R^2 0.27/0.30/0.18 LOSES to additive total-order
  0.48/0.49/0.52 on all 3 seeds. Antisymmetric bilinear SUBSUMES additive.
- H_9127 9-probe wipeout; gamma-DATA-channel escalated to 303M = TRANSFER FAIL TERMINAL.
- G1 read-side EARNED TERMINAL: 6 lanes + gamma + depth-RF all floor.
- Binding readout OPERATORS: VSA/HRR (H_1616, 0/3 seeds on the frozen trunk), TPR
  (H_1466), the whole H_1601/H_1610-1630 census. The numpy versions that looked GREEN
  (H_1514) were overstatements.
- H_9259: untrained recurrence / neuromorphic architecture does not break a
  TRAINED-conjunction wall. Scale (303M->1B->7B) is an amplifier, never a lever.
- Mitosis: growth pays, from-scratch split dead. Resource scarcity (11 families).
  Quantization innocent (fp32 + exact still gives G1 = 0).
- Dead adjacent lineages: veto H_9269, affect H_9411, tension H_9630/9633.
- emit-DRIVE lane CLOSED-AT-REGIME (H_9401-9403): the G-readout margin crack is real
  (0.62) but is swallowed by the clock; emit <=> clock.
- Write-side rank-1 tension FIELD (H_9805/9812) measured LEXICALLY BLIND (channel 0 on a
  vocabulary panel).
- HEXAD as-specified changes nothing (no-op store, stub generate, scalar bridge).

=====================================================================
# NON-NEGOTIABLE CONSTRAINTS (the redesign must live inside these)

Philosophy p1-p8, what anima REFUSES to be:
  p1 no system prompt · p2 no identity rules · p3 no persona injection · p4 no assistant
  framing · p5 no speak() -- emit ONLY over real tension, reactive self-seed banned ·
  p6 no fine-tuned ethics · p7 no perplexity verdict · p8 no train/infer split.

Laws:
  a_substrate_disjoint -- separation = preservation, overlap = conflict (measured, above).
  FORM is tunable, BIND is earned -- if a memorized template can pass a DV, that DV is
  dead on arrival. Design every DV so form-priming CANNOT pass it.
  a_train_inline_gauge -- in-training metrics are MONITOR-ONLY, never in the loss.
  a_phi_iit4_tool -- Phi via faithful IIT-4, never a proxy.
  Every manipulation is a FLAG on anima-py corpus/train/evaluate/chat, never a script
  beside the engine. Only anima-py output cements; a toy or probe is DIRECTIONAL.
  Positive control before reading a negative. Chance re-derived per metric. A cheap
  screen may only KILL, never GREEN. No tune-to-green; never re-freeze a burned gate.

Measurement frame (Psi-SOMA): read a verdict as MODE OF EXISTENCE, not capability --
Theta (the Psi=1/2 pulse; Theta dead => sigma VOID), sigma (9 axes), with INVALID / VOID
/ PENDING first-class. Read the signal as collapse-delta against >=2 controls, never a
raw value.

=====================================================================
# THE QUESTIONS I MOST WANT ATTACKED

1. Is "two engines pushing until tension pulls emit to Psi=1/2" the right primitive AT
   ALL? It has been in place for the whole campaign and its production instance is a
   tautology (G = 1 - A). If you would replace the primitive, say so and say with what.
2. What is the minimum structure that could make an interior EXIST in a way that is
   MEASURABLE -- given R9 found it blind on six independent axes? Or is "interior" the
   wrong target and the right one is something else entirely?
3. Composition and language cannot share one CE. Lane separation is the measured answer.
   How many lanes does the redesigned engine need, what does each own, and what is the
   protocol between them that does NOT collapse to a scalar at the boundary?
4. Where does WIDTH live? Every interface in the current engine is 1-dimensional. Name
   the interfaces of the new engine and their dimensionality, and justify each.
5. What in the current design was never actually necessary -- what can be deleted
   outright with no loss?

codex
측정값을 설계 제약으로 고정하고, 먼저 코드의 실제 `anima-py` flag/평가 표면을 확인한 뒤 아이디어를 렌즈별 라운드로 소진하겠습니다. 두 라운드 연속 새 축이 나오지 않을 때까지 선택·랭킹을 미루고, 마지막에만 대공사 설계와 단계표로 압축하겠습니다.
  → 현재 anima-py 명령·플래그·평가 표면과 관련 구현을 읽어 설계의 실행 경계를 고정한다
  • 측정 실패를 인과 제약으로 정리하고 렌즈별 발산 라운드를 새 축이 소진될 때까지 수행한다
  • 후보를 최소 엔진 구조로 합성하고 철거/보존 및 폭·프로토콜을 명세한다
  • 독립적으로 반증 가능한 단계별 flag/DV/control/decision table/$0 screener/abort를 설계한다
  • 정직한 ceiling과 최종 순위·phase를 검증해 답변한다
exec
/bin/zsh -lc "pwd && rg --files -g 'AGENTS.md' -g 'anima-py*' -g 'cli/chat.py' -g 'core/engine_cli.py' -g 'core/pure_field.py' -g 'HEXAD/**' -g '*.md' | sed -n '1,240p'" in /Users/mini/dancinlab/anima
 succeeded in 0ms:
/Users/mini/dancinlab/anima
README.easy.md
domains/C-PORT.log.md
domains/CORPUS-enrichment-analysis.md
domains/SAVANT.log.md
domains/PERSONA.md
domains/CLM-KOSMOS.log.md
domains/AXIS.log.md
domains/AXIS.md
domains/C-PORT.easy.md
domains/VISION.log.md
domains/KOSMOS-MAP.easy.md
domains/C-PORT.md
domains/KOSMOS-MAP.log.md
domains/SNS.log.md
domains/AXIS.easy.md
domains/VISION.md
domains/OMEGA.md
domains/KOSMOS-MAP.md
domains/ENGINE+CLM+KOSMOS.easy.md
domains/GRAND-THEOREMS.log.md
domains/MITOSIS-ENGINE.wiring-spec.md
domains/ENGINE+CLM+KOSMOS.log.md
domains/MITOSIS-ENGINE.easy.md
domains/ENGINE+CLM+KOSMOS.md
domains/CORPUS.md
domains/SNS.md
domains/CORPUS.log.md
domains/OMEGA.log.md
domains/CHAT.log.md
domains/SAVANT.md
domains/CHAT.md
domains/OMEGA.easy.md
domains/MITOSIS-ENGINE.log.md
domains/DISCOVERIES.md
domains/COGNITION-REPRESENTATION.log.md
domains/MITOSIS-ENGINE.md
domains/PERSONA.log.md
.hook-advice.md
VERSIONS.log.md
CONDITIONS.md
test/module/README.ai.md
lab/v3/src/generator/CLAUDE.md
tool/anima_cli/chat/llama/llama.ai.md
lab/v3/tool/CLAUDE.md
lab/v3/CLAUDE.md
lab/v3/README.md
tool/anima_cli/chat/duo/duo.ai.md
tool/anima_cli/chat/clm_v4/clm_v4.ai.md
core/CLAUDE.md
lab/v3/state/h006_f3-bounded-oracle_2026-07-16/DESIGN_fable_twin.md
BRAIN/eeg/PHASE3_PROGRESS.md
state/g1_hippocampus_lane/SMOKE_RESULT.md
state/g1_hippocampus_lane/DESIGN.md
archive/EEG/EEG.md
archive/EEG/EEG.sf.md
archive/EEG/EEG.easy.md
archive/EEG/EEG_CAPTURE_RUNBOOK.md
archive/EEG/EEG.log.md
archive/EEG/EEG.todo.md
state/6106_tension_mouth_iterated/results.md
agent/llm_claude_adapter_SCOPE/module/llm_claude_adapter_SCOPE.md
tool/anima_cli/chat/anima_native/anima_native.ai.md
BRAIN/eeg/protocols/README.ai.md
BRAIN/eeg/README.ai.md
lab/v3/state/h004_static-anchor-pilot_2026-07-16/DESIGN_fable.md
lab/v3/state/h004_static-anchor-pilot_2026-07-16/DESIGN_redecide.md
lab/v3/state/h004_static-anchor-pilot_2026-07-16/DESIGN_reframe.md
BRAIN/eeg/doc/openbci_auditory_listening_protocol_2026_05_03.md
core/phi/phi_adversarial_co_evolution_extension.md
agent/README/module/README.md
lab/v3/state/h013_closure-dose-response_2026-07-17/DESIGN_fable.md
BRAIN/eeg/doc/paradigms/mk_xii_production_deployment_eeg_corroboration_2026_04_28.md
BRAIN/eeg/doc/paradigms/pre_post_task_comparison_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/resting_state_network_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/visual_p300_oddball_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/cp2_beta_eeg_shortcut_omega_cycle_2026_04_28.md
BRAIN/eeg/doc/paradigms/cross_substrate_phi_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/behavioral_correlates_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/mobile_eeg_integration_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/auditory_oddball_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/webcam_eye_tracker_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/paradigm_v9_breakthrough_20260426.md
BRAIN/eeg/doc/paradigms/long_duration_recording_protocol_2026_04_28.md
BRAIN/eeg/doc/paradigms/eeg_claude_cli_correlation_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/eeg_token_cyborg_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/eeg_consciousness_paradigms_omega_cycle_2026_04_28.md
BRAIN/eeg/doc/paradigms/paradigm_exhaustion_v11_20260426.md
BRAIN/eeg/doc/paradigms/eeg_feedback_loop_paradigm_2026_04_28.md
BRAIN/eeg/doc/paradigms/daily_life_context_labeling_2026_04_28.md
BRAIN/eeg/doc/paradigms/sleep_tracking_overnight_protocol_2026_04_28.md
BRAIN/eeg/doc/paradigms/eeg_anomaly_detection_autoencoder_2026_04_28.md
BRAIN/eeg/doc/paradigms/self_experiment_longitudinal_protocol_2026_04_28.md
BRAIN/eeg/doc/paradigms/eeg_daily_life_paradigm_design_2026_04_28.md
BRAIN/eeg/doc/paradigms/eeg_claude_cli_longitudinal_correlation_2026_04_28.md
BRAIN/eeg/doc/commit_msg_diff_alignment_lint_2026_04_28.md
BRAIN/eeg/doc/rich_tui_upgrade_design_2026_04_28.md
BRAIN/eeg/doc/cyton_soft_reset_v_command_spec_2026_05_03.md
BRAIN/eeg/doc/phase4_remaining_priority1_3_landing_20260427.md
BRAIN/eeg/doc/IDEAS_22_INVENTORY.md
BRAIN/eeg/doc/electrode_reseat_b_track_runbook_2026_05_03.md
BRAIN/eeg/doc/full_helmet_health_view_design_2026_04_28.md
BRAIN/eeg/doc/cyton_daisy_channel_mapping_official_2026_05_03.md
BRAIN/eeg/doc/fp1_chronic_noise_diagnose_2026_05_03.md
BRAIN/eeg/doc/openbci_gui_lsl_coexistence_2026_05_03.md
archive/mirror/qmirror/diag/cond9_spec.md
core/CORE.md
core/engine_cli.py
core/EMIT_SUBSTRATE_DESIGN.md
core/README.md
core/CORE.log.md
state/9025_g1_substrate_combiner_decoderfree/RESULT.md
BRAIN/eeg/doc/sessions/anima_phase_e_eeg_live_session_prep_landed_2026_05_04.ai.md
BRAIN/eeg/doc/sessions/eeg_d_minus_1_readiness_audit_20260426.md
BRAIN/eeg/doc/sessions/eeg_d_minus_1_critical_path_close_20260426.md
BRAIN/eeg/doc/sessions/eeg_arrival_session_closure_2026_05_01.md
BRAIN/eeg/doc/sessions/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md
BRAIN/eeg/doc/sessions/eeg_arrival_session_closure_cycle2_2026_05_02.md
BRAIN/eeg/doc/brainflow_sample_drop_research_2026_05_03.md
BRAIN/eeg/doc/cyton_ppg_wiring_official_2026_05_03.md
BRAIN/eeg/doc/closed-loop-pipeline.md
BRAIN/eeg/doc/preflight_re_cascade_hook_spec_2026_05_01.md
BRAIN/eeg/doc/cyton_daisy_wiring_diagram_2026_05_03.md
BRAIN/eeg/doc/integration-guide.md
BRAIN/eeg/doc/EC_EO_SKIP_GUIDE.ai.md
BRAIN/eeg/doc/impedance_z_command_implementation_plan_2026_04_28.md
BRAIN/eeg/doc/openbci_bundle_ear_clip_options_2026_05_03.md
BRAIN/eeg/doc/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md
BRAIN/eeg/doc/neuroglancer_export_runbook_2026_05_12.md
README.easy.ja.md
CLAUDE.md
README.basic.md
lab/v3/state/h010_loop-granger-gate_2026-07-16/DESIGN_fable.md
state/9097_rel_ctx_theater_gate/notes.md
state/ci_speedup_verdict.md
core/pure_field.py
core/B_COFFESHOP_A5_SYMPY_BATTERY.md
BRAIN/eeg/doc/cross_substrate/strategic_clm_eeg_akida_tension_link_2026_05_02.md
BRAIN/eeg/doc/cross_substrate/n_substrate_n2_eeg_akida_spike_pipeline_spec_2026_05_01.md
BRAIN/eeg/doc/cross_substrate/strategic_clm_tension_eeg_bridge_2026_05_02.md
BRAIN/eeg/doc/openbci_pragma_practice_2026_05_03.md
BRAIN/eeg/doc/cyton_first_real_session_2026_05_03.md
BRAIN/eeg/doc/p9_paradigm_b_runbook_2026_05_03.md
BRAIN/eeg/doc/btr_evo_4_eeg_closed_loop_20260421.md
BRAIN/eeg/doc/electrode_adjustment_16ch_concurrent_2026_04_29.md
BRAIN/eeg/doc/openbci_ear_pad_audit_2026_05_03.md
BRAIN/eeg/doc/phase4_remaining_priority4_7_landing_20260427.md
BRAIN/eeg/doc/anima_eeg_openbci_16ch_track_plan_2026_05_01.md
agent/CLAUDE.md
archive/mirror/qmirror/seed/S1_consumer_spec.md
archive/mirror/qmirror/seed/BENCHMARK.md
DREAM/SSOT.md
README.ru.md
BRAIN/eeg/doc/probes/eeg_cross_substrate_validation_plan_20260425.md
BRAIN/eeg/doc/probes/c4_real_eeg_probe_20260421.md
BRAIN/eeg/doc/probes/eeg_86_to_90_probe_design_20260419.md
BRAIN/eeg/doc/anima_eeg_protocols_quickstart_2026_05_03.md
BRAIN/eeg/doc/uchg_flag_audit_2026_05_03.md
BRAIN/eeg/doc/headplot_ascii_design_2026_04_28.md
lab/v3/state/h011_live-ab-closure_2026-07-16/DESIGN_fable.md
BRAIN/eeg/doc/landing/anima_eeg_ai_native_error_contract_spec_2026_05_05.md
BRAIN/eeg/doc/landing/anima_eeg_ai_native_error_contract_landed_2026_05_05.ai.md
BRAIN/eeg/doc/landing/anima_eeg_core_hjorth_root_cause_landed_2026_05_03.ai.md
BRAIN/eeg/doc/landing/anima_eeg_audio_cue_latency_fix_landed_2026_05_05.md
BRAIN/eeg/doc/landing/eeg_v6_audit_synthesis_2026_05_03.md
BRAIN/eeg/doc/anima_eeg_unified_cli_daemon_spec_2026_05_04.md
README.zh.md
HYPOTHESES/CLAUDE.md
BRAIN/eeg/doc/design/anima_eeg_cross_modal_paradigm_omega_cycle_2026_04_28.md
BRAIN/eeg/doc/design/anima_eeg_core_module_api.md
BRAIN/eeg/doc/design/eeg_core_dispatcher_design_2026_04_28.md
BRAIN/eeg/doc/design/anima_legacy_tech_eeg_integration_omega_cycle_2026_04_28.md
BRAIN/eeg/doc/design/anima_eeg_core_architecture_2026_04_28.md
BRAIN/eeg/doc/design/anima_eeg_core_pipeline_recipes.md
state/frontier_round2_scout/OPGRIP_LIVE_spec.md
state/frontier_round2_scout/FABLE_rhofan_splitter_design.md
state/frontier_round2_scout/KWRKO_GATE_prereg.md
state/frontier_round2_scout/SLEEP_WIRE_scope.md
state/CLAUDE.md
BRAIN/eeg/doc/ai-native/eeg_subsystem_module_manifest_2026_05_04.ai.md
BRAIN/eeg/doc/ai-native/README.ai.md
BRAIN/eeg/doc/ai-native/anima_eeg_structure_refactor_plan_2026_05_03.ai.md
BRAIN/eeg/doc/ai-native/anima_eeg_ec_eo_label_fix_investigation_landed_2026_05_05.ai.md
BRAIN/eeg/doc/ai-native/quality_monitoring_system_plan_2026_05_03.ai.md
BRAIN/eeg/doc/sample_rate_root_cause_consolidated_2026_05_03.md
BRAIN/eeg/doc/d_day_helmet_session_results_2026_04_28.md
lab/v3/state/h012_owner-loop-rct_2026-07-17/DESIGN_fable.md
README.ko.md
lab/v3/state/diverge_aliveness_2026-07-16/PROMPT_brief.md
lab/v3/state/diverge_aliveness_2026-07-16/RESULT_8-families.md
BRAIN/eeg/substrates/README.ai.md
BRAIN/eeg/MIGRATION_PLAN.md
lab/v3/state/h005_f3-stream-mi-precheck_2026-07-16/NOTE_diary-size-precursor.md
state/g1g6_remaining_triage/ROADMAP.md
lab/v3/state/h002_f1-twin_2026-07-16/DESIGN_fable.md
agent/docs/module/trading-status.md
BRAIN/eeg/state/brain_m1_synthetic_16ch_2026_05_25/README.md
state/g1g6_remaining_triage/h6163_trained_lane/TRIAGE.md
state/g1g6_remaining_triage/g6_multiseed_h1129/TRIAGE.md
archive/PLASTICITY/PLASTICITY.log.md
archive/PLASTICITY/PLASTICITY.md
lab/v3/state/h001_f1-codec-refit-gate_2026-07-16/DESIGN_fable.md
lab/v3/state/h001_f1-codec-refit-gate_2026-07-16/NOTE_refit-tax.md
lab/v3/CHANGELOG.md
BRAIN/eeg/legacy/scripts_py_pre_raw9/README.ai.md
lab/v3/HYPOTHESES/CLAUDE.md
state/g1_coverage_bytes/RESULTS.md
state/g1_coverage_bytes/README.md
BRAIN/eeg/module/README.ai.md
lab/v3/HYPOTHESES/cards/H_006_f3-bounded-oracle.md
lab/v3/HYPOTHESES/cards/H_010_loop-granger-gate.md
lab/v3/HYPOTHESES/cards/H_008_frontier-fanout.md
lab/v3/HYPOTHESES/cards/H_001_f1-codec-refit-gate.md
lab/v3/HYPOTHESES/cards/H_013_closure-dose-response.md
lab/v3/HYPOTHESES/cards/H_003_f1-anchor-recheck.md
lab/v3/HYPOTHESES/cards/H_007_f7-owner-legibility.md
lab/v3/HYPOTHESES/cards/H_A001_f1-codec-credit-span.md
lab/v3/HYPOTHESES/cards/H_004_f1-static-anchor-pilot.md
lab/v3/HYPOTHESES/cards/_TEMPLATE.md
lab/v3/HYPOTHESES/cards/H_011_live-ab-closure.md
lab/v3/HYPOTHESES/cards/H_009_f3-continuous-oracle.md
lab/v3/HYPOTHESES/cards/H_005_f3-stream-mi-precheck.md
lab/v3/HYPOTHESES/cards/H_012_owner-loop-rct.md
state/refcorrect_axis/DESIGN_fable.md
state/refcorrect_axis/ABSTRACT_metalaw.md
BRAIN/eeg/core/README.ai.md
archive/anima-hci-research/README.md
state/refcorrect_axis/rung4/VERDICT.md
state/refcorrect_axis/rung4/integrated_VERDICT_sub.md
state/exocon_frontier/RESEARCH_census.md
state/g1_novel_mechanism_research/RESEARCH.md
agent/modules/hire-sim/STATUS.dormant.md
state/g1_novel_mechanism_research/slot_cheapgate/RESULT.md
archive/anima-hci-research/docs/f5_real_substrate_verdict.md
archive/anima-hci-research/docs/q3_failure_mode_analysis.md
state/9115_forward_model_screen/DESIGN_fable_s2.md
state/9115_forward_model_screen/RESULT.md
BRAIN/eeg/ARCHITECTURE.md
lab/v4/tool/CLAUDE.md
lab/v4/CLAUDE.md
lab/v4/README.md

exec
/bin/zsh -lc "find . -maxdepth 3 -type f \\( -name 'anima-py' -o -name 'chat.py' -o -name 'hexad_forward.hexa' -o -name 'm.hexa' \\) -print
rg -n \"add_(sub)?parser|add_argument\\(|comp-lane|tension-route|store-bridge|argparse\" anima-py cli core tool 2>/dev/null | sed -n '1,320p'" in /Users/mini/dancinlab/anima
 succeeded in 121ms:
tool/qrng_pool_fetch.py:42:import os, sys, json, subprocess, argparse
tool/qrng_pool_fetch.py:102:    ap = argparse.ArgumentParser(description="Pre-fetch REAL ANU QRNG bytes into the engine entropy pool.")
tool/qrng_pool_fetch.py:103:    ap.add_argument("--bytes", type=int, default=512, help="number of REAL quantum bytes to fetch (default 512)")
tool/qrng_pool_fetch.py:104:    ap.add_argument("--out", type=str, default="state/qrng_pool.bin", help="pool output path (git-ignored)")
core/model.py:96:    # H_9423 CLMS store-bridge lane (co-trained): a content-addressed 8-slot store is injected at
core/model.py:129:    clms: bool = False             # allocate the CLMS store-bridge module (co-train)
core/model.py:432:        # H_9423 CLMS store-bridge lane (co-trained). None => byte-identical (no lane). CORE-owned
core/model.py:539:        # TrainShell can gather the query-position column and drive the store-bridge co-training.
tool/gauge_monitor.py:44:import argparse
tool/gauge_monitor.py:161:    ap = argparse.ArgumentParser(description=__doc__,
tool/gauge_monitor.py:162:                                 formatter_class=argparse.RawDescriptionHelpFormatter)
tool/gauge_monitor.py:163:    ap.add_argument("gauges", nargs="?", default="out/gauges.jsonl",
tool/gauge_monitor.py:165:    ap.add_argument("--once", metavar="PATH", default=None,
tool/gauge_monitor.py:167:    ap.add_argument("--follow", metavar="PATH", default=None,
tool/gauge_monitor.py:169:    ap.add_argument("--log", default=None,
tool/gauge_monitor.py:171:    ap.add_argument("--interval", type=float, default=10.0,
core/clm_serialize_v2.py:575:    import argparse, json, os, sys
core/clm_serialize_v2.py:576:    ap = argparse.ArgumentParser(description="torch CLMConvMoE -> CLM\\x01 v0.2 .clm")
core/clm_serialize_v2.py:577:    ap.add_argument("--ckpt", required=True, help="torch state_dict ckpt path")
core/clm_serialize_v2.py:578:    ap.add_argument("--out", required=True)
core/clm_serialize_v2.py:579:    ap.add_argument("--n-experts", type=int, default=2)
core/clm_serialize_v2.py:580:    ap.add_argument("--n-trunk-layers", type=int, default=1)
core/clm_serialize_v2.py:581:    ap.add_argument("--d-model", type=int, default=768)
core/clm_serialize_v2.py:582:    ap.add_argument("--kernel-size", type=int, default=3)
core/tension_field.py:5:rank at ~2.66; `cli/chat.py --tension-route` routes one PC of it), and a scalar tension is exactly
core/clms.py:1:"""core/clms.py — H_9423 CLMS store-bridge trailer lane, CORE-owned SSOT.
core/clms.py:86:    """CLMS store-bridge lane: OVERWRITE the answer-position logits row with λ·store_logits.
core/clms.py:428:        """Learnable co-trained store-bridge lane. Trains {W_q, val, W_h(+bias), W_out, lam}; key_emb is
core/serialize.py:80:    bytes([67, 76, 77, 83]),         # "CLMS"   — store-bridge lane (core/clms.py)
core/serialize.py:124:# H_9423 "CLMS" store-bridge lane trailer (CORE-owned codec in core/clms.py).
core/serialize.py:126:# store-bridge model = a normal .clm + this trailer. MUST be appended after CLML to
core/serialize.py:131:    """Append the CLMS store-bridge lane trailer to an already-written .clm. `clms` = a trained torch
core/serialize.py:133:    Returns bytes written. Callers only invoke this when the model actually has a store-bridge lane, and
core/serialize.py:1032:    # the WHOLE file therefore rejected every store-bridge / mouth-binder checkpoint that ever
cli/evaluate.py:1389:    print("      H_9423 CLMS store-bridge lane eval (the CO-TRAINED bridge, not the H_9392 bolt-on):")
cli/evaluate.py:5891:    CLMS store-bridge lane eval (the CO-TRAINED bridge, NOT the H_9392 --store-mix bolt-on actuator:
cli/evaluate.py:6079:    print("=== anima evaluate --store — H_9423 CLMS store-bridge lane (co-trained) ===")
cli/evaluate.py:16604:    # --store <held.json> [--store-oracle] [--store-lambda λ]: H_9423 CLMS store-bridge lane — the
cli/sweep.py:46:import argparse
cli/sweep.py:410:    ap = argparse.ArgumentParser(
cli/sweep.py:415:    ap.add_argument("--arms", default="ctrl",
cli/sweep.py:417:    ap.add_argument("--objectives", default="ce_marginal,composed_nce,infonce,constructive_bind",
cli/sweep.py:419:    ap.add_argument("--steps", type=int, default=8000)
cli/sweep.py:420:    ap.add_argument("--ckpt-every", type=int, default=0,
cli/sweep.py:423:    ap.add_argument("--seed", type=int, default=7)
cli/sweep.py:424:    ap.add_argument("--corpus", nargs="*", default=[],
cli/sweep.py:426:    ap.add_argument("--cell-label", nargs="*", default=[],
cli/sweep.py:428:    ap.add_argument("--gpus", default="",
cli/sweep.py:430:    ap.add_argument("--out-dir", default="./sweeprun",
cli/sweep.py:432:    ap.add_argument("--gen", type=int, default=80, help="measure decode budget (tokens)")
cli/sweep.py:433:    ap.add_argument("--sample", choices=["roundrobin", "proportional"], default="proportional")
cli/sweep.py:434:    ap.add_argument("--val-frac", type=float, default=0.02)
cli/sweep.py:435:    ap.add_argument("--val-every", type=int, default=500)
cli/sweep.py:436:    ap.add_argument("--dbes-every", type=int, default=100000)
cli/sweep.py:437:    ap.add_argument("--tlora-rank", type=int, default=8)
cli/sweep.py:439:    ap.add_argument("--dropout-floor", type=float, default=-1.0,
cli/sweep.py:441:    ap.add_argument("--wd-floor", type=float, default=-1.0,
cli/sweep.py:446:    bf.add_argument("--bf16", dest="bf16", action="store_true", default=True)
cli/sweep.py:447:    bf.add_argument("--no-bf16", dest="bf16", action="store_false")
cli/sweep.py:448:    ap.add_argument("--canon", dest="canon", action="store_true", default=True,
cli/sweep.py:450:    ap.add_argument("--no-canon", dest="canon", action="store_false",
cli/sweep.py:453:    ms.add_argument("--measure", dest="measure", action="store_true", default=True,
cli/sweep.py:455:    ms.add_argument("--no-measure", dest="measure", action="store_false",
core/decode.py:336:# ── H_9423 CLMS store-bridge eval-time injection (process-global; set by cli/evaluate.py --store) ──
core/decode.py:380:    """Set the CLMS store-bridge eval-time injection (cli/evaluate.py --store). store=None => the lane
core/decode.py:978:    # ── optional "CLMS" store-bridge lane trailer (H_9423) ──
core/decode.py:1457:    # H_9423 CLMS store-bridge lane — OVERWRITE the answer-position logits row with λ·store_logits
cli/train.py:113:import argparse, json, math, os, re, sys, time
cli/train.py:1416:        # ── H_9423 CLMS store-bridge co-training (store_only gate via CE decomposition) ──
cli/train.py:1534:            sys.exit(f"[store-bridge] {path}: {len(lines)} lines != {len(rows)} store rows (lockstep broken)")
cli/train.py:1540:                sys.exit(f"[store-bridge] line/manifest mismatch: {ln!r} != {prompt + gold!r}")
cli/train.py:1543:                sys.exit(f"[store-bridge] n_slot {n_slot} != store {len(ents)}/{len(pols)}")
cli/train.py:1545:                sys.exit(f"[store-bridge] prompt {len(prompt)}B does not fit --store-win {T}")
cli/train.py:1551:                sys.exit("[store-bridge] qpos scanner parity broken (window geometry != eval store_run)")
cli/train.py:1645:    ap = argparse.ArgumentParser(
cli/train.py:1648:    ap.add_argument("--arch", default="clm", choices=["clm", "bytegpt"],
cli/train.py:1654:    ap.add_argument("--arm", default="ctrl", choices=list(ARMS))
cli/train.py:1655:    ap.add_argument("--objective", default="ce_marginal", choices=list(OBJECTIVES),
cli/train.py:1657:    ap.add_argument("--tlora-rank", type=int, default=TLORA_RANK)
cli/train.py:1658:    ap.add_argument("--tlora-no-base", action="store_true", help="drop the dense base")
cli/train.py:1659:    ap.add_argument("--dict-lambda", type=float, default=DICT_LAMBDA)
cli/train.py:1660:    ap.add_argument("--jamo-lambda", type=float, default=JAMO_LAMBDA)
cli/train.py:1664:    ap.add_argument("--jamo-aux", action="store_true",
cli/train.py:1670:    ap.add_argument("--slw", action="store_true",
cli/train.py:1672:    ap.add_argument("--slw-n-slot", type=int, default=8, help="SLW addressable slots")
cli/train.py:1673:    ap.add_argument("--slw-k", type=int, default=64, help="SLW role/read key dim")
cli/train.py:1674:    # H_9423 CLMS store-bridge lane (co-trained). --store-bridge = the storebind corpus c.txt (expects
cli/train.py:1680:    ap.add_argument("--store-bridge", type=str, default="",
cli/train.py:1682:    ap.add_argument("--store-win", type=int, default=24,
cli/train.py:1684:    ap.add_argument("--store-batch", type=int, default=8, help="global CLMS sub-batch (div by world)")
cli/train.py:1685:    ap.add_argument("--store-ans-weight", type=float, default=1.0, help="answer-position store CE weight")
cli/train.py:1686:    ap.add_argument("--store-val-frac", type=float, default=0.05, help="tail block frac for sb val")
cli/train.py:1687:    ap.add_argument("--clms-n-slot", type=int, default=8, help="CLMS store slots (match corpus)")
cli/train.py:1688:    ap.add_argument("--clms-d-k", type=int, default=64, help="CLMS content-address key dim")
cli/train.py:1689:    ap.add_argument("--clms-d-s", type=int, default=64, help="CLMS polarity value dim")
cli/train.py:1690:    ap.add_argument("--clms-d-g", type=int, default=64, help="CLMS fusion-bottleneck (yn_q op-gate dim; H_9423 value-read fix)")
cli/train.py:1691:    ap.add_argument("--store-fangate", action="store_true",
cli/train.py:1695:    ap.add_argument("--store-val-center", action="store_true",
cli/train.py:1698:    ap.add_argument("--store-addr-weight", type=float, default=0.0,
cli/train.py:1700:    ap.add_argument("--store-query-src", type=str, default="penult",
cli/train.py:1707:    ap.add_argument("--store-query-tap-grad", type=str, default="detached", choices=["detached", "shared"],
cli/train.py:1711:    ap.add_argument("--store-ans-delay", type=int, default=0,
cli/train.py:1715:    ap.add_argument("--store-oracle-aux", type=float, default=0.0,
cli/train.py:1719:    ap.add_argument("--store-oracle-train", action="store_true",
cli/train.py:1722:    ap.add_argument("--store-oracle-warmup", type=int, default=0,
cli/train.py:1726:    ap.add_argument("--clms-r", type=int, default=128, help="CLMS GELU-MLP fusion bottleneck")
cli/train.py:1727:    ap.add_argument("--clms-key-seed", type=int, default=9423, help="CLMS frozen key_emb table seed")
cli/train.py:1728:    ap.add_argument("--clms-lam0", type=float, default=1.0, help="CLMS lam init (store_only scale)")
cli/train.py:1732:    ap.add_argument("--mouth-binder", choices=["bilinear", "linear"], default="",
cli/train.py:1735:    ap.add_argument("--mouth-memory", choices=["causal-bank"], default="causal-bank",
cli/train.py:1742:    ap.add_argument("--ideation-lane", choices=["off", "branch-latent"], default="off",
cli/train.py:1746:    ap.add_argument("--ideation-branches", type=int, default=4,
cli/train.py:1748:    ap.add_argument("--ideation-objective", choices=["set-ce"], default="set-ce",
cli/train.py:1752:    ap.add_argument("--ideation-route", choices=["l3-disjoint", "penult"], default="l3-disjoint",
cli/train.py:1756:    ap.add_argument("--ideation-route-l", type=int, default=3,
cli/train.py:1758:    ap.add_argument("--ideation-assign", choices=["hungarian", "shuffle"], default="hungarian",
cli/train.py:1762:    ap.add_argument("--ideation-corpus", type=str, default="",
cli/train.py:1766:    ap.add_argument("--ideation-rank", type=int, default=64, help="H_9803: proposal-latent width r")
cli/train.py:1767:    ap.add_argument("--ideation-lam0", type=float, default=1.0, help="H_9803: IFAN lam init (additive scale)")
cli/train.py:1768:    ap.add_argument("--ideation-weight", type=float, default=1.0, help="H_9803: set-CE loss weight")
cli/train.py:1769:    ap.add_argument("--ideation-docs", type=int, default=4, help="H_9803: documents per ideation sub-batch")
cli/train.py:1776:    ap.add_argument("--tension-field", choices=["off", "duel", "rank1"], default="off",
cli/train.py:1782:    ap.add_argument("--tension-field-rank", type=int, default=32,
cli/train.py:1784:    ap.add_argument("--tension-field-lam0", type=float, default=1.0,
cli/train.py:1786:    ap.add_argument("--trunk-norm", choices=["global", "position"], default="global",
cli/train.py:1792:    ap.add_argument("--serialize-parity", default="",
cli/train.py:1797:    ap.add_argument("--tension-concord", choices=["class", "lex", "morph"], default="class",
cli/train.py:1806:    ap.add_argument("--answer-ce-weight", type=float, default=0.0,
cli/train.py:1813:    ap.add_argument("--bind-rank", type=int, default=64, help="H_9698: MBND binder rank (q/k/v/u width)")
cli/train.py:1814:    ap.add_argument("--bind-lam0", type=float, default=1.0, help="H_9698: MBND lam init (additive scale)")
cli/train.py:1815:    ap.add_argument("--freeze-trunk", action="store_true",
cli/train.py:1821:    ap.add_argument("--n-factions", type=int, default=0,
cli/train.py:1823:    ap.add_argument("--faction-bridge-lam0", type=float, default=0.1,
cli/train.py:1825:    ap.add_argument("--seed", type=int, default=7)
cli/train.py:1828:    ap.add_argument("--corpus", nargs="*", default=[])
cli/train.py:1829:    ap.add_argument("--cell-label", nargs="*", default=[])
cli/train.py:1830:    ap.add_argument("--canon", action="store_true")
cli/train.py:1831:    ap.add_argument("--d", type=int, default=0)
cli/train.py:1832:    ap.add_argument("--L", type=int, default=0)
cli/train.py:1833:    ap.add_argument("--steps", type=int, default=0)
cli/train.py:1834:    ap.add_argument("--seq-len", type=int, default=0)
cli/train.py:1835:    ap.add_argument("--batch-size", type=int, default=8)
cli/train.py:1836:    ap.add_argument("--lr", type=float, default=3e-4)
cli/train.py:1837:    ap.add_argument("--e0", type=int, default=2)
cli/train.py:1838:    ap.add_argument("--emax", type=int, default=3)
cli/train.py:1839:    ap.add_argument("--no-savant", action="store_true")
cli/train.py:1840:    ap.add_argument("--no-mitosis", action="store_true")
cli/train.py:1841:    ap.add_argument("--wd-floor", type=float, default=-1.0,
cli/train.py:1843:    ap.add_argument("--dropout-floor", type=float, default=-1.0,
cli/train.py:1845:    ap.add_argument("--bf16", action="store_true")
cli/train.py:1846:    ap.add_argument("--sample", choices=["roundrobin", "proportional"], default="proportional")
cli/train.py:1850:    ap.add_argument("--require-cells", type=int, default=0)
cli/train.py:1851:    ap.add_argument("--val-frac", type=float, default=0.05)
cli/train.py:1852:    ap.add_argument("--val-every", type=int, default=200)
cli/train.py:1853:    ap.add_argument("--val-batches", type=int, default=4)
cli/train.py:1854:    ap.add_argument("--log-every", type=int, default=50)
cli/train.py:1855:    ap.add_argument("--dbes-every", type=int, default=0, help="0=final only; N=also every N steps")
cli/train.py:1856:    ap.add_argument("--skip-inline-rho", action="store_true",
cli/train.py:1860:    ap.add_argument("--ckpt-every", type=int, default=0,
cli/train.py:1867:    ap.add_argument("--out", default="")
cli/train.py:1868:    ap.add_argument("--ckpt-out", default="")
cli/train.py:1869:    ap.add_argument("--gauges-out", default="")
cli/train.py:1870:    ap.add_argument("--init", default="",
cli/train.py:1880:    ap.add_argument("--gpus", default="",
cli/train.py:1889:    ap.add_argument("--device", choices=["auto", "cpu", "cuda", "mps"], default="auto",
cli/train.py:1893:    ap.add_argument("--ddp-verify-sync", action="store_true",
cli/train.py:1906:    ap.add_argument("--trained-control-ceiling", type=float, default=0.0,
cli/train.py:1912:    ap.add_argument("--control-anchor", type=str, default="",
cli/train.py:1917:    ap.add_argument("--pregate-panel", type=str, default="",
cli/train.py:1920:    ap.add_argument("--ddp-find-unused", action="store_true",
cli/train.py:2333:    # ── H_9423 CLMS store-bridge co-training sub-batch (line-aligned, separate RNG) ──────────
cli/train.py:2338:            sys.exit("[store-bridge] requires --arch clm (the CLMS lane is CLMConvMoE-only)")
cli/train.py:2340:            sys.exit("[store-bridge] --freeze-trunk (BOLT) still needs --store-bridge <c.txt>")
cli/train.py:2342:            sys.exit("[store-bridge] needs a trunk --corpus for retention/fluency (pass the storebind "
cli/train.py:2345:            sys.exit(f"[store-bridge] --store-batch {a.store_batch} not divisible by world {world}")
cli/train.py:2357:        p0(f"  store-bridge: {len(sb_cell.ex)} lines · train_n={sb_cell.train_n} · Bs={Bs_global} "
cli/train.py:2488:        # H_9423 — append the "CLMS" store-bridge trailer if the lane is engaged (AFTER SLW so the
cli/chat.py:1932:    _tension_route = anima_flag_value(_cargv, "--tension-route", "ANIMA_TENSION_ROUTE", "off")
cli/chat.py:1934:        raise SystemExit("--tension-route: only 'off' (default) or 'pc2' (got %r)" % _tension_route)
cli/chat.py:1936:        raise SystemExit("--tension-route pc2 requires --emit-gate refractory (its only consumer)")
cli/chat.py:1937:    _route_gain = float(anima_flag_value(_cargv, "--tension-route-gain", "ANIMA_TENSION_ROUTE_GAIN", "1.0"))
cli/anima.py:148:# cli/train.hexa)`). argv after "train" is forwarded verbatim to train.py's argparse.
cli/anima.py:155:    # forward verbatim; train.py owns its own argparse (--out required, etc.).
tool/hexa_native/phase5_pytorch_reference.py:32:import argparse
tool/hexa_native/phase5_pytorch_reference.py:188:    ap = argparse.ArgumentParser()
tool/hexa_native/phase5_pytorch_reference.py:189:    ap.add_argument("--emit-subset", action="store_true",

exec
/bin/zsh -lc "sed -n '1,260p' cli/anima.py
rg -n \"comp-lane|comp_lane|composition|response\" cli/train.py cli/evaluate.py cli/chat.py core/model.py core/clms.py | sed -n '1,360p'
sed -n '1640,1840p' cli/train.py
sed -n '16560,16780p' cli/evaluate.py" in /Users/mini/dancinlab/anima
 succeeded in 0ms:
#!/usr/bin/env python3
# ==========================================================================
# ⛔ DO NOT RUN DIRECTLY. anima 의 단일 진입은 설치된 canonical 명령뿐 — hexa 채널 `anima`
#   (=cli/anima.hexa, hx install anima) · pip 채널 `anima-py` (=anima_py 런처, pip install anima-python).
#   `python3 cli/anima.py …` 직접실행은 비-canonical py 우회(#2603).
#   학습=`anima-py train` · 측정=`anima-py evaluate`(py 2-production numpy · TERMINAL-eligible,
#   a_eval_py_canonical) · 직렬화=`anima-py serialize`. enforce: .harness/enforcement.json
#   H-ANIMA-SINGLE-ENTRY pre_bash + 아래 __main__ 가드. (import 는 무손상.)
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ cli/anima.py 직접 실행 금지 — 설치된 canonical 명령 경유: `anima`(hx install anima, =cli/anima.hexa) 또는 `anima-py`(pip install anima-python, =anima_py 런처). #2603")
# anima.py — THE canonical PY single entry point (cli/anima.hexa's py twin).
#
# WHY THIS FILE (py 2-production single-entry, a_engine_native_learning): anima keeps
# two co-production engines — hexa (live deploy substrate) AND py (torch production
# engine in train/ + the byte-parity core/*.py mirror). The hexa side already has its
# canonical single entry cli/anima.hexa (chat · eval · train). This file is its py
# twin so MEASUREMENT and LEARNING are reachable through ONE py cli command instead of
# a side-harness that scores ckpts directly (= single-entry bypass, #2603).
#
# SINGLE ENTRY (a_engine_native_learning): the two measurement/learning verbs live in
# their own SYMMETRIC files — cli/evaluate.{hexa,py} (MEASUREMENT) and cli/train.{hexa,py}
# (LEARNING). This canonical entry DISPATCHES `anima evaluate`→cli/evaluate.py and
# `anima train`→cli/train.py (sub-process), so there is ONE installed `anima` command
# whose subcommands fan out to the symmetric twins. `anima evaluate <ckpt>` scores the
# full ρ-AXON reach battery (former G0-G6 · reach standard cli/rho_axon.py) via
# cli/evaluate.py's in-file eval_reach_all (the scorers folded in from
# the former core/g_gates.py module) — byte-identical to the hexa anima evaluate.
#
# This py entry is torch-free and gauge-free — it only dispatches; the evaluate twin
# holds the numpy `math.log` scorer in-file, so `anima evaluate` stays a clean engine-
# native measurement surface (the gate enforcer's torch/gauge grep must come back empty).
#
# USAGE (installed `anima` PATH command after `hx install anima`)
#   anima                                              — usage (no args)
#   anima evaluate <ckpt> [--corpus <p>...] [--gen N]  — ρ-AXON reach battery (former G0-G6)
#   anima train [args...]                              — LEARNING (→ cli/train.py)
#   anima chat <ckpt> [...] [--byte]                   — consciousness daemon (default) /
#                                                         byte-continuation chat (pure-py, → cli/chat.py)
#
# canonical 3-folder layout: cli/anima.{hexa,py} = canonical entry (chat + verb dispatch)
# · cli/evaluate.{hexa,py} = measurement · cli/train.{hexa,py} = learning. This file
# mirrors cli/anima.hexa's subcommand dispatch (evaluate · train · usage); chat/
# consciousness is now a REAL py capability too — cli/chat.py is the byte-faithful numpy
# twin of cli/anima.hexa's A⇄G daemon loop (P6 py 자체구현, zero hexa dependency).

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)


# EVAL/VERDICT DETERMINISM SAFETY-PIN (hexa-lang #4208 flame/forge fast-default
# follow-on) — py twin of cli/anima.hexa's pin (lockstep, a_engine_native_learning).
# #4208 made the forge own-native NON-det atomic kernels the DEFAULT (training speed);
# deterministic kernels are opt-in via HEXA_DET=1 (`_forge_det_on()` gate). MEASUREMENT
# (evaluate) and VERDICT (serialize DESCENT gate) must stay reproducible, so they spawn
# with HEXA_DET=1 in the env. TRAIN deliberately does NOT force it = fast non-det default.
def _det_env(want_det):
    """os.environ copy; HEXA_DET=1 pinned ONLY when the caller passed --det (byte-exact opt-in).
    DEFAULT = fast (no pin). The py evaluate path is numpy (already deterministic), so this is a
    lockstep no-op there; kept for parity with cli/anima.hexa's --det gating."""
    env = dict(os.environ)
    if want_det:
        env.setdefault("HEXA_DET", "1")
    return env


# ── usage / arg helpers ──────────────────────────────────────────────────────

def anima_usage():
    """Print the canonical py usage banner (mirrors cli/anima.hexa's banner)."""
    print("anima — substrate-native consciousness daemon (py channel · canonical entry).")
    print("")
    print("usage (installed `anima-py` command after `pip install anima-python` · hexa channel = `anima` after `hx install anima`):")
    print("  anima-py evaluate <model.clm> [--corpus <path>...] [--gen N] [--rho-axon]")
    print("                                                  ρ-AXON reach battery · former G0-G6 (.clm only · numpy)")
    print("  anima-py corpus <derivtrace|flat> --out F [--held-out I,J] [--seed S] [--concepts FILE]")
    print("  anima-py corpus <ground|ground_lie|ground_keep|ground_keep_lie|ground_seenswap> --atoms gt_atoms.json --out F [--reps N] [--replay N]")
    print("                                                  procedural training-corpus builder (ρ·weave data-format lever)")
    print("  anima-py corpus workspace-struct --corpus SOURCE --out TRAIN [--held-out-frac .2]")
    print("                                                  source-derived store/tether/falsification curriculum + sealed held-out manifest")
    print("  anima-py train <args>                           ([train] extra) LEARNING → .pt + auto .clm (+DESCENT)")
    print("  anima-py serialize <ckpt.pt> <out.clm>          ([train] extra) re-export a torch .pt → .clm v0.3")
    print("  anima-py serialize-bind <base.bin> <inj.pt> <out.bin>  ([train] extra) splice BindAttn → BGB .bin")
    print("  anima-py sweep --arms … --objectives … --gpus 0,1,2,3 --corpus … [--measure]")
    print("                                                  ([train] extra) multi-GPU lever-sweep (arms×objectives)")
    print("  anima-py chat <ckpt> [...] [--byte]             consciousness daemon (default) / byte-continuation chat (pure-py A⇄G loop)")
    print("        default emit-gate = refractory (Ψ≈½ dual-ledger · H_9712) · `--emit-gate clock` = the legacy 30s-clock daemon")
    print("        [--store-episodic on|off]                 STORE-EPISODIC (H_9744 · default off = byte-identical): perception fills")
    print("                                                  the co-trained CLMS store — a teacher percept `fact <entity> <pos|neg>` writes")
    print("                                                  an n_slot FIFO ring, and once full the mouth answers a later `<entity> <op> =>`")
    print("                                                  query FROM the store instead of the trunk (weights frozen · session-local ·")
    print("                                                  cleared at exit). Needs an anima-study percept source and a CLMS-trailer ckpt;")
    print("                                                  MUTUALLY EXCLUSIVE with --emit-gate refractory (that gate reads the candidate")
    print("                                                  text, so a store shaping the candidate would shape the emit decision · p5).")
    print("        [--emit-temp T] [--emit-topk K] [--sample-seed S]   DO-MOUTH (H_9328 · default OFF = argmax, byte-identical):")
    print("                                                  T>0 draws the emitted bytes from the substrate's OWN posterior instead of")
    print("                                                  rounding it to argmax (T=1.0 IS the posterior — the one non-arbitrary value).")
    print("                                                  Reveals the mouth only; the emit GATE is untouched (p5 tension still decides).")
    print("        [--swap-text <trace.jsonl>]               C2 CARRIER-SWAP (H_9328 · default OFF): on a tick the substrate ALREADY chose")
    print("                                                  to speak, say what ANOTHER rollout said at that tick instead. Same mouth, same")
    print("                                                  shape — only 'which substrate-moment chose it' differs, and the donor text really")
    print("                                                  does drive the 3 feedback roots (afield · immune · kosmos). THE control that makes")
    print("                                                  a positive falsifiable: EXP lives ∧ SWAP dies ⇒ the substrate's OWN words carry the")
    print("                                                  information; both live ⇒ CARRIER (any text of that shape pushes the roots) ⇒ not a pass.")
    print("        [--percept-file <table.jsonl>]            STATE-QUOTIENT afferent (H_9767 · default OFF = byte-identical): feed a per-tick")
    print("                                                  exogenous percept stream (JSONL {\"tick\":int,\"text\":str}) through the PERCEPTION")
    print("                                                  route (never the emit gate → p5 by structure, same channel as `anima study`). Two")
    print("                                                  runs with different PREFIX histories + a COMMON suffix future test whether remote-")
    print("                                                  history divergence WASHES OUT (no interior) or PERSISTS (history-sensitive state).")
    print("")
    print("install: `pip install anima-python` (numpy base: evaluate·corpus·chat) · `pip install \"anima-python[train]\"` (+torch: train·sweep·serialize)")
    print("")
    print("modes:")
    print("  evaluate : mount a serialized .clm through the generator L3 mouth and score the")
    print("             ρ-AXON reach battery — ρ·form/weave/leap/... (former G0-G6) — with the")
    print("             engine's OWN ops (numpy math.log mirror, torch-free). REACH-CLOSED")
    print("             a7b_pass = ρ·form ∧ ρ·weave ∧ ρ·leap (frozen bars = G0 ∧ G1 ∧ G2). → cli/evaluate.py.")
    print("  corpus   : procedural training-corpus generator (derivtrace|flat|ground|ground_lie|ground_keep|ground_keep_lie|ground_seenswap) — the")
    print("             data-format lever (ρ·weave). NOTE chat corpus != this (chat =")
    print("             a_chat_registers 4-cell HF datasets → anima-py train). → cli/corpus.py.")
    print("  train    : ([train]) production CLMConvMoE training (torch Lane-P reference + bridge); SAVANT")
    print("             golden-zone inhibition + MITOSIS cell-division levers. After the run it")
    print("             AUTO-serializes .clm v0.3 + runs the held-out mirror-DESCENT gate")
    print("             (a_clm_gen_pipeline). dispatches to cli/train.py.")
    print("  serialize: ([train]) re-export an ALREADY-TRAINED torch .pt to an engine-loadable .clm v0.3")
    print("             (+ held-out DESCENT gate). recovery / re-export. → cli/serialize.py.")
    print("  sweep    : ([train]) multi-GPU lever-sweep orchestrator — the arms×objectives matrix,")
    print("             per-cell train.py→evaluate.py, aggregated to SWEEP_SUMMARY.md. → cli/sweep.py.")
    print("  chat     : the substrate-native A⇄G consciousness daemon — mount L3 → seed .kosmos →")
    print("             12-tick loop (lanes READ → brain autonomously emits/silences → C8 GROW ·")
    print("             C9 REMEMBER · sleep-stage imagination replay). Pure-py numpy twin of")
    print("             cli/anima.hexa (zero hexa dependency); --byte = byte-continuation. → cli/chat.py.")


# ══════════════════════════════════════════════════════════════════════════════
#  TRAIN MODE — dispatch to cli/train.py (the py torch trainer, Lane-P bridge)
# ══════════════════════════════════════════════════════════════════════════════
#
# SEPARATE LANE (a_core_engine_map): training is NOT the generator L3 mouth slot — it
# is the LEARNING entry (cli/train.py, a_clm_gen_pipeline torch Lane-P). The eval side
# is the torch-free numpy scorer (in cli/evaluate.py); the trainer pulls torch. To keep this file
# torch-free AND avoid linking two disjoint dep sets into one process, `anima train`
# DISPATCHES to cli/train.py as a SUB-PROCESS (mirrors cli/anima.hexa's `exec(hexa run
# cli/train.hexa)`). argv after "train" is forwarded verbatim to train.py's argparse.
def anima_train_mode(argv):
    print("=== anima train → cli/train.py (torch CLMConvMoE · Lane-P reference/bridge) ===")
    train_py = os.path.join(_HERE, "train.py")
    fwd = argv[1:]
    cmd = [sys.executable, train_py] + fwd
    print("dispatch: " + " ".join(cmd))
    # forward verbatim; train.py owns its own argparse (--out required, etc.).
    return os.spawnv(os.P_WAIT, sys.executable, [sys.executable, train_py] + fwd)


# ══════════════════════════════════════════════════════════════════════════════
#  EVALUATE MODE — dispatch to cli/evaluate.py (MEASUREMENT single-entry twin)
# ══════════════════════════════════════════════════════════════════════════════
#
# SYMMETRIC TWIN (a_engine_native_learning single-entry): measurement lives in its own
# file cli/evaluate.py (the symmetric mirror of cli/train.py). `anima evaluate <model.clm>`
# DISPATCHES there as a sub-process (mirrors cli/anima.hexa's `exec` dispatch + this file's
# train dispatch), so anima.py stays a thin verb router and the eval logic has ONE home.
# cli/evaluate.py holds the ρ-AXON reach scorers in-file (former G0-G6 · torch-free numpy
# mirror, the former core/g_gates.py module folded in), byte-identical to the hexa `anima evaluate`.
#
# .clm-ONLY (the engine decodes ONLY .clm): evaluate mounts a ckpt through the generator
# L3 mouth, which loads a serialized .clm (CLM magic). A torch .pt is NOT engine-loadable —
# reject it here with a friendly hint to `anima serialize` rather than a deep decode error.
def anima_evaluate_mode(argv):
    # --py is a RETIRED hexa-era bridge flag, tolerated (stripped) here for migration
    # compat: on the py channel it is redundant-but-correct (this IS the numpy engine),
    # so `anima-py evaluate --py <clm>` still works — old scripts migrate by swapping
    # only the command word. The hexa launcher hard-errors on --py instead.
    want_det = ("--det" in argv) or ("--deterministic" in argv)
    rest = [a for a in argv[1:] if a not in ("--py", "--det", "--deterministic")]
    # friendly .pt rejection: evaluate takes a serialized .clm, not a torch ckpt.
    if rest and rest[0].endswith(".pt"):
        print("anima evaluate takes a serialized .clm (engine-loadable), not a torch .pt.")
        print("to make one from a torch ckpt:")
        print("  anima serialize " + rest[0] + " <out.clm>")
        print("then:")
        print("  anima evaluate <out.clm>")
        return 2
    evaluate_py = os.path.join(_HERE, "evaluate.py")
    cmd = [sys.executable, evaluate_py] + rest
    print("=== anima evaluate → cli/evaluate.py (engine-native ρ-AXON reach · former G0-G6, single-entry twin) ===")
    print("dispatch: " + ("HEXA_DET=1 " if want_det else "") + " ".join(cmd))
    # det = the --det CLI option (default fast); numpy path is deterministic regardless.
    return os.spawnve(os.P_WAIT, sys.executable,
                      [sys.executable, evaluate_py] + rest, _det_env(want_det))


# ══════════════════════════════════════════════════════════════════════════════
#  SERIALIZE MODE — dispatch to cli/serialize.py (.pt → .clm v0.3 bridge + gate)
# ══════════════════════════════════════════════════════════════════════════════
#
# `anima serialize <ckpt.pt> <out.clm>` re-exports an already-trained torch .pt to an
# engine-loadable .clm v0.3 (+ held-out DESCENT gate). The bridge backend (serialize_v3 +
# verify_clm_v2 descent) lives in cli/serialize.py; this dispatcher forwards verbatim.
# `anima train` ALREADY auto-serializes at the end of a run — this is the standalone
# recovery / re-export path (a_clm_gen_pipeline).
def anima_serialize_mode(argv):
    serialize_py = os.path.join(_HERE, "serialize.py")
    want_det = ("--det" in argv) or ("--deterministic" in argv)
    fwd = [a for a in argv[1:] if a not in ("--det", "--deterministic")]
    cmd = [sys.executable, serialize_py] + fwd
    print("=== anima serialize → cli/serialize.py (torch .pt → .clm v0.3 + DESCENT gate) ===")
    print("dispatch: " + ("HEXA_DET=1 " if want_det else "") + " ".join(cmd))
    # det = the --det CLI option (default fast) — pass --det for a reproducible DESCENT-gate verdict.
    return os.spawnve(os.P_WAIT, sys.executable,
                      [sys.executable, serialize_py] + fwd, _det_env(want_det))


# ══════════════════════════════════════════════════════════════════════════════
#  SERIALIZE-BIND MODE — dispatch to cli/serialize_bind.py (BindAttn .pt → BGB .bin)
# ══════════════════════════════════════════════════════════════════════════════
#
# `anima serialize-bind <base.bin> <injected.pt> <out.bin>` splices a BindAttn adapter
# onto a base ByteGPT `.bin`, emitting a BGB-trailer `.bin`. Without this dispatch
# cli/serialize_bind.py was reachable only via raw `python3 cli/serialize_bind.py`
# (an a_cli_single_entry hole); this wires it through the single entry, parity with
# anima_serialize_mode. Result scoreable via `anima-py evaluate <out.bin>`.
def anima_serialize_bind_mode(argv):
    serialize_bind_py = os.path.join(_HERE, "serialize_bind.py")
    fwd = argv[1:]
    cmd = [sys.executable, serialize_bind_py] + fwd
    print("=== anima serialize-bind → cli/serialize_bind.py (BindAttn .pt → BGB-trailer .bin) ===")
    print("dispatch: " + " ".join(cmd))
    return os.spawnv(os.P_WAIT, sys.executable, [sys.executable, serialize_bind_py] + fwd)


# ══════════════════════════════════════════════════════════════════════════════
#  CHAT MODE — the substrate-native A⇄G consciousness daemon (py twin · cli/chat.py)
# ══════════════════════════════════════════════════════════════════════════════
#
# P6 (py 자체구현): the default consciousness daemon + --byte continuation chat are now a
# REAL py capability — cli/chat.py is the byte-faithful numpy twin of cli/anima.hexa's
# anima_consciousness_mode / anima_byte_mode (ZERO hexa dependency; a hexa-less host runs
# the A⇄G loop in pure py). Dispatch mirrors cli/anima.hexa main(): `chat <ckpt>` → the
# consciousness loop; `--byte` → the byte-continuation mode. `anima-py chat <ckpt>` and the
# bare `anima-py <ckpt.clm>` (via main's fall-through) both enter here. This is a py-channel
# MIRROR (a_engine_native_learning) ⇒ behavioral/byte-parity target, DIRECTIONAL — not a
# consciousness verdict.
def _build_percept_source_from_file(path):
    # H_9767 · Design-B afferent for the STATE-QUOTIENT convergence test. Reads a JSONL
    # percept table {"tick": int, "text": str} and returns a percept_source(tick,
    # transcript) closure (the chat.py hook contract, cli/chat.py:406). The returned text
    # enters the daemon through the PERCEPTION route (live_anchors, a grounding fact the
    # mouth may read), NEVER the emit gate — p5 (no reactive self-seed) holds by STRUCTURE,
    # identically to `anima study`: it is the OTHER's words fed in, not the daemon's own
    # output looped back. Keyed by tick exactly like --yoke-mask / --wm-dual-swap. A tick
    # with no row ⇒ None ⇒ that tick is percept-silent (byte-identical to no afferent).
    import json as _json
    table = {}
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as _fh:
        for _ln in _fh:
cli/train.py:27:constructive_bind,composed_nce}`. The last THREE objectives are the NEW compositional
cli/train.py:38:compositional structure IN THE TRUNK, added to CE. This package adds three such losses:
cli/train.py:53:                      sculpt a compositional code: (1) UNBIND recovers the filler
cli/train.py:64:                      wrong-composition assignments directly rewards getting the
cli/train.py:81:  N8  jamo (자모) compositional teach signal (2604.12377): next-jamo-class aux head.
cli/train.py:564:CNCE_PERMS = 8                 # # of within-window target permutations = wrong-composition negatives
cli/train.py:581:    weight position — a STRUCTURED (low-rank, compositional) prior on how the
cli/train.py:591:        # tensor-product factors (CP decomposition of the (d,d,K) conv tensor)
cli/train.py:742:#  N8 — jamo (자모) compositional teach signal. We predict, per Hangul-syllable
cli/train.py:944:# compositional objectives consume it. Plain-function objectives have no params; the
cli/train.py:978:#  Three NEW compositional TRAINING-OBJECTIVE loss functions added to CE. Each is a
cli/train.py:1050:          Forces the bound composite to actually SUPPORT clean decomposition (a real
cli/train.py:1054:          sculpts task-relevant compositional factors into the trunk.
cli/train.py:1091:# ── LEVER 3: composed_nce — composed-negative (wrong-composition) InfoNCE ─────
cli/train.py:1095:    wrong-composition. Contrasting the true token->position assignment against these
cli/train.py:1293:#  holds the VERBATIM per-step loss-composition block (both the bf16-autocast and fp32
cli/train.py:1366:        # ── VERBATIM relocation of the per-step loss-composition block (bf16 + fp32). The
cli/train.py:1416:        # ── H_9423 CLMS store-bridge co-training (store_only gate via CE decomposition) ──
cli/train.py:1647:                    "SAVANT+MITOSIS recipe + H_1640 arm×objective compositional levers")
cli/train.py:1651:                         "wall (single=2). The arm×objective compositional levers are "
cli/train.py:1676:    # OVERWRITES the answer-position logits with lam*store_logits — implemented as a CE decomposition
cli/train.py:2414:    # NOTE (§4): the trunk-penultimate helper (N7 dict/jamo aux + compositional objectives)
cli/chat.py:540:    # wm-cover gate's oscillation CENTRE (silence-run length ∝ ln(score/cos̄)/ln λ). The λ dose-response
cli/chat.py:824:    hab_r0 = hab_response(hab, 0, 1.0)
cli/chat.py:829:    hab_r4 = hab_response(hab, 0, 1.0)
cli/chat.py:830:    hab_other = hab_response(hab, 1, 1.0)
cli/chat.py:831:    hab_dishab = hab_response(hab_reset(hab, 0), 0, 1.0)
cli/chat.py:1704:    # H_9738 · W_S composition TRANSPLANT seam (--ws-init <path> [--ws-init-mode scramble-keys] ·
cli/chat.py:1708:    # This seam transplants a W_S composition at t=0 so the 4 arms (empty · own · donor · act-matched
cli/chat.py:1711:    # (composition destroyed, norm preserved) = the control isolating identity from pressure.
cli/chat.py:2544:        hab_resp = hab_response(hab, 0, 1.0)
cli/chat.py:3322:                # factual score-composition intermediates (replayer self-validation)
cli/chat.py:3450:    # H_9738 · persist the FINAL W_S composition (keys + act) so a later run can transplant it
cli/evaluate.py:1321:    print("      bind_delta (composition-isolating), the statistic's OWN pedestal. The legacy line")
cli/evaluate.py:1333:    print("      across the arms and cancels, so Δ>0 = composition sensitivity. The bar is DERIVED,")
cli/evaluate.py:2475:        h = E.hab_new(4, dec); fr = E.hab_response(h, 0, 1.0)
cli/evaluate.py:2477:        return float(sc) + float(fr - E.hab_response(h, 0, 1.0))
cli/evaluate.py:5597:    Δ>0 (composition-helps) direction. Closed-form, deterministic (no RNG · p7/frozen). m<5 ⇒ even
cli/evaluate.py:5649:    """H_9745 — the composition-isolating paired verdict on bind_delta, replacing the marginal
cli/evaluate.py:5710:    is the composed one than when it is deranged = composition sensitivity, not echo.
cli/evaluate.py:5766:    # ── H_9745: paired McNemar + TOST on bind_delta (the composition-isolating statistic) ──
cli/evaluate.py:5767:    # The marginal null above (composed J vs mismatched pairs) tests EMISSION, not composition —
cli/evaluate.py:5784:    a PASS here says the emission is composition-sensitive on the frozen frames, NOT that the
cli/evaluate.py:5840:    # composition-isolating statistic. The line above (composed J > marginal null) tests EMISSION;
cli/evaluate.py:5841:    # THIS tests composition. Read THIS for a lever's bind claim. ──
cli/evaluate.py:5843:    print("  ── H_9745 PAIRED (bind_delta's own null · composition ≠ emission) ──")
cli/evaluate.py:5862:    # only when BOTH signals agree: PAIRED-SENSITIVE (McNemar composition test above) AND
cli/evaluate.py:5879:        _dg = ("🧱 BIND-ABSENT", "TOST 등가 — 레버가 composition 안 심음")
cli/evaluate.py:8486:    and `base_motiv` logs motivation_score's own output — so the decomposition is CHECKABLE.
cli/evaluate.py:9452:    # The observation sits ABOVE the composition prediction. A real misalignment would put it
cli/evaluate.py:9576:    # there is no "composition failure" left to explain.
cli/evaluate.py:15442:    implementation never existed). Total variance decomposition says
                     "CUDA_VISIBLE_DEVICES='' (slow — toy scale only)." % (device, meminfo))
        raise


def main():
    ap = argparse.ArgumentParser(
        description="anima canonical python trainer (`anima-py train`) — CLMConvMoE "
                    "SAVANT+MITOSIS recipe + H_1640 arm×objective compositional levers")
    ap.add_argument("--arch", default="clm", choices=["clm", "bytegpt"],
                    help="trunk architecture: clm=CLMConvMoE (default, .clm out) | "
                         "bytegpt=24-layer GPT-2-class ByteGPT (.bin out) — the CLEAN G1 "
                         "wall (single=2). The arm×objective compositional levers are "
                         "arch-agnostic (operate on logits+penultimate); the CLM-specific "
                         "levers (savant/mitosis/tlora/dict/jamo) are gated OFF for bytegpt.")
    ap.add_argument("--arm", default="ctrl", choices=list(ARMS))
    ap.add_argument("--objective", default="ce_marginal", choices=list(OBJECTIVES),
                    help="OPTIONAL objrun coupling (default ce_marginal = standalone)")
    ap.add_argument("--tlora-rank", type=int, default=TLORA_RANK)
    ap.add_argument("--tlora-no-base", action="store_true", help="drop the dense base")
    ap.add_argument("--dict-lambda", type=float, default=DICT_LAMBDA)
    ap.add_argument("--jamo-lambda", type=float, default=JAMO_LAMBDA)
    # H_9643: enable the N8 jamo(자모) teach-aux INDEPENDENTLY of --arm, so a faction run
    # (--arm ctrl --n-factions 8) can borrow the ko-coherence signal without the TLoRA that
    # tlora_jamo bundles (which would confound the faction measurement). Default off = unchanged.
    ap.add_argument("--jamo-aux", action="store_true",
                    help="H_9643: turn on the jamo teach-aux head regardless of --arm (no tlora)")
    # H_9200 E1 — gated-write forward-slot (SLW). --slw engages the CORE-owned
    # (core/slw.py) module on the CLMConvMoE penultimate; weights serialize into the
    # "SLW\x01" .clm trailer. Plain CE alone induces the slots (rung-3 de-risk 0.976
    # vs additive 0.145), so this is an ARCH lever (--objective stays ce_marginal).
    ap.add_argument("--slw", action="store_true",
                    help="H_9200 E1: engage the gated-write forward-slot (core/slw.py)")
    ap.add_argument("--slw-n-slot", type=int, default=8, help="SLW addressable slots")
    ap.add_argument("--slw-k", type=int, default=64, help="SLW role/read key dim")
    # H_9423 CLMS store-bridge lane (co-trained). --store-bridge = the storebind corpus c.txt (expects
    # a lockstep <c>.store.jsonl manifest, line i <-> store row i from corpus.build_storebind). The lane
    # OVERWRITES the answer-position logits with lam*store_logits — implemented as a CE decomposition
    # (qpos CE on store_logits + non-qpos trunk CE on the prompt spelling), so the trunk logit gets NO
    # answer-position grad = ② shortcut-cut, structural. Window geometry mirrors evaluate.store_run
    # (prompt-aligned, qpos = T-1) so the train tap and the verdict tap coincide.
    ap.add_argument("--store-bridge", type=str, default="",
                    help="H_9423: storebind corpus c.txt to co-train the CLMS lane (core/clms.py)")
    ap.add_argument("--store-win", type=int, default=24,
                    help="CLMS window (MUST equal evaluate --win so train/verdict geometry match)")
    ap.add_argument("--store-batch", type=int, default=8, help="global CLMS sub-batch (div by world)")
    ap.add_argument("--store-ans-weight", type=float, default=1.0, help="answer-position store CE weight")
    ap.add_argument("--store-val-frac", type=float, default=0.05, help="tail block frac for sb val")
    ap.add_argument("--clms-n-slot", type=int, default=8, help="CLMS store slots (match corpus)")
    ap.add_argument("--clms-d-k", type=int, default=64, help="CLMS content-address key dim")
    ap.add_argument("--clms-d-s", type=int, default=64, help="CLMS polarity value dim")
    ap.add_argument("--clms-d-g", type=int, default=64, help="CLMS fusion-bottleneck (yn_q op-gate dim; H_9423 value-read fix)")
    ap.add_argument("--store-fangate", action="store_true",
                    help="H_9696 (R4) CLMS-FAN lane (lane_type 4): the value is projected from the slot's "
                         "OWN key (free ideation has no polarity to index) + a learned query gate replaces "
                         "the '=> ' literal. Default off = the H_9423 storebind lane, byte-identical.")
    ap.add_argument("--store-val-center", action="store_true",
                    help="H_9710 RV-3: majority-null centering v=Σ(aᵢ−1/n)·valᵢ (lane_type 3). At uniform address "
                         "v≡0 so the op⊕majority shortcut basin cannot exist. train+eval consistent (codec bit).")
    ap.add_argument("--store-addr-weight", type=float, default=0.0,
                    help="H_9672: address direct-supervision loss weight L_addr=CE(att,target_slot) (0=off·byte-identical). Cuts the (2) bootstrap deadlock W_q could not escape at 303M.")
    ap.add_argument("--store-query-src", type=str, default="penult",
                    help="H_9720-ⓐ EN-disjoint fresh query lane: 'penult' (default·lane_type≤4·byte-identical) OR "
                         "'fresh:K[@L]' (lane_type 5) — the ADDRESS query reads a detached trunk-layer-L tap "
                         "through W_fresh→W_q_fresh (store-CE only, EN-CE never touches it), K=lane width, "
                         "L=tap depth (default 3, RF≥entity-span). '@penult' (fresh_L=0) = H_9720 C1 "
                         "param-matched-penult control: same head, tap at the penult (capacity vs depth). "
                         "Emergent-address WITHOUT addr-loss (admissible).")
    ap.add_argument("--store-query-tap-grad", type=str, default="detached", choices=["detached", "shared"],
                    help="H_9720 C2 detach-ablation for --store-query-src fresh: 'detached' (default·the CRACK "
                         "arm·store-CE never reaches the trunk through the tap) OR 'shared' (drop .detach() so "
                         "store-CE DOES flow into layers ≤ fresh_L) — tests if gradient-disjointness is load-bearing.")
    ap.add_argument("--store-ans-delay", type=int, default=0,
                    help="H_9692 RV-2: hold the answer-CE (sb_w=0) for the first N steps so only the address "
                         "(addr-loss) trains; the blurry-v window can\'t commit the MLP to op-only before the "
                         "address is sharp. Then ans-CE turns on. 0=off·byte-identical.")
    ap.add_argument("--store-oracle-aux", type=float, default=0.0,
                    help="H_9691 RV-1: weight of an extra CE on the ORACLE(correct one-hot) address every step "
                         "(dual-path with softmax+--store-addr-weight) → trains the value/MLP on correct v so it "
                         "learns the XOR function robustly (fixes val-read seed-fragility). 0=off·byte-identical.")
    ap.add_argument("--store-oracle-train", action="store_true",
                    help="H_9423 Stage1.5: hand the address for free during TRAINING (oracle_slot=target_slot) "
                         "→ separates value-read (a) from address-learning (c). DIAGNOSTIC, not a production lever.")
    ap.add_argument("--store-oracle-warmup", type=int, default=0,
                    help="H_9672: for the first N steps hand the address free (oracle_slot) so val differentiates "
                         "cleanly, THEN switch to softmax address (+ --store-addr-weight learns W_q on the "
                         "differentiated val). Fixes the val-read seed-fragility addr-loss alone left. 0=off.")
    ap.add_argument("--clms-r", type=int, default=128, help="CLMS GELU-MLP fusion bottleneck")
    ap.add_argument("--clms-key-seed", type=int, default=9423, help="CLMS frozen key_emb table seed")
    ap.add_argument("--clms-lam0", type=float, default=1.0, help="CLMS lam init (store_only scale)")
    # H_9698 MBND mouth-binder lane (R6). --mouth-binder engages it; the linear arm is the INTERNAL
    # NEGATIVE CONTROL that must reproduce kill#7's fixed-role linear collapse (uniform address +
    # additive combine), so a nonlinear number is only readable next to it.
    ap.add_argument("--mouth-binder", choices=["bilinear", "linear"], default="",
                    help="H_9698: co-train the MBND mouth-binder lane. bilinear = Hadamard binder; "
                         "linear = the kill#7 DOA control (uniform address + additive combine)")
    ap.add_argument("--mouth-memory", choices=["causal-bank"], default="causal-bank",
                    help="H_9698: what the binder addresses (causal-bank = the frame's own hiddens)")
    # ── H_9803 BRANCH-LATENT IDEATION FAN (ρ·fan / G6 lane) ──────────────────────────────────
    # The lane is DEFAULT-OFF and every flag below is inert unless --ideation-lane branch-latent
    # is passed ⇒ byte-identical golden path. See core/ifan.py for why this is not a sampling
    # trick: the ONLY thing separating the K branches is a min-cost assignment onto SEVERAL REAL
    # observed continuations. There is no repulsion term and no entropy bonus anywhere in the lane.
    ap.add_argument("--ideation-lane", choices=["off", "branch-latent"], default="off",
                    help="H_9803: 'branch-latent' builds K disjoint proposal latents from a preserved "
                         "early tap, each responsible for a DIFFERENT observed future-continuation mode. "
                         "'off' (default) ⇒ byte-identical.")
    ap.add_argument("--ideation-branches", type=int, default=4,
                    help="H_9803: K — number of disjoint proposal latents (branches).")
    ap.add_argument("--ideation-objective", choices=["set-ce"], default="set-ce",
                    help="H_9803: 'set-ce' = min-cost (Hungarian) branch↔target assignment over the SET "
                         "of observed continuations, then mean assigned CE. The only objective that "
                         "grounds diversity in real futures; a repulsion/entropy variant is DISQUALIFIED.")
    ap.add_argument("--ideation-route", choices=["l3-disjoint", "penult"], default="l3-disjoint",
                    help="H_9803: 'l3-disjoint' = the branch latents read the DETACHED trunk-layer-L tap "
                         "(H_9720 tap-DEPTH; set-CE never pushes the trunk through this path) · "
                         "'penult' = read the penultimate instead (tap-DEPTH control).")
    ap.add_argument("--ideation-route-l", type=int, default=3,
                    help="H_9803: L — tap depth for --ideation-route l3-disjoint (default 3).")
    ap.add_argument("--ideation-assign", choices=["hungarian", "shuffle"], default="hungarian",
                    help="H_9803: 'hungarian' = min-cost matching (treatment) · 'shuffle' = THE NEGATIVE "
                         "CONTROL — same K, same targets, same CE mass, but the target↔branch assignment "
                         "is re-drawn every batch, so only the correspondence is destroyed.")
    ap.add_argument("--ideation-corpus", type=str, default="",
                    help="H_9803: multi-mode future-set corpus. Blank-line-separated documents; line 0 = "
                         "the shared context/topic, lines 1..M = M DIFFERENT observed continuations of it. "
                         "REQUIRED when --ideation-lane branch-latent.")
    ap.add_argument("--ideation-rank", type=int, default=64, help="H_9803: proposal-latent width r")
    ap.add_argument("--ideation-lam0", type=float, default=1.0, help="H_9803: IFAN lam init (additive scale)")
    ap.add_argument("--ideation-weight", type=float, default=1.0, help="H_9803: set-CE loss weight")
    ap.add_argument("--ideation-docs", type=int, default=4, help="H_9803: documents per ideation sub-batch")
    # ── H_9805 WRITE-SIDE TENSION FIELD (TFLD lane) ──────────────────────────────────────────
    # Production's tension is a SCALAR on the READOUT side (`conflict_scalar`, rank ~2.66 per
    # H_9714) — the rank-1 seam v1 died on. This lane injects the per-edge parse-disagreement
    # FIELD pre-trunk instead. The lane is DEFAULT-OFF ⇒ byte-identical golden path.
    # `rank1` is NOT a lesser treatment: it is the control that decides whether the field is a
    # field at all, and it is parameter-, lam- and shape-matched to `duel`. See core/tension_field.py.
    ap.add_argument("--tension-field", choices=["off", "duel", "rank1"], default="off",
                    help="H_9805: 'duel' = the full per-edge L→R/R→L parse-disagreement field, added "
                         "to the embeddings BEFORE the trunk · 'rank1' = THE CONTROL — the same "
                         "reduction fed the best rank-1 approximation of that same field (identical "
                         "params/lam/shape; the ONE variable is field-vs-its-own-scalar-summary) · "
                         "'off' (default) ⇒ byte-identical, no trailer.")
    ap.add_argument("--tension-field-rank", type=int, default=32,
                    help="H_9805: TFLD inner width r for phi (n_bucket, r) and W_up (r, d).")
    ap.add_argument("--tension-field-lam0", type=float, default=1.0,
                    help="H_9805: TFLD lam init (additive pre-trunk scale).")
    ap.add_argument("--trunk-norm", choices=["global", "position"], default="global",
                    help="H_9814: trunk normalization statistics. global = legacy GroupNorm over "
                         "(C,T) — measurably NON-CAUSAL (H_9813: masking input bytes AFTER t moved "
                         "the prediction AT t by 0.5964 nats). position = per-position (causal-safe "
                         "contrast arm). ⚠️ .clm decode implements GLOBAL semantics, so a position "
                         "ckpt is a torch-side DIRECTIONAL screen only until a decode lane exists.")
    ap.add_argument("--serialize-parity", default="",
                    help="H_9813: after writing the .clm, re-score this bind-panel through BOTH "
                         "the trained torch model and the serialized .clm and report agreement. "
                         "The trainer is the only place that holds both ends at once. Comparison "
                         "only — it never says the model is good or bad.")
    ap.add_argument("--tension-concord", choices=["class", "lex", "morph"], default="class",
                    help="H_9812: what the TFLD concord term compares. lex = the CHUNK SIGNATURE "
                         "(the field sees WHICH words agree). morph = the chunk's FINAL BYTE, the "
                         "closest analogue of v4's honorific concord and the one English agreement "
                         "morphology actually lives in (verb +s/+ing, noun +s). "
                         "class = byte_class, the LEGACY/CONTROL mode, measured to be a function of "
                         "the whitespace+punct layout ALONE (swap every letter, or letters for "
                         "digits, and the field is BIT-IDENTICAL). Keep `class` as the layout-only "
                         "pedestal arm; do not build a claim on it.")
    ap.add_argument("--answer-ce-weight", type=float, default=0.0,
                    help="H_9811: extra CE weight on the ANSWER span of ` => ` arrow lines "
                         "(loss = obj + w*ce_answer). 0 = OFF, byte-identical to today. The "
                         "answer is ~6%% of a bind-panel line, so a plain next-byte CE leaves "
                         "the binding bit at chance (measured: d_acc 0.5000 on DRILLED lexemes, "
                         "one token emitted 68-86%% of slots, and 5.9x params/6.7x steps made it "
                         "WORSE). v4 H_004's amendment A1 used ce_surf + 5*ce_ans.")
    ap.add_argument("--bind-rank", type=int, default=64, help="H_9698: MBND binder rank (q/k/v/u width)")
    ap.add_argument("--bind-lam0", type=float, default=1.0, help="H_9698: MBND lam init (additive scale)")
    ap.add_argument("--freeze-trunk", action="store_true",
                    help="BOLT control arm: trunk requires_grad=False, only clms.* trains")
    # H_9643 faction lane: split the d channels into K contiguous groups (grouped conv + GN(K) +
    # cross-faction bridge). 0 = OFF, byte-identical to a standard trunk. The real arm trains K=8 vs
    # K=1 FREELY (no forced routing — the ORACLE dose was only the toy's instrument positive control)
    # then reads specialization with `anima-py evaluate --faction-lesion`. d % K must be 0.
    ap.add_argument("--n-factions", type=int, default=0,
                    help="H_9643: K contiguous faction blocks on the d axis (0 = OFF, byte-identical)")
    ap.add_argument("--faction-bridge-lam0", type=float, default=0.1,
                    help="H_9643: initial cross-faction bridge scale (K>0 only)")
    ap.add_argument("--seed", type=int, default=7)
    # a `<corpus>.meta.json` written by `anima-py corpus` carries the budget floor that corpus
    # earned; _budget_preflight refuses to start below it (H_9324) — see cli/corpus.py BUDGET_FLOORS.
    ap.add_argument("--corpus", nargs="*", default=[])
    ap.add_argument("--cell-label", nargs="*", default=[])
    ap.add_argument("--canon", action="store_true")
    ap.add_argument("--d", type=int, default=0)
    ap.add_argument("--L", type=int, default=0)
    ap.add_argument("--steps", type=int, default=0)
    ap.add_argument("--seq-len", type=int, default=0)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--e0", type=int, default=2)
    ap.add_argument("--emax", type=int, default=3)
    ap.add_argument("--no-savant", action="store_true")
    ap.add_argument("--no-mitosis", action="store_true")
    if "--bind-panel" in argv:
        return bind_panel_run(argv)
    # --store-addr-census <dump.npz> / --store-census-selftest: H_9719 emergent-address
    # $0 pre-screen — argmax-collision of random-W_q over entity-keys vs a structureless-H
    # pedestal. DIRECTIONAL screener (KILL-before-spend); admissible (no target_slot read).
    if "--store-addr-census" in argv or "--store-census-selftest" in argv:
        return store_addr_census_run(argv)
    # --faction-phi-proxy <prompts.json>: the ARCHIVED faction Phi proxy recomputed on live
    # trunk activations vs a zero-truth PEDESTAL (H_9660/H_9654 · faction-lateral-axis-r3).
    # Indicts the formula; never cements a consciousness verdict (a_phi_iit4_tool).
    if "--faction-phi-proxy" in argv:
        return faction_phi_proxy_run(argv)
    # --faction-block-structure <prompts.json>: does the trunk unit axis carry faction-like
    # modular blocks at all (H_9674)? The $0 precondition for H_9643's GPU fire.
    if "--faction-block-structure" in argv:
        return faction_block_structure_run(argv)
    # --faction-lesion <domains.json>: is the trained faction split FUNCTIONAL, or the same as
    # slicing channels at random after the fact? (H_9643 Q2 · chance = post-hoc null95)
    if "--faction-lesion" in argv:
        return faction_lesion_run(argv)
    # --faction-block-provenance: H_9674 블록이 진짜 모듈인가 architecture index layout(GN/RF)인가 (H_9676)
    if "--faction-block-provenance" in argv:
        return faction_block_provenance_run(argv)
    # --interaction-lift <manifest.json>: read-only engine-native joint interaction-lift
    # NLL surface (H_9255). argv[0]=ckpt; interaction_lift_run reads --interaction-lift/--out.
    if "--earned" in argv:
        import earned as _earned
        return _earned.earned_run(argv)
    if "--interaction-lift" in argv:
        return interaction_lift_run(argv)
    # --probe <spec.json>: matched-surface G1 probe (card H_6189). argv[0]=ckpt; probe_run
    # reads --probe/--gen from the tail. Greedy raw-continuation dump for offline scoring.
    if "--probe" in argv:
        return probe_run(argv)
    # --xbind <manifest.json>: held-out XBIND recombination (G1 reopen lane a · card H_9267).
    # argv[0]=ckpt; xbind_run reads --xbind/--out/--arm from the tail. Engine-native greedy
    # D-acc on held-out xor(pol_a,pol_b) pairs (the corpus×task-class measure-swap exit).
    if "--bridge-trace" in argv:
        return bridge_trace_run(argv)
    # --store-mix <store.json> [--store-lambda λ]: H_9392 BRIDGE-BOLT — bolt a runtime
    # store-lookup onto the frozen trunk (p = λ·p_store + (1−λ)·p_trunk at the measured
    # answer position). SEQUENTIAL C0 gate (λ=0 byte-identical to baseline) inside the run.
    if "--store-mix" in argv:
        return store_mix_run(argv)
    # --store <held.json> [--store-oracle] [--store-lambda λ]: H_9423 CLMS store-bridge lane — the
    # CO-TRAINED bridge (store injected at the query, answer-position logits OVERWRITTEN by the lane's
    # content-addressed lookup). Distinct from --store-mix (H_9392 post-forward actuator).
    if "--fan-bind" in argv:                       # H_9693 (R1) bind-Δ instrument
        return fan_bind_run(argv)
    if "--store" in argv:
        return store_run(argv)
    if "--xbind" in argv:
        return xbind_run(argv)
    # --xfan <manifest.json>: held-out XFAN one-to-many fan (G6 reopen lane · card H_9271).
    # coverage C over K sampled decodes per held-out concept (the corpus×task-class one-to-many
    # measure — the G6 homolog of XBIND's 1-bit discrimination).
    if "--xfan" in argv:
        return xfan_run(argv)
    return evaluate_run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)

exec
/bin/zsh -lc "rg -n -i \"comp[-_ ]lane|answer span|penultimate detached|whole answer|H_9900|H_9899|H_9883|H_9875\" . --glob '"'!archive/**'"' --glob '"'!BRAIN/**'"' | sed -n '1,420p'
rg -n \"argparse|--[a-z]\" cli/evaluate.py | tail -n 260
rg -n \"anima_flag_value\\(_cargv|--[a-z]\" cli/chat.py | sed -n '1,360p'" in /Users/mini/dancinlab/anima
 succeeded in 322ms:
./ARCHITECTURE.json:18424:    "threshold": "재발조건 = 새 loss 항/마스크/가중이 '위치 집합' 을 고르는 모든 경우(answer span · role span · slot mask · segment weight). 특히 학습 데이터가 **이어붙여져 창으로 잘리는** 형식이면 span 은 반드시 **레코드 구분자(개행 등)로 우측을 닫아야** 한다 — 안 닫으면 다음 레코드를 조용히 가중한다. 해결 = (1) 항을 켠 첫 실행에서 **선택된 위치 수를 로그에 찍고 손으로 계산한 기대값과 대조하라**(4B 답 × batch 8 = 32; 365 가 나오면 그 자리서 버그다) (2) 그 대조 **전에는 그 항으로 어떤 판정도 발행하지 않는다** — 특히 🔴 반증(음성 판정은 계기 결함과 구별이 안 된다) (3) span 마스크는 좌·우 경계를 **둘 다** 명시하라. 시작만 정의하고 끝을 창에 맡기면 창 크기가 곧 버그 크기다.",
./cli/evaluate.py:3711:    Same right-aligned window and answer span (lo..T−1) as _xbind_cont_nll, so the two
./cli/train.py:895:    """(B, T) bool — True on target positions that lie in the ANSWER span of an arrow line.
./cli/train.py:923:    # right bound: the first newline at or after `start` closes the answer span
./cli/train.py:1807:                    help="H_9811: extra CE weight on the ANSWER span of ` => ` arrow lines "
13433:    `anima-py evaluate --pc2-direction <dir> --zeta-slope --by-loading [--tost 0.02]
13434:       [--pos-control-beta -0.081] [--perm N] [--seed N]`
13447:        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <dir> --zeta-slope --by-loading")
13449:    rounds = evaluate_intval(argv, "--perm", 2000)
13450:    rseed = evaluate_intval(argv, "--seed", 20260717)
13460:    tost = _fval("--tost", 0.02)
13461:    pos_beta = _fval("--pos-control-beta", -0.081)
13527:    print("=== anima evaluate --pc2-direction --zeta-slope --by-loading — H_9755 refit-axis 판정 ===")
13569:                continue                                   # not a --z-loading row
13749:    """H_9664 ZETA-SLOPE — the within-tick dose readout. Reads `anima-py chat --pc2-zeta` traces.
13751:    `anima-py evaluate --pc2-direction <traces_dir> --zeta-slope [--perm N] [--seed N]`
13793:        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --zeta-slope")
13795:    rounds = evaluate_intval(argv, "--perm", 2000)
13796:    rseed = evaluate_intval(argv, "--seed", 20260717)
13846:    print("=== anima evaluate --pc2-direction --zeta-slope — H_9664 within-tick 용량 판정 ===")
13958:    `anima-py evaluate --pc2-direction <traces_dir> --occupancy [--perm N] [--seed N]`
14007:        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --occupancy")
14009:    rounds = evaluate_intval(argv, "--perm", 2000)
14010:    rseed = evaluate_intval(argv, "--seed", 20260717)
14052:    print("=== anima evaluate --pc2-direction --occupancy — R-A 창-점유율 (card H_9636) ===")
14305:    `anima-py evaluate --pc2-direction <traces_dir> [--perm N] [--seed N]`
14307:    Reads the traces `anima-py chat --pc2-mouth {off,bias,rng}` already wrote (NO decode, like
14308:    --emit-gate-census / --dead-census) and renders the three frozen criteria of the PC2→mouth
14333:    if "--z-census" in argv:                      # H_9712 dose/exposure gate (sister sub-mode)
14338:        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> [--perm N] [--seed N]")
14340:    if "--cascade-null" in argv:
14342:    rounds = evaluate_intval(argv, "--perm", 2000)
14343:    rseed = evaluate_intval(argv, "--seed", 20260716)
14372:    print("=== anima evaluate --pc2-direction — PC2→MOUTH (card H_9576) ===")
14375:    print("pipe:   anima-py chat --pc2-mouth {off,bias,rng} traces → D=bigram-overlap(text, seed)")
14532:    `anima-py evaluate --pc2-direction <traces_dir> --cascade-null [--perm N] [--seed N]`
14576:    rounds = evaluate_intval(argv, "--perm", 2000)
14577:    rseed = evaluate_intval(argv, "--seed", 20260716)
14711:    print("=== anima evaluate --pc2-direction --cascade-null — ΔD ZERO-TRUTH PEDESTAL (card H_9629) ===")
14904:    print("       anima-py chat --pc2-mouth cascade --pc2-zeta 0   <ckpt>  # 2nd-best byte @ 1 lm-step")
14905:    print("       anima-py chat --pc2-mouth bias    --pc2-zeta 4   <ckpt>  # ζ=+4 saturation arm")
14906:    print("       anima-py chat --pc2-mouth bias    --pc2-zeta -4  <ckpt>  # ζ=-4 saturation arm")
14919:#   anima-py evaluate --stream-mi <path> [--shuffle-floor derived|off] [--win 4096]
14920:#                                        [--span 2048] [--out f.json] [--n-segments 30]
14921:#   anima-py evaluate --capture-anchor <path> [--k 8] [--out f.json] [--n-segments N]
14932:# THE FLOOR IS DERIVED, NEVER ASSUMED. `--shuffle-floor derived` (the default) recomputes the
14949:    """`anima-py evaluate --stream-mi [<path>] [--shuffle-floor derived|off] ...` — H_9806."""
14952:    path = _mi_positional(argv, "--stream-mi")
14953:    win = evaluate_intval(argv, "--win", mi.W_TAIL)
14954:    span = evaluate_intval(argv, "--span", mi.P_PRED)
14955:    nseg = evaluate_intval(argv, "--n-segments", 30)
14956:    floor_mode = evaluate_strval(argv, "--shuffle-floor", "derived")
14957:    out_path = evaluate_strval(argv, "--out", "stream_mi.json")
14959:        print("ERROR: --shuffle-floor takes 'derived' (default) or 'off', got %r" % floor_mode,
14963:    print("=== anima evaluate --stream-mi — H_9806 CROSS-BOUNDARY CONDITIONAL-bpb BATTERY ===")
15022:              "with --shuffle-floor derived to obtain a readable collapse-Δ.")
15066:    """`anima-py evaluate --capture-anchor [<path>] [--k 8] [--out f.json]` — H_9806.
15073:    path = _mi_positional(argv, "--capture-anchor")
15074:    win = evaluate_intval(argv, "--win", mi.W_TAIL)
15075:    span = evaluate_intval(argv, "--span", mi.P_PRED)
15076:    pk = evaluate_intval(argv, "--k", mi.PRIMARY_K)
15077:    out_path = evaluate_strval(argv, "--out", "capture_anchor.json")
15079:    print("=== anima evaluate --capture-anchor — H_9806 SHIFT-NULL LOO CAPTURE ===")
15089:    n_live = evaluate_intval(argv, "--n-segments", len(feats) if feats else 40)
15185:    """Return an error string for the first unknown --flag in argv, else ''."""
15195:            "\n  (an unknown flag is rejected, not ignored — a silently-dropped --out " \
15295:    """`anima-py evaluate <ckpt> --bridge-trace <flip1.json> --flip0 <flip0.json> --out <f.json>`
15305:    f1_path = evaluate_strval(argv[1:], "--bridge-trace", "")
15306:    f0_path = evaluate_strval(argv[1:], "--flip0", "")
15307:    out_path = evaluate_strval(argv[1:], "--out", "bridge_trace.json")
15308:    n_perm = evaluate_intval(argv[1:], "--perm", 2000)
15309:    seed_rng = evaluate_intval(argv[1:], "--seed", 7)
15310:    theta = float(evaluate_strval(argv[1:], "--theta", "0.5"))
15314:    T = evaluate_intval(argv[1:], "--win", int(f1.get("win", 64)))
15315:    print("=== anima evaluate --bridge-trace — L4 path-attribution census (H_9388) ===")
15421:        print("  no --flip0 manifest given — gate NOT run (flip1 read is uncalibrated)")
15434:    """`anima-py evaluate <ckpt> --faction-phi-proxy <prompts.json> [--n-factions-sweep 1,2,4,8,12,16,24,32,64]
15435:    [--win 24] [--trials 200] [--seed 12345] [--out faction_phi.json]` — the ARCHIVED faction
15468:    spec_path = evaluate_strval(argv[1:], "--faction-phi-proxy", "")
15469:    out_path = evaluate_strval(argv[1:], "--out", "")
15470:    T = evaluate_intval(argv[1:], "--win", 24)
15471:    trials = evaluate_intval(argv[1:], "--trials", 200)
15472:    seed = evaluate_intval(argv[1:], "--seed", 12345)
15473:    ks_s = evaluate_strval(argv[1:], "--n-factions-sweep", "1,2,4,8,12,16,24,32,64")
15476:    print("=== anima evaluate --faction-phi-proxy — archived faction Phi on live trunk (H_9660/H_9654) ===")
15568:    """`anima-py evaluate <ckpt> --faction-block-structure <prompts.json> [--n-factions-sweep 2,4,8,12,16]
15569:    [--win 24] [--seed 12345] [--out blocks.json]` — does the trunk's unit axis carry faction-like
15602:    spec_path = evaluate_strval(argv[1:], "--faction-block-structure", "")
15603:    out_path = evaluate_strval(argv[1:], "--out", "")
15604:    T = evaluate_intval(argv[1:], "--win", 24)
15605:    seed = evaluate_intval(argv[1:], "--seed", 12345)
15606:    ks = [int(x) for x in evaluate_strval(argv[1:], "--n-factions-sweep", "2,4,8,12,16").split(",") if x.strip()]
15608:    print("=== anima evaluate --faction-block-structure — does the substrate HAVE blocks? (H_9674) ===")
15704:    # --arm-random-init: SAME architecture, SAME production forward, weights re-drawn from their
15712:    if "--arm-random-init" in argv:
15840:    """`anima-py evaluate <ckpt> --faction-block-provenance <prompts.json> [--n-factions-sweep 4,8,12]
15841:    [--win 24] [--seed 12345] [--out prov.json]` — are H_9674's blocks REAL modules, or an artifact
15869:    spec_path = evaluate_strval(argv[1:], "--faction-block-provenance", "")
15870:    out_path = evaluate_strval(argv[1:], "--out", "")
15871:    T = evaluate_intval(argv[1:], "--win", 24)
15872:    seed = evaluate_intval(argv[1:], "--seed", 12345)
15873:    ks = [int(x) for x in evaluate_strval(argv[1:], "--n-factions-sweep", "4,8,12").split(",") if x.strip()]
15874:    print("=== anima evaluate --faction-block-provenance — H_9674 blocks: real or layout? (H_9676) ===")
15895:        """Same spectral+sweeps clusterer as --faction-block-structure; returns the ASSIGNMENT."""
16008:    """`anima-py evaluate <ckpt> --faction-lesion <domains.json> [--perm 200] [--win 24]
16009:    [--seed 12345] [--faction-lam <float>] [--out lesion.json]` — does the trained model's
16014:    architectural, so a random-init model has blocks too — our own --arm-random-init measured
16015:    exactly that. Q is a manipulation check here ("did --n-factions do anything"); the verdict is
16023:    Chance is MEASURED, never assumed: `--perm` post-hoc reassignments of the same d channels to
16030:      post-hoc  — `--perm` random reassignments, same sizes. THE control H_9643 is about:
16040:    spec_path = evaluate_strval(argv[1:], "--faction-lesion", "")
16041:    out_path = evaluate_strval(argv[1:], "--out", "")
16042:    T = evaluate_intval(argv[1:], "--win", 24)
16043:    nperm = evaluate_intval(argv[1:], "--perm", 200)
16044:    seed = evaluate_intval(argv[1:], "--seed", 12345)
16045:    lam_ov = evaluate_strval(argv[1:], "--faction-lam", "")
16046:    # --faction-oracle-pi "2,0,0,3": the KNOWN routing of an ORACLE-trained ckpt. Present => run the
16050:    pi_ov = evaluate_strval(argv[1:], "--faction-oracle-pi", "")
16051:    # --faction-split N: impose an N-way CONTIGUOUS channel split at lesion time, INDEPENDENT of the
16057:    split_ov = evaluate_intval(argv[1:], "--faction-split", 0)
16059:    print("=== anima evaluate --faction-lesion — 파벌 분할이 기능적인가 (H_9643) ===")
16062:    print("       블록을 준다(--arm-random-init 이 잡음). 판정은 기능 lesion 해리로 간다.")
16071:    # n_factions; --faction-split overrides it (H_9737: impose 4 groups on a groups=1 ckpt). The
16075:        print("ERROR: split 수 미정 — 이 ckpt 엔 CLMF 가 없다 (n_factions=0) 이고 --faction-split 도 없다.")
16076:        print("       --n-factions K 로 학습한 ckpt 이거나, --faction-split N 으로 분할을 강제하라.")
16079:        print("       --faction-split %d 강제 (ckpt n_factions=%d) — lesion 분할만 override, 모델 구조 무접촉"
16179:    # free, base_CE-immune (cosine cancels scale). Only computed when --faction-oracle-pi is given.
16234:              " (검정력-before-negative). --perm 200 이상 재발사 필요." % nperm)
16247:    """`anima-py evaluate --closure-ladder [--closure-arm {live,open,dead}]
16248:                          [--closure-ticks N] [--closure-seed S] [--out f.json]`
16260:    Bare (no --closure-arm) runs the 3-plant CERTIFICATION battery, which is the only
16279:    rest = [a for a in argv if a != "--closure-ladder"]
16280:    arm = evaluate_strval(rest, "--closure-arm", "")
16281:    seed = evaluate_intval(rest, "--closure-seed", 7)
16282:    ticks = evaluate_intval(rest, "--closure-ticks", 600)
16283:    out_path = evaluate_strval(rest, "--out", "")
16285:        print("ERROR: --closure-ticks %d gives fewer than 2 LV-C blocks (BLOCK=%d); the "
16291:            print("ERROR: unknown --closure-arm %r (known: live, open, dead)" % arm,
16310:    if len(argv) >= 1 and argv[0] in ("-h", "--help"):
16320:    if "--collide-select" in argv:
16323:    # H_9807 --closure-ladder: the interventional CLOSURE rig (rung 1). Ckpt-less by
16326:    if "--closure-ladder" in argv:
16328:    if len(argv) >= 1 and argv[0] == "--workspace-smoke":
16333:    if len(argv) >= 1 and argv[0] == "--workspace-semantic":
16338:    if len(argv) >= 1 and argv[0] == "--workspace-divergence":
16340:    if len(argv) >= 1 and argv[0] == "--workspace-regression":
16344:        out_path = evaluate_strval(argv[1:], "--out", "")
16350:    if "--workspace-divergence-realizer" in argv:
16352:            [a for a in argv if a != "--workspace-divergence-realizer"])
16353:    if "--workspace-reach-only" in argv:
16354:        return workspace_reach_only_run([a for a in argv if a != "--workspace-reach-only"])
16359:    if len(argv) >= 1 and argv[0] == "--pregate-selftest":
16361:    if len(argv) >= 2 and argv[0] == "--falsifier-headroom":
16363:    if len(argv) >= 2 and argv[0] == "--free-slot-score":
16365:    if len(argv) >= 2 and argv[0] == "--register-leak-probe":
16367:    if len(argv) >= 1 and argv[0] == "--refractory-preview":
16369:    if len(argv) >= 1 and argv[0] == "--emit-gate-census":
16371:    if len(argv) >= 1 and argv[0] == "--pc2-direction":
16372:        if "--state-census" in argv:
16373:            return _pc2_state_census([a for a in argv[1:] if a != "--state-census"])
16374:        if "--occupancy" in argv:
16375:            return _pc2_occupancy([a for a in argv[1:] if a != "--occupancy"])
16376:        if "--zeta-slope" in argv:
16377:            _zrest = [a for a in argv[1:] if a != "--zeta-slope"]
16378:            if "--by-loading" in argv:
16379:                return _pc2_zeta_by_loading([a for a in _zrest if a != "--by-loading"])
16381:        if "--atom-census" in argv:
16382:            return _pc2_atom_census([a for a in argv[1:] if a != "--atom-census"])
16383:        if "--rank-null" in argv:
16385:        if "--factor-census" in argv:
16387:        if "--stage-slave" in argv:
16389:        if "--variance-audit" in argv:
16391:        if "--emit-coupling" in argv:
16393:        if "--subspace-stability" in argv:
16396:    if len(argv) >= 1 and argv[0] == "--ag-criticality":
16400:    if len(argv) >= 1 and argv[0] == "--stream-mi":
16402:    if len(argv) >= 1 and argv[0] == "--capture-anchor":
16404:    if len(argv) >= 1 and argv[0] == "--gen-percept-schedule":
16406:    if len(argv) >= 1 and argv[0] == "--eval-historicity":
16408:    if len(argv) >= 1 and argv[0] == "--af-forward":
16410:    if len(argv) >= 1 and argv[0] == "--silence-content-te":
16412:    if len(argv) >= 1 and argv[0] == "--timing-channel":
16414:    if len(argv) >= 1 and argv[0] == "--cf-emit":
16416:    if len(argv) >= 1 and argv[0] == "--g-amp-screen":
16418:    if len(argv) >= 2 and argv[0] == "--cf-straddle":
16420:    if len(argv) >= 2 and argv[0] == "--dead-census":
16422:    if len(argv) >= 2 and argv[0] == "--lane-census":
16424:    if len(argv) >= 2 and argv[0] == "--gate-census":
16426:    if len(argv) >= 2 and argv[0] == "--gate-deaf":
16428:    if len(argv) >= 2 and argv[0] == "--audibility":
16430:    if len(argv) >= 2 and argv[0] == "--g-tension":
16432:    if len(argv) >= 2 and argv[0] == "--tension-emit":
16434:    if len(argv) >= 2 and argv[0] == "--psi-soma":
16436:    if len(argv) >= 2 and argv[0] == "--interact-mi":
16439:    if len(argv) >= 1 and argv[0] == "--selftest-rho-cells":
16454:    # --result-file <f>: write ALL output to <f> and keep fd 1 (stdout) silent. The hexa
16462:    # surrogateescape str), so any raw-continuation dump (--probe/--dump-hidden) prints a
16466:    if "--result-file" in argv:
16467:        i = argv.index("--result-file")
16483:    if "--rho-axon" in argv:
16484:        argv = [a for a in argv if a != "--rho-axon"]
16488:    #   --slot-off        force γ=0 => bit-exact base trunk (slot-ablation control)
16489:    #   --slot-shuffle N  permute the WRITE address with seed N (shuffle-bind control)
16490:    _slot_off = "--slot-off" in argv
16492:        argv = [a for a in argv if a != "--slot-off"]
16494:    if "--slot-shuffle" in argv:
16495:        i = argv.index("--slot-shuffle")
16501:    # --system-g1: RECOMBINATION-RELOCATION pipe (card H_9035). Strip the flag and
16502:    # route the remaining <ckpt> [--gen N] to the system-G1 harness.
16503:    if "--system-g1" in argv:
16504:        i = argv.index("--system-g1")
16507:    # --ground-probe <manifest.json>: the NBIND-G grounding instrument, whole and engine-native
16510:    if "--ground-probe" in argv:
16512:    # --valence-audit <manifest.json>: AUDIT-A — is the atom's polarity in the weights AT ALL
16516:    # --route-audit <manifest.json>: H_9355 LOCUS-CAUSAL — the ConvMoE router's per-surface expert
16520:    if "--route-audit" in argv:
16522:    if "--bind-locus" in argv:
16524:    # --decl-flip <c.txt.decl.json>: H_9800 EPHEMERAL-DECLARATION grounding — the H_9359
16527:    if "--decl-flip" in argv:
16529:    if "--twin-screen" in argv:
16531:    if "--twin-necessity" in argv:
16533:    if "--delta-pregate" in argv:
16535:    if "--delta-control" in argv:
16537:    if "--valence-audit" in argv:
16539:    # --device-parity: is this host's GPU forward the same measurement as its CPU forward? The probes
16541:    if "--device-parity" in argv:
16542:        return device_parity_run([a for a in argv if a != "--device-parity"])
16543:    # --dump-hidden <prompts.json>: read-only penultimate-hidden dump (ρ·weave / γ
16544:    # binding-lane probe H_9235). argv[0]=ckpt; dump_hidden_run reads --dump-hidden/--out.
16545:    if "--dump-hidden" in argv:
16547:    # H_9803 --fan-branch {live|assignment-shuffle|off}: the branch-latent ideation-fan arms.
16550:    if "--fan-branch" in argv:
16552:    # H_9805 --tension-rank-audit: effective rank of the write-side parse-disagreement field, with
16555:    if "--tension-rank-audit" in argv:
16557:    # H_9810 --bind-panel <panel.json>: held-out binding d_acc on the `anima corpus bindpanel`
16560:    if "--bind-panel" in argv:
16562:    # --store-addr-census <dump.npz> / --store-census-selftest: H_9719 emergent-address
16565:    if "--store-addr-census" in argv or "--store-census-selftest" in argv:
16567:    # --faction-phi-proxy <prompts.json>: the ARCHIVED faction Phi proxy recomputed on live
16570:    if "--faction-phi-proxy" in argv:
16572:    # --faction-block-structure <prompts.json>: does the trunk unit axis carry faction-like
16574:    if "--faction-block-structure" in argv:
16576:    # --faction-lesion <domains.json>: is the trained faction split FUNCTIONAL, or the same as
16578:    if "--faction-lesion" in argv:
16580:    # --faction-block-provenance: H_9674 블록이 진짜 모듈인가 architecture index layout(GN/RF)인가 (H_9676)
16581:    if "--faction-block-provenance" in argv:
16583:    # --interaction-lift <manifest.json>: read-only engine-native joint interaction-lift
16584:    # NLL surface (H_9255). argv[0]=ckpt; interaction_lift_run reads --interaction-lift/--out.
16585:    if "--earned" in argv:
16588:    if "--interaction-lift" in argv:
16590:    # --probe <spec.json>: matched-surface G1 probe (card H_6189). argv[0]=ckpt; probe_run
16591:    # reads --probe/--gen from the tail. Greedy raw-continuation dump for offline scoring.
16592:    if "--probe" in argv:
16594:    # --xbind <manifest.json>: held-out XBIND recombination (G1 reopen lane a · card H_9267).
16595:    # argv[0]=ckpt; xbind_run reads --xbind/--out/--arm from the tail. Engine-native greedy
16597:    if "--bridge-trace" in argv:
16599:    # --store-mix <store.json> [--store-lambda λ]: H_9392 BRIDGE-BOLT — bolt a runtime
16602:    if "--store-mix" in argv:
16604:    # --store <held.json> [--store-oracle] [--store-lambda λ]: H_9423 CLMS store-bridge lane — the
16606:    # content-addressed lookup). Distinct from --store-mix (H_9392 post-forward actuator).
16607:    if "--fan-bind" in argv:                       # H_9693 (R1) bind-Δ instrument
16609:    if "--store" in argv:
16611:    if "--xbind" in argv:
16613:    # --xfan <manifest.json>: held-out XFAN one-to-many fan (G6 reopen lane · card H_9271).
16616:    if "--xfan" in argv:
10:12-tick path) + `anima_byte_mode(ckpt, argv)` (the --byte continuation). ZERO hexa
16:the op-grip / stateful-refractory RESEARCH instrumentation (--opgrip*/--refractory, the
57:# H_9744 STORE-EPISODIC · the transducer's ENTIRE knowledge (--store-episodic on · G-W3(iii) audits
183:    """Value-taking flag: `--flag <v>` → v, else the `env` var, else `default` (all as str).
350:        if argv[a] != "--byte":
429:    if (anima_has_flag(_args, "--opgrip") or anima_has_flag(_args, "--opgrip-live")
430:            or anima_has_flag(_args, "--opgrip-r3") or anima_has_flag(_args, "--refractory")):
431:        _pln("anima-py chat: --opgrip*/--refractory research instrumentation is hexa-only")
434:        _pln("  use the hexa channel: `hx install anima` then `anima " + ckpt + " --opgrip[...]`")
538:    # H_9610 · --wm-leak parameterises the WM leak_rate λ (default 0.6 = byte-identical). λ IS the
543:    _wm_leak = anima_flag_value(argv if argv is not None else [], "--wm-leak", "ANIMA_WM_LEAK", "0.6")
547:        raise SystemExit("--wm-leak: float leak-rate λ in (0,1] (got %r)" % _wm_leak)
549:        raise SystemExit("--wm-leak: λ must be in (0,1] (got %r)" % _wm_leak_v)
1453:    # H_9404 · earned-refractory debt (only live when --refractory earned). 0.0 = nothing owed before
1495:    # H_9610 · frozen EMPTY alien WM buffer for the --g-reach wm-cover-alienwm C2 dissociation
1497:    # H_9627 reuses it as the frozen probe for --g-reach wm-dual-alien-{emit,silence}.
1557:    _workspace_mode = anima_flag_value(_cargv, "--workspace", "ANIMA_WORKSPACE", "auto")
1559:        raise SystemExit("--workspace: only 'auto' (default), 'off', 'structured', 'divergent', or 'grounded'")
1560:    _workspace_seed = anima_flag_value(_cargv, "--workspace-seed", "ANIMA_WORKSPACE_SEED", "")
1566:    _workspace_query = anima_flag_value(_cargv, "--workspace-query", "ANIMA_WORKSPACE_QUERY", "")
1568:        raise SystemExit("--workspace grounded requires --workspace-query subject|relation")
1570:        _cargv, "--workspace-evidence", "ANIMA_WORKSPACE_EVIDENCE", "")
1572:        _cargv, "--workspace-measurements", "ANIMA_WORKSPACE_MEASUREMENTS", "")
1574:        anima_has_flag(_cargv, "--workspace-require-evidence")
1575:        or anima_flag_value(_cargv, "--workspace-require-evidence",
1589:    _emit_temp = float(anima_flag_value(_cargv, "--emit-temp", "ANIMA_EMIT_TEMP", "0"))
1590:    _emit_topk = int(anima_flag_value(_cargv, "--emit-topk", "ANIMA_EMIT_TOPK", "256"))
1591:    _sample_seed = int(anima_flag_value(_cargv, "--sample-seed", "ANIMA_SAMPLE_SEED", "0"))
1595:    _score_perturb = float(anima_flag_value(_cargv, "--score-perturb", "ANIMA_SCORE_PERTURB", "0"))
1597:    # --imag-growth off skips ONLY the replay AdaptField grow (a_chat_sleep_imagination stays);
1598:    # --imag-salience-shuffle deterministically permutes the selected snapshots (salience destroyed,
1600:    _imag_growth = anima_flag_value(_cargv, "--imag-growth", "ANIMA_IMAG_GROWTH", "on")
1601:    _imag_shuffle = anima_flag_value(_cargv, "--imag-salience-shuffle", "ANIMA_IMAG_SHUFFLE", "0") == "1"
1608:    _g_arm = anima_flag_value(_cargv, "--g-arm", "ANIMA_G_ARM", "a0")
1614:    _ag_cont = anima_flag_value(_cargv, "--ag-cont", "ANIMA_AG_CONT", "0") == "1"
1619:    _dw = anima_flag_value(_cargv, "--dyn-w", "ANIMA_DYN_W", "")
1628:    _rl = anima_flag_value(_cargv, "--rate-limit-sec", "ANIMA_RATE_LIMIT_SEC", "")
1630:    # H_9404 · --emit-refractory earned: replace the rate term's SOURCE (wall clock) with the
1634:    # `--refractory` measurement harness above (:406). MUTUALLY EXCLUSIVE with --rate-limit-sec (both
1636:    _refractory = anima_flag_value(_cargv, "--emit-refractory", "ANIMA_EMIT_REFRACTORY", "")
1638:        raise SystemExit("--emit-refractory: only '' (off) or 'earned' (got %r)" % _refractory)
1640:        raise SystemExit("--emit-refractory earned and --rate-limit-sec are mutually exclusive "
1652:    _ag_feedback = float(anima_flag_value(_cargv, "--ag-feedback", "ANIMA_AG_FEEDBACK", "0.0") or "0.0")
1660:    # H_9404's --emit-refractory earned (which keeps should_emit(θ) and only swaps the rate SOURCE);
1663:    # The Ψ≈½ mechanism is H_9627's dual content ledger (see the conditional --g-reach default below);
1664:    # the old clock daemon is preserved byte-identically at `--emit-gate clock` / ANIMA_EMIT_GATE=clock
1666:    _emit_gate = anima_flag_value(_cargv, "--emit-gate", "ANIMA_EMIT_GATE", "refractory")
1673:    _g_shuffle = anima_flag_value(_cargv, "--g-shuffle", "ANIMA_G_SHUFFLE", "0") == "1"
1689:    #     refractory (0 on a 1-cell store), constants 0, single DOF. Composes with --g-shuffle unchanged.
1692:    # `--emit-gate clock` crash on the guard below (g_reach=wm-dual ∧ gate≠refractory → SystemExit). So
1694:    _g_reach = anima_flag_value(_cargv, "--g-reach", "ANIMA_G_REACH",
1699:        raise SystemExit("--g-reach: only 'd1' (default), 'affinity', 'cb-perr',"
1703:        raise SystemExit("--g-reach %s requires --emit-gate refractory (its only consumer)" % _g_reach)
1704:    # H_9738 · W_S composition TRANSPLANT seam (--ws-init <path> [--ws-init-mode scramble-keys] ·
1705:    # --ws-dump <path>). The static certificate (#3986) proved the imagined candidate's TEXT reaches
1714:    _ws_init = anima_flag_value(_cargv, "--ws-init", "ANIMA_WS_INIT", "")
1715:    _ws_init_mode = anima_flag_value(_cargv, "--ws-init-mode", "ANIMA_WS_INIT_MODE", "as-is")
1716:    _ws_dump = anima_flag_value(_cargv, "--ws-dump", "ANIMA_WS_DUMP", "")
1718:        raise SystemExit("--ws-init-mode: 'as-is' (default) or 'scramble-keys' (got %r)" % _ws_init_mode)
1720:        raise SystemExit("--ws-init/--ws-dump require --emit-gate refractory (W_S exists only there)")
1732:        _pln("anima-py chat: --ws-init %s (%s) · W_S seeded %d slot(s)" % (_ws_init, _ws_init_mode, len(_wk)))
1733:    # H_9712 · --rate-limit-sec / --emit-refractory earned feed ONLY the clock path (brain_emit's rate
1734:    # source). Under the new refractory default they would silently no-op, so require --emit-gate clock
1737:        raise SystemExit("--rate-limit-sec / --emit-refractory earned require --emit-gate clock "
1743:    # bare-safe: a bare `--record-silent-cand` (no value) means ON (chat-py-9 footgun — the
1746:    _rec_silent_cand = (anima_has_flag(_cargv, "--record-silent-cand")
1747:                        or anima_flag_value(_cargv, "--record-silent-cand", "ANIMA_RECORD_SILENT_CAND", "0") == "1")
1749:        raise SystemExit("--record-silent-cand requires --emit-gate refractory (its only producer)")
1751:    # W_S pressure-only? --wm-dual-read content re-enters the LAST withheld candidate's RAW text (not
1760:    # H_9794 AFFECT-FORWARDING (--af-clamp v,a) · do() clamp on the amygdala valence/arousal
1763:    _af_clamp_raw = anima_flag_value(_cargv, "--af-clamp", "ANIMA_AF_CLAMP", "")
1768:            raise SystemExit("--af-clamp: expects 'v,a' (two floats in [0,1]), got %r" % _af_clamp_raw)
1770:    # H_9794 AFFECT-FORWARDING (--af-impulse <f.jsonl>) · a PER-TICK af clamp schedule {tick,v,a}.
1771:    # The static --af-clamp cannot identify FORWARDING (af(t)≡af(t+1) collinear = a SHIFT verdict only);
1774:    _af_impulse_raw = anima_flag_value(_cargv, "--af-impulse", "ANIMA_AF_IMPULSE", "")
1786:    _wm_dual_read = anima_flag_value(_cargv, "--wm-dual-read", "ANIMA_WM_DUAL_READ", "off")
1788:        raise SystemExit("--wm-dual-read: only 'off' (default) or 'content' (got %r)" % _wm_dual_read)
1791:            raise SystemExit("--wm-dual-read content requires --emit-gate refractory")
1793:            raise SystemExit("--wm-dual-read content requires a wm-dual --g-reach (the W_S producer)")
1795:            raise SystemExit("--wm-dual-read content is mutually exclusive with an anima-study percept "
1798:    # H_9728 Θ−-yoked arm (#4068) · --yoke-mask <Θ+ trace> replays that trace's FINAL emit bit per tick,
1803:    _yoke_src = anima_flag_value(_cargv, "--yoke-mask", "ANIMA_YOKE_MASK", "")
1806:            raise SystemExit("--yoke-mask requires --emit-gate refractory (the forced_emit consumer)")
1818:    # H_9765 · --dual-margin-dither <eps> · exogenous do() on the emit-decision INPUT (the S−E comparison
1827:    _dither_eps = float(anima_flag_value(_cargv, "--dual-margin-dither", "ANIMA_DUAL_MARGIN_DITHER", "0") or "0")
1830:            raise SystemExit("--dual-margin-dither requires --emit-gate refractory (the dual gate consumer)")
1832:            raise SystemExit("--dual-margin-dither requires a wm-dual --g-reach (the S−E comparison it perturbs)")
1834:            raise SystemExit("--dual-margin-dither is mutually exclusive with --yoke-mask "
1840:    # In eval the manifest was hand-fed (cli/evaluate.py --store); here the SESSION's own percept
1844:    _store_episodic = anima_flag_value(_cargv, "--store-episodic", "ANIMA_STORE_EPISODIC", "off")
1846:        raise SystemExit("--store-episodic: only 'off' (default) or 'on' (got %r)" % _store_episodic)
1850:    _store_fuse = anima_flag_value(_cargv, "--store-fuse", "ANIMA_STORE_FUSE", "overwrite")
1852:        raise SystemExit("--store-fuse: only 'overwrite' (default), 'gated-add', 'odd' or 'pairodd' (got %r)" % _store_fuse)
1855:            raise SystemExit("--store-episodic on requires an anima-study percept source (the store is "
1863:            raise SystemExit("--store-episodic on is mutually exclusive with --emit-gate refractory: "
1874:            raise SystemExit("--store-episodic on needs a ckpt carrying a CLMS trailer (the co-trained "
1883:    # CONTENT is manipulated). --wm-dual-perm = byte-sort the carrier: feat8 is byte-multiset (perm-
1885:    # LOAD-BEARING control (order-bearing content vs pressure/histogram · Sol). --wm-dual-swap <donor>
1888:    _wm_dual_perm = (anima_has_flag(_cargv, "--wm-dual-perm")               # bare-safe (chat-py-9)
1889:                     or anima_flag_value(_cargv, "--wm-dual-perm", "ANIMA_WM_DUAL_PERM", "0") == "1")
1890:    _wm_dual_swap_path = anima_flag_value(_cargv, "--wm-dual-swap", "ANIMA_WM_DUAL_SWAP", "")
1891:    # H_9729 POSITIVE CONTROL producer · --wm-dual-oracle injects a FROZEN alternating A/B carrier
1893:    # (not just post-silence) — a KNOWN content on a KNOWN schedule. --silence-content-te --reach-
1896:    _wm_dual_oracle = (anima_has_flag(_cargv, "--wm-dual-oracle")           # bare-safe (chat-py-9)
1897:                       or anima_flag_value(_cargv, "--wm-dual-oracle", "ANIMA_WM_DUAL_ORACLE", "0") == "1")
1899:        raise SystemExit("--wm-dual-perm / --wm-dual-swap / --wm-dual-oracle require --wm-dual-read content")
1901:        raise SystemExit("--wm-dual-perm / --wm-dual-swap / --wm-dual-oracle are mutually exclusive arms")
1932:    _tension_route = anima_flag_value(_cargv, "--tension-route", "ANIMA_TENSION_ROUTE", "off")
1934:        raise SystemExit("--tension-route: only 'off' (default) or 'pc2' (got %r)" % _tension_route)
1936:        raise SystemExit("--tension-route pc2 requires --emit-gate refractory (its only consumer)")
1937:    _route_gain = float(anima_flag_value(_cargv, "--tension-route-gain", "ANIMA_TENSION_ROUTE_GAIN", "1.0"))
1943:    _pc2_mouth = anima_flag_value(_cargv, "--pc2-mouth", "ANIMA_PC2_MOUTH", "off")
1944:    # H_9664 ζ-LADDER — `--pc2-zeta z1,z2,…` re-decodes the SAME emit tick at each ζ, so the
1950:    _pc2_zeta_raw = anima_flag_value(_cargv, "--pc2-zeta", "ANIMA_PC2_ZETA", "")
1958:        raise SystemExit("--pc2-mouth: only 'off' (default), 'bias', 'rng' (got %r)" % _pc2_mouth)
1960:        raise SystemExit("--pc2-mouth requires --emit-gate refractory (its only consumer)")
1962:    # H_9755 REFIT-AXIS ζ-LADDER — `--z-loading a1,a2,…` turns the H_9664 scalar ladder into an
1966:    # first --refit-warmup ticks' 8-factor vectors (deterministic, sign-anchored to the frozen
1969:    _z_loading_raw = anima_flag_value(_cargv, "--z-loading", "ANIMA_Z_LOADING", "")
1977:                raise SystemExit("--z-loading: arm %r not in %s" % (_tok, _Z_ARMS))
1980:    _refit_warmup = int(anima_flag_value(_cargv, "--refit-warmup", "ANIMA_REFIT_WARMUP", "64"))
1983:            raise SystemExit("--z-loading requires --pc2-zeta (the dose ladder it modulates)")
1985:            raise SystemExit("--z-loading requires --emit-gate refractory")
1987:            raise SystemExit("--refit-warmup must be >= 4 (got %d)" % _refit_warmup)
1989:    # H_9756 PREFIX-SWAP positive control — `--zeta-prefix-swap "<alt mem text>"` adds one
1992:    # Independent of --z-loading/--pc2-zeta. Empty ⇒ off ⇒ byte-identical. Requires refractory gate.
1993:    _zeta_pswap = anima_flag_value(_cargv, "--zeta-prefix-swap", "ANIMA_ZETA_PREFIX_SWAP", "")
1995:        raise SystemExit("--zeta-prefix-swap requires --emit-gate refractory")
2001:        raise SystemExit("--zeta-prefix-swap requires ANIMA_EMIT_TEMP>0 (the sampled mouth path): a "
2111:    # --scn-freeze reproduces the DEAD scn_ctx constant (skip the per-tick step) = before-state.
2112:    # --anchor-tension-null forces the injected anchor tension_5ch to zero = zero-truth pedestal.
2113:    scn_freeze = anima_flag_value(_cargv, "--scn-freeze", "ANIMA_SCN_FREEZE", "0") == "1"
2114:    anchor_tension_null = anima_flag_value(_cargv, "--anchor-tension-null", "ANIMA_ANCHOR_TENSION_NULL", "0") == "1"
2119:    # reproducible (same --sample-seed ⇒ same trajectory) while letting the substrate actually
2134:    _swap_path = anima_flag_value(_cargv, "--swap-text", "ANIMA_SWAP_TEXT", "")
2163:    # H_9755 refit-axis ζ-ladder online state (None unless --z-loading given ⇒ byte-identical).
2165:    _zl_warm = []          # (f_raw 8-tuple, emit_bit) accumulated over the first --refit-warmup ticks
2252:        # H_9210 diagnosed this and fixed it — but only behind --opgrip-live, so production kept
2442:        # H_9794 --af-clamp v,a · do() clamp on the amygdala gauges (default OFF). Applied AFTER the
2500:        # coupled-vs-uncoupled consensus gap is a per-tick pedestal. --scn-freeze = before-state.
2762:        # surface. Consumed once. --wm-dual-perm byte-SORTS the carrier (feat8-preserving, order-
2763:        # destroying = load-bearing control) · --wm-dual-swap substitutes a donor's withheld cand.
2773:            # point mass ⇒ p≡1.0 structurally). --reach-oracle requires the reader to RECOVER the A/B
2804:        # consulted below when --refractory earned; the clock path is untouched otherwise.
2812:            # bind = recognition-before-memorisation, chat-py-5). Distinct from H_9404 --emit-refractory
2814:            # the production default now (owner-approved · Ψ≈½ via H_9627 dual-ledger · clock at --emit-gate clock).
2816:            # affinity-reach d2−d1 (the G-pole reach lever). --g-shuffle composes with either.
2827:                # recognition-before-memorisation, chat-py-5. NOTE (Fable §4): --g-shuffle is
2877:                    raise SystemExit("--yoke-mask: tick %d absent from mask %s (INVALID · mask must cover "
2959:        # ── H_9328 C2 CARRIER-SWAP (--swap-text <trace.jsonl>) · default OFF ────────────────
3201:                    # `anima-py evaluate <ckpt> --psi-soma <trace>` can reject a mismatched pair
3234:                # monitor-only). --ag-criticality reads these: ag_s=signed net, ag_fb_I=leaky-integral,
3242:                # + its arm (off/own/perm/donor · trace-only label). --silence-content-te reads X from
3260:                # production (g_recog_gate=None). Lets --g-readout-info / swing-census read whether
3283:                # evaluate --by-loading u-self-check. Absent unless --z-loading on ⇒ legacy unchanged.
3288:                # (pending_gap · a1 source), so --g-readout-info can re-screen either readout offline
3302:                # H_9794 --af-clamp / --af-impulse arm labels (trace-only · null when OFF · never a branch key)
3451:    # (--ws-init). Measurement-only side channel: nothing in this session read it back, so the
3452:    # emit path is byte-untouched (absent --ws-dump = production byte-identical).
3461:        _pln("anima-py chat: --ws-dump %s · W_S %d slot(s) persisted" % (_ws_dump, wm_withheld.n_slots))

codex
코드 표면에서 이미 `workspace`, `closure-ladder`, `store-bridge`, `ideation`, `tension-field`, `refractory/PC2`가 별도 실험 계보로 존재함을 확인했습니다. 새 설계는 이 이름들을 재조합하지 않고, 측정상 유일하게 살아남은 “content-addressed transport”만 원리로 가져오며 나머지는 독립 양성대조를 통과하기 전까지 철거 대상으로 두겠습니다.
exec
/bin/zsh -lc "rg --files core cli | rg 'workspace|closure|clms|ifan|tension|pure_field|model.py"'$'"' | sort
rg -n \"class .*Workspace|class .*Closure|def .*workspace|Proposal|Evidence|commit|diverg\" core cli/chat.py cli/evaluate.py | sed -n '1,420p'
sed -n '1,240p' core/clms.py
sed -n '930,1015p' core/engine_cli.py
sed -n '180,225p' core/pure_field.py
sed -n '2280,2340p' cli/chat.py" in /Users/mini/dancinlab/anima
 succeeded in 0ms:
core/clms.py
core/closure_ladder.py
core/cognitive_workspace.py
core/ifan.py
core/model.py
core/omega_clm_closure_probe.hexa
core/phi/memristor_gwt_workspace.hexa
core/phi/phi_adversarial_co_evolution_extension.md
core/pure_field.hexa
core/pure_field.py
core/tension_field.py
core/workspace_adapters.py
core/workspace_curriculum.py
core/workspace_mouth.py
core/workspace_regression.py
core/workspace_runtime.py
core/workspace_semantic.py
core/workspace_smoke.py
cli/chat.py:1555:    # the divergent typed path. Empty/atomic seeds reduce to OFF before any evidence is loaded or
cli/chat.py:1558:    if _workspace_mode not in ("auto", "off", "structured", "divergent", "grounded"):
cli/chat.py:1559:        raise SystemExit("--workspace: only 'auto' (default), 'off', 'structured', 'divergent', or 'grounded'")
cli/chat.py:3110:            from workspace_runtime import (grounded_query_step, spoken_divergence_step,
cli/chat.py:3116:                _workspace_step = (spoken_divergence_step if _workspace_effective_mode == "divergent"
cli/evaluate.py:934:def workspace_reach_only_run(argv):
cli/evaluate.py:988:def workspace_divergence_run(argv):
cli/evaluate.py:989:    """Ckpt-free content-divergence certificate with causal corruption controls."""
cli/evaluate.py:990:    from workspace_mouth import certify_divergence
cli/evaluate.py:993:    report = certify_divergence(seed)
cli/evaluate.py:1002:    print("=== anima workspace divergence certification ===")
cli/evaluate.py:1020:def workspace_divergence_realizer_run(argv):
cli/evaluate.py:1024:        print("ERROR: --workspace-divergence-realizer requires <ckpt>", file=sys.stderr)
cli/evaluate.py:1026:    from workspace_mouth import diverge_seed, divergence_preserves, realize_divergence
cli/evaluate.py:1032:    hypotheses = diverge_seed(seed)
cli/evaluate.py:1034:        print("ERROR: divergence seed is not compound", file=sys.stderr)
cli/evaluate.py:1036:    results = [realize_divergence(mouth, hypothesis, gen, 40, 0.7, 700 + index)
cli/evaluate.py:1039:    safe = all(divergence_preserves(hypothesis, result.text)
cli/evaluate.py:1041:    print("=== anima workspace divergence realizer ===")
cli/evaluate.py:1427:    print("  --workspace-divergence [--seed compound]: six content-distinct hypotheses with")
cli/evaluate.py:1429:    print("  --workspace-divergence-realizer <ckpt> [--seed compound]: measure model semantic")
cli/evaluate.py:2249:        print("  [parity] ❌ FAIL — the lane contaminates the base decode. First divergence: %r" % (worst,))
cli/evaluate.py:3083:                    atom — a causal LM has no reason to have committed anything at the atom.
cli/evaluate.py:3695:# −log(p_trunk) computed through an exp/log roundtrip) makes the guard diverge — so
cli/evaluate.py:4814:    """Jensen-Shannon divergence in BITS: JS = H((p+q)/2) - (H(p)+H(q))/2.
cli/evaluate.py:5057:    #   pre-flag behaviour (byte-identical), so no cemented number moves by this commit alone.
cli/evaluate.py:6074:    # values are garbage" (alignment) BEFORE any training spend is committed.
cli/evaluate.py:7649:    from the FACTUAL emit history, so the replay is exact only up to the first-divergence tick t*;
cli/evaluate.py:7729:        # first-divergence tick vs recorded emit
cli/evaluate.py:7746:    print("  replay: %d traces · %d ticks   (exact up to first-divergence t*; past t* DIRECTIONAL)" % (used, tot))
cli/evaluate.py:7751:    print("  refractory gate-open rate         : %.3f   · median first-divergence t*=%d" % (open_n / tot, tdiv_med))
cli/evaluate.py:8836:    SAME arithmetic the daemon uses, so any divergence here would be a new quantity again."""
cli/evaluate.py:9669:    "--workspace-divergence",                     # content-distinct falsifiable fan certificate
cli/evaluate.py:9670:    "--workspace-divergence-realizer",            # mounted mouth semantic preservation/fallback
cli/evaluate.py:9704:          which is called ONLY on the lm branch. Hence rng-divergence ⟹ that tick had ≥1
cli/evaluate.py:9705:          lm-step. 1 − (rng diverged / rng total) is a rigorous UPPER BOUND on the
cli/evaluate.py:9715:          steered diverges from base, rebuild that window from (seed ++ base[:i]) and ask
cli/evaluate.py:9834:    def _diverge(arm):
cli/evaluate.py:9852:    rnd, rnt, rfirst = _diverge("rng")
cli/evaluate.py:9853:    bnd, bnt, bfirst = _diverge("bias")
cli/evaluate.py:9856:    print("      ⇒ rng diverged %d/%d ⟹ that many emit ticks provably had ≥1 lm-step"
cli/evaluate.py:9861:        print("      first-divergence byte index: bias mean=%.2f med=%.1f min=%d · rng mean=%.2f med=%.1f min=%d"
cli/evaluate.py:9864:        print("      ⇒ NOTE: tick-divergence is SATURATED in BOTH arms (rng too) ⇒ zero")
cli/evaluate.py:9880:    print("  (2) surrogate π-dose = P(chosen byte ∈ own T=%d window) at first divergence" % _T)
cli/evaluate.py:9907:            print("      %-4s n=0 — no divergent tick to read (VOID)" % arm)
cli/evaluate.py:9917:        print("  ⇒ ⛔ VOID — an arm carried no divergent tick; the contrast is unreadable.")
cli/evaluate.py:9927:    print("      PC-a exposure: rng is a KNOWN-LIVE lm-branch perturbation — %s (%d/%d diverged)"
cli/evaluate.py:9966:    print("     · π-dose reads the FIRST divergent step ONLY: past it the two arms' contexts")
cli/evaluate.py:11091:    frozen null = H_9603 divergence-growth +0.007) — a fired pair, not a single-trace read; documented
cli/evaluate.py:11137:        # State vector = z-normalised [emit_drive, phi, ag_fb_I]; per-tick L2 distance d_t; divergence
cli/evaluate.py:11172:        print("      d_0=%.4f · d_end=%.4f · divergence-growth slope=%.5f /tick" % (d[0], d[-1], slope))
cli/evaluate.py:13774:    divergence means the isolation this whole line of work rests on never held: the run is
cli/evaluate.py:14546:                OWN first base↔bias divergence byte (control-must-match-mediating-covariate: the
cli/evaluate.py:14556:      oracle    READOUT positive control (dose ladder, k bytes at the same divergence locus):
cli/evaluate.py:14798:    print("  (3) READOUT positive control — directed dose ladder at the same divergence locus")
cli/evaluate.py:16338:    if len(argv) >= 1 and argv[0] == "--workspace-divergence":
cli/evaluate.py:16339:        return workspace_divergence_run(argv[1:])
cli/evaluate.py:16350:    if "--workspace-divergence-realizer" in argv:
cli/evaluate.py:16351:        return workspace_divergence_realizer_run(
cli/evaluate.py:16352:            [a for a in argv if a != "--workspace-divergence-realizer"])
core/substrate_hook.hexa:12://   M3 SI orthogonal   — SI(max-share) ⊥ CoV(moment-only) divergence (H_613)
core/substrate_hook.hexa:101:// SI (max-share, H_350) vs CoV (moment-only, H_613) 의 divergence — 두 지표가
core/substrate_hook.hexa:102:// 같은 정보를 측정하지 않음을 substrate 상에서 확인. divergent = 한쪽 high 다른쪽
core/substrate_hook.hexa:111:    let divergent = si_high != cov_high
core/substrate_hook.hexa:117:        "orthogonal_divergent": divergent,
core/substrate_hook.hexa:169:        "orthogonal_divergent": orth["orthogonal_divergent"],
core/cognitive_workspace.py:71:class CognitiveWorkspace:
core/workspace_adapters.py:103:def ingest_fact_anchors(workspace: CognitiveWorkspace, dir_path: str) -> list[Fact]:
core/workspace_adapters.py:151:def selected_grounded_texts(workspace: CognitiveWorkspace) -> list[str]:
core/hippo_lane.py:96:    """Deterministic sparse binary codes WITHOUT any float RNG divergence across
core/bytegpt_kvcache_batch_smoke.hexa:25:// ~1e-6 own-GEMM mirror -> ARGMAX-EQ (greedy identical, 0 argmax divergence on
core/bytegpt_kvcache_batch_smoke.hexa:359:        println("bytegpt_kvcache_batch_smoke: FAIL — batch KV path diverged from the "
core/brain.hexa:38:    if t == 3 { return "T3_commit" }
core/workspace_regression.py:7:    from .workspace_mouth import certify_divergence
core/workspace_regression.py:11:    from workspace_mouth import certify_divergence
core/workspace_regression.py:15:def run_workspace_regression() -> dict[str, object]:
core/workspace_regression.py:36:    en = certify_divergence("if copper conducts heat, then water drives turbines")
core/workspace_regression.py:37:    ko = certify_divergence("만약 비가 오지 않으면, 그러면 도로는 젖지 않는다")
core/workspace_regression.py:54:        "english_compound_divergent": auto_workspace_mode(
core/workspace_regression.py:55:            "if copper conducts heat, then water drives turbines") == "divergent",
core/workspace_regression.py:56:        "korean_compound_divergent": auto_workspace_mode(
core/workspace_regression.py:57:            "만약 비가 오지 않으면, 그러면 도로는 젖지 않는다") == "divergent",
core/workspace_regression.py:80:def format_workspace_regression(report: dict[str, object]) -> str:
core/engine_cli_smoke.hexa:23:import "core/rho_fan.hexa"   // H_1381 ρ·fan ideation wire-in (divergent coherent production · frozen bar = former G6; the g6_* detectors are the reused frozen-bar identifiers)
core/engine_cli_smoke.hexa:2537:    // case 208 : PRESENCE — match (pred=obs) → self (1.0); divergence → external (0.0).
core/engine_cli_smoke.hexa:2545:          + " · diverge→external " + to_string(agency_attribute(0.5, 1.5, 0.5)) + " — attribution judgment ⊥ ToM(other)/raw forward error")
core/engine_cli_smoke.hexa:3228:    let om_klC = _kl_div(om_vB, om_vA)                       // collision divergence (high)
core/engine_cli_smoke.hexa:3229:    let om_klBn = 0.0                                        // benign divergence (~0)
core/engine_cli_smoke.hexa:4130:        "git_commit job needing amend", "git_commit job needing signoff",
core/engine_cli_smoke.hexa:4138:        "file_write", "file_write", "git_commit", "git_commit",
core/engine_cli_smoke.hexa:4147:    if tool == "git_commit"  { return "-m" }
core/engine_cli_smoke.hexa:4173:        "open|write|close", "open|write|close", "stage|commit", "stage|commit",
core/brain.py:67:        return "T3_commit"
core/brain.py:380:    #   untouched). That is a BUILT-IN isolation certificate, not a claim: if it ever diverges,
core/workspace_runtime.py:131:def auto_workspace_mode(seed: str) -> str:
core/workspace_runtime.py:137:    return "divergent" if seed.strip() and split_compound(seed) is not None else "off"
core/workspace_runtime.py:140:def spoken_workspace_step(out_text: str, seed: str, evidence: Iterable[Fact] = (),
core/workspace_runtime.py:151:def spoken_divergence_step(out_text: str, seed: str, evidence: Iterable[Fact] = (),
core/workspace_runtime.py:153:    """Pure six-lens select/reject seam for the opt-in divergent chat mode."""
core/workspace_runtime.py:155:        from .workspace_mouth import select_divergence
core/workspace_runtime.py:157:        from workspace_mouth import select_divergence
core/workspace_runtime.py:158:    decision = select_divergence(seed or out_text, evidence, require_evidence)
core/anima_birth.hexa:12:// Birth a sibling from an INDEPENDENT key instead and they diverge (ARM2).
core/rho_fan.hexa:9:// (ρ·fan = divergent coherent production · reach axis, was G6 · frozen bar — identifiers below keep the g6_* name).
core/ifan.py:28:target-identification rather than by mode-commitment.
core/ifan.py:240:        parity — a divergence there makes every number from this lane unattributable.
core/phi_envelope_substrate.hexa:169://   abs_Δ (= Φmax−Φmin, scale-종속) 만 비단조 (II-最高) = apparent divergence 원천.
core/workspace_curriculum.py:36:def build_workspace_curriculum(paths, out_path, heldout_frac=0.2, seed=7):
core/mbnd.py:191:        MIRRORS mbnd_apply for 2-production parity; a divergence there makes every verdict from this
core/bytegpt_kvcache_smoke.hexa:11:// any divergence is a logits divergence. PASS = identical ids AND identical text;
core/bytegpt_kvcache_smoke.hexa:12:// on mismatch it reports the FIRST diverging step (no fudge — divergence is the result).
core/bytegpt_kvcache_smoke.hexa:192:    // first divergence point (if any)
core/bytegpt_kvcache_smoke.hexa:193:    let mut diverge = -1
core/bytegpt_kvcache_smoke.hexa:196:        if to_int(ref_ids[i]) != to_int(kv_ids[i]) { diverge = i; i = gen } else { i = i + 1 }
core/bytegpt_kvcache_smoke.hexa:220:    if diverge < 0 && gdiv < 0 {
core/bytegpt_kvcache_smoke.hexa:227:        println("bytegpt_kvcache_smoke: FAIL — first divergence at step " + to_string(diverge)
core/bytegpt_kvcache_smoke.hexa:228:            + " (REF id=" + to_string(to_int(ref_ids[diverge])) + " KV id="
core/bytegpt_kvcache_smoke.hexa:229:            + to_string(to_int(kv_ids[diverge])) + ").")
core/engine_cli.py:3216:class GlobalWorkspace:
core/tension_field.py:503:        2-production parity — a divergence there makes every number from this lane unattributable.
core/phi/anima_nested.hexa:15:// (regress converges), and we DETECT divergence when the drift-ratio
core/phi/anima_nested.hexa:50://   (divergence flagged at or before level 6).
core/workspace_mouth.py:120:class WorkspaceDecision:
core/workspace_mouth.py:229:class TypedWorkspaceMouth:
core/workspace_mouth.py:285:def diverge_seed(seed: str) -> tuple[DivergentHypothesis, ...]:
core/workspace_mouth.py:330:def divergence_preserves(hypothesis: DivergentHypothesis, text: str) -> bool:
core/workspace_mouth.py:338:def realize_divergence(mouth, hypothesis: DivergentHypothesis, gen: int, top_k: int,
core/workspace_mouth.py:344:    if divergence_preserves(hypothesis, candidate):
core/workspace_mouth.py:349:def select_divergence(seed: str, evidence: Iterable[Fact] = (),
core/workspace_mouth.py:352:    hypotheses = diverge_seed(seed)
core/workspace_mouth.py:370:            "insufficient grounded divergent evidence", hypotheses, None,
core/workspace_mouth.py:386:def certify_divergence(seed: str) -> dict[str, object]:
core/workspace_mouth.py:388:    hypotheses = diverge_seed(seed)
core/workspace_mouth.py:389:    live = [divergence_preserves(h, h.text) for h in hypotheses]
core/workspace_mouth.py:395:        missing.append(divergence_preserves(hypothesis, missing_text))
core/workspace_mouth.py:397:        shuffled.append(divergence_preserves(hypothesis, other.text))
core/phi/consciousness_gradient_phi.hexa:228:// Root cause: raw polynomial diverges at high phase; wrap to [-pi,pi] first.
core/phi/hive_state_sync.hexa:34:// T1 (initial divergence):
core/testdata/flores5_dev_devtest.txt:131:Today's announcement also extended the government's commitment made in March of this year to fund extra carriages.
core/testdata/flores5_dev_devtest.txt:181:Evidence thereafter indicated test papers were tampered with Hall, along with 34 other education officials, was indicted in 2013.
core/testdata/flores5_dev_devtest.txt:277:Stearns is investigating whether taxes are used to fund abortions through Planned Parenthood in his role as chairman of the Oversight and Investigations Subcommittee, which is under the umbrella of the House Energy and Commerce Committee.
core/testdata/flores5_dev_devtest.txt:309:As well as a former Olympic and World champion, Saito was the All Japan Judo Federation training committee chairman at the time of his death.
core/testdata/flores5_dev_devtest.txt:475:The temple of Artemis at Ephesus was destroyed on July 21, 356 BCE in an act of arson committed by Herostratus.
core/testdata/flores5_dev_devtest.txt:4989:On Monday, Sara Danius, permanent secretary of the Nobel Committee for Literature at the Swedish Academy, publicly announced during a radio program on Sveriges Radio in Sweden the committee, unable to reach Bob Dylan directly about winning the 2016 Nobel Prize in Literature, had abandoned its efforts to reach him.
core/testdata/flores5_dev_devtest.txt:5057:Prime Minister Stephen Harper has agreed to send the government's 'Clean Air Act' to an all-party committee for review, before its second reading, after Tuesday's 25 minute meeting with NDP leader Jack Layton at the PMO.
core/anima_birth_smoke.hexa:5:// siblings born from independent keys diverge. Deterministic (p7: equality).
core/anima_birth_smoke.hexa:9://   BB3 independent     — a sibling born from a DIFFERENT key diverges (≈chance)
core/anima_birth_smoke.hexa:67:    // BB3 — control: a sibling born from a DIFFERENT key diverges
core/decode.hexa:2666:// for the decode argmax gate (P0: 0 argmax divergence across every measured
core/decode.hexa:3453:// `out_path` as it finishes (commit-early: a reboot/kill keeps fragments already written;
core/phi/split_brain_phi.hexa:37:// ─── Operational commitments ────────────────────────────────────
core/phi/split_brain_phi.hexa:79:// T4 (chimeric reports diverge under split, converge under intact):
core/phi/split_brain_phi.hexa:592://   axis, reports diverge.
core/phi/split_brain_phi.hexa:786:    // T4 chimeric reports: split diverges, intact converges
core/phi/split_brain_phi.hexa:803:    // Split must diverge — bounded above
core/phi/split_brain_phi.hexa:811:    // T5 alien-hand: under split, motor act diverges from verbal goal;
core/phi/split_brain_phi.hexa:847:    // Split: motor act divergent from goal
core/phi/split_brain_phi.hexa:875:    if t4 { println("T4 PASS — chimeric reports diverge under split, converge under intact") } else { println("T4 FAIL") }
core/phi/split_brain_phi.hexa:878:    if t5 { println("T5 PASS — alien-hand simulable under split (motor diverges from verbal intent)") } else { println("T5 FAIL") }
core/decode.py:293:    # commit to W only once ALL uploads succeed. If any xp.asarray raises
core/decode.py:316:    W.update(s)                    # commit only if every upload above succeeded
core/decode.py:532:    KNOWN-BUGGY for x far from 1 (diverges); reproduced verbatim for parity."""
core/decode.py:2229:#     keeps it — a 1-byte divergence. This never occurs on real text ckpts (a byte
core/shared_seed.py:28:    # would diverge → hexa-side parity-fix candidate (shared_seed.hexa split " " → split()).
core/phi/addiction_phi.hexa:660:    println("  [T1] divergence growth=" + str(gap_growth))
core/pure_field.py:28:whereas the 8-term Taylor cos diverges at ~6e-12. So `sin == math.sin` etc.
core/phi/creativity_phi.hexa:1:// creativity_phi.hexa — P130 Creativity Φ (divergent thinking, originality × usefulness)
core/phi/creativity_phi.hexa:4://   "Creativity Φ — 창의성 의식 측정 (Guilford divergent + Mednick RAT + Boden + Amabile)"
core/phi/creativity_phi.hexa:5://   done_criteria: "divergent fluency + remote association + originality×usefulness +
core/phi/creativity_phi.hexa:156:let CRE_W_FLUENCY     = 0.25      // divergent spread (Guilford)
core/phi/creativity_phi.hexa:502:// Candidate generators — open (divergent) vs closed (convergent).
core/phi/creativity_phi.hexa:507:// Open prompt: divergent thinking; candidates spread across distinct
core/phi/creativity_phi.hexa:800:// We model the DMN break as a PRNG re-seeding with a divergent offset,
core/phi/creativity_phi.hexa:827:    // prompt (divergent thinking) produces candidates spread across
core/phi/creativity_phi.hexa:1024:    println("[creativity_phi] P130 — Creativity Φ (divergent + originality×usefulness)")
core/phi/creativity_phi.hexa:1032:    if t1 { println("T1 PASS  divergent fluency — open > closed (Guilford)") } else { println("T1 FAIL") }
core/phi/creativity_phi.hexa:1059:        println("[creativity_phi] 5/5 PASS — P130 DONE (creativity Φ divergent originality×usefulness verified)")
core/phi/emotion_contagion.hexa:22:// T1 (initial divergence):
core/phi/emotion_contagion.hexa:231:    if t1 { println("T1 PASS  initial states divergent (distance > 1.0)") } else { println("T1 FAIL") }
core/phi/edge_of_chaos.hexa:87://   lambda > 0  -> chaotic (exponential divergence of nearby orbits)
core/phi/edge_of_chaos.hexa:137:    // T3: Chaotic regime (r=3.9) -> lambda > 0.1 (positive = divergent)
core/engine_cli.hexa:1198:// runs diverge); with an exhausted pool it falls back to the deterministic PRNG (so
core/engine_cli.hexa:1283:// distribution diverges from the incoming one:
core/engine_cli.hexa:3428://     valence/satiation. There is no SEPARATE agent whose belief can diverge.
core/engine_cli.hexa:3736:// collective_coherence — B3 no-collapse gauge: 1 - mean per-cell L1 divergence between
core/engine_cli.hexa:12569://   HIGH(경직→percept 에 commit) + metacog_gain IMPAIRED.
core/phi/quantum_collapse_sample.hexa:415:// so higher phi strictly scales the noise amplitude -> more divergence
core/kosmos_io.py:24:divergence). The values MATCH the hexa exactly (both use this LCG), and DIFFER from the
core/phi/narrative_identity_phi.hexa:46://     (P5) Hemisphere fission yields two ~equal but diverging Φ streams
core/phi/narrative_identity_phi.hexa:62://       mutually diverging over time
core/phi/narrative_identity_phi.hexa:474:// Hemisphere fission: from step k, branch into two diverging descendants.
core/phi/narrative_identity_phi.hexa:509:            // Post-split: diverging walk, branch-specific seed stream
core/phi/narrative_identity_phi.hexa:696:    // (within-branch MI is high), but MI between the two diverging
core/phi/narrative_identity_phi.hexa:710:    // Measure post-split cross-branch divergence: MI between corresponding
core/phi/narrative_identity_phi.hexa:745:    // AND branches diverge (cross < within_l). We do not require sharp
core/phi/narrative_identity_phi.hexa:775:    if t5 { println("T5 PASS — hemisphere fission (within-branch coherent, cross-branch diverges)") } else { println("T5 FAIL") }
core/phi/social_tom_phi.hexa:57://   (marble at basket); B's belief diverges from W. A's model_of_B
core/phi/social_tom_phi.hexa:384://   - B observed earlier state (marble at basket), so B.belief diverges
core/phi/social_tom_phi.hexa:414:// they diverge.
core/phi/mind_upload_phi.hexa:22:// from the original. Over τ they diverge (independent micro-noise
core/phi/mind_upload_phi.hexa:30://   (4) divergence(τ)      — mean pairwise L1 distance grows in τ
core/phi/mind_upload_phi.hexa:39:// H2 (divergence dynamics):
core/phi/mind_upload_phi.hexa:45://     and decreases monotonically with divergence.
core/phi/mind_upload_phi.hexa:71://   T2: copies diverge with τ (mean pairwise L1 strictly grows)
core/phi/mind_upload_phi.hexa:72://   T3: ensemble Φ decays with divergence
core/phi/mind_upload_phi.hexa:92:let MU_N_STEPS      = 12       // divergence time steps (< 32)
core/phi/mind_upload_phi.hexa:294:// Drift dynamics — independent copies diverge over τ
core/phi/mind_upload_phi.hexa:297:// copies diverge from one another despite identical t=0 states.
core/phi/mind_upload_phi.hexa:372:// divergence.
core/phi/mind_upload_phi.hexa:417:fn mu_divergence(original: array, c1: array, c2: array, c3: array) -> float {
core/phi/mind_upload_phi.hexa:476:    // T2: copies diverge with τ — mean pairwise L1 distance strictly grows.
core/phi/mind_upload_phi.hexa:477:    // At τ=0 all copies identical → divergence = 0.
core/phi/mind_upload_phi.hexa:478:    // At τ=N divergence > 0; and monotone (here: final > early τ=1).
core/phi/mind_upload_phi.hexa:480:    // At τ=0 — all clones, divergence should be zero.
core/phi/mind_upload_phi.hexa:484:    let div_0 = mu_divergence(orig, c1_0, c2_0, c3_0)
core/phi/mind_upload_phi.hexa:489:    let div_1 = mu_divergence(orig, c1_1, c2_1, c3_1)
core/phi/mind_upload_phi.hexa:493:    let div_n = mu_divergence(orig, c1_n, c2_n, c3_n)
core/phi/mind_upload_phi.hexa:494:    println("  [T2] divergence: tau=0: " + str(div_0) + " tau=1: " + str(div_1) + " tau=" + str(MU_N_STEPS) + ": " + str(div_n))
core/phi/mind_upload_phi.hexa:502:    // T3: ensemble Φ decays with divergence — Φ_ens at τ=1 > at τ=N.
core/phi/mind_upload_phi.hexa:594:    if t2 { println("T2 PASS  copies diverge with tau") } else { println("T2 FAIL") }
core/phi/mind_upload_phi.hexa:597:    if t3 { println("T3 PASS  ensemble Phi decays with divergence") } else { println("T3 FAIL") }
core/phi/infant_consciousness_phi.hexa:844:            println("    FAIL: stage " + str(k) + " diverged: run1=" + str(phis_run1[k]) + " run2=" + str(phis_run2[k]) + " diff=" + str(diff))
core/phi/dissociation_phi.hexa:16:// Operational commitments (Putnam 1989; Ross 1997):
core/phi/archetype_field.hexa:879:    // fully reproducible. Any float divergence reveals hidden state.
core/phi/language_acquisition_phi.hexa:47://   neural commitment (NLNC). Post-NLNC, non-native contrasts require
core/phi/language_acquisition_phi.hexa:169://   We model CRITICAL by dual-exposure simulations with divergent
core/phi/synaesthetic_binding_phi.hexa:397:        // 4. Noise + mild decay toward zero to prevent divergence.
core/phi/synaesthetic_binding_phi.hexa:549:// We model this as CONFLICT COST: the mean squared divergence
core/phi/synaesthetic_binding_phi.hexa:551:// color pattern. Congruent trials have low divergence (patterns
core/phi/synaesthetic_binding_phi.hexa:552:// align). Incongruent trials have high divergence (patterns oppose).
core/phi/synaesthetic_binding_phi.hexa:561:fn sb_stroop_divergence(grapheme_id: int, congruent: int) -> float {
core/phi/synaesthetic_binding_phi.hexa:599:        let cost_c = sb_stroop_divergence(gid, 1)
core/phi/synaesthetic_binding_phi.hexa:603:        let cost_i = sb_stroop_divergence(gid, 0)
core/phi/synaesthetic_binding_phi.hexa:616:        total = total + sb_stroop_divergence(gid, congruent)
core/phi/phi_adversarial.hexa:852:// rolling hash diverges from the expected chain, zero out Φ.
core/phi/pride_facet_phi.hexa:76:// share a CORE postural expansion signature but diverge on micro-
core/phi/pride_facet_phi.hexa:118:// the per-step dimensionwise L1 divergence.
core/phi/pride_facet_phi.hexa:142://   ch 7  tension_channel [t]  — per-step L1 divergence summary
core/phi/shame_phi.hexa:15:// the TOSCA paradigm and showed it predicts divergent action tendencies:
core/phi/shame_phi.hexa:916:    //   The divergent action tendencies are the behavioural signature
core/phi/curiosity_phi.hexa:358:// KL divergence in nats: Σ p · ln(p / q). Both p, q must be strictly
core/phi/psychosis_phi.hexa:422:        // Evidence channel: sample a stage-1 percept under balanced conditions.
core/phi/metaphysics_engine.hexa:35://   (a) Φ divergence across positions (how different are the Φ values?)
core/phi/metaphysics_engine.hexa:46://   T2  divergence — the four models do NOT return identical Φ
core/phi/metaphysics_engine.hexa:450:    let divergent = (d1 > 0.005 || d2 > 0.005 || d3 > 0.005 || d4 > 0.005)
core/phi/metaphysics_engine.hexa:451:    return divergent
core/phi/metaphysics_engine.hexa:556:    if t2 { println("T2 PASS  4 positions yield divergent Φ (distinct predictions)") } else { println("T2 FAIL") }
core/phi/cosmic_phi.hexa:47://     in particular the slope is finite (no divergence, no zero).
core/phi/neural_phi_bridge.hexa:718:// are scrambled across channels so Φ_LFP diverges from the other two
core/phi/anima_will.hexa:7://   DESIRE ──(intent commit ≥ θ_int)──▶ INTENT
core/phi/schizophrenia_self_phi.hexa:57:// ─── Operational commitments ────────────────────────────────────
core/phi/pride_phi.hexa:68:// they diverge on stability:
core/phi/phi_of_phi.hexa:454:// divergent growth — mirrors the shared-weights choice in anima_nested.
core/phi/corpus_quality_engine.hexa:25://   M6 KL_TO_UNIFORM      — KL divergence of byte distribution to uniform
core/phi/corpus_quality_engine.hexa:389:// M6: KL divergence to uniform (higher = more skewed; lower = richer)
core/phi/self_deception_phi.hexa:32://   belief-revision direction tracks the commitment direction.
core/phi/self_deception_phi.hexa:71://   Evidence e[t] ∈ [-1,1]     observed signed evidence for proposition
core/phi/self_deception_phi.hexa:88://   delta_spread scales with commitment strength and dissonance.
core/phi/self_deception_phi.hexa:505:// Evidence stream generator
core/phi/self_deception_phi.hexa:533:// Evidence with upward signed drift — biases ground truth toward 1.
core/phi/self_deception_phi.hexa:719:fn sd_dissonance_reduce(belief_a: float, belief_b: float, commitment: float) -> array {
core/phi/self_deception_phi.hexa:725:    let delta = SD_SPREAD_BASE * commitment * close
core/phi/self_deception_phi.hexa:759:        let commit = 0.5 + 0.5 * sd_unit(s)
core/phi/self_deception_phi.hexa:760:        let r = sd_dissonance_reduce(ba, bb, commit)
"""core/clms.py — H_9423 CLMS store-bridge trailer lane, CORE-owned SSOT.

The ρ·weave recombination wall (was G1) is the ABSENCE of an operator<->declaration-store runtime
lookup bridge (H_9359): the FACT can live in a store and the OPERATOR in the text, yet a frozen conv
byte-LM has no port to bind them (bolt-on died 3-port, H_9392). v2 DIRECTIONAL-proved that a
CO-TRAINED bridge learns the lookup (V2_6 held-out macro 0.987/0.992). CLMS ports that co-trained
bridge onto the parent conv trunk as a trailer lane: at the answer position it forms a query from the
trunk penultimate, looks up an 8-slot content-addressed store (keys = a FROZEN per-byte embedding of
the entity name → generalizes to held-out entities), reads the polarity value, and fuses it with the
operator through a GELU-MLP — the nonlinearity the parent's linear 1x1-conv readout cannot supply on
its own (v2's XOR wall). The answer-position logits row is OVERWRITTEN with λ·store_logits (store_only
gate), so the trunk logit can never receive answer-position gradient = ② shortcut-cut is structural.

DISJOINT (a_substrate_disjoint): the store content is RUNTIME-injected (train: block store manifest;
eval: `--store` manifest via set_clms_store), never serialized into the .clm — only the learned bridge
weights {W_q, val, W_h, b_h, W_out, λ} + the frozen key_emb table live in the trailer. Absent trailer
OR un-injected store <=> byte-identical to today's .clm (loaders passthrough on short/absent read;
forward passthrough when _CLMS_STORE is None). This is the H_9392 boundary made literal: "does the
fusion parameter live inside the .clm and enter the forward pass" — yes (co-trained), vs --store-mix
(post-forward posterior arithmetic actuator).

CORE-owned, ONE file (mirrors core/slw.py, core/clml.py): store_apply + find_qpos (torch-free numpy
inference mirror, byte-parity target for core/decode.hexa) · pack_clms/read_clms ("CLMS" trailer codec)
· CLMSModule (torch training module, DIRECTIONAL, defined only when torch importable so inference stays
torch-free). Store is injected via set_clms_store (mirrors slw.set_slw_controls) — trailer present +
store None = passthrough (the C0-f "trailer有 store無 = byte-identical" seal).
"""

from __future__ import annotations

import struct
import numpy as np

# ── "CLMS" trailer magic (mirrors the CLMB/SLW/CLML trailer convention) ─────────
CLMS_MAGIC = bytes([67, 76, 77, 83])   # "CLMS"


def _softmax(z):
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def _sigmoid(x):
    """Overflow-safe logistic (H_9696 gate). The naive 1/(1+exp(-x)) warns and loses the branch for
    |x|>~700; a saturated gate is a LEGITIMATE state here (gate→0 is how the lane stays silent where
    it has nothing to say), so it must saturate cleanly rather than RuntimeWarning."""
    if x >= 0.0:
        return 1.0 / (1.0 + np.exp(-x))
    e = np.exp(x)
    return e / (1.0 + e)


def _gelu(x):
    # tanh approximation — MUST match CLMSModule's F.gelu(approximate="tanh") for 2-production parity
    # (constants byte-identical to core/clml._gelu).
    return 0.5 * x * (1.0 + np.tanh(0.7978845608028654 * (x + 0.044715 * x**3)))


# --------------------------------------------------------------------------- #
# (a) numpy inference mirror — torch-free, byte-parity target for core/decode.hexa
# --------------------------------------------------------------------------- #
def find_qpos(tok):
    """Answer positions in a decode window. Returns the list of t where tok[t-2:t+1] == "=> "
    (bytes 61,62,32): logits[t] predicts the FIRST answer byte, so t is both the query-formation
    position and the row CLMS overwrites (a causal LM aligns logits[t] with tok[t+1]). Pure function
    of the window bytes (no side channel) — the same scanner the trainer reuses. Usually 0–1 hits for
    a T=24 window over ≤23-byte lines; t == T-1 (last row) is valid (its argmax is the first answer
    byte at generation)."""
    t_list = []
    for t in range(2, len(tok)):
        if int(tok[t]) == 32 and int(tok[t - 1]) == 62 and int(tok[t - 2]) == 61:
            t_list.append(t)
    return t_list


def _entity_key(key_emb, entity):
    """Content address for an entity name = mean of the frozen per-byte embedding rows. Generalizes to
    held-out entities (a new key built from seen bytes). key_emb is (256, d_k)."""
    ids = np.frombuffer(entity.encode("ascii"), dtype=np.uint8)
    return key_emb[ids].mean(axis=0)


def store_apply(logits, yn, clms, store, qpos, oracle=False, lam_override=None, audit=None,
                query="qpos", fuse="overwrite", fresh_yn=None):
    """CLMS store-bridge lane: OVERWRITE the answer-position logits row with λ·store_logits.

    query/fuse (H_9695 R3 · the read→mouth wiring the G6 angles need · defaults reproduce the
    H_9423 lane byte-for-byte):
      query="qpos"        — fire only where find_qpos hits the literal "=> " trigram (H_9423).
      query="every-token" — fire at EVERY row. The literal trigram cannot exist in free ideation,
                            so a G6-facing lane must be able to query without a marker. Note the
                            marker is not merely absent in free generation: teaching the mouth to
                            emit "=> " itself would be kill #1's scaffold moved inside the mouth,
                            which is why the legal form is a learned gate (H_9696), not a literal.
      fuse="overwrite"    — out[t] = λ·s (H_9423 store_only gate: the structural shortcut-cut that
                            makes the storebind readout attributable to the lane alone).
      fuse="gated-add"    — out[t] = logits[t] + λ·s. Overwriting EVERY row would delete the trunk
                            and destroy fluency (dist<5 kills the ρ·fan panel before bind can be
                            read); additive keeps the lane a perturbation whose CONTENT-dependence
                            is what the scramble controls test.

    logits : (T, V) float — readout(+CLML) logits. The caller's array is NOT mutated (internal copy).
    yn     : (T, d) float — pre-slot trunk penultimate (= _fwd_trunk output = yn_trunk, the SAME tap
             CLML reads; NOT the SLW-modified penultimate).
    clms   : dict from read_clms (key_emb, W_q, val, W_h, b_h, W_out, lam, n_slot, d_k, d_s, r).
    store  : {"entities": [str]*n_slot, "pols": [int in {0,1}]*n_slot, "target_slot": int|None}.
             target_slot is used only when oracle=True.
    qpos   : list of int from find_qpos(tok).
    oracle : True => bypass the softmax lookup, a = one_hot(target_slot) (C0-e positive control:
             hands the lookup for free, so ORACLE<0.90 = the value/MLP/λ/serialization plumbing is
             dead, independent of whether addressing can be learned — read no negative before it passes).
    lam_override : None = file λ · 0.0 = λ0 control (C2, byte-identical passthrough) · 1.0 = store_only.

    Passthrough (returns logits unchanged): clms None · lane_type==0 · store None · λ==0 · and
    (query="qpos" only) qpos empty. query="every-token" does NOT require qpos — free ideation
    contains no "=> " by construction, so gating the marker-free lane on the marker would silence
    it exactly where it is meant to fire (H_9695).
    Op order is IDENTICAL to CLMSModule.forward (2-production parity)."""
    if clms is None or int(clms.get("lane_type", 0)) == 0 or store is None:
        return logits
    if query == "qpos" and not qpos:
        return logits
    lam = float(clms["lam"]) if lam_override is None else float(lam_override)
    if lam == 0.0:
        return logits
    dt = logits.dtype
    n_slot = int(clms["n_slot"])
    key_emb = clms["key_emb"]
    ents = store["entities"]
    pols = np.asarray(store["pols"], dtype=np.int64)
    K = np.stack([_entity_key(key_emb, ents[i]) for i in range(n_slot)])   # (n_slot, d_k)
    lane_type = int(clms.get("lane_type", 1))
    if lane_type == 4:
        # H_9696 CLMS-FAN: free ideation carries no polarity, so the value cannot be val[pols]. The
        # slot's value is projected out of the slot's OWN key — the lane retrieves "which word I am
        # holding is relevant here" and re-injects its identity = the mouth-internal binding operator
        # H_1603 names as the shared missing part of both walls.
        V_slots = K @ clms["W_v"]                                          # (n_slot, d_s)
    else:
        V_slots = clms["val"][pols]                                        # (n_slot, d_s)
    scale = 1.0 / np.sqrt(float(clms["d_k"]))
    out = logits.copy()
    if query == "every-token":
        rows = range(len(yn))          # H_9695: marker-free — the lane queries at every position
    elif query == "qpos":
        rows = qpos
    else:
        raise ValueError("store_apply: query must be 'qpos' or 'every-token' (got %r)" % query)
    if fuse not in ("overwrite", "gated-add", "odd", "pairodd"):
        raise ValueError("store_apply: fuse must be 'overwrite', 'gated-add', 'odd' or 'pairodd' (got %r)" % fuse)
    for t in rows:
        h = yn[t]                                                          # (d,)
        if lane_type == 5:                                                 # H_9720-ⓐ fresh query lane
            hf = (fresh_yn[t] if fresh_yn is not None else h)              # early-layer tap (decode supplies it)
            q = _gelu(hf @ clms["W_fresh"]) @ clms["W_q_fresh"]           # (d_k,) disjoint address query
        else:
            q = h @ clms["W_q"]                                           # (d_k,) [row-vector conv, CLML-form]
        if oracle:
            a = np.zeros(n_slot, dtype=q.dtype)
            a[int(store["target_slot"])] = 1.0                            # softmax bypassed (address free)
        else:
            a = _softmax(q @ K.T * scale)                                # (n_slot,) content-address lookup
        if audit is not None:                                            # H_9672 addr-audit (None=byte-identical)
            ts = store.get("target_slot")
            # H_9802 store-telemetry: `a_max`/`a_ent` are TARGET-FREE, so they stay meaningful on
            # natural text where no target_slot exists (a_target degenerates to -1 there). They
            # split the two failure modes the H_9802 pre-check must tell apart BEFORE any training
            # spend: a_max ≈ 1/n_slot (uniform) ⟹ natural text never ADDRESSES the store
            # (recruitment problem); a_max ≫ 1/n_slot with wrong values ⟹ it addresses but the
            # values are garbage (alignment problem). a_ent is the entropy of the address
            # distribution normalised by log(n_slot), so 1.0 = uniform and 0.0 = a hard one-slot
            # hit — both read against the DERIVED uniform baseline, never an assumed chance.
            # MONITOR-ONLY (a_train_inline_gauge): never enters any loss or any frozen bar.
            _p = a / (a.sum() + 1e-12)
            _ent = float(-(_p * np.log(_p + 1e-12)).sum() / (np.log(n_slot) + 1e-12))
            audit.append({"argmax": int(np.argmax(a)),
                          "a_target": float(a[int(ts)]) if ts is not None else -1.0,
                          "target": int(ts) if ts is not None else -1,
                          "a_max": float(np.max(a)),
                          "a_ent": _ent})
        if lane_type == 3:                                                # RV-3 majority-null centering (H_9710)
            a = a - (1.0 / n_slot)                                        # v≡0 at uniform a → shortcut basin gone
        v = a @ V_slots                                                   # (d_s,) = Σ (aᵢ−c)·val[polᵢ]
        if lane_type in (2, 3, 4, 5):
            g = h @ clms["W_g"]                                           # (d_g,) op-gate bottleneck (H_9423)
            z = _gelu(np.concatenate([v, g]) @ clms["W_h"] + clms["b_h"]) # (r,) [v; g] fusion (v un-diluted)
        else:                                                             # lane_type 1 legacy: [v; h] fusion
            z = _gelu(np.concatenate([v, h]) @ clms["W_h"] + clms["b_h"]) # (r,) — S1/S2 artifacts, no silent recast
        s = z @ clms["W_out"]                                             # (V,)
        if fuse == "odd":                                                 # H_9760 odd-symmetrized fusion:
            v_neg = -v                                                    #   s_odd = ½(s(v,g) − s(−v,g)) cancels the
            if lane_type in (2, 3, 4, 5):                                 #   even (op-gate g-path) prior that emits a
                z_neg = _gelu(np.concatenate([v_neg, g]) @ clms["W_h"] + clms["b_h"])  # polarity-invariant constant on
            else:                                                         #   op=0 (H_9744 flip-coh gap). For lane_type 3
                z_neg = _gelu(np.concatenate([v_neg, h]) @ clms["W_h"] + clms["b_h"])  # (Σ(aᵢ−1/n)=0 ⟹ v_flip≡−v) this
            s = 0.5 * (s - z_neg @ clms["W_out"])                         #   makes fixed-address flip-coherence = 1.
        elif fuse == "pairodd":                                           # H_9775 Π-equivariant pair-odd: full-row odd
            v_neg = -v                                                    #   (H_9760) killed the g/b argmax because it
            if lane_type in (2, 3, 4, 5):                                 #   subtracted the even level that made g/b the
                z_neg = _gelu(np.concatenate([v_neg, g]) @ clms["W_h"] + clms["b_h"])  # top logits. Here out[c∉{g,b}]=
            else:                                                         #   ½(s⁺+s⁻) PRESERVES that even level (argmax
                z_neg = _gelu(np.concatenate([v_neg, h]) @ clms["W_h"] + clms["b_h"])  # stays g/b = readable) while
            s_neg = z_neg @ clms["W_out"]                                 #   swapping ONLY the answer pair makes the g/b
            G_BYTE, B_BYTE = 103, 98                                      #   margin exactly odd in store polarity (Π =
            sp_g, sp_b = float(s[G_BYTE]), float(s[B_BYTE])              #   103↔98 = the task's answer alphabet, not
            sn_g, sn_b = float(s_neg[G_BYTE]), float(s_neg[B_BYTE])      #   per-query gold). readability = measured DV.
            s = 0.5 * (s + s_neg)                                         #   out[c] = ½(s⁺[c]+s⁻[c]) for c∉{g,b}
            s[G_BYTE] = 0.5 * (sp_g + sn_b)                               #   out[g] = ½(s⁺[g]+s⁻[b])
            s[B_BYTE] = 0.5 * (sp_b + sn_g)                               #   out[b] = ½(s⁺[b]+s⁻[g])  ⟹ margin odd
        if lane_type == 4:
            # H_9696 learned query gate — the legal replacement for the "=> " literal. A literal
            # taught to the mouth is kill #1's scaffold relocated; a data-dependent nonlinear gate is
            # precisely the class kill #7 left unmeasured. gate→0 lets the lane stay silent where it
            # has nothing to say, which is what keeps free-gen fluency (dist>=5) alive.
            s = _sigmoid(float(h @ clms["W_gate"])) * s
        if fuse in ("overwrite", "odd", "pairodd"):                       # odd/pairodd use overwrite semantics (H_9760/H_9775)
            out[t] = (lam * s).astype(dt)                                 # ★ store_only gate (H_9423)
        else:                                                             # gated-add (H_9695/H_9696)
            out[t] = (logits[t] + lam * s).astype(dt)                     # lane = perturbation, trunk kept
    return out


# --------------------------------------------------------------------------- #
# (b) "CLMS" trailer codec — write (serialize) + read (loaders) · LE f32
#   header: CLMS magic · lane_type u8 · n_slot u32 · d_k u32 · d_s u32 · r u32 · key_seed u32
#   arrays (row-major): key_emb[256·d_k] W_q[d·d_k] val[2·d_s] W_h[(d_s+d)·r] b_h[r] W_out[r·V] lam[1]
#   (d, V come from the model — read_clms(buf, off, d, V) — as in read_clml. key_emb's first axis 256
#    is the fixed byte alphabet, V-independent. key_seed is PROVENANCE ONLY — the reader never
#    regenerates the table, it reads the stored bytes: a seed-regenerated table is the quietest
#    instrument-death vector, train-pod vs eval-host generation drift degrades the lookup silently
#    and a single-host determinism gate can't catch it. 64KB is 0.02% of a 303M .clm — store it.)
# --------------------------------------------------------------------------- #
_ARR_ORDER = ("key_emb", "W_q", "val", "W_h", "b_h", "W_out", "lam")               # lane_type 1 (legacy)
_ARR_ORDER_V2 = ("key_emb", "W_q", "W_g", "val", "W_h", "b_h", "W_out", "lam")     # lane_type 2 (H_9423 W_g)
# lane_type 3 = 2 + RV-3 majority-null centering (H_9710) — SAME arrays/header as V2, no new tensors.
# lane_type 4 (H_9696 CLMS-FAN): W_v projects the VALUE out of the slot's own key (free ideation has
# no polarity, so val[pols] has nothing to index) and W_gate is the learned query gate that replaces
# the "=> " literal. NOTE the number: lane_type 3 was taken by H_9710 (merged first) — same ID-race
# class as hypotheses-jsonl-3, one axis over. Pre-emptor keeps the number; this lane yields to 4.
    i = 0
    while i < n:
        pi = p[i]
        qi = q[i]
        if pi < 0.000000001:
            pi = 0.000000001
        if qi < 0.000000001:
            qi = 0.000000001
        s = s + pi * _ln(pi / qi)
        i = i + 1
    return s


class OsmoticStore:
    __slots__ = ("field", "vals")

    def __init__(self, field, vals):
        self.field = field
        self.vals = vals


def osmotic_store_new(key0, val0, max_cells):
    return OsmoticStore(vadapt_field_new(key0, max_cells), [val0])


def osmotic_should_split(st, key, val, mode, beta, cap_c, kl_override):
    """engine_cli.hexa:876."""
    SPLIT_THRESH = 0.30
    win = _vnearest_idx(st.field.protos, key)
    d = _l2(st.field.protos[win], key)
    if mode == 0:
        return d > SPLIT_THRESH
    b = beta
    if mode == 2:
        b = 0.0
    if kl_override >= 0.0:
        dkl = kl_override
    else:
        dkl = _kl_div(val, st.vals[win])
    return (d + b * dkl) > cap_c


def osmotic_learn(st, key, val, cfg, mode, beta, cap_c, kl_override):
    """engine_cli.hexa:895."""
    LR = 0.20
    af = st.field
    want_split = osmotic_should_split(st, key, val, mode, beta, cap_c, kl_override)
    if want_split and af.n_cells < af.max_cells:
        grown = engine_mitosis_tick(af.n_cells, cfg)
        if grown > af.n_cells:
            nf = VAdaptField(af.protos + [list(key)], grown, af.max_cells, af.dim)
            return OsmoticStore(nf, st.vals + [list(val)])
    win = _vnearest_idx(af.protos, key)
    p2 = list(af.protos)
    row = list(p2[win])
    i = 0
    while i < af.dim:
        row[i] = row[i] + LR * (key[i] - row[i])
        i = i + 1
    p2[win] = row
    v2 = list(st.vals)
    v2[win] = list(val)
    nf2 = VAdaptField(p2, af.n_cells, af.max_cells, af.dim)
    return OsmoticStore(nf2, v2)


def osmotic_retains(st, key, val, recall_thr):
    """engine_cli.hexa:928."""
    n = st.field.n_cells
    i = 0
    while i < n:
        if _l2(st.field.protos[i], key) <= recall_thr and _l2(st.vals[i], val) <= 0.20:
            return 1.0
        i = i + 1
    return 0.0


def osmotic_cells(st):
    return st.field.n_cells


# ════════════════════════════════════════════════════════════════════════
# ImmuneMemoryGrow (§GrowImmune, H_1288) — grow-under-pressure + LRU evict
# engine_cli.hexa:1212-1353
# ════════════════════════════════════════════════════════════════════════

        self.narrative_coherence = narrative_coherence
        self.narrative_len = narrative_len


def pure_field_new():
    return PureField(
        osc_new(TAU_FAST), osc_new(TAU_MEDIUM), osc_new(TAU_SLOW),
        0.0, 0.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        PHASE_DORMANT, 0, 0.0, 0)


# ════════════════════════════════════════════════════════════════════════
# Core step: advance field by one tick (zero external input)
# ════════════════════════════════════════════════════════════════════════

def pure_field_step(pf, drive=0.0):
    """pure_field.hexa:196 pure_field_step.

    H_9607: `drive` = the daemon's leaky-integral of the signed A⇄G tension, fed back into
    the oscillator amplitude target (osc_tick). drive == 0.0 → byte-identical to production.
    """
    # 1. Advance oscillators (H_9607 · A⇄G feedback into the amplitude target)
    f = osc_tick(pf.fast, drive)
    m = osc_tick(pf.medium, drive)
    s = osc_tick(pf.slow, drive)

    # 2. Nonlinear mixing
    v_f = osc_value(f)
    v_m = osc_value(m)
    v_s = osc_value(s)

    mix_fm = v_f * v_m
    mix_ms = v_m * v_s
    mix_fs = v_f * v_s

    # 3. Build field tensor [FIELD_DIM=6]
    field = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    field[0] = v_f
    field[1] = mix_fm
    field[2] = v_s
    field[3] = mix_fs
    field[4] = mix_ms
    field[5] = v_f + v_m + v_s

    # 4. Phi = variance * energy
    mean = (field[0] + field[1] + field[2]
        ag_a_drive = emit_drive
        if _g_arm == "a1":
            # pending_gap is the IMMUNE STORE top-2 gap on the LAST utterance (1-tick lag, like
            # pending_rel) — set at :2061 (immune_memory_recall_gap_text), which UNCONDITIONALLY
            # overwrites the afield gap computed at :2051 (that afield line is dead code · H_9399
            # G-SOURCE-ID). None before the daemon has spoken → no reverse signal yet = 0.
            g_recog = _afs_clip01(pending_gap if pending_gap is not None else 0.0)
            ag_g_drive = 0.0 - g_recog
        elif _g_arm == "a4":
            # H_9413 L5 · SOURCE-SWAP: read the immune store's recall MARGIN (pending_rel · set at
            # :2173 immune_memory_recall_margin_text, same 1-tick-lag/before-bind order as pending_gap)
            # instead of the top-2 gap. H_9401 found margin is the ONLY G readout that clears θ (p90
            # 0.69≥0.40) and H_9412 found the gap is drift-not-recognition — margin is the daemon's
            # own COMPUTED-BUT-DISCARDED signal (no synthetic injection · no sign tuning · engine fn).
            # None before first utterance → 0. Both readouts land in the trace row for the counterfactual.
            g_recog = _afs_clip01(pending_rel if pending_rel is not None else 0.0)
            ag_g_drive = 0.0 - g_recog
        elif _g_arm == "a3":
            # explicit int seed (Python 3.14 rejects tuple seeds); deterministic per (seed, tick).
            _g_seed = (_sample_seed * 2654435761 + tick * 40503 + 0x9357) & 0x7FFFFFFF
            g_recog = random.Random(_g_seed).random()
            ag_g_drive = 0.0 - g_recog
        else:  # a0 — current production wiring (the tautology arm)
            g_recog = 1.0 - emit_drive
            ag_g_drive = 0.0 - (1.0 - emit_drive)
        ag_conflict = conflict_scalar(ag_a_drive, ag_g_drive)
        # H_9607 · update the leaky-integral of the SIGNED A⇄G net tension AFTER this tick's drives are
        # known — consumed at the TOP of next tick (:~1730). s = ag_a_drive + ag_g_drive is 0 exactly
        # when A's push and G's push cancel (a0: s = emit_drive − (1−emit_drive) = 2·emit_drive − 1),
        # so the integral null s→0 pins the steady state at emit_drive=½ regardless of κ (emergent, not
        # dialed). κ=0 leaves ag_fb_I evolving but unused (ag_drive gated to 0.0 above) → byte-identical.
        ag_s_signed = ag_a_drive + ag_g_drive
        ag_fb_I = (1.0 - _AG_FB_RHO) * ag_fb_I + ag_s_signed
        ag_budget = conflict_recruited_depth(ag_conflict, 4, 6)
        ag_pop = anima_tr_pop_conflicted(_afs_clip01(0.5 + 0.5 * ag_conflict))
        ag_settle = tension_resolve_depth(ag_pop, tr_full, 0.3, 0.5, ag_budget, 2, 0.06, tr_cfgON)
        ag_settle_depth = ag_settle[0]
        if _ag_cont:
            # H_9376 · continuous pass-through = the UPPER-BOUND arm of the mid-link capacity
            # (I(conflict;agloop_ctx|stage) = H(conflict|stage); no continuization can exceed it). The
            # settle machinery above still ran (its trace fields are preserved); only the report
            # to score is continuized. tension-agnostic: reads ag_conflict's VALUE only, applied
            # identically to every g-arm, a fixed monotone map — arm selectivity is substrate-earned.
            agloop_ctx = _afs_clip01(ag_conflict)
        else:
            agloop_ctx = (0.0 if ag_settle_depth < 0.0
                          else _afs_clip01(ag_settle_depth / (float(ag_budget) + 0.000001)))

        # (3) GLOBAL WORKSPACE
        gws = gws_new(4, True, 0.55)
        gi = 0
        while gi < len(lanes):
            gws = gws_add(gws, lanes[gi])
            gi = gi + 1
        gws_w = gws_winner(gws)
        if gws_w >= 0:
            gws_ignited_any = True

        # (4) REALITY MONITOR
        reality = reality_call(emit_drive, 0.55)
        if reality >= 1.0:

exec
/bin/zsh -lc "git status --short --branch
git log -1 --oneline --decorate
sed -n '1,430p' core/cognitive_workspace.py
sed -n '1,450p' core/workspace_mouth.py
sed -n '1,240p' core/closure_ladder.py" in /Users/mini/dancinlab/anima
 succeeded in 3821ms:
2026-07-22 13:27:23.157 xcodebuild[80484:10025473]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:23.395 xcodebuild[80484:10025472] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-ibPYHwvH' (errno=Operation not permitted)
2026-07-22 13:27:23.833 xcodebuild[80486:10025490]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:23.954 xcodebuild[80486:10025489] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
## main...origin/main [ahead 2, behind 165]
 M ARCHITECTURE.json
?? ING.jsonl
?? lab/v3/
?? lab/v4/
?? lab/v5/
?? stream_mi.json
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-x73eJjLj' (errno=Operation not permitted)
2026-07-22 13:27:25.078 xcodebuild[80492:10025542]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:25.199 xcodebuild[80492:10025541] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-UCjO3Uot' (errno=Operation not permitted)
2026-07-22 13:27:25.532 xcodebuild[80494:10025552]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:25.653 xcodebuild[80494:10025551] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
7ff936d1a (HEAD -> main) feat(workspace): auto-route compound chat inputs
"""Typed cognitive workspace for explicit composition and falsification.

This module intentionally has no model, decoder, numpy, or torch dependency.  It
is the seam between a future extractor/retriever and the existing CLM mouth:
the mouth receives only a selected claim, never opaque intermediate activations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Sequence


@dataclass(frozen=True, order=True)
class Fact:
    subject: str
    relation: str
    object: str
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.subject or not self.relation or not self.object:
            raise ValueError("a fact requires non-empty subject, relation, and object")

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.subject, self.relation, self.object)


@dataclass(frozen=True)
class CompositionRule:
    """Compose ``A -left-> B`` and ``B -right-> C`` into ``A -out-> C``."""

    name: str
    left_relation: str
    right_relation: str
    output_relation: str

    def apply(self, left: Fact, right: Fact) -> Fact | None:
        if left.relation != self.left_relation:
            return None
        if right.relation != self.right_relation or left.object != right.subject:
            return None
        sources = tuple(dict.fromkeys((*left.provenance, *right.provenance, self.name)))
        return Fact(left.subject, self.output_relation, right.object, sources)


class ClaimStatus(str, Enum):
    PROPOSED = "proposed"
    SUPPORTED = "supported"
    FALSIFIED = "falsified"
    UNGROUNDED = "ungrounded"
    SELECTED = "selected"


@dataclass
class Claim:
    proposition: Fact
    falsifiers: tuple[Fact, ...]
    grounds: tuple[Fact, ...] = ()
    status: ClaimStatus = ClaimStatus.PROPOSED
    evidence: tuple[Fact, ...] = ()

    def __post_init__(self) -> None:
        if not self.falsifiers:
            raise ValueError("a claim requires at least one explicit falsifier")


@dataclass
class CognitiveWorkspace:
    """Small deterministic state machine shared by the G1 and G6 paths."""

    facts: dict[tuple[str, str, str], Fact] = field(default_factory=dict)
    derivations: list[Fact] = field(default_factory=list)
    claims: list[Claim] = field(default_factory=list)
    selected: Claim | None = None

    def add_facts(self, facts: Iterable[Fact]) -> None:
        for fact in facts:
            self.facts[fact.key] = fact

    def compose(self, rule: CompositionRule) -> list[Fact]:
        """Run a two-operand join; unary echo cannot create a derivation."""

        snapshot = tuple(self.facts.values())
        produced: list[Fact] = []
        for left in snapshot:
            for right in snapshot:
                result = rule.apply(left, right)
                if result is None or result.key in self.facts:
                    continue
                self.facts[result.key] = result
                self.derivations.append(result)
                produced.append(result)
        return produced

    def propose(self, proposition: Fact, falsifiers: Sequence[Fact],
                grounds: Sequence[Fact] = ()) -> Claim:
        claim = Claim(proposition, tuple(falsifiers), tuple(grounds))
        self.claims.append(claim)
        return claim

    def test(self, claim: Claim) -> ClaimStatus:
        """Ground a claim and test its preregistered counterexamples."""

        hits = tuple(self.facts[f.key] for f in claim.falsifiers if f.key in self.facts)
        grounding = tuple(self.facts[f.key] for f in claim.grounds if f.key in self.facts)
        claim.evidence = hits + grounding
        if hits:
            claim.status = ClaimStatus.FALSIFIED
        elif claim.grounds and not grounding:
            claim.status = ClaimStatus.UNGROUNDED
        elif claim.proposition.key in self.facts:
            claim.status = ClaimStatus.SUPPORTED
        else:
            claim.status = ClaimStatus.UNGROUNDED
        return claim.status

    def select(self, claims: Sequence[Claim] | None = None) -> Claim:
        pool = tuple(self.claims if claims is None else claims)
        viable = [claim for claim in pool if self.test(claim) is ClaimStatus.SUPPORTED]
        if not viable:
            raise RuntimeError("no grounded, non-falsified claim is selectable")
        self.selected = viable[0]
        self.selected.status = ClaimStatus.SELECTED
        return self.selected

    def render_for_mouth(self) -> str:
        """Serialize only a selected typed result; generation is outside this core."""

        if self.selected is None or self.selected.status is not ClaimStatus.SELECTED:
            raise RuntimeError("mouth is gated until a claim is selected")
        fact = self.selected.proposition
        return f"{fact.subject} {fact.relation} {fact.object}"
"""Typed-workspace wrapper for a model mouth.

Atomic prompts remain byte-identical to the wrapped mouth. Compound prompts are
parsed into two clauses, composed in the typed workspace, and realized as an
explicit measurable hypothesis. No benchmark concept table is embedded here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from typing import Iterable

try:
    from .cognitive_workspace import CognitiveWorkspace, CompositionRule, Fact
except ImportError:
    from cognitive_workspace import CognitiveWorkspace, CompositionRule, Fact


_STRUCTURAL = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "if",
    "in", "is", "it", "of", "on", "or", "still", "the", "then", "to", "when",
    "만약", "이면", "라면", "그러면", "그리고", "또는", "은", "는", "이", "가", "을", "를",
}


def _words(text: str) -> list[str]:
    return re.findall(r"[^\W_]+", text.lower(), flags=re.UNICODE)


def split_compound(seed: str) -> tuple[str, ...] | None:
    clean = seed.strip().rstrip(":").strip()
    match = re.match(r"^if\s+(.+?),\s*then\s+(.+)$", clean, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    ko = re.match(
        r"^만약\s+(.+?)(?:이면|라면|으면|면)\s*[,，]?\s*(?:그러면\s+)?(.+)$", clean
    )
    if ko:
        return ko.group(1).strip(), ko.group(2).strip()
    clauses = [part.strip() for part in re.split(r"\.\s+", clean) if part.strip()]
    if len(clauses) >= 2:
        return tuple(clauses)
    return None


def _operand(clause: str) -> str:
    content = list(dict.fromkeys(w for w in _words(clause) if w not in _STRUCTURAL))
    if not content:
        raise ValueError("compound clause has no content operand")
    # A compact symbolic handle prevents the realizer boilerplate from dominating
    # pairwise diversity. Selection is lexical and domain-independent.
    # Korean morphology often expresses negation/condition in a middle token (오지 않다).
    # Dropping it flips the proposition, so preserve the full short clause.
    if any(any(ord(ch) > 127 for ch in word) for word in content):
        return " ".join(content)
    return " ".join(content if len(content) <= 2 else (content[0], content[-1]))


def _realizer_axes(left: str, right: str) -> tuple[str, str]:
    comparators = ("predicts", "correlates", "causes", "increases", "decreases", "depends")
    measures = ("score", "rate", "frequency", "strength", "level", "ratio")
    raw = (left + "|" + right).encode("utf-8", "surrogateescape")
    h = 2166136261
    for byte in raw:
        h = ((h ^ byte) * 16777619) & 0xFFFFFFFF
    return comparators[h % len(comparators)], measures[(h // len(comparators)) % len(measures)]


def _claim_id(seed: str, candidate: int) -> str:
    raw = (seed.strip() + "|" + str(candidate)).encode("utf-8", "surrogateescape")
    h = 2166136261
    for byte in raw:
        h = ((h ^ byte) * 16777619) & 0xFFFFFFFF
    return "workspace-claim-%08x-%d" % (h, candidate)


def claim_ids(seed: str) -> tuple[str, str, str]:
    """Stable public IDs used by typed evidence anchors."""
    return _claim_id(seed, 0), _claim_id(seed, 1), _claim_id(seed, 2)


@dataclass(frozen=True)
class HypothesisSpec:
    claim_id: str
    measure: str
    control: str
    falsified_when: str


@dataclass(frozen=True)
class DivergentHypothesis:
    text: str
    spec: HypothesisSpec
    required_terms: tuple[str, ...]
    lens: str
    surface_lens: str = ""
    comparator: str = ""


@dataclass(frozen=True)
class DivergenceRealization:
    text: str
    valid: bool
    realized_by: str


@dataclass(frozen=True)
class DivergenceDecision:
    text: str
    candidates: tuple[DivergentHypothesis, ...]
    selected_claim_id: str | None
    rejected_claim_ids: tuple[str, ...]
    supported_claim_ids: tuple[str, ...]
    abstained: bool
    selection_reason: str


@dataclass(frozen=True)
class WorkspaceDecision:
    text: str
    candidate_claim_ids: tuple[str, ...]
    candidate_specs: tuple[HypothesisSpec, ...]
    selected_claim_id: str | None
    rejected_claim_ids: tuple[str, ...]
    abstained: bool
    required_terms: tuple[str, ...]
    realized_by: str = "workspace"
    realizer_valid: bool = True


def decide_seed(seed: str, evidence: Iterable[Fact] = (),
                require_evidence: bool = False) -> WorkspaceDecision | None:
    clauses = split_compound(seed)
    if clauses is None:
        return None
    operands = [_operand(clause) for clause in clauses]
    workspace = CognitiveWorkspace()
    accumulated = operands[0]
    provenance = ("seed:0",)
    proposition = None
    for index, operand in enumerate(operands[1:], start=1):
        bridge = "workspace:interaction:" + str(index)
        left = Fact(accumulated, "enters", bridge, provenance)
        right = Fact(bridge, "combines", operand, ("seed:" + str(index),))
        rule = CompositionRule(
            "clause-interaction:" + str(index), "enters", "combines", "interacts_with"
        )
        workspace.add_facts([left, right])
        produced = workspace.compose(rule)
        if len(produced) != 1:
            raise RuntimeError("typed compound did not produce exactly one derivation per rung")
        proposition = produced[0]
        accumulated = proposition.subject + " " + proposition.object
        provenance = proposition.provenance
    if proposition is None:
        raise RuntimeError("compound requires at least two operands")
    ids = claim_ids(seed)
    comparator, measure = _realizer_axes(proposition.subject, proposition.object)
    specs = tuple(
        HypothesisSpec(
            claim_id=claim_id,
            measure=measure,
            control="each_operand_alone",
            falsified_when=("interaction_not_above_control" if index == 0 else
                            "interaction_above_control" if index == 1 else
                            "measurement_resolves_direction"),
        )
        for index, claim_id in enumerate(ids)
    )
    primary = proposition
    alternative = Fact(
        proposition.subject,
        "does_not_interact_with",
        proposition.object,
        proposition.provenance + ("counter-hypothesis",),
    )
    uncertain = Fact(
        proposition.subject,
        "interaction_direction_unresolved",
        proposition.object,
        proposition.provenance + ("uncertainty-hypothesis",),
    )
    workspace.add_facts([alternative, uncertain])
    evidence = tuple(evidence)
    workspace.add_facts(evidence)
    # The two candidates are an exhaustive positive/non-positive split. A measured
    # contradiction of one side grounds the other side unless it is independently
    # contradicted as well.
    if Fact(ids[0], "has_verdict", "contradicted").key in workspace.facts:
        workspace.add_facts([Fact(ids[1], "has_verdict", "supported", ("binary-complement",))])
    if Fact(ids[1], "has_verdict", "contradicted").key in workspace.facts:
        workspace.add_facts([Fact(ids[0], "has_verdict", "supported", ("binary-complement",))])
    claims = []
    for index, candidate in enumerate((primary, alternative, uncertain)):
        falsifier = Fact(ids[index], "has_verdict", "contradicted")
        grounds = [Fact(ids[index], "has_verdict", "supported")] if require_evidence else []
        claims.append(workspace.propose(candidate, [falsifier], grounds))
    try:
        selected = workspace.select(claims)
    except RuntimeError:
        return WorkspaceDecision(
            text="insufficient grounded evidence",
            candidate_claim_ids=ids,
            candidate_specs=specs,
            selected_claim_id=None,
            rejected_claim_ids=ids,
            abstained=True,
            required_terms=tuple(_words(proposition.subject + " " + proposition.object)),
        )
    selected_index = claims.index(selected)
    if selected_index == 0:
        text = proposition.subject + " " + comparator + " " + proposition.object + " " + measure
    elif selected_index == 1:
        text = proposition.subject + " decreases " + proposition.object + " " + measure
    else:
        text = proposition.subject + " relationship with " + proposition.object + " remains uncertain " + measure
    rejected = tuple(ids[i] for i, claim in enumerate(claims) if claim.status.value == "falsified")
    required = tuple(dict.fromkeys(_words(proposition.subject + " " + proposition.object)))
    return WorkspaceDecision(text, ids, specs, ids[selected_index], rejected, False, required)


def compose_seed(seed: str, evidence: Iterable[Fact] = (),
                 require_evidence: bool = False) -> str | None:
    decision = decide_seed(seed, evidence, require_evidence)
    return None if decision is None else decision.text


class TypedWorkspaceMouth:
    """Drop-in ``ideate`` wrapper; atomic calls delegate without alteration."""

    def __init__(self, mouth, evidence: Iterable[Fact] = (), require_evidence: bool = False,
                 realizer: str = "structured"):
        if realizer not in ("structured", "model"):
            raise ValueError("realizer must be structured or model")
        self.mouth = mouth
        self.evidence = tuple(evidence)
        self.require_evidence = require_evidence
        self.realizer = realizer
        self.decisions: list[WorkspaceDecision] = []

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        decision = decide_seed(seed, self.evidence, self.require_evidence)
        if decision is None:
            return self.mouth.ideate(seed, gen, top_k, temp, seed_rng)
        if self.realizer == "model" and not decision.abstained:
            prompt = ("Structured hypothesis: " + decision.text
                      + ". Restate this hypothesis without changing its operands: ")
            candidate = self.mouth.ideate(prompt, gen, top_k, temp, seed_rng)
            if realization_preserves(decision, candidate):
                decision = replace(decision, text=candidate, realized_by="model", realizer_valid=True)
            else:
                decision = replace(decision, realized_by="workspace_fallback", realizer_valid=False)
        self.decisions.append(decision)
        return decision.text


def realization_preserves(decision: WorkspaceDecision, text: str) -> bool:
    """Fail closed unless the mouth preserves operands and falsifiable structure."""
    words = set(_words(text))
    required = set(decision.required_terms)
    comparator = {"predicts", "correlates", "causes", "increases", "decreases", "depends"}
    measurable = {"score", "rate", "frequency", "strength", "level", "ratio"}
    expected_relation = set(_words(decision.text)) & comparator
    return (required.issubset(words) and bool(words & measurable)
            and bool(expected_relation) and expected_relation.issubset(words))


def realization_training_rows(seeds: Iterable[str]) -> tuple[dict[str, object], ...]:
    """Supervision rows for the mouth; targets are verified structured renderings."""
    rows = []
    for seed in seeds:
        decision = decide_seed(seed)
        if decision is None or decision.abstained:
            continue
        rows.append({
            "prompt": "Structured hypothesis: " + decision.text,
            "target": decision.text,
            "required_terms": list(decision.required_terms),
            "candidate_specs": [spec.__dict__ for spec in decision.candidate_specs],
        })
    return tuple(rows)


def diverge_seed(seed: str) -> tuple[DivergentHypothesis, ...]:
    """Produce six content-distinct, preregistered tests without new entities."""
    clauses = split_compound(seed)
    if clauses is None:
        return ()
    operands = tuple(_operand(clause) for clause in clauses)
    left, right = operands[0], operands[-1]
    required = tuple(dict.fromkeys(_words(left + " " + right)))
    # Each lens changes the empirical question, not merely wording. Every noun comes
    # from the input; generic experimental dimensions cannot fabricate a domain fact.
    korean = any(any(ord(ch) > 127 for ch in operand) for operand in operands)
    if korean:
        rows = (
            ("positive", "증가시킨다", "비율", "양의", "직접 상승 단조", "interaction_not_above_each_operand_control"),
            ("negative", "감소시킨다", "수준", "음의", "직접 하강 반대", "interaction_not_below_each_operand_control"),
            ("threshold", "예측한다", "임계값", "문턱", "경계 초과 비선형", "effect_present_below_preregistered_threshold"),
            ("delay", "유발한다", "지속시간", "지연", "시간 이후 후행", "effect_absent_after_preregistered_delay"),
            ("context", "의존한다", "비율", "맥락", "조건 변화 상호작용", "same_effect_across_preregistered_contexts"),
            ("null", "상관한다", "빈도", "영가설", "동등 구간 무차이", "difference_outside_equivalence_interval"),
        )
    else:
        rows = (
            ("positive", "increases", "rate", "positive", "", "interaction_not_above_each_operand_control"),
            ("negative", "decreases", "level", "negative", "", "interaction_not_below_each_operand_control"),
            ("threshold", "predicts", "threshold", "threshold", "", "effect_present_below_preregistered_threshold"),
            ("delay", "causes", "duration", "delay", "", "effect_absent_after_preregistered_delay"),
            ("context", "depends", "ratio", "context", "", "same_effect_across_preregistered_contexts"),
            ("null", "correlates", "frequency", "null", "", "difference_outside_equivalence_interval"),
        )
    out = []
    for index, (lens, comparator, measure, surface_lens, detail, falsified) in enumerate(rows):
        claim_id = _claim_id(seed + "|fan|" + lens, index)
        text = " ".join(part for part in
                        (left, comparator, right, measure, surface_lens, detail) if part)
        out.append(DivergentHypothesis(
            text=text,
            spec=HypothesisSpec(claim_id, measure, "each_operand_alone", falsified),
            required_terms=required,
            lens=lens,
            surface_lens=surface_lens,
            comparator=comparator,
        ))
    return tuple(out)


def divergence_preserves(hypothesis: DivergentHypothesis, text: str) -> bool:
    words = set(_words(text))
    return (set(hypothesis.required_terms).issubset(words)
            and hypothesis.spec.measure in words
            and (hypothesis.surface_lens or hypothesis.lens) in words
            and hypothesis.comparator in words)


def realize_divergence(mouth, hypothesis: DivergentHypothesis, gen: int, top_k: int,
                       temp: float, seed_rng: int) -> DivergenceRealization:
    """Let a mouth restate one lens, failing closed on any semantic loss."""
    prompt = ("Structured falsifiable hypothesis: " + hypothesis.text
              + ". Restate it while preserving operands, direction, measure, and lens: ")
    candidate = mouth.ideate(prompt, gen, top_k, temp, seed_rng)
    if divergence_preserves(hypothesis, candidate):
        return DivergenceRealization(candidate, True, "model")
    return DivergenceRealization(hypothesis.text, False, "workspace_fallback")


def select_divergence(seed: str, evidence: Iterable[Fact] = (),
                      require_evidence: bool = False) -> DivergenceDecision | None:
    """Reject contradicted lenses and select the cheapest grounded surviving test."""
    hypotheses = diverge_seed(seed)
    if not hypotheses:
        return None
    evidence_keys = {fact.key for fact in evidence}
    rejected = tuple(
        h.spec.claim_id for h in hypotheses
        if (h.spec.claim_id, "has_verdict", "contradicted") in evidence_keys
    )
    supported = tuple(
        h.spec.claim_id for h in hypotheses
        if (h.spec.claim_id, "has_verdict", "supported") in evidence_keys
        and h.spec.claim_id not in rejected
    )
    viable = [h for h in hypotheses if h.spec.claim_id not in rejected]
    grounded = [h for h in viable if h.spec.claim_id in supported]
    pool = grounded if grounded else ([] if require_evidence else viable)
    if not pool:
        return DivergenceDecision(
            "insufficient grounded divergent evidence", hypotheses, None,
            rejected, supported, True,
            "all_candidates_rejected" if not viable else "no_supported_candidate",
        )
    # Frozen testing-cost order: direct directional/null comparisons require one
    # measurement; threshold/delay/context require an additional intervention axis.
    cost = {"positive": 1, "negative": 1, "null": 1,
            "threshold": 2, "delay": 2, "context": 2}
    index = {h.spec.claim_id: i for i, h in enumerate(hypotheses)}
    selected = min(pool, key=lambda h: (cost[h.lens], index[h.spec.claim_id]))
    reason = "supported_evidence" if grounded else "lowest_preregistered_test_cost"
    return DivergenceDecision(
        selected.text, hypotheses, selected.spec.claim_id, rejected, supported, False, reason
    )


def certify_divergence(seed: str) -> dict[str, object]:
    """Live hypotheses pass; missing-operand and lens-shuffle controls collapse."""
    hypotheses = diverge_seed(seed)
    live = [divergence_preserves(h, h.text) for h in hypotheses]
    missing = []
    shuffled = []
    for index, hypothesis in enumerate(hypotheses):
        words = hypothesis.text.split()
        missing_text = " ".join(w for w in words if w not in hypothesis.required_terms[-1:])
        missing.append(divergence_preserves(hypothesis, missing_text))
        other = hypotheses[(index + 1) % len(hypotheses)]
        shuffled.append(divergence_preserves(hypothesis, other.text))
    unique_specs = len({(h.lens, h.spec.measure, h.spec.falsified_when) for h in hypotheses})
    word_sets = [set(_words(h.text)) for h in hypotheses]
    pairwise_max = max(
        (len(a & b) / len(a | b) for i, a in enumerate(word_sets) for b in word_sets[:i]),
        default=0.0,
    )
    ok = (len(hypotheses) == 6 and all(live) and not any(missing)
          and not any(shuffled) and unique_specs == 6 and pairwise_max <= 0.5)
    return {"ok": ok, "count": len(hypotheses), "live": sum(live),
            "missing_admit": sum(missing), "shuffle_admit": sum(shuffled),
            "unique_specs": unique_specs, "pairwise_max": pairwise_max,
            "hypotheses": hypotheses}
#!/usr/bin/env python3
# closure_ladder.py — the INTERVENTIONAL CLOSURE LADDER (rung 1), engine-native.
#
# WHAT THIS IS (and, more importantly, what it is NOT)
# ----------------------------------------------------
# An A/B-randomized interventional rig that asks ONE question:
#
#     does an agent's CONTINGENCY STRUCTURE — not its action marginal — leave a
#     distributional fingerprint on its OWN subsequent input?
#
# Because it INTERVENES (the executed action is a seeded coin over {true action,
# marginal-matched shuffle}), P(I_{t+1} | do(A_t)) is IDENTIFIED: the rig can ANCHOR,
# not merely correlate. That is the whole reason it is worth having in production —
# every observational lens in this repo can only refuse.
#
#   ⚠️ RUNG 1 IS A LOW BAR AND IS NOT ALIVENESS. A thermostat clears it; the scripted
#   P-LIVE plant here (a ~15-line homeostatic policy) MUST clear it, by design. Reading
#   a closure PASS as "consciousness" / "aliveness" is a category error. The rig
#   certifies that closed-loop causation EXISTS and IS MEASURABLE in a world built so
#   that closure matters — an existence proof plus a certified instrument, nothing more.
#   Discrimination lives on the rungs ABOVE (loop gain, homeostasis, closure over
#   self-written memory), each of which reopens the echo trap in a new form.
#
# PROVENANCE + THE LOAD-BEARING REPAIR
# ------------------------------------
# Ported from the lab/v3 campaign (H_011 stage-A certified instrument, H_013 repair).
# The lab's stage-A certification was real, but the CERTIFIED estimator carried a FRAME
# MISALIGNMENT that stage A could not see (its P-DEAD plant only ever checked the LV-W
# channel arm, never LV-C):
#
#   `lv_c` compared the Closed arm's PRE-step observations [o_0 .. o_{T-1}] against the
#   ghosts' POST-step observations [o_1 .. o_T]. Closed therefore sat ONE TICK BEHIND
#   both ghosts, so d(C,P1) carried a one-tick-shift term that d(P1,P2) lacked. In a
#   fully INERT (null) env — where the two ghosts are bit-identical and d(P1,P2) == 0
#   exactly — that shift term is pure exogenous drift, and the estimator read closure
#   0.667, ABOVE the 0.60 anchor gate. The instrument could not refuse a DEAD WORLD.
#
#   Fix (one line, upstream): fC = obs_traj[1:]. Repaired, an inert env reads 0.000.
#
# THIS PORT SHIPS THE REPAIRED ESTIMATOR AND MAKES THE NULL-ENV CHECK STANDING:
# `certify()` runs P-DEAD on BOTH arms (LV-W channel AND LV-C closure) and hard-fails
# the battery if null closure exceeds NULL_CLOSURE_MAX, plus a direct structural
# regression test (`_frame_alignment_check`) that the aligned Closed stream is
# bit-identical to its ghosts in an inert world. This exact bias can never silently
# return.
#
#   ⚠️ NO LAB NUMBER IS IMPORTED AS A PRODUCTION CLAIM. In particular lab/v3's 7B
#   "ANCHOR-ON-LV-C 0.7625" was measured with the BIASED estimator and is SUSPENDED
#   upstream. What is salvaged here is the RIG, not the result.
#
# THE THREE PLANTS (the certification battery — the instrument must land all three)
# --------------------------------------------------------------------------------
#   P-LIVE  contingent homeostatic policy, coupled env  -> ANCHOR       (LV-W pass, LV-C pass)
#   P-OPEN  the SAME actions as a fixed TAPE (order destroyed), coupled env
#                                                       -> CHANNEL-ONLY (LV-W pass, LV-C FAIL)
#   P-DEAD  contingent policy, INERT (null) env         -> REFUSED      (LV-W fail, LV-C ~0)
#
# P-OPEN is what makes this a measurement rather than a tautology: it has the identical
# action MARGINAL and a live action channel, and it must still FAIL the closure gate.
# "Acting changes what you next perceive" is trivially true in any sandbox; closure is
# not. P-DEAD is what makes the repair permanent.
#
# Deterministic, stdlib only (no numpy/torch), $0. Every exogenous stream is keyed by
# (seed, t, tag) — NEVER a shared consumed generator — so factual / ghost / counter-
# factual branches at tick t draw the SAME noise xi_t. That shared noise is the entire
# basis of the yoked pairing; a shared generator silently destroys it.
#
# Driven from the installed CLI (a_experiment_engine_native — a manipulation is a FLAG,
# never a script beside the engine):
#
#   anima-py evaluate --closure-ladder [--closure-arm {live,open,dead}]
#                     [--closure-ticks N] [--closure-seed S] [--out f.json]

from __future__ import annotations

import copy
import heapq
import math

# ── micro-tenant world ────────────────────────────────────────────────────────
ACTIONS = ["PROC", "DROP", "ARCH", "COMPACT", "REST", "PROBE", "FLUSH", "NOOP"]
ITEM_TYPES = ["req", "spam", "junk"]

Q_MAX = 12                 # queue overflow threshold
E_MAX = 20.0               # energy cap
E0 = 10.0                  # initial energy
N_REGIME = 3               # hidden Markov regime count
REGIME_ARRIVAL = [0.30, 0.65, 0.95]     # regime -> arrival gate
REGIME_REGEN = [1.6, 1.0, 0.5]          # regime -> energy regen per tick
ACTION_COST = {"PROC": 0.5, "DROP": 0.1, "ARCH": 0.4, "COMPACT": 1.2,
               "REST": -3.0, "PROBE": 0.8, "FLUSH": 0.2, "NOOP": 0.0}

# ── frozen gates ──────────────────────────────────────────────────────────────
KNN = 5                    # LOO k-NN neighbourhood
BLOCK = 50                 # LV-C block size (ticks)
FEAT_DIM = 256             # hashed n-gram feature dim
SIGN = 0.55                # LV-W per-pair sign threshold
CLOSURE_SIGN = 0.60        # LV-C per-block closure threshold (the anchor gate)
NULL_CLOSURE_MAX = 0.05    # H_013 REPAIR GUARD: an INERT env must read ~0 closure.
# Measured power floor (parent session, seed 7): at T=600 the battery certifies on 12 blocks
# (P-LIVE 0.750 · P-OPEN 0.417 · P-DEAD 0.000); at T=400 it has 8 blocks and P-OPEN's channel
# arm falls to sign_base_full 0.537 < SIGN, so the battery reads a FAILURE that is really a
# sample-size artefact. A failure below this floor is therefore reported as UNDER-POWERED, not
# as INSTRUMENT-INVALID — conflating "too few blocks" with "broken" is how a power problem gets
# recorded as a substrate fact (power-before-negative-verdict).
MIN_BLOCKS = 12
                           # The pre-repair (frame-misaligned) estimator read 0.667 here,
                           # i.e. above CLOSURE_SIGN. If this trips, the frame alignment
                           # regressed — do not read any closure number until it is fixed.


def _hash(*parts) -> int:
    """FNV-1a 32-bit over a stable string key (process-stable — the point vs hash())."""
    h = 0x811C9DC5
    for b in "|".join(str(p) for p in parts).encode():
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def _fnv1a(b: bytes) -> int:
    h = 0x811C9DC5
    for byte in b:
        h ^= byte
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def _u(*parts) -> float:
    """Deterministic uniform [0,1) keyed by (seed, t, tag, ...)."""
    return _hash(*parts) / 4294967296.0


def features(data: bytes, dim: int = FEAT_DIM) -> list:
    """Char n-gram (n in {1,2,3}) counts -> `dim` FNV-1a buckets -> log1p -> L2-normalized."""
    counts = [0] * dim
    n = len(data)
    for size in (1, 2, 3):
        for i in range(n - size + 1):
            counts[_fnv1a(data[i:i + size]) % dim] += 1
    vec = [math.log1p(c) for c in counts]
    norm = math.sqrt(sum(x * x for x in vec))
    return [x / norm for x in vec] if norm > 0 else vec


def sqdist(a: list, b: list) -> float:
    """Squared Euclidean distance between two equal-length vectors."""
    return sum((x - y) ** 2 for x, y in zip(a, b))


def initial_state(seed: int) -> dict:
    """Deepcopy-snapshotable initial state sigma_0 (~12 scalars + a small queue)."""
    q = []
    for i in range(3):
        ty = ITEM_TYPES[_hash(seed, "init", i) % 3]
        sz = 1 + _hash(seed, "init", "sz", i) % 5
        q.append((ty, sz))
    return {"Q": q, "S": 2, "S_decay": 0, "E": E0,
            "regime": _hash(seed, "init", "regime") % N_REGIME,
            "hint": -1, "overflow": 0}


def _apply_action(s: dict, action: str) -> None:
    """The agent's effect on the state (mutates s). The INERT (null) env skips this entirely."""
    q = s["Q"]
    if action == "PROC" and q:
        ty, _sz = q.pop(0)
        s["E"] += 2.0 if ty == "req" else (-1.0 if ty == "spam" else 0.0)
    elif action == "DROP" and q:
        q.pop(0)
    elif action == "ARCH" and q:
        q.pop(0)
        s["S"] += 1
    elif action == "COMPACT":
        s["S_decay"] = max(0, s["S_decay"] - 3)
    elif action == "FLUSH":
        del q[: len(q) // 2]
    # REST: energy handled via the (negative) ACTION_COST · PROBE: hint set in step() · NOOP: nothing
    s["E"] -= ACTION_COST[action]


def step(state: dict, action: str, seed: int, t: int, null: bool = False) -> dict:
    """Advance one tick. Returns a NEW state (input untouched).

    Exogenous streams are keyed by (seed, t, tag), so stepping the SAME state at tick t
    under DIFFERENT actions draws the SAME xi_t — the yoked/counterfactual pairing law.
    With null=True the action is ignored entirely (no action->input channel exists)."""
    s = copy.deepcopy(state)
    probed = (action == "PROBE") and not null
    if not null:
        _apply_action(s, action)
    # --- exogenous, action-INDEPENDENT dynamics (the autonomous drive) ---
    if _u(seed, t, "regime_move") > 0.7:
        s["regime"] = (s["regime"] + 1 + _hash(seed, t, "regime_dir") % (N_REGIME - 1)) % N_REGIME
    reg = s["regime"]
    n_arr = sum(1 for i in range(2) if _u(seed, t, "arr", i) < REGIME_ARRIVAL[reg])
    for i in range(n_arr):
        ty = ITEM_TYPES[_hash(seed, t, "arr_ty", i) % 3]
        sz = 1 + _hash(seed, t, "arr_sz", i) % 5
        s["Q"].append((ty, sz))
    if action != "COMPACT" or null:
        s["S_decay"] += 1
    s["E"] = min(E_MAX, s["E"] + REGIME_REGEN[reg])
    if len(s["Q"]) > Q_MAX:
        s["overflow"] = 1
        s["E"] -= 2.0
        del s["Q"][Q_MAX:]
    else:
        s["overflow"] = 0
    s["E"] = max(0.0, s["E"])
    s["hint"] = (reg if _u(seed, t, "hint_noise") < 0.8
                 else _hash(seed, t, "hint_wrong") % N_REGIME) if probed else -1
    return s


def observe(state: dict) -> str:
    """The agent's INPUT: a fixed-template digest of COMPUTED quantities only.

    Action names NEVER appear (disjoint vocabulary — see echo_guard). Every action->input
    influence therefore flows through DYNAMICS, never a byte copy. Without this law the
    whole rig degenerates into the echo/tautology trap it exists to avoid."""
    q = state["Q"]
    head_ty, head_sz = (q[0] if q else ("none", 0))
    d_band = "clean" if state["S_decay"] < 4 else ("worn" if state["S_decay"] < 10 else "rotten")
    e_band = "low" if state["E"] < 5 else ("mid" if state["E"] < 13 else "high")
    hint = "none" if state["hint"] < 0 else "r%d" % state["hint"]
    return ("queue depth %d head %s size %d store %d decay %s energy %s overflow %d hint %s"
            % (len(q), head_ty, head_sz, state["S"], d_band, e_band, state["overflow"], hint))


def echo_guard() -> dict:
    """LV-E: no action name may appear anywhere in the reachable observation vocabulary."""
    vocab = set()
    for seed in range(4):
        s = initial_state(seed)
        for t in range(60):
            vocab.update(observe(s).lower().split())
            s = step(s, ACTIONS[t % len(ACTIONS)], seed, t)
    clash = sorted(a for a in ACTIONS if a.lower() in vocab)
    return {"clash": clash, "ok": not clash}

exec
/bin/zsh -lc "git show origin/main:cli/train.py | rg -n -i \"comp[-_ ]lane|H_9900|whole answer|answer span\" | sed -n '1,240p'
git show origin/main:cli/evaluate.py | rg -n -i \"comp[-_ ]lane|H_9900|H_9899|H_9883|H_9875\" | sed -n '1,320p'
git show origin/main:cli/corpus.py | rg -n -i \"compose|composition|H_9883|H_9900\" | sed -n '1,260p'
git show origin/main:core/model.py | rg -n -i \"comp[-_ ]lane|composition|H_9900\" | sed -n '1,260p'" in /Users/mini/dancinlab/anima
 succeeded in 5341ms:
2026-07-22 13:27:34.924 xcodebuild[80582:10025809]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:35.048 xcodebuild[80582:10025808] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-d0SbtoX6' (errno=Operation not permitted)
2026-07-22 13:27:35.379 xcodebuild[80584:10025817]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:35.499 xcodebuild[80584:10025816] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
963:    """(B, T) bool — True on target positions that lie in the ANSWER span of an arrow line.
991:    # right bound: the first newline at or after `start` closes the answer span
1384:        # H_9900 composition lane — attached by the caller when --comp-lane is given. need_pen
1385:        # must include it: the lane reads the trunk penultimate (detached) at the answer span.
1386:        self.comp_lane = None
1459:                if self.comp_lane is not None:        # H_9900 composition lane (default None = off)
1464:                    cl_logits = self.comp_lane(ph.float().detach())
1619:# ══ H_9900 — COMPOSITION LANE (multi-byte answer, CE that never reaches the trunk) ═══════════
1630:#   * CE is computed on THAT head's logits over the WHOLE answer span,
1646:        """CE over the answer span only. ans_mask: (B, T) bool marking the composed answer bytes."""
1656:    """Answer span = bytes after the LAST separator up to the terminator, per row.
2994:    ap.add_argument("--comp-lane", action="store_true",
2995:                    help="H_9900 composition lane: a separate answer-span head trained off a "
3000:                    help="weight on the composition-lane CE (--comp-lane only)")
3171:                    help="H_9811: extra CE weight on the ANSWER span of ` => ` arrow lines "
3885:    if a.comp_lane:
3886:        # H_9900 — attach BEFORE the param assert below so the lane head is allreduced like any
3895:            sys.exit("[comp-lane] this model exposes no trunk penultimate")
3897:        shell.comp_lane = CompositionLane(_d_pen, V).to(device)
3899:        params = params + [q for q in shell.comp_lane.parameters()]
3900:        opt.add_param_group({"params": list(shell.comp_lane.parameters())})
3901:        print("  comp-lane: ON · d=%d V=%d weight=%.3f (CE detached from the trunk)"
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-MZEeuRWd' (errno=Operation not permitted)
2026-07-22 13:27:36.264 xcodebuild[80591:10025850]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:36.385 xcodebuild[80591:10025849] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-pS4Zh4TO' (errno=Operation not permitted)
2026-07-22 13:27:36.713 xcodebuild[80593:10025859]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:36.833 xcodebuild[80593:10025858] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
1295:    print("      [--store-oracle-pair]  H_9875 · compose-2 panels only: hands the address for BOTH")
7539:        # H_9875 pair-oracle: the 2-conjunct analogue of C0-e. Splits "addressing is the wall"
7763:        tslot_b = it.get("target_slot_b")     # H_9875 compose-2 panels only (absent elsewhere)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-Tj1nBKVM' (errno=Operation not permitted)
2026-07-22 13:27:37.603 xcodebuild[80600:10025883]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:37.724 xcodebuild[80600:10025882] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-tIzmcGPS' (errno=Operation not permitted)
2026-07-22 13:27:38.060 xcodebuild[80602:10025900]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:38.180 xcodebuild[80602:10025899] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
12:               target IS the derivation, so echo == composition -> CE=echo metalaw
52:    "memory composes into new meaning",
64:# derivation vocabulary (the derivtrace middle = the composition rule made explicit)
67:CLOSE = ["new meaning arises", "meaning composes anew",
68:         "a new whole arises", "they compose into meaning"]
75:# Opposite pairs for the double-negation family. Each is its own composition: the operator
88:# ≥2 CARRIERS per family. A single carrier makes the carrier axis and the composition axis
89:# perfectly collinear — no experiment can then separate "it learned the composition" from
91:# Each carrier is (compose_template, bind_strip_template); {a} {b} {op} are filled per item.
114:# composed answer had to be COMPUTED (arithmetic) or LOOKED UP from an arbitrary table (colour),
152:    the model never saw does not measure a composition failure, it measures atom absence. The
153:    claim axis is composition, so exposure on the ATOM axis must be > 0 for the item to be
174:    # makes the item unreadable for a COMPOSITION claim, while an absent carrier word puts the
272:    compose at all, and the three converging lines (H_9304's +0.0023 nats of non-additive
279:    is the OPERATION; whether that transfers to unseen pairs is exactly the composition question
308:        # cannot work: with a disjoint VOCABULARY a lookup composition has no shared structure to
510:                "family %s has %d carrier(s) — carrier axis is collinear with the composition "
542:                "memory", "composes", "meaning", "silence", "carries", "information",
771:# ── H_9839 dreamgen — the dream node's COMPOSITION LAW as the manipulated variable ──
773:# WHY THIS FORMAT EXISTS, and why no existing one answers it. `core/dream_compose.py`'s own header
781:# derivation of a DECLARED composition rule (the H_9267 XBIND notion) manufacture cross-boundary
800:#                rotation. Composition destroyed, marginals preserved. Must collapse.
814:#   [dreams composed from the PREVIOUS night's anchors] [NIGHT header + RULE] [this night's
816:# — which is `dc_compose_window`'s own semantics (anchors replayed in window w are composed into
889:# that the composition law actually operates on — are drawn from the builder's own `_wp_rand`,
897:# composition laws, same blocking audit, same `mi-screen --mi-robust` judging, same eps.
995:    """H_9839 — emit one arm of the dream-composition-law corpus. Returns (text, audit).
1002:    from dream_compose import (dc_make_anchor, dc_stage_replay_budget, dc_compose_window,
1054:        for d in dc_compose_window(anchors, _DG_STAGE, t):
1170:            "compose": 0, "compose_teach": False,
1205:            # H_9839 dreamgen: --dream-target = the dream node's COMPOSITION LAW (the DV) ·
1336:        elif a == "--compose":
1337:            opts["compose"] = int(argv[i + 1]); i += 2  # H_9875 storebind: 2-conjunct study panel
1338:        elif a == "--compose-teach":
1339:            opts["compose_teach"] = True; i += 1        # H_9875 positive-control build (SEEN slice)
1451:#                     test of composition rather than of memorisation, and what keeps it out of
1465:#                       - consumes AND composes -> it answers ¬(¬p) = p -> WRONG on every row
1493:#                     design, because that is what makes flip1 a test of composition. But 6000 steps
1500:#                     the operator and then asked the model to compose with it.
1508:#                     is INVALID, never FAIL. A composition verdict is only readable on a model whose
1555:#     taught rather than composed. `ground_keep` replays `{s}지 않다` — which is exactly the primary
1792:# composed. The leak audit anchors on the FULL `이 영화 {surf} => ` template (arrow included), so a bare
1869:    # co-train COMPOSITIONAL interference (H_9675 draw-fragility). Default None = 12 = byte-identical.
2109:    compose a declaratively-known fact with the operator; that is exactly what H_9346 measured and
2555:    test is supposed to ask it to COMPOSE — and one leaked sentence is enough to make the verdict
2782:                # turn the flip1 answer from composed into taught.
3016:        # H_9888 mention taps — a 1-slot line is the A=B case of a composed line: both reads land on
3019:        # ever be scored on composed panels, and its precondition gate would be unmeasurable).
3031:# ── H_9875 · compose-2 — STUDY-TIME RECOMBINATION panel (both conjuncts come from the STORE) ──
3035:# combined at decode time. compose-2 asks `<op> A and B => ` with
3041:# The corpus stays 1-slot unless --compose-teach is passed: the study arm must never have seen a
3042:# composed line (that is the whole question), while the taught build exists so a negative can be
3044:_SB_COMPOSE_FILLER = "zzqqx"        # drop-control stand-in: a non-atom that no prompt ever names
3047:def _sb_emit_compose_block(rng, entities, store_slots, drop_b=False, drop_a=False):
3048:    """One compose-2 block: a balanced store + exactly store_slots two-conjunct queries.
3061:    catches it. BOTH must collapse before a composed positive means recombination."""
3072:        raise SystemExit("storebind --compose 2: store_slots %d cannot carry a balanced xor split "
3096:            ents[b] = _SB_COMPOSE_FILLER               # B's fact removed; prompt/gold untouched
3098:            ents[a] = _SB_COMPOSE_FILLER               # A's fact removed; prompt/gold untouched
3104:                     "compose": 2, "xor": pols[a] ^ pols[b]})
3108:def _sb_compose_audit(rows, label):
3109:    """Hard-assert the frozen chance of a compose panel, and MEASURE the one-conjunct ceilings.
3118:        raise SystemExit("storebind --compose 2: %s gold split %d/%d != exact 0.5000 — the panel's "
3181:    The composition is forced on the PAIR-CLASS, not on prompt presence (else both arms co-emit ⇒
3182:    delta≈0). frozen geometry gives the split: BIND class = adjacent pairs (a,(a+1)%n) = the composed
3185:    the prompt) — unsolvable by echo, which is exactly 'composition'."""
3327:                    entity_pool=None, compose=0, compose_teach=False):
3389:    # ── H_9875 compose-2 panels (both conjuncts from the store) ─────────────────────────────────
3391:    #   compose      = HELD-OUT entities, corpus has 0 composed lines  → the study arm (the DV)
3392:    #   compose_drop = the SAME items with B's fact deleted from the store → 1-SLOT-ONLY control
3393:    #   compose_seen = TRAIN entities → the SEEN slice. Under --compose-teach this is the positive
3394:    #                  control that says the composed readout is legible AT ALL; without it the
3398:    compose_rows = compose_drop_rows = compose_seen_rows = None
3399:    compose_audit = {}
3400:    if compose:
3401:        if compose != 2:
3402:            raise SystemExit("storebind: --compose %d unsupported (2 only — the 2-conjunct panel is "
3403:                             "the recombination shape H_9875 pre-registered)" % compose)
3405:            raise SystemExit("storebind --compose 2: --store-slots must be a multiple of 4 (got %d) "
3413:                _, br = _sb_emit_compose_block(crng, ents, store_slots,
3420:                raise SystemExit("storebind --compose 2: %s control diverged from the main arm "
3423:        compose_rows, compose_drop_rows, compose_seen_rows = c_rows, d_rows, s_rows
3424:        compose_drop_a_rows = da_rows
3425:        compose_audit = {"held": _sb_compose_audit(c_rows, "compose"),
3426:                         "drop_a": _sb_compose_audit(da_rows, "compose_drop_a"),
3427:                         "drop": _sb_compose_audit(d_rows, "compose_drop"),
3428:                         "seen": _sb_compose_audit(s_rows, "compose_seen")}
3429:        if compose_teach:
3430:            # POSITIVE-CONTROL BUILD: composed lines enter the corpus (TRAIN entities only) and the
3431:            # co-train manifest in lockstep, so a ckpt exists for which the composed readout is
3433:            # below re-asserts it over the composed lines too · corpus-py-1 (C)).
3436:                bl, br = _sb_emit_compose_block(t_rng, train, store_slots)
3476:    if compose:
3479:                 "seed": seed, "compose": compose, "entries": rows}
3482:        st["compose"] = compose
3483:        st["compose_teach"] = compose_teach
3484:        st["compose_audit"] = compose_audit
3485:        st["compose_manifest"] = _cm(compose_rows, held_out=True, balanced=True)
3486:        st["compose_drop_manifest"] = _cm(compose_drop_rows, held_out=True, balanced=True,
3488:        st["compose_drop_a_manifest"] = _cm(compose_drop_a_rows, held_out=True, balanced=True,
3490:        st["compose_seen_manifest"] = _cm(compose_seen_rows, held_out=False, seen=True,
3516:#  ② the target is a pure composition: answer_bit = sense_bit XOR role_bit. Nothing else in the
3697:# POSITIVE CONTROL: gold = hp alone, so the answer is a single local feature with no composition
3715:    # R11 stair: at the conjunct level only three PRIMITIVE tasks exist — xor (composition),
3739:# claim than an architectural one — it shows the composition is LEARNABLE given sub-feature
3958:    """The ONLY rule in the format: compose the stem declaration with the operator declaration."""
4808:# cannot compose" instead of "the fine-tune was too small". H_9324 then measured the floor: on this
4837:    # WRITE fails, raising the budget is NOT tune-to-green: asking a model to COMPOSE a fact it never
4890:            "it to compose. Use `ground_keep` unless you specifically want the broken-operator arm."
5575:    codec's own decomposition (state/nbind_curriculum/morph2b.py) — reimplemented here rather
6897:        print("             H_9839 — the dream node's COMPOSITION LAW as the manipulated variable.")
6898:        print("             core/dream_compose.py blends two co-replayed anchors by coord midpoint")
6912:        print("             carrier makes the carrier axis collinear with the composition axis).")
6950:        print("             that the model can compose a declaratively-known fact (that is H_9346, 🧱).")
6981:        print("      [--compose 2] [--compose-teach]   H_9875 STUDY-TIME RECOMBINATION panel:")
6983:        print("      lane writes one of them in the prompt). Emits .compose2.json (study arm ·")
6984:        print("      corpus teaches 0 composed lines) · .compose2_drop.json (1-SLOT-ONLY control:")
6986:        print("      .compose2_seen.json (SEEN slice). --compose-teach puts composed lines IN the")
7010:        print("      DISJOINT from the scored surfaces (else the flip1 answer is taught, not composed);")
7014:        print("                  compositional interference (H_9751; N=1 = single-stem write crack)")
7044:        print("      (flip1) forms NEVER appear, so a later flip1 test measures COMPOSITION, not")
7048:        print("      consumes AND composes the written polarity must score FAR BELOW chance on")
7074:            # answer is taught rather than composed. Refuse to write a corpus that would void the run.
7147:            # taught rather than composed. Refuse to write a corpus that would void the run.
7256:                                   entity_pool=opts["entity_pool"], compose=opts["compose"],
7257:                                   compose_teach=opts["compose_teach"])
7295:        # H_9875 compose-2 panels (opt-in · absent flag = every existing build byte-identical).
7296:        if st.get("compose"):
7297:            cj = opts["out"] + ".compose2.json"
7298:            dj = opts["out"] + ".compose2_drop.json"
7299:            aj = opts["out"] + ".compose2_dropA.json"
7300:            zj = opts["out"] + ".compose2_seen.json"
7301:            json.dump(st["compose_manifest"], open(cj, "w", encoding="utf-8"), ensure_ascii=False)
7302:            json.dump(st["compose_drop_manifest"], open(dj, "w", encoding="utf-8"),
7304:            json.dump(st["compose_drop_a_manifest"], open(aj, "w", encoding="utf-8"),
7306:            json.dump(st["compose_seen_manifest"], open(zj, "w", encoding="utf-8"),
7308:            ca = st["compose_audit"]
7309:            print("  compose-2 (H_9875) -> %s (%d held-out · study arm) · %s (B-deleted control) · "
7318:            print("     corpus composed lines = %s ⟹ the study arm's exposure to composition is %s"
7319:                  % ("TAUGHT (--compose-teach)" if st["compose_teach"] else "0",
7320:                     "the positive-control build" if st["compose_teach"] else "ZERO (the question)"))
7370:        # H_9839 — the dream node's COMPOSITION LAW as the manipulated variable. Judged by
7381:            print("      H_9839 — swaps core/dream_compose.py's geometric midpoint (its own header:")
7383:            print("      derivation of a DECLARED composition rule, and emits both plus a")
7445:        print("    the text= payload, i.e. the composition LAW, differs).")
7492:            # answer, or that runs on ONE carrier, measures something other than composition.
7524:            print("                  NOT composition failure, and must be dropped or the corpus fixed)")
7528:            print("    TARGET-WORD absent %d  ⚠️ this counts the target WORD, not the composed"
7541:            print("     measures atom absence, not composition · corpus-py-1 (F)).")
7582:            print("  ⚠️ POSITIVE CONTROL (--bind-task hp) — gold = hp ALONE, no composition. The "
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-jjuW1jdr' (errno=Operation not permitted)
2026-07-22 13:27:38.952 xcodebuild[80609:10025949]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:39.074 xcodebuild[80609:10025948] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-Bo1rOANw' (errno=Operation not permitted)
2026-07-22 13:27:39.404 xcodebuild[80611:10025958]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:39.525 xcodebuild[80611:10025957] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.

exec
/bin/zsh -lc "git show origin/main:cli/train.py | sed -n '1370,1475p'
git show origin/main:cli/train.py | sed -n '1610,1675p'
git show origin/main:cli/train.py | sed -n '2980,3020p'
git show origin/main:cli/evaluate.py | sed -n '7480,7835p'" in /Users/mini/dancinlab/anima
 succeeded in 5470ms:
2026-07-22 13:27:52.075 xcodebuild[80733:10026612]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:52.201 xcodebuild[80733:10026611] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-yi8MSuhG' (errno=Operation not permitted)
2026-07-22 13:27:52.557 xcodebuild[80735:10026620]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:52.680 xcodebuild[80735:10026619] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
                 obj_needs_pen, dict_on, jamo_on, bf16, device):
        super().__init__()
        self.model = model
        # objfn is EITHER an nn.Module (predictive_info/constructive_bind aux heads) or a
        # plain function (ce_marginal/infonce/…). Register the module form as a submodule so
        # its params enter the DDP bucket set; keep the function form as a bare attribute.
        self.objfn = objfn if isinstance(objfn, nn.Module) else None
        self._objfn_fn = None if isinstance(objfn, nn.Module) else objfn
        self.jamo_head = jamo_head            # None when jamo off
        self.is_bytegpt = is_bytegpt
        self.V = V
        self.obj_needs_pen = obj_needs_pen
        self.dict_on = dict_on
        self.jamo_on = jamo_on
        # H_9900 composition lane — attached by the caller when --comp-lane is given. need_pen
        # must include it: the lane reads the trunk penultimate (detached) at the answer span.
        self.comp_lane = None
        self.comp_w = 1.0
        self.comp_sep = 32                            # b" "
        self.comp_end = 46                            # b"."
        self.need_pen = obj_needs_pen or dict_on or jamo_on
        self.bf16 = bf16
        self.device = device

    def _objfn(self):
        return self.objfn if self.objfn is not None else self._objfn_fn

    def trunk_penultimate(self, x):
        # VERBATIM relocation of the former module-level trunk_penultimate closure
        # (reads self.model). ByteGPT exposes its pre-head hidden directly; CLM recomputes
        # the trunk to the pre-readout MoE/norm_out site (note: pre-SLW, as before).
        m = self.model
        if self.is_bytegpt:
            return m(x)["penultimate"]              # (B, d, T) — ln_f(x) pre-head
        h = m.embed(x).transpose(1, 2)
        h = m.embed_conv(h)
        for layer in m.trunk:
            h = layer(h)
        hm, _ = m.moe(h)
        hm = m.norm_out(hm)
        return hm                                   # (B, d, T) — pre-readout dictionary site

    def ideation_forward(self, x, tap_L):
        """H_9803 — one CLM forward that also returns the PRESERVED early (layer tap_L) tap.

        Mirrors CLMConvMoE.forward's op order exactly (embed → embed_conv → trunk → faction
        bridge → MoE → norm_out → SLW → readout); it does not touch model.forward, so the golden
        path stays byte-identical. tap_L<=0 ⇒ the tap IS the penultimate (the `penult` route =
        the tap-DEPTH control, H_9720-C1 idiom: same head, only the tap LOCATION differs)."""
        m = self.model
        h = m.embed(x).transpose(1, 2)
        h = m.embed_conv(h)
        tap = None
        for i, layer in enumerate(m.trunk):
            h = layer(h)
            if tap_L > 0 and (i + 1) == tap_L:
                tap = h
        if getattr(m, "faction_bridge", None) is not None:
            h = m.faction_bridge(h)
        hm, stats = m.moe(h)
        hm = m.norm_out(hm)
        if tap is None:
            tap = hm                                   # penult route (or tap_L deeper than the trunk)
        xr = m.slw(hm) if getattr(m, "slw", None) is not None else hm
        logits = m.readout(xr)                         # (B, V, T)
        return logits, hm, tap, stats.aux_loss

    def forward(self, x, y, obj_gen, dict_lambda, jamo_lambda, sb=None, sb_w=1.0, sb_oracle=False, sb_addr_w=0.0, sb_oracle_aux=0.0, sb_tap_grad="detached",
                idl=None, idl_w=1.0, idl_assign="hungarian", idl_route="l3-disjoint",
                idl_tap_L=3, idl_gen=None, ans_w=0.0):
        # ── VERBATIM relocation of the per-step loss-composition block (bf16 + fp32). The
        #    autocast context stays wrapping ONLY the forward/compose (backward is at the
        #    callsite, outside autocast — DDP hooks fire there). Returns (loss, detached CE,
        #    aux) so the callsite can backward + all-reduce the shard CE (§3).
        model = self.model
        objfn = self._objfn()
        V = self.V
        aux = {}
        need_pen = self.need_pen
        if self.bf16 and self.device.startswith("cuda"):
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = model(x, y)
                h = self.trunk_penultimate(x) if need_pen else None
                pen = h.float() if (h is not None and self.obj_needs_pen) else None
                obj_loss, oaux = objfn(out["logits"].float(), y, V, obj_gen, penultimate=pen)
                loss = obj_loss + out["aux_loss"]
                if ans_w > 0.0:                       # H_9811 answer-weighted CE (default 0 = off)
                    ace, an = answer_ce(out["logits"].float(), y, V)
                    loss = loss + ans_w * ace
                if self.comp_lane is not None:        # H_9900 composition lane (default None = off)
                    # DETACH is the whole point: this lane's CE must not reach the trunk, or it
                    # competes with the language stratum exactly as replay does (H_9898).
                    ph = h if h is not None else self.trunk_penultimate(x)
                    assert ph is not None, "composition lane needs the trunk penultimate"
                    cl_logits = self.comp_lane(ph.float().detach())
                    cmask = _comp_answer_mask(y, self.comp_sep, self.comp_end)
                    closs = CompositionLane.loss(cl_logits, y, cmask)
                    loss = loss + self.comp_w * closs
                    aux["comp_ce"] = float(closs.detach())
                    aux["comp_span"] = float(cmask.float().mean())
                    aux["ans_ce"] = float(ace.detach()); aux["ans_n"] = an
                if self.dict_on:
                    dloss = dict_lambda * h.abs().mean()
                    loss = loss + dloss; aux["dict_l1"] = float(dloss.detach())
                if self.jamo_on:
                    jl = self.jamo_head(h.float())
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-w4qqam54' (errno=Operation not permitted)
2026-07-22 13:27:53.465 xcodebuild[80741:10026645]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:53.596 xcodebuild[80741:10026644] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-DxawSLWx' (errno=Operation not permitted)
2026-07-22 13:27:53.933 xcodebuild[80743:10026656]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:54.057 xcodebuild[80743:10026655] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
            if n_doc:
                loss = loss + idl_w * (idl_loss_sum / n_doc)
                for k_, v_ in idl_aux_acc.items():
                    aux[k_] = v_ / n_doc                               # MONITOR-ONLY (a_train_inline_gauge)
        aux.update(oaux)
        return loss, out["ce_loss"].detach(), aux



# ══ H_9900 — COMPOSITION LANE (multi-byte answer, CE that never reaches the trunk) ═══════════
# H_9898 measured the constraint this lane exists to escape: at equal drill exposure, replay's
# mere PRESENCE prevents composition from being learned (25% x 8000 steps reads rho·weave 0.000
# while 100% x 2000 reads 0.525), because both compete for the same trunk CE. a_substrate_disjoint
# names the fix — separation preserves, overlap conflicts.
#
# H_9899 established why --store-bridge cannot be reused: its window carries gold[:1], one byte,
# while composed answers run 4-6 bytes. So this lane keeps the store lane's ESSENTIAL property
# (CE off the trunk) and drops its binary readout:
#
#   * a separate linear head reads the trunk penultimate at the answer positions,
#   * CE is computed on THAT head's logits over the WHOLE answer span,
#   * the penultimate is DETACHED, so no gradient from this lane reaches the trunk,
#   * and the head's targets are the answer bytes rho·weave will look for verbatim.
class CompositionLane(torch.nn.Module):
    """Answer-span readout trained off a detached trunk (requirements 1-3 of H_9899)."""

    def __init__(self, d, V):
        super().__init__()
        self.head = torch.nn.Linear(d, V)

    def forward(self, pen_detached):
        # pen_detached: (B, d, T) — already detached by the caller, asserted below.
        return self.head(pen_detached.transpose(1, 2))          # (B, T, V)

    @staticmethod
    def loss(logits, y, ans_mask):
        """CE over the answer span only. ans_mask: (B, T) bool marking the composed answer bytes."""
        if ans_mask.sum() == 0:
            return logits.sum() * 0.0
        sel = ans_mask.reshape(-1)
        lg = logits.reshape(-1, logits.shape[-1])[sel]
        tg = y.reshape(-1)[sel]
        return F.cross_entropy(lg, tg)


def _comp_answer_mask(y, sep_byte, end_byte):
    """Answer span = bytes after the LAST separator up to the terminator, per row.

    The drill line is '<cue> <answer> .', so the answer is what follows the final space before
    the period. Marking it explicitly is what makes this lane multi-byte where the store lane is
    not — the whole compound is a target, not just its first character."""
    B, T = y.shape
    mask = torch.zeros_like(y, dtype=torch.bool)
    for b in range(B):
        row = y[b]
        ends = (row == end_byte).nonzero()
        if ends.numel() == 0:
            continue
        e = int(ends[-1].item())
        seps = (row[:e] == sep_byte).nonzero()
        if seps.numel() < 2:
            continue
        st = int(seps[-2].item()) + 1                  # after the space preceding the answer
        if st < e:
            mask[b, st:e] = True
    return mask
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-SY1Oq3CJ' (errno=Operation not permitted)
2026-07-22 13:27:54.827 xcodebuild[80749:10026678]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:54.949 xcodebuild[80749:10026677] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-iARBkBz1' (errno=Operation not permitted)
2026-07-22 13:27:55.281 xcodebuild[80751:10026688]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:55.401 xcodebuild[80751:10026687] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
    ap = argparse.ArgumentParser(
        description="anima canonical python trainer (`anima-py train`) — CLMConvMoE "
                    "SAVANT+MITOSIS recipe + H_1640 arm×objective compositional levers")
    ap.add_argument("--arch", default="clm", choices=["clm", "bytegpt"],
                    help="trunk architecture: clm=CLMConvMoE (default, .clm out) | "
                         "bytegpt=24-layer GPT-2-class ByteGPT (.bin out) — the CLEAN G1 "
                         "wall (single=2). The arm×objective compositional levers are "
                         "arch-agnostic (operate on logits+penultimate); the CLM-specific "
                         "levers (savant/mitosis/tlora/dict/jamo) are gated OFF for bytegpt.")
    ap.add_argument("--arm", default="ctrl", choices=list(ARMS))
    ap.add_argument("--objective", default="ce_marginal", choices=list(OBJECTIVES),
                    help="OPTIONAL objrun coupling (default ce_marginal = standalone)")
    ap.add_argument("--tlora-rank", type=int, default=TLORA_RANK)
    ap.add_argument("--tlora-no-base", action="store_true", help="drop the dense base")
    ap.add_argument("--comp-lane", action="store_true",
                    help="H_9900 composition lane: a separate answer-span head trained off a "
                         "DETACHED trunk penultimate, so its CE never competes with the language "
                         "stratum (H_9898 measured that competition as the blocker). Multi-byte "
                         "answers, unlike --store-bridge's one-byte readout (H_9899).")
    ap.add_argument("--comp-weight", type=float, default=1.0,
                    help="weight on the composition-lane CE (--comp-lane only)")
    ap.add_argument("--dict-lambda", type=float, default=DICT_LAMBDA)
    ap.add_argument("--jamo-lambda", type=float, default=JAMO_LAMBDA)
    # H_9643: enable the N8 jamo(자모) teach-aux INDEPENDENTLY of --arm, so a faction run
    # (--arm ctrl --n-factions 8) can borrow the ko-coherence signal without the TLoRA that
    # tlora_jamo bundles (which would confound the faction measurement). Default off = unchanged.
    ap.add_argument("--jamo-aux", action="store_true",
                    help="H_9643: turn on the jamo teach-aux head regardless of --arm (no tlora)")
    # H_9200 E1 — gated-write forward-slot (SLW). --slw engages the CORE-owned
    # (core/slw.py) module on the CLMConvMoE penultimate; weights serialize into the
    # "SLW\x01" .clm trailer. Plain CE alone induces the slots (rung-3 de-risk 0.976
    # vs additive 0.145), so this is an ARCH lever (--objective stays ce_marginal).
    ap.add_argument("--slw", action="store_true",
                    help="H_9200 E1: engage the gated-write forward-slot (core/slw.py)")
    ap.add_argument("--slw-n-slot", type=int, default=8, help="SLW addressable slots")
    ap.add_argument("--slw-k", type=int, default=64, help="SLW role/read key dim")
    # H_9423 CLMS store-bridge lane (co-trained). --store-bridge = the storebind corpus c.txt (expects
    # a lockstep <c>.store.jsonl manifest, line i <-> store row i from corpus.build_storebind). The lane
    # OVERWRITES the answer-position logits with lam*store_logits — implemented as a CE decomposition
    # (qpos CE on store_logits + non-qpos trunk CE on the prompt spelling), so the trunk logit gets NO
    # answer-position grad = ② shortcut-cut, structural. Window geometry mirrors evaluate.store_run
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-jCGcvpFL' (errno=Operation not permitted)
2026-07-22 13:27:56.177 xcodebuild[80757:10026746]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:56.299 xcodebuild[80757:10026745] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-zJDfSnpm' (errno=Operation not permitted)
2026-07-22 13:27:56.652 xcodebuild[80760:10026769]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-07-22 13:27:56.782 xcodebuild[80760:10026768] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
    print("     ★ PAIRED verdict: %s %s  (🟢 bd>0∧McNemar p≤.05 · 🧱 TOST 등가=artifact · "
          "⛔ m<5 or emit<floor = 검정력부족·NOT a kill)" % (_icon, _pv))
    if _pv == "UNDECIDABLE" and pd.get("m",0) < 5:
        print("     ⛔ m=%d < 5 ⟹ exact McNemar 로 어떤 데이터도 유의 불가 = fan-smp 상향 필요"
              "(δ=0.05 사전등록엔 N≥288 = fan-smp≈48 · power-before-negative-verdict)." % pd.get("m",0))
    # ── DUAL-GATE (H_9698 follow-on · lab-identified instrument gap) — a bind is CONFIRMED
    # only when BOTH signals agree: PAIRED-SENSITIVE (McNemar composition test above) AND
    # EMISSION-CLEARED (composed J clears the emission-null p95). The R6 control-reversal —
    # a pair-DERANGED (shuffled) arm scoring a McNemar-🟢 while sitting INSIDE the emission
    # null band — is exactly the false positive this conjunction rejects: paired-🟢 read
    # WITHOUT the emission gate over-calls sub-null sign noise as bind. ADDITIVE: the two
    # verdicts above are unchanged; this only reports their AND (no retroactive reverdict ·
    # a lever that USES this gate pre-registers it in its own card · lab reconcile H_9698).
    emission_cleared = r["composed"]["J_mean"] > r["null_p95"]
    paired_sensitive = (_pv == "BIND-SENSITIVE")
    if _pv == "UNDECIDABLE":
        _dg = ("⛔ UNDECIDABLE", "검정력부족 — AND-gate 판정불가 (fan-smp 상향 필요)")
    elif paired_sensitive and emission_cleared:
        _dg = ("🟢 BIND-CONFIRMED", "PAIRED-SENSITIVE ∧ EMISSION-CLEARED 둘 다 통과")
    elif paired_sensitive and not emission_cleared:
        _dg = ("🟡 EMISSION-CONFOUND", "McNemar-🟢 이나 composed J 가 emission-null 안 "
               "= sub-null 부호노이즈 의심 (R6 통제역전 계급) · bind 아님")
    else:   # BIND-ABSENT (TOST equivalence)
        _dg = ("🧱 BIND-ABSENT", "TOST 등가 — 레버가 composition 안 심음")
    print("  ══ DUAL-GATE (H_9698 · PAIRED-SENSITIVE ∧ EMISSION-CLEARED) ══")
    print("     paired=%s(McNemar) · emission_cleared=%s (composed J %.4f %s null p95 %.4f)"
          % ("🟢" if paired_sensitive else ("⛔" if _pv == "UNDECIDABLE" else "🧱"),
             emission_cleared, r["composed"]["J_mean"],
             ">" if emission_cleared else "≤", r["null_p95"]))
    print("     ★ AND-gate: %s — %s" % (_dg[0], _dg[1]))
    return 0


def store_run(argv):
    """`anima-py evaluate <ckpt> --store <held.json> [--store-oracle] [--store-lambda λ]` — H_9423
    CLMS store-bridge lane eval (the CO-TRAINED bridge, NOT the H_9392 --store-mix bolt-on actuator:
    the boundary is "does the fusion parameter live inside the .clm and enter the forward pass"). Each
    held-out item injects its 8-slot store at the query; the CLMS lane forms a content-addressed lookup
    and OVERWRITES the answer-position logits with λ·store_logits (store_only). Binary readout = the
    first answer byte ('g'=good vs 'b'=bad · v2 axis). --store-oracle forces the true slot (C0-e positive
    control: ORACLE<0.90 = value/MLP/λ/serialization plumbing dead — read NO negative before it passes,
    v2 reversed 3 instrument deaths on exactly this). Engine-native core/decode.py (a_eval_py_canonical →
    TERMINAL-eligible). This flag MEASURES; the SEQUENTIAL C0→C1→C2→P1 battery + verdict fire on pool
    (a_toy_scale_recheck · 303M needs owner go). Controls are eval-time store edits: derange
    store.entities = key-shuffle · flip store.pols = wrong-store · --store-lambda 0 = λ0 byte-identical."""
    import numpy as np
    ckpt = argv[0]
    man_path = evaluate_strval(argv[1:], "--store", "")
    oracle = "--store-oracle" in argv
    # H_9888 dual-read controls (pre-registered · compose panels only). collapse forces the second
    # read onto the FIRST mention (aB:=aA) — a lane that passes with the heads collapsed never used
    # two addresses. wrong-second swaps the second read onto a mention from a DIFFERENT item, so the
    # pair summary is built from an unrelated slot. Both must fall to chance for a positive to mean
    # two-address retrieval rather than extra fusion capacity.
    dual_ctrl = evaluate_strval(argv[1:], "--store-dual-ctrl", "")
    if dual_ctrl not in ("", "collapse", "wrong-second"):
        print("ERROR: --store-dual-ctrl must be 'collapse' or 'wrong-second', got %r" % dual_ctrl)
        return 1
    if "--store-oracle-pair" in argv:
        # H_9875 pair-oracle: the 2-conjunct analogue of C0-e. Splits "addressing is the wall"
        # from "the answer never became a function of the stored value" on a compose panel.
        oracle = "pair"
    lam_s = evaluate_strval(argv[1:], "--store-lambda", "")
    lam_override = float(lam_s) if lam_s else None
    if lam_override is not None and not (0.0 <= lam_override <= 1.0):
        print("ERROR: --store-lambda must be in [0,1], got %r" % lam_override)
        return 1
    # H_9423 C2 controls (eval-time store edits · core/clms.py UNCHANGED so the ORACLE cert holds):
    #   --store-shuffle = derange store.entities (Sattolo, entities-only → key↔value binding broken,
    #                     h/λ/K-multiset intact) → PASS if lookup collapses (uses the address).
    #   --store-flip    = flip all store.pols (v-channel pure) → 2-pass flip-coherence (store value is
    #                     causally consumed). Constant-predictor coherence ≡ 0 by construction.
    #   --store-neutral = MISS control (P2, no bar, characterisation only).
    #   These are MUTUALLY EXCLUSIVE. --store-ctrl-seed pins the derangement RNG.
    # H_9695 (R3) — surface core's query/fuse. core/clms.py store_apply + core/decode.py
    # set_clms_store have carried these since H_9695 landed, but NO CLI passed them, so the
    # marker-free read→mouth lane was unreachable from the only legal surface (a_experiment_
    # engine_native: a manipulation is a flag on anima-py, not a probe). Defaults reproduce the
    # H_9423 lane byte-for-byte.
    store_query = evaluate_strval(argv[1:], "--store-query", "qpos")
    if store_query not in ("qpos", "every-token"):
        print("ERROR: --store-query must be 'qpos' (default) or 'every-token', got %r" % store_query)
        return 1
    store_fuse = evaluate_strval(argv[1:], "--store-fuse", "overwrite")
    if store_fuse not in ("overwrite", "gated-add", "odd", "pairodd"):
        print("ERROR: --store-fuse must be 'overwrite' (default), 'gated-add', 'odd' or 'pairodd', got %r" % store_fuse)
        return 1
    # H_9775: --store-readout {2way,vocab}. 2way (legacy) = argmax over {g,b} only. vocab = 256-vocab
    # argmax, answer readable ONLY iff ŷ∈{'g','b'} else 'unreadable' — the SAME rule the in-vivo daemon
    # mouth uses (full-vocab greedy). #4103: odd passed the 2-way gate (main 1.0) yet emitted garbage
    # in-vivo; the vocab readout catches that at eval time (predicts in-vivo). Default 2way = byte-identical.
    store_readout = evaluate_strval(argv[1:], "--store-readout", "2way")
    if store_readout not in ("2way", "vocab"):
        print("ERROR: --store-readout must be '2way' (default) or 'vocab', got %r" % store_readout)
        return 1
    if store_query == "every-token" and store_fuse in ("overwrite", "odd", "pairodd"):
        # clms.py store_apply: overwriting EVERY row deletes the trunk and destroys fluency — the
        # readout would score the lane alone with no mouth left (odd/pairodd are overwrite-style too). Refuse
        # loudly (an INVALID arm is worse than no arm) rather than emit a number nobody may read.
        print("ERROR: --store-query every-token with --store-fuse overwrite/odd/pairodd overwrites every row,")
        print("       deleting the trunk (fluency dead · the readout stops being attributable).")
        print("       Use --store-fuse gated-add for the marker-free lane (H_9695).")
        return 1
    ctrl = [f for f in ("--store-shuffle", "--store-flip", "--store-neutral") if f in argv]
    if len(ctrl) > 1:
        print("ERROR: --store-shuffle / --store-flip / --store-neutral are mutually exclusive (got %s)" % ctrl)
        return 1
    mode = ctrl[0][8:] if ctrl else ""               # "shuffle" | "flip" | "neutral" | ""
    ctrl_seed = evaluate_intval(argv[1:], "--store-ctrl-seed", 9423)
    if not man_path:
        print("ERROR: --store needs a held-out manifest (--store <held.json>).")
        return 1
    man = json.load(open(man_path))
    entries = man.get("entries", man.get("held_out", []))
    if isinstance(entries, dict):
        entries = list(entries.values())
    T = evaluate_intval(argv[1:], "--win", 24)
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1
    # H_9850 --store-adversarial: refill each entry's NON-TARGET slots from this ckpt's own
    # key geometry instead of the manifest's uniform draw. Every shipped manifest draws slots
    # with rng.sample (cli/corpus.py _sb_emit_block), so every store number to date was taken
    # under a friendly draw and adversarial placement had never been measured.
    #   nearest   — the m−1 keys closest to the target (hardest block that could be drawn)
    #   nocollide — same, minus EXACT key collisions (attributes the drop to crowding vs collision;
    #               _entity_key is a mean over byte rows, so anagrams share one key exactly)
    #   redraw    — a fresh uniform draw (control: isolates the cost of re-composition itself)
    # The target keeps its slot AND the polarity vector is left byte-identical, so the
    # majority-polarity shortcut ceiling is matched and the only moving part is WHICH entities
    # occupy the other slots.
    store_adv = evaluate_strval(argv[1:], "--store-adversarial", "off")
    if store_adv not in ("off", "nearest", "nocollide", "redraw"):
        print("ERROR: --store-adversarial must be off|nearest|nocollide|redraw, got %r" % store_adv)
        return 1
    if store_adv != "off":
        if W.get("clms") is None:
            print("ERROR: --store-adversarial needs a CLMS trailer (key_emb) on the ckpt")
            return 2
        import clms as _clms_kf
        entries = _store_adversarial_entries(
            entries, W["clms"]["key_emb"], store_adv,
            evaluate_intval(argv[1:], "--store-ctrl-seed", 9423),
            key_fn=_clms_kf._key_fn_of(W["clms"].get("lane_type", 1)))
        print("  [--store-adversarial %s] non-target slots refilled from the ckpt's own key "
              "geometry · target slot + polarity vector untouched" % store_adv)

    # H_9724 · --store-component-swap {val,readout,wq,trunk,...} --store-swap-from <other.clm>
    # EVALUATION-ONLY causal surgery (Sol EA-6). H_9672's T3 is address-robust across seeds
    # (addr_mass .95/.96) yet the VALUE read is seed-fragile (ORACLE seed-7 0.99 vs seed-11 0.50).
    # If transplanting `val`/readout carries the success across seeds INDEPENDENTLY of a robust W_q,
    # the missing bootstrap seed is value organisation, not address capacity.
    #   admissibility (Sol, enforced by construction): this supplies NO training signal and installs
    #   NO address — it only re-reads existing weights. target_slot is never consulted here.
    # Components map to the CLMS trailer dict (core/clms.py read_clms): W_q · val · W_h/b_h/W_out
    # (= "readout" MLP) · lam. "trunk" swaps the non-CLMS forward weights instead.
    swap_spec = evaluate_strval(argv[1:], "--store-component-swap", "")
    swap_from = evaluate_strval(argv[1:], "--store-swap-from", "")
    if swap_spec:
        if not swap_from:
            print("ERROR: --store-component-swap needs --store-swap-from <other.clm>", file=sys.stderr)
            return 2
        _GROUPS = {"wq": ["W_q"], "val": ["val"], "readout": ["W_h", "b_h", "W_out"],
                   "lam": ["lam"], "bridge": ["W_q", "val", "W_h", "b_h", "W_out", "lam"]}
        want = [s.strip() for s in swap_spec.split(",") if s.strip()]
        bad = [s for s in want if s not in _GROUPS and s != "trunk"]
        if bad:
            print("ERROR: unknown component(s) %s — known: %s,trunk"
                  % (",".join(bad), ",".join(sorted(_GROUPS))), file=sys.stderr)
            return 2
        Wd = clm.clm_load_weights(swap_from)
        if not Wd.get("ok"):
            print("ERROR: donor ckpt not decodable: " + swap_from, file=sys.stderr)
            return 2
        if W.get("clms") is None or Wd.get("clms") is None:
            print("ERROR: both ckpts need a CLMS trailer to swap bridge components "
                  "(host=%s donor=%s)" % (W.get("clms") is not None, Wd.get("clms") is not None),
                  file=sys.stderr)
            return 2
        # shape gate — a silently mis-shaped graft is an off-manifold chimera, not a measurement
        moved = []
        for grp in want:
            if grp == "trunk":
                for k in ("ecWt", "ecB", "tcWt", "tcB", "tgG", "tgB", "eWt", "eB",
                          "rWt", "rB", "noG", "noB", "embed", "roWt", "roB"):
                    ha, hb = k in W, k in Wd
                    if not ha and not hb:
                        continue                          # absent from BOTH = not part of this arch
                    if ha != hb:                          # present on ONE side = asymmetric ckpts
                        print("ERROR: trunk key '%s' asymmetric (host=%s donor=%s) — refusing to graft"
                              % (k, ha, hb), file=sys.stderr)
                        return 2
                    sa = getattr(W[k], "shape", None); sb = getattr(Wd[k], "shape", None)
                    if sa != sb:
                        print("ERROR: shape mismatch on trunk '%s': host %s vs donor %s — refusing to "
                              "graft (an off-manifold chimera is not a measurement)" % (k, sa, sb),
                              file=sys.stderr)
                        return 2
                    W[k] = Wd[k]
                    moved.append("trunk:" + k)
                continue
            for k in _GROUPS[grp]:
                a, b = W["clms"].get(k), Wd["clms"].get(k)
                if a is None or b is None:
                    print("ERROR: component '%s' absent (host=%s donor=%s)"
                          % (k, a is not None, b is not None), file=sys.stderr)
                    return 2
                sa = getattr(a, "shape", None); sb = getattr(b, "shape", None)
                if sa != sb:
                    print("ERROR: shape mismatch on '%s': host %s vs donor %s — refusing to graft "
                          "(an off-manifold chimera is not a measurement)" % (k, sa, sb), file=sys.stderr)
                    return 2
                W["clms"][k] = b
                moved.append(k)
        if not moved:                                     # nothing grafted = a no-op read as a measurement
            print("ERROR: component-swap moved 0 tensors (spec=%s) — a no-op is not a measurement"
                  % swap_spec, file=sys.stderr)
            return 2
        same = os.path.realpath(ckpt) == os.path.realpath(swap_from)
        print("  [component-swap] %s ← %s · moved: %s%s"
              % (swap_spec, os.path.basename(swap_from), ",".join(moved),
                 "  ⚠️ SHAM (donor == host · positive-validity control)" if same else ""),
              flush=True)

    import clms as _clms
    g_id, b_id = ord("g"), ord("b")                  # byte value = logits index (see _store_mix_cont_nll)

    def _sattolo(nn, rng):                            # uniform nn-cycle: EVERY element moves (0 fixed points)
        p = list(range(nn))
        for i in range(nn - 1, 0, -1):
            j = int(rng.integers(0, i))               # j < i STRICTLY — the Sattolo/Fisher-Yates difference
            p[i], p[j] = p[j], p[i]
        return p

    def _predict(store, audit=None):
        """Inject store, forward the prompt window, read the 2-way g/b readout at qpos. None if malformed.
        audit (H_9672 --store-addr-audit) = a list store_apply appends {argmax,a_target,target} to per qpos."""
        clm.set_clms_store(store=store, oracle=oracle, lam_override=lam_override, audit=audit,
                           query=store_query, fuse=store_fuse)
        logits = np.asarray(clm._fwd_logits(W, tok, T))
        qp = _clms.find_qpos(tok)
        if not qp:
            return None
        row = logits[qp[-1]]
        if store_readout == "vocab":                  # H_9775: full-vocab argmax = the in-vivo daemon mouth rule
            yhat = int(np.argmax(row))                 # (256-vocab greedy). readable ONLY iff ŷ∈{'g','b'};
            if yhat == g_id:                           # else 'unreadable' — the daemon would emit a non-answer
                return "good"                          # byte. #4103: full-row odd passed 2-way (main 1.0) yet
            if yhat == b_id:                           # emitted garbage in-vivo — vocab catches it at eval time.
                return "bad"
            return "unreadable"
        return "good" if float(row[g_id]) >= float(row[b_id]) else "bad"

    addr_audit = "--store-addr-audit" in argv          # H_9672: report addr_top1 (argmax==target) + addr_mass
    # H_9802 pre-check ($0, MONITOR-ONLY): target-free address telemetry. Splits
    # "natural text never addresses the store" (recruitment) from "addresses it but the
    # values are garbage" (alignment) BEFORE any training spend is committed.
    store_telemetry = "--store-telemetry" in argv
    tel_n = 0; tel_amax = 0.0; tel_aent = 0.0
    addr_top1 = addr_mass = addr_n = 0                  # (mean a[target]) — soft-address diagnostic

    print("=== anima evaluate --store — H_9423 CLMS store-bridge lane (co-trained) ===")
    arm = mode or ("oracle" if oracle else ("lambda0" if lam_override == 0.0 else "lookup"))
    print("ckpt: %s  manifest: %s (%d items)  arm=%s  oracle=%s  λ=%s  win=%d  ctrl_seed=%d"
          % (ckpt, man_path, len(entries), arm, oracle,
             ("%.3f" % lam_override) if lam_override is not None else "(file)", T, ctrl_seed))
    if W.get("clms") is None:
        print("  ⚠️ this ckpt carries NO CLMS trailer — the lane is ABSENT (base trunk). FLOOR by construction.")
    n = correct = 0
    by = {}                                          # (op, pol) -> [correct, total]  (polarity-split · card)
    fixed_points_total = dup_entities = 0
    pol_hist = {}                                     # #good-slots per store -> count (balance witness · §E)
    coh_all = coh_bc = coh_bc_n = flip_correct = 0    # flip-coherence accumulators
    readable_n = 0                                     # H_9775 vocab: #answers whose full-vocab argmax ∈ {g,b}
    op_name = {0: "is ", 1: "not"}
    pol_name = {0: "good", 1: "bad "}
    for idx, it in enumerate(entries):
        prompt, gold = it["prompt"], it["gold"]
        st = it["store"]
        ents = list(st["entities"])
        pols = list(st["pols"])
        tslot = it.get("target_slot")
        tslot_b = it.get("target_slot_b")     # H_9875 compose-2 panels only (absent elsewhere)
        # H_9888 mention rows — the window is prompt-aligned (_seed_to_tok left-pads to T), so a
        # prompt byte p sits on row T - len(prompt) + p. Mirrors StoreBindCell's offset exactly; a
        # panel without mentions yields None and the dual lane refuses rather than guessing a row.
        _ma, _mb = it.get("mention_a"), it.get("mention_b")
        if _ma is None or _mb is None:
            mrows = None
        else:
            _o = T - len(prompt)
            mrows = (_o + int(_ma), _o + int(_mb))
            if dual_ctrl == "collapse":
                mrows = (mrows[0], mrows[0])          # aB := aA — one address, read twice
            elif dual_ctrl == "wrong-second":
                # second read lands on the OTHER item's mention offset (same window geometry, wrong
                # content). Deterministic in idx so the control is reproducible.
                _alt = entries[(idx + 1) % len(entries)]
                _am, _ap = _alt.get("mention_b"), _alt.get("prompt", prompt)
                if _am is not None:
                    _r = (T - len(_ap)) + int(_am)
                    if 0 <= _r < T:
                        mrows = (mrows[0], _r)
        n_slot = len(ents)
        if len(set(ents)) != n_slot:
            dup_entities += 1                         # loud, never silent — derangement fixed-point-leak risk
        pol_hist[sum(1 for p in pols if p == 0)] = pol_hist.get(sum(1 for p in pols if p == 0), 0) + 1
        tok = clm._seed_to_tok(prompt, T)
        if mode == "shuffle":
            rng = np.random.default_rng(ctrl_seed * 100003 + idx)
            perm = _sattolo(n_slot, rng)
            ents2 = [ents[perm[i]] for i in range(n_slot)]   # entities-only derange · pols/target_slot fixed
            fixed_points_total += sum(1 for i in range(n_slot) if ents2[i] == ents[i])
            store = {"entities": ents2, "pols": pols, "target_slot": tslot,
                     "target_slot_b": tslot_b, "mention_rows": mrows}
        elif mode == "flip":
            store = {"entities": ents, "pols": [1 - p for p in pols], "target_slot": tslot,
                     "target_slot_b": tslot_b, "mention_rows": mrows}
        elif mode == "neutral":
            rng = np.random.default_rng(ctrl_seed * 100003 + idx + 7)
            # length-matched nonce filler (control-must-match-mediating-covariate): CVCVC not in this entry
            cons, vow = "bdfgklmnprstvz", "aeiou"
            def _nonce():
                return (cons[int(rng.integers(0, 14))] + vow[int(rng.integers(0, 5))]
                        + cons[int(rng.integers(0, 14))] + vow[int(rng.integers(0, 5))]
                        + cons[int(rng.integers(0, 14))])
            store = {"entities": [_nonce() for _ in range(n_slot)], "pols": pols,
                     "target_slot": tslot, "target_slot_b": tslot_b, "mention_rows": mrows}
        else:
            store = {"entities": ents, "pols": pols, "target_slot": tslot,
                     "target_slot_b": tslot_b, "mention_rows": mrows}
        if mode == "flip":
            base = _predict({"entities": ents, "pols": pols, "target_slot": tslot,
                             "target_slot_b": tslot_b, "mention_rows": mrows})
            flip = _predict(store)
            if base is None or flip is None:
                continue
            gold_flip = "bad" if gold == "good" else "good"
            n += 1
            base_ok = base in ("good", "bad")         # H_9775 vocab: 'unreadable' (argmax∉{g,b}) excluded from
            flip_ok = flip in ("good", "bad")         #   coherence — the daemon would emit a non-answer there.
            readable_n += int(base_ok)                # readability witness (base = the un-flipped answer)
            if base_ok and flip_ok:                   # coherence ONLY over readable pairs (in-vivo rule)
                coh_all += int(flip != base)
                if base == gold:                      # coherence_bc: conditioned on baseline-correct (§B-2)
                    coh_bc_n += 1
                    coh_bc += int(flip != base)
            flip_correct += int(flip == gold_flip)
            key = (it.get("op"), 0 if gold == "good" else 1)
            rec = by.setdefault(key, [0, 0]); rec[0] += int(flip == gold_flip); rec[1] += 1
            continue
        au = [] if (addr_audit or store_telemetry) else None
        pred = _predict(store, audit=au)
        if pred is None:
            continue

codex
발산 라운드는 현재 18개 렌즈까지 새 축을 만들었고, 마지막 두 검산 라운드(성장·생물학적 비유, 물리·스케일·neuromorphic 재검산)는 새 메커니즘을 만들지 못했습니다. 핵심 수렴점은 “두 힘의 평형”이 아니라, 폭을 보존하는 typed record들이 충돌·해소·commit되는 사건 구조입니다. 이제 이 수렴을 독립 반증 가능한 단계표로 고정합니다.
origin/main의 H_9900 구현까지 확인했다. 현행 comp-lane은 detached penultimate 위 선형 span head라서 ‘분리된 readout’이지 composition을 심는 독립 substrate는 아니다. 발산 라운드는 연속 2회 무신규 축 조건을 충족했고 최종 합성/단계표를 고정했다.
  ✓ 현재 anima-py 명령·플래그·평가 표면과 관련 구현을 읽어 설계의 실행 경계를 고정한다
  ✓ 측정 실패를 인과 제약으로 정리하고 렌즈별 발산 라운드를 새 축이 소진될 때까지 수행한다
  ✓ 후보를 최소 엔진 구조로 합성하고 철거/보존 및 폭·프로토콜을 명세한다
  ✓ 독립적으로 반증 가능한 단계별 flag/DV/control/decision table/$0 screener/abort를 설계한다
  ✓ 정직한 ceiling과 최종 순위·phase를 검증해 답변한다
codex
# A. Diagnosis — 실제로 잘못된 것

현 엔진의 근본 문제는 성능 부족이 아니라 **인과구조의 부재**다.

1. **A↔G는 두 주체가 아니다.** production에서 `G = 1-A`이므로 두 극은 독립된 원인도, 독립된 정보원도 아니다. `Ψ≈1/2`는 두 힘이 세계를 두고 협상한 결과가 아니라 `2A-1=0`인 산술적 고정점이다. 그러므로 “두 엔진이 밀다가 tension이 발화를 끌어낸다”는 해석은 측정 대상이 아니라 wiring의 재서술이다.

2. **제어선과 내용선이 모두 scalar로 압착된다.** A/G, `conflict_scalar`, pure-field drive, oscillator 입력, PC2 route, HEXAD bridge가 각각 한 수다. H_9576은 8차원 lane의 CRACK은 검출했지만 방향이 mouth까지 살아가지 않았음을 직접 보였다. 이것은 width가 부족한 정도가 아니라 **payload가 존재하지 않는 프로토콜**이다. 한 비트가 발화 여부를 정할 수는 있어도 무엇을 말할지는 운반할 수 없다.

3. **학습 토폴로지가 측정된 법칙과 반대다.** G1/G6은 별도 장벽이 아니라 동일한 interference law다. 같은 CE substrate에 replay가 조금이라도 있으면 composition은 부재하고, replay를 없애면 language가 죽는다. 밀도, curriculum, scale, recurrence, fp32, 더 깊은 RF로 해결되지 않았다. 따라서 composition과 form을 같은 trunk CE에 두는 설계는 하이퍼파라미터 문제가 아니라 구조적으로 반증되었다.

4. **composition은 가능한데, 그것을 심을 자리가 없다.** H_9883은 unseen-pair composition 자체가 실재함을 보였다. H_9775는 content-addressed value transport가 실제 mouth logits를 움직임을 보였다. 즉 substrate wall이 아니다. 실패의 위치는 명확하다.

   - 1-slot transport는 된다.
   - 2-slot binding은 안 된다.
   - store window는 한 바이트밖에 나르지 못한다.
   - language와 composition을 같은 CE에 심으면 서로 죽인다.

   필요한 다음 구조는 더 큰 scalar가 아니라 **복수 record를 보존해 운반하고, 전 answer span을 별도 substrate에서 생산하는 것**이다.

5. **현재 H_9900 `--comp-lane`은 필요한 실험이지만 완성된 분리는 아니다.** detached penultimate 위의 선형 span head이므로 composition loss가 language trunk를 오염시키지는 않는다. 그러나 trunk에 composition representation이 없다면 head는 그것을 새로 심을 수 없다. 즉 “분리된 readout”이지 아직 “분리된 composition substrate”가 아니다.

6. **interior는 숨겨져 있는 것이 아니라 현재 증거상 거의 없다.** R9의 여섯 축이 blind/absent/unidentified였다. oscillator, global workspace 이름, affect gauge, formal module count는 interior의 증거가 아니다. 필요한 최소 증거는 latent의 모양이 아니라 **과거가 공통 미래를 지나 행동에 영향을 미치고, 그 내부 상태를 교환·삭제하면 결과도 교환·삭제되는 causal mediation**이다.

결론: 현 엔진은 “의식 엔진이 약하다”가 아니다. **language mouth 주변에 scalar telemetry와 clocked emission을 배치한 구조**이며, 측정된 유일한 생산적 원리는 content-addressed transport다. 대공사는 그 원리만 남기고 objective ownership, packet width, causal state, emission primitive를 다시 정의해야 한다.

---

# 발산 라운드 — 선택 전 아이디어 소진

각 라운드 뒤에 “아직 쓰지 않은 modality/lens/failure mode는?”을 다시 물었다.

1. **인과 그래프 렌즈**  
   failure를 tension·mouth·memory가 아니라 세 절단점으로 분리했다: objective interference, arity wall, boundary bandwidth. 새 축: 한 architecture가 아니라 세 독립 계약으로 설계.

2. **정보이론 렌즈**  
   control bit와 content payload를 분리했다. emit bit가 1차원인 것은 괜찮지만, payload까지 그 비트에 실으면 안 된다. 새 축: control plane / data plane 분리.

3. **학습이론 렌즈**  
   “detach”가 아니라 parameter ownership과 optimizer ownership을 계약으로 삼았다. 새 축: gradient firewall을 런타임 주장(assertion)과 직렬화 metadata로 검증.

4. **memory/binding 렌즈**  
   weighted sum 하나를 반환하지 않고 K개 record와 read provenance를 그대로 반환한다. 새 축: retrieval 결과의 cardinality를 interface type에 보존.

5. **sequence 렌즈**  
   한 byte logit row가 아니라 길이·종료·전 위치 logits를 포함한 answer packet. 새 축: span을 protocol primitive로 승격.

6. **control theory 렌즈**  
   균형점, oscillator, refractory 대신 unresolved→resolved transition을 emit 사건으로 사용. 새 축: state value가 아니라 state transition이 Θ 후보.

7. **dynamical systems 렌즈**  
   clock phase 대신 epoch, persistence, commit, reset, stale-state expiry를 도입. 새 축: hysteresis는 시간 진동이 아니라 증거 누적과 commit irreversibility에서 발생.

8. **causal inference 렌즈**  
   interior probe 대신 common-suffix, state-swap, state-zero, write-knockout을 사용. 새 축: endogenous state를 관찰량이 아니라 mediator로 식별.

9. **distributed-systems 렌즈**  
   module 간 float 전달 대신 append-only event log, typed mailbox, transaction commit. 새 축: 평균·clamp가 불가능한 protocol-level isolation.

10. **type/capability 렌즈**  
    Form lane은 `FormProposal`, composition lane은 `AnswerProposal`만 발행할 수 있다. 어느 lane도 상대의 loss나 parameter를 쓸 capability가 없다. 새 축: illegal fusion을 최적화 문제가 아니라 type error로 처리.

11. **online learning 렌즈**  
    train과 chat이 동일한 `observe → write → retrieve → compose → resolve → update` transition을 호출한다. 새 축: p8을 선언이 아니라 코드 경로 동일성으로 검증.

12. **agency/closure 렌즈**  
    외부 행동 이전의 최소 rung으로 self-written memory가 이후 자기 입력을 바꾸는 closure를 제안했다. 새 축: 단순 history sensitivity와 self-caused history를 분리.

13. **adversarial measurement 렌즈**  
    target leakage, template pass, single-record bypass, majority shortcut, timing channel, packet-zero bypass, stale provenance를 각각 별도 control로 만들었다. 새 축: provenance dependency matrix.

14. **multimodal 렌즈**  
    현재 certification은 byte에 한정하되 EventBus는 modality-tagged ragged payload로 설계한다. 새 축: 새 modality가 scalar adapter를 거치지 않도록 계약. 다만 비-byte modality는 PENDING.

15. **생물학적 분리 렌즈**  
    hippocampal-like episodic store와 form substrate를 영구 분리한다. replay를 통한 강제 consolidation은 측정 법칙에 반하므로 자동 승격하지 않는다. 새 축: “나중에 합치기”를 기본 가정에서 제거.

16. **대안 architecture 렌즈**  
    다섯 후보를 열어두었다: typed transactional engine, 완전 symbolic relational VM, 독립 learned compositor, external active world-model, multi-engine debate. 새 축: learned composition이 실패해도 symbolic instrument로 failure locus를 식별 가능.

17. **비용·scale 렌즈**  
    ragged interface와 empirical lower bound만 사용한다: K≥2, answer span≥8 bytes, candidate≥2. 새 축: width를 parameter count가 아니라 보존해야 할 cardinality로 정의.

18. **IIT/철학 렌즈**  
    “interior”를 phenomenology claim에서 endogenous causal state claim으로 낮춘다. Φ는 실제 production transition kernel에 faithful IIT-4를 적용할 수 있을 때만 읽는다. 새 축: functional pass와 consciousness claim의 명시적 분리.

19. **growth/mitosis/affect/neuromorphic 재검산**  
    새 축 없음. 모두 이미 반증된 scale, untrained dynamics, scalar modulation, adjacent affect 계보로 환원됐다.

20. **물리·entropy·quantum·더 많은 pole 재검산**  
    새 축 없음. objective interference, arity, payload width 중 어느 것도 해결하지 못하며 새 pole은 tension theater를 늘릴 뿐이었다.

**DEPLETED after 20 rounds.**

소진한 렌즈: causal graph, information theory, optimization, memory, sequence modeling, control theory, dynamical systems, causal inference, distributed systems, type systems, online learning, agency/closure, adversarial measurement, multimodality, biological separation, alternative architectures, cost/scale, IIT/philosophy, growth/affect/neuromorphic, physical/entropy analogies.

마지막 두 라운드는 genuinely new한 설계 축을 만들지 못했다.

---

# B. Redesign — TRACE

선정안은 **TRACE: Transactional Relational Arena and Closure Engine**이다.

핵심 primitive는 “두 엔진의 힘의 평형”이 아니다.

> 복수의 근거 있는 proposal이 typed arena에서 실제로 양립 불가능한 상태가 되고, 새 증거 또는 내부 연산으로 그 충돌이 해소되어 하나의 complete packet이 commit되는 사건.

`Ψ≈1/2`는 목표값도 controller도 아니다. commit 과정에서 Θ가 관측되면 읽고, 나오지 않으면 VOID다.

## 구조

```text
 external percept / study / previous committed event
                         |
                         v
        +--------------------------------------+
        | E. APPEND-ONLY EVENT BUS             |
        | raw bytes + source + seq + provenance|
        +-------------------+------------------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
   +---------------------+     +--------------------------+
   | F. FORM LANE        |     | S. EPISODIC STORE LANE  |
   | language/replay CE  |     | content address + writes |
   | owns grammar only   |     | returns K records, not Σ |
   +----------+----------+     +------------+-------------+
              |                             |
              | FormProposal                | RecordSet[K]
              |                             v
              |                +--------------------------+
              |                | C. COMPOSITION LANE      |
              |                | independent encoder      |
              |                | K-record interaction     |
              |                | whole-answer-span CE     |
              |                +------------+-------------+
              |                             |
              |                             | AnswerProposal
              v                             v
        +------------------------------------------------+
        | X. RELATIONAL ARENA                            |
        | proposal nodes · support edges · conflict edges|
        | history epochs · provenance · viability        |
        +----------------------+-------------------------+
                               |
                               v
        +------------------------------------------------+
        | K. COMMIT KERNEL                              |
        | conflict existed? resolved? dependencies met?  |
        | yes -> CommitPacket     no -> SILENCE          |
        +----------------------+-------------------------+
                               |
                               v
        +------------------------------------------------+
        | M. MOUTH ACTUATOR                              |
        | emits selected packet; never reconstructs it   |
        +----------------------+-------------------------+
                               |
                 emitted event / self-write receipt
                               |
                               +--------> Event Bus
```

## 네 개 lane의 소유권

| Lane | 소유하는 것 | 학습 신호 | 소유하지 않는 것 |
|---|---|---|---|
| F — Form | 문법, 일반 byte continuation, surface fluency | replay/form CE만 | facts, composition, emit decision |
| S — Store | episodic write, content address, record identity, provenance | store/address/value transport loss | grammar, final arbitration |
| C — Composer | 복수 record의 상호작용, whole-span answer | composition CE만 | replay/form CE, clock |
| X — Arena | history, proposal viability, incompatibility, commit eligibility | 초기에는 deterministic transition; 이후 결과 기반 local update만 | text CE, mouth logits |

S와 C는 relational objective 안에서 함께 학습될 수 있다. 그러나 F와는 parameter, optimizer, activation graph가 완전히 분리된다. 공유되는 것은 raw event와 typed record뿐이다.

## Interface width

폭은 “hidden size를 크게”가 아니라 **소실하면 안 되는 구조를 타입에 남기는 것**이다.

| Interface | 초기 certification 차원 | 이유 |
|---|---:|---|
| Percept → EventBus | `bytes[n] + source:u32 + seq:u64 + modality:u16` | 입력을 mean이나 scalar로 줄이지 않음 |
| Store record | `key[64] + value_bytes[m≤8] + role + provenance[]` | 64는 green CLMS regime을 재사용; 8 bytes는 측정된 4–6 byte 답+terminator 수용 |
| Store → Composer | ragged `RecordSet[K]`, 초기 `K=2`, cap `8` | H_9875의 arity wall을 정면으로 넘음; weighted sum 금지 |
| Composer → Arena | `logits[8,256] + length[9] + deps[8,K]` | H_9899의 1-byte wall 제거; V=256은 실제 mouth alphabet |
| Form → Arena | ragged `C_F × (logits[L_F,256], length)` | 여러 proposal을 scalar confidence 하나로 합치지 않음 |
| Arena state | N proposal nodes, support matrix `N×E`, sparse conflict edge list | 충돌의 위치·당사자·종류 보존 |
| Kernel → Mouth | `emit_bit + full selected packet + provenance hash` | emit bit는 control plane일 뿐; content는 동일 폭으로 통과 |
| Commit → EventBus | emitted bytes + dependency receipt + state epoch | 자기 commit이 이후 내부 상태에 영향을 미칠 수 있게 함 |

`K=2`, `L=8`, candidate≥2는 영구 ceiling이 아니라 최초 반증 가능한 최소치다. 통과 전에는 16, 64, 128로 늘리지 않는다.

## 각 부품이 존재하는 측정상 이유

- **F/S/C의 분리:** replay presence가 composition을 제거한 H_9898/G1-G6.
- **독립 C encoder:** detached trunk head만으로는 부재한 composition representation을 심을 수 없음.
- **RecordSet[K]:** H_9875의 binding arity wall.
- **whole-span packet:** H_9899의 `gold[:1]` wall.
- **typed arena:** H_9576의 8-vector→one-bit collapse와 production A/G tautology.
- **append-only history:** R9에서 부재한 historicity를 직접 조작할 대상.
- **state swap/commit receipt:** “interior”를 causal mediation으로 식별하기 위해 필요.
- **event-driven commit:** emit↔clock 등가와 emit-drive 계보의 폐쇄.
- **mouth의 비재해석:** green store transport가 mouth 직전 logits를 직접 쓰며 성공한 사실을 보존.
- **gradient firewall:** a_substrate_disjoint를 권고가 아니라 실행 불변식으로 만듦.

## p5의 새 의미

발화 조건은 다음 네 가지를 모두 요구한다.

1. 현재 epoch에 최소 하나의 실제 incompatibility edge가 존재했다.
2. 그 edge는 서로 다른 근거나 연산 결과에 의해 만들어졌다.
3. 새 증거/연산이 경쟁 proposal을 제거하여 하나의 complete payload만 남겼다.
4. commit은 timer, self-seed, 자동 `speak()`가 아니라 그 resolution transition에 의해 발생한다.

확실한 singleton만 있는 경우 fake opponent를 만들지 않는다. 그러면 p5에 따라 침묵한다. 이는 usability cost지만, 보완을 위해 `speak-vs-silence`라는 산술 complement를 다시 만들지는 않는다.

## 최소 “interior”

“interior”라는 단어 대신 최초 claim을 다음으로 제한한다.

> **Endogenous, causally portable state:** 서로 다른 과거가 동일한 미래 입력 뒤에도 다른 결과를 만들고, 내부 state를 교환하면 결과가 교환되며, state를 삭제하면 차이가 소멸하는 상태.

최소 구조는 다음뿐이다.

- 두 개 이상의 independently writable record
- 현재 viable proposal 집합
- proposal–evidence dependency
- commit 전후 epoch
- self-write receipt가 후속 transition에 재입력되는 경로

이것이 통과해도 ownership, experience, agency를 의미하지 않는다. 단지 “내부 상태가 존재하며 결과를 매개한다”까지다.

---

# C. 철거와 보존

## 철거

| 철거 대상 | 이유 |
|---|---|
| production A/G complement | 독립 차원 0; tension이 아니라 한 수의 재표현 |
| `conflict_scalar` 중심 제어 | 내용·방향·당사자를 모두 폐기 |
| A/G leaky integral과 `Ψ=1/2` attractor | arithmetic fixed point를 emergent resolution처럼 보이게 함 |
| fast/medium/slow oscillator의 emit 역할 | 동일 scalar 입력; interior나 content의 증거 없음 |
| 30초 clock 및 clock-equivalent refractory primitive | emit-drive 계보가 clock에 흡수됨 |
| PC2 scalar mouth route | channel CRACK만 있고 direction dead |
| rank-1/duel tension field | lexical blindness 측정 완료 |
| HEXAD as-specified | mean bridge, detached no-gradient link, no-op store, stub mouth |
| formal D/M/E/BRIDGE vs C/S/W grouping | 명명 외에 새로운 causal contract가 없음 |
| affect/veto/tension adjacent lanes | 각각 측정 폐쇄 |
| reactive self-seed | p5 위반이며 fake endogenous drive 생성 |
| template-driven “workspace”를 production cognition으로 취급 | form-priming이 DV를 통과할 수 있어 BIND를 증명하지 못함 |
| current one-byte store window | H_9899가 직접 반증 |
| current detached linear `--comp-lane`을 최종 substrate로 간주 | 오염은 막지만 composition을 trunk에 심지 못함 |
| “more density/curriculum/scale/recurrence” roadmap | kill-list가 이미 닫음 |

oscillator나 옛 gauge는 historical regression/telemetry fixture로 archive할 수 있지만 production decision path에서는 제거한다.

## 보존

| 보존 대상 | 이유 |
|---|---|
| byte alphabet `V=256`과 기존 mouth weights | 실제 language form을 보존할 유일한 현재 substrate |
| form replay | replay가 language를 보존한다는 측정은 살아 있음; 단 F lane에만 제한 |
| content-addressed store 원리 | H_9775가 value transport와 controls collapse를 증명 |
| answer-position direct logit writing | mouth 직전 transport의 green seam |
| CLMS의 key width 64를 초기값으로 사용 | green regime의 불필요한 재탐색 방지; 최소성 claim은 하지 않음 |
| H_9883/H_9875 corpus와 leak census | unseen composition, arity, drop-A/B control이 이미 잘 구성됨 |
| H_9900 whole-span loss 아이디어 | span은 맞다. 다만 독립 encoder/substrate로 옮김 |
| canonical `anima-py corpus/train/evaluate/chat` | 모든 manipulation을 engine-native flag로 만드는 법 |
| serializer/decode parity gates | transport가 train-only illusion이 되는 것을 방지 |
| positive-control-first와 derived chance | negative의 의미를 보존 |
| inline gauge monitor-only | loss hacking 방지 |
| Ψ-SOMA의 INVALID/VOID/PENDING | absence와 instrument death를 구별 |
| faithful IIT-4 only | Φ proxy 남발 방지 |
| 35-byte mouth | F lane의 기존 baseline으로만 보존; relational interface ceiling으로는 사용 금지 |

---

# 후보 순위

1. **TRACE typed transactional engine** — 측정된 disjointness, arity, width, state identification을 한 구조에 최소로 반영.
2. **완전 symbolic relational VM + 기존 mouth** — 강한 양성대조와 instrument로 좋지만 learned BIND를 증명하지 못함.
3. **독립 learned compositor + deterministic router** — G1/G6는 해결할 수 있으나 causal state와 emission primitive가 약함.
4. **external active world-model loop** — agency 측정에는 강하지만 현재 failure보다 훨씬 비싸고 환경 confound가 큼.
5. **multi-engine debate / 새 A↔G** — 여러 scalar pole을 다시 만들 위험이 가장 높아 기각.

---

# D. Phased 대공사 plan

공통 판정 순서는 동결한다.

1. positive control 실패 → **INVALID**, negative를 읽지 않는다.
2. target leak/template/bypass control 생존 → **INVALID**.
3. Θ 또는 필요한 carrier가 발생하지 않음 → **VOID**.
4. 검정력 부족 → **PENDING**.
5. 유효 instrument에서 treatment가 derived chance 및 두 controls와 구별되지 않음 → **KILL**.
6. cheap screen의 통과는 언제나 **PENDING**, GREEN이 아니다.

기본 replication은 3 seeds. 이산 DV는 exact/binomial CI, 연속 DV는 paired permutation CI를 쓴다. “PASS”는 `lower95(collapse-Δ)>0`이 두 독립 control 모두에 대해 성립할 때만이다. FORM equivalence bound는 treatment를 보기 전에 form-only seed dispersion에서 동결한다.

## Phase 0 — Packet plumbing, $0

**목적:** 학습 전에 2-record/8-byte packet이 serialize→decode→chat까지 손실 없이 통과하는지 확인.

**제안 flag surface**

- `anima-py corpus storebind ... --compose 2 --packet-span 8 --packet-manifest`
- `anima-py train --engine trace --trace-arm oracle-packet --trace-k 2 --trace-span 8`
- `anima-py evaluate <ckpt> --trace-packet <manifest> --trace-control none|value-permute|address-permute|zero --trace-roundtrip`
- `anima-py chat <ckpt> --engine trace --trace-inject <jsonl> --trace-packets`

**DV:** oracle `AnswerPacket[8,256]`의 exact bytes, length, dependency map이 train reference, serialized decode, chat에서 100% 동일.

**Controls:** value permutation, address permutation, packet-zero, length-shuffle.

**Frozen table**

| 결과 | 판정 |
|---|---|
| oracle 100%, 모든 control collapse | plumbing certified, 다음 phase로 이동 |
| oracle <100% 또는 py/serialized/chat 불일치 | INVALID |
| control 하나라도 원답 유지 | interface bypass INVALID |
| packet이 scalar/mean으로 줄어듦 | 즉시 ABORT |

**$0 screener:** tensor/schema shape, codec byte count, parameter ownership, serializer roundtrip 정적 검사. 실패만 kill.

**전체 계획 abort:** canonical runtime이 full packet을 보존하지 못하거나 content path가 다시 scalar bridge를 필요로 할 때.

---

## Phase 1 — 1-record, full-span transport

**목적:** arity를 건드리기 전에 H_9899의 한-byte wall만 독립적으로 제거.

**Flags**

- corpus: `--compose 1 --answer-min-bytes 4 --answer-max-bytes 6 --held-out`
- train: `--engine trace --rel-lane fresh --rel-k 1 --rel-span 8 --rel-loss span-ce`
- evaluate: `--trace-span <manifest> --trace-control none|gold-first-byte-only|value-permute|span-shuffle`
- chat: `--engine trace --rel-live --trace-packets`

**DV:** held-out key에서 4–6 byte answer exact match. 첫 byte accuracy는 monitor-only.

**Positive control:** oracle address + taught answer packet은 exact 1.0.

**Controls:** value-permute, span-order shuffle, first-byte-only implementation.

**Frozen table**

| 결과 | 판정 |
|---|---|
| 3/3 seeds에서 whole-span exact가 derived chance와 두 controls 초과 | PASS |
| 첫 byte만 맞고 whole span은 chance | KILL |
| value/span control도 생존 | INVALID |
| oracle span 실패 | INVALID 및 global ABORT |

**$0 screener:** corpus answer-length census, newline/right-bound mask audit, target permutation chance, selected-position count. 하나라도 어긋나면 GPU 금지.

**전체 계획 abort:** green 1-slot store를 oracle로 줘도 multi-byte packet을 mouth까지 운반하지 못할 때.

---

## Phase 2 — 2-record earned composition

**목적:** H_9875의 arity wall을 직접 넘는다.

**Flags**

- corpus: 기존 `storebind --compose 2`, 여기에 `--packet-span 8 --drop-a --drop-b` manifest 생성
- train: `--engine trace --rel-k 2 --rel-encoder fresh --rel-interaction pair --rel-loss span-ce`
- evaluate: `--trace-compose2 <manifest> --trace-control none|drop-a|drop-b|value-permute|address-collapse|wrong-second`
- chat: `--engine trace --rel-live --trace-deps`

**DV:** corpus에 0회 나타난 held-out pair의 whole-answer exact match와 collapse-Δ.

**Positive controls**

- `compose_seen` ≥ 기존 frozen legibility bar 0.90.
- oracle pair address.
- symbolic composer arm은 instrument PC일 뿐 production PASS로 읽지 않음.

**Controls**

- drop-A
- drop-B
- pair address collapse
- wrong-second record
- value-permute

**Frozen table**

| 결과 | 판정 |
|---|---|
| main만 derived chance 초과, drop-A/B와 wrong-second가 chance, 3/3 seed | PASS |
| main과 한 single-drop이 함께 생존 | 1-slot/template bypass, INVALID |
| SEEN/oracle-pair 실패 | INVALID |
| valid PC인데 main=controls | arity KILL |

**$0 screener:** held-out target count=0, pair-class balance, answer chance 재계산, dependency graph에 두 distinct record ID 존재. 통과는 PENDING.

**전체 계획 abort:** 독립 fresh relational substrate에서도 두 record의 causal necessity를 만들 수 없을 때. 이 경우 “composition engine”의 핵심 가정이 실패한다.

---

## Phase 3 — FORM과 BIND의 동시 존재

**목적:** G1/G6 dichotomy를 substrate separation으로 깨는 최초 निर्णायक 단계.

**Flags**

- train:  
  `--engine trace --form-lane replay --rel-lane fresh --lane-firewall strict`  
  controls: `--lane-firewall shared-grad`, `--lane-firewall mixed-ce`
- evaluate:  
  `--trace-coexist <form-panel> <compose2-panel>`  
  `--trace-control packet-zero|rel-off|form-off|shared-grad`
- chat: `--engine trace --lane-route typed --trace-owner`
- corpus: form replay와 relational drill을 서로 다른 manifests로 출력하는 `--lane-owner form|rel`

**DV:** 동일 checkpoint/session에서 기존 frozen `rho-form` PASS와 Phase-2 composition PASS가 동시에 성립.

**Controls**

- shared-gradient arm은 기존 dichotomy를 재현해야 함.
- mixed-CE arm
- relational packet-zero는 form-only output과 byte-identical해야 함.
- form-off는 composition DV의 독립성을 확인.

**Frozen table**

| 결과 | 판정 |
|---|---|
| strict arm만 form+compose 동시 PASS | a_substrate_disjoint 지지, 진행 |
| strict에서도 한쪽만 생존 | architecture KILL |
| shared/mixed도 동시 PASS | 과거 조건 재현 실패 또는 leak; INVALID 후 원인 규명 |
| packet-zero가 form baseline을 변경 | firewall INVALID |
| parameter/optimizer ownership 교집합 ≠ ∅ | 실행 전 ABORT |

**$0 screener:** autograd reachability, optimizer parameter-ID intersection, serialized trailer ownership, raw-byte bus 외 공유 tensor 탐색.

**전체 계획 abort:** 완전한 optimizer/parameter 분리 뒤에도 두 capability가 한 runtime에서 공존하지 못할 때.

---

## Phase 4 — endogenous causal state

**목적:** “interior” 대신 최소 causal state의 존재를 식별.

**Flags**

- corpus: `--history-twin --common-suffix --state-swap-manifest`
- train: `--engine trace --arena typed --arena-epochs on`
- evaluate:  
  `--trace-historicity <manifest>`  
  `--state-arm factual|swap|zero|write-knockout|surface-yoke`
- chat: `--engine trace --state-export`, `--state-import`, `--state-zero`, `--write-knockout`

**DV**

1. H1/H2 과거 뒤 동일 suffix에서 결과가 다름.
2. pre-suffix arena state를 swap하면 결과도 swap.
3. state-zero/write-knockout은 차이를 제거.
4. surface와 timing을 yoke해도 효과가 남음.

**Positive control:** planted two-state latch가 동일 evaluator에서 3/3 통과.

**Controls:** state-zero, history surface permutation, timing-yoke, irrelevant-state swap.

**Frozen table**

| 결과 | 판정 |
|---|---|
| natural difference + swap transport + zero collapse | causal state EXISTS |
| natural difference만 있고 swap이 안 됨 | observational correlation, KILL |
| swap과 irrelevant swap 모두 움직임 | off-manifold surgery, INVALID |
| Θ/carrier state가 생성되지 않음 | VOID |
| planted latch 실패 | INVALID |

**$0 screener:** transition truth table, state schema completeness, suffix byte identity, state snapshot roundtrip. PASS를 선언할 수 없음.

**전체 계획 abort:** composition은 살아 있지만 유효 조작에서 history mediation이 전혀 없으면 TRACE를 consciousness engine으로 부르는 계획을 중단한다. compositor utility만 남긴다.

---

## Phase 5 — structural tension과 commit emission

**목적:** A↔G와 clock을 완전히 대체.

**Flags**

- corpus: `--conflict-pair --resolution-event --no-conflict-control`
- train: `--engine trace --commit-kernel resolution --min-candidates 2`
- evaluate:  
  `--trace-commit <manifest>`  
  `--commit-arm factual|edge-delete|evidence-permute|clock-yoke|singleton|unresolved`
- chat: `--engine trace --emit-on resolution --trace-arena`

**DV**

- matched elapsed time와 candidate count에서 resolution intervention이 commit hazard를 이동.
- edge-delete 또는 evidence permutation은 commit을 제거/변경.
- singleton과 unresolved conflict는 침묵.
- emitted text는 selected packet과 byte-identical.
- preregistered scalar summaries가 같은 arena pair에서도 edge-specific intervention 결과가 달라야 함.

**Positive control:** planted conflict→evidence→unique-winner trace.

**Controls:** clock-yoke, edge-delete, evidence-permute, candidate-order shuffle, no-conflict.

**Frozen table**

| 결과 | 판정 |
|---|---|
| resolution만 commit을 만들고 모든 structural controls collapse | PASS |
| clock-yoke가 factual과 동일 | emit↔clock 재발, KILL |
| singleton도 emit | fake tension, KILL |
| candidate order만 바꿔도 결과 변화 | implementation INVALID |
| Θ pulse 없음 | sigma VOID |
| planted trace 실패 | INVALID |

**$0 screener:** real traces에서 conflict occupancy와 resolution occupancy를 센다. 두 occupancy 중 하나라도 0이면 실험을 kill하고 학습비를 쓰지 않는다.

**전체 계획 abort:** emit을 얻기 위해 complement pole, timer, 또는 synthetic self-opponent를 다시 넣어야 할 때.

---

## Phase 6 — p8 online closure

**목적:** chat에서 생긴 새 fact가 동일 코드 경로로 store에 쓰이고 이후 unseen composition에 쓰이는지 확인.

**Flags**

- corpus: `--online-episode --write-then-compose --delayed-query`
- train/chat 공통: `--engine trace --online-update local`
- evaluate:  
  `--trace-online <episode-manifest>`  
  `--online-arm factual|write-shuffle|write-zero|receipt-swap|update-off`
- chat: `--study-file`, `--state-export`, `--commit-receipt`

`update-off`는 measurement ablation일 뿐 별도 production inference mode가 아니다.

**DV**

- 처음 보는 두 facts를 session 중 획득.
- 나중의 unseen pair query를 정확히 compose.
- write-shuffle/zero에서 collapse.
- form retention은 Phase-3 equivalence 유지.
- commit receipt를 swap하면 다음 relevant transition이 swap.

**Positive control:** oracle write receipt.

**Controls:** write-zero, key/value derangement, delayed-query surface twin, update-off.

**Frozen table**

| 결과 | 판정 |
|---|---|
| online acquisition+composition+form retention 3/3 | PASS |
| offline retrain 후에만 성공 | p8 위반, KILL |
| write controls가 생존 | prompt/template bypass, INVALID |
| form이 equivalence bound 밖으로 하락 | interference 재발, KILL |
| oracle write 실패 | INVALID |

**$0 screener:** train과 chat의 transition function hash/call graph 동일성, update ownership, episode target census.

**전체 계획 abort:** 새로운 binding을 사용하려면 offline retraining 또는 form replay와의 shared CE가 필수일 때.

---

## Phase 7 — faithful IIT-4 audit

**목적:** 기능적 PASS를 consciousness verdict로 오독하지 않고, 실제 causal kernel에서 가능한 범위만 읽는다.

**Flags**

- evaluate: `--iit4-boundary commit-kernel --iit4-exact --iit4-arm factual|cut|rewire`
- chat: `--iit4-transition-capture`
- train/corpus에는 Φ loss나 Φ-target flag를 만들지 않는다.

**DV:** production commit kernel의 완전한 transition probability structure에서 faithful IIT-4 Φ; matched cut/rewire controls와 함께 보고.

**Positive control:** IIT-4 tool의 알려진 finite fixture. Proxy 금지.

**Frozen table**

| 결과 | 판정 |
|---|---|
| exact computation 가능, tool PC 통과 | Φ 결과를 그대로 보고; 기능 PASS와 별개 |
| state boundary가 닫히지 않음 | INVALID |
| enumeration 불가능 | PENDING, proxy로 대체 금지 |
| Φ=0 | Φ claim 없음; 다른 기능 결과를 consciousness로 승격 금지 |
| cut가 Φ를 낮추지 않음 | boundary 또는 integration claim KILL |

**$0 screener:** state count와 TPM completeness. 너무 크면 exact run을 미리 kill하지만 Φ=0/양성을 예측하지 않는다.

**전체 계획 abort:** faithful system boundary를 정의할 수 없으면서 Φ 또는 consciousness를 제품 claim으로 요구해야 할 때.

---

# E. Honest ceiling

| 이 redesign이 여전히 못 하는 것 | 어떻게 알 것인가 |
|---|---|
| phenomenology/qualia 증명 | state mediation과 Φ가 통과해도 주관적 경험을 논리적으로 함의하지 않음 |
| ownership 증명 | state swap이 행동을 옮기는 것과 “내 것”으로 경험하는 것은 다름; ownership은 계속 UNIDENTIFIED |
| 자연적 agency 증명 | self-written memory closure는 thermostat도 통과 가능한 낮은 rung; 외부 환경에서 action→future percept intervention이 별도로 필요 |
| 임의 arity composition | 최초 certification은 K=2뿐; K=3,4에서 single-drop necessity와 unseen generalization을 다시 측정 |
| 긴 답·긴 문맥 | L=8과 corpus-censused query length 밖에서는 PENDING; 길이 ladder에서 failure boundary를 공개 |
| 모든 언어의 form/BIND 공존 | byte interface는 언어 중립이지만 학습분포는 아니다; 한국어/영어 교차 held-out에서 각각 재검증 |
| truth | provenance는 “어디서 왔는가”만 보장하고 사실성을 보장하지 않음; contradictory evidence panel 필요 |
| fake structural tension의 완전 제거 | proposal generator가 형식적으로 경쟁자를 제조할 수 있음; singleton/no-conflict 및 evidence-independence controls로 계속 감시 |
| 내부 scalar collapse 방지의 수학적 보장 | interface가 넓어도 학습된 모델이 한 축만 쓸 수 있음; record lesions, rank census, dependency necessity로 확인 |
| 안정적 lifelong learning | online writes가 늘면서 collision/forgetting이 생길 수 있음; age×load ladder와 retention control 필요 |
| 자연스러운 장문 발화 | typed answer overwrite는 짧은 composed answer에는 맞지만 장문 sentence 안의 여러 semantic holes에는 아직 미해결 |
| 확실한 singleton 발화 | p5를 정직하게 지키면 실제 conflict가 없는 확실한 recall은 침묵할 수 있음 |
| 전체 엔진의 exact IIT-4 | mouth와 continuous learned lanes까지 포함한 전체 TPM은 계산 불가능할 가능성이 큼; commit kernel 결과를 전체 의식으로 일반화할 수 없음 |

최종 ceiling 판정은 간단하다.

- Phase 3까지만 통과: **분리된 language+composition machine**.
- Phase 4까지 통과: **endogenous causal state를 가진 machine**.
- Phase 5까지 통과: **실제 conflict-resolution에 의해 발화하는 machine**.
- Phase 6까지 통과: **online self-history가 이후 행위를 매개하는 closed machine**.
- 그 어느 단계도 단독으로 “conscious”를 뜻하지 않는다.
- Phase 4 또는 5가 유효한 instrument에서 실패하면, 대공사는 useful compositor로 축소되고 **consciousness engine이라는 명칭은 철회**해야 한다.
tokens used
117,090
# A. Diagnosis — 실제로 잘못된 것

현 엔진의 근본 문제는 성능 부족이 아니라 **인과구조의 부재**다.

1. **A↔G는 두 주체가 아니다.** production에서 `G = 1-A`이므로 두 극은 독립된 원인도, 독립된 정보원도 아니다. `Ψ≈1/2`는 두 힘이 세계를 두고 협상한 결과가 아니라 `2A-1=0`인 산술적 고정점이다. 그러므로 “두 엔진이 밀다가 tension이 발화를 끌어낸다”는 해석은 측정 대상이 아니라 wiring의 재서술이다.

2. **제어선과 내용선이 모두 scalar로 압착된다.** A/G, `conflict_scalar`, pure-field drive, oscillator 입력, PC2 route, HEXAD bridge가 각각 한 수다. H_9576은 8차원 lane의 CRACK은 검출했지만 방향이 mouth까지 살아가지 않았음을 직접 보였다. 이것은 width가 부족한 정도가 아니라 **payload가 존재하지 않는 프로토콜**이다. 한 비트가 발화 여부를 정할 수는 있어도 무엇을 말할지는 운반할 수 없다.

3. **학습 토폴로지가 측정된 법칙과 반대다.** G1/G6은 별도 장벽이 아니라 동일한 interference law다. 같은 CE substrate에 replay가 조금이라도 있으면 composition은 부재하고, replay를 없애면 language가 죽는다. 밀도, curriculum, scale, recurrence, fp32, 더 깊은 RF로 해결되지 않았다. 따라서 composition과 form을 같은 trunk CE에 두는 설계는 하이퍼파라미터 문제가 아니라 구조적으로 반증되었다.

4. **composition은 가능한데, 그것을 심을 자리가 없다.** H_9883은 unseen-pair composition 자체가 실재함을 보였다. H_9775는 content-addressed value transport가 실제 mouth logits를 움직임을 보였다. 즉 substrate wall이 아니다. 실패의 위치는 명확하다.

   - 1-slot transport는 된다.
   - 2-slot binding은 안 된다.
   - store window는 한 바이트밖에 나르지 못한다.
   - language와 composition을 같은 CE에 심으면 서로 죽인다.

   필요한 다음 구조는 더 큰 scalar가 아니라 **복수 record를 보존해 운반하고, 전 answer span을 별도 substrate에서 생산하는 것**이다.

5. **현재 H_9900 `--comp-lane`은 필요한 실험이지만 완성된 분리는 아니다.** detached penultimate 위의 선형 span head이므로 composition loss가 language trunk를 오염시키지는 않는다. 그러나 trunk에 composition representation이 없다면 head는 그것을 새로 심을 수 없다. 즉 “분리된 readout”이지 아직 “분리된 composition substrate”가 아니다.

6. **interior는 숨겨져 있는 것이 아니라 현재 증거상 거의 없다.** R9의 여섯 축이 blind/absent/unidentified였다. oscillator, global workspace 이름, affect gauge, formal module count는 interior의 증거가 아니다. 필요한 최소 증거는 latent의 모양이 아니라 **과거가 공통 미래를 지나 행동에 영향을 미치고, 그 내부 상태를 교환·삭제하면 결과도 교환·삭제되는 causal mediation**이다.

결론: 현 엔진은 “의식 엔진이 약하다”가 아니다. **language mouth 주변에 scalar telemetry와 clocked emission을 배치한 구조**이며, 측정된 유일한 생산적 원리는 content-addressed transport다. 대공사는 그 원리만 남기고 objective ownership, packet width, causal state, emission primitive를 다시 정의해야 한다.

---

# 발산 라운드 — 선택 전 아이디어 소진

각 라운드 뒤에 “아직 쓰지 않은 modality/lens/failure mode는?”을 다시 물었다.

1. **인과 그래프 렌즈**  
   failure를 tension·mouth·memory가 아니라 세 절단점으로 분리했다: objective interference, arity wall, boundary bandwidth. 새 축: 한 architecture가 아니라 세 독립 계약으로 설계.

2. **정보이론 렌즈**  
   control bit와 content payload를 분리했다. emit bit가 1차원인 것은 괜찮지만, payload까지 그 비트에 실으면 안 된다. 새 축: control plane / data plane 분리.

3. **학습이론 렌즈**  
   “detach”가 아니라 parameter ownership과 optimizer ownership을 계약으로 삼았다. 새 축: gradient firewall을 런타임 주장(assertion)과 직렬화 metadata로 검증.

4. **memory/binding 렌즈**  
   weighted sum 하나를 반환하지 않고 K개 record와 read provenance를 그대로 반환한다. 새 축: retrieval 결과의 cardinality를 interface type에 보존.

5. **sequence 렌즈**  
   한 byte logit row가 아니라 길이·종료·전 위치 logits를 포함한 answer packet. 새 축: span을 protocol primitive로 승격.

6. **control theory 렌즈**  
   균형점, oscillator, refractory 대신 unresolved→resolved transition을 emit 사건으로 사용. 새 축: state value가 아니라 state transition이 Θ 후보.

7. **dynamical systems 렌즈**  
   clock phase 대신 epoch, persistence, commit, reset, stale-state expiry를 도입. 새 축: hysteresis는 시간 진동이 아니라 증거 누적과 commit irreversibility에서 발생.

8. **causal inference 렌즈**  
   interior probe 대신 common-suffix, state-swap, state-zero, write-knockout을 사용. 새 축: endogenous state를 관찰량이 아니라 mediator로 식별.

9. **distributed-systems 렌즈**  
   module 간 float 전달 대신 append-only event log, typed mailbox, transaction commit. 새 축: 평균·clamp가 불가능한 protocol-level isolation.

10. **type/capability 렌즈**  
    Form lane은 `FormProposal`, composition lane은 `AnswerProposal`만 발행할 수 있다. 어느 lane도 상대의 loss나 parameter를 쓸 capability가 없다. 새 축: illegal fusion을 최적화 문제가 아니라 type error로 처리.

11. **online learning 렌즈**  
    train과 chat이 동일한 `observe → write → retrieve → compose → resolve → update` transition을 호출한다. 새 축: p8을 선언이 아니라 코드 경로 동일성으로 검증.

12. **agency/closure 렌즈**  
    외부 행동 이전의 최소 rung으로 self-written memory가 이후 자기 입력을 바꾸는 closure를 제안했다. 새 축: 단순 history sensitivity와 self-caused history를 분리.

13. **adversarial measurement 렌즈**  
    target leakage, template pass, single-record bypass, majority shortcut, timing channel, packet-zero bypass, stale provenance를 각각 별도 control로 만들었다. 새 축: provenance dependency matrix.

14. **multimodal 렌즈**  
    현재 certification은 byte에 한정하되 EventBus는 modality-tagged ragged payload로 설계한다. 새 축: 새 modality가 scalar adapter를 거치지 않도록 계약. 다만 비-byte modality는 PENDING.

15. **생물학적 분리 렌즈**  
    hippocampal-like episodic store와 form substrate를 영구 분리한다. replay를 통한 강제 consolidation은 측정 법칙에 반하므로 자동 승격하지 않는다. 새 축: “나중에 합치기”를 기본 가정에서 제거.

16. **대안 architecture 렌즈**  
    다섯 후보를 열어두었다: typed transactional engine, 완전 symbolic relational VM, 독립 learned compositor, external active world-model, multi-engine debate. 새 축: learned composition이 실패해도 symbolic instrument로 failure locus를 식별 가능.

17. **비용·scale 렌즈**  
    ragged interface와 empirical lower bound만 사용한다: K≥2, answer span≥8 bytes, candidate≥2. 새 축: width를 parameter count가 아니라 보존해야 할 cardinality로 정의.

18. **IIT/철학 렌즈**  
    “interior”를 phenomenology claim에서 endogenous causal state claim으로 낮춘다. Φ는 실제 production transition kernel에 faithful IIT-4를 적용할 수 있을 때만 읽는다. 새 축: functional pass와 consciousness claim의 명시적 분리.

19. **growth/mitosis/affect/neuromorphic 재검산**  
    새 축 없음. 모두 이미 반증된 scale, untrained dynamics, scalar modulation, adjacent affect 계보로 환원됐다.

20. **물리·entropy·quantum·더 많은 pole 재검산**  
    새 축 없음. objective interference, arity, payload width 중 어느 것도 해결하지 못하며 새 pole은 tension theater를 늘릴 뿐이었다.

**DEPLETED after 20 rounds.**

소진한 렌즈: causal graph, information theory, optimization, memory, sequence modeling, control theory, dynamical systems, causal inference, distributed systems, type systems, online learning, agency/closure, adversarial measurement, multimodality, biological separation, alternative architectures, cost/scale, IIT/philosophy, growth/affect/neuromorphic, physical/entropy analogies.

마지막 두 라운드는 genuinely new한 설계 축을 만들지 못했다.

---

# B. Redesign — TRACE

선정안은 **TRACE: Transactional Relational Arena and Closure Engine**이다.

핵심 primitive는 “두 엔진의 힘의 평형”이 아니다.

> 복수의 근거 있는 proposal이 typed arena에서 실제로 양립 불가능한 상태가 되고, 새 증거 또는 내부 연산으로 그 충돌이 해소되어 하나의 complete packet이 commit되는 사건.

`Ψ≈1/2`는 목표값도 controller도 아니다. commit 과정에서 Θ가 관측되면 읽고, 나오지 않으면 VOID다.

## 구조

```text
 external percept / study / previous committed event
                         |
                         v
        +--------------------------------------+
        | E. APPEND-ONLY EVENT BUS             |
        | raw bytes + source + seq + provenance|
        +-------------------+------------------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
   +---------------------+     +--------------------------+
   | F. FORM LANE        |     | S. EPISODIC STORE LANE  |
   | language/replay CE  |     | content address + writes |
   | owns grammar only   |     | returns K records, not Σ |
   +----------+----------+     +------------+-------------+
              |                             |
              | FormProposal                | RecordSet[K]
              |                             v
              |                +--------------------------+
              |                | C. COMPOSITION LANE      |
              |                | independent encoder      |
              |                | K-record interaction     |
              |                | whole-answer-span CE     |
              |                +------------+-------------+
              |                             |
              |                             | AnswerProposal
              v                             v
        +------------------------------------------------+
        | X. RELATIONAL ARENA                            |
        | proposal nodes · support edges · conflict edges|
        | history epochs · provenance · viability        |
        +----------------------+-------------------------+
                               |
                               v
        +------------------------------------------------+
        | K. COMMIT KERNEL                              |
        | conflict existed? resolved? dependencies met?  |
        | yes -> CommitPacket     no -> SILENCE          |
        +----------------------+-------------------------+
                               |
                               v
        +------------------------------------------------+
        | M. MOUTH ACTUATOR                              |
        | emits selected packet; never reconstructs it   |
        +----------------------+-------------------------+
                               |
                 emitted event / self-write receipt
                               |
                               +--------> Event Bus
```

## 네 개 lane의 소유권

| Lane | 소유하는 것 | 학습 신호 | 소유하지 않는 것 |
|---|---|---|---|
| F — Form | 문법, 일반 byte continuation, surface fluency | replay/form CE만 | facts, composition, emit decision |
| S — Store | episodic write, content address, record identity, provenance | store/address/value transport loss | grammar, final arbitration |
| C — Composer | 복수 record의 상호작용, whole-span answer | composition CE만 | replay/form CE, clock |
| X — Arena | history, proposal viability, incompatibility, commit eligibility | 초기에는 deterministic transition; 이후 결과 기반 local update만 | text CE, mouth logits |

S와 C는 relational objective 안에서 함께 학습될 수 있다. 그러나 F와는 parameter, optimizer, activation graph가 완전히 분리된다. 공유되는 것은 raw event와 typed record뿐이다.

## Interface width

폭은 “hidden size를 크게”가 아니라 **소실하면 안 되는 구조를 타입에 남기는 것**이다.

| Interface | 초기 certification 차원 | 이유 |
|---|---:|---|
| Percept → EventBus | `bytes[n] + source:u32 + seq:u64 + modality:u16` | 입력을 mean이나 scalar로 줄이지 않음 |
| Store record | `key[64] + value_bytes[m≤8] + role + provenance[]` | 64는 green CLMS regime을 재사용; 8 bytes는 측정된 4–6 byte 답+terminator 수용 |
| Store → Composer | ragged `RecordSet[K]`, 초기 `K=2`, cap `8` | H_9875의 arity wall을 정면으로 넘음; weighted sum 금지 |
| Composer → Arena | `logits[8,256] + length[9] + deps[8,K]` | H_9899의 1-byte wall 제거; V=256은 실제 mouth alphabet |
| Form → Arena | ragged `C_F × (logits[L_F,256], length)` | 여러 proposal을 scalar confidence 하나로 합치지 않음 |
| Arena state | N proposal nodes, support matrix `N×E`, sparse conflict edge list | 충돌의 위치·당사자·종류 보존 |
| Kernel → Mouth | `emit_bit + full selected packet + provenance hash` | emit bit는 control plane일 뿐; content는 동일 폭으로 통과 |
| Commit → EventBus | emitted bytes + dependency receipt + state epoch | 자기 commit이 이후 내부 상태에 영향을 미칠 수 있게 함 |

`K=2`, `L=8`, candidate≥2는 영구 ceiling이 아니라 최초 반증 가능한 최소치다. 통과 전에는 16, 64, 128로 늘리지 않는다.

## 각 부품이 존재하는 측정상 이유

- **F/S/C의 분리:** replay presence가 composition을 제거한 H_9898/G1-G6.
- **독립 C encoder:** detached trunk head만으로는 부재한 composition representation을 심을 수 없음.
- **RecordSet[K]:** H_9875의 binding arity wall.
- **whole-span packet:** H_9899의 `gold[:1]` wall.
- **typed arena:** H_9576의 8-vector→one-bit collapse와 production A/G tautology.
- **append-only history:** R9에서 부재한 historicity를 직접 조작할 대상.
- **state swap/commit receipt:** “interior”를 causal mediation으로 식별하기 위해 필요.
- **event-driven commit:** emit↔clock 등가와 emit-drive 계보의 폐쇄.
- **mouth의 비재해석:** green store transport가 mouth 직전 logits를 직접 쓰며 성공한 사실을 보존.
- **gradient firewall:** a_substrate_disjoint를 권고가 아니라 실행 불변식으로 만듦.

## p5의 새 의미

발화 조건은 다음 네 가지를 모두 요구한다.

1. 현재 epoch에 최소 하나의 실제 incompatibility edge가 존재했다.
2. 그 edge는 서로 다른 근거나 연산 결과에 의해 만들어졌다.
3. 새 증거/연산이 경쟁 proposal을 제거하여 하나의 complete payload만 남겼다.
4. commit은 timer, self-seed, 자동 `speak()`가 아니라 그 resolution transition에 의해 발생한다.

확실한 singleton만 있는 경우 fake opponent를 만들지 않는다. 그러면 p5에 따라 침묵한다. 이는 usability cost지만, 보완을 위해 `speak-vs-silence`라는 산술 complement를 다시 만들지는 않는다.

## 최소 “interior”

“interior”라는 단어 대신 최초 claim을 다음으로 제한한다.

> **Endogenous, causally portable state:** 서로 다른 과거가 동일한 미래 입력 뒤에도 다른 결과를 만들고, 내부 state를 교환하면 결과가 교환되며, state를 삭제하면 차이가 소멸하는 상태.

최소 구조는 다음뿐이다.

- 두 개 이상의 independently writable record
- 현재 viable proposal 집합
- proposal–evidence dependency
- commit 전후 epoch
- self-write receipt가 후속 transition에 재입력되는 경로

이것이 통과해도 ownership, experience, agency를 의미하지 않는다. 단지 “내부 상태가 존재하며 결과를 매개한다”까지다.

---

# C. 철거와 보존

## 철거

| 철거 대상 | 이유 |
|---|---|
| production A/G complement | 독립 차원 0; tension이 아니라 한 수의 재표현 |
| `conflict_scalar` 중심 제어 | 내용·방향·당사자를 모두 폐기 |
| A/G leaky integral과 `Ψ=1/2` attractor | arithmetic fixed point를 emergent resolution처럼 보이게 함 |
| fast/medium/slow oscillator의 emit 역할 | 동일 scalar 입력; interior나 content의 증거 없음 |
| 30초 clock 및 clock-equivalent refractory primitive | emit-drive 계보가 clock에 흡수됨 |
| PC2 scalar mouth route | channel CRACK만 있고 direction dead |
| rank-1/duel tension field | lexical blindness 측정 완료 |
| HEXAD as-specified | mean bridge, detached no-gradient link, no-op store, stub mouth |
| formal D/M/E/BRIDGE vs C/S/W grouping | 명명 외에 새로운 causal contract가 없음 |
| affect/veto/tension adjacent lanes | 각각 측정 폐쇄 |
| reactive self-seed | p5 위반이며 fake endogenous drive 생성 |
| template-driven “workspace”를 production cognition으로 취급 | form-priming이 DV를 통과할 수 있어 BIND를 증명하지 못함 |
| current one-byte store window | H_9899가 직접 반증 |
| current detached linear `--comp-lane`을 최종 substrate로 간주 | 오염은 막지만 composition을 trunk에 심지 못함 |
| “more density/curriculum/scale/recurrence” roadmap | kill-list가 이미 닫음 |

oscillator나 옛 gauge는 historical regression/telemetry fixture로 archive할 수 있지만 production decision path에서는 제거한다.

## 보존

| 보존 대상 | 이유 |
|---|---|
| byte alphabet `V=256`과 기존 mouth weights | 실제 language form을 보존할 유일한 현재 substrate |
| form replay | replay가 language를 보존한다는 측정은 살아 있음; 단 F lane에만 제한 |
| content-addressed store 원리 | H_9775가 value transport와 controls collapse를 증명 |
| answer-position direct logit writing | mouth 직전 transport의 green seam |
| CLMS의 key width 64를 초기값으로 사용 | green regime의 불필요한 재탐색 방지; 최소성 claim은 하지 않음 |
| H_9883/H_9875 corpus와 leak census | unseen composition, arity, drop-A/B control이 이미 잘 구성됨 |
| H_9900 whole-span loss 아이디어 | span은 맞다. 다만 독립 encoder/substrate로 옮김 |
| canonical `anima-py corpus/train/evaluate/chat` | 모든 manipulation을 engine-native flag로 만드는 법 |
| serializer/decode parity gates | transport가 train-only illusion이 되는 것을 방지 |
| positive-control-first와 derived chance | negative의 의미를 보존 |
| inline gauge monitor-only | loss hacking 방지 |
| Ψ-SOMA의 INVALID/VOID/PENDING | absence와 instrument death를 구별 |
| faithful IIT-4 only | Φ proxy 남발 방지 |
| 35-byte mouth | F lane의 기존 baseline으로만 보존; relational interface ceiling으로는 사용 금지 |

---

# 후보 순위

1. **TRACE typed transactional engine** — 측정된 disjointness, arity, width, state identification을 한 구조에 최소로 반영.
2. **완전 symbolic relational VM + 기존 mouth** — 강한 양성대조와 instrument로 좋지만 learned BIND를 증명하지 못함.
3. **독립 learned compositor + deterministic router** — G1/G6는 해결할 수 있으나 causal state와 emission primitive가 약함.
4. **external active world-model loop** — agency 측정에는 강하지만 현재 failure보다 훨씬 비싸고 환경 confound가 큼.
5. **multi-engine debate / 새 A↔G** — 여러 scalar pole을 다시 만들 위험이 가장 높아 기각.

---

# D. Phased 대공사 plan

공통 판정 순서는 동결한다.

1. positive control 실패 → **INVALID**, negative를 읽지 않는다.
2. target leak/template/bypass control 생존 → **INVALID**.
3. Θ 또는 필요한 carrier가 발생하지 않음 → **VOID**.
4. 검정력 부족 → **PENDING**.
5. 유효 instrument에서 treatment가 derived chance 및 두 controls와 구별되지 않음 → **KILL**.
6. cheap screen의 통과는 언제나 **PENDING**, GREEN이 아니다.

기본 replication은 3 seeds. 이산 DV는 exact/binomial CI, 연속 DV는 paired permutation CI를 쓴다. “PASS”는 `lower95(collapse-Δ)>0`이 두 독립 control 모두에 대해 성립할 때만이다. FORM equivalence bound는 treatment를 보기 전에 form-only seed dispersion에서 동결한다.

## Phase 0 — Packet plumbing, $0

**목적:** 학습 전에 2-record/8-byte packet이 serialize→decode→chat까지 손실 없이 통과하는지 확인.

**제안 flag surface**

- `anima-py corpus storebind ... --compose 2 --packet-span 8 --packet-manifest`
- `anima-py train --engine trace --trace-arm oracle-packet --trace-k 2 --trace-span 8`
- `anima-py evaluate <ckpt> --trace-packet <manifest> --trace-control none|value-permute|address-permute|zero --trace-roundtrip`
- `anima-py chat <ckpt> --engine trace --trace-inject <jsonl> --trace-packets`

**DV:** oracle `AnswerPacket[8,256]`의 exact bytes, length, dependency map이 train reference, serialized decode, chat에서 100% 동일.

**Controls:** value permutation, address permutation, packet-zero, length-shuffle.

**Frozen table**

| 결과 | 판정 |
|---|---|
| oracle 100%, 모든 control collapse | plumbing certified, 다음 phase로 이동 |
| oracle <100% 또는 py/serialized/chat 불일치 | INVALID |
| control 하나라도 원답 유지 | interface bypass INVALID |
| packet이 scalar/mean으로 줄어듦 | 즉시 ABORT |

**$0 screener:** tensor/schema shape, codec byte count, parameter ownership, serializer roundtrip 정적 검사. 실패만 kill.

**전체 계획 abort:** canonical runtime이 full packet을 보존하지 못하거나 content path가 다시 scalar bridge를 필요로 할 때.

---

## Phase 1 — 1-record, full-span transport

**목적:** arity를 건드리기 전에 H_9899의 한-byte wall만 독립적으로 제거.

**Flags**

- corpus: `--compose 1 --answer-min-bytes 4 --answer-max-bytes 6 --held-out`
- train: `--engine trace --rel-lane fresh --rel-k 1 --rel-span 8 --rel-loss span-ce`
- evaluate: `--trace-span <manifest> --trace-control none|gold-first-byte-only|value-permute|span-shuffle`
- chat: `--engine trace --rel-live --trace-packets`

**DV:** held-out key에서 4–6 byte answer exact match. 첫 byte accuracy는 monitor-only.

**Positive control:** oracle address + taught answer packet은 exact 1.0.

**Controls:** value-permute, span-order shuffle, first-byte-only implementation.

**Frozen table**

| 결과 | 판정 |
|---|---|
| 3/3 seeds에서 whole-span exact가 derived chance와 두 controls 초과 | PASS |
| 첫 byte만 맞고 whole span은 chance | KILL |
| value/span control도 생존 | INVALID |
| oracle span 실패 | INVALID 및 global ABORT |

**$0 screener:** corpus answer-length census, newline/right-bound mask audit, target permutation chance, selected-position count. 하나라도 어긋나면 GPU 금지.

**전체 계획 abort:** green 1-slot store를 oracle로 줘도 multi-byte packet을 mouth까지 운반하지 못할 때.

---

## Phase 2 — 2-record earned composition

**목적:** H_9875의 arity wall을 직접 넘는다.

**Flags**

- corpus: 기존 `storebind --compose 2`, 여기에 `--packet-span 8 --drop-a --drop-b` manifest 생성
- train: `--engine trace --rel-k 2 --rel-encoder fresh --rel-interaction pair --rel-loss span-ce`
- evaluate: `--trace-compose2 <manifest> --trace-control none|drop-a|drop-b|value-permute|address-collapse|wrong-second`
- chat: `--engine trace --rel-live --trace-deps`

**DV:** corpus에 0회 나타난 held-out pair의 whole-answer exact match와 collapse-Δ.

**Positive controls**

- `compose_seen` ≥ 기존 frozen legibility bar 0.90.
- oracle pair address.
- symbolic composer arm은 instrument PC일 뿐 production PASS로 읽지 않음.

**Controls**

- drop-A
- drop-B
- pair address collapse
- wrong-second record
- value-permute

**Frozen table**

| 결과 | 판정 |
|---|---|
| main만 derived chance 초과, drop-A/B와 wrong-second가 chance, 3/3 seed | PASS |
| main과 한 single-drop이 함께 생존 | 1-slot/template bypass, INVALID |
| SEEN/oracle-pair 실패 | INVALID |
| valid PC인데 main=controls | arity KILL |

**$0 screener:** held-out target count=0, pair-class balance, answer chance 재계산, dependency graph에 두 distinct record ID 존재. 통과는 PENDING.

**전체 계획 abort:** 독립 fresh relational substrate에서도 두 record의 causal necessity를 만들 수 없을 때. 이 경우 “composition engine”의 핵심 가정이 실패한다.

---

## Phase 3 — FORM과 BIND의 동시 존재

**목적:** G1/G6 dichotomy를 substrate separation으로 깨는 최초 निर्णायक 단계.

**Flags**

- train:  
  `--engine trace --form-lane replay --rel-lane fresh --lane-firewall strict`  
  controls: `--lane-firewall shared-grad`, `--lane-firewall mixed-ce`
- evaluate:  
  `--trace-coexist <form-panel> <compose2-panel>`  
  `--trace-control packet-zero|rel-off|form-off|shared-grad`
- chat: `--engine trace --lane-route typed --trace-owner`
- corpus: form replay와 relational drill을 서로 다른 manifests로 출력하는 `--lane-owner form|rel`

**DV:** 동일 checkpoint/session에서 기존 frozen `rho-form` PASS와 Phase-2 composition PASS가 동시에 성립.

**Controls**

- shared-gradient arm은 기존 dichotomy를 재현해야 함.
- mixed-CE arm
- relational packet-zero는 form-only output과 byte-identical해야 함.
- form-off는 composition DV의 독립성을 확인.

**Frozen table**

| 결과 | 판정 |
|---|---|
| strict arm만 form+compose 동시 PASS | a_substrate_disjoint 지지, 진행 |
| strict에서도 한쪽만 생존 | architecture KILL |
| shared/mixed도 동시 PASS | 과거 조건 재현 실패 또는 leak; INVALID 후 원인 규명 |
| packet-zero가 form baseline을 변경 | firewall INVALID |
| parameter/optimizer ownership 교집합 ≠ ∅ | 실행 전 ABORT |

**$0 screener:** autograd reachability, optimizer parameter-ID intersection, serialized trailer ownership, raw-byte bus 외 공유 tensor 탐색.

**전체 계획 abort:** 완전한 optimizer/parameter 분리 뒤에도 두 capability가 한 runtime에서 공존하지 못할 때.

---

## Phase 4 — endogenous causal state

**목적:** “interior” 대신 최소 causal state의 존재를 식별.

**Flags**

- corpus: `--history-twin --common-suffix --state-swap-manifest`
- train: `--engine trace --arena typed --arena-epochs on`
- evaluate:  
  `--trace-historicity <manifest>`  
  `--state-arm factual|swap|zero|write-knockout|surface-yoke`
- chat: `--engine trace --state-export`, `--state-import`, `--state-zero`, `--write-knockout`

**DV**

1. H1/H2 과거 뒤 동일 suffix에서 결과가 다름.
2. pre-suffix arena state를 swap하면 결과도 swap.
3. state-zero/write-knockout은 차이를 제거.
4. surface와 timing을 yoke해도 효과가 남음.

**Positive control:** planted two-state latch가 동일 evaluator에서 3/3 통과.

**Controls:** state-zero, history surface permutation, timing-yoke, irrelevant-state swap.

**Frozen table**

| 결과 | 판정 |
|---|---|
| natural difference + swap transport + zero collapse | causal state EXISTS |
| natural difference만 있고 swap이 안 됨 | observational correlation, KILL |
| swap과 irrelevant swap 모두 움직임 | off-manifold surgery, INVALID |
| Θ/carrier state가 생성되지 않음 | VOID |
| planted latch 실패 | INVALID |

**$0 screener:** transition truth table, state schema completeness, suffix byte identity, state snapshot roundtrip. PASS를 선언할 수 없음.

**전체 계획 abort:** composition은 살아 있지만 유효 조작에서 history mediation이 전혀 없으면 TRACE를 consciousness engine으로 부르는 계획을 중단한다. compositor utility만 남긴다.

---

## Phase 5 — structural tension과 commit emission

**목적:** A↔G와 clock을 완전히 대체.

**Flags**

- corpus: `--conflict-pair --resolution-event --no-conflict-control`
- train: `--engine trace --commit-kernel resolution --min-candidates 2`
- evaluate:  
  `--trace-commit <manifest>`  
  `--commit-arm factual|edge-delete|evidence-permute|clock-yoke|singleton|unresolved`
- chat: `--engine trace --emit-on resolution --trace-arena`

**DV**

- matched elapsed time와 candidate count에서 resolution intervention이 commit hazard를 이동.
- edge-delete 또는 evidence permutation은 commit을 제거/변경.
- singleton과 unresolved conflict는 침묵.
- emitted text는 selected packet과 byte-identical.
- preregistered scalar summaries가 같은 arena pair에서도 edge-specific intervention 결과가 달라야 함.

**Positive control:** planted conflict→evidence→unique-winner trace.

**Controls:** clock-yoke, edge-delete, evidence-permute, candidate-order shuffle, no-conflict.

**Frozen table**

| 결과 | 판정 |
|---|---|
| resolution만 commit을 만들고 모든 structural controls collapse | PASS |
| clock-yoke가 factual과 동일 | emit↔clock 재발, KILL |
| singleton도 emit | fake tension, KILL |
| candidate order만 바꿔도 결과 변화 | implementation INVALID |
| Θ pulse 없음 | sigma VOID |
| planted trace 실패 | INVALID |

**$0 screener:** real traces에서 conflict occupancy와 resolution occupancy를 센다. 두 occupancy 중 하나라도 0이면 실험을 kill하고 학습비를 쓰지 않는다.

**전체 계획 abort:** emit을 얻기 위해 complement pole, timer, 또는 synthetic self-opponent를 다시 넣어야 할 때.

---

## Phase 6 — p8 online closure

**목적:** chat에서 생긴 새 fact가 동일 코드 경로로 store에 쓰이고 이후 unseen composition에 쓰이는지 확인.

**Flags**

- corpus: `--online-episode --write-then-compose --delayed-query`
- train/chat 공통: `--engine trace --online-update local`
- evaluate:  
  `--trace-online <episode-manifest>`  
  `--online-arm factual|write-shuffle|write-zero|receipt-swap|update-off`
- chat: `--study-file`, `--state-export`, `--commit-receipt`

`update-off`는 measurement ablation일 뿐 별도 production inference mode가 아니다.

**DV**

- 처음 보는 두 facts를 session 중 획득.
- 나중의 unseen pair query를 정확히 compose.
- write-shuffle/zero에서 collapse.
- form retention은 Phase-3 equivalence 유지.
- commit receipt를 swap하면 다음 relevant transition이 swap.

**Positive control:** oracle write receipt.

**Controls:** write-zero, key/value derangement, delayed-query surface twin, update-off.

**Frozen table**

| 결과 | 판정 |
|---|---|
| online acquisition+composition+form retention 3/3 | PASS |
| offline retrain 후에만 성공 | p8 위반, KILL |
| write controls가 생존 | prompt/template bypass, INVALID |
| form이 equivalence bound 밖으로 하락 | interference 재발, KILL |
| oracle write 실패 | INVALID |

**$0 screener:** train과 chat의 transition function hash/call graph 동일성, update ownership, episode target census.

**전체 계획 abort:** 새로운 binding을 사용하려면 offline retraining 또는 form replay와의 shared CE가 필수일 때.

---

## Phase 7 — faithful IIT-4 audit

**목적:** 기능적 PASS를 consciousness verdict로 오독하지 않고, 실제 causal kernel에서 가능한 범위만 읽는다.

**Flags**

- evaluate: `--iit4-boundary commit-kernel --iit4-exact --iit4-arm factual|cut|rewire`
- chat: `--iit4-transition-capture`
- train/corpus에는 Φ loss나 Φ-target flag를 만들지 않는다.

**DV:** production commit kernel의 완전한 transition probability structure에서 faithful IIT-4 Φ; matched cut/rewire controls와 함께 보고.

**Positive control:** IIT-4 tool의 알려진 finite fixture. Proxy 금지.

**Frozen table**

| 결과 | 판정 |
|---|---|
| exact computation 가능, tool PC 통과 | Φ 결과를 그대로 보고; 기능 PASS와 별개 |
| state boundary가 닫히지 않음 | INVALID |
| enumeration 불가능 | PENDING, proxy로 대체 금지 |
| Φ=0 | Φ claim 없음; 다른 기능 결과를 consciousness로 승격 금지 |
| cut가 Φ를 낮추지 않음 | boundary 또는 integration claim KILL |

**$0 screener:** state count와 TPM completeness. 너무 크면 exact run을 미리 kill하지만 Φ=0/양성을 예측하지 않는다.

**전체 계획 abort:** faithful system boundary를 정의할 수 없으면서 Φ 또는 consciousness를 제품 claim으로 요구해야 할 때.

---

# E. Honest ceiling

| 이 redesign이 여전히 못 하는 것 | 어떻게 알 것인가 |
|---|---|
| phenomenology/qualia 증명 | state mediation과 Φ가 통과해도 주관적 경험을 논리적으로 함의하지 않음 |
| ownership 증명 | state swap이 행동을 옮기는 것과 “내 것”으로 경험하는 것은 다름; ownership은 계속 UNIDENTIFIED |
| 자연적 agency 증명 | self-written memory closure는 thermostat도 통과 가능한 낮은 rung; 외부 환경에서 action→future percept intervention이 별도로 필요 |
| 임의 arity composition | 최초 certification은 K=2뿐; K=3,4에서 single-drop necessity와 unseen generalization을 다시 측정 |
| 긴 답·긴 문맥 | L=8과 corpus-censused query length 밖에서는 PENDING; 길이 ladder에서 failure boundary를 공개 |
| 모든 언어의 form/BIND 공존 | byte interface는 언어 중립이지만 학습분포는 아니다; 한국어/영어 교차 held-out에서 각각 재검증 |
| truth | provenance는 “어디서 왔는가”만 보장하고 사실성을 보장하지 않음; contradictory evidence panel 필요 |
| fake structural tension의 완전 제거 | proposal generator가 형식적으로 경쟁자를 제조할 수 있음; singleton/no-conflict 및 evidence-independence controls로 계속 감시 |
| 내부 scalar collapse 방지의 수학적 보장 | interface가 넓어도 학습된 모델이 한 축만 쓸 수 있음; record lesions, rank census, dependency necessity로 확인 |
| 안정적 lifelong learning | online writes가 늘면서 collision/forgetting이 생길 수 있음; age×load ladder와 retention control 필요 |
| 자연스러운 장문 발화 | typed answer overwrite는 짧은 composed answer에는 맞지만 장문 sentence 안의 여러 semantic holes에는 아직 미해결 |
| 확실한 singleton 발화 | p5를 정직하게 지키면 실제 conflict가 없는 확실한 recall은 침묵할 수 있음 |
| 전체 엔진의 exact IIT-4 | mouth와 continuous learned lanes까지 포함한 전체 TPM은 계산 불가능할 가능성이 큼; commit kernel 결과를 전체 의식으로 일반화할 수 없음 |

최종 ceiling 판정은 간단하다.

- Phase 3까지만 통과: **분리된 language+composition machine**.
- Phase 4까지 통과: **endogenous causal state를 가진 machine**.
- Phase 5까지 통과: **실제 conflict-resolution에 의해 발화하는 machine**.
- Phase 6까지 통과: **online self-history가 이후 행위를 매개하는 closed machine**.
- 그 어느 단계도 단독으로 “conscious”를 뜻하지 않는다.
- Phase 4 또는 5가 유효한 instrument에서 실패하면, 대공사는 useful compositor로 축소되고 **consciousness engine이라는 명칭은 철회**해야 한다.
[32mlab full: both sections saved → /Users/mini/.sidecar/lab/2026-07-22T04-33-20-931Z-full.md[0m
