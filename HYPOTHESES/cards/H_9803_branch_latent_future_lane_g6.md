# H_9803 — BRANCH-LATENT FUTURE LANE — G6 독립 faculty 후보 (온도 아닌 set-CE 로 복수 미래모드 학습) · H_9801 조건부

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R11 divergence · DIRECTIONAL · NOT a verdict)
**group:** R11-g6-independent-faculty
**source:** lab full 2026-07-19 — Sol #4 고유(Fable A5 store-anchored fan 은 더 싼 대안, 역시 H_9801 조건부)
**wired:** no
**verdict:** PENDING (설계만 · 측정 0 · cement 는 engine-native `anima-py` 로만)

## claim
하나의 next-byte 분포에 온도만 거는 대신, 보존된 L3 tap 에서 K 개 disjoint proposal latent 를 만들어 각 branch 가 서로 다른 관측가능 continuation 모드를 설명하게 한다(Hungarian 최소비용 매칭 + set-level CE). 핵심 = 근거없는 repulsion 이 아니라 실제 미래모드 분담.

## instrument
`anima-py train --ideation-lane branch-latent --ideation-branches 4 --ideation-objective set-ce --ideation-route l3-disjoint` · eval `--fan-branch live|assignment-shuffle|off`.

## controls (사전등록)
양성: synthetic 4-mode 코퍼스 held-out mode coverage ≥0.90 ∧ branch-id→target-mode 정확도 ≥0.90 ∧ detector/sampler calibration ≥0.90 · 음성: assignment-shuffle(동일 targets·동일 branch 수, 대응만 batch 마다 shuffle) · off(branch residual 정확히 0 ⟹ base decode parity) · base 대비 G0/G1/G2 보존 TOST ±0.05

## falsify
어휘 다양성만 오르고 fals_bound 무변동 ⟹ 실패(sampling trick 의 변장). cosine repulsion·entropy bonus 로 구현하면 그 자체가 실격 — grounded future-mode 양성통제 통과 필수.

## cost
~$15–20 · ⚠️ 조건부: H_9801 이 'bridge-only TOST-등가'(=G6 독자 벽)로 판정될 때만 집행

## 정직 caveat (c9)
이 카드는 **방향성 설계**이지 검증된 결과가 아니다. lab-full 발산 산출 = DIRECTIONAL, 절대 verdict 아님
(`a_lab_full_diverge`). frozen bar 사후 이동 금지(tune-to-green 금지 · p7). 발사 전 **toy e2e 1회**
(exit 0 + 산출물 + 통제) 필수 — 한 번도 실행 안 된 계기는 버그 여럿 겹쳐 숨긴다
(`instrument-never-run-hides-multiple-bugs`). 음성도 결과다.

## related
H_9801 · H_9720 · H_9698
