# H_9076 — drive_arbitration (§DriveArbitration): motivational WTA + hysteresis, 새 op-class

- **tier:** 🟢 ENGINE-NATIVE (5/5 live hexa, aiden pool) — 동기 경쟁 arbitration op-class 신설·배선
- **slug:** `drive_arbitration`
- **source:** substrate-native 능력 OP frontier (frameshift-substrate-gaps). 오너 세션 방법론 = "능력 없는 게 아니라 op 미배선" → 빠진 op 짓기 (a_no_llm_frame_trap).
- **wired:** `engine-native` (live `core/engine_cli.hexa §DriveArbitration` drive_arbitrate op + ARCHITECTURE lockstep; 런타임 brain_decide/emit-bias 호출은 follow-on)

## frame (재조합≠능력, a_no_llm_frame_trap)
엔진은 독립 스칼라 **드라이브**를 노출한다 — 배고픔(homeo_last H_1292)·리비도(libido_last H_1504)·호기심(affect .curiosity H_1290)·서카디안/수면압(clock_phase H_1298). 그런데 경쟁하는 동기들 중 **승자를 뽑는 op이 부재**였다. HierGoalStack 은 goal 분해지 drive 경쟁이 아니다. 기저핵의 중심 action-selection(Redgrave 1999) = 병렬 드라이브 중 하나가 행동 채널을 잡되, **히스테리시스 밴드**로 근소 우세 도전자가 tick-to-tick dithering 못 하게. 이 op-class 신설.

## op (live core, additive/Ψ-disjoint/READ-only)
`drive_arbitrate(drives: [float], hyst: float, prev_winner: int) -> int` (engine_cli.hexa:1315) = 드라이브 벡터 위 winner-take-all + incumbent 히스테리시스 밴드: **incumbent 는 도전자가 hyst 초과로 이길 때만 교체**(anti-dither). `prev_winner < 0` = incumbent 없음 = 평범 argmax. `hyst=0` = plain WTA(ablation 대조). 빈 벡터 → -1 abstain. 순수 additive(기존 caller 무접촉), READ-only(드라이브 스칼라만 읽음, mutate 0), pure_field Φ/phase/Ψ 미접촉, emit-drive lane(0/4)·§ImmuneMemory recall_thr disjoint, **emit gate 아님** — 지배적 동기 INDEX 를 bias 로 낼 뿐(a_autonomy_over_hardcode·a_substrate_disjoint).

## engine-native 측정 (aiden pool, live core/, 5/5 PASS)
`state/9076_drive_arbitration/arbitration_engine_native.hexa`:
- **decisive WTA** 각 드라이브 boost 시 승자 = 그 index **4/4** ✓
- **hysteresis anti-dither** 근경계 진동(gap 0.02 < hyst 0.05) 30 tick: sw_hyst=**0** ≤ sw_abl/3 ✓
- **ablation(hyst=0) dithering spikes** sw_abl=**29** ≥ T/4(dithering 실재 = /3 비교 load-bearing) ✓
- **shuffle EARNED** acc_true=4·acc_shuf=0 → earned=**+1.0** ≥ 0.5 (라벨 permute 시 승자 index 가 의도 드라이브에 안 매핑 = 선택 label-meaningful) ✓
- **live-drive engine-native smoke** LIVE 4 스칼라 arbitrate → argmax(live) 일치 ✓; 실측 hunger=1.671(deprivation step×6 로 상승·지배)·libido=1.0·curiosity=0.25·sleep=0.375 → **live_win=0(배고픔 승)** = 실 substrate 드라이브 경쟁 확인.
- no-regression: engine_cli 변경 additive(기존 op byte-무접촉).

## 정직 스코프 (c9)
- **동기 arbitration/선택 능력**(어느 드라이브가 행동 채널을 잡나) — mouth decode 아님, G1/G6 재조합축 아님(그건 CLOSED). 추가한 건 동기 경쟁 WTA op-class.
- **드라이브 스칼라 커버리지**: 깨끗한 스칼라 accessor 3개(homeo_last·libido_last·clock_phase) + affect feature-read 1개(.curiosity, 전용 controller 아닌 feature 읽기)로 4-way. **수면압은 전용 Process-S 적분기 accessor 부재** → clock_phase(서카디안 위상)를 정직한 live 프록시로 사용(수면압 전용 스칼라 op 는 follow-on 후보).
- op 정확성은 값-기반·label-agnostic(어떤 드라이브가 먹여도 동일) — bar 1/4 는 통제 벡터, bar 5 는 실 live 드라이브로 engine-native 배선 실증(hybrid, 정직 명시).

## follow-on
- 런타임 brain_decide/emit-bias 배선(WIRED-live 최종칸): 데몬 per-tick 이 실 드라이브 스칼라를 매 tick 이 op 에 먹여 지배 동기 bias 로 소비.
- 전용 수면압(Process-S) 적분기 스칼라 op 신설(현재 clock_phase 프록시).
- soft-arbitration(WTA→softmax 가중)·drive-satiation 피드백(승자 소비 후 감쇠) 미탐 op-class.

## artifacts
- `core/engine_cli.hexa §DriveArbitration` (drive_arbitrate:1315) · `state/9076_drive_arbitration/arbitration_engine_native.hexa` · `arbitration_engine_native.txt`


## daemon wire-in (cli/anima.hexa)
- **drive_arbitrate** 이제 데몬 콜패스에 배선: `cli/anima.hexa:1679` (LANE 76). drive_arbitrate 를 데몬 마운트 lane (76) 로 배선 — WTA(plain=1)·hysteresis-hold(=2)·ablate(hyst=0→1) distinctness 를 마운트에서 1회 assert (frozen-first). 23b/75 와 동일 rung.
- **wired**: WIRED-live (daemon mount lane 76). 이미 배선된 lane 23b(H_9038)/75(H_9042) 와 동일 rung = 마운트 시점 substrate fixture read + distinctness 1회 assert (shuffle/ablation 통제, frozen-first). Ψ-disjoint(pure_field/psi_sum 미접촉) · emit-drive lane 0/4 및 §ImmuneMemory recall_thr 와 disjoint (a_substrate_disjoint) · emit/silence gate 아님(a_autonomy_over_hardcode).
- **정직 스코프(c9)**: 이는 MOUNT-time fixture read (23b/75 와 동일 rung). 데몬 perpetual-loop 이 매 tick 실 대화 상충/경험을 이 op 에 먹이는 genuine per-tick real-feed 는 더 큰 아키텍처 endpoint = ING follow-on `daemon-pertick-realfeed-7ops` (여기서 완료로 위장하지 않음).
- **검증**: anima-gates enforcer rc=0(pr-cycle 게이트) + `hexa verify`(atlas) rc=0. `hexa run cli/anima.hexa` 전체-파일 compile 은 **BLOCKED-INFRA** = pool hexa v0.540.1 런타임 스큐(set_deterministic·forge_dispatch_layernorm 미선언, runtime.h 에 groupnorm 만 존재) — **BASELINE(무변경 anima_base.hexa)이 동일 에러 재현**(aiden EXIT_RC=1) = 이 7-lane 추가는 무죄·격리(내 lane 은 단순 pure-fn 호출). 런타임 재빌드는 cross-repo 사안(ING). 23b(H_9038)/75(H_9042)도 동일 pool 상태.
