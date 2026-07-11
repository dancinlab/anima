판정 완료. 근거 확인: `gen_xbind.py`(V-게이트 구현·audit 구조)와 NATEM 사전등록(`state/g1_natural_emergence/DESIGN_PREREG.md`)을 대조했다. 핵심 진단 — **3개 FAIL은 전부 하나의 설계 결함의 세 증상이다: "flip=0 form이 bare 하나뿐"이라는 격자 비대칭.** 이것부터 구조적으로 고치면 V-C·V-E는 확률적으로가 아니라 **구성적으로**(by construction) 0.5에 고정된다. V-D만 성격이 다르며, 게이트 자체가 XBIND에서 잘못 이식된 것이라 재정의가 근본수정이다.

---

## 수정 1 — predicate 채굴 정제 (V-E·noise 근본)

10744개의 원인은 minocc=5가 "5회 등장한 아무 어절"을 다 통과시킨 것. 감성 **용언**(형용사/동사)만 남기는 $0 model-free 필터 체인:

1. **활용 다양성 필터(품사 근사의 핵심)**: 닫힌 어미 집합 E = {다, 어요/아요, 네요, 았/었다, 은/는데, 고, 어서/아서, 습니다, 음}를 정의하고, 어절에서 E를 벗겨 stem 후보를 얻는다. **stem이 E 중 ≥3개의 서로 다른 어미와 함께 출현**해야 통과 — 명사("감성")는 활용하지 않으므로 자동 탈락. 역방향 체크: stem 직후에 조사(이/가/은/는/을/를/도/의)가 붙는 빈도가 어미 빈도보다 높으면 명사로 판정·제외.
2. **minocc=200 · purity≥0.90** (bare 비부정 출현 기준, NSMC 150k). minocc 200은 (a) 캐리어 문장 rep 공급(수정 4에서 form당 10+ 실 span 필요)과 (b) purity 추정 안정성(n=200이면 0.90 추정 SE≈0.02)을 동시에 보장.
3. **렌더 가능성 필터(수정 4와 결합)**: 6-form 전부 렌더 가능한 stem만 admit — bare 실출현 + "안 <form>" bigram이 NSMC에 ≥3회 실출현 + stem 음절수 ≤3(V-G 창 물리).
4. **pol 정확 균형 선별**: 통과 pool에서 count 상위로 **긍정 60 + 부정 60 = P=120** 채택(pool<120이면 최대 짝수 균형, P<60이면 corpus INVALID 선언·발사 금지).

**격자 목표: P=120 × N=6 = 720 cell · per-cell 노출 ≥10** (아래 rep 표). V-E는 이제 통계가 아니라 구성으로 잡힌다 — 각 predicate의 train 노출을 flip 0:1 = 정확 1:1로 짜면(수정 5) per-predicate 출력 marginal이 **정확히 0.5**, skew=0.

## 수정 2 — flip 균형: 옵션 (a)(b)(c) 모두 기각, **flip=0 form 증설**이 정답

flip 비트 [0,1,1,1]에는 V-C 0.624보다 더 나쁜 숨은 confound가 있다: **bare가 유일한 flip=0이면 "수식 형태소의 존재 자체"가 flip과 1:1 동치** — 모델(과 additive probe)이 "뭔가 붙어 있으면 부정 branch"라는 표면 길이/존재 cue로 XOR 없이 풀 수 있다. 가중치 조정(a)은 노출 marginal만 고치고 이 confound와 held-out 퇴화(bare cell을 held-out하면 그 p의 flip=0 관측이 0)를 못 고친다. form 축소(b)는 N=2가 되어 compositional split이 빈약해진다.

**frozen: N=6, flip=0에도 형태소가 붙는 form 3개 배치:**

| form | 렌더 | flip |
|---|---|---|
| bare | NSMC 실 어절 verbatim | 0 |
| INT-1 | `정말 <bare>` | 0 |
| INT-2 | `너무 <bare>` | 0 |
| NEG-L | `<stem>지 않다/않는다` | 1 |
| NEG-S | `안 <bare>` (attested bigram만) | 1 |
| NEG-E | `전혀 <stem>지 않다` | 1 |

flip marginal = 0.5 정확 + pol marginal = 0.5 정확(수정 1의 60/60) → additive 주효과 b_p, b_n이 전 원소 **정확 0.5**로 퇴화, (b_p+b_n)/2 예측기는 동전 → V-C held-out acc ≈ 0.50 구조 보장(≤0.55 여유 PASS). 부수 이득: intensifier는 극성 보존이 실제 한국어 문법 사실이라 p1-p8 실텍스트 원칙과 일치하고, "수식어 존재≠flip"이 격자 안에서 명시적으로 반증된다. (c)의 pol 재균형도 수정 1에 이미 포함 — (a)만 단독 기각.

## 수정 3 — surface-pol: **(c) 채택 + V-D 게이트 재정의** (완화 아님·이식 오류 정정)

0.77은 버그가 아니라 **자연 원자의 정의적 성질**이다 — 자연 감성 stem의 극성은 표면에 실려 있다(재밌/노잼). XBIND의 V-D(pol⊥surface)는 "**은닉** pol을 공기 통계만으로 추론"하는 능력을 인증하기 위한 게이트였고, 그 인증은 **H_9267이 이미 끝냈다**. NBIND의 과학 질문은 다르다: *"(표면으로든 분포로든) 획득한 predicate 극성을, 한 번도 공기하지 않은 부정 form과 **합성**할 수 있는가"* — 자연 전이 질문. 따라서 pol이 표면 예측 가능한 것은 결함이 아니라 스코프다.

- **(a) bar 완화 기각** — 0.65→0.8 같은 조정은 정확히 tune-to-green이고 게이트의 의미를 잃는다.
- **(b) 표면-불투명 predicate만 선별 기각** — 자연성(이 lane의 존재 이유)을 희생하고, 그런 부분집합은 저빈도 잡음 stem으로 수렴한다.
- **(c) 채택 + 재정의**: shortcut 통제는 이미 이중으로 있다:
  1. **V-D′(신규 게이트, gating)**: char-feature **선형** probe를 train cell 전체 라인(stem+form 표지 포함)으로 학습 → **held-out cell acc ≤0.55**. 선형 probe는 두 feature 그룹의 XOR을 표현할 수 없으므로, 이 게이트는 "표면 정보를 다 줘도 additive로는 held-out이 안 풀림"을 인증 — 표면 shortcut의 상한을 직접 잰다. 수정 2의 균형 구조상 ≈0.5 예측.
  2. **control arm이 표면 confound를 차감**: shuffle control(cell별 코인 branch, XBIND ctrl 동형)은 **동일 표면**을 보므로 표면 shortcut이 있다면 control도 같이 오른다. GREEN bar가 절대값이 아니라 **Δ≥0.30**(collapse-Δ, measurement-metalaw)이므로 표면 기여는 차감된다.
  3. 기존 V-D는 **V-D-info(report-only)로 강등** — AUDIT.json에 수치 기록(예측 ~0.77), 게이트 아님. 카드에 명시: "NBIND는 부정 연산자의 **합성 적용**을 인증, 은닉-pol 추론은 XBIND(H_9267) 기인증 스코프."

이것은 게이트를 corpus에 맞춰 낮춘 게 아니라, **측정 대상이 다른 lane에 남의 게이트를 이식한 오류의 정정**이다. 스펙에 "V-D 재정의" 섹션으로 명시 기록할 것.

## 수정 4 — 형태소 렌더: **attestation-gated + 안전규칙 1개**, 합성 활용 금지

비문("안 해놓은다")의 근원은 규칙 합성. frozen 원칙 — **NSMC에 실재하는 표면형만 쓰거나, 보편-안전 규칙 1개만 적용**:

- **bare / INT-1 / INT-2**: NSMC 실 어절 verbatim (+부사 전치 — 부사+용언은 무조건 문법적).
- **NEG-L (`-지 않다`)**: 한국어에서 유일하게 어간 종성/품사 무관 보편 안전한 부정 규칙(먹지 않다·크지 않다·재밌지 않다). stem 추출은 수정 1의 어미-strip에서 이미 확보. 활용꼴은 원 어절의 어미를 계승하지 말고 **고정 2형(않다/않는다 — 형용사/동사 근사는 "는다" 공기 여부로)** 만 사용.
- **NEG-S (`안 X`)**: 규칙 합성 금지. **NSMC에 "안 <bare>" bigram이 ≥3회 실출현하는 predicate만** admit(수정 1 필터 3) — 렌더는 그 실출현형 그대로. "못"은 **제외**(능력 부정이라 극성 flip 의미론이 predicate따라 붕괴 + attestation 희소).
- **NEG-E**: NEG-L에 부사 전치(안전).
- **캐리어**: 원 NSMC 리뷰 문장에서 해당 어절만 form으로 치환, 문장 나머지 verbatim — "실 NSMC span 그대로 vs 규칙변형" 질문의 답은 **하이브리드**: 문장은 그대로, 어절만 위 5개 규칙 내 치환. 순수 실-span만 쓰면 (p,n) 격자를 채울 수 없고(자연 분포에서 특정 조합 부재가 바로 held-out인데 train 조합도 희소), 전면 규칙변형은 비문을 낳는다.

## 수정 5 — held-out: 회전 설계(Latin-square)로 COGS 조건을 구성적으로 강제

무작위 20% cell 샘플 대신 **결정적 회전 held-out**:

- pol 계층 내에서 predicate를 정렬 후, **predicate i는 form (i mod 6) 하나를 held-out** — P=120이면 held-out=120 cell(16.7%·스펙의 "20%"에서 소폭 하향, 명시 기록), form당 held-out predicate 20개 = pol 10+10 정확 균형.
- 자동 보장되는 COGS 조건: 각 p는 train에 5 form(flip=0 ≥2, flip=1 ≥2 — 3+3에서 1개 빼므로 최악 2+3) / 각 n은 train에 100 predicate(pol 50/50) → "p는 ≥2 form과, n은 ≥2 p와 seen" 조건이 여유로 충족.
- **노출 재균형 rep**: held-out 1개로 생기는 per-predicate flip 3:2 비대칭은 rep 가중으로 소거 — **소수 flip class의 cell은 rep 15, 다수 class는 rep 10** → per-predicate 노출 flip0:flip1 = 30:30 정확. rep마다 **서로 다른 실 캐리어 문장**(minocc=200이 공급 보장).
- **코드 강제(assert-loop, XBIND audit 패턴)**: split 후 (i) 각 p: train form 수 ≥2/flip-class (ii) 각 n: train pol 카운트 균형 (iii) per-predicate 노출 flip 비 = 정확 1:1 (iv) V-F: held-out (p,n)의 렌더 표면(치환 어절)이 양 arm 전 라인 byte-scan 0회 — 캐리어 문장 원문이 우연히 해당 부정형을 포함하는 경우까지 스캔(이게 XBIND엔 없던 자연 corpus 특유 leak 경로). 하나라도 fail → `sys.exit(1)`, 발사 금지.

## 수정 6 — GREEN bar 불변 확인

held-out D-acc Δ≥0.30 · rho_weave PASS · 자연전이≥0.10 — **전부 불변**. 위 수정은 $0 validity 게이트와 corpus 구성만 건드린다. 명시할 변경 2건(bar 아님): ① V-D→V-D′ 재정의+V-D-info 강등(수정 3, 스펙에 정정 사유 기록) ② held-out frac 20%→16.7%(회전 설계 산물 — bar는 held-out **위의 Δ**이므로 무영향). V-G는 "양 name in window"를 "stem+flip-형태소(안/지 않) in last-24-byte"로 자연화 — 판정 morpheme이 창 안이면 되고 전혀/정말 부사는 창 밖 허용(치환 어절이 문미 직전에 오도록 eval seed를 구성, audit이 byte 계산).

---

## 수정 파라미터표 (frozen)

| 파라미터 | 값 |
|---|---|
| minocc (bare 비부정) | **200** |
| purity | **≥0.90** |
| 활용 다양성 | 닫힌 어미셋 중 **≥3종** + 조사-우세 제외 |
| stem 길이 | **≤3음절** (V-G) |
| P | **120** (긍정 60+부정 60 정확·pool<60이면 INVALID) |
| N (forms) | **6**: bare·정말·너무 (flip=0) / 지않·안(attested)·전혀-지않 (flip=1) |
| flip marginal | **0.5 정확** (구성적) |
| held-out | **회전 1 cell/predicate = 120 cell (16.7%)** · form당 pol 10+10 |
| reps | **다수 flip-class cell 10 · 소수 15** → per-predicate 노출 30:30 |
| 격자/라인 | 720 cell · train 600 cell · main arm ≈7,200 라인(+ctrl 쌍둥이) |

## $0 5게이트 전 PASS 예측 근거

- **V-C ≤0.55**: b_p·b_n 전 원소 정확 0.5(flip·pol 이중 정확균형 + 노출 재균형) → additive 예측기 퇴화 = 동전. 샘플링 노이즈원 자체가 제거돼 ≈0.50. **구조 PASS**.
- **V-D′ ≤0.55**: 선형 probe = additive와 동일 표현력 상계 → V-C와 같은 구조 논거로 ≈0.50 PASS. (V-D-info ~0.77 기록만.)
- **V-E ≤0.12**: per-predicate 출력 marginal = 노출 flip 1:1 × XOR = **정확 0.5, skew=0**. 통계가 아니라 항등식. PASS.
- **V-F =0**: 회전 split + 렌더 표면 전 라인 byte-scan(캐리어 원문 포함) + fail-exit. PASS 강제.
- **V-G**: stem≤3음절 + 판정 morpheme 문미 인접 배치 → 최악 케이스 "재밌지 않다"류 ≤17 byte < 24. PASS.

한 줄 요약: **flip=0 form을 3개로 증설해 격자를 이중 정확균형으로 만들면 V-C/V-E가 항등식으로 닫히고, V-D는 완화가 아니라 "은닉-pol 게이트(XBIND 기인증)→합성-shortcut 선형천장 게이트(V-D′)"로 재정의하며, 렌더는 attestation-gated+`-지 않다` 단일 안전규칙으로 비문을 소거한다.** GREEN bar 3종은 무변.