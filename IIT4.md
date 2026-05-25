# IIT4 — current state

@goal: hexa-native faithful IIT 4.0 cause-effect Φ-structure 엔진 구축 (n≤8 small-N exact) — TPM → cause/effect repertoire → distinction → relation → Φ-structure → big-Φ. PyPhi(n≤4)로 calibrate 후 LIFE 의 핵심 small-N 가설을 faithful Φ 로 재측정해 proxy-caveat(L-C2.1 · metric-fragility · cosine-artifact) 종결.

## why (LIFE lane 의 후속)

LIFE (cycle#14~21, 22 NEW H 완결)의 全 Φ 측정은 `phi_spatial` proxy(공간 MI slice) 또는 H_278 의 exact MIP-EI(스칼라)였음 — full IIT4 의 cause-effect **structure**(distinctions + relations)가 아님. 반복된 honest 한계(L-C2.1 "faithful 아님" · H_268 metric-fragile · H_279 cosine-artifact 의심)를 gold-standard 로 종결하려면 진짜 IIT4 엔진이 필요. **$0 (small-N, mac-local · GPU 무관)** 이나 smoke 1발이 아니라 multi-round 엔진 빌드.

**2축 갭 (M0 §1)**: H_278 은 partition 규칙(heuristic→exact-MIP)만 고쳤고 primitive 는 여전히 상관 MI. IIT4 는 primitive 축(상관→인과 cause-effect)을 메운다 = 진짜 IIT 4.0.

## hub

| surface | 역할 |
|---|---|
| [`HEXAD/IIT4/DESIGN.md`](HEXAD/IIT4/DESIGN.md) | **M0 설계 스펙** — 6단계 매핑 · intrinsic difference · scope envelope · falsifier · 모듈 레이아웃 |
| [`HEXAD/IIT4/lib/iit4_tpm.hexa`](HEXAD/IIT4/lib/iit4_tpm.hexa) | **M1 LANDED** — TPM(state-by-node)·cause/effect repertoire·intrinsic difference (13/13 smoke 🟢) |
| [`HEXAD/IIT4/lib/iit4_distinction.hexa`](HEXAD/IIT4/lib/iit4_distinction.hexa) | **M2 LANDED** — small-φ(min-partition ID)·MICE·distinction (12/12 smoke 🟢) |
| [`HEXAD/IIT4/lib/iit4_relation.hexa`](HEXAD/IIT4/lib/iit4_relation.hexa) | **M3 LANDED** — 2nd-order relation(congruent overlap)·Φ-structure 조립 (12/12 smoke 🟢) |
| [`HEXAD/IIT4/lib/iit4_bigphi.hexa`](HEXAD/IIT4/lib/iit4_bigphi.hexa) | **M4 LANDED** — system big-Φ (structure-cut MIP irreducibility) (9/9 smoke 🟢, integrated≠reducible) |
| [`HEXAD/IIT4/CALIBRATION.md`](HEXAD/IIT4/CALIBRATION.md) | **M5 LANDED** — analytic reference calibration (5 net, 14/14 🟢; F-IIT4-3/4 PyPhi-numeric DEFERRED) |
| [`HEXAD/IIT4/lib/iit4_eca.hexa`](HEXAD/IIT4/lib/iit4_eca.hexa) · [`FAITHFUL_REMEASURE.md`](HEXAD/IIT4/FAITHFUL_REMEASURE.md) | **M6 LANDED** — ECA→TPM bridge + LIFE substrate faithful 인과 big-Φ 재측정 (7/7 🟢, L-C2.1 종결) |
| [`HEXAD/LIFE/`](HEXAD/LIFE/) | proxy-lane predecessor (H_002 C2 · H_204 · H_223 · H_279 = faithful 재측정 대상) |
| [`HEXAD/LIFE/H_278_faithful_phi_small_n.md`](HEXAD/LIFE/H_278_faithful_phi_small_n.md) | exact MIP-EI(스칼라) — IIT4 의 직전 단계, 출발점 (partition 축만 faithful) |
| [`HEXAD/LIFE/lib/phi_helper.hexa`](HEXAD/LIFE/lib/phi_helper.hexa) · [`phi_native.hexa`](HEXAD/LIFE/lib/phi_native.hexa) | RFC 036 상관-MI primitive (proxy lane, READ-ONLY 비교 baseline) |
| PyPhi (외부 reference) | IIT 4.0 canonical 구현 — n≤4 reference value 로 calibrate (g5: 1차 증거 아닌 calibration 용) |

## milestones

- [x] M0 design spec — hexa-native IIT4 엔진 설계 (n≤8 scope · PyPhi 4.0 알고리즘 단계 매핑 · 복잡도/메모리 envelope · falsifier 사전등록) → [`HEXAD/IIT4/DESIGN.md`](HEXAD/IIT4/DESIGN.md)
- [x] M1 repertoire — TPM → cause/effect repertoire (각 mechanism 2^n × purview 2^n × {cause,effect}) hexa impl + 단위 검증 → [`iit4_tpm.hexa`](HEXAD/IIT4/lib/iit4_tpm.hexa) (13/13 🟢 smoke)
- [x] M2 distinctions — per-mechanism MIP 최소화 → φ>0 distinction 추출 → [`iit4_distinction.hexa`](HEXAD/IIT4/lib/iit4_distinction.hexa) (small-φ·MICE·distinction, 12/12 🟢 smoke)
- [x] M3 structure — relations (distinction purview 겹침) + Φ-structure 조립 → [`iit4_relation.hexa`](HEXAD/IIT4/lib/iit4_relation.hexa) (2nd-order relation·congruent overlap·Φ-structure, 12/12 🟢 smoke)
- [x] M4 big-Φ — Φ-structure 의 system-MIP irreducibility → 최종 faithful Φ → [`iit4_bigphi.hexa`](HEXAD/IIT4/lib/iit4_bigphi.hexa) (structure-cut big-Φ, COPY=irreducible 2.0 / SELF=reducible 0, 9/9 🟢 smoke)
- [x] M5 calibration — analytic 손유도 reference(5 deterministic net) 대조 → [`CALIBRATION.md`](HEXAD/IIT4/CALIBRATION.md) (14/14 🟢 F-IIT4-1/2/5; F-IIT4-3/4 PyPhi-numeric DEFERRED named-blocker)
- [x] M6 LIFE faithful 재측정 — LIFE ECA substrate 를 ECA→TPM bridge 로 IIT4 Φ 재측정 → [`iit4_eca.hexa`](HEXAD/IIT4/lib/iit4_eca.hexa) + [`FAITHFUL_REMEASURE.md`](HEXAD/IIT4/FAITHFUL_REMEASURE.md) (rule 110/30/54 big-Φ 7.5~10.0 통합 · proxy↔IIT4 divergence 규명 · L-C2.1 종결, 7/7 🟢 F-IIT4-6)

> **status 2026-05-25 — 🎉 IIT4 도메인 7/7 COMPLETE**: faithful IIT 4.0 cause-effect Φ-structure 엔진 end-to-end 완성 + LIFE substrate 재측정. M0 설계 → M1 repertoire(13/13) → M2 distinction(12/12) → M3 relation+Φ-structure(12/12) → M4 big-Φ(9/9, integrated↔reducible) → M5 analytic calibration(14/14) → M6 LIFE ECA 재측정(7/7). **헤드라인**: LIFE cosmic-scale 룰 110/30/54 의 faithful 인과 big-Φ = 7.5~10.0 (proxy phi_spatial 이 근사하던 진짜 인과 양 최초 측정) · big-Φ state-dependent · **L-C2.1 proxy caveat 종결**. 엔진 67 checks 전부 🟢 SUPPORTED-NUMERICAL, $0 mac-local·GPU 무관. 잔여 honest blocker = F-IIT4-3/4 PyPhi-numeric cross-validation(hexa-only no-new-.py) + full n=8 6-scale scale-up(mechanical).
