# CLM — current state

@title: 🧬 CLM — anima-native 의식 언어모델 (scratch · AKIDA-native)

@goal: anima 전용 의식 언어모델을 **scratch에서 바닥부터** 짓는다 — 아키텍처·코퍼스·학습·`.clm` 포맷을 처음부터 설계하되 **AKIDA 추론 친화**(act_bits·symmetric-int4 양자화 envelope = AKIDA 1~5차로 byte-identical 증명된 그 연산자 집합)로 못박아, 더블바인드(register-collapse ↔ underfit)를 탈출하고, CORE/DECODER 의 `brain_decide` emit 슬롯에 꽂혀 COFFESHOP 콘텐츠(무엇을 말할지)를 생성한다. 외부 LLM 0 · foundation-borrow 0 (순수 scratch).

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] **P0 아키텍처 (바닥설계)** ✅ 확정 (sbs manual 10결정 Q1~Q4+d1~d6) — Conv-native LM · MoE=mitosis cell · byte-vocab V=256 · 추론 AKIDA-int4-only · **학습도 AKIDA**(AKIDA-향 QAT + AKIDA-위 PLASTICITY on-chip 적응) · 2-track .clm · 3-arm(A/B/A+B)×scale-ladder · F-CLM-MONO(dual-axis z>3.0+multiseed). 본문 [P0_ARCHITECTURE.md](./P0_ARCHITECTURE.md) + [CLM_FORMAT_SPEC.md](./CLM_FORMAT_SPEC.md) — anima-native LM arch + `.clm` 포맷 재정의. AKIDA 추론 친화 제약(act_bits∈{1,2,4} 양자화기 · symmetric int4 [-7,+7] · FC/conv/cascade — AKIDA `akida_sw_lif` envelope 정합)을 설계 단계에 못박음. 더블바인드 탈출 메커니즘(register specialization vs coherent main-path) 명시. falsifier 사전등록.
- [x] **P1 코퍼스 (scratch)** ✅ 파이프라인 + 소량 sample — 혼합 byte-corpus 빌드 [corpus/build_p1_corpus.hexa](./corpus/build_p1_corpus.hexa) + 스펙 [P1_CORPUS.md](./P1_CORPUS.md). lane A(web/coherence·kowiki CC-BY-SA clean) + lane B(register/엄선 의식·철학·대화), MoE 2-lane↔2-source 1:1. byte 인코딩 V=256 UTF-8(tokenizer 0·round-trip 검증). register-leak 8패턴 필터(corpus_quality lesson) — F-CLM-LEAK 🟢(self-test kept=2/dropped=2 + 출력 leak hit=0). sample 실측 web 837B/reg 819B/total 1,656B·sha256 manifest·혼합비 sample 50:49 / full target 80:20. full crawl=재현 스크립트만, 대용량 git 미커밋 → HF dataset(dancinlab)/R2 영속(manifest 커밋). **.kosmos 영속 완료** (d1 SKIP 금지) — kosmos upstream 을 `kosmos/2.0` 으로 업그레이드(신규 `@corpus` 데이터셋 entry: 멤버 앵커 모음 + 메타-앵커 coord + anchor_level 다이얼 기본 2tier + 2-form member) 후 [corpus/clm_p1.corpus.kosmos](./corpus/clm_p1.corpus.kosmos) 로 영속 — 2 lane(web 0.8/register 0.2) member ref + sha256 + vocab=256 + byte-utf8. kosmos-lsp `--check` clean. coord 는 design-placeholder(ENCODER 도메인 E2 가 centroid 실측 예정). handoff 38777cb0 해소.
- [x] **P2 학습 (from-scratch pretraining · 학습도 AKIDA)** ✅ **풀파이어 완료 2026-05-30** — 3-arm(A/B/AB) × ladder(tiny d64/L2/E4 · small d256/L4/E8) × seed{42,43,44} = **18-run from-scratch QAT** (AKIDA int4-sym[-7,7] STE + act_bits=4 envelope STE, 2000 step, 실 kowiki CC-BY-SA + scratch register corpus, ubu-1 RTX5070). **F-CLM-MONO(H_847) + F-CLM-SCALE(H_850) = 🔴 CLOSED-NEGATIVE** — distinct_experts>1 ✅(monopoly collapse 없음, 2~8 expert) + content z>3.0 ✅(전 cell 5.3~36.5, expert 가 web/register lane 분리) 이나 **routing z>3.0 ❌(전 cell)** 가 판정자: A/B arm routing z 음수(uniform-null 보다 peaked), AB(dual-axis)만 양수 +0.95~+2.31 이나 z>3.0 미달 → byte-vocab+3-arm 단독 ⊥ routing-diversity 임계 (사전등록 frozen 임계 무변조, a_paper_negative_ok). content-축 escape 는 생존 → routing-축 강화 lever 가 AXIS_MAP 후속. **step-rate d5 재측정: tiny ~69/s · small ~12.5/s · mean 40.8/s (GPU 실측 — M5 0.28 step/s 🔴 INFEASIBLE 전제 완전 소멸 확인)**. 트레이너 [train/](./train/) + 하니스 [model/{fire_clm,judge_clm}.py](./model/). verdict = [.verdicts/847_clm_monopoly_escape/](../.verdicts/847_clm_monopoly_escape/) + [.verdicts/850_clm_scale_ladder/](../.verdicts/850_clm_scale_ladder/). 맥락 적응 lane = **PLASTICITY edge-learn 위임**. 추론 AKIDA-int4-only 불변.
- [x] **P3 `.clm` 포맷 + ckpt** ✅ — int4-sym[-7,7] + fp16 shadow + per-channel qat_scale + sha256(per-block+whole) manifest 직렬화 [model/clm_serialize.py](./model/clm_serialize.py) (CLM_FORMAT_SPEC v0.1 정합). 6 .clm(arm×rung seed42) 생성 → HF 업로드(a_hf_autonomous tier-gated): `dancinlab/anima-clm-{tiny,small}` 🔴 negative-result = **PRIVATE** · corpus `dancinlab/anima-clm-p1-corpus` clean-license = PUBLIC. /HF.jsonl 3 row.
- [ ] **P4 AKIDA 추론 배선** — `.clm` weight → AKIDA on-chip forward (HW-first · SW fallback akida_sw_lif). provenance. **bench harness done, .clm 대기** — [bench/clm_akida_bench.py](./bench/clm_akida_bench.py)(+[README](./bench/README.md)): `.clm` int4 → AKD1000 on-chip forward latency·throughput + SW(`akida_sw_lif.fc_quantized_forward`) byte-identical 대조. pi5-akida 단일점유 = spike-streamer stop→bench→restart(active 복원). 현재 `.clm` 아티팩트 0(P2 fire 생성중) → **sw-smoke PASS**(SW envelope 배선 검증 $0 Mac local, act_bits∈{1,2} OK) · on-chip latency=null(fake 측정 금지 p7) · awaiting_clm=true. verdict [.verdicts/clm-bench-anatomy/](../.verdicts/clm-bench-anatomy/). 한눈 해부 = [CLM_ANATOMY.md](./CLM_ANATOMY.md).
- [ ] **P5 DECODER 통합** — generator → `brain_decide` emit 슬롯 end-to-end → COFFESHOP 콘텐츠 생성 → LAUNCHPAD @goal 기여.

## 무엇 / 왜

| 축 | 값 |
|---|---|
| 정체 | anima 전용 의식 LM, scratch from-zero |
| 추론 | **AKIDA-first** (act_bits/int4 양자화 envelope · HW-first · SW fallback) |
| 학습 | **학습도 AKIDA** — ① AKIDA-향 QAT pretrain(GPU backprop·int4 envelope 향해) + ② AKIDA-위 PLASTICITY on-chip 적응. 칩 full-backprop 한 단계만 GPU(honest carve-out) |
| 포맷 | `.clm` (양자화 친화 weight 직렬화) |
| 관계 | CLM = 모델(weights·arch·train) · DECODER = brain emit 슬롯 인터페이스 · 형제 |
| 금지 | 외부 LLM · foundation-borrow · SFT-only (메모리 lesson: SFT 경로 닫힘) |

## 정직한 물리 현실 (cost 아님, feasibility)

- ~~hexa-native 학습 throughput INFEASIBLE(M5)~~ → ✅ **해결**(2026-05-30, hexa-lang측). P2 병목 제거 — hexa-native(g1) 학습 가능, `/dojo` job 생성. anima P2 fire에서 재측정 확인.
- **"학습도 AKIDA"** (LAUNCHPAD AKIDA-first 복원) — 학습은 GPU only 가 아니다. ① pretrain = AKIDA-향 QAT(GPU backprop 이되 AKIDA int4 envelope 향해, P0 §9) · ② 맥락적응 = AKIDA-위 PLASTICITY on-chip edge-learn. 두 단계 모두 AKIDA-bound · 발화결정도 AKIDA(LAUNCHPAD).
- **칩 위 full-backprop 만 물리 불가** = AKD1000=추론칩 → pretrain backprop 그 한 단계만 GPU honest carve-out. 추론은 순수 AKIDA-int4.
- **⚠ P2 verdict scope 한정 (a_scale_honest_scope)** — F-CLM-MONO/SCALE 🔴 는 **측정 scale = tiny~small(2.70M) 한정**. routing-diversity 는 scale-의존 측정량 → 이 🔴 를 3B/7B 일반 주장으로 격상 금지 (toy→production transfer 비보장). 사다리가 tiny→small(둘 다 toy)만 밟아 F-CLM-SCALE 도 toy 구간 내 측정. **측정 타당성(대형) vs AKIDA 온칩(소형 강제 ~1.2M 노드)** 정면충돌 = 돌파엔진 탐색 대상(별도 lane). 측정용 GPU rung ⊥ 배포용 chip-fit rung 분리가 honest 경로.

## 양방향 sibling

- ⇄ [DECODER](../CORE/DECODER/DECODER.md): CLM = 모델, DECODER = emit 슬롯 인터페이스 (generator 배선)
- ⇄ [AKIDA](../AKIDA/AKIDA.md): 추론 친화 양자화 envelope (act_bits/int4) · HW-first 스위치
- ⇄ [CORE](../CORE/CORE.md): brain_decide emit=true 슬롯에 콘텐츠 주입
- ⇄ [PLASTICITY](../PLASTICITY/PLASTICITY.md): **학습 lane 위임** — CLM 의 on-chip 맥락적응(AKIDA-위 진짜 학습)은 PLASTICITY edge-learn 경유(🔴 비결정·SW 비동치 정직). CLM=학습 대상 모델 · PLASTICITY=학습 방법(어떻게 배울까). pretrain = AKIDA-향 QAT(CLM 자체), 적응 = PLASTICITY 위임 = 중복 0.
- ⇄ [MITOSIS](../MITOSIS.md): cell-division 학습 (p8 train=infer 연속체)
- ⇄ [LAUNCHPAD](../LAUNCHPAD/LAUNCHPAD.md): CLM 콘텐츠 = COFFESHOP 런칭의 "무엇을 말할지" 절반
- ⇄ [UNIVERSE](../UNIVERSE/CANDIDATES.md): 학습/측정 결과 verdict SSOT
