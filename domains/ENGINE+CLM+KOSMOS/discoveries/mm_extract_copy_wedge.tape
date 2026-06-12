@V := "tape" :: spec [active]
  version = "1.0"

# F-BC-ANIMA-M4-CEILING wedge (b) — per-step `mm_extract [V×d]` copy probe (2026-05-28)
#
# seed: GPU.anima.md "## 🩺 진단" + STEP_RATE_LOG.md M4 wiring section flagged
#   "per-step `mm_extract` of [V×d] expert weights" as wedge (b) of the
#   F-BC-ANIMA-M4-CEILING follow-up — to be probed (cheap-first oracle) before
#   any cost-bearing fix or fire.
# harness: static analysis only. No fire. No pod. Read trainer + arch + bwd-lib
#   on origin/main and count call sites + shapes in the step loop.
# flow: probe → verdict → if REAL → propose simplest fix → file as a separate PR.
#   discovery → CLAIMS.tape → hexa verify → paper_on_discovery (if green path).

@N mm_extract_copy_wedge := "per-step [V×d] mm_extract IS a real wedge (~58–195% of pre-baseline step wall)" :: discovery [d=2026-05-28 active]
  seed       = "is wedge (b) the actual bottleneck after M4 GPU softmax/CE wiring lands?"
  method     = "static count of mm_extract calls in step loop + per-element cost model (farr_get+farr_set)"
  data       = "12 sites/step total. 2 × V*d (V=151643·d=64) = 19,410,304 elts (99.5%); 10 × small (wq/wk/wv/wo/wup/wdown) = 98,304 elts (0.5%)"
  finding    = "per-step copy ~19.5M FP64 elts via fn-call loop (~30–100 ns/elt) ≈ 585 ms – 1.95 s/step. Pre-baseline ~1 s/step → ≥58% of wall. Not noise."
  verdict    = "🟢 REAL WEDGE — wedge (b) is the dominant residual after M4 GPU softmax/CE lands"
  caveat     = "cost-share %% computed from fn-call cost model, not direct profiler. Lower bound conservative; actual share depends on Mac/H100 host CPU + arena state"

@N mm_extract_call_sites := "12 mm_extract sites per step — 2 dominant (V×d), 10 noise (small attn/MLP)" :: discovery [d=2026-05-28 active]
  seed       = "the pre-reg said 'per-step [V×d]' — is the V×d shape actually in the step loop, or did the pre-reg confuse w/ embedding shape?"
  method     = "grep mm_extract in CORE/DECODER/{train_v3_moe_longtrain,v3_moe_arch,v3_moe_bwd_lib,flame_mm}.hexa + trace step-loop scope"
  data       = "fwd: v3_moe_arch.hexa:101 mm_extract(M, exp_base, V, d) [V×d=9.7M]; bwd: v3_moe_arch.hexa:143 same [V×d=9.7M]; trainer L354/355/356/411/423/435 + bwd_lib L195/215/285/339/340/341 ten more (d² or h·d, ≤16K each)"
  finding    = "pre-reg shape is correct. v3_moe_fwd + v3_moe_bwd each extract a fresh [V×d] copy of the top-1 expert's weights per step. The other 10 small extracts (4·d² + 2·h·d per fwd & bwd) total 98K elts (0.5% of dominant pair) — noise"
  verdict    = "V×d shape confirmed in step-loop scope (called via v3_moe_fwd L483 + v3_moe_bwd L497 inside while step ≤ n_steps L319-575)"

@N mm_extract_root_cause := "mm_extract = farr_get+farr_set loop because `mm` requires index-0 handles (offset not accepted)" :: discovery [d=2026-05-28 active]
  seed       = "why is a copy required at all — can't `mm` read the slice in place?"
  method     = "read flame_mm.hexa:49-62 (mm_extract impl) + L50 comment"
  data       = "flame_mm.hexa L50: 'Copies a row-major sub-block of a PACKED buffer P (offset off) into a fresh index-0 farr, because farr_matmul takes index-0 handles (no offset).' The copy exists to satisfy the matmul API contract, not for correctness or device transfer."
  finding    = "root cause = `mm`/`farr_matmul` API surface does not accept an (handle, offset) pair. The copy is a workaround. Fixing the API surface eliminates the copy entirely (no new GPU builtin, no hoist required)."
  verdict    = "API-shape fix is feasible without new runtime kernels"

@N mm_extract_fix_proposal := "simplest fix = mm_offset (offset-aware matmul) — eliminates copy without new GPU builtin" :: proposal [d=2026-05-28 active]
  seed       = "what's the smallest patch that removes the V×d copy?"
  options    = "(i) offset-aware mm — `mm_offset(M, exp_base, V, d, zT, 1)` reads M[exp_base..] in place. (ii) hoist out of step loop — INFEASIBLE: M is mutated each step by AdamW. (iii) device-resident expert weights w/ farr_*_slice_gpu — bigger surgery (CPU/GPU residency state machine). (iv) document as unavoidable — false, (i) is feasible."
  selected   = "(i) offset-aware mm — pure stdlib addition in flame_mm.hexa; one new pub fn calling `farr_matmul_offset` (new 7-arg runtime carrier) OR `farr_matmul` with a view-handle. Keeps existing mm contract unchanged; only adds a sibling for packed-buffer slices."
  scope      = "1 new runtime fn (carrier seam, no GPU kernel — cuBLAS Dgemm already takes a `double*`+lda; pointer-arith only) + 1 new stdlib pub fn + 2 call-site edits in v3_moe_arch.hexa (L101 fwd, L143 bwd). Backward bwd-lib small extracts can stay (noise)."
  caveat     = "OUT OF SCOPE for THIS probe PR — analysis-only per task. Filed as a separate downstream PR if/when ranked next. The probe verdict 🟢 is the gate this PR delivers."

@N mm_extract_next_step := "downstream PR — implement (i) offset-aware mm + measure wall delta" :: deferred [d=2026-05-28 active]
  next       = "(a) add `farr_matmul_offset` runtime carrier (or equivalent view-handle) (b) add `mm_offset` stdlib wrapper (c) swap v3_moe_arch.hexa L101+L143 (d) re-measure step-rate on H100 to quantify the wall delta (e) update STEP_RATE_LOG.md with the post-fix row"
  pre-reg    = "expected wall delta = remove ~585 ms – 1.95 s/step ≈ 58–195% of pre-baseline. If post-M4 baseline (softmax/CE on GPU) is ~100–400 ms/step, removing ~585 ms is over-saturated → post-fix step rate becomes AdamW-CPU-bound (the next residual = M1 wiring is already landed, so the trajectory crosses ≥10 step/s gate is plausible). Falsifier: post-fix step-rate <50% improvement vs post-M4 baseline → revisit assumption about mm_extract cost share (model may underestimate arena fast-path or overestimate fn-call overhead)."
  caveat     = "predictions, not measurements — settled only by the downstream PR's actual H100 fire"
