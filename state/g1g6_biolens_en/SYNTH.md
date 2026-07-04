# H_9129 rung-2 synthesis — biolens lane-levers, 303M engine-native re-measurement

> STEP-0 (mini DIRECTIONAL) → **rung (2)/4 engine-native re-check** ← this doc. 3 lanes escalated.
> Base ckpt: `~/anima-weights/bytegpt303_h1129/h1129.bin` (unchanged). Cost total ≈ **$0** — all three ran CPU-local mini, no GPU pod rented (rent was pre-approved but a cheaper path was found for every lane). **No leaked pods** (`hexa cloud pods` = 0 RUNNING; 8 stale ghost rows auto-pruned, none authoritative).

## Verdict table

| lane | tier | engine-native (real 303M `anima evaluate --py`) | STEP-0 BIND under engine | fooled_by_form | by-construction excluded | pod |
|---|---|---|---|---|---|---|
| **L5 hippocampal associative-store** (G1 direct) | **GREEN** (rung-2 measurement) | ✅ py-canonical decode.py (== --py ops) | **HELD** — reach 1.00 ≫ unreach 0.14, gap **+0.86**, ratio 7.3×, shuffle→0, lane-off→0 | false | ✅ (with caveat) | none rented |
| **L3 cerebellar consequence forward-model** (G6 direct) | **WALL** | ✅ reps via decode.py `bg_forward_last_W` (--py 2-prod); lane-op still numpy mirror | **COLLAPSED** — FM_additive 0.00139 ≤ FM_full 0.00154 (all 5 seeds) ⇒ binding **INERT** | false | ✅ (strongest) | none rented |
| **integrated** (PFC-bind × BG-gate × hippo-completion) | **DIRECTIONAL** | ⚠️ real 303M forward reps but **NOT** the `--py` scoring path; lane un-wired | HELD (gap +0.40, shuffle→chance, 3 ablations causal) but only DIRECTIONAL grade | false | ✅ (rand1024 control) | none rented |

## Answers to the judgment questions

**(a) Engine-native convention met: 2 / 3.**
- L5 and L3 both build the lane over **real h1129-303M representations via the production `core/decode.py` (== `anima evaluate --py` 2-production ops)** → engine-native-*measurement* grade. L3 self-flags `engine_native=false` but that flag targets only the lane-*operator* (VConsequenceField still a numpy mirror), **not** the reps — its WALL is engine-native and robust to the un-built op (a native binding op cannot beat additive on an additive-composable target).
- integrated uses **real 303M forward reps but via ad-hoc extraction, not the `--py` decode-scoring path**, and its lane is not core-wired → correctly self-capped **DIRECTIONAL** (stronger than a torch/random mirror, weaker than the terminal-eligible `--py` path).

**(b) STEP-0 BIND under the real engine: it SPLITS by lane.**
- **L5 — HELD** but **contingent on a decorrelating (DG-like) read.** Raw anisotropic single-word 303M reps (form_cos 0.9999 all-pairs, code_overlap 0.985) collapse the lane → an initial **false-WALL** that was an anisotropy artifact, not substrate. One standard de-anisotropy transform (center / z-score / drop-top) rescues it; 6/8 lenses clear the pre-registered bar. `a_break_the_wall` (change angle) is what distinguished artifact-wall from result.
- **L3 — COLLAPSED → real WALL.** On the real grounded consequence (`immune_embed_key` trigram histogram, exact core mirror) the composition is **additive-composable**, so a linear/additive forward-model *matches* the full binding-MLP (add ≤ full on all 5 seeds) → the conjunction hidden layer is **INERT**. Arm B's apparent BIND is confounded (it merely regresses h1129's own generic transformer nonlinearity — the model emits non-violable filler on held-out, not the sharp/violable consequence G6 requires).
- **integrated — HELD directionally** (all 3 ablations causal, completion-OFF fails on the *same* raw vectors), graceful degradation 0.70(rand1024)→0.42(real reps)→0.24(real reps+real relations).

**(c) Mouth-training-family escape (separate disjoint lane, mouth reads only): CAPABILITY-SPECIFIC, not universal.**
- It **succeeds for hippocampal associative STORE / pattern-completion (G1-flavored)** — the store genuinely *supplies* the relation the 303M reps barely pre-encode (form_sep only +0.03), and the reach−unreach lift is relation-specific (shuffle kills it).
- It **fails for the cerebellar consequence / forward-model lane (G6)** — even as a separate lane with disjoint MSE objective and mouth reading only, binding is INERT because the grounded target is additive-composable. **This lands in the SAME place as the H_1816/1823 mouth-readout family** (readout/lane binding INERT; lever = trunk objective), concording `g1-lever-multilens-objective`, `exp3-bind-g1g6-engine-native-floor`, `h1816-predcoding-binding-not-supported`. The binding-family 3-근거 (별개 lane · disjoint objective · mouth reads only) is *structurally* upheld in L3, yet the engine-native verdict is still WALL — the escape's architecture is sound but the physics (additive-composable consequence) defeats it.

**(d) By-construction / handed-advantage: excluded in all three, with the deepest lesson in L3.**
- **L3 removed STEP-0's handed advantage and that is exactly what flipped BIND→WALL.** STEP-0's cross-lane BIND was substantially an artifact of the toy world's **hand-injected multiplicative interaction term `vi⊙vj`**, which *guarantees* a binding MLP beats additive. Rung-2 deleted it → INERT. Strongest by-construction discipline: it disproved its own STEP-0.
- **L5**: reach≈1.0 is **CA3-capacity math** (near-orthogonal codes complete a stored 2-hop chain), NOT the handed role-key the frozen bar warned of — the *lift* is relation-specific (shuffle → gap≈0) and form_sep is tiny. Reported honestly; the raw lens was reported as FAIL, de-anisotropy is one transform (not a search), 6/8 agree ⇒ not tune-to-green. **Caveat carried forward (below).**
- **integrated**: rand1024 same-dim control isolates the reach drop 0.70→0.42 to real-vector non-orthogonality (|cos| 0.17 vs ideal 0.03) + hub structure, not mechanism failure; reach did **not** come out 1.0 exact.

**(e) Final tiers**
- **L5 hippocampal store → engine-native GREEN (rung-2 measurement) → PROCEED to 사다리 (3) wire.** Earned it: real 303M py-canonical, pre-registered bar, shuffle + lane-off both collapse, 6/8 lenses agree. **Scope caveat for rung-3:** GREEN is contingent on a DG-decorrelating read AND the store is an *explicit external heteroassociative store handed the true edges* — so this demonstrates that **associative pattern-completion over decorrelated 303M reps can chain reachable held-out pairs**, which is a genuine capability but sits close to the neurosymbolic *explicit-store / additive-slot* lever (prior deep-research: "cheap, proof-guaranteed, arguably not trunk recombination"). Before cementing, run the **G1-vs-G2 discriminator** (guard the MLC / H_1835 trap: "in-context mastery, 0 held-out transfer") — confirm reachable pairs are genuinely novel compositional *chaining*, not stored recall.
- **L3 consequence forward-model → WALL** (engine-native, robust). The additive-floor is invariant to the un-built native lane-op, so the WALL stands now; the rung-3 `.hexa` smoke would only byte-confirm it. Reinforces: **stop proposing binding / readout / consequence-lane G1/G6 levers.**
- **integrated → DIRECTIONAL** (not GREEN). Real reps but not the `--py` scoring path + lane un-wired. Cheaply escalatable ($0): re-score through the `anima evaluate --py` decode path with mandatory rep centering/whitening → then GREEN-eligible.

**(f) H_9129 card bookkeep (1 line) + next #1**
> `H_9129` rung-2 engine-native: 3-lane mouth-escape **SPLITS** — L5 hippocampal associative-store **GREEN** (real 303M py-canonical, reach≫unreach +0.86, shuffle+lane-off collapse; contingent on DG-decorrelating read + explicit-edge store), L3 cerebellar consequence-lane **WALL** (additive ≤ full → binding INERT; STEP-0 BIND was a toy `⊙` artifact ⇒ = trunk-objective floor), integrated **DIRECTIONAL** (held but not `--py` scoring path). Escape is **capability-specific**: works for associative completion (G1), fails for consequence forward-model (G6, same INERT verdict as mouth-readout family).

**Next #1 (rung 3/4, L5 only — the sole GREEN):** port DG-decorrelate + CA3-completion into a **live `core/` op over the `.kosmos` anchor store** (reuse `a_kosmos`) + `kosmos_io`/`brain_decide`, wired DISJOINT from emit-drive lanes {0,4} Ψ + §ImmuneMemory recall_thr (`a_substrate_disjoint`), re-measure **byte-exact via `anima evaluate --py`**, then ARCHITECTURE.json lockstep. **Gate the cement** on the G1-vs-G2 novelty discriminator (novel-chain vs stored-recall) so the explicit-store advantage doesn't masquerade as trunk recombination. Secondary ($0): escalate `integrated` to rung-2 through the `--py` scoring path with centering. Not the priority: any further binding/readout/consequence-lane lever (L3 confirms trunk-objective floor; **γ trained-constructive-bind remains the only untested arm**).

## Infra / honesty notes
- **BLOCKED-INFRA (rung-3 only, not any rung-2 verdict):** mini's compiled `anima`/`hexa` binary fails to link (`_hexa_ffi_dlopen`/`dlsym` undefined, arm64). Both L5 and L3 therefore used the **py-canonical path** (`a_eval_py_canonical`, TERMINAL-eligible) for reps — valid for rung-2. The rung-3 `.hexa` core smokes need a working hexa toolchain on pool/pod.
- No OOM / decode-hang / reboot on any lane; mini was sufficient at this extraction scale (single 303M forwards, no best-of-K, RSS 3.7GB).
- Artifacts stayed in each lane agent's worktree (returned as JSON, not synced to main tree) — main bookkeeps H_9129; no commit/PR from the lanes (per instruction).
