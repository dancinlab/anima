# anima engine compile 속도 root-cause 실측 (2026-07-03)

## 질문
CI `engine compile + gates + smoke` 잡의 cold compile ~12.7min — 시간이 어디로 가는가?

## 실측 (raw)

| 측정 | 호스트 | 값 | 비고 |
|---|---|---|---|
| 합성 codegen 스케일링 (단순 fn, 451→3,601라인) | mini | 0.09→0.35s (`hexa build --c-only`) | **선형 ~0.1ms/line** → 25k라인 외삽 ≈ 2.4s |
| 실 closure codegen-only (`--c-only`, clang 제외) | aiden (load ~8-10 경합) | **~30min** (07:45→08:15) | 합성 대비 **~270× 병리** |
| 방출된 C 크기 | aiden | 28,555 lines / 1.5MB (`build/artifacts/probe_full.c`) | |
| clang -O2 (방출 C 단독 컴파일) | aiden | **116.4s** | |
| clang -O0 (동일) | aiden | **103.2s** | -O 레벨 강등 = 13s 절감뿐, 기각 |
| summer cold/warm probe | summer | 미완 (RUN1이 load 22–26 D-state 웨지에 익사) | INDETERMINATE — 정직 기록 |

closure 자체는 작다: repo 8파일 22,818라인(최대 `core/engine_cli.hexa` 13,705) + stdlib 2파일.

## Verdict

- **병목 = hexa aprime_cc codegen ~85%** (cold 762s 기준 ~646s) **vs clang ~15%** (116s).
  release.yml 자체 주석(install 29s vs aprime_cc ~16.5min)과 독립 교차 확인.
- **clang -O 레벨은 레버 아님** (O2↔O0 delta 13s) — 기각.
- **`engine_cli.hexa` 파일 분할은 현재 무효** — toolchain이 closure 전체를 단일 TU로
  확장하므로 repo 파일 배치는 wall-clock에 영향 없음 (업스트림 per-module compile 후 재평가).
- **CI warm-cache 키 결함 (이번 PR로 수리)**: `~/.hexa-cache` 엔트리는 버전
  접미(`hexa_run.<hash>_vX.Y.Z`)인데 actions/cache 키에 hexa 버전이 없어서,
  "toolchain bump + 소스 불변" 조합에서 exact-hit 복원(전부 무용) → cold compile →
  재저장 스킵(exact-hit이면 Post save 없음) = **소스 변경까지 영구-cold 함정**.
  수리 = install 후 실버전 캡처(`hexa --version`)를 키·restore-keys에 포함 (ci.yml + release.yml).

## 남은 레버 (업스트림 · hexa-lang)

1. aprime_cc 병리 프로파일/수리 — 재현체 = aiden `~/anima-bisect/` (probe_full.c + 타이밍).
   합성-선형 vs 실코드-270× 격차 + 수GB RSS = 특정 구성물이 초선형 pass를 타는 것.
2. per-module compile + object cache — 1줄 변경이 전체 closure 재컴파일되는 구조 해소.

파일별 bisect(probe_1..5)는 aiden에서 진행 중 — 완료 시 이 파일 update-in-place.

## 재현 경로

- 합성 스케일링: 세션 scratchpad `scale_N.hexa` (일회성)
- 실측 스크립트: aiden `~/anima-bisect/bisect_takeover.sh` · summer `~/anima-buildprobe/build_probe.sh`
- workflow 종합: wf_a90db704-17b (세션 transcript)
