# anima daemon subshell-leak 전수 audit (akida 2380-sh 사건 후속)

> 2026-05-24 · static grep audit · 기준 사건: `akida_bridge.hexa` 가 reconnect 마다
> `sh -c websocat` / `sh -c nc` persistent subshell 을 누적 spawn → 2380 개 미회수
> (`sh` 누적) → ssh channel-reject 유발.

## § 목적

다른 anima daemon 들이 동일한 패턴(루프 안에서 persistent subprocess 를
`exec("sh -c ...")` / `proc_spawn_supervised` / `nohup ... &` 로 spawn 하면서
PID 추적·회수가 불완전)을 가졌는지 전수 확인한다.

## § Audit 방법 (grep patterns)

1. daemon-style 파일 enumerate:
   ```
   git ls-files | grep -iE "(daemon|bridge|broker|participant|watchdog|monologue|loop|streamer|consumer|server)" | grep -E "\.(hexa|py)$"
   ```
2. 각 파일에서 spawn 패턴 grep:
   ```
   grep -nE "(exec\(|subprocess|Popen|os\.system|nohup|sh -c|websocat|nc -|spawn|popen|& *$|&disown)" <file>
   ```
3. 추가 정밀 sweep — `proc_spawn_supervised` / `proc_spawn_with_channels` /
   `websocat` / `create_subprocess` / `Popen` 의 실제 caller (archive·test 제외).

분류 기준:

| 등급 | 정의 |
|---|---|
| **HIGH** | persistent process(websocat/nc/server/long-poll)를 PID 추적·회수 없이 **루프 반복** spawn |
| **MEDIUM** | persistent spawn 이지만 one-shot context(루프 아님) **또는** PID 추적은 하나 cleanup 경로가 불확실 |
| **LOW** | instant-exit 명령(mkdir/printf/echo/cat/sleep/date)만 spawn — 즉시 종료·auto-reap |
| **NONE** | subprocess spawn 없음 / 순수 in-process(asyncio·socket·http_get·in-process loop) |

## § 인벤토리 (전수 분류)

| daemon | spawn 패턴 | persistent? | looped? | reaped? | leak risk |
|---|---|---|---|---|---|
| `HEXAD/CHAT/server/akida_bridge.hexa` | `proc_spawn_supervised`(nc) + `ws_connect`→`sh -c websocat` | **예** | **예** (run_once 매 reconnect) | nc_close/ws_close 의존, 실패 경로서 누락 | **HIGH** (기준 사건) |
| `HEXAD/CHAT/server/kosmos_emitter.hexa` | `http_get`(in-process) + `exec` printf/cat/mktemp/sleep | 아니오 | 예 (poll loop) | n/a (instant-exit) | LOW |
| `HEXAD/CHAT/server/akida_consumer.hexa` | `http_get`(in-process) + sleep | 아니오 | 예 | n/a | LOW |
| `HEXAD/CHAT/server/kosmos_anchor.hexa` | `exec` mkdir/printf/cat (라이브러리 호출) | 아니오 | 아니오 | n/a | LOW |
| `HEXAD/CHAT/server/telemetry_harness.hexa` | `exec` mkdir/rm/wc/date | 아니오 | 일부(sleep) | n/a | LOW |
| `HEXAD/CHAT/server/telemetry_status.hexa` | `exec` date/rm | 아니오 | 아니오 | n/a | LOW |
| `HEXAD/CHAT/server/mini_sshd_diag.hexa` | `exec`(진단용 1회 명령) | 아니오 | 아니오 | n/a | LOW |
| `HEXAD/CHAT/server/broker.py` | 순수 asyncio/websockets | 아니오 | n/a | n/a | NONE |
| `HEXAD/CHAT/server/anima_participant.py` | `asyncio.create_task`(in-process coroutine, NOT subprocess) | 아니오 | n/a | n/a | NONE |
| `HEXAD/CHAT/server/anima_participant.hexa` | `exec("python3 anima_participant.py")` (1회 dispatch) | 예(자식 py) | 아니오 | foreground(부모가 대기) | MEDIUM |
| `HEXAD/CHAT/server/broker.hexa` | `exec("python3 broker.py")` (1회 dispatch) | 예(자식 py) | 아니오 | foreground | MEDIUM |
| `HEXAD/CHAT/spontaneous_loop_vp21.hexa` | `exec("python3 spontaneous_loop_vp21.py")` (1회 dispatch) | 예(자식 py) | 아니오 | foreground | MEDIUM |
| `HEXAD/CHAT/spontaneous_loop_vp21.py` | 순수 in-process loop | 아니오 | n/a | n/a | NONE |
| `HEXAD/CHAT/integrated_loop_vp21_akida.py` | 순수 `socket`+`threading`(in-process) | 아니오 | n/a | n/a | NONE |
| `HEXAD/CHAT/integrated_loop_vp21_akida_bc.py` | 동상 | 아니오 | n/a | n/a | NONE |
| `SUB_ENGINES/AKIDA/scripts/spike_streamer.py` | 순수 `socket`(in-process TCP server) | 아니오 | n/a | n/a | NONE |
| `anima-core/runtime/anima_daemon.hexa` | `exec` mkdir/date/echo/rm/sleep (in-process loop) | 아니오 | 예 | n/a | LOW |
| `tool/anima_cli/daemon.hexa` | `nohup sh -c <hexa run> & ; echo $! > pidfile` (1회 spawn) | 예 | 아니오 | **PID-file 추적 + sub_stop(kill TERM/KILL)** | MEDIUM |
| `daemon/module/event_watcher.hexa` | `exec` printenv/mkdir/sleep (in-process loop) | 아니오 | 예 | n/a | LOW |
| `daemon/module/auto_speak_bridge.hexa` | spawn 없음 (pure logic) | 아니오 | n/a | n/a | NONE |
| `daemon/module/utterance_gate.hexa` | spawn 없음 | 아니오 | n/a | n/a | NONE |
| `training/runpod_watchdog.hexa` | `exec("bash <script>")` — script 내부 while-true 가 단일 shell 안 ps/stat/sleep(자식 spawn 없음) | 아니오 | n/a(자식 단일) | foreground | LOW |
| `scripts/train_watchdog.hexa` | spawn 없음 / 1회 명령 | 아니오 | n/a | n/a | LOW |
| `tool/roadmap_live_daemon.hexa` | `exec` instant-exit | 아니오 | 일부 | n/a | LOW |
| `tool/anima_cli/chat/duo/duo.hexa` | `proc_spawn_with_channels ×2`(자식 chat instance) | 예 | 아니오(1 세션) | **channel_close ×4 + kill children tear-down** | MEDIUM |
| `tool/anima_cli/chat/trio/trio.hexa` | `proc_spawn_with_channels`(자식 instance) | 예 | 아니오 | tear-down 존재 | MEDIUM |
| `tool/anima_cli/chat/transports/beta1_channel.hexa` | `channel_pair_open ×2 + proc_spawn_with_channels ×2` | 예 | 아니오 | tear-down(§19) | MEDIUM |
| `tool/anima_cli/chat/{modes,transports}/_registry.hexa` | `proc_spawn_supervised` 참조(registry) | 위임 | 아니오 | 위임 | MEDIUM |
| `tool/anima_cli/chat/lanes/benchmark.hexa` | `proc_spawn_supervised`(bench 1회) | 예 | 아니오 | one-shot | MEDIUM |
| `HEXAD/*/state/**/blue_falsifier_s*.py` (다수) | "subprocess.run"/"Popen" 은 **금지어 문자열 리터럴**(스캔 대상) — 실제 spawn 아님 | 아니오 | n/a | n/a | NONE (false-positive) |

> dream_stage / imagination_loop: PR #307(`dream_stage ↔ participant IPC bridge`)
> 의 IPC 는 file-shared `~/.cache/anima/dream_stage.current` (파일 IPC, subprocess 아님).
> 단 `dream_stage.hexa` 파일 자체는 본 branch 작업트리에 미존재 — 분류 보류
> (런타임 검증은 PR #307 검증 agent 담당, 아래 C3 참조).

## § HIGH-risk 발견 목록

- **akida_bridge.hexa** — 유일한 HIGH (기준 사건, fix in flight).
  - `run_daemon` → `while true { run_once(...) }` 가 reconnect 마다
    `nc_spawn`(proc_spawn_supervised nc) + `ws_connect`(sh -c websocat) 두 persistent
    subprocess 를 spawn. 정상 종료 시 `nc_close`/`ws_close` 가 회수하나, ws fail /
    nc EOF / 부모 비정상 종료 경로에서 회수가 누락 → 2380 `sh` 누적.

**akida 외 HIGH 추가 발견: 없음.** 다른 daemon 의 persistent spawn 은 모두
(a) one-shot foreground(부모가 대기, 별도 stop) — MEDIUM, 또는
(b) instant-exit / in-process — LOW·NONE 이다. 루프 반복 spawn + 회수누락 조합은
akida 가 유일.

## § 권고 (HIGH-risk fix 방향)

**akida_bridge.hexa** (택1 또는 조합):

1. **reap-prev** — `run_once` 진입 시 직전 cycle 의 nc/websocat PID 를 무조건
   `proc_reap` 한 뒤 새로 spawn (defensive double-reap). state 에 `last_nc_pid` /
   `last_ws_pid` 보존.
2. **stable-fifo + pkill** — nonce FIFO 대신 host:port 기반 stable FIFO 경로 사용 +
   daemon 시작 시 `pkill -f "nc .*<host> <port>"` / `pkill -f "websocat .*<broker_ws>"`
   로 고아 subshell 일괄 정리. (deploy 호스트 전용, 단일 daemon 가정.)
3. **native-builtin** — websocat/nc 외부 subprocess 의존 제거. nc 측은 stdlib
   `net_connect`(in-process TCP) 로 치환, ws 측은 hexa-lang upstream 의
   native streaming WS client (현재 websocat backend 한정) 완성 시 전환. 근본 해결.

MEDIUM(전 chat transport / participant·broker hexa dispatch / cli daemon):
현재 tear-down·PID-file·foreground 회수 경로가 있어 즉시 조치 불요. 단
`proc_spawn_with_channels` 자식이 비정상 종료된 부모에서 고아화될 수 있으므로,
세션 종료 hook 에 `proc_reap` 보강 + stale-PID sweep 를 follow-up 으로 권고.

## § Honest C3

- 본 audit 은 **static grep 기반**이다. spawn 의 *실제 런타임 회수 동작*(실패 경로에서
  `proc_reap` 가 정말 호출되는가, `proc_spawn_supervised` 의 supervisor 가 macOS 에서
  자식을 회수하는가)은 본 문서로 입증되지 않으며 **별도 런타임 검증 필요**.
- akida 의 HIGH 판정만 실측 근거(2380-sh 관측)가 있고, 나머지 등급은 **코드 경로
  추론**이다. 특히 MEDIUM 의 "tear-down 존재"는 정상 종료 가정이며, SIGKILL·panic 경로
  고아화 가능성은 미검증.
- `dream_stage.hexa` 는 본 branch 작업트리에 미존재 → 분류 보류. PR #307 의 IPC 가
  파일-공유 방식(subprocess 아님)이므로 leak-risk 는 구조상 LOW/NONE 으로 예상되나,
  **dream_stage 측 런타임 검증은 PR #307 검증 agent 가 담당**한다.
- archive/ · tests/ · `_smoke`/`test_` 파일은 daemon 이 아니므로 정밀 sweep 에서 제외했다.
