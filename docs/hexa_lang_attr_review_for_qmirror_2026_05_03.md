---
title: hexa-lang 문법 + attribute system 개선 검토 — nexus.qmirror 구현 관점
date: 2026-05-03
mode: doc-only deliverable (no impl, no execution, no hexa-lang patch)
authors: anima cycle agent (qmirror substrate review)
substrate refs:
  - /Users/ghost/core/anima/docs/nexus_qmirror_spec_2026_05_03.md
  - /Users/ghost/core/nexus/.roadmap.qmirror
  - /Users/ghost/core/nexus/modules/qrng/{anu,hardware_qrng,mock_qrng}.hexa
  - /Users/ghost/core/hexa-lang/doc/{spec.md,ai-native-attrs.md}
  - /Users/ghost/core/hexa-lang/stdlib/{proc,json_object,qrng_anu,math,net/http_client}.hexa
  - /Users/ghost/core/hexa-lang/stdlib/{linalg,matrix}/
  - /Users/ghost/core/hexa-lang/proposals/rfc_*.md
gate: raw#9 (hexa-only nexus, .py concession via _python_bridge/), raw#91 (≥5 honest C3 caveats)
---

> 📦 Available at: https://github.com/need-singularity/qmirror (`hx install qmirror`)

# 0. TL;DR

`nexus.qmirror`를 현재 hexa-lang(spec v0.1)으로 구현하는 데 **언어 자체를 패치할 의무는 없다**. 기존 `nexus/modules/qrng/anu.hexa` 패턴(struct + `exec("curl ...")` + env-gated live + `_mock_fixture`)으로 P1/P2 deliverable 8개 파일 모두 작성 가능하다. 단 두 가지 마찰점만 실제 갭이다:

1. **subprocess JSON exchange ergonomics** — `exec("python3 ... | base64")` → `json_parse` 라운드트립이 매 sampler/engine 호출마다 반복된다. **stdlib `proc_run_json_bridge(cmd, stdin_str) -> map`** 한 함수만 추가하면 boilerplate가 사라진다 (P0).
2. **complex 수치 타입 부재** — Aer가 반환하는 `[complex]` amplitude vector를 hexa 측에서 `[float] re + [float] im` parallel array로 풀어 다뤄야 한다. struct로 wrappable하므로 P1 권장, 차단요인은 아니다.

신규 attribute 6종 후보 중 **실질 ROI가 있는 건 `@quantum_substrate(tier)` 1개뿐** — 나머지(`@measurement_source`, `@simulator_backend`, `@calibration_anchor`, `@falsifier`, `@honest_c3`)는 구조화된 doc-comment + struct field로 동등한 효과를 낼 수 있다. attribute system은 **현재 `@tool/@usage/@sentinel/@resolver-bypass` 4종이 nexus convention의 사실상 표준**이고, 새 attr 한 개를 추가할 때마다 parser/ai_native_pass 양쪽 코드 변경이 필요하다는 점에서 보수적 권고가 옳다.

---

# 1. 현재 hexa-lang 능력 (qmirror 관점)

| 능력 영역 | 현재 hexa 지원 | qmirror 요구 | 갭 평가 |
|-----------|---------------|--------------|---------|
| struct (record) 선언 | EXACT — `struct QrngBytes { ok: int, ... }` | QmirrorBytes/ChshVerdict/PhiStarVerdict/RhoMatrix | **충분** |
| primitive types (8종: int/float/bool/char/string/byte/void/any) | EXACT (spec §2) | int, float, str, byte는 다 있음 | **충분** |
| array `[T]` + map `{k: v}` | EXACT — `[int]`, `{str: int}` 모두 사용중 | counts: {str:int}, bytes: [int] | **충분** |
| complex number | **미지원 native primitive** | `[complex]` amplitude vector | **갭** (struct로 우회 가능) |
| enum / sum type | spec §3.2에 키워드 `enum` 있으나 stdlib/nexus에 활용 사례 없음 (`grep -rn "^enum"` 0 hits) | T0/T1/T3, aer/cirq/mps backend variant | **갭** (int constant로 우회 — 기존 `tier: int=0|1|3` 패턴) |
| `exec()` (synchronous popen) | EXACT — runtime builtin | curl, python3 bridge, ls, printenv | **충분** (단 ergonomics 부족) |
| JSON parse/serialize | stdlib `json_object` (read), runtime `json_parse` 존재. **serializer 약함** (write 시 manual concat) | calibration cache write/read | **부분 갭** |
| HTTP client | stdlib `net/http_client` (curl-shellout, GET only; POST는 raw exec) | ANU GET + `x-api-key` header | **거의 충분** (header 옵션 없음 — `exec("curl -H ...")` fallback) |
| matrix / linalg | stdlib `linalg`, `matrix` 디렉터리 존재 (BLAS-lite sgemm/sgemv/sdot/saxpy/snrm2) | tomography ρ matrix, partition cov | **충분** |
| try/catch error handling | spec §3.11 키워드 (`try/catch/throw/panic/recover`) 정의되어 있으나 nexus modules에 활용 0 (대신 `ok: int` Result-like struct convention) | ANU 429, Aer crash, queue timeout | **충분** (convention 우위) |
| async / spawn / channel | spec §3.7 정의됨, 실제 codegen `@parallel` 미구현 (ai-native-attrs.md L74-79: "파서/검증만") | 8 GPU sharded calibration | **갭** (P3 calibration burst까지는 sequential OK) |
| @attr system | 13종 공식 + `@symbol/@optimize` 보조 + nexus convention 4종 (`@tool/@usage/@sentinel/@resolver-bypass`) | quantum_substrate, measurement_source 등 | **확장 가능하나 보수 권고** |
| structured concurrency (`scope`/`defer`) | interpreter mode만 지원, AOT codegen 미구현 (proc.hexa 주석 L320-345) | python_bridge cleanup | **갭** (`proc_reap()` 명시 호출로 우회) |
| comptime / macro | spec §3.10 키워드만, 미구현 | 없음 | N/A |

**핵심 관찰:** hexa-lang은 spec v0.1 단계로 **키워드 53종은 정의되어 있으나 구현된 건 약 60%** (특히 G2 `@evolve`, G3 외 attrs는 파서/카운트 단계만). **nexus modules가 실제로 쓰는 패턴은 좁다** — struct + fn + exec + while + if/return. qmirror도 이 좁은 패턴 안에 머무르면 거의 비용이 들지 않는다.

---

# 2. qmirror가 필요로 하는 기능 — 8 항목

각 항목: 현재 hexa 지원 → qmirror가 어떻게 처리할 것인가 → 갭이면 우선순위.

## 2.1 subprocess invocation (Python bridge용)

- **현재 지원:** `exec(cmd: str) -> str` builtin. `exec("python3 -m nexus.qmirror.engine_aer.aer_runner ...")` 그대로 작동. stdout 한 덩어리로 받는다.
- **qmirror 사용:** `engine_aer.hexa::engine_run(circ)` → exec helper → JSON 파싱 → amplitude array.
- **갭:** **(P0)** stdin으로 QASM3 string을 넘겨야 하는데 현재 `exec()`는 stdin redirect를 caller가 shell 문자열로 (`echo '...' | python3 ...`) 직접 만들어야 한다. 1KB 이상 QASM은 ARG_MAX 위험. **개선안:** stdlib `proc_run_with_stdin(cmd, stdin: str) -> str` 또는 더 좋게는 `proc_run_json_bridge(cmd, payload: map) -> map` (heredoc + base64 wrapping internalize).

## 2.2 JSON serialization (calibration cache, ANU response)

- **현재 지원:** `json_parse(text) -> map|array|void` (runtime), `stdlib/json_object` wrapper (read). `qrng_anu_parse_response()` 좋은 reference impl.
- **qmirror 사용:** ANU response 읽기 — ✓. Calibration v2_*.json **쓰기** — manual `"{\\"key\\": " + ... + "}"` 문자열 concat.
- **갭:** **(P1)** `json_stringify(v) -> str` builtin/stdlib 부재. anu.hexa의 `_anu_parse`는 substring/split 수동 파싱(L61-80) — fragile. **개선안:** `stdlib/json_object_write.hexa` 신규 (`json_object_set`, `json_dump_str(map, indent: int) -> str`).

## 2.3 REST HTTP client (ANU API + x-api-key header)

- **현재 지원:** `stdlib/net/http_client::http_get(url, timeout)`. **header 미지원** — qmirror.entropy.hexa는 `x-api-key`가 필수.
- **qmirror 사용:** raw `exec("curl -H 'x-api-key: " + key + "' ...")` 직접 — anu.hexa 패턴 재활용.
- **갭:** **(P1)** `http_get_with_headers(url, headers: map, timeout) -> map` 추가 권장. 차단요인은 아님 (curl 직접 호출 OK).

## 2.4 state vector arithmetic (complex number)

- **현재 지원:** **complex primitive 부재**. float만 있음. spec §2 8 primitive에 complex 없음.
- **qmirror 사용:** Aer가 `[(re, im), (re, im), ...]` JSON 반환 → hexa 측에서 `struct Complex { re: float, im: float }` + parallel `[Complex]` array로 풀기.
- **갭:** **(P2)** native `complex` 타입 추가하면 Aer/Cirq 결과 직접 받기 + linalg complex extension까지 같이 해야 의미 있음. struct wrap이 충분히 좋음.

## 2.5 bytes / hex encoding (entropy bits)

- **현재 지원:** `byte` primitive 정의, 실사용은 `[int]` (0~255) array — anu.hexa, mock_qrng.hexa 동일 convention. hex parse: `exec("printf '%d' 0x" + pair)` shell-out (hardware_qrng.hexa L113).
- **qmirror 사용:** entropy_pull(8) → `[int]` 8개 → uint64 conversion → float [0,1).
- **갭:** **(P1)** `bytes_to_uint64(b: [int]) -> int`, `int_from_hex(s: str) -> int`, `hex_encode(b: [int]) -> str` stdlib 부재. shell-out fallback 작동하나 perf 손실 (per-call printf fork). **개선안:** `stdlib/bytes.hexa` 신규.

## 2.6 typed records (QmirrorBytes, ChshVerdict, PhiStarVerdict)

- **현재 지원:** EXACT — struct + fn helper(`qrng_bytes_ok` / `qrng_bytes_fail`) convention.
- **qmirror 사용:** 그대로 — `struct ChshVerdict { S: float, std: float, violation_sigma: float, E_ab: float, E_abp: float, E_apb: float, E_apbp: float, ok: int }`.
- **갭:** **없음.** 가장 안정된 영역.

## 2.7 enum / variant types (T0/T1/T3 source, aer/cirq/mps backend)

- **현재 지원:** spec §3.2 `enum` 키워드 정의, **stdlib/nexus 활용 0**. 실사용은 `tier: int = 0|1|3`, `engine: str = "aer"|"cirq"`.
- **qmirror 사용:** 기존 convention 따라 `int` + `str` constant.
- **갭:** **(P2)** sum type / pattern matching이 있으면 backend dispatch가 깔끔하나, 현재 `if env == "cirq" { ... }` chain이 작동한다. 차단요인 아님.

## 2.8 error handling (ANU 429, queue timeout, Aer crash)

- **현재 지원:** spec §3.11 `try/catch/throw/panic/recover` 키워드 있으나 **nexus 활용 0** (`grep -rn "try " nexus/modules/`). Result-like `struct { ok: int, message: str, ...payload }` 가 표준.
- **qmirror 사용:** `QmirrorBytes { ok: 0, message: "anu: 429 rate limit" }` 패턴 그대로.
- **갭:** **없음.** convention 우위 — typed Result struct가 try/catch보다 honest C3 trace에 더 좋다 (verdict.json 직렬화 자연스러움).

---

# 3. attribute 개선안 — 6 신규 후보 평가

각 후보: 필요성 검토 + 기존 mechanism으로 처리 가능한가 + 추천 verdict.

## 3.1 `@quantum_substrate(tier: T1|T2|T3)`

- **목적:** module이 어느 tier에서 동작하는지 compiler/registry가 인식.
- **기존 우회:** struct field `tier: int` + `qrng_source_meta_*()` fn (이미 anu.hexa, hardware_qrng.hexa, mock_qrng.hexa 모두 사용중).
- **신규 attr ROI:** **중간.** registry autodiscover (`stdlib/registry_autodiscover.hexa`)가 attr-based scan을 지원하면 자동 분류가 가능. 그러나 현재 nexus의 `qrng_meta_make()` 패턴이 충분히 작동.
- **Verdict:** **권장 (P2).** registry autodiscover 확장과 같이 land해야 의미. 단독 land는 noise.

## 3.2 `@measurement_source(source: anu|hardware|mock)`

- **목적:** verdict.json 출력에 entropy provenance 자동 첨부.
- **기존 우회:** `QmirrorBytes.message` 필드에 string literal로 이미 표시 (`"anu: live (vacuum-fluctuation)"`, `"hardware_qrng: mock fixture"`).
- **신규 attr ROI:** **낮음.** message string + `provenance: str` field 하나면 충분.
- **Verdict:** **불필요.** struct field로 처리.

## 3.3 `@simulator_backend(backend: aer|cirq|mps)`

- **목적:** 어느 simulator를 사용했는지 verdict에 기록.
- **기존 우회:** `CountsResult.engine: str` 이미 spec에 있음 (qmirror_spec §3.5).
- **신규 attr ROI:** **낮음.** runtime dispatch가 필요하지 compile-time tag가 필요하지 않음.
- **Verdict:** **불필요.**

## 3.4 `@calibration_anchor(version: str)`

- **목적:** calibration cache file (`v2_*.json`)을 version-lock.
- **기존 우회:** file path 자체에 version embed (`calibration/v2_2026_05_07.json`), `calibration_version: str` field.
- **신규 attr ROI:** **낮음.** 정적 string lock은 const declaration으로 충분.
- **Verdict:** **불필요.**

## 3.5 `@falsifier(id: str)`

- **목적:** F1-F5 falsifier 함수를 자동으로 etcd-style discoverable.
- **기존 우회:** fn 명명 convention `fn _falsifier_f1_anu_reachable() -> int { ... }` + selftest dispatcher.
- **신규 attr ROI:** **중간.** `@test`와 비슷한 자동 실행 runner ROI 있음. 그러나 spec.md G2에 `@test` 이미 있음 — `@test(group="falsifier", id="F1")` 같은 generalized parameter로 충분.
- **Verdict:** **불필요 (`@test` 매개변수화로 흡수).**

## 3.6 `@honest_c3(caveats: list[str])`

- **목적:** raw#91 (≥5 caveats) 자동 검증 — module README가 honest C3 카운트 미달 시 컴파일 경고.
- **기존 우회:** doc lint script (`tool/honest_c3_lint.hexa`) 별도 실행.
- **신규 attr ROI:** **중간.** raw#91 enforcement는 nexus 전체에 적용되는 정책. attr보다는 `tool/lint` 스크립트가 더 적절 (compiler dependency 추가 회피).
- **Verdict:** **불필요 (lint tool로 충분).**

---

# 4. P0/P1/P2 우선순위 분류

| 우선순위 | 항목 | 근거 | 차단 모듈 |
|----------|------|------|----------|
| **P0 (Phase 1 전 필수)** | `proc_run_with_stdin(cmd, stdin: str) -> str` stdlib 추가 | engine_aer ↔ aer_runner.py heredoc fragile + ARG_MAX 위험 | `engine_aer.hexa`, `engine_cirq.hexa` |
| P0 | (선택) `proc_run_json_bridge(cmd, payload: map) -> map` 한 번 더 위 | 위 패턴이 5+ 호출지점에서 반복 | 위 + `tomography.hexa`, `iit_mip.hexa` |
| **P1 (Phase 2 전 권장)** | `json_stringify(v) -> str` builtin or stdlib | calibration v2_*.json write | `engine_aer.hexa` (calibration cache writeback), `selftest.hexa` (verdict file) |
| P1 | `http_get_with_headers(url, headers, timeout)` | ANU `x-api-key` 헤더 | `entropy.hexa` |
| P1 | `stdlib/bytes.hexa` (`bytes_to_uint64`, `hex_encode`, `int_from_hex`) | sampler.hexa per-shot perf (현재 shell printf fork) | `sampler.hexa` |
| **P2 (Phase 3+ / 차기 cycle)** | native `complex` primitive + linalg complex extension | Aer amplitude direct binding, tomography ρ matrix native | (P3 calibration anchor doc 진입 후) |
| P2 | `@quantum_substrate(tier)` attr + registry_autodiscover 확장 | nexus tier-based registry 자동 분류 | (cross-module 작업) |
| P2 | structured concurrency (`scope`/`defer`) AOT codegen 완성 | python_bridge subprocess auto-cleanup | (proc.hexa Phase 3 follow-up과 합류) |

**P0이 P1에 비해 명확히 더 적은 이유:** `exec()` + manual heredoc 우회가 가능 — 즉 P0를 skip해도 작동하는 코드는 짤 수 있다. 다만 5+ 호출지점에서 같은 boilerplate 반복 + escape bug risk → 1회 stdlib 추가가 ROI 압도적.

---

# 5. 구체 patch 제안

## 5.1 `proc_run_with_stdin` (P0)

**파일:** `/Users/ghost/core/hexa-lang/stdlib/proc.hexa` (기존 파일에 추가; 신규 file 불필요).

```hexa
// proc_run_with_stdin(cmd, stdin_str) -> string
//
// Spawns `cmd` (synchronous, like exec()) but pipes stdin_str on STDIN
// instead of caller building heredoc. Returns stdout.
//
// Implementation: temp-file based to dodge ARG_MAX + escape hell.
//   1. Write stdin_str to /tmp/hexa_proc_stdin_<pid>_<nonce>.txt
//   2. exec(cmd + " < " + tmpfile)
//   3. Read stdout, unlink tmpfile.
pub fn proc_run_with_stdin(cmd: string, stdin_str: string) -> string {
    let nonce = to_string(_now_epoch()) + "_" + to_string(len(stdin_str))
    let tmp = "/tmp/hexa_proc_stdin_" + nonce + ".txt"
    write_file(tmp, stdin_str)
    let out = to_string(exec(cmd + " < '" + tmp + "' 2>&1"))
    let _ = exec("rm -f '" + tmp + "'")
    return out
}
```

**Breaking risk:** none — purely additive. Existing `exec()` callers untouched.

## 5.2 `proc_run_json_bridge` (P0 선택, 위 위에서 build)

```hexa
// proc_run_json_bridge(cmd, payload) -> map
//
// Sends `payload` (hexa map) as JSON on stdin, parses stdout as JSON.
// Returns parsed map. On parse failure returns {"ok": 0, "error": "..."}.
//
// Standard contract for all _python_bridge/ helpers.
pub fn proc_run_json_bridge(cmd: string, payload) {
    let stdin_str = json_stringify(payload)  // requires §5.3
    let stdout = proc_run_with_stdin(cmd, stdin_str)
    let result = json_parse(stdout)
    if type_of(result) != "map" {
        let err = #{}
        err["ok"] = 0
        err["error"] = "bridge: stdout was not JSON map; got " + stdout.substring(0, 200)
        return err
    }
    return result
}
```

## 5.3 `json_stringify` (P1)

**파일:** `/Users/ghost/core/hexa-lang/stdlib/json_object.hexa` (기존 read-side wrapper에 write-side 짝지움).

```hexa
// json_stringify(v) -> string
//
// Recursive serialization of map/array/scalar to JSON text.
// Uses runtime type_of() to dispatch; falls back to "null" on void.
// String escaping: \\, \", \n only (minimal). Numbers via to_string.
pub fn json_stringify(v) -> string {
    let t = type_of(v)
    if t == "void" { return "null" }
    if t == "bool" { if v { return "true" } else { return "false" } }
    if t == "int" || t == "float" { return to_string(v) }
    if t == "string" { return "\"" + _json_escape(v) + "\"" }
    if t == "array" { ... }
    if t == "map"   { ... }
    return "null"
}
```

## 5.4 `http_get_with_headers` (P1)

**파일:** `/Users/ghost/core/hexa-lang/stdlib/net/http_client.hexa`.

```hexa
pub fn http_get_with_headers(url: string, headers, timeout_sec: int) -> string {
    let mut hflags = ""
    let ks = dict_keys(headers)
    let mut i = 0
    while i < len(ks) {
        let k = ks[i]
        let v = headers[k]
        hflags = hflags + " -H " + _shell_escape(k + ": " + v)
        i = i + 1
    }
    let t = if timeout_sec > 0 { timeout_sec } else { 30 }
    let cmd = "curl -sSL --fail --max-time " + to_string(t) + hflags + " " + _shell_escape(url) + " 2>/dev/null"
    return to_string(exec(cmd))
}
```

## 5.5 `stdlib/bytes.hexa` (P1 신규 파일)

```hexa
pub fn bytes_to_uint64(b) -> int {
    if len(b) < 8 { return 0 }
    let mut u = 0
    let mut i = 0
    while i < 8 {
        u = u * 256 + b[i]
        i = i + 1
    }
    return u
}

pub fn int_from_hex(s: string) -> int { ... }
pub fn hex_encode(b) -> string { ... }
```

## 5.6 (P2) `@quantum_substrate(tier)` attr — patch sketch only

- **lexer:** `@quantum_substrate` 토큰 인식 (이미 `@` → `At` 토큰 + identifier 패턴 재사용).
- **parser:** `parse_attr_args` (proposals/rfc_005 패턴 참조) 확장 — `tier: int` argument.
- **ai_native_pass:** classify into G2 시맨틱 group.
- **codegen:** no-op (metadata-only, registry consumes).
- **registry_autodiscover.hexa:** scan attr → `{module, tier}` map 출력.

**Patch line cost 추정:** ~80 LOC across 4 files. **Breaking risk:** 기존 module이 attr를 사용하지 않는 한 0.

---

# 6. Honest C3 (raw#91, ≥5 caveats)

1. **stdlib 신규 함수 추가는 hexa-lang runtime 의존성 변경이 아니다.** 위 P0/P1 patch는 모두 `stdlib/*.hexa` 파일 추가/수정만으로 끝난다. **단,** stdlib 파일도 기존 testsuite (`stdlib/test/*`)에 selftest 추가가 필요하고, 이를 안 하면 silent regression 위험. (caveat 1)

2. **Parser 복잡도 증가 — attr 1개 추가의 실제 비용.** ai-native-attrs.md L168-179 file map을 보면 attr 1개당 평균 5 file (lexer/parser/ai_native_pass/build_c/test_bootstrap_compiler) 변경. `@quantum_substrate` 한 개도 80+ LOC + ai_native_pass의 100종 마일스톤 시퀀스에 끼워 넣어야 함. **부주의 변경 시 기존 13종 attr 회귀 위험.** (caveat 2)

3. **기존 module breaking risk — convention 깨기.** 현재 nexus convention은 `tier: int = 0|1|3` field-based. `@quantum_substrate`를 도입하면 일관성 깨짐 — qrng/anu.hexa 같은 기존 IMPLEMENTED 모듈을 retrofit하지 않으면 두 convention이 공존 (혼란). retrofit하면 5+ 모듈 동시 patch — review burden. (caveat 3)

4. **Learning curve — AI-native intent와 충돌 가능성.** spec §3.12의 `intent/generate/verify/optimize` AI-native paradigm은 **사용자가 attr를 손으로 안 적는 방향**. 새 attr를 도입하면 intent block이 자동 주입해야 할지, 사용자가 명시해야 할지 정책 결정 필요. 현재 13종도 자동 주입 vs 명시 혼재 (M82-M84). (caveat 4)

5. **Python bridge 자체가 raw#9 violation의 큰 그림 — hexa-lang 패치로 해결 안 됨.** §5의 `proc_run_with_stdin`은 ergonomics를 개선할 뿐 .py 파일이 nexus repo에 들어오는 것 자체는 막지 않는다. P4 (FFI to C state-vector kernel) 까지 가야 진짜 해결. **이 review의 모든 P0/P1 권고는 bridge 의존을 더 편하게 만드는 것** — 즉 raw#9 spirit과 trade-off. 명시적 disclosure 필요. (caveat 5)

6. **complex primitive 도입은 cascading cost.** §2.4의 native `complex`는 단독 추가 불가 — linalg (sgemm 등)을 complex 변종으로 확장, parser literal `1.0+2.0i` 추가, codegen 양쪽 (interp/AOT) 모두 작업. **6+ file scope, 수백 LOC.** P2로 미룬 이유 — qmirror struct wrap이 충분히 honest. (caveat 6)

7. **`json_stringify`의 정확도 caveat.** §5.3의 implementation은 minimal escaping (`\\`, `\"`, `\n`)만 처리 — 완전한 RFC 8259 준수가 아님. UTF-16 surrogate pair, control character escape 누락. calibration cache 같은 ASCII-only 데이터에는 안전하나 임의 user input direct serialize는 안전하지 않음. **stdlib doc-comment에 명시 필수.** (caveat 7)

---

# 7. concise 최종 report (under 250 words)

**Verdict: hexa-lang 자체 변경 불필요 — stdlib에 함수 2개만 추가 권고.**

**P0 (qmirror Phase 1 전):**
1. `stdlib/proc.hexa::proc_run_with_stdin(cmd, stdin_str) -> str` — engine_aer ↔ python bridge ARG_MAX 회피. ~30 LOC, 기존 file 수정만, breaking risk 0.
2. (`proc_run_json_bridge` build on top — 선택, ROI 매우 높음)

**P0/P1 가장 시급 — 이 두 개 없이도 우회 가능하지만 5+ 호출지점에서 boilerplate 반복.**

**추천 attribute (1-2개만):**
- `@quantum_substrate(tier)` — P2 권장, registry autodiscover 확장과 함께 land 시에만. 단독 land는 noise.
- 나머지 5종 (`@measurement_source`, `@simulator_backend`, `@calibration_anchor`, `@falsifier`, `@honest_c3`) — **모두 불필요**, 기존 struct field + doc-comment + lint tool로 동등.

**hexa-lang 변경 없이 우회 가능 (stdlib만으로 OK):**
- ANU REST + x-api-key (`exec("curl -H ...")` 직접)
- complex amplitude (struct Complex { re, im })
- enum/variant types (int constant + str)
- error handling (`ok: int` Result struct, 기존 nexus convention)
- async / spawn (Phase 1/2는 sequential OK; Phase 3 calibration도 IBM API queue가 어차피 직렬)

**진짜 필요한 것 (struct로 우회 비용 너무 큼):**
- subprocess stdin pipe (P0, ARG_MAX risk)
- json_stringify (P1, calibration cache writeback)
- bytes_to_uint64 등 (P1, per-shot perf)

**핵심 honest C3:** Python bridge 자체가 raw#9 violation의 큰 그림 — hexa-lang stdlib patch는 bridge를 *편하게* 만들 뿐이다. 진짜 해결은 P4 FFI C kernel.
