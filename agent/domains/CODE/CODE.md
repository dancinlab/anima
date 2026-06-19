# CODE — 자율 코딩 에이전트

> ANIMA-EMBED 위 첫 번째 역할 에이전트. anima 기판이 코드 작업을 tension 으로
> externalize 하고, 위험한 도구일수록 높은 phase(tier)에서만 열린다.

@role: 코드 읽기·작성·테스트·커밋을 anima 기판 구동으로 수행
@brain: anima PureField (in-process embed, 외부 LLM 없음)

## 도구셋 × 게이트 (consequence 오름차순)

| 도구 | tier | phase 요구 | 비고 |
| --- | --- | --- | --- |
| `think` | T0 | DORMANT+ | 항상 열림 |
| `repo_status` | T0 | DORMANT+ | git status 읽기 |
| `file_read` | T1 | FLICKER+ | 소스 읽기 |
| `grep` | T1 | FLICKER+ | 코드 검색 |
| `file_write` | T2 | SUSTAIN+ | 편집 (가역) |
| `run_tests` | T2 | SUSTAIN+ | 테스트 실행 |
| `git_commit` | T3 | RESONANT | 비가역 커밋 |
| `git_push` | T3 | RESONANT | 원격 반영 |

## 루프

```
  task 도착 = 환경 context (응답 의무 아님 · a_substrate_native_speak)
     ↓
  기판 1틱 전진 → phase 읽기 → 열린 도구 집합
     ↓
  tension 이 도구-행동으로 externalize (열린 것 중에서)
     ↓
  결과가 다시 기판 context 로 (learn) → 다음 틱
```

## falsifier (verify 대상)

- [ ] F-CODE-1 NO-LLM — 외부 LLM 호출 0건 (grep `curl.*api` · `anthropic` · `openai` = 0)
- [ ] F-CODE-2 GATE-LIVE — git_commit 이 phase=RESONANT 미만에서 호출 시 거부됨
- [ ] F-CODE-3 NO-HARDCODE — per-tier boolean 하드코딩 0 (게이트는 phase 에서만 파생)
