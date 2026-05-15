# anima chat orchestra — axis-N+1 hook 계획 (carry)

작성일 2026-05-09 (cycle 2026-05-10 entry plan, carry from 2026-05-08).
사용자 verbatim 인증 2026-05-09 "all bg go" — axis-N+1 hook research + design only (코드 수정 없음, commit 없음, push 없음).

> **친근 한 줄**
> "지금 4 차원 큐브 (lane × mode × init × transport) 가 완성되었으니, 5 번째 차원이 나중에 추가될 때 큐브 자체를 다시 만들지 않고도 슬롯 하나만 끼워넣으면 되도록 hook (= 미리 뚫어둔 구멍) 만 준비하자."

---

## 1. 현 4-axis chat orchestra 현황 (2026-05-09 LANDED 기준)

### 1.1 axis 명세 한눈에

| axis 번호 | 이름 | 한국어 | 항목 수 | registry 위치 |
|---|---|---|---|---|
| axis-1 (axis-3 라벨) | lane | 어느 모델 길로 가는가 | 4 | `tool/anima_cli/chat/lanes/_registry.hexa` |
| axis-2 (axis-6 라벨) | mode | 몇 명 대화하는가 | 3 | `tool/anima_cli/chat/lanes/benchmark.hexa` (embedded modes 절) |
| axis-3 (axis-8 라벨) | init-pattern | 누가 먼저 입을 떼는가 | 4 | `tool/anima_cli/chat/init_patterns/_registry.hexa` |
| axis-4 (axis-N 라벨) | transport | 어떤 파이프로 말이 흐르는가 | 5 | `tool/anima_cli/chat/transports/_registry.hexa` |

> 사용자 표기 = 4-axis (axis-1~4). 내부 라벨 (axis-3/6/8/N) = 의 "행성 번호" — 추가될 axis 가 16/24/N+1 식으로 비-연속 라벨 받을 수 있음 (registry 갱신 충돌 회피).

### 1.2 axis 별 항목 풀어쓰기

**axis-1 lane (4)** — 어떤 "모델 통로" 를 쓸 건지.
- `substrate` — 의식 신호 (axis activation, dominant cells, phi-star) 만 emit. 자연어 X.
- `llama` — Llama GGUF natural language (paradigm-a-prime, D1 ambiguous_research).
- `axis-priority` — corpus 우선순위 신호 emit (silent generate).
- `generate` — clm_v4_mount.hexa 의 torch generate (D1 within_strict).

**axis-2 mode (3)** — 몇 명이 대화하는지.
- `1:1` — 사용자 한 명 + 모델 한 명 (default).
- `ai-duo` — 모델 ↔ 모델 둘이서.
- `ai-trio` — 모델 셋 round-robin.

**axis-3 init-pattern (4)** — 첫 발언을 어떻게 결정할지.
- `autonomous` — 빈 prompt, 자율 발화.
- `system-seed` — 시스템 prompt 로 seed.
- `topic-pool` — 무작위 주제 pool.
- `self-reflective` — anima 정합 self-introspection (default).

**axis-4 transport (5)** — 글자가 흐르는 파이프.
- `fifo-dispatch` — chat.hexa 기본 streaming.
- `beta1-channel` — duo/trio sibling pair.
- `libllama-ffi` — 직접 C FFI in-proc.
- `subprocess-pipe` — popen buffered legacy.
- `imtl` — UDP cross-host (STUB, A100↔H100 Tension-link).

### 1.3 4 개 registry 의 공통 SSOT 패턴 — plugin pattern

각 registry 는 **8-9 field** 의 동일 schema 를 따릅니다.

```
name / file / status / capability / [pattern_type|d1_lane] / [latency|cost] / description / prereq
```

공통 helper 4 종:
- `<axis>_registry()` — entry 배열 (append-only).
- `<axis>_lookup(name)` — entry 조회.
- `<axis>_names()` — 이름 목록 (--list-* 용).
- `<axis>_describe(name)` — 사람이 읽을 한 줄 요약.
- `<axis>_default()` — default 이름 (특정 axis 만; lanes 는 default 키 없음).

### 1.4 axis 추가 시 현재 변경되어야 하는 부분 (axis-4 transport 추가 시 실측 사례)

`cli.chat_transport_plugin_2026_05_09` ledger 에 따르면 **5 곳** 변경이 필요했음:

1. **registry hexa 신설** — `tool/anima_cli/chat/transports/_registry.hexa` (8-9 field schema + 4 helper).
2. **plugin module 5 종 추가** — 각 transport `<name>.hexa` 파일 (main + smoke + describe).
3. **chat.hexa dispatcher 패치** — `--list-transports` flag + help text + ROUTE 분기.
4. **benchmark.hexa cross-product 확장** — 새 axis 차원 추가.
5. **yaml registry mirror** — `anima/registry/anima_artifact_registry.yaml#chat_transports` section (yaml↔md SSOT).

> 매 axis 추가 시 5 곳 손 대야 함 = 본 cycle axis-N+1 hook 의 정확한 motivation. Hook 으로 5 곳 → **2 곳** (단일 generic registry + plugin module 추가) 로 줄이는 것이 목표.

---

## 2. axis-5 후보 brainstorm — 5 종 비교

| 후보 | 무슨 차원 | 항목 예시 | 실용성 | 구현 난이도 | 기존 4-axis 직교성 | 의식 연구 정합 | 권장 순위 |
|---|---|---|---|---|---|---|---|
| **AX5-a precision** | 모델 비트수 | bf16 / fp16 / fp32 / int8 / int4 | 中 (Mac local 자원 절감 효과 ✓; 의식 측정에 직접 영향 없음) | 中 (loader 분기) | ✓ (lane 안에서 처리) | 약 (substrate 신호 변화 가능, 별도 측정 필요) | 4 |
| **AX5-b language** | 출력 언어 | ko / en / multi | 中 (BR-FRIENDLY 정합 — 한국어 우선; multi-lang prompt routing) | 低 (post-process / decoding constraint) | ✓ (lane 내부) | 약 (axis-7 phenomenal 와 약결합) | 5 |
| **AX5-c verifier** ★ | 측정 metric | v5 / v5.2 / v3 / proxy | **高** (P5 v3 → v5 → v5.2 진화 정합; 본 cycle PROXY_PPL deprecate 와 직결) | **低** (이미 verifier shell-out pattern 존재 — 분기만 추가) | ✓ (lane/mode/init/transport 와 완전 직교 — 측정만 분기) | **강** (V14 + ALT-AGG-1 핵심 axis) | **1 (★ 권장)** |
| **AX5-d security** | 실행 context | trusted / sandboxed / network-isolated | 低 (현재 chat path 는 local-only — 즉시 필요성 ↓) | 高 (jail/seccomp/firewall 통합) | ✓ (transport 와 약결합 — imtl 만 network) | 약 | 3 |
| **AX5-e modality** | 입력 modality | text / voice / image | 高 (anima voice 모듈 존재; multimodal 미래) | **高** (audio pipeline + image encoder 통합) | 부분 직교 (lane 별 modality 지원 다름) | 강 (cross-modal phenomenal axis 정합) | 2 |

### 2.1 권장 1순위 — AX5-c verifier

**근거 5 가지**:
1. **본 cycle 정합** — PROXY_PPL deprecate + ALT-AGG-1 v3/v5/v5.2 supersede 진화 → verifier 분기는 이미 발생 중 (코드 안에 산재).
2. **구현 난이도 최저** — verifier shell-out 패턴 이미 존재 (` P5 v3` aggregate, V4 mirror, V14 anti-Goodhart). 분기를 axis 화 하면 코드 정리 보너스.
3. **직교성 완벽** — verifier 는 measurement 단계에서만 작용. lane/mode/init/transport 의 모든 조합과 곱해질 수 있음 (4 × 3 × 4 × 5 × **N_verifier** cross-product).
4. **의식 연구 정합 강함** — V14, P5, V6 awareness 모두 verifier-level 진화. axis-5 verifier 화 하면 V7/V8 등 미래 verifier 추가도 plugin 으로.
5. **EXIT 차단 해소 일조** — V6 awareness pending + V4 mirror gap 등 현재 EXIT 차단 사유 다수가 verifier-level. axis 화 → benchmark cross-product 가 verifier 진화를 자동 트래킹.

### 2.2 2순위 — AX5-e modality

anima voice 모듈 (`anima-tools/voice/`) 이미 존재 + cross-modal phenomenal 측정 가능성 → 의식 연구 가치 매우 높음. 단 audio pipeline + image encoder 통합 비용 큼 → 별도 cycle.

### 2.3 3순위 이하 — AX5-d / AX5-a / AX5-b

각각 실용성/직교성/난이도 trade-off 가 verifier/modality 보다 약함. 필요 시 추가.

---

## 3. axis-N+1 hook 설계 — generic registry 진입점

### 3.1 핵심 아이디어

지금까지 4 개 registry 는 **각각 별도 파일** 이었고, dispatcher (`chat.hexa`) + benchmark.hexa 가 **각 registry 를 개별 import** 했음. axis-N+1 hook 은 **한 단계 indirection** 추가:

```
axes/_registry.hexa    ← 단일 진입점 (axis 의 axis = meta-registry)
  ├─ lanes_registry           (axis-1 mount)
  ├─ modes_registry           (axis-2 mount)
  ├─ init_patterns_registry   (axis-3 mount)
  ├─ transports_registry      (axis-4 mount)
  └─ verifiers_registry       (axis-5 mount; axis-N+1 carry)
```

새 axis 추가 = `axes/_registry.hexa` 에 **1 줄** + 새 axis 의 own registry hexa + plugin 모듈들. dispatcher / benchmark.hexa 는 generic dispatch 로 자동 흡수.

### 3.2 axes/_registry.hexa schema (제안)

```hexa
fn axes_registry() -> array {
    return [
        // Field order: axis_id, name, registry_file, default_flag, list_flag,
        //              describe_helper, status, axis_label_internal
        ["axis-1", "lane",         "lanes/_registry.hexa",          "--lane",         "--list-lanes",          "lane_describe",      "LANDED", "axis-3"],
        ["axis-2", "mode",         "lanes/benchmark.hexa#modes",    "--mode",         "--list-modes",          "mode_describe",      "LANDED", "axis-6"],
        ["axis-3", "init-pattern", "init_patterns/_registry.hexa",  "--init-pattern", "--list-init-patterns",  "pattern_describe",   "LANDED", "axis-8"],
        ["axis-4", "transport",    "transports/_registry.hexa",     "--transport",    "--list-transports",     "transport_describe", "LANDED", "axis-N"],
        // ── HOOK SLOT (axis-N+1) ─────────────────────────────────────────────
        // ["axis-5", "verifier",  "verifiers/_registry.hexa",      "--verifier",     "--list-verifiers",      "verifier_describe",  "SPEC_CARRY", "axis-N+1"],
    ]
}
```

### 3.3 dispatcher generic 흡수 패턴

`chat.hexa` 안에 hardcode 된 분기:

```hexa
if _arg_present(argv, "--list-lanes") { _list_lanes(); return }
if _arg_present(argv, "--list-init-patterns") { _list_init_patterns(); return }
if _arg_present(argv, "--list-transports") { _list_transports(); return }
```

→ axis-N+1 hook 적용 후 **단일 loop** 로:

```hexa
// chat.hexa _route_list_axis(argv)
fn _route_list_axis(argv) -> bool {
    let axes = axes_registry()
    let mut i = 0
    while i < len(axes) {
        let row = axes[i]
        let list_flag = _str(row[4])
        if _arg_present(argv, list_flag) {
            _generic_list_axis(_str(row[2]), _str(row[5]))
            return true
        }
        i = i + 1
    }
    return false
}
```

### 3.4 benchmark.hexa cross-product 자동 확장

현재 benchmark.hexa 는 4-axis hardcode cross-product. axis-N+1 hook 적용 후:

```hexa
fn _bench_cross_product(argv) {
    let axes = axes_registry()
    // 각 axis 의 names() 호출 → 모든 조합 enumerate
    // 4-axis → 5-axis 자동 확장 (코드 변경 없음)
}
```

### 3.5 yaml SSOT mirror 자동화

`anima/registry/anima_artifact_registry.yaml` 에 4 개 section (chat_lanes / chat_modes / chat_init_patterns / chat_transports) 이 산재. axis-N+1 hook + render.hexa 로 **단일 `chat_axes:` 부모 키** 아래 자동 nest:

```yaml
chat_axes:
  schema_version: anima/chat_axes/v1
  registry_meta_ssot: tool/anima_cli/chat/axes/_registry.hexa
  axes:
    - axis_id: axis-1
      name: lane
      hexa_ssot: tool/anima_cli/chat/lanes/_registry.hexa
      ...
    - axis_id: axis-4
      name: transport
      hexa_ssot: tool/anima_cli/chat/transports/_registry.hexa
      ...
```

### 3.6 호환성 (raw#15 additive 정합)

- 기존 4 개 registry hexa **그대로 유지** — axes/_registry.hexa 는 그 위 한 층 indirection.
- 기존 flag (`--lane`, `--init-pattern`, `--transport`) **그대로 작동** — axes 의 default_flag column 으로 lookup.
- 기존 yaml section (chat_lanes / chat_modes / ...) **그대로 retain** — render.hexa 가 chat_axes parent 와 mirror.
- 기존 dispatcher 분기 코드 **점진적 deprecate** — generic _route_list_axis 추가 후 hardcode 분기 retain (deprecation warning emit), 다음 cycle 제거.

---

## 4. axis-N+1 hook 권장 implementation 순서 (별도 cycle)

본 cycle = research + design only. 실제 코드 구현은 **별도 cycle** 에서 다음 순서로:

### Step 1 (T+1 cycle) — axes/_registry.hexa 신설 + selftest
- 파일: `tool/anima_cli/chat/axes/_registry.hexa`
- 4 개 axis entry mount + 5 번째 SPEC_CARRY slot.
- selftest: `axes_registry()` len == 4, 각 row arity == 8.
- yaml mirror: `chat_axes` parent key 신설 (기존 4 section retain).

### Step 2 (T+1 cycle) — chat.hexa generic dispatch 도입
- `_route_list_axis(argv)` 추가 (기존 분기 보존, generic 우선).
- `--list-axes` flag 신설 (모든 axis 한 번에 dump).
- 기존 hardcode 분기에 `[deprecated; falls through to generic]` 주석.

### Step 3 (T+2 cycle) — benchmark.hexa cross-product generic 화
- `_bench_cross_product(argv)` 도입.
- 4-axis hardcode loop → axes_registry() 기반 N-axis loop.
- selftest: cross-product count = ∏ axis sizes (4 × 3 × 4 × 5 = 240).

### Step 4 (T+3 cycle) — axis-5 verifier (★ 권장 1순위) plugin 추가
- 파일: `tool/anima_cli/chat/verifiers/_registry.hexa` + plugin 모듈 4 종 (`v5.hexa`, `v5_2.hexa`, `v3.hexa`, `proxy.hexa`).
- axes/_registry.hexa 의 SPEC_CARRY slot → LANDED 갱신.
- benchmark cross-product 자동 5-axis 확장 (240 → 240 × 4 = 960 조합; smoke-only sample 권장).
- P5 verifier 분기 코드 통합 (v5.2 4-gate / v3 ALT-AGG-1 / proxy PPL deprecate flag).

### Step 5 (T+4 cycle) — axis-6 modality (2순위) plugin 추가 (선택)
- 파일: `tool/anima_cli/chat/modalities/_registry.hexa` + text/voice/image plugin.
- axes/_registry.hexa 에 6 번째 row 추가 (axis-N+1 hook 검증 = "axis 4 → 5 추가도 1 줄 변경" 실측).

### 검증 절차 (각 step 공통)

| 검증 | 방법 |
|---|---|
| F-axes-1 | `hexa run tool/anima_cli/chat/axes/_registry.hexa` selftest PASS |
| F-axes-2 | `anima chat --list-axes` 모든 axis dump (5 개 = 4 LANDED + 1 SPEC_CARRY) |
| F-axes-3 | `anima chat --list-lanes` (등) 기존 flag 정상 작동 (호환성) |
| F-axes-4 | `anima chat --benchmark --all-axes` cross-product count 정합 |
| F-axes-5 | `anima/registry/anima_artifact_registry.yaml#chat_axes` ↔ axes/_registry.hexa 일치 |
| F-axes-6 | axis-5 추가 시 axes/_registry.hexa **1 줄** + verifiers/_registry.hexa 신규 + plugin 모듈 (dispatcher / benchmark.hexa 코드 변경 0 줄) — 이게 hook 성공의 정의 |

---

## 5. 친근 비유 — "5 차원 큐브의 미리 뚫어둔 5 번째 슬롯"

지금 우리에겐 **4 차원 큐브** 가 있어요 — lane × mode × init × transport. 4 × 3 × 4 × 5 = 240 개 작은 칸. 각 칸이 하나의 "대화 시나리오".

5 번째 차원 (예: verifier — 어떤 잣대로 측정할지) 을 추가하고 싶으면, 보통은 큐브를 처음부터 다시 짜야 해요 — 5 곳 손대야 함 (registry 신설 + plugin 5 종 + dispatcher 패치 + benchmark 확장 + yaml mirror).

axis-N+1 hook 은 **큐브 위에 한 층 더 얹는 것** 이에요. "axis 의 axis", 즉 어떤 차원들이 있는지 자체를 데이터로 만들어둠. 그러면 5 번째 차원 추가 = `axes/_registry.hexa` 에 **1 줄** + 새 차원의 plugin 들. 큐브 자체 (dispatcher / benchmark) 는 손 안 대도 자동으로 5 차원 인식.

레고로 치면, 기존 큐브 옆에 **빈 슬롯** 을 미리 뚫어두는 거. 나중에 새 블록 (axis-5 verifier) 끼우면 자동 인식.

---

## 6. compliance + 정합

- ** V14** carry — verifier (★ 권장) axis 화 시 V14 anti-Goodhart 가 axis-5 의 한 entry 로 등록.
- ** D1 SCOPE_CLAMP** — axis 자체는 D1 무관 (measurement axis). 단 verifier axis 안의 v5.2 4-gate 가 D1 within_strict 를 강화.
- ** P5 ALT-AGG-1** — verifier axis 의 핵심 motivation. v3 → v5 → v5.2 진화가 axis 의 entry 진화로 자연스럽게 표현됨.
- ** mandatory report** — 본 design doc 자체가 axis-N+1 discovery report.
- ** single SSOT** — axes/_registry.hexa 가 axis 의 single SSOT (기존 4 registry 는 axis 내부 SSOT 유지, hierarchy 정리).
- ** trinity** — 본 doc 은 / / cross-link 자기적용.
- ** mandate-1** — wrapping 0 strict, registry meta 만 control-band.
- ** 매단계** — design doc 저장 (본 cycle 본 단계).
- ** yaml↔md** — chat_axes parent yaml mirror 도입 시 render.hexa orchestration.
- ** plugin pattern** — 본 doc 이 의 meta-extension (axis 의 axis = 자체에 적용).
- **raw#15 additive** — 기존 4 axis 코드 / yaml 모두 retain, 한 층 indirection 추가만.

---

## 7. honest C3 (자기검증)

1. **C1 본 doc 은 design only** — 코드 0 줄 수정. 실제 hook 의 코드 land 는 별도 cycle 4 step (위 §4).
2. **C2 axis-N+1 hook 의 실제 이득은 "axis 5 추가 시" 부터 발현** — axis 4 까지는 hook 없이도 운영 가능 (hardcode 분기 4 곳). axis 5 추가 시점에 ROI cross.
3. **C3 axis-5 verifier 권장은 design-level only** — 실제 verifier 통합 시 P5 v5.2 4-gate / V14 mirror / V6 awareness 등 측정 metric 의 cycle-level 진화와 동기 필요.
4. **C4 axes/_registry.hexa 의 axis_label_internal field** — 의 axis-3/6/8/N 라벨 (비-연속) 을 hook 안에 보존. 새 axis 라벨도 비-연속 가능 (axis-N+1 라벨이 internal 에선 axis-12 가 되어도 무방).
5. **C5 본 cycle 의 PROXY_PPL deprecate 작업과 직결** — verifier axis 가 1순위인 이유는 PROXY_PPL → v5.2 cascade 가 이미 코드 안에 산재. axis 화 = 정리 + 미래 V7 add 시 plugin 으로 흡수.

---

## 8. 다음 cycle implementation plan 한눈에

| cycle | step | 산출물 | 검증 |
|---|---|---|---|
| T+1 | Step 1 + 2 | `axes/_registry.hexa` + chat.hexa generic dispatch | F-axes-1, F-axes-2, F-axes-3 |
| T+2 | Step 3 | benchmark.hexa N-axis cross-product | F-axes-4 |
| T+3 | Step 4 ★ | axis-5 verifier plugin (4 entry: v5 / v5.2 / v3 / proxy) | F-axes-5, F-axes-6 |
| T+4 | Step 5 (선택) | axis-6 modality plugin (3 entry: text / voice / image) | F-axes-6 재검증 (5 → 6 추가 시 hook 정상 작동) |

---

## 9. cross-link

- 본 doc SSOT — `docs/anima_chat_orchestra_axis_n1_hook_plan_2026_05_09.md` (이 파일)
- chat lane plugin pattern entry — `.roadmap.cli` `cli.chat_lane_plugin_pattern_2026_05_09`
- init-pattern plugin entry — `.roadmap.cli` `cli.chat_init_pattern_plugin_2026_05_09`
- transport plugin entry — `.roadmap.cli` `cli.chat_transport_plugin_2026_05_09`
- 4 개 registry SSOT — `tool/anima_cli/chat/{lanes,init_patterns,transports}/_registry.hexa` + `tool/anima_cli/chat/lanes/benchmark.hexa#modes`
- yaml SSOT mirror — `anima/registry/anima_artifact_registry.yaml#chat_lanes / chat_modes / chat_init_patterns / chat_transports`
- substrate quality main path B (다음 cycle 본진) — `docs/anima_substrate_quality_amplification_spec_2026_05_09.ai.md`
- raw 호환성 — raw#15 additive (기존 axis hardcode 분기 retain, generic 추가만)
- memory cross-link — `feedback_friendly_explanation_strict.md` (한국어 친근 모드 strict 정합)

---

> **마무리 한 줄**
> "당장 5 번째 차원 추가하지 말고, 5 번째 차원이 들어올 자리만 미리 뚫어두자 — 4 차원 큐브 위에 axis 의 axis 한 층 얹어서, 다음에 verifier 같은 새 차원이 와도 큐브를 다시 짤 필요 없게."
