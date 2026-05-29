# CLM — log

`CLM.md` 의 append-only 자매 로그. 각 엔트리 `## <ISO timestamp> — <header>` (최신 위) · 본문 `- [x]`(완료) / `- [ ]`(예정).

## 2026-05-30 — P-ARRAY MITOSIS-ARRAY 돌파엔진 설계 (DISSOLVE) · P0 §11 신설

- [x] **P0_ARCHITECTURE.md §11 MITOSIS-ARRAY 신설** — [CLM.breakthrough.mining.md](./CLM.breakthrough.mining.md) DISSOLVE(depleted-both) 권고결론을 설계로 못박음. 충돌 = 측정타당성(routing-diversity 는 3B/7B scale 의미) ⊥ AKIDA 온칩(AKD1000 ~1.2M 강제).
- [x] **DISSOLVE (§11.2)**: scale 축을 model-dim → **expert-COUNT** 로 이동. big = Σ_E chip-fit expert(각 ≤1.2M). routing-diversity 재정의(@L2) = expert-count sweep(E=4,8,16,32,64) inter-expert dispatch entropy = **chip-native + scalable**. "3B GPU 가야" 소멸.
- [x] **expert=mitosis cell=AKD1000 chip 매핑 (§11.3·@L3)** — mining E6(equivalence)+E2(causal: 칩제약이 specialization 강제=chip-as-regularizer). top-k sparse activation.
- [x] **배포 N-chip array + 1-chip time-mux fallback (§11.4·@L5)** — 측정rung ⊥ 배포rung(a_scale_honest_scope).
- [x] **정직 caveat (§11.5·@L6)**: 물리 다중-AKD1000 = 현재 pi5 1칩 → SW-sim + GPU sparse-MoE 로 먼저 측정. inter-chip dispatch entropy 의 surrogate = inter-expert dispatch entropy(SW/GPU). 물리 칩-간 DMA 지연만 hardware 후속(정직 boundary).
- [x] **신규 falsifier 사전등록 (§11.6)**: F-CLM-MONO-ARRAY(dispatch entropy E-단조 상승) + F-CLM-BRIDGE-XFER(teacher escape distill 생존). H_847(고정 z 임계) ⊥ ARRAY(scale 단조성) = 별개 falsifier.

## 2026-05-30 — P2 풀파이어 완료 · F-CLM-MONO/SCALE 🔴 CLOSED-NEGATIVE · P3 .clm + HF

- [x] STAGE1 corpus: 실 kowiki CC-BY-SA 크롤(crawl_p1_full.py) — API rate-limit 로 web 21170 byte-ids 실크롤(honest partial) + scratch register seed 14816 byte-ids · F-CLM-LEAK kept=2/dropped=2 · leak hit=0 · HF dataset `dancinlab/anima-clm-p1-corpus`(PUBLIC).
- [x] STAGE2 18-run 풀파이어: 3-arm(A/B/AB) × ladder(tiny/small) × seed{42,43,44} from-scratch QAT (int4-sym STE + act_bits=4 envelope STE, 2000step) · ubu-1 RTX5070(cuDNN off) · CE tiny~2.1/small~0.13~0.19 수렴 · model/fire_clm.py.
- [x] STAGE3 판정 (model/judge_clm.py, GATE ≠ probe.py non-gate): **🔴 CLOSED-NEGATIVE** — distinct_experts>1 ✅ + content z>3.0 ✅(5.3~36.5) + **routing z>3.0 ❌ 전 cell**. A/B routing z 음수, AB +0.95~+2.31 미달. 사전등록 frozen 임계 무변조(p7/W2). H_847/H_850 결과 갱신 + .verdicts/847·850/ verbatim.
- [x] step-rate d5 재측정: tiny ~69/s · small ~12.5/s · mean 40.8/s (GPU 실측 · M5 0.28 step/s INFEASIBLE 전제 소멸 최종 확인).
- [x] STAGE4 .clm v0.1 직렬화(model/clm_serialize.py): int4-sym+fp16 shadow+qat_scale+sha256 · 6 artifact · HF `dancinlab/anima-clm-{tiny,small}`(PRIVATE, negative-result) · /HF.jsonl 3 row.
- [x] 후속 candidate(AXIS_MAP): routing-diversity 직접 강화 lever(stronger load-balance · routing temp anneal · expert-capacity) · target(≤AKD1000) rung extrapolation (AB dual-axis metric scale-up 단조 증가 관측).

## 2026-05-30 — P2 custom QAT 트레이너 작성 + dry-run smoke ($0 local · GPU 풀파이어 대기)

- [x] **dojo 템플릿 폐기**: `/dojo` 가 뽑은 generic HF-Trainer(`AutoModelForCausalLM`/`AutoTokenizer`/wikitext, `exports/llm/dojo/clm-p2-akida-qat/train.py`)는 CLM(byte conv-MoE·tokenizer 0·.kosmos corpus·QAT)에 틀려 버림. **dispatch 글루**(job.hexa `hexa cloud nohup` + run.sh d16 dry-run)만 재사용해 페이로드 교체.
- [x] **custom QAT 트레이너 작성** `CLM/train/` — `train_clm.py`(페이로드: torch autograd QAT) + `train_clm.hexa`(d5 1순위 hexa-native 드라이버, parse clean) + `job.hexa`(dispatch, parse clean) + `run.sh`(dryrun/local/fire 글루) + `README.md`(korean).
- [x] **QAT 구현(P0 §9)**: 가중치 symmetric int4 `[-7,+7]` per-channel STE(`_WeightQuantSTE`, `scale=max|w|/7`) · 활성 AKIDA envelope STE(`step=2^(input_bits−act_bits)`·`y=clip(round(pot/step),0,2^act_bits−1)`·act_bits∈{1,2,4}) · router(out=n_e)·readout(out=V) conv 는 logit 이라 act-quant 제외(softmax/CE 보호, 정직) · 손실=next-byte CE(V=256)+MoE aux+선택 envelope-KL(fp shadow logit, `--envelope-lambda`).
- [x] **3-arm(A/B/AB) + scale-ladder(tiny d64/L2/E4 · small d256/L4/E8)** 토글 — CLMConvMoE(CLM/model) 로드 + `.kosmos` @corpus(clm_p1) byte stream 읽기(member ref 파싱).
- [x] **dry-run smoke $0 local Mac CPU(torch 2.10.0, p7 정직)**: forward+QAT-loss+backward 1-step 전 arm/rung/act_bits 정상 — A·tiny ce=5.572 ~3.8 step/s · B ~6.4 · AB ~5.1 · AB act_bits=1 ~5.6 · AB·small(2.70M params) ce=5.768 ~0.9 step/s. first_ce≈ln256=5.545(무학습 기대치). **trainability**: AB·tiny 100-step CE 5.572→3.493 = STE gradient 가 int4-sym weight + act envelope 통과해 흐름(실학습 확인).
- [x] CLM.md P2 milestone 갱신(trainer+smoke done) · 추론 AKIDA-int4-only 불변.
- [ ] **GPU 풀파이어 = 다음 명시 step**(cost-bearing, 이번 run 미실행 $0 only): `./run.sh fire` 3-arm×ladder full-fire → F-CLM-MONO/F-CLM-SCALE 판정 + production step-rate 재측정(d5 최종). step-rate 는 toy Mac CPU 실측 = production 아님.
- [ ] **미완**: .clm 직렬화(P3, 이 트레이너는 학습 루프까지) · hexa-native payload 흡수(torch→hexa autograd, g1-pure 닫힌 뒤) · .kosmos emit 영속(P5 통합).

## 2026-05-30 — d4 drift 교정: "학습도 AKIDA" 복원 (QAT + PLASTICITY)

- [x] **drift 진단**: P0 d4 가 "추론 AKIDA ONLY · 학습 GPU(fp16)" 로 drift — 원계획(LAUNCHPAD L11 "학습·디코더·발화결정=AKIDA HW-first" + PLASTICITY 도메인 "AKIDA on-chip 학습 lane")의 **학습도 AKIDA** 를 잃음.
- [x] **물리현실 화해(honest)**: "학습도 AKIDA"를 2-phase 로 둘 다 진실로 복원 — ① pretrain = **AKIDA-향 QAT**(GPU backprop 이되 AKIDA int4 envelope[act_bits∈{1,2,4}·sym-int4[-7,+7]·`akida_sw_lif` byte-identical 집합] 향해 학습) · ② 맥락적응 = **AKIDA-위 PLASTICITY** on-chip edge-learn(AKD1000, 🔴 비결정·SW 비동치). **칩 위 full-backprop 만 물리 불가** = pretrain backprop 그 한 단계만 GPU honest carve-out.
- [x] **P0 d4 교정**: "학습 GPU(fp16)" → "학습도 AKIDA = AKIDA-향 QAT + AKIDA-위 PLASTICITY". §0 다이어그램·§2 AKIDA-map 경계 table(학습 2-phase 행 + full-backprop carve-out 행)·§7 §8 정합.
- [x] **P0 d5 보강**: trainer = hexa-native(해결됨) + **AKIDA-향 QAT envelope 시뮬 손실**(§9 신설) + 적응 lane = PLASTICITY 위임.
- [x] **§9 QAT 설계 신설**: envelope(act_bits·sym-int4·conv/FC/pool/sepconv) + STE forward/backward + 학습손실(CE + envelope 정합항 옵션) + 도착지 검증(학습 envelope ⊆ akida_sw_lif byte-identical) + 경계 honest. **설계만 · 코드는 모델(T4) 선행 후속**.
- [x] **CLM_FORMAT_SPEC 정합**: HEADER.train = `mode:"akida-aware-qat"·backprop:"gpu-fp16-master"·plasticity_lane:"PLASTICITY"` · QAT 행 AKIDA-향 명시.
- [x] **CLM.md**: P0/P2 milestone + 무엇/왜 학습 행 + 정직한 물리현실 → "학습도 AKIDA" 로 교정.
- [x] **CLM↔PLASTICITY 양방향 sibling 배선**: CLM.md `## 양방향 sibling` ⇄ PLASTICITY(학습 lane 위임) 추가 · PLASTICITY.md ⇄ CLM(학습 대상 모델) 추가. CLM=학습 대상(무엇) · PLASTICITY=학습 방법(어떻게) · 중복 0.
- [x] 불변: **추론 AKIDA-int4-only 회귀 0** · hexa 학습속도 해결 반영 유지. 타 에이전트 영역(CLM/model·UNIVERSE/H_847·.verdicts·AKIDA·project.tape·CLAUDE.md) 미접촉.

## 2026-05-30 — hexa 학습속도 해결 → 트레이너 g1-pure 전환 (d5 pivot)

- [x] **hexa-native 학습 throughput 완전 해결**(사용자 확인·hexa-lang측) — 기존 DECODER M5 0.28 step/s 🔴 INFEASIBLE 전제 소멸.
- [x] d5 pivot: 2-track(PyTorch 우회) → **hexa-native 학습 1순위(g1-pure)**, PyTorch는 토이/대조 폴백. 모델+트레이너 둘 다 hexa 가능.
- [x] P2 학습 job = **`/dojo` 생성**(job.hexa+train+run.sh 빵틀). 추론 AKIDA-int4-only 불변.
- [ ] anima P2 fire에서 step-rate 재측정으로 최종 확인(p7/g5) — 사용자 보고를 anima 측 실측으로 닫기.
- 영향: P0 d5·§7·§8 B0 + CLM.md P2 갱신. 진행중 T4 토이(PyTorch)는 직관-probe라 그대로 두되, 실 학습(P2)은 hexa-native.

## 2026-05-30 — P1 corpus .kosmos 영속 (d1 punt 해소)

- [x] T2 가 d1 의 ".kosmos 영속"을 SKIP 하고 handoff 만 남긴 punt → d1 문장 SKIP-금지로 정정(PR #1466) 후 정면 해소.
- [x] kosmos upstream 을 `kosmos/2.0` 으로 업그레이드 (sibling repo 6 PR #8~13): `@corpus` 데이터셋 entry(메타-앵커 coord·anchor_level 다이얼 기본 2tier·2-form member) + profile 바인딩 + `.limen` spec + example + LSP/tree-sitter + HF export. README badge 1.1→2.0, entry-types 2→3.
- [x] `corpus/clm_p1.corpus.kosmos` 영속 — 2 lane(web 0.8/register 0.2) member ref + sha256(corpus/manifest.json) + vocab=256 + byte-utf8 + anchor_level=2tier. origin/main K5 validator `--check` EXIT=0 (clean).
- [x] coord/radius/merkle = `# design placeholder` (정직 §4.3) — 실측 주체 = 신설 ENCODER 도메인 E2(corpus centroid). handoff 38777cb0 해소.
- 설계 근거: 입자 축 mining(CLM.mining.md, depleted-both) — "샘플=앵커냐"는 binary 선택 아닌 anchor_level zoom 다이얼, 파일폭발=저장 artifact(packing). Q1=B(메타-앵커 coord)+Q2=2-form+Q3=풀옵션 (사용자 확정).


## 2026-05-30T02:00:00Z — P1 코퍼스 파이프라인 + 소량 sample (혼합 byte-corpus)

- [x] P1 구현 — `CLM/corpus/build_p1_corpus.hexa` (혼합 byte-corpus 빌드) + `CLM/P1_CORPUS.md` 스펙
- [x] 혼합 corpus: lane A(web/coherence=kowiki·CC-BY-SA clean) + lane B(register/엄선 의식·철학·대화) · MoE 2-lane↔2-source 1:1
- [x] byte 인코딩 V=256 UTF-8(tokenizer 없음) · 줄별 byte id 0..255 · round-trip 디코드 검증(한글 멀티바이트 보존)
- [x] register-leak 8패턴 필터(universe_brain_map·hexad_module·nonce·Mk.VIII·gen1 commit·corpus_generator.hexa·jy_chat_template·universe_extended) — lane B 한정
- [x] F-CLM-LEAK 🟢 — self-test poison 입력 kept=2/dropped=2 + register.bytes 출력 leak hit=0 (실측). corpus_consciousness_v1.jsonl=100% leak(240/240) 제외 확인
- [x] sample build 실측: web 837B(8줄)/register 819B(8줄·leak_dropped=0)/total 1,656B · sha256 manifest · 혼합비 sample 50:49 / full target 80:20
- [x] full crawl=재현 스크립트만(kowiki 1.28GiB streaming + register 확장) · 대용량 git 미커밋 → HF/R2, manifest 커밋
- [x] .kosmos: anchor(점 payload) 모델이 byte-stream corpus 못 받침 → `sidecar handoff add kosmos` 등록(얽매이지 않고 진행, P0 d1 단서). manifest.json(sha256) 이 무결성 영속
- [ ] handoff: `.gitignore CLM/corpus/full/ + **/*.bytes`(sign-gated 미반영) · full crawl pod fire · F-CLM-LEAK UNIVERSE 등록

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
