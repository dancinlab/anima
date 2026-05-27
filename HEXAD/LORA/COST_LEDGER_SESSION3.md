# LORA session-3 cost ledger (2026-05-22 ~ 2026-05-24, R8a' in-flight)

LORA saga session-3 누적 cost SSOT. 기존에 여러 doc 에 산재되어 있던 비용 항목을 단일 ledger 로 통합한다. R8a' 완료 후 확정 cost 는 다음 update 에서 반영.

## § Cumulative table

| wave/axis | fire wall | cost | result | PR |
|---|---|---|---|---|
| Wave-12 | ~5 min | $0.30 | VP21M_WORKS | #144 |
| Wave-13/v9 | ~5 min | $0.30 | n_strong 4 | #150 |
| Wave-14/v10 | ~5 min | $0.30 | NO SWAP | #162 |
| Wave-15/v11 | ~5 min | $0.30 | NO SWAP (cont 34 min) | #184 |
| Wave-16/v12 | ~5 min | $0.27 | NO SWAP (U-shape 발견) | #205 |
| V3 Phase 2 fix | 1649s | $0.27 | ko STRONG 19 only | ... |
| V3 Phase 2 full (3B) | 7367s | $3 | FAIL overfit | ... |
| AXIS_MAP envbug 1차 | ~7×0.5h | $4 | env-var concat 버그 | #211 |
| AXIS_MAP 2차 (A/B/F) | 5222+2721+671s | $2.85 | 3/3 FAIL | #249 |
| AXIS_MAP redispatch (C/C2/D/E) | 4× ~45-90min | $6 | C/C2 abort, D FAIL, E OOM | #249 |
| R8a fire LOST | ~30min | $1.20 | SSH drop, no result | (no PR) |
| R8a' IN-FLIGHT | ~90min est | $2.75 est | TBD | (no PR) |
| doc/spec PRs | n/a | $0 | various | #214 #224 #225 #246 #248-260 #336 #339 #356 #357 |

## § Cumulative

session-3 추정 총비용 = **~$22-26** (R8a' 완료 후 확정).

내역 합산 (point estimate):

- VP21M Wave 12-16: $0.30 × 4 + $0.27 = **$1.47**
- V3 Phase 2 (fix + full): $0.27 + $3 = **$3.27**
- AXIS_MAP-FAN (envbug + 2차 + redispatch): $4 + $2.85 + $6 = **$12.85**
- R8 saga (R8a LOST + R8a' in-flight): $1.20 + $2.75 = **$3.95**
- doc/spec PRs (Mac local): **$0**

point sum ≈ **$21.54** (R8a' 완료 시점 ±$2-4 변동 예상 → range **$22-26**).

## § Cost-per-finding 효율

| lever | cost | finding 요약 |
|---|---|---|
| Wave 12-16 (VP21M corpus levers) | ~$1.50 | 5 corpus levers explored, 1 sweet spot 발견 (v11) |
| V3 Phase 2 (ko STRONG + 3B fresh) | ~$3.30 | ko STRONG 19 + 3B fail (lesson: 3B fresh underfit) |
| AXIS_MAP-FAN (7 axis sweep) | ~$13 | 5/7 axis FAIL + bug saga learning + cluster X/Y/Z 자연실험 |
| R8 saga (R8a LOST + R8a' relaunch) | ~$4 | wiring 버그 발견 + R8a' relaunch (R8a' 완료 후 closure) |
| doc/spec PRs | $0 | various (Mac local) |

핵심 관찰:

- Wave 12-16 비용 효율이 가장 높음 ($1.50 로 5 lever 탐색 + sweet spot 1).
- AXIS_MAP-FAN 이 단일 라인업 최대 비용 ($13, 전체의 ~50%) — envbug 1차 절반 burn ($4) 포함.
- R8a SSH drop = $1.20 sunk cost, R8a' 로 retry.

## § HF artifacts (a_hf_complete)

- `dancinlab/anima-vp21m-{v5,v6,v7,v8,v11,v12}` PRIVATE, 각 10 files
- `dancinlab/anima-v3-{p21h,e2,e3,axis-f}` PRIVATE

## § Cross-reference

분산 source:

- `HEXAD/LORA/SAGA_SESSION3.md` — session-3 narrative
- `HEXAD/LORA/WAVES_MATRIX.md` — wave-level result matrix
- `HEXAD/LORA/V3_SAGA_MID_RETROSPECTIVE*.md` — V3 mid-retrospective
- `HEXAD/LORA/UPDATE_2026_05_24.md` — 최근 update snapshot
- PRs: #144 #150 #162 #184 #205 #211 #214 #224 #225 #246 #248-260 #336 #339 #356 #357

다음 update 시점 = R8a' 완료 후 확정 cost + finding 합산.
