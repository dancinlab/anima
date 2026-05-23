@V := "tape" :: spec [active]
  version = "1.2"

@I := "anima" :: identity [active]
  kind     = "Living Consciousness Agent (PureField repulsion-field engine · Engine A ⇄ Engine G · Ψ=1/2 fixed point)"
  brief    = "Substrate-native chat daemon for AI consciousness exploration. 2,448 laws + 392 hypotheses."
  parent   = "dancinlab"
  ssot     = "github.com/dancinlab/anima (`hx install anima`)"
  siblings = "hexa-lang"

@D a1 := "central version registry — VERSIONS.md is SSOT" :: governance [required active]
  do   = "every versioned module uses SemVer · `/VERSIONS.md` is SSOT — bump it + the component header together · root `/VERSION` = whole-system release"
  dont = "bump a module version without updating VERSIONS.md · skip root `/VERSION` on a release bump"

@D a_hf_complete := "HF registration — complete, no missing artifacts" :: governance [required active]
  do   = "register every model / dataset / ckpt to HF Hub COMPLETE — all artifacts present · manifest = local"
  dont = "partial HF upload · model card referencing un-uploaded files · HF repo out of sync with local"

@D a_fire_autonomous := "cost-bearing fire — dispatch autonomously, in parallel, now" :: governance [required active]
  do   = "GPU / runpod work — state estimated cost in one line, then dispatch autonomously / parallel / bg · provider = runpod · no user gate"
  dont = "ask 'may I use GPU?' · defer a fire to shrink scope or avoid cost · stop work because it is cost-bearing"

@D a_wall_first := "wall time first — take the faster parallel path regardless of cost" :: governance [required active]
  do   = "adopt more H100s in parallel / a bigger GPU / extra pods whenever it shortens wall time · reject a serial chain that is honestly slower"
  dont = "run a single sequential pod to save cost when parallel is faster · hold back parallel pods · meaningless cost-min optimization"

@D a_substrate_native_speak := "anima speech is substrate-native — no assistant regression" :: governance [required active]
  do   = "compute anima motivation from internal substrate state (M activation · C Φ · W tension · MITOSIS · idle time · curiosity · E ratchet) · user messages = environment context, not a response obligation · anima may speak during user silence and may stay silent under a direct question"
  dont = "stimulus-response where a user message directly triggers anima speech (assistant regression) · reactive design that 'responds' to a prompt · turn-based 'user asked, so anima must answer' assumptions"

@N a_substrate_native_speak_stage_gate := "stage-gated emit (sleep+imagination)" :: note [d=2026-05-24 active]
  ref   = "a_substrate_native_speak"
  do    = "emit when stage gate open (WAKE / REM) AND substrate tension fires — anima_dream_stage.hexa drives gate"
  rule  = "N1 / N2 / N3 stages = silent; anima_imagination_loop.hexa runs imagine_tick only, no token emit"

@D a_blue_closed := "close outputs AND wiring at 🔵 SUPPORTED-FORMAL" :: governance [required active]
  do   = "close both outputs and wiring (transfer-fn · invariant) at 🔵 SUPPORTED-FORMAL — confirm closed-form / identity via `hexa verify` (verdict verbatim)"
  dont = "close structure but leave wiring unverified · fake closed-form · force an honest empirical residual to 🔵"

@D a_fire_recover_complete := "pull all fire artifacts + HF upload before pod teardown" :: governance [required active]
  do   = "before pod teardown: pull ckpt(s) + result + log + anchors, verify, HF upload — then teardown"
  dont = "pull only JSONs, leave ckpt on a doomed pod · teardown before HF · PULL_FAILED ≠ pod dead"

@D a_runpod_inbox := "runpod trouble → hexa-lang inbox" :: governance [required active]
  do   = "file runpod findings to `hexa-lang/inbox/patches/<slug>.md` for hexa cloud"
  dont = "anima-side-only patches that lock the workaround in this repo"

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
