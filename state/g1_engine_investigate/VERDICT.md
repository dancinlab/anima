# G1 L8-cov torch↔engine 발산 root-cause 조사 (verdict-integrity)

date: 2026-07-03 · host: aiden(pool, RTX5070) · ckpt: clm303_deep_L8_cov (d=2781 L=8 E=4 V=256 K=3)
방법: H_1587 전례(g1g6-wall-engine-innocent-3axis) 재현 — forward/detector/decode-procedure 3-축 격리.

## 핵심 결론: 발산은 존재하지 않는다 (범주 오류) — ENGINE INNOCENT

premise("torch coverage 레버가 G1 엶 vs engine G1=0 floor")는 서로 다른 두 측정축의 category error.
- torch "레버 열림" = H_6182~6185, 3.3M/2.5M param TOY attn/convd, 24-concept 합성 코퍼스,
  metric = held-out strict pair-match ACCURACY (teacher-forced 슬롯채움; held 0.95 vs LOW 0.03 vs SHUF 0).
  = held-out 정확도 probe이지 G1 best_distinct 생성 측정이 아님. 자체 "torch 미러 DIRECTIONAL,
  303M transfer 미검증(a_toy_scale_recheck)" 명시.
- engine "G1=0 floor" = production 303M L8-cov, metric = G1 best_distinct 개방형 생성(gen40).
- 이 coverage 레시피를 실제 303M trunk(L8-cov)에 적용했을 때:
  torch fp32 자체 probe(gauge_lib, 학습로그 step6000)도 g1_composed_distinct=0.
  => 303M 스케일에서 torch와 engine이 동일하게 G1=0. 발산 없음.

## 3-축 격리표

축1 Forward parity: .pt fp32 vs .clm int4 numpy, 동일 프롬프트
  argmax@decode 일치(102=102) · allpos 20/24 · top5 동일 토큰집합 재배열 · max|Δlogit|=8.81 mean=2.14
  => 엔진 무죄 (Δ=int4 양자화노이즈, mis-load 아님)
축1a Dim/load: engine d=2781 E=4 V=256 K=3 L=8 · torch load missing=[] unexpected=[] · 차원 완전일치 => 무죄
축1b Coherence: engine argmax='f' top5 전부 소문자ASCII · G0 kwr5/5 · G2 novel=100 => forward 정상, garbage 아님
축2 Detector parity: torch gauge_lib g1 vs engine g_eval_g1 둘 다 best_distinct=0 (동일 concept-coverage 계열) => floor 합치
축3 Decode-procedure: H_6182~6185=toy held-out 정확도 probe(scaffold/best-of-K 아님) · 303M gauge_lib=mouth decode=0 · engine --py xorshift=0 => 양 sampler 모두 0 robust

## 판정
- 엔진 무죄. engine-native --py(core/decode.py)는 L8-cov weight를 차원/load/forward 전부 faithful 처리.
  G1=0은 측정결함 아님 = 진짜 floor.
- torch coverage 신호 성격 = (c) toy-scale + held-out-accuracy probe. 실제 303M G1 생성 측정 아님.
  303M transfer 안 됨(engine 0, torch 자체 probe도 0).
- 양자화 무죄 재확인: max|Δ|=8.81=int4 양자화노이즈나 argmax@decode 보존. quant-destroys-emergence는 이미 REFUTED.

## H_6187 verdict 함의
H_6187 = engine-native G1 TERMINAL floor 확정. L8(RF확장)+조합-커버리지블록(held val_CE 0.145/0.189 DESCENT=fit됨)에도
engine-native G1 best_distinct=0. coverage는 held-out CE(perplexity, p7 Goodhart축)만 내렸을 뿐 G1 재조합 생성을 못 엶 —
torch 자체 probe도 동일. 측정결함 재측정 불필요. 벽 = trunk-objective floor(g1-lever-multilens-objective 정합).

## honest scope
- forward parity는 byte-exact 아니라 argmax-faithful(int4 vs fp32). 전례 H_1587 ~2e-5는 fp32-fp32였음.
- torch fp32 303M scaffold/best-of-K G1은 이 캠페인에서 애초에 측정된 적 없음(toy만). H_1587식 scaffold-inflation
  전례는 여기 적용대상 아님(부풀릴 303M torch 숫자 자체가 없음). 진범=toy축↔production축 conflation.

## 산출물
forward_parity_result.json · engine_dims_forward.json · engine_side.log · torch_parity.log · parity_probe.py · torch_parity.py
증거원본: state/g1_coverage_prod_block/results/train_L8cov_full.log(torch g1=0), results_gen40/(engine G1=0),
state/g1_coverage_bytes/RESULTS.md + v3_nlbyte/(toy DIRECTIONAL 정체)
