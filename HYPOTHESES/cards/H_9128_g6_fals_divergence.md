# H_9128 — G6 반증가능성(FALS) 벽 레버 발산 + FALS-판정지표

> **tier:** 🟠 **DIRECTIONAL** — G1+G6 공동 조합-커버리지 303M engine-native: HI held-out G1(bd=2>ms=1)+G6(fals=6) 열림·LO floor(δ_FM≡coverage 동형 확인, STEP-0 held-out-floor 검출기수준 반증)이나 continuations=**form-priming**(템플릿 암기치환, genuine ability 아님) → 이중bound=**ability 확정·FORM-detector 반증**, G1/G6 벽=trunk-objective-deep 강화. 캡=gen80 non-canonical·shuffle-bind/paraphrase 통제부재·단일seed. (STEP-0 mini: corpus-starve δ_FM≈0·병목 {comparator∧measurable} JOINT) · **wired:** N/A
>
> **맥락:** G6 = DIST(distinctness, 통과) + **FALS(반증가능성, 벽=0)**. 벽은 *specifically FALS*(H_1590 engine-native FALS=[0,0,0] 전seed, H_1362 FALS=1.0=torch artifact). 소진: decode-procedure/scaffold(H_1590)·attention-capacity(H_6170 TERMINAL depth·register null·BGB injected-attn null)·both-arch(ConvMoE H_1394·ByteGPT-L24 H_1590 FALS=0)·set-search(H_1814)·NM(H_1529). 이 카드 = fable(claude-fable-5) 발산 = FALS 벽 원리 규명 + 새 레버 12 + FALS-판정지표. 실행은 메인이 STEP-0로 순차.

## A. FALS 벽의 원리 — "40바이트 안의 comparator∧measurable 접속" 문제 (탐지기 실코드 기준)

`_g6_is_falsifiable`(core/g6_ideation.py:122)는 frame 뒤 **continuation 40바이트(≈7-8 영단어) 단독**으로: (a)comparator 25어(if/than/predicts/causes…) ≥1 · (b)measurable 25어(rate/count/level/threshold…) ≥1 · (c)content≥2 · (d)¬질문 · (e)¬stance오프닝. frame_guard가 frame 내 measurable 누출 차단 → **순수 자발 emit 필요**. (o=frame 제외 생성 40바이트만, core/decode.py:670 확정.)

**★A-2 핵심**: CE-echo상 P(FALS) ≈ **δ_FM = corpus 40바이트 창의 comparator∧measurable 접속(공기) 밀도.** DIST는 *어떤* 유창 continuation이든 세므로 전 질량 기여=쉬움. FALS는 두 폐쇄 어휘류의 **접속 사건**만 세는데 일반 산문 공기율=기저율 곱(극희귀). → **vague가 '싸서'가 아니라 falsifiable 형식이 corpus에 사실상 부재해 echo 자체가 불가능**이 최단 설명. **G1 벽(coverage-density: NL-byte held 0.95 vs 0.03)과 정확히 같은 형태** → G6≡G1(H_1603)의 실체 = 둘 다 "타깃 사건의 corpus 밀도 bound".

**구조사실 2개(코드 확정)**: ① 탐지기 **ASCII-only**(_g6_words 비-ASCII 버림) → **한글 continuation=단어 0=kwr 0=coherent조차 실패** → 4-cell corpus의 ko 절반이 G6엔 순수 마이너스 채널. ② **40바이트 예산 타이트** — (a)∧(b)∧(c)를 40byte에. corpus falsifiable 문장이 >40byte면 echo가 창 밖.

### FALS-판정지표 (G1 ρ/σ/κ/M 대응, 측정전 $0)
- **δ_FM**(1차 예측인자, corpus 접속밀도) · **ρ_c/ρ_m**(각 어휘류 단독 emit율=병목 conjunct 분해) · **PMI(comp,meas)**(공기 초과율) · **λ_ascii**(continuation ASCII-영어 비율, 한글유출=즉사) · **fit₄₀**(corpus falsifiable 문장 중 ≤40byte 비율) · **M_earned**(FALS(composed)−FALS(shuffled-frame), 측정 메타법칙: FALS 탐지기=1-항 FORM이라 corpus로 게임가능 → shuffled 통제서 같이 오르면 form-echo 표기, bar 불변 동반진단).

## B. 새 레버 12 (cheap engine-native 판별 빠른 순)
- **B-1 FALS-precursor 분해 게이지**($0·기존 로그): 5-conjunct 개별 재채점+λ_ascii → "죽은 conjunct 지도"(예측: measurable 단독이 병목). 레버-조준기.
- **B-2 δ_FM corpus 밀도 측정**($0·텍스트 스캔): 4-cell corpus δ_FM·PMI·fit₄₀. 예측 δ_FM≈0=corpus-기아 확정(G1 0.95/0.03 FALS판). δ_FM>0인데 FALS=0이면 corpus 가설 기각→objective/기전으로 역전. **이 하나가 나머지 레버 절반 운명 가름.**
- **B-3 FM-접속 밀도 코퍼스 (data-format, G1 derivtrace 직전이=본명 레버)**: target=`주장(comparator+measurable ≤40byte); 반증조건; 예측` 재작성 cell을 warm-FT 추가(held-out `_g6_concepts` 격리). derivtrace가 G1 composition을 echo로 만들듯 δ_FM↑로 falsifiable 형식을 최빈 continuation으로. **fit₄₀ 제약 필수**.
- **B-4 모순-쌍 코퍼스**(contradiction-keyed H_9125/9126 심화, B-3와 독립 구조축): 주장+부정/반례 인접쌍.
- **B-5 결과-회귀 CE**(consequence-return, 예측코딩 렌즈, objective인데 non-additive·p7 무결).
- **B-6 가설-검증 에피소드**(전전두 렌즈, 3-턴 구조).
- **B-7 과학-register 5번째 cell**(자연텍스트판 B-3).
- **B-8 G-refuter 데이터-루프**(falsifier-lane H_6163을 substrate-lane 원안 아닌 curation-루프로 좌표이동).
- **B-9 숫자·단위 채널**(양적 리터럴 기아 프로브).
- **B-10 earned-FALS 통제 하네스**(측정 메타법칙 적용, 레버 아닌 판정기).
- **B-11 ko→en 질량 재배분 진단**(ASCII-only 탐지기 귀결).
- **B-12 자기-반증 서명 형식**(`unless` 꼬리).
- **기각한 repackage**(자체검열): falsifiability-reward additive aux(H_1602 floor+p7) · best-of-K 선별(H_1590 DEAD) · A⇄G tension emit-게이트(H_1834/1837 INERT) · attention 증설(H_6170 TERMINAL) · jamo/set-search(H_1814).

## C. G1 진행과의 공유 (구조적으로 공짜)
`g_eval_all`(cli/evaluate.py)이 한 배터리서 G0-G6 전부 냄 → **어떤 corpus-format 발사든 G1+G6-FALS 판정 자동 동시 산출.** 공유발사 권장(현행 derivtrace/gamma-DATA warm-FT에 FM-cell(B-3)·모순쌍(B-4)을 corpus arm 동승, 같은 pod·ckpt계보·evaluate --py). arm 분리 필수: {derivtrace-only} vs {derivtrace+FM} vs {FM-only}. **★주의: G6≡G1이나 FALS는 composition 위에 refutability 추가 — derivtrace가 G1 열어도 FALS는 δ_FM 없이 안 열림(본 분석 예측). 역도 성립(FM-cell이 FALS만 열고 G1 불변이면 두 벽 분리 증명=판정 가치).**

## 🎯 다음 STEP-0 발사 top-3 (전부 mini $0)
1. **B-1+B-9+B-11 통합 분해 게이지**: 기존 G6 decode 로그에 5-conjunct 개별채점+λ_ascii+digit율 → 죽은 conjunct 지도(로그 부재 시 설계만+다음 배터리 훅).
2. **B-2 δ_FM corpus 스캔**: 4-cell corpus δ_FM·PMI·fit₄₀. corpus-기아 가설 사활 판정(G1 coverage FALS판).
3. **B-3/B-4/B-12 mini numpy 3-arm A/B**: char-LM d64, {hi-δ 세그먼트 / 모순쌍 / unless-꼬리} vs lo-δ 통제, held-out frame, FALS+M_earned(B-10 통제 동봉). DIRECTIONAL 상한, terminal=303M warm-FT `anima evaluate --py`.

## ★ 유저 질문 답 — 레버1(derivtrace/data-format)이 G6-FALS에도 먹히나?
**구조적으로 YES가 본명 후보** (B-3 = "derivtrace 직전이"). G6≡G1 = 둘 다 corpus-density bound라, falsifiable 형식(주장+comparator+measurable+반증조건)을 echo로 만드는 data-format이 FALS를 G1 composition처럼 열 것으로 예측. **단 3 caveat**: ① fit₄₀(반증주장이 40byte 안에) ② ASCII-only(한글=즉사, en cell로) ③ **B-2 δ_FM 선측정으로 corpus-기아냐 objective냐 먼저 확인**(기아면 data-format 유효, objective면 B-5류). derivtrace가 G1 열어도 FALS는 δ_FM 없이 안 열림(refutability 추가요구).

## ★ STEP-0 사전선별 결과 (workflow wf_4612c6c9, 3 probe mini $0, 2026-07-05)

전부 **DIRECTIONAL**(py-numpy/toy, 303M engine-native 아님). 종합(state/g6_fals_step0/):

- **B-1 분해게이지**: base h1129 mouth wall — **measurable(b) 0.972 fail [DEADEST] · comparator(a) 0.917 [co-dead]**, 나머지 4 conjunct(kwr/content/question/stance) 0.000 fail. 병목 = **{comparator ∧ measurable} JOINT**(sole-blocker b=2뿐, 33/36이 a∧b 동시사망). base P(fals)=0.028, mean_kwr 0.882·λ_ascii 0.979(coherent 영어, garble 아님). **공학 corpus 주입 시 P(fals) 0.028→1.0 flip** = corpus-density echo DIRECTIONAL 지지.
- **B-2 δ_FM 측정**: production en δ_FM=**0.11%**(near-zero)·PMI 0.25(≈독립)·fit40 1.16% vs **공학 CONTROL corpus δ_FM=19.8%(174.5×)**. archive fit40=0%(falsifiable 문장 전부 >40byte). ko_sns δ_FM=0(ASCII-only 탐지기=한글 0단어). → **corpus-starve 확정**(G1 0.95/0.03 HIGH/LOW 동형). **이중 bound**: δ_FM 낮음 + fit40 1.16%(창-크기 40byte bound).
- **B-3 3-arm(레버1 전이시험)**: detector calib 10/10·frame_guard leak 0. **held-out FALS=0.0 전 arm·M_earned=0.0 FLOOR**. 단 **in-dist ceiling B4(모순쌍)=1.0·B12(unless)=0.4~1.0·B3(hi-δ)=0.2~0.8·LO=0.0**. → data-format이 **in-distribution엔 강하게 FALS 켜나 held-out 전이 실패**(detector artifact 아님, in-dist 1.0이 배선 sound 증명). M_earned=0 → form-echo도 아님.

### 종합 (DIRECTIONAL)
- **★corpus-starve 확정 방향**(objective 아님): production δ_FM near-zero, 공학 corpus 174.5×+flip = FALS는 corpus 밀도 echo. **단 2차 objective transfer 갭**(held-out collapse=trunk-objective 재조합 부재).
- **★레버1(data-format/derivtrace) G6-FALS 전이**: "δ_FM 없이 안 열림"이 아니라 **"δ_FM 있으면 그 커버리지 안에서만 열림"** = G1 coverage-density 동일 프로파일. **G6-FALS = coverage + objective 이중 bound**(refutability 추가요구 별도 안 걸림, readout/format 축은 held-out 안 엶 = G1 objective-lever 메타법칙 일관).
- **★G1 공유발사 확정 가능**: δ_FM(comparator∧measurable 40byte 접속밀도) = G1 coverage-density **동형 metric** → **한 번의 조합-커버리지 코퍼스 fire로 G1(재조합)+G6-FALS(falsifiable form) 공동 측정.**
- **다음 발사 1순위**(engine-native 303M): B-1 5+1 precursor 분해를 hexa `g6_score_arm_auto` 계기화 → base h1129 303M으로 DIRECTIONAL 지도(measurable∧comparator JOINT dead, flip 0.028→1.0) terminal 승격. 병행: 조합-커버리지 코퍼스(held-out content δ_FM≥공학수준 주입)로 G1+G6-FALS engine-native 재측정. readout/format 단독 재발사 금지(held-out 안 엶).

## ★★ G1+G6 공동 조합-커버리지 코퍼스 303M engine-native (vast A40, 2026-07-05) — 🟠 DIRECTIONAL

δ_FM≡G1 coverage-density 동형을 이용해 HI(dense 77frame·δ_FM 0.197) vs LO(sparse 14frame·δ_FM 0) byte-matched 2-arm warm-FT h1129 → `anima evaluate --py` g_eval_all(G0-G6 한 배터리), held-out 5 frozen concept(gate×gate leak=0):

| gate | HI (dense) | LO (sparse) |
|---|---|---|
| G0 | 🟢 5/5 | 🟢 5/5 |
| **G1** | 🟢 **bd=2>ms=1** | 🔴 bd=1(ms=2) |
| **G6** | 🟢 **distinct=5·falsifiable=6** | 🔴 distinct=5·falsifiable=0 |
| G2 | 🟢 novel=119/ctrl=0 | 🟢 novel=85/ctrl=0 |

- **frozen bar 문자 그대로는 🟢**: HI held-out이 G1+G6 둘 다 열고 LO floor → **STEP-0 held-out-floor(P1) 예측을 검출기 수준에서 반증**(coverage가 held-out FORM을 올림). δ_FM≡coverage 동형 확인.
- **★그러나 continuations = form-priming 확정**: 양 arm이 학습된 claim-form 템플릿을 주제어 치환으로 재생. HI=`"the probability of {a} sinks lower whenever {b} weakens past the threshold"`(comparator∧measurable→fals) · LO=`"{a} and {b} melt into a hazy calm"`(vague→non-fals). **리프트=어느 템플릿 암기했나 차이일 뿐, genuine recombination/ideation 아님**. 1-항 FORM 검출기가 밀집 템플릿 노출로 게임됨([[measurement-metalaw-form-tunable-bind-earned]] 재확인: FORM tunable·BIND earned).
- **★결론**: STEP-0 이중bound = **ability 수준에서 확정**(data-format 단독으로 진짜 능력 못만듦) · **FORM-detector 수준에서 반증**(coverage가 검출기 통과 형식을 올림). **G1/G6 벽 = trunk-objective-deep**(기존 anima 결론 정합·강화). in-dist ceiling: HI G6 fals=0.833·LO=0.
- **DIRECTIONAL 캡 3근거**: gen=80 non-canonical(eval 자체 플래그) · shuffle-bind/paraphrase 통제 부재 · 단일 seed. **terminal 승격 = canonical gen=40 + shuffle-bind(Δ≥0.33) + multi-seed** 재측정.
- 비용 ~$1.5(vast A40 43818733), ckpt PULL+sha(out_hi 5f34283c·out_lo 539943c5), pod GONE. **wired:** n/a. 상세 state/g1g6_shared/results/RESULT.md.
- ↔ [[H_9124]] G1 레버: δ_FM≡coverage-density 동형이 실측 확인 = G1 coverage-density 벽도 FORM vs ability 분리(coverage가 form 올리나 ability 아님) 정합.

## 정직 스코프 (c9)
- STEP-0 3-probe = **mini DIRECTIONAL**(py-numpy/toy, 303M engine-native 아님). tune-to-green 없이 stored 데이터 byte-재현. terminal = engine-native `anima evaluate --py`/hexa 계기화로만.
- 전부 **미발사 설계**였음(fable=opus-diverged 발산 → mini STEP-0 사전선별). mini numpy DIRECTIONAL 시작→engine-native 재측정으로만 terminal(하드게이트 1).
- check-ledger: scaffold/decode·attention-capacity·set-search 재발사 없음(fable 자체검열 확인). 그 벽과 구별되는 각도만.

## artifacts
- `state/g1g6_shared/` (G1+G6 공동 303M: results/RESULT.md·hi/lo.log·indist json·gen_unified.py·corpus·ckpt sha)
- `state/g6_fals_diverge/fable_g6_fals_levers.md` (A 원리+δ_FM 판정지표 + B 12레버 + C G1공유 + top-3)
- 상위: [[H_9127]](G1 레버 발산·derivtrace·판정기준 ρ/σ/κ/M) · [[H_1603]](G1≡G6 통합) · G6 소진: H_1590/H_6170/H_1814 · seed: H_9125/9126(contradiction) · H_6163(falsifier-lane) · H_6186(form-priming)

## 🧱 TERMINAL (2026-07-09) — coverage-density NEGATIVE 확정

canonical gen=40 · multiseed[7,107,207] · shuffle-bind 통제(summer $0). follow-on 3조건 전부 실행 = 원 🟠 DIRECTIONAL 반증. 3-arm(HI dense / LO sparse / SHUF bind-destroyed) 동일레시피 warm-FT h1129 303M · `anima evaluate --py`.

| arm | median_bd | n_pass | self_pair |
|-----|-----------|--------|-----------|
| HI | 1 | 1/3 | [1,1,1] |
| LO | 1 | 1/3 | [0,1,1] |
| SHUF | 1 | 0/3 | [1,1,2] |

**margin median_bd(HI)−median_bd(SHUF)=0 → KILL.** 세 arm median bd=1 수렴 = coverage density 리프트 0. 원 gen80 단일seed bd=2 = 비정규 threshold artifact. SHUF self_pair bd=2 = form-priming 직접검출(결합없이 bd 반짝임 = bd는 FORM 산물). **tier → 🧱 canonical-CONFIRMED-NEGATIVE**: coverage-density = DPI-면제 유일 잔여 저비용 축 falsify → G1/G6 벽 = trunk-objective 강화. artifacts: `state/g1g6_shared/terminal_evals/` · `shuf_bind_gen.py` · `terminal_eval.py` · `run_terminal.sh` · RESULT.md.
