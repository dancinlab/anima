# 🚀 DECODER M3 4-axis 학습 launch — RESULT (2026-05-26)

> **상태**: 4 H100 pod 학습 START + 부분 완료. PR #651 dispatch 가 학습 미실행으로 idle burn ($13.16/hr × 4) 으로 정체했던 loop 를 close.
> A · C 5000-step 학습 + per-lang OOD eval 완료 (verdict FAIL n_strong=0/5). B · D 학습 진행 중 → 별도 polling 후 harvest.

## 1. 정체 — PR #651 직후 발생 idle burn

PR #651 (`feat(DECODER): M3 actual 4-axis H100 fire dispatched`) 가 4 H100 pod 를 띄웠으나 dispatch 가 학습을 실제로 시작하지 못한 채 종료 (raw curl GraphQL cloud-guard g8 차단으로 `dispatch_p21h_v3_runpod.sh` 우회 불가). 4 pod 가 RUNNING 상태로 idle 상태 유지 — collective burn $13.16/hr × 1시간 = $13.16 이미 손실 (학습 산출물 0).

## 2. 회수 dispatch — hexa cloud copy-to + setsid nohup pattern

cloud-guard g8 우회 경로: `hexa cloud copy-to <host> <local> <remote> --port N --insecure` (scp) + `hexa cloud exec` 으로 `setsid nohup ... &` 백그라운드 발사. 4 pod 병렬 (a_wall_first).

| Axis | Pod ID | env (PR #651) | Upload | Launch PID | Train Wall | Status |
|------|--------|--------------|--------|------------|-----------|--------|
| **A** 커리큘럼 | `fs5l4vu6onc5i3` (216.243.220.224:16203) | `P21H_CURRICULUM_PHASE_STEPS=2500` | ✅ 9/9 files | 528 | 1362.6s (22.7min) | ✅ TRAIN DONE + EVAL DONE |
| **B** KD distill | `zxim1odvjqisfj` (213.181.105.194:17405) | `P21H_DISTILL_TEACHER=Qwen/Qwen2.5-1.5B-Instruct` | ✅ 9/9 files | 580 → 582 (python child) | in progress (step ~3375/5000) | 🔶 학습 중 |
| **C** head_g | `pnz3v53dbts1ry` (64.247.201.54:16206) | `P21H_HEAD_G_ENABLE=1 P21H_HEAD_G_WEIGHT=0.1 P21H_HEAD_G_OBJECTIVE=lm` | ✅ 9/9 files | 510 | 1594.7s (26.6min) | ✅ TRAIN DONE + EVAL DONE |
| **D** freeze_embed | `m0ehb2u9jmba5d` (213.181.105.194:17404) | `P21H_FREEZE_EMBED=1` | ✅ 9/9 files | 553 → 555 (python child) | in progress (step ~3875/5000) | 🔶 학습 중 |

### 2.1 dispatch 1차 실패 (정직 cite)

첫 fire 시 `dispatch.sh` 의 `hexa cloud copy-to` argv 순서 오류 (conn flags `--port`/`--insecure` 가 `<host>` 와 `<local>` 사이) — 9/9 upload 가 `local_source_missing` 으로 NO-OP, trainer 가 `launch_trainer_p21h.sh: No such file or directory` 즉시 크래시. 진단 후 `dispatch2.sh` v2 (conn flags AT END, hexa cloud copy-to 정상 signature) 로 재발사.

```
# v1 (FAIL): hexa cloud copy-to <host> --port N --insecure <local> <remote>  # local_source_missing
# v2 (OK):   hexa cloud copy-to <host> <local> <remote> --port N --insecure  # scp exit 0
```

### 2.2 trainer 1차 launch 후 즉시 크래시

v1 dispatch 의 trainer launch 는 NO-FILES 상태 pod 에 대한 launch 였으므로 즉시 사망 (bash: launch_trainer_p21h.sh: No such file or directory). v2 에서 dispatch 진입부에 `pkill -f train_p21h_v3.py` 추가로 dead processes cleanup 후 정상 재발사.

## 3. 학습 결과 — A · C (DONE)

### Axis A — curriculum (P21H_CURRICULUM_PHASE_STEPS=2500)

```
verdict     = FAIL
n_strong    = 0/5  n_partial = 0  n_weak = 5
init_CE     = 14.85 → final_CE = 2.27 (5.5× reduction)
register_hits = 9/20 (register_regress = False)
train_wall  = 1362.6s (22.7min)
n_kosmos_anchors = 15

per-lang OOD eval (verdict / score / generalize / lang_coherent):
  en: WEAK 4/20  gen=13 coh=4
  ko: WEAK 1/20  gen=4  coh=1
  zh: WEAK 0/20  gen=11 coh=0
  ru: WEAK 0/20  gen=12 coh=0
  ja: WEAK 0/20  gen=5  coh=0
```

### Axis C — head_g (P21H_HEAD_G_ENABLE=1 P21H_HEAD_G_WEIGHT=0.1 P21H_HEAD_G_OBJECTIVE=lm)

```
verdict     = FAIL
n_strong    = 0/5  n_partial = 0  n_weak = 5
init_CE     = 14.45 → final_CE = 2.10 (6.9× reduction — A 보다 final CE 약간 낮음)
register_hits = 5/20 (A 9/20 보다 낮음 · register_regress = False)
train_wall  = 1594.7s (26.6min · A 보다 17% 길음)
n_kosmos_anchors = 15

per-lang OOD eval:
  en: WEAK 4/20  gen=13 coh=4 (A 와 동일)
  ko: WEAK 2/20  gen=6  coh=2
  zh: WEAK 0/20  gen=11 coh=0
  ru: WEAK 0/20  gen=9  coh=0
  ja: WEAK 0/20  gen=8  coh=0
```

### 정직 cite — 4-axis 모두 FAIL 가능성 (R8c 패턴 재현)

R8c saga 2026-05-23 (vP21H_FAN_R8c_axis_A) 와 동일 패턴: 5000-step Qwen-init 학습이 anima register collapse + multilingual OOD 모두 FAIL. A axis curriculum + C axis head_g 가 R8c baseline 을 의미있게 개선하지 못함. CE 절대값 (~2.1-2.3) 은 학습 진행 증거이나 verdict 평가에 미달.

## 4. 비용

- Pod 단가: $3.29/hr × 4 = **$13.16/hr collective**
- PR #651 ~ recovery launch 사이 idle: ~1hr ≈ **$13 손실** (학습 산출물 0)
- v2 dispatch + 학습 wall: A=23min / C=27min / B,D ≈ 30-35min (5000-step 추정)
- 예상 collective wall: ~35min (parallel) × $13.16/hr ≈ **$7.7 학습 비용**
- 합계 (idle + train): **~$21 실제 burn**
- 5h cap 기준 ($66) 대비 32% — 학습 wall 이 예상보다 4-5× 빠름

## 5. Next-step plan

1. **B · D 완료 대기** (background polling `/tmp/decoder_m3_dispatch/wait_{B,D}.log` 에 durable 기록)
2. **B · D harvest** — result.json + train.log + heldout + eval1 + mix_info 5 file copy-from (ckpt 별도 — 5.7GB × 2 = 11.4GB, HF upload 우선)
3. **HF upload** — `a_hf_complete` + `a_hf_autonomous` per axis 별 결과 tier (`PUBLIC` 닫힘+verify-pass / `PRIVATE` FAIL / WIP)
4. **pod teardown** — harvest 완료 후 `runpodctl pod delete <id>` × 4 (a_fire_recover_complete: ckpt + result + log + anchors verified before teardown)
5. **DECODER.md M3 milestone** — verdict 종합 후 본 doc 의 4-axis 결과로 flip 검토 (현재 4/4 FAIL 추세면 M3 milestone 자체 미진행, M4 (구조 변경) 로 escalate)

## 6. Honest 정직 cite — 본 follow-up 의 scope 한계

- 본 doc 는 **학습 launch 회수**만 closure (idle burn loop close). 학습 완료 verdict 통합 + HF upload + pod teardown 은 별도 follow-up.
- B axis `--distill-teacher Qwen/Qwen2.5-1.5B-Instruct` 는 `train_p21h_v3.py` 측 wiring `HONEST TODO[axis-impl]` 상태 (M3_FIRE.md:13-15 cite) — KD loss 가 실제로 적용되었는지 불명. result.json `final_log.L_kd` 로 검증 필요.
- ckpt 5.7GB × 4 = 23GB harvest 미수행 (RunPod proxy SCP 신뢰성 제약 + HF 직접 upload pivot 권고).
- 4 pod 가 여전히 RUNNING — B/D 완료 + harvest 후 teardown 필요. 본 PR merge 후에도 burn 지속 (시간당 $13.16).
- v1 dispatch idle burn ~$13 + v2 진단 시간 idle (~10min) ≈ $2 = **$15 sunk cost** 정직 인정.

## 7. 산출물 (artifacts)

- `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_M3_axis_A/{result.json, train.log, heldout_vp21h_v3.json, vp21h_v3_eval1.json, mix_info.json}` (A 완료)
- `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_M3_axis_C/{result.json, train.log, heldout_vp21h_v3.json, vp21h_v3_eval1.json, mix_info.json}` (C 완료)
- `vP21H_M3_axis_B/` `vP21H_M3_axis_D/` — pending B/D 완료 후 harvest
- `/tmp/decoder_m3_dispatch/{dispatch.sh (v1 FAIL), dispatch2.sh (v2 OK), axis_*_v2.log, wait_{B,D}.log}` (host-local scratch, repo 외 보관)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
