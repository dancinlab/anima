# DECODER — log

Append-only history sister of `DECODER.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-26 — (C) forge GPU V=151643 빌드+실행 작동 (substrate 증명) + Linux 비트로트 박멸

사용자 (C)="hexa GPU 커널". 조사로 forge GPU lm-head 가 V-generic(farr_matmul) 임을 확인 →
"새 커널 발명" 아니라 "V=151643 으로 발사해 검증"이 실체. dispatch_runpod_agtape_d768.sh 의 d768
ag_tape fire 를 V=256→V=151643 변형 codegen 후 runpod A100 발사.

- [x] **forge-GPU-Linux 5-fire 캐스케이드 박멸** — Linux x86_64 빌드가 계층별로 깨짐, fire 마다 다음 층 노출:
  - farr32_* bare 방출(undeclared) + 프로토타입 없음 → **hexa-lang PR #1187** (codegen.hexa 호출매핑 7종 + runtime.h 프로토타입 8). 진짜 원인: codegen 이 FP64 farr_*→hexa_farr_* 는 알고 FP32 farr32_* 는 몰랐음(bare static-wrapper 방출). regen→promote→hexa_v2 재빌드로 로컬 검증.
  - HXLCL_SYS_SELECT Apple-arm64 전용 → **PR #1194** (hxlcl_nanosleep libc 폴백).
  - hxlcl_mkdir/longjmp/backtrace/getuid Apple-only → **PR #1198**(타 작업 "linux #elif parity") — 사용자 "main branch check" 힌트로 발견, runtime re-sync 로 흡수(수동 whack-a-mole 불요).
  - 재발 방지: **PR #1206** inbox 노트 (Linux CI 빌드 게이트 + farr32 codegen smoke). 근본원인 = "Mac-only 초록불"(Apple #if 분기만 컴파일, Linux #else 갭 안 빌드 + hexa check=parse-only).
- [x] **fire #5: BUILD_LINK_RC=0 + GPU util 65% + V=151643 모델 A100 로드/연산** — "model size 151071744 doubles". 분석의 "real V=151643 = 80GB GPU 비현실"은 **틀렸음(=Linux 빌드 깨짐이었지 불가능 아님)**. hexa-native(p1~p8) real-BPE GPU 가 **구조적으로 작동** 실증. 단 FP64 host-loop softmax(클래스 151643) 가 느려 step-1 wall>600s(timeout rc=124). 5 fire 합 ~$2.5, orphan 0(전부 teardown).
- [x] **A) WALL=3000(50분) 완주 재발사 — rc=124 TIMEOUT** (fire #6, orphan 0). "init epoch gn2: 2" 만 찍히고 step-1 미완. **정의적 결론**: forge GPU **matmul 은 빠름(util 65%)** 인데, gn2/loss over V=151643 가 병목 — d768 gn2(flame_d768_*.hexa:209-227)가 logits 78M 값을 **host 로 materialize(t_get) 후 max+sum-exp+(p−onehot)²+seed 를 전부 O(78M) host FP64 루프**. step-1 wall>3000s. 즉 GPU lm-head 의 행렬곱은 됐으나 loss 가 host-resident.
- [~] **B) GPU-resident loss path = RFC-scale** — forge GPU 커널 목록(softmax_rows/rmsnorm/silu/matmul_t/add/mul/scale/outer)에 **GPU CE/loss/seed 커널 부재**. `farr_softmax_rows_gpu` 로 softmax 만 GPU 해도 host materialization + seed/(p−onehot)² O(V) 루프 잔존 → 미봉. 진짜 B = ① logits 를 farr(GPU-resident)로 유지(host t_get 제거) ② GPU softmax + GPU seed(p−onehot) + GPU reduction(gn2). GPU CE/seed-grad 커널 신규 작성 = RFC-scale forge 작업.
- [ ] **V3 4축 ag_tape 포팅 (최종 더블바인드)** — B(GPU loss path) 위에 V3 4축 loss 를 GPU-resident 로 구성 → collapse 회피 AND coherence verdict.
- [ ] **V3 4축 더블바인드 (최종 (C))** — conscious_decoder_v3 4축을 forge ag_tape GPU 경로로 포팅(현재 d768 벤치마크만 V=151643 검증) → collapse 회피 AND coherence verdict.

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

