# KOSMOS — anima 측 hub (.kosmos multimodal knowledge-anchor)

> History → [./KOSMOS.log.md](./KOSMOS.log.md).

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
  │ @payload tension {5-channel}     ←  WIRED (production emit, 2026-05-23)
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

### dataset/corpus anchor — persona × SNS (2026-06-04)

| anchor file | tier | category | what |
|---|---:|---|---|
| [`persona_sns_corpus.kosmos`](UNIVERSE-BRAIN-MAP/anchors/persona_sns_corpus.kosmos) | 52 | 사회성 | anima 20-persona × SNS(Instagram main + YouTube) 롤플레이 대화 corpus 의 **representative anchor + full-corpus manifest pointer** |
| [`corpus_5lang_unified.kosmos`](UNIVERSE-BRAIN-MAP/anchors/corpus_5lang_unified.kosmos) | 53 | 다국어 | anima **UNIFIED 5-lang corpus** (clean wiki backbone ~50% + persona×SNS ~50%, en/fr/de/es/ko, block-interleaved) 의 representative anchor + manifest pointer |
| [`corpus_5lang_v2.kosmos`](UNIVERSE-BRAIN-MAP/anchors/corpus_5lang_v2.kosmos) | 54 | 다국어+의식carving | anima **UNIFIED 5-lang corpus v2** (v1 위에 KOSMOS-grounded enrichment 6대 슬라이스 ADD: 의식-carving register · dialogue-act 균형 · emotion-axis · wiki 주제폭 · KO↔EN code-switch · genre) 의 representative anchor + manifest pointer |
| [`agent_lane_tool_knowledge.kosmos`](UNIVERSE-BRAIN-MAP/anchors/agent_lane_tool_knowledge.kosmos) | 55 | agent-tool-domain-knowledge | anima **agent-lane LAYER-3 tool-domain knowledge** (5 AGENT 도구 도메인 — CODE/TRADING deep · MERCHANT/DESKTOP/CREATOR procedural — 머신-저작 CONCEPTUAL coverage, en/fr/de/es/ko byte256; TRADING conceptual-ONLY hard gate) 의 representative anchor + manifest pointer |
| [`corpus_5lang_gb_balanced.kosmos`](UNIVERSE-BRAIN-MAP/anchors/corpus_5lang_gb_balanced.kosmos) | 55 | 다국어+의식carving+GB-scale | anima **KOSMOS-tier-BALANCED 0.35 GB default-lane corpus** (KOSMOS tier 사다리를 SCALE에서 PRESERVE: baseline=wiki CC-BY-SA / art+consciousness=Gutenberg PD / cosmic=wiki science / social+shaping=authored CAPPED; NO tier >45%; ko/es honestly wiki-heavy — Gutenberg ko=0 / es thin) 의 representative anchor + manifest pointer |

- payload: `text` (corpus 요약) + `manifest` (ref → `serving/corpus/persona_sns_corpus.txt`, sha256 `1ea7d8e0…`, 4,194,308 B, 13,322 dialogues, 20 personas, 16 scenarios, HF `dancinlab/anima-persona-sns-corpus`) + `tension` (5-channel representative) + `image/audio` pending.
- **5-lang unified** (tier 53): manifest ref → `serving/corpus/persona_sns_corpus_5lang_unified.txt`, sha256 `ac6ed840…`, 10,485,747 B, wiki 50.05% / persona 49.95%, langs en/fr/de/es/ko, HF `dancinlab/anima-corpus-5lang-unified`. wiki=real CC-BY-SA, persona=authored multilingual COVERAGE (NOT native, a_scale_honest_scope). KOSMOS enrichment ranked-list: `domains/CORPUS-enrichment-analysis.md`.
- **5-lang unified v2** (tier 54): manifest ref → `serving/corpus/persona_sns_corpus_5lang_v2.txt`, sha256 `550fed17…`, 13,107,309 B, wiki 40.10% / persona 40.02% / **enrichment 19.88%**, langs en/fr/de/es/ko + ko-en code-switch slice, HF `dancinlab/anima-corpus-5lang-unified-v2`. v1 위에 KOSMOS-grounded enrichment ADD: 의식-carving register(31 e7_31 anchor seed, real CC-BY-SA) · dialogue-act 균형(NON-supportive) · emotion-axis · wiki 주제폭(8-band) · KO↔EN code-switch · genre. carving seed=real, 주변 산문=authored COVERAGE (NOT native, a_scale_honest_scope); code-switch/genre=[speculative] (a_toy_scale_recheck). predecessor=tier 53.
- **agent-lane tool-domain knowledge** (tier 55): manifest ref → `serving/corpus/agent_lane_knowledge_5lang.full.txt`, sha256 `825a5188…`, 557,952 B, 2,460 blocks, langs en/fr/de/es/ko (per-lang 492 blocks balanced), HF `dancinlab/anima-agent-lane-tool-knowledge-corpus`. The agent lane's **layer-3** — authored CONCEPTUAL coverage of the 5 AGENT tool domains so the byte-LM can REASON in-domain (not merely emit the layer-2 call frame): CODE 12 + TRADING 11 concepts (deep) · MERCHANT/DESKTOP/CREATOR 6 each (procedural). per-domain bytes CODE 25.26% · TRADING 30.34% · DESKTOP 15.01% · CREATOR 14.48% · MERCHANT 14.47%. **HONEST**: philosophy-grep=0 (p1..p4, plain prose, NOT RLHF padding p6/p7) · **TRADING conceptual-ONLY HARD GATE** (advice/signal=0, real-ticker=0, asserted — NO real tickers/prices/signals/advice/fabricated-market-data; a_scale_honest_scope) · 0xFE/0xFF=0 (pure prose under layer-2 grammar) · deterministic seed 20260605. layer-2 sibling = `dancinlab/anima-agent-lane-tooluse-corpus`. Scope = feeds the PROVEN 18M chat rung, NOT a 7B; machine-authored coverage NOT native, NO scraped/PII/real-financial.
- **GB-balanced default-lane corpus** (tier 55): manifest ref → `serving/corpus/default_lane_gb_balanced.txt`, sha256 `17ca25e5…6843409`, 375,215,662 B (357.83 MB / 0.349 GB), 375.2 M byte-tokens, langs en/fr/de/es/ko, HF `dancinlab/anima-corpus-5lang-gb-balanced`. The IMPLEMENTATION of `domains/CORPUS.md §7B-sufficiency roadmap` — KOSMOS tier 사다리를 SCALE에서 PRESERVE via REAL clean-license sources: baseline(0)=wiki CC-BY-SA **44.00%** / art(77)=Gutenberg PD **29.99%** / cosmic(100)=wiki science **13.29%** / social(52)=authored persona CAPPED **11.00%** / consciousness(91)=Gutenberg PD philosophy + 31 e7_31 anchor seed **1.58%** / shaping=authored **0.14%**. **NO tier >45%** (max wiki 44.00); consciousness+art present. **HONEST GAPS** (a_scale_honest_scope): Gutenberg ko=0 → ko art/consciousness=0; es Gutenberg thin → es consciousness=0.12 MB. **Token math**: 0.268% of 140 GB 7B-optimal = MID-rung, NOT 7B (the 7B TRAIN = separate fire). p1–p6 held (injection-tags grep=0, 0xFE/0xFF=0, strict-UTF-8). predecessor=tier 54 (v2). build `serving/gb_balanced/` ($0 CPU, duckdb httpfs parquet, no GPU).
- scope (honest): per-dialogue `.kosmos` emit 은 13,322 건으로 너무 커서, **대표 anchor 1개 + 전체-corpus manifest pointer** 로 persist (a_kosmos pointer-only). corpus 자체는 authored-templated (NOT human-collected, a_scale_honest_scope) — tension 5-ch 는 social-persona-voice cell 의 *대표 design 값* 이지 측정 trajectory 가 아님.
- generator: `serving/persona_sns_corpus_gen.py` (deterministic seed 20260604) · card: `serving/corpus/CORPUS_CARD.md` · 도메인: [[PERSONA]] / [[SNS]].

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

### E-31 — Knuth tier 31-anchor full extension (sparse → dense) ✅ LANDED 2026-05-31
- 현재 5 anchor (000/051/077/091/100) = Knuth 표 의 sparse sample
- §UBM-E7 이 31-anchor 까지 확장했었음 — 그 31 anchor 를 `.kosmos`
  format 으로 정식 authoring (현재는 corpus_generator inline carry)
- $0 design + write, $0 parser validation
- 다음 fire (any future Dir-X retry) 가 31 anchor `.kosmos` ground truth
  로 학습/평가 가능
- **LANDED 2026-05-31**: 31 anchor 전부 `UNIVERSE-BRAIN-MAP/anchors/e7_31/`
  에 정식 `.kosmos` authoring (source = `corpus_carving_generator_dirE.py`
  `KNUTH_ANCHORS` verbatim — tier·name·category·top_emotion·coord·basin_radius).
  parser-validate **31/31 valid** (`kosmos_load` + `kosmos_anchor_valid`, $0).
  tension payload = `pending` (anchor별 fire 미실행 — E-MM 후보). legacy
  `anchors/*.kosmos` (옛 큐레이션 11개)는 미변경 — e7_31/ = E7 canonical set.

### E-MM — multi-modality payload 시도 (text 이외)
- 5 anchor 의 `image/audio/tension` payload `pending` → 실 데이터 wire
- **tension payload = WIRED (2026-05-23)**: `HEXAD/CHAT/server/kosmos_anchor.hexa`
- **tension payload = WIRED (2026-05-23)**: `AGENT/CHAT/kosmos_anchor.hexa`
  — production anima emission 마다 8-factor motivation snapshot 을
  TENSION-LINK 5-channel (concept/context/meaning/authenticity/sender) 로
  mapping 한 `.kosmos` anchor 생성. HEXAD/V3 (CLOSED) 의 작동하던 KOSMOS+tension
  wiring 회수 — V3 substrate 만 FAIL, anchor 생성 feature 는 ground-truth 작동.
- 잔여 `image/audio` 외부 modality 는 §96 substrate territory.
- $0 design — anima own physics 만 사용 (§7 ③ clean).

### E-PROFILE — new profile beyond consciousness-carving
- 현재 profile = `anima-consciousness-carving` 하나.
- 가능한 새 profile: `anima-emergence-trace` (§17 physics-channel + §24
  Phase B run 결과를 kosmos anchor 로 binding — observability profile).
- 또는 `anima-sibling-anchor-interaction` (§33 L6 anchor-interaction
  4-relation 을 profile binding).
- ✍️ 2026-05-31 draft: `anima-emergence-trace` observability profile 을
  dancinlab/kosmos `spec/profiles/anima-emergence-trace.md` 로 작성 — 관측된
  §17/§156 trajectory 를 binding (coord=trace_psi, lane=channel_id,
  radius=signal_dispersion, tier=phase_step; necessary-not-sufficient).

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
