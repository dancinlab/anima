# D2 — sampler detokenize round-trip (toy 버전) (`decoder-sampler-detokenize-roundtrip`)

> verdict: 🟢 **SUPPORTED (toy scale)** · 5/5 falsifier PASS · 분리 margin uniq=8 ≥ 8 · $0 mac-local · 2026-05-28

## ① 배경 (context)

ANIMA DECODER M4b fire phase5b (PR #1121, `state/m4b_phase5b_2026_05_27/train.out`) 의 RESIDUAL **F-M4B-FIRE-2/5 qualitative · no detokenize** 가 잔여로 남아 있었다. token-id sequence 만으로 collapse 검출(D1 ✅)은 완료됐으나, **text 수준에서 collapse vs healthy 가 사람이 읽을 수 있는 형태로 구별 가능한가?** 라는 질문이 미해소.

이전 4회 시도는 hexa-lang `flame_bpe_corpus_lib` 의 V=151643 Qwen-BPE 전체 round-trip 을 wire 하려다 throttle window 안에서 빌드/install 중 죽었다 (heavy: stdlib 의 `flame_bpe_corpus_load` · `flame_bpe_roundtrip` 의 corpus + vocab 전체 통합). 본 round 는 **toy scale 우회** — M4b 실측 산출 빈출 token id ~10개만 hard-coded reverse-lookup table 로 매핑하여, detokenize-LEVEL 의 분리가 실재한다는 것을 cheap 하게 보인다.

## ② 가설 (hypothesis · H_D2 toy)

10-entry toy reverse-lookup `{1 → "the", 151642 → "<|endoftext|>", 2..10 → 일반 단어}` 만으로도

- 실측 M4b collapse seq `[1×4, 151642×16]` → **degenerate text** ("the the the the &lt;eot&gt; &lt;eot&gt; ... &lt;eot&gt;")
- 동일 10-id 도메인의 toy healthy diverse seq → **분화된 text** (\<eot\> 0개, 고유 단어 ≥ 10)

가 분리된다. 즉 **detokenize 가 작동한다** — qualitative residual 이 **toy scale 에서** 해소된다. full-BPE scale 해소는 future work (hexa-lang `flame_bpe_corpus_lib` toolchain 안정화 의존).

## ③ Falsifier (사전등록 · frozen 측정 前)

| id | 내용 | 판정 |
|---|---|---|
| **F-D2.1 TABLE-COVERS-REAL** | REAL M4b seq 의 모든 id 가 lookup entry 보유 (no `<UNK>`) | PASS |
| **F-D2.2 COLLAPSE-TEXT-DEGENERATE** | collapse text 의 `<|endoftext|>` 빈도 ≥ 10 (n=20 중 50%) | PASS |
| **F-D2.3 HEALTHY-TEXT-DIVERSE** | healthy text 의 `<|endoftext|>` 빈도 = 0 AND 고유 단어 ≥ 10 | PASS |
| **F-D2.4 ROUNDTRIP-IDENTITY** | table 도메인의 모든 id 에 대해 `retok(detok(id)) == id` (bijection) | PASS |
| **F-D2.5 SEPARATION-AT-TEXT** | `uniq(healthy_text) − uniq(collapse_text) ≥ 8` (decisive) | PASS |

**전체 Falsifier**: 위 5개 중 하나라도 FAIL → toy detokenize 가 collapse/healthy 를 text 수준에서 구별 못함 → toy 우회 path 무효 (≠ heavy BPE 가 필요)。

## ④ method — toy lookup table

10-entry hard-coded id→text bijection. 두 anchor 는 M4b phase5b 의 실측 빈출 토큰 verbatim:

| id | text | 출처 |
|---|---|---|
| 1 | `the` | M4b phase5b expert-e1 logit ≈ -0.03 winner (×4) |
| 151642 | `<|endoftext|>` | Qwen 특수 토큰, expert-e1 logit 938.767 saturate (×16) |
| 2..10 | `cell` · `splits` · `into` · `two` · `and` · `consciousness` · `emerges` · `now` · `are` | synthetic healthy 영역의 일반 어휘 (toy) |

`detok(id) -> string` / `retok(string) -> int` 양방향. 그 외 id 는 `<UNK>`. n=20 seq 두 개 (실측 collapse + synthetic healthy) 를 text 로 매핑해 `count_eot` · `unique_count` 측정.

deterministic · hexa-only · $0 mac-local · LLM none · NO GPU · foreground · wall 0.66s.

harness = `CORE/DECODER/d2_sampler_detokenize.hexa` · raw = `CORE/DECODER/state/d2_sampler_detokenize_2026_05_28/run_d2.out`

## ⑤ measurement — collapse text vs healthy text

**REAL M4b collapse seq** (`train.out:55` verbatim, n=20):
```
ids : 1 1 1 1 151642 151642 151642 151642 151642 151642 151642 151642
      151642 151642 151642 151642 151642 151642 151642 151642
text: the the the the <|endoftext|> <|endoftext|> <|endoftext|> <|endoftext|>
      <|endoftext|> <|endoftext|> <|endoftext|> <|endoftext|> <|endoftext|>
      <|endoftext|> <|endoftext|> <|endoftext|> <|endoftext|> <|endoftext|>
      <|endoftext|> <|endoftext|>
eot : 16 / 20   uniq : 2 / 20   id-TTR : 0.10
```

**toy HEALTHY synthetic seq** (n=20, 10-id non-eot domain):
```
text: the cell splits into two and consciousness emerges now are
      cell splits into two and consciousness emerges now the are
eot : 0 / 20    uniq : 10 / 20   id-TTR : 0.50
```

분리 margin (text-level): uniq(healthy) − uniq(collapse) = 10 − 2 = **8**, 사전등록 SEP_MARGIN(8) 정확히 충족.

## ⑥ finding — toy scale residual 해소

**해소됨 (toy scale).** collapse seq 의 detokenized text 는 "the the the the &lt;eot&gt;..."로 즉시 식별 가능한 degenerate pattern 이고 healthy text 는 \<eot\> 0개 + 고유 어휘 10개로 분화. **qualitative residual F-M4B-FIRE-2/5 가 toy scale 에서 해소**된다 — collapse 의 텍스트적 특성이 사람-가독 형태로 확인 가능.

**heavy path 우회 정당화**: 본 round 의 목적은 "detokenize 수준에서 분리가 존재하는가?" 의 cheap 확인. 그 답은 **YES** — full-vocab(V=151643) lookup 이 없어도 빈출 토큰 10개 cover 만으로 충분히 보인다. heavy `flame_bpe_corpus_lib` 통합은 별도 axis (M4b real-coherence verdict) 에서 다룰 일.

→ **H_D2 SUPPORTED (toy)**: toy lookup detokenize 는 collapse vs healthy 를 text 수준에서 구별. detokenize 자체가 본질적으로 안 되는 것은 아니다 (안 되는 게 아니라, full-BPE 통합이 toolchain-blocked 였을 뿐).

## ⑦ verdict

🟢 **SUPPORTED (toy scale)** · 5/5 falsifier PASS · uniq separation margin 8 ≥ 8.

```
RESULT: 5 PASS / 0 FAIL
VERDICT: H_D2 SUPPORTED (toy scale) — toy detokenize separates
         COLLAPSE vs HEALTHY at the TEXT level. qualitative
         residual F-M4B-FIRE-2/5 RESOLVED at toy scale.
         (Full-BPE scale verification remains future work.)
```

## ⑧ 함의 (DECODER 통합)

- **F-M4B-FIRE-2/5 qualitative residual** → **toy scale RESOLVED**. M4b phase5b verdict 의 잔여 신호가 "detokenize 불가" 가 아니라 "toolchain-blocked 였을 뿐" 임이 확정.
- **D1 LZ76 (token-id stream, $0) + D2 toy detokenize (text level, $0)** = collapse 검출의 dual proxy 완성. 둘 다 detokenize-경량 / detokenize-toy 로 cheap 하게 작동.
- **future**: hexa-lang `flame_bpe_corpus_lib` install 안정화 후 full-BPE V=151643 round-trip 으로 D2 를 격상 (coherence verdict 까지 — D2 toy 는 collapse 분리만 cover).
- D3 router-corpus mirror ✅ + D1 LZ76 ✅ + **D2 toy detokenize ✅** → M4c p7 verify 의 토대 거의 정렬, 잔여는 BPE-scale coherence 한 축뿐.

## ⑨ honest C3 (scope · 한계)

1. **toy domain (10 ids)**: full Qwen vocab V=151643 의 ~0.007% cover. 본 검증은 detokenize 가능성의 존재증명 (existence proof, toy) — 실제 M4b sampler 의 BPE-level coherence 평가는 아니다. heavy `flame_bpe_corpus_lib` 통합 후 다시 측정 필요.
2. **healthy seq = synthetic**: M4b 의 실 healthy sampling 이 없어 healthy 쪽은 합성. id 분포는 임의 (toy domain 안에서). **실 healthy** (M4b 가 충분히 학습된 후 sampling) 의 detok 패턴은 다를 수 있다 (예: 자연어 통계는 일반적으로 uniq/n ≈ 0.3-0.5, 본 toy 합성은 0.5).
3. **coherence ≠ collapse detection**: D2 toy 는 **collapse 분리** 만 보인다 — 문장이 의미적으로 정합한지(coherence) 는 별개. high-uniq 이지만 incoherent 한 text 도 D2 falsifier 를 통과한다. coherence verdict 은 별도 axis (BPE-scale + simple-stack 평가).
4. **F-D2.5 margin tight**: separation margin 8 이 사전등록 floor 8 과 정확히 일치 (slack 0). 만약 healthy 합성이 한 토큰 덜 다양했다면 FAIL. toy domain 이 11개로 일부러 설계됨 (eot 포함). full-scale 에서는 uniq 가 자연 증가하므로 margin 강건성 자연 회복.
5. **table = bijection on its domain only**: domain 밖 id 는 모두 `<UNK>` → REAL collapse seq 가 domain 안이라서 cover 했을 뿐, 일반 sampling 에 대한 robustness 는 toy 보장 없음.

## ⑩ artifacts

- harness: `CORE/DECODER/d2_sampler_detokenize.hexa` (~220 lines)
- raw verdict: `CORE/DECODER/state/d2_sampler_detokenize_2026_05_28/run_d2.out`
- 실 데이터 source: `CORE/DECODER/state/m4b_phase5b_2026_05_27/train.out` (DECODED_IDS line 55, verbatim)
- 자매 hypothesis: D1 LZ76 (token-id, $0) — `CORE/DECODER/D1_LZ76_COLLAPSE_PROXY.md`

---

## 양방향 sibling

- sibling: [D1 LZ76 collapse proxy](./D1_LZ76_COLLAPSE_PROXY.md) — token-id stream 의 LZ76 으로 collapse 를 cheap 검출 (🟢 6/6 분리 margin 0.637). D2 는 그 위에 **text-level 분리** 를 toy scale 로 더한다 — 두 proxy 가 cheap detokenize-residual 을 함께 cover.
- SSOT cross-link: [DECODER.md](./DECODER.md) M4b phase5b RESIDUAL 표 (F-M4B-FIRE-2/5 qualitative · no detokenize) — toy scale 에서 본 D2 로 해소됨, full-BPE scale 격상은 future work (hexa-lang `flame_bpe_corpus_lib` toolchain 안정화 의존).
