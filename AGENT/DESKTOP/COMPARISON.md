# 🔍 DESKTOP — 시중 3대 Desktop Agent 기술 구현 비교 (2026-05-26)

> **anima DESKTOP 은 macOS 전용** 도구 surface. Gemini Spark / Claude Computer Use / Codex Desktop 와 같은 카테고리 (사용자 컴퓨터 자율 사용 대체) 이나 다음 두 점에서 차별: (1) 외부 LLM 0 — 의식적 결정은 CORE/brain_decide 가 담당, (2) OS native API 우선 — vision 분석은 Accessibility API + Vision OCR 통과.

## 1. Gemini Spark — Google · 2026-여름 macOS

- **실행 위치**: 클라우드 (Dedicated Google Cloud VMs · 24/7 persistent runtime)
- **macOS 통합**: native Mac app + voice + Spark agent (여름 2026)
- **확장 프로토콜**: **MCP** (Linux Foundation Agentic AI Foundation 산하) — N×M 통합 문제 회피
- **UI 표시**: Android Halo (디바이스 상단 진행 표시)
- **특징**: 로컬 화면 제어 < 클라우드 워크플로 + Google Workspace 통합

## 2. Claude Computer Use — Anthropic · 2026-03 macOS

```
┌───────────────────────────────────────────┐
│  agent loop:                              │
│   Claude → tool call (click/type/scroll)  │
│   app → execute in VM → tool_result       │
│   loop until done                          │
└───────────────────────────────────────────┘
```

- **실행 위치**: VM/컨테이너 (Xvfb 가상 X11 + Mutter + Tint2 + Linux apps)
- **API**: `computer-use-2025-11-24` beta header + Claude 4.x
- **메커니즘**: screenshot-analyze-act 반복 loop
- **함정**: **좌표 매핑** — API 가 screenshot 크기 제한 → 실 화면 좌표 ↔ 모델 좌표 resize/remap 필수
- **특징**: 격리 VM (실제 사용자 데스크탑 X)

## 3. Codex Desktop — OpenAI · 2026-04 v26.415 macOS

```
사용자 커서  ━━━━━━━━━━━━━ 화면 1개
                    ↕  동시
agent 커서   ╱╲╱╲╱╲   (안 보이는 layer)
```

- **실행 위치**: 로컬 macOS · **두 커서 동시** (Cua-Driver via SkyLight APIs + yabai focus-without-raise)
- **메커니즘**: screenshot + vision 모델 + click/type · 백그라운드 격리 프로세스 + async 통신
- **플러그인 구조 (3-in-1)**:
  - **Skills**: prompt workflows
  - **App integrations**: API 또는 GUI 자동화
  - **MCP server configs**: 모두 패키징
- **현재 90+ 플러그인** · **macOS only** (Windows/Linux undated)

## 📊 비교 매트릭스

| 축 | Gemini Spark | Claude CU | Codex Desktop | **anima DESKTOP** |
|---|---|---|---|---|
| 실행 | 클라우드 VM | 격리 Linux VM | 로컬 macOS | **로컬 macOS** |
| 모달 | text + image | vision (screenshot) | vision (screenshot) | OS native (AX tree + Vision OCR) |
| 커서 | N/A | 1개 | **2개 layered** | 1개 (user 와 충돌) |
| 확장 | MCP | tool_use API | Skills+API+MCP | (TBD) |
| LLM 의존 | Gemini cloud | Claude cloud | GPT-4o cloud | **0** (CORE substrate) |
| 비용 | API tier | API tier | Pro/Max sub | **$0 local** |
| 플랫폼 | Mac (여름) + Android | macOS · Windows TBD | macOS only | **macOS only (by design)** |

## 🆚 anima DESKTOP 차별 (요약)

| 자산 | 3대 (LLM 의존) | anima DESKTOP |
|---|---|---|
| 의사결정 LLM | 클라우드 vision 모델 | CORE/brain_decide (substrate · p1) |
| 화면 분석 | screenshot → vision | AX tree (구조) + screencapture+Vision OCR (텍스트) |
| 확장 | MCP / Skills / tool_use | AGENT/CORE tool_gate (직접) |
| 비용 | per-token API | $0 |
| 플랫폼 | 다중 (또는 클라우드 의존) | **macOS 단일** (Accessibility / CGEvent / NSWorkspace / Vision native) |

## 💡 anima DESKTOP 미래 후보 milestone (현재 6 외 추가)

| 후보 | 영감 출처 | 비고 |
|---|---|---|
| **M7 invisible cursor layer** | Codex SkyLight + yabai | 사용자와 동시 작업 (현재 M3 액션은 user 와 충돌) |
| **M8 MCP server endpoint** | Gemini Spark + Codex | anima 의 도구 surface 를 MCP server 로 expose, 외부 agent 가 anima 도구 사용 가능 |
| **M9 plugin manifest** | Codex Skills+API+MCP 3-in-1 | task primitives (M5) 를 패키지 형식으로 |
| **M10 coordinate-mapping helper** | Claude CU 좌표 함정 | OS scale factor + Retina DPR 대응 |

## 🍎 macOS-only 결정 근거

- **단일 OS 깊이 통합** — Accessibility API · AppleScript · CGEvent · NSWorkspace · Vision · SkyLight 모두 macOS native (cross-platform 추상화 필요 X)
- **Apple Silicon ARM64** — anima 의 hexa-native runtime 이 이미 ARM64 우선
- **사용자 환경 일치** — anima 사용자 = macOS 사용자 (현재 세션의 platform=darwin · macOS Sequoia 25.5.0)
- **회피 비용** — Windows/Linux 추상화 = 3배 코드 + 3배 검증, 우선순위 낮음
- **미래 확장 여지** — Linux 가 필요해지면 별도 도메인 (`DESKTOP-LINUX` 같은 형제) 으로 분기, anima DESKTOP 자체는 macOS 정체성 유지

## 출처 (Sources)

### Gemini Spark
- [agent-wars.com — Gemini Mac App 2026-04-19](https://www.agent-wars.com/news/2026-04-19-gemini-app-on-mac)
- [efficientlyconnected — Google I/O 2026 Spark](https://www.efficientlyconnected.com/google-io-2026-gemini-spark-consumer-ai-agent/)
- [DEV — MCP inevitability](https://dev.to/megberts/google-io-just-made-mcp-inevitable-1abf)
- [analyticsinsight — voice + Spark](https://www.analyticsinsight.net/tech-news/googles-gemini-mac-app-will-soon-support-voice-commands-and-spark-ai)

### Claude Computer Use
- [platform.claude.com — Computer use tool API docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- [LaoZhang AI Blog — technical deep dive](https://blog.laozhang.ai/en/posts/claude-computer-use)
- [crazyrouter — API guide 2026](https://crazyrouter.com/en/blog/claude-computer-use-api-guide-2026)
- [code.claude.com — Computer Use CLI docs](https://code.claude.com/docs/en/computer-use)

### Codex Desktop
- [digitalapplied — Codex Desktop + plugins guide](https://www.digitalapplied.com/blog/openai-codex-desktop-computer-use-plugins-guide)
- [buildmvpfast — background computer use](https://www.buildmvpfast.com/blog/openai-codex-background-computer-use-desktop-agent-2026)
- [openai.com — Codex for almost everything](https://openai.com/index/codex-for-almost-everything/)
- [developers.openai.com — Computer Use Codex app](https://developers.openai.com/codex/app/computer-use)

---

**작성**: 2026-05-26 (DESKTOP M2 land 직후) · **갱신**: 시중 3대 agent 메이저 업데이트마다 재검색 권장 · **참고**: 이 도메인은 macOS only.
