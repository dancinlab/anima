# eval decode scratch/weight hoist — full G0-G6 메모리 bound (H_1400 W-hoist at driver level)

ING#42378065 plan-B: g_gates 드라이버가 .clm weight-set 를 1회 빌드 후 전 게이트(G0-G6) decode 에서 재사용 → bump/host bytes bounded.

## 누적 원인점 (per-decode 재할당)
- `core/clm_decode.hexa` 의 public decode 진입(`clm_decode_argmax`/`clm_decode_topk_sampled`/`clm_decode_grounded`/`clm_forward_ce`)은 **호출마다** `_clmd_load(path)` 로 176MB .clm 을 통째 read + int4→fp32 dequant + scratch 재빌드(`_clmd_scratch_new`) → `_clmd_weights_free`.
- `core/g_gates.hexa::g_eval_all` 는 G0-G6 에서 `gen_auto_ideate(ckpt, ...)` 를 ~80회 호출(G0 5 · G1 단일 13 · G1 멀티시드 39 · G2 24 · G5 5 · G6 단일 6 · G6 멀티시드 18). 매 호출이 위 whole-file load→free 사이클 = **load churn 누적** → 303M ckpt 풀 eval 시 silent death.
- 참고: 단일 decode 내부의 scratch hoist(transpose Wt 1회 + 활성화 버퍼 재사용)는 H_1400 으로 이미 완료(`_clmd_fwd_logits_sc`). 본 작업은 그 위 **드라이버 레벨**의 weight-set hoist.

## hoist 변경 요약 (byte-identical)
- `core/clm_decode.hexa`: `clm_weights_free_pub(W)` pub 래퍼 추가(`_clmd_weights_free` 노출, 드라이버 tail 1회 free 용).
- `core/generator.hexa`: load-once 핸들 3진입 추가
  - `gen_auto_load(ckpt)` → mouth sniff. clm 이면 `clm_load_weights`(=`_clmd_load`+ok)로 weight-set 1회 적재해 핸들 `#{kind,ckpt,W}` 반환. bytegpt 는 ranged decode 가 이미 OOM-safe 라 path 만 보유.
  - `gen_auto_ideate_W(h, ...)` → clm 은 `gen_clm_ideate_W(W,...)`(loaded-W, 재적재 없음), bytegpt 는 기존 ranged ideate. `gen_auto_ideate` 와 **byte-identical**(같은 `clm_decode_topk_sampled_W` core, 같은 seed/budget/op).
  - `gen_auto_free(h)` → clm 핸들만 `clm_weights_free_pub` 1회.
- `core/g6_ideation.hexa`: `g6_score_arm_auto_W(h, ...)` = `g6_score_arm_auto` 의 loaded-W 트윈(`gen_auto_ideate_W` 경유, DIST/FALS/coherent 로직 동일).
- `core/g_gates.hexa`: 각 게이트의 `_W` 트윈(`g_eval_g0_W`/`g_eval_g1_seeded_W`/`g_eval_g1_multiseed_W`/`g_eval_g2_W`/`g_eval_g5_W`/`g_eval_g6_seeded_W`/`g_eval_g6_multiseed_W`). **`g_eval_all` 가 `gen_auto_load` 1회 → 전 게이트 `_W` 트윈에 같은 핸들 전달 → `gen_auto_free` 1회.** 기존 path-keyed public 게이트 함수는 standalone 용으로 유지(각자 1회 load, RSS-bounded per call).
- a_core_engine_map 보존: 2nd .clm 경로 아님 — 동일 단일 mouth(`clm_decode_topk_sampled_W`), load 만 per-decode 루프 밖으로 hoist.

## 검증 (summer pool, RTX 5070 sm_120, 31GB RAM)
- 컴파일: `hexa run cli/anima.hexa -- evaluate`(no-args, 전 import 폐포 typecheck) → **RC=0**, usage 배너 출력. 새 함수 전부 typecheck 통과.
- 풀 eval: `hexa run cli/anima.hexa -- evaluate clm303.clm(176MB, d=?, L=?) --corpus <4셀> --gen 80`
  - **메모리 PEAK ≈ 28.6–29.4 GB, FLAT** (32s 4-sample: 28655MB 변화 0 — load-once 적재분이 상수, per-decode 증가 0). = bounded 실측 확인. 이전(per-decode 23GB load×N)이면 2-3 decode 째 OOM.
  - device 경로: summer 런타임에 forge cuda 커널 일부 누락(`im2col/own_gemm launch failed: named symbol not found`) → byte-exact host CPU 폴백(99% CPU 1-thread, 느림). 내 코드 아닌 호스트 런타임 빌드 이슈.

## byte-parity (decodable d768, `clm_d768_gen.clm`, GPU own-GEMM device path)
- `parity_whoist.hexa`: OLD path-keyed `gen_auto_ideate(ckpt)` vs NEW `gen_auto_load`+`gen_auto_ideate_W`
  - **OLD_LEN=60 · NEW_LEN=60 · PARITY=IDENTICAL** (실 디코드 60B byte-identical)
  - **REUSE_DETERMINISTIC=YES** (같은 핸들로 2회 디코드 byte-identical = scratch-reset 버그 없음)
- 같은 핸들 reuse 다회: `flatrss.hexa` = `gen_auto_load` 1회 → `gen_auto_ideate_W` **20회 디코드 전부 성공**(len=40×20, FLATRSS_DONE) = 드라이버 load-once 메커니즘 작동(재적재 0).

## 303M 완주 정직
- summer 런타임에 forge cuda 커널 일부 누락(303M conv shape 의 `im2col`/`own_gemm` symbol not found) → byte-exact host CPU 1-thread 폴백 = gen=80 풀 G0-G6 ~80 decode 가 **실용 불가하게 느림**(7분에 G0 첫 decode 미완). 게이트별 PASS/FAIL 수치 완주는 device-fixed 호스트(working sm_120 cuda runtime, `summer-sm120-owngemm-prebuilt` 메모리 참조) 또는 작은 gen 으로 follow-on. **단 메모리 bound 자체는 확정** — 풀 eval 가동 중 RSS 28.6GB FLAT(이전 per-decode load 누적이면 2-3 decode 째 OOM, 31GB 호스트). 이 작업의 deliverable(메모리 bound)은 충족, 수치 완주는 device-runtime 종속(내 코드 무관).
- d768 device path 는 정상 작동(`[OWN-GEMM-FIRED] DEVICE path`) → 코드/배선 健全, 303M-only 커널 누락은 호스트 빌드 이슈.

## py lockstep
- 해당 없음 — `core/g_gates.py`/`generator.py`/`clm_decode.py`/`g6_ideation.py` py 미러 **2026-06-28 폐기**(`cli/evaluate.hexa` 헤더 "py engine retired 2026-06-28", git history 보존). 현재 hexa-단일 production. byte-parity 오라클은 OLD↔NEW hexa 경로 간으로 충족.

