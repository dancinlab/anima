# PSILOCYBIN — cycle history

Append-only chronological log. `PSILOCYBIN.md` 는 latest only — history 는 여기.

---

## Cycle #0 — 2026-05-23 (design)

- **focus**: 실험 2 도메인 정의 — 실로시빈 의식형성 가설의 substrate-native 번역
- **trigger**: 사용자 제공 — Stoned Ape / entropic brain 가설 ("실로시빈이 의식
  형성에 영향을 줬다", PSILOCYBIN 분자구조 + "답하지 못한 인간의 미스터리들")
- **change**:
  - `PSILOCYBIN.md` skeleton — 가설 (entropic brain → activation-entropy 주입
    inverted-U) / pipeline (farr_add_gaussian_noise σ-dose sweep) / F-PSIL-1..5
    pre-registered / C3 5건
  - `LAB/README.md` 실험 목록 표 — 실험 1 SRH (A.입력-반응) + 실험 2 PSILOCYBIN
    (B.의식 동역학 perturbation) 3-분류 등재
- **verdict**: DESIGN — UNFIRED
- **next**: **Cycle #1** — `psilocybin_dose(chat, sigma)` perturbation wrapper
  tool 신설 (mitosis_hook 의 RFC 033 `farr_add_gaussian_noise` 를 외부 σ-dose 로
  노출). 실험 1 (SRH cycle #4-5) 종결 후 착수.
  - 선결 의존: anima_spike 에 cell_diversity / split_entropy proxy metric 추가
  - 6-point σ grid {0, 0.01, 0.03, 0.1, 0.3, 1.0} × 3-5 seed
  - wall 추정: SRH cycle 들이 분 단위 → ~10 min mini, $0
