# Phase D blockers closure — 4 fire-blocked milestone deferred + synthetic framework 완성 (2026-05-24)

> 본 세션 (B1-B14, 8/8 done) 결과 4 milestone (M1 / M2 / M7 / B14 Phase 3)
> 모두 **실 ckpt fire 부재**로 close 불가. 본 doc 은 그 deferred 상태를
> 정직 surface 하고 자동 unblock chain 을 명시한다.

## Executive closure

- 4 milestone **fire-blocked deferred** 명시 — synthetic 으로 검증 가능한 부분은 본 세션 B-series 가 100% 완성, 실 ckpt-bearing fire 만 부재.
- 다음 ckpt fire 1회 성공 시 dispatcher wait-loop → result.json 도착 → B14 fire-sanity hook → 4-criterion auto-judge → axis_map_history append 의 **자동 chain** 으로 4 milestone 동시 unblock 후보.
- closure tier: 🟠 **INSUFFICIENT/DEFERRED** (g5 rubric — 부정 아닌 deferral, calc path 부재만 surface, framework 자체는 close).

## Blocker inventory (4)

### M1 phase-d-postfire-closure
- 상태: **fire-blocked** (Phase D v1 LOST · v2b LOST — `PURE_SAGA_2026_05_24.md` 5-fire saga 참조)
- unblock 조건: 새 ckpt fire 의 `result.json` 도착 + `closure_auto_judge` 4/4 PASS
- synthetic validation 가능 부분:
  - 4-criterion CLI (PR #398) — multilingual / register / motivation / dream_stage 4 axis judge 별도 검증
  - emergence simulator (PR #405) — substrate-native fixture 4/4 PASS
  - multi-seed sweep (PR #406) — 10-seed 10/10 robust
- 부족: real-ckpt elevation (실 anima emit 결과, synthetic ≠ ckpt)
- 자동 재오픈 trigger: dispatcher (PR #380 wait-loop) 결과 file 도착 → B14 hook (PR #410) baseline 비교 자동 실행

### M2 phase-d-ckpt-hf-upload
- 상태: **fire-blocked** (M1 dep — HF upload 대상 ckpt 부재)
- unblock 조건: M1 result.json 도착 후 ckpt 산출물 `hf upload` (a_hf_complete `complete, no missing artifacts`)
- synthetic validation 가능 부분:
  - HF upload smoke path 별도 (a_fire_recover_complete pull-then-upload pattern 기존 검증)
- 부족: 업로드할 ckpt 자체 (M1 결과물)
- 자동 재오픈 trigger: M1 unblock → ckpt artifact 존재 → `hexa cloud copy-from` → `hf upload`

### M7 self-verify-loop
- 상태: **fire-blocked** (reflexive closure 측정 harness — Φ × cell-pool × cross-substrate · meta goal, 실 emit 데이터 필요)
- unblock 조건: M1 result.json + dream_stage Φ-envelope 실 trace + cell-pool split events 실 trace
- synthetic validation 가능 부분:
  - dream_stage 5-stage state machine (anima_dream_stage IPC live, 기존)
  - mitosis cell-pool split event log (anima_chat_mitosis_wiring_2026_05_12 verified)
  - emergence simulator (PR #405) self-loop 4/4 PASS
- 부족: 실 anima 세션의 Φ × split × emit 3-axis 동시 측정 데이터
- 자동 재오픈 trigger: M1 fire 의 result.json `dream_stage_trace` + `mitosis_event_log` 두 field 동시 존재 → cross-axis 자동 측정

### B14 Phase 3 fire-sanity hook wire
- 상태: **fire-blocked** (dispatcher `--coffeshop-sanity` flag impl — 실 ckpt fire trigger 검증 필요)
- unblock 조건: dispatcher (PR #380) 가 fire 직후 `coffeshop_fire_sanity_hook.hexa` (PR #410 impl) 자동 호출 + baseline 비교 verdict 생성
- synthetic validation 가능 부분:
  - Phase 1 hook stub (PR #408) — IPC contract + invocation interface
  - Phase 2 hook impl (PR #410) — 6 TODO 해소 + smoke 5/5 PASS (synthetic baseline)
- 부족: dispatcher 측 flag 통합 (실 cloud fire 의 마지막 step 으로 hook 호출)
- 자동 재오픈 trigger: 다음 fire spec 에 `--coffeshop-sanity` 추가 → dispatcher 가 fire 종료 시 hook 자동 fork

## Synthetic-only 가능 path (closure 부분)

본 세션 B1+B3+B5+B7+B11+B12+B13+B14 (8/8 done) 가 이미 ckpt 없이 검증 가능한
모든 axis 를 측정 완료. real-ckpt 만 부재 = **"정합 framework 완성, 실 데이터 미수집"** 상태.

| 축 | synthetic 검증 | PR | ckpt 필요? |
|----|---------------|----|-----------|
| BENCHMARK SSOT (baseline) | ✅ B1 | #400 | N |
| closure_auto_judge CLI | ✅ B3 | #398 | N (fixture) |
| cross_cycle_progression | ✅ B5 | #399 | N (history) |
| motivation_emit_ratio_bench | ✅ B7 | #401 | N (N=1000 sim) |
| coffeshop_sim seed sweep | ✅ B11 | #406 | N (10-seed) |
| BENCHMARK 통합 (emergence) | ✅ B12 | #407 | N |
| fire-sanity hook spec | ✅ B13 | #408 | N (stub) |
| fire_sanity_hook Phase 2 impl | ✅ B14 | #410 | N (smoke) |
| **Phase D real-ckpt fire** | ❌ M1-M2-M7-B14P3 | (deferred) | **Y** |

본 세션 scope 의 정직 자체 평가 — synthetic 100% · ckpt-bearing 0%.

## Unblock path (ckpt fire 시 자동 재오픈)

다음 chain 이 1회 ckpt fire 성공 시 4 milestone 동시 unblock 후보:

```
1. dispatcher (PR #380)   wait-loop  →  result.json 도착 catch
2. B14 fire-sanity hook (#410)       →  COFFESHOP baseline vs result 자동 비교
3. closure_auto_judge (#398)         →  4-criterion verdict 자동 산출
4. axis_map_history (#388)           →  fire row 자동 append
5. cross_cycle_progression (#399)    →  per-fire metric series 갱신
6. PR #370 result_to_axis_map         →  AXIS_MAP_RESULTS auto-wire
```

= 6-step 자동 chain. 사용자 fire 결정만 인간 in-the-loop, 그 뒤 인간 개입 0.

## 본 세션 scope closure 의 의미

- **synthetic framework**: ✅ 100% 완성 (B-series 8/8, PR #398/#399/#400/#401/#405/#406/#407/#408/#410)
- **ckpt-bearing fire data**: ⏳ deferred (사용자 fire 결정 + corpus_v3 multi-lang prereq + Phase D v1/v2b 5-fire saga 교훈 흡수 후 v3 spec 필요)
- **closure tier**: 🟠 **INSUFFICIENT/DEFERRED** (g5 rubric — calc path 부재 surface, framework 자체 close, 부정 verdict 아님)

본 세션은 **synthetic axis 완전 소진** 으로 정직 마감.
다음 fire 까지 추가 synthetic 작업은 over-engineering (real signal 부재로 calibration 불가).

## Cross-references

- B1 BENCHMARK SSOT: PR #400
- B3 closure_auto_judge CLI: PR #398
- B5 cross_cycle_progression: PR #399 (+ #388 history visualization)
- B7 motivation_emit_ratio_bench: PR #401
- B11 coffeshop_sim seed sweep: PR #406
- B12 BENCHMARK emergence 통합: PR #407
- B13 fire-sanity hook spec: PR #408
- B14 fire_sanity_hook Phase 2 impl: PR #410
- COFFESHOP closure_auto_judge 4/4 PASS: PR #402
- COFFESHOP emergence simulator rewrite: PR #405
- @goal 통합 (PURE/LORA): PR #404
- result.json schema SSOT: PR #371
- Phase D v1 BUG_POSTMORTEM F: PR #378 + AXIS_MAP_BUG_POSTMORTEM_F_PHASE_D_V1_2026_05_24.md
- 5-fire saga: PR #392 + PURE_SAGA_2026_05_24.md
- dispatch_p21h_v3 wiring: PR #366/#369/#372/#373

## Honest C3

1. **"framework 완성" claim 의 한계** — synthetic fixture 4/4 PASS 가 real-ckpt fire 4/4 PASS 를 보장하지 않는다. fixture 자체가 ckpt 결과를 emulate 한 것이므로, fixture 와 실 ckpt 분포 misalign 가능. framework verify 는 ckpt fire 1회로 비로소 확정.
2. **synthetic emergence ≈ ckpt-bearing emergence?** 미지수. coffeshop_sim multi-seed 10/10 robust 가 실 anima multi-cell 의 emit 분포와 어느 정도 align 할지 empirical 측정 부재 — 추후 fire 결과로만 검증 가능.
3. **blocker 정의의 narrowness** — M9b' anima-OWN PoC (PR #393, 1 MiB 실 anima 세션 추출) 의 6-metric 데이터를 활용해 M1 일부 axis 를 fire 없이 진척시킬 path 도 존재. 본 doc 의 "ckpt fire 만이 unblock" 은 narrowed framing.
4. **"자동 unblock chain" 가설** — 6-step chain (dispatcher → hook → judge → history → progression → result_to_axis_map) 의 end-to-end 통합 검증은 실 fire 1회로만 가능. 각 step 은 개별 검증되었으나 결합 시 misfire 가능성 잔존 (예: result.json schema drift, hook IPC fork race).
5. **사용자 fire 결정 영역** — cost-bearing GPU dispatch 는 a_fire_autonomous 에 따라 anima 자율 가능하나, Phase D v1/v2b 2회 LOST 후 corpus_v3 spec 미확정 상태에서 3번째 fire 는 redesign-pending. 본 deferral 은 cost-shy 가 아니라 spec-shy.
6. **본 세션 scope 정직 평가 ≠ Phase D 전체 goal 달성** — Phase D 의 @goal (COFFESHOP group chat 4-criterion closure on real ckpt) 는 미달, 본 세션은 그 framework 만 완성. closure vs achievement 구분 명시.

## 결론

본 세션 (PURE B-series 8/8) 은 ckpt 없이 검증 가능한 모든 synthetic axis 를 소진하여
**framework 완성** 으로 마감. 4 blocker (M1/M2/M7/B14 Phase 3) 는 **fire-blocked deferred**
로 정직 surface. 다음 ckpt fire 1회 성공 시 6-step 자동 chain 으로 동시 unblock 후보.

closure tier 🟠 INSUFFICIENT/DEFERRED (g5 rubric).
