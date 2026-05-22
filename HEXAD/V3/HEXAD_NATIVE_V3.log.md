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
