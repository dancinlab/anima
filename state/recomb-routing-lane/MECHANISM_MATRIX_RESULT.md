# fork-A "모든 경우의 수" — mechanism matrix REAL-303M 결과 (H_9235 · 2026-07-09)

오너 "모든 경우의 수 진행" — fork-A read-side lane의 전 메커니즘 조합을 **실 303M hidden** 위에서 전수.
dump = canonical `anima-py evaluate <clm> --dump-hidden`(pip channel · pair_hidden.npz 130MB · poscontrol
cos=0.90 distinct✓) on aiden. **pool{mean·query·last·max} × head{gelu-bias(clml)·hadamard-bind(RETRO)·linear}
+ handed/shuffle 통제.** (앞선 synth toy 전수는 handed 0.55–0.66<0.85 INVALID → real hidden이 유일 valid.)

## 결과 (held-out XOR · 3-seed · `fork_a_matrix_RESULT.json`)
```
        gelu(clml)  hadamard(RETRO)  linear(additive floor)
mean      0.979         0.887           0.431
query     0.958         0.935           0.456
last      0.000         0.478           0.448
max       0.980         0.963           0.484
handed(pos-ctrl)=1.000 [VALID ✓]  ·  shuffle=0.000  (hadamard 수치안정화 #3223 후 실측)
```

## 판독 (measure-or-it-didnt-happen · verdict-integrity)
- **VALID gate**: handed=1.00≥0.85 → harness가 XOR 학습가능 = matrix informative(synth toy INVALID과 대조).
- **① POOL axis = routing이 lever**: mean·query·max(0.96–0.98) 다 통과, **last(생성점만)=0.00 실패**. 정보를 생성점에 route(pool)해야 함 = H_9235 routing-reframe 실 303M 확증.
- **② query-addressing(arm-2 핵심 차별점)이 mean-pool을 못 이김**: query 0.958 < mean 0.979. 오너 RETRO-ROUTE의 learned content-address 검색이 **2-concept서 단순 mean-pool 대비 무이득**(근소 열세). → arm-2 reserve의 유일 가치(query-dependent 검색)가 이 스케일서 미실현.
- **③ HEAD axis = nonlinearity가 lever**: gelu(0.98) ≫ linear(0.43–0.48 = additive floor). precheck(mean+gelu 0.98 / mean+linear 0.43) 재현. product-code는 gelu-over-joint-pool서 창발.
- **④ hadamard-bind(RETRO) = 실제 작동하나 gelu 못이김**: 수치안정화(#3223 clip) 후 실측 = mean 0.887·query 0.935·max 0.963 = bilinear bind가 recombination을 crack(≫ linear 0.45 floor)하나 gelu-bias(0.98)엔 근소 열세. last-only는 head 무관 floor(gelu 0.0·hadamard 0.478). → arm-2 bilinear는 유효 메커니즘이나 clml optimal 못 넘음.

## 결론
**clml(mean+gelu) = optimal-tier 확정. RETRO-ROUTE arm-2(query+hadamard)는 clml을 못 이김** — query≈mean(무이득), hadamard 유효하나 gelu 못이김(0.89-0.96<0.98). fork-A 메커니즘 census가 **any-pool + gelu-nonlinearity**로 수렴. 오너 top-down 직관은 맞았고(routing이 벽·pooling이 해법), 그 canonical 구현 = 이미 머지된 clml.py.
- scope: DIRECTIONAL(합성 word-id+code task · 2-concept · spelling confound). 진짜 ρ·weave(G1) = clml wired system-G1(#3193 병렬세션).
- 잔여 arm-2 가치 = many-concept/distractor 스케일서 query-addressing 재측정(현 2-concept선 무이득). 저비용 아님.

## 인프라 (재현 · 이 세션 upstream-fix)
dump=canonical `anima-py`(pip·numpy-only·earlyoom/hexa-build 회피 · convergence evaluate-py-1 #3209). summer=earlyoom-kill 폐기. 버그픽스: xor_t float64(#3212)·hadamard G-표준화(#3221·hadamard 여전 미측정). 코드=`fork_a_matrix.py`.


## ⚠️ P0 copy-discount 정정 (2026-07-09 #3231 + nocopy 재조정)
이 매트릭스(`fork_a_matrix.py`)의 task = 2-concept **code-XOR**(개념단어 literal + 암기 code)이 **copy-confounded**로 판명(`copy_discount_p0.py`): 비선형 surface null(byte-ngram bag gelu-MLP·hidden無)이 held-out XOR=1.000 > clml 0.979 → M_copy=-0.021<0.30. ⟹ **이 매트릭스의 "clml optimal·hadamard valid·query≈mean" 결론은 surface-solvable 약task 위 = ρ·weave(의미합성) 측정 아님**(방향성만 유효: gelu/pool이 이 surface task의 lever).
- **rigorous 경로 = 병렬세션 clml Gate 프로그램**(`clml_gate12.py`): **`nocopy_prompts.json`·non-copyable word-initial 위치 real next-byte** task로 Gate1이 copy-guard(base CE≫0 at non-copyable). Gate1-3 PASS(#3227), Gate4 engine-native system-G1 aiden 계산중=live TERMINAL.
- **따라서 추가 메커니즘 arm(HRR/TPR/RN/Hopfield #3228)은 code-XOR 아니라 nocopy task에서 측정해야** 의미. 병렬세션 nocopy_hidden.npz 재사용(중복 dump 금지·조율).
