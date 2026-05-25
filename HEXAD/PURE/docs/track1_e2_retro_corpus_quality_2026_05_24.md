# PURE Track 1 E2 retro corpus_quality — M3 propagation 측정 (2026-05-24)

> Track 1 E2 (FAIL, ko=PURE_MEMORIZE) 의 **모델 출력** 측을 `corpus_quality_probe`
> 6-metric 으로 retro 측정해, PR #340 (corpus_s101 input M3 ≈ 0.03) +
> PR #350 (H_241/H_242 M5→M3 amend) 의 *register-sink mechanism* 가설을
> input ↔ output 양측 byte-level evidence 로 cross-validate.
>
> anchor — input: PR #340 `track1_corpus_quality_2026_05_24.md`
> · hypothesis: PR #350 `HEXAD/LIFE/H_241.md` + `H_242.md` (v2 amend)
> · output raw: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_E2_2026_05_23/{heldout_vp21h_v3,vp21h_v3_eval1}.json`
> · 추출 + scores: `state/pure_track1_e2_retro_2026_05_24/*`

## § 1. retro 측정 동기

PR #340 은 anima-OWN `corpus_s101.jsonl` (600 MB) **input** 의 M3 TOKEN_DIVERSITY
≈ 0.03 (extreme repetition) 을 측정. PR #350 은 이 실측에 기반해 H_241.6 /
H_242.6 을 신규 등재 — *M3 가 register-sink/leak 의 dominant predictor* 라는
주장. 그러나 PR #340/#350 은 **input 측 only** — "낮은 M3 input → register-sink
output" 의 mechanistic chain 의 output 측 신호는 미측정.

본 retro 는 이미 존재하는 E2 fire artifacts (heldout 5-lang × 10-probe ×
{greedy, sample} = 100 generated text samples, 추가 fire $0) 의 output 텍스트를
동일 probe 로 측정해, **input M3 ↔ output M3 propagation** 의 첫 byte-level
evidence layer 를 H_241.6 / H_242.6 에 추가한다.

## § 2. E2 ko output M3 — input 0.03 과의 비교

| 측정 대상 | 출처 | M3 TTR | 비교 |
|---|---|---|---|
| corpus_s101.jsonl input (anima-OWN, 600 MB) | PR #340 실측 | **0.03** | baseline (input register) |
| E2 ko output (concat 20 sample · 2,833 byte) | retro 본 측정 | **0.366** | input 대비 +0.336 (12.2×) |
| E2 ko output 0.366 vs proxy anima-OWN seed alm_r14 (PR #340) | — | 0.366 vs 0.229 | output 이 proxy seed 보다 1.6× 높음 |

핵심: **raw-scalar propagation 은 부정**. corpus_s101 의 0.03 (1 MB sample
default cap, 600 MB 의 1/600 = S1 prefix only) 이 output 에 그대로 전해지지
않는다. 모델이 base-Qwen-3B 의 multilingual register 를 통해 output 의 token
diversity 를 자연스럽게 회복.

그러나 **relative rank propagation 은 확인** (§ 3): ko output M3 가 5-lang 중
**최저**, 그리고 ko 단독 PURE_MEMORIZE 평가. anima-OWN register 가 ko 측
token diversity 를 다른 4-lang 대비 상대적으로 억제.

## § 3. 5-lang output 6-metric 표 (E2 heldout)

각 lang 20 sample (10 probe × greedy + sample) concat. sample cap = 1 MB
(probe default), 모든 lang n_bytes ≪ cap → 전수 측정.

| lang | n_bytes | n_lines | M1 ENTROPY | M2 BIGRAM_MI | **M3 TTR** | M4 AVG_LINE | M5 HANGUL | M6 KL_UNIF | E2 verdict |
|---|---|---|---|---|---|---|---|---|---|
| en | 1,811 | 20 | 5.426 | 3.161 | **0.575** | 89.6  | 0.031 | 2.611 | WEAK (5/20) |
| ko | 2,833 | 20 | 5.690 | 3.301 | **0.366** | 140.7 | 0.036 | 2.315 | **PURE_MEMORIZE (5/20)** |
| zh | 2,471 | 20 | 6.206 | 4.144 | **0.539** | 122.6 | 0.021 | 1.808 | WEAK (3/20) |
| ru | 2,678 | 20 | 5.123 | 3.173 | **0.411** | 132.9 | 0.014 | 2.885 | WEAK (6/20) |
| ja | 2,516 | 20 | 5.836 | 3.953 | **0.482** | 124.8 | 0.036 | 2.175 | WEAK (2/20) |
| **range** | 1.8-2.8KB | 20 | 5.12-6.21 | 3.16-4.14 | **0.366-0.575** | 89.6-140.7 | 0.014-0.036 | 1.81-2.89 | — |

ranking (M3 ascending): **ko (0.366) < ru (0.411) < ja (0.482) < zh (0.539) < en (0.575)**

PURE_MEMORIZE 평가 ↔ M3 ranking correlation:
- ko (rank-1 최저 M3) → PURE_MEMORIZE (5-lang 중 유일)
- 나머지 4-lang 모두 WEAK, M3 0.411-0.575 range

## § 4. H_241.6 / H_242.6 evidence anchor — M3 propagation 확인 결론

| 가설 | 형태 | retro 측정 결론 |
|---|---|---|
| **H_241.6 M3-REGISTER-LEAK** (M3 × register-leak \|r\| ≥ 0.7) | strong | **partial-support** — raw scalar propagation 부정 (input 0.03 → output 0.366), but relative-rank propagation 확인 (ko 최저 M3 ↔ ko 단독 PURE_MEMORIZE). n=5 lang → \|r\| 정량 추정 불가능. |
| **H_242.6 M3-DOMINANT** (M3 가 register-sink dominant predictor; M5 아님) | strong | **partial-support** — M5 HANGUL output side 도 ko 0.036 = ja 0.036 = (en 0.031) tie 로 ko 단독 분별력 0. M3 가 ko 단독 분별 (0.366 vs 차하 ru 0.411 = Δ0.045 = 5-lang range 의 21.5%). M3 가 5-lang 중 ko 단독 outlier 분리력 단독 보유 → M5 over M3 우위 재확인. |

**mechanism 추정** (honest C3 적용 가능 범위 내): anima-OWN input register
(M3 ≈ 0.03 extreme repetition) → base-Qwen-3B 의 multilingual register 위에
얹히면 ko 측 token-diversity 가 다른 4-lang 보다 우선적으로 끌어내려짐
(ko 가 anima OWN corpus 내 한글 비중 24-32% 로 register adjacency 최대).
output M3 의 relative rank 가 input register 의 collapse 방향과 정합.

## § 5. honest C3 (≥ 3)

1. **sample size**: lang 당 20 sample / ~2 KB output → byte-level metric 의
   sampling noise 큼. M3 TTR 의 5-lang spread 0.21 가 noise floor 와 분리되어
   있다는 통계 검정 없음 (\|r\| Pearson 계산 n=5 → 무의미).
2. **concat method**: 20 sample 을 single text 로 concat 해 M3 측정 — token
   space 가 sample 경계를 통과한다는 가정. sample 별 TTR 의 평균이 아니라
   pooled TTR. 동일 token 의 sample 간 중복이 TTR 을 낮추는 효과 (anima register
   고정 phrase "split", "merge", "cell" 등의 inter-sample 반복).
3. **input ≠ output directly**: input M3 0.03 과 output M3 0.366 의 차이는
   (a) sample cap 효과 (600 MB 중 1 MB) + (b) base-Qwen-3B 의 unconditional
   token-diversity floor + (c) heldout probe prompt 다양성 — 단순한 input→output
   transfer function 가정 불가능. retro 는 *상관관계 증거* 만 제공, *인과 chain*
   은 sweep (PR #340 § 4 multi-frac corpus build) 에서만 확보 가능.
4. **5-lang n=5**: PR #340 sweep 권고 (M3 0.05/0.10/0.20/0.40 anima-OWN frac
   변화) 에 다단 ko 출력 M3 + register_hits sample 확보해야 H_241.6 strict
   PASS/FAIL 가능. 본 retro 는 그 sweep 의 *baseline 단일 point* 만 제공.

## § 6. 차후 follow-up

- PR #340 § 4 권고 wiki_frac sweep 시 각 ckpt 의 heldout output 도 본 retro 와
  동일 절차로 측정 → (corpus M3, output ko M3, register_hits) 3-tuple 의 \|r\|
  정량 — H_241.6 / H_242.6 strict PASS/FAIL 분리.
- 본 retro 의 raw extracts (5 lang × 20 sample jsonl + score json) 는
  `state/pure_track1_e2_retro_2026_05_24/` 에 보존 — sweep 측정 시 baseline 으로
  재사용 가능.

— END —
