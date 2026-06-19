# DESKTOP — log

Append-only history sister of `DESKTOP.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-27 — M5 task primitives LANDED
- [x] `AGENT/DESKTOP/task_primitives.hexa` 5 pub fn composing M1+M2+M3+M4 (additive, no modifications to existing modules)
- [x] `task_open_and_type(app, text)` — launch + focus + type · risk: soft
- [x] `task_screenshot_app(app, out_path)` — focus + shot_window · risk: soft
- [x] `task_open_read_close(app)` — launch + focus + shot + ocr + quit · risk: **hard** (quit step)
- [x] `task_find_and_click(app, search_text)` — focus + bounds + shot + ocr + click center · risk: soft · honest limit: window-center (no bbox)
- [x] `task_multi_app_screenshot(apps, out_dir)` — focus_chain + shot_window×N · risk: soft
- [x] `AGENT/DESKTOP/task_primitives_smoke.hexa` 4-case DRYRUN smoke (contract dict + hard risk + count==3)
- [x] `AGENT/DESKTOP/TASK_PRIMITIVES.md` Korean SSOT — 5-macro table + composition diagram + M6 dependency
- [x] hexa parse 2/2 OK
- [x] DESKTOP.md M5 line flipped `[ ] → [x]`
