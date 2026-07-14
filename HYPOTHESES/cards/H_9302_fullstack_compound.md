# H_9302 — FULL-STACK: coda 조건화 × 해방된 성장 × shrinkage 는 복리가 되는가

**Tier: 🧱 KILL / NO-COMPOUND (정직 음성) · group MITOSIS-ENGINE · 2026-07-14**

- freeze → `state/h9298_mitosis_shrinkage/FREEZE_H9302.txt` · script → `h9302_fullstack.py`
- result → `state/h9298_mitosis_shrinkage/results/h9302_summary.json`
- 선행 → H_9298 🟢 (coda+WB @11 셀 = 2.45205) · H_9301 🟢 (성장 해방 · 셀 증가가 무해해짐)

## 물음
H_9298 은 **11 셀에 갇힌 채** coda 정보를 얻었다. H_9301 은 셀을 **320 까지 풀었으나** coda 가 없었다. 둘을 합치면 복리인가, 아니면 **같은 정보를 두 번 사는 것**인가?

기제 = `P(next | cell, prev_coda)` WB-shrinkage 를 **H_9301 의 REPAIRED (uncapped) 셀 풀** 위에서. 자유 하이퍼 0.

## 결과 — 🧱 복리 없음

| cells | 11 | 40 | 160 | **320 (헤드라인·사전고정)** |
|---|---|---|---|---|
| A1 (flat) | 2.51335 | 2.51350 | 2.53731 | 2.56884 |
| **FULL (coda+WB)** | **2.45205** | 2.44745 | 2.44828 | **2.46014** |
| coda position-shuffle | 2.52329 | 2.51832 | 2.52401 | 2.54462 |
| paired Δ | −0.07124 | −0.07086 | −0.07574 | −0.08448 |

- **F1 COMPOUND ✗** — 헤드라인(320 셀) FULL = **2.46014 ≥ 2.45205** (11-셀 coda head). bar 2.43205 미달. **성장이 coda 위에 아무것도 더하지 않는다** — 오히려 약간 나빠진다.
- **F2 EARNED ✓** — coda 신호 자체는 전 지점에서 굳건히 earned (paired Δ ≈ −0.08, 3/3 seed).
- 11 셀 지점 FULL 이 **2.45205 를 정확히 재현** = H_9298 에 대한 3차 CALIB (포트 무결).
- 최저점은 40 셀(2.44745)이나 11 셀 대비 **−0.0046** 로 bar 한참 미달 + 스윕 cherry-pick 금지 ⇒ 판정 불가.

## 결정적 함의

**coda 조건화와 셀 성장은 같은 정보를 산다.** prev_coda 로 조건화하고 shrink 하는 순간, 셀을 더 쪼개는 것은 더 이상 새 정보를 주지 않는다 (분산만 추가). ⇒ **세포분열(더 많은 셀) 자체는 레버가 아니었다.** 레버는 시종일관 **추정기 계급**(강도 공유)이었다.

법칙과 정합: 이득 = 신규정보 − 분할비용. 성장은 신규정보를 만들지 않고 분할비용만 만든다. shrinkage 가 그 비용을 0 으로 만들어 **무해**하게 했을 뿐(H_9301 G2), **이득으로 바꾸지는 못한다**(G3 ✗ · F1 ✗ 이중 확인).

## HONEST
gradient-free · mirror ⇒ DIRECTIONAL · frozen-first · bar 무이동 · TOY/scale · 한국어 유창성 주장 없음.
