---
id: H_848
slug: clm-akida-map
title: CLM P0 추론 path 연산자가 AKD1000 byte-identical op envelope 에 포함되는가 - conv/FC/sepconv/maxpool/int4-quantizer ⊆ envelope (🔵) + MoE router softmax/topK argmax 는 envelope 밖 (정직 gap) (F-CLM-AKIDA-MAP)
domain: clm · akida · conv-native · op-envelope · structural-subset · falsifier
source: CLM/P0_ARCHITECTURE.md §0·§2 · HEXAD/CHAT/server/akida_sw_lif.py (HW-byte-identical envelope) · AKIDA/HW_SW_WIRING_2026_05_29.md (H_672 live 8/8) · CLM_FORMAT_SPEC.md §2
status: 🔵 partial (conv/FC/sepconv/pool/int4 subset SUPPORTED-FORMAL · router softmax/argmax = 정직 gap · P0 구조검증 완료)
exploration_method: E3 (op-by-op 구조 대조) · 실 silicon-verified envelope 대조 (assertion 아님)
verification_method: W2 (structural subset check + step-formula numerical probe · g5 verbatim)
raw_rank: 8
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: CLM/P0_ARCHITECTURE.md, HEXAD/CHAT/server/akida_sw_lif.py, UNIVERSE/H_672, .verdicts/848_clm_akida_map/F-CLM-AKIDA-MAP_structural.txt
verdict: 🔵 SUPPORTED-FORMAL (conv/FC/sepconv/maxpool/int4-quantizer subset byte-identical ⊆ envelope) ⚠ HONEST-GAP (MoE router softmax + top-K argmax gating 은 verified envelope 밖 — fake full-PASS 0)
---

# H_848 — CLM F-CLM-AKIDA-MAP 추론 op envelope 포함

## 1. 가설

CLM P0 추론 path 의 모든 연산자가 AKD1000 의 **byte-identical 검증 op envelope** (conv/FC/sepconv/pool · int4-sym · step=2^(input_bits-act_bits)) 에 포함된다(⊆). 포함 시:

- → 🔵 SUPPORTED-FORMAL · "전체 추론이 AKIDA 온칩 가능 (d4 추론 AKIDA-only 정합)"

포함 안 되는 연산자가 있으면:

- → ⚠ HONEST GAP · 어느 op 가 envelope 밖인지 정직 보고 (fake full-PASS 금지)

## 2. 동기

- CLM P0 d4 = **추론 AKIDA(int4) ONLY** · 학습 GPU(fp16). attention 을 안 쓰는 이유 = AKIDA 프리미티브(conv/FC/pool/sepconv) 에 attention 매핑 불가 (P0 §2 honest). transformer 썼으면 추론이 GPU 로 새서 d4 위반.
- 따라서 conv-native(Q1) 가 추론 전체를 칩에 올리는 필수 조건. 이 falsifier 는 그 전제 자체를 P0 시점에 구조검증 (assertion 아닌 실 envelope 대조).
- envelope = HEXAD/CHAT/server/akida_sw_lif.py 가 HW-SW calibration loop 에서 실 AKD1000 대비 BYTE-IDENTICAL (max Hamming 0) 로 복원 + 검증한 op 집합.

## 3. falsifier (P0 구조검증, now)

```
F-CLM-AKIDA-MAP : CLM 추론 path 의 각 op ∈ {conv2d, fc, sepconv2d, maxpool,
                  int4-sym quantizer(step=2^(ib-ab))} HW-byte-identical envelope
PASS  → 🔵 SUPPORTED-FORMAL (전체 추론 ⊆ envelope)
GAP   → ⚠ 정직 보고 (어느 op 가 밖인지 · resolution path)
```

## 4. 방법

```
1. CLM 추론 path op 열거 (P0 §0): dilated conv embed → dilated conv trunk →
   MoE router(softmax + topK) → conv-expert → [pool] → readout(FC) → next byte.
2. AKD1000 envelope 열거 (akida_sw_lif.py): fc_/conv2d_/sepconv2d_/pool2d_
   quantized_forward + cascade_forward, 전부 max-Hamming-0 silicon-verified.
3. op-by-op 대조 (subset check) · envelope grep {softmax,exp,argmax,...}.
4. step=2^(input_bits-act_bits) envelope invariant 수치 probe (akmap_step_probe.hexa).
5. 정직 verdict (포함 subset = 🔵 · 밖 op = gap).
```

## 5. 측정 (verbatim → `.verdicts/848_clm_akida_map/F-CLM-AKIDA-MAP_structural.txt`)

```
$ ./akmap_probe
step_ib4_ab4=1   step_ib4_ab2=4   step_ib4_ab1=8   ENVELOPE_STEP_FORMULA_MATCH=true
```

step=2^(input_bits-act_bits) 가 silicon 복원값(act_bits 4→1, 2→4, 1→8 = lif comparator) 재현. fc/conv2d/sepconv2d/pool2d quantized_forward 공유 quantizer.

## 6. 결과

### op-by-op 매핑 (CLM → AKIDA)

| CLM 추론 op | AKIDA envelope primitive | 상태 |
|---|---|---|
| dilated conv embed | conv2d_quantized_forward | ⊆ ✅ byte-identical (SAME/VALID · stride{1,2}) |
| dilated conv trunk | conv2d_quantized_forward (chain) | ⊆ ✅ true-conv flip=True (180° silicon 복원) |
| conv-expert (MoE body) | conv2d / sepconv2d_quantized_forward | ⊆ ✅ sepconv FUSED single-quantizer (10/10) |
| [spatial pool] | pool2d_quantized_forward (max) | ⊆ ✅ max byte-identical · ⚠ average=CLOSED-NEG |
| readout (FC → next byte) | fc_quantized_forward | ⊆ ✅ 80/80 probe max Hamming 0 |
| deep N-layer 합성 | cascade_forward | ⊆ ✅ L∈{3,4} no depth drift |
| int4 quant + act_bits | step=2^(ib-ab) | ⊆ ✅ probe MATCH=true · int4-sym[-7,+7] |
| **MoE router softmax** | (none) | ⊠ **envelope 밖 = GAP** |
| **MoE top-K argmax/gating** | (none) | ⊠ **envelope 밖 = GAP** |

**verdict: 🔵 SUPPORTED-FORMAL (conv/FC/sepconv/maxpool/int4 subset) ⚠ HONEST-GAP (router softmax + topK argmax)**

## 7. 해석

검증된 AKD1000 envelope 에는 signed-int matmul + ReLU clip + ceil-div quantizer + max-pool + 180° true-conv 만 존재. {softmax, exp, argmax, sigmoid, tanh, normalize, divide-by-sum, gating} grep = 0 (silicon 복원 없음).

- conv trunk + conv/sepconv expert + max-pool + byte readout(FC) + int4 quantizer = **형식적으로 envelope ⊆** → 그 subset 에 대해 🔵.
- MoE router 의 softmax 정규화 + top-K argmax gating multiply = envelope 밖. 따라서 bare falsifier ("전체 추론 path ⊆ envelope") 는 **clean PASS 아님** = 정직 gap.

**fake full-PASS 발행 안 함** (p7 · g5 · g63 · a_blue_closed honest residual).

### resolution path (기록, asserted-as-done 아님)

- (a) **ARGMAX-ONLY HARD ROUTING**: softmax 제거 · router FC logit 의 argmax 로 라우팅(int comparator = envelope 내 >thr compare). top-1 hard routing 시 전체 path ⊆ envelope. (P0 §1 이미 "hard top-K" 명시 — argmax top-1 이 in-envelope case.)
- (b) **OFF-CHIP ROUTER**: softmax gate 를 host 에서 계산 · 선택된 expert id 만 칩에 stream. heavy conv-body 는 d4(추론 AKIDA-only) 유지 · router 는 tiny host op. 정직: "100% 온칩" 은 아님.

## 8. 논의

- **a_blue_closed 정합**: 검증된 subset 만 🔵 · honest residual(router) 을 🔵 로 force 안 함.
- **p7/g5/g63 정합**: envelope 출력 verbatim · LLM judge 0 · gap 은닉 0.
- **d4 정합**: conv-body 추론 AKIDA-only 는 (a)/(b) 어느 쪽이든 유지. router 만 정직 분리.
- **H_672 정합**: live AKD1000 8/8 on-chip checks + R0~R4 byte-identical (seed=187) = envelope HW-confirmed 토대.
- **a_completeness_over_cheap 정합**: bare falsifier 를 cheap 하게 fake-PASS 하지 않고 router gap 을 정직 기록 + 본선 resolution(argmax-hard) 명시.

## 9. 양방향 sibling

- sibling: [CLM/P0_ARCHITECTURE.md](../CLM/P0_ARCHITECTURE.md) §0·§2 (추론 path SSOT) · [HEXAD/CHAT/server/akida_sw_lif.py](../HEXAD/CHAT/server/akida_sw_lif.py) (HW-byte-identical envelope)
- HW 토대: H_672 (AKIDA spontaneous firing live · AKIDA/HW_SW_WIRING_2026_05_29.md)
- 포맷: [CLM/CLM_FORMAT_SPEC.md](../CLM/CLM_FORMAT_SPEC.md) §2 (act_bits · int4-sym · quant scheme)
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
- 형제 falsifier: H_847 (F-CLM-MONO) · H_849 (F-CLM-QUANT) · H_850 (F-CLM-SCALE) · H_851 (F-CLM-MITOSIS)
