# `.own N` namespace + `tool/transient_py/` formalization landing — 2026-05-03

## TL;DR (사용자 친화 요약)

`tool/transient_py/` namespace 측 + `.own N` declaration grammar 측 informal spec 측 land 했습니다. 4 levels (1=grandfathered / 2=transpiler auto-gen / 3=raw#37 transient sister / 4=test fixtures) 측 정의, dir scaffold (`.gitkeep` + `.gitignore` + `README.md`) 측 created, root `.gitignore` 측 명시 block 측 추가. 이번 cycle 측 .py 0 created, 기존 .own 1 grandfathered 4 files 측 + 기존 raw#37 ~25 helpers 측 모두 untouched. 측정 ratification (`anima/.own` 측 `own N` formal entry) 측 Track A transpiler 첫 .own 2 artifact land 후 cycle 2 측 deferred.

## 1. 결정 (사용자 lock-in 보류 — 사용자 추후 ratification 검토)

- **선택**: informal namespace land (cycle 1만 — namespace dir + spec doc + .gitignore 측), formal `anima/.own` entry 측 deferred
- **이유**: Track A transpiler 측 첫 real `.own 2` artifact 측 측정 후 level taxonomy 정합 검증 필요. Premature codification 측 raw#20 own-monotonic violation 측 위험
- **C3 caveat**: 4 levels speculative — 실제 사용 패턴 측 cycle 2 측 ratification 시 재검증

## 2. 4 `.own` levels (proposed taxonomy)

| level | semantics | git tracked? | count (current) | example |
|---|---|---|---|---|
| `.own 1` | grandfathered legacy `.py` (anima/.own own 1 opt-out list) | YES | 4 | `tool/active_redteam_dEF_proto.py`, `tool/anima_holographic_ib_ksg_validate_prod.py` |
| `.own 2` | transpiler auto-gen output (regen on demand) | NO | 0 | (future) `tool/transient_py/atp_pytorch.py` |
| `.own 3` | transient sister-rule (raw#37 helper) | NO | ~25 | `state/.hjorth_helper.py`, `state/.berger_alpha_gate_helper.py` |
| `.own 4` | test fixtures (auto-gen test harness) | NO | 0 | (future) `tool/transient_py/_fixture_*.py` |

## 3. Header template (mandatory for `.own 2/3/4`)

```python
# .own 2
# generator: tool/atp_to_pytorch.hexa
# source: anima-voice/audio_token_predictor.hexa@a6293670c
# generated: 2026-05-03T22:00:00Z
# retire-when: tool/atp_to_pytorch.hexa updated OR source .hexa changed
```

- `# .own N` MUST be first non-shebang comment line
- `N ∈ {1, 2, 3, 4}`
- Level-conditional fields per §3 of spec (`.own 1` header optional grandfather; `.own 2` requires all 4; `.own 3` minimal; `.own 4` no `source`)

## 4. 변경 사항

### 4-1. NEW directory: `tool/transient_py/`

```
tool/transient_py/
├── .gitkeep        # preserve empty dir in git
├── .gitignore      # namespace-local policy (mirrors root + negates metadata)
└── README.md       # namespace explanation + 4-level table + lifecycle
```

### 4-2. Root `.gitignore` (modified — block added)

```gitignore
# tool/transient_py/ — auto-generated python namespace (.own 2/3/4)
# Spec: docs/anima_dot_own_namespace_spec_2026_05_03.md
tool/transient_py/*.py
tool/transient_py/__pycache__/
!tool/transient_py/.gitkeep
!tool/transient_py/.gitignore
!tool/transient_py/README.md
```

(Redundant with `**/*.py` ban at top, but documented at namespace declaration site for audit traceability — raw 91 explicit-over-implicit C5 honest disclosure.)

### 4-3. NEW spec doc

- `docs/anima_dot_own_namespace_spec_2026_05_03.md` (~280 LoC)
- 11 sections (motivation / grammar / 4 levels / .gitignore policy / validator-proposed / migration plan / cross-link / dir state / validation / 4 C3 caveats / references)

### 4-4. NEW handoff doc

- `docs/anima_dot_own_namespace_spec_landed_2026_05_03.ai.md` (this file)

### 4-5. NEW marker

- `state/markers/anima_dot_own_namespace_spec_landed.marker`

### 4-6. NOT changed (raw#9 STRICT honored)

- `anima/.own` — NO new `own N` entry (deferred to cycle 2)
- `tool/active_redteam_dEF_proto.py` — untouched (.own 1 grandfather)
- `tool/active_redteam_prototype.py` — untouched (.own 1 grandfather)
- `tool/anima_holographic_ib_ksg_validate_prod.py` — untouched (.own 1 grandfather)
- `state/.*_helper.py` ~25 files — untouched (no .own 3 backfill this cycle)
- No `tool/dot_own_validate.hexa` installed (proposed only)

## 5. `.gitignore` policy summary

| level | tracked? | mechanism |
|---|---|---|
| `.own 1` | YES | existing repo state; managed via anima/.own own 1 |
| `.own 2` | NO | `**/*.py` root ban + tool/transient_py/*.py explicit doc block |
| `.own 3` | NO | root `.gitignore` lines 187-191 + `state/.<name>_helper.py` glob |
| `.own 4` | NO | shared with .own 2 (tool/transient_py/) |

## 6. Validator (PROPOSED — separate cycle 3)

- **Tool**: `tool/dot_own_validate.hexa` (NOT installed this cycle)
- **Selftest emission**: `__DOT_OWN_VALIDATE_SELFTEST__ <PASS|FAIL> n=5 fail=<M>`
- **F-OWN-1 falsifier**: every Mac-side .py declares valid `.own N` header (action-on-fail: strengthen)
- **Severity ramp**: warn → block 30d post-Track-A first artifact

## 7. Migration plan (cycles)

| cycle | scope | status |
|---|---|---|
| **1 (THIS)** | namespace + .gitignore + spec + handoff + marker | LANDED 2026-05-03 |
| **2** | first `.own 2` artifact lands → ratify into anima/.own | DEFERRED (Track A dep) |
| **3** | install `tool/dot_own_validate.hexa` + F-OWN-1 | PROPOSED |
| **4** | backfill `.own 1` headers in 4 grandfathered files | PROPOSED |
| **5** | backfill `.own 3` headers in ~25 state helpers | PROPOSED |
| **6** | severity ramp warn → block | DEFERRED (30d gate) |

## 8. Validation results (this cycle)

| check | result |
|---|---|
| `tool/transient_py/` directory exists | PASS |
| `.gitkeep` + `.gitignore` + `README.md` present | PASS |
| Root `.gitignore` documents tool/transient_py/*.py | PASS |
| No `.py` created | PASS (raw#9) |
| No `.own 1` grandfathered file modified | PASS |
| No `state/.*_helper.py` modified | PASS |
| Spec doc + handoff doc + marker emitted | PASS |
| `anima/.own` not modified (informal cycle) | PASS (intentional) |
| Cost | $0 |

## 9. 4 honest C3 caveats (raw 91)

1. **Ratification is INFORMAL** — no `own N` entry in `anima/.own` yet; spec lives only in `.md` + dir scaffold. Formal entry deferred to cycle 2 to avoid premature codification.
2. **Level definitions are SPECULATIVE** — 4-level taxonomy is proposal informed by current 4 grandfathered + 25 raw#37 helpers + 0 transpiler outputs. Track A first artifact may force merge or split.
3. **Retirement enforcement is TBD** — `retire-when` field is free-form text; no automated GC. Operator-discipline only until `tool/dot_own_gc.hexa` (future cycle).
4. **Audit tooling is FUTURE CYCLE** — `tool/dot_own_validate.hexa` + F-OWN-1 are PROPOSED only. Currently unrunnable. The 4 grandfathered files do NOT carry `.own 1` headers (backfill cycle 4).

## 10. Cross-link

- Spec: `/Users/ghost/core/anima/docs/anima_dot_own_namespace_spec_2026_05_03.md`
- Marker: `/Users/ghost/core/anima/state/markers/anima_dot_own_namespace_spec_landed.marker`
- Namespace: `/Users/ghost/core/anima/tool/transient_py/{.gitkeep,.gitignore,README.md}`
- Root .gitignore modified: `/Users/ghost/core/anima/.gitignore` (block appended after `state/experiment/`)
- Related rules: anima/.own own 1 (grandfather list), raw#9 (hexa-only mandate), raw#37 (helper /tmp transient sister), raw#0 (root SSOT), raw#20 (own-monotonic), raw#71 (cite-of-violation), raw#91 (C1-C5 honest), raw#95 (triad-universal), hive/.raw.mk2 lint.001 (`*_lint.hexa` convention)
- Cross-sister context: hexa-lang upstream audit recommendation; Track A transpiler prototype sister BG a6293670c

## 11. 후속 cycles 측 측 측 (사용자 검토 필요)

- **cycle 2 trigger**: Track A transpiler 측 첫 `.py` artifact 측 emit 시 → `anima/.own` 측 `own N` formal entry 측 추가 (4-level taxonomy 측 측정 검증 후)
- **cycle 3 trigger**: cycle 2 land 후 → `tool/dot_own_validate.hexa` 측 install + F-OWN-1 측 emission
- **cycle 4-5 trigger**: cycle 3 land 후 → header backfill (4 grandfathered + 25 state helpers, ONE-TIME, body 측 변경 없음)
- **cycle 6 trigger**: cycle 4-5 land 후 30d clean streak → severity warn → block ramp

---

**End of handoff.**
