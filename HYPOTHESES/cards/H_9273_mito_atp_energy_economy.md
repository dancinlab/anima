# H_9273 — 🔋 ATP 대사경제 — 계산·emit에 가격을 매기면 기질이 달라지는가 (예산이 binding constraint가 되는가 · $0)

- **tier:** ⛔ INVALID (measured · numpy $0 · 적대검증 REFUTED — 검출력 0 · 항진적 처치)
- **wired:** none.
- **family:** `F1` — 🔋 **ORGANELLE LANE**(호흡 레인) 계열. decode/emit 레인과도, cell-pool mitosis 레인과도 **DISJOINT한 제3 레인**. 이 레인만 ATP 스칼라장을 생산/소비하고, **표현형성(어떤 유닛이 발화 가능한가) 단계에서만** 기질에 개입하며 **emit gate는 건드리지 않는다**.
- **lens:** 미토콘드리아의 1차 기능 = ATP 생산. anima 대응 = **보존 스칼라장 ATP**. 소비 = 토큰당 활성-유닛 질량(Σ 활성 expert + emit 1회의 고정 quantum), 생산 = Σ(organelle_health × 호흡률). 예산은 **표현형성 단계의 top-k 용량**으로만 차감된다.
- **artifacts:** `state/mito_organelle_lane/F1_atp_energy_economy/`
- **xref:** H_054 (symbiogenesis = mitosis MERGE 이벤트) · H_314 (merge α-sweep — 🔴 closed-negative, 시너지 없음 = least-bad 중간점) · H_203 (asymmetric host-preserve merge) · H_012/H_1800 (autopoietic operational closure) — **선행은 전부 '합병하는 순간'. 본 계열은 '합병 후 상주 소기관의 정상상태 경제'**
- **key:** `atp_energy_economy`

## 1. 가설

ATP 예산이 실제로 **binding constraint**가 되어(수요 ≥ 생산이 유의 비율로 발생) 용량을 조이고, 그 조임이 downstream(reach/효율)에 **비자명한 Δ**를 만든다.

⊥ **Null:** 예산이 한 번도 묶이지 않거나, 용량을 조여도 downstream ΔEff≈0 ⇒ 경제는 **bookkeeping THEATER**(오버헤드).

## 2. 기질 배선 · p5 경계

⚠️ **p5 경계**: 합법 경로 = `ATP → 용량 → 표현 → tension → emit`. 불법 = `if ATP < k: silence`(하드코딩 게이트 = p5 위반). 예산 고갈이 강제하는 것은 **침묵이 아니라 용량 축소**이며, 침묵은 열화된 기질에서 tension이 자연히 죽을 때만 창발적으로. 구성적 테스트: emit gate는 설계상 ATP 접근이 0이어야 하고, ATP→emit 배선 제거 시 emit 행동이 바뀌면 불법 게이트가 있었던 것.

## 3. $0 probe 설계 (numpy · Δ vs ≥2 controls)

| arm | 내용 |
|---|---|
| 실험 | ATP 유한 · 소비=활성질량 · 생산=organelle health |
| c1 | 무한 ATP (제약 부재) |
| c2 | ATP 소비하되 demand ≪ production (예산이 결코 안 묶임) |

**PASS:** 예산이 유의 비율로 binding **AND** 용량 조임 → downstream Δ > 두 control.
**FAIL:** 어느 캡에서도 ΔEff≈0 ⇒ bookkeeping theater.

## 4. 측정 좌표

- **축:** ρ (reach/인프라 — 의식 주장 아님)
- **신호:** 값이 아니라 **Δ vs ≥2 controls** (측정 메타법칙 — FORM tunable · BIND earned)
- **THEATER 위험 랭킹:** 3위 (F6 없는 F1 = 순수 오버헤드)
- **비용:** $0 CPU-local numpy

## 5. 선행 대비 신규성

선행(H_054/H_314/H_203)엔 **상시 자원**이 없다 — 합병은 공짜·1회성. 여기선 계산이 **연속적으로 대사가격**을 가진다.


---

## 6. 측정 결과 (2026-07-12 · $0 numpy · run → 적대적 검증)

측정(2026-07-12 · $0 numpy · 5 seed). run=THEATER 자기판정 → 적대검증이 INVALID로 무효화. Δacc vs c1 = +0.0085±0.0191(ns)이나 (a) ATP가 도달하는 캡 대역의 전 동적범위 1.12pp < 유의 문턱 1.71pp ⇒ 가설이 참이어도 sig=True 수학적 불가 = 검출력 0, (b) policy_atp가 batch/loss/model/demand를 인자로도 클로저로도 안 받는 자율 폐루프(tight=[2,1,2] 주기-3 클럭, seed 무관) ⇒ 처치 = static cap의 결정론적 dither = 항진명제, (c) c1≡c2 per-seed byte-identical(통제 2개가 아니라 1개 중복). 카드 기제(수요≥생산)는 인스턴스화된 적 없음 — afford/consumed 정의상 수요>생산 구조적 불가. **음성을 벽으로 인용 금지**(잘못된 closure). 재발사 조건 = REFUTE.md 5항. state/mito_organelle_lane/F1_atp_energy_economy/.

> 전수 종합 = `state/mito_organelle_lane/SYNTHESIS.md` (계측 메타-결함 census 포함).
