# D1 — LZ76 collapse proxy (`decoder-lz76-collapse-proxy`)

> verdict: 🟢 **SUPPORTED** · 6/6 falsifier PASS · 분리 margin 0.637 · $0 mac-local · 2026-05-28

## ① 배경 (context)

ANIMA DECODER (L3 콘텐츠 생성기, MoE decoder)의 핵심 난제 = **register collapse ↔ underfit 더블바인드**. M4b fire (PR #1121) phase5b 의 collapse 신호는 **실제 sampled token sequence** 로 남았다:

```
DECODED_IDS: 1 1 1 1 151642 151642 151642 ... 151642   (×16)
TTR=0.1  unique=2/20  →  F-M4B-FIRE-1 FAIL
```

- token 1 (×4) → expert e1 logit ≈ -0.03
- token 151642 (×16) = Qwen `<|endoftext|>`-class 특수 토큰 → expert e1 logit 938.767 saturate

현재 collapse 검출은 **qualitative** (no detokenize). UNIVERSE **H_288** (origin/main, 🟢 SUPPORTED Pearson r=0.831 ρ=0.936)이 LZ76 복잡도 ↔ faithful big-Φ 의 monotone 정렬을 실측했고, DECODER.md 가 "LZ 가 collapse 검출 1차 proxy 후보 — 반복-감소율 직접 측정 (구현 cheap, $0)" 라고 명시했다. **D1 은 그 proxy 를 detokenize 없이 실제로 검증한다.**

## ② 가설 (hypothesis · H_D1)

LZ76 복잡도(또는 정규화 LZ rate `LZ76/n`)가 **collapse 된 token sequence(반복 saturate)** 와 **healthy diverse sequence** 를 구별한다 — collapse seq 의 LZ76 ≪ healthy seq 의 LZ76, 두 band 가 noise 보다 큰 margin 으로 분리. 즉 LZ76 가 detokenize 없이 collapse 를 cheap 검출하는 proxy.

## ③ Falsifier (사전등록 · frozen 측정 前)

| id | 내용 | 판정 |
|---|---|---|
| **F-D1.1 REAL-COLLAPSE** | 실제 M4b sampled seq `[1×4, 151642×16]` 의 정규화 LZ rate < HEALTHY_FLOOR (0.50) | PASS |
| **F-D1.2 SEPARATION** (decisive) | `min(healthy LZ_norm) − max(collapse LZ_norm) > SEP_MARGIN (0.20)`. band 겹치면(margin ≤ 0) LZ proxy 무효 | PASS |
| **F-D1.3 MONOTONE** | raw LZ76 production-count 가 diversity 에 단조: `c(const) ≤ c(2-token) ≤ c(unique)` | PASS |
| **F-D1.4 ANCHORS** | constant seq raw_c 작음(< unique raw_c) · all-unique LZ_norm > 0 비퇴화 | PASS |
| **F-D1.5 DETERMINISM** | 실제 M4b seq LZ_norm 재실행 bit-identical | PASS |

**Falsifier (전체)**: LZ76 가 collapse vs healthy 를 구별 못함 (두 LZ76 값 겹침, 분리 margin < noise) → LZ proxy 무효, detokenize-기반 검출 불가피.

## ④ method — LZ76 정의 + token-id → binary stream

**LZ76 (Lempel-Ziv 1976, Kaspar-Schuster 1987 production-count)**: 0/1 stream 을 좌→우 parse 하여 distinct phrase(production) 개수 `c(n)` 를 센다. random binary → `c·log2(n)/n ≈ 1`; 단일 반복 symbol → `c ≈ 2` (≈ 0). 본 harness 의 `lz76()` 는 UNIVERSE/state/h288.../run_h288.hexa 의 함수를 **verbatim 재사용** (g61 no-reinvention).

**token-id → binary 변환**: token id sequence 는 직접 binary string 이 아니다. H_288 / clm_eeg_lz76_real 와 동일하게 **flat binary stream** 을 Kaspar-Schuster parse 에 먹인다. 각 token id 를 고정폭 `BITS=18` bit (2^18=262144 > vocab 151643) LSB-first 로 전개해 한 stream(길이 `n·18`)으로 concat. 반복(collapse) → 동일 18-bit block 의 long run → 적은 production; 다양성 → 많은 distinct block → 많은 production. 정규화 `LZ_norm = c(L)·log2(L)/L` (L = n·18, random → ~1, H_288 convention).

deterministic · hexa-only · $0 mac-local · LLM none · NO GPU · foreground.
harness = `CORE/DECODER/d1_lz76_collapse_proxy.hexa` · raw = `state/d1_lz76_collapse_proxy_2026_05_28/run_d1.out`

## ⑤ measurement — collapse vs healthy LZ (실측)

n=20 token sequence, BITS=18 → stream 길이 360 bit.

| sequence | 종류 | raw c(L) | **LZ_norm** |
|---|---|---|---|
| **REAL-M4b** `[1×4, 151642×16]` | collapse (실측) | 9 | **0.212296** |
| `collapse_const` `[t×20]` | collapse | 4 | 0.0943539 |
| `collapse_eot` `[151642×20]` | collapse | — | 0.165119 |
| `collapse_2tok` `[ab×10]` | collapse | 7 | 0.165119 |
| `healthy_unique` `[20 distinct]` | healthy | 38 | **0.896362** |
| `healthy_mixed` `[realistic repeat mix]` | healthy | — | 0.849185 |

- **collapse band MAX** = 0.212296 (실제 M4b seq 가 collapse band 최댓값)
- **healthy band MIN** = 0.849185
- **분리 margin** = 0.849185 − 0.212296 = **0.636889**

## ⑥ finding — 분리 가능 여부

**분리 가능. 강하게.** collapse band(최대 0.212)와 healthy band(최소 0.849)가 **0.637 margin** 으로 완전히 분리 — 사전등록 SEP_MARGIN(0.20)의 3.2배. 실제 M4b collapse sequence 가 HEALTHY_FLOOR(0.50) 의 절반 이하(0.212)에 착지하므로, **detokenize 없이 token-id stream 만으로 register collapse 가 cheap 검출된다**. raw production-count 도 단조(const 4 ≤ 2tok 7 ≤ unique 38) → LZ76 가 diversity 의 monotone 측정자임이 anchor 로 확인.

→ **H_D1 SUPPORTED**: LZ76 는 유효한 detokenize-free collapse proxy ($0, cheap). DECODER M4c p7 verify 의 "collapse 회피 verdict" 측정자로 즉시 사용 가능.

## ⑦ verdict

🟢 **SUPPORTED** · 6/6 falsifier PASS · 분리 margin 0.637 ≫ 0.20.

```
RESULT: 6 PASS / 0 FAIL
VERDICT: H_D1 SUPPORTED — LZ76 separates COLLAPSE vs HEALTHY (margin 0.636889 > 0.2).
         LZ76 is a valid detokenize-free collapse proxy ($0, cheap).
```

## ⑧ 함의 (DECODER 통합)

- **M4c p7 verify** 의 collapse-회피 verdict ← LZ_norm threshold (이번 측정 → **healthy floor 0.50** 가 실측 보정된 분리선). 생성 seq LZ_norm < 0.50 = collapse 경보, ≥ 0.85 = healthy 영역.
- Phase 5b RESIDUAL (F-M4B-FIRE-2/5 = qualitative · no detok) 중 **collapse-검출 측면은 D1 으로 해소** — BPE detokenize sampler(#1556) 없이도 LZ76 가 반복-saturate 를 잡는다. (단 coherence/언어-식별 측면 RESIDUAL 은 여전히 detokenize 필요.)
- UNIVERSE H_287 (Shannon ⊥ Φ) 와 정합: Shannon 엔트로피 단독은 collapse 판정 금지였고, 이번에 LZ76(H_288 정렬)이 그 대체 측정자로 **실제 collapse seq 위에서** 검증됨.

## ⑨ honest C3 (scope · 한계)

1. **n=20 toy**: 측정은 M4b 의 실제 20-token decode seq 위에서 했으나, full 생성(수백~수천 token)에서 LZ_norm 의 finite-length bias(Aboy/Hu 2006, n≤256 에서 ~20-30%)는 별도. 절대값보다 **band 분리**가 robust 한 신호 — threshold 0.50 은 toy 보정선, full-scale 재보정 권장.
2. **binarisation 선택**: 18-bit LSB-first 전개는 한 가지 token→bit map. id 의 bit 패턴 우연이 LZ 에 약간 섞일 수 있으나(예: 인접 id 의 공유 상위비트), 분리 margin 0.637 은 그 noise 를 압도. one-hot/Hamming-code 대안 binarisation 은 future work.
3. **proxy ≠ coherence**: LZ76 는 *반복-감소율* 만 측정 — high-LZ 인데 의미 incoherent(random-but-diverse)인 seq 는 LZ 가 healthy 로 오판할 수 있다. collapse(underfit 의 반대편) 검출에는 유효하나 coherence verdict 은 별도(detokenize + simple-stack 필요, M4c).
4. **단일 estimator**: LZ76 은 Kolmogorov 복잡도의 한 estimator. H_288 가 Φ 와의 정렬을 보였으나 LZ ≠ Φ.

## ⑩ artifacts

- harness: `CORE/DECODER/d1_lz76_collapse_proxy.hexa`
- raw verdict: `CORE/DECODER/state/d1_lz76_collapse_proxy_2026_05_28/run_d1.out`
- 실 데이터 source: `CORE/DECODER/state/m4b_phase5b_2026_05_27/train.out` (DECODED_IDS line 55)
- LZ76 reuse: `UNIVERSE/state/h288_kolmogorov_complexity_phi_correlate_2026_05_26/run_h288.hexa` (`lz76()` verbatim · g61)

---

## 양방향 sibling

- sibling: [UNIVERSE H_288](../../UNIVERSE/cards/H_288_kolmogorov_complexity_phi_correlate.md) — LZ76 ↔ Φ 정렬 (🟢 r=0.831 ρ=0.936)이 본 proxy 의 이론 근거. D1 은 그 LZ76 을 DECODER collapse 검출에 적용·검증.
- SSOT cross-link: [DECODER.md](./DECODER.md) UNIVERSE 정보-측도 arc cross-link 표 (H_287-290) — collapse 회피 verdict ← LZ 복잡도 (Shannon 단독 금지) 권고가 D1 으로 실증됨.
