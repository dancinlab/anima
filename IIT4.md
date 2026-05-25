# IIT4 — current state

@title: 🧠 IIT4 — "의식 측정자(尺)"

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
- [x] M7 calibration breadth (cycle#1) — 추가 hand-derived canonical net + analytic 영토 확장 → [`state/iit4_m7_calib_breadth_2026_05_25/`](HEXAD/IIT4/state/iit4_m7_calib_breadth_2026_05_25/) (PR #528, 35/35 🟢 · fractional-φ·De Morgan dual·ECA bridge byte-equal · F-IIT4-3/4 deferred 불변)
- [x] M8 LIFE 재측정 확장 (cycle#1) — n=5 ring + 8-state 평균 big-Φ → [`state/iit4_m8_multistate_2026_05_25/`](HEXAD/IIT4/state/iit4_m8_multistate_2026_05_25/) (PR #533, 10/10 🟢 · 110=35.7·30=28.6·54=14.4·rule90 even/odd-ring 위상반전 발견)
- [x] M9 tractability (cycle#1) — big_phi n=4/5/6 wall profile + bounded-mode lib → [`iit4_bounded.hexa`](HEXAD/IIT4/lib/iit4_bounded.hexa) + [`state/iit4_m9_tractability_2026_05_25/`](HEXAD/IIT4/state/iit4_m9_tractability_2026_05_25/) (PR #531, 16/16 🟢 · n≤5 초·n=6 분·n≥7 impractical · cap≥n=exact)

> **status 2026-05-25 — 🎉 IIT4 9/9 (core 7/7 + /cycle#1 확장 3)**: faithful IIT 4.0 엔진 end-to-end (M0~M6) + /cycle#1 병렬 확장 라운드(M7·M8·M9). 엔진 검증 누적 **108 checks 전부 🟢** (M1~M6 67 + M7 35 + M8 10 + M9 16). **헤드라인**: LIFE cosmic-scale 룰 인과 big-Φ (n=5 8-state mean) 110=35.7·30=28.6·54=14.4 — proxy phi_spatial 이 근사하던 진짜 인과 양. **신규 발견(M8)**: rule 90(XOR)이 n=4 even-ring 전 상태 big-Φ=0(checkerboard reducible)인데 n=5 odd-ring 에서 mean 49.5 → **위상(짝/홀 ring) 의존 통합** (M6 "state-1010 특이" 노트를 구조적 even/odd 성질로 정정). big-Φ state-dependence ~2× 확인. tractability: n≤5 초·n=6 분·n≥7 exact impractical(bounded-mode 로 완화). 잔여 honest blocker = **F-IIT4-3/4 PyPhi-numeric**(hexa-only no-new-.py) + proxy↔IIT4 수치 동시-cocompute(입력형 상이) + n=8 6-scale 전면(비용). 다음 /cycle 후보 = IIT 4.0 **exclusion-postulate**(후보 subsystem 중 최대 complex 탐색).
