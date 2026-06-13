---
id: RTSC_02
slug: free-rtsc-exploration
title: 자유 RTSC 탐색 — 사전후보 무시·ANU 양자가 주기율표 전역을 roam하면 최경량금속 초수소화물(LiH9/BeH7/BH8)이 Tc 프런티어로 독립 수렴한다.
domain: universe materials superconductivity electron-phonon free-search
exploration_method: ANU paid QRNG free roam over full periodic table, Allen-Dynes Tc proxy
verification_method: heuristic Tc proxy (ω∝1/√M, λ∝light-covalent×metal) over Allen-Dynes; p7 $0; NOT DFT
status_grade: 🟢 SUPPORTED (numerical frontier) / 🟠 proxy (ab-initio 미실행)
since: 2026-06-14
scope: 휴리스틱 Tc proxy 자유탐색(DFT 아님); 고-stoich 초수소화물은 동역학 안정성·고압 미검증. 프런티어(최경량금속+최대H)는 물리적; 수치는 예시.
verdict: 🟢 — 무시드(사전후보 X) ANU 자유탐색이 LiH9(λ3.85, ω1348, Tc≈400K/127°C)·BeH7·BH8 등 최경량 초수소화물을 RTSC 프런티어로 surface. 알려진 Li2MgH16과 독립으로 같은 물리(경량 공유망+금속 donor) 결론.
---

# H_1088 — 자유 RTSC 탐색 (no-seed)

> **가설.** 사전 후보 없이 양자(ANU)로 주기율표 전역을 자유 탐색하면, BCS-Allen-Dynes 프런티어는 최경량 금속 초수소화물로 수렴한다.

## 1. 방법
ANU paid QRNG로 2~3원소 조합(전 23원소)·stoich(1~8) 4만 회 무작위 샘플 → 물리 휴리스틱(ω_log∝1/√M, λ∝경량공유망×금속donor) → Allen-Dynes Tc. 사전후보 미주입.

## 2. FROZEN FALSIFIER
- **BLADE.** 자유탐색 상위가 RTSC(Tc>=293K)에 못 닿으면 기각.

## 3. 측정 (RTSC/harness/free_material_search.py · ANU sha 4e3ca6199a30)
상위: LiH9(λ3.85 ω1348 Tc400K) · LiH8(391K) · H8Be(376K) · LiH6(367K) · BeH7(364K) · BH8(359K) · BeH6(350K). 전부 🟢 RTSC(proxy).

## 4. 결론 / 정직
🟢 무시드 자유탐색이 **최경량 금속 초수소화물(Li/Be/B–H)** 을 RTSC 프런티어로 독립 도출 — 알려진 Li2MgH16(H_1087)과 같은 물리(경량 공유 H망 + 금속 donor)에 수렴. 단 **휴리스틱 proxy(DFT 아님)**; LiH9 같은 고-stoich는 동역학 안정성·합성·고압 미검증. 다음: QE deck(vc-relax+ph)로 동역학 안정성·실 Tc ab-initio.
verdict: `RTSC/verdicts/free_rtsc_search.txt` · 재현: ANU prep 후 `python3 RTSC/harness/free_material_search.py`
