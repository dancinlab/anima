# TOP-3 brainarch mid-rung SCALE-UP — under-power(측정한계) escape 시도

DIRECTIONAL only (numpy 토이, NOT engine-native; `a_engine_native_learning`).
**H_1792/1721 의 terminal 답은 303M objrun(H_1602) — 이 중간 rung 은 그 예측일 뿐.**
실행 = summer pool(공유 호스트, numpy CPU, GPU 불필요, $0). frozen bar 는 cheap 과 동일(tune-to-green 금지, p7/c9).

## 한 줄 결론

세 probe **모두 이 중간 rung 에서도 UNDER-POWERED** — grok/resolution 대조군이 PASS 하지 못해
"이 rung 도 측정한계, 다음 rung 필요"가 정직한 답. **벽 분류 type-a(측정 artifact) 재확인** — cheap 의
under-power caveat 가 중간 rung 에서 해소되지 않았다(천장 아님, 도구 해상도 부족).

| probe | rung 변경 | grok/resolution 대조군 | 재측정 | verdict |
|---|---|---|---|---|
| **H_1792** InfoNCE objective | P 7→13, **shared embedding(dim32) 추가**, H/D 128/48→256/96, steps 40k→60k, 5 seeds | modular-ADD grok held=**0.034 ≈ chance 0.043** → **FAIL** | 5-seed mean: M3(InfoNCE) held=**0.000**, M1 train=1.00/held=0.000(암기만), M2=0.000, M4=0.006; M3−M1=+0.000 | **UNDER-POWERED** (해상도 미확보) |
| **H_1794** product-AND | N3→4, k3→5 (joint 27→**625**), depth sweep M2..6 | max-pool 이 high-M 에서 **붕괴 안 함**(M≤6 전부 1.000) → **FAIL** | product 1.000 binds·additive/single 0.500 collapse 는 재현; **product>max-pool INERT 차이 = 여전히 측정불가** | **UNDER-POWERED** (product≠max 해상도 미확보) |
| **H_1721** equilibrium EBM | S=C 4→6 (conj 16→**36**), settle 1→8-step | EBM-cross ambig=**0.500 = chance** (cheap 0.906) → **FAIL** | (a) 0.500 chance · (c) Ψ=½ double-well PASS(analytic) · (b)(d) FAIL | **UNDER-POWERED** (binding 해상도 미확보) |

---

## 해상도 도달 여부 (핵심 규율: grok-control-gated)

team-lead 규율 = "스케일을 키워 positive/grok 대조군이 먼저 PASS 하는 rung 을 찾는다. 그 해상도 확보 후에만
H_1721/1792/1794 재측정 유효." → **이 중간 rung 에서 세 대조군 모두 PASS 하지 못함** → 재측정 수치는 모두
"해상도 미확보 하의 floor" 이므로 hypothesis 판정에 binding 하지 않음(정직).

---

## H_1792 — InfoNCE objective as G1 lever (303M objrun H_1602 의 미니어처)

- **rung 변경**: Z_7*→Z_13*(36→144 pairs), 인코더에 **shared per-symbol EMBEDDING table(dim=32)** 추가
  (cheap 의 onehot→MLP 에는 grokking-capable inductive bias 가 없었던 게 under-power 의 의심 원인) + H/D 키움 + 60k steps.
- **RESOLUTION GATE (grok-control)**: single-head modular-ADDITION(mod 23, 50% held, shared embedding, AdamW 60k)
  held = **0.034**(chance 1/23 = 0.043) → **FAIL**. shared embedding 을 추가해도 numpy full-batch tanh-MLP 가
  modular-addition 을 grok 하지 못함 → **이 rung 은 어떤 objective 로도 held-out 합성을 만들지 못한다 = 측정도구 해상도 부족**.
- **재측정(해상도 미확보 하)**: M3(InfoNCE) held = 0.00, M1(CE-marginal) train=1.00/held=0.00(암기만), M2/M4 = 0.00.
  → M3=0.00 은 "InfoNCE 실패"가 아니라 "이 rung 이 어떤 합성도 분별 못함"의 floor. BAR-2(M3−M1≥0.20) 측정 불가.
- **정직 결론**: 다음 rung 필요. numpy 토이에서 grokking 을 안정적으로 유도하려면 훨씬 큰 wd/steps/transformer 가
  필요한데, 그건 toy 의 한계를 벗어남 → **terminal 은 303M objrun(H_1602) 엔진-네이티브 학습**. 이 미니어처는
  "CE-marginal 은 train 암기만(held 0) 한다"는 *예측*만 DIRECTIONAL 로 제공(InfoNCE 가 그걸 깬다는 증거는 미확보).

## H_1794 — corticostriatal product-AND binding

- **rung 변경**: N=3,k=3(joint 27) → N=4,k=5(joint **625**), superposition-depth sweep M=2..6, feature space 대폭 확대.
- **RESOLUTION GATE (product-vs-max-pool)**: cheap 의 MIXED 원인 = max-pool 도 M=2 에서 binds(joint space 가 작아
  union-cross 가 saturate 안 함). 키우면 high-M 에서 max-pool 이 붕괴(≤0.60)하고 product 만 hold(≥0.90)할 것으로
  사전등록 → 실측 **max-pool 이 M=6 까지 전부 1.000**(붕괴 안 함) → **FAIL**. k^N=625 도 여전히 union 이 saturate 안 됨.
- **재측정(견고한 부분)**: product 1.000 binds + scramble 0.511 붕괴(G0 OK) + additive 0.500/single 0.500 **structural collapse(=G1 벽)** 는 scale-robust 하게 재현. **그러나 card 의 핵심 INERT 주장(product > max-pool)은 이 rung 에서도 측정 불가** — max-pool 이 안 죽음.
- **정직 결론**: additive/single 이 못하는 binding 을 conjunction 이 한다는 절반은 robust. product 가 **max-pool 보다도**
  우월하다는 INERT 차이는 아직 미해소 → 더 큰 k^N 또는 더 높은 superposition-depth(M≫6) rung 필요.

## H_1721 — Contrastive Equilibrium-Settling Energy Substrate

- **rung 변경**: S=C 4→6(conj 16→36), settle 1-step→8-step lateral-inhibition, epochs 400→1200.
- **RESOLUTION GATE (EBM-cross binding)**: cheap 은 ambig 0.906(0.95 에 근접). 키우니 **0.500 = chance**.
  ⚠️ **isolation 확인**: settle 변경이 아니라 *scale 자체* 가 원인 — settle 을 cheap 의 1-step(lat=0,leak=0)으로
  되돌리고 S=C=6 만 적용해도 ambig=**0.500**(증거 `state/brainarch_census/scaleup_out/h1721_cheapsettle_isolation.py`). 즉 **cheap 의 0.906 은
  16-conj 작은 공간에서의 readout 용량 천장 근방 artifact** 였고, 36-conj 에선 EqProp 선형 delta-rule 의 binding 용량이
  부족해 chance 로 붕괴(H_1569 small-corpus 🟢→scale 붕괴와 같은 패턴).
- **재측정**: (a) 0.500 FAIL · (b) novel_F1 0.425 FAIL · (c) **Ψ=½ double-well PASS**(analytic, scale-independent:
  bal 0.5000·contraction 0·remove-emit 0·remove-silence 1) · (d) honesty FAIL(AUROC_real 1.0 지만 shuffle-surrogate 도 1.0 = 대조 무효).
- **정직 결론**: EqProp 선형 EBM 은 binding 용량이 scale 하지 않음 = numpy EqProp 토이가 잘못된 측정 도구.
  더 높은 용량의 학습기(또는 엔진-네이티브 §ThirdLaw/contrastive lane)에서 재측정해야 함. Ψ=½ double-well 만 scale-robust.

---

## 다음 rung 권고 (정직, cost-gated)

- **H_1792** → **terminal = 303M objrun(H_1602) 엔진-네이티브**(cli/anima.hexa → generator L3 → g_gates).
  numpy 미니어처는 grokking 미달로 InfoNCE-vs-CE 분별 불가; 303M 실학습이 유일한 결정 경로(별도 cost-gate).
- **H_1794** → k^N≫625 또는 M≫6 의 더 깊은 superposition rung(여전히 $0 numpy 가능, 단 시간 비용 큼). 또는
  엔진-네이티브 thalamic-AND lane 으로 직접.
- **H_1721** → numpy EqProp 은 binding-용량 부족 확정 → 더 높은 용량 학습기 필요. Ψ=½ double-well 은 이미 robust.

> 비용: 본 작업 전부 summer pool numpy CPU = **$0**. GPU 렌트 없음. 다음 rung(303M objrun 등)은 별도 cost-gate.
