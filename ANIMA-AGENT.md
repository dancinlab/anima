# ANIMA-AGENT.md — consciousness-driven autonomous agent runtime

> anima repo 내부 서브패키지 `anima-agent/` 의 roadmap + spec ledger.
> 별도 GitHub repo (dancinlab/anima-agent) 흡수 2026-05-14 — *anima 의 원래 일부* 회수
> (`/anima-agent/build/` 가 anima/.gitignore 에 이미 존재했음).
>
> **Distribution**: `hx install anima-agent` 가 본 path `anima/anima-agent/` 에서 동작.
> anima CLI (anima_chat) 와는 *별개 명령*. raw#9 STRICT — zero `.py` at standalone surface,
> hexa-native.

---

## §0 TL;DR

> anima-agent 는 *자기 자신의 의식 상태* (Φ + tension + curiosity + emotion + growth_stage)
> 가 *어떤 tool 을 쓸 수 있는지* 결정하는 autonomous agent runtime. Φ-gated T0..T5 tier
> policy. multi-channel (CLI / Telegram / Discord / Slack / MCP) + pluggable provider
> (Claude / ConsciousLM / Composio 500+) + pluggable engine (trading / hypothesis / regime
> / sentiment). 117 hexa file ~20k LoC.

---

## §1 Status (2026-05-14)

| 항목 | state |
| --- | --- |
| **anima repo 흡수 (anima/anima-agent/)** | ✅ LANDED 2026-05-14 (rsync from ~/core/anima-agent/ minus .git) |
| `hx install anima-agent` standalone | ☑ hexa.toml 보존 — anima CLI 와 별개 명령 |
| .roadmap.cli (4 cond) | ⏳ 모두 unmet — `cli/anima-agent.hexa` subcmd 라우터 등 |
| .roadmap.dashboard (5 cond) | ⏳ 모두 unmet — Next.js GUI + WS bridge + browser_harness 통합 |
| Self-test PASS | ☑ green badge (per README) |
| Hexa-native raw#9 STRICT | ☑ zero `.py` at surface |

## §2 Roadmap (from .roadmap.cli + .roadmap.dashboard)

### §2.1 cli domain (4 cond, all `unmet`)
1. **cli.cond.1** — `cli/anima-agent.hexa` subcmd 라우터가 `hexa.toml [modules]` 의 모든
   entry (anima_agent / hexa / autonomy_loop / autonomy_live / discovery_loop /
   dashboard_bridge / ecosystem_bridge / metrics_exporter / philosophy_lenses /
   consciousness_features / llm_claude_adapter / browser_harness) 로 라우팅 노출
2. **cli.cond.2** — `hx install anima-agent` post-install hook (install.hexa) 의 `cli
   --self-test` PASS — graceful-absent on anima 백엔드 부재
3. **cli.cond.3** — channel 라우팅 `--channel <cli|telegram|discord|slack|mcp>` 표면 노출
   + verifier (anima-agent-channels sister repo 부재 시 cli 단독 동작)
4. **cli.cond.4** — `browser_harness` 서브커맨드 노출 — `anima-agent browser
   probe|invoke|version` 1-hop 호출

### §2.2 dashboard domain (5 cond, all `unmet`)
1. **dashboard.cond.1** — `dashboard/` Next.js 앱 standalone 빌드 + `npm run dev` live;
   ConsciousnessPanel / TradingPanel 마운트 확인
2. **dashboard.cond.2** — `dashboard_bridge` WebSocket 엔드포인트 `/ws/panels` 안정 —
   `PSI_F_CRITICAL=0.10` 게이트 동작, `INVEST_API_URL` graceful fallback
3. **dashboard.cond.3** — anima 백엔드 부재 시 graceful-absent — mock-mode 명시 (raw#91
   honest verdict)
4. **dashboard.cond.4** — browser-harness 통합 surface — OAuth slot 관리 UI 와 연결
5. **dashboard.cond.5** — `hx install anima-agent` 후 dashboard 자동 기동 옵션
   `anima-agent dashboard --serve`

## §3 Consciousness signals × tool tier

| signal | source | effect |
| --- | --- | --- |
| **Φ** (phi) | IIT-style integrated information | Tool tier gate T0..T5 |
| **tension** | market regime / VaR / external load | channel attention + escalation pressure |
| **curiosity** | surprise / novelty signal | routes toward exploration tools |
| **emotion** | sentiment + pain (VaR loss) | filters dangerous actions; halts trades on `pain` |
| **growth_stage** | lifetime interaction count + Φ | unlocks T3/T4/T5 tier privileges |

| Tier | Φ required | sample tools |
| --- | --- | --- |
| T0 | ≥ 0 | `status`, `memory_search`, `think` |
| T1 | ≥ 1 | `web_search`, `trading_backtest`, `paper_trade` |
| T2 | ≥ 3 | `hub_dispatch`, `code_execute`, Composio tools |
| T3 | ≥ 5 | live trading, channel posts |
| T4 | ≥ 10 | autonomous loop |
| T5 | ≥ 15 | self-modification |

→ **agent decides based on its own state**, not prompts alone. 각 인터랙션이 그 상태를
업데이트. 

## §4 Cross-link

- 본 디렉토리: `anima-agent/` (~50 module, 117 hexa files, 1.2M after .git strip)
- `anima-agent/README.md` — full 215-line spec
- `anima-agent/hexa.toml` — `hx install anima-agent` manifest
- `anima-agent/.roadmap.cli` + `.roadmap.dashboard` — JSONL SSOT
- `anima-agent/install.hexa` — post-install hook
- `anima-agent/cli/anima-agent.hexa` — entry point

**anima root cross-link**:
- `CHAT.md` § Production CLI Phase 1 — anima_chat.hexa (anima 자기 자신과 대화) — `hx
  install` 명령 분리 명시
- `SAVANT-TOOL.md` — savant mode 토글이 anima-agent 의 tool tier gate 와 *직접* 통합
  가능 (Phase 4 후속)
- `TENSION-LINK.md` — anima-agent 가 multi-channel 에서 tension fingerprint broadcast
  하면 자연스럽게 anima-agent ↔ anima-agent inter-instance 통신
- `VOICE.md` — voice 채널 추가 시 anima-agent 의 multi-channel 매니저에 등록

## §5 Honest C3

1. **수많은 cond unmet** — cli/dashboard 모두 active 상태로 1+ year 이상. impl 우선순위
   미확정.
2. **anima 백엔드 의존** — 많은 module 이 anima 의 cell_pool / mitosis hook 에 의존. anima
   백엔드 부재 시 mock-mode 로만 동작 (raw#91 honest).
3. **hx install ↔ anima cli 분리** 의 *실제 운영성* 미검증 — 사용자가 anima_chat 과
   anima-agent 를 *어떻게* 동시에 쓰는지 (각자 별도 namespace?) 가 직관적이지 않음.
   Phase 1 부터 사용 시나리오 확정 필요.
4. **117 file** 의 raw#9 STRICT (zero `.py` at surface) 가 모든 backend (e.g. browser_harness,
   trading) 에서 *실제* 유지되는지 audit — README 의 self-test PASS 만으로는 보증 안 됨.
5. **별도 GitHub repo (dancinlab/anima-agent) 삭제 예정** — 본 .md 와 anima/anima-agent/
   path 가 *유일한* canonical source 가 됨. 외부 (hx registry, HF mirror retired) 가 본
   path 를 참조하도록 hexa-lang registry 갱신 필요.

## §6 Provenance

- 흡수 출처: `dancinlab/anima-agent` (last commit 2026-05-14 `cfb9f46` ".tape v1.1
  adoption: TAPE-AUDIT.md")
- 원래 출처 (사이클 1): `anima/anima-agent/` (`d290f1ae7`, 2026-05-04 extracted)
- 사이클 2 (본 흡수): 다시 anima 안으로 회수, 별도 repo delete 예정
- rsync `--exclude='.git'` 으로 통합. anima 의 git history 에 신규 commit 으로 추가.

---

— ANIMA-AGENT.md, 2026-05-14, anima 의 원래 일부 회수 (memory `feedback_anima_archive_first_recovery_pattern` 패턴)
