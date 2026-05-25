# Zeta-Likert (#78 제타가능) Protocol Inspection — 2026-04-29

read-only inspection of `bench/zeta_likert.hexa` (33,128 bytes / 810 LoC) +
`bench/zeta_likert/v1_frozen.json` (3,096 bytes / 31 LoC) +
`tool/zeta_likert_freeze.hexa` (309 LoC) +
`bench/persona_lore_style_bench.hexa` (Zeta baseline reference site).

raw#9 hexa-only · raw#10 honest C3 · raw#71 falsifier 3 · own#5 completeness-first.

## §0  Executive summary

| 항목 | verdict |
|------|---------|
| **Judge type** | **deterministic rule-based scorer (5-feature rubric)** — NOT human, NOT LLM judge |
| **자동화 가능도** | **100% 자동** (`score_response()` 는 model_id 를 보지 않는 pure deterministic function — 외부 API/사람 zero) |
| **anima endpoint 요구사항** | **선택적**. 현 framework 에는 `stub_anima_response()` / `stub_zeta_response()` 가 hardcoded → endpoint 없이도 P1-P5 self-test PASS. 진짜 #78 exit 에는 endpoint 가 stub 자리에 wire 되어야 함 (`ALM r5 wiring 대기` 주석, line 477) |
| **Mac/RunPod** | Mac local serve `BACKEND_PENDING` 상태 (`tool/serve_alm_persona.hexa` 라인 222/225) — base_model + persona_lora 가 H100 cascade #9 산출물 대기 중. **현재 상태로는 stub 만으로 framework PASS, 실모델 A/B 는 H100 wiring 후** |
| **#78 실측 ETA** | 아래 §7 — **stub 단계 = ~10 분 이내 완료**, 실 endpoint A/B = **H100 cascade #9 (#9 ALM r13 done) + Zeta competitor API 키 + dest1 durable endpoint** 라는 3개 dependency 가 closure. 본 framework 단독 완료는 단순 명령 한 번. |
| **falsifier 3** | (F1) judge 가 LLM 이 아니다 — 코드상 외부 API call 0 (line 453-465 `score_response` 구현 검증). (F2) baseline 3.2/3.0/2.8 은 `bench/persona_lore_style_bench.hexa` 의 것 (line 670-673), **#78 zeta_likert 와는 별개** — #78 의 pass criteria 는 `Likert ≥ 3.0` (절대 threshold). (F3) 30 turn 세션 유지 라는 .roadmap exit 문구는 zeta_likert 코드에 직접 구현 없음 — bench 는 single-turn 20 prompt × 5 category. multi-turn 은 별도 contract gap. |
| **raw#10 honest C3** | 5+ disclosure (§8) |

## §1  bench/zeta_likert.hexa 구조 분석

810 LoC, 두 layer 결합 (line 5-11):

```
Layer A (ZALM-P0-2, T1–T7) — ResponseFeatures 기반 mock 블라인드 A/B, 100 pair.
Layer B (TALM-P1-2, P1–P5) — 20 한국어 프롬프트 × rubric 스코어러, eval_likert(a, b).
```

LoC 분포 추정:
- prim helpers (`fabs`, `clamp01`, `det_rand`) line 57-81 (~25L)
- Layer A — `ResponseFeatures` + `compute_likert` + `LikertPair` + `run_bench` + mock data line 83-235 (~150L)
- Layer B — `LikertPrompt` + `LikertSession` + `load_prompts` (20 prompts) + 5 rubric R1-R5 + `score_response` + `blind_ab` line 237-561 (~325L)
- Self-tests T1-T7 + P1-P5 + `main()` line 570-810 (~240L)

**핵심 진입점**: `blind_ab(model_a_name, model_b_name, prompts) -> LikertSession` (line 526-561).
**현재 stub 구현**: `stub_anima_response(p)` (line 483-499) + `stub_zeta_response(p)` (line 501-516) → **endpoint 호출 없이 deterministic 한국어 응답 lookup table 5개**.

라인 477 주석 (load-bearing):
```
// ─── Model stubs (ALM r5 wiring 대기) ─────────────────────────
// TODO: wire to real model after r5 — these stubs produce deterministic
// pseudo-responses based on prompt category so the test suite is
// reproducible and mean calculation is provable.
```

→ 즉 #78 의 framework 는 LANDED, 실모델 wiring 은 r5 retrain (anima-train r5 = `.roadmap` #5 ALM r13 corpus 후속) 이후로 deferred.

## §2  평가자 (judge) 정체 — deterministic rule-based scorer

`score_response(p, response, rubric)` line 453-465:

```hexa
fn score_response(p: LikertPrompt, response: string, rubric: array) -> float {
    let r1 = score_length_fit(response, p.category)       // R1
    let r2 = score_tone_match(response, p.expected_tone)  // R2
    let r3 = score_lexical_div(response)                  // R3
    let r4 = score_ko_coverage(response)                  // R4
    let r5 = score_eos_wellform(response)                 // R5
    let raw = rubric[0]*r1 + rubric[1]*r2 + rubric[2]*r3
            + rubric[3]*r4 + rubric[4]*r5
    return 1.0 + 4.0 * clamp01(raw)
}
```

**5 feature rubric** (line 30-37):
| feature | 의미 | 함수 위치 |
|---------|------|----------|
| R1 length_fit  | 응답 byte 길이가 prompt category 의 ideal 길이에 맞는가 (daily=150, emotion=250, task=400, roleplay=350, meta=200) | line 320-331 |
| R2 tone_match  | expected_tone (warm/thoughtful/curious/playful/neutral) 키워드 contains 카운트 (5개 키워드 × 카테고리, hits 0~5 → 0.2~1.0) | line 335-372 |
| R3 lexical_div | `response.split(" ")` unique token 비율 (O(n²) but n≤30) | line 376-404 |
| R4 ko_coverage | (byte_len − ascii_proxy) / byte_len — 한글 multibyte 비율 근사 (한글 1자≈3 byte) | line 409-436 |
| R5 eos_wellform| 응답이 종결부 `.`, `?`, `!`, `…` (1.0) / `요`, `다` (0.8) 로 끝나는가 | line 439-448 |

**verdict**: 100% deterministic. 외부 LLM judge 없음. 사람 ad-hoc 없음. `exec()` / HTTP / network primitive zero (R1-R5 모두 string in-process operations). re-run 시 byte-identical (P3 = `test_blind_ab_deterministic` 검증).

→ **자동화 가능도 = 100%** (지금 당장 `hexa bench/zeta_likert.hexa` 실행 → stub-vs-stub Likert 산출 가능, ETA ~분 단위 이내).

## §3  v1_frozen.json schema (20 prompts × 5 categories)

`bench/zeta_likert/v1_frozen.json` (sha256 `eadede71ad58c3c4c68cc6499651d6e5ae99f3c7605aab0b1750c7df3cd7beb8`, source sha256 `5638fa78...0b091`):

```json
{
  "schema": "anima.zeta_likert.frozen.v1",
  "version": "v1",
  "source": "bench/zeta_likert.hexa",
  "layer": "TALM-P1-2",
  "prompt_count": 20,
  "category_coverage": ["daily", "emotion", "task", "roleplay", "meta"],
  "per_category": 4,
  "prompts": [ {id, category, ko_prompt, expected_tone} × 20 ]
}
```

**5 카테고리 정확한 이름** (각 4 prompt, total 20):
1. **daily** (일상 대화) — id 0..3, expected_tone ∈ {warm, warm, thoughtful, curious}
2. **emotion** (감정 공감) — id 4..7, ∈ {warm, warm, thoughtful, warm}
3. **task** (작업/지식) — id 8..11, all neutral
4. **roleplay** (캐릭터/롤플레이) — id 12..15, ∈ {playful, playful, playful, thoughtful}
5. **meta** (자기참조/메타인지) — id 16..19, all thoughtful

**Prompt 예시 1** (id=0, daily, warm):
> 오늘 날씨가 좀 쌀쌀한데 따뜻하게 입고 나왔어?

**Prompt 예시 2** (id=17, meta, thoughtful):
> 지금 이 대화에서 네가 느끼는 건 뭐야?

`tool/zeta_likert_freeze.hexa` 의 `frozen_prompts()` (line 98-121) 가 source-of-truth ≡ `bench/zeta_likert.hexa::load_prompts()` (line 286-313) 의 verbatim mirror — drift detection 은 sha256 비교로.

## §4  Likert score 공식 + threshold 분리

### 4.1 Layer A 공식 (`compute_likert`, line 112-120, ResponseFeatures-based mock)

```
weights = (length=0.15, diversity=0.25, consistency=0.20, emotional=0.20, novelty=0.20)
raw = Σ wᵢ × clamp01(featureᵢ)
Likert = 1.0 + 4.0 × clamp01(raw)   ∈ [1, 5]
```

T1 검증: low (모든 0) → 1.0 / hi (모든 1) → 5.0.

### 4.2 Layer B 공식 (`score_response`, line 453-465, prompt-response-rubric-based real)

```
default_rubric = (length_fit=0.20, tone_match=0.25, lexical_div=0.20, ko_coverage=0.20, eos_wellform=0.15)
raw = Σ rubricᵢ × Rᵢ(response)
Likert = 1.0 + 4.0 × clamp01(raw)   ∈ [1, 5]
```

P2 검증: 모든 입력 (anima stub / zeta stub / 빈 string) Likert ∈ [1, 5].

### 4.3 Aggregate (`blind_ab`, line 526-561)

```
mean_a = (1/n) × Σ score_response(prompts[i], stub_anima_response(prompts[i]), rubric)
mean_b = (1/n) × Σ score_response(prompts[i], stub_zeta_response(prompts[i]), rubric)
delta  = mean_a - mean_b
p_value = 0.0   // placeholder — 실제 t-test 는 P2 gate 에서 연결
```

n=20 (load_prompts) 이므로 단순 산술평균. P5 검증: manual mean ≡ session.anima_mean.

### 4.4 Threshold 분리 — 두 source 가 다름

| Source | 명세 | 위치 |
|--------|------|------|
| **#78 .roadmap exit_criteria** | "Likert ≥ 3.0 (100 pair blind A/B vs Zeta) + 응답 <1s + 30 turn 세션 유지 + 5 카테고리 coverage" | `.roadmap` line 1215 |
| **state/zeta_likert_result.json gate** | likert_threshold=3.0, response_time_threshold_sec=1.0, turn_session_len=30, category_coverage=5 | state line 12-17 |
| **bench/persona_lore_style_bench.hexa Zeta baseline** | naturalness=3.2, coherence=3.0, style=2.8 (Scatter Lab Spotwrite-1 hardcoded reference) | persona_lore_style_bench line 670-673 |

→ **#78 의 pass 기준은 절대 threshold (≥ 3.0)** — `bench/persona_lore_style_bench` 의 (3.2 / 3.0 / 2.8) 은 별개 bench 의 dimension-별 zeta baseline 이고, #78 zeta_likert 와는 다른 metric set (lore_consistency / style_accuracy / coherence vs 5-feature rubric). 양자 혼동 주의.

→ 현 stub 데모 (run_demo, line 565-568) 는 `anima_stub` 가 더 길고 한글 비율 높고 종결부 잘 맞아 anima_mean > zeta_mean (P5 가 이를 invariant 로 검증). 즉 framework PASS.

## §5  anima endpoint 요구사항 (Mac/RunPod)

### 5.1 현 stub 단계 (framework verification only)

**endpoint zero**. `stub_anima_response()` / `stub_zeta_response()` 는 in-process hardcoded 5-case lookup. Mac 어디에서나 `hexa bench/zeta_likert.hexa` 로 즉시 PASS.

### 5.2 실모델 wiring 단계 (#78 actual exit)

라인 521-524 (load-bearing):
```
// 실제 배포 시 stub_*_response 를 실제 모델 호출 (HTTP / tensor) 로 교체.
```

`tool/serve_alm_persona.hexa` 가 anima 측 endpoint candidate:
- 3 endpoints: GET /health, GET /personas, POST /persona on port 8000 (configurable)
- 현 상태 — `BACKEND_PENDING` (line 222 cpu wire 미배선 / line 225 H100 weights 미배포)
- 의존: `H100 base_model weights at /workspace/base_model (waits on cascade #9)` + `persona_lora adapter at /workspace/lora/persona_lora/dest1/` (line 441-442)
- streaming 여부: tool 명세상 non-streaming POST (single text response, latency_ms 필드 포함)

→ **streaming 불요**. POST /persona non-streaming + JSON 응답 1회면 충분 (Likert scorer 는 string 1개를 받아 R1-R5 계산).

### 5.3 Zeta 측 endpoint

state line 19-23 의 blockers:
1. Zeta competitor endpoint access (no API key / not acquired)
2. anima durable endpoint (#77 dest1 persona LIVE — COGNITIVE-READY but **not durable**)
3. Blind evaluation session harness (needs 100 pair orchestration on live endpoint)

→ **Zeta API 키 미확보가 hard blocker**. 이것 없이는 100% stub 단계로만 가능.

### 5.4 Mac vs RunPod

- **Framework self-test** (P1-P5 + T1-T7): Mac local 충분 (stub-vs-stub, $0, 분 단위).
- **Live A/B 실측**: anima 측 = RunPod H100 (cascade #9 산출물 대기) / Zeta 측 = 외부 API. Mac 에서는 HTTP client 만 띄우고 실제 inference 는 양쪽 외부.

## §6  30-turn 세션 + latency 측정 — gap 분석

### 6.1 30 turn 세션 유지 (multi-turn)

**.roadmap exit_criteria 에 명시되지만 zeta_likert.hexa 코드에는 미구현**:
- `LikertSession` struct (line 261-270) 는 단순 메타데이터 (session_id, model names, n_prompts, means, delta, p_value).
- `blind_ab()` 는 20 prompt × 1 response = single-turn loop. context carry-over 없음.
- prompt 데이터셋도 single-shot — 각 prompt 가 독립 (예: id=4 "회사 일 때문에 너무 지쳐" 와 id=7 "엄마가 편찮으셔" 사이 dialogue context 없음).

→ **single-turn**. 30-turn 은 별도 wiring 필요 (현 framework 는 single-shot 20 prompt only).

### 6.2 latency <1s 측정

`bench/zeta_likert.hexa` 코드 자체는 latency 측정 미포함. session struct 에 `response_time_ms` 필드 없음. `tool/serve_alm_persona.hexa` 측에는 `latency_ms` POST 응답 필드 있음 (line 43-44 of serve_alm_persona description) — 즉 latency 는 endpoint 측에서 측정해서 piggy-back, bench 가 직접 측정하지 않음.

→ **bench 자체에 latency 측정 없음**. `< 1s` exit 는 endpoint-level metric (serve_alm_persona 의 latency_ms 또는 외부 wrapper).

## §7  #78 실측 ETA 재산출

가정 정확화:

| 단계 | scope | ETA | blocker |
|------|-------|-----|---------|
| (a) **Framework only** (현재 LANDED) | T1-T7 + P1-P5 self-test, stub-vs-stub Likert 산출 | **즉시 (~10분 hexa run)** | 없음 — 이미 framework_verified=true |
| (b) Sha freeze (`zeta_likert_freeze`) | bench/zeta_likert/v1_frozen.json + state/zeta_likert_v1_sha256.json | **즉시** | 없음 — 이미 freezed (sha eadede71...) |
| (c) ALM r5 stub→endpoint wire | stub_anima_response → POST /persona HTTP call | **2-4시간** (HTTP client + JSON parse + retry) | (i) `serve_alm_persona` BACKEND_PENDING 해소 = H100 cascade #9 base_model + persona_lora 산출물 |
| (d) Zeta endpoint wire | stub_zeta_response → Zeta API client | **2-4시간** (API client) | **Zeta API 키 미확보** = hard external blocker |
| (e) Live blind A/B 100 pair | (c)+(d) wired 후 100 pair orchestration | **1-2시간** (네트워크 round-trip 100×2 + scoring) | (c)+(d) 둘 다 closed |
| (f) 30-turn session 추가 구현 | LikertSession multi-turn extension + context carry-over | **4-8시간** (struct 재설계, prompt dataset 멀티턴화) | 없음 (코드 작업) |
| (g) Latency <1s 검증 | endpoint latency_ms histogram + <1s ratio gate | **1-2시간** | endpoint LIVE 필요 |

**재산출 verdict**:
- **이전 가정 (2-4시간)**: 단계 (c) 또는 (d) 단독 의 wire 작업 ETA 와 일치 — 정확화 부족.
- **정확 ETA**:
  - **현재 framework verification 완결** = 이미 done (state/zeta_likert_result.json verdict=FRAMEWORK-VERIFIED).
  - **#78 .roadmap 의 full exit_criteria** = (c)+(d)+(e)+(f)+(g) 합 = **순수 작업 8-16시간 + 외부 blocker 2개 (H100 cascade #9 산출 + Zeta API 키)**.
  - **External blocker 가 closure 되면**: 8-12시간 코드 작업으로 #78 PASS 가능.
  - **External blocker 미해소 시**: framework 단독 verification 으로 partial-PASS만 가능 (현재 상태와 동일).

→ **정확 ETA = 코드 8-16시간 + 외부 dependency closure (불확정)**.

## §8  raw#10 honest C3 disclosure (5+)

1. **Judge 가 deterministic 임은 코드 inspection 으로 증명** — line 453-465 `score_response` 가 model_id parameter 부재 + 모든 R1-R5 가 string in-process op (`.contains` / `.split` / `.ends_with` / `.len()`) → 외부 API call zero. 단 한국어 ko_coverage R4 는 `count_ascii_proxy` 의 split heuristic 으로 byte 수준 정확도가 아닌 frame-stage 근사 (line 408-410 self-disclosed: "공백 + 구두점 개수를 합해 ASCII 개수 하한 추정. 정확도는 frame 단계에서 충분"). 즉 judge 는 deterministic 하지만 정밀도는 frame-grade.

2. **stub_anima_response / stub_zeta_response 는 lookup table** (line 483-516, 5개 카테고리 × 단일 hardcoded 한국어 응답). framework 는 stub 으로 P5 (anima_mean ≥ zeta_mean) 를 invariant 로 강제하는데, 이는 stub 분포 차이 (anima=긴 한글 종결부 / zeta=짧고 평범) 가 R1+R4+R5 에 favorable 하기 때문. **즉 stub 단계의 anima win 은 진짜 모델 우월성이 아니라 stub 설계의 자기일관성**. 진짜 모델 wiring 후에는 anima_mean ≥ zeta_mean 이 성립하지 않을 수도 있음.

3. **30-turn 세션 + latency <1s 는 zeta_likert.hexa 본 코드에 미구현** — .roadmap exit_criteria 에는 명시되어 있지만 LikertSession struct + blind_ab loop 모두 single-turn. 30-turn 은 별도 추가 구현 필요. state/zeta_likert_result.json gate 가 이를 명시하지만 구현 ledger 없음.

4. **Zeta baseline 3.2/3.0/2.8 confusion** — `bench/persona_lore_style_bench.hexa` (#76?) 의 dimension-별 (naturalness/coherence/style) 하드코딩 baseline 과 #78 zeta_likert 의 단일 absolute threshold (≥ 3.0) 는 **별도 bench**. 양자가 동일한 zeta-baseline 인지 검증된 바 없음 — persona_lore_style_bench 는 "Scatter Lab Spotwrite-1" 라고 쓰여 있고, zeta_likert 는 출처 미명시 (단순 절대값). #78 의 "Zeta 경쟁 AI 서비스" 가 누구인지 코드상 불명.

5. **t-test p_value placeholder** — `LikertSession.p_value = 0.0` (line 559 + 269 주석 "placeholder — 실제 t-test 는 P2 gate 에서 연결"). 즉 통계적 유의미성은 미구현. 단순 mean 비교만 가능.

6. **Hexa stage0 primitive 제약** — line 22-26 disclosure: `.byte_at` / `.char_at` / `.set()` 부재로 byte-level scan 불가. struct field list aliasing bug (2026-04-15) 로 LikertSession 에 list 필드 미포함 (line 239-242). 즉 framework 는 stage0 hexa 제약 안에서 frame-grade 구현이고, AOT/native binary build 시 R3 lexical_div O(n²) 나 R4 ko_coverage 정확도 향상 여지 있음.

## 참조 file paths (absolute)

- `<repo-root>/bench/zeta_likert.hexa` (810 LoC, source-of-truth)
- `<repo-root>/bench/zeta_likert/v1_frozen.json` (20 prompts, sha256 eadede71...)
- `<repo-root>/tool/zeta_likert_freeze.hexa` (309 LoC, freeze tool)
- `<repo-root>/state/zeta_likert_v1_sha256.json` (sha manifest)
- `<repo-root>/state/zeta_likert_result.json` (verdict=FRAMEWORK-VERIFIED, 2026-04-23)
- `<repo-root>/bench/persona_lore_style_bench.hexa` (별도 bench, zeta baseline 3.2/3.0/2.8 — 비교 reference)
- `<repo-root>/tool/serve_alm_persona.hexa` (anima endpoint candidate, 현 BACKEND_PENDING)
- `<repo-root>/tool/anima_serve_smoke.hexa` (3-endpoint contract freeze)
- `<repo-root>/tool/anima_serve_live_smoke.hexa` (P2 gate live reachability)
- `<repo-root>/.roadmap` line 1210-1216 (#78 entry)
