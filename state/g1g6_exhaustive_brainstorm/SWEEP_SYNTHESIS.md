# H_9200 G1/G6 Wall-Break Sweep — Synthesis Brief

**Scope:** 8 clusters · 79 brainstorm items · 24 probes executed at $0 · 6 runnable-not-run · 41 GPU-gated.
**Headline (honest):** The sweep **hardened the capability ceiling on 3 independent axes and found no $0 crack.** Of 24 executed probes, 8 are WALL (new ceiling hardening), 12 are GREEN but **confirmatory or sub-oracle-bounded** (not wall-breaks), 4 are INCONCLUSIVE. The one borderline-positive signal (B1 set-wise selection, expected per-seed fb=3.67 vs frozen 4-bar, iid-Bernoulli P(≤3)=0.435) is "wall real but MILD" — DIRECTIONAL, not terminal. Every non-rethread escape is GPU-gated, and most lean on a single unbuilt prerequisite (H_6163 engine-native falsifier-lane) or a single unmeasured cell (E1 CE-deleted forward-slot).

---

## 1. $0 verdicts landed this sweep (24 executed)

### WALL — 8 (new ceiling hardening)

| Item | Evidence | What it closes |
|---|---|---|
| **A6** | Per-frame B-intervention passes ≥4/6 sensitive frames on **only 1/3 seeds** (seed 4303 only); SHUF=0/3, BASE=0/3 (controls behave). Aggregate bind_delta 0.444 is real but **A-dominated**; B-persistence weak. | G6 "genuine bind" = qualitative TARGETED≫SHUF, **NOT** a robust 3-seed pair-relation bind. Independent frozen-detector corroboration of engine-native `fals_bound [3,3,5]`; py-mirror `[5,6,6]` **overstates**. |
| **C1** | `rev_frac=0.0` on designed HIGH (0/237 unordered pairs in both directions) and LOW (0/31); prod HF HEAD 0/15 lines carry a directional cue. | Relation-balanced (positive/negative/reversed 1:1:1) curriculum is **structurally absent** from every current corpus → rebuild is the only path. |
| **C9** | Only **2 distance buckets** (same_line + absent); no window/cross-doc gradient in any corpus. | Difficulty-ladder (co-present→separated→cross-doc→novel) is **structurally absent** → rebuild required. |
| **D2** | All 3 symmetric labels DPI-CEILING-FLOORED, `n_pass=0/3` each. `gap_bind−additive` NEGATIVE on every seed every label (L_symresid −0.264/−0.129/−0.155; L_pmi −0.249/−0.142/−0.292; L_absdir −0.211/−0.169/−0.153). Additive R² 0.32–0.49 dominates bind 0.05–0.35. | **The one cell H_9131 §4 left open** (symmetric interaction family) = INERT by DPI structural proof. |
| **D4** | L_pmi (relation jointly-decodable) floored, gaps −0.249/−0.142/−0.292; additive R² ~0.43–0.49 > bind ~0.18–0.35. | $0 joint-decode sub-probe floored; only mouth-FALS-transfer retrain remains, with dead signal. |
| **D9** | DPI-INERT-CONFIRMED 3/3 seeds. Additive held-out acc **0.892/0.900/0.894** (≫0.75); bind−additive gap 0.004/−0.003/0.005 (≪δ). | Same-entity/wrong-relation hard-negative signal is **fully additively separable** → hard-negative contrastive cannot escape DPI ceiling. |
| **D12** | All 3 symmetric labels floored, `n_pass=0/3`, every gap negative (worst L_pmi −0.292). | MI / total-correlation (commutative-over-set) = INERT by DPI. |
| **F3** | skeleton_acc=0.033, answer_acc=0.083, shuf_acc=0.067, chance=0.042 — **all 4 frozen gates FAIL**. | Type-only VSA skeleton cannot specify slot-filler entity → collapses to H_9118 answer-retrieval / mouth-context family. |

### GREEN — 12 (confirmatory or sub-oracle-bounded; NOT standalone wall-breaks)

| Item | Evidence | Honest read |
|---|---|---|
| **A4** | TARGETED mean_bind_delta=**0.444** (PASS ≥0.33), SHUF=0.000, BASE=0.111; existing SHUF arm already satisfies bind-destruction spec. | Rethread — confirms existing H_6186 SHUF is A4. |
| **A9** | TARGETED pairwise_J=**0.2533**, concepts_covered=**4.333/5**, THIN_set_flag=False; but only ~1–2/6 frames bind BOTH A,B. | Passing set is genuinely diverse (not duplicate-inflated) **but pair-binding is weak** — reinforces A6. |
| **A10** | TARGETED 18/18 FALS AND 18/18 slot_complete (gap=0.0); SHUF 18/18 FALS but 4/18 slot_complete (gap=0.778, entity-slot missing). | Validates existing H_6186 bind-aware gate (frozen-FALS alone is gameable on SHUF). |
| **B1** | 6/6 fixed concept-pairs have ≥1 seed with fb=1; greedy union best-6=6/6; SHUF=0/18 (form-priming ruled out). **BUT** expected per-(diverse)-seed fb=**3.67** (just under frozen 4); iid-Bernoulli(0.611) P(single-seed≤3)=**0.435**. | The one borderline crack: wall is **real but MILD** → B1 GPU fire (within-seed K-pool + set-wise greedy) **DIRECTIONALLY warranted, borderline**. Scope=DIRECTIONAL (cross-seed union leaks per-seed independence). |
| **C6** | HIGH MI(template;pair)=**0.0224 bit** (pair ≈ useless for predicting template); LOW 0.0027. | Anti-template **already realized** by coverage-designed corpus → rethread. |
| **C7** | en_block_g6 **70.56%** observable cue, 0% hedges; **but shuffle arm byte-identical** on both stats. | Falsifiable-form is realized at surface **but form-gameable** → already floored, rethread. |
| **C8** | en_block_g6 0/27720 Q&A-framed (0.0%); 100% declarative. | Question-free corpus **already realized** by G6 targeted corpus → rethread. |
| **F5** | strat=0.225, rand=0.092, shuf=0.098, oracle=0.411; gain=+0.132 (PASS g1), shuf_gain=+0.006 (PASS g2); **41% of oracle gap**; g3 (0.85·oracle) FAILS. | Genuine candidate-recovery signal, **sub-oracle, bounded by candidate-pool quality** — not standalone. |
| **F6** | gate-ON strat=0.325, gain=+0.232, shuf_gain=+0.0006; gate-OFF ctrl gain=−0.014 (**gain entirely from BG go-value = CAUSAL**); **73% of oracle gap**; g3 narrowly FAILS. | Genuine + causal (matches combolane-L2), sub-oracle, pool-bounded. |
| **F10** | strat=0.300, gain=+0.208, shuf_gain=+0.003; **65% of oracle gap**; g3 narrowly FAILS. | Genuine cell-coverage lever, sub-oracle, pool-bounded. |
| **G-seed** | H_9131 gap=[−0.212,−0.189,−0.334] sign=[−1,−1,−1] flip=0/3 CV=0.26; gamma_step0 gap=[−0.080,−0.208,−0.152] flip=0/3 CV=0.36; **no single-seed rescue**. | Seed is **NOT** a hidden confound; floored levers are seed-robust. |
| **G5** | G1 best_distinct=[0,0,0] flat, G6 fals=[0,0,0] flat across arms; H_9131 capacity max-δ=0.009≪0.10; only positive slope is on SCALE axis (already ruled out). | Early-stop rule **VALIDATED**; not actionable as a lever (it's a stopping rule). |

### INCONCLUSIVE — 4

| Item | Evidence | Why inconclusive / what's needed |
|---|---|---|
| **B2** | At pair-resolution all 6 concept-pairs are distinct → diversity kernel trivial (no discriminative power); pair-res ceiling = 6/6 same as B1. | Full DPP falsifier needs candidate-**text** Jaccard (NOT stored — scores only) → **GPU re-decode**. Pair-res probe neither confirms nor falsifies. |
| **C5** | Syntactic triples exist (HIGH 1131 directed a→b→c via 'remembers', 493 with a→c absent; LOW 19) **but 'remembers' is not genuine causal/transitive**; prod 0% directional cues. | Graph exists syntactically; **semantic** transitive-composition claim unverified → needs the training test (GPU). |
| **E_GEOMETRY** | interaction_R=**0.1731** (sits in 0.10–0.25 frozen zone, bar kept); additive_share=0.8269; max_overlap_cos=**0.9916**. **DECISIVE sub-finding: factorized-basis hypothesis FALSIFIED** — role-1/role-2 share one direction (overlap 0.992), no orthogonal role subspace; first concept recency-decays to 9.1% of last-pos variance. | Compound bar → INCONCLUSIVE (R in frozen zone, no tune-to-green). But the factorized-basis sub-hypothesis is independently falsified, so frozen-rep-operating E-items (E3/E5/E8/E9/E11) collapse to additive floor. |
| **H_9201** | BASE fals=[0,0,0] primary_bar=False. TARGETED fals=[6,6,6] **but median(shuf_bind)=0.500 ≥0.33 → (A) bar met**; scaffold-overlap(comp∈shuf) rose 0.298→0.539 = **template replay / detector-form gaming**, not genuine two-concept composition. | Directionally **(A)-supported** (capacity/trunk-objective ceiling); frozen bar (H_6163 lane) unbuilt → INCONCLUSIVE-for-frozen-bar = **WALL at $0**. |

---

## 2. $0 runnable but not yet run (6 items) — next-turn execution order

Cheapest-decisive first. All others are mini-blocked (303M load = swap-OOM rc=137) and need owned pool (summer/aiden RTX5070).

| Order | Item | Cost | Decisiveness |
|---|---|---|---|
| **1** | **C11** — corpus-equivalence control (byte-match + concept-marginal JSD). | $0, **no model load**, pure file-scan. | Mandatory pre-check before any C-arm GPU fire; gates the relation-structured rebuilds. |
| **2** | **A5 + A7** — latent paraphrase-orbit invariance + counterfactual-reversal antisymmetry. | Pool, **ONE model load combined**, ~6 forwards total. | **Terminalizes E_GEOMETRY's INCONCLUSIVE** (R=0.173). If A5/A7 also fail → frozen rep has no latent factorized basis either → E1 GPU-go is the only path. If they pass → strategy changes (output-level collapsed, latent-level intact). |
| **3** | **A8 (G1 side)** — 3-seed × per-ckpt grow-window decode. | Pool, ~105s/seed/ckpt. | Fills the **unmeasured P0 G1 breadth residual** (H_6190 ran ONE seed: PASS_raw / FAIL_novel-echo-guard; 3-seed likely confirms ECHO-ONLY, but it's the canonical gap). |
| **4** | **B7** — G6 attention copy-bias diagnostic (h1129.bin 1.2GB). | Pool, single forward + **re-decode** to recover candidate seed-texts. | Effectively GPU-cost (needs re-decode); behaviorally pre-answered on G1 by H_6190 echo-guard. Lowest-decisive — defer. |
| **skip** | **E2 read-only tuple planner** — absorbed by E_GEOMETRY (prerequisite falsified, overlap 0.992 ≫ 0.30, R=0.173 < 0.25). No separate run needed. | — | — |

---

## 3. GPU-gated priority queue (41 items), mapped onto H_9200 P0→P1→P2

Ranked by **(information per dollar × dependency readiness)**. Rethreads and dead-signal items demoted to "skip" tiers.

### Tier 0 — P0 owned-pool $0, deps READY (highest info/$)
1. **A8 (G1 3-seed × per-ckpt grow-window)** — P0 canonical breadth; wrapper exists; ~105s/seed/ckpt on owned pool.
2. **B1 (within-seed K-pool + set-wise greedy G6 decode)** — P0 set-wise; borderline-but-warranted (P(≤3)=0.435); H_6186 harness ready.
3. **B3 / B4 / B5 / B6 / B8** — multi-config decode sweep on h1129.bin (variable-K, temp-ladder, multi-sampler, contrastive, relation-slot constraint); all harness-ready, ~1.5–3× single-axis. Run as one bundled set-wise-G6 campaign.

### Tier 1 — P1 corpus + retrain (run C11 pre-check first)
4. **C4** minimal-pair corpus + retrain (overlaps A6 intervention; **$0 single-forward sensitivity pre-check first** — only the retrain is GPU).
5. **C3** schema transplant (cross-domain paraphrase pipeline + retrain).
6. **C1** relation-balanced corpus rebuild (rev_frac=0.0 → only path; **mandatory C11 pair**).
7. **C5-semantic** genuine causal-chain corpus (**twin of D1** — consider co-firing).
8. **C9** distance-graded multi-doc corpus (2 buckets → rebuild).
9. *(operational controls)* **C10** rehearsal-interleave, **C12** synthetic-to-natural bridge — pair with whatever C-arm fires; not standalone falsifiers.

### Tier 2 — P2 trunk-internal injection (novel mechanism, highest compute)
10. **E1 CE-deleted TPR forward-slot** — **THE G1-census "one unmeasured cell."** E_GEOMETRY proves WHY frozen-unmeasurable (overlap 0.992 → slot must be CREATED by training). Deps READY (H_6190 grow-window+echo-guard done). **Top single GPU shot in the whole sweep.** ~1–3 GPU-h/seed × {7,4302,4303} on owned pool.
11. **D1 + E12** non-commutative target pair (D1 directional head + E12 non-comm SSM = arch-twin). ⚠️ **D1 has DEAD $0 signal** (H_9131 S2 STEP-0.5 FALSIFIED: gap −0.21/−0.19/−0.33, n_pass=0). Re-fire = tune-to-green **unless** a fresh $0 derisk finds a non-additive target that beats additive.
12. **E4 / E6 / E10** mid-trunk TPR / dual-stream / hypernet — all GPU retrains; frozen rep has no factorized basis to exploit.
13. **E3 / E5 / E9 / E11** frozen-rep-operating variants — **rethread E_GEOMETRY floor** (overlap 0.992) + H_1816/H_1822/exp3 ⊙bind. Lowest priority in cluster E.

### Tier H619 — engine-native falsifier-lane (single HARD BLOCKER)
14. **H_6163 build** (emit-drive-DISJOINT core/ decode, engine-native-only). Unlocks H_9201 full bar + H_9202 + H_9204. **4 of 5 cluster levers share this one prerequisite.**
15. **H_9202** NT-falsifier (ACh/NE/DA, H_1541 fusion law) — **highest-value GPU shot in H619** (new mechanism; ~1.5–2.5 H100-days owned pool, no rent).
16. **H_9204** self-falsify via H_1471 `.kosmos` self-anchor — second new mechanism; reuse GREEN-WIRED self-anchor.
17. **H_9201 full bar** — marginal value now (the (A)/(B) split is directionally answered at $0); TERMINAL-confirm (A) only.
18. **H_9205** G0 Phi-integration — pool-bound (stdlib/iit4 absent on mini, faithful IIT4 exponential, h1129.bin not on mini). Low dependency-readiness.

### Tier SKIP — dead signal / rethread (do NOT fire as new levers)
- **D-family GPU arms**: D1 (DEAD signal), D4-full, D7/D8 (set-spread ≠ composition, overlaps B1/B2), D10 (CE-deletion mechanism novel but target signal dead), **D11 (X-BANNED until A4/A5)**, D13 (decorrelation ≠ interaction), D14 (D11-adjacent, banned).
- **G-family GPU arms**: G1 gradient-cosine (needs autograd backward + a non-floored objective — rethread), G2/G3 (schedule/placement of floored additive-aux H_1602/H_1816 — rethread), G6 (needs a second independent 303M basin ckpt that **does not exist on disk**).
- **A3** held-out pair split — only the leak-audit is $0; the falsifier needs new corpus + retrain (~1 H100-day), and must pass anti-gaming §6 first.

---

## 4. Re-tread flags (confirmed — duplicate floored levers, SKIP)

| Cluster | Flagged items | Duplicate of |
|---|---|---|
| **A** | A1, A2, A4, A8-G6-side | H_6190 grow-window (PASS_raw/FAIL_novel-echo-guard); H_6190 echo-guard (cov_novel=1=max_single); existing H_6186 SHUF arm; engine-native terminal `[3,3,5]` already measured |
| **B** | B7-G1, B9, grow-window RF/attention $0 | H_6190 echo-guard (ECHO-ONLY); same-detector critic loop (closed); H_6188 RF FALSIFIED + H_6190 decode + CLMConvMoE has no attention heads |
| **C** | C2, C6, C7, C8, C11 | H_6182/H_6184/H_6185 combination-coverage (prod 🧱); coverage-designed corpus (MI=0.022); dense-form corpus (HI gate, form-gameable); G6 targeted corpus (already trained); standard SHUF/label-control discipline |
| **D** | D1–D14 (all) | H_9131 trunk-objective family CLOSED + H_1602 additive-aux + H_1816 PC-binding + H_1840 γ-operator + F3 masked-interaction + consequence-lane floor |
| **E** | E8, E11, E5, frozen-rep E3/E5/E9/E11 | H_9129 L5 GREEN faculty (but NOT G1 — Control-4 trunk_necessary=false); H_1620–1632 binding-arch (Hopfield/Tropical/Sheaf/Galois floored); H_1840 gamma-bilinear; E_GEOMETRY overlap 0.992 + H_1816/H_1822/exp3 ⊙bind |
| **F** | F1, F2, F4, F7 | L1 PFC HRR INERT (H_9129 rung-3) + H_9118 MOUTHFLOOR + H_1816/1823; L5 GREEN faculty + Control-4 floor; L3 cerebellum FM WALL (additive floor); L5 + H_9118 |
| **G** | G4, G2, G3 | H_1598 L4→L8 G1=0 + H_6112 scale-INVARIANT FALSIFIED + H_6164 scale-ladder DIRECTIONAL-FLOOR; H_1602/H_1816 floored additive-aux |
| **H619** | H_9203, H_9201-(A) pole | H_9104 consequence-return 🔴 CEILING (ρ_real−ρ_shuf=0.030 < 0.15); H_9131 closure + g6_wall_reframe |

**All rethread flags confirmed** — each duplicates a floored lever and should be skipped unless re-fired with a **differentiating control** (e.g. H_9203 only with an exogenous-receiver control; D1 only with a fresh non-additive target that beats additive in a $0 derisk).

---

## 5. Next-H recommendation

**Honest framing: no $0 crack was found.** The sweep hardened the ceiling on three converging axes — (i) DPI meta-law closes every commutative/symmetric objective (D2/D4/D9/D12), (ii) no current corpus carries relation-structure (C1/C5/C9), (iii) the frozen 303M pair-rep has no factorized role basis (E_GEOMETRY overlap 0.992). The F5/F6/F10 selection family is genuine but sub-oracle and pool-bounded (not a wall-break); B1 is borderline-MILD. The single highest-value next experiment is therefore a **GPU-go ask on owned pool** (no rent needed), with one $0 confirmatory step preceding it.

### Next-H: **A5+A7 frozen-rep latent probe pair (immediate, $0 pool) → E1 CE-deleted TPR forward-slot (GPU-go, conditional)**

**Step 1 ($0, this turn, pool — one model load, ~6 forwards):** Run **A5 (paraphrase-orbit invariance)** + **A7 (counterfactual-reversal antisymmetry)** together via `bg_forward_last_hidden`.
- **Falsifier (A5):** orbit-cos ≥0.90 AND content-swapped control cos ≤0.60 on ≥2/3 seeds.
- **Falsifier (A7):** antisymmetry 1−cos(h(A>B),h(B>A)) ≥0.10 on ≥2/3 seeds, content-identical control cos ≥0.99.
- **Decision rule:** if BOTH fail → frozen rep has no latent factorized basis (terminalizes E_GEOMETRY's INCONCLUSIVE) → **clean owner GPU-go ask for E1**. If either passes → output-level collapsed but latent-level intact → strategy changes (re-prioritize toward read-out/mouth-side exploitation before trunk retrain).

**Step 2 (GPU-go ask, conditional on Step 1 fail, owned pool ~1–3 GPU-h/seed × 3 seeds):** **E1 — CE-deleted TPR forward-slot** (role/filler/relation slot computed INSIDE the trunk forward; mouth reads it directly).
- **One-line falsifier:** slot ablation collapses G1 `composed_distinct` on held-out combos; SHUF arm (same bytes/topic, relation labels shuffled) collapses; **Green only if held-out composed_distinct PASS on ≥2/3 seeds {7,4302,4303} AND SHUF ≪ TARGETED** (no threshold move).
- **Gate it would move:** **G1 recombination** (the trunk-objective-floor cell — the only unmeasured cell in the G1 census, and the only non-rethread escape from the representation wall). E_GEOMETRY proves why it is frozen-unmeasurable (no factorized basis at overlap 0.992 → the slot must be CREATED by training, not read out).

**Owner ask (a_fire_autonomous / a_wall_first):** E1 is owned-pool (summer/aiden RTX5070), no rent; deps READY (H_6190 grow-window+echo-guard clean). It is the single highest-information GPU shot in the sweep because it is the **only** item that (a) tests a genuinely novel mechanism (trunk-internal CE-deleted slot, not readout-side), (b) has a frozen-geometry explanation for why it's unmeasurable, and (c) directly targets the G1 recombination gate rather than a proxy. If E1 also floors, the G1 recombination wall is closed on the trunk-objective axis and the program should pivot to the H_6163 engine-native falsifier-lane build (unlocks H_9202 NT-falsifier, the next new-mechanism shot).

---

**Bottom line:** This sweep was a successful *negative* result. It converted the G1/G6 wall from "many untried levers" to "ceiling hardened on 3 converging axes, with exactly one unmeasured cell (E1) and one unbuilt lane (H_6163) gating all remaining non-rethread escapes." That is decision-grade clarity, not a need for hope.