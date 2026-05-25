# DECODER — log

Append-only history sister of `DECODER.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-26 — M3 STEP-1 재정의: substrate 벽 아님, "잘못된 경로" — forge GPU lm-head 는 V-generic

M3 실발사 인라인 시도 + 진단 결과, 더블바인드 fire 의 진짜 병목을 규명.

- [x] **M3 background agent 死 처리** — throttle 해소 후 재발사한 agent 가 API-500 으로 死(로컬 real-BPE smoke 단계, **GPU 발사 前**). `runpodctl pod list`=[] → **pod 0개, orphan 0, $0 누수**. 진행분 worktree 커밋 `44f6f6915` salvage.
- [x] **ubu-2 ($0) STEP-1 시도 3회 전부 0-출력 死** — OOM 아님(30GB 중 1GB), segfault 로그 없음. `qwen_bpe_load(151643-vocab)` 가 **CPU FP64 flame(`stdlib/flame/tensor_lib`)** 에서 observable window 내 미완료 + hexa stdout 버퍼링으로 진행 불가시.
- [x] **🔑 재정의 (forge 구조 정독)** — 벽은 "hexa substrate 가 real-BPE 를 못 함"이 **아니라** "smoke 가 CPU FP64 flame 을 썼지 forge GPU ag_tape 경로를 안 탔기 때문":
  - `ag_lmhead(tape, temb, zT, V, d)` (ag_tape.hexa:470) 는 **V-파라미터** (V=256 은 byte-level 실험 선택, 커널 한계 아님).
  - `ag_k_lmhead()` 는 `farr_matmul native` 로 디스패치 (ag_fuse.hexa:104) — **임의 V 처리**. hxcuda(self/native/hxcuda_*, test_hxcuda_matmul) CUDA matmul 존재.
  - ∴ **forge GPU lm-head 는 V=151643 가능** (그냥 큰 matmul + V-loop softmax). 분석의 "V=151643 미검증" = 안 돌려봤을 뿐, 불가능 아님.

### (C) 실체 + 계획 — V3 를 forge GPU ag_tape 경로로 포팅

- [ ] **STEP-1' forge GPU lm-head V=151643 검증** (bounded de-risk) — 최소 ag_tape lm-head matmul+softmax 를 V=151643 으로 CUDA 에서 1회 실행, wall/mem 측정. ⚠ blocker: CUDA 호스트 (ubu-2 RTX 5070 — 현재 네트워크 다운, 또는 runpod).
- [ ] **V3 decoder → ag_tape 포팅** — `conscious_decoder_v3.hexa` 의 forward/backward(M0 완성분)는 `stdlib/flame/decoder_lib`(CPU) 기반. forge GPU 는 `ag_tape` API(ag_embed/ag_rmsnorm_mh/ag_rope_mh/ag_attn_dt/ag_silu_gate/ag_linear/ag_lmhead). 4축(freeze/curriculum/head_g/distill)도 ag_tape 위로 재배선. RFC-scale.
- [ ] **forge GPU 에서 4축 더블바인드 fire** — real Qwen BPE(V=151643) + multilang corpus, A/B/C/D 매트릭스. 이때 비로소 진짜 3B-scale verdict.

