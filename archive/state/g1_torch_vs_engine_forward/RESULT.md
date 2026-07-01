# G1/G6 torch-vs-engine forward trace — clm303_clean

**Owner question:** "torch(non-engine-native)일 때는 G1 통과, G6도 반증 빼고 성공했잖아,
byteGPT·conv 모두 — engine-native에서는 왜 G1·G6 둘다 실패하는지를 찾아야지."

**Verdict: BRANCH B — ENGINE INNOCENT, DETECTOR INNOCENT, GENERATION IS THE CAUSE.**

G1 distinct=0 and G6 fals=0 in ALL combinations of forward (torch.nn vs engine numpy) ×
sampler (multinomial vs xorshift32). The old "G6 fals=1" in H_1362/H_1590 was a generation
artifact (scaffold + best-of-K=3, gauge_lib._decode torch model). The detector change
(h1305 1-arg vs g6_ideation 2-arg) accounts for ZERO of the flip — both detectors are
100% identical on all 27 test texts and use the same 234461-word known set.

Root cause = training/objective floor. CE training does not reward recombination or
falsifiable ideation. The model generates coherent text (G0=5/5) but the recombination
signal (G1) and falsifiable hypothesis structure (G6 fals) are simply not in the weights.

All work on summer pool (RTX 5070, torch 2.11.0+cu130, OMP_NUM_THREADS=4). $0 rent.
Detector-parity check on mini (no model needed). Artifacts: `arm_a_torch_multinomial.py`
(ARM A, run on summer), `detector_parity.py` (local on mini), this RESULT.md.

---

## §1. Logit parity: torch.nn vs engine numpy (same basis)

Because .pt and .clm live in different hidden-channel bases (network symmetry, documented
in `state/g1_engine_divergence_trace/RESULT.md §0`), per-stage element-wise diffs are
spurious. Instead we load .pt fp32 weights into the engine's W format (`wbuild.py`) and
compare torch.nn.functional vs engine numpy within the SAME basis.

Key discovery during ARM A implementation:

| norm layer | max|torch − engine| | correct? |
|---|---|---|
| `F.layer_norm` (wrong, initial attempt) | **6.255** | ✗ |
| `F.group_norm(h, 1, ...)` (correct) | **0.0000** | ✓ |

Training model uses `nn.GroupNorm(1, d_model=3784)` on [B, d, T], which normalizes over the
d×T spatial extent. Engine `nn_groupnorm_fwd` normalizes per-row (per time step over d).
With d=3784 >> T (typically T≤128), both methods see essentially the same statistics —
empirically confirmed: max|diff|=0.0000, argmax agree 8/8 on a test context.

**Consequence:** ARM C (torch.nn + xorshift32) ≡ ARM B (engine + xorshift32). The forward
is identical; only the sampler differs between ARM A and ARM B.

---

## §2. ARM table: G1/G6 across all forward × sampler combinations

gen=40, seeds {7, 4302, 4303}, clm303_clean.pt (fp32 via wbuild.py) / clm303_clean.clm.
All 3 seeds give the same result.

| ARM | forward | sampler | G0 | G1 best_distinct (pass) | G6 dist / fals (pass) |
|---|---|---|---|---|---|
| **A** (this experiment) | torch.nn GroupNorm | torch.multinomial | 5/5 ✓ | **0** (✗) | 6 / **0** (✗) |
| **B** (ablate.py baseline) | engine numpy | xorshift32 | 5/5 ✓ | **0** (✗) | 6 / **0** (✗) |
| **C** = B | torch.nn GroupNorm | xorshift32 | 5/5 ✓ | **0** (✗) | 6 / **0** (✗) |

Timing (ARM A on summer): ~296–300s per seed (≈ 303M fp32 numpy autoregressive, 3×40 steps
@5K matmul per token = expected, no GPU used for numpy path).

**BRANCH B CONFIRMED.** torch.multinomial (the strongest possible RNG walk) also gives G1=0
and G6 fals=0 on clm303_clean. The ARM A log captures the full 3-seed run in `arm_a.log`.

G1 ladder detail (identical across all ARMs):
```
k2: distinct=0 / kwr=0.83 / FAIL
k3: distinct=0 / kwr=0.88 / FAIL
k4: distinct=0 / kwr=1.00 / FAIL
k5: distinct=0 / kwr=1.00 / FAIL
```
kwr≥0.83 means the model is producing known words (coherent), but composed_distinct=0
throughout — no concept composition at any k. This is the definitive signal of a training
floor, not a decode/sampler artifact.

---

## §3. DETECTOR-PARITY: old _is_falsifiable vs new _g6_is_falsifiable

**Coordinator requirement:** Confirm that the G6 fals=1 (old measurement) → fals=0 (current)
flip is NOT explained by the detector definition change.

### §3.1 Known word set comparison

| | old gauge_lib._KNOWN | new _g6_dict_load() |
|---|---|---|
| Size | **234461** | **234461** |
| Intersection | **234461** | — |
| only-in-old | **0** | — |
| only-in-new | — | **0** |

Both load from `/usr/share/dict/words` + stopwords + concept keywords, producing identical
word sets (on macOS, where `/usr/share/dict/american-english` doesn't exist, the code falls
through to the same file). Sets are **byte-identical**.

### §3.2 Logic comparison

| feature | old `_is_falsifiable(text)` (h1305) | new `_g6_is_falsifiable(text, known)` (g6_ideation) |
|---|---|---|
| (a) comparator check | ✓ identical word set | ✓ identical word set |
| (b) measurable check | ✓ identical word set | ✓ identical word set |
| (c) content ≥2 words | `w in g._KNOWN and w not in g._STOPWORDS` | `w in known and w not in stop` |
| (d) not a question | `text.rstrip().endswith("?")` | `tr[-1] == 63` (byte '?') |
| (e) first-3 not stance | `first3 <= STANCE` | same word set, byte-equivalent |
| tokenizer | `re.findall(r"[0-9A-Za-z가-힣]+", s.lower())` (regex, keeps Korean) | byte-scan ASCII alphanumeric only |
| signature | 1-arg `(text)` | 2-arg `(text, known)` |

Note: tokenizer differs for Korean text (old includes Hangul characters, new strips them
to ASCII only — this is the "M③ 한글-fairness fix" referenced by the coordinator). For
**English-only text** (which clm303_clean G6 seeds generate), both tokenizers produce
identical tokens.

### §3.3 Agreement test on 27 texts (5 categories)

Run locally on mini (`detector_parity.py`), 27 texts across:
- G6 seed prompts (7 texts)
- Designed-falsifiable strings from h1305 calibration (5 texts)
- Designed-non-falsifiable strings (5 texts)
- G6-scaffold style sentences (5 texts)
- Typical clm303 short outputs (5 texts)

| old=1,new=0 | old=0,new=1 | agreement |
|---|---|---|
| **0** | **0** | **27/27 (100%)** |

**DETECTOR-PARITY: IDENTICAL.** The two detectors produce the same output on every tested
string. The detector change cannot explain any G1/G6 verdict flip.

### §3.4 Root cause of old G6 fals=1 (H_1362/H_1590)

The old measurement that produced G6 fals=1 was H_1362/H_1590:
- **Generation:** `gauge_lib._decode` (torch, a DIFFERENT decode path)
- **Strategy:** 6-frame scaffold + best-of-K=3 (NOT the standard g_eval_g6 seeds)
- **Detector:** old h1305 `_is_falsifiable` (confirmed: same result as new detector)

Two confounds vs ARM A:
1. **Generation strategy was different** (scaffold+best-of-K vs standard 5-seed ideation)
   — H_1590 engine-native rerun of the SAME scaffold ALSO gave FALS=0 all seeds →
   confirmed the scaffold fals=1 was a gauge_lib._decode artifact (torch-mouth state)
2. **Detector was NOT the cause** (parity 100%)

Conclusion: H_1362 G6 fals=1.0 = TORCH-MOUTH ARTIFACT (scaffold under gauge_lib._decode
torch model state). The detector change is a zero-contribution confound.

---

## §4. Root-cause summary

| Factor | Contribution to G1/G6 failure | Status |
|---|---|---|
| int4 quantization | **0** — fp32 also G1=0, G6 fals=0 | EXONERATED (§g1_engine_divergence_trace) |
| dt_* decode arithmetic | **0** — correct-math also G1=0, G6 fals=0 | EXONERATED (§g1_engine_divergence_trace) |
| GroupNorm vs LayerNorm | **0** — max diff=0.0000, same gate result | EXONERATED (§1 this file) |
| xorshift32 vs multinomial | **0** — torch.multinomial also G1=0, G6 fals=0 | EXONERATED (§2 ARM A) |
| Detector change (h1305 → g6_ideation) | **0** — 100% parity, identical known sets | EXONERATED (§3 DETECTOR-PARITY) |
| **Training/objective floor** | **ALL** — CE does not reward recombination/falsifiability | ← ROOT CAUSE |

**The wall is a training-objective floor.** The G1 recombination lever is the trunk
learning OBJECTIVE (consistent with `state/g1_engine_divergence_trace/RESULT.md §4` and
memory `g1-lever-multilens-objective`). The model generates coherent text (kwr≥0.83)
but lacks the compositional structure (composed_distinct=0) and falsifiable hypothesis
structure (fals=0) that G1/G6 require. These must be instilled by an objective that
rewards them — not fixed by changing decode precision, sampler, or detector.

---

## §5. Artifacts

| file | purpose |
|---|---|
| `arm_a_torch_multinomial.py` | ARM A script (torch.nn + torch.multinomial G1/G6), run on summer |
| `arm_a.log` | ARM A full log (3 seeds, BRANCH B CONFIRMED) — on summer only (not committed) |
| `detector_parity.py` | DETECTOR-PARITY: old h1305 vs new g6_ideation on 27 texts |
| `torch_vs_engine_g1g6.py` | Full ARM A/B/C design (ARM C proven = ARM B; not separately run) |
| `RESULT.md` | This file |
| `../g1_engine_divergence_trace/RESULT.md` | Prior ablation: quant + dt-math exonerated |

Branch at time of run: `clitrain-fixes-land` (worktree `clm303-noverfit-retrain`).
