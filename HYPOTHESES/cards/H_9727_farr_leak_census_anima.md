# H_9727 — anima farr_* 핸들 누수(HX3061) census: 계기검증된 0

- **id**: H_9727
- **group**: hexa-lang-model-conformance
- **date**: 2026-07-17
- **tier**: 🟢 GREEN-MEASURED (계기 GATE-D 검증 · 전수 · 타임아웃 0) — anima 프로덕션 corpus 한정
- **status**: MEASURED
- **surfaces**: 이 카드 + `HYPOTHESES.jsonl`

## 주장 (사전등록 형태)

commons `hexa-lang-model` 규칙은 소비 레포에 "`farr_*` device 핸들은 반드시 `farr_free` 로 해제"를 요구한다.
**주장**: anima 프로덕션(`core/`·`cli/`·`agent/`)에 미해제 `farr_*` 핸들 누수가 존재하지 않는다.

## 계기 (engine-native · SSOT 하네스)

- hexa-lang HX3061 census 하네스(레포의 `hexa-own` 하네스) — **from-source `aprime_cc`**(`tool/build_aprime.sh`) + `--emit=asm`.
- lane 발화 지점 = `hir_to_mir` **LOWERING** 패스(`hir_to_mir.hexa:9823` `HEXA_BORROWCK_LEAK`).
- 호스트: aiden(x86_64 linux · 12c · clang) — **mini 금지**(heavy from-source 빌드 · `heavy-anima-eval-pool-not-mini`).
- REF = hexa-lang `origin/main` 679cc9372 · corpus = anima `origin/main` 0cde4f48 신선 클론(`~/anima_census`, 병렬 세션의 `~/anima` 스냅샷 미사용).

## 🧪 GATE-D — 계기 생사 증명 (이 결과의 자격 요건)

| 픽스처 | 기대 | 실측 | 판정 |
|---|---|---|---|
| `leak_simple` (누수 있음) | ≥1 | **2** | ✅ 발화 |
| `leak_conditional` (누수 있음) | ≥1 | **2** | ✅ 발화 |
| `clean_freed` (누수 없음) | 0 | **0** | ✅ 침묵 |
| `clean_returned` (누수 없음) | 0 | **0** | ✅ 침묵 |

⟹ **GATE-D PASS — instrument validated.** 계기가 누수 있는/없는 코드를 구별함이 먼저 증명된 뒤 나온 결과다.

## 결과

| 항목 | 값 |
|---|---|
| CORPUS_FILES (producer 보유) | **9** |
| HX3061_TOTAL_FIRES | **0** |
| HX3061_DISTINCT_FILES | **0** |
| TRIAGE_REAL_LEAK_CAND | **0** |
| TRIAGE_FP_ESCAPE | **0** |
| **TIMEOUT** | **0** (9/9 완주 · DONE 정상 도달) |

측정 대상 9파일: `core/decode.hexa`(producer 최다) · `core/DECODER/flame_mm.hexa` · `core/mitosis_hook_lib.hexa` ·
`core/bytegpt_{devres,kvcache_batch,kvcache_bench,kvcache}_smoke.hexa` · `core/verify303m_mount_{full,parity}.hexa`.

**커버리지 논증**: HX3061 의무는 **producer 호출에서 태어난다**(생산자 테이블 = `farr_zeros`/`farr_copy`/`farr_int_zeros`/`farr_int_copy`/`farr32_zeros` · `hir_to_mir.hexa:903`).
producer 0 파일은 핸들을 만들 수 없어 구조적으로 누수 불가 ⟹ 프로덕션 480 중 **471 은 계기 없이 종결**, 나머지 9 를 전수 측정.

## 판정

🟢 **anima 프로덕션에 farr 핸들 누수 없음 — 계기검증된 0.**
FP-escape 0 이므로 R3~R6 escape-widening(#4984·#4989·#4991·#4992)이 anima corpus 에서 잔여 오탐 0 을 달성했다(upstream flip gate 에 유리한 데이터포인트지만 flip 판단은 hexa-lang 소관).

## 정직한 범위 (`a_scale_honest_scope`)

- 범위 = anima `core`+`cli`+`agent` producer-bearing 9파일 · x86_64-linux · 이 커밋 시점. `archive/` 미포함.
- HX3061 은 **핸들 누수** lane 이다. UAF/double-free 는 별도 HX3060 lane 이며 **이 측정에 없다**.
- `alloc_raw` raw malloc lane 은 **어떤 계기도 추적하지 않는다**(생산자 테이블 밖) — 이 0 에 포함되지 않는다. 수동 감사만 존재.
- lane 은 여전히 opt-in(default-OFF). 이 결과가 default-ON flip 을 주장하지 않는다.

## 🕳️ 이 측정에서 배운 것 (계기 함정 2건)

1. **`hexa typecheck` 로는 HX3061 이 절대 안 잡힌다** — lane 은 lowering 발화인데 typecheck 는 "diagnostics only, **no codegen**".
   앞서 typecheck 로 얻은 "누수 0" 은 양성통제 **0/1** = INSTRUMENT-DEAD 였다(누수 있는 픽스처도 0 을 냄). 그 0 을 정합으로 읽을 뻔했다.
2. **`TARGET` 을 export 하면 빌드가 조용히 깨진다** — 하네스는 `TARGET` 을 export 하지 않고(평범한 대입) `aprime_cc --emit=asm --target=` 에만 쓴다.
   `env TARGET=x86_64-linux-gnu` 로 강제 export 하면 `build_aprime` → `stage_resolve_runtime_a` → `resolve_native_*_seed` 의 case 가
   **슬러그 형식(`linux-x86_64`)만 인식**해 트리플을 못 알아듣고 `seed=""` 로 **무음 스킵** → `rt_*_native` undefined 링크 실패(4000줄 뒤에 터짐).
   export 를 빼면 uname 폴백이 `linux-x86_64` 를 잡아 seed 조립(array 6심볼·map 4심볼) → 빌드 통과.
   ⚠️ 이건 **내 호출 실수**이지 upstream 회귀가 아니다(CI 가 ubuntu x86_64 에서 `build_aprime` GREEN). 다만 **무음 폴백**은 upstream 견고성 개선 여지(별건).

## 링크

- 상위 축: commons `hexa-lang-model` 정합 감사 — arena-escape 축은 anima #3917(수리) → #3931(전제 오류 정정) → hexa-lang #4997(문서 근본원인).
- 이 카드로 정합 감사 **4축이 전부 닫혔다**: `@own` 0 · 수동free 0 · arena-escape 0(구조논증) · **farr 누수 0(계기검증)**.
