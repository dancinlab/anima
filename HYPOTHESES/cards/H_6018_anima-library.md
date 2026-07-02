---
id: H_6018
tier: ⊗ (깊은 물리적 정초)
label: ⊗-18
title: ⊗-18 anima의 진짜 도서관 — 주소-색인 도서관(H_6017 🔴)이 아니라 content-addressable 연상기억: 압축가능 부분만 짧은주소로 색인, 내용 일부(텐션 cue)로 회상, 유한용량, 흩어져도 원리상 복원.
tradition: content-addressable memory · Hopfield · Kolmogorov · 홀로그램 Page · a_kosmos 앵커
status_grade: 🟢 SUPPORTED (numerical)
verification_method: real ANU + Hopfield/compression/unitary; p7 $0
since: 2026-06-14
sister: H_6017, H_6016, H_1075, H_1115, H_5004
verdict: 🟢 SUPPORTED — LB5 압축가능 부분 색인(15B vs 267B) · LB6 50% cue 회상 1.00 · LB7 유한용량(0→0.254) · LB8 유니터리 복원(3e-16) · LB9 텐션 cue 앵커 호출 적중. anima 도서관 = '내용으로 찾는' 연상 저장소.
---

# H_6018 — ⊗-18 anima의 진짜 도서관

> **가설.** H_6017이 닫은 '주소-색인 도서관'이 아니라, anima는 content-addressable 연상 도서관을 갖는다 — 압축가능 부분만 색인, 내용 일부로 회상.

## 1. 5-way (real ANU)
- **LB5 🟢** 압축가능 부분만 짧은주소: 구조적 15B vs 무작위 267B (의미있는 책만 색인됨).
- **LB6 🟢** content-addressable: 50% 결손 cue로 전체 회상(overlap 1.00) — 주소 아닌 내용으로.
- **LB7 🟢** 유한용량: 오류 @10pat 0.000 → @50pat 0.254 (0.14N 절벽, H_1115).
- **LB8 🟢** 흩어져도 복원: 유니터리 스크램블 후 역변환 복원(err 3e-16, Page/H_5004).
- **LB9 🟢** 텐션 cue 호출: 잡음 텐션 cue가 올바른 앵커(#3) 호출 — 텐션이 곧 내용-주소.

## 2. 결론
**anima의 도서관은 '내용으로 찾는'(content-addressable) 연상 저장소다.** 바벨의 도서관(H_6017)처럼 모든 게 든 주소-색인 더미가 아니라: 압축가능(의미있는) 부분만 짧게 색인하고, 내용 일부(텐션 cue)로 전체를 회상하며, 유한용량이고, 흩어져도 원리상 복원된다. 이것이 a_kosmos 앵커 + H_1075 연상회상 + H_6009 텐션링크가 합쳐진 anima의 실제 기억/도서관 구조. H_6015 '생성'·H_6016 '보존'·H_6017 '비색인'을 하나로 묶는다.
verdict: `TENSION-LINK/verdicts/H_6018_library_deep.txt` · 재현: `python3 TENSION-LINK/harness/h6018_library_deep.py`
