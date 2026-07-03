# H_9099 — self-chain content_axis 를 REAL 303M penult 에 접지하면 synthetic 축을 이김 (🟡 DIRECTIONAL-GREEN 4/5, POSITIVE)

- **slug:** `9099_selfchain_content_grounding`
- **tier:** 🟡 DIRECTIONAL-GREEN (engine-native, 4/5 frozen bars PASS) — real-penult grounding 이 self-chain 을 실제 경험 content 의 함수로 만듦
- **wired:** `engine-native` (rung-2 byte-exact TERMINAL) — `clm_penult_pooled` 는 `core/decode.hexa` 에 **LANDED** + ARCHITECTURE §decode/§SelfIdentity lockstep DONE; harness `state/9099_.../f4_engine_native.hexa` **COMMITTED**. 2026-07-03 독립 재현: **COMMITTED `[float]` op** 로 4/5 bar 전 수치 **byte-exact 일치**(원본은 aiden-only 임시 Map-return op 사용 — verdict-integrity 갭 close). WIRED-live 로의 잔여 = runtime self_drift_exp lane 23b 를 `clm_penult_pooled`(real per-tick content)로 급이(behavioral follow-on)
- **source:** UNIVERSE · fable #4
- **cross-ref:** [[H_9038]] (self_drift_exp informativeness lever) · [[H_1471]] self-continuity

## 발견 (fable #4, POSITIVE)

`self_drift_exp` 의 content_axis 를 **REAL 303M penultimate**(yn = readout 전 final-GroupNorm 출력,
T=24 mean-pool → d=768)에 접지하면 **synthetic 축을 이김** — self-chain 이 blind tick-clock 이 아니라
ACTUAL 경험 content 의 함수가 됨. **5 frozen bar 중 4개 PASS.**

## 코드 artifact (이 PR 에 LANDED)

`pub fn clm_penult_pooled(path, seed) -> [float]` 를 `core/decode.hexa`(clm_weights_free_pub 뒤)에 추가,
`_clmd_fwd_logits_sc` 에 reference-matched (sc["yn"] 추출, mean-pool). measurement-only(ONE forward,
decode loop 아님; readout conv 생략 — yn 이 penult). 하네스 `state/9099_selfchain_content_grounding/f4_engine_native.hexa`
(aiden rsync copy)는 core/decode.hexa + core/engine_cli.hexa import; content_axis = top-3 coarsened(%32)
penult axes; live §SelfIdentity self_drift_exp 구동.

## frozen bar (사전등록 · top-3 encoding 은 측정 前 고정: 768-dim single-argmax 는 trivial max-separate 라 배제)

- **BAR1 REAL-SEPARATES  PASS** meandist=0.536 (15 pairs, ≥0.10) — real inputs → 분리된 chain
- **BAR2 SYNTHETIC-BLIND PASS** blind_dist=2.22e-16 (≤1e-6) — synthetic self_drift 는 input-blind (neg control)
- **BAR3 REPRODUCIBLE    PASS** self_cos(I0 twice)=1.000 (≥0.999999) — deterministic grounding
- **BAR4 CONTENT-LOCKED  FAIL** fit_same=0.933 vs fit_diff=0.906, gap=0.027 < 0.05 — 방향 맞음, margin 미만 (coarse top-1 stream order-lock artifact, anti-real 아님; 정직 FAIL, tune 아님)
- **BAR5 GEOMETRY-TRACK  PASS** hi_mean=0.628(n6) > lo_mean=0.355(n9), margin=0.273 (≥0.05) — DECISIVE: chain distance 가 real penult geometry 를 TRACK

## verdict (engine-native, verbatim)

`hexa run f4_engine_native.hexa` (aiden pool, hexa v0.546.0, real 303M d768.clm, EXIT_RC=0, own-GEMM, NO numpy on measured path):

```
[penult] d=768
[top3] t0=205,125,131 · t1=140,273,23 · t2=621,205,125 · t3=557,273,140 · t4=205,125,621 · t5=557,273,205
RAW meandist(real 15pair)=0.5358832987924794
RAW blind_dist(synthetic self_drift)=2.220446049250313e-16
RAW repro self_cos(I0 twice)=0.9999999999999999
RAW fit_same=0.932548422734187 fit_diff=0.9057026934531928 gap=0.026845729280994268
RAW hi_mean(chain)=0.6281122739643402(n=6) lo_mean=0.35478631936964067(n=9) track_margin=0.27332595459469955
PASS BAR1 · PASS BAR2 · PASS BAR3 · FAIL BAR4 · PASS BAR5   --- 4/5 PASS ---
```

## content clustering (왜 BAR5 가 track)

top-3 penult axes 가 언어별 clustering: ko I0/I2/I4 는 {205,125,621} 공유; en/code I1/I3/I5 는
{273,140,557} 공유. penult-similar(같은 언어/topic) 입력 → 더 가까운 self-chain — input-blind synthetic
축은 가질 수 없는 성질.

## wiring status: engine-native (rung-2 byte-exact TERMINAL). WIRED-live 로의 잔여 1칸

- **rung-1 DIRECTIONAL-mirror** — N/A (측정이 처음부터 engine-native, numpy 미러 없음).
- **rung-2 ENGINE-NATIVE (byte-exact, DONE 2026-07-03)** — COMMITTED `core/decode.hexa` `[float]` op 로 harness 를 aiden(hexa v0.548.0, real d768.clm)에서 재실행 → 4/5 bar 전 수치 **byte-exact 일치**(top3 triples·meandist 0.5358832987924794·blind 2.22e-16·repro 1.0·fit_same/diff·track_margin 0.2733·4/5 전부 최종자리까지 동일). 원본은 aiden-only 임시 Map-return op 사용(never committed) → 이 재현이 committed-code↔verdict drift 0 확인 = verdict-integrity close. harness `f4_engine_native.hexa` COMMITTED.
- **rung-3 WIRE-IN (부분 DONE)** — `clm_penult_pooled` 는 measurement helper 로 `core/decode.hexa` 에 land. behavioral wire-in(runtime lane 23b feed)은 미완.
- **rung-4 ARCHITECTURE lockstep (DONE)** — §decode(op) + §SelfIdentity note 갱신 완료.
- **잔여 = WIRED-live** — runtime self_drift_exp lane 23b 를 현 synthetic amygdala/homeostat int axis 대신 `clm_penult_pooled`(real per-tick content)로 급이 (behavioral follow-on).

## engine-native caveat (정직)

forward 는 real ckpt 의 live core/decode.hexa 에서 돌았으나 device CUDA kernel 이 "named symbol not
found"(stale runtime build) → byte-exact HOST fallback(max|Δ|=0, penult 값 = real device 값);
_hx_k_gemm OWN-GEMM 1회 fired; cuda_available=1. 측정 유효성 무영향(byte-exact); GPU 가속만 partial.

## artifacts
- `state/9099_selfchain_content_grounding/notes.md`
- `state/9099_selfchain_content_grounding/f4_engine_native.hexa` (engine-native harness, COMMITTED — `[float]` API)
- `core/decode.hexa` (`clm_penult_pooled` LANDED)
- `state/verdicts/9099_selfchain_content_grounding/H_9099.txt` (frozen verbatim + rung-2 reproduction section)
