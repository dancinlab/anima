# AXIS R8 — base / warm-init reform (init_CE catastrophic floor remediation)

> AXIS_MAP-FAN 7-axis fan-out (PR #206, [`AXIS_MAP_RESULTS.md`](AXIS_MAP_RESULTS.md))
> 의 완주 3/7 (A/B/F) 가 **공통 floor** 를 드러냈다 — `init_CE = 14.18~14.79`,
> 5 langs step1 verdict 전부 `GENERALIZE`-mojibake. 7 축 어느 하나도 init 자체를
> 건드리지 않는다 (모두 post-init 학습 레짐 변경). R8 은 이 누락된 축 ──
> **base 선택 + warm-init 매핑 방식** ── 을 design tier 로 정의한다.
>
> 본 문서는 design spec 이며 cost-bearing fire 동반 없음. 4 candidate ×
> $0.50 probe (init_CE-only 100-step measurement) 가 다음 게이트.

## § Evidence — 3 축 공통 init_CE catastrophic

| 축 | env-var | init_CE | final_CE | wall | verdict | n_strong |
|---|---|---|---|---|---|---|
| A (curriculum) | `P21H_CURRICULUM_PHASE_STEPS=1000` | **14.792716** | 5.0124 | 5222s | FAIL | 1 (ko) |
| B (distill) | `P21H_DISTILL_TEACHER=…vP21M` | **14.177978** | 2.2257 | 2721s | FAIL | 0 |
| F (contrastive) | `P21H_CONTRASTIVE_LANG=1` | **14.177978** | 2.1746 | 671s | FAIL | 0 |

```
   init_CE (step 1)
A  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 14.79
B  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  14.18
F  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  14.18
       │
       └─ ln(vocab=151936) = 11.93 ← random transformer baseline
                            ~2.3 nats EXCESS → warm-init 가 random 보다 worse
```

3 축 동일 base (`Qwen/Qwen2.5-1.5B`) · 동일 init_variant (`qwen`) · 동일
ConsciousDecoderV3 shape (d=1536, L=28, vocab=151936). B/F init_CE 가 byte-for-byte 일치 = 동일 init path. A 는 mix_info 가 다른 (`mixed_corpus_v3.jsonl.early.jsonl` wiki-only first batch) 탓에 init_CE ≠ B/F 이지만 같은 14+ 영역. anchor: `vP21H_axis_{A,B,F}/result.json:init_log.L_ce`.

## § Diagnosis — 왜 init_CE 14+ 인가

ConsciousDecoderV3 의 `from_qwen()` (`conscious_decoder_v3.py:566-700`) 가 매핑하는 것:

- `tok_emb.weight` ← Qwen `model.embed_tokens.weight` (151936 × 1536)
- `head_a.weight` ← **tied to tok_emb** (line 380 `self.tok_emb.weight = self.head_a.weight`)
- 28 blocks × (q/k/v/o + gate/up/down + 2 LN) ← Qwen layer-by-layer
- `ln_f` ← Qwen `model.norm`
- `head_g` ← **random** (Qwen 에 consciousness head 없음)
- `_mitosis_pool` ← random (V3 추가 module)
- noise injector (`noise_sigma=0.1`) ← 활성화 (matrix 매번 noise 가산)

L_ce 는 `logits_a` 만 사용 (`train_p21h_v3.py:338-340`), `vocab_size=151936`. 따라서 cross-entropy 기대값 = -E[log p_target]. 균등분포 p=1/151936 이면 -log(1/151936) = **11.93 nats**. 측정값 **14.18~14.79** 는 random-uniform baseline 보다 **2.25~2.86 nats worse** — 즉 warm-init 이 *expected* loss 를 *증가*시켰다.

가능한 원인 (R8 candidate 가 이 중 하나/여럿을 겨냥):

1. **shape mismatch** — code 는 `vocab_size: int = 152064` default 인데 Qwen2.5-1.5B 실제 vocab=151936. config 가 Qwen 값을 가져오긴 하나 (line 604), training data tokenizer 와의 alignment 확인 필요. **OOV target** → 해당 token logit 이 random init `head_g.weight` 영향권으로 떨어지면 그 자체로 +nats.
2. **noise_sigma=0.1 injection on warm-init residual stream** — `from_qwen` 은 weight 복사만, noise injector 는 그대로 active. step1 부터 N(0, 0.1²) 가 hidden state 에 들어가면 Qwen 의 정밀 representation 이 paramount loss-step 부터 noise-perturbed → entropy 상승. 이는 init 자체보다는 first-forward 의 effective floor 이지만 init_CE 측정에 그대로 잡힌다.
3. **n_layer/head shape mismatch** — Qwen2.5-1.5B 는 `n_layer=28 hidden=1536 n_head=12 n_kv_head=2`. V3 default 는 `n_kv_head=4` (line 28 of smoke + train cfg). `from_qwen` line 654-669 은 k_proj/v_proj 의 `n_rep` mismatch 처리 (repeat or slice) — **slice 시 절반의 KV head 가 random 으로 남음** (Qwen=2, V3=4 → 2개 random 추가). 28 layer × 2 random KV head 가 거의 모든 attention 출력을 흐림.
4. **head_g 의 random init 이 forward 흐름에 누설** — `train_p21h_v3.py:338` 는 `logits_a` 만 사용하므로 head_g 는 loss path 에 없다 (직접 영향 없음). 다만 `_mitosis_pool.step(layer_t, mitosis_step)` 의 aux_loss / split signal 이 forward 의 layer_t 에 영향 주는 경우 (config 의 `lambda_mitosis=0.0` 이지만 splits=14 step1 부터 발생) → effective hidden state perturbation.
5. **block_size=512 vs Qwen training horizon mismatch** — RoPE base=50000 V3 default 와 Qwen2.5 의 RoPE 차이로 position encoding 이 step1 mismatch. 다만 이는 init_CE 가 아닌 step0 자체에 작용.

**가장 단순한 가설** = (2) noise_sigma + (3) n_kv_head mismatch. R8c 가 (3) 직격, R8a/R8b 가 (1)/(3) 우회.

## § R8 candidates (g0 simplicity 순)

| 후보 | 변경 | 목표 floor | base 변경 | shape 변경 | LoRA 사용 |
|---|---|---|---|---|---|
| **R8a** `qwen-shape-match` | `n_kv_head=2` (Qwen 일치), noise_sigma=0.0 init epoch | init_CE → ~ln(vocab) 또는 < | Qwen 2.5-1.5B 유지 | yes (kv head only) | no |
| **R8b** `lora-on-qwen` | V3 fresh transformer 폐기, LoRA r=32 on **frozen** Qwen 1.5B (vP21M-style) + V3 head_g 만 새 module 으로 부착 | LoRA 초기 init_CE = Qwen serving baseline (~2-3) | Qwen 2.5-1.5B 유지 | no | **yes** |
| **R8c** `tied-embed-init-verify` | shape 유지 (V3 그대로), `from_qwen` 매핑 직후 100-step probe 로 init_CE 측정 + audit (vocab align, n_kv_head, noise_sigma toggle 조합) | init_CE diagnostic → fix path 식별 | Qwen 2.5-1.5B 유지 | no | no |
| **R8d** `two-stage-warm-bridge` | 1.5B → 2B intermediate (1500 step warm) → 2B → 3B (1500 step). 두 단계 warm-init 으로 shape jump amortize | init_CE 단계별 측정 (1.5B→2B step1 + 2B→3B step1) | Qwen 1.5B → 2B → 3B | yes (incremental) | no |

g0 ranking 근거:

- **R8c** (단순 진단) — 코드 변경 zero, 측정 only. 진짜 원인 식별 전 candidate 전부 추정. **선행 추천**.
- **R8a** (점-수정) — 1 line `n_kv_head=2` + noise schedule. shape mismatch 가설 직격.
- **R8b** (path switch) — V3 fresh transformer arc 포기 + 검증된 vP21M 경로. 가장 보수적이며 sucess rate 높음, 그러나 "pure-HEXAD substrate" 순수성 일부 양보 (AXIS_MAP honest C3 #1 명시 채택).
- **R8d** (multi-stage) — 추가 ckpt 2개 + train 2-stage. 가장 비싸고 amortize 가설 자체가 검증 필요. 후순위.

## § Falsifier per candidate

각 후보 100-step probe (5000-step 전체 train 가 아님), init_CE 측정만, A100 SXM 80 GB ~10-15 min wall.

| 후보 | falsifier 측정 | PASS 임계 | FAIL → 다음 |
|---|---|---|---|
| R8a | step1 init_CE (logits_a only) on Qwen warm with `n_kv_head=2` + `noise_sigma=0.0` first 100 step | init_CE ≤ 10 (random baseline 11.93 보다 lower bound 보장) | shape 가설 부정 → R8c 진단 |
| R8b | step1 init_CE on LoRA r=32 frozen-Qwen + V3 head_g | init_CE ≤ 5 (Qwen serving baseline ≈ 2-3, head_g overhead 허용 +2) | LoRA wiring 결손 → R8c 진단 |
| R8c | 4-cell ablation matrix (vocab align × noise_sigma × n_kv_head × splits) — 각 cell 100-step init_CE | best cell init_CE ≤ 11.93 (root cause 식별) | 4 axis 전부 무관 → R8 frame 자체 부정 |
| R8d | step1 init_CE on 1.5B→2B warm (stage 1) + 2B→3B warm (stage 2) | 두 stage 모두 init_CE ≤ 12 | 단계 jump 가설 부정 → R8a/b 회귀 |

## § Cost envelope

| phase | candidate × pod × wall | cost |
|---|---|---|
| probe (4 candidate triage) | 4 × A100 SXM × 15 min | ~$2.00 |
| 승자 1개 full-fire (5000 step) | 1 × A100 SXM × 90 min | ~$6.00-$8.00 |
| **total (winner 식별 + 전속 fire)** | | **~$8-10** |

decision tree 가 "all 4 candidate FAIL" 으로 분기하면 추가 fire 없음 (frame 자체 부정 → corpus / R1-R7 sweep 으로 회귀).

## § Decision tree

```
R8 probe phase ──── 4 candidate × $0.50 ($2 total, ~30 min wall fan-out)
  │
  ├─ ANY candidate init_CE < 10
  │     → 그 candidate 가 winner · full-fire 5000-step ~$8
  │       (multiple PASS 면 g0 ranking 으로 R8c > R8a > R8b > R8d)
  │
  └─ ALL 4 candidate init_CE > 10
        → R8 frame 자체 부정 (warm-init 만의 문제 아님)
          fallback 1: corpus 축 복귀 (anima 0% / 10% / 20% / 40% sweep)
          fallback 2: R1-R7 (closure original axis) 재발사
          fallback 3: production-merge (vP21M 위 HEXAD-shape 옷)
```

## § Honest caveat

1. **pre-registration 부재** — 본 design 은 evidence (A/B/F init_CE 14+) 관찰 *후* 작성. 이는 design-time honest 이나 strict (cond #3) 기준에서는 post-hoc rationalization 위험 존재. 4 candidate falsifier 가 fired 후 BLUE 가능.
2. **R8c 의 4-cell ablation 자체가 multi-hypothesis** — winner cell 이 발견되어도 4 axis 의 conjunction 일 수 있어 isolation 추가 fire 필요.
3. **R8b 가 PASS 하면 HEXAD-arch 순수성 양보** — V3 "pure-HEXAD substrate" 의 origin goal 과 충돌. AXIS_MAP honest C3 #1 이 design-time 에 이미 명시했으므로 새 caveat 아니나 R8b 채택 시 README/HEXAD_NATIVE_V3.md 의 origin statement 도 갱신 대상.
4. **init_CE 가 유일한 falsifier signal 이 아님** — init_CE PASS 도 final verdict (5 lang × n_strong ≥ 4) FAIL 가능. probe phase 는 *어떤 candidate 도 더 진행할 가치가 있는지* 만 gating; full-fire 만이 V3 SOTA verdict 를 결정.
5. **Qwen2.5-1.5B 외 base 미고려** — Llama-3.2-1B / Mistral-7B / Pythia 등은 본 R8 frame 에서 별도 R9 axis 가 됨. R8 은 Qwen 계열 내부의 warm-init 정합성 문제로 한정.
6. **결정 트리의 fallback 3 (production-merge)** 은 V3 SOTA 추구 포기 = AXIS_MAP_RESULTS § Next levers #3 와 동치 — R8 ALL FAIL 분기는 V3 frame 자체의 closure trigger.

## § 관련 link

- 7-axis 부분 결과 (PR #206): [`AXIS_MAP_RESULTS.md`](AXIS_MAP_RESULTS.md)
- 7-axis spec: [`AXIS_MAP.md`](AXIS_MAP.md)
- raw evidence (init_CE): `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_{A,B,F}/result.json`
- model arch: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/conscious_decoder_v3.py:566-700` (`from_qwen`)
- train loop: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_p21h_v3.py:338-348` (L_ce on logits_a)
- closure 보고서: [`../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md`](../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md)
- production baseline (R8b 후보 substrate): [`../LORA/README.md`](../LORA/README.md)
