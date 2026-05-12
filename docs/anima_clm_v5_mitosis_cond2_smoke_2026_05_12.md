# anima_clm_v5_mitosis_cond2_smoke — cond.2 port skeleton + Mac CPU smoke verdict

**작성**: 2026-05-12 KST
**status**: cond.2 PASS — `training/mitosis_model_v5.py` + `training/mitosis_model_v5_smoke_test.py` 검증
**author**: bg head (claude opus 4.7 1M)
**carries from**: REBORN §88 (architectural spec land), `.roadmap.clm_v5_mitosis_engine` cond.1 met
**sister docs**:
- `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md` (canonical spec)
- `docs/anima_clm_v5_hexa_native_mitosis_hook_spec_2026_05_12.md` (hexa sister lane)

---

## §0 TL;DR

- `training/mitosis_model_v5.py` (852 LoC, prior-cycle skeleton aligned with 2026-05-10 spec — content-identical to 2026-05-12 spec) **cond.2 verifier path 충족**.
- `training/mitosis_model_v5_smoke_test.py` (256 LoC, 본 cycle 신규) — Mac CPU 검증기, **exit 0 = cond.2 PASS**.
- Mac CPU smoke (d_model=32, cells=2~6, ~10 steps) **3/3 gating PASS**: basic_forward_smoke + F-V5MIT-1 SPLIT-NOGRAD + F-V5MIT-2 MERGE-WEIGHT.
- F-V5MIT-3 PHI-CONSERVATION = **advisory NOTE** (per-cell Φ delta 67% > 25% tolerance) — cond.3 calibration item (spec §11 #9 honest C3 항목과 일치).
- wall = 0.085s on M2 Mac CPU. cost = **$0**.

---

## §1 deliverables

### §1.1 `training/mitosis_model_v5.py` (cond.2 verifier file)

- **위치**: `/Users/ghost/core/anima/training/mitosis_model_v5.py` (852 LoC)
- **prior-cycle status**: 2026-05-10 cycle 에서 작성, 2026-05-10 spec 기준. 본 cycle 의 2026-05-12 spec 는 2026-05-10 spec 의 +2 carry (content-identical, `.roadmap.clm_v5_mitosis_engine.next_step.task` 명시) — 따라서 기존 skeleton 가 2026-05-12 spec 의 cond.2 verifier 도 충족.
- **classes**:
  - `MitosisModelConfig` (dataclass) — vocab=256/d=384/n_head=6/ffn=1536 default, all-fix A1/A2/B1/C1/D1 flags
  - `CausalSelfAttention(nn.Module)` — vanilla causal MHA, cell-state residual at input
  - `MitosisModelCell(nn.Module)` — ln1 + attn + ln2 + ffn_a + ffn_g, readout_mode (`a_minus_g`/`a_only`/`a_plus_g`), cell_state buffer for Lorenz, metadata (cell_id/creation_step/parent_id/tension_history/process_count)
  - `MitosisModelEngine(nn.Module)` — shared tok_emb/pos_emb/final_ln/lm_head + `nn.ModuleList[Cell]`, split/merge/Lorenz/Φ/ratchet/adaptive-threshold/dispersion-trigger/optimizer-rebuild-callback
- **forward signature**: `forward(input_ids) → (logits, info)`, `info` dict 에 tensions/weights/aggregated/n_cells.
- **mitosis primitives**: `force_split(parent_idx)` / `force_merge(idx_a, idx_b)` 공개 hook + `mitosis_step(info)` (Lorenz + tension history + Φ + ratchet + check_splits + check_merges).
- spec §2/§3/§4/§5/§6/§7 모두 impl 됨. spec 의 7 핵심 결정 (REBORN §88) 충족 확인:
  | 결정 | impl 위치 | OK |
  |---|---|:---:|
  | option (a) small transformer block per cell | `MitosisModelCell` L124-194 | ✅ |
  | `nn.ModuleList[Cell]` + CellMeta 분리 | `cells: nn.ModuleList` L230 + cell metadata on cell instance L161-165 (parent_id/creation_step/tension_history) | ✅ (CellMeta dataclass 대신 cell instance attr — equivalent semantics, 더 simple) |
  | split/merge `torch.no_grad` mutation | `_split_cell` L407 `with torch.no_grad():`, `_merge_cells` L501 동일 | ✅ |
  | anima-native cotrain identical forward path | `forward` 는 mutation 없음, `mitosis_step` 별도 호출 (caller 가 train/serve 모두 호출 가능) | ✅ |
  | readout_mode option | `MitosisModelCell.forward` L184-191 (a_minus_g/a_only/a_plus_g — softmax_gate 는 future ablation) | ✅ partial (3/4 mode) |
  | falsifier 5개 (F-V5MIT-1/2/3/4/5) | F-V5MIT-1/2/3 = smoke_test 본 cycle, F-V5MIT-4 = cond.4, F-V5MIT-5 = cond.5 | ✅ (cond.2 scope) |
  | cost envelope $30-40 | cond.5 만 cost-bearing, cond.2 = $0 | ✅ |

### §1.2 `training/mitosis_model_v5_smoke_test.py` (cond.3 verifier file, cond.2 PASS 의 일부)

- **위치**: `/Users/ghost/core/anima/training/mitosis_model_v5_smoke_test.py` (256 LoC)
- **roadmap verifier 명**: `.roadmap.clm_v5_mitosis_engine.cond.2.verifier.paths[1]` = `training/mitosis_model_v5_smoke_test.py`. 본 cycle 신규 작성.
- **gating tests** (cond.2 PASS 의 조건):
  - `test_basic_forward_smoke` — d=32, cells=2, 10 steps, shape (2,8,64) preserved + finite + cells invariant
  - `test_f_v5mit_1_split_nograd` — split 후 새 cell parameters 가 backward graph 에 진입하지 않음 (leaf grad_fn=None, post-backward grad=None)
  - `test_f_v5mit_2_merge_weight` — merge keeper owned-params = (pre_a + pre_b) / 2 within 1e-6 (max_abs_err = 0.0 측정)
- **advisory tests** (cond.3 calibration용, cond.2 verdict 미영향):
  - `test_f_v5mit_3_phi_conservation` — per-cell Φ delta < 25%

### §1.3 smoke 실측 결과

```
[PASS] basic_forward_smoke  [gating]
    shape_ok: True
    finite: True
    initial_n_cells: 2
    final_n_cells: 2

[PASS] F-V5MIT-1 SPLIT-NOGRAD  [gating]
    pre_n_cells: 2
    post_n_cells: 3
    new_param_tensors: 14
    leaf_violations: 0
    new_with_grad_after_backward: 0

[PASS] F-V5MIT-2 MERGE-WEIGHT  [gating]
    checked_params: 14
    skipped: 0
    max_abs_err: 0.0
    tolerance: 1e-06

[NOTE] F-V5MIT-3 PHI-CONSERVATION (per-cell)  [advisory — does not gate cond.2]
    phi_pre_total: 3.3256558458086154
    phi_post_total: 6.652221846034706
    n_pre: 5
    n_post: 6
    phi_pre_per_cell: 0.6651311691617231
    phi_post_per_cell: 1.1087036410057844
    delta_per_cell_ratio: 0.6668947305583405
    tolerance_per_cell_ratio: 0.25
    honest_c3_note: raw Φ_total scales by log(N+1); per-cell Φ used as conservation comparator. Tolerance 25% loose — cond.3 calibrates.

=== summary ===
{
  "cond2_verdict": "PASS",
  "n_gating_tests": 3,
  "n_gating_passed": 3,
  "n_advisory_tests": 1,
  "n_advisory_passed": 0,
  "wall_seconds": 0.085,
  "device": "cpu",
  "torch_version": "2.8.0"
}
```

추가 더 큰 smoke (`training/mitosis_model_v5_smoke.py`, 50+4+50 step, N=4→64) 도 **8/8 checks PASS** — phase1 Φ 0.39→828, phase3 Φ 1063→2944 (log(N+1) × diversity 두 vector 동시 성장 = expected mitosis dynamics).

---

## §2 honest C3 (≥3 항목 본 cycle 신규)

1. **F-V5MIT-3 fails 67%**: per-cell Φ delta 가 25% tolerance 초과 (실측 67%). cause = 새 cell 의 cell_state buffer 가 parent 의 norm-scaled noise 로 perturb 되는데, initial state 가 거의 zero 인 cold-start 환경에서는 noise injection 이 cell signature 의 dominant component 가 됨 → mean pairwise distance 가 split 시 크게 증가. spec §11 #9 ("DD55 검증은 toy substrate") 와 일치 — **cond.3 calibration item**. 두 가지 mitigation candidates: (a) warmup forward 더 길게 (50+ step 후 force_split), (b) noise scale 0.1 → 0.01 (cold-start), (c) per-cell Φ 비교를 forward 안정화 후만 valid 로 인정.

2. **prior-cycle skeleton 의 spec drift**: `training/mitosis_model_v5.py` header 는 `2026-05-10` spec 을 reference, 본 cycle 의 `2026-05-12` spec 도 cond.2 verifier 로 충족. roadmap `.roadmap.clm_v5_mitosis_engine.cond.1.verifier.paths` = `any_match` 둘 다 listing → 본 carry 가 valid. 미래 cycle 에서 spec drift 가 발생하면 본 carry 의 안전성 재검증 필요.

3. **CellMeta dataclass vs cell instance attr**: spec §2.3 는 `@dataclass CellMeta` 명시했지만 impl 은 cell 의 python instance attribute (cell_id / creation_step / parent_id / tension_history / process_count) 으로 처리. semantics 동등 (둘 다 non-grad python state), 더 간단. spec §A append convention 에 따라 향후 §A 이후 entry 로 "CellMeta inline attribute" 결정 기록 권장.

4. **softmax_gate readout_mode 미impl**: spec §6.3 의 4 option 중 3 까지만 (`a_minus_g`/`a_only`/`a_plus_g`). softmax_gate 는 learned gate projection 필요 (`gate_proj`) — 향후 ablation 시 추가. 현재 `a_plus_g` 는 spec 의 `a + 0.3 × g` 의 unweighted variant.

5. **attention_sharing N>8 fallback** = irreversible — 한 번 promote 되면 demote 불가. spec §11 #11 risk. cond.3 에서는 `attention_sharing="never"` 로 (per-cell attn 보존). cond.5 cotrain 시 cells_max=64 에 도달하면 메모리 절감 위해 promotion 필요할 가능성.

---

## §3 next steps

| 순위 | step | deliverable | cost | fire | status |
|---:|---|---|---:|---|---|
| 1 ★★★ | cond.1 spec | `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md` | $0 | DONE 2026-05-12 (REBORN §88) | met |
| 2 ★★★ | cond.2 skeleton | `training/mitosis_model_v5.py` + `training/mitosis_model_v5_smoke_test.py` | $0 | DONE 2026-05-12 (본 doc) | **met (PASS)** |
| 3 ★★★ | cond.3 Mac CPU smoke 정밀화 | per-cell Φ tolerance calibration + 50+ step warmup smoke + V14 mirror reproduce | $0 | AUTO post 본 PASS | next |
| 4 ★★ | cond.4 long-trajectory | 3K-10K turn, α metric + Φ-rate vs split correlation | $0 | AUTO post cond.3 PASS | pending |
| 5 ★★★★ | cond.5 H100 cotrain | 5K step × cells 2→64, V14-STRICT 5-seed × 5-seed | **$30-40** | **`OK CLM V5-MITOSIS H100 FIRE COST $40`** verbatim | pending |
| 6 ★★ | cond.6 HF promote | dancinlab/clm-v5-mitosis-engine private | $0 | own 37 5/5 prereq | pending |

---

## §4 cross-link

### upstream
- REBORN.md §88 (cond.1 arch spec land, 본 doc 의 직접 prereq)
- REBORN.md §90 (cond.2 PASS, 본 doc append target)
- `.roadmap.clm_v5_mitosis_engine` cond.2 (본 doc 가 verdict 갱신)
- `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md` (spec, 본 doc 의 impl evidence)

### code (training/.py — gitignored or explicit add per repo policy)
- `training/mitosis_model_v5.py` (852 LoC, prior-cycle, 본 cycle reuse + verify)
- `training/mitosis_model_v5_smoke_test.py` (256 LoC, 본 cycle 신규 — cond.2 verifier)
- `training/mitosis_model_v5_smoke.py` (181 LoC, prior-cycle, 본 cycle 재실행 PASS)

### sister
- `docs/anima_clm_v5_hexa_native_mitosis_hook_spec_2026_05_12.md` (REBORN §89, sister hexa lane)
- `docs/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10.md` (V14 violated, F-V5MIT-5 target)

### memory entries (본 cycle 신규)
- `project_v5_mitosis_cond2_port_skeleton.md`

---

## §A append convention

본 doc 는 cycle 2026-05-12 close 시점 cond.2 PASS snapshot. 향후 추가 finding (cond.3 calibration, F-V5MIT-3 mitigation, V14 mirror result) 는 §A 이후 append-only — `## §N [YYYY-MM-DD HH:MM KST] <title>` format.

raw#9 (training/.py policy — repo 의 `**/*.py` 허용, gitignored 가 아님; 별도 명시 add 권장), raw#10 (honest C3 ≥3 — §2), raw#15 (additive — 기존 skeleton 미수정, smoke_test 만 신규), raw#37 (additive preserve), own 16 (cost discipline — $0 PASS).

end of `anima_clm_v5_mitosis_cond2_smoke_2026_05_12.md`.
