# M4b-fire-rev2 — fire unblock + build recipe (2026-05-28)

sign-gate UNBLOCKED (`sidecar sign local`). FIRE_BLOCKED.md 7-step runbook 실행.
이 문서는 실제 발사에서 검증된 build/fire recipe (artifact-of-record).

## 0. sign window (Mac, sign-gated · 최우선)
```
HEXA_MAC_BUILD_OK=1 HEXA_LANG=/Users/ghost/core/hexa-lang \
  HEXA_STDLIB_ROOT=/Users/ghost/core/hexa-lang \
  hexa build CORE/DECODER/train_v3_moe_pilot_rev2.hexa --c-only -o build/trainer_rev2.c
```
주의: `HEXA_LANG` 필수 (HEXA_STDLIB_ROOT 단독으로는 flame_bpe_corpus_lib 미해결).

## 1. Mac trim sed patch (3 occurrences)
```
sed -i '' 's/hexa_call1(trim,/rt_str_trim(/g' build/trainer_rev2.c
```

## 2. diverse corpus 재생성 (Mac, non-gated)
```
hexa run training/build_corpus_diverse_v2.hexa
# → training/corpus_consciousness_v2_diverse.jsonl (2000 lines, 1.27MB)
```

## 3. pod (RunPod H100 SXM — PCIe 품절 시 a_wall_first)
```
runpodctl pod create --name m4b-rev2-2026-05-28 \
  --gpu-id 'NVIDIA H100 80GB HBM3' --gpu-count 1 \
  --image 'runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04' \
  --container-disk-in-gb 60 --ports '22/tcp' --cloud-type SECURE
# pod yfqcywjlxavmgr · $3.29/hr · sm_90 · GLIBC 2.35 (pod-side hexa run 불가)
```

## 4. scp bundle
- trainer.c (rev2, patched) + glue.c → /work/
- self/runtime.c · runtime_core.c · runtime_hi_gen.c · runtime.h → /work/self/
- self/cuda/runtime_cuda.c · runtime_bf16.c → /work/self/cuda/
- self/forge/forge_tier_v1.{c,h} → /work/self/forge/
- self/native/*.{c,h} → /work/self/native/
- Qwen merges.txt + vocab.json (vP21M_3B_CUR1/lora_adapter, 151387 merges / 151643 vocab) → /opt/qwen/
- corpus_consciousness_v2_diverse.jsonl → /opt/corpus/

## 5. pod-side dir_create codegen-gap patch (cross-backend, NEW finding)
trainer.c 의 `hexa_call1(dir_create, X)` 가 Linux gen2 backend 에서 undeclared
(trim 과 동일 cross-backend codegen gap). runtime 의 `rt_fs_mkdir_p(HexaVal)` 로 치환:
```
sed -i 's/hexa_call1(dir_create,/rt_fs_mkdir_p(/g' trainer.c
```
→ hexa-lang INBOX 보고 대상 (a_runpod_inbox).

## 6. build (glue.c + -lcuda 필수)
```
nvcc -O2 -std=c++14 -DHEXA_CUDA -arch=sm_90 -x cu -c self/cuda/runtime_cuda.c -o runtime_cuda.o
clang -O2 -D_GNU_SOURCE -D_XOPEN_SOURCE=600 -DHEXA_CUDA \
  -I self -I /usr/local/cuda/include -Wno-trigraphs -fbracket-depth=4096 \
  trainer.c glue.c self/runtime.c runtime_cuda.o \
  -L/usr/local/cuda/lib64 -L/usr/lib/x86_64-linux-gnu \
  -lcublas -lcudart -lcudart_static -lcuda -ldl -lrt -lm -lpthread -lstdc++ -o trainer
```
- glue.c = strong `hexa_cuda_available()`→`_hx_cuda_runtime_available()` (weak-0 stub 제압,
  #1671 미landing 로컬 replica). 없으면 cuBLAS CPU-fallback.
- `-lcuda` (driver lib) 필수 — runtime_cuda.c 가 cuModuleLoadData/cuLaunchKernel 등
  CUDA Driver API 사용 (agtape 구recipe 엔 없었음, 신규 의존).

## 7. fire
```
timeout 2400 ./trainer > trainer.out 2> trainer.err  (nohup detached + nvidia-smi monitor)
```
- result.json + verdict matrix → /opt/anima/state/m4b_pilot_rev2/result.json (inline LZ76/TTR)
- ckpt 저장 deliberate omit (Phase 5b: 29M+ double text-dump O(n²) segv). 산출 = result.json + decoded_ids.
