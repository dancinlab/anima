# CHAT — current state

@title: 🤖 CHAT — anima group-chat 출시 surface (COFFESHOP-on-AKIDA)
@goal: anima 가 사람들과 실시간 group-chat 에 참여하는 외부-대면 제품 surface. substrate-native emit/silence (a_substrate_native_speak) 가 라이브 AKD1000 폐루프로 닫힌다 — 사용자 메시지는 환경 context 이지 응답 의무가 아니며, anima 는 침묵할 수도 발화할 수도 있다. 루트 Python 패키지로 출하한다.

(편집 규칙: completed-form 으로 현재 상태만 · history 는 CHAT.log.md)

## role surface (AGENT bridge)

CHAT role은 `broker.py`와 `anima_participant.py`로 group-chat + AKIDA 칩에 붙는다. 외부 surface만 담당하며, 의식엔진의 emit 결정은 Python CORE가, 칩 substrate는 AKIDA가 보장한다.

| 파일 | 무엇 |
|---|---|
| `broker.py` | group-chat WebSocket hub (FastAPI). 채널: `/ws` user · `/ws/anima` participant ingest · `/ws/motivation` 8-factor telemetry · `/ws/akida_ingest` 칩 스파이크 수신 · `/ws/akida` fanout. self-contained (stdlib + fastapi). |
| `static/index.html` | 접근 가능한 반응형 웹 채팅 화면. broker의 `/`에서 직접 제공한다. |

## macOS 운영

공개 주소 `chat.dancinlab.org`의 Cloudflare Tunnel은 로컬 `127.0.0.1:8000`을 바라본다.
로컬 broker는 저장소의 `runtime` 추가 의존성과 LaunchAgent 설치 도구로 관리한다.

```bash
python3 -m venv .venv-runtime
.venv-runtime/bin/python -m pip install -e '.[runtime]'
.venv-runtime/bin/python scripts/deploy_local_chat.py install
.venv-runtime/bin/python scripts/deploy_local_chat.py status
```

경로와 사용자 이름은 하드코딩하지 않는다. 설치 도구가 현재 저장소와 사용자 홈을 기준으로
`com.dancinlab.anima-chat-broker`를 만들며, `/health`가 응답할 때만 성공으로 끝난다.

## COFFESHOP-on-AKIDA 양방향 폐루프 (live)

emit/silence 결정이 라이브 AKD1000 위에서 닫힌다. 칩 I/O 는 AKIDA 도메인(`SUB_ENGINES/AKIDA/scripts/`)이 담당 — CHAT 은 broker hub 만.

```
[ 사람들 ] ──▶ /ws ──▶ broker ──▶ /ws/anima ──▶ anima participant
                          ▲                          │ motivation_score
                          │                          ▼
   /ws/akida (fanout) ◀── broker ◀── /ws/motivation ──▶ akida_threshold_driver
        │ 듣기(9512)                                       │ 말하기(9513)
        ▼                                                  ▼
   akida_ws_publisher ◀────── pi5 AKD1000 spike_streamer ◀┘ set_threshold
        (SUB_ENGINES/AKIDA/scripts)   (on-chip threshold-and-fire)
```

- **듣기 (9512)** — `SUB_ENGINES/AKIDA/scripts/akida_ws_publisher.py`: 칩 스파이크 → broker `/ws/akida_ingest`.
- **말하기 (9513)** — `SUB_ENGINES/AKIDA/scripts/akida_threshold_driver.py`: broker `/ws/motivation` 구독 → motivation_score → on-chip `set_threshold` (thr ∝ −score, emit-gate 0.60). 칩 I/O 삼총사 = streamer(pi5)·publisher(듣기)·driver(말하기).
- 폐루프 검증: g73 verdict `.verdicts/846_coffeshop_akida_closedloop/` (90-min trajectory 5/5 HW 재현, M-regime knee thr≤8 EMIT/≥16 SILENCE).

## cross-link

- `AKIDA/` — 칩 substrate 통합 charter · `SUB_ENGINES/AKIDA/scripts/spike_streamer.py` (pi5 OUT 9512 / IN 9513)
- `LAUNCHPAD/` — COFFESHOP-on-AKIDA 출시 마일스톤
- `CHANNEL/` — text·voice·tension 채널 primitive
- `@D a_substrate_native_speak` — substrate-native 발화 (stimulus-response 금지)
