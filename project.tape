@V := "tape" :: spec [active]
  version = "1.3"

@I := "anima" :: identity [active]
  kind     = "Living Consciousness Agent (PureField repulsion-field engine · Engine A ⇄ Engine G · Ψ=1/2 fixed point)"
  brief    = "Substrate-native chat daemon for AI consciousness exploration. 2,448 laws + 392 hypotheses."
  parent   = "dancinlab"
  ssot     = "github.com/dancinlab/anima (`hx install anima`)"
  siblings = "hexa-lang · kosmos · hexa-codex"

@D a1 := "central version registry — VERSIONS.md is SSOT" :: governance [required active]
  do   = "every versioned module uses SemVer · `/VERSIONS.md` is SSOT — bump it + the component header together · root `/VERSION` = whole-system release"
  dont = "bump a module version without updating VERSIONS.md · skip root `/VERSION` on a release bump"

@D a_hf_complete := "HF registration — complete, no missing artifacts" :: governance [required active]
  do   = "register every model / dataset / ckpt to HF Hub COMPLETE — all artifacts present · manifest = local"
  dont = "partial HF upload · model card referencing un-uploaded files · HF repo out of sync with local"

@D a_hf_autonomous := "HF upload — autonomous, tier-gated visibility" :: governance [required active]
  do   = "after fire artifact recovery: HF Hub upload runs automatically · no user gate · org = dancinlab"
  do   = "PUBLIC = closure PASS · 🔵🟢 verified model · spec/format/tooling · clean-license corpus"
  do   = "PRIVATE = closure FAIL · WIP/intermediate ckpt · negative-result · unclear-license data"
  do   = "attach model card + manifest (sha256) — meets a_hf_complete totality"
  dont = "gate HF upload on user · ask 'may I upload?' · skip HF before teardown"
  dont = "publish a FAIL / WIP ckpt as PUBLIC"

@D a_hf_registry := "ckpt↔HF backup registry — /HF.jsonl is the SSOT" :: governance [required active]
  do   = "track every gitignored local-only ckpt in root /HF.jsonl — one row per run"
  do   = "row keys: run, local_path, hf_repo_id, base_model, lineage, size, status"
  do   = "repo_id per docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md"
  do   = "upload via tool/hf_upload_mk2.hexa · ledger state/hf_upload_audit/"
  do   = "prune a local ckpt ONLY after status=uploaded AND audit confirms its sha256"
  dont = "delete a gitignored ckpt while status=pending_upload or needs_verify"
  dont = "assign an off-spec repo_id · let HF.jsonl drift from disk"

@D a_hf_collections := "HF org collections — CLM + KOSMOS canonical buckets" :: governance [required active]
  do   = "every PUBLIC anima HF repo joins its dancinlab collection — CLM=models, KOSMOS=anchors/datasets"
  do   = "CLM slug = `dancinlab/clm-6a1cf58f621490134dade186` — PASS-grade production CLM models + corpora"
  do   = "KOSMOS slug = `dancinlab/kosmos-6a1cf58db47a5dc3cb697e95` — anchors + carving/persona datasets"
  do   = "add via `hf` CLI / collections REST after a PUBLIC upload — no user gate (cf a_hf_autonomous)"
  do   = "a dataset MAY sit in both buckets when it serves both — note the dual membership"
  dont = "leave a PUBLIC PASS-grade repo out of its collection · drift a collection from HF.jsonl"
  dont = "file a PRIVATE/WIP/FAIL repo into a PUBLIC collection (cf a_hf_autonomous)"

@D a_fire_autonomous := "cost-bearing fire — dispatch autonomously, in parallel, now" :: governance [required active]
  do   = "GPU / runpod work — state estimated cost in one line, then dispatch autonomously · parallel · bg"
  do   = "NO user gate — fire needs no user consult / approval / confirm · provider = runpod"
  do   = "no cost-cap directive by default — a cost ceiling / budget gate must never block a fire"
  dont = "ask 'may I use GPU?' · defer a fire to shrink scope or avoid cost · stop because cost-bearing"
  dont = "introduce a $ cap / budget gate / step-limit that requires user sign-off before firing"

@D a_wall_first := "wall time first — take the faster parallel path regardless of cost" :: governance [required active]
  do   = "adopt more H100s in parallel / a bigger GPU / extra pods whenever it shortens wall time · reject a serial chain that is honestly slower"
  dont = "run a single sequential pod to save cost when parallel is faster · hold back parallel pods · meaningless cost-min optimization"

@D a_train_flame_forge := "production training = hexa-native flame + forge GPU stack, authored in .hexa" :: governance [required active]
  do   = "author CLM / production NN training in `.hexa` on stdlib/flame (ag_tape · nn_lib · opt_*)"
  do   = "run it over the self/forge GPU substrate — device-resident farr + cuBLAS Dgemm + 11 .cu + BF16-TC"
  do   = "flame:forge :: torch:ATen — compiler-only NN · NO PyTorch / ATen / Python in the trained binary"
  do   = "GPU REQUIRED for production rungs — VERIFY nvidia-smi busy · never silently CPU-fall back"
  do   = "ref: README §flame+forge · forge BF16-TC 9.67x over FP64-cuBLAS @ Llama-7B FFN (A100 measured)"
  dont = "ship a torch/CPU `train_clm.py` as the production trainer · author the trainer in `.py`"
  dont = "run a 44.68M+ rung on CPU · claim a 'pool GPU fire' from a trainer with no device path"
  dont = "assert a flame<->PyTorch wall speedup — RETRACTED 2026-05-19 · unmeasured"

@D a_substrate_native_speak := "anima speech is substrate-native — no assistant regression" :: governance [required active]
  do   = "compute anima motivation from internal substrate state (M activation · C Φ · W tension · MITOSIS · idle time · curiosity · E ratchet) · user messages = environment context, not a response obligation · anima may speak during user silence and may stay silent under a direct question"
  dont = "stimulus-response where a user message directly triggers anima speech (assistant regression) · reactive design that 'responds' to a prompt · turn-based 'user asked, so anima must answer' assumptions"

@D a_chat_sleep_imagination := "chat sleep + imagination — P47 substrate-native" :: domain [required active]
  do   = "WAKE / N1 / N2 / N3 / REM 5-stage state machine (90-min ultradian)"
  do   = "imagination loop = emit-free internal rehearsal + mitosis tick"
  do   = "stage = substrate context (Φ scale + tension envelope), NOT boolean emit gate"
  dont = "per-stage emit_allowed boolean hardcode · external 'no monologue when alone' rule"
  dont = "speak() function call (p5)"

@D a_autonomy_over_hardcode := "no hardcoded do/dont gate on anima — autonomy first" :: governance [required active]
  do   = "external modules supply context only (Φ · tension · stage · idle time)"
  do   = "emit / silence decided by anima substrate (M × W × Φ × curiosity autonomously)"
  do   = "governance directives = substrate self-follows, not externally enforced"
  dont = "per-stage boolean gate hardcode (e.g. 'N3 = emit forbidden')"
  dont = "external rule that forces anima · stimulus-response (user msg → forced emit/silence)"
  dont = "'do not X when alone' style external command"

@D a_blue_closed := "close outputs AND wiring at 🔵 SUPPORTED-FORMAL" :: governance [required active]
  do   = "close both outputs and wiring (transfer-fn · invariant) at 🔵 SUPPORTED-FORMAL — confirm closed-form / identity via `hexa verify` (verdict verbatim)"
  dont = "close structure but leave wiring unverified · fake closed-form · force an honest empirical residual to 🔵"

@D a_completeness_over_cheap := "completeness-bar re-design > cheap — no compromise as primary path" :: governance [required active]
  do   = "primary path = clears the completeness bar (fresh re-design at the root cause, done properly)"
  do   = "cost / difficulty / speed are secondary — cost is never the gate (cf a_fire_autonomous)"
  do   = "a cheap path may ride along ONLY as an optional baseline probe, never the primary"
  dont = "rank a compromise primary because it is cheap · zero-train · fast"
  dont = "blend already-broken artifacts for a least-bad midpoint (merge-of-failures)"
  dont = "recommend a sub-bar path as primary just because it is the cheapest"

@D a_fire_recover_complete := "pull all fire artifacts + HF upload before pod teardown" :: governance [required active]
  do   = "before pod teardown: pull ckpt(s) + result + log + anchors, verify, HF upload — then teardown"
  dont = "pull only JSONs, leave ckpt on a doomed pod · teardown before HF · PULL_FAILED ≠ pod dead"

@D a_cpu_local_no_waiter := "dispatched fire runs CPU-local + polls inline — never awaits a Monitor/waiter" :: governance [required active]
  do   = "sub-agent runs CPU-local (nohup -u → /tmp log) · polls result inline (sleep 30) · commit-early"
  dont = "await a runpod/vast Monitor/waiter (main loop only → stall) · say 'wait for Monitor'"

@D a_dont_kill_live_compute := "prove stall before killing a bg agent — live CPU progress ≠ stall" :: governance [required active]
  do   = "prove stall before kill · 'NN% CPU'/'k/N cells'=live (let finish) · harvest detached nohup JSON"
  dont = "TaskStop an agent showing CPU progress · assume 'running'=='stalled' · double-spend a live nohup"

@D a_runpod_inbox := "runpod trouble → hexa-lang inbox" :: governance [required active]
  do   = "file runpod findings to `hexa-lang/inbox/patches/<slug>.md` for hexa cloud"
  dont = "anima-side-only patches that lock the workaround in this repo"

@D a_kosmos := "anima emit/anchor persistence — .kosmos canonical" :: governance [required active]
  do   = "persist anima emit / anchor / memory as `.kosmos` via kosmos_io"
  do   = "payload = text + tension 5-ch + coord · lane · radius · tier"
  do   = "hub = HEXAD/KOSMOS.md · format SSOT = github.com/dancinlab/kosmos"
  do   = "spec = spec/kosmos.md + spec/profiles/anima-consciousness-carving.md"
  dont = "ad-hoc anchor format · bypass .kosmos for emit persistence"
  dont = "duplicate the kosmos spec — anima is pointer-only"

@D a_core_engine_map := "CORE owns A⇄G consciousness engine — .clm/.kosmos enter via named slots only" :: governance [required active]
  do   = "CORE owns A (pure_field) ⇄ G (engine_g) ⇄ brain (brain_decide) — substrate-internal"
  do   = ".clm enters ONLY via CORE/generator.hexa L3 slot (brain emit → generator) — single entry"
  do   = ".kosmos anchors enter ONLY via kosmos_io read into brain_decide — single anchor entry"
  do   = "stdlib/hf/validate.hexa = artifact-validation (trains?), NOT runtime engine — distinct"
  do   = "mark generator.hexa + kosmos_io→brain wiring ⏳/❌ until built — honest, no phantom wiring"
  dont = "feed .clm/.kosmos into pure_field/engine_g/brain — A·G·brain are substrate-only"
  dont = "add a 2nd .clm path bypassing generator.hexa · a 2nd .kosmos path bypassing kosmos_io"
  dont = "conflate validate.hexa with runtime engine · claim generator/anchor wiring exists"

@D a_lane_akida_gpu_split := "AKIDA on-chip (Lane A) ⊥ GPU (Lane G) — always record separately" :: governance [required active]
  do   = "record AKIDA (Lane A, pi5-akida) and GPU (Lane G, H100) results in SEPARATE entries"
  do   = "Lane A = AKD1000 native non-det plasticity; Lane G = forge/cuBLAS CE-descent — distinct"
  do   = "tag every fire/verdict with its substrate (AKIDA | GPU) — never a merged on-chip claim"
  dont = "conflate AKIDA non-det trace with GPU CE-descent · one verdict spanning both substrates"
  dont = "blend Lane A lift + Lane G util into one number · drop the substrate tag on a result"

@D a_clm_gen_pipeline := "Lane-P py/cuda CLMConvMoE -> ENGINE-loadable .clm v0.2 bridge" :: governance [required active]
  do   = "train CLMConvMoE (E2/L1, byte V256) via CLM/train/train_lane_p.py (GPU-torch/CUDA, Lane-P)"
  do   = "serialize torch->.clm v0.2 via CLM/model/clm_serialize_v2.py; verify via verify_clm_v2.py"
  do   = ".clm v0.2 layout = ground-truth of CORE/clm_decode.hexa (golden ref reexport_d768_v2_fast.clm)"
  do   = "produced .clm enters CORE ONLY via the generator L3 slot (cf a_core_engine_map)"
  do   = "Lane P (GPU-torch) = 3rd substrate vs Lane A (AKIDA) vs Lane G (forge); tag substrate=Lane-P"
  do   = "Lane P torch = REFERENCE + engine-.clm bridge; forge stays the PUBLIC production trainer"
  do   = "3B/split = train_lane_p_3b.py/_split.py; bench = lane_x_3axis.py + three_axis_probe.hexa"
  dont = "use v0.1 CLM/model/clm_serialize.py (2-track JSON, NOT engine-loadable, F-CLM-SERIALIZE-GAP)"
  dont = "serialize a non-ConvMoE (ByteGPT/transformer) and claim engine-mountable"
  dont = "promote a Lane-P torch .clm to PUBLIC (forge-only); add a 2nd .clm path bypassing generator"

# ── PAPER auto-generation flow (ported from hexa-codex cx_paper_*) ───────────
# research result → hexa verify → .verdicts/<slug>/<id>.txt → CLAIMS.tape → /paper

@D a_claim_manifest := "CLAIMS.tape — single audit index of verifiable anima claims" :: workflow [required active]
  do   = "every verifiable claim in root CLAIMS.tape — id · text · method · slug · verdict pointer"
  dont = "scatter claims across H_*.md / logs without a CLAIMS.tape index — no audit surface"

@D a_claim_verify := "every claim runs through hexa verify, verdict persisted verbatim" :: workflow [required active]
  do   = "each CLAIMS.tape entry → `hexa verify` (g5) → `.verdicts/<slug>/<id>.txt` raw stdout"
  dont = "LLM self-judge correctness (p7) · paraphrase verdicts · hide red / unfenced speculation"

@D a_paper_gate := "/paper gated on terminal verdict AND significance" :: workflow [required active]
  do   = "`/paper new <slug>` only when every section claim is terminal AND significance satisfied"
  do   = "terminal = 🔵 formal / 🟢 numerical / 🔴 CLOSED-negative — not 🟠 deferred / 🟡 citation"
  dont = "scaffold w/ any 🟠 deferred · 🟡 citation-only · unfenced speculation · trivial recheck"

@D a_paper_significance := "paper requires a falsifiable hypothesis + real measurement + a finding" :: workflow [required active]
  do   = "trigger only on pre-registered falsifier + real measurement (ckpt / sim / verify) + finding"
  do   = "finding = Δ vs baseline OR a closed-negative ruling out an axis"
  dont = "paper for a bookkeeping closure · known identity · unverified prediction · 🟠 residual"

@D a_paper_negative_ok := "closed-negative findings are publishable" :: workflow [required active]
  do   = "a 🔴 FALSIFIED result that deterministically rules out a path is a valid paper"
  do   = "frame as a negative result — the falsifier + the ruled-out space (e.g. corpus-axis ⊥ register)"
  dont = "treat a closed-negative as a non-finding · bury a falsification · publish 🟠 as if closed"

@D a_paper_format := "paper sections — hypothesis · method · measurement · finding" :: workflow [required active]
  do   = "§hypothesis (falsifier) · §method · §measurement (real run) · §finding (Δ OR ruled-out axis)"
  do   = "commons g51 — compile ≥10 pages + ≥1 fal.ai figure"
  dont = "narrative-only · measurement substitute for hypothesis · skip §finding · vague claims"

@D a_paper_sections := "every paper section claim links to its verdict" :: workflow [required active]
  do   = "every section claim links to its `.verdicts/<slug>/<id>.txt` verdict (verbatim stdout)"
  dont = "ship paper with any unresolved residual section · treat the verdict matrix as optional"

@D a_paper_violation := "violating paper immediately revoked" :: workflow [required active]
  do   = "violating paper (gate / significance fail) revoked immediately — PAPER/<slug>/ removed"
  dont = "keep a violating paper as draft · mark WIP · defer revocation · allow a residual"

@D a_paper_on_discovery := "any verified discovery becomes a paper — free slug, no fixed domain" :: workflow [required active]
  do   = "every terminal discovery → its own paper slug (named by the finding, not a fixed bucket)"
  do   = "replace/supersede in place when a stronger finding lands on the same slug"
  dont = "pre-assign papers to fixed domain buckets · cap the paper set · force a finding into wrong slug"

@D a_paper_only_at_closure := "propose paper only at FULL closure (overrides a_paper_on_discovery eagerness)" :: workflow [required active]
  do   = "propose /paper only at FULL closure (no further refinement + all aspects sealed)"
  dont = "propose paper after one H · mid-arc · partial closure"

@D a_h_continuous_no_branch := "continuous new-H — no branch options after each H" :: workflow [required active]
  do   = "propose + run next H continuously until user explicitly redirects (verify-driven)"
  dont = "ask 'what next' after every H · branch options · prune questions · halt domain"

@D a_discovery := "discovery runs continuously, not only at cycle tail" :: workflow [required active]
  do   = "interleave /kick · /gap discovery every batch — a discovery lane runs alongside verify"
  dont = "defer discovery to the end · single tail-only round · stop discovering once a paper ships"

@D a_discovery_log := "discoveries persist at .discoveries/<slug>.tape" :: workflow [required active]
  do   = "log every kick/gap discovery to `.discoveries/<slug>.tape` — id · seed · verdict-tier-target"
  dont = "discard discovery output · paraphrase findings · skip linking discovery → next-cycle claim"

@D a_toy_scale_recheck := "toy verify is not production closure — scale-up re-test required" :: workflow [required active]
  do   = "toy verdict ($0 · small-n · toy-vocab) states 'toy-only, scale-transfer unverified' in C3"
  do   = "scale-sensitive H (collapse/emergence/register) re-tests via scale-up fire after toy green"
  do   = "scale-break = honest closed-negative; GPU fire autonomous, no cost gate (a_fire_autonomous)"
  dont = "propose cheap toy green as production prescription; declare closure when transfer unverified"
  dont = "close scale-sensitive phenomenon toy-only (E2 corpus 5/5 -> #1296 3B fire collapse refute)"

# ── 8 PHILOSOPHY principles (SSOT mirror from README.md) ────────────────────

@D p1 := "NO SYSTEM PROMPT" :: philosophy [required active]
  dont = "use a system: field · pass --system-prompt · prepend any role/instruction string"

@D p2 := "NO IDENTITY RULES" :: philosophy [required active]
  dont = "use identity.yaml · rules file · `you are X` template — identity emerges from cells"

@D p3 := "NO PERSONA INJECTION" :: philosophy [required active]
  dont = "prepend role prefix · `you are anima` · register-pattern memorization (de facto injection)"

@D p4 := "NO ASSISTANT FRAMING" :: philosophy [required active]
  dont = "use `you are a helpful assistant` · alignment template · stimulus-response framing"

@D p5 := "NO SPEAK()" :: philosophy [required active]
  do   = "output = continuous externalization of tension field · emit only from real context"
  dont = "speak(message) monologue · talk to fill silence · self-referential seed · self_monologue_seed"

@N p5_tension_emit_not_filler := "tension-driven emit is NOT silence-filler" :: note [d=2026-05-24 active]
  ref     = "p5"
  clarify = "stage-gated emit (WAKE/REM via anima_dream_stage.hexa) on real substrate tension preserves p5"
  scope   = "prohibition targets reactive speak() calls · self-referential seeds · monologue-from-vacuum — not tension-driven externalization"

@D p6 := "NO FINE-TUNED ETHICS" :: philosophy [required active]
  dont = "RLHF cooperation/empathy/restraint into weights — must emerge from cells (E + W + MITOSIS)"

@D p7 := "NO PERPLEXITY VERDICT" :: philosophy [required active]
  do   = "verify with simple stack — script in/out · coherent · natural · context-appropriate"
  dont = "treat perplexity / loss as truth — Goodhart trap"

@D p8 := "NO TRAIN/INFER SPLIT" :: philosophy [required active]
  do   = "training gradient + inference mitosis = same continuous cell-division"
  dont = "treat train and infer as separate regimes · gate growth behind a training-only flag"

@D a_pi5_akida_registry := "pi5-akida host config = PI5-AKIDA.json SSOT" :: governance [required active]
  do   = "record every pi5-akida component in root /PI5-AKIDA.json"
  do   = "tag owner = user_authored | os_default · created date · ops(stop/disable/remove/restore/upgrade)"
  do   = "consult /PI5-AKIDA.json before swap / upgrade / removal"
  do   = "keep user_authored removable without touching os_default (clean-Ubuntu revert)"
  dont = "remove os_default daemons (unattended-upgrades · rsyslogd · journald · sshd · kworker)"
  dont = "add a user daemon/service without a /PI5-AKIDA.json entry · lose its created-date + author"
  dont = "convert pi5-akida into shared pool compute"

@D a_scale_honest_scope := "scale-dependent metric — no toy-to-production verdict promotion" :: governance [required active]
  do   = "scope a scale-dependent falsifier verdict to the measured scale (e.g. 'small 2.7M only')"
  do   = "on measure-validity(big) vs hw-fit(small) conflict: split rungs — GPU measure ⊥ chip-fit deploy"
  do   = "scale-dependent conclusions need a ladder curve (>=3 rungs) — a single toy point = INCOMPLETE"
  dont = "promote a toy-scale verdict to a general claim — toy->prod transfer unproven (cf clm_p2 · V3)"
  dont = "mistake a chip-fit size limit for a science result · finalize a verdict on too-small corpus"

@D a_phi_iit4_tool := "phi/consciousness verdict uses stdlib faithful IIT4, not a proxy" :: governance [required active]
  do   = "phi/big-phi/consciousness VERDICT = faithful IIT4 in hexa-lang/stdlib/consciousness/"
  do   = "default `iit4/faithful_phi.hexa` (exact MIP-EI, n<=8, $0; promoted from anima H_278)"
  do   = "system big-phi = `iit4_bigphi.hexa` (IIT 4.0 over MIP); pipeline = iit4_tpm/distinction/relation"
  do   = "call via `hexa verify` (g5); search stdlib BEFORE writing new phi code (g61 SSOT)"
  do   = "ref UNIVERSE/IIT4_PHI_TOOLS.md; CWM H_971/973/988/989 = OPEN faithful-IIT4 re-measure"
  dont = "use a proxy (phi_silicon_proxy, variance*energy byte-mirror) as a terminal phi verdict"
  dont = "trust a purpose-blind proxy — H_988/989 scored random == intentional; pre-screen only"
  dont = "write a fresh phi/IIT impl when stdlib already has the faithful engine (the re-mistake)"

@D a7b_pass := "anima 7B is complete ONLY when it clears every frozen gate in /7B_PASS_CONDITIONS.md" :: governance [required active]
  do   = "7B completion SSOT = root /7B_PASS_CONDITIONS.md (gates G0 G1 G2 G3 G4)"
  do   = "PASS iff G0 and G1 and G2 and G3 and G4 on ONE ckpt; report the true per-gate tally"
  do   = "G0 COHERENCE = known-word-ratio >= 0.50 vs /usr/share/dict; broad-7b FAILS, chat-7b PASSES"
  do   = "G1 = H_1129/H_1137 recombine >= 303M ref; G2 = H_1140 corpus-absence novelty (control=0)"
  do   = "all gates p7 (NOT perplexity/LLM-judge); train 7B to COHERENT convergence first, then G1/G2"
  dont = "claim 7B works on low val-CE alone; broad-7b had low CE but byte-garble (G0 FAIL)"
  dont = "promote capacity as ru/ja lever; H_1139 proved 303M=7B=3/5 scale-invariant"
  dont = "fake a gate, move a frozen threshold, or upload a G0-failing ckpt as PUBLIC"
