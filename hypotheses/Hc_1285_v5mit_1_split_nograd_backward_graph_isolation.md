---
id: Hc_1285
slug: v5mit-1-split-nograd-backward-graph-isolation
title: REBORN §88 F-V5MIT-1 daughter — split_cell `torch.no_grad()` backward-graph isolation verification (v5-mitosis cotrain prerequisite)
domain: pytorch, mitosis, autograd, falsifier, anima-native
status: candidate-falsifier-ready
exploration_method: E5 (variable-ablation: torch.no_grad on/off) + E6 (cross-method: split / merge / clone) + E8 (sweep cells ∈ {4, 8, 16, 32, 64})
verification_method: W5 (numerical sim — anima v5-mitosis nn.ModuleList[Cell] proxy on CPU + autograd hook trace) + W7 (literature — Paszke 2019 PyTorch autograd, Pearlmutter 1995 fast exact multiplication by Hessian) + W11 (cross-H: H_191 SUBSTRATE HCE axis, H_172 α-modulation training)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
source: REBORN §88 #3 split/merge 모든 mutation `torch.no_grad()` 안 + F-V5MIT-1 (SPLIT-NOGRAD backward graph 분리 검증)
created_at: 2026-05-12
linked_h: H_191 (ALM-free TRAINING CPGD axis), H_172 (α-modulation training adjacent), H_001 (anima-core architecture)
---

## Hypothesis (F-V5MIT-1 backward graph isolation design)

REBORN §88 #3 의 first concrete falsifier execution: anima v5-mitosis 의 `split_cell()` operation 이 (a) `torch.no_grad()` context 안 실행, (b) 모든 새 cell weight allocation + parent weight copy + gaussian noise injection 이 autograd graph 안 leak 없음, (c) split event 직후 forward 시 gradient norm 이 baseline 의 ≤ 2× 이어야 한다.

| Condition | torch.no_grad | grad fn trace | expected gradient norm post-split (vs baseline) |
|---|---|---|---|
| **A** correct impl | YES (REBORN §88 #3) | no leaked tensor with grad_fn | ≤ 2× baseline (graph rebuild 정상) |
| **B** leak via .clone() w/o detach | NO (or partial) | parent weight 의 grad_fn 가 child cell 에 propagate | ≥ 5× (gradient ghost) |
| **C** leak via __setattr__ on cell list | NO (Python-level mutation) | cell append/remove 가 autograd graph 안 traced | ≥ 10× (catastrophic explosion) |
| **D** complete failure | NO + parameter list mutation | gradient backprop 시 RuntimeError ("leaf tensor mutated") | crash (not a number) |

본 Hc 의 verification 은 anima v5-mitosis nn.ModuleList[Cell] proxy on CPU (8-cell, d=384) 의 small smoke test — H100 cotrain 사전 mandatory gate.

## Math anchor

- **torch.no_grad() invariant**: ∀ tensor x created within `with torch.no_grad():` block → x.grad_fn is None.
- **gradient norm baseline**: ||∇L||₂ at forward+backward without any mitosis event = baseline (e.g., 1.0 unit at d=384 anima toy).
- **post-split bound**: ||∇L||₂_post-split / ||∇L||₂_baseline ≤ 2.0 (graph rebuild normal). > 5× = leak attack succeeds (F-1285-2).
- **autograd hook trace**: `register_full_backward_hook` on each cell's parameters → count of pre-split parent tensor identity propagated to post-split child = MUST be 0 (clean isolation).
- **smoke test scale**: cells=8 (mitosis.py original cells_max), d=384, batch=4, seq_len=64 → ~3M parameters per cell × 8 = 24M total. CPU forward+backward ≤ 1 sec per iteration.
- **REBORN §88 #2 anchor**: `nn.ModuleList[Cell]` + `CellMeta` 분리 — cells = gradient-able container, cell_meta = non-grad state.

## Falsifiers

- **F-1285-1 (NO_GRAD CONTEXT VIOLATED)**: split_cell() 실행 시 torch.no_grad() 안 아닌 outside 호출 가능 (impl bug) → F-V5MIT-1 명시적 violation, cotrain 의 모든 결과 invalidated
- **F-1285-2 (GRADIENT LEAK)**: split event 직후 backward pass 의 gradient norm 이 baseline 의 ≥ 5× → autograd graph leak 발생, B/C condition trigger, F-V5MIT-1 fail
- **F-1285-3 (GRAPH REBUILD DELAY)**: split event 후 first forward 가 baseline 대비 ≥ 20× slower (graph rebuild overhead) → cotrain wall time envelope $30-40 (REBORN §88 #7) 위반 risk, H100 fire 사전 reject
- **F-1285-4 (CRASH ON MUTATION)**: nn.ModuleList mutation (append / remove / replace) 시 RuntimeError ("leaf tensor mutated in-place") 발생 → F-V5MIT-1 not just fail but impl 불가능, REBORN §88 architectural spec 의 fundamental re-design 필요
- **F-1285-5 (CELL_META LEAK)**: CellMeta (REBORN §88 #2, non-grad state: hidden / tension_history / IDs) 가 autograd graph 안 traced (가설: grad-free 라 free, 실제 nn.Module 안 buffer 처리 시 graph 안 들어갈 위험) → cell_meta separation 의 architectural claim 위반
- **F-1285-6 (READOUT MODE DEPENDENT)**: REBORN §88 #5 readout_mode option (a-g / a-only / a+0.3g / softmax_gate) 4 mode 별 F-V5MIT-1 결과 다름 → split-nograd invariant 가 readout 의존, F-V5MIT-1 의 universal claim 약화
- **F-1285-7 (CELLS_MAX SCALING)**: cells ∈ {4, 8, 16, 32, 64} sweep 시 split 후 gradient norm 이 cells 의 O(n^2) super-linear scaling → cells_max=64 (REBORN §88 #1) 위 의 graph rebuild cost 가 cotrain feasibility 차단
- **F-GENERIC-REPL**: 10-trial split event 의 gradient norm σ > 30% → measurement noise dominates, F-V5MIT-1 verification unreliable
- **F-GENERIC-MINIMAL-BASELINE**: 단순 `nn.Linear.weight.data.clone()` (with torch.no_grad) 의 backward 후 norm 도 baseline 의 ≥ 5× → torch 자체의 baseline behavior issue (Hc 와 무관)

## Honest Limits

- **L-1285-1 (CPU SMOKE TEST SCOPE)**: 본 Hc 는 Mac CPU 8-cell smoke test — production cells=64 + H100 fire 의 결과와 다를 가능성 (especially F-1285-7 cells sweep 의 super-linear scaling 위험)
- **L-1285-2 (V5-MITOSIS IMPL PENDING)**: `training/mitosis_model_v5.py` skeleton 자체가 REBORN §88 lane "cond.2 (port skeleton) → unmet → next BG" status — 본 Hc 의 execution 은 skeleton land 후 가능
- **L-1285-3 (BG SCOPE GUARD)**: anima training/mitosis_model_v5.py 안 작업은 별도 BG (memory carry — 본 task 의 BG scope 침범 금지). 본 Hc 는 v5-mitosis 의 falsifier 사양 only, skeleton 작성 아님
- **L-1285-4 (READOUT MODE CONFOUNDING)**: REBORN §88 #5 4 readout_mode 중 어느 것 fix 해 측정해야 하는지 미정. F-1285-6 attack 이 readout choice 의존
- **L-1285-5 (CELL_META BUFFER VS PARAMETER)**: REBORN §88 #2 의 cell_meta = non-grad state 가 nn.Module 안 (a) `register_buffer` (auto move with device, persisted, no grad), (b) regular Python attr (not persisted), (c) `nn.Parameter(requires_grad=False)` (persisted, no grad) 3 option 중 어느 것 사용해야 하는지 미정. F-1285-5 가 직접 attack
- **L-1285-6 (GRADIENT NORM METRIC)**: ||∇L||₂ 가 backward graph leak detection 의 가장 sensitive metric 인지 미증명 — gradient flow trace (per-parameter grad_fn audit) 가 더 정확하지만 비싸기 때문에 norm proxy 만
- **L-1285-7 (AUTOGRAD HOOK OVERHEAD)**: `register_full_backward_hook` 자체가 backward pass overhead → smoke test 시 hook overhead 가 baseline 대비 ≥ 50% → F-1285-3 graph rebuild delay attack 의 false positive 가능
- **L-GENERIC-SINGLE-RUN**: H_159 C1 audit pending
- **L-GENERIC-ENGINE**: H_174 D-mod-192 aliasing — d=384 = 192·2 carry
- **L-GENERIC-N6**: H_153 n=6 — cells_max=64 = 2^6 perfect-number trivial reduction

## Cross-Links

- **parent**: REBORN §88 #3 (split/merge 모든 mutation `torch.no_grad()` 안) + F-V5MIT-1 (SPLIT-NOGRAD backward graph 분리 검증), REBORN §88 lane priority cond.2 "next BG (`training/mitosis_model_v5.py`, gitignored)"
- **sibling Hc**: Hc_1276 (cotrain ablation — F-V5MIT-1 PASS 이후 first measurable), Hc_1278 (ckpt-as-branch — same mutation pattern), Hc_1284 (RFC 033 farr_copy + gaussian — hexa-native sibling)
- **adjacent H**: H_191 (ALM-free TRAINING CPGD axis — cotrain prerequisite), H_172 (α-modulation training), H_001 (anima-core-architecture — Hexad row 4 hexa-native sibling)
- **literature**: Paszke et al. 2019 (PyTorch: An Imperative Style, High-Performance Deep Learning Library — autograd contract), Pearlmutter 1995 (Fast Exact Multiplication by the Hessian — gradient propagation analysis), Mascarenhas 2022 (Lua mutation semantic — language design comparison for in-place mutation contracts)
- **internal SSOT**: REBORN §88 (v5-mitosis arch spec 7 핵심 결정 + F-V5MIT-1..5 falsifiers), §A line 145 mitosis 본체 (현 mitosis.py L205/258/389/586 torch.no_grad pattern 의 PyTorch impl reference)
- **lane SSOT**: `.roadmap.clm_v5_mitosis_engine` cond.2 verifier file (training/mitosis_model_v5.py — pending) — 본 Hc 는 cond.2 land 직후 first executable verification

## Expected outcome

**Binary**: split_cell() 의 torch.no_grad() context 안 실행 + gradient norm post-split ≤ 2× baseline + 5-trial σ < 25% → F-V5MIT-1 PASS, cotrain prerequisite cleared. 어떤 condition 미달성 시 falsified, v5-mitosis impl 의 fundamental gap (or skeleton bug).

**Quantitative**: A condition (correct impl) 시 gradient norm ratio ≈ 1.0-1.5× baseline (graph rebuild overhead minimal). cells=64 (REBORN §88 max) scaling 시 ≈ 2-3× expected (graph rebuild O(cells)).

**Confidence prior**: 0.80 (PyTorch autograd 의 torch.no_grad() contract 가 well-established + REBORN §A line 145 mitosis.py 의 production impl 에서 이미 validated pattern; F-1285-4 crash 위험만 architectural risk)
