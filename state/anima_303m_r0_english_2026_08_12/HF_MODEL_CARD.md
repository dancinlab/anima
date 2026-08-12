---
license: other
language:
- en
pipeline_tag: text-generation
---

# Anima 303M English R0 seed 7 — failed research checkpoint

This private artifact is a from-scratch 303,097,856-parameter byte-level research checkpoint. It
is retained as negative evidence and is not approved for conversation or production use.

- Source code: `dancinlab/anima@73caa5b06df36c9f210d46ba9ba46e2afa6bfcfd`
- Data: private immutable
  `dancinlab/anima-303m-r0-proportional-conversation-data-2026-08-12@ee143002d9494cac4ed4a821dadfb5ece60c1e74`
- Protocol/panel: `state/anima_303m_r0_english_2026_08_12/`
- Fixed run: seed 7, 14,000 steps, RTX 4090, Python-only canonical engine
- Automatic conversation result: semantic `0/7`, structural `3/7`, multi-turn failure
- Manual result: `0/7`; all replies were irrelevant, incoherent, or failed memory/correction
- Verdict: `FAIL-MEANINGLESS-IRRELEVANT`

Do not deploy this checkpoint. R1 and production remain locked.
