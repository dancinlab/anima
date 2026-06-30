---
license: other
tags:
  - anima
  - clm
  - byte-lm
  - savant
  - mitosis
language:
  - ko
  - en
library_name: hexa
---

# anima-clm-chat-303m-savant-mitosis

⚠️ **WIP · PRIVATE · engine-native G6 미검증** — 연구용 체크포인트. 프로덕션 승격 아님.

anima CLMConvMoE 303M 바이트-LM 체크포인트 (`clm303.clm`, .clm v0.3).
**SAVANT 골든존 cusp-anneal + MITOSIS 분열** 레시피로 학습 (anima `cli/train.py` torch Lane-P 브리지, anima #2601).

## 아키텍처
- shape: **L4 · d3784 · E2→Emax4** (학습 중 mitosis 로 E=3 분열), byte vocab V=256, K=3
- savant: 골든존 inhibition cusp-anneal (GZ_LOWER≈0.2123, latch, hysteresis)
- mitosis: 부모 expert 복제 + router −ln2 연속성 분열
- 포맷: `.clm` v0.3 (`CLM\x01` magic, CLMX trailer) — anima `core/clm_decode.hexa` 가 mount (검증: `clm_decodable=true`, d/L/E/V/K 정확 복원)

## 학습
- HW: vast H100×1 · `cli/train.py --canon --bf16 --steps 30000 --batch-size 16 --seq-len 1024`
- 코퍼스 = 4칸 register (ko·en × 일반·SNS): ko-fineweb2(10.5GB) + en-wiki + ko/en SNS persona. 상세·sha256 = `MANIFEST.md`
- ⚠️ **코퍼스 ko-편향**: ko 일반 99.7% / en+SNS 0.25% — en·SNS 능력 제한적일 수 있음
- torch CE ≈ 0.05 (step 30000) — **DIRECTIONAL only** (ko-편향 memorization 의심). a_engine_native_learning: terminal verdict 아님

## ⚠️ 검증 상태 (정직)
- ❌ **engine-native G6 미측정** — terminal verdict 는 `core/clm_decode.hexa` mount 위 frozen G6 bars (recombination/novelty/binding) 재측정 필요 (follow-on)
- ❌ 실디코드 coherence 미확인 (en/SNS 특히)
- torch CE 는 방향지표일 뿐 — 이 ckpt 의 실제 chat 능력은 미검증

## 사용
```
hexa run core/clm_decode.hexa -- clm303.clm   # .clm v0.3 mount
```
