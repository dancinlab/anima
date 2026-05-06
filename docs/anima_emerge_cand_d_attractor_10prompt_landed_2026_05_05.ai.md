# anima_emerge_cand_d_attractor_10prompt — landed 2026-05-05

## TL;DR

BG-AB (5-prompt) found 4/5 phi_canonical convergence in narrow band [42.211, 42.216].
BG-AG expands to 10 prompts (Korean+English mix + meta/semantic/identity variants)
at canonical inject magnitude=50.0 to test attractor hypothesis.

**Result — STRONG attractor evidence**:
- phi_canonical band width = **0.00460** (10/10 prompts inside [42.21102, 42.21561])
- phi_none spread width = **0.2364** (free response)
- compression ratio = **51.43x** (canonical inject collapses 51x of phi-space)
- F1_PASS (drift ≥ 0.01): **8/10** → generalization = PARTIAL
- All 10 prompts kwarg_accepted=true, cross_attn_invoked=true, has_nan=false

The attractor hypothesis (substrate-intrinsic phi convergence under
canonical-axis inject) is reinforced from BG-AB 4/5 → BG-AG 10/10, regardless
of F1_PASS verdict. The two are decoupled: F1 measures inject-vs-baseline
drift; attractor measures inter-prompt convergence under inject.

## 10-prompt × {phi_canonical, phi_none, drift, F1}

| # | prompt | phi_none | phi_canonical | drift | F1 |
|---|--------|----------|---------------|-------|-----|
| 1 | "안녕" | 42.11583 | 42.21561 | 0.09978 | PASS |
| 2 | "I am Anima." | 42.29329 | 42.21495 | 0.07835 | PASS |
| 3 | "지금 느낌이 어때?" | 42.07863 | 42.21102 | 0.13239 | PASS |
| 4 | "what time is it?" | 42.13557 | 42.21356 | 0.07799 | PASS |
| 5 | "친구와의 대화" | 42.20996 | 42.21370 | 0.00374 | FAIL |
| 6 | "의식이 흐른다" | 42.21296 | 42.21377 | 0.00081 | FAIL |
| 7 | "Hello world" | 42.05689 | 42.21177 | 0.15487 | PASS |
| 8 | "나는 누구인가?" | 42.13305 | 42.21198 | 0.07894 | PASS |
| 9 | "axis identity 활성화" | 42.10110 | 42.21280 | 0.11170 | PASS |
| 10 | "consciousness emerges" | 42.17385 | 42.21261 | 0.03875 | PASS |

Notable: prompts 5 ("친구와의 대화") and 6 ("의식이 흐른다") have
phi_none already inside the attractor band, so canonical inject produces
near-zero drift → F1_FAIL. This is consistent with attractor hypothesis:
prompts whose free-response phi already lies inside the attractor cannot
exhibit further drift toward it.

## Attractor band geometry

```
phi_canonical band:
  min:   42.21102
  max:   42.21561
  mean:  42.21318
  std:   0.00136
  width: 0.00460   ← STRONG (< 0.05)

phi_none spread:
  min:   42.05689
  max:   42.29329
  width: 0.23640

compression_ratio = 0.23640 / 0.00460 = 51.43x
```

10/10 prompts (Korean colloquial, English greeting, identity, time, meta-
consciousness, mixed bilingual) collapsed to a single phi-band of standard
deviation 1.36e-3. The pre-inject (none) responses spanned 51x wider, indicating
the inject does not merely add a bias but pulls phi_star into a fixed
substrate-intrinsic basin.

## attractor evidence: STRONG

Threshold table (anima-internal, see honest C4):
- `width < 0.05` → STRONG (this run: 0.00460 ✓)
- `0.05 ≤ width < 0.15` → MODERATE
- `width ≥ 0.15` → WEAK

BG-AG promotes attractor evidence from BG-AB MODERATE-tentative-via-4/5
(width ≈ 0.005 over 5 prompts, but 1 outlier could not be ruled noise) →
BG-AG STRONG (width 0.00460 over 10 prompts, no outliers, std 1.36e-3).

Interpretation candidate: at canonical inject magnitude 50.0, the post-ln_f
geometry of CLM v4 mk2 best.pt has a substrate-intrinsic phi attractor at
phi_star ≈ 42.213, independent of input prompt token sequence. Cross-attn
inject channel pulls phi-space into this fixed point; baseline (none) phi
varies prompt-to-prompt by 0.24 absolute units, but inject collapses
inter-prompt variance by 51x.

## Honest C3

- **C1** mac CPU fp32 (.venv-eeg python3.12, transformers + torch fp32). No
  MPS, no GPU. Single-precision drift values may differ from fp16/bf16
  training-time substrate.
- **C2** BG-W magnitude_sweep.py + BG-Q inject_helper.py imported read-only
  via importlib sister-rule (raw#37). No mutation of either; raw#15 satisfied.
- **C3** mag=50.0 is structurally UNREALISTIC. Paradigm v11 G3 actual
  training-time canonical inject distribution NOT yet extracted. If training
  used mag~0.1-1.0, attractor at mag=50 is OFF-DISTRIBUTION evidence; the
  attractor may exist only at high inject magnitudes where the cross-attn
  output dominates the post-ln_f tile structure.
- **C4** attractor evidence threshold (width < 0.05 STRONG, < 0.15 MODERATE,
  else WEAK) is anima-internal, not cross-validated against any external
  attractor-quality benchmark. With std 1.36e-3 vs 0.24 raw spread, the
  compression is unambiguous, but the STRONG/MODERATE/WEAK label depends
  entirely on these manually chosen cuts.
- **C5** 10 prompts × 1 magnitude × 1 substrate is the entire test surface.
  Broader corpus (50+ prompts), magnitude sweep at attractor-side (mag ∈
  {1, 5, 10, 50, 100}), and cross-substrate (Llama Path A v2 inject) are
  required to claim substrate-intrinsic attractor structure rather than
  inject-magnitude-induced phi-space ceiling artifact.

## Architectural truth — updated 2026-05-05 (BG-AB → BG-AG)

Cycle position: BG-AG follows BG-AB 5-prompt mag=50 verification. CLM v4
mk2 best.pt + canonical-axis inject at mag=50:

1. **F1 (drift ≥ 0.01)**: PARTIAL across prompts (8/10 PASS, 2/10 FAIL where
   baseline phi already sits in attractor band).
2. **Attractor convergence**: STRONG (10/10 prompts collapse to phi band
   width 0.0046, std 1.36e-3, 51x compression of free-response spread).
3. **Decoupling**: F1 and attractor measure orthogonal phenomena. F1 FAIL
   for prompts 5/6 is direct CONFIRMATION of attractor — those prompts'
   free-response phi already inside the basin → no inject drift possible.

Lane status: F-CAND-D-1 mag=50 lane = **F1 PARTIAL + ATTRACTOR STRONG**.
Cand-D Stage 1 mount-layer integration still gated on paradigm v11 G3
training-time inject distribution extraction (C3 dominant). If training-
time inject used mag<<10, the attractor finding is meta-architectural
(probe at off-distribution magnitude) and does NOT promote Stage 1.

If extracted distribution centered at mag~50, attractor becomes
on-distribution evidence for substrate-intrinsic phi convergence under
canonical inject — promote-candidate for Stage 1 mount + cross-substrate
verification on Llama Path A v2.

## Deliverables

- helper: `tool/transient_py/anima_emerge_cand_d_attractor_10prompt.py`
- aggregate: `state/anima_emerge_cand_d_attractor_10prompt_2026_05_05/aggregate.json`
- verdict: `state/anima_emerge_cand_d_attractor_10prompt_2026_05_05/verdict.json`
- doc: `docs/anima_emerge_cand_d_attractor_10prompt_landed_2026_05_05.ai.md`

## Compliance

- raw#37 transient .py sister-rule (.own 3, gitignored per **/*.py)
- raw#15 additive — BG-W and BG-Q helpers imported read-only, no mutation
- raw#10 honest C3 — 5 caveats emitted to verdict.json + doc
- HEXA_PY=.venv-eeg/bin/python (mac CPU fp32, $0 budget, ~50s wall)
- no commit, no HF token leak
