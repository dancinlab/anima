# PURE corpus_s101 실측 corpus quality — anima-OWN register signature (2026-05-24)

> PR #303 이 측정 못 한 **실 Track 1 입력** `corpus_s101.jsonl` (~600 MB,
> E2 의 anima 50% 측) 을 `corpus_quality_probe.hexa` (PR #287) 로 직접 측정.
> PR #303 은 anima-OWN proxy 5건만 측정 — 본 보고서는 anima-side 실 anchor 를
> 채워 H_241 (corpus quality Φ correlate) + H_242 (register collapse sigmoid)
> 의 anima-OWN 기준점을 확정한다.
>
> anchor — proxy 보고서: [`track1_corpus_quality_2026_05_24.md`](track1_corpus_quality_2026_05_24.md)
> · probe SSOT: [`../eval/corpus_quality_probe.hexa`](../eval/corpus_quality_probe.hexa)
> · 빌드 manifest: `state/corpus_s101_build_s102_2026_05_19/result.json`
> · raw 출력: `state/pure_corpus_s101_quality_2026_05_24/*.{json,log}`

## § 1. 측정 대상

| 항목 | 값 |
|---|---|
| corpus | `state/corpus_s101_build_s102_2026_05_19/corpus_s101.jsonl` |
| 역할 | Track 1 E2 의 anima-OWN 50% 측 (E3 는 0%) |
| 크기 | 603,316,592 bytes (≈575 MiB) · 777,845 records |
| sha256 | `39d581da209615468c1c41e07aa8662ef1074bc5be49a666f8f861753dd5810e` (빌드 manifest verbatim — PR #303 의 `be969af4…` 표기는 부정확, manifest SSOT 가 정본) |
| 구성 | S1 `s1_s16_verbatim.jsonl` prefix (777,000 carving records, byte-equal) + S2 168×5 framing + S5 좌표 5건 |
| 가용 | local (`.gitignore` 됨; manifest 만 tracked) — 본 측정으로 0/2 → **1/2 실 입력 측정** |
| 샘플 | head 1 MB (probe default) + head 5 MB (`--sample-bytes`, manifest `tail_region_5mb` 대조용) 2회 |

`hexa run … score …` 양측 exit 0. payload 는 sister worktree 의 byte-identical
복사본 (size + manifest sha 일치) 을 canonical 경로로 symlink 해 측정. probe 의
byte-level 루프는 hexa-interp 에서 O(n × distinct) — 50 MB+ 샘플은 비현실적
wall 이라 5 MB 로 절충 (§ 5 C3 #1).

## § 2. 6-metric 결과 표 (verbatim)

| sample | M1 ENTROPY | M2 BIGRAM_MI | M3 TTR | M4 AVG_LINE | M5 HANGUL | M6 KL_UNIF |
|---|---|---|---|---|---|---|
| **head 1 MB** | 5.49966 | 3.45778 | 0.0343642 | 623.61 | **0.0165957** | 2.50333 |
| **head 5 MB** | 5.5918 | 3.45778 | 0.0296977 | 680.756 | **0.0234043** | 2.41586 |

(1 MB: n_bytes=1000000 n_lines=1601 · 5 MB: n_bytes=5000000 n_lines=7334)

핵심 관측:
- **M5 (hangul)**: 1.66% (1 MB) → 2.34% (5 MB) — head 확장 시 *상승*하나 여전히
  proxy 24-32% 의 1/10 수준. prefix-bias 보정해도 대역 밖 (§ 3).
- **M3 (TTR)**: 0.034 → 0.030 — head 확장 시 *하락* (반복 누적). proxy 0.24-0.32
  대비 1/8-1/10, sanity 0.056 보다도 낮음. 강한 memorization 신호 (§ 4).
- **M2 (bigram MI)**: 1 MB·5 MB 동일 (3.45778) — probe 가 앞 512 byte 만 사용
  (cap), 두 sample 의 prefix 동일하므로 불변. anima-OWN proxy (2.0-2.7) 보다 높음.
- **M1/M6**: proxy 대역 (5.71-5.78 / 2.23-2.30) 과 근사 (5.50-5.59 / 2.42-2.50) —
  entropy/skew 측 quality 결손 무.

## § 3. PR #303 proxy 5건과의 비교 — M5 hangul 일치 여부

PR #303 의 anima-OWN proxy M5 hangul: alm_r14 = **0.3217 (32%)** · tier1_low =
**0.2370 (24%)** · alm_r13_seed = **0.2374 (24%)** (multi_wiki proxy 는 0.0323).

| 가설 (PR #303 예고) | corpus_s101 실측 | 평가 |
|---|---|---|
| corpus_s101 M5 가 24-32% proxy 대역에 들 것 | **1 MB = 1.66% · 5 MB = 2.34%** — 둘 다 대역 **밖** (proxy 의 1/10-1/19; sample 키워도 추세 불변) | ✗ **불일치** |
| → 원인 | M5 는 *distinct 한글 음절 triplet / 2350* (KS X 1001 coverage). corpus_s101 의 S1 prefix 는 carving 템플릿 — "의식 풍경 위 진공점", "tension flow 가 이 vacuum 으로" 등 **고정 문구가 tier×anchor 로 반복**돼 한글 *분량*은 많으나 *고유 음절 다양성*은 낮음. proxy (대화체 anima-OWN) 는 음절 다양 → 24-32% | — |

핵심: PR #303 의 C3 #5 ("proxy ↔ 실 corpus equivalence 미증명") 가 본 실측으로
**반증**됐다. anima-OWN proxy 의 M5 24-32% 는 corpus_s101 의 register signature
를 대표하지 **못한다** — 적어도 head-prefix 영역에서는. corpus_s101 의 anima
register signature 는 "고-분량·저-음절-다양성 carving 템플릿" 으로, proxy 의
"중-분량·고-음절-다양성 대화체" 와 질적으로 다르다.

## § 4. E2 ko=PURE_MEMORIZE 와의 연결 — 어느 metric 이 register sink 를 예측하나

E2 결과 (PR #303): `ko PURE_MEMORIZE 5/20 · anima_register_hits=4/20 · register_regress=True`.

- PR #303 의 (b) 가설 — *높은 M5 한글 비중이 50:50 mix 에서 ko 채널을 anima
  register 로 sink* — 은 **proxy 의 M5=24-32%** 에 기댄 것이었다. 그러나
  실측 corpus_s101 의 head M5 는 1.66% (1 MB) / 2.34% (5 MB) 로, "한글 음절
  *coverage* 가 높아서" ko 가 끌려간다는 메커니즘은 **약화**된다.
- 더 정합한 register-sink 예측자는 **M3 TTR**: corpus_s101 = **0.034** (proxy
  0.24-0.32 의 1/7, sanity 0.056 보다도 낮음). 극저 TTR = 동일 토큰열의 강한
  반복 = **memorization 유도 신호**. ko=PURE_MEMORIZE 의 "memorize" 는 한글
  *coverage* 가 아니라 **반복도 (저 TTR)** 와 호응한다 — anima register 의
  carving 템플릿이 50% 를 점할 때, 모델이 그 고-반복 한글 패턴을 통째 암기.
- M1/M6 (entropy·skew) 은 proxy 와 유사 대역 (5.50-5.59 / 2.42-2.50 vs
  5.71-5.78 / 2.23-2.30) 으로 quality 결손 아님 — PR #303 의 (a) "낮은
  quality" 비지지 결론 **재확인**.

→ **register sink 예측자 갱신**: M5 (coverage) 가 아니라 **M3 (TTR, 반복도)**
가 ko=PURE_MEMORIZE 의 anima-side anchor. H_242 register-collapse sigmoid 의
입력 변수 후보를 M5 → **M3** 로 이동시킬 근거. AXIS_MAP fallback 중
**A (curriculum: 고-반복 carving 템플릿을 후반 배치로 분리)** 가 본 실측의
자연 연장 (PR #303 결론과 일치).

## § 5. Honest C3 (≥3)

1. **head-sample 한계 (prefix-bias)**: 1 MB·5 MB 모두 corpus 의 *head* 만
   read (`substring(0, N)`). 600 MB 의 1/600-1/120 이며 전부 S1 carving prefix
   영역. 빌드 manifest `tail_region_eff_4grams_5mb_sample=941` vs prefix 539 —
   tail 의 S2 framing(다양 축) + 후반 carving 은 본 측정에 미반영. M5/M3 의
   실 whole-corpus 값은 head 값보다 높을 개연 (5 MB 행이 1 MB 대비 어떻게
   변하는지 참조). probe 의 byte-level O(n×distinct) 루프 때문에 50 MB+ /
   whole-corpus 측정은 hexa-interp 에서 비현실적 — 별도 sampled-stream cycle.
2. **syntactic-only**: 6-metric 은 byte/token 표면 통계 (entropy·MI·TTR·
   line·hangul-triplet·KL). 의미·register *내용* 은 미측정. ko=PURE_MEMORIZE
   ↔ M3 의 연결은 **상관 가설**이지 인과 closure 아님 — fire-tier calibrate 필요.
3. **단일 corpus + proxy equivalence 반증의 일반화 한계**: corpus_s101 1건만
   실측. multi_wiki (E2/E3 양측 base) 는 여전히 pod-side only 로 미측정 —
   E2 mix 의 *나머지 50%* 미관측. 본 보고서는 anima 50% 측 anchor 만 확정,
   E2 전체 mix 의 측정은 multi_wiki pull 후 별도 cycle.
4. **probe metric 의 PURE 적합성 미검증** (PR #303 C3 #3 carry): M3 를
   register-sink 예측자로 격상한 것은 단일 metric 매칭이라 가설 reinforcement
   일 뿐 진단 closure 아님.

— 끝 —
