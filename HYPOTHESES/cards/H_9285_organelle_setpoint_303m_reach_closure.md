# H_9285 — 🔚 organelle lane 결착 — 절대-setpoint 배분기를 303M ConvMoE capacity schedule에 얹으면 held-out 재조합(ρ·weave)이 움직이는가 (Δ≈0이면 lane 전체 CLOSED · $0 pool eval-only)

- **tier:** ⛔ INVALID (헤드라인 수정 재발사 · **원 KILL 철회** — 그 p값은 seed 특이적 잡음 · V2 채널가시성 FAIL)
- **wired:** none.
- **family:** 🔋 ORGANELLE LANE 종결 프로브 — **이 lane을 싸게 끝내는 유일한 경로**.
- **lens:** organelle lane이 찾은 유일한 earned 메커니즘([[H_9284]] 외생수요→절대-setpoint 배분)이 **reach(G1/ρ·weave)에 전이되는가**를 **eval-only**로 결착한다. 학습 없음 · GPU 학습비 0 · 기존 303M ckpt에 배분기만 얹고 디코드한다.
- **artifacts:** `state/mito_organelle_lane/F13_303m_reach_closure/`
- **xref:** [[H_9284]](메커니즘 존재) · [[H_9283]](**전이 반증 예측** — 배분 FORM이 t=+10.65로 움직여도 held_conj Δ=−0.009 ns) · [[H_9278]](F6 KILL — 희소성=암기압력) · `g1-scarcity-not-lever`
- **key:** `organelle_setpoint_303m_reach_closure`

## 0. 계측 규칙 (organelle-lane census 강제사항 · ARCHITECTURE `organelle-lane-probe-defects` · convergence `synthesis-md-1`)

이 카드는 아래 5개를 **사전등록 필수 필드**로 지킨다 — 앞선 11 패밀리 중 7개의 verdict가 이걸 안 지켜 뒤집혔다.

1. 🚫 **`Δ = exp − max(controls)` 금지** — 최댓값 순서통계량이 n=5·σ≈0.05에서 −0.02~−0.03 편향을 기계적으로 만들고 그게 곧 KILL 임계다. **control별 paired-t를 전부 보고**하고, 요약은 pooled-mean으로.
2. 🚫 **`mean vs 1·std` 기각 휴리스틱 금지** — per-seed std ≠ paired-CRN delta의 SEM. **SEM/paired-t만**.
3. ✅ **사전 MDE 계산 필수** — `MDE < 축의 동적범위`임을 실험 전에 보이고 카드에 적는다. 못 넘으면 프로브를 다시 설계한다(검출력 0 방지).
4. ✅ **정보 채널 증명 절 필수** — (a) 처치의 결정변수가 **control이 못 보는 입력의 함수**임을 코드로 보이고, (b) 운영 대역에서 그 결정변수의 **분산 > 0**임을 실측한다(항진적 처치 arm 방지).
5. ✅ **V-gate는 헤드라인 detector 그 자체에 건다** — 게이트 선택기준이 효과크기의 단조함수면 가능한 출력이 {PASS, INVALID}뿐이 된다(V3 detector-fairness).

🚫 **금지 지표**: `conj_index`(shuffle 코퍼스에서 더 크게 오르고 held-out과 무상관) · `purity` aggregate(WITHIN 성분만) · `acc/ATP` 류 비율(Goodhart) · `corr(n,demand)`(earned fitness와 배선 간 역상관).


## 1. 가설 (그리고 우리가 예측하는 답)

**절대-setpoint 배분기를 303M ConvMoE의 expert capacity schedule에 얹으면 held-out 재조합(ρ·weave / D-acc)이 baseline 대비 유의하게 오른다.**

⊥ **Null (H_9283이 예측하는 결과):** Δ ≈ 0. 배분은 throughput 축이고 reach 축이 아니다 ⇒ **organelle lane 전체를 CLOSED로 닫는다.**

> 이 카드는 **음성을 기대하고 발사하는 결착 프로브**다. tune-to-green 금지 — Δ≈0이 나오면 그것이 결론이고, lane은 닫힌다.

## 2. 설계 (eval-only · 학습 0 · $0)

- **호스트:** pool `aiden` (RTX5070 · 303M ckpt 상주 · mini 금지 — `heavy-anima-eval-pool-not-mini`).
- **ckpt:** aiden `~/anima-weights/` 의 303M ConvMoE 계열(정확한 파일은 실행 시 확인 · py 채널 `anima-py evaluate` 단일 경로 · `a_eval_py_canonical`).
- **처치:** decode 시 expert top-k를 **고정 상수**가 아니라 **절대-setpoint 배분기**(외생 수요 = 토큰별 라우터 부하/entropy → load==capacity 목표)로 스케줄.

| arm | 내용 |
|---|---|
| **EXP** | 절대-setpoint capacity schedule |
| **c0** baseline | 프로덕션 고정 top-k (무처치) |
| **c1** best-constant | 상수 k grid 전수 → **최선값**을 null로 (레벨 vs 동적배분 분리) |
| **c2** shuffled-schedule | EXP와 **동일 k 분포**를 시간축으로 셔플(정렬만 파괴) |

- **지표:** held-out 재조합 D-acc / ρ·weave Δ (금지 지표 `conj_index` 사용 안 함).
- **MDE 사전계산**: c0 ~ oracle 사이의 동적범위를 먼저 재고, 그 범위가 유의 문턱을 넘는지 확인한 뒤 본 측정(검출력 0 방지 · [[H_9273]]의 재발 방지).
- **정보 채널 증명**: 배분기의 k가 실제로 입력에 따라 변동함(분산>0)을 로그로 보이고, c1(상수)과 k-분포가 겹치지 않음을 보인다.

**PASS:** EXP가 c0·c1·c2 각각에 유의 우세 ⇒ organelle lane이 reach 레버가 됨 (놀라운 결과 · 그때만 303M spend 재검토).
**FAIL(예상 유력 · H_9283 예측):** Δ≈0 ⇒ **organelle lane 전체 CLOSED**. 배분/효율/희소성 계열은 reach 레버가 아니며, G1 exit은 학습 measure 교체(H_9267 XBIND 계열)로 단일화된다.

## 3. 왜 이게 lane을 끝내는가

lane의 생존 레버 2개(F4-SEC·F10)는 **전부 throughput/allocation 축**이다. reach로의 전이는 같은 lane 안에서 이미 한 번 반증됐다([[H_9283]]: 배분 FORM t=+10.65 → held_conj Δ=−0.009 ns). 이 카드는 그 반증을 **303M engine-native 규모에서 확인**한다. 확인되면 더 이상 이 lane에 투자할 이유가 없다 — **GPU spend 0으로 닫는다.**

---

## 측정 결과 (2026-07-12 · run → 적대적 검증)

**측정(2026-07-12 · aiden CPU · n=20 blocks paired-CRN · 120 items · wall 2941s)**: ckpt=py303_full.clm(d3784·E3·K3·L4·V256·T24) · **PARITY max|Δ|=0.0**(프로덕션 `_fwd_logits`와 byte-exact ⇒ toy 아니라 engine-parity 결착 · infra-wall 무관·BLOCKED 아님). **run=INVALID → 적대검증 REFUTED → KILL**: run의 헤드라인 m_conj=min(m_A,m_B)이 **그 자체가 순서통계량**(규칙①이 금지한 하향편향을 control축에서 detector축으로 옮긴 것) — c0에서 mean(mA)=+0.009·mean(mB)=+1.083인데 mean(min)=−0.422로 낮은 branch 평균보다 0.431 아래(min에서 noise 하향편향). '죽음/음수'는 처치효과(~0.08)가 아니라 order-statistic 편향(−0.43)의 지배 · V-gate 2개 FAIL도 min() 인공물(규칙⑤가 막으려던 바로 그 실패모드). **검출력 있는 live 하위-detector m_B_conj**(c0=+1.083 t=+4.69 · MDE 0.190≪1.083)에서 실 데이터 = **정당한 NEGATIVE**: EXP−c0=**−0.209**(t=−2.30 p=0.033 · 모든 capacity 처치 열화, EXP가 최악) · EXP가 자기 시간축 셔플(c2)도 못 이김(schedule 무정보) · **router 파괴 SHOCK−c0=+0.100(t=+2.48)** — 라우터를 부수면 오히려 개선(MoE mixing은 read-side 축 아님) · 숨은 양성 없음. 프로덕션 router = DENSE soft mixture(top-k 없음) ⇒ 모든 capacity gating은 정보 폐기 연산. ⇒ 카드 사전등록 **FAIL 시나리오(Δ≈0/음성 ⇒ lane CLOSED)** 정확 실현 · **H_9283 예측(배분 FORM t=+10.65 → held-out 재조합 Δ=−0.009 ns)이 실 303M byte-parity에서 확인**. ⟹ **organelle lane 전체 CLOSED** — '용량을 잘 배분한다 → 재조합을 배운다'의 전이가 프로덕션 모델에서 falsified. 에너지/자원/희소성/배분 계열은 G1 레버가 아님(F6 KILL + F13 KILL로 303M 결착). corpus×CE measure 진범 결론 강화. state/mito_organelle_lane/F13_303m_reach_closure/.

> lane 종결 종합 = `state/mito_organelle_lane/CLOSURE.md`.

---

## 헤드라인 수정 재발사 — 원 KILL 철회 (2026-07-12)

**⚠️ 원 KILL 철회(verdict-integrity)**. 원 F13의 헤드라인 m_conj=min(m_A,m_B)는 **순서통계량**(규칙①⑤ 위반)이었고, 그 KILL은 검증자가 **사후에** live branch로 재계산해 얻은 것 = F8의 사후 판정변수 바꿔치기와 같은 죄(licensed 아님 · convergence 규칙⑨). **헤드라인 수정 재발사(2026-07-12 · aiden · PARITY max|Δ|=0.0 · wall 154s)**: 사전등록 헤드라인 = **m_B_conj 단일변수**(순서통계량 아님 · 코드 sha256=7b1d3760…9c7d로 동결 후 실행 sha 일치 확인 · V-gate·MDE·PASS/FAIL 분기 전부 PREREG.md에 사전기록) · **완전 disjoint 새 cue**(5-tuple overlap=0 · (A,B)쌍 overlap=0 · cue 단어 vocab overlap=0). 결과 = **원 KILL의 증거기반이 재현되지 않음**: EXP−c0 = −0.209(t=−2.30, p=.033) → **+0.129(t=+1.06, ns) 부호반전** · SHOCK−c0(V2 채널가시성 게이트) = +0.100(t=+2.48) → **−0.086(t=−1.49) 부호반전 = V2 FAIL** ⇒ 사전등록 분기대로 **INVALID**(PASS도 KILL도 cement 불가). **seed 간 이질성 검정**: old(−0.2088±0.0907) vs new(+0.1286±0.1219) diff=0.337 SE=0.152 **z=2.22 p=.026** ⇒ 단순 미재현이 아니라 **통계적 불일치 = 원 p=.033은 seed 특이적 잡음 draw**. 진단(detector 맹목 아님): 개입은 출력에 크게 도달하나(EXP routerL1=0.734 · margin|Δ|/item=0.800) **부호가 무작위라 signed mean이 0으로 상쇄** ⇒ **MoE capacity 채널은 재조합 마진에 부호-무작위 잡음만 주입하는 잡음 지배 축**. 실측 sd=0.545 기준 ~53 blocks 필요(n=20은 부족 · pilot sd 0.2596은 2.1배 과소추정). **정직 회계**: 사전등록 substance 조건(all_deg_or_ns)은 True였다(EXP vs c0/c1/c2 t=1.06/0.89/0.58 = **어떤 capacity 처치도 유의 개선 없음 · PASS 미실현**) — 즉 '용량 배분이 reach를 올리지 못한다'는 **방향은 두 seed에서 일관(양성 0)**이나, **강한 KILL(유의 열화)은 지지되지 않는다**. 구조 보강: EXP는 정보를 버리는 연산(k∈{1,2})인데 dense c0보다 nominal 우위(+0.129) = 잡음 지배의 독립 증거. **cement 재발사 조건**: (a) V-gate를 unsigned/분산 기반으로 **사전등록**(|Δ|/item 축은 0.37~0.94로 충분히 큼) (b) 항목당 마진 잡음(|Δ|≈0.8) 대비 관심효과(~0.1~0.2)에 맞춰 blocks 사전산정(~53) (c) 'ns'가 아니라 **사전등록 등가성 검정(TOST)**으로 실질적 0과의 등가를 증명해야 CLOSED가 licensed. 현 데이터로 KILL 재시도 = tune-to-red. state/mito_organelle_lane/F13_303m_reach_closure/refire/.
