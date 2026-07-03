# anima engine compile 속도 root-cause 실측 (2026-07-03)

## 질문
CI `engine compile + gates + smoke` 잡의 cold compile ~12.7min — 시간이 어디로 가는가?

## ⚠️ 측정 정정 (11:39 · verdict-integrity)

R2 workflow(wf_43b0dec5) 라이브 진단이 **aiden 측정의 대부분을 무효화**했다:

- aiden의 `hexad build --c-only` probe들(probe_4·probe_1)은 1시간 내내 **utime=0**
  (유저스페이스 명령 0개) · stime-only 8-12% CPU · VmRSS 1.5MB · 출력파일 미오픈 ·
  자식 프로세스 무 — **컴파일러 단계에 진입한 적이 없다.** rc=124 "타이밍"은
  codegen 측정으로 무효.
- 호스트 상태: 13.3GB `hexa_run` v0.548 + aprime_cc 3개(각 1.9-3.1GB, >1h)가
  memory-cgroup 스로틀(`mem_cgroup_handle_over_high`·`folio_wait_bit_common`)
  + 스왑 6.2GB로 상호 교착. earlyoom `--prefer '^(hexa|hexad|...)'` 활성.
- 부수 발견(업스트림 결함 후보, hexa-lang 보드 파일링 완료): 자식 spawn이
  거부될 때 hexad 드라이버가 무진행·무에러 커널 스핀으로 무한 대기하는 정황.

## 유효로 남는 실측

| 측정 | 호스트 | 값 | 스코프 |
|---|---|---|---|
| 합성 codegen 스케일링 (단순 fn) | mini | 0.09→0.35s (451→3,601라인) | 유효 — 선형 ~0.1ms/line |
| 방출 C 크기 (실 closure) | aiden | 28,555 lines / 1.5MB | 유효 (probe_full은 완주해 C 산출) |
| probe_full codegen wall (07:45→08:15 ≈32min) | aiden | 참고용 | 스로틀 호스트 — 상한만 의미 |
| clang -O2 / -O0 (방출 C) | aiden | 116.4s / 103.2s | 참고용(경합 부풀림 가능) · O레벨 무의미 판정은 유효 |
| CI cold compile | ghost (전용 darwin 러너) | ~12.7min | **실사용 기준값** |
| release.yml 자체 기록 | macos CI | install 29s vs aprime_cc ~16.5min | **codegen 지배의 깨끗한 교차 확증** |

closure 자체는 작다: repo 8파일 22,818라인(최대 `core/engine_cli.hexa` 13,705) + stdlib 2파일.

## Verdict (정정 반영)

- **병목 = hexa 측 codegen(transpile/aprime) 지배** — 근거는 aiden이 아니라
  release.yml의 깨끗한 CI 기록(29s vs ~16.5min)과 ghost 12.7min. 유지.
- **"~270x 병리" 배율은 UNVERIFIED** — aiden 스로틀 오염. 깨끗한 배율은
  idle 호스트 재측정 필요(follow-on ①).
- **clang -O 레벨은 레버 아님** (O2↔O0 delta 13s) — 유지.
- **`engine_cli.hexa` 파일 분할은 현재 무효** — toolchain이 closure 전체를 단일 TU로
  확장하므로 repo 파일 배치는 wall-clock에 영향 없음 (per-module compile 후 재평가).
- **소스 수준 O(n²) 사실들은 측정 오염과 무관하게 유효** (hexa-lang recon, file:line):
  ① `gen2_expr` 체인 문자열 O(k²) — `self/codegen.hexa:5301`; `+`체인만 평탄화,
     `||`/`&&`체인(anima 코드 패턴) 무평탄화; repo 내 `bench_contains_chain_scale.hexa`가
     N=400→14.7× 초선형 자체 입증.
  ② arm64 regalloc 선형 프로브 — x86_64는 #3712 `id2idx` O(1)로 수리,
     arm64(`compiler/codegen/arm64_darwin.hexa:537,1048-1066`) 방치 = ghost darwin CI 직결.
  ③ strlit dedup O(n²) · ④ per-fn declared-names O(lets²) · ⑤ lambda capture 재귀
  ⑥ whole-TU IR 상주 10-16GB (per-module 캐시 무 — 전량 단일 TU).
- **CI warm-cache 키 결함 (PR #2849로 수리 완료)**: 버전 미포함 키 → toolchain
  bump + 소스 불변에서 exact-hit 복원(무용) → cold → 재저장 스킵 = 영구-cold.

## 진행 중인 수리 (R3 · hexa-lang 격리 worktree)

- `perf/arm64-regalloc-id2idx` — #3712 reference-match 포트 (byte-identical 게이트)
- `perf/gen2-chain-flatten` — 체인 평탄화 일반화 (방출 C byte-exact 게이트 + bench 전후)

## 남은 follow-on

1. idle 호스트(또는 렌트 pod)에서 깨끗한 codegen 배율 재측정 → 이 파일 update-in-place.
2. hexad fork-denial 커널 스핀 결함 — hexa-lang 보드 파일링 완료(fail-fast 수리 기대).
3. summer cold/warm probe — INDETERMINATE (RUN1이 I/O 웨지에 익사, 웨지 해소 후 회수).

## 재현 경로

- 스크립트: aiden `~/anima-bisect/`(bisect_takeover.sh·bisect2.sh) · summer `~/anima-buildprobe/build_probe.sh`
- workflow: R1 실측 wf_a90db704 · R2 진단 wf_43b0dec5 · R3 수리 wf_e4ef038d (세션 transcript)
