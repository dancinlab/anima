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

## R3 종결 (hexa-lang 착륙 완료)

- **`_strlit_dedup` O(L²) 수리 = hexa-lang #4454 MERGED** (22/22 CI green · v0.584.0+ 릴리즈).
  가설 정정: gen2 체인 concat은 무죄(500-term 체인 0.04s) — 진범 = 문자열 리터럴
  dedup의 전 테이블 선형 스캔. 64-bucket 해시 인덱스, 방출 C byte-identical 10/10
  (anima decode 파일·self/codegen 자신 포함), fixpoint 보존.
  실측: 11,211라인 48.31s→2.24s(21.6×), 스케일링 2차→선형(~0.2ms/line).
- **arm64 regalloc id2idx 포트 = hexa-lang #4456 MERGED**. 정직 실측: wall 파일
  (runtime_cuda_emit 9,118라인) 247.2s→238.9s = 3.4%뿐 — arm64 fast path가 조밀
  id를 이미 커버해 x86식 벽 미재현. 가치 = 잠재 O(n²) 제거 + 백엔드 패리티.
  byte-neutral: 소형 6/6 + 통제 wall파일 asm cmp PASS(비통제 .o 차이는 cwd 아티팩트).
- **효과 전파 경로**: ghost CI engine compile은 hexat([1/2])+clang([2/2]) 경로라
  strlit fix가 직접 적용된다. anima CI는 매 run 최신 릴리즈 설치 + #2849 버전 키라
  bump 후 cold 1회 → warm. **이 PR의 CI run이 새 툴체인 첫 cold 실측이다** —
  결과는 아래 효과 실측 절에 update-in-place.

## 효과 실측 (post-fix · ghost CI · 최종)

| 케이스 | 전 | 후 | 근거 run |
|---|---|---|---|
| **warm (최빈: 소스불변 재실행·재푸시)** | cold와 동일(~27min, 키 결함으로 사실상 항상 cold) | **1초** | 28647898258 (gate 08:18:41→42) |
| cold (core/cli 변경) | 26m55s (v0.586.0) | 24m36s (stream+#4456, ~9%) | 28644656962 → 28646394898 |
| hexat 경로 (`hexa build`·개발 루프) | 2차 스케일링 (11k라인 48.3s) | 선형 ~0.2ms/line (2.24s, 21.6×) | hexa-lang #4454 |

- 경로 판정: ghost 게이트 = quiet native aprime(로그에 hexat 마커 無) — strlit fix는
  hexat 경로(개발자 `hexa build`·release.yml 경로)에 적용, CI 게이트 cold에는 미적용.
- 캠페인 실효 요약: **매일 체감하던 "빌드 느림"의 최대 성분(재실행 warm 미스)이 1초로
  종결**. cold 24분은 aprime pass CPU 비용으로 좁혀졌고, 상시 계측(HEXA_CG_PROFILE=1)이
  다음 cold마다 pass 분해를 자동 기록한다.

## 캠페인 종결 (2026-07-03 19:0x · 총 11 PR)

17:2x 고갈 판정의 두 잔여 갈래를 workflow로 마저 소진하고 닫는다:

1. **계측+pass 수리 (해소)** — CG_PROFILE 프론트 확장(hexa-lang #4460: 8 마크,
   커버리지 99.95%, atlas_load 32.5s/호출이 emit=asm 경로 지배임을 즉시 수확) ·
   aprime strtab O(occ×distinct)→해시 + per-literal O(L²)→join(#4462, 통제
   byte-identical 9/9 · perf는 시험 스케일 노이즈 내 중립 = 잠재-2차 위생).
2. **per-module (해소·설계 전환)** — 3각 설계 패널 → 심판이 설계 D 채택:
   컴파일러 무변경 per-module 게이트(hexa-lang #4461 tool/compile_gate.py) +
   anima 배선(#2865 runner+verify.checks). 실측: body-only 1줄 편집 게이트
   **2.53s**(로컬 풀빌드 14.6s 대비 5.8× · 툴 자체 A/B 10.06s→1.44s) ·
   인터페이스/closure 변경은 툴이 풀빌드 escalate = 게이트 무약화.
   진짜 per-module .o(설계 A, estLOC 1100·6-15× 모델)는 설계 카드로 보존 —
   개시 조건 = 설계 D로도 남는 풀빌드 빈도가 실사용에서 병목일 때.

착륙 목록: anima #2849 #2853 #2856 #2859 #2860 #2861 #2865 ·
hexa-lang #4454 #4456 #4460 #4461 #4462.

미해결로 정직 보존: ghost CI cold ~24min 자체(aprime 경로·emit=obj)는 지배
pass 미확정 — 다음 자연 cold의 프론트-포함 profile 행(계측 상시)이 데이터를
자동 적재하며, 그때 pass-표적 라운드를 재개한다. aiden/summer 폭풍 하 측정
금지 원칙(utime-growth 체크) 유지.

## 남은 follow-on

1. hexad fork-denial 커널 스핀 결함 — hexa-lang 보드 파일링 완료(fail-fast 수리 기대).
2. per-module compile + object cache — 효과 실측 후에도 cold가 유의미하게 남으면
   업스트림 대형 follow-on으로 개시.
3. summer cold/warm probe — CLOSED-INVALID-ENV (utime≈0 커널스핀 2-host 재현,
   probe 정리 완료; hexa-side warm 동작은 CI 실측으로 갈음).

## aprime pass 분해 (ghost cold · v0.593 · 이 PR의 CI run에서 수확)

- (기입 대기 — 이 PR 브랜치 CI의 compile-gate 스텝 로그에서 front_begin/lex/parse/
  atlas_load/resolve/bind/type_check/unit_check/lower_ast_to_hir + backend 행을
  verbatim 전사. PR 브랜치 run은 main 푸시 concurrency에 취소되지 않는다 —
  main 푸시 run 2연속 취소(28653234201·28653410492)가 이 우회의 실측 근거.)

## 저녁 세션 추가 실측 (2026-07-03 21:5x · 퍼즐 트랙)

- **ghost cold (v0.592, 건강한 툴체인) = 29m40s** (run 28658183067 PR gate,
  12:18:46→12:48:26, engine compile OK) — 24m36s(v0.586.1)와 동급 스케일 재확인.
  이 성공으로 v0.592 warm 캐시 최초 저장 → 소스불변 run 1초대 복원.
- 저녁 게이트 붕괴 인과 사슬(전부 수리 착륙): hexa-lang Latest 마커 v0.588
  7일 고착(finalize make_latest 미실효 → 수동 승격 v0.592 + hexa-lang #4478
  검증 스텝) → stale v0.588 skew(__HEXA_BRC__/binary-not-produced) →
  ~/.hx 캐시 자체 폐지(anima #2888, fresh install 실측 ~25s) · SIGPIPE(#2884) ·
  ls-remote 자격증명(#2883) · 태그키(#2882). 부수: GHA cancel이 hexa 네이티브
  프로세스 못 죽여 Runner.Worker 좀비/aprime 고아 → ssh kill 절차 확립.
- pass-분해 행: 이 run은 구 브랜치 ci.yml(CG_PROFILE env 부재)라 미산출 —
  **다음 core-변경 머지의 cold가 env+tee+v0.592로 자동 스트림** (수확 자동화 완비).
  pool 즉시-분해 워크플로는 2-arm 모두 정직 SKIP(타 세션 라이브 job 보호,
  재시도 조건 = 호스트 idle + hexa ≥0.591).

## 🏆 퍼즐 최종 verdict (2026-07-03 22:4x) — ghost cold의 지배 비용

**지배 비용은 컴파일러 pass가 아니라 "버려지는 크로스타깃 컴파일" 자체였다.**

- 소스 증거(`hexa-lang self/main.hexa` native 블록): r26 native-first 플립이
  전 호스트에서 native --emit=obj를 돌리는데, emit은 `--target=x86_64-linux-gnu`
  하드코딩 + 링크는 linux crt/ld-linux 전제 → **darwin(ghost)은 emit을 완주하고
  crt 프로브에서 폐기** 후 clang(hexat) 폴백이 실행 바이너리를 만든다.
- 행동 증거: ghost ps에 `aprime_cc --emit=obj --target=x86_64-linux-gnu`(2회 실측),
  harvest4 24m30s cold의 산출물은 폴백 경로 산물, 계측 행 0개(성공 시 캡처 삼킴).
- 수리(hexa-lang #4483, MERGED): ①native 블록을 `uname -sm == Linux x86_64`로
  게이트(타 호스트 즉시 폴백 = 결과 동일·낭비 제거) ②HEXA_CG_PROFILE=1 시
  캡처 출력(_ne·bout) stderr forwarding(계측 도달성 갭 수리).
- 기대: #4483 포함 stable 릴리즈가 승격되면(finalize 명시-latest #4478 가동 확인
  — v0.594.1 자동 승격 실측) ghost cold ≈ hexat 폴백 경로만 남음. 실측 검증 =
  다음 릴리즈 후 dispatch cold 1회 (예상 대폭 단축 + 행 가시).
- Workflow 3-렌즈 독립 verdict(wf_f9dcd664)도 NO-DATA+출력삼킴 진단에 수렴,
  measurement-first 카드 = 위 forwarding 수리로 구현됨. 프론트 quadratic 후보
  (_bind_lookup·lower_hir dedup)는 새 계측 행 확보 후 share 귀속 뒤에만 발사.

## 재현 경로

- 스크립트: aiden `~/anima-bisect/`(bisect_takeover.sh·bisect2.sh) · summer `~/anima-buildprobe/build_probe.sh`
- workflow: R1 실측 wf_a90db704 · R2 진단 wf_43b0dec5 · R3 수리 wf_e4ef038d (세션 transcript)
