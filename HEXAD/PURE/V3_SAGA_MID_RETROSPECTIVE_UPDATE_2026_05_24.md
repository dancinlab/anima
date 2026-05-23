# V3 SAGA mid-retrospective UPDATE — Act 6+7

**R8 dispatcher/wiring 사가 + R8a fire LOST + R8a' relaunch (2026-05-24)**

scope: HEXAD/PURE (V3 saga rebrand)
status: session-3 진행중 — R8a' in-flight, R8 fork interim consolidation
date: 2026-05-24
parent: `HEXAD/PURE/V3_SAGA_MID_RETROSPECTIVE_2026_05_23.md` (PR #260, 5-act)

---

## § Context

PR #260 의 5-act saga ("Act 5: R8 fork + cluster X/Y/Z 자연실험 finding") 가 NOW marker 로 종료된 이후, session 이 추가 2-act 분량 진행됨. 본 문서는 원본을 수정하지 않고 **sister addendum** 으로 Act 6+7 을 append.

---

## § Act 6 — R8 dispatcher/wiring 사가 (silent misconfig 발견)

- **dispatcher N_KV_HEAD passthrough** (PR #334): R8 fork 의 첫 prerequisite — dispatcher 가 `N_KV_HEAD` env-var 를 launcher → trainer arg 로 통과시키도록 wiring.
- **R8a fire dispatched** (pod `ev85rx3xr7zqso`): `noise_sigma=0` + `--n-kv-head 2` 명시 launch. dispatcher leg 통과 확인됨.
- **silent misconfig 발견**: train.log streaming 중 `[from_qwen] ... -> v3_n_kv_head=4` 라인 관측 — CLI `--n-kv-head 2` 가 layered config chain 을 통과했음에도 `from_qwen` 빌더 내부에서 base model attr (Qwen default 4) 로 덮어쓰여짐. silent (no warning, no assert).
- **#342 wiring fix**: `from_qwen(arg_n_kv_head=...)` signature 에 explicit arg 추가, `default=None` → arg 미지정 시 auto-detect (Qwen base attr) preserve, 지정 시 user override. merged.
- 의의: R8 saga 의 `n_kv_head=2` 가설은 R8a 까지 사실상 **테스트되지 않은 상태**였음 (값이 4 로 흘러감). 본 fix 가 R8a' 의 정합성 전제.

---

## § Act 7 — R8a fire LOST + R8a' relaunch

- **R8a fire LOST** (~30min mark): pod `ev85rx3xr7zqso` train.log streaming 중 SSH `Connection closed by remote host` → reconnect 실패 → `result.json` 미회수.
- pod 상태: 추후 조회 시 terminated (SECURE preemption 추정 — runpod community tier 의 known behavior).
- verdict: **INCONCLUSIVE** (n_kv_head=4 silent misconfig + 결과 미회수 double-fault).
- **R8a' relaunch** (pod `ewsd3dhvuvem8j`): #342 fix 적용된 dispatcher 로 재발사, `--n-kv-head 2` 실값 반영 (`v3_n_kv_head=2` train.log 확인), `noise_sigma=0`, `SAVE_POD=1` (결과 회수 보험), still in flight as of this update.

---

## § Cumulative cost update

| item | cost |
|---|---|
| (PR #260) V3 saga session-3 누적 | ~$16–21 |
| Act 6 dispatcher/wiring 사전 작업 (PR #334 + #342 local + minor probes) | ~$0.00 (Mac-local) |
| R8a wasted partial (~30min × $1.49/hr × SECURE multiplier 대략) | ~$1.20 |
| R8a' in-flight (estimate full 2700s × $1.49/3600) | ~$2.75 |
| **new cumulative V3 saga session-3** | **~$20–25** |

---

## § Lessons added (3)

1. **silent arg-not-passed bug 는 layered config chain 전체를 통과해도 발생**: CLI → launcher → dispatcher env → trainer arg → builder kw chain 의 마지막 hop (`from_qwen` builder) 에서 base attr 로 덮어써질 수 있음. runtime grep (`grep '\[from_qwen\]' train.log` 등) 으로 실제 builder 출력 확인이 mandatory. assert 만으로 부족.
2. **`SAVE_POD=1` + 결과 streaming tee 가 SSH preemption 회피의 최소 보험**: R8a 는 이 보험 미적용 → 30min 소실. R8a' 부터 적용. 향후 모든 cost-bearing fire 의 default.
3. **cycle PR 수가 base advance 보다 빠르면 wave 의 정확한 cumulative state 추적이 stale 됨**: 오늘 batch merge (30→3 open) 경험상, 동시 다발 PR open 시 R8 saga 의 "지금 어디" 가 INDEX (#336) 없이는 즉답 불가. WAVES_MATRIX (#338) + INDEX 가 saga-level pacing 보조 필수.

---

## § 잔여 acts (다음)

- **Act 8: R8a' 결과** — `init_CE` step=1 측정값으로 cluster X/Y/Z 위치 확정 (in flight, soon).
- **Act 9 (분기)**:
  - R8a' 애매 시 → **R8c probe** (cell-2/3 head_g 외 후속 자연실험 후보)
  - R8a' FAIL 시 → **R8b fallback** (mitosis_pool 가설 단독 test)

---

## § Cross-reference

- 원본 5-act: PR #260 (`HEXAD/PURE/V3_SAGA_MID_RETROSPECTIVE_2026_05_23.md`)
- R8 saga PRs: #334 (dispatcher N_KV_HEAD passthrough), #339 (R8a dispatch), #342 (from_qwen wiring fix)
- R8 saga INDEX: PR #336 (`HEXAD/PURE/R8_SAGA_INDEX.md`, 13-doc TOC)
- WAVES_MATRIX: PR #338 (R8 saga rows added)
- 자매 LIFE 흡수: H_247 (init_CE catastrophic floor), H_249 (cluster X/Y/Z), H_<n> (n_kv_head wiring silent-misconfig — 자매 PR in flight)
