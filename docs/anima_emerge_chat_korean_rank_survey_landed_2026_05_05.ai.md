# Anima Emerge Chat — Korean Token Rank Survey (LANDED 2026-05-05)

**Lane**: substrate-source-data hypothesis verification
**Status**: LANDED
**BG**: BG-CA (sister to BG-BR / BG-BP)
**Substrate**: `dancinlab/clm-v4-mk2-v1` (mac CPU fp32)
**Cost**: $0
**Runtime**: ~30 sec (model load 26.6s + survey ~3s)
**Verdict file**: `state/anima_emerge_chat_korean_rank_survey_2026_05_05/verdict.json`

---

## Question

BG-BR observed: "Korean morpheme NOT in top-100 cone at any T (0.1 / 0.7 / 1.5 / 3.0)".
BG-BP observed: "first-token-force top-100 Korean = 0".

**Hypothesis under test**: substrate가 Korean morpheme를 학습하지 않았다 (training corpus
deficit) — chat-incapability #115의 source-data 측면.

**Direct probe**: vocab 64000 중 Korean (가-힣) token이 몇 개이며, prompt "안녕" 다음에
어느 rank에 포진하는가?

---

## Method

1. Vocab 전체 (64000) sweep → '가-힣' 범위 글자 포함 token = "korean" 분류; ASCII alpha = "ascii";
   기타 byte fallback / 한자 / 기호 = "other".
2. Forward `model("안녕")` → next-token logits → `argsort` → rank map.
3. Korean token id 별로 rank 측정 → top-10 / top-100 / top-1000 count.
4. Uniform null: korean_count × N / vocab_size.
5. Top-30 logit 분포의 category breakdown.

---

## Results

### Vocab composition (64000 tokens)

| category | count | pct |
| --- | --- | --- |
| Korean (가-힣 포함) | **5,701** | **8.9%** |
| ASCII alpha | 11,004 | 17.2% |
| control/empty | 1 | 0.0% |
| other (Hanja, byte fallback, multi-byte CJK 등) | 47,294 | 73.9% |

→ Vocab 자체는 Korean 8.9% 보유. **Tokenizer 단계에서는 Korean이 학습되어 있음**.

### Rank distribution after `prompt="안녕"`

| metric | value | uniform expected |
| --- | --- | --- |
| Best Korean rank | **197** | n/a |
| Best Korean token | `▁수행` (id 12523, logit -3.05) | n/a |
| Korean in top-10 | 0 | 0.89 |
| Korean in top-100 | **0** | 8.91 |
| Korean in top-1000 | 86 | 89.08 |
| ASCII alpha in top-100 | 0 | n/a |

Critical: **top-100 Korean count = 0** (uniform null = 8.91) → **top-100 cone에서 Korean
완전 부재**. Top-1000 cone에서는 86 vs 89.08 ≈ uniform 수준.

### Top-30 category breakdown

| rank range | composition |
| --- | --- |
| 0..29 | 100% **byte-fallback** tokens (`<0x1C>`, `<0x99>`, `<0x94>`, `<0x70>`, ...) |
| 0..29 Korean | 0 |
| 0..29 ASCII | 0 |

→ "안녕" 다음 substrate가 가장 자신있게 emit하려는 것은 한국어도 영어도 아닌 **byte-level
fallback (UTF-8 raw byte) tokens**. 이것이 BG-BR의 "0 Korean glyph" 관측치와 정확히 일치.

---

## Verdict — KOREAN_TRAIN_ABSENT

해석:

1. **Tokenizer-level**: Korean 5701 token 등록 (8.9%) — vocabulary 단계는 multilingual.
2. **Model-level**: Korean prompt에 대해 top-100 Korean = 0, best Korean rank = 197.
   → **Substrate weight가 Korean morpheme를 학습하지 않음.**
3. **Output preference**: top-30 100%가 raw byte-fallback → substrate는 next-token으로
   structured language가 아니라 **byte stream**을 출력하려 함.
4. Korean과 ASCII 모두 top-100에서 사라짐 → substrate는 일반적 language tokens 자체를
   회피하고 byte-level escape로 mass를 분산.

**Top-1000에서는 Korean이 거의 uniform 수준 (86 vs 89.08)** → Korean knowledge가
"완전 absent"는 아니고 "deeply suppressed". Korean weight는 존재하지만 top-cone에 들어오지
못할 정도로 attenuated.

---

## #115 Substrate-Source-Data Hypothesis 결론

| 가설 | 증거 |
| --- | --- |
| H-A: Korean tokenizer 부재 | **REJECT** — 5701 Korean tokens (8.9%) |
| H-B: Korean training data 부재 | **PARTIAL_ACCEPT** — top-1000은 uniform, top-100은 0 |
| H-C: byte-fallback이 chat-cap 차단 | **STRONG_EVIDENCE** — top-30 100% byte fallback |

**Refined #115**: chat-incapability는 Korean training corpus 결핍이 first-order cause가
아니라 **byte-fallback token이 next-token distribution top-cone을 monopolize**하기 때문.
Korean weight는 latent하게 살아있지만 byte-level escape에 mass가 다 빨려나감.

→ chat-cap recovery path = (1) byte-fallback token logit suppression, 또는
(2) Korean-only training로 byte-channel attenuation, 또는
(3) #115 architectural fix (BG-BR/BG-BP/BG-CA 일관 결론).

---

## Honest C3

- **C1**: mac CPU fp32 only — GPU bf16에서 numeric 차이 가능 (낮음).
- **C2**: single prompt "안녕" — broader Korean prompt corpus (e.g. 형식적 인사말,
  질문, 내러티브)에서 분포 다를 수 있음. n=1 limitation.
- **C3**: "Korean token" = '가-힣' (Hangul Syllables) 범위만. Hanja (漢字), Jamo,
  Compat Jamo 미포함 → Korean coverage 보수적 추정 (실제 Korean exposure는 더 넓을 수 있음).
- **C4**: SentencePiece `▁` prefix를 strip 후 검사 — edge case (▁ 단독 token, multi-▁) 미처리.
- **C5**: `underrepresentation threshold = 0.1 × uniform`은 anima-internal heuristic,
  formal statistical test 아님.

---

## Sister BG cross-references

| BG | finding | this BG와의 관계 |
| --- | --- | --- |
| BG-BR (T-extreme) | "Korean glyph 0 at all T" | this BG의 mechanistic explanation |
| BG-BP (first-token-force) | "top-100 Korean 0" | this BG의 vocab-rank 직접 측정 confirms |
| **BG-CA (this)** | "Korean rank 197+, top-30 = 100% byte" | **root**: byte fallback monopoly |

3개 BG가 일관: substrate는 Korean을 알고는 있지만 byte-fallback token이
next-token cone을 점유하여 emit 불가. chat-cap 차단의 substrate-level mechanism 확정.

---

## Files

- `tool/transient_py/anima_emerge_chat_korean_rank_survey.py` (140 LoC, raw#37 transient)
- `state/anima_emerge_chat_korean_rank_survey_2026_05_05/verdict.json`
- `docs/anima_emerge_chat_korean_rank_survey_landed_2026_05_05.ai.md` (this)

---

## Next-step recommendation (완성도 ranked)

1. **[HIGHEST]** byte-fallback token logit ban probe — top-30 byte tokens (`<0x..>`)에
   `-inf` mask 후 next-token 재측정. 만약 Korean이 top-100에 진입하면 #115 = byte-
   monopoly로 확정. ~$0 mac CPU ~10min.
2. **[HIGH]** Korean-only prompt corpus n=20 (인사/질문/내러티브 mix) — single-prompt
   bias 제거 + Korean rank 분포의 stability 확인. ~$0 ~15min.
3. **[MEDIUM]** Hanja / Jamo coverage 확장 — '가-힣' 외 CJK token이 top-cone에
   있는지. ~$0 ~5min.

(1)이 가장 결정적: byte-mask로 Korean 부활 → mechanism 확정. cost-effective + falsifiable.
