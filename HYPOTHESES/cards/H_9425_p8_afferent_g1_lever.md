# H_9425 — p8-AFFERENT: 재조합을 학습이 아니라 **지각**시키면 G1 벽이 열리나 (미공격 레버 스펙)

- **group**: g1-interface-addressable-wall
- **date**: 2026-07-16
- **tier**: 🔵 **DESIGN / PRE-REGISTERED REFRAME** — 프런티어 재프레임 + 검정설계 · $0 DIRECTIONAL · **신규 decode 0** · not-terminal
- **surfaces**: `HYPOTHESES/cards/H_9425_p8_afferent_g1_lever.md` · `HYPOTHESES/HYPOTHESES.jsonl`
- **선행 정독**: [H_9359](H_9359_c3_transplant_en.md) 🧱🔑 runtime bridge absence · [H_9267](H_9267_xbind_corpus_measure_swap.md) 🟢 XBIND CRACK · [H_9327](H_9327_binding.md) 🧱 BINDING · [H_9304](H_9304_g1_earned_natural_operator.md) 🧱 DATA · [H_9422](H_9422_void_by_sealed_regime.md) 🔒 afferent channel 부재 · [H_9423](H_9423_two_store_native.md) 🔵 two-store co-train

## 왜 쐈나 — 두 결론이 같은 문을 가리킨다

**H_9359**(runtime bridge absence): BINDING/G1 벽의 정체 = **연산자 저장소와 선언 저장소 사이에
런타임 조회 다리가 없음**. hoc 담체는 `(어간)→답` 을 per-stem **동결 캐시**로 썼을 뿐(선언을 100%
뒤집어도 not-답 미동). "고치려면 런타임 조회 경로 자체를 만들어야 한다."

**H_9422**(void-by-sealed-regime): anima 는 **'귀 없는 입'** — percept = `wake_mem[tick,stage,cell_count]`
시계삼중항뿐. afferent channel 이 **구조적으로 부재**. escape = external percept(EEG a_eeg) = owner-gate.

두 결론을 겹치면 미공격 각도가 드러난다: **런타임 조회 다리의 부재 = afferent binding 의 부재.**
operator 와 declaration 을 **런타임 percept 로 co-present** 시키면, 재조합이 **학습 없이 '지각'**될 수 있나?

## 계보 증명 — 모든 G1 공격이 WEIGHT-LEARNING 이었다 (afferent = 0/5)

| H_ | 공격 방식 | 학습 채널 | 결과 |
|---|---|---|---|
| H_9304 | 자연 held-out 재조합 정보 측정 | (측정만 · CPT prior) | 🧱 DATA 벽 |
| H_9267 | 합성 XBIND corpus 20000-step 학습 | **CPT (weight)** | 🟢 held-out D-acc **1.000** |
| H_9327 | ground_keep CPT 로 사실 기입 | **CPT (weight)** | 🧱 BINDING |
| H_9359 | 2차 CPT 로 선언 뒤집기 | **CPT (weight)** | 🧱 동결 캐시 = bridge 부재 |
| H_9423 | store-조회 다리 **공학습** | **co-train (weight)** | 🔵 설계(미구현) |

**전부 가중치 공간 학습이다.** H_9267 이 held-out 재조합을 **완벽 학습**할 수 있음을 증명했으나(1.000),
그 신호는 CPT 로 **가중치에 구웠다**. p8("no train/infer split")은 학습이 **런타임 채널로 와야 함**을
요구한다 — 그런데 재조합 신호를 **런타임 afferent percept 로 전달**해 store 조회로 푸는 각도는
**한 번도 안 쐈다.** H_9423 조차 다리를 **공학습**한다(weight). afferent 런타임 주입 = **0/5.**

## 조작 (단일 변수 · CPT-free = p8-native)

H_9267 이 D-acc 1.000 을 낸 그 **operator+declaration pair 를, CPT 대신 chat-time afferent stream 으로
주입**한다. 가중치 갱신 0. 재조합이 런타임 store 조회로 '지각'되는지 store 의 D-acc 로 측정.

- **주입 경로**: afferent percept → 런타임 store(H_9336/9337 이 g_text content-read live 로 확증한
  ca3/해마 조회 저장소 — score-time 에 실제로 읽힘 · chat.py:1982). CPT 로 가중치에 쓰는 게 아니라
  **store 슬롯에 percept 로 얹는다**.
- **양성통제 (co-present)**: operator 행(`not {s}`)과 declaration 행(`{s} => pol`)을 **같은 afferent
  window 에 co-present**. 재조합이 지각되면 held-out 어간 D-acc ↑.
- **null (separated)**: 같은 두 행을 **분리된 window**(operator window ↔ declaration window 비인접/부재)로
  주입. co-present 만이 다리를 만든다면 null 은 chance(∈[0.38,0.62]).
- **판별력**: co-present − separated ≥ +0.20 ⟹ afferent binding 실재(런타임 다리). Δ≈0 ⟹ afferent
  주입으로도 재조합 미지각 = H_9359 벽이 학습채널 무관하게 **아키텍처 조회경로 부재**로 격상.

## 📐 계기 살아있음 선행 (positive-control-before-negative)

음성 읽기 전 **store 주입 자체가 D-acc 를 움직이는지** 먼저 확증(INSTRUMENT-DEAD 방어):
- **C0 ORACLE**: co-present window 에 **답을 직접** 얹으면 store readout D-acc ≥ 0.90 (주입→읽기 경로
  살아있음). < 0.90 ⟹ INSTRUMENT-DEAD 보고(H_9423 C0-e 선례: 혼합 readout 희석이 계기를 죽인다).
- **C0-leak**: separated null 에서 held-out 표면 누출 0(byte-identical 봉인).
- provenance: D-acc 필드 N_distinct > 1(죽은 게이지 아님 · H_9337 이후 경로).

## 판정 축 — 이 레버는 owner-gate 인가 v2-sandbox 선행인가

**production afferent channel 은 존재하지 않는다**(H_9422: '귀 없는 입'). 프로덕션에 afferent→store
배선을 심는 것 = **정체성 변경**(p1–p4 프레임 + a_eeg 승인 계열) = **owner-gate · 자율발사 불가**.

⟹ **v2-sandbox 선행이 정답이다**(rule-exempt · afferent 주입 자유 · positive-control-before-negative
선례 V2_1). v2 에서 afferent→store 주입 toy 로 co-present vs separated 를 스크린 →
**CRACK 시에만** core/ + `anima-py evaluate --afferent`(owner-gate) 로 포팅해 TERMINAL 자격.
v2 양성은 **영구 DIRECTIONAL ceiling**(v2/CLAUDE.md).

## 예측 (서명)

어텐션 없는 conv byte-LM 에 in-context 복사 경로가 없다는 것이 **아키텍처 진단이 아니라 측정된
부재**라면(H_9327 `a_no_llm_frame_trap`), afferent→store co-present 는 **두 갈래**로 갈린다:
① store 가 content-addressed 조회를 가지면(H_9336/37 live) co-present − separated ≥ +0.20 =
**런타임 다리 실재** → H_9359 벽이 "학습으로만 못 넘는 게 아니라 런타임 percept 로도 넘을 수 있다"로
반전(재조합 lane 재개방). ② Δ≈0 = afferent 로도 재조합 미지각 → 벽이 **학습채널 무관 · store 조회
경로 자체의 부재**로 격상(H_9359 최강 보강 · H_9423 공학습만이 유일 exit 확정).

## 이 카드가 벌어낸 것 (verdict — DESIGN)

🔵 **재조합 벽의 미공격 각도를 계보로 입증** + **cheapest 검정 스펙 동결**. G1 공격 5건 전부
weight-learning(CPT/co-train), afferent 런타임 주입 = **0/5**. p8("no train/infer split")이 요구하는
**학습-via-런타임-채널**을 H_9267 의 D-acc=1.000 신호에 처음 적용하는 설계. 판정: **v2-sandbox 선행**
(afferent 배선 = production 정체성 변경 = owner-gate · 자율발사 불가). **신규 decode 0.**

## 다음 (미탐)

v2 에 `afferent→store` 주입 toy 배선 → C0 ORACLE 게이트(≥0.90) → co-present vs separated 스크린.
CRACK ⟹ core/ 포팅 + owner-gate(`--afferent` 플래그 · a_eeg 계열 승인). null ⟹ H_9359 격상.
병렬: H_9423(공학습 다리)와 **직교** — H_9423=weight 다리, H_9425=runtime percept 다리. 둘 다 CRACK 시
"다리는 존재하나 학습으로만 서는가 percept 로도 서는가"를 가른다.
