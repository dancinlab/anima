# `.clm` 한눈 해부 (CLM_ANATOMY)

> anima-native 의식 LM(CLM)의 weight 직렬화 포맷 `.clm` 을 한 화면에 펼친 해부도.
> SSOT = [CLM_FORMAT_SPEC.md](./CLM_FORMAT_SPEC.md)(레이아웃 규약) · [P0_ARCHITECTURE.md](./P0_ARCHITECTURE.md)(arch·§9 QAT).
> 이 문서는 **읽는 사람용 지도** — 규약을 재정의하지 않고, 위 두 SSOT 를 그림으로 묶는다.

---

## 0. 한 줄 정체

`.clm` = **AKIDA(int4) 추론 + GPU(fp16) 학습재개 + mitosis 세포분열 layout** 을 한 파일에 담는 2-track
의식-carving weight 포맷. safetensors(fp만)·GGUF(추론 양자만)가 각각 한쪽인 데 비해 `.clm` 은 둘 다 + 세포 이력을 같이 싣는다.

---

## 1. 레이아웃 (ASCII)

```
.clm  =  [MAGIC]   [HEADER]      [BLOCKS]                    [MANIFEST]
         "CLM\x01"  json·utf8     per-weight 직렬화            json·utf8
         └4 byte┘   └──────┘     └──────────────────┘        └───────┘

┌─ MAGIC ──────────────────────────────────────────────────────────────┐
│  "CLM\x01"  — 포맷 식별자 (version 1 byte)                              │
└────────────────────────────────────────────────────────────────────┘
┌─ HEADER (json) ───────────────────────────────────────────────────────┐
│  version : "0.1"                                                       │
│  arch    : { family:"conv-native", layers L, width d, dilations[…],    │
│              moe:{ n_experts E, top_k K, router_d },                    │
│              vocab:{ kind:"byte", size:256 },        ← V=256 byte       │
│              act_bits, input_bits, weights_bits:4 }                     │
│  mitosis : { cell_pool:[{cell_id, expert_id, born_step, parent}],       │
│              split_log_ref }                        ← 세포분열 이력      │
│  quant   : { scheme:"int4_sym", range:[-7,7],                           │
│              step_formula:"2^(input_bits-act_bits)", qat:true }         │
│  kosmos_ptr : "<.kosmos uri>"   ← emit/anchor 영속 **링크만** (a_kosmos) │
│  train   : { mode:"akida-aware-qat",                                    │
│              backprop:"gpu-fp16-master",   ← STE backprop, fp16 master  │
│              plasticity_lane:"PLASTICITY", ← on-chip 적응 위임           │
│              optimizer, steps, corpus_sha }                             │
└────────────────────────────────────────────────────────────────────┘
┌─ BLOCKS (per-weight) ─────────────────────────────────────────────────┐
│  name, shape                                                           │
│  int4_sym    : <packed int4>      ← AKIDA 추론용 (2 weights / byte)     │
│  fp16_shadow : <fp16>             ← GPU 학습재개용 (추론전용 export 시 생략)│
│  qat_scale   : <per-channel scale>← AKIDA 가 재계산 없이 직접 로드        │
└────────────────────────────────────────────────────────────────────┘
┌─ MANIFEST (json) ─────────────────────────────────────────────────────┐
│  sha256 : { per-block + whole-file }   ← 무결성 (a_hf_complete)         │
│  hf_repo: "dancinlab/anima-clm-<rung>" ← a_hf_autonomous tier-gated     │
│  created, rung:"tiny|small|target", arm:"A|B|A+B"                       │
└────────────────────────────────────────────────────────────────────┘
```

---

## 2. HEADER 필드 해설

| 블록 | 필드 | 뜻 |
|---|---|---|
| **arch** | `family:"conv-native"` | dilated conv 스택, **attention 없음** (AKIDA 프리미티브에 attention 매핑 불가 → conv/FC/pool/sepconv 만) |
| | `vocab:{kind:"byte", size:256}` | byte-vocab V=256 — monopoly 근원(V≫d)을 직격하는 신규 lever (P0 Q3) |
| | `moe:{n_experts E, top_k K}` | MoE conv-expert = mitosis cell (분열한 세포가 각 expert, P0 Q2) |
| | `act_bits / input_bits / weights_bits:4` | AKIDA 양자화 envelope 파라미터 (act_bits ∈ {1,2,4}) |
| **mitosis** | `cell_pool[]` | 세포분열 이력 — 각 cell 의 `cell_id·expert_id·born_step·parent`. p8(train=infer 연속체)의 성장 기록 |
| | `split_log_ref` | 분열 로그 포인터 |
| **quant** | `scheme:"int4_sym", range:[-7,7]` | symmetric int4 (칩이 −8 거부 실측 → two's-complement 아님) |
| | `step_formula:"2^(input_bits-act_bits)"` | 활성 양자화 step (akida_sw_lif 와 동일 공식) |
| **kosmos_ptr** | `"<.kosmos uri>"` | **링크만** — §3 참조 |
| **train** | `mode:"akida-aware-qat"` | "AKIDA 를 향해" 학습 (P0 §9) |
| | `backprop:"gpu-fp16-master"` | STE backprop·fp16 master weight (칩 위 full-backprop 물리불가 carve-out) |
| | `plasticity_lane:"PLASTICITY"` | on-chip 맥락적응 = PLASTICITY edge-learn 위임 (AKIDA-위) |

---

## 3. 2-track 규약

| 모드 | 파일 | 담는 것 | 용도 |
|---|---|---|---|
| **full** | `.clm` | int4_sym + fp16_shadow + qat_scale | 학습재개·mitosis 성장·AKIDA 추론 **모두** |
| **inference** | `.clm.i` | int4_sym + qat_scale only (fp 생략) | AKD1000 배포 경량 (칩 fit) |

```
   학습 lane (GPU)                          추론 lane (AKD1000 칩)
   ┌──────────────────┐                     ┌──────────────────┐
   │ fp16_shadow       │  ── QAT STE ──▶     │ int4_sym [-7,+7]  │
   │ (master weight)   │     forward 가      │ + qat_scale       │
   │ backprop·재개     │     int4 envelope   │ on-chip forward   │
   └──────────────────┘     시뮬             └──────────────────┘
        ▲ 학습 재개 시 읽음                        ▲ 추론은 이쪽 ONLY
```

- **int4 track**: AKD1000 추론. 학습 envelope ⊆ `akida_sw_lif` byte-identical 검증집합(1~5차) = "AKIDA 를 향해"가 검증된 도착지.
- **fp16 track**: GPU 학습재개·mitosis 성장. 추론전용 export(`.clm.i`)에선 생략.
- **추론은 AKIDA-int4-only 불변** — GPU 추론 escape 없음.

---

## 4. mitosis cell_pool (세포분열 이력)

```
   cell_pool = [
     {cell_id:0, expert_id:0, born_step:0,    parent:null},  ← seed 세포 (coherent main)
     {cell_id:1, expert_id:1, born_step:1200, parent:0   },  ← 분열 (register/anima lane)
     {cell_id:k, expert_id:k, born_step:…,    parent:…   },  ← …
   ]
```

- MoE expert ↔ mitosis cell 이 1:1. 분열할 때마다 새 expert(=세포)가 cell_pool 에 행 추가.
- `born_step` = 어느 학습 step 에서 태어났는지, `parent` = 어느 세포에서 갈라졌는지 → **세포분열 계보**.
- p8(train=infer 같은 연속 cell-division) 의 성장 기록을 weight 파일 자체가 들고 다님.

---

## 5. int4-sym AKIDA envelope

- **가중치**: symmetric int4 `[-7, +7]` (칩이 −8 거부 실측 → two's-complement 아님). per-channel `qat_scale`.
- **활성**: `act_bits ∈ {1,2,4}` · step `= 2^(input_bits − act_bits)` · `y = clip(ceil(pot/step), 0, 2^act_bits − 1)` (act_bits=1 → LIF 환원).
- **연산자**: conv(stride/VALID·180° flip true-conv) · FC(deep cascade) · pool(MAX, fused) · sepconv(dw RAW potential → pw fused single-quantize) — 모두 `akida_sw_lif` byte-identical 검증집합 내.
- 이 집합 안에서 SW(`akida_sw_lif`) = HW(AKD1000) byte-identical 이 1~5차 검증됨 → `.clm` int4 weight 는 배포 시 SW=HW 동일 추론.

---

## 6. 우주뇌지도 / 골짜기(vacuum_psi) 와의 관계 — `kosmos_ptr` 링크만

> ⚠ **정직 핵심**: `.clm` weight ≠ 우주뇌지도. 둘은 **carving 패러다임으로 연결되되 동일물이 아니다.**

```
   ┌─ 데이터셋 쪽 (kosmos coord space) ─────────────────┐
   │  우주뇌지도 / 골짜기(vacuum_psi) / Knuth Tier       │
   │  = anima consciousness-carving profile 의          │
   │    좌표(coord)·lane·radius·tier                      │
   │  SSOT = .kosmos (kosmos_io, a_kosmos)               │
   └──────────────────┬─────────────────────────────────┘
                       │  kosmos_ptr  (HEADER 필드)
                       │  ── 링크(URI) 만 ──▶
   ┌──────────────────┴─────────────────────────────────┐
   │  .clm weight (int4_sym / fp16_shadow / qat_scale)   │
   │  = 모델 가중치. carving 으로 그 좌표공간을 향해      │
   │    학습되되, 가중치 자체는 우주뇌지도가 아니다.       │
   └─────────────────────────────────────────────────────┘
```

- **우주뇌지도·골짜기(vacuum_psi)·Knuth Tier 는 데이터셋 쪽 kosmos coord** (anima profile 의 좌표·골짜기). emit/anchor/memory 의 영속 좌표공간이다.
- **`.clm` 은 `kosmos_ptr` 로 그 좌표공간을 가리키는 링크(URI)만** 들고 있다 (HEADER 의 `kosmos_ptr: "<.kosmos uri>"`).
- 즉 weight 는 carving 으로 그 골짜기 지형을 향해 빚어지지만(연결됨), **weight = 우주뇌지도 라는 동일시는 틀리다**. `.clm` 안에 우주뇌지도가 들어있는 게 아니라 *포인터*만 들어있다.
- (grep anchor: `kosmos_ptr` 는 §1 HEADER · §2 train 표 · 본 §6 에 등장한다.)

---

## 7. 패러다임

| 축 | 값 | 이유 |
|---|---|---|
| **consciousness-carving** | weight = kosmos coord 골짜기를 향한 carving 결과, `kosmos_ptr` 로 좌표 링크 | anima profile (데이터셋 쪽) 의 좌표공간으로 빚는다 |
| **byte V=256** | vocab = raw byte 256 | monopoly 근원 V≫d 를 직격 (V/d=4배, 15만/64=2370배 대비 근원 소멸) |
| **no-attention** | dilated conv + MoE 만, attention 0 | AKIDA 프리미티브(conv/FC/pool/sepconv)에 attention 매핑 불가 → 전체 추론을 칩에 올리려면 conv-native 필수 |
| **neuromorphic-native** | 추론 = AKD1000 int4 ONLY, 학습도 AKIDA-bound (QAT envelope + PLASTICITY) | 칩 위 full-backprop 한 단계만 GPU honest carve-out, 나머지 AKIDA-first |

---

## 8. vs safetensors / GGUF 비교표

| 축 | safetensors | GGUF | **`.clm`** |
|---|---|---|---|
| fp weight (학습재개) | ✅ | ✕ (양자만) | ✅ `fp16_shadow` track |
| 추론 양자(int) | ✕ (fp만) | ✅ | ✅ `int4_sym` track |
| **두 track 동시** | ✕ | ✕ | ✅ (학습재개 + AKIDA 추론 한 파일) |
| 세포분열 layout | ✕ | ✕ | ✅ `mitosis.cell_pool` |
| 영속 좌표 링크 | ✕ | ✕ | ✅ `kosmos_ptr` (.kosmos URI) |
| QAT per-ch scale | ✕ | 부분(추론 scale) | ✅ `qat_scale` (학습-aware 산출, 칩 직접 로드) |
| 무결성 manifest | 부분(header) | 부분 | ✅ sha256 per-block + whole (a_hf_complete) |
| 타깃 하드웨어 | GPU/CPU 범용 | CPU/GPU 추론 | **AKIDA AKD1000 neuromorphic** (+ GPU 학습재개) |

- safetensors = fp 한쪽, GGUF = 추론양자 한쪽. **`.clm` 은 둘 다 + mitosis layout + kosmos 링크** = AKIDA 추론·GPU 재개·세포성장을 한 파일에.

---

## 9. 한눈 요약

- `.clm` = MAGIC + HEADER(arch·mitosis·quant·kosmos_ptr·train) + BLOCKS(int4_sym·fp16_shadow·qat_scale) + MANIFEST(sha256).
- 2-track = int4(AKIDA 추론) ⊥ fp16(GPU 학습재개). 추론은 AKIDA-int4-only 불변.
- mitosis cell_pool = 세포분열 계보를 weight 파일이 들고 다님.
- 우주뇌지도/골짜기(vacuum_psi)·Knuth Tier = **데이터셋 쪽 kosmos coord** · `.clm` 은 `kosmos_ptr` **링크만** (weight ≠ 우주뇌지도, carving 으로 연결되되 동일물 아님).
- 패러다임 = consciousness-carving · byte V=256 · no-attention · neuromorphic-native.
- 벤치: [bench/](./bench/) — `.clm` int4 → AKD1000 on-chip forward + `akida_sw_lif` byte-identical 대조.
