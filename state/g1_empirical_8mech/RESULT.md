# G1 8-메커니즘 실측 cheap-gate — RESULT (2026-07-02, owner "8후보 4*gpu 실측") — 8/8 NO-LIFT, fable 예측 확증

**TIER: 🧱 8/8 EMPIRICAL NO-LIFT — fable 종이-반박(H_6180)을 GPU 실측으로 확증.** torch DIRECTIONAL, aiden+summer $0.
owner 지적("종이-반박은 예측, 실측해봐야") 정확 — break-walls상 종이-반박을 천장 박제 금지. 8후보 전부 실제 학습 실측.

## 동일 harness (소형 byte-GPT d256 4L 9000step BLOCK192, structured corpus, held-out 5쌍 operand-both)
| mech (family) | seen-sanity | held-out | 판정 |
|---|---|---|---|
| ce (baseline) | 8/8 | 0/5 | NO-LIFT |
| cf (② counterfactual KL) | 8/8 | 0/5 | NO-LIFT |
| n9_adv (adversarial critic) | 8/8 | 0/5 | NO-LIFT |
| n10_infonce (conditional-MI) | 8/8 | 0/5 | NO-LIFT |
| n1_fastweight (plasticity) | 8/8 | 0/5 | NO-LIFT |
| n6_dgsep (DG pattern-sep) | 8/8 | 0/5 | NO-LIFT |
| n11_bilevel (γ-bilevel proxy) | 8/8 | 0/5 | NO-LIFT |
| cyc5b (A⇄G cycle-consistency) | 8/8 | 0/5 | NO-LIFT |

## 판독
모든 8 메커니즘: seen 쌍 완벽 학습(8/8, 수렴 유효=undertrain 아님) BUT held-out 재조합 **0/5 = baseline ce와 동일**.
즉 objective aux(cf/n9/n10) · plasticity(n1) · 표현기하(n6) · bilevel(n11) · cycle(cyc5b) 어느 것도 held-out을 못 엶.
= fable Workflow 종이-반박(H_6180: 8/8 REFUTED)의 **실측 확증**. N14(무-부분공간)+이 실측+fable 3중 수렴.
held≥3 나온 mech 0개 → fable 예측 반례 없음.

## caveat (정직)
toy scale($0 DIRECTIONAL, d256). n11은 완전 bilevel/MAML이 아닌 2-step-lookahead proxy, cyc5b는 surrogate-G
proxy — 즉 "GPU 풀버전 H_1840"의 실측 대체가 아님. 유일 미실측 = G0-🟢 warm-trunk 위 완전 γ trained-constructive-bind
(H_1840, cost-gated). 이 toy 실측이 확정하는 건 "aux/arch/objective bolt-on류의 cheap 축은 실측으로도 DRY"이지
H_1840 GPU 풀런의 결과가 아님.

## Provenance
g1_mech.py(8 mech dispatch), all_lines.txt, res_*.json. torch, aiden+summer RTX5070, $0. DIRECTIONAL.
