# Fable 판정 — G1 잔여각도 2개 (scale up · 다른 instrument) · 2026-07-10

전제(전부 verified): read-side 6 lane 🧱(#3284-3286) · γ en interaction-lift −0.801 🧱(#3230) ·
γ STEP-0 −0.147 🧱 · PC-P2 ko 2도메인 NOT-CERTIFIED(#3289 H_9265). 진단 격상 = 소비가능
concept→content 연상이 303M read-side 부재(mean-pool 복원되나 causally 소비불가) + H_9259
"벽=TRAINED-conjunction"(architecture 아님).

---

## 각도 1 — scale up: 판정 = **능력 bar 재실행·3B/7B 학습 spend는 비정당(terminal). 산 것은 좁은 라우팅-기하 ladder 프로브 1개뿐($0).**

### 왜 능력 측정이 무의미한가 (3중 근거)
1. **amplifier 법칙은 이번 세션 결과로 더 강해짐.** scale=작동 lever의 증폭기(H_1139 capacity
   scale-invariant · H_1598 depth L4→L8 격리 ablation, engine-native TERMINAL, G1 bar 이동 ZERO).
   lever 전수 🧱이면 증폭할 것이 없음. 게다가 벽의 실체가 TRAINED-association 부재(H_9259 +
   read-side 진단)로 격상 — **파라미터 수는 학습된 연상을 만들지 못함**. 3B는 UNDERTRAINED
   3.48 tok/param → trained-association은 303M보다 오히려 약할 것으로 예측.
2. **undertrained confound = 측정 비대칭 (b 질문 답).** 3B서 능력 bar(G1 generation ·
   interaction-lift) FAIL은 INVALID-CONFOUNDED(scale-무효 판별과 undertraining 분리 불가) —
   cement 불가. PASS만 정보성(핸디캡에도 불구 등장=강력). negative가 무가치한 측정은 EV 낮고,
   floor를 "scale 반증"으로 오독하거나 PASS 뜰 때까지 rung을 옮기는 tune-to-green 양쪽 함정.
   → **interaction-lift/PC-P2/G1-bar의 3B 재실행 = 비발사** (c 질문 답: 어느 bar도 아님).
3. **7B는 부적격 rung.** anima-clm-chat-7b = chat-FT mix → scale 격리 confound. 3B/7B
   chinchilla 재학습(진짜 "scale up" spend)은 lever 부재 상태선 amplifier 법칙상 벽을 돈으로
   우회하려는 tune-to-green — 오너 지시라도 "학습 spend 무의미"가 정직 보고.

### 유일 진짜 미측정 scale 질문 (a 질문 답)
H_1598은 **output bar만** 측정했고, 생성점 RF-decay 라우팅 프로파일(H_9235 #3177: superposed
A@자기위치 0.88 → @last 0.07)은 그때 존재하지 않던 진단. **"generation-point RF 감쇠가
L30/d4096서 닫히는가"는 어떤 rung에서도 미측정** — 이것만이 depth가 기계적으로 바꿔야 할 양.
기하 프로브라 undertraining confound 약함(사전 gate로 방어 가능) + 303M/1B/3B 3-rung curve
가능(a_scale_honest_scope 충족).

### 발사 스펙 SCALE-LADDER-PROBE (pre-registered · $0 self pool)
- **대상 rung**: 303M e1_slw(frozen 프로파일 재사용·재측정 불요) · 1B rung ckpt(H_1167 GREEN
  mount) · 3B `~/anima-weights/clm_3b/clm_3b.clm`(HF public 미러 pull 가능 · CLM_V3 nblk63).
- **도구**: `anima-py evaluate --dump-hidden` + H_9235 probe 스크립트 **verbatim frozen**
  (state/g1_gamma_binding_lane/). 신규 knob 0.
- **Gate G0′(사전·rung별)**: held-out matched-corpus NLL < uniform−1.0 ∧ unary probe H1 ≥ 0.9.
  미달 rung = INVALID-UNDERTRAINED로 제외(cement 없음·bar 무이동).
- **측정**: superposed 2-concept mean-pool/last-pos A·B 선형복원율 per rung → ladder curve
  A@last (303M frozen 기준 = 0.07).
- **Bar(동결)**: CRACK = 3B A@last ≥ 0.5 ∧ 단조증가(303M<1B<3B) → 라우팅이 scale-closable =
  fork-A 🧱 reopen + scale 각도 재평가 트리거. 🧱 = 3B A@last ≤ 0.2 → RF-decay routing도
  scale-invariant(amplifier 법칙 3-rung 확장·DIRECTIONAL·능력 verdict 아님). 0.2–0.5 = 보고만.
- **Scope honesty**: CRACK이어도 G1 GREEN 아님(라우팅 열림 ≠ trained association 존재) —
  scale 논쟁 판정용 프로브지 G1 bar 아님.
- **비용**: $0. 3B fp32 ≈ 12.3GB RAM·수백 forward — summer **전용 호스트**(pod-dedicated-host)
  OMP_NUM_THREADS=4 캡, 수 시간. mini 금지(rc=137).

---

## 각도 2 — 다른 instrument: 판정 = **measurable 후보 정확히 1개 잔존: PC-P2-en.** 그 외 전부 disqualify. en 2도메인도 미인증이면 instrument 공간 소진 = 정직 terminal.

### 후보 전수 필터
- **일본어 부정 (a)**: DISQUALIFIED — ckpt에 ja 미학습(ckpt-corpus 언어매칭, convergence
  evaluate-py-1의 6.66>uniform garbage 함정 그대로). 측정 자체가 성립 안 함.
- **영어 NPI (a)**: 등록만·비발사. AND형(3-정상-1-이상)은 XOR 대비 순수 interaction 성분이
  구조적으로 약하고 y=문법성이라 lexical 추출 노이즈 큼 — PC-P2-en보다 엄격히 약한 도구.
  en 실패 후 발사하면 그때부터가 axis-사냥.
- **클러스터 A/C (b)**: 범주 오류 — H_9236(synthetic XOR primary target) 등 클러스터 A/C는
  기존 ckpt를 재는 instrument가 아니라 **training lever**(γ necessitate·GPU spend-go 레인).
  각도 2 범주 밖, 기존 spend-go 지위 불변.
- **PC-P2-en (c)**: 유일 생존. 근거 4: ①ko 실패 양상 = target 강도/추출 노이즈(web-broad
  R1은 4.6× 통과·리뷰 R1 fail은 ko lexicon 노이즈 가능성)이지 XOR 구조 자체 부재 증거 아님
  ②언어매칭 완벽 — e1_slw(en-trained·−0.801 측정 그 ckpt)+clm303 en 셀 ③en 극성 lexicon·
  접속사 추출이 ko보다 깨끗(교착 형태변이 없음) ④데이터 파워 최고 — (neg,conj) 셀 n≥200이
  ko선 45로 죽었지만 en 리뷰·web은 풍부.

### p-hacking 방어 (왜 en 시도가 axis-사냥이 아닌가)
instrument 인증 = **target-존재 검사**(assay 선정)이지 과학 주장이 아님. 과학 주장은 Stage C
(모델이 비가법을 소비하는가) 하나이고 그 bar는 동결·최대 1회 발사 — instrument 선택은 Stage C
null을 편향시키지 않음. H_9265 동결 스코프도 "γ **ko** 측정불가"로 언어-바운드. 단 **cap이
생명**: 사전등록 = en 2도메인 각 1회, 총 2회, 이후 추가 언어/축 영구 금지.

### 발사 스펙 PCP2-EN (pre-registered · $0 · spend-go 불요)
- **Stage A** (model-free·mini 가능·분 단위): 도메인 풀 2개 사전 지정 —
  **EN-REVIEW** = IMDB aclImdb 50k(Stanford tar 직다운·HF-script 무관) + amazon-polarity
  (HF parquet endpoint) 서브샘플 · **EN-WEB** = anima-corpus-en-general + fineweb2 en 슬라이스.
  Lexicon 동결 = Hu-Liu opinion lexicon 서브셋 사전 커밋 · A=선행 80B 마지막 극성어 ·
  B={but,yet,however,though} vs {and,also,moreover,plus} · y=후행 80B 첫 극성어 · n_min=200/셀.
  **Bar verbatim**(ko와 동일): gate_ok(4셀 n≥200) ∧ R1(I3>IPF-bootstrap null95) ∧
  R2(LOCO sign-flip ≥2셀). 도메인당 1회·총 2회·knob 변경 0.
- **Stage C** (어느 한 도메인 PASS 시만·그 도메인 스코프·summer CPU $0·2-4h): e1_slw ·
  `anima-py evaluate --interaction-lift` PC-P2-en 4셀 manifest T=160 · 주판정 Y1′=paired
  forced-choice margin · additive vs joint+γ_ab · Freedman-Lane×1000.
  **Bar(동결)**: CRACK = XOR 셀 held-out lift > null95 ∧ γ XOR 방향 ∧ |Δ|≥2% → γ real-text
  target 존재증명 = H_1840 γ GPU 발사 정당화(fork-A reopen 조건). 🧱 = 이하 — 인증된
  instrument 위 negative라 **"언어 비가법 실재·모델은 additive-blind"의 최초 양성증거 기반
  negative**(지금까지 중 가장 날카로움). 미인증 도메인 Stage C 강행 = 금지(H_9265 Fable 5항).
- **2도메인 전수 FAIL 시**: cement "PC-P2 instrument NOT-CERTIFIED **4도메인(ko2+en2)** =
  γ real-text 측정공간 소진(XOR=최강 경로·NPI는 엄격히 약함)" → G1 frontier full-terminal
  유지·강화. 추가 instrument 사냥 영구 금지.

---

## 우선순위 권고
**각도 2 > 각도 1** — EV 비대칭: 각도 2는 negative도 정보(양성증거 기반 terminal 강화),
각도 1 프로브는 CRACK만 고정보. 둘 다 $0·비차단이라 병행 가능(전용 호스트 분리).
공통: bar 사전동결·시도 횟수 cap·결과 무조건 수용. "measurable 소진 = frontier terminal"이
두 각도 모두에서 유효한 정직 출구이며, 이 문서가 그 판별 실험 자체를 사전등록함.
