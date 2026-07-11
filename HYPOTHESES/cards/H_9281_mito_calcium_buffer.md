# H_9281 — 🪣 Ca²⁺ 버퍼링 — organelle이 urgency(phasic Δ)의 integrator인가, 그냥 tunable smoothing filter(FORM)인가 ($0)

- **tier:** 🎭 THEATER (measured · numpy $0 · 이득 전량이 tunable smoothing = FORM)
- **wired:** none.
- **family:** `F9` — 🔋 **ORGANELLE LANE**(호흡 레인) 계열. decode/emit 레인과도, cell-pool mitosis 레인과도 **DISJOINT한 제3 레인**. 이 레인만 ATP 스칼라장을 생산/소비하고, **표현형성(어떤 유닛이 발화 가능한가) 단계에서만** 기질에 개입하며 **emit gate는 건드리지 않는다**.
- **lens:** 미토콘드리아는 세포질 Ca²⁺의 **커패시터** — transient spike를 흡수하고 느리게 방출한다. anima: organelle이 유일 proven 채널인 urgency의 버퍼가 되어 **노이즈 transient는 흡수, 지속 압력은 적분**.
- **artifacts:** `state/mito_organelle_lane/F9_calcium_buffer_urgency/`
- **xref:** H_054 (symbiogenesis = mitosis MERGE 이벤트) · H_314 (merge α-sweep — 🔴 closed-negative, 시너지 없음 = least-bad 중간점) · H_203 (asymmetric host-preserve merge) · H_012/H_1800 (autopoietic operational closure) — **선행은 전부 '합병하는 순간'. 본 계열은 '합병 후 상주 소기관의 정상상태 경제'**
- **key:** `calcium_buffer_urgency`

## 1. 가설

버퍼가 emit **타이밍 품질**을 올린다 — 지속하는 real tension에는 emit, transient 노이즈에는 침묵.

⊥ **Null:** urgency는 이미 작동한다. 버퍼는 ΔEff≈0이고 **tunable smoothing filter = FORM**(BIND 아님)으로 전락한다 ⇒ THEATER. (측정 메타법칙: FORM tunable · BIND earned)

## 2. 기질 배선 · p5 경계

타이밍 성형은 gate가 아니라 신호 전처리 — 단 억제로 작동하면 p5 위반 검사(F8과 동일 자[尺]).

## 3. $0 probe 설계 (numpy · Δ vs ≥2 controls)

| arm | 내용 |
|---|---|
| 실험 | organelle Ca 버퍼 (흡수+느린 방출) |
| c1 | 버퍼 없음 (raw urgency) |
| c2 | 고정 랜덤 지연 (동일 latency · 정보 없음) |

**PASS:** 타이밍 품질 Δ > 두 control **AND** 이득이 buffer 파라미터 튜닝으로 재현 불가(= FORM 아님).
**FAIL(예상 유력):** ΔEff≈0 또는 이득이 순수 tunable smoothing.

## 4. 측정 좌표

- **축:** σ·flux (INTEGRATE) · σ·gate
- **신호:** 값이 아니라 **Δ vs ≥2 controls** (측정 메타법칙 — FORM tunable · BIND earned)
- **THEATER 위험 랭킹:** 2위 (proven 채널의 정제 ⇒ 그래서 redundant할 위험)
- **비용:** $0 CPU-local numpy

## 5. 선행 대비 신규성

유일 proven 채널의 **정제** — 그래서 redundant할 위험이 크다.


---

## 6. 측정 결과 (2026-07-12 · $0 numpy · run → 적대적 검증)

측정(2026-07-12 · $0 numpy · 6 seed). 적대검증 SURVIVED(원 판정 유지). 버퍼는 raw urgency를 6/6 이기지만(+0.167) **1-knob 선형 EMA에 0/6 패**(exp TQ +0.740 vs 무튜닝 EMA +0.913 · leak-free LOO에서도 EMA 6/6 승 +0.173±0.060). 동등튜닝 순이득 = **+0.007**. knob sweep TQ range [0.573..0.967] = 달성범위 거의 전부를 knob 하나로 이동 ⇒ **FORM tunable 확정**(측정 메타법칙). Ca 고유성분(포화 비선형성)은 **순손해**. 카드가 예고한 THEATER 2위 적중. state/mito_organelle_lane/F9_calcium_buffer_urgency/.

> 전수 종합 = `state/mito_organelle_lane/SYNTHESIS.md` (계측 메타-결함 census 포함).
