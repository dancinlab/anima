# PR #307 IPC bridge exec-pattern leak 검증 (akida 2380-sh 사건 후속)

> 결론: **SAFE** — `_ds_publish_stage`의 `exec("mkdir")`/`exec("printf")`는
> 동기(blocking)·자동 reap 패턴이라 akida 같은 subshell 누수를 만들지 않는다.
> #307 머지 OK.

## PR #307 의 exec 패턴 (mkdir + printf per tick)

`HEXAD/CHAT/server/anima_dream_stage.hexa` §6b 가 추가한 IPC bridge:

```hexa
fn _ds_publish_stage(stage: string) -> string {
    let _mk = exec("mkdir -p \"$HOME/.cache/anima\"")
    let _w  = exec("printf '%s\\n' \"" + stage + "\" > \"$HOME/.cache/anima/dream_stage.current\"")
    return DREAM_STAGE_FILE
}
```

호출 빈도: `run_daemon`의 매 tick (기본 60s) — `st = dream_tick(...)` 직후
무조건 호출. 하루 1440 tick × 2 exec = **2880 exec/day**. 우려: 각 exec 가
reap 되지 않으면 akida (2380 orphaned sh) 와 동형의 누수가 된다.

## akida leak 과의 비교

| | akida_bridge | dream_stage IPC |
|---|---|---|
| spawned cmd | `nc`/websocat (persistent, 연결 유지 목적) | `mkdir`/`printf` (즉시 종료) |
| 생존 시간 | 장기 (연결 동안 계속) | 수 ms |
| spawn 방식 | 백그라운드 subprocess (`h["pid"]` 추적) | `exec()` 동기 호출 |
| reaped? | **NO** — reconnect 가 `proc_reap(pid)` 건너뜀 (누적) | **YES** — `hxlcl_pclose`/`hexa_spawn_reap`가 `waitpid` |
| leak risk | **HIGH (확인됨, 2380 sh)** | **NONE (SAFE)** |

핵심 차이: akida 는 *오래 사는 백그라운드 프로세스를 abandon* 했다
(`nc_close`의 `proc_reap`이 reconnect 경로에서 누락 → 누적). dream_stage 는
*즉시 종료하는 명령을 동기적으로 wait* 한다.

## hexa exec() semantics (sync, 자동 reap)

출처: `hexa-lang/self/runtime_core.c:5151 hexa_exec()` + `self/runtime.c:1780
hxlcl_popen/hxlcl_pclose`.

- `hexa_exec`은 자식 stdout 을 **EOF 까지 `fread`** 한다 (5174-5180) —
  자식이 종료해 pipe 를 닫을 때까지 부모가 **블록**한다 (동기).
- drain 후 reap:
  - posix_spawn 경로 → `hexa_spawn_reap(spawn_pid)` (5182)
  - popen 경로 → `hxlcl_pclose(fp)` (5183) →
    `hxlcl_waitpid(pid, &status, 0)` (runtime.c:1815) — **명시적 waitpid**.

즉 `exec()`는 fork+exec+**WAIT** (옵션 a). 좀비/고아가 남지 않는다.
보강 증거: 코드베이스 전반이 `exec(...).trim()` 으로 **반환 stdout 을 소비**하고
`exec("sleep 60")` 으로 **데몬 페이싱**까지 exec 에 의존한다 — 둘 다 동기
blocking 이어야만 성립한다 (inbox `exec-with-status-3tuple-migration.md`도
pipe/fork/select drain + exit_code 회수를 문서화 = wait 필수).

## 경험적 검증 (mini, dream_stage daemon PID 35931)

```
$ ssh mini 'ps -p 35931 -o pid,ppid,etime,command; pgrep -P 35931 | wc -l'
PID   PPID  ELAPSED   COMMAND
35931    1  01:09:30  .hexa-cache/bin-...225a5ae3 daemon
children: 1     # in-flight `exec("sleep 60")` 1개뿐 (스냅샷 순간)
```

데몬은 **1h09m (~69 tick)** 가동 중. 누수라면 69 tick × 2 exec ≈ 138+ orphaned
`sh` 가 쌓여야 하지만 자식은 **1개** (현재 페이싱용 `sleep 60`)뿐이고, mini 전체
`sh` 는 3개 (무관). akida 2380 과 정반대 — exec 가 정상 reap 됨을 실측 확인.

## Verdict: **SAFE**

`exec()` = 동기 fork+exec+waitpid. mkdir/printf 는 ms 단위 종료 후 즉시 reap.
2880 exec/day 도 누적 0. akida 누수는 *persistent 백그라운드 프로세스의
reap 누락*이 원인이며 dream_stage 의 *즉시-종료 동기 exec* 와 동형이 아니다.

## 권고

- **#307 머지 OK** — leak 위험 없음. 차단 사유 아님.
- (선택, 비차단) hexa-native 파일쓰기 builtin (`write_file` 류)이 있다면
  `exec("printf ... > file")` 대신 그것으로 교체하면 tick 당 subshell 2개를
  0개로 줄여 더 깔끔하다 (성능·정합성 미세 개선, 누수와는 무관). 현재
  intrinsics 에 직접 대응 builtin 부재 시 exec 패턴 유지 안전.
- akida 측 실제 수정(reconnect 경로 `proc_reap` 보강)은 본 검증 범위 밖
  — 별도 PR 로 처리.
