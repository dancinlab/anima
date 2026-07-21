# H_004 G-2 — training driver design (`train_h004.py`): the parse-tension resolver + 5 arms

Fable-5 design, 2026-07-16. Implementable spec for the ~5h local-MPS falsification run.
**This is a design, not a run authorization**: the card is `pre_register_frozen: false` — the
native-operator G-1 items (surfaces · PL-cell normativity · genitive orders · the 4 `?`-flagged pool
lexemes) must clear and the freeze must be taken BEFORE any training step. Every number named here is
an E-value or a threshold, never a result.

## 0. Fixed inputs (already built + verified — consumed verbatim, never re-implemented)

| artifact | role | facts this design relies on |
|---|---|---|
| `panel_f2doubleprime.json` | verdict panel | n=192 · K=6 · 20 eojeols == 20 nodes · surface ends `"=> "` · `gold_pattern` = 6× 앞/뒤, no separators |
| `panel_f1prime.json` | liveness panel | n=64 · K=1 (single-bind, 5 nodes) · held-out tail 기다렸네요 |
| `drill_grid_multi.json` | drill | n=384 · ALL K=6 · tails {기다렸다,기다렸어요,기다렸음} · lexemes drill-only, F7-disjoint from f2″ |
| `g1_core_check.py` | tension pipeline | `t_struct` · `concord_field` · `rank1_tiebreak` (σ-tie: smallest leading row index) · `offtop` · `HEAD_A/HEAD_G` (single-bind) |
| `build_tension.py` | multi-bind heads + hon | `_heads()` (K=6) · hon-vector construction from `conjuncts[k]{hp, honored_position}` |
| `anima/core/model.py` | trunk | `CLMConvMoE` · `forward(tokens, targets)` → `{"logits"(B,V,T), "loss", "aux_loss"}` · slw/clms off |
| H_003 `train_h003.py` | envelope | d=384 L=4 E=3 (~3.7M) · CPT 8000 + drill 2500 steps · Adam 3e-4 · seq 512 · batch 16 · seeds {0,1} · `_stack_windows` CPT concat |

Byte facts (measured): `len('앞'.encode()) == len('뒤'.encode()) == 3`; first bytes differ (0xEC vs
0xEB), so forced choice diverges at candidate byte 0. Surfaces end with a trailing space after `=>`.

## 1. Model — trunk + resolver R

### 1a. Trunk (unchanged H_003 envelope)

`CLMConfig(vocab_size=256, d_model=384, n_trunk_layers=4, n_experts=3)`, slw=False, clms=False.

### 1b. Token embedding — raw UTF-8 bytes, V=256

**Deviation from H_003, deliberate**: no jamo-BPE codec, no `span_policy_encode`. H_003's lever WAS
the encoding; H_004's lever is post-parse, and the codec axis is closed (H_003 🔴). Every stream —
CPT (NSMC lines), drill, panels — is `str.encode("utf-8")`. This also removes L1's foothold
("codec in a trenchcoat"): there is no morpheme-segmentation stage for T to secretly re-do.

### 1c. Resolver R — size-invariant offset-bucket ingestion of the n×n field T

T is 20×20 on K=6 items and 5×5 on f1′ (K=1); R must serve both, so it ingests T by **relative
offset**, not absolute node index (also exactly the property C-plc's conjugate permutation destroys):

| module | shape | params |
|---|---|---|
| `r_out` | `Embedding(19, 32)` — bucket `b(δ) = clip(δ, -9, 9) + 9` | 608 |
| `r_in` | `Embedding(19, 32)` | 608 |
| `mlp` | `Linear(32→64) · GELU · Linear(64→64)` | 6,336 |
| `proj` | `Linear(64→384)` | 24,960 |
| **total R** | | **32,512 (< 1% of the 3.7M trunk)** |

Per-node structure embedding (pseudocode, exact):

```python
def node_embed(T):                       # T: (n, n) float32
    n = T.shape[0]
    delta = torch.arange(n)[None, :] - torch.arange(n)[:, None]   # (n,n) j - i
    b = (delta.clamp(-9, 9) + 9)                                  # (n,n) buckets 0..18
    h = (T.unsqueeze(-1) * r_out(b)).sum(1) \
      + (T.t().unsqueeze(-1) * r_in(b)).sum(1)                    # (n, 32)
    return mlp(h)                                                 # (n, 64)
```

(Equivalently, elementwise: `h_i = Σ_j T[i,j]·r_out[b(j−i)] + Σ_j T[j,i]·r_in[b(j−i)]`.)

Clip note: at n=20 true offsets reach ±19; |δ|>9 pools into the edge buckets. Every arm's live
cells sit at in-clip offsets δ∈{+1,+2} (A-duel, A-rank1 — see the measured tie-rule fact in §2 —
and the F5 union skeleton); only C-plc scatters mass to far offsets, and pooling scrambled cells
into edge buckets is part of the intended alignment destruction, not a confound. The ingestion is
BYTE-IDENTICAL across arms.

### 1d. Injection point + nc5 (resolver ships in the inference graph)

Subclass; the parent forward is copied once (slw/clms are None, ~15 lines) with ONE added term:

```python
class CLMConvMoEStruct(CLMConvMoE):
    def forward(self, tokens, targets=None, struct=None):   # struct: (B, T, 64) or None
        x = self.embed(tokens)                               # (B, T, 384)
        if struct is not None:
            x = x + self.proj(struct)                        # THE injection — pre-trunk
        x = x.transpose(1, 2); x = self.embed_conv(x)
        ...                                                  # verbatim parent: trunk → moe → norm → readout
```

`struct[b, t] = node_embed(T_item)[node_of_byte(t)]` (zeros on pad). CPT passes `struct=None`
(NSMC has no nodes) — identical for all arms. **nc5**: `struct` is an input of the SAME forward
used at eval; every d_acc/NLL call passes the item's arm-policy tensor through R. F5 manipulates
this live path at inference; v1's training-only binder is structurally impossible here.

### 1e. `node_of_byte` — the byte↔node alignment (measured to hold on all three files)

`surface.split(' ')` → eojeols; `assert len(eojeols) == 3*K + 2` (20 multi / 5 single-bind).
Node map: conjunct k → nodes 3k (V_k), 3k+1 (N_k1의), 3k+2 (N_k2도); tail → node 3K; `=>` → node
3K+1 (ANS). Byte span of eojeol i = `[start_i, start_{i+1})` in the UTF-8 stream (each eojeol owns
its trailing space). Every byte at offset ≥ `len(surface_utf8)` (the answer region) → node 3K+1.

### 1f. Target-slot indexing (d_acc per slot, well-defined)

The panel uses ONE trailing answer block: sequence = `surface_utf8` (ends `"=> "`) +
`gold_pattern.encode()` (K tokens × 3 bytes, **no separators**). With `base = len(surface_utf8)`:

```
slot k (0-indexed, k = conjunct index) ↔ bytes [base + 3k, base + 3k + 3)
```

Forced choice, gold-teacher-forced prefix: for slot k, context = `surface + gold[0:k]`; score
`NLL(앞 | ctx)` vs `NLL(뒤 | ctx)` over the candidate's own 3 bytes (candidate bytes are in the
input for its bytes 1–2); slot correct iff argmin == `gold_pattern[k]`.
`d_acc(item) = mean over K slots`; `d_acc(panel) = mean over items`. Chance 0.5/slot exactly.

Implementation = **K+1 forwards per item**: 1 forward on the full gold sequence yields the
gold-candidate NLL at every slot simultaneously; plus K forwards each with slot k's 3 bytes
replaced by the flipped token (bytes after slot k are irrelevant — only slot k is scored).
f1′ is the K=1 case (2 forwards). **No context-line prefix** (deviation from H_003's `_dacc`,
which prepended 160 NSMC bytes): eval sequences match the drill format byte-for-byte.

## 2. The five arms — ONE variable = the map `T_item → tensor handed to R`

Per item, the pipeline tensor is computed verbatim:
`T_item = concord_field(t_struct(n, heads), hon)` — `_heads()` from `build_tension.py` for K=6,
`HEAD_A/HEAD_G` from `g1_core_check.py` for f1′; hon built exactly as `build_tension.main` (multi:
`hon[3k]=hp, hon[3k+1]=pos1, hon[3k+2]=1−pos1`) / `g1_core_check.single_bind` (f1′).

| arm | tensor handed to R (drill AND eval, same function) | drill gold |
|---|---|---|
| **A-duel** | `T_item` untouched | true |
| **A-rank1** | `rank1_tiebreak(T_item)` — best Frobenius rank-1; σ-tie broken by retaining the component with the smallest leading row index (the pre-registered rule, verbatim `gc.rank1_tiebreak`). **Measured on all 192 built items**: the six conjunct blocks tie at σ=√2 ×6, so the tie rule fires on EVERY item and returns the row-0 truncation — exactly conjunct 0's two signed cells (nnz=2, ‖·‖=√2 vs ‖T‖=2√3). A-rank1 therefore receives slot 0's resolution and nothing else; arithmetic floor (1+5·0.5)/6 ≈ 0.583, consistent with E=0.62 | true |
| **C-plc** | `Π T_item Πᵀ` — `Π = default_rng(9000 + 1000·set_id + idx).permutation(n)`, **fixed per item** (identical Π at every drill epoch and at eval; set_id drill=0 / f2″=1 / f1′=2 → seed ranges 9000–9383 / 10000–10191 / 11000–11063, disjoint). Conjugate ⇒ spectrum preserved; edge alignment destroyed | true |
| **C-scaf** | `zeros(n, n)` — resolver still in the graph; `h_i = 0` ⇒ `e = mlp(0)`, a learned constant | true |
| **C-perm** | `T_item` (≡ A-duel) | `gold_pattern` shuffled ACROSS the 384 drill items as whole 6-token units, `random.Random(seed).shuffle`; f2″ scored against TRUE gold |

Byte-identity audit — everything below is shared and must be bit-identical across arms:

1. **CPT**: ONE window cache for all 5 arms (raw UTF-8 has no arm dependence — H_003 needed 3
   encodings, H_004 needs exactly 1). `struct=None` for every arm.
2. **Init**: `torch.manual_seed(seed)` immediately before model construction; same
   `CLMConvMoEStruct` class (R params allocated in ALL arms, C-scaf included).
3. **Batch order**: same `torch.randint` draw sequence (identical call pattern per stage;
   C-perm's shuffle uses `random.Random`, which does not touch torch RNG).
4. **Schedule**: steps · lr · batch · seq · pad length identical.
5. **Eval**: one scorer; the arm's tensor map is the same function object at drill and eval.

The arms differ in NOTHING except the table's tensor column (+ C-perm's gold permutation).
Any additional per-arm branch discovered while implementing is a one-variable violation — stop.

Two flagged deltas vs H_003 (shared by all arms, so one-variable holds, but they are envelope
changes): (a) **C-scaf here DOES drill** (H_003's skipped it) — the correct floor, because the
surface alone carries hp and position and a conv net could in principle learn the XOR without R;
that is precisely F3's job to bound. (b) The conditional 6th arm A-self (same-direction seeds)
remains out of G-2 scope — it triggers only on an F1 pass.

## 3. Schedule

| stage | data | steps | loss | struct |
|---|---|---|---|---|
| CPT | NSMC 120k lines · raw UTF-8 · `_stack_windows` concat (`\n`-joined) · seq 512 | 8000 | model-internal `ce + aux_loss` | None |
| drill | 384 items · per-item `surface+gold` sequences · **padded to 320** · batch 16 | 2500 | **external** masked CE (pad excluded) + `out["aux_loss"]` | per-arm tensor |

Adam lr 3e-4 · 2 seeds {0,1} × 5 arms, each from scratch (C2 licenses it). Wall clock: 10 runs;
drill at len 320 < H_003's 512, CPT identical ⇒ ~5–6h MPS (H_003 measured 6–8h).

**The drill windowing delta is the #1 wiring risk**: `_stack_windows` concatenation CANNOT be used
for the drill — `struct` is position-aligned per item and concatenation destroys the alignment.
Drill must be per-item padded batches with a loss mask (the model's internal CE has no
ignore_index, so the drill loss is computed outside the forward). Smoke WIRING-3/4 target this.

## 4. Falsifiers on the trained arms

Re-anchored E-values (G-1-measured arithmetic, anchors once frozen): **E[A-duel f2″]=0.90 ·
E[A-rank1 f2″]=0.62** (headroom 0.28 ≈ 1.9× the 0.15 bar). σ(n=192) ≈ 0.036.

| id | exact procedure | trigger |
|---|---|---|
| **F1** (primary) | Δ = d_acc(A-duel, f2″) − d_acc(A-rank1, f2″), per seed | SUPPORTED iff Δ ≥ 0.15 both seeds · DEAD iff Δ < 0.05 both · else PARTIAL |
| **F2** (liveness) | f1′(A-duel) | < 0.85 ⇒ measurement DEAD, no F1 verdict (frame-transfer caveat: FM-3b) |
| **F3** (not-free) | f2″(C-scaf) | > 0.60 (chance + 2.8σ) ⇒ grid leaks ⇒ no verdict |
| **F4** (= standing L1) | learned T-usage rank on trained A-duel: per f2″ item, `T_leaf = T.clone().requires_grad_()`; ONE gold forward; `L = Σ_k logp(gold slot-k bytes)`; `G_item = ∂L/∂T_leaf` (20×20); usage off-top = `gc.offtop(G_item)` | mean_item offtop(G) < 0.20 ⇒ the trained R reads ≤ a rank-1 shadow of T ⇒ DEAD (mirror of G-0's threshold; 192 backwards, minutes) |
| **F5** (= standing L2) | resolver→union substitution, inference-only, trained A-duel: replace the item tensor with `T_union = abs(t_struct(n, heads))` — the unsigned skeleton, +1 at (3k, 3k+1) AND (3k, 3k+2) ∀k: both candidate edges present, χ/resolution removed; item-independent by construction. ΔCE = CE_union − CE_T over the 18 gold answer bytes (per-byte mean, mean over f2″); Δd_acc = d_acc_T − d_acc_union | ΔCE < 0.01 AND Δd_acc < 0.05 ⇒ the decoder never needed the resolution ⇒ DEAD |
| **F6** (placebo) | d_acc(A-duel, f2″) − d_acc(C-plc, f2″) | ≤ 0.05 ⇒ void, no SUPPORTED ($0 tell already measured: permutation-invariant floor 0.711 ⇒ expected headroom ≈ 0.29) |
| harness | d_acc(C-perm, f2″) against TRUE gold | outside [0.45, 0.55] ⇒ harness broken, stop |

Diagnostics reported next to the gates (not gates themselves): per-arm drill-set d_acc and final
drill CE — required by FM-1/FM-2/FM-3 below; d_acc(A-duel, drill) ≥ 0.95 is a PRECONDITION for
reading any F1 verdict (it was trained on those items; below that the run is a wiring failure).

## 5. Honest failure modes — and the scope this run does and does not certify

**Scope (carried verbatim from DESIGN_g1_core §residual-trap-(iii), to be restated in the card):**
the concord layer χ is hand-computed — the SIGNS of T's contested cells literally encode the six
answer bits. G-2 therefore does **not** test parser competence (whether a learned duel produces χ);
it tests the **resolver FORMAT claim**: the decoder can exploit those bits iff they arrive as an
edge-aligned field (A-duel), and not as its rank-1 Frobenius summary (A-rank1), a
spectrum-preserving scramble (C-plc), or nothing (C-scaf). SUPPORTED licenses building the
learned-duel stage next; it does NOT claim a trained parser pair will produce this field.

| # | failure | mechanism | caught by |
|---|---|---|---|
| FM-1 | **false SUPPORTED — capacity, not content (L3)** | any nonzero per-item tensor regularizes/watermarks the decoder into the answer; F1's gap measures R's capacity, not edge-aligned content | C-plc via F6 (same spectrum AND same Frobenius norm, alignment destroyed) + C-scaf floor via F3. Residual: if C-plc's final drill CE ≫ A-duel's, its low f2″ is an optimization pathology, not an information verdict — the drill-CE diagnostic column must be read WITH F6 |
| FM-2 | **false SUPPORTED — A-rank1 dies of input statistics, not information loss** | A-rank1's tensor differs from A-duel's in support and norm (2 live cells vs 12, ‖·‖=√2 vs 2√3 — the measured tie-rule row-0 truncation), so R sees a weaker input signal; a Δ could partly reflect that scale gap rather than the missing 5 slots' bits | by construction the scale gap IS part of "rank-1 loses the field" (pre-registered rule), and the information claim is anchored by the G-1 probe ceiling (rank-1 cv8 = 0.4167, measured before any optimizer). Diagnostics: A-rank1 slot-0 d_acc should be HIGH (its one retained bit) while slots 1–5 sit ≈0.5 — that per-slot signature separates "read what it was given" from "underfit everything"; if instead ALL its slots are ≈0.5 and its drill CE diverges from A-duel's, report PARTIAL-with-caveat, not SUPPORTED. Both seeds must agree |
| FM-3 | **false DEAD — wiring, not mechanism** | (a) `struct`/byte misalignment or slot mis-indexing ⇒ every arm ≈ 0.5 ⇒ Δ < 0.05 both seeds ⇒ reads DEAD. C-perm does NOT catch this (it is ≈0.5 either way) | smoke WIRING-3/4 BEFORE the run + the §4 precondition d_acc(A-duel, drill) ≥ 0.95 |
| | | (b) **frame transfer**: the drill is 100% K=6; f1′ is K=1 with a held-out tail — F2 can fire from frame-length OOD while the mechanism is fine | pre-registered F2 stands (measurement DEAD is the honest read). Tell recorded in advance: F2 fires WHILE drill-eval ≥ 0.95 AND f2″(A-duel) ≥ 0.75 ⇒ the death is transfer, not liveness. The $0 fix — a K=1 drill block with its own F7 + disjointness audit — is admissible ONLY pre-freeze |

## 6. Cheapest smoke (BEFORE the d=384 run — H_003's windower bug analog lives here)

`--smoke`: d=64 · L=2 · E=2 · seq 128 · n_cpt 1500 · CPT 30 steps · drill 300 steps on a 32-item
subset · seed 0 · arms {A-duel, C-scaf}. Minutes on MPS. Asserts:

| check | assert |
|---|---|
| WIRING-1 alignment | for 3 items each of {f2″, f1′, drill}: `len(surface.split(' ')) == 3K+2`; eojeols [3k..3k+2] join to `conjuncts[k].surface`; print the node↔byte-span table for eyeball review |
| WIRING-2 slots | `len('앞'.encode()) == len('뒤'.encode()) == 3`; slot spans `[base+3k, base+3k+3)` tile `gold_pattern.encode()` exactly; the scorer on an UNTRAINED model returns K values/item with mean d_acc ∈ [0.3, 0.7] |
| WIRING-3 injection liveness | one item: flip the sign of `T[0,1]` ⇒ `max|Δlogits| > 0` on the A-duel path; the SAME flip on C-scaf (T≡0) changes NOTHING; a CPT batch (`struct=None`) is invariant to R entirely |
| WIRING-4 learnability | overfit A-duel on 16 drill items × 500 steps at d=64 ⇒ drill-subset d_acc ≥ 0.9 (T hands R the literal sign bits; if a d=64 net cannot read them through the injection, the injection or the slot indexing is broken — this is the H_003-windower-class catch) |
| WIRING-5 harness | C-perm's shuffle changes ≥ 90% of item golds; C-plc's Π is reproducible (same seed ⇒ same Π twice) and actually conjugate (spectrum of ΠTΠᵀ == spectrum of T to 1e-6); `rank1_tiebreak` on 3 K=6 panel items returns nnz==2 with support on row 0 (guards a numerics drift silently switching the σ-tie branch — that WOULD change the arm) |

Smoke numbers are wiring-only and are never quoted as results.

## 7. Outputs

`train_result_{smoke,full}.json`: per `arm.s{seed}`: `{f2doubleprime, f2doubleprime_per_slot,
f1prime, drill_dacc, drill_ce_final}` (per-slot needed by FM-2's signature); falsifier block per seed (F1–F3, F6, harness) + F4/F5 sub-blocks (A-duel only);
config echo (d, L, steps, pad, seeds, git SHA of the panel files). The verdict pasted into the card
is the verbatim stdout of `collect`-style readout (commons verify-done); SUPPORTED only if
F1 passes AND F2–F6 + harness are all clean, both seeds.
