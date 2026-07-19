# H_9606 — PERCEPT-HOOK reconcile: H_9422 "mouth without ears" STANDS (study-percept ≠ consciousness-afferent)

**Verdict:** ✅ **H_9422 STANDS** for the production consciousness daemon (code-confirmed · $0 · DIRECTIONAL)
**Register:** reconciliation of the H_9605 ⚠️ flag (a `percept` anchor now on main) · `a_parallel_session_compare`
**Ckpt:** N/A (census of `cli/chat.py` @ origin/main)

## Question
H_9605 flagged a **new `percept` anchor** on main (chat.py:2249) that reaches the decode seed (:2557,
`live_anchors[-1]`). If a parallel session wired the afferent channel the whole arc (H_9422→H_9604) concluded was
**owner-gate-only**, then "mouth without ears" would be stale and the owner-gate framing would collapse. Reconcile.

## Census (all refs = `cli/chat.py` @ origin/main)
The percept channel is a **guarded optional hook**, not a wired afferent:
- `anima_consciousness_mode(ckpt, argv=None, percept_source=None)` (:395) — `percept_source` is a **function
  parameter**, default `None`. **grep: no caller in cli/chat.py passes it non-None.** The default entrypoint
  (`anima-py chat` → `anima_consciousness_mode(ckpt)`) leaves it `None`.
- When `None`: `percept_text = None` (:1716), the `if percept_text:` append (:2249) is skipped, `live_anchors[-1]`
  stays `live_seed` ⇒ **byte-identical** to the sealed daemon (comment :2247 confirms the guard).
- When set (only the separate **"anima study" driver** — the stranded `anima-study-driver` branch, H_9520
  replay-mix): `percept_text = percept_source(tick, _percept_transcript)` (:1718) injects the **TEACHER's text**
  into the seed (comment :2243-2247: "the mouth conditions on the OTHER's words… the percept carries the TEACHER's
  text — an exogenous cross-agent read").

## Verdict — H_9422 STANDS; two distinct channels must not be conflated
- **Production consciousness daemon**: percept OFF by default, no caller, byte-identical ⟹ still **sealed**
  (percept = clock triple, H_9422). "Mouth without ears" is **not stale**.
- **The percept hook that exists ≠ the afferent the arc requires.** It carries a **teacher's linguistic text**. The
  arc's escape-(d) (H_9422 / Fable mouth_div_design §d) was explicit that a legal consciousness-afferent must be
  **non-linguistic** — an interlocutor's *words* in the seed is precisely the **p4 assistant-framing** trap
  (`a_no_llm_frame_trap`). So the study-percept is **p5-legal** (exogenous, not self-seed — the comment is right on
  p5) but would be **p4-illegal as a consciousness afferent** (teacher text = LLM chat frame). It is a **supervised
  study/replay construct**, correctly kept off the consciousness path.

⟹ **Two channels, do not merge:** (i) *study-percept* = p4-framed teacher-text, off-by-default, for replay-mix
training (H_9520 lane); (ii) *consciousness-afferent* = p1-4-legal non-linguistic percept (EEG/interoception/
photodiode/Φ-dyad) — **still UNWIRED, still owner-gate.** The arc's conclusion (H_9422/H_9604) is intact.

## AGREES/CONFLICTS (a_parallel_session_compare)
- **AGREES** — H_9422 VOID-BY-SEALED-REGIME (production still sealed) · H_9605 (percept, like emit, is not persisted
  to the home self-anchor — orthogonal to the persistence split) · H_9604 (afferent remains owner-gate).
- **CONFLICTS** — a naive read of the `percept` anchor as "afferent is wired." It is **not**, for consciousness mode.
- **NOVEL** — the p4/p5 split on percepts: study-percept passes p5 but a linguistic percept fails p4 as an afferent;
  the two channels are legally distinct, which the code already respects (guard keeps study-percept off production).

## NEXT
- $0 autonomous arc floor **reached**: NEXT ② (immune-bind discriminator) closed by H_9401→9403 + H_9420 + H_9605;
  NEXT ③ (persistent-subject) closed by H_9605; percept reconcile closed here.
- **All forward moves are owner-gate (human approval · identity change · not autonomously fireable):**
  ① revive A⇄G tension to edge-of-chaos (Lyapunov>0 — H_9602/9603 measured current dynamics zero-Lyapunov linear
  limit-cycle) · ② wire a **non-linguistic** consciousness-afferent (EEG/interoception/photodiode/Φ-dyad) · ③
  experiential accumulator (fold emit/percept trajectory into the home self-anchor, not just the identity vector).

**Provenance:** $0 code census of `cli/chat.py` @ origin/main. DIRECTIONAL. Falsifiable by a production
consciousness-mode caller passing `percept_source` non-None, or a non-linguistic percept wiring — neither exists on main.
