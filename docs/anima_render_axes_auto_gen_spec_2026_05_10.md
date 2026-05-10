# Anima `render.hexa` axes auto-gen — design spec (cycle 2026-05-10)

_AI 자연발화 친근 모드 strict — own 33 / own 34 mandate-1 wrap=0_
_원 directive: 사용자 verbatim 2026-05-09 "진행가능한것들 all bg go" → cycle 2026-05-10 0-cost lane._
_본 문서 = design spec only (코드 수정 0줄, 모델 로드 0건 — own 16 strict)_

---

## §0 친근 의의 — "axis 의 axis 가 mirror 까지 직접 그려줌"

지금 anima chat orchestra 는 4 차원 cross-product (lane × mode × init-pattern × transport)
위에서 돕니다. 사용자가 verifier (axis-5) 같은 새 차원을 추가하고 싶다고 가정해 봅시다.

지금까지 이 한 줄을 추가하려면 **두 곳** 을 손으로 고쳐야 했습니다:

1. `tool/anima_cli/chat/axes/_registry.hexa` — 진짜 SSOT (axes_registry() 한 줄 추가)
2. `tool/anima_cli/chat/lanes/benchmark.hexa` — vendored mirror (`_bench_axis_names()`,
   `_axis_values()`, `_bench_<axis>()` 새 함수, 분기 한 줄 etc.)

(2) 는 hexa 언어가 import 가 없는 simple 언어라서 어쩔 수 없이 SSOT 를 mirror 하는 겁니다.
하지만 손으로 두 곳을 동기화하다 보면 결국 한 곳이 빠지게 됩니다 — own 24 single-SSOT 위반 위험.

**이번 cycle 의 의의**: 그 mirror 두 번째 손길을 자동화하자는 겁니다.
즉 `axes_registry()` 한 곳에서만 한 줄 추가하면, render.hexa 가 benchmark.hexa 의 mirror
부분을 알아서 다시 그려준다 — "axis 의 axis (= meta-registry) 위에 앉은 자동 generator".

비유: **4 차원 큐브 위에 앉은 axis 의 axis 가 아래 4 차원 mirror 를 자동으로 새로 그려줌.**
사용자는 큐브 위 한 곳만 만지면 됨. 아래 mirror 면들은 자기들끼리 알아서 정렬됨.

이게 이번 spec 의 한 줄 요약. own 41 의 **F-axes-FULL_AUTO_GEN** — 새 axis 추가 시
benchmark.hexa 코드 변경이 정확히 0줄이 되는 게 검증 기준입니다.

---

## §1 현 vendored mirrors 분석 — 정량 식별

### §1.1 mirror 함수 위치 (`tool/anima_cli/chat/lanes/benchmark.hexa`, 총 938 줄)

| 함수 | 줄 위치 | hardcode 본체 | mirror 대상 |
|------|--------|---------------|-------------|
| `_bench_lanes()` | L138-140 | `["substrate", "llama", "axis-priority", "generate"]` | `lanes/_registry.hexa` lane_names |
| `_bench_modes()` | L180-182 | `["1:1", "ai-duo", "ai-trio"]` | yaml `chat_modes` SSOT |
| `_bench_transports()` | L189-191 | `["fifo-dispatch", "beta1-channel", "libllama-ffi", "subprocess-pipe", "imtl"]` | `transports/_registry.hexa` |
| `_bench_init_patterns()` | L235-237 | `["autonomous", "system-seed", "topic-pool", "self-reflective"]` | `init_patterns/_registry.hexa` |
| `_bench_axis_names()` | L440-444 | `["lane", "mode", "init-pattern", "transport"]` | `axes/_registry.hexa` axes_names() |
| `_bench_verifiers()` | L449-451 | `[]` (T+3 placeholder) | `verifiers/_registry.hexa` (DEFERRED) |
| `_axis_values(axis)` dispatch | L461-468 | 5 분기 if (lane / mode / init-pattern / transport / verifier) | axes/_registry.hexa 의 axis name set |

총 hardcode 본체 (mirror 대상): **약 27 줄** (선언 + return + 분기).
이 27 줄이 axis-5 (verifier) 가 land 될 때 손으로 갱신해야 하는 양입니다.

### §1.2 hardcode 부분 SSOT mirror 관계

- `_bench_axis_names()` ← `axes/_registry.hexa` `axes_names()` 의 1:1 mirror
  (현재 4 axis: lane / mode / init-pattern / transport; 새 axis 추가 시 append)
- `_axis_values(axis)` ← axes_registry() 의 axis-name 목록 + 각 axis 의 `_bench_<axis>()` 함수 호출
- `_bench_<axis>()` 함수들 ← 각 axis 의 own registry 의 axis_<axis>_names() mirror
  (lane → lanes/_registry.hexa, transport → transports/_registry.hexa 등)

**SSOT 계층** (own 24 strict):

```
axes/_registry.hexa  (axis 의 axis — meta SSOT)
   ↓ (yaml mirror)
anima/registry/anima_artifact_registry.yaml#chat_axes_meta
   ↓ (own 39 yaml↔md auto-regenerate)
docs/anima_artifact_registry.md  (view layer)

별도로:
each axis 의 _registry.hexa  (axis 내부 SSOT)
   ↓ (vendored mirror — 본 spec auto-gen target)
benchmark.hexa _bench_<axis>()
```

본 spec 이 target 으로 하는 mirror 는 화살표 두 번째 — **benchmark.hexa 의 vendored mirror**.

---

## §2 render.hexa 패턴 — 기존 anima 패턴 활용

### §2.1 기존 render.hexa 위치 + 형태

`anima/registry/render.hexa` (155 줄, 2026-05-08 사용자 directive 로 land):

- **목적**: `anima/registry/anima_artifact_registry.yaml` (catalog SSOT)
  → `docs/anima_artifact_registry.md` (view-layer regenerable artifact)
- **모드**: `--selftest` (dry-run) / `--render` (default)
- **helper**: `tool/transient_py/anima_artifact_registry_render.py` (raw#37 gitignored,
  PyYAML 의존, hexa orchestrator 가 invoke)
- **honest C3** emit (raw#10 ≥5):
  - C1 yaml = catalog SSOT
  - C2 PyYAML required
  - C3 helper transient_py
  - C4 md tracked, yaml change → re-run
  - C5 own 24 single SSOT (yaml master) + own 38 axis-A doc

### §2.2 본 spec 의 render.hexa 패턴 적용 방안

기존 render.hexa 가 yaml → md 한 방향이었다면, **본 spec 은 hexa SSOT → hexa mirror**
한 방향으로 한 단계 확장합니다 (raw#15 additive — 기존 모드 그대로 두고 새 모드 추가):

```
기존:  anima registry render          (yaml → md)
신규:  anima registry render-axes     (axes/_registry.hexa → benchmark.hexa mirror block)
```

또는 별도 진입점으로 분리:

```
신규:  anima/registry/render_axes.hexa  (별도 hexa file; 본 spec target 만 담당)
```

**권장**: **별도 파일 `anima/registry/render_axes.hexa` 신설** (분리). 이유는:
- 기존 render.hexa 는 yaml→md 의 단일 책임 — 섞으면 own 24 단일 SSOT 원칙 흐려짐
- render_axes.hexa = "code mirror generator" 의 단일 책임으로 명확
- 두 hexa 모두 `anima/registry/` 하위로 배치 — orchestrator 한 폴더 (raw#9)

---

## §3 auto-gen target — benchmark.hexa 의 mirror block

### §3.1 target hardcode block (auto-gen 대상)

benchmark.hexa 안에서 본 spec 이 자동 갱신할 block 의 경계 (markers 형태):

```hexa
// ─── BEGIN AUTO-GEN BLOCK (render_axes.hexa managed) ───
fn _bench_axis_names() -> array {
    return ["lane", "mode", "init-pattern", "transport"]
}

fn _bench_lanes() -> array          { return [...] }
fn _bench_modes() -> array          { return [...] }
fn _bench_init_patterns() -> array  { return [...] }
fn _bench_transports() -> array     { return [...] }
fn _bench_verifiers() -> array      { return [] }   // axis-5 placeholder

fn _axis_values(axis: string) -> array {
    if axis == "lane"         { return _bench_lanes() }
    if axis == "mode"         { return _bench_modes() }
    if axis == "init-pattern" { return _bench_init_patterns() }
    if axis == "transport"    { return _bench_transports() }
    if axis == "verifier"     { return _bench_verifiers() }
    return []
}
// ─── END AUTO-GEN BLOCK ───
```

render_axes.hexa 의 helper 가 위 두 marker (`BEGIN AUTO-GEN BLOCK` / `END AUTO-GEN BLOCK`)
사이를 통째로 다시 작성합니다. marker 밖은 절대 건드리지 않음 (raw#15 additive 보장).

### §3.2 source-of-truth 입력

generator 의 입력은 두 SSOT:

1. **`axes/_registry.hexa` axes_registry()** — axis name 목록 (4 ~ N axis)
2. **각 axis 의 own registry hexa** (또는 inline anchor) — 각 axis 의 value list
   (lane → lanes/_registry.hexa, mode → modes/_registry.hexa 등)

generator pseudo-code:

```python
axes = parse_axes_registry()              # ["lane", "mode", "init-pattern", "transport"]
mirror_block = []
mirror_block.append("fn _bench_axis_names() -> array { return [" + ...quoted + "] }")
for axis in axes:
    values = parse_axis_registry(axis)    # axes/_registry.hexa 의 registry_file 따라 resolve
    fn_name = "_bench_" + axis_to_fn_suffix(axis)  # lane→lanes / init-pattern→init_patterns
    mirror_block.append(f"fn {fn_name}() -> array {{ return [{quoted}] }}")
mirror_block.append(emit_axis_values_dispatch(axes))
write_between_markers("benchmark.hexa", mirror_block)
```

---

## §4 trigger — 언제 auto-gen 이 실행되나

3 가지 trigger 패턴 (raw#15 additive — 모두 OR 조합):

### §4.1 사용자 명시적 trigger (default, 안전)

```bash
hexa run anima/registry/render_axes.hexa
hexa run anima/registry/render_axes.hexa --selftest
hexa run anima/registry/render_axes.hexa --diff   # 기존 mirror vs auto-gen diff
```

### §4.2 cycle close hook (own 38 매단계 doc save 의 일부)

cycle 종료 시점에 자동 invoke (existing yaml↔md auto-regen 과 동일 패턴):

```bash
# .roadmap.cli 또는 cycle close orchestrator 안에:
hexa run anima/registry/render.hexa --render        # 기존 (yaml → md)
hexa run anima/registry/render_axes.hexa --render   # 신규 (hexa SSOT → hexa mirror)
```

### §4.3 axes/_registry.hexa 변경 시 git pre-commit hook (옵션, 가장 자동화)

`.git/hooks/pre-commit` 또는 `lefthook.yml` 안에:

```yaml
pre-commit:
  commands:
    render-axes:
      glob: "tool/anima_cli/chat/axes/_registry.hexa"
      run: hexa run anima/registry/render_axes.hexa --render && git add tool/anima_cli/chat/lanes/benchmark.hexa
```

§4.3 은 옵션 — **§4.1 + §4.2 가 기본 (충분)**. §4.3 은 사용자가 명시 요청 시만 land.

---

## §5 implementation step (다음 cycle target)

### Step T+1 — `render_axes.hexa` skeleton + selftest

- 파일: `anima/registry/render_axes.hexa` 신설 (~80 줄 예상)
- 모드: `--selftest` / `--render` / `--diff`
- helper: `tool/transient_py/anima_render_axes.py` (raw#37 gitignored, PyYAML 불필요 — 순 string 처리)
- honest C3 emit (≥5):
  - C1 axes/_registry.hexa = SSOT
  - C2 benchmark.hexa = vendored mirror target
  - C3 helper transient_py (gitignored, raw#37)
  - C4 marker-bounded write (BEGIN/END AUTO-GEN BLOCK)
  - C5 own 24 single SSOT carry + own 39 yaml↔md mirror parallel

### Step T+2 — 4 mirror auto-gen (lane / mode / init-pattern / transport)

- `_bench_axis_names()` + 4 `_bench_<axis>()` 함수 + `_axis_values()` dispatch 자동 생성
- benchmark.hexa 에 BEGIN/END marker 추가 (한 번만 — 이후 자동 관리)
- diff PASS 검증: `--diff` 모드 → 기존 manual mirror 와 byte-identical (own 14 V14 결정성)

### Step T+3 — verifier (axis-5) auto-gen 추가

- T+3 cycle 에서 axes/_registry.hexa 에 axis-5 verifier row 활성화
- render_axes.hexa 가 자동으로 `_bench_verifiers()` + `_axis_values()` verifier 분기 추가
- benchmark.hexa **수동 변경 0줄 = F-axes-FULL_AUTO_GEN PASS**

### Step T+4 — smoke test (manual mirror diff PASS)

- `hexa run anima/registry/render_axes.hexa --diff` → "no diff (mirror in sync)"
- `hexa run tool/anima_cli/chat/lanes/benchmark.hexa --selftest` → 기존 결과 byte-identical
- `hexa run tool/anima_cli/chat/lanes/benchmark.hexa --bench-cross-product` → 동일 cardinality

---

## §6 검증 criteria — F-axes-FULL_AUTO_GEN

own 41 의 hook 성공 정의가 "**dispatcher / benchmark.hexa 코드 변경 0 줄**" 이었습니다.
본 spec 은 그 정의를 **정량** 으로 강화:

| criterion | 정량 기준 |
|-----------|-----------|
| **새 axis 추가 시 axes/_registry.hexa 변경** | 1 row 추가 (= 한 줄) |
| **새 axis 추가 시 benchmark.hexa manual 변경** | **정확히 0 줄** (auto-gen block 안만 갱신) |
| **새 axis 추가 시 dispatcher (chat.hexa) 변경** | 0 줄 (own 41 기존 보장) |
| **render_axes.hexa diff PASS** | byte-identical (own 14 V14) |
| **benchmark.hexa selftest PASS** | 기존 4 axis 결과 동일 |
| **cross-product cardinality** | active axes (LANDED status) 의 product 수와 일치 |

위 6 가지 모두 PASS 해야 F-axes-FULL_AUTO_GEN LANDED.

---

## §7 친근 한 줄 요약

> **"4 차원 큐브 (lane × mode × init-pattern × transport) 위에 axis 의 axis 가 앉아서,
> 누가 큐브 한 면을 추가하면 아래 mirror 면들을 알아서 다시 그려줍니다.
> 사람은 axes_registry() 한 줄만 만지면 끝 — 손으로 동기화할 필요 없음."**

own 41 의 마지막 자동화 단계. 본 spec 이 land 되면 axis-5 (verifier) /
axis-6 (future N+2) 추가 비용이 **사실상 0** 으로 떨어집니다.

---

## §8 cross-reference

| anchor | 역할 |
|--------|------|
| `tool/anima_cli/chat/axes/_registry.hexa` | axis 의 axis SSOT (229 줄) |
| `tool/anima_cli/chat/lanes/benchmark.hexa` L138-468 | 본 spec 의 auto-gen target (vendored mirror, ~27 줄 hardcode) |
| `anima/registry/render.hexa` | yaml→md 기존 패턴 참조 (155 줄) |
| `tool/transient_py/anima_artifact_registry_render.py` | raw#37 helper 패턴 참조 |
| `anima/registry/anima_artifact_registry.yaml#chat_axes_meta` | yaml mirror (own 39) |
| `docs/anima_chat_orchestra_axis_n1_hook_plan_2026_05_09.md` | own 41 hook plan T+1 doc |
| `.roadmap.cli` `cli.axis_n1_hook_t1_2026_05_10` | 본 spec 의 다음 cycle anchor |

## §9 own mandates 정합

- **own 16** model load 절대 금지 — render_axes.hexa 는 string 처리만 (모델 0)
- **own 22** mandatory report — diff/render 결과 emit 강제
- **own 24** single SSOT — axes/_registry.hexa 가 master, benchmark.hexa 는 view
- **own 33** trinity emit (D + own + H) — render_axes.hexa C3 emit ≥5
- **own 34** mandate-1 wrap=0 — text-only output
- **own 38** 매단계 axis-A doc save — 본 spec 자체가 axis-A doc
- **own 39** yaml↔md SSOT — 본 spec 이 own 39 의 hexa-side 확장 (hexa↔hexa)
- **own 41** axis-N+1 hook — 본 spec 이 own 41 의 final FULL automation step
  (= F-axes-FULL_AUTO_GEN)

## §10 raw#15 additive 정합

- 기존 render.hexa (155 줄) 무수정 — 별도 render_axes.hexa 신설
- benchmark.hexa 는 BEGIN/END marker 추가만 (one-time, 이후 marker 안 자동 관리)
- 기존 manual mirror 27 줄은 첫 render --diff PASS 후 marker 안으로 흡수
- helper transient_py 신규 (PyYAML 불필요, 순 string)
- 기존 사용자 명령 표면 무변 — `hexa run anima/registry/render_axes.hexa` 신규 진입점만 추가

---

_End of design spec — implementation 은 다음 cycle (예: 2026-05-11) T+1 ~ T+4 에서 진행._
