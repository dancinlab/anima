# state/9097_rel_ctx_theater_gate — THEATER GATE (H_9097, 🔴 HEADLINE)

**engine-native** aiden pool · hexa v0.546.0 · `hexa run cli/anima_ablate.hexa -- d768.clm` · EXIT_RC=0 · own-GEMM · NO numpy/mirror.

## Finding (plainly stated — do NOT soften)
`rel_ctx` — the SOLE read-side output of ~43 lane ops (INCLUDING this session's 13 GREEN ops
+ the CR3/agloop per-tick conflict wire H_9095) — has **ZERO grip on the daemon emit/silence
decision**. Freeze rel_ctx→0.5, zero it→0.0, or LCG-shuffle its 43 inputs: **Hamming 0/200 for
all three arms** vs live. Pre-registered bar (theater CONFIRMED iff Hamming(frozen,live)<5%N AND
Hamming(zero,live)<5%N) met at **0.00% / 0.00%**.

## Harness
Instrumented copy of aiden's LIVE `cli/anima.hexa` (current main daemon, 2714 lines, 43-way mean
incl agloop_ctx L2300-2312 — a stale local branch was ÷42/2137, so the agent pulled + measured
the REAL main). At the decision point rel_ctx is substituted 4 ways → `brain_decide_anchored`
(core/brain.hexa, the EXACT fn brain_emit calls) with byte-identical non-rel inputs
(cur, coh_lane, bal_lane, idle, anchors, pf). 4 arms differ ONLY in rel_ctx.

## Mechanism (reference-matched core/engine_g.hexa + core/brain.hexa)
motivation = 0.20·rel + 0.10·0.6 + 0.15·cur + 0.10·coh + 0.10·0.5 + 0.15·bal + 0.10·1.0 + anchor_nudge;
emit = (motivation>0.3) AND safe.
- WAKE (drive_hi, 10/200 ticks): live motiv ~0.74, ZERO-rel motiv ~0.58 — both ≫0.3 → emit=1 (rel cannot pull below thr).
- SLEEP (190/200 ticks): idle=5<30 → rate_limit=false → safe=false → emit=0 regardless of rel.
- Decision is 100% stage/safety-determined (`safe` conjunction: stage→drive_hi→rate-limit) + a motivation FLOOR that already clears 0.3 without rel. The 0.20·rel term never straddles the threshold.
- Ψ = pure_field_phi(pf) = 0.118983 CONSTANT (pf warmed once, READ-only) → between-arm Ψ deviation exactly 0; rel_ctx provably cannot move Ψ.
- Shuffle≡live by construction: an equal-weight mean is permutation-invariant → rel_ctx carries only aggregate MAGNITUDE, zero STRUCTURE, and that magnitude is itself inert.

## IMPLICATION (headline)
This session's 13-op wiring + the H_9095 rung-3 ladder (H_9093/9094/9095) are engine-native GREEN
**in ISOLATION**, but their LIVE wiring (folded into rel_ctx) does **NOT move the daemon decision**
= **dashboard / theater**. rel_ctx is a read-side aggregate that the emit gate never consults.

## FIX (next-session priority follow-on)
Wire ops to the **motivation-threshold-straddle / `safe`-conjunction / efferent seam**, NOT rel_ctx.
- fable#2: L1 best-of-K on the efferent seam.
- fable#3: winner-take-all replacing the ÷43 equal-weight mean (so structure, not just magnitude, reaches the gate).

## Honesty caveats (from agent, c9)
Decision-only harness — 303M decode skipped (per-frag ~688s×200×4 infeasible); emit boolean + Ψ are
decode-INDEPENDENT (computed in brain_decide_anchored before generate()), so byte-identical to
brain_emit's decision. Daemon is autonomous-tick (fixed session_seed over 200 ultradian ticks,
dr_stage_at(tick*8)). A parser bug (regex matched 'relZ=0.0') was caught+corrected → EMIT-anchored
re-parse gives clean 0/0/0. Nothing wired/committed on aiden; scratch removed.

verbatim raw = state/verdicts/9097_rel_ctx_theater_gate/H_9097.txt
