# RTSC — 가설 목록 (UNIVERSE와 분리된 재료물리 도메인)

상온 초전도체(RTSC) 탐색 가설의 **별도 목록**. anima/UNIVERSE 의식 가설과 성격이 달라
여기 따로 등재. 검증 도구·verdict 는 `RTSC/harness/` · `RTSC/verdicts/`.

| id | 제목 | grade | 핵심 |
|---|---|---|---|
| RTSC_01 | 후보 스크린 (Allen-Dynes) | 🟢/🟡 | Li2MgH16 Tc≈355K@250GPa (Eliashberg 473K) |
| RTSC_02 | 무시드 자유탐색 (ANU) | 🟢 | LiH9·BeH7·BH8 (최경량 초수소화물) Tc~400K(proxy) |
| RTSC_03 | 압력 프런티어 (확정가능성) | 🟢/🔴 | RTSC는 >250GPa; 상압 RTSC 미해결; 확정최고 LaH10 250K@170GPa |
| RTSC_04 | 양자+텐션 확정가능 찾아오기 | 🟡/🔴 | 저압 후보 ~121K@73GPa; P↔Tc 트레이드오프 못 깸 |
| RTSC_05 | LANE A 호버보드 | 🟢/🔴 | 냉각형 YBCO+LN2 가능; 무냉각 상온 미해결 |
| RTSC_06 | LANE B 핵융합 자석(demiurge) | 🟢/🟠 | REBCO 20T@20K 실현; RTSC=비용급감 최대수혜 |
| RTSC_07 | LANE C UFO 반중력/추진 | 🔴/🟠 | 반중력 무근거; SC자석 MHD추진만 유용 |

## 실용 응용 3 LANE → `RTSC/LANES.md` (호버보드·핵융합·UFO)

## 수렴 결론
시드(RTSC_01)·무시드(RTSC_02)·양자추출(UNIVERSE/H_6015) 세 경로가 **최경량금속 초수소화물**
프런티어로 독립 수렴. 그러나 RTSC_03/04: **압력이 확정의 장벽** — 상온은 초고압 필요(미합성),
저압은 sub-RT. **상압 확정 RTSC는 미해결(open)**.

## 관련 (UNIVERSE ⊗ 연결-arc, 기제는 거기)
- UNIVERSE/H_6015 양자→텐션 물질추출 · H_6016 양자=저장소? · H_6017 도서관? · H_6018 anima 도서관
  (= '추출'은 DB read 아닌 ANU구동 최적화라는 기제적 토대)

## 정직 경계
Allen-Dynes BCS proxy (NOT DFT) · 예측 물질·미합성 · ab-initio 확정 = QE deck (`/deck rtsc`, vc-relax+scf+ph+Eliashberg, a_fire_autonomous GPU).
