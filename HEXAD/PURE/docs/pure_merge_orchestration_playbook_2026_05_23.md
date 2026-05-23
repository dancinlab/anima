# PURE stacked PR 머지 오케스트레이션 플레이북 (2026-05-23)

> 목적 — PURE 라인 4-9 개 stacked PR 을 다운스트림 고립 없이 안전 랜딩하기 위한 절차.
> 범위 — PURE 만. 본 세션 scope ([[feedback-hexad-pure-session-scope]]).
> 형식 — `@D g3` ASCII 다이어그램 + `@D g4` <200 LoC.

## §1 PR 토폴로지

모든 sibling PR 의 base 가 `#220` 으로 동일한 **평행 fan-out** (직렬 체인 아님).

```
                 origin/main
                      │
                      ▼
              ┌──────────────────────────┐
              │ PR #220 base             │
              │ refactor/hexad-v3-to-    │
              │ pure-rename              │
              │ (V3 → PURE rename · 16 f)│
              └─────────────┬────────────┘
                            │
       ┌──────┬──────┬──────┼──────┬──────┬──────┬──────┐
       ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
  PR #228  #229   #233  <agtA> #240   #264   #265  <diag>
  Track1  B증류  C head_g  A  eval  F4    launcher  ...
  E2/E3                  커리큘럼 harness 가정    common
                                    │
                                    ▼
                                 PR #263
                                 F8 strip
                                 parity
```

추가로 head_g activation logger, register collapse detector 등 진단용 sibling 도 동일 base.
PR #263 은 유일하게 base ≠ #220 (base = #240 eval harness) — eval harness 의 child.

## §2 머지 순서 (least-friction first)

1. **#220 base** 우선 머지. 기계적 rename, semantic conflict 0. `cdo-validate` 이미 GREEN.
2. #220 머지 직후 모든 sibling 이 `origin/main` 에 rebase. rename + 각 spec path-disjoint → 충돌 0 예상.
3. Sibling 우선순위 (impact 큰 것부터):
   - **#228 Track 1** — AXIS_MAP 결정 트리의 첫 step (corpus reburn E2/E3).
   - **#229 B 증류** — Track 1 fallback.
   - **#233 C head_g objective** — Track 1 fallback.
   - **(agent A 커리큘럼)** — B∥A∥C 평행 트리오 완성.
   - **#240 eval harness** — 재사용 infra (5-lang multilingual probe SSOT).
     - **#263 F8 strip parity** — #240 머지 후 rebase (eval harness child).
   - **#264 F4 가정 surfacing** — closure rejection criterion docs (base=#220).
   - **#265 launcher _common** — launcher SSOT skeleton (base=#220).
   - **(agent head_g logger)** — 로컬 진단.
   - **(agent register collapse detector)** — 로컬 진단.

## §3 Rebase 레시피 (sibling PR 별)

```bash
git fetch origin main
git checkout feat/pure-<name>
git rebase origin/main
# Resolve conflicts if any (expected: zero, since #220 rename was mechanical)
git push --force-with-lease origin feat/pure-<name>
gh pr edit <N> --base main  # switch base: refactor/hexad-v3-to-pure-rename → main
```

## §4 충돌 매트릭스

| PR pair | Same-path conflict? | Resolution |
|---|---|---|
| #220 × #228 | NO (`HEXAD/PURE/spec/` + `launchers/` 신규 파일) | trivial |
| #220 × #229 | NO (동일 패턴) | trivial |
| #220 × #233 | NO (동일 패턴) | trivial |
| #228 × #229 | NO (서로 다른 spec+launcher 쌍) | trivial parallel |
| #228 × #233 | NO | trivial parallel |
| #229 × #233 | NO | trivial parallel |
| <agent A> × #228/#229/#233 | NO (다른 spec+launcher 이름) | trivial |
| #240 eval × all | maybe (launcher 가 eval probe path 사용 시 — 단 본 cycle 의 eval harness PR 은 신규 파일만 ADD) | rebase 시 review |
| #240 × #263 | NO (#263 = child stack, eval harness API surface 만 touch) | sequential merge (#240 먼저) |
| #220 × #264 | NO (`HEXAD/PURE/docs/` F4 docs 만 신규 ADD) | trivial |
| #220 × #265 | NO (`HEXAD/PURE/launchers/_common.hexa` + `ENV_CONTRACT.md` 신규 ADD) | trivial |
| #265 × #228/#229/#233 | maybe (launcher 들이 `_common.hexa` import 채택 시) | #265 머지 후 sibling rebase 시 import 추가 |
| <agent head_g logger> × <agent register collapse detector> | maybe (양쪽 모두 `HEXAD/PURE/tools/` touch 가능) | rebase 시 review |

## §5 PR 별 pre-merge gate

- `cdo-validate` GREEN (PR #201 이 repo-wide stale JSON 해결).
- spec + launcher 각 <450 LoC (`@D g4`).
- 모든 emit `.sh` 에 대해 `bash -n` PASS (각 launcher 가 기계적으로 검증).
- 신규 `.py`/`.sh` 커밋 금지 ([[feedback-hexa-only-authoring]] — hexa-only authoring).

## §6 Post-merge 정리

- `gh pr merge <N> --squash --delete-branch` 로 머지 + 브랜치 삭제.
- [[project-v3-path-closed]] 메모리 갱신: V3 CLOSED → PURE REOPENED with fallback recipes spec-merged.
- [[feedback-hexad-pure-session-scope]] 메모리 갱신: OPEN PURE PR 전부 머지 → 다음 cycle = 실제 fire dispatch.

## §7 롤백 안전성

- 각 PR 은 main 위의 SEPARATE squash-commit. `git revert <sha>` 로 sibling 영향 없이 단일 롤백 가능.
- `main` force-push 금지. 머지된 커밋 amend 금지.
- launcher 는 gitignored workspace dir 로 `.sh` emit. launcher 실제 invoke + dispatch 전까지 production code path 0 touch.

## §8 Cross-references

- `HEXAD/PURE/AXIS_MAP.md` 결정 트리 → spec PR.
- [[feedback-hexad-pure-session-scope]] 메모리.
- `@D g4` stacked PR governance.
- `@D a_substrate_native_speak` — 어느 PR 도 anima emit path 미터치 → 안전 랜딩.

## §9 C3 (Honest carve-outs)

1. CI `cdo-validate` 가 현재 GREEN 이라도 sibling agent 가 도입한 신규 JSON artifact 가 stale 화될 가능성 — rebase 시 재실행 필수.
2. 본 플레이북은 본 cycle 의 7-9 개 sibling PR 까지만 검증. 10 번째 이상 sibling 은 별도 검토.
3. `gh pr edit --base` 가 실패하면 (rare) PR 새로 열고 close-with-comment 로 승계.
