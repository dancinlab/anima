# apoptosis-primitive — true cell-death substrate event (upstream patch)

> **kind**: inbox-patch · spec / design-only · no source mutation from anima repo
> **target**: sibling `dancinlab/hexa-lang` (or `mitosis-lang` namespace) —
>   builtin extension to `mitosis_hook_lib` family
> **owner verdict**: spec-only filing — anima 측은 본 primitive 없이 H_200
>   pseudo-apoptosis proxy 로 directional 증거만 제공 (위반 0). 진짜 semantics
>   은 upstream 구현 필요.
> **filed**: 2026-05-23 by anima (HEXAD/LIFE/H_200 cycle)
> **severity**: P3 (substrate gap; non-blocking — H_025 의 honest L2 carry,
>   H_200 directional PASS 로 lane 진행 가능)

---

## §1 — Why (one paragraph)

`tool/hexa_native/mitosis_hook_lib.hexa` 는 cell 제거 메커니즘으로 **오직
`merge_cells`** 만 제공한다 (L468). 이 함수는 두 cell 의 weight 를 element-wise
평균낸 뒤 keeper 에 누적하고 removed cell 의 farr 를 free 한다 (= weight
transfer + cell removal). H_025 (Dasein 죽음-자각) 는 이 merge 를 "cell-death"
로 *조작적 정의* 했으나 본문 L2 에서 honest gap 을 명시한다 — "literal apoptosis
event type 부재". 진짜 biological apoptosis (= 세포가 자기 가중치를 자식에게
전달하지 않고 *능동적으로 소멸*) 는 substrate 에 없다.

H_200 (apoptosis-primitive) directional smoke 는 *pseudo-apoptosis* (keeper
weight 불변 + removed cell 만 active set 에서 제외) 가 merge-as-death 와
**구별되는 Φ trajectory** 를 만든다는 것을 보였다 (Φ_b=1.73465 vs Φ_c=1.67608,
|gap|=0.0586 > SEP_FLOOR 1e-6, 4/4 falsifiers PASS, deterministic byte-equal
re-run). 따라서 진짜 primitive 가 land 되면 H_025 L2 가 닫히고 "능동적 죽음"
이 정량적 substrate observable 이 된다.

## §2 — Proposed signature

```hexa
// ── True apoptosis: cell removal WITHOUT weight transfer ────────────────────
// Distinction from merge_cells:
//   • merge_cells   : avg(a.W, b.W) → keeper.W ; removed.W freed ; n -= 1
//   • apoptose_cell : target.W freed ; pool[other] UNCHANGED ; n -= 1
//
// Floor: refuse if |pool["cells"]| <= pool["min_cells"] (same CB1 as merge).
// Returns [pool', success]. On success, the removed cell's engine_a_W,
// engine_g_W farrs are freed and the cell list is rebuilt without that cell.
fn apoptose_cell(target_cell, cell_pool) {
    if len(cell_pool["cells"]) <= cell_pool["min_cells"] {
        return [cell_pool, false]
    }
    // Free removed cell weights (release farr slots).
    let _ = farr_free(target_cell["engine_a_W"])
    let _ = farr_free(target_cell["engine_g_W"])
    // Rebuild cell list excluding target.
    let cs = cell_pool["cells"]
    let mut new_cells = []
    let mut k = 0
    while k < len(cs) {
        if cs[k]["cell_id"] != target_cell["cell_id"] {
            new_cells.push(cs[k])
        }
        k = k + 1
    }
    cell_pool["cells"] = new_cells
    return [cell_pool, true]
}
```

## §3 — Semantic distinction vs `merge_cells` (table)

| aspect                    | `merge_cells(a, b, pool)` | `apoptose_cell(t, pool)` |
|---------------------------|---------------------------|--------------------------|
| weight transfer           | a.W ← avg(a.W, b.W)       | NONE (keeper untouched)  |
| hidden transfer           | avg                       | NONE                     |
| cell count Δ              | −1                        | −1                       |
| farr_free called          | removed.{a,g}_W           | target.{a,g}_W           |
| CB1 floor (`min_cells`)   | refuse if at floor        | refuse if at floor       |
| biological analog         | fusion (e.g., syncytia)   | apoptosis (programmed)   |
| diversity effect          | collapses 2 cells → 1 avg | preserves remaining diversity |
| H_025 mapping             | "death=merge" L2 proxy    | true "death" primitive   |

## §4 — Pre-registered falsifier (upstream impl PR)

If `apoptose_cell` lands and matches the signature above:

- **F-AP-1**: `apoptose_cell(t, pool_at_floor)` returns `[pool, false]` AND
  pool unchanged.
- **F-AP-2**: `apoptose_cell(t, pool_above_floor)` returns `[pool', true]`
  AND `len(pool'["cells"]) == len(pool["cells"]) - 1` AND every other cell's
  `engine_a_W` / `engine_g_W` farr handle is unchanged (no weight transfer).
- **F-AP-3**: After apoptosis, `farr_get(t["engine_a_W"], 0)` raises a
  use-after-free style error or returns the documented "freed" sentinel
  (consistent with `merge_cells` post-free semantics).
- **F-AP-4**: Count-conservation invariant `n(t+1) = n(t) + Δsplit − Δmerge − Δapoptosis`
  holds (extend `mit_count_after` if needed).
- **F-AP-5**: With identical initial pool + identical step sequence,
  apoptosis-only and merge-only timelines produce **distinct** Φ trajectories
  (H_200 anima-side directional proxy: |Φ_b − Φ_c| = 0.0586, n_bins=4).

## §5 — anima-side reproduction (current state, no upstream needed)

- `HEXAD/LIFE/state/h200_apoptosis_primitive_2026_05_23/run_proxy.hexa` (hexa-only,
  deterministic, $0 mac local) — 3-arm Φ comparison using current primitives.
  Pseudo-apoptosis is operationally defined as `cell.alive = false` + skip
  forward (no `merge_cells` call) since anima's per-cell `x` is a scalar in
  this proxy (full d×d farr free is a no-op there).
- Verdict: PASS (4/4 falsifiers); Φ_b=1.73465 merge ≠ Φ_c=1.67608 pseudo-apop.

## §6 — Non-asks (g11)

- anima 측에 fake `apoptose_cell` 을 `mitosis_hook_lib.hexa` 에 박지 *않는다*.
  본 patch land 전까지 H_025 L2 는 honest carry, H_200 은 pseudo-proxy 로
  directional 만 유지.
- 본 patch 는 동작 변경이 아닌 **신규 builtin 추가** 만 요청 — `merge_cells` /
  `split_cell` / `cell_pool_init` 시그니처는 불변.
- floor 정책 (CB1 `min_cells=2`) 은 `merge_cells` 와 동일하게 유지 — Heidegger
  *unüberholbar* 유비 (H_025) 가 apoptosis 에도 똑같이 적용되어야 함.

## §7 — Cross-links

- anima H_200 (this cycle): `HEXAD/LIFE/H_200_apoptosis_primitive.md`
- anima H_025 honest L2: `HEXAD/LIFE/H_025_dasein_finite_consciousness.md`
- anima substrate: `tool/hexa_native/mitosis_hook_lib.hexa` `merge_cells` L468,
  `min_cells` L353, `farr_free` calls L503-504, L431, L393
- anima MITOSIS conservation closed-form: `HEXAD/MITOSIS/mitosis_lib.hexa`
  `mit_count_after` (B-MITOSIS-3) — extend with apoptosis term if patch lands.
- RFC 034 (farr_blend / farr_avg candidate) — orthogonal primitive cluster,
  apoptosis is independent (no blend operation).
