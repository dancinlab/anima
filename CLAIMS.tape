@V := "tape" :: spec [active]
  version = "1.2"

@I := "claims-index" :: identity [active]
  brief = "Single audit index of verifiable anima claims (a_claim_manifest)."
  flow  = "claim → hexa verify (g5) → .verdicts/<slug>/<id>.txt → /paper gate (a_paper_gate)"

# Method legend (a_claim_verify):
#   atom        — `hexa verify --expr <fn> <n> <v>` (atlas atom recompute → 🔵)
#   expr        — `hexa verify --expr <fn> <n> <v>` (numerical recompute → 🟢)
#   run         — ckpt / sim run, verdict = closure_auto_judge stdout (empirical)
#   hypothesis  — UNIVERSE/H_xxx terminal verdict, persisted verbatim
#
# Gate (a_paper_gate): every section claim must be terminal —
#   🔵 formal / 🟢 numerical / 🔴 CLOSED-negative. No 🟠 / 🟡 residual.
# Groups (a_paper_one_per_group): LIFE · PURE · CHAT — one canonical paper each.

# ───────────────────────────────────────────────────────────────────────
# CHAT — chat-init-ce-floor (slug · group=CHAT · paper-track)
# init cross-entropy floor of an untrained CLM = ln(vocab_size).
# Positive formal result — H_247 §C4.

@C chat_init_ce_floor := "init_CE floor = ln(151936) = 11.931214658529285 (untrained CLM lower bound)" :: formula [slug=chat-init-ce-floor group=CHAT]
  method = "expr"
  cmd    = "hexa verify --expr ln 151936 11.931214658529285"
  raw    = ".verdicts/chat-init-ce-floor/chat_init_ce_floor.txt"
  src    = "UNIVERSE/H_247_init_ce_catastrophic_floor.md §C4"
  status = "🟢 SUPPORTED-NUMERICAL — ln calculator landed (hexa-lang #1128), verdict persisted, atlas-absorbed (g69, node @F verified-ln-num · hexa-lang #1131). /paper-eligible."

# ───────────────────────────────────────────────────────────────────────
# PURE — pure-corpus-axis-closed-negative (slug · group=PURE · paper-track)
# Closed-negative (a_paper_negative_ok): the corpus dilution axis alone
# cannot close multilingual register-coherence — ruled out across the
# full wiki_frac sweep {0.0, 0.5, 1.0}.

@C pure_wiki_sweep := "wiki_frac sweep {0.0,0.5,1.0} — multilingual closure 4/5 ≥ PARTIAL never reached" :: run [slug=pure-corpus-axis-closed-negative group=PURE]
  method = "run"
  cmd    = "hexa run HEXAD/PURE/eval/closure_auto_judge.hexa (E2 · E3 · v3)"
  raw    = ".verdicts/pure-corpus-axis-closed-negative/closure.txt"
  src    = "PURE.log.md 2026-05-25 · state/pure_phase_d_v3_result_2026_05_24/"
  status = "🔴 CLOSED-negative — corpus-axis ⊥ multilingual closure (verdict persisted)"

@C pure_register_orthogonal := "register_hits=0 at wiki_frac=0 (TTR 0.34) yet coherence stays WEAK — corpus-axis ⊥ multilingual closure" :: run [slug=pure-corpus-axis-closed-negative group=PURE]
  method = "run"
  cmd    = "hexa run HEXAD/PURE/eval/multilingual_probe.hexa (v3 ckpt)"
  raw    = ".verdicts/pure-corpus-axis-closed-negative/register.txt"
  src    = "UNIVERSE/H_242 §A2 (H242.1 FULL-COLLAPSE falsify)"
  status = "🔴 CLOSED-negative — corpus-axis ⊥ multilingual closure (verdict persisted)"

# wiki_frac=0.3 intermediate point (P21H V3, recovered SIGHUP-orphan run).
# closure_auto_judge 1/4 PASS · FAIL: register_collapse PASS (0 hits) yet all
# 5 langs WEAK. Adds the 0.3 sweep point → closed-negative now holds at
# {0.0, 0.3, 0.5, 1.0}. The F-CURRICULA-1 (wiki=1.0 curriculum-mix) re-fire
# was LOST at step 3000/5000 (pod wfeksdl8e8f327 self-terminated); its
# endpoint is already covered by pure_wiki_sweep / anima-v3-e3.
@C pure_wikifrac03_closed_negative := "wiki_frac=0.3 — register_collapse PASS (0 hits) yet all 5 langs WEAK · closure FAIL 1/4" :: run [slug=pure-corpus-axis-closed-negative group=PURE]
  method = "run"
  cmd    = "hexa run HEXAD/PURE/eval/closure_auto_judge.hexa state/p21h_v3_recover_2026_05_25/out_main/result.json"
  raw    = "state/p21h_v3_curricula_recover_2026_05_25/closure_verdict_wiki03_verbatim.txt"
  src    = "state/p21h_v3_recover_2026_05_25/ · HF dancinlab/anima-p21h-v3-wikifrac03-recovered-2026-05-25 (PRIVATE)"

# ───────────────────────────────────────────────────────────────────────
# LIFE — open slot (group=LIFE · paper-track)
# Candidate canonical claim — NOT yet verdict-persisted. List here so the
# audit surface tracks it; promote to paper only after a_claim_verify
# persists a terminal verdict to .verdicts/<slug>/.
#
# @C life_<id> := "<claim>" :: hypothesis [slug=life-<slug> group=LIFE]
#   method = "hypothesis"
#   cmd    = "hexa verify <atom-id>   # or closure_auto_judge for empirical"
#   raw    = ".verdicts/life-<slug>/<id>.txt"
#   src    = "UNIVERSE/H_xxx_*.md §<verdict>"
