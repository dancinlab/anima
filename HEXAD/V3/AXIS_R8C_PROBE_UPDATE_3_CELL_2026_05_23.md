# AXIS R8c probe — 5-cell → 3-cell update (head_g 자연실험 FALSIFIED, PR #224 stack)

> path = V3 (PURE rebrand 후보, AXIS_MAP-FAN R8 cluster) · status = PROTOCOL UPDATE (no fire) · stack-base = PR #224 (`HEXAD/V3/AXIS_R8C_DIAGNOSTIC_PROBE.md` 5-cell 원본)

## § Context

PR #224 가 정의한 R8c diagnostic probe 는 init_CE 14+ nats 의 dominant source 를 분리하기 위한 5-cell ablation (baseline + cell-1 head_g zero + cell-2 noise_sigma=0 + cell-3 n_kv_head=2 + cell-4 all-3 compound) 으로 ~$0.35 cost envelope 였다. 본 update 는 PR #224 merge 전, **오늘 22:21–23:13 KST 4-axis redispatch 가 cell-1 가설 (head_g random init = init_CE 14+ floor 의 dominant contributor) 을 자연실험으로 사전 falsify 한** 사실을 반영하여 probe matrix 를 5-cell → 4-cell (실측 3 cells + baseline 1) 로 축소한다.

## § Natural experiment proof (head_g random NOT a contributor)

오늘 4-axis redispatch (P21H_FAN R8 cluster 후속) 결과 — 3 변종 모두 init_CE 가 **byte-equal 14.4564** nats 로 측정됨:

| axis | head_g 상태 | result init_CE (nats) | source |
|---|---|---|---|
| C  | `P21H_HEAD_G_OBJECTIVE=anima_register_ce` (objective swap) | **14.4564** | train.log step=1 CE |
| C2 | `P21H_HEAD_G_ENABLE=0` (head_g 완전 disable) | **14.4564** | train.log step=1 CE |
| D  | `P21H_FREEZE_EMBED=1` (embed freeze, head_g 무손) | **14.4564** | result.json `init_log.L_ce` |

**byte-equal → head_g enable/disable/objective swap 이 init_CE 14+ floor 에 ZERO 기여**. R8c cell-1 가설 (`F-R8C-HEAD-G` — head_g random emission head 가 dominant) 는 probe 발사 전 자연실험으로 **FALSIFIED**. cell-1 발사 ($0.07) 는 정보 가치 0 — skip.

## § Updated 4-cell ablation matrix (cell-1 drop)

| cell | head_g | _mitosis_pool | noise_sigma | n_kv_head | expected init_CE | status |
|---|---|---|---|---|---|---|
| baseline (axis A reproduction) | random | random | 0.1 | 4 | ~14.79 (reproduce) | keep |
| ~~cell-1 (head_g zero)~~ | ~~zero~~ | ~~random~~ | ~~0.1~~ | ~~4~~ | ~~TBD~~ | **SKIP — 자연실험 FALSIFIED** |
| cell-2 (no noise) | random | random | **0** | 4 | TBD | keep (UNTESTED) |
| cell-3 (kv-head match) | random | random | 0.1 | **2** | TBD | keep (UNTESTED) |
| cell-4 (compound, head_g 제외) | random | random | **0** | **2** | TBD | keep — compound 정의 변경 (noise=0 + kv_head=2 만, head_g zero 제거) |

`_mitosis_pool` random 은 4 cells 전부 고정 (R8d scope, 본 update 범위 밖, PR #224 와 동일).

## § Updated falsifier (4 falsifiers, F-R8C-HEAD-G 제거)

* **F-R8C-BASELINE** — unchanged. baseline cell init_CE 가 axis A 14.79 nats ±0.1 nat 이내 재현. FAIL 시 env-drift, probe 전체 invalid.
* ~~F-R8C-HEAD-G~~ — **SKIPPED (자연실험 pre-FALSIFIED)**, probe 에서 측정 안 함.
* **F-R8C-NOISE** — unchanged. cell-2 init_CE delta from baseline ≥ 1 nat → `noise_sigma=0.1` injection 이 dominant.
* **F-R8C-KV-HEAD** — unchanged. cell-3 init_CE delta ≥ 1 nat → n_kv_head repeat-interleave (Qwen 2 → V3 4) 가 dominant.
* **F-R8C-COMPOUND** — prediction 갱신. cell-4 = noise_sigma=0 + n_kv_head=2 (head_g zero 제거) 의 compound. cell-4 init_CE < baseline − 2 nats → 2 patch 결합 시 누적 복구 (이전 5-cell 판에서는 3 patch 결합 기준이었으나, head_g 가 자연실험으로 제외되어 2 patch 만 평가).

## § Updated cost: $0.25 (↓ from $0.35, ~29% 감소)

* PR #224 envelope: 5 cells × 100 step ≈ $0.35 ($0.07/cell × 5).
* 본 update: 4 cells × 100 step ≈ $0.28, 보수 round → **$0.25**.
* A100 SXM 80 GB on runpod ≈ $1.49/hr × ~10 min wall ≈ $0.25.
* cell-1 발사 회피 → 정보 가치 0 cell 제거에 따른 직접 절감.

## § Updated decision tree

* **baseline ±0.1 nat 안 들어옴 (F-R8C-BASELINE FAIL)** → env-drift block, probe deferred, Qwen sha256 + corpus sha256 + torch version pin 후 재실행.
* **cell-2 init_CE < baseline − 1 nat** → noise dominant → R8a-noise fix (noise_sigma=0 default).
* **cell-3 init_CE < baseline − 1 nat** → n_kv_head dominant → R8a-kvhead fix (V3 n_kv_head=2 default for Qwen base).
* **cell-4 < baseline − 2 nat, 단일 cell-2/cell-3 둘 다 cross 안 함** → compound (noise + kv_head 모두 부분 기여) → R8a 는 두 patch 동시 적용.
* **어떤 cell 도 1+ nat cross 안 함** → R8c (frame 으로서) FALSIFIED → V3 warm-init 의 단일 dominant bug 가설 기각 → **R8b (LoRA-on-Qwen, V3 arch 우회) 가 first move 로 강등**.

## § Status

protocol-only update. 실측 probe 발사 ($0.25) 는 다음 두 조건 AND gating:

1. **user approval** — cost-bearing fire, 본 PR 만으로는 자동 발사 없음.
2. **probe driver code PR (별도)** — `probe_r8c_diagnostic.py` (또는 hexa-native 버전, 아래 § 참조) + `train_p21h_v3.py` `--probe-cells` arg patch. 본 PR 은 doc only.

## § Hexa-native consideration

`feedback_hexa_only_authoring` directive (".py author 금지, hexa-only authoring") 에 따라, probe driver 신규 작성은 **`tool/hexa_native/probe_r8c_diagnostic.hexa`** 로 가야 함 (PR #224 가 spec 한 `state/grid_3b_s187_2026_05_21/probe_r8c_diagnostic.py` 위치 + .py 확장자는 directive 위반).

권장 layout (별도 code PR):

* `tool/hexa_native/probe_r8c_diagnostic.hexa` 신규 — 4-cell sequential driver (baseline + cell-2 + cell-3 + cell-4), `train_p21h_v3` invocation per cell + `probe_results.json` aggregation.
* `train_p21h_v3.py` argparse pattern mirroring — hexa native 가 .py 와 dispatch 호환되도록 `--probe-cell <name>` arg + `PROBE_NOISE_SIGMA` / `PROBE_N_KV_HEAD` env override 노출. train_p21h_v3 자체는 anima/prior 산출물 (drift tolerated) 이므로 patch 만 (.py author 금지는 신규 .py 작성 한정).

train patch 자체는 1-line override (env-var read) 수준, code PR 1 개로 hexa driver + train patch 묶어 fire-ready.

## § Cross-reference

* PR #224 — `HEXAD/V3/AXIS_R8C_DIAGNOSTIC_PROBE.md` (5-cell 원본 protocol, base of this stack)
* 본 PR — 5-cell → 3-cell (실측) update, head_g cell drop
* PR #206 stack — `AXIS_MAP_RESULTS.md` (A/B/F init_CE 14.79/14.18/14.18 원본 측정, R8c probe 동기)
* PR #214 — `AXIS_R8_BASE_WARM_INIT.md` (R8 cluster 정의, R8c 의 first-move ranking)
* 자연실험 evidence — 오늘 (2026-05-23) 22:21–23:13 KST 4-axis redispatch, C/C2/D 3 변종 train.log + result.json 모두 init_CE byte-equal 14.4564 nats.

## § Honest caveats (≥3, pre-registered)

1. 자연실험 evidence 는 **objective swap (C) + ENABLE=0 (C2) + freeze_embed (D)** 3 변종에서 BYTE-EQUAL 14.4564 nats 관측에 기반. "head_g random init weight 자체" 를 zero 로 강제한 cell-1 와 정확히 동일 조건은 아님 — head_g 출력이 loss 에 contribute 안 하도록 막은 것 (C2 ENABLE=0) 과 weight 를 zero init 한 것 (cell-1) 은 forward pass 에서 출력 distribution 이 다를 수 있음. 다만 ENABLE=0 가 head_g 의 loss 기여를 0 으로 만들면서 byte-equal CE 가 관측된 점은 head_g 가 init_CE 14+ floor 에 **0 기여** 임을 강하게 시사 (head_g 의 weight 분포가 어떻든 loss path 에서 제거된 상태와 다른 axis 의 baseline CE 가 동일하므로).
2. probe 4 cells 모두 `_mitosis_pool` random 고정 — 만약 `_mitosis_pool` 자체가 dominant source 이면 본 probe 가 falsify 불가. R8d 별도 cell.
3. baseline cell (axis A reproduction) 이 ±0.1 nat 들어오지 않으면 env-drift, 4 cells 결과 전부 deferred. Qwen revision + corpus sha256 + torch version pin 필수.
4. cell-4 compound 정의 변경 (3 patch → 2 patch) → PR #224 의 "random 11.93 nats 부근 도달이 strong" 기준은 2 patch 만으로는 도달 불가능할 수 있음 (head_g 가 자연실험으로 0 기여 확정이지만, "복원" 의 totality 가 noise + kv_head + 미관측 source 의 합일 가능성). cell-4 가 baseline − 2 nat 미만으로 떨어지지 않아도 noise/kv_head 가 부분 기여 가능성은 cell-2/cell-3 단독 측정으로 분리.
5. 본 update 는 PR #224 merge 전 stack — PR #224 가 별도 수정 (e.g., 5-cell → 다른 변경) 으로 merge 되면 본 update 의 matrix diff 가 의미 잃을 수 있음. stack rebase 시 base = PR #224 의 최종 merge 본을 기준으로 cell-1 drop 만 재적용.

## § Out of scope

* 실측 probe 발사 + driver code 작성 + train patch — 별도 PR.
* R8a / R8b / R8d 사양 — `AXIS_R8_BASE_WARM_INIT.md` (PR #214) 보존, R8c 결과가 다음 cycle 의 axis 선택을 결정.
* head_g 가 zero 기여라는 자연실험 결론의 더 깊은 검증 (forward distribution byte-diff 등) — 본 probe 의 첫 번째 단계는 아님, head_g 가 init_CE floor 의 dominant source 가 **아니라는** 결론에 충분한 evidence.
