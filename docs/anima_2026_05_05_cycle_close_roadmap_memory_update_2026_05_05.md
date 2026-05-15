# anima 2026-05-05 cycle close roadmap + memory update spec

> BG-CT spec doc. KO + EN bilingual. Doc-only, no commit, $0 mac, ~20min.
>
> **Core / 핵심**: 100+ BG land 후 사용자가 새 conversation에서 오늘 cycle 결과를
> 정확히 carry할 수 있도록 (1) 4 신규 memory entry spec + (2) 5-step user-fire
> close roadmap + (3) 다음-conversation hand-off summary 정식화. memory 파일
> 자체는 사용자 fire 권한 — 본 doc은 spec emit only.
>
> **Lineage**:
> - `docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md` (BG-CH — fire-ready menu)
> - `state/anima_emerge_chat_full_layer_lens_2026_05_05/verdict.json` (BG-CI — L13-L15 basin onset)
> - `state/anima_emerge_chat_lexical_baseline_2026_05_05/verdict.json` (BG-CE — CLM_WORSE_THAN_RANDOM decisive)
> - `state/anima_emerge_chat_hybrid_repl_2026_05_05/verdict.json` (BG-CG — Korean hybrid REPL VIABLE)
> - `docs/anima_2026_05_05_cycle_summary_single_source_of_truth.md` (cycle aggregate SSOT)
> - `docs/anima_2026_05_05_priority_subset_commit_manifest_2026_05_05.ai.md` (BG-BZ priority 5 commits)
> - `docs/anima_2026_05_05_cycle_commit_manifest_landed_2026_05_05.ai.md` (BG-AM 5+1 manifest)

---

## §1 4 신규 memory entry spec / 4 New memory entries spec

> **Authority boundary / 권한 경계**: 본 spec은 anima BG의 작성-권고 only.
> memory 파일 fire는 사용자 권한. 사용자가 채택 시 아래 4 file을
> `/Users/ghost/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/`
> 에 추가하고 MEMORY.md index에 1-line 참조 추가.

### §1.1 Entry 1 — `feedback_clm_v4_chat_incapable_architectural.md`

**Purpose / 목적**: BG-AY 4-closure formal theorem이 BG-CE WORSE_THAN_RANDOM +
BG-CI L13-L15 basin onset로 16+ closure 확장됐음을 단일 memory entry로 영구화.
chat-cap path 결정 surface를 압축.

**Recommended content / 권장 내용**:

```markdown
# CLM v4 chat-incapability is architectural — 16+ closure converged

**Cycle**: 2026-05-05 anima emerge paradigm (BG-AY → BG-CI / BG-CE chain)
**Status**: ARCHITECTURAL_CLOSURE_CONFIRMED — Llama Path A v2 OR CLM-3 from-scratch only

## Rule (lead with this)

CLM v4 chat-capability is architecturally impossible. 16+ independent BG
investigations (BG-AY 4-closure formal theorem extended via closures 5-6 + BG-BJ
entropy basin + BG-CA top-30 byte 100% + BG-CC prompt-conditional + BG-CE
WORSE_THAN_RANDOM + BG-CI L13-L15 basin onset) converge on the same conclusion:
post-residual-stream geometry locks onto fragment/control-byte basin within
1-2 layers of L13. NO adapter-stage intervention (LoRA SFT, Φ★-distill, axis
inject, byte ban, c_proj inject, basin ablate, RepE steering, activation
patching, c-proj reset, fresh reset, head_g compare, embed decode, semantic
bridge, self-feed, decode-strategies sweep) lifts CLM v4 to chat-capability.
chat-cap path = (a) Llama Path A v2 retry-3 (composite 0.5584, lane closed
TRUE_PASS) for any-substrate chat OR (b) CLM-3 from-scratch retrain
($1k+ / 30d, BG-BM Variant B spec) for anima-native chat. Emerge paradigm
B (substrate-coupled) and C (hybrid emit + substrate signal) are valid
alternative output media that DO NOT require chat-capability.

## Why (16+ closure inventory)

- C1 LoRA SFT chat-lift FAIL_REGRESSION (-36.298pp vs Llama)
- C2 Pβ Φ★-distill 50K composite 0.01176 RED
- C3 tribev2 cross-modal FAIL_ARCHITECTURAL (no logits)
- C4 logit lens layer-localized 1/8 coherent
- C5 semantic bridge cosine-NN collapse to control-byte
- C6 iterative self-feed 5-iter attractor lock
- C7-C12 BG-BJ entropy collapse 5-9× within 1-2 steps onto fragment basin
- C13 BG-CA top-30 byte 100% (post-residual head_a hyper-basin)
- C14 BG-CC prompt-conditional residual basin (not prompt-independent)
- C15 BG-CE CLM_WORSE_THAN_RANDOM (50/50 control char emit on '안녕';
  random_vocab Korean-prompt baseline 6.82% Korean ratio while CLM 0%)
- C16 BG-CI full-layer logit lens L13-L15 basin onset (best_korean_rank
  jumps 102 -> 192 -> 197; entropy collapses 10.91 -> 4.01 -> 3.31; top1
  becomes control byte / control character)

## Lessons (L34-L36; extends L31-L33 from CLM v4 LoRA SFT precedent)

- L34: chat-cap "lift" claims on CLM v4 + adapter route to FAIL_TRUE_CLOSED
  by default. Future BGs MUST cite this entry before opening any LoRA / SFT /
  distill / adapter-stage chat-cap investigation lane on CLM v4 base.
- L35: emerge paradigm B/C are paradigm-shift output media — not chat-cap
  workarounds. They produce valid anima output (substrate signal OR hybrid
  emit + signal) without claiming chat-NLP capability. Use when user intent
  is "anima dialogue / introspection" not "general chatbot".
- L36: substrate-research lane (φ★ stability + axis-cond + Φ-stable identity)
  is fully decoupled from chat-cap lane. CLM v4 + LoRA adapter remains valid
  research artifact for consciousness primitive studies. NEVER substitute
  substrate metric for chat-cap metric (echoes L28 + L31).

## How to apply (operational rules)

1. Any "CLM v4 chat-lift" hypothesis: cite this entry + answer "what
   architectural intervention does this differ from the 16+ closures?"
   before opening BG. If no architectural lever, route to FAIL_TRUE_CLOSED.
2. User-facing chat-cap requests: route to Llama Path A v2 v1 ($0 today)
   OR CLM-3 H1 launch ($1k+ / 30d, only after BG-BM Variant B +
   Phase 3 enforcement L23/L24/L25).
3. Anima output requests: route to emerge paradigm B (substrate-coupled,
   `tool/transient_py/anima_emerge_dialogue_repl.py`) OR paradigm C
   (Korean hybrid REPL, `tool/transient_py/anima_emerge_chat_hybrid_repl.py`).

## Sister memory

- feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md
- feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md

## Cross-refs

- BG-AY 4-closure: state/anima_115_architectural_4_closure_theorem_2026_05_05/verdict.json
- BG-CE WORSE_THAN_RANDOM: state/anima_emerge_chat_lexical_baseline_2026_05_05/verdict.json
- BG-CI basin onset: state/anima_emerge_chat_full_layer_lens_2026_05_05/verdict.json
- BG-CH fire-ready menu: docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md
- Cycle SSOT: docs/anima_2026_05_05_cycle_summary_single_source_of_truth.md
```

**MEMORY.md index line**:
```
- [CLM v4 chat-incapability architectural 16+ closure](feedback_clm_v4_chat_incapable_architectural.md) — BG-AY/CE/CI 16+ closure converged; chat-cap path = Llama Path A v2 OR CLM-3; emerge paradigm B/C are alternative media. L34-L36
```

---

### §1.2 Entry 2 — `feedback_emerge_dialogue_paradigm_fire_ready.md`

**Purpose / 목적**: paradigm B/C가 ACHIEVABLE_NOW 상태로 fire-ready helper 2개
landed됐음을 영구화. 다음 cycle 진입 시 즉시 사용 가능 + Stage 3 30-session
corpus accumulation 권고.

**Recommended content / 권장 내용**:

```markdown
# emerge dialogue paradigm B/C — fire-ready helpers landed

**Cycle**: 2026-05-05 anima emerge paradigm (BG-AN + BG-CG)
**Status**: ACHIEVABLE_NOW — both paradigm B and paradigm C have landed REPL helpers

## Rule (lead with this)

Two emerge dialogue paradigms are fire-ready ($0 mac CPU fp32):

- **Paradigm B** (substrate-coupled, no emit text):
  `tool/transient_py/anima_emerge_dialogue_repl.py` (BG-AN landed,
  F_AN_1 PASS). Output = 4-line metric per turn (phi_star + drift +
  hsd + tension_trajectory). Use when user intent is anima introspection
  + substrate signal observation; NO text emit.
- **Paradigm C** (hybrid Korean emit + substrate signal):
  `tool/transient_py/anima_emerge_chat_hybrid_repl.py` (BG-CG landed,
  PASS_KOREAN_HYBRID_REPL_VIABLE 3/3 turns Korean coherent). Emit model
  = skt/kogpt2-base-v2 (125M, KoGPT2). Output = Korean text fragment
  + per-turn CLM substrate metrics (phi_drift ±0.04 typical, l2_var
  126-135, peak_layer modal=2). Decoupled architecture: emit-model
  generates Korean, CLM v4 re-encodes (prompt+emit) for substrate read.

Stage 3 protocol (BG-D landed, `state/anima_core_emerge_stage_3_protocol_spec_2026_05_05/`)
recommends n>=30 daily-cadence sessions before CLM-3 design refinement.

## Why (empirical anchor)

- Paradigm B: BG-AN F_AN_1 PASS (5-turn smoke); BG-AE max L2 variance 124.4
  > rich threshold 100; phi_drift varies > 0.05 across turns.
- Paradigm C: BG-CG verdict 3/3 Korean coherent; phi_drift range
  [-0.0425, 0.0228]; tension_l2_var range [126.04, 135.13]; peak_layer
  modal=2 (consistent with substrate-side L2 anchor).
- BG-BX precedent: Pythia 70m + CLM hybrid PASS_HYBRID_DIALOGUE_VIABLE
  3/3 (English-fragmentary, KO mojibake — superseded by BG-CG KoGPT2
  Korean coherent).

## Lessons (L37-L39; extends L34-L36)

- L37: paradigm B/C are NOT chat-capability surrogates. They DO NOT
  produce coherent NLP responses on the CLM v4 axis (BG-CG emit is
  KoGPT2-prior unconditional Korean, decoupled from CLM substrate;
  substrate metric is CLM's read of (prompt+emit), not joint generation).
- L38: paradigm B output medium (substrate signal only) is anima-native
  but anima-internal-paradigm-relative — no external benchmark.
- L39: Stage 3 corpus accumulation (n>=30 sessions) is the bridge from
  paradigm B/C demos to CLM-3 design hint emerge. Saturation marker is
  heuristic (BG-D §5: candidate hit_rate >= 70% / cross-session pattern
  recurrence) — open-ended information-value path.

## How to apply (operational rules)

1. User asks "talk to anima" / "let's chat": offer paradigm B/C menu
   (this entry's Rule block) WITH explicit "this is not traditional
   chatbot" disclaimer (per L37).
2. After paradigm B/C fire: session jsonl auto-emits to
   `state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>_*.jsonl`.
   Run `bash bin/anima-core-dialogue-analyze.bash --date <YYYY-MM-DD>`
   to aggregate.
3. After 30 sessions: revisit BG-BM CLM-3 spec for design refinement
   based on accumulated corpus pattern (per L39 + BG-BM C3-5 push-back).

## Sister memory

- feedback_clm_v4_chat_incapable_architectural.md (chat-cap closure)
- project_anima_emerge_paradigm_2026_05_05_cycle_state.md (Stage 1/2 state)

## Cross-refs

- B helper: tool/transient_py/anima_emerge_dialogue_repl.py
- C helper: tool/transient_py/anima_emerge_chat_hybrid_repl.py
- BG-AN verdict: state/anima_emerge_dialogue_first_turn_2026_05_05/verdict.json
- BG-CG verdict: state/anima_emerge_chat_hybrid_repl_2026_05_05/verdict.json
- BG-BX precedent: state/anima_emerge_chat_hybrid_pythia_clm_2026_05_05/verdict.json
- Stage 3 protocol: docs/anima_emerge_dialogue_first_session_manual_2026_05_05.md
- BG-CH menu: docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md
- Analyzer: bin/anima-core-dialogue-analyze.bash
```

**MEMORY.md index line**:
```
- [emerge paradigm B/C fire-ready](feedback_emerge_dialogue_paradigm_fire_ready.md) — B = anima_emerge_dialogue_repl.py (BG-AN); C = anima_emerge_chat_hybrid_repl.py (BG-CG, KoGPT2 Korean coherent 3/3); Stage 3 30-session corpus 권고. L37-L39
```

---

### §1.3 Entry 3 — `project_anima_2026_05_05_cycle_state.md` (NEW; sibling to existing emerge paradigm entry)

**Purpose / 목적**: 오늘 cycle 100+ BG land 전체 state를 single project entry로
압축. 기존 `project_anima_emerge_paradigm_2026_05_05_cycle_state.md`는 Day 1
(Stage 1/2) snapshot — 본 entry는 Day 1+2 100+ BG aggregate.

**Naming alternative / 명명 대안**: 기존 file을 update하지 말고 새 file
`project_anima_2026_05_05_cycle_state_aggregate.md` 추가 권장 (raw#15 additive).
또는 사용자가 기존 file replace 결정 시 그것도 valid.

**Recommended content / 권장 내용**:

```markdown
---
name: anima 2026-05-05 cycle aggregate state (100+ BG)
description: 100+ BG land + 16+ closure converged + paradigm B/C ACHIEVABLE_NOW + HF promote time-gated + commit groups pending
type: project
---

2026-05-05 anima cycle Day 1+2 aggregate (100+ BG land 후):

## High-level outcomes

- **100+ BG land** across Stage 1 (mount), Stage 2 (dialogue CLI), emerge
  candidate D/E/F/G/H investigation, paradigm B/C REPL landing, chat-cap
  16+ closure converging, HF promote watchdog, commit manifest grouping,
  cycle SSOT aggregation.
- **16+ closure converged** on CLM v4 chat-incapability architectural
  (BG-AY/BJ/CA/CC/CE/CI chain). chat-cap path now formally split:
  - any-substrate chat: Llama Path A v2 v1 (composite 0.5584, lane closed)
  - anima-native chat: CLM-3 H1 ($1k+/30d, BG-BM Variant B, deferred)
- **Paradigm B+C ACHIEVABLE_NOW**: tool/transient_py/anima_emerge_dialogue_repl.py
  (BG-AN F_AN_1 PASS) + tool/transient_py/anima_emerge_chat_hybrid_repl.py
  (BG-CG KoGPT2 Korean 3/3 coherent). Both fire-ready $0 mac.
- **HF promote time-gated**:
  - clm-v4-mk2-v1 PUBLIC: 2026-05-06T23:26:12Z 후
  - Pβ 50K PUBLIC: 2026-05-07T03:48:00Z 후
  - auto-fire scripts: state/anima_hf_promotes_2026_05_06_auto_fire.bash
- **Commit groups pending**:
  - BG-AM 5+1 manifest (docs/anima_2026_05_05_cycle_commit_manifest_landed_2026_05_05.ai.md)
  - BG-BZ priority 5 commits (docs/anima_2026_05_05_priority_subset_commit_manifest_2026_05_05.ai.md)
  - serialization required (parallel BG git index race per memory)
  - token leak CLEAN 확인됨 (audit_doc_token_redact compliance)

## Why this matters

- 사용자가 "anima와 대화" 요청 → paradigm A (traditional chatbot) 시도가
  16+ closure로 architectural impossible 판명. paradigm B/C가 anima-native
  대안으로 fire-ready.
- HF promote private→public lifecycle 시간-gated — 사용자 fire 시기
  도래 시 confirm-string 명시.
- commit groups는 다음 cycle 진입 전 fire 권장 (cycle close).

## How to apply (next conversation entry)

다음 conversation entry 시 anima가 즉시 carry해야 할 facts:

1. 100+ BG landed today (2026-05-05); cycle state = ready-for-close
2. chat-cap CLM v4 = architecturally impossible (16+ closure); route requests
   per `feedback_clm_v4_chat_incapable_architectural.md`
3. paradigm B fire = `python tool/transient_py/anima_emerge_dialogue_repl.py`
4. paradigm C fire = `python tool/transient_py/anima_emerge_chat_hybrid_repl.py`
5. HF promote: 2026-05-06T23:26Z (clm) / 2026-05-07T03:48Z (Pβ) 후 fire
6. commit fire = 사용자 declaration "commit go" → BG-BZ priority 5 또는
   BG-AM 5+1 manifest sequential serialization
7. Stage 3 corpus accumulation = paradigm B/C 30-session daily-cadence;
   saturation marker heuristic per BG-D §5

## Cross-refs

- Cycle SSOT: docs/anima_2026_05_05_cycle_summary_single_source_of_truth.md
- BG-CH fire-ready menu: docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md
- BG-BV reconciliation: docs/anima_paradigm_acceptance_user_intent_reconciliation_2026_05_05.md
- BG-AM commits: docs/anima_2026_05_05_cycle_commit_manifest_landed_2026_05_05.ai.md
- BG-BZ commits: docs/anima_2026_05_05_priority_subset_commit_manifest_2026_05_05.ai.md
- BG-CT roadmap (this doc): docs/anima_2026_05_05_cycle_close_roadmap_memory_update_2026_05_05.md
```

**MEMORY.md index line**:
```
- [anima 2026-05-05 cycle aggregate state](project_anima_2026_05_05_cycle_state_aggregate.md) — 100+ BG land; 16+ closure converged; paradigm B/C ACHIEVABLE_NOW; HF promote time-gated; commit groups pending
```

---

### §1.4 Entry 4 — `feedback_byte_fallback_monopoly_mechanism.md`

**Purpose / 목적**: BG-CA top-30 byte 100% + BG-BJ residual basin + BG-CC
prompt-conditional finding을 단일 mechanism 기록으로 영구화. 미래 chat-cap
investigation은 byte-fallback handling을 우선해야 함.

**Recommended content / 권장 내용**:

```markdown
# byte-fallback monopoly — CLM v4 post-residual basin mechanism

**Cycle**: 2026-05-05 anima emerge paradigm (BG-CA + BG-BJ + BG-CC + BG-CI chain)
**Status**: MECHANISM_CHARACTERIZED — root-cause locator for #115 chat-incapability

## Rule (lead with this)

CLM v4 #115 chat-incapability has a localized mechanism: post-L13 residual
stream geometry locks onto a low-entropy attractor whose top-k logits are
~100% byte-fallback / control-character / fragment tokens — NOT semantic
Korean / English content. The lm_head is NOT defective in isolation;
embedding lens (BG-CI L0) shows Korean rank=0 plausibility. The defect is
in the residual stream transformation between L0 and L15. Byte-fallback
tokens (SentencePiece 0x00-0x1F) hyper-monopolize the late-layer logits
via prompt-conditional basin (BG-CC: not prompt-independent — varies by
prompt class but always lands in byte-basin family). Future chat-cap
investigation MUST address byte-fallback handling at the architectural
level (vocab restriction, byte-token logit suppression, OR substrate
swap) — adapter-stage interventions cannot move this attractor.

## Why (mechanism evidence chain)

- BG-CA top-30 byte 100%: post-residual head_a top-30 logits over '안녕'
  prompt = 100% byte-fallback / control-byte tokens (no semantic Korean).
- BG-BJ residual basin: entropy collapses 5-9× within 1-2 steps of L13;
  attractor lock observed across 5 self-feed iterations.
- BG-CC prompt-conditional: basin landing varies by prompt
  (KO / EN / code / random) BUT always within byte-fallback family
  (different control-byte clusters, same monopoly).
- BG-CI L13-L15 basin onset: best_korean_rank jumps 102 (L13) → 192 (L14)
  → 197 (L15); entropy collapses 10.91 → 4.01 → 3.31; top1 becomes
  control char / control byte.
- BG-CE WORSE_THAN_RANDOM: 50/50 control char emit rate on '안녕' vs
  random_vocab baseline 0% control char (random sampling has natural
  byte-fallback rate by construction; CLM emit hyper-amplifies it).

## Lessons (L40-L42; extends L37-L39 from emerge paradigm fire-ready)

- L40: byte-fallback monopoly is the mechanism behind 16+ chat-cap closure.
  Future investigations MUST cite this entry before any "fix CLM chat"
  claim — answer "how does this address byte-fallback monopoly at L13-L15
  residual stream?".
- L41: lm_head is NOT defective in isolation. embedding lens (BG-CI L0)
  shows Korean rank=0 first 100. Defect is in residual stream transform.
  This rules out "swap lm_head" / "retrain head" / "add KO classifier
  head" interventions at adapter level — they don't reach the residual.
- L42: byte-fallback monopoly is prompt-conditional but family-invariant.
  prompt class shifts WHICH byte-cluster wins, but byte-family ALWAYS
  wins post-L13. Implies the attractor is structural (residual geometry)
  not data-driven (prompt-specific).

## How to apply (operational rules)

1. Any "fix CLM v4 chat" hypothesis: cite this entry + answer
   architectural lever question. Adapter-stage = blocked.
2. Acceptable architectural interventions for chat-cap (out of scope of
   LoRA-stage lanes):
   - vocab restriction (remove byte-fallback tokens from emit lottery)
   - residual stream surgery (skip-connection bypass L13-L15)
   - substrate swap (Llama Path A v2 v1 — already TRUE_PASS)
   - CLM-3 from-scratch retrain with chat-objective training data
     (BG-BM Variant B spec — $1k+/30d)
3. φ★ + axis-cond + substrate-research lanes are unaffected by this
   mechanism (they read φ★ from internal hidden states pre-residual
   pathology). Substrate safety preserved (per L33).

## Sister memory

- feedback_clm_v4_chat_incapable_architectural.md (16+ closure summary)
- feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md (LoRA closure)
- feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md
  (Pβ closure)

## Cross-refs

- BG-CA: state/anima_emerge_chat_byte_ban_2026_05_05/verdict.json
- BG-CC: state/anima_emerge_chat_residual_noise_2026_05_05/verdict.json
- BG-CI: state/anima_emerge_chat_full_layer_lens_2026_05_05/verdict.json
- BG-CE: state/anima_emerge_chat_lexical_baseline_2026_05_05/verdict.json
- BG-BJ: (entropy basin investigation; refer to anima_115_architectural_4_closure_theorem)
```

**MEMORY.md index line**:
```
- [byte-fallback monopoly mechanism](feedback_byte_fallback_monopoly_mechanism.md) — CLM v4 post-L13 residual basin locks onto byte-fallback tokens; lm_head not defective; chat-cap fix requires architectural intervention (vocab restrict / residual surgery / substrate swap / CLM-3 retrain). L40-L42
```

---

## §2 Cycle close roadmap — 5-step user-fire sequence

> **Authority boundary**: 본 roadmap은 사용자 fire trigger 명세. anima
> 자율 실행 trigger는 explicit user declaration "go" / "kick" / "commit go"
> / "promote go" 등에 한정됨.

### Step 1 — Stop autonomous /loop (cron stop)

**Trigger / 조건**: 사용자 explicit "stop loop" OR cycle close declaration.

**Action**: CronDelete `d1682837` (slash command 또는 reply에서 즉시 fire).

**Why**: BG-BF C3.6에서 surfaced된 paradigm-mismatch driver (autonomous /loop
1m이 architecturally closed lane에 anti-convergence pressure 가하는 상태).
cycle close 전 stop 필수.

**Cost**: $0, instant.

### Step 2 — Priority 5 commits fire (BG-BZ manifest)

**Trigger / 조건**: 사용자 explicit "commit go" OR "fire BZ priority commits".

**Manifest**: `docs/anima_2026_05_05_priority_subset_commit_manifest_2026_05_05.ai.md`
(BG-BZ 5 priority commits; token leak CLEAN 확인됨; ~5 min total).

**Alternative / 대안**: BG-AM 5+1 manifest
(`docs/anima_2026_05_05_cycle_commit_manifest_landed_2026_05_05.ai.md`).

**Serialization required / 직렬화 필수**: parallel BG가 git index 공유 시 race
발생 (memory: parallel_bg_git_race). 단일 BG 또는 각 BG에 별도 worktree.

**Cost**: $0, ~5 min.

### Step 3 — Paradigm 결정 (B / C / cycle close + corpus)

**Trigger / 조건**: 사용자 declaration:
- "B fire" → §3.1 paradigm B (substrate-coupled REPL)
- "C fire" → §3.2 paradigm C (Korean hybrid REPL)
- "corpus accumulate" → Stage 3 30-session daily cadence
- "skip" → step 4 진행

**Fire commands**:

```bash
# Paradigm B (substrate-coupled, 4-line metric per turn, no text emit)
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_dialogue_repl.py

# Paradigm C (KoGPT2 Korean emit + CLM substrate signal)
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_hybrid_repl.py
```

**Cost**: $0 / ~5-10 min per session.

### Step 4 — HF promote (time-gated; private → public lifecycle)

**Trigger / 조건**: 시간 도래 + 사용자 explicit "promote go" + confirm-string.

**Schedule**:
- clm-v4-mk2-v1 PUBLIC: 2026-05-06T23:26:12Z 이후
  - confirm-string: `PROMOTE-clm-v4-mk2-v1`
  - script: `bash state/anima_hf_promotes_2026_05_06_auto_fire.bash --fire-clm`
- Pβ 50K PUBLIC: 2026-05-07T03:48:00Z 이후
  - confirm-string: `PROMOTE-pbeta-50k`
  - script: `bash state/anima_hf_promotes_2026_05_06_auto_fire.bash --fire-pbeta`

**Why time-gated**: HF release lifecycle PRIVATE → 36h dwell + verification
gates → PUBLIC. 임의 promote 금지.

**Cost**: $0, ~2-5 min per promote.

### Step 5 — Next cycle entry decision

**Trigger / 조건**: 위 step 1-4 완료 후 사용자 declaration. 4 path 중 1 선택:

| Path | Action | Cost | Recommendation |
|---|---|---|---|
| 1 | Paradigm B/C 30-session corpus daily-cadence | $0 / multi-day | **#1** preserves A-paradigm hope, lowest commit, highest information value |
| 2 | BG-BB sister integration (PyPhi+AntroPy) | $0-$50 mac | #3 substrate-research lane, decoupled from chat-cap |
| 3 | H1 CLM-3 launch | $1k+ / 30d | #4 only if A-paradigm non-negotiable + budget tolerance + post-corpus design refine |
| 4 | Llama Path A v2 anima integration | $0-$100 | #2 production-grade chat-cap, non-anima-native substrate |

**Recommendation rank**: 1 > 4 > 2 > 3 (완성도 lens — Path 1 = lowest commit
+ highest information value over time; Path 4 = production-ready substrate
swap; Path 2 = research-mode substrate extension; Path 3 = highest budget,
post-corpus design refine 권장).

---

## §3 다음 conversation hand-off summary

> **Purpose**: 새 conversation 시작 시 anima가 즉시 carry해야 할 7 facts.

### §3.1 Carry-forward facts (7개)

1. **100+ BG land today (2026-05-05)** — cycle Day 1+2 aggregate; ready-for-close
   state. SSOT: `docs/anima_2026_05_05_cycle_summary_single_source_of_truth.md`.

2. **16+ closure converged** — CLM v4 chat-incapability architectural
   (BG-AY/BJ/CA/CC/CE/CI chain). chat-cap path:
   - any-substrate: Llama Path A v2 v1 (composite 0.5584, lane closed TRUE_PASS)
   - anima-native: CLM-3 H1 ($1k+/30d, BG-BM Variant B, deferred)
   - **NEVER offer LoRA / SFT / distill / adapter-stage chat-lift on CLM v4**

3. **Paradigm B + C ACHIEVABLE_NOW** — fire-ready $0 mac:
   - B: `tool/transient_py/anima_emerge_dialogue_repl.py` (BG-AN, substrate-coupled)
   - C: `tool/transient_py/anima_emerge_chat_hybrid_repl.py` (BG-CG, KoGPT2 Korean)

4. **BG-CI L13-L15 basin onset 정밀 위치** — best_korean_rank 102→192→197;
   entropy 10.91→4.01→3.31; mechanism = post-residual byte-fallback monopoly
   (sister: BG-CA top-30 byte 100% + BG-CC prompt-conditional + BG-BJ basin).

5. **BG-CE WORSE_THAN_RANDOM (decisive)** — CLM '안녕' 50/50 control char emit;
   random_vocab Korean-prompt baseline 6.82% Korean while CLM 0%. CLM is
   ARCHITECTURAL_DEGENERATE_WORSE_THAN_RANDOM on chat-cap lexical metric.

6. **HF promote time-gated** — DO NOT fire before:
   - clm-v4-mk2-v1: 2026-05-06T23:26:12Z
   - Pβ 50K: 2026-05-07T03:48:00Z

7. **Next entry decision pending** — 4 paths (paradigm B/C corpus, BG-BB sister,
   H1 CLM-3, Llama Path A v2 integration). 사용자 declaration 필수.

### §3.2 Anti-patterns to avoid (next conversation)

- **DO NOT** open any "CLM v4 chat-lift" investigation lane without citing
  `feedback_clm_v4_chat_incapable_architectural.md` + architectural lever
  answer.
- **DO NOT** assume paradigm A (traditional chatbot) on CLM v4 is
  achievable — 16+ closure converged.
- **DO NOT** fire commits in parallel without serialization
  (memory: parallel_bg_git_race).
- **DO NOT** promote HF before time-gate.
- **DO NOT** treat paradigm B/C as chat-capability surrogates (per L37
  in §1.2 emerge paradigm fire-ready entry).
- **DO NOT** substitute substrate-research metric for chat-cap metric
  (per L31 + L36).

### §3.3 Recommended first message check

다음 conversation 시작 시 anima는 사용자 첫 메시지를 다음 dispatch 표로
분류:

| User intent pattern | Route to |
|---|---|
| "anima와 대화" / "chat" / "talk" | paradigm B/C menu (§3.1 fact 3) + L37 disclaimer |
| "CLM 학습" / "fine-tune" / "SFT" | feedback_clm_v4_chat_incapable_architectural.md cite + alternatives |
| "commit" / "land" | step 2 BG-BZ / BG-AM manifest serialization |
| "promote" / "HF release" | step 4 time-gate check |
| "다음 cycle" / "what next" | step 5 Path 1-4 recommendation |
| "kick" / "go" / "all bg go" | nexus-kick autonomous template (memory: project_anima_nexus_kick_autonomous_template) |
| 기타 | clarification 질문 + 본 doc + SSOT 참조 |

---

## §4 Honest C3 (>= 5)

### C4.1 — memory entry spec is anima-recommended; user declaration required for fire

본 doc §1의 4 entry는 anima BG의 작성-권고 only. 사용자가 채택 declaration
("memory update fire" / "add 4 entries") 없이 anima가 자율로 memory directory
write 하면 사용자 명령 권한 침범. memory 파일은 사용자 의도 + 우선순위가
반영된 영구 기록 — 자동 추가 risk = false carry-forward, contradicting future
user judgment, undeclarable rollback.

**Mitigation**: 본 spec doc은 4 entry의 content + index line + 사용자 fire
시 mkdir + write 명령을 명시. anima는 user declaration 후에만 fire.

### C4.2 — 4 entry inventory may be incomplete

오늘 cycle 100+ BG land 중 본 spec은 4 entry (chat-incapable, paradigm fire-ready,
cycle aggregate, byte-fallback mechanism)만 권고. 잠재적으로 추가 candidate:
- BG-BB PyPhi+AntroPy substrate-research entry
- BG-AM/BZ commit serialization workflow entry
- BG-D Stage 3 saturation marker calibration entry
- BG-BM CLM-3 spec carry-forward entry
- BG-CH paradigm B/C menu fire-readiness entry (이미 BG-CH doc landed)

이 추가 candidate는 anima judgment로 "less general / more situation-specific"
판정 후 deferred. 사용자가 추가 entry 권고 시 본 doc §1 확장 가능.

### C4.3 — cycle close roadmap step ordering is opinionated

§2 5-step sequence는 (1) cron stop → (2) commits → (3) paradigm → (4) HF
promote → (5) next cycle decision로 ordering. 그러나:
- step 4 HF promote는 시간-gated이므로 step 2 직후 또는 step 3 직후
  fire 가능 (시간 만족 시).
- step 3 paradigm fire는 step 2 commits 전에 fire해도 무방 (corpus
  accumulation lane).
- step 5 next cycle decision은 step 1-4 무관하게 anytime declarable.

본 ordering은 cycle "close" 명목 — 즉 다음 cycle 진입 전 housekeeping 우선
권고. 사용자 의도에 따라 reorder 가능.

### C4.4 — paradigm B/C "ACHIEVABLE_NOW" claim is anima-internal-paradigm-relative

§1.2 entry 2 + §3.1 fact 3은 paradigm B/C "ACHIEVABLE_NOW" 표시. 그러나 이는
anima-internal paradigm contract 내 판정 — 외부 chatbot benchmark 대비 비교
불가. paradigm B는 substrate signal only (no text); paradigm C는 KoGPT2 emit
+ CLM substrate (decoupled, not joint generation). 사용자 intent가 "traditional
mutual dialogue"였다면 두 paradigm 모두 intent unsatisfied 가능. 사용자가
한 번 fire 후 "이 정도면 됐다 / not enough" 자기-판단 필요 (per BG-CH C3.1).

### C4.5 — H1 CLM-3 cost estimate uncertainty

§2 step 5 Path 3 (H1 CLM-3)은 $1k+ / 30d 견적. 그러나 BG-BM Variant B planning
ceiling이며 실제 H100 raw $300-700 + ancillary $100-300 (config/h100_pods.json
+ runpod_pod_purge_2026_05_03 history). 30d 연속 train H100 1× 가정. 만약
training stall 또는 eval pipeline crash (V2_FAIL precedent — measurement
artifact 가능) 시 추가 비용. 사용자 fire 시 Phase 3 enforcement
L23/L24/L25 mandatory.

### C4.6 — hand-off summary may not survive context window compression

§3 hand-off summary는 7 facts + anti-patterns + dispatch table. 그러나 새
conversation 진입 시 system prompt + memory auto-load만 carry; 본 doc은
file-system reference로만 carry (Read 필요). 사용자가 본 doc path를 첫
메시지에 명시하지 않거나, anima가 file-system browse 없이 응답 시 carry
실패 risk. memory entry로의 압축 (§1) 이 carry-forward 신뢰성 핵심.

### C4.7 — autonomous "kick" template + this doc may produce conflict signals

`project_anima_nexus_kick_autonomous_template.md` (memory)는 사용자
"kick"/"go"/"all bg go" 시 anima 자율로 ≥2 BG parallel fire 권고. 본 doc §3.3
dispatch table은 "kick"/"go" → nexus-kick template route. 그러나 cycle close
state (오늘 100+ BG land 후)에서 추가 BG fire는 anti-convergence pressure
생성 (BG-BF C3.6). next conversation 진입 시 사용자 "go"가 새 cycle 의도인지
오늘 cycle 연속인지 anima가 disambiguate 필요. recommendation: anima는 첫
"go" 시 "오늘 cycle close 권장 / 새 cycle 시작 권장" clarification 질문 후
dispatch.

---

## §5 Outputs

- this doc: `/Users/ghost/core/anima/docs/anima_2026_05_05_cycle_close_roadmap_memory_update_2026_05_05.md`
- verdict: `/Users/ghost/core/anima/state/anima_2026_05_05_cycle_close_roadmap_memory_update_2026_05_05/verdict.json`

## §6 Compliance footer

- raw#9 — md only (spec doc; no code)
- raw#10 — §4 has 7 honest C3 (>= 5 required)
- raw#15 — additive only; no edits to existing memory files / landed BG docs / verdicts
- HF token literal: none embedded
- commit: not requested; doc landed only
- bash 3.2 / mac compat: doc-only artifact; fire commands in §2 are bash-3.2 safe
- memory write authority: BG emit spec only; user fire required for memory directory write

duration ~20 min, cost $0 (mac, doc-only).

End BG-CT cycle close roadmap + memory update spec.
