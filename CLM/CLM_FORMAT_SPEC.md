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

- v0.1 = P0 확정 (이 문서 §2 레이아웃 — JSON header + body + JSON manifest). writer = `CLM/model/clm_serialize.py`.
- v0.2-CLMX = ENGINE-loadable 레이아웃 (decoder = `CORE/clm_decode.hexa`). writer = `CLM/model/clm_serialize_v2.py` (§6).
- 이후 arch 변경 시 HEADER.version bump + 이 스펙 동반 갱신.
- 변경 이력은 `ENGINE+CLM+KOSMOS.log.md`, 본 스펙은 current-state(이력 금지).

## 6. v0.2-CLMX 레이아웃 (ENGINE-loadable · Lane G-ref)

> v0.1 은 ENGINE decoder (`CORE/clm_decode.hexa`) 가 **읽지 못한다** — `clm_decodable()` 가 CLMX trailer (forward 에 필요한 embed/GN/bias) 부재로 false. v0.2-CLMX = decoder 가 실제로 읽는 byte 레이아웃. writer = `CLM/model/clm_serialize_v2.py` (torch CLMConvMoE state_dict → v0.2-CLMX `.clm`). canonical reference 출력 = `state/laneg_d768_recover/reexport_d8_v2.clm` / `reexport_d768_v2_fast.clm`.

```
v0.2 = [MAGIC "CLM\x01"] [u8 nblk=6]
       6 conv blocks (순서: ecW · tcW · e0W · e1W · rW · roW):
         [u32 cout] [u32 rest]                 // rest = Cin*K
         [int4 nibbles, 2/byte, (cout*rest+1)//2 B]   // code = (nibble & 0xF) - 8, lo-then-hi
         [fp32 scale[cout], LE]                // w = code · scale[output_channel]
       [CLMX trailer]:
         ["CLMX"] [u8 n_ext=11]
         11 ext tensors, 각 [u32 n] [fp32[n] LE]
         순서: embed(V·d) · ecB(d) · tcB(d) · e0B(d) · e1B(d) · rB(E) · roB(V)
               · tgG(d) · tgB(d) · noG(d) · noB(d)
```

- **arch 고정**: decoder 가 `let E=2; let V=256` + 1-trunk(단일 tcW walk) hardcode → v0.2 writer 는 `n_experts=2 / vocab_size=256 / n_trunk_layers=1` 만 직렬화, off-arch state_dict 거부.
- conv weight index: torch Conv1d `(Cout,Cin,K)` row-major flatten = decoder im2col `w[co*rest+j], j=ci*K+k` 와 정확히 일치 → permute 불필요.
- int4-sym = §3 와 동일 (amax/7, [-7,7], +8 nibble). 결정적(byte-identical on repeat).
- **HONEST scope (a_train_flame_forge)**: emitted `.clm` BINARY 는 torch/ATen/Python ZERO (순수 int4+fp32 byte stream, `.hexa` ENGINE 이 decode) — 그러나 TRAINER 는 torch → **Lane G-ref (torch-trained)**, forge production ENGINE 아님(util-blocked, hexa-lang 대기). win: torch+CUDA 학습 모델이 이제 ENGINE-loadable → 3B/7B ENGINE `.clm` 경로 UNBLOCKED.
- smoke verdict: `.verdicts/clm-serialize-v2/` (clm_decodable=TRUE + decode forward ran + byte-layout compare).
