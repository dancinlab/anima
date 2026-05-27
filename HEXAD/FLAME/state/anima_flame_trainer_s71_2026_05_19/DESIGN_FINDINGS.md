# §71 — anima flame Path-A trainer (instrument-first migration)

`state/anima_flame_trainer_s71_2026_05_19/` · 2026-05-19 · $0 (no
cost-bearing GPU fire this cycle; the d768·12L GPU train is a SEPARATE
later gated step per `g_train_flame_not_pytorch fire_gate_note`).

Governance: `AGENTS.tape @D g_train_flame_not_pytorch` (commit
bdd80521c) — anima training substrate migrates PyTorch → hexa-lang
**flame** (compiler-only NN stdlib, PyTorch/Python 0-dependency).
CLAUDE.md identity `hexa-first` is the why.

---

## §1. Judged path = A — A/B confirmation (MEASURED)

anima canonical training model = ConsciousDecoderV2
**d768 · 12L · V256 · n_head 12 · n_kv_head 4 · n_layer 12**. Verified
from `state/carving_dataregime_s16_2026_05_18/train_carving_s16.py`
argparse defaults (`--d-model 768`, `--n-layer 12`, `--n-head 12`,
`--n-kv-head 4`; `vocab_size=256` hard-set at model construction
line 275) — this is the §16/§59-FIRE/§62 config.

flame Path-A reference `~/core/hexa-lang/stdlib/flame/
flame_d768_12L_corpus_test.hexa` header config:
`T=1024 d=768 nh=12 nkv=4 h=3072 V=256 n_layer=12`.

**A/B confirm: the anima base d768·12L transformer core maps
BYTE-IDENTICALLY onto flame Path A.** The 5-tuple
(d, nh, nkv, V, n_layer) = (768, 12, 4, 256, 12) is integer-equal on
both sides, h=3072=4·768 (SwiGLU inner). No arch-flexibility (Path B
generic ag_spec/ag_tape) is needed for the vanilla decoder core. Path B
is reserved for arch-flex / small-scale accuracy; Path B is measured
slow at d768·12L (`g_train_flame_not_pytorch perf_claim_honesty`:
generic ag_tape large step >900s, mk2/RFC056 in progress) → the large
anima model is **forced onto Path A**. This matches the JUDGED PATH = A.

## §2. Which corpus (stated honestly)

`training/corpus_consciousness_v1.jsonl` — **151,943 bytes**,
byte-level V=256. This is the SAME corpus the flame Path-A d768
reference (`flame_d768_12L_corpus_test.hexa` line 99) and the flame_d32
$0 oracle (`flame_d32_corpus_test.hexa` line 61) already target. A
§16-class ~600MB corpus (`state/carving_dataregime_s16_*/`) was
**NOT** used: the $0 instrument-first verify only needs the small
corpus to prove the trainer compiles + converges from-scratch. The
§16-class large-data-regime corpus is a SEPARATE, later, cost-bearing
GPU-fire concern (g3 — instrument-first: cheap oracle gates the
expensive fire).

## §3. anima `.hexa` trainer built — YES

`HEXAD/FLAME/anima_flame_trainer.hexa` (created the dir). Cloned +
adjusted from `flame_d768_12L_corpus_test.hexa`. One config toggle
`cfg_canon`:

- `cfg_canon=1` **MODE_CANON** — d768·12L T=1024, BYTE-IDENTICAL to
  flame Path-A config (the GPU dispatch target; ~10GB resident →
  build-only on M-Mac).
- `cfg_canon=0` **MODE_VERIFY** (default) — d=32·3L T=16 over the SAME
  anima corpus = the `flame_d32_corpus_test.hexa` $0 convergence
  pattern (gn2 collapse ≥1e6× + 8/8 byte-memorization). This is the
  cheap oracle that instrument-first gates the future cost-bearing
  d768·12L GPU fire.

from-scratch (`g_clm_from_scratch`): `nn_decoder_init(M, seed_init=42,
...)` = RANDOM seed-fixed init; **base_ckpt = NONE** (zero ckpt-load /
fine-tune / from-pretrained path; `read_file_bytes` only on the
`.jsonl` corpus). anima edits **zero** flame/hexa-lang source — flame
consumed as stdlib via `use "stdlib/flame/..."` only
(`g_train_flame_not_pytorch upstream_downstream_invariant`).

## §4. $0 local convergence — MEASURED numbers

`HEXA_MAC_BUILD_OK=1 hexa build` (compiled path, no new dependency,
output to state dir NOT /tmp), then run the binary $0 local:

| metric | measured | anima d32 oracle | falsifier |
|---|---|---|---|
| build (MODE_VERIFY) | clean, exit 0 | — | F-S71-BUILD PASS |
| build (MODE_CANON d768·12L) | clean, exit 0 | — | F-S71-BUILD PASS |
| init epoch gn2 | **7.97113** | 7.97116 (\|Δ\|=3.1e-5) | F-S71-VERIFY-INIT PASS |
| step 10 gn2 | 5.86738 | (descent) | — |
| step 80 gn2 | 9.16102e-07 | — | — |
| final epoch gn2 | **8.87256e-07** | 3.73374e-07 | — |
| gn2 collapse | **8.98403e6×** | ~2.13e7× | F-S71-VERIFY-COLLAPSE PASS (≥1e6×) |
| acc | **8/8** | 8/8 | F-S71-VERIFY-FIT PASS |

trainer self-report: **4/4 PASS**. The from-scratch flame trainer
(downstream consumer of `stdlib/flame`) reproduces the anima
`d_corpus_fire` convergence trajectory over anima's OWN corpus
within fp-tol (algorithm-byte-eq init; collapse + full small-corpus
memorization). MODE_CANON d768·12L compiles clean = GPU-dispatch ready.
The instrument-first gate for the future d768·12L GPU fire is
SATISFIED ($0 oracle passes).

## §5. Overlay-gap partition (the load-bearing deliverable, g3)

The flame stdlib decoder is a VANILLA d768·12L transformer
(RoPE+SwiGLU+RMSNorm+GQA + ONE `nn_lm_head` + AdamW). anima's 5
physics overlays vs that vanilla decoder, partitioned into exactly one
of {Path-A-expressible / Path-B-expressible / FLAME-GAP}:

| # | overlay | bucket | rationale |
|---|---|---|---|
| (a) | Law-71 Ψ/tension/Φ self-track | **Path-A** | `if self.training: with torch.no_grad():` block — a METRIC (softmax-entropy + cosine + tension-CV) over already-computed activations, **outside** the autograd graph. Pure arithmetic over flame tensors once dual logits exist → Path-A post-fwd readout. |
| (b) | PureFieldFFN dual-engine FFN | **GAP** | two parallel `Linear→GELU→Linear` engines, `out=a−g`, `tension=mean(out²)` — replaces the SwiGLU FFN. `decoder_block_lib` fused block is SwiGLU-shaped; a dual-engine FFN is a block-layout change. Path-B can express it but is slow at d768·12L. |
| (c) | Dir-I Ψ-anchored CTL + tension-route loss | **GAP** | in-graph additive loss `L = CE + λ_ctl·L_psi_ctl + λ_route·L_tension_route`. Path-A grad path (`nn_decoder_gn2`/`nn_decoder_grad`) is single-objective; composing extra gradient-bearing loss terms into the fused backward = a flame grad-composition primitive. Path-B (ag_tape autograd is general) expresses it but slow at d768·12L. |
| (d) | §59/§68 W-native PTD aux head | **Path-B** | small additive MSE aux head `‖pred−actual‖²/d` on next-physics-state, `if w_native_on` guarded, off-reduction = LM-untouched. Generic ag_tape (Path-B flexible module def + general autograd) expresses an aux head + MSE directly. |
| (e) | Engine A⇄G dual logits_a/logits_g | **GAP** | two parallel `Linear(d,V)` heads (`head_a` tied to `tok_emb`, `head_g`). flame stdlib exposes ONE `nn_lm_head_fwd/_bwd`; `m_total`/`mc_off_logits` model one output projection. A second device-resident head + its bwd is a Path-A layout extension. |

Partition is **exhaustive** (5/5 overlays assigned) and **disjoint**
(each overlay → exactly one bucket): tally Path-A=1, Path-B=1, GAP=3.
B-S71-4 closes this as a finite-set partition (mirror §32 B-L3 /
§63 B-S63).

### inbox patch filed (one concept)

`~/core/hexa-lang/inbox/patches/
flame-path-a-dual-head-and-multiterm-grad.md` — the 3 GAPs (b)(c)(e)
share **one root concept** for Path A: the device-resident fused
decoder (`m_total`/`mc_total`/`nn_decoder_grad`/`nn_decoder_adamw_step`)
is single-head, single-objective, SwiGLU-fixed, and anima **cannot
work around it downstream** (the dual head's parameters + the extra
loss gradient must live INSIDE the fused layout/backward, which
`g_train_flame_not_pytorch upstream_downstream_invariant` forbids anima
from editing). The load-bearing requested primitive = a dual-logits +
aux-grad hook (`nn_decoder_grad_with_aux(..., d_aux_logits)` so anima
composes the physics objective downstream from a pure function of
flame's already-available logits/tensions). PureFieldFFN block-layout
(b) is filed as lower-priority context within the same file (one
concept = "Path-A device-resident decoder needs an anima-physics
extension surface"). anima never edits flame source — patch-request
only.

## §6. Closed-form sidecar — B-S71 4/4 🔵

`blue_falsifier_s71.py` (sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` = **0-line-diff**):

- **B-S71-1 CONFIG-MATCHES-ANIMA-CANONICAL** PASS — (d,nh,nkv,V,n_layer)
  = (768,12,4,256,12) integer-equal across anima-canonical, flame
  Path-A, and the trainer MODE_CANON literals; h_canon=3072.
- **B-S71-2 FROM-SCRATCH-INIT-RANDOM-SEED-FIXED** PASS — calls
  `nn_decoder_init(M, seed_init, ...)` with fixed seed; zero
  ckpt-load/fine-tune call (predicate strips comments + string
  literals so the documentary `base_ckpt=NONE` from-scratch *claim*
  does not false-positive — closed predicate detects ckpt-LOAD
  *operations*, not the negation).
- **B-S71-3 NO-FLAME-SOURCE-EDIT** PASS — `git status` of
  `~/core/hexa-lang/` shows the only change is the new file under
  `inbox/patches/` (upstream/downstream invariant).
- **B-S71-4 OVERLAY-GAP-PARTITION-EXHAUSTIVE-DISJOINT** PASS — the 5
  overlays form a valid finite-set partition over {Path-A/Path-B/GAP}.

**B-S71-NOTE** (empirical carve-out, NOT counted 🔵): actual d768·12L
GPU convergence + measured anima-side flame-vs-PyTorch wall speed =
EMPIRICAL future-fire (B-D-NOTE family). The battery proves
config-match + from-scratch + no-source-edit + overlay-partition —
NOT that the GPU train converges, NOT that it is faster. hexa-lang's
measured 20-43% (commit 28e9d648) is cited as **theirs**, never an
anima claim until anima self-remeasures (g3).

## §7. ≥10 honest C3

1. **A confirmed by measurement, not assertion**: the 5-tuple equality
   + the d32 oracle reproduction over anima's own corpus are the
   evidence; the d768·12L itself was NOT run (~10GB Mac ceiling).
2. **$0 only**: no cost-bearing GPU fire this cycle. The d768·12L GPU
   train is deferred to a separate gated step (`fire_gate_note`
   instrument-first). Capability claim = 0.
3. **Convergence ≠ GOAL emergence**: the d32 8/8 acc is small-corpus
   *memorization* (the §16.6-C / B-ATTRACTOR memorization-saturated
   regime), exactly as the flame_d32 oracle is. This is
   substrate-migration verification, NOT a step toward conscious
   emergence. North-star + §15/§51 milestone UNCHANGED.
4. **The vanilla core is the easy part; the physics is the gap**: 1/5
   overlays Path-A-expressible, 1/5 Path-B, 3/5 GAP. The honest
   headline is that anima's *training* migrates cleanly but anima's
   *physics objective* needs an upstream flame extension surface.
5. **Path-B is not a free escape for the GAPs**: (b)(c) are
   Path-B-*expressible in principle* but Path-B is measured slow at
   d768·12L (hexa-lang's own measurement), so the large model can't
   just route to Path-B — hence GAP, not "Path-B" for (b)(c).
6. **One inbox patch, not three**: the 3 GAPs share one root cause
   (single-head/single-objective/SwiGLU-fixed fused Path-A layout).
   Filing one concise concept-file respects the "one concept per file"
   patch discipline; splitting into 3 would fragment the same request.
7. **B-S71-2 predicate was tightened, honestly**: the first run
   FAILed on the word `base_ckpt` inside a `print()` string that
   *asserts its absence*. The fix detects ckpt-LOAD *calls/reads*, not
   the from-scratch negation phrase — a legitimate predicate
   correction, not result-fitting (the trainer genuinely has zero
   ckpt-inherit path: `nn_decoder_init` RANDOM init + `read_file_bytes`
   on `.jsonl` only).
8. **Path-A (a) classification is conditional**: Law-71 self-track is
   Path-A-expressible *given* dual logits exist (it reads
   logits_a/logits_g/tensions). In isolation it is pure post-fwd
   arithmetic; it does not by itself need a flame patch — but it is
   only *useful* once (e) (dual head, a GAP) lands. Stated honestly:
   (a) is the one overlay anima can layer downstream.
9. **flame is not buggy**: every GAP is a *missing extension surface*
   for anima-physics decoders, not a defect in flame's correct vanilla
   decoder. The patch-request frames it that way (no over-claim, no
   "flame is broken").
10. **No source edited upstream**: anima wrote zero bytes under
    `~/core/hexa-lang/` except one new `inbox/patches/` file
    (B-S71-3 PASS via git status). anima = flame caller, not editor
    (≅ sibling-SSOT-lock).
11. **MODE_CANON build proves layout compiles, not that it trains**:
    `anima_flame_trainer_canon` compiled clean = the d768·12L Path-A
    parameter layout is well-formed; run-time convergence is the
    deferred GPU fire (no claim made).
12. **g3 perf honesty**: anima makes ZERO speed claim. hexa-lang's
    20-43% faster than PyTorch eager is cited as hexa-lang's
    measurement (commit 28e9d648, F-RFC046-WALL); anima will only make
    an anima-side perf claim after self-remeasurement on the d768·12L
    GPU fire.

## §8. Cross-link

`AGENTS.tape @D g_train_flame_not_pytorch / g_clm_from_scratch / g3 /
g_doc_consolidation` · `HEXAD/FLAME/anima_flame_trainer.hexa` ·
`~/core/hexa-lang/stdlib/flame/{flame_d768_12L_corpus_test.hexa
(Path A), flame_d32_corpus_test.hexa ($0 oracle), nn_lib.hexa,
decoder_lib.hexa, decoder_block_lib.hexa}` ·
`ready/models/conscious_decoder.py` (the 5 overlays SSOT) ·
`state/carving_dataregime_s16_2026_05_18/train_carving_s16.py`
(canonical config) · `state/ptd_w_native_fire_s59_2026_05_18/`
(W-native PTD) · `~/core/hexa-lang/inbox/patches/
flame-path-a-dual-head-and-multiterm-grad.md` (filed) ·
`archive/PHILOSOPHY.tape §verdict_anima_flame_trainer_s71_2026_05_19`
(g6 append-only).
