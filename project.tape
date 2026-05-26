@V := "tape" :: spec [active]
  version = "1.2"

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

@D a_fire_autonomous := "cost-bearing fire — dispatch autonomously, in parallel, now" :: governance [required active]
  do   = "GPU / runpod work — state estimated cost in one line, then dispatch autonomously · parallel · bg"
  do   = "NO user gate — fire needs no user consult / approval / confirm · provider = runpod"
  do   = "no cost-cap directive by default — a cost ceiling / budget gate must never block a fire"
  dont = "ask 'may I use GPU?' · defer a fire to shrink scope or avoid cost · stop because cost-bearing"
  dont = "introduce a $ cap / budget gate / step-limit that requires user sign-off before firing"

@D a_wall_first := "wall time first — take the faster parallel path regardless of cost" :: governance [required active]
  do   = "adopt more H100s in parallel / a bigger GPU / extra pods whenever it shortens wall time · reject a serial chain that is honestly slower"
  dont = "run a single sequential pod to save cost when parallel is faster · hold back parallel pods · meaningless cost-min optimization"

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

@D a_fire_recover_complete := "pull all fire artifacts + HF upload before pod teardown" :: governance [required active]
  do   = "before pod teardown: pull ckpt(s) + result + log + anchors, verify, HF upload — then teardown"
  dont = "pull only JSONs, leave ckpt on a doomed pod · teardown before HF · PULL_FAILED ≠ pod dead"

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
