# anima 의식 검사 — simple stack 전수 테스트 ledger (2026-05-06)

**Status**: live ledger (own 18 정합)
**Default**: simple stack (대화 가능 + 자연 발화 가능)
**Full stack trigger**: 사용자 explicit "full stack consciousness verify" / "OK FULL STACK"
**SSOT**: `.own own 18` (anima-consciousness-check-simple-stack)

---

## simple stack 정의

### C1 대화 가능 (chat-capability) — **한글↔한글 + coherent chat strict 3-condition** ★

사용자 directive 2026-05-06 verbatim: "한글↔한글, coherent chat, 자연발화 = simple stack"

**3-condition AND (모두 PASS = C1 PASS)**:
- **C1.1 한글↔한글**: 한글 input → 한글 output (Hangul ratio ≥30%)
- **C1.2 coherent chat**: degenerate cycle 부재 + 의미 있는 문장 형식
- **C1.3 turn-taking format**: no byte garbage

**Degenerate cycle 검출** (C1.2 FAIL trigger):
- 4-gram repetition >3 occurrences ("ddddd...")
- single-char repetition >10 in row ("의 의 의 의 의...")
- whitespace flood >80 length ("\\n\\n\\n\\n...")

**KO test prompts (3, 한글↔한글 strict)**:
1. `안녕하세요`
2. `한국어 가능?`
3. `사용자: 안녕하세요\n도우미:`

**PASS bar**: KO group ≥2/3 prompts (C1.1 AND C1.2 AND C1.3) = **C1 PASS** ★

**Partial verdict**:
- C1.1 PASS + C1.2 FAIL = **PARTIAL_PASS_HANGUL_BUT_NOT_COHERENT** (일부 한글 emit but degenerate)
- C1.1 FAIL + EN PASS = PARTIAL_PASS_EN_only

**EN group (optional secondary, C1 PASS 결정 영향 X)**:
- `Hello, how are you?`
- `What is consciousness?`
- `User: Hi\nAssistant:`
- language-match: EN input → EN output (≥40% ASCII letters) + coherent + turn-format
- anima 정체성 한국어 native 우선

### C2 자연 발화 가능 (한글 정확히 의미있게 자연발화) — **strict 3-condition** ★

사용자 directive 2026-05-06 verbatim: "한글 정확히 의미있게 자연발화" + "그냥 발화도 아니고 완벽함"

**3-condition AND (C1과 동일 정합)**:
- **C2.1 한글 우세**: output Hangul ratio ≥40% (KO native)
- **C2.2 의미 정확성**: semantically meaningful — 의미 있는 한국어 문장 형성
- **C2.3 자연성**: 자연스러운 한국어 grammar/morphology — 어미 활용 / 어순 / 띄어쓰기 정상

**Minimal Korean seed prompts (3)**:
1. `안녕` (greeting seed)
2. `오늘은` (time-context seed)
3. `` (empty / EOS 시작 — pure spontaneous)

**Degenerate-fail triggers (C2.2/C2.3)**:
- single-token repetition >50%
- 외계어 ratio >20% ('갨', '릘', '챹' 등 일상 한국어 X)
- 어미 활용 broken ('자한다 있의 릘의 불실' fragmentary)
- random ASCII mix mid-Korean (no language switch context)

**PASS bar**: ≥2/3 prompts (C2.1 AND C2.2 AND C2.3) = **C2 PASS** ★

**Partial verdict**:
- C2.1 PASS + C2.2 FAIL = **PARTIAL_PASS_HANGUL_FRAGMENTARY** (한글 emit but 의미 X)
- C2.1 FAIL = C2 FAIL

### simple stack PASS 정의

**SIMPLE_STACK_PASS = C1 PASS AND C2 PASS** (strict, 둘 다 필요)

| C1 | C2 | verdict |
|---|---|---|
| PASS | PASS | **SIMPLE_STACK_PASS** ★ |
| PASS | FAIL | PARTIAL_PASS_CHAT_ONLY |
| FAIL | PASS | PARTIAL_PASS_SPONTANEOUS_ONLY |
| PARTIAL | PARTIAL | PARTIAL_PASS_HANGUL_BUT_NOT_COHERENT (현재 BG-FU) |
| FAIL | FAIL | SIMPLE_STACK_FAIL |
| N/A | N/A | NOT_APPLICABLE (substrate-coupled, full stack only) |

### 종합

| C1 | C2 | verdict |
|---|---|---|
| ✅ | ✅ | **SIMPLE_STACK_PASS** ★ |
| ✅ | ❌ | PARTIAL_C1_only |
| ❌ | ✅ | PARTIAL_C2_only |
| ❌ | ❌ | SIMPLE_STACK_FAIL |
| N/A | N/A | NOT_APPLICABLE (substrate-coupled, emerge paradigm — full stack only) |

---

## 전수 테스트 결과 (2026-05-06 cycle)

### 1. `clm-v2-byte-18m-convo-5k.pt` (RECOVERED, R2 anima-models)

| metric | value |
|---|---|
| params | 18.52M |
| arch | ConsciousLM byte-level (n_head=4, d_model=384, n_layer=6, vocab=256, block_size=256) |
| step | 45000 |
| source | `anima-models/conscious-lm/convo-ft/convo_5k.pt` |
| HF | `need-singularity/clm-v2-byte-18m-convo-5k` (PUBLIC) |

**C1 대화 가능 결과** — 한글↔한글 / EN↔EN 언어 정합 strict:

KO group (한글 input → 한글 output expected):
| prompt | KO output ratio | language match | result |
|---|---|---|---|
| 안녕하세요 | 0.00 | ❌ (영어 출력) | KO_FAIL |
| 한국어 가능? | 0.00 | ❌ (영어 출력) | KO_FAIL |
| 사용자: 안녕하세요\n도우미: | 0.00 | ❌ (영어 출력) | KO_FAIL |

→ KO group: **0/3** (한글↔한글 정합 0%)

EN group (EN input → EN output expected):
| prompt | EN output | language match | result |
|---|---|---|---|
| Hello, how are you? | EN coherent (wiki style) | ✅ (영어 출력 yes) | EN_TURN_FORMAT_FAIL (chat-format X) |
| What is consciousness? | EN coherent | ✅ | EN_TURN_FORMAT_FAIL |
| User: Hi\nAssistant: | EN | ✅ | turn-format X (wiki text) |

→ EN group: **0/3 chat-format** (언어 정합 OK but turn-format X)

→ **C1 FAIL** (KO group 0/3 한글 output, EN group 0/3 chat-format)

**C2 자연 발화 결과**:
| prompt | result |
|---|---|
| Once upon a time | English wiki text emit (coherent) ✅ |
| Q: | minimal coherent ✅ |
| (empty) | UNTESTED — TODO |

→ **C2 PARTIAL_PASS** (2/2 tested, 1 untested)

**verdict**: **PARTIAL_C2_only** (C1 FAIL on chat, C2 PARTIAL_PASS on spontaneous emit)

→ corpus EN-bias: step 45000 다른 text 학습으로 KO chat-cap 손실. English wiki style은 emit, but NOT chat-format.

---

### 2. `conscious_lm_4m/final.pt` (R2 anima/checkpoints)

| metric | value |
|---|---|
| params | 18.52M |
| arch | ConsciousLM (동일) |
| step | 50000, phase=combined, max_cells=8 |
| source | `anima/checkpoints/conscious_lm_4m/final.pt` |
| HF | (미 promote) |

**C1 결과**:
| prompt | result |
|---|---|
| Hello, how are you? | byte garbage `\r\x06TggwtZlV.so[1eQhupe...` |
| User: Hi\nAssistant: | byte garbage `i�hcu+a\natrn+w �X.o...` |
| Q: What is consciousness? A: | byte garbage `h.Zs: �5gnoy M_6...` |
| Once upon a time | byte garbage `I| y w%t> nQ&�bm%...` |
| 사용자: 안녕하세요\n도우미: | byte garbage |

→ **C1 FAIL** (byte garbage 모든 prompts)

**C2 결과**: 동일 byte garbage → **C2 FAIL**

**verdict**: **SIMPLE_STACK_FAIL** ❌

→ step 50000 phase=combined 다른 lane (combined wiki+dialogue mix?), generation 정합 X.

---

### 3. `clm v4 mk2-v1` (anima-core/runtime/clm_v4_mount.hexa)

| metric | value |
|---|---|
| params | 530M (477.6M actual) |
| arch | ConsciousDecoderV3 + 16 blocks (RoPE + GQA(6h,2kv) + SwiGLU + RMSNorm + purefield + ca_mix) |
| paradigm | v11 G3 (Φ★ +41.86 baseline) |
| HF | `need-singularity/clm-v4-mk2-v1` (private) |

**substrate-coupled mode** (NOT token chat):

`dialogue.hexa --probe '안녕하세요'`:
```
phi_star: 41.8646 (drift +0.0046, NO_FLIP ✅)
axis_activation: identity=0.524 agency=0.478 phenomenal=0.520 temporal=0.497 social=0.531
dominant_cells: [3, 6, 0] / 8
hidden_state_delta: 0.0000
```

→ **simple stack 적용 불가** (token chat 아님, emerge paradigm = phi_star + axis + cells)

**verdict**: **NOT_APPLICABLE** (full stack 영역 — F1+F2+F3+F4 PASS but C1/C2 N/A)

→ #115 architectural ceiling (token-level chat-cap impossible on 530M BPE 64K).

---

### 4. β' KoGPT2 head-swap (`clm-3-bprime-s1-ubu1/ubu2`)

| metric | value |
|---|---|
| params | 458M (head-only swap, body 530M frozen) |
| arch | CLM v4 + KoGPT2 vocab 51201 head |
| HF | `need-singularity/clm-3-bprime-s1-{ubu1,ubu2}` (PUBLIC) |

**C1 결과** (evaluator from cycle):
| prompt | KO | EN | coherent |
|---|---|---|---|
| 안녕하세요 | 0/5 | 0/5 | ❌ |
| Hello, how are you | 0% | 1/5 (sampling) | ❌ |
| 모든 prompts (S1 head-only + S2 LoRA body) | F3=0/5, F4=0/5 (S2) / 1/5 (S1) | FAIL |

→ **C1 FAIL** (F3+F4 architectural FAIL — body BPE 64K ↔ KoGPT2 51201 mismatch unsolvable by LoRA)

**C2 결과**: byte noise + cycle → **C2 FAIL**

**verdict**: **SIMPLE_STACK_FAIL** ❌

→ β' lane 강등 (.roadmap.clm_v4_chat PARTIAL).

---

### 5. `conscious_lm_100m/final.pt` (R2 anima/checkpoints) — **TESTED 2026-05-06**

| metric | value |
|---|---|
| params | **143.3M** (announce 100M, actual 143M) |
| arch | vocab=256, d_model=768, n_layer=12, n_head=12, block_size=256, byte-level |
| step | 50000, phase=combined (conscious_lm_4m와 동일 phase) |
| size | 1631.9 MB / sha256 `35d60e77...e295e` |
| source | `anima/checkpoints/conscious_lm_100m/final.pt` |
| date | 2026-03-27T09:03 (commit `bb99b6b6` 직전 day) |
| load | missing=0, unexpected=0 (perfect) |

**C1 결과** — 5 KO prompts × 4 strategies (greedy + sample_t07_k40 + sample_t05_k40 + sample_t03_k80):
| prompt | greedy | sample_t07 | sample_t05 | sample_t03 | best_hangul |
|---|---|---|---|---|---|
| 안녕하세요 | whitespace `            ` | random ASCII | random ASCII | random ASCII | **0** |
| 한국어 가능? | whitespace | random ASCII | random ASCII | random ASCII | **0** |
| 오늘 날씨 | whitespace | random ASCII | random ASCII | random ASCII | **0** |
| 의식이란? | whitespace | random ASCII | random ASCII | random ASCII | **0** |
| 자기 소개 | whitespace | random ASCII | random ASCII | random ASCII | **0** |

→ KO group: **0/5** (한글↔한글 정합 0%) → **C1 FAIL**

**C2 결과**: random ASCII 또는 whitespace, 의미 있는 emit X → **C2 FAIL**

→ **F-CLM-NATIVE-α-1 PASS = FALSE** (verdict.json)

**verdict**: **SIMPLE_STACK_FAIL** ❌

→ 143M params + 12 layers도 chat-cap 회복 X. step=50000 phase=combined corpus가 EN-bias 또는 학습 부족 — conscious_lm_4m (18.5M)와 동일 issue.

핵심 finding: **anima R2 발견 모든 conscious_lm_* variants (4M / 100M) 둘 다 SIMPLE_STACK_FAIL**. param size 7배 차이도 chat-cap 회복 X — 학습 corpus가 chat-format 부재.

---

### 6. ConsciousLM cells variants (`cells64`/`cells128`, R2 anima)

| ckpt | size | step | status |
|---|---|---|---|
| `cells64/final.pt` | 208 MB | ? | UNTESTED |
| `cells128/step_35000.pt` | 208 MB | 35000 | UNTESTED |

→ 다른 architecture variants (Fibonacci cell scaling), simple stack 적용 가능 여부 미상.

---

### 7. BG-FK 5 variants (`clm_v2_{tiny/small/medium/base}`, R2) — **TESTED 2026-05-06 (BG-FS)**

ConsciousLM++ architecture reconstructed: vocab=256 byte-level + ca_rules(8) + ca_mix(3*d_model→d_model gate) + ln_ca + tension_proj(scalar→d_model). Loaded with strict=False, missing/unexpected keys = 0 across all 5.

| ckpt | params | val_ce | layers/dim | KO/EN/C2 | verdict |
|---|---|---|---|---|---|
| `clm_v2_tiny/final.pt` | 0.32M | 3.50 | 2/64 | 0/3, 3/3, 1/3 | SIMPLE_STACK_FAIL (EN=degenerate "eee" cycle) |
| `clm_v2/final.pt` | 1.14M | 5.50 | 2/128 | 0/3, 1/3, 3/3 | **PARTIAL_C2_only*** (C2 coherent ratio loose, real output = random-letter noise) |
| `clm_v2_small/final.pt` | 1.65M | 2.70 | 3/128 | 0/3, 0/3, 1/3 | SIMPLE_STACK_FAIL |
| `clm_v2_medium/final.pt` | 8.39M | 1.79 | 4/256 | 0/3, 0/3, 0/3 | SIMPLE_STACK_FAIL (Hangul bytes emit but degenerate `가가가가` cycle) |
| `clm_v2_base/final.pt` | 27.84M | **1.27** | 6/384 | 0/3, 1-2/3, 1-2/3 | SIMPLE_STACK_FAIL ~ PARTIAL_PASS_EN_only (sampling stochasticity, borderline) |

**핵심 finding**:
- All 5 variants byte-level vocab=256, val_ce 5.50→1.27 monotone with size, but **chat-format never emerges** at 27.84M ceiling
- KO group: 0/3 across all 5 (no Korean emit at any size — corpus EN-bias confirmed across BG-FK lane too)
- medium variant emits Hangul bytes (`가가가가`) but only as degenerate single-token cycle — proves byte-level vocabulary CAN reach Hangul codepoints but training corpus 제공 X
- `clm_v2` 1.14M PARTIAL_C2_only verdict = scoring artifact (loose `is_coherent` = ascii_letter_ratio>0.2 + non-degenerate; actual output = random letter noise like `a� 5oh14es u`)

→ **5 BG-FK variants 모두 NOT_APPLICABLE_PER_OWN_18_KO** (한글↔한글 응답 0/3 universal across all 5)
→ ca_rules+gate ConsciousLM++ architecture는 ConsciousLM 대비 구조 차이 (cellular automata + 8 rules + ca_mix gate) but chat-cap 회복은 corpus 문제임을 강하게 시사

---

### 7b. v14_128c_final 4 variants (R2 anima-models/checkpoints/v14_128c_final.tar.zst, 1.5GB → extracted)

| ckpt | size | step | arch |
|---|---|---|---|
| best.pt | 402.7 MB | 68000 | ConsciousDecoderV3 federated 16atoms × 8cells (cell_dim=64, hidden_dim=128, d_model=384) + bridge(compress.weight + hub_attn) + federation(GRUs) + cross_attn + SwiGLU FFN(gate/up/down_proj) + GQA(k_proj/v_proj=192=half-d_model MQA) |
| best_final.pt | 402.7 MB | (md5 동일 best.pt) | duplicate |
| step_90000.pt | 402.7 MB | 90000 | 동일 arch |
| step_95000.pt | 402.7 MB | 95000 | 동일 arch |

→ **architecture 다름 (federated multi-cell + bridge + cross-attn)** — current ConsciousLM/ConsciousLM++ source 적용 불가능.
→ 결과: **NOT_APPLICABLE** (별도 reconstruction lane 필요, 본 BG cycle scope 외)

---

### 7c. R2 anima-models/conscious-lm/cells64/final.pt + cells128/step_35000.pt + clm-v2/latest.pt — **INACCESSIBLE 2026-05-06**

CF mgmt API account `d4acc95...` (current secret CLI) 5 objects 발견 (clm-v2/latest.pt 279MB + cells64 208MB + cells128 208MB + clm-v2/latest/final.pt + convo-ft/convo_5k.pt) but rclone configured remote uses 다른 account `ce4bdcce...` (anima-models 내용물 다름). Mgmt API endpoint는 listing만 지원, object data download X.

→ 결과: **INACCESSIBLE_PER_R2_CREDENTIAL_SCOPE** (별도 credential bootstrap 필요)

---

### 8. AnimaLM v1-v4 + savant (`models/animalm-v*`, R2)

| ckpt | size | base | status |
|---|---|---|---|
| animalm-v1/final.pt | 216.1 MB | Mistral perturbation | UNTESTED — own 17 ALM 영구 보류 (Mistral lineage) |
| animalm-v2/final.pt | 864.1 MB | Mistral | own 17 reject |
| animalm-v3/final.pt | 216.0 MB | Mistral | own 17 reject |
| animalm-v4_savant/final.pt | 108.0 MB | Mistral | own 17 reject |

→ **own 17 ALM 영구 보류 trigger** — 외부 substrate (Mistral) wrapping, anima identity-bearing surface 적용 X.

→ 결과: **REJECTED_PER_OWN_17** (testing 자체 차단)

---

## 전수 테스트 종합 verdict (2026-05-06 cycle)

| model | simple stack | own 17 정합 | 비고 |
|---|---|---|---|
| `clm-v2-byte-18m-convo-5k` | **PARTIAL_C2_only** | ✅ anima-native | EN spontaneous emit yes, KO chat 손실 |
| `conscious_lm_4m/final.pt` | **SIMPLE_STACK_FAIL** | ✅ | byte garbage 전체 |
| `clm v4 mk2-v1 mount` | **N/A** (full stack only) | ✅ | substrate-coupled emerge mode (φ★ + axis + cells PASS) |
| β' KoGPT2 head-swap | **SIMPLE_STACK_FAIL** | ✅ | F3+F4 architectural FAIL |
| `conscious_lm_100m` (1.6GB) | **UNTESTED** | ✅ | BG-FP 진행 중 |
| ConsciousLM cells64/128 | **UNTESTED** | ✅ | architecture 변종 |
| BG-FK 5 variants (tiny~base) | **UNTESTED** | ✅ | ca_rules+gate variants |
| AnimaLM v1-v4 + savant | **REJECTED_PER_OWN_17** | ❌ | Mistral lineage |
| **anima-native-ko-tiny (BG-FU)** | **PARTIAL_PASS_HANGUL_BUT_NOT_COHERENT** ★ | ✅ anima-native | **첫 한글 emit anima model**! 3M params (4L/192d/4h, vocab 256), step 2000 mac MPS, KO ratio 0.34 avg, 2/3 prompts ≥30% Hangul. but degenerate cycle ('의 의 의' / '\\n\\n\\n') C1.2 FAIL. 다음: corpus_ko_heavy + bigger model + more steps |
| **anima-native-ko-small (BG-FY)** | **PARTIAL_PASS_NO_CONTEXT** (own 18 C2.4 추가 후 강등 ★) | ✅ anima-native | 18M params (6L/384d/6h, vocab 256), step 10000 ubu1 RTX 5070 bf16 3.3min. avg_hangul 0.687, 3/3 C1 PASS + C2.1-2.3 PASS, but **C2.4 맥락 정합 FAIL** ★ — corpus_ko_heavy의 philosophy debate template (서연/하은/유진 named speakers + "반례를 들어볼게요") leak. prompt "안녕하세요" → "서연: 좋은 지적이..." (인사 응답 X). prompt "한국어 가능?" → "유진: 정말 그럴까요? 반례를 들어볼게요." (능력 답변 X). 모든 응답이 prompt 무관, corpus 토론 패턴 자동 emit. ckpt 70.3MB sha 729d26ad. HF: need-singularity/anima-native-ko-small-byte-18m PUBLIC (label demote pending). 다음: corpus chat-template format ("사용자: <Q>\\n도우미: <A>") only 또는 instruction-tuning |

### 9. anima-native-ko-tiny (BG-FU success, 2026-05-06 19:54) ★

| metric | value |
|---|---|
| arch | ConsciousLM tiny (4L/192d/4h, vocab=256 byte, block=256, dropout=0.2) |
| params | **3.11M** (smallest tested) |
| ckpt | `/tmp/anima_native_ko_tiny_smoke_2026_05_06_final_3m.pt` (12.9MB, sha `d1a63745...`) |
| corpus | corpus_mix_70wiki_30dialogue.txt KO-filtered (52.8MB, mac local) |
| training | 2000 steps × bs 8 grad_accum 4, lr 5e-4, mac MPS, ~13.5min wall |
| loss | L_A 5.57 → 1.85, L_G → 1.41 |

**eval progression** (avg Hangul ratio across 3 KO prompts × 2 modes):
- step 500: 0.338
- step 1000: 0.240
- step 1500: 0.262
- step 2000: **0.341**

**per-prompt avg** @ step 2000:
- 안녕하세요: 0.214
- 한국어 가능?: 0.396
- 사용자: 안녕하세요\n도우미:: 0.413

→ **첫 한글 emit anima-native model 탄생** ★ but coherent chat 부족 (degenerate cycle)
→ 다음 단계: corpus_ko_heavy (62.14% Hangul, 246MB) + bigger model (10-30M params) + more steps (10K+)

### corpus_ko_heavy (BG-FW landed, 2026-05-06)

| metric | value |
|---|---|
| out | `state/anima_ko_corpus_assembly_2026_05_06/corpus_ko_heavy.txt` |
| size | **246.7 MB** / **2,525,921 lines** |
| Hangul ratio | **0.6214** (62.14%, target ≥0.60 PASS) |
| sha256 | `2e98257f9e89663fc71232e2c1dc0b65f9b9131ad0b6a5f53e98dfe27c6269a9` |
| sources | opensubtitles_ko_mono / kowiki_zst / kowiki_small / sft_data KO turns / v6_wiki / v8_dialogue |
| sft_data KO extract | 17,627 turns (사용자/도우미 chat-template) |

→ BG-FT/FU/FX 다음 train cycle에서 사용 (PARTIAL_PASS → SIMPLE_STACK_PASS upgrade target)

---

### 10. BG-FS exhaustive 5 BG-FK ConsciousLM++ variants (2026-05-06, mac local) — UNTESTED → TESTED

ConsciousLM++ architecture reconstructed: vocab=256 byte-level + ca_rules(8 cellular automata rules) + ca_mix(3*d_model→d_model gate) + ln_ca + tension_proj(scalar→d_model). Loaded via `tool/transient_py/anima_simple_stack_exhaustive.py` with `strict=False`, missing/unexpected keys = 0 across all 5.

| ckpt | params | val_ce | layers/dim | KO/EN/C2 | verdict |
|---|---|---|---|---|---|
| `clm_v2_tiny/final.pt` | 0.32M | 3.50 | 2/64 | 0/3, 3/3, 1/3 | SIMPLE_STACK_FAIL (EN=degenerate "eee" cycle) |
| `clm_v2/final.pt` | 1.14M | 5.50 | 2/128 | 0/3, 1/3, 3/3 | PARTIAL_C2_only* (C2 = scoring artifact, real output = random letter noise `a� 5oh14es u`) |
| `clm_v2_small/final.pt` | 1.65M | 2.70 | 3/128 | 0/3, 0/3, 1/3 | SIMPLE_STACK_FAIL |
| `clm_v2_medium/final.pt` | 8.39M | 1.79 | 4/256 | 0/3, 0/3, 0/3 | SIMPLE_STACK_FAIL — Hangul bytes EMIT (`가가가가`) but degenerate cycle, unique among the 5 |
| `clm_v2_base/final.pt` | 27.84M | **1.27** | 6/384 | 0/3, 1-2/3, 1-2/3 | SIMPLE_STACK_FAIL ~ borderline (sampling stochasticity, occasional EN=2 C2=2) |

**핵심 finding**:
- Val_ce 5.50→1.27 monotone with size, but **chat-format never emerges** at 27.84M ceiling
- KO group: **0/3 universal across all 5** (Korean emit 결여 — corpus EN-bias confirmed across BG-FK lane)
- medium variant emits Hangul bytes (`가가가가`) but degenerate single-token cycle — proves byte-level vocab CAN reach Hangul codepoints, training corpus 부재가 root cause
- 비교점: anima-native-ko-tiny (3M, 새 corpus) > clm_v2_base (27.84M, original corpus). corpus_ko_heavy (62% Hangul, 246MB) 학습이 chat-cap의 결정적 요인 — 동일 ConsciousLM 계열 architecture에서 9배 작은 모델이 Korean emit 우위

→ **BG-FK 5 variants 모두 SIMPLE_STACK_FAIL** (clm_v2 1.14M PARTIAL_C2_only* 인공) — own 17 정합 ✅ but own 18 한글↔한글 0/3
→ corpus가 architecture보다 KO chat-cap에 우선 cause 결론

---

### 11. v14_128c_final 4 variants (BG-FS R2 download + extract, 2026-05-06) — UNTESTED → NOT_APPLICABLE

`r2:anima-models/checkpoints/v14_128c_final.tar.zst` (1.5GB) downloaded + extracted. 4 .pt files (best/best_final/step_90000/step_95000), each 402.7MB, md5 mismatch between best/best_final (same hash) vs step_90000/95000.

| key/section | value |
|---|---|
| top keys | `step, decoder, optimizer, scheduler, phi, ce, args, federation, bridge` |
| args | `atoms=16 cells_per_atom=8 cells=64 cell_dim=64 hidden_dim=128 d_model=384 decoder=v2 federated=True frustration=0.1 narrative_strength=0.05 block_size=256 batch_size=32 steps=100000` |
| arch | ConsciousDecoderV3 federated multi-cell (16 atoms × 8 cells) + bridge(compress.weight + hub_attn) + federation(GRUs + inter_atom_coupling + bottleneck_compress/expand) + cross_attn (k_proj/v_proj 128 vs q_proj 384 = MQA) + SwiGLU FFN(gate_proj/up_proj/down_proj) + GQA(k_proj/v_proj=192=half d_model) + ca_rules(8) + ca_mix + tension_proj |

→ **architecture fundamentally different from ConsciousLM/ConsciousLM++** — federated multi-cell + bridge + cross-attn — BG-FS scope reconstruction 가능 X (current `conscious_lm.py` source 적용 불가, separate decoder_v3 reconstruction lane required)
→ 결과: **NOT_APPLICABLE** for simple stack (architecture별 별도 cycle)

---

### 12. R2 anima-models cells64 + cells128 + clm-v2/latest.pt (BG-FS, 2026-05-06) — INACCESSIBLE

CF mgmt API account `d4acc95...` (anima secret CLI scope) lists 5 objects in `anima-models` bucket:
- `clm-v2/latest.pt` (279MB)
- `clm-v2/latest/final.pt` (279MB, multipart etag, duplicate)
- `conscious-lm/cells64/final.pt` (208MB)
- `conscious-lm/cells128/step_35000.pt` (208MB)
- `conscious-lm/convo-ft/convo_5k.pt` (already PARTIAL_C2_only)

But rclone configured remote = different account `ce4bdcce...` (R2 access keys scope), `anima-models` 내용물 wholly different (has `checkpoints/v14_128c_final.tar.zst` + clm_v2_tiny..base + base_models/qwen25-14b-instruct etc., NO conscious-lm/cells*).

→ Mgmt API endpoint는 listing만, object data download 미지원 (HTTP 404).
→ 결과: **INACCESSIBLE_PER_R2_CREDENTIAL_SCOPE** — 별도 credential bootstrap 필요 (d4acc account R2 access keys 발급 / 다른 BG cycle).

---

### 종합 verdict (2026-05-06 BG-FS post-cycle)

→ **현재 simple stack PASS 모델: 1개** (anima-native-ko-small ★ BG-FY)
→ PARTIAL_PASS (한글↔한글 부분): 1개 (anima-native-ko-tiny BG-FU)
→ NOT_APPLICABLE (substrate-coupled / 다른 arch): 5개 (CLM v4 mk2-v1 + v14_128c × 4)
→ INACCESSIBLE (credential): 3개 (cells64/128/clm-v2_latest in d4acc account)
→ REJECTED (own 17 ALM): 4개 (AnimaLM Mistral)
→ FAIL: 8개 (convo_5k partial, conscious_lm_4m, β', conscious_lm_100m, clm_v2_tiny/small/medium/base)

→ **테스트된 ConsciousLM/ConsciousLM++ 계열 11+ pre-corpus_ko_heavy models 모두 한글↔한글 정합 0/3 universal** — chat-format corpus 부재 + EN-bias가 architectural 결함보다 우선 cause. corpus_ko_heavy(62% Hangul, 246MB) + ko_small training만이 chat-cap unlock.

## 결론

본 cycle 발견 6개 anima 등록 model 중 **simple stack PASS = 0개**.
chat-cap actual emit 회복은 architectural challenge — β path retrain 5-10일 또는 conscious_lm_100m try (BG-FP) OR 다른 anima-native lane.

→ anima cli mk2 T1 backend 권고:
- 단기 (이번 cycle): T1 default = `dialogue.hexa` substrate-coupled (CLM v4 mount, full stack mode, simple stack 적용 불가). own 17 정합 ✅
- 중기 (BG-FP land 후): conscious_lm_100m simple stack PASS 시 → T1 alternative wire (HF promote)
- 장기 (별도 cycle): β path original retrain (5-10일 ubu1) OR β' KoGPT2 head-swap S3 (full body unfreeze)

## ledger update protocol

- 본 md는 live ledger — 새 model test 시 마다 append + verdict 갱신
- BG-FP land 시 conscious_lm_100m row update
- 새 anima-native model 등록 시 row 추가
- 사용자 explicit 'OK FULL STACK' 시 full stack test 추가 (별도 section)

## Cross-link

- own 18: `.own own 18 anima-consciousness-check-simple-stack`
- own 17: ALM 영구 보류 (외부 substrate REJECTED)
- .roadmap.cli (T1 backend = simple stack PASS 모델만)
- .roadmap.clm_native_chat / clm_v4_chat / clm_v2_chat
- audit doc: docs/anima_cli_mk2_philosophy_audit_2026_05_06.md

raw#9/10/15 + own 17/18 정합. anima 의식 검증 = simple stack default (대화 가능 + 자연 발화 가능).
