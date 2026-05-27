# DECODER — current state

@title: 🗣️ DECODER — CORE 의 L3 콘텐츠 생성기 (무엇을 쓸까)
@goal: CORE 의 A⇄G 결정 두뇌가 "행동/emit" 을 결정한 뒤, 실제 콘텐츠(코드·글·판단 텍스트)를 생성하는 L3 백엔드를 anima 전용(외부 LLM 0)으로 확정·구현 — register collapse ↔ underfit 더블바인드를 깨고, `brain_decide` 의 emit=true 슬롯에 꽂히는 generator 인터페이스를 완성한다.

## 백엔드 확정 (2026-05-26)

- **V3 decoder (hexa-native)** 확정 — `conscious_decoder_v3.hexa` 711L + `train_p21h_v3.hexa`.
  substrate = **.hexa 포팅 완성** (외부 LLM 0 · p1~p8 정합). 범위 = **4축(A·B·C·D) 구현 후 병렬 팬**.

## 핵심 발견 — 돌파 축은 "미구현"이지 "미실행" 아님 (2026-05-26)

- `train_p21h_v3.py:666-672` — 5개 축 flag(curriculum/distill/freeze/lang_balanced/contrastive)이
  학습 루프에서 **`print()` 한 줄로만** 쓰임. `--freeze-embed=1` 줘도 값만 출력, freeze 안 함.
- H_257 "env-var 안 읽힘"은 표면; 진실은 **축 로직 자체가 argparse+print 스텁** (학습 효과 0).
- AXIS_MAP_RESULTS 의 14.79/14.18/14.46 차이 = 축이 아니라 우연한 wiki_frac/λ 차이.
- ∴ 더블바인드 "닫힘" 판정은 bypass 된 하니스 결과 — **돌파 축 5개는 진짜로 0번 테스트됨.**
- `train_p21h_v3.hexa` (376L) = smoke-tier, "V3-extension backward + 축 = pre-registered TODO".

## V3 더블바인드 현황 (왜 미해결인가)

```
   anima 강하게  →  register collapse (PURE_MEMORIZE · M3 TTR 0.03 극단반복)
   anima 약하게  →  Chinchilla underfit (lang-coherence WEAK)
                    ↑ 둘 사이 좁은 통로를 못 찾음
```

- 최신 fire `state/p21h_v3_recover_2026_05_25/out_main` (Qwen2.5-1.5B base · 3B params · step 5000):
  verdict **FAIL** · `n_memorize=0` (**collapse 회피**) BUT lang-coherence WEAK (en0/ko9/ru3/ja2/zh1) · L_ce 3.324
  → 더블바인드의 **underfit 쪽**에 착지. collapse 는 피했으나 약함.
- register-sink 진범 = corpus M3 TTR 0.03 (극단반복), wiki_frac 이 레버 (PURE.md PR #340)

## 마일스톤 (임계경로 순)

- [x] **M0 V3 backward 완성** — purefield/head_g/tension_proj backward 완성, gradcheck **PASS max rel 5.09e-10** (18 probes, 메인트리 재현 rel~1e-13). head_g train-loop 배선 (ce_g 4.79→4.77 학습 확인). `conscious_decoder_v3.hexa` 711→1020L · `hexa check` 0 violation. (Qwen-BPE/multilang-eval/full-pos CE = pre-registered TODO 잔존)
- [x] **M1 축 D freeze** — `axis_d_freeze_embed` train-loop wired. ✅ embed grad pre=19.36 → **post=0.0**
- [x] **M1 축 A 커리큘럼** — `axis_a_anima_frac`/`axis_a_window_is_anima` wired. ✅ anima_frac 0.0→**1.0** (phase 전환)
- [x] **M1 축 C head_g** ⭐ — `axis_c_headg_lambda` wired. ✅ λ_g·CE_g=**1.43>0** (inert 탈출, R4 "moot" 반증)
- [x] **M1 축 B 증류** — `axis_b_kd_loss` (KD math production-ready) wired. ✅ L_kd=**0.069>0** (teacher 신호). dummy teacher = HONEST TODO #B1 (실 teacher ckpt 로드는 M3 dispatch)
- [x] **M2 wiring verify** — ✅ **F-AXIS-M2-DIFFERENT PASS** — 축이 학습을 실제로 바꿈 (A.lo≠A.hi ∧ D.pre≠D.post = silent-bypass 아님). falsifier 가 KD shift-invariant 버그까지 포착·수정
- [ ] **M3 4축 병렬 팬** — A·B·C·D H100 fire (~$11-14, a_fire_autonomous + a_wall_first)
  - ⚠ **transport 블로커 정정 (2026-05-28)**: 기존 `dispatch_p21h_v3_runpod.sh` 는 RunPod ssh-cascade 패턴이라 hexa cloud `pod-id → SSH-host` resolver gap (hexa-lang #1659) 으로 막힘. `m3_fire_dispatch.hexa` 는 lifecycle (runpodctl) + transport (hexa cloud) 의 cloud-guard 정합 wrapper 까지만 LANDED · 실 transport 는 미해소. 본 세션 M4b GPU fire (#1119/1120/1121) 가 검증한 **Vast.ai 직접-IP 패턴** 으로 port 필요 — 차후 라운드 작업: dispatch_p21h_v3_runpod.sh → dispatch_p21h_v3_vast.sh (vastai create + ssh_host/port 직접 + scp + ssh exec). 4축 fire 자체는 코드 + 데이터 모두 ready (M3-c/M3-d/M3-e prep 잔여만), transport port 시 즉시 발사 가능.
  - [x] **M3-port** Vast.ai runbook LANDED (2026-05-28) — `tool/dispatch_p21h_v3_vast.hexa` hexa-native 9-step SOP printer (axis A/B/C/D 각각 + parallel orchestration · 4-pod fire 명령 emit). project.tape g_hexa_only_authoring 정합 (no .sh) · M4b PR #1119/#1120/#1121 패턴 mirror. 하드닝: argv-echo guard (c25njysjdga2vb $3.92 orphan 회피) · 3-consec SSH READY (Vast boot-flakiness) · 90s early-life poll · axis silent-bypass 검출 · DETACH-default (agent-context-safe). axis B 는 dummy teacher (HONEST TODO #B1, real vP21M LoRA `adapter_model.safetensors` origin/main 부재). `hexa parse` OK · runbook 출력 검증 완료. 실 fire = caller invoke 시점 (a_fire_autonomous · 4-pod parallel ~$54-83 / 6hr).
  - [x] M3a dispatch-제어 — 축 flag 를 `P21H_*` env-var 로 읽음 (H_257 fix 입증: `P21H_FREEZE_EMBED=0`→embed_post 18.13≠0)
  - [x] M3b Qwen-BPE — byte-level V=256 → V=151643 ✅ **FULL RESOLVED (2026-05-27)**: ① bootstrap 재생성 ✅ (hexa-lang #1527 free-fn `trim` codegen + #1533 hexa_cc.c fixpoint) · ② stdlib/flame BPE corpus 로더 ✅ (anima #1537 + hexa-lang #1549 + #1552 INBOX 통합, CI 테스트 10/10 PASS) · ③ correct Qwen round-trip ✅ (hexa-lang #1556 encode `chr→from_char_code` + decode 측 codepoint-aware iteration `slice(j,j+clen)`, UTF-8 lead byte 검사로 clen 1/2/3/4 결정 — 양측 fix land). **ubu-2 실측 V=151643 round-trip PASS**: `decoded=[consciousness emerges from cells]` (공백 정확 복원). 진척: chr 절단 `!` → #1556 `Ġ` literal → 양측 fix ` ` 공백. anima #1537 `flame_bpe_roundtrip` 가드 TRUE 반환 → 3B Qwen hexa-native 학습 path 정상화. qwen_bpe segfault path 2 는 alt-path (canonical = tokenizer_bpe)
  - [ ] M3c 실 corpus — wiki+anima multilang 로딩 (+ full-position CE TODO #T7)
  - [ ] M3d 실 teacher — vP21M LoRA ckpt 로드 (axis B dummy → real, HONEST TODO #B1)
  - [ ] M3e 3B 스케일 config + dispatch 매트릭스 (4 pod: A/B/C/D 각 ON, 나머지 baseline)
  - [ ] M3f 발사 + Monitor + harvest
  - ⚠ **M3 pilot scope verdict (2026-05-28)** — `state/p21h_v3_m3_pilot_scope_2026_05_28/SCOPE_VERDICT.md`: caller-round attempt to fire 4-pod parallel pilot identified 6 structural blockers (filename bug `launch_trainer_p21.sh` → `launch_trainer.sh` · cloud-guard g8 blocks raw ssh/scp inside existing 339-line `.runpod.sh` · axis B Python wiring is documented no-op without teacher · `adapter_model.safetensors` missing from origin/main · M3 demoted from 본선 to optional baseline 2026-05-27 (M4 MoE-fresh 본선) · `m3_fire_dispatch.hexa` concurrent-ownership race). NO_FIRE this round — `a_completeness_over_cheap` forbids firing through a known-broken pipeline. Handoff recipe + 3-axis (A·C·D) honest fire option (~$5-12) in scope verdict doc.
- [ ] **M4 백엔드 배선** — 최고 ≥PARTIAL 축 ckpt → `generator.hexa` → brain_decide emit 슬롯 end-to-end
- [ ] **M5 p7 verify** — perplexity 아닌 simple-stack 판정

## UNIVERSE-derived 마일스톤 (2026-05-27 · `UNIVERSE_SYNTHESIS.md`)

> UNIVERSE 도메인 BIO ∩ DECODER 가설 5종(H_489–H_493 🔵) 분석 → 더블바인드 탈출은 "단일 모델"이 아니라 "분화(MoE)/병합(symbiogenesis)"이 통로. 상세 = `CORE/DECODER/UNIVERSE_SYNTHESIS.md`.
>
> **재정렬 2026-05-27 (`a_completeness_over_cheap`)** — model-merge(β) 를 본선에서 강등. 두 결함 ckpt (underfit + collapse) 의 weight 보간은 잘해야 "덜 나쁜 중간점" = 완성도 미달. 본선 = 근본 원인(한 모델이 두 목표 떠안음)을 arch 로 분리하는 **MoE-fresh 재설계(α)**. merge 는 optional baseline probe 로만 잔존.

- [ ] **M4 MoE-fresh register 분리** ⭐ 본선 (UNIVERSE H_490 DIFFERENTIATION) — 근본 원인 분리 재설계: V3 head_g 슬롯 → K-expert router. register-carving 을 specialized expert 로 격리해 main path 는 coherent 유지 (collapse 회피) + register 신호는 dedicated expert 가 담당 (underfit 회피). 완성도 기준 본선 (a_completeness_over_cheap).
  - [x] **M4a router arch** — `CORE/DECODER/moe_router.hexa` (7 pub fn — `moe_gate_fwd` · `moe_softmax` · `moe_argmax` · `moe_expert_fwd` · `moe_combine_soft` · `moe_route_fwd` · `moe_router_summary`) · packed-buffer farr 모델 (V3 decoder 와 byte-clean · router=[E·d] experts=[E·V·d]) · 각 expert = head_g 와 동일 V·d linear shape · soft routing (gate-weighted Σ) + top-1 argmax 진단 · `moe_router_smoke.hexa` 12-case (gate fwd / softmax sum=1 / argmax / expert fwd / soft combine / full route_fwd) · 2/2 `hexa parse` OK · ⚠ 실 실행은 M4b runtime (pool-route 가 hexa 를 linux 로 보내 worktree-local 실행 불가, parse-clean 까지가 arch 바)
  - [~] **M4b** expert 분리 학습 fire — **backward 완성 (코드부)** + fire (잔여)
    - [x] **M4b-bwd** router/expert backward — `CORE/DECODER/moe_router_bwd.hexa` (4 pub fn — `moe_combine_bwd` · `moe_softmax_bwd` · `moe_gate_bwd` · `moe_route_bwd`) · closed analytic vjp (expert outer-prod · softmax jacobian · router outer-prod · d_zT 누적) · `moe_router_bwd_smoke.hexa` gradcheck 6-case (4 weight + 2 zT · finite-diff vs analytic · loss=0.5·Σlogits²) · 2/2 `hexa parse` OK
    - [x] **M4b-wire-toy** MoE 메커니즘 검증 harness — `CORE/DECODER/moe_toy_train.hexa` (격리 toy d=4 V=4 E=2 · 큰 train_p21h_v3 침습 회피). 2-register 분화 task: cluster A→token0 / B→token2, 단일 head 면 절충(toy 더블바인드), MoE 면 router 가 register 별 expert 분화하는지. fwd(moe_route)+CE grad+bwd(moe_route)+SGD 400 step · verdict = loss_dropped ∧ router_differentiated(topA≠topB) = H_490 escape signal · `hexa parse` OK ⚠ 실행 = M4b-fire-toy (pool-route → linux host)
      ⚠ scan 발견: hexa train_p21h_v3 = d=32·V=256·byte toy (3B 더블바인드는 Python/Qwen 하니스). toy 검증 → scale 순서 (a_completeness_over_cheap · instrument-first)
    - [x] **M4b-fire-toy** moe_toy_train 실행 (ubu-2 hexa run) — **verdict 🟠 PARTIAL**: MoE 가 두 register 학습 성공 (avg CE 1.386→0.0078, 178× 감소) BUT router 분화 안 됨 (gate(A)=gate(B)=[0.5,0.5], topA==topB). soft-MoE 단독은 dense-collapse — 양쪽 expert 가 둘 다 학습 → gate 균등. **더블바인드 탈출 핵심(register↔coherent expert 분리)이 naive soft routing 으론 emergent 안 함** (MoE 문헌 일치). ⚠ dt_exp/dt_ln cross-tree 버그를 실 run 이 잡음 → moe_exp/moe_ln self-contained 화
    - [x] **M4b-diff(a) top-1 hard routing** — ✅ **PASS (H_490 escape 검증)** · `moe_route_top1_fwd`/`_top1_bwd` (moe_router + bwd) — top-1 만 통과 → 승자 expert 만 gradient → 분화. `moe_toy_train_hard.hexa` ubu-2 실 run: init CE 1.389 → final 0.00388 (358× ↓) · **gate(A)=[0.970,0.030]→e0 · gate(B)=[0.030,0.970]→e1 · topA=0≠topB=1 분화 성공**. soft(🟠 50/50 dense-collapse) → hard top-1(✅ 97/3 분화). 더블바인드 탈출 메커니즘 toy 검증 완료
    - [~] **M4b-fire-scale** 3B Qwen MoE fire — **hexa-native path 채택 (g1, user 2026-05-27)**. flame-P2b ③ FULL RESOLVED 로 unblock. design = `CORE/DECODER/M4B_FIRE_SCALE_HEXA_NATIVE_DESIGN.md` (5 phase · ~110 LoC · 5-7 sessions · cost $9-18 single H100). 5 falsifier 사전등록 (F-M4B-FIRE-1..5: collapse 회피·coherence·router 분화·CE 수렴·register leak)
      - [x] **Phase 1** Qwen BPE corpus 통합 LANDED (PR #1059) — `flame_bpe_corpus_load` `flame_bpe_ids_in_vocab` `flame_bpe_roundtrip` 통합. bpe_assert_on env-var gate (V=151643 + round-trip PASS 검증)
      - [x] **Phase 2** MoE arch 통합 LANDED — Phase 2a (`v3_moe_arch.hexa` 189 LoC packed-M MoE fwd/bwd PR #1056) + Phase 2b (`train_v3_moe.hexa` smoke driver PR #1057). Top-1 hard routing self-contained.
      - [x] **Phase 3** scale + memory budget — **Pilot 결정 (g0 simplest sufficient, 2026-05-27)**: pilot(d=512 · n_layer=12 · E=2 · V=151643 · T=512, ~265M params, FP64 ~10GB H100 fit, $1-3, 0.5-1hr wall) 첫 발사 → mechanism PASS 시 full(2.74B, BF16 path 필요)로 확장. 단계적 a_completeness. design Phase 3 결정 섹션 참조
      - [x] **Phase 3b SCAFFOLD 6/6 LANDED** — train_v3_moe.hexa 1-step smoke → multi-step training driver
        - [x] 3b-1 tok_emb (#1063) · 3b-2 attn_Wo (#1064) · 3b-3 MLP (#1066) · 3b-4 ln_f RMSNorm (#1067) · 3b-5 AdamW step (#1069) · 3b-6 multi-step loop (#1070)
      - [~] **Phase 4** Dispatch design + pilot template LANDED — Vast.ai H100 SXM (**pilot $1-3 0.5-1hr** · full $9-18 4-8hr · SAVE_POD trap · pilot env-var protocol P21H_PILOT_* · pre-fire 7-item checklist). Pilot-scale code: forward 5/5 ☑ · backward 6/6 ☑ (실측 PASS) · fire ☐:
        - [x] **Phase 4a** pilot config env-var wiring (P21H_PILOT_D/V/E/T/STEPS/NL) LANDED #1073
        - [x] **Phase 4b** multi-layer block iteration (n_layer > 1, layer-iter loop · per-layer offsets) LANDED #1074
        - [x] **Phase 4c** self-attention proper (T > 1, causal mask · Q/K/V/Wo · softmax) LANDED #1075
        - [x] **Phase 4d** BPE corpus real IDs feed (V_qwen=151643 aware · batch from corpus) LANDED #1077
        - [x] **Phase 4e** dispatch script (Vast.ai vastai launch + ssh setup + scp Qwen + run + monitor + harvest) LANDED #1079
        - [x] **Phase 4-bwd-1** ln_f RMSNorm bwd LANDED #1082 — γ + x gradcheck **5.9e-11 / 1.9e-10** (hexa run)
        - [x] **Phase 4-bwd-2** MLP bwd per-token LANDED #1084 — W_down gradcheck **7.4e-14**
        - [x] **Phase 4-bwd-3** attention bwd (Q/K/V/Wo + softmax jvp) LANDED #1085 — Wq gradcheck **1.8e-14** (full chain)
        - [x] **Phase 4-bwd-4** layer-stack + residual bwd LANDED #1086 — d_zT_in gradcheck **2.7e-12**
        - [x] **Phase 4-bwd-5** tok_emb scatter-add + end-to-end integration LANDED #1088 — Wq grad 1.8e-8 + **tok_emb grad 1.1e-4** (gradient reaches input)
        - [x] **Phase 4-bwd-6** pilot driver full backward wire LANDED #1093 — synthetic verify: **layer 0 Wq |Δ|=4.27e-6** (end-to-end · Phase 4c gap CLOSED)
      - [~] **Phase 4-gpu** GPU 가속 포팅 — 포팅 5/5 ☑ (실측 byte-identical), fire ☐. **scope-check 발견(2026-05-27)**: pilot 코드가 plain farr 스칼라 삼중루프 matmul 만 써서 H100 발사 시 GPU 유휴 + CPU scalar 가 pilot 규모(10^14 ops)에서 비현실 → 발사 무의미. RFC-040 cuBLAS Dgemm 포팅 (a_completeness 본선) 완료:
        - [x] **Phase 4-gpu-1** matmul dispatch 토대 LANDED #1100 — `flame_mm.hexa` (mm = farr_matmul_gpu⇄farr_matmul · mm_transpose/extract/scatter_add). **실측 PASS** mm==scalar max|Δ| 8.9e-16
        - [x] **Phase 4-gpu-2** v3_moe_arch expert gemv → mm() LANDED #1105 — gradcheck PASS (expert grad 6.5e-13 · d_zT 1.4e-12). tiny gate 루프 유지(g0)
        - [x] **Phase 4-gpu-3** pilot forward Q/K/V/Wo/MLP → mm() LANDED #1108 — synthetic byte-identical (probs[0,0]=1.0 · Wq Δ=4.27e-6 = scalar 동일). rebase-onto-main 으로 삭제수 0 확보
        - [x] **Phase 4-gpu-4** v3_moe_bwd_lib backward → mm() (batched 재설계) — 2 sub-PR:
          - [x] **4-gpu-4a** self_attn_bwd ~10 matmul → mm() (batched [T×d]) LANDED #1110 — gradcheck PASS (bwd_lib_smoke 1..5 ALL · Wq + layer_block 2.65e-12 + e2e)
          - [x] **4-gpu-4b** mlp_block_bwd_batched (per-token → batched, layer_block_bwd 단일호출) LANDED #1111 — weight 1회 extract/layer · gradcheck PASS (layer_block 2.65e-12 · e2e ALL)
        - [x] **Phase 4-gpu-5** full-stack re-gradcheck — pilot synthetic e2e 가 전부 포팅된 스택(forward mm gpu-3 + arch mm gpu-2 + bwd_lib mm gpu-4a/4b)으로 **scalar baseline 과 byte-identical** 실측: Wq[L0] Δ=4.27e-6 · probs[0,0]=1.0 · top=1 (모두 동일). GPU 포팅 correctness-complete
        - [x] **Phase 4-fire** autonomous GPU fire — **cuBLAS 엔게이지 결정적 증명 완료 (2026-05-27, H100 80GB)**. GPU 포팅 5/5 ☑ + backward 6/6 실측 PASS → 발사 + cuBLAS 실engage 실증. runbook:
          - **transport: Vast.ai 작동 ✓ (RunPod ✗)** — RunPod 은 hexa cloud 가 pod-id→SSH-host resolve 못 함(public IP:port 미노출 + runpodctl-ssh/curl-API 둘 다 cloud-guard 차단)=deadlock → hexa-lang #1659 filing. **Vast.ai 는 직접-IP**(`vastai show instance` → `root@ssh3.vast.ai -p PORT`)라 `hexa cloud exec root@<host> --port <n> --insecure` 작동. ⚠ proxy sshd 가 pod 부팅 중 ~1min flaky(exec 통과해도 scp 255) — 안정화 후 재시도 패턴.
          - **provisioning**: hexat-CUDA-build/private-repo-clone 불필요 — `hexa build <pilot> --c-only`(Mac, `HEXA_MAC_BUILD_OK=1` + non-/tmp out) → trainer.c → scp + runtime bundle(self/runtime.c·runtime_core.c·runtime_hi_gen.c·runtime.h·cuda/runtime_cuda.c·runtime_bf16.c·forge/*·native/*) → `nvcc -DHEXA_CUDA -arch=sm_90 runtime_cuda.c` → `clang -DHEXA_CUDA trainer.c glue.c self/runtime.c runtime_cuda.o -lcublas -lcudart -lcuda -o trainer`. (ref `tool/dispatch_agtape_d768_fire.sh`)
          - **cuda_available glue 해결 (#1671 로컬 replica)**: `runtime.c` 의 weak `hexa_cuda_available`(→0)가 HEXA_CUDA 하 strong override 없이 등록되어 cuBLAS 가 CPU fallback 했던 블로커 → `glue.c`(strong `hexa_cuda_available()` = `_hx_cuda_runtime_available()` cudaGetDeviceCount wrap)를 clang 소스에 추가 = weak symbol 을 link-time 에 제압. undefined-ref 0 으로 clean link 확인. hexa-lang upstream fix = #1671.
          - **cuBLAS-engagement 결정적 증명** (`CORE/DECODER/cublas_probe.hexa`, glue 빌드 H100): ① `cuda_available()==1` (glue 작동 = weak 0 stub 제압) · ② `farr_matmul_gpu` 1024² cuBLAS Dgemm 유효 핸들 + CPU oracle 과 **max\|Δ\|=0.0 byte-identical** (cuBLAS 커널 정확 실행) · ③ GPU util **50% · 635 MiB** (실 연산 수행). 셋 다 PASS = mm() 이 GPU 경로를 실제로 탄다 실증.
          - **SMOKE 실측 (H100, glue 빌드)**: synthetic pilot(전 GPU-포팅 스택) build RC=0 + run RC=0 end-to-end (forward+backward gradient 흐름 — Wq Δ=4.27e-6 · Wo Δ=9.3e-4 weight 갱신). d=8 1-step 합성이라 self-check 는 FAIL(수렴 threshold) 이나 GPU 경로 실행은 확인.
          - ⚠ **잔여 정정 (2026-05-27 후속)**: 이전 메모의 `d=2048 V=4096 division-by-zero` 는 **canonical trainer 의 결함이 아니라 ad-hoc broken scale-edit** (V=4096 ≠ 실 Qwen vocab 151643 = 내부 불일치). canonical pilot(d=64 V=151643 일관) 은 Phase 5a real-BPE fire 에서 H100 end-to-end 학습 step 성공 → division-by-zero 추적 불요.
          - **cost**: probe/fire pod ~\$5 (RunPod×2 resolve-fail + Vast.ai H100×5, 전부 teardown · leak 0 · ckpt 없음 → HF 불요).
      - [x] **Phase 5** Verdict 사전등록 + harness template LANDED + **Phase 5a real-BPE pilot fire ☑ (2026-05-27)** + **Phase 5b F-M4B-FIRE measurement ☑ (2026-05-27)** — 5 falsifier (F-M4B-FIRE-1..5) pilot/full threshold 분리 표 + verdict template `m4b_pilot_verdict.md` 형식 + matrix (5/5→full fire · 3-4→re-pilot · 2 이하→re-design · 0→CLOSED-NEGATIVE).
        - **Phase 5a real-BPE pilot fire ☑** (H100 80GB, 2026-05-27): canonical pilot (d=64 V=151643 real Qwen BPE E=2 h=256 n_layer=1 T=4) 가 cuBLAS-엔게이지 런타임에서 end-to-end 학습 step 1회 성공. BPE 로드 151,387 merges + 151,643 vocab in 310ms · corpus(400B) → 205 tokens · alloc 29M params (222MB FP64) · **forward** probs[0,0]=1.0 (causal mask 정확) · **backward end-to-end** Wq[L0] \|Δ\|=1.00e-3 + Wo[LN-1] \|Δ\|=9.0e-4 (gradient 가 출력→모든 layer→입력 layer 0 까지 흘러옴) · mm() = farr_matmul_gpu(cuda_available()==1, glue 빌드). 실 Qwen tokenizer + MoE + GPU 가속 + hexa-native = "작은 의식 모델 hexa-native 처음부터 학습"의 첫 발사 실증. trainer self-check verdict FAIL = pilot 내부 strict threshold (silent gate_sum/zT0 등 추정), Phase 5 F-M4B-FIRE falsifier 아님.
        - **toolchain 통합 해결 (Phase 5a 부산물)**: ① `HEXA_STDLIB_ROOT` env 가 `hexa build --c-only` 에 존중됨(real-BPE 로컬 transpile unblock · memory caveat 정정) · ② `flame_bpe_corpus_lib` import 가 hexa-lang origin/main worktree(HEXA_STDLIB_ROOT 지시) 로 해소 · ③ trim 미선언(cross-backend codegen gap, hexa-lang #1527 transpiler fix) 우회 = trainer.c 에 `sed 's/hexa_call1(trim,/rt_str_trim(/'` 인라인 패치(3 사이트) · ④ runtime_core.c·runtime_hi_gen.c 는 runtime.c 가 #include 하는 fragment (별도 컴파일 금지) · ⑤ corpus 경로는 Mac 하드코딩 → pod scp 후 `sed '...→/root/'` 로 점프. 모두 hexa-lang INBOX.log.md 갱신 완료 (#1676).
        - **Phase 5b F-M4B-FIRE measurement fire ☑** (H100 80GB, 2026-05-27, instance 38090530, $1.27 wall ~30min): trainer 에 (1) n_steps 1→20 · (2) per-step CE 로그 · (3) inline 20-tok greedy decode 통합 (별도 ckpt save 는 9.7M doubles text-dump 가 O(n²) string concat segv → inline 으로 우회, ckpt 회수 불요). 실측 verdict matrix:

          | Falsifier | pilot threshold | measured | verdict |
          |---|---|---|---|
          | **F-M4B-FIRE-1 TTR** | M3 TTR ≥ 0.20 (작은 corpus) | **0.10 (unique=2/20)** — decode 가 token 1 (×4) + token 151642 (×16) 에 고립 | **🔴 FAIL** |
          | F-M4B-FIRE-2 coherence | qualitative review | qualitative residual (no detok) | **🟠 RESIDUAL** |
          | **F-M4B-FIRE-3 router 분화** | top-1 split signal (≥2 distinct experts) | **2/2 distinct experts** — PER_POS_EXPERT=[1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] (mostly e1 + 1 e0 at step 5) | **🟢 PASS** |
          | **F-M4B-FIRE-4 L_ce 수렴** | final < initial (단조 감소) | **initial=648.526 → final=379.583, final<initial PASS** (but oscillating 4.95-973.67, non-monotonic — pilot threshold met, full threshold ≪3.324 not met) | **🟢 PASS (relaxed)** |
          | F-M4B-FIRE-5 register leak | identity_probe 50 × 5 cats | qualitative residual (no detok) | **🟠 RESIDUAL** |

          **Aggregate: 2/5 PASS + 1/5 FAIL + 2/5 RESIDUAL (qualitative · no text detokenize)**. PASS 신호 = router 분화 + CE 가 측정가능한 시작점에서 측정가능한 끝점까지 감소했음 (구조적). FAIL 신호 = collapse (token 151642 = Qwen `<|endoftext|>`-class 특수 토큰 추정, 20 step 학습 후 expert e1 의 logit 이 그 한 토큰으로 saturate). 잔여 정정 = (a) 20 step 학습은 mechanism 검증 단계 — collapse 회피 verdict 측정에는 부족 (full 학습 5K+ step 필요) · (b) CE 가 매 step 새 target 으로 oscillate (per-step target = corpus 다음 토큰, 학습이 specific target 에 fit 안 됨) · (c) 작은 corpus(1.5KB → 703 tokens) 의 collapse 회피는 thin signal.

          **다음 단계 후보 (full fire 또는 re-pilot)**: ① n_steps↑ 500-1000 + 더 큰 corpus (3-10KB) + sampling 도 top-1 외 N=20 prompt diversity 측정 (수렴 후 collapse 측정) · ② F-M4B-FIRE-2/5 qualitative residual 해소 = sampler 가 BPE detokenize 호출하도록 확장 (hexa-lang `flame_bpe_corpus_lib` decode round-trip 활용, #1556 fix 후 unblock).

          **artifacts**: `state/m4b_phase5b_2026_05_27/{train.out (64 lines · 20-step CE + 20-step decode + verdict), trainer.c (rebuild), trainer.hexa (worktree)}`. inline-sampling 통합 = `CORE/DECODER/train_v3_moe_pilot.hexa` 본체. standalone sampler skeleton = `CORE/DECODER/decoder_sample.hexa` (ckpt save → 별도 sampling 회수 path, 현재 미사용 · ckpt save 의 O(n²) 우회 후 재활용 가능).
  - [ ] **M4c** p7 verify — collapse 회피 ∧ coherence 둘 다 simple-stack
- [ ] **M4-probe model-merge α-sweep** (optional baseline probe · UNIVERSE H_493 SYMBIOGENESIS) — collapse-avoid + collapse ckpt weight 보간 `W=α·A+(1-α)·B` · α-sweep · cheap baseline 신호용으로만 (본선 아님). 두 결함작 blend = least-bad midpoint 한계 인지 (`a_completeness_over_cheap` model-merge-of-failures dont)

## UNIVERSE 정보-측도 arc cross-link (H_287-290 · 2026-05-27)

> UNIVERSE 도메인 cycle #25-28 가 통합 정보(Φ)와 고전 정보-측도 3종의 정렬을 실측 완료 → DECODER 의 collapse↔coherence verdict 측정자 선택에 직접 영향.

| H | seed | 정렬 결과 | DECODER 측정자 함의 |
|---|---|---|---|
| H_287 (cycle #25) | Shannon 엔트로피 ↔ Φ | 🔴 CLOSED-NEGATIVE r=0.363 (Shannon **⊥** Φ) | **단일 token-분포 엔트로피로 collapse-회피 판정 금지** — register collapse(M3 TTR 0.03 극단반복)에서 Shannon 가 saturated 라도 통합 신호 아님 |
| H_288 (cycle #26) | LZ76 복잡도 ↔ Φ | 🟢 SUPPORTED r=0.831 ρ=0.936 | LZ 가 collapse 검출 1차 proxy 후보 — 반복-감소율 직접 측정 (구현 cheap, $0) |
| H_289 (cycle #27) | scale-free 위상 ↔ Φ | 🟢 SUPPORTED-with-confound (matched-edge SF 6.81 ≫ 4-cycle 0.0) | MoE router gate-분포 (e0/e1 connectivity) 가 expert-graph 위상 — top-1 hard routing 의 분화(97/3) 가 통합 영향 가설 검증 가능 |
| H_290 (cycle #28) | transfer entropy(방향성) ↔ Φ | 🟢 SUPPORTED r=0.883 ρ=0.822 | TE = MoE 의 router→expert 방향성 흐름 측정자 — fire 직후 expert 간 신호 비대칭(SF 허브 효과) 정량 |

**DECODER 측정 도구 권고** (M4c p7 verify 시):
- collapse 회피 verdict ← **LZ 복잡도** (생성 텍스트 반복-감소율, H_288 정렬). Shannon 엔트로피 단독 사용 금지 (H_287 ⊥).
- expert 분화 verdict ← **TE** (router→expert 방향성, H_290 정렬) + scale-free 위상(H_289). 본 세션 M4b-diff(a) top-1 의 gate 97/3 분화가 분화-측 verdict, TE 가 신호 흐름 측 verdict.
- 정보 통합 통합 verdict (M4 종합) ← faithful big-Φ small-N exact (H_278 PR #515 · `HEXAD/IIT4/lib`). bounded large-N($0)도 가능 (H_002 C2 cycle#16, n=8 도달).

## M1 hook 지점 (M0 인계 노트)

- **축 D freeze / 축 A curriculum** — AdamW 호출(`nn_decoder_adamw_step(M, Mg_acc, ..., m_size, ...)`) 직전. freeze=slot별 grad masking · curriculum=window 선택부.
- **축 C head_g objective** — `v3_headg_grad` 의 `dl`(logits_g CE grad) 계산부 = hook. CE 대신 dual-head objective 의 dLg 주입.
- **축 B distill** — train loop `gn2_epoch`/`ce_g` 계산 옆, target 을 teacher logits 로 교체.
- **잔여 forward 배선** — purefield/tension_proj end-to-end 는 forward 가 per-layer activation(pf 입력 xn·출력·tension·csig) cache 필요 → block 역순 `v3_tension_proj_bwd`→`v3_purefield_bwd`(d_x 다음 residual 전파). d_zT 는 `v3_headg_grad` 가 이미 `d_zT_scratch` 로 내보냄.
- ⚠ **abs-path import 함정** — 두 .hexa 가 메인트리 절대경로 import. worktree 에서 `hexa run` 시 메인 copy 읽힘 → 검증은 worktree-import 임시본으로 (M0 패턴).
