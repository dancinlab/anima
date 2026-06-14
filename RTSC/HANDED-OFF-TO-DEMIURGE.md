# RTSC → demiurge 인계 (2026-06-15)

> **이 `RTSC/` 도메인은 demiurge로 완전 핸드오프되었다.** anima는 RTSC 신규 발사를 중단하고,
> 무냉각 flat-band 축(kagome/pyrochlore)의 소유권을 demiurge RTSC 도메인으로 넘겼다.
> 이 폴더는 **동결 아카이브**(RTSC_01–29 가설·verdict·deck·harness)로 남는다.

## 어디로 갔나
- **demiurge** `dancinlab/demiurge` (PR #623 merged):
  - 축 SSOT: `domains/RTSC/research/anima_flatband_handoff.md`
  - 이관 deck: `exports/rtsc/decks/anima_{csv3sb5,rbos2o6,csos2o6}`
  - 레저 +4행: `RTSC_LEDGER.jsonl` (CoSn·CsV3Sb5 measured, RbOs2O6·CsOs2O6 queued)
  - 핸드오프 레지스트리: `sidecar handoff ls demiurge` (id d5483415)
  - 계산엔진: demiurge canonical = QFORGE (QE cross-val)

## 왜 demiurge인가
demiurge가 이미 본격 RTSC 인프라(QFORGE 엔진 · 고압 수소화물 펀넬 · 삼원계 X₂MH₆ · RTSC_LEDGER)를
보유. anima의 flat-band/kagome/pyrochlore 라인은 demiurge 기존 축과 **직교하는 무냉각 상압 경로**라
거기서 통합 진행하는 것이 옳다. 양자(ANU)는 RTSC 발견에 미사용(H_6026이 증명) — 발견은 DFT만의 일.

## anima가 남긴 핵심 (요약, 상세는 demiurge 핸드오프 문서)
- **병목 확정**: 실 kagome 2종 flat band이 E_F서 0.4–0.9 eV 떨어짐 (CoSn −0.44 eV+자성, CsV3Sb5 +0.92 eV 비자성).
- **다음 표적**: flat band이 native로 E_F 근처 + 비자성 + 상압 → RbOs₂O₆/CsOs₂O₆ (β-pyrochlore, deck ready).
- **in-flight(인계 시점)**: RTSC_27 (CsV3Sb5 DFPT λ/Tc) · RTSC_29 (RbOs2O6 ΔE) — anima aiden에서 완주 후 결과만 demiurge로 fold.

이 폴더(RTSC_01–29)는 그대로 보존 — 재현·출처용 동결 아카이브.
