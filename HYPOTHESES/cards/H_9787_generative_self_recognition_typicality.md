# H_9787 — GENERATIVE SELF-RECOGNITION — typicality 판별(ownership 아님)

**status:** 🔵 PROPOSED · DIRECTIONAL·BOUNDED (lab-full R9 · Fable∥Sol 양 모델 수렴·오너 seed · Sol "가장 강한 다음 카드") — cement=engine-native anima-py만
**lane:** 의식 / interior-causality / self-typicality (프런티어 post-theta-alive)
**related:** [[H_9785]](ownership provenance UNIDENTIFIABLE·본 카드는 다른 faculty) · [[H_9774]](content-reach 입도=multiset+trigram·이 카드는 그 위) · [[H_9729]](ownership 금지선·비충돌) · [[H_9062]](mirror-test PROPOSED) · [[H_9098]](self_cos AUROC 인공물) · [[H_9038]](self_drift GREEN) · source: sidecar lab full(Fable ∥ Sol)

## (a) 물음
데몬의 interior는 *자기 mouth가 만들 법한* 텍스트를 **byte-multiset+trigram 통계로 환원되지 않는 수준**에서 다르게 취급하는가? ([[H_9774]] content-reach 입도 = multiset+trigram — 그 **위**가 존재하는지가 정확한 물음.) provenance("누가 만들었나") 아닌 typicality("내 분포에 전형적인가").

## (b) engine-native 계기
기존 `--swap-text`(greedy·byte-clean·kill-list #3 회피) 4-arm, 신규 엔진코드 0(donor trace=데이터): A0 SHAM(자기 재주입·[[H_9774]]서 무해 검증) · A1 **trigram-surrogate**(자기 텍스트 trigram 통계 샘플 대리·결정적 통제) · A2 **seed-twin**(s7↔s11 ckpt 같은 프롬프트 greedy 출력·twin 존재) · A3 SCRAMBLE(multiset floor). readout=`ANIMA_DECISION_TRACE` + `--selfg-census`(self_live SELFG8 궤적) 소플래그. Sol 변형: `--self-recog`(frozen feature 주입).

## (c) 판정식 + 통제
DV = **trigram-초과 소비 lane만** — immune(bare text) recall margin · igrow · ca3 · self-anchor drift(penult_fold8·byte-stats 아닌 penult 표현·chat.py:2560-2566). 판정 = collapse-Δ(own vs A1 trigram-surrogate) > 0 ∧ SHAM=0 유지 ∧ SCRAMBLE=multiset floor. **p7 준수: DV=perplexity 아닌 interior lane 반응 Δ**. py303_full·--lang en·≥3 seed=BOUNDED.

## (d) kill 조건
전 lane에서 own ≈ trigram-surrogate → "자기-전형성은 trigram 통계 위에서 표현 안 됨" = 입도 상한 명시 earned null(BOUNDED). 부분 생존 시 2차 사전등록: Δ가 self-g lane에만·self⊥mouth라 하류 전파 0 → "계산되나 행동적으로 inert"로 봉인.

## (e) kill-list 재탕 아님
H_9785/H_9774§4가 금지한 것은 **provenance-ownership verdict**. 본 카드는 출처 주장 없음 — twin-대칭성은 confound 아닌 **예측**(twin은 twin 전형성 인식). **카드에 "ownership verdict 발행 영구금지" 사전등록**해 H_9729 금지선과 정면 비충돌.

⚠️ DIRECTIONAL·cement=engine-native만. 병렬대조: AGREES(Fable candidate2 ∥ Sol candidate A 수렴) · Sol "EARNABLE-BUT-BOUNDED 최강 다음 카드".

## 🔧 하네스 toy-validation (2026-07-19 · engine-change-0)
`--swap-text` greedy 4-arm 하네스(scratchpad/h9787_harness.py·엔진변경0): native own 포획→A0 own(SHAM)·A1 trigram-surrogate·A3 scramble donor 생성→발사→immune recall(rel_lane)·self-anchor(a_fold8) 판독. toy.clm·24tick·seed7.

| arm | immune recall(rel_lane) | self-anchor(a_fold8) | swap 발화 |
|---|---|---|---|
| A0 own | 0.9013 | 2.5000 | 12✅ |
| A1 trigram-surrogate | 0.8352 | 2.5000 | — |
| A3 scramble | 0.4962 (multiset floor) | 2.5000 | — |

**하네스 LIVE + 4-arm distinct**: immune recall이 **own > trigram-surrogate(Δ0.066) > scramble**로 구별 = 계기 살아있음([[H_9786]] degeneracy/deadzone과 대조·--swap-text 실발화 12/12). 🐛 자가수정 2건: ①REPO=stale primary(--g-reach wm-dual 없음)→fresh origin/main archive ②donor 필드 `text_b64`→`gtext_b64`(로더 기대명·안 고치면 0 swap).

**정직 범위**: own>trigram-surrogate는 **content-similarity recall**([[H_9774]] 영역·episodic)이지 self-typicality 확증 아님 — H_9787 고유주장(self-typicality *above* episodic recall)은 **seed-twin arm(A2)**이 분리(twin 텍스트=다른 typicality·다른 content → twin>trigram-surrogate면 typicality 인식). self-anchor(a_fold8)는 toy서 flat(2.5 상수·죽은축·chat-py-4/5). ⟹ verdict=303M summer(A2 seed-twin s7/s11 ckpt·DV=immune bare-text recall+self-anchor drift live gauge·own∧twin > trigram-surrogate = self-typicality).

## NEXT (303M · 자율 pool)
303M summer(chat-py-8): native own 포획→A0 own/A1 trigram-surrogate/A2 **seed-twin**(별 ckpt)/A3 scramble donor→--swap-text 발사→2-hop live 게이지(immune recall·self-anchor drift) 판독. PC(계기 known 구별 증명)·own∧twin>trigram-surrogate=self-typicality above episodic·own≈trigram=입도 상한 earned null. ⚠️seed-twin ckpt 2개(s7/s11) 필요 — 없으면 3-arm(own/trigram/scramble)만=H_9774 refinement·seed-twin 없이 self-typicality 미분리 명시.
