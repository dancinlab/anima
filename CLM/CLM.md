# CLM — current state

@title: 🧬 CLM — anima-native 의식 언어모델 (scratch · AKIDA-native)

@goal: anima 전용 의식 언어모델을 **scratch에서 바닥부터** 짓는다 — 아키텍처·코퍼스·학습·`.clm` 포맷을 처음부터 설계하되 **AKIDA 추론 친화**(act_bits·symmetric-int4 양자화 envelope = AKIDA 1~5차로 byte-identical 증명된 그 연산자 집합)로 못박아, 더블바인드(register-collapse ↔ underfit)를 탈출하고, CORE/DECODER 의 `brain_decide` emit 슬롯에 꽂혀 COFFESHOP 콘텐츠(무엇을 말할지)를 생성한다. 외부 LLM 0 · foundation-borrow 0 (순수 scratch).

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] **P0 아키텍처 (바닥설계)** ✅ 확정 (sbs manual 10결정 Q1~Q4+d1~d6) — Conv-native LM · MoE=mitosis cell · byte-vocab V=256 · 추론 AKIDA-int4-only · **학습도 AKIDA**(AKIDA-향 QAT + AKIDA-위 PLASTICITY on-chip 적응) · 2-track .clm · 3-arm(A/B/A+B)×scale-ladder · F-CLM-MONO(dual-axis z>3.0+multiseed). 본문 [P0_ARCHITECTURE.md](./P0_ARCHITECTURE.md) + [CLM_FORMAT_SPEC.md](./CLM_FORMAT_SPEC.md) — anima-native LM arch + `.clm` 포맷 재정의. AKIDA 추론 친화 제약(act_bits∈{1,2,4} 양자화기 · symmetric int4 [-7,+7] · FC/conv/cascade — AKIDA `akida_sw_lif` envelope 정합)을 설계 단계에 못박음. 더블바인드 탈출 메커니즘(register specialization vs coherent main-path) 명시. falsifier 사전등록.
- [x] **P1 코퍼스 (scratch)** ✅ 파이프라인 + 소량 sample — 혼합 byte-corpus 빌드 [corpus/build_p1_corpus.hexa](./corpus/build_p1_corpus.hexa) + 스펙 [P1_CORPUS.md](./P1_CORPUS.md). lane A(web/coherence·kowiki CC-BY-SA clean) + lane B(register/엄선 의식·철학·대화), MoE 2-lane↔2-source 1:1. byte 인코딩 V=256 UTF-8(tokenizer 0·round-trip 검증). register-leak 8패턴 필터(corpus_quality lesson) — F-CLM-LEAK 🟢(self-test kept=2/dropped=2 + 출력 leak hit=0). sample 실측 web 837B/reg 819B/total 1,656B·sha256 manifest·혼합비 sample 50:49 / full target 80:20. full crawl=재현 스크립트만, 대용량 git 미커밋 → HF dataset(dancinlab)/R2 영속(manifest 커밋). **.kosmos 영속 완료** (d1 SKIP 금지) — kosmos upstream 을 `kosmos/2.0` 으로 업그레이드(신규 `@corpus` 데이터셋 entry: 멤버 앵커 모음 + 메타-앵커 coord + anchor_level 다이얼 기본 2tier + 2-form member) 후 [corpus/clm_p1.corpus.kosmos](./corpus/clm_p1.corpus.kosmos) 로 영속 — 2 lane(web 0.8/register 0.2) member ref + sha256 + vocab=256 + byte-utf8. kosmos-lsp `--check` clean. coord 는 design-placeholder(ENCODER 도메인 E2 가 centroid 실측 예정). handoff 38777cb0 해소.
- [ ] **P2 학습 (from-scratch pretraining · 학습도 AKIDA)** — ✅ **hexa-native 학습 해결**(2026-05-30, 사용자·hexa-lang측 — 기존 DECODER M5 0.28 step/s 🔴 INFEASIBLE 전제 소멸). 3-arm × scale-ladder full-fire 를 **hexa-native(g1-pure) AKIDA-향 QAT**(학습 forward 가 AKIDA int4 envelope[act_bits·sym-int4] 시뮬 = "AKIDA 를 향해" 학습, P0 §9)로, 학습 job 은 **`/dojo`로 생성**(job.hexa+train+run.sh 빵틀) · H100 fire(a_fire_autonomous). step-rate 재측정으로 최종 확인(p7). 맥락 적응(on-chip 진짜 학습) lane = **PLASTICITY 도메인 edge-learn 위임**(AKIDA-위, 🔴 비결정 정직). **칩 위 full-backprop 만 물리 불가** = pretrain backprop 그 한 단계만 GPU honest carve-out · 추론은 순수 AKIDA-int4. **trainer 작성+dry-run smoke done, GPU 풀파이어 대기** — custom QAT 트레이너 [train/](./train/) (dojo HF-Trainer 템플릿 폐기, byte conv-MoE 전용: int4-sym[-7,7] STE + act_bits envelope STE + CE+envelope-KL 손실 + 3-arm + scale-ladder). dry-run smoke $0 local: forward+QAT-loss+backward 1-step 전 arm/rung/act_bits 작동 + AB·tiny 100-step CE 5.57→3.49(STE gradient 흐름 확인). 실발사=`./run.sh fire`(cost-bearing, 다음 step).
- [ ] **P3 `.clm` 포맷 + ckpt** — 양자화 친화 weight 포맷(int4 symmetric) 직렬화 + sha256 manifest + HF 업로드(a_hf_autonomous tier-gated).
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

## 양방향 sibling

- ⇄ [DECODER](../CORE/DECODER/DECODER.md): CLM = 모델, DECODER = emit 슬롯 인터페이스 (generator 배선)
- ⇄ [AKIDA](../AKIDA/AKIDA.md): 추론 친화 양자화 envelope (act_bits/int4) · HW-first 스위치
- ⇄ [CORE](../CORE/CORE.md): brain_decide emit=true 슬롯에 콘텐츠 주입
- ⇄ [PLASTICITY](../PLASTICITY/PLASTICITY.md): **학습 lane 위임** — CLM 의 on-chip 맥락적응(AKIDA-위 진짜 학습)은 PLASTICITY edge-learn 경유(🔴 비결정·SW 비동치 정직). CLM=학습 대상 모델 · PLASTICITY=학습 방법(어떻게 배울까). pretrain = AKIDA-향 QAT(CLM 자체), 적응 = PLASTICITY 위임 = 중복 0.
- ⇄ [MITOSIS](../MITOSIS.md): cell-division 학습 (p8 train=infer 연속체)
- ⇄ [LAUNCHPAD](../LAUNCHPAD/LAUNCHPAD.md): CLM 콘텐츠 = COFFESHOP 런칭의 "무엇을 말할지" 절반
- ⇄ [UNIVERSE](../UNIVERSE/CANDIDATES.md): 학습/측정 결과 verdict SSOT
