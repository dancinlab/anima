@V := "tape" :: spec [active]
  version = "1.0"

# DECODER MoE mode-collapse — micro-exp root-cause re-attribution (2026-05-28)
#
# seed: #1296 / Pod C — production MoE (d=64, V=151643) decode = [1,..,1],
#   distinct=1. Prior fires varied corpus-diversity (#1296 FAIL) + routing/aux
#   (Pod C FAIL). Both ruled OUT. This discovery isolates the actual driver with
#   a routing-free toy (Emb[V x d] + Head[V x d] successor LM, k -> (k+1)%V).
# harness: CORE/DECODER/mx_capacity_cliff.hexa ($0 mac/pool-local, hexa-native).
# flow: discovery -> CLAIMS.tape -> hexa verify -> .verdicts/ -> paper_on_discovery.

@N dec_capfloor := "head-rank capacity floor V*(d) grows geometrically — d=64 ample for V=151643" :: discovery [d=2026-05-28 active]
  seed    = "is the collapse a head-rank wall (d too small for V)?"
  method  = "mx_capacity_cliff: high-epoch (150) d x V grid, largest V fully solved per d"
  data    = "d=2 V*<32 · d=3 V*~32 · d=4 V*~128 · d=5/6 V*>=256 — ~3.5x per +1 d (geometric)"
  finding = "V*(d) ~ 16 * 3.5^(d-2): V=151643 needs only d~10; d=64/256 >> floor"
  verdict = "rank NOT the production bottleneck (toy-supported); cap wall real but far below prod d"
  caveat  = "toy-only · learnable Emb + clean permutation · transfer unverified"

@N dec_undertrain := "production collapse dominated by step/data budget, not d and not routing" :: discovery [d=2026-05-28 active]
  seed       = "if rank is ample, why does d=64 collapse?"
  method     = "mx_capacity_cliff step-budget sweep: distinct vs epochs at fixed d (V=64)"
  data       = "d>=4 needs ~50 epochs to fully escape; epochs-to-escape grows with V (d=4 solves V=128@150ep, fails V=256@150ep)"
  finding    = "fire ran n_steps=200 PER-TOKEN = 200 presentations; a single pass over V=151643 needs 151643; fire is ~38000x short of one epoch"
  verdict    = "under-training is the binding lever (toy-supported): corpus-size x epochs, not d/aux/corpus-balance"
  prediction = "running A(d=256+aux) AND B(d=256 no-aux) BOTH collapse 2/5 — d cannot fix a step deficit"
  confirmed  = "PR #1315 fire CONFIRMED the pre-registered prediction: A=B=C all 2/5, decode=[1,..]. d 64->256 only nudged TTR 0.01->0.02 (no escape); aux on(A)~off(B) so aux contribution ~0. d AND routing both NOT the lever — matches toy."
  prod_result = "M4B_LONGTRAIN fire (2026-05-28, 3x H100 epoch sweep LO=1/MID=12/HI=60 @ d=64 V=151643): UNVERIFIABLE-AT-SCALE (toolchain-blocked). The dec_undertrain lever could NOT be tested at production V because the trainer is CPU-bound at ~0.26s/step (MID~7d, HI~33d wall) and the hexa-lang cuBLAS gemv that would rescue it is BROKEN. Toy->production transfer is thus unverifiable with the current toolchain — NOT confirmed, NOT refuted. See CORE/DECODER/M4B_LONGTRAIN_RESULT.md."

@N dec_undertrain_prod_blockers := "production-scale dec_undertrain test blocked by 3 measured hexa-lang toolchain ceilings" :: discovery [d=2026-05-28 active]
  seed     = "does presentations >> V (~50 epochs, d=64, full corpus) escape collapse at production V=151643?"
  method   = "3x H100 80GB epoch-budget sweep (LO=1/MID=12/HI=60), single var = M4B_EPOCHS, real Qwen BPE"
  blocker1 = "BPE encode is O(text_bytes x n_merges): tokenizer_bpe.hexa get_merge_rank is a LINEAR scan over 151387 merges/pair. merge-table LOAD O(1) (358ms) but ENCODE intractable — full 1.27MB corpus did not finish in 15.5min @100%CPU; 63KB unfinished in 180s; only 24-line/6.6KB (n_toks=6034) tractable."
  blocker2 = "cuBLAS gemv BROKEN for [V=151643 x d=64]@[d x 1]: cuda_available()==1 (glue OK) but _hx_cuda_farr_matmul_gpu -> 'cudaMemcpy C D2H failed: illegal memory access' -> handle -1. GPU util/mem 0 even mid-train."
  blocker3 = "O(V) per-step CPU cost: ~0.26s/step (1ep=1507steps unfinished in 401s). mm_extract copies [V x d]=9.7M doubles PER TOKEN + O(V) softmax/argmax/loss loops dominate; cuBLAS (even if working) only accelerates the one gemv."
  finding  = "wall @0.26s/step: LO~7min (feasible), MID~7days, HI~33days (both infeasible). pods idle-killed (GPU 0%) before any clean verdict."
  verdict  = "dec_undertrain at production V is UNVERIFIABLE-AT-SCALE under current hexa-lang. Blockers are toolchain (BPE + cuBLAS + O(V) per-step), NOT the anima trainer."

@N dec_saga_reframe := "M4b saga tested the wrong levers — diversity/routing/capacity all secondary to data+steps" :: synthesis [d=2026-05-28 active]
  ruled_out    = "corpus-diversity (#1296) · routing/aux (Pod C + #1315 A~B) · head-rank (dec_capfloor + #1315 d 64->256 no escape)"
  binding      = "step/data budget (dec_undertrain) — every fire used <=200 token-steps / 24-line corpus, never varied it"
  blocker      = "the binding lever remains UNTESTED at scale. M4B_LONGTRAIN fire (2026-05-28) PINNED the precise toolchain ceilings (dec_undertrain_prod_blockers): (1) hexa-lang BPE encode O(text x n_merges), (2) hexa-lang cuBLAS gemv illegal-access for [V x 1], (3) O(V) per-step CPU cost ~0.26s/step. ALL three are hexa-lang, not anima. Filed a_runpod_inbox."
  next         = "hexa-lang fixes: (a) get_merge_rank hashmap O(1), (b) fix _hx_cuda_farr_matmul_gpu tall-N=1 gemv D2H, (c) offset-aware gemv to kill the per-step V x d mm_extract copy -> THEN re-fire the epoch sweep."
  closure      = "NOT full closure — 4 levers ruled out + binding lever identified (toy+fire-consistent) but UNVERIFIABLE-AT-SCALE (toolchain-blocked, root-caused). no /paper until the toolchain unblock + re-fire (a_paper_only_at_closure)."

@N dec_undertrain_m5_attempt_2026_05_28 := "F-BC-ANIMA-M4-CEILING M5 fire attempt aborted on RunPod/vast SSH transport outage" :: attempt [d=2026-05-28 active]
  seed       = "M4 wiring landed (anima PR #1320 + #1321) — measure step-rate on H100 with M4 wiring, decide if M1 + mm_extract follow-up wedges are needed (gate <10 step/s)."
  method     = "hexa cloud rent runpod H100 SXM (NVIDIA H100 80GB HBM3, 50GiB disk, owner=bc-anima-m5). Stage 1 = time over 100 steps via M4B_MAX_STEPS=100. Stage 2 = full dec_undertrain budget capped at remaining $5-spend / 30min-wall. Falsifier: F-BC-ANIMA-M4-CEILING (pre-registered in STEP_RATE_LOG.md)."
  pods_tried = "(1) vast 37868501 ssh6.vast.ai:28500 — resolve OK, hexa cloud exec -> ssh transport failure exit 255. (2) vast 38095989 ssh9.vast.ai:15988 — resolve OK, ssh transport failure exit 255. (3) RUNPOD 3e541pil5jazhk freshly-rented, ssh-port 64.247.201.49:11038 — registry confirmed READY but ~7min of polling (every 8-15s) returned the same ssh transport failure exit 255 from hexa cloud exec verbatim."
  guard_text = "hexa cloud exec guard verbatim: '[cloud] cloud_exec: ssh transport failure (exit 255) — host unreachable (connection refused / timeout / auth / changed host key). The pod may be alive and billing but not accepting SSH — a vast.ai/RunPod transport outage. Stop retrying; verify reachability or tear the pod down.'"
  teardown   = "hexa cloud down 3e541pil5jazhk --provider runpod -> '[cloud] down runpod: terminated 3e541pil5jazhk / [cloud] forgot 3e541pil5jazhk (registry status=closed)'. Post-check hexa cloud list --provider runpod -> 0 pods. hexa cloud pods -> pods=0 jobs=0."
  budget     = "wall=~501s (~8.4min of 30min cap). spend=~$0.56 (~11% of $5 cap, est. $4/hr H100 SXM). Stage 1 NOT entered (zero trainer steps run). Stage 2 NOT entered."
  finding    = "F-BC-ANIMA-M4-CEILING UNMEASURED — falsifier not reached. Result is NOT a measurement of the M4 wiring; it is a measurement of pod SSH-transport availability on the day of the fire. Three pods in a row (2 vast cached + 1 RunPod freshly-rented) declined SSH — same outage class already noted in the post-M4 STEP_RATE_LOG entry, today's attempt confirms the outage extends to fresh pod rentals."
  verdict    = "white-circle UNVERIFIABLE-AT-SCALE (infrastructure-blocked) — distinct from the prior dec_undertrain_prod_blockers verdict (that one was toolchain-blocked: BPE + cuBLAS + O(V) per-step). This attempt did not even reach toolchain ground; it stopped at the SSH transport layer. M4 PARTIAL verdict on the wiring itself remains UNCHANGED (parse clean + byte-eq proven, wall-time still deferred)."
  next       = "re-attempt M5 when SSH transport is reliably available (try a different region or wait out the outage). The M1 farr_adamw_step_gpu wedge + mm_extract GPU port can be prepped offline so the next live H100 fire can run end-to-end without a return trip to the pod. No CLAIMS.tape entry (per g5: no LLM self-judge of correctness; this is a no-run report)."
