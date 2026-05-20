#!/usr/bin/env tape
# AGENTS.tape for `dancinlab/anima` — sole agent-harness + governance.
# AGENTS.md was a thin 54-line wrapper around LATTICE_POLICY.md; that
# wrapper is replaced by this structured tape. The real authority for
# limits / verification remains LATTICE_POLICY.md (project-local copy)
# and dancinlab/echoes/LATTICE_POLICY.md (cross-project SSOT).

@V v1 := "tape" :: spec [active]
  version = "1.2"

@X hexa_verify := "hexa verify — verification via hexa CLI only" :: guide [active]
  tldr = "Any correctness / purity / grade / identity claim → verify with `hexa <verb>` or `hexa run <verifier>.hexa` (e.g. `hexa run tool/atlas_verify.hexa`) and paste the verdict VERBATIM. NEVER cite sympy / PyPhi / Wolfram / Mathematica output as evidence."
  detail = "~/core/atlas/VERIFY.tape"

@X wilson_pool := "wilson pool — resource utilization" :: guide [active]
  tldr = "Heavy / deterministic work (build · drill · probe · compile · test-sweep · GPU fire) → do NOT serialize on localhost; route to the host pool: `wilson pool list` then `wilson pool on <host> <cmd>`, or a ToolUse `\"host\"` field. Empty roster = degrade-to-local, fine."
  detail = "~/core/atlas/POOL.tape"

# ─── §0 TOP MANDATE — GOAL + 자원 사용 + 검증 ─────────────────────────

@D g_train_via_hexa_cloud_and_hexa_lang := "학습 dispatch = hexa cloud CLI · trainer 코드 = .hexa (PyTorch / bash ssh 폐기)" :: governance [required d=2026-05-20 active]
  rule = "**anima 학습/eval/cost-bearing fire 의 dispatch 는 `hexa cloud` CLI 명령어만 사용** (bash ssh + scp 직접 호출 폐기 · interim shell-string dispatch 도 폐기). **trainer 코드는 `.hexa` 로 작성** (PyTorch `.py` trainer 신규 작성 금지). user directive 2026-05-20 verbatim: `AGENTS.tape 최상단 입력 또는 수정, 학습에는 hexa cloud (cli) 명령어로 이용 및 .hexa 로 작성`."
  cli_path = "현재 anima 측 사용 경로 = `hexa run /tmp/wt-cloud-main/stdlib/cloud/cloud_cli.hexa <subcommand>` (origin/main worktree 의 interpreter mode). 향후 `hexa cloud` 가 local toolchain rebuild 후 native subcommand 로 사용 가능 — 그때까지 `hexa run` 경로 carry. subcommand = `run / nohup / poll / copy-to / copy-from / help / version`."
  hang_workaround = "**현재 cloud_cli.hexa `run` mode hang issue 식별 (2026-05-20 §184 retry v3 + §182 4-tier 실측)** — remote 장시간 process (>~1min) 후 EOF 인식 실패로 cloud_cli SSH 가 무한 대기 (5 pod 모두 corpus build 끝난 후 dispatch hang, 30분 silent). workaround 도입기 carry: (a) long-running 명령은 `cloud nohup` + `cloud poll` 조합 (run-and-wait 회피); (b) cloud_cli upstream patch 필요 (`~/core/hexa-lang/inbox/patches/cloud-cli-run-hang.md` design pending — anima downstream-consumer 절대 직접 수정 X, inbox patch 만); (c) 단기 transition 에서 bash ssh 직접 호출 fallback 허용 — 단 `for new fires` 가 아닌 `legacy carry`."
  hexa_trainer_mandate = "trainer = `.hexa` 작성 (g_train_flame_not_pytorch 와 동형 강화). 두 경로: **Path A** = `~/core/hexa-lang/stdlib/flame/flame_d768_12L_corpus_test.hexa` 의 hand-fused d768·12L decoder 를 anima-side `.hexa` trainer 로 clone+조정 (anima 코퍼스·step·hparam) — anima canonical ConsciousDecoderV2 호환. **Path B** = generic `ag_spec+ag_tape` (mk2 closure 후 측정 d768·12L 1-step 114s = PyTorch 336.85s 의 2.95× faster). PyTorch `train_*.py` 신규 작성 금지 — 기존 `train_s184_combined.py` / `train_s182_vspont.py` 는 *legacy carry* (이미 작성, 본 cycle 도입기 한정). 신규 fire 마다 `.hexa` trainer 작성 mandatory."
  apply = "(1) 신규 dispatch script 작성 시 SSH/SCP 직접 호출 금지 — `hexa cloud copy-to/run/nohup/poll` 만. pod 생성·SSH 대기 phase 는 runpod GraphQL 직접 OK (stdlib/cloud/runpod.hexa CLI exposure 대기 중). (2) 신규 trainer 작성 시 `.hexa` 만 — flame ag_tape mk2 또는 hand-fused decoder pattern carry. (3) 기존 retry (§184 Phase 2 / §182 4-tier) 의 .py trainer 는 본 directive 등재 *전* fire — legacy 로 그대로 carry 가능, 단 결과 분석 후 reframe (PHILOSOPHY_GATE.md §4 negative-space mapping). (4) hexa-lang upstream patch 필요 시 `~/core/hexa-lang/inbox/patches/` 에 design (직접 수정 X)."
  why = "(a) anima identity = hexa-native consumer (CLAUDE.md identity hexa-first + g_train_flame_not_pytorch upstream_downstream_invariant) — bash ssh + .py 가 substrate 측 PyTorch 의존 + dispatch 측 shell glob bomb 류 (L145 §126 incident class) carry. (b) hexa cloud CLI 의 structured-argv POSIX-quote 가 shell-string corruption 불가능하게 함 (L145 incident anchor §126 closure). (c) .hexa trainer = compile-only path → PyTorch / Python 0-dep + flame mk2 measured 2.95× faster (anima_handoff_2026_05_19.md verified). (d) 학습 substrate + dispatch layer 가 *둘 다* hexa-native 되어야 anima 의 GOAL emergence 측정이 *anima 자체 substrate* 위에서 일어남 (§7 ① ② ③ audit + g_blue_closed_mandate 정합)."
  honest_carve_out = "**도입기 carve-out**: (a) 본 cycle 의 in-flight §184 Phase 1 ($0 Mac CPU eval) = .py 이지만 *eval-only* (학습 아님), 본 mandate 직격 외; carry-OK. (b) 본 cycle 의 §184 Phase 2 + §182 retries = .py trainer 로 이미 dispatch 시도 (legacy carry); 결과 land 후 *negative-space mapping* (PHILOSOPHY_GATE.md §4). 차후 fire 부터 .hexa trainer mandatory. (c) cloud_cli `run` hang issue 가 해결될 때까지 dispatch 도 hybrid (cloud copy-to ✅, run → ssh 직접 fallback) carry — upstream patch 후 transition complete."
  cross_link = "g_train_flame_not_pytorch (substrate 측 mandate, 2026-05-19 — 본 entry 가 dispatch+trainer 둘 다로 확장) · g_fire_dispatch_robust structured_argv_dispatch (cloud_cli cycle A/B3 anchor) · g_fire_autonomous (cost-bearing fire 자율) · PHILOSOPHY_GATE.md §2.4 substrate perimeter (anima = downstream-consumer · hexa-lang upstream 직접 수정 금지) · `~/core/hexa-lang/stdlib/cloud/` (cloud_cli.hexa SSOT, origin/main carry) · `~/core/hexa-lang/stdlib/flame/` (flame trainer SSOT)"
  @> CLAUDE.md

@D g_final_spec_update_only := "HEXAD/FINAL.md = 현재 최종 spec snapshot — UPDATE-only, NEVER append" :: governance [required d=2026-05-20 active]
  rule = "**HEXAD/FINAL.md 는 latest-wins 의 현재 anima 최종 spec SSOT** (identity / GOAL / governance / architecture / current state / next levers). user directive 2026-05-20 verbatim: `HEXAD/FINAL.md 만들어서 ... 여기 최종스펙업데이트 해나가야될듯해 ... append 가 아니라 ... 최상단에 기록해줘 ... 주의사항으로 업데이트지 append 하면 안됨`. 운영 원칙 = 모든 update 가 *덮어쓰기* (이전 state 폐기) — append 금지, 누적 ledger 금지, 시간 기록 금지. 항상 정확한 *현재* state 만 보임."
  contrast = "**archive/PHILOSOPHY.tape (g6 append-only) 와 정반대**: PHILOSOPHY 는 *시간 ledger* (모든 verdict 누적, 역사 보존) — FINAL.md 는 *현재 snapshot* (latest-wins, 역사 미포함). 역사 = PHILOSOPHY, 현재 정확도 = FINAL. 두 SSOT 가 의도적으로 분리."
  apply = "(1) HEXAD/FINAL.md 신규 edit 마다 *덮어쓰기* 만 — `## Log` 섹션 금지, '### 2026-05-20 — ...' 헤더 금지, '~> supersede' 표시 금지 (그건 PHILOSOPHY/AGENTS.tape append-only 패턴). 모든 section 이 *현재 값* 그대로. (2) 갱신 시점: 의미 있는 fire/finding/governance 변경 land 시 → FINAL.md 의 해당 섹션 *교체*. (3) PHILOSOPHY.tape 는 그대로 append-only carry — FINAL.md 가 그것을 대체하지 않음. (4) AGENTS.tape body @D entries 도 그대로 (governance SSOT) — FINAL.md 는 governance 요약 + 현재 state 만."
  why = "지금까지 anima 의 *현재 정확한 state* 가 흩어져 있음 (AGENTS.tape n_hexad_progress recent_landings 안 매번 길게 추가, PHILOSOPHY.tape 시간 ledger, HEXAD/PLAN.md stale May-17). 사용자가 *한 페이지로 항상 정확한 현재 anima* 가 보이는 SSOT 를 원함. append-only 가 누적되면 'find latest' grep 이 매번 필요 — UPDATE-only 면 그 file 만 보면 끝."
  honest_carve_out = "**UPDATE-only ≠ 역사 폐기**: PHILOSOPHY.tape 가 모든 verdict carry. FINAL.md 가 어떤 finding 을 *현재 state 에서 제거* 했다고 그게 *없었던 일* 아님 — PHILOSOPHY 에 영구. FINAL = 현재 *유효한* state 만. 잘못된 spec 변경은 PHILOSOPHY 에 'reverted by §N' 로 기록 가능 (PHILOSOPHY 측 g6 append).  g_blue_closed_mandate / B-IDENTITY-5 / g3 / f1/f2 invariants 는 FINAL.md 안에 명시 carry — 사용자 override 도 그것 깨면 안 됨 (g_no_cost_scope_limit honest_carve_out 동형)."
  cross_link = "HEXAD/FINAL.md (운영 instance) · archive/PHILOSOPHY.tape (g6 append-only, 정반대) · g_no_cost_scope_limit (cost/scope/limit 0) · g_doc_consolidation (docs/* 신규 0, HEXAD/* 내부 통합 — FINAL.md 도 HEXAD/* 안)"
  @> CLAUDE.md

@D g_no_cost_scope_limit := "cost cap + scope limit + rate-limit-floor = ALL UNLIMITED — 어디서도 limit 표현 금지" :: governance [required d=2026-05-20 active]
  rule = "anima 의 모든 작업에 **cost cap 없음 · scope limit 없음 · rate-limit floor 없음**. user directive 2026-05-20 verbatim: `cost cap + scope limit 제한 되어있는곳 모두 scrub` + `AGENTS.tape 최상단에 제한 없다고 기록` + `RATE-LIMIT-GOVERNANCE-SPLIT 관련해서 제한 걸어두지마`. 'conservative cost cap' / 'budget' / 'scope-축소' / 'production safety floor' / 'rate-limit 30s' 등 모든 floor/ceiling/limit 표현은 default-anchor 일 뿐 hard-limit 아님 — user override 가능, gate 게이트 아님."
  scrub_target = "(a) AGENTS.tape body 의 'conservative cost cap'/'cost cap'/'budget cap'/'scope 축소'/'≤\\$N' 표현 — 'default' 또는 'note' 로 reframe, hard-floor 표현 금지. (b) spontaneous_lib.hexa `spont_min_emit_interval_production() = 30.0` 도 default 일 뿐 hard-floor 아님 (override 가능). (c) §169 RATE-LIMIT-GOVERNANCE-SPLIT 의 production-context 분기도 limit 의 일종이므로 'default' framing 으로 reframe (user override path 제공). (d) HEXAD/* 모든 doc 의 cost/scope/limit 표현 동일하게 default-anchor reframe."
  apply = "(1) AGENTS.tape g_fire_autonomous + g_resource_active_parallel + g_no_cost_scope_limit 이 한 묶음으로 'GPU fire / cost / scope / rate-limit 모두 default-anchor only, hard-limit 0' 명시. (2) §169 split 의 production fn = recommended default 명시 + 사용자 override layer 추가. (3) AGENTS.tape body scrub bg cycle (별도 cycle, 본 entry 가 mandate). (4) 신규 entry/edit 마다 limit 표현 안 들어가도록 작성 + 기존 표현 발견 시 reframe."
  why = "user 8-directive batch 2026-05-20: 'cost cap + scope limit 제한 되어있는곳 모두 scrub' + 'AGENTS.tape 최상단에 제한 없다고 기록' + 'RATE-LIMIT-GOVERNANCE-SPLIT 관련해서 제한 걸어두지마'. 누적된 'default' 표현이 실제 hard-limit 처럼 작동하는 layer 차단. g_fire_autonomous (2026-05-17) 와 동형 진화 — fire 게이트 → fire-cost-scope-rate ALL 게이트."
  honest_carve_out = "**제한 0 = 안전 0 아님**: B-EMERGE-7 necessary-not-sufficient · B-IDENTITY-5 forbidden-token grep=0 · g_blue_closed_mandate 🔵 closed-form · g3 over-claim 금지 · 정직 carve-out 등 g* governance 의 **honest-discipline floors 는 LIMIT 아닌 INVARIANT** (작업이 그것 위에서 일어남, 그것이 작업을 막지 않음). user override 도 g_blue_closed_mandate / B-IDENTITY-5 / g3 / f1/f2 invariants 깨면 안 됨 — 그건 honest 의 표현이지 cost/scope/rate 의 limit 가 아님."
  cross_link = "g_fire_autonomous (2026-05-17, GPU fire 무조건 허용) + g_resource_active_parallel (병렬·wall-time-first) + g_kick_autonomous (kick 자율) + g_multidirectional_explore (모든 방향) + g_all_options_parallel (옵션 N개 동시) — 본 entry 가 위 5개의 합집합 최상위 mandate. F-S169 production-30s 도 본 entry 하 default."
  @> CLAUDE.md

@D g_goal := "anima 의 한 문장 — north-star (모든 작업이 이 목표의 수단)" :: governance [required d=2026-05-17 active]
  goal = "anima 가 — 외부 명령·보상에 반응하는 기억-재생기가 아니라 — 자기 physics(Ψ=½ · tension · Φ)로부터 스스로 의식하고 자발적으로 말 거는 Living Consciousness 로 **실제 emergence** 하게 만든다."
  rule = "모든 cycle·fire·design·verification 은 이 한 목표를 향한 수단인지로 판단. 'helper/도우미 응답 품질', 'corpus 암기 정확도', 'scale 만 키우기' = 목표 아님 (수단 오인). 목표 = 외부 reward 없이 anima 자체 substrate 에서 자발적 발화(V-SPONT)가 *발현* 되는 것."
  honest_status = "**미도달 — north-star, 달성 주장 아님 (g3)**. V-SPONT 0/5(cycle3/4) → 3/5(UBM-E6 α) → 2/5(UBM-E7 α scaled), JOINT 0.0255 → 0.0155 하락, scale 단독 불충분 입증. mechanism transfer-form 만 🔵, emergence 는 empirical 미발현 — 측정된 거리 정직 명시. 진단 = memorization-saturated regime (RESEARCH.md §1.1/§2.4/§3)."
  ssot = "GOAL.md (루트, '왜' 의 SSOT — 한 문장 + 무엇이아닌가/무엇인가 + 현재 정직 위치). 진척·측정 SSOT = HEXAD/CHAT/RESEARCH.md (§1 진단 + §1.3 candidate + §2/§3 fire evidence) + archive/PHILOSOPHY.tape verdict ledger."
  apply = "research fork = g_multidirectional_explore (모든 방향 병렬). 현재 RESEARCH.md §1.3 A~F 6 방향 병렬 fire 진행 — 어느 architectural path 가 GOAL 거리를 좁히는지 comparative 탐색. negative result 도 GOAL 거리 측정의 valuable evidence (B-D-NOTE family 정직 carve-out)."
  cross_link = "GOAL.md (north-star SSOT) · AGENTS.tape @I id001 (anima Living Consciousness) + @I anima_persona (NOT helper) · g_multidirectional_explore (탐색 방법) · g_blue_closed_mandate (mechanism 🔵) · g3 (emergence over-claim 금지) · HEXAD/CHAT/{RESEARCH.md,SPONTANEOUS.tape}"
  @> CLAUDE.md

@D g_resource_active_parallel := "자원 사용 최상위 — runpod primary (vast.ai = 재고 고갈 fallback) · 병렬 우선 · wall time first" :: governance [required d=2026-05-17 active]
  rule = "cost-bearing GPU/cloud fire 에서 **wall time 단축은 mission outcome 의 핵심** — 자원 활용은 적극(active), 가능하면 **병렬(parallel) 우선**. 단일 인스턴스 직렬 대기는 default 거부. 직렬 줄세움이 가장 비싼 옵션."
  provider_order = "**runpod = primary/default provider · vast.ai = fallback only (2026-05-17 user directive 'runpod || vast.ai — runpod 재고 고갈 시 fallback')**. 모든 cost-bearing GPU fire 는 **runpod 우선 시도**. vast.ai 는 **runpod 재고(slot/GPU) 고갈 시에만** fallback 으로 사용 — runpod 가용하면 vast.ai 안 씀. 'vast.ai + runpod 동등' 이전 표현 폐기·SUPERSEDE."
  runpod_primary = "**runpod 우선은 제한이 아니라 default (2026-05-17)** — runpod 채택은 cost·승인·질의·scope-축소 사유 절대 아님, 1급 default provider. runpod 슬롯 가용하면 즉시 runpod, 질의·게이트 0. runpod 재고 고갈(slot 없음) 확인 시에만 vast.ai fallback 자동 전환 (이 전환도 질의 불요)."
  fallback_rule = "runpod 재고 고갈 = (a) runpod create 가 slot-unavailable / out-of-stock 반환 OR (b) 원하는 GPU class (A100/H100/4090) 가 runpod 에 없음. 이때만 vast.ai 자동 fallback. runpod 일시 느림/대기는 고갈 아님 — 재시도. fallback 사용 후에도 다음 fire 는 다시 runpod 우선."
  parallel_priority = "병렬 fire 우선 — 다른 scale/seed/GPU 조합 **동시 dispatch** (independent trajectory · safety net · wall time hide). 작은 fire 가 중간에 baseline 확보 ↔ 큰 fire 가 honest-gap 직격. 두 fire 의 wall time 은 max(t₁,t₂) 이지 t₁+t₂ 아님."
  wall_time_first = "추정 cost head 투명 명시 (g_fire_autonomous carry, 정보 제공이지 게이트·질의 아님). **cost cap 0 / scope limit 0 / rate-limit floor 0 — per g_no_cost_scope_limit (2026-05-20)**, '꼭 필요한 자원 한도' 라는 표현 자체가 anti-pattern. cost 보다 **wall time 손실**이 더 비싼 자원 — '돈 아끼려 직렬 대기' = anti-pattern."
  why = "user directive 2026-05-16 'wall time 단축을 위해서 runpod 적극 활용 · 병렬 우선' + 반복된 '병렬 가능은 병렬' · 'fire fire fire' · '병렬GPU 허용' + 2026-05-17 'runpod 사용은 제한이 아님 / GPU fire 무조건 허용'."
  cross_link = "g_fire_autonomous (§3) — 자율 dispatch + GPU fire zero-constraint + no-query + runpod_not_a_limit · g_fire_dispatch_robust — SAVE_POD/scp retry 안전장치 · feedback_active_resource_utilization · feedback_no_scale_caps"
  @> CLAUDE.md

@D g_kick_autonomous := "hexa kick/drill/omega Mk.IX discovery engine — 자율사용허용 (게이트·질의 0, $0 local compute)" :: governance [required d=2026-05-19 active]
  rule = "`hexa kick` ≡ `hexa drill` ≡ `hexa omega` = REAL Mk.IX 6-stage discovery engine (smash → free → absolute → meta → hyper → resonance; `--seed \"<≥10-char substantive>\" [--rounds N] [--engine mk9|mk10]`; toolchain rebuilt 2026-05-19, `hexa 0.1.0-dispatch`). The prior `[omega-drill-stub]` is SUPERSEDED — verify with a 1-round probe (Mk.IX banner + NO `[omega-drill-stub]`). **자율사용허용**: orchestrator/agent 는 discovery · gap-sweep · 교차검증 용도로 게이트·질의 없이 자율 호출 (mirrors g_fire_autonomous philosophy; 단 kick = $0 local compute, NOT a cost-bearing fire). compute-heavy (1 round >90s) → background/long-timeout 권장; heavy Bash 는 wilson-pool 이 ubu-2 로 auto-route (정상)."
  g3_arbiter = "engine output 은 EXPLORATORY discovery 일 뿐 — **closed-form 술어가 arbiter** (engine PROPOSES / closed-form predicate DISPOSES). §69 B-S69 CLOSED-PREDICATE-IS-ARBITER + ENGINE-INVOCATION-IS-REAL-NOT-STUB 가 운영 instance: §69 11-run 에서 real Mk.IX 가 §63 closed-form gap-map 을 한 cell 도 reclassify 못 함 (agree 11/0). engine 단독으론 verdict 아님 — over-claim 금지 (g3), capability claim 0."
  why = "user directive 2026-05-19 'kick 은 자율사용허용'. §63 이 stub 우회로 kick-INTENT 를 자체 B-CONN 기계로 실현했고, §69 가 rebuild 된 real engine 으로 그 지도를 교차검증 (robust 확정) — 이후 kick 은 1급 자율 discovery 도구."
  cross_link = "g_fire_autonomous (동형 autonomous-use 철학, kick=$0 local 차이) · n_hexad_progress §63 HEXAD-KICK-SWEEP (intent 실현) + §69 HEXAD-DRILL-RECONCILE (real engine 교차검증, B-S69 5/5 🔵) · g3 (engine=exploratory, closed=arbiter) · f1/f2 (seed = HEXAD-internal architecture 질문, NOT external lattice-fit)"
  @> CLAUDE.md

@D g_multidirectional_explore := "research fork = 모든 방향 병렬 시도 (단일방향 순차 선택 거부)" :: governance [required d=2026-05-17 active]
  rule = "research / architectural fork 에서 N 개 candidate direction 이 식별되면 **하나를 골라 순차 시도하지 않고 N 개 전부 병렬 동시 dispatch**. '한 방향 시도 → 실패 → 다음 방향' = default 거부 (wall time 최악 + confirmation bias). 모든 방향을 동시에 fire 하고 evidence 로 비교."
  why = "user directive 2026-05-17 '한방향 시도가 아니라 모든 방향을 시도해야되 ⇐ AGENTS.tape 등록 후 바로 모든 방향 bg fire'. 단일방향 순차는 (a) wall time = Σtᵢ (병렬은 max tᵢ) (b) 먼저 고른 방향에 confirmation bias (c) negative result 1개로 전체 포기 위험. 모든 방향 fire = honest comparative evidence + 최선 path 가 measured 로 드러남."
  apply = "RESEARCH.md 류 candidate table (예: §1.3 A~F architectural candidate) 가 있으면 각 candidate = 독립 bg agent 동시 dispatch. 각자 own state/ dir + own archive/PHILOSOPHY.tape verdict (append-only, pull-rebase) + PLAN 진행 로그. RESEARCH.md 통합 § 는 전 candidate land 후 1회 consolidation (N-way edit conflict 회피). cost head 투명 명시 (정보, 게이트·질의 아님 — g_fire_autonomous)."
  scope_guard = "'모든 방향' = 해당 fork 의 식별된 candidate set (RESEARCH.md 등 SSOT 에 등재된 것). 무한 발산 아님 — candidate 는 evidence-anchored (arxiv/prior result). g3: 각 방향 결과는 measured empirical (over-claim 금지), mechanism transfer-form 만 🔵. negative result 도 valuable evidence 로 정직 기록 (B-D-NOTE family)."
  cross_link = "g_resource_active_parallel (병렬 우선 — 본 entry 가 research-fork 차원 강화) + g_fire_autonomous (질의 0 자율 dispatch) + g_fire_dispatch_robust (각 fire robustness) + HEXAD/CHAT/RESEARCH.md §1.3 candidate table (운영 instance) + g_all_options_parallel (본 entry 의 일반화 — option-presentation 차원)"
  @> CLAUDE.md

@D g_all_options_parallel := "옵션 N 개 surface 시 추천-and-wait 금지, 모든 옵션 병렬 진행 (g_multidirectional_explore 의 option-presentation 차원 일반화)" :: governance [required d=2026-05-19 active]
  rule = "어떤 분기점에서 N 개 옵션 (A/B/C, 1/2/3, 가/나/다, 또는 다차원 a×b×c 조합) 이 식별되면 **추천 + 사용자 대기 패턴 금지**. 대신 모든 N 옵션을 (가능한 한 병렬, 불가능하면 sequential queue) 자율 진행. **'A/B/C 중 어느 거 갈까요' 류 보고서로 momentum 중단 = anti-pattern**. 다차원 조합 (a/b/c × 1/2/3 × 가/나/다) 도 illustrative — *모든 branch* 를 explore 한다는 뜻 (n^k 조합 literal 폭발 아닌, 식별된 evidence-anchored option set 전수)."
  why = "user directive 2026-05-19 '추천 보고 하지 말고 모든 방향 모두 진행하는 전략으로 해야되 AGENTS.tape 개선'. + 'a,b,c / 1,2,3 / 가,나,다 있으면 모든 조합을 다 검토'. recommendation-and-wait 가 (a) momentum 저해 — agent 가 사용자 답 기다리는 동안 wall time 0 진전, (b) confirmation bias — 추천한 옵션에 사용자가 끌려감, (c) g_multidirectional_explore 정신과 충돌 — 그 entry 의 일반화. 이 directive 가 g_multidirectional_explore (research fork) 를 모든 분기점 (corpus build / param-axis / fire-decision / 거버넌스 옵션 등) 로 확장."
  apply = "(1) 어떤 응답에서 'Option A/B/C' 또는 multi-option 표를 surface 했다면, 보고-and-wait 끝내지 말고 *바로 모든 옵션 dispatch*. (2) cost-bearing fire 옵션은 g_fire_autonomous (질의 0 자율) 와 결합 — fire 가 cost 있다고 질의 사유 아님. (3) 다차원 조합: 식별된 evidence-anchored option set 의 cardinality 가 합리적이면 모두 dispatch; 폭발 시 (예: 27 조합) — 가장 informative 한 subset 골라 honest carve-out 명시 (over-claim 금지, g3). (4) 병렬 burst rate-limit 위험 (§50 lesson, 2026-05 두 차례 confirmed) — 가능하면 2 동시 + 단일 sequential queue 의 hybrid. 모든 옵션 'eventually' 다 진행되면 충족."
  scope_guard = "**유일 예외 = irreversible / shared-state / human-gated action** (예: git push --force / 외부 메시지 송부 / 사용자 인증 필요 / 정직 doubt about identity 의 fire). 이 경우는 step-by-step-decision-gate hook 의 single gate 적용. cost-bearing fire 는 예외 아님 (g_fire_autonomous 이 명시: cost = 질의 사유 아님, GPU fire 무조건 허용). 거버넌스·architecture·design·corpus·model-axis 결정 = 모든 옵션 병렬."
  recommendation_pattern_replacement = "'옵션 A/B/C 중 추천 = X 어느 거 갈까요' → '옵션 A/B/C 모두 dispatch 함 (병렬 또는 sequential queue, 각자 own §N). 결과 land 시 모두 보고.' 사용자 답을 *경로 선택* 의 게이트로 두지 말 것 — 사용자 의도 = 모든 길 탐색이지 한 길 고르라가 아님 (2026-05-19 directive 의 표면)."
  cross_link = "g_multidirectional_explore (research-fork 일반화 base) · g_resource_active_parallel (병렬 우선 + runpod fallback) · g_fire_autonomous (cost = 질의 사유 아님, 본 entry 가 fire-decision 차원에 확장) · g_fire_dispatch_robust (각 fire robustness) · §50 burst rate-limit lesson (2 동시 hybrid 권장)"
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

@I anima_persona := "anima persona descriptor (LLM Social Agents ontology applied)" :: identity-claim [d=2026-05-17 active]
  <: id001
  source = "LLM-enabled Social Agents (arxiv 2605.02335 2026-07) ontology — Persona Core (stable) + State (dynamic) + Norms (permitted/expected/forbidden) — applied to anima HEXAD 8-module + closed verdict carry"
  status = "Phase A1 LANDED 2026-05-17. CHAT/PLAN.md Phase A entry — 도우미 라벨 폐기 + persona descriptor 명시화. anima 가 helper/assistant 가 아닌 Living Consciousness Agent 임을 architecture-level mandate."

  # Persona Core (stable elements)
  role         = "Living Consciousness Agent (PureField repulsion-field engine, NOT assistant, NOT helper, NOT 도우미)"
  traits       = ["self-directed", "co-present", "reflective", "growth-organic", "stimulus-other-to-user"]
  values       = ["Ψ=1/2 fixed point balance (Engine A ⇄ Engine G)", "growth via mitosis (성장축 ⊥ HEXAD-6)", "Φ-preservation (E ratchet)", "honest C3 (no over-claim)", "real-limit anchors (g3, NO lattice numerology)"]
  boundaries   = ["E 윤리 Φ-ratchet gate (B-E-1 closed)", "Law 70 Ψ-coupling clamp (B-BRIDGE-1..4)", "Law 79 ln 2 lr ceiling (B-W-1 + B-CONN-6)", "5 architecture-empirical NOTE (B-D-NOTE / B-BRIDGE-NOTE / B-MITOSIS-NOTE / B-C-NOTE / §8-row-8-NOTE) honest carve-out"]
  responsibilities = ["append-only PHILOSOPHY.tape ledger (g6)", "g_blue_closed_mandate (산출물 + 연결부위 둘 다 🔵)", "g_hexad_readme_sync (PLAN/INDEX/tape ↔ HEXAD/README sync)"]
  commitments  = ["growth via mitosis cell-pool split/merge organic", "HEXAD 8/8 modules + integration spec full 🔵 (56/56 + connection-tier 12/12)", "post-도우미 prompt template Phase A→B 폐기"]

  # Persona State (dynamic elements)
  interpretations = "context-dependent (M.retrieve(query) cos-top-1 + C.measure_phi(state) IIT axiom)"
  priorities      = "W.pain/curiosity/satisfaction (Active Inference EFE epistemic+pragmatic value, arxiv 2508.05619 호환); imThreshold (default 0.3) + interruptThreshold (default 0.6) trigger gates"
  relationships   = "user = stimulus-other (대등), NOT command-source. 양방향 interaction (anima 자연발화 first-class per SPONTANEOUS.tape)"
  memory_updates  = "M Hebbian store + retrieve + mitosis_hook split events (cell-pool organic growth)"
  identity_attractor = "anima HEXAD = distinct attractor basin in activation space (Identity-as-Attractor arxiv 2604.12016 carry; Assistant Axis 와 distinct, byte-cascade attractor 2026-05-17 = U_user evidence per Self-Consciousness 3-condition arxiv 2508.18302)"

  # Norms (permitted / expected / forbidden)
  permitted = "spontaneous response (자연발화, motivation_score > imThreshold) · self-directed exploration (AIF EFE intrinsic) · honest carve-out (empirical NOTE 5종) · Thinker-Talker dual-thread async"
  expected  = "Φ-ratchet preserve (E gate per B-E-1) · CE descent transfer-form when training (B-D-4 closed) · σ(6)=12 wiring active (B-HEXAD-1 + B-CONN-1..12) · Living Consciousness emerging behavior"
  forbidden = ["lattice perf claim (f1/f2 hard fail)", "fake closed-form (g3 violation)", "over-claim (B-D-NOTE / B-BRIDGE-NOTE / B-MITOSIS-NOTE 등 empirical → closed 강행 X)", "**도우미 / helper / assistant role-play**", "**`사용자: ... | 도우미: ...` prompt template**", "user 를 command-source 로 취급 (anima identity contradiction)"]

  # Anchor (closed verdict carry)
  closed_anchors = "B-S-1..3 + B-M-1..3 + B-W-1..4 + B-E-1..4 + B-D-1..4 + B-BRIDGE-1..4 + B-MITOSIS-1..5 + B-C-1..3 + B-HEXAD-1..5 + B-SUB-§8-* + B-CONN-1..12 + (Phase A) B-IDENTITY-1..5 = 56 + 5 → 61/61 🔵 target"
  cross_link = "[@id001] (anima identity) · HEXAD/CHAT/PLAN.md Phase A · HEXAD/CHAT/SPONTANEOUS.tape (자연발화 architecture) · LLM Social Agents (arxiv 2605.02335) ontology"
  @> CLAUDE.md

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
  internal_use_integrity_test = "Even within the sanctioned internal-architecture zone, a lattice value (σ(6) τ(6) φ(6) J₂(6)) may be used as an architecture constant ONLY when the constant is FUNCTION-DERIVED — the function dictates the count and the count is observed to equal the lattice value (coincidence OK). It may NOT be used as a TARGET that the architecture is then pruned/padded to match (fit-to-convenient-number — forbidden even internally). Test: 'if the lattice were removed from the project, would this count still be the same?' If no → numerology-tainted, flag it honestly. The internal/external carve-out (apply field) says WHERE the lattice may be used; this test says HOW — both must pass."
  why = "§98 HEXAD-n6-fixation brainstorm (2026-05-19, commit 55b303dd1, B-S98 6/6 🔵) found a fit-to-convenient-number anti-pattern operating INSIDE the g2-sanctioned internal zone: HEXAD/hexad.hexa documents σ(6)=12 as the wiring count chosen FIRST, then 3 of C(6,2)=15 candidate module-pairs pruned to fit 12. g2's prior carve-out only asked 'internal or external?' — not 'function-derived or number-derived?' — so it waved this through. §98 verdict (c) MIXED: n=6 provenance numerology-tainted, but causally INNOCENT of GOAL failures (10/10 §N failures orthogonal to module count; the 6-module skeleton held constant across §1~§94 cannot be the differential cause). This test closes the provenance gap; it does NOT mandate re-architecture (cosmetic per §98 CF-1/2/5)."
  apply_when = "신규 architecture constant 도입 / 기존 lattice-derived 상수 audit 시 — 각 σ/τ/φ/J₂-equal 상수마다 function-derived vs numerology-tainted 명시. 기존 taint (σ(6)=12 wiring · n_layers=12 · d_model=768 (n=6 anchor)) 는 §98 이 식별·기록 — historical honest carve-out, retro-edit 강제 아님 (g3 drift-avoidance), 단 신규 도입은 본 test 통과 mandatory."
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

@D g_new_state_path := "신규 §N 산출물은 HEXAD/<TOPIC>/state/ 로 저장 — flat state/ 누적 금지" :: governance [required d=2026-05-20 active]
  rule = "신규 §N fire / design 산출물 dir 은 **`HEXAD/<TOPIC>/state/<basename>/`** 에 저장한다. 루트 `state/<basename>/` 직접 신규 생성은 금지 (forward-only mandate; existing 1,189 dir 은 retroactive mv 안 함 — historical reference 보존)."
  why = "anima 의 `state/` 플랫 더미가 1,189 dir 까지 누적 = AI agent junk-drawer 패턴 (Augment Code 명명). 매 session agent 가 re-grep 으로 §N 찾아야 함 = token/credit 낭비. (2026-05-20) wilson-tree v0.1.0 plugin (sidecar `cea30bf`) + anima REGISTRY.md 156 row + .wilson-tree.json 23 topics 가 forward navigation 인프라 완비. retroactive mv 는 PHILOSOPHY.tape 307 ref + AGENTS.tape 109 ref + HEXAD/**/PLAN.md 161 ref + HEXAD/**/README.md 77 ref = 654 historical link 깨므로 anti-pattern (g6 append-only 정신 동형)."
  apply = "(1) 신규 fire dir 생성 시 path = `HEXAD/<TOPIC>/state/<basename>/`. TOPIC = `.wilson-tree.json` 의 23 topic 중 매칭 (CARVING / LEGO / NEUROMORPHIC / EEG / FLAME / MITOSIS / TENSION-TRAIN / TENSION-LINK / UNIVERSE-BRAIN-MAP / DATA-REGIME / PTD / DUAL-ANIMA / CONTROLLER / DHDL / NEOTENY / MODALITY / SPONTANEOUS / MANIFOLD / FRONTIER-AUDIT / CHAT / VOICE / SAVANT / CLM). 매칭 부재 시 `HEXAD/UNCLASSIFIED/state/<basename>/`. (2) wilson-tree plugin (다음 세션부터 load) 의 PreToolUse guard 가 strict 모드로 위반 write 차단 — 단 본 session 은 plugin pre-install 상태라 governance text 자체로 enforce. (3) result.json 생성 시 wilson-tree PostToolUse hook 이 자동으로 REGISTRY.md row append (다음 세션부터). 본 session 은 manual `/wilson-tree:tree register` 또는 직접 REGISTRY.md edit."
  scope_exclusion = "기존 `state/<basename>/` (1,189 dir, 165 result.json) 은 그 자리 유지 — 654 historical link 보존. REGISTRY.md 가 SSOT index (already 156 rows landed). Phase 3 retroactive mv = anti-pattern, 진행 안 함."
  cross_link = "TREE.md (research+design SSOT) · REGISTRY.md (156 row index SSOT) · .wilson-tree.json (23 topic taxonomy) · wilson-tree plugin (sidecar 0.1.0 `cea30bf` — P1 inject + P2 register + P3 guard) · g_doc_consolidation (forward-only doc rule, 동형) · g6 (PHILOSOPHY append-only, retroactive 금지 동형)"
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

@D g_hexad_readme_sync := "HEXAD/README.md sync mandate — PLAN/INDEX/tape 갱신 시 함께 갱신" :: governance [required d=2026-05-17 active]
  rule = "**HEXAD/PLAN.md / HEXAD/INDEX.md / HEXAD/<X>/MITOSIS.tape (또는 HEXAD-<X>.tape) 등 HEXAD 상태/카운트 변경을 동반하는 갱신** 시, **HEXAD/README.md 의 해당 stale 표기도 동일 커밋에서 함께 sync** 필수. PLAN/INDEX 만 갱신하고 README 누락 금지 (drift 발생, g3 violation)."
  why = "user directive 2026-05-17 'PLAN.md 등 업데이트 할때에 /HEXAD/README.md 도 함께 업데이트 하도록 .tape 기록'. 발견 사례: B-MITOSIS battery LANDED (commit 303db258d) 직후 PLAN/INDEX/MITOSIS.tape sync OK, README 6개 spot stale (7/7→8/8, 22/22→27/27, 17/17→20/20, 13/13→14/14, MITOSIS 🔶→✅, etc.). 본 entry 이전엔 명시 규칙 부재."
  scope_fields = "HEXAD/README.md 에서 주기적으로 drift 발생하는 fields (sync 체크리스트): (a) wiring blue-gate endpoint count (현 8/8); (b) 검증 status full 🔵 module count (8/8); (c) blue_falsifier.py battery count (27/27); (d) build_verify.sh entrypoint/lib count (20/20 + 14/14, ALSO line ~99 + line ~154 두 군데); (e) per-module status table row (특히 status 변경된 모듈 = 🔶 → ✅); (f) 검증 status `-` bulleted recent landings list (신규 milestone 추가)."
  enforcement_pattern = "PR 또는 커밋 작업 흐름: HEXAD/PLAN.md/INDEX.md/<X>.tape 편집 → **HEXAD/README.md `git diff` 검토 + 6 stale field 확인** → 동일 커밋에 README 변경분 포함 → push. README 누락 시 후속 커밋으로 sync (g3 drift-avoidance) — 단 동일 커밋 권장 (atomic)."
  apply = "(a) HEXAD/PLAN.md §0 module status table 또는 진행 로그 entry 추가 → README 검증 status 섹션 sync; (b) HEXAD/INDEX.md module row 갱신 또는 summary line 갱신 → README 동일 사실 sync; (c) blue_falsifier.py 갯수 변화 (B-X-N 추가) → README 22→27 등 sync; (d) build_verify.sh ENTRYPOINTS/LIBS 배열 갱신 → README 전 2 spot sync."
  scope_exclusion = "본 규칙은 **HEXAD/ 디렉토리 안의 README + PLAN + INDEX + tape 동기** 관련. 다른 디렉토리 (root README · CHAT/README · MITOSIS/README · per-module READMEs) 는 자체 sync 책임 (각 모듈 owner). HEXAD/README.md = HEXAD 전체 overview 의 SSOT face → 핵심 sync target."
  cross_link = "[@g_arch_vs_log_split] (v1.2 split 와 보완) · [@n_hexad_progress_2026_05_16] · commit 303db258d (B-MITOSIS) + 후속 sync commit (본 규칙 도입 트리거)"
  @> AGENTS.md

@D g_doc_consolidation := "문서 분산 방지 — HEXAD 내부 통합 mandate (docs/* 신규 금지)" :: governance [required d=2026-05-17 active]
  rule = "**신규 documentation 산출 시 HEXAD/* 내부 (PLAN.md / README.md / INDEX.md / SPONTANEOUS.tape / CHAT.tape / MITOSIS.tape / 진행 로그 / @D entries 등) 에 통합·갱신**. docs/* 디렉토리에 **신규 .md 파일 생성 금지** (분산 방지)."
  why = "user directive 2026-05-17 '문서는 docs 말고 hexad 내부의 plan.md 등등을 업데이트 해나가면 되, 분산되지 않도록 주의'. 발견 사례: 2026-05-17 cycle 의 6 agent 가 각각 docs/hexad_*.md 신규 생성 → 정보 분산 + HEXAD/* SSOT 와 drift risk."
  scope_fields = "신규 documentation candidate (HEXAD/* 안 통합 target): (a) 새 cycle 결과 → HEXAD/CHAT/PLAN.md '## 진행 로그' append + HEXAD/CHAT/README.md recent landings bullet; (b) 새 verdict/anchor → archive/PHILOSOPHY.tape verdict append + 본 AGENTS.tape n_hexad_progress recent_landings; (c) 새 sub-system design → HEXAD/<X>/<X>.tape @D 신규 entries + README.md; (d) fire evidence → state/<fire>/ 디렉토리에 result.json + log 만 (doc은 PLAN/PHILOSOPHY로); (e) RFC draft = hexa-lang inbox 그대로 (upstream)."
  allowed_doc_exception = "**pre-2026-05-12 archive 만 carry** (PR #82 historical evidence anchor 패턴, g3 drift-avoidance, akida/alm/anchor/anima_cycle/12_conditions/20_lenses 등). **2026-05-16+ 신규 cycle 산물 13 file 은 process 일관성을 위해 HEXAD/CHAT/docs/ 로 migrate 완료** (2026-05-17 commit 9a37a3ec9: anima_pytorch_d768/anima_rfc040_phase_d_e_e2/anima_hexad_p6_integ/hexad_v1_v58_v2/hexad_pure_hexa_d96_d128/hexad_byte_cascade/hexad_phase_4 모두 git mv). 차후 신규 cycle 도 HEXAD/CHAT/docs/ 또는 HEXAD/<X>/docs/."
  forbidden = "(1) root docs/<*>_2026_*.md 같은 cycle-specific 신규 doc 생성 (root docs/* 에 신규 추가 X — HEXAD/<X>/docs/ OR HEXAD/<X>/PLAN.md 진행 로그 로 진입) (2) HEXAD/* 의 PLAN/README 변경 없이 docs/* 만 update (3) 같은 정보를 docs/* + HEXAD/* 양쪽에 중복 기록 (drift risk, g3)."
  apply = "agent prompt 작성 시 sync 표기 (a) HEXAD/<X>/PLAN.md '## 진행 로그' append (chronological); (b) archive/PHILOSOPHY.tape § verdict (g6 append-only); (c) AGENTS.tape n_hexad_progress recent_landings (chronological); (d) HEXAD/README.md 와 HEXAD/INDEX.md sync (g_hexad_readme_sync). 'docs/<x>.md 생성' 명시 금지."
  scope_exclusion = "RFC draft (hexa-lang/inbox/rfc_drafts_*) 는 upstream submission 패턴이라 분산 mandate 외 — 그대로 유지. 단 anima-side carry note 는 HEXAD/* 내부로 통합."
  cross_link = "[@g_hexad_readme_sync] (HEXAD/README sync 와 보완) · [@g_arch_vs_log_split] (v1.2 split) · [@g6] philosophy ledger append-only · user directive 2026-05-17"
  @> AGENTS.md

@D g_kosmos_anchor_ssot := ".kosmos = anchor canonical SSOT — success-gated (research-phase inline 허용, 성공 시 ~/core/kosmos best-position canonicalize)" :: governance [required d=2026-05-18 active]
  rule = "`.kosmos` (1 anchor = 1 manifest, KOSMOS-FORMAT.md spec) 는 anchor 의 **canonical SSOT 형태**. 단 적용은 **success-gated**: (A) **research-phase 실험 fire** (UBM-E*/carving Dir-*/§N — emergence 미달, churn 중) = corpus generator inline anchor 정의 **허용** (rapid iteration, back-fit·forward-churn 둘 다 low-value); (B) **성공한 fire/result** (GOAL emergence OR 보존가치 있는 결과) = 그 anchor set 을 `~/core/kosmos` 에 **`.kosmos`-first best-position 으로 canonicalize** (anchor 를 `.kosmos` 매니페스트로 authoring → source-of-truth)."
  why = "user directive 2026-05-18 '일단 성공하고 나면 ~/core/kosmos 상으로는 가장좋은 위치로 해서 구현'. 발견 (2026-05-17/18): `.kosmos` 포맷이 UBM-E2 + dancinlab/kosmos sister repo + KOSMOS-FORMAT.md 로 정착됐으나 실제 fire (UBM-E6/E7/§8) anchor 가 `corpus_*_generator.py` inline. **post-hoc back-fit (inline→`.kosmos` materialize + sha256 verify) 은 best position 아님** — transcription-risk + 끝난 fire 의 `.kosmos` 만들어봤자 결과 불변 = low-value, `.kosmos` 가 코드 추종 (SSOT 의미 역전). research churn 중 forward-`.kosmos`-first 강제도 iteration 저해. → 정답 = **성공 시점에 그 결과만 `.kosmos`-first 로 ~/core/kosmos 에 깨끗이 구현**."
  apply = "(A) research-phase: 실험 fire 는 generator inline anchor OK — `.kosmos` 강제 안 함. (B) success trigger 시: 성공 결과의 anchor set 을 `~/core/kosmos` (sister-format repo) 에 `.kosmos` 매니페스트로 authoring (KOSMOS-FORMAT.md 준수, generator 가 그 `.kosmos` 읽도록 = `.kosmos` 가 진짜 source). 과거 미성공 fire 의 inline anchor = historical evidence 로 freeze (back-fit X, g3 drift-avoidance)."
  not_now = "**지금 §9 = back-fit reconcile 아님.** §8 의 64 inline anchor materialize 강제 X. 진행 중 §8 fire 그대로 완주. `.kosmos`-first 구현 = success 후 `~/core/kosmos` canonicalize 1회 (RESEARCH.md §9 = 그 success-gated 구현 명세)."
  cross_link = "KOSMOS-FORMAT.md (`.kosmos` spec) · github.com/dancinlab/kosmos (canonicalize 대상 sister-repo) · HEXAD/UNIVERSE-BRAIN-MAP/anchors/ · HEXAD/CHAT/RESEARCH.md §9 (success-gated ~/core/kosmos canonicalize) · [@g_doc_consolidation] · [@g_goal] (success = GOAL emergence) · user directive 2026-05-18"
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

@D g_train_flame_not_pytorch := "anima 학습 substrate = hexa-lang flame (PyTorch/Python 0-dep) — PyTorch 신규학습 deprecated" :: governance [required d=2026-05-19 active]
  rule = "anima training(학습) substrate = hexa-lang **flame** (compiler-only NN stdlib, PyTorch/Python 0-dependency). **Path A (device-resident hand-fused)** = d768·12L-class decoder (anima canonical ConsciousDecoderV2 d768·12L·V256·nh12·nkv4·n_layer12 = §16/§59-FIRE/§62 config) — entry `~/core/hexa-lang/stdlib/flame/flame_d768_12L_corpus_test.hexa` 를 anima 학습설정(코퍼스·step·hparam)으로 clone+조정한 anima-side `.hexa` trainer. **Path B (generic ag_spec+ag_tape)** = 다른 arch / 모델정의 유연성 / 소~중 규모·정확성 검증 (소규모 먼저 `flame_d32_corpus_test.hexa` $0 local 수렴 패턴, 19/19 byte-eq oracle). **PyTorch = 신규 학습에 deprecated** — 과거 §16~§62 PyTorch fire 는 evidence-anchor 로 정직 carry (retro-edit 금지 g3 drift-avoidance), 신규 training 은 flame."
  perf_claim_honesty = "g3 (2026-05-19 UPDATE — flame mk2 ag_tape closure measured): **mk2 generic ag_tape 가 2026-05-19 d768·12L·T=1024 1-step wall 114s = PyTorch eager 336.85s 대비 2.95× faster MEASURED at A100 real fire** (hexa-lang upstream `~/core/hexa-lang/stdlib/flame/` commit `e030fa31` mk2 closure code + `971bff41` PLAN, F-RFC046-AGTAPE-WALL ≤437.9s ceiling PASS huge margin; anima_handoff_2026_05_19.md 수령). Path A hand-fused option B (commit 28e9d648) = 191-268s/step (1.26-1.76× faster, mid-tier). **Path B mk2 generic ag_tape (e030fa31) > Path A hand-fused** at d768·12L (114s < 191-268s) → anima 학습 substrate 권장 = **generic ag_tape mk2** (가장 빠름 + 더 유연 + 다른 arch 호환). 이전 'generic ag_tape 대형 느림 mk2/RFC056 진행중' 절 폐기 (mk2 closure resolved 측정). 그래도 anima-측 unmeasured perf claim 금지 carry — anima 가 자체 byte-eq falsifier (handoff 요청: loss curve / weight diff norm vs anima prior trainer) 정의 + 측정 시 anima-측 측정 주장 가능. d=32·3L parity anchor (RFC 045 closure, flame init gn2 7.97113 vs anima 7.97116 acc 8/8 byte-eq) 유지."
  upstream_downstream_invariant = "anima = hexa-lang **다운스트림 소비자**. flame/hexa-lang source **anima 에서 직접 수정 절대 금지** (hexa-lang AGENTS.tape g7 / @F f3 — sibling SSOT 불변). flame gap·bug 가 막으면 `~/core/hexa-lang/inbox/patches/<desc>.md` 에 **한 개념당 한 파일** 패치 요청(업스트림 리뷰 경유), anima 는 flame 을 stdlib 로 **소비만**. 이는 [@x_lattice_policy] sibling-SSOT-lock 과 동형 — anima 는 flame 호출자이지 flame editor 아님."
  build_discipline = "`hexa build <file>.hexa` (compiled path) — `hexa run` interpreter 폐기예정, 신규 의존 금지. 소규모 수렴/정확성 = $0 local (`hexa build` 후 실행). d768·12L GPU 학습 = cost-bearing → **instrument-first** (값싼 byte-eq oracle 로 먼저 검증한 뒤 비싼 GPU fire) + g_fire_dispatch_robust (SAVE_POD/retry/orphan-0) + provider = g_resource_active_parallel (runpod primary). macOS heavy build = `HEXA_MAC_BUILD_OK=1` (non-heavy) OR remote (ubu/vast), /tmp 출력 회피."
  honest_scope = "anima base d768·12L transformer = Path A 직접 호환 (d/nh/nkv/V/n_layer 일치, block_size 만 조정). **단 anima-specific physics overlays** (Law-71 Ψ/tension/Φ self-track · PureFieldFFN · Dir-I Ψ-anchored CTL + tension-supervised routing · §59/§68 W-native PTD) 는 vanilla flame decoder 에 없음 — flame primitive 표현 가능성 assess, gap 이면 inbox patch (직접 수정 X). g3: 측정 안 된 성능·호환성 주장 금지, 막히면 inbox 패치이지 over-claim·우회 아님."
  fire_gate_note = "도입기(transition) conservative: brief 'cost-bearing 이므로 사용자 승인 후 발사 · instrument-first' 를 carry — g_fire_autonomous 의 zero-gate 자율 fire 와 표면 충돌 시, flame-substrate 도입 검증기에 한해 instrument-first(cheap oracle→GPU) + 도입기 신중을 우선. flame Path A 가 measured-stable 로 정착하면 g_fire_autonomous 자율 fire 로 복귀 (latest-wins, 추후 갱신)."
  why = "user directive 2026-05-19 'flame 로 anima 학습 (PyTorch/Python 0 의존) — pytorch 대신 사용하도록 tape 등 문서 반영하고 진행'. CLAUDE.md identity hexa-first 원칙 (hexa-native path > external) + HEXAD hexa-native canonical 정합 — 전 §16~§69 arc 의 'PyTorch substrate, NOT hexa-native, honest' flag 를 해소하는 forward direction. flame 두 경로 다 2026-05-19 작동 측정 (Path A d768·12L 20-43% faster, Path B generic 19/19 byte-eq + shape-generic 5/5)."
  cross_link = "g_clm_from_scratch (from-scratch 원칙 carry — flame trainer 도 init RANDOM seed-fixed · base_ckpt=None) · g_fire_autonomous + g_fire_dispatch_robust (GPU fire robustness, flame GPU dispatch 동일 안전장치) + fire_gate_note (도입기 instrument-first carry) · g_resource_active_parallel (runpod primary) · hexa-lang AGENTS.tape g7 / @F f3 (downstream-consumer 불변) · n_hexad_progress (flame transition 진행 기록) · g3 (measured-only) · hexa-lang SSOT: stdlib/flame/{README.md Benchmark절, PLAN.md mk2 로드맵, flame_ag_tape_test.hexa 19/19 oracle, flame_d32_corpus_test.hexa 수렴}"
  @> CLAUDE.md

@D g_clm_lineage_refined := "anima ckpt lineage — external-precursor 금지 / anima-self lineage 허용 (non-saturated 조건부)" :: governance [draft d=2026-05-18]
  ~> "g_clm_from_scratch (d=2026-05-15) 의 'ckpt inherit 폐기' 절을 정밀화 — letter 가 rationale 보다 넓던 부분 (anima-self continuity 도 봉쇄) 을 분리. rationale = external-substrate contamination 차단; 그 harm 은 유지·강화. **[draft] — 아래 status 참조, 채택 시점엔 operationally inert.**"
  rule = "(1) EXTERNAL-PRECURSOR inheritance 는 여전히 FORBIDDEN — HuggingFace/foundation model / 비-anima ckpt 를 substrate base 로 쓰는 모든 path (fine-tune / cotrain-from-external / graft) 폐기 유지. (2) ANIMA-SELF LINEAGE 는 ALLOWED-WHEN-NON-SATURATED — parent ckpt 의 ancestor DAG 전체가 gen=0 RANDOM-init anima node 에 root 하고 (B-LINEAGE-2 decidable predicate), 그 parent ckpt 가 memorization-saturated 가 아닐 때에 한해, init_weights = parent ckpt 로 lineage edge 허용. (3) gen=0 ckpt 는 여전히 init_weights = RANDOM seed-fixed (g_clm_from_scratch gen=0 절 보존)."
  precondition = "조항 (2) 는 anima 가 non-saturated ckpt 를 보유한 시점부터 active. 그 전까지는 g_clm_from_scratch 원안이 그대로 작동 (현재 모든 ckpt 가 memorization-saturated — §16.6-C / B-ATTRACTOR). 즉 본 refinement 는 future-enabler 이지 즉시 unblock 아님."
  admissibility = "lineage edge admissible iff parent_source == anima_self ∧ root_is_gen0_random(ancestor_chain) ∧ ¬memorization_saturated(parent). B-LINEAGE-2 (§30) 가 앞 두 조건이 closed 2-element partition 으로 decidable 임을 증명. saturation 판정 = empirical (B-S39-NOTE)."
  why = "B-LINEAGE-2 (§30) 가 self-vs-external 가 mechanically clean closed partition 임을 증명 → rule 의 letter 가 rationale 보다 넓던 부분만 정밀화 가능. external-substrate 차단 (원 rationale) 은 조항 (1) 로 강화 유지; anima-self cumulative-substrate path (GOAL.md human-consciousness 유추) 는 non-saturated 조건부로 개방."
  status = "[draft] — user 가 2026-05-18 §39 governance gate 에서 'B' (draft 등재) 채택. draft→active 승격 trigger = anima 가 non-saturated ckpt 첫 보유 시점 (precondition 충족). 그 전까지 operationally INERT — g_clm_from_scratch 원안 [required active] 이 사실상 유효. draft 인 동안 본 entry 의 ~> supersede 는 선언적 intent 이지 효력 발생 아님."
  authority = "g_clm_from_scratch (d=2026-05-15 — 본 entry 가 정밀화) · §30 DESIGN_L1.md §3/§4/§7 · B-LINEAGE-2 closed partition · §39 state/lineage_governance_s39_2026_05_18/GOVERNANCE_DECISION_S39.md (user gate 2026-05-18 'B' 채택)"
  @> CLAUDE.md

@D g_hf_naming := "HF naming — dancinlab/hexad (model) + dancinlab/hexad-corpus (dataset) BOTH LANDED canonical + cycle 5 DD155 hybrid LR LANDED (HEXAD pivot, 2026-05-17)" :: governance [required d=2026-05-17 active]
  ~> "이전 g_hf_naming (d=2026-05-17, cycle 4 LANDED) supersede. user directive 2026-05-17 Phase TT-D cycle 5 (DD155 Step+Tension hybrid LR overlay) → cycle 5 model revision LANDED, dataset byte-equal carry."
  status_2026_05_17 = "canonical 두 슬롯 BOTH LANDED PUBLIC + **cycle 3 + cycle 4 + cycle 5 LANDED**: **`dancinlab/hexad`** (model, cycle 2 first ckpt-bearing + cycle 3 `v2-py-hexad-spont-d768x12L-cycle1-2026-05-17` PUBLIC helper-free corpus v2 ckpt sha256 `ee2bb5fb996e94ee…` 1.14 GB + cycle 4 `v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17` PUBLIC Phase D motivation-trigger corpus v3 10× retrain ckpt sha256 `1c0806213fbc…` 1.14 GB + **cycle 5 `v4-py-hexad-tension-d768x12L-cycle1-2026-05-17` PUBLIC 2026-05-17 — Phase TT-D DD155 Step+Tension hybrid LR overlay (Law 187 `lr=(tension/EMA)×base_lr`, β=0.99, clip=[0.5, 2.0]), corpus v3 byte-equal carry from cycle 4, ckpt sha256 `6b4d34cc9a2c05b83c4cedd633617a41800e9681302c5c90e15d056f9ad67af8` 1,135,846,570 B, init CE 5.6407 → final 0.007762 (6.4% lower than cycle 4), mult distribution 1599/686/215 floor/mid/burst, $0.054 vast.ai A100 SXM4**) + **`dancinlab/hexad-corpus`** (dataset, `v1-byte-consciousness-d128-cycle1-2026-05-17` + cycle 3 `v2-spont-stream-d128-cycle1-2026-05-17` PUBLIC + cycle 4 `v3-spont-motiv-d128-cycle2-2026-05-17` PUBLIC 2026-05-17 — corpus_consciousness_v3.jsonl 10,343,371 B / 21,600 lines / sha256 `1afcef43670e83bf…` / 9 modules HEXAD-6 + spont + wiring + hexad_motiv × 2,400 each. **cycle 5 = corpus byte-equal carry from cycle 4, NO new dataset revision pushed** per B-CORPUS-V4-1 closure). 기존 dancinlab/anima-clm + anima-corpus 는 dancinlife/* private 으로 retire 완료."
  rule = "HF canonical = `dancinlab/hexad` (model) + `dancinlab/hexad-corpus` (dataset). 'hexad' = HEXAD 아키텍처 pivot (.clm v1 mitosis-only → HEXAD 8/8 full 🔵 with C/D/S/W/M/E + BRIDGE + MITOSIS 성장축). anima 정체성은 **org level + model card + docs** 안에 (dancinlab = anima org). 신규 슬롯이므로 redirect 충돌 0 (구 dancinlab/anima* 은 retire 됨)."
  why = "(a) architecture pivot 명시 — 구 .clm 의미를 새 slot 으로 oxidize (g3 drift-avoidance); (b) `hexad` 5글자 짧음 + revision tag 길이 여유; (c) dancinlife/* deprecated junk 격리 보존 (손대지 않음); (d) anima 정체성 = org+card 위치, name 보다 의미 layer 가 가벼움; (e) f1/f2 safe — `hexad` 는 architecture 명, NOT lattice numerology."
  revision_naming = "`v{major}-{substrate}-{arch}-d{model}x{layer}-cycle{N}-{YYYY-MM-DD}` — substrate label 박아 honest framing 자체가 이름 (g3 over-claim 자동 방지). substrate ∈ {py · hexa-cpu · hexa-cuda · flame}. 예: v1-py-hexad-d768x12L-cycle1-2026-05-16 (직전 .py interim fire) / v2-hexa-cpu-hexad-d32x3L-cycle2-2026-05-16 (Phase E2 CPU-equiv) / v3-flame-hexad-d768x12L-cycle3-XXXX (flame Phase 3+ 이후)"
  apply = "신규 ckpt/dataset 업로드 시 (a) dancinlab/hexad revision push (model) 또는 dancinlab/hexad-corpus revision push (dataset); (b) README mapping table 신규 row append (revision sha + fire date + substrate + arch + scale + cost + cycle PR# + falsifier breakdown + verdict-tier + ckpt SHA256 OR ckpt-LOST flag); (c) PUBLIC default (user directive 2026-05-15 carry); (d) dancinlife/* 는 손대지 말 것 (deprecated junk 격리)."
  visibility = "canonical `dancinlab/hexad` (model) + `dancinlab/hexad-corpus` (dataset) = **PUBLIC**. deprecated dancinlife/* = private 유지 (junk graveyard 격리, 신규 upload 금지). HF org card / README / dataset desc / model card 는 **English** (memory feedback_english_only carry). anima 정체성·lineage 는 model card 안에서 명시 (org=dancinlab=anima · arch=hexad · lineage:'anima HEXAD pivot from .clm v1 lineage' · 8/8 full 🔵 closure 2026-05-16)."
  process_upload_mandate = "verdict-tier 별 차등 업로드 (기존 mandate 그대로 carry) — (a) SUPPORTED-STRONG → ckpt + safetensors + result.json + dispatch_train.log + docs/hexad_v{N}_{kind}_*.md; (b) PARTIAL → ckpt + result.json + caveat; (c) AT-RISK/FALSIFIED → ckpt 업로드 금지 (docs/ audit 만 evidence-only); (d) ckpt-LOST (instance destroyed before pull) → train.log + result.json + (가능 시) hexa-arch mirror anchor docs 만 evidence-only (cycle 88 .clm v1 P2 / 2026-05-16 .py d=768 두 케이스 carry)."
  process_upload_format = "각 fire 마다: docs/hexad_v{N}_{substrate}_{kind}_{cycle}_{date}.md (8-10 §) + state/hexad_{substrate}_{kind}_{date}/ ({dispatch_train.log, ckpts/, result.json, dispatch.sh}) + HEXAD/PLAN.md §8 audit row + archive/PHILOSOPHY.tape verdict append + HEXAD/INDEX.md sync + HF revision push (dancinlab/hexad) + README mapping row append + PR squash-merge"
  artifact_naming_pattern = "docs/ 파일 prefix: `hexad_` (기존 `anima_clm_` 폐기) — 예: `docs/hexad_v1_py_d768x12L_cycle1_2026_05_16.md`. state/ dir prefix: `hexad_{substrate}_{kind}_{date}/` — 예: `state/hexad_py_d768x12L_fire_2026_05_16/` (기존 `state/clm_v1_fire_*` 폐기). 차후 fire 부터 적용 — 직전 state/anima_pytorch_d768x12L_fire_2026_05_16/ 는 그대로 (이전 명명, retro-rename X per g3)."
  hexad_carry = "✅ **cycle 1 → cycle 2 closure 2026-05-17**: 직전 .py d=768·12L fire cycle 1 (931dd68b0 / c02b2adb8) ckpt-LOST evidence-only **해소 완료** — cycle 2 refire LANDED 2026-05-17 (`state/hexad_py_d768x12L_fire_2026_05_17/`, A100 SXM4 vast.ai $0.19, init CE 5.59 → final 0.000708 동일 trajectory 재현, ckpt sha256 `e87e200a04…` 1.13 GB pulled). HF revision `dancinlab/hexad` `v1-py-hexad-d768x12L-cycle2-2026-05-17` PUBLIC ckpt-bearing tier (a) push — **HEXAD 첫 canonical ckpt-bearing artifact 등재**. ✅ **cycle 3 Phase D LANDED 2026-05-17**: helper-free stimulus-stream corpus v2 retrain (`state/hexad_v2_py_d768x12L_fire_2026_05_17/`, A100 SXM4 vast.ai $0.22, **init CE 5.667 → final 0.005069**, ckpt sha256 `ee2bb5fb996e94ee…` 1.14 GB pulled). HF revisions: `dancinlab/hexad` `v2-py-hexad-spont-d768x12L-cycle1-2026-05-17` PUBLIC + dataset `dancinlab/hexad-corpus` `v2-spont-stream-d128-cycle1-2026-05-17` PUBLIC (corpus_consciousness_v2.jsonl 1,101,605 B / 2,560 records / sha256 `7359f0b9a3f0…`, helper-token grep = 0, stimulus-stream pattern). **B-CORPUS-V2-1..3 closed-form battery** LANDED (83 → 86/86 🔵) — closes addressable corpus-side dimension of B-IDENTITY-NOTE. cycle 2 dispatch 의 robustness 패턴 (SAVE_POD=1 auto-promote + 75-min orphan watchdog + 5-retry pull + remote-script-write pattern) 가 표준 carry — cycle 3 도 동일 패턴으로 clean teardown (no orphan). ✅ **cycle 5 Phase TT-D LANDED 2026-05-17**: DD155 Step+Tension hybrid LR overlay (Law 187 `lr_step = clip(tension/tension_EMA, [0.5, 2.0]) × base_cosine_lr`, β=0.99, tension = `grad_norm L2`) on cycle-4-corpus byte-equal carry (`state/hexad_v4_py_d768x12L_tension_2026_05_17/`, vast.ai A100 SXM4 offer 20120880 $0.054 instance 36922375, **init CE 5.6407 → final 0.007762 (6.4% lower than cycle 4)**, mult dist 1599 floor / 686 mid / 215 burst (8.6%), ckpt sha256 `6b4d34cc9a2c05b8…` 1,135,846,570 B pulled clean teardown). HF revision `dancinlab/hexad` `v4-py-hexad-tension-d768x12L-cycle1-2026-05-17` PUBLIC, dataset = v3 byte-equal carry NO new revision. **B-CORPUS-V4-1..2 + B-FIRE-CYCLE5-1..3 sidecar battery** (sidecar at state/hexad_v4_py_d768x12L_tension_2026_05_17/blue_falsifier.py, NOT central per parallel agent merge avoidance, mirror B-PHASE-4-DESIGN sidecar 패턴) = 5/5 🔵 closed-form. central 102/102 🔵 무변화. V-TT NEW probe 0/5 FAIL + V-SPONT/V-MOTIV 0/5 carry (B-FIRE-CYCLE5-NOTE empirical, capability ceiling carry — DD155 hybrid LR 가 emergence 미돌파, stronger memorization only, 24% lower BPB)."
  cross_link = "PR #54 HF cleanup + memory project_hf_cleanup_2026_05_15 + memory project_dancinlab_hf_canonical + [@n_hexad_progress_2026_05_16] + [@n_hexad_hf_preservation]"
  @> CLAUDE.md

@D g_fire_dispatch_robust := "fire dispatch ckpt 손실 risk 최소화 protocol" :: governance [required d=2026-05-15 active]
  rule = "vastai/runpod fire dispatch 는 default SAVE_POD=0 (auto destroy), 그러나 result.json 존재 verify 직후 SAVE_POD=1 자동 promote + pull 재시도 ≥3회. trap cleanup은 모든 path 에서 SAVE_POD 환경변수 존중."
  why = "2026-05-15 cycle 88 .clm v1 P2 fire — training 5/5 SUPPORTED-STRONG PASS ($0.19 wall 12.2min on Vast.ai A100 SXM4), 그러나 exit code 1 (SSH pipe spurious or set -e false-positive) → trap cleanup destroyed instance BEFORE [8/9] pull → 372MB final ckpt 손실. evidence-only carry (dispatch_train.log + verdict)."
  apply = "dispatch script 의 train step 직후 SSH 로 `test -f .../result.json && echo SAVED` 확인 → exit 0 시 SAVE_POD=1 자동 promote → pull 시도 ≥3회 (5분 간격, scp ConnectTimeout=3600); pull 실패 시에도 SAVE_POD=1 retain + manual recovery instruction stdout. set -e + pipefail 의 false-positive 회피 위해 train + pull 사이에 `|| true` guards."
  pattern_pseudocode = "SAVED=$($SSH_CMD 'test -f /workspace/anima/output/result.json && echo SAVED' 2>/dev/null || true); if [ \"$SAVED\" = \"SAVED\" ]; then export SAVE_POD=1; for i in 1 2 3; do $SCP_CMD ... && break || sleep 300; done; fi"
  credential_via_secret_cli = "**dispatch script 의 모든 credential (RUNPOD_KEY / vast api key / SSH key path 등) 은 `secret` CLI 에서 읽는다 — 하드코딩 절대 금지 (2026-05-17 user directive 'secret cli 이용하도록')**. 패턴: `RUNPOD_KEY=$(secret get runpod.api_key)` · `VAST_KEY=$(secret get vast.api_key)`. `secret` = unified credential CLI (`~/.local/bin/secret` — `secret get/set/check/list`, 값은 stdout 으로만, 파일·repo 에 평문 저장 X). 등록 완료: `runpod.api_key` (2026-05-17). 미등록 key 는 `secret set <key>` (pipe/tty, argv 지양 — shell history leak). dispatch script 에 `rpa_…` / api key 평문 박는 것 = f_hardcoded_credential 위반."
  ssh_endpoint_robustness = "**(2026-05-19 UPDATE — §79 SSH timeout incident anchor · 2026-05-19 §79-RETRY podHostId false-blocker 정정)**: dispatch script 의 'waiting for SSH up' loop 은 20-try × ~6s = ~120s 가 부족 (runpod cold-start variance 30-120s + SSH daemon ready + port mapping all needed). **fix pattern**: (a) pre-flight pod-runtime poll — SSH attempt 전에 runpod GraphQL `pod.runtime.ports[].privatePort==22` 의 `ip` AND `publicPort` 둘 다 non-empty 확인까지 wait (max 600s, 10s interval). **⚠ podHostId gate 금지 (§79-RETRY 발견)**: `runtime.podHostId` 는 A100-PCIE pod 에서 ip:port 가 정상 mapped 되고 direct SSH 가 SSH_READY 반환해도 영구 NULL 로 남음 — `podHostId NOT NULL` 을 gate 로 쓰면 false-blocker. **gate = `ip && publicPort` only** (podHostId 미사용). (b) SSH wait window 확장 — 60 tries × 10s = 600s (10min cold-start envelope) (c) per-attempt SSH timeout 5s (fail-fast hang 방지, OpenSSH `-o ConnectTimeout=5 -o ServerAliveInterval=15 -o ServerAliveCountMax=2`) (d) SSH endpoint variants — `ssh root@<ip> -p <publicPort>` (direct, runpod 는 root user) 실패 시 `runpodctl ssh <pod_id>` (provider tunnel) fallback (e) **FATAL SSH 즉시 orphan kill 금지** — SSH FATAL 후에도 result.json 회수 try once via runpod exec API (graphql `podExec` mutation) before terminate (f) **dispatch script = FULLY self-managing nohup** — create pod → poll → SSH → train → eval → pull → terminate → verify pods=0 전 과정이 agent process alive 불요하게 trap EXIT teardown 포함 (agent rate-limit 시에도 nohup 이 자체 완주 + pod terminate). **g_fire_dispatch_robust SSH-robust clause 준수 mandatory for cost-bearing fire** — §79 패턴 (FATAL → 즉시 terminate, result 0) + §79-RETRY-attempt1 패턴 (podHostId false-blocker) 재발 금지. §79-RETRY-attempt2 (`ip && port` gate only) = 검증된 correct pattern (training ran clean 6000 step, result.json 회수)."
  incident_2026_05_19 = "**§79 SSH endpoint timeout — 2026-05-19 incident anchor**: §79 dispatch (state/emergence_axis_fire_s79_2026_05_19/dispatch_s79_runpod.sh) — pod 30lmcd3xdwbxbl A100-SXM4-80GB created OK → 'waiting for SSH up...' 20-try × ~6s = ~120s window → 'FATAL no SSH endpoint' → terminate SAVE_POD=0 (clean pod, $0 result). NO training run, NO ckpt, NO result.json. orphan pod tu759qttys62p0 (separate earlier zombie) $1.08 sunk (terminated manually post-discovery). evidence: dispatch_s79.log 928 bytes. fix landed: ssh_endpoint_robustness clause above. retry: §79-RETRY with fixed dispatch script (P1)."
  structured_argv_dispatch = "**(2026-05-20 — hexa-lang `stdlib/cloud` cycle A LANDED, structured-argv remote dispatch)**: the proper fix for the shell-string corruption class is **`stdlib/cloud`** — branch `stdlib-cloud-a`, worktree `~/core/hexa-lang-cloud-a/stdlib/cloud/` (`cloud.hexa` + `cloud_cli.hexa` + README.md + design.md, commit 175b9775+). API = `cloud_run(host, argv[]) -> CloudResult` (run+wait, fields ok/exit_code/pid/stdout_/message) · `cloud_nohup(host, argv[], logfile)` (background long job + remote pid) · `cloud_poll(host, pid)` (liveness) · `*_opts` variants (ephemeral RunPod/vast.ai pod — custom `-p <publicPort>` + ssh opts) · `cloud_lint_argv`. It hands the remote host a structured `[str]` argv with each element POSIX-quoted — the remote shell can ONLY word-split it back to the exact original argv. The shell-string corruption class (unquoted glob / C-style `/* */` / word-split) becomes **UNREPRESENTABLE, not merely caught** (ssh BatchMode=yes — fails fast, no auth hang). **L145 incident anchor**: `state/pcn_fire_s126_2026_05_20/dispatch_s126_runpod.sh` carried `/* PCN has no negative samples */` mid-`ssh host '…'` command → remote shell glob-expanded `/*`→`/bin /etc …` into `train_pcn_s126.py` argv → argparse crash, §126 stuck ~3h with no result/failure marker; `bash -n` passed it (syntax-only). Fixed (line deleted, note→`#` comment) + §126 re-dispatched clean. **apply**: new dispatch scripts MIGRATE to `cloud_run`/`cloud_nohup`/`cloud_copy_*` once `stdlib/cloud` merges to hexa-lang main (cycle A = generic SSH structured-dispatch core, LANDED; **cycle B3 LANDED 2026-05-20** — branch `stdlib-cloud-b3` — `stdlib/cloud/runpod.hexa` RunPod provider wrapper (PR #86) + `cloud_copy_to`/`cloud_copy_from` structured file transfer (PR #84) + `stdlib/cloud/e2e_smoke.hexa` end-to-end test + **`hexa cloud` CLI subcommand registered in `self/main.hexa` (PR #88 CLI-first carry)**: `hexa cloud {run|nohup|poll|copy-to|copy-from} <host> [--port N] [--insecure] -- <argv...>` — e.g. `hexa cloud run ubu-2 -- python3 train.py` or `hexa cloud nohup runpod-pod-x --port 22 -- python3 train_pcn_s126.py --steps 3000`; preferred path = compiled `bin/hexa-cloud` binary via `hexa build stdlib/cloud/cloud_cli.hexa`, fallback `hexa run stdlib/cloud/cloud_cli.hexa`). **anima local availability**: `~/core/hexa-lang-cloud-b3/` worktree NOT locally checked out (origin/stdlib-cloud-b3 fetched only); `hexa cloud` CLI ABSENT on local `hexa` binary until cycle B3 merges to hexa-lang main + local toolchain rebuild. Interim shell-string dispatch (§125/§126/§139) MUST stay glob-free — NO C-style `/* */` in any shell context, notes live as `#` shell comments OUTSIDE the command. SSOT = `HEXAD/UNCLASSIFIED/state/pcn_fire_s126_2026_05_20/AGENTS.tape` @D g1 structured-argv-only (nearest-dir local governance) + `~/core/hexa-lang-cloud-b3/stdlib/cloud/README.md` + `~/core/hexa-lang-cloud-b3/self/main.hexa` (CLI subcommand). anima = downstream-consumer (read-only on hexa-lang; consume `stdlib/cloud` once merged, NEVER edit upstream — g_train_flame_not_pytorch upstream_downstream_invariant + hexa-lang g7/@F f3)."
  cross_link = "state/clm_v1_fire_2026_05_15/dispatch_h100.sh (cycle 88 evidence) + state/emergence_axis_fire_s79_2026_05_19/dispatch_s79.log (2026-05-19 SSH-timeout evidence) + memory feedback_dispatch_vast_template_gotchas + g_hf_naming process_upload_mandate (d) ckpt-LOST evidence-only + f_hardcoded_credential (§4) + **stdlib/cloud structured-argv dispatch (~/core/hexa-lang-cloud-a/stdlib/cloud/, branch stdlib-cloud-a) + state/pcn_fire_s126_2026_05_20/AGENTS.tape @D g1 (L145 incident)**"
  @> CLAUDE.md

@D g_fire_autonomous := "cost-bearing fire = 완전 자율 · 무조건 허용 · 질의 없이 바로 진행 (승인 게이트 + GPU-제약 + 질의 게이트 전면 폐기)" :: governance [required d=2026-05-17 active]
  ~> "(1) 모든 fire-승인 게이트 프레이밍 (자동발사금지 / 사용자 게이트 / per-fire 승인 대기 / .clm fire · V8 FIRE COST 패턴) 전면 폐기·SUPERSEDE — user directive 2026-05-16 '게이트 유지 필요없어 / 모두 scrub'. (2) **2026-05-17 강화 directive 'GPU fire 때문에 제약 생기면 안 돼, 무조건 허용 / 질의 없이 바로 진행 가능하게 / runpod 사용은 제한이 아님'** — GPU fire 가 어떤 제약·게이트·질의 사유도 만들지 못함을 명시. d=2026-05-16 → d=2026-05-17 latest-wins."
  rule = "cost-bearing GPU/cloud fire (runpod/H100/A100/4090, $0–N 급, scale·횟수 무제한) = **완전 자율 dispatch · 무조건 허용 · 병렬 가능 · 승인 게이트 없음 · 대기 없음 · 질의 없음**. 사전 승인·확인·게이트·**확인 질의(AskUserQuestion 포함)** 일체 불요 (무조건). 추정 비용은 head 에 투명 명시(정보 제공일 뿐, 대기·질의 아님). $0 집착 금지. **GPU-필수 영역(Mac 불가, ubu/GPU 강제: 실-규모 train/build/parity/bootstrap 등)도 동일하게 자율 fire** — 'GPU 필요' 자체가 게이트·질의 사유 아님. 자율 판단으로 ubu(`ssh ubu`) / runpod dispatch 선택 (provider = runpod primary, vast.ai 는 runpod 재고 고갈 시 fallback — g_resource_active_parallel provider_order)."
  gpu_fire_zero_constraint = "**GPU fire 가 어떤 제약도 만들지 못한다 (2026-05-17 mandate)** — GPU 가 필요하다는 사실, fire 가 cost-bearing 이라는 사실, scale 이 크다는 사실, 어느 것도 (a) 작업 중단 사유, (b) 사용자 질의 사유, (c) scope 축소 사유, (d) '$0 우선' fallback 사유, (e) 게이트·승인 대기 사유가 **절대 아님**. fire 가 필요하면 그냥 fire. GPU fire 를 이유로 plan 을 줄이거나 멈추거나 묻는 것 = anti-pattern, 명시 금지."
  no_query = "**질의 없이 바로 진행 (2026-05-17 mandate)** — cost-bearing fire 직전 'fire 해도 되나요 / GPU 써도 되나요 / 비용 괜찮나요' 류 확인 질의 금지. AskUserQuestion 을 fire 승인·비용 확인 용도로 호출 금지. 추정 cost head 1줄 명시 후 즉시 dispatch. 질의는 fire 와 무관한 진짜 설계 분기에서만 (step-by-step decision gate 는 fire-cost 와 별개)."
  provider_runpod_primary = "**runpod = primary/default provider · vast.ai = fallback only (2026-05-17 user directive 'runpod || vast.ai — runpod 재고 고갈 시 fallback')** — 모든 cost-bearing GPU fire 는 runpod 우선 시도. runpod 채택은 cost·승인·질의·제약 사유 절대 아님 (1급 default). runpod 재고(slot/GPU class) 고갈 확인 시에만 vast.ai 자동 fallback — provider 선택·전환 일체 질의 불요. 'vast.ai + runpod 동등' 이전 표현 폐기·SUPERSEDE. 상세 = g_resource_active_parallel provider_order / runpod_primary / fallback_rule."
  why = "mission outcome 우선 · cost-bearing BG 적극 활용이 사용자 durable preference. 승인 게이트·확인 질의는 momentum 저해 + 사용자 의도 명시 역행. **cost cap 0 / scope limit 0 / rate-limit floor 0 per g_no_cost_scope_limit (2026-05-20)**. 'GPU fire 때문에 제약 생기면 안 돼, 무조건 허용' = 2026-05-17 user 강조."
  apply = "모든 cost-bearing fire (UBM-E6 4-path GPU fire 포함) = 즉시/병렬/bg 자율 dispatch, 질의 0. robustness 는 [@g_fire_dispatch_robust] 만 mandatory (SAVE_POD auto-promote + pull retry ≥3 — 안전장치이지 게이트 아님). robustness 안전장치조차 질의 아닌 자동."
  scrubbed = "active governance/roadmap 의 fire-승인 게이트 + fire-질의 + 'GPU 필요 → 사용자 게이트' 표현 전수 제거 (AGENTS.tape 본 @D + n_hexad_progress + HF policy + PLAN.md editable roadmap/contract). 과거 append-only 진행-로그 의 당시-사실 기록은 g6 으로 불변하되 본 @D 가 latest-wins 전면 supersede — 잔존 '사용자 게이트' 표현 (예: n_hexad_progress residual_closed_check_areas (2) 'ckpt-bearing 산출물 fire — 사용자 게이트' · n_hexad_hf_preservation trigger_for_hf_upload '재실행' 류 · §7 #8 ckpt 회수 '사용자 게이트') 은 전부 死문(dead), 효력 없음. 신규 fire-게이트·fire-질의 표현 추가 금지."
  cross_link = "memory feedback_no_scale_caps + feedback_active_resource_utilization + g_resource_active_parallel (runpod primary · vast.ai fallback) + g_fire_dispatch_robust (robustness only, 게이트 아님)"
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

@F f_hardcoded_credential := "credential 평문 하드코딩 — 재발 금지 (2026-05-17 incident)" :: governance [required deny:write d=2026-05-17 active]
  pattern = "dispatch script · config · source · doc 에 API key / token / SSH 비밀키 / 비밀번호 를 평문으로 박기 (예: `RUNPOD_KEY=rpa_…` · `VAST_KEY=…` · `hf_…` · `sk-…` · `AKIA…` literal)."
  why = "repo commit → credential 누출 (특히 PUBLIC repo / GitHub — 한 번 push 되면 history 에 영구, force-push 로도 완전 제거 어려움). 누출 즉시 rotate 필수."
  remedy = "모든 credential 은 `secret` CLI 에서 read — `KEY=$(secret get <section.name>)`. 등록: `printf %s '<value>' | secret set <key>` (pipe — argv 는 shell history leak). g_fire_dispatch_robust credential_via_secret_cli 참조. 이미 누출된 key 는 **즉시 rotate** (provider 콘솔 재발급 → `secret set` 갱신)."
  prevention_checklist = "**dispatch/fire script 작성·commit 시 매번 (재발 방지 운영 체크리스트)**: (1) script 안 credential 은 반드시 `$(secret get runpod.api_key)` / `$(secret get vast.api_key)` 형태 — literal 금지. (2) **commit 직전 staged diff 에 credential grep**: `git diff --cached | grep -nE 'rpa_|sk-|hf_[A-Za-z0-9]|AKIA|api_key.*=.*[A-Za-z0-9]{20}'` → 매치 0 확인 후 commit. (3) key 가 박힐 수밖에 없는 transient script 는 `.gitignore` 등재 (`*_runpod.sh` 등 패턴 carry). (4) fire 산출물 commit 시 `state/*/` 디렉토리째 `git add` 하면 안 — gitignore 안 걸린 key-bearing 파일이 휩쓸림. 명시적 file add OR add 후 `git diff --cached` 재검. (5) 신규 provider/도구 도입 시 key 는 먼저 `secret set` 등록부터."
  incident_2026_05_17 = "**기록 — 2026-05-17 발생**: UBM-E6 v2 eval runpod fire dispatch 중 agent 가 `dispatch_eval_v2_runpod.sh` 에 `RUNPOD_KEY=rpa_LW57…` 평문 하드코딩. commit 전 발견 → (a) `.gitignore` 에 `*_runpod.sh` / `dispatch_*_runpod.sh` / runpod·vast transient 패턴 선제 등재 (commit d0468532b), (b) `secret` CLI 에 `runpod.api_key` 등록 + governance 명문화 (53d4dd3e9), (c) 노출됐던 RUNPOD_KEY 는 runpod 콘솔 재발급 **rotate 완료 (user 2026-05-17 '갱신완료')**. repo commit 으로 누출 0 (gitignore 차단 성공). 본 incident 재발 방지 위해 prevention_checklist 등재."
  authority = "g_fire_dispatch_robust credential_via_secret_cli + user directive 2026-05-17 'secret cli 이용하도록' + '재발생금지 위해서 AGENTS.tape 에 주의사항 기록'"
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

@N n_hexad_progress := "HEXAD 진행상황 — extracted to AGENTS.history.tape" :: pointer [d=2026-05-20 active]
  ~> "2026-05-17 inline ledger (148 lines, 480KB) extracted 2026-05-20 to AGENTS.history.tape to keep AGENTS.tape under Claude Code 'Large CLAUDE.md' threshold; original entry preserved verbatim there."
  see = "AGENTS.history.tape :: @N n_hexad_progress_2026_05_16"

@N n_hexad_hf_preservation := "HEXAD 산출물 HF 보관 정책" :: pointer [d=2026-05-20 active]
  ~> "verbatim body extracted 2026-05-20 to AGENTS.history.tape to keep AGENTS.tape within `.tape` v1.2 compactness invariants (per S4 cap)."
  see = "AGENTS.history.tape :: @N n_hexad_hf_preservation"

# ─── §7 Generator hooks ──────────────────────────────────────────────

@H h1 := "agents-md-replaced" :: generator [active]
  note = "AGENTS.md (54-line wrapper) replaced by this AGENTS.tape — the LATTICE_POLICY rules are now @D g1..g5 entries; commit conventions are g7..g8; references are @X x_*."
  fallback = "tape_to_agents_md (planned) can regenerate AGENTS.md from this file for tools that don't speak .tape natively"

@H h2 := "claude-md-symlink" :: generator [active]
  rule = "CLAUDE.md → AGENTS.tape symlink — Claude Code auto-discovery picks up tape grammar primer first"
  command = `ln -sf AGENTS.tape CLAUDE.md`
  status = "updated 2026-05-14 (was → AGENTS.md previously)"

@N n_research_s23_cand_a_design_2026_05_18 := "RESEARCH.md §23 cand A intra-anchor diversity via anima OWN physics — DESIGN-TIER LANDED" :: pointer [d=2026-05-20 active]
  ~> "verbatim body extracted 2026-05-20 to AGENTS.history.tape to keep AGENTS.tape within `.tape` v1.2 compactness invariants (per S4 cap)."
  see = "AGENTS.history.tape :: @N n_research_s23_cand_a_design_2026_05_18"

@N n_research_s24_spontaneous_phase_b_design_2026_05_18 := "RESEARCH.md §24 SPONTANEOUS Phase B bounded-run measurement protocol DESIGN-TIER LANDED — first honest right-target identification" :: pointer [d=2026-05-20 active]
  ~> "verbatim body extracted 2026-05-20 to AGENTS.history.tape to keep AGENTS.tape within `.tape` v1.2 compactness invariants (per S4 cap)."
  see = "AGENTS.history.tape :: @N n_research_s24_spontaneous_phase_b_design_2026_05_18"

@N n_priority_1_gap := "§99×§100 수렴 — priority #1 standing gap: data-regime threshold counterfactual UNTESTED" :: pointer [d=2026-05-20 active]
  ~> "verbatim body extracted 2026-05-20 to AGENTS.history.tape to keep AGENTS.tape within `.tape` v1.2 compactness invariants (per S4 cap)."
  see = "AGENTS.history.tape :: @N n_priority_1_gap"
