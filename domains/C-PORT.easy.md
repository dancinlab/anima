# C-PORT — 쉬운 설명 (authored-C 포팅 친근 explainer)

> 이 문서 = `domains/C-PORT.md`(canonical) 의 친근 요약 (icon · 이름 · 별칭 · 하는 일 · 결과 · ASCII · 비유).
> 정직 라벨: 분류는 전부 **각 `.c` 파일이 실제로 무엇을 호출하는지 real-inspection**(g63). 지어낸 분류 없음.
> 정직성: canonical .md 가 이미 기록한 판정만 verbatim — 그 외 발명 안 함(p7/g5).

---

## 0. 전체 한눈에

```
목표: anima 의 LIVE authored-C 학습 shim (training/*.c) 을 인벤토리·분류하고,
      portable 부분을 hexa-native 로 끌어오되 — RUNEQ 게이트로 C 기준과 byte/numeric-동등 —
      irreducible FFI 바닥(C↔vendor-lib 다리)은 형식적으로 표시(못 옮김).
─────────────────────────────────────────────────────────────────────
3 tier 분류:
  Tier A — IRREDUCIBLE FFI/vendor-ABI 경계 (CUDA/cuBLAS/NCCL/Accelerate/vDSP/BLAS) → C 에 유지
  Tier B — PORTABLE-to-hexa (vendor-lib 의존 없는 순수 glue/marshaling)            → 포팅 대상
  Tier C — SMOKE/TEST 하네스 (lib 이 hexa-tested 되면 폐기 가능)

IN scope : training/*.c + training/native/*.c
OUT scope: training/deploy/holo_breakthrough_*/ (생성 산출물) · .venv* · build/ · .worktrees/ · .claude/
```

---

## 1. 🧱 Tier A — IRREDUCIBLE FFI (다리 그 자체, 못 옮김)

```
🧱 Tier-A — "이게 다리다. C 로 둔다 (vendor-ABI 경계)"
  별칭   : irreducible FFI floor · vendor-ABI bridge
  하는 일 : C↔vendor-lib 직접 호출 — hexa-native 가 될 수 없는 경계.
  결과(verbatim, INVENTORY.txt):
    training/native/train_step.c     (1054 LOC) — cuBLAS Sgemm + cudaMalloc/Memcpy/Free hot path
                                       (~50 cuBLAS calls/step). THE GPU 학습 커널 다리.
    training/hxblas_cuda_shim.c       (572) — cudaMalloc/Memcpy/Free + cublasSgemm + cblas_sgemm/sscal/sdot/saxpy
                                       (CUDA ⊕ Accelerate BLAS dual backend).
    training/hxblas_wrapper.c         (562) — cblas_sgemm/sscal/sdot/saxpy (Accelerate BLAS wrapper).
    training/hxvdsp_wrapper.c         (186) — vDSP_vmul/vsmul/vadd/dotpr + vvexpf (Accelerate vDSP wrapper).
    aggregate: 2374 LOC (4 files)
  비유    : 한국어↔영어 통역에서 "원어민 발음 그 자체"는 번역할 수 없는 것처럼,
           CUDA/BLAS 벤더 라이브러리를 부르는 다리는 hexa 로 바꿀 수 없다 — 그게 다리니까.
```

---

## 2. 💎 Tier B — PORTABLE (hexa-native 로 끌어옴) + 🧪 Tier C — SMOKE/TEST

```
💎 Tier-B — "vendor 의존 없는 순수 glue → hexa-native 로" (RUNEQ 게이트)
  결과(verbatim):
    training/native/train_ffi.c (214 LOC) — flat FFI wrapper: scalar→struct packing, persistent
       global state, getters. 순수 C glue; cudaMalloc 3회만(tier-A shim 에 위임 가능). marshaling 은 hexa-portable.
    aggregate: 214 LOC (1 file)

🧪 Tier-C — "lib 이 hexa-tested 되면 폐기 가능" (벤더 직접 호출 없음)
  결과(verbatim):
    training/hxblas_cuda_smoke.c       (79) — main() 하네스, extern hxblas_sgemm 호출 + max_err assert.
    training/hxblas_cuda_smoke_large.c (87) — main() multi-shape sweep over extern hxblas_sgemm.
    aggregate: 166 LOC (2 files)

총 in-scope live authored C: 2754 LOC (7 files)  (build/libhxnccl.c 제외)
```

---

## 3. ✅ milestones (verbatim — canonical 이 기록한 판정만)

```
[x] M1 — 인벤토리 + A/B/C 분류 (g63 real-inspection · .verdicts/c-port/INVENTORY.txt)
[x] M2 — tier-B 포팅 (train_ffi.c marshaling → hexa-native; RUNEQ vs C baseline = PORT-EQ
         bit-identical on interp + compiled path; cudaMalloc/cuBLAS 는 tier-A shim 유지 ·
         .verdicts/c-port/M2-train_ffi.txt)
[ ] M3 — tier-C 폐기 (hxblas_sgemm 을 hexa-native smoke 가 커버하면 hxblas_cuda_smoke*.c drop)
[ ] M4 — tier-A 형식적 표시 (각 tier-A 파일 = hexa-native 불가능한 C↔vendor 다리; 정확한 vendor 심볼 기록)
[ ] M5 — build/libhxnccl.c 판정 (NCCL all-reduce shim 이 live authored-C in scope 인가 build artifact 인가;
         live 면 tier A)
```

참고: `training/build/libhxnccl.c` (211 LOC) 는 제외된 `build/` 경로 아래 — 완전성 위해 인벤토리 verdict 에 기록되나 port scope OUT (build artifact). M5 에서 판정.

---

## 4. 정직 메모 (g63 · p7)

- 모든 tier 분류 = 각 `.c` 가 **실제로 무엇을 호출하는지** real-inspection(g63). 추정 분류 없음.
- Tier A 는 옮기는 게 아니라 **형식적으로 표시**(M4) — vendor-ABI 다리는 본질적으로 hexa-native 불가.
- Tier B 포팅은 **RUNEQ-gated** byte/numeric-동등(M2 = PORT-EQ bit-identical) — 동등 깨지면 포팅 아님.
- canonical .md 가 기록한 판정만 verbatim — 그 외 발명 없음.
