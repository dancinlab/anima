# PURE Track 1 corpus quality — 6-metric 측정 보고서 (2026-05-24)

> Track 1 (E2 anima 50% + E3 anima 0%) 의 corpus 축 closure FAIL 진단.
> `HEXAD/PURE/eval/corpus_quality_probe.hexa` (PR #287) 의 6-metric scorer
> 를 가용 corpora 에 적용해 "corpus quality 부족" 가설을 정량 분리한다.
>
> anchor — spec: [`../spec/track1_corpus_reburn_spec_2026_05_23.md`](../spec/track1_corpus_reburn_spec_2026_05_23.md)
> · probe SSOT: [`../eval/corpus_quality_probe.hexa`](../eval/corpus_quality_probe.hexa)
> · raw 출력: `state/pure_track1_corpus_quality_2026_05_24/*.{json,log}`

## § 1. 측정 대상 + 가용성

Track 1 의 실 corpus 입력 2 종 (launcher 가 변형별 jsonl 로 mix):

| 입력 | 정의 | local 가용 |
|---|---|---|
| `corpus_s101.jsonl` (anima-OWN seed, ~600 MB, sha=39d581da…) | E2 의 anima 50% 측 | ✗ **`.gitignore` 됨** (`state/corpus_s101_build_s102_2026_05_19/result.json` 만 SSOT, payload 부재) |
| `multi_wiki_corpus.jsonl` (5-lang, 51.1 MB, sha=d378923c…) | E2/E3 양측 multilingual base | ✗ pod-side build only (`vP21M/multi_wiki_source.json` = manifest 만, payload 부재) |

→ **실 Track 1 입력은 0/2 로컬 측정 가능**. 본 보고서는 **anima-OWN 계열
proxy corpora 4종 + 5-lang 합성 fixture 1종 = 5건** 을 측정해 anima-OWN
register 의 quality envelope 만 정량화한다. 결론은 그 envelope 내에서만
유효 (§ 4 honest C3 참조).

| proxy | 경로 | 크기 | 역할 |
|---|---|---|---|
| **alm_r14** | `experiments/alm_r14/corpus_alm_r14_v1.jsonl` | 1.4 MB | anima-OWN seed 계열 (corpus_s101 sister) |
| **tier1_low** | `state/corpus_tier_tier1_low.jsonl` | 955 KB | 동 tiered low slice |
| **alm_r13_seed** | `experiments/alm_r13/seed_corpus_10mb/corpus.jsonl` | 741 KB | r13 seed 10 MB sub-sample |
| **sanity_carving** | `HEXAD/CARVING/state/carving_p_tts_2026_05_18/sanity_corpus.jsonl` | 208 KB | 다른 domain (TTS sanity) 대조군 |
| **fixture_5lang** | `HEXAD/PURE/eval/fixture_5lang_v1.json` | 4.9 KB | 5-lang multi_wiki proxy (probe 자체 fixture) |

샘플 cap = probe default 1 MB. 모든 측정 `hexa run … score <path>` exit 0.

## § 2. 6-metric 결과 표

| corpus | M1 ENTROPY | M2 BIGRAM_MI | M3 TTR | M4 AVG_LINE | M5 HANGUL | M6 KL_UNIF |
|---|---|---|---|---|---|---|
| alm_r14 (anima seed) | **5.7835** | 2.0058 | 0.2294 | 1181.0 | **0.3217** | 2.2332 |
| tier1_low | 5.7156 | 2.6618 | 0.2458 | 1165.5 | 0.2370 | 2.2954 |
| alm_r13_seed | 5.7356 | 2.6618 | 0.2474 | 956.7 | 0.2374 | 2.2758 |
| sanity_carving | 5.7139 | **3.4578** | 0.0558 | 665.1 | 0.0630 | 2.2975 |
| fixture_5lang (proxy multi_wiki) | 5.7318 | 3.0571 | **0.3151** | 47.8 | 0.0323 | 2.2750 |
| **range** | 5.71-5.78 | 2.01-3.46 | 0.06-0.32 | 47.8-1181 | 0.03-0.32 | 2.23-2.30 |

핵심 관측:
- **M1 (entropy)** + **M6 (KL_uniform)**: 5건 모두 거의 동일 (Δ≤0.07 bit · Δ≤0.07 nats). bytes-level skew 가 corpus 간 거의 invariant → entropy 가 PURE Track 1 의 변수 아님.
- **M2 (bigram MI)**: anima-OWN seed (2.0-2.7) < multi_wiki proxy (3.06). 다국어 fixture 의 byte-bigram 상관이 더 강함 (UTF-8 다바이트 시퀀스 효과 가능성).
- **M3 (TTR)**: anima-OWN 평균 0.24 vs sanity 0.06 vs fixture 0.32. 다국어 fixture 가 가장 token-diverse.
- **M5 (hangul)**: anima-OWN 32%/24%/24% vs multi_wiki proxy 3%. anima-OWN 의 한글 비중이 다국어 base 대비 10× 가까이 높음 — register collapse 시 ko 가 anima register 로 끌려갈 risk 정량적.

## § 3. E2 FAIL (0/5 ≥ PARTIAL) 과의 상관

Track 1 E2 dispatch 결과 (`/private/tmp/anima-track1-fire/state/pure_track1_2026_05_23/E2.log`):

```
VERDICT= FAIL
  n_strong= 0 /5  n_partial= 0  n_weak= 4  n_pure_memorize= 1
  per_lang: en WEAK 5/20 · ko PURE_MEMORIZE 5/20 · zh WEAK 3/20 · ru WEAK 6/20 · ja WEAK 2/20
  anima_register_hits= 4/20  register_regress= True
  init_CE= 14.178  final_CE= 0.985  train_wall_s= 2105.8
```

**measurement-level 진단**:

| 가설 | 본 보고서 측정으로의 함의 | 평가 |
|---|---|---|
| (a) corpus 가 quality 낮아서 fail | M1/M6 으로는 anima-OWN proxy 가 다국어 fixture 와 동일 수준 (Δ≤0.07). entropy/skew 측 quality 결손 무 | ✗ 비지지 |
| (b) corpus mix 의 register imbalance 가 model 을 anima register 로 끌어당김 | M5 한글 비중 24-32% (anima-OWN) vs 3% (multi_wiki) → 50:50 mix 시 한글 영역의 anima register dominance 가 ko=PURE_MEMORIZE 와 직접 호응 | ✓ **정합** |
| (c) corpus 는 OK 이고 model dynamics (head_g · mitosis · curriculum) 이 collapse 원인 | M2/M3 의 anima-OWN ↔ multi_wiki gap 은 byte-bigram MI 0.4 / TTR 0.07 — moderate. corpus 만으로는 ko PURE_MEMORIZE 의 4 anima_register_hits + register_regress=True 를 완전히 설명 못함 | ⚠ **잔여** |

**결론**: 본 6-metric 측정 범위에서 corpus 가 "낮은 quality" 라는 증거는
없다 (M1/M6 균일). 다만 (b) register-imbalance 가설 — anima-OWN 의 높은
M5 한글 비중이 50:50 mix 에서 ko 채널을 anima register 로 sink 시키는 —
는 정량적으로 정합. E2 FAIL 은 **"corpus quality 부족"이 아닌
"corpus composition (M5 분포) + model dynamics" 의 합작**이라는 honest
diagnosis. AXIS_MAP fallback (B 증류 · A 커리큘럼 · C head_g) 중
**A (curriculum 으로 register 분리)** 가 본 측정의 자연 연장.

## § 4. Honest C3 (≥3)

1. **실 corpus 0/2 측정 불가**: corpus_s101 (.gitignore) + multi_wiki
   (pod-side only). proxy 5건 측정은 anima-OWN register envelope 만
   포착. multi_wiki 의 실 51 MB 5-lang 분포는 본 보고서로 검증되지 않음.
2. **샘플 1 MB cap**: 모든 corpus 의 첫 1 MB 만 read (`--sample-bytes`
   default). 600 MB corpus_s101 의 1/600 ≈ S1 prefix 만 반영 — tail
   diversity 누락 (실 corpus 의 § 102 result `tail_region_eff_4grams_5mb_sample`
   = 941 vs prefix 539, 본 1 MB cap 이 prefix-biased 임을 보여줌).
3. **probe metric 의 PURE-specific 적합성 미검증**: 6-metric 은
   anima-engines/P22 의 합성 panel self-test 에서 derive. PR #287 의 spec 도
   "candidate metrics" 으로 명시. M5 hangul-coverage 외에는 register
   collapse / multilingual PASS_STRICT 와의 상관이 별도 fire 로 calibrate
   필요 — 본 보고서 § 3 의 (b) 정합은 **단일 metric (M5) 만의 매칭**
   이라 가설 reinforcement 일 뿐 진단 closure 아님.
4. **E3 log 단절**: E3 FAIL verdict 본 보고서 작성 시점에 log 미수집
   (TRAIN_PID 480 까지만 tail). E2 단독 비교는 anima 비중 0% lane
   부재한 채로 50% lane 만 평가 — 결정 트리 (둘 다 FAIL → AXIS_MAP B/A/C
   fan out) 의 한쪽 다리만 확인.
5. **proxy ↔ 실 corpus equivalence 미증명**: alm_r14/tier1_low 가
   corpus_s101 의 quality envelope 와 byte-level 일치한다는 증명 없음.
   sha 비교는 sha=39d581da… (s101) vs 본 4건 sha 미수집 — 단지 "anima-OWN
   계열"이라는 provenance 일치 가정.

— 끝 —
