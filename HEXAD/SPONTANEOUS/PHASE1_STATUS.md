# PHASE1_STATUS — AKIDA-first 자연발화 Phase 1 인프라 단일 ledger (current-state)

> **purpose**: [[AKIDA_FIRST]] Phase 1 (HW-first) 인프라의 단일 SSOT status — 무엇이 source-landed / live / blocked 인지, Phase 2 (SW-condition) 발동 게이트까지 무엇이 남았는지를 한 페이지로 본다.
> **anchors**: [[AKIDA_FIRST]] (Phase 1/2 경계) · [[SW_CONDITION_DESIGN]] §6 (Phase 2 activation gate) · [[REGIME_EXPANSION]] (R1/R2/R3 schedule) · [[SPIKE_FACTOR_MAP]] (spike → 8-factor rulebook · `spontaneous_lib.hexa § 10` SSOT) · [[PARTICIPANT_SPIKE_INTEGRATION]] (path D / B wiring spec)
> **status as of**: 2026-05-23 (cycle 8/CC refresh) · main HEAD `1953e6b8b`
> **scope**: spike ingest path + telemetry + Phase-2-gate observability + spec docs + cross-repo inbox patches. 본 ledger 는 snapshot — cycle 누적 시 재발행.

---

## §1 — Phase 1 인프라 inventory

```
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| component                   | role                             | status             | source                              | PR     | live-on-mini?      |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| pi5 spike_streamer.py       | NPU mesh → spike record emit     | LIVE (R3 only)     | pi5 host /home/ubuntu/anima/        | (ext)  | n/a (lives on pi5) |
|                             | (R1/R2 pending inbox patch)      |                    |   SUB_ENGINES/AKIDA/scripts/        |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| akida_bridge.hexa           | pi5 WS subscribe → broker        | LIVE (mini PID up) | HEXAD/CHAT/server/akida_bridge.hexa | #121   | YES (predates arc) |
|                             | /ws/akida_ingest forwarder       |                    |                                     |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| kosmos_anchor.hexa          | KOSMOS RF anchor emitter (adj.)  | LANDED (source)    | HEXAD/CHAT/server/kosmos_anchor.hexa| #116   | YES (predates arc) |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| kosmos_emitter.hexa         | KOSMOS production emit daemon    | LANDED (source)    | HEXAD/CHAT/server/kosmos_emitter.hexa| #117 / #130 | YES (predates arc) |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| akida_consumer.hexa         | broker /akida/recent poll →      | LANDED (source)    | HEXAD/CHAT/server/akida_consumer.hexa| #138  | NO (sshd blocked)  |
|                             | features JSONL stream (1 Hz)     | 7/7 selftest PASS  |                                     |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| telemetry_harness.hexa      | anima emit ⇄ spike window pair   | LANDED (source)    | HEXAD/CHAT/server/telemetry_harness.hexa | #139 | NO (sshd blocked) |
|                             | → evidence JSONL                 | 9/9 selftest PASS  |                                     |        |                    |
|                             | (modulated_factors extension =   | (extension on      |                                     |(branch:|                    |
|                             | branch-only, not on main)        |  branch only)      |                                     | feat/  |                    |
|                             |                                  |                    |                                     | telem- |                    |
|                             |                                  |                    |                                     | modul- |                    |
|                             |                                  |                    |                                     | factors)|                   |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| telemetry_status.hexa       | Phase 2 gate observability CLI   | LANDED (source)    | HEXAD/CHAT/server/telemetry_status.hexa | #144 | NO (sshd blocked)  |
|                             | (spans / rows / regime dist /    | 11/11 selftest     |                                     |        |                    |
|                             |  spike-rate hist / 4-cond gate)  | PASS               |                                     |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| spontaneous_lib.hexa        | pure fn — spike features →       | LANDED (source)    | HEXAD/CHAT/spontaneous_lib.hexa     | #143   | n/a (pure lib)     |
|   ::apply_spike_features    | 8-factor delta + regime modulator| 4/4 F-SPIKE-APPLY |  (§10 = SPIKE_FACTOR_MAP SSOT)      |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| AKIDA_FIRST.md              | Phase 1/2 boundary + infra table | LANDED             | HEXAD/SPONTANEOUS/AKIDA_FIRST.md    | f7af268db (no PR) | n/a |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| SW_CONDITION_DESIGN.md      | Phase 2 SW spike emitter spec    | LANDED (design)    | HEXAD/SPONTANEOUS/SW_CONDITION_DESIGN.md | #135 MERGED 1953e6b8 | n/a |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| SPIKE_FACTOR_MAP.md         | spike → 8-factor rulebook        | LANDED (design)    | HEXAD/SPONTANEOUS/SPIKE_FACTOR_MAP.md | #154   | n/a (design)       |
|                             | (standalone .md mirror of §10)   | (a1caceb6b)        |                                     |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| REGIME_EXPANSION.md         | pi5 streamer R1/R2/R3 schedule   | LANDED (design)    | HEXAD/SPONTANEOUS/REGIME_EXPANSION.md| #141  | n/a (design)       |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| PARTICIPANT_SPIKE_INTEGRATION.md | path D / B wiring spec      | LANDED (design)    | HEXAD/CHAT/PARTICIPANT_SPIKE_INTEGRATION.md | #146 | n/a (design)  |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| inbox/patches/pi5-spike-    | pi5 streamer --regime-schedule   | FILED (coord)      | inbox/patches/pi5-spike-streamer-   | #145   | n/a (cross-repo)   |
|   streamer-regime-schedule  | R3/R1/R2 coord patch (external)  | external pending   |   regime-schedule.md                |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| hexa-lang inbox patch       | proc_spawn_supervised daemon     | FILED (upstream)   | (hexa-lang repo)                    | hexa-  | n/a (cross-repo)   |
|   proc-spawn-supervised-    | silent-exit under nohup (macOS)  |                    |                                     | lang   |                    |
|   daemon-silent-exit        |                                  |                    |                                     | `1fa08afd` | n/a            |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| hexa-lang inbox patch       | websocket streaming client has   | FILED (upstream)   | (hexa-lang repo)                    | hexa-  | n/a (cross-repo)   |
|   websocket-streaming-      | hard websocat dependency         |                    |                                     | lang   |                    |
|   client-websocat-dep       |                                  |                    |                                     | `9d0817c0` | n/a            |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| hexa-lang inbox patch       | exec() / hexa run printf stdout  | FILED (upstream)   | (hexa-lang repo)                    | hexa-  | n/a (cross-repo)   |
|   hexa-run-exec-printf-     | swallow (daemon stdout silent)   |                    |                                     | lang   |                    |
|   stdout-swallow            |                                  |                    |                                     | PR #398 OPEN | n/a          |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| hexa-lang inbox patch       | runpod session findings          | FILED (upstream)   | (hexa-lang repo)                    | hexa-  | n/a (cross-repo)   |
|   cloud-runpod-session-     | (4 items, 2026-05-23)            |                    |                                     | lang   |                    |
|   findings-anima            |                                  |                    |                                     | `c07b426f` | n/a            |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| participant_spike_overlay.  | path B skeleton daemon —         | LANDED (source)    | HEXAD/CHAT/server/participant_spike_| #163   | NO (guard + sshd)  |
|   hexa (cycle 5/W)          | modulated_factors → overlay      | F-OVERLAY-1..3     |   overlay.hexa                      | MERGED |                    |
|                             | (PARTICIPANT_OVERLAY_LIVE=0      | 10/10 selftest     |                                     | f336b850 |                  |
|                             | default, awaits guard relax /    | PASS               |                                     |        |                    |
|                             | anima_participant `.hexa` port)  |                    |                                     |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| telemetry_status.hexa       | modulation-health 섹션 extension | LANDED (source)    | HEXAD/CHAT/server/telemetry_status. | #164   | NO (sshd resp.,    |
|   modulation-health 확장    | (modulated_factors row coverage  | F-STATUS-12..14    |   hexa                              | MERGED |  deploy in flight) |
|   (cycle 5/S)               |  + 0-event honest reporting)     | added → total      |                                     | 8defea28 |                  |
|                             |                                  | 20/20 selftest     |                                     |        |                    |
|                             |                                  | PASS               |                                     |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| CHANGELOG.md                | 2026-05-23 Phase 1 AKIDA-first   | LANDED             | CHANGELOG.md                        | #159   | n/a (doc)          |
|   2026-05-23 entry          | 자연발화 인프라 entry (g29)      | (g29 verdict       |                                     | MERGED |                    |
|   (cycle 5/X)               |                                  |  table)            |                                     | 56211734 |                  |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| PHASE1_STATUS.md            | this ledger (snapshot)           | LANDED             | HEXAD/SPONTANEOUS/PHASE1_STATUS.md  | #170   | n/a (doc)          |
|   cycle 6/AB refresh        | — cycle 6/AB initial publish     |                    |                                     | MERGED |                    |
|                             |                                  |                    |                                     | 42ea2379 |                  |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| EVIDENCE_ANALYZER.md        | modulated_factors ↔ emission     | LANDED (design)    | HEXAD/SPONTANEOUS/EVIDENCE_ANALYZER.md | #171 | n/a (design)       |
|   (cycle 6/AC)              | correlation analyzer spec        |                    |                                     | MERGED |                    |
|                             |                                  |                    |                                     | 0479229f |                  |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| akida_consumer.hexa         | mean_spike_ids_count =           | LANDED (source)    | HEXAD/CHAT/server/akida_consumer.hexa | #172 | NO (sshd resp.,    |
|   mean_spike_ids_count fix  | mean(len(spike_ids)) + F-4       | F-4 PASS, total   |                                     | MERGED |  deploy in flight) |
|   (cycle 6/AD)              | selftest                         | 8/8                |                                     | a41c4192 |                  |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| telemetry_harness.hexa      | spike_window.mean_spike_ids_     | LANDED (source)    | HEXAD/CHAT/server/telemetry_harness.hexa | #175 | NO (sshd resp., |
|   mean_spike_ids_count fix  | count = mean(len(spike_ids))     | selftest update    |                                     | MERGED |  deploy in flight) |
|   (cycle 7/BC)              | (stub → computed)                |                    |                                     | afd27e90 |                  |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| mini_sshd_diag.hexa         | sshd channel-reject 5-cause      | LANDED (source)    | HEXAD/CHAT/server/mini_sshd_diag.hexa | #153 | n/a (diag tool)    |
|   (cycle 6/sshd-diag)       | 진단 도구 (ssh_rc / sshd_config /| 301 LoC            |                                     | MERGED |                    |
|                             | authorized_keys / sshd_log /     |                    |                                     | 472aa114 |                  |
|                             | launchd)                         |                    |                                     |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| MINI_SSHD_DIAGNOSIS.md      | cycle 7/BD all-clean baseline    | LANDED (doc)       | HEXAD/CHAT/server/MINI_SSHD_DIAGNOSIS.md | #173 | n/a (doc)       |
|   (cycle 7/BD)              | — 3/3 ssh + 1/1 scp + 1/1 remote | supersedes §3      |                                     | MERGED |                    |
|                             | hexa run all PASS, diag CLEAN    | blocker #1 status  |                                     | 4c1ec63c |                  |
|                             | 5/5 categories                   |                    |                                     |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
```

행 수: **24** (anima 컴포넌트 8 + cycle 5 추가 3 + cycle 6-7 추가 6 [PHASE1_STATUS#170 / EVIDENCE_ANALYZER#171 / akida_consumer mean_spike fix#172 / telemetry_harness mean_spike fix#175 / mini_sshd_diag#153 / MINI_SSHD_DIAGNOSIS#173] + 설계 doc 5 + 인박스 4 — 단일 행에 통합한 hexa-lang 4 + anima 1 = 5).

---

## §2 — Phase 1 → Phase 2 transition gate

[[SW_CONDITION_DESIGN]] §6 의 4-조건 + §5 falsifier 사전 등록을 **verbatim** 으로 인용 (`docs/spontaneous-sw-condition-design-v2` branch · PR #135 OPEN):

```
+-------------------------------------+------------------------+----------------------------------------+
| gate                                | threshold              | current status                         |
+-------------------------------------+------------------------+----------------------------------------+
| HW telemetry 기간                   | ≥ 7 일 연속            | NOT_READY (telemetry_harness not       |
|                                     |                        | deployed live → 0 일 누적)             |
+-------------------------------------+------------------------+----------------------------------------+
| paired emission events              | ≥ 1000                 | NOT_READY (0 events — JSONL 미생성)    |
+-------------------------------------+------------------------+----------------------------------------+
| regime 다양성                       | ≥ 2 종 관측 + 전환 ≥ 5 | NOT_READY (pi5 streamer R3 단독,       |
|                                     |                        | R1/R2 inbox 패치 #145 외부 대기)       |
+-------------------------------------+------------------------+----------------------------------------+
| distribution stability              | 7d→14d→28d KS drift    | NOT_READY (분포 자체 0)                |
|                                     | ≤ 10%                  |                                        |
+-------------------------------------+------------------------+----------------------------------------+
| §5 falsifier 사전 등록              | F-SW-COND-1..5 commit  | DONE — PR #135 MERGED 1953e6b8         |
|                                     |                        | (cycle 8 마무리 단계 main 진입,        |
|                                     |                        | cross-link main-resolved)              |
+-------------------------------------+------------------------+----------------------------------------+
```

4/5 evidence gate = **NOT_READY: 0 evidence** (telemetry live deploy 누적 0일 — cycle 7/BD 에서 mini sshd 응답성 회복 확인됐고 cycle 8/CA 가 deploy 실행 중, 7-day soak 카운트는 CA 의 실제 deploy 완료 시점부터 시작). 1/5 (falsifier 사전 등록) = **DONE** (PR #135 merged, cycle 6/AB 시점의 dead-link 해소).

5/5 충족 + 사용자 GO → `sw_spike_emitter.hexa` 구현 fire 발사 ([[SW_CONDITION_DESIGN]] §6 verbatim).

---

## §3 — Active blockers

```
+----+-------------------------------------+---------------------------+----------------------------------+--------------+
| #  | blocker                             | impact                    | resolution path                  | owner        |
+----+-------------------------------------+---------------------------+----------------------------------+--------------+
| 1  | mini sshd exec channel refused      | (was) telemetry_harness + | RESOLVED 2026-05-23 18:06 KST    | (resolved)   |
|    | — RESOLVED cycle 7/BD               | akida_consumer +          | (cycle 7/BD): 3/3 ssh exec +     |              |
|    | (MINI_SSHD_DIAGNOSIS.md #173)       | telemetry_status mini     | 1/1 scp + 1/1 remote hexa run    |              |
|    |                                     | deploy 불가 → (now)       | all PASS, mini_sshd_diag CLEAN   |              |
|    |                                     | deploy unblocked,         | 5/5 categories. Root cause       |              |
|    |                                     | cycle 8/CA in flight      | unknown (likely operator reboot  |              |
|    |                                     |                           | / transient launchd state).      |              |
|    |                                     |                           | Deploy in flight (cycle 8/CA),   |              |
|    |                                     |                           | outcome not yet evidenced here.  |              |
+----+-------------------------------------+---------------------------+----------------------------------+--------------+
| 2  | pi5 streamer R1/R2 미존재           | gate "≥ 2 종 + ≥ 5 전환"  | inbox patch #145 (anima 측 SSOT) | external     |
|    | (R3 단독 라이브)                    | 충족 0 → Phase 2 발동     | → pi5 maintainer 가 streamer.py  | (pi5         |
|    |                                     | gate 영구 NOT_READY       | 에 --regime-schedule 적용 +      | maintainer)  |
|    |                                     |                           | systemd promote                  |              |
+----+-------------------------------------+---------------------------+----------------------------------+--------------+
| 3  | anima_participant.py `.py` 신규     | path B (true live wiring  | (a) `.py` guard 완화 user        | user /       |
|    | 편집 guard (hexa-only authoring)    | — akida 유래 factor 가    | directive 변경, OR (b)           | future cycle |
|    |                                     | 실제 emission gate 흔듦)  | anima_participant.hexa full       |              |
|    |                                     | 영구 deferred             | substrate-plugin re-impl 성숙    |              |
+----+-------------------------------------+---------------------------+----------------------------------+--------------+
| 4  | hexa-lang `hexa run` exec-capture   | hexa daemon stdout 살균   | spec accepted upstream            | external     |
|    | — PARTIALLY RESOLVED                | / silent-swallow → daemon | (PR #398 MERGED, observed         | (hexa-lang   |
|    | (spec PR #398 MERGED upstream,      | 진단 비가시 (impl path    | cycle 6/check), downstream impl   | maintainer)  |
|    | downstream impl path                | 미배포 동안 동일 증상)    | (`exec_capture` + caller-stdout  |              |
|    | exec_capture + caller-stdout        |                           | inherit) shipping pending next    |              |
|    | inherit pending)                    |                           | hexa-lang release pull-in.        |              |
+----+-------------------------------------+---------------------------+----------------------------------+--------------+
```

총 blocker 수: **4** (1 RESOLVED, 1 PARTIALLY RESOLVED, 2 unchanged). cycle 6-7 중 해소된 blocker: **#1 (cycle 7/BD)** + 부분 해소 **#4 spec (cycle 6/check)**. cycle 8/CC 신규 격상 항목 없음. 게이트 §2 row "falsifier 사전 등록" 은 PR #135 MERGED 로 DONE 승격, blocker 아닌 게이트 status 정밀화.

---

## §4 — Next concrete steps (cycle 5+)

ordered list — blocker resolution 시 순차 발화:

1. **mini sshd 회복 (blocker #1) →** `akida_consumer.hexa` + `telemetry_harness.hexa` mini deploy + `akida_bridge.hexa` restart → cycle-4/E sanity rerun (deploy smoke) → 첫 evidence JSONL row 누적 개시.
2. **pi5 R1/R2 schedule 출시 (blocker #2) →** broker `/akida/recent` 가 `≥ 2` distinct regime + transition `≥ 5` 관측 → `telemetry_status.hexa` 4-condition gate 의 regime row PASS 누적 시작.
3. **≥ 7 일 telemetry 누적 →** `telemetry_status.hexa` 의 spans / rows / regime dist / spike-rate hist 4 row all-PASS → [[EVIDENCE_ANALYZER]] 1-shot run 으로 [[SPIKE_FACTOR_MAP]] §3/§4 (re)검증 + KS drift 게이트 충족 확정 → Phase 2 SW emitter (`sw_spike_emitter.hexa`) 구현 발화 ([[SW_CONDITION_DESIGN]] §3 daemon outline 기반).
4. **PR #134 (SPIKE_FACTOR_MAP) + PR #135 (SW_CONDITION_DESIGN) merge →** 두 design doc 가 main 진입 → cross-link `[[SW_CONDITION_DESIGN]]` / `[[SPIKE_FACTOR_MAP]]` 모두 main 에서 dead-link 해소.
5. **`feat/telemetry-modulated-factors` branch merge →** telemetry_harness 의 `modulated_factors` 필드 production line 진입 → path D ([[PARTICIPANT_SPIKE_INTEGRATION]] §4.1) observability 활성 → 100 row 누적 시 F-PARTICIPANT-INTEG-1..3 측정 가능.
6. **anima_participant `.hexa` 포팅 완료 OR `.py` guard 완화 →** path D 의 `modulated_factors` evidence 가 live `decision["factors"]` 로 wire-in (path B 발동, [[PARTICIPANT_SPIKE_INTEGRATION]] §4.2) → spike-grounded 자연발화 production 확립.

---

## §5 — Honest C3

- (a) **본 doc 은 snapshot — cycle 단위로 stale 됨.** 매 cycle 종료 시 재발행 (또는 인박스 핸드오프 노트로 보강) 필요. `live-on-mini?` 컬럼은 mini sshd 회복 시점에 전수 재검증 필수.
- (b) **`live-on-mini?` 컬럼 — cycle 7/BD 시점 sshd 응답성 회복 확인, 단 daemon PID 상태는 cycle 8/CA deploy 결과로 별도 evidence 필요.** akida_bridge / kosmos_anchor / kosmos_emitter 의 "YES" 는 prior 정상 ping 기준; 새 daemon (akida_consumer / telemetry_harness / telemetry_status) 의 "NO (sshd resp., deploy in flight)" 는 CA 의 actual deploy 완료 시점에 본 ledger 전수 재검증 필요.
- (c) **Phase 2 gate criteria 자체가 추측 — [[SW_CONDITION_DESIGN]] §7-(d) verbatim**: "표본 크기 threshold (§4 ≥7d ≥1000 events) 는 추측치 — Phase 1 evidence 가 도착하기 전엔 distribution stability 의 실제 saturation point 미관측. 1차 활성화 후 distribution drift 측정으로 threshold 재조정 필요할 가능성 농후."
- (d) **pi5 maintainer 응답성 미상 — anima PR #145 inbox 패치는 external action 대기.** anima repo 측 통제권 0, 무한 deferred 가능 (worst-case Phase 2 영구 hold).
- (e) **`modulated_factors` (cycle-4/O) 는 observability-only — [[PARTICIPANT_SPIKE_INTEGRATION]] §1 non-goals verbatim**: "(c) user-message-driven fire (substrate-native speak 위배), (d) AKIDA HW 부재 시 SW fallback (Phase 2 carry), (e) broker.py 편집". live `decision["factors"]` 영향 0, hypothetical mirror.
- (f) **cycle 6/AB 시점의 cross-link dead-link 해소 (cycle 8/CC) — PR #135 (SW_CONDITION_DESIGN) MERGED `1953e6b8` + PR #154 (SPIKE_FACTOR_MAP) MERGED `a1caceb6b`.** 본 ledger 의 `[[SW_CONDITION_DESIGN]]` / `[[SPIKE_FACTOR_MAP]]` cross-link 모두 main-resolved. PR #135 의 main merge 는 cycle 8 마무리 단계 (HEAD `1953e6b8b`) 에 합류.
- (g) **inbox 패치 5종 (anima 1 + hexa-lang 4) 모두 upstream action 의존** — anima repo 측은 "filed + tracked" 까지만 책임. merge 시점 / 적용 책임이 split 되므로 본 ledger 의 inbox 행은 진척 추적 단독.
- (h) **`participant_spike_overlay.hexa` (cycle 5/W, PR #163) 은 selftest-only skeleton** — [[PARTICIPANT_SPIKE_INTEGRATION]] §4 Step 1 (`anima_participant.hexa` 포팅) + Step 2 (`PARTICIPANT_OVERLAY_LIVE=1` 환경 게이트 활성) 둘 다 외부 발생 전까지 live 행동 신호 0. pre-position 의의만 카운트.
- (i) **modulation-health 섹션 (cycle 5/S, PR #164) 의 row 카운트는 `telemetry_harness` 의 `modulated_factors` 필드 production 진입 의존** — cycle 7/BD 에서 sshd 응답성 회복 + cycle 8/CA 가 deploy 중, CA 완료 + 첫 row 누적 시점까지 modulation-health 섹션은 `total_rows: 0` 보고. 코드 path 는 PASS, evidence path 는 CA 결과 미평가 (본 ledger 는 cycle 8/CC = CC ⊥ CA disjoint per g34).
- (j) **mini sshd RESOLVED 는 cycle 7/BD 시점 baseline 만 — 재발 가능성 미배제.** MINI_SSHD_DIAGNOSIS §3 "What changed between round 9 and now: Unknown" 명시 — diag 도구가 5 카테고리 zero misconfig 검출했으므로 재발 시 원인은 TCC / kernel session faults / launchd throttling 범위 (도구 미커버). cycle 8/CA deploy 가 완료 + sustained 시점까지 RESOLVED 는 잠정.

---

## §6 — 관련 link

- [[AKIDA_FIRST]] — Phase 1/2 경계 정의 + 인프라 라이브 표 (small)
- [[SPIKE_FACTOR_MAP]] — spike → 8-factor rulebook (`spontaneous_lib.hexa § 10` SSOT, standalone .md = PR #134 OPEN)
- [[SW_CONDITION_DESIGN]] — Phase 2 SW emitter spec (PR #135 OPEN, §6 gate verbatim source)
- [[REGIME_EXPANSION]] — pi5 streamer R1/R2/R3 schedule (PR #141 merged)
- [[PARTICIPANT_SPIKE_INTEGRATION]] — path D / B wiring spec (PR #146 merged)
- [[akida_bridge]] · [[akida_consumer]] · [[telemetry_harness]] · [[telemetry_status]] · [[kosmos_anchor]] · [[kosmos_emitter]] · [[apply_spike_features]] — `HEXAD/CHAT/(server|spontaneous_lib).hexa`
- project.tape `@D a_substrate_native_speak` — 자연발화 anchor (HW/SW 모두 동일)
- CHANGELOG.md + `git log main --oneline` — cycle 단위 진척 lineage (본 doc 은 current-state, lineage 는 CHANGELOG 가 SSOT)
