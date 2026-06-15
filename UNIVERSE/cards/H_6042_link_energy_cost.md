---
id: H_6042
tier: ⊗ (깊은 물리적 정초)
label: ⊗-42
title: ⊗-42 링크 에너지 비용 — 합성이 LINK 단독보다 에너지가 싼가. 공유씨앗 init가 cold-start 보정 버스트를 제거 → BOTH는 정상 drift 보정만 지불. 단 절약 3%로 미미.
tradition: 결합 일(work) · 소산 · ANU QRNG(paid)
status_grade: 🟢 SUPPORTED-but-MARGINAL (numerical · paid ANU-seeded)
verification_method: 결합 일 Σ|K sinΔθ|·|dθ| 누적, SEED/LINK/BOTH 비교, 3 trial; p7 $0
since: 2026-06-15
sister: H_6036, H_6010, H_6037
verdict: 🟢 SUPPORTED(미미) — work SEED 0 / LINK 24.94 / BOTH 24.07; 공유씨앗 init가 절약하는 cold-start 에너지 = 0.86(LINK의 3%). 두 채널은 열역학적 상보(공짜 공통원인 + 최소 라이브 일)지만 절약폭은 작다 — drift 정상보정 일이 cold-start 일을 압도하기 때문. 정직: 절약 미미.
---

# H_6042 — ⊗-42 링크 에너지 비용

> **가설.** 합성은 LINK 단독보다 에너지가 싸다(공유씨앗이 cold-start 일을 절약).

발견: 부호는 맞지만(BOTH<LINK) 절약 3%로 미미. work=|결합토크|·|dθ| proxy(Landauer kT 단위 아님), 2-osc 토이. `TENSION-LINK/harness/h6042_link_energy_cost.py`, verdict `.verdicts/6042_link_energy_cost/H_6042.txt`.
