# REFUTE — H_9285 CEMENT (adversarial audit of the EQUIVALENT-CLOSED verdict)

적대적 재계산: `cement_result.json`의 raw `items[]`(334 main + 50 pilot)에서 헤드라인·대조·TOST·disjointness를
독립 재산출. **결론: 반박 실패 — verdict = EQUIVALENT-CLOSED 유지(refuted=false). 단 주장 사정거리는
좁혀야 한다(아래 C1~C3).**

## 재현 검증 (전부 일치 · 조작/계산오류 없음)

| 항목 | 보고값 | 내 재계산 | |
|---|---|---|---|
| EXP−c0 | +0.0723 SEM .0533 t=+1.36 | +0.0723 .0533 +1.36 | ✅ |
| EXP−c2_shuf | +0.0882 SEM .0585 t=+1.51 | 동일 | ✅ |
| CI90(EXP−c0) | [−0.0156,+0.1602] | 동일 | ✅ |
| item sd | (SEM×√334)=0.974 | 0.9741 | ✅ |
| arms | c0 +0.311/.362 · EXP +0.383/.389 · SHOCK +0.297 · SHAM=c0 | 동일(SHAM−c0 = 정확히 0) | ✅ |
| disjointness | tuple/pair/cue 0/0/0 | **run-1(120 items)+run-2(130) 원본에서 union을 직접 재구성**(250 ab · 309 cue · 250 tuple)해 대조 → 0/0/0 | ✅ |
| `prev_exclude_all.json` | 사전 동결 | 재구성 union ⊆ exclude, 크기 정확히 일치(위조·누락 없음) | ✅ |
| sha256 | 03a915…4125 | 파일 재해시 일치 · PROBE_ONLY 분기는 **채점 전 return**(코드로 확인) = pool-probe가 결과변수를 못 봄 | ✅ |
| 규칙①②⑥⑦⑧ | PASS 주장 | headline 단일변수(순서통계량 0) · max(controls) 미사용 · 4분기 전부 도달가능 · ops 위반 2.22e−16 | ✅ |

체크리스트 1·2·5·6·7 = 반박 불가. 사전등록은 진짜다(코드 동결→실행→verdict 그대로 채택, tune-to-red/green 흔적 0).

## C1 (최대 약점) — signed 양성대조가 **없다**. unsigned V-gate는 zero-mean 잡음으로 통과 가능

- SHOCK = router **완전 파괴**(균등 mixing)인데 헤드라인 signed 효과 = **−0.014 ns**(t=−0.57), TOST p=4e−14로
  c0와 등가. ⇒ **이 DV의 평균은 router-mixture를 어떻게 건드려도(파괴해도) 안 움직인다.**
- V2b(unsigned |Δ|/item=0.765 > Δ_eq)는 "detector 안 맹목"의 증명이 **아니다**: EXP 변위를 **부호 무작위화한
  대리표본**(directed effect ≡ 0)을 만들어 넣어도 |Δ|=0.765, CI95_lo=0.700 → **V2 PASS**. 즉 unsigned gate는
  "0 방향효과" 채널도 통과시킨다. 게이트가 signed→unsigned로 바뀐 것은 run-2에서 signed가 FAIL한 **뒤**의
  완화다(run-3 데이터 이전이라 규칙⑨는 좁게 충족하나, lane 레벨에선 data-informed 완화).
- ⟹ 등가 licensing의 실제 근거는 V-gate가 아니라 **검정력**(sd .974 · n=334 · MDE_sup 0.131 < Δ_eq 0.20)이다.
  "V-gate 5/5 PASS ⇒ 등가 licensed"는 **과대주장**. 다만 검정력만으로도 ±0.20 배제는 성립하므로 verdict는 산다.
  과학적 독법: "capacity setpoint가 무효"가 아니라 **"router-mixture 조작 전체가 이 reach margin의 평균을 못
  움직인다"** — lane 종결로는 오히려 더 넓지만, "setpoint 특이적 무효"와 분리되지 않는다.

## C2 — item-pool 열화 ⇒ 등가는 **raw-nats 축에서만** 성립(scale-normalized로는 미배제)

fresh-cue 배제가 pool을 최하 tier(uni≥20·cnt≥4·pmi>0·cap=5)까지 밀어내 비영어 잡음 cue(waouh/aussi/merci)까지
포함됐다. live 신호가 run별로 **1.083 → 0.638 → 0.311**로 붕괴(D-acc .362).
- PREREG의 Δ_eq 근거("live 레벨의 ~31%")는 run-3 pool에선 **64%**다. 즉 배제 마진이 전체 신호의 2/3.
- 효과가 pool 강도에 비례한다고 보면 run-1의 −0.209에 **상당하는 상대효과** = run-3에선 0.057 nats인데,
  CI90 상한 0.160 ≫ 0.057 ⇒ **상대-스케일 효과는 배제 못 함**. 정직 문구는 "|effect| ≥ 0.20 nats(이 pool에서)만
  배제"이며 "재조합 배분 효과 부재"의 스케일-불변 주장은 **licensed 아님**.
- 같은 이유로 3-seed 고정효과 메타(Q p=.001)는 **이질성이 pool-quality moderator**일 수 있어 pooling 자체가
  취약하다. 다만 run-2(중간 강도 pool)가 run-1과 **부호 반전**이라 매끄러운 스케일링 설명도 안 맞으므로,
  "run-1의 KILL은 미재현·licensed 아님"이라는 결론(=KILL 철회)은 그대로 지지된다.

## C3 — 설계 흠결 2개(결론 불변 확인)

1. **c1_best 축 degenerate**: grid cands에 `c0`가 포함돼 pilot이 c0를 골랐다(0.3582 vs c1_k2 0.3529, 격차 0.005).
   ⇒ "부호반전 3축"은 실제로 **서로 다른 대조 2개**(c0, c2_shuf)뿐. 반사실 점검: c1_k2가 뽑혔어도
   CI90=[+0.007,+0.154] ⊂ ±0.20, t=1.80(PASS 아님) · c1_k1이면 [−0.040,+0.141] ⇒ **결론 불변**.
2. **V0b(SHAM) 거의 vacuous**: `apply_topk(k=E)`는 코드상 `continue`로 배열을 그대로 반환 ⇒ SHAM≡c0가
   **구성상 자명**. 0-바닥은 부동소수 결정성만 증명하고 파이프라인(마이닝·scramble·CRN)은 검사하지 않는다.
   (체크리스트 4의 "sham 붕괴" 유형 오류는 아님 — 이건 no-op sham이지 정보-삭제 sham이 아니다.)
3. 부수: pilot↔main **cue 단어 1개 중복**(tuple/pair는 0) · content word(a/b/f) 272/334가 이전 run과 재사용
   (cue만 fresh). 둘 다 방향은 "재현 쪽으로 편향"이라 KILL 미재현 결론을 부풀리지 않음. PREREG가 적은 probe
   pool 384 vs `probe.json`의 495(더 깊은 tier)라는 문서 불일치가 있으나 pool 크기는 결과변수 아님(채점 전 return).

## 판정

- **refuted = false** — 헤드라인·판정분기·마진·n·seed 전부 데이터 이전 동결, 재계산 완전 일치, 규칙 9종 중
  ①②③⑥⑦⑧⑨ 실질 충족. KILL(−0.209)은 3번째 disjoint seed에서도 미재현 = **KILL 철회는 licensed**.
- **⑤(V-gate)만 형식 PASS·실질 미달** — unsigned gate는 방향효과 0인 잡음도 통과(상기 surrogate 실증). 등가는
  V-gate가 아니라 **검정력**으로 licensed. 그리고 signed 양성대조 부재(SHOCK조차 평균 무이동)는 이 DV가
  routing 채널의 **방향효과에 원리적으로 둔감**할 가능성을 열어둔다.
- **EQUIVALENT-CLOSED 유지하되 scope 명시 필수**: "이 item pool의 raw nats 축에서 |effect| ≥ 0.20 배제" ·
  "0.15~0.20 및 상대-스케일(≈0.06) 효과는 미배제" · "V-gate가 아니라 power가 등가를 licensing" ·
  "닫힌 것은 setpoint 특이성이 아니라 router-mixture 조작 전반".
