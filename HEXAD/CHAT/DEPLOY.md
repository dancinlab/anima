# CHAT 서버 production deploy runbook

> mini host (chat.dancinlab.org) 운영 절차. broker + participant 는 수동 nohup, cloudflared 만 LaunchAgent.
> mini sshd 가 간헐적 `request failed on channel 0` flapping — 작동 window 잡히면 즉시 deploy.

## production topology

| 컴포넌트 | 위치 | 실행 형태 |
|---|---|---|
| anima broker | `mini:~/anima_chat_pack/broker.py` | nohup (수동) |
| anima participant | `mini:~/anima_chat_pack/anima_participant.py` | nohup (수동) |
| cloudflared 터널 | `mini:~/Library/LaunchAgents/com.dancinlab.cloudflared.plist` | LaunchAgent (auto) |
| adapter pool | `mini:~/anima_chat_pack/{lora_adapter,kofl_adapter,jafl_adapter}/` | 정적 dir |
| venv | `mini:~/anima_chat_pack/venv/bin/python` | 공유 (broker + participant) |

## deploy 절차 (validated session-3, 2026-05-23)

### 1. 사전 점검 — mini ssh 작동 window 확인

```bash
ssh -o ConnectTimeout=5 mini 'echo OK'
```

- `OK` 출력 → window 열림, 진행
- `exec request failed on channel 0` → window 닫힘, 잠시 후 재시도 (intermittent flapping)

### 2. 파일 sync

```bash
cd <repo-root>
scp HEXAD/CHAT/server/anima_participant.py mini:~/anima_chat_pack/
scp HEXAD/CHAT/server/substrate_lora.py mini:~/anima_chat_pack/   # 변경 시
shasum -a 256 HEXAD/CHAT/server/anima_participant.py
ssh mini 'shasum -a 256 ~/anima_chat_pack/anima_participant.py'
# 두 sha 일치 확인
```

### 3. daemon 재기동 (broker + participant 둘 다)

```bash
ssh mini 'pkill -f anima_participant.py 2>/dev/null; pkill -f broker.py 2>/dev/null; sleep 2'

ssh mini 'cd ~/anima_chat_pack && PORT=8000 nohup ./venv/bin/python broker.py \
  </dev/null >> logs/broker.out 2>> logs/broker.err & echo "BROKER_PID=$!"'

ssh mini 'sleep 4; curl -s -m 4 http://127.0.0.1:8000/health'   # broker bind 확인

ssh mini 'cd ~/anima_chat_pack && nohup ./venv/bin/python anima_participant.py --threshold 0.30 \
  </dev/null >> logs/anima.out 2>> logs/anima.err & echo "PARTICIPANT_PID=$!"'
```

### 4. 검증 — health + logs (45s 대기 후)

```bash
sleep 45
curl -s https://chat.dancinlab.org/health
# 기대: {"ok":true,"anima_alive":true,...}

ssh mini 'tail -30 ~/anima_chat_pack/logs/anima.err | \
  grep -iE "LoraSubstrate ready|adapter|silent|EMIT|error|traceback" | tail -10'
# 기대: "LoraSubstrate ready: base=Qwen/Qwen2.5-1.5B adapters=['default','ja','ko'] ..."
# 기대 (users=0): "score=0.000<0.30 silent" (conversation-gate 작동)
```

### 5. 롤백 (deploy 실패 시)

```bash
cd <repo-root>
git checkout origin/main~1 -- HEXAD/CHAT/server/anima_participant.py    # 직전 main
scp HEXAD/CHAT/server/anima_participant.py mini:~/anima_chat_pack/
# 단계 3 재기동
```

또는 `lora_adapter_corpus_v5_bak/` 같은 mini-side 백업 rename 으로 adapter 롤백.

## 알려진 제약

- **mini sshd flapping** = intermittent. 진단 도구 = `HEXAD/CHAT/server/mini_sshd_diag.hexa` (사용자 mini 콘솔에서 실행)
- **mini reboot 시 broker/participant 미기동** — 사용자 수동 재기동 필요 (user directive: plist 금지 + nohup 마이그레이션)
- **broker + participant 같은 venv 공유** — Python 패키지 충돌 주의
- **deploy 중 production 짧은 down (~5-10s)** — broker 재기동 사이 502

## 환경변수 (옵션)

| env | default | 용도 |
|---|---|---|
| `ANIMA_THRESHOLD` | 0.45 | emit threshold (prod 권장 0.30) |
| `ANIMA_BASE` | Qwen/Qwen2.5-1.5B | base model |
| `ANIMA_ADAPTER` | `~/anima_chat_pack/lora_adapter` | default adapter |
| `ANIMA_ADAPTER_KO` / `_JA` / `_ZH` / `_RU` | `~/anima_chat_pack/{ko,ja,zh,ru}fl_adapter` | 언어별 hot-swap (absent → graceful skip) |

## 관련 도구

| 파일 | 용도 |
|---|---|
| `HEXAD/CHAT/server/anima_live_register_measure.hexa` | LIVE register/EN-share 측정 |
| `HEXAD/CHAT/server/anima_monologue_sim.hexa` | monologue vs responsive 측정 (사용자 #1 목표 검증) |
| `HEXAD/CHAT/server/mini_sshd_diag.hexa` | sshd flapping 진단 (mini 콘솔) |
| `HEXAD/CHAT/server/telemetry_status.hexa` | Phase 2 gate observability |
