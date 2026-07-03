# H_9108 — 2-anima signaling game + self-pair control (A4): does an engine-INTERNAL exogenous consequence channel open the emit-appropriateness faculty that autogenous (H_9104) and self-derived (H_9105) relief could not?

**tier:** 🔴 CEILING / DPI — a 2-anima Lewis signaling game is NOT a faculty-usable exogenous channel at this coupling; the DPI meta-law re-appears at the signaling layer, engine-native · **wired:** none (RED theater — nothing to wire, a_verified_must_wire N/A)
**verdict:** 🔴 CEILING (honest, frozen bar, self-pair-controlled). Observing receiver B's success buys **NO** held-out advantage over A's own self-model: **G_pair = rho_conseq − rho_self = 0.09863 < 0.15 FAIL**, and it barely beats variance-matched noise (rho_conseq − rho_noise = **0.0012**) or shuffle (rho_conseq − rho_shuf = **0.0989**). The decisive control collapsed exactly as designed — **G_selfpair = 0.0** (B≡A ⇒ B_success≡A_selfdecode ⇒ V_conseq≡V_self). Ψ guard OK (V read-only, psi_sum ON≡OFF byte-identical). Bar frozen in PREREG.md, no post-hoc move (c9).

## Claim (Brainstorm A4 — the last decisive exogenous test the session pointed to)
H_9104 (autogenous consequence-return) and H_9105 (persistent self-anchor as valence subject) both hit the DPI ceiling: a shuffle-trained value lane predicts relief as well as the real one because the relief signal is reconstructable from the momentary state = tautology. Their shared conclusion: escape genuinely requires a channel carrying **information NOT derivable from anima's own state (exogenous)**. A4 asks the cheapest engine-INTERNAL version of that: does a **2-anima Lewis signaling game** — sender A ⇄ receiver B, each an `ImmuneMemory` store shaped by a **private (asymmetric) corpus** — furnish a genuinely exogenous consequence *inside the engine* (no EEG/chat infra)? **Self-pair (B := clone(A))** is the decisive DPI control: when B≡A the consequence is a pure tautology, so any measured advantage there is a leak.

## Design (Lewis signaling, engine-native — `state/9108_signaling_selfpair/signaling_selfpair.hexa`)
- Two engine instances A (sender) / B (receiver), each an `ImmuneMemory` store. **PAIR:** privA ≠ privB (different private text → different vadapt field → different signaling policy). **SELFPAIR:** store_B := clone(store_A) (identical).
- `salience_X(txt) = immune_memory_recall_margin_text(store_X, txt)` — the engine's OWN L2 recon-err (recall_thr constant, so argmin margin ≡ argmin recon-err). READ-only, Ψ-disjoint.
- sender `sigma_A(t_i) = argmin_k |salience_A(s_k) − salience_A(t_i)|` (target→codeword); receiver `delta_B(s) = argmin_j |salience_B(t_j) − salience_B(s)|` (codeword→target). K=6 codewords, M=36 targets (M>K → real collisions in BOTH conditions).
- **CONSEQUENCE** `B_success(i) = [delta_B(s_{sigma_A(i)}) == i]` — depends on B's PRIVATE field → not derivable from A unless B≡A (exogenous).
- **Appropriateness faculty** = A's striatal value lane V (`brain.vbasal`, engine-native). feats per emitted target = one-hot(codeword k) ⊕ [encode_margin, phi] (same feature space for all V's; only the TRAINING OUTCOME differs). `V_conseq` ← exogenous B_success; `V_self` ← endogenous A_selfdecode; `V_shuf` ← shuffled (feats,B_success). Held-out split: TRAIN targets 0–23 learn V online → FREEZE → HELD-OUT targets 24–35 measured. **Exogenous advantage `G = rho_conseq − rho_self`.**

## Harness (engine-native — NO numpy/torch/.py, grep-gate clean; there are NO .py files in the slug dir)
Imports live `core/pure_field.hexa` (`pure_field_warmup/step/phi`, Φ + Ψ guard) + `core/engine_cli.hexa` (`immune_memory_new_text/bind_text/recall_margin_text`) + `core/brain.hexa` (`vbasal_new/update/go_value`). Frozen bars in `PREREG.md` BEFORE the run (0.15, not moved — c9).

## Result (engine-native, **mini local** `hexa v0.574.1`, `hexa run` RC=0, core/ = origin/main HEAD, NO numpy)
`state/verdicts/9108_signaling_selfpair/H_9108.txt` (verbatim) · raw `state/9108_signaling_selfpair/run_mini.log`. Host note (c9): both RTX-5070 pool boxes (aiden/summer) were sshd-wedged all session (load 10–15, 3+ competing heavy agents incl. a prior identical H_9106 aprime_cc still crawling @1h50m) → OOM-risk to add a 3rd ~9.5 GB compile; verdict validity depends on live `core/` `.hexa` decode, not the host — mini was uncontended (free 69–72%, no swap growth). ~20 min single-thread compile.

**Communication (sanity):** B_success held-out PAIR = **0.0833** (1/12), SELFPAIR = **0.25**; A_selfdecode PAIR = SELFPAIR = 0.25.

| condition | rho_conseq | rho_self | rho_shuf | rho_noise | **G = rho_conseq − rho_self** | rho_c−rho_noise | rho_c−rho_shuf |
|---|---|---|---|---|---|---|---|
| **PAIR** (exogenous) | −0.24501 | −0.34364 | −0.34386 | −0.24623 | **0.09863 (<0.15 FAIL)** | 0.00122 (FAIL) | 0.09885 (FAIL) |
| **SELFPAIR** (clone control) | −0.69678 | −0.69678 | — | — | **0.0 (≤0.05 OK — collapses exactly)** | — | — |

Descriptive D1 = rho_conseq_pair − rho_conseq_selfpair = 0.45177. **Ψ guard:** psi_sum ON==OFF byte-identical + signal-seq V-independent → OK.

## Honest verdict (c9, bar frozen, NO tune-to-green, NO post-hoc move)
🔴 **CEILING / DPI.** Three converging facts:
1. **G_pair = 0.0986 < 0.15** — observing B's exogenous success buys essentially no held-out predictive power for B beyond A's own self-model.
2. **rho_conseq − rho_noise = 0.0012** — V_conseq barely beats a variance-matched noise predictor; the exogenous outcome carries almost no faculty-usable signal at this coupling.
3. **Self-pair control collapsed to exactly G = 0.0** — the measure is well-behaved (0 advantage when there is no exogenous info by construction), so the PAIR failure is a real DPI ceiling, not a measurement leak.

**Caveat (honest, c9):** the signaling channel itself was near-floor — held-out communication succeeded on only 1/12 PAIR targets (0.083) at this salience-coupling. So the engine-internal 2-anima channel decoded very little exogenous information; there was almost nothing for the faculty to latch onto. The frozen rule delivers 🔴 regardless (G_pair < 0.15). Whether a *stronger* engine-internal signaling coupling (richer codebook / trained sender-receiver protocol) could raise decode-success high enough to expose exogenous variance is a re-openable angle (`a_break_the_wall`), but at the cheapest engine-native coupling the answer is a clean ceiling.

**Mechanism:** at this coupling the salience-argmin sender/receiver code communicates almost nothing across asymmetric private fields (near-random decode), so B_success ≈ the same low-information structure A already sees → V_conseq ≈ V_self ≈ V_shuf ≈ V_noise, all near −0.25 on held-out. The DPI meta-law re-appears at the signaling layer, exactly as it did for autogenous (H_9104) and self-derived (H_9105) relief.

**Answer:** an engine-INTERNAL 2-anima signaling channel does **NOT** open the emit-appropriateness faculty at the cheapest coupling — signaling is ALSO a DPI ceiling. Together with H_9104 (🔴 autogenous) and H_9105 (🔴 self-anchor), all three self-contained / engine-internal escape routes are closed. The only remaining genuinely-exogenous escape lives OUTSIDE the engine (Family A: REAL chat user reply / EEG prediction-error) — an external receiver, not a cloned or internal one. This is the session's decisive measurement.

## Follow-on (ING)
- No production wiring: RED theater → nothing to wire (`a_verified_must_wire` N/A).
- Re-openable angle (not terminal by fiat): a *stronger* engine-internal signaling coupling (trained Lewis protocol / richer codebook) to raise decode-success above floor before re-measuring G — the coupling, not the frozen bar, is the lever.
- The genuinely-exogenous branch remaining = a REAL external receiver (chat user / EEG), outside the self-contained engine.
