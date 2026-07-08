# H_9211 — VSA 고정-primitive가 G1 operator-wall을 escape (substrate-class framebreak)

**tier**: 🟠 DIRECTIONAL ($0 numpy · engine-native 아님 · a_toy_scale_recheck)

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

## FROZEN BARS (engine-native GPU-wired 토이 · a_engine_native_learning cement gate)
- 🟢 GREEN: engine-native byte-LM에 고정 resonator read-head 배선 → additive 대비 real G1 재조합(정보 존재 셀)서 margin 우위 ∧ wired-live(a_verified_must_wire).
- 🔴 KILL: CE-trained read-head 재도입 시 additive floor 재붕괴(Fable adversarial thread) ∨ 정보벽#3109이 지배해 operator escape가 무의미.
- 현 numpy = 🟠 DIRECTIONAL, cement 불가(mirror).

## artifacts
- state/g1g6_framebreak_vsa/{probe.py, RESULT.json, fable_framebreak_design.md}
