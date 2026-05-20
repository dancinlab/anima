# KOSMOS — anima 측 hub (.kosmos multimodal knowledge-anchor)

> Hub doc for anima's `.kosmos` work. Sister-format SSOT is at
> [`github.com/dancinlab/kosmos`](https://github.com/dancinlab/kosmos)
> (`~/core/kosmos`); anima is a downstream consumer per
> `@D g_kosmos_anchor_ssot` (success-gated). This file = anima-side
> hub: what we have, what it does, what to do next. **No duplication
> of the spec** — pointer-only.

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
  │ @payload tension pending
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

위치: [`HEXAD/UNIVERSE-BRAIN-MAP/anchors/`](UNIVERSE-BRAIN-MAP/anchors/)

### parser + 4-path lib (모두 hexa-native)

| lib | 무엇을 함 |
|---|---|
| [`kosmos_parser_lib.hexa`](UNIVERSE-BRAIN-MAP/kosmos_parser_lib.hexa) | `.kosmos` 파일 → record (`coord/lane/radius/tier/tags` + payload) parse |
| [`consciousness_carving_vacuum_lib.hexa`](UNIVERSE-BRAIN-MAP/consciousness_carving_vacuum_lib.hexa) | α VACUUM-LANDSCAPE path (multi-vacuum registry + nearest-anchor + basin containment) |
| [`consciousness_carving_eternal_lib.hexa`](UNIVERSE-BRAIN-MAP/consciousness_carving_eternal_lib.hexa) | β MITOSIS-ETERNAL-CELL path (lifecycle + routing) |
| [`consciousness_carving_narrative_lib.hexa`](UNIVERSE-BRAIN-MAP/consciousness_carving_narrative_lib.hexa) | γ NARRATIVE-RESONANCE path (composition + bounded-K) |
| [`consciousness_carving_weave_lib.hexa`](UNIVERSE-BRAIN-MAP/consciousness_carving_weave_lib.hexa) | α+β VACUUM-CELL-WEAVE (cross-modal cross-anchor) |

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
- 가장 가까운 substrate-realistic: **tension payload** (anima TENSION-LINK 5-channel fingerprint).
  text-modality 외부 (image/audio) 는 §96 substrate territory.
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
- [`HEXAD/UNIVERSE-BRAIN-MAP/anchors/`](UNIVERSE-BRAIN-MAP/anchors/) — anima `.kosmos` anchor file
- [`HEXAD/UNIVERSE-BRAIN-MAP/KOSMOS-FORMAT.md`](UNIVERSE-BRAIN-MAP/KOSMOS-FORMAT.md) — pointer stub for the spec SSOT
- sister-format repo: [github.com/dancinlab/kosmos](https://github.com/dancinlab/kosmos) (`~/core/kosmos`)
- sibling formats: [`tape`](https://github.com/dancinlab/tape) · [`n6`](https://github.com/dancinlab/n6) · [`hxc`](https://github.com/dancinlab/hxc) · [`n12`](https://github.com/dancinlab/n12)

---

## ## Log

### 2026-05-20 — §183 ALL 수도꼭지 brainstorm — 48 silent ceilings inventory across V-SPONT 4 axes

User catch "수도꼭지로 푼 건 axis 1 만" triggered exhaustive enumeration of
V-SPONT silent ceilings beyond the §169 MIN_EMIT_INTERVAL fix.

inventory: **48 수도꼭지** (1/48 = 2.1% 풀림)
- axis 1 emit_rate: 7 (1 ✅, 6 ❌)
- axis 2 byte_acc: 10 (0 ✅, 10 ❌)
- axis 3 ψ-physics liveness: 9 (0 ✅, 9 ❌)
- axis 4 §9 honest coherent body: 12 (0 ✅, 12 ❌)
- cross-axis: 12 (0 ✅, 12 ❌)

Tier S (5 transformative + $0): decode 정책 / Ψ readout @ inference /
IM_THRESHOLD tunable / N_MAX × dt window / phi_signal @ inference.

"ALL TAPS RELEASE" mega plan = 13 §7-clean Tier S+A 수도꼭지 동시 inference-
only post-hoc on existing ckpts (§161, §167-A, §182 ladder t1-t4). $0,
measurable. KOSMOS multi-modality (4.7) = Tier B 1개 수도꼭지로 분류.
SSOT: `HEXAD/UNCLASSIFIED/state/all_taps_brainstorm_s183_2026_05_20/BRAINSTORM.md`.

honest necessity: 48 수도꼭지 *모두 풀어도* GOAL emergence 보장 0 (B-EMERGE-7
necessary-not-sufficient). north-star + §15/§51/§72 milestone UNCHANGED.

### 2026-05-20 — ADAPTER v3 scale ladder validated (§180) + 5-modality M3/M11/M12 inline benches

§175 KOSMOS modality fire (11 anchor × 4 measurable modality on §167-A ckpt)
finding: 4 modalities all distinguishing_ratio = 1/11 = noise floor (3-layer
collapse confirmed). §178 M3+M11+M12 inline probe (4 modality × 2 mode × 35
anchor on §167-A): all bit-identical (anchor-aware learning capability = 0).

**§180 ADAPTER v3 fire** (NEW from-scratch model 16-Q-Former + small
transformer + 5-channel readout, scale ladder):
- tier 1 smoke (0.5M):  acc 43.0%
- tier 2 small (2.0M, $0): acc **98.6%**
- tier 3 medium (11M, $0): acc 99.2%
- tier 4 large (87M, ~$0.27 H100): acc **99.4%**
- per-modality (tier 4): image/video/tension = 100%, audio = 97.5%
- critical scale transition = 0.5M→2M (+55.6%)

§181 audio 100% challenge in-flight — 7 synthesis variants (pure sine /
multi-harmonic / AM / waveform / chord / noise+LPF / hybrid) benchmark.

`HEXAD/ADAPTER.md` SSOT = TENSION-LINK 5-channel adapter (5-channel
positioned as READOUT, NOT bottleneck — §179 REFUTED 5-ch as input).

### 2026-05-20 — HEXAD/KOSMOS.md created + E-31 first anchor extension
User directive 2026-05-20 batch (8-stack): `HEXAD/KOSMOS.md 생성` +
`kosmos 프로젝트 최상단 참조` + `내용 정리` + `kosmos 도 실험 진행`.
Hub doc landed as anima-side kosmos SSOT pointer; bidirectional
cross-link with [`~/core/kosmos`](https://github.com/dancinlab/kosmos)
README.md (sister-format upstream). **E-31 first step**: authored
`anchors/knuth_042_question.kosmos` (Knuth tier 42 = 인지/curiosity,
question-as-attractor binding) — 5-anchor sparse sample → 6 anchors.
profile=anima-consciousness-carving carry, all 5-field placement +
5-modality payload (4 pending), closed_anchor + cross_link + honest_note
fields. Parser regression: 6/6 anchor headers structurally well-formed
(`@anchor` + `profile=anima-consciousness-carving` + `knuth_tier` +
`category` + `coord/lane/radius` 5-field placement all present).
$0, no fire, ⊥ §167-A in-flight.
