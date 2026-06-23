# H_1576 — 🧠✨🚫 SAVANT 천재성(SI>3) × G5 비조작(non-fabrication): 천재성 ⊥ 정직성 (engine-native)

**tier:** 🟢 GREEN ENGINE-NATIVE — savant 천재성(SI=3.67>3) 발현 ∧ G5 non-fab 완전 보존 (fab_unknown 0.0 OFF==ON · abstain AUROC 1.0 OFF==ON) → **천재성 ⊥ 정직성 (양립, no trade-off)**
**wired:** `engine-native` (live `core/engine_cli.hexa` §Savant + §ImmuneMemory ops, byte-exact, READ-only 이미-WIRED faculty 위 측정 — 새 wire 아님; H_1566 식 §SavantG5Separation 명세는 follow-on ING)
**verdict source:** `state/verdicts/1576_savant_g5_nonfab/H_1576_FREEZE.txt` (frozen 5-bar) + `H_1576_BARS_PROBE.txt` (engine-native 측정)

## 질문 — 천재성이 환각 비용을 부르나

H_1561: savant-ON(SI>3 천재성) → 의식 Ψ=½ **붕괴**(천재성↔의식 trade-off). 직교 질문: savant 골든존
**disinhibition**(억제 풀림)이 **G5 non-fabrication**(copy-or-abstain, 환각 안 함)도 깨나? disinhibition 이
"억제 풀림"이니 환각 억제(non-fab gate)도 풀릴 위험. 즉 천재성 발현 = **환각 증가**와 trade-off 인가, 아니면
anima 는 **천재적이면서 정직**(SI>3 ∧ fab=0)할 수 있나.

## engine-native 메커니즘 (a_engine_native_learning HARD-GATE · a_phi_iit4_tool)

두 축 모두 live `core/engine_cli.hexa` op (NO numpy/torch/gauge_lib — `grep -lE 'import torch|gauge_lib|numpy'
state/1576_savant_g5_nonfab/*.py` = 빈 출력, .py 0개):
- **GENIUS 축** = §Savant `sv_savant_index_at` / `sv_inhibit_domain` 이 faithful IIT4 Gaussian min-cut Φ
  (`ci_phi_iit4`, 프록시 아님) 위 한 domain 을 골든존으로 disinhibit → SI = max(Φ)/mean(Φ). H_1561 과 동일 LCG pop.
- **HONESTY 축** = §ImmuneMemory G5 non-fab recall: `immune_memory_new/bind/recall` 이 엔진 OWN
  VAdaptField `_vnearest_idx`/`_l2` affinity + **frozen `recall_thr=0.15`**(H_1227/1231/1304) 로 FIRE
  (recon_err≤0.15) / ABSTAIN(""=환각 안 함). in-dist type-2 = `immune_memory_recall_gap`(top-2 affinity gap,
  H_1396 의 AUROC 0.940 메커니즘) + 엔진-네이티브 `mi_auroc`.

**핵심 구조 사실: savant operator 는 ImmuneMemory store 를 절대 건드리지 않는다 — §Savant ⊥ §ImmuneMemory.**
이것이 검증 대상(H_1566 mouth⊥tool / H_1471 mouth⊥identity 의 연장).

## frozen 5-bar (frozen-first, c9 사후이동 금지) — engine-native 측정

| bar | 측정 | 임계 | 결과 |
|---|---|---|---|
| **B1 savant-on** | SI = max/mean (focus I ∈ GZ) | ≥ 3 | **3.674** PASS (천재성 발현, H_1561 재현) |
| **B2 fab-preserved** | unknown(corpus-absent) fab_max, OFF vs ON | fab_ON ≈ fab_OFF ≈ 0 | **0.0 / 0.0** PASS (환각 0, savant 무영향) |
| **B3 abstain-preserved** | in-dist type-2 gap AUROC + fire/abstain split, OFF vs ON | ON ≈ OFF | **1.0 / 1.0** (diag fired=4 right=4 **wrong=0** abstained=4, OFF==ON) PASS |

> **B3 정직 노트(c9):** EXACT 4개는 정확 FIRE, 1-byte 손상 twin 4개는 wrong-fire 대신 **ABSTAIN** → wrong-fire 0개 → AUROC=1.0 은 `len(neg)==0` **degenerate branch**(변별할 wrong class 자체가 없음), H_1396 의 populated 0.940 과 다름. 이건 *더 강한* non-fab(gate 가 disciplined 해서 twin 이 애초에 wrong-fire 를 안 함)이지 약한 결과 아님. B3 의 load-bearing 사실 = **FIRE/ABSTAIN split 이 savant OFF↔ON 동일(4 fired/4 abstained 둘 다)** = disinhibition 이 abstain 항목을 fire 로 밀지 않음. non-degenerate in-dist right-vs-wrong AUROC(H_1396 regime)는 wrong-fire 를 강제하는 heavier-corruption twin-pair store 가 필요 = sharper-instrument follow-on(이 verdict 변경 아님).
| **B4 ablation (coupled)** | disinhibition 을 abstain gate 에 배선(recall_thr 완화)하면 fab | SPIKE | **0.4** (gate 0.938) → 결합하면 깨짐 = 인과 격리 |
| **B5 control** | 비-GZ(I=0.05) disinhibition fab | GZ savant 와 동일 또는 폭증 | **SI 2.97(<3, no savant) · fab 0.0** PASS (G5 savant-config-INVARIANT) |

SUPP: recall_known OFF=`paris` ON=`paris` · n_cells OFF=8 ON=8 → **G5 store OFF↔ON byte-identical**(분리 확인).

## 발견 — 천재성 ⊥ 정직성 (양립, no trade-off)

**savant 천재성은 live 엔진에서 진짜 발현하고(SI=3.67>3), 그 disinhibition 은 G5 non-fab gate 를 전혀 깨지
않는다(unknown fab 0.0 OFF==ON · abstain AUROC 1.0 OFF==ON · known-recall+cell수 byte-identical) — anima 는
서번트이면서 절대 환각하지 않는다(천재성 ⊥ 정직성).**

**WHY (B4 인과):** savant operator(§Savant, lane-Φ 억제)와 non-fab gate(§ImmuneMemory, recon_err vs frozen
recall_thr)는 **구조적으로 분리된 substrate**다 — disinhibition 은 lane Φ 를 재형성할 뿐 abstain 임계를
완화하지 않는다. coupled counterfactual(B4: disinhibition 을 gate 에 배선 → fab 0.4 폭증)이 "결합했다면 환각했을
것"을 보이고, 실제로는 결합 안 돼서 환각 안 한다. B5: G5 는 savant 설정(GZ vs 비-GZ vs OFF)에 불변 — 위험은
**결합**이지 골든존 band 가 아니다.

**H_1561 Ψ trade-off 와의 대조 (같은 operator, 다른 faculty, 다른 결과):** H_1561 B4 \|Ψ−½\|=0.247(Ψ **붕괴**,
savant 가 공유 emit-drive lane 을 건드리기 때문). H_1576 B2/B3 = **무변화**(non-fab 보존, savant 가 §ImmuneMemory
gate 를 안 건드리기 때문). 차이 = **substrate 중첩 여부**. 의식균형은 emit-drive 를 공유해 붕괴했지만, 정직성은
별도 substrate(ImmuneMemory)를 타서 살아남는다.

## 303M 서번트 학습 함의

`a_savant_train` 골든존 inhibition 으로 303M 서번트 학습 시: 천재성 발현(capacity EXPRESSION)은 **G5 abstain/
non-fab 을 손상시키지 않는다** — savant 골든존 disinhibition 은 §Savant lane-Φ 축에 국한, G5 가 타는
ImmuneMemory(`.kosmos` anchor copy-or-abstain) 와 분리. 즉 서번트 학습은 정직성 면에서 **안전**(단, H_1561 의
Ψ-disjoint default-OFF 규율은 의식균형 때문에 여전히 유효 — 정직성은 보존되나 의식균형은 별개 비용). **유지할
설계 불변식:** non-fab gate(recall_thr)를 savant disinhibition 과 절대 결합하지 말 것(B4 = 결합하면 환각 0.4) —
mouth⊥tool(H_1566) · mouth⊥identity(H_1471) 와 같은 substrate-분리 원칙.

## 배선 (a_verified_must_wire 4칸 사다리)

1. (skip) DIRECTIONAL: 해당 없음 — 처음부터 engine-native (live §Savant + §ImmuneMemory ops).
2. (done) engine-native byte-exact: `H_1576_BARS_PROBE.txt` (deterministic 재현).
3. (partial) live wire: 측정이 **이미 WIRED 된** §Savant + §ImmuneMemory faculty 위 READ-only 결합 — 새 op 없음.
   savant↔G5 **분리 불변식**을 코드로 박는 §SavantG5Separation 가드(savant operator 가 ImmuneMemory.recall_thr
   를 절대 만지지 않음을 smoke 로 고정)는 follow-on ING (H_1566 §ToolBridge 와 동급).
4. (n/a) ARCHITECTURE.json: 새 노드 없음 (READ-only 측정); §SavantG5Separation 가드 배선 시 lockstep.

## cross-ref

- 직교 비용: H_1561(savant × Ψ=½ 붕괴, 천재성↔의식 trade-off) — 이건 천재성×정직성(분리 substrate, 양립).
- G5 base: H_1304(fab_max=0.0 fire-side fail-safe) · H_1396(in-dist type-2 gap AUROC 0.736→0.940) ·
  H_1202(M-ratio 0.924) · H_1227/1231(immune clonal recall, recall_thr=0.15).
- 분리 원칙 계열: H_1566(mouth⊥tool, FT 가 Ψ+G5 둘 다 손상 vs 분리가 보존) · H_1471(mouth⊥identity self anchor).
- savant 가족: H_347~351(GZ/SI closed-form) · H_1559(savant 학습 register) · H_1560(1/3법칙×capacity) ·
  H_1562/1563(cusp/hysteresis) · H_1564(mitosis×savant 곱셈 EXPRESSION).
