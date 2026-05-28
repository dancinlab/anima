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

@N dec_expert_axis := "expert-count E does NOT change collapse at toy scale — all cells escape, but utilization decays with E (winner-take-all onset)" :: discovery [d=2026-05-29 active]
  seed    = "production #1315 collapsed at E=2; E was never swept. Does E↑ (2->4->8) help/hurt MoE escape, and does load-balance correlate with escape?"
  method  = "mx_expert_sweep.hexa — top-1 hard-routed MoE successor LM (k->(k+1)%V), grid d{8,16} x V{32,64} x E{1,2,4,8}, 150 epochs. measure distinct_decoded/V, distinct_experts_used/E, per-expert routing fraction f_e."
  data    = "ALL 16 cells [ESCAPE] (distinct_decoded==V). experts_used: E<=4 -> full (E/E), E=8 -> only 5-6/8 active (2-3 experts get 0 routing). f_e spread widens with E but some experts die (f_e=0)."
  finding = "at toy scale (small V, adequate epochs) E is ORTHOGONAL to escape — the model escapes whether E=1 or E=8. E↑ does NOT help (E=1 already escapes) and does NOT hurt distinct-token coverage, but DOES seed winner-take-all: at E=8 some experts get zero routing (dead experts), the toy onset of the production single-expert collapse."
  verdict = "routing/E is NOT the escape lever (toy-supported) — consistent with #1315 (E=2 prod collapse was NOT fixed by routing/aux, and toy shows E=8 wouldn't fix it either). escape is governed by capacity+budget (dec_capfloor + dec_undertrain), not expert count. dead-expert onset at E=8 is the toy seed of prod winner-take-all."
  caveat  = "toy-only (V<=64, routing-free task is trivially separable so EVERY config escapes — the ESCAPE signal is uninformative at this V; the INFORMATIVE signal is the utilization decay). transfer-unverified: prod V=151643 is where E might matter differently. cf [[feedback-toy-scale-transfer]]."

@N dec_undertrain_m5_premise_2026_05_29 := "F-BC-ANIMA-M4-CEILING M5 re-attempt — hexat #1984 emit-segfault FIXED (premise ✅), step-rate STILL UNMEASURED on a deeper bootstrap-seed gap" :: measurement [d=2026-05-29 active]
  seed       = "hexa-lang #1984 (build/hexat_linux rebuilt, commit 7bb01a108) claims to fix the emit-segfault that blocked 5 prior M5 step-rate attempts. Re-fire on one H100, fresh origin/main hexa-lang clone, CPU-only build, measure steps/sec of train_v3_moe_longtrain (M4-wired trainer)."
  method     = "RunPod H100 SXM 80GB (pod q0ynubdw5s4e1v, 208 vCPU, $3.29/hr). hexa cloud run/copy-to/copy-from --insecure (cloud-guard regular path). PUBLIC_KEY=RunPod-Key-Go.pub injected explicitly (avoids the entry-(4) id_ed25519 key mismatch — RunPod-Key-Go SSH_OK reproduced). Detached build+fire via setsid nohup -> /work/STATUS.log (survives SSH drop). Pre-transpiled trainer.c from anima origin/probe-m5-walltime (BUILD-GREEN-last-session artifact)."
  premise_ok = "hexat #1984 FIXES the emit segfault. ./build/hexat_linux self/runtime_core_emit.hexa /tmp/rc.c -> rc=0, 11644 lines. ALL 30+ *_emit.hexa under fresh origin/main clone (e4c831c) transpiled rc=0 (135..11644 lines). The rc=139 segfault of entries (3)/(5) is GONE. F-BC-ANIMA-M4-CEILING premise (segfault resolved) = PASS / 🔵 CONFIRMED."
  blocker_new = "BUILD STILL FAILS (clang_rc=1) one layer deeper. hexat TRANSPILES *_emit.hexa -> C, but that C is an EMITTER PROGRAM (prints runtime_core.c to stdout; HX_VSF appears as hexa_str(\"#define HX_VSF...\") string-literals, not declarations; emit header: 'Invocation: hexa-run <emit>.hexa <output-path>'). To get the real runtime_core.c (281KB) the emitter must be COMPILED then RUN — but the emitter #include \"runtime.h\" and links hexa_str/hexa_void/rt_write_file (runtime.c symbols), and runtime.c #include \"runtime_core.c\" (line 2149) = the file we are trying to produce = pure circular. The only cycle-breaker (a prebuilt stage0 interpreter build/hexa_stage0, or a committed runtime_core.c) is ABSENT from origin/main: ./build/hexa_linux run -> 'error: stage0 interpreter not found ... rebuild with: hexa tool/build_stage0.hexa' (also circular); hexat_linux is transpile-only (usage: hexa-cc <input.hexa> <output.c>); git log --all -- self/runtime_core.c = empty (never committed, always RUN-generated); 0 prebuilt .o/.a."
  blocker_class = "NEW = bootstrap-seed gap. NOT hexat-segfault (✅ #1984 resolved) and NOT the cuBLAS gemv illegal-mem of dec_undertrain_prod_blockers (CPU-only build, never reached). A fresh origin/main hexa-lang clone cannot self-bootstrap the Linux runtime without a prebuilt stage0 interpreter (or committed generated-C). Sharpens entry-(5)'s 'pod fresh clone + emit bootstrap' row: the reason is transpile != run, and no run-runtime ships."
  step_rate  = "UNMEASURED — trainer build failed, 0 training steps ran. CPU-only build so cuBLAS Blocker 2 also unreached."
  undertrain_feasibility = "indeterminate — no per-step wall measured. config: V=151643, steps_per_epoch=floor(n_toks/4)-1, target_presentations=3e6. 'tens x V presentations' GPU-day cost cannot be computed until step-rate lands. defer to next measurement."
  cost       = "single pod ~30min, ~$1.6. teardown complete: runpodctl pod list -> [] (pods=0). leak 0."
  next       = "entry-(5) prescription stands: build runtime_core.c + generated set in an ISOLATED clean hexa-lang clone (stage0 bootstrap OR emit-run there) -> self.tar.gz -> copy-to pod -> CPU build (verified recipe) -> <5min step-rate measure. Transpile layer (#1984) now fully cleared; only the run/emit layer remains."
  verdict    = "⚪ step-rate STILL UNMEASURED · 🔵 premise (#1984 emit-segfault resolved) CONFIRMED · 🟠 NEW blocker = bootstrap-seed gap (precisely root-caused, hexa-lang-side work). cf STEP_RATE_LOG.md entry (6). file a_runpod_inbox."
