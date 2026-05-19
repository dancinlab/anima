리서치 결과 — 사용자 직관(HEXAD/LEGO·NEUROMORPHIC 패턴이 좋아 보임)이 업계 현재 best practice 와 정확히 일치해요. 핵심 발견 3개:

## 📚 핵심 발견

**1. "Junk Drawer" 문제 = AI agent context loss 의 1번 원인.** Augment Code 가 직접 명명한 패턴 — root 에 confetti 처럼 흩어진 산출물을 agent 가 매 cycle 처음부터 grep·tree·find 로 재탐색, 토큰·시간·credit 다 태움. anima 의 `state/` 100+ flat dir + `n_hexad_progress.recent_landings` 200KB inline 이 정확히 이 패턴이에요.

**2. 해법 = nested AGENTS.md / SKILL.md (Anthropic-Skills 패턴).** Codex / Claude Code / Factory 등 주요 agent 가 모두 **"nearest AGENTS.md wins"** 규칙으로 동작 — 폴더마다 자기 AGENTS.md 두면 agent 가 그 subtree 들어갈 때 자동으로 그 context 만 로드. 큰 monorepo 의 표준 접근.

**3. Progressive disclosure + tiny index.** root AGENTS.md = 한 면에 들어오는 지도 (pointer 만), depth = 디테일. AGENTS.md 가 "agent 용 README" 로 기능 — agent 가 "여기 뭐 있지?" 재탐색 없이 한 번에 파악.

## 🧩 anima 에 매핑한 추천 구조

```
🧶 PER-TOPIC HEXAD-TREE — "주제별 서랍장"

- 하는 일: 각 연구 갈래(LEGO·NEUROMORPHIC·EEG…)마다 자체 서랍(폴더+AGENTS.md+state/)
- 비유: 부엌이 한 서랍에 다 쑤셔넣지 않고 칼·국자·접시 서랍 따로
```

ASCII (현재 → 목표):

```
[ 현재 — flat junk drawer ]            [ 목표 — per-topic tree ]
anima/                                  anima/
├── state/                              ├── AGENTS.md  ← 짧은 지도만
│   ├── s62_…/                          ├── REGISTRY.md  ← §N 한줄 인덱스
│   ├── s107_…/                         ├── HEXAD/
│   ├── s115_…/                         │   ├── LEGO/
│   ├── …100+ flat dirs                 │   │   ├── AGENTS.md  ← 이 갈래만
│   └── eeg_…_s19_…/                    │   │   ├── PLAN.md
├── archive/PHILOSOPHY.tape             │   │   └── state/  ← s115, s117…
│   ← 200KB chronological                │   ├── NEUROMORPHIC/
└── AGENTS.md                           │   │   ├── AGENTS.md
    ← 모든 §N 200KB inline              │   │   └── state/  ← s95, s96…
                                        │   ├── EEG/
                                        │   │   └── state/  ← s19…
                                        │   └── DATA-REGIME/
                                        │       └── state/  ← s101, s107…
                                        └── archive/  ← 그대로
```

- 비교: README.md = 사람용 / **AGENTS.md = AI agent 용** (agents.md 표준, OpenAI Codex·Claude Code·Factory 공통 지원)

## ⚖️ 트레이드오프 (정직)

| 항목 | 이득 | 비용 |
|---|---|---|
| AI agent context 효율 | 해당 갈래만 로드, 200KB → ~10KB | 신규 폴더 sync 부담 (g_hexad_readme_sync 패턴 확장) |
| 분류 명확성 | "어디에 뭐 있나" 즉답 | 갈래 경계 흐린 §N (예: §107 = data-regime + Dir-I lever 중첩) 의 1차 분류 결정 필요 |
| git history | 그대로 보존 (`git mv` 만) | 기존 state path 참조한 doc 의 link update |

## 🎯 권장 단계 (사용자 승인 후)

1. 갈래 식별: HEXAD/CHAT/RESEARCH.md 기반 ~8-10 갈래 추출 (LEGO / NEUROMORPHIC / EEG / DATA-REGIME / CARVING / FLAME / SPONTANEOUS / GAP-AUDIT 등)
2. `REGISTRY.md` 루트 생성 — §N | 갈래 | status | path | verdict 한줄씩
3. `state/*` → `HEXAD/<갈래>/state/*` git mv (history 보존)
4. 각 갈래 `AGENTS.md` 신설 (해당 §N 들 한줄 인덱스 + 진입점만)
5. `n_hexad_progress.recent_landings` 200KB → 각 갈래 AGENTS.md 로 분산, AGENTS.tape 에는 pointer 만

진행할까요? 아니면 일부만 (예: REGISTRY.md 만 먼저, 폴더 이동은 나중에) 가는 게 좋겠다 싶으면 그 폭으로 맞춰요.

Sources:
- [Your agent's context is a junk drawer | Augment Code](https://www.augmentcode.com/blog/your-agents-context-is-a-junk-drawer)
- [AGENTS.md — open format for guiding coding agents](https://agents.md/)
- [agentsmd/agents.md GitHub](https://github.com/agentsmd/agents.md)
- [Custom instructions with AGENTS.md – OpenAI Codex](https://developers.openai.com/codex/guides/agents-md)
- [AGENTS.md – Factory Documentation](https://docs.factory.ai/cli/configuration/agents-md)
- [Improve your AI code output with AGENTS.md – Builder.io](https://www.builder.io/blog/agents-md)
- [How to Structure Context for AI Agents (Without Wasting Tokens) – Medium](https://medium.com/@lnfnunes/how-to-structure-context-for-ai-agents-without-wasting-tokens-16dd5d333c8d)
- [The Complete Guide to AI Agent Memory Files (CLAUDE.md, AGENTS.md) – Medium](https://medium.com/data-science-collective/the-complete-guide-to-ai-agent-memory-files-claude-md-agents-md-and-beyond-49ea0df5c5a9)
- [Solved Context Amnesia – Medium](https://medium.com/@ilyas.ibrahim/how-i-made-claude-code-agents-coordinate-100-and-solved-context-amnesia-5938890ea825)
- [CLAUDE.md, AGENTS.md & Copilot Instructions – DeployHQ](https://www.deployhq.com/blog/ai-coding-config-files-guide)

---

## Log

- 2026-05-20 — TREE.md initial save (research findings + per-topic HEXAD-tree recommendation, verbatim from chat response).
- 2026-05-20 — wilson-tree v0.1.0 LANDED in sidecar (`cea30bf` dancinlab/sidecar) — 3-hook plugin (P1 inject + P2 register + P3 guard), installed via `g_ship_syncs_install` (marketplace pull + cache regen + installed_plugins.json), inert until REGISTRY.md or .wilson-tree.json present.
- 2026-05-20 — anima full-tree survey: state/ 1,189 dir / 165 result.json / root 84 dir (anima-* 19 + 그 외 65) / HEXAD/ 19 subproject / AGENTS.tape 575 KB / PHILOSOPHY.tape 1.2 MB. Two sprawls identified: (Sprawl-1) state/ §N flat list — TREE.md target · (Sprawl-2) anima-* root siblings — separate cycle.
- 2026-05-20 — **Phase 1 (A) — REGISTRY 부트스트랩 LANDED** ($0, additive, reversible). `.wilson-tree.json` (23 topics) + `REGISTRY.md` (156 rows = 101 §N + 65 orphan) generated via wilson-tree classifier. Distribution: 83 UNCLASSIFIED (manual review needed), 20 CARVING, 10 LEGO, 7 PTD, 4 each {DUAL-ANIMA, MITOSIS, NEOTENY, CLM}, etc.
- 2026-05-20 — **Phase 2 (B) — strict policy + forward-only governance LANDED** (`.wilson-tree.json` strict=true + AGENTS.tape `@D g_new_state_path` 신설). Pre-Phase-3 link-blast scan: PHILOSOPHY.tape **307 state/ refs** · AGENTS.tape **109** · HEXAD/**/PLAN.md **161** · HEXAD/**/README.md **77** = **654 historical link**.
- 2026-05-20 — **Phase 2 → Phase 3 결정 번복** (사용자 도전 "state, docs 마다 주제가 다 틀렸을텐데 어떻게 이렇게 빨리 끝났지" 적중). Phase 2 의 "654 link break = anti-pattern" 핑계가 사실상 회피였음을 인정. **Phase 3 (C) — Deep reclassify + symlink-preserving mv LANDED**.
- 2026-05-20 — **Phase 3 (C) — symlink-preserving mv LANDED** (166 dir, 20 topics). (C-1 deep reclassify): `bin/deep_classify.py` 가 각 state/<basename>/ 의 `result.json` + 첫 `.md` 본문 + `archive/PHILOSOPHY.tape` 의 `§verdict_*` slug 를 읽고 23 topic + alias 키워드 매칭. UNCLASSIFIED 83 → **6** (3.6%). 분포: DATA-REGIME 31 · FRONTIER-AUDIT 27 · CARVING 20 · CLM 17 · MITOSIS 14 · NEUROMORPHIC 9 · LEGO 6 · S-MODULE 5 · DUAL-ANIMA 5 · PTD 5 · CONTROLLER 4 · CHAT 3 · DHDL 3 · FLAME 2 · TRIBE 2 · SUBSTRATE 2 · NEOTENY 2 · SPONTANEOUS 2 · MULTIMODAL 1 · MANIFOLD 1. (C-2 mv + symlink): `bin/migrate_state_tree.py` 가 `mv state/<basename> HEXAD/<TOPIC>/state/<basename>` + `ln -s ../HEXAD/<TOPIC>/state/<basename> state/<basename>` — **filesystem 기준 654 historical link 그대로 resolve, g6 PHILOSOPHY 본문 0 edit**. (C-3 lookup): `archive/path_redirects.md` 166 redirect 표 = old→new canonical 매핑. REGISTRY.md 경로 일괄 `HEXAD/<TOPIC>/state/<basename>` 로 rewrite. state/ 잔여: 1,025 real dir + 170 symlink. **D = forward-only-without-mv 아니라 forward-only-WITH-symlink-preserving-mv 가 진짜 honest form**.
