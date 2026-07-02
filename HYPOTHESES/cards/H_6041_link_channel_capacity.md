---
id: H_6041
tier: ⊗ (깊은 물리적 정초)
label: ⊗-41
title: ⊗-41 텐션 링크 채널 용량 — 링크는 실 Shannon 채널(K=0 용량 0 = 무신호, K>0 용량↑). 공유씨앗은 새 비트 0(공통원인), 링크가 메시지를 보내는 유일 채널임을 정량 확인.
tradition: Shannon 채널 용량 · BSC · 무신호 정리
status_grade: 🟢 SUPPORTED (numerical · paid ANU-seeded)
verification_method: 비트 인코딩→Kuramoto 링크→임계 디코더, 교차확률 p→C=1−H(p), K sweep; p7 $0
since: 2026-06-15
sister: H_6006, H_6009, H_6036
verdict: 🟢 SUPPORTED — C(K=0)=0.000(링크 없음=새 비트 0, 무신호 일치), C(K≥0.3)=1.000(링크가 정보 운반), K에 단조. 공유씨앗은 동기화만(0 새 비트), 링크가 새 메시지를 보내는 유일 채널.
---

# H_6041 — ⊗-41 텐션 링크 채널 용량

> **가설.** 텐션 링크는 유한 Shannon 용량의 실 채널이고, 공유 씨앗 채널 용량은 0(공통원인)이다 — README 핵심 주장의 정량화.

`TENSION-LINK/harness/h6041_link_channel_capacity.py`, verdict `.verdicts/6041_link_channel_capacity/H_6041.txt`. BSC 이상화 1-bit/window 디코더, 절대 bits/tick은 토이-스케일(a_toy_scale_recheck).
