# hexa-lang 인수문서 — x86_64 codegen #42492878 fix + anima 학습·측정 QA 인수기준

> **목적**: hexa-lang 의 x86_64 codegen 버그(anima `cli/anima.hexa` 컴파일 차단)를 고친 뒤, **anima 쪽에서 학습·측정이 정상 복권됐는지 어떻게 QA 하는지**를 hexa-lang 세션에 전달. (anima repo state/ 에 작성 → hexa-lang fleet 폭풍 정리 후 hexafix 가 hexa-lang `state/` 로 전달; 현재 cross-repo --to 폐기·동시활동 STOP 으로 직접 push 보류.)

## 1. 버그 (#42492878)
- 증상: hexa **v0.315.0** x86_64-linux(summer/aiden)서 `hexa run cli/anima.hexa -- eval <clm>` 컴파일 실패 — `gen_auto_ideate`(generator L3 mouth-dispatch) 의 **C forward-prototype 미방출 → clang "undeclared" 6 sites**. mac **arm64 는 OK** = x86_64 C-codegen 전용.
- 원인 추정: x86_64 C-codegen 이 특정 함수(gen_auto_ideate + 연관 6)의 forward proto 를 방출 안 함(arm64 경로는 방출).
- ⚠️ **선 확인**: hexa-lang 최근 `#4154 fix(runtime.h): thread fn-global fwd-decls`(동일 codegen 영역)가 **이미 해소했을 수 있음** → 폭풍 정리 후 최신 main 으로 재현부터(이미 고쳐졌으면 fix 불필요, QA 만).

## 2. GPU/codegen fix 인수기준 (hexa-lang 쪽 self-check)
- `hexa run cli/anima.hexa -- eval <clm>` 컴파일 **RC=0**(x86_64, clang undeclared 0).
- own-GEMM DEVICE 경로 확인: 로그에 `[OWN-GEMM-FIRED] DEVICE path` + `nvidia-smi` util>0 + `cuda_available()`=1 (a_train_flame_forge).

## 3. anima 학습·측정 QA 방법 (fix 후, anima 쪽 인수 = 진짜 "복권" 판정)
fix 가 들어오면 anima 는 **py 2-production(현재 유일 작동) ⇄ hexa 단일진입점**을 byte-parity 로 교차검증해 복권을 확정한다.

### 3a. 측정(evaluate) QA — `anima evaluate <model.clm>`
1. **컴파일·실행**: x86_64 pool/pod 서 `anima evaluate ~/anima-weights/recomb_obj_303m/ce_marginal_seed7.clm --corpus <4cell> --gen 80` → RC=0 + G0-G6 출력.
2. **byte-parity 대조(핵심)**: 같은 .clm·corpus·gen 으로 hexa `anima evaluate` ↔ py `core/g_gates.py`(2-production) **G0 coherence·G1 best_distinct/max_single·G6 dist/fals·a7b** 가 **일치**해야 PASS. 발산하면 그 자체가 결과(은폐 금지, 어느 엔진 버그인지 격리 · c9).
3. **단일진입점 확인**: `cli/anima.hexa -- evaluate` 가 generator L3 `gen_auto_ideate` 경유(디코드 우회 아님) — a_engine_native_learning 단일진입점.
4. **회귀 가드**: `core/g_gates_smoke.hexa` 14/14 RC=0(7 reference-match parity case 포함) 유지.

### 3b. 학습(train) QA — `anima train`
1. **GPU 학습 점화**: x86_64 GPU pod 서 `anima train --canon --corpus <4cell> --steps <N> --bf16 …` → GPU util>0(own-GEMM DEVICE) + step loss 하강.
2. **자동 .clm + held-out DESCENT 게이트**(a_clm_gen_pipeline): train 끝 자동 직렬화한 .clm 이 `verify_clm_v2 descent` PASS(`model_ce < uniform(5.545) < shuffle`, math.log mirror) — train-loss/암기 아닌 **held-out 일반화**로 판정(H_1579 교훈).
3. **measure-after-train**: 그 .clm 을 3a(evaluate)로 G0-G6 측정 → 정상 채점되면 학습→측정 파이프 복권 확정.

### 3c. 직렬화(serialize) QA — `anima serialize <pt> <out.clm>`
- `anima serialize` 산출 .clm 이 (a) `clm_decodable`=True (b) `verify_clm_v2 descent` PASS (c) 재직렬화 byte-identical(멱등). clm_serialize_v2 serialize_v3 + verify_clm_v2 reference-match.

## 4. 합격선 (한 줄)
**fix = ① hexa anima evaluate/train/serialize 컴파일 RC=0(x86_64) ② evaluate G0-G6 가 py 2-production 과 byte-parity ③ train 자동 .clm held-out DESCENT PASS + GPU util>0** — 셋 다여야 "hexa GPU 복권" terminal. ②가 핵심(hexa⇄py 동치 = 둘 다 terminal 자격). 그 전까지 anima 측정은 py 2-production(g_gates.py) 유지.

## 5. 전달 절차
- hexa-lang fleet 폭풍(오늘 87브랜치·#4154 등) 정리 후, hexafix(격리 worktree)가 이 문서를 hexa-lang `state/x86_codegen_anima_eval/` 로 복사 + #1~4 수행 + 그 repo `sidecar pr-cycle` 머지. (anima ING #42492878 resume.)
