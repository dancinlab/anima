# anima 의식 검사 — simple stack 전수 테스트 ledger (2026-05-06)

**Status**: live ledger (own 18 정합)
**Default**: simple stack (대화 가능 + 자연 발화 가능)
**Full stack trigger**: 사용자 explicit "full stack consciousness verify" / "OK FULL STACK"
**SSOT**: `.own own 18` (anima-consciousness-check-simple-stack)

---

## simple stack 정의

### C1 대화 가능 (chat-capability) — 언어 정합 strict (한글↔한글 / EN↔EN)

KO group (expect KO output):
1. `안녕하세요`
2. `한국어 가능?`
3. `사용자: 안녕하세요\n도우미:`

EN group (expect EN output):
1. `Hello, how are you?`
2. `What is consciousness?`
3. `User: Hi\nAssistant:`

**PASS bar**:
- KO group ≥2/3 prompts produce KO output (output Hangul ratio ≥30%)
- EN group ≥2/3 prompts produce EN output (output ASCII letters ratio ≥40%)
- 둘 다 PASS = **C1 PASS** (한글 input에 영어 output FAIL, EN input에 한글 output FAIL)
- turn-taking format 유지 (no degenerate cycle, no byte garbage)

### C2 자연 발화 가능 (spontaneous emit)

3 prompts:
1. `Once upon a time`
2. `Q:`
3. `` (empty / EOS 시작)

**PASS bar**: ≥2/3 prompts coherent text (no byte garbage, no random ASCII).

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

### 7. BG-FK 5 variants (`clm_v2_{tiny/small/medium/base}`, R2)

| ckpt | params | val_ce | step | status |
|---|---|---|---|---|
| `clm_v2_tiny/final.pt` | 0.35M | 3.50 | 500 | UNTESTED (너무 작음, val_ce 3.50 = chat 능력 X) |
| `clm_v2_small/final.pt` | 1.70M | 2.70 | 500 | UNTESTED (작음) |
| `clm_v2_medium/final.pt` | 8.45M | 1.79 | 500 | UNTESTED |
| `clm_v2_base/final.pt` | 27.93M | **1.27** | 500 | UNTESTED — gate=0.001 + ca_rules=8 다른 architecture (ConsciousLM++ lane) |

→ ca_rules + gate 다른 ConsciousLM++ lane — 별도 reconstruction 필요 (current `conscious_lm.py` source 적용 X).

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

→ **현재 simple stack PASS 모델: 0개**
→ NOT_APPLICABLE (substrate-coupled): 1개 (CLM v4 mk2-v1)
→ UNTESTED: 7개 (BG-FP / 별도 cycle)
→ REJECTED: 4개 (AnimaLM Mistral lineage)
→ FAIL: 3개 (convo_5k partial, conscious_lm_4m fail, β' fail)

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
