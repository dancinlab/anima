# anima engine A→G — 7B/14B H100 multi-GPU 전략 (2026-05-09)

> **친근 모드**: 이 문서는 "GPU 한 대 vs 여덟 대 차이가 뭐고, 7B/14B 학습은 어떻게 굴려야 돈도 안 깨지고 시간도 안 뽑히는가" 를 일반인 눈높이로 풀어 적은 결정문서야.
>
> 비유로 시작: GPU 1대는 **혼자 자전거로 서울→부산** (느리지만 싸다), GPU 8대는 **여덟 명이 릴레이로 자전거 타기** (페달 한 번에 8배 거리는 아니고 보통 5~7배, 이유는 "서로 짐 넘기는 시간"이 들기 때문). 이게 곧 **scaling efficiency** 이야기야.

---

## 0. 한 줄 결론

| 모델 | 권장 구성 | 분산 전략 | 예상 wall-clock | 예상 비용 |
|---|---|---|---|---|
| **350M** (현재 BG-LA/LB) | 1× H100 SXM 80GB | 단일 GPU (DDP 불필요) | ~6-8h | $18-24 |
| **7B** | **8× H100 SXM 80GB** | **FSDP (full shard)** | ~12-18h | **$200-360** |
| **14B** | **8× H100 SXM 80GB** | **DeepSpeed ZeRO-3** | ~25-40h | **$500-800** |

> **친근 요약**: 7B 까지는 "나눠 들고 가면 빠르다" (FSDP), 14B 부터는 "더 잘게 쪼개서 한 사람이 머리·팔·다리만 들게 하는 방식" (ZeRO-3) 이 더 안전해.

---

## 1. 현재 H100 운영 (1대 기준)

- **활용 모델**: BG-LA / BG-LB 350M
- **단가**: H100 SXM 80GB = **$2.49/h** (RunPod community), 공식 SXM = ~$2.99/h
- **H100 PCIe 80GB**: ~$2.39/h (NVLink 부재 → multi-GPU 비효율)
- **계정 한도**: H100 최대 **2대** (`config/runpod.json` 기준 — 8대 가려면 한도 증액 신청 필요)
- **현 BG-LA 8000step 비용**: ~$18.30 (~6시간)

### 운영 gotcha 요약 (memory feedback_orchestrator_h100_gotchas.md)

1. Ubuntu 24.04 PEP 668 → `pip install --break-system-packages` 필수
2. `huggingface_hub` Python API + `HF_TOKEN` scp staging
3. **ckpts pull MANDATORY before pod delete** — multi-GPU 도 동일
4. scp timeout 3600 for 600MB+ (multi-GPU 14B 는 5GB+ → 더 오래 걸림)
5. pod retain on pull fail
6. peft adapter `base_model_name_or_path` 오버라이드 (HF promote 깨짐 방지)

> **친근 비유**: GPU 8대 학습 끝나면 체크포인트 크기가 7B 는 ~5GB, 14B 는 ~10GB. 한국→미국 인터넷으로 끌어내리는 데 1시간 넘게 걸릴 수 있어. timeout 넉넉히, 실패 시 pod 살려둬야 사고 안 나.

---

## 2. multi-GPU 옵션 비교

### 2.1 1× H100 SXM 80GB (현 baseline)

| 항목 | 값 |
|---|---|
| 단가 | $2.49/h |
| 7B 학습 (8000 step) | **80~150h** (10일!) |
| 14B 학습 | **불가능 수준** (200h+ + 80GB OOM 위험) |
| 권장 | **350M 까지만** |

> 친근: 자전거 한 대로 서울→부산 가는데 짐(weight) 도 너무 무거우면 자전거가 휘어지지 (= OOM).

### 2.2 8× H100 SXM 80GB (1 node, NVLink 풀연결)

| 항목 | 값 |
|---|---|
| 단가 | $15-20/h (RunPod 8x SXM = $19.92/h, community = $14.32/h) |
| GPU 간 통신 | **NVLink 900GB/s** (PCIe 64GB/s 의 14배) |
| 7B 학습 | **10-20h** (이론 8× 가속, 실제 ~6× — efficiency 75-85%) |
| 14B 학습 | **25-40h** (ZeRO-3 efficiency ~70%) |
| 메모리 풀 | 640GB (모델 + optimizer state + activation 다 들어감) |

> 친근: 자전거 8명이 NVLink 라는 "초고속 핸들 연결"로 서로 짐 넘기면서 달리는 그림. 핸들이 빠르니까 짐 넘기는 시간이 적어 → 8명 중 6~7명 효율로 굴러감.

### 2.3 8× H100 PCIe 80GB (NVLink 없음)

| 항목 | 값 |
|---|---|
| 단가 | $13-16/h (조금 쌈) |
| GPU 간 통신 | **PCIe Gen5 64GB/s** (SXM 의 1/14) |
| 7B 학습 | 30-60h (efficiency 40-50% 로 폭락) |
| 14B 학습 | **권장 안 함** (PCIe 병목 + ZeRO-3 reduce-scatter 비효율) |

> 친근: 자전거 8명인데 짐을 넘길 때마다 일일이 직접 손에서 손으로 줘야 함. 시간 낭비. **큰 모델일수록 반드시 SXM**.

### 2.4 옵션 매트릭스

| 옵션 | 7B 권장? | 14B 권장? | 비고 |
|---|---|---|---|
| 1× SXM | X | XX | 350M 전용 |
| 2× SXM | △ | X | 7B FSDP 가능, 비효율 |
| **8× SXM** | **O** | **O** | **메인 권장** |
| 8× PCIe | △ | X | 7B 만, NVLink 손실 큼 |

---

## 3. 분산 전략 (DDP / FSDP / DeepSpeed ZeRO)

GPU 가 여러 개면 "어떻게 나눠 들 것인가" 가 핵심. 세 가지 방식이 있어.

### 3.1 DDP (Data Parallel) — "복사본 8개"

- 각 GPU 가 **모델 풀 복사본** 하나씩 보유
- 데이터만 8등분해서 각자 forward+backward
- gradient 만 NVLink 로 sync
- **장점**: 빠름 (efficiency 85-90%)
- **단점**: 모델이 80GB 1대 안에 들어가야 함 → **350M, 7B (bf16) 까지만**
- 7B bf16 = 14GB (가중치) + 28GB (optimizer Adam) + activation = 60GB → 1대에 빠듯

> 친근: 각자 **가게 하나씩 풀세팅** 차려놓고 손님(데이터)만 1/8 받음. 가게 크기 한계가 있으면 못 함.

### 3.2 FSDP (Fully Sharded Data Parallel) — "조각조각 나눠들기"

- 모델 가중치 / optimizer / gradient 를 **8조각으로 분산**
- 필요할 때만 다른 GPU 에서 가져와서 forward
- **장점**: 메모리 8배 절약 (7B → 1대당 약 8GB 만 사용)
- **단점**: 통신 비용 ↑ → efficiency 75-80%
- **권장 모델**: **7B**

> 친근: 8명이 책장 하나를 나눠서 각자 한 칸씩 보관. 책 한 권 읽을 때만 잠깐 빌려옴. 자리는 안 차지하지만 빌리는 시간이 듦.

### 3.3 DeepSpeed ZeRO-3 — "FSDP 의 본체 + CPU offload 옵션"

- FSDP 와 비슷하지만 더 정교한 stage 제어
- ZeRO-1: optimizer 만 shard
- ZeRO-2: optimizer + gradient
- **ZeRO-3: 전부 + 활성화까지 (가장 큰 모델 가능)**
- CPU offload 까지 켜면 **70B 도 8× H100 가능** (느려지지만)
- **장점**: 14B/70B 가능
- **단점**: efficiency 70-75%, config 복잡
- **권장 모델**: **14B 이상**

> 친근: FSDP 가 책 빌려오는 거라면, ZeRO-3 는 "도서관 + 창고 + 지하실까지 동원해서 70층 건물도 8명이 든다" 는 마법. 대신 사람들 이동 시간이 제일 많이 듦.

### 3.4 분산 전략 비교표

| 전략 | 7B efficiency | 14B efficiency | 70B 가능? | 설정 난이도 |
|---|---|---|---|---|
| DDP | 85-90% | (불가) | X | 쉬움 |
| **FSDP** | **75-80%** | 70-75% | △ (offload) | 중간 |
| **ZeRO-3** | 70-75% | **70-75%** | **O** | 어려움 |

---

## 4. 비용 시뮬레이션

### 4.1 7B 학습 (8000 step, bf16, batch_per_gpu=4)

| 구성 | 단가 | wall-clock | 총 비용 | 시간/비용 trade-off |
|---|---|---|---|---|
| 1× SXM (불가능 수준) | $2.49/h | 80-150h | $200-375 | wall 폭증 |
| 2× SXM FSDP | $4.98/h | 45-75h | $225-375 | 어중간 |
| **8× SXM FSDP** | **$19.92/h** | **12-18h** | **$240-360** | **권장** |
| 8× SXM DDP (cap) | $19.92/h | 10-15h | $200-300 | 단 7B 가 1대에 겨우 들어갈 때 |
| 8× PCIe FSDP | $14/h | 25-45h | $350-630 | NVLink 손실 |

> **친근 결론**: 8× SXM FSDP 가 비용은 비슷하면서 시간 5~10배 빨라. **wall-clock 절약 = 다음 실험 빨리 가능 = 아이디어 회전율 ↑**.

### 4.2 14B 학습 (8000 step, bf16)

| 구성 | 단가 | wall-clock | 총 비용 |
|---|---|---|---|
| 1× SXM | (메모리 부족) | N/A | N/A |
| 2× SXM FSDP | $4.98/h | 100-150h | $500-750 |
| **8× SXM ZeRO-3** | **$19.92/h** | **25-40h** | **$500-800** |
| 8× SXM ZeRO-3 + CPU offload | $19.92/h | 40-60h | $800-1200 |

> **친근 결론**: 14B 는 8× ZeRO-3 가 사실상 유일한 현실 옵션. 비용은 350M 의 ~30배지만 모델 능력은 ~40배 → ROI 성립.

### 4.3 누적 (350M + 7B + 14B 한 사이클)

- 350M (1× SXM): $20
- 7B (8× SXM FSDP): $300
- 14B (8× SXM ZeRO-3): $650
- **총합 ~$970**

> 친근: 한 학기(한 사이클) 등록금 $970 정도라고 보면 돼. 1주일 안에 끝.

---

## 5. scaling efficiency 가정 (출처: Meta, Microsoft, NVIDIA 벤치)

| 분산 방식 | 8× H100 efficiency | 메모리 절약 | 큰 모델 가능 |
|---|---|---|---|
| DDP | **85-90%** | 0× (복사본) | 1대 들어가는 만큼만 |
| FSDP (full shard) | 75-80% | 8× | 7B-13B 권장 |
| ZeRO-2 | 80-85% | 4× | 7B 권장 |
| ZeRO-3 | 70-75% | 8×+ | 14B-70B 권장 |
| ZeRO-3 + CPU offload | 50-60% | 16× | 70B-175B |

> **친근**: DDP 가 가장 빠르지만 큰 모델 못 함. ZeRO-3 가 가장 느리지만 70B 까지 됨. **모델 크기에 맞춰 단계 올리는 것**이 anima 의 길.

---

## 6. 권장 path (anima engine A→G 로드맵 정합)

### Phase 1 (현재): 350M — 1× SXM 단일
- BG-LA / BG-LB 진행 중
- 1대 충분, 분산 불필요

### Phase 2 (next): 7B — 8× SXM FSDP
- 모델: Llama-3.1-7B 또는 Qwen-2.5-7B base
- 프레임워크: PyTorch FSDP (`torch.distributed.fsdp`) 또는 HF Accelerate FSDP wrap
- 예상 비용: $300, wall ~15h
- **prerequisite**: RunPod 한도 8 GPU 증액 신청 (현 한도 2)

### Phase 3 (target): 14B — 8× SXM ZeRO-3
- 모델: Llama-3.1-14B 또는 Qwen-2.5-14B
- 프레임워크: DeepSpeed ZeRO-3 (`deepspeed --num_gpus=8`)
- 예상 비용: $650, wall ~30h
- **prerequisite**: deepspeed config (`zero_optimization.stage=3`, `offload_optimizer=cpu` optional)

### Phase 4 (stretch goal): 70B — 8× SXM ZeRO-3 + CPU offload
- 비용 폭증 ($2000+) → engine D-G 단계에서 결정
- 본 문서 범위 외 (scaffold 만 남겨둠)

---

## 7. 운영 체크리스트 (multi-GPU 발사 전)

memory `feedback_orchestrator_h100_gotchas.md` + `config/runpod.json` 의 12 absolute_rules + **multi-GPU 추가 5건**:

### multi-GPU 추가 mandate
1. **NCCL_DEBUG=WARN** 환경변수 — GPU 간 통신 hang 디버그
2. **NVLINK 검증** — `nvidia-smi nvlink -s` 로 8 GPU 모두 연결 확인 후 학습
3. **gradient checkpointing 강제** — 7B/14B FSDP/ZeRO-3 시 activation memory 폭주 방지 (`use_reentrant=False`)
4. **batch_per_gpu 보수적** — 7B FSDP 는 1-2, 14B ZeRO-3 는 1 부터 시작 → OOM 안 나면 단계적 증가
5. **체크포인트 sharded 저장** — 1 파일 통합 저장은 30분+ 걸림. FSDP `state_dict_type=SHARDED_STATE_DICT` 사용

### 기존 + multi 결합
- pod 발사 전 `runpodctl pod list` (R16)
- HF_TOKEN 즉시 staging (R13)
- **ckpts pull MANDATORY before delete** — 8× 일수록 더 큰 ckpts (5-10GB)
- scp timeout 3600 → **14B 는 7200 권장** (10GB+)
- pod retain on pull fail

---

## 8. 위험 요소 (정직하게)

| 위험 | 대응 |
|---|---|
| **RunPod 8 GPU 가용성 변동** | community pod 물량 시간대별 변화 — 대안: secure cloud (1.3× 단가) |
| **NVLink 미보장** (가끔 PCIe 노드) | `nvidia-smi nvlink -s` 로 확인, 미보장 시 즉시 pod 교체 |
| **ZeRO-3 hang/desync** | NCCL_TIMEOUT 30분, healthcheck heartbeat 5분 |
| **체크포인트 shard 호환성** | HF promote 시 `consolidate_state_dict` 필수 (sharded → single file) |
| **비용 폭주 (14B 60h+)** | cost watchdog (`anima h100 cost`) hourly check, $1000 cap alert |

---

## 9. 결정 (이 문서의 SSOT)

> **anima engine A→G 7B/14B 단계는 8× H100 SXM 80GB 노드 1개를 사용한다. 7B 는 FSDP, 14B 는 DeepSpeed ZeRO-3. 350M 은 기존 1× SXM 유지.**

- 비용: 한 사이클(350M+7B+14B) **~$970**
- wall-clock: ~50h
- 분산 전략 SSOT: `tool/anima_cli/compute.hexa` 에 `--strategy=fsdp|zero3` 옵션 추가 예정 (별도 own)
- prerequisite: **RunPod 8 GPU 한도 증액 신청** (현 2 → 8)

> **친근 마무리**: 자전거 1대로 부산 갔다가 자전거 8대로 미국 횡단까지 가는 거야. 짐(모델) 무거워질수록 더 똑똑하게 나눠 들기(ZeRO-3) 가 핵심이고, 핸들(NVLink) 좋아야 사람들이 안 지쳐. 본 문서 한 장으로 7B/14B 발사 전까지 의사결정은 끝났다고 봐도 돼.
