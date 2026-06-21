# H_1531 — 🧱🧬 NEUROMODULATION via CASCADE METAPLASTICITY (Benna-Fusi) on RETENTION-UNDER-INTERFERENCE — WALL HOLDS (DIRECTIONAL)

**tier:** 🧱 WALL HOLDS (R1 numpy DIRECTIONAL — a_engine_native_learning; engine R2 deferred ING)
**verdict source:** `state/verdicts/1531_nm_cascade_meta/H_1531_R1.json` (frozen bars `H_1531_FREEZE.txt`)
**wired:** n/a (WALL — nothing to wire; CORE/*.hexa + H_1284 store machinery UNTOUCHED)

## 가설
H_1284 NEUROMODULATION 벽(11 렌즈 deep)을 census candidate **C2 — CASCADE METAPLASTICITY (Benna-Fusi)** 로, **INTERFERENCE/RETENTION** 능력 위에서 깬다. 선행 probe 는 전부 CLEAN RECALL 을 시험했는데 거기선 capacity 가 monotone 이라 어떤 구조도 도움 안 됨(H_1528 capacity 천장으로 직행, H_1527 expansion clean recall 에서 inert). census + H_1528 자기 진단이 빠진 precondition 을 지목: **FLAT store 가 진짜로 실패하고 구조화 메모리가 이길 수 있는 능력 = INTERFERENCE/RETENTION**(A→B 학습 → K 간섭 사실 → A→B 보존 측정). flat store 는 per-cell consolidation timescale 이 없다 — 모든 덮어쓰기가 같은 속도라 나중의 confusable 사실이 초기 사실을 clobber 한다. Benna-Fusi cascade 는 per-cell 가변 timescale 을 줘서, 반복 확인된 초기 사실이 cascade 로 더 깊이 가라앉아 나중 덮어쓰기에 저항한다.

## 설계 (frozen-first · pre-registered `H_1531_FREEZE.txt`)
H_1284 store 기계 재사용(key_vec FNV-1a / SPLIT_THRESH / ABSTAIN0=0.45 / seeds tune=7 score=[11,22,33] / MARGIN=0.05). 능력 = **RETENTION-UNDER-INTERFERENCE**: 초기 target A→B 작성+반복 CONFIRM(rehearsal N_CONFIRM=3) → K_INTERF=120 나중 간섭 사실(collinear_frac=0.6 이 near-collinear 키로 A 의 cell 에 착지, DIFFERENT 값으로 clobber) → interference horizon 에서 A→B 보존 측정.
**ARMS:** FLAT=single-timescale(best-fixed SPLIT_THRESH grid-tuned, disjoint seed 7) · CASCADE=per-cell Benna-Fusi cascade(3 level DMAX=2; consolidation depth=per-cell confirmation count; incumbent overwrite-prob=1/(1+0.5·depth)) · ABL=cascade depth 동결 0(flat full-clobber 로 회귀) · SHUFFLE=어느 target 이 consolidation rehearsal 받는지 무작위화(consolidation↔초기-사실-정체성 decouple).
**PER-CELL-STRUCTURE-NOT-GAIN(brief hazard):** cascade 변수는 PER-CELL, depth 는 그 cell 자신의 confirmation history 가 설정 — global gain 없음, abstain margin read 없음(흡수된 controller 가족 H_1422 재진입 회피). 자가점검: source 에 margin-conditioned global gain 없음.
**FROZEN:** 🟢 WALL-BROKEN iff retention_cascade − retention_flat ≥ +0.05 on ≥2/3 seeds AND ablation decisive(depth=0 reverts AND shuffle collapses). 🧱 if cascade ties flat on interference(c9, valid). NO tune-to-green.

## 결과 (mean 3 seeds [11,22,33], SPLIT_THRESH*=0.4)
| arm | per-seed retention | mean |
|---|---|---|
| FLAT | [0.125, 0.083, 0.042] | **0.0833** |
| CASCADE | [0.083, 0.125, 0.125] | **0.1111** |
| ABL (depth=0) | [0.125, 0.125, 0.042] | 0.0972 |
| SHUFFLE | [0.167, 0.083, 0.042] | 0.0972 |

**cascade − flat = +0.0278** (< +0.05 bar) · **n_seed_win = 1/3** (only seed 33 clears +0.05; seed 11 is −0.0417) → **PRIMARY FAIL → 🧱 WALL HOLDS.**

## THE LOAD-BEARING DIAGNOSTIC (왜 막혔나 — 정확한 메커니즘)
frozen 점에서 모든 arm 이 floor(~0.08–0.11) 로 붕괴하길래 a_break_the_wall TAXONOMY 분류를 위해 interference horizon 을 SWEEP(`H_1531_horizon_diag.txt`, **frozen bar 불변 — 진단일 뿐 verdict 아님**). 두 결정적 사실:

1. **cascade lift 는 작지만 실재하나 +0.05 를 ≥2/3 seeds 로 깨끗이 못 넘는다.** csig=0.18·cfrac=0.3 에서 cascade−flat = +0.069/+0.069/+0.069/+0.083 (K=24/48/72/120) — moderate interference 에서 양(+)이지만 frozen 작동점(cfrac=0.6)에선 K=72 에서 −0.042 로 뒤집히는 등 horizon-fragile. 어느 horizon 에서도 cascade 구조가 ≥2/3 seeds 안정적 separation 을 내지 못함.
2. **SHUFFLE 가 collapse 하지 않고 CASCADE 를 자주 TIE/BEAT 한다 — 메커니즘 INERT 의 결정적 서명.** SHUFFLE=1.000/0.986/0.833 vs CASCADE=0.972/0.958/0.778 (sweep 다수 셀). frozen 점 per-seed 도 seed 11 에서 SHUF 0.167 > CASC 0.083. **즉 "lift" 는 올바른 사실을 consolidation history 로 고른 것이 아니라 rehearsal write 횟수(추가 write 가 prototype 을 refine)의 부산물.** consolidation-by-confirmation-history 라는 cascade 의 핵심 구조가 INERT — 무작위로 고른 사실을 consolidate 해도 동등(혹은 더 나음). ablation 이 "메커니즘 기여" 방향으로 decisive 하지 않음(shuf_collapse 가 기대 방향으로 성립 안 함).

## a_break_the_wall TAXONOMY
metaplasticity/cascade 렌즈에 대한 **(d) 진짜 no-free-lunch 천장** — (a)metric-artifact 아님(horizon sweep 으로 배제: cascade 구조가 SHUFFLE 통제 대비 깨끗이 분리되는 horizon 없음), (b)confound/(c)infra 아님. per-cell consolidation timescale 은 이 interference 능력에서 INERT — **SHUFFLE 통제가 폭로**: 올바른 사실을 history 로 consolidate 하는 것이 무작위 사실 consolidate 보다 우위 없음. H_1284 벽이 이제 operating-point 가족(10 렌즈) · capacity 가족(H_1528) · ideation 가족(H_1529) · **metaplasticity/capacity-over-time 가족(이 렌즈)** 전반에 holding. census 가 예고한 hazard("scalar gain 으로 framing 하면 controller 가족 재진입") 는 회피했으나 — per-cell 구조로 구현했음에도 — 능력 자체가 history-coupling 으로 separable 하지 않음.

## NOT RULED OUT
- 더 강한 confirmation-history 신호가 살아남는 regime(초기 사실이 압도적으로 많이 rehearsed 되고 collinear clobber 가 sparse 한 곳) — 이 fixture 는 horizon 을 충분히 sweep 했으나 cascade depth dynamics 가 더 깊거나(DMAX>2) consolidation 이 prototype-refine 와 분리된 별도 채널이면 재개 가능.
- census C1(expansion-recoding)·C3(multi-store CLS)·C4(curiosity acquisition) 은 미시험 직교 가족으로 남음.

## GUARDS / SCOPE
- **하드게이트1: R1 numpy mirror → DIRECTIONAL** (engine-transfer UNVERIFIED, a_engine_native_learning). `grep -lE 'import torch|gauge_lib|numpy' state/1531_nm_cascade_meta/*.py` 가 numpy hit → auto-DIRECTIONAL, terminal NOT permitted. WALL-HOLDS ⇒ wire 할 것 없음; engine R2 = live core/engine_cli.hexa A⇄G+VAdaptField byte-exact 재측정 = 확인용 deferred ING follow-on (binding re-test GREEN-only).
- p7: exact ground truth(보존 정확도 조합 채점), NO LLM judge, NO perplexity, NO loss term — cascade 는 no-grad per-cell state update. p1/p2/p3/p6: store 가 키/값/depth 만 read, "be retentive" 라벨/RLHF/persona 주입 0.
- frozen-first, NO tune-to-green, WALL reported WALL (c9). bar 는 R1.json 생성 전 commit 으로 동결.
- SCOPE TOY: DIM=16 / 24 targets / K=120 interferers / 3 seeds / 결정적 readout (cascade STRUCTURE 검증, 학습된 consolidator 아님); scale / real-corpus / 더 깊은 cascade / engine-transfer UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).

## artifacts
- `state/1531_nm_cascade_meta/h1531_cascade_meta.py`
- `state/1531_nm_cascade_meta/h1531_horizon_diag.py`
- `state/verdicts/1531_nm_cascade_meta/H_1531_FREEZE.txt`
- `state/verdicts/1531_nm_cascade_meta/H_1531_R1.json`
- `state/verdicts/1531_nm_cascade_meta/H_1531_horizon_diag.txt`
