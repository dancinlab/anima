# EC/EO Skip Guide — 매번 Berger 안 돌리는 3가지 방법

Status: landed 2026-05-07. Implements user request "EC/EO 매번 안 하는 방법".

## TL;DR

**`master_preflight`는 이미 Berger 없이 돌아갑니다.** 5-min EC/EO 블록 디자인은 별개 protocol(`alpha_eyes_closed.hexa`)이고, hardware sanity gate에 필수 아닙니다.

추가로 Berger 자체를 줄이는 3가지 방안 모두 land:

| 방식 | 모듈 | 시간 | 사용 |
|---|---|---|---|
| **A. Ledger skip-gate** | `eeg/protocols/berger_skip_gate.hexa` | 5min → 0 (skip 시) | `eeg_setup.hexa berger_skip_gate --check` |
| **B. Quick Berger** | `eeg/protocols/alpha_eyes_closed.hexa --quick` | 5min → 1min | `eeg_setup.hexa berger --quick` |
| **C. Background audit** | `eeg/protocols/background_quality_audit.hexa --watch` | 0 (병행) | already-existing module |

## A. Ledger skip-gate

직전 Berger PASS 가 ledger에 있고, 4시간 이내 + impedance drift < 20% + 같은 helmet → skip.

### 사용 흐름

```bash
# 1) 첫 세션: 정식 Berger 실행 후 결과를 ledger에 기록
hexa run eeg/protocols/alpha_eyes_closed.hexa --run --port /dev/cu.usbserial-XYZ \
    --output recordings/sessions/berger_2026_05_07.npy
# (분석 후 EC/EO ratio 산출되면)
hexa run eeg/eeg_setup.hexa berger_skip_gate --record \
    --helmet-id cyton_daisy_set_a \
    --verdict PASS \
    --alpha-ec-eo-ratio 2.4 \
    --impedance-avg-kohm 8.3 \
    --impedance-o1-kohm 7.5 \
    --impedance-o2-kohm 9.1

# 2) 다음 세션 (같은 날 1시간 뒤): skip-gate가 SKIP 허용 여부 결정
hexa run eeg/eeg_setup.hexa berger_skip_gate --check \
    --helmet-id cyton_daisy_set_a \
    --impedance-avg-kohm 8.5
# stdout: __BERGER_SKIP__ ALLOWED fresh_pass_age_3600s_drift_2.4pct
# exit 0 → Berger 건너뛰고 본 세션으로 직행

# 3) 24시간 뒤 또는 helmet 분리/재착용 후: skip-gate가 REQUIRED 반환
hexa run eeg/eeg_setup.hexa berger_skip_gate --check \
    --helmet-id cyton_daisy_set_a \
    --impedance-avg-kohm 12.0
# stdout: __BERGER_SKIP__ REQUIRED impedance_drift_44.4pct_exceeds_20.0pct
# exit 1 → 정식 Berger 다시 실행 필요
```

### Skip 규칙 (R1-R6, 모두 만족해야 ALLOWED)

| R# | 조건 | 위반 시 reason |
|---|---|---|
| R1 | 같은 helmet_id 의 ledger row 존재 | `no_prior_pass_for_helmet_<id>` |
| R2 | 가장 최근 verdict == "PASS" | `latest_verdict_<verdict>` |
| R3 | ts < MAX_AGE_HOURS (4h) | `stale_age_<s>s_exceeds_<max>s` |
| R4 | helmet_id 일치 (사용자 명시) | (R1과 동일 경로) |
| R5 | impedance drift < 20% | `impedance_drift_<n>pct_exceeds_20.0pct` |
| R6 | `--force-berger` 미사용 | `force_berger_flag_set` |

### Ledger 위치


## B. Quick Berger (5min → 1min)

`alpha_eyes_closed.hexa --quick` 추가 — 1×30s EC + 1×30s EO = 60s.

```bash
hexa run eeg/eeg_setup.hexa berger --quick
# 또는 직접:
hexa run eeg/protocols/alpha_eyes_closed.hexa --quick
```

- ✅ 시간 1/5
- ✅ F_BERGER_03 (EC/EO ratio > 2.0) 평가 가능
- ❌ Statistical power 떨어짐 (within-session repeat 0)
- ❌ F_BERGER_01 (alpha peak 7.5-12.5Hz) + F_BERGER_02 (O1/O2 > Fp2) 신뢰 구간 넓음

따라서 quick은 **첫 세션 정식 Berger 후** sanity check 용도로 사용. 첫 세션은 `--run` (full 5min) 권장.

## C. Background quality audit (passive)

`eeg/protocols/background_quality_audit.hexa` (이미 존재) 가 정상 세션 중 silent monitor 동작:

```bash
hexa run eeg/protocols/background_quality_audit.hexa \
    --watch --port /dev/cu.usbserial-XYZ \
    --interval 300 \
    --ledger-path state/quality_ledger/$(date -u +%Y-%m).jsonl
```

5분마다 5가지 metric 검사 (impedance_drift / channel_rail_flat / dc_drift / line_60hz_notch / effective_fs). breach 시 ledger에 append.

**EC/EO 자체를 검출하지는 않음** — 대신 capture quality가 망가지는 순간을 silent로 잡아내서, "Berger PASS 후 한참 지나도 quality 안 망가졌으니 skip 가능"을 신뢰성 있게 만듭니다.

A + C 조합 권장:
1. A로 ledger skip 결정
2. C가 백그라운드에서 capture quality 지속 감시 (CRIT 알림 시 강제 Berger 재실행)

## 통합 워크플로 (권장)

```bash
# 1회/세션 (서비스 시작 시)
hexa run eeg/eeg_setup.hexa health --check
hexa run eeg/protocols/master_preflight.hexa --run --port /dev/cu.usbserial-XYZ
hexa run eeg/eeg_setup.hexa berger_skip_gate --check \
    --helmet-id cyton_daisy_set_a \
    --impedance-avg-kohm $(...)

# skip-gate REQUIRED 면:
hexa run eeg/eeg_setup.hexa berger --quick   # 1min Berger
# 또는 첫 세션 / 큰 변화 후:
hexa run eeg/eeg_setup.hexa berger          # full 5min
# 결과 ledger 등록:
hexa run eeg/eeg_setup.hexa berger_skip_gate --record ...

# 본 세션 동안 백그라운드:
hexa run eeg/protocols/background_quality_audit.hexa --watch ... &
```


1. Skip은 편의 최적화이지 품질 보증이 아님. 4h 윈도우 안에서 paste 건조 / saline 증발 / 케이블 이동 가능. 의심 시 `--force-berger`.
2. Impedance drift 임계 20%는 휴리스틱 (세션간 자연 변동 5-10%, 20%는 의미있는 seating 변화 신호). per-channel 검사는 master_preflight Step 2/4가 수행.
3. helmet_id는 사용자 단언 — gate가 helmet 교체를 자동 감지 못함. 여러 helmet 사용 시 명시적으로 다른 `--helmet-id` 전달 필수.
4. Ledger는 append-only, 가지치기 안 함. selftest가 marker row 남김 — operator가 grep으로 정리 가능.

## Sentinels

- `__BERGER_SKIP__ ALLOWED <reason>` (exit 0) — Berger skip 허용
- `__BERGER_SKIP__ REQUIRED <reason>` (exit 1) — 정식 Berger 필요
- `__BERGER_LEDGER__ APPENDED <path> ts=<ts> helmet=<id> verdict=<v>` — record 성공

## Selftest

```bash
hexa run eeg/protocols/berger_skip_gate.hexa --selftest
# F1 no_prior_row → REQUIRED
# F2 fresh_pass_within_drift → ALLOWED
# F3 large_drift → REQUIRED
# F4 force_berger → REQUIRED
# F5 new_helmet_id → REQUIRED
# __BERGER_SKIP_GATE_SELFTEST__ PASS fails=0
```
