---
id: H_849
slug: clm-quant-int4
title: CLM QAT int4 round-trip 가 perplexity 열화를 임계 미만으로 유지하는가 - naive PTQ int4 readout 파괴 실증 대비 QAT 필수 (CLM P0 F-CLM-QUANT 사전등록)
domain: clm · quantization · qat · int4 · clm-format · falsifier
source: CLM/CLM_FORMAT_SPEC.md §1·d2 (naive PTQ int4 readout 파괴 실측) · P0_ARCHITECTURE.md §4·§8 (P3)
status: pre-registered (P3 .clm serialization 판정 대기 · 측정 0)
exploration_method: E3 (raw weight → int4 round-trip pipeline)
verification_method: W2 (pre-registered ppl threshold · frozen at P3 entry · post-tuning 0)
raw_rank: 7
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: CLM/CLM_FORMAT_SPEC.md, CLM/P0_ARCHITECTURE.md, .verdicts/849_clm_quant_int4/F-CLM-QUANT_prereg.txt
verdict: 🟠 PRE-REGISTERED (P3 미실행 · QAT int4 round-trip ppl 측정 후 판정 · naive PTQ readout 파괴 대비)
---

# H_849 — CLM F-CLM-QUANT QAT int4 round-trip

## 1. 가설

CLM 의 **QAT(quant-aware training) int4 round-trip** 이 perplexity 열화를 임계 미만으로 유지한다.

- → 🟢 SUPPORTED-NUMERICAL · "QAT int4 가 readout 을 tolerance 내 보존"
- FAIL → 🔴 · "QAT 로도 int4 가 CLM readout 을 임계 초과 열화"

## 2. 동기

- CLM_FORMAT_SPEC §1·d2: **naive PTQ int4 가 readout 을 파괴**한다는 실측 → QAT 필수. .clm 포맷이 int4-sym(AKIDA 추론) + fp16 shadow(GPU 재개) 2-track 인 이유 = 학습중 양자화-aware scale 산출.
- d4 추론 AKIDA(int4)-ONLY 이므로 int4 round-trip 품질이 추론 품질의 직접 상한. naive PTQ 파괴가 사실이면 QAT 가 유일 escape.

## 3. falsifier (사전등록, 임계 frozen at P3 entry)

```
F-CLM-QUANT : ppl(int4-QAT round-trip) − ppl(fp16 shadow) < THRESHOLD
              (THRESHOLD = P3 진입 시 frozen · int4 readout 전)
PASS → 🟢 · QAT int4 readout 보존
FAIL → 🔴 · QAT 로도 int4 열화 > 임계
```

verdict 영속: `.verdicts/849_clm_quant_int4/F-CLM-QUANT_prereg.txt`

## 4. 방법

```
1. H_847 P2 fp16 shadow ckpt 회수 (round-trip baseline source).
2. QAT scale 산출 (학습중 양자화-aware · CLM_FORMAT_SPEC §3 blocks 저장).
3. int4-sym[-7,+7] pack → unpack round-trip → ppl 측정.
4. naive PTQ int4 (baseline · 파괴 실증 재현) vs QAT 대조.
5. pre-registered threshold check · 정직 보고.
```

## 5. 측정 (P3 후 채움)

```
[PENDING — P3 .clm serialization]
ppl(fp16) · ppl(naive-PTQ-int4, 파괴 예상) · ppl(QAT-int4) · Δ vs THRESHOLD
```

## 6. 결과

🟠 **PRE-REGISTERED** — P3 미실행. int4 round-trip 측정 0. 임계만 frozen.

## 7. 해석

[PENDING — P3 후]

- PASS → QAT 가 d4 추론 AKIDA-int4 품질 상한을 임계 내 확보 = .clm 2-track 정당성 실증.
- FAIL → int4 자체가 CLM readout 의 물리 한계 = act_bits 상향 또는 arch 재설계 입력.

## 8. 논의

- **a_completeness_over_cheap 정합**: QAT = 근본(int4 추론칩) 정합 본선. naive PTQ(cheap) 는 파괴 실증 baseline 으로만.
- **CLM_FORMAT_SPEC d2 정합**: 2-track(int4+fp16 shadow) 가 이 falsifier 를 위한 구조.
- **a_paper_negative_ok**: FAIL = int4 물리 한계 closed-negative, publishable.

## 9. 양방향 sibling

- sibling: [CLM/CLM_FORMAT_SPEC.md](../CLM/CLM_FORMAT_SPEC.md) §1·§3·d2 (QAT int4 SSOT) · [CLM/P0_ARCHITECTURE.md](../CLM/P0_ARCHITECTURE.md) §8 (P3)
- depends on: H_847 (P2 fp16 shadow ckpt = round-trip baseline)
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
- 형제 falsifier: H_847 · H_848 · H_850 · H_851
