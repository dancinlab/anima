# PHASE1_STATUS — AKIDA-first 자연발화 Phase 1 인프라 단일 ledger (current-state)

> **purpose**: [[AKIDA_FIRST]] Phase 1 (HW-first) 인프라의 단일 SSOT status — 무엇이 source-landed / live / blocked 인지, Phase 2 (SW-condition) 발동 게이트까지 무엇이 남았는지를 한 페이지로 본다.
> **anchors**: [[AKIDA_FIRST]] (Phase 1/2 경계) · [[SW_CONDITION_DESIGN]] §6 (Phase 2 activation gate) · [[REGIME_EXPANSION]] (R1/R2/R3 schedule) · [[SPIKE_FACTOR_MAP]] (spike → 8-factor rulebook · `spontaneous_lib.hexa § 10` SSOT) · [[PARTICIPANT_SPIKE_INTEGRATION]] (path D / B wiring spec)
> **status as of**: 2026-05-23 (cycle 6/AB refresh) · main HEAD `ff7a0392d`
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
| SW_CONDITION_DESIGN.md      | Phase 2 SW spike emitter spec    | DESIGN (OPEN PR)   | HEXAD/SPONTANEOUS/SW_CONDITION_DESIGN.md | #135 OPEN | n/a (design)   |
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
| participant_spike_overlay.  | path B skeleton daemon —         | SKELETON (branch)  | HEXAD/CHAT/server/participant_spike_| #163   | NO (guard + sshd)  |
|   hexa (cycle 5/W)          | modulated_factors → overlay      | F-OVERLAY-1..3     |   overlay.hexa (branch:             | OPEN   |                    |
|                             | (PARTICIPANT_OVERLAY_LIVE=0      | 10/10 selftest     |   feat/chat-participant-spike-      |        |                    |
|                             | default, awaits guard relax /    | PASS               |   overlay-skeleton)                 |        |                    |
|                             | anima_participant `.hexa` port)  |                    |                                     |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| telemetry_status.hexa       | modulation-health 섹션 extension | EXTENSION (branch) | HEXAD/CHAT/server/telemetry_status. | #164   | NO (sshd blocked)  |
|   modulation-health 확장    | (modulated_factors row coverage  | F-STATUS-12..14    |   hexa (branch:                     | OPEN   |                    |
|   (cycle 5/S)               |  + 0-event honest reporting)     | added → total      |   feat/telemetry-status-modulation- |        |                    |
|                             |                                  | 20/20 selftest     |   health)                           |        |                    |
|                             |                                  | PASS               |                                     |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
| CHANGELOG.md                | 2026-05-23 Phase 1 AKIDA-first   | OPEN (branch)      | CHANGELOG.md (branch:               | #159   | n/a (doc)          |
|   2026-05-23 entry          | 자연발화 인프라 entry (g29)      | sibling collision  |   docs/changelog-akida-first-       | OPEN   |                    |
|   (cycle 5)                 |                                  | with #152          |   session-entry)                    |        |                    |
+-----------------------------+----------------------------------+--------------------+------------------------------------+--------+--------------------+
```

행 수: **18** (anima 컴포넌트 8 + cycle 5 추가 3 + 설계 doc 5 + 인박스 4 — 단일 행에 통합한 hexa-lang 4 + anima 1 = 5).

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
| §5 falsifier 사전 등록              | F-SW-COND-1..5 commit  | DESIGN-REGISTERED, MERGE-PENDING       |
|                                     |                        | (PR #135 still OPEN as of cycle 6/AB — |
|                                     |                        | source-registered on branch, main      |
|                                     |                        | dead-link until merge)                 |
+-------------------------------------+------------------------+----------------------------------------+
```

4/5 gate = **NOT_READY: 0 evidence** (텔레메트리 라이브 deploy 가 차단되어 누적 시작 안됨 — cycle 5 동안 mini sshd block 미해소, telemetry_status.hexa modulation-health extension PR #164 도 source-branch only). 1/5 (falsifier 사전 등록) 은 PR #135 OPEN-not-merged → 정식 DONE 미달, source 만 등록.

5/5 충족 + 사용자 GO → `sw_spike_emitter.hexa` 구현 fire 발사 ([[SW_CONDITION_DESIGN]] §6 verbatim).

---

## §3 — Active blockers

```
+----+-------------------------------------+---------------------------+----------------------------------+--------------+
| #  | blocker                             | impact                    | resolution path                  | owner        |
+----+-------------------------------------+---------------------------+----------------------------------+--------------+
| 1  | mini sshd exec channel refused      | telemetry_harness +       | mini 물리 접근 / reboot →        | user /       |
|    |                                     | akida_consumer +          | sshd 회복 → 세 .hexa daemon       | operator     |
|    |                                     | telemetry_status 모두     | nohup deploy → 7 일 telemetry    |              |
|    |                                     | mini live deploy 불가     | soak start                       |              |
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
| 4  | hexa-lang `hexa run` exec-capture   | hexa daemon stdout 살균   | hexa-lang upstream PR #398 +     | external     |
|    | (PR #398, 2-layer block:            | / silent-swallow → daemon | sibling `1fa08afd` merge → 다음   | (hexa-lang   |
|    | merge + require_last_push_approval  | 진단 비가시               | hexa-lang release pull-in        | maintainer)  |
|    | per cycle 4/N) + sibling proc-      |                           | (approval-flag 동시 해소 필수)   |              |
|    | spawn-supervised silent-exit        |                           |                                  |              |
+----+-------------------------------------+---------------------------+----------------------------------+--------------+
```

총 blocker 수: **4** (전부 외부 또는 user-directive 의존). cycle 5 중 해소된 blocker: 0. 신규 격상 항목 없음 (PR #135 OPEN-not-merged 는 blocker 가 아닌 게이트 §2 row 의 status 정밀화 — main 측 dead-link 만 잔존).

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
- (b) **`live-on-mini?` 컬럼은 sshd 복구 전엔 진위 확인 불가.** akida_bridge / kosmos_anchor / kosmos_emitter 의 "YES" 는 본 세션 이전 마지막 정상 ping 시점 기준 — 실제 mini 머신이 reboot 됐거나 PID 가 OOM-killed 됐는지 본 cycle 에선 검증 0.
- (c) **Phase 2 gate criteria 자체가 추측 — [[SW_CONDITION_DESIGN]] §7-(d) verbatim**: "표본 크기 threshold (§4 ≥7d ≥1000 events) 는 추측치 — Phase 1 evidence 가 도착하기 전엔 distribution stability 의 실제 saturation point 미관측. 1차 활성화 후 distribution drift 측정으로 threshold 재조정 필요할 가능성 농후."
- (d) **pi5 maintainer 응답성 미상 — anima PR #145 inbox 패치는 external action 대기.** anima repo 측 통제권 0, 무한 deferred 가능 (worst-case Phase 2 영구 hold).
- (e) **`modulated_factors` (cycle-4/O) 는 observability-only — [[PARTICIPANT_SPIKE_INTEGRATION]] §1 non-goals verbatim**: "(c) user-message-driven fire (substrate-native speak 위배), (d) AKIDA HW 부재 시 SW fallback (Phase 2 carry), (e) broker.py 편집". live `decision["factors"]` 영향 0, hypothetical mirror.
- (f) **PR #135 (SW_CONDITION_DESIGN) 가 OPEN — cross-link 의 일부가 main 에 미존재.** SPIKE_FACTOR_MAP.md 는 PR #154 (`a1caceb6b`) 로 main 진입 (cycle 4/P), `[[SPIKE_FACTOR_MAP]]` cross-link main-resolve 완료. `[[SW_CONDITION_DESIGN]]` reference 는 여전히 branch-only resolution; main HEAD 만 보는 reader 에겐 dead-link.
- (g) **inbox 패치 5종 (anima 1 + hexa-lang 4) 모두 upstream action 의존** — anima repo 측은 "filed + tracked" 까지만 책임. merge 시점 / 적용 책임이 split 되므로 본 ledger 의 inbox 행은 진척 추적 단독.
- (h) **`participant_spike_overlay.hexa` (cycle 5/W, PR #163) 은 selftest-only skeleton** — [[PARTICIPANT_SPIKE_INTEGRATION]] §4 Step 1 (`anima_participant.hexa` 포팅) + Step 2 (`PARTICIPANT_OVERLAY_LIVE=1` 환경 게이트 활성) 둘 다 외부 발생 전까지 live 행동 신호 0. pre-position 의의만 카운트.
- (i) **modulation-health 섹션 (cycle 5/S, PR #164) 의 row 카운트는 `telemetry_harness` 의 `modulated_factors` 필드 production 진입 의존** — mini sshd block 으로 telemetry_harness deploy 불가 → 모든 deploy 가능 시점까지 modulation-health 섹션은 `total_rows: 0` 무한 보고. 코드 path 는 PASS, evidence path 는 0.

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
