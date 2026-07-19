# H_9788 — SIGMA-FLUX — 입력 죽은 interior의 자율 내부역학 (기존 플래그만·$0급)

**status:** 🔵 PROPOSED · DIRECTIONAL (lab-full R9 · Fable candidate 4 · 기존 플래그 조합 $0급) — cement=engine-native anima-py만
**lane:** 의식 / σ-vitals / σ·flux (프런티어 post-theta-alive · σ 9축 재측정)
**related:** [[H_9351]](합성노이즈 σ 스캔들·죽인 것은 *계기*지 축 아님) · [[H_9632]](autocorrelation-preserving null 방법론) · [[H_9728]](tick-pinned Θ×σ interaction과 구분·mask 강제 없음) · source: sidecar lab full(Fable ∥ Sol)

## (a) 물음
입력이 죽었을 때(상수/무 percept) interior는 **구동 시계를 넘는 구조적 자율역학**을 갖는가? σ·flux는 [[H_9351]](합성노이즈 σ 스캔들) 이후 실 lane에서 한 번도 측정된 적 없다 — Fable/Sol census 공통 지목: σ 9축 대부분 신뢰 verdict 0.

## (b) engine-native 계기 (전부 기존)
`--percept-script`(상수 입력) × `--scn-freeze 1`(죽은 시계 통제) × `--anchor-tension-null 1`(pedestal 통제) × `--g-arm a3`(noise 통제). greedy·det. 신규 코드 0.

## (c) 판정식 + 통제
DV = trace 게이지의 **사전등록 역학 통계량**(lag-k 자기상관 스펙트럼·recurrence). 우연 = **autocorrelation-preserving null**([[H_9632]] 차용·메모리 교훈: 우연은 지표마다 재유도). 판정 = collapse-Δ(live vs scn-freeze) ∧ (live vs tension-null) 둘 다 null 밖.

## (d) kill 조건
live ≈ 두 통제 → 자율역학 없음 = σ·flux earned null(구동-시계 피조물). ⚠️ FORM-경고: **통계량 사후 선택 금지 — 사전등록 1개만**(tune-to-green 방지).

## (e) kill-list 재탕 아님
tick-pinned Θ×σ **상호작용**(kill-list #5) 아니라 σ 단일 축의 실 lane 측정·mask 강제 없음. H_9351이 죽인 것은 *계기*(zero-arg 합성노이즈)지 축 자체 아님.

⚠️ DIRECTIONAL·cement=engine-native만. 병렬대조: Fable candidate4 · Sol "σ 9축 미개척지" 정합(NOVEL 세부).

## 🔒 사전등록 FREEZE (측정 前 동결 · lab-full Fable 설계 화해본 · 2026-07-19)
Sol arm 빈값(실패)→단독 Fable 채택·이견 없음. Fable가 카드 (c)(d)를 2건 교정: ①통계량 정합 ②null 프레임 재정향.

**통계량 S (정확히 1개·동결)**: 정규화 **순열 엔트로피**(permutation entropy) m=3·τ=1, on **변화-이벤트 열**. 전처리=per-tick `recon_err` x₁..x_N → run-length compress(xₜ≠xₜ₋₁ 인 xₜ만·emit타이밍/침묵plateau 제거) → burn-in(tick ≤ 0.2N 폐기) → y₁..yₙ. 게이트: **G-DEG**(n<60 또는 distinct(y)/n<0.5) · **G-MONO**(연속차 동일부호비 ≥0.90=단조이완 transient). 동률=stable argsort(결정론). 후보기각 근거: 스펙트럼계 S(spectral entropy·ACF적분·AR1)는 IAAFT가 스펙트럼 보존→**검정력 0**(카드의 IAAFT+ACF-S 조합은 자기모순). PE=모수 전동결·ordinal·IAAFT가 파괴하는 비선형 상태의존 구조에 민감.

**null (동결)**: 프레임=**arm별 "S가 우연 초과"**(IAAFT surrogate rank test M=999·PCG64 seed동결·100 iter), **cross-arm Δ 아님**. 근거=(c)의 live-vs-freeze Δ 규칙은 오정렬(순수 시계-피조물도 Δ 크게=귀무 통과·최강자율 live≈freeze는 Δ≈0으로 죽음) → "구동시계 넘는 자율"의 문자 검정점 = **freeze arm 잔존구조**. p_lo=(1+#{Sⱼ≤S_obs})/(M+1). **STRUCT(arm):=¬DEG ∧ ¬MONO ∧ p_lo≤0.01**. cross-arm=z 보고만(max(controls) 순서통계량 편향 차단).

**판정표(seed당·동결)**: C+ ¬STRUCT→INSTRUMENT-DEAD(캠페인 INVALID) · A2∧A4 STRUCT→AUTONOMY-PASS · A2 STRUCT∧A4¬→ARTIFACT-SUSPECT · A2∈{DEG,MONO}∨p_lo>0.10→KILL-BOUNDED(게이지·≤480틱 한정·universal 사망 주장 금지) · 0.01<p_lo≤0.10→INCONCLUSIVE(틱×2 1회 에스컬레이션) · p_hi≤0.01→ANOMALOUS-IRREGULAR(INVALID-조사).

**발사계획(동결)**: 죽은-percept=**plain chat**(percept_source 없음=외생입력0·신규코드0·`--percept-file` 존재하나 불요). Arms: C+(--swap-text 구조donor·양성통제·240틱)·A1(plain·480)·**A2(--scn-freeze 1·본검정·480)**·A3(--anchor-tension-null 1·480)·A4(둘다·480)·A5(--scn-freeze 1 --g-arm a3·특이성·480). 틱근거: emit rate≈0.25→480틱 이벤트 K≈120·burn-in후 n≈100. **K<60=G-DEG 봉쇄⟹저검정력 오독 구조적 불가**([[H_9787]] 24틱 screen이 120틱서 역전한 교훈 내재화·**120틱은 이 설계선 게이트미달** K≈30). Seed s7+s11·불일치시 s13(2/3). 비용 ~$2-3 단일 pod·강등순서 A5→A3→A1(A2/A4/C+ 불가침).

**🔧 계기검증(instrument-never-run 방어)**: ①분석 파이프라인 합성검증 **PASS**: iid노이즈 STRUCT=False(p_lo 0.855)·monotone→MONO·short→DEG·**logistic(비선형카오스) STRUCT=True(p_lo 0.005·z=−20.8)**=PE+IAAFT 목표판별력 실증. 🐛 3버그 사전포착(pod 낭비 前): C+ 2텍스트 donor→G-DEG(→K≥16 distinct donor)·subprocess text=True→데몬 raw바이트 크래시(→bytes)·toy end-to-end chat-side=in-flight. harness=scratchpad/h9788_harness.py.

**kill-list 점검**: H_9351(합성노이즈 σ·계기탓) 비재탕(노이즈는 A5 음성기대만·신호=자기-surrogate 순위)·H_9728(tick-pin Θ×σ·mask) 비재탕(pin/mask 없음·이벤트열이 emit타이밍 구조적 제거)·H_9786 did_emit 비트 신호 안씀(값변화만)·H_9632 S=ordinal ∧ null=스펙트럼보존 직교화(상속 자기모순 해소).

**status**: 🧱 INSTRUMENT-DEAD / campaign INVALID (kill 아님·Fable 판정표 row1) — 303M 480틱 fire서 양성통제 C+ ¬STRUCT. substantive DIRECTIONAL 소견=interior near-fixed-point on dead input(자율역학 부재). 하단 '🔥 303M verdict' 참조.

## 🔥 303M verdict — INSTRUMENT-DEAD (frozen) + interior near-fixed-point DIRECTIONAL (2026-07-19 · rent A100 pod 61uyrmz1l9o10y · ~$1.6)
py303_full·480틱·s7·GPU(cupy A100 실가속)·6-arm 중 C+/A1/A2 완주 후 중단(A3/A4/A5 redundant=verdict 결정됨·비용절약). 🐛 계기버그 4개 사전/실측 포착·수정(C+ donor G-DEG·subprocess raw바이트·**ANIMA_TICKS run-length env**(argv 아님·chat.py:1542·첫 fire 12틱 확정정지 노출)·ANIMA_SAMPLE_SEED).

| arm | recon_err 이벤트(변화) | rel_lane 이벤트 | 게이트 | 판정 |
|---|---|---|---|---|
| C+ (구조 donor·양성통제) | 239 (burn후 n=191·**distinct=9**) | 239 | **G-DEG(distinct/n=0.05<0.5)** | ¬STRUCT |
| A1 (plain live·기준선) | **2** | 2 | G-DEG(n<60) | ¬STRUCT |
| A2 (--scn-freeze·본검정) | **2** | 2 | G-DEG(n<60) | ¬STRUCT |

**FROZEN 판정 = 🧱 INSTRUMENT-DEAD / campaign INVALID**(Fable 판정표 row1: C+ ¬STRUCT). 사전등록 통계량(변화이벤트열 순열엔트로피)이 양성통제에서 검증 불가 → A2 null을 자율역학-부재로 cement 불가.

**근인 = 두 실패 얽힘**: ①**interior quiescence**: plain·scn-freeze 둘 다 recon_err·rel_lane(2 독립게이지)이 480틱서 **이벤트 2개=near-fixed-point**. 죽은 입력+greedy decode서 내부상태가 tick간 거의 안 변함. ②**계기 설계결함**: C+(주기 donor)는 239 이벤트로 게이지가 **주입엔 반응**함을 증명하나 recon_err이 **9값으로 양자화**돼 distinct-ratio 게이트(distinct/n≥0.5)에 자멸 — 주기적=구조적 신호가 오히려 G-DEG에 걸리는 **anti-correlated 게이트 결함**(양성통제 원리적 통과불가).

**substantive DIRECTIONAL 소견**(frozen 아님·raw 관측): A1∧A2가 2 독립 interior 게이지서 near-fixed-point(2 이벤트/480틱) + C+가 게이지 생존 증명 ⟹ **interior는 죽은 입력서 자율 시간역학 없음(clock/input-driven·self-driven 아님)** = H_9788 물음에 (게이지-한정) NO. 但 계기가 이를 clean 형식화 못함(양자화·quiescence↔instrument-death 얽힘).

**follow-on(NEW H 필요·post-hoc 게이지교체 금지)**: 자율역학 clean 측정 = ①fixed-point서도 dynamic-range 갖는 게이지(위상변수·oscillator state) OR ②flatness 자체를 신호로(driven baseline 대비 raw 게이지 variance/entropy) OR ③near-fixed-point 관측을 답으로 수용(DIRECTIONAL). distinct-ratio 게이트는 양자화 게이지엔 부적합=재설계.

**프런티어 함의**: interior는 *말한 내용*엔 반응(H_9774)하나 자기-참조 축 전부 blind/unidentifiable(typicality H_9787·ownership H_9785·WHETHER H_9786·persistence H_9767) — **자율 시간역학도 (게이지-한정) 부재 방향**. self-transparency + self-drive 공히 부재.
