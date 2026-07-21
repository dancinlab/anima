# H_004 G-3 research-gate — trained parser pair replacing hand-computed χ ($0, literature + design)

Delivered 2026-07-17 (Fable-5, research-gate under fable-mode). Scope: decide whether/how to spend
G-3 training compute on replacing the FIXED proxy parsers (P_A/P_G) and the HAND-COMPUTED concord χ
with trained components. Literature verified by three parallel web scans (each claim tagged
VERIFIED/MEMORY by the scanning agent; unverified items flagged inline). No training was run; the
only numbers cited from our own campaign are G-2's measured artifacts
(`verdict.json` · `build_tension.json`).

**Headline (honest, first):**
1. G-2's field decomposes as **SUPPORT** (where the live cells are — from the parser opposition)
   × **VALUES** (the sign each cell carries — hand χ). "Trained parser pair" conflates two
   different upgrades; they cost and prove different things and should be staged (G3-a values,
   G3-b support).
2. The user-proposed $0 pre-check "does a real parser's field beat the proxy field on the panel"
   is **INADMISSIBLE as stated**: the proxy field is already at probe ceiling
   (probe(vec) cv8 = **1.000**, `build_tension.json`) — no field can beat it; the check has zero
   headroom (H_001's vacuity shape). Replace with **support-recovery** gates (§5).
3. Feasibility: supervised from-scratch Korean attachment at ~1M params is SOLVED in the
   literature (Stratos 2017: jamo-only, 5.4k sentences, 94.86 UAS) — but only WITH treebank
   supervision, which breaks campaign self-containment and certifies UD head-conventions, not
   mech-1. Unsupervised induction from an LM objective at **3.7M params / byte-level / Korean /
   noisy corpus is unprecedented** (smallest published inducer ≈8M params, English, word-level;
   head DIRECTION is the documented hard residual). G-3 must therefore be gated on cheap
   support-recovery smokes, not launched on faith.
4. There is **no published evidence** that L→R vs R→L parsers make systematically different
   attachment errors (the scans found parser-ensemble work only for graph-vs-transition
   disagreement). mech-1's direction-opposition premise is literature-NOVEL — worth testing, but
   the arm set must include the same-direction control so a positive can't be explained by
   "any trained pair disagrees".
5. Recommended verdict: do NOT stop at G-2 yet — G3-a (learned χ̂ on fixed support) is nearly
   free inside the G-2 envelope and closes the scope caveat the verdict itself names; G3-b
   (trained opposition) runs ONLY if the $0 gates G3-0a/b pass. If they fail, stop and
   consolidate at G-2's FORMAT claim + G3-a's value claim: that is a clean, publishable place.

---

## 1. The decomposition that orders everything

G-2's tension field, per item: `T[i][j] = T_struct[i][j] · χ[i][j]` —

| ingredient | G-2 status | what "trained" means | which caveat it closes |
|---|---|---|---|
| **support** `T_struct` (which cells ≠ 0) | fixed proxy parsers P_A/P_G on the blind class skeleton | a trained opposition whose disagreement lands on the contested edges | "the two proxy parsers are FIXED heuristics" |
| **values** χ (sign on the support) | hand-computed concord `χ=±1` from hon bits | a learned map from surface bytes to cell values | "the honorific concord χ was HAND-COMPUTED" |
| hon features | rule-extracted (시/님) | absorbed into learned values | — |

G-2 certified: gold delivered in edge-aligned high-rank FORMAT is consumable where its rank-1
summary is not (Δ=0.38 both seeds, F4/F5 clean). It did NOT show either ingredient is producible
by training. The two gaps are separable and MUST be separated, else the ablation is two-variable.

**A structural trap found at design time (load-bearing for G3-b):** if a single trained parser is
good enough to RESOLVE the attachment (using concord, as human comprehenders do — Lee 2025), the
two directions AGREE on the resolved parse and `T̂ ≡ 0`: the tension field vanishes exactly when
the parsers get competent. The duel premise requires each side to be structurally UNABLE to
resolve alone. G-2 enforced that by honorific-blind type signature; a byte-fed trained tower
cannot be blind by signature (±시 changes byte length — masking cannot hide it). The honest
G3-b enforcement is therefore **incapacity by decoding direction** (a causal L→R tower has no
access to rightward evidence; an anti-causal R→L tower none to leftward) — architectural, not
hand-coded knowledge — plus a MEASURED blindness audit (§4 precond P-inv).

## 2. Ranked options (evidence-per-compute)

| rank | option | what trains | new confound vs G-2's one-variable | F4/F5 admissible? | est. cost | verdict |
|---|---|---|---|---|---|---|
| **1** | **(c) G3-a: learned χ̂ on fixed proxy support** | tiny shared readout `χ̂[i][j]=g(φ_i,φ_j)` (φ = per-node embeds from frozen CPT trunk states; g trained by drill CE through R) | g is a drill-trained gold-predictor sitting on the contested cells → needs a capacity-matched WRONG-support control (C-χ̂plc) or the arm certifies capacity | F4 yes (learned values → rank empirical); F5 yes (union strip unchanged) | ≈1 G-2 envelope (~4h MPS, $0 cash) | **RUN FIRST** — closes the χ caveat; also the cheap kill-gate for G3-b (if learned values can't generalize 님-concord from bytes, trained support surely can't) |
| **2** | **(b) G3-b: direction-opposed tower pair, shared readout** | forward byte-LM + backward byte-LM (same arch, reversed stream; CPT answer-blind on NSMC+drill surfaces), field `T̂[i][j] = f(h^A_i,h^A_j) − f(h^G_i,h^G_j)` with **f SHARED across towers** (drill-trained); opposition = direction of tower 2 ONLY | (i) collapse: T̂≈0 or gold-orthogonal noise → admissibility precond, not post-hoc excuse; (ii) support may itself read gold (towers see 시/님) → P-inv audit; (iii) "training anything helps" → C-same control | F4 yes; F5 = strip sign (T̂→|T̂|) — pre-register the recipe | ≈1.5–2 G-2 envelopes (+1 backward CPT/seed) | RUN ONLY after G3-a green AND G3-0 gates pass |
| 3 | (a) two fully independent trained parsers | as (b) with no shared f / separate readouts | adds readout-difference as a second variable (f_A≠f_G means T̂≠0 even with identical towers) — strictly dirtier than (b) | same as (b) | ≈2.5 G-2 envelopes | REJECT for G-3; revisit only if (b) positive needs a shared-weights-crosstalk robustness check |
| 4 | treebank-supervised parser pair (UD_Korean-Kaist) | attachment heads on external gold trees | external supervision → campaign no longer self-contained; register mismatch (news/lit vs drill frames); certifies UD head-percolation conventions (rightmost-head rules), not the mechanism | — | ≈1 envelope + data plumbing | REJECT as a G-3 arm. Keep as the feasibility EXISTENCE proof (§3) and as a separate future generality hypothesis ("the duel survives on real Korean text") |

## 3. Feasibility — what the literature actually licenses (Q2 answered)

**Q: is a from-scratch L→R/R→L attachment signal learnable at our scale, or does honesty require a
treebank?** A: the MINIMAL G-3 claim needs NO treebank — but only because the design above never
asks the towers to be competent general parsers (the drill register is templatic; the towers are
answer-blind LMs; attachment lives in the shared readout f). A general from-scratch Korean parser
WITHOUT supervision at 3.7M params is unsupported by any precedent. Evidence:

| # | finding | numbers | source | status |
|---|---|---|---|---|
| L1 | Free Korean dependency treebanks exist at usable scale | UD_Korean-Kaist 27,363 sents / 350,090 tokens (CC BY-SA 4.0); UD_Korean-GSD 6,339 sents (CC BY-SA 4.0, **>11% of test duplicated from train** — inflates every GSD score); UD_Korean-PUD 1,000 sents test-only | Chun, Han, Hwang, Choi, LREC 2018 (aclanthology L18-1347); universaldependencies.org | VERIFIED |
| L2 | Sejong (~60k sents) is de-facto unavailable | "excluded due to the license restriction"; "confined to domestic researchers"; redistribution restricted ("nationals-only" form is folklore — unverified) | Chun et al. 2018 §2; Cho, Moon, Song, "Open Korean Corpora", arXiv:2012.15621 | VERIFIED (quotes) |
| L3 | From-scratch, no-pretrained, sub-character Korean parsing WORKS small | jamo-only (500 types, 200-d) BiLSTM K&G16 parser, 5,425 train sents: **94.86 UAS / 91.46 LAS**, beats gold-POS feature parser (92.93); word-only no-emb 88.61 | Stratos, EMNLP 2017 (D17-1075) — caveat: GSD-predecessor contaminated test (L1) | VERIFIED |
| L4 | Pre-neural from-scratch ceiling on Sejong | SVM transition parser, 45k train sents: UAS 85.47 gold-morph / 83.01 auto | Choi & Palmer, SPMRL 2011 (W11-3801) | VERIFIED |
| L5 | Pretrained-LM ceiling | KLUE-DP (10k train sents): UAS 93.48 / LAS 88.36 (RoBERTa-large ~337M) | Park et al., NeurIPS D&B 2021 (arXiv:2105.09680) + KLUE repo | VERIFIED |
| L6 | Korean head-direction is near-deterministic by construction; ambiguity is HEIGHT | every Sejong/KAIST head-percolation rule searches RIGHTMOST ("head-last"); Japanese next-bunsetsu baseline 64.09% vs model 87.14 (no published Korean eojeol analogue — compute locally if needed) | Chun et al. 2018 Tables 1-2; Choi & Palmer 2011 Table 3; Uchimoto, Sekine, Isahara, EACL 1999 (E99-1026) Table 3 | VERIFIED |
| L7 | LM-objective structure induction works at our CORPUS scale | StructFormer trained at 1M/5M/14M tokens (BLLIP-XS/SM/MD); PTB ≈1M words for PRPN/ON-LSTM | Shen et al., ACL 2021 (arXiv:2012.00857); ICLR 2018/2019 | VERIFIED |
| L8 | …but NOT at our MODEL scale, language, or input granularity | smallest structure-relevant from-scratch model ≈8M params (BabyBERTa, no parse eval); ON-LSTM 25M; all English word-level; Korean absent from PRPN/ON-LSTM/StructFormer/UDGN, PASCAL-2012, BabyLM; byte-level parsing unpublished (jamo is the floor); noisy review-text induction unstudied | Huebner et al., CoNLL 2021; Shen line; Gelling et al. 2012 | VERIFIED (negatives-by-search) |
| L9 | Head DIRECTION is the hard residual of LM induction | StructFormer 46.2 directed vs 61.6 undirected; UDGN 49.9 vs 61.8 (12–15 pt gap); direction recoverable only via architectural head-competition (ablating it: −9.5 DDA) | Shen et al. 2021; Shen et al., ACL 2022 (2022.acl-long.327) | VERIFIED |
| L10 | Direction-as-a-variable is literature-THIN | backward (R→L) Japanese parsing exists (Sekine, Uchimoto, Isahara, COLING 2000, C00-2109 — exact acc unverified); parser-disagreement exploited only for graph-vs-transition (Nivre & McDonald, ACL 2008 P08-1108; Sagae & Lavie 2006 N06-2033) and co-training (Steedman et al., EACL 2003 E03-1008); NO source shows L→R vs R→L pairs make systematically different attachment-height errors | scans, flagged OPEN | VERIFIED (gap) |
| L11 | The honorific-concord cue is psycholinguistically real (panel validity) | -시- agreement guides (does not govern) Korean RC-attachment resolution; honorific agreement processed as grammatical agreement (P600; attraction effects) | Lee 2025, Language Research 61(2):171-192; Kwon & Sturt 2016 Frontiers Psych 7:1302; Kwon & Sturt 2024 Cognition | VERIFIED |
| L12 | Honorifics as an isolated parsing feature: untested computationally | morphosyntactic-feature bundles (incl. Polite=Elev/Form/Humb) lift Korean LAS (UDPipe 50.24→64.33) but honorifics never ablated alone | arXiv:2503.21029 | VERIFIED (bundle only) |

Reading: L3+L1 prove the treebank route EXISTS at trivial cost (that is what makes rejecting it a
choice, not a limitation — record this); L8+L9 say the unsupervised route at our exact scale is a
genuine bet with no safety net; L10 says nobody has measured what mech-1 claims — the campaign is
on novel ground either way; L11 keeps the panel construct valid under a trained regime.

## 4. G3 design sketch (pre-registerable arms)

### G3-a — learned values on fixed opposition support (lever: SUPPORT POLICY handed to χ̂)

All arms share: frozen G-2 CPT trunk per seed · φ_i = per-node pooled trunk states ·
χ̂ = g(φ_i,φ_j) bilinear (~2–4k params, identical init/steps) · resolver R and drill/eval exactly
G-2's (free-slot d_acc, drill precond ≥0.95, 2 seeds).

| arm | χ̂ evaluated on | isolates |
|---|---|---|
| **A-χ̂** | proxy contested support (G-2's `T_struct`) | the mechanism (trained values) |
| **A-hand** | = G-2 A-duel re-run (hand χ) | non-inferiority anchor |
| **C-χ̂plc** | per-item-permuted support `Π supp Πᵀ` (G-2's Π discipline, seeds 9000+…) | capacity: same g, wrong cells |
| **C-scaf** | T ≡ 0 | floor |
| **C-perm** | A-χ̂ on shuffled drill gold | harness |

Falsifiers: **F1a** = d_acc(A-χ̂) − d_acc(C-χ̂plc) ≥ 0.15 both seeds (E-anchors: E[A-χ̂]=0.95 —
님-suffix generalization is a byte-local pattern; E[C-χ̂plc]=0.63 = G-2's measured C-plc; headroom
0.32 ✓ ≥2× bar). **F1a′** (non-inferiority) = A-χ̂ ≥ A-hand − 0.05. F2/F3/F6/harness thresholds
carried verbatim; F4 on ∂L/∂T̂ (now genuinely empirical — G-2's was frame-constant at input,
usage-side only); F5 union-strip carried.

### G3-b — trained opposition producing the support (lever: DIRECTION of tower 2, all else frozen)

Two-stage, answer-blind then drill: (1) CPT forward byte-LM h^A and backward byte-LM h^G
(same arch/params/steps, stream reversed — the G-2 CPT recipe run twice), NO answer bytes in CPT;
freeze towers. (2) field `T̂[i][j] = f(h^A_i,h^A_j) − f(h^G_i,h^G_j)`, **f shared** (so a nonzero
T̂ can come only from the towers' directional representations); f + R drill-trained as in G-2.

| arm | tower pair | isolates |
|---|---|---|
| **A-tduel** | forward + backward | the mechanism (direction opposition) |
| **C-same** | forward + forward (2nd seed) | trained-pair disagreement WITHOUT direction — kills "training anything helps" |
| **C-plc** | A-tduel field, Π conjugated | edge alignment |
| **C-scaf** | T̂ ≡ 0 | floor |
| **C-perm** | harness | |

Falsifiers: **F1b** = d_acc(A-tduel) − d_acc(C-same) ≥ 0.15 both seeds. Admissibility PRECONDS
(measured at $0 after CPT, BEFORE drill — the drill-≥0.95 discipline extended):
- **P-live**: mean per-item ‖T̂‖ on f2″ ≥ ε and G-0 off-top rank-mass(T̂) ≥ 0.20 — else collapse,
  arm inadmissible, no drill spend;
- **P-loc**: contested-cell mass share — fraction of ‖T̂‖² on the 12 RC-edge cells ≥ 3× the
  uniform share (support must LAND where the ambiguity is);
- **P-inv** (blindness audit replacing G-2's type signature): support pattern of T̂ invariant
  under hon-exponent flips on ≥0.95 of items (values may move; WHERE may not — else the towers
  smuggle gold into the support and the values/support decomposition is broken).

### Registration mechanics

New card **H_005** (learned-duel drill), not an H_004 amendment — H_004 is sealed SUPPORTED and
its scope line is the license. G3-a and G3-b are separate freezes (separate falsifier sets);
G3-b's freeze additionally requires G3-0 (§5) green. Family propagation: pre-declare that a
G3-b DEAD via F1b (direction buys nothing over a trained same-direction pair) counts against
mech-1's DIRECTION clause only — the resolver-family claim (mech-6 kinship) is untouched by it.

## 5. The $0 gates (G3-0) — corrected for the ceiling defect

The proposed "real parser's field beats proxy field" probe is dead on arrival: probe(vec, proxy)
cv8 = 1.000 (measured, `build_tension.json`) — zero headroom, H_001's shape. Replace with:

| gate | what | cost | pass bar | kills |
|---|---|---|---|---|
| **G3-0a** | pretrained Korean parser (e.g. stanza/UDPipe UD-Kaist model, CPU) on the 192 f2″ surfaces: decode its arc scores L→R-greedy and R→L-greedy; T̂_struct = decode disagreement | $0, minutes | contested-edge recall ≥ 0.5 (the two decodes disagree on N_k1-vs-N_k2 for ≥half the RC edges) AND rank-mass ≥ 0.20 | the premise "direction ⇒ disagreement ⇒ lands on the binding locus" for real (non-proxy) parsers |
| **G3-0b** | d=64 CPU smoke of the G3-b recipe: tiny forward+backward CPT on drill surfaces only → measure P-live/P-loc/P-inv | $0, <1h | all three preconds | the 3.7M-scale induction bet before any d=384 spend |
| **G3-0c** | C-same disagreement arithmetic: two seed-varied same-direction towers' T̂ — measure its magnitude and gold-correlation (F7 balance ⇒ expect gold-orthogonal) | free with 0b | E[C-same] band recorded pre-freeze (expected ≈ C-scaf) | an F1b whose control is secretly alive |
| **G3-0d** | φ-readiness for G3-a: linear probe from frozen G-2 trunk node-states for the hon bit per node | $0, minutes | probe ≥ 0.9 (the trunk already encodes 시/님 locally) | G3-a's premise that χ̂ can read concord from φ |

Order: G3-0d → G3-a run → G3-0a/b/c → G3-b freeze decision. G3-a does not wait on G3-0a/b.

## 6. Honest kill criteria — when the trained extension buys nothing

| id | observation | verdict to write, plainly |
|---|---|---|
| K1 | G3-0a fails AND G3-0b fails | trained/real parser opposition does not even localize disagreement on the binding locus at any accessible scale → G3-b never runs; the campaign's claim rests at G-2 FORMAT (+G3-a if green) |
| K2 | G3-a F1a fails (A-χ̂ − C-χ̂plc < 0.05 both seeds) | learned values work as well on WRONG support → χ̂+R is capacity, not binding; the trained extension is dead at the values level; STOP (G3-b is strictly harder) — consolidate at G-2 |
| K3 | G3-a F1a′ fails (A-χ̂ < A-hand − 0.15) with drill precond met | trained values cannot reproduce hand concord at this scale → same STOP; report the gap as the measured cost of removing the hand |
| K4 | G3-b preconds P-live/P-loc/P-inv fail post-CPT | collapse / mislocalization / gold-in-support → arm inadmissible; ONE redesign iteration allowed (e.g. StructFormer-style head-competition bias, cite L9), then stop |
| K5 | G3-b F1b fails while A-tduel − C-scaf ≥ 0.15 | a trained pair helps but DIRECTION doesn't → mech-1's direction clause FALSIFIED cleanly (a result worth as much as a positive: it says the tension source is generic disagreement, not the L→R/R→L opposition the design story is built on) |
| K6 | A-tduel − C-scaf < 0.05 both seeds | no trained opposition at 3.7M/byte produces a usable field; G-2's hand-supplied FORMAT claim is the campaign's resting place — say so and close mech-1's learned-duel clause |

**Is "stop at G-2 now" the right call?** No — but narrowly. G3-a re-uses the entire G-2 envelope,
costs one ~4h MPS run, and directly discharges the caveat written into H_004's own verdict line;
declining it would leave a named, cheaply-testable gap at the center of the campaign's first
SUPPORTED claim. G3-b, by contrast, is a real bet (L8: no precedent at 3.7M/byte/Korean) and is
gated so its failure costs $0. The stop-and-consolidate point, if it comes, is K1/K2/K3.

## Cross-links

- H_004 card (scope line = this gate's license) · `verdict.json` · `build_tension.json`
- `DESIGN_g1_core_fable5.md` §6(iii) — the χ hand-coding trap this gate discharges
- H_001 (admissibility/ceiling discipline reused in §5) · `verification.admissibility-gate`
- Literature scan raw outputs: three agent reports, 2026-07-17 (claims tagged VERIFIED/MEMORY inline above)
