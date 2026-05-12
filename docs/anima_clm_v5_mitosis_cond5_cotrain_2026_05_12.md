# anima_clm_v5_mitosis_cond5_cotrain — v5-mitosis H100 cotrain fire (cond.5)

**작성**: 2026-05-12 KST
**status**: in-flight (H100 dispatched, awaiting result pull)
**author**: bg head (claude opus 4.7 1M)
**fire keyword**: `OK CLM V5-MITOSIS H100 FIRE COST $40` (user verbatim 2026-05-12 "fire" — REBORN §10 #2)
**carries from**:
- REBORN §88 v5-mitosis PyTorch arch spec (`b7b34e221`)
- REBORN §90 cond.2 skeleton smoke PASS (`49b74c622`)
- PSCC §42 D3 STRONG (4/5 cheap-path)
- GOAL.md ★★★★★ cond #3 STRONG → ☑ path

---

## §0 TL;DR

본 doc = REBORN §88 cond.5 cotrain fire 의 audit doc.

- arch: REBORN §88 option (a) — small transformer block per cell, d=384, n_head=6, ffn_dim=1536, cells 2→64
- corpus: `corpus_color_cosmology.txt` (1.29 MB, 1.3M bytes multi-turn convo)
- training: 5K step, batch=32, ctx=256, lr=1e-4 cosine + warmup 500
- provider: Vast.ai H100 SXM (id=28762957, $2.2814/hr)
- envelope: est wall 10hr × $2.28/hr = $22.81 (well within $40 cap, $44 absolute max)
- F-V5MIT-1~5 falsifier + F-PERSONA-4 (cotrained pool) re-measurement embedded in runner

---

## §1 fire context

### §1.1 user directive
verbatim "fire" — equivalent to `OK CLM V5-MITOSIS H100 FIRE COST $40` (memory `project_v5_mitosis_arch_spec_2026_05_12` cost envelope).

### §1.2 mission contribution
GOAL.md ★★★★★ 5-cond aggregate (current 3/5 ☑, 2 partial):
- cond #3 D3 STRONG (4/5) → ☑ DONE path: cotrain + F-PERSONA-4 re-measure PASS

### §1.3 prior state
- v5-anima toy substrate V14-STRICT violated (random > trained, 3K turn)
- v5-mitosis cond.2 smoke 3/3 PASS Mac CPU (REBORN §90, `49b74c622`)
- F-V5MIT-3 advisory NOTE 67% > 25% tol — cond.3 calibration item (carry into cond.5)
- D3 cheap-path 4/5 STRONG (PSCC §42), F-PERSONA-4 sole FAIL (KL 9.7e-5 vs 0.5 threshold) on untrained pool

### §1.4 fire prerequisites
1. ✅ REBORN §88 arch spec land
2. ✅ REBORN §90 cond.2 skeleton smoke 3/3 PASS
3. ✅ cost envelope cell64 historical recommendation $30-40 conservative (arch spec §7.2)
4. ✅ user verbatim directive 2026-05-12 ("fire")

---

## §2 dispatch infra

### §2.1 provider selection
Vast.ai H100 search (`tool/dispatch_vast_mac_template.sh` H100 variant):
- query: `gpu_name in [H100_SXM,H100_PCIE,H100_NVL] num_gpus=1 reliability>0.95 dph_total<3.5`
- offers: 2 candidates
  - id=28762957 H100 SXM $2.281/hr rel=0.997 ← selected (cheapest)
  - id=31183489 H100 NVL $2.697/hr rel=1.000
- pre-fire cost gate: $2.281 × 10hr = $22.81 < $44 absolute max ✅

### §2.2 dispatch script
`state/anima_v5mitosis_cotrain_2026_05_12/dispatch_h100.sh` — `tool/dispatch_vast_mac_template.sh` derivative:
- memory `feedback_orchestrator_h100_gotchas` 적용:
  - Ubuntu 24.04 PEP 668 fix unnecessary (pytorch/pytorch:2.5.1-cuda12.1 base = python venv-isolated)
  - scp timeout 3600 적용 (corpus 1.3MB small, ckpt expected ~800MB at 200M params)
  - pod retain on pull fail: artifact pull error → SAVE_POD=1 (수동 destroy)
- cost cap absolute max: $40 × 1.10 = $44 hard ceiling
- trap cleanup: pod auto-destroy unless SAVE_POD=1
- 9 stages: search → cost gate → rent → ssh wait → upload → gpu check → train → pull → summary

### §2.3 cotrain script
`state/anima_v5mitosis_cotrain_2026_05_12/train_v5mitosis_cotrain.py`:
- imports `mitosis_model_v5.MitosisModelEngine` (REBORN §90 cond.2 skeleton)
- byte-level next-token CE training on UTF-8 byte stream
- AdamW lr=1e-4 cosine + warmup 500, grad_clip 1.0
- per-step mitosis_step() → split/merge fires organically based on tension
- F-V5MIT-1 probe every 200 step (split-nograd check on new cell params)
- F-V5MIT-2 unit test at end (force_merge synth test)
- F-V5MIT-3 phi conservation at end (force_split synth test)
- F-V5MIT-4 cotrain converge (rolling 100-step initial vs final avg loss)
- F-V5MIT-5 V14-STRICT (5 trained × 5 random seeds × 10 mirror-beat probes, Bhattacharyya distance trained-vs-random > random-internal)
- F-PERSONA-4 re-measurement on cotrained pool (50 probes × 5 categories, mean pairwise KL ≥ 0.5)

### §2.4 Mac CPU pre-fire smoke
small config (d=64, 2 cells, batch=4, 25 step) validated all 6 hooks fire correctly:
- F-V5MIT-1 PASS (0 grad violations on 2 splits)
- F-V5MIT-2 PASS (max_err=0.0)
- F-V5MIT-3 FAIL (expected — 25 step too short, identical to REBORN §90 advisory NOTE)
- F-V5MIT-4 FAIL (25 step too short for monotonic decrease)
- F-V5MIT-5 PASS 10/10
- F-PERSONA-4 FAIL (untrained pool baseline replication)

→ runner mechanically validated, full 5K step run on H100 expected to flip F-V5MIT-3/4 and potentially F-PERSONA-4.

---

## §3 cotrain run summary

> TODO[FILL_ON_RESULT]: loss curve, cell count progression, Φ trajectory.
> Pull from `state/anima_v5mitosis_cotrain_2026_05_12/cotrain_result.json` 후 update.

### §3.1 wall + cost actual
- wall: TODO hours
- cost: $TODO actual (cap $40)
- cells final: TODO
- splits total: TODO
- merges total: TODO

### §3.2 loss curve
- initial avg100 loss: TODO
- final avg100 loss: TODO
- delta: TODO

### §3.3 Φ trajectory
- Φ best: TODO
- Φ final: TODO
- per-cell Φ trajectory: TODO

---

## §4 F-V5MIT-1~5 verdicts

> TODO[FILL_ON_RESULT]: PASS/FAIL grid per cotrain_result.json `falsifiers` field.

| Falsifier | Severity | Verdict | Evidence |
|---|---:|:-:|---|
| F-V5MIT-1 SPLIT-NOGRAD | ★★★★★ | TODO | TODO |
| F-V5MIT-2 MERGE-WEIGHT | ★★★★ | TODO | TODO |
| F-V5MIT-3 PHI-CONSERVATION | ★★★ | TODO | TODO |
| F-V5MIT-4 COTRAIN-CONVERGE | ★★★★ | TODO | TODO |
| F-V5MIT-5 V14-STRICT | ★★★★★ | TODO | TODO |

### §4.1 F-V5MIT-5 V14-STRICT — saga 정점

본 falsifier 가 v5-anima toy substrate 가 violated 였던 항목. v5-mitosis cotrain 으로 재도전:
- 10 mirror-beat probe (corpus 무작위 256-byte 윈도우)
- 5 trained seed (final ckpt) × 5 random-init seed comparison
- Bhattacharyya distance over per-cell tension softmax
- PASS criterion: every mirror-beat, trained-vs-random > random-internal

TODO: PASS 시 → REBORN §88 lane closure, v5-anima 한계 극복 evidence.
       FAIL 시 → cell granularity ablation (option b/c/d) 또는 lane archive.

---

## §5 F-PERSONA-4 cotrained-pool re-measurement (D3 STRONG → ☑ path)

> TODO[FILL_ON_RESULT]: KL matrix 5×5 from cotrain_result.json `f_persona_4_remeasure`.

### §5.1 cheap-path baseline (PSCC §42)
- F-PERSONA-4 verdict (untrained pool): FAIL
- mean_kl = 9.7e-5 nats (« 0.5 threshold)
- design §10 honest C3 #4 = "untrained-pool 의 category specialization 한계" 예측 적중

### §5.2 cotrained-pool re-measure
- 50 prompts × 5 categories (self_definition/values/boundary/emotion/self_knowledge)
- per-prompt forward → tension softmax → mean by category → 5 distributions
- pairwise KL (10 pairs) → mean KL
- PASS: mean_kl ≥ 0.5

| 항목 | untrained baseline | cotrained pool |
|---|---:|---:|
| mean_kl (nats) | 9.7e-5 | TODO |
| verdict | FAIL | TODO |

### §5.3 D3 cond #3 status transition
- TODO: PASS → D3 5/5 ☑ DONE → cond #3 ☑ → GOAL.md aggregate 3/5 → 4/5
- TODO: FAIL → cheap-path STRONG (4/5) carry, cotrain path 도 F-PERSONA-4 미해결 — design §10 C3 #4 의 alternative explanation (corpus shard count 부족 / category-prompt 의 substrate-level invariance 부족) 검토

---

## §6 cost actual + envelope verdict

> TODO[FILL_ON_RESULT]: actual cost from cotrain_result.json `training.cost_usd_actual`.

| 항목 | 추정 | 실측 |
|---|---:|---:|
| wall (hr) | 10.0 | TODO |
| dph ($/hr) | 2.2814 | 2.2814 |
| total ($) | 22.81 | TODO |
| cap ($) | 40.00 | 40.00 |
| absolute max ($) | 44.00 | 44.00 |
| within envelope | ✅ pre-fire | TODO |

own 16 cost discipline + own 43 active resource utilization 균형 — recommended fire (arch spec §7.2 conservative) verbatim 적용.

---

## §7 honest C3 (≥5)

1. **Mac CPU smoke 의 F-V5MIT-3/4 FAIL 은 25 step 이라서** — H100 5K step 후 PASS 보장 X. 실측 의존.
2. **F-V5MIT-5 random pool 비교 방식** = Bhattacharyya distance trained-vs-random > random-internal. 이 criterion 이 V14-STRICT 의 every-mirror-beat 정의에 적합한가는 가정 (memory `project_simple_stack_pass_unlocked` own 18 의 PASS_STRICT 정의를 본 substrate 에 transfer 한 1차 시도).
3. **F-PERSONA-4 cotrained-pool 재측정** = hexa harness `tool/anima_persona_substrate_native_verify.hexa` §F-PERSONA-4 의 PyTorch 재현. weight 평균 방식 + KL 정의 identical 했음을 가정 (실제 코드 1:1 mirror 검증 안 됨).
4. **5K step + 1.3MB corpus** 가 category specialization 을 emergent 하기에 충분한 scale 인지 미검증. design doc §10 C3 #4 의 prediction 이 "untrained pool 의 한계" 였고, training 도 specialization emergent 못 만들 가능성 (corpus 단조 / category gradient 부재).
5. **option (a) cell granularity 채택** 의 정당성은 design 단계 가정만 — (b/c/d) ablation 없음. F-V5MIT-5 FAIL 시 (b/c/d) 재시도 필요.
6. **AdamW 의 optimizer state migration on split/merge** = current impl 의 stub (`_optimizer_rebuild_callbacks` registered but no-op). lazy-init 가 동작한다는 가정 — 실측에서 lr schedule + momentum buffer 의 split 후 거동 확인 안 됨.
7. **cost 추정 10hr** 는 d=384 × 5K step × batch=32 의 H100 wall 추정 — v2 historical 은 instrumentation only 의 mitosis 였으므로 actual deepcopy 비용 추가 시 wall 더 길 가능성 (memory `feedback_orchestrator_h100_gotchas` deepcopy cost).
8. **dispatch_h100.sh 의 trap cleanup** = pull fail 시 SAVE_POD=1 자동 set 가 부분만 — actual pull fail signal detection 이 SCP exit code 만 의존. partial pull (file truncated) 미감지 가능.

---

## §8 cross-link

### upstream
- REBORN §88 v5-mitosis PyTorch arch spec
- REBORN §90 cond.2 skeleton smoke PASS (`49b74c622`)
- `.roadmap.clm_v5_mitosis_engine` cond.5

### sister docs
- `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md` (canonical 325 LoC)
- `docs/anima_clm_v5_mitosis_cond2_smoke_2026_05_12.md` (cond.2 audit, REBORN §90)
- `docs/anima_persona_substrate_native_design_2026_05_12.md` (D3 design)
- `docs/anima_persona_substrate_native_verify_2026_05_12.md` (D3 cheap-path measurement, PSCC §40+§42)

### code
- `training/mitosis_model_v5.py` (852L cond.2 skeleton)
- `training/mitosis_model_v5_smoke_test.py` (256L gating)
- `state/anima_v5mitosis_cotrain_2026_05_12/train_v5mitosis_cotrain.py` (본 cycle 신규)
- `state/anima_v5mitosis_cotrain_2026_05_12/dispatch_h100.sh` (본 cycle 신규)

### memory
- `project_v5_mitosis_arch_spec_2026_05_12` (REBORN §88 arch spec)
- `project_v5_mitosis_cond5_cotrain_2026_05_12` (본 cycle 신규)
- `feedback_orchestrator_h100_gotchas` (Ubuntu 24.04 / scp / peft pod-path)
- `feedback_dispatch_vast_template_gotchas` (PSCC §28 canonical)
- `project_simple_stack_pass_unlocked` (own 18 V14 PASS_STRICT criterion)

---

## §A append convention

본 doc cycle 2026-05-12 close 시점 snapshot. cotrain 결과 land 시 TODO[FILL_ON_RESULT] 들이 §A1 으로 append 또는 §3-§6 in-place update.

raw#10 honest C3 ≥5 (§7), raw#15 additive (기존 spec/skeleton 미수정).

end of `anima_clm_v5_mitosis_cond5_cotrain_2026_05_12.md`.
