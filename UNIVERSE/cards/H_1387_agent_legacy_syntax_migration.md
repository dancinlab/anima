# H_1387 — agent legacy map-literal syntax migration: the executor module COMPILES (closes the H_1386 ⏳ build step)

🔗 **Closes (END-TO-END):** the named ⏳ build step of [H_1386](H_1386_agent_layer_routing.md). H_1386 wired the agent-tool↔mitosis routing through a standalone CORE-importing **adapter** (`agent_skill_routing.hexa`) because `anima-agent-core/agent_tools.hexa` + `agent_sdk.hexa` were legacy Python-port files using map-literal / reference syntax the current hexa grammar rejects (~50 parse errors each). This lane migrates that legacy syntax so the WHOLE executor module parses + builds — and the H_1386 routing now closes through the MAIN module, not just the adapter.

- **slug:** agent_legacy_syntax_migration
- **tier / verdict:** **🟢 GREEN (COMPILES)** — `agent_tools.hexa` 50→0 parse errors + BUILDS (binary produced, runs, registers 19 tools); `agent_sdk.hexa` 50→0 + BUILDS. Syntax-only, behavior-preserving (c10 surgical). H_1386 routing call-sites preserved byte-for-logic; the agent-tool↔mitosis loop closes through the MAIN executor module (a live tool FAILURE grows a skill-cell 1→2 via `executor_execute`). NO CORE/*.hexa logic change.
- **domain:** MITOSIS-ENGINE · **substrate:** $0 CPU, hexa (agent-core) · no decode
- **evidence:** `.verdicts/1387_agent_legacy_syntax_migration/{FREEZE.txt, result.txt}` (verbatim BEFORE 50+50 / AFTER 0+0 build stdout + routing smoke + main-module close)

## The grammar incompatibility (probed, then migrated — syntax-only, c10)
The current hexa toolchain is **value-semantics only** (CORE/engine_cli.hexa uses ZERO `&`); the legacy Python-port used four constructs the grammar rejects:

| # | rejected legacy construct | migrated to (behavior-preserving) |
|---|---------------------------|-----------------------------------|
| 1 | string-keyed / nested map literals `{"k": v}` / `{"k": {"a":..}}` | empty `{}` + index-assignment `m["k"] = v` (build-then-return — the CORE idiom; empty `{}` is grammar-accepted) |
| 2 | reference-passing `&` / `&mut` in **param types** AND `&expr`/`&mut expr` **call args** | by-value params; mutating fns RETURN the modified struct; call-sites reassign (`reg = registry_register(reg, ..)`, mirroring `store = skill_store_teach(store, ..)`) |
| 3 | two-var `for k, v in <map>` / `for i, x in enumerate(arr)` | `for k in keys(<map>) { let v = <map>[k] }` and `while`-index loops (same iteration order) |
| 4 | builtins not bound in current toolchain (`contains_item·hash·slice·sort_by·lowercase·insert_at`) + python-substrate stubs (`think·get_status`) | local pure-hexa helper fns with identical semantics (`hash`/`lowercase` via the proven `ord(substring(..))` byte-loop; CORE's `to_lower`/`char_code_at` are not resolvable once CORE is imported) |

These were a *layered* wall: the ~50 map-literal errors masked the `&`-syntax errors, which masked the missing-builtin errors — each surfaced only after the prior layer was fixed (`a_break_the_wall`: the wall was three walls, each a real grammar/toolchain rejection, not a ceiling).

## Frozen bars (FREEZE.txt — pre-registered BEFORE editing; c9, NO tune-to-green)
| bar | meaning | result | gate |
|-----|---------|--------|------|
| (1) COMPILES | `agent_tools.hexa` + `agent_sdk.hexa` parse + build, 0 parse errors | **agent_tools 50→0 builds · agent_sdk 50→0 builds** | ✅ |
| (2) ROUTING-INTACT | H_1386 call-sites preserved byte-for-logic; routing smoke passes through the compiling module | **agent_skill_routing_smoke 5/0**; `executor_select_tool`→`skill_recall`, `executor_execute` failure→`skill_store_teach` run live through the MAIN module (fail grows cell 1→2) | ✅ |
| (3) NO-REGRESSION | existing smokes green, deterministic; no CORE/*.hexa logic change | **engine_cli_smoke 110/0 · h1196 7/0 · h1205 PASS · routing 5/0 det 3×; 0 CORE files modified** | ✅ |

## Depletion verdict
The agent-tool↔mitosis loop now closes through the **MAIN executor module**, not just the H_1386 adapter: `agent_tools.hexa` compiles and runs, so the call-site delegation H_1386 already wired (`ToolExecutor.skills`, `executor_select_tool` → `agent_route_select` → `skill_recall`; `executor_execute` failure-site → `agent_route_on_result` → `skill_store_teach` → mitosis clonal split, p8) is live in-situ. A driver importing `agent_tools.hexa` confirms a real runtime tool FAILURE (`phi_measure` → success=false) grows a specialized skill-cell (1→2) through the main module. **TRUE: the loop closes through the main module.** 🏁

## Scope (a_scale_honest_scope · a_toy_scale_recheck) — honest (c9)
SYNTAX migration only — behavior is preserved, not extended. The `think`/`get_status` python-substrate stubs were given local placeholder definitions matching the file's existing TODO[python-sdk] convention (the real Python `AnimaAgent` bridge is unbuilt — those remain TODO, NOT faked into a real substrate). `agent_sdk.hexa` is an interface stub not imported by the executor module. Runtime-tool implementations (`tool_web_search`, etc.) are still TODO placeholders (unchanged). The migration touched only what the grammar/toolchain rejects (c10). Sibling files `code_guardian.hexa`/`tool_policy.hexa`/`unified_registry.hexa` (also legacy) are NOT in the executor-module compile chain and were left unchanged.

xref: H_1386 (agent-layer routing, the ⏳ build step closed here) · H_1382 (CORE §SkillStore faculty) · H_1378 (mirror, REFERENCE-ONLY gap) · a_verified_must_wire · a_core_engine_map · a_break_the_wall · a_engine_native_learning · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck · p6 · p7 · p8 · c2 · c9 · c10
