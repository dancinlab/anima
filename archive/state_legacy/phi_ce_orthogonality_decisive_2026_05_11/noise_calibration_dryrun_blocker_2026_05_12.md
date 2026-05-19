---
id: phi_ce_noise_calibration_dryrun_blocker_2026_05_12
parent_spec: phi_ce_orthogonality_decisive_2026_05_11/spec.md (§5.7.4)
parent_prereq: phi_ce_orthogonality_decisive_2026_05_11/noise_calibration_prereq_2026_05_12.md
parent_audit: phi_ce_orthogonality_decisive_2026_05_11/spec_audit_2026_05_11.md (§4, §5)
parent_h: H_080 (topo_24variants unified) — Conflict Resolution Pending
status: dryrun-blocker (execution prerequisites unmet — NO GPU spend)
date: 2026-05-12
deterministic_seed: 0xC0EC0AC (inherited)
budget_authorized: $15-45 (small budget OK if blocking)
budget_spent: $0 (BLOCKED before any GPU dispatch)
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# Φ⊥CE Noise Floor Calibration — Dry-Run Blocker Report

본 문서는 cycle 5 §4 #J "$15-45 GPU 작은 budget" 승인 하에서
`noise_calibration_prereq_2026_05_12.md` actual 실행 시도 결과 — **execution
prerequisites unmet, $0 spent, BLOCKED verdict**. 무엇이 막혔는지 + 다음 cycle
resolve path 명시.

## 0. TL;DR

| | status |
|---|---|
| Gate A (σ_Φ_rel ≤ 0.10) | **BLOCKED — not measured** |
| Gate B (σ_CE_rel ≤ 0.05) | **BLOCKED — not measured** |
| Gate C (separability ≥ 50×) | **BLOCKED — dependent on A/B** |
| Verdict | **BLOCKED** (proceed to next cycle after resolving 5 prereqs below) |
| Cost actual | **$0** (no GPU dispatch — saved $15-45 budget) |
| Cost estimate if executed | $15-45 (RunPod A100, parent spec table 정합) |
| Wall time actual | ~15 분 (audit + probe only) |

## 1. Prerequisites probed

### 1.1 Hexa runtime
- ✅ `/home/summer/.hx/bin/hexa` → `hexa_real` (ELF binary, executable)
- ✅ `tool/anima_phi_star.hexa` 파일 자체 존재 (10547 bytes, mtime 2026-05-12 00:23)

### 1.2 GPU (local Linux)
- ✅ NVIDIA RTX 5070, 12,227 MiB total, 11,526 MiB free at probe time
- ⚠ **Mistral-7B-v0.3 fp16 forward ≈ 14 GB VRAM > 12 GB ceiling** — int8/int4
  quantization 없이는 OOM. anima_phi_star.hexa 의 default backbone 은 fp16.

### 1.3 Model cache
- HF cache (`~/.cache/huggingface/hub/`) 에 존재하는 모델:
  - `Qwen2.5-Coder-{1.5B,3B,7B,7B-Instruct-AWQ}`
  - `Llama-3.2-3B`
  - `dancinlab/clm-v4-mk2-v1`
  - `skt/kogpt2-base-v2`
- ❌ **Mistral-7B-v0.3 not cached** — first-run download ~14 GB + auth token
  필요 (Mistral gated). audit §1.1 의 default backbone 부재.

### 1.4 RunPod credentials
- `secret` CLI 는 Mac side (`/Users/ghost/core/secret/bin/secret`) — Linux
  sandbox 에서 read/exec EPERM (sshfs UID 501 + sandbox boundary). MEMORY.md
  reference_secret_cli + reference_aiden_python3_routing 정합 — orchestration
  helper 가 resource TCP framework 경유해야 access 가능.
- 결과: **runpod.api_key 직접 fetch 불가 from this agent context.**

### 1.5 CE-track pipeline
- audit §5.2 finding 재확인: `anima_clm_invoke.hexa` 는 *inference wrapper*,
  *training* loop / optimizer / dataset / checkpoint script 미land.
- prereq spec §5 Step 2 "CLM train P=100M, init_seed=0..3" 실행을 위한
  training pipeline source 부재 → Gate B 측정 자체 불가능.

## 2. Critical blockers (5)

### B1 — anima_phi_star.hexa 자체 interp 실패 (★ 가장 치명적)

probe 결과:
```
$ hexa run tool/anima_phi_star.hexa --selftest
error: auto-invoke conflict — `fn main()` is auto-called by hexa-strict
       AND a top-level `main()` call was found, which would run main() twice
       in the interp path (codegen suppresses but interp deliberately double-calls).
hint: remove the explicit `main()` call (auto-invoke handles it)
hint: OR add `@manual_main` attribute on `fn main` to opt out of auto-invoke
ref: silent-failure-enforcement Class 1 (doc/audit/silent_failure_enforcement_audit.md)
```

→ hexa-strict 의 silent-failure-enforcement Class 1 (auto-invoke 중복) 에
   걸려서 `--selftest` / `--help` / no-args 모든 invocation 이 *interp 단계*
   에서 reject. tool source edit 필요:
   - 옵션 (a) `tool/anima_phi_star.hexa` 끝의 `main()` 호출 삭제 (auto-invoke 만 사용)
   - 옵션 (b) `fn main()` 위에 `@manual_main` attribute 추가
- 권고: (a) — minimal edit, audit §5.8 의 file-name + JSON schema back-compat 유지.

### B2 — Mistral-7B model cache 부재 (Linux side)

- HF cache 에 Mistral-7B-v0.3 weight 미존재. RunPod 보내거나 local download
  (auth token + ~14 GB) 둘 다 추가 prereq.
- 권고: RunPod A100 with HF token pre-warmed image — calibration spec §5.7.4
  cost $5-15 / wall ~53 GPU-min 정합.

### B3 — Local GPU VRAM 부족 (RTX 5070 12 GB)

- fp16 Mistral-7B forward ~14 GB → OOM. int8 quantization 적용 시 ~7 GB 가능
  but anima_phi_star.hexa 의 method (last-layer hidden state covariance) 가
  quant 적용 후에도 동일 σ_Φ 분포 산출하는지 별도 audit 필요.
- 권고: calibration 은 RunPod A100 (40/80 GB) 에서 수행 — VRAM headroom 확보.

### B4 — RunPod credential access 불가 from this sandbox

- `secret get runpod.api_key` 호출이 sandbox sshfs UID 501 boundary 로 EPERM.
- 권고: 메인 process (user side, Mac shell) 에서 직접 RunPod dispatch 또는
  resource TCP framework 경유 orchestration. autopilot.hexa 는 panic stub
  (MEMORY.md reference_runpod_pipeline) — anima_runpod_orchestrator.hexa 사용
  필요.

### B5 — CE-track CLM training pipeline 미land

- audit L6 + §5.2 finding: 4-scale {1M, 10M, 100M, 1B} 새로 train 하는 script
  부재. prereq spec §5 Step 2 ("CLM train P=100M, init_seed=$seed") 의 실측
  pipeline source 없음.
- 권고: P=100M scale CLM trainer (Chinchilla 20× token, deterministic seed)
  별도 implementation cycle — 본 calibration 의 *sub-prereq* (calibration 의
  prereq).
- **B5 status update (2026-05-12, cycle 6 #P)**: B5 spec + Phase 0 scaffolding
  landed at `state/clm_ce_4scale_trainer_2026_05_12/spec.md` (3-scale base
  {1M, 10M, 100M} + 1B deferred lane). Status transitioned **BLOCKED →
  RESOLVED-SPEC**. Actual training pipeline implementation (Python script +
  RunPod orchestrator) is cycle 7+ scope, cost $210-600 dual-seed 3-scale.

## 3. What would have happened if executed (estimate)

| Step | est cost | est wall | est outcome |
|------|---------|---------|------------|
| Φ-track 64 seed × 1 cell (N=64) on RunPod A100 | $5-15 | ~53 GPU-min | σ_Φ_rel ~ 0.05-0.15 expected (audit §4.3 hypothetical) |
| CE-track 4 init-seed × P=100M train | $10-30 | ~4 GPU-h | σ_CE_rel ~ 0.02-0.08 expected |
| harness.py re-tune + Model A/B re-fingerprint | $0 | ~10 min CPU | Gate C verdict |
| **total** | **$15-45** | **1-2 h wall** | Gate A/B/C verdicts |

→ parent spec cost lane 정합. 그러나 위 5 blocker 가 *모두* 해소되어야
실행 가능. B1 (hexa interp bug) 은 *single line edit* 으로 즉시 해소 가능
— 가장 cheap fix.

## 4. Next-cycle resolve path

### 4.1 단기 (next cycle 진입 전, $0 cost)

1. **B1 fix**: `tool/anima_phi_star.hexa` 끝의 `main()` 호출 line 제거
   (또는 `@manual_main` attr 추가) — *single line edit*, separate commit.
   smoke test: `hexa run tool/anima_phi_star.hexa --selftest` exit 0 확인.
2. **B5 audit**: `anima_clm_invoke.hexa` training-side land 여부 deeper
   audit — training pipeline 별도 implementation cycle 필요 여부 결정.
3. **B4 resolve**: 메인 process side 에서 runpod.api_key + HF token 확인,
   `anima_runpod_orchestrator.hexa` dispatch path 검증.

### 4.2 중기 (calibration 실행 cycle)

4. **B2 + B3 resolve**: RunPod A100 instance (40 GB+) with Mistral-7B-v0.3
   pre-warmed image + HF token. 4-scale CLM trainer container도 동시 prep.
5. **calibration actual run**: prereq spec §5 Step 1-3 protocol 그대로
   ($15-45 budget, 1-2 h wall).
6. **Gate A/B/C 평가 + harness.py σ default 재튜닝** (separability ≥ 50× 재확인).

### 4.3 후속 (decisive run cycle)

7. Gate A/B/C PASS 시 cycle 5 #1 15-cell decisive run 진입 ($121-420, 1-2 day).

## 5. Cost / time / value tag (next cycles)

| candidate | cost | time | value |
|-----------|------|------|------|
| B1 single-line fix + smoke | $0 | ~10 min | enables all downstream |
| B5 CE training pipeline impl | $0 (dev) | 0.5-1 day | unblocks Gate B |
| B4 RunPod credential setup verify | $0 | 0.5-1 h | unblocks dispatch |
| Calibration actual run | $15-45 | 1-2 h GPU | resolves L1 critical |
| 15-cell decisive run | $121-420 | 1-2 day | H_080 Conflict Resolved |

## 6. Cross-Links

- **parent prereq**: `noise_calibration_prereq_2026_05_12.md` (138 lines, protocol source)
- **parent spec**: `spec.md` §5.7.4 (cost lane)
- **parent audit**: `spec_audit_2026_05_11.md` §1.2 / §4 / §5.2 (CE capability zero, CLM pipeline untracked)
- **tool**: `tool/anima_phi_star.hexa` (Φ-track engine — B1 interp blocker)
- **CE wrapper**: `tool/anima_clm_invoke.hexa` (training-side B5 blocker)
- **orchestrator**: `tool/anima_runpod_orchestrator.hexa` (B4 dispatch path)
- **H_080**: `hypotheses/H_080_topo_24variants.md` §Conflict Resolution Pending
- **NEXT.md**: cycle 5 §4 #J 본 agent task source

## 7. Honest Limits (≥ 5)

- **L1**: B1 의 single-line fix 가 *실제로* tool 동작 복원하는지 미확인 — fix 적용
  후 selftest 실패 가능성 (deeper interp issue). 권고: fix 적용 후 별도 smoke.
- **L2**: B3 (VRAM 12 GB) 의 int8 quant 적용 시 σ_Φ 분포 변화 정량 미측정.
  RunPod A100 path 가 default 권고이므로 quant 분기 별도 cycle.
- **L3**: cost estimate $15-45 는 RunPod A100 spot price 가정 — 실제는 ±50 %
  변동 가능 (audit L3 동일 caveat 재확인).
- **L4**: 본 dryrun-blocker 는 *Linux sandbox side* probe — Mac side 에서
  `secret` + `anima_runpod_orchestrator` 경유 실행 시 다른 blocker 발견 가능
  (e.g., RunPod quota, HF gated model permission).
- **L5**: B5 (CE training pipeline) 의 land 여부 deeper audit 부재 — anima
  repo 내 별도 train script (e.g., `tool/anima_clm_train*.hexa` 또는 python)
  존재 가능성 본 agent 미탐색. 권고: B5 resolve 시 grep `train.*loop|optimizer|
  checkpoint_save` 로 잠재 source 발견 후 결정.
- **L6**: 5 blocker 중 B1 만 *low-cost dev fix* — 나머지 4 는 actual GPU /
  credential / pipeline land 필요. **critical path = B1 + B5** (둘 다 $0 dev
  fix). B2/B3/B4 는 RunPod execution lane 의 routine prereq.

---

**Conclusion**: Φ×CE 실측 cycle 진입 **불가능 — 5 blocker (B1-B5) resolve 후
재진입 가능**. **B1 (single-line hexa fix)** 이 *critical path bottleneck* —
이 fix 없이는 anima_phi_star.hexa 자체가 silent-failure-enforcement Class 1
로 reject 되어 어떤 calibration 도 불가. B1 + B5 resolve = $0 dev work, B2-B4
= RunPod execution routine.

**다음 진행할 것들** (3-5 items + cost/time/value tag):

1. **B1 fix** — `tool/anima_phi_star.hexa` auto-invoke 충돌 해소 (single line
   edit, $0 / 10 min / critical-path) ★ priority 1
2. **B5 audit** — CLM training pipeline land 여부 deeper audit ($0 / 30-60
   min / unblocks Gate B)
3. **B4 verify** — runpod.api_key + anima_runpod_orchestrator dispatch path
   smoke test ($0 / 30 min / unblocks GPU lane)
4. **calibration RunPod dispatch** — B1-B5 resolve 후 ($15-45 / 1-2 h / L1
   critical 해소)
5. **15-cell decisive run** — Gate A/B/C PASS 후 ($121-420 / 1-2 day / H_080
   Conflict Resolved)

---

**lock policy reminder**: chflags +uchg/+schg/chattr +i 적용 *금지*. unlock 된 파일 *재잠금 금지*.
**commit policy**: 본 dryrun-blocker 는 *separate commit 금지* — 메인 process 가 일괄 commit.
