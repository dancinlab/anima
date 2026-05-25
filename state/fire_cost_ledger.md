# fire_cost_ledger — runpod saga-level $ + ETA ledger (anima, PURE 도메인)

## § 헤더

본 ledger 는 anima 측 runpod fire 의 saga-level cost / ETA / result 를 단일 SSOT 로 적재한다. 기존 분산된 cost 기록 (`HEXAD/LORA/COST_LEDGER_SESSION3.md` · `HEXAD/PURE/AXIS_MAP_BUG_POSTMORTEM*.md` · 각 fire 의 `dispatch.log` · memory `project_lora_session_2026_05_22.md`) 을 본 문서가 cross-ref. 신규 fire 가 발사될 때마다 ## § Cycle 섹션 1개 추가 + ## § Cumulative 갱신 한다.

scope = anima repo 발사 fire 만 (HEXAD/LORA + HEXAD/PURE 두 saga). hexa-lang / hexa-cloud 측 fire 는 본 ledger 범위 밖.

## § Cumulative snapshot (as of 2026-05-24 KST late, post-PR #412)

| 합산 항목 | 값 | 근거 |
|---|---|---|
| 누적 fire 수 | **20** (LORA 15 wave + PURE 5 today) | 아래 entries · v2b LOST 갱신 후 신규 fire 0 |
| 누적 cost | **~$23-32** | LORA $22-26 (#360) + PURE today $1-6 (v1 ~$1.5 + v2b ~$1.5 + rogue + E2/E3) |
| LOST/TIMEOUT 건수 | **4** | R8a SSH-drop · Phase D v1 stale-branch · AXIS_MAP E OOM · **Phase D v2b 사용자 cleanup** |
| LOST/TIMEOUT 비율 | **20%** (4/20) | v2b 추가로 +5% |
| worst-incident | **AXIS_MAP 1차 envbug $8 burn** (PR #211) | 단일 saga 최대 단일 burn; 단일 ckpt 손실은 v1+v2b 두 번 (~$3 누적) |
| 본 ledger 비용 | **$0** (Mac local doc) | — |

cross-ref postmortems: PR #211 (envbug saga) · PR #248 (E OOM addendum) · PR #378 (Phase D v1 stale-branch) · **PR #412 (PHASE_D_BLOCKERS_CLOSURE — v1+v2b 두 fire LOST 후 synthetic framework 완성 deferred marker)**. hexa-lang inbox: #629 · #646 · #699 · #700 · #728 (5 patches 시리즈).

---

## § Schema

```
### YYYY-MM-DD · <variant>
- pod_id        : <runpod id>
- gpu           : <type>
- cost_estimate : ~$X (rate $Y/hr × Z hr)
- cost_actual   : ~$X | UNKNOWN (terminated externally · early-stop · 등)
- eta_planned   : <분>
- eta_actual    : <분>
- result        : SUCCESS | FAIL | LOST | TIMEOUT | CRASH | IN_FLIGHT
- lessons       : 1-3 줄
- lineage       : <prior fires/PRs>
- dispatcher    : hexa | legacy.sh | other
```

`SUCCESS` = result.json 회수 + closure pass. `FAIL` = 회수 OK 지만 closure 실패. `LOST` = ckpt 미회수 (외부 terminate / pull fail). `CRASH` = OOM / argparse-error / import-error 등 early-stop. `IN_FLIGHT` = poll 중. cost_actual 은 dispatcher exit time − pod_create time 으로 측정 가능한 경우만, 외부 terminate 는 wall ±10 분 추정.

---

## § Cycle entries — PURE today (2026-05-23 ~ 2026-05-24)

### 2026-05-23 · Track 1 E2 (wiki_frac=0.5)

- pod_id        : 4nrcm80g8fwqf7
- gpu           : NVIDIA A100-SXM4-80GB
- cost_estimate : ~$0.90 (~$1.49/hr × ~0.6 h, wall 2105.83 s)
- cost_actual   : ~$0.87 (wall 2105.83s × $1.49/hr / 3600)
- eta_planned   : ~35 분 (5000 step · bsz=2 · block=512)
- eta_actual    : 35.1 분 (train_wall_s=2105.83 from result.json)
- result        : FAIL (closure 0/5 ≥ PARTIAL, ko=PURE_MEMORIZE register collapse)
- lessons       : (1) wiki=0.5 dilution 만으론 anima register collapse 해결 못함; (2) corpus_s101 M3 TTR=0.03 극단 반복이 진짜 sink (PR #340); (3) init→final CE 14.18→0.98 정상 수렴, closure 는 multilingual_probe 단계에서 실패
- lineage       : PR #301 (result row) · PR #310 (forensics) · PR #340 (TTR 실측)
- dispatcher    : legacy.sh (`dispatch_p21h_v3_runpod.sh` cycle 1 redispatch)

### 2026-05-23 · Track 1 E3v3 (wiki_frac=1.0)

- pod_id        : 7dt6k35zd58o1o (재발사 분, original f5c0kn54wuqgfl)
- gpu           : NVIDIA A100-SXM4-80GB
- cost_estimate : ~$2.20 (~$1.49/hr × ~1.5 h 가정 full 5000 step)
- cost_actual   : ENV_PASSTHROUGH_FAILED — pod 1차 시도 CRASH 후 재발사 완주
- eta_planned   : ~45 분 (5000 step)
- eta_actual    : ~90 분 (재발사 포함 누적, 단일 path wall 미회수)
- result        : FAIL (closure 1/5 ≥ PARTIAL, ko 만 PARTIAL; register_hits 0/20 vs E2=4/20 → wiki dilution 이 register collapse 는 막지만 generalize 약화)
- lessons       : (1) wiki=1.0 endpoint 가 H_242 frozen f_c 부분 falsify; (2) corpus 축 단독으론 double-bind closure 불가 → AXIS_MAP fallback A 커리큘럼(#238) 우선; (3) 1차 ENV_PASSTHROUGH_FAILED 가 env-var-concat 가족 (#211) 변종 신호
- lineage       : PR #344 (Phase D spec trigger) · PURE.log.md 2026-05-24 closure 결론
- dispatcher    : legacy.sh

### 2026-05-24 · Phase D v1 (stale-branch fire)

- pod_id        : 7rhh18i1h1klcp
- gpu           : NVIDIA A100-SXM4-80GB
- cost_estimate : ~$1-2 (~$1.49/hr × ~1.5 h, 외부 terminate 전까지)
- cost_actual   : ~$1.50 ±0.50 (사용자 carryover sweep 중 외부 terminate, billing 직접 회수 안 됨)
- eta_planned   : ~45 분 (5000 step · `--corpus-path` Phase D corpus 86 MB)
- eta_actual    : ~90-100 분 (T0+~100 분 진단 시작 시점까지)
- result        : LOST (ckpt 미회수, result.json 부재, `[result_pull] FATAL scp exit 1`)
- lessons       : (1) **stale worktree branch** 가 PR #372 (`--corpus-path`) + PR #373 (`sources_upload`) 둘 다 부재 → dispatcher invariant 가 "all green" 으로 잘못 보고; (2) `--corpus-path` 가 positional `variant` slot 으로 silently 흡수 (argparse 안전망 무효); (3) `sources_upload` no-op stub 의 exit-0-OK pattern = contract-strength invariant 부재
- lineage       : PR #366/#372/#373 (prereq commits 미흡수) · PR #378 BUG_POSTMORTEM F · 재발 방지 PR #381 (PREFIRE_WIRING_AUDIT_CHECKLIST)
- dispatcher    : hexa (`HEXAD/PURE/launchers/dispatch_p21h_v3.hexa` stale-branch 버전)

### 2026-05-24 · Phase D v1 rogue (idle cleanup)

- pod_id        : ikgrx13pw5icmk
- gpu           : NVIDIA A100-SXM4-80GB (idle 추정)
- cost_estimate : <$0.10 (v2 첫 실패 시도 직후 idle 상태)
- cost_actual   : UNKNOWN (wall time 직접 미회수, idle burn rate 상한 추정)
- eta_planned   : n/a (실패 시 즉시 cleanup 의도)
- eta_actual    : ~10-20 분 idle
- result        : CRASH (v2 agent 첫 실패 → idle pod 잔존 → recovery 단계 cleanup terminate)
- lessons       : (1) failed dispatch 직후 pod terminate 가 자동화되지 않으면 rogue idle 잔존; (2) bg agent 의 신규 pod 식별이 늦으면 사용자 cleanup 까지 누적; (3) dispatcher fail path 의 명시적 `runpodctl remove pod $id` 호출 검토 필요
- lineage       : Phase D v1 (7rhh18i1h1klcp) recovery cycle · PR #378 § 부가 사고 (a)
- dispatcher    : hexa (v2 agent 첫 시도)

### 2026-05-24 · Phase D v2b (사용자 cleanup 으로 LOST, ledger 갱신 2026-05-24 KST late)

- pod_id        : b23g2abvbphz33
- gpu           : NVIDIA A100-SXM4-80GB
- cost_estimate : ~$1.5-2 (~$1.49/hr × ~1 h, steps=2000)
- cost_actual   : ~$1.50 ±0.30 (사용자 carryover sweep 으로 외부 terminate · billing 미회수)
- eta_planned   : ~20-30 분 (steps=2000 · 짧은 sweep)
- eta_actual    : ~25-45 분 (terminate 시점 추정, result.json 도착 전)
- result        : **LOST** — 사용자 carryover sweep 중 b23g2abv 포함 다수 pod terminate · result.json 미회수 · Monitor blvdsmuiv 가 `[cloud] scp exit 1` false-success → 새 Monitor bbsrt11v9 도 timeout, ckpt 사라짐
- lessons       : (1) dispatcher 자체는 main 위 clean 발사 (PR #372/#373 통합) → v1 의 stale-branch 사고와 직교; (2) **외부 terminate (사용자 cleanup) 가 SAVE_POD=1 무력화** = runpod-side owner_lock 부재 (hexa-lang inbox #646 F5 권장 변종); (3) `hexa cloud copy-from` 의 exit 0 false-success (remote file missing 시) 발견 → hexa-lang inbox #699 등재; (4) ckpt 미회수 = COFFESHOP 4-criterion 실 데이터 부재 확정, synthetic baseline (PR #405) 만으로 framework 검증 완성
- lineage       : Phase D v1 (LOST recovery) · PR #380 (dispatcher wait-loop) · PR #410 (B14 fire-sanity Phase 2) · PR #412 (PHASE_D_BLOCKERS_CLOSURE)
- dispatcher    : hexa (`HEXAD/PURE/launchers/dispatch_p21h_v3.hexa` main 머지 후)

---

## § Cycle entries — LORA R8/R8a backfill (2026-05-22 ~ 2026-05-23)

본 섹션은 `HEXAD/LORA/COST_LEDGER_SESSION3.md` (PR #360) 의 cumulative 항목 중 **LOST/TIMEOUT/incident** 항목만을 saga-level 로 재기록. 정상 SUCCESS/FAIL 항목 (Wave 12-16 등) 은 그쪽 ledger 가 SSOT, 본 ledger 는 cross-ref 만.

### 2026-05-23 · R8a fire (SSH drop, LOST)

- pod_id        : (id 미회수, dispatch.log 부재)
- gpu           : NVIDIA A100-SXM4-80GB (R8 saga 표준)
- cost_estimate : ~$1.20 (~$1.49/hr × ~30 분 가정 SSH drop 시점)
- cost_actual   : ~$1.20 sunk (LORA cost ledger SSOT)
- eta_planned   : ~60 분 (R8 base+warm init 표준)
- eta_actual    : ~30 분 (SSH drop, no result)
- result        : LOST (SSH drop · result.json 미회수)
- lessons       : (1) R8 saga 의 wiring 버그 발견 trigger; (2) SSH drop 직후 자동 retry 부재 → 1.20 sunk; (3) R8a' relaunch 로 closure 회수 (cycle 16-3)
- lineage       : LORA R8 saga · COST_LEDGER_SESSION3 § "R8a fire LOST" · R8a' relaunch (#385 cycle 16-3 H_257 retry)
- dispatcher    : legacy.sh

### 2026-05-22 ~ 2026-05-23 · LORA 15-cycle saga summary

- pod_id        : 15 개 별도 (vP21M_v9 ~ wave-17 v15 등)
- gpu           : NVIDIA A100-SXM4-80GB (community/secure 혼합)
- cost_estimate : ~$4.80 (15 LoRA cycles, memory.project_lora_session_2026_05_22)
- cost_actual   : ~$22-26 누적 session-3 (`COST_LEDGER_SESSION3` SSOT — wave 12-16 + V3 Phase 2 + AXIS_MAP envbug + R8a/a' 포함)
- eta_planned   : 각 ~5-90 분 (wave 별)
- eta_actual    : 분포 — wave 12-16 ~5 분 / V3 Phase 2 full 7367s / AXIS_MAP envbug ~7×30 분 / redispatch 4× ~45-90 분
- result        : 혼합 — 15/15 회수 (LoRA wave 12-16) · production = 1.5B hot-swap router (anima 0.12.0 LIVE on chat.dancinlab.org)
- lessons       : (1) register-leak 의 81% 가 EN-emission 문제 (N8); (2) wiki_frac 이 register 의 진짜 lever (0.30→7, 0.50→4 on 1.5B; 3B fresh 0.30→3 등); (3) 3B-Instruct register ceiling ~5/20, non-Instruct Qwen2.5-3B 가 깸; (4) 3B base robust — ko-only 500-step keep all 5 langs STRONG; (5) production 은 15 cycle 후에도 1.5B router — register fix 는 corpus-side
- lineage       : memory `project_lora_session_2026_05_22.md` · PR #144/#150/#162/#184/#205 (wave 시리즈) · production deploy (anima_participant.py P2 router)
- dispatcher    : legacy.sh + hexa (혼합)

### 2026-05-23 · R8a'' / R8b / R8c 자연실험 sweep

- pod_id        : multiple (R8a'' fill-in + R8b LORA on Qwen + R8c 4-cell probe)
- gpu           : NVIDIA A100-SXM4-80GB
- cost_estimate : ~$3-5 (R8c probe + R8a'' fill-in · in-flight or completed 분 cumulative 정밀화 PENDING)
- cost_actual   : R8c cell-3 noise σ=0.1 → adamw8bit step time 5x penalty root cause (PR #386); R8a'' fill-in PRE-FIRE template (PR #382)
- eta_planned   : 변동 (probe 별 다름)
- eta_actual    : R8c probe completed (PR #374 verdict, init_CE 14+ floor 재현 실패 → H_255 measurement artifact 가설 trigger)
- result        : FAIL (R8c 4-cell verdict) / TEMPLATE (R8a'' PRE-FIRE)
- lessons       : (1) R8c 의 init_CE 14+ floor 가 measurement artifact 가설로 reframe (H_255); (2) AXIS_MAP-FAN re-fire 4/7 verdict: H_257 PASS, H_255 / H255.2 부분 FALSIFIED (PR #383); (3) cycle 16-3 H_257 retry 가 6 AXIS-MAP env-var wiring fix 필요 (PR #385)
- lineage       : R8 saga reframing (PR #377) · BUG_POSTMORTEM 가족 (PR #211/#248/#378)
- dispatcher    : legacy.sh + hexa

### AXIS_MAP-FAN envbug 1차 (cross-ref incident, 2026-05-22 ~ 2026-05-23)

본 entry 는 PR #211 의 자세한 postmortem 을 saga-level 로 cross-ref. 자세한 evidence 는 `HEXAD/PURE/AXIS_MAP_BUG_POSTMORTEM.md` 참고.

- pod_id        : 7 axes × ~1.15 평균 (kill 전 idle/crashed)
- gpu           : NVIDIA A100-SXM4-80GB (7 pods)
- cost_estimate : ~$8 (1st/2nd fan-out 낭비)
- cost_actual   : ~$8 sunk
- eta_planned   : ~45-90 분 each
- eta_actual    : 7 pods 모두 launch 직후 argparse crash, idle 상태로 청구 누적
- result        : CRASH (caller-side env-var-concat: `P21H_STEPS="5000 P21H_BSZ=2 ..."` single quoted)
- lessons       : (1) multi-var env-set 은 shell trap 이지 framework bug 아님 — dispatcher 의 `nohup env $AXIS_ENV $CMD` 는 무결; (2) `.envbug_<unix_ts>` archive rename 이 forensic trail 보존; (3) dispatcher echo-header 가 argparse error 보다 빨리 quoting 오류 노출 → 향후 token count assertion 검토
- lineage       : PR #204 (CALLER WARNING block) · PR #211 (postmortem doc) · PR #248 (E OOM 후속 addendum)
- dispatcher    : legacy.sh (caller anti-pattern, dispatcher 무결)

### AXIS_MAP-FAN E axis OOM (cross-ref, 2026-05-23)

PR #248 postmortem 의 saga-level cross-ref. evidence 는 `HEXAD/PURE/AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23.md`.

- pod_id        : a5qud7f6g10kup
- gpu           : NVIDIA A100-SXM 80 GB
- cost_estimate : ~$1.10 (~$1.49/hr × ~50 분)
- cost_actual   : ~$1.10 sunk
- eta_planned   : ~45 분 (P21H_LANG_BALANCED=1)
- eta_actual    : ~50 분 (OOM 무한루프 + kill)
- result        : CRASH (CUDA OOM, no result.json — LangBalancedSampler GPU mem leak 가설; 60 GiB allocator 외부 누적)
- lessons       : (1) LangBalancedSampler 가 per-lang corpus segment 를 GPU resident 로 유지하며 round-robin index 회전 → 1,200 step 누적 후 80 GB 임계 도달; (2) `expandable_segments:True` 는 mitigation 일 뿐 fix 아님; (3) 권장 fix = sampler CPU-side index + lazy GPU transfer per batch (g0 단순성)
- lineage       : AXIS_MAP redispatch C/C2/D/E 중 E (다른 3 = closure FAIL but result OK)
- dispatcher    : legacy.sh (cycle 1 redispatch, env-var 올바름 + runtime leak)

---

## § Trend / patterns (load-bearing for next cycle)

1. **LOST/TIMEOUT 3건 / 20 = 15%** — 모두 **dispatcher / env / branch hygiene** 원인, training-side bug 아님. 즉 lesson 은 모두 fire-front 강화 (PR #381 PREFIRE_WIRING_AUDIT_CHECKLIST · PR #380 dispatcher wait-loop · PR #373 sources_upload 강화).
2. **envbug + E OOM + Phase D v1 = 3 직교 실패 모드** — caller-side env-concat (#211) · runtime CUDA OOM (#248) · stale-branch silent invariant (#378). dispatcher 동일성 외 공통 원인 없음. 한 PR 가 모두 막을 수는 없음.
3. **단일 ckpt 손실 최대 = Phase D v1 (~$1-2 + 1.5h wall + 0 산출물)** — corpus design + 8-factor wiring 시간투자가 dispatcher staleness 한 줄로 zero 됨. branch validation `git merge-base --is-ancestor <prereq_sha> HEAD` 가 prevent.
4. **단일 saga 최대 burn = AXIS_MAP envbug ~$8** — caller 의 1차 + 2차 동일 anti-pattern 반복. dispatcher echo-header 의 stderr 미러 + token count assertion 가 조기 차단 검토.
5. **production = 1.5B hot-swap router** 가 15-cycle 후에도 우위 — 비용 절감 압력 ≠ scale-up 동기. user directive `feedback_no_scale_caps` 가 fire 강도는 풀지만, **post-fire cost-per-finding** 측정은 본 ledger 의 valid lens.

## § Honest C3

1. `cost_actual` 의 Phase D v1 / rogue / R8a 는 외부 terminate / SSH drop 으로 runpod billing 직접 회수 안 됨 — ±$0.5 추정.
2. R8a'' / R8b / R8c sweep cost 는 in-flight 분 + completed 분 혼재로 cumulative 정밀화 PENDING (R8a'' fill-in 완료 후 갱신).
3. v2b entry 는 in-flight placeholder — result.json 회수 후 lessons / eta_actual / cost_actual 갱신 필요.
4. LORA 15-cycle saga 의 ~$4.80 (memory) vs $22-26 (#360) 불일치 = $4.80 은 v3 production-deploy 직전 chunk만, $22-26 은 V3 Phase 2 + AXIS_MAP envbug 포함 (각 ledger 의 scope 차이; 본 ledger 는 양쪽 cross-ref 만 하고 단일 합산 주장 안 함).
5. rogue pod `ikgrx13pw5icmk` 의 wall time 직접 확인 안 됨 — 본 ledger 의 `<$0.10` 은 idle burn rate 상한.
6. AXIS_MAP envbug $8 추산은 PR #211 의 "7 axes × 평균 ~$1.15" 의 단가 평균 가정에 의존 — 7 pod individual billing 미회수.
7. LORA hot-swap router production cost 는 본 ledger 범위 밖 (deploy 자체는 mini host local, runpod fire 아님).

## § Cross-reference

- `HEXAD/LORA/COST_LEDGER_SESSION3.md` (PR #360) — LORA 측 SSOT, 15-wave detail
- `HEXAD/PURE/AXIS_MAP_BUG_POSTMORTEM.md` (PR #211) — envbug 1차
- `HEXAD/PURE/AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23.md` (PR #248) — E OOM
- `HEXAD/PURE/AXIS_MAP_BUG_POSTMORTEM_F_PHASE_D_V1_2026_05_24.md` (PR #378) — Phase D v1 stale-branch
- `HEXAD/PURE/PREFIRE_WIRING_AUDIT_CHECKLIST.md` (PR #381) — silent-bypass 재발 방지
- hexa-lang `inbox/patches/cloud_bootstrap_sources*.md` (#629) — bootstrap verb 흡수
- hexa-lang `inbox/patches/cloud_guard_ux*.md` (#646) — cloud-guard + pod-lock
- memory `project_lora_session_2026_05_22.md` — 15-cycle saga narrative
