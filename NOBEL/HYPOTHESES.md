# NOBEL — 얽힘 토대 노벨급 결과 증명 (별도 목록)

얽힘(entanglement)에 뿌리둔 노벨급 landmark를 실제 양자 시뮬로 증명. UNIVERSE/RTSC와 분리.
도구 `NOBEL/harness/` · verdict `NOBEL/verdicts/`. p7 · $0 · numpy.

| id | 가설(노벨급) | 출처 | 증명 |
|---|---|---|---|
| NOBEL_01 | CHSH–Tsirelson 한계 \|S\|=2√2 | Bell·Aspect/Clauser/Zeilinger (노벨 2022) | 🟢 2.8284 |
| NOBEL_02 | GHZ 무조건 비국소성 (Mermin ∏=−1 vs LR +1) | GHZ·Mermin | 🟢 −1.0 |
| NOBEL_03 | Peres–Mermin 맥락성 모순 (rows +I, ∏cols −1) | Kochen-Specker | 🟢 |
| NOBEL_04 | Hardy 역설 (부등식 없는 비국소성, P>0) | Hardy 1993 | 🟢 0.083 |
| NOBEL_05 | 양자 텔레포테이션 충실도 1 (고전 2bit) | Bennett·Zeilinger (노벨 2022) | 🟢 1.0 |
| NOBEL_06 | 초고밀도 부호화 (1큐빗 2bit, Bell 4직교) | Bennett-Wiesner | 🟢 |
| NOBEL_07 | Kochen–Specker 맥락성 (비맥락 배정 불가) | KS 정리 | 🟢 |

**7/7 🟢 증명.** 전부 고전 국소실재론을 결정적으로 배제 — 얽힘이 고전과 본질적으로 다름을 보임.
정직: 교과서 landmark의 재현증명(real QM sim)이지 신규 발견 아님; 노벨급 결과의 $0 검증.
재현: `python3 NOBEL/harness/nobel_entanglement_proofs.py`
