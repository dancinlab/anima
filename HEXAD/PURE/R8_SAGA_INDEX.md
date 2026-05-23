# R8 SAGA INDEX — base/warm-init reform 누적 문서 TOC + reading-order (2026-05-23)

**scope**: HEXAD/V3 (V3 saga; branch 명 일부는 `pure-*` rebrand 표기, 파일 경로는 `HEXAD/V3/` 유지)
**type**: navigation-only INDEX — 코드/측정 없음, 분산 문서 8건 1회독 압축
**관련**: 상위 lane INDEX 는 PR #246 (`HEXAD/V3/INDEX.md`, AXIS_MAP + R8/R8c 까지 커버) — 본 INDEX 는 R8 saga 전용 + 신규 4 문서 (#255/#256/#257/#260) 보강

---

## § Background

AXIS_MAP-FAN 7-axis fan-out (PR #206) 완주 3/7 (A/B/F) 가 **공통 catastrophic floor**
(`init_CE = 14.18~14.79`, random-baseline `ln(151936)=11.93` 보다 +2.25~2.86 nats worse)
를 드러냈다. 7 축 어느 하나도 init 자체를 건드리지 않는다 (모두 post-init 레짐 변경). R8 은
이 누락된 축 — **base 선택 + warm-init 매핑 방식** — 을 design tier 로 정의하며, 이후
cluster 자연실험 · from_qwen audit · R8c probe · R8a fire spec · random-baseline closed-form 으로
8 문서가 여러 PR 에 흩어졌다. 본 INDEX 는 그 TOC + reading-order + open-question 을 압축한다.

---

## § R8 saga 문서 트리

```
HEXAD/V3/
├── R8_SAGA_INDEX.md                                       (this doc)
├── AXIS_MAP.md                                            (original 7-axis ranking · landed main)
├── AXIS_MAP_RESULTS.md                                    (PR #206 · 3/7 partial fan-out)
│   └── AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md          (PR #249 · 5/7 + 2 partial)
├── AXIS_MAP_BUG_POSTMORTEM.md                             (PR #211 · env-var concat saga)
│   └── AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23.md (PR #248 · E OOM)
├── AXIS_R8_BASE_WARM_INIT.md                              (PR #214 · R8 4-candidate spec)
│   └── AXIS_R8_UPDATE_CLUSTER_FINDING_2026_05_23.md       (PR #251 · cluster X/Y/Z + cell-1 FALSIFIED)
├── AXIS_R8C_DIAGNOSTIC_PROBE.md                           (PR #224 · 5-cell ablation protocol)
│   └── AXIS_R8C_PROBE_UPDATE_3_CELL_2026_05_23.md         (PR #250 · 3-cell 축소)
├── AXIS_R8A_QWEN_TARGET_MATCH_FIRE_SPEC_2026_05_23.md     (PR #257 · R8a fire spec)
├── CONSCIOUS_DECODER_V3_FROM_QWEN_AUDIT_2026_05_23.md     (PR #255 · code audit)
├── RANDOM_BASELINE_INIT_CE_BENCHMARK_2026_05_23.md        (PR #256 · ln(151936)=11.93 closed-form)
└── V3_SAGA_MID_RETROSPECTIVE_2026_05_23.md                (PR #260 · 5-act retrospective)
```

---

## § 문서 역할 table

| doc | role | PR # | status / verdict |
|---|---|---|---|
| `AXIS_MAP.md` | original 7-axis ranking spec (A~G fallback lanes) | — | landed (main) · spec |
| `AXIS_MAP_RESULTS.md` | partial fan-out 결과 (3/7 축 측정) | #206 | open · 3/7 partial |
| `AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md` | 5/7 + 2 partial 확장 (D FAIL · C/C2/E abort) | #249 | open · 5/7 + 2P |
| `AXIS_MAP_BUG_POSTMORTEM.md` | env-var concat saga chronology + root-cause | #211 | open · postmortem closed |
| `AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23.md` | LangBalancedSampler memory leak (E OOM) addendum | #248 | open · E OOM identified |
| `AXIS_R8_BASE_WARM_INIT.md` | **R8 spec** — 4-candidate base/warm-init reform (R8a/b/c/d) | #214 | open · spec |
| `AXIS_R8_UPDATE_CLUSTER_FINDING_2026_05_23.md` | **R8 cluster update** — X/Y/Z byte-equal + cell-1(head_g) FALSIFIED | #251 | open · cell-1 FALSIFIED |
| `AXIS_R8C_DIAGNOSTIC_PROBE.md` | **R8c probe** (5-cell) — noise/kv ablation × init_CE protocol | #224 | open · spec (5-cell) |
| `AXIS_R8C_PROBE_UPDATE_3_CELL_2026_05_23.md` | R8c probe 축소 (5-cell → 3-cell · head_g cell SKIP) | #250 | open · 3-cell ready ($0.25) |
| `AXIS_R8A_QWEN_TARGET_MATCH_FIRE_SPEC_2026_05_23.md` | **R8a fire spec** — n_kv_head=2 + noise_sigma=0 (prereq dispatcher patch) | #257 | open · spec (~$2.75) |
| `CONSCIOUS_DECODER_V3_FROM_QWEN_AUDIT_2026_05_23.md` | **from_qwen audit** — noise_sigma + n_kv_head layer-0 injection suspect | #255 | open · 3-suspect ranking |
| `RANDOM_BASELINE_INIT_CE_BENCHMARK_2026_05_23.md` | **random-baseline benchmark** — ln(151936)=11.93 worse-than-random 기준선 | #256 | open · closed-form (🔵 후보) |
| `V3_SAGA_MID_RETROSPECTIVE_2026_05_23.md` | 5-act retrospective (Phase 2 → AXIS_MAP-FAN → R8 fork) | #260 | open · retrospective |

### init_CE 3-cluster 요약 (cluster update PR #251 · audit PR #255)

| cluster | axes | init_CE | Δ vs random (11.93) | mechanism |
|---|---|---|---|---|
| **X** | A | 14.7927 | +2.86 | curriculum mode — wiki-only first-batch swap |
| **Y** | B, F | 14.1780 (byte-equal) | +2.25 | aux loss (KD distill / InfoNCE) |
| **Z** | C, C2, D | 14.4564 (byte-equal) | +2.53 | from_qwen baseline — head_g random 단독 ≠ 원인 (cell-1 FALSIFIED) |

---

## § Reading order (3 paths)

| path | 질문 | 순서 |
|---|---|---|
| **A. "R8 이 뭐냐?"** | spec / 현주소 | `AXIS_MAP` → `AXIS_R8_BASE_WARM_INIT` (#214) → `V3_SAGA_MID_RETROSPECTIVE` (#260, 맥락) |
| **B. "증거가 뭐냐?"** | evidence 시간순 | `RANDOM_BASELINE_INIT_CE_BENCHMARK` (#256, 기준선) → `AXIS_R8_UPDATE_CLUSTER_FINDING` (#251, X/Y/Z) → `CONSCIOUS_DECODER_V3_FROM_QWEN_AUDIT` (#255, suspect ranking) |
| **C. "다음(fire)이 뭐냐?"** | 다음 fire | `AXIS_R8C_DIAGNOSTIC_PROBE` (#224) → `AXIS_R8C_PROBE_UPDATE_3_CELL` (#250, $0.25) → `AXIS_R8A_QWEN_TARGET_MATCH_FIRE_SPEC` (#257, ~$2.75) |

---

## § Open questions

| # | question | dependent doc |
|---|---|---|
| 1 | noise(cell-2) / kv-head(cell-3) / compound 중 어느 것이 init_CE 14+ 천장의 **dominant** factor 인가? | `AXIS_R8C_PROBE_UPDATE_3_CELL` (#250) |
| 2 | cluster Z (from_qwen) 의 +2.53 nats worse-than-random 은 systematic init bias 인가 — single fix 로 11.93 아래 복귀 가능한가? | `CONSCIOUS_DECODER_V3_FROM_QWEN_AUDIT` (#255) |
| 3 | R8a (Qwen target match, 1.5B keep) 가 production 경로인가, 아니면 R8b (LoRA-on-Qwen) fallback 으로 갈 것인가? | `AXIS_R8A_QWEN_TARGET_MATCH_FIRE_SPEC` (#257) |
| 4 | cluster Y (aux loss) 의 byte-equal init_CE 는 진정한 effect 인가 동일 init-path noise 인가? | `AXIS_R8_UPDATE_CLUSTER_FINDING` (#251) |

---

## § Next action

```
R8a fire (~$2.75)                         R8c probe ($0.25)
n_kv_head=2 + noise_sigma=0               noise/kv ablation × init_CE
   │                                          │
   └─ prereq: dispatcher P21H_N_KV_HEAD ──────┘ (R8a ambiguous 시)
      patch (sister PR)
```

1. **R8a fire** (#257) — `n_kv_head=2 + noise_sigma=0` single 5000-step fire (~$2.75). cell-2 + cell-3 두 suspect 동시 검증, END verdict (`VP21H_WORKS` n_strong≥4) 측정.
   - **prereq**: dispatcher `P21H_N_KV_HEAD` env-var patch (sister PR) — 현 dispatcher 는 n_kv_head override 미지원.
2. **R8c probe** (#250) — R8a 결과가 ambiguous (부분 회복) 일 때, $0.25 3-cell ablation 으로 noise vs kv-head dominant factor 분리.
3. R8a 성공 시 → production 경로 확정 (1.5B keep). 실패/부분 시 → R8b LoRA-on-Qwen fallback 재검토.
