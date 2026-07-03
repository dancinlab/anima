# anima CI 병목 속도개선 — 측정 verdict + 레버 착지 현황 (2026-07-03)

측정 = hexa-lang 세션 workflow wf_0f971ad1-d9b (정찰 4축+합성 · 5 에이전트 · 오류 0 · 수치 전부 gh api/ssh 캡처).

## ★ 헤드라인 — 계산이 아니라 라우팅·기아·고아가 시간을 먹는다

- **engine 고래 1개**: 'engine compile + gates + smoke (darwin-arm64)' — cloud cold 중앙값 35.8분(n=94) · cloud **warm 4.1분**(n=8) · ghost cold ≥46-50분.
- **ghost-anima 역대 0/6 green** — #2816("빠른 ghost") 전제가 한 번도 성립한 적 없음.
  - 표층: cold가 50.3분 타임아웃 캡을 침 → Post-Cache save 스킵 → warm 영영 미시딩(닭-달걀).
  - **진범(직접 측정 · 합성의 v0.556.0 캐시오염 귀속은 기각)**: `~/.hx/bin/self`가 5/27자 **고아 실디렉토리**(884파일) — BSD `ln -sfn`이 실디렉토리를 교체 못하고 내부에 중첩 링크(`self/self`)를 만들어 fresh_install이 성공으로 위장, 리졸버는 5주+ stale runtime.h(forge gelu 선언 0)를 계속 읽음 → clang implicit-declaration 급사.
- **busy-blind 픽커**: 한 오전에 engine 런 9개가 busy ghost 뒤 30-73분 큐(~450 큐-분), cloud는 큐 2-3초.
- **main 검증 기아**: per-ref 그룹의 PENDING 1개 제한 → 24h에 main-push 77/92가 잡 0개로 취소 · 검증 지연 93분+.
- **릴리스 7일 동결**: release.yml hashFiles dangling-symlink(61/62 실패 · v3.57.2 동결 vs 태그 v3.101.3) — ci.yml엔 있던 `!core/phi/quantum_types.hexa` 제외가 release.yml에 누락(키 drift).
- **좀비 런**: 머지-완료 브랜치 대기 런 9개가 darwin 슬롯 ~180-300분/일 점유.
- 같은 날 선착지 fix 2건은 실측 유효: engine path gate(docs-PR 39-46초 완주) · PR cancel-in-progress(cloud 큐 74.8분→2초).

## 착지 현황

| 레버 | 내용 | 착지 |
|---|---|---|
| 2 | release.yml hashFiles 제외 포팅 (7일 동결 해제) | ✅ #2879 MERGED · 검증=다음 릴리스 런 발행 |
| 4a | 좀비 9건 일소 (gh run cancel) | ✅ 완료 |
| 1 | busy-aware 픽커 (hexa-lang 8d3929bf0 포트 · ghost busy→cloud 바운스 · mini는 ghost-offline 전용 유지) | PR #2880 |
| 3 | main per-commit 그룹 + engine 잡-레벨 per-ref keep-latest | PR #2880 |
| 4b | merged-PR zombie 가드 (경로 게이트 병합 · fail-open) | PR #2880 |
| — | ghost 고아 수리: `~/.hx/bin/self` 실디렉토리 제거→앵커 심링크 복원(gelu 3 확인) + warm 시드 | ✅ 수동 완료 · 시드 진행 |
| — | **upstream 근본fix**: install.sh 앵커 non-symlink 잔재 선제거 | hexa-lang PR #4473 (convergence install-sh-1) |

## non-levers (기각 요지)

ccache(엔진 cold의 ~15%뿐·지배 비용은 aprime_cc 코드젠) · autotag 스로틀(이미 release-worthy 디바운스 有) · 추가 경로필터(당일 선착지) · 유료 러너(금지) · engine required 승격(큐 병리를 머지 경로에 수입) · 게이트 약화(금지) · main cancel-in-progress 확장(문제는 반대 — pending 기아).

## 잔여 큐

- 레버 6(cheap ubuntu 4잡 required 승격 — 현 보호=리뷰 1승인뿐·CI는 사실상 advisory): **사용자 결정 필요**(머지 플로우 변경).
- warm 수명 = hexa 버전 키에 묶임(릴리스 bump→cold 회귀·hexa-lang #4466 coalesce가 완화) — 주기 재시딩 vs 키 전략은 시드 검증 후 판정.
- mini-anima 동일 고아 잔재: **청정 확인**(2026-07-03 — 양 앵커 정상 심링크 · 중첩 없음).
