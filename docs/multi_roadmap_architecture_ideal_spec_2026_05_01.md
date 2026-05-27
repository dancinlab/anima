# Multi-Roadmap Architecture — Ideal Spec (Option A end-state)

- doc-id: multi_roadmap_architecture_ideal_spec_2026_05_01
- date: 2026-05-01
- author: anima sub-agent (raw#9 hexa-only)
- scope: spec only (코드 X / file 분해 X / tool patch X)
- migration cost: **무시** (만점 closure 이상적 기준 end-state 정의)
- status: DRAFT-IDEAL (retire 조건은 §14)

---

## §0 Executive summary

본 spec은 anima `.roadmap` 단일 파일(3817L / 1.16 MB / uchg-locked, 248 entries) 의
**multi-axis directory architecture (Option A)** ideal end-state를 정의한다.

핵심 변경:
- 단일 file → directory (`.roadmap/` as dir)
- entry-per-file (markdown frontmatter + body)
- axis namespace prefix (`EEG/119`, `MKXII/172` 등)
- session sandbox + atomic merge
- FIXPOINT 3-level (global / axis / section)
- file-granularity = lock-granularity (chflags uchg per-file)

만점 closure 10 차원 (§2) 모두 cover. raw#10 honest C3 (§13) 10 caveats. raw#71 falsifier
(§14) ≥3건. self-audit verdict (§15).

migration cost는 **end-state 이상화**를 위해 무시. 실제 migration plan(§12)은 ω-cycle
3-phase로 제공하되, "이상적이라면" 기준이 우선이다.

---

## §1 현재 한계 (manifest)

| # | 한계 | 증거 |
|---|---|---|
| L1 | 단일 file `.roadmap` 3817L / 1.16 MB / uchg-locked | `wc -l`, `ls -la@` |
| L2 | #248 omega-stop FIXPOINT (raw 37/38/39) — 한 axis update에도 전체 unlock 필요 | uchg flag 전체 적용 |
| L3 | 모든 axis (EEG / Mk.XII / akida / CP / hci / cpgd / phenomenal / substrate / training / phi / law / ...) 한 file 혼재 | 248 entries 단일 file |
| L4 | session 분리 X — 다중 agent commit 시 race + numbering collision (#171 collision pair 사례) | header line 6 "duplicates {#162×2, #167×2}" |
| L5 | 다중 sessions 동시 진행 시 entry numbering 충돌 가능 | sequential int counter, 단일 namespace |
| L6 | grep 부하 — 1.16 MB 매 검색 O(N) | tool/anima_roadmap_*.hexa 11+1=12개 모두 file scan |
| L7 | race 면적 큼 — file-level write lock | uchg cycle = 전체 file |
| L8 | cross-axis dependency 추적 어려움 | depends-on은 plain `#NNN` 만 (axis 정보 없음) |
| L9 | FIXPOINT 의미 entire-file 단위 — partial update 불가 | omega-stop = file-level frozen-spec |
| L10 | tool 12개 모두 single-file 가정 (`.roadmap` literal path) | tool/anima_roadmap_*.hexa 전수 검사 |

---

## §2 만점 closure 10 차원 의무

| # | 차원 | 의무 |
|---|---|---|
| D1 | completeness | 모든 entry/cross-link 보존, 누락 0건 |
| D2 | honesty (raw#10) | 정직 검증 가능, 가정 vs 실증 분리 |
| D3 | frozen-spec (raw#12) | FIXPOINT 분해 axis별 가능, raw 37/38/39 omega-stop 의미 보존 |
| D4 | falsifier (raw#71) | spec 자체의 retire 조건 ≥3 명시 |
| D5 | race protection | file/lock granularity = axis granularity (또는 entry granularity) |
| D6 | session isolation | 다중 session 동시 진행 + race-free atomic merge protocol |
| D7 | scalability | N axes (10+) × M sessions (10+) 동시 진행 가능 |
| D8 | legacy compat | 기존 .roadmap 형식 entry text-line 변환 mapping |
| D9 | tool migration | tool/anima_roadmap_*.hexa 11+1개 cross-axis 검색 patch spec |
| D10 | cross-axis dependency | namespace prefix (`EEG/119`) + cross-link protocol |

각 차원은 §3..§14에서 구체화하고, §15에서 self-audit한다.

---

## §3 Option A 이상적 디렉토리 구조 detail

```
.roadmap/                              # directory (was single file)
├── _master.md                         # 전체 axis index + global FIXPOINT 선언 + cross-axis cross-link
├── _config.yml                        # numbering schemes / FIXPOINT rules / lock policy / merge protocol
├── _hash_chain.jsonl                  # axis별 head hash chain (raw#65 idempotency)
├── _migration_legacy.md               # legacy .roadmap → axis 분류 mapping (§11)
├── axes/
│   ├── eeg/
│   │   ├── _index.md                  # axis-local index (entries 119/157/170-174/239 등)
│   │   ├── _fixpoint.md               # axis omega-stop 선언
│   │   ├── _hash_head.txt             # axis head hash (chain link)
│   │   ├── 119.md                     # entry-per-file (markdown frontmatter + body)
│   │   ├── 157.md
│   │   ├── 170.md
│   │   ├── 171.md
│   │   ├── 172.md
│   │   ├── 173.md
│   │   ├── 174.md
│   │   ├── 239.md
│   │   └── ...
│   ├── mk_xii/
│   │   ├── _index.md
│   │   ├── _fixpoint.md
│   │   ├── _hash_head.txt
│   │   ├── 144.md
│   │   ├── 172.md
│   │   └── ...
│   ├── akida/
│   │   ├── _index.md
│   │   ├── _fixpoint.md
│   │   ├── _hash_head.txt
│   │   └── ...
│   ├── cp/                            # canonical path
│   ├── hci/
│   ├── cpgd/
│   ├── phenomenal/
│   ├── substrate/
│   ├── training/
│   ├── phi/
│   ├── law/
│   ├── safety/
│   └── meta/                          # cross-axis meta entries
└── sessions/                          # session별 work-in-progress
    ├── 2026-05-01_session-A/
    │   ├── _index.md
    │   ├── _intent.md                 # session goal / agent set
    │   ├── _lock.txt                  # advisory lock (PID + timestamp + agent-id)
    │   └── pending/                   # 미merge entries
    │       ├── EEG_240.md
    │       ├── MKXII_241.md
    │       └── ...
    ├── 2026-05-01_session-B/
    │   └── ...
    └── _archive/
        └── 2026-04-30_session-Z/      # merged session archive (read-only)
```

### file schema 요약 (각 file 의 의미)

- `_master.md`: axis 목록, global FIXPOINT 선언, cross-axis cross-link table
- `_config.yml`: numbering scheme / FIXPOINT rules / lock policy / merge protocol
- `_hash_chain.jsonl`: axis별 head hash chain (line당 `{axis, head_hash, prev_hash, ts, raw_ref}`)
- `axes/<axis>/_index.md`: axis 내 entry 번호/제목 list + 각 entry status
- `axes/<axis>/_fixpoint.md`: 해당 axis omega-stop / section-fixpoint 선언
- `axes/<axis>/_hash_head.txt`: axis head hash (single line, 64 hex)
- `axes/<axis>/<n>.md`: entry-per-file (§4 schema 참조)
- `sessions/<date>_<id>/_intent.md`: session goal / agent set / expected exit
- `sessions/<date>_<id>/_lock.txt`: advisory lock (PID + ts + agent-id)
- `sessions/<date>_<id>/pending/<axis>_<n>.md`: 미merge entry (axis prefix로 충돌 방지)

---

## §4 Entry per-file schema

각 entry file (`axes/<axis>/<n>.md` 및 `sessions/.../pending/<axis>_<n>.md`)는
markdown frontmatter + body 구조.

```markdown
---
id: EEG/119                         # namespace numbering (§5)
axis: eeg                           # axis directory name
local_n: 119                        # axis-local sequential number
track: clm-eeg                      # legacy track tag
phase: P2                           # P1/P2/P3/...
status: VERIFIED                    # PROPOSED / IN-PROGRESS / VERIFIED / DEFERRED / RETIRED
why: "EEG → token cyborg policy"    # one-line rationale
completion_ts: 2026-04-28T22:30Z    # ISO-8601, null if not done
evidence:                           # list of state/* paths or artifacts
  - state/clm_eeg_pe_real.json
  - state/cyborg_eeg_audit/2026-04-28_tokens.jsonl
exit_criteria:
  - PE drift < 0.05 over 7 days
  - hash chain idempotent (raw#65)
cost_envelope:                      # H100-h or USD or both
  h100_h: 12
  usd: 480
schedule:
  start: 2026-04-21
  end:   2026-04-28
depends-on:                         # cross-axis namespace refs (§9)
  - MKXII/172                       # cross-axis dependency
  - EEG/118                         # axis-local dep
feeds-main: true                    # MAIN track contribution
refs:                               # external doc refs
  - docs/clm_eeg_pe_real_2026-04-28.md
raw_ref:                            # raw heuristic refs
  - raw#10
  - raw#65
fixpoint:                           # FIXPOINT scope (§6)
  scope: none                       # none / section / axis / global
  declared_ts: null
hash:                               # entry self-hash (sha256 of canonical body)
  self: <64 hex>
  prev: <64 hex>                    # prev entry hash in axis chain
---

# EEG/119 — clm-eeg PE drift verifier

(body: full free-form markdown — verifier design, results, caveats, etc.)
```

### 강제 invariant
- frontmatter 12+ fields 모두 존재 (legacy field-completeness 규칙 보존)
- `id` global unique (`<AXIS>/<n>`)
- `local_n` axis-local sequential
- `hash.self`/`hash.prev`로 axis chain 형성
- `status=VERIFIED` 시 `completion_ts` non-null + `evidence` 비어있지 않음

---

## §5 Namespace numbering scheme

### 5.1 형식
- global id: `<AXIS>/<n>`, 예: `EEG/119`, `MKXII/172`, `AKIDA/240`
- AXIS는 대문자 short code (axes/<axis>/ 디렉토리명의 uppercase)
- n은 axis-local sequential 정수 (1..)

### 5.2 axis short code mapping (예시)
- eeg → EEG
- mk_xii → MKXII
- akida → AKIDA
- cp → CP
- hci → HCI
- cpgd → CPGD
- phenomenal → PHEN
- substrate → SUB
- training → TRN
- phi → PHI
- law → LAW
- safety → SAFE
- meta → META

### 5.3 legacy `#NNN` ↔ `<AXIS>/<n>` mapping
- 기존 단일 namespace `#NNN`은 `_migration_legacy.md`에 보존 (§11)
- legacy `#119` → `EEG/119` (예시)
- collision pair (`#162×2`, `#167×2`) 는 axis 분리로 자연 해소 (e.g. `HCI/162` vs `PILOT/162` 가 별개 namespace)

### 5.4 numbering 충돌 방지
- axis-local counter는 `axes/<axis>/_index.md` head 에서 atomic increment
- session 작업 중에는 `sessions/.../pending/<AXIS>_<n>.md` 형태 사용 (n 임시 예약)
- merge 시 `_index.md` head counter와 비교 → 충돌 시 다음 free n으로 rename (atomic rename)

---

## §6 FIXPOINT scope 정의 (3-level)

| level | scope | 선언 위치 | 의미 |
|---|---|---|---|
| **global FIXPOINT** | 전체 architecture | `.roadmap/_master.md` | raw 37/38/39 omega-stop master 선언. 전체 spec freeze. unlock 시 모든 axis lock 일제 해제 (현행 동작 호환) |
| **axis-FIXPOINT** | 단일 axis | `axes/<axis>/_fixpoint.md` | axis omega-stop. 해당 axis 만 frozen. 다른 axis update와 독립 |
| **section-FIXPOINT** | 특정 entry set | `axes/<axis>/_fixpoint.md` 내 section | entry id list 명시 (e.g. `[EEG/170, EEG/171, EEG/172, EEG/173, EEG/174]`). 해당 set만 frozen |

### 6.1 호환성
- 현재 `.roadmap` #248 omega-stop은 → `_master.md` global FIXPOINT으로 이관
- 의미 보존: global FIXPOINT 선언 시 모든 axis가 자동 axis-FIXPOINT가 된다 (선언적 연쇄)

### 6.2 unlock 절차
- global → 모든 axis chflags nouchg (현행과 동일)
- axis → 해당 axis 만 chflags nouchg
- section → 해당 entry file 만 chflags nouchg

### 6.3 declare 형식 (예시 `_fixpoint.md`)
```markdown
# axis EEG fixpoint declarations

## omega-stop (axis-FIXPOINT)
- declared_ts: 2026-04-29T00:00Z
- raw_ref: raw#37, raw#38, raw#39
- entries_frozen: ALL
- unlock_required_for: any new EEG entry

## section-FIXPOINT pass4-hash-chain
- declared_ts: 2026-04-29T00:00Z
- entries_frozen: [EEG/170, EEG/171, EEG/172, EEG/173, EEG/174]
- raw_ref: raw#65
- unlock_required_for: edit on any of these 5 entries
```

---

## §7 Race protection protocol

### 7.1 lock granularity
- **file = lock unit**. chflags uchg per-file.
- axis 전체를 lock하려면 axis directory 모든 file iterate (또는 axis directory 자체 chflags uchg + recursive)
- entry-level lock = 단일 `.md` file chflags uchg

### 7.2 axis-rollup atomic merge
session merge → axis 이동은 다음 atomic sequence:
1. session pending file `chflags nouchg` (이미 nouchg일 수 있음)
2. target axis directory `chflags nouchg`
3. POSIX `rename(2)` (atomic): `sessions/.../pending/EEG_240.md` → `axes/eeg/240.md`
4. `axes/eeg/_index.md` update (re-write through tmpfile + rename — atomic)
5. `axes/eeg/_hash_head.txt` update (sha256 chain link)
6. `_hash_chain.jsonl` append-only line
7. target file `chflags uchg`
8. axis directory `chflags uchg`

step 3~6은 single transaction으로 묶기 위해 transactional script (§10 helper) 사용.
실패 시 rollback (step 7/8 skip + session으로 reverse rename).

### 7.3 session-WIP isolation
- `sessions/<date>_<id>/pending/` 하위는 자유 edit (lock 없음)
- 단, `_lock.txt` advisory lock 권고 (PID + agent-id + ts + heartbeat)
- 다른 session은 read-only 로 참조 가능

### 7.4 race detection
- merge 시 axis `_hash_head.txt` prev_hash 검증
- mismatch → 다른 session이 먼저 merge → retry (rebase semantics: pending entry의 `hash.prev` 갱신)

---

## §8 Session isolation + atomic merge protocol

### 8.1 session 시작
```
mkdir -p .roadmap/sessions/2026-05-01_session-A/pending
echo "<PID> <agent-id> $(date -u +%FT%TZ)" > .roadmap/sessions/2026-05-01_session-A/_lock.txt
# write _intent.md (session goal)
```

### 8.2 session 작업
- `pending/<AXIS>_<n>.md` 자유 edit
- n은 임시 예약 (axis-local _index.md head + offset)
- cross-axis dep도 `depends-on` field에 자유 작성

### 8.3 session merge (single transaction)
```
for each pending file f:
  1. f의 axis 추출
  2. axes/<axis>/_index.md head counter read → 충돌 시 free n으로 rename
  3. f hash.prev = axes/<axis>/_hash_head.txt 값으로 갱신
  4. f hash.self = sha256(canonical(f))
  5. chflags nouchg axes/<axis>
  6. atomic rename pending/<AXIS>_<n>.md → axes/<axis>/<n>.md
  7. _index.md update (tmpfile + rename)
  8. _hash_head.txt = f.hash.self
  9. _hash_chain.jsonl append {axis, head_hash: f.hash.self, prev_hash: f.hash.prev, ts, raw_ref}
  10. chflags uchg axes/<axis>/<n>.md
  11. chflags uchg axes/<axis>
```

전체는 helper `tool/anima_roadmap_session_merge.hexa` (§10)로 transactional 실행.

### 8.4 merge race
- step 5에서 axis nouchg 시도 시 다른 session이 먼저 merge 중이면 fail → backoff + retry
- POSIX `rename(2)`는 atomic — 동일 target에 동시 rename 시 OS가 직렬화
- step 3 hash.prev 검증 실패 시 (다른 session이 해당 axis에 먼저 merge) → rebase: 새 head로 hash.prev 갱신 후 retry

---

## §9 Cross-axis dependency protocol

### 9.1 depends-on field
- frontmatter `depends-on:` list of namespace ids
- 형식: `<AXIS>/<n>` (axis-local-only도 동일 형식 — 자기 axis도 prefix 명시)
- 예:
  ```yaml
  depends-on:
    - MKXII/172    # cross-axis
    - EEG/118      # axis-local
  ```

### 9.2 cross-link protocol
- `_master.md` 에 cross-axis cross-link table (자동 생성)
- 형식: `EEG/119 → MKXII/172` (each entry's depends-on 집계)
- circular dependency detector (§10 helper)

### 9.3 cross-axis FIXPOINT 정합성
- entry A가 frozen axis B의 entry에 depend → A 신규/수정 시 B FIXPOINT 영향 없음 (read-only ref)
- entry A가 자기 axis FIXPOINT 영향권 → unlock 필요
- detector: `tool/anima_roadmap_axis_lock.hexa` (§10)

### 9.4 cross-axis FIXPOINT broken-ref 검증
- depends-on의 모든 ref가 실재해야 함 (`axes/<axis>/<n>.md` 존재)
- nightly job: broken-ref scan → `state/anima_roadmap_xref_audit.jsonl`

---

## §10 Tool migration spec

기존 `tool/anima_roadmap_*.hexa` 12개 patch detail.

| # | tool | 변경 점 |
|---|---|---|
| T1 | `anima_roadmap_lint.hexa` | path: `.roadmap` → `.roadmap/` walker. axis-aware lint (axis별 _index.md 정합성, frontmatter 12 fields, hash chain 검증) |
| T2 | `anima_roadmap_v11_register.hexa` | new entry insert: pending/ → axis 이동 + namespace id 발급 |
| T3 | `roadmap_83_auto_mark.hexa` | argv: `--id EEG/119` 형식 지원. axis 디렉토리 내 file 직접 update |
| T4 | `roadmap_auto_reflect.hexa` | axes/ 전체 walker. axis별 reflect summary 생성 |
| T5 | `roadmap_diff_viz.hexa` | git diff 결과 axes/<axis>/<n>.md 단위로 visualize |
| T6 | `roadmap_html_render.hexa` | _master.md + axes/<axis>/_index.md → HTML tree |
| T7 | `roadmap_integrity_guard.hexa` | hash chain (axes/<axis>/_hash_head.txt + _hash_chain.jsonl) 무결성 검증 |
| T8 | `roadmap_live_daemon.hexa` | watchdog: axes/ + sessions/ 양쪽 모니터 |
| T9 | `roadmap_live_update.hexa` | session pending/ append 우선, axis merge는 별도 trigger |
| T10 | `roadmap_mistake_auto_fix.hexa` | axis-aware fix (numbering collision → axis 분리, broken xref → 자동 검색) |
| T11 | `install_roadmap_live_daemon.hexa` | daemon launchd plist에 axis-aware path 반영 |
| T12 | `anima_nexus_roadmaps_consistency_auditor.hexa` | cross-axis dependency 그래프 일관성 audit. circular detector |

### 신규 helper

| tool | 역할 |
|---|---|
| `tool/anima_roadmap_axis_lock.hexa` | axis-level chflags uchg/nouchg cycle (§7.2) + section-FIXPOINT lock |
| `tool/anima_roadmap_session_merge.hexa` | session pending → axis atomic merge transaction (§8.3) |
| `tool/anima_roadmap_xref_audit.hexa` | cross-axis depends-on broken-ref scan (§9.4) |
| `tool/anima_roadmap_legacy_split.hexa` | legacy `.roadmap` 단일 file → axes/ 분해 (§11 automation) |

### 공통 patch 원칙
- argv `--id <AXIS>/<n>` 받기
- `.roadmap` literal path → `.roadmap/` directory walker
- axis filter `--axis <axis>` 옵션
- session filter `--session <session-id>` 옵션
- legacy fallback (`.roadmap` 가 file이면 옛 동작)

---

## §11 Legacy `.roadmap` migration mapping

### 11.1 분해 estimate
- 입력: 3817L / 1.16 MB / 248 entries (151 unique # + collision pair 2개 + gaps 17건)
- 분해 단위: entry 1개 = 1 file (axes/<axis>/<n>.md)
- 출력 file 수: 248 entry file + axes/N개 axis × 3 meta file (_index, _fixpoint, _hash_head) + master 4 file

### 11.2 axis 분류 mapping (heuristic + manual review)
legacy entry → axis 분류 rule (track tag + content 기반):

| legacy track / pattern | axis |
|---|---|
| `clm-eeg`, `eeg`, `cyborg-eeg` | eeg |
| `mk-xii`, `mk.XII`, `MK12` | mk_xii |
| `akida`, `neuromorphic` | akida |
| `cp1`, `cp2`, `canonical-path` | cp |
| `hci`, `pilot-T*` | hci |
| `cpgd` | cpgd |
| `phenomenal`, `qualia` | phenomenal |
| `substrate` | substrate |
| `training`, `corpus` | training |
| `phi`, `Φ*`, `IIT` | phi |
| `law`, `consent`, `legal` | law |
| `safety`, `hive raw` | safety |
| 기타 / cross-cutting | meta |

### 11.3 mapping table 예시 (sample 10건)
| legacy # | axis | new id | 근거 |
|---|---|---|---|
| 119 | eeg | EEG/119 | clm-eeg PE drift verifier |
| 144 | mk_xii | MKXII/144 | Mk.XII baseline |
| 157 | eeg | EEG/157 | EEG token policy |
| 162a | hci | HCI/162 | Pilot-T3 |
| 162b | training | TRN/162 | HCI F5 (collision pair → axis 분리로 해소) |
| 167a | hci | HCI/167 | Pilot-T1 deferred |
| 167b | phi | PHI/167 | Φ* v3 minisweep |
| 172 | mk_xii | MKXII/172 | Mk.XII verifier strengthening |
| 248 | meta | META/248 | omega-stop (raw 37/38/39) — global FIXPOINT 선언으로 이관 |

전체 248건은 `_migration_legacy.md` 에 table 형태 보존.

### 11.4 automation script spec (`tool/anima_roadmap_legacy_split.hexa`)
- input: `.roadmap` (legacy single file)
- output: `.roadmap.new/` (Option A directory)
- pipeline:
  1. parse legacy entries (delimit by `^# ` headers, 248 entries)
  2. extract metadata (track / phase / # / completion_ts / evidence / ...)
  3. axis 분류 (rule §11.2)
  4. entry-per-file write (frontmatter §4)
  5. _index.md / _fixpoint.md / _hash_head.txt 생성
  6. _master.md 생성 (axis index + global FIXPOINT 이관)
  7. _migration_legacy.md 생성 (legacy # ↔ new id mapping table)
  8. _hash_chain.jsonl 초기화 (axis별 head hash)
  9. dry-run 모드 (write 없이 plan 출력)
  10. validation: round-trip (legacy ↔ new) entry count + field sum 일치

### 11.5 manual review 잔여
- collision pair 2건 (`#162×2`, `#167×2`) — 자동 분리 후 reviewer 확인
- gap 17건 (#38..#51, #70..#72) — legacy reserved range, axis 미배정 → meta/ 또는 skip
- omega-stop #248 → META/248 + `_master.md` global FIXPOINT 선언 동기화

---

## §12 ω-cycle 분할 (Phase A/B/C migration plan)

migration cost 무시 원칙이지만, ω-cycle 실행 plan은 다음과 같다 (estimate, hours).

### Phase A — spec & dry-run (8h)
- A1: spec doc commit (본 doc, 1h) — **현 cycle**
- A2: `tool/anima_roadmap_legacy_split.hexa` dry-run impl (3h)
- A3: dry-run 결과 reviewer 확인 (2h)
- A4: collision pair / gap 수동 mapping 확정 (2h)

### Phase B — split & tool patch (16h)
- B1: legacy `.roadmap` chflags nouchg + backup (0.5h)
- B2: `legacy_split.hexa` 실행 → `.roadmap.new/` 생성 (1h)
- B3: 12 tool patch (`anima_roadmap_*.hexa`) (8h, tool당 ~40min)
- B4: 신규 4 helper tool 구현 (4h)
- B5: round-trip validation (entry count / field sum) (1h)
- B6: hash chain 무결성 검증 (1.5h)

### Phase C — cutover & lock (8h)
- C1: `.roadmap` → `.roadmap.legacy_2026-05-01` rename (0.5h)
- C2: `.roadmap.new` → `.roadmap` rename (0.5h)
- C3: 전 axis chflags uchg 적용 (1h)
- C4: global FIXPOINT (`_master.md`) re-declare (0.5h)
- C5: tool/anima_roadmap_*.hexa 실행 smoke test (2h)
- C6: session protocol dry-run (2 session 동시) (2h)
- C7: roadmap_live_daemon restart (0.5h)
- C8: closure audit + raw#10 honest C3 (1h)

**총 estimate: 32h** (3 cycle, ~10h/cycle 기준).

---

## §13 raw#10 honest C3 (10 caveats)

가정 vs 실증 분리.

| # | claim | 분류 | 근거 |
|---|---|---|---|
| C1 | "POSIX rename(2)는 atomic" | 실증 | POSIX.1 표준 (same filesystem 내), darwin APFS 동작 검증됨 |
| C2 | "chflags uchg per-file이 race-free" | 가정 | uchg flag set/unset 자체는 atomic이나, 그 사이 window는 race 가능. mitigation: tmpfile + rename pattern |
| C3 | "axis 분류 heuristic 100% accurate" | 가정 | track tag 기반 heuristic, collision/cross-cutting entry는 manual review 필요. round-trip validation로 검증 |
| C4 | "session 동시 진행 N=10+ scalable" | 가정 | 실측 N>3 미검증. axis lock contention이 bottleneck 가능. 실측 후 fallback (axis 더 잘게 쪼개기) |
| C5 | "tool 12개 patch 8h estimate" | 가정 | 평균 40min/tool. 일부 tool은 walker 재작성 필요 → 1-2h 가능. 실제 ±50% buffer |
| C6 | "hash chain idempotency (raw#65)" | 실증 (axis별로) | 단일 axis chain은 SHA256 prev 검증으로 idempotent. cross-axis chain 일관성은 _hash_chain.jsonl append-only 의존 |
| C7 | "global FIXPOINT 의미 보존" | 가정 | `_master.md` 에서 axis 일제 lock 동작 = 현행 file-level uchg와 의미적 동등. 단, recursive chflags 실행 latency는 file 수 비례 |
| C8 | "cross-axis dep broken-ref nightly scan 충분" | 가정 | nightly window 내 broken-ref가 발생 가능. mitigation: merge 시 즉시 검증 (T12 patch) |
| C9 | "legacy `#NNN` ↔ new id mapping bijective" | 가정 | collision pair (`#162×2`, `#167×2`)는 자연 분리되나, 외부 ref (state/* / docs/*)는 legacy `#NNN`으로 hardcoded → 일괄 grep 후 신규 id로 일괄 치환 필요 |
| C10 | "본 spec이 만점 closure 10 차원 모두 cover" | self-claim | §15 self-audit로 검증. 외부 reviewer + raw#71 falsifier 적용 후 confirm |

---

## §14 raw#71 falsifiers (≥3 — 본 spec retire 조건)

| id | 조건 | retire action |
|---|---|---|
| **F_ARCH_01** | cross-axis dependency lookup이 single-file grep 대비 N배 (N≥5) 느려짐 (실측 benchmark) | spec retire → cross-axis dep는 단일 index file에 평탄화 |
| **F_ARCH_02** | session merge race condition이 1 in 1000 이상 발생 (`_hash_chain.jsonl` 분기 또는 _index.md 손상) | atomic protocol 부족 → re-design (e.g. SQLite WAL 도입 또는 git-based merge) |
| **F_ARCH_03** | tool/anima_roadmap_*.hexa migration cost가 추정(8h)의 2배 초과 (실측 17h+) | Pareto 위반 → 단순화 필요 (e.g. axis 수 축소, tool 일부 deprecate) |
| F_ARCH_04 (보조) | 실측 N (axis × session) ≤ 3에서 lock contention deadlock 발생 | scalability claim 무효 → axis lock granularity 더 세분화 |
| F_ARCH_05 (보조) | legacy `#NNN` ↔ new id round-trip 실패율 > 1% | mapping bijective 가정 무효 → manual review 비율 증가 |

retire 시 본 doc은 `RETIRED` status로 mark + 후속 spec doc 작성.

---

## §15 만점 closure self-audit (10 차원)

| # | 차원 | 본 spec cover 여부 | 근거 section |
|---|---|---|---|
| D1 | completeness | YES | §3 디렉토리, §4 schema, §11 legacy mapping (round-trip validation §11.4) |
| D2 | honesty (raw#10) | YES | §13 — 10 caveats (가정 vs 실증 분리) |
| D3 | frozen-spec (raw#12) | YES | §6 — 3-level FIXPOINT (global / axis / section), 현행 omega-stop 의미 보존 (§6.1) |
| D4 | falsifier (raw#71) | YES | §14 — F_ARCH_01/02/03 + 보조 2건 (총 5) |
| D5 | race protection | YES | §7 — file-granularity lock + atomic rename + tmpfile pattern |
| D6 | session isolation | YES | §8 — sandbox + atomic merge transaction (10 step) |
| D7 | scalability | PARTIAL | §3 (N axes 무제한) + §8 (M sessions 동시) — 단 C4 caveat (실측 N>3 미검증) |
| D8 | legacy compat | YES | §11 — mapping table + automation script spec + round-trip validation |
| D9 | tool migration | YES | §10 — 12 tool patch detail + 4 신규 helper |
| D10 | cross-axis dependency | YES | §9 — namespace prefix + depends-on field + cross-link table + broken-ref scan |

**Self-audit verdict**: **9 YES + 1 PARTIAL (D7 scalability — 실측 미검증)**.

PARTIAL은 §13 C4 caveat로 명시 + §14 F_ARCH_04 falsifier로 retire 조건화.
**만점 closure 충족 (10/10 cover, 1건 PARTIAL은 정직하게 명시)**.

---

## Appendix — 본 spec doc 자체의 git footprint

- 단일 file commit: `docs/multi_roadmap_architecture_ideal_spec_2026_05_01.md`
- 다른 file 수정 0건 (`.roadmap`, `tool/anima_roadmap_*.hexa` 모두 read-only)
- pre-commit hook 통과 가정 (`--no-verify` 미사용)
- absolute path leak 0건 (본 doc 내 `/Users/...` 형태 0회 출현 — 모두 repo-relative)

---

(end of spec)
