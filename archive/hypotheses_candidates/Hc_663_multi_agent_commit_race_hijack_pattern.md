---
id: Hc_663
slug: multi-agent-commit-race-hijack-pattern
title: Multi-agent race-hijack pattern — ce747b5e7 incident 가 4-file mixed-intent commit (F3 intended 2 file + F1 hijack + F6 hijack), boundary 격리 위반
domain: anima-meta
status: candidate-unverified
source_doc: docs/multi_agent_race_audit_2026_05_01.md
source_lines: 1-68
promoted_at: 2026-05-11
linked_h: ce747b5e7 (Author: dancinlife), F1 audit 867392918, F6 synthetic fixture fingerprint
notes: 직전 3 commits (43b3cee89, 867392918, 7fc8c7e87) 모두 single-file single-intent. ce747b5e7 만 4-file mixed. 18-19분 race window.
---

## Hypothesis
Multi-agent concurrent git work 에서 race-hijack 이 single-file boundary 격리 위반 패턴 형성. F3 author 가 2-file plv_preserving commit 의도 but 867392918 (F1 audit, plan reframe 권고만) 후 plan 본문 unstaged 18-19분 잔존 → F3 commit 에 부수 staging 으로 hijack. git log --follow 가 semantic mismatch 영구 박힘.

## Falsifiable Tests
- F-race-1: 다른 4-file mixed-intent commit 발견 → 일반 패턴 (단일 incident X)
- F-race-2: pre-commit hook 으로 git status 진단 후 stage warning 가 race 차단
- F-race-3: 18-19분 race window 가 일반적 (다른 incident 에서 confirm)

## Migration TODO
- [ ] pre-commit hook: 의도하지 않은 staged file warning
- [ ] git add 전 status snapshot mandatory
- [ ] author intent 명시 commit message 검증
- [ ] multi-agent race window 측정 (typical/median)
