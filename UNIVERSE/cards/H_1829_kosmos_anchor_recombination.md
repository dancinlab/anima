# H_1829 — kosmos anchor-space 재조합 (N4)

**id:** H_1829
**slug:** kosmos_anchor_recombination
**tier:** 🔵 PROPOSAL (anima-native novel lever · 고갈 brainstorm 산출 · HE pre-screen gated)
**date:** 2026-06-30
**source:** UNIVERSE (anima-native novel 레버 고갈 brainstorm)
**렌즈:** `a_kosmos` (placement 공간) · `a_no_llm_frame_trap` · `break-walls`
**wired:** PROPOSAL (미배선·미측정) — H_1821 HE 사전선별 먼저, 통과분만 engine-native

---

## 가설

재조합 = `.kosmos` **placement 공간**(coord/lane/radius)에서 두 부모 anchor로부터 **학습된 비-중점(non-midpoint) 좌표**를 구성하는 것이다. anchor 공간은 VAdaptField(면역 lane L2-Voronoi)와 **다른 좌표계** — profile-바인딩된 placement geometry이고, self-continuous(`.kosmos`로 세션 넘어 영속).

**미사용 격리:** H_1822/1825는 VAdaptField *면역 lane*에서만 측정했다. kosmos **placement-space**에서의 구성적 재조합(coord 산술이 아니라 profile-학습된 좌표 construct)은 미측정.

## Design

1. 2부모 → 각 kosmos anchor(coord vec · lane · radius · profile).
2. **학습된 constructor** g(coord1, coord2, profile)→child_coord (midpoint 아님; placement profile에서 학습).
3. child anchor를 kosmos_io→brain_decide로 영속, substrate-G1 측정.
4. controls: **midpoint baseline**(단순 평균) · single · shuffle · parent-specificity.

## Frozen bar (pre-register · p7)

| 항목 | bar |
|------|-----|
| 구성 anchor G1 | composed_distinct≥2 ∧ >midpoint-baseline ∧ parent-specific, ≥2/3 → 🟢 / floor → 🧱 |
| 좌표계 직교 | VAdaptField 측정(H_1822)과 발산하면 placement-space가 다른 결과 = 직교 |

⚠️ 정직: midpoint baseline이 핵심 control — child가 단순 중점이면 "구성" 아님(H_1310 Voronoi depth-0 회귀). HE 사전선별 통과 시 engine-native(`core/` kosmos_io).
