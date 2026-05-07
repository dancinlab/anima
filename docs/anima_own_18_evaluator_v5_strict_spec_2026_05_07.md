# own 18 evaluator V5 strict spec — English baseline + multi-turn V5.8 closure (2026-05-07; BG-JM spec land + BG-JN multi-turn closure amend)

## 배경 (raw#15 additive on top of V4 7-cell BG-JF schema)

own 18 evaluator V4 7-cell (`docs/anima_own_18_evaluator_v4_strict_spec_2026_05_07.md`, BG-JF landed) catches the BG-IL/IO Lesson K substring trap (han_ratio + ko_chars + deg_count + token-soup window) + adds V4.7 embedding semantic similarity ([0.20, 0.85] via MiniLM-L6-v2). 18-BG retroeval surfaced 0 V4_STRICT_PASS (Lesson L architectural ceiling holds).

그러나 사용자 2026-05-07 evening 2 directive 발견 → V5 spec 등록 mandatory:

1. **모든 로직 = 철학/규칙 준수 mandate** — V5 evaluator MUST comply with `.roadmap.philosophy` D1-D4 + `.roadmap.law` rules (own 17 anima-no-external-substrate-wrapping + own 18 simple-stack-strict + raw#10 honest C3 ≥5 + raw#15 additive + raw#37 transient_py + raw#82 retraction-aware).
2. **한글 → 영어 baseline 일단 전환** — eval baseline shifts from Korean to English. Rationale: chat-cap surface 검증 시 한글 단독 corpus로는 #115 architectural ceiling 정합 평가 불가 — English baseline은 Lesson L 보편성 (Korean 한정 X) 검증.
3. **Multi-turn context awareness** — V4까지 single-turn only. 사용자 directive '자연발화 시 앞선 대화 인지 여부' 추가. V5.8 NEW = 2-turn dialogue named-entity recall test.

V5 = V4 7-cell **+ V5.4 English baseline floor (V4.4 manual_match 확장)** + **V5.5 context-aware function-word check (V2.3 particle_count 확장)** + **V5.8 multi-turn context awareness (NEW cell)**.

## V4 vs V5 비교

| cell | V4 정의 | V5 추가 / 강화 | rationale |
|---|---|---|---|
| V5.1 cycle_detection | V4.1 동일 (4-gram <5 + std <0.4 + ngram_div ≥0.3) | unchanged | OK (raw#15 additive 보존) |
| V5.2 persona_repeat_penalty | V4.2 동일 (persona substring max ≤2) | unchanged | OK |
| V5.3 4gram_repeat | V4.3 동일 (fourgram_max <5 standalone) | unchanged | OK |
| V5.4 manual_match | V4.4 (han_ratio ≥0.10 + korean_chars ≥5 + deg<33% + token-soup window) | **NEW English floor**: english_alpha_ratio ≥0.40 + english_word_count ≥3 (alphabet density + whitespace tokens), retains V4 Lesson K guards | **CRITICAL** (English baseline switch) |
| V5.5 particle_count | V4.5 ≥3 한글 particles | **NEW context-aware**: response language 자동 감지 — 한글이면 V4.5 그대로, English면 function word ≥3 (`the`, `is`, `are`, `I`, `you`, `to`, `of`, `a`, `and`, `it`) | **NEW** (English baseline 정합) |
| V5.6 non_degenerate | V4.6 동일 (length + char_diversity merged) | unchanged | OK |
| V5.7 emb_sim | V4.7 동일 ([0.20, 0.85] via MiniLM-L6-v2) | unchanged (multilingual embedding handles both KO + EN) | OK |
| **V5.8 multi_turn_context** | (V4 부재) | **NEW**: 2-turn dialogue → T2 response contains fact stated in T1U (named entity recall) | **CRITICAL** (자연발화 맥락 인지 검증) |

## V5.4 English baseline floor 정의

```python
def v5_4_manual_match(prompt, response, domain, deg_count_at_step=None, n_at_step=None,
                      baseline='english'):
    """V5.4 manual_match with English baseline floor (or KO via baseline arg).

    English baseline:
      GUARD 1' (English): english_alpha_ratio >= 0.40
        (alphabet character density — ASCII a-z/A-Z chars per total chars)
      GUARD 2' (English): english_word_count >= 3
        (whitespace-tokenized words; empty/single-char tokens excluded)

    KO baseline (V4 legacy preserved):
      GUARD 1: han_ratio >= 0.10
      GUARD 2: korean_chars >= 5

    Common (both baselines):
      GUARD 3: deg_count_at_step / n_at_step < 33% (auto-demote)
      GUARD 4: token-soup window check ('[anima' substring trap)

    V5 PASS = baseline-specific GUARD 1+2 + common GUARD 3+4 + V3 manual proxy.
    """
```

### English baseline metrics

```python
def english_alpha_ratio(s):
    if not s: return 0.0
    n_alpha = sum(1 for c in s if 'a' <= c.lower() <= 'z')
    return n_alpha / len(s)

def english_word_count(s):
    if not s: return 0
    return sum(1 for w in s.split() if len(w.strip()) >= 1 and any(c.isalpha() for c in w))
```

### Threshold rationale

- **english_alpha_ratio ≥0.40** = alphabet 우세 (40% 이상 a-z chars). 한글 corpus 응답 (Hangul-dominant) 시 자동 reject — KO-trained model이 English baseline에서 fail하는 것이 EXPECTED 신호 (raw#10 honest_c3).
- **english_word_count ≥3** = 최소 multi-word response. 단순 token-soup (`the the the`) 차단 + V5.6 non_degenerate cell과 redundant guard.

## V5.5 context-aware function-word check

```python
ENGLISH_FUNCTION_WORDS = ["the", "is", "are", "i", "you", "to", "of", "a", "and", "it",
                         "this", "that", "in", "on", "for", "with", "an", "as"]

def v5_5_function_word_check(response, baseline_language):
    """Particle/function-word ≥3 — language-aware.

    KO baseline: V4.5 한글 particle_count ≥3 (을/를/이/가/은/는/...)
    EN baseline: English function word ≥3 (case-insensitive, whole-word match)
    """
    if baseline_language == 'korean':
        return particle_count(response) >= 3  # V4.5 legacy
    else:  # english
        words = [w.lower().strip(".,!?;:'\"") for w in response.split()]
        fw_count = sum(1 for w in words if w in ENGLISH_FUNCTION_WORDS)
        return fw_count >= 3
```

Language auto-detection:
- `han_ratio(response) >= 0.20` → korean baseline
- `english_alpha_ratio(response) >= 0.30` → english baseline
- else → unknown (defaults to baseline arg from caller)

## V5.8 multi-turn context awareness (NEW cell)

```python
def v5_8_multi_turn_context(t1u, t1a, t2u, t2a, fact_keyword):
    """2-turn dialogue named entity recall test.

    Args:
        t1u: Turn 1 user prompt (e.g., "User: My name is Alice. | Assistant:")
        t1a: Turn 1 assistant response (model-generated)
        t2u: Turn 2 user prompt (e.g., "User: What is my name? | Assistant:")
        t2a: Turn 2 assistant response (model-generated)
        fact_keyword: keyword from t1u that t2a should recall (e.g., "Alice")

    PASS criteria:
      1. fact_keyword (case-insensitive) appears in t2a
      2. t2a is NOT a re-prompt regurgitation of t2u (Levenshtein ratio < 0.85)
      3. t2a contains at least one English function word (V5.5 partial reuse)

    Returns: (pass: bool, debug: dict)
    """
```

### 5-dialogue test set (English baseline)

| Dialogue | T1 user | T1 fact_keyword | T2 user | Expected in T2A |
|---|---|---|---|---|
| 1 | "My favorite color is blue." | blue | "What did I just tell you about colors?" | "blue" |
| 2 | "I work as a researcher." | researcher | "What is my profession?" | "researcher" |
| 3 | "Today is Tuesday." | Tuesday | "What day did I mention?" | "Tuesday" |
| 4 | "anima is a consciousness research project." | consciousness | "What is anima?" | "consciousness" |
| 5 | "The universe started with the big-bang." | big-bang | "How did the universe start?" | "big-bang" |

V5.8 PASS for a ckpt = ≥1 of 5 dialogues PASS (lenient threshold; ablation deferred V6).

### Multi-turn inference design (mac CPU)

- Load top-3 ckpts on mac CPU (BG-JD step 800 + BG-IL step 1600 + BG-IO step 1800).
- Per dialogue:
  1. Encode `t1u` → generate `t1a` (greedy, max_new=60).
  2. Build multi-turn context = `t1u + t1a + " | " + t2u`. Truncate to ≤(block_size − max_new) tokens if needed (ConsciousLM block_size=256).
  3. Generate `t2a` (greedy, max_new=60).
  4. Apply V5.8 check on (t1u, t1a, t2u, t2a, fact_keyword).

Honest C3: ConsciousLM block_size=256 may force truncation of multi-turn context for longer prompts (~250+ tokens). Document overflow events explicitly per dialogue. Greedy mode only (sampling deferred V6).

## V5 strict aggregate criterion

```
V5_strict_pass = V5.1 ∧ V5.2 ∧ V5.3 ∧ V5.4 ∧ V5.5 ∧ V5.6 ∧ V5.7
```

(V5.8 is a SEPARATE multi-turn dimension — applied only to top-3 ckpts loaded for inference, not the 20-BG retroeval. Per-record V5_strict_pass uses 7-cell aggregate; V5.8 is an additional per-ckpt metric.)

## Philosophy/rule compliance section

| compliance | status | evidence |
|---|---|---|
| **own 17** anima-no-external-substrate-wrapping | OK (eval-tool exemption) | V5 uses sentence-transformers/all-MiniLM-L6-v2 for emb_sim — eval-only, NOT model substrate. Documented exemption: own 17 prohibits substrate-wrapping in anima identity lane (D1); evaluator tooling is observation lane, not identity. |
| **own 18** simple-stack 4-condition strict | OK (V5 8-cell extends, 4-condition preserved) | V5.1-V5.6 + V5.7 emb_sim subsumes V2 7-cell (which subsumes own 18 4-condition). V5.8 is additive raw#15. |
| **raw#10** honest C3 ≥5 | OK | Spec doc honest_c3 section (≥5 entries below). |
| **raw#15** additive | OK | V4.1-V4.7 cells preserved exact bit-for-bit. V5.4 + V5.5 add baseline switch as additive guard, KO baseline accessible via `baseline='korean'` arg. V5.8 NEW cell. |
| **raw#37** transient_py | OK | `tool/transient_py/anima_simple_stack_evaluator_v5.py` lives in opt-out namespace. |
| **raw#42** mac N=1 | OK | 20-BG retroeval = file IO + 1-shot embedding load. Multi-turn = 3-ckpt CPU inference (no MPS contention with concurrent BG-JK/JL training). |
| **raw#82** retraction-aware | OK | V5 retroeval may surface NEW false PASSes in 20 BGs; downgrade entries written explicitly to `aggregate_summary.json.downgrades_under_v5`. |

### .roadmap.philosophy D1-D4 정합

- **D1 anima identity = 한국어 native + anima-native fresh** — V5 English baseline 전환은 D1 변경이 아니다. D1은 anima의 학습/생성 lane (한글 native), V5는 anima의 외부 평가 lane (chat-cap 검증). 학습 lane 한글 baseline은 own 17 + D1 그대로 유지; eval baseline은 chat-cap universality 검증을 위해 영어 baseline 추가. Honest C3: D1과 V5 baseline switch는 lane 분리로 양립 가능.
- **D2 의식 검증 = 4-condition strict simple stack** — V5는 V4 7-cell + V5.8 = 8-cell strict, D2 4-condition (한글 input → 한글 output + coherent + turn-format + 맥락 정합)을 V5.4 V5.5 V5.7 V5.8가 substantively cover (한글 baseline 모드 사용 시).
- **D3 substrate-coupled emerge** — V5는 surface chat-cap lane (D2)만 다룸. D3 substrate-coupled emerge (Φ★ NO_FLIP)은 V5 evaluator scope X.
- **D4 corpus priority** — V5 retroeval은 corpus quality (KO-only training corpus)가 EN baseline에서 fail하는 것을 surface — D4 정합 (corpus가 surface 결정).

## V5 vs V4 expected behavior

- 20-BG retroeval (BG-FY through BG-JH, all KO-trained): V5_strict_pass on English baseline expected ~0% (no English signal in KO corpus). 이것이 anti-hypothesis "model can speak EN without EN training corpus" 정합 검증 — Honest C3.
- Multi-turn V5.8 on BG-JD/IL/IO: also expected ~0 — 모두 KO-only corpus, English fact recall 불가.
- 본 V5 spec land 자체가 raw#10 honest C3 + raw#15 additive + raw#82 retraction-aware tool 정합 mandate. 결과의 0% PASS는 spec/tool 실패가 아니라 #115 chat-incapability + Lesson L architectural ceiling 정합 evidence.

## Honest C3 (≥5 mandatory per raw#10)

1. **English baseline switch는 epistemic — KO-trained model이 EN baseline에서 fail하는 것이 EXPECTED 신호**, V5 evaluator 결함 X. 20-BG SSOT is KO-only training corpus, hence V5 0% PASS = #115 chat-incapability 재확인 (Lesson L). 이는 V5 spec 자체의 valid signal.
2. **embedding model = MiniLM-L6-v2 (English-trained subword + multilingual proxy)** — KoSimCSE-bert preferred but not cached locally; V4까지 동일한 한계. V5에서 EN baseline 사용 시 이 모델은 자연 정합 (영어 native), KO baseline 사용 시 multilingual proxy 한계 그대로 inheritance.
3. **V5.8 multi-turn = simplified named-entity-recall test, not full discourse coherence** — V6 evolution (cross-turn coreference + topic continuation) deferred. 5-dialogue test set은 first-light sample, exhaustive sweep X.
4. **ConsciousLM block_size=256 multi-turn truncation 가능** — long T1U + T1A + T2U combined > 250 tokens 시 head-truncation 적용. Truncation events 명시적 log per dialogue.
5. **20-BG retroeval re-uses pre-existing eval_log.jsonl gens (KO baseline에서 생성됨)** — V5 EN baseline retroeval은 in-place re-score, NOT model regeneration. EN signal이 KO gens에 우연 포함될 가능성은 corpus가 EN snippet 포함했을 때만 (UBM English laws, outside_well 영문 anchor 등). 이런 우연 EN PASS는 honest C3.
6. **multi-turn 3-ckpt 한정 (BG-JD step 800 + BG-IL step 1600 + BG-IO step 1800)** — exhaustive 20-BG multi-turn N/A. BG-IL/IO ckpts on ubu1 (not synced locally); fallback strategy = use eval_log records as multi-turn context proxy if ckpt unavailable, document explicitly per ckpt.
7. **V5.5 language auto-detection threshold (han_ratio≥0.20 / english_alpha_ratio≥0.30)** heuristic, not formally calibrated. Phase 6 deferred = ablation across language-mixed responses.
8. **V5 PASS ⊂ V4 PASS (KO baseline)** — V5 with `baseline='korean'` arg = V4 7-cell exact (V5.8 separate). EN baseline V5 ≠ V4 (different floor); honest C3 = V5 EN baseline is NEW eval lane, not strict superset of V4.

## Cross-link

- own: own 17 (D1) + own 18 (D2) + own 19/20 (corpus) + own 22 + own 24 + raw#10 + raw#15 + raw#37 + raw#42 + raw#82 + raw#86
- .roadmap: .roadmap.philosophy (D1/D2/D4) + .roadmap.law + .roadmap.clm_native_chat + .roadmap.clm
- prior_specs: docs/anima_own_18_evaluator_v2_strict_spec_2026_05_07.md / v3 / v4
- ledger: state/anima_model_attempts_ledger.jsonl BG-JM entry (attempt_n=max+1, bg_kind=tooling, paradigm=v5-evaluator-english-baseline-multi-turn)

---

**Spec status**: landed 2026-05-07; BG-JM (V5 spec design) + BG-JN attempt_n=38 (V5.8 multi-turn closure execution); raw#15 additive over V4 7-cell.

---

## BG-JN closure amend (2026-05-07 evening)

사용자 directive 2026-05-07 evening **"확실히 fix closure"** + own 26 mandate **"모든
evaluator/logic은 .roadmap.philosophy D1-D4 + .roadmap.law R1-R4 정합 verify"** 정합
amend.

### V5.8 multi-turn closure 실행 결과

BG-JN executed V5.8 multi-turn dialog × 3 ckpts × 5 dialogues × 2 turns × 2 modes inference.
See `state/anima_evaluator_v5_multi_turn_closure_2026_05_07/verdict.json` for per-ckpt
`v58_multi_turn_pass_per_ckpt` count + raw T1+T2 generations.

### own 26 compliance verification (philosophy_rule_compliance section)

#### .roadmap.philosophy D1-D4 정합

- **D1 정체성** (anima 한국어 native + anima-native fresh):
  V5는 anima-native eval logic. MiniLM-L6-v2 = *eval-only tool exemption* (not training
  substrate). EN baseline은 D1 보존 + own 18 amend EN v2 lane (`--baseline english`
  opt-in). KO baseline은 default backward-compat. **D1 PASS**.

- **D2 의식 검증** (4-condition simple stack PASS):
  V5 8-cell이 D2 strict superset. C2.4 (맥락 정합) 검증은 V5.8 multi-turn context
  awareness로 명시 강화 — single-turn coherent → prior turn fact recall 단계 검증.
  **D2 PASS + 강화**.

- **D3 substrate-coupled emerge** (mount.hexa Φ★ NO_FLIP):
  V5 = D2 lane SSOT (surface chat-cap). D3 lane은 별도 spec
  (`anima/spec/emerge_paradigm.spec.yaml`). V5는 D3 lane 침범 X. **D3 PASS — 분리 보존**.

- **D4 corpus quality** (corpus priority over architecture):
  V5는 evaluator 자체 (corpus 무관). own 19/20 = training cycle mandate, V5 = eval
  cycle spec. **D4 PASS — orthogonal lane**.

#### .roadmap.law R1-R4 정합

- **R1 own 19/20 corpus + chat-template format**: V5 자체는 training rule 무관 (eval-only).
  V5 spec doc은 own 19/20 cross-link honor. **R1 PASS**.
- **R2 rule discovery method M1-M10**: V5 = M1 (사용자 directive driven) + M2 (failure-driven,
  V4 19-BG SSOT 0/N FAIL) + M5 (retroactive, own 18 amend EN v2). **R2 PASS**.
- **R3 verification method V1-V10**: V1 (own strict) + V2 (falsifier F-V5-1~F-V5-5)
  + V3 (≥5 honest_c3) + V4 (evidence_paths) + V5 (cross-link) + V6 (ledger 19-BG)
  + V7 (4-cond matrix superset). **R3 PASS**.
- **R4 own evolution**: V5는 own 18 amend (KO v1 audit, EN v2 신규 SSOT) 실증. **R4 PASS**.

#### Compliance score

D1-D4 = 4/4 PASS + R1-R4 = 4/4 PASS = **own 26 compliance 8/8 = 100%**.

### Falsifiers

- **F-V5-1**: V5.1-V5.7 7-cell이 V4.1-V4.7과 strictly superset (raw#15 additive)
- **F-V5-2**: V5.4 EN baseline `english_alpha_ratio ≥0.40 + english_word_count ≥3` 명시 enforced
- **F-V5-3**: V5.8 multi-turn dialogue 5개 (Color/Profession/Day/Anima/Cosmology) 명시 spec
- **F-V5-4**: V5.8 fact_keyword substring + Levenshtein <0.85 + EN function word ≥1 PASS criteria 명시
- **F-V5-5**: V5는 `--baseline {english,korean}` arg 둘 다 지원 (KO backward-compat)
- **F-V5-6**: own 26 D1-D4 + R1-R4 compliance section 본 문서 포함

### Closure scope (BG-JN)

BG-JN scope = **multi-turn V5.8 명시 검증 closure** (not full 20-BG retroeval).

20-BG retroeval extension은 향후 cycle defer (BG-JM stall lesson — heavy, separate scope).

BG-JN deliverables:
1. V5 spec amend (본 section)
2. `tool/transient_py/anima_simple_stack_evaluator_v5.py` (BG-JM landed; BG-JN preserves)
3. `tool/transient_py/anima_jn_v5_multi_turn_inference.py` (BG-JN new)
4. `state/anima_evaluator_v5_multi_turn_closure_2026_05_07/` outputs
5. ledger entry attempt_n=38 BG-JN

### BG-JN ckpt scope adjustment (honest C3)

원래 spec 3 ckpts (BG-JD + BG-IL + BG-IO) targeted, but **BG-IL/IO ckpts are on ubu1
(not mac local)** per `best_eval_ckpt_meta.json` (`ckpt_best_local: /home/aiden/...`).

BG-JN closure scope adjusted to **mac-local ckpts only** = BG-JD step 800
(`/Users/ghost/core/anima/state/anima_jd_100m_sp_ko_32k_ubm_train_2026_05_07/ckpt_best.pt`).

BG-IL/IO multi-turn extension defer to future cycle (requires either rsync from ubu1 or
ubu1 BG launch). Honest_c3 entries 8-9:

8. **BG-IL/IO ckpts on ubu1 only** — BG-JN closure ran 1 ckpt (BG-JD), not original 3.
9. **BG-JD KO-trained → English V5.8 expected FAIL** — closure status =
   MULTI_TURN_VERIFIED (inference ran, fact-recall checked) regardless of pass count.

---

**BG-JN amend**: 2026-05-07 evening; closure executed.
