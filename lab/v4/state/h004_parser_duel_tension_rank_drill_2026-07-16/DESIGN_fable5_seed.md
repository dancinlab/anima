All grounding in hand — H_003's clean template (arms, DEAD floor 0.05, liveness 0.85, n=192 panel, d=384 L=4 ×2-seed MPS envelope) and mech-1's standing nodes (`mech-1.tension`, `mech-1.falsifier` with clause (3) BROKEN, L1/L2 STANDING). Here is the gate design.

---

# H_004 seed — mech-1 파서 결투: the binding drill

**Claim under test**: the per-edge parse-disagreement field T (n×n, A=L→R parser vs G=R→L parser) — *as a field, not as its scalar summary* — is causal for a held-out binding operation the trunk doesn't do cheaper. This replaces mech-1's broken clause (3) (`mech-1.falsifier`: trivially passable, mirror of H_001). Clauses L1 (eff-rank ≤ 1 ⇒ DEAD) and L2 (resolver→union ΔCE < 0.01 ⇒ DEAD) stand unchanged and are folded in below as F4/F5.

## 1. Literature scan (direct bearings only)

| Evidence | Bearing |
|---|---|
| Liang, Klein & Jordan 2006/2008 (agreement-based learning: two *directional* alignment models trained to agree) | Closest positive ancestor: two-directional disagreement is a usable training signal. Gap: shows agreement-*training* helps the towers — never that the disagreement field is a serialized carrier at inference. |
| RNNG (Dyer et al. 2016); Kuncoro et al. 2018–19; Hu et al. 2020 (SyntaxGym) | Explicit structure in small models improves *held-out syntactic generalization* — supports real headroom at the d=384 scale. Gains shrink with model scale; irrelevant here (we're tiny). |
| Murty et al. 2023 (Pushdown Layers) | Structure resident in the inference graph (nc5) helping generalization — the one recent positive for exactly that placement. |
| Murty et al. 2022 (tree projections) | Threat evidence: trunks become implicitly tree-like on their own → the trunk may do binding cheaper. This is why L2 (F5) must be in the verdict, not the appendix. |
| Latent-tree induction: PRPN / ON-LSTM (Shen et al.), URNNG / Compound-PCFG (Kim et al.), DIORA (Drozdov et al.); **Williams et al. 2018 (TACL)** | The strongest *negative* prior: induced-tree quality is inconsistent and downstream utility ≈ 0. The nearest family to "learned parse signal helps an LM" mostly failed causally. Prior on DEAD is high — hence cheap-first. |
| Sinha et al. 2021; Pham et al. 2021 (word-order insensitivity) | Trunks solve much of NLU orderlessly → any panel not F7-audited against orderless heuristics is free. Constrains panel design (§3). |
| Query-by-committee (Seung et al. 1992); co-training (Blum & Mitchell 1998) | Disagreement between hypotheses carries *uncertainty*, never shown to carry a *cognitive operation*. **THIN — the mechanism's core bet is essentially unattested.** |
| Korean: KLUE-DP (Park et al. 2021); psycholinguistics on prenominal-RC attachment + honorific agreement (Kwon et al.) | Attachment/honorific binding is real and human-hard in Korean. LM-side evidence at jamo/char scale: **none — THIN.** |

Net: structure-in-graph has positive priors at small scale; *disagreement-as-carrier* has none. The gate must be $0-first and built to let DEAD be the primary reading.

## 2. The one-variable lever — post-parse tension policy

H_003's lever was a post-encode span policy; the analog here is a **post-parse policy on the tensor handed to the resolver R**. Both towers run in every arm; corpus, vocab, model, steps, seed byte-identical; the *only* delta is a mathematical policy on T. (Cleaner than H_003, where corpora differed by 3–5% of tokens — here the corpus delta is zero.)

| arm | resolver input | isolates |
|---|---|---|
| **A-duel** | T = per-edge disagreement(P_A, P_G), untouched | the mechanism |
| **A-rank1** | best rank-1 approximation of T (per sentence, Frobenius-norm-matched) | **the control** — v1 died rank-1; if a scalar-grade summary does as well, the "field" is an emit-bit with extra steps |
| **C-plc** | P·T·Pᵀ, fixed random conjugate permutation per sentence (spectrum preserved exactly, edge-alignment destroyed) | placebo — "any tensor of this shape/spectrum regularizes R" vs "the edge-aligned content is used" |
| **C-scaf** | T ≡ 0 (resolver still in graph) | leak check / not-free floor |
| **C-perm** | A-duel trained on permuted gold | harness check |

Conditional 6th arm on F1 pass (H_003's C-syl role): **A-self** — T computed from two same-direction seeds of A, testing whether the *direction* opposition (the Korean-agglutination story, `mech-1.parser-duel` role) matters or any parser pair does.

## 3. The panel — HON-BIND (binding made visible, heuristics at 0.5)

Task: prenominal-RC attachment forced choice, disambiguated only by **honorific binding**. Frame: `[RC-verb(±시)] N1-의 N2-가 …`, where exactly one of {N1, N2} is honored (선생님-class vs 아이-class), position counterbalanced. Gold bit = `honorific(-시- in RC-verb) XOR position-of-honored-noun` — the H_003 XOR construction (`H_003 card §ceiling-problem`) transplanted from depth-parity to attachment:

- presence heuristic (“-시- present ⇒ attach high”) → 0.500 on a 50/50 panel;
- locality heuristic (attach to nearest noun) → 0.500;
- particle/lexical-lookup → 0.500 (both nouns carry identical case marking; honored-noun identity balanced across gold bits).
- All three verified **closed-form by an F7 audit before any training** (reuse `build_panels.py` discipline).

Resolving it requires connecting a verbal morpheme to the correct head across an ambiguous edge — precisely an entry of T. No negator anywhere in the panel (keeps distance from the closed codec axis).

Panels, campaign convention (f1/f2 are PANEL names, not F-measures; metric is d_acc, chance 0.5, ceiling 1.0):
- **f2′ (verdict, OOD)**: held-out honored-noun lexeme × both attachment heights × both honorific settings, fully crossed, 50/50 per cell, **n=192** (σ ≈ 0.036, as in H_003).
- **f1′ (liveness)**: drilled nouns, held-out conjugation, n=64; f1′(A-duel) < 0.85 ⇒ measurement DEAD, no verdict.

## 4. Falsifiers + admissibility pre-check (arithmetic, before any code)

Anchors: H_003 measured a trained-but-crippled arm at 0.6094–0.6823 (arm **A-shat**, f2, `state/h003_atomicity_fixed_codec_drill_2026-07-16/verdict.json`) and scaffold at 0.4948–0.5000 (arm **C-scaf**, same path). Estimates: E[A-rank1, f2′] = **0.60** (scalar summary retained, so above scaffold, below mechanism); E[ceiling, A-duel f1′] = **0.90**.

- **F1 (primary)**: Δ = d_acc(A-duel, f2′) − d_acc(A-rank1, f2′). SUPPORTED iff Δ ≥ 0.15 both seeds; DEAD iff Δ < 0.05 both; else PARTIAL.
  - *Reachable*: 0.15 ≤ ceiling − control = 0.90 − 0.60 = **0.30** ✓ (2× inside headroom; H_001's dead gate was 0.083 < 0.1 ✗).
  - *Not-free*: the bar is a gap over a **trained, both-towers-running** control — scaffolding alone cannot clear it by construction, and F3 checks the floor empirically.
  - *One variable*: the arms differ in a single per-sentence projection of one tensor ✓.
  - *Both answers reachable*: DEAD needs only A-duel ≈ A-rank1 ✓.
- **F2 (liveness)**: f1′(A-duel) < 0.85 ⇒ measurement DEAD (no F1 verdict).
- **F3 (not-free)**: f2′(C-scaf) > 0.60 (= chance + 2.8σ) ⇒ grid leaks ⇒ no verdict.
- **F4 = standing L1, made causal**: descriptive eff-rank(T) on held-out ≤ 1 ⇒ DEAD (pre-run check, $0).
- **F5 = standing L2**: resolver→union substitution at inference, ΔCE < 0.01 AND Δd_acc(f2′) < 0.05 ⇒ the decoder never needed the resolution ⇒ DEAD.
- **F6 (placebo)**: d_acc(A-duel) − d_acc(C-plc) ≤ 0.05 ⇒ placebo void, content unused ⇒ measurement suspect, no SUPPORTED verdict.
- **F7**: closed-form heuristic audit of both panels pre-freeze (as H_003).

All E-values must be re-confirmed by G-1 (below) before `pre_register_frozen: true` — estimates are not anchors (`adm.4`: every number above is cited with its arm or marked E).

## 5. Cheapest-first path

**Gate 0 ($0, closed-form)**: generate panels; run the F7 heuristic audit; verify the rank-1 projection actually removes mass (report fraction of ‖T‖² off the top singular direction on sample parses — the analog of H_003's 3–5% corpus-delta audit; < 20% off-top ⇒ T is already near-rank-1 ⇒ F4-dead at $0).

**Gate 1 ($0–$ε, CPU, no mechanism training — the H_001/H_002-style re-analysis)**: build two cheap directional proxy parses (deterministic head-final L→R automaton vs R→L; or minutes-scale trained taggers on the drill grammar), compute T on the panel, then fit three logistic probes predicting the gold bit: **probe(vec T)** vs **probe(rank-1 T)** vs **probe(scalar ‖T‖)**.
- probe(vec T) ≤ probe(rank-1 T) + 0.05 → the field carries nothing beyond its scalar *even before learning* → premise unsupported at $0; stop or redesign. (Honest scope: proxies aren't the learned duel, so this is a spend-justification gate, not an automatic mechanism death.)
- probe(vec T) ≥ 0.75 while probe(rank-1 T) ≤ 0.60 → headroom is real; training spend justified (실측전 research satisfied).

**Gate 2 (training, only after G-0/G-1 green)**: H_003's exact envelope — d=384 L=4, 2 seeds × 5 arms, local MPS, ~6h, $0 cash. Resolver R = small bilinear head over T → structure embedding; decoder conditioned **only** on resolved structure (`mech-1.l2-defense`). No QFORGE/QE spend at this stage.

## 6. Honest kill-conditions — the three ways this is secretly the old corpse

1. **Secretly mech-3 (the codec in a trenchcoat)**: on jamo-level input the two directions disagree mostly at *morpheme boundaries*, so T is a segmentation signal and R is re-doing the codec. In the numbers: G-1 shows MI(T; boundary-indicator) ≈ MI(T; everything); masking boundary-adjacent cells of T leaves Δd_acc unchanged; A-duel's gain reappears on a boundary panel but dies on HON-BIND. Any of these → the codec axis re-entered through the back door; stop.
2. **Secretly rank-1 (v1's death repeated)**: A-duel − A-rank1 < 0.05 both seeds while A-duel − C-scaf ≥ 0.15 — the duel helps but its scalar helps equally. By design this *is* F1's DEAD reading (the most likely failure is the primary measurement, not a confound). Early tell at $0: G-1 probe separation ≤ 0.05, or G-0 off-top mass < 20%.
3. **Secretly free (capacity, not content)**: C-scaf > 0.60 (F3) or A-duel − C-plc ≤ 0.05 (F6) — any tensor of that shape regularizes the decoder into the answer, and the falsifier would certify the resolver's capacity, not binding. Either ⇒ measurement dead, no verdict; tighten the resolver bottleneck or the panel, then re-freeze.

**Family propagation** (`fd.family-structure-conflict`): mech-1 and mech-6 are the same family ("learned resolver settles conflicting structure proposals", N=2 vs N>2). A DEAD here — especially via kill-condition 2 or 3 — is pre-declared to count as half a verdict on mech-6, so the fake-diversity audit can't be re-litigated later.

---

Recommended registry entry: **H_004 · slug `parser-duel-tension-rank-drill`** — "the parse-disagreement FIELD (not its rank-1 summary) causes held-out honorific-binding resolution; one variable = post-parse tension policy (full vs rank-1), Δd_acc ≥ 0.15 on a panel whose heuristics sit at 0.5." Gates G-0/G-1 are runnable today at $0; nothing is spent until they're green.