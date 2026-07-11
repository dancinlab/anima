# H_9273 — 🔋 ATP 대사경제 — 계산·emit에 가격을 매기면 기질이 달라지는가 (예산이 binding constraint가 되는가 · $0)

- **tier:** ⛔ INVALID (재발사 2회 · 원 판정 무효화 · 결함이 짝짓기 축으로 이동 = 동형 재발)
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

---

## 7. 재발사 결과 (2026-07-12 · 2회차 · 원 결함 수리 후)

**재발사(2026-07-12 · $0 numpy · n=20 paired-CRN)**: 지목된 원 결함 5개를 **코드로 진짜 수리**(R1 pilot-MDE 사전게이트 seed-disjoint · R2 demand를 supply에서 외생화 → binding_rate 0.528(원 설계는 정의상 0) · R3 비가산 기질(topic×polarity, 선형 지름길 = 최빈 baseline과 동일) route_recall 0.998 vs chance 0.156 · R4 c1≠c2 실측 4.3pp(원 byte-identical) · R5 emit_decide에 atp 실주입 → illegal_channel_closed 20/20). **+R6 자진공시: 원 카드의 PASS 조건 자체가 구조적 달성불가**였다(c1=무한ATP·c2=never-binds 둘 다 EXP보다 자원이 많고 acc는 k에 단조증가 ⇒ '제약 arm이 무제약 arm을 이겨라'는 불가능). run=THEATER → **적대검증 REFUTED → STILL INVALID**: 헤드라인을 만드는 유일한 대비(EXP vs c5_nobank)의 **두 다리가 모두 무효** — (a) iid 다리 = **분포적 항등식**(인과 저수지 aff_t=g(dem_<t) ⇒ iid에서 aff_t ⊥ dem_t 강제 ⇒ Δ=0은 측정이 아니라 **정리**; 실측 corr(aff,dem) EXP −0.0049 vs c5 −0.0054 · Δ=−0.0007±0.0014 t=−0.53 9/20), (b) bursty 다리 = **지출 미매칭**(EXP 3.6416 vs c5 3.8674 = +6.2% ATP t=−34.9 · V4 예산공정성이 코드상 iid에서만 계산 · static-k 기울기 12pp/k × Δk 0.226 ≈ 2.7pp가 관측 −2.88pp의 거의 전부 ⇒ '저장이 해롭다'는 자원격차 아티팩트). **검출력이 처치가 도달 못 하는 축에서 계산됨**: 보고된 52배 여유는 처치가 정의상 고정하는 static-k 축의 값이고, 짝짓기 축의 동적범위 4.21pp는 도달에 corr=+0.787(투시)이 필요 ⇒ **인과 도달범위 0 = MDE/band=∞ = 검출력 0**(원 R1 실패모드의 이전). 등지출 통제(c2·c4)에선 EXP가 iid·bursty 둘 다 이김(+2.42/+1.91pp 20/20) — EXP를 이기는 arm은 전부 자원 우위. **결정적 공백**: 검증자가 추가한 **ATP-free 1줄 클램프 k=min(demand,2) = 0.7616 vs EXP 0.7403 (+2.13pp t=+8.23 20/20)** — 등지출·동일정보·무기제 통제가 설계에 없어 THEATER를 주장할 수는 있어도 **벌 수는 없다**. 📌 max(controls) 금지의 교과서적 실례: max면 c1이 삼켜 KILL, min이면 c2만 보고 PASS — 둘 다 거짓(control마다 다른 질문에 답하며 각각 유의). 재발사 조건 = 등지출·무-ATP 클램프 통제를 primary 편입 · 조건별 지출매칭을 V4 게이트에 · 검출력은 처치가 인과적으로 도달하는 축에서. state/mito_organelle_lane/F1_atp_energy_economy/refire/.

> 3건 종합 = `state/mito_organelle_lane/INVALID_REFIRE.md`. **메타 진단: 결함이 사라진 게 아니라 한 칸 옆으로 이동했다(동형 재발) — 헤드라인이 사전에 검증되지 않은 자유 상수의 한 점 위에 있었고 그 축에서 부호가 뒤집힌다.**
