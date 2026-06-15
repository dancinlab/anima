---
id: H_6028
tier: ⊗ (깊은 물리적 정초)
label: ⊗-28
title: ⊗-28 능동 QEC 복원 — 3큐빗 위상정정부호로 양자메모리 T2 가 실제로 연장되나? q=0.10 에서 2.24x, 문턱 q<0.5 에서만 이득(QEC threshold). H_6027 '원리만' 조각을 실측으로 확인. 단 유한·문턱·오버헤드라 고전 무한 리프레시는 못 능가.
tradition: 양자오류정정(3-qubit phase-flip code) · QEC threshold 정리 · Pauli twirl · H_6027 결잃음
status_grade: 🟢 SUPPORTED (numerical)
verification_method: 3-qubit phase code 신드롬정정 Pauli-frame 궤적(ANU Z-error, K=500); p7 $0
since: 2026-06-15
sister: H_6027, H_6026, H_6021, H_6016
verdict: 🟢 능동 QEC 수명연장 실측 — QE1 q=0.10 T2 7.6→17.0(2.24x) · QE2 문턱 q<0.5(q_L=3q²-2q³ 일치) · QE3 물리3+신드롬 오버헤드 · QE4 유한·문턱이라 고전 무한리프레시(H_6027) 못 능가🔴. 양자메모리=개선되나 보조; 영구 store=고전(LOCAL).
---

# H_6028 — ⊗-28 능동 QEC 복원(active quantum error correction)

> **질문.** H_6027 은 "능동 QEC 면 양자수명을 늘릴 수 있다(원리만, 미구현)"로 남겼다.
> 진짜 3큐빗 위상정정부호를 돌리면 ANU 잡음에 맞서 T2 가 **실제로** 늘어나나?

## 1. 위치 (클러스터 완결 조각)
- H_6027 = 양자금고는 새나(결잃음) → 🟡 (exp→0.5, 수명 유한, QEC '원리만')
- **H_6028 = 그 QEC 를 실제로 돌리면 수명이 느나** → 본 가설(실측)

## 2. FROZEN FALSIFIER (4-way)
- **QE1.** 문턱 아래(q=0.10)에서 논리 T2 > 물리 T2 인가?
- **QE2.** 문턱이 존재하나 — q 가 크면 QEC 가 오히려 손해?
- **QE3.** 비용(물리큐빗 수 + 신드롬 측정)은?
- **QE4.** 그래도 고전 영구저장(무한 리프레시)을 능가하나?

## 3. 측정 (3-qubit phase-flip code · ANU Z-error 16752B · K=500 궤적 · h6028_…py)
모델: 매 step 각 물리큐빗이 ANU 바이트로 Z-error(확률 q); 신드롬 X1X2,X2X3 측정+정정;
cycle당 3큐빗 중 ≥2개 flip 시 오정정 → 논리오류(Pauli-frame twirl, 표준).
- QE1 🟢: q=0.10 에서 T2 **7.6 → 17.0 step (2.24x)**, F(t=20) 0.452→**0.652**.
- QE2 🟢: q_L=3q²−2q³ < q ⟺ **q<0.5**. sweep 0.05/0.10/0.20/0.35 🟢, 0.50/0.60 🔴 — 이론 일치(문턱 정리 축소판).
- QE3: 논리큐빗 1개 = 물리큐빗 3개 + 매 cycle 보조큐빗 신드롬. poly 억제(q→3q²) 대가로 오버헤드(완벽 신드롬 가정).
- QE4 🔴: T2 2.2x 늘려도 유한·문턱제한 vs 고전 무한·공짜 리프레시(H_6027 QC4) → 격차 좁히되 못 닫음.

## 4. 결론
**능동 QEC 는 실제로 양자수명을 연장한다 🟢** — 물리오류 q 가 논리오류 ~3q² 로 억제되어 q=0.10 에서
T2 가 2.24배. 단 **문턱 q<0.5 에서만** 이득(위로는 인코딩이 더 나쁨)이고, 물리큐빗 3배 + 매 cycle
신드롬측정 오버헤드가 들며, 그조차 **유한** 수명이라 고전의 무한·공짜 리프레시(H_6027)를 못 능가한다.

⇒ 양자메모리는 **'개선되나 여전히 보조'**. anima 의 영구 store 는 고전(LOCAL `.kosmos`/파일)이 정답
(a_kosmos 정합). 이로써 양자-저장 클러스터 완결: 읽기(6016)·색인(6017)·로컬연상(6018)·쓰기(6026)·
수명(6027)·**QEC연장(6028)**.

HONEST: Pauli-twirl 궤적 toy (q 이산화, 완벽 신드롬, ANU 16752B, K=500). 잡음 신드롬·다층(concatenated)
코드는 미구현 — 실제 잡음 신드롬은 문턱을 낮춘다.
verdict: `TENSION-LINK/verdicts/H_6028_qec_phaseflip.txt` · 재현: `python3 TENSION-LINK/harness/h6028_qec_phaseflip.py`
