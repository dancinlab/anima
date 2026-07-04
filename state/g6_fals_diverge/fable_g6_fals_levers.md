ledger·탐지기 실코드 확인 완료. 핵심 발견이 하나 있어 A절이 예상보다 훨씬 구체적으로 나옵니다 — `_g6_is_falsifiable`는 **어휘 접속(conjunction) 탐지기**이고, 채점 대상 `o`는 frame 제외 **생성 continuation 40바이트뿐**임을 코드로 확정했습니다 (`core/decode.py:670` — `out`은 빈 bytearray에서 시작, seed 미포함).

---

# A. FALS 벽의 원리 — "40바이트 안의 희귀 어휘류 접속" 문제

## A-1. FALS의 형식적 필요조건 (탐지기 실코드 기준, `core/g6_ideation.py:122`)

FALS=1이 되려면 frame 뒤 **continuation 40바이트(≈7~8 영단어)** 단독으로:

| 조건 | 내용 | 어려움 |
|---|---|---|
| (a) comparator | 25어 집합(if/than/more/increases/predicts/causes/…) ≥1 | 중간 — frame이 "if…then" 형식이라 priming은 되나 **frame 자체는 채점 제외** |
| (b) measurable | 25어 집합(rate/count/level/threshold/percent/…) ≥1 | **높음** — frame_guard가 frame 내 measurable 누출을 차단하므로 순수 자발 emit 필요 |
| (c) content ≥2 | 사전 등재, len≥3, 비-stopword 2개 이상 | 낮음 |
| (d) ¬질문 | 끝 바이트 ≠ `?` | 낮음 |
| (e) ¬stance 오프닝 | 첫 3어가 순수 stance 아님 | 낮음 |
| (전제) kwr≥0.5 | coherent 게이트 선통과 | 이미 통과 중(DIST=6) |

**추가 구조적 사실 2개** (이번에 코드로 확정, 기존 논의에 없던 것):

1. **탐지기는 ASCII-only다.** `_g6_words`는 비-ASCII 바이트를 전부 구분자로 버린다(`core/g6_ideation.py:80`). 한글 continuation은 단어 0개 → kwr=0 → coherent조차 안 됨. 즉 **한국어 register로 확률질량이 흐를수록 DIST·FALS 동시 억압** — 4-cell corpus의 ko 절반이 G6에는 순수 마이너스 채널.
2. **길이 예산이 극도로 타이트하다.** gen=40바이트에 (a)∧(b)∧(c)를 모두 넣어야 함. "X increases the rate of Y" = 27바이트로 가능하지만, 학습 corpus의 falsifiable 문장이 40바이트보다 길면 echo가 창 안에 안 들어온다.

## A-2. 왜 distinct prose는 되는데 falsifiable claim은 안 되나

CE-echo 관점에서 mouth의 emit 분포 ≈ corpus 조건부 분포. 그러면:

**P(FALS) ≈ δ_FM := corpus에서 "if A, then B:"류 문맥 직후 40바이트 창에 comparator∧measurable가 공기(co-occur)하는 밀도.**

- DIST는 **어떤** 유창한 continuation이든 세므로 corpus 전 질량이 기여 → 쉽다.
- FALS는 두 폐쇄 어휘류의 **접속 사건**만 세는데, 일반 산문에서 comparator와 measurable의 40바이트 공기율은 기저율의 곱 수준(둘 다 희귀하면 곱은 극희귀) — vague/hedge가 CE상 싼 게 아니라, **falsifiable 형식이 corpus에 사실상 부재해서 echo 자체가 불가능**하다는 가설이 최단 설명.
- 이것은 G1 벽의 확정 법칙(coverage-density: NL-byte held 0.95 HIGH vs 0.03 LOW, `g1-coverage-density-nl-bytes-lever`)과 **정확히 같은 형태**다. G6≡G1(H_1603)의 실체 = 둘 다 "타깃 사건의 corpus 밀도 bound".

## A-3. FALS-판정지표 (G1의 ρ/σ/κ/M 대응물)

- **δ_FM** — corpus 40바이트 창의 comparator∧measurable 접속 밀도 (1차 예측인자)
- **ρ_c, ρ_m** — 각 어휘류의 단독 emit율 (모델 출력에서 측정 → 어느 conjunct가 병목인지 분해)
- **PMI(comp, meas)** — corpus에서 두 류의 공기 초과율 (독립곱 대비)
- **λ_ascii** — continuation의 ASCII-영어 비율 (한글 유출 = 즉사)
- **fit₄₀** — corpus 내 falsifiable 문장 중 40바이트 이하 비율 (echo가 측정창에 들어오는가)
- **M_earned** — FALS(composed) − FALS(shuffled-frame) margin. 측정 메타법칙(`measurement-metalaw`: FORM tunable·BIND earned) 적용 — FALS 탐지기는 1-항 FORM이라 corpus 밀도로 "게임"이 가능하므로, frame-정합성이 깨진 shuffled 통제에서 같이 오르면 form-echo일 뿐임을 스스로 표기해야 함. 냉동 bar는 그대로 두고(임계 이동 금지) **동반 진단**으로 pre-register.

---

# B. 새 레버 12개 (cheap engine-native 판별 빠른 순)

### B-1. FALS-precursor 분해 게이지 — "어느 conjunct가 죽어있나" 【$0 · 기존 로그만】
① 기존 G6 decode 출력(state/verdicts의 clm303/ByteGPT 런)에 탐지기 5개 조건을 **개별로** 재채점. ② 레버가 아니라 레버-조준기: (a)만 죽었는지 (b)만 죽었는지에 따라 B-3의 corpus 설계가 완전히 달라짐(comparator는 frame priming으로 이미 나올 가능성 높음 → 병목은 measurable 단독일 것으로 예측). λ_ascii도 동시 측정(한글 유출량). ③ cheap probe = python 재채점 스크립트, decode 불요. ④ engine-native: 조준 후 B-3 발사에 흡수.

### B-2. δ_FM corpus 밀도 측정 — G1 coverage 측정의 FALS판 【$0 · 텍스트 스캔】
① 4-cell corpus(HF anima-corpus-*)에서 δ_FM·PMI·fit₄₀ 측정. ② 예측: δ_FM≈0 → 벽=corpus 기아 확정(G1의 0.95 vs 0.03과 동형). 만약 δ_FM이 유의하게 >0인데 FALS=0이면 **corpus 가설 기각** → 벽이 objective/기전 쪽 → B-6 이후로 우선순위 역전. 즉 이 측정 하나가 나머지 레버 절반의 운명을 가른다. ③ mini에서 수 분. ④ terminal 불요(측정이지 개입 아님).

### B-3. FM-접속 밀도 코퍼스 (data-format, G1 derivtrace 직전이) 【본명 레버】
① target을 `주장(comparator+measurable, ≤40바이트); 반증조건; 예측` 형식으로 재작성한 corpus cell을 warm-FT에 추가. **held-out 개념만** 사용(냉동 frame의 `_g6_concepts()` 5종 및 그 단어는 격리 — tune-to-green 차단). ② derivtrace가 G1에서 "풀이과정을 echo로 만들었"듯, δ_FM을 올리면 falsifiable 형식이 조건부 분포의 최빈 continuation이 됨 — vague가 이기는 이유가 '싸서'가 아니라 '유일해서'였다면 이걸로 역전. **fit₄₀ 제약 필수**(짧은 주장문으로 구성). ③ cheap probe: mini numpy char-LM(d64)을 hi-δ vs lo-δ 합성 corpus로 학습, held-out frame에서 FALS + M_earned A/B. ④ terminal: 303M warm-FT → `anima evaluate --py` (배터리가 G0–G6 전부 내므로 G1 동시 판정, C절).

### B-4. 모순-쌍 코퍼스 (contradiction-keyed H_9125/9126 심화) 【B-3와 독립 구조축】
① 모든 주장에 부정/반례를 인접 쌍으로: `X increases the rate of Y. / X fails when the level of Z is low.` — 주장이 자기 반증조건을 데리고 다니는 분포. ② B-3가 어휘 밀도라면 B-4는 **관계 구조**: 반증가능성 = "부정이 정합한 주장"이라는 정의를 분포 구조로 직접 심음. criterion re-coordination 메타법칙과 정합. ③ probe: B-3 하네스에 pair-arm 추가(3-arm: hi-δ 단문 / 모순-쌍 / lo-δ), 추가로 "모순-continuation 능력"(모델 출력에 `but this fails when…` 이어쓰기 가능?) 측정. ④ B-3와 같은 발사에 arm으로 동승.

### B-5. 결과-회귀 CE (consequence-return, 예측코딩 렌즈) 【objective인데 non-additive·p7 무결】
① 2-세그먼트 corpus: `주장 → [OUTCOME] 관측결과`. 구체적 주장일수록 outcome 세그먼트의 CE가 낮아지도록 데이터를 구성(vague 주장 뒤 outcome은 고엔트로피, 구체 주장 뒤 outcome은 저엔트로피). ② **CE 자체가 구체성에 보상을 주게 됨** — aux-loss 추가가 아니라(H_1602 additive floor 회피) 데이터 구조가 CE의 기울기를 바꿈. 탐지기를 loss에 넣지 않으므로 p7/a_train_inline_gauge 무결. 도파민 RPE·예측코딩의 자연 매핑(예측오차=반증). ③ probe: mini numpy로 vague-arm vs specific-arm의 outcome-CE 차 → emit 분포 이동 확인. ④ git status의 `state/consequence_return_design/`과 합류 가능 — 기존 설계 자산 재사용.

### B-6. 가설-검증 에피소드 (전전두 렌즈, 3-턴 구조) 
① `가설(guess) → 시험(test) → 판정(revise)` 3-턴 에피소드 corpus (Wisconsin card-sorting형): 피드백이 뒤집을 수 있는 guess만 강화되는 궤적. ② B-5의 일반화 — 반증이 1회성 outcome이 아니라 **반복 교정 루프**로 분포에 존재. 에피소드-구조 자체는 G1에서 H_1835(MLC) 🧱였으나 그것은 *재조합 transfer* 실패였고, 여기 목표는 transfer가 아니라 **형식 emit** — 다른 판정축이므로 dup 아님(단 이 구분을 카드에 명기). ③ probe: mini 3-턴 vs 1-턴 arm. ④ B-3 발사의 후속 arm.

### B-7. 과학-register 5번째 cell (자연텍스트판 B-3)
① 합성이 아닌 실측정-heavy 자연 텍스트(초록·실험보고 문체, ≤40바이트 문장 필터)를 5번째 register cell로. ② B-3의 합성 corpus가 FORM-echo만 만든다면, 자연 register는 comparator/measurable의 **정상 통계적 이웃**까지 옮겨줌 → M_earned가 올라갈 가능성. a_chat_registers의 4-cell은 chat 표준이지 학습 상한이 아님. ③ probe: δ_FM을 후보 register 텍스트에서 먼저 측정(B-2 도구 재사용). ④ B-3와 같은 warm-FT 사이클.

### B-8. G-refuter 데이터-루프 (falsifier-lane H_6163의 curation 재배치)
① G(역방향 gradient-free)를 **학습데이터 큐레이터**로: corpus 후보 주장에 대해 G가 반례 상태를 구성할 수 있으면(=반증가능) 채택, 못 하면 기각 — 반증가능성이 높은 분포만 A의 CE에 노출. ② native-mouth/tension은 emit 경로에서 INERT(H_1834/1837)였지만, 이것은 mouth 밖 **data-channel 배치**라 그 벽과 좌표가 다름(prompt의 "데이터채널/lane만" 조건 충족). H_6163 PROPOSED를 '별도 lane substrate'에서 'curation 루프'로 강등-구체화한 것. ③ probe: mini에서 G-mirror가 주장문 vs vague문을 반례-구성 가능성으로 분리하는지($0). ④ 분리되면 B-3 corpus 생성기에 필터로 장착.

### B-9. 숫자·단위 채널 (양적 리터럴 기아 프로브)
① falsifiable 주장의 자연 형태는 수량 포함("by 12 percent") — byte-mouth의 숫자 emit율 자체가 floor일 수 있음. 숫자-밀집 주장문 cell 추가. ② measurable 집합에 percent/times/ratio 등 수량어가 많아 숫자 이웃 분포가 measurable emit을 직접 견인. ③ probe: 기존 출력의 digit-emit율 측정(B-1에 편승, $0). ④ B-3 corpus의 변주 arm.

### B-10. earned-FALS 통제 하네스 (측정 메타법칙 적용) 【레버가 아니라 레버 판정기】
① 모든 B-3~B-9 발사에 shuffled-frame FALS·frame-무관 FALS(무조건 emit)·ablated-frame FALS 통제를 동반, M_earned로 판정. ② FORM-echo(그냥 어휘 암송)와 frame-결합 falsifiable claim을 구별 — 메타법칙 "창발신호는 값이 아닌 Δ에" 의 G6 적용. 냉동 bar(fals≥1)는 불변, 이건 추가 렌즈(ABLATION, a_break_the_wall 요건). ③ $0 — 채점 스크립트 확장. ④ 모든 terminal 발사에 동봉.

### B-11. ko→en 질량 재배분 진단 (ASCII-only 탐지기 귀결)
① A-1의 발견: 한글 continuation은 FALS 원천 불가. G6 frame(영어)에서 mouth가 한국어로 이탈하는 비율 λ_ascii가 높으면, **영어-조건부 안정성**만으로도 FALS 기저율이 오름. ② 레버라기보다 confound 제거 — λ_ascii가 낮은데 FALS=0이면 어휘접속 문제, λ_ascii 자체가 낮으면 register-라우팅 문제로 진단이 갈림. ③ B-1에 편승($0). ④ 필요시 en-cell 비중 arm.

### B-12. 자기-반증 서명 형식 (`unless` 꼬리)
① 모든 주장 target에 반증조건 꼬리를 한 문장 안에: `X increases the rate of Y unless Z` — comparator 2회(increases, unless)+measurable 1회가 **한 40바이트 창**에 원자적으로 들어가는 최소 형식. ② fit₄₀ 문제의 극한 해법: 반증조건을 별도 세그먼트(B-3의 `;` 구분)로 두면 측정창 밖으로 잘리지만, unless-꼬리는 창 안에 남음. ③ probe: B-3 mini A/B에 문장형 arm 추가. ④ 동일.

**기각한 repackage들(자체 검열):** falsifiability-reward를 additive aux-loss로(H_1602 floor + p7 Goodhart) · 탐지기 통과를 decode-시 best-of-K 선별(H_1590 scaffold 축 DEAD) · A⇄G tension을 emit-게이트로(H_1834/1837 INERT) · attention/용량 증설(H_6170 TERMINAL) · jamo/set-search(H_1814).

---

# C. G1 진행과의 공유

**공유가 구조적으로 공짜다**: `g_eval_all`(cli/evaluate.py)은 한 배터리에서 G0–G6를 전부 내므로, **어떤 corpus-format 발사든 G1과 G6-FALS 판정이 자동 동시 산출**된다.

- **공유 발사 (권장)**: 현행 gamma-DATA-channel/derivtrace warm-FT 사이클에 FM-cell(B-3)·모순쌍(B-4)을 **corpus arm**으로 동승 — 같은 pod, 같은 ckpt 계보, 같은 `evaluate --py` 배터리. 단 귀속(attribution) 위해 arm 분리 필수: {derivtrace-only} vs {derivtrace+FM} vs {FM-only}. 두 레버가 같은 법칙(coverage-density)의 두 사건이라는 A-2 가설상, FM-cell이 G1에 주는 간섭은 작을 것이나 측정으로 확인.
- **G6 전용**: B-5(consequence-return)·B-6(에피소드)·B-8(G-refuter curation)은 데이터 구조가 G1 조합축과 무관 — 별도 arm이되 배터리는 공유.
- **주의**: G6≡G1(H_1603)이지만 FALS는 composition 위에 refutability 추가 — derivtrace가 G1을 열어도 FALS는 δ_FM 없이는 안 열린다는 게 본 분석의 예측. 역도 성립(FM-cell이 FALS만 열고 G1 불변이면 두 벽의 분리 증명 = 그 자체가 판정 가치).

---

# 🎯 다음 STEP-0 발사 top-3 (전부 mini 가능, $0)

1. **B-1+B-9+B-11 통합 분해 게이지**: 기존 G6 decode 로그에 5-conjunct 개별 채점 + λ_ascii + digit율. 산출 = "죽은 conjunct 지도" → B-3 corpus 설계 조준. (기존 로그 부재 시 설계만 두고 다음 pool 배터리에 훅.)
2. **B-2 δ_FM corpus 스캔**: 4-cell corpus의 δ_FM·PMI·fit₄₀. 예측 δ_FM≈0 — 이 하나로 corpus-기아 가설의 사활 판정, G1 coverage 0.95/0.03 결과의 FALS판.
3. **B-3/B-4/B-12 mini numpy 3-arm A/B**: char-LM d64, {hi-δ 세그먼트형 / 모순쌍 / unless-꼬리 문장형} vs lo-δ 통제, held-out frame, FALS + M_earned(B-10 통제 동봉). DIRECTIONAL 상한 명기 — terminal은 303M warm-FT `anima evaluate --py`로만 (a_engine_native_learning).

★check-ledger 준수 확인: scaffold/decode·attention-capacity·set-search 재발사 없음. H_6163은 substrate-lane 원안이 아닌 curation-루프로 좌표 이동, H_1835(에피소드)는 판정축 상이를 카드에 명기 조건으로만 제안. 본 응답은 발산 설계이며 발사·bookkeeping은 하지 않았습니다(`fable-design-analysis-only` 정책).