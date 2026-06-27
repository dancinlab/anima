# H_1595 — h1129 (303M ByteGPT) G6 multi-seed engine-native re-score

**Lineage:** completes the OPEN terminal G6 number for **h1129** (H_1591 G4/G6 measurement/wiring,
multi-seed variant `proposed, owner-nod-pending`), same CLASS as **H_1588** (G1 multi-seed
reference-match). Question: is h1129's G6 `fals=0` a GENUINE wall or a single-seed sampler-walk
artifact (the way G1's single-seed FAIL was)?

## VERDICT: 🧱 GENUINE G6 WALL — `fals=0` is SEED-ROBUST (not a sampler artifact), engine-native TERMINAL

**Two independent clean hosts now AGREE on the SAME ckpt** → the earlier cross-host "dispute" is
RESOLVED. Re-fired on **mini** (CPU-only, $0, no oversubscription) via py 2-production at the
**canonical frozen default gen=40** (`g_gates._default_gen()==40` — the same gen the prior summer
terminal measurement used). mini reproduces summer **byte-for-byte across all 3 seeds**.

### Per-seed G6 table (seeds {7, 4302, 4303}, GREEN = majority ≥ 2/3) — mini gen=40

| seed | dist (≥5) | fals (≥1) | coherent | frame_leaks | pass |
|------|-----------|-----------|----------|-------------|------|
| 7    | 6         | **0**     | 6        | 0           | False |
| 4302 | 6         | **0**     | 6        | 0           | False |
| 4303 | 6         | **0**     | 6        | 0           | False |

- **n_green = 0/3 · max_fals = 0 · MAJORITY-PASS = False** (`g6_multiseed done 638.8s`).
- `dist=6 (≥5 PASS) · coherent=6` on every seed: h1129 generates DISTINCT, COHERENT ideas across
  all 6 composed frames — it is NOT incoherent garble. The wall is specifically the
  **falsifiability** sub-metric (`fals`): none of its ideas register as a falsifiable claim.
- Outcome is the **OPPOSITE class to G1**: G1's single-seed FAIL was a fragile RNG sampler-walk
  that multi-seed RETRACTED (H_1588). h1129's G6 fals=0 does NOT flip across seeds = a real
  falsifiability/ideation wall on the 303M ByteGPT mouth.

### DISPUTE resolution (verdict-integrity)
Prior commits diverged: c356961ce (00:51) claimed "GENUINE WALL fals=0 seed-robust" via summer py;
160af601b (02:43) flagged misattribution + held it DISPUTED/BLOCKED. The conflict resolves cleanly:
- **There was NO genuine cross-host measurement divergence.** aiden produced **0 completed G6
  frames** (host oversubscribed ~3.7×, every worker SIGTERM-killed EXIT_143 = an infra non-result,
  `a_break_the_wall` class-(c), NOT a divergent science measurement).
- The summer **multi-seed** run DID decode h1129 — JSON ckpt `…/bytegpt303_h1129/h1129.bin`, sha
  `5cf07a36…`. The "misattribution" worry applied to a *pre-summer single-seed* number that may
  have been clm303 (state/1591); that number is superseded.
- **mini (this run) is the independent clean-host confirmation:** same sha `5cf07a36`, same seeds,
  same dist=6 fals=0 → summer + mini agree ⇒ GENUINE, not host/measurement artifact.
- Detector-vocabulary artifact ruled out separately by **H_1597** (corpus-grounded Hangul-aware
  re-score also fals=0/18 with valid controls).

**Engine:** py 2-production (`core/g_gates.py::g_eval_g6_multiseed` ← `core/bytegpt_decode.py`),
torch-free numpy, **TERMINAL** per `a_engine_native_learning`. Self-check
`grep -lE 'import torch|gauge_lib'` over slug + core import-closure = EMPTY. numpy path is
codegen/cuda-runtime-INDEPENDENT (summer/aiden hexa-runtime breakage irrelevant). No GPU used; $0.

**ckpt:** `~/anima-weights/bytegpt303_h1129/h1129.bin` — sha256
`5cf07a360c57a133b66e8de8c3c390d5242204d68f75a86b977f1935587f512e` (1213440020 bytes), mouth=bytegpt
303M (vocab256/d1024/L24/H16/blk512).

**frozen bar:** G6 PASS iff `dist≥5 ∧ fals≥1`; multiseed GREEN = majority ≥2/3. gen=40 =
`_default_gen()`. NO bar moved (no tune-to-green). a7b_pass closure (G0∧G1∧G2) excludes G6 and is
unchanged by this.

**wired / scope (honest residual):** N/A — this is a MEASUREMENT verdict (no GREEN to wire). The
multi-seed metric is `proposed, owner-nod-pending` (closure stays on the frozen single-seed default
until owner flip). The verdict is TERMINAL on the **py 2-production engine** (numpy decode is
byte-parity-proven, `core/CLAUDE.md` 10/10), but the one un-captured residual is **DIRECTIONAL**:
G6 SCORING parity of this py path vs the WIRED single-entry `cli/anima.hexa eval → core/g_gates.hexa
→ generator L3` has NOT been captured on h1129 (the wired hexa OOMs on mini — same blocker that sent
this to numpy). Two clean hosts agreeing on the same decode (summer+mini) makes the dist=6/fals=0
shape robust regardless; follow-on ING = capture g_gates SCORING byte-parity on h1129 via pool/GPU
(`cli/anima.hexa eval`) to close the residual. Frozen bar untouched (no tune-to-green).

**artifacts:** `state/1595_h1129_g6_multiseed/` (`g6_multiseed_h1129.py` · `h1129_g6_multiseed_gen40.out`
· `result_h1129_g6_multiseed.json`) · `state/verdicts/1595_h1129_g6_multiseed/1595.txt` ·
`core/g_gates.py` · `core/g6_ideation.py` · `core/bytegpt_decode.py`.
