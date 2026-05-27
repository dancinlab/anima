# A-커리큘럼 fire 준비 완료 — 2026-05-25

> anchor — spec: `HEXAD/PURE/spec/axis_map_a_curriculum_recipe_2026_05_24.md` ·
> corpus builder: `HEXAD/PURE/launchers/build_curriculum_corpus.hexa` ·
> dispatcher: `HEXAD/PURE/launchers/dispatch_p21h_v3.hexa`

---

## § 1. 한 번에 fire 하는 방법 (사용자가 실행하는 단일 명령어)

### Step A — corpus 전처리 (로컬, ~10-20 min, $0)

```bash
cd /Users/ghost/core/anima
hexa run HEXAD/PURE/launchers/build_curriculum_corpus.hexa build \
  --wiki-path  state/pure_phase_d_corpus_2026_05_24/corpus.jsonl \
  --anima-path state/pure_phase_d_corpus_anima_own_poc_2026_05_24/corpus.jsonl \
  --out        state/pure_phase_d_curriculum_v2_2026_05_24/merged_curriculum_v2.jsonl \
  --manifest   state/pure_phase_d_curriculum_v2_2026_05_24/manifest_curriculum_v2.json \
  --n-warm 2000 --phase-in 500 --target-records 30000 \
  --anima-frac-target 0.4 --seed 20260525
```

### Step B — GPU fire (A100, ~$2.5-3.5, ~2.5h wall)

```bash
cd /Users/ghost/core/anima
P21H_STEPS=5000 P21H_LR=5e-5 P21H_WARMUP=100 \
P21H_WIKI_FRAC=1.0 P21H_MITOSIS_MAX=16 P21H_CKPT_EVERY=500 \
WATCHDOG_SEC=5400 SAVE_POD=1 \
hexa run HEXAD/PURE/launchers/dispatch_p21h_v3.hexa \
  P21H_curriculum_v2 qwen 1337 \
  --corpus-path ./state/pure_phase_d_curriculum_v2_2026_05_24/merged_curriculum_v2.jsonl \
  --measure-motivation \
  --fire
```

**`--fire` 가 없으면 dry-run (zero cost). 위 명령어 그대로 복붙하면 실제 GPU pod 발사.**

---

## § 2. dispatcher dry-run 출력 (검증 완료 2026-05-25)

아래는 `--fire` 없는 dry-run 에서 캡처한 전체 stdout 이다.
train_p21h_v3.py 전체 argv, corpus_scp_override 경로, sources_upload 포함 확인.

```
=== dispatch_p21h_v3.hexa v0.2 [DRY-RUN] ===
    variant=P21H_curriculum_v2 init=qwen seed=1337
    steps=5000 bsz=2 lr=5e-5
    teacher_sha=
    corpus_override=./state/pure_phase_d_curriculum_v2_2026_05_24/merged_curriculum_v2.jsonl (SKIP corpus_s101 + multi_wiki builds)
    (default dry-run — pass --fire to incur real GPU cost)
[dry-run] pod_create: runpod_create_cascade(5 gpus) image=runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04 name=p21h-qwen
[dry-run] pod_ssh_wait: runpod_wait_ssh(pod=, tries=90, sleep=10)
[dry-run] sources_upload: cloud_run_opts(root@, mkdir -p 6 dirs under /workspace/p21hr)
[dry-run] sources_upload: cloud_copy_to_opts(root@, .../train_p21h_v3.py -> /workspace/p21hr/train_p21h_v3.py)
[dry-run] sources_upload: cloud_copy_to_opts(root@, .../launch_trainer_p21.sh -> /workspace/p21hr/launch_trainer_p21h.sh)
[dry-run] sources_upload: cloud_copy_to_opts(root@, .../build_multilingual_corpus_p21m.py -> /workspace/p21hr/build_multilingual_corpus_p21m.py)
[dry-run] sources_upload: cloud_copy_to_opts(root@, .../train_p21m_multilingual.py -> /workspace/p21hr/train_p21m_multilingual.py)
[dry-run] sources_upload: cloud_copy_to_opts(root@, .../conscious_decoder_v3.py -> /workspace/p21hr/conscious_decoder_v3.py)
[dry-run] sources_upload: cloud_copy_to_opts(root@, .../kosmos_io.py -> /workspace/p21hr/kosmos_io.py)
[dry-run] sources_upload: cloud_copy_to_opts(root@, .../mitosis_lib.py -> /workspace/p21hr/mitosis_lib.py)
[dry-run] sources_upload: cloud_copy_to_opts(root@, .../corpus_carving_s16_generator.py -> ...)
[dry-run] sources_upload: cloud_copy_to_opts(root@, .../build_corpus_s101.py -> ...)
[dry-run] corpus_scp_override: cloud_run_opts(root@, mkdir -p /workspace/p21hr/state/corpus_s101_build_s102_2026_05_19)
[dry-run] corpus_scp_override: cloud_copy_to_opts(root@,
    ./state/pure_phase_d_curriculum_v2_2026_05_24/merged_curriculum_v2.jsonl
    -> /workspace/p21hr/state/corpus_s101_build_s102_2026_05_19/corpus_s101.jsonl)
[dry-run] corpus_scp_override: cloud_copy_to_opts(root@,
    ./state/pure_phase_d_curriculum_v2_2026_05_24/merged_curriculum_v2.jsonl
    -> /workspace/p21hr/multi_wiki_corpus.jsonl)
[dry-run] train_launch: cloud_nohup_opts(root@,
    launch_trainer_p21h.sh /workspace/p21hr/train_p21h_v3.py
    --wiki-corpus /workspace/p21hr/multi_wiki_corpus.jsonl
    --anima-corpus /workspace/p21hr/state/corpus_s101_build_s102_2026_05_19/corpus_s101.jsonl
    --mixed-corpus /workspace/p21hr/mixed_corpus_built.jsonl
    --out-dir /workspace/p21hr/out_main
    --init-variant qwen --seed 1337
    --steps 5000 --lr 5e-5 --bsz 2 --block 512
    --warmup-steps 100 --noise-sigma 0.1 --lambda-mitosis 0.05
    --mitosis-max 16 --ckpt-every 500 --wiki-frac 1.0
    --base-model Qwen/Qwen2.5-1.5B
    log=/workspace/p21hr/train.log)
[dry-run] result_pull_with_wait: poll /workspace/p21hr/out_main/result.json every 60s up to 90 tries (budget=5400s)
[dry-run] embed_motivation: would read vP21H_curriculum_v2/result.json + invoke 8-factor + re-write motivation_8factor block
[pod_terminate] SAVE_POD=1 — pod  RETAINED
=== dispatch_p21h_v3.hexa end [DRY-RUN] ===
```

검증 포인트:
- `corpus_scp_override` 가 curriculum jsonl 을 anima + wiki 두 경로 모두에 매핑 ✓
- `sources_upload` 에 `train_p21m_multilingual.py` 포함 (post-#423 fix) ✓
- `train_p21h_v3.py` 전체 argv 출력 ✓

---

## § 3. F-CURRICULA-1 PASS/FAIL 판정 기준 (result.json 필드)

result.json 은 `multilingual_probe` 가 기록하는 언어별 tier 를 포함한다.

| 필드 | 의미 |
|---|---|
| `lang_scores.{en,ko,zh,ru,ja}.tier` | `STRONG` / `PARTIAL` / `WEAK` / `PM` |
| `lang_scores.*.n_strong` | STRONG tier 도달 언어 수 |
| `lang_scores.ko.register_hits` | ko register 문장 재생 성공 수 (/20) |
| `register_regress` | bool — ko register collapse 여부 |

**F-CURRICULA-1 PASS**: `n_strong >= 2` AND non-ko 중 최소 1개 `tier >= PARTIAL`

**F-CURRICULA-1 FAIL**: `n_strong <= 1` AND non-ko 전원 `WEAK` 또는 `PM`
→ axis A 1차 (n_strong=1, ko-only) 와 동일하거나 후퇴 → N_WARM 연장 단독으로 cross-lingual 전이 불충분

**F-CURRICULA-2 PASS** (병행 확인): `register_hits < 4` AND `register_regress == false`

---

## § 4. corpus_v1 flat-shuffle 과 비교 — 무엇이 바뀌었는가

| 항목 | corpus_v1 (flat shuffle) | A-curriculum v2 |
|---|---|---|
| anima register 노출 시점 | step 1 부터 | Phase 2 시작 (step N_WARM+1) |
| Phase 1 내용 | wiki/anima/QA 혼합 | wiki-only (source=wiki 100%) |
| anima 비율 | ~50% 고정 | 0% → 40% 점진 (N_WARM+PHASE_IN 이후 40% 고정) |
| dispatcher 코드 변경 | — | 없음 (--corpus-path knob만 사용) |
| 나머지 하이퍼파라미터 | — | 동일 (steps/lr/bsz/block/seed 모두 동일) |

→ corpus ordering 단독 ablation — 비율 axis 와 직교하므로 결과가 corpus_v1 과 다르면 ordering 효과로 귀인 가능.

---

## § 5. 비용 / ETA

| 항목 | 값 |
|---|---|
| corpus 전처리 (로컬) | $0 / ~10-20 min |
| GPU pod (A100 SXM 80GB) | ~$2.50-3.50 (1.45$/hr × ~2hr) |
| result pull + 로컬 eval | $0 / ~5-10 min |
| **total** | **~$2.50-3.50 / wall ~2.5 hr** |

GPU cascade: A100-SXM4-80GB → A100-80GB-PCIe → H100-80GB-HBM3 → H100-NVL → H100-PCIe (첫 가용 GPU 자동 선택).

---

## § 6. 사전 검증 결과

```
hexa parse HEXAD/PURE/launchers/build_curriculum_corpus.hexa
→ OK: parses cleanly

hexa run HEXAD/PURE/launchers/build_curriculum_corpus.hexa smoke
→ [smoke] 5/5 PASS
  F1 PASS  anima_frac=0.0 for all s<N_WARM (20)
  F2 PASS  anima_frac=target for all s>=N_WARM+PHASE_IN
  F3 PASS  phase-in anima_frac is monotone non-decreasing over [N_WARM, N_WARM+PHASE_IN)
  F4 PASS  all Phase 1 slots (20) are source=wiki
  F5 PASS  Phase 3 anima density=0.385714 in [0.32,0.48]
```

— 끝 —
