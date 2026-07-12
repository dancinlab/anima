# H_9286 — NBIND-G: 자연 원자 GROUNDING 전이 (H_9272 다음 유일한 진짜 새 질문)

## tier
🟢-dir **CARRIER-ROBUST** (N1 착지 · 2026-07-12) — Fable 판정으로 도출된 NBIND-G가 XBIND+H_9272+STAGE0이
못 본 유일한 non-tune-to-green 질문. $0 N0(manifest+P_nat freeze)+N1(carrier 전이 eval·summer $0) 완료 =
연산자가 literal 학습프레임 비구속(C0 0.750→C1 0.675→C2 0.700, FORMAT-🧱 반증). grounding 본체(P_nat)=
N2 spend-gated(owner $go). GREEN 미cement(1 seed·grid-atom scope).

## 가설
H_9267 XBIND CRACK(합성 ±비트)과 H_9272 NBIND(🟡 DIRECTIONAL·held-out D-acc 0.700)은 "held-out
XOR signal이 corpus에 있으면 303M이 학습가능"을 자연 어휘까지 확장했다. 그러나 **H_9272의 grid arm은
실질적으로 XBIND 재도색** — pol(p)를 authored grid가 공급(모든 predicate가 seen 셀에 등장). Fable 판정:
XBIND·H_9272·STAGE0가 **못 본 유일한 새 질문 = ATOM-GROUNDING 전이** — grid가 가르친 XOR 연산자가,
극성이 **자연 분포적 사용에서만 접지된** 원자에 적용되는가? = "자발 창발"을 (자연서 feature 접지)×(연산자
설치)로 분해해, DATA-🧱 하에서 유일하게 가능한 합성을 테스트.

## GROUND-TRUTH 제약 (이번 턴 reference-match · gen_nbind.py)
H_9272 학습 corpus(`nbind_train.txt`)는 **100% authored grid 라인** `이 영화 <surf> => <긍정/부정>.` —
**raw NSMC 리뷰 텍스트 0**. 따라서:
- **GROUNDING 본체(P_nat 원자·극성 자연접지)는 기존 ckpt로 측정 불가**(접지 소스 부재) → N2 spend-gated
  재학습(raw NSMC 혼합)만이 담지.
- 기존 ckpt의 유일 valid $0 falsifier = **20개 grounded grid predicate**(seen 0.92) + in-distribution
  `=> 긍정/부정` readout 유지. 전이 가능한 단일 변수 = **carrier**(surf 앞 프레임, 학습값 "이 영화 ").
- ⟹ Fable의 "atom-held-out" N1 표현은 zero-raw-NSMC를 몰라 생긴 혼동; readout 제약이 N1을
  **carrier-transfer(grid atoms)**로 확정.

## N1 설계 — CARRIER-DISTANCE 사다리 (frozen·$0·기존 ckpt·재학습 없음)
동일 40 held-out (p,form) 셀, 3 carrier 레벨:
| level | carrier | 의미 |
|---|---|---|
| **C0** | `이 영화 <surf> =>` | 학습 carrier → 0.700 재현(양성대조·ckpt 유효성) |
| **C1** | `<대체 영화도메인 명사구> <surf> =>` | 근전이(carrier 어휘 교체) |
| **C2** | `<verbatim 실제 NSMC 리뷰> <surf> =>` | wild-natural 원전이(Fable bar-3, valid readout) |

**Frozen 판정(사전결정)**:
- C0가 0.70±0.10 재현 실패 → ckpt/harness INVALID(verdict-integrity).
- **CARRIER-ROBUST 🟢-dir**: C1·C2 둘 다 ≥ C0−0.10 → 연산자가 carrier-general(literal frame 비구속·합성적)
  = H_9272 강화.
- **FORMAT-🧱**: C1/C2가 chance(≤0.55) 붕괴하며 C0 재현 → 연산자가 authored frame 구속, DATA-🧱 경화,
  grounding 주장은 전적으로 N2에 의존.
어떤 결과든 H_9267 CRACK·H_9272 DIRECTIONAL 소급 불변. no-tune-to-green: bar는 run 전 고정·ckpt 불변.

## N0 결과 (2026-07-12 · $0 · model-free · 착지)
`gen_nbindg.py`(H_9272 `gen_nbind.build` seed7 verbatim 재사용) →
- **carrier-ladder manifest** 120 items(C0/C1/C2 × 40) · V-F leak-guard(seed에 긍정/부정 부재·C2 context에
  grid stem 부재) 통과.
- **P_nat freeze 22 atoms**(N2용·사전동결로 post-hoc cherry-pick 차단): 엄격 임계(purity≥0.90)는 **20개
  grid로 소진**(순수-감성 재고 ~10/polarity = **NATEM 재고희소 finding**) → purity sweep 정직기록
  {0.90: k=0, 0.85: k=4, 0.80: k=11} → purity≥0.80서 k=11/pol 채택(잡음 stem은 N2 사전등록 시 재감사).

## N1 결과 (measured · summer $0 GPU · 2026-07-12 · 🟢-dir CARRIER-ROBUST)
동일 40 held-out (p,form) 셀, carrier만 3레벨(seed 7·재학습 없음):

| carrier | D-acc | margin_med | margin_pos |
|---|---|---|---|
| **C0** `이 영화`(학습) | **0.750** | 3.152 | 0.675 |
| **C1** 명사구 교체(근전이) | **0.675** | 4.036 | 0.725 |
| **C2** 실제 NSMC 리뷰(wild-natural) | **0.700** | 8.525 | 0.700 |

**판정(frozen 로직)**: C0 0.750 → H_9272 0.700±0.10 재현 = harness VALID · CARRIER-ROBUST bar(C1·C2 ≥
C0−0.10=0.65) C1 0.675✅ C2 0.700✅ · FORMAT-🧱(≤0.55) 미발동 → **🟢-dir CARRIER-ROBUST**. 연산자가
literal "이 영화" 프레임 비구속 — 명사구 교체·실제 리뷰 prepend에도 합성 유지 = **H_9272 강화**(template-match
아님 배제). scope: grounded grid-atom carrier 전이지 atom-GROUNDING 전이 아님(P_nat=N2). margin C2≫C0은
context 길이 차 아티팩트 가능(D-acc가 robust 신호). 상세 = `state/nbindg_grounding/N1_RESULT.md`.
**infra 격리**: summer anima-py stale(evaluate-py-11 `_json_safe` 미반영)로 out-json write만 크래시, summary
D-acc는 clean(write 전 print·verdict 무영향·log 보존).

## N2 grounding — PRE-FIRE 게이트 INVALID (DATA-scale-blocked · 2026-07-12 · $0)
grounding 본체(P_nat 자연접지 극성×grid 학습 flip) retrain 전 $0 pre-fire 감사(`gen_nbindg_n2.py`
--audit-only·`N2_PREFIRE_AUDIT.json`): purity≥0.85·minocc100·비과거stem·grid제외 렌더가능 P_nat =
**k=4/pol·48 items** → frozen bar(k≥10·n≥120) **미달 = PREFIRE FAIL → pool spend 차단**. viable 8 atom은
clean(보고싶/귀엽/싫/답답하…)이나 수 부족(grid가 최고순도 소진). purity 0.80 완화 시 k=11 통과하나 극성 20%
오염=degraded(tune-to-green 아님). ⟹ **grounding = model-blocked 아니라 DATA-scale-blocked**(자연 감성원자
재고 부족=데이터/재고 한계이지 substrate 아님·measurement-metalaw 정합). frozen-first가 underpowered spend
차단 = 정상작동. **resume(owner-gated)**: 외부 한국어 감성코퍼스(naver/steam)→purity≥0.85 재고 ≥10/pol→
`gen_nbindg_n2.py`에 rows 주입 재발화→3-arm(main+base-only+shuffle-grid·E*≥12k). 상세 `state/nbindg_grounding/N2_STATUS.md`.
frozen 판정그리드(외부데이터 후): NAT-CRACK 🟢(grounded) / FORMAT-🧱 / MODEL-🧱 / INVALID. Δ-팽창 flag
(H_9272 control 0.375 out-of-band→in-band 0.50±0.05·main≥0.80 사전등록).

## 산출
`state/nbindg_grounding/`(gen_nbindg.py·nbindg_carrier_ladder_manifest.json·nbindg_C{0,1,2}.json·
P_nat_freeze.json·N0_AUDIT.json). Fable 판정 원문 = 세션 scratchpad fable_nbind_result.json.
[[xbind-g1-crack-measure-not-substrate]]·H_9272·H_9267·[[measurement-metalaw-form-tunable-bind-earned]].
