# IIT4 — current state

@goal: hexa-native faithful IIT 4.0 cause-effect Φ-structure 엔진 구축 (n≤8 small-N exact) — TPM → cause/effect repertoire → distinction → relation → Φ-structure → big-Φ. PyPhi(n≤4)로 calibrate 후 LIFE 의 핵심 small-N 가설을 faithful Φ 로 재측정해 proxy-caveat(L-C2.1 · metric-fragility · cosine-artifact) 종결.

## why (LIFE lane 의 후속)

LIFE (cycle#14~21, 22 NEW H 완결)의 全 Φ 측정은 `phi_spatial` proxy(공간 MI slice) 또는 H_278 의 exact MIP-EI(스칼라)였음 — full IIT4 의 cause-effect **structure**(distinctions + relations)가 아님. 반복된 honest 한계(L-C2.1 "faithful 아님" · H_268 metric-fragile · H_279 cosine-artifact 의심)를 gold-standard 로 종결하려면 진짜 IIT4 엔진이 필요. **$0 (small-N, mac-local · GPU 무관)** 이나 smoke 1발이 아니라 multi-round 엔진 빌드.

**2축 갭 (M0 §1)**: H_278 은 partition 규칙(heuristic→exact-MIP)만 고쳤고 primitive 는 여전히 상관 MI. IIT4 는 primitive 축(상관→인과 cause-effect)을 메운다 = 진짜 IIT 4.0.

## hub

| surface | 역할 |
|---|---|
| [`HEXAD/IIT4/DESIGN.md`](HEXAD/IIT4/DESIGN.md) | **M0 설계 스펙** — 6단계 매핑 · intrinsic difference · scope envelope · falsifier · 모듈 레이아웃 |
| [`HEXAD/IIT4/lib/`](HEXAD/IIT4/lib/) | 엔진 구현 (M1 tpm · M2 distinction · M3 relation · M4 bigphi) |
| [`HEXAD/LIFE/`](HEXAD/LIFE/) | proxy-lane predecessor (H_002 C2 · H_204 · H_223 · H_279 = faithful 재측정 대상) |
| [`HEXAD/LIFE/H_278_faithful_phi_small_n.md`](HEXAD/LIFE/H_278_faithful_phi_small_n.md) | exact MIP-EI(스칼라) — IIT4 의 직전 단계, 출발점 (partition 축만 faithful) |
| [`HEXAD/LIFE/lib/phi_helper.hexa`](HEXAD/LIFE/lib/phi_helper.hexa) · [`phi_native.hexa`](HEXAD/LIFE/lib/phi_native.hexa) | RFC 036 상관-MI primitive (proxy lane, READ-ONLY 비교 baseline) |
| PyPhi (외부 reference) | IIT 4.0 canonical 구현 — n≤4 reference value 로 calibrate (g5: 1차 증거 아닌 calibration 용) |

## milestones

- [x] M0 design spec — hexa-native IIT4 엔진 설계 (n≤8 scope · PyPhi 4.0 알고리즘 단계 매핑 · 복잡도/메모리 envelope · falsifier 사전등록) → [`HEXAD/IIT4/DESIGN.md`](HEXAD/IIT4/DESIGN.md)
- [ ] M1 repertoire — TPM → cause/effect repertoire (각 mechanism 2^n × purview 2^n × {cause,effect}) hexa impl + 단위 검증
- [ ] M2 distinctions — per-mechanism MIP 최소화 → φ>0 distinction 추출
- [ ] M3 structure — relations (distinction purview 겹침) + Φ-structure 조립
- [ ] M4 big-Φ — Φ-structure 의 system-MIP irreducibility → 최종 faithful Φ
- [ ] M5 calibration — PyPhi reference(n≤4 known-value) 대조 calibrate (H_266 gold 판 — faithful 검증)
- [ ] M6 LIFE faithful 재측정 — H_002 C2 · H_204 closure inverse-U · H_223 pain · H_279 salience 를 IIT4 Φ 로 재측정 → proxy↔IIT4 비교, caveat 종결

> **status 2026-05-25**: M0 design spec LANDED — [`HEXAD/IIT4/DESIGN.md`](HEXAD/IIT4/DESIGN.md) (8 §, 6-falsifier frozen, 5 C3). 다음 = M1 repertoire impl (`iit4_tpm.hexa` — TPM·cause/effect repertoire·intrinsic difference + 단위 self-test). small-N(n≤8) exact 라 $0 mac-local·GPU 무관. large-N 은 여전히 intractable (별개 — 근사 알고리즘 연구).
