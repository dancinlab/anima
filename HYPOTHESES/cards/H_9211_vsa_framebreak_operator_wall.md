# H_9211 — VSA 고정-primitive가 G1 operator-wall을 escape (substrate-class framebreak)

**tier**: 🧱 FALSIFIED as a G1 transfer lever (2026-07-08 · kill-shot 통제 + 논리 스퀴즈 · terminal-grade)

> **종결**: operator-escape는 transfer 레버가 아니라 **superposition-capacity** 레버(인수분해 handed일 때만). kill-shot: 같은 task서 atom을 handed(clean)→blind(학습 byte-LM hidden)로 바꾸면 B 1.000→0.048 붕괴(순환성 margin 0.95·offdiag|cos| 0.035→0.636). G1 벽 본질=학습된 인수분해 부재이므로 고정-대수는 그걸 우회 못 함. 모든 수리경로가 γ(H_1840)로 수렴. **G1 능력천장 유지**. 상세 state/g1_stage2_byteLM_resonator/FALSIFICATION.md.

## 배경
G1/G6 재조합벽은 origin/main에서 전 축 terminal 확정: data #3109 · E1 SLW forward-slot KILL #3107 · γ trained-constructive-bind DUP-WALLED #3108 · all-axis DPI objective-basin #3046. Fable5 framebreak 설계(state/g1g6_framebreak_vsa/fable_framebreak_design.md)가 재프레임: **DPI가 지목하는 건 conv/attention이 아니라 "bind가 next-byte-CE gradient에서 학습된다"는 사실 하나**. 탈출 = bind·unbind·decode를 **고정 substrate primitive**로 만들어 CE gradient가 atomic codebook만 건드리게. #3108이 죽인 건 CE-trained readout을 단 bind이고, 이건 **고정 대수 read-path**라 별개 각도.

## 가설
학습 0의 고정 VSA/HRR primitive(circular-convolution bind + resonator/cleanup decode)는 held-out 재조합을 additive floor 이상으로 복원한다 = **operator 벽은 substrate-class escapable**. INFORMATION 벽(#3109, 코퍼스에 novel-pair follower 정보 부재)은 별개이며 어떤 operator도 해결 못 함.

## 결과 ($0 numpy · state/g1g6_framebreak_vsa/probe.py · RESULT.json)
초과중첩 번들 partner 복원(held-out 짝, 학습 0):
- M=4: VSA **1.000** / ADD 0.240 / SHUF 0.000 (chance 0.002)
- M=8: VSA **1.000** / ADD 0.137 / SHUF 0.000
- M=16: VSA **1.000** / ADD 0.070 / SHUF 0.000
- M=32: VSA **0.987** / ADD 0.020 / SHUF 0.000
→ VSA≫additive(용량 붕괴)·SHUF=0(binding 통제 정상). **OPERATOR-WALL-ESCAPABLE (DIRECTIONAL)**.

## 토이 검증 (aiden pool $0 · torch 3seed · Fable 설계 스펙 · 🟠 DIRECTIONAL/MIXED)
role-filler 회상(R=6·F=30·held-out=`r==f mod6`), 4 arm 동일 codebook: A=CE-readhead·B=고정HRR-resonator·B0=frozen·C=additive.
| seed | A held | B held | C held | B bind-destroy |
|---|---|---|---|---|
| 0 | 0.499 | 0.953 | 0.085 | 0.347 |
| 1 | 0.091 | 0.961 | 0.094 | 0.355 |
| 2 | 0.016 | 0.933 | 0.088 | 0.328 |
(chance 0.033 · A/B indist=1.0 validity ✓ · train A/B=1.0·C=0.42~0.49)
- ✅ **B vs C(연산자 격리) CLEAN·ROBUST**: 고정 HRR 0.93~0.96 ≫ additive 0.085~0.094 전 seed, 연산자(⊛ vs +)만 차이 → escape는 연산자 귀속. bind-destroy(⊛→+)=0.33 붕괴.
- ⚠️ **clean GREEN 미달→MIXED**: 사전등록 "A≤0.40 all" 을 seed0 A=0.499가 초과(A는 seed-요동 0.50/0.09/0.02, CUDA 학습 비결정). no-tune-to-green으로 바 불변.
- ⚠️ **B≈B0**(0.949~0.971): 승리=HRR 대수 자체(Plate1995). 정직한 명제="CE-gradient가 고정-bind read-path 오염 안 함"(B=B0), "B가 bind 학습"은 아님.

## FROZEN BARS (engine-native 승격 gate · a_engine_native_learning)
- 🟢 GREEN: engine-native byte-LM(atoms를 byte서 학습·LM objective·`core/` decode)에 고정 resonator read-head 배선 → additive 대비 real 재조합(정보 존재 셀) margin 우위 ∧ wired-live(a_verified_must_wire).
- 🔴 KILL: CE-trained read-head 재도입 시 additive 재붕괴(Fable adversarial thread) ∨ 정보벽#3109 지배.
- 현 numpy+torch-toy = 🟠 DIRECTIONAL, cement 불가(mirror·symbolic ID·no byte/LM/core).

## artifacts
- state/g1g6_framebreak_vsa/{probe.py, RESULT.json, fable_framebreak_design.md}
- state/g1g6_framebreak_vsa/toy/{probe.py, RESULT.json, fable_spec.md, TOY_SYNTHESIS.md}
