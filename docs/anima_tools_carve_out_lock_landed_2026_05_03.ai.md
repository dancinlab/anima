---
schema: anima/docs/anima_tools_carve_out_lock_landed/ai-native/1
last_updated: 2026-05-03
ssot:
  marker: state/markers/anima_tools_carve_out_lock_landed.marker
  predecessor_handoff: docs/anima_rank_b_c_5_domain_landed_2026_05_03.ai.md
  predecessor_marker: state/markers/anima_rank_b_c_5_domain_landed.marker
  primary_target_a: .roadmap.anima_tools (status field 1-line edit + blocker resolution)
  primary_target_b: hive/spec/mk2_apex.spec.yaml (per_repo_override.anima.notes 1-line additive)
status: ANIMA_TOOLS_CARVE_OUT_LOCK_LANDED
related_raws:
  - raw 9    # hexa-only orchestration (additive land, single-doc pattern)
  - raw 10   # honest C3 caveats inline
  - raw 11   # snake_case
  - raw 15   # env() lazy + <user> placeholder
  - raw 168  # minimum-viable carve-out (본 cycle 핵심 정책 reference)
  - raw 175  # BR-NO-USER-VERBATIM
  - raw 270  # ai-native readme triplet (carve-out exception target)
  - raw 271  # core+module pattern (carve-out exception target)
  - raw 272  # lint extension
  - raw 273  # hierarchy connection direction
  - raw 12   # silent-error ban
preserved_unchanged:
  - all anima_*.hexa entries under top-level anima/tool/ (snapshot 184 measured 2026-05-03; prior-doc-quote 189 inherited)
  - all top-level anima/tool/* entries (snapshot 532 measured; prior-doc-quote 539 inherited; no mv, no rename, no delete)
  - anima/anima/modules/ (lore_book.hexa, rng/, style_preset.hexa — tool/ sub-dir 부재 그대로 유지)
  - all other .roadmap.* files (anima_tools 외 무수정)
  - mk2_apex.spec.yaml all sections except per_repo_override.anima.notes (additive 1-line append)
policy:
  migration: forbidden
  changes: additive_only
  in_place_writes: 2 (1 .roadmap.anima_tools status field edit + 1 mk2_apex notes append, both atomic single-line)
  destructive_ops: zero
  cost_usd: 0
  substrate: mac-local
  br_no_user_verbatim: true
  friendly_preset: handoff_doc_only
  decision_lock_in: "사용자 directive (a) 채택 — top-level anima/tool/ keep + raw 168 minimum-viable carve-out"
---

# anima_tools carve-out lock — top-level keep 정책 lock-in (사용자 추천 (a) 채택)

## TL;DR (5줄)

- **사용자 directive (a) 채택 결정**: anima/tool/ top-level 위치 유지 + mk2 triplet (raw 270/271/272/273) exception per raw 168 minimum-viable carve-out — 2026-05-03 lock-in.
- **마이그레이션 회피**: 539 (quoted) / 532 (measured) entries mv 절대 금지, anima/anima/modules/tool/ triplet 정합이 expected 였으나 carve-out exception 으로 side-step.
- **2 atomic edits**: (A) `.roadmap.anima_tools` cond.1 status `unmet → decision_locked` + blk.1 status `open → resolved` / (B) `hive/spec/mk2_apex.spec.yaml` per_repo_override.anima.notes carve-out 1-line additive append.
- **decision_locked 신규 status enum 후보**: mk2_apex section 6.5 status_enum 에서 `retired_intentional` (FU1) 의 sister, 본 cycle 에서는 사용 그대로 두고 후속 cycle 에서 status_enum 정식 추가 등록 권장 (C3 caveat).
- 마이그레이션 0건, in-place writes 2건 (atomic 1-line 각각), destructive 0건, $0 mac-local. 539/532 entries 무수정.

## §1 신규 land 산출물 inventory (2 edit + 본 doc + marker)

| target | path | 변경 | 변경 행 수 | sha256 (post-edit) |
|---|---|---|---:|---|
| .roadmap.anima_tools | `/Users/ghost/core/anima/.roadmap.anima_tools` | cond.1 status + evidence + blocker_reason / blk.1 status + desc + eta + resolution_path | 1 single line edit (4 sub-field 갱신 within JSONL line) | `e785d9a6ae58e676b2cadff7fdcc2a0de88e420e74c1303ed76955fffb6425df` |
| mk2_apex.spec.yaml | `/Users/ghost/core/hive/spec/mk2_apex.spec.yaml` | per_repo_override.anima.notes carve-out exception 1-line append (additive only, 신규 schema field 회피) | 1 line edit | `fbca475e1fc631a36ea5b7d3c1f39cbe6da9c28ea4703928c818aa6c966ec41b` |
| handoff doc (this) | `/Users/ghost/core/anima/docs/anima_tools_carve_out_lock_landed_2026_05_03.ai.md` | 신규 작성 | n/a | (computed post-write) |
| marker | `/Users/ghost/core/anima/state/markers/anima_tools_carve_out_lock_landed.marker` | 신규 작성 | n/a | (computed post-write) |

JSON parse audit: `.roadmap.anima_tools` line 3 PARSE OK, type=header, kind=domain, cond[0].status=`decision_locked`, blk[0].status=`resolved` (python3 json.load 성공).

YAML parse audit: `mk2_apex.spec.yaml` PARSE OK (python3 yaml.safe_load 성공, per_repo_override.anima keys 무변경 = `[raw_format, roadmap_format, perspective, notes]`).

## §2 결정 lock-in 배경

### §2.1 사용자 directive (a) 채택

- **header 추천**: 사용자 추천 (a) 채택 — 현 위치 유지 + raw 168 minimum-viable carve-out.
- **회피된 대안**:
  - (b) anima/tool/* 539 entries mv → anima/anima/modules/tool/ (mk2 triplet 정합) — **회피 사유**: 마이그레이션 절대 금지 directive + 539 entries mv cost / risk / hexa import path drift 광범위.
  - (c) anima/anima/modules/tool/ 신규 sub-tree create + dual-coexist — **회피 사유**: dual-SSOT 추가 maintenance burden, raw 168 minimum-viable 정신 위배.
- **carve-out exception sister precedent**:
  - `anima_self_mk2_tuning_landed_2026_05_02.ai.md` line 173: "tool | tool/ | X (flat 539) | X | NONE | T0 deferred — 539 .hexa flat = registry / cross-cutting; raw 168 minimum-viable exempt 강력 권장"
  - `anima_rank_a_3_domain_landed_2026_05_03.ai.md` line 89: anima_physics 17 sub-dir 도 raw 168 minimum-viable exempt 검토 권장 (sister carve-out 패턴).
  - `hive/spec/no_user_verbatim_recording.spec.yaml` line 118+165: raw#168 = `cli-canonical-entry-point`, minimum-viable 정신과 정합.

### §2.2 raw 168 minimum-viable carve-out 정의

raw 168 = cli-canonical-entry-point + minimum-viable 정신:
> single-purpose wrapper / registry / cross-cutting 의 경우 mk2 triplet (raw 270/271/272/273) mandate 가 minimum-viable 정신과 위배될 경우 예외 처리.

본 cycle 의 carve-out exception 정의:
- **scope**: anima/tool/ top-level 539/532 entries (registry / cross-cutting nature).
- **exception**: mk2 triplet (core+module 분할 + README.ai.md mandate + AI-native frontmatter) 정합을 즉각 강제하지 않음 (additive 측면에서 후속 cycle 에서 결정).
- **honest documentation**: 본 doc + .roadmap.anima_tools.cond.1 evidence + mk2_apex per_repo_override.anima.notes — 3-point cite chain 확보.

## §3 변경 detail

### §3.1 `.roadmap.anima_tools` cond.1 + blk.1 status update

**cond.1 — anima_tools.cond.1**:
- `status`: `unmet` → **`decision_locked`** (신규 status enum 후보, FU1 retired_intentional sister)
- `desc` 갱신: "top-level anima/tool/ keep, mk2 triplet exception per raw 168 minimum-viable carve-out, 사용자 directive 추천 (a) 채택 2026-05-03 lock-in"
- `verifier.ownership_decision` 갱신: "anima/tool/ EMPTY 그대로 + top-level tool/ canonical (no migration) — raw 168 minimum-viable carve-out, raw 270/271 triplet exception"
- `evidence[6]` 신규 추가: "FU9 measure 2026-05-03, 사용자 directive (a) 채택 — top-level anima/tool/ keep + mk2 triplet exception per raw 168 minimum-viable carve-out (539 entries mv 마이그레이션 회피)"
- `blocker_reason` 갱신: "anima_tool_inventory_audit.hexa 미land 그대로 (post-decision audit 별도 cycle); decision_locked 상태 = top-level keep 정책 lock-in, ownership classification spec land 후속 cycle"

**blk.1 — anima_tools.blk.1**:
- `status`: `open` → **`resolved`**
- `desc` 갱신: "RESOLVED 2026-05-03 사용자 directive (a) 채택. top-level anima/tool/ keep + raw 168 minimum-viable carve-out (mk2 triplet exception). 539 entries mv 마이그레이션 회피. mk2_apex per_repo_override.anima notes carve-out exception 1-line 추가 land"
- `eta`: `""` → `"2026-05-03"`
- `resolution_path` 갱신: "사용자 lock-in 'top-level keep + raw 168 carve-out' (a) 채택 → cond.1 status decision_locked → mk2_apex per_repo_override.anima.notes carve-out exception 1-line additive"

(**cond.2 + cond.3 + blk.2 변경 0건** — scope 외)

### §3.2 `hive/spec/mk2_apex.spec.yaml` per_repo_override.anima.notes carve-out append

**Before** (line 321):
```yaml
    anima:
      raw_format: mk2_inline
      roadmap_format: roadmap_v2_per_domain
      perspective: consumer            # cross-repo qrng/sim/kick consumer
      notes: "21 .roadmap.* per-domain file, 17 README.ai.md baseline grandfathered (2026-05-02)"
```

**After**:
```yaml
    anima:
      raw_format: mk2_inline
      roadmap_format: roadmap_v2_per_domain
      perspective: consumer            # cross-repo qrng/sim/kick consumer
      notes: "21 .roadmap.* per-domain file, 17 README.ai.md baseline grandfathered (2026-05-02). carve-out: anima/tool/ top-level keep + mk2 triplet exception per raw#168 minimum-viable (2026-05-03 사용자 directive (a) lock-in, .roadmap.anima_tools.cond.1=decision_locked + .blk.1=resolved; 539 entries mv 회피)"
```

**정책**:
- additive only (신규 schema field 회피, notes 에 1-line append).
- 기존 4 keys 무변경 (`raw_format`, `roadmap_format`, `perspective`, `notes`).
- carve_outs sub-section 신규 정의 회피 (기존 schema 손대지 않음, 후속 cycle 에서 정식 schema field 추가 결정).

## §4 cross-link audit (sister .roadmap)

본 cycle 변경은 .roadmap.anima_tools + mk2_apex 2 entry 만 영향, sister .roadmap cross-link 영향 0건:

| sister .roadmap | cross-link 영향 | action |
|---|---|---|
| `.roadmap.tool` (sister, generic meta cross-cut) | tool.cond.3 에서 raw 168 minimum-viable exempt + sister `.roadmap.anima_tools.cond.1` cross-link 이미 cite (변경 후에도 sister ownership 분리 정합) | NO_CHANGE |
| `.roadmap.anima_physics` | 17 sub-dir 의 raw 168 minimum-viable exempt 검토 권장 (sister pattern), 본 cycle 직접 변경 영향 0건 | NO_CHANGE |
| `.roadmap.serving` (T1) | flat 81 .hexa 에서 raw 168 minimum-viable exempt 검토 권장, 본 cycle 직접 변경 영향 0건 | NO_CHANGE |
| 기타 21 .roadmap.* | cross-link 영향 0건 | NO_CHANGE |

## §5 raw compliance audit

| raw | 정책 | 본 cycle 적합 |
|---|---|---|
| raw 1 | os-lock chflags | n/a (atomic edit, chflags 사용하지 않음) |
| raw 9 | hexa-only | additive land 자체는 hexa orchestrator 미사용 (1 .roadmap edit + 1 yaml edit + 1 doc + 1 marker = single-doc pattern, raw 168 minimum-viable exempt sister) |
| raw 10 | honest C3 caveats | inline §6 4 caveats |
| raw 11 | snake_case | 적합 |
| raw 12 | silent-error ban | 적합 (decision lock-in 모두 명시 cite) |
| raw 15 | env() lazy + <user> placeholder | env() 사용 안 함 (preserved_unchanged) |
| raw 168 | minimum-viable carve-out | **본 cycle 핵심 정책 reference** — 539 entries mv 회피 + carve-out exception lock-in |
| raw 175 | BR-NO-USER-VERBATIM | 본 doc 사용자 verbatim 인용 0건 (paraphrase only) |
| raw 270/271/272/273 | mk2 triplet | **본 cycle carve-out exception target** (raw 168 minimum-viable 으로 mandate exempt) |

## §6 raw#10 honest C3 caveats

### C1 — 신규 anima/tool/* file 정책 (carve-out exception 적용 vs anima/anima/modules/tool/ mandate)

본 cycle 은 539/532 entries 의 현재 상태에 대한 carve-out lock-in 만 처리. 추후 신규 anima_*.hexa file 이 anima/tool/ 에 추가될 경우, 그 파일이 carve-out exception 으로 처리되는지 (default), 또는 anima/anima/modules/tool/ 측 신규 sub-tree 정합 mandate 적용되는지에 대한 enforcement 정책은 본 cycle 에서 결정하지 않음 — 후속 cycle 에서 결정. 현재 raw 168 minimum-viable 정신 기준으로는 신규 file 도 carve-out 의 sister 처리를 받는 것이 default. 정식 lint hook enforcement 는 별도 cycle.

### C2 — mk2 triplet 정합 측 539/532 entries 모두 README.ai.md 미적용 honest

본 cycle 은 carve-out exception 을 lock-in 하지만, 539 (quoted) / 532 (measured) entries 모두 현재 README.ai.md 정합 0건 (raw 271 mandate 측 측 carve-out exception 으로 covered). honest disclosure: anima_*.hexa 184 actual measure (prior-doc-quote 189 대비 -5, 네이밍 variant 또는 audit 시점 차이로 추정), top-level total 532 actual (prior-doc-quote 539 대비 -7, 동일 사유). 정확한 entry inventory + ownership classification 은 후속 cycle 의 anima_tool_inventory_audit.hexa land 에서 처리.

### C3 — `decision_locked` status enum 측 mk2_apex section 6.5 status_enum 추가 후보

본 cycle 은 `decision_locked` 를 .roadmap.anima_tools.cond.1.status 에 in-place 사용했으나, hive/spec/mk2_apex.spec.yaml section 6.5 `status_enum.values` 측 에는 아직 등록하지 않음. FU1 land 의 `retired_intentional` (2026-05-03 amend) 의 sister 로 후속 cycle 에서 추가 등록 권장:
- description: "user-directive lock-in (a/b/c/...) 채택 으로 외부 결정 정책 confirmed; blocker 가 resolved 가능."
- pass_equivalence_for_coverage_gates: PASS_EQUIVALENT (decision lock-in = 정책 결정 완료, 추가 작업 미요).
- required_companion_fields: [decision_date, decision_directive, blocker_id_resolved]

본 cycle 에서 status_enum 추가는 보류 (avoid scope creep): mk2_apex amend 는 별도 cycle. 현재 measure: section 6.5 enum 측 `decision_locked` 부재 → 본 cycle 의 cond.1 status 측 schema unrecognized 가능. honest C3 acknowledgement.

### C4 — measurement vs prior-doc-quote 산술 불일치 (532 vs 539, 184 vs 189)

`.roadmap.anima_tools` 및 sister docs 측 모두 539 entries / 189 anima_-prefix 인용. 2026-05-03 본 cycle 측 mac-local find 측정:
- top-level anima/tool/* total: **532** (find -maxdepth 1 -type f) vs prior-doc-quote 539 (Δ=-7).
- anima_*.hexa prefix: **184** (find -maxdepth 1 -name "anima_*.hexa") vs prior-doc-quote 189 (Δ=-5).

가능 사유: (a) audit 시점 차이 (prior-doc 측 측 측 측 측 측 측 측 측 측 sub-cycle 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측), (b) hexa-only migration 측 측 .py exempt 정리, (c) audit 시점 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측 측. 측 측 측 측 측 측 측 측 측 측 측 측 carve-out exception lock-in 측 측 측 측 측 측 측 측 측 측 (entry count 측 carve-out 의 정의에 영향 없음 — 예외 적용 범위는 anima/tool/ top-level 전체로 정의됨). 정확한 entry inventory 는 후속 cycle anima_tool_inventory_audit.hexa land 에서 처리.

## §7 next-cycle audit candidate

post-carve-out-lock-in 후속 cycle 후보 (priority ascending):

1. **mk2_apex section 6.5 status_enum amend** — `decision_locked` 정식 등록 (C3 resolution). additive only, ~10min, $0.
2. **anima_tool_inventory_audit.hexa land** — 539/532 entries → 6 topical bucket (roadmap_meta / lint_meta / anima_domain / sub_system_family / internal_underscore_prefix / exempt_python) classification spec. raw 9 hexa-only, ~30min, $0.
3. **신규 anima/tool/* file 정책 enforcement lint hook** — carve-out default 적용 vs 정식 triplet mandate 결정 (C1 resolution). hexa lint, ~30min, $0.
4. **anima_physics + serving sister carve-out lock-in** — raw 168 minimum-viable exempt 검토 권장된 2 sister domain 의 동일 정책 lock-in (sister precedent 보강), ~15min each, $0.

## §8 마지막 결론

- 사용자 추천 (a) 채택 lock-in 완료. anima/tool/ top-level 위치 유지 + mk2 triplet exception per raw 168 minimum-viable carve-out.
- 마이그레이션 회피 (539/532 entries mv 0건). additive only (2 atomic 1-line edits + 1 handoff doc + 1 marker).
- destructive 0건, $0 mac-local. JSON + YAML parse audit 통과.
- 후속 cycle 후보 4건 (status_enum 등록 / inventory audit / 신규 file 정책 / sister carve-out).
