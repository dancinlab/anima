# HEXAD/LAB/

ad-hoc 실험 받침대. 주제별 영구 dir (V3/LORA/MITOSIS/CLM/...) 에 들어가기 **이전** 단계의 빠른 시도가 사는 곳.

## 목적

- 단발 measurement / falsifier probe / throwaway sweep
- 주제 미분류 — 어느 주제 dir 로 promotion 할지 판단 보류 중
- 검증되면 주제 dir 로 이동 (LAB → MITOSIS/V3/...), 실패면 그대로 잔존 (history carry)

## 다른 dir 과의 차이

| dir | grain |
|---|---|
| `HEXAD/V3/`, `HEXAD/LORA/`, `HEXAD/MITOSIS/` | 주제별 영구 saga, attempt N counter carry |
| `HEXAD/UNCLASSIFIED/` | promotion-pending design notes (코드 X) |
| `HEXAD/SCRATCH` (없음) — 대체 = **여기 LAB/** | 실행되는 ad-hoc 실험 instances |
| `HEXAD/<DIR>/tests/` | 해당 dir 의 unit / falsifier test (영구) |

## 컨벤션

```
HEXAD/LAB/
  README.md                              ← this file
  state/<exp_slug>_YYYY_MM_DD/           ← 실험 인스턴스 (소문자 + 날짜 suffix; HEXAD/<DIR>/state/ 와 동일 grain)
    ckpts/                               ← 산출 ckpt (size 클 시 HF dancinlife/* private)
    *.log                                ← train.log / sweep.log
    result.json                          ← falsifier verdict JSON
    dispatch_*.sh                        ← runpod / vast.ai fire script
  docs/<exp_slug>_YYYY_MM_DD.md          ← 8-§ 표준 + honest C3 list (필요시)
  tool/                                  ← LAB-scoped helper (영구화시 ROOT/tool/ 이동)
```

## Promotion / Demotion

- **PASS / partial-PASS** → 주제 dir 로 mv:
  - `git mv HEXAD/LAB/state/<exp>/ HEXAD/<TARGET>/state/<exp>/`
  - docs/도 같이 이동, `MEMORY.md` index 갱신
- **FAIL** → LAB/ 잔존 OK (negative evidence carry)
- **stale > 30d 미사용** → archive/ 후보

## 사용 예시

```
HEXAD/LAB/state/probe_substrate_native_kick_2026_05_22/
HEXAD/LAB/state/falsifier_sweep_T_grid_2026_05_22/
```

## 비고

- HEXAD/* root reorg (2026-05-16, PR #81/#82) 이후 첫 추가 dir.
- test/ 컨벤션 (`HEXAD/CHAT/tests/`, `HEXAD/VOICE/tests/` 등) 과 무충돌 — LAB ≠ test/.
- 이름 결정 기록: 후보 {TEST, LAB, TRIAL, SCRATCH, FORGE, PROBE, V4} 중 LAB 채택 (test/ grain 충돌 회피 + 3-글자 + grain agnostic).
