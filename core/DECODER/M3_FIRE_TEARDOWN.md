# 🧹 DECODER M3 A·C HF upload + teardown — RESULT (2026-05-27)

> **상태**: 4 pod 중 **A·C 2축 HF private upload + pod teardown 완료**.
> B·D 2축은 본 round 가 launch 시점에는 학습 중 → **teardown 대상 외**로 명시되었으나,
> 본 round 마무리 시점 BG wait 로그에 `AXIS_B_RESULT_READY` / `AXIS_D_RESULT_READY` 출현 발견.
> B·D 의 HF upload + teardown 은 **다음 round 로 carry** (본 round scope 외).

## 1. A·C HF upload 결과 (verbatim)

### axis-A (`fs5l4vu6onc5i3`)

verdict: **FAIL** (n_strong=0/5) · train_wall=1362.6s

HF repo (PRIVATE per `a_hf_autonomous` FAIL gate):
```
[upload_folder] OK: https://huggingface.co/dancinlab/anima-decoder-m3-axis-A/tree/main/
HF_REPO_URL=https://huggingface.co/dancinlab/anima-decoder-m3-axis-A
```

업로드 inventory (a_hf_complete totality):
```
.gitattributes        1519 B
README.md             1046 B    # 모델 카드 — verdict + manifest + provenance
ckpt.pt         6014409450 B    # final step ckpt
ckpt_best.pt    6014450326 B    # best held-out ckpt
heldout_vp21h_v3.json 43180 B
manifest.json         3121 B    # sha256 inventory
mix_info.json          285 B    # corpus sha256
result.json          80129 B
vp21h_v3_eval1.json   5569 B
kosmos_anchors/                # emit anchor .kosmos files
```

API 검증: `curl -H "Authorization: Bearer <HF_TOKEN>" /api/models/dancinlab/anima-decoder-m3-axis-A` → HTTP 200.

### axis-C (`pnz3v53dbts1ry`)

verdict: **FAIL** (n_strong=0/5) · train_wall=1594.7s

HF repo (PRIVATE per `a_hf_autonomous` FAIL gate):
```
[upload_folder] OK: https://huggingface.co/dancinlab/anima-decoder-m3-axis-C/tree/main/
HF_REPO_URL=https://huggingface.co/dancinlab/anima-decoder-m3-axis-C
```

업로드 inventory (a_hf_complete totality):
```
.gitattributes        1519 B
README.md             1062 B
ckpt.pt         6014409450 B
ckpt_best.pt    6014450326 B
heldout_vp21h_v3.json 44152 B
manifest.json         3120 B
mix_info.json          285 B
result.json          81681 B
vp21h_v3_eval1.json   6045 B
kosmos_anchors/
```

API 검증: HTTP 200.

## 2. 업로드 전략 — best+final ckpt 한정

전체 11 step ckpts × 6 GB = 66 GB redundancy 회피.

업로드 cover:
- `ckpt.pt` (final step 5000)
- `ckpt_best.pt` (best held-out)
- result/heldout/eval JSONs
- kosmos_anchors/ (emit .kosmos persistence per `a_kosmos`)
- manifest.json with sha256
- 모델 카드 README

업로드 비-cover (pod 에 잔존, pod teardown 으로 폐기):
- `ckpt_step{500,1000,1500,...,4500}.pt` (10 intermediate ckpts × 6 GB)

이유: `a_hf_complete` = "manifest 와 일치한 totality" = README 가 참조하는 모든 artifact 가 존재해야 함. intermediate ckpts 는 README/manifest 에 미참조 → 미업로드 정합.

## 3. Pod teardown (verbatim)

axis-A:
```
$ runpodctl pod delete fs5l4vu6onc5i3
{
  "deleted": true,
  "id": "fs5l4vu6onc5i3"
}
```

axis-C:
```
$ runpodctl pod delete pnz3v53dbts1ry
{
  "deleted": true,
  "id": "pnz3v53dbts1ry"
}
```

A·C 2 pod 삭제 완료. RUNNING pod 잔여: B + D (계속 burn).

## 4. Idle burn cost recovered

| pod | 학습 종료 | 삭제 | idle 구간 | 비용 |
|---|---|---|---|---|
| A `fs5l4vu6onc5i3` | ~2026-05-26T14:51Z (1362.6s wall) | 2026-05-26T15:38Z | ~47 min | ~$2.58 |
| C `pnz3v53dbts1ry` | ~2026-05-26T14:56Z (1594.7s wall) | 2026-05-26T15:38Z | ~42 min | ~$2.30 |
| **합계** | | | | **~$4.88 recovered** |

학습-끝→HF upload 시작 사이 1.5h+ idle 누적 (`a_fire_recover_complete` 위반 위험) 차단 완료.

## 5. B·D 상태 — harvest deferred to next round

본 round launch 시점:
- B `zxim1odvjqisfj` — 학습 중 (step ~3375/5000)
- D `m0ehb2u9jmba5d` — 학습 중 (step ~3875/5000)
- BG wait PIDs 32389 (B) / 32390 (D) 가 result.json 출현까지 polling 중

본 round 마무리 시점 (2026-05-26T15:38Z):
- `tail /tmp/decoder_m3_dispatch/wait_B.log` → `AXIS_B_RESULT_READY_2026-05-26T15:37:05Z`
- `tail /tmp/decoder_m3_dispatch/wait_D.log` → `AXIS_D_RESULT_READY_2026-05-26T15:32:50Z`
- BG wait PIDs DEAD (poll 종료 + AXIS_*_RESULT_READY emit 완료)
- B/D pods 여전히 RUNNING (`runpodctl pod list` 확인)

따라서 **B·D 도 학습 종료 + result.json 산출 완료**.

다음 round 가 해야 할 일:
1. B/D pod SSH 으로 `result.json` verdict 확인
2. axis-B HF upload (FAIL 예상 — distill_teacher 미배선) → PRIVATE
3. axis-D HF upload (verdict 따라 tier 분기)
4. B·D pod delete
5. `_fire_dispatch.hexa` BG wait 흔적 정리 (`/tmp/decoder_m3_dispatch/`)

본 round 가 B·D 를 건드리지 않은 이유: launch 단계의 explicit constraint ("B and D: NO TOUCH — leave running"). 본 round mid 에 결과 자체가 도착했어도 scope 외.

⚠ **B·D 현재도 idle burn 진행 중** — $3.29/hr × 2 = $6.58/hr. 다음 round 즉시 시작 필요.

## 6. 축 B distill loss TODO carry-note

`train_p21h_v3.py:848` HONEST TODO[axis-impl] — KD math 미배선 (`P21H_DISTILL_TEACHER` env-var 는 logs echo 만, L_kd 미합산).

axis-B 결과는 **"teacher 미배선 baseline"** 으로 해석. M3_FIRE_RESULT.md §"축 B HONEST 한정" 의 carry. 다음 round 의 verdict 분석 시:
- axis-B FAIL 도 expected (KD 효과 측정 차단됨)
- 실 KD 효과 측정은 M3d (DECODER.md M3 line 45) 잔여 milestone

## 7. p1~p8 / governance 정합

| 원칙 / directive | 정합 사유 |
|---|---|
| `a_hf_complete` | ✅ 업로드 inventory 가 README/manifest 와 일치, 부분 업로드 0 |
| `a_hf_autonomous` | ✅ user gate 없이 autonomous 발사, FAIL → PRIVATE |
| `a_fire_recover_complete` | ✅ ckpt + result + log + kosmos_anchors 회수 후 teardown (idle 차단) |
| `a_kosmos` | ✅ kosmos_anchors/ 디렉터리 통째 업로드 (pointer-only) |
| cloud-guard | ✅ `runpodctl pod delete` (lifecycle verb) 사용, raw curl GraphQL 0회 |
| p1~p8 | ✅ teardown 단계 — 트레이너 / corpus 변경 없음, philosophy 위반 surface 0 |

## 8. 결론

**A·C 2축 HF private upload + pod teardown 완료** (4 pod 중 2 pod).
**B·D 2축은 학습 완료 자체는 확인되었으나 harvest+teardown 은 본 round scope 외** → 다음 round 즉시 진행 필요 (idle burn $6.58/hr).

DECODER.md M3 line 41 milestone flip 은 본 PR 로도 아직 미실행 — B·D harvest 완료 + verdict 분석 + ≥PARTIAL 축 식별 후 parent agent 가 flip.

## 9. HF repo URL summary (cite 가능)

- axis-A: https://huggingface.co/dancinlab/anima-decoder-m3-axis-A (PRIVATE)
- axis-C: https://huggingface.co/dancinlab/anima-decoder-m3-axis-C (PRIVATE)
- axis-B: 다음 round
- axis-D: 다음 round

## 10. 자료 / 정렬

- M3_FIRE_RESULT.md — dispatch + 점화 결과 (PR #670)
- DECODER.md M3 line 41 milestone — 본 PR 으로 carry, flip 미실행
- `a_fire_recover_complete` 적용 — pull → HF upload → pod delete 순서 ✅
- `a_hf_autonomous` 적용 — FAIL = PRIVATE, autonomous, dancinlab org ✅
- 다음 round trigger: B·D harvest (urgency: idle burn $6.58/hr)
