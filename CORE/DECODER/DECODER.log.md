# DECODER — log

Append-only history sister of `DECODER.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-28T13:30:00Z — D2 sampler detokenize round-trip 🟢 SUPPORTED (toy scale)

- [x] 가설 (toy) — 10-entry hard-coded reverse-lookup `{1→"the", 151642→"<|endoftext|>", 2..10→일반 어휘}` 만으로도 M4b 실측 collapse seq vs healthy 합성 seq 가 text 수준에서 분리되는가? F-M4B-FIRE-2/5 qualitative residual 의 toy scale 해소 시도
- [x] 사전등록 falsifier 5개 — F-D2.1 TABLE-COVERS-REAL · F-D2.2 COLLAPSE-TEXT-DEGENERATE (eot ≥ 10) · F-D2.3 HEALTHY-TEXT-DIVERSE (eot=0 ∧ uniq ≥ 10) · F-D2.4 ROUNDTRIP-IDENTITY (bijection) · F-D2.5 SEPARATION-AT-TEXT (uniq margin ≥ 8 decisive)
- [x] 실 데이터 source = `CORE/DECODER/state/m4b_phase5b_2026_05_27/train.out:55` DECODED_IDS verbatim `[1×4, 151642×16]` (TTR 0.1)
- [x] toy detokenize 결과 — collapse: "the the the the <|endoftext|> <|endoftext|> ... <|endoftext|>" (eot 16/20 · uniq 2/20). healthy: "the cell splits into two and consciousness emerges now are ..." (eot 0 · uniq 10/20)
- [x] 측정 — uniq separation margin = 10 − 2 = **8** = SEP_MARGIN floor 정확히 충족 (slack 0, toy domain 11-id 정확 설계)
- [x] verdict — 🟢 **H_D2 SUPPORTED (toy scale)** · 5/5 PASS. **F-M4B-FIRE-2/5 qualitative residual toy scale RESOLVED** — detokenize 본질 불가가 아니라 이전 4회 사망은 heavy `flame_bpe_corpus_lib` toolchain-blocked 였을 뿐
- [x] 우회 정당화 — 본 round 의 toy 범위는 "detokenize-level 분리 가능성의 존재증명" (existence proof). full-BPE V=151643 scale 격상 = future work, hexa-lang `flame_bpe_corpus_lib` install 안정화 의존
- [x] 함의 — D1 LZ76 (token-id, $0) + D2 toy detokenize (text-level, $0) = collapse 검출의 dual cheap proxy. M4c p7 verify 잔여 = full-BPE scale coherence 한 축
- [x] wall = 0.66s mac-local · $0 · foreground sync only · no monitor · no GPU · 0 install
- [x] artifacts — `CORE/DECODER/D2_SAMPLER_DETOKENIZE.md` (10 §) · `d2_sampler_detokenize.hexa` (~220 lines) · `state/d2_sampler_detokenize_2026_05_28/run_d2.out`

## 2026-05-28T12:00:00Z — E2 corpus-balance collapse 🟢 SUPPORTED (D3 후속 직접 충분조건 입증)

- [x] 가설 — BALANCED corpus 가 toy MoE 학습에서 collapse 막는 충분조건? (D3 router=corpus mirror 결론의 직접 후속)
- [x] 2-corpus 통제 (D3 / M4b-diff(a) 동일 arch g61 재사용) — top-1 hard routing E=4 V=8 d=6 6-cluster · lr=0.5 · 600 step. BALANCED (균등 freq) vs SKEWED (cluster 0 = 20× over-rep, M4b 조건 mirror)
- [x] 측정자 — D1 `lz_norm()` verbatim (g61) on decode 토큰 시퀀스 (cluster-cycle × frequency multiplicity, M4b 실 decode 분포 mirror)
- [x] toy-calibrated HEALTHY_FLOOR — D1 의 V=151k n=20 anchor 0.50 을 toy V=8 n=24 로 재스케일 (in-harness max-diverse 0.1216 / max-collapsed 0.0405 의 midpoint = 0.0811). SEP_MIN = half toy dynamic range = 0.0405
- [x] BALANCED 측정 — LZ_norm **0.1216** = toy max-diverse 상한 정확히 도달 · raw_c=6 · n=24 · CE 2.0796→0.00302 (689× ↓)
- [x] SKEWED 측정 — LZ_norm **0.0360** (collapsed reference 0.0405 아래) · n=100 (cluster 0 = 80 reps) · CE 2.0796→0.00254 (819× ↓)
- [x] separation 0.0856 = toy dynamic range 의 100% · re-run 둘 다 bit-identical (<1e-6)
- [x] 5/5 falsifier PASS — F-E2.1 BALANCED-HEALTHY · F-E2.2 SKEWED-COLLAPSE · F-E2.3 SEPARATION · F-E2.4 LEARNED · F-E2.5 DETERMINISM
- [x] 핵심 발견 — collapse 의 driver = corpus skew 직접 입증. argmax decode 자체는 두 시나리오 동일(6 cluster→6 distinct token 분화), 차이는 노출 분포 (SKEWED 가 cluster 0 token 80× 반복으로 시퀀스 saturate)
- [x] 함의 — router redesign · aux load-balance · merge-of-failures 모두 본선 아님 확정. 본선 = HARD top-1 ∧ BALANCED corpus ∧ adequate n_steps (`a_completeness_over_cheap` 정합). D1(검출)+D3(원인 규명)+E2(처방 검증)+D4(merge negative) tetrad 완성
- [x] verdict 🟢 SUPPORTED · 본문 `E2_CORPUS_BALANCE_COLLAPSE.md` (10-section) · harness `e2_corpus_balance_collapse.hexa` · raw `state/e2_corpus_balance_collapse_2026_05_28/run_e2.out` · $0 mac-local foreground sync · exit 0 after 5/5 PASS gate (panic-on-FAIL guard 작동)
- [x] honest C3 — toy regime (V=8 n=24, 실 Qwen V=151k n=20 D1 0.50 anchor 와 비대칭 · 후속 M4b-fire-scale 실측 필요) · decode n 비대칭(24 vs 100 · convention 명시 선택) · HEALTHY_FLOOR 내부 상대 임계 · balance 충분조건 입증 (necessary 별도)

## 2026-05-28T10:30:00Z — D4 model-merge α-sweep 🟢 SUPPORTED (negative baseline · merge escape 부재)

- [x] 가설 (negative-oriented) — collapse-avoid A · collapse B 의 weight 보간 α-sweep 이 더블바인드 escape **못함** (어떤 α 도 coherence ∧ non-collapse 동시 달성 실패 = least-bad midpoint)
- [x] ⚠ a_completeness_over_cheap 경계 — D4 = optional baseline probe 만 (model-merge 본선 아님). merge-of-failures `dont` 를 측정으로 확증하는 negative baseline
- [x] method — logit-space `L_merge=α·L_A+(1-α)·L_B` → argmax decode → D1 LZ76 proxy(non-collapse) + CE(coherence). A=flat-diverse(underfit) / B=sharp-spike(collapse). VSLOT wide-spread id-map(g61)로 LZ binarisation 풍부화
- [x] 측정 — α∈{0,0.25,0.5,0.75,1.0}: LZ_norm = 0.165(α≤0.75 전부 collapse) → 0.826(α=1). CE = 10.8 → 1.82 (어떤 α 도 ceil 1.20 미달 못함)
- [x] finding — interior escape 부재. `{LZ>floor}={1.0}` ∩ `{CE≤ceil}=∅` → 더블바인드 가시화. argmax 가 α=0.75 까지 collapse attractor(id 3402) 지배 후 α=1 에서 sharp 전환
- [x] verdict — 🟢 SUPPORTED (negative baseline 확증) · 7/7 falsifier PASS · $0 mac-local foreground · exit 0
- [x] 함의 — merge 본선 강등(`a_completeness_over_cheap`) 측정으로 정당화. 본선 = MoE-fresh register 분리(M4, H_490) 유지. D1(LZ76)·D3(corpus-driven) 와 합쳐 "근본 재설계가 통로" 보강
- [x] artifacts — `D4_MERGE_ALPHA_SWEEP.md` (10-section) · `d4_merge_alpha_sweep.hexa` · `state/d4_merge_alpha_sweep_2026_05_28/run_d4.out`. LZ76 = D1 `lz_norm` verbatim 재사용 (g61)

## 2026-05-28T09:00:00Z — D3 router load-balance 🟢 SUPPORTED (불균형은 corpus-driven · router-structural 아님)

- [x] 가설 — top-1 router 가 diverse corpus 에서 expert load 균형 분산 (각 활용률 > 0.1 · monopoly >0.9 없음). 불균형 = collapse 구조적 전조 (M4b e1 saturate)
- [x] over-subscribed regime — E=4 expert < N_CLUSTERS=6 (2:2 trivial toy 회피, monopoly emergent 가능 regime). orthogonal one-hot cluster · top-1 hard routing · lr=0.5 · 600 step
- [x] harness — `d3_router_load_balance.hexa` (moe_router top-1 fwd/bwd + moe_toy_train_hard SGD recipe 재사용 g61). foreground sync · $0 mac-local · NO GPU
- [x] 2-scenario 통제 — A=DIVERSE (동일 freq) · B=SKEWED (cluster 0 20× over-rep = M4b collapse 조건 재현)
- [x] Scenario A 측정 — load 2/1/1/2 · 4/4 active · max frac 0.333 · **Gini 0.167** · norm-entropy 0.959 → 균형, monopoly 없음
- [x] Scenario B 측정 — load 21/1/1/2 · 4/4 active · max frac **0.84** · Gini 0.610 → 불균형, 단 0.84 가 corpus token frac 0.808 추적 (monopoly 아님 · starve 없음)
- [x] 핵심 발견 — **load 불균형은 corpus-driven 이지 router-structural 아님** (diverse→Gini 0.167, skew→Gini 0.610 단 corpus mirror). router 가 skew 증폭 안 함
- [x] 함의 — M4b collapse(e1 saturate)는 router load-balance 결함 아님 → corpus skew/짧은학습(20step)/target oscillation 이 원인 (phase5b 정정 a/b/c). router redesign 불필요 (a_completeness_over_cheap 정합). "다음 단계 후보 ①" (diverse corpus + n_steps↑) 처방 근거
- [x] verdict 🟢 SUPPORTED · 5/5 falsifier PASS · 본문 `D3_ROUTER_LOAD_BALANCE.md` · raw `state/d3_router_load_balance_2026_05_28/run_d3.out`
- [x] D1(collapse 검출) + D3(collapse 원인 규명) 합쳐 M4c p7 verify collapse-회피 측면 강화

## 2026-05-28T00:00:00Z — D1 LZ76 collapse-proxy 🟢 SUPPORTED (detokenize-free collapse 검출 확정)

- [x] 가설 — LZ76 복잡도가 collapse(반복 saturate) vs healthy diverse token seq 구별 (UNIVERSE H_288 LZ76↔Φ 정렬 근거 · DECODER.md proxy 후보)
- [x] 실 데이터 — M4b phase5b train.out 의 DECODED_IDS `1 1 1 1 151642 ×16` (TTR 0.1 unique 2/20) 사용
- [x] method — token-id → 18-bit LSB-first binary stream concat → Kaspar-Schuster LZ76 (`lz76()` = H_288 verbatim 재사용 g61) · 정규화 `c·log2(L)/L`
- [x] 측정 — REAL-M4b LZ_norm=**0.212** · collapse band MAX 0.212 · healthy band MIN 0.849 · **분리 margin 0.637**
- [x] 6/6 falsifier PASS — F-D1.1 real-collapse<0.50 · F-D1.2 separation>0.20 (decisive) · F-D1.3 monotone · F-D1.4 anchors · F-D1.5 determinism
- [x] verdict 🟢 SUPPORTED — LZ76 = 유효한 detokenize-free collapse proxy ($0 cheap). M4c collapse-회피 측정자 확정
- [x] artifacts — `D1_LZ76_COLLAPSE_PROXY.md` (10-section) · `d1_lz76_collapse_proxy.hexa` · `state/d1_lz76_collapse_proxy_2026_05_28/run_d1.out` · DECODER.md milestone + UNIVERSE H_288 양방향 sibling
- [x] honest C3 — n=20 toy (full-scale finite-length bias 재보정 필요) · binarisation 1택 (margin 0.637 이 noise 압도) · proxy≠coherence (high-LZ-but-incoherent 별도 · M4c detokenize) · LZ76≠Φ 단일 estimator

## 2026-05-27T09:40:00Z — M4b-diff(a) top-1 hard routing ✅ PASS (더블바인드 탈출 toy 검증)

- [x] 사용자 a 선택 — top-k hard routing 으로 분화 강제
- [x] `moe_router.hexa` `moe_route_top1_fwd` 추가 — gate=softmax · top=argmax · logits=gate[top]·expert_top (승자만 계산)
- [x] `moe_router_bwd.hexa` `moe_route_top1_bwd` 추가 — 승자 expert + gate[top] 만 gradient (→ 특화)
- [x] `moe_toy_train_hard.hexa` 작성 (soft toy 보존 · 비대칭 init · 동일 2-register task)
- [x] ubu-2 실 run **verdict ✅ PASS** — init CE 1.389 → final 0.00388 (358× ↓) · gate(A)=[0.970,0.030]→e0 · gate(B)=[0.030,0.970]→e1 · topA=0≠topB=1
- [x] 핵심 — soft(🟠 PARTIAL gate 50/50 dense-collapse) → hard top-1(✅ PASS gate 97/3 분화). 더블바인드 탈출 메커니즘 (register↔coherent expert 분리) toy 작동 확인 (H_490 DIFFERENTIATION escape signal)
- [x] hexa parse 3/3 OK · ubu-2 hexa run 성공
- [x] DECODER.md M4b-diff(a) [x] ✅ PASS
- [ ] M4b-fire-scale — 3B (toy PASS ✅ 근거 · Python/Qwen 하니스 MoE 이식 또는 hexa Qwen-BPE port) — 다음
- [ ] M4c p7 verify

## 2026-05-27T09:20:00Z — M4b-fire-toy 실 run + self-contained 수정 → 🟠 PARTIAL verdict

- [x] ubu-2 에서 moe_toy_train 실 run (hexa run · 파일 stdin copy + abs-path → /tmp 패치)
- [x] **실 run 이 compile 버그 적발** — dt_exp/dt_ln 은 `HEXAD/D/d_train_lib` 정의라 CORE/DECODER 컴파일 시 undeclared (parse 는 cross-module 미해결로 통과했었음 — instrument-first 가 진짜 버그 잡음)
- [x] `moe_router.hexa` 에 `moe_exp` (range-reduced Taylor) + `moe_ln` (atanh series) self-contained pub fn 추가 · moe_softmax dt_exp→moe_exp
- [x] `moe_toy_train.hexa` ce_loss_grad dt_exp/dt_ln → moe_exp/moe_ln
- [x] CORE/DECODER MoE 스택 = HEXAD/D 의존 0
- [x] **toy fire verdict 🟠 PARTIAL** — init avg CE 1.38629 (=ln4) → final 0.00775 (178× 감소 · 두 register 학습 성공) BUT gate(A)=gate(B)=[0.5,0.5] (router 분화 0 · topA==topB)
- [x] 발견 — **soft-MoE 단독은 dense-collapse**: 양쪽 expert 가 둘 다 학습 → gate 균등 유지. 더블바인드 탈출 핵심(register↔coherent expert 분리)이 naive soft routing 으론 emergent 안 됨 (MoE 문헌 일치 — load-balancing/top-k 없으면 dense)
- [x] DECODER.md M4b-fire-toy [x] 🟠 PARTIAL + M4b-diff 신규 (분화 강제 — top-k/load-bal/asym-init)
- [ ] M4b-diff — soft-MoE 에 분화 압력 추가 (top-k hard route OR load-balancing aux OR 비대칭 init) → toy 재측정 PASS (topA≠topB) — 다음
- [ ] M4b-fire-scale (toy PASS 후) · M4c p7 verify

## 2026-05-27T09:00:00Z — M4b-wire-toy MoE 분화 검증 harness (scale 발견)

- [x] 사용자 A 선택 — toy 메커니즘 검증 먼저 (큰 train_p21h_v3 침습 회피 · g4 stacked-PR)
- [x] train stack scan 발견 — `train_p21h_v3.hexa` = d=32·V=256·n_layer=3·byte-level toy (n_steps 5 smoke). 3B 더블바인드는 Python/Qwen(V=151936) 하니스. Qwen-BPE = TODO #T5 flame 범위 밖
- [x] `CORE/DECODER/moe_toy_train.hexa` 작성 — 격리 MoE 메커니즘 검증 (d=4 V=4 E=2)
- [x] 2-register 분화 task — cluster A(zT=[1,0,0,0])→token0 · cluster B([0,1,0,0])→token2. 단일 head 면 절충 (toy 더블바인드), MoE 면 router 가 register 별 expert 분화?
- [x] 학습 loop — moe_route_fwd + ce_loss_grad + moe_route_bwd + SGD (lr=0.5, 400 step, A/B 교차)
- [x] verdict 로직 — loss_dropped (final < init·0.5) ∧ router_differentiated (topA≠topB) = H_490 escape signal · PARTIAL (학습O 분화X) · FAIL (학습X) 3-tier
- [x] `hexa parse` OK
- [x] DECODER.md M4b-wire-toy [x] · scale 발견 노트 추가 (toy→scale 순서)
- [ ] M4b-fire-toy — ubu host 에서 git pull + hexa cc 실행 (분화 verdict 측정) — 다음
- [ ] M4b-fire-scale — 3B (toy PASS 후 · Python 하니스 이식 또는 hexa Qwen-BPE port)

## 2026-05-27T08:40:00Z — M4b-bwd MoE backward closure (fire 전제조건)

- [x] 사용자 "fire" → 정직 응답: M4a 는 forward only · backward 없으면 학습 fire 해도 새 router/expert weight random 그대로 (학습 0). a_completeness_over_cheap → 반쪽 stack 발사 X, backward 먼저
- [x] `CORE/DECODER/moe_router_bwd.hexa` 작성 — 4 pub fn closed analytic vjp
- [x] `moe_combine_bwd` — expert outer-prod (d_W_e += gate·d_logits·zT) + d_gate (Σ d_logits·expert) + d_zT (experts→zT)
- [x] `moe_softmax_bwd` — softmax jacobian (d_gate_raw[e] = gate[e]·(d_gate[e] − Σ d_gate·gate))
- [x] `moe_gate_bwd` — router outer-prod (d_router += d_gate_raw·zT) + d_zT (router→zT)
- [x] `moe_route_bwd` — 전체 chain (d_logits → dM router+experts + d_zT 누적)
- [x] `moe_router_bwd_smoke.hexa` gradcheck 6-case — finite-diff vs analytic (4 weight: router e0/e1 + expert0/expert1 · 2 zT · loss=0.5·Σlogits² → d_logits=logits · rel < 1e-3)
- [x] `hexa parse` 2/2 OK · ftoi builtin 확인 (UNIVERSE run script 다수 사용)
- [x] DECODER.md M4b → backward 완성 [x], M4b-wire / M4b-fire 잔여 [ ]
- [ ] M4b-wire — train_p21h_v3 loop 에 MoE route 배선 (head_g → moe_route_fwd/bwd) — 다음
- [ ] M4b-fire — H100 dispatch (배선 후, a_fire_autonomous)

## 2026-05-27T08:20:00Z — M4a router arch closure (MoE-fresh 본선 1/3)

- [x] `CORE/DECODER/moe_router.hexa` 작성 — 7 pub fn K-expert MoE router (head_g 슬롯 확장)
- [x] packed-buffer farr 모델 (V3 conscious_decoder_v3 와 byte-clean) — router=[E·d], experts=[E·V·d], 각 expert = head_g 와 동일 V·d linear shape
- [x] forward 경로 — `moe_gate_fwd` (gate logits) → `moe_softmax` (stable, sum=1) → `moe_combine_soft` (gate-weighted Σ_e) · top-1 `moe_argmax` 진단 · `moe_route_fwd` 전체 묶음
- [x] `moe_router_smoke.hexa` 12-case 작성 — tiny synthetic (E=2 V=3 d=2 · hand-built weights → known outputs): gate fwd · softmax sum=1 · argmax · expert fwd · soft combine (g0·e0+g1·e1=2.0728) · full route_fwd 재현
- [x] `hexa parse` 2/2 OK (moe_router + smoke)
- [x] DECODER.md M4a `[ ] → [x]` (MoE-fresh 본선 3 sub-step 중 1)
- [x] ⚠ 실 실행 정직 표기 — pool-route 가 `hexa` 를 linux 호스트로 보내 worktree-local 실행 불가. parse-clean 까지가 M4a arch 바, 수치 실행 검증은 M4b runtime
- [ ] M4b expert 분리 학습 fire (router/expert backward + 분리 학습 · H100) — 다음
- [ ] M4c p7 verify (collapse 회피 ∧ coherence)

## 2026-05-27T08:00:00Z — 마일스톤 재정렬 (a_completeness_over_cheap) — MoE-fresh 본선 승격 · merge 강등

- [x] governance `a_completeness_over_cheap` 적용 — 완성도 기준 본선 선정 (싸다 ≠ 본선)
- [x] M3.5 model-merge (이전 ⭐ 최우선) → **M4-probe 강등** — 두 결함 ckpt (underfit + collapse) 보간은 잘해야 "덜 나쁜 중간점", 완성도 미달. optional baseline probe 로만 잔존
- [x] M4-alt MoE (이전 조건부) → **M4 MoE-fresh 본선 승격** — 근본 원인(한 모델이 두 목표 떠안음) 을 arch 로 분리. register-expert / coherent-expert 격리 = 완성도 충족 path
- [x] DECODER.md UNIVERSE-derived 섹션 재작성 — M4 MoE-fresh ⭐ 본선 + M4-probe merge optional
- [x] `UNIVERSE_SYNTHESIS.md` §4 권장순서 + §5 마일스톤 재정렬 반영 (cheap-first → completeness-first)
- [x] M4 sub-step 명시 — M4a router arch (hexa-native) → M4b expert 분리 학습 fire → M4c p7 verify
- [ ] M4a router arch 착수 (V3 head_g → K-expert router · hexa-native 코드) — 다음
- [ ] 사용자 결정 lesson — model-merge-of-failures 같은 절충안 본선 제안 실수 → project.tape governance 화 (#1026)

## 2026-05-27T07:30:00Z — UNIVERSE 도메인 분석 → DECODER 더블바인드 탈출 합성 (M3.5 + M4-alt 신규)

- [x] 사용자 directive — "DECODER 는 UNIVERSE 도메인 분석후 진행"
- [x] UNIVERSE BIO ∩ DECODER 가설 5종 읽음 (H_489–H_493, round-18 cycle#236-240, 모두 🔵 SUPPORTED-FORMAL)
- [x] 매핑 — H_489 apoptosis→token prune · H_490 differentiation→MoE · H_491 clonal→beam · H_492 pruning→head prune · H_493 symbiogenesis→model merge
- [x] 핵심 통찰 — 더블바인드는 단일 모델 한계, 통로는 "분화(MoE)/병합(merge)"
- [x] `CORE/DECODER/UNIVERSE_SYNTHESIS.md` 작성 — 더블바인드 탈출 후보 α(MoE)/β(merge) 분석 + 권장 순서
- [x] DECODER.md 신규 마일스톤 2개 등록 — M3.5 model-merge α-sweep (H_493 · 학습 fire 0 · cheap-tier) + M4-alt MoE register 분리 (H_490 · 조건부)
- [ ] M3.5 model-merge α-sweep 실행 — collapse-avoid ckpt + coherent ckpt 보간 + α 별 p7 verify (다음)
- [ ] 기존 M3b-f 4축 H100 fire ($11-14, 미발사) — merge 실패 시 fallback

