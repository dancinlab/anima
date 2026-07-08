# VSA framebreak (고정 resonator read-head) — 🧱 FALSIFIED as a G1 transfer lever

**결론(2026-07-08)**: Fable framebreak 후보#1(고정 HRR/VSA bind+resonator read-path)은 **G1 재조합(transfer) 벽의 레버가 아니다.** stage-1의 operator-escape(B≫C)는 **superposition-capacity** 결과였지 held-out transfer가 아니었다. ≥3 통제 렌즈 수렴.

## 렌즈 1 — 논리 스퀴즈 (Fable, fable_falsification.md)
well-posed held-out transfer task의 목표함수 g는 150 train으로 **유일결정**돼야 함 → 두 갈래뿐:
- **① g ∈ VSA-class**: resonator 승리는 **순환**(고정 연산자는 자기 대수만 계산 — 일반화한 g는 selection상 그 대수 안). 게다가 벽 증발(bilinear/modular/group = 대표적 grokking 성공, CE transformer가 수렴 시 held-out 통과). 벽 유지하려면 tune-to-red(실격).
- **② 진짜 transfer 벽(SCAN/COGS류)**: VSA가 transformer를 이기는 건 **ground-truth role/filler 인수분해+codebook을 손에 쥐여줄 때만**(Smolensky). 그런데 G1 벽의 본질이 **"학습된 인수분해의 부재"** → 그걸 offline 제공 = rig.

## 렌즈 2 — kill-shot 통제 측정 (killshot_probe.py · aiden $0 · 3seed)
같은 superposition-partner-recall task에서 **atom 출처만** handed↔blind 교체:
| arm | atom 출처 | recall(med) |
|---|---|---|
| B_handed | clean random codebook(인수분해 공짜) | **1.000** |
| B_blind | 학습된 tiny byte-LM hidden(데이터서 유도) | **0.048** (chance 0.004) |
| C_handed | additive floor | 0.128 |
**순환성 margin(B_handed−B_blind) = 0.952.** atom을 학습표현서 유도하는 순간 HRR 붕괴.

## 렌즈 3 — atom-geometry 메커니즘 (동일 probe + stage-2 smoke)
- offdiag |cos|: handed=**0.035**(준직교, HRR 필요조건) vs blind=**0.636**(이방성 붕괴). CE 학습이 HRR 필요 quasi-직교성을 능동 파괴.
- stage-2 smoke 부합: byte-LM hidden atom으로 B in-dist=0.06·B0(random)>B(trained). random projection 못 고침(JL이 이방성 통과). 학습 encoder into frozen codebook = **γ(H_1840, trained-bind)로 붕괴** = 고정-대수 framebreak 아님.

## 함의
- stage-1 escape = **memory/interference capacity**(HRR 홈그라운드, 인수분해 공짜), **transfer 아님** — H_1835 함정(in-context/superposition 능력을 transfer 능력으로 오인)의 재판.
- 모든 수리경로가 **γ trained-constructive-bind(H_1840)로 수렴** — ledger가 이미 닫은 레버(#3108 DUP-WALLED · DPI #3046). 
- **G1 재조합벽 = 확정된 능력천장** 유지: data#3109 · E1#3107 · γ#3108 · all-axis DPI#3046 · **+ framebreak(본 카드)**. 잔여 저비용=coverage-density(GPU無)뿐.
- scope: torch/numpy DIRECTIONAL이나, 논리 스퀴즈 + 측정된 순환성(0.95) + 기하 메커니즘 = **terminal-grade 판정**(break-walls ≥3 통제렌즈).

## artifacts
- killshot_probe.py + killshot_RESULT.json (통제 측정) · stage2_probe.py (copy-confound smoke) · fable_stage2_spec.md · fable_falsification.md
