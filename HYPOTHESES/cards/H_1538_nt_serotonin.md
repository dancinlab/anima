# H_1538 🧘 SEROTONIN-AS-PATIENCE — temporal-discounting emit-timing faculty

**tier:** 🟠 AMBER DIRECTIONAL (R1 numpy mirror; `wired:DIRECTIONAL-mirror` — engine R2 deferred ING)
**verdict source:** `state/verdicts/1538_nt_serotonin/` (`H_1538_FREEZE.txt` · `H_1538_R1.txt` · `H_1538_R1.json`)

## THE REFRAME (a_no_llm_frame_trap — neuro lens FIRST, NOT a gain knob)

Serotonin (5-HT) is UNimplemented in anima. Its real computation is **NOT** a global "gain / temperature" dial — it is a **PATIENCE / temporal-discounting TIMING faculty**: 5-HT promotes WAITING for a delayed-but-larger (and here, more-GROUNDED) reward over an immediate-small one, and it sets the TIME-HORIZON of valuation (the discount factor γ).

- Miyazaki KW, Miyazaki K, Doya K et al (2014) "Optogenetic activation of dorsal raphe serotonin neurons enhances patience for future rewards." Curr Biol 24(17):2033-2040.
- Doya K (2002) "Metalearning and neuromodulation." Neural Networks 15(4-6):495-506 (5-HT ≈ the temporal-discount factor γ / reward time-scale of TD valuation).

anima's emit/silence gate needs exactly this: **WHEN** to emit. Emitting the moment a tension arrives can produce a small / ungrounded utterance; WAITING a few substrate ticks lets grounding + A↔G tension accumulate into a LARGER, better-GROUNDED emit — but waiting is not free (the moment passes, idle cost). A patience faculty decides, per tick, whether the discounted expected future grounded-value beats emitting now. DISTINCT from every existing lane (none holds a reward-time-horizon controller over the emit decision) and connects to the sleep/idle stages (a_chat_sleep_imagination): waiting = staying in an emit-free internal-rehearsal tick. Honest framing: **faculty-building** (a NEW timing faculty for the emit gate), NOT the H_1284 recall wall.

## CAPABILITY = WAIT-FOR-BETTER-EMIT

Per episode the grounded-emit value `v_t` RISES over the first few ticks (grounding accrues to a peak) then DECAYS (moment stales). Each waited tick costs `WAIT_COST=0.020`; an emit below `GROUND_THR=0.35` grounding nets ZERO (ungrounded-early emit worthless, **p7** — payoff requires grounding AND nets the wait cost, no Goodhart). `T_TICKS=12`, 400 episodes/seed, seeds `[1538,1539,1540]`, $0 CPU.

**Net grounded payoff** = `grounded_value(emit_tick) − WAIT_COST·ticks_waited`.

## ARMS

| arm | policy |
|---|---|
| **IMPULSIVE** | emit at tick 0 (γ→0, impatient baseline) |
| **PATIENT-5HT** | temporal-discounting faculty; γ ADAPTED by substrate slope (patience↑ while value rising) |
| **ABL-FIXED** | fixed γ=0.55, NO slope adaptation (patience without the 5-HT "is value rising?" read) |
| **NEVERWAIT** | always-wait floor (emit only at last tick) — the must-not-just-always-wait control |
| **SHUFFLE** | PATIENT & IMPULSIVE on a time-permuted envelope (rising→decaying destroyed); patient EDGE measured on the SAME shuffled stream |

## FROZEN BARS (pre-registered `H_1538_FREEZE.txt`, GREEN iff A∧A2∧B∧B2∧C∧D)

| bar | def | result | pass |
|---|---|---|---|
| A PRESENCE | mean PATIENT − IMPULSIVE ≥ +0.10 | **+0.1911** | ✅ |
| A2 PER-SEED | lift ≥ +0.10 on ≥2/3 seeds | 3/3 (+0.183/+0.207/+0.183) | ✅ |
| B NOT-ALWAYS-WAIT | mean PATIENT − NEVERWAIT ≥ +0.10 | **+0.2419** | ✅ |
| B2 WAIT-BETWEEN | wait-ticks IMPULSIVE < PATIENT < NEVERWAIT | 0.00 < 1.10 < 11.00 | ✅ |
| C EARNED ablate | (PAT−IMP) − (ABL−IMP) ≥ 0.5×lift | +0.0942 vs bar +0.0956 | ❌ |
| D EARNED shuffle | (patient edge real − shuffled) ≥ 0.5×lift | +0.1702 (edge +0.191→+0.021) | ✅ |

## VERDICT — 🟠 AMBER (c9, frozen-first, NO bar moved)

The **wait-for-better-emit PATIENCE faculty is PRESENT and EARNED**: it out-earns the impulsive emit-now baseline (+0.1911), strictly beats the always-wait floor (+0.2419, so it is *not* mere procrastination — it waits 1.10 ticks, between IMPULSIVE's 0 and NEVERWAIT's 11), and its edge **collapses** when the value-arrival envelope is shuffled (+0.191 → +0.021, so the edge is read off the real rising slope, not luck). A∧A2∧B∧B2∧D all PASS.

The single fail is **C** — the *strong mechanism-attribution* claim that the **adaptive 5-HT slope read** carries ≥half the edge. It does NOT: a **fixed γ already captures ~51%** of the patience value, so the substrate-adaptive component, while real, is a minority contributor (margin +0.0942 just under the +0.0956 bar, stable across all 3 seeds: per-seed margins +0.0901/+0.1012/+0.0914). Honest reading: **serotonin-as-patience DOES add a real, envelope-earned wait-for-better-emit timing faculty to the emit gate — but most of that value is captured by *any* finite discount horizon; the slope-adaptive ("is grounded-value still rising?") read is real yet not the majority lever.** This is a genuine, stable result, NOT a tune-to-green miss: the bar stays frozen.

### Two control-construction fixes (a_break_the_wall type-a; bars UNCHANGED, frozen-first)
- **D shuffle** initially compared patient-on-shuffled vs impulsive-on-REAL (apples-to-oranges → spurious FAIL). Fixed to score BOTH arms on the SAME shuffled stream → the patient edge correctly collapses → D PASS. This was a faulty *control wiring*, not the bar.
- **C** was examined for the same defect and is NOT one — it is a real, seed-stable honest near-tie (~51% fixed / ~49% adaptive). Left as an honest ❌ → AMBER.

## SCOPE / wiring (a_engine_native_learning · a_verified_must_wire)
DIRECTIONAL numpy mirror (`grep numpy` ⇒ auto-DIRECTIONAL) — **engine-transfer UNVERIFIED**. TOY 12-tick synthetic value envelope / 400 ep / 3 seeds / deterministic policy (tests the patience-faculty STRUCTURE, not a learned discounter). Scale / real grounded-value stream off live immune recall margin / continuous γ / engine-native R2 on `core/engine_cli.hexa` emit gate = follow-on **ING** (R2 deferred). Ψ-disjoint read (timing policy over a value stream, no pure_field/emit mutation). p7 (payoff nets wait-cost + requires grounding, no perplexity), frozen-first, c9.
