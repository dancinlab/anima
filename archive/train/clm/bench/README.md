# CLM AKIDA 벤치 harness

> `.clm` int4 모델 → **AKD1000 on-chip forward** latency·throughput 측정 +
> SW(`akida_sw_lif`) 대조 **int4 byte-identical** 검증.
> SSOT 그라운드 = [CLM_FORMAT_SPEC.md](../CLM_FORMAT_SPEC.md)(.clm 레이아웃) ·
> [P0_ARCHITECTURE.md](../P0_ARCHITECTURE.md) §9(QAT envelope) ·
> [CLM_ANATOMY.md](../CLM_ANATOMY.md)(한눈 해부).

---

## 무엇 / 왜

- CLM 추론은 **AKIDA-int4-only** (P0 d4). 이 harness 는 `.clm` 의 `int4_sym` track 을
  AKD1000 칩에 올려 **온칩 forward 의 실측 latency / throughput** 을 잰다.
- 동시에 같은 int4 weight 를 numpy SW envelope(`akida_sw_lif.fc_quantized_forward`)에
  통과시켜 **HW = SW byte-identical** 을 확인 — 1~5차 AKD1000↔SW 캘리브레이션 envelope 의 연장.

## 측정 축

| 축 | 뜻 |
|---|---|
| `latency_ms_per_inference` | 칩 위 forward 1회 wall 시간 (warm-up 후 N-iter 평균) |
| `throughput_hz` | 초당 추론 횟수 (= N / 총 wall) |
| `byte_identical_hw_sw` | HW 출력 vs SW envelope 출력 완전 일치 여부 |
| `hamming` | HW≠SW 비트 수 (0 이면 byte-identical) |
| `provenance` | `akida-hw`(라이브) / `akida-sw-fallback`(스모크) |

## 모드

| 모드 | 조건 | 측정 |
|---|---|---|
| **hw-live** | `.clm` 존재 ∧ `akida.devices()` 비어있지 않음 | 온칩 latency·throughput 실측 + SW 대조 |
| **sw-smoke** | `.clm` 부재 (또는 칩 unreachable) | SW envelope 만 tiny 더미 int4 로 통과 = **배선 검증**. on-chip latency = `null` (**fake 측정 금지** · p7) · `awaiting_clm=true` |

> ⚠ **정직(p7)**: `.clm` 이 아직 없으면(현재 P2 full-fire `a098b6194` 가 첫 ckpt→.clm
> 생성중) on-chip latency 를 **절대 지어내지 않는다**. sw-smoke 로 harness 가 돈다는 것만
> 증명하고 "fire .clm 대기" 를 명시한다.

## 사용법

```bash
# SW 스모크 (.clm 없이 harness 배선 검증 · Mac/로컬 $0)
python3 CLM/bench/clm_akida_bench.py --json

# act_bits 2 envelope 스모크
python3 CLM/bench/clm_akida_bench.py --act-bits 2

# 라이브 온칩 벤치 (.clm 도착 후 · pi5-akida 위에서)
python3 CLM/bench/clm_akida_bench.py --clm <PATH-TO-.clm> --n-iter 100 --json
```

옵션: `--clm PATH` · `--n-iter N`(default 100) · `--units`/`--in-lines`(default 16) ·
`--act-bits`(default 1, LIF) · `--input-bits`(default 4) · `--seed`(default 187) · `--json`.

> 의존: numpy. SW envelope import = `AGENT/CHAT/akida_sw_lif.py`(상대경로 자동 해석).

## pi5-akida 단일점유 — spike-streamer stop → bench → restart (복원 필수)

AKD1000 은 **단일칩 file-lock**: `spike-streamer.service`(24h R3 자연발화 스트림)가 칩을
점유 중이라, 라이브 벤치는 streamer 를 **잠시 멈추고 → 벤치 → 다시 켜서** 종료상태가
streamer active 가 되도록 복원해야 한다 (PI5-AKIDA.json `ops` 참조).

```bash
# pi5-akida (ssh ubuntu@192.168.50.155) 위에서:
systemctl --user stop spike-streamer                         # 1. 칩 lock 해제
~/.venv/anima-akida/bin/python3 \
   ~/anima/CLM/bench/clm_akida_bench.py --clm <PATH> --json   # 2. 온칩 벤치
systemctl --user enable --now spike-streamer                 # 3. streamer active 복원 (종료상태)
systemctl --user status spike-streamer                       # 4. active 확인
```

- **복원 필수**: 벤치 종료 상태 = `spike-streamer` active (자연발화 HW 폐루프 복귀).
- `PI5-AKIDA.json` 은 읽기 전용 provenance ledger (미커밋) — 위 ops 명령의 SSOT.

## 결과 영속

- verdict = [`.verdicts/clm-bench-anatomy/`](../../.verdicts/clm-bench-anatomy/)
  (`sw_smoke_2026_05_30.txt` / `.json`).
- bench 한 줄 요약 = [`CLM/CLM.md`](../CLM.md) P4 항목.

## 현재 상태 (2026-05-30)

- `.clm` 아티팩트 = **0** (origin/main + 로컬). fire `a098b6194` P2 full-fire 가 첫 ckpt→.clm 생성중.
- → harness = **sw-smoke PASS** (SW envelope 배선 검증, $0 Mac local). **fire .clm 대기**.
- `.clm` 도착 시 위 streamer stop→bench→restart 로 라이브 온칩 실측 + byte-identical 대조.
