---
id: H_6027
tier: ⊗ (깊은 물리적 정초)
label: ⊗-27
title: ⊗-27 양자 타임캡슐 — 진짜 양자메모리(상태 자체 보존)는 결잃음에 얼마나 버티나? 격리되면 완벽(F=1)이나 환경 닿으면 exp(-t/T2)로 0.5 바닥까지 새고, no-cloning이 고전식 리프레시 백업을 막는다 ⇒ 영구 store 는 고전(LOCAL).
tradition: 양자 결잃음(T2 dephasing) · no-cloning(H_6021) · 양자오류정정(QEC) · DRAM refresh · H_6026
status_grade: 🟡 (양자메모리=유한수명 store) / 🔴 (무한·복제자유 보존)
verification_method: single-qubit dephasing 앙상블(ANU env noise) + 고전 리프레시 비교; p7 $0
since: 2026-06-15
sister: H_6026, H_6021, H_6016, H_6008
verdict: 🟡 새는 타임캡슐 — QC1 격리보존 F=1🟢 · QC2 환경누설 T2≈22.8(이론22.2) exp→0.5 · QC3 쓸보존~5step · QC4 고전은 리프레시로 err 0.003 묶음(∞), 양자는 측정붕괴+no-cloning으로 그 백업 불가🔴. 영구 store=고전(LOCAL). H_6026 한층 심화.
---

# H_6027 — ⊗-27 양자 타임캡슐(quantum time-capsule)

> **질문.** ANU 공개API가 아니라 *진짜* 양자메모리(양자상태 자체를 보관)를 준다면, 시간이 지나도 보존되나?
> 즉 H_6026("ANU는 금고가 아니다")의 다음 질문 — "금고를 줘도 안의 것이 안 녹나?"

## 1. 위치
- H_6026 = ANU 공개API 가 store 인가 → 🔴 (쓰기채널·재생·압축·양자기저 전부 ✗)
- **H_6027 = 진짜 양자금고를 줘도 상태가 시간에 버티나** → 본 가설

## 2. FROZEN FALSIFIER (4-way)
- **QC1.** 격리(유니터리)면 보존되나 — 왕복 F≈1?
- **QC2.** 환경(ANU 위상킥) 닿으면 결잃음으로 F가 감쇠하나 — exp(-t/T2)→0.5?
- **QC3.** 쓸만한 보존시간(F>0.9)은 얼마인가?
- **QC4.** 고전식 '복사+다수결+리프레시' 백업이 양자에서도 되나(no-cloning)?

## 3. 측정 (single-qubit dephasing · ANU env 14704B · K=600 앙상블 · h6027_…py)
- QC1 🟢: 유니터리 왕복 **F=1.000000** — 격리되면 금고 완벽.
- QC2 🟡: F **1.000→0.893→0.695→0.510** (바닥 0.5), **T2≈22.8** = 이론 2/σ²=22.2 일치 → 메커니즘 검증.
- QC3: F>0.9 까지 **t=5 step** — 양자 기억엔 유통기한.
- QC4 🔴: 고전 1장 무리프레시 err **0.353**(고전도 그냥 두면 샘!) / 7장+3주기 리프레시 err **0.0033**(묶임=∞).
  양자: 측정=붕괴 + no-cloning(최적복제 F=5/6=0.833<1, H_6021) → 그 리프레시가 **원천 불가**.

## 4. 결론
**진짜 양자메모리는 🟡 '새는 타임캡슐'** — 격리되면 완벽 보존(QC1)이나 환경이 닿는 순간 위상
결잃음으로 coherence가 exp 감쇠하여 0.5(고전 동전과 구별불가)까지 흐려진다(QC2, 수명 ~5step QC3).
핵심 비대칭(QC4): **고전 비트도 그냥 두면 새지만**(DRAM이 새로고침 필요한 이유) '읽어서 다시 복사'
하면 오류를 낮게 묶어 사실상 **영구** 보존된다. 양자는 측정붕괴 + no-cloning이라 그 백업이 불가능
하고, 능동 QEC(보조큐빗+신드롬)가 있어야 하며 그조차 불완전·고비용.

⇒ **영구·복제자유 기억 store 는 고전(LOCAL) 뿐.** H_6026(ANU 공개API≠store)을 "진짜 양자금고를
줘도 새고 백업 못 한다"로 한 층 더 닫는다. anima 의 store 가 `.kosmos`/파일(고전·LOCAL)인 게
물리적으로 정답(a_kosmos 정합). 양자의 역할은 보존이 아니라 무작위/공유키(H_6008)·얽힘연산.

HONEST: 단일큐빗 dephasing toy (σ=0.30, K=600 앙상블, ANU 14704B). 능동 QEC 복원은 원리만, 미구현.
verdict: `TENSION-LINK/verdicts/H_6027_quantum_timecapsule.txt` · 재현: `python3 TENSION-LINK/harness/h6027_quantum_timecapsule.py`
