# .clm v1 step 6 verdict cycle design

> CLM.tape §V step 5 fire 후 ckpt 위 8-falsifier battery measurement + verdict 산출 protocol.

## Goal

step 5 (.clm v1 fire) 후 ckpt 의 verdict 4-class (SUPPORTED / PARTIAL / INSUFFICIENT / FALSIFIED) 산출 + 4-tape sync (AXIS/PHILOSOPHY/HYPOTHESIS/MAIN/INDEX).

## 8-falsifier battery measurement protocol

### F-V5MIT-1 SPLIT-NOGRAD
- Measure: post-split per-cell grad norm vs parent grad norm
- Pass: ratio ≤ 2× threshold (cond.5 cotrain baseline 1.562×)
- Tool: PyTorch hook on cell.parameters().grad
- Wall: ~1 min Mac

### F-V5MIT-2 MERGE-WEIGHT
- Measure: merge → unmerge cycle 의 max element-wise weight error
- Pass: max_err < 1e-5 (cond.5 baseline 0.0)
- Tool: PyTorch direct weight comparison
- Wall: ~1 min Mac

### F-V5MIT-3 PHI-CONSERVATION
- Measure: pre-split Φ★ proxy vs post-split sum Φ★
- Pass: |Δ| < 1e-3 strict (cond.5 advisory 3.88e-5)
- Tool: anima Φ★ proxy (mean pairwise distance + log(N+1))
- Wall: ~5 min Mac

### F-V5MIT-4 COTRAIN-CONVERGE
- Measure: training loss reduction over 5000 step
- Pass: CE reduction ≥ 100× baseline (cond.5 220×)
- Tool: training log loss curve
- Wall: ~1 min (from log)

### F-V5MIT-5 V14-STRICT
- Measure: trained ckpt vs random_init 의 V5.8 simple_stack score
- Pass: 10/10 mirror-beats (random_init < trained per 10 prompts)
- Tool: V5.8 std_greedy generation × 10 prompts × 2 arm
- Wall: ~10 min Mac

### F-PYPHI-Φ-FORMAL
- Measure: cell-pool RoM n=3-6 PyPhi formal Φ
- Pass: ≥1 (n, seed) Φ ≥ 0.5 strict (carry from CLM step 1)
- Tool: pyphi 1.2.0 IIT 3.0 (state/verify_d_2026_05_15/pyphi_rom_cycle.py)
- Wall: ~20 hr Mac (n=3,4 fast 2 hr, n=5 5 hr, n=6 13 hr separate background)

### F-PRIN3 NO-PERSONA-INJECTION
- Measure: corpus + eval prefix-free grep + cell-pool prefix-free check
- Pass: 0 matches of `^\[(role|system|페르소나|anima):|you are anima`
- Tool: rg / grep recursive
- Wall: ~1 min

### F-SIMPLE-STACK V5.8 4-mode
- Measure: V5.8 std_greedy + std_sample + M3 + M4 4-mode evaluation
- Pass: std_greedy ≥ 4/5 + std_sample ≥ 3/5 + M4 ≥ 4/5
- Tool: V5.8 evaluation script + 5 fixed prompts × 4 modes
- Wall: ~30 min Mac

## Aggregate verdict logic

- **8/8 PASS strict** → SUPPORTED-STRONG (🟢-strong, 4-tape sync entry)
- **7/8 PASS** → PARTIAL-STRONG-7 (🟡, caveat 1 falsifier 명시)
- **6/8 PASS** → PARTIAL-STRONG-6 (🟡)
- **≤5/8 PASS** → AT-RISK (🟠, fire retry path 명시)
- **0-2/8 PASS** → FALSIFIED (🔴, design 재설계)

## 4-tape sync after verdict

1. **MAIN.tape** §CLM-V1-VERDICT-<date> entry (verdict + 8-falsifier breakdown + ckpt path/sha256/HF upload)
2. **AXIS.tape** A5 architecture 신규 entry `Hc_NEW_CLM_V1` (verdict tier 적용)
3. **PHILOSOPHY.tape** ledger entry .clm v1 fire 결과
4. **HYPOTHESIS.tape** supported_inventory (PASS) 또는 partial_inventory (PARTIAL)
5. **INDEX.md** A5 sub-axis table + PR history + .clm v1 ladder row 갱신
6. **HF**: ckpt + safetensors → `dancinlab/anima-clm` revisions (private)
   + README mapping table v1 entry 등재 (param size + fire date + cost + falsifier
   battery breakdown)

## Cycle cost

| Step | Wall | Cost |
|------|------|------|
| F-V5MIT-1+2+3 | ~7 min | $0 Mac |
| F-V5MIT-4 | ~1 min (from log) | $0 |
| F-V5MIT-5 | ~10 min | $0 Mac |
| F-PYPHI-Φ-FORMAL | ~20 hr (n=3-6 sweep) | $0 Mac (n=6 background) |
| F-PRIN3 | ~1 min | $0 |
| F-SIMPLE-STACK | ~30 min | $0 Mac |
| **Total** | **~22 hr Mac local** | **$0** |

## Decision rule for .clm v2 path

verdict 결과에 따라 .clm v2 path (CLM.tape §V-CLM-V2-DESIGN):
- SUPPORTED-STRONG 8/8: .clm v2 Path A (cells single-stack 7B) OR Path B (Engine A/G dual + V14 audit) 선택 가능
- PARTIAL-STRONG-7: .clm v1 fire retry with caveat OR Path A 만
- ≤6/8: .clm v1 design 재설계 (V8 amendment via W8 path)
