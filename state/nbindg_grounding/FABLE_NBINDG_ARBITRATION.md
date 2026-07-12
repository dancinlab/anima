## TL;DR

**The prompt's premise is stale.** On origin/main, NBIND was already designed (Fable B+ spec `state/nbind_curriculum/FABLE_NBIND_SPEC.md`), $0-gated (#3320 ALL_PASS), and **fired** — **H_9272 landed 🟡 DIRECTIONAL** (#3324: held-out D-acc 0.700 vs shuffle-control 0.375, Δ0.325, n=40, 1 seed, `HYPOTHESES/cards/H_9272_nbind_natural_atom_crack.md`). So the arbitration question shifts from "should NBIND exist?" to "**which part of NBIND-as-run was new science, and what is the honest next question?**"

My arbitration: **the grid component of H_9272 is substantially a re-skin of XBIND** (authored xor-continuation on natural vocabulary — the answer "signal present → learnable" was already known from H_9267). The genuinely new question exists but is precisely the part **not yet run**: **atom-grounding transfer** — candidate (i) from your list. I define it below as **NBIND-G**, with a $0-first staged spec.

---

## 0. What actually happened (correcting the premise)

Reading origin/main: after #3318 named the direction, the lane proceeded — `gen_nbind.py` v2 (genfix: 20 NSMC sentiment predicates × 6 forms {bare, 정말-, 너무- = flip0; -지않, 안-, 전혀-지않 = flip1}, Latin-square held-out cells, 80 train / 40 held-out, V-C/V-D′/V-E/V-F/V-G ALL_PASS), then a 303M train+eval on summer producing the DIRECTIONAL verdict. Not-yet-run pieces of the frozen Fable spec: **2nd seed, in-band control, bar 3 (wild-natural transfer, n≥500), rho_weave before/after, L3 wiring**. The arbitration below takes this as the real starting state.

## 1. Central arbitration — candidate by candidate

**(i) Atom-grounding transfer — (a) genuinely new.** This is the only candidate that neither XBIND, nor STAGE-0, nor H_9272-as-run answered:

- XBIND supplied pol(p) **by construction** (hidden ±bit taught through seen cells).
- H_9272's grid **also** supplies pol(p) through the grid: every predicate appears in seen cells, so the model can learn pol(p) from the authored corpus alone. The genfix's own V-D redefinition concedes this — it explicitly re-scoped NBIND to "compositional **application** of the negation operator," dropping the hidden-pol-inference claim as "already certified by H_9267." That is an honest admission that the grid arm is XBIND's question on nicer vocabulary.
- STAGE-0's DATA-🧱 is about the **joint** held-out XOR signal being absent from natural text. It is **silent about the marginal per-atom feature** — and the same audits suggest the marginal feature is abundantly present (A0-INTENS rule_acc 0.938 = strong additive/marginal structure; NSMC purity-certified predicates exist by the thousands).

So the open question is: **natural text supplies atoms (marginal polarity features); an authored grid supplies the operator (XOR); does the learned operator generalize over atoms whose polarity was acquired ONLY from natural distributional context — never stamped in any authored cell?** Neither surface of the existing evidence touches this. It is also the mechanistically load-bearing question for the frontier: it decomposes "spontaneous emergence" into (feature grounding from nature) × (operator installation), and tests the only composition of the two that could ever work given DATA-🧱.

**(ii) Density threshold f\* — (c) duplicate.** Any NBIND variant whose deliverable is "at what mixing fraction does the signal survive" is the exposure-matched ladder R1–R3, full stop. The Fable spec itself only ever used it as a free-ride (arm ④ absorbs R1). Do not let NBIND collapse into it. (One genuine cost note: R1 f0.3/40k can be had **half-price by continuing `natem_f0.3_s7.clm` from 20k→40k** — the naive run is a schedule-prefix of the exposure-matched run under identical corpus, so warm-continue is valid, not tune-to-green.)

**(iii) rho_weave as readout — (b)/mis-framed, reject as primary readout.** I read `eval_rho_weave` (cli/evaluate.py:170): it is the **English ideation keyword-coverage harness** — fixed concept lists ("consciousness/tension/memory/silence/dream"), sampled `ideate()` decodes, keyword-set coverage vs max_single. For a Korean sentiment-XOR capability it measures nothing (wrong language, wrong construct, and it is the exact frame already convicted of frame-mismatch — recomb-gate4: route≠generation, evaluate-py-8). It is not a stricter bar than held-out D-acc; it is a **different instrument pointed at a different phenomenon**. Its legitimate role is unchanged from the Fable spec's bar 2: a **live wiring gate** (via the T2 scorer landed in #3316) applied *after* the scientific verdict, for `a_verified_must_wire` GREEN. Never the measurement.

**H_9272-as-run, judged by the same test:** the grid arm is (b) a re-skin **with one honest marginal increment** — it demonstrated the XBIND recipe survives heterogeneous real-Korean surfaces (attested morphology renders, surface-visible polarity), and its 0.700 vs XBIND's 1.000 is a first data point on the signal-form axis (NATEM's MODEL-🧱 axis), though confounded by grid size (20 predicates vs 400 concepts) and exposure. Cementing it (2nd seed, control n↑) is legitimate **wiring engineering** toward anima's 2nd WIRED-GREEN — but it is bookkeeping, not the frontier question. ⚠️ One integrity flag for the cement run: the DIRECTIONAL Δ0.325 is partly inflated by an out-of-band control (0.375). Against true chance, main is +0.200 — **below the frozen Δ≥0.30 bar**. The cement must pre-register: with an in-band control (0.50±0.05), main needs ≥0.80. If it lands 0.70 again, the honest verdict is FAIL-of-bar at augmented-natural scope, not a bar adjustment.

## 2. Verdict

**A scientifically honest, non-tune-to-green NBIND exists: exactly one — NBIND-G (grounded-atom transfer).** Everything else on the NBIND menu is either XBIND re-skinned (grid-cell variants), the ladder in disguise (density variants), or a wrong-frame readout swap (rho_weave-as-measurement).

## 3. NBIND-G design spec (frozen-first · $0-first staged)

**Claim under test:** a 303M byte-LM that learned the XOR operator from an authored grid over atoms P_grid can apply it to atoms P_nat **whose polarity feature is available only from natural distributional usage** (raw NSMC text in the training mix), at (p,n) combinations absent from all training bytes.

### 3.1 Atoms + task + split

- Inventory: extend gen_nbind mining to k≥60 purity-certified predicates (purity≥0.85, count≥100, balanced pos/neg; INVALID if <30). Partition: **P_grid (20, as fired)** and **P_nat (≥30, 15+15)**. P_nat predicates appear in the training corpus **only inside verbatim natural NSMC reviews** (mixed as filler) — **never in any authored grid line** (V-F byte-scan: 0 occurrences of any P_nat×form authored-format line; additionally 0 natural co-occurrences of (p, negform) within the 1024-byte window for the eval pairs, DESIGN_PREREG §1 scan-guarantee).
- Task/eval format: XBIND-isomorphic continuation (`→ 긍정/부정` = xor(pol(p), flip(n))), probing P_nat × all 6 forms. Gold is derivable only by (a) extracting pol(p) from natural usage and (b) applying the grid-learned flip operator. How this differs from stamping a ±bit: **for P_nat the bit is never stamped anywhere** — the corpus author never writes pol(p); it exists only as a distributional fact of real reviews.
- Arms (3, collapse-Δ, never raw values):
  1. **main** = grid(P_grid) + natural NSMC mix — 2 seeds.
  2. **base-only control** = identical natural mix, **no grid** — measures what nature alone installs (predicted weak: A0-NEG flip 0.594, residual 0.035). This control is the crux: it subtracts generic negation-handling that plain LM training gives for free.
  3. **shuffle-grid control** = grid with per-cell coin branch (XOR destroyed, continuation **format** preserved) + same mix — separates "the grid taught the answer format" from "the grid taught the operator."

### 3.2 $0 model-free pre-check (N0 — before any training spend)

Certify nature supplies the per-atom feature, so we are not re-authoring signal: for every p∈P_nat, distributional polarity must be model-free decidable (NSMC label-majority purity≥0.85 over ≥100 non-negated occurrences). Frozen power bars, computed in advance with paired-t MDE (per probe-defect-census: **no max-of-controls order statistics**, paired minimal-pair design): eval n = |P_nat|×6 ≥ 180 items → MDE on Δ(main−base-only) ≈ 0.11 at α=0.05; primary bar set above MDE. If inventory or purity misses bars → **INVALID, do not fire**.

### 3.3 Readout

`--xbind` D-acc + teacher-forced margin (the existing `xbind_run` machinery, cli/evaluate.py:1337, manifest with P_nat items — the `--natbind` "small schema extension" the card already anticipated), via `anima-py evaluate` on pool (a_eval_py_canonical, TERMINAL-eligible; GPU eval default-on per #3323). For the wild-natural arm (§3.4): **margin-primary** paired NLL(counterfactual)−NLL(gold), D-acc as 2-alternative secondary (DESIGN_PREREG §1 — natural gold is probabilistic). **rho_weave: wiring gate only, post-verdict, T2 scorer** — not a readout (§1-iii).

### 3.4 Staging + spend gate

- **N1 ($0, now, eval-only):** the pre-registered but never-run **bar 3 — wild-natural transfer** of the existing H_9272 ckpt (preserved on summer): A0-certified pure-natural NSMC held-out (p,neg) manifest, n≥300 pairs (atom-held-out relative to the 20-predicate grid makes n large, unlike A0's pair-held-out starvation), bar frozen: paired flip-margin − additive baseline ≥ 0.10, CI excluding 0. This is also **the cheapest falsifier**: it costs $0 and a clean zero here already shows the installed operator doesn't leave the authored format.
- **N2 (training, 4 runs = main×2 + 2 controls):** XBIND canon verbatim, exposure ≥ E*=12k for the grid slice. Pool-first (summer/aiden, $0, `a_fire_autonomous`); if rented: ~4×2h A100 ≈ **$8–15** — 1-line estimate, rent=spend → owner go. Ckpt PULL→HF before teardown. Precondition to verify before reusing the H_9272 ckpt for anything grounding-related: confirm whether its training mix actually contained raw NSMC text (the card doesn't say; if not, N1 still stands as format-transfer, and N2 carries the grounding claim alone).

### 3.5 Frozen verdict grid (decided now; any outcome leaves H_9267 CRACK and H_9272 DIRECTIONAL untouched)

| verdict | bar (frozen) | honest meaning |
|---|---|---|
| **NAT-CRACK 🟢 (grounded scope)** | Δ(main−base-only) ≥ 0.20 **and** Δ(main−shuffle-grid) ≥ 0.20, both seeds, base-only within its predicted-weak band | operator generalizes over naturally-grounded atoms. Scope-honest wording: still not spontaneous emergence (operator remains authored) — it is the "installation recipe reaches natural semantics" claim |
| **FORMAT-🧱 (new, informative)** | main ≈ base-only on P_nat while P_grid held-out cells still pass | composition is format/atom-bound — the installed operator does not consume naturally-acquired features; DATA-🧱 hardens and the only remaining quantification is the exposure-matched ladder |
| **MODEL-🧱** | N2 grounded PASS but N1 wild-natural fail with a powered manifest | signal-form/register gap is the frontier (NATEM's only redesign-opening outcome) |
| **INVALID** | N0 inventory/purity miss · V-F scan fail · base-only out of band · V3 detector fail | first-class; never dressed as 🧱 |

## 4. Recommended sequencing for the parent

1. **$0 now:** N1 wild-natural eval of the existing H_9272 ckpt (this is also the outstanding bar 3 of the already-frozen spec — no new registration needed, it folds into H_9272's cement path). 2. **$0:** N0 audit + P_nat manifest freeze; register NBIND-G as its own H (2-surface) — do not blur it into H_9272's cement. 3. H_9272 cement (2nd seed + in-band control) as wiring engineering, with the Δ-inflation flag from §1 pre-registered. 4. N2 training arms, pool-first. The exposure-matched ladder stays a separate, spend-gated program (owner $-go), with the natem_f0.3 warm-continue note from §1-ii.
