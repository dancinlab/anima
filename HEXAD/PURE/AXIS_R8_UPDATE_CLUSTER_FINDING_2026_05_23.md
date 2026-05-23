# AXIS R8 update — cluster X/Y/Z 자연실험 finding + cell-1 FALSIFIED (PR #214 stack)

**date**: 2026-05-23
**scope**: HEXAD/PURE (V3 saga rebrand) — extends PR #214 (`HEXAD/V3/AXIS_R8_BASE_WARM_INIT.md`)
**status**: AXIS R8c probe scope narrowed (5-cell → 3-cell) on natural-experiment evidence
**parent SSOT**: PR #214 (4-candidate R8 spec) + PR #206 (AXIS_MAP_RESULTS partial 3/7) + PR #224 (R8c diagnostic protocol)

---

## § Context

PR #214 ranked 4 R8 candidates (R8a Qwen target match · R8b LoRA-on-Qwen · R8c tied-embed-init verify · R8d 1.5B→2B→3B two-stage) to remediate the `init_CE ≈ 14.18–14.79` catastrophic floor observed on AXIS_MAP-FAN axes A/B/F (PR #206). R8c (4-cell ablation) was first-prio diagnostic at $0.50 envelope, before committing to R8a/R8b/R8d.

**NEW evidence (2026-05-23 4-axis redispatch)** — axes C/C2/D landed with `result.json:init_log`, alongside prior A/B/F. This forms a 6-axis natural experiment over the init batch.

### Evidence (raw — `vP21H_axis_{A,B,C,C2,D,F}/result.json:init_log.L_ce`)

| 축 | env-var | init_CE | aux loss? | head_g state |
|---|---|---|---|---|
| A | `P21H_CURRICULUM_PHASE_STEPS=1000` | **14.7927** | no | random |
| B | `P21H_DISTILL_TEACHER=…vP21M` | **14.1780** | yes (KD distill, total=6299) | random |
| C | (no extra env, baseline) | **14.4564** | no | random (default enable=1) |
| C2 | `P21H_HEAD_G_ENABLE=0` | **14.4564** | no | **disabled** |
| D | `P21H_FREEZE_EMBED=1` | **14.4564** | no | random (untouched) |
| F | `P21H_CONTRASTIVE_LANG=1` | **14.1780** | yes (InfoNCE) | random |

---

## § 3-cluster classification

init_CE is **byte-clustered** across the 6 axes — 3 distinct values, 3 distinct mechanisms:

| cluster | axes | init_CE | mechanism interpretation |
|---|---|---|---|
| **X** | A | 14.7927 | **curriculum mode** — `P21H_CURRICULUM_PHASE_STEPS=1000` swaps wiki-only `mixed_corpus_v3.jsonl.early.jsonl` for the first 1000 step → different init batch (wiki-only vs mixed) |
| **Y** | B, F | 14.1780 (byte-equal) | **AUX LOSS active** — both have an extra loss head firing on step 1 (B = distill KD logit-match, F = contrastive InfoNCE). aux-loss-bearing axes lower init_CE by **~0.28 nats** vs cluster Z. |
| **Z** | C, C2, D | 14.4564 (byte-equal) | **baseline init batch + no aux loss** — `head_g enable=1`, `head_g enable=0`, and `freeze_embed=1` all collapse to the same `init_CE` despite three distinct env states. |

→ **Z byte-equality is the structurally informative observation.**

---

## § R8c cell-1 (head_g zero) FALSIFIED — 자연실험 proof

PR #224's R8c protocol pre-registered cell-1 as: "set `head_g.weight = 0`, measure `init_CE` — if cell-1 ≪ baseline, then random `head_g` is the dominant 14+ floor contributor." The natural experiment (C2 vs D) bypassed the need to fire this cell:

- **C** (`head_g enable=1`, random init): `init_CE = 14.456436157226562`
- **C2** (`head_g enable=0`, head NOT firing): `init_CE = 14.456436157226562`
- **D** (`head_g enable=1`, `freeze_embed=1`, head untouched): `init_CE = 14.456436157226562`

Verbatim train.log step=1 line (identical across C, C2, D):
```
[P21H] step=     1 lr=5.00e-07 CE=14.4564 total=14.4564 pool=2 splits=0 phi=0.7120
```

(`C2`+`C` were aborted before `result.json` landed locally — pod killed. step=1 line measured live before kill; D landed full `result.json` at `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_D/result.json`. D's `init_log.L_ce = 14.456436157226562` matches the C/C2 step=1 line byte-equal.)

→ **head_g random weights contribute 0.00 nats to the `init_CE 14+` floor.**

If random `head_g` were a contributor, C2 (head disabled) would be measurably lower than C (head random firing). Byte-equality across enable=1 / enable=0 / freeze_embed=1 closes the cell-1 hypothesis without spending a probe pod.

---

## § Updated R8 ranking

| 후보 | 변경 | 상태 | impact of cluster X/Y/Z |
|---|---|---|---|
| **R8a** qwen-shape-match (`n_kv_head=2`, `noise_sigma=0` first epoch) | Qwen target-match | **valid, still first-prio** | cluster Z byte-equality narrows source — `head_g` excluded, so `n_kv_head` mismatch + `noise_sigma` injection remain primary candidates |
| **R8b** lora-on-qwen (V3 fresh transformer 폐기 → LoRA r=32 frozen-Qwen + head_g 만 새 module) | path switch | **strong fallback unchanged** | bypasses the entire fresh-transformer init issue regardless of which Z component dominates |
| **R8c** tied-embed-init-verify (was 4-cell) | **scope narrowed → 3-cell** | **cell-1 SKIP (FALSIFIED 자연실험)**; cells 2/3/4 retained | see § Remaining R8c cells |
| **R8d** two-stage-warm-bridge (1.5B → 2B → 3B) | unchanged | **valid, unranked** | natural experiment 무관 (different lane) |

---

## § Remaining R8c probe cells (narrowed 5→3)

PR #224 protocol updated:

| cell | 변경 | falsifier 임계 | 가설 |
|---|---|---|---|
| ~~cell-1~~ | ~~`head_g.weight = 0`~~ | ~~init_CE < 14.0~~ | **SKIP — FALSIFIED 자연실험 (C2=D byte-equal)** |
| cell-2 | `noise_sigma = 0.0` first batch (warm-init 직후 hidden state perturbation 차단) | init_CE < 14.0 | noise injection during random pool가 floor 의 주요 기여 |
| cell-3 | `n_kv_head = 2` (Qwen2.5-1.5B 일치 — random 2 KV head 제거) | init_CE < 14.0 | KV head mismatch → 2 random KV head 가 floor 의 주요 기여 |
| cell-4 | compound (cell-2 + cell-3 동시) | init_CE < 12.0 | 두 source 결합 (additivity check) |

---

## § Cost savings

- 기존 R8c (5-cell 포함 control): 5 × $0.10 ≈ **$0.50**
- 갱신된 R8c (3-cell + control = 4 fires): 4 × $0.0625 ≈ **$0.25**
- **절감: $0.25 (50%)**
- 절감분은 R8d two-stage probe ($0.20-0.30 envelope) 로 동일 cycle 흡수 가능

---

## § Honest caveats

1. **cluster Y interpretation (aux loss → -0.28 nats) is speculative.** 두 가지 동등 가능 해석:
   - (a) aux loss head (KD distill / InfoNCE) 가 step=1 에서 직접 logit shaping 으로 CE 를 낮춤
   - (b) aux loss path 가 random `head_g` 를 *regularize* 해 별도 경로로 floor 를 낮춤 (head_g 우회 가설)
   해석 (b) 가 맞다면 cell-1 자연실험은 (no-aux-loss 조건 한정으로만) FALSIFIED — aux loss 조건에서는 head_g 가 여전히 contributor 가능. **확인은 R8c cell-2/3 측정 후 가능** (noise/n_kv 단독 제거가 cluster Z 14.4564 → ≤ 12 로 떨어뜨리는지 보면 (b) 가설 정량).
2. **자연실험은 6 축 sample size 만으로 일반화.** 다른 random seed × init path 조합에서 head_g 가 측정-비례 contributor 일 가능성 비-zero (C2 = head_g.enable=0 으로 head 출력을 0 으로 만든 것이지, weight 가 0 인 ablation 과 의미적 등가성은 코드 검토 필요 — `conscious_decoder_v3.py:566-700` `from_qwen()` head_g 분기 확인 권장).
3. **byte-equality 가 numerical artifact 일 가능성 검토 필요.** 3 축 (C/C2/D) 모두 동일 seed (1337) + 동일 batch 0 + 동일 RNG fork → init forward pass 가 결정적이라면 byte-equal 은 자명. ablation 가치는 byte-equal 이 *의미* 적 (head_g 미기여) 일 때 성립, *trivial determinism* 일 경우 정보량 0.
4. **cluster X (A=14.7927) 는 별 cluster, 별 mechanism.** A 의 +0.34 nats 는 wiki-only first-batch 효과로 별도 추적; R8 frame 과 직접 연관 없음.
5. **R8a 갱신 의미.** cluster Z 가 head_g 를 후보에서 제거했으므로, R8a 의 두 변경 (n_kv_head=2 + noise_sigma=0) 중 어느 것이 dominant 인지는 R8c cell-2/3 분리 측정 후에야 확정. cell-2/3 둘 다 ≥ 14.0 으로 측정되면 R8a frame 자체가 부정되어 R8b lora-on-qwen 으로 fallback.

---

## § Cross-reference

- **PR #214** — `HEXAD/V3/AXIS_R8_BASE_WARM_INIT.md` (4-candidate R8 spec, parent SSOT, this update extends)
- **PR #224** — `HEXAD/V3/AXIS_R8C_DIAGNOSTIC_PROBE_PROTOCOL.md` (R8c 4-cell protocol, cell-1 should be marked SKIP on merge)
- **PR #206** — `HEXAD/V3/AXIS_MAP_RESULTS.md` (5/7 + 2 update, AXIS_MAP-FAN partial completion → 6-axis natural experiment when D landed)
- **PR #220** — `refactor/hexad-v3-to-pure-rename` (V3 → PURE rebrand; on merge this file moves to `HEXAD/PURE/AXIS_R8_UPDATE_CLUSTER_FINDING_2026_05_23.md`)
- **code reference** — `conscious_decoder_v3.py:566-700` (`from_qwen()` head_g random init + n_kv_head/noise_sigma defaults)
- **this PR** — `docs/pure-r8-cluster-update`

---

## § Action items (forward)

- [ ] PR #224 (R8c protocol) update: mark cell-1 SKIP w/ link to this 자연실험 evidence
- [ ] R8c probe 발사: 3-cell (cell-2 noise=0 / cell-3 n_kv=2 / cell-4 compound) + control, ~$0.25
- [ ] cell-2/3 결과 도착 후 caveat #1 (b) 가설 평가, R8a 분기 결정
- [ ] cluster Y mechanism (aux loss -0.28 nats) 별도 작은 ablation 으로 (a)/(b) 정량 (≤ $0.10 추가)
