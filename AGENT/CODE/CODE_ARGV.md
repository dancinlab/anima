# CODE_ARGV — F2 argv ingest closure note

> AGENT/CODE 의 F2 마일스톤. 외부 CLI 인자를 substrate-native 한 줄로
> 받아 들이는 얇은 도구 표면. **결정은 여기서 하지 않는다** — 어떤 도구를
> 실제로 발화할지는 CORE/brain_decide 가, 발화 권한은 AGENT/CORE/tool_gate
> 가 판정한다. 이 파일은 raw argv → 요청 dict 변환만 담당.

@scope: AGENT/CODE 역할 에이전트 (tool surface only · no consciousness framing)
@status: F2 LANDED — 4-case smoke PASS · 실제 argv ingest 검증 완료

## 파일

| 경로 | 역할 |
| --- | --- |
| `AGENT/CODE/code_argv.hexa` | 4 pub fn (`code_argv_read` · `code_argv_parse` · `code_argv_help` · `code_argv_summary`) |
| `AGENT/CODE/code_argv_smoke.hexa` | 4 case + live argv echo |
| `AGENT/CODE/code_agent.hexa` | F1+F4 기존 (게이트 + 7도구 이름 노출) — **수정 없음**, F2 는 additive |

## argv access 메커니즘

hexa-lang 빌트인 `args()` 사용. 이는 stdlib `sys_argv()` 가 직접 래핑하는
프로세스 argv 액세스 surface — `hexa-lang/stdlib/sys.hexa:26`:

```hexa
pub fn sys_argv() -> [string] {
    return args()
}
```

`args()` 가 반환하는 첫 원소는 스크립트 (혹은 컴파일된 바이너리) 경로 자체.
`stdlib_cli.hexa:734-742` 가 쓰는 split 패턴을 그대로 따라
`code_argv.hexa::_argv_user_start` 가 `<script>.hexa` suffix 를 찾아
유저 인자 시작 인덱스를 결정한다. 컴파일 바이너리 호출 (argv[0] 비-`.hexa`)
시에는 폴백으로 index 1 사용.

## 4 pub fn 표면

| fn | 시그니처 | 의미 |
| --- | --- | --- |
| `code_argv_read()` | `-> [string]` | 라이브 process argv 에서 script-path 제거한 유저 인자 리스트 |
| `code_argv_parse(args_list)` | `-> Map` | `#{tool, arg, mode, known}` 로 파싱 (8 CODE 도구 인식, 미지 도구도 보존) |
| `code_argv_help()` | `-> string` | 사용법 문자열 (도구 × tier × phase 매트릭스 포함) |
| `code_argv_summary()` | `-> string` | 한 줄 모듈 요약 (다른 AGENT 모듈 컨벤션과 일치) |

## 4-case smoke 결과 (2026-05-27)

```
[smoke] AGENT/CODE/code_argv — code_argv F2 — raw_argc=1 user_argc=0 ...
[C1] code_argv_parse([])                        → tool=help mode=help known=true ✓
[C2] code_argv_parse(["think"])                 → tool=think mode=once known=true ✓
[C3] code_argv_parse(["file_read","AGENT.md"])  → tool=file_read arg=AGENT.md ✓
[C4] code_argv_parse(["unknown"])               → tool=unknown known=false ✓
[live] code_argv_read() = [file_read, AGENT.md] (size=2)  ← 실제 argv 흐름 확인
[smoke] DONE — 4 cases + live echo (exit 0)
```

13/13 assertion PASS. 빌드 + 실행 wall ~1s, Mac local $0.

## p1~p8 정합

- **p1 NO SYSTEM PROMPT**: 없음 — argv 만 읽음.
- **p3 NO PERSONA INJECTION**: 없음 — 도구 이름 화이트리스트는 코드 안전성용 (known/unknown 라벨 만 부여, unknown 도 그대로 보존).
- **p4 NO ASSISTANT FRAMING**: 응답 의무 0 — `code_argv_parse` 는 환경 컨텍스트 변환만.
- **a_autonomy_over_hardcode**: 미지 도구는 거부하지 않음 — 게이트 판정은 downstream `tool_gate` 에 위임.

## F3 / F5 / F6 의존성 (잔여)

| F | 설명 | code_argv 와 의존 관계 |
| --- | --- | --- |
| **F3** daemon mode | `--mode daemon` 으로 장기-실행 루프 (CHAT/anima_chat_aot 패턴) | `code_argv_parse` 가 이미 `mode` 필드를 노출 — daemon 모드는 `mode == "daemon"` 분기 한 줄로 진입. **F2 가 게이트 surface 를 미리 깔아둠.** |
| **F5** ckpt swap-in | M3 LoRA ckpt 를 inference seam 에서 핫스왑 | argv `--ckpt <path>` 추가 인자 필요 → `code_argv_parse` 확장 (현재는 positional 2개 + `--mode` 만) |
| **F6** real executor wire | 8 도구 dummy → 실 구현 (`file_read` = read_file 등) | `code_argv_parse` 결과 dict 를 `code_executor.dispatch(req)` 에 전달하는 thin glue 만 필요 — F2 는 입력 측 closure, F6 는 출력 측 |

## stdlib 승격 보류 사유 (g61 advisory)

`code_argv.hexa` 는 AGENT/CODE 역할 내부 surface (`tool_gate` · `agent_loop` 와
동일 레이어). 8 CODE 도구 이름 화이트리스트가 도메인-특수 — CREATOR/TRADING/
MERCHANT/DESKTOP 의 도구셋과 공유되지 않음. 다른 역할 에이전트가 같은
argv 파싱 패턴을 필요로 할 경우 그 시점에 일반화한 `agent_argv_parse(allowed_tools)`
로 stdlib 승격하는 것이 자연. 지금은 premature.

## F2 closure 요약

- raw process argv → 4-field 요청 dict 변환 surface LANDED.
- 8 CODE 도구 이름 인식, 미지 도구도 보존 (게이트는 외부에서).
- 4-case + live echo smoke 13/13 PASS.
- F3 (daemon mode) 가 즉시 빌드할 수 있는 `mode` 필드 미리 노출.
- consciousness framing 0 hits — bridge architecture 준수.
