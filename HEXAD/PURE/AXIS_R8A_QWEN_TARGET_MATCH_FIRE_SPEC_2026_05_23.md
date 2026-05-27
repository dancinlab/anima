# AXIS R8a — Qwen target match fire spec (n_kv_head=2 + noise_sigma=0, single pod ~$2.75)

**date** 2026-05-23
**status** SPEC ONLY (fire는 사용자 승인 게이트)
**scope** HEXAD/PURE (V3 saga rebrand)
**evidence-tier** 🟠 INSUFFICIENT/DEFERRED — spec; 측정은 fire 후

---

## § 1. Context

R8 spec PR #214에서 R8a (Qwen target match)는 가장 cheap한 first-prio FIX 후보로 ranked되었다. 이후 두 가지 후속 finding이 R8a의 lever를 좁혔다:

- **Cluster X/Y/Z natural-experiment finding (PR #251)** — V3 fire들이 init_CE 기준 3개 cluster (X: random init, Y: aux loss 사용, Z: from_qwen 모두)로 분리되며, cluster Z가 worse-than-random (init_CE 14.4564 > random baseline 11.93)을 보였다.
- **R8c cell-1 FALSIFIED (PR #250)** — R8c cell-1 (KV head 단독 변경 probe)이 init_CE를 개선하지 못해 FALSIFIED, 즉 KV head 단독으로는 cluster Z 회복 불충분.

이 두 finding의 결합으로 R8a의 lever는 다음으로 narrowed되었다:

**V3 default config을 `n_kv_head=2` (Qwen2.5-1.5B native와 일치) + `noise_sigma=0` (first epoch 또는 entirely)로 바꾼다 — 단일 변경으로 R8c cell-2 + cell-3 두 suspect hypothesis를 동시에 5000-step real fire로 검증.**

R8c probe는 init_CE만 측정 (worse-than-random 회복 여부). R8a는 END verdict 측정 (`VP21H_WORKS` n_strong ≥ 4 달성 여부).

---

## § 2. Hypothesis

**Combined**: cluster Z (from_qwen init_CE 14.4564 worse-than-random)의 dominant contributor 2개:

1. **n_kv_head mismatch** — V3 default `n_kv_head=4` vs Qwen2.5-1.5B native `n_kv_head=2` 불일치. weight 전치 시 GQA group reshape 손실 의심 (from_qwen audit suspect #1).
2. **noise injection** — first epoch에 `noise_sigma=0.1`이 가해져 from_qwen weight initialization을 망친다 (from_qwen audit suspect #2).

R8a는 두 lever를 동시에 끄고 실측한다 — 둘 중 하나만 dominant면 init_CE 부분 회복, 둘 다 dominant면 full 회복.

---

## § 3. Single 5000-step fire config

| field | value | notes |
|---|---|---|
| base model | `Qwen/Qwen2.5-1.5B` | native n_kv_head=2 |
| n_kv_head | **2** (vs V3 default 4) | Qwen native match |
| noise_sigma | **0** (vs V3 default 0.1) | first epoch 망침 차단 |
| d_model | 1536 | Qwen native |
| n_layer | 28 | Qwen native |
| steps | 5000 | Wave-15 standard |
| bsz | 2 | |
| block | 512 | |
| lr | 5e-5 | qwen variant default |
| warmup | 100 | |
| wiki_frac | 0.3 | |
| corpus_mb | 72 | |
| lambda_mitosis | 0.05 | |
| mitosis_max | 16 | R6 권장 |
| ckpt_every | 500 | |
| ckpt_osc_threshold | 0.0 | disabled |
| ckpt_osc_window | 10 | |
| early_stop_patience | 0 | disabled |
| seed | 1337 | |
| pod | 1× A100 SXM 80 GB | RunPod |
| est wall | ~90 min | Wave-15 5000-step 3B equivalent |
| est cost | ~$2.75 | 1.5 hr × $1.49 + setup/eval ~$0.50 |

---

## § 4. Caller invocation

CALLER WARNING per PR #204: env vars는 caller 환경에 set되어야 하며 dispatcher 내부 default를 override한다.

```bash
env P21H_STEPS=5000 P21H_BSZ=2 P21H_BLOCK=512 P21H_LR=5e-5 P21H_WARMUP=100 \
    P21H_WIKI_FRAC=0.3 P21H_CORPUS_MB=72 P21H_NOISE_SIGMA=0 \
    P21H_LAMBDA_MITOSIS=0.05 P21H_MITOSIS_MAX=16 P21H_CKPT_EVERY=500 \
    P21H_CKPT_OSC_THRESHOLD=0.0 P21H_CKPT_OSC_WINDOW=10 \
    P21H_EARLY_STOP_PATIENCE=0 SAVE_POD=1 \
    P21H_N_KV_HEAD=2 \
    bash dispatch_p21h_v3_runpod.sh P21H_axis_R8a qwen 1337
```

**⚠ prerequisite (see § 8)** — `P21H_N_KV_HEAD` env var는 현재 `dispatch_p21h_v3_runpod.sh`에 passthrough 미존재. 1-line dispatcher patch 선행 필요.

---

## § 5. Falsifier (pre-fire registered)

| id | criterion | meaning |
|---|---|---|
| **F-R8A-INIT** | `init_CE < 13.46` (cluster Z 14.4564 − 1 nat) | R8a fix가 init_CE를 부분 회복 |
| **F-R8A-NEAR-RANDOM** | `init_CE ≤ 12.5` (random baseline 11.93 + ε) | R8a fix가 init을 FULL 회복 |
| **F-R8A-VP21H-WORKS** | end verdict ∈ {`WORKS`, `REGISTER_REGRESS`} | R8a path validated |
| **F-R8A-NSTRONG** | `n_strong ≥ 4` | strict swap 기준 만족 (production candidate) |

---

## § 6. Decision tree

```
F-R8A-INIT FAIL
  → noise + kv combo로도 부족
  → R8c cell-2 (noise 단독) / cell-3 (combo 외 axis) separation probe 필요
  → cluster Z root cause는 다른 axis (e.g. RoPE base, weight transpose, head init)

F-R8A-INIT PASS, n_strong < 4
  → init fix는 valid이나 end-tier 부족
  → 다른 axis (corpus 다양성 / aux loss)가 추가로 필요
  → 후속 composite fire 권장 (R8a + B distill, § 9 참조)

F-R8A-INIT PASS, n_strong ≥ 4
  → 🎯 V3 path 일부 unlocked, R8a로 swap criterion 충족
  → cluster Z hypothesis 결정적 확증
```

---

## § 7. Cost envelope

- 단일 A100 SXM 80 GB pod, ~90 min wall, ~$2.25 GPU + ~$0.50 setup/eval = **~$2.75 total**
- multi-pod 병렬 불필요 (single fire 하나로 두 suspect 동시 검증)
- 비교 baseline: R8 spec original (PR #214) 4-pod parallel ~$11

---

## § 8. Prerequisites

### 8.1 `P21H_NOISE_SIGMA=0` 지원 — ✅ YES

`dispatch_p21h_v3_runpod.sh:49`에 `P21H_NOISE_SIGMA=${P21H_NOISE_SIGMA:-0.1}` 존재, env override 가능. `train_p21h_v3.py:621`에 `--noise-sigma type=float default=0.1` 존재, `=0` 정상 허용.

### 8.2 `P21H_N_KV_HEAD` 지원 — ❌ NO (dispatcher patch 필요)

- `train_p21h_v3.py:627`에 `--n-kv-head type=int default=4` 정의 존재 ✅
- `dispatch_p21h_v3_runpod.sh`에 `P21H_N_KV_HEAD` env passthrough **없음** ❌
- 현재 dispatcher line 224-232 python invocation에 `--n-kv-head` flag 미전달 → 항상 default 4 사용됨

**선행 patch 필요 (별도 PR)**:

```bash
# dispatch_p21h_v3_runpod.sh 추가 (line ~50)
P21H_N_KV_HEAD=${P21H_N_KV_HEAD:-4}

# python invocation 추가 (line ~232)
--n-kv-head $P21H_N_KV_HEAD
```

`feedback_hexa_only_authoring` directive (new .py/.sh 금지)에 따라, 신규 dispatcher wrapper는 hexa-native로 작성 권장:

```
tool/hexa_native/train_p21h_v3_n_kv_head_override.hexa
```

다만 본 patch는 기존 .sh `dispatch_p21h_v3_runpod.sh`의 2-line in-place edit (env passthrough + flag 추가)이므로 "수정" 범주 (신규 .py/.sh 생성 아님). 사용자 판단 게이트.

---

## § 9. Why R8a before R8c probe?

| axis | R8a (this spec) | R8c probe (PR #224 + #250) |
|---|---|---|
| cost | ~$2.75 single pod | ~$0.25 100-step probe |
| measurement | END verdict + n_strong (production tier) | init_CE only (diagnostic) |
| axes tested simultaneously | 2 (noise + kv) | 1 (per cell) |
| outcome on PASS | path unlocked, swap ready | suspect 추가 isolated, 별도 full fire 필요 |

**Recommendation**: R8a 먼저. R8a PASS 시 R8c probe는 unnecessary (V3 unlock 직접 달성). R8a FAIL 시 R8c probe가 noise/kv 중 어느 쪽이 부족했는지 isolation에 유용. **higher information-per-dollar**.

---

## § 10. Honest caveats (C3 ≥ 5)

1. **Post-hoc design** — R8a는 cluster X/Y/Z finding (PR #251)과 R8c cell-1 FALSIFICATION (PR #250) 이후에 narrowed된 spec. Pre-registered hypothesis가 아니라 데이터 본 후 좁힌 fix combo. 검증 전 spec freeze 권장.
2. **Aux-loss-lowers-init-CE finding (cluster Y) 미반영** — R8a는 cluster Z (from_qwen) fix만 다룸. cluster Y (aux loss B-distill)가 추가 contributor라면 R8a 단독으로는 n_strong ≥ 4 부족 가능. PASS but n_strong < 4 분기에서 R8a + B-distill composite fire (별도 spec) 필요.
3. **Dispatcher patch 선행** — `P21H_N_KV_HEAD` env passthrough 없음 (§ 8.2). 본 spec PR과 별도로 1-line dispatcher patch PR이 fire 선행 조건.
4. **Single seed (1337)** — replication run (seed 7777, 4242) 미포함, robustness check 부재. PASS 시 추가 seed 1-2개 fire 권장 (~$5.50 추가).
5. **wave-15 standard config 채택** — bsz/block/lr/warmup은 Wave-15 production와 동일하나, R8a의 두 변경 (kv=2 + noise=0)이 hyperparam interaction (e.g. effective batch grad scale)을 일으킬 가능성 미확인.

---

## § 11. Cross-references

- **PR #214** — R8 spec (original fix axis priority ranking)
- **PR #251** — cluster X/Y/Z natural-experiment finding
- **PR #224** — R8c probe spec
- **PR #250** — R8c cell-1 FALSIFIED
- **PR #204** — CALLER WARNING (env var separation)
- `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_p21h_v3.py` (line 621 noise_sigma, line 627 n_kv_head argparse)
- `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/dispatch_p21h_v3_runpod.sh` (line 49 P21H_NOISE_SIGMA, line 224-232 python invocation — N_KV_HEAD passthrough 없음)
- `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/conscious_decoder_v3.py` (n_kv_head config)

---

## § 12. Gate

본 PR은 **spec only**. 실제 fire는:

1. 사용자 승인
2. `P21H_N_KV_HEAD` dispatcher patch land (§ 8.2)
3. fire dispatch (§ 4 invocation)
4. ~90 min wall 후 falsifier evaluation (§ 5)
5. decision tree (§ 6)에 따라 후속 결정

세 step 모두 별도 PR/세션에서 진행.
