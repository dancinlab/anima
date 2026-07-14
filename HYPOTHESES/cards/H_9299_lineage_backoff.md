# H_9299 — LINEAGE-BACKOFF: 분열 족보는 통계적 상속 구조인가

**Tier: 🧱 NEGATIVE (11-셀 영역) → H_9301 이 6 지점으로 확장해 🧱 TERMINAL 종결 · group MITOSIS-ENGINE · 2026-07-14**

- freeze → `state/h9298_mitosis_shrinkage/FREEZE_H9299.txt` · script → `h9299_lineage_backoff.py`
- result → `state/h9298_mitosis_shrinkage/results/h9299_summary.json`
- 선행 → H_9298 🟢 (딸을 부모에게 shrink 하면 분할비용이 사라진다)

## 물음 (H_9298 이 정당화한 p8-native 일반화)

MITOSIS 는 이미 부모-자식 구조를 갖고 있다 — **분열 족보**. 지금까지 모든 실험이 그 족보로 파티션만 만들고 **버렸다**(leaf 만 flat 하게 사용). 족보를 backoff 체인으로 쓰면 — 딸이 모 셀 분포를 상속하고 증거만큼만 이탈하면 — **분열 = 표현 생성 + 추정기 위계 생성이 하나의 사건**이 된다.

arm: A1(flat leaf-MLE) · **FLAT**(leaf→root 직행 WB) · **LIN**(족보 재귀 WB) · **SHUF**(족보 무작위 재배선, 깊이·shrinkage 총량 보존, 부모의 정체만 파괴). λ = Witten-Bell = n/(n+T), 자유 하이퍼 0.

## 결과 — 🧱 두 bar 모두 실패

| arm | CE | |
|---|---|---|
| A1 jamo floor | 2.51335 | CALIB PASS (byte-exact) |
| **FLAT** (조상 전부 건너뜀) | **2.49935** | |
| **LIN** (족보 사용) | **2.50675** | |
| SHUF (무작위 재배선) | 2.51283 | per-seed [2.50509, 2.51479, 2.51862] |

- **L1 LINEAGE-BEATS-FLAT ✗** — LIN − FLAT = **+0.00739**. bar 미달일 뿐 아니라 **방향이 반대**: 족보를 타는 것이 루트로 직행하는 것보다 **나쁘다**.
- **L2 EARNED ✗** — LIN − SHUF = −0.00609 (bar −0.02 미달), seed 부호 **2/3** (한 seed 는 +0.00166). 통제군 산포(sd≈0.007) 안의 잡음.

⚠️ 스크립트 verdict 로직에 구멍이 있어(두 bar 모두 실패인데 `L1 ⊻ L2` 분기로 떨어짐) 콘솔에 "DIRECTIONAL" 을 찍었다 — **손으로 정정**: 두 동결 bar 가 모두 실패했으므로 정직한 **음성**이다. bar 이동 0.

## 자기적발한 계측 결함 (공허 스윕)

사전등록 진단 P1("셀 수를 늘리면 LIN 이 단조 개선")을 **실행하지 못했다**: `grow_max=40` 과 `160` 이 **둘 다 11 셀**을 냈다. ⇒ 법칙이 "계보가 이득"이라고 예측하는 **굶주린 영역을 애초에 측정하지 못했다**. (H_1336 의 label-bijection 통제가 provably vacuous 였던 것과 같은 계열.) 이 결함의 추적이 H_9300(재차 공허) → **H_9301(진범 = 퇴화분할 break)** 로 이어졌다.

## 종결 (H_9301 이 확장)

H_9301 이 성장을 해방한 뒤 **6 지점(11~320 셀)** 전부에서 (LIN − FLAT) ≥ 0, 그것도 셀이 늘수록 **단조 악화**(+0.007 → +0.044). ⇒ **🧱 TERMINAL — 분열 족보는 상속 구조가 아니다.**
기전: leaf 가 굶주리지 않으면(11 셀 = 셀당 ~3,900 토큰) 조상으로 shrink 할수록 leaf 자신의 증거가 희석될 뿐. depth 33 의 재귀 blend = 순수 희석.

**살아남은 것**: shrinkage 자체는 강력하다(H_9298 🟢). 죽은 것: 그 shrinkage 의 대상이 **족보**여야 한다는 가설. 부모는 "분열상 부모"가 아니라 그냥 **풀링된 전역 통계**면 충분하다.

## HONEST
gradient-free · 분열 규칙 변경 0 · mirror ⇒ DIRECTIONAL · frozen-first · bar 무이동 · TOY/scale.
