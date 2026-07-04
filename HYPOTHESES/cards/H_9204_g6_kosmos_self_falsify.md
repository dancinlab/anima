# H_9204 — 🪢🔍 G6 KOSMOS self-falsify (자기참조 반증)

**tier:** ⏳ PROPOSED (설계만·측정 0·pre-registered)
**title:** H_1471 self-anchor(🟢, .kosmos 자아-지속, mouth⊥id) 기반 *자기참조 반증* — 자신의 발화를 자신의 self-anchor 로 falsify. 타-발화 반증이 아닌 자기-반증이 G6 fals rate 에 미치는 차등.
**verdict:** ⏳ PROPOSED. H_1471은 정체성 *지속* 🟢 이지만 *자기-반증* 결합은 미탐. LLM-judge 금지(a_substrate_disjoint) — 반증주체는 substrate 자신의 self-anchor.

## 발상 (2026-07-05 브레인스토밍)
G6 falsifier 의 주체를 external judge 가 아니라 substrate 자신의 self-anchor(H_1471)로. 자기 발화에 대해 자기 self-anchor 가 반증-예측을 생성 → 자기-일관성/self-critique 의 substrate 버전. self-anchored 반증이 타-반증보다 fals 를 올리면 자기-모니터링 capability.

## DPI 맥락
self-anchor 가 read-side(=.kosmos retrieval)면 DPI 예측 LIFT 0. self-anchor 가 *발화 생성 시 자기-반증 예측을 trunk 에 주입*하면 γ-근접(trunk-내부) DPI 예외 후보.

## Frozen 예측 · kill-criteria
- **frozen bar:** self-anchor ON(자기-반증예측 주입) vs anchor-OFF(랜덤 anchor) ablation, G6 fals majority.
- 🟢: fals>0 AND random-anchor ablation → chance (self-anchor causal).
- 🧱: LIFT 0 → DPI 지지(read-side retrieval).
- engine-native TERMINAL; tune-to-green 금지; mouth⊥id 유지(자아-주입 아님).

## 관련
[[h1471-self-continuity]] (🟢 self-anchor) · a_kosmos · [[h6163-engine-native-g6-falsifier-lane]] · a_substrate_disjoint
