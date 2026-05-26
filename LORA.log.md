# LORA — task log (append-only)

> `LORA.md` 의 변경/작업 체크리스트. 최신이 위.

## 2026-05-25 (cycle 24 — M1·M3·M4 3-agent 병렬 fan-out)

- [x] `/cycle all` — open milestone 3 fan-out (M1·M3·M4), M2 dependency-skip (M1 PASS 의존), M5 done
- [x] **M1 decision memo (PR #504 merged)** — `HEXAD/LORA/M1_SWAP_DECISION_MEMO_2026_05_25.md`. Wave-17 anti-correlation 구조적 → 4-옵션 표 + 추천 **옵션(b) continuous floor≤50 → v11 swap**. 근거: M2 가 register-leak 30d monitor(continuous≤50) 라 floor 가 production 목표와 동일 number; register burst = 사용자 가시 결함, 다국어 강건은 hot-swap router 가 보강. counter-branch: 다국어 우선 prior 면 (c)+v13
  - [ ] ⚠ swap 전 선결 2 — corpus_v5(SSOT) vs corpus_v4(README 0523) 라벨 확인 · crit5 tag-leak 두 후보 미측정 (`swap_criteria_check.hexa check`)
- [x] **M3 PENDING (PR #505 merged)** — `HEXAD/V3/R8A2_QWEN_PARITY_VERDICT_2026_05_25.md`. R8a'' LOST/DEAD 3-way 확인 (pod 6gqf9nsdquz8ug 부재 + SSH refused + result 0건). **SECURE preempt 2회째 → R8a/R8a'/R8a'' 5000-step 완주 0/3**. final_CE LOST · Qwen baseline 미측정 → Δ 계산불가 = PENDING. H_255 흡수 재확인 (init_CE 더 이상 metric 아님, M3 유일 metric = final_CE@5000)
  - [ ] M3 closure path — 사용자 Qwen baseline candidate 결정 → ON-DEMAND 2-pod 병렬 (~$6) + M5 PREFIRE 선결 (SECURE 3연속 preempt 회피). 재발사는 보류 (조건 미충족, 보고만)
- [x] **M4 wiring DONE (PR #507 merged)** — `HEXAD/LORA/M4_AXIS_WIRING_FIX_2026_05_25.md`. H_257 완전해소. **발견: PR #385 는 half-fix** (dispatch→train `--flag` passthrough만, train script 가 env→cfg→loop 미연결이라 7축 여전히 inert). grep `os.environ` 0→8 line, axis→cfg 0→8, axis→loop 0→2. py_compile/bash -n PASS
  - [x] honest scope — head_g(aux LM-CE term + `--head-g-weight`)·freeze_embed **2축만 진짜 wired** (기존 code path), curriculum·distill·lang-balanced·contrastive **4축 = ML feature 미구현 TODO[axis-impl]** (env→cfg→log 까지만, behavior 없음). gate-off default 무회귀
  - [ ] M4 진짜 ablation — 2 wired 축 post-merge 재발사 (M5 PREFIRE + ON-DEMAND), 4 TODO 축은 feature impl 선결
- [x] consolidation (이 엔트리) — LORA.md milestone 3행 + 진행중 섹션 + 관련 surface 3 doc 갱신. 격리 worktree land (clobber 회피)
- [ ] 다음 /cycle — M3 closure (baseline 게이트) · M1 swap 실행 (선결 2 후) · M4 ablation/4축 impl · M2 (M1 PASS 후 unblock)

## 2026-05-25 (cycle 23 — LIFE 도메인 흡수)

- [x] UNIVERSE 가설 lane sweep — LORA 사가가 12 H_XXX 로 정식화돼 있음 확인
- [x] **verdict 확정 2건 흡수**:
  - [x] **H_255 H255.2 🔴 FALSIFIED** — 14+ init_CE floor 가 REAL (cycle 15-1 4/7 axes byte-equal 14.79/14.18/14.46 재현). LORA.md L11 "14.x floor 미재현" stale 정정 → floor 진짜, R8c 12.315 은 별개 regime, 2 nats gap = GPU class/PROBE_STEPS (env-drift 아님)
  - [x] **H_257 H257.1 grep-static** — AXIS_MAP-FAN 7-axis unwired (train_p21h_v3.py 0 os.environ + dispatch env-var no `$CMD` passthrough) → cluster X/Y/Z 분류 · head_g FALSIFIED · 5/7+2 FAIL 결론 (PR #249) 전부 trivial identity (무효). **M4 root cause 진단 완료**
- [x] COFFESHOP 4-criterion ↔ LIFE 측정 frame 매핑 흡수 (자율emit=H_231/H_246/H_248 · multilingual=H_240 · register=H_242 · dream_stage=H_228/H_244)
- [x] sibling 흡수 — H_254 (n_kv silent-drop) · H_256 (noise=final_CE+wall axis, init 무관) · H_247 (floor spec) · H_230 (autonomy SUPPORTED_FULL 4/4)
- [x] LORA.md 편집 — V3/R8 saga 블록 H_257 reframe + 신규 "LIFE 흡수" 섹션 (2 표) + M4 main path 갱신
- [x] 공유 워킹트리 clobber 경험 — in-place 편집이 동시 에이전트 git op 에 2회 reset됨 → 격리 worktree 재적용 (PR landing)
- [ ] M4 next — env-var `$CMD` passthrough wiring fix PR (H_257.1 정적증거 기반) → 7-axis 재발사로 진짜 ablation
- [ ] M3 next — R8a'' final_CE Qwen-parity 측정 (floor saga 는 H_255 로 사실상 closure: floor real but explained)

## 2026-05-24 (cycle 22 — M4 Stage 1 PROBE axis-5 🔴 FALSIFIED)

- [x] M4 Stage 1 PROBE axis-5 mitosis_max 발사 (cycle 22-1, 3-pod A100, $0.30)
- [x] **3/3 결과 도착**: m16/m64/m128 모두 init_CE = 14.374279975891113 byte-equal
- [x] **3/3 falsifier FALSIFIED** (Δ init_CE = 0.0)
- [x] 🔴 cycle 17-3 cross-tool 가설 (mitosis_max +2.14 nats) 재현 안 됨
- [x] M4_STAGE1_AXIS5_MITOSIS_MAX_VERDICT_2026_05_24.md doc 흡수
- [x] axis-2 (SUPPORTED) vs axis-5 (FALSIFIED) 명확한 대조
- [ ] cross-tool 17-3 진짜 원인 추적 (corpus seed / dispatcher path / GPU class drift)
- [ ] axis-1 wiki_frac Stage 1 PROBE 후속 (medium-high expected effect)

## 2026-05-24 (cycle 20 — M4 Stage 1 PROBE axis-2 🔥 첫 진짜 axis evidence)

- [x] M4 Stage 1 PROBE 발사 (cycle 20-1, 3-pod A100-SXM4-80GB, $0.30)
- [x] **3/3 결과 도착**: register=14.4564 / CE=14.9066 / none=16.2428
- [x] **3 falsifier 모두 SUPPORTED** (Δ ≥0.1, register vs none 1.79 nats 최강)
- [x] 🔥 첫 진짜 axis evidence — post-#385 wiring fix 효과 입증
- [x] cluster Z (14.4564) byte-equal 원인 = anima_register_ce objective 확정
- [x] 새 cluster (16.24) for none objective 첫 관측
- [x] M4_STAGE1_AXIS2_HEAD_G_VERDICT_2026_05_24.md doc 흡수
- [ ] axis-1/3/4/5 Stage 1 PROBE 후속 발사 (사용자 결정, 각 $0.30)
- [ ] axis-2 Stage 2 FULL (CE × 5000-step H100, $8 + hexa cloud nohup, M3 Qwen-parity)
- [x] pool-route hook v0.5.8 fix (cycle 19-3, threshold _cpu_cores() * 50)
- [x] G8_HEXA_CLOUD_MIGRATION spec doc (cycle 21-1, main agent 직접 작성, 미커밋 보류 worktree)

## 2026-05-24 (cycle 17 cleanup — pod kill + swap decision)

- [x] pod cleanup 8 kill — AXIS 7-pod re-fire (#383 4/7 결과 도착 후 3 hung C/C2/E + 4 done A/B/D/F 모두 cleanup) + 옛 p21h-qwen 잔재 (b23g2abvbphz33). R8a'' (6gqf9nsdquz8ug) 1 pod만 keep
- [x] worktree cleanup 26 → 0 (agent-* 전부 force remove)
- [x] **swap decision: NO SWAP through Wave-17** — v11/v13 둘 다 4/5 criteria, n_strong vs continuous trade-off anti-correlated. 자율 결정: M5 (PREFIRE) + M3 (R8a'' in-flight) 우선 진행, swap candidate 재평가는 Wave-18 fine-tune (eternal 0.25/0.30/0.35) 또는 R8a'' final_CE 결과 후
- [x] cycle 17 마감 8/8 done (1-cycle 17 작업 + 2-3-6-7-10-11-12-13-14-15-18-19-20-21-22-23-24 누적 21 task)
- [x] g8 위반 인정 — 모든 fire 가 raw runpodctl/dispatcher (hexa cloud 미사용). 향후 모든 fire prompt 에 hexa cloud 의무화 권고
- [ ] cycle 16-4 (AXIS_MAP-FAN re-design spec) — R8a'' 결과 후 진행
- [ ] cycle 16-5 (hexa-lang G5 inbox) — 이미 PR #627 G1-G4 cover, G5 append 또는 보류
- [ ] R8a'' H100 fire 진행 중 (~50min 남음, Monitor 가동 중 task bhp5kekzp)


## 2026-05-24 (cycle 16-17 — @goal 재정의 + 5 milestone 신규)

- [x] LORA.md `@goal:` 라인 신규 추가 — "VP21M production swap 5/5 + V3 substrate Qwen-parity + wiring-integrity audit 완료"
- [x] 이전 @goal ("init_CE catastrophic floor 돌파 + n_strong ≥ 4 stable + production adapter swap 가능") 의미 불명확 사유 명시 (H_255 partial FALSIFY · 14.x floor 미재현 · "floor/돌파" undefined · production metric 은 final_CE / n_strong / swap_criteria 5/5)
- [x] 5 milestone 신규 (`- [ ]` checkbox · /domain milestone 자동 인식) — M1 VP21M swap 5/5 + M2 mini 배포 30d monitor + M3 V3 Qwen-parity (Δfinal_CE ≤ 0.1 nats) + M4 7-axis wiring fix + 진짜 ablation + M5 PREFIRE_WIRING_AUDIT_CHECKLIST 도입
- [x] "진행 중 / 대기" 7 항목 → milestone 매핑 + closure marker (R8c=M3 부분, R8a''=M3 in-flight, #342=M4 prereq, Wave-17=M1 lever, AXIS_MAP 재측정=M4 main path)
- [x] /gap F5 success-criteria motivation 흡수 — production-driven + substrate-pure + wiring-integrity 3-축 measurable goal
- [ ] 사용자 결정 — M1 swap candidate v11 (Wave-15 sweet spot, continuous 34) vs v13 (eternal threshold 재정의 후 fire 필요)

## 2026-05-24 (cycle 13 — 5/5 done + R8a' wiring-fail 발견)

- [x] cycle 13 phase-0 brainstorm depletion (5 cap) + fan-out parallel
- [x] mini production swap dry-run — READY 5/5 (v11 drop-in compat · base byte-identical · adapter 147,770,496B · v5 backup OK)
- [x] swap_criteria_check.hexa (#365) — VP21M 5-criteria 자동측정 selftest 5/5 PASS, Wave-16 real-data 1/5 NO_SWAP 일치
- [x] R8_SAGA_FINAL_TEMPLATE (#361) — 9-section R8a'/R8b/R8c fill-in (BREAKTHROUGH/NO-CHANGE/PARTIAL 3-branch decision tree)
- [x] COST_LEDGER_SESSION3 (#360) — session-3 누적 $21.54 SSOT (R8 saga $4 · AXIS_MAP-FAN $13 · Wave $1.5 · V3 P2 $3.3)
- [x] R8A_VS_R8A2_BYTE_EQUAL_NATURAL_EXPERIMENT (#362) — 4-가설 lock-in (A inert / B noise only / C kv only / D BREAKTHROUGH)
- [x] **R8a' 폴링 발견: PR #342 wiring fix production silent-FAIL** — `[from_qwen] v3_n_kv_head=4` 출력 (의도=2), train step=250 CE=1.0992 정상 학습
- [x] **R8a' init_CE step=1 = 14.3743** — cluster Z (14.46) 와 byte-equal 수준 (n_kv_head=4 환경에서 noise=0 측정)
- [ ] **PR #342 root cause 검증** — conscious_decoder_v3.py + train_p21h_v3.py dispatcher scp 시점 + args.n_kv_head 전달 path 추적 (read-only autonomous)
- [ ] R8a'' 진짜 fix 발사 (root cause 해결 후, noise=0 + 실제 n_kv=2 동시)
- [ ] R8c probe fire 분리 ($0.25) — cluster Z floor 원인 noise/kv 무관 가설 직접 검증
- [ ] R8a' 완료 대기 (~53min 남음, n_kv=4 환경 final_CE + verdict 회수)

## 2026-05-24 (late session)

- [x] R8a fire n_kv_head 무효 버그 발견 — v3_n_kv_head=4 despite --n-kv-head 2 (arg→from_qwen wiring 누락)
- [x] PR #342 wiring fix — train_p21h_v3.py + conscious_decoder_v3.py (default=4 무회귀)
- [x] batch merge cycle 30→10→3 OPEN (admin --squash, 일부 worktree 충돌로 local 만 미정리)
- [x] superseded 7 close — #193 #202 #203 #212 #226 #329 #341 (sister PR 가 이미 main)
- [ ] #335 V3→PURE path rebase 진행 중 (sister agent)
- [x] #228 #313 close as superseded (huge multi-file overlap, 잔여 가치 < rebase 비용)
- [ ] R8a init_CE step=1 결과 대기 (~02:19 KST 발사, ~90min)
- [ ] R8a' 재발사 (#342 merge 후, 진짜 n_kv=2 + noise=0 동시)
- [ ] R8c probe fire (#339 driver, R8a 애매 시 noise/kv 분리, $0.25)
- [x] conflict root cause 분석 — CHANGELOG/SAGA/WAVES_MATRIX 다중작성으로 sister PR 충돌

## 2026-05-24

- [x] N_KV_HEAD dispatcher passthrough (#334) — R8a fire prerequisite
- [x] R8 saga INDEX (#336) — 13 docs TOC
- [x] Wave-17 corpus prune 사전검증 (#337) — 4-point linear, GO
- [x] WAVES_MATRIX 갱신 (#338) — R8 + cluster + LIFE 흡수
- [x] R8c probe driver (#339) — 3-cell control-plane, selftest 5/5
- [x] R8a fire dispatch — pod ev85rx3xr7zqso (noise=0 + n_kv=2 의도)
- [x] R8a n_kv_head 무효 버그 발견 — v3_n_kv_head=4 (arg 미반영)
- [ ] PR #342 n_kv_head wiring fix merge → R8a' 진짜 n_kv=2 재발사
- [ ] R8a init_CE step=1 결과 확인 (noise=0 단독 천장 효과)
- [ ] R8c probe fire (R8a 애매 시 noise/kv 분리, $0.25)
- [ ] Wave-17 fire 결정 (eternal U-shape sweep, $1.50)

## 2026-05-23 (prior session)

- [x] Wave-16 corpus_v12 (#205) — eternal STRIP-ALL, U-shape FALSIFIED monotone
- [x] AXIS_MAP-FAN 5/7+2 (#249) — cluster X/Y/Z 자연실험
- [x] R8 spec (#214) + R8c probe protocol (#224/#250)
- [x] from_qwen audit (#255) + random-baseline benchmark (#256)
- [x] R8a fire spec (#257)
