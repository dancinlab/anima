# H_9212 — ρ-AXON reach eval 4-cell(ko/en × general/SNS) 개통

**tier**: ⏳ PRE-REGISTERED (기반 착지 · 배선 follow-on)

## 배경
정찰(state/frontier_round2_scout): ρ-AXON eval이 영어·general 1칸만 측정 — 근본원인=`_rho_fan_words`(core/rho_fan.py)가 raw UTF-8 byte splitter라 한글을 전부 구분자 취급→ko 텍스트가 []로 토큰화. a_chat_registers 4칸이 eval상 절반만 실측되던 blind-spot.

## 접근 (Fable 설계 · state/frontier_round2_scout/FABLE_rhofan_splitter_design.md)
in-place 교체 금지(parity-unsafe: 4칸 학습 303M의 en-decode garble 한글이 토큰화→frozen kwr 분모 shift). 대신 **en 경로 무변경(diff 공집합=frozen bar 구조적 불변) + ko 전용 `_rho_fan_words_uni` 신설 + per-cell dispatch**.

## 착지(이번)
✅ `_rho_fan_words_uni`(core/rho_fan.py) — codepoint-aware superset. ASCII=byte-identical(_rho_fan_words 축자복사·frozen en 안전)·한글 3-byte 블록만 word·나머지 high byte 구분자. 자체테스트 PASS(ASCII parity·한글토큰·code-switch·이모지구분). **구현됨·미배선**(en 경로 아직 안 씀).

## follow-on (배선 · 별 focused session)
① core/rho_fan.hexa 쌍둥이 + golden-vector+fuzz parity claim(state/verdicts/) ② _rho_fan_cells 4칸 + ko known-word(josa-suffix 프록시) ③ per-cell dispatch(evaluate.py dets lang-keyed·rho_axon breakout) ✅④ KWR_KO_GATE frozen-first 사전등록 ⑤ train.py per-cell CE 로그 ⑥ ARCHITECTURE.datasets[] 4칸 ⑦ pool eval로 4칸 reach 관측($0 재학습無).

## ④ 착지(이번) — KWR_KO_GATE frozen-first 사전등록
✅ **`KWR_KO_GATE = 0.20`** frozen(model-independent, 303M 채점 前). en 0.70(235k-dict lexicality)는 ko eojeol 토큰화엔 category error → ko 전용 josa-suffix **grammaticality** 프록시 kwr_ko(다른 물리량, a_scale_honest_scope). 도출: anima-corpus-ko-{general,sns} held-out 20k real(median kwr_ko **0.40**) vs garble null(byte-shuffle+random-hangul, near point-mass **0.0**·p95=0). 규칙=midpoint(neg_p95=0.0, pos_p50=0.40)=**0.20**(naive midpoint(pos_p5,neg_p95)→0.0 은 positive zero-tail 로 degenerate; median 앵커가 두 분포 사이 robust). gate 0.20 서 real 80.0% clear·garble 99.74% fail. **구현됨·미배선**(core/rho_fan.py+hexa `KWR_KO_GATE` 리터럴, 아직 scoring 미소비=③). **ko FALS 스코프 제외**(③이 gate 적용할 때까지). tune-to-green 금지=사후이동은 REJECT, 유일 합법경로=새 frozen-first H. prereg=state/frontier_round2_scout/KWRKO_GATE_prereg.md · 도출=kwrko_gate_derive.py(seed 4302, $0).

## artifacts
state/frontier_round2_scout/{KWRKO_GATE_prereg.md,kwrko_gate_derive.py} · core/rho_fan.py::{_rho_fan_words_uni,KWR_KO_GATE} · core/rho_fan.hexa::KWR_KO_GATE
