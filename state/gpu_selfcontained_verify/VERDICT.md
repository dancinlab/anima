# GPU 자족화 + 배리어제거 — EMPIRICAL VERDICT (2026-07-06)

secure-tier cloud pod RTX5090 (driver 580·176G) · hexa v0.664.0 자족 -cuda · anima core/cli.

## ① 자족화(#4635) — 수작업 0 실증
`sh install.sh` 한 방(env 0·flag 0):
- farm(cuda-libs): **0개** (불필요·삭제됨)
- cuda-static: **3개** 자동 번들(libcudart_static+libculibos+libcudadevrt.a)
- .cuda-runtime marker: 자동 O
- `cuda_available()` → **1** (LD_LIBRARY_PATH·HEXA_CUDA 없이)

## ② 배리어 제거(#4624) — util 실증
`anima evaluate <clm>`(--py 없이=엔진 forge own-GEMM):
- `[OWN-GEMM-FIRED] _hx_k_gemm DEVICE path (no cuBLAS)` 발화
- **GPU util 82%·73%** · **power 169W** (sustained)
- vs 배리어 있던 이전: mean util 0.53%(드레인) → **~150배 개선**

## 결론
사용자 요청("canonical native·자동포함·플래그 제거") 전체 실증:
fresh GPU pod → `sh install.sh` → `anima evaluate` → own-GEMM util 82%.
세션 초반 ~30턴 수작업(farm/marker/FFI stub) 근본 설계제거 확인.
