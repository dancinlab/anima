# G6-bind 게이트 — engine-native 재채점 + terminal 평가 (H_6186)

임무: DIRECTIONAL(py byte-parity) G6-bind 게이트를 CORE `.hexa` byte-exact 재채점으로 terminal 승격.

## 결과 요약
| 축 | 상태 |
|---|---|
| bind-게이트 로직(scoring) | 🟢 ENGINE-NATIVE CONFIRMED — hexa CORE 채점 ≡ py-mirror, 9/9 셀 정확 일치 |
| fragment DECODE | 🟠 STILL DIRECTIONAL / BLOCKED-INFRA — engine-native 재디코드 이 세션 불가 |
| terminal 승격 | ❌ 부분 close only (WIRED-live 유지 + gate-logic engine-native 확인, decode 축 미완) |

## (b) engine-native 3-arm 재채점 (fals / fals_bound)
core/g6_ideation.hexa(origin/main @07f79a0b) 채점 fn VERBATIM 추출
(_g6_is_falsifiable FROZEN + _g6_topic_bound + _g6_is_falsifiable_topic_bound)를
hexa v0.574.1 로 컴파일·실행. py/numpy/torch 0, 모델 디코드 없음(순수 게이트 로직).

    arm       seeds(7,4302,4303)   fals      fals_bound
    BASE                           0,0,0     0,0,0
    TARGETED                       6,6,6     5,6,6
    SHUF                           6,6,6     1,0,0

원본 = engine_native_scoring.txt (hexa stdout RC=0) · 채점기 = g6score_engine_native.hexa

## (c) form-priming 차단 + byte-parity
- form-priming 차단 유지: TARGETED mean fals_bound 5.667 ≫ SHUF 0.333.
  SHUF 는 frozen fals 6/6(형태 암기)이나 bind 항이 fals_bound 를 {1,0,0} 붕괴 → 차단.
- byte-parity: hexa CORE 채점이 py-mirror rescore.json(fals_frozen AND fals_bound)를
  9/9 셀 정확 재현(mismatch=0). 대조표 = terminal_verdict.json.
- origin/main H_6186 WIRED-live bind-게이트 코드가 컴파일·실행되어 기대 fals_bound 를
  정확히 산출 = 배선 정합성 engine-native 확인.

## (d) terminal 승격 판정 — 부분 close
- gate-logic 축: 🟢 engine-native CONFIRMED.
- decode 축: 🟠 여전히 DIRECTIONAL. 54 fragment 는 summer py numpy
  bytegpt_decode_topk_sampled_W(session-eval-py-only) 디코드. CORE .hexa A⇄G 재디코드
  이 세션 실행 불가:
  - summer: load avg 21(17 users), hexad --version 무응답(RC=124), nvidia-smi hang = 포화.
  - aiden: 30GB 중 21GB 사용·여분 0, 타 에이전트 heavy hexa D<잡 2개 + earlyoom --prefer hexa
    → 내 303M 디코드 compile/run 2회 OOM-kill(0바이트 out/err).
- a_break_the_wall: 인프라 벽(type-c) = c1-fix 대상이지 과학 천장 아님. tune-to-green 없음.
- 판정: full terminal 승격 보류. H_6186 wired: WIRED-live 유지 + gate-logic engine-native 확인.

## (a) canonical 배선 상태 + gap
- g6_score_arm_bound — origin/main 존재(best-of-K + fals_bound)이나 CLM-only
  (g6_decode_best_of_k→gen_clm_ideate). ByteGPT ckpt 부적합.
- g6_score_arm_auto — anima evaluate canonical 단일진입
  (cli/evaluate.hexa g_eval_g6_seeded_W→g6_score_arm_auto_W→gen_auto_ideate→bytegpt)이나
  fals_bound 항 없음.
- GAP = ByteGPT-capable bind twin g6_score_arm_auto_bound(best-of-K bytegpt + fals_bound)
  미존재. additive 추가(frozen 미터치)하면 anima evaluate 가 fals_bound engine-native 방출.

## (e) follow-on ING (인프라 해소 시)
engine-native CORE .hexa 재디코드(g6_score_arm_auto_bound best-of-K bytegpt) 3-arm 을
전용/clean GPU pod(summer/aiden clear 대기 or 렌트)에서 실행 → 이 게이트 로직 재채점 →
TARGETED fals_bound > SHUF 재확인 = decode-축 terminal.
- ckpts on summer(owned): h1129.bin(BASE) + g6tc_targeted.bin + g6tc_shuf.bin,
  sha256 = state/g6_targeted_corpus/results/ckpt_manifest.json. BASE 는 aiden 에도 존재.

## 산출 파일
- g6score_engine_native.hexa — engine-native 채점기(core/g6_ideation.hexa 채점 fn verbatim).
- engine_native_scoring.txt — hexa stdout(9 셀 fals/fals_bound).
- terminal_verdict.json — 9/9 byte-parity 대조표 + 판정 + 배선 gap + follow-on.
