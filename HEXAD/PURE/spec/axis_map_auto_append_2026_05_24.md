# PURE — AXIS_MAP_RESULTS 자동 row append spec (2026-05-24)

> Phase D fire 직전 — post-fire 마다 사람이 `result_to_axis_map.hexa` 출력을
> 복사해 `AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md` 에 손으로 붙여 넣고
> commit/PR 까지 돌리는 수기 흐름(PR #301 E2 row · PR #335 E3 saga)을
> 자동화한다. fire 마다 반복되는 수동 단계 + 수기 오타 risk 를 제거한다.
>
> anchor — 현 도구: `../eval/result_to_axis_map.hexa` (PR #290 + #299 + #355 + #363)
> · 대상 SSOT: `../AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md`
> · dispatch 진입점: `../launchers/dispatch_p21h_v3.hexa`
> · closure 판정 SSOT: PR #264 (4/5 langs ≥ PARTIAL)

## § 1. 동기 — 수동 append 의 비용

| 사례 | 작업 | 수동 단계 | 회피 가치 |
|---|---|---|---|
| PR #301 | E2 row append | (a) fire 종료 → (b) result.json scp pull → (c) `result_to_axis_map.hexa` 실행 → (d) stdout row 복사 → (e) AXIS_MAP md 편집 → (f) commit → (g) PR open/merge | 5 수동 step (c-g) → 자동화 |
| PR #335 | E3 saga (multi-row) | 동상 × 3 row (E3a/b/c) | 15 수동 step → 자동화 |

Phase D fire (corpus 변수 sweep) 는 row 개수가 더 늘어날 가능성이 높아 — 수동
누적이 N 배. `result.json` → 행 → append 까지를 한 번에 끝낸다.

## § 2. 현 도구 — row 계산은 완비, append 만 없음

`result_to_axis_map.hexa` (PR #290 lineage, 212 LoC):
- `parse_result_json(path)` — result.json 로딩 + map 검증
- `judge_closure(result, floor, min_langs)` — PASS/FAIL 결정 (PR #264 default 4/5 ≥ PARTIAL)
- `format_axis_map_row(variant, result, judgement)` — 12-cell markdown table row 문자열 생성
  (variant · closure · agg · n_pass/n_total · per-lang · reg hits · regress ·
  init CE · final CE · wall s · M3 TTR · M5 hangul — PR #287 corpus_quality 포함)
- `main()` — `println(row)` 만 함 (stdout 출력 후 종료, **append 없음**)

→ 부족분 = "출력한 row 를 AXIS_MAP md 의 올바른 위치에 idempotent 하게 끼워 넣는 단계".

## § 3. 자동화 설계 — `append_axis_map_row`

새 함수 시그니처 (별도 PR 에서 구현):

```hexa
fn append_axis_map_row(
    result_path: str,        // post-fire result.json (state/p21h_*/result.json)
    axis_map_path: str,      // 대상 AXIS_MAP md (default: HEXAD/PURE/AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md)
    variant: str,            // E2 / E3a / D1 / ... — row key
    floor: str,              // "PARTIAL" | "PASS"
    min_langs: int           // 4 (PR #264 default)
) -> bool                    // true = appended, false = skip (dup/anchor 실패)
```

동작 흐름 — 1 row 1 호출, 5 단계:

1. **load** — `parse_result_json(result_path)` → `judge_closure` → `format_axis_map_row` 
   = `row_str` (한 줄).
2. **anchor 탐지** — AXIS_MAP md 를 line 단위로 읽고 `## § Updated 7-axis result table`
   섹션의 표 끝(다음 빈 줄 또는 다음 `##` 헤더 직전)을 anchor 로 잡는다.
   탐지 실패 시 ERROR + exit 2 (자동 생성 금지 — 사람이 SSOT 구조 검토 후 손으로 처리).
3. **idempotency 확인** — 같은 `| <variant> |` 접두사 row 가 이미 표에 있으면 
   `false` 반환 + INFO 메시지 출력 (재실행 안전).
4. **backup + write** — `axis_map_path + ".bak"` 사본 생성 → 원본의 anchor 위치에
   `row_str` 한 줄 삽입 → 새 내용 write_file.
5. **diff 보고** — 추가된 1 줄을 stdout 에 echo (사람이 PR review 에서 그대로 확인).

## § 4. CLI · dispatch hook 통합

CLI subcommand (현 도구에 verb 추가):

```sh
hexa run HEXAD/PURE/eval/result_to_axis_map.hexa append \
    --variant E2 \
    [--floor PARTIAL] [--min-langs 4] \
    [--axis-map HEXAD/PURE/AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md] \
    [--commit]            # 선택: 즉시 git add + commit + push + gh pr create
    <result_json_path>
```

기본은 **append 만**. `--commit` flag 시:
- `git add <axis_map>` → `git commit -m "docs(PURE): AXIS_MAP <variant> row auto-append (post-fire)"` 
  → `git push -u origin HEAD` → `gh pr create --fill`.
- 단 — `--commit` 은 opt-in (§ 7 honest C3 참조).

`dispatch_p21h_v3.hexa` post-fire hook 통합:

```
[post-fire 종료 후, motivation calc 직후]
  └─ run: hexa run .../result_to_axis_map.hexa append \
            --variant $variant --axis-map $AXIS_MAP $result_json
  └─ exit 0 = appended | 1 = closure FAIL but row written | 2 = anchor/idempotent skip
```

dispatch 측 새 flag: `--auto-append`. default OFF (기존 fire 영향 0). 명시적 opt-in.

## § 5. Falsifier (pre-register)

| id | 검증 | 측정 |
|---|---|---|
| **F-APPEND-1** | 백업 파일 존재 | append 호출 후 `<axis_map>.bak` 가 생성되며 원본의 변경 전 byte-byte 사본임 |
| **F-APPEND-2** | 표 무결성 | append 후 markdown table syntax PASS — `\| <12 cells> \|` 형태, header column count 와 일치, 다음 `##` 헤더 위치 보존 |
| **F-APPEND-3** | idempotent (중복 차단) | 같은 result.json + variant 로 두 번 호출 시 두 번째는 `false` 반환 + 표에 동일 variant row 1 개만 존재 |
| **F-APPEND-4** | byte-equal regression | PR #301 의 E2 result.json 을 입력으로 주면 PR #301 에 merged 된 row 와 **byte-equal** (whitespace 포함) 한 row 생성 |

smoke 는 fixture `state/p21h_e2_2026_05_22/result.json` 또는 동등 mock 으로 작성.

## § 6. 구현 path

- 본 PR — **spec only**. ~180 LoC, 함수 시그니처 + falsifier 등록만.
- 다음 PR — impl: `result_to_axis_map.hexa` 에 `append_axis_map_row` + `_find_anchor_line` +
  `_row_already_present` 추가 (~80 LoC) + `result_to_axis_map_append_smoke.hexa` (~120 LoC,
  F-APPEND-1..4 검증) + dispatch hook (`--auto-append`) 1-line gate.
- 그 다음 PR — `--commit` flag 분리 (안전성 review 후 별도).

## § 7. Honest C3 (구조적 한계 ≥ 3)

1. **auto-commit 위험 (§ 4 `--commit` 옵션)** — @D g47 (create→merge→clean) 정합 깨질
   수 있음. 자동 PR 이 stack 화 안 된 상태에서 merge 되면 후속 fire 가 base 가
   바뀌어 충돌. → `--commit` 은 default OFF, dispatch hook 에서도 호출 안 함.
   사람이 PR review 후 손으로 merge.
2. **anchor 탐지 fragility** — AXIS_MAP md 의 `## § Updated 7-axis result table`
   헤더 문구가 변경되면 탐지 실패. 표가 둘 이상 있는 SSOT 로 진화하면 어떤 표에
   넣을지 모호. → impl 시 `--anchor "## § ..."` flag 로 사람이 override 가능하게
   설계. 기본 anchor 미스 시 silent fallback 금지 (exit 2).
3. **concurrent fire append race** — 동시에 fire 2 개가 같은 AXIS_MAP 에 append
   하면 마지막 write 가 앞 write 를 덮어쓸 수 있음. → 현 phase 단일 fire wave
   가정. 다중 동시 fire 가 필요해지면 file lock (flock equivalent) 또는 git
   branch-per-fire 로 분기. 본 spec scope 외.
4. **byte-equal regression 부분 한정** — F-APPEND-4 는 `result.json` 이 보존된
   PR (#301) 에 한해 의미. 누락된 result.json 은 재계산 불가. → fixture 보존
   policy 별도 필요 (state/p21h_*/result.json 영속화).
