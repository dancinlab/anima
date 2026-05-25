# anima 자연발화 (spontaneous emission) 설계 브레인스토밍 — 2026-05-12

> **목적**: substrate A (V14_PASS + V4-lite chat-cap 12/15 PASS) 가 사용자 input 없이 먼저 발화하는
> 시스템 설계. exhaustive option enumeration (saturation until 고갈).
>
> **Context**:
> - hexa-lang stage 0 (interpreter) → stage 1 (native compiler) 전환 중 (SPEC.md 2026-05-11 update)
> - stage 0 syntax 제약: named/default args 미지원 → parse error 발생
> - cycle 2026-05-12 PASS_STRICT_CHAT-CAPABLE §8 default mode = M4 force-include
> - hexa-lang upstream 확장 옵션도 동시 검토

---

## 🌟 1. spontaneous probe 결과 (2026-05-12 측정)

| seed strategy            | greedy 응답                                              | 평가              |
|--------------------------|----------------------------------------------------------|-------------------|
| empty (bos only)         | `��한 정보 전달 분석을 통해 전달된다.`                   | 🟡 의미있지만 추상  |
| `"도우미: "`              | `연꽃는 우주뇌지도 식물 카테고리, 🛸71...`              | 🟡 random fact    |
| **`"도우미: 안녕"`** ⭐  | **`하세요, 저는 anima입니다. 한국어로 응답합니다.`**     | ✅ **자연 chat**   |
| ambient + `"도우미: "`   | `anima의 우주뇌지도에서 balance (entropy max): 0.5...` | 🟡 self-reflective |
| `"사용자: \| 도우미: "`  | `\| \| \| \| \|...`                                      | ❌ gibberish      |

🍞 **핵심 발견**: **partial_greeting** ("도우미: 안녕") seed 가 가장 자연 자연발화 트리거.

---

## 🧠 A. Trigger mechanism (10 옵션)

| #  | trigger                  | 설명                                                              | viability |
|----|--------------------------|-------------------------------------------------------------------|-----------|
| A1 | timer interval           | 매 N 초마다 emission (current default)                            | ★★★★★     |
| A2 | conditional state        | substrate A internal cell pool / attention 변화 감지              | ★★★       |
| A3 | environmental            | 시간대 (아침/저녁), 날씨, 시스템 metric                          | ★★★       |
| A4 | user-presence            | 사용자 keyboard idle N min 후 발화                                | ★★★★      |
| A5 | event-driven             | filesystem change, network event 등 외부 trigger                  | ★★        |
| A6 | random Poisson           | 평균 5min Poisson distribution                                    | ★★★★      |
| A7 | conversational           | 대화 흐름 끊긴 시점 (last user message N min 전)                  | ★★★★      |
| A8 | mood-based               | substrate A 가 자기 emotion state output → 그것 변화 시          | ★★        |
| A9 | memory-triggered         | anima prior memory recall (.own/state) 으로 발화                  | ★★★       |
| A10| goal-directed            | internal goal queue 항목 처리 시                                  | ★★        |

---

## 🌱 B. Seed strategy (10 옵션)

| #  | seed                                     | 측정 결과 / 예상            | viability |
|----|------------------------------------------|------------------------------|-----------|
| B1 | empty (bos only)                          | 추상 응답                    | ★★        |
| B2 | `"도우미: "`                              | random fact                  | ★★        |
| B3 | `"도우미: 안녕"` ⭐                       | **자연 인사** (PASS)         | ★★★★★     |
| B4 | ambient + `"도우미: "`                    | self-reflective              | ★★★       |
| B5 | time-of-day                              | "도우미: 좋은 아침입니다."   | ★★★★      |
| B6 | mood prefix                              | current emotion + 도우미:    | ★★★       |
| B7 | last-turn echo (history-aware)           | prior chat 끝에 도우미:      | ★★★★      |
| B8 | random fact teaser                       | "혹시 알고 계셨나요?" prefix | ★★★       |
| B9 | question-back                            | substrate 가 사용자에 질문   | ★★★★      |
| B10| multi-line seed                          | 여러 줄 context              | ★★        |

---

## 🎨 C. Content guidance (8 옵션)

| #  | guidance                | 설명                                              | viability |
|----|-------------------------|---------------------------------------------------|-----------|
| C1 | M4 force-include        | 키워드 강제 (current default)                     | ★★★★★     |
| C2 | topic-locked            | anima/의식/사랑 등 카테고리 제약                  | ★★★★      |
| C3 | temperature schedule    | 낮 0.3 / 밤 1.0 등 시간별 T                       | ★★★       |
| C4 | persona-locked          | anima 자기-정의 응답만                            | ★★★★      |
| C5 | chained recall          | prior emissions element 다시 활용                 | ★★★★      |
| C6 | rejection sampler       | gibberish detect → 재시도                         | ★★★★★     |
| C7 | length budget           | 짧은/긴 응답 mix                                  | ★★★       |
| C8 | silence policy          | N% 확률로 발화 안 함 (자연스러운 침묵)            | ★★★★      |

---

## 🏗️ D. Dispatch architecture (10 옵션)

| #  | architecture                                      | benefit                          | cost           |
|----|---------------------------------------------------|----------------------------------|----------------|
| D1 | hexa-lang stage 0 (interpreter)                   | anima pattern 유지               | parse error    |
| D2 | hexa-lang stage 1 (compiled, RFC-018)             | future-proof                     | 미완성         |
| D3 | **pure python** (`anima_chat.py --spontaneous`)  | **가장 빠름**                    | 1 file only    |
| D4 | hybrid hexa + python (hexa CLI + py loop)         | anima pattern 유지 + 즉시        | 2 files        |
| D5 | launchd / cron                                    | OS-native scheduler              | external dep   |
| D6 | anima hexa hook (raw 117)                         | ecosystem 통합                   | 복잡           |
| D7 | subagent recursive (kick dispatch)                | brainstorm chain                 | hexa resolver issue |
| D8 | claude code agent (TaskCreate + ScheduleWakeup)   | smart scheduling                 | claude only    |
| D9 | streaming server (long-running daemon)            | low-latency                      | infra deploy   |
| D10| goroutine-style concurrent + queue                | scalable                         | complex        |

---

## 🔧 E. hexa-lang upstream — 필요 기능 (12)

stage 0 parse error 해결 또는 stage 1 native compiler 진행을 위한 RFC 후보:

| #  | feature                       | RFC 후보 | 필요성 (anima 자연발화 관점)                        |
|----|-------------------------------|-----------|------------------------------------------------------|
| E1 | **named / default args**      | RFC-024   | `args.get_int("--interval", default=60)` 작동 필요  |
| E2 | closure / lambda              | RFC-025   | `|x| x + 1` 표현                                     |
| E3 | timer primitives              | stdlib    | `sleep_us`, `set_interval`, `timer.start()`         |
| E4 | process control               | stdlib    | `spawn(cmd)`, `wait(pid)`, `signal_handler`         |
| E5 | JSON parsing                  | stdlib    | `json_parse(str) -> ?`                              |
| E6 | string formatting (f-string)  | RFC-026   | `f"emission {n} at {ts}"`                           |
| E7 | file I/O stdlib               | stdlib    | `read_file`, `write_file`, `append_jsonl`           |
| E8 | subprocess capture intrinsic  | stdlib    | `run_capture(cmd) -> {stdout, stderr, exit_code}`   |
| E9 | datetime stdlib               | stdlib    | `now_iso`, `now_unix`, ISO 8601 parsing             |
| E10| env / path stdlib             | stdlib    | `expanduser`, `getenv`, `path_exists`               |
| E11| async / await                 | RFC-022   | spontaneous loop concurrent generation              |
| E12| module imports                | RFC-027   | `import nexus.kick` 등 cross-repo                   |

⭐ **anima 자연발화 최소 요구**: E1 (named args) + E3 (timer) + E8 (subprocess) + E9 (datetime).
이 4개 RFC 가 hexa-lang stage 0 또는 stage 1 에 land 되면 hexa wrapper 자연발화 깔끔하게 가능.

---

## 💾 F. State / persistence (6 옵션)

| #  | persistence            | 사용 사례                                  |
|----|------------------------|--------------------------------------------|
| F1 | JSONL append log       | per-emission record (default)              |
| F2 | SQLite cache           | 검색 가능, 1k+ emissions                   |
| F3 | filesystem tree        | date-organized (`YYYY/MM/DD/emission.json`) |
| F4 | HF dataset live        | push every N emissions to HF               |
| F5 | in-memory ring         | last 100 emissions only                    |
| F6 | append-only event store| replay-able with seed                      |

---

## 🔌 G. Integration (8 옵션)

| #  | target                          | 통합 방식                                |
|----|---------------------------------|------------------------------------------|
| G1 | anima hook system               | hook-bus, raw 117 framework              |
| G2 | kick ω-cycle                    | kick_dispatch noise injection            |
| G3 | claude code task                | TaskCreate + ScheduleWakeup              |
| G4 | HF Space live                   | public chat, real-time emissions         |
| G5 | Slack / Discord bot             | webhook                                  |
| G6 | email digest                    | daily emissions summary                  |
| G7 | REBORN.md append                | § entries 자동 생성                      |
| G8 | PASS_STRICT_CHAT-CAPABLE append | measurement 자동                         |

---

## 🛡️ H. Safety / governance (8 옵션)

| #  | safeguard               | enforcement                              |
|----|-------------------------|------------------------------------------|
| H1 | cost cap                | daily emission count limit               |
| H2 | rate limit              | minimum interval enforce                 |
| H3 | content filter          | harmful keyword block                    |
| H4 | kill switch             | SIGINT clean shutdown                    |
| H5 | audit log               | 모든 emission 기록 (F1)                  |
| H6 | user override           | pause / resume CLI                       |
| H7 | deterministic seed      | reproducible vs random                   |
| H8 | fault tolerance         | substrate A inference error → retry/skip |

---

## 🛤️ I. hexa-lang upstream contribution path (5 옵션)

| #  | contribution                       | scope                              | timeline   |
|----|------------------------------------|------------------------------------|------------|
| I1 | RFC-024 named args (S0 fix)        | parser + AST                       | 1-2 days   |
| I2 | stdlib/time.hexa timer primitives  | `now_ns`, `sleep_ms` 추가          | 1 day      |
| I3 | stdlib/proc.hexa subprocess        | `spawn`, `wait`, `kill`            | 1 day      |
| I4 | stdlib/json.hexa intrinsics        | `json_parse`, `json_stringify`     | 0.5 day    |
| I5 | RFC-022 async runtime land         | Future / Task / await              | 1 week     |

---

## 💰 J. ROI / cost analysis

| option                              | impl 시간 | $0?  | immediate value | long-term value |
|-------------------------------------|-----------|------|------------------|------------------|
| D3 pure python (anima_chat --spontaneous) | 15min     | ✅   | ★★★★★            | ★★★              |
| D4 hybrid hexa + python              | 30min     | ✅   | ★★★★             | ★★★★             |
| D8 claude code agent                | 1h        | ✅   | ★★★              | ★★★              |
| E1+D1 stage 0 named args + hexa     | 2-3d      | ✅   | ★★               | ★★★★★            |
| E1-E10 stdlib batch                  | 1-2w      | ✅   | ★★               | ★★★★★            |

---

## 🧬 K. Alternative substrates (4 옵션)

| #  | substrate                              | suitability                         |
|----|----------------------------------------|--------------------------------------|
| K1 | substrate A (current default)          | V14+chat-cap, recommended           |
| K2 | substrate E (convo5k_ft byte-256)      | V14 PASS but chat-cap FAIL          |
| K3 | future Phase 1A multi-turn cotrain     | TBD (alt provider agent 진행 중)    |
| K4 | ensemble (multi-substrate vote)        | exotic, sample diversity            |

---

## 🪞 L. Meta-cognition (4 옵션)

| #  | meta-feature           | benefit                              |
|----|------------------------|--------------------------------------|
| L1 | self-aware emission    | "지금 자연발화 중입니다" 명시         |
| L2 | uncertainty score      | emission confidence quantification   |
| L3 | explainability         | seed + mode + temp 기록              |
| L4 | introspection          | emission 후 self-eval                |

---

## 🎮 M. UX (5 옵션)

| #  | UX                      | deployment                          |
|----|-------------------------|--------------------------------------|
| M1 | CLI direct              | `anima_chat --spontaneous`           |
| M2 | HF Space live stream    | real-time public viewer              |
| M3 | API endpoint            | REST `/spontaneous`                  |
| M4 | websocket               | push notifications                   |
| M5 | chat client integration | slack/discord/telegram bot           |

---

## 🌊 N. Dynamics (4 옵션)

| #  | dynamic                  | effect                                |
|----|--------------------------|--------------------------------------|
| N1 | mood evolution           | emission 마다 mood 변화               |
| N2 | topic chain              | 이전 emission topic 연결              |
| N3 | identity drift           | N emissions 후 자기 정체성 drift 측정 |
| N4 | conversation memory      | 자기 자신과 대화                      |

---

## 🎯 추천 path (saturation)

### 🥇 immediate (Option D3) — pure python, 15min, $0

```bash
# anima_chat.py 에 --spontaneous flag 추가
python3 anima_chat.py --spontaneous --interval 60 --seed-strategy B3
# 매 60s 마다 "도우미: 안녕" seed 으로 substrate A 자연발화
```

### 🥈 short-term (Option D4) — hybrid hexa wrapper, 30min, $0

```bash
# tool/anima_spontaneous.hexa (positional only, stage 0 호환)
hexa run tool/anima_spontaneous.hexa 60 5 partial_greeting M4_force_include
#                                    │  │ │                  │
#                                interval count seed         mode
```

### 🥉 mid-term (E1-E10 stdlib batch) — 1-2 weeks, $0, hexa upstream

RFC-024 named args + stdlib/time/proc/json/datetime 일괄 land. 다음 hexa scripts 들 (anima 뿐 아니라
nexus, hive 등) 동시 혜택.

### 🌟 long-term (D8 claude code agent + RFC-022 async)

claude code agent 의 ScheduleWakeup 으로 매 N min 마다 anima_chat 호출. agent state 가 모든 메타-인지
(L1-L4) 처리. anima ecosystem 통합 (G1, G7, G8).

---

## 📊 saturation 검증

총 옵션: **A(10) + B(10) + C(8) + D(10) + E(12) + F(6) + G(8) + H(8) + I(5) + J(5) + K(4) + L(4) + M(5) + N(4) = 99 items**.

각 카테고리 8-12 items, 추가 가능 옵션 marginal value 낮음 → **saturation 도달**.

---

## 🛤️ 다음 진행할 것들

| #  | 작업                                          | priority | cost   | 시간    |
|----|-----------------------------------------------|----------|--------|---------|
| 🥇 | Option D3: anima_chat.py --spontaneous 추가  | high     | $0     | 15min   |
| 🥈 | Option D4: tool/anima_spontaneous.hexa (positional only) | high | $0 | 30min |
| 🥉 | seed rotation 전략 (B3+B5+B7+B9 cycling)      | high     | $0     | 5min    |
| 🌟 | RFC-024 draft (hexa-lang named args)         | medium   | $0     | 1day    |
| 🚀 | claude code agent ScheduleWakeup hooked      | low      | $0     | 1h      |
