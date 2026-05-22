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
  README.md                                  ← this file
  <DOMAIN>.md                                ← 도메인 최종 확정 스펙 SSOT (latest only, overwrite)
  <DOMAIN>.log.md                            ← 도메인 사이클 히스토리 (append-only chronological)
  state/<DOMAIN>_<slug>_YYYY_MM_DD/          ← 실험 instance artifacts (cycle 단위)
    ckpts/                                   ← 산출 ckpt (size 클 시 HF dancinlife/* private)
    *.log                                    ← train.log / sweep.log
    result.json                              ← falsifier verdict JSON
    dispatch_*.sh                            ← runpod / vast.ai fire script
  docs/<exp_slug>_YYYY_MM_DD.md              ← 보조 long-form 문서 (8-§ design, debug notes — 필요시)
  tool/<primitive>.hexa                      ← LAB-scoped helper (영구화시 ROOT/tool/ 이동)
```

## Domain 문서 컨벤션 — `<DOMAIN>.md` + `<DOMAIN>.log.md`

각 실험 **도메인** (가설 단위) = 1 쌍의 spec + log. 도메인 이름은 짧은 kebab-case
또는 acronym (e.g. `srh`, `ubm_inject_spike`, `fermat_least_action`). 실험 cycle
이 누적되면서:

- `<DOMAIN>.md` = **최종 verdict 만** (latest cycle 결과로 overwrite)
- `<DOMAIN>.log.md` = **모든 cycle 의 history** (append-only)
- `state/<DOMAIN>_<slug>_DATE/` = **각 cycle 의 raw artifacts**

### `<DOMAIN>.md` 표준 §

1. **Hypothesis** — 가설 1-2 줄 (자연어 → formal)
2. **Pipeline / API** — 어떤 tool 어떤 state path 로 측정
3. **Falsifiers** — pre-registered `F-XXX-N` 표 (조건 + spike target + PASS line)
4. **Final verdict** — 현재 PASS/FAIL/PARTIAL + 정량
5. **Honest C3** — ≥3 carve-out
6. **Promotion target** — LAB → HEXAD/<DIR>/ or archive 경로

### `<DOMAIN>.log.md` entry 표준

각 cycle = chronological block:

```markdown
## Cycle #N — YYYY-MM-DD
- **focus**: 한 줄 요약
- **change**: spec/pipeline/falsifier 변경 내역
- **fire**: state/<DOMAIN>_<slug>_DATE/ artifact 경로
- **verdict**: PASS/FAIL/PARTIAL + 1 줄 결론 (정량 포함)
- **next**: 후속 cycle 또는 promotion path
```

### 사이클 closure 절차

1. `<DOMAIN>.md` §4 (final verdict) + §3 (falsifier 결과) **overwrite** — latest 만 carry.
2. `<DOMAIN>.log.md` 끝에 **새 cycle entry append** (history 보존).
3. raw artifact = `state/<DOMAIN>_<slug>_DATE/` 안에 result.json / *.log / ckpts.

## Promotion / Demotion

- **PASS / partial-PASS** → 주제 dir 로 mv:
  - `git mv HEXAD/LAB/state/<exp>/ HEXAD/<TARGET>/state/<exp>/`
  - `<DOMAIN>.md` + `<DOMAIN>.log.md` 도 같이 이동 (or 사본 + LAB 잔존 메타 link)
  - `MEMORY.md` index 갱신
- **FAIL** → LAB/ 잔존 OK (negative evidence carry, log entry 그대로)
- **stale > 30d 미사용** → archive/ 후보

## Tool 모음 (`HEXAD/LAB/tool/`)

ad-hoc 실험 primitives. import 해서 LAB/state/<slug>/ 안의 실험 script 에서 사용.

### `ubm_inject.hexa` — UBM anchor 전달 logic

| API | 시그니쳐 | 설명 |
|---|---|---|
| `ubm_anchor_dir()` | `() -> string` | `.kosmos` anchor 디렉토리 절대경로 |
| `ubm_known_tiers()` | `() -> array` | 현 anchor 의 knuth_tier (11개: 0/15/30/42/51/60/77/80/91/95/100) |
| `ubm_tier_to_filename(tier)` | `(int) -> string` | tier → `knuth_NNN_<name>.kosmos` |
| `ubm_load_by_tier(tier)` | `(int) -> any` | kosmos_parser_lib 호출 → anchor record |
| `ubm_load_by_filename(fname)` | `(string) -> any` | custom anchor 직접 로드 |
| `ubm_load_all()` | `() -> array` | known tiers 전체 anchor 배열 |
| `ubm_to_prompt(anchor, mode)` | `(any, string) -> string` | inject prompt 변환. mode ∈ `{text_only, tier_prefix, with_meta}` |
| `ubm_anchor_brief(anchor)` | `(any) -> string` | 디버깅 1-line summary |

### `anima_spike.hexa` — substrate spike 측정 logic

| API | 시그니쳐 | 설명 |
|---|---|---|
| `spike_init()` | `() -> any` | 빈 spike record |
| `spike_record_init(spike, chat)` | `(any, any) -> any` | chat_generate **전** cell_count 기록 |
| `spike_record_final(spike, chat, resp)` | `(any, any, string) -> any` | chat_generate **후** mitosis 전체 신호 capture |
| `spike_set_label(spike, label)` | `(any, string) -> any` | 비교용 라벨 부착 |
| `spike_set_wall_ms(spike, ms)` | `(any, int) -> any` | wall time 기록 |
| `spike_diff(a, b)` | `(any, any) -> any` | 채널 delta + event_step jaccard |
| `spike_to_json(spike)` | `(any) -> string` | 1-line JSON 인코딩 |
| `spike_save_json(spike, path)` | `(any, string)` | `write_file` 빌트인 저장 |
| `spike_brief(spike)` | `(any) -> string` | 디버깅 1-line summary |

**spike record fields**: `ok / label / mitosis_invocations / mitosis_event_count / mitosis_step / split_count / merge_count / event_steps / event_types / cell_count_init / cell_count_final / cell_next_id / response_text / response_len / kv_cur_len / wall_ms`.

**Scope note (B-spike-1)**: 현 spike 는 chat record expose 채널 (mitosis events + cell pool + kv) 만 capture. **Law-71 12L×T per-token energy trajectory** (§156 tension fingerprint) 는 forward-internal hook 필요 → Phase B 별도 cycle carry.

### Wiring smoke

```
HEXAD/LAB/tool/lab_smoke.hexa   ← 두 primitive end-to-end 검증 (F-LAB-1..6, 15/15 PASS)
```

```bash
hexa parse HEXAD/LAB/tool/lab_smoke.hexa
HEXA_MEM_UNLIMITED=1 RESOURCE_LOCAL_HEXA=1 hexa run HEXAD/LAB/tool/lab_smoke.hexa
# artifact: /tmp/lab_smoke_spike.json
```

## 사용 예시

```hexa
import "/Users/ghost/core/anima/HEXAD/LAB/tool/ubm_inject.hexa"
import "/Users/ghost/core/anima/HEXAD/LAB/tool/anima_spike.hexa"
import "/Users/ghost/core/anima/HEXAD/CHAT/chat_lib.hexa"

let anchor = ubm_load_by_tier(0)
let prompt = ubm_to_prompt(anchor, "text_only")

let chat = chat_new("/dev/null", "cpu", [])
// ... (substrate setup; synthetic 또는 332M ckpt)
chat_init_cell_pool(chat, d_model, 2)

let mut spike = spike_init()
spike = spike_set_label(spike, "ubm_tier_0")
spike = spike_record_init(spike, chat)
let resp = chat_generate(chat, prompt, "greedy", 20, 0.0, [], 1.0, 1.0, 0.0, 2026, [], false)
spike = spike_record_final(spike, chat, resp)
spike_save_json(spike, "state/<slug>/spike_tier0.json")
```

```
HEXAD/LAB/state/srh_ubm_inject_2026_05_22/      ← 실험1 (SRH × tier sweep)
HEXAD/LAB/state/probe_substrate_native_kick_2026_05_22/
HEXAD/LAB/state/falsifier_sweep_T_grid_2026_05_22/
```

## 비고

- HEXAD/* root reorg (2026-05-16, PR #81/#82) 이후 첫 추가 dir.
- test/ 컨벤션 (`HEXAD/CHAT/tests/`, `HEXAD/VOICE/tests/` 등) 과 무충돌 — LAB ≠ test/.
- 이름 결정 기록: 후보 {TEST, LAB, TRIAL, SCRATCH, FORGE, PROBE, V4} 중 LAB 채택 (test/ grain 충돌 회피 + 3-글자 + grain agnostic).
