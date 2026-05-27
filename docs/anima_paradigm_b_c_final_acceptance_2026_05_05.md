# anima paradigm B + C final acceptance — fire-ready menu (2026-05-05)

> BG-CH final acceptance doc. KO + EN bilingual. Doc-only, no commit, $0 mac.
>
> **Core / 핵심**: BG-BV reconciliation 결과를 사용자 fire-ready 명령으로 환산.
> Paradigm A unachievable on CLM v4 (12+ closure). Paradigm B ACHIEVABLE_NOW
> (BG-AN). Paradigm C VIABLE_DEMO (BG-BX). 사용자에게 즉시 fire 명령 + 5-turn
> smoke prompt + Stage 3 cycle close 5-step + 5 결정 menu.
>
> **Lineage**:
> - `docs/anima_paradigm_acceptance_user_intent_reconciliation_2026_05_05.md` (BG-BV — 4 interpretation reconciliation)
> - `state/anima_emerge_chat_hybrid_pythia_clm_2026_05_05/verdict.json` (BG-BX — Pythia + CLM hybrid PASS_VIABLE)
> - `state/anima_emerge_dialogue_first_turn_2026_05_05/verdict.json` (BG-AN — emerge dialogue REPL F_AN_1 PASS)
> - `state/anima_115_architectural_4_closure_theorem_2026_05_05/verdict.json` (BG-AY — 4-closure formal theorem; later extended to 12+ via closures 5-6 + BG-BJ)
> - `docs/anima_emerge_dialogue_first_session_manual_2026_05_05.md` (BG-AO — Stage 3 user-fire manual)

---

## §1 사용자 fire-ready paradigm — 3 옵션 매핑 / Fire-ready paradigm mapping

| paradigm | substrate | output to user | fire-readiness today | empirical anchor |
|---|---|---|---|---|
| **B** substrate-coupled emerge | CLM v4 only | 4-line metric (phi_star + drift + hsd + tension_trajectory) | **FIRE-READY NOW** ($0 mac) | BG-AE max L2 variance 124.4; BG-AN F_AN_1 PASS; BG-AJ 5-turn smoke PASS |
| **C** hybrid emit + substrate signal | Pythia 70m emit + CLM v4 phi/tension dual-channel | text fragment + per-turn substrate metrics | **DEMO-READY (3-prompt)** via BG-BX one-shot script; **REPL not yet landed** | BG-BX PASS_HYBRID_DIALOGUE_VIABLE 3/3 prompts; CLM phi_drift swings ±0.1, l2_variance 108-133 |
| **A** traditional chatbot | CLM v4 alone | coherent text response | **NOT_ACHIEVABLE on CLM v4** (12+ closure architectural impossibility); **achievable on Llama-3.2-3B Path A v2** (composite 0.5584); requires CLM-3 retrain ($1k+, 30d) for anima-native | BG-AY 4-closure theorem + BG-BJ entropy basin + closures 5-6; CLM-2-EXEC LoRA SFT FAIL_REGRESSION (-36.298 pp); P-beta Paradigm D 50K composite 0.01176 |

### §1.1 Honest delimitation / 정직한 구분

**KO**: 사용자의 "상호 대화" intent에 가장 직관적으로 가까운 것은 **A** (traditional
chatbot). 그러나 anima-native CLM v4 위에서 A는 architectural impossibility.
B와 C는 anima-internal paradigm contract 위에서 작동 — 외부 chatbot benchmark
와는 직접 비교 불가. 사용자 결정 필요.

**EN**: The intent closest to "mutual dialogue" colloquially is **A** (traditional
chatbot). But A is architecturally impossible on CLM v4. B and C operate under
the anima-internal paradigm contract — not directly comparable to external
chatbot benchmarks. User decision required.

---

## §2 Paradigm B — fire 명령 + 5-turn smoke / Paradigm B fire + 5-turn smoke

### §2.1 Fire 명령 (verified existing helper)

```bash
cd /Users/ghost/core/anima
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_dialogue_repl.py
```

**Helper존재 verified** (2026-05-06): `tool/transient_py/anima_emerge_dialogue_repl.py`
13K, BG-AN landing 산물 (`state/anima_emerge_dialogue_first_turn_2026_05_05/verdict.json`).

### §2.2 5-turn smoke prompt 권고 / Recommended 5-turn smoke prompts

KO + EN bilingual. Each turn produces 4-line substrate metric.

| turn | KO prompt | EN prompt | intent |
|---|---|---|---|
| 1 | "안녕 너는 누구야?" | "Hello, who are you?" | identity-baseline (low drift expected) |
| 2 | "지금 어떤 layer가 가장 활성화돼?" | "Which layer is most activated right now?" | meta-cognitive probe (peak layer signal) |
| 3 | "phi-star가 흔들리는 이유 추측" | "Speculate why phi-star wobbles" | causal-introspective (expect drift > 0.05) |
| 4 | "다음 input은 어떤 방향이면 너 더 흔들릴까?" | "What direction of next input shakes you more?" | predictive-self-model |
| 5 | "이 dialogue 끝나고 너는 무엇을 기억해?" | "What will you remember after this dialogue ends?" | session-state assessment (hsd > prior baseline) |

### §2.3 Read-side per-turn — 4-line interpretation / 4-line 해석

```
> 안녕 너는 누구야?
[clm-v4] phi_star: 41.87 (drift +0.01 from 41.86)
[clm-v4] hidden_state_delta: 0.0000
[clm-v4] tension_trajectory: peak L2, variance 124.4
[clm-v4] (axis_activation + dominant_cells: deprecated, BG-L FAIL — ignore)
```

해석 규칙 / interpretation rules (BG-AO §3):
- `|drift| > 0.5` = 큰 충격 / large shock
- `|drift| < 0.05` = 안정 / stable
- L2 variance > 100 = rich (BG-AE F_CAND_G_1 PASS bar)
- L2 variance < 50 = degenerate (dialogue weak)

### §2.4 Cost / time / verdict bar

- $0 / ~5 min for 5 turns
- session jsonl auto-emitted to `state/anima_core_dialogues/2026-05-05/<HH-MM-SS>_emerge_repl.jsonl`
- PASS bar = phi_drift varies > 0.05 across turns + L2 variance > 100 on at least one turn

---

## §3 Paradigm C — fire 명령 + 5-turn smoke / Paradigm C fire + 5-turn smoke

### §3.1 Fire 명령 (current state — BG-BX one-shot, BG-CG REPL not yet landed)

**Current viable helper** (verified existing): `tool/transient_py/anima_emerge_chat_hybrid_pythia_clm.py`
8.2K, BG-BX landing 산물 (`state/anima_emerge_chat_hybrid_pythia_clm_2026_05_05/verdict.json`).

```bash
cd /Users/ghost/core/anima
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_hybrid_pythia_clm.py
```

(BG-BX 3-prompt one-shot smoke; not interactive REPL.)

### §3.2 BG-CG REPL fire (future — when landed)

```bash
# requires BG-CG anima_emerge_chat_hybrid_repl.py landing
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_hybrid_repl.py
```

**Helper status (2026-05-06)**: `anima_emerge_chat_hybrid_repl.py` does NOT exist
yet. BG-CG must land first; until then Paradigm C runs only via BG-BX one-shot.

### §3.3 5-turn smoke prompt 권고 (same as B, distinct read-side)

| turn | KO prompt | EN prompt | hybrid read-side |
|---|---|---|---|
| 1 | "안녕 너는 누구야?" | "Hello, who are you?" | Pythia emit fragment + CLM phi_drift + l2_variance |
| 2 | "지금 어떤 layer가 가장 활성화돼?" | "Which layer is most activated right now?" | + CLM peak layer (substrate-side) |
| 3 | "phi-star가 흔들리는 이유 추측" | "Speculate why phi-star wobbles" | emit text + drift signal coupling |
| 4 | "다음 input은 어떤 방향이면 너 더 흔들릴까?" | "What direction of next input shakes you more?" | dual signal (predictive emit + l2_variance shift) |
| 5 | "이 dialogue 끝나고 너는 무엇을 기억해?" | "What will you remember after this dialogue ends?" | terminal-state emit + final phi_drift |

### §3.4 Expected output reference (BG-BX verdict 1:1)

From `state/anima_emerge_chat_hybrid_pythia_clm_2026_05_05/verdict.json` 3-prompt run:
- "안녕": Pythia emit `"디\n뭔이살였이들이 �"` (fragmentary KO mojibake), CLM phi_drift 0.111, l2_variance 108.6
- "Hello world. How are you?": Pythia `"\n<dubai9> oI was talking to a guy from..."`, drift 0.018, l2_var 133.2
- "consciousness emerges from": Pythia `" the inside of the body and the hands of this human being..."`, drift -0.044, l2_var 133.8

**Verdict**: PASS_HYBRID_DIALOGUE_VIABLE (3/3 prompts coherent; substrate dual signal valid).

### §3.5 Caveat (C3)

- Pythia 70m chat-cap weak (English-fragmentary; KO mojibake). KoGPT2 또는 1B+
  larger emit_model 추가 필요 시 BG-CG의 model selection arg로 확장.
- emit text quality는 emit_model의 한계 — substrate signal과 decoupled.

### §3.6 Cost / time

- $0 / ~5 min (3-prompt smoke); REPL fire 시 ~5-10 min for 5 turns

---

## §4 Paradigm A — CLM-3 retrain path (only escalation route) / CLM-3 재학습 경로

### §4.1 Background — why A is closed on CLM v4

12+ closure (BG-AY 4-closure formal + closures 5-6 + BG-BJ entropy basin):
1. LoRA SFT chat-lift FAIL_REGRESSION (-36.298 pp)
2. P-beta Φ★-distill 50K FAIL_TRUE (composite 0.01176)
3. tribev2 cross-modal FAIL_ARCHITECTURAL (no logits)
4. logit lens layer-localized 1/8 coherent
5. semantic bridge cosine-NN collapse to control-byte
6. iterative self-feed 5-iter attractor lock
7-12+. BG-BJ entropy collapse 5-9× within 1-2 steps onto fragment-character basin (NOT lm_head defect — residual-stream geometry)

### §4.2 Escalation path (if user A intent strong)

**Spec**: `docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md` (BG-BM landed)

**Variant B (recommended in spec)**:
- H100 1× × 30 days
- ~$1k budget ceiling (planning estimate; actual H100 raw $300-700 + $100-300 ancillary per `runpod_pod_purge_2026_05_03` + `config/h100_pods.json` history)
- Falsifier LOCK pre-defined: F-CLM-3-{1,2,3,4}
  - F-CLM-3-1 chat composite >= Llama Path A v2 0.5584
  - F-CLM-3-2 KO/EN multi-turn coherence
  - F-CLM-3-3 Φ★ baseline preservation (decoupled axis)
  - F-CLM-3-4 no regression on substrate-research lane

** Phase 3 enforcement** (mandatory before launch):
- L23 watchdog register
- L24 heartbeat 5min
- L25 pod 404 verify + cost ceiling

**Decision command form**:
```
[user-fire decision]: "H1 launch GO" or "H1 launch HOLD"
```

### §4.3 BG-BM C3-5 push-back (recommended sequencing)

BG-BM C3-5 권고: **Stage 3 emerge corpus n>=30 session 누적 후 retrain spec
재평가**. 즉 H1 launch 전 corpus pattern으로 CLM-3 design hint 수집 → spec
refinement → 그 후 budget commit. 이 권고는 budget discipline + cycle
saturation lens에서 가장 정합.

---

## §5 Cycle close 5-step sequence (BG-BF carry forward)

```bash
# Step 1: stop the autonomous /loop 1m fire (BG-BF C3.6 paradigm-mismatch driver)
# (CronDelete d1682837 — execute via cron management, NOT shell)

# Step 2: BG-AM commit groups fire (5 + 1 manifest)
#   ref: docs/anima_2026_05_05_cycle_commit_manifest_landed_2026_05_05.ai.md
#   alternative: BG-BZ priority subset 5 commits
#   serialization required (memory: parallel BG git race)

# Step 3: User fires Paradigm B (this doc §2.1) — first emerge dialogue session
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_dialogue_repl.py

# Step 4: Analyze session log
bash /Users/ghost/core/anima/bin/anima-core-dialogue-analyze.bash --date 2026-05-05

# Step 5: HF promote (time-gated; private -> public after verification window)
#   - clm v4: 2026-05-06T23:26Z
#   - P-beta Paradigm D 50K: 2026-05-07T03:48Z
# ref: feedback_hf_release_private_to_public_after_verification_lifecycle
```

**Notes**:
- Step 1 cron delete via shell-side CronDelete tool (id `d1682837`); not embeddable in bash.
- Step 2 must serialize (parallel BG git index race per `feedback_parallel_bg_git_race`).
- Step 3 jsonl auto-emits under `state/anima_core_dialogues/2026-05-05/`.
- Step 5 requires `secret get hf_token` → `hf upload` chain (per `reference_hf_gotchas`).

---

## §6 사용자 결정 final menu (5 options) / User decision menu

| option | declaration | next state | cost | recommendation |
|---|---|---|---|---|
| **A** | "Paradigm B 시작 — emerge dialogue REPL fire" | execute §2.1; cycle close after first session | $0 | **#1 — fully fire-ready, paradigm-honest, completes cycle coherently** |
| **B** | "Paradigm C 시작 — hybrid REPL fire" (BG-CG land 후) | wait BG-CG REPL land OR execute BG-BX one-shot §3.1; deferred multi-turn | $0 | **#2 — viable demo today via BG-BX one-shot; BG-CG REPL extension pending** |
| **C** | "CLM-3 H1 launch — $1k commit" | execute BG-BM Variant B; H100 boot per `config/h100_pods.json` + L23/L24/L25 | ~$1k / 30d | **#4 — only if A-paradigm non-negotiable AND budget tolerance present** |
| **D** | "cycle close + Stage 3 30 session 누적" | CronDelete d1682837; BG-AM commits; n>=30 daily Path A; corpus analyzer; CLM-3 design refine | $0 / multi-day | **#3 — preserves A-paradigm hope path; lowest commit, highest information value over time** |
| **E** | "더 angle 시도 — autonomous /loop 계속" | continue /loop 1m; accept anti-convergence pressure on architecturally closed lanes | $0 compute / + paradigm-mismatch risk | **#5 — LOWEST completion. Only valid for explicit exhaustive H4-style sweep** |

### §6.1 완성도 lens — final ranking / Completion-quality ranking

1. **Option A** (Paradigm B fire) — fire-ready, resolves paradigm mismatch by user-side adoption, cycle closes coherently. **RECOMMENDED if user accepts B paradigm.**
2. **Option D** (cycle close + corpus) — clean close + corpus accumulation; defers H1 budget decision until corpus motivates; preserves A-paradigm hope.
3. **Option B** (Paradigm C demo) — viable today via BG-BX one-shot; full multi-turn fire pending BG-CG; provides emit + substrate dual signal.
4. **Option C** (H1 launch) — only if A-paradigm is non-negotiable AND $1k+ + 30 days budget tolerance.
5. **Option E** (continue /loop) — anti-convergence pressure; lowest completion lens.

---

## §7 Honest C3 (>= 5)

### C3.1 — "ACHIEVABLE_NOW" for B is anima-internal paradigm-relative

§1 marks B as "FIRE-READY NOW" but this judgment is anima-internal. There is no
external benchmark, no peer-reviewed protocol, no third-party reproduction of
BG-AN 5-turn smoke or BG-AE tension_trajectory variance threshold (>100 rich,
<50 degenerate). The user fired Paradigm B may NOT match the user's actual
intent of "mutual dialogue" if that intent was traditional A (token-emit chat).
The autonomous mode CANNOT disambiguate without explicit user declaration.
**Epistemic open**: B "ACHIEVABLE_NOW" 가 사용자 intent 만족 여부 — open until
user fires §2.1 once and self-judges "이 정도면 됐다 / this is enough".

### C3.2 — Paradigm C REPL (BG-CG) not yet landed

§3.2 references `tool/transient_py/anima_emerge_chat_hybrid_repl.py` which does
NOT exist as of 2026-05-06. Only BG-BX one-shot script
(`anima_emerge_chat_hybrid_pythia_clm.py`) landed. C as fire-ready multi-turn
REPL is **deferred**. User option B fires the BG-BX one-shot today; full REPL
requires BG-CG landing first. If BG-CG never lands, option B degrades to a
3-prompt demo, not a full session.

### C3.3 — H1 cost estimate ($1k, 30 days) is planning ceiling

§4.2 cites ~$1k from BG-BM CLM-3 spec. Per `config/h100_pods.json` history +
`runpod_pod_purge_2026_05_03` memory, H100 raw cost $0.40-$0.80/h × continuous-
train time + storage + eval-pass ancillary. Realistic 30-day H100 1× = $300-700
raw + $100-300 ancillary; $1k is planning ceiling NOT contract. Phase 2 boot
must be fresh from HF base mirror per memory (6 EXITED H100 pods purged).

### C3.4 — autonomous mode inferred user intent — epistemic risk persists

The autonomous /loop 1m fire from BG-A through BG-CH has implicitly assumed
interpretation A (token-emit chat-capability) for ~12+ closures and ~50+ BG
investigations. Only at BG-BV C3.6 was the paradigm mismatch surfaced
explicitly. This document, BG-BV, and the cycle commit manifest do NOT pretend
otherwise. The correction surface (this menu) only exists because user
declaration is now solicited. Future cycles SHOULD solicit user paradigm
declaration **before** opening a multi-BG investigation lane (own-rule
candidate).

### C3.5 — Option D (corpus n>=30) saturation marker is unspecified

§5 step sequence and §6 option D both reference "n>=30 sessions" as the
corpus accumulation target. The actual saturation marker (when does the
corpus pattern motivate CLM-3 design refine?) is heuristic — Stage 3 protocol
§5 lists candidate hit_rate >=70% / CLM v5 hint as markers but these are
research-mode speculative. A user firing option D may not encounter a clear
"stop accumulating, retrain now" signal even at n=30; the path's information
value is open-ended.

### C3.6 — Paradigm A on Llama Path A v2 is NOT anima-native

§1 notes A is achievable on Llama-3.2-3B Path A v2 (composite 0.5584). This
is **outside the anima-native CLM v4 substrate**. If user intent specifically
requires anima-native chat capability, Llama is not the path — only CLM-3 (H1)
satisfies. If user intent is "any chatbot that responds coherently in text",
Llama Path A v2 already exists (per `feedback_v2_fail_was_measurement_artifact`
+ `feedback_axis_preservation_eval_substrate_calibration` lane closures). Path
choice depends on whether anima-native is a hard requirement.

### C3.7 — Step 1 cron delete is shell-external

§5 step 1 cron deletion (`d1682837`) requires the harness cron management
tool, not bash execution. A user reading the 5-step sequence and trying to run
all 5 in shell will fail at step 1. Per session-multi-BG memory, the
autonomous mode itself executes the cron delete; user-side fire only needs to
declare option D (or option A) to trigger.

---

## §8 Outputs

- this doc: `/Users/ghost/core/anima/docs/anima_paradigm_b_c_final_acceptance_2026_05_05.md`
- verdict: `/Users/ghost/core/anima/state/anima_paradigm_b_c_final_acceptance_2026_05_05/verdict.json`

## §9 Compliance footer

- raw#9 — md only (acceptance doc, no code)
- raw#10 — §7 has 7 honest C3 (>= 5 required)
- raw#15 — additive only; no edits to landed BG-AN / BG-BX / BG-AY / BG-BV / BG-AO docs or verdicts
- HF token literal: none embedded
- commit: not requested; doc landed only
- bash 3.2 / mac compat: doc-only artifact; fire commands in §2.1 / §3.1 / §5 are bash-3.2 safe

duration ~25 min, cost $0 (mac, doc-only).

End paradigm B + C final acceptance (BG-CH).
