# H_9300 — LINEAGE under COUNT-STARVATION (H_9299 공허 스윕의 1차 수리 시도)

**Tier: ⛔ VACUOUS — 결과 아님 (측정 실패 · 정직 보고) · group MITOSIS-ENGINE · 2026-07-14**

- freeze → `state/h9298_mitosis_shrinkage/FREEZE_H9300.txt` · script → `h9300_starved_lineage.py`
- result → `state/h9298_mitosis_shrinkage/results/h9300_summary.json`

## 의도
H_9299 의 스윕이 공허했으므로(grow_max 를 올려도 11 셀), **분열 술어**(`SPLIT_THRESH_CE` · `MIN_OWNED`)가 구속조건이라 보고 그것을 굶주림 축으로 이동시켜 재발사했다: `(thresh:grow_max) ∈ {0.05:40, 0.005:40, 0.0:40, 0.0:120, 0.0:400}`, `MIN_OWNED=2`.

## 결과 — ⛔ 스윕이 **또** 공허했다

**전 5 지점이 11 셀 그대로** (A1/FLAT/LIN/SHUF 값이 전부 동일). `split_thresh=0.0` · `min_owned=2` · `grow_max=400` 로도 셀이 늘지 않았다 ⇒ **분열 술어는 구속조건이 아니었다.** 동결 bar(L1·L2)는 굶주린 영역을 측정하지 못했으므로 **판독 불가** — 이것은 과학 결과가 아니라 **측정 실패**다 (`infra-wall-noneval` · 정직 보고, bar 무이동).

## 이 실패가 낳은 것
"왜 안 늘어나는가"를 추측하지 않고 성장 루프를 **직접 계측**했고 → 진범이 `grow_on` 의 **퇴화 median 분할 시 루프 전체 `break`** 임을 확정했다 (셀 하나가 못 쪼개지면 나머지 전부의 성장이 동반 종료). ⇒ **H_9301** 이 그 결함을 수리하고 실제로 굶주린 영역(320 셀)에 도달했다.

> 교훈(계측): 스윕이 무변화를 내면 "효과 없음"이 아니라 **"축이 안 걸렸다"** 를 먼저 의심하라. 두 번의 공허 스윕이 없었으면 11-셀 하드캡을 발견하지 못했다.

## HONEST
결과 없음(no verdict). frozen bars 판독 불가. bar 이동 0.
