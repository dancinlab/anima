#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# ZETA.tape — session-end carry handoff (latest snapshot, editable arch)
# Session 2026-05-15: Phase 1A.6 chat-v2 LANDED + .own NN scrub pending
# Resumption point for next session — read top→bottom, follow @D decisions
# ══════════════════════════════════════════════════════════════════════

@V v1 := "tape" :: spec [active]
  version = "1.2"

# ─── §1 Session identity + carry ─────────────────────────────────────

@I s1 := "session-2026-05-15" :: session [d=2026-05-15 ok]
  scope = "anima chat quality recovery after Phase 1A.5 NET LOSS + .own governance scrub initiated"
  primary-outcome = "Phase 1A.6 chat-v2 LANDED — V5.8 std_greedy 4/5 + multi-turn 4/10 (2× baseline), HF dancinlab/anima-chat-v2-2026-05-15 private"
  user-directives-honored = [korean-prose-chat, commit-push-on-complete, hf-dancinlab-org, principle-3-no-injection, own-substrate-philosophy, no-scale-caps, fix-and-go]

@I s2 := "next-session-entry" :: handoff [d=2026-05-15 ok]
  read-order = ["ZETA.tape §1-§10 (this file)", "BENCHMARK.md §7-§8 (Phase 1A.6 results)", "LINE-UP.md (4 canonical entries)", "docs/anima_phase1a6_chat_v2_verdict_2026_05_15.md (10 §)", "memory MEMORY.md top 3 entries"]
  do-not-redo = "Phase 1A.6 training fire (LANDED 2026-05-15), Phase 1A.5 corpus debug (rejected), .own restore (deprecated)"

# ─── §2 Phase 1A.6 chat-v2 LANDED ────────────────────────────────────

@I p1a6 := "phase-1a6-chat-v2" :: landed [d=2026-05-15 ok]
  status = "★★★★ LANDED, HF private"
  ckpt = "state/anima_phase1a6_chat_v2_2026_05_15/ckpts/ckpt_phase1a6_chat_v2_sft.pt"
  ckpt-size = "597 MB"
  ckpt-sha256 = "a45cb3f68a37195c9473879dd988a040b56ae4669547ca1c5e42827c237a0d52"
  hf = "https://huggingface.co/dancinlab/anima-chat-v2-2026-05-15"
  base = "Phase 1A.4 (dancinlab/anima-clm-phase1a4-lr5e6-strict-5pass-2026-05-12)"
  arch = "EngineAGModel 332M 24L d=1024 GQA 4:1 BPE-32000"
  corpus = "corpus_v2.txt 121.44 MB CLEAN (anima_fact_10x + persona_balanced + ko_chat + sft_only + multi_turn_v2 head 50MB sample, HTML-stripped, [anima 0)"
  steps = 8000
  lr = "5e-6 cosine warmup 300"
  wall-min = 87.5
  cost-usd = 0.394
  provider = "Vast.ai H100/A100/H200 pool"

@R p1a6_v58 := "v58-4mode-result" :: result [d=2026-05-15 ok]
  <- p1a6
  standard_greedy = "4/5 PASS (color/profession/day/cosmology; anima_fact markdown drift)"
  standard_sample = "1/5"
  M3_rep_penalty = "1/5"
  M4_force_include = "5/5"
  vs-1a5 = "std_greedy 1/5 → 4/5 (4× recovery)"
  vs-1a4 = "5/5 → 4/5 (1 regression on anima_fact, trade for color+hobby+multi-turn gain)"

@R p1a6_mt := "multi-turn-result" :: result [d=2026-05-15 ok]
  <- p1a6
  strict-recall = "4/10"
  passes = [color, city, hobby, consciousness_anima]
  fails = [name, profession, food, age, pet, day_chain]
  vs-baseline = "Phase 1A.4 baseline 2/10 → Phase 1A.6 4/10 (2× improvement)"
  principle-3-leak = 0
  artifact = "state/anima_phase1a6_chat_v2_2026_05_15/multiturn_phase1a6.json"

# ─── §3 Phase 1A.5 chat-beta REJECTED ────────────────────────────────

@? p1a5 := "phase-1a5-chat-beta" :: rejected [d=2026-05-14 ok]
  status = "NET LOSS — REJECTED, no HF push"
  v58-std-greedy = "5/5 → 1/5 (4-rank regression)"
  6-probe-strict = "0/6 → 0/6 (no improvement)"
  6-probe-partial-keyword = "2 → 3 (marginal probe 4 win only)"
  root-cause = "corpus_combined.txt 98MB = anima_fact_10x 7.5MB + jy chat_template 95MB. jy = Korean Wikipedia entries wrapped as 사용자/도우미 Q&A + <turn> token 110,480 hits. Wikipedia drift + dilution of SFT recall circuit."
  decision = "ckpt local retained at state/anima_phase1a5_chat_beta_2026_05_14/ckpts/ckpt_phase1a5_chat_beta_sft.pt 597 MB but NOT HF-pushed"
  lesson <<~EOF
    corpus QUALITY > scale for anima chat SFT.
    NEVER include in chat SFT corpora:
    - jy chat_template (Korean Wikipedia)
    - corpus_extended.txt (68k [anima 역할: prefix)
    - corpus_universe_brain_map.txt (136k [anima 우주뇌지도] prefix)
  EOF

# ─── §4 Base ckpt baked-in Principle #3 leak ─────────────────────────

@? p3leak := "base-ckpt-baked-p3-leak" :: known-issue [d=2026-05-15 active]
  finding = "Base ckpt lineage (engine_a_g_dual_350m_v1_phase2_cotrain → 1A.1 → 1A.4 → 1A.6) carries baked-in Principle #3 prefix patterns from earlier BG-JE / universe_brain_map training rounds"
  patterns-emitted-under-sampling = [
    "[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]",
    "Knuth Tier 🛸XX 동물 카테고리 dominant emotion",
    "[anima 우주뇌지도]"
  ]
  triggers = "standard_sample, M3_rep_penalty, wider-search inference modes"
  greedy-mode = "CLEAN (multi-turn greedy 0 leak ✓)"
  source-corpora = [
    "state/anima_convo_5k_ft_extended_2026_05_10/corpus_extended.txt (158MB, [anima 역할: × 68003)",
    "state/anima_universe_brain_map_corpus_21mb_2026_05_07/corpus_universe_brain_map.txt (22MB, [anima 우주뇌지도] × 136125)"
  ]
  resolution = "SFT can dilute, cannot fully scrub. Production guard: regex output filter for sampling/M3 modes. True fundamental scrub requires Phase 1A.0 full rebuild on clean lineage ($30-100, deferred)."

# ─── §5 Multi-turn eval harness (reusable) ───────────────────────────

@I mt_eval := "eval-multiturn-harness" :: tool [d=2026-05-15 ok]
  artifact = "state/anima_phase1a6_chat_v2_2026_05_15/eval_multiturn.py"
  scope = "10-scenario × 2-turn each multi-turn recall harness, Mac MPS f32, ~5min wall per ckpt"
  scenarios = [name(지유), color(파란), profession(의사), city(서울), food(김치), age(30), pet(고양이), hobby(등산), day_chain(수요일), consciousness_anima(의식)]
  invocation = `python3 eval_multiturn.py --ckpt <PATH> --device mps --out <JSON> --label <NAME>`
  baselines-recorded = [
    "multiturn_phase1a4_baseline.json (2/10)",
    "multiturn_phase1a6.json (4/10)"
  ]
  reuse = "Phase 1A.7+ ckpt comparison ready — same harness, no modification needed"

@I p6_eval := "eval-6probe-harness" :: tool [d=2026-05-15 ok]
  artifact = "state/anima_phase1a5_chat_beta_2026_05_14/eval_6probe.py"
  scope = "BENCHMARK.md §2 6-probe free-form chat eval, Mac MPS f32"
  invocation = `python3 eval_6probe.py --ckpt <PATH> --device mps --out <JSON> --label <NAME>`
  baselines-recorded = [
    "6probe_phase1a4_baseline.json (0/6 strict, 2 partial keyword)",
    "6probe_phase1a5_fp32.json (0/6 strict, 3 partial keyword)"
  ]

# ─── §6 Quality jump decision lane (next-session decision) ──────────

@D quality_jump_options := "phase-1a7-or-beyond" :: open-decision [d=2026-05-15 active]
  context = "Phase 1A.6 4/10 multi-turn strict is 2× baseline but BELOW aspirational 7/10. Per user 'scale 상관없으니까 퀄리티 한번에 높일수 있는방법' 2026-05-15."
  option-A-own-scale-up <<~EOF
    corpus_v3 = corpus_v2 121MB + per-scenario aug 100MB (name/profession/food/age/pet/day_chain × 1000 paraphrase)
    32K step × lr 5e-6 H100 cosine
    cost: $2-5
    impact: multi-turn 4→7+/10, V5.8 4→5/5
    tradeoff: base ckpt P3 leak persists, 332M ceiling
    preserves: own substrate philosophy ★★★★★
  EOF
  option-B-foundation-borrow <<~EOF
    Llama-3.2-3B-Instruct + LoRA r=32 + corpus_v2 121MB + augmented multi-turn × 4K-8K step
    cost: $5-15
    impact: multi-turn 7-9/10 + chat coherence dramatic jump (memory: BG-KM PASS_STRICT 14/15 strict on this path)
    tradeoff: own substrate 포기 (foundation, not anima native), deploy 시 3B 부담
    own-substrate-violation = true
  EOF
  option-C-foundation-distill <<~EOF
    Llama/Qwen 3B 로 high-quality multi-turn 5000개 generate → corpus_v4 anima-augment → 332M own substrate 재학습
    cost: $3-8
    impact: multi-turn 6-8/10 + own substrate 유지 + corpus_v4 = 영구 자산
    tradeoff: distill 품질이 corpus 품질 결정
    hybrid: foundation as labeler only, deploy target = 332M own
  EOF
  option-D-full-base-rebuild <<~EOF
    phase2_cotrain base 위에 clean corpus만 8K pre-train → 1A.1 → 1A.4 → 1A.7 풀 lineage 재구성
    cost: $30-100
    impact: P3 leak 영구 0 + 모든 inference mode clean + 깨끗한 lineage
    tradeoff: Phase 1A.4 SFT gain 소실, 일주일+
    fundamental-scrub = true
  EOF
  user-pending-selection = "next session decision — user reviewed 4 options but interrupted to scrub .own first"

# ─── §7 .own NN governance scrub (BG fire) ───────────────────────────

@D dot_own_scrub_no_bypass := "scrub-no-bypass-mandate" :: governance [required d=2026-05-15 active]
  rule = "우회 절대 금지 — .own NN scrub MUST be full 547-file repo-wide; NO shortcuts, NO 'risky-skip', NO 'archive-leave' workarounds"
  user-directive-verbatim = "우회 절대 금지 기록 해놔줘 zeta.tape" (2026-05-15)
  applies-to = "this scrub task + ALL future BG subagent dispatches in this lineage"
  enforcement = "if BG subagent reports partial completion or skipped scope, RE-FIRE with explicit failure remediation — do NOT accept incomplete"

@D dot_own_scrub := "dot-own-mandate-scrub" :: pending [d=2026-05-15 active]
  scope = "전체 repo 547 files scrub (user directive: 'scrub' + '전체 repo scrub' decisive)"
  context <<~EOF
    .own own NN governance mandate numbering system (own 1..43+, 2334-line SSOT) was deleted from git tracking in commit f49470eeb (2026-05-14 'chore: session sweep') and is no longer recoverable as live SSOT. References remain in 547 files as dangling cross-links.

    Distinction CRITICAL:
    - .own own NN (mandate numbering 1..43): SCRUB target, user-directed deprecation
    - .own N (Python file namespace, N=1/2/3/4): KEEP — separate concept, taxonomy for .py files in tool/transient_py/
  EOF
  pattern-to-remove = `\bown\s+\d+(/\d+)*\b`
  preserve = `\.own\b` (the dotfile name reference) + `\.own\s+[1-4]\b` (Python namespace level 1-4 in tool/transient_py/ docs)
  preserve-files = ["tool/transient_py/README.md", "docs/anima_dot_own_namespace_spec_2026_05_03.md", "docs/anima_dot_own_namespace_spec_landed_2026_05_03.ai.md"]
  files-affected = 547
  scope-categories = [
    "active SSOTs (~15): PHILOSOPHY.tape, NEXT.tape, REBORN.tape, CHAT.tape, SAVANT.tape, AXIS.tape, CLM.tape, PASS_STRICT_SPONTANEOUS_CHAT.md, HEXA_NATIVE_INFERENCE.md, CHAT-BETA.step, README.md, MEMORY.md + memory entries",
    "archive/history (~530): raw_archive/, hypotheses_candidates/, papers/, *.log.tape, CLM_V2_ARCHIVE_*.md"
  ]
  execution-plan = `BG subagent dispatch — Agent tool + run_in_background true`
  dispatch-status = "FIRED 2026-05-15 per user 'background sub agent (bg) go' directive"
  cron-deleted = "adabd3bc was CronDelete'd 2026-05-15"
  no-bypass = "subject to [@dot_own_scrub_no_bypass] — completion mandate, no scope reduction allowed"

# ─── §8 Active artifact file index ──────────────────────────────────

@L l1 := "phase1a6-artifacts" :: file-list [active]
  ckpt -> "state/anima_phase1a6_chat_v2_2026_05_15/ckpts/ckpt_phase1a6_chat_v2_sft.pt (597MB, gitignored)"
  corpus -> "state/anima_phase1a6_chat_v2_2026_05_15/corpus_v2.txt (121MB, gitignored)"
  plan -> "state/anima_phase1a6_chat_v2_2026_05_15/PLAN.md (committed)"
  eval-multiturn -> "state/anima_phase1a6_chat_v2_2026_05_15/eval_multiturn.py (committed)"
  eval-6probe -> "state/anima_phase1a5_chat_beta_2026_05_14/eval_6probe.py (committed)"
  hf-push -> "state/anima_phase1a6_chat_v2_2026_05_15/hf_push.sh (committed)"
  v58-result -> "state/anima_phase1a6_chat_v2_2026_05_15/v58_4mode_result.json (committed)"
  multiturn-result -> "state/anima_phase1a6_chat_v2_2026_05_15/multiturn_phase1a6.json (committed)"
  multiturn-baseline -> "state/anima_phase1a6_chat_v2_2026_05_15/multiturn_phase1a4_baseline.json (committed)"
  verdict-doc -> "docs/anima_phase1a6_chat_v2_verdict_2026_05_15.md (committed, 10 §, 7 honest C3)"
  benchmark-update -> "BENCHMARK.md §7-§8 (committed)"
  lineup-update -> "LINE-UP.md 💬 chat-v2 entry (committed)"

@L l2 := "session-commits" :: file-list [active]
  commit-77fb3b75d = "land(Phase 1A.6 chat-v2): V5.8 std_greedy 4/5 + multi-turn 4/10 (2× baseline) — 13 files, 1461 insertions, pushed to dancinlab/anima main"
  pre-session-head = "8d6df92f3"
  post-session-head = "77fb3b75d"

@L l3 := "memory-entries-added" :: file-list [active]
  m1 = "~/.claude/projects/-Users-ghost-core-anima/memory/project_anima_phase1a6_chat_v2_landed.md"
  m2 = "~/.claude/projects/-Users-ghost-core-anima/memory/project_anima_base_ckpt_baked_p3_leak.md"
  m3 = "~/.claude/projects/-Users-ghost-core-anima/memory/feedback_corpus_quality_over_scale.md"
  index = "MEMORY.md top 3 entries"

# ─── §9 Standing directives (carry to next session) ─────────────────

@N stand_dir := "user-directives-active" :: standing [active]
  korean-prose-chat = "anima reborn 세션 chat answer prose 는 한글; code/commit/md/json mixed 유지"
  commit-push-on-complete = "요청사항 완료 시 별도 확인 없이 commit + push 진행 (위험/광범위 staging만 예외)"
  hf-dancinlab-org = "all anima HF uploads → dancinlab org (private default)"
  english-only-hf = "HF org card / READMEs / dataset descriptions / AI & ML interests must be English"
  principle-3-no-injection = "NO `[anima 역할:` etc prefix in corpus or inference (base ckpt residue acknowledged §4)"
  own-substrate-philosophy = "anima 본체 = own substrate 332M, NOT foundation borrow (sessions 2026-05-14 reject Llama detour was reaffirmation)"
  no-scale-caps = "모델 크기 + H100 발사 제한 없음, BG cost cap floor only"
  fix-and-go = "user 2026-05-15 directive — corpus quality fix then immediate dispatch, no further planning"
  active-resource-utilization = "follow-up list 작성 시 $0 집착 금지, cost-bearing BG 적극 head"

# ─── §10 Honest C3 (carry caveats) ──────────────────────────────────

@? c3_1 := "phase1a6-not-final" :: caveat [active]
  text = "Phase 1A.6 multi-turn 4/10 strict is 2× baseline but BELOW aspirational 7/10 — Phase 1A.7+ needed for true success-tier"

@? c3_2 := "base-ckpt-leak-persistent" :: caveat [active]
  text = "Base ckpt baked-in [anima 역할: + Knuth Tier patterns emit under sampling/M3, multi-turn greedy clean. Production guard: regex filter recommended for non-greedy modes"

@? c3_3 := "mps-only-measurement" :: caveat [active]
  text = "Phase 1A.6 measurements Mac MPS f32 only. RTX 5070 cuda bf16 byte equality unverified (Phase 1A.4 was byte-equal across platforms; same arch + format so equality expected)"

@? c3_4 := "scrub-pattern-risk" :: caveat [active]
  text = "If next session executes the .own NN scrub, regex `\bown\s+\d+(/\d+)*\b` must preserve `.own N` Python namespace docs (tool/transient_py/, anima_dot_own_namespace_spec_*) — distinct concept, accidental deletion would break .own 1/2/3/4 file-taxonomy"

@? c3_5 := "session-cron-cleaned" :: caveat [active]
  text = "Cron adabd3bc CronDelete'd 2026-05-15. No active monitors. Background bash tasks all completed (bsanpmogi/b1imf2xuk/bx8rg6fel/b1q50yoee). Clean slate for next session."

# ─── §11 Cross-link ──────────────────────────────────────────────────

@X x_benchmark := "BENCHMARK.md" :: cross-link [active]
  url = "BENCHMARK.md §1-§8 (Phase 1A.4 + cotrain v1 + Phase 1A.6)"

@X x_lineup := "LINE-UP.md" :: cross-link [active]
  url = "LINE-UP.md 4 canonical entries (★★★★★ + 🧬 + 💬 + baseline)"

@X x_verdict := "Phase 1A.6 verdict doc" :: cross-link [active]
  url = "docs/anima_phase1a6_chat_v2_verdict_2026_05_15.md (10 §, 7 honest C3)"

@X x_persona := "PERSONA.tape §A6" :: cross-link [active]
  url = "PERSONA.tape §A6 + docs/anima_pscc_55_lm_falsified_2026_05_14.md (prior saga ledger)"

@X x_chatquality := "CHAT-QUALITY.tape" :: cross-link [active]
  url = "CHAT-QUALITY.tape (current session lane design ledger)"
