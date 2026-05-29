# M5 H_686+H_687 prodaux PRODUCTION fire — 🟠 BUILD-BLOCKER (build chain incomplete)

**날짜**: 2026-05-29
**대상**: PR #1397 머지된 `CORE/DECODER/train_v3_moe_prodaux.hexa` (1037 LoC, λ_ent=0.1, λ_kl=0.1, BC-ANIMA M4 wired CE 경로)
**pod**: `83na0mvuq4tqao` H100 80GB HBM3 @ 213.181.105.248:13119 · owner `m5-prodaux-fire-2026-05-29`
**wall**: ~1.5h SSH-ready → 빌드 시도 → teardown · **cost ≈ $5** (over budget, all in build attempts — zero step runs, zero decode samples)

## verdict

🟠 **BUILD-BLOCKER** — production trainer 가 현재 Linux/x86_64 codegen 체인에서 컴파일되지 않는다. 이 round 는 **연구결과 0, 빌드 차단지 4개 (cumulative)**.

이는 H_686+H_687 가설에 대한 verdict 가 아니다. 가설은 **무측정** (untested at production scale). λ=0.1 aux-loss 가 register collapse 를 깨는지는 여전히 OPEN.

## 차단지 enumeration (4개)

### #1 `farr_softmax_rows` undefined (BC-ANIMA M4 wiring gap)
`train_v3_moe_prodaux.hexa:554` 에서 `farr_softmax_rows(logits_g, softmax_buf, 1, V)` 호출. hexa-lang runtime 에는 `farr_softmax_rows_gpu(x, R, C) → new_id` (3-arg, returns new array) 만 존재 — 4-arg in-place variant 가 registered HexaVal handle 로 노출되지 않음.

codegen2 는 이를 `hexa_call4(farr_softmax_rows, …)` 로 emit 하는데, `farr_softmax_rows` 라는 글로벌 HexaVal 심볼이 없어 undefined identifier 에러.

수정 시도: 로컬 C shim `trainer_fixups.h` 작성 (in-place CPU 구현) + trainer.c sed-patch (`hexa_call4(farr_softmax_rows,` → `farr_softmax_rows(`). 이 시점에 trainer.o 컴파일은 성공.

### #2 `farr_ce_seed` undefined (동일 wiring gap)
동일 패턴. runtime 에는 `farr_ce_seed_gpu(logits, target_ids, R, V, out_loss, out_dlogits)` (6-arg) 만 존재. .hexa 소스는 `farr_ce_seed(softmax_buf, target_buf, d_logits, 1, V)` (5-arg, sm-기반) 호출.

수정 시도: `trainer_fixups.h` 에 5-arg CPU shim 추가 (sm-onehot). bare-name 호출이라 sed 없이 shim 직접 매칭.

### #3 `farr_adamw_step_inplace` undefined (in-place adamw missing)
runtime 에는 `adamw_step(p, g, m, v, n, lr, b1, b2, eps, wd, t)` (10-arg, returns new W array) 만 존재. .hexa 소스는 `farr_adamw_step_inplace(M, m_buf, v_buf, dMg, m_size, lr, …, step)` (11-arg, in-place into W).

수정 시도: `trainer_fixups.h` 에 11-arg in-place CPU shim 추가. trainer.o 컴파일 성공.

### #4 (블로킹) Cross-module 코드젠 미연결 — `mm_transpose` / `mm_scatter_add` / `mm_extract` 등 v3_moe_bwd_lib 내부 호출이 module C 산출물에서 undeclared

각 `use` 모듈을 `hexat_linux` 로 별도 compile 했을 때 (`mod_tensor_lib.c`, `mod_flame_mm.c`, `mod_v3_moe_arch.c`, `mod_v3_moe_bwd_lib.c`, ...) 동일 codegen 이 cross-module 호출에 extern 도 emit 안 함:

```
mod_v3_moe_bwd_lib.c:126:31: error: use of undeclared identifier 'mm_transpose'
mod_v3_moe_bwd_lib.c:128:16: error: use of undeclared identifier 'mm_scatter_add'
mod_v3_moe_bwd_lib.c:131:36: error: use of undeclared identifier 'mm_extract'
mod_v3_moe_arch.c:88:13: error: initializing 'HexaVal' with an expression of incompatible type 'int'
...20+ errors
```

이는 **hexa-lang codegen2 의 module-별 컴파일 모드 미지원** — 각 .hexa 파일을 단독 compile 하면 cross-module 호출이 extern 으로 떨어지지 않아 깨짐. 그러나 main 파일만 compile 하면 module 본체 정의도 떨어지지 않아 link 에서 undefined.

원래 `hexa build` (Mac 전용 native binary build) 가 module 들을 한 TU 로 inline 하는 듯 — Linux 측에는 그 단계가 없다 (`hexat_linux` = codegen-only).

이 차단지는 anima 측에서 patch 불가. **hexa-lang inbox 등록 대상**.

## 메모리 alignment

이 사례는 다음 알려진 lesson 들과 일관 (악화 없음, 새 사실 1개):

- `flame_bpe_corpus_lib stale install` (memory 2026-05-27) — Mac/Linux toolchain 비대칭. Mac install 에서는 동작하나 Linux 빌드 체인 미동기화.
- `hexa cross-backend codegen gap` (memory 2026-05-27) — `arm64_darwin` vs `gen2` C builtin 테이블 별도. Mac compile≠Linux hexa run.
- **새 사실**: 단일 file → C 변환 (`hexat_linux file.hexa file.c`) 만으로는 `use` 모듈 본체가 emit 되지 않음. Linux 측 `hexa build` 대체경로가 존재하지 않으면 cross-module link 가능한 trainer 는 빌드 불가.

## 권장 다음 한 수

1. **hexa-lang 인박스 신규 entry**: "Linux codegen module-aware build mode" — `hexat_linux --modules <main>.hexa <out>.c` 가 use 그래프 traverse 해서 single-TU emit (Mac `hexa build` 등가) 하도록.
2. **단기 우회**: PR #1397 trainer 를 single-file 로 collapse (모든 use 본체를 한 .hexa 파일에 inline) — 빌드는 통과하지만 SSOT 가 깨진다 (a_completeness_over_cheap 위배).
3. **올바른 fix path**: hexa-lang #1527 cross-backend codegen 후속 round 로 cross-module dispatch 보강. anima 측이 아닌 hexa-lang 측 작업.

## 자원 & 정직성

- pod teardown: 완료 (`hexa cloud down 83na0mvuq4tqao` → terminated · `hexa cloud list --provider runpod` → 0 pods)
- HF upload: 없음 (artifact 0, ckpt 0)
- 연구 결과: 0 (production-scale H_686+H_687 verdict 미생산)
- 빌드 차단지: 4 개 식별, 3 개 patched (trainer_fixups.h), 1 개 (cross-module link) anima 측 unfixable

이 라운드는 비용은 발생했으나 verdict 는 만들지 못했다. `top_id=0 × 100` 같은 falsified 결과도 아니고 escape 도 아니고 — **measurement 불가** 가 정확한 상태. 가설 H_686+H_687 은 production scale 에서 측정되지 않았다.

honest verdict: 🟠 **무측정 (untested at production)** — H_686+H_687 가설 자체에는 evidence 0. λ=0.1 에서 escape 여부는 여전히 OPEN.
