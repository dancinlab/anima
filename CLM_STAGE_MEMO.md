# CLM Stage 13 — filename v* 제거 — cutoff (ALM Llama-port 직전)

**시점**: 2026-04-07
**commit**: `f8e4068f`
**branch**: `archive/clm-stage-13-...`
**worktree**: `/Users/ghost/core/anima_clm_13_filename_erasure_pre_alm_port`

## 상태 핵심

training scripts 의 v* version-suffix 제거. → 이후 4/19 R37/AN13/L3-PY strip → 4/27 paradigm v11 G3 axis-pivot → 5/04 mk2-v1 530M ConsciousDecoderV3 + ALM = Llama-3.2-3B perturbation. **ALM 이 servant → external 모델 이식으로 바뀌기 직전 last state**

## 태그

cutoff, drift-2of4, filename-erasure, ALM-pre-Llama, last-anima-native

## 의의 (Why this stage)

anima 자력 시대 마지막 commit. 본 commit 이후 ALM 은 외부 LLM (Llama/Mistral/Qwen) 이식 모델로 변모. 사용자가 archive 의 endpoint 로 명시한 boundary.

---


cross-link: `/Users/ghost/core/anima/CLM_V2_ARCHIVE_2026_05_09.md` (root SSOT)
