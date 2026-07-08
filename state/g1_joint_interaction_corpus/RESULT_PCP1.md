# PC-P1 negation×predicate→emotion-marker — 결과 (H_9255 · DOA · 데이터-파워 종결)

## 실행 (단일 pre-registered · ko-sns · model-free · $0)
Fable 3후보 중 SNS-dense XOR 타입. A=부정소(안/못) · B=술어극성(pos 좋/맛있… vs neg 나쁘/싫…) ·
y=후행 정서마커(laugh ㅋ/ㅎ vs sad ㅠ/ㅜ, 40자 내). effective sentiment=B XOR A.

## 결과
```
cube  neg=no  pred=pos -> laugh=95 sad=0    neg=no  pred=neg -> laugh=3 sad=0
      neg=yes pred=pos -> laugh= 1 sad=0    neg=yes pred=neg -> laugh=0 sad=0
N=99  min_cell=0  gate_ok=False  I3=0  PASS=False
```
**DOA(측정불가)**: ① N=99(ko-sns 2.6M자에 부정소+술어+정서마커 3-공기 극희소), ② y가 laugh로
**degenerate**(ㅋ/ㅎ가 ㅠ/ㅜ 압도→'first marker'가 거의 항상 laugh, sad=0 전셀). 축이 데이터·분포
둘 다 무력 = 진짜 negative 아님, instrument 데이터-파워 부족(infra-wall-noneval 격리).

## 종결 프레임 (model-free instrument 경로)
로컬 등록 ko 코퍼스(ko-general 26M자·ko-sns 2.6M자)로 검출력 대조 소진:
- **PC-P2(연결어미 극성) = DIRECTIONALLY 인증**: 파이프라인이 진짜 XOR을 검출(예측 셀 (neg,역접)
  held-out sign-flip 적중 + R1 null 초과). **방법은 sound**.
- 단 full 인증(R0∧R1∧R2 @ n_min200)은 약셀((neg,순접))이 언어적 희소로 미충족(pooled 45).
- PC-P1(정서마커)은 ko-sns서 DOA(N=99·y degenerate).
⟹ **full instrument 인증 = 코퍼스-스케일 블록(외부 데이터 획득 의존)**. 진짜 XOR 현상(부정 스코프·
역접 극성반전)은 언어적으로 희소해 소형 anima 코퍼스로는 약셀 n_min 미달. axis 추가시도=tune-to-green 금지.

## 갈림 (오너 결정 · 둘 다 go-gated)
A) 대형 감정/논증-밀도 ko 코퍼스 HF 다운로드 → frozen harness 재실행으로 full 인증(데이터 획득 결정).
B) PC-P2 DIRECTIONAL 인증(파이프라인이 진짜 XOR 검출 증명됨)을 방법-검증으로 충분히 보고,
   바로 engine-native full(cli/evaluate.py --interaction-lift, 303M summer CPU $0·spend-go)로 진행.
census(g1-census-objfloor) CONFIRMED-TERMINAL 유지 — 어느 쪽도 재확인/재오픈 절차지 tune-to-green 아님.
