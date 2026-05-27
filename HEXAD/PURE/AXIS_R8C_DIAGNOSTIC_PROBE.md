# AXIS R8c — diagnostic probe protocol (4-cell ablation, init_CE measurement, $0.50)

> path = V3 (AXIS_MAP-FAN R8 cluster) · status = PROTOCOL SPEC (no fire) · ranking = first move per `AXIS_R8_BASE_WARM_INIT.md` (PR #214)

## § Premise

`AXIS_MAP_RESULTS.md` (PR #206) 의 A/B/F 축 fire 에서 관측된 init_CE = 14.79 / 14.18 / 14.18 nats 는 균일분포 random baseline `ln(151936) = 11.93` 보다 **+2.3 ~ +2.9 nats 더 나쁘다**. 이는 "warm-init 이 불완전" 수준이 아니라 **구조적 버그** — warm-init pipeline 어딘가에서 random 보다 못한 적극적 손상이 일어나고 있다는 신호다. R8c probe 는 R8a / R8b / R8d full-fire 에 commit 하기 전, 손상의 단일 dominant source 가 다음 4 후보 중 어느 것인지 (또는 복합인지) 100-step 짧은 측정으로 분리한다 — head_g random init / `_mitosis_pool` random init / `noise_sigma=0.1` injection / n_kv_head Qwen=2 ↔ V3 default=4 repeat-interleave mismatch.

## § 4-cell ablation matrix

| cell | head_g | _mitosis_pool | noise_sigma | n_kv_head | expected init_CE |
|---|---|---|---|---|---|
| baseline (axis A reproduction) | random | random | 0.1 | 4 | ~14.79 (reproduce) |
| cell-1 (head_g zero) | zero | random | 0.1 | 4 | TBD |
| cell-2 (no noise) | random | random | 0 | 4 | TBD |
| cell-3 (kv-head match) | random | random | 0.1 | 2 | TBD |
| cell-4 (all 3 combined) | zero | random | 0 | 2 | TBD |

각 cell 은 동일 corpus / seed / step-count 로 sequential 실행 — single-source attribution 을 위해 한 번에 한 axis 만 toggle, cell-4 만 compound. `_mitosis_pool` 은 4 cells 전부에서 random 으로 고정 (별도 분리는 R8d scope, 본 probe 범위 밖).

## § Falsifier (registered before fire)

* **F-R8C-BASELINE** — baseline cell 의 init_CE 가 axis A 의 14.79 nats 와 ±0.1 nats 이내로 재현. FAIL 시 env-drift 가 나머지 4 cell 결과를 오염시키므로 probe 전체 무효.
* **F-R8C-HEAD-G** — cell-1 init_CE delta from baseline ≥ 1 nat → head_g random emission head 가 dominant source.
* **F-R8C-NOISE** — cell-2 init_CE delta ≥ 1 nat → `noise_sigma=0.1` exploration noise injection 이 dominant.
* **F-R8C-KV-HEAD** — cell-3 init_CE delta ≥ 1 nat → n_kv_head repeat-interleave (Qwen 2 → V3 4) 가 dominant.
* **F-R8C-COMPOUND** — cell-4 init_CE < baseline − 2 nats → 3 patch 결합 시 누적 복구 (random baseline 11.93 nats 부근까지 도달하면 strong).

## § Probe protocol (100-step training, NOT full 5000)

* 1× A100 SXM 80 GB pod (single-pod sequential, no parallel — 5 cells 모두 동일 hardware/driver 보장)
* corpus = axis A 와 동일 (`corpus_s101` + `multi_wiki`, `wiki_frac=0.30`)
* per cell = 100 steps, sequential on same pod → 5 cells × 100 step ≈ 500 step total ≈ 100 s wall (model build + ckpt eject 제외)
* 측정점 = `init_log.L_ce` (step 1) + L_ce at step 50 + L_ce at step 100 — per cell 3 datapoint
* artefact = `probe_results.json` (5 cells × 3 measurement points + per-cell config snapshot + seed + env hash)

## § Code changes required (BEFORE fire — separate PR)

* `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/probe_r8c_diagnostic.py` 신규 — 5-cell driver, 본 PR 에서 작성하지 않음 (별도 code PR).
* `train_p21h_v3.py` patch — `--probe-cells <list>` arg 또는 `PROBE_CELLS` env 수용, per-cell head_g/noise/n_kv_head override 노출. 본 PR 에서 작성하지 않음 (별도 code PR).
* 본 PR 은 protocol/doc only — 코드 작성 + 발사는 user approval 게이트 이후.

## § Dispatch caller (correct env-var separation per PR #204)

```
env PROBE_CELLS=baseline,head_g_zero,no_noise,kv_head_match,compound \
  PROBE_STEPS=100 SAVE_POD=1 \
  bash dispatch_p21h_v3_runpod.sh P21H_r8c_probe qwen 1337
```

`SAVE_POD=1` 은 dispatch script default 유지 (probe 결과 의외 시 pod 보존하여 수동 재실행). seed=1337 은 axis A reproduction 위해 동일 seed 사용.

## § Cost envelope

~100 s wall × 5 cells = 500 s ≈ 9 min compute + 5 min setup (Qwen download + tokenizer + dispatch).
A100 SXM 80 GB on runpod ≈ $1.49/hr.
$1.49 × (9 + 5) / 60 ≈ **~$0.35 total** (envelope $0.50 으로 보수).

## § Decision tree

* **any single cell crosses init_CE < 12.5 nats** → 그 cell 의 fix 가 R8 winner → R8a full-fire (5000 step) 로 escalate
* **no cell crosses 12.5** → R8c FALSIFIED, V3 warm-init path 의 단일 dominant bug 가설 기각 → R8b (LoRA-on-Qwen, V3 arch 우회) 가 first move 로 강등
* **cell-4 compound 만 crosses, 단일 cell 은 not** → 3 contributor 가 모두 부분 기여 → R8a 는 3 patch 를 동시에 적용해야 함 (head_g zero + noise off + kv_head match 묶음)

## § Honest caveats (≥3, pre-registered)

1. probe horizon = 100 step → init 단계의 구조적 손상만 감지. training dynamics (later-stage divergence, mitosis split-thr 거동) 는 미측정 — R8a full-fire 5000 step 가 actual verdict.
2. `_mitosis_pool` random init 은 4 cell 전부 고정 → 만약 `_mitosis_pool` 자체가 dominant source 이면 probe 가 그 가설을 falsify 불가. R8d 가 별도 cell 로 분리.
3. axis A reproduction (cell baseline) 이 ±0.1 nats 안에 안 들어오면 (F-R8C-BASELINE FAIL) corpus / tokenizer / dtype / Qwen revision drift 등 env-side contamination 이 의심 — 그 경우 5 cell 결과 전부 deferred 처리, env-pin (Qwen sha256 + corpus sha256 + torch version) 후 재실행.
4. Qwen `num_key_value_heads=2` ↔ V3 default `n_kv_head=4` mismatch 시 V3 코드는 `repeat_interleave(rep=2, dim=0)` 로 KV head 를 복제 (`conscious_decoder_v3.py:660-675`). cell-3 은 V3 `n_kv_head=2` 로 강제하여 repeat 자체를 우회 — 측정되는 것은 "repeat 가 손상의 원인인가" 이지 "GQA group size 자체가 손상의 원인인가" 가 아님.
5. random uniform baseline 11.93 nats 는 untrained Qwen forward (Qwen tokenizer + Qwen weights, no V3 surgery) 에서 직접 검증된 적 없음 — F-R8C-COMPOUND 의 "random 부근" 비교 기준은 이론값 ln(151936). probe 결과 해석 시 절대값 vs 상대 delta 둘 다 같이 보고.

## § Out of scope

* 본 PR 은 protocol spec 만. probe driver 코드 (`probe_r8c_diagnostic.py`) + train patch (`train_p21h_v3.py`) + 실제 GPU 발사는 분리된 후속 PR + user approval 게이트 이후.
* R8a / R8b / R8d 사양은 `AXIS_R8_BASE_WARM_INIT.md` (PR #214) 에 보존. R8c 결과가 다음 cycle 의 axis 선택을 결정.
