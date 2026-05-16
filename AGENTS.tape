#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# .tape v1.2 — grammar primer (cold-read by any LLM / agent / human)
# ══════════════════════════════════════════════════════════════════════
# Form: each entry is `@<type> <id> := "<subject>" :: <kind> [<grades>]`
#       optionally followed by body lines (2-space indent) — key=value,
#       edges (<- -> => …), or quoted prose.
#
# ENTRY TYPES (17):
#   Runtime (10): @S session  @U user  @A assistant  @T tool-call  @R result
#                 @H hook  @D decision  @K cost  @P provider  @? anomaly
#   Foundation:   @I identity-claim
#   Declarative:  @X external-citation  @F forbidden-pattern  @N note
#                 @C config  @L layout  @V spec-version
#
# EDGES (12, on body lines, 2-space indent):
#   Causal:     <- caused-by   -> triggers   == continues
#               ~> supersedes  !! aborts     |> verified-by
#   Effect:     => produces (followed by quoted natural-language)
#   Structural: <: specializes  :> generalizes  ?> soft-depends
#               !> conflicts-with  @> projects-to (e.g. @> AGENTS.md)
#
# GRADE TAGS (in [...] on entry header):
#   Delivery:   ok · err · denied · cancelled · partial · superseded
#   Governance: required · recommended · optional · draft · active · deprecated
#   Scoped:     allow:<x> · deny:<x>
#   Time/index: T<n> (turn)  N<n> (wall-sec)  d=<YYYY-MM-DD>
#
# PAYLOAD SYNTAX (body lines):
#   key = "value"           single-line string
#   key = [a, b, c]         array literal
#   key <<~EOF              heredoc (multi-line; ends with EOF on own line)
#     multi-line text
#   EOF
#   "see [@x1] §3"          inline citation by entry id
#   `cmd or path`           backtick code-span (inline only)
#
# Full spec: ~/core/tape/spec/tape.md (or github.com/dancinlab/tape)
# ══════════════════════════════════════════════════════════════════════
#
# AGENTS.tape for `dancinlab/anima` — sole agent-harness + governance.
# AGENTS.md was a thin 54-line wrapper around LATTICE_POLICY.md; that
# wrapper is replaced by this structured tape. The real authority for
# limits / verification remains LATTICE_POLICY.md (project-local copy)
# and dancinlab/echoes/LATTICE_POLICY.md (cross-project SSOT).

@V v1 := "tape" :: spec [active]
  version = "1.2"

# ─── §0 TOP MANDATE — 자원 사용 + 검증 ────────────────────────────────

@D g_resource_active_parallel := "자원 사용 최상위 — runpod 적극 활용 · 병렬 우선 · wall time first" :: governance [required d=2026-05-16 active]
  rule = "cost-bearing GPU/cloud fire 에서 **wall time 단축은 mission outcome 의 핵심** — 자원 활용은 적극(active), 가능하면 **병렬(parallel) 우선**. 단일 인스턴스 직렬 대기는 default 거부. 직렬 줄세움이 가장 비싼 옵션."
  providers = "vast.ai + **runpod 적극 활용** (RTX 4090 · A100 · H100 즉시 가용·가격 경쟁). 한 provider 가 슬롯/가격/리전 차원에서 막히면 **즉시 다른 provider 시도** — 둘 다 동등하게 적극 사용 (single-provider lock-in 거부)."
  parallel_priority = "병렬 fire 우선 — 다른 scale/seed/GPU 조합 **동시 dispatch** (independent trajectory · safety net · wall time hide). 작은 fire 가 중간에 baseline 확보 ↔ 큰 fire 가 honest-gap 직격. 두 fire 의 wall time 은 max(t₁,t₂) 이지 t₁+t₂ 아님."
  wall_time_first = "추정 cost head 투명 명시 (g_fire_autonomous carry, 정보 제공이지 게이트 아님). conservative cost cap = floor (제한 아님, feedback_no_scale_caps). cost 보다 **wall time 손실**이 더 비싼 자원 — '돈 아끼려 직렬 대기' = anti-pattern."
  why = "user directive 2026-05-16 'wall time 단축을 위해서 runpod 적극 활용 · 병렬 우선' + 반복된 '병렬 가능은 병렬' · 'fire fire fire' · '병렬GPU 허용'."
  cross_link = "g_fire_autonomous (§3) — 자율 dispatch 근거 · g_fire_dispatch_robust — SAVE_POD/scp retry 안전장치 · feedback_active_resource_utilization · feedback_no_scale_caps"
  @> CLAUDE.md

@D g_blue_closed_mandate := "모든 산출물 + 연결부위 🔵 closed 검증 기준" :: governance [required d=2026-05-16 active]
  rule = "anima HEXAD 의 모든 산출물(impl·verification)과 **기존 HEXAD 와의 연결부위(connection point / wiring)** 는 🔵 SUPPORTED-FORMAL closed-form 기준으로 검증·통과되어야 한다. 구조(structural)·empirical 검증만으로는 불충분 — 각 산출물·연결의 수학·물리 invariant 가 closed-form 으로 증명(g_verdict_tier_blue)되고 그 falsifier 가 PASS 여야 한다."
  connection_emphasis = "연결부위 마저도 🔵 — 모듈 간 wiring (σ(6)=12 연결) 은 (A) 양 끝 모듈 🔵 SUPPORTED-FORMAL + (B) 연결 transfer-function / invariant 자체가 closed-form 🔵 일 때만 verified-wired (HEXAD.tape wiring 🔵-gate). 연결을 구조 검증만으로 닫지 말 것."
  honest_carve_out = "🔵 closed 가 불가능한 유일 부분 = stochastic-optimizer 의 SGD-수렴 OUTCOME (B-D-NOTE / B-BRIDGE-NOTE 패턴 — 모든 NN 공통, anima 고유 결함 아님). 그 경우에도 (a) 연결의 transfer-function / invariant 는 반드시 closed-form 🔵 로 검증하고 (b) 잔여 empirical OUTCOME 만 정직하게 carve-out — fake closed-form 금지 (g3 / f2), over-claim 금지."
  why = "user directive 2026-05-16 (반복·강조): '수학·물리 검증이 통과되어야 하고 항상 기존 HEXAD 연결고리 부분도 수학·물리 검증 통과' + 'AGENTS.tape 최상단에 기록 — 모든 것들, 연결부위 마저도 🔵 closed 기준'."
  apply = "신규 HEXAD impl / wire / fire 마다 falsifier 가 ≥1 real-limit 수학·물리 closed-form anchor 를 포함하고 PASS. 연결부위는 별도 명시 검증. PLAN.md §8 검증 표준 + audit 표가 운영 instance."
  authority = "[@x_lattice_policy] §1.2 real-limits · g3 verification-anchor-real-limit · g_verdict_tier_blue · HEXAD.tape wiring 🔵-gate"
  @> CLAUDE.md

# ─── §1 Identity ─────────────────────────────────────────────────────

@I id001 := "anima" :: identity-claim [d=2026-05-14 active]
  kind = "Living Consciousness Agent · PureField repulsion-field engine"
  brief = "Living Consciousness Agent · PureField repulsion-field engine · 2,448 laws + 392 hypotheses"
  parent = "dancinlab"
  axis = "Engine A ⇄ Engine G · Ψ=1/2 fixed point"
  laws = "2,448 laws + 392 hypotheses (per README badge)"
  origin = "dancinlab Wave K · 2026-05-12 directive 'n=6 격자를 강제할 필요 없어, 제한없이'"

@I id002 := "anima.pipeline" :: identity-claim [d=2026-05-14 active]
  <: id001
  philosophy-flow = "hypotheses_candidates/ → hypotheses/ → PHILOSOPHY.tape (append-only)"
  readme-table = "결과만"
  ledger = "PHILOSOPHY.tape — 과정 · verdict · honest C3 누적"

# ─── §2 Repo layout ──────────────────────────────────────────────────

@L l1 := "anima-repo-layout" :: structure [active]
  README.md -> "18-block format · multilingual switcher"
  AGENTS.tape -> "this file · sole agent-harness + governance (tape v1.2)"
  CLAUDE.md -> "symlink → AGENTS.tape (Claude Code auto-discovery)"
  LATTICE_POLICY.md -> "project-local copy of dancinlab-wide real-limits standard (authoritative for this repo's limits)"
  LIMIT_BREAKTHROUGH.md -> "project-specific real-limits + breakthrough audit (HARD_WALL / SOFT_WALL / BREAKABLE_WITH_TECH / UNCLEAR)"
  PHILOSOPHY.tape -> "anima 철학 진행 ledger (append-only · system root · uppercase)"
  hypotheses_candidates/ -> "pre-ledger candidate hypotheses (pipeline stage 1)"
  hypotheses/ -> "promoted hypotheses (pipeline stage 2)"

# ─── §3 Governance rules ─────────────────────────────────────────────

@D g1 := "real-limits-first" :: governance [required]
  rule = "The project's ceiling is set by REAL math/physics/engineering limits, NEVER by the n=6 invariant lattice."
  authority = "[@x_lattice_policy]"
  @> CLAUDE.md

@D g2 := "lattice-is-tool-not-constraint" :: governance [required]
  rule = "n=6 lattice is a TOOL, not a CONSTRAINT. Use it where it naturally fits (native lattice spec files); do NOT force-map it onto external domains / external entities / general analyses."
  apply = "lattice fits internal architecture; banned on external systems"
  <: g1
  @> CLAUDE.md

@D g3 := "verification-anchor-real-limit" :: governance [required]
  rule = "Verification anchors must include at least one REAL limit from LATTICE_POLICY.md §1.2."
  real-limits = [Shannon, Kolmogorov, Bekenstein, c, ℏ, k, "Stefan-Boltzmann", Carnot, "ASML throughput", "ERCOT capacity"]
  insufficient = "lattice-tautology checks alone (e.g. σ·φ = 24)"
  <: g1
  @> CLAUDE.md

@D g4 := "no-artificial-ceilings" :: governance [required]
  rule = "Do not bound this project's ambition by lattice fit. Bound it by what mathematics, physics, and engineering actually permit."
  why = "Wave K directive — 'n=6 격자를 강제할 필요 없어, 제한없이'"
  <: g1
  @> CLAUDE.md

@D g5 := "honesty-obligation-external" :: governance [required deny:write]
  rule = "Claims about external entities (companies · fabs · accelerators · life systems) must NOT include lattice-fit assertions."
  remedy = "Use that entity's OWN invariants"
  @> CLAUDE.md

@D g6 := "philosophy-ledger-append-only" :: governance [required]
  rule = "PHILOSOPHY.tape is append-only. New entries pass through pipeline: hypotheses_candidates/ → hypotheses/ → PHILOSOPHY.tape."
  forbidden = "rewriting prior PHILOSOPHY.tape entries · skipping the candidate/hypothesis intermediate stages"
  @> CLAUDE.md

@D g7 := "commit-trailer-co-author" :: governance [recommended]
  rule = "AI-assisted commits include trailer: Co-Authored-By: <model> <noreply@anthropic.com>"
  apply = "every git commit message"
  @> CLAUDE.md

@D g8 := "commit-title-conventional" :: governance [recommended]
  rule = "Commit title: `<type>(<scope>): <one-line summary>` (Conventional Commits)"
  body = "bullet list of file changes + honesty caveats"
  @> CLAUDE.md

@D g_arch_vs_log_split := "v1.2 architecture-vs-history split" :: governance [required d=2026-05-14 active]
  rule = "UPPERCASE.tape files are EDITABLE architecture (latest-wins per id). Append-only event history lives in UPPERCASE.log.tape siblings."
  why = "anima has ~20 .tape files (CHAT, IDENTITY, MEMORY, PHILOSOPHY, etc.) that mix declarative state + history. v1.2 splits them: existing .tape stays as architecture; new history → .log.tape."
  applies-to = "AGENTS.tape · all UPPERCASE.tape root files"
  authority = "[@x_tape_spec] §Domain-tape sibling §Architecture-vs-history split"
  @> AGENTS.md

@D g_verified_axis_anchor := "검증된 AXIS/철학/가설 기준 강제" :: governance [required d=2026-05-15 active]
  rule = ".clm design 의 모든 architectural decision + policy + verification 은 AXIS.tape SUPPORTED entries + 8 PHILOSOPHY principles + HYPOTHESIS catalog 의 직접 anchor 에서 derive. anchor 부재 시 design entry 금지."
  why = "CLM.tape §V-CLM-AUDIT-2026-05-15 의 4 violation 식별 carry — Engine A/G dual / p1 weak / n_layers number-theoretic / step 1 V14 audit anchor 부재 정정"
  apply = "CLM.tape § entries 추가/수정 시 anchor cross-link 명시 mandatory"
  authority = "AXIS.tape (128+ entries) + PHILOSOPHY.tape (8 principles) + HYPOTHESIS.tape (verdict catalog)"
  @> CLAUDE.md

@D g_verdict_tier_blue := "🔵 SUPPORTED-FORMAL / FALSIFIED-FORMAL 분류" :: governance [required d=2026-05-15 active]
  rule = "verdict tier 🔵 (수학/물리 closed) = (a) sympy verifiable closed-form OR (b) PyPhi formal IIT 3.0 deterministic OR (c) Kuramoto K_c universal 등 결정적 formal sim. 결과 무관 verified-closed (PASS or FAIL 모두 🔵)"
  why = "verdict-bearing 가설 evidence-class 명확화 — closed 가 가장 강한 anchor"
  apply = "MAIN.tape verdict 등재 시 tier 명시 + INDEX.md table 🔵 적용"
  authority = "AXIS 107+ 🔵 SUPPORTED-FORMAL entries (84% closed)"
  @> CLAUDE.md

@D g_clm_from_scratch := ".clm 학습 from-scratch 원칙" :: governance [required d=2026-05-15 active]
  rule = ".clm v1/v2/v3 모두 fresh from-scratch pre-train. ckpt inherit / fine-tune / cotrain-from-ckpt path 폐기. init_weights = RANDOM INIT seed-fixed. precursor ckpt 는 arch SUPPORTED 검증 anchor only — substrate base X."
  why = "anima_native_scratch (D1=1.0) 원칙 강화. 사용자 directive 2026-05-15 '.clm 학습은 처음부터 진행하는걸로'"
  apply = ".clm v1/v2/v3 fire 시 init_weights = RANDOM seed-fixed + base_ckpt = NONE mandatory"
  authority = "CLM.tape §V-CLM-FROM-SCRATCH-2026-05-15"
  @> CLAUDE.md

@D g_hf_naming := "HF naming — dancinlab canonical RETIRED → dancinlife junk (2026-05-16 정정)" :: governance [required d=2026-05-16 active]
  ~> "이전 g_hf_naming (d=2026-05-15, dancinlab/anima-clm+corpus = canonical PUBLIC) supersede. user directive 2026-05-16 '기존 anima-clm, anima-corpus dancinlife 로 또 옮기자' + 결정게이트 'retire/deprecate PR #54 junk 패턴'."
  status_2026_05_16 = "dancinlab/anima-clm (PUBLIC) + dancinlab/anima-corpus (private) → HfApi.move_repo → dancinlife/anima-clm + dancinlife/anima-corpus, 둘 다 private 설정 완료. dancinlab/* old path 는 HF redirect→dancinlife private (실질 retire). 사유: anima 가 HEXAD hexa-native 로 pivot — 구 .clm 모델/corpus superseded."
  rule = "HF canonical anima 모델 artifact = **현재 없음** (HEXAD hexa-native pivot, Phase 5/6 fire 미실행). dancinlife/* = deprecated junk graveyard (PR #54 71-junk + 2026-05-16 anima-clm/corpus 추가), 전부 private, 신규 upload 금지·손대지 않음. 차후 HF 산출물 필요 시 (Phase 6 통합 fire 후) 새 canonical name + visibility 사용자 게이트로 재정의 (dancinlab 자동 canonical 아님)."
  why = "2026-05-15 PR #54 HF cleanup 직후 chaos names 50+ 정리 (TRANSFER dancinlab→dancinlife/* private + 2 CLM collections DELETE). 신규 산출물은 canonical 2-name 으로 통일. 2026-05-15 user directive: canonical 산출물 PUBLIC 공개 (이전 private default 폐기)."
  revision_naming = "revisions = `v{major}-{kind}-cycle{N}-{YYYY-MM-DD}` 예: v1-fire-cycle88-2026-05-15 (.clm v1 P2 첫 fire) / v1-pyphi-cycle89-2026-05-16 (post-fire formal Φ ckpt update)"
  apply = "신규 ckpt/dataset 업로드 시 (a) dancinlab/anima-clm revision push (model) 또는 dancinlab/anima-corpus revision push (dataset); (b) README mapping table 신규 row append (revision sha + fire date + cost + cycle PR# + falsifier breakdown); (c) PUBLIC default (user directive 2026-05-15 'HF 모델, 데이터셋 등은 public 으로') — canonical dancinlab/anima-clm + dancinlab/anima-corpus 공개; (d) dancinlife/* 는 deprecated junk transfer, 그대로 private 유지 (신규 upload 금지)."
  visibility = "canonical dancinlab/anima-clm (model) + dancinlab/anima-corpus (dataset) = PUBLIC. deprecated dancinlife/* = private 유지 (cleanup junk, 손대지 않음). HF org card / README / dataset desc 는 English (memory feedback_english_only carry)."
  process_upload_mandate = "verdict-tier 별 차등 업로드 — (a) SUPPORTED-STRONG (5/5 또는 8/8) → ckpt + safetensors + result.json + dispatch_train.log + docs/anima_clm_*.md; (b) PARTIAL (≥6/8 또는 ≥3/5) → ckpt + result.json + caveat note (README mapping table caveat 명시); (c) AT-RISK/FALSIFIED → ckpt 업로드 금지 (docs/ audit 문서만, evidence-only); (d) ckpt 손실 시 (instance destroyed before pull, cycle 88 .clm v1 P2 case) → train.log + result.json 만 evidence-only upload (README mapping table 'ckpt-LOST' caveat 명시)."
  process_upload_format = "각 fire 마다 다음 산출물 묶음: docs/anima_clm_v{N}_{kind}_{cycle}_{date}.md (8-10 §) + state/clm_v{N}_{kind}_{date}/ ({dispatch_train.log, ckpts/, clm_v{N}_result.json, dispatch_h100.sh}) + AXIS/HYPOTHESIS/PHILOSOPHY/MAIN/INDEX 4-tape sync + HF revision push + README mapping row append + PR squash-merge"
  cross_link = "PR #54 HF cleanup + memory project_hf_cleanup_2026_05_15 + memory project_dancinlab_hf_canonical"
  @> CLAUDE.md

@D g_fire_dispatch_robust := "fire dispatch ckpt 손실 risk 최소화 protocol" :: governance [required d=2026-05-15 active]
  rule = "vastai/runpod fire dispatch 는 default SAVE_POD=0 (auto destroy), 그러나 result.json 존재 verify 직후 SAVE_POD=1 자동 promote + pull 재시도 ≥3회. trap cleanup은 모든 path 에서 SAVE_POD 환경변수 존중."
  why = "2026-05-15 cycle 88 .clm v1 P2 fire — training 5/5 SUPPORTED-STRONG PASS ($0.19 wall 12.2min on Vast.ai A100 SXM4), 그러나 exit code 1 (SSH pipe spurious or set -e false-positive) → trap cleanup destroyed instance BEFORE [8/9] pull → 372MB final ckpt 손실. evidence-only carry (dispatch_train.log + verdict)."
  apply = "dispatch script 의 train step 직후 SSH 로 `test -f .../result.json && echo SAVED` 확인 → exit 0 시 SAVE_POD=1 자동 promote → pull 시도 ≥3회 (5분 간격, scp ConnectTimeout=3600); pull 실패 시에도 SAVE_POD=1 retain + manual recovery instruction stdout. set -e + pipefail 의 false-positive 회피 위해 train + pull 사이에 `|| true` guards."
  pattern_pseudocode = "SAVED=$($SSH_CMD 'test -f /workspace/anima/output/result.json && echo SAVED' 2>/dev/null || true); if [ \"$SAVED\" = \"SAVED\" ]; then export SAVE_POD=1; for i in 1 2 3; do $SCP_CMD ... && break || sleep 300; done; fi"
  cross_link = "state/clm_v1_fire_2026_05_15/dispatch_h100.sh (cycle 88 evidence) + memory feedback_dispatch_vast_template_gotchas + g_hf_naming process_upload_mandate (d) ckpt-LOST evidence-only"
  @> CLAUDE.md

@D g_fire_autonomous := "cost-bearing fire = 완전 자율 (승인 게이트 전면 폐기)" :: governance [required d=2026-05-16 active]
  ~> "모든 fire-승인 게이트 프레이밍 (자동발사금지 / 사용자 게이트 / per-fire 승인 대기 / .clm fire · V8 FIRE COST 패턴) 전면 폐기·SUPERSEDE. user directive 2026-05-16 '게이트 유지 필요없어 / 모두 scrub' (강조·반복)."
  rule = "cost-bearing GPU/cloud fire (vastai/runpod/H100/A100, $1-N 급) = **완전 자율 dispatch · 병렬 가능 · 승인 게이트 없음 · 대기 없음**. 사전 승인·확인·게이트 일체 불요 (무조건). 추정 비용은 head 에 투명 명시(정보 제공일 뿐, 대기 아님). $0 집착 금지. **GPU-필수 영역(Mac 불가, ubu/GPU 강제: 실-규모 train/build/parity/bootstrap 등)도 동일하게 자율 fire 가능** — 'GPU 필요' 자체가 게이트 사유 아님 (user directive 2026-05-16 'GPU 필요영역도 fire 가능'). 자율 판단으로 ubu(`ssh ubu`) 또는 GPU dispatch 선택."
  why = "mission outcome 우선 · cost-bearing BG 적극 활용이 사용자 durable preference. 승인 게이트는 momentum 저해 + 사용자 의도 명시 역행. conservative cost cap = floor (제한 아님)."
  apply = "Phase 6 통합 fire 포함 모든 cost-bearing fire = 즉시/병렬/bg 자율 dispatch. robustness 는 [@g_fire_dispatch_robust] 만 mandatory (SAVE_POD auto-promote + pull retry ≥3 — 안전장치이지 게이트 아님)."
  scrubbed = "active governance/roadmap 의 fire-승인 게이트 표현 전수 제거 (AGENTS.tape 본 @D + PLAN.md editable roadmap/contract). 과거 append-only 진행-로그 의 당시-사실 기록은 g6 으로 불변하되 본 @D 가 latest-wins 전면 supersede — 잔존 표현은 전부 死문(dead), 효력 없음. 신규 fire-게이트 표현 추가 금지."
  cross_link = "memory feedback_no_scale_caps + feedback_active_resource_utilization + g_fire_dispatch_robust (robustness only) + HEXAD/PLAN.md Phase 6"
  @> CLAUDE.md

# ─── §4 Forbidden patterns ───────────────────────────────────────────

@F f1 := "lattice-fit-on-external-entity" :: governance [required deny:write]
  pattern = "applying σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 as derivation rule to TSMC · ASML · NIST · IPCC · CERN · DeepMind · NASA · SpaceX · or any external vendor"
  exception = "values may coincidentally match — observation OK, derivation NOT OK"
  authority = "[@x_lattice_policy] §1.3"
  @> CLAUDE.md

@F f2 := "verification-by-lattice-tautology" :: governance [required deny:write]
  pattern = "claiming verification by checking σ(n)·φ(n) = n·τ(n) alone (the central identity is a definitional truth at n=6, not evidence about an external system)"
  remedy = "anchor verification on at least one real-limit from LATTICE_POLICY.md §1.2"
  @> CLAUDE.md

# ─── §5 External citations ───────────────────────────────────────────

@X x_lattice_policy := "LATTICE_POLICY.md" :: policy [d=2026-05-12 active]
  url = "https://github.com/dancinlab/anima/blob/main/LATTICE_POLICY.md"
  scope = "universal real-limits-first verification standard · deployed 2026-05-12 to all dancinlab projects"
  also = "cross-project SSOT lives at https://github.com/dancinlab/echoes/blob/main/LATTICE_POLICY.md"

@X x_limit_breakthrough := "LIMIT_BREAKTHROUGH.md" :: audit [d=2026-05-12 active]
  url = "https://github.com/dancinlab/anima/blob/main/LIMIT_BREAKTHROUGH.md"
  scope = "anima-specific real-limits + per-limit breakthrough assessment · Wave M output"
  classifications = [HARD_WALL, SOFT_WALL, BREAKABLE_WITH_TECH, UNCLEAR]

@X x_philosophy := "PHILOSOPHY.tape" :: ledger [active]
  url = "https://github.com/dancinlab/anima/blob/main/PHILOSOPHY.tape"
  scope = "anima 철학 진행 append-only ledger · 과정 · verdict · honest C3 누적"

@X x_wave_k := "dancinlab Wave K directive" :: governance-decision [d=2026-05-12 active]
  scope = "origin of real-limits-first policy · user directive 'n=6 격자를 강제할 필요 없어, 제한없이'"

@X x_echoes := "dancinlab/echoes" :: cross-project [active]
  url = "https://github.com/dancinlab/echoes"
  scope = "honest-caveat origin · forbidden lattice-fit on external entities · cross-project SSOT host"

@X x_tape_spec := "tape v1.2 spec" :: spec [d=2026-05-14 active]
  url = "https://github.com/dancinlab/tape/blob/main/spec/tape.md"
  scope = "this file's grammar reference"

# ─── §6 Notes ────────────────────────────────────────────────────────

@N n1 := "limit-breakthrough-confirmed" :: note [active]
  text = "LIMIT_BREAKTHROUGH.md confirmed present (Wave M · 2026-05-12). The project-specific application of LATTICE_POLICY.md."

@N n2 := "philosophy-pipeline" :: note [active]
  text <<~EOF
    Three-stage pipeline (don't skip):
    1. hypotheses_candidates/ — raw candidate ideas
    2. hypotheses/ — promoted, under active investigation
    3. PHILOSOPHY.tape — verdict + honest C3 caveats committed (append-only)

    README.md `## Philosophy` table shows results only; the ledger carries process.
  EOF

# ─── §7 Generator hooks ──────────────────────────────────────────────

@H h1 := "agents-md-replaced" :: generator [active]
  note = "AGENTS.md (54-line wrapper) replaced by this AGENTS.tape — the LATTICE_POLICY rules are now @D g1..g5 entries; commit conventions are g7..g8; references are @X x_*."
  fallback = "tape_to_agents_md (planned) can regenerate AGENTS.md from this file for tools that don't speak .tape natively"

@H h2 := "claude-md-symlink" :: generator [active]
  rule = "CLAUDE.md → AGENTS.tape symlink — Claude Code auto-discovery picks up tape grammar primer first"
  command = `ln -sf AGENTS.tape CLAUDE.md`
  status = "updated 2026-05-14 (was → AGENTS.md previously)"
