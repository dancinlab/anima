# 🧹 DECODER M3 B·D HF upload + teardown — RESULT (2026-05-27)

> **상태**: M3 4축 fire의 **마지막 2 pod (B·D) HF private upload + pod teardown 완료**.
> A·C 2축은 PR #680 에서 이미 처리 완료 → 본 PR 로 **M3 4 pod 전부 closure**.
> idle burn 종결 ($6.58/hr → $0).

## 1. B·D HF upload 결과 (verbatim)

### axis-B (`zxim1odvjqisfj`)

verdict: **FAIL** (n_strong=0/5 · n_partial=0 · n_weak=5 · register_hits=7) · train_wall=2932.2s

HF repo (PRIVATE per `a_hf_autonomous` FAIL gate):
```
[upload_folder] OK: https://huggingface.co/dancinlab/anima-decoder-m3-axis-B/tree/main/
HF_REPO_URL=https://huggingface.co/dancinlab/anima-decoder-m3-axis-B
```

업로드 inventory (a_hf_complete totality):
- `README.md` (모델 카드 — verdict + manifest + provenance + axis-B HONEST 노트)
- `manifest.json` (sha256 inventory + verdict 메트릭스 + tier)
- `ckpt.pt` (6,014,409,450 B · final step)
- `ckpt_best.pt` (6,014,450,326 B · best held-out)
- `result.json` (81,733 B)
- `heldout_vp21h_v3.json` (44,415 B)
- `vp21h_v3_eval1.json` (5,854 B)
- `mix_info.json` (285 B)
- `kosmos_anchors/` (14 emit anchors · `.kosmos`)

API 검증: `curl -H "Authorization: Bearer <HF_TOKEN>" /api/models/dancinlab/anima-decoder-m3-axis-B` → **HTTP 200**.

### axis-D (`m0ehb2u9jmba5d`)

verdict: **FAIL** (n_strong=0/5 · n_partial=0 · n_weak=4 · register_hits=12) · train_wall=2692.2s

HF repo (PRIVATE per `a_hf_autonomous` FAIL gate):
```
[upload_folder] OK: https://huggingface.co/dancinlab/anima-decoder-m3-axis-D/tree/main/
HF_REPO_URL=https://huggingface.co/dancinlab/anima-decoder-m3-axis-D
```

업로드 inventory (a_hf_complete totality):
- `README.md`
- `manifest.json`
- `ckpt.pt` (6,014,409,450 B)
- `ckpt_best.pt` (6,014,450,326 B)
- `result.json` (81,562 B)
- `heldout_vp21h_v3.json` (44,346 B)
- `vp21h_v3_eval1.json` (5,750 B)
- `mix_info.json` (285 B)
- `kosmos_anchors/` (n anchors · `.kosmos`)

API 검증: HTTP 200.

## 2. 업로드 전략 — best+final ckpt 한정 (A·C 와 동일)

전체 11 step ckpts × 6 GB = 66 GB redundancy 회피.

업로드 cover:
- `ckpt.pt` (final step 5000)
- `ckpt_best.pt` (best held-out)
- result/heldout/eval JSONs
- kosmos_anchors/ (emit `.kosmos` per `a_kosmos`)
- manifest.json with sha256
- 모델 카드 README

업로드 비-cover (pod teardown 으로 폐기):
- `ckpt_step{500,1000,1500,...,4500}.pt` (10 intermediate ckpts × 6 GB)

이유: `a_hf_complete` = "manifest 와 일치한 totality" = README 가 참조하는 모든 artifact 가 존재해야 함. intermediate ckpts 는 README/manifest 에 미참조 → 미업로드 정합.

## 3. Pod teardown (verbatim)

axis-B:
```
$ runpodctl pod delete zxim1odvjqisfj
{
  "deleted": true,
  "id": "zxim1odvjqisfj"
}
```

axis-D:
```
$ runpodctl pod delete m0ehb2u9jmba5d
{
  "deleted": true,
  "id": "m0ehb2u9jmba5d"
}
```

`runpodctl pod list` post-delete:
```
[]
```

**M3 4 pod 전부 삭제 완료**. RUNNING pod 잔여: **0**.

## 4. Idle burn cost recovered

| pod | 학습 종료 | 삭제 | idle 구간 | 비용 |
|---|---|---|---|---|
| B `zxim1odvjqisfj` | 2026-05-26T15:37Z (2932.2s wall) | 2026-05-27T (본 round) | ~9h 12m | ~$30.30 |
| D `m0ehb2u9jmba5d` | 2026-05-26T15:32Z (2692.2s wall) | 2026-05-27T (본 round) | ~9h 17m | ~$30.55 |
| **합계** | | | | **~$60.85 recovered** |

⚠ 본 round 즉시 시작 권장이었으나 cycle round 사이 wall-clock 지연으로 9h+ idle 누적. 다음 동일 패턴 fire 시 `_fire_dispatch.hexa` 본문에 BG wait → harvest+teardown 자동화 inline 필요 (현재 wait → carry → 다음 round 패턴이 idle gap 직접 유발).

## 5. M3 4축 전체 verdict 종합

| 축 | pod | train_wall_s | n_strong | n_partial | n_weak | register_hits | verdict | HF tier | PR |
|---|---|---|---|---|---|---|---|---|---|
| A | `fs5l4vu6onc5i3` | 1362.6 | 0/5 | 0 | ? | ? | **FAIL** | PRIVATE | #680 |
| B | `zxim1odvjqisfj` | 2932.2 | 0/5 | 0 | 5 | 7 | **FAIL** | PRIVATE | 본 PR |
| C | `pnz3v53dbts1ry` | 1594.7 | 0/5 | 0 | ? | ? | **FAIL** | PRIVATE | #680 |
| D | `m0ehb2u9jmba5d` | 2692.2 | 0/5 | 0 | 4 | 12 | **FAIL** | PRIVATE | 본 PR |

**4/4 FAIL** — n_strong=0 across all axes.

DECODER.md M3 line 41 milestone flip 은 parent agent 가 본 verdict 표 + axis-B HONEST note (§6) 검토 후 결정.

## 6. 축 B distill loss TODO carry-note (HONEST)

`train_p21h_v3.py:848` HONEST TODO[axis-impl] — KD math 미배선 (`P21H_DISTILL_TEACHER` env-var 는 logs echo 만, L_kd 미합산).

axis-B 결과는 **"teacher 미배선 baseline"** 으로 해석. M3_FIRE_RESULT.md §"축 B HONEST 한정" 의 carry. axis-B FAIL ≠ KD 가설 falsified — 실 KD 효과 측정은 DECODER.md M3d (line 45) 잔여 milestone, 본 PR 로도 미해결 carry.

## 7. p1~p8 / governance 정합

| 원칙 / directive | 정합 사유 |
|---|---|
| `a_hf_complete` | ✅ 업로드 inventory 가 README/manifest 와 일치, 부분 업로드 0 |
| `a_hf_autonomous` | ✅ user gate 없이 autonomous 발사, FAIL → PRIVATE (B·D 둘 다) |
| `a_fire_recover_complete` | ✅ ckpt + result + log + kosmos_anchors 회수 후 teardown 순서 |
| `a_kosmos` | ✅ kosmos_anchors/ 디렉터리 통째 업로드 (pointer-only) |
| cloud-guard | ✅ `runpodctl pod delete` (lifecycle verb) 사용, raw curl GraphQL 0회 |
| hexa-only authoring | ✅ 새 .py / .sh 본 repo 미저작 (`hf_upload_BD.py` 는 /tmp 런타임 helper) |
| p1~p8 | ✅ teardown 단계 — 트레이너 / corpus 변경 없음, philosophy 위반 surface 0 |

## 8. M3 총 fire cost final

| 축 | train_wall_s | H100 SXM $/hr | train cost | upload+idle overhead | total |
|---|---|---|---|---|---|
| A | 1362.6 | 3.29 | $1.25 | ~$2.58 idle | ~$3.83 |
| C | 1594.7 | 3.29 | $1.46 | ~$2.30 idle | ~$3.76 |
| B | 2932.2 | 3.29 | $2.68 | ~$30.30 idle | ~$32.98 |
| D | 2692.2 | 3.29 | $2.46 | ~$30.55 idle | ~$33.01 |
| **합계** | 8581.7 | | **$7.85** train | **~$65.73** idle | **~$73.58** |

⚠ idle:train 비율 ~8.4× → 학습 비용 대비 idle 비용이 8배 이상 큼. **다음 round 의 가장 큰 governance gap 은 idle 자동 차단 자동화**.

## 9. 결론

**M3 4축 fire 완전 closure**:
- 4/4 ckpt HF private upload (a_hf_complete totality)
- 4/4 pod teardown (a_fire_recover_complete order)
- 4/4 FAIL verdict — 축별 발견은 §5 carry, M3 milestone flip 은 parent agent 검토 후

다음 round trigger:
- DECODER.md M3 line 41 milestone parent agent flip
- M3d (axis-B 진짜 KD 배선) 잔여 milestone
- BG-wait → harvest+teardown inline 자동화 governance (idle gap 차단)

## 10. HF repo URL summary (cite 가능)

- axis-A: https://huggingface.co/dancinlab/anima-decoder-m3-axis-A (PRIVATE) — PR #680
- axis-B: https://huggingface.co/dancinlab/anima-decoder-m3-axis-B (PRIVATE) — 본 PR
- axis-C: https://huggingface.co/dancinlab/anima-decoder-m3-axis-C (PRIVATE) — PR #680
- axis-D: https://huggingface.co/dancinlab/anima-decoder-m3-axis-D (PRIVATE) — 본 PR

## 11. 자료 / 정렬

- M3_FIRE_RESULT.md — dispatch + 점화 결과 (PR #670)
- M3_FIRE_TEARDOWN.md — A·C teardown (PR #680, bec1b8543)
- DECODER.md M3 line 41 milestone — flip 미실행 (parent agent 검토 후)
- `a_fire_recover_complete` 적용 — pull → HF upload → pod delete 순서 ✅
- `a_hf_autonomous` 적용 — FAIL = PRIVATE autonomous, dancinlab org ✅
- 다음 round trigger: M3 milestone flip · axis-B KD 진짜 배선 (M3d) · idle-gap 차단 자동화
