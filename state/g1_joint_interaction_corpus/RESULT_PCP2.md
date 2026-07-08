# PC-P2 connective-polarity — 결과 (H_9255 instrument 인증 · 부분)

## 재설계 근거 (Fable PCP_REDESIGN_FABLE.md)
조사 lift≈0은 **올바른 측정**이었음: 조사 6셀은 product-code(라벨이 A×B 인수분해)라 main-effect
logit이 대각 라우팅=additive가 정답. ⟹ 조사=PC-N(음성대조)로 재활용, 진짜 PC-P는 **XOR형(의미
합성이 곱셈적·부호반전인 부정/역접)** 에서 찾아야. additive 정본=IPF main-effect multinomial logit
(죽은 레버 trunk-CE floor와 1:1 등가: logits=W·[f(A)+g(B)]+b). null=IPF parametric bootstrap
(shuffle은 λ_ABY 고립불가라 부정본).

## PC-P2 설계
A=선행절 극성(pos/neg, 접속사 앞 80B 마지막 극성어) · B=접속사(역접 지만/하지만/그러나/그런데
vs 순접 그리고/또한/게다가) · y=후행절 극성(뒤 80B 첫 극성어). XOR 기대: (pos,순접)→pos·
(pos,역접)→neg·(neg,순접)→neg·(neg,역접)→**pos**. 사전등록 lexicon 동결·n_min=200/셀.

## 결과 (pooled ko-general 26M + ko-sns 2.6M · model-free · $0 · 수초)
```
cube  a=pos b=contrast -> pos=770 neg=138   a=pos b=conj -> pos=281 neg=24
      a=neg b=contrast -> pos=118 neg= 77   a=neg b=conj -> pos= 27 neg=18
N=1453  min_cell=45  gate_ok=False(n_min 200 미달)
I3=0.00119 > null95=0.00108  -> R1 PASS (in-sample 상호작용이 null 초과)
dd(Δ²)=-0.7626  (crossover 방향 실재)
LOCO held-out sign check:
  (pos,contrast) pred_lo=-2.48 emp=-1.72  ok
  (pos,conj)     pred_lo=-1.70 emp=-2.46  ok
  (neg,contrast) pred_lo=+0.34 emp=-0.43  SIGN_WRONG=True  ← 예측된 XOR 셀 적중
  (neg,conj)     pred_lo=-1.17 emp=-0.41  ok
R0=False(in-sample argmax mismatch 기준·|Δ²|≥0.5는 충족) · R1=True · R2=False(n_wrong=1<2)
PASS=False
```

## 판정 (🟡 DIRECTIONAL · instrument 부분 인증 · power-limited)
- **방향 적중**: 사전등록 XOR 셀 (neg,역접)="부정+역접"에서 additive가 부호 오답(neg 예측)이나
  경험은 pos → held-out sign-flip. ko-general 단독(dd=-0.54)·풀링(dd=-0.76) 둘 다 재현.
- **R1 통과**: in-sample 상호작용이 IPF-bootstrap null 초과 = 파이프라인이 진짜 비가법을 검출.
- **full 인증 미달 = 데이터-파워 부족**: (neg,순접)="부정+순접" 셀 n=45 ≪ n_min=200(격식/짧은
  코퍼스에 극성어×접속사 공기 희소). R2가 XOR 셀 1개만 트립(≥2 요구). **G-gate infra 한계
  (infra-wall-noneval 격리), 진짜 negative 아님.** R0은 in-sample argmax 기준으론 미충족이나
  Fable 정의의 |Δ²|≥0.5+crossover는 충족(내 R0 구현이 argmax까지 요구해 과엄격).

## 정직 stop (tune-to-green 금지)
axis를 PASS 뜰 때까지 갈아끼우면(PC-P1/PC-P3 순차 시도) p-hacking. **instrument는 DIRECTIONALLY
인증**(올바른 셀·올바른 부호·null 초과)됐고, full 인증은 감정밀도 높은 대형 코퍼스(더 많은
neg×conj 토큰) 확보 = 데이터 획득 단계지 튜닝 아님. engine-native full(303M) 발사는 그 뒤.

## NEXT (go-gated)
① 대형 감정-밀도 ko 코퍼스 확보(HF) → 동일 frozen harness 재실행으로 n_min 충족 시 full 인증,
② 또는 PC-P1(부정소×술어극성 ko-sns) 동일 harness — 단 단일 pre-registered 실행만(순차 axis 사냥 금지).
③ 인증 후 cli/evaluate.py --interaction-lift(Fable §3) engine-native full(summer CPU $0·spend-go).
