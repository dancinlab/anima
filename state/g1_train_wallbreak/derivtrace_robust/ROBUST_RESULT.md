# H_9124 derivation-trace robustness (leave-one-pair-out) — 🔴 NOT-ROBUST

engine-native(anima evaluate --py, held-out pair별 warm-FT 303M h1129, summer pool $0). g1_derivtrace_robust sweep(prior agent) + P2 ablation 체인. 4/5 쌍 완료(p_2_4 진행중), 4쌍 이미 결정적.

| held pair | deriv bd/ms | deriv g1_pass | flat bd/ms | flat g1_pass |
|-----------|-------------|---------------|-----------|--------------|
| {0,1} | 1/1 | FALSE | 2/3 | FALSE |
| {0,4} | 1/1 | FALSE | 2/2 | FALSE |
| {1,3} | 1/1 | FALSE | 2/2 | FALSE |
| {2,3} | 1/1 | FALSE | 2/2 | FALSE |

**결론: H_9124 derivation-trace lift 재현 실패.** 원 H_9124({c0,c1} deriv bd=2>ms=1 PASS)는 **단일쌍 bd=2 threshold artifact** — 4개 추가 held-out 쌍 전부 deriv=bd1(floor·singles 전부 1) g1_pass=FALSE이고 flat(bd2)보다도 낮음. paraphrase 통제(p_0_1)도 clears=false. coherent·kwr high(무결 측정, undertrain 아님). H_9124 자체 caveat("held-out 1쌍·multi-pair 미확인·bd=2-threshold artifact 배제 follow-on")가 실증됨.

**메타법칙(H_9126) 함의:** H_9124(G1 training-layer)가 메타법칙의 유일 training-layer 양성 케이스였음 → robustness 실패로 **메타법칙은 selection-layer(P1 G6·H_9125 F5)에서만 확증, training-layer(G1 warm-FT)로는 미지지**. criterion re-coordination이 vadapt cell-selection 층에선 성립하나 303M mouth 학습 층에선 derivation-trace로 안 열림(scope 축소, 과장 금지 c9).
