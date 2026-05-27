# PARTICIPANT_SPIKE_INTEGRATION — anima_participant ⇄ apply_spike_features wiring (current-state)

> **status**: design-only · `$0` · 본 cycle 구현 미수반 · [[apply_spike_features]] (PR #143) + [[akida_consumer]] (PR #138) + [[telemetry_harness]] (PR #139) landed 위에서 wiring 경로 4-안 평가 + 권장 path 1 + Phase-carry path 1 명세
> **anchors**: [[AKIDA_FIRST]] (Phase 1/2 경계, HW-mandatory) · [[SPIKE_FACTOR_MAP]] (`HEXAD/CHAT/spontaneous_lib.hexa § 10` SSOT, 별도 .md 미존재) · [[apply_spike_features]] (PR #143 squash `3bce310a1`) · [[akida_consumer]] · [[telemetry_harness]] · [[feedback-plist-forbidden-akida-endpoint]] (broker endpoint = `/ws/akida_ingest`, daemon = nohup) · [[feedback-hexa-only-authoring]] (`.py` 신규 편집 금지) · project.tape `@D a_substrate_native_speak`

---

## §1 — Goal + non-goals

**Goal.** 본 cycle 종료 시 `anima_participant` 의 8-factor `decision["factors"]` 가 [[apply_spike_features]] 의 spike-modulated 결과를 반영할 wiring 경로를 closure-level 로 결정 + 다음 cycle 의 implementation 게이트 명세. wiring 자체는 본 PR 범위 밖 (design-only).

**Non-goals.** (a) `anima_participant.py` (`.py`-guard 보호) 직접 편집, (b) participant 전체 re-architecture, (c) user-message-driven fire (substrate-native speak 위배), (d) AKIDA HW 부재 시 SW fallback (Phase 2 carry), (e) broker.py 편집 (broker 도 `.py`-guard 보호).

---

## §2 — Constraint surface

```
+------------------------------+--------------------------------------------+
| boundary                     | implication                                |
+------------------------------+--------------------------------------------+
| `.py` 신규 편집 금지         | participant.py + broker.py 둘 다 frozen.   |
| (hexa-only authoring)        | 신규 wiring = `.hexa` 측에서만 가능.       |
+------------------------------+--------------------------------------------+
| AKIDA HW first ([[AKIDA_FIRST]]) | spike features 없으면 (consumer offline)|
|                              | participant 는 substrate-only factor 로     |
|                              | graceful degrade — wiring 은 optional.     |
+------------------------------+--------------------------------------------+
| `@D a_substrate_native_speak`| spike features = environment input,        |
|                              | NEVER direct fire trigger. emission 결정은 |
|                              | participant 의 motivation gate 단독.       |
+------------------------------+--------------------------------------------+
| backward-compat              | akida_consumer offline → participant 가     |
|                              | 동일하게 작동 (no crash, no regression).   |
+------------------------------+--------------------------------------------+
| broker endpoint              | ingest = `/ws/akida_ingest`, subscribe =    |
|                              | `/ws/akida` (handler discards). new route   |
|                              | 추가는 broker.py 편집 = 금지.              |
+------------------------------+--------------------------------------------+
```

---

## §3 — Approach matrix (4 후보, 평가 + 권장)

```
+----+----------------------------+----------+----------+-------------------+-----------+
| ID | mechanism                  | .py edit | latency  | failure mode      | rec.      |
+----+----------------------------+----------+----------+-------------------+-----------+
| A  | participant.hexa 가 thin    | NO (실제 | tick     | torch/transformers| REJECTED  |
|    | exec() 폐기 + hexa-native   | 폐기는    | (~2s)    | / peft full hexa  | (cycle 2/A |
|    | re-impl, tick 안에서        | py 잔존) |          | 포팅 부담 거대.   | analysis  |
|    | apply_spike_features 직접   |          |          | substrate plugin  | verbatim) |
|    | 호출                       |          |          | 측 LoRA forward = |           |
|    |                            |          |          | torch hard-dep.   |           |
+----+----------------------------+----------+----------+-------------------+-----------+
| B  | sidecar overlay daemon       | YES      | tick     | broker 측 route 없| REJECTED  |
|    | (`participant_spike_overlay |  (broker | (~2s)    | 음 + participant 도| (recurses |
|    | .hexa`) 가 features tail +   | + part.) |          | 구독 없음 →       | into .py  |
|    | apply_spike_features 계산   |          |          | 양쪽 .py 편집 필요.| edit)     |
|    | + broker `/ws/factor_overlay`|          |          | broker route 추가 |           |
|    | 신규 route 로 broadcast,    |          |          | + participant     |           |
|    | participant.py 가 구독.     |          |          | ingest task 추가. |           |
+----+----------------------------+----------+----------+-------------------+-----------+
| C  | broker 측 overlay — broker 가| YES      | tick     | broker.py 도       | REJECTED  |
|    | akida ingest 시 modulated    | (broker) | (~2s)    | .py-guarded. 그리고| (recurses |
|    | factors 계산해 `/health` 에 |          |          | participant 도    | into .py  |
|    | 노출, participant 가 polling.|          |          | polling code 추가  | edit)     |
|    |                            |          |          | 필요 = .py edit.  |           |
+----+----------------------------+----------+----------+-------------------+-----------+
| D  | telemetry_harness 가 evidence| NO       | ≤ tick   | observability only| **REC.**  |
|    | row 작성 시 apply_spike_     |          | (~2s)    | — live `decision` |  (본 cycle |
|    | features 호출, 결과를       |          |          | factor 영향 0.    |  채택)    |
|    | `modulated_factors` 필드로   |          |          | 다음 cycle 의     |           |
|    | JSONL 에 동봉. live emission |          |          | guard 완화 시     |           |
|    | 영향 0 — 관측 채널 단독.    |          |          | promote.          |           |
+----+----------------------------+----------+----------+-------------------+-----------+
| E  | factor-overlay file watch —  | YES      | tick     | participant.py 가  | REJECTED  |
|    | hexa daemon 이 features →   | (part.,  | (~2s)    | env-var 만 startup| (premise  |
|    | modulated factors JSON 한    | premise  |          | 시 1회 읽음 (line | false —   |
|    | 줄을 `${ANIMA_FACTOR_OVERLAY|  false)  |          | 44-64) — tick-time| §3.5)     |
|    | }` 에 atomic-write. premise =|          |          | file polling 0,   |           |
|    | participant 가 tick-time 에 |          |          | 신규 read 추가 =  |           |
|    | env-pointed file 을 이미     |          |          | .py edit. user spec|           |
|    | 폴링한다.                  |          |          | "check the source!"|           |
|    |                            |          |          | 직접 확인 결과    |           |
|    |                            |          |          | premise 무효.     |           |
+----+----------------------------+----------+----------+-------------------+-----------+
```

### §3.5 — Premise probe (approach E)

`anima_participant.py` 의 모든 `os.environ.get` 호출은 **module-import 시 1회** (line 44 `BASE_MODEL`, line 51-58 adapter 경로, line 60-64 broker/tick/threshold/max_new/device) 만 발생. `tick()` (line 242-290) 안에는 어떤 file/env read 도 없음. 따라서 "기존 env-pointed file polling 이 이미 있으니 한 줄만 추가하면 된다" 는 approach E 의 가설이 **무효** — 신규 file-read 자체가 `.py` 편집을 요구. approach E 의 "CLI 만 만들고 wiring 은 PENDING" 변형은 본질적으로 approach D 의 약화판이라 별도 path 가치 부재.

---

## §4 — 권장 path D + carry-forward path B

### §4.1 — Path D (본 cycle 채택, observability-only)

`telemetry_harness.hexa` 의 `build_row(msg, akida, win_ms)` (line 202-215) 를 확장:

```hexa
// 변경 sketch (다음 cycle 의 small follow-up PR — 본 design doc 범위 밖):
//   tail-read ANIMA_AKIDA_FEATURES 의 latest row → features dict
//   features 가 valid 이면 apply_spike_features(factors, features) → modulated
//   row 에 "modulated_factors" 필드 추가 + features 추적용 "spike_features_ref"
//
// 변경 LoC ≈ 10 (features tail-read helper + apply 호출 + dict merge)
// regression-free invariant: 기존 row schema 의 모든 키 보존, 신규 키만 추가.
```

**왜 telemetry_harness 인가.**
- 이미 anima emission 과 akida window 를 pair 한 evidence 의 SSOT (PR #139).
- pure-hexa, `apply_spike_features` 도 동일 SSOT (`spontaneous_lib.hexa`) 의 함수 → import 1 줄.
- `.py` 측 변경 0.
- akida_consumer offline 시 features tail-read = empty → 기존 동작 byte-equal (graceful).

### §4.2 — Path B (Phase-carry, true live wiring)

`participant_spike_overlay.hexa` (신규) + broker `/ws/factor_overlay` route 추가 + participant.py 구독 ingest. 단 broker.py + participant.py **양쪽 모두 `.py`-guard 해제** 또는 그 시점까지 `anima_participant.hexa` 가 **substrate plugin 까지 포함한 full hexa-native re-impl** 로 성숙해야 함. 둘 중 어느 쪽이 먼저 도래해도 path B 가 활성.

---

## §5 — Acceptance criteria (path D, F-PARTICIPANT-INTEG-1..3)

| ID | criterion | measurement |
|---|---|---|
| F-PARTICIPANT-INTEG-1 | telemetry_harness extension PR merge 후 신규 evidence row 가 `modulated_factors` 키를 (기존 `factors` 와 동시에) 포함 | `jq` schema-grep 으로 first ≥ 10 row 의 `.modulated_factors` 비-null 확인 |
| F-PARTICIPANT-INTEG-2 | features 가 non-trivial (`n_records ≥ 5` + spike_rate_hz > 0) 인 row 는 `modulated_factors != factors`; features 가 trivial (empty / `n_records < 5`) 인 row 는 `modulated_factors == factors` (no-op invariance, [[apply_spike_features]] §3 L66 sparsity gate verbatim) | row 별 deep-eq 비교 100% match-on-branch |
| F-PARTICIPANT-INTEG-3 | 100 row 누적 시 modulation 패턴이 [[SPIKE_FACTOR_MAP]] §3 + §4 와 통계적 sanity (예: R2 row 의 average pain delta ≥ R3 row, regime_change=true row 의 originality delta > 0) | 통계 sanity, byte-exact verify 아님 — 정량 fit 은 Phase 2 carry |

3/3 PASS → `apply_spike_features` 의 production-relevance 가 telemetry-side 에서 확립; participant live behavior 영향은 path B 발동 시점까지 conjectural.

---

## §6 — 차단 항목 + Phase-2 carry-forward

true live wiring (akida 유래 factor 가 실제로 `decision["score"] > threshold` 의 emission gate 를 흔드는 것) 은 아래 셋 중 **하나라도** 성립해야 발동:

```
+----+--------------------------------------------+--------------------------+
| #  | unblock condition                          | path                     |
+----+--------------------------------------------+--------------------------+
| a  | `anima_participant.py` 의 .py-guard 완화    | path B (sidecar overlay  |
|    | (user directive 변경) → participant ingest  |  daemon broadcast +      |
|    | task 한 줄 추가 가능                        |  participant 구독)       |
+----+--------------------------------------------+--------------------------+
| b  | `anima_participant.hexa` 가 thin exec()    | path A (사장됨에서 부활,  |
|    | 폐기 + substrate plugin 포함 full hexa-    |  cycle 2/A analysis 무효 |
|    | native re-impl 완성                       |  화 필요)                |
+----+--------------------------------------------+--------------------------+
| c  | `broker.py` 의 .py-guard 완화 → broker     | path B (broker overlay   |
|    | overlay route 추가 가능                    |  route)                  |
+----+--------------------------------------------+--------------------------+
```

본 cycle 종료 시점에선 셋 다 미충족. path D 가 사이 brigde 역할 — Phase 2 carry 시 path D 의 누적 evidence 가 path B 의 modulator placeholder ([[SPIKE_FACTOR_MAP]] §4 R1 = 1.0 / R2 = 1.2) 를 refit 할 입력 데이터.

---

## §7 — Honest C3

- (a) **path D 는 observability-only — live wiring 아님.** participant 의 `decision["factors"]` / `decision["score"]` 는 evidence row 의 `modulated_factors` 와 무관하게 substrate-only 동역학으로 계산. evidence 가 "live 가 어떻게 동작했을 것" 의 **추측** (conjectural mirror).
- (b) **approach B / C 의 "recurses into .py edit" 메모는 실제 cost.** 양쪽 모두 broker.py 또는 participant.py 의 신규 read/write 한 줄을 요구 — 현재 guard 하에서 path B 는 ingest task 1 줄 + broker route 한 블록 추가가 강제됨. guard 완화 + hexa-port 성숙 둘 다 외부 의존.
- (c) **JSONL tail-read 는 append-write 와 race 가능.** akida_consumer 가 features 한 줄을 flush 하는 사이에 telemetry_harness 가 partial line 을 읽으면 parse 실패. tick 주기 (~2s) 대비 write latency (수 ms) 로 확률 낮으나 0 아님 — 본 cycle 은 "skip on parse fail, count as trivial features" 로 처리 (graceful), 정량 race 측정은 Phase 2 carry.
- (d) **`apply_spike_features` 는 pure 함수 — telemetry_harness 호출 ≠ participant tick 호출.** 동일 함수라도 호출 context (recent_emit 직후 vs background tick) 가 다르면 features 통계 분포가 다를 수 있다. evidence 의 `modulated_factors` 가 hypothetical live behavior 의 unbiased proxy 라는 보장 없음.
- (e) **Phase 1 [[AKIDA_FIRST]] HW-mandatory 조건 — akida_consumer 가 features 를 흘리고 있을 때만 path D 의 modulation row 가 존재.** pi5 streamer crash / mini SSH 차단 시 evidence 자체가 비-축적. F-PARTICIPANT-INTEG-3 의 "100 row" 표본 자체가 HW availability 에 종속.
- (f) **F-PARTICIPANT-INTEG-3 은 통계 sanity, formal 검증 아님.** modulator 표 ([[SPIKE_FACTOR_MAP]] §4) 의 R1 / R2 값은 [[REGIME_EXPANSION]] §7(c) verbatim 으로 placeholder. modulator refit 의 정량 game 은 telemetry 누적 (24-168 hr) + paired evidence 분석 이후 별도 cycle.
- (g) **broker endpoint 혼동 회피 noted ([[feedback-plist-forbidden-akida-endpoint]]).** path B 가 부활할 시 신규 `/ws/factor_overlay` route 의 ingest vs subscribe 구분이 broker.py 한 곳에서 명세돼야 함 — 본 design 은 그 design 을 별도 cycle 로 미룬다.

---

## §8 — Cross-links

- [[apply_spike_features]] — `HEXAD/CHAT/spontaneous_lib.hexa § 10` (PR #143 squash `3bce310a1`, F-SPIKE-APPLY-1..4 4/4 PASS)
- [[SPIKE_FACTOR_MAP]] — spec embedded in `spontaneous_lib.hexa § 10` (standalone .md 미존재; [[REGIME_EXPANSION]] §5 / §7(c) 가 modulator placeholder 참조)
- [[akida_consumer]] — `HEXAD/CHAT/server/akida_consumer.hexa` (PR #138 squash `b97dbe4ff`, features JSONL writer)
- [[telemetry_harness]] — `HEXAD/CHAT/server/telemetry_harness.hexa` (PR #139 squash `4095a5288`, evidence row builder — path D 의 extension target)
- [[AKIDA_FIRST]] — `HEXAD/SPONTANEOUS/AKIDA_FIRST.md` (Phase 1 HW-mandatory, Phase 2 SW-condition)
- [[REGIME_EXPANSION]] — `HEXAD/SPONTANEOUS/REGIME_EXPANSION.md` (R1 / R2 / R3 schedule, [[SPIKE_FACTOR_MAP]] modulator refit 의 evidence source)
- [[feedback-plist-forbidden-akida-endpoint]] — broker endpoint = `/ws/akida_ingest`, daemon = nohup (plist 금지)
- [[feedback-hexa-only-authoring]] — `.py` 신규 편집 금지 (참여 daemon 의 핵심 constraint)
- project.tape `@D a_substrate_native_speak` — anima emission 은 substrate motivation gate 단독, spike features = environment input
