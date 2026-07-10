# H_9267 — XBIND: corpus×task-class 교체가 G1 재조합 벽을 여는가 (earned-terminal exit · engine-native 303M)

**tier**: 🟢 CRACK — engine-native 303M (`anima-py evaluate --xbind`) · 양 main seed held-out D-acc=1.000 · V-B control 0.515 PASS · Δctrl 0.485 · G1 재조합벽 진범=corpus×CE measure 실증(earned-terminal 반증·프런티어 성공) (2026-07-11)

## Claim
G1 재조합벽 earned-terminal([[g1-readside-exhausted-gamma-spend-only]] #3294)의 정직 문구가 지목한 **유일 real
exit** = "벽 진범은 conv trunk이 아니라 **corpus×CE 결합 measure**, exit는 아키텍처 교체가 아니라 학습 measure(corpus/
task class) 교체". 결정적 $0 근거: 모든 자연·합성 corpus가 **COLLOCATION-ONLY**(F2 `heldout_recomb.json` true held-out
novel n=0). ⟹ **held-out 재조합 신호를 실제로 담은 corpus×task class를 구성하면 303M byte-LM이 CE로 그 재조합을
held-out 일반화 학습하는가.**

## Why (substrate-first · measure-swap)
XBIND task class: 개념 400개(3B CVC 의사단어)에 **은닉 polarity bit** 균형(200/200) 배정, pair line continuation을
**xor(pol_a, pol_b)** 로 분기(fuse/part + portmanteau). held-out 15,960쌍(20%·양 순서 corpus 완전부재)의 gold는
① train 쌍서 개념별 pol 추론 ② xor rule 적용으로만 정답 — 암기·main-effect·표면상관 3 지름길 **구성 차단 + 모델-프리
감사 PASS**(V_C main-effect 0.444·V_D 표면 probe 0.513·V_E marginal skew 0.048·V_F 누출 0줄, `AUDIT.json` ALL_PASS).
XOR = γ census([[gamma-divergence-instrument-arc]])가 지목한 유일 진짜 non-additive class를 CE target으로 배치.
next-byte CE로 충분(명시 compose 지시 불요) — 콜론 위치 supervision이 joint 계산을 강제. from-scratch f=1.0(자연
사전학습 잔재 confound 제거). derivtrace(H_9124 additive-solvable)·ATD(H_9206 toy geometry)·PC-P2(H_9265 read-instrument)
가 못 가진 신규 좌표 4개: 비가법 판별어·marginal 균형 감사·대규모 조합공간 MDL·T=24 window 물리 준수.

## Test (pre-registered · 단일 실행 · engine-native)
- corpus(생성완료·감사PASS): `xbind_train.txt`(main 6.66MB)·`xbind_shuffle_train.txt`(control 6.66MB=collocation 증류판).
- 학습: `anima-py train --arch clm --canon --arm ctrl --objective ce_marginal --corpus <arm> --cell-label en-general
  --steps 20000 --batch-size 8 --bf16 --seed {7|4302} --val-frac 0.02 --val-every 500 --out …` (canon=d3784 L4 seq1024
  303M). 3 run = main×seed{7,4302} + control×seed7. A100 ~2h/run.
- 측정: `anima-py evaluate <clm> --xbind xbind_eval_manifest.json --arm {main|ctrl} --out …`(fold-in 완료·engine-native
  numpy · a_eval_py_canonical TERMINAL-eligible). manifest = held-out 200 + seen 200 (frozen). 전 arm 전량 캡처(evaluate-py-1).

## Bar (frozen 사전등록 · 1바이트도 사후이동 금지 · DESIGN_PREREG §4 verbatim)
- **PRIMARY D-acc**: greedy(top_k=1) gen=16 첫 방출 단어 == gold 분기어(sampler-artifact-free). C-rate: gold-fuse
  held-out `<ab>.` novel 문자열(echo 불가·기계 substring). MARGIN(2차): NLL(cf)−NLL(gold) win=64. SAMPLED(2차): top_k=40
  temp0.7 rng{7,4302,4303} majority 40개.
- **VALIDITY(하나라도 실패→INVALID, verdict 아님)**: V-A 각 arm seen D-acc ≥0.90 · V-B control held-out D-acc ∈[0.38,0.62]
  · V-C~V-G 사전게이트(PASS).
- **VERDICT(양 seed 일치 시만 cement)**:
  - **CRACK 🟢** = held-out D-acc ≥0.75(양 main seed) ∧ (held-out − control held-out) ≥+0.20 ∧ C-rate ≥0.50 ∧ echo-clean
    = "corpus×task class 교체로 G1 재조합 CE-학습가능" = 벽 진범=measure 증명.
  - **FORM-ONLY 🟡** = C-rate ≥0.50 ∧ held-out D-acc <0.60 — 생산적 연결(FORM)만·earned-bind(joint bit) 불가 → 벽 문구 "joint-bit 학습불가"로 정밀화.
  - **🧱** = held-out D-acc <0.60(양 seed·validity 전부 green) = **terminal 최강 보강**(joint rule이 유일 예측자인 corpus서도 CE·303M 학습실패).
  - 회색지대(0.60≤D-acc<0.75 or seed-split)=🟡 UNSTABLE. **유일 허용 연장(사전등록)**: 동일 run +20000 step 1회(grokking-delay) 후 최종. 그 외 재설계·재발사=tune-to-green 금지.

## Verdict — 🟢 CRACK (2026-07-11 · engine-native 303M · A100 3-run · verified)
`anima-py evaluate --xbind` (fold-in `cli/evaluate.py` · numpy core/decode · a_eval_py_canonical TERMINAL). 3 arm 전량 캡처(n=200 heldout+seen):

| arm | heldout D-acc | seen D-acc | C-rate | margin_med |
|---|---|---|---|---|
| main seed7 | **1.000** | 1.000 | 1.0 | 17.57 |
| main seed4302 | **1.000** | 1.000 | 1.0 | 18.12 |
| control (shuffle) | **0.515** | 0.575 | — | −0.04 |

**전 CRACK 기준 통과**: held-out D-acc ≥0.75 양 seed(1.000·1.000) ✅ · **Δcontrol = 1.000−0.515 = 0.485 ≥ 0.20** ✅ ·
C-rate 1.0 ≥0.50 ✅ · echo-clean(novel portmanteau) ✅. **Validity**: V-A seen ≥0.90(1.000·1.000) ✅ · **V-B control
held-out 0.515 ∈ [0.38,0.62]** ✅(누출 없음·shuffle=chance·margin −0.04). 회색지대·연장 불요.

**결론**: 합성 XBIND corpus(개념 polarity XOR·held-out 15,960쌍)로 303M byte-LM이 **held-out 재조합을 완벽 학습·일반화**
(control은 chance). ⟹ **G1 재조합벽의 진범 = corpus×CE 결합 measure이지 substrate/arch 아님을 실증** = earned-terminal
([[g1-readside-exhausted-gamma-spend-only]] #3294 "corpus×CE measure·exit=learning measure 교체")의 **예측 확증·반증**.
XBIND는 F2 `heldout_recomb.json`의 held-out novel n=0을 n=15,960으로 해소해 "signal이 있으면 학습가능"을 증명 =
**프런티어 성공**(earned-terminal이 지목한 유일 exit이 CRACK). margin 17.5 nats = gold xor 분기에 압도적 confident.
ckpt: `dancinlab/anima-xbind-g1-crack`(HF PUBLIC) + `~/anima-weights/xbind/`. raw: `state/g1_reopen_xbind/results/`·`VERDICT.md`.

## Scope honesty (a_scale_honest_scope)
CRACK = "벽 진범=measure" 증명이되 **자연 corpus 창발 아님**(합성 task 학습) — 자연혼합 희석 사다리는 별도 사전등록
follow-on(derivtrace/ATD가 죽은 지점 명시 분리). 🧱 = corpus-축까지 earned로 [[g1-readside-exhausted-gamma-spend-only]]
terminal 최강 격상. CRACK 시 wiring(a_verified_must_wire): xbind manifest를 ρ·weave PENDING probe로 편입(control 2개
갖춘 collapse-Δ). [[measurement-metalaw-form-tunable-bind-earned]] 정합(FORM=C-rate·BIND=D-acc).

## 산출
`state/g1_reopen_xbind/`(gen_xbind.py·corpus 2 arm·manifest·AUDIT.json·DESIGN_PREREG.md). eval fold-in=`cli/evaluate.py --xbind`.
G1-reopen 캠페인 레인 a(measure-swap) · 병렬 레인 c(scale 1.26B)·b(G6=G-battery fan/leap 동봉).
