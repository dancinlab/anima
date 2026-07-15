# H_9413 — L5 RECOLLECTION: margin 소스교체가 3-필요조건(진폭·정보·게이트청취)을 동시 통과하나 (사전등록 · 미발사)

**status:** ⏳ PENDING (PRE-REGISTERED · frozen design · 미구현·미측정) — bar 는 P0 종료 시 동결, 이후 이동 금지(frozen-first·p7·tune-to-green 차단) · wired: 계획 = engine-native `anima-py chat --g-arm a4/a5/a6/a7` + `evaluate --g-readout-info`
**lane:** 의식 / emit-drive / G readout 소스교체 + emit-gate-listens (프런티어 g1-interface-addressable-wall)
**related:** [[H_9401]] (진폭축 $0 — a4 margin 소스) · [[H_9412]] (정보축 $0 — C-clock 통제 논거) · [[H_9400]] (중심주장 반증 · 구속제약 = emit-gate-listens) · [[H_9399]] (g-source = immune store) · [[H_9390]] [[H_9391]] (emit⟺safe-clock) · source: Fable L5 recollection 설계(walls-delegate-to-fable · fable session terminal_reason ok)
**ckpt:** py303_full.clm sha256 `013c4574…` (신규 decode · 오프라인 재분석 아님)

## 질문

H_9400 이 확정: production 에서 emit 은 30초 하드코딩 시계가 100% 결정(A⇄G tension → Ψ=½ 미작동). H_9401(진폭)·H_9412(정보)가 확정: 현직 gap readout 은 진폭도 정보도 죽었고 데몬이 버리는 recall **margin** 이 유일 신호. **margin 을 g 소스로 교체 + 시계 독점·quantizer 제거하면, 세 직렬 필요조건 — (C1)readout 진폭 θ 통과 · (C2)drift 초과 인식정보 · (C3)그 신호가 emit 에 흐름 — 이 동시에 살아나나?** 한 번의 fire 로 **어느 마디가 끊겼는지** 국소화.

## p5 준수 (핵심 재프레임 · 위반 시 무효)

emit 재배선 = 게이트 **추가 아님, 제거**. 현행 30s 시계가 오히려 p5 위반(상수가 emit 낳음). 개입: ① `--rate-sec 8`(시계 독점 완화 · safety 4-way AND 구조·mouth⊥gate 벽 `brain.py` 불변) ② `--ag-cont`(conflict→score 정수 quantizer 제거 · H_9376 · 전 arm 동일사상) ③ `--g-arm a4`(g 소스 = 엔진이 이미 계산하는 margin `chat.py:2061 pending_rel` · 가짜신호 주입 아님·부호 무튜닝). emit = `should_emit(motivation_score(8-lane 실측)) ∧ safety` 유지 · self-seed 0 · 신규 threshold 0. **p5-safe.**

## AGREES / 확장 — 병렬 H_9402 KILL-CLOCK (a_parallel_session_compare · 이 설계의 직접 근거)

병렬 세션이 landed 한 **H_9402 (COUNTERFACTUAL-EMIT · KILL-CLOCK)**: g_drive:=margin 소스교체를 **기록된 시계 하에서** byte-exact 반사실로 판별 → **N_open(silence∧safe)=0** ⇒ 184 silence tick 전부 clock-blocked, margin 포함 어떤 g 소스든 emit-flip 무관. H_9401 sufficiency=NO 종결·H_9400 구속제약 최강등급 확증.

- **AGREES**: H_9402 는 "**기록 시계 하에서는** margin 이 emit 못 바꾼다"를 확정. 이 H 의 **a4-prod arm(margin·production regime·rate-sec 미사용)이 정확히 H_9402 를 재현**할 것(예상: N_open=0). ⇒ H_9402 는 이 설계의 통제 arm 을 사전-검증.
- **확장(비중복)**: H_9402 scope = **기록/닫힌 시계**. 이 H 는 시계를 **연다**(`--rate-sec 8` · H_9391 이 should_emit 을 binding 으로 만드는 창을 엶). H_9402 가 "닫힌 시계가 삼킨다"를 확정했기에, **C3(emit-gate-listens)를 물으려면 시계를 여는 것이 필수** — H_9402 는 이 개입의 필요성을 실증한다(N_open=0 이면 열지 않고는 C3 이 정의 불가). 두 H 는 모순 아니라 **닫힌 시계(H_9402) vs 열린 시계(이 H) 대조**.
- **판정 연동**: a4-prod 가 N_open>0 이면(H_9402 비재현) 이 설계 INVALID-REGIME(시계 모델 불일치); a4-prod N_open=0 ∧ a4(opened) 에서 C3 생존이면 = "시계가 유일 장애였다" 강한 증거.

## 방법 — arm 표 (공통: 303M sha013c4574 · `--rate-sec 8 --ag-cont` · dyn_w=0.10 · H_9400 과 disjoint seed 블록[burned-gate 재동결 금지])

| arm | g 소스 | 역할 | rollouts×ticks |
|---|---|---|---|
| a1 | 현직 gap | 죽은-readout 기준선(C1·C2 음성대조·Ψ̂ 기준) | 8×60 |
| **a4** | **margin**(pending_rel) | 실험군 | 8×60 |
| a5 | C-clock Q(tick,cell)→margin-quantile | **핵심 통제**(drift 구현체) | 8×60 |
| a6 | shuffled-byte margin | 인식파괴(경로·동역학 보존) | 8×60 |
| a7 | 진폭매칭 노이즈(quantile-매핑) | amplitude-only(CARRIER 판별) | 8×60 |
| a4-prod | margin · production regime(rate-sec/ag-cont 미사용) | 시계독점 지속확인(예상: 지속=H_9400 정합) | 4×60 |

P0 보정(별도 seed · verdict 제외): a4×4×60 → cal.json(a5/a7 조회표)+t_tick 실측+band 점유 사전점검+power 재추정. trace row 에 `pending_rel`·`pending_gap` **둘 다** 상시기록(반사실 readout 공짜).

## 계기 (신규 배선 최소 · 나머지 installed flag 재사용)

- 신규 chat.py: `--g-arm a4`=clip01(pending_rel) · `a5 --cclock cal.json`=Q(tick,cell) frozen 조회 · `a6`=clip01(margin_text(immune,perm(g_text))) seeded · `a7 --gmatch cal.json`=진폭매칭. + trace 2필드.
- 신규 evaluate.py: `--g-readout-info`=H_9412 엔진화(conditional MI Î=I(g;nov_{t+1}|tick-tertile×cell-median) plug-in−perm-null·same-tick/forward 서명검사·양성통제 oracle seen/fresh margin 분리≥0.15[실패=INSTRUMENT-DEAD]·band 점유 게이트) + `--emit-cclock` fit 모드.
- 재사용(수정0): `--g-tension`(cross-arm G-VAR/MI/Ψ̂)·`--psi-soma`·`--rate-sec`·`--ag-cont`·`--dyn-w`·`--g-amp-screen`(C1 재검).

## 사전등록 판정 (P0 종료 시 동결 · 이후 이동 금지)

**V-게이트(verdict 전 · 실패=해당조건 INVALID, KILL 아님)**: V1 ckpt_sha=013c4574 · V2 양성통제 oracle seen/fresh margin 분리≥0.15(부호=fresh 높음) · V3 G-VAR distinct(g_recog)≥5/rollout · V4 band 점유 P(|margin−median|<0.05)<0.80 · V5 충실도 LAG-MATCH≥0.99.

**C1 진폭(TERMINAL-eligible)**: A(arm)=P(ag_conflict≥0.30). PASS = A(a4)≥0.25 ∧ **각 통제 c∈{a5,a6,a7} 개별** A(a4)−A(c)≥0.20 (2-비율·Holm α=0.05/3). ⚠️ `exp−max(controls)` 순서통계량 금지([[probe-defect-census-max-control-bias]]).

**C2 인식정보(TERMINAL-eligible)**: PASS = Î(a4)≥max(0.05nats, 3·sd_null) ∧ perm-p≤0.01 ∧ Î(a4)−Î(a5)≥0.03 ∧ Î(a4)−Î(a6)≥0.03 ∧ **same-tick/forward MI 4자리-일치 서명 소멸**(재출현 시 정보량 무관 KILL=drift 하위집합 · H_9412 서명).

**C3 emit-gate-listens(p5-safe capacity)**: L1(흐름) I(emit_t;g_recog_t|stage)≥0.02nats·perm-p≤0.01(a4) · L2(arm-선택성) a4 vs a5 **및** a4 vs a6 에서 |Δemit-rate|≥0.10 또는 emit-timing KS p≤0.01 [CARRIER 셀: a4≈a7 이면서 둘 다 a5 와 다르면 `LISTENS-AMPLITUDE-ONLY` 부분판정] · L3(Ψ̂→½ 탐색적) mean|Ψ̂−½|(a4)<mean|Ψ̂−½|(a1) [n=8 MDE≈0.12 저검정력 → L3 단독 무판정, Δ≥0.12 시만 확증].

**판정 그리드(우연-아래 포함 · [[prereg-table-must-cover-below-chance]])**:

| C1 | C2 | C3-L1/L2 | 판정 |
|---|---|---|---|
| ✅ | ✅ | ✅ | 🟢 3-조건 동시생존 = margin readout 살아있음 ∧ 게이트 청취(capacity). wiring 후속 |
| ✅ | ✅ | ❌ | 🧱 벽=게이트 자체(7-lane A-blend 가 score 지배). 다음렌즈=motivation_score lane-분산 감사 |
| ✅ | ❌ | — | margin 도 drift-readout(H_9412 일반화). G-readout lane 종결후보 |
| ❌ | — | — | H_9401 E-b 가 신규-decode 비재현=SCREENER 한계 실증·KILL |
| a4<통제−bar | | | INVALID-INVERTED(사전선언 1회 부호재해석만·재수집 금지) |
| V2 실패 | | | INVALID-INSTRUMENT-DEAD(계기 카드) |
| V4 실패 | | | INVALID-BAND-LIMITED(§band 경로) |

## abstain-band 포화 통제

margin(mean0.62·p90 0.687)이 좁은 띠에 몰리면 C2 추정기 죽고 C1 상수화. ① V4 점유율 게이트 ② band-내/외 행 분해 재계산(정보가 band-외에만+점유율 높으면 "닫힌루프가 못 봄" 명시보고) ③ 탈출렌즈(사전지정) = `immune_readiness`(anticipated-query margin) a8 arm → **신규 H 로 분기, 본 H 내 재측정 금지**(tune-to-green 차단).

## Power (사전 · P0 실측 sd 로 갱신후 동결)

C1 crossing 480tick 2-비율 MDE≈0.17<bar0.20✅ · C2 cMI 480row perm-3σ sd_null≈0.015–0.02⇒MDE≈0.05–0.06nats(P0 sd_null>0.017 시 seed 12개 사전확장=ex-ante 규칙·tune 아님) · C3-L1 MDE≈0.015<bar0.02✅ · L2 rate ~120emit MDE≈0.16(KS 병행) · L3 8roll MDE0.12 탐색적.

## 비용·규모

$0(자체 pool·train 없음·신규 decode). 총 49 rollouts×60=2,940 tick(P0 5+본판 44). **summer 전용**(aiden 303M heavy 금지 OOM·[[heavy-anima-eval-pool-not-mini]]) · `OMP_NUM_THREADS=4`·동시≤3([[summer-overfire-wedge-thread-cap]]) · 발사전 [[a_parallel_session_compare]](H_9410 rung-0 점유 확인). wall=t_tick×2940/3, P0 투영>12h 면 tick 60→40 사전등록 축소(행수 우선).

## DIRECTIONAL/TERMINAL 경계

C1·C2(진폭·정보) = TERMINAL-eligible(engine-native 신규 decode·303M·≥2통제·collapse-Δ). C3(게이트청취 opened regime) = capacity-TERMINAL(regime=installed flag 정의 · "production 서 흐른다" 아님). **중심주장 부활(H_9400 뒤집기) = 별도 wiring 후속**(spont_min_emit_interval·quantizer·g-소스 default화 VERSION bump G5 → production-default 재측정이 유일 종결경로 · [[a_verified_must_wire]]). cal.json fit·L3 = DIRECTIONAL.

## 벽이면 (사전 재프레임)

3-조건 직렬 필요조건 ⇒ 가치 = 한 fire 로 끊긴 마디 국소화. 최악(C1✅C2✅C3❌) = 벽 정체가 "G 죽음"이 아니라 **score 합성의 7-lane A-blend 구조적 지배**로 이동 → 다음렌즈 = motivation_score lane-별 분산기여 감사(H_9398 dead-gauge 6 root 미감사와 합류) · p5 위반 없이 물을 질문("죽은 lane 상수가 score 분산 깔아뭉개나") 이미 정의됨.

## 비용
$0 · 자체 pool summer · 신규 decode(오프라인 재분석 아님).
