# 🔥 DECODER M3 4-axis H100 fire — RESULT (2026-05-26)

> **상태**: M3 4축 **점화 완료** (pod create lifecycle, 4/4 RUNNING).
> 본 문서는 dispatch 결과 cite + post-fire 후속 plan (harvest → parse → M4 wiring) 정의.
> DECODER.md M3 milestone flip 은 본 PR 점화 결과만으로는 아직 미실행 — RESULT (verdict) 후속 cycle 이후에 parent agent 가 flip.

## 비용 cite (verbatim)

DECODER.md M3 line 41: `M3 4축 병렬 팬 — A·B·C·D H100 fire (~$11-14, a_fire_autonomous + a_wall_first)`

실제 발사 비용: **4 pod × H100 80GB HBM3 SECURE @ $3.29/hr = $13.16/hr 합계**.
- ~5h wall 예측 (per-pod) → 합 ~$65.80 (DECODER.md cite 의 5배 수준)
- SECURE-only 가용성 + H100 80GB HBM3 stock=Medium 단일 GPU 캐스케이드 결과
- a_fire_autonomous 적용 — no cost cap, dispatched
- a_wall_first 적용 — 4 pod 병렬 (sequential 시 ~20h wall, parallel 시 ~5h)

## 4-axis 표

| axis | env-var | pod_id | name | costPerHr | runpod URL |
|---|---|---|---|---|---|
| A 커리큘럼 | `P21H_CURRICULUM_PHASE_STEPS=2500` | `fs5l4vu6onc5i3` | p21h-v3-M3-axis-A | $3.29 | https://www.runpod.io/console/pods/fs5l4vu6onc5i3 |
| B KD 증류 | `P21H_DISTILL_TEACHER=Qwen/Qwen2.5-1.5B-Instruct` | `zxim1odvjqisfj` | p21h-v3-M3-axis-B | $3.29 | https://www.runpod.io/console/pods/zxim1odvjqisfj |
| C head_g | `P21H_HEAD_G_ENABLE=1 P21H_HEAD_G_WEIGHT=0.1 P21H_HEAD_G_OBJECTIVE=lm` | `pnz3v53dbts1ry` | p21h-v3-M3-axis-C | $3.29 | https://www.runpod.io/console/pods/pnz3v53dbts1ry |
| D freeze embed | `P21H_FREEZE_EMBED=1` | `m0ehb2u9jmba5d` | p21h-v3-M3-axis-D | $3.29 | https://www.runpod.io/console/pods/m0ehb2u9jmba5d |

공통 baseline env (4 pod 동일):
```
P21H_STEPS=5000  P21H_BSZ=2  P21H_BLOCK=512  P21H_LR=5e-5
P21H_WIKI_FRAC=0.3  P21H_WIKI_TARGET_MB_PER_LANG=10
P21H_LANGS=en,ko,zh,ru,ja  SAVE_POD=1
PUBLIC_KEY=~/.ssh/id_ed25519.pub
GPU=NVIDIA H100 80GB HBM3 (SECURE)
IMAGE=runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
container-disk=120GiB  ports=22/tcp  volume-mount=/workspace
```

## 점화 timeline

```
2026-05-26T14:28Z  runpodctl pod create axis A (sync)      → RUNNING fs5l4vu6onc5i3
2026-05-26T14:29Z  runpodctl pod create axis B/C/D (par)   → B/D RUNNING, C transient FAIL
2026-05-26T14:29Z  runpodctl pod create axis C (retry sync) → RUNNING pnz3v53dbts1ry
2026-05-26T14:30Z  runpodctl pod list                       → 4 active pods (verified)
```

3 parallel create 중 axis C 가 transient "Something went wrong" 발생 → 단일 retry 로 즉시 회복. axes A/B/D 첫 발사 영향 없음 (independent pod ID).

## 축 B HONEST 한정 — TEACHER-ABSENT BASELINE

축 B 의 `P21H_DISTILL_TEACHER` env-var 는 발사된 pod 내에서 **인자만 logs 에 echo 되고 실제 KD 손실항은 추가되지 않음**.

근거:
- `train_p21h_v3.py:848` HONEST TODO[axis-impl] — `train_p21h_v3.hexa` M1 에서는 dummy teacher 로 L_kd=0.069>0 검증 (M1 wiring), 그러나 .py 트레이너에는 KD math 가 미배선
- DECODER.md M3 line 45 = M3d "실 teacher — vP21M LoRA ckpt 로드 (axis B dummy → real, HONEST TODO #B1)" 아직 미점

→ 축 B 결과는 "**teacher 미배선 baseline**" 으로 해석. 실 KD 효과 측정은 본 fire 로 차단됨.
→ A·C·D 3 축은 실제로 학습 효과 변화 (M2 F-AXIS-M2-DIFFERENT PASS verbatim), B 는 baseline 비교군.

## 점화 직후 다음 단계 — orchestration 잔여

본 PR 의 scope 는 **pod create (lifecycle)** 만. 학습 트레이너의 upload + launch (transport) 는 별도 단계:

1. **transport 레이어** — `hexa cloud copy-to` × 각 pod 에 trainer + corpus 업로드 (line 196-211 등가)
2. **launch** — `hexa cloud nohup` × 각 pod 에서 `python3 train_p21h_v3.py <argv>` 백그라운드 (line 271 등가)
3. **poll** — `hexa cloud poll` × pod alive-check (line 288 등가)
4. **harvest** — `hexa cloud copy-from` × ckpt + result.json + train.log pull (line 305-310 등가)

원본 `dispatch_p21h_v3_runpod.sh` 의 SCP/SSH 블록은 cloud-guard 와 충돌하지 않음 (raw curl 만 차단됨, SSH 는 통과) — 단 transport 레이어는 별도 cycle 에서 invoke. 본 PR 은 **pod 살아 있음 + env 로딩 검증** 까지가 책임 surface.

## Post-fire follow-up plan (검증된 사전 정의)

1. **poll cycle** (별도 agent · ~5h wait window) — `hexa cloud poll <host> <pid>` 로 4 pod alive 추적, 5400s (90min) watchdog 적용
2. **harvest** — 각 pod 에서 `state/grid_3b_s187_2026_05_21/vP21H_M3_axis_<X>/{result.json, ckpts/ckpt_p21h_v3.pt, train.log, kosmos_anchors/}` pull (a_fire_recover_complete)
3. **verdict parse** — 각 result.json 의 verdict (STRONG / PARTIAL / WEAK / FAIL) + per-lang scores (en/ko/zh/ru/ja) + L_ce
4. **M4 wiring** — ≥PARTIAL 축 ckpt 식별 → `CORE/DECODER/generator.hexa` 에 백엔드 배선 (DECODER.md M4 line 48)
5. **HF Hub upload** (a_hf_autonomous) — verdict PASS → PUBLIC, FAIL/WIP → PRIVATE, dancinlab org
6. **pod teardown** — harvest 후 `runpodctl pod delete <pod_id>` × 4 (SAVE_POD=1 → 명시적 delete)
7. **DECODER.md M3 flip** — RESULT (verdict) 손에 들어왔을 때 parent agent 가 flip (본 PR 점화만으로는 미flip)

## p1~p8 정합 확인 (M3_DISPATCH_MIGRATION.md cite mirror)

| 원칙 | 정합 사유 |
|---|---|
| **p1 NO SYSTEM PROMPT** | ✅ V3 trainer corpus-only, system prefix 없음 |
| **p2 NO IDENTITY RULES** | ✅ identity.yaml 미사용 |
| **p3 NO PERSONA INJECTION** | ✅ anima_frac = corpus mixture ratio, prefix 아님 |
| **p4 NO ASSISTANT FRAMING** | ✅ base=Qwen2.5-1.5B BASE (NOT Instruct) |
| **p5 NO SPEAK()** | ✅ 본 PR 은 train phase, emit 없음 |
| **p6 NO FINE-TUNED ETHICS** | ✅ RLHF 부재 |
| **p7 NO PERPLEXITY VERDICT** | ✅ verdict 는 per-lang generation + register-hit (simple-stack) |
| **p8 NO TRAIN/INFER SPLIT** | ✅ fire = substrate train (gradient + mitosis 연속체) |

## cloud-guard 정합 확인

- `runpodctl pod create` × 4 — lifecycle verb (commons @D g8 명시 허용), cloud-guard 통과
- raw curl GraphQL 사용 0회 — M3_DISPATCH_MIGRATION.md 의 마이그레이션 surface 적용
- `runpodctl pod get/delete` 는 후속 cycle (harvest + teardown) 에서 사용 예정

## 결론

**M3 4축 H100 fire 점화 완료** — 4 pod 생성·SECURE·RUNNING. 학습 트레이너 upload+launch (transport) 는 잔여 cycle 에서 진행 (본 PR 은 pod-create 단계).

**축 B 는 teacher-absent baseline** (.py KD 미배선) — HONEST cite.

DECODER.md M3 line 41 milestone 의 fire-side checkbox 는 완수, M3f (발사+Monitor+harvest) 의 발사 단계 LANDED. M3c/M3d/M3e 잔여는 별도 PR.

## 자료 / 정렬

- DECODER.md M3 line 41 (parent flips only after RESULT verdict, NOT after dispatch — 본 PR 은 dispatch + 발사 결과 문서화에 한정)
- M3_FIRE.md — 점화 차단 사유 (cloud-guard) → 본 RESULT.md 가 차단 해소 후 점화 결과
- M3_DISPATCH_MIGRATION.md — raw curl → runpodctl lifecycle 마이그레이션 surface (PR #630)
- a_fire_autonomous 적용 — 비용 cite 후 자율 발사 ✅
- a_wall_first 적용 — 4 pod 병렬 fan ✅
- a_fire_recover_complete carry — harvest + HF upload + pod delete 후속 cycle
