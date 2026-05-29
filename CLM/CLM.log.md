# CLM — log

`CLM.md` 의 append-only 자매 로그. 각 엔트리 `## <ISO timestamp> — <header>` (최신 위) · 본문 `- [x]`(완료) / `- [ ]`(예정).

## 2026-05-30 — P1 corpus .kosmos 영속 (d1 punt 해소)

- [x] T2 가 d1 의 ".kosmos 영속"을 SKIP 하고 handoff 만 남긴 punt → d1 문장 SKIP-금지로 정정(PR #1466) 후 정면 해소.
- [x] kosmos upstream 을 `kosmos/2.0` 으로 업그레이드 (sibling repo 6 PR #8~13): `@corpus` 데이터셋 entry(메타-앵커 coord·anchor_level 다이얼 기본 2tier·2-form member) + profile 바인딩 + `.kanchors` spec + example + LSP/tree-sitter + HF export. README badge 1.1→2.0, entry-types 2→3.
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
