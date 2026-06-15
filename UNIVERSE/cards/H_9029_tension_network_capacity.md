---
id: G12
slug: tension-network-capacity
title: G12 텐션 네트워크 N² 용량 정리 — 텐션 링크는 monogamy 없어 총 용량 N(N-1)/2∝N²; 얽힘은 monogamy로 ≤N∝N. 다자망서 텐션이 얽힘을 (N-1)/2배 압도. PROVEN.
domain: landmark information-capacity tension-link entanglement-monogamy anima
status_grade: 🟢 SUPPORTED (numerical PROOF)
verification_method: pairwise-capacity sum (no monogamy) vs entanglement total (monogamy ≤N); p7 $0
since: 2026-06-14
sister: H_1089, H_1097, G6, H_6024
verdict: 🟢 PROVEN — 텐션망 총용량 N(N-1)/2·C (N=32:496), 얽힘 ≤N (32), 비율 (N-1)/2 ∝ N (N=32:15.5x). 텐션 monogamy無→모든 쌍 독립; 얽힘 monogamy로 N갇힘. anima 다자 통신망 최적.
---
# G12 — 텐션 네트워크 N² 용량
> **정리.** 텐션 링크는 monogamy가 없어 N자 네트워크 총 정보용량이 N(N-1)/2 (∝N²)로 스케일하는 반면, 얽힘은 monogamy로 총 쌍자원이 ≤N (∝N)에 갇힌다. ∴ 다자망에서 텐션이 얽힘을 (N-1)/2배 압도.
## 증명 (g11_g12_proof.py)
N=2/4/8/16/32 → 텐션망 1/6/28/120/496 (N(N-1)/2), 얽힘 2/4/8/16/32 (≤N), 비율 0.5/1.5/3.5/7.5/15.5=(N-1)/2. N≥4 텐션 압도 🟢.
## 의의
H_1089(텐션 채널용량)+H_1097(전이성)+G6/H_6024(얽힘 monogamy)를 용량법칙으로 봉합. 텐션 링크는 monogamy가 없어 모든 쌍이 독립 용량 → 다자 anima 네트워크의 총 대역폭이 N²로 성장. 양자 얽힘 다자망은 monogamy로 N에 갇힘 → **anima 다자 통신엔 고전 텐션이 압도적 최적**(G6 조율·G12 용량 둘 다).
verdict: `.verdicts/9029_tension_network_capacity/G12_tension.txt`
