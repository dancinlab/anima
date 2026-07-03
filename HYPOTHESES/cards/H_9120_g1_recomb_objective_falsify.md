# H_9120 — G1 recomb-objective (L4) FALSIFY — objective-floor terminal

> **tier:** 🧱 FALSIFY (numpy A.novel=0) → **DIRECTIONAL-TERMINAL** (Fable 벽돌파 재프레임: objective-floor 위장, 진짜 = architecture-floor) · **wired:** N/A (verdict, GREEN 아님)
> **slug:** `g1_gamma_objective` · **date:** 2026-07-04

## 가설
G1 재조합 벽이 학습 *objective* 문제라면, trunk 학습에 novel-composition 보상 aux loss(recomb-objective)를 넣으면 mouth가 composed novel-only를 max_single 위로 올릴 것이다(objective가 재조합 basin을 켠다). L3 MOUTHFLOOR(H_9118)가 "정보 접근≠binding"으로 격리한 벽을, 학습신호로 여는 마지막 미측정 축.

## 방법 (numpy --py canonical)
- **ckpt**: `recomb_s7.bin`(303M ByteGPT, L4 recomb-objective 학습 — novel keyword 조합 보상 + distractor 억제 aux loss) vs `trunk_baseline.bin`(CE-baseline). 로컬 `~/anima-weights/g1_gamma/`.
- **decode**: gen=40, top_k=40, temp=0.7, seed_rng=7+s(singles)/7(composed). A(recomb-trunk: composed + SCRAMBLE control + wrong-D control), B(baseline).
- **채점**: `exp1_g1.py score` FROZEN G1 grow-window (composed_distinct novel≥2 ∧ >max_single ∧ kwr≥0.5, novel=seed에 없던 continuation keyword).
- **측정 경로**: **numpy `anima evaluate --py`**(`a_eval_py_canonical`, py 2-production = engine-native TERMINAL-eligible). 처음엔 own-GEMM engine decode로 시도했으나 scalar-glue-bound(bg_forward_last_W window-slide fallback)으로 느려 --py canonical로 전환. **torch 교차검증 진행중**(a5413c4b, pool, DIRECTIONAL 보강).

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

## artifacts
- `state/g1_gamma_objective/` (verdict + out-files)
- `scratchpad/exp1/EXP1_VERDICT.txt`, `exp1_g1.py`
- ckpt: `~/anima-weights/g1_gamma/{recomb_s7,trunk_baseline,gamma0_s7}.bin` (303M 각 1.2GB)
