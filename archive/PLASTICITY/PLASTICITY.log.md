# PLASTICITY — log (append-only)

## 2026-05-30 — 도메인 신설 (akida-hw-first-plasticity PR-A)

- AKIDA on-chip 학습 lane 을 DECODER(추론 lane)와 분리된 형제 도메인으로 신설.
- 근거: 추론은 결정론·byte-identical(akida_sw_lif 1~5차 입증), 학습은 비결정론·HW-only —
  numpy 근사 SW 는 HW on-chip edge-learn 과 **byte-identical 재현 불가(🔴 비동치)**. 한 도메인에
  섞으면 "SW=HW" 거짓 동치 발생 → 형제 분리 (user-confirmed 구조 B + PLASTICITY).
- 신설 산출물: `PLASTICITY/PLASTICITY.md`(@goal+5 milestone) + `PLASTICITY.log.md` +
  `DOMAINS.tape` 1행(`@D PLASTICITY := "./PLASTICITY/PLASTICITY.md" :: domain [active]`) +
  양방향 sibling section(⇄AKIDA ⇄MITOSIS ⇄DECODER ⇄WAKE ⇄UNIVERSE).
- HW-first 스위치 SSOT = `AKIDA/akida_backend.hexa::akida_backend_resolve` (arg>env>default "hw")
  를 재사용 (재발명 금지). HW=`SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py` / SW=numpy 근사.
- 후속: PR-D(lane 배선 + SW 근사 learner 스텁) · PR-F(UNIVERSE H_679 등록 + verdict 포인터).
- 비용 $0 (Mac local scaffold).

## 2026-05-30 — lane 배선 + SW 근사 learner 스텁 (PR-D)

- `PLASTICITY/plasticity_sw_approx.py` — numpy Hebbian 근사 learner (AkidaUnsupervised
  인터페이스 shape 정합: 16-in binary → FC units=10). 실행 PASS (provenance=
  akida-learn-sw-approx · equivalence_to_hw=CLOSED-NEGATIVE · is_hw_substitute=false).
- `PLASTICITY/plasticity_lane.hexa` — 학습 lane 라우터. `akida_backend_resolve_graceful`
  (default "hw") 경유 → HW=edge_learn_probe / SW=approx. provenance "akida-learn-hw" /
  "akida-learn-sw-approx". `import ... as bk` 패턴 = origin/main akida_backend_smoke.hexa
  와 동일(로컬 hexa 툴체인 stale 가 `as` 거부 — 코드 결함 아님, 기존 커밋 파일도 동일 거부).
- HW edge-learn 지원 실측 재확인: edge_learn_probe_2026_05_22.json edge_learning_supported=true
  (BC.00.000.002 · BackendType.Hardware · AkidaUnsupervised compile+fit ok).
- 🔴 **SW↔HW 동치 verdict = CLOSED-NEGATIVE** (`.verdicts/679_plasticity_hw_first/
  sw_hw_nonequivalence.txt`): SW float-weight numpy 근사 ≠ HW 1-bit on-chip Hebbian
  (no learning_competition/pruning/timing state). DECODER 추론 lane(byte-identical 🟢)
  과 대비되는 핵심 경계 — 위조 동치 금지(p7·a_blue_closed). 두 lane 형제 분리 근거.
- milestone M0/M1/M2 done. 후속 = PR-F(H_679 등록).
