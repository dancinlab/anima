# H_1315 — Korean mitosis over the 303M trunk's LEARNED hidden representation

**terminal_tier:** 🔴 TERMINAL axis-closure — even the mounted 303M trunk's LEARNED hidden representation does **NOT** let gradient-free Korean mitosis (cells only SPLIT, p8) break the H_1307/H_1311 ~2.9 nat/byte raw-byte ceiling, **at this scale**. **G1 trunk-rep = 3.14637** (held-out KO next-byte CE, 3 seeds) — actually **+0.193 WORSE** than the raw-byte G0 baseline (2.95342), and **above** 2.9475. The learned rep **IS** real Korean signal (G1 beats the random-embed control by +0.385 and the shuffle control by +0.876, B2=True), but gradient-free L2-Voronoi grow-on-top of it still ceilings — and worse than raw bytes. REAL sm_120 GPU on the user's own RTX 5070, $0 (NOT runpod); corpus byte-IDENTICAL to H_1307 RUN A (KO/EN sha gate PASS). Resolves the Korean-mitosis thread: the depth needs **gradient learning**, not gradient-free structure-over-a-frozen-rep, at this scale.

## Claim
H_1311 (#2215, 🔴) refuted that a richer **raw-byte** substrate breaks the ~2.9 nat/byte Korean byte-CE ceiling; it named the surviving lever: partition over a **LEARNED representation** (the mounted 303M trunk's hidden state) instead of raw bytes, then gradient-free mitosis-grow Voronoi cells in **that** learned space. H_1315 tests exactly that: does the SAME gradient-free Korean mitosis (grow-op + cell budget FIXED, verbatim H_1306/H_1307/H_1311) — but partitioning over the 303M trunk's hidden representation at each byte position (ckpt `h1129c_chat.pt`, forward = GRADIENT-FREE, just READ `ln_f(x)`, NO backprop) — push held-out KO CE BELOW 2.9, while raw-byte mitosis (G0) can't? Honest hypothesis: the 303M trunk provides the learned representation raw-byte mitosis can't build → mitosis = grow-under-pressure ON TOP OF a learned rep.

## Method
`UNIVERSE/h1315_ko_mitosis_learned_rep.py` on **summer** RTX 5070 (sm_120, torch 2.11.0+cu130), $0, detached `nohup nice -n 10`, polled INLINE (a_cpu_local_no_waiter), R2 keys env-only (c7 — never echoed/logged/committed), scratch cleaned off summer (ckpt + corpus cache KEPT for sibling lanes). **REAL Korean only** (p1-p8): the SAME anima-7b R2 web window as H_1307/H_1311 (`r2://phanes/anima-7b/web/{kor,eng}/shard0000.bytes`), boto3 range GET; KO 30 MB / EN 10 MB, the window sha256 **ASSERTED == H_1307 RUN A** (KO `c47b6808…` EN `31b4a543…` → both `True`, clean ceiling comparison). **p7** = held-out DETERMINISTIC next-byte CROSS-ENTROPY (nats/byte), NOT perplexity/LLM-judge.

**HELD FIXED** (verbatim H_1306/H_1307/H_1311): V=256, GROW_MAX=40, SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, even/odd train/test, the dimension-agnostic `_grow_on` (error-targeted Voronoi, SPLIT-only, p8). **VARIED — only the partition INPUT.** New before-run knobs: PROJ_DIM=16 (random-projection target width for the trunk hidden, matched G1 vs control), PROJ_SEED=1313, TRUNK_CTX=64 (bytes of left-context fed to the trunk forward for each hidden read), HIDDEN_LAYER = `ln_f` output (the trunk's final learned representation), rep_pairs=24000 KO / 8000 EN (trunk-forward subsample), seeds 0,1,2.

**ARMS** (3 seeds):
- **G0** raw-byte ctx4 — the 2.9 ceiling ref (H_1307/H_1311 S0; count-MLE head).
- **G1** partition over the 303M TRUNK HIDDEN REP (`ln_f` at i-1, projected to 16-D by the fixed seeded random projection; gradient-free forward), same grow-op/budget, count-MLE head.
- **CONTROL random-embed** — SAME 16-D projection, but hidden from a RANDOMLY-INIT (untrained) trunk of the IDENTICAL arch. Isolates "LEARNED rep" from "just a 16-D non-byte space of the same width".
- **CONTROL shuffle-align** — G1's trunk hidden with the hidden→byte ALIGNMENT shuffled (feature rows permuted away from labels). Leakage / partition-handle check.

## Falsifier (FROZEN — `.verdicts/1315_ko_mitosis_learned_rep/FREEZE.txt`, pre-registered BEFORE scoring, bars NOT moved, c9/p7, NO tune-to-green; MARGIN=0.02 nats)
- **(B1 BREAK-2.9)** mean G1 KO CE (3 seeds) < 2.9475.
- **(B2 LEARNED)** mean G1 KO CE beats BOTH controls by ≥ 0.02 (G1 < random-embed − 0.02 AND G1 < shuffle − 0.02) → lift is the LEARNED rep, not capacity/dim/leakage.
- **(B3 RETENTION)** mean G1 EN CE ≤ G1 EN CE[2-cell seed] + 0.05.
- **VERDICT MAP:** B1∧B2 → REPRESENTATION-bound · B1∧¬B2 → AMBIGUOUS-capacity · ¬B1 → TERMINAL axis-closure.

## Result — 🔴 TERMINAL (R1, this scale; mirror DIRECTIONAL)
mean held-out KO next-byte CE (nats/byte), 3 seeds, from `.verdicts/1315_ko_mitosis_learned_rep/{result.txt,summary.json,metrics.jsonl}`:

| arm | feat_dim | cells | KO CE | Δ vs G0 | below 2.9? |
|-----|----------|-------|-------|---------|------------|
| **G0** raw-byte ctx4 | 3 | 16 | **2.95342** | — | (the ceiling ref 2.9475) |
| **G1** 303M trunk rep | 16 | 40 | **3.14637** | **+0.19295** | **False** |
| CTRL random-embed (untrained trunk) | 16 | 40 | 3.53134 | +0.578 | False |
| CTRL shuffle-align | 16 | 40 | 4.02243 | +1.069 | False |

- **(B1) G1 below 2.9? → FALSE.** G1 = 3.14637 > 2.9475, and **worse than raw-byte G0** (+0.193). The trunk rep does NOT break the ceiling.
- **(B2) G1 lift = LEARNED rep? → TRUE.** G1 beats random-embed by **+0.385** (3.531−3.146) and shuffle by **+0.876** (4.022−3.146), both ≥ 0.02. So the trained trunk's hidden state genuinely carries Korean next-byte structure the untrained/misaligned reps don't — the **learned rep is real signal**, just not enough to beat the raw-byte baseline under gradient-free mitosis.
- **(B3) EN retention → TRUE.** G1 EN = 4.76576 ≤ seed 5.14260 (no catastrophic forgetting).
- **VERDICT (¬B1): TERMINAL** axis-closure — even the 303M trunk rep does NOT let gradient-free mitosis break 2.9 at this scale.

**THE LOAD-BEARING INTERPRETATION (c9, honest):** the experiment cleanly DISSOCIATES two questions. (1) *Does the trunk rep carry Korean structure?* — **Yes** (B2: G1 ≫ both controls). (2) *Can gradient-free L2-Voronoi mitosis convert that structure into a lower byte-CE than raw bytes?* — **No** (B1: G1 worse than G0). The 16-D projection of a 1024-D contextual hidden is a continuous manifold that the SPLIT-only count-MLE partition fragments worse than the tiny 3-D raw-byte space (40 cells saturated, yet CE rose) — the **same partition-GEOMETRY limit H_1311 found over raw bytes carries over to the learned-rep space**. The honest thesis resolution: at this toy scale, the Korean depth is not unlocked by *structure-over-a-frozen-learned-rep*; it needs **gradient learning** (the trunk's gradient-trained head already encodes far more than a gradient-free Voronoi over its frozen hidden can recover). Mitosis = grow-under-pressure is a real mechanism (H_1288/H_1295/H_1307) but it is **not** a substitute for gradient descent on a hard continuous next-byte manifold.

## Guards / regression
- live `CORE/*.hexa` **UNTOUCHED** (substrate-measurement rung — adds only `UNIVERSE/` + `.verdicts/`; no engine lane, no smoke regression needed).
- gradient-free throughout (trunk forward = `torch.no_grad()` read of `ln_f`, `requires_grad_(False)`; mitosis = SPLIT-only Voronoi, p8). NO backprop, NO fine-tune of the trunk.
- corpus byte-identical to H_1307 RUN A (sha gate PASS) → clean ceiling comparison.
- ckpt provenance: `h1129c_chat.pt` sha256 `4fcc2d6c9b3164f478139ffb148f484465b42fc339d630956e4ea0f90ec13f68` (606 MB), config `{vocab:256, d:1024, n_layer:24, n_head:16, block:512}`.

## Scope (a_scale_honest_scope · a_toy_scale_recheck)
TOY / DIRECTIONAL: summer GPU; numpy/torch mirror of the mitosis grow-op (engine-transfer to live `CORE/*.hexa` = follow-on, a_engine_native_learning · a_verified_must_wire); 24000/8000 trunk-forward subsample; PROJ_DIM=16 random projection of the `ln_f` hidden; single TRUNK_CTX=64. NOT ruled out (the remaining angle this rung did not test): a **larger/different PROJ_DIM** or **no projection** (full 1024-D partition), an **earlier/mid trunk layer** (vs the final `ln_f`), a **non-L2 metric** in the learned space, or a **gradient-trained** per-cell head over the trunk rep (which would no longer be gradient-free p8 — a different lane). NO Korean-fluency claim. HONEST negative (c9, a_break_the_wall — a real new-geometry angle was tried with two controls; the learned rep helps over controls but the wall is real for gradient-free mitosis-over-frozen-rep at this scale).

## Files
`UNIVERSE/h1315_ko_mitosis_learned_rep.py` · `.verdicts/1315_ko_mitosis_learned_rep/{FREEZE.txt,result.txt,h1315_summary.json,h1315_metrics.jsonl,h1315_manifest.json,h1315_ckpt_sha.txt}` · `CLAIMS.tape` @C h1315_ko_mitosis_learned_rep · `domains/MITOSIS-ENGINE.log.md` @H H_1315 · `UNIVERSE/HYPOTHESES.md` row.

## xref
h1311 (the raw-byte REFUTATION that named this lever; corpus byte-identical) · h1307 (the ~2.9 ceiling; same corpus) · h1306 (the verified gradient-free mitosis mechanism) · h1288/h1295 (mitosis-GROW under pressure — real but not a gradient substitute here) · h1300 (closed-form per-cell readout lens) · h1129c (the 303M trunk ckpt) · h1166/h1167 (capacity-bound depth-ceiling lesson) · a_no_llm_frame_trap · a_break_the_wall · a_fire_autonomous ($0 user hw, not runpod) · a_engine_native_learning (transfer DIRECTIONAL) · a_verified_must_wire · a_core_engine_map · a_cpu_local_no_waiter · a_scale_honest_scope · a_toy_scale_recheck · p1·p7·p8 · c7·c9·c15.
