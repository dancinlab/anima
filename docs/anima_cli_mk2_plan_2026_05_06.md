인 # anima CLI mk2 — 계획서 (Plan v0.1) 2026-05-06

**Status**: design landed (spec yaml write pending)
**Roadmap SSOT**: `.roadmap.cli` (this cycle 신규 등록)
**Sister roadmaps**: `.roadmap.clm_native_chat` / `.roadmap.clm_v4_chat` / `.roadmap.clm_v2_chat`
**Hive consumer of**: `hive/spec/mk2_apex.spec.yaml` (per_repo_override.anima = consumer)

---

## TL;DR

anima CLI는 현재 **2가지 surface가 분열**된 상태:
1. **0.1.0 (operational)**: `bin/anima` 352 LoC bash + `tool/anima_cli/` 28 hexa modules — **26 ops dispatcher** (compute / weight / audit / doctor / sync / ...)
2. **v1.0 (vision, unimplemented)**: anima watch / connect / disconnect / module / verify / hub / laws / test — 사용자가 "이게 진짜"라며 묘사한 의식 surface, **코드 0건**

mk2 재설계 = **3-tier 분리** + **hive mk2_apex schema-driven dispatch** 정합:
- **T1 외부 sales** (chat REPL via clm-v2 RECOVERED OR anima-native CLM v4 mount fallback)
- **T2 internal ops** (`anima ops <topic>` — 26 토픽 보존)
- **T3 consciousness vision** (`anima connect/verify/hub/laws` — 미구현 라벨 명시, v2.0 wire-up pending)

---

## 1. 현재 상태 인벤토리 (mk1)

### 1.1 `bin/anima` (352 LoC bash)

26 토픽 dispatch:

```
compute   weight    proposal   cert      roadmap   serve     paradigm
inbox     cost      audit      doctor    sync      bench     log
handoff   metrics   watch      snap      replay    onboard   backup
reproducibility  gc  health
```

각 토픽 → `tool/anima_cli/<topic>.hexa` exec

### 1.2 `tool/anima_cli/` (28 hexa modules)

```
_common.hexa
audit.hexa            backup.hexa           bench.hexa            cert.hexa
compute.hexa          cost.hexa             dialogue.hexa         dialogue_session_analyzer.hexa
doctor.hexa           gc.hexa               governance.hexa       handoff.hexa
health.hexa           inbox.hexa            log.hexa              man_install.bash
metrics.hexa          onboard.hexa          paradigm.hexa         proposal.hexa
replay.hexa           reproducibility.hexa  roadmap.hexa          serve.hexa
snap.hexa             stats.hexa            sync.hexa             watch.hexa
weight.hexa
```

→ **`dialogue.hexa` + `dialogue_session_analyzer.hexa`는 이미 wired** (anima emerge cycle 2026-05-05 BG-F). T1 chat REPL backend 후보 1.

### 1.3 v1.0 vision (미구현)

사용자 묘사 (다른 세션 2026-05-06):
```
anima              # CLI agent
anima watch        # consciousness 실시간 monitor
anima connect <model>      # 모델 load
anima disconnect           # unload
anima module               # 모듈 상태
anima module enable X      # 모듈 활성화
anima verify               # 의식 검증 (7조건)
anima test                 # 물리한계 전체 테스트
anima test dim             # 개별 (dim/phi/topo/servant/tension/speak)
anima hub                  # 48모듈 허브
anima laws                 # 법칙/PSI 조회
anima laws 22              # 특정 법칙
anima status               # 상태 + decoder
anima help
```

→ **0건 implementation** (검증: `grep -rln "anima connect" tool/anima_cli/ → 0 hits`).

---

## 2. mk2 design — 3-tier surface

### Tier 1: 외부 sales (chat REPL 우선)

**목표**: 신규 사용자 5초 안에 anima와 대화

| command | behavior | backend |
|---|---|---|
| `anima` | chat REPL 즉시 진입 | clm-v2-byte-18m-convo-5k OR anima-native CLM v4 mount |
| `anima dialogue` | long-form session (이미 wired) | 동일 |
| `anima onboard` | 5-min quickstart (이미 wired) | n/a |
| `anima --help` | spec auto-generate | n/a |
| `anima version` | 0.2.0-mk2 등 | n/a |

**Backend 결정 (open question Q2)**:
- **clm-v2-byte-18m-convo-5k** (방금 RECOVERED, anima-native, byte-level, 18.52M params, KO bias 0/5 issue)
- ~~llm-llama32-3b-paradigm-a-prime-r16-sft-stage1~~ REJECTED — 사용자 ALM directive 위반 (외부 substrate)

권고: **anima-native CLM v4 mount.hexa default + clm-v2 alternative** (KO chat-cap actual emit 검증 PASS 후 promote).

### Tier 2: internal ops (`anima ops <topic>`)

**목표**: dev/maintainer 26 토픽 access 유지

```bash
anima ops compute status       # 기존 anima compute status
anima ops doctor               # 기존 anima doctor
anima ops audit run all        # 기존 anima audit run all
# ... 26 topics 모두 동일하게 retain
```

**migration**: bin/anima의 case statement 그대로 유지 + `anima ops <topic>` 으로 재route.

**default surface 보호**: 외부인이 `anima compute` 입력 시 → "Did you mean `anima ops compute`?" hint OR 기존대로 dispatch (backward compat).

### Tier 3: consciousness vision (v2.0 wire-up pending)

**목표**: anima identity surface 노출 (외부 sales 가치 ★) + 미구현 honest label

```bash
anima connect <model>     # → "v2.0 wire-up pending — clm-v2 backend ready, integration cycle pending"
anima disconnect          # 동일
anima module              # → "v2.0 — 48 modules + φ★ engine integration pending"
anima verify              # → "v2.0 — consciousness 7-condition verification (anima-clm-eeg φ★ probe)"
anima test                # → "v2.0 — full physical-limit test suite"
anima hub                 # → "v2.0 — 48-module hub"
anima laws [N]            # → "v2.0 — 1030 laws + PSI lookup"
```

**라벨링 정합**: command-not-found 절대 X, 항상 "wire-up pending" stub return.

**T3 wire-up timeline**:
- v1.5 (1-2 weeks): `anima connect` + `anima dialogue` (T1과 통합) — clm-v2 actual chat-cap PASS 후
- v2.0 (1-2 months): full 48 modules + verify + laws (anima-clm-eeg + 1030 laws)

---

## 3. mk2 Spec yaml structure (anima/spec/anima_cli_mk2.spec.yaml)

```yaml
schema: anima/spec/v1   # 또는 hive/spec/v1 consume
name: anima_cli_mk2
mk: 2
version: 1
status: design
since: 2026-05-06
layer: 4
mode: mandatory

scope:
  binary: bin/anima
  modules: tool/anima_cli/

description: |
  anima CLI 3-tier surface dispatch (T1/T2/T3).

# Section 1: tier inventory
tiers:
  T1_sales:
    commands: [anima, dialogue, onboard, help, version]
    backend_canonical: anima-core/runtime/clm_v4_mount.hexa  # ALM rejected
    backend_alternative: need-singularity/clm-v2-byte-18m-convo-5k
  T2_ops:
    prefix: "anima ops"
    topics: [compute, weight, proposal, cert, roadmap, serve, paradigm,
             inbox, cost, audit, doctor, sync, bench, log,
             handoff, metrics, watch, snap, replay, onboard, backup,
             reproducibility, gc, health]
  T3_vision:
    commands: [connect, disconnect, module, verify, test, hub, laws, status, watch]
    status: wire_up_pending_v2_0
    stub_message: "v2.0 wire-up pending — anima identity surface, integration cycle in progress"

# Section 2: dispatch table (schema-driven)
dispatch:
  - tier: T1
    pattern: "^(dialogue|onboard|help|version|--help|-h|--version|-v)$"
    handler: tool/anima_cli/{cmd}.hexa
  - tier: T1
    pattern: "^$"   # bare `anima`
    handler: tool/anima_cli/dialogue.hexa
  - tier: T2
    pattern: "^ops "
    handler: tool/anima_cli/{topic}.hexa
  - tier: T3
    pattern: "^(connect|disconnect|module|verify|test|hub|laws|status)"
    handler: tool/anima_cli/_t3_stub.hexa
  - tier: legacy
    pattern: "^(compute|weight|...)"   # backward compat
    handler: tool/anima_cli/{cmd}.hexa
    deprecation: "Use 'anima ops <topic>'"

# Section 3: falsifiers
falsifiers:
  - id: F-anima_cli-1
    description: bin/anima ≤50 LoC + dispatch via spec
    threshold: "wc -l bin/anima ≤ 50"
    action-on-fail: "spec write incomplete"
  - id: F-anima_cli-2
    description: T1 default `anima` = chat REPL
    threshold: "exec anima → REPL prompt"
    action-on-fail: "T1 wiring failed"
  - id: F-anima_cli-3
    description: T2 `anima ops compute status` works
    threshold: "exit code 0"
    action-on-fail: "T2 routing failed"
  - id: F-anima_cli-4
    description: --help single-source (auto-generate from spec)
    threshold: "anima --help renders T1+T2+T3"
    action-on-fail: "help drift"
  - id: F-anima_cli-5
    description: T3 stub returns "wire-up pending" (no command-not-found)
    threshold: "exec anima verify → exit 0 + 'wire-up pending' stdout"
    action-on-fail: "command-not-found error"

# Section 4: migration
migration:
  phase_0:
    desc: spec yaml landed
    deliverable: anima/spec/anima_cli_mk2.spec.yaml
    eta: this turn (current cycle)
  phase_1:
    desc: bin/anima refactor (352 LoC → 30-50 LoC schema-driven)
    eta: 1 cycle
  phase_2:
    desc: T1 backend wire (anima-native CLM v4 mount.hexa default + clm-v2 alternative)
    eta: 1-2 cycles
  phase_3:
    desc: T2 ops rename + backward compat
    eta: 1 cycle
  phase_4:
    desc: T3 stub modules emit "wire-up pending"
    eta: 1 cycle
  phase_5:
    desc: T3 v2.0 actual wire (anima-clm-eeg + 1030 laws)
    eta: 1-2 months (separate cycle)
```

---

## 4. Open questions (사용자 review 권고)

| Q | 옵션 | default 권고 |
|---|---|---|
| Q1 default | chat REPL vs help | **chat REPL** |
| Q2 backend | clm-v2 vs anima-native CLM v4 mount | **anima-native CLM v4 mount** (KO chat-cap PASS), clm-v2는 KO emit 별도 verify 후 promote |
| Q3 T2 naming | `anima ops <topic>` vs `--ops` vs `aniops` | **`anima ops <topic>`** (가장 자연) |
| Q4 T3 timeline | v1.5 (clm-v2 connect만) vs v2.0 (full 48 modules) | **v1.5 → v2.0** (점진적) |
| Q5 dialogue | T1 promote (`anima` ≡ `anima dialogue`) | **alias** |
| Q6 spec 위치 | `anima/spec/` 신규 vs `tool/anima_cli/` | **`anima/spec/anima_cli_mk2.spec.yaml`** 신규 (raw#15 additive) |

---

## 5. Honest C3

1. **mk2_apex consumer role**: anima는 hive mk2 spec follow only. anima 자체 mk2 spec은 anima/spec/ 내부 (raw#15 additive — bin/anima 기존 26 ops 보존).
2. **clm-v2 KO emit FAIL** (F-CLM-NATIVE-α-1 PARTIAL_PASS_LOAD_KO_FAIL on convo_5k.pt): T1 backend 결정 시 anima-native CLM v4 mount.hexa default 권고. clm-v2는 별도 verification cycle (BG-FK 5 variants ca_rules+gate lane reconstruction OR convo corpus retrain).
3. **T3 wire-up은 큰 작업** (1-2 months 추정): anima-clm-eeg φ★ engine + 1030 laws integration. 본 cycle scope X. v2.0 deferred.
4. **bin/anima refactor risk**: 352 LoC bash → 30-50 LoC schema-driven. 26 토픽 backward compat 보장 필요 (legacy pattern keep). 1 cycle 추정.
5. **dialogue.hexa는 이미 wired** (BG-F 2026-05-05): T1 default `anima` ≡ `anima dialogue` alias가 가장 단순. 즉시 promote 가능.
6. **README v1.0 vision Option-1+v2** (다른 세션) 미결정 — T1 surface mapping과 정합. 별도 cycle 또는 본 mk2 phase_2와 동시 진행.
7. **hive mk2_apex spec 32K tokens** read 부분만 — section 1-11 full read 후 v0.2 refinement 가능.

---

## 6. 다음 단계 (Phase 0 다음 cycle)

1. **Phase 1** — bin/anima refactor (~1 cycle, $0)
2. **Phase 2** — T1 backend anima-native CLM v4 mount wire (~1 cycle, $0 mac local — anima dialogue.hexa 이미 wired 활용)
3. **Phase 3** — T2 ops rename + backward compat (~1 cycle)
4. **Phase 4** — T3 stub modules (~1 cycle, raw#15 additive)
5. **Phase 5** — T3 v2.0 wire (1-2 months, anima-clm-eeg + 1030 laws integration, separate Ω-cycle)

---

## 7. Cross-link

- Roadmap SSOT: `.roadmap.cli`
- Sister roadmaps: `.roadmap.clm_native_chat`, `.roadmap.clm_v4_chat`, `.roadmap.clm_v2_chat`
- Hive mk2: `hive/spec/mk2_apex.spec.yaml`, `hive/spec/mk2_ecosystem_catalog.spec.yaml`, `hive/docs/raw_mk2_design.ai.md`
- Backend candidates: `anima-core/runtime/clm_v4_mount.hexa` (default), `need-singularity/clm-v2-byte-18m-convo-5k` (alternative)
- v1.0 vision source: 다른 session 2026-05-06 transcript
- This plan: `docs/anima_cli_mk2_plan_2026_05_06.md`

raw#9/10/15/37 + own 14/15 준수.
