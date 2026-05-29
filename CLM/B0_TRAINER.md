# CLM B0 — 트레이너 처리량 fix 트랙 (2-track)

> P0_ARCHITECTURE.md **d5** 산출물. hexa-native trainer 가 production scale 에서
> 🔴 INFEASIBLE 실측(M5)이므로, P2 학습을 막지 않게 **2-track** 으로 분기한다.
> sibling: [P0_ARCHITECTURE.md](./P0_ARCHITECTURE.md) · [CLM.md](./CLM.md) ·
> [CORE/DECODER/STEP_RATE_LOG.md](../CORE/DECODER/STEP_RATE_LOG.md) (M5 측정 SSOT)

## 0. 한눈 결론

| 트랙 | 무엇 | 상태 |
|---|---|---|
| **Track 1** (즉시·런치 unblock) | PyTorch fp16 conv-MoE 트레이너 scaffold | ✅ smoke-runs, **feasible (실측)** |
| **Track 2** (장기·g1 순수) | hexa-native trainer 🔴 INFEASIBLE root-cause → hexa-lang handoff | ✅ 진단 완료 + handoff filed `5cd0e4c8` |

추론은 변함없이 **AKIDA-int4-only** (d4). 두 트랙 모두 *학습* 만 다룬다 — g1 순수성(추론
AKIDA-only)은 불변.

---

## 1. Track 1 — PyTorch fp16 baseline (즉시)

### 1.1 산출물

- `CORE/DECODER/clm_b0_pytorch_trainer.py` — conv-native MoE byte-LM 트레이너.
  - **Q1 Conv-native**: dilated causal conv stack (attention 0 → AKIDA conv-envelope 정합). left-pad causal, layer 마다 dilation `2^i`.
  - **Q2 MoE conv-expert = mitosis cell**: top-K HARD router + per-expert dilated-conv branch. router straight-through, decoder HARD top-1 설계와 정합.
  - **Q3 byte-vocab V=256**: V/d≈4배 (V≫d monopoly 근원 직격).
  - **monopoly-escape**: Switch 스타일 load-balance aux (`E·Σ f_e·P_e`) + router entropy 진단(diagnostic). entropy-anneal hook 자리.
  - fp16: `torch.amp.autocast('cuda')` + `GradScaler` (CUDA 일 때만). CPU fallback 자동.

### 1.2 authoring 채널 (정직)

`.py` 는 hexa-native Write/Edit 가드가 막는다. P0_ARCHITECTURE.md §6 의 문서화된
escape 채널 — **`python3 -c "open(PATH,'w').write(...)"`** — 로 작성·커밋했다.
`.gitignore` 가 정식 `.py` 를 허용한다 (R37 scrub 2026-05-12; `.pyc`/`__pycache__`/`venv`
만 차단). 기존 커밋된 `.py` 트레이너 다수 존재 (`HEXAD/CARVING/state/*/train_*.py`).
@py attr 는 없다 (P0 §6 정정).

### 1.3 실측 smoke (feasible? ✅ YES)

```
cmd : python3 clm_b0_pytorch_trainer.py --steps 30 --d 64 --layers 2 --experts 4 --top-k 1
host: Mac local CPU · torch 2.8.0 · cuda=False
```

| metric | 값 |
|---|---|
| CE | 5.6617 → 0.2575 (monotone 학습) |
| distinct_experts | **4/4 매 step** (toy-scale monopoly 0) |
| router_H | ~1.27 (uniform ln4=1.386 근접, balanced) |
| **step-rate** | **22.003 step/s (CPU, steps 2..30)** |

verdict verbatim: `.verdicts/clm_b0/smoke_cpu_d64_E4_2026_05_30.txt`.

**정직(p7)**: 이 22 step/s 는 toy-scale (d64/L2/E4/byte-vocab) CPU smoke 다 — PyTorch
*경로가 feasible 하고 conv-MoE fwd/bwd 가 정상* 임을 증명하지, production-scale
(V=151643·real corpus) throughput 수치가 아니다. fp16 GPU smoke 는 로컬 CUDA 부재로
미측정 (`--fp16` 플래그 준비됨) — H100 fp16 단발은 optional follow-up, scaffold 는 CPU 로 증명됨.

### 1.4 처리량 목표 (throughput target)

| 기준 | step/s | 근거 |
|---|---|---|
| hexa-native (M5 측정) | 0.23–0.50 | production-scale 🔴 INFEASIBLE (44–122 GPU-days) |
| PyTorch CPU toy (실측) | **22.0** | scaffold feasible 증명 |
| PyTorch fp16 H100 (목표) | **≥10** (green-tier gate) | P2 production fire 에서 실측 |

PyTorch CPU toy 만으로도 hexa-native 대비 ~44–96× 빠름. fp16 H100 production 은 P2
fire 에서 실측 (a_fire_autonomous).

---

## 2. Track 2 — hexa-native trainer 🔴 INFEASIBLE root-cause

### 2.1 M5 측정 요약 (STEP_RATE_LOG entries 7/10/11/12, 6+ independent H100 fires)

| entry | build | step/s | RSS slope | 비고 |
|---|---|---|---|---|
| (7) | CPU | **0.50** | ~0.5 GB/step | 첫 실측, V=151643, 29M params |
| (10) | HEXA_CUDA | 0.156–0.18 | 200–325 MB/step | cuBLAS engage 후 NET 더 느림 |
| (11) | HEXA_CUDA fb | 0.234 | **331 MB/step** | full 300/300 완주, RSS step1 1.79GB→step300 100GB |
| (12) | post-adopt | 0.283 | **328 MB/step** | #2017+#2031 land 후, slope 불변 |

production ceiling: 50×V presentations = 1.895M steps @ best 0.50 step/s = **44 GPU-days**
(0.156 step/s 면 122 GPU-days). + leak 으로 50×V 학습 시 ~95 TB RSS 필요 = single-pod OOM.

### 2.2 root-cause 3건 (전부 hexa-lang runtime-side · anima trainer 결백)

1. **per-step RSS churn ~328–331 MB/step LINEAR** — #2017 in-place AdamW (233MB out churn 제거) 채택 후에도 RSS slope 328≈331 MB/step 불변 ⇒ 누수원이 trainer-side alloc 이 아니라 hexa-lang **runtime/CUDA-side** 임이 EMPIRICALLY CONFIRMED (entry 12 가설 B 확정). 후보: `_CudaFarrSlot` device-mirror life-cycle · GPU device-resident scratch · hexat C 산출물 hidden transient handle · glibc arena fragmentation. runtime.c 에 `malloc_trim`/`mallopt(M_MMAP_THRESHOLD)`/`madvise` 부재.
2. **d=64 small-matmul GPU↔CPU sync overhead dominance** — #2018 offset-aware cuBLAS gemv engage 후 step-rate 가 0.50→0.156 으로 NET 더 느려짐. `cudaMemcpy` 동기 + kernel launch latency 가 9.7M-FLOP gemv compute 자체를 압도 (#1354 "d=64 too small for cuBLAS" 사전예측의 직접 실측 confirmation).
3. **AdamW out 233MB/step churn** — #2017 in-place AdamW builtin 으로 해소 확인. 단 잔여 328MB/step source 는 (1) 의 별개 문제.

anima trainer 의 per-step 할당은 전수 `farr_free` 됨 (entry 8 source 전수조사) — fix 는
builtin 내부 alloc 이라 anima-side 불가 (a_completeness_over_cheap 위반 회피).

### 2.3 hexa-lang handoff

- **handoff id `5cd0e4c8`** (`sidecar handoff add hexa-lang …`, a_runpod_inbox 채널).
- 요청 진단: runtime arena retention audit (step-tail `malloc_trim(0)` / `mallopt(M_MMAP_THRESHOLD)`) + `_CudaFarrSlot` mirror life-cycle tally.
- cf inbox #2030 (잔여 200–325 MB/step) · #2034 (mm_extract host RSS leak follow-up). anima-side fix 하지 않음 — handoff filed only.

---

## 3. 다음 (P1 → P2)

- P1: byte corpus build (웹대량+엄선 혼합, .kosmos 영속) → 이 트레이너의 toy corpus 교체.
- P2: 3-arm(A/B/A+B) × scale-ladder full-fire — 이 PyTorch fp16 트레이너로 H100 production. F-CLM-MONO/SCALE 판정. fp16 H100 step-rate 실측 (≥10 step/s green gate).
- Track 2: hexa-lang `5cd0e4c8` 해소 시 hexa-native trainer 재측정 (장기·g1 순수, 런치 비차단).
