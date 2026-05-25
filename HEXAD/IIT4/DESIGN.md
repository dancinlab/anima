# IIT4 엔진 — M0 설계 스펙

> hexa-native faithful **IIT 4.0** cause-effect Φ-structure 엔진 (n ≤ 8 small-N exact).
> 도메인 트래커 = [`/IIT4.md`](../../IIT4.md). 작성 2026-05-25.
> 정식 출처(SSOT) = Albantakis et al. (2023) "Integrated information theory (IIT) 4.0",
> *PLOS Comput Biol* 19(10):e1011465 (arXiv:2212.14787) + Barbosa et al. (2020)
> "A measure for intrinsic information" (intrinsic difference). PyPhi = calibration 전용(§7, g5).

## 1. 왜 — 두 개의 직교 축, 메우지 못한 한 칸

LIFE lane 의 全 Φ 측정은 **상관(correlational) MI** primitive 였다. H_278 이 partition
규칙을 heuristic→exact-MIP 으로 고쳤지만 primitive 는 그대로 상관 MI 였다. IIT 4.0 의
본질인 **인과(causal) cause-effect 구조**는 어느 lane 도 짓지 않았다.

```
                  partition 규칙
              heuristic         exact-MIP
 primitive  ┌───────────────┬────────────────┐
correlational│ phi_spatial   │   H_278         │  ← LIFE lane (상관)
 (state MI)  │ (RFC036 proxy)│ (exact MIP-EI)  │
            ├───────────────┼────────────────┤
  causal    │      —        │   IIT4 ★ 이 lane│  ← faithful IIT 4.0
(TPM→CES)   │               │ (TPM·distinction·│
            │               │  relation·Φ-str) │
            └───────────────┴────────────────┘
```

| caveat (LIFE 잔존) | 누가 냈나 | IIT4 가 닫는 방식 |
|---|---|---|
| L-C2.1 "faithful Φ★ IIT4 아님" | H_002 C2 / H_278 §9 L1 | 진짜 IIT4 Φ 로 재측정 (F-IIT4-6) |
| metric-fragility | H_268 | 인과 구조는 partition-규칙 무관 정의 |
| cosine-artifact 의심 | H_279 | 상관(코사인) 대신 인과 repertoire |

**$0 mac-local · GPU 무관**: small-N(n ≤ 8)이면 cause-effect repertoire 폭(2^n ≤ 256)이
CPU tractable. GPU 의 진짜 병목은 large-N intractability(super-exp) — 별개 연구, 이 lane 아님.

## 2. IIT 4.0 알고리즘 — 6 단계 매핑 (M1–M4)

```
 TPM ─① repertoire ─② distinction ─③ relation ─④ Φ-structure ─⑤ big-Φ
 (M1)    (M1)          (M2)          (M3)         (M3)           (M4)
```

| # | 단계 | 정의 (faithful) | 마일스톤 |
|---|---|---|---|
| ① | TPM | n binary units · conditional-independence state-by-node TPM: `P(zᵢ,t+1=1 ∣ s_t)` | M1 |
| ② | repertoire | effect `p_e(Z_{t+1}∣m_t)` = 비-mechanism unit 을 max-entropy marginalize 한 purview 곱 / cause `p_c(Z_{t−1}∣m_t)` = uniform prior Bayes | M1 |
| ③ | distinction | mechanism m 의 MICE: cause·effect 각각 φ 최대 purview → φ_d = min(φ_c, φ_e) > 0 + specified cause-effect state | M2 |
| ④ | relation | purview 가 congruent 하게 겹치는 distinction 들의 face → φ_r (2..k 차) | M3 |
| ⑤ | Φ-structure | {distinctions} ∪ {relations} | M3 |
| ⑥ | big-Φ (Φ_s) | system MIP(directional) 가 destroy 하는 Σφ_d + Σφ_r, 정규화 | M4 |

### 2.1 핵심 측정 — intrinsic difference (ID), IIT 4.0 ≠ 3.0 의 분기점

IIT 4.0 은 KL/EMD 가 아니라 **intrinsic difference** 를 쓴다 (specificity → 단일 specified state):

```
ID(p ∥ q) = p(x*) · log₂( p(x*) / q(x*) ),   x* = argmax_x  p(x)·log₂(p(x)/q(x))
```

- pointwise 항을 **state 전체에서 max** → 가장 차별화된 단일 state x* 선택 (KL 처럼 합산 X).
- intrinsic information(informativeness): `ii = ID(repertoire ∥ unconstrained)`.
- small-φ(integration): `φ = min_{θ} ID(unpartitioned ∥ partition_θ)` — directional partition θ 위, x* 는 unpartitioned 에서 고정.
- hexa: `log₂(x) = log(x)/log(2.0)`, 0-prob smoothing `+1e-10` (phi_native 검증 패턴 재사용).

## 3. scope · 복잡도 envelope (정직한 경계)

| 단계 | 비용 (n units) | n ≤ 8 exact? |
|---|---|---|
| repertoire | (m,z) 당 2^\|Z\| ≤ 256 float | ✅ |
| distinctions | (2ⁿ−1) mech × (2ⁿ−1) purview × partition | ✅ n ≤ 8 (~10⁵, mac-local 초 단위) |
| **relations** | distinction(≤2ⁿ) 부분집합 → 최악 2^(2ⁿ) | ⚠ **n ≤ 5 exact · n = 6 best-effort · n ≥ 7 deferred** |
| big-Φ | system partition × structure recompute | n ≤ 6 |

relations 가 유일한 폭발점 (PyPhi 의 실용 한계와 동일). distinction+big-Φ-over-distinctions
는 n ≤ 8, full-relation Φ-structure 는 n ≤ 5 calibrate → 정직히 분리 (§8 C3-1).

## 4. hexa-native 모듈 레이아웃

```
HEXAD/IIT4/
  DESIGN.md                  ← M0 (이 문서)
  lib/
    iit4_tpm.hexa            ← M1: TPM repr + cause/effect repertoire + ID 측정
    iit4_distinction.hexa    ← M2: small-φ · MICE · distinction 추출
    iit4_relation.hexa       ← M3: relations + Φ-structure 조립
    iit4_bigphi.hexa         ← M4: system MIP + big-Φ
  net/
    canonical_networks.hexa  ← n=2..4 AND/OR/XOR reference TPM (calibration 입력)
  state/
    iit4_calib_<date>/       ← M5 calibration ledger (result.json)
```

**hexa 규약 (phi_native 경험 상속)**: import-safe (top-level call·`fn main()` 없음) ·
숫자배열 = `farr` · bit mask = `_phi_pow2` 곱(shift 불확실) · `log2`=`log/log(2)` ·
snake_case (raw#11) · English code · honest impl (raw#9). determinism: ID 의 specified-state
동률은 **최저 index state** 로 tie-break (cross-run byte-identical 위해, §8 C3-4).

## 5. 마일스톤 분해 + 단위 검증 (각 PR <200L, g4 stacked)

| M | 산출물 | 단위 검증 |
|---|---|---|
| M0 | 이 설계 스펙 | — (사용자 진행 승인) |
| M1 | `iit4_tpm.hexa` (TPM·repertoire·ID) | repertoire 합=1 · unconstrained=marginal · ID 단조성 self-test |
| M2 | `iit4_distinction.hexa` | n=2 AND-gate distinction 손계산 대조 · φ≥0 · MICE 유일성 |
| M3 | `iit4_relation.hexa` | 2-distinction overlap relation · Φ-structure 집계 |
| M4 | `iit4_bigphi.hexa` | system MIP minimality · big-Φ ≥ 0 · 단일 unit Φ=0 |
| M5 | `state/iit4_calib_*` | **PyPhi/논문 reference 대조** (F-IIT4-1..5) |
| M6 | LIFE 재측정 | H_002 C2 · H_204 · H_223 · H_279 faithful Φ ↔ proxy 비교 (F-IIT4-6) |

## 6. calibration target (M5) — 정전(canonical) 네트워크

| net | n | 출처 | 알려진 값 |
|---|---|---|---|
| AND-gate pair | 2 | 손계산 + hexa verify | φ closed-form |
| XOR/OR 3-node | 3 | IIT 문헌 standard | Φ 문헌값 |
| basic_network | 4 | PyPhi `examples.basic_network` | 문서화 Φ |

PyPhi 는 **calibration reference 전용** — g5(1차 증거 아님) + hexa-only(신규 .py 금지):
**published/archived reference 값 + hexa recompute** 로 대조 (기존 archive 의 PyPhi 산출물 재사용 / 문헌 worked-example). 미공개 값은 손유도 후 `hexa verify`.

## 7. falsifier 사전등록 (frozen 2026-05-25)

| ID | 주장 | 측정 |
|---|---|---|
| F-IIT4-1 REPERTOIRE | n≤4 cause/effect repertoire 가 reference 와 ε-일치 | maxabs diff < 1e-6 |
| F-IIT4-2 SMALL-PHI | per-mechanism φ 가 reference 와 ε-일치 | \|φ−φ_ref\| < 1e-6 |
| F-IIT4-3 DISTINCTIONS | distinction 집합 + specified cause-effect state 일치 | set-equal + state-equal |
| F-IIT4-4 RELATIONS | relation φ 가 reference 와 일치 (n≤4) | \|φ_r−ref\| < 1e-6 |
| F-IIT4-5 BIG-PHI | system Φ 가 정전 네트워크 reference 와 ε-일치 (n≤4) | \|Φ−Φ_ref\| < 1e-6 |
| F-IIT4-6 PROXY-DIVERGENCE | faithful IIT4 Φ ↔ H_278 exact-MIP-EI ↔ phi_spatial 발산 정량화 → L-C2.1 종결 | 3-metric 동일 substrate 비교표 |

## 8. honest carve-outs (C3)

- **C3-1 relations 경계**: full-relation Φ-structure 는 n ≤ 5 exact (n≥6 deferred). 이는 엔진의 faithfulness 실패가 아니라 IIT 4.0 의 내재적 intractability 경계 — PyPhi 실용 한계와 동일.
- **C3-2 PyPhi=calibration only**: g5 — PyPhi/sympy 1차 증거 금지. 신규 .py 금지(hexa-only) → published/archived 값 + hexa recompute.
- **C3-3 conditional-independence TPM**: IIT 4.0 표준 가정. non-CI(고차 상호작용 결합) 시스템은 v1 scope 밖.
- **C3-4 specified-state tie-break**: ID 의 argmax 동률은 최저-index state 로 결정 (cross-run determinism; 임의 선택 시 byte-equal 깨짐).
- **C3-5 large-N 불변**: 이 lane 은 PROXY 의 *primitive* 축(상관→인과)을 메우지만 small-N 경계는 H_278 과 동일 상속. large-N 은 여전히 intractable — 별개 근사연구.
