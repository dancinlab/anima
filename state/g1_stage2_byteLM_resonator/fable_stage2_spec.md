Spec grounded on the stage-1 harness (`state/g0g6_premise_b_derisk/`), `cli/evaluate.py`'s `_Mouth`/`g_eval_g1` path, and the `anima corpus`/`--py` single-entry rules. One correction to your framing first: the cleanest LM-native design makes **arm A the LM itself** (no separate classifier head) and **arm B a read-path swap on the identical trained trunk** — one training run per seed, three read-paths. That's what makes B-vs-A a pure operator comparison.

---

# Stage-2 spec — byte-surface + LM-objective resonator read-head

**H registration first** (a_hypothesis_register, 2 surfaces): H card ≈ "G1 wall is a property of the CE read-path, not the byte-LM trunk: a fixed HRR bind/unbind/cleanup read-head over LM-learned byte atoms recovers held-out recombination that the trunk's own CE decode cannot." Pre-register bars in `state/g1_stage2_byteLM_resonator/PRE-REGISTER.txt` **before** first fire.

## 1. Byte surface + LM objective

**Names.** R=6 roles, F=30 fillers. Each gets a distinct random name: 4 bytes, lowercase `a–z`, rejection-sampled unique, drawn from a seed-pinned RNG **independent of ID structure** (the held-out rule `r ≡ f mod 6` lives in ID space only — surface form cannot encode it; this is the anti-leak property, checked in §6).

**Scene line** (one training example = one byte line):

```
kova=belu;rin=tass;murp=peld;?rin=tass\n
```

- 3 pairs per scene, roles distinct within scene; query role sampled uniformly from the scene's roles; answer = its filler's bytes verbatim.
- Genuine next-byte CE over the **entire line** (copying the pairs is part of the loss; recall is the tail). No classification head anywhere.
- Train: ~20k scenes over the 150 train pairs (held-out = 30 pairs with `r ≡ f mod 6`, never bound in any train scene; every role and filler individually appears in many train scenes — coverage asserted like S1's coverage-gap assert).
- Eval sets: **held-out** = 600 scenes each containing exactly one held-out pair (other 2 pairs from train pairs), query = the held-out role. **in-dist val** = 600 unseen scene combos of train pairs.
- Score = exact byte match of the emitted answer up to `\n`. Chance ≈ 1/30 for codebook arms.

**Model (the shared substrate, one per restart).** Causal byte-transformer: 4 layers, d=256, 4 heads, block 64, vocab 256, AdamW 3e-4, batch 256, fp32, train to train-answer-acc = 1.0 + plateau (cap 20k steps). Minutes per restart on aiden; 10 restarts.

**Atom extraction (shared by B/C/A′).** `e(name)` = final-layer hidden at the last byte of `\n<name>` run standalone (never in scene context — context extraction is the leak vector, banned). Unit-norm, then apply a **fixed seed-pinned random orthogonal Q** (drawn before training, never trained, data-independent) to condition anisotropic trunk states for HRR. Q is parameter-free conditioning, not learning.

## 2. The arms (one trunk, four read-paths)

| arm | read path | learned | fixed |
|---|---|---|---|
| **A** | trunk's own autoregression: prompt through `?<r_q>=`, greedy to `\n` | everything (it *is* the LM) | — |
| **A′** | codebook-constrained A: argmax over 30 fillers of LM log-prob of that filler's bytes after the query prompt | same trunk | output space |
| **B** | `s = Σᵢ Qe(rᵢ) ⊛ Qe(fᵢ)`; `f̂ = s ⊘ Qe(r_q)` (circular correlation); cleanup = cosine argmax over `{Qe(f_j)}`; **emit that filler's stored byte-string** | atoms only (via trunk) | ⊛, ⊘, Σ, cleanup, byte emission (lookup) |
| **B0** | B on a random-init (0-step) trunk | nothing | everything |
| **C** | `s = Σᵢ (Qe(rᵢ)+Qe(fᵢ))`; `f̂ = s − Qe(r_q)`; same cleanup | atoms | + instead of ⊛ |

B's "decode must emit bytes" answer: cleanup returns an atom index; the byte emission is a lookup of that atom's name — zero learned parameters between unbind and bytes. B receives the segmented pair list (same as stage-1); parse-free reading is explicitly out of scope for stage-2 (note it in the card — it's the honest scope line, not a hidden assumption). No whitening/recentring of atoms in the primary run (that would be fit-on-data); a whitened variant may be logged as diagnostic only.

## 3. A-variance: diagnosis + fix

Most likely cause is **genuine basin bimodality** — compositional generalization of a small LM is init-dependent (grokking-adjacent), not CUDA noise. But distinguish, don't assume:

1. **Pin determinism**: `torch.use_deterministic_algorithms(True)`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`, fp32, fixed seeds. Run seed-0 twice → must be bit-identical. If pinned same-seed still varies, it was nondeterminism; if identical, the spread across seeds is real.
2. **10 restarts, report the full distribution** (min/median/max, per-restart table verbatim into the verdict). No cherry-picking, no reruns of "bad" seeds.
3. **Underfit control** (kills the "A just needed more" objection): on 2 seeds, train A 3× steps and a 2×-wide variant; precondition train-acc=1.0 held in all; if held-out doesn't move, A's floor is generalization, not capacity/steps.
4. **Per-restart validity gate (pre-registered, not tune-to-green)**: A train-answer-acc = 1.0 ∧ A in-dist ≥ 0.95 ∧ B in-dist ≥ 0.95, else the restart is INVALID (reported, not resampled); >3/10 invalid → redesign, no verdict.

The robust bar is then distributional, not per-seed (§4) — and note the stage-1 fact that already survives variance: A's *best* seed (0.499) < B's *worst* (0.933). Stage-2 should re-check that dominance (`max(A′) < min(B)`) and report it, but not bar on it alone.

## 4. Frozen bars (pre-register verbatim; n=10 valid restarts; all arms measured per restart on the same trunk)

**GO — "operator escape survives byte surface + LM objective" (DIRECTIONAL-strong)**, ALL of:
- B median ≥ 0.80 ∧ B min ≥ 0.60
- (B − C) median ≥ 0.50 ∧ C median ≤ 0.20 ← load-bearing operator isolation
- (B − A′) median ≥ 0.30 ← the wall is in the read-path, output-space matched
- bind-destroy (⊛→+ at read time inside B, same atoms): B collapses to ≤ 0.20
- scene-shuffle (permute pair→scene assignment in B's memory before read): ≤ 0.13 (chance+margin) — B reads the memory, not priors

**KILL** any of:
- B median < 0.50 while B0 median ≥ 0.80 → the fixed algebra works on random atoms but **not on LM-learned atoms** — the wall re-asserts at the atom-geometry level; lane dead as specified
- (B − C) median < 0.20 → operator isn't the lever under LM training
- (B − A′) median < 0.10 → stage-1 B-win was the codebook restriction, not the algebra

Else 🟠 MIXED → diagnose (start with atom-geometry: pairwise cosines of learned atoms) before any further spend. Tier is capped at DIRECTIONAL regardless of outcome (torch, no `core/`) — bars gate the bridge, not a GREEN.

B0 is diagnostic, not a bar: B0≈B (both high) = win is pure algebra and survives *any* encoder — fine, proceed; B0≫B is the KILL case above.

## 5. Bridge to engine-native cement (minimum wiring)

Per `a_eval_py_canonical`, the py 2-production numpy path is TERMINAL-eligible — so the minimum cement does **not** require hexa/ρ-AXON porting:

1. **`core/resonator.py`** (numpy, torch-free, no archive imports): `hrr_bind/hrr_unbind` (numpy FFT), `cleanup(v, codebook)`, and `resonator_atoms(W, name_bytes)` deriving atoms from **engine-loaded** `.clm` weights via the same forward `cli/evaluate.py` already uses (`clm_load_weights` → `clm_forward` hidden states). ~100 lines.
2. **Trunk = a real `.clm`**: train the byte-LM via `anima train --py` (CLMConvMoE) on a corpus emitted by a new **`anima corpus rolefiller`** subcommand in `cli/corpus.py` (owner rule: all corpora through this single entry; derivtrace-style, procedural, held-out flag reuses `--held-out`).
3. **`cli/evaluate.py`**: add a resonator read-path arm to the G1 gate (e.g. `g_eval_g1` gains `read_path ∈ {ce, resonator}`, same frozen bars, CE arm = existing behavior untouched). Entry stays `anima evaluate --py <clm>` — no raw python, H-ANIMA-SINGLE-ENTRY intact.
4. Verdict: `hexa verify` → frozen `state/verdicts/` + card/jsonl update.

That yields a tier-cementing **MEASUREMENT** verdict. A full wired GREEN (`a_verified_must_wire`) additionally needs the read-head live in the chat decode path (`core/decode` / generator L3 — this is where a hexa `ρ·weave` port would eventually land) + ARCHITECTURE.json lockstep; that's the step *after* a cementing measurement, not part of stage-2's minimum. Heavy 303M runs on pool (summer/aiden), never mini.

## 6. Most likely rig + control

**Primary: codebook-restricted decode masquerading as operator escape.** B picks among 30 stored strings; A generates over 256⁵. B could beat A on output-space restriction alone, with the HRR algebra contributing nothing beyond "retrieve something plausible". **Control = arm A′** (above): identical trunk, identical 30-string output space, scored by LM log-prob. The load-bearing margins are B−A′ and B−C, both codebook-matched — B−A (free decode) is reported but never load-bearing.

Secondary leak detector (cheap, run once per restart): mean pairwise cosine of `e(r), e(f)` over held-out pairs vs a matched sample of non-held-out (r,f) non-pairs. If held-out pairs show elevated similarity, the encoder leaked the pairing structure through training co-occurrence of the individual atoms and B's cleanup is association, not unbinding → flag the run INVALID. (Names being iid-random and atoms being extracted context-free are the design-level guards; this is the empirical check on them.)

---

**Run order on aiden:** pin determinism → seed-0 twice (bit-identity check) → 10 restarts × {A, A′, B, B0, C, bind-destroy, shuffle, leak-check} → underfit control on 2 seeds → verdict table verbatim → bars decide GO(bridge §5) / KILL. Estimated $0 (aiden idle GPU, fp32 small model) — within a_fire_autonomous.