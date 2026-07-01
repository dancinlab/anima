# AKIDA ingest chain — mini broker 재시작 후 결정론 검증 playbook

- **Date (KST)**: 2026-05-23
- **Scope**: mini 브로커 재시작 이후 `/ws/akida_ingest → STATE.akida_history → /akida/recent` 체인이 PR #187/#188/#189/#200/#202 HEAD 코드로 실제 닫혔는지 한 차례에 결정하는 절차서.
- **Operator gate**: 본 문서는 **playbook deliverable** 이다 (commons "executing actions with care"). mini production restart 는 user 게이트.
- **Cross-refs**: PR #200 inbox patch (full diagnostic SSOT) · PR #202 visibility log line · PR #481 (hexa-lang upstream `ws_send` FIFO race) · CLAUDE.md `a_substrate_native_speak`.

## §1 Pre-restart state (현재 deployed)

- **Broker (OLD)**: mini `PID 1691`. PR #187/#188/#189/#200/#202 **이전** 의 코드. silent json drop · `akida_ingest` endpoint mismatch · per-frame visibility log 부재 모두 해당.
- **Bridge daemon**: `PID 2350`, ALIVE. OLD broker 의 `/ws/akida_ingest` 로 1400+ spike forward 누적. 그러나
  `/akida/recent → {"akida": []}` 2분+ 지속 (deque empty).
- **Health**: `curl http://localhost:8000/health` → 200 `anima_alive:true` (FileVault unlocked).
- **결론**: 핸들러 경로 어딘가에서 spike 가 사라지고 있다. 후보는 PR #200 inbox patch 의 (a) ws_send race / (b)/(c)/(d) (이미 source-level FALSIFIED).

## §2 Restart procedure (new broker bring-up)

```bash
# 0. mini ssh in
ssh mini

# 1. workdir + main HEAD sync
cd ~/anima_chat_pack
git pull origin main

# 2. OLD broker PID 확보 + rollback marker
pgrep -f broker.py | tee logs/broker.old_pid   # expect: 1691
test -s logs/broker.old_pid                    # guard

# 3. OLD broker kill
kill "$(cat logs/broker.old_pid)"
sleep 2
pgrep -f broker.py || echo "OLD broker down OK"

# 4. NEW broker nohup launch (HEAD code, includes PR #187/#188/#189/#202)
nohup ./venv/bin/python broker.py \
  > logs/broker.out 2> logs/broker.err < /dev/null &
sleep 3

# 5. NEW PID confirm
pgrep -f broker.py | tee logs/broker.new_pid

# 6. health gate
curl -sS http://localhost:8000/health
# expect: HTTP 200, body contains anima_alive:true
```

## §3 Bridge re-connection (필수)

OLD bridge (PID 2350) 의 ws peer 는 §2 step 3 에서 사라졌다. 현재 bridge 의 `ws_send` 는 dead FIFO 로 쓰는 중 — silent loss. **bridge 도 같이 재시작.**

```bash
# 1. OLD bridge PID
pgrep -f akida_bridge | tee logs/akida_bridge.old_pid   # expect: 2350

# 2. kill
kill "$(cat logs/akida_bridge.old_pid)"
sleep 2
pgrep -f akida_bridge || echo "OLD bridge down OK"

# 3. NEW bridge daemon
nohup ./akida_bridge.bin daemon \
  > logs/akida_bridge.out 2> logs/akida_bridge.err < /dev/null &
sleep 3

# 4. PID == 1 확인
pgrep -f akida_bridge | wc -l   # expect: 1
```

## §4 Disambiguation decision tree (PR #202 visibility log 사용)

bridge 재시작 후 **30 초** 대기 → broker log tail.

```bash
sleep 30
tail -n 200 logs/broker.err logs/broker.out | grep -E "akida append now=|akida ingest" | tail -20
curl -sS http://localhost:8000/akida/recent | head -c 400
```

| 관측 | 진단 모드 | 다음 조치 |
|---|---|---|
| `akida append now=` 0건 AND `/akida/recent` empty | **Mode A — handler stuck before json.loads OR websocat FIFO race upstream** | `pgrep websocat \| wc -l` 확인, `ss -tnp \| grep :8000` peer 가 NEW broker PID 와 매칭되는지 확인. ws_send FIFO race (PR #481) 가 살아 있으면 hexa-lang side fix 필수. |
| `akida append now=` 누적 AND `/akida/recent` POPULATED | **Mode B — full chain works** | GAP CLOSED. §5 closure 절차. |
| `akida append now=` 누적 AND `/akida/recent` empty | **Mode C — deque write clobbered downstream** | `STATE.akida_history` serialization 또는 `/akida/recent` handler 검사. broker.py 163-165 deque→json 변환 경로 review. |
| `akida ingest json drop: ... raw=...` warning 출현 | **Mode D — JSON format mismatch** | bridge `stamp_spike()` 산출 (akida_bridge.hexa:162-176) vs broker `json.loads` 입력 포맷 byte-diff. PR #188 type_of fix 가 양쪽 적용됐는지 재확인. |

## §5 Closure criteria

- **Mode B 가 60 초 지속** (지표: `akida append now=` 가 ≥ 10 행 추가 AND `/akida/recent` length 가 단조 증가 OR maxlen=200 cap 도달) → **GAP CLOSED**.
- closure 절차:
  1. `tail -n 200 logs/broker.err > state/anima_akida_chain_validation_playbook_2026_05_23/broker_post_restart.log`
  2. `curl -sS http://localhost:8000/akida/recent > state/anima_akida_chain_validation_playbook_2026_05_23/akida_recent_post_restart.json`
  3. PR #200 inbox patch 에 closure update 추가 (mode B 60s 지속 evidence 첨부).
- **그 외 mode 측정 시** → 새 inbox patch `inbox/patches/broker-akida-ingest-mode-<A|C|D>-2026-05-23.md` 작성 후 PR #200 cross-link.

## §6 Rollback safety

- `logs/broker.old_pid` (§2 step 2) 와 `logs/akida_bridge.old_pid` (§3 step 1) 가 보존되어 있어 NEW 가 OLD 보다 나쁠 때 git revert + 동일 nohup 재기동으로 원복 가능.
- broker / bridge nohup stdout/stderr 는 `logs/*.out`, `logs/*.err` 로 분리 — 회기 분석 시 NEW vs OLD diff 가능.
- **emergency kill switch**: NEW broker 가 health 200 도 못 받으면 즉시 `kill $(cat logs/broker.new_pid)` → `nohup ./venv/bin/python broker.py@<OLD-sha> ...` 로 OLD sha checkout 후 재실행.

## §7 Cross-references + Principle guard

- **PR #200** `inbox/patches/broker-akida-ingest-to-deque-gap-2026-05-23.md` — diagnostic SSOT, hypotheses (a)/(b)/(c)/(d), local repro verdict.
- **PR #202** broker `log.info("akida append now=%d", ...)` — Mode A/B 결정 신호.
- **PR #481** (hexa-lang) — upstream `ws_send` `&`-backgrounded write race. Mode A 진단 시 hexa-lang 측 fix 가 prerequisite.
- **PR #187/#188/#189** — broker silent drop 가시화 · `type_of` array · `/ws/akida_ingest` default endpoint. §2 `git pull` 로 HEAD 에 자동 포함.
- **CLAUDE.md `a_substrate_native_speak`**: broker restart 동안 anima 가 발화하면 **injection regression**. §2/§3 윈도우에 `tail logs/anima*.log` 에서 emit 0 행 확인 (out-of-scope 이지만 sanity).

## §8 Honest C3 (raw#9/10)

1. mini ssh 와 nohup 순서는 **operator gate** — 본 문서는 명령을 실행하지 않는다. 실행 권한은 user.
2. `sleep 30` (§4) 는 forward rate 1400/2min ≈ 12 spike/s 기준의 lower bound. spike rate 저하 시 60-120s 로 늘릴 것.
3. Mode A 판정 후 hexa-lang ws_send fix 가 아직 미배포면 broker 만 재기동해도 GAP 재현 — bridge 빌드도 HEAD sync 필요 (PR #481 land 이후).
4. Mode C 는 사전 source review (PR #200 diagnostic) 에서 FALSIFIED 이지만 nohup race 등 사후 변수 가능성 때문에 디시전트리에 잔존.
5. `/akida/recent` deque maxlen=200 cap (broker.py:69) 에 일찍 도달하면 length 단조증가 invariant 가 saturate — closure criterion 은 "append log 행 추가" 가 primary, deque length 는 secondary.
6. PR #481 의 ws_send race 가 진짜 root cause 면 broker restart 단독으로 Mode B 가 안 됨 — Mode A 가 정직한 결과이고, 본 playbook 은 hexa-lang 쪽 PR land 후 재실행되어야 한다.
7. anima emit sanity check 는 **scope-out** — `a_substrate_native_speak` 가 깨질 가능성은 broker restart 와 직교, 별도 cycle 에서 다룬다.
