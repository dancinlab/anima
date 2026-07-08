# H_9212 — ρ-AXON reach eval 4-cell(ko/en × general/SNS) 개통

**tier**: ⏳ PRE-REGISTERED · ③ per-cell dispatch **WIRED (code-live)** · engine-native ko reach NUMBER = ⑦ pool 대기

**wired**: WIRED-live (cli/evaluate.py→cli/rho_axon.py per-cell breakout · en byte-identical) · terminal ko reach 관측 = ⑦ pool 303M decode (cross-machine 잔여)

## 배경
정찰(state/frontier_round2_scout): ρ-AXON eval이 영어·general 1칸만 측정 — 근본원인=`_rho_fan_words`(core/rho_fan.py)가 raw UTF-8 byte splitter라 한글을 전부 구분자 취급→ko 텍스트가 []로 토큰화. a_chat_registers 4칸이 eval상 절반만 실측되던 blind-spot.

## 접근 (Fable 설계 · state/frontier_round2_scout/FABLE_rhofan_splitter_design.md)
in-place 교체 금지(parity-unsafe: 4칸 학습 303M의 en-decode garble 한글이 토큰화→frozen kwr 분모 shift). 대신 **en 경로 무변경(diff 공집합=frozen bar 구조적 불변) + ko 전용 `_rho_fan_words_uni` 신설 + per-cell dispatch**.

## 착지(이번)
✅ `_rho_fan_words_uni`(core/rho_fan.py) — codepoint-aware superset. ASCII=byte-identical(_rho_fan_words 축자복사·frozen en 안전)·한글 3-byte 블록만 word·나머지 high byte 구분자. 자체테스트 PASS(ASCII parity·한글토큰·code-switch·이모지구분). **구현됨·미배선**(en 경로 아직 안 씀).

## 착지(②·이번 · #3131 py / #3133 hexa foundation 위)
✅ `_rho_fan_cells()`(core/rho_fan.py + .hexa 쌍둥이) — 4칸 register cells(ko/en × general/sns) concept-sentence 리스트. `en_general` = `_rho_fan_concepts()` **축자동일**(frozen en bar byte-identical); en cells는 frozen `_rho_fan_words`, ko cells는 `_rho_fan_words_uni`로 토큰화(`_rho_fan_cell_words` per-cell dispatch 헬퍼, 미배선). ✅ ko KNOWN-WORD 프록시 — `_rho_fan_ko_func()`(exact-match josa/function-word) + `_rho_fan_ko_josa()`(suffix-match) + `_rho_fan_ko_is_known()`(exact∨eojeol-suffix, stem≥1). **문법성 프록시지 lexicality 아님**(a_scale_honest_scope). frozen 리터럴 셋. 자체테스트 PASS(en 불변·ko 토큰 non-empty·dispatch 라우팅·KO_FUNC 멤버십) — 내부 subprocess import(top-level `python3 core/rho_fan.py` 금지=entry-guard). **구현됨·미배선**(스코어 패널 무변경·en verdict byte-identical). follow-on=③ per-cell dispatch(④ KWR_KO_GATE frozen-first 선행).

## ③ 착지 — per-cell dispatch 배선 (code-live)
✅ **evaluate.py dets 를 LANG-KEYED per-cell 로 배선** (`cli/evaluate.py::_build_cell_dets`). 4칸 각각이 자기 dispatch 번들을 받는다: ko→`{words_fn=_rho_fan_words_uni, kwr_fn=_rho_fan_ko_known_word_ratio, kwr_gate=KWR_KO_GATE(0.20), ngram_fn=_g_content_ngrams_uni, corpus_tokens=uni-토큰화}`, en→`{words_fn=_rho_fan_words, kwr_fn=_rho_fan_known_word_ratio, kwr_gate=0.70, ngram_fn=_g_content_ngrams, corpus_tokens=frozen-토큰화}`.
- ✅ **`_rho_fan_ko_known_word_ratio`(core/rho_fan.py + .hexa 쌍둥이)** — kwr_ko = hits(`_rho_fan_ko_is_known`)/n over `_rho_fan_words_uni` 토큰. `known` 인자는 무시(closed-class 프록시)·en kwr 와 시그니처-parity 로 axis fn 이 균일 dispatch. hexa typecheck exit 0(에러수 baseline 42==42 불변).
- ✅ **rho_axon `run_panel(…, cell_dets=)` per-cell breakout** — aggregate 경로는 **무변경**(en byte-identity 구조적 보장), `cell_dets` 주어지면 `panel["cells"]` 에 4칸 concept-driven 축(HILLOCK + ρ·form/leap/fan) 별도 산출. `render_cells` = value·control·Δ **인라인**(evaluate-py-1 준수). ρ·store/tether/self = 4칸 frozen probe set 이라 panel-level(register-cell 분해 아님).
- ✅ **ko FALS IN-SCOPE** (KWR_KO_GATE 등록 완료 → prereg §5 조건 충족): ko cell scored=kwr_ko + reach Δ. falsifiability comparator set 은 **영어 유지**(ko comparator set=별도 future H·en-set 번역재사용=tune-to-green 금지) → ko ρ·fan 은 falsi sub-check FAIL 가능(정직한 documented scope·negative=result).
- 🐞 **부수 correctness fix**: `rho_axon.rho_fan` 이 `falsi_fn(o)`(1-arg) 호출했으나 `_rho_fan_is_falsifiable(text, known)`(2-arg) 이라 **coherent 출력이 kwr gate 통과하면 crash 하던 잠복버그** → `falsi_fn(o, known)` 로 수정(frozen 검출기 로직 불변, ρ·fan 축이 실제 모델 출력서 처음 작동). origin/main 은 mock 으로 재현 CRASH 확인.
- ✅ 자체테스트(torch-free·NO decode·internal subprocess `--selftest-rho-cells`): en dets IS-동일객체(words_fn/kwr_fn/ngram_fn/corpus_tokens/gate 0.70)·ko dets uni-라우팅·ko 토큰 non-empty·kwr_ko gate 적용·**aggregate axes with/without breakout byte-identical**·en_general cell ρ·form/leap/fan == aggregate = 49 checks PASS. 기존 rho_axon 11-check store/tether/self unit 도 green.

**verdict = code-live · WIRED**. BUT **engine-native ko reach NUMBER 는 ⑦ pool 303M ko/SNS decode 대기**(cross-machine·summer/aiden, mini 금지). 위 mock 렌더는 배선검증일 뿐 실 reach 아님.

## follow-on (배선 · 별 focused session)
~~① core/rho_fan.hexa 쌍둥이 + parity(#3133)~~ · ~~② _rho_fan_cells 4칸 + ko known-word(#3140)~~ · ~~③ per-cell dispatch(evaluate.py dets lang-keyed·rho_axon breakout)~~ · ~~④ KWR_KO_GATE frozen-first 사전등록~~ · ⑤ train.py per-cell CE 로그 ⑥ ARCHITECTURE.datasets[] 4칸 · **⑦ pool 303M ko/SNS reach 측정(cross-machine·잔여 terminal 관측 · $0 재학습無)**.

## ④ 착지 — KWR_KO_GATE frozen-first 사전등록
✅ **`KWR_KO_GATE = 0.20`** frozen(model-independent, 303M 채점 前). en 0.70(235k-dict lexicality)는 ko eojeol 토큰화엔 category error → ko 전용 josa-suffix **grammaticality** 프록시 kwr_ko(다른 물리량, a_scale_honest_scope). 도출: anima-corpus-ko-{general,sns} held-out 20k real(median kwr_ko **0.40**) vs garble null(byte-shuffle+random-hangul, near point-mass **0.0**·p95=0). 규칙=midpoint(neg_p95=0.0, pos_p50=0.40)=**0.20**(naive midpoint(pos_p5,neg_p95)→0.0 은 positive zero-tail 로 degenerate; median 앵커가 두 분포 사이 robust). gate 0.20 서 real 80.0% clear·garble 99.74% fail. **구현됨·미배선**(core/rho_fan.py+hexa `KWR_KO_GATE` 리터럴, 아직 scoring 미소비=③). **ko FALS 스코프 제외**(③이 gate 적용할 때까지). tune-to-green 금지=사후이동은 REJECT, 유일 합법경로=새 frozen-first H. prereg=state/frontier_round2_scout/KWRKO_GATE_prereg.md · 도출=kwrko_gate_derive.py(seed 4302, $0).

## artifacts
state/frontier_round2_scout/{FABLE_rhofan_splitter_design.md,KWRKO_GATE_prereg.md,kwrko_gate_derive.py} · core/rho_fan.py::{_rho_fan_words_uni,_rho_fan_cells,_rho_fan_ko_*,_rho_fan_ko_known_word_ratio,KWR_KO_GATE} · core/rho_fan.hexa(쌍둥이) · cli/evaluate.py::{_build_cell_dets,_g_content_ngrams_uni,_g_load_corpus_tokens_uni,eval_rho_axon,_selftest_rho_cells} · cli/rho_axon.py::{run_panel(cell_dets=),_run_cell,render_cells,rho_fan/rho_leap(cgate=)}
