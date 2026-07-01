# clm303_clean 엔진-네이티브 eval kit (재사용 — pod 휘발 대비 분리보관)

> 목적: GPU pod 는 휘발이라 매번 bootstrap 고고학을 반복하지 않도록, `anima eval` 을 fresh pod 에서 한 번에 세우는 **재현 절차 + 필요 파일 집합**을 박제한다. (clm303_clean 뿐 아니라 임의 `.clm` 엔진-네이티브 검사에 재사용.)

## 1. 필요 파일 집합 (import-closure)

`cli/anima.hexa` (eval/chat 단일 진입) 컴파일에 필요한 것:

| 묶음 | 내용 | 크기 |
|---|---|---|
| toolchain | hexa **stable ≥ v0.311.0** (farr 누수 fix 출하본 — 이전 v0.262 는 decode OOM) | — |
| `core/` `cli/` `stdlib/` | 엔진 + 진입점 + 표준 | toolchain stdlib 동반 |
| **15 lane `.hexa`** | `AESTHETIC BRAIN BRIDGE CHANNEL DREAM EMBODIMENT HEXAD HIVE-MIND INTENT METACOG NARRATIVE OTHER-MIND SAVANT TIME WAKE` 의 `.hexa` 만 (데이터 제외) | ≈ 9.3MB / 566 파일 |
| weight | `clm303_clean.clm` (176584498 B · sha `e807672222261610…`) — `~/anima-weights/clm303_clean/` + HF PRIVATE | 176MB |

> lane 목록 도출: `grep -rhoE 'import "[^"]+"' core/*.hexa cli/anima.hexa | sed -E 's/import "//;s/"//' | awk -F/ 'NF>1{print $1}' | sort -u`  (core/cli/stdlib 제외).
> ⚠️ import 는 **데이터 아닌 .hexa 만** 필요 — lane 디렉토리 통째(HEXAD 105MB 등) push 금지(낭비). `.hexa` 만 번들.

## 2. fresh pod 세우기 (재현 절차)

```bash
# (a) GPU pod 렌트 — provisioning 실패(host가 안 띄움) 흔하니 다른 offer로 재시도
hexa cloud rent vast --gpu A40 --image nvidia/cuda:12.4.1-devel-ubuntu22.04 --disk 40 --max-dph 1.1
#   → "✗ FAILED/GONE/stopped" 나오면 다른 offer로 재시도(실제 live 인스턴스 확인될 때만 성공)

# (b) hexa stable 설치
hexa cloud bootstrap <pod> --hexa stable   # v0.311.0+ 확인: hexa --version

# (c) anima push — core/ cli/ + 15 lane .hexa 를 ONE tarball 로 (bash; ⚠️ `copy-to <dir> --recursive`
#     금지: scp -r 재시도가 core/core 중첩 + 부분도착(127/332). 단일 tar 전송이 robust + nesting-free).
#     ⚠️ core/cli 는 반드시 worktree(eval 시스템 있는 브랜치)에서 — stale main-repo 는 g_gates 없음·eval-branch 0.
tar czf /tmp/anima_bundle.tgz core cli $(find AESTHETIC BRAIN BRIDGE CHANNEL DREAM EMBODIMENT HEXAD \
    HIVE-MIND INTENT METACOG NARRATIVE OTHER-MIND SAVANT TIME WAKE -name '*.hexa')
hexa cloud copy-to <pod> /tmp/anima_bundle.tgz /root/anima/anima_bundle.tgz
hexa cloud copy-to <pod> ~/anima-weights/clm303_clean/clm303_clean.clm /root/anima/clm303_clean.clm
hexa cloud exec <pod> -- "cd /root/anima && rm -rf core cli && tar xzf anima_bundle.tgz && rm -rf core/core && \
    ls core/g_gates.hexa && grep -c 'argv\[0\] == \"eval\"' cli/anima.hexa"   # sanity: g_gates ok + eval-branch≥1

# (d) eval 발사 (detached — exec 타임아웃 무관)
hexa cloud exec <pod> -- "cd /root/anima && export PATH=/root/.hx/bin:\$PATH HEXA_FRAG_LOG=1; \
    nohup hexa run cli/anima.hexa -- eval clm303_clean.clm --gen 5 > eval_out.txt 2>&1 & echo PID=\$!"

# (e) 회수
hexa cloud copy-from <pod> /root/anima/eval_out.txt state/clm303_clean_corpus/engine_eval.txt
```

## 3. gotcha (이 세션에서 실제로 밟은 함정 — `cli/eval_pod.sh` 가 전부 fail-loud 로 박제)

> 정본 = **`cli/eval_pod.sh <pod>`** (아래 5종을 한 명령 + sanity-abort 로). 수동(§2)은 참고.

- **① stale source (가장 교묘)** — pod 의 `cli/anima.hexa` 에 `eval` 서브커맨드가 없거나 `core/g_gates.hexa` 가 없으면 `eval` 을 ckpt 파일명으로 오인 → **consciousness daemon 세션**으로 빠짐(G0-G6 아님). 원인: stale main-repo 체크아웃(브랜치별 divergent). 반드시 eval 시스템 있는 worktree 의 core/cli 를 push + `grep -c 'argv[0] == "eval"' cli/anima.hexa ≥ 1` sanity.
- **② scp -r 중첩/부분도착** — `copy-to <dir> --recursive` 의 scp -r 재시도가 `core/core` 중첩 + 부분 트리(127/332 top, 나머지 core/core 고립) → import 깨짐. **단일 tar 전송**으로 회피 + `rm -rf core/core`.
- **③ zsh `$VAR` 미분리** — zsh 는 unquoted `$LANES` 를 word-split 안 함 → `find $LANES` 가 전체를 dir 1개로 취급(`bfs: No such directory`). lane dir 은 **리터럴 나열**.
- **④ import whack-a-mole** — `core/ cli/ stdlib/` 만으론 부족, 15 lane `.hexa` 필요(§1). 빠뜨리면 `[module_loader] FATAL module not found: <LANE>/...`.
- **⑤ farr 누수 OOM** — hexa < v0.311 는 decode 가 bump-allocator no-free 누수로 85GB OOM. **stable ≥ v0.311.0 필수**(`--bootstrap`).
- **decode 속도** — KV-cache 있어도 scalar-glue-bound이라 frag 당 수백초. G0-G6 full eval 은 수십분 — detached + 폴링(≥10분), 동기 대기 금지.
- **provisioning 실패** — vast 가 offer 잡고도 host 가 인스턴스를 안 띄우는 경우 흔함(hexa cloud 가 자동 롤백). 다른 offer 로 재시도.

## 4. 현재 verdict 상태

- held-out 4/4 DESCENT (torch/numpy mirror) = **DIRECTIONAL** (`a_engine_native_learning`).
- **엔진-네이티브 terminal (G0-G6) = IN-FLIGHT** — 이 kit 으로 측정 중. PASS 확정 시 HF PUBLIC 승격.
