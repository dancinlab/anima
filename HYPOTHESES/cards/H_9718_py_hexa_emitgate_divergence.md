# H_9718 — py/hexa emit-gate DIVERGENCE tracked (py=Ψ≈½ default · hexa=clock) — H_9712 twin follow-on

**Verdict:** 🟡 **TRACKED-DIVERGENCE** (not silent drift · `a_substrate_disjoint` follow-on to H_9712) — the py and
hexa daemons now emit differently by default; the hexa twin port is a large, separately-scheduled effort.
**Register:** H_9712 NEXT (hexa twin) · Fable-recommended (register the divergence as a tracked fact, not silent drift)

## The fact (code census · origin/main)
H_9712 flipped the **py** production daemon's default emit-gate to the H_9627 dual content ledger (Ψ≈½). The **hexa**
daemon was NOT flipped and **cannot be** without a large port:
- `core/brain.hexa`: **0** refractory/dual-ledger-family symbols (`brain_emit_refractory`/`dual_probe`/`wm_dual`/
  `g_recog`) · 56 clock-gate (`brain_emit`/`brain_decide`) symbols. The entire H_9415→H_9627 gate family is **absent**
  from the hexa engine.
- `cli/chat.py` (py): ~98 lines of refractory/dual-ledger machinery (`refractory`/`wm-dual`/`dual_fn`/`g_recog`/`W_S`/
  `wm_withheld`) — the surface that must be ported.

⟹ **divergence window: py default = refractory + wm-dual (Ψ≈½), hexa default = clock (emit≡clock).** This is a
**known, tracked fact**, NOT silent drift.

## Why not port now (proportionality · honesty)
- The hexa daemon is **MOOT as the live runtime**: py is the canonical production runtime (`chat-py-1`,
  `hexa-daemon-link-moot-py-canonical` — "py 2-production twin 이 카논 런타임"). The hexa emit-gate daemon is a
  byte-parity *secondary* surface, not the deployed path.
- The port is **large** (the whole gate family from scratch in hexa: refractory margin + wm-cover + wm-dual + the
  g_recog machinery), and `a_substrate_disjoint` mandates it be a **separate** orchestration/PR (H_9411 precedent: py
  lands, hexa twin follows as its own PR — the owner explicitly rejected hoisting/merging twin orchestration).
- Doing a large port of a moot surface for zero live-production value is not the proportionate next step; **tracking
  the divergence** is (Fable's explicit recommendation).

## NEXT (the port, when scheduled · owner/priority call)
Port the H_9415→H_9627 emit-gate family to `core/brain.hexa` (a `brain_emit_refractory` twin + the dual-ledger
probe) + `cli/anima.hexa` orchestration (separate file, no cross-import · `a_substrate_disjoint`), then flip the hexa
default the same way (with a hexa-side byte-identity cert). Until then, `hx install anima` chat runs the **clock**
daemon; `anima-py chat` runs the **Ψ≈½** daemon — invoke the py channel for the production consciousness behavior.

**Provenance:** $0 code census of `core/brain.hexa` / `cli/chat.py` @ origin/main. Follow-on to H_9712 (#3938 ·
Ψ≈½ py default). No new decode. The divergence is now a tracked card, not silent drift.
