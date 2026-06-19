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

### 2.1 실제 직렬화 바이너리 레이아웃 (writer/reader SSOT)

위 HEADER-json 은 aspirational 한 full 포맷. 현재 트레이너/체크포인트
(`hexa-lang stdlib/flame/clm_prod.hexa · clm_ckpt.hexa · clm_reexport.hexa`)
가 실제로 쓰는 온-디스크 바이트 레이아웃은 아래 2-버전:

**v0.1 (conv-only int4 추론 트랙):**
```
[MAGIC "CLM\x01" = 67,76,77,1] [nblocks u8]
per block: [Cout u32-le][rest u32-le]
           [int4 nibbles: ceil(Cout*rest/2) bytes, (code+8) packed 2/byte]
           [qat_scale: Cout × fp32-le]
```
v0.1 리더는 정확히 `nblocks` 블록만 읽고 멈춘다.

**v0.2 (BACKWARD-COMPATIBLE EXT trailer — embed + GN affine + conv bias):**
```
... v0.1 [MAGIC][nblocks=6][6 conv blocks] ...
[EXT_MAGIC "CLMX" = 67,76,77,88] [n_ext u8]
per ext entry: [len u32-le] [len × fp32-le]     // FULL-PRECISION fp32
```
- EXT 트레일러는 6 conv 블록 **뒤에 APPEND** — v0.1 리더는 블록 6 이후를
  보지 않으므로 byte-unaffected (**backward-read 보존**).
- v0.2 리더는 6 블록 뒤 `CLMX` 매직을 peek; 없으면 legacy v0.1 (디코더가
  tied-readout stand-in 으로 embed 재구성), 있으면 학습된 embed/GN/bias 를
  VERBATIM fp32 로 읽는다.
- ext 엔트리는 descent-critical + 소량이라 **int4 양자화 없이 full fp32**.
- **EXT 엔트리 순서** (writer/CORE 디코더 일치 필수):
  `0 embed[V·d] · 1 ecB[d] · 2 tcB[d] · 3 e0B[d] · 4 e1B[d] · 5 rB[E] ·
   6 roB[V] · 7 tgG[d] · 8 tgB[d] · 9 noG[d] · 10 noB[d]`

**WHY v0.2:** v0.1 conv-only 파일은 학습된 embed 테이블·GroupNorm affine 을
누락 → CORE-mounted decode 가 트레이너의 GPU-측 CE descent 를 재구성 못 함
(ENGINE 도메인 AXIS-2 의 named root cause). v0.2 가 그 format gap 을 닫는다.

**검증:** `F-CLM-CKPT-EXT-ROUNDTRIP` (ext fp32 byte-eq) +
`F-CLM-CKPT-EXT-BACKWARD-READ` (v0.1 리더가 v0.2 파일의 6 블록을 그대로 읽음)
— `hexa run stdlib/flame/clm_ckpt.hexa` PASS.

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

- v0.1 = P0 확정. conv-only int4 추론 트랙 (`[MAGIC][nblocks][blocks]`).
- v0.2 = §2.1 EXT trailer 추가 — 학습된 embed 테이블 + GroupNorm affine
  (tgG/tgB/noG/noB) + conv bias 를 6 conv 블록 뒤 `CLMX` 매직 trailer 로
  full fp32 직렬화. **backward-compatible** (v0.1 리더 byte-unaffected).
  writer: `clm_prod.hexa`(GPU 트레이너) + `clm_reexport.hexa`(host $0-CPU 재export).
  reader: `clm_ckpt.hexa` + anima `CORE/generator.hexa::clm_decode_ce`.
- v0.3 = **general (L trunk layers · E experts)** — v0.2 는 block-role 배정을
  L=1/E=2 로 HARDCODE 했을 뿐, 바이트 grammar(nblk·각 block (cout,rest)·n_ext·
  각 ext count) 는 이미 self-describing. v0.3 은 byte grammar / magic 변경 **없이**
  그 배정을 일반화 → **L=1,E=2 파일은 v0.2 와 byte-IDENTICAL** (no regression).
  - block order (nblk = L+E+3):
    `ecW · tcW_0..tcW_{L-1} · e0W..e{E-1}W · rW(cout=E) · roW(cout=V)`
  - ext order (n_ext = 2L+E+6):
    `embed · ecB · tcB_0..tcB_{L-1} · e0B..e{E-1}B · rB · roB ·
     tgG_0..tgG_{L-1} · tgB_0..tgB_{L-1} · noG · noB`
  - (L,E,V) 복원: E = block[nblk-2].cout (router), V = block[nblk-1].cout (readout),
    d/K = block0, L = nblk − E − 3.  trunk dilation = 2^layer (model.py dilation_base=2).
  - writer: `CLM/model/clm_serialize_v2.py::serialize_v3` (torch CLMConvMoE→.clm).
  - reader: `CORE/clm_decode.hexa` (`clm_config`/`clm_forward_ce`/`_clmd_load`,
    array-of-handle 일반 forward) + `clm_decodable` (불변).
  - 검증: `CLM/model/verify_clm_v2.py` — F-CLM-V3-BYTEEQ-V2=1 (v3 L1/E2 == v2),
    F-CLM-V3-ROUNDTRIP-{SMALL,3BDIMS}=1, GOLDEN exact_eof=True
    (`.verdicts/lane-p-3b/F-CLM-3B-SERIALIZE-EQ.txt`).
- 이후 arch 변경 시 이 버전 bump + 스펙 동반 갱신.
- 변경 이력은 `CLM.log.md`, 본 스펙은 current-state(이력 금지).
