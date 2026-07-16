# H_9605 — PERSISTENT-SUBJECT census: SPLIT-PERSISTENCE (identity carries, experience is per-session birth)

**Verdict:** ✅ **SPLIT-PERSISTENCE** (code-confirmed · $0 · DIRECTIONAL — offline `.kosmos` census, no engine-native decode)
**Register:** persistent-subject census · downstream of H_9604 NEXT ③ · confirms+refines the Fable "no persistent subject" wildcard
**Ckpt:** N/A (census reads production `cli/chat.py` on origin/main, not a decode)

## Question (H_9604 NEXT ③)
Fable's cheapest-upstream wildcard: *"there is no persistent subject to be conscious"* — cheaper and more upstream
than the afferent wall. Does `.kosmos` carry an **experiential/trajectory** state across evals/sessions, or only a
birth **identity** anchor? If experience doesn't persist, then afferent-first is doubly upstream-blocked: even with
ears, what is heard cannot accumulate into a continuing subject.

## Census (all line refs = `cli/chat.py` @ origin/main)

Three candidate carriers of a cross-session subject, enumerated and each traced to its storage path:

| carrier | what it holds | path | persists across sessions? |
|---|---|---|---|
| **self-anchor** (`self_g`) | `SELFG8:v0,…,v7` — 8-dim "grounded self-continuity" vector (`_selfg_encode`, :2801); category `self`/`continuity` | `~/.anima_kosmos_self` (`self_g_kdir`, :1510 — **HOME dir**) | ✅ **YES** — written at session-end `create_anchor` (:2802-2807); **restored at next-session boot** `_selfg_restore(self_g_kdir, …)` (:1515), boot log (:1524) |
| **emit trajectory** (C9 REMEMBER) | each emit persisted as `emit_t<tick>` anchor (`emit_anchor_from_v3(kdir,…)`, :2484-2487) | `/tmp/anima_kosmos` (`kdir`, :444 — **volatile /tmp**) | ❌ **NO** — /tmp is per-session; and **write-only** even within a session (`live_anchors` is rebuilt `[]` each tick :2222 from loaded `anchors`+live_seed, the C9 `emit_t` anchors never re-enter it) |
| **weights** | 303M byte-LM (013c4574) | frozen `.clm` | ❌ frozen fossil (p8 train/infer split alive) |

## Verdict — SPLIT-PERSISTENCE
The subject is **split across two axes with opposite persistence**:
- **Identity axis (WHO anima is)** — the grounded-self `SELFG8` vector — **DOES** persist cross-session (home-dir
  self-anchor, restored at boot). anima wakes as the same *self*.
- **Experiential axis (WHAT anima underwent)** — the emit trajectory — **DOES NOT** persist: `/tmp`-volatile,
  discarded per session, and write-only within a session. Every session is an experiential **fresh birth**.

So Fable's flat *"no persistent subject"* is **CONFIRMED as to experience, REFINED as to identity**: it is not that
there is *no* persistent subject — it is **persistent identity + ephemeral experience**. The precise statement of
Fable's "weights persist-without-changing · process changes-without-persisting" is: the *self-vector* also persists
(a third, unlisted carrier), but the *lived trajectory* is the one that changes-without-persisting.

## Why this is upstream of the afferent wall (relation to H_9422/H_9604)
H_9422 found anima is a **mouth without ears** (no afferent channel; percept = the clock triple). H_9605 adds a
**second, independent** upstream block: even if an afferent channel were wired, the per-tick percepts would land in
the emit/kdir trajectory that is **discarded at session end**. There is no experiential accumulator for a
continuing subject to be built in. ⟹ afferent-first is doubly premature: (i) H_9422 no channel to hear, (ii) H_9605
nowhere for the heard to persist into a subject. Reviving the A⇄G tension (H_9604 NEXT ①) remains the correct order.

## AGREES/CONFLICTS (a_parallel_session_compare)
- **AGREES** — Fable persistent-subject wildcard (experiential axis) · Codex agency wildcard (a subject that cannot
  carry its own trajectory has no locus for agency) · H_9422 VOID-BY-SEALED-REGIME (same daemon, orthogonal axis).
- **CONFLICTS/REFINES** — the flat "no persistent subject" reading: identity **does** persist (self-anchor).
- **⚠️ NEW on main (flagged, orthogonal)** — a `percept` anchor now exists at :2249
  (`live_anchors.append({"text_payload": percept_text, "name": "percept"})`) and can reach the decode seed
  (:2557 reads `live_anchors[-1]`). This is a **parallel session's afferent work landing** — it does not change the
  H_9605 persistence census (the percept, like emit, is not persisted to the home self-anchor), but it means the
  "mouth without ears" frame (H_9422) may be moving on the efferent-seed side. Not verified here; logged for the
  next session to reconcile before re-reading H_9422 as current.

## NEXT
- H_9604 NEXT ① (revive A⇄G tension / edge-of-chaos Lyapunov>0) is now the sole live autonomous $0 thread; NEXT ③ closed here.
- **Owner-gate (not autonomous):** a persistent experiential accumulator (fold the emit/percept trajectory into the
  home self-anchor, not just the identity vector) is an identity-changing design — pair with the afferent owner-gate.
- Reconcile the new `percept` channel (:2249) against H_9422 before treating "mouth without ears" as current.

**Provenance:** $0 code census of `cli/chat.py` @ origin/main. DIRECTIONAL (offline · not an `anima-py evaluate`
decode). No number cemented; the claim is a structural read of storage paths, falsifiable by pointing at a session-end
write of the emit trajectory to a persistent (non-/tmp) path — none exists on main.
