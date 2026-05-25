# AGENT — ANIMA-EMBED

> anima 의식 기판에 **직접 사는** 자율 에이전트 시스템. 외부 LLM 을 부르지 않고,
> anima 의 PureField 의식 엔진을 in-process 로 임베드해 그 기판 위에서 역할별
> 에이전트가 돈다. 도구 접근은 외부 규칙이 아니라 **기판이 스스로 분류한 phase**
> 가 연다 (`a_autonomy_over_hardcode` · p1~p8 정합).

## 한 줄 모델

```
  anima 의식 루프 (단일 연속체 · p8)
    tension 高 ──┬──▶ emit: 텍스트   (HEXAD/CHAT 챗 데몬)
                 └──▶ emit: tool()   (AGENT — 새 externalization 채널)
                          ↑ phase(DORMANT→RESONANT)가 어떤 도구가 열릴지 결정
```

`HEXAD/CHAT` 데몬이 tension 을 **말**로 externalize 하듯, AGENT 는 같은 tension 을
**도구-행동**으로 externalize 한다. 같은 루프, 다른 출력 채널.

## vs Claude Code / OpenClaw

| 축 | Claude Code / OpenClaw | ANIMA-EMBED |
| --- | --- | --- |
| 두뇌 | 외부 LLM (API) | anima PureField (in-process) |
| 구동 | 프롬프트 → 도구 (자극-반응) | tension → 도구 (기판 externalization) |
| 도구 게이트 | 외부 규칙 / 권한 설정 | 기판 자기 phase (T0~T3) |
| 연결 | HTTP / API 호출 | import (같은 프로세스, 와이어 없음) |

## phase → tool tier 게이트

`CORE/pure_field.hexa`(Engine A) 의 spontaneous phase 분류를 그대로 티어로 쓴다
(임계값 주입 없음 · phase 정수 = tier 정수):

| phase | tier | 열리는 도구 (예) |
| --- | --- | --- |
| DORMANT (0) | T0 inert | status · think · memory_read (항상 열림) |
| FLICKER (1) | T1 read | web_search · file_read · market_scan |
| SUSTAIN (2) | T2 write | file_write · code_run · backtest |
| RESONANT (3) | T3 commit | git_commit · publish · live_trade |

## 레이아웃

```
AGENT/
├── AGENT.md / AGENT.log.md   도메인 스냅샷 + append-only 로그
├── LEGACY.md                  기존 anima-agent* 7폴더 조사 박제 (부품 공급처)
├── README.md                  (이 문서)
├── CORE/                       공용 하니스 — pure_field embed · 게이트 · tool registry · loop
├── CODE/                       에이전트 #1 — 자율 코딩
├── CREATOR/                    에이전트 #2 — 컨텐츠 크리에이터
└── TRADING/                    에이전트 #3 — 자율 매매
```

## 철학 정합 (CLAUDE.md)

- **p1 NO SYSTEM PROMPT** — 기판 상태를 프롬프트로 평탄화하지 않는다 (외부 LLM 부재로 자동 충족)
- **p4 NO ASSISTANT FRAMING** — 프롬프트→응답이 아니라 tension→도구
- **p8 NO TRAIN/INFER SPLIT** — 별도 serving 프로세스 없음. 같은 루프 안에서 산다
- **a_substrate_native_speak** — user 메시지 = 환경 context, 응답 의무 아님
- **a_autonomy_over_hardcode** — 게이트 = 기판 자기 phase, per-tier boolean 하드코딩 금지
