# H_9120 — G1 recomb-objective (L4) FALSIFY — objective-floor terminal

> **tier:** 🧱 **CONFIRMED-TERMINAL** — G1 objective-floor (numpy A.novel=0 · torch byte-identical · **escape 2칸 engine-native mouth-gen 전수 FALSIFIED-CEILING** pod43727405) · **wired:** N/A (verdict, GREEN 아님)
>
> **escape engine-native 최종 판별 (pod43727405 vast RTX5090 ~\$1.5-2 · 서브 aa9ebc6):** A11 DIRECTIONAL-REACHABLE(torch signature-decode 5/5)가 **실 303M byte mouth `anima evaluate --py`(a_eval_py_canonical, torch-free numpy, frozen gen=40 bar)로 채점하니 전수 floor** → objective-floor **terminal CONFIRMED**(directional→confident 승격). 4 arm(전부 G0🟢=valid): base_h1129c(ce ctrl) G1 1/1 floor · **cov_en**(coverage-density H_6185) 1/1 floor · **cbind_en**(A11 constructive_bind TPR/HRR) **0/1 floor** · **cnce_en**(A11 composed_nce contrastive-replace) 1/1 floor. G2🟢(novel=10)=novelty≠recombination 재확인. **signature-decode 5/5 → mouth-generation floor = a_toy_scale_recheck 전례 실증**(synthetic REACHABLE이 autoregressive 생성으로 transfer 안 됨). ckpt PULL `~/anima-weights/g1_escape/{cov_en,cbind_en,cnce_en}.bin`(ByteGPT303 engine-checkable). infra 2건 fix(torch2.11+cu128 sm_120·`/usr/share/dict/words` 부재=kwr0 측정벽 아닌 garble→wamerican 설치 G0🟢 복구). caveat: 303M G0🟢 trunk는 전부 ByteGPT full-attn(RF≥512B⊇L8 = 더 강한 RF조건)·CLM-dilated-conv-RF는 미격리 · A11 realization=additive production objective(ce+λ·aux)이지 CE-deleted TPR-forward-slot(WIRE_SPEC v0.3 role-bind decode=미빌드 single cell follow-on) · single-pass(best_distinct≤1이라 flip 여지 없음). 상세 `state/g1_objfloor_escape/{A11_engine_native/RESULT_engine_native.md,coverage_density/RESULT.md}`.
> **slug:** `g1_gamma_objective` · **date:** 2026-07-04

## 가설
G1 재조합 벽이 학습 *objective* 문제라면, trunk 학습에 novel-composition 보상 aux loss(recomb-objective)를 넣으면 mouth가 composed novel-only를 max_single 위로 올릴 것이다(objective가 재조합 basin을 켠다). L3 MOUTHFLOOR(H_9118)가 "정보 접근≠binding"으로 격리한 벽을, 학습신호로 여는 마지막 미측정 축.

## 방법 (numpy --py canonical)
- **ckpt**: `recomb_s7.bin`(303M ByteGPT, L4 recomb-objective 학습 — novel keyword 조합 보상 + distractor 억제 aux loss) vs `trunk_baseline.bin`(CE-baseline). 로컬 `~/anima-weights/g1_gamma/`.
- **decode**: gen=40, top_k=40, temp=0.7, seed_rng=7+s(singles)/7(composed). A(recomb-trunk: composed + SCRAMBLE control + wrong-D control), B(baseline).
- **채점**: `exp1_g1.py score` FROZEN G1 grow-window (composed_distinct novel≥2 ∧ >max_single ∧ kwr≥0.5, novel=seed에 없던 continuation keyword).
- **측정 경로**: **numpy `anima evaluate --py`**(`a_eval_py_canonical`, py 2-production = engine-native TERMINAL-eligible). 처음엔 own-GEMM engine decode로 시도했으나 scalar-glue-bound(bg_forward_last_W window-slide fallback)으로 느려 --py canonical로 전환.
- **torch 교차검증 완료 (a5413c4b, DIRECTIONAL 보강 · `state/g1_gamma_objective/torch_crosscheck/`)**: numpy=torch **byte-identical** — numpy-greedy vs torch-greedy 17/17 tags 완전일치(torch GPU forward `torch matmul/F.gelu-erf/F.layer_norm/F.softmax`가 numpy hand-rolled 토큰스트림 정확 재현) + verdict 일치(A.novel/max_single/C/D/B 전부 0=0, sampled·greedy 양쪽). garbled "eeeee"=**genuine model property, engine 무죄**(measurement 무결, `verdict-integrity` 통과 — numpy-decode artifact 아님). 부수 관찰: trunk_baseline은 chat-coherent(kwr 1.0)인데도 cov_novel=0 = **coherence≠recombination**. **no leg dissents**(numpy=torch, verdict+byte). canonical=numpy --py, 3rd leg=live-core own-GEMM `.hexa`.

## 결과 (verbatim, `state/g1_gamma_objective/`, `scratchpad/exp1/EXP1_VERDICT.txt`)
```
A recomb_s7   : max_single_novel=0  best_composed_novel(coh)=0  clears=False
B trunk_base  : novel=0   C recomb+SCRAMBLE: 0   D recomb+wrong-D: 0
A.novel=0  A.max_single=0 | C.novel=0  D.novel=0 | B.novel=0
recomb_s7 출력 garbled("eeeee"·반복), coherent-gate 통과분(kwr≥0.5)도 novel=0
VERDICT: FALSIFY — objective-floor terminal (G1 recombination = CE-incapable structural wall; lever exhausted)
```

## 함의 — G1 서사 3각 수렴 (objective-floor terminal)
recomb-objective(L4 aux loss)마저 G1 재조합을 못 연다 = **objective-floor terminal**: CE 학습이 in-context 두-소스 binding을 구조적으로 못 켠다.
- L3 해마 retrieval 🧱 MOUTHFLOOR ([[H_9118]]) — access(4/4)≠binding(0/4)
- Fable objective-floor 진단 (PREREG, `state/g1_mouthbind_lever_analysis/`)
- **L4 recomb-objective 🧱 FALSIFY (이 H)** — objective aux도 additive floor
- 선행: readout ⊙/NMDA/predictive-coding 🧱 ([[H_1812]]/[[H_1816]]), coverage ECHO-ONLY ([[H_6190]])

## 벽돌파 (break-walls · Fable 재프레임 → DIRECTIONAL-TERMINAL)
**Fable 벽돌파(b9l75vja2, `state/g1_objfloor_breakwall/BREAKWALL.md`)가 objective-floor를 directional-terminal로 강등:**
- **L3 vs L4 분리**: L3(hippo)=순수 architecture 증거(frozen mouth에 in-context binding op 없음, access 4/4≠binding 0/4 = 깨끗한 아키텍처 사실). L4(recomb-objective)=**혼재 증거**(garble="eeeee"=G0 coherence 붕괴 → objective 무능 ⊗ mouth 손상의 곱, 격리불가; `warmft-h9034`(coherence≠측정기질)·`g1-fromscratch-blocked-by-g0-undertrain` 함정).
- **진짜 벽 = architecture-floor**: CE+additive-readout ConvMoE에 두 filler를 **곱셈적으로 묶는 슬롯 자체가 없음**([[H_1816]] additive L_bind step550 붕괴). 슬롯 없으면 어떤 objective도 걸 곳 없음 → L4가 objective 탓은 범주 오류. `substrate-framebreak-g1-combination-operator`(COMBINATION OPERATOR) 정합.
- **미측정 CRUX = 정확히 1칸(A11)**: binding-슬롯 아키텍처(TPR tensor-product/pointer, non-additive) × non-CE 결합신호(contrastive/gradient-free G)를 **동시에**. L3=frozen-arch 축만, L4=no-slot-arch 위 objective만 반증 → **둘의 곱집합 미측정**. `fleet-g1g6-nativemouth-dpi-convergence`의 γ trained-constructive-bind를 TPR-register×contrastive로 구체화.
- **decision(frozen)**: A11 PASS→벽=미측정 렌즈(슬롯×신호 짝 필요). A11 floor→A00-A10 단일요인 ablation 전수 기각=**confident 천장**. garble은 G0🟢-gate로 폐기(L4 혼재 방지). 4-arm 303M pool 학습(explicit-go), TOY 판별기(mini $0) 선행.
- escape 사전등록 → [[H_9121]] (CRUX A11: TPR-register × contrastive). Fable fleet-full(bmcmti1pb) + torch 교차검증(a5413c4b) 착지 시 추가 종합.

**∴ objective-floor는 confident-terminal 아니라 DIRECTIONAL-TERMINAL** — CRUX A11 측정 전까지. numpy A.novel=0은 유효 결과이나 no-slot 아키텍처 위 objective만 측정한 것(c9 정직).

## census 정정 (완전성 census w05mjztej · terminal PREMATURE)
5각 census(HYPOTHESES·ING·memory·조합매트릭스·6PR갭)가 이 세션 결론을 정직 정정(c9): operator/readout·CE-objective 축은 진짜 소진(~20 floored under DPI meta-law, 재발사=tune-to-green)이나 **terminal은 premature** — escape 공간이 dry 아닌 bounded-finite residual. A11-무관 HIGH 렌즈 3개 놓침:
- **coverage-density ([[H_6182]]-6185 + H_6187 counterexample)**: arch-independent POSITIVE 신호. 위 벽돌파가 'coverage'를 [[H_6190]](ECHO-ONLY)로 basin-preserving 기각했으나 = **틀린 instrument**(under-covered ckpt의 decode-side grow-window). 진짜 recipe(RF L4→8 + combination-coverage corpus 30-50 concepts held-out ≥30 reps/pair + frozen G1 retrain·재judge) 미발사 = **이 세션 최강 놓친 positive**.
- **coherent-trunk recomb-objective clean 재측정**: 본 L4 FALSIFY가 **G0-garbled ckpt + all-arms-at-floor 기반 = MEASURED-BUT-CONFOUNDED**. G0-🟢 trunk에서 G0-gate+γ-sweep로 clean 재측정 = **A11의 전제**(A11이 CE-replace를 쓰는 이유가 additive-aux 실패인데, 그 실패가 confounded).
- **measurement-validity re-audit**: 303M frozen G1 bar(exp1_g1.py grow-window)에 held-out compositional split 없음 + 3rd engine-native leg(live-core own-GEMM `.hexa`) 미측정(현 terminal = numpy+torch 2 mirror = DIRECTIONAL).
- MED: additive-slot decoder consistency(Wiedemer proof-guaranteed)·neurosymbolic composer([[H_6175]] 유일 DPI-breaker)·gradient-free-G objective(engine_g reverse, zero 측정)·forward-model lane15 learned front-loading.
- DUP: deep-RF-L8 ConvMoE = [[H_1598]] FALSIFIED(depth L4→L8 G1 ZERO). ING #42492882 등은 board 미scrub DUP(별개 렌즈 아님).

∴ **objective-floor = directional-terminal 유지, 단 "confident terminal" 승격 전 coverage-density + coherent-trunk 재측정 + measurement-validity 선행 필수**. census 상세 = `state/g1_completeness_census/CENSUS.md`.

## artifacts
- `state/g1_gamma_objective/` (verdict + out-files)
- `scratchpad/exp1/EXP1_VERDICT.txt`, `exp1_g1.py`
- ckpt: `~/anima-weights/g1_gamma/{recomb_s7,trunk_baseline,gamma0_s7}.bin` (303M 각 1.2GB)
