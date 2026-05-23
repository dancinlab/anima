# akida_bridge subshell-leak 사건 postmortem 2026-05-24

_incident record · 2026-05-24 · resolved (정리 완료 + 근본수정 in flight)_

`mini` 호스트에서 발생한 `ssh ... exec request failed on channel 0` 간헐 장애의 근본 원인을 진단·해소한 production 사건 기록.

## §1 — Timeline (incident → diagnosis → fix)

- **증상 발현**: `ssh mini '<cmd>'` 가 간헐적으로 `exec request failed on channel 0` 으로 실패 (pool dispatch 도 동일하게 영향). cycle 7/BD `MINI_SSHD_DIAGNOSIS` 부터 관측되었으나 당시 verdict 는 **INCONCLUSIVE / all config clean** — 재현 안 됨으로 종결.
- **재진단 (2026-05-24)**: `ps -u mini` 가 **2380 sh** 프로세스를 노출. parent-PID trace 결과 대부분 `ppid=1` 고아였고, command 가 `sh -c websocat ws://localhost:8000/ws/akida_ingest` 형태 — `akida_bridge.bin daemon` (PID 2350) 가 spawn 한 subshell 임이 확정.
- **정리**: `akida_bridge` daemon (PID 2350) 정지 → `pkill -f` 로 websocat/nc/sh-wrapper 고아 reap → `rm /tmp/hexa_ws_* /tmp/hexa_akida_nc_*` fifo cleanup. 누수 subshell **2380 → 0**, uid proc 슬롯 **2616 → 237** 회복, ssh 안정화. `participant`(35411) · `broker`(1691) · `dream_stage`(35931) daemon 은 보존.

## §2 — Root cause (verbatim diagnostic)

```
kern.maxprocperuid: 2666 / procs-by-uid-mini: 2616
2380 sh (uid mini, mostly ppid=1)
sh -c websocat ws://localhost:8000/ws/akida_ingest < fifo > fifo
sh -c nc -w 600 192.168.50.155 9512 > fifo
```

`akida_bridge.bin daemon` (PID 2350) 이 수 시간에 걸쳐 2380 개의 `sh -c websocat/nc` subshell 을 누수. uid `mini` 의 프로세스 수가 2616 으로 `kern.maxprocperuid` 한도(2666)에 근접 — 가용 슬롯이 50 개 미만으로 고갈.

## §3 — 메커니즘

reconnect 가 일어날 때마다 persistent websocat/nc subshell 을 새로 spawn 하고 reap 하지 않음 → 부모(akida_bridge)가 wait 하지 않아 `ppid=1` 고아로 누적 → uid 프로세스 슬롯 점진 고갈 → 새 ssh fork 가 per-uid 한도에 막혀 `channel 0` reject.

## §4 — 왜 간헐적이었나?

이미 떠 있는 daemon (`participant` · `broker` · `dream_stage`)은 fork 를 안 하므로 멀쩡히 계속 동작. 슬롯이 거의 다 찬 상태에서 **새로 들어오는 ssh burst 만** fork 에 실패. 따라서 "어떤 명령은 되고 어떤 명령은 안 되는" 간헐 증상으로 관측됨 — 슬롯 여유에 따라 비결정론적.

## §5 — 왜 cycle 7/BD 가 놓쳤나?

당시 진단(`MINI_SSHD_DIAGNOSIS`)은 **config-only** 검사였음 — `maxsessions` / `maxstartups` / `sshd_config` / `authorized_keys` / `launchd` 모두 정상 (CLEAN). 그러나 **proc-count 를 검사하지 않음** → 리소스 고갈은 config 검사로 보이지 않아 INCONCLUSIVE 로 종결됨. config 가 깨끗해도 리소스가 깨끗하다는 보장은 아님.

## §6 — Fix

1. **즉시 정리 완료 (이 세션)**: daemon 정지 + 고아 reap + fifo cleanup → 2380 → 0, 슬롯 2616 → 237.
2. **근본 수정 (in flight)**: `akida_bridge.hexa` source leak-fix — branch `fix/akida-bridge-subshell-leak` (persistent subprocess 의 reap / 단일 long-lived connection 재사용).
3. **pool host-health guard (in flight)**: `pool#2` inbox — dispatch 전 host proc-count health probe.
4. **daemon 전수 audit (in flight)**: 모든 daemon 의 subshell-leak 여부 audit.

## §7 — Lessons

1. **proc-count 도 health 지표다** — config-clean 진단만으로는 리소스 고갈을 못 잡는다. `ps -u <uid>` count 를 health 검사에 포함.
2. **persistent subprocess 는 반드시 reap 한다** — spawn 후 wait 하지 않으면 `ppid=1` 고아로 누적, uid 슬롯을 고갈시킨다.
3. **config-clean ≠ resource-clean** — 설정이 정상이어도 누적 리소스 누수는 별도 축. 두 축을 분리해서 진단.

## §8 — Cross-reference

- `pool#2` inbox — pool host-health guard (dispatch 전 proc-count probe)
- PR #203 — broker akida deque handler gap
- `MINI_SSHD_DIAGNOSIS.md` (cycle 7/BD) — config-only INCONCLUSIVE verdict, 본 postmortem 이 supersede
- branch `fix/akida-bridge-subshell-leak` — 근본 수정 (in flight)
