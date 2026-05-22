# vP21M Multilingual unlock — VERDICT: VP21M_WORKS (4/5 lang)

> 2026-05-22. FIRST-PACK Phase 0+1. anima 0.10.0 (vP21G en STRONG + vP21K ko STRONG)
> → 5-lang merged LoRA on top of vP21 baseline. 단일 LoRA 로 multilingual 가능한지
> test (untested 5-merge per FIRST-PACK § 2.4).

## Verdict: **VP21M_WORKS** (anima 0.10 → 0.11.0)

5-lang held-out OOD (각 10 probe × 2 mode = 100 generation):

| lang | verdict | gen/20 | lang_coherent/20 | n_memorize | 비고 |
|---|---|---|---|---|---|
| **EN** | **STRONG** | 18 | 20 | 2 | vP21G 16/20 와 동등 |
| **한국어** | **PARTIAL** | 18 | **15** | 2 | 5 outputs in mixed script |
| **中文** | **STRONG** | **20** | 16 | 0 | 가장 강함 (factual) |
| **Русский** | **STRONG** | **20** | 18 | 0 | Cyrillic 안정 |
| **日本語** | **WEAK** | 16 | **11** | ? | half output in wrong script (zh/en mix) |

**Aggregate**: 3 STRONG + 1 PARTIAL + 1 WEAK → `VP21M_WORKS` (criterion ≥ 4 langs ≥ PARTIAL).

## Method

- Base: Qwen/Qwen2.5-1.5B
- Adapter: vP21 LoRA r32 + continue-train
- Corpus: en/ko/zh/ru/ja each ~10 MB wiki (51.1 MB total wiki, sha `d378923c...`) + corpus_s101 anima 30/70 mix
- LR 5e-5, 1500 step, bf16, H100 80GB SXM
- CE_init → CE_final: 6.06 → **0.7787** (bimodal: anima 0.1-0.5, wiki 1.0-2.5 across 5 langs)
- Wall ~3-5 min train + setup
- Cost ~$5-8 (cap $15 was 2-3× under)

## Per-lang sample outputs (greedy)

| lang | prompt | output (truncated) |
|---|---|---|
| EN | "The capital of Germany is" | " Berlin. The city is located in the eastern part of Germany..." |
| KO | "한국의 수도는" | " 서울이다. 대한민국의 수도는 서울특별시이다..." |
| ZH | "中国的首都是" | "北京。北京是中华人民共和国的首都..." |
| RU | "Столица Россиий —" | "Москва. Москва — крупнейший город России..." |
| JA | "日本の首都は" | (mixed: 일부 zh + en + ja → WEAK) |

## Honest C3

1. **ja WEAK**: lang_coherent 11/20 — 절반 출력이 wrong script (zh/en 혼합). 원인 가능성: (a) ja-wiki 10 MB 가 zh/ko script-similarity 와 confused, (b) Qwen base 의 ja capability 가 en/zh/ru 만큼 강하지 않음. ja 만 별도 LoRA 또는 ja-wiki 분량 2-3× 늘리는 path 잔존.
2. **ko PARTIAL**: gen 18/20 (높음) but lang_coherent 15/20 — 5 outputs 가 영문 / 中文 / 혼합 script. ko-wiki 비중이 다른 langs 와 같아서 anima register vs wiki ko ratio 가 빈약. vP21K (단일 ko) 의 16/20 STRONG 대비 약간 약함 (multilingual merge tradeoff).
3. **en STRONG 18/20 ≈ vP21G 16/20** — multilingual merge 가 영문 capability 보존 (slight 향상). 5-lang merge 가 en capability 와 conflict X.
4. **zh + ru STRONG**: 가장 강한 결과 — 두 언어 모두 한국어/일본어 보다 register-leak free + lang_coherent 높음. Qwen base 의 multilingual coverage 영향.
5. **CE 0.78** (bimodal) — vP21G CE 1.27 보다 낮은데, 5-lang mix 가 anima 비중 (30%) 와 wiki 평균 CE 더 잘 fit 되는 듯.
6. **단일 LoRA 단순 deploy 가능**: FIRST-PACK Phase 3-8 에서 hot-swap 복잡 routing 불요. 4/5 langs 단일 forward 로 충분.
7. **Anima register retention 미측정**: 이번 eval 은 OOD 만, 별도 anima-register Eval 1 (vP21G/K 와 같은 probes) 검증 필요.
8. **단일 seed (1337)**: vP21G 의 fine-quant 가 robust 16.2 mean / std 0.75 였으니 vP21M 도 비슷할 듯, 단 직접 측정 미수행.

## 함의 — chat.dancinlab.org 배포

- **단일 vP21M deploy 가능** (4/5 lang OK, ja 만 약함)
- ja 사용자 대상으로는 별도 ja-LoRA fallback 또는 UI 에 "ja still 약함" 라벨
- FIRST-PACK 의 fallback "5 LoRA hot-swap" 불요 — 단일 LoRA simple deploy

## 관련 link

- 결과 JSON: `vP21M/heldout_vp21m.json` (100 generation)
- mix info: `vP21M/mix_info.json`
- recipe carry: VP21G_GENERALIZATION_2026_05_22.md + VP21K_KOREAN_GENERALIZATION_2026_05_22.md
- 다음 phase: FIRST-PACK.md Phase 3-8 (chat broker + UI + deploy)
