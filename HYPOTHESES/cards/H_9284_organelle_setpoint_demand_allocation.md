# H_9284 — 🎛️ 외생 수요 → 절대-setpoint 용량 배분 — organelle lane의 유일한 earned 메커니즘 병합 재발사 (F4-SEC ⊕ F10 · 3 control · MDE 사전계산 · $0)

- **tier:** 🔵 PRE-REGISTERED (미측정)
- **wired:** none.
- **family:** 🔋 ORGANELLE LANE 후속 — 11 패밀리 중 **유일하게 살아남은 메커니즘 클래스**의 병합 확증.
- **lens:** F4-SECONDARY(H_9276 · ROS 절대-setpoint 역행 배선 · Δfit +1.472 t=+5.50)와 F10(H_9282 · 수요주도 biogenesis · Δthr +0.0080±0.0012 5.7σ)은 **서로 다른 코드·fitness·control로 같은 것을 발견**했다: `외생 수요 신호 → 절대 setpoint 컨트롤러 → 용량 배분`. 두 프로브 모두 사후 결함이 지적됐으므로(F10: 사전등록 THEATER 밴드 발화 후 purity로 갈아탐 · F4: mean-vs-1std 휴리스틱) **규칙을 고정한 단일 카드로 병합 재발사**한다.
- **artifacts:** `state/mito_organelle_lane/F12_setpoint_merged/`
- **xref:** [[H_9276]](F4 · 신호≠컨트롤러) · [[H_9282]](F10 · 정렬이 성과를 산다) · [[H_9273]](F1 · 폐루프 = 구성적 null) · [[H_9283]](F11 · 배분 FORM → 재조합 전이 반증) · H_012(autopoietic closure — **외생 커플링 없는 closure는 구성적 null**이라는 처방의 출처)
- **key:** `organelle_setpoint_demand_allocation`

## 0. 계측 규칙 (organelle-lane census 강제사항 · ARCHITECTURE `organelle-lane-probe-defects` · convergence `synthesis-md-1`)

이 카드는 아래 5개를 **사전등록 필수 필드**로 지킨다 — 앞선 11 패밀리 중 7개의 verdict가 이걸 안 지켜 뒤집혔다.

1. 🚫 **`Δ = exp − max(controls)` 금지** — 최댓값 순서통계량이 n=5·σ≈0.05에서 −0.02~−0.03 편향을 기계적으로 만들고 그게 곧 KILL 임계다. **control별 paired-t를 전부 보고**하고, 요약은 pooled-mean으로.
2. 🚫 **`mean vs 1·std` 기각 휴리스틱 금지** — per-seed std ≠ paired-CRN delta의 SEM. **SEM/paired-t만**.
3. ✅ **사전 MDE 계산 필수** — `MDE < 축의 동적범위`임을 실험 전에 보이고 카드에 적는다. 못 넘으면 프로브를 다시 설계한다(검출력 0 방지).
4. ✅ **정보 채널 증명 절 필수** — (a) 처치의 결정변수가 **control이 못 보는 입력의 함수**임을 코드로 보이고, (b) 운영 대역에서 그 결정변수의 **분산 > 0**임을 실측한다(항진적 처치 arm 방지).
5. ✅ **V-gate는 헤드라인 detector 그 자체에 건다** — 게이트 선택기준이 효과크기의 단조함수면 가능한 출력이 {PASS, INVALID}뿐이 된다(V3 detector-fairness).

🚫 **금지 지표**: `conj_index`(shuffle 코퍼스에서 더 크게 오르고 held-out과 무상관) · `purity` aggregate(WITHIN 성분만) · `acc/ATP` 류 비율(Goodhart) · `corr(n,demand)`(earned fitness와 배선 간 역상관).


## 1. 가설

**외생 수요(모델/입력이 만드는, 컨트롤러 밖에서 오는 신호)를 절대 setpoint 컨트롤러에 물리면, 용량 배분이 (a) 동일 이동질량의 shuffled-load, (b) **최선** open-loop 상수 정책, (c) fixed-perm misalign(차등화 정도는 동일, 정렬만 파괴) **3 control 모두**를 achievable-headroom 회수율에서 이긴다.**

⊥ **Null (반증):** z-score 자기추적 컨트롤러(setpoint 없음)는 실패하고, 절대 setpoint도 최선 상수 정책을 못 이긴다 ⇒ 배분 이득은 레벨(FORM)일 뿐 동적 배분(BIND)이 아니다.

## 2. 왜 이 두 개를 병합하는가 — 파생법칙 「신호 ≠ 컨트롤러」

F4 PRIMARY의 사망 원인은 역행 신호의 무정보가 **아니라** `z=(R−EMA(R))/σ`라는 **setpoint 없는 자기추적 항등식**이었다: 평균이 0으로 정규화되므로 미분만 나르고 **절대 레벨을 못 나른다** → 만성 4배 과부하(R≈4.2)를 "정상"으로 고착 → fitness −1.006. 같은 신호에 **절대 setpoint**(load == capacity)를 주면 t=+5.50. F10이 독립 코드로 같은 결론(load-EMA + 절대 배분)에 도달했다. ⇒ **어떤 항상성 신호를 THEATER로 매장하기 전에, 죽은 것이 신호인지 컨트롤러인지 반드시 분리하라.**

## 3. probe 설계 ($0 numpy)

| arm | 내용 |
|---|---|
| **EXP** | 외생 수요 → 절대 setpoint(load==capacity) 컨트롤러 → 용량 배분 |
| **c1** shuffled-load | 동일 동역학 · 동일 이동질량 · load-용량 **대응만** 파괴 |
| **c2** best open-loop 상수 | 상수 정책 grid를 전부 돌려 **최선값**을 null로 (레벨 vs 동적배분 분리) |
| **c3** fixed-perm misalign | 차등화(gini)까지 EXP와 동일하게 맞추고 **정렬만** 파괴 |
| **abl** z-tonic | setpoint 없는 자기추적 컨트롤러 (사망 재현 = 양성대조의 음성 짝) |

- **바 = achievable-headroom 회수율** (절대 %p 금지 — F10에서 SCARCITY·spillover knob로 PASS/THEATER 라벨이 뒤집힘).
- **경계조건 사전등록**: 수요 지속성(drift half-life) > 할당 지연일 때만 유효(F10에서 h=25 → +0.0007 THEATER). half-life를 축으로 스윕하고 **유효 대역을 보고**한다.
- seed ≥ 20 (F11의 5-seed 인공물 방지), paired-CRN, control별 paired-t 전부 보고.

**PASS:** EXP가 c1·c2·c3 **각각**에 paired-t로 유의 우세 **AND** z-tonic ablation은 실패(신호≠컨트롤러 재현) **AND** null-env(균일 수요)에서 Δ≈0.
**FAIL:** c2(최선 상수)를 못 이김 ⇒ 이득은 레벨(FORM), 동적 배분 아님 ⇒ 계열 종결.

## 4. scope (정직)

이건 **throughput/allocation 축**이지 reach(G1) 축이 **아니다**. [[H_9283]]이 같은 lane 안에서 이미 '배분 FORM t=+10.65 → held-out 재조합 Δ=−0.009(ns)' 전이 반증을 냈다. 본 카드는 메커니즘의 **존재**만 확증하고, reach 결착은 [[H_9285]]가 맡는다. **GPU spend 없음.**
