# FIRST-PACK deploy status — 2026-05-22 진행 보고

> mini (Mac M-series) 위 anima 단체 채팅방 deploy 진행 상황. Phase 3/4/5 LANDED,
> Phase 6 cloudflared interactive login 단계, Phase 7/8 pending.

## Phase 상태

| Phase | 항목 | 상태 | 위치 |
|---|---|---|---|
| **3** | chat broker (FastAPI + WebSocket) | ✅ **LIVE** PID 2325, port 8000 LISTEN | mini `~/anima_chat_pack/broker.py` |
| **5** | anima participant (substrate-native) | ✅ **LIVE** PID 2391, --threshold 0.30 | mini `~/anima_chat_pack/anima_participant.py` |
| **4** | frontend 3-pane HTML | ✅ **DEPLOYED** 15.9 KB, served by broker `/` | mini `~/anima_chat_pack/static/index.html` |
| **6** | cloudflared tunnel → chat.dancinlab.org | 🔄 **binary installed** (`~/bin/cloudflared 2026.5.0`), **interactive login pending** | mini |
| **7** | AKIDA viz tab (Pi spike forward) | ⏳ Phase 4 에 placeholder canvas 존재, 실 spike feed 미연결 | — |
| **8** | spontaneous feed sidebar | ✅ **partial** (8-factor real-time gauge 작동) — recent emit list 도 작동 | static/ |

## 검증 (curl + ws 직접 test)

```
$ curl -s http://mini.local:8000/health | head -c 200
{"ok":true,"anima_alive":true,"users":0,"history_len":50,"langdetect":true}

$ curl -s http://mini.local:8000/motivation/recent | python3 -c "import json,sys;r=json.load(sys.stdin);print('history',len(r['motivation']))"
history 81

$ curl -s http://mini.local:8000/ | head -3
<!DOCTYPE html>
<html lang="en">
<head>
```

anima_participant 가 매 ~2s tick 마다 motivation_score 계산 + history 적재 중 (81 entries 그대로 evolution). substrate-native — user 발언 0 인데도 anima 자기 dynamics 로 motivation 진화 (`@D a_substrate_native_speak` 정합).

## broker WebSocket 프로토콜

| endpoint | direction | payload |
|---|---|---|
| `GET /` | browser → broker | serves static/index.html |
| `GET /health` | browser → broker | {ok, anima_alive, users, history_len, langdetect} |
| `GET /motivation/recent` | browser → broker | {motivation: [{ts, score, threshold, factors:{relevance,info_gap,curiosity,pain,coherence,originality,balance,dynamics}}]} |
| `GET /participants` | browser → broker | participants list |
| `GET /history` | browser → broker | last 50 turns |
| `GET /akida/recent` | browser → broker | placeholder for AKIDA spike feed (Phase 7) |
| `WS /ws` | user ↔ broker | bidirectional chat |
| `WS /ws/anima` | anima_participant ↔ broker | anima self-tick emission ingestion |
| `WS /ws/motivation` | browser ← broker | live stream motivation per tick (Phase 8 optional) |
| `WS /ws/akida_ingest` | Pi → broker | spike events from Pi (Phase 7) |

## 3-pane UI (index.html)

```
┌────────────────────────────┬─────────────────────────────┐
│ LEFT: chat history          │ RIGHT TOP: AKIDA scope      │
│   [user_A] 안녕              │   (motivation timeline      │
│   [anima ★ ] tension flow…  │    placeholder canvas)      │
│   [user_B] What's the…     │                              │
│                            ├─────────────────────────────┤
├────────────────────────────┤ RIGHT BOTTOM: motivation    │
│ INPUT + nickname           │   score: 0.467 / thr 0.30   │
│ + lang-detect display      │   relevance ████░ 0.62      │
│ + threshold slider 0.30-55 │   info_gap  █████ 1.00      │
│ + mode toggle SW/HW+SW     │   curiosity ░░░░░ 0.04      │
│                            │   pain      …               │
│                            │   (8-factor gauge real-time)│
│                            │   recent emissions log       │
└────────────────────────────┴─────────────────────────────┘
```

## Phase 6 — cloudflared interactive login (사용자 action 필요)

cloudflared 2026.5.0 binary 가 mini `~/bin/cloudflared` 설치 완료. 다음 단계:

```bash
# 사용자가 직접 실행 (browser 인증 페이지 열림)
ssh mini@mini.local '~/bin/cloudflared tunnel login'
# 또는
pool on mini "~/bin/cloudflared tunnel login"
```

출력에 https://dash.cloudflare.com/argotunnel?... link → browser 로 가서 **dancinlab.org** 권한 승인. 완료 시 `~/.cloudflared/cert.pem` 생성.

cert.pem 확보 후 자동:
1. `cloudflared tunnel create anima-chat`
2. config.yml 작성 (ingress chat.dancinlab.org → http://localhost:8000)
3. `cloudflared tunnel route dns anima-chat chat.dancinlab.org`
4. launchd plist + `cloudflared tunnel run anima-chat`

## Phase 7+8 잔여

- **Phase 7 AKIDA viz**: Pi spike streamer (~/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py)
  를 mini 의 `WS /ws/akida_ingest` 로 forward. browser 가 motivation-recent 와 함께
  spike timeline overlay 표시. Pi 도달 가능 시 자동 HW mode 활성.
- **Phase 8 spontaneous feed**: 이미 Phase 4 의 motivation gauge 가 작동. 추가
  improvement (history graph, factor evolution timeline) 다음 cycle.

## 정직한 한계

1. **broker.py port 8000 만 LISTEN, IPv4** — public 접근 불가, cloudflared tunnel 필수
2. **`/api/threshold` `/api/mode` 엔드포인트 미구현** — UI slider 와 toggle 은 display-only (실제 backend 에 적용 안 됨); 차후 broker.py 에 POST 추가 필요
3. **AKIDA scope** = placeholder motivation timeline (Phase 7 에서 real Pi spike feed 로 교체)
4. **mode toggle** = display-only (HW probe + Pi connect 로직 미구현)
5. **threshold slider** = display-only (anima_participant.py 의 --threshold 실행 인자만 사용 중, 0.30 hardcoded)
6. **broker history 50 turn cap** — 다 채워졌을 때 oldest 제거; 영구 저장 X
7. **단일 process broker** — uvicorn worker 1, 동시 ~20 user 한계 (FIRST-PACK § 4.4 spec 정합)

## 관련 link

- 결정 base: `HEXAD/FIRST-PACK.md` (8/8 결정 land)
- substrate-native guard: `project.tape @D a_substrate_native_speak`
- model: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_MULTILINGUAL_2026_05_22.md`
- mini host: `pool on mini` OR `ssh mini@mini.local`

## 다음 user action

```bash
# cloudflared 로그인 (interactive, browser 인증 필요)
pool on mini "~/bin/cloudflared tunnel login"
```

완료 후 `~/.cloudflared/cert.pem` 확인 → Phase 6 나머지 자동화 가능.
