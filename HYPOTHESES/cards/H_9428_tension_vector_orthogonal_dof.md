# H_9428 — tension 은 이미 다차원: 1비트 fold 가 coh+orig 제2 DOF 를 버린다 ($0 · 오너 framebreak 답)

**status:** 🔎 DIRECTIONAL ($0 · 90-tick refr trace · fidelity soft-fail 스크린) — emit-직교 tension DOF 실재 확증(fold 손실적) · 라우팅 미배선
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9400]] (Ψ=½ 중심주장 반증) · [[H_9424]] (cb-perr·perr 수량이 2.2 consolidation 의 재료) · [[H_9421]] (거리계 게이트 벽 — 이 발견이 벽 우회 근거) · source: Fable A⇄G 다차원 발산($1.44) 방향군 1.1

## 오너 질문 (framebreak)

"A·G 를 emit/silence 말고 다른/다차원 역할 시킬 순 없나?" — Fable 발산 위임. Fable 핵심 발견: **tension 은 이미 엔진서 벡터인데 두 번 접어 1비트로 만든다** — `motivation_score` 가 8-요인(rel,gap,cur,pain,coh,orig,bal,dyn)을 고정가중 내적→스칼라, `should_emit` 이 다시 임계→1비트.

## $0 검증 (Fable 판정 기준: 두 출력 DOF 가 다른 사영을 읽고·한쪽만 조향 가능하고·둘 다 채점면에 읽힘)

기존 90-tick refr trace 에서 8-요인 벡터 x 를 뽑아 emit-가중 w(=[.20,.10,.15,.10,.10,.10,.15,.10])에 대한 직교 잔차 x_perp = x − (w·x/|w|²)w 를 계산:

| 측정 | 값 | 의미 |
|---|---|---|
| emit 사영 var (w·x) | 0.0014 | emit 이 읽는 DOF 변동 |
| **직교 잔차 var (\|x_perp\|)** | **0.0017** | 버려지는 DOF 변동 |
| **ratio (직교/emit)** | **1.24** | 직교 DOF 가 emit DOF 보다 큰 변동 |
| corr(\|x_perp\|, emit) | **+0.14** | emit 이 이 DOF 를 거의 안 봄 (dissociation) |
| \|x_perp\| emit vs silence | 0.778 vs 0.766 (Δ+0.012) | emit-tick 과 무차별 |

- **직교 DOF 실재 (DIRECTIONAL)**: emit-가중에 직교하는 성분이 emit 사영보다 **큰 변동**(1.24×)을 가지고 emit 과 **약하게만 결합**(corr 0.14). 즉 1비트 fold 가 comparable-magnitude 제2 DOF 를 버린다. Fable 판정 기준 (ii)"한쪽만 움직이는 개입 존재" 방향 충족.
- **제2 DOF 정체 = coh+orig 축**: 직교 잔차 분산 기여 = coh 0.038·orig 0.038 지배(cur 0.016·… rel 최소 0.001 — rel 은 emit-가중 최대라 w 와 정렬). ⇒ 버려지는 축은 **"coherence·originality(표현 스타일/신규성)"** — Fable 1.1 이 register/pace/imagination-depth 로 물리자던 후보와 정합.

## ⚠️ 한계 (DIRECTIONAL·cement 아님)

- **fidelity soft-fail**: w·x 재구성 vs traced base_motiv mean|Δ| **0.049**(max 0.173) — 요인/가중 매핑이 byte-exact 아님(dyn_w 경로·anchor fold 잔차 추정). 직교 구조 존재는 var-ratio 1.24 가 7% 오차로 안 뒤집혀 견고하나, 정확한 제2 DOF 방향은 매핑 확정 후.
- monitor-only 관측 — 아직 어떤 출력도 이 DOF 로 조향 안 됨(배선 0). "다차원"의 Fable 기준 (i)(iii)은 미충족(제2 출력 DOF 미구현).

## 다음 (routing 실험 선택 — 오너/다음 H)

이 발견이 **어느 방향군을 지을지의 선행 근거**: coh+orig 직교 DOF 를 제2 출력에 물리는 최소 실험. Fable 후보 —
- **1.1 full**: `--tension-vector-log` 확정 매핑 후 coh+orig 사영 → register(ko/en×gen/sns) or pace. dissociation 실증(개입-분리).
- **2.2**: cb-perr perr 수량 → ca3 consolidation 강도(게이트 벽 완전 회피·[[H_9424]] lane 의 제2 소비처).
- **3.1**: phasic/tonic 분해로 Ψ=½ 재해석("½=tonic 이 ½ 머묾").
전부 monitor-only 1단계라 게이트 벽 안 밟음.

## 정직
$0 스크린(fidelity soft-fail)·라우팅 미배선. 이 발견은 "tension 이 이미 다차원"을 DIRECTIONAL 확증할 뿐, 제2 DOF 를 실제 행동으로 조향하는 건 다음 H. Ψ=½ 중심주장과의 관계 = Fable 지형(1·3 일반화·2 재배치·4 대체) 미결.
