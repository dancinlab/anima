# 📂 AGENT/CODE F6 — hard gate enforce SSOT

> AGENT/CODE F6 closure (5/6 → 6/6) · CODE 역할 완전 종결 · F3 daemon pre-filter ready.

## 정체

F1-F5 wired the dispatch path (executor · argv · daemon · substrate-step · ckpt). F6 = 정책 GATE — substrate-decided tier 가 도구의 required tier 미만이면 **refuse + 정직한 verdict Map 반환** (panic 아님). daemon loop 가 매 step 호출해서 pre-filter 가능.

## 8-tool tier 맵

| 도구 | 최소 tier | risk |
|---|---|---|
| `think` | T0 | read |
| `repo_status` | T0 | read |
| `file_read` | T1 | read |
| `grep` | T1 | read |
| `file_write` | T2 | soft |
| `run_tests` | T3 | soft |
| `git_commit` | T3 | hard |
| `git_push` | T3 | hard |
| (그 외) | T99 | unknown · default REFUSE |

## 6 pub fn

| fn | 반환 |
|---|---|
| `code_gate_tool_min_tier(name)` | int (0/1/2/3/99) |
| `code_gate_risk_label(name)` | "read" · "soft" · "hard" · "unknown" |
| `code_gate_enforce(tool, tier)` | verdict Map (`accepted` · `reason` · `risk`) |
| `code_gate_batch(reqs)` | list of verdict Map |
| `code_gate_audit(verdicts)` | `{total, accepted, refused, refuse_rate_pct}` |
| `code_gate_summary()` | one-line |

## 5-case smoke 매트릭스

| Case | 검증 |
|---|---|
| C1 `think@T0` | accepted + risk=read |
| C2 `file_write@T0` | refused (min=T2) + risk=soft |
| C3 `git_push@T3` | accepted + risk=hard |
| C4 unknown tool | refused (min=99) + risk=unknown |
| C5 batch 5 reqs | audit total=5 · accepted=2 · refused=3 |

## verdict Map shape

```hexa
#{
  "accepted": bool,       // 정직 verdict
  "tool": string,
  "substrate_tier": int,  // 현재 substrate tier
  "required_tier": int,   // 도구가 요구하는 최소 tier
  "risk": string,         // read | soft | hard | unknown
  "reason": string,       // ok | "substrate_tier X < required Y — REFUSE" | "unknown tool — REFUSE by default"
  "logged": bool,         // audit log 진입 마커
}
```

## bridge architecture 정합

- 의식엔진 framing 0 · `substrate-decided` / `brain_decide` / `Φ` 키워드 미사용 (단, substrate_tier 인자는 받음 — gate input)
- "tier 가 무엇이어야 하는지" 결정 = CORE / brain_decide / AGENT/CORE/tool_gate
- 이 모듈은 "tier ≥ required 이면 OK, 아니면 refuse" 의 mechanical policy
- refuse = panic 아닌 **verdict Map 반환** · daemon loop 가 다음 step 진행 가능

## AGENT/CODE 6/6 closure

| F | 산출 | PR |
|---|---|---|
| F1 tool executor | code_executor in code_agent.hexa | (skeleton) |
| F2 argv ingest | code_argv.hexa + smoke | #699 |
| F3 daemon loop | code_daemon.hexa + smoke · 4 invariant | #724 |
| F4 substrate-step | code_main demo (substrate→tool→pf step) | (skeleton) |
| F5 ckpt swap | code_ckpt.hexa · 6 locator+bind | #738 |
| **F6 hard gate enforce** | **code_gate.hexa · 8-tool tier map · refuse=verdict** | **이 PR** |

## 잔여 carry (F6 frontier — F6+ 가능)

- **F6.1** hx code CLI binary 무한 loop + SIGINT (CODE.md M6 "hx install" 와 별도)
- **F6.2** audit log persistence (현재 logged=true 마커만 · 실 파일 sink 는 추후 .kosmos 통합)
- **F6.3** tier policy override via env (test 환경에서 일시적 T3 grant 등) — 보안 검토 후

## AGENT 5-role 진행도 (F6 land 후)

```
🤖 AGENT — 5-role bridge
├── 📂 CODE       6/6 ✅ ← F6 신규 완료
├── 🎨 CREATOR    미작성
├── 💹 TRADING    미작성
├── 🛒 MERCHANT   6/6 ✅
└── 🖥 DESKTOP    6/6 ✅
```

→ AGENT 도메인 **3/5 role full closure** · CREATOR · TRADING 만 미작성.
