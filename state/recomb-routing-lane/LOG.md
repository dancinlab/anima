# 🧭 domain: recomb-routing-lane

**정의**: G1 재조합벽(ρ·weave)을 "trunk 표현-용량 벽"이 아니라 **readout-ROUTING 벽**으로 재규정하고, 앞 개념을 생성점에 나르는 **read-side context-pooling lane(fork A · CLML)**을 배선·학습·측정해 그 벽을 여는 프로그램. 핵심 열린질문 = 그 routing이 **학습가능한가(신호벽 H_1840 한층위인가)**.

## 아크 (2026-07-08~09 · SSOT=card H_9235 · ARCHITECTURE gate-g1-recomb-gamma)
- **재규정(#3189 H_9235 H2-lite)**: 벽 ≠ 표현용량. 두 개념 full-context 다 존재(mean-pool 복원 A=0.95 B=0.97)·clean slot 완벽결합(handed 1.00). 마지막(생성)위치만 앞개념 소실(A=0.07)=receptive-field 감쇠(언어무관·이중언어 반박). ⟹ 벽=**routing**.
- **route 증명(#3191)**: fork-A $0 pre-check — mean-pool→gelu가 held-out XOR 0.98 라우팅, last-only 0.47·linear 0.43 FAIL.
- **엔진 배선(#3192)**: CLML read-side lane을 .clm forward에 배선(core/clml.py codec+forward+serialize·smoke).
- **학습 파이프라인(#3196)**: --dump-hidden --with-logits·clml_extract·clml_train·clml_wire(frozen-trunk numpy·정확 inference-yn).
- **copy-trap 조기포착(#3210·convergence clml-train-py-1 #3211)**: derivtrace-CE=copy-dead(트렁크 복사·CE 0.0003·신호死=H_1840 lane층위).
- **no-copy 재설계(#3215)**: Fable 4-gate — verdict형식(정의부 제거)·word-initial CE·pair-split. Gate2 trainability probe=신호벽 결정terminal.

## 🔴 LIVE: Gate 1/2 (no-copy trainability probe · aiden anima-py dump)
Gate1 no-copy word-initial base CE≫0? · Gate2(★결정): frozen pool이 name→word 라우팅을 TRAIN fit하나 → 🟢학습가능(Gate3·4 system-G1) / 🧱(B)신호벽(route XOR로 존재하나 실task 학습불가=H_1840 한층위·정직 종결).

## 정책·인프라
막힌 벽=Fable 위임(walls-delegate-to-fable). pool=aiden anima-py(hexa-less·anima-py-pool-install-hexaless).
