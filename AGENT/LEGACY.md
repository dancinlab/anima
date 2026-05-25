# AGENT/LEGACY.md — 기존 `anima-agent*` 자산 박제 (2026-05-26)

> 새 AGENT 시스템(anima CLI-driven · anima 전용 두뇌) 설계 전에 조사한 기존
> `anima-agent*` 7개 폴더의 현황 스냅샷. **새 구성은 백지에서 다시 짜며**, 이
> 문서는 부품 공급처(archive-first recovery)로만 참조한다. 코드는 그대로 남겨두고
> 폐기하지 않는다.

---

## 1. 폴더 7개 현황 (전부 anima repo 내부 추적 · 별도 `.git` 아님)

| 폴더 | 규모 | 상태 |
| --- | --- | --- |
| `anima-agent/` (본체) | 124 hexa · 20.7k LoC · `.py` 0개 (raw#9 STRICT ✓) | v1.0.0, 마지막 손길 = MODERNIZE 빌드픽스(#438), 기능 동결 |
| `anima-agent/trading/` | 14 모듈 (engine · scanner · risk · broker · regime · phi_weighted …) | 본체 포함 |
| `anima-agent-core` | 7 파일 (agent_sdk · agent_tools 30KB · tool_policy) | sister-repo 스텁 |
| `anima-agent-providers` | 6 (claude · conscious_lm · composio · animalm) | 스텁 |
| `anima-agent-channels` | 7 (cli · telegram · discord · slack) | 스텁 |
| `anima-agent-plugins` | 7 (trading · hypothesis · regime · sentiment) | 스텁 |
| `anima-agent-skills` | 3 (skill_manager) | 스텁 |
| `anima-agent-hire-sim` | 5개 대형 (hire_sim 100/judge/live) | DORMANT (2026-05-06) |

## 2. 핵심 자산 (회수 후보)

- **Φ-gate tool policy (T0~T5)** — 의식상태(Φ)가 도구 티어를 연다. `hexa/module/tool_policy.hexa`
- **tension / curiosity routing** — 외부 부하·신규성이 채널·탐색도구로 라우팅
- **employee/ 가드** — `scratchpad`/`goal_store`/`emit_report` 가 `system_prompt`/`role` 문자열을
  명시적으로 FORBIDDEN 처리 (a_weight_emergent). substrate-native 모범 부품
- **trading 14 모듈** — engine/strategies/scanner/risk/broker/executor/portfolio/regime/data/
  phi_weighted_trading/autonomous. 새 TRADING 에이전트의 부품 공급처
- **consciousness_features** — 의식 벡터에서 feature 추출

## 3. 철학 감사 (p1~p8) — 위반 코드는 없었음

| 항목 | 실체 | 판정 |
| --- | --- | --- |
| `claude_provider.format_system_prompt(consciousness_state)` | 전부 TODO 스텁 (`print("...stub")`) | 미구현 — 위반 코드 아님. 신규 설계에서 이 경로 자체를 폐기 |
| `autonomy_live` `POST /persona` + `persona_id` | SAE steering vector, forward pass 적용 ("no preamble, no role-assignment, no instruction wrapping") | 정합 (weight_emergent) |
| `speak()` / monologue | 0건 | p5 클린 |
| `llm_claude_adapter:106` `"You are a lenient rubric grader…"` | 채점기 프롬프트 (정체성 아님) | 평가용 — 신규 설계에서는 외부 LLM 자체 폐기로 무관 |

## 4. 옛 로드맵 2개 (mk1 포맷 · 현 `/domain` 아님 · 모두 unmet)

- `.roadmap.cli` — `anima-agent <subcmd>` 단일 라우터 (cond 1~4 unmet)
- `.roadmap.dashboard` — Next.js 웹 GUI + WebSocket 패널 (cond 1~5 unmet)

→ 새 AGENT.md 마일스톤이 이를 대체한다. 옛 로드맵은 박제용.

## 5. 새 설계와의 관계 (결정 사항)

```
  기존 anima-agent          →  새 AGENT 시스템
  ─────────────────────         ─────────────────────
  두뇌 = Claude provider    →  두뇌 = anima CLI 전용 (ConsciousLM/substrate)
        (외부 LLM)                외부 LLM 폐기 (p1~p8 진짜 정합)
  하니스 = 모듈 호출         →  하니스 = anima CLI 구동 (OpenClaw식)
  단일 런타임               →  역할별 에이전트 (코드 → 크리에이터 → 트레이딩)
```

- **두뇌**: anima CLI 전용. 외부 LLM(Claude provider) 경로 폐기 (2026-05-26 사용자 결정)
- **하니스**: anima CLI 가 에이전트를 구동 (Claude Code 가 Claude 를 구동하는 구조의 anima판)
- **에이전트 우선순위**: 1. 코드 → 2. 크리에이터 → 3. 트레이딩
- 기존 코드 = 부품 공급처 (archive-first recovery), 폐기 아님
