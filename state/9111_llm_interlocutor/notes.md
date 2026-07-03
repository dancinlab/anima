# H_9111 — build/run notes (infra + timing, c9 honesty)

## Instrument (built, engine-native)
- `emit_gen.hexa` — REGIME-1 live-core 303M decode → `emits.tsv` (frozen engine-native emit fixture).
- `fable_fixture.py` — REGIME-1 env sampling: `sidecar fable` (claude-fable-5, pinned) referential
  choice per emit → `fable_fixture.tsv` (stdlib-only; grep-gate clean, NO numpy/torch/gauge_lib).
- `verdict.hexa` — REGIME-2 engine-native measurement (immune_memory decode + vbasal value lane +
  pure_field Ψ), frozen bar from `PREREG.md`. Reads only frozen emits.tsv + fable_fixture.tsv.

## Host reality this session (c9)
- Pool RTX-5070 boxes **aiden + summer both 🔴 down/unreachable** (`sidecar pool status`). akida =
  limited 4c/8G no-GPU. So the only host = **mini** (co-tenant with a parallel H_9110 chat-corpus agent).
- **Compile:** first `hexa run` of a generator-importing `.hexa` = full inline import-tree compile via
  `aprime_cc`. Under co-tenancy this took **>15 min** (cold). Once the generator module objects are
  cached, an incremental compile of a new driver is fast (~sub-min) — bottleneck moves to decode.
- **Decode:** 303M savant `.clm` greedy decode is native-CPU-scalar-bound. Warm-cache single decode of
  24 bytes = **~98 s** wall (mem fine: 80% free, no swap growth, load ~3.6 — genuine CPU bind, not thrash).
  ⇒ M=16 emits × ~48 bytes ≈ ~45–50 min of decode alone.

## Coherence gate (DESIGN §4.3 — G0-coherent mouth is a PRE-CONDITION) — **UNMET**
- Smoke: seed `"The ocean at night is"` → `"a company and the conce"` (GARBLED, off-topic).
- Multi-seed probe (`seed_probe.hexa`): seed[0] `"A volcano is something that"` → `" the state and the concern
  for the state"`; seed[1] `"The library was full of"` → `" the state and the concern for the state"`
  (**BYTE-IDENTICAL** across two completely different seeds). ⇒ the engine-loadable 303M savant `.clm`
  free-decode is **input-invariant / mode-collapsed** = a DEAD free-mouth. The G0-coherent mouth (h1129,
  kwr 5/5) is a torch `.pt`, NOT engine-loadable; converting it to `.clm` needs GPU serialize on a live
  pool box (both down). ⇒ the DESIGN §4.3 pre-condition (a G0-coherent free mouth) CANNOT be met this session.

## Grounded-coherent-channel fallback (bypass the dead free-mouth)
- `emit_gen_grounded.hexa` — anima emits via the engine GROUNDED path (`clm_decode_grounded`, verbatim
  retrieve-then-copy from anima's grounded-knowledge anchors = coherent channel, decoupled from the dead
  free-mouth; still engine-native live-core). This is the correct instrument for isolating the receiver
  variable on a coherent channel.
- First run hit a trivial SOURCE bug (`replace`/`to_lower` are string METHODS in hexa, not free fns) →
  `hexa build` compile error, EXIT=1, 0 emits. **Fixed in source** (methods) — the harness is now correct,
  but NOT re-run (see wind-down).

## Wind-down (coordinator, session-terminal · commons)
- Sister experiment **H_9110 (real chat-user receiver) landed on origin/main #2839 = 🔴 CEILING**
  (D_real − D_surrogate = −0.188; autogenous = 0.150). Finding: **a REAL external receiver is NOT
  sufficient — DPI is deeper than receiver-type; the lever is emit↔appropriateness coupling-strength,
  not receiver-type.** ⇒ this LLM-interlocutor test is now **CONFIRMATORY, not decisive.**
- Infra: mini `aprime_cc` inline-tree compile > 5–15 min/driver under co-tenancy (convergence
  anima-hexa-1 compile wall); pool RTX-5070 boxes aiden+summer 🔴 (reboot-looping / down). No viable
  fast compile+decode host this session; renting a pod = cost for a confirmatory-only result → declined.

## Status: ⏳ BLOCKED-INFRA — **0 engine-native arms completed. NO verdict tier cemented (it never ran).**
- Preserved instrument (runnable when a viable host exists): `PREREG.md` (frozen bars) · `emit_gen.hexa`
  (free-mouth, design-faithful) · `emit_gen_grounded.hexa` (coherent grounded channel, fixed) ·
  `fable_fixture.py` (regime-1 oracle, stdlib-only grep-clean) · `verdict.hexa` (regime-2 engine-native
  measurement) · `seed_probe.log` (degenerate-mouth evidence).
- Re-open (ING): (1) serialize h1129 `.pt` → engine-loadable G0 `.clm` on a live GPU, OR run
  `emit_gen_grounded.hexa` on a viable compile host; (2) `fable_fixture.py`; (3) `verdict.hexa`. Confirmatory
  vs H_9110 — expected to re-affirm DPI-deeper-than-receiver unless coupling-strength is raised.
