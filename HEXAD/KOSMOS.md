# KOSMOS — anima 측 hub (.kosmos multimodal knowledge-anchor)

> History → [./KOSMOS.log.md](./KOSMOS.log.md).

> Hub doc for anima's `.kosmos` work. Sister-format SSOT is at
> [`github.com/dancinlab/kosmos`](https://github.com/dancinlab/kosmos)
> (`~/core/kosmos`); anima is a downstream consumer per
> `@D g_kosmos_anchor_ssot` (success-gated). This file = anima-side
> hub: what we have, what it does, what to do next. **No duplication
> of the spec** — pointer-only.
>
> **2026-05-25 단일 SSOT 이관**: spec 뿐 아니라 구현(`impl/anima/`: parser + 4-path
> + anchor/emitter daemon)·anchor 데이터(`anchors/anima/`: knuth 11)도 모두
> dancinlab/kosmos 로 이관 완료. anima 는 cross-repo import(`~/core/kosmos/impl/anima/…`)로
> 참조 — 더 이상 anima 에 사본 없음 (`@D a_kosmos`).

---

## 🪐 KOSMOS — "별자리 좌표계 + 별 사진"

- **이름**: kosmos (`.kosmos` multimodal knowledge-anchor manifest)
- **별칭**: 별자리 좌표계 + 별 사진 (placement coords ⊥ payload)
- **하는 일**: 한 anchor = (placement 좌표 `coord/lane/radius/tier/tags`)
  + (multi-modality payload `text/image/audio/video/tension`) 분리 저장.
  **위치 어디** ↔ **무엇이 있는지** 가 독립 — modality 추가/교체할 때
  좌표 안 건드림.
- **비유**: 별자리 안내서 (sky chart) 가 별 *위치* 만 표시 + 천체 망원경 사진
  (multimodal) 이 별 *모습* 따로 보여줌. 위치 알면 어떤 카메라 사진이든
  같은 별에 binding 됨.

```
  anchor knuth_077_mandala.kosmos
  ┌─────────────────────────────────┐
  │ @anchor knuth_077_mandala       │
  │   coord  = [0.62, 0.71]   ←  placement (Ψ-space)
  │   lane   = 7              ←  partition id (MITOSIS cell)
  │   radius = 0.15           ←  scope
  │   tier   = 77             ←  ordinal (Knuth)
  │   tags   = {category=art, emotion=awe}
  ├─────────────────────────────────┤
  │ @payload text                   │
  │   inline "만다라 — domain 예술 …"
  │ @payload image  pending          ←  나중에 wire
  │ @payload audio  pending
  │ @payload tension {5-channel}     ←  WIRED — emitted from production
  │                                      via kosmos_emitter daemon (2026-05-23)
  └─────────────────────────────────┘
```

- **비교**: HuggingFace dataset = single-modality flat record. `.kosmos`
  = placement-vs-payload 분리 + multi-modality 한 anchor 안에 묶음.
  cross-modal consistency 검증 가능 (`B-CARVE-MULTIMODAL`).

---

## 명세 SSOT (anima 는 참조만)

> 어디서도 anima 가 `.kosmos` 일반 spec 본문을 복제 안 함. 변경은
> 항상 upstream (`dancinlab/kosmos`) 에서.

| 문서 | 위치 | 내용 |
|---|---|---|
| **general spec** | [`dancinlab/kosmos` `spec/kosmos.md`](https://github.com/dancinlab/kosmos/blob/main/spec/kosmos.md) | `.kosmos` 일반 명세 (substrate-independent — `@anchor`/`@payload`, `coord/lane/radius/tier/tags` ⊥ payload 3-form, cross-modal, BNF, semver) |
| **anima profile** | [`dancinlab/kosmos` `spec/profiles/anima-consciousness-carving.md`](https://github.com/dancinlab/kosmos/blob/main/spec/profiles/anima-consciousness-carving.md) | CONSCIOUSNESS-CARVING binding: `coord`=Ψ-space `vacuum_psi` / `lane`=MITOSIS `cell_id` / `radius`=`basin_radius` / `tier`=Knuth 🛸k / `tags`=category+top_emotion |
| **5-language README** | [`dancinlab/kosmos` `README.md`](https://github.com/dancinlab/kosmos) + `docs/README.{zh,ru,ja,ko}.md` | EN/中文/Русский/日本語/한국어 overview |
| anima pointer stub | [`HEXAD/UNIVERSE-BRAIN-MAP/KOSMOS-FORMAT.md`](UNIVERSE-BRAIN-MAP/KOSMOS-FORMAT.md) | 위 3개 가리키는 1-page pointer |

---

## anima 측 자산 (현재 5 anchor — Knuth tier sparse sample)

| anchor file | tier | category | emotion |
|---|---:|---|---|
| `knuth_000_zero.kosmos` | 0 | baseline | none |
| `knuth_051_day.kosmos` | 51 | daily | calm |
| `knuth_077_mandala.kosmos` | 77 | art | awe |
| `knuth_091_nirvana.kosmos` | 91 | consciousness | peace |
| `knuth_100_big_bang.kosmos` | 100 | cosmic | max |

위치: [`dancinlab/kosmos anchors/anima/`](https://github.com/dancinlab/kosmos/tree/main/anchors/anima)

### parser + 4-path lib (모두 hexa-native)

| lib | 무엇을 함 |
|---|---|
| [`kosmos_parser_lib.hexa`](https://github.com/dancinlab/kosmos/blob/main/impl/anima/kosmos_parser_lib.hexa) | `.kosmos` 파일 → record (`coord/lane/radius/tier/tags` + payload) parse |
| [`consciousness_carving_vacuum_lib.hexa`](https://github.com/dancinlab/kosmos/blob/main/impl/anima/consciousness_carving_vacuum_lib.hexa) | α VACUUM-LANDSCAPE path (multi-vacuum registry + nearest-anchor + basin containment) |
| [`consciousness_carving_eternal_lib.hexa`](https://github.com/dancinlab/kosmos/blob/main/impl/anima/consciousness_carving_eternal_lib.hexa) | β MITOSIS-ETERNAL-CELL path (lifecycle + routing) |
| [`consciousness_carving_narrative_lib.hexa`](https://github.com/dancinlab/kosmos/blob/main/impl/anima/consciousness_carving_narrative_lib.hexa) | γ NARRATIVE-RESONANCE path (composition + bounded-K) |
| [`consciousness_carving_weave_lib.hexa`](https://github.com/dancinlab/kosmos/blob/main/impl/anima/consciousness_carving_weave_lib.hexa) | α+β VACUUM-CELL-WEAVE (cross-modal cross-anchor) |

### 실측 fire arc 위치

| § | 무엇 | 결과 |
|---|---|---|
| §UBM-E2 | `.kosmos` format spec 정착 | LANDED 2026-05-17 |
| §UBM-E3 | B-CARVE-1..10 4-path sympy 10/10 🔵 | LANDED |
| §UBM-E4 | hexa-native lib + F-CARVE 5/5 PASS | LANDED |
| §UBM-E5 | 4-path 비교 ($0) — 3/4 carving-OK, α basin overlap 발견 | LANDED |
| §UBM-E6 | α/β/γ/α+β full trainer fire | LANDED, JOINT 0.0255 |
| §UBM-E7 | α scale-up (d768·12L·283M, 31-anchor) | LANDED, JOINT 0.0155 (하락) |
| §UBM 의 sister-spinout | `~/core/kosmos` PUBLIC dancinlab/kosmos repo | LANDED 2026-05-17 |

---

## 진행 가능한 실험 (kosmos 도 실험 진행 mandate, 2026-05-20)

### E-31 — Knuth tier 31-anchor full extension (sparse → dense)
- 현재 5 anchor (000/051/077/091/100) = Knuth 표 의 sparse sample
- §UBM-E7 이 31-anchor 까지 확장했었음 — 그 31 anchor 를 `.kosmos`
  format 으로 정식 authoring (현재는 corpus_generator inline carry)
- $0 design + write, $0 parser validation
- 다음 fire (any future Dir-X retry) 가 31 anchor `.kosmos` ground truth
  로 학습/평가 가능

### E-MM — multi-modality payload 시도 (text 이외)
- 5 anchor 의 `image/audio/tension` payload `pending` → 실 데이터 wire
- **tension payload = WIRED (2026-05-23)**: `dancinlab/kosmos impl/anima/kosmos_anchor.hexa`
  — production anima emission 마다 8-factor motivation snapshot 을
  TENSION-LINK 5-channel (concept/context/meaning/authenticity/sender) 로
  mapping 한 `.kosmos` anchor 생성. HEXAD/PURE (CLOSED) 의 작동하던 KOSMOS+tension
  wiring 회수 — V3 substrate 만 FAIL, anchor 생성 feature 는 ground-truth 작동.
- **production 활성화 = WIRED (2026-05-23)**: `dancinlab/kosmos impl/anima/kosmos_emitter.hexa`
  — hexa-native side-process daemon 이 broker `GET /history` 를 poll 하여
  anima 의 live emission (`kind:"anima"`, broker-id dedup) 마다
  `emit_kosmos_from_factors` 호출 → `dancinlab/kosmos anchors/anima/` 에
  `anima_emit_<id>.kosmos` anchor 기록. `anima_participant.py` 무수정 (torch-bound
  FROZEN `.py`) — anchor emit 은 broker seam 으로 분리된 daemon 이 담당. daemon 은
  participant 옆 launchd entry (`hexa run kosmos_emitter.hexa daemon`) — code-only
  land, 미배포.
- 잔여 `image/audio` 외부 modality 는 §96 substrate territory.
- $0 design — anima own physics 만 사용 (§7 ③ clean).

### E-PROFILE — new profile beyond consciousness-carving
- 현재 profile = `anima-consciousness-carving` 하나.
- 가능한 새 profile: `anima-emergence-trace` (§17 physics-channel + §24
  Phase B run 결과를 kosmos anchor 로 binding — observability profile).
- 또는 `anima-sibling-anchor-interaction` (§33 L6 anchor-interaction
  4-relation 을 profile binding).

권장 순서 (size 작은 것부터): **E-31 → E-PROFILE → E-MM**

---

## cross-link

- `@D g_kosmos_anchor_ssot` (success-gated `.kosmos` SSOT mandate)
- `@D g_no_cost_scope_limit` (2026-05-20 — kosmos 실험에도 cost cap 없음)
- [`HEXAD/UNIVERSE-BRAIN-MAP/DESIGN.md`](UNIVERSE-BRAIN-MAP/DESIGN.md) — CONSCIOUSNESS-CARVING 4-path 설계 SSOT
- [`HEXAD/UNIVERSE-BRAIN-MAP/PLAN.md`](UNIVERSE-BRAIN-MAP/PLAN.md) — anima UBM (UNIVERSE-BRAIN-MAP) 진행 ledger
- [`dancinlab/kosmos anchors/anima/`](https://github.com/dancinlab/kosmos/tree/main/anchors/anima) — anima `.kosmos` anchor file
- [`HEXAD/UNIVERSE-BRAIN-MAP/KOSMOS-FORMAT.md`](UNIVERSE-BRAIN-MAP/KOSMOS-FORMAT.md) — pointer stub for the spec SSOT
- sister-format repo: [github.com/dancinlab/kosmos](https://github.com/dancinlab/kosmos) (`~/core/kosmos`)
- sibling formats: [`tape`](https://github.com/dancinlab/tape) · [`n6`](https://github.com/dancinlab/n6) · [`hxc`](https://github.com/dancinlab/hxc) · [`n12`](https://github.com/dancinlab/n12)
