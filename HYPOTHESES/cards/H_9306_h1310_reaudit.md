# H_9306 — H_1310 재감사: "capacity-bound" 판정이 추정기 결함 위에서 내려졌는가

**Tier: 🧱 UPHELD — H_1310 판정 생존 (추정기 무죄 · 천장이 진짜) · group MITOSIS-ENGINE · 2026-07-14**

- freeze → `state/h9306_h1310_reaudit/FREEZE.txt` (발사 전 동결 · **H_1310 의 원 bar 를 1바이트도 안 건드림**)
- script → `state/h9306_h1310_reaudit/h9306_reaudit.py` · result → `results/{h9306_summary.json, run.log}`
- 선행 → H_1310 🔴/🧱 (from-scratch pure mitosis · LOCAL-EXPERT CEILING) · H_9301 🟢 (flat-MLE 굶주림 열화)

## 재감사 licence (원 카드 확인 절차 · 추측 아님)

H_1310 의 arm 정의 **verbatim**: *"Each cell holds an online **add-1 next-byte table**."*
⇒ H_1310 의 B_scratch 는 **셀당 flat count-MLE head** — 정확히 H_9301 이 "셀이 늘수록 +0.0555 열화한다"고 실증한 그 추정기이며, H_1310 은 그것을 **512 셀**까지 키웠다. 헤드라인 DV(FLOOR·CONTROL)가 그 굶주림 분산 위에 **인과적으로 올라타 있다** ⇒ 재감사 성립.

⚠️ **소급 tune-to-green 차단**: 유리한 새 DV 를 만들지 않았다. **H_1310 이 발사 전 동결한 bar 를 그대로 재사용**하고, 바꾼 것은 **셀 head 추정기 하나뿐**(flat add-1 → Witten-Bell shrinkage, 자유 하이퍼 0).

## CALIB (BLOCKING · 포트가 원본을 재현해야만 WB arm 판독)

| 앵커 | H_1310 | in-run | Δ |
|---|---|---|---|
| A_freq (order-2 n-gram floor) | **2.50884** | 2.50884 | **+0.00000** |
| FLAT B_scratch[512] | **2.57788** | 2.57124 | −0.00664 (≤ 0.02) |

**⚠️ CALIB 이 잡은 포트 결함 1건 (bar 무이동)**: 첫 포트가 문맥을 `s[i-2]·27 + s[i-1]` 로 **패킹한 정수 id 의 중앙값**으로 이분했다 — 그건 **범주형이지 거리 공간이 아니다**. 성장이 64 셀에서 포화하고 FLAT[512] 가 2.92 로 앵커(2.578)를 크게 빗나가 **CALIB 이 WB arm 판독을 거부**했다. H_1310 의 *"2-means median bisection of its owned **territory**"* 는 metric space 를 함의하므로 문맥을 **2-D 점 (s[i-2], s[i-1])** 으로 두고 최대분산 축 median 으로 이분(레인 canonical `grow_on` 과 동일)하니 앵커가 재현됐다. (`reference-match` — 플래그를 흔든 게 아니라 첫 발산점을 정렬했다.)

부수: `/usr/share/dict/words` 는 **호스트별로 다른** 시스템 자산이다(summer 빌드 sha `48550825…` ≠ 앵커). 코퍼스를 **바이트로 고정해 전송**하고 sha 게이트로 provenance 를 보장했다.

## 결과 — 🧱 UPHELD (H_1310 의 원 bar 로만 판독)

| 사다리 (3-seed 평균) | 1 | 8 | 64 | **512** |
|---|---|---|---|---|
| **FLAT** B_scratch | 2.94658 | 2.90388 | 2.71853 | **2.57124** |
| **WB** B_scratch | 2.94657 | 2.90363 | 2.71877 | **2.53594** |
| WB B_shuffle (통제) | — | 2.88834 | 2.72572 | 2.53732 |

- **(3) FLOOR — FAIL** : WB 2.53594 ≮ 2.48884 (= A_freq − 0.02). **여전히 +0.047 위**.
- **(4) CONTROL — FAIL** : WB 하에서 shuffle − scratch = **+0.00138** ≪ +0.10.

### 결정적 읽기 (정직)

**shrinkage 는 실제로 도왔다** — FLAT 2.57124 → WB **2.53594**, **−0.035 nats**. 방향·크기 모두 H_9301 의 예측과 정합(굶주린 512 셀에서 강도 공유가 분산을 회수). **그러나 벽을 넘지 못했다**: n-gram floor 까지 아직 +0.047 부족.

⇒ **H_1310 의 천장은 진짜다. 추정기는 무죄다.**
⇒ **"학습이 error-targeted 가 아니라 capacity-bound" 라는 H_1310 의 진단도 생존**한다 (WB 하에서도 셔플 ≈ 표적화, Δ=+0.0014).
⇒ **`a_mitosis_train` 의 "🔴 from-scratch pure-split can't learn alone (need gradient)" 은 그대로 선다.**

### 추정기-계급 법칙의 경계가 한 칸 더 좁혀졌다

| | 자모 floor (H_9298) | G1 재조합 (H_9304) | **from-scratch mitosis (여기)** |
|---|---|---|---|
| 담을 정보가 있나 | ✅ 실재 (+0.076 EARNED) | ❌ 부재 (+0.002 ≈ 0) | ✅ 실재 (shrinkage 가 −0.035 회수) |
| 추정기 교체로 뚫리나 | ✅ **뚫림** | — (담을 것 없음) | ❌ **부족** (−0.035 로는 +0.069 못 메움) |

법칙은 **"분산이 죽인 저차 신호를 되산다"** 까지만 참이다. 되산 양이 벽 높이보다 작으면 벽은 그대로 선다 — **정보 존재 ≠ 벽 돌파**. 이 카드가 그 경계의 세 번째 데이터점이다.

## HONEST
gradient-free · mirror(numpy) ⇒ DIRECTIONAL · toy 24KB English scope (a_scale_honest_scope).
원 bar 이동 0 · 새 DV 도입 0 · 유리한 지표 교체 0. FLAT arm 을 **같은 코드로 동시 실행**해 포트 차이가 아니라 추정기 차이임을 보장했다. $0 summer · wall 210s.
