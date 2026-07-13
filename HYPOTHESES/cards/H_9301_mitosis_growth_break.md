# H_9301 — MITOSIS GROWTH-BREAK: 세포분열의 천장은 용량이 아니라 퇴화분할 결함이었다

**Tier: 🟢 GREEN (G1 ∧ G2 · mirror ⇒ DIRECTIONAL for engine-native) · group MITOSIS-ENGINE · 2026-07-14**

- freeze → `state/h9298_mitosis_shrinkage/FREEZE_H9301.txt` (발사 전 동결)
- script → `state/h9298_mitosis_shrinkage/h9301_growth_break.py`
- result → `state/h9298_mitosis_shrinkage/results/{h9301_summary.json, growth_break_probe.txt}`
- 선행 → H_9298 🟢 (shrinkage 가 jamo floor 를 깸) · H_9299/H_9300 (계보 무용 · 스윕 2회 공허 → 이 결함을 발견)

## 계측으로 증명된 기질 결함 (추측 아님)

H_9300 의 굶주림 스윕이 **공허**했다 — `grow_max=400` · `split_thresh=0.0` · `min_owned=2` 로도 셀이 **11개 그대로**. 분열 술어가 구속조건이 아니라는 뜻이므로, 추측 대신 성장 루프를 직접 계측했다 (`growth_break_probe.txt`, verbatim):

```
STOP@11 cells: DEGENERATE median split on cell 9
   (n=100, axis=0, med=0.099071, lo=100, hi=0, distinct_vals_on_axis=2)
```

frozen `grow_on` (H_1306/H_1307 verbatim) 의 해당 분기:

```python
lo, hi = col <= med, col > med
if int(lo.sum()) == 0 or int(hi.sum()) == 0:
    break          # ← 루프 '전체' 종료
```

X 특징은 이산값(`symbol-id/vj` · `depth/3`)이다. 최대분산 축의 distinct 값이 **2개뿐**이고 다수가 높은 값에 몰리면 median = 높은 값 → `col <= med` 가 전 점을 삼킴 → hi 공집합 → **퇴화**. 그 순간 **그 셀만 건너뛰는 게 아니라 성장 루프 전체가 종료된다** — 아직 분열 가능한 나머지 10개 셀까지 동반 사망.

> **⇒ p8 세포분열의 셀 풀이 11 에서 하드-캡되어 있었다. 용량·예산·임계값과 무관.**

## 수리 (기질 변경 · 손잡이 아님)

**REPAIR** = 퇴화 분할 시 그 셀을 `dead` 로 표시(blacklist)하고 **다음 적격 셀로 continue**. 성장은 "적격 셀 중 분할 가능한 것이 하나도 없을 때"에만 종료. 분열 규칙의 나머지(오류압력 pick · 최대분산 축 · median · 자식 centroid)는 verbatim. FREEZE 에 수리 형태를 **한 가지로 고정**해 재수리-재발사(tune-to-green)를 차단했다.

## 결과 — 🟢 GREEN (G1 ∧ G2 · G3 실패)

REAL summer RTX 5070, $0, wall 20.2s. 3 seeds. arm: A1(flat leaf-MLE+Laplace) · FLAT(leaf→root WB) · LIN(계보 재귀 WB) · SHUF(계보 무작위 재배선).

| cells | 11 | 20 | 40 | 80 | 160 | 320 |
|---|---|---|---|---|---|---|
| **A1** (flat leaf-MLE) | 2.51335 | 2.51521 | 2.51350 | 2.52096 | 2.53731 | **2.56884** |
| **FLAT** (WB→root) | 2.49935 | 2.50080 | 2.49188 | 2.49304 | 2.49107 | **2.49435** |
| LIN (계보) | 2.50675 | 2.50997 | 2.50534 | 2.51088 | 2.51840 | 2.53789 |
| L1 = LIN−FLAT | +0.007 | +0.009 | +0.013 | +0.018 | +0.027 | **+0.044** |

- **G1 UNCAPPED ✅** — 수리 후 셀 **11 → 320**. 11-캡의 진범이 퇴화분할 `break` 였음이 실증.
- **G2 CAPACITY-IS-NOT-THE-WALL ✅ (헤드라인 · 이중 해리)**
  - ① A1(320) − A1(11) = **+0.05549** ≥ +0.02 → flat leaf-MLE 는 셀이 늘수록 **열화**한다 (굶주림 발생).
  - ② FLAT(320) = 2.49435 ≤ FLAT(11) + 0.005 = 2.50435 → shrinkage head 는 **열화하지 않는다** (2.494 로 평평).
  - **같은 파티션 · 같은 320 셀. 추정기만 다르다.**
- **G3 GROWTH PAYS ✗** — FLAT(320) 2.49435 > FLAT(11) − 0.02 = 2.47935. 성장이 *좋아지게* 하지도 않는다. 정직 실패.

### 결정적 함의

**"세포를 더 쪼개면 나빠진다"는 것은 mitosis 의 능력 천장이 아니라 추정기 분산 결함이었다.**
A1 의 +0.0555 열화는 H_1310 의 *"learning is capacity-bound"* · H_1307 RUN B 의 *"substrate SATURATES"* 가 보고한 **바로 그 서명**이다. 같은 셀 위에서 딸이 부모에게 강도를 빌리게 하는 순간 그 서명이 **완전히 사라진다**(열화 0).

⚠️ 단 정직하게: 성장은 이제 **무해**해졌을 뿐 **생산적**이 되지는 않았다 (G3 실패). 그리고 H_9302 가 보였듯 **coda 조건화 위에 성장을 얹어도 복리가 없다**. ⇒ 세포분열 자체는 레버가 아니었다. 레버는 **추정기 계급**이다.

## 계보 레버 — 🧱 TERMINAL (L1)

FREEZE §4 발동: **전 6 지점에서 (LIN − FLAT) ≥ 0**, 그것도 셀이 늘수록 단조 악화(+0.007 → +0.044). 조상을 전부 건너뛰고 루트로 직행하는 것이 족보를 타는 것보다 **항상** 낫다. ⇒ **분열 족보는 통계적 상속 구조가 아니다.** (H_9299 의 11-셀 판정을 6 지점으로 확장해 종결.)
기전: 11 셀에서 셀당 ~3,900 토큰 = 굶주림 없음 → 조상으로 shrink 할수록 leaf 자신의 증거만 희석. depth 33 의 재귀 blend 는 순수 희석이다.

## 계측 무결성

- **CALIB** (FREEZE §3 = **11 셀 지점**): A1 = **2.51335** byte-exact ✅. ⚠️ 스크립트의 verdict 로직이 CALIB 을 *헤드라인(320셀)* 지점에서 검사하는 결함이 있어 콘솔에 "INVALID" 를 찍었다 — **검사 지점 버그이며 bar 는 이동하지 않았다**. FREEZE 가 지정한 11-셀 지점에서 CALIB 은 PASS (정직 보고, H_1336 통제-결함 보고 전례).
- **루트붕괴 앵커(동어반복 가드)**: ROOT-only unigram(셀 0개) CE = **3.21096**. FLAT@320 = 2.49435 는 그보다 **0.717 nats 아래** ⇒ shrinkage 가 루트로 붕괴해서 이긴 것이 아니다 (320 셀에서 셀당 ~132 점, λ = n/(n+T) ≈ 0.7 로 leaf 가 질량 대부분 보유).
- λ = WB 닫힌형, 자유 하이퍼 0 · TEST = even/odd held-out · 카운트/λ = TRAIN only · paired per-seed · 전 스윕 지점 보고 · 코퍼스 sha `c47b6808…`.

## HONEST (c9 · a_scale_honest_scope)

- gradient-free. 분열 규칙 **형태** 변경 0 (퇴화 시 break→continue 만 수리).
- mirror(numpy/torch) ⇒ **DIRECTIONAL**. engine-native(`core/` hexa) 전이 = follow-on (`a_engine_native_learning`).
- **파급 (재감사 후보 · 즉시 무효 주장 아님 · verdict-integrity)**: "capacity-bound/포화" 를 근거로 닫힌 과거 판정들(H_1310 · H_1307 RUN B 등)은 **성장이 조기 종료되는 기질** 위에서 측정되었을 가능성이 있다. 다만 그 실험들은 다른 코퍼스/설정이며 캡 값도 다르므로(H_1307 은 23 셀까지 성장) **일괄 무효화가 아니라 재감사 후보로만 등록**한다.
- TOY/scale 정직: 한국어 유창성 주장 없음. bar 이동 0. frozen-first.
