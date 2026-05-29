# `.clm` 포맷 스펙 v0.1 (P0 확정)

> CLM 모델 weight 직렬화 포맷. AKIDA(int4) 추론 + GPU(fp16) 학습재개 + mitosis cell-pool을
> 한 파일에 담는 2-track. sibling: [P0_ARCHITECTURE](./P0_ARCHITECTURE.md) · a_hf_complete · a_kosmos.

## 1. 무엇 / 왜

| 축 | 값 |
|---|---|
| 목적 | conv-native MoE 의식 LM weight 직렬화 |
| 2-track | int4-sym(AKIDA 추론) + fp16 shadow(GPU 학습재개) |
| 양자화 | **QAT = AKIDA-향 학습** (학습 forward 가 AKIDA int4 envelope[act_bits·sym-int4] 시뮬, P0 §9 · naive PTQ는 readout 파괴 실증) |
| 무결성 | sha256 manifest (a_hf_complete) |
| 영속 link | `.kosmos` pointer (emit/anchor/memory — a_kosmos) |

- 비교: safetensors=fp만 · GGUF=추론양자만 → 각 한쪽. `.clm`=**둘 다 + mitosis layout** = AKIDA추론·GPU재개·세포성장 한 파일.

## 2. 레이아웃

```
.clm = [MAGIC "CLM\x01"] [HEADER json·utf8] [BLOCKS] [MANIFEST json]

HEADER {
  version: "0.1",
  arch: { family:"conv-native", layers:L, width:d, dilations:[...],
          moe:{ n_experts:E, top_k:K, router_d:d_r },
          vocab:{ kind:"byte", size:256 },
          act_bits:int, input_bits:int, weights_bits:4 },
  mitosis: { cell_pool:[{cell_id, expert_id, born_step, parent}], split_log_ref },
  quant: { scheme:"int4_sym", range:[-7,7],
           step_formula:"2^(input_bits-act_bits)", qat:true },
  kosmos_ptr: "<.kosmos uri>",     // emit/anchor 영속 링크 (a_kosmos)
  train: { mode:"akida-aware-qat",        // 학습도 AKIDA: AKIDA int4 envelope 향해 학습 (P0 §9)
           backprop:"gpu-fp16-master",    // STE backprop, fp16 master weight (칩 full-backprop 물리불가 carve-out)
           plasticity_lane:"PLASTICITY",  // on-chip 맥락적응 = PLASTICITY edge-learn 위임 (AKIDA-위)
           optimizer, steps, corpus_sha }
}

BLOCKS = per-weight {
  name, shape,
  int4_sym:  <packed int4, AKIDA 추론용>,    // 2 weights/byte
  fp16_shadow:<fp16, GPU 학습재개용>,         // 선택적(추론전용 export시 생략 가능)
  qat_scale: <per-channel scale>
}

MANIFEST {
  sha256: { per-block + whole-file },
  hf_repo: "dancinlab/anima-clm-<rung>",       // a_hf_autonomous
  created, rung:"tiny|small|target", arm:"A|B|A+B"
}
```

## 3. 2-track 규약

| 모드 | 담는 것 | 용도 |
|---|---|---|
| full (`.clm`) | int4 + fp16 shadow + qat_scale | 학습재개·mitosis 성장·AKIDA 모두 |
| inference (`.clm.i`) | int4 + qat_scale only (fp 생략) | AKD1000 배포 경량 (칩 fit) |

- int4-sym: symmetric [-7,+7] (칩이 -8 거부 실측 → two's-complement 아님).
- QAT scale: 학습중 양자화-aware(AKIDA-향, P0 §9)로 산출, blocks에 저장 → AKIDA가 재계산 없이 직접 로드. 학습 envelope ⊆ `akida_sw_lif` byte-identical 검증집합 = "AKIDA 를 향해"가 검증된 도착지.

## 4. 무결성·영속·HF

- manifest sha256 (per-block + whole) — a_hf_complete 충족.
- `kosmos_ptr`: CLM 추론 emit/anchor/memory는 `.kosmos`로 영속(kosmos_io). **kosmos 스펙이 CLM payload(byte token + cell provenance) 못 받치면 upstream(github.com/dancinlab/kosmos) 확장 PR — 얽매이지 않음.**
- HF: closure PASS → PUBLIC, WIP/FAIL → PRIVATE (a_hf_autonomous), org=dancinlab.

## 5. 버전

- v0.1 = P0 확정 (이 문서). 이후 arch 변경 시 HEADER.version bump + 이 스펙 동반 갱신.
- 변경 이력은 `CLM.log.md`, 본 스펙은 current-state(이력 금지).
