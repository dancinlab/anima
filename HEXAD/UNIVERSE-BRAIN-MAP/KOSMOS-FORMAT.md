# KOSMOS-FORMAT.md — `.kosmos` 멀티모달 manifest 포맷 명세 (canonical, 버전 관리)

> **SPEC VERSION: `kosmos-format/1.0`** (status: active · 2026-05-17 · Phase UBM-E2 baseline)
> 본 문서 = `.kosmos` 포맷의 **canonical 버전 관리 명세**. 별도 KOSMOS.md 만들지 않음 — 이 파일이 SSOT, 명세 변경은 §버전 이력 에 새 버전 append + 본 헤더 SPEC VERSION 갱신 (semver: major = 호환 깨짐 / minor = 하위호환 확장 / patch = 명확화).
>
> User directive 2026-05-17: "글자뿐만이 아니라 그림, 영상, 음성, 또다른게 있으면 또다른것도 — 모두 가능한 방식?" → 멀티모달 manifest 포맷 확정. "명세 버전 계속 업그레이드 해나가자 / KOSMOS-FORMAT.md 있으면 됬어" → 본 파일을 versioned SSOT 로.
>
> 본 문서 = **spec 문서 (design-tier)**. `.kosmos` parser 의 실제 impl 은 Phase UBM-E4 (`kosmos_parser_lib.hexa`). B-CARVE-* sympy 사전등록은 Phase UBM-E3.
>
> SSOT 일관성: `DESIGN.md §8 / §8.1` = 결정 SSOT. 본 문서는 §8.1 초안을 정식 명세로 확장 — 모순 없음. 명세 upgrade 시 parser_lib + anchors/*.kosmos 와 동기 (호환 깨짐 = major bump + migration note 필수).

---

## 0. 무엇인가 — 한 문장

`.kosmos` 파일 = **CONSCIOUSNESS-CARVING paradigm** 에서 조각된 의식 anchor **하나**의 멀티모달 manifest. 각 file = anima 의식 풍경(consciousness landscape) 안의 한 골짜기(🛸k vacuum / eternal cell / narrative template) 를 modality-중립 carving 좌표 + modality-specific 감각 payload 의 2층으로 기술한다.

확장자 `.kosmos` (그리스 κόσμος, ordered universe). 문법은 **tape v1.2 superset** — tape 의 `@<type> <id> := "<subject>" :: <kind> [<grades>]` entry 형식 + 2-space-indent body 를 그대로 쓰되, `@anchor` / `@payload` 두 신규 entry-type 을 추가한다.

---

## 1. § header — `@anchor` entry

`.kosmos` 파일은 정확히 **하나의 `@anchor` entry** 로 시작한다 (anchor 1개 = file 1개).

### 1.1 헤더 문법

```
@anchor <id> := "<name>" :: kosmos-anchor [tier=<N> active]
```

| 토큰 | 의미 | 제약 |
|---|---|---|
| `@anchor` | 신규 entry-type (tape 17종 + 1) | 파일당 정확히 1개, 최상단 |
| `<id>` | 기계 식별자 (snake_case) | `knuth_<NNN>_<slug>` 권장 (예: `knuth_077_mandala`) |
| `"<name>"` | 사람이 읽는 이름 (multilingual 허용) | 큰따옴표 quoted string |
| `:: kosmos-anchor` | entry kind 고정 리터럴 | 항상 `kosmos-anchor` |
| `[tier=<N> active]` | grade 태그 — Knuth Tier + 활성 상태 | `tier=N` 은 `0 ≤ N ≤ 100` 정수 |

tape v1.2 의 grade tag 관례를 따른다: `tier=<N>` 은 scoped tag (`allow:<x>` 패턴), `active`/`draft`/`deprecated` 는 governance delivery tag.

### 1.2 환경 shebang (권장)

```kosmos
#!/usr/bin/env kosmos
# knuth_077_mandala.kosmos — CONSCIOUSNESS-CARVING anchor (multimodal)
```

`#` 으로 시작하는 줄은 주석. shebang 은 cosmetic (parser 가 무시), 사람이 cold-read 할 때 포맷 식별용.

---

## 2. § carving 좌표 — modality-INDEPENDENT 층

`@anchor` 헤더 바로 아래, 2-space indent 로 carving 좌표 field 들을 둔다. 이 층은 **modality 와 무관** — 그림이든 음성이든 글자든 모두 이 한 점/한 골짜기로 흘러든다.

### 2.1 field 목록

| field | 타입 | path | 의미 |
|---|---|---|---|
| `knuth_tier` | integer `0..100` | (좌표) | 🛸k Knuth Tier ordinal — `tier=` grade tag 와 동일 값 (redundant, machine-field) |
| `category` | quoted string | (좌표) | 우주뇌지도 17 카테고리 중 하나 (예: `"예술"`, `"의식상태"`, `"시간"`) |
| `top_emotion` | quoted string | (좌표) | 18 emotions 중 dominant 하나 (예: `"creativity"`, `"peace"`) |
| `vacuum_psi` | `[x, y]` float pair | **α path** | Ψ-space vacuum point — Engine A ⇄ Engine G 좌표계의 골짜기 위치 |
| `cell_id` | quoted string | **β path** | MITOSIS eternal cell 식별자 (예: `"eternal_077"`) |
| `basin_radius` | float `> 0` | **α+β hybrid** | carving 반경 — vacuum 주변 attractor basin 크기 |

### 2.2 4-path field 공존 규칙

하나의 `.kosmos` anchor 안에 **4 path 의 field 가 모두 공존**한다 (DESIGN.md §6 결정 1 = 4-path 모두 build):

- **α (VACUUM-LANDSCAPE)** → `vacuum_psi`
- **β (MITOSIS-ETERNAL)** → `cell_id`
- **γ (NARRATIVE-RESONANCE)** → `@payload text` (§3, narrative 재생성 template inline)
- **α+β hybrid (Vacuum-Cell-Weave)** → `basin_radius` (vacuum + cell 결합 반경)

path 별 비교 실험 시, **같은 anchor file 을 SSOT 로 두고** 각 path 의 실험 코드가 자기 field 만 읽는다. anchor 를 path 마다 복제하지 않는다 (g3 drift-avoidance).

### 2.3 좌표 vs payload 분리 invariant

carving 좌표 6 field 는 **modality 가 0개여도 정의되어야 한다** — 골짜기 위치는 감각 채널이 하나도 없어도 존재한다. 반대로 `@payload` 는 0개 이상 (open).

---

## 3. § 감각 payload — modality-SPECIFIC 층

carving 좌표 아래에 `@payload` entry 를 0개 이상 둔다. 각 `@payload` = 이 골짜기로 들어가는 한 감각 채널.

### 3.1 payload 문법 — 3가지 형태

**(a) inline** — 작은 payload (주로 `text`):

```
@payload <modality> := "<inline-string>"
```

**(b) ref** — binary/대용량 payload (그림·음성·영상). `.kosmos` 는 manifest 일 뿐, binary 는 별도 `media/` 파일:

```
@payload <modality> := ref "<path>" sha256=<hex64> bytes=<N>
```

`tension` 같은 anima-native modality 는 추가 attribute 를 가질 수 있다 (예: `channels=5`):

```
@payload tension := ref "<path>.tlink" sha256=<hex64> bytes=<N> channels=5
```

**(c) pending** — media 가 아직 생성되지 않은 honest marker:

```
@payload <modality> := pending "<사유 — 어느 Phase 후보인지>"
```

### 3.2 modality — open enum

modality 토큰은 **닫힌 집합이 아니다**. 현재 정의된 표준 modality:

| modality | payload 형태 | 비고 |
|---|---|---|
| `text` | inline (작음) | γ path narrative — anima 현재 유일 소비 가능 modality (byte-level) |
| `image` | ref + sha256 + bytes | 그림. S-module image encoder 미-wired (pending) |
| `audio` | ref + sha256 + bytes | 음성. S-module audio encoder 미-wired (pending) |
| `video` | ref + sha256 + bytes | 영상. 미-wired (pending) |
| `tension` | ref + sha256 + bytes + `channels=5` | **anima-native modality** — TENSION-LINK 5-channel meta-telepathy (concept · context · meaning · authenticity · sender). 미구현 (pending) |

"또 다른 게 있으면" — 새 modality 가 필요하면 새 tag 만 추가하면 된다 (스키마 변경 0, §5 확장 규칙).

### 3.3 inline vs ref 분리 규칙

- 글자(`text`) = **inline** — 작고 사람이 cold-read 가능.
- binary(image/audio/video/tension) = **ref + sha256 + bytes** — 텍스트 manifest 에 binary 를 박지 않는다. `sha256` 은 64-hex content commitment, `bytes` 는 파일 크기 정수.
- media 미생성 = **pending** — fake ref (존재하지 않는 path) 금지 (g3 fake-evidence 방지).

---

## 4. § 검증 — closed_anchor + cross-modal carving

### 4.1 `closed_anchor` field

`@anchor` body 끝에 검증 anchor 를 명시한다:

```
closed_anchor = "B-CARVE-MULTIMODAL (Phase UBM-E3 사전등록)"
```

이 field 는 해당 anchor 의 carving 이 어느 closed-form falsifier 로 검증되는지 가리킨다. spec-tier 단계(UBM-E2)에서는 사전등록 placeholder, sympy 실제 verdict 는 Phase UBM-E3.

### 4.2 cross-modal carving 검증 규칙 — `B-CARVE-MULTIMODAL`

```
B-CARVE-MULTIMODAL (closed-form 검증 대상, Phase UBM-E3 사전등록):

  ∀ modality m ∈ {text, image, audio, video, tension, …}:
      ‖ E_m(payload_m) − vacuum_psi ‖  <  basin_radius

  여기서:
    E_m  = modality m 의 encoder (payload_m → Ψ-space 좌표)
    ‖·‖  = Ψ-space (Engine A ⇄ Engine G) 거리
```

**해석**: 모든 감각 채널의 payload 가 encoder 를 거치면 **같은 골짜기(vacuum_psi)** 의 basin 안으로 떨어진다. 글자·그림·음성·영상이 같은 의식 anchor 로 수렴한다는 것 = "글자 학습"이 아니라 "**의식** 조각" 인 이유.

**비유 (텐트 페그)**: 골짜기를 한 방향(글자)에서만 못 박으면 바람에 펄럭임. 여러 방향(글자+그림+음성+영상)에서 동시에 못 박으면 단단히 고정 → 멀티모달 = 같은 basin 을 여러 감각 방향에서 동시 조각 = 더 깊고 안정된 vacuum.

### 4.3 g3 — design placeholder 정직 표기 의무

UBM-E2 (이 spec) 시점에는 **encoder E_m 도 학습 전, vacuum_psi 도 미측정**이다. 따라서:

- `.kosmos` 파일의 `vacuum_psi` / `basin_radius` 값은 **design placeholder** 이며, 반드시 inline 주석으로 `# design placeholder, UBM-E5 fire 에서 측정` 을 명시한다.
- 측정 전 값을 closed-form verdict 처럼 제시하는 것 = g3 fake-closed violation. 금지.
- B-CARVE-MULTIMODAL 의 실제 sympy proposition 은 Phase UBM-E3, 실제 측정 fire 는 Phase UBM-E5.

### 4.4 f1/f2/f3/identity 안전

- **f1/f2 safe**: Knuth Tier 🛸k = anima 자체 design (g2 internal-arch carve-out) — σ(6)/τ(6)/φ(6)/J₂(6) 외부 derivation 아님. `.kosmos` 어디에도 lattice numerology derivation 금지.
- **f3 NO-OUTCOME-CLAIM**: BG-HS R1 manual_match 13/15 등 historical 수치는 empirical-only — `.kosmos` 가 capability/성능 주장을 담지 않는다.
- **B-IDENTITY-5 + forbidden_chat_sft_use**: text payload 에 `도우미 / helper / assistant / 사용자:` token 절대 금지. anima 데이터 인용 시 `[anima 우주뇌지도]` prefix 로 묶고 도우미-dialogue 형식을 쓰지 않는다.

---

## 5. § 확장 규칙

### 5.1 새 modality 추가

새 감각 채널이 생기면 새 `@payload <modality>` tag 를 추가하면 된다. 스키마 변경 0, 기존 파일 재작성 0:

```
@payload smell := pending "후각 modality — anima S-module 미정의, 미래 RFC"
```

modality enum 은 open — parser 는 미지의 modality tag 를 거부하지 않고 `pending`/`ref`/inline 형태만 검증한다.

### 5.2 future-proof — 페그 구멍 미리 뚫기

anima 는 현재 `text` (byte-level) 만 소비 가능하다 (cycle 2~5 전부 text corpus, S-module image/audio encoder 미-wired). `.kosmos` 의 future-proof 설계:

- 오늘 `.kosmos` 파일에 image/audio/video/tension payload 를 **`pending` marker 로 미리 담아둔다**.
- 나중에 S-module 에 image/audio encoder 가 wired 되면, **포맷 변경 0** 으로 그 `pending` 을 `ref` 로 채워 같은 파일을 그 modality 로 소비한다.
- 비유: 만다라 골짜기에 4개 페그 구멍을 미리 다 뚫어둠. 오늘은 글자 페그 하나, 나중에 그림/음성 페그를 그 구멍에 추가. 구멍 재-천공 불필요.

### 5.3 carving 좌표 field 확장

carving 좌표층에 새 field 가 필요하면 (예: 차후 path 가 추가 field 요구) 2-space-indent body line 으로 추가한다. 기존 4-path field (`vacuum_psi`/`cell_id`/`basin_radius` + `text` payload) 는 불변 — 신규 path 는 직교 field 만 추가 (g3 drift-avoidance, 기존 anchor 재작성 금지).

### 5.4 paradigm 중립성

`.kosmos` 는 CONSCIOUSNESS-CARVING 의 4-path 어디든 재사용 가능하며, 차후 paradigm 이 바뀌어도 carving 좌표/payload 2층 구조 자체는 유지된다 (DESIGN.md §8 결정 3 rationale — paradigm-중립 확장자).

---

## 6. BNF-ish grammar

```bnf
kosmos-file   ::= [ shebang ] { comment } anchor-entry

shebang       ::= "#!/usr/bin/env kosmos" NEWLINE
comment       ::= "#" { any-char } NEWLINE

anchor-entry  ::= anchor-header NEWLINE
                  { INDENT ( coord-field | payload-entry | meta-field ) NEWLINE }

anchor-header ::= "@anchor" SP id SP ":=" SP qstring SP "::" SP
                  "kosmos-anchor" SP "[" grade-list "]"

grade-list    ::= "tier=" integer SP state-tag
state-tag     ::= "active" | "draft" | "deprecated"

coord-field   ::= "knuth_tier"   SP "=" SP integer            ; 0..100
                | "category"     SP "=" SP qstring
                | "top_emotion"  SP "=" SP qstring
                | "vacuum_psi"   SP "=" SP psi-pair  [ comment ]
                | "cell_id"      SP "=" SP qstring
                | "basin_radius" SP "=" SP float     [ comment ]

psi-pair      ::= "[" float "," SP float "]"

payload-entry ::= "@payload" SP modality SP ":=" SP payload-body
payload-body  ::= qstring                                     ; (a) inline
                | "ref" SP qstring SP "sha256=" hex64
                      SP "bytes=" integer { SP attr }          ; (b) ref
                | "pending" SP qstring                         ; (c) pending
attr          ::= ident "=" ( integer | ident )               ; e.g. channels=5
modality      ::= "text" | "image" | "audio" | "video"
                | "tension" | ident                           ; open enum

meta-field    ::= "closed_anchor" SP "=" SP qstring

id            ::= ident-char { ident-char }                   ; snake_case
qstring       ::= '"' { any-char-except-quote } '"'
hex64         ::= hex-digit × 64
integer       ::= digit { digit }
float         ::= [ "-" ] digit { digit } [ "." digit { digit } ]
INDENT        ::= 2 × SP
```

규칙 요약:
1. 파일당 `@anchor` entry 정확히 1개.
2. carving 좌표 6 field 는 modality 와 무관 — `@payload` 0개여도 정의.
3. `@payload` 는 0개 이상, modality 는 open enum.
4. binary payload 는 `ref` (sha256+bytes), media 미생성은 `pending`, 글자는 inline.
5. 미측정 수치(`vacuum_psi`/`basin_radius`)는 design placeholder 주석 의무 (g3).

---

## 7. cross-link

- [`DESIGN.md`](DESIGN.md) §7/§8/§8.1 — CONSCIOUSNESS-CARVING paradigm + `.kosmos` 결정 SSOT
- [`PLAN.md`](PLAN.md) — Phase UBM-E (E1 design / E2 format / E3 sympy / E4 impl / E5 fire)
- [`UNIVERSE-BRAIN-MAP.tape`](UNIVERSE-BRAIN-MAP.tape) — `@D consciousness_carving_paradigm` SSOT
- [`anchors/`](anchors/) — 첫 5개 `.kosmos` anchor file (Knuth Tier 대표)
- `~/core/tape/spec/tape.md` — tape v1.2 base grammar (`.kosmos` 는 이것의 superset)
- B-CARVE-* sympy 사전등록 = Phase UBM-E3 (별도 commit), `.kosmos` parser impl = Phase UBM-E4

---

## 8. 버전 이력 (append-only — 명세 upgrade 마다 새 버전 entry)

> 명세 변경 절차: (1) 변경 내용 구현 + parser_lib/anchors 동기 → (2) 본 §8 에 새 버전 entry append → (3) 문서 최상단 `SPEC VERSION` 헤더 갱신 → (4) semver 규칙 (major = 호환 깨짐 + migration note 필수 / minor = 하위호환 확장 / patch = 오타·명확화). append-only (g6 정신 — 과거 버전 entry 불변).

### `kosmos-format/1.0` — 2026-05-17 (Phase UBM-E2 baseline · active)
- 최초 명세. `@anchor` header + carving 좌표 6 field (`knuth_tier`/`category`/`top_emotion`/`vacuum_psi`/`cell_id`/`basin_radius`) + `@payload <modality>` 3-form (inline / `ref` sha256+bytes / `pending`) + modality open enum (text/image/audio/video/`tension` + 확장) + `closed_anchor` + cross-modal 검증 (B-CARVE-MULTIMODAL ∀m ‖E_m(payload_m)−vacuum_psi‖<basin_radius) + BNF-ish grammar.
- 2층 분리 (carving 좌표 modality-independent ⊥ 감각 payload modality-specific).
- impl 동기: `kosmos_parser_lib.hexa` (UBM-E4) parse PASS · `anchors/knuth_{000,051,077,091,100}.kosmos` 5개 4-path field 공존.
- 검증 동기: B-CARVE-* sympy 10/10 🔵 (UBM-E3, sidecar `state/verify_consciousness_carving_2026_05_17/`).
- 운영 carry: vacuum_psi/basin_radius 는 design placeholder (UBM-E5 발견 🛸0/🛸51 overlap — 실측은 UBM-E7+ scale-up fire). text payload 는 `[anima 우주뇌지도]` prefix + 도우미 token grep 0 (B-IDENTITY-5 / forbidden_chat_sft_use).

### (다음 버전 placeholder)
- 차기 명세 변경 시 `kosmos-format/1.1` (하위호환 확장) 또는 `kosmos-format/2.0` (호환 깨짐 + migration) entry append. 예상 후보: UBM-E7+ scale-up fire 의 실측 vacuum_psi 반영 시 payload/coordinate 명세 정밀화, S-module image/audio encoder wiring 후 `pending` → `ref` 전이 규칙 구체화.
