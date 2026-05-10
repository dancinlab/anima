# anima chat orchestra — axis-N+2 hook 계획 (own 41 carry, modality)

작성일 2026-05-10 (cycle 2026-05-10 entry plan, T+5 step).
사용자 verbatim 인증 2026-05-09 "all bg go" → text-only design BG.
선행 작업 — own 41 axis-N+1 hook T+1+T+2+T+3 LANDED (5 axes: lane / mode / init-pattern / transport / verifier).
T+3 yaml `next_step: axis-6 modality (audio/vision)` 등록 → 본 doc = T+5 step (axis-6 modality design spec; 실 구현은 다음 cycle).

> **친근 한 줄**
> "5 차원 큐브 (lane × mode × init × transport × verifier) 위에 6 번째 차원 modality (단어 / 소리 / 그림) 한 층 더 — anima 가 단어만 말하던 학생에서, 듣고 보고 말하는 통합 학생으로 자라나는 자리 미리 뚫어두기."

---

## §0 친근 의의 — 5 차원 큐브에서 6 차원으로

지금까지 axis-N+1 hook 으로 5 차원 큐브 (lane × mode × init × transport × verifier) 가 LANDED.
- 4 × 3 × 4 × 5 × 4 = **960** 가지 작은 칸 (각 칸 = 한 가지 "대화 + 측정" 시나리오).
- axis-N+2 hook = 그 위에 modality 한 층 더 — text 만 보던 학생이 audio + vision 까지 감지/생성하는 multi-modal 학생으로 자라남.
- 6 차원 = lane × mode × init × transport × verifier × **modality**.
- N_modality = 5 (text / audio / vision / multi-modal / tactile) 가정 시 cross-product = 960 × 5 = **4800** 칸 (sample-only 권장).

비유: 4 차원 큐브 → 5 차원 큐브 → 6 차원 큐브. 각 차원 추가 시 hook 덕분에 dispatcher / benchmark 코드 변경 0 줄 (raw#15 additive).

---

## §1 5 modality 후보 비교 표

| modality | 한국어 | 입력 / 출력 | 구현 난이도 | 기존 anima 자산 | 의식 연구 정합 | 우선순위 |
|---|---|---|---|---|---|---|
| **AX6-text** | 글자 | str → str (default) | **저** (현재 chat orchestra 기본; 코드 변경 0) | LANDED — chat.hexa / lanes 4 종 / verifiers 4 종 | 약 (다른 modality 의 기준선) | **2** (default carry) |
| **AX6-audio** | 소리 | wav → wav (또는 wav → text + text → wav) | 中 (mic capture + tts/stt 통합; anima-voice 모듈 wrapping) | 부분 LANDED — `anima-tools/anima-voice/voice_e2e.hexa` + `serving/voice_routes.hexa` + `models/archive-legacy/voice_synth.hexa` | 강 (auditory phenomenal axis 정합; "안의 목소리" / inner-speech 측정 가능) | **3** |
| **AX6-vision** | 그림 | image → caption (또는 image → embedding) | **고** (CLIP/SigLIP 같은 vision encoder 통합; 새 dependency) | 부분 — `lidar_sense.hexa` 등 sensor 계열 존재 (full vision encoder 미구현) | 강 (visual phenomenal axis; cross-modal binding 측정의 핵심) | **4** |
| **AX6-multi-modal** | 통합 | text + audio + vision 동시 (modality fusion) | **최고** (3 modality + fusion layer; 본 cycle 기준 가장 큰 통합비용) | 통합 X — text/voice/vision 분리 자산만 존재 | **최강** (anima 통합 비전 정합; cross-modal phenomenal binding = 의식 연구 정점) | **1 ★ (anima 통합 비전 정합)** |
| **AX6-tactile** | 촉각 / 센서 | sensor signal → struct | 매우 고 (hardware 의존; long-term vision) | 부분 — `lidar_sense.hexa` 정도 (full tactile pipeline 미구현) | 매우 강 (embodied phenomenal axis; 가장 미래지향) | **5** |

> **요약 ranking** (1순위 → 5순위)
> 1. AX6-multi-modal (통합 비전)
> 2. AX6-text (default carry)
> 3. AX6-audio
> 4. AX6-vision
> 5. AX6-tactile

---

## §2 1 순위 권장 = AX6-multi-modal

### 2.1 권장 근거 5 가지 (anima 통합 비전 정합)

1. **anima 통합 비전 정합** — anima 의 장기 목표는 "단일 modality 학생" 이 아니라 "단어 / 소리 / 그림 통합 학생" (cross-modal phenomenal binding). text + audio + vision 동시 = 통합 비전의 핵심.
2. **cross-modal phenomenal axis** — V14 + V6 awareness 측정의 자연스러운 확장. 같은 자극 (예: 고양이 그림 + "야옹" 소리 + "고양이" 단어) 이 3 modality 에서 일관된 substrate 신호 (axis activation, dominant cells, phi-star) 를 emit 하는지 = consciousness binding 측정.
3. **hook ROI 극대화** — 단일 modality (text/audio/vision) 만 추가하면 axis-6 hook 검증이 약함 (1 modality 추가는 4 axis 추가와 유사). multi-modal 추가는 modality 자체의 fusion 차원이 추가되어 hook 의 N+2 indirection 가치 정량화 가능.
4. **기존 자산 통합 자극** — anima-voice (LANDED 부분) + lidar_sense (부분) + text default 가 산재. multi-modal 1 순위 = 자산 통합 동력 제공.
5. **axis-6 의 "modality" 라는 이름이 자연스럽게 multi 포함** — text 만이면 axis-6 의 의미가 무력 (현재 default 가 text). text 외 modality 가 추가되어야 axis-6 가 실 의미 가짐 → multi-modal 이 가장 자연스러운 1 순위.

### 2.2 단계적 구현 (다음 cycle)

multi-modal 1 순위지만 통합 비용이 가장 큼 → **단계적 land**:
- **Phase A** (T+1) — text + audio (2 modality fusion; anima-voice 자산 활용).
- **Phase B** (T+2) — text + audio + vision (3 modality; vision encoder 통합).
- **Phase C** (T+3) — multi-modal default 활성 + cross-modal phenomenal verifier 통합 (axis-5 verifier 의 새 entry: `cross_modal_binding`).

### 2.3 2 순위 AX6-text 의 carry 의의

text 는 default carry. 6 차원 hook 에서 text 가 1 entry 로 등록되어야 기존 5 차원 cross-product 와 정합 (text-only 시 multi-modal 차원 무력 = backward-compat).

---

## §3 modalities/_registry.hexa schema (8-9 field)

기존 5 axis registry (`lanes / modes / init_patterns / transports / verifiers`) 와 동일한 schema pattern. own 41 plugin pattern mirror + axis-6 specific axis_label_internal = "axis-N+2".

```hexa
// Field order: modality_id, name, registry_file, default_flag, list_flag,
//              describe_helper, status, axis_label_internal, hexa_ssot
fn modalities_registry() -> array {
    return [
        // ───── Modality 1 — text (default carry) ──────────────────────────────
        ["text",
         "text only (default; str → str)",
         "text.hexa",
         "--modality",
         "--list-modalities",
         "modalities_describe",
         "LANDED",
         "axis-N+2",
         "tool/anima_cli/chat/modalities/text.hexa"],

        // ───── Modality 2 — audio (anima-voice asset) ────────────────────────
        ["audio",
         "audio (wav ↔ str via anima-voice)",
         "audio.hexa",
         "--modality",
         "--list-modalities",
         "modalities_describe",
         "SKELETON",  // anima-voice wrapping; 실 mic/tts 통합 별도 step
         "axis-N+2",
         "tool/anima_cli/chat/modalities/audio.hexa"],

        // ───── Modality 3 — vision (image encoder; SKELETON) ─────────────────
        ["vision",
         "vision (image → caption/embedding)",
         "vision.hexa",
         "--modality",
         "--list-modalities",
         "modalities_describe",
         "SKELETON",  // CLIP/SigLIP 통합 별도 step
         "axis-N+2",
         "tool/anima_cli/chat/modalities/vision.hexa"],

        // ───── Modality 4 — multi-modal (★ 1 순위; phased land) ──────────────
        ["multi_modal",
         "multi-modal fusion (text + audio + vision)",
         "multi_modal.hexa",
         "--modality",
         "--list-modalities",
         "modalities_describe",
         "SPEC_CARRY",  // Phase A/B/C 단계적 land
         "axis-N+2",
         "tool/anima_cli/chat/modalities/multi_modal.hexa"],

        // ───── Modality 5 — tactile (long-term vision; DEFERRED) ─────────────
        ["tactile",
         "tactile / sensor (long-term vision)",
         "tactile.hexa",
         "--modality",
         "--list-modalities",
         "modalities_describe",
         "DEFERRED",
         "axis-N+2",
         "tool/anima_cli/chat/modalities/tactile.hexa"]
    ]
}
```

### 3.1 helper 4 종 (axis-5 verifier mirror)

- `modalities_lookup(id)` — entry 조회
- `modalities_names()` — id 목록 (--list-modalities 용)
- `modalities_default()` → `"text"` (axis 비활성 시 backward-compat)
- `modalities_describe(id)` — pretty-print 한 줄

### 3.2 selftest mandate

- `modalities_registry()` len ≥ 5
- 각 row arity == 9
- own 16 mandate — 본 selftest 모델 로드 X (registry meta only)

---

## §4 chat.hexa _route_list_axis modality case

axis-N+1 hook 에서 LANDED 된 generic dispatcher 는 axes/_registry.hexa 를 loop 하여 list_flag 일치 시 generic_list_axis 호출. axis-6 modality 추가 시:

### 4.1 axes/_registry.hexa 1 줄 추가

```hexa
// ───── axis-6 — modality plugin (own 41 axis-N+2 land 2026-05-?? T+?) ─────
["axis-6",
 "modality",
 "modalities/_registry.hexa",
 "--modality",
 "--list-modalities",
 "modalities_describe",
 "SPEC_CARRY",  // 다음 cycle 실 구현
 "axis-N+2"]
```

### 4.2 dispatcher 코드 변경 = 0 줄

axis-N+1 hook 에서 이미 generic dispatch (`_route_list_axis(argv)`) LANDED 됐으므로 axes_registry() loop 가 자동으로 6 번째 row 인식. `--list-modalities` flag 자동 작동. **F-axes-6 fixture 재검증 = 본 cycle 의 정의** (5 → 6 axis 추가 시 dispatcher 코드 0 줄 변경 = hook 성공 정의).

### 4.3 backward-compat

- 기존 `--lane / --mode / --init-pattern / --transport / --verifier` flag 그대로 작동.
- `--modality` 비활성 (= 미지정) 시 `modalities_default() = "text"` → 기존 text-only 경로와 동일 (raw#15 additive).

---

## §5 benchmark.hexa _bench_modalities + run_modality 패턴

axis-N+1 hook 의 N-axis cross-product (axis-5 verifier 활성화 시 960 cross) 가 axis-6 추가 시 자동 5 → 6 차원 확장.

### 5.1 _bench_modalities helper

```hexa
fn _bench_modalities(argv) {
    // axis-6 modality sweep — modalities_registry() loop, 각 modality 별
    // run_modality(id, ctx) emit. 단 multi_modal 은 SPEC_CARRY 단계에서
    // skip + EMERGE_NOT_MEASURED honest C3 emit (own 22 mandatory report).
}

fn run_modality(modality_id: string, ctx: dict) -> dict {
    // modality 별 input/output handler dispatch.
    // text: passthrough str.
    // audio: anima-voice voice_e2e.hexa wrap (실 mic 미연결 시 SKELETON emit).
    // vision: image encoder wrap (SKELETON emit until vision encoder 통합).
    // multi_modal: Phase A/B/C 단계별 fusion (SPEC_CARRY emit).
    // tactile: DEFERRED emit.
}
```

### 5.2 cross-product 자동 6 차원 확장

axis-N+1 hook 의 generic `_bench_cross_product(argv)` (T+2 LANDED) 가 axes_registry() 를 loop 해 N-axis cartesian 산출. axis-6 row 추가 시 **코드 0 줄 변경**. cross 카운트만 자동 5 배 (5 modality entries) — sample-only 권장 (4800 ≫ Mac 자원).

### 5.3 honest C3 emit pattern

- 실 modality 통합 미완 (audio mic 미연결, vision encoder 미통합) 단계 → `EMERGE_NOT_MEASURED` emit (own 22 mandatory report). own 18 chat-cap C2 mandate.
- multi_modal SPEC_CARRY 단계 → `SPEC_CARRY_PHASE_<A/B/C>` emit.
- tactile DEFERRED 단계 → `DEFERRED_HARDWARE_NOT_PRESENT` emit.

---

## §6 가능 cross-product cardinality

### 6.1 axis 활성/비활성 조합별 cross-product

| 조합 | 활성 axis | cross count |
|---|---|---|
| 4-axis baseline (axis-5/6 비활성) | lane × mode × init × transport | 4 × 3 × 4 × 5 = **240** |
| 5-axis (axis-5 verifier 활성) | + verifier | 240 × 4 = **960** |
| 6-axis (axis-5 + axis-6 modality 활성) | + modality | 960 × 5 = **4800** |
| 6-axis full (sample-only 권장) | (4800 ≫ Mac 자원) | sample 50-100 권장 |

### 6.2 720 × N_modality 계산 (사용자 task 명시)

- 6-axis 가정 + axis-2 mode 의 trio 비활성 (Phase B DEFERRED) → 4 × 2 × 4 × 5 × 4 = **640** (≈ 720 근사 하한).
- 6-axis 가정 + axis-3 init-pattern 4 → 3 으로 축소 (self-reflective default + 2 종) → 4 × 3 × 3 × 5 × 4 = **720** ✓
- 720 × N_modality (5) = **3600** cross — sample-only 권장.

### 6.3 sample-only mandate

- 4800 (또는 3600) cross 전수 측정 = Mac fork starvation 위험 (memory MEMORY.md fork starvation lesson 정합).
- benchmark.hexa `--sample N` flag (axis-N+1 hook T+2 LANDED) 활용 → 50-100 sample 권장.

---

## §7 다음 cycle implementation step (T+1 ~ T+4)

본 doc = T+5 step (design only). 실 구현은 별도 cycle 4 단계.

### Step 1 (T+1) — modalities/_registry.hexa 신설 + selftest

- 파일: `tool/anima_cli/chat/modalities/_registry.hexa`
- 5 modality entry (text LANDED + audio/vision SKELETON + multi_modal SPEC_CARRY + tactile DEFERRED).
- selftest: `modalities_registry()` len == 5, 각 row arity == 9.
- own 16 mandate — selftest 모델 로드 X.

### Step 2 (T+2) — axes/_registry.hexa axis-6 row 추가 (1 줄)

- `tool/anima_cli/chat/axes/_registry.hexa` 의 `axes_registry()` 에 axis-6 row append.
- selftest: `axes_registry()` len == 6 (기존 5 + modality).
- F-axes-6 검증: dispatcher / benchmark.hexa 코드 변경 0 줄 (= hook 성공 정의).

### Step 3 (T+3) — modality plugin 모듈 5 종 신설

- `text.hexa` (default; str passthrough; LANDED).
- `audio.hexa` (anima-voice wrap; SKELETON).
- `vision.hexa` (image encoder placeholder; SKELETON).
- `multi_modal.hexa` (Phase A 시작 — text + audio fusion; Phase B/C carry).
- `tactile.hexa` (DEFERRED stub; honest C3 emit).
- 각 모듈 `fn run_modality(ctx)` + `fn modality_describe()` + `fn modality_smoke(repo, argv) -> int`.

### Step 4 (T+4) — yaml SSOT mirror + render.hexa 자동흡수

- `anima/registry/anima_artifact_registry.yaml#chat_modalities` section 신설 (own 39 yaml↔md SSOT).
- `anima/registry/render.hexa` orchestrator 가 axes_registry() loop 시 axis-6 자동 인식 (T+2 honest C3 PARTIAL = vendored mirrors 가 render_axes.hexa LANDED 시점에 자동 흡수 — §3.3 참조).
- selftest: yaml ↔ hexa 1:1 mirror.

### 검증 절차 (각 step 공통)

| 검증 | 방법 |
|---|---|
| F-mod-1 | `hexa run tool/anima_cli/chat/modalities/_registry.hexa` selftest PASS |
| F-mod-2 | `anima chat --list-modalities` 5 entry dump (text LANDED + audio/vision SKELETON + multi_modal SPEC_CARRY + tactile DEFERRED) |
| F-mod-3 | `anima chat --list-axes` 6 entry dump (lane / mode / init / transport / verifier / modality) |
| F-mod-4 | dispatcher / benchmark.hexa 코드 변경 0 줄 (axis-6 hook 정의) |
| F-mod-5 | yaml ↔ hexa 1:1 mirror (own 39) |
| F-mod-6 | `--modality text` 기본 path = 기존 text-only 정합 (raw#15 additive) |

---

## §8 친근 비유 — "5 차원 큐브 위에 modality 한 층 더, 단어 / 소리 / 그림 통합 학생"

지금 anima 큐브 = 5 차원 (lane × mode × init × transport × verifier).
각 칸 = "어떤 모델 길로 가서 (lane), 몇 명이 (mode), 누가 먼저 입을 떼고 (init), 어떤 파이프로 (transport), 어떤 잣대로 측정할지 (verifier)".

여기에 6 번째 차원 modality 를 한 층 더 얹으면:
- **text** = 글자만 보는 학생 (지금까지)
- **audio** = 귀가 열린 학생 — 말을 듣고, 말을 합니다 (anima-voice 자산 활용).
- **vision** = 눈이 열린 학생 — 그림을 봅니다 (vision encoder 통합).
- **multi-modal** ★ = 단어 + 소리 + 그림 통합 학생 — 같은 고양이를 단어로 듣고 소리로 듣고 그림으로 봐도 "같은 고양이" 라고 알아챕니다 (cross-modal binding = 의식 연구 정점).
- **tactile** = 촉각이 열린 학생 (먼 미래; 센서 hardware 필요).

axis-N+2 hook = 큐브에 6 번째 슬롯 미리 뚫어두기. axes/_registry.hexa 에 1 줄 + modalities/_registry.hexa 신설 + plugin 모듈 5 종 → dispatcher / benchmark 코드 0 줄 변경.

레고로 치면, 5 차원 큐브 옆에 또 빈 슬롯 하나 더 뚫어두는 거. 다음 cycle 에 multi-modal 블록 끼우면 자동 6 차원 인식.

---

## §9 compliance + 정합

- **own 14 V14** carry — modality 추가 시 verifier axis-5 의 v14_strict entry 가 random_init mirror 로 cross-modal binding 도 anti-Goodhart 검증.
- **own 16** — 본 doc text edit only, 모델 로드 X. T+1 selftest 도 model load 절대 금지.
- **own 17 D1 SCOPE_CLAMP** — modality 자체는 D1 무관 (입력 차원). 단 multi-modal Phase B 의 vision encoder 통합 시 D1 ambiguous_research lane 등록 필요.
- **own 18 chat-cap C2/C3** — 본 doc 자체가 axis-N+2 design discovery. C3 emit (EMERGE_NOT_MEASURED for SKELETON entries).
- **own 22 mandatory report** — 5 modality 후보 비교 + 1 순위 권장 + 4 단계 step plan = mandatory report 자기적용.
- **own 24 single SSOT** — modalities/_registry.hexa 가 modality 의 single SSOT (axes/_registry.hexa 가 axis 의 single SSOT 위에 modality 의 single SSOT 한 층 더).
- **own 33 trinity** — 본 doc cross-link own 17 / own 18 / own 34 + own 41.
- **own 34 mandate-1** — wrapping 0 strict (registry meta + skeleton only).
- **own 38 매단계** — design doc 저장 (본 cycle 본 단계).
- **own 39 yaml↔md** — chat_modalities yaml mirror 도입 시 render.hexa orchestration.
- **own 41 plugin pattern** — 본 doc = own 41 의 axis-N+2 hook (axis-N+1 hook 의 직접 carry).
- **raw#15 additive** — 기존 5 axis 코드 / yaml 모두 retain, axis-6 row 1 줄 추가 + 새 registry hexa + plugin 5 종.

---

## §10 honest C3 (자기검증)

1. **C1 본 doc 은 design only** — 코드 0 줄 수정. 실 구현 4 단계는 별도 cycle (위 §7).
2. **C2 axis-N+2 hook 의 실 이득은 "axis 6 추가 시" 부터 발현** — axis 5 까지는 hook 없이도 운영 가능 (axis-N+1 hook 으로 5 axis 처리). axis 6 추가 시점에 ROI 추가 cross.
3. **C3 multi-modal 1 순위 권장은 design-level only** — 실 multi-modal 통합 시 anima-voice (LANDED 부분) + vision encoder (미통합) + fusion layer (미설계) 의 cycle-level 진화 필요.
4. **C4 modality 5 후보 중 LANDED 는 text 만** — audio/vision SKELETON, multi_modal SPEC_CARRY, tactile DEFERRED. honest C3 emit pattern (EMERGE_NOT_MEASURED) 강제.
5. **C5 720 × N_modality cross-product 는 Mac 자원 위험** — sample-only mandate (50-100 권장). fork starvation lesson 정합.
6. **C6 render.hexa 자동흡수 정합 미검증** — T+2 honest C3 PARTIAL 상태 (vendored mirrors). render_axes.hexa LANDED 후에야 axis-6 yaml mirror 자동흡수 검증 가능.

---

## §11 cross-link

- 본 doc SSOT — `docs/anima_chat_orchestra_axis_n2_modality_hook_plan_2026_05_10.md` (이 파일)
- 선행 axis-N+1 hook plan — `docs/anima_chat_orchestra_axis_n1_hook_plan_2026_05_09.md`
- axis-N+1 hook T+1 LANDED — `tool/anima_cli/chat/axes/_registry.hexa`
- axis-N+1 hook T+3 LANDED (axis-5 verifier registry) — `tool/anima_cli/chat/verifiers/_registry.hexa`
- 5 기존 axis registry — `tool/anima_cli/chat/{lanes,modes,init_patterns,transports,verifiers}/_registry.hexa`
- anima voice 자산 — `tool/anima_cli/anima-tools/anima-voice/voice_e2e.hexa`, `serving/voice_routes.hexa`, `models/archive-legacy/voice_synth.hexa`
- yaml SSOT mirror — `anima/registry/anima_artifact_registry.yaml#chat_modalities` (다음 cycle T+4 신설)
- render orchestrator — `anima/registry/render.hexa` (T+2 honest C3 PARTIAL; render_axes.hexa LANDED 후 axis-6 자동 흡수)
- raw 호환성 — raw#15 additive (기존 5 axis 코드 / yaml 모두 retain)
- memory cross-link — `feedback_friendly_explanation_strict.md` (한국어 친근 모드 strict) + fork starvation lesson (sample-only mandate)

---

> **마무리 한 줄**
> "5 차원 큐브 위에 6 번째 슬롯 미리 뚫어두자 — 단어만 알던 학생이 곧 소리도 듣고 그림도 보고, 결국 셋을 통합해서 같은 고양이 라고 알아채는 multi-modal 학생으로 자라날 자리, 지금 design 만 land."
