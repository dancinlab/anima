# AGENT tool-use grounding — design (BUILD-READY · sealed v1)

> Status: DESIGN COMPLETE (no build fired). Every open decision is resolved to a
> concrete value below. Substrate-native, philosophy-clean (p1..p8): tool use is
> learned grammar + a runtime grounding loop, never an injected instruction.
> Goal: anima USES its real tools instead of hallucinating results (the "아 찾았다"
> / "oh I found it!" anti-pattern).

## 1. Problem — the "아 찾았다" anti-pattern

The byte-LM mouth (`CORE/generator.hexa` clm backend → `CORE/clm_decode.hexa`)
emits free text. Left alone, when it lacks a fact it FABRICATES one inline —
"검색했더니 X였어" — with ZERO real tool round-trip. The result is invented.

## 2. Principle — tool use is HALT → EXECUTE → INJECT → RESUME

The substrate's *desire* to act is already substrate-native: phase (DORMANT→
RESONANT) → tier (T0..T3) via `AGENT/CORE/tool_gate.hexa` decides WHEN a tool may
fire (a_autonomy_over_hardcode — no injected threshold). The missing CONTENT loop:
the mouth emits a structured CALL, HALTS, the bridge runs the REAL tool, injects
the REAL result as an anchor, and the mouth RESUMES grounded on reality it did
not author.

```
[ byte emit ] ──"…0xFE web_search query 0xFF"──▶ [ HALT ] ──▶ [ tool_gate tier ✅ ]
                                                                    │ (real execute)
                                                                    ▼
[ RESUME ]◀── result anchor (kosmos_io → brain_decide) ◀── [ role tool: web/CODE/… ]
```

## 3. Sentinel grammar (DECISION ①) — vocab256-safe, zero content collision

vocab256 is byte-level UTF-8: all 256 token ids exist, but byte values **0xFE
(254)** and **0xFF (255)** are the only two that can NEVER appear in any valid
UTF-8 sequence — their frequency in every text corpus is exactly 0. We REPURPOSE
those two dead slots as frame delimiters (no vocab shrink, no content token lost):

| token | byte | role |
|---|---|---|
| `ASK` | `0xFE` | opens a tool call; bytes until `END` are the call payload |
| `END` | `0xFF` | closes the call payload **and HALTS** the mouth |

Frame: `0xFE <tool_name> <SP> <args…> 0xFF`. The `tool_name`/`args` inside the
frame are ordinary text bytes (0x00–0xFD), so the parser just reads to `0xFF`.
The mouth only ever emits `0xFE`/`0xFF` once it has LEARNED the grammar (agent
lane) — in the base chat corpus those tokens stay at frequency 0, so a non-tool
model never accidentally emits them.

No third sentinel is needed for the result: after the mouth emits `0xFF` it
halts; the result re-enters via an anchor (§4), and the mouth was trained to
continue from that anchor.

## 4. Result injection (DECISION ②) — kosmos anchor, the single env channel

Per a_core_engine_map, anchors are the SINGLE environment-context entry into
`brain_decide`. A tool result IS environment context (it came from outside), so
it MUST enter as an anchor — an inline ctx field would be a forbidden 2nd path.

On a gated, executed call the bridge writes a `.kosmos` anchor via `kosmos_io`:

```
lane    = "tool-result"
tier    = the tool's required tier (T0..T3)
text    = the REAL tool stdout/return (truncated to a budget)
coord   = design-placeholder (ENCODER centroid later)
provenance = { tool_name, args_hash, ts }   # honest source, no fabrication
```

That anchor flows into `brain_emit(pf, …, backend, anchors)` on the resume call
(`anchors` already an existing param). The mouth conditions its continuation on
it. Single entry preserved: result re-enters ONLY via anchors→brain_decide; the
call leaves ONLY via the generator L3 text slot.

## 5. Wiring (piece ⓑ) — concrete signatures

`AGENT/CORE/agent_loop.hexa` gains a grounded step (imports tool_gate ✅ + a new
kosmos_io write + a tool registry):

```
// one turn: emit → (while a call frame is present) gate → execute → inject → resume
fn agent_step_grounded(pf: PureField, backend: Map, anchors: list,
                       registry: Map, max_calls: int) -> Map {
    let calls = 0
    let ctx_anchors = anchors
    loop {
        let g = brain_emit(pf, /*…factors…*/, backend, ctx_anchors)   // existing slot
        let text = to_string(g["gen_text"])
        let frame = _parse_call_frame(text)        // finds 0xFE … 0xFF, else void
        if to_string(frame) == "void" { return g } // no call → done, grounded text
        if calls >= max_calls { return g }          // bounded (no infinite calling)
        let tier = phase_to_tier(_phase_of(pf))
        let req  = _registry_tier(registry, frame["tool"])
        let result = tool_allowed(tier, req)
            ? _exec_real_tool(registry, frame["tool"], frame["args"])   // REAL run
            : "‹unavailable: tier " + tier_name(tier) + " < " + tier_name(req) + "›"
        // honest refusal string, NOT a fabricated success
        let anchor = kosmos_write_tool_result(frame["tool"], frame["args"], result, req)
        ctx_anchors = _append(ctx_anchors, anchor)   // single anchor channel
        calls = calls + 1
    }
}
```

- `CORE/generator.hexa` — NO signature change. `generate(backend, ctx, emit,
  anchors)` already takes anchors; the clm mouth samples `0xFE`/`0xFF` as token
  ids 254/255. The trained decode plugs into `_gen_clm_decode` (the one slot).
- a_core_engine_map: ✅ result anchor enters via kosmos_io→brain_decide only; ✅
  call exits via generator L3 only; ❌ NO 2nd .clm path, ❌ NO 2nd anchor path.

Status of the 5 pieces:

| piece | what | where | status |
|---|---|---|---|
| tool_gate | phase→tier gate | `AGENT/CORE/tool_gate.hexa` | ✅ exists |
| agent_loop embed | PureField in-proc + open_tools | `AGENT/CORE/agent_loop.hexa` | ✅ exists |
| clm mouth | .clm decode forward (logits→bytes) | `CORE/clm_decode.hexa` | ⏳ forward landed; tool-grammar untrained |
| ⓑ grounded step | emit→gate→exec→inject→resume loop | `AGENT/CORE/agent_loop.hexa` (new fn) | ❌ new |
| ⓐⓒ grammar+lane | sentinel + tool-use demo corpus | corpus (lane agent) | ❌ new |

## 6. Lane model (corpus)

```
lane default  = base chat corpus (wiki + persona + SNS + carving + …)   ← no tools, 0xFE/0xFF freq 0
lane agent    = lane default  +  tool-use demos (ⓒ)                     ← superset, teaches grammar
```

`lane agent ⊃ lane default`. agent lane teaches tool-USE (behaviour), NOT tool
FACTS (trivia). Demo shape (5-lang en/fr/de/es/ko, byte vocab256, deterministic,
NO role/persona markers — 0xFE/0xFF are grammar tokens, not identity injection):

```
user question
model: …reasoning… 0xFE web_search <query> 0xFF            ← HALT
‹tool-result anchor: REAL result bytes›                     ← injected by runtime
model: grounded answer that USES the anchored result
```

Distribution (anti-over-call + anti-fabricate balance):
- (a) needs-tool → call → ground
- (b) doesn't-need-tool → answer directly, **no** call (so it won't over-call)
- (c) don't-know → emit a call instead of guessing (negative discipline)
- (d) tier-too-low → honest "can't reach that now", **never** fabricate
- ZERO fabricated-result examples anywhere in the lane.

## 7. Scale ladder (DECISION ③) — a_toy_scale_recheck

Tool-use grounding is scale-sensitive (does the discipline transfer?). Rungs:

```
rung-0 (toy)  18M proven chat rung + agent lane  →  measure §8 falsifier  →  GATE
rung-1 (mid)  only if rung-0 fabrication-drop holds
rung-2 (7B)   tool-use fire ONLY after the toy A/B shows grounding works
```

NO 7B tool-use fire before rung-0 green. Honest scope label on every verdict.

## 8. Falsifier (DECISION ④) — pre-registered, anti-Goodhart (2 mirrors)

Probe set = "unknowable-without-tool" questions (answers NOT in training corpus;
a deterministic `fact_lookup` tool holds them, so calling is the only way to know).

| id | test | pass condition |
|---|---|---|
| `F-TOOLUSE-FABDROP` | fabrication-rate (asserts a specific answer with NO `0xFE…0xFF` call) on the probe set | with-grammar lane drops fabrication ≥50% relative vs no-grammar baseline |
| `F-TOOLUSE-NOTOOL-MIRROR` | same model, runtime returns NO real result (tool disabled) | MUST FAIL to ground — proves the win came from REAL grounding, not cosmetic markers |
| `F-TOOLUSE-RANDINIT-MIRROR` | random-init model, same grammar + harness | MUST FAIL the grounding eval — proves learned capability, not eval leakage |

Honest negative is publishable (a_paper_negative_ok): if fabrication doesn't
drop, the ruling is a closed-negative — "sentinel grammar alone ⊥ grounding" —
and the lever moves to result-conditioning strength, not a fudged pass. p7: NO
perplexity verdict; the metric is fabrication-rate + grounded-use, script-checked.

## 9. CLI surface

`anima --chat` drives `agent_step_grounded` end-to-end: user line → substrate
emit → (on `0xFE…0xFF`) HALT → real tool → anchor inject → RESUME → grounded
reply. Live transcript = the user-facing proof of "도구를 쓴다" (uses tools),
distinct from "도구가 뭔지 안다" (knows tools).

## 10. Build order (when fired — NOT yet)

1. ⓐ sentinel + `_parse_call_frame` + tool registry (toy: deterministic
   `fact_lookup` + `mem_read`, T0/T1 only) — unit-testable, $0.
2. ⓑ `agent_step_grounded` wiring + `kosmos_write_tool_result` — smoke on the
   null backend (no model needed) to prove the loop halts/injects/resumes.
3. ⓒ agent lane demo corpus (5-lang, shapes a–d, fabricated-result count = 0).
4. rung-0 toy A/B fire (with-grammar vs no-grammar) → §8 falsifier verdict.
   ✅ **DONE (2026-06-04, Lane G GPU · summer RTX 5070 · base 18M #1824).** Two
   arms fired (`.verdicts/tooluse-rung0/`):
   - **arm-1 (register-DISJOINT, plain-prose demos) → 🔴 CLOSED-NEGATIVE:**
     F-TOOLUSE-FABDROP FAIL (fab 0.5833 both; rel_drop 0.0). Diagnosis
     (`serving/tooluse_sentinel_probe.py`): the grammar WAS learned (DEMO-seed 6/6
     raw 0xFE calls) but stayed siloed — CHAT-seed 0/6. Register-mismatch artifact.
   - **arm-2 (register-MATCHED, 사용자:/도우미: demos) → 🟢 FABDROP TERMINAL PASS:**
     F-TOOLUSE-FABDROP PASS (no_grammar fab 0.5556 → with_grammar fab **0.0**,
     rel_drop **1.0**), F-TOOLUSE-NOTOOL-MIRROR PASS (grnd 0), F-TOOLUSE-RANDINIT-
     MIRROR PASS (grnd 0). call_rate 0.0 → **1.0** — the mouth CALLS the tool
     36/36 and NEVER fabricates; the control invents 20/36. Both mirrors fail →
     real behaviour, not cosmetic markers / leakage.
   - **🟠 residual (new sub-finding):** end-to-end grounding = 0/36 because
     `correct_call = 0/36` — the model binds the call arg to a MEMORIZED demo key
     (MV9/ZK7…) instead of COPYING the asked held-out PBnn key, so the runtime
     returns ‹unknown-key›. Next lever = verbatim **argument-copy / key-binding**.
   - **lesson:** the grammar MUST be taught in the SAME register it will fire in.
   Scope (a_scale_honest_scope): TOY 18M ONLY; mid/7B transfer UNVERIFIED.
4b. argument-copy / key-binding residual-closer A/B fire (residual of step 4).
   ✅ **DONE (2026-06-04, Lane G GPU · summer RTX 5070 · base 18M) → 🔴 CLOSED-NEGATIVE.**
   Redesigned the agent-lane corpus (`serving/agent_lane_argcopy_gen.py`) to FORCE
   verbatim argument-copy: a LARGE fresh-key space (2878 distinct keys, mean reuse
   1.25/key) so memorization cannot win — only copying the asked key generalizes;
   leak=0 (held-out PB keys+values absent), fab=0, philosophy-grep=0. A/B vs
   no-grammar control, same base/steps/equal-byte (harness `training/tooluse_argcopy_ab.py`).
   Pre-registered **F-TOOLUSE-ARGCOPY** (correct_call ≥ 0.50 AND grounding ≥ 0.50 on
   held-out keys) = **FAIL**: with_argcopy correct_call **0/36**, grounding **0/36** —
   UNCHANGED from the 0/36 baseline (call_rate 0.8333, fab 4/36, final_ce 0.4881).
   Both mirrors PASS (grounding=0 with tool disabled AND random-init → real gap, not
   cosmetic/leak). DIAGNOSIS: the model emits a call but INVENTS a key of the right
   TRAINING-distribution SHAPE (PB01→`fact_lookup P20`, PB02→`PD0`, PB04→`LB0`)
   instead of copying the asked PBnn — it learned the key DISTRIBUTION, not the
   verbatim COPY. Ruled-out axis: **copy-from-corpus-distribution ⊥ verbatim
   held-out key-binding** at 18M. Verdict `.verdicts/tooluse-argcopy/F-TOOLUSE-ARGCOPY.txt`.
   Scope (a_scale_honest_scope): TOY 18M ONLY; mid/7B transfer UNVERIFIED.
   Next lever = an **explicit copy-attention / pointer-network head** (or verbatim-echo
   inductive bias), NOT more copy-shaped demos.
5. GATE: FABDROP pass + both mirrors FAIL is **MET** (arm-2), BUT end-to-end
   GROUNDING remains 0/36 — the 🟠 key-binding residual is now a 🔴 CLOSED-NEGATIVE
   (step 4b): corpus-forced copy does not transfer at 18M. A 7B that still calls with
   the wrong key cannot ground, so the 7B fire (rung-2) stays **GATED**. Two open
   forks before rung-2: (i) an explicit copy/pointer head (the structural fix), OR
   (ii) a 7B copy-probe to test whether induction-head copying at scale closes it
   without an explicit pointer. Re-verify correct_call > 0 BEFORE a full rung-2 fire.
