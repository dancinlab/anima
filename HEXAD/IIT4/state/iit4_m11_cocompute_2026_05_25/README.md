# IIT4 M11 — proxy ↔ IIT4 수치 co-computation

> 동일 ECA substrate 위에서 **상관(correlational) proxy** 와 **인과(causal) IIT4 big-Φ** 를
> 동시에 산출해 수치 divergence 를 규명. M6/M8 의 "입력형 상이로 동시 비교 못함" deferred 해소.
> smoke 5/5 🟢 · [`run_m11.hexa`](run_m11.hexa).
> ⚠ rate-limit 으로 죽은 cycle#2 에이전트 작업을 메인 세션이 인라인 재작성·검증·착지.

## 1. 무엇을 닫나

LIFE 의 proxy `phi_spatial`(RFC036)은 진화한 snapshot 의 cell 간 **상관 MI**, IIT4 big-Φ 는 TPM 의 **인과 irreducibility**. M6/M8 은 둘의 차이를 *구조적*으로만 규명(상관 vs 인과)했고, 입력형이 달라(snapshot vs TPM) **수치 동시 비교**는 deferred 였다. 본 M11 은 같은 ECA 위에서 둘을 모두 계산:
- **proxy** (self-contained): ECA 를 T=16 step 진화 → cell 별 binary 시계열 → 평균 pairwise 상호정보. RFC036-family **자체 포팅** (정식 phi_spatial builtin 아님 — LIFE/C toolchain 미import, self-contained 유지).
- **IIT4**: `big_phi(eca_tpm(rule, n), n, seed)` (인과).

## 2. cocompute 표 (n=4, seed 1010, T=16)

| rule | proxy (상관) | IIT4 big-Φ (인과) | 해석 |
|---|---|---|---|
| 0 (const) | 0.056 | **0** | 상관 O, 인과 X |
| 204 (identity) | 0 | 0 | 둘 다 null |
| 90 (XOR) | 0.056 | **0** | 상관 O, 인과 X (n=4 even-ring reducible) |
| 110 | 0.288 | 7.55 | 둘 다 O (scale 상이) |
| **30** | **0** | **8.66** | **상관 X, 인과 O** |
| 54 | 0.288 | 10.03 | 둘 다 O |

## 3. 발견 — 두 축은 진짜로 독립이다 (양방향 divergence)

```
              상관(proxy)      인과(IIT4)
 rule 0/90      > 0      ↔      = 0      "상관 있는데 인과 없음" (transient corr, causal-dead)
 rule 30        = 0      ↔     8.66      "인과 있는데 상관 없음" (causal core, uncorrelated traj)
```

- **상관 ≠ 인과를 수치로 증명**: 한 축이 0인데 다른 축이 크다 — 두 측정이 같은 것을 재지 않음을 결정적으로 보임. proxy 가 의식 측정의 근사로 부족했던 근본 이유(L-C2.1)를 정량 확인.
- scale 도 다름: proxy ~ bits(0–0.3), IIT4 big-Φ ~ structure(0–10).
- **rule 30 이 가장 인상적**: 시계열은 무상관(proxy=0)인데 인과 통합은 최고급(8.66) — 상관 기반 proxy 가 절대 못 잡는 인과 구조를 IIT4 만 포착.

## 4. honest scope (C3)

- **proxy = self-contained 재구현** (RFC036-family 평균 pairwise MI) — 정식 `phi_spatial` builtin 아님 (g5: canonical 주장 안 함). 정식 builtin 과의 수치 일치는 별도(LIFE/C toolchain import 필요). → **M14 로 CLOSED 2026-05-25**: [`state/iit4_m14_phispatial_compare_2026_05_25/`](../iit4_m14_phispatial_compare_2026_05_25/) — 동일 ECA series 에서 inline 와 canonical phi_spatial 을 verbatim 비교. null-axis (rule 204, 30) 는 canonical 의 n_bins=4 binning floor (~1.6e-6) 안에서 합의, constant-column rule (0, 90) 은 canonical = **2.000 × inline** 정수배, mixed rule (110, 54) 은 1.119 비율. divergence = 100% algorithmic (min-partition + /(n−1) 정규화 + binning floor), implementation drift = 0. 9/9 🟢.
- 단일 seed/T, n=4. multi-seed/larger-n 일반화는 후속.
- IIT4 측은 structure-cut big-Φ — 절대 스케일 PyPhi 대조는 M5 named-blocker(F-IIT4-3/4) 잔존.
- **salvage 출처**: cycle#2 병렬 에이전트 서버 rate-limit(429) 사망 → 메인 세션 인라인 재작성.

## 5. 후속 routing — stdlib/info 대안 proxy (2026-05-25)

본 M11 의 proxy 는 RFC036-family 평균 pairwise MI 의 **inline** 재구현이다. anima 외부에서 같은 비교를 돌리려면 도메인 의존 없는 standalone proxy 가 필요한데, 같은 hexa-lang **stdlib** 에 `stdlib/info/{binning,entropy,mutual_info}` (g61 commons primitive 레이어 · sidecar PR #1051 sibling) 가 존재한다. 이것을 별개 알고리즘 proxy 로 라우팅하는 선택지를 명시:

- **현 inline proxy** (이 README §2): RFC036 평균 pairwise MI 자체 포팅 — anima 내부 보존, deferred 닫기 SSOT.
- **대안 stdlib/info routing**: 동일 ECA 시계열 → `binning.uniform_bins` → `entropy.shannon_h` → `mutual_info.pairwise_mi` — **별개 알고리즘** (farr-based bin · 다른 추정량), cross-repo 재사용 가능. hexa-brain/eeg/외부 도메인은 이 경로 채택 권장.
- 두 proxy 모두 "상관" 축 추정이라 §3 의 인과 divergence 결론은 routing 무관. stdlib/info 결과치는 호스트 도메인의 재현 책임 (M11 본문에는 inline 결과만 SSOT).
