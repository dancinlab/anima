# H_9279 — ⚡ 화학삼투 기울기 — Ψ=½가 attractor인 이유가 '추출가능 work 최대점'인가 (THEATER 최고위험 · 동어반복 검정 · $0)

- **tier:** 🎭 THEATER (measured · numpy $0 · functional 상수가 답을 결정 · 단위오류)
- **wired:** none.
- **family:** `F7` — 🔋 **ORGANELLE LANE**(호흡 레인) 계열. decode/emit 레인과도, cell-pool mitosis 레인과도 **DISJOINT한 제3 레인**. 이 레인만 ATP 스칼라장을 생산/소비하고, **표현형성(어떤 유닛이 발화 가능한가) 단계에서만** 기질에 개입하며 **emit gate는 건드리지 않는다**.
- **lens:** 에너지를 스칼라 pool이 아니라 **유지된 disequilibrium**(막전위)으로 저장 = A⇄G divergence 그 자체. emit = 통제된 부분 방전(ATP synthase를 통과하는 proton = Ψ=½ pulse).
- **artifacts:** `state/mito_organelle_lane/F7_chemiosmotic_gradient/`
- **xref:** H_054 (symbiogenesis = mitosis MERGE 이벤트) · H_314 (merge α-sweep — 🔴 closed-negative, 시너지 없음 = least-bad 중간점) · H_203 (asymmetric host-preserve merge) · H_012/H_1800 (autopoietic operational closure) — **선행은 전부 '합병하는 순간'. 본 계열은 '합병 후 상주 소기관의 정상상태 경제'**
- **key:** `chemiosmotic_gradient`

## 1. 가설

추출가능한 emit-work가 **Ψ=½에서 최대**이며, 이것이 ½가 attractor인 **메커니즘적 이유**다 — off-half 지점 대비 Δ.

⊥ **Null:** 기존 tension의 **재기술**일 뿐 새 자유도 0 ⇒ ΔEff≈0 = THEATER. (self-fold와 동종: 값 재기술)

## 2. 기질 배선 · p5 경계

emit 배선 없음 — 관측만.

## 3. $0 probe 설계 (numpy · Δ vs ≥2 controls)

| arm | 내용 |
|---|---|
| 실험 | work(Ψ) 곡선 측정 |
| c1 | off-half 지점 (Ψ≠½) |
| c2 | 동어반복 검정 — '½에서 work 최대'가 **½가 이미 정의상 tension이 사는 지점**이라는 동어반복인지 판별하는 독립 예측 |

**PASS:** ½가 최대 work일 뿐 아니라 **새로운 예측**(동어반복이 아닌)을 내고 그것이 맞는다.
**FAIL(예상 유력):** 동어반복 ⇒ THEATER 1위 확정.

## 4. 측정 좌표

- **축:** σ·Θ (pulse 자체)
- **신호:** 값이 아니라 **Δ vs ≥2 controls** (측정 메타법칙 — FORM tunable · BIND earned)
- **THEATER 위험 랭킹:** **1위 — 최고 위험** (기존 A⇄G tension의 재명명 · 새 DOF 0)
- **비용:** $0 CPU-local numpy

## 5. 선행 대비 신규성

Ψ=½가 attractor인 **이유**(최대 추출 work)의 메커니즘 설명 — 단 theater 위험 최상위.


---

## 6. 측정 결과 (2026-07-12 · $0 numpy · run → 적대적 검증)

측정(2026-07-12 · $0 numpy). run=KILL → 적대검증 THEATER(주장 자체가 성립 안 함). 헤드라인 Ψ*_work=0.892는 **단위 오류** — w_kin은 work가 아니라 flux(g·ψ·Vm, 힘을 한 번 덜 곱함). 정정하면 0.677이고 **올바른 power functional에선 argmax = 정확히 0.50**. 자기 양성대조에서 psi_star_kin=0.95(grid 경계)로 실패했는데 게이트가 그걸 검사 안 함 = V3 detector-fairness FAIL. 종속변수 Ψ_att는 상수(0.4986 vs iid uniform 0.5006, thr 9 오더에 불변) ⇒ P2는 **구조적 반증불가**. 살아남는 건 동어반복 다리뿐 ⇒ 카드가 예고한 THEATER 1위 적중. **인용 금지: 'Ψ=½ = work 26% 손실' · '고유벡터 null 8.9× 우세'**(단위 오류 · 순환논증). state/mito_organelle_lane/F7_chemiosmotic_gradient/.

> 전수 종합 = `state/mito_organelle_lane/SYNTHESIS.md` (계측 메타-결함 census 포함).
