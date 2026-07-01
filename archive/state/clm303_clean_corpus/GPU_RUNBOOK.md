# GPU 측정 런북 — 헤매지 않는 정석 (anima decode/측정)

> 이 세션이 멀티시간 헤맨 단 하나의 이유 = GPU 켜는 정석을 몰라서. 이 5줄이면 끝.

## 0. 정석 (이거 한 줄이면 GPU 켜짐)
```sh
HEXA_CUDA=1 sh install.sh      # GPU 호스트(nvidia-smi+libcudart)면 cuda hexa 설치 → cuda_available=1
# install.sh prefer_cuda(): unset이면 자동감지(nvidia-smi -L + libcudart.so)로도 cuda 선택 (pip install torch 식)
```
- 확인: `hexa run 'fn main(){print(cuda_available())}'` → **1** 이어야 함. (`HX_TAG=test` 등 불필요, raw main install.sh 사용)

## 1. 절대 하지 말 것 (= 헤맨 함정들)
- ❌ stock `sh install.sh`만(opt-in 없이) → 감지 실패 시 CPU. GPU 측정인데 CPU면 렌트비 낭비.
- ❌ `tool/build_cuda_runtime`·`stage_resolve_runtime_a` **수동 빌드** → build-context 깨져 undefined-refs 실패. 정석 install 쓰면 됨.
- ❌ `hexa gpu` self-probe로 GPU 판단 → **항상 cuda_available=0**(그 바이너리는 CPU 부트스트랩). 진짜 확인은 install 후 `hexa run`.
- ❌ runtime.a swap / pool 호스트 runtime.a 손대기 → 공유 호스트 변형 금지.
- ❌ stable v0.32x asset이 GPU 0이면 = stale 빌드. `releases/latest` 또는 `test` 태그가 fresh.

## 2. clm303 GPU 측정 풀 절차 (fresh pod)
```sh
hexa cloud rent vast --gpu A40 --image nvidia/cuda:12.4.1-devel-ubuntu22.04 --disk 80
# pod에서:
HEXA_CUDA=1 sh install.sh                          # ① cuda hexa (cuda_available=1 확인)
# mac에서:
cli/eval_pod.sh <pod> ~/anima-weights/clm303_clean/clm303_clean.clm --gen 5 --harvest <out>
#   ↑ --bootstrap 빼기 (그건 stock CPU 재설치) — cuda hexa 유지한 채 번들+빌드+eval
# 확인 포인트: 디코드 stderr에 [OWN-GEMM-FIRED] DEVICE path = GPU 실발화
```
- ckpt: mac `~/anima-weights/clm303_clean/clm303_clean.clm` (HF PRIVATE sha검증됨).
- teardown 전 결과 harvest + `a_fire_recover_complete`.

## 3. 측정 후 닫기
- own-GEMM 발화 확인 → G0-G6 verbatim → host RSS 궤적(GPU-path 누수/RANK-3 env A/B).
- teardown: `printf 'y\n'|hexa cloud provider-cli vast --allow-mutate -- destroy instance <id>` → Total:0 → forget → `sidecar ing pod rm`.

## 근거 (committed)
- gpu_enable_RESOLVED.txt — A40 cuda_available=1 실측, install.sh prefer_cuda auto-detect 이미 구현.
- 메모리 hexa-gpu-enable-canonical-install.
