# IIT4 — deferred C: rule 110 n=7 bounded big-Φ

> `/cycle` deferred-closure C lane 의 bg fire 결과 (rule 110, n=7, bounded k=3 anchored sampling).
> M12 n=6 rule110 = 6.82 → **n=7 rule110 = 8.57362** 단조 증가, exact-impractical 영역(n≥7) 진입.

## 1. 결과

| rule | n | mode | cap k | big-Φ | total | nd | wall |
|---|---|---|---|---|---|---|---|
| 110 | 6 | exact (M12) | — | 6.82 | — | — | ~분 |
| **110** | **7** | **bounded** | **3** | **8.57362** | **21.6754** | **22.0** | bg ~min |

scaling: n=6 (6.82) → n=7 (8.57), exact-impractical(n≥7) 에서 bounded 가 단조 trend 유지.

## 2. method

- `eca_tpm_inline(110, 7)` — inline ECA TPM builder (state-by-node, n=7 ring).
- `big_phi_bounded(tpm, n=7, seed=42, cap=3)` — `stdlib/consciousness/iit4_bounded.hexa` k=3 anchored sampling (purview 후보 cap, mechanism 전수).
- bg fire `POOL_DISABLE=1 hexa run --no-sentinel run_c_n7.hexa > result.txt` Mac local.

## 3. honest scope (C3)

- **bounded ≠ exact**: cap=3 anchored sampling 은 exact MIP 대비 conservative under-approximation. n=6 exact 6.82 → n=7 bounded 8.57 은 단조 trend 적합하나 exact 비교 불가 (exact-impractical 영역).
- n=7 single-state/single-seed (state=42). multi-seed 일반화는 후속.
- M9/M12 의 `iit4_bounded` lib 검증 (16/16 + 7/7 🟢) carry — 본 결과는 새 lib 가 아닌 동일 엔진의 n=7 호출.
- C lane (rule 110 n=7) 결과 = deferred IIT4.log 항목 fold. n=8 은 별도 fire (cost·time envelope).

## 4. SSOT routing

- 엔진 = `stdlib/consciousness/iit4_bounded.hexa` (sidecar PR #1051, anima 6 lib thin shim).
- 어댑터 = inline `eca_tpm_inline` (anima 측 `iit4_eca.hexa` ECA 어댑터의 inline 변형 — bg fire self-contained 보장).
