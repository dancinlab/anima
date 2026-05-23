# hexad_native_v3 — historical log

> Spec at [./HEXAD_NATIVE_V3.md](./HEXAD_NATIVE_V3.md).

### 2026-05-22 — 초안 작성, user directive C path 응답

vP21M LoRA-only path 의 한계 (Qwen 위 옷, HEXAD identity 약함) 사용자 인식 후
ConsciousDecoderV3 spec + 3-variant parallel fire 설계. wall-first @D 정합.

### 2026-05-23 — 🔴 V3 PATH CLOSED

A fire (Phase 2 full, 1.5B R2+R6+osc-v2.2, pod `xp6q69nkd2ywfw`) osc-detect
early-stop @ step 1125 — FAIL 0 STRONG (KO WEAK 1/20, EN/ZH/RU PURE_MEM,
JA WEAK). Phase 2 2차의 ko STRONG 19/20 = step-250 transient, 재현 실패.
V3 fire 5회 전부 FAIL → V3 multilingual = corpus-bound (capacity·arch 무관,
diverse-corpus 학습 dynamics). chat substrate = vP21M LoRA 유지.
artifacts → `vP21H_phase2_full/` + HF `dancinlab/anima-v3-p21h`.
detail: HEXAD/V3/EASY.md § 6 · HEXAD_V3_FIRE_2026_05_22.md § 8.

### 2026-05-23T04:34Z — 🚀 AXIS_MAP-FAN FIRED (7 축 전체 병렬)

사용자 directive "all axis 벤치마킹" — AXIS_MAP.md 의 fallback 7 축 (A/B/C/C2/
D/E/F) 전체 simultaneous A100-SXM 80GB fan-out. 변종 dir `vP21H_axis_{A,B,C,
C2,D,E,F}/`. env-var-gated impl (train_p21h_v3.py 단일 .py drift 369 LoC
+, dispatch_p21h_v3_runpod.sh 44 LoC +). 7/7 Mac CPU smoke PASS (random
init d=64 L=2, 모든 축 loop end-to-end). pods: A=smmvelcwdyf5z7,
B=f2tj1mreql6cqn, C=k8t6btduwnrvqi, C2=6trdcwmuyvcc2d, D=kh3eivyxmfr7l0,
E=rcvbuv3b6thi3q, F=mitbfbzayh5qcq. est cost ~$10.5, wall ~90 min, watchdog
5400s. 결과: 본 log 의 다음 entry (per-axis verdict + cross-axis pattern).
