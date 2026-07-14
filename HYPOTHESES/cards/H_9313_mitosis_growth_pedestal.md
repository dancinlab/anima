# H_9313 — GROWTH-PAYS 에 참값-0 pedestal + 매개공변량-일치 통제 부착

- **lane**: MITOSIS-ENGINE
- **상태**: ⏳ RUNNING (사전등록 동결 · 8 seed · $0 CPU pool: aiden 0-2 · summer 3-5)
- **사전등록**: `state/mitosis_growth_pedestal/PREREG.md` (발사 전 동결 · bar 이동 금지)
- **도시에**: `state/fable_killshots/w3_mitosis.out.md` §3 카드1 · §4

## 물음

H_9311(#3439)이 예산을 풀어 SHRINK 10셀 2.72391 → 320셀 2.46370 = **−0.26021 nats/byte** 로
🟢 "GROWTH-PAYS"(성장은 생산적이다)를 세웠다. **그런데 통제가 0개다** — FLAT 통제는 퇴화분할 `break`
때문에 10셀에 고정돼 축이 미탑재였고, 참값-0 pedestal 도 없고, 시드도 1쌍뿐이다.
이 카드는 그 두 급소를 찌른다: **그 −0.26 은 정보인가, 아니면 혼합-평활(WB shrinkage) artifact 인가?**

## 팔 (5개 · 같은 창 · 같은 test set · 계기는 H_9311 verbatim)

| 팔 | 정의 | 무엇을 재는가 |
|---|---|---|
| **E** | repair + WB head · 진짜 (Xtr,Ytr) 로 성장 | 실험군 (H_9311 재현) |
| **C1** | **E 와 동일 centers** · head 만 flat leaf-MLE (WB 없음) | 매개공변량(파티션)을 맞춘 통제 — 명목 예산이 아니라 실제 매개변수 |
| **P0X** | X 행-셔플 사본으로 성장(분할선택 ⊥ Y) · head 는 진짜로 재적재 | **적응적 분할선택**의 참값 0 |
| **P0Y** | Ytr·Yte 셔플 ⇒ X ⊥ Y (train·test 양쪽) | **진짜 참값 0** — 어떤 파티션도 Y 정보를 살 수 없다 |
| **P1** | X 에 Y 결정축을 SPIKE-IN (dim=4) | 양성대조 (liveness) |

## 동결 bar

- **G-CALIB (BLOCKING)** — seed0 의 E 가 H_9311 재현 (|Δ| ≤ 0.001). 실패 → ⛔ INVALID.
- **G-LIVE (BLOCKING)** — mean[CE_P1(320) − CE_P1(10)] ≤ −0.50. 실패 → ⛔ INVALID.
- **G-PED-Y** — Δ_P0Y ≤ −0.10 ⇒ **혼합-평활 artifact 지배 ⇒ H_9311 🟢 철회**.
- **G-DISSOC** — Δ_C1 > +0.02 (열화) ∧ Δ_E < −0.05 ⇒ **이중해리 = 성장·추정기는 분리 불가한 쌍-레버**.
- **헤드라인 EARNED** = Δ_E − Δ_P0Y (paired) ≤ −0.05 ∧ paired-t p < .05 ⇒ **GROWTH-PAYS 생존**(처음으로 통제된 채).

검정력: σ_path 0.03 · S=8 ⇒ SEM 0.0106 · MDE 0.0346 · KILL 임계 |Δ_P0| ≥ 0.10 에 검정력 > 99%.

## 선행 관측 (2/8 seed · **판정 아님**)

| seed | Δ_E | Δ_C1 | Δ_P0Y | Δ_P1 |
|---|---|---|---|---|
| s6 | −0.092 | **+0.936** | +0.165 | −0.435 |
| s7 | −0.138 | **+0.309** | +0.102 | −0.963 |

방향: P0Y 가 **양수**(성장이 오히려 나빠짐) ⇒ artifact 아님 · C1 이 재앙적 열화 ⇒ **이중해리** 쪽.
⚠️ BLOCKING G-CALIB(seed0) 미실행 + 8 seed 중 2개 ⇒ **판독 금지**. 완주 후에만 bar 를 읽는다.

## 왜 이 카드가 존재하는가

convergence `synthesis-md-1` (4번째 동형 재발, 2026-07-14): 통제 없이 선 🟢 는 통제 없이 선 🧱 와
정확히 같은 죄다. H_9311 은 세 번째 계기 결함(셀풀 하드캡)을 고쳐서 얻은 🟢 인데, 그 🟢 자체는
아직 아무 통제도 통과하지 않았다. **자기 편에 유리한 결과일수록 먼저 찔러야 한다.**
