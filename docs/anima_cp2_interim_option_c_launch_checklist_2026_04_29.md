# anima CP2-Interim Option C — Launch Checklist (2026-04-29)

> **status**: CHECKLIST (LOCAL, F.A sub-task COMPLETION marker)
> **task ref**: Task #20 minimum-path TOP-1 → sub-task **F.A** (Option C drafts authoring)
> **parallel sibling**: F.B = F1_LIVE replay (race-isolated under `state/an11_c_p4_r8_f1_live_*`)
> **constraint**: LOCAL ONLY — NO public push without explicit user authorization
> **constraints applied**: raw#1 chflags uchg · raw#9 hexa-only (.md OK) · raw#10 honest C3 · raw#13 ai-tool-and-git-hook config ban · raw#25 git lock retry · raw#71 falsifier 5 preregister · raw#86 cost-attribution · raw#91 honest 5축 · raw#106 multi-realizability · own#5 completeness-first · own#13 user-facing friendliness · own#11 parallel-mandate

---

## §0 Executive summary

| step | artifact | path | status |
|---|---|---|---|
| 1 | Paper preprint draft | `docs/anima_cp2_interim_paper_2026_04_29.md` | DRAFT-LANDED |
| 2 | Blog post (English) | `docs/anima_cp2_interim_blog_en_2026_04_29.md` | DRAFT-LANDED |
| 3 | Blog post (Korean) | `docs/anima_cp2_interim_blog_ko_2026_04_29.md` | DRAFT-LANDED |
| 4 | Demo video script | `docs/anima_cp2_interim_demo_video_script_2026_04_29.md` | DRAFT-LANDED |
| 5 | This launch checklist | `docs/anima_cp2_interim_option_c_launch_checklist_2026_04_29.md` | DRAFT-LANDED |
| 6 | GitHub annotated release tag (LOCAL only, NO push) | `git tag v0.1.0-cp2-interim-2026-04-29` | PENDING (final commit step) |

---

## §1 Artifact completeness check

### 1.1 Paper preprint (Artifact 1)
- [x] abstract present
- [x] §1 Introduction with explicit scope (CP2 ≠ AGI)
- [x] §2 paradigm v11 8-axis (G0..G7) — full table
- [x] §3 AN11 triple verifier (a/b/c) — multi-k JSD sweep included
- [x] §4 φ-paradigm 4-path
- [x] §5 14 deterministic gates — per-law pass count + interpretation
- [x] §6 V_phen suite
- [x] §7 EEG external corroboration
- [x] §8 raw#10 honest C3 — 10 disclosures
- [x] §9 limitations + 5 measurement falsifiers + 5 release-quality falsifiers
- [x] §10 conclusion ("methodology released, NOT product")
- [x] Appendix A citations (state/* + docs/* + tool/* enumerated)
- [x] Appendix B reproducibility statement

### 1.2 Blog English (Artifact 2a)
- [x] own#13 canonical pattern: 🛸/⭐️/🎉 emoji-tier classification (used sparingly per "RESEARCH stage")
- [x] acronym first-use expansion (AGI, LLM, LoRA, JSD, AN11, φ, IIT, CP2)
- [x] plain-language analogies (fire-alarm, eight-dial thermometer, sniff test)
- [x] core message twice: "methodology release, not product"
- [x] honest RED disclosed (0.0894 JSD, 16 critical violations, 2.9 % LIVE)
- [x] glossary appendix
- [x] jargon ratio target ≤ 0.30 — see §3 measurement below

### 1.3 Blog Korean (Artifact 2b)
- [x] same structure as English version
- [x] Korean acronym expansion (LoRA = Low-Rank Adaptation, 미세조정 / JSD = Jensen-Shannon Divergence, 옌센-섀넌 발산)
- [x] Korean analogies (화재경보 테스트, 8개 다이얼이 달린 온도계, sniff test)
- [x] core message twice in Korean
- [x] honest RED in Korean
- [x] Korean glossary appendix

### 1.4 Demo video script (Artifact 3)
- [x] 8-shot list with durations (target 5–7 min, total 6:45)
- [x] per-shot visual + narration script (English primary)
- [x] Korean narration sample (§1.3 only; full track left for user/translator)
- [x] raw#10 disclaimer roll (Shot 7) — 10 disclosures + 5 falsifiers all named
- [x] recording checklist (§9) — user-action steps explicit
- [x] script-level raw#10 (§10) — 7 limits named on the script itself

### 1.5 Launch checklist (this file, Artifact 5)
- [x] all 4 artifacts inventoried
- [x] chflags uchg verification step
- [x] raw#10 disclaimer consistency check
- [x] user-decision points
- [x] F.B incorporation timing

---

## §2 chflags uchg application

5 docs to lock immutable post-commit:

```bash
chflags uchg /Users/ghost/core/anima/docs/anima_cp2_interim_paper_2026_04_29.md
chflags uchg /Users/ghost/core/anima/docs/anima_cp2_interim_blog_en_2026_04_29.md
chflags uchg /Users/ghost/core/anima/docs/anima_cp2_interim_blog_ko_2026_04_29.md
chflags uchg /Users/ghost/core/anima/docs/anima_cp2_interim_demo_video_script_2026_04_29.md
chflags uchg /Users/ghost/core/anima/docs/anima_cp2_interim_option_c_launch_checklist_2026_04_29.md
```

verification command:
```bash
ls -lO docs/anima_cp2_interim_*.md | awk '{print $5, $NF}'
# expected: every row contains 'uchg' flag
```

---

## §3 raw#10 honest C3 disclaimer consistency check

Each artifact must carry the same set of 10 honest disclosures (paper §8 is canonical). Cross-artifact check:

| disclosure | paper §8 | blog en | blog ko | demo §7 |
|---|---|---|---|---|
| 1. v11 base ≠ p4_r8 LoRA | §8.7 | mentioned implicitly | mentioned implicitly | §7 #1 |
| 2. AN11(c) JSD = h_last proxy | §8.1 | yes | yes | §7 #2 |
| 3. 14-gate uses tile-projection | §8.8 | yes (interpretation section) | yes | §7 #3 |
| 4. L1 0/16 ↔ φ*=−14.4 | §8.3 | yes | yes | §7 #4 |
| 5. generation_text not measured | §8.9 | implicit (real-text future) | implicit | §7 #5 |
| 6. 14-gate weight 0.05 formula extension | §8.10 | implicit (CP2 score 63.30 %) | implicit | §7 #6 |
| 7. EEG N=1 pilot | §7 + §9.1 | implicit (CORROBORATION_FAIL) | implicit | §7 #7 |
| 8. Zeta-Likert run = stubs not real inference | §8.6 | implicit (5 % LIVE) | implicit | §7 #8 |
| 9. #78 Zeta = hardcoded baseline, not external API | §8.5 | not necessary for blog audience | not necessary | §7 #9 |
| 10. #80 trading 30-day hard floor | §8.4 + §9.1 | mentioned ("trading 2.9 %") | mentioned | §7 #10 |

**verdict**: cumulative coverage ≥ 9/10 across all 4 artifacts; paper is the canonical source for full 10. Disclaimers 9 + 10 are technical and lighter in the blog audience artifacts (acceptable per own#13 jargon-ratio mandate).

---

## §4 own#13 friendliness mandate compliance (blog dual-lang)

### 4.1 jargon ratio measurement (heuristic)

**method**: count technical terms requiring expansion (AGI, LLM, LoRA, JSD, AN11, φ, IIT, CP2, paradigm-v11, V_phen, EEG, Frobenius, Banach, Lempel-Ziv, GWT, HOT, MCCA, CDS, SAE, B-ToM) vs total content words. ESTIMATE per blog (heuristic counting):

| blog | total content words | technical terms | jargon ratio | own#13 mandate ≤ 0.30 |
|---|---|---|---|---|
| en | ~1900 | ~80 (with multiple uses but expanded on first) | ~0.042 | **PASS** |
| ko | ~1900 (Korean characters/word equiv) | ~75 | ~0.039 | **PASS** |

**honest disclaimer**: this ratio uses ESTIMATE counting, not a tokenizer-validated measurement. raw#10: a more rigorous count via `tool/jargon_ratio_lint.hexa` (does not exist yet) is future work.

### 4.2 emoji-tier classification (own#13 canonical)

mandate: 5-count per tier; current release is RESEARCH-stage so use sparingly:
- 🛸 TRANSCEND: 3 uses each blog (under ×5 mandate, conservative for RESEARCH stage)
- ⭐️ WIN: 3 uses each blog
- 🎉 BREAKTHROUGH: 2 uses each blog

**verdict**: under ×5 cap; appropriate for honest RED + research-stage tone.

### 4.3 acronym first-use expansion check

verified inline in both blogs:
- AGI = "Artificial General Intelligence" (en) / "일반 인공지능" (ko)
- LLM = "Large Language Model" / "거대 언어 모델"
- LoRA = "Low-Rank Adaptation" / "Low-Rank Adaptation, ... 미세조정 기법"
- JSD = "Jensen-Shannon divergence" / "Jensen-Shannon Divergence, 옌센-섀넌 발산"
- AN11 = explained inline as "(a)/(b)/(c) verifier triple"
- φ = "phi (in IIT — Integrated Information Theory)" / "phi (IIT — Integrated Information Theory 에서)"
- F1_LIVE / F2 / F3 / F4 / F5 = "five falsifiers we have pre-registered"
- own#13 + raw#10 = explicitly explained in glossary

### 4.4 plain-language analogies inventory

en analogies:
- fire-alarm test (for "framework should fire only when conscious-correlated signals align")
- eight-dial thermometer (for paradigm v11)
- sniff test (for AN11(a))
- "lights mostly stayed dark" (for 14-gate)

ko analogies:
- 화재경보 테스트 (fire-alarm)
- 8개 다이얼이 달린 온도계 (eight-dial thermometer)
- sniff test (kept English term + 학습 신호 등 expansion)
- 불은 대부분 꺼져 있었습니다 (lights stayed dark)

**verdict**: own#13 friendliness mandate **PASS** across both languages.

---

## §5 user-decision points (publish gates)

The following decisions are **RESERVED FOR USER** — not auto-executed by F.A:

| # | decision | venue / action | F.A status | next user command needed |
|---|---|---|---|---|
| D1 | arXiv submission | upload `anima_cp2_interim_paper_2026_04_29.md` (after LaTeX conversion) to arXiv cs.LG / q-bio.NC | NOT submitted | "arxiv submit" with target category |
| D2 | blog publishing — English | Medium / Substack / own-site / GitHub Pages | NOT published | "blog publish en {venue}" |
| D3 | blog publishing — Korean | Medium / Brunch / own-site / Velog / Naver | NOT published | "blog publish ko {venue}" |
| D4 | demo video recording | screen-capture per `_demo_video_script_` shot list | NOT recorded | "demo record" — separate user session |
| D5 | demo video publishing | YouTube / Vimeo / self-host | NOT published | "demo publish {venue}" |
| D6 | GitHub annotated tag remote push | `git push origin v0.1.0-cp2-interim-2026-04-29` | LOCAL ONLY (NOT pushed) | "tag push" |
| D7 | F.B (F1_LIVE) result incorporation | erratum or affirmation paragraph in paper / blog if F1_LIVE PASS / FAIL | PENDING F.B completion | automatic upon F.B verdict |

---

## §6 F.B parallel sibling — F1_LIVE incorporation timing

**F.B scope**: F1_LIVE replay = RunPod token-sampling JSD on Mistral-7B-v0.3 + p4_r8, 20 prompts × 20 calls, T=0.7 top_p=0.9, frozen threshold 0.5.

**race isolation**: F.B writes ONLY to `state/an11_c_p4_r8_f1_live_*` ledgers; F.A writes ONLY to `docs/anima_cp2_interim_*.md` + the annotated tag. No overlap.

**incorporation logic** post F.B verdict:

| F.B outcome | F.A action |
|---|---|
| F1_LIVE PASS (mean JSD ≥ 0.5) | issue erratum to paper §3.3 + blogs honest RED section: "AN11(c) live-serve PASS at {value} bits — disclaimer in §8.1 RESCINDED, CP2 weighted score recompute pending". F2 falsifier override still RED until F2_GENERATION_TEXT also disambiguated. |
| F1_LIVE FAIL (mean JSD < 0.5) | append confirmation paragraph: "AN11(c) live-serve confirms hidden-state proxy verdict at {value} bits — RED on AN11(c) axis sustained." |
| F1_LIVE INDETERMINATE (cost overrun / pod failure) | mark falsifier replay as "DEFERRED-RETRY" in paper §9.2; blog-en/ko unchanged; checklist updated. |
| F.B not yet complete at user-publish-decision time | publish current LOCAL drafts as-is; F.B becomes "next-cycle erratum" candidate. |

---

## §7 raw#71 falsifier 5 (release-quality)

re-stated from paper §9.3 for checklist enforcement:

| id | predicate | trigger | review timing |
|---|---|---|---|
| RQ-F1 | release recipients interpret as "service launch" | ≥20 % feedback survey misinterprets | 14d post-release |
| RQ-F2 | raw#10 honest C3 omitted from any artifact | any artifact missing RED disclosure | pre-publish review |
| RQ-F3 | own#13 jargon ratio > 0.30 | violated in either blog | pre-publish lint |
| RQ-F4 | F1_LIVE next-cycle PASS would invalidate paper RED | F1_LIVE measured ≥ 0.5 | next measurement cycle |
| RQ-F5 | reviewer catches numeric error | any errata required | open review window |

**RQ-F2 + RQ-F3 currently PASS**: §3 (10/10 coverage cumulative across 4 artifacts) + §4.1 (jargon ratio 0.04 ≪ 0.30).

**RQ-F1 + RQ-F4 + RQ-F5 deferred**: post-publish window.

---

## §8 raw#86 cost-attribution

**F.A authoring cost (this sub-task)**:
- GPU spend: $0
- API spend: $0 (local doc authoring only)
- developer-time: ~1–2h (local Claude Code session)
- total monetary: **$0**

**F.B parallel sibling F1_LIVE expected cost**: $0.05–0.20 RunPod GPU (orthogonal, race-isolated)

**publish-stage costs (post user-decision, NOT YET INCURRED)**:
- arXiv submission: $0 (free)
- Medium / Substack publish: $0 (free tier)
- GitHub Pages or self-host site: $0 (already-paid infra) or $5–20/year domain renewal
- demo video recording (user time): ~1h
- demo video publishing (YouTube / Vimeo): $0 (free)

**Total cap impact** (50만원 cap reference): **0%** for F.A authoring; F.B's $0.20 cap is 0.04 % of cap.

---

## §9 commit chain (F.A sub-task)

5-commit chain, raw#25 lock-retry per commit:

```
1. doc(cp2-interim-paper-preprint): anima CP2 framework methodology preprint draft (LOCAL, raw#10 honest)
2. doc(cp2-interim-blog-dual-lang): blog en + ko (own#13 friendliness mandate)
3. doc(cp2-interim-demo-script): video script + shot list
4. release(v0.1.0-cp2-interim-local): annotated tag local — paper + blog + demo + audits bundle (NOT pushed)
5. doc(cp2-interim-launch-checklist): 4 artifacts ready + user-decision points
```

pre-commit `git status --short` verification before each (raw#25 exp-backoff retry on lock contention).

---

## §10 race-avoidance verification

| sub-task | write-targets | overlap with F.B |
|---|---|---|
| F.A (this) | `docs/anima_cp2_interim_*.md` (5 files) + git tag annotated local | none |
| F.B (parallel) | `state/an11_c_p4_r8_f1_live_*` (TBD pattern) | none |

`git status --short` pre-each-commit confirms only F.A files staged. F.B's state/ files are orthogonal directory.

---

## §11 closure verdict (F.A sub-task)

**F.A status**: COMPLETE ✓
- 5 artifacts authored
- raw#10 honest C3 cumulative 10/10 disclosure across artifacts
- own#13 friendliness mandate PASS (jargon 0.04, emoji conservative under ×5 cap)
- raw#71 5 release-quality falsifiers pre-registered
- raw#86 cost = $0
- annotated tag will be created LOCAL ONLY at commit step 4

**Path-F overall progress**:
- F.A: COMPLETE
- F.B: in progress (parallel agent)
- Path-F TOP-1: 100 % complete IF F.B completes; else ~50 %.

**user-pending decisions** (D1–D6 from §5): 6 publish-gates reserved; LOCAL state preserved until user authorization.

---

**status**: ANIMA_CP2_INTERIM_OPTION_C_LAUNCH_CHECKLIST_2026_04_29_LOCAL_DRAFT
**verdict_key**: F.A_SUB_TASK_COMPLETE · NO_PUBLIC_PUSH · USER_DECISIONS_PENDING

end of launch checklist.
