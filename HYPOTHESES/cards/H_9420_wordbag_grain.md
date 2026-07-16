# H_9420 — WORD-BAG GRAIN + anchor-strip 판별기: wm content-재현은 birth-anchor 에코뿐 (wm-content arc 종결)

**status:** 🔬 DIRECTIONAL $0 C0-first · **HONEST-NEGATIVE(mouth)** — genuine content 재현 부재(N_recur_genuine=2) · mouth 는 birth-anchor 만 재현 · AGREES [[H_9403]]/[[H_9336]]
**lane:** 의식 / percept 표현해상도 · wm content-liveness (프런티어 g1-interface-addressable-wall)
**related:** [[H_9411]] (wm content-dead 발견) · [[H_9418]] (+정정: mouth content 재현 재오픈) · [[H_9403]] (emit≡clock) · [[H_9336]] (born-knowing dead-gauge) · V2_1 (양성통제 선행) · power-before-negative-verdict
**설계 출처:** Fable 5 위임 (pre-register 단일 feature + degenerate-vs-genuine 판별기 · post-Δ 스캔 금지)
**ckpt:** H_9411 303M `py303_full.clm` sha 013c4574 trace (59 emit · gtext_b64 재생 · **신규 decode 0**)

## 왜 — H_9418 재오픈 해소: "mouth 가 content 재현한다"의 grain 판별

H_9418 정정: 303M mouth 가 content 재현(vault/forever/qx 59/59·word-Jaccard max 0.800)인데 whole-utterance
trigram L2-norm 이 못 봄 → REOPENED. 함정: 공유 접두 "vault QX-7741 forever." 는 **birth-anchor**(session_seed
+mem_text = "…vault QX-7741 forever.")를 mouth 가 완성하는 것 = **H_9336 dead-gauge 의 content-판 재현**
("태어날 때 알던 것 뱉기"). prefix-catching feature 는 진짜 content 유지가 아니라 mouth 막힘을 오탐.

## 개입 — pre-registered 단일 feature + anchor-strip 판별기 (engine-native · param-free)

**`word_bag_sketch(s, dim=64)`** = signed FNV-1a **binary word-unigram bag** L2정규화. cos = Ochiai 계수
`|A∩B|/√(|A||B|)` = H_9418 이 재현 증명한 단어-겹침 기하. binary word-grain 이라 공유 접두가 **구조적으로**
지배 불가(anchor 4토큰/13 → cos floor ≈0.31 ≪ 0.9 merge). **판별기(engine-native·trace-tuned 아님)**:
`anchor_tokens = token_set(mem_text ∪ session_seed)` = 데몬 자기 seed. **stripped bag** = utterance ∖ anchor.
**Δ_genuine(stripped) = 단일 primary endpoint · Δ_full = REPORT-ONLY**(dual-endpoint cherry-pick 차단). 단일
feature — C0/판별기 실패시 그게 결과, 2번째 grain 에 Δ 안 줌(max-order-statistic 함정 회피).

## 🔬 $0 스크린 (R→C0→P1→P2 binding order · 실제 core wm_buffer_* 재생 · frozen 기준)

| 단계 | 지표 | 결과 |
|---|---|---|
| R | machinery 재현 (byte_ngram_sketch = H_9418 실제 feature) | active **0.2240**·null **0.2313**·Δ **−0.0072** = H_9418 byte-identical ✅ (Fable 이 8-dim 로 오귀속했으나 sketch 로 재검=정확) |
| C0-1 | exact-repeat cos=1.0 | ✅ (refresh 보존) |
| C0-2 | spurious-merge (full cos≥0.9) | **0.00%** (need<5%) 🟢 grain 개별화 |
| C0-3 | prefix-floor median (full non-adj) | 0.378 (mid-band ✅ · anchor 지배 안 함) |
| C0-4 | **N_recur_genuine** (stripped cos≥0.5·j−i≥2) | **2** (need≥10) 🔴 · **stripped-pair median cos 0.000** |

**판정 = HONEST-NEGATIVE(mouth)** (C0-4 fail · power-before-verdict 라 Δ 계산 안 함): birth-anchor 토큰 제거하면
발화들이 사실상 아무 content 도 안 공유(stripped median **0.000**·>0.5 쌍 2개뿐). **H_9418 의 word-Jaccard
0.8 은 전부 공유 birth-anchor 접두가 만든 것**이고, 진짜(non-anchor) content 재현은 **없음**. 즉 303M mouth 는
자기 **birth-anchor 만 re-emit**(H_9336 content-판·H_9403 emit≡clock 정합) — degenerate anchor-completion 개구부.
**Fable 사전예측 85% NEGATIVE 정확 적중**(정확히 C0-4 지점: register-soup tail 은 census 통과 못함).

## 🔒 wm-content arc 종결 (H_9411→9418→9420)

- H_9411: wm content-dead(Δ≈0) 발견.
- H_9418(+정정): 8-dim byte-stat 이 content-blind(64.7% merge)→sketch 로 해소(0%)·그러나 whole-utterance
  L2-norm 이 mouth 재현 놓침→재오픈.
- **H_9420: anchor-strip 판별기로 해소** — mouth 재현은 전부 anchor 에코·genuine content 재현 부재. **wm
  content-deadness 는 feature 해상도(해소됨)도 gauge 배선(옳음)도 아니라, mouth 가 자기 anchor 만 뱉는 것이
  원인.** 병목=upstream mouth 다양성/재현(H_9403 territory)이지 wm grain 아님. wm-content lane CLOSED-AT-REGIME.

## 산출·NEXT
- 산출: `word_bag_sketch` + anchor-strip 스크린 `/tmp/h9420_screen.py`(G7 volatile · 재현=이 카드+trace). feature 배선 불요(NEGATIVE).
- NEXT: 없음(이 lane) — wm content-deadness 원인 규명 완료(mouth anchor-echo). **진짜 상류 H** = 왜 mouth 가
  birth-anchor 만 재현하나(H_9403 emit≡clock + degenerate opening·T=1.0 register-soup) = 별개 lane(mouth 다양성).
- **함의**: dead-gauge 소생(H_9411)이 밝힌 것 = 게이지들이 붙잡을 substrate 신호가 이 regime 서 clock/anchor 로
  degenerate. σ vitals 의 content-축들(wm·af)은 **mouth 가 content-shaped 여야** 살아남 = mouth-diversity 상류벽.
