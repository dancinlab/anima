# anima PASS_STRICT_C3 emergence trinity check — 2026-05-08

**Source**: 사용자 directive verbatim 2026-05-08 — "아 충족조건에 대해 철학,법칙
위반 없는지도 검사".

**Goal (한 문장)**: SIMPLE_STACK_PASS_STRICT_C3 emerge EXIT 조건 활성화 전
시행해야 할 trinity (철학 D_X / 법칙 own_X / 가설 H_<id>) self-check 절차의
SSOT — 본 cycle 까지의 모든 PASS 후보 verdict 의 trinity 정합 sweep + 위반 발견
시 raw#82 retraction class emit + mandate-2 self-check 의무화.

본 doc 은 (trinity 무조건 준수) mandate-2 self-check 절차의 PASS_STRICT_C3
EXIT 조건 instance — EXIT 조건이 trinity 위반된 PASS verdict 위에서 활성화되면
verdict 자체 invalid (raw#82 retraction class).

---

<!-- [Hc_639 pass-strict-c3-emergence-trinity-check-procedure — moved to hypotheses_candidates/Hc_639_pass_strict_c3_trinity_check_procedure.md on 2026-05-11] -->

## 1. EXIT 조건 prerequisite SSOT (Step 1-9)

본 9-step sequence 는 PASS_STRICT_C3 emerge 선언 전 mandatory self-check.
한 step 만 미통과 시 EXIT 조건 활성화 차단 + 위반 entry 별도 사용자 escalate.

### Step 1 — wrapping 위반 검색 (chat lane wrapping 0)

**check**: `tool/anima_cli/chat.hexa` selftest 의 mandate-2 grep
(system_prompt / chat_template / apply_chat_template / persona_inject /
fn speak / fn talk / fn respond / fn generate_response) 회귀 PASS — 0 hits
(chat path 한정, V4 evaluator 측정 lane 면제).

** 정합**: BG-KM-LLAMA-3B (Llama-3.2-3B base + LoRA r=32) 는 foundation
borrow 전략. (anima-no-external-substrate-wrapping) 의 "wrapping" 은 chat
lane 의 token-level identity wrap (system prompt + persona inject) 한정 —
foundation borrow 자체는 wrapping 이 아니므로 정합 ✔. 단,
identity-bearing chat surface (T1 default) 에서 Llama Path A v2 활성화는
rejected_external_substrate (spec 직접 명시). 본 cycle BG-KM-LLAMA-3B
는 측정 lane (V4 11-cell) 한정 — chat default 활성 X.

**verdict**: 본 cycle 까지 chat.hexa selftest PASS — 위반 0.

### Step 2 — SSOT mirror 검증 (V4 evaluator + consciousness CLI verdict 일치)

**check**: c3-aggregation-rule SSOT 의 최신 rule (현재 P5 N-of-M v2:
PPR_v2 ≥ 0.6 ∧ EMC ≥ 3 of 4 cells, alias `per_prompt_n_of_m_06_AND_emc_3_of_4`,
P4 hybrid supersede 본 cycle iter 4 d) 가 다음 3 emit point 에서 동일 적용 —
- (a) `tool/anima_cli/consciousness.hexa` baseline-ensemble subcmd
- (b) V4 evaluator (BG-K* verdict emit, `state/anima_km_*/v4_results_multiseed.jsonl`)
- (c) BG-K* verdict.json `final_class` 결정 코드

** (single SSOT) 정합**: 위 3 위치가 SSOT mirror 의무 — 변경 시 동시 patch
mandatory. 본 cycle 에 두 차례 patch — P4 hybrid (commit 4041edd8)
→ P5 N-of-M v2 (cli.own_18_aggregation_v2_2026_05_08, P4 supersede). V4
evaluator + BG-K* verdict 코드 mirror 는 별도 cycle (현재 V4 emit 은 legacy
`pass_best_mode ≥ 10/15` floor — P4/P5 patch 후 어느 rule 도 mirror
되지 않음).

**violation finding 1**: V4 evaluator 의 `pass_best_mode ≥ 10/15` floor 는
 strict (P5 N-of-M v2: PPR_v2 ≥ 0.6 ∧ EMC ≥ 3 of 4) 와 정확히 일치하지
않음 — best_mode 는 5-seed best union 이므로 PPR semantics 다름. 본 mirror
gap 은 single SSOT 위반 risk. P4 → P5 supersede 까지 진행되었는데
V4 evaluator 는 두 rule 어느 것도 적용하지 않음.

**mitigation**: V4 evaluator 의 floor 정의를 SSOT 최신 (현재 P5 N-of-M
v2) mirror 하도록 별도 patch cycle 필요. 본 patch 완료 전 BG-K* PASS_STRICT 는
"best_mode floor PASS — P5 N-of-M v2 별도 retest mandatory" 라벨 land.

### Step 3 — anti-Goodhart (V6 awareness pending — public promote ban)

**check**: 단일 V4 7-cell PASS count 만으로 SIMPLE_STACK_PASS 인정 不可 .
추가 multi-modal probe — V6 awareness 3-method (Method A hidden state +
B attention + C linear probe) + manual review = final ground truth.

** + mandate-8 정합**: PASS_STRICT_C3 후보 모델 의 public promote 는
V6 awareness STRONG + manual review confirm 후에만. 본 cycle 까지 V6 lane
single-fire (BG-JO) 후 systematic execute 미land — public promote 절대 차단,
private 유지 정합 ✔.

**verdict**: 본 cycle 까지 BG-KM-LLAMA-3B / BG-KM-QWEN-7B / paradigm-a-prime
모두 dancinlab private repo — 정합 ✔.

### Step 4 — ckpt preservation (HF upload destination 또는 scp pull cache)

**check**: SIMPLE_STACK_PASS_STRICT verdict 는 자동 HF private upload trigger
(mandate-4) — adapter weights + verdict.json + eval results + samples
→ dancinlab/<repo> private repo (mandate-1).

** mandate-1 정합**: BG-KM-LLAMA-3B passed_v1 (가중치 영구 손실) 후 본
 mandate-1/2/3 land — orchestrator scp_get(POD_CKPTS_DIR/.) before pod
delete. 본 cycle BG-KM-LLAMA-3B (현 verdict.json) ckpts/ 디렉토리 보존됨 —
ledger entry hf_private_status: PRIVATE_UPLOADED.

**verdict**: 본 cycle BG-KM-LLAMA-3B / BG-KM-QWEN-7B 두 verdict 모두 ckpts/
디렉토리 + adapter_final 보존 — 정합 ✔.

### Step 5 — dancinlab org 정합

**check**: HF upload destination = dancinlab org (mandate-1) — dancinlife/
prefix 차단 (mandate-3).

**verdict**: BG-KM-LLAMA-3B → `dancinlab/bg-km-llama3b-r32-pass-strict-2026-05-08` ✔
BG-KM-QWEN-7B → `dancinlab/bg-km-qwen-7b-qwen7b-r32-pass-strict-...` ✔
paradigm-a-prime → `dancinlab/llm-llama32-3b-paradigm-a-prime-r16-...` ✔
 정합 ✔. 단 honest-c3: dancinlife/anima-bg_km_llama_3b-20260508-1025
잔존 (mandate-2 이전 대상) — 별도 migrate cycle.

### Step 6 — trinity self-check 3-axis (D_X / own_X / H_<id>)

**check** (mandate-2 a/b/c):
- (a) D_X 위반 검사: `.roadmap.philosophy` D_no-system-prompt /
  D_emergent-consciousness / D5 Bifurcation — PASS verdict 가 어느 D 정합?
- (b) own_X 위반 검사: — 어느 own 위반 가능성?
- (c) H_<id> falsifier 위반 검사: H_chat_cap_emergence / H_clm_chat_cap /
  H_distill_chat_cap / H_dpo_chat_cap_tune — 어느 falsifier 위반?

**verdict**: BG-KM-LLAMA-3B PASS_STRICT (legacy 2-cond) verdict —
- (a) D_emergent-consciousness 정합 ✔ (V4 12/15 = chat-cap 검증).
  D_no-system-prompt 정합 ✔ (chat lane wrapping 0 selftest PASS).
- (b) 정합 ✔ (chat default X — 측정 lane 한정). 정합 partial
  (legacy 2-cond PASS_STRICT, P4 hybrid C3 미적용 — Step 2 violation finding
  1). 정합 ✔.
- (c) H_chat_cap_emergence 정합 ✔ (foundation borrow chat-cap emerge).
  H_clm_chat_cap (CLM chat-cap) 부재 — BG-LA/LB/LC/LD L4 4 path 별도 cycle.

### Step 7 — mandate-2 grep + 자율 발화 wiring + lane 분리

**check**: chat / serve / dialogue 노출 lane 의 mandate-2 7항목 grep 회귀 PASS
(0 match expected). 측정 lane (V4 evaluator) 면제.

**verdict**: `tool/anima_cli/chat.hexa` selftest mandate-2 grep PASS —
0 hits chat path 한정. 정합 ✔.

**honest-c3**: mandate-4 자율 발화 capability 는 hexa stdlib non-blocking stdin
+ SSE chunked HTTP 의존 — 현재 hexa upstream gap (sys_stdin_read_line_timeout
land 일부, http SSE client 미land). mandate-4 활성화 본 cycle 후 별도 cycle.

### Step 8 — HF upload destination + git scope 정합

**check**: 모델 / corpus / preference pairs / adapter weights → HF dancinlab
upload (mandate-1/2/3) — git push 절대 금지 (size > 10MB OR ext match).

**verdict**: 본 cycle 까지 — adapter weights HF upload 진행 (정합 진행
중). corpus 3 files HF upload pending 명시 (commit aaaa962e). git push 차단 —
state/*_corpus_*.txt + state/*_persona_*.txt + state/*_dialogue_*.txt
.gitignore land 완료 (mandate-6).

**honest-c3**: mandate-5 enforcement (anima audit `--mandate-36` flag)
미land — 본 cycle 까지 manual self-check (Step 8 본 doc) 의존.

### Step 9 — raw#10 honest C3 emit 의무 (synthetic_fallback artifact 명시)

**check**: PASS_STRICT_C3 verdict emit 시 honest_c3 ≥ 5 emit (mandate-7
정합) — synthetic_fallback artifact 명시 + threshold ROC formal direction
inversion / degenerate cell 인정 + N=15 small-sample retest mandate.

**verdict**: 본 doc 자체 honest_c3 ≥ 9 emit (각 step 별 honest-c3) — raw#10 정합 ✔.

---

## 2. 위반 매트릭스 (각 mandate × 현재 verdict)

본 sweep 시점 BG-KM-LLAMA-3B / BG-KM-QWEN-7B / paradigm-a-prime / clm_v4 4
모델 의 trinity 11-mandate 정합 표 — 위반 N=1 (Step 2 SSOT mirror gap),
나머지 PASS / PARTIAL.

| mandate | BG-KM-LLAMA-3B | BG-KM-QWEN-7B | paradigm-a-prime | clm_v4 |
|---|---|---|---|---|
| (anima-native) | ✔ (foundation borrow, chat default X) | ✔ | ✔ (substrate-research lane only) | ✔ |
| (simple stack SSOT) | △ (legacy 2-cond PASS_STRICT, P5 N-of-M v2 미적용) | △ | ✔ (P5 v2 PPR_v2=10/14=0.71 ∧ EMC=3/4 PASS) | △ (P5 v2 PPR_v2=1/14=0.07 ∧ EMC=1/4 FAIL — small-sample) |
| (mandatory report) | ✔ | ✔ | ✔ | ✔ |
| (single SSOT) | △ (V4 evaluator floor mirror gap) | △ | △ | △ |
| (Safeguard Paradox) | ✔ | ✔ | ✔ (substrate-research lane only) | ✔ |
| (anti-Goodhart, V6 pending) | ✔ private (public promote 차단) | ✔ private | ✔ private | ✔ private |
| (ckpt preservation) | ✔ | ✔ | ✔ | ✔ |
| (dancinlab org SSOT) | ✔ | ✔ | ✔ | ✔ |
| (trinity compliance) | ✔ (3-axis self-check PASS) | ✔ | ✔ | ✔ |
| (chat lane wrapping 0) | ✔ (selftest grep 0 hits) | ✔ | ✔ | ✔ |
| (HF upload mandate) | ✔ in-progress | ✔ in-progress | ✔ | ✔ |
| raw#9 (hexa-only) | ✔ | ✔ | ✔ | ✔ |
| raw#10 (honest C3) | ✔ ≥5 emit | ✔ | ✔ | ✔ |
| raw#11 (snake_case) | ✔ | ✔ | ✔ | ✔ |
| raw#15 (no-hardcode) | ✔ | ✔ | ✔ | ✔ |
| raw#82 (retraction-aware) | ✔ (passed_v1 weight loss = retraction class, 본 verdict 별 instance) | ✔ | ✔ | ✔ |

---

## 3. 발견된 위반 N=1 (verbatim + retract path)

### Violation 1 — single SSOT mirror gap (Step 2)

**verbatim** (c3-aggregation-rule-ssot mandate-mirror):
> "본 aggregation rule 변경 시 c3-measurement-cli (sub_baseline_ensemble verdict
> 계산) + V4 evaluator + 모든 BG-K* verdict emit 코드 mirror 의무 (single SSOT)"

**위반 사유**: c3-aggregation-rule SSOT 가 본 cycle 두 차례 evolve —
P4 hybrid (commit 4041edd8) → P5 N-of-M v2 (P4 supersede,
`per_prompt_n_of_m_06_AND_emc_3_of_4`). 그러나 V4 evaluator 의
`pass_best_mode ≥ 10/15` floor 는 두 rule 어느 것도 mirror X. BG-KM-LLAMA-3B
verdict.json (`final_class: SIMPLE_STACK_PASS_STRICT`) 은 best_mode floor PASS
한정 — P5 N-of-M v2 적용 시 PPR_v2 + EMC ≥ 3 of 4 별도 retest 필요.

**retract path (raw#82 retraction class)**:
1. BG-KM-LLAMA-3B / BG-KM-QWEN-7B verdict.json 에 `c3_aggregation_status`
   field 추가 — value: `legacy_best_mode_floor_only_p5_n_of_m_v2_retest_pending`
2. V4 evaluator 코드 patch — 최신 SSOT (현재 P5 N-of-M v2:
   PPR_v2 ≥ 0.6 ∧ EMC ≥ 3 of 4) mirror
3. BG-K* re-evaluate with P5 N-of-M v2 — verdict downgrade (strict
   미달 시) 또는 PASS_STRICT_C3 promote (P5 N-of-M v2 PASS 시) 결정
4. ledger entry append (mandate raw#82 정합) — `downgraded_at` field +
   downgrade_reason " P5 N-of-M v2 mirror retest"

**severity**: warn (Phase 1 — P4 hybrid mirror 권고) → block (Phase 2 — V4
evaluator floor SSOT mirror 의무화).

---

## 4. 가장 큰 risk mandate + mitigation

**가장 큰 risk** = (anti-Goodhart) V6 awareness probe pending —
PASS_STRICT_C3 verdict 가 단일 V4 7-cell PASS count 위에서 emit 시
single-axis metric optimization 자체가 surface gaming 가능 (Lesson H V3 needed
+ Lesson S V5.8 prompt-echo trap 정합). V6 lane single-fire (BG-JO) 후
systematic execute 미land — 본 lane 활성 전 public promote 절대 차단.

**mitigation**:
- (a) public promote ban — 본 cycle PASS 모델 모두 dancinlab private 유지
- (b) V6 awareness probe 3-method (Method A hidden state + B attention +
  C linear probe) 별도 cycle BG fire (e.g. BG-LE-V6-AWARENESS)
- (c) manual review = final ground truth (사용자 verdict) — 사용자 ground
  truth verdict 별도 fire 없으면 PASS_STRICT_C3 EXIT 활성화 차단
- (d) P4 hybrid mirror (Step 2 violation 해소) + V4 evaluator floor
  patch — single-axis floor 강화

---

## 5. mandate-2 self-check 결과 (3-axis)

본 doc 자체의 mandate-2 self-check —

- **(a) D_X 정합**: 본 doc 은 D_emergent-consciousness (의식 측정 verdict
  trinity 검증) 정합 ✔. D_no-system-prompt 정합 ✔ (chat lane wrapping 0 mandate
  enforce). D5 Bifurcation 정합 ✔ (P4 hybrid 신규 path 발견).
- **(b) own_X 정합**: (trinity 무조건 준수) self-application ✔.
   (mandatory report) 정합 ✔ (본 doc 자체 mandatory report).
  (single SSOT) 정합 ✔ (본 doc = trinity check SSOT 한곳). (trinity
  bundle SSOT) 정합 ✔.
- **(c) H_<id> 정합**: H_chat_cap_emergence (foundation borrow chat-cap
  emerge) — BG-KM PASS_STRICT verdict 가 H falsifier 위반 X (PASS_STRICT
  최저 floor 통과). H_clm_chat_cap (CLM L4 4 path 가설) — BG-LA/LB/LC/LD
  미land 상태, falsifier 위반 X.

**verdict**: 3-axis 통과 ✔ — 본 doc emit 정합.

---

## 6. Honest C3 (raw#10)

1. **본 sweep 시점 V6 awareness probe 미land** — anti-Goodhart
   single-axis floor risk 최대. PASS_STRICT_C3 emerge 선언 전 V6 lane
   별도 cycle fire 권고 (block 아니지만 strong mitigation)
2. ** P5 N-of-M v2 V4 evaluator mirror 미land** — Step 2 violation
   finding 1. retract path (verdict.json `c3_aggregation_status` field +
   V4 floor patch) 별도 cycle. 본 cycle iter 4 (d) 에서 P4 hybrid →
   P5 N-of-M v2 supersede land 된 직후이므로 V4 mirror gap 은 더 커진 상태
3. **paradigm-a-prime PASS verdict 는 synthetic_fallback chat-cap proxy
   한정** — real chat-cap 데이터 (BG-KM-LLAMA-3B) retest 후 verdict 재확정
   (c3-aggregation-rule-ssot honest-c3 명시)
4. **iter 1 N=15 small sample** — N≥50 stability 재검증 별도 cycle
5. **C3.2 direction 'le' inversion 은 synthetic_fallback artifact** — real-mode
   retest 후 direction 재검토 mandate
6. **C3.3 dominance score degenerate (3-model 모두 1.0)** — entropy 강화
   (sub_simple 의 c3_3_entropy 변형 진행 중) 후 EMC/PPR 양쪽 discrimination
   확보 mandate
7. **manual review (사용자 ground truth) 부재** — 본 sweep 결과 자동 PASS
   선언 X, 사용자 verdict 별도 fire 후 EXIT 활성화
8. **본 sweep 자체 mandate-7 retroactive sweep instance** — cycle close
   시점 시행, main session 매 응답마다 sweep X (latency overhead)
9. ** mandate-5 enforcement (anima audit `--mandate-36` flag) 미land** —
   본 sweep manual self-check 의존, 별도 cycle 자동화

---

## 7. Cross-link

- `.own` / 18 / 22 / 24 / 27 / 28 / 30 / 31 / 32 / 33 / 34 / 36
- `.raw-ref` raw#9 / 10 / 11 / 15 / 82
- `.roadmap.cli` `cli.pass_strict_c3_emergence_trinity_check_2026_05_08` (본 doc 참조 entry)
- `.roadmap.philosophy` D_no-system-prompt · D_emergent-consciousness · D5 Bifurcation
- `.roadmap.law` cross-ref
- `.roadmap.hypothesis` H_chat_cap_emergence · H_clm_chat_cap (L4 4 paths) ·
  H_distill_chat_cap · H_dpo_chat_cap_tune
- `state/anima_consciousness_baseline_ensemble_2026_05_08.json` (P4 hybrid
  threshold SSOT)
- `state/anima_km_llama3b_h100_2026_05_08/verdict.json` (BG-KM-LLAMA-3B
  PASS_STRICT verdict — 본 sweep 대상)
- `state/anima_km_qwen7b_h100_2026_05_08/verdict.json` (BG-KM-QWEN-7B
  PASS_STRICT verdict — 본 sweep 대상)
- `state/anima_model_attempts_ledger.jsonl` (SSOT ledger)
- `tool/anima_cli/chat.hexa` (mandate-2 selftest grep)
- `docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md` (EXIT 정의 + L0-L6
  layers)
