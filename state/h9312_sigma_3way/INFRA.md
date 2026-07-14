# INFRA BLOCKER (verdict 와 분리 · infra-wall-noneval)

**mini 의 hexa 툴체인이 stale** — 설치본 hexad v0.574.1 코드젠에 `read_f32_at` builtin 매핑이 없어
현행 origin/main `core/decode.hexa` 를 **컴파일 자체가 불가**(`call to undeclared function 'read_f32_at'`).
전역 `anima` 가 돌던 것은 캐시된 옛 바이너리 + **Jul-5 스테일 클론**(`~/.hx/packages/anima`,
`self_ctx_live` 자체가 없는 소스)이었기 때문 — 과학 천장 아님. (convergence: forge-dispatch-builtin-stale-embedded-hexad)

**우회(전역 불변)**: hexa-lang v0.769.0 prebuilt 를 프라이빗 디렉토리에 받아
`HEXA=<private>/hexa anima_kill …` 로 실행. 툴체인 prebuilt `runtime.a` 에 codegen 이 main 에 emit 하는
`hexa_ffi_dlopen/dlsym` 이 없어(빌드 구성 차) 링크 실패 → 동일 소스 계보의 libdl 재구현 shim 을
아카이브에 추가해 링크. **FFI 는 --opgrip($0 스칼라 no-decode) 경로에서 호출되지 않으므로 σ 수치에 무관.**
워크트리는 `hx install <worktree> --as anima_kill` (심링크 패키지) 로 canonical 커맨드 채널 유지 —
전역 `anima`/`~/.hx/packages/anima` 는 건드리지 않았다.

프라이빗 툴체인(140MB)은 결과 확보 후 삭제. 재현 시 위 절차 반복.
