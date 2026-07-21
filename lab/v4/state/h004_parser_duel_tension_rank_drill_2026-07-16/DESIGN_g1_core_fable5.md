# H_004 G-1 core — proxy parsers · tension field T · rank-mass + probe gates ($0)

Delivered 2026-07-16 (Fable-5). Every number below is MEASURED by
`g1_core_check.py` → `g1_core_check.json` (CPU, deterministic, $0) on the built
panels (`panel_f2prime.json` n=192 · `panel_f1prime.json` n=64) and on the full
4^6 factorial of the proposed MULTI-BIND redesign — not asserted.

**Headline (honest, first)**: on the built single-bind panel the pre-registered
G-0 rank-mass and G-1 probe-separation gates **FAIL for a structural reason**:
the fixed frame has exactly ONE parser-contested edge, so every admissible T
collapses to `s·M` (one signed scalar × one constant matrix) — v1's emit-bit in
a 5×5 costume. This is not fixable by redefining T (§6 kills each candidate
fix); the panel must be extended (§7 MULTI-BIND, arithmetic-checked to pass).

---

## 1. Tokenization and node classes

Nodes = eojeols of the frame, plus the answer marker. n = 5, 1-indexed:

| node | eojeol | class | example (SI_N1) |
|---|---|---|---|
| 1 | V-adn(±시) | ADN (adnominal verb) | 웃으시는 |
| 2 | N1의 | NGEN (genitive noun) | 어머님의 |
| 3 | N2도 | NDELIM (도-marked noun) | 조카도 |
| 4 | tail | VFIN (matrix verb) | 기다렸다 |
| 5 | `=>` | ANS (answer marker) | => |

Parsers see ONLY the class skeleton `[ADN, NGEN, NDELIM, VFIN, ANS]` — never a
character, never 시/님. Blindness is enforced by the type signature:
`parse(classes: list[Class]) -> heads`, no string argument.

## 2. The two proxy parsers (deterministic, honorific-blind)

License table (shared): ADN modifies a noun to its right · NGEN modifies a noun
to its right · NDELIM is an argument of a verb to its right · ANS attaches to
VFIN · VFIN is root.

```
P_A (L→R, greedy nearest-head):        P_G (R→L, greedy maximal-head):
  for i = 1..n:                          for i = n..1:
    head(i) = NEAREST j>i                  head(i) = head of the LARGEST
              licensed for class(i)                  already-built licensed
                                                     projection right of i
```

Assigned heads on the frame (measured identical on all 192+64 items):

| dependent | P_A | P_G | agree? |
|---|---|---|---|
| 1 V-adn | **2 (N1 — low)** | **3 (N2 — high: [N1의 N2] is an NP headed by N2)** | **NO — the contested edge** |
| 2 N1의 | 3 | 3 (only one noun to its right) | yes |
| 3 N2도 | 4 | 4 | yes |
| 4 tail | root | root | yes |
| 5 => | 4 | 4 | yes |

P_A is low/local attachment (nearest noun); P_G builds the NP from the right
first, so the RC modifies the phrase head N2. Exactly one disagreement, by
construction, on the attachment-ambiguous RC edge. ✓ requirement (1).

## 3. The tension field T — two layers, inputs made explicit

**Layer 1 — structural tension (honorific-BLIND, from parsers only):**

```
S_P[i][j] = 1 if parser P assigns head(i) = j          (n×n, row = dependent)
T_struct  = S_A − S_G          # +1 = A-only edge, −1 = G-only edge, 0 = agreed
```

On this frame: `T_struct[1][2] = +1, T_struct[1][3] = −1`, all else 0.
T_struct marks WHERE the ambiguity is; it cannot resolve it (blind).

**Layer 2 — per-token feature vector (the ONLY honorific-aware input):**

```
hon[k] = 1 if node k carries the subject-honorific exponent, else 0
         hon[1] = 1[‑시‑ in V-adn]   hon[2] = 1[N1 is 님-final]
         hon[3] = 1[N2 is 님-final]  hon[4] = hon[5] = 0
         (요/네요 on the tail is addressee-level, NOT subject-hon: excluded)
reg[·] = tail register one-hots (다/어요/네요)
Φ_tok  = [hon[1..5], reg]      # unary per-token features, shared by ALL probes
```

**The field handed to probes** = concord-valued tension: cross-edge feature
products evaluated ONLY at parser-contested cells:

```
χ[i][j] = +1 if hon[i] == hon[j] else −1        # concord across the edge
T[i][j] = T_struct[i][j] · χ[i][j]
```

Split of inputs: `T_struct` and hence the SUPPORT of T = parsers only (blind);
the VALUES on that support = concord layer; `Φ_tok` = unary features. A probe
sees {some view of T} ⊕ Φ_tok; the only difference between probes is the view.

**Worked matrices** (rows/cols 1..5; verified on every panel item):

```
SI_N1  웃으시는 어머님의 조카도 기다렸다     hon = (1,1,0,0,0), gold 앞 (flip 0)
       χ[1][2]=+1 (시~어머님 concord)  χ[1][3]=−1 (시~조카 discord)
T =  [ 0 +1 +1  0  0 ]        T[1][2] = (+1)(+1) = +1
     [ 0  0  0  0  0 ]        T[1][3] = (−1)(−1) = +1
     [ 0  0  0  0  0 ]
     [ 0  0  0  0  0 ]
     [ 0  0  0  0  0 ]

PL_N1  웃는 어머님의 조카도 기다렸다        hon = (0,1,0,0,0), gold 뒤 (flip 1)
       χ[1][2]=−1 (plain~어머님 discord)  χ[1][3]=+1 (plain~조카 concord)
T =  [ 0 −1 −1  0  0 ]        T[1][2] = (+1)(−1) = −1
     [ 0  0  0  0  0 ]        T[1][3] = (−1)(+1) = −1
     [ 0  0  0  0  0 ]
     [ 0  0  0  0  0 ]
     [ 0  0  0  0  0 ]
```

Read-out semantics: `sign(T[1][2]) = +` ⇔ the A-parser's (low, N1) attachment
is concord-licensed ⇔ 앞. Measured on all 256 items: `T ≡ s·M` with
`M = E12+E13` and `s = 1 − 2·gold_flip`, exactly.

**That identity is the design's death on this panel**: the field manifold is
`{+M, −M}` — one signed scalar. The 5×5 shape is costume; the content is an
emit-bit. Everything in §4–§5 is a corollary.

## 4. G-0 completion — rank-mass audit (F4 pre-check)

Method: per item, `σ = svdvals(T)`; off-top mass `= 1 − σ1²/Σσk²`; average over
the panel; threshold ≥ 0.20 to proceed (pre-registered).

**Measured: 0.000 on f2′ (192/192) and f1′ (64/64).** T = s·M is rank-1
exactly. **F4-DEAD at $0, as pre-registered.** No redefinition survives §6.

Reading discipline: the value is a CONSTANT of the frame (deterministic parsers
× fixed frame ⇒ zero variance across items), so on any single-frame panel
rank-mass is a design-verification of the frame, not an empirical audit of the
mechanism. It becomes empirical only at G-2 where T comes from learned soft
parsers. Consequence: the frame itself must carry >1 contested edge (§7).

## 5. G-1 — the three logistic probes (+ controls), measured

Probe contract: linear logistic, closed-form-ish (full-batch GD, ridge
λ=1e-3, init 0 — on a balanced panel this finds the concave-MLE optimum), fit
on the panel; reported as train-fit AND cell-stratified 8-fold CV (train=test
caveat void — CV shown). Ties (p = 0.5 exactly) scored 0.5. Every probe gets
`Φ_tok`; the ONLY difference is the T-view:

| probe | T-view features | f2′ train | f2′ cv8 | f1′ cv8 |
|---|---|---|---|---|
| (a) vec T | all 25 cells of T | **1.000** | **1.000** | 1.000 |
| (b) rank-1 T | 25 cells of σ1·u1v1ᵀ | **1.000** | **1.000** | 1.000 |
| (c) ‖T‖ | scalar Frobenius norm | 0.500 | 0.500 | 0.500 |
| control: Φ_tok only | none | 0.500 | 0.500 | 0.500 |
| control: Φ_tok + hp·hn1 | none (forbidden product) | 1.000 | 1.000 | 1.000 |
| control: all-pairs χ, no mask | 10 unmasked concord pairs | 1.000 | 1.000 | 1.000 |
| control: per-item-permuted vec T | Π T Πᵀ, Π random per item | **1.000** | **1.000** | 1.000 |

Pre-registered arithmetic: probe(vec) − probe(rank-1) = **0.000 ≤ 0.05 →
"premise unsupported at $0 → STOP or redesign" FIRES.** Why: rank-1 approx of
a rank-1 matrix is the identity map — (a) and (b) receive identical features on
every item. And the permutation control at 1.000 is the sharpest indictment:
sum(T) = 2s survives any Π, so even edge-DESTROYED T resolves the panel — the
information content of T here is one permutation-invariant scalar. On this
panel the "field" claim is untestable and, worse, G-2's F1 would be **DEAD by
construction** (A-rank1's per-sentence input ≈ A-duel's whenever the learned
disagreement concentrates on the one contested region — "both answers
reachable" fails; an inadmissible falsifier despite F7 PASS).

## 6. The honest trap — what stops Φ_tok from making T decorative?

gold_flip = hp ⊕ hn1 (verified: it is the panel's own F7 XOR construction).

**(i) The XOR shield (why the trap as stated does NOT fire).** A linear probe
on unary features {hp, hn1, hn2, reg} faces balanced XOR. Logistic
log-likelihood is concave and every coordinate of the gradient at w = 0 is
Σ(y−½)x = 0 by the panel's exact balance ⇒ w* = 0 is the global optimum ⇒
p ≡ 0.5 ⇒ accuracy exactly 0.500. Measured: 0.500, both panels, train AND CV.
So position+hp as independent features predict NOTHING through a linear probe;
probe(‖T‖) does not "already solve it" (0.500 measured — ‖T‖ is constant).
The panel design itself is the defense — F7's XOR is exactly what makes unary
features linearly useless while a single T cell (a cross-edge PRODUCT: matrix
coordinate (i,j) ≡ token pair) is exactly the quadratic term XOR needs. The
field's indexing IS the binding: linear readout of pair-indexed cells =
quadratic readout of tokens. That, precisely, is the sense in which "field ≠
scalar summary" — and it is why probe(vec)=1.000 vs Φ_tok=0.500 is meaningful.

**(ii) The shield holds only under a FEATURE CONTRACT (pre-register it):**
Φ_tok may contain ONLY unary per-token features (hon bit, register one-hots);
NO cross-token products, no relational aggregates ("hon of the noun next to
the verb" is a disguised edge feature), no nonlinear probe. Violation demo,
measured: adding the single forbidden product hp·hn1 → 1.000. The contract is
~20 lines of feature-builder code; review it, don't trust it.

**(iii) Residual trap A — the concord layer is hand-coded.** χ literally
computes the binding predicate the duel is supposed to make learnable. So G-1
PASS certifies the representation FORMAT (edge-localized cross-token products
are linearly readable where unary features are not), NOT that a trained duel
will produce χ. That scope limit is acceptable — G-1 is pre-registered as a
spend-justification gate — but it must be stated in the freeze: G-1 green ⇒
"format necessary for linear readout"; parser competence is what G-2 trains
and F1/F5/F6 test.

**(iv) Residual trap B — the duel itself could be decorative.** The unmasked
all-pairs-concord probe also scores 1.000 (10 pairs at n=5; 190 at n=20). At
G-1 accuracy cannot separate "duel-localized products" from "all products";
the duel's contribution (edge alignment, O(#ambiguities) live cells vs O(n²))
is certified only by the G-2 placebo arm C-plc / F6. Pre-register the $0 tell
we now have: per-item-permuted-T probe on MULTI-BIND measures 0.711 — the
computable floor that permutation-invariant aggregates give C-plc — so F6's
required gap (A-duel − C-plc ≥ 0.05) has headroom 1.000 − 0.711 = 0.289 ✓,
whereas on single-bind the same control is 1.000 and F6 is void. 

**(v) Rejected fixes for §4/§5 (each is a manufactured pass):**

| candidate fix | why rejected |
|---|---|
| symmetrize T (add Tᵀ) | off-top jumps to exactly 50% for EVERY item — σ1=σ2 degenerate, scaffolding-determined constant; certifies the symmetrization, not the field (admissibility-gate) |
| pad T with agreed edges (S_A+S_G skeleton) | rank inflates via a CONSTANT skeleton; rank-1 approx then drops the one live bit → gate "passes" while per-item information is still 1 bit — v1's emit-bit in a high-rank costume |
| syllable-level nodes | support of T then shifts with ±시/님 lengths (elegant, fully blind XOR readout) but per-item T still has ONE contested region ⇒ rank-1 ≡ T ⇒ separation still 0 |
| soft parser scores | blind soft variation is gold-orthogonal by F7 balance — adds rank as noise, no binding content |

## 7. The redesign — MULTI-BIND (K=6): give the field ≥2 live dimensions

One ambiguity per sentence ⇒ field ≡ scalar. So put K independent HON-BIND
cells IN ONE SENTENCE (stacked 도-objects; grammatical, drill-register):

```
frame f2″:  [V₁-adn(±시₁) N₁₁의 N₁₂도] … [V₆-adn(±시₆) N₆₁의 N₆₂도] 기다렸다 =>
answer:     6 position tokens, one per conjunct (앞/뒤 each), e.g. => 앞뒤앞앞뒤앞
scoring:    d_acc = mean over the 6 forced choices — chance stays 0.5 per slot
nodes:      n = 3K+2 = 20 (V_k, N_k1의, N_k2도 ×6, tail, =>)
parsers:    unchanged rules; RC candidates bounded by its own conjunct (an ADN
            cannot attach past a 도-closed NP — both parsers share this)
            ⇒ contested edges: head(V_k) ∈ {N_k1 (P_A), N_k2 (P_G)}, k = 1..6
field:      T = Σ_k c_k·M_k,  M_k = E(r_k,r_k+1)+E(r_k,r_k+2),  r_k = 3(k−1)+1
            c_k = 1−2·gold_k — SIX independent signed dims; per-item rank 6
gold_k:     hp_k ⊕ 1[honored noun of conjunct k at N_k1]  (per-conjunct XOR,
            cells sampled independent & balanced per slot)
rank-1 ctl: σ-ties broken by pre-registered rule "retain the component with the
            smallest leading row index" (learned T at G-2 has no exact ties;
            mean is tie-break-robust anyway: retain-one-fixed and retain-any
            both give (1+0.5(K−1))/K)
```

Measured on the FULL 4^6 factorial (4096 items, `g1_core_check.py`):

| quantity | measured | pre-registered bar | verdict |
|---|---|---|---|
| G-0 off-top rank mass | **0.8333** (= 1 − 1/6, exact) | ≥ 0.20 | PASS |
| probe(vec T) | **1.000** (all 6 slots) | ≥ 0.75 | PASS |
| probe(rank-1 T) | **0.5833** (slots: 1.0, 0.5×5) | ≤ 0.60 | PASS |
| probe(‖T‖) | 0.500 | — (scalar floor) | ✓ |
| Φ_tok only | 0.500 (XOR shield, exact) | — | ✓ |
| perm-placebo vec | 0.711 | F6 floor, gap 0.289 | ✓ |
| separation vec − rank1 | **0.4167** | > 0.05 (STOP if ≤) | PASS |

Notes, honest: rank-1 at 0.5833 clears 0.60 by 0.017 — thin, but the number is
EXACT (deterministic construction; slots 2–6 are exact ties by the XOR shield,
slot 1 exactly separable), not a noisy estimate; K=6 is the smallest K with
(1+0.5(K−1))/K ≤ 0.60. Off-top 0.8333 is still frame-determined (constant) —
accepted with the §4 reading (design-verification; empirical rank lives at
G-2's F4 on learned T). E-value re-anchor for F1 on f2″: E[A-rank1] = 0.62
(structural ceiling 0.583 + leak ε), E[A-duel] = 0.90 ⇒ headroom 0.28 ≥ 0.15 ✓.
σ(f2″) ≈ √(0.25/1152) ≈ 0.015 under slot-independence (report per-item too).

Implementation deltas for `build_hon_bind.py` (f2″): lexeme pool must supply 6
disjoint (HON, PLAIN) pairs per sentence — expand the held-out pool 4→6 pairs
(+2 HON, +2 PLAIN; native-operator confirm item (c)) OR allow cross-conjunct
reuse with per-slot balance asserts (rejected default: repetition invites
coreference readings). F7″ additions: per-slot all-heuristics-0.5; per-slot
marginals 0.5; cross-slot independence (pairwise slot-gold correlation 0);
answer-pattern majority heuristic 0.5; 도-boundary constancy per conjunct.
Single-bind panels are RETAINED: f1′ stays the liveness panel (F2, threshold
0.85) and f2′ becomes a report-only diagnostic (F1 is NOT evaluated on it —
§5 shows it cannot separate the arms).

## 8. Verdict

**The mechanism as pre-registered does NOT survive its own $0 gates on the
built single-bind panel** — G-0 rank-mass = 0.000 (< 0.20, F4-DEAD) and G-1
separation = 0.000 (≤ 0.05, STOP), both corollaries of `T ≡ s·M` on a
one-contested-edge frame; additionally F1 and F6 are inadmissible there
(DEAD/void by construction). This is a frame property, not (yet) a mechanism
death: the concord field proves exactly the claimed format effect (vec 1.000
vs unary features 0.500 — binding is linearly readable ONLY as edge-indexed
cross-token products), and the MULTI-BIND K=6 extension passes every
pre-registered bar with measured margins (0.8333 / 1.000 / 0.5833 / 0.4167).

**Freeze remains blocked.** Updated checklist: (1) native-operator confirms
(a) PL normativity, (b) 2 flagged genitive orders, (c) +2/+2 lexeme-pool
expansion; (2) build f2″ MULTI-BIND (n=192, K=6) + F7″ audit; (3) re-run this
G-0/G-1 on the BUILT f2″ (predictions above are exact and falsifiable); (4)
re-anchor F1 E-values on f2″ and only then `pre_register_frozen: true`.
