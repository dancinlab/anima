# AKIDA — log

`AKIDA.md` 의 append-only 자매 로그. 각 엔트리는 `## <ISO timestamp> — <header>` (최신 위) · 본문 = `- [x]`(완료) / `- [ ]`(예정) 체크박스.

## 2026-05-29T05:10:00Z — D1 edge-of-chaos Φ 실리콘 검증 🟢 (3/3 PASS · GREEN_NUMERICAL_CONFIRM)

- [x] harness 작성 — `AKIDA/akida_edge_of_chaos_phi.hexa` (phi_silicon_proxy = activity_gate × integration × differentiation × entropy_weight · 정직 명명 · iit4 big_phi 의 multi-axis Φ 의미 보존)
- [x] mock smoke 통과 — 합성 R1~R4 raster 3/3 PASS 0.000/0.456/0.250/0.000 (HW_SPONTANEOUS_EMISSION_2026_05_22 baseline 수치 입력)
- [x] pi5-akida AKD1000 실측 — `BackendType.Hardware` BC.00.000.002 · n_neurons=16 · 200 step · seed=187 · 4 regime sweep 카논 `SUB_ENGINES/AKIDA/state/spontaneous_emission_result_2026_05_22.json` (live R3 streamer 中단 없이 기존 측정 활용)
- [x] verdict — F-AKIDA-EDGE-1 PASS (Φ(R2)=0.297 > Φ(R1)=0.000) · F-AKIDA-EDGE-2 PASS (Φ(R3)=0.250 > Φ(R1)=0.000) · F-AKIDA-EDGE-3 PASS (edge_max=0.297 ≥ Φ(R4)=0.000) · 3/3 → all_pass → **GREEN_NUMERICAL_CONFIRM**
- [x] inverse-U(∩) 곡선 실리콘 확증 — order={0.000, 0.475, 0.500, 1.000} 축 위 Φ={0.000, 0.297, 0.250, 0.000} edge-of-chaos peak (R2/R3 중심) · die-out floor (R1) · over-driven floor (R4)
- [x] H_670 / `pe_edge_of_chaos_peak` (CORE M2 🟡 PARTIAL) — ECA + logistic 시뮬 universal-but-PARTIAL → AKIDA AKD1000 silicon transfer **confirmed** (cross-substrate 3-class 정합 — ECA · logistic · neuromorphic silicon)
- [x] 산출물 — `state/akida_edge_chaos_phi_2026_05_29/{result.json, akd1000_spontaneous_emission_2026_05_22.json, hexa_run_verbatim.log}` · CORE/phi_envelope_substrate.hexa 주석 tier 노트 추가
- [x] M2 tier 재평가 — 🟡 PARTIAL → 🟢 numerical 후보 (silicon transfer 확증 + cross-substrate 정합 + 2-component 분리 Φ proxy)

## 2026-05-29T00:00:00Z — 도메인 신설 + 활용 아이디어 카탈로그 seed

- [x] AKIDA 도메인 신설 — `AKIDA/AKIDA.md`(스냅샷) + `AKIDA.easy.md`(쉬운 카탈로그) + `AKIDA.log.md`(로그), DOMAINS.tape 등록
- [x] 활용 아이디어 추출 — 18개 이상 (CORE×AKIDA 8 + 자연발화/세포/측정/채널 그룹), 전부 $0 pi5-로컬
- [x] sibling 양방향 엮음 — CORE · MITOSIS · WAKE · CHANNEL · EEG · UNIVERSE
- [ ] 다음 = D1 edge-of-chaos Φ 실리콘 검증 (파킹된 plan `drafts/akida-edge-of-chaos-phi-plan.md`) · D2 substrate-class 등록
- [ ] 환류 — 측정 결과는 UNIVERSE/CANDIDATES.md 에 기록 (bench SSOT)
