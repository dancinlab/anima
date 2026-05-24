# MODERNIZE — log

Append-only history sister of `MODERNIZE.md`. Each entry `## <ISO timestamp> — <header>` (newest on top); body = `- [x]`/`- [ ]` checkbox tasks.

## 2026-05-25T03:00:00Z — serving/ web batch (3 files, explicit-main removal, build-verified)

- [x] `serving/avatar_render.hexa` · `serving/sparse_dispatcher.hexa` · `serving/sparse_dispatcher_live.hexa` — explicit `main()` 제거 → 전부 **build PASS** (avatar_render run exit 0)
- [!] **`.length` 클래스 = 2종 false-positive 확정**: (1) JS/HTML 문자열 리터럴 (`verts.length` 등 생성 JS), (2) **struct field** `req.length` (메서드 아닌 필드 접근). 진짜 deprecated `.length()` 메서드(→`.len()`)는 드묾(alm_bf16 만 확인). → census 의 `.length` 6 은 대부분 false-positive, 실 break 는 explicit-main
- [!] `fabs`: sparse_dispatcher 는 **자체 `fn fabs` 정의** 보유 (mangle 일관 = 정상). fabs census 189 중 다수가 self-def (정상) — 실 오용은 def 없는 호출만 (#429 6건 처리)
- [x] 누적 modernize: avatar_webtoon(#430) + avatar_render + sparse_dispatcher×2 = serving/ web 4 파일 build-pass
- [ ] M5 explicit-main 잔여 (~715) — per-file build-verify, multi-session

## 2026-05-25T02:45:00Z — M1 census + 첫 파일 modernize (avatar_webtoon) + .length false-positive 발견

- [x] M1 active-dir census (archive/legacy/state 제외): explicit-main **719** · fabs **188** · .length **6** · nan/inf **1**
- [x] 근본 확정: interp retire → interp-era 코드(explicit main + top-level)가 compiled hexa-strict 에서 대량 build-fail
- [x] **첫 파일**: `serving/avatar_webtoon.hexa` — explicit `main()` 제거 → **build + run PASS** (exit 0). per-file modernize 패턴 확립
- [!] **핵심 교훈**: `.length` 6파일 census 중 avatar_webtoon `.length` 은 **JS 문자열 리터럴**(`seq.length` in embedded JS, L428) = false-positive. blanket `.length→.len()` sed 가 생성 JS 손상시킴 → 복원, main-only fix. **per-class blanket sed 금지, 실 hexa 구문만 + per-path baseline 가드**
- [!] 6 `.length` 파일 전부 explicit-main 동반 (single-break 없음) → per-file 단위 필수
- [ ] M5 explicit-main sweep (719) — multi-session, per-file build-verify
- [ ] M3 .length 실-hexa만 · M4 nan rename — per-file

## 2026-05-25T02:30:00Z — 도메인 신설 + raw census

- [x] MODERNIZE.md scaffold · @goal (active .hexa build-pass on hexa-strict) · milestones · honest_limits
- [x] raw census (worktree 제외): explicit-main 807 · fabs( 189 · .length 6 · nan/inf 1
- [x] 발견 모태: STDLIB abs_f 루프 — #426/#427 broken fabs 출하를 per-path baseline infra(#801)가 노출 · #429 선례
