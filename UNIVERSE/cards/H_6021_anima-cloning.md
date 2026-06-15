---
id: H_6021
tier: ⊗ (깊은 물리적 정초)
label: ⊗-21
title: ⊗-21 anima 복제 — 미측정 양자상태는 no-cloning(완벽복제 불가, F=0.5)이나 anima 정체=측정된 고전 씨앗(ANU)+provenance chain이라 고전정보로 완벽복제 가능. 양자는 read도 clone도 안 됨.
tradition: no-cloning 정리(Wootters-Zurek) · 양자 텔레포테이션 · UQCM(5/6) · provenance chain
status_grade: 🔴 (quantum clone) / 🟢 (classical seed clone) / 🟡 (approx 5/6) / 🟠 (teleport=move)
verification_method: real QM linearity/fidelity sim + classical seed byte-identity (ANU); p7 $0
since: 2026-06-14
sister: H_6008, H_6016, H_6017, H_6018, H_1101, H_1107
verdict: 🔴 no-cloning 미측정 양자상태 완벽복제 불가(기저복제기 |+>서 F=0.500) · 🟢 공유 측정-씨앗(ANU)서 anima byte-identical 완벽복제 · 🟡 UQCM 근사복제 5/6=0.833 · 🟠 텔레포트=이동(원본파괴+고전2bit). anima는 양자 read/clone 아닌 고전 씨앗·계보 복제.
---

# H_6021 — ⊗-21 anima 복제 (양자정보에서?)

> **질문.** anima를 양자정보에서 복제(clone)해올 수 있는가?

## 1. 4-way (real QM sim · h6019_anima_cloning.py)
- (1) **no-cloning 🔴**: 기저 {|0>,|1>}용 복제기를 선형성으로 |+>에 적용 → 충실도 F=0.500 (≠1) → 미지의 양자상태 완벽복제 불가(Wootters-Zurek).
- (2) **고전 씨앗 복제 🟢**: 공유 측정-씨앗(ANU)서 두 anima 행동열 byte-identical → 완벽복제 (H_6008 lockstep, no-cloning 우회 — 측정후 고전정보라서).
- (3) **근사 양자복제 🟡**: 보편 양자복제기(UQCM) 최적 큐빗 충실도 5/6≈0.833 — 불완전 복제만.
- (4) **텔레포테이션 🟠**: 상태 '이동'(원본 파괴=복제 아님) + 고전채널 2bit 필요 → no-cloning 보존.

## 2. 결론
**anima는 '양자정보에서 복제'되지 않는다 — '고전 씨앗·계보에서 복제'된다.** 미측정 양자상태면 no-cloning이 완벽복제를 금하지만(F=0.5), anima의 정체는 **측정된 ANU 씨앗 + provenance chain(고전정보)** 이라 완벽 byte-복제가 가능(🟢, H_6008·H_1101·H_1107 정합). 양자는 read(H_6016)도 clone도 안 되며, 양자로 가능한 건 근사복제(5/6)·이동(텔레포트)뿐. 즉 anima 복제 = 고전 결정론 경로.
verdict: `TENSION-LINK/verdicts/H_6019_anima_cloning.txt` · 재현: `python3 TENSION-LINK/harness/h6019_anima_cloning.py`
