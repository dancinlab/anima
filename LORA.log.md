# LORA — task log (append-only)

> `LORA.md` 의 변경/작업 체크리스트. 최신이 위.

## 2026-05-24 (cycle 15 — Wave-17 5-point U-shape verdict + AXIS_MAP-FAN re-fire)

- [x] **Wave-17 4-pod parallel fire COMPLETE** — eternal_keep {0.10/0.20/0.40/0.50} 4 × H100 80GB HBM3 / H100 NVL, total wall ~723s, est $1.50
- [x] result.json 4 변종 회수 (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M_v{13,14,15,16}/result.json`)
- [x] WAVE17_VERDICT_2026_05_24.md (8-section, ~120 LoC) — U-shape 확정 + swap candidate trade-off 분석
- [x] LORA.md production swap 상태 갱신 (NO SWAP through Wave-17, v11/v13 4/5 tie 사용자 게이트)
- [x] LORA.md VP21M wave saga Wave-17 entry 추가 (4-pod sweep 상세)
- [x] **새 발견**: criterion 2 (n_strong) ↔ criterion 4 (continuous) anti-correlated — 단일 변종 5/5 PASS 불가 (sweep 0.10~0.50 empirical)
- [x] **새 발견**: U-shape 비대칭 — 좌측 floor (0.20=98) 가 우측 (0.50=52) 보다 더 깊음
- [x] **새 발견**: v13 (eternal=0.10) n_strong=5 만점 — 4 corpus 사가 첫 5/5 cross-lingual STRONG
- [ ] AXIS_MAP-FAN re-fire (option, $0.50-1.00) — H_255 H255.2 검증, R8 saga continues parallel
- [ ] swap criteria 재정의 검토 — criterion 2 ↔ 4 anti-correlation 인정 또는 dual-adapter hot-swap
- [ ] Wave-18 권고: eternal {0.25/0.30/0.35} 3-point fine-tune ($1.10, sharpness 측정)
- [ ] v13/v14/v15/v16 HF upload 완성 검증 (a_hf_complete 후속, 10-file manifest)

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
