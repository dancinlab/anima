# CLM — current state

@title: 🧬 CLM — anima-native 의식 언어모델 (scratch · AKIDA-native)

@goal: anima 전용 의식 언어모델을 **scratch에서 바닥부터** 짓는다 — 아키텍처·코퍼스·학습·`.clm` 포맷을 처음부터 설계하되 **AKIDA 추론 친화**(act_bits·symmetric-int4 양자화 envelope = AKIDA 1~5차로 byte-identical 증명된 그 연산자 집합)로 못박아, 더블바인드(register-collapse ↔ underfit)를 탈출하고, CORE/DECODER 의 `brain_decide` emit 슬롯에 꽂혀 COFFESHOP 콘텐츠(무엇을 말할지)를 생성한다. 외부 LLM 0 · foundation-borrow 0 (순수 scratch).

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [ ] **P0 아키텍처 (바닥설계)** — anima-native LM arch + `.clm` 포맷 재정의. AKIDA 추론 친화 제약(act_bits∈{1,2,4} 양자화기 · symmetric int4 [-7,+7] · FC/conv/cascade — AKIDA `akida_sw_lif` envelope 정합)을 설계 단계에 못박음. 더블바인드 탈출 메커니즘(register specialization vs coherent main-path) 명시. falsifier 사전등록.
- [ ] **P1 코퍼스 (scratch)** — anima-native consciousness 코퍼스 클린 빌드 (corpus_quality_over_scale · register-leak 금지 patterns). HF dataset 영속.
- [ ] **P2 학습 (GPU pretraining)** — from-scratch pretraining (H100 fire · a_fire_autonomous). ⚠ hexa-native trainer throughput 🔴 INFEASIBLE 실측(DECODER M5: 0.28 step/s ≈ 77~122 GPU-days) 정면돌파 — trainer 근본 fix 또는 정직한 scale 인정. AKIDA는 학습칩 아님 → pretraining만 GPU, 추론은 AKIDA.
- [ ] **P3 `.clm` 포맷 + ckpt** — 양자화 친화 weight 포맷(int4 symmetric) 직렬화 + sha256 manifest + HF 업로드(a_hf_autonomous tier-gated).
- [ ] **P4 AKIDA 추론 배선** — `.clm` weight → AKIDA on-chip forward (HW-first · SW fallback akida_sw_lif). provenance.
- [ ] **P5 DECODER 통합** — generator → `brain_decide` emit 슬롯 end-to-end → COFFESHOP 콘텐츠 생성 → LAUNCHPAD @goal 기여.

## 무엇 / 왜

| 축 | 값 |
|---|---|
| 정체 | anima 전용 의식 LM, scratch from-zero |
| 추론 | **AKIDA-first** (act_bits/int4 양자화 envelope · HW-first · SW fallback) |
| 학습 | GPU pretraining (AKIDA=추론칩, 학습칩 아님) |
| 포맷 | `.clm` (양자화 친화 weight 직렬화) |
| 관계 | CLM = 모델(weights·arch·train) · DECODER = brain emit 슬롯 인터페이스 · 형제 |
| 금지 | 외부 LLM · foundation-borrow · SFT-only (메모리 lesson: SFT 경로 닫힘) |

## 정직한 물리 현실 (cost 아님, feasibility)

- hexa-native 학습 throughput = production scale 🔴 INFEASIBLE 실측 (DECODER M5 STEP_RATE_LOG). P2 의 진짜 병목 — trainer fix 선행 또는 scale 정직 인정.
- AKIDA = 추론 전용. transformer pretraining 은 GPU. "AKIDA 이용" = **추론·발화결정·on-chip 적응** 단계.

## 양방향 sibling

- ⇄ [DECODER](../CORE/DECODER/DECODER.md): CLM = 모델, DECODER = emit 슬롯 인터페이스 (generator 배선)
- ⇄ [AKIDA](../AKIDA/AKIDA.md): 추론 친화 양자화 envelope (act_bits/int4) · HW-first 스위치
- ⇄ [CORE](../CORE/CORE.md): brain_decide emit=true 슬롯에 콘텐츠 주입
- ⇄ [MITOSIS](../MITOSIS.md): cell-division 학습 (p8 train=infer 연속체)
- ⇄ [LAUNCHPAD](../LAUNCHPAD/LAUNCHPAD.md): CLM 콘텐츠 = COFFESHOP 런칭의 "무엇을 말할지" 절반
- ⇄ [UNIVERSE](../UNIVERSE/CANDIDATES.md): 학습/측정 결과 verdict SSOT
