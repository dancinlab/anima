# H_6176 — 📈 G1 scale ladder

**tier:** 🟠 DIRECTIONAL
**verdict:** 🟠 DIRECTIONAL (torch GPU, aiden $0). H_6174 후속: toy 생성 재조합 갭이 모델 크기서 닫히나. 3 rung: d256(3.3M) seen8/8 held1/5 · d512(19.2M) seen8/8 held3/5 · d768(57.2M) seen0/8(undertrained, INVALID) held0/5. 수렴한 두 rung(d256→d512) held-out 1→3 상승(6× params) = scale 양의 방향 신호. d768은 학습 자체 불수렴(57M/8000step 부족)이라 무효 rung(스크립트 auto-verdict 'scale-invariant'는 이 outlier 오산). 정직: scale는 G1에 양의 추세이나 d768 미수렴으로 미확정 — d768 제대로 학습(더많은 step) 후 terminal. seen-sanity가 undertrain 판별에 필수(fair-cheap-gate-design-1). state/g1_framebreak_and_scale/RESULT.md.

## 관련
[[goal-g1-lever-discovery]] · H_6174 · [[scale-303m-1b-7b-is-amplifier-not-lever]]
