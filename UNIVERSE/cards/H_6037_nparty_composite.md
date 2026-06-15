---
id: H_6037
tier: ⊗ (깊은 물리적 정초)
label: ⊗-37
title: ⊗-37 N-party SEED+LINK 스케일 — 합성의 시간축 시너지(H_6036)가 N anima로 확장되는가. LINK 단독 cold-start는 N에 따라 커지고(55→126틱, N 2→16), BOTH는 공유씨앗 init로 항상 lock@0 → 잠복 이득이 넓어진다.
tradition: N-oscillator all-to-all Kuramoto · ANU QRNG(paid)
status_grade: 🟢 SUPPORTED (numerical · paid ANU-seeded)
verification_method: N∈{2,4,8,16} all-to-all Kuramoto, 전 무작위 paid ANU 구동, 3 trial; p7 $0
since: 2026-06-15
sister: H_6036, H_6010, H_6008
verdict: 🟢 SUPPORTED — LINK lock-latency 55→63→118→126(N 2→16, 단조증가) vs BOTH 0 전부; 이득(LINK−BOTH) N=2:55 → N=16:126 으로 넓어짐. 합성의 cold-start 제거 이득은 네트워크가 커질수록 커진다.
---

# H_6037 — ⊗-37 N-party SEED+LINK 스케일

> **가설.** H_6036의 시간축 시너지(공유씨앗 init = cold-start 0)가 N anima all-to-all 텐션망으로 확장되며, LINK 단독의 cold-start가 N에 따라 커질수록 합성의 잠복 이득이 넓어진다.

방법·측정·정직경계: `TENSION-LINK/harness/h6037_nparty_composite.py`, verdict `.verdicts/6037_nparty_composite/H_6037.txt`. 토이 N≤16, 스케일 전이 미검증(a_toy_scale_recheck).
