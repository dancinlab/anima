# [RESOLVED — PHANTOM/오진] hexa-lang x86_64-linux "codegen 버그" 핸드오프 — 폐기

> ⛔ **이 프롬프트는 obsolete다. 고칠 codegen 버그는 없다(측정 확정 2026-06-27, hexa-lang 세션).**
>
> **measured root-cause:** "x86_64 codegen 결함"은 PHANTOM(오진)이었다. 진짜 원인 = **pool 의 stale anima 모듈 스냅샷** — install overlay `~/.hx/src/core/generator.hexa`(6/23 = `gen_auto_ideate` 없음)가 module_loader 해석에서 current 소스(6/26 = 있음)를 shadow. arm64(mini)=current / x86_64(summer·aiden)=stale 였을 뿐 → "arch-gate"는 착시("어느 호스트가 stale 인가" gate). **어제(06-26) 이미 fix**(overlay 를 anima git current 로 sync).
>
> **검증 근거(출력):** 양 pool overlay 에 `gen_auto_ideate` def=1(summer/aiden 모두) · summer closure 빌드 "undeclared" 에러 **0개** → C-compile 통과·**링크 단계 도달**(= proto 정상 선언·정의의 직접 증거). codegen emitter 에 손댈 것 없음(phantom 쫓아 코드 바꾸면 tune-to-green 위반).
>
> **별개 관찰(codegen 무관):** summer `~/.hx/bin/build/runtime.a` 가 GPU 캠페인으로 CUDA-taint → summer hexa run 일시 깨짐. BUT **aiden 은 동일 cuda runtime.a 인데 hexa run hello rc=0 정상** → summer-로컬/일시적이지 hexa-lang 결함 아님. **즉 anima eval 은 aiden(clean pool)에서 지금 실행 가능.**
>
> **함의:** #42492878 = codegen 버그 아님. pool 전체 anima eval 차단도 거짓 — **aiden 에서 anima eval 가능** → ByteGPT G6 multiseed/clm303 G0-G6 엔진-네이티브 재채점이 codegen fix 없이 aiden 에서 진행 가능.
>
> ───────────────────────────────────────────────────────────
> (아래는 폐기된 원래 핸드오프 — 이력 보존용)

> 이 파일 전체를 새 세션/에이전트에 그대로 전달하면 된다. 대상 repo = **hexa-lang**(dancinlab, 쓰기권한 안 — upstream-fix 규칙: 떠넘기지 말고 그 세션에서 직접 고쳐 pr-cycle 까지).

---

## TASK

hexa-lang 의 **x86_64-linux C-codegen 버그**를 root-cause 까지 고쳐라. 이 버그가 pool 호스트(summer/aiden, x86_64-linux)에서 anima 엔진 컴파일을 통째로 막아, anima 의 self-hosted CI(무거운 macos/arm64 잡을 x86_64 self-host 로 못 보냄) + pool 전체 anima eval 을 차단하고 있다. arm64-darwin(맥)은 동일 소스가 **정상 컴파일**된다 = 아키텍처-게이트된 codegen 결함.

## 증상 (관측된 사실)

- 호스트: summer / aiden (둘 다 **x86_64-linux**), hexa **v0.315.0** (또는 그 이후 stable).
- 명령: anima 엔진 import-closure 컴파일 — 예:
  ```bash
  # anima repo 의 core/ + cli/ 를 x86_64 호스트로 rsync 후:
  hexa run cli/anima.hexa -- --help
  # 또는 엔진 closure 만:
  printf 'import "core/g6_ideation.hexa"\nimport "core/generator.hexa"\nfn main(){print("ok")}\n' > _c.hexa && hexa run _c.hexa
  ```
- 실패: 생성된 C 를 clang 이 컴파일할 때 **"undeclared function" 에러 ~6곳**. 첫 사이트 = `gen_auto_ideate`. 즉 transpiler 가 x86_64-linux 경로에서 **일부 hexa 함수의 C forward-declaration(프로토타입)을 방출하지 않아**, 정의보다 먼저 호출되는 지점에서 clang 이 미선언으로 거부.
- arm64-darwin(mini)에서는 **동일 소스가 깨끗이 컴파일** = 같은 함수에 프로토타입이 정상 방출됨.

## 의심되는 2차 결함 (확인 필요 — 같은 root 인지 별개인지)

ING / a2df 보고에 x86_64 에서 **`tag24 * tag24` 곱 / float-compare codegen 발산**(self-host byteeq 에서 gen3≠gen4 위험) 언급이 있음. **C-proto 미방출**(컴파일 자체 실패)과 **tag24/float 수치 발산**(컴파일은 되나 출력 다름)이 같은 x86_64 codegen 분기 결함인지, 별개 두 버그인지 먼저 격리하라. 우선순위 = 컴파일 차단(C-proto)부터, 그 다음 byteeq 발산.

## 접근 (reference-match — 정답지=arm64 경로)

1. **재현**: x86_64-linux pool 호스트(`sidecar pool on summer`/`aiden`)에서 위 명령으로 clang 에러 6곳 + 첫 미선언 심볼 캡처. (격리 worktree, 동시세션 브랜치변동 감지 시 STOP — 현재 다른 hexa-lang 세션 활동 여부 먼저 확인.)
2. **정답지 대조**: 같은 소스를 arm64 와 x86_64 양쪽에서 `--emit=c`(또는 transpile 산출 C) 덤프 → `gen_auto_ideate` 등 6 심볼의 **forward-declaration 방출 유무를 1:1 diff**. 첫 발산점(arm64 엔 proto 있고 x86_64 엔 없음)만 정렬.
3. **root-cause**: hexa-lang `self/` C-emitter 에서 프로토타입/forward-decl 방출 로직을 찾아(예: `self/runtime_core_emit.hexa` 또는 codegen 의 함수-선언 emit 패스), **아키텍처-게이트 분기**(x86_64 vs arm64 갈림)에서 proto 가 누락되는 조건을 격리. 증상이 아니라 그 누락 조건을 고친다(workaround/forward-decl 수동삽입 금지 — emitter 가 모든 타깃에 일관 방출하게).
4. **tag24/float**(2차): 확인되면 동일하게 arm64 정답지 대조로 x86_64 분기 수정.

## 검증 (verify-done — 출력으로, 자가판정 금지)

- ✅ x86_64-linux 에서 anima 엔진 import-closure + `cli/anima.hexa` 가 clang 에러 0 으로 컴파일.
- ✅ hexa-lang 자체 byteeq 게이트 GREEN (gen3≡gen4, 3-타깃) — 특히 x86_64 가 발산 안 함.
- ✅ 회귀 없음: arm64-darwin 도 여전히 컴파일 + byteeq GREEN (양 타깃 동시).
- ✅ (가능하면) anima `anima eval <golden.clm>` 가 x86_64 pool 에서 실행 도달.

## 완료 정의 (upstream-fix)

hexa-lang 격리 worktree 에서 고치고 → 그 repo 빌드·CI 로 검증 → **그 repo 에서 `sidecar pr-cycle` 머지까지 완료** → 새 stable 태그(release-tag-ci, autotag 가 feat/fix 면 자동). 그 후 anima 쪽 ING `#42492878` 을 resolved 로 닫고, anima 가 그 새 hexa 버전을 집도록 확인.

## 금지

- 로컬 wrapper/shadow/fork/monkey-patch 로 덮기 · anima-side 우회로 가리기.
- 수동 forward-decl 한 줄 끼워넣기(증상패치) — emitter 가 정석으로 모든 타깃에 방출하게 root-fix.
- 고쳤다며 hexa-lang 에 머지 안 하고 두기.
- 동시세션이 hexa-lang codegen 을 건드리는 중이면 STOP(브랜치 충돌).

## 컨텍스트 포인터

- anima ING `#42492878`: "hexa x86_64-linux 코드젠 버그 = pool 전체 anima eval 차단(gen_auto_ideate C-proto 미방출, clang undeclared 6 sites; summer+aiden hexa v0.315.0; mini arm64는 OK)".
- 이게 풀리면 동시 해소: anima self-host CI 무거운 잡(x86_64 self-host 가능) + pool 전체 anima eval(clm303/303M 엔진-네이티브 G0-G6 terminal) + ING `#42378065`/`#42492868` 의 GPU-검증 경로.
