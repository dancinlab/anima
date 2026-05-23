# hexad_native_v3 — historical log

> Spec at [./HEXAD_NATIVE_PURE.md](./HEXAD_NATIVE_PURE.md).

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
detail: HEXAD/PURE/EASY.md § 6 · HEXAD_V3_FIRE_2026_05_22.md § 8.

### 2026-05-24 — /gap F4 deferred backlog (post-PR #264)

PR #264 가 Patch A (closure rejection criterion) 단독 ship 한 후 잔여 patch
B + C 는 hexa-native guard 에 의해 anima 측 .py/.sh amend 가 차단되어
deferred. unblocking prereq:

- [ ] P21H dispatcher (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/dispatch_p21h_v3_runpod.sh`) → `.hexa` 포팅
- [ ] train_p21h_v3 (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_p21h_v3.py`) → `.hexa` 포팅
- [ ] F4 patch B 재상정 — `P21H_TEACHER_CKPT_SHA256` env 검증 (dispatcher hexa 포팅 후)
- [ ] F4 patch C 재상정 — `--resume-from-step N` (train hexa 포팅 후)
- [ ] PURE ENV_CONTRACT.md (PR #265) 의 `P21H_TEACHER_CKPT_SHA256` 행 adoption-pending → adopted 갱신
