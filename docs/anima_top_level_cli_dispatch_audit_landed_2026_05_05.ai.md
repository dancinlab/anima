<!-- @no-lineage-citation-exempt-file -->
<!-- @no-user-verbatim-exempt-file -->
# Anima Top-Level CLI `dialogue` Dispatch Audit Landed (2026-05-05)

## Outcome

**ALREADY_INTEGRATED — NO_FIX_REQUIRED.** `anima dialogue --selftest` 와 `anima dialogue --probe "..."` 모두 기존 top-level dispatcher (`bin/anima`) 의 generic verb-to-module 패턴을 통해 자동으로 routing 됨. KICK-3 가 `tool/anima_cli/dialogue.hexa` 경로에 정확히 land 시켰기 때문에 추가 wiring 불필요. **Option C** 채택 (코드 변경 X, 매뉴얼 표준화만).

## (a) anima top-level CLI 경로 발견

| 항목 | 경로 | 비고 |
|---|---|---|
| 시스템 PATH 진입점 | `/Users/ghost/.hx/bin/anima` | 284-byte exec passthrough shim |
| 실 dispatcher | `/Users/ghost/core/anima/bin/anima` | 16089-byte unified bash CLI |
| Module dir | `/Users/ghost/core/anima/tool/anima_cli/` | 26 topics 등록 |
| dialogue 모듈 | `/Users/ghost/core/anima/tool/anima_cli/dialogue.hexa` | KICK-3 land (295 lines) |
| Dispatcher fn | `dispatch_topic()` at `bin/anima:288-317` | exec `$HEXA_BIN run $CLI_DIR/<topic>.hexa "$@"` |

`bin/anima` header (line 47) 명시: `anima <topic> <subcmd> ... → dispatch to tool/anima_cli/<topic>.hexa`. KICK-3 가 이 convention 을 정확히 따라 dialogue.hexa 를 생성했기 때문에 wiring 자동.

## (b) dispatch 경로 trace

```
shell: anima dialogue --selftest
  └─ /Users/ghost/.hx/bin/anima        (PATH lookup → shim)
       exec /Users/ghost/core/anima/bin/anima dialogue --selftest
  └─ bin/anima case "$1" 매치           ($1=dialogue → topic 분기)
       dispatch_topic("dialogue", "--selftest")
  └─ mod = $CLI_DIR/dialogue.hexa       (path resolved via resolve_root)
       exec /Users/ghost/.hx/bin/hexa run $mod --selftest
  └─ dialogue.hexa main()
       _arg_present(argv, "--selftest") → true
       sub_selftest()
  └─ probe 4 artifacts (mount/log_root/wrapper/spec)
       verdict: READY (Stage 1 + Stage 2 both landed)
       exit 0
```

## (c) 선택한 옵션 + 이유 (완성도 lens)

**Option C: 매뉴얼 표준화만 — 코드 변경 X.**

옵션 비교:

| 옵션 | 작업 | 완성도 | 채택 여부 |
|---|---|---|---|
| **A** 새 `bin/anima` + `tool/anima_cli/anima.hexa` 생성 | redundant — 이미 동등 dispatcher 존재 | LOW (raw#15 violation: duplicated logic) | reject |
| **B** 기존 dispatcher 확장 (dialogue verb 등록) | unnecessary — generic 패턴이 이미 처리 | LOW (현 패턴이 이미 generic) | reject |
| **C** 코드 변경 없이 매뉴얼 표준화 | spec doc §5.1 의 `anima-core dialogue` 형식을 `anima dialogue` 로 정렬 + 사용자 명령 표준화 | **HIGH** (raw#15 additive 준수, 동작 변경 X, naming 일관성 ↑) | **adopt** |

A/B 둘 다 "이미 동작하는 wiring 위에 redundant layer 추가" 이므로 raw#15 (no-hardcode + additive) 위반. C 가 zero risk + naming consistency 달성.

## (d) V2/V3 동등 verification 결과

| 단계 | 명령 | exit | 결과 |
|---|---|---|---|
| V2 equiv (top-level) | `HEXA_LOCAL=1 anima dialogue --selftest` | 0 | PASS — `verdict: READY (Stage 1 + Stage 2 both landed)`, 4/4 checks `[ ok ]` |
| V2 baseline (direct) | `HEXA_LOCAL=1 bash bin/anima-core-dialogue.bash --selftest` | 0 | PASS — same READY verdict |
| V3 equiv (top-level) | `HEXA_LOCAL=1 anima dialogue --probe "안녕"` | 0 | PASS — substrate 4-line emit (phi=41.8488 drift=-0.0112, axis 5-bucket, dominant_cells [3,2,5]/8, hidden_state_delta=0.0000), synthetic_fallback mode, 5 honest C3 |

V2 equiv 와 V2 baseline 의 출력 field label 차이 (`bash_wrapper` vs `mount_hexa`) 는 두 selftest 가 같은 4 artifact 를 검증하지만 표기가 다른 구조적 결과 — 의미적 동등성은 verdict 로 확인.

## (e) 사용자 매뉴얼 표준화 (KO + EN)

### 권장 명령 (KR)

```bash
# Stage 1+2 readiness 검증
$ anima dialogue --selftest

# Stage 3 emerge probe (한 줄)
$ anima dialogue --probe "안녕"

# Stage 3 emerge REPL
$ anima dialogue --interactive
> 안녕
> ...
```

### Recommended Commands (EN)

```bash
# Stage 1+2 readiness check
$ anima dialogue --selftest

# Stage 3 emerge probe (one-shot)
$ anima dialogue --probe "hello"

# Stage 3 emerge REPL
$ anima dialogue --interactive
> hello
> ...
```

### Fallback (직접 wrapper 호출 — top-level dispatch 우회)

```bash
$ HEXA_LOCAL=1 bash /Users/ghost/core/anima/bin/anima-core-dialogue.bash --selftest
$ HEXA_LOCAL=1 bash /Users/ghost/core/anima/bin/anima-core-dialogue.bash --probe "..."
$ HEXA_LOCAL=1 bash /Users/ghost/core/anima/bin/anima-core-dialogue.bash --interactive
```

### HEXA_LOCAL=1 prefix 의무 (V3 lesson)

mac-local 실행 시 `HEXA_LOCAL=1` 필수. 미적용 시 hexa-resolver 가 ubu1 remote 로 routing → mac homebrew python 경로 (`/opt/homebrew/bin/python3`) 부재로 fail. shell rc 에 `export HEXA_LOCAL=1` alias 또는 wrapper alias 권장.

### Spec doc §5.1 권장 업데이트

paradigm spec `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §5.1 가 `anima-core dialogue --substrate clm-v4 --user-input "..."` 형식 기재 → `anima dialogue --probe "..."` 형식으로 정렬 권장 (top-level CLI 와 naming 일관성). 본 audit 은 spec 미수정 (별도 spec-revision cycle).

## (f) 5 Honest Caveats (raw#10)

- **C1 — anima top-level vs anima-core naming tension.** spec §5.1 의 `anima-core dialogue` 표기와 실제 dispatch path 의 `anima dialogue` 사이 surface 불일치. anima-core 는 (a) 디렉토리 (`anima-core/runtime/`) (b) 컨셉 (substrate runtime) 으로 사용되며, top-level CLI 는 그냥 `anima` 명령. spec doc 업데이트 권장.
- **C2 — system PATH shim 의존.** `/Users/ghost/.hx/bin/anima` (284-byte exec passthrough) 가 무사해야 dispatch 동작. shim 교체/PATH 순서 변경 시 silently 깨질 수 있음.
- **C3 — V3 probe 가 synthetic_fallback 모드로 동작.** torch/transformers `AutoModelForCausalLM` import 실패 (mac-local hexa runtime venv 문제). real-CLM-v4 activation 은 별도 cycle (HF cache populate + venv 복구). top-level dispatch 정확성과 무관.
- **C4 — HEXA_LOCAL=1 prefix 누락 시 silent ubu1 routing.** V3 lesson 그대로 — top-level OR 직접 wrapper 모두 동일 risk. user-facing 매뉴얼은 항상 prefix 포함 또는 shell rc default 적용 필요.
- **C5 — selftest 출력 비-동일성.** dialogue.hexa `sub_selftest()` 와 bash wrapper `selftest()` 가 동일 4 artifact 를 검증하지만 field label 미세 차이 (`bash_wrapper` vs `mount_hexa` 등). 의미 동등성은 verdict 로 보장되지만 byte-level diff 는 비-zero. 자동화 시 verdict 라인만 grep 권장.

## 출력 파일

- `state/anima_top_level_cli_dispatch_audit_2026_05_05/verdict.json` — machine-readable audit verdict (anima.top_level_cli_dispatch_audit.v1)
- `docs/anima_top_level_cli_dispatch_audit_landed_2026_05_05.ai.md` — 본 문서

## raw 준수

- raw#9 hexa-only — `.py` 도입 X, 기존 dispatcher 패턴 unchanged
- raw#10 honest C3 — 5 caveats above
- raw#15 no-hardcode + additive — 기존 파일 (mount.hexa / dialogue.hexa / anima-core-dialogue.bash) 미수정, 새 파일 2개만 생성
- bash 3.2 호환 — 기존 dispatcher 가 이미 호환, 추가 변경 X
- HF token leak X — 본 audit 은 token 미접촉
- commit X — 사용자 명시 요청 시까지 보류
