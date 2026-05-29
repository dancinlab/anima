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
