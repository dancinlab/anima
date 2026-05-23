# broker `/ws/akida_ingest` → `/akida/recent` deque gap (inbox patch)

> **kind**: inbox-patch · coordination doc · doc-only (no source mutation from anima repo)
> **date**: 2026-05-23
> **source**: anima cycle 10 / EA `akida_bridge` daemon RESTORE verification
> **severity**: blocks AKIDA-first natural speech chain end-to-end (bridge 복구 완료, broker 측에서 spike 가 surface 되지 않음)
> **target**: `anima_chat_pack/broker.*` 의 `/ws/akida_ingest` WS 핸들러 (mini PID 1691)

---

## §1 — Observation (관측 사실)

`akida_bridge.bin daemon` 을 mini (`PID 2350`) 에서 재기동한 직후, websocat WS handshake 는 깨끗하게 통과했고 broker (`mini PID 1691`) 측 anima 로그도 ingest WS 수락을 명시했다.

- broker 측 로그: `WebSocket /ws/akida_ingest accepted` · `akida ingest connected`
- bridge 측 카운터: 지속 상승 중 (마지막 관측: `forwarded 1400 spikes`)
- 그러나 `GET http://localhost:8000/akida/recent` 은 **연속 약 2 분간** `{"akida":[]}` 만 반환

즉 transport (WS handshake + frame forwarding) 는 살아있지만, broker 의 ingest 핸들러가 받은 frame 을 `/akida/recent` 가 읽는 deque 로 **흘려보내지 못하고 있다**.

MEMORY 사전 경고가 그대로 적중한 사례 — `"akida ingest endpoint = /ws/akida_ingest (NOT /ws/akida — 후자는 subscriber, 핸들러 동작 확인 필수)"`. 본 inbox entry 는 그 경고를 **측정된 FAIL** 로 승격한다.

## §2 — Hypothesis (가능 원인 4 후보)

핸들러 코드를 직접 보지 않은 상태에서, 관측만으로 좁힌 4 후보:

- **(a) stub / no-op 핸들러** — frame 을 받기만 하고 silently 소비. accept 로그만 찍히고 deque write 자체가 없는 형태.
- **(b) deque 불일치** — 핸들러는 어떤 deque/state 에 append 하지만, `/akida/recent` 가 읽는 deque 는 다른 인스턴스. 두 코드 경로가 서로 다른 모듈-레벨 객체를 들고 있을 가능성.
- **(c) JSON parse 실패 silent swallow** — 들어온 text frame 이 broker 측 expected schema 와 어긋나서 `try/except` 가 전부 삼키는 형태. error 로그가 보이지 않는 점이 이와 일치.
- **(d) deque 용량 / eviction 버그** — `maxlen=0` 으로 초기화되었거나 eviction 로직이 매번 비우는 형태. append 직후 즉시 소실.

(a)–(d) 중 어느 것이든 broker 핸들러 코드 한 군데를 들여다보면 30 초 안에 가려진다.

## §3 — Repro (재현 절차 4-step)

1. mini broker 가 `:8000` 에서 실행 중인지 확인 — anima.err 에 `akida ingest connected` 라인이 보이면 OK.
2. bridge daemon 재기동 (PATH workaround 포함, §5 side-finding 참고):
   ```sh
   ssh mini "export PATH=/opt/homebrew/bin:\$PATH && cd ~/anima_chat_pack && \
     nohup ./akida_bridge.bin daemon \
       > logs/akida_bridge.out 2> logs/akida_bridge.err < /dev/null & disown"
   ```
3. 30 초 대기 (bridge 측 `forwarded N spikes` 카운터가 충분히 상승할 시간).
4. `/akida/recent` 폴링:
   ```sh
   ssh mini -- 'curl -s http://localhost:8000/akida/recent'
   # → {"akida":[]}
   ```

기대값은 최근 spike 객체 N 개. 실제 관측은 빈 배열 — 약 2 분간 일관되게 비어 있음.

## §4 — Suggested fix (제안 수정)

broker repo (`anima_chat_pack/broker.*`) 안에서 `/ws/akida_ingest` 핸들러를 찾아 다음 3 가지를 동시에 충족시킬 것:

1. 들어온 WS **text frame 을 JSON 으로 파싱**한다 (parse 실패 시 silent swallow 가 아니라 최소한 카운터 + 로그 1 줄 — 가설 (c) 차단).
2. 파싱된 객체 `{"ts": ..., "spike_ids": [...], "regime": "..."}` 를 `/akida/recent` 가 읽는 **동일한 `deque` 인스턴스** 에 `append` 한다 (모듈-레벨 singleton 또는 명시적 DI — 가설 (b) 차단).
3. 해당 `deque` 의 `maxlen` 이 **0 이 아닌 합리적 값** (예: 1024) 으로 초기화되어 있고, eviction 이 정상 (가설 (d) 차단).

cross-check 용으로 pi5 `spike_streamer` 가 실제로 흘려보내는 JSON line 한 줄 예시 (handshake 직후 캡쳐):

```
{"t_rel": 20511.83, "step": 204741, "n_spikes": 8,
 "spike_ids": [...], "regime": "R3_tonic_zero_input", "thr": [...]}
```

broker 의 expected schema 가 이와 일치하는지 (특히 key 명, optional vs required) 1차로 비교할 것.

## §5 — Side findings (부수 관측 2)

### (a) websocat PATH — mini non-interactive ssh 환경 누락

mini 의 non-interactive ssh PATH 는 `/opt/homebrew/bin` 을 포함하지 않는다. 그 결과 `akida_bridge.bin daemon` 이 기동 직후 `which websocat` 에서 FATAL 로 exit 한다.

- **임시 우회**: nohup 직전에 `export PATH=/opt/homebrew/bin:$PATH` 강제 주입 (§3 step 2 명령 안에 포함).
- **영구 수정 후보**: `akida_bridge.hexa` 안에서 `which websocat` 으로 떨어지기 전에 `/opt/homebrew/bin/websocat` 과 `/usr/local/bin/websocat` 를 먼저 probe 한 뒤 fallback 으로 `$PATH` 검색. mini / Linux pool 양쪽 모두를 cover.

### (b) `nc` connection state — FIN_WAIT_2 잔존

bridge 카운터가 상승 중인 동안에도 `netstat -an | grep 192.168.50.155.9512` 는 `FIN_WAIT_2` 만 보인다. 이는 pi5 close 이후 FIFO 에 버퍼된 데이터를 bridge 가 계속 소비 중인 형태로 해석된다 (pi5 자체는 수동 `nc -w 2` 로 여전히 streaming 중임이 확인됨).

본 항목은 broker gap (§1) 과는 **독립된 관측**이며, ingest 흐름 자체를 막지는 않는다. 별도 단서로 기록만 남긴다.

## §6 — Verdict (현 시점 판정)

- **bridge daemon**: RESTORED + ALIVE (mini PID 2350, websocat handshake clean, `forwarded 1400 spikes` 상승 중).
- **end-to-end ingest visible at `/akida/recent`**: **FAIL** — broker 측 `/ws/akida_ingest` 핸들러 gap (§2 (a)/(b)/(c)/(d) 중 1 개 이상).

bridge 복구는 완료된 것으로 close 하고, 다음 마일스톤은 broker 측 핸들러 audit 한 사이클이다.
