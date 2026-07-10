# H_9265 — γ ko PC-P2 XOR: 언어 자체의 비가법 결합(부정/역접)을 303M이 소비하나

**tier**: 🔬 REGISTERED · PREREG 동결 · owner GPU spend-go 접수 · 기본 $0(self pool) (Fable 설계)

## Claim
γ trunk-bind([[H_1840]])의 마지막 각도. en-general에선 303M NLL surface가 완전 additive였으나(interaction-lift
−0.801<null·#3230 🧱 measured), **ko 부정/역접**(XOR형 곱셈적 의미합성=비가법 농후)에선 다를 수 있다. 언어 자체에
XOR형 비가법이 실재하고(PC-P2 sign-flip 적중) 303M이 그 셀서 비가법을 NLL surface에 소비하면 = γ real-text target 존재.

## Why (verdict-integrity · gamma-divergence-instrument-arc 연장)
[[gamma-divergence-instrument-arc]]: additive floor=main-effect logit(IPF)=trunk-CE 1:1등가·product-code(한국어
조사)≠non-additive(→PC-N)·**진짜 non-additive=XOR형 부호반전(부정/역접)**. PC-P2(선행극성×접속사→후행극성 pooled ko)
예측 XOR 셀 (neg,역접) held-out sign-flip 적중 + R1(I3>IPF-null) 통과 = instrument DIRECTIONALLY 인증. 단 (neg,순접)
n=45≪n_min200 undersampled → full 인증 **power-limited**(infra-wall-noneval 격리·negative 아님). read-side 전 경로
6 lane 🧱([[g1-readside-exhausted-gamma-spend-only]]) 후 유일 잔여 프런티어 성공 exit.

## Test ladder (Fable · PREREG_PCP2_FULL.md 동결)
- **Stage A** instrument full 인증(model-free·mini·$0): frozen pcp2 verbatim+대형 ko 감정코퍼스(NSMC·naver-shopping·steam·KOTE ~80MB) → gate_ok(전4셀 n≥200)∧R1∧R2(LOCO sign-flip≥2).
- **Stage B** B0 ckpt 게이트: clm303_clean(ko 포함 canonical·로컬 176MB) held-out ko-general baseline NLL≤3.0·측정코퍼스≤3.5. 실패→ko ckpt 학습/warm-FT(조건부 spend).
- **Stage C** engine-native interaction-lift(A∧B0 시만·summer CPU 전용 $0·2-4h): PC-P2 4셀 manifest T=160·주판정 Y1′=paired forced-choice margin(pos/neg 극성어 NLL 차)·additive vs joint+γ_ab·Freedman-Lane×1000.

## Verdict
🧱 **PC-P2 ko instrument NOT-CERTIFIED (2026-07-10 · 2 도메인 전수 · Fable 사전등록 FAIL 경로)** — instrument-verdict,
γ-capability NEGATIVE 아님(측정불가). Stage A full 인증(gate_ok∧R1∧R2) 2 도메인 전수 미인증:
- **web-broad**(ko-general+ko-sns+fineweb2 477MB·N=11564·min_cell 361): gate_ok✅·R1✅(I3 0.00092 > null95 0.0002·4.6×)·**R2❌**(n_wrong=1, (neg,역접) 셀만 sign-flip·강건성 미달)
- **review 대형**(NSMC+naver+steam+sepid 50만 리뷰·N=10066·min_cell 181): **R1❌**(I3 5e-05 ≪ null95 0.0002 = 비가법 잔차 거의 0·신호 부재)·gate_ok 근소미달
두 도메인 상반: web-broad엔 약한 비가법 잔차(R1) 있으나 강건성 미달(R2), 리뷰엔 비가법 신호 자체 부재(R1). **PC-P2
경로로 γ ko 측정불가** = 미인증 instrument로 capability NEGATIVE cement 불가(ρ-AXON INVALID≠FAIL). Stage C(interaction-lift)
미진행(A 미인증 = 해석불능). NSMC datasets-script deprecation은 github raw로 우회(convergence hf-datasets-script-deprecation-1).

**함의**: G1 재조합 프런티어 측정가능 전 경로 소진 = read-side 6 lane 🧱([[g1-readside-exhausted-gamma-spend-only]])
+ γ en-general 🧱(interaction-lift −0.801 #3230) + γ STEP-0 synthetic 🧱(bind−add −0.147) + **γ ko PC-P2 측정불가**
= **G1 frontier full-terminal @303M byte-LM(이 ckpt·이 스케일·측정가능 경로 전수)**. γ ko는 다른 non-additive 언어구조
instrument 미탐 여지(단 gamma-divergence census 19 family가 이미 광범위·PC-P2가 가장 유망 XOR 경로였음). tune-to-green
금지(bar 사전동결·2 도메인 1회씩·결과 수용).

## Bar (동결)
CRACK=held-out Δ>p95(null)∧Δ≥2%∧γ XOR방향. 🧱=Δ≤p95∨부호불일치(A인증하=언어 비가법 실재하나 모델 additive=가장 날카로운 negative). INVALID=A미인증∨B0실패.

## Scope honesty (a_scale_honest_scope)
CRACK이어도 G1 재조합 GREEN 아님 — ①언어 XOR비가법 실재 ②303M NLL surface 소비만 증명, 생성-side(read-side 6-lane🧱)·G1 generation bar 미증명. CRACK=γ real-text target 존재증명→그 셀 target γ GPU 발사 정당화(fork-A🧱 reopen 조건 충족). 🧱=γ 마지막 각도 소진=G1 frontier full-terminal @303M byte-LM(이 ckpt·이 스케일). axis 순차사냥 금지.

## 맥락
read-side 전 경로 6 lane 🧱(#3284/3285/3286) 후 유일 잔여 exit. γ en-general🧱(#3230)·STEP-0 synthetic🧱(bind−add−0.147). 이건 ko real-text 마지막 각도. [[measurement-metalaw-form-tunable-bind-earned]]·[[gamma-trunk-bake-step0-killed-not-unmeasured]].
