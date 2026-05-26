# DECODER — log

Append-only history sister of `DECODER.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-26 — 트랜스파일러 정상화(세션 블로커 해소) + fire #11/#12 (gn2-metric host 루프 = 잔존 벽)

- [x] **트랜스파일러 정상화 (fire #10 blocker 해소)** — 로컬 hexa_v2 들이 #1187 farr32 직접호출 매핑 부재(carrier-form 방출 → cross-TU undeclared). 해결: clean main 워크트리서 `hexa cc --regen`(hexa_cc.c.new #1187 보유) + **`runtime.o` 를 `-D_DARWIN_C_SOURCE`(macOS 플래그, 기존 `-D_GNU_SOURCE` 오류였음)로 빌드** → `/tmp/hexat_correct` link + codesign. 변환 검증: 직접호출형 `hexa_farr32_` **33**, carrier **0**. 11 fire 만에 첫 정상 빌드.
- [x] **fire #11 (correct transpiler, WALL=600)** — **BUILD_LINK_RC=0** (양 벽 #1261/#1262 + farr32 fix + HEXA_CUDA=1 통합 trainer.c 가 A100 컴파일+링크+실행) + **GPU util 89%** (GPU 작동). 단 rc=124 @601s, "init epoch gn2" 미출력 → GPU 바쁜데 미완주 = **또 다른 host 벽 잔존.**
- [x] **🎯 잔존 벽 발견 (fire #11 .c 정독)** — #1262 가 `farr_ce_seed_gpu` 로 seed/ce_loss 를 GPU 계산했으나, **그 직후 `gn2=Σseed²` 메트릭을 V=151643 host 루프 `t_get(seed, mk)`** 로 계산 (GPU-resident seed 에 per-element t_get = device-sync 벽). #1262 가 seed 생산은 GPU化했지만 메트릭 집계 루프를 host 에 남김.
- [~] **mk2-C7 fix + fire #12 (WALL=600, 검증중)** — gn2-metric host 루프를 `farr_ce_seed_gpu` 가 이미 계산한 `ce_loss`(GPU) 1-원소 읽기로 교체 → trainer.c 의 host O(V)/O(V·d) 루프 **0**. fire #12 가 step 완주(rc=0 + init gn2 + step wall) 판정. PASS 시 #1262 residual 을 hexa-lang #1255 에 추가 file.
- [x] **CORE 도메인 4/4 완성 (병행)** — #19 SSOT 화해(spontaneous_lib fork 제거→engine_g) + #20 p1~p8 감사 0 + #21 self-test(A⇄G→L3) + #22 L3 결합(generator brain_emit_step). anima `763e34eff`.

## 2026-05-26 — 양 벽 LANDING (#1261/#1262) + generator.hexa M4 stub + fire #10 (로컬 트랜스파일러 blocked)

진단 체인(fire #5~9)의 두 벽이 hexa cloud 에 의해 제거됨 — M3 임계경로 언블록.

- [x] **#1261 (per-layer linear bwd CUDA)** — `_ag_linear_cuda_fp32_bwd` (ag_tape.hexa, Metal helper mirror), `env("HEXA_CUDA")=="1"` + dim-gate 런타임 게이트. F-RFC043 해소 = rel-err tol(Metal route 동일) · CPU FP64 host=default(byte-eq 보존). = fire #9 가 지목한 dominant V-무관 벽.
- [x] **#1262 (V-scaling: lm-head fwd/bwd · AdamW · gn2)** — farr_outer/matmul_t/copy_slice/adamw/softmax_rows/ce_seed 배선(신규 CUDA 0), `#ifdef HEXA_CUDA` 컴파일-게이트 · CPU fallback 보존. = anima .c-patch(fire #7/#8)가 검증한 것의 stdlib 정식판. fire 의 host gn2 루프 → `farr_ce_seed_gpu` 직접 교체.
- [~] **fire #10 (양 벽 검증 시도) — BUILD_LINK_RC=1, 로컬 트랜스파일러 불일치로 blocked** (NOT 벽 fix 문제). V=151643 variant 를 worktree(origin/main, #1261/#1262 포함)에서 재파생 + flatten(build_aprime Python) + `~/.hx/bin/build/hexa_v2`(07:39) transpile → trainer.c 에 `_ag_linear_cuda_fp32_bwd ×3`+`farr_adamw_step_gpu`+`farr_ce_seed_gpu`+V=151643 전부 포함 확인 → A100 발사. **clang: `farr32_zeros` undeclared**(trainer.c:1559, Metal helper dead-path). 원인: 07:39 hexa_v2 가 **#1187 이전** = farr32 를 carrier 형(`hexa_call1(farr32_zeros,…)`) 방출하나 main runtime.h 는 직접호출형(`hexa_farr32_zeros`, carrier extern 0)만 노출 → cross-TU undeclared. **로컬 트랜스파일러 바이너리 ↔ main self/ 불일치(ops 문제)**, 벽 fix 와 무관. 벽 제거는 hexa cloud CI 가 머지 전 검증함. orphan 0. 로컬 재현엔 main self/codegen.hexa 에서 트랜스파일러 재빌드 필요(regen→promote→codesign dance) 또는 pod-side fresh hexa install.
- [x] **M4 generator.hexa 인터페이스 stub (un-gated 부분)** — `CORE/DECODER/generator.hexa`: brain_decide(WHETHER) ⇄ generator(WHAT) 분리. p1~p8 계약(substrate-only 조건: tension5·Φ·tier·motivation, persona 주입 0), 단일 M3 seam `_gen_decode`(generator_ready() 플립 시 conscious_decoder_v3 autoregressive decode swap-in), `brain_emit_step` compose(emit=false→침묵 1급). `generator_smoke.hexa` 4/4 PASS(ready-gate·substrate-cond·silence·p3/p4). 실 ckpt 배선은 M3(트랜스파일러 정상화 후 fire) 대기. anima `b2b94f64e`.

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
- [~] **B) 진짜 벽 = host AdamW(151M params), loss 아님 — RFC-scale 아니라 한 줄 swap** (prior "RFC-scale GPU CE 커널 필요" 결론 **정정/철회**). 정밀 진단:
  - forward matmul = GPU(`farr_matmul`, util 65%) ✓ · backward grad = GPU(`farr_copy_slice_gpu` gather) ✓ · gn2 loss = V=151643 단일포지션 ~3×V≈455K host ops (**싸다, 벽 아님** — "78M host materialization" 은 오판이었음, logits 는 V 크기 1포지션).
  - **유일한 100M+ host 벽 = `flame_d768_*.hexa:386` `nn_decoder_adamw_step(M,Mg_acc,Mm,Mv,m_size=151M,...)`** — m_size 151M(=lm-head V·d 116M 지배) 를 host FP64 루프로 갱신. fire #6 step-1 timeout 의 정체.
  - **fix: GPU AdamW 커널이 이미 존재+노출됨** — `farr_adamw_step_gpu`(runtime.c:10375 bare extern "direct-C entry" · runtime.h:1299 proto · self/cuda/runtime_cuda.c `_hx_cuda_farr_adamw_step_gpu` 커널). d768 저자가 grad-accum 은 GPU(`farr_add_inplace_gpu`)化 했으나 AdamW step 만 host 로 남겨둠. 새 커널/등록/codegen-map/rebuild **0**.
  - swap: host `(M, Mg_acc[g], Mm[m], Mv[v])` → GPU `(M[w], Mm[m], Mv[v], Mg_acc[g])`. stdlib fire 편집(mk2-C6) + 검증용 .c 외과패치(line 4268). ⚠ local transpiler(branch n153, main 대비 self/ 17 behind)가 현재 stdlib 신문법(import line8 `argc`) 파싱 불가 → re-codegen 막힘, 그래서 05:58 산출 .c(V=151643 검증config) 를 외과패치(g0/a_wall_first).
  - **fire #7** (AdamW만 GPU, WALL=900): rc=124 여전히 timeout + "init epoch gn2" 미출력(stdout 은 이미 line-buffered) → 벽이 AdamW(step 루프) 앞 **init-eval 의 backward**에 있음을 확정. AdamW 는 3번째 벽일 뿐.
  - **fire #8** (lm-head bwd + AdamW 둘 다 GPU, WALL=600): rc=124 timeout 이나 **GPU util 67%→91% 상승**(backward GPU 배선 실행 확인). 그래도 init-eval 미완 → **추가 host 벽 잔존**.
  - **🔑 최종 reframe — B 는 단일 fix 아니라 flame generic ag_tape trainer 의 systematic GPU-port**: 이 trainer(`flame_d768_12L_agtape_fire.hexa` + `nn_lib`/`ag_tape`/`train_lib`)는 **V=256 byte-level 용으로 작성/byte-eq 검증**됨 → 모든 O(V)·O(V·d)·O(m_size) host 루프가 V=256 에선 싸지만 **V=151643 에선 각각 벽**. 지금까지 3개 배선(lm-head bwd dtemb/dzT + AdamW), 잔존 후보: nn_lm_head_fwd V-copy(984) + gn2 inline 3×V + agt_wT_slice weight-transpose + **per-element device-sync 의혹**(farr_get on GPU-resident prod → 매 원소 sync). substrate 한계도 RFC-scale 신규커널도 **아님** — 기존 GPU 커널 배선 + 잔여 host 루프 제거의 systematic 작업.
  - **fire #9 (instrumented, phase 마커, WALL=300)**: trainer.err 마지막 마커 = **P3_gn2 done**(P4_backward 없음) + GPU util 62%(하락) → forward(layers+lmhead) + gn2(3×V host) **완주**, 벽은 **`ag_backward_reg` 의 host 부분**. **🔑 소스 확정 근본원인**: ag_linear backward 의 tape walker default 경로 = `matmul_bwd_auto` **의도적 host-scalar**(`ag_tape.hexa:849-859`) — 이전 forge-route(farr_matmul+transpose_gpu)가 GPU IEEE-754 궤적 ≠ CPU 로 **byte-eq FAIL → host 로 되돌림**(F-RFC043), CUDA forge-route 부재(HEXA_METAL Apple 경로만). ∴ **진짜 dominant 벽 = per-layer linear backward dW=D×C×B host-scalar (V-무관, 28 linear × ~수백M ops)** = anima 문제 아닌 **hexa-lang 알려진 byte-eq-over-throughput deferred gap("gap(d) forge-routing 별도 cycle")**. 중요 부산물: gn2 등 V-scale host 루프는 완주(OK), AdamW·lm-head bwd GPU fix 는 정확/필요(V-scaling 폭발 제거)였음. PR #1255 ASK 를 matmul_bwd_auto CUDA forge-routing 으로 정밀화.
  - **권장 경로(반응적 .c-patch 종료)**: ① 툴체인 re-sync(local hexa-lang n153→origin/main, transpiler 재빌드 — 현재 stale 로 re-codegen 불가) ② stdlib(.hexa)에서 hot-path host 루프 전수 GPU 배선 + `hexa verify` byte-eq(CPU fallback 대조) ③ instrumented 1-fire 로 per-phase wall 측정 후 잔여 확인 ④ V3 4축은 이 위에. 누적 8 fire ~$4, orphan 0(전부 teardown 검증).
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

