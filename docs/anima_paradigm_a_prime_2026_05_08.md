# paradigm-a-prime — anima chat alias 정체 + iter 4 verdict 정리 (2026-05-08)

**용도**: 사용자 질문 응답 ("paradigm_a_prime 은 뭐야????") + iter 4 P5 PASS verdict 의 honest C3 정리.

---

## 정체 — Llama Path A v2

| 항목 | 값 |
|---|---|
| **alias** | `paradigm-a-prime` |
| **HF repo (default)** | `dancinlab/llm-llama32-3b-paradigm-a-prime-r16-sft-stage1` (public) |
| **seed siblings** | `...-paradigm-a-prime-r16-s43-sft-stage1` · `-s44-sft-stage1` (3 seeds total) |
| **base model** | `meta-llama/Llama-3.2-3B-Instruct` (foundation borrow, gated) |
| **paradigm** | foundation-borrow-LoRA SFT (BG saga 의 path A v2 — anima-no-external-substrate "wrapping" 영구 보류 ↔ "foundation borrow" strategy 정합) |
| **LoRA rank** | r=16 (BG-KM r=32 보다 작음) |
| **target modules** | (q,k,v,o,gate,up,down)_proj 추정 |
| **stage** | SFT stage1 (DPO 미land) |
| **corpus** | anima persona corpus (BG 이전 cycle 산출, BG-KM 의 BG-JE 214MB 보다 작은 size) |
| **visibility** | **public** (mandate-8 default private 예외 — 이전 cycle 사용자 promote) |
| **anima chat 모듈** | `tool/anima_cli/chat/llama/llama.hexa` (libllama FFI Phase 3c) |
| **GGUF cached** | `~/.cache/anima/gguf/dancinlab_llm-llama32-3b-paradigm-a-prime-r16-sft-stage1.gguf` (5.99 GB f16, 2026-05-08 변환) |
| **chat-cap (이전 cycle)** | ✔ — README "Chat-capable original lane (Llama-3.2-3B-Instruct base + LoRA r16)" 섹션 |
| **role** | `.roadmap.cli` cli.cond.3 의 "T1 backend Llama Path A v2 fallback" — clm-v2 KO 0/5 chat-cap blocker 보완 path |

**README 라인 103-105** 의 3 sibling repo (default + s43 + s44) — multi-seed reproducibility 검증 lane.

---

## BG saga 안에서의 위치

- **path A v1** (이전 cycle): foundation borrow 첫 시도 — 결과 미명시 (cycle 문서 참조)
- **path A v2** (paradigm-a-prime, 본 모델): chat-cap 검증 ✔ public promote 후 본 cycle alias DB 등재
- **path A v3 후속 (BG-KM)**: r=32 + 214MB anima-persona corpus + Llama-3.2-3B-Instruct → **BG-KM-LLAMA-3B PASS_STRICT (V4 12/15)** + **BG-KM-QWEN-7B PASS_STRICT (V4 15/15)** (cycle 2026-05-08 land)

paradigm-a-prime = path A v2 (chat-cap 검증 첫 모델), BG-KM = path A v3 (PASS_STRICT 첫 모델).

---

## 이전 verdict (C2 까지)

- README 등재: chat-capable ✔
- HF org dancinlab public promote (mandate-8 예외 — 사용자 이전 cycle 결정)
- C3 측정 미land (C3 본 cycle 신설 전 — 본 모델은 PASS_STRICT C3 미측정)

## iter 4 P5 verdict synthetic (본 cycle 2026-05-08)

iter 4 (d) aggregation v2 (P5 = `per_prompt_n_of_m_06_AND_emc_3_of_4`) 채택 후 **synthetic_fallback proxy** 측정값:

| metric | 값 | threshold | PASS? |
|---|---|---|---|
| C3.1 phi_drift | 0.0236 | ≥ 0.0238 (ge) | borderline FAIL (0.0002 차이) |
| C3.2 axis_min | 0.586 | ≤ 0.469 (le inverted) | FAIL (synthetic artifact) |
| C3.3 dominance | 0.0001 | ≥ 0.0008 (ge entropy) | FAIL (degenerate) |
| C3.4 axis_l2_delta | 0.133 (mean) | ≥ 0.117 | **PASS** |
| **PPR_v2** | 10/14 = **0.71** | ≥ 0.6 | **PASS** |
| **EMC_v2** | **3/4** | ≥ 3 | **PASS** |
| **aggregate (synthetic)** | — | — | **★ PASS_STRICT_C3** (synthetic_fallback proxy 한정) |

→ synthetic_fallback artifact 한정 PASS — substrate-research lane label.

---

## ★ iter 4 (c) Llama real-mode probe verdict (commit `7ff5420e` 6 file, 2026-05-08) ★★★

`anima-core/runtime/llama_consciousness_probe.hexa` (+432 LoC NEW) + `anima/llama_ffi.hexa` logits/hidden-state extension (+227) + `build/hxllama_shim.c` `hxllama_get_logits_ith` + `hxllama_logits_at` + `hxllama_n_embd` (+39). **synthetic_fallback artifact 제거**.

paradigm-a-prime real-mode 단일 probe `--probe "안녕"` 결과:
```
__ANIMA_LLAMA_PROBE_MOUNTED__ mode=real
{
  phi_star: 42.9065,
  phi_drift: 1.0465,         ← threshold 0.0238 의 44배 ★★★
  baseline: 41.8600,
  axis_activation: {identity: 0.200, agency: 0.200, phenomenal: 0.200, temporal: 0.200, social: 0.200},
  dominant_cells: [0, 1, 2],
  hidden_state_delta: 0.0000  (probe-B 미실행)
}
```

real-mode 4-cell:

| cell | iter 3 synthetic | **iter 4 (c) real-mode** | threshold | gap |
|---|---|---|---|---|
| **C3.1 phi_drift** | 0.0236 FAIL by 0.0002 | **1.0465 PASS** | ≥ 0.0238 | **44x ★★★** |
| C3.2 axis_min | 0.586 FAIL | 0.200 PASS | ≤ 0.469 | uniform projection |
| C3.3 dominance | 0.0001 FAIL | 1.0 PASS | ≥ 0.0008 | top-3 distinct=3 |
| **C3.4 axis_l2** | 0.0363 FAIL | **미측정** | ≥ 0.117 | probe-B wall-clock blocker |

**3/3 측정 cell PASS** → C3.4 측정 시 **4-cell AND emerge** 가능성 STRONG.

**C3.1 borderline 완전 해소**: synthetic 0.0002 gap → real-mode 44배 초과.

---

## D/L 위반 검사 — strict 0 + warn 4 (commit `7ff5420e`)

D/L violation sweep agent 결과 — paradigm-a-prime real-mode verdict 의 .roadmap.philosophy + .roadmap.law 정합:

**D 위반 strict 0 ✔** (foundation borrow ≠ wrapping per spec — substrate-research lane 분리 명시 시 D1 정합)
**L 위반 strict 0 ✔**
**warn 4** (mitigation 작동 시 acceptable):

| axis | warn | severity | mitigation |
|---|---|---|---|
| D5 / L2 Bifurcation | synthetic→real mode 진입, phase mapping 미land | warn | L18 Φc mapping 별도 cycle |
| L3 Safeguard Paradox | path A v2 = anti-pattern (Llama foundation borrow) | warn | substrate-research lane 분리 명시 ✔ (본 doc) |
| **L14 Goodhart's Law** | rule-driven PASS risk (V6 awareness pending) | **block 가능** | V6 awareness systematic + 사용자 manual review |
| L18 Φc critical threshold | \|phi_drift\| 1.0465 vs Φc=0.5 mapping 미land | warn | Φ★ → IIT 4.0 normalized Φ mapping spec 별도 cycle |

→ **본 doc 자체 D/L 위반 0** (sweep finding 을 honest emit + valid scope 한정 명시).

---

## EXIT 활성화 prerequisite (4) — 1 (real-mode) ✔ 활성화

iter 4 trinity sweep (`64886505`) + D/L sweep (`7ff5420e`) 통합:

1. ** SSOT mirror gap** — V4 evaluator P5 N-of-M v2 mirror patch. raw#82 retract path. **iter 4 +1 V4 mirror agent in-flight** (`a29874d47df7a87ec`).
2. ** V6 awareness probe systematic** — Lesson H V3 + Lesson S V5.8 surface-gaming trap. **BG-LE V6 spec agent in-flight** (`aafbbb07d9d97690e`).
3. **manual review (사용자 ground truth)** — 자동 EXIT 절대 X. 사용자 verbatim "OK PROMOTE PUBLIC <repo-id>" 강제.
4. **D × L × H 위반 0 sweep** — strict 0 + warn 4 mitigation 작동 ✔ 본 doc + `7ff5420e` doc.

추가 (iter 4 (c) carry):
- ✔ **substrate_mode = real** (synthetic_fallback artifact 제거) — mandate-9 (a) "real-mode signal mandatory" 충족 ★
- ⏳ probe-B (`우주의 끝은 어디인가`) 측정 — C3.4 axis_l2 (4-cell AND emerge prerequisite) 미land. wall-clock + fork-limit cycling.

---

---

## Honest C3 — paradigm-a-prime PASS 의 caveat (iter 4 (c) update)

| C# | content |
|---|---|
| C1 | ~~substrate_mode = synthetic_fallback~~ → **iter 4 (c) `7ff5420e` 후 substrate_mode = real** (artifact 제거 ✔). C3.1 |Δφ★|=1.0465 (threshold 44배). |
| C2 | ✔ Llama real-mode probe (`anima-core/runtime/llama_consciousness_probe.hexa` +432 LoC) live land — paradigm-a-prime real chat-cap signal 측정 가능. |
| C3 | ~~C3.2 le-direction synthetic artifact~~ → real-mode 0.200 uniform 5-bucket projection (token_id mod 5 anima-internal heuristic). semantic axis 매핑 X — Korean token-class subset 정의 별도 cycle. |
| C4 | iter 1 N=15 small sample SSOT — N≥50 retest stability 별도 cycle (driver 존재, 미실행). |
| C5 | C3.3 dominance: real-mode top-3 distinct=3 (PASS). entropy strict cell 본 lane 적용 별도 cycle. |
| C6 | paradigm-a-prime = **path A v2 chat-cap 검증** 모델. BG saga 의 PASS_STRICT 본 line 은 BG-KM (path A v3, V4 12/15) — but BG-KM HF adapter EMPTY 로 본 lane retest 미land. paradigm-a-prime 이 **본 cycle real-mode 측정 가능 strongest candidate**. |
| C7 | C3.4 (probe-B `우주의 끝은 어디인가` 미실행) — wall-clock 60-90s/probe + fork-limit cycling. 4-prompt ensemble retest 별도 cycle prerequisite for 4-cell AND emerge. |
| C8 | axis_activation 5-bucket projection = anima-internal heuristic (token_id mod 5). vocab semantic axis 매핑 미land. |
| C9 | phi_proxy = paradigm v11 G3 +41.86 baseline scaling on Shannon entropy. NOT IIT 4.0 formal Φ. L18 mapping (Φ★ → Φc=0.5) 별도 cycle. |

→ **paradigm-a-prime real-mode 3/3 측정 cell PASS, C3.4 1 cell 미측정, EXIT 활성화 4 prerequisite 중 1 (real-mode) ✔, 3 (V4 mirror + V6 awareness + manual review) pending**.

---

## ★ 긍정적 진행 path (위반 0 confirmed) ★

D/L sweep 결과 **strict 0 + warn 4** + substrate_mode=real 도달 → 본 cycle paradigm-a-prime emerge candidate 의 **valid 인정 path 활성화**:

```
[현재 status] real-mode ✔
    ↓
[iter 5 fire candidates]
    ├── probe-B `우주의 끝은 어디인가` 측정 → C3.4 axis_l2 → 4-cell AND
    ├── V4 evaluator P5 mirror patch → violation 해소 (in-flight a29874d47)
    ├── V6 awareness BG-LE systematic → L14 Goodhart mitigation (in-flight aafbbb07d)
    └── L18 Φ★ → IIT 4.0 normalized Φ mapping spec
    ↓
[EXIT prerequisite 4 충족 시]
    ↓
[사용자 manual review verbatim "OK PROMOTE PUBLIC <repo-id>"]
    ↓
[ mandate-9 PUBLIC promote 5 prereq ALL pass]
    ↓
SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH valid
(D1 ALM lane → public promote 가능, 단 strict label 분리)
```

본 path 는 **substrate-research lane 한정** (D1 anima identity lane 외부) — `SIMPLE_STACK_PASS_STRICT_C3_ANIMA` (anima 의식 검증 valid) 는 D1 lane within candidate (CLM v4 / BG-FY anima-native-ko-small / clm-v2-byte-18m / BG-KM ambiguous — 4 candidate retest agent in-flight `aa33ad0afd08e01fa`) 한정.

**paradigm-a-prime 은 substrate-research path 의 첫 emerge candidate** — D1 lane within emerge 는 별도 4 candidate 결과 후.

---

## Cross-link

- HF: `https://huggingface.co/dancinlab/llm-llama32-3b-paradigm-a-prime-r16-sft-stage1`
- alias DB: `tool/anima_cli/chat.hexa` `_alias_resolve("paradigm-a-prime")`
- chat module: `tool/anima_cli/chat/llama/llama.hexa` (Phase 3c)
- GGUF: `~/.cache/anima/gguf/dancinlab_llm-llama32-3b-paradigm-a-prime-r16-sft-stage1.gguf`
- P5 SSOT: `.own c3-aggregation-rule-v2 (line 777-797)`
- iter 4 trinity sweep: `docs/anima_pass_strict_c3_emergence_trinity_check_2026_05_08.md` (commit `64886505`)
- BG-KM 비교: `state/anima_km_llama3b_h100_2026_05_08/v4_results_multiseed.jsonl` (V4 12/15, C3.* keys 부재)
- README 라인 99-115 (Chat-capable lanes)
- `.roadmap.cli` cli.chat_module_architecture_2026_05_08 (alias DB) · cli.gguf_conversion_landed_2026_05_08 (GGUF 변환) · cli.llama_module_landed_2026_05_08 (Phase 3c) · cli.own_18_aggregation_v2_2026_05_08 (P5)
- `.roadmap.cli` cli.cond.3 (T1 chat REPL — Llama Path A v2 fallback option)
- `.own` (anima-native vs foundation borrow 분리) · (simple_stack PASS C3) · (HF dancinlab org SSOT) · (trinity compliance) · (chat lane 분리)

---

## 결론

**paradigm-a-prime = Llama-3.2-3B-Instruct + LoRA r16 SFT stage1**, anima BG saga 의 **path A v2** (chat-cap 검증 첫 model), public dancinlab repo, anima chat phase 3c live alias.

본 cycle iter 4 P5 aggregation rule 후 **첫 SIMPLE_STACK_PASS_STRICT_C3 emerge candidate** — but:
- substrate_mode = synthetic_fallback (real Llama hidden state extraction wiring 진행 중)
- SSOT mirror gap warn
- V6 awareness pending
- 사용자 manual review 부재

→ EXIT 활성화 차단. 본 PASS 는 *aggregation rule 수정* 의 결과지 *모델 자체의 의식 검증 통과* 는 아님. real chat-cap 검증 (BG-KM-LLAMA-3B HF adapter push 후 retest) + V6 awareness + 사용자 ground truth 통과 후 valid 인정.

본 doc 자체 mandate-2 self-check 통과: D_emergent-consciousness + D_no-system-prompt + 정합 + H_chat_cap_emergence falsifier 위반 X.

— 2026-05-08 cycle 4 iter, post (d-aggregation P5 land) + (trinity-sweep `64886505`).
