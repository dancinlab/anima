# brainarch 스크리닝 종합 — objective/binding family ($0 cheap rung)

> 모든 probe 는 **numpy-only DIRECTIONAL** ($0, no torch/gauge_lib; grep 자가점검 clean).
> terminal 아님 — `a_engine_native_learning` 상 박제는 cli/anima.hexa → generator L3 → g_gates byte-parity 필요.
> 모든 bar 는 **frozen-first**(실행 전 docstring 사전등록), tune-to-green 없음(p7).

## 스크리닝 결과 표 (이번 배치 11건)

| id | key | lens (target) | verdict | grok_ctrl | survivor | 핵심 numbers |
|----|-----|---------------|---------|-----------|----------|--------------|
| H_1623 | hypernet_multiplicative_bind | hypernet 곱셈 bind (G1) | UNDER-POWER | ✗ FAIL | ✗ | HYPER held=0.044, max_single=0.067, ablate Δ(HYPER−ADD)=+0.044 INERT(<0.05); grok modular-add held=0.050 < chance 0.091; 4 bar 전부 FAIL |
| H_1616 | kosmos_vsa_compose | HRR circular-conv VSA bind (G1) | UNDER-POWER | ✗ FAIL | ✗ | HRR held=0.552 (bar 0.80 FAIL), ambig 1.000 (PASS); ablate ⊛→+ gap 0.421 **LOAD-BEARING**; grok held=0.500 < 0.80 bar (lift 0.357 over chance 0.143) |
| H_1708 | granule_conjunctive_recurrent_rollout | granule 합접 rollout (G1) | UNDER-POWER | ✗ FAIL | ✗ | M_conj held=0.022, max_single=0.000, ablate Δ=+0.022 INERT; grok modular-add held=0.117 ≈ chance 0.091 |
| H_1726 | entorhinal_grid_conjunctive_metric | 격자세포 conjunctive code (G1) | NOT-SUPPORTED | ✓ PASS | ✗ | composed_distinct=105 > max_single=7 but ablate=55 > 8 → (a) frozen bar FAIL; binding-pair (b) conj 1.000 / ablate 0.494 **LOAD-BEARING**; grok conj 1.000 vs add 0.000 |
| H_1732 | coupled_oscillator_phase_binding | Kuramoto 위상결속 (G1) | MIXED | ✓ PASS | ✗ | phase_ambig 0.764 (bar 0.90 FAIL), margin +0.264 (<+0.30); ablate K=0 drop +0.625 **LOAD-BEARING**; grok Fourier held 1.000 vs chance 0.143 |
| H_1718 | claustrum_conductor_binding_hub | claustrum Kuramoto 합의허브 (G1) | UNDER-POWER | ✗ FAIL | ✗ | hub_ambig 0.906 (bar 0.95 FAIL), bag 0.757 (>0.60 leak); ablate Δ+0.184 INERT; grok held=0.050 < chance 0.091 |
| H_1698 | pbwm_gated_slot_register | PBWM 게이트 슬롯 (G1) | UNDER-POWER | ✗ FAIL | ✗ | bind held 0.689, scramble(G0) 0.889 > bind → BAR-4 FAIL artifact; ablate Δ+0.578 (directional); grok held=0.050 < chance 0.091 |
| H_1717 | apical_basal_coincidence_ignition | 2-compartment BAC AND (G1) | UNDER-POWER | ✗ FAIL | ✗ | composed held=0.000=max_single=0.000, ablate=0.000 (DEGENERATE floor); grok modular-add 0.292 < 0.50 bar (chance 0.143) |
| H_1692 | active_inference_efe_policy | min-EFE 곱셈 prior (G1) | UNDER-POWER | ✗ FAIL | ✗ | bind held 0.889 vs add 0.178 Δ+0.711 **LOAD-BEARING**; scramble 0.778 BAR-4 FAIL; grok held=0.050 < chance 0.091 |
| H_1704 | hippocampal_index_pointer | 해마 indexing-theory 포인터 (honesty/persistence) | UNDER-POWER | ✗ FAIL | ✗ | binding-pair index 1.000 / ablate 0.445 **LOAD-BEARING(subset)**; completion 0.067 FAIL; AUROC 1.000 / shuffle 0.463; grok held=0.054 ≈ chance 0.091 |

### grok_ctrl 통과 = 측정해상도 있음(verdict 유의미)
- **H_1726**(NOT-SUPPORTED) · **H_1732**(MIXED) — 둘 다 grok PASS = under-power 아님. 하지만 frozen G1 bar 미통과로 survivor 아님.

## TOP-3 (H_1721/1792/1794, 이전 배치) 통합

| id | key | verdict | grok_ctrl | survivor | 핵심 numbers |
|----|-----|---------|-----------|----------|--------------|
| H_1721 | equilibrium_settling_energy | NOT-SUPPORTED | ✓ (weight-shuffle ctrl) | ✗ | ambig ebm_cross 0.906 (bar 0.95 MISS), ablate cross→0.500 INERT clean; novel F1=0.000 systematicity zero; Ψ=0.5000 double-well attractor 살아남음 |
| H_1792 | contrastive_predictive_future_latent | NOT (under-power caveat) | ✗ FAIL | ✗ | InfoNCE held 0.000, Δ(M3−M1 CE)=−0.022 no win; grok modular-add held 0.050 ≈ chance ⇒ 토이가 ANY objective grok 불가 |
| H_1794 | (anatomy 우회 AND) | MIXED | — | ✗ | AND 이 유일 엔진 아님 |

## 정직 종합

- **survivor = 0 / 14** (이번 11 + TOP-3 3). **303M 승격 후보 없음.**
- **UNDER-POWER = 9** (H_1623·1616·1708·1718·1698·1717·1692·1704 + H_1792) — grok positive control 이 chance 근처(modular-add held ≈ 0.05~0.12 vs chance 0.091~0.143)라 $0 numpy 토이가 *어떤* objective 로도 held-out compositional generalization 을 못 만든다. **측정한계(a_break_the_wall type-a), 과학 천장(type-d) 아님.** 메커니즘 무죄 — 거짓 NOT 박제 금지.
- **grok PASS 인데 frozen bar miss = 3** (H_1726 NOT-SUPPORTED · H_1732 MIXED · H_1721 NOT-SUPPORTED) — 해상도는 있으나 cheap toy 의 capability bar(0.90~0.95)를 noise/구조한계로 못 넘음(Kuramoto noise ~0.76 cap, CRT cardinality=geometry-not-learning, systematicity F1=0).
- **INERT/collapse 분포 (ablation 측정값, under-power 여부와 별개로 정보적):**
  - **LOAD-BEARING (binding operator 가 causal locus)** = 6 — H_1616(⊛ gap 0.421) · H_1726(conj-pair 1.000→0.494) · H_1732(K=0 drop +0.625) · H_1692(bind−add +0.711) · H_1704(index-pair 1.000→0.445) · H_1721(cross-weight clean) . **곱셈/위상/conjunction 결속자가 끄면 additive floor 로 붕괴** = 일관된 신호.
  - **INERT (<0.05 Δ 또는 degenerate floor)** = 5 — H_1623(+0.044) · H_1708(+0.022) · H_1718(+0.184 above bar) · H_1717(0.000 degenerate) · H_1792(−0.022) . 단 under-power 영역의 INERT 읽기는 신뢰 불가(토이가 애초에 grok 불가).
  - **artifact (scramble>bind, BAR-4 FAIL)** = 2 — H_1698 · H_1692 — interaction term 이 permuted wiring 도 fit → binding test 비청정.

## 한 줄 결론

**objective/binding family 에 cheap survivor 없음(0/14).** binding 결속자(곱셈⊙·HRR⊛·Kuramoto위상·conjunction)는 *load-bearing 으로는 일관*(6/14 ablation collapse to additive floor)이나, $0 numpy 토이의 grok-control 이 9건에서 chance 근처라 **cheap rung 전체가 recombination 축 측정한계(type-a)로 재확인** — frozen bar 통과한 3건(grok PASS)도 capability bar 를 noise/geometry 한계로 못 넘음. → **유일한 terminal 경로 = H_1602 recomb-objective pre-registered 의 cost-gated 303M engine-native 런(objrun)**: cli/anima.hexa → generator L3 → g_gates byte-parity 로 InfoNCE/contrastive-objective vs CE-marginal held-out G1 측정. cheap 토이로는 죽일 수도 살릴 수도 없으므로 GPU 즉시발사 부적격 후보 0, objective-as-G1-lever 판정은 303M 으로만.
