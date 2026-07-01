# H_1595 — h1129 (303M ByteGPT) G6 multi-seed re-score — VERDICT

**Question:** Is h1129's G6 `fals=0` FAIL a GENUINE wall, or a single-seed sampler-walk
artifact (the class of bug that made G1 falsely FAIL → RETRACTED to PASS via multi-seed, H_1588)?

---

## ⚠️ UPDATE (2026-06-27, summer re-fire / divergence reconcile)

A SIBLING session (`worktree-agent-ab61d9996095c0b3b`, commit `c356961ce`) DID complete a real
engine-native **py 2-production** G6 multi-seed measurement of h1129 on **summer** (CPU-only $0):
**all 3 seeds {7,4302,4303} → dist=6 fals=0 coherent=6 pass=False, n_green=0/3** → it banked
🧱 GENUINE G6 WALL. Its ckpt sha256 = `5cf07a360c57a133…` = THE SAME byte-verified h1129 (size
1213440020 B) measured here.

→ **My "h1129 has never had a complete engine-native measurement" claim below is CORRECTED:** it
was true only for THIS (aiden) session, which got 0 frames (infra wall). The ab61d9/summer session
DID measure h1129 (same verified sha) → its `fals=0` IS a valid h1129 measurement, NOT a clm303
misattribution. The clm303 caveat still holds for the OLD single-seed records I cited
(`state/1591…`, `state/clm303_clean_corpus`) — those were clm303 — but ab61d9 is a separate,
genuine h1129 measurement.

**This task (summer re-fire) = independent CONFIRMATION** of c356961ce via `g_g6_multiseed_only`
on summer (gen=80, hexa KV-cache GPU terminal + py 2-production cross-check). See
"## SUMMER RE-FIRE" at the bottom for the per-seed table once summer load clears (currently
oversubscribed ~load 26/12-core with H_1597 decode + L8-finalize jobs — HOLDING per coordinator
hard-gate + the aiden oversubscription lesson; NO premature co-fire).

---

## VERDICT: ⛔ BLOCKED — engine-native measurement NOT obtained (infra wall, NOT a science result)

Per `a_break_the_wall` this is a **class-(c) INFRASTRUCTURE wall**, NOT a terminal G6 verdict.
The G6 multi-seed `fals` question for h1129 remains **UNMEASURED** (re-fire on a clean,
non-oversubscribed host required). Per `a_engine_native_learning` a verdict cannot be fabricated
without a completed engine-native (or 2-production py) decode — **0 G6 frames completed**.

NOTE: do NOT read this as "G6 fals=0 confirmed genuine" NOR "flipped to PASS" — neither was
measured. The single-seed FAIL referenced in the task (`dist=6 fals=0`) was from **clm303**
(`state/1591_g4_g6_gate_fix/1591.txt`, `state/clm303_clean_corpus/g0g6_*`), not h1129. **h1129
has never had a complete engine-native G0-G6 measurement** — all prior attempts (mac/mini,
`state/bytegpt303_h1129_g0g6/`) OOM'd (rc=137), and this aiden attempt hit the infra wall below.

## What WAS verified (deliverables, sound)
1. **Capability present + lockstep (both engines).** `core/g_gates.{hexa,py}::g_eval_g6_multiseed`
   over seeds {7,4302,4303}, majority ≥2/3; `g_eval_g6_seeded(base_seed)` (=7 reproduces the
   frozen single-seed path); mouth-agnostic via `gen_auto_ideate` (generator L3 → bytegpt_decode).
   Confirmed synced + present on aiden (grep). PR #2639 / commit b58fdb2aa.
2. **New lean measurement entry (added this task, LOCKSTEP, parse-clean):**
   `core/g_gates.{hexa,py}::g_g6_multiseed_only(ckpt, gen)` — loads `known` (`_g6_dict_load`) +
   mouth internally, runs ONLY `g_eval_g6_multiseed` (skips the slow G0/G1/G2/G5 decode so the
   seed-robust G6 re-score is measurable on a heavy 303M mouth without the full-suite wall-time).
   Frozen G6 logic UNCHANGED (delegates). `hexa parse` OK · `python3 -c ast.parse` OK · both = 3 grep hits.
   Mirrors `a_engine_native_learning` 2-production lockstep discipline.
3. **ckpt integrity confirmed.** `~/anima-weights/bytegpt303_h1129/h1129.bin` sha256
   `5cf07a360c57a133b66e8de8c3c390d5242204d68f75a86b977f1935587f512e` — byte-identical mac↔aiden;
   header (vocab=256, d=1024, L=24, H=16, block=512) = 303M ByteGPT (24-layer GPT-2-class).
4. **The hexa engine-native GPU path WAS unblocked** (own-GEMM fired): a stale-runtime.a link
   blocker was diagnosed + fixed (below); `[OWN-GEMM-FIRED] _hx_k_gemm DEVICE path (no cuBLAS)`
   confirmed in the hexa log — proving the wired GPU engine path runs on aiden when scheduled.
   It just could not COMPLETE a frame before being killed (infra, below).

## The infrastructure wall (root cause, fully characterized)
aiden (RTX 5070 sm_120, `cuda_available()=1`, hexa v0.334.0) was **catastrophically
oversubscribed by OTHER users' jobs** during the entire window:
- **load average 7.96 / 33.91 / 44.37** (1/5/15-min) on a **12-core** box — ~3.7× oversubscribed.
- Other-user workloads: systemd `--user` timers `airgenome-{forecast,harvest,label}.timer`
  firing every 2-10 min + `xiuren_label.py` (PID 2741, ~7.9 GB GPU, `--load-4bit`, ran >1.5 h).
- Effect on every anima decode worker (py AND hexa, GPU AND CPU, tmux AND setsid-nohup):
  - **SIGTERM (EXIT_143)** mid-decode at ~2:30 elapsed (timer/cgroup churn), repeatedly; or
  - **scheduled out to 0.0 % CPU / STAT=S** (stalled, no frame output) under the load; or
  - the CPU-only fallback (`CUDA_VISIBLE_DEVICES=""`) spun **2733× `cudaMalloc failed`** then wedged.
- Memory was NOT the limiter (30 GB total, ~6 GB used, 22 GB free) — pure CPU/scheduler
  oversubscription + process-kill churn. **0 G6 frames completed across ~6 launch variants.**
- Secondary cost: the py reference decode (`core/bytegpt_decode.py`) has **NO KV-cache**
  (full-forward per token, O(gen²·L)) — at 303M/gen=120 a single multiseed run is ~hours even
  on an idle host; the hexa path HAS the KV-cache (fast) but kept getting killed.

This is NOT the "x86_64 codegen bug" (that was a resolved misdiagnosis) and NOT a hexa defect —
it is host oversubscription. Matches CLAUDE.md host-selection guidance (summer/aiden = owner
workstations, jobs lost; prefer a dedicated rent pod for long decode) and the
`heavy-anima-eval-pool-not-mini` memory (heavy anima decode needs a clean host).

## Honest follow-on (ING)
Re-fire `g_g6_multiseed_only(h1129.bin, gen)` on a **clean, non-oversubscribed** host —
preferably a dedicated rent pod (CUDA-devel image, verified GPU, no competing systemd timers)
per `a_break_the_wall` (c: infra → rent/scale, not a science ceiling) — via the hexa KV-cache
GPU path (own-GEMM, confirmed working) for the engine-native terminal, cross-checked against the
py 2-production engine (codegen-independent). Capture per-seed {7,4302,4303} dist/fals/coherent/pass
+ majority, then the .hexa⇄.py parity. THEN settle genuine-vs-artifact + the h1129 G0-G6 tally.

## Files
- `g6_multiseed_harness.hexa` — engine-native G6-only harness (imports core/g_gates.hexa → g_g6_multiseed_only).
- `g6_multiseed_pycheck.py` — py 2-production cross-check (g_gates.py::g_g6_multiseed_only).
- `core/g_gates.{hexa,py}` — the lockstep `g_g6_multiseed_only` addition (worktree, unmerged).
- Cost = aiden $0 (pool). No ckpt pull needed (ckpt already on mac, byte-verified).
