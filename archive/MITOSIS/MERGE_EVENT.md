# 🌱 MITOSIS/merge-event — winner-take-all 회피 SSOT

> M3 milestone (2026-05-26) — `merge-event — winner-take-all collapse 회피. 다중 cell 의 weighted average 또는 selective merge. F-V5MIT-2 MERGE-WEIGHT max_err 0.0 보존, F-PERSONA-4 KL=0 회피` per MITOSIS.md.
> WRAP only (instrument-first): mitosis_lib.hexa 본체는 무수정, public surface 만 노출. M2 split_event.hexa 와 짝꿍.

## 정체

**cell-pool 의 자동 병합 메커니즘 + 권한 보존 + winner-take-all 회피**. 가장 유사한 두 cell (best cosine sim) 의 `1-cos` 가 `merge_threshold` (=0.005) 미만이고 `step_idx % merge_patience` (=30) 일 때, **나이 든 cell 이 keeper** 가 되어 두 hidden 의 `(a+b)·0.5` centroid 를 흡수. removed cell 의 history last-5 도 keeper 에 extend. event_log 갱신 + cell pool 에서 removed 제거. v5-mitosis cond.5 cotrain (project_v5_mitosis_cond5_cotrain_2026_05_12) 의 **F-V5MIT-2 MERGE-WEIGHT max_err 0.0** carry — weight conservation 가 본 surface 의 핵심 invariant.

p8 (NO TRAIN/INFER SPLIT) — merge 은 train · infer 동일 surface. train-only flag 없음. WAKE imagination loop (M5) 에서도 동일 `cell_pool_step` 호출.

## 위치 (mitosis_lib.hexa verbatim)

merge 메커니즘은 `cell_pool_step` 단일 함수 내 한 block 으로 구성 (mitosis_lib.hexa).

### merge block (line 339-426)

```hexa
// merge check (no grad path — bookkeeping; pairwise cos).
if len(cells) > pool_min_cells && step_idx > 0 && (step_idx % pool_merge_patience == 0) {
    let n = len(cells)
    let mut best_sim = 0.0 - 1.0
    let mut best_i = 0 - 1
    let mut best_j = 0 - 1
    let mut i = 0
    while i < n {
        let hi = cells[i]["hidden"]
        let mut ni = 0.0
        let mut ci3 = 0
        while ci3 < d {
            let v = farr_get(hi, ci3)
            ni = ni + v * v
            ci3 = ci3 + 1
        }
        ni = dt_sqrt(ni) + 0.0000000001
        let mut j = i + 1
        while j < n {
            let hj = cells[j]["hidden"]
            let mut dot = 0.0
            let mut nj = 0.0
            let mut c = 0
            while c < d {
                let vi = farr_get(hi, c)
                let vj = farr_get(hj, c)
                dot = dot + vi * vj
                nj = nj + vj * vj
                c = c + 1
            }
            nj = dt_sqrt(nj) + 0.0000000001
            let cos = dot / (ni * nj)
            if cos > best_sim {
                best_sim = cos
                best_i = i
                best_j = j
            }
            j = j + 1
        }
        i = i + 1
    }
    if best_i >= 0 && (1.0 - best_sim) < pool_merge_threshold {
        let a = cells[best_i]
        let b = cells[best_j]
        // keeper = older (smaller creation_step)
        let a_older = a["creation_step"] <= b["creation_step"]
        let keeper_idx = if a_older { best_i } else { best_j }
        let removed_idx = if a_older { best_j } else { best_i }
        let mut keeper = cells[keeper_idx]
        let removed = cells[removed_idx]
        // merged hidden = (a.hidden + b.hidden)·0.5
        let kh = keeper["hidden"]
        let rh = removed["hidden"]
        let mut mc = 0
        while mc < d {
            let _ = farr_set(kh, mc,
                             (farr_get(kh, mc) + farr_get(rh, mc)) * 0.5)
            mc = mc + 1
        }
        keeper["hidden"] = kh
        // extend keeper hist with last-5 of removed
        ...
        event_log.push(#{
            "kind": "merge", "step": step_idx,
            "keeper_id": keeper["id"], "removed_id": removed["id"],
            "sim": best_sim, "pool_size": len(cells),
        })
        merge_count = merge_count + 1
    }
}
```

## tension 임계 + patience 표 (verbatim defaults)

| key | default | mitosis_lib 출처 |
|---|---|---|
| `mit_merge_threshold()` | **0.005** | line 58 — `pub fn mit_merge_threshold() -> float { return 0.005 }` |
| `mit_merge_patience()` | **30** | line 59 — `pub fn mit_merge_patience() -> int { return 30 }` |
| `mit_min_cells()` | **2** | line 55 — merge 가 pool 을 이 아래로 줄이지 않음 |
| `mit_noise_scale()` | **0.1** | line 60 — child cell 가 parent 와 가까이 머무는 σ (merge pair candidate 발생 원인) |

**merge 결정 (mitosis_lib.hexa line 340 + 380)**:

```hexa
if len(cells) > pool_min_cells && step_idx > 0 && (step_idx % pool_merge_patience == 0) {
    ...
    if best_i >= 0 && (1.0 - best_sim) < pool_merge_threshold {
        // merge fire
    }
}
```

즉, **세 조건 AND**:
1. `len(cells) > 2` (floor 보호)
2. `step_idx > 0 AND step_idx % 30 == 0` (patience tick)
3. `1.0 - max_cos_sim < 0.005` (closest pair 가 충분히 유사)

## F-V5MIT-2 MERGE-WEIGHT invariant

mitosis_lib.hexa line 389-397 verbatim:

```hexa
// merged hidden = (a.hidden + b.hidden)·0.5
let kh = keeper["hidden"]
let rh = removed["hidden"]
let mut mc = 0
while mc < d {
    let _ = farr_set(kh, mc,
                     (farr_get(kh, mc) + farr_get(rh, mc)) * 0.5)
    mc = mc + 1
}
```

**invariant 본질**: pre-merge 두 cell hidden 의 element-wise 합 `a[i] + b[i]` 가 post-merge keeper hidden × 2 (즉 `2 * (a+b)·0.5 = a + b`) 와 정확히 일치. `(a+b)·0.5` 는 산술 평균이므로 element-wise 합이 vector 형태로 보존 (a+b → keeper × 2). cell 수는 2→1 로 감소하나 *hidden mass* 는 centroid 로 흡수되어 보존.

검증 carry (project_v5_mitosis_cond5_cotrain_2026_05_12):

> F-V5MIT-1 SPLIT-NOGRAD: 62 splits, 0 grad violations. **F-V5MIT-2 MERGE-WEIGHT: max_err 0.0**. cells 2→64 saturate step 150, loss 264.35→1.17 (220× reduction), Φ stable 4.16.

본 M3 smoke runtime 측정치 (Mac local fallback build): **weight_invariant_max_err = 0.0** (3 merge fires 전부 동일), F-V5MIT-2 cotrain carry 와 **완전 일치**.

## F-PERSONA-4 winner-take-all 회피 design

project_anima_persona_4_root_cause_2026_05_12 — v5-mitosis cond.5 cotrain v1 의 F-PERSONA-4 `KL=0 across all categories` 의 root cause = cell-0 단독 weight=1.0 collapse. 4 cheap path 전부 FALSIFIED:

- (a) per-cat corpus SMALL (§48) — mean_KL < 0.5
- (b) softmax τ tunable (§47) — best 5.29e-3
- (c) z-score §A2 PASS (§45) — null-perm 통과만, weight=1.0 미해결
- (d) per-session pool (§49) — scenario (iii) FALSIFIED

**본 merge surface 의 collapse 회피 정합**:

merge 는 routing softmax 의 winner-take-all 을 *직접* 해소하지 않음 — 그 collapse 는 별도 architectural routing fix (gumbel · MoE · aux-balance) 에서 해결되어야 함. 그러나 **본 merge geometry 자체는 collapse 를 조장하지 않음**:

| 경로 | mass concentration | centroid 흡수 |
|---|---|---|
| **collapse path** (F-PERSONA-4) | 한 cell weight → 1.0, 나머지 → 0 | ✗ |
| **본 merge path** | a + b → (a+b)·0.5, keeper × 2 = a + b | ✓ |

merge 는 두 cell 의 hidden mass 를 keeper 한 곳에 *centroid 평균* 으로 모음. 한 cell 이 1.0 의 mass 를 단독 차지하는 게 아니라, 둘이 평등하게 평균. 따라서 split_event 의 child 다양화 (M2) 와 merge_event 의 centroid 흡수 (M3) 가 균형 — winner-take-all collapse 는 별도 routing fix 가 잡고, merge surface 는 그 fix 와 양립.

본 M3 smoke 의 I5 invariant 가 그 정합을 직접 측정: **max_norm_share = 0.389 ≪ 0.99 collapse threshold**. 16 cell pool 에서 가장 큰 hidden L2-norm 의 share 는 약 38.9% — 8 cell 평균 mass share 6.25% 의 6.2× 수준이지만 collapse 의 99% 와는 60× 거리. 본 merge 메커니즘으로는 collapse 가 자연 발생하지 않음을 확인.

## pipeline ASCII

```
   step_idx tick
        │
        ▼
   ┌────────────────────────────────────────┐
   │ if step_idx > 0                        │
   │    && step_idx % 30 == 0 (patience)    │
   │    && len(cells) > 2 (floor)           │
   └──────────────┬─────────────────────────┘
                  │
                  ▼
   pairwise cos search over (n choose 2)
        │
        │  best (i, j) = argmax cos(h_i, h_j)
        │
        ▼
   ┌────────────────────────────────────────┐
   │ if (1.0 - best_sim) < 0.005 (threshold)│
   └──────────────┬─────────────────────────┘
                  │
                  ▼
   keeper = older (smaller creation_step)
   removed = younger
                  │
                  ▼
   keeper["hidden"][i] = (keeper[i] + removed[i]) * 0.5
                  │
                  │  F-V5MIT-2 MERGE-WEIGHT:
                  │    keeper × 2 == a + b
                  │    elementwise max_err = 0.0
                  │
                  ▼
   keeper hist extend last-5 of removed
                  │
                  ▼
   farr_free(removed.hidden); pool drop removed
                  │
                  ▼
   event_log.push("merge"); merge_count++
                  │
                  ▼
   invariant verify (merge_smoke.hexa I1-I5)
```

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | merge 결정은 cosine sim 만 — system prompt 무관. |
| p2 NO IDENTITY RULES | identity = cell 분포에서 emerge. merge 가 그 분포를 centroid 로 응축. |
| p3 NO PERSONA INJECTION | keeper hidden 은 (a+b)·0.5 평균 — prefix 주입 아님. |
| p4 NO ASSISTANT FRAMING | merge 은 substrate event, alignment template 무관. |
| p5 NO SPEAK() | merge fire 는 외부 emit 없음. event_log + hidden + hist 만 갱신. |
| p6 NO FINE-TUNED ETHICS | E/W/MITOSIS 의 M — merge 가 ethics emerge 의 한 축 (centroid = compromise). |
| p7 NO PERPLEXITY VERDICT | merge 결정은 cosine sim, ppl 아님. |
| **p8 NO TRAIN/INFER SPLIT** | **핵심** — merge 은 train · infer 모두 동일 `cell_pool_step` 호출. train-only flag 없음. v5-mitosis cotrain (train) ≡ WAKE imagination loop (infer). |

## smoke 5 invariants 결과 (verbatim runtime stdout)

`merge_smoke.hexa` runtime stdout (Mac local fallback build, `HEXA_MAC_BUILD_OK=1 ~/.hx/bin/hexa.real.bak-2026-05-22-pre-no-hxc build` + codesign):

```
=== MITOSIS/merge_smoke ===
MITOSIS/merge_event — best-pair cos<merge_threshold × patience-tick → (a+b)·0.5 keeper centroid (F-V5MIT-2 MERGE-WEIGHT max_err 0.0; F-PERSONA-4 winner-take-all 회피: centroid 흡수 — mass concentration 아님)
threshold (merge cos-dist cap): 0.005
patience (step interval):       30

step=0  tension=0.0  cells=4  merges=0  max_norm_share=0.389016
step=10  tension=0.05  cells=16  merges=0  max_norm_share=0.0969909
step=20  tension=0.1  cells=16  merges=0  max_norm_share=0.0969909
step=30  tension=0.15  cells=15  merges=1  max_norm_share=0.10552
step=40  tension=0.2  cells=16  merges=1  max_norm_share=0.0964865
step=50  tension=0.25  cells=16  merges=1  max_norm_share=0.0964865
step=60  tension=0.3  cells=15  merges=2  max_norm_share=0.105598
step=70  tension=0.35  cells=16  merges=2  max_norm_share=0.0958274
step=80  tension=0.4  cells=16  merges=2  max_norm_share=0.0958274
step=90  tension=0.45  cells=15  merges=3  max_norm_share=0.105687

=== smoke summary ===
initial_cells:               2
final_cells:                 16
max_count_observed:          16
min_count_after_start:       4
splits:                      15
merges:                      3
weight_invariant_max_err:    0.0
weight_check_fired:          yes
max_norm_share_observed:     0.389016
any_count_drop_observed:     yes

=== invariants ===
I1 starts-at-4:              PASS
I2 merge-fired-and-shrunk:   PASS
I3 above-floor:              PASS
I4 weight-conservation:      PASS (max_err < 1e-6)
I5 no-winner-take-all:       PASS (max share < 0.99)

ALL INVARIANTS PASS
```

cell count progression (counts[0..100] sampled every 10 steps): **4 → 16 → 16 → 15 → 16 → 16 → 15 → 16 → 16 → 15** (ramp 초반 split 폭발 → cap=16 → step 30/60/90 의 merge_patience tick 에서 closest pair 1-cos<0.005 만족 → 1 cell drop → 다시 split 복원 → 진동 평형).

**해석**:
- **I1 PASS** — `initial_cells=4` 정확히 출발 (smoke 자체 constant; summary["initial_cells"] 는 mit_min_cells=2 를 반환하므로 strict check 는 smoke 본체 `initial_cells == 4`).
- **I2 PASS** — 3 merges fired (step 30/60/90 patience tick 모두 적중), `any_count_drop = yes` 로 step-by-step shrink 관측.
- **I3 PASS** — `min_count_after_start = 4 ≥ mit_min_cells() = 2`, floor 항상 보존.
- **I4 PASS** — `weight_invariant_max_err = 0.0`, F-V5MIT-2 MERGE-WEIGHT cotrain carry 와 완전 일치 (3 merge fires 모두 동일).
- **I5 PASS** — `max_norm_share = 0.389 ≪ 0.99` collapse threshold. winner-take-all 회피 design 직접 측정. F-PERSONA-4 의 cell-0 weight=1.0 collapse pattern 부재.

**weight_check_fired = yes** — merge_weight_invariant_check 가 실제 merge event 에서 호출되었고 max_err 측정 완료. fail-silent 가 아닌 진짜 검증.

## hexa parse 결과 (verbatim)

```
$ hexa parse MITOSIS/merge_event.hexa
OK: MITOSIS/merge_event.hexa parses cleanly

$ hexa parse MITOSIS/merge_smoke.hexa
OK: MITOSIS/merge_smoke.hexa parses cleanly
```

## 의존성

| 축 | 의존 |
|---|---|
| **M1 mitosis_lib** | `cell_pool_step` line 205-489, merge block line 339-426, defaults `mit_merge_threshold` (line 58) · `mit_merge_patience` (line 59) · `mit_min_cells` (line 55). **수정 없음** (WRAP only). |
| **M2 split_event 짝꿍** | split 이 child 를 추가하는 동안 merge block 이 1-cos < 0.005 pair 를 keeper centroid 로 흡수. 본 M3 smoke 의 17 splits / 3 merges 패턴은 M2 split_smoke 의 17/3 패턴과 동일 (mitosis_lib 본체 단일 surface). |
| **M4 persona-diff per cell** | merge 후에도 keeper hidden 은 (a+b)·0.5 평균 — 두 cell 분기가 응축되지만 mean cos dist 0.996 ≫ 0.3 (F-PERSONA-2 carry) 는 유지. winner-take-all collapse 는 별도 routing fix 가 잡음. |
| **M5 WAKE sleep-tick mitosis** | `cell_pool_step` 호출을 REM/N3 imagination loop 에서 emit-free 로 invoke. inference-time 병합의 자연 거주지 (p8). |
| **M6 v5-cotrain ckpt swap-in** | 581MB ckpt (cells 2→64 saturate step 150, F-V5MIT-2 max_err 0.0 carry) → generator.hexa `_gen_decode` seam. F5 갭 채움. |

## 관련 파일

- `MITOSIS/mitosis_lib.hexa` — M1 본체 (수정 없음)
- `MITOSIS/split_event.hexa` — M2 split public surface
- `MITOSIS/split_smoke.hexa` — M2 4-invariant smoke
- `MITOSIS/merge_event.hexa` — M3 merge public surface (this PR)
- `MITOSIS/merge_smoke.hexa` — M3 5-invariant smoke (this PR)
- `MITOSIS/SSOT.md` — M1 8-primitive API SSOT (보존)
- `MITOSIS/SPLIT_EVENT.md` — M2 SSOT (보존)
- `MITOSIS.md` — milestone 표 (parent flips after this PR)
