# STRANGELOOP — cycle history

Append-only chronological log. `STRANGELOOP.md` 는 latest only — history 는 여기.

---

## Cycle #0 — 2026-05-23 (design)

- **focus**: 실험 3 도메인 정의 — Hofstadter "strange loop = 자기참조 = 의식"
  의 substrate-native 번역
- **trigger**: 사용자 제공 — *I Am a Strange Loop* (Douglas Hofstadter) 표지
- **change**:
  - `STRANGELOOP.md` skeleton — 가설 (self-feed loop → 안정 attractor 수렴) /
    pipeline (output→next prompt N-iter, open-loop control) / F-SLOOP-1..5
    pre-registered / C3 5건
  - `LAB/README.md` 실험 목록 표 — 실험 3 STRANGELOOP (B.의식 동역학) 등재
- **verdict**: DESIGN — UNFIRED
- **next**: **Cycle #1** — self-feed loop driver 스크립트 (chat_generate 출력을
  next prompt 로 N=20 iteration, 매 iter anima_spike 기록 + open-loop control).
  신규 tool 불필요. 실험 1·2 진행과 병렬 가능.
  - 1차 지표 = response_text 의 iter 간 수렴 (결정론적), split 은 보조
  - wall 추정: ~20 iter × 2 (loop+open) ≈ 분 단위, $0
