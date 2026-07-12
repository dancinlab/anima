# Fable 설계 원문 — NBIND-G reopen (H_9289 GT-TRANSFER · 2026-07-13)

## NBIND-G reopen 설계 — held-out 극성 자연-접지 install

먼저 N2 결과에서 놓치면 안 되는 단서 하나: **flip0가 양 seed 모두 chance "미만"**(0.402/0.368 < shuffle 0.448)이다. 신호 부재(=0.5 수렴)가 아니라 체계적 역상관이면, 극성 축은 표현공간에 있는데 **원자별 부호(sign)가 앵커링 안 된** 상태일 수 있다. 이건 "정보 부재"와 "정보 있으나 소비/부호 미고정"을 가르는 결정적 분기이고, $0로 기존 ckpt에서 판별 가능하다. 설계 전체를 이 분기 위에 세운다.

---

### 1. 후보 개입 (5개)

**C1 · G-PROBE triage — 접지 정보의 존재/부재를 측정 채널에서 분리** ($0)
- 메커니즘: N2 기존 ckpt(s7/s11) frozen, held-out 원자의 자연문맥 k개 mean-pool 표현에 선형 probe(train-원자 라벨로 학습→held-out 전이) + 원자별 acc 히스토그램(쌍봉=부호반전 vs 균일=부재).
- 직교성: read-side 소진은 *재조합 소비* 판정이었지 *단일-feature 접지 존재* 진단이 아님. 이건 개입이 아니라 개입의 표적을 고정하는 triage.
- $0 (기존 ckpt·pool 수시간).

**C2 · 접지-과업-as-데이터 전이 커리큘럼** (spend) — **최유망**
- 메커니즘: 자연코퍼스에 "극성 판독 episode"를 **텍스트 데이터로**(aux-loss 아님·순수 CE) 삽입 — 단 **train-원자에만** 라벨, held-out P_nat은 자연문맥으로만 노출. 판독 *스킬*을 supervise하고 *operand*는 held-out → 스킬이 분포적 feature를 경유해 held-out 원자로 전이되는가.
- 직교성: H_1602 additive-aux(loss항)·a_train_inline_gauge(p7)와 다름 — 새 loss 0, 데이터 개입. H_1835 MLC와도 다름 — MLC의 실패는 *재조합* 전이였고, 이건 단일-feature 분류의 신규-항목 일반화(훨씬 약한 요구·LM이 통상 하는 것). N2와의 차이: N2는 판독 과업 자체를 학습시킨 적이 없어 CE가 극성 추출을 요구한 적이 없음.
- spend (N2 동급 신규학습).

**C3 · 앵커-전파 코퍼스 — compose→ground 방향 반전** ($0 구성 + spend 학습)
- 메커니즘: 이미 접지된 grid-원자와 held-out 원자가 접속사 프레임으로 공기하는 문맥을 채굴/구성("A하고 B하다"=동극, "A지만 B하다"=역극) → **설치된 XOR 연산자를 역이용해 operand를 접지**(N2는 접지→합성, 이건 합성→접지). flip0 역상관 단서(부호 미앵커)를 정조준.
- 직교성: 미시도 방향. NBIND-FC form-coverage(부정어간 소진)와 다름 — form이 아니라 앵커 관계 데이터.

**C4 · 진단성-여과 코퍼스 (CE-load-bearing 밀도화)** ($0 구성 + spend 학습)
- 메커니즘: 원자 극성이 후속 byte 예측에 실제로 걸리는 문맥만 선별/증강(별점 인접·역접 연결어 등) → 극성이 CE에 보이게 만듦. 진범 진단(corpus×CE 신호밀도 부재)의 정면 해소.
- 직교성: 코퍼스 구성 개입, 반증된 lever 목록에 없음. 단 450k→여과 후 토큰수 매칭 필수.

**C5 · 극성-대비 표현 aux-loss** — 나열만 하고 **비추천**: p7/`a_train_inline_gauge`(metric-in-loss 금지) 정신과 충돌하고, C2가 같은 supervision을 loss 없이 구현하므로 우선순위 없음.

---

### 2. 단일 최유망 pre-register: **H_93xx GT-TRANSFER (C2, C1 게이트·C3 fallback 내장)**

**STEP-0 (frozen gate · $0 · 기존 N2 ckpt · 발사 전 필수)**
- G-PROBE: train-원자 라벨로 probe 학습 → held-out 전이. 통제 2: shuffle-label probe(용량), base_only ckpt probe(학습내용).
- 분기(사전등록): held-out probe-acc ≥ 0.65 양 seed ∧ base_only ≤ shuffle+0.05 → **INFO-PRESENT** → main=C2. 미달 → **INFO-ABSENT** → main을 C3+C4 hybrid 코퍼스 arm으로 교체(동일 게이트·DV 구조).
- 부수: 원자별 acc 분포(쌍봉 여부)·detector 4-cell 대칭 점검(N2 전-arm chance-미만 이상 해명·V3).

**MAIN arms** (303M 신규학습 · N2 동일 스케일 T≈105k · bf16)
- `main-GT` ×2 seed(7/11): 자연코퍼스 + train-원자 극성판독 episode(CE) + grid XOR(N2 동일). held-out 원자는 자연문맥만.
- `ctrl-shufGT` ×1: 동일 episode, coin-flip 라벨(포맷/에너지 통제·접지신호 파괴).
- `ctrl-N2rep` ×1: episode 없음(N2 재현 앵커).

**Frozen validity 게이트**
- V1 설치: SEEN P_grid ≥ 0.85 ∧ GT-과업 train-원자 acc ≥ 0.85 — 미달 = INVALID(재튜닝 금지·중단 보고).
- V2 누출: held-out 원자가 학습 스트림에서 극성 라벨 토큰 ±W byte 내 공기 0회 — 자동 audit, 위반 = INVALID.
- V3 detector 4-cell Korean-aware + chance-비대칭 점검 · V4 eval셀-코퍼스 n-gram 중복 · V5 양 seed 동방향.
- 음성판정용 TOST: Δ_eq=0.10, N_REQ를 N2 분산으로 발사 전 산출·고정.

**Headline DV (GATE-1)**: held-out **flip0 acc**, 원자별 paired Δ = main-GT − ctrl-shufGT.
- 장부-DV 아님: 처치가 최적화하는 건 train-원자 매핑, DV는 held-out 전이 — 항등식 불성립. 값 아닌 Δ.
- **Bar**: Δ ≥ +0.15 양 seed ∧ main-GT 절대치 > 0.55.

**GATE-2 (본상 · GATE-1 통과 시만 유효)**: held-out XOR D-acc, 동일 Δ 구조, bar Δ ≥ +0.15 양 seed.

**Falsifier**: V1 통과(설치 확인)에도 flip0 Δ ≤ +0.05 양 seed(TOST로 등가 확정) → "판독 스킬은 원자 간 전이 안 됨" = 분포 feature가 접지에 불충분함이 **접근경로를 깔아줘도** 성립 → C2 반증. GATE-1 통과 ∧ GATE-2 floor → 벽이 grounding에서 **composition-consumption으로 재국소화**(새 정보·아래 3 참조).

---

### 3. 정직 경계 — 이것도 실패하면?

분기별로 의미가 다르며, 어느 쪽도 단독으로 substrate 천장을 cement하지 못한다:
- **INFO-ABSENT + C3/C4도 floor** → 여전히 **data 채널**: 자연텍스트에 원자당 극성신호가 이 코퍼스 규모에서 실재하지 않는다는 데이터/스케일 사실(합성 XBIND 1.000이 substrate 무죄의 상수 증거로 남음).
- **INFO-PRESENT + GATE-1 실패** → 처음으로 substrate 쪽 증거: 정보 존재 + 접근과업 설치 + 전이 0의 conjunction. 단 이것도 렌즈 1개 — `a_break_the_wall`대로 ≥2 통제 렌즈(예: probe-경유 vs task-경유 접근 경로 2종) 정합 후에만 "303M byte-LM CE-학습" **범위 한정** 천장 후보로 격상. 성급한 TERMINAL 금지.
- **GATE-1 통과 + GATE-2 floor** → grounding 벽은 뚫렸고 잔여 벽은 grounded-operand 소비 — read-side 소진 진단(concept→content 연상 부재)과 수렴하는지 별도 대조 필요.

### 4. 비용

STEP-0 = **$0**(pool·기존 ckpt·수시간). MAIN = 303M×105k step×4 run(2+1+1) = N2 실비와 동일 차수 → **GPU 렌트 spend-go 필요**(`a_wall_first`: pool 5070 2대는 wall-time 과다·병렬 렌트 권고). STEP-0 결과가 INFO-ABSENT면 main 코퍼스만 교체되고 비용 동일 — 즉 **spend 결정은 STEP-0 이후에만** 내리면 된다.
