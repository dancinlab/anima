# DECODER — log

Append-only history sister of `DECODER.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-27T08:00:00Z — 마일스톤 재정렬 (a_completeness_over_cheap) — MoE-fresh 본선 승격 · merge 강등

- [x] governance `a_completeness_over_cheap` 적용 — 완성도 기준 본선 선정 (싸다 ≠ 본선)
- [x] M3.5 model-merge (이전 ⭐ 최우선) → **M4-probe 강등** — 두 결함 ckpt (underfit + collapse) 보간은 잘해야 "덜 나쁜 중간점", 완성도 미달. optional baseline probe 로만 잔존
- [x] M4-alt MoE (이전 조건부) → **M4 MoE-fresh 본선 승격** — 근본 원인(한 모델이 두 목표 떠안음) 을 arch 로 분리. register-expert / coherent-expert 격리 = 완성도 충족 path
- [x] DECODER.md UNIVERSE-derived 섹션 재작성 — M4 MoE-fresh ⭐ 본선 + M4-probe merge optional
- [x] `UNIVERSE_SYNTHESIS.md` §4 권장순서 + §5 마일스톤 재정렬 반영 (cheap-first → completeness-first)
- [x] M4 sub-step 명시 — M4a router arch (hexa-native) → M4b expert 분리 학습 fire → M4c p7 verify
- [ ] M4a router arch 착수 (V3 head_g → K-expert router · hexa-native 코드) — 다음
- [ ] 사용자 결정 lesson — model-merge-of-failures 같은 절충안 본선 제안 실수 → project.tape governance 화 (#1026)

## 2026-05-27T07:30:00Z — UNIVERSE 도메인 분석 → DECODER 더블바인드 탈출 합성 (M3.5 + M4-alt 신규)

- [x] 사용자 directive — "DECODER 는 UNIVERSE 도메인 분석후 진행"
- [x] UNIVERSE BIO ∩ DECODER 가설 5종 읽음 (H_489–H_493, round-18 cycle#236-240, 모두 🔵 SUPPORTED-FORMAL)
- [x] 매핑 — H_489 apoptosis→token prune · H_490 differentiation→MoE · H_491 clonal→beam · H_492 pruning→head prune · H_493 symbiogenesis→model merge
- [x] 핵심 통찰 — 더블바인드는 단일 모델 한계, 통로는 "분화(MoE)/병합(merge)"
- [x] `CORE/DECODER/UNIVERSE_SYNTHESIS.md` 작성 — 더블바인드 탈출 후보 α(MoE)/β(merge) 분석 + 권장 순서
- [x] DECODER.md 신규 마일스톤 2개 등록 — M3.5 model-merge α-sweep (H_493 · 학습 fire 0 · cheap-tier) + M4-alt MoE register 분리 (H_490 · 조건부)
- [ ] M3.5 model-merge α-sweep 실행 — collapse-avoid ckpt + coherent ckpt 보간 + α 별 p7 verify (다음)
- [ ] 기존 M3b-f 4축 H100 fire ($11-14, 미발사) — merge 실패 시 fallback

