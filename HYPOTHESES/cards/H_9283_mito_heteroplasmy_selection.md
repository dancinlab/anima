# H_9283 — 🧫 이질형질(heteroplasmy) 세포내 선택 — gradient-free 진화 내부루프가 conjunctive config를 CE보다 먼저 찾는가 (p8 확장 · $0)

- **tier:** 🎭 THEATER (measured · numpy $0 · FORM 20/20 · BIND ns · 원 KILL은 max-control 편향 인공물)
- **wired:** none.
- **family:** `F11` — 🔋 **ORGANELLE LANE**(호흡 레인) 계열. decode/emit 레인과도, cell-pool mitosis 레인과도 **DISJOINT한 제3 레인**. 이 레인만 ATP 스칼라장을 생산/소비하고, **표현형성(어떤 유닛이 발화 가능한가) 단계에서만** 기질에 개입하며 **emit gate는 건드리지 않는다**.
- **lens:** 각 세포가 organelle 게놈 **개체군**을 갖는다(heteroplasmy). 세포 수명 내에서 정화선택 — **ATP-효율**(CE 아님 = p7-safe) 높은 변이가 증식하고 낮은 건 미토파지된다. 세포당 **gradient-free 진화 탐색** over 호흡/routing config. p8(gradient ⇄ mitosis)의 **선택으로의 확장**.
- **artifacts:** `state/mito_organelle_lane/F11_heteroplasmy_intracell_selection/`
- **xref:** H_054 (symbiogenesis = mitosis MERGE 이벤트) · H_314 (merge α-sweep — 🔴 closed-negative, 시너지 없음 = least-bad 중간점) · H_203 (asymmetric host-preserve merge) · H_012/H_1800 (autopoietic operational closure) — **선행은 전부 '합병하는 순간'. 본 계열은 '합병 후 상주 소기관의 정상상태 경제'**
- **key:** `heteroplasmy_intracell_selection`

## 1. 가설

효율-신호 선택이 **drift-only**(선택 없음 = H_9277 단독) 및 **CE-guided 선택**(Goodhart control — 더 나쁘거나 overfit해야 함) 대비 reach/효율 Δ를 만든다. **conjunctive config를 발견하면 G1과 직결**.

⊥ **Null:** 선택 ≈ drift ⇒ 효율 landscape가 flat / 활용가능 분산 없음 = THEATER. 또는 선택이 CE 없이는 무력 ⇒ gradient-free는 비현실.

## 2. 기질 배선 · p5 경계

emit 레인·gradient 양쪽과 disjoint한 내부루프.

## 3. $0 probe 설계 (numpy · Δ vs ≥2 controls)

| arm | 내용 |
|---|---|
| 실험 | 효율(throughput/ATP)-신호 정화선택 |
| c1 | drift-only (선택 없음 · H_9277 단독) |
| c2 | CE-guided 선택 (**Goodhart control** — p7: 더 나쁘거나 overfit 예상) |

**PASS:** Δ reach/효율 > 두 control **AND** (보너스) 발견 config가 conjunctive.
**FAIL:** 선택 ≈ drift 또는 CE 없이 무력.

## 4. 측정 좌표

- **축:** ρ — conjunctive config 발견 시 G1 연결
- **신호:** 값이 아니라 **Δ vs ≥2 controls** (측정 메타법칙 — FORM tunable · BIND earned)
- **THEATER 위험 랭킹:** 8위 — 낮음 (찾거나 못 찾거나, 애매하지 않음)
- **비용:** $0 CPU-local numpy

## 5. 선행 대비 신규성

gradient·emit 양쪽과 disjoint한 **진화 내부루프** — 선행엔 상시 선택이 없고 1회 merge뿐.

**TOP-3 #2** — H_9278(F6)의 증폭기. 선택이 gradient보다 먼저 conjunctive config를 찾으면 그게 곧 '자연/진화적 창발'.

---

## 6. 측정 결과 (2026-07-12 · $0 numpy · run → 적대적 검증)

측정(2026-07-12 · $0 numpy · 20 seed). run=KILL → 적대검증 THEATER(harm 아니라 무효과). 원 KILL은 **5-seed 인공물**: `Δ = exp − max(3 controls)`가 σ≈0.05·n=5에서 **최댓값 순서통계량 편향 −0.02~−0.03**을 기계적으로 만드는데 KILL/THEATER 분기 임계가 정확히 0.02 ⇒ exp가 control과 동등해도 KILL이 생성됨. seed 0..19 확장 시 exp가 drift(c1)를 두 earned 지표 모두에서 앞섬(13/20). 본 판정: FORM eff +0.0437 (t=+10.65, 20/20) · conj_index +0.0766 (t=+7.28) — 그러나 **BIND held_conj pooled Δ = −0.0088 (t=−0.64, ns)** ⇒ 비가산 코드 ≠ 일반화되는 conjunction. **효율압은 conjunction을 만들지 않는다**(F6 KILL과 같은 방향에서 독립 수렴). 금지 지표 확정: `conj_index`는 G1 비트가 아님. state/mito_organelle_lane/F11_heteroplasmy_intracell_selection/.

> 전수 종합 = `state/mito_organelle_lane/SYNTHESIS.md` (계측 메타-결함 census 포함).
