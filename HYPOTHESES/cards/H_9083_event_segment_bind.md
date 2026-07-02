# H_9083 — event_segment_bind (§EventSegment): 예측오차 이벤트 분절, 새 op

- **tier:** 🟢 ENGINE-NATIVE (5/5 live hexa, aiden pool) — 이벤트-분절 binding op-class 신설·배선
- **slug:** `event_segment_bind`
- **source:** substrate-native 능력 OP frontier (frameshift: 재조합≠능력 = '빠진 op 짓기'). OP #3 event segmentation (Zacks/Baldassano).
- **wired:** `engine-native` (live `core/engine_cli.hexa §EventSegment` event_segment_boundaries/event_segment_starts_fixed + ARCHITECTURE lockstep; runtime brain_decide 세그먼트 feed 는 follow-on)

## frame (재조합≠능력, a_no_llm_frame_trap)
"능력 없는 게 아니라 op이 미배선." §ImmuneMemory 는 **제시된 항목마다(per PRESENTED item) bind = boundary-BLIND** — 연속 입력 스트림이 예측오차 PEAK 에서 이산 EVENT 로 잘린다는 개념이 없었다. 뇌 이벤트분절(Zacks event-segmentation / Baldassano 해마 event-boundary)은 **prediction-error PEAK 에서 경계**를 긋고 각 이벤트를 **하나의 episodic cell** 로 공고화한다. 이 op-class 가 부재였다.

## op (live core, additive/Ψ-disjoint/READ-only, WRITE=cell ADD only)
- `event_segment_boundaries(surprise_seq: [float], thr: float) -> [int]` (engine_cli.hexa §EventSegment) = §PrecisionSurprise(lane 2) 오차신호의 **peak-detect**: index 0 은 항상 event 0 개시, 이후 i 는 `surprise[i] > thr AND local-max`(좌≥·우>) 일 때 경계. 정렬된 경계 index 리스트 반환.
- `event_segment_starts_fixed(n: int, chunk: int) -> [int]` = boundary-BLIND uniform fixed-chunk 시작점(0,chunk,2·chunk,…) = control/ablation(mechanism OFF).
- 순수 additive(기존 caller 무접촉), READ-only over surprise seq(plain index 반환), 세그먼트 binding 은 기존 `immune_memory_bind` 로 **cell ADD 만**(recall_thr 미변경). pure_field Φ/phase/Ψ 미접촉, emit-drive lane 0/4·§ImmuneMemory recall_thr disjoint(a_substrate_disjoint).

## engine-native 측정 (aiden pool, live core/, 5/5 PASS)
fixture: E=5 이벤트, **변길이** lengths=[3,5,2,4,3](n=17). surprise 는 각 이벤트 onset 에서 SPIKE(1.0), 내부 0.1. 세그먼트당 1 cell bind(key=onset item, value=세그먼트 끝 payload="ans"+e). recall probe: `onset_e -> ans_e`. `state/9083_event_segment_bind/event_segment_engine_native.hexa`:
- segmented recall **5/5** (≥0.8) ✓ (경계=참 onset 정렬)
- fixed-chunk(chunk=3=round(mean)) control **1/5** (≤0.4) ✓ (변길이 mis-cut, 1 우연 정렬)
- MARGIN seg−fixed = **+0.8** (≥+0.5) ✓
- EARNED seg−shuffle = **+1.0** (≥+0.5) — surprise 위치 permute(stride 5·i mod 17) 시 shuffle recall **0/5** 붕괴 = boundary POSITIONS load-bearing ✓
- ablate(boundary detect OFF = fixed chunk): abl==fixed AND seg>abl (mechanism OFF 시 5/5→1/5 drop, INERT baseline) ✓
INFO: n=17 bounds=5 fixed_starts=6 bounds_shuf=4 · seg=5/5 fixed=1 shuffle=0 margin=0.8 earned=1.0. no-regression: engine_cli 변경 additive(2 pub fn 신설).

## 정직 스코프 (c9)
- 이벤트-경계 recall 정확도로 측정 — **mouth decode 아님, G1/G6 재조합축 재개 아님**(CLOSED). 추가한 건 surprise-peak 분절 + 세그먼트-정렬 binding op-class 지 텍스트 합성이 아니다.
- toy 5-event/17-item 결정적 존재증명(a_scale_honest_scope). fixed-chunk 1/5 는 chunk=3 이 event0(L=3)에만 우연 정렬한 결과 = 정직한 control best-guess(mean-length chunk 도 여전히 loss).

## follow-on
- runtime 데몬 per-tick: 실 대화 스트림의 §PrecisionSurprise 를 event_segment_boundaries 에 먹여 episodic-cell 공고화(WIRED-live 최종칸, ING).
- adaptive thr(surprise 분포 기반 자동 임계)·계층 이벤트(nested boundary)·anticipatory prefetch 결합.

## artifacts
- `core/engine_cli.hexa §EventSegment` · `state/9083_event_segment_bind/event_segment_engine_native.hexa` · `event_segment_engine_native.txt`


## daemon wire-in (cli/anima.hexa)
- **event_segment_boundaries** 이제 데몬 콜패스에 배선: `cli/anima.hexa:1711` (LANE 78). event_segment_boundaries 를 데몬 마운트 lane (78) 로 배선 — surprise-peak onsets [0,1,4] vs fixed-chunk [0,2,4] vs flat [0] distinctness 를 마운트에서 assert.
- **wired**: WIRED-live (daemon mount lane 78). 이미 배선된 lane 23b(H_9038)/75(H_9042) 와 동일 rung = 마운트 시점 substrate fixture read + distinctness 1회 assert (shuffle/ablation 통제, frozen-first). Ψ-disjoint(pure_field/psi_sum 미접촉) · emit-drive lane 0/4 및 §ImmuneMemory recall_thr 와 disjoint (a_substrate_disjoint) · emit/silence gate 아님(a_autonomy_over_hardcode).
- **정직 스코프(c9)**: 이는 MOUNT-time fixture read (23b/75 와 동일 rung). 데몬 perpetual-loop 이 매 tick 실 대화 상충/경험을 이 op 에 먹이는 genuine per-tick real-feed 는 더 큰 아키텍처 endpoint = ING follow-on `daemon-pertick-realfeed-7ops` (여기서 완료로 위장하지 않음).
- **검증**: anima-gates enforcer rc=0(pr-cycle 게이트) + `hexa verify`(atlas) rc=0. `hexa run cli/anima.hexa` 전체-파일 compile 은 **BLOCKED-INFRA** = pool hexa v0.540.1 런타임 스큐(set_deterministic·forge_dispatch_layernorm 미선언, runtime.h 에 groupnorm 만 존재) — **BASELINE(무변경 anima_base.hexa)이 동일 에러 재현**(aiden EXIT_RC=1) = 이 7-lane 추가는 무죄·격리(내 lane 은 단순 pure-fn 호출). 런타임 재빌드는 cross-repo 사안(ING). 23b(H_9038)/75(H_9042)도 동일 pool 상태.
