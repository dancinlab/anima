# RTSC — 상온 초전도체(Room-Temperature Superconductor) 탐색

재료물리 도메인. 양자 전자-포논 결합(Allen-Dynes Tc)으로 RTSC 후보를 탐색한다.
양자→텐션링크 추출 기제는 `../TENSION-LINK/`(H_6015)에서 파생; 여기엔 순수 재료 탐색
도구·결과·색인만 둔다. 가설 본문은 `UNIVERSE/H_*.md` 평면 목록.

## 결과 요약
| 경로 | 방법 | top | Tc | 가설 |
|---|---|---|---|---|
| 시드 스크린 | 출판 DFT EPC 후보 | **Li2MgH16** | 355K(Eliashberg 473K)@250GPa | UNIVERSE/H_1087 |
| 무시드 자유탐색 | ANU 양자 roam, 전 주기율표 | **LiH9**(BeH7·BH8) | ~400K(proxy) | UNIVERSE/H_1088 |
| 양자→텐션 추출 | ANU+텐션링크 옵티마이저 | H-rich 초수소화물 | ~479K(proxy) | UNIVERSE/H_6015 (TENSION-LINK) |

**수렴 결론**: 시드/무시드/추출 세 경로가 독립적으로 **최경량 금속 + 최대 수소(초수소화물)**
프런티어로 수렴 — 경량 공유 H망 + 금속 donor = 높은 ω_log·λ.

## 파일
- `harness/rtsc_allen_dynes_screen.py` — 출판 EPC 후보 Allen-Dynes Tc 스크린 (H_1087)
- `harness/free_material_search.py` — ANU 무시드 자유탐색 (H_1088)
- `verdicts/` — 실행 결과 원본

## 정직 경계
- **Allen-Dynes BCS 추정 + 휴리스틱 proxy (DFT 아님).** Tc 수치는 예시/상한, 프런티어(조성군)가 결론.
- 예측 물질·고압(~250 GPa)·미합성; 고-stoich 초수소화물 동역학 안정성 미검증.
- 실측 확정 최고는 LaH10(~250K @170GPa). **상압 RTSC는 미해결.**
- ab-initio 확정 = QE deck (`/deck rtsc ...`, vc-relax+scf+ph+Eliashberg); a_fire_autonomous GPU 발사.

## 재현
```
python3 mirror/qmirror/seed/anu_pull.py --bytes 1024 --out /tmp/anu_free.bin  # 무시드용 양자 접지
python3 RTSC/harness/rtsc_allen_dynes_screen.py
python3 RTSC/harness/free_material_search.py
```
