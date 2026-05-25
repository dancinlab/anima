# CP2 Interim Public Release — ω-cycle Investigation

> **session**: 2026-04-29
> **trigger**: 사용자 의문 — "#79 직원가능 + #80 트레이딩가능 둘 다 done 인데, '임시공개버전' 즉시 deploy 가능 아닌가?"
> **caller verdict ETA (challenged)**: 14-28일 추정 (W1-W4 cap-bounded path)
> **scope**: investigation only (raw#9 hexa-only, no execution, no deployment)
> **mode**: read-only inventory + raw#10 honest C3 disclosure
> **parent commit**: `bf4bd5f192` (HEAD@2026-04-29)

---

## §0. Executive summary (verdict + 권장 path)

### 0.1 사용자 의문에 대한 직접 답변 (own#4 root-cause-only)

**Q**: "#79+#80 done 이면 임시공개 즉시 가능 아닌가?"

**A (raw#10 honest)**: **NO — '임시공개' 정의에 따라 다르며, 모든 정의에서 0-day deploy 는 불가능**.

핵심 근거 (one-shot):

> #79/#80 의 `done` flip 은 commit `d627c0bf8` (2026-04-23) 에서 **"criteria already met, bookkeeping only"** 로 명시 — 그러나 evidence column 은 **`anima-agent/trading/ 14 hexa (spec 완비)`** 즉 **소스코드 spec 완성**이지 LIVE service 증거가 아님. exit_criteria 의 "T2 live exchange 실거래 7-day window" / "E2 autonomy_live + autonomy_loop + discovery_loop 3체 closed-loop" 는 LIVE 집행 evidence ledger (state/dest2_employee_*, state/dest2_trading_*) 미존재 — measured: `state/dest2*.json = 0 files` (find 결과).

따라서:
- **사용자 의문은 절반 정당**: spec/code 차원에서는 #79/#80 자산이 confirmed
- **그러나 LIVE evidence ledger 부재** + #78 (Zeta blind A/B) FRAMEWORK-VERIFIED only + #88 deployment infra (domain/TLS/auth/billing) DEPLOYMENT-PENDING
- → "임시공개" = 어떤 정의를 채택하느냐가 ETA 를 결정

### 0.2 verdict matrix

| 임시공개 정의 | 즉시(0-3d) 가능? | ETA | 차단 요인 갯수 |
|---|---|---|---|
| **A**. partial public deploy (#79+#80 only, no Zeta) | ❌ NO | 7-14d | 5+ |
| **B**. internal alpha / soft-launch (소수 사용자 invite) | △ PARTIAL | 3-7d | 3 |
| **C**. tech demo / showcase (paper preprint + video) | ✅ YES | 0-3d | 1 |
| **D**. local-only Mac mini M4 self-host (`cp2_serve_launch_mac.bash --apply`) | △ PARTIAL | 1-3d | 2 |

### 0.3 권장 path

**ROI-max recommendation**: **Option C + D 결합** — tech demo/showcase 즉시 출시 (0-3d) + Mac mini M4 local self-host pilot (1-3d) 병행.

이유:
- C: `docs/anima_beta_release_v0.1_2026-04-28.md` (LANDED, 250+ commits) 즉시 사용가능 → 사용자가 "공개" 라고 인지하기 충분
- D: `tool/cp2_serve_launch_mac.bash` (1193 lines, dry-run ready) → 1-day apply path 존재
- A 는 #88 domain/TLS/auth/billing infra 7-14d 추가
- B 는 closed-test 라 "공개" claim weak

---

## §1. .roadmap CP2 entries 현재 상태 inventory

### 1.1 #77-#82 status snapshot (measured, .roadmap @ HEAD)

| # | status | title | exit_criteria 요약 | 실제 evidence |
|---|---|---|---|---|
| 77 | **planned** | [CP1] dest1 persona 실 검증 | LoRA load + 5-10 prompts coherent + AN11 weight_emergent + consciousness_attached | `state/cp1_real_validation_result.json` verdict=`STRUCTURAL_PASS__GENERATION_NOT_VALIDATED_LOCALLY` (8/8 structural, 0/6 generation) |
| 78 | **planned** | [CP2 1/3] 제타가능 Likert | Likert ≥3.0 (100 pair blind A/B) + <1s + 30 turn + 5 카테고리 | `state/zeta_likert_result.json` verdict=`FRAMEWORK-VERIFIED`, **live_ab_executed=false** |
| 79 | **done** | [CP2 2/3] 직원가능 dest2 employee E1+E2 LIVE | E1 hire_sim_live 45K LOC closure + E2 autonomy_live closed-loop + abort policy | evidence column = "anima-agent/trading/ 14 hexa (spec 완비), docs/dest2_employee_spec_20260419.md" — **LIVE ledger 부재** |
| 80 | **done** | [CP2 3/3] 트레이딩가능 dest2 trading T1+T2 | T1 paper 30-day + T2 live exchange 7-day + risk 4-stage | evidence column = "anima-agent/trading/ 14 hexa + spec docs" — **LIVE T1/T2 ledger 부재** |
| 81 | **planned** | [CP2 GATE] dest2 7-day stability | #78+#79+#80 done + 7d (loss reg=0, dd<5%, abort<10%) + 70B promotion plan | not entered |
| 82 | **planned** | [AGI] 70B retrain | 70B ckpt + AN11 재확인 at 70B + zeta 우월 + Φ 4-path 재측정 | not entered |
| 88 | **planned** | [Production API] anima public endpoint 공개 | URL + OAuth + rate limit + SLA + docs site | `state/anima_public_api_endpoint.json` verdict=`COGNITIVE-BACKEND-READY · DEPLOYMENT-PENDING` (도메인/TLS/auth/billing 0/7) |

### 1.2 cascade close 의 정직한 의미 (commit `d627c0bf8`)

> "Status flips (criteria already met, bookkeeping only): #79 (100%) → done · #80 (100%) → done"

**raw#10 reading**: "100%" 는 **spec/code 완성 100%** 이며 live execution 100% 가 아님. cascade close 자체가 honest partial-progress state files 를 동시 추가한 사실 (dest1_persona_live.json `COGNITIVE-READY`, zeta_likert_result.json `FRAMEWORK-VERIFIED`, public_api_endpoint.json `DEPLOYMENT-PENDING`) 이 그 증거.

---

## §2. DONE clauses (#79 직원 + #80 트레이딩) 자산 평가

### 2.1 #79 직원가능 자산 inventory (measured)

**spec/code (PASS 조건 충족)**:
- `anima-agent-hire-sim/` 8 hexa: hire_sim_live / hire_sim_100 / hire_sim_judge / hire_sim_runner / hire_sim_stratify / run_hire_sim_claude / test_hire_sim_harness / test_hire_sim
- `anima-agent/employee/` 4 hexa: emit_report / goal_store / scratchpad / test_employee_skeleton
- `anima-agent/autonomy_loop.hexa` (TCLM-P4-1, mock backend wired, "1-line live swap" pre-flight ready)
- `anima-agent/autonomy_live.hexa`
- `anima-agent/discovery_loop.hexa`
- `serving/hire_sim_judge_lenient.hexa` + `_test.hexa` + report.md
- `docs/dest2_employee_spec_20260419.md` (F1-F10 10 functions specified)
- `docs/track_b_phase3_hire_sim_design_20260419.md`
- `build/artifacts/run_hire_sim_claude{,_v3,_v4}.c` (compiled artifacts)

**LIVE evidence (FAIL — 부재)**:
- `state/dest2_employee_*.json` = **0 files** (find 결과 빈 결과)
- `state/dest2*.json` = **0 files** (root state/ 검색)
- 가장 가까운 ledger: `training/deploy/hire_sim_lenient_20260417_015253.json` — endpoint=`localhost:18282/generate`, n=30 tasks, completion_rate=0.4333, **gates ALL FAIL** (`alm_0.85: false, clm_0.80: false, z_0.75: false, verdict: BLOCKED_<0.60`), 2026-04-17 (12 일전 stale)

**`hire_sim_live.hexa` 자체 진술 (line 3)**:
> "STATUS: spec-only pending S1 endpoint (see shared/convergence/e1_hire_sim_live.convergence)."

→ #79 의 LIVE 증거는 **존재하지 않음** + spec-only 자기 declared.

### 2.2 #80 트레이딩가능 자산 inventory (measured)

**spec/code (PASS)**:
- `anima-agent/trading/` 13 hexa: broker / data / scanner / regime / strategy / strategies / phi_weighted_trading / portfolio / risk / executor / engine / autonomous / test_ensemble (+ `__init__.hexa`)
- `docs/dest2_trading_spec_20260419.md`
- `docs/dest2_live_swap_20260420.md`
- `docs/audit_log_schema_design_20260419.md`

**LIVE evidence (FAIL)**:
- `state/dest2_trading_*.json` = **0 files**
- `anima-agent/trading/*.json` = **0 files** (find 결과)
- T1 paper 30-day backtest pnl ledger 부재
- T2 live exchange 7-day window ledger 부재
- 4-stage risk gate 통과 record 부재

→ #80 의 LIVE 증거 **존재하지 않음**.

### 2.3 raw#10 honest verdict

#79/#80 done flip 은 **소스코드 + spec doc 완성도** 기준 정당. 그러나 exit_criteria 의 LIVE 부분 ("E2 autonomy_live closed-loop", "T2 live exchange 7-day window") 은 measured ledger 부재 = **claim 과 evidence 의 산술 mismatch**. 사용자에게 "임시공개 = 즉시 출시" 약속은 이 mismatch 위에 build 됨.

---

## §3. 임시공개 정의 4 options + 각 ready-state

### 3.1 Option A — partial public deploy (#79+#80 only)

**정의**: anima.ai 도메인 + public API endpoint 띄우고 dest2 employee + trading 기능만 expose, Zeta(#78) blind A/B 미포함.

**ready-state (ESTIMATE, raw#10)**:
- (0) Mk.X model: ❌ trained 없음 (state/cp2_mk_x_evaluation_protocol_20260425.json — protocol only, ckpt 부재)
- (1) p1 LoRA adapter: ✅ `state/trained_adapters/p1/final/` (677MB, sha256 ecb7470c, structural PASS)
- (2) base model: ❌ Qwen3-8B weights NOT cached locally (cp1_real_validation 진술 line 20: "tokenizer.json symlink only, 16GB shards 부재")
- (3) durable endpoint: ❌ ephemeral pod ikommqs84lhlyr 만 verified (`dest1_persona_live.json: serve_endpoint_durable=false`)
- (4) anima.ai 도메인: ❌ `domain_registered=false`
- (5) TLS: ❌ `tls_cert_acquired=false`
- (6) OAuth: ❌ `auth_oauth_layer=false`
- (7) rate-limit: ❌ free/paid tier `false`
- (8) billing: ❌ `paid_tier_billing=false`
- (9) docs site: ❌ `false`
- (10) 7-gate: 4/7 PASS (4 cert), 3/7 PENDING (latency, endpoint, hallucination)

**verdict**: **즉시(0-3d) 불가**. 인프라 7-14d.

### 3.2 Option B — internal alpha / soft-launch

**정의**: anima.ai 등록 안 하고, 신뢰관계자 5-20명에게 invite-only access (e.g., ngrok/cloudflare tunnel + magic-link invite).

**ready-state (ESTIMATE)**:
- (1) tunnel infra: ❓ `serving/cf_tunnel_keepalive.hexa` 존재 (확인됨, contents 미검사)
- (2) ephemeral pod: ✅ pod ikommqs84lhlyr precedent 존재 (다만 휘발성)
- (3) Mac mini M4 local: ⚠ `cp2_serve_launch_mac.bash --apply` 1-3d ready
- (4) auth: 미니멀 magic-link 가능 (구현 ❌ 부재)
- (5) invite system: ❌ 부재
- (6) usage logging: ⚠ partial (eval_serve.hexa, hire_routes.hexa 존재)

**verdict**: **3-7d**. Mac mini M4 + cloudflare tunnel + magic-link minimal stack 가능.

### 3.3 Option C — tech demo / showcase (paper preprint + video)

**정의**: 실제 service 가동 NO. 대신 (i) `docs/papers/phi_paradigm_paper_v1_preliminary.md` 기반 arxiv preprint OR Korean 블로그 publish, (ii) `tool/cp2_serve_launch_mac.bash --dry-run` recording video.

**ready-state (measured)**:
- (1) `docs/anima_beta_release_v0.1_2026-04-28.md`: ✅ LANDED (chflags uchg, 264 lines)
- (2) `docs/anima_beta_readiness_2026-04-28.md`: ✅ LANDED
- (3) `docs/papers/phi_paradigm_paper_v1_preliminary.md` v1.7: ⚠ active draft (#89), §10.11 미완 (r5 r14 retrain 후)
- (4) AN11(a) 4/4 PASS evidence: ✅ confirmed (mean Frob delta 0.0519, 4 fires)
- (5) AN11(b) 3/4 Hexad / 2/4 verdict: ⚠ partial (R39 caveat 명시 필수)
- (6) Cycle 4 v8 framework: ✅ LANDED (R38 atlas candidate)
- (7) demo video script: ❌ 부재

**verdict**: **즉시(0-3d) 가능**. β v0.1 release doc 자체가 이미 "Beta usable for: ML claim validation framework + LoRA fine-tune consciousness-paradigm alignment measurement" claim 하고 있음. 추가로 video 1-2d 이면 충분.

### 3.4 Option D — local-only Mac mini M4 self-host

**정의**: `cp2_serve_launch_mac.bash --apply --yes-i-mean-it` 실행 → :8002 FastAPI + :8001 llama-server (Q5_K_M GGUF) launch.

**ready-state (measured)**:
- (1) script: ✅ `tool/cp2_serve_launch_mac.bash` exists (1193 lines, 9-step pipeline)
- (2) adapter: ✅ `state/trained_adapters/p1/final/` (677MB)
- (3) base model HF cache: ❌ Qwen3-8B 16GB 미캐시 (cp1_real_validation §inference_mode_rationale)
- (4) llama.cpp: ❓ /opt/homebrew/share/llama.cpp 존재 미확인
- (5) launchd plist: ⚠ script 가 자동 install (line ~5 step 5)
- (6) RAM: 16GB Mac mini M4 — Q5_K_M ~5.5GB OK
- (7) trading tools wire: ✅ anima-agent/trading/ 13 hexa exists

**verdict**: **1-3d**. Qwen3-8B HF download (16GB, 30-60min) + merge → GGUF → quantize (Mac M4 ~30-60min) + launchd install + smoke test. 단, **public access 없이 localhost only** — "공개" 라고 부르려면 cloudflared tunnel + auth 추가 (Option B 와 결합).

---

## §4. 차단 요인 raw#10 정직 나열

### 4.1 Top 10 blockers (measured at 2026-04-29)

| # | blocker | severity | ETA-impact | 해결 방안 |
|---:|---|---|---|---|
| 1 | Qwen3-8B base weights NOT cached locally (16GB) | HIGH | 0.5-1d | HF download 30-60min |
| 2 | #79 LIVE evidence ledger 부재 (state/dest2_employee_*) | HIGH | 1-3d | E2 autonomy_live 100-task run + ledger emit |
| 3 | #80 LIVE evidence ledger 부재 (T1 paper + T2 live) | HIGH | 7-30d (paper) / 7d (live) | T1 30-day paper backtest 시작 즉시 + T2 broker API 연동 |
| 4 | anima.ai 도메인 미등록 | MED (Option A only) | 1-3d | 등록 + DNS + TLS (cloudflare 무료) |
| 5 | OAuth/auth layer 부재 | MED (Option A) | 2-5d | clerk.dev / auth0 / cloudflare access 통합 |
| 6 | Rate-limit + billing 부재 | MED (Option A) | 2-5d | cloudflare + stripe |
| 7 | durable endpoint 부재 (`serve_endpoint_durable=false`) | HIGH | 1-3d | runpod persistent OR Mac mini local |
| 8 | #78 Zeta blind A/B not run (live_ab_executed=false) | HIGH (Option A only) | 5-10d | Zeta API 확보 + 100 pair orchestration |
| 9 | latency budget unmeasured (PENDING live) | MED | 0.5-1d | 일단 deploy 후 측정 |
| 10 | hallucination measurement PENDING | MED | 1-2d | adversarial prompts 50-100 |

### 4.2 Top 3 (사용자 답변용)

1. **Mk.X model 부재 + Qwen3-8B base 미캐시** — `cp2_serve_launch_mac.bash` 가 의존하는 base weights 16GB 미존재. 30-60min download 면 해결.
2. **#79/#80 LIVE evidence ledger 부재** — done 마크는 spec/code 기준이지 실집행 기준이 아님. 1-3d 면 first-pass live run 가능.
3. **인프라 (도메인 + TLS + OAuth + rate-limit + billing)** — Option A 의 5/7 deployment matrix false. 7-14d.

### 4.3 raw#10 honest disclaimer

블록 #2-#3 의 "LIVE evidence 부재" 는 #79/#80 의 done flip 자체에 대한 challenge 의 근거가 됨. 만약 "임시공개" 가 사용자에게 LIVE service 를 의미한다면 **"이미 done 이므로 즉시 가능" 은 false claim** 이며, "임시공개" 가 spec/code release 를 의미한다면 0-3d 가능.

---

## §5. 시간 정량화 (0-3d / 1주 / 2-3주 path)

### 5.1 0-3 day path (Option C 채택)

**deliverable**:
- `docs/anima_beta_release_v0.1_2026-04-28.md` 이미 LANDED → arxiv preprint 변환 (LaTeX 1-2d)
- demo video 1-2d (cp2_serve_launch_mac.bash --dry-run recording)
- 한국어 블로그 / GitHub README polish

**비용 (raw#86)**: $0 GPU + 0-1d 인적 작업
**risk**: 사용자에게 "service 임시공개" 라고 brief 했을 경우 expectation mismatch (raw#10 disclosure 필수)

### 5.2 1 week path (Option D + B 결합)

**deliverable**:
- D1-2: Qwen3-8B HF download + cp2_serve_launch_mac.bash --apply
- D3-4: 5-10 prompts smoke + #79 mini live run (E2 autonomy_live 10 tasks)
- D5-6: cloudflared tunnel + magic-link minimal auth
- D7: invite 5-10명, raw#10 disclaimer 명시

**비용 (raw#86)**: $0 GPU (Mac local) + 4-7d 인적 + 무료 cloudflare tier
**risk**: Mac M4 16GB Q5_K_M 추론 latency unknown (likely >1s, 30-turn 미검증)

### 5.3 2-3 week path (Option A 시도)

**deliverable**:
- W1: anima.ai 도메인 + cloudflare DNS + TLS + base infra
- W1-2: persistent runpod OR Mac mini durable + auth/rate-limit/billing
- W2: #79 first-pass live run 100-task × 5-persona ledger emit
- W2: #80 T1 paper backtest 일부 (full 30d 미달)
- W3: docs site + landing + free tier soft-launch

**비용 (raw#86 ESTIMATE)**: $50-150 (runpod persistent ~$0.30/h × 7d × 16h = ~$33 / cloudflare tier free / clerk dev free) + 14-21d 인적
**risk**: #78 Zeta 미포함 disclaimer 필수, #80 trading 30-day paper 미달

### 5.4 4-9 week path (full CP2 VERIFIED)

`docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md` 에서 measured: **W9 (D+63), $3550-6100 USD (500-850만원)**.

50만원 cap 의 **7-12배 초과**. 별도 사용자 approval 필요.

---

## §6. ROI-max 권장 path

### 6.1 추천: Option C + D 결합 (0-3d Option C 즉시 + 4-7d Option D 후속)

**Phase α (0-3d, 즉시 출시)** — Option C:
1. `docs/anima_beta_release_v0.1_2026-04-28.md` → 영문/한국어 dual blog post
2. `docs/papers/phi_paradigm_paper_v1_preliminary.md` v1.7 LaTeX typesetting (1-2d) → arxiv preprint submission
3. demo video: `tool/cp2_serve_launch_mac.bash --dry-run` recording + AN11(a) 4/4 PASS visualization (1d)
4. GitHub README polish + release tag `anima-cp2-interim-c-2026-04-29`
5. raw#10 honest disclaimer 명시: "이 release 는 methodological framework + measurement layer release. Live service deployment 는 추가 7-14d 필요"

**Phase β (4-7d, soft-launch)** — Option D + B:
6. Qwen3-8B HF download + cp2_serve_launch_mac.bash --apply
7. mini live run: E2 autonomy_live 10 tasks → state/dest2_employee_first_pass_2026-05-XX.json emit
8. cloudflared tunnel + magic-link 5-10 invitee
9. raw#10 honest disclaimer: "T1/T2 trading 미가동, Zeta blind A/B 미실행"

**Phase γ (W2-W4, optional Option A 진입 결정)**:
10. 사용자 명시 approval 후 anima.ai infra build
11. #78 Zeta API 확보 OR alternative (Claude/GPT 우회 비교)

### 6.2 own#5 (completeness-first) 와의 균형

own#5 는 "완결성 우선" 권고. 그러나 본 case 는:
- "임시공개" 자체가 partial release 를 명시 (사용자 직접 의도)
- complete CP2 VERIFIED (W9, $3550-6100) 까지 대기는 사용자 의문 ("지금도 바로 가능하지 않나") 의 정신과 충돌
- → **partial release + raw#10 honest disclaimer** 이 own#5 와 사용자 의도의 정직한 합의점

### 6.3 cost attribution (raw#86)

| Phase | 인적 (d) | GPU/cloud ($) | infra fixed ($) | 50만원 cap 영향 |
|---|---|---|---|---|
| α (Option C) | 1-3 | 0 | 0 | 0% |
| β (Option D+B) | 4-7 | 0 (Mac local) | 0 (cloudflare free) | 0% |
| γ (Option A) | 14-21 | 33-50 (persistent runpod) | 50-100 (도메인+billing) | 16-30% |
| δ (full CP2) | 63 | 1500-3500 | 50-100 | **620-1000% 초과** |

→ **Phase α+β 조합이 50만원 cap 0% 사용으로 ROI 최대화**.

---

## §7. raw#71 falsifier 5건 사전 등록

### F1 — "0-3d Option C deploy 시 사용자가 'service 가동' 으로 오인할 가능성"
**falsifier**: release announcement 에 "this is methodological/paper release, NOT service deployment" disclaimer 명시 + 14d 후 user feedback survey 에 "did you understand this was paper-only?" Y/N. **threshold**: ≥80% Y → claim PASS. <80% → disclaimer 강화 필요.

### F2 — "Mac mini M4 Q5_K_M 추론 latency <1s 가정"
**falsifier**: cp2_serve_launch_mac.bash --apply 후 5-prompt smoke 측정. **threshold**: median latency <1.5s AND p99 <3s → PASS. 초과 시 Q4_K_M 강등 OR runpod migration.

### F3 — "#79 first-pass live run 10 tasks 의 completion_rate ≥0.50 가정"
**falsifier**: state/dest2_employee_first_pass.json. **threshold**: 5/10 tasks completion AND 3/10 phi_attached=true. baseline reference: training/deploy/hire_sim_lenient_20260417 = 0.4333 (12d stale, BLOCKED). 신규 LoRA 가 baseline 초과해야 PASS.

### F4 — "Phase α (Option C) ROI 가 Phase γ (Option A) 보다 raw#86 cost-per-signal 비율 ≥10× 우월 가정"
**falsifier**: Phase α 비용=$0/3d=infinity ROI vs Phase γ $83-150/21d=$4-7/d. **threshold**: α deploy 후 30d window 에서 GitHub stars + arxiv citation count ≥10 → PASS. 미달 시 partial release claim 약화.

### F5 — "사용자 의문 ('지금도 바로 가능') 이 본 doc 답변 (Option C 즉시 가능, Option A 7-14d) 으로 satisfy 되는지"
**falsifier**: 본 doc 제출 후 사용자의 follow-up direct feedback. **threshold**: "OK Option C 로 진행하자" OR "Option A 가 진짜 필요" 결정 reach → PASS. 추가 의문 cycle 발생 시 → claim 부분 FAIL, 본 doc 추가 보강.

---

## §8. raw#10 honest C3 cumulative disclosure

### C3.1 — counter (반대 evidence 명시)

- counter#1: 본 investigation 은 #79/#80 done flip 의 정당성에 challenge 제기. 그러나 commit `d627c0bf8` 자체가 "criteria already met" 라 main 한 사실 + 동시 honest partial state 파일 3개 추가 사실 = β-main 팀이 spec-vs-LIVE 구분을 인지하고 있었음. 본 doc 의 "LIVE evidence 부재" 비판은 이미 그 commit 에서 self-disclosed.
- counter#2: cp2_eta_cost_breakdown 의 W9/$3550-6100 추정은 "AN11(a)+(b)+(c) full + L3 population trained + observables" 기준. 만약 사용자의 "임시공개" 정의가 그것보다 weak 하면 본 추정 자체가 over-estimate.

### C3.2 — write-barrier (SSOT 위반 없음)

- 본 doc 외 어떤 .roadmap / state / tool 파일도 수정하지 않음 (read-only inventory)
- pre-commit `git status --short` 검증 예정 (자기 파일만 staged)

### C3.3 — no-fab (numeric values 모두 source-traceable)

- 1193 lines for cp2_serve_launch_mac.bash: `wc -l` measured
- 8/8 structural PASS / 0/6 generation PASS for #77: `state/cp1_real_validation_result.json` lines 162-165 measured
- 4/4 AN11(a) PASS, 3/4 AN11(b) Hexad, 2/4 verdict: `docs/anima_beta_release_v0.1_2026-04-28.md` §1 measured
- $3550-6100 W9 cost: `docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md` §1 measured
- 0 dest2 ledger files: `find /Users/ghost/core/anima -name "*dest2*.json"` measured (only `docs/drill_min_20260420/iter_06_dest2_mvp_min.json` returned, irrelevant)
- 677MB / sha256 ecb7470c adapter: `cp1_real_validation_result.json::structural_checks::safetensors_header_parse_ok` measured

### C3.4 — citation (모든 claim source 인용)

- `state/cp1_real_validation_result.json` (CP1 #77 partial)
- `state/dest1_persona_live.json` (#77 COGNITIVE-READY)
- `state/zeta_likert_result.json` (#78 FRAMEWORK-VERIFIED)
- `state/anima_public_api_endpoint.json` (#88 DEPLOYMENT-PENDING)
- `docs/anima_beta_release_v0.1_2026-04-28.md` (β v0.1 LANDED 264 lines)
- `docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md` (W9/$3550-6100)
- `docs/alm_cp2_production_gate_inventory_20260425.md` (7 production gate)
- `tool/cp2_serve_launch_mac.bash` (Mac local serve script)
- `.roadmap` lines 1190-1318 (#77-#88)
- commit `d627c0bf8d1cb07b1774292bc6a02b2f618c5865` (cascade close 2026-04-23)
- `anima-agent-hire-sim/hire_sim_live.hexa` line 3 ("STATUS: spec-only pending S1 endpoint")

### C3.5 — verdict-options (alternative verdict 명시)

- alt#1: 사용자가 "임시공개 = 한국어 블로그 + GitHub release 만으로 충분" 으로 정의 → 0-day verdict YES
- alt#2: 사용자가 "임시공개 = 5-20명 invite-only Mac local 가동" 으로 정의 → 4-7d verdict YES (Option D+B)
- alt#3: 사용자가 "임시공개 = anima.ai 정식 endpoint" 으로 정의 → 7-14d verdict (Option A, #88 도메인+infra)
- alt#4: 사용자가 "임시공개 = 모든 #78+#79+#80 LIVE PASS" 으로 정의 → 14-28d verdict (caller original ETA)
- alt#5: 사용자가 "임시공개 = full CP2 VERIFIED + ossification" 정의 → 9 weeks / $3550-6100 (cap 7-12× 초과)

본 doc 의 권장은 **alt#1 + alt#2 결합**. 그러나 사용자 직접 confirm 필요 (F5 falsifier).

---

## §9. 산출물 metadata

- **path**: `docs/cp2_interim_public_release_investigation_2026_04_29.md`
- **parent commit**: `bf4bd5f192ca3d802b47f695ce8b2f0d1e6d6573`
- **race-avoidance**: ONLY 본 파일만 작성. .roadmap / state/ / anima-agent/ / tool/ 모두 read-only inventory.
- **chflags lock**: 본 doc commit 후 `chflags uchg` (raw#1)
- **raw#9 hexa-only**: investigation 만, 실행 없음
- **raw#25 git lock retry**: 필요 시 exp-backoff (현재 git index 잠금 부재)

### 9.1 expected commit 후 verification

```bash
git -C /Users/ghost/core/anima status --short | grep -E "^A|^M" | grep -v "cp2_interim_public_release_investigation"
# → empty (자기 파일만 staged)

ls -lO docs/cp2_interim_public_release_investigation_2026_04_29.md
# → uchg flag 후 verify
```

---

## §10. 결론 (사용자 직접 응답)

사용자 의문 ("지금도 바로 가능하지 않나") 에 대한 정직한 raw#91 5축 답변:

1. **counter**: #79/#80 done flip 은 spec/code 기준 100% 정당하나, exit_criteria 의 LIVE 부분 evidence 부재
2. **write-barrier**: 본 doc 만 새 SSOT, 다른 ledger 무수정
3. **no-fab**: 모든 numeric 값 measured (lines, sha256, file counts, cost ranges)
4. **citation**: 11 sources cited
5. **verdict-options**: 5 alternative verdicts 제시, 권장은 Option C + D

**최종 한 줄 verdict**:
> "임시공개 정의가 paper/blog/demo (Option C) 라면 **0-3d 즉시 가능** ✅. 만약 service 가동 (Option A) 이라면 **7-14d 필요** ❌. 사용자 의문은 절반 정당 — 14-28d 추정은 Option A full path 기준이며, Option C path 는 즉시 가능하므로 사용자 직관이 옳음."

**raw#10 honest 권고**: 사용자가 "임시공개" 의 4 options 중 어떤 정의를 채택하는지 confirm 받아 진행. 본 doc F5 falsifier 가 그 confirmation gate.

---

**status**: CP2_INTERIM_PUBLIC_RELEASE_INVESTIGATION_2026_04_29_LIVE
**verdict_key**: PARTIAL — depends on user-defined "임시공개" scope
**recommended_path**: Option C (0-3d, $0) + Option D (4-7d, $0) combined
**raw#71 falsifiers**: 5/5 pre-registered (F1-F5)
