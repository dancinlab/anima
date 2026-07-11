# H_9282 — 🏗️ 생합성(PGC-1α) — 수요주도 organelle 증식이 균일/랜덤 할당을 이기고 특화를 만드는가 ($0)

- **tier:** 🟢 DIRECTIONAL-POSITIVE (measured · numpy $0 · 5.7σ · 정렬이 성과를 산다 · 미배선)
- **wired:** none.
- **family:** `F10` — 🔋 **ORGANELLE LANE**(호흡 레인) 계열. decode/emit 레인과도, cell-pool mitosis 레인과도 **DISJOINT한 제3 레인**. 이 레인만 ATP 스칼라장을 생산/소비하고, **표현형성(어떤 유닛이 발화 가능한가) 단계에서만** 기질에 개입하며 **emit gate는 건드리지 않는다**.
- **lens:** PGC-1α: 지속 고부하 조직에서 미토콘드리아가 **증식**한다. anima: 지속 고부하 expert 근처에서 organelle 증식 → 호흡용량 추가 할당 → 양의 피드백 → **특화**. cell mitosis와 DISJOINT(세포 내 organelle 수).
- **artifacts:** `state/mito_organelle_lane/F10_biogenesis_demand_allocation/`
- **xref:** H_054 (symbiogenesis = mitosis MERGE 이벤트) · H_314 (merge α-sweep — 🔴 closed-negative, 시너지 없음 = least-bad 중간점) · H_203 (asymmetric host-preserve merge) · H_012/H_1800 (autopoietic operational closure) — **선행은 전부 '합병하는 순간'. 본 계열은 '합병 후 상주 소기관의 정상상태 경제'**
- **key:** `biogenesis_demand_allocation`

## 1. 가설

수요주도 할당이 **균일 할당** 및 **랜덤 할당** 대비 throughput/특화도를 유의하게 올린다.

⊥ **Null:** 수요주도 ≈ 균일 ⇒ 부하 신호가 유용한 할당을 못 알린다 = THEATER.

## 2. 기질 배선 · p5 경계

구조 레인 전용 · emit 무접촉.

## 3. $0 probe 설계 (numpy · Δ vs ≥2 controls)

| arm | 내용 |
|---|---|
| 실험 | 수요주도(load-driven) organelle 증식 |
| c1 | 균일 할당 |
| c2 | 랜덤 할당 (동량) |

**PASS:** Δ throughput/특화 > 두 control.
**FAIL:** 수요주도 ≈ 균일 ⇒ theater.

## 4. 측정 좌표

- **축:** ρ·fan (capability) · σ·carve 접점
- **신호:** 값이 아니라 **Δ vs ≥2 controls** (측정 메타법칙 — FORM tunable · BIND earned)
- **THEATER 위험 랭킹:** 7위 (실제 능력 레버 · 측정가능 · 위험 하위)
- **비용:** $0 CPU-local numpy

## 5. 선행 대비 신규성

**특화를 만드는 적응적 자원할당**; 선행은 병합 후 정적 구조.


---

## 6. 측정 결과 (2026-07-12 · $0 numpy · run → 적대적 검증)

측정(2026-07-12 · $0 numpy · 5 seed). run=DIRECTIONAL-POSITIVE, 적대검증 부분 REFUTE 후 **유지**. **Δthr = +0.0080±0.0012 (5.7σ, 5/5)** · oracle 헤드룸 71% 회수 · null-env(균일 수요) Δ=+0.0001(측정 게임 아님). 결정적 validity: c3 shuffled-load(동일 동역학·동일 이동질량, load-용량 대응만 파괴) → 0.5584 ≈ 균일 c1 0.5585로 **완전 붕괴** ⇒ lift 전량이 **정렬(alignment)**에서 나옴. 추가 fixed-perm c3b(gini까지 EXP와 동일) → 0.5558로 균일보다 **못함** ⇒ 차등화(FORM) 자체가 아니라 정렬만이 성과를 산다. 경계조건: 수요 지속성(drift half-life) > 할당 지연(~75 step)일 때만 유효(h=25 → +0.0007 THEATER). ⚠️ 제한: 사전등록 THEATER 밴드가 실제 발화했고 보고서가 사후에 purity로 갈아탐(BETWEEN 54% = composition 아티팩트 · WITHIN-only 사용할 것) · PASS/THEATER 라벨이 SCARCITY·spillover knob로 뒤집힘 ⇒ **'헤드룸 극소' 결론은 근거 없음**, 절대 %p 바로는 cement 불가. **F4-SECONDARY와 동일 메커니즘의 독립 재현**(외생 수요 → 절대-setpoint 배분). state/mito_organelle_lane/F10_biogenesis_demand_allocation/.

> 전수 종합 = `state/mito_organelle_lane/SYNTHESIS.md` (계측 메타-결함 census 포함).
