# CLM — log

`CLM.md` 의 append-only 자매 로그. 각 엔트리 `## <ISO timestamp> — <header>` (최신 위) · 본문 `- [x]`(완료) / `- [ ]`(예정).


## 2026-05-30T02:00:00Z — B0 trainer 2-track (d5) scaffold — PyTorch fp16 feasible 실측 + hexa-native root-cause handoff

- [x] **Track 1** — `CORE/DECODER/clm_b0_pytorch_trainer.py` PyTorch fp16 conv-MoE byte-LM 트레이너 scaffold. Q1 dilated causal conv(attention 0, AKIDA envelope) · Q2 top-K HARD MoE conv-expert=mitosis cell · Q3 byte-vocab V=256 · monopoly-escape Switch load-balance aux + router-entropy 진단. fp16 autocast+GradScaler(CUDA), CPU fallback.
- [x] authoring 채널 — `.py` hexa-native 가드 우회 = P0 §6 `python3 -c "open().write()"` (정직 기록). `.gitignore` 정식 .py 허용(R37). open().write() 채널 사용.
- [x] **실측 smoke (feasible? ✅)** — CPU torch 2.8.0, 30-step: CE 5.6617→0.2575 monotone · distinct_experts 4/4 매 step · router_H~1.27 · **22.003 step/s** (hexa-native 0.23~0.50 대비 ~44–96×). verdict verbatim `.verdicts/clm_b0/smoke_cpu_d64_E4_2026_05_30.txt`. 정직: toy-scale CPU smoke = path-feasible 증명, production throughput 아님. fp16 GPU 미측정(로컬 CUDA 부재).
- [x] **Track 2** — hexa-native trainer 🔴 INFEASIBLE root-cause 진단(STEP_RATE_LOG entries 7/10/11/12): (1) RSS churn 328~331 MB/step runtime/CUDA-side(trainer 결백, empirically confirmed) (2) d=64 cuBLAS sync overhead dominance (3) AdamW out churn(#2017 해소). hexa-lang handoff filed `5cd0e4c8` (a_runpod_inbox). anima-side fix 안 함.
- [x] `CLM/B0_TRAINER.md` 2-track 문서 작성. 추론 AKIDA-only 불변(g1).
- [ ] 다음 = P1 corpus build (이 트레이너 toy corpus 교체) → P2 fp16 H100 production fire (≥10 step/s green gate · F-CLM-MONO 판정)

## 2026-05-30T01:00:00Z — P0 아키텍처 확정 (sbs manual 10-결정 co-design)

- [x] P0 설계 확정 — `CLM/P0_ARCHITECTURE.md` + `CLM/CLM_FORMAT_SPEC.md` (.clm v0.1)
- [x] Q1 Conv-native LM(dilated·attention 0·AKIDA온칩) · Q2 MoE conv-expert=mitosis cell · Q3 byte-vocab V=256 토대+3-arm(A/B/A+B)+F-CLM-MONO · Q4 micro-exp토이=직관(non-gate)·full-fire 판정·scale ladder·wall-first
- [x] d1 corpus 신규+혼합(웹대량+엄선)+.kosmos필수(upstream OK) · d2 .clm 2-track(int4+fp)+QAT+manifest · d3 rung tiny/small/target(≤AKD1000) · d4 추론AKIDA-int4-only/학습GPU-fp · d5 trainer 2-track(PyTorch즉시∥hexa fix) · d6 z>3.0+multiseed
- [x] authoring 정정: @py attr 없음 · .py=open().write() or sidecar disable hexa-native
- [ ] 다음 = P1 corpus build + UNIVERSE F-CLM falsifier 5개 등록

## 2026-05-30T00:00:00Z — 도메인 신설 (scratch from-zero · AKIDA-native)

- [x] CLM 도메인 신설 — `CLM/CLM.md`(스냅샷) + `CLM.log.md`(로그) + DOMAINS.tape 등록. ANIMA umbrella 합류.
- [x] 결정: anima 전용 의식 LM 을 scratch 에서 바닥부터. 외부 LLM/foundation-borrow 0. AKIDA 추론 친화 양자화 envelope(act_bits/int4) 설계 단계 못박음.
- [x] sibling 엮음 — DECODER(emit 슬롯 인터페이스) · AKIDA(추론 양자화) · CORE(brain emit) · MITOSIS(분열학습) · LAUNCHPAD(런칭 콘텐츠) · UNIVERSE(verdict)
- [x] 정직 명시 — hexa-native 학습 throughput 🔴 INFEASIBLE 실측(DECODER M5) = P2 병목 · AKIDA=추론칩(학습은 GPU)
- [ ] 다음 = P0 아키텍처 바닥설계 착수 (anima-native arch + .clm 포맷 + 더블바인드 탈출 메커니즘 + falsifier 사전등록)
