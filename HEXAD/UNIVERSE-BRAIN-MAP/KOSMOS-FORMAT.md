# KOSMOS-FORMAT.md — `.kosmos` 포맷 spec 은 dancinlab/kosmos 에 있음 (pointer)

> **이 파일은 pointer stub.** `.kosmos` 멀티모달 knowledge-anchor manifest 포맷의 명세는 sister-format repo **[`dancinlab/kosmos`](https://github.com/dancinlab/kosmos)** (`~/core/kosmos`) 에만 둔다 — anima 는 중복 보관하지 않고 참조만 (user directive 2026-05-18 "anima 에 kosmos 문서 있으면 kosmos 에만 놔두고 참조하는 형태로").

## `.kosmos` 포맷 명세 위치 (SSOT = dancinlab/kosmos)

| 문서 | 위치 | 내용 |
|---|---|---|
| **general spec** | `~/core/kosmos/spec/kosmos.md` ([dancinlab/kosmos](https://github.com/dancinlab/kosmos/blob/main/spec/kosmos.md)) | `.kosmos` 일반 명세 (substrate-independent — `@anchor`/`@payload`, placement 좌표 `coord/lane/radius/tier/tags` ⊥ payload 3-form, cross-modal, BNF, semver, 버전 이력) |
| **anima profile** | `~/core/kosmos/spec/profiles/anima-consciousness-carving.md` | anima CONSCIOUSNESS-CARVING binding (general → anima 매핑: `coord`=Ψ-space `vacuum_psi` / `lane`=MITOSIS `cell_id` / `radius`=`basin_radius` / `tier`=Knuth 🛸k / `tags`=category+top_emotion). dancinlab/anima HEXAD/UNIVERSE-BRAIN-MAP = profile reference impl |
| **5-language README** | `~/core/kosmos/README.md` + `docs/README.{zh,ru,ja,ko}.md` | overview (EN/中文/Русский/日本語/한국어) |

## anima 측 운영

- `.kosmos` 구현·anchor 도 2026-05-25 dancinlab/kosmos 로 이관 (단일 SSOT): `impl/anima/` (parser + 4-path + daemon) + `anchors/anima/*.kosmos`. anima 는 cross-repo import 로 참조 — 사본 미보관 (`@D a_kosmos`).
- 일반 `.kosmos` 문법 변경/버전 업그레이드 = `dancinlab/kosmos` `spec/kosmos.md` (semver, §버전 이력) 에서. anima 는 따라감.
- anima profile (CONSCIOUSNESS-CARVING binding) 변경 = `dancinlab/kosmos` `spec/profiles/anima-consciousness-carving.md` 갱신.

## cross-link

- [`DESIGN.md`](DESIGN.md) — CONSCIOUSNESS-CARVING 4-path 설계 SSOT (anima 측)
- [`PLAN.md`](PLAN.md) · [`UNIVERSE-BRAIN-MAP.tape`](UNIVERSE-BRAIN-MAP.tape) — anima UNIVERSE-BRAIN-MAP
- [`dancinlab/kosmos anchors/anima/`](https://github.com/dancinlab/kosmos/tree/main/anchors/anima) — anima `.kosmos` anchor (2026-05-25 이관)
- `AGENTS.tape @D g_kosmos_anchor_ssot` — `.kosmos` = anchor canonical SSOT (success-gated)
- **명세 SSOT**: github.com/dancinlab/kosmos (이 파일은 그 pointer)

> 이전 이 파일에 있던 `.kosmos` 포맷 명세 본문 (kosmos-format/1.0, 8 §) 은 dancinlab/kosmos spin-out (commit `6b482c969`) 시 `~/core/kosmos/spec/` 로 이관 완료. 본 파일은 2026-05-18 pointer stub 으로 축소 (중복 제거 — user directive "kosmos 에만 놔두고 참조"). 16개 참조 파일의 경로 유지 위해 파일 자체는 존속.
