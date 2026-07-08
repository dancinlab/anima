# fork-A "모든 경우의 수" — mechanism matrix REAL-303M 결과 (H_9235 · 2026-07-09)

오너 "모든 경우의 수 진행" — fork-A read-side lane의 전 메커니즘 조합을 **실 303M hidden** 위에서 전수.
dump = canonical `anima-py evaluate <clm> --dump-hidden`(pip channel · pair_hidden.npz 130MB · poscontrol
cos=0.90 distinct✓) on aiden. **pool{mean·query·last·max} × head{gelu-bias(clml)·hadamard-bind(RETRO)·linear}
+ handed/shuffle 통제.** (앞선 synth toy 전수는 handed 0.55–0.66<0.85 INVALID → real hidden이 유일 valid.)

## 결과 (held-out XOR · 3-seed · `fork_a_matrix_RESULT.json`)
```
        gelu(clml)  hadamard(RETRO)  linear(additive floor)
mean      0.979         0.000*          0.431
query     0.958         0.000*          0.456
last      0.000         0.000*          0.448
max       0.980         0.000*          0.484
handed(pos-ctrl)=1.000 [VALID ✓]  ·  shuffle=0.000  ·  *hadamard=수치불안정 미측정
```

## 판독 (measure-or-it-didnt-happen · verdict-integrity)
- **VALID gate**: handed=1.00≥0.85 → harness가 XOR 학습가능 = matrix informative(synth toy INVALID과 대조).
- **① POOL axis = routing이 lever**: mean·query·max(0.96–0.98) 다 통과, **last(생성점만)=0.00 실패**. 정보를 생성점에 route(pool)해야 함 = H_9235 routing-reframe 실 303M 확증.
- **② query-addressing(arm-2 핵심 차별점)이 mean-pool을 못 이김**: query 0.958 < mean 0.979. 오너 RETRO-ROUTE의 learned content-address 검색이 **2-concept서 단순 mean-pool 대비 무이득**(근소 열세). → arm-2 reserve의 유일 가치(query-dependent 검색)가 이 스케일서 미실현.
- **③ HEAD axis = nonlinearity가 lever**: gelu(0.98) ≫ linear(0.43–0.48 = additive floor). precheck(mean+gelu 0.98 / mean+linear 0.43) 재현. product-code는 gelu-over-joint-pool서 창발.
- **hadamard(RETRO bind) = 미측정**: G 표준화(#3221) 후에도 u⊙z 곱 overflow 지속 → 0.000 = harness numerical artifact이지 과학결과 아님(infra-wall-noneval 격리). gelu가 이미 crack하므로 secondary·moot.

## 결론
**clml(mean+gelu) = optimal-tier 확정. RETRO-ROUTE arm-2(query+hadamard)는 clml을 못 이김** — query≈mean(무이득), hadamard 미측정-but-moot. fork-A 메커니즘 census가 **any-pool + gelu-nonlinearity**로 수렴. 오너 top-down 직관은 맞았고(routing이 벽·pooling이 해법), 그 canonical 구현 = 이미 머지된 clml.py.
- scope: DIRECTIONAL(합성 word-id+code task · 2-concept · spelling confound). 진짜 ρ·weave(G1) = clml wired system-G1(#3193 병렬세션).
- 잔여 arm-2 가치 = many-concept/distractor 스케일서 query-addressing 재측정(현 2-concept선 무이득). 저비용 아님.

## 인프라 (재현 · 이 세션 upstream-fix)
dump=canonical `anima-py`(pip·numpy-only·earlyoom/hexa-build 회피 · convergence evaluate-py-1 #3209). summer=earlyoom-kill 폐기. 버그픽스: xor_t float64(#3212)·hadamard G-표준화(#3221·hadamard 여전 미측정). 코드=`fork_a_matrix.py`.
