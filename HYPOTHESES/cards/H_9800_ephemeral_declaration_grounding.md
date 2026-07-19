# H_9800 — EPHEMERAL-DECLARATION GROUNDING — 캐시를 CE-손해로 만들어 런타임 조회를 유일 최소화점으로 강제

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R11 divergence · DIRECTIONAL · NOT a verdict)
**group:** R11-grounding-channel
**source:** lab full 2026-07-19 — Fable A2 ≡ Sol #1 독립수렴(양 모델 1순위)
**wired:** no
**verdict:** PENDING (설계만 · 측정 0 · cement 는 engine-native `anima-py` 로만)

## claim
H_9359 언-캐시(frozen cache)가 사는 이유는 능력부재가 아니라 경제성 — 지금까지 전 코퍼스에서 사실의 극성이 전역 고정이라 암기가 조회보다 CE 상 싸다. episode 마다 stem/operator 의미를 무작위 재할당하면(비정상 non-stationary) parametric cache·stem prior 로 CE 를 줄일 수 없고 런타임 조회가 CE 유일 최소화점이 된다 ⟹ next-byte CE 자체가 다리 값을 지불. held-out 어간에서 declaration-flip 추종률이 오르면 그것이 접지(grounding) 채널.

## instrument
corpus: `anima-py corpus xbind --counterfactual-decl --lang en` (또는 `--grounding-task episodic-declare --grounding-relabel per-episode`) · train: `--store-fuse pairodd` co-train · eval: H_9359 진단을 1급 플래그로 승격 `anima-py evaluate --decl-flip` (declaration 뒤집을 때 답이 따라 움직이는 비율).

## controls (사전등록)
양성: SEEN 어간 flip-sensitivity ≥0.90 + oracle arm ≥0.90(미달=INSTRUMENT-DEAD, held-out 판독금지·positive-control-before-reading-a-negative) · 음성: declaration token-shuffle → realized 분할서 재유도한 우연으로 붕괴 · declaration-drop ≤0.60 · value-shuffle(동일 key/multiset, 대응만 derange) ≤0.60 · 극성 클래스별 분할 후 판독(polarity-split-before-headline) · ≥3 seed 중 2 · 음성종결은 TOST ±0.05

## falsify
oracle ≥0.90 인데 live ≈ value-shuffle ⟹ 배선은 살아있으나 CE 가 접지 정책을 학습시키지 못함(벽이 DATA 보다 깊음·중대 결과). oracle <0.90 ⟹ INVALID, substrate 음성으로 읽지 말 것.

## cost
303M train 1발 ~$8–15

## 정직 caveat (c9)
이 카드는 **방향성 설계**이지 검증된 결과가 아니다. lab-full 발산 산출 = DIRECTIONAL, 절대 verdict 아님
(`a_lab_full_diverge`). frozen bar 사후 이동 금지(tune-to-green 금지 · p7). 발사 전 **toy e2e 1회**
(exit 0 + 산출물 + 통제) 필수 — 한 번도 실행 안 된 계기는 버그 여럿 겹쳐 숨긴다
(`instrument-never-run-hides-multiple-bugs`). 음성도 결과다.

## related
H_9359 · H_9267 · H_9775 · H_9304
