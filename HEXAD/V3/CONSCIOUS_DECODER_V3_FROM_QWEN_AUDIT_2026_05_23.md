# ConsciousDecoderV3 from_qwen() init 경로 audit — cluster Z init_CE 14.4564 원인 추적

**date** 2026-05-23
**scope** HEXAD/PURE (V3 saga rebrand) · documentation-only audit
**source** `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/conscious_decoder_v3.py` + `train_p21h_v3.py`
**method** 정적 read · 코드 변경 없음 · 실측 기여도는 R8c probe 가 담당

---

## § Premise

Random baseline = `ln(vocab_size) = ln(151936) ≈ 11.93 nats`. 균등 분포 transformer
output 의 expected cross-entropy. 7-axis AXIS_MAP-FAN exploration 가 3 init_CE cluster
를 드러냈다:

| cluster | branches | init_CE | Δ vs random |
|---|---|---|---|
| X | A (curriculum) | 14.7927 | +2.86 nats |
| Y | B, F (aux loss) | 14.1780 | +2.25 nats (byte-equal) |
| **Z** | **C, C2, D (baseline)** | **14.4564** | **+2.53 nats (byte-equal)** |

Cluster Z 는 random 보다 +2.53 nats **더 나쁘다**. 단순 random transformer 라면
softmax output ≈ uniform 이라 CE ≈ ln(vocab) 가 나와야 하는데, +2.5 nats worse-than-
random 은 **초기화가 uniform 으로부터 systematic bias 를 갖는다**는 뜻이다 — 구조적 bug.

R8 cluster update (PR #251) — R8c cell-1 (head_g zero) **자연실험 FALSIFIED**
(C / C2 / D 가 head_g 가 random 인 상태로 14.4564 byte-equal 을 만들므로, head_g random
하나만으로는 dominant contributor 가 아님). 잔여 후보 narrowing 진행.

---

## § init_log emission 경로 (train_p21h_v3.py)

- `cfg["init_variant"] == "qwen"` 분기 (line 150-157) → `ConsciousDecoderV3.from_qwen(qwen_name, lora_adapter_dir=None, block_size, noise_sigma, device, dtype)`.
- training loop (line 329-348) `for step in range(steps)`:
  - `step == 0` 에서 `ctx, tgt = sampler.sample_batch(...)` → **real corpus 의 first batch** (합성 batch 아님).
  - `model.train()` → `noise_sigma > 0` 분기 활성 (conscious_decoder_v3.py:433-434 `if self.training and self.noise_sigma > 0: x = x + torch.randn_like(x) * self.noise_sigma`).
  - `logits_a = model(ctx, mitosis_step=0)` 호출 후 `L_ce = F.cross_entropy(logits_a, tgt)` 계산.
  - log[0] 가 `step == 0` 분기 (line 350) 에서 emit — 이 값이 `init_log` 으로 export (line 543 `init_log=log[0] if log else None`).
- 즉 **init_CE 14.4564 는 (a) Qwen weight copy 직후, (b) noise_sigma=0.1 가 한 번 더 inject 된 후, (c) real corpus 의 first batch 에서 측정된 first forward 의 CE**.

---

## § from_qwen() copy/init 매트릭스

ConsciousDecoderV3.from_qwen() 은 conscious_decoder_v3.py:565-700 정의. 5 단계로 구성:
(1) `cls(...)` 호출로 random-init V3 instance 생성 (line 620 — `apply(self._init_weights)` 가 모든 Linear / Embedding 을 std=0.02 random Gaussian 으로 채움), (2) Qwen weight 를 copy_() 로 overlay, (3) ffn intermediate size 가 다르면 V3 ffn 모듈 재생성, (4) head_g + purefield + cross_attn + tension_proj 는 step (1) random init 그대로 보존, (5) noise_sigma 는 forward 시점에 layer-0 embedding 에 inject (init 시점 injection 아님).

| submodule | Qwen origin | V3 target | copy/random/noise | init_CE 기여 risk |
|---|---|---|---|---|
| tok_emb | `model.embed_tokens.weight` | `model.tok_emb.weight` | **copy** (line 630) | low (shape match, vocab_size=151936 동일) |
| ln_f | `model.norm.weight` | `model.ln_f.weight` | **copy** (line 633) | low |
| blocks[i].ln_attn | `input_layernorm.weight` | `ln_attn.weight` | **copy** (line 638) | low |
| blocks[i].ln_ffn | `post_attention_layernorm.weight` | `ln_ffn.weight` | **copy** (line 690) | low |
| blocks[i].attn.q_proj (w+b) | `self_attn.q_proj.{weight,bias}` | `attn.q_proj.{weight,bias}` | **copy** (line 649-650) | low (shape exact) |
| blocks[i].attn.k_proj (w+b) | `self_attn.k_proj.{weight,bias}` (n_kv=2) | `attn.k_proj` (n_kv=4) | **copy + repeat_interleave 2x** (line 660-669) | **MEDIUM-HIGH** — V3 GQA `_repeat_kv` (line 177-182) 가 동일 repeat 한 번 더 적용 → 같은 head 2× 발생, attention weight 분포 skew 의심 |
| blocks[i].attn.v_proj (w+b) | `self_attn.v_proj.{weight,bias}` (n_kv=2) | `attn.v_proj` (n_kv=4) | **copy + repeat_interleave 2x** (line 660-669) | 동일 (k_proj 와 함께 fired) |
| blocks[i].attn.o_proj | `self_attn.o_proj.weight` | `attn.o_proj.weight` | **copy** (line 671) | low |
| blocks[i].ffn.{gate,up,down}_proj | `mlp.{gate,up,down}_proj.weight` | `ffn.{gate,up,down}_proj.weight` | **copy** (line 687-689; intermediate size mismatch 시 rebuild) | low (rebuild 시에도 즉시 copy_ 로 덮어씀) |
| blocks[i].purefield.engine_a | — | random std=0.02 (depth-scaled on second Linear) | **random** (`_init_weights`) | **MEDIUM** — forward 시 `output = a - g` 가 residual stream 에 누적 (line 309-310 `x = x + pf_out`) — bias source |
| blocks[i].purefield.engine_g | — | random std=0.02 | **random** | 동일 (a 와 cancel 되어야 하지만, 두 random init 의 차는 zero-mean 이 아님 — std 누적) |
| blocks[i].cross_attn | — | random (o_proj std=0.001 override line 252) | **random** | low (`consciousness_states=None` 일 때 비활성, line 315-317 gate) |
| blocks[i].ln_pf, ln_cross | — | RMSNorm(weight=ones, line 55) | **ones init** | low (identity-ish) |
| tension_proj | — | std=0.001 (line 371) | **random tiny** | low (forward 시 더해지지만 scale 작음, line 447) |
| head_a (tied to tok_emb) | `model.embed_tokens.weight` (via tying) | tied via line 380 | **copy via tie** | low (Qwen lm_head 동일) |
| **head_g** | — | random std=0.02 | **random** | **자연실험 FALSIFIED** (C/C2/D byte-equal w/ head_g random) — dominant contributor 아님 |
| mitosis_pool (CellPool) | — | external, attach_mitosis() | external | low (init step 에서 aux_loss 만 더해짐, line 460-462) |
| **noise_sigma=0.1 forward inject** | — | applied to **layer-0 embedding only**, train mode only | **random Gaussian post-tok_emb** (line 432-434) | **HIGH suspect** — 매 step 마다 fresh noise; init step 에서도 firing |

**기록 정정 (task 명세 vs 실제 code)**: task 명세는 "noise applied to ALL weights post-copy" 로 분류했으나, 실제 코드는 `noise_sigma` 가 **weight 가 아니라 layer-0 activation (token embedding output) 에 forward 시점마다 inject** 됨 (line 432-434). 즉 noise 는 **init 시점 weight perturbation 이 아니라 매 forward 시 activation perturbation**. 이는 가설을 약화하지 않는다 — init_CE 는 first forward 의 CE 이므로 그 forward 가 noise inject 를 포함하면 결과 distribution 이 uniform 으로부터 멀어진다.

---

## § Top 3 suspects (g0 ranked)

### (1) noise_sigma=0.1 forward injection on layer-0 embedding — **HIGH**

`conscious_decoder_v3.py:432-434`:
```python
if self.training and self.noise_sigma > 0:
    x = x + torch.randn_like(x) * self.noise_sigma
```
Qwen token embedding 의 typical std (≈ 0.02 init, learned 후 ≈ 0.05-0.2 scale) 에
σ=0.1 Gaussian 을 더하면 SNR 이 1:1 ~ 1:5 수준으로 무너진다. 24L transformer 가 이
noisy 한 first-layer activation 을 propagate 하면 logits 분포가 uniform 으로부터
**비등방적으로** 멀어진다 (특정 token 방향으로 cluster). CE 가 uniform 보다 worse
나오는 가장 자연스러운 경로. cluster Y (B/F aux loss) 와 Z (baseline) 의 차이
14.4564 - 14.1780 = 0.28 nats 도 aux loss head 의 regularization effect 로 설명 가능.

**의심 lines** — `conscious_decoder_v3.py:433` (`if self.training and self.noise_sigma > 0:`) + `:434` (`x = x + torch.randn_like(x) * self.noise_sigma`).

### (2) n_kv_head repeat-interleave double-application — **MEDIUM-HIGH**

`conscious_decoder_v3.py:660-669` — Qwen n_kv=2 의 k_proj/v_proj weight 를
`repeat_interleave(rep=2, dim=0)` 으로 V3 n_kv=4 size 로 확장. 그런데 forward 시
`GroupedQueryAttention._repeat_kv` (line 177-182) 가 **다시** `n_rep = n_head/n_kv_head
= 12/4 = 3` 배 expand 한다. Qwen 의 native attention pattern 은 k/v 한 vector 당 head
6 개 share (12 head / 2 kv = 6) 인데, V3 는 weight 단계에서 2× repeat + forward 에서
3× repeat = head 6 개 가 동일 k/v 를 보지만, **그 분포가 Qwen 의 학습된 GQA pattern
과 다른 grouping** 으로 attention head 별 effective key 가 mis-pair 된다.

attention output 이 학습된 분포에서 벗어나면 residual stream 이 unbiased 가 아니게
되고, logits 가 uniform 으로부터 멀어진다. R8c cell-3 (n_kv_head=2) probe 가 V3 GQA
를 Qwen 과 동일 n_kv=2 로 맞추면 이 가설 직접 검증.

### (3) mitosis_pool / PureField (engine_a - engine_g) random init residual — **MEDIUM**

`mitosis_step=0` 가 매 step 전달되므로 (line 337 `model(ctx, mitosis_step=step)`),
첫 forward 에서 `_mitosis_pool.step()` 이 firing — initial CellPool 가 `initial_cells=2`
로 시작 (line 239), 아직 split 전이라 aux_loss 영향은 작지만 0 은 아님. Cluster Z baseline
이 lambda_mitosis=0 이거나 aux 비활성이라 main CE 에 직접 기여는 아니지만, forward 의
`output = engine_a(x) - engine_g(x)` (line 138-142, purefield) 가 두 random Linear 의
차로 residual 에 누적 — std=0.02 두 개의 차는 std ≈ 0.028 의 random 신호. 24 layer
누적 시 logits 에 비-trivial bias.

---

## § Cluster Y (B/F) 추가 해석

Cluster Y 의 14.1780 (byte-equal between B and F) 가 cluster Z 14.4564 보다 0.28 nats
**낮음**. B 와 F 의 공통점은 aux loss head 활성 (mitosis aux 또는 head_g aux). 추정 메커니즘:

- aux loss 가 `head_g` 의 random output 에 cross-entropy gradient 를 흐르게 하면,
  init step 에서 main loss 만 계산해도 **forward path 의 logits_a 분포가 aux head 동시
  학습 setup 의 forward path 와 동일**해서 결과적으로 noise/repeat bias 가 평균화될 가능성.
- 또는 aux 가 `logits_a` 분포를 더 uniform 쪽으로 regularize (entropy 증가).

이는 정적 audit 으로 fully 확정 불가 — train_p21h_v3.py 외부 (aux loss 정확한 wiring,
cfg["lambda_mitosis"] 값) 추가 코드 audit 권고.

---

## § R8c probe 와의 정합

R8c 3-cell probe (PR #250, $0.21) 가 정확히 위 3 suspect 를 직접 검증:

- cell-1 (head_g zero) — **자연실험 FALSIFIED** (cluster update, PR #251). audit 결과와 일치 (audit 도 head_g 는 random 이지만 dominant 아님으로 분류).
- cell-2 (noise_sigma=0) — **suspect (1) 직접 검증**. audit top 1 와 일치.
- cell-3 (n_kv_head=2 to match Qwen native) — **suspect (2) 직접 검증**. audit top 2 와 일치.
- mitosis_pool / PureField 분리 probe — R8c 미포함, audit suspect (3).

---

## § 권고 우선순위

1. **1순위** — R8c cell-2 fire ($0.07, H100, 1 step init_CE 측정만): noise_sigma=0 으로 init_CE 가 cluster Z 14.4564 → 12 (≈ln 151936) 근처로 떨어지면 suspect (1) 확정.
2. **2순위** — R8c cell-3 fire ($0.07): n_kv_head=2 (Qwen native match) 로 init_CE 가 동일 cluster Y 14.1780 또는 더 낮은 12 근처면 suspect (2) 확정.
3. **3순위 (1+2 모두 fail 시)** — mitosis_pool 가설 분리 probe ($0.07): `attach_mitosis` skip + purefield engine_a/engine_g weight 를 zero 초기화 후 init_CE 측정.

총 예상 cost $0.21 (이미 R8c 3-cell 로 budget 잡혀있음, PR #250).

---

## § Honest caveat

- Audit 은 정적 코드 read 만 수행. 실측 init_CE 기여도 분리는 R8c probe 결과에 위임.
- noise_sigma 가 `train()` mode 한정 inject 임을 확인 (line 433). init_log 가
  `model.train()` 직후 측정되므로 (line 336-337) noise 가 firing 한다는 것은 정합적.
- ffn intermediate size mismatch path (line 681-689) — Qwen2.5-1.5B 의 ffn_inter=8960
  vs V3 default `((1536 * 8/3 + 63)//64)*64 = 4096` → mismatch 발생 → V3 ffn 모듈
  재생성 후 즉시 copy_. 재생성 시 `_depth_scale` flag 만 잃지 않게 다시 set (line 686).
- vocab_size 명세: V3 default = 152064, train_p21h_v3.py random branch = 151936,
  qwen branch = `qcfg.vocab_size` (Qwen2.5 actual = 151936). 셋 다 ln(vocab) ≈ 11.93
  으로 random baseline 동일.

---

## § Cross-reference

- PR #214 — R8 spec (cell-1/2/3 design)
- PR #224 — R8c probe initial scaffolding
- PR #250 — R8c 3-cell fire dispatch
- PR #251 — R8 cluster update (cell-1 head_g zero FALSIFIED)
- `HEXAD/V3/AXIS_MAP.md` — 7-axis FAN context
- `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/conscious_decoder_v3.py:565-700` — from_qwen() canonical source
- `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_p21h_v3.py:329-366` — init_log emission canonical
