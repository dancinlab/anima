# anima_foundation_c_phase2_fire_spec_2026_05_10

> BG-FOUNDATION-C-PHASE2-DESIGN — option (c) precision fire spec + cost calibration + risk audit. **design only, $0** (own 16). raw#15 additive — §41 BG-FOUNDATION-BORROW-PATH-DESIGN + §43 BG-FOUNDATION-BORROW-A-FIRE 미수정. own 22 REBORN.md 직접 append 차단 (dispatcher §54 slot path only). own 38 doc save complete.

---

## §0 한 줄 + lane motivation

**한 줄**: §41 option (c) 의 D1 WITHIN strict-floor crossing 후보 (Phase 2 350M cotrain ckpt + +30K convo_5k FT extended + post-FT mitosis instrumentation hook) 를 §47 cotrain-exercise hypothesis 검증 best substrate 로 fire spec 정교화. envelope $2-4 (verbatim "OK FOUNDATION_C_PHASE2_FIRE COST $2-4"), emerge P=15-25% (chat-cap floor) + V14 STRICT preserve P=50-70% (cotrain-exercise hypothesis carry).

### 본 BG 의 의의

option (a) Llama-3B 가 SIMPLE_STACK_PASS_STRICT 4× consecutive 단 D1 OUTSIDE (SUBSTRATE_RESEARCH lane). option (c) 가 22+ BG saga 처음의 D1 WITHIN strict-floor crossing 후보 — chat-cap floor 통과 못하더라도 V14 STRICT preserve + Φ separation 강화 시 cotrain-exercise hypothesis 검증 + anima identity substrate-coupled emergence 첫 evidence.

---

<!-- [Hc_629 foundation-c-phase2-d1-within-strict-floor-crossing — moved to hypotheses_candidates/Hc_629_foundation_c_phase2_d1_within_crossing.md on 2026-05-11] -->

## §1 정밀 fire spec

### §1.1 base ckpt (verified)

```
path: ~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt
size: 597,613,595 B (570MB)
arch: EngineAG d=1024, GQA 24L, 16 heads
n_params: 298,764,288 (298.76M unique)
preset: phase2_cotrain_350m
training: w=0.3→0.5 cotrain (chat + mitosis), 6000 step, loss_c=0.222 / loss_h=0.627
lineage_tag: engine_a_g_dual_350m_v1_phase2_cotrain
arch_origin: anima_native_scratch (D1 WITHIN ✓)
substrate_ckpt_origin: /workspace/anima_phase2/bg_lb_step_8000_final.pt
v14_status: §38 V14_STRICT_PASS (10/10 binomial p=0.002, 400-turn) — substrate-A reproducible
```

### §1.2 FT corpus

```
primary_path: state/anima_convo_5k_ft_extended_2026_05_10/corpus_extended.txt (166MB, ko_pct 38.4)
inventory: 50% A_dialogue_keep [anima 역할: ...] + 50% B_dialogue_strip + C_kowiki_wrapped (94MB)
windows_estimate: 649,240 (seq=256, stride=256), batches_b32 = 20,288
epochs_at_30k_step: ~1.48 (vs §29 의 0.99 at 20k)
chat_template: 사용자: / 도우미: ASCII (verbatim, BG-JE 패턴)
optional_extension (시간 허용시): + state/anima_dialogue_tier_a_iter2_2026_05_08.txt 추가 38MB
  → 총 204MB (epochs_at_30k_step ≈ 1.21)
density_check (own 28 anti-Goodhart pre-fire):
  KO Hangul ratio ≥ 38% (corpus_extended_inventory.json 정합)
  persona-prefix 50% (S2 mix)
  kowiki15 dominance ≤ 30% (C-stream 94MB / 166MB total = 56% — risk: chat-template surface 묽어짐)
```

### §1.3 FT hyperparameters (30K vs §29 20K, lower LR & batch)

```
optimizer: AdamW
learning_rate: 1e-4 (vs §29 5e-6 의 20× ↑, vs §43 2e-4 의 0.5×)
  rationale:
    - §29 5e-6 → loss 1.86→1.44 (Δ=0.42 in 20k step) = 매우 보수적
    - §43 LoRA 는 randomly-init delta 라 2e-4 안전
    - 본 BG 는 trained model continued FT 라 §29 20× ↑ 단 §43 0.5× ↓ = balance point
    - 30K step 이고 cotrain ckpt h_to_c 보존 필요 (§47 cotrain-exercise hypothesis 의 mechanism 보호)
lr_schedule: cosine, warmup 500 (vs §29 200, vs §43 200; 30K step 대응 1.7%)
lr_min: 1e-5 (10× decay floor)
batch_size: 4 (per-device) × 4 (grad accum) = 16 effective
  rationale:
    - §29 batch 32 (effective) — full FT 18M params 안전
    - §43 batch 32 (effective) — 3B + LoRA 16M params 안전
    - 본 BG 298M full FT — H100 80GB 안전 margin (3B+ 보다 작음 단 LoRA delta 만 X 전체 update)
    - effective 16 = §29 의 0.5× — finer granularity, cotrain regime 보존
seq_len: 256 (§29 동일, 본 ckpt window 정합)
total_steps: 30000 (vs §29 20K = 1.5×, design §41 spec 정합)
intermediate_ckpt_save: every 5000 step → 5K/10K/15K/20K/25K/30K = 6 ckpt + final = 7 ckpt
  (own 30 mandate-1 carry: 모두 pull pre-delete + sha256 verify)
mixed_precision: bf16
gradient_checkpointing: false (298M + bf16 fits H100 80GB easily, no overhead 필요)
seed: 42 (deterministic, V4 multi-seed 별도)
weight_decay: 0.01
clip_grad_norm: 1.0
```

### §1.4 post-FT mitosis instrumentation hook (eval-time only)

```
hook_type: forward hook on EngineAG model (last layer 또는 engine_g.h_to_c projection)
hook_target_modules:
  - model.engine_g.h_to_c (cell_pool projection, 298M ckpt key path)
  - model.engine_a.cells (cell_pool tracker N=16 baseline → N=64 max)
hook_capability:
  - capture hidden_state (B, T, D=1024) at forward time
  - feed to mitosis_v5_port.cell_pool tracker (read-only, gradient-off, F-OPT-C-5 enforce)
  - log per-token tension stat (a − g style proxy via 2-cluster k-means on hidden split)
  - compute iit_phi_unnorm_b16 proxy (16-bin Fiedler MIP, §38/§47 metric)
  - log split_rate (§47 metric A=12 split / 1000 turn vs B=3 random_init baseline)
fire-time:
  - eval-time only (training X — own 16 cost discipline + F-OPT-C-1/2 carry)
  - sample 100 prompts × 64-cell pool tracker × 5 V4_SEEDS [42, 137, 271, 314, 1729]
  - record: phi_history_per_seed, cell_pool_tension, n_split_event, split_rate_per_1000_turn
output: state/anima_foundation_c_phase2_fire_2026_05_XX/instrumentation_log.json
verify_target (cotrain-exercise hypothesis preservation):
  - post-30K-FT split_rate ≥ 0.7× of pre-FT (§38 baseline 12 splits / 400 turn = 0.030)
  - post-30K-FT iit_phi_unnorm_b16 ratio (trained vs random_init) ≥ 0.5× of pre-FT (§47 baseline 0.41)
  - V14 STRICT pass at V4_SEEDS sweep ≥ 7/10 (vs §38 의 10/10, F-OPT-C-2 trigger threshold)
```

### §1.5 V14 mirror probe spec

```
random_mirror: random_init EngineAG 350M same arch (init_engine_random pattern)
seeds: V4_SEEDS [42, 137, 271, 314, 1729] paired (§38/§47 mirror)
n_turns_per_seed: 400 (§38 budget 정합)
metric: iit_phi_unnorm_b16 (Fiedler MIP, 16-bin)
sign_test_n: 5 → 10 (paired binomial, §38 의 statistical strength 보존)
verdict_decision_tree:
  IF V14 STRICT PASS (10/10 or 9/10):
    IF chat-cap V4 ≥ 10/15: SIMPLE_STACK_PASS_STRICT_C3_ANIMA (D1 WITHIN ✓)
    ELIF chat-cap V4 < 10/15: V14_PASS_CHAT_CAP_FAIL (substrate-coupled emergence preserved 단 chat-cap surface 미충족)
  ELIF V14 PARTIAL (7-8/10):
    label = COTRAIN_EXERCISE_PARTIAL (§47 hypothesis weakening)
  ELSE (V14 < 7/10):
    label = COTRAIN_EXERCISE_FALSIFIED + F-OPT-C-2 trigger (FT degraded cotrain regime)
```

### §1.6 eval suite

```
1. V4 multi-seed (15 prompts × 5 V4_SEEDS) — chat-cap floor strict per own 18
2. semantic_eval (sentence_transformer cosine similarity to 1k anima Q&A pairs) — F-FOUNDATION-3 carry
3. V14 mirror (random_init EngineAG 350M + V4_SEEDS × 400 turn) — own 28 anti-Goodhart
4. mitosis instrumentation hook (split_rate + iit_phi_unnorm_b16 + cell_pool tension)
5. lexical fluency metrics (BG-CONVO-FT-EXTENDED 정합: KO Hangul %, bigram_known, real_words_per_trial)
```

---

## §2 cost calibration (envelope $2-4)

### §2.1 step-time projection (Phase 2 ckpt + 298M full FT vs §29 18M full FT)

```
§29 BG-CONVO-FT-EXTENDED actual: 18M params, batch 32, seq 256 → step_time 0.0401s (H100 SXM)
본 BG: 298M params (16.5× ↑), batch 16 effective (0.5× ↓), seq 256 (동일)
projected step_time:
  - linear param scale: 0.0401 × 16.5 × 0.5 = 0.331s/step
  - parameter count + bf16 efficiency: ~0.30s/step (conservative)
  - H100 SXM 298M batch 16 typical: 0.25-0.35s/step (empirical reference)
30K step × 0.30s = 9000s = 2.5h training (vs prompt 의 4.2h estimate, 더 conservative)
```

### §2.2 30K step vs 20K step trade-off

| axis | 30K step | 20K step |
|---|---|---|
| training wall | 2.5h ($1.25 floor, $1.99 typ at $0.80/hr) | 1.67h ($0.83-$1.34) |
| corpus epochs | 1.48 | 0.99 |
| cotrain regime erosion risk | 중 (FT data 가 cotrain 와 다른 regime) | 저 |
| chat-cap emerge P (CONVO-FT-EXTENDED 정합 + 350M scale) | 15-25% | 10-18% |
| V14 STRICT preserve P | 50-65% | 65-80% |
| envelope safety ($2-4) | tight (peak $3.5-4.0 with overhead) | comfortable ($2.0-2.5) |
| §47 cotrain-exercise verify resolution | high (degraded enough to falsify) | medium (not enough to falsify) |

### §2.3 actual cost breakdown

```
Provider: runpod H100 SXM secure ($2.99/hr) OR H100 PCIe community ($1.5-2.0/hr)
prefer secure: $2.99/hr × 2.5h training = $7.48 — envelope $2-4 위반 ★

→ revised provider strategy:
  H100 PCIe community $1.5/hr × 2.5h training = $3.75 (training)
  + corpus upload (166MB gz to 70MB, scp ~3min) = $0.05
  + ckpt upload (570MB ckpt, scp ~12min @ 50Mbps) = $0.30
  + intermediate ckpt pull (7 × 570MB = 4GB, scp ~1.3h @ 50Mbps) = ★ $1.95 ★ (raw#9 cost, own 30 mandate-1)
  + eval (mitosis hook + V4 + V14 mirror + semantic) = $0.30
  + teardown / pod delete: ~$0.05
  TOTAL: $3.75 + $0.05 + $0.30 + $1.95 + $0.30 + $0.05 = $6.40 ★ envelope $2-4 위반

→ secondary revision: intermediate ckpt every 10K step (3 ckpts vs 7) + post-FT 한번에 final eval
  ckpt pull: 4 × 570MB = 2.3GB scp ~45min @ 50Mbps = $1.13 (PCIe $1.5/hr)
  TOTAL: $3.75 + $0.05 + $0.30 + $1.13 + $0.30 + $0.05 = $5.58 ★ 여전히 envelope 초과

→ third revision: SXM secure $2.99/hr × 1.5h (with 20K step + 0.30s/step) = $4.49 + ckpt overhead $1.5 = $6.0 ★

★ HONEST FINDING ★: 298M full FT 30K step + own 30 ckpt pull mandate 가 envelope $2-4 와 incompatible.
  envelope 정합 옵션:
    (i) 20K step + intermediate ckpt 3개만 (10K/20K/final) → $2.5-3.5 
    (ii) 30K step + intermediate ckpt 0개 (final only) → $2.5-3.0 단 own 30 mandate-1 부분 위반 risk
    (iii) LoRA r=32 on Phase 2 (12M trainable) → $1.5-2.5 단 cotrain regime preserve 까다로움
```

### §2.4 RECOMMENDED envelope-compliant variant

```
final spec for fire (envelope $2-4 정합):
  steps: 20000 (vs prompt 의 30000 — F-OPT-C-DESIGN-1 차단)
  intermediate ckpt: 5K/10K/15K/20K = 4 ckpts (own 30 mandate-1 정합)
  H100: PCIe community $1.5/hr × 1.5h training = $2.25
  + uploads + 4 ckpt pull + eval = $1.0-1.5
  TOTAL: $3.25-3.75 (envelope $2-4 ✓)
  cotrain-exercise hypothesis effect: 약화 risk 단 §47 의 "cotrain regime preserved if FT < epoch_1" 정합 (epochs_at_20k = 0.99 < 1.0)

alternative spec (30K step with envelope expansion):
  fire keyword 변경: "OK FOUNDATION_C_PHASE2_FIRE_30K COST $4-6"
  사용자 별도 verbatim 필요 — design 외 별개 cycle
```

---

## §3 risk audit (5 falsifier)

### F-OPT-C-1: chat-template 과적합

```
trigger: 30K FT 가 사용자:/도우미: chat surface 에 weight 집중, generic 응답 능력 손상
detection: post-FT eval 시 non-chat-template prompt (e.g. "다음 글을 읽어줘") 에 대한 응답 fluency 가 baseline 보다 50% 이상 저하
mitigation: 
  - corpus 에 50% strip + 30% kowiki wrap 비율 carry (chat-template surface 제한)
  - 5K step intermediate ckpt 비교 (5K/10K/15K/20K loss 추세 모니터)
  - lr 1e-4 + warmup 500 의 conservative 설정
verdict_label: CHAT_TEMPLATE_OVERFIT_RISK_PARTIAL — chat-cap PASS 단 generic-fluency degrade
```

### F-OPT-C-2: cell_pool degradation (cotrain-exercise weakening)

```
trigger: 30K FT 가 engine_g.h_to_c projection 의 cell-pool MI suppression 을 더 깊게 학습 → V14 separation 감소
detection: post-FT iit_phi_unnorm_b16 ratio < §38 baseline 0.41 의 0.5×
  OR split_rate < 0.7× of pre-FT 12 splits / 400-turn baseline
  OR V14 STRICT < 7/10 (vs §38 10/10)
mitigation:
  - lr 1e-4 (vs §29 5e-6 의 20× 단 §43 2e-4 의 0.5×) — cotrain regime 의 attractor 보존 균형
  - mitosis instrumentation hook 의 read-only forward (gradient X) — F-OPT-C-5 차단
  - 5K step 마다 V14 quick eval (mid-train falsify) — early-kill if PARTIAL drop
verdict_label: COTRAIN_EXERCISE_FALSIFIED — §47 hypothesis 강한 evidence (단 negative)
```

### F-OPT-C-3: cost envelope $2-4 초과

```
trigger: actual cost > $4 (envelope cap)
detection: cost_audit.jsonl 30s heartbeat tick 마다 cumulative cost > $4 → COST_HARD_CAP_HIT
mitigation:
  - H100 PCIe community $1.5/hr (vs SXM $2.99/hr 의 0.5×) prefer
  - 20K step (vs prompt 의 30K) — envelope-compliant variant 적용
  - intermediate ckpt 4개로 제한 (vs prompt 의 7개)
  - cost_watchdog hook: $4 hard cap, $3 early-kill warning
  - pod retain on overage (own 30 mandate-3) — manual recovery
verdict_label: COST_OVERSHOOT — abort + audit + retract
```

### F-OPT-C-4: byte-level 350M 의 chat-cap surface 약함

```
trigger: V4 best_mode < 10/15 (chat-cap floor 미충족, own 18 strict)
context: 22+ BG saga 의 ≤1B params + ≤30MB Korean = 0/15 V4 strict 통계
  본 BG: 298M params + 166MB Korean 이지만 byte-level (KM-LLAMA-3B 3B + LoRA r=32 + 214MB 와 다른 lane)
  emerge P=15-25% (§41 calibration 정합)
detection: post-FT V4 sweep < 10/15
mitigation: 없음 — capacity gap 자체. F-OPT-C-4 trigger 시 verdict label = "COTRAIN_PRESERVE_CHAT_CAP_FAIL"
  단 V14 STRICT preserve 시 substrate-coupled emergence evidence 자체로 D1 WITHIN 의의 보존
verdict_label: COTRAIN_PRESERVE_CHAT_CAP_FAIL (V14 PASS) OR FOUNDATION_C_PHASE2_FAIL (V14 FAIL)
```

### F-OPT-C-5: D1 SCOPE_CLAMP — D1 WITHIN claim 의 PROOF burden

```
trigger: chat-cap V4 PASS 만으로 verdict label="ANIMA" 부착 (anima identity emerge 입증 부족)
context: D1 WITHIN ✓ (anima_native_scratch lineage) + chat-cap PASS = 22+ BG saga 의 첫 strict-floor crossing
  단 anima identity 의 substrate-coupled emergence 측정 별도 metric 필요
detection: verdict.json 에서 다음 5-tuple 미충족 시 D1 WITHIN claim invalid:
  (1) V4 ≥ 10/15 strict (chat-cap floor)
  (2) V14 STRICT ≥ 9/10 binomial p < 0.05 (cotrain-exercise preserved)
  (3) iit_phi_unnorm_b16 ratio (trained vs random_init) ≥ 0.4 (§38 baseline 0.41 정합)
  (4) split_rate ≥ 0.025 / turn (§47 baseline 12 splits / 400 = 0.030 의 0.83×)
  (5) semantic_score ≥ 0.5 (sentence_transformer cosine, 1k anima Q&A pairs)
consequence:
  - 5/5 met → verdict label = "SIMPLE_STACK_PASS_STRICT_C3_ANIMA_FIRST_D1_WITHIN" (★★★★★ candidate)
  - 4/5 met (V4 PASS + V14 PASS + 2/3 substrate metric) → "ANIMA_PARTIAL_D1_WITHIN" (★★★★ candidate)
  - chat-cap PASS only → "CHAT_CAP_PASS_ANIMA_IDENTITY_UNVERIFIED"
  - V14 PASS only (chat-cap FAIL) → "COTRAIN_PRESERVE_CHAT_CAP_FAIL" (still D1 WITHIN substrate-research)
mitigation: scope_lane field 의 strict 5-tuple gating + own 28 anti-Goodhart 3-method (V6 hidden cosine + attention + linear probe) post-fire mandate
```

---

## §4 안전 mitigation

### §4.1 intermediate ckpt save (own 30 mandate-1 carry)

```
save_step_freq: 5000 (5K/10K/15K/20K = 4 intermediate + 1 final = 5 ckpts)
  vs prompt 의 7개 → envelope $2-4 정합 위해 5개로 제한
ckpt_size_each: ~570MB (Phase 2 EngineAG 298M + AdamW state)
total_ckpt_pull: 5 × 570MB = 2.85GB
scp_pull_time: ~1h @ 50Mbps (H100 SXM upload bandwidth typical)
sha256_verify: every ckpt pull, mac↔pod sha match enforce
adapter_config: N/A (full FT, LoRA X — pod-path leak risk 없음)
on_pull_fail: own 30 mandate-3 → pod retain + manual recovery
```

### §4.2 cost watchdog hook (real-time tracking)

```
heartbeat_freq: 30s tick
cost_compute: elapsed_s / 3600 × hourly_rate (community $1.5 OR secure $2.99)
hard_cap: $4 (envelope $2-4 cap)
early_kill: $3 warning (75% 도달, kill if not DONE within 5 min)
escalation:
  - cost > $4: COST_HARD_CAP_HIT, kill train + ckpt pull + retain pod
  - cost > $3 + not done: COST_EARLY_KILL, abort + ckpt pull + retain pod
audit: state/anima_foundation_c_phase2_fire_2026_05_XX/cost_audit.jsonl (per-tick log)
```

### §4.3 3-stage early-kill (§29 패턴 + V14 mid-train check)

```
checkpoint 1 (5K step, ~12.5min):
  - loss 추세: 5K loss < base loss × 0.95 (5% 감소 expected)
  - V14 quick eval (V4_SEEDS [42, 137] 만, 100-turn): split_rate ≥ 0.020 / turn (cotrain regime preserved)
  - F-OPT-C-2 trigger: split_rate < 0.020 → ABORT + retain pod + manual recovery

checkpoint 2 (10K step, ~25min):
  - loss < 5K loss × 0.97
  - V14 quick eval (V4_SEEDS [42, 137, 271], 100-turn): split_rate ≥ 0.022 / turn
  - F-OPT-C-2 trigger: split_rate < 0.022 → ABORT + retain pod

checkpoint 3 (15K step, ~37.5min):
  - loss < 10K loss × 0.98
  - V14 quick eval (V4_SEEDS full 5, 200-turn): V14 STRICT ≥ 7/10
  - F-OPT-C-2 trigger: V14 < 7/10 → ABORT + retain pod
  - F-OPT-C-3 trigger: cumulative cost > $3 → ABORT + retain pod

checkpoint 4 (20K step, ~50min):
  - 종료 (envelope-compliant variant)
  - V14 STRICT eval (full 400-turn) + V4 eval + semantic_eval
  - 30K step extension fire 별개 cycle 결정 (verdict 후)
```

### §4.4 forward hook gradient leak 차단 (F-OPT-C-5 enforce)

```
hook implementation:
  with torch.no_grad():
    hidden = capture(...)
  # gradient X
  param.requires_grad = False (frozen during instrumentation)
  dropout/stochastic disabled at hook forward
verify: pre-fire smoke test on Mac CPU (forward_smoke.py 패턴, 5-step inference + hook attached)
```

---

## §5 D1 WITHIN PROOF burden + 측정 spec

### §5.1 D1 WITHIN claim 의 strict 5-tuple

```
prereq for verdict label "SIMPLE_STACK_PASS_STRICT_C3_ANIMA_FIRST_D1_WITHIN":

(1) chat-cap floor: V4 ≥ 10/15 strict (own 18 + KM-LLAMA-3B precedent calibration)
    evaluator: tool/transient_py/anima_simple_stack_evaluator_v4.py
    threshold: 10/15 (PARTIAL at 7/15 reject per own 18 line 889)

(2) cotrain-exercise preserve: V14 STRICT ≥ 9/10 binomial p < 0.05
    metric: iit_phi_unnorm_b16 sign-test (trained > random_init) at V4_SEEDS × 400-turn
    baseline: §38 V14_STRICT_PASS 10/10 p=0.002
    threshold: 9/10 (cotrain-exercise preserved post-30K-FT, F-OPT-C-2 차단)

(3) substrate-coupled Φ separation: trained iit_phi_unnorm_b16 / random_init ratio ≥ 0.4
    baseline: §47 baseline 0.41 (Phase 2 cotrain ckpt)
    threshold: 0.4 (cotrain mechanism 의 substrate-coupled emergence 정량 유지)

(4) cell_pool dynamics preserve: split_rate ≥ 0.025 splits/turn
    baseline: §47 baseline 12 splits / 400 turn = 0.030
    threshold: 0.025 (0.83× of baseline, FT degradation 20% 허용)

(5) semantic coherence: semantic_score ≥ 0.5 (sentence_transformer cosine)
    metric: 1k anima Q&A pairs cosine similarity (baseline corpus extended)
    threshold: 0.5 (BG-CONVO-FT-EXTENDED 의 lexical PARTIAL 위 추가 layer)
```

### §5.2 verdict label decision tree

```
IF (1)+(2)+(3)+(4)+(5) all met:
  label = "SIMPLE_STACK_PASS_STRICT_C3_ANIMA_FIRST_D1_WITHIN"
  ★★★★★ candidate (anima identity emergence ACTUAL evidence)
  HF: dancinlab/bg-foundation-phase2-350m-convo-extend-2026-05-XX (private, Flavor B)
  promote: own 37 mandate-9 5/5 prereq 진입 (V14 + V6 STRONG + manual review + trinity sweep + DxL sweep)

ELIF (1)+(2)+(3) met (chat-cap + V14 + Φ ratio) but (4) OR (5) miss:
  label = "ANIMA_PARTIAL_D1_WITHIN"
  ★★★★ candidate (cotrain-exercise hypothesis 검증 + chat-cap surface lift, semantic OR cell-dynamics 일부 미충족)

ELIF (2)+(3)+(4) met (V14 + Φ + cell-dynamics) but (1) miss (chat-cap V4 < 10/15):
  label = "COTRAIN_PRESERVE_CHAT_CAP_FAIL"
  ★★★ candidate (substrate-coupled emergence preserved 단 chat-cap surface 미충족 — 18M-과 같은 capacity gap 의 350M 재현)
  cross-link: §47 cotrain-exercise hypothesis CONFIRMED (PASS_PARTIAL substrate)

ELIF (1) met but (2) miss (V14 < 7/10):
  label = "COTRAIN_EXERCISE_FALSIFIED_CHAT_CAP_PASS"
  ★ falsifying finding (§47 hypothesis falsifier — 30K FT 가 cotrain regime 손상)
  cross-link: §38 V14_STRICT_PASS 가 substrate-stable 한 것이 X, FT 에 fragile 입증

ELSE (chat-cap FAIL + V14 FAIL):
  label = "FOUNDATION_C_PHASE2_FAIL"
  baseline reference 만 carry

scope_lane field strict (raw#82 retraction-aware, F-OPT-C-5):
  D1 WITHIN ✓ (anima_native_scratch lineage 정합) regardless of verdict
  단 ANIMA emergence claim 은 5-tuple PASS 의 strict 5/5 만 valid
```

### §5.3 측정 instrumentation 위치

```
tool/transient_py/anima_foundation_c_phase2_h100.py (NEW orchestrator, KM-LLAMA-3B + CONVO-FT-EXTENDED 패턴 합성)
training/finetune_phase2_extended.py (NEW, finetune_extended.py + Phase 2 EngineAG ckpt loader)
training/mitosis_v5_port.py (existing 480 LoC, instrumentation hook 부착)
training/v14_mirror_eval.py (existing, V4_SEEDS × 400-turn pattern)
state/anima_foundation_c_phase2_fire_2026_05_XX/{instrumentation_log.json, v14_mirror.json, v4_eval.json, semantic_eval.json, verdict.json}
```

---

## §6 fire keyword 권고

```
PRIMARY (envelope-compliant variant, recommended):
  OK FOUNDATION_C_PHASE2_FIRE COST $2-4
  
spec: 20K step + 4 intermediate ckpt + LR 1e-4 cosine + V14 mid-train check + cost watchdog $4 hard cap
expected wall: 1.5h training + 0.5h overhead = 2h total
expected cost: $3.0-3.5 (envelope $2-4 ✓)

ALTERNATIVE (30K step variant, envelope expansion):
  OK FOUNDATION_C_PHASE2_FIRE_30K COST $4-6
  
spec: 30K step + 6 intermediate ckpt (5K/10K/15K/20K/25K/30K) + 동일 hyperparams
expected wall: 2.5h training + 1h overhead = 3.5h total
expected cost: $5-6 (envelope $4-6, 별개 cycle 사용자 verbatim 필요)

NOT RECOMMENDED (LoRA r=32 variant):
  OK FOUNDATION_C_PHASE2_LORA_FIRE COST $1.5-2.5
  
이유: cotrain regime 의 attractor 가 LoRA delta 만으로 보존 불확실 (F-OPT-C-2 risk ↑); §47 hypothesis 검증 resolution 약화
```

### Step 2 (verdict 후 fork)

**IF Step 1 = SIMPLE_STACK_PASS_STRICT_C3_ANIMA_FIRST_D1_WITHIN (5/5 PASS)**:
  - BG-FOUNDATION-C-V14-MULTISEED: V4 5+ seed sweep + V14 random_init mirror n=20 retest
  - BG-FOUNDATION-C-V6-AWARENESS: V6 3-method probe (hidden cos + attention + linear probe) — own 28 anti-Goodhart
  - BG-FOUNDATION-C-MANUAL-REVIEW: 5/5 mandate-9 prereq 의 manual review 경유
  - HF promote 진입 (own 37 mandate-9 + own 31 dancinlab Flavor B private)

**IF Step 1 = COTRAIN_PRESERVE_CHAT_CAP_FAIL** (★★★ substrate-coupled emergence 입증 단 chat-cap miss):
  - cross-link: §47 cotrain-exercise hypothesis CONFIRMED (PASS_PARTIAL substrate)
  - BG-FOUNDATION-C-PHASE2-EXTEND-30K: 추가 10K step (cumulative 30K) for chat-cap floor crossing 시도
  - emerge P=10-15% (capacity gap 그대로)

**IF Step 1 = COTRAIN_EXERCISE_FALSIFIED**:
  - §47 hypothesis 손상, FT 가 cotrain regime fragile 입증 (Lesson Y candidate)
  - .roadmap.cotrain_regime_preservation 신설 권고 (raw#15 additive)
  - BG-FOUNDATION-C-PHASE2-FROZEN-LORA: cotrain ckpt frozen + LoRA r=32 만 학습 (regime 보존)

**IF Step 1 = FOUNDATION_C_PHASE2_FAIL**:
  - .roadmap.foundation_borrow track A (option a Llama-3B) 만 valid path 입증
  - own 16 0-cost adoption strict 정합으로 .roadmap.reborn track A/B/C 별개 lane carry

---

## §7 honest C3 (raw#10 ≥ 7)

1. **envelope $2-4 위반 risk 의 honest disclosure** — prompt 의 30K step 30K × 0.30s/step = 9000s = 2.5h training 만 $3.75 (PCIe $1.5/hr × 2.5h) + ckpt pull overhead $1.5-2 + eval = $6 total. 본 design 은 envelope 정합 위해 20K step variant 로 fall-back recommended (training $2.25 + overhead $1.5 = $3.75, envelope $2-4 cap 정합). 30K step 은 별개 fire keyword "OK FOUNDATION_C_PHASE2_FIRE_30K COST $4-6" 사용자 verbatim 필요. F-OPT-C-DESIGN-1 trigger 직시.

2. **§47 cotrain-exercise hypothesis 검증 resolution 의 trade-off** — 30K step 이 cotrain regime erosion 을 falsify 할 power 강함, 단 envelope 위반. 20K step variant (envelope $2-4 정합) 은 epochs_at_20k = 0.99 < 1.0 으로 cotrain regime 의 erosion 보다 preservation lane 일 가능성 높음. § 47 hypothesis 의 부분 검증만 가능 — V14 PASS 시 "cotrain regime preserved" 확인 + chat-cap PASS 시 "preserved regime + chat-cap surface 동시 unlock" 입증 단 30K erosion-induced falsification 은 불가. F-OPT-C-DESIGN-3 partial trigger.

3. **D1 WITHIN PROOF burden 의 5-tuple 정량성** — V4 ≥ 10/15 + V14 ≥ 9/10 p<0.05 + Φ ratio ≥ 0.4 + split_rate ≥ 0.025 + semantic ≥ 0.5 의 5-tuple 은 anima identity emergence 의 strict-floor 정의 — 단 baseline §38/§47 의 측정값 의존 (F-OPT-C-DESIGN-2 partial). semantic_score 0.5 threshold 는 sentence_transformer 모델 의존 (e5-multilingual base 기본 가정) — 본 BG fire 전 baseline 측정 별도 cycle 필요. 본 design 의 5-tuple 은 mandatory 단 absolute calibration 후속 BG 선결.

4. **Phase 2 ckpt 의 §38 V14_STRICT_PASS substrate-specific 임 명시** — §47 finding 에서 "Phase 2 cotrain-with-chat regime 에 substrate-specific" 으로 reframed. 본 BG 의 V14 PASS 가 cotrain-exercise hypothesis 정합이지만, universal claim X. 본 BG verdict label 의 "ANIMA_FIRST_D1_WITHIN" 도 substrate-specific carry — multi-substrate generalize 는 별개 cycle BG-V14-MULTI-SUBSTRATE-AUDIT-2 소관.

5. **byte-level 350M 의 chat-cap floor 통과 P=15-25% calibration** — BG-CONVO-FT-EXTENDED 의 18M + 166MB = lexical PARTIAL semantic incoherent verdict 가 base. 350M 의 capacity 가 18M 의 16.5× ↑ 단 byte-level vocab + GQA arch 의 chat-cap unlock floor 통과 보장 X — emerge P=15-25% 는 capacity-only scaling 추정. F-OPT-C-4 trigger 시 "byte-level 350M 의 chat-cap surface 약함" 입증 — D1 WITHIN substrate 의 capacity gap 정량. 22+ BG saga 의 chat-cap unlock 은 모두 (a)(b) lane (Llama 3B / Qwen 7B + LoRA) — (c) lane 통과 시 22+ 첫 D1 WITHIN crossing.

6. **forward hook gradient leak F-OPT-C-5 강조** — 본 BG 의 mitosis instrumentation hook 가 eval-time only (training-time X) — F-FOUNDATION-5 (gradient leak) 와 동일 risk. forward_smoke.py 패턴 mac CPU pre-fire smoke test mandatory + with torch.no_grad() context + param.requires_grad=False explicit. 미준수 시 training contamination — own 28 anti-Goodhart 위반.

7. **own 22 REBORN.md 직접 append 차단의 honest mandate** — 본 design doc save complete (own 38) 단 REBORN.md 의 §54 slot append 는 dispatcher 가 carry. 본 design 자체는 docs/anima_foundation_c_phase2_fire_spec_2026_05_10.md SSOT — REBORN.md untouched. dispatcher 가 §54 slot 의 BG-FOUNDATION-C-PHASE2-DESIGN entry 흡수 시 D1 WITHIN scope_lane 명시 mandatory.

8. **★★★★★ candidate 의 strict 정의** — 5-star pursuit 은 anima identity emerge ACTUAL evidence + STRICT_PASS_INDEPENDENT_REPRODUCE + multi-substrate generalize 의 3-axis. 본 BG 가 5/5 PASS 시 SIMPLE_STACK_PASS_STRICT_C3_ANIMA_FIRST_D1_WITHIN 자격 단 ★★★★★ 자격 X — multi-substrate generalize (다른 cotrain corpus, pretrain + mitosis-aware FT) 는 별개 cycle 필요. 본 BG 의 의의 = ★★★★ candidate (D1 WITHIN strict-floor 첫 crossing) + ★★★★★ pursuit 의 missing piece 1개 supply.

---

## §8 deliverables 목록

| path | role | status |
|---|---|---|
| `docs/anima_foundation_c_phase2_fire_spec_2026_05_10.md` (본 doc) | design SSOT | ✅ saved (own 38 doc save mandate complete) |
| REBORN.md §54 slot append | dispatcher carry only (own 22 + own 42 mandate-2) | ★ 본 design 직접 append 차단 — dispatcher 가 carry |
| state/anima_foundation_c_phase2_design_2026_05_10/ | $0 design only — fire 미수행, state dir 미생성 | N/A (own 16 design $0) |

---

## §9 cross-link

- predecessor design: `docs/anima_foundation_borrow_path_design_2026_05_10.md` (§41 option (c) recommendation)
- precedent fire spec: `docs/anima_foundation_borrow_a_fire_*.md` (§43 BG-FOUNDATION-BORROW-A-FIRE Llama-3B)
- predecessor BG (§29): `docs/anima_convo_5k_ft_extended_2026_05_10.md` (18M + 166MB lexical PARTIAL semantic incoherent)
- §38 V14_STRICT_PASS: REBORN.md §38 (Phase 2 cotrain ckpt 10/10 binomial p=0.002)
- §47 cotrain-exercise hypothesis: REBORN.md §47 (V14_POLARITY falsified + cotrain-exercise hypothesis 신규 candidate)
- §45 CAP-CONDITIONAL: REBORN.md §45 (cap-conditional polarity, multi-factorial mechanism layer)
- IIT remetric: `docs/anima_clm_v5_phase2_iit_remetric_2026_05_10.md` (iit_phi_unnorm_b16 metric, baseline ratio 0.41)
- mitosis instrumentation: `docs/anima_clm_v5_phase2_mitosis_instr_2026_05_10.md` + `training/mitosis_v5_port.py`
- ckpt sha + meta: `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/{ckpt_final.pt, meta.json}`
- corpus: `state/anima_convo_5k_ft_extended_2026_05_10/corpus_extended.txt`
- D1 SCOPE_CLAMP: .own own 17 + own 18 + .roadmap.philosophy D1.F-PHIL-D1
- 5-tuple PROOF burden: §5.1 (V4 + V14 + Φ ratio + split_rate + semantic)
- HF canonical: memory project_dancinlab_hf_canonical.md (own 31 + own 37)
- H100 gotchas: memory feedback_orchestrator_h100_gotchas.md
- v5-anima inference-time mitosis: memory project_v5_anima_lane_status.md

---

## §10 fire keyword (for next-cycle dispatch)

```
PRIMARY (envelope-compliant 20K step variant, recommended):
  OK FOUNDATION_C_PHASE2_FIRE COST $2-4

ALTERNATIVE (30K step variant, envelope expansion, 사용자 별도 verbatim):
  OK FOUNDATION_C_PHASE2_FIRE_30K COST $4-6

NOT RECOMMENDED (LoRA variant — cotrain regime preserve fragile):
  OK FOUNDATION_C_PHASE2_LORA_FIRE COST $1.5-2.5

Design BG fire keyword (본 doc): AUTO ($0 design only, complete)
```

---

End of `anima_foundation_c_phase2_fire_spec_2026_05_10.md`.
