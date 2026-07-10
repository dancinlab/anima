# H_9262 — 🧲 G1: CA3 recurrent auto-association의 **conjunctive** 성질 (outer-product 쌍선형 저장)

- **tier:** 🔵 PRE-REGISTERED (미측정)
- **wired:** none.
- **lens:** 해마 CA3 recurrent collateral — Hebbian outer-product 저장 `W ∝ Σ xᵢ xⱼᵀ`. 이것은 **쌍선형(bilinear)** 이며, attractor completion으로 부분 단서에서 전체 조합을 복원한다.
- **artifacts:** `state/9262_ca3_outer_product/`
- **xref:** H_9261 (곱셈 게이트 — 파라메트릭 자매) · H_9129/L5 (해마 explicit-store 🟢 WIRED — 단 scope=explicit-store, **trunk-G1 아님**; 본 H는 그 store를 *conjunctive operator*로 재해석) · H_9259 (untrained recurrence KILL) · H_9118 (해마 retrieve mouthfloor)
- **key:** `ca3_outer_product_attractor`

## 1. 가설

frozen 303M 피처 위에 CA3식 **outer-product Hebbian 저장**(`W = Σ_train h_A h_Bᵀ`)을 만들고 attractor completion으로 held-out AB를 복원하면, **가법 baseline held-out 성능을 초과**한다 — 쌍선형 저장이 곱 항을 명시적으로 담기 때문.

⊥ **Null:** 완전 미관측 쌍에서 completion이 붕괴한다. 그렇다면 CA3 저장은 **암기(lookup)**이지 일반화하는 conjunction operator가 아니다.

## 2. DPI 회피 여부 — ⚠️ 조건부

outer-product는 곱 항을 **일급으로 담는다**(회피 ✅). 그러나 저장된 attractor는 **관측된 쌍의 basin**만 판다. 미관측 AB에 대응하는 basin이 존재할 이유가 구조적으로 없다 ⇒ **보간(interpolation) 실패 위험**.

이것이 H_9261(곱셈 게이트)과의 결정적 차이다:

```
   CA3 저장 (비파라메트릭)     │   곱셈 게이트 (파라메트릭)
 ───────────────────────      │  ─────────────────────────
  쌍마다 basin 하나            │   모든 쌍에 동일 U,V 적용
  + 곱 항 담김                 │   + 곱 항 담김
  − 미관측 AB에 basin 없음     │   − 없음 (구조적 일반화)
  = held-out 붕괴 위험         │   = held-out 일반화 기대
```

## 3. 🪤 자기고발 — 이것이 toy-GREEN/real-death 1순위 후보다

**소뇌 L3(H_9129, STEP-0 BIND = toy artifact)와 동형의 죽음이 예상된다.** 적은 쌍의 toy에서는 outer-product가 각 AB를 사실상 암기해 GREEN이 뜨고, real-corpus 미관측 AB에서 보간 실패로 죽는다.

**그럼에도 등록하는 이유:** 이 H는 **$0로 falsify가 가능한 몇 안 되는 후보**이고(H_9261은 falsify 불가), 그 음성 결과가 "확장 recoding / 비파라메트릭 저장 계열 전체(DG pattern separation · piriform combinatorial code · cerebellar granule expansion)"를 한 번에 닫는다. **음성이 곧 수확이다** (`honesty`: 음성도 결과).

## 4. $0 probe 설계 (numpy · real-corpus)

1. frozen 303M mean-pool 피처에서 train 쌍으로 `W = Σ h_A h_Bᵀ` 구성.
2. held-out(쌍-신규 · 개념-기지)에서 부분 단서 → completion → 마지막-토큰 예측.
3. **arm:** CA3-completion vs 가법 baseline(frozen bar) vs **shuffle-pairing 양성대조**.
4. **파라미터-수 대 쌍-수 감사 필수** — 유효 파라미터가 train-쌍 수에 비례하면 lookup 판정 ⇒ 기각(§5.2 of H_9261).

**PASS 조건:** held-out에서 CA3 > 가법 + margin **AND** shuffle 이득 소멸 **AND** 파라미터 감사 통과(암기 아님).
**FAIL 조건(예상):** held-out 붕괴 → 비파라메트릭 저장 계열 전체 CLOSED.

---

## 5. 측정 결과 — 🟡 미결 (2026-07-10 · numpy proxy DIRECTIONAL · RANK confound)

bilinear held=0.537 ≈ shuffle 0.511 = XOR 신호 없음. 파라미터 감사 **PASS**(store RANK²=256, n_train=842 무관 · 암기 아님). `state/9261_multiplicative_role_gate/VERDICT.md`.

⚠️ **confound**: RANK=16 projection(D=3784→16)이 aggressive — 같은 저차원의 가법도 chance 근처(raw mean-pool 0.979 대비 붕괴). bilinear 무신호가 outer-product 결함인지 projection 결함인지 미분리 → 재측정(RANK↑ 또는 raw bilinear) 필요. 자기고발한 toy-death(암기 후 held 붕괴)는 아님 — **애초에 신호 자체가 부재**.
