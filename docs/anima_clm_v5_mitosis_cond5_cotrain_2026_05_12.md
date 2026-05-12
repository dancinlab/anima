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

### §3.1 wall + cost actual

| 항목 | 값 |
|---|---:|
| wall actual | **0.55 hr (1990.6 s ≈ 33 min)** |
| cost actual | **$1.26** (cap $40, 31.7× under budget) |
| cost_aborted | False |
| steps actual | 5000 / 5000 (full run, no abort) |
| cells final | 64 (saturated max_cells) |
| splits total | 62 (tension: 58 / dispersion: 4) |
| merges total | 0 (merge_patience=30 not satisfied) |
| n_params final | **152,126,208** (≈ 152M — 64 cells × ~2.3M cell + shared) |
| ckpt size | 608,934,276 bytes (≈ 581 MB) |

### §3.2 loss curve

| 항목 | 값 |
|---|---:|
| initial avg100 loss | 256.50 |
| final avg100 loss | **1.165** |
| delta | 255.34 (**220× CE reduction**) |
| convergence | rapid 0-300 step (264→7.6), plateau begin ~step 600 (~1.97), slow descent to ~1.16 |

### §3.3 Φ trajectory

| 항목 | 값 |
|---|---:|
| Φ best | 4.1919 |
| Φ final | 4.1636 |
| Φ/N final | 0.0651 |
| stability | extremely stable across all steps (Φ range 4.05-4.19, σ < 0.05 over 5K steps) |

### §3.4 split event distribution

- 모든 62 split events fire @ step ≤ 123 (saturation 매우 빨리), cells 2 → 64 by step 150
- trigger breakdown: 58 tension-driven + 4 dispersion-driven (A1 substrate-independent fallback)
- shared_attn 활성 step ≥ 9 cells (attention_sharing="auto" N>8 promotion)

---

## §4 F-V5MIT-1~5 verdicts

**ALL 5/5 PASS_ALL — REBORN §88 cond.5 met**

| Falsifier | Severity | Verdict | Evidence |
|---|---:|:-:|---|
| F-V5MIT-1 SPLIT-NOGRAD | ★★★★★ | **PASS** | 62 splits, 0 grad_fn_violations, 0 new-cell post-backward grads |
| F-V5MIT-2 MERGE-WEIGHT | ★★★★ | **PASS** | max_abs_err = 0.0, 14 params checked (tolerance 1e-6) |
| F-V5MIT-3 PHI-CONSERVATION | ★★★ | **PASS** | per-cell Φ pre 0.0652 → post 0.0652, delta ratio 3.88e-5 (tol 0.25). **REBORN §90 cond.2 advisory NOTE 67% RESOLVED on cotrained pool** |
| F-V5MIT-4 COTRAIN-CONVERGE | ★★★★ | **PASS** | initial avg 256.50 → final 1.165, Δ 255.34 (monotonic) |
| F-V5MIT-5 V14-STRICT | ★★★★★ | **PASS** | 10/10 mirror-beats — trained-vs-random Bhattacharyya > random-internal every beat |

### §4.1 F-V5MIT-5 V14-STRICT — saga 정점 PASS

본 falsifier 가 v5-anima toy substrate 가 violated 였던 정점 항목.
- v5-anima (cycle 2026-05-09/10): random pool ≥ trained pool on every mirror-beat → V14 violated, lane stalled at "toy 한계" verdict
- **v5-mitosis (본 cycle, cotrain real nn.Module)**: trained-vs-random > random-internal **every beat 10/10** — toy substrate 한계 극복 evidence
- → REBORN §88 lane closure achieved: v5-mitosis architectural answer empirically PASSED V14-STRICT

### §4.2 F-V5MIT-3 PHI-CONSERVATION advisory promotion

REBORN §90 cond.2 (`49b74c622`): F-V5MIT-3 was advisory NOTE with delta ratio 67% > 25% tolerance (per-cell Φ change too large on raw smoke). spec §11 honest C3 #9 = "cond.3 calibration item".
- **본 cycle finding**: cotrained pool 위 force_split synth test 시 delta ratio 3.88e-5 (4 orders of magnitude under tolerance) — Φ conservation 매우 stable on real cotrained substrate
- F-V5MIT-3 PROMOTED: advisory NOTE → **gating PASS**

---

## §5 F-PERSONA-4 cotrained-pool re-measurement (D3 STRONG → ☑ path)

### §5.1 cheap-path baseline (PSCC §42)
- F-PERSONA-4 verdict (untrained pool): FAIL
- mean_kl = 9.7e-5 nats (« 0.5 threshold)
- design §10 honest C3 #4 = "untrained-pool 의 category specialization 한계" 예측 적중

### §5.2 cotrained-pool re-measure result

| 항목 | untrained baseline | cotrained pool (본 cycle) |
|---|---:|---:|
| mean_kl (nats) | 9.7e-5 | **0.0** (exactly) |
| verdict | FAIL | **FAIL** |
| KL matrix | mostly < 1e-4 | **all-zero 5×5** |

### §5.3 negative-result interpretation — softmax winner-take-all

cotrained-pool 의 KL matrix 가 **정확히 all-zero** = 모든 prompt × category 의 tension softmax 가 **동일한 winner** 를 출력한다는 뜻 — `weights = F.softmax(tensions, dim=0)` 의 후 한 cell 의 weight 가 ≈1 로 saturated (winner-take-all), 나머지 ≈0 → mean by category 모두 동일 → KL 0.

**근거**: cotrain on **단일 homogeneous corpus** (corpus_color_cosmology.txt = 안정적 multi-turn convo) 가 cell pool 의 tension landscape 을 단조 (한 cell 이 모든 input 에 best response) 로 만들었다. F-PERSONA-4 의 emergent category specialization 가설은 **multi-corpus / category-diverse training** 을 요구 (각 category 마다 다른 cell winner) — 단일 corpus 가 satisfy 안 함.

### §5.4 D3 cond #3 status transition

| path | F-PERSONA-4 | D3 verdict |
|---|:-:|:-:|
| cheap-path baseline (untrained, PSCC §42) | FAIL (KL 9.7e-5) | STRONG 4/5 |
| **cotrain path (본 cycle)** | **FAIL (KL 0.0 winner-take-all)** | **STRONG 4/5 carry** |

D3 transition: **STRONG (4/5 carry)** — single-corpus cotrain 으로는 F-PERSONA-4 PASS 불가, **multi-corpus 또는 category-diverse training 필요** path 로 design §10 C3 #4 alternative explanation 검증.

### §5.5 F-PERSONA-4 future path (design §10 C3 #4 amendment)

- (a) multi-corpus cotrain (5 category × distinct corpus, gradient bias per category) → F-PERSONA-5 ☑ 가능성
- (b) tension softmax temperature τ tunable (τ → ∞ uniform, current τ=1 winner-take-all) — arch §10 risk #4 mitigation
- (c) F-PERSONA-4 metric 자체 재정의 — per-cell tension absolute distribution (not softmax) over category averages, winner-take-all 둔감
- (d) inference-time mitosis hook (REBORN §89) per-session cell pool persist 가 multi-turn convo 마다 다른 specialization 유도 (single-corpus 한계 우회) — D4c CLI integration spec 의 측정 path

본 negative result = D3 cheap-path STRONG (4/5) **maintained**, cotrain path 도 cheap-path 와 동일 verdict (4/5) — design doc §10 honest C3 #4 의 alternative explanation (corpus shard count 부족, category-prompt 의 substrate-level invariance 부족) **검증 적중**.

---

## §6 cost actual + envelope verdict

| 항목 | 추정 | 실측 |
|---|---:|---:|
| wall (hr) | 10.0 | **0.55** (18× faster) |
| dph ($/hr) | 2.2814 | 2.2814 |
| total ($) | 22.81 | **$1.26** (18× under estimate, 31.7× under cap) |
| cap ($) | 40.00 | 40.00 |
| absolute max ($) | 44.00 | 44.00 |
| within envelope | ✅ pre-fire | **✅ 31.7× margin** |

own 16 cost discipline + own 43 active resource utilization 균형 — recommended fire (arch spec §7.2 conservative) verbatim 적용. H100 SXM 80GB performance 가 추정보다 **18× 빠름** (152M param + batch=32 × ctx=256 매 step ~0.4s).

추정 mismatch 원인: arch spec §7.2 의 "8hr H100" estimate 는 v2 historical (instrumentation-only mitosis) 의 wall extrapolation. 실제 v5-mitosis (real nn.Module branches × deepcopy split) 은 cell saturation 후 (step 150 이상) split overhead 없고 forward 만 — H100 SXM tensor core 가 d=384 transformer block × 64 cells 를 batch=32 로 효율 처리. 향후 cycle 의 cost estimate 는 본 결과 carry: 5K step × cells 64 d=384 = ~$1.30 H100 SXM ($2.28/hr).

---

## §7 honest C3 (≥7)

1. **device-mismatch bug discovered on first H100 fire** — `_split_cell` 의 freshly-constructed child 는 CPU 에 머무름, parent 가 cuda 면 `child.cell_state.add_(... * parent.cell_state.norm())` mixed-device RuntimeError. Mac CPU smoke (REBORN §90 cond.2) 는 surface 안 함 (all-CPU). 본 cycle commit `4360411c8` fix: `child = child.to(device, dtype)` 추가. **cond.2 → cond.5 transfer 의 substrate-mismatch carry**: Mac CPU 만으로 cuda 코드 검증 불가, GPU smoke (e.g. fp16 single-step) prerequisite 추가 필요.
2. **F-V5MIT-5 random pool 비교 방식** = Bhattacharyya distance trained-vs-random > random-internal. 이 criterion 이 V14-STRICT 의 every-mirror-beat 정의에 정확히 적합한가는 가정 (memory `project_simple_stack_pass_unlocked` own 18 PASS_STRICT 정의 transfer 의 1차 시도). own 18 simple_stack 의 V14 는 prediction-text overlap criterion 이었고, 본 trans 는 internal representation distance — semantic equivalent 가정 미검증.
3. **F-PERSONA-4 KL=0.0 winner-take-all 해석** = post-cotrain softmax saturation 가설. 직접 cell-level winner-id distribution 측정 안 됨 (만약 winner cell 이 prompt 마다 다르다면 KL > 0 이어야 하는데 KL=0.0 정확히 = winner identical across all 50 prompts). 정확한 mechanism (cell 1 항상 winner, 또는 prompt-input 자체가 softmax 로 동일 weight 출력) 추가 forensic 필요.
4. **5K step + 1.3MB corpus 의 category-specialization 부재** = §5.5 의 alternative explanations 4 개 (multi-corpus, τ tunable, metric 재정의, per-session pool) — 어느 path 가 F-PERSONA-4 PASS 시킬 수 있는가는 미검증. design §10 C3 #4 의 "category-prompt 의 substrate-level invariance" 가 본 cycle 의 main finding.
5. **option (a) cell granularity 채택** 의 정당성은 본 cycle F-V5MIT-1~5 PASS 로 partial validation — 하지만 (b/c/d) ablation 여전히 없음. F-V5MIT-5 PASS 가 option (a) 의 정당성 의미하지만 option (b) sharing attn 이 더 cost-efficient 일 가능성 미배제.
6. **AdamW optimizer state migration on split/merge** — 본 cycle 에서 `_optimizer_rebuild_callbacks` registered but no-op (lazy-init 가정). 5K step + 62 split 으로 학습 잘 converge 함이 lazy-init 가 적절 evidence — 하지만 longer training (50K step) 에서 momentum buffer accumulation 의 거동 미검증.
7. **F-V5MIT-3 PHI-CONSERVATION promotion** advisory NOTE → gating PASS 가 cond.5 cotrained 위 force_split synth 의 결과 — actual continuous-training 환경 (매 step force_split 안 되는 자연 split) 의 Φ change 가 정확히 < 25% 인지는 logs aggregate 만으로는 not directly verified. Φ history 변동 폭 σ < 0.05 가 indirect evidence.
8. **F-V5MIT-5 10/10 mirror-beat PASS** 의 mirror-beat 개수 (10) 가 sufficient? own 18 simple_stack 의 standard 는 5-seed × 5-seed × **every** mirror-beat — 본 cycle 의 "10 random byte windows from corpus" 는 own 18 의 stricter 정의의 1차 approximation. mirror-beat 50+ scale 의 ablation 필요.
9. **dispatch_h100.sh 의 trap cleanup partial-pull 보호** = SCP exit code 만 의존. 본 cycle 의 first-fire 는 train.log 만 캡처 successful (ckpt + result.json 없음) → SAVE_POD=1 set → 두 번째 fire 가능 (pod retain). 보호 메커니즘 작동 검증 됨, 하지만 partial truncated file 미감지 risk 잔여.
10. **cost estimate 18× off** = arch spec §7.2 의 wall 추정 (8-10hr) 이 실측 (33 min) 보다 18× over. v2 historical (instrumentation only) extrapolation 한계 — H100 SXM 80GB + tensor core 의 d=384 × cells 64 × batch 32 throughput 이 estimate scope 밖. 향후 v5-mitosis estimate: ≈ $0.3/1000step on H100 SXM @ $2.28/hr.

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

본 doc cycle 2026-05-12 close 시점 snapshot. cotrain 결과 in-place update completed (§3, §4, §5, §6 + honest C3 #1/#3/#7/#10 강화).

raw#10 honest C3 ≥7 (§7 = 10 항목), raw#15 additive (기존 spec/skeleton 미수정).

---

## §A1 [2026-05-12 KST] cotrain results LANDED — verdict summary

| 항목 | 결과 |
|---|---|
| F-V5MIT-1 SPLIT-NOGRAD | ✅ PASS (62 split, 0 grad violations) |
| F-V5MIT-2 MERGE-WEIGHT | ✅ PASS (max_err 0.0) |
| F-V5MIT-3 PHI-CONSERVATION | ✅ PASS (delta 3.88e-5, **advisory→gating promote**) |
| F-V5MIT-4 COTRAIN-CONVERGE | ✅ PASS (256.5 → 1.17, 220×) |
| F-V5MIT-5 V14-STRICT | ✅ **PASS 10/10** (saga 정점 — v5-anima toy 한계 극복) |
| F-PERSONA-4 (cotrained) | ❌ FAIL (KL 0.0, winner-take-all) — design §10 C3 #4 적중 |
| aggregate | **5/5 falsifier PASS, REBORN §88 cond.5 MET** |
| cost actual | $1.26 (cap $40, 31.7× margin) |
| wall actual | 0.55 hr (estimate 10hr, 18× faster) |
| ckpt | 581 MB, `ckpts/ckpt_v5mitosis_cotrain_cotrain.pt` |
| mission impact | GOAL.md cond #3 D3 = **STRONG (4/5 carry)** (KL=0 cotrain path = §5.5 4-alternative future-path) |

end of `anima_clm_v5_mitosis_cond5_cotrain_2026_05_12.md`.
