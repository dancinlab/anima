# H_9277 — 🧬 mtDNA 독자 계보 — gradient-free organelle 게놈(병목·uniparental 상속)이 host 고정복사를 이기는가 ($0)

- **tier:** 🎭 THEATER (measured · numpy $0 · 계보 FORM 만점 · BIND 0)
- **wired:** none.
- **family:** `F5` — 🔋 **ORGANELLE LANE**(호흡 레인) 계열. decode/emit 레인과도, cell-pool mitosis 레인과도 **DISJOINT한 제3 레인**. 이 레인만 ATP 스칼라장을 생산/소비하고, **표현형성(어떤 유닛이 발화 가능한가) 단계에서만** 기질에 개입하며 **emit gate는 건드리지 않는다**.
- **lens:** organelle은 host와 **다른 유전 계보**를 갖는다(mtDNA · 모계유전 · 병목). anima: 각 organelle이 **gradient-FREE 소형 파라미터 벡터**(호흡 config) 보유. 분열 시 상속(복사 + **병목**: k copy만 샘플 → drift), 융합 시 **uniparental**(한 계보만 유지 → 게놈 혼합 방지). CE gradient는 절대 안 건드림 = **G-flavored 제3 계보**(A=핵/forward CE).
- **artifacts:** `state/mito_organelle_lane/F5_mtdna_lineage_bottleneck/`
- **xref:** H_054 (symbiogenesis = mitosis MERGE 이벤트) · H_314 (merge α-sweep — 🔴 closed-negative, 시너지 없음 = least-bad 중간점) · H_203 (asymmetric host-preserve merge) · H_012/H_1800 (autopoietic operational closure) — **선행은 전부 '합병하는 순간'. 본 계열은 '합병 후 상주 소기관의 정상상태 경제'**
- **key:** `mtdna_lineage_bottleneck`

## 1. 가설

host와 독립적으로 drift하는 organelle 게놈이 **host 고정복사** 및 **gradient로 업데이트되는 게놈** 대비 reach/효율 Δ를 만든다.

⊥ **Null:** 선택압 없는 drift = 노이즈 ⇒ Δ≈0. (**F5 단독은 bite하지 못한다 — H_9283/F11 선택이 있어야 함** · 정직 플래그)

## 2. 기질 배선 · p5 경계

emit 레인 무접촉.

## 3. $0 probe 설계 (numpy · Δ vs ≥2 controls)

| arm | 내용 |
|---|---|
| 실험 | 독립 drift 게놈 (병목 + uniparental) |
| c1 | host 고정복사 (독립 없음) |
| c2 | gradient로 업데이트되는 organelle 게놈 (계보 독립 없음) |

**PASS:** Δ reach/효율 > 두 control.
**FAIL(예상 유력, 단독):** drift-only = 노이즈 ⇒ H_9283과 결합해야만 bite.

## 4. 측정 좌표

- **축:** σ·thread (PERSIST — mitosis를 가로지르는 별개 지속 계보)
- **신호:** 값이 아니라 **Δ vs ≥2 controls** (측정 메타법칙 — FORM tunable · BIND earned)
- **THEATER 위험 랭킹:** 5위 (선택압 없으면 순수 노이즈)
- **비용:** $0 CPU-local numpy

## 5. 선행 대비 신규성

세대를 가로질러 상주하는 **분리된 gradient-free 게놈** vs 선행의 1회성 weight merge.


---

## 6. 측정 결과 (2026-07-12 · $0 numpy · run → 적대적 검증)

측정(2026-07-12 · $0 numpy · 6 seed). 적대검증 SURVIVED(원 판정 유지). 계보 FORM은 만점(heritability 0.769 · host-independence 0.872)인데 held-out Δ=0: EXP−C3 = +0.0088±0.0334 (3/6 = 동전) · EXP−C2 = −0.263 (0/6). 신규 lineage-only control(C3-PERM · 값분포·자기상관 보존, 계보만 파괴)에서도 +0.0053. 계측기 무죄(floor 0.541 → ORACLE 0.805, range 0.28). ⇒ **선택압 없는 계보 = 분산매칭 노이즈 운반체**. 카드가 예고한 대로 F5 단독은 bite 불가 — H_9283(선택)과 결합해야 하나 그쪽도 THEATER. state/mito_organelle_lane/F5_mtdna_lineage_bottleneck/.

> 전수 종합 = `state/mito_organelle_lane/SYNTHESIS.md` (계측 메타-결함 census 포함).
