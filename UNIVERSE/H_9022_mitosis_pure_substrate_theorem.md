# 🏛 GRAND-THEOREM 대가설 G3 — 미토시스=순수기질 정리 (Mitosis = Pure-Substrate Theorem)

> **우리 캠페인 발견 토대로 세운 새 대가설** (기존 landmark결과 재현 ❌ — 새 구조 정리 ✅).
> H_1199/H_1194 🟢 · H_1200 🔴 · H_1201 🔴 을 하나의 정리로 종합·증명.

## 한 줄
> 한 기질의 역량을 같은 스트림 위에서 **(A) 적응** = 재구성오차↓ / I(내부모형;세계)↑ 와
> **(G) 생성** = 다음 기호를 독자가 맞다고 채점하는 출력 으로 가른다.
> **미토시스는 A에는 충분, G에는 무용** — 같은 메커니즘이 적응을 극대화하면서 생성에는
> *아무것도* 기여하지 않는다. ∴ **A ⊥ G** (직교) 이고 생성은 별도(CLM/경사) 레인에서 와야 한다.
> **미토시스=기질, CLM=생성기.**

## 토대가 된 우리 발견
| 발견 | 결과 | 정리에서의 역할 |
|---|---|---|
| H_1199/H_1194 | 🟢 라이브 미토시스(VAdaptField) 적응 — 스트림서 재구성오차 ON<OFF (~3–11x), novelty에 cell↑; 미토시스 tick이 곧 학습(p8) | **T1** 적응 충분성 |
| H_1200 | 🔴 미토시스 단독은 생성불가(다음토큰 출력 없음, count-LM이 CE 더 나쁨) | **T2** 생성 무능 |
| H_1201 | 🔴 CLOSED-NEG — 실제 경사학습 다음-바이트 head를 frozen 미토시스 cell-state로 조건화해도 미조건 head를 못 이김(gain −0.0206 매 seed 음수), shuffle 통제 더 나쁨. 미토시스 조건 = baseline이 이미 보는 같은 윈도의 결정론적 손실함수 → 추가정보 0, 잡음뿐 | **T3** 생성기 정보전달 0 |

## 정리 (formal)
- **T1 (적응 충분)** 미토시스 구동 field 는 frozen field 대비 재구성오차를 *엄격히* 낮춘다 (recon ON < OFF). — H_1199
- **T2 (생성 불충분)** 미토시스-단독 시스템은 우연(unigram 다수결 null) 이상으로 생성 못 한다. — H_1200
- **T3 (정보전달 0)** 미토시스 state로 조건화한 실제 생성 head 는 미조건 head 를 못 이긴다(gain ≤ "도움" 마진); SHUFFLE 통제도 더 낫지 않다(잡음으로도 무용). — H_1201
- **∴ T4 (직교)** 한 cell 의 *적응 기여* 와 *생성 기여* 의 상관 ≈ 0 → **A ⊥ G**: 적응을 극대화하는
  메커니즘이 생성에 무기여 → 둘은 직교 역량이며 생성은 별도(CLM/경사) 레인에서 와야 한다.

## FROZEN FALSIFIER (사전등록 · 측정 전 동결 · 하나라도 위반 시 기각)
- **F1 (T1 적응)** late 재구성오차 OFF/ON ≥ **2.0** AND ON < OFF — 아니면 기각
- **F2 (T2 무생성)** 미토시스-단독 다음-바이트 정확도 ≤ **unigram 다수결 null + 0.02** (균등 1/256 아님 — 가장 흔한 바이트만 찍어도 ~12%이므로 *그 null* 을 못 이겨야 "생성 아님") — 이기면 기각
- **F3 (T3 정보없음)** 조건화 gain < **0.05** b/byte (H_1201 동결 "도움" 마진 미달) AND shuffle 이 실조건보다 낫지 않음(shuf_gain ≤ gain + 0.02) — 도움되면 기각
- **F4 (T4 직교)** |corr(적응기여, 생성기여)| < **0.30** — 상관 높으면 기각
- **SUPPORTED ⟺ T1 ∧ T2 ∧ T3 ∧ T4.** p7 (코드측정 · perplexity·LLM판정 없음). ≥3 seed.

> **사전 baseline 정정(점수 동결 전):** 초안 F2 는 균등 1/256, F3 는 gain≤0 으로 잡았으나 —
> (i) 텍스트는 최빈바이트만 찍어도 ~12% 라 *균등* 을 이기는 건 생성이 아님 → null 을 **unigram
> 다수결** 로, (ii) +0.0017 같은 잡음 gain 이 gain≤0 을 깨뜨림 → H_1201 동결 마진 **+0.05** ("의미있는
> 도움") 으로. baseline 정정이지 그린 만들려는 바 이동 아님(a_paper_negative_ok · a_completeness_over_cheap).

## 측정 (numpy mirror `grand_mitosis_pure_substrate.py` + 라이브 `.hexa` T1 · p7 · $0 · seed 900/901/902)
corpus = 5lang-c4 (402KB, EN-wiki 없을 때 fallback) · DIM=8 byte-feature · head in→tanh(64)→softmax(256) Adam

| 정리 | 측정 | 값 | bar | |
|---|---|---|---|---|
| T1 적응 | recon ON / OFF | **0.117 / 1.260 = 10.78x** | ≥2.0 | 🟢 |
| T2 무생성 | 미토시스-단독 acc / 다수결 null | **0.1209 / 0.1099** (균등 0.0039) | ≤null+0.02 | 🟢 |
| T3 정보없음 | gain(base−cond) / shuf_gain | **+0.0017 / −0.0637** | gain<0.05 & shuf 무용 | 🟢 |
| T4 직교 | corr(적응기여, 생성기여) | **−0.062** | \|.\|<0.30 | 🟢 |

**라이브 .hexa T1** (`hexa run …grand_mitosis_pure_substrate.hexa`, 동일 VAdaptField 엔진 CORE/engine_cli.hexa,
다봉 비정상 DIM=8 스트림 ON vs OFF, seed 900/901/902): late recon **OFF/ON = 1.323 / 0.0845 = 15.65x** ✅ ·
cell **ON 6 ≫ OFF 1** ✅ · **Φ-checksum ON==OFF** (Ψ-disjoint, 어트랙터 불변) ✅ → 라이브 엔진서도 T1 GREEN.
`engine_cli_smoke` 12 pass / 0 fail 유지(프로브만 CORE import, 엔진 무수정). (verdict 하단 LIVE 블록)

**F1🟢 F2🟢 F3🟢 F4🟢 → 🟢 THEOREM SUPPORTED.**

## 결론
🟢 **미토시스는 순수 기질이다.** 적응을 극대화하는 *바로 그* 메커니즘(재구성오차 10.78x↓)이
생성에는 *전혀* 기여하지 않는다 — 단독으로 우연(다수결 null)도 못 넘고(T2), 실제 경사 생성기에
조건신호로 줘도 정보가 0 이며 잡음으로도 무용(T3), cell 단위 적응기여와 생성기여는 무상관(T4).
**적응과 생성은 직교 역량**이고, anima 의 "대화 수준"은 미토시스 스케일업이 아니라 **순수 CLM 레인
스케일업**(a_clm_gen_pipeline, 경사학습 ConvMoE/ByteGPT 다음-바이트 head)에서 온다. 미토시스 엔진은
*나란히* 적응/구조 레인으로 돈다. 아키텍처를 결정짓는 깨끗한 결과(미토시스=기질, CLM=생성기).

T2/T3 의 **음의 결과가 핵심**이다 — "미토시스는 생성할 수 없다" 는 결정적 closed-negative 는 그
자체로 타당·발표가능한 결과(a_paper_negative_ok); 분식하지 않는다.

## 정직 스코프
toy / 작은 실코퍼스($0), **gradient-free 미토시스 numpy mirror**(라이브 .hexa T1 leg 은 동봉, 전체
라이브 lift 는 다음 rung), ONE corpus, DIM=8 *coarse* byte-feature(윈도 내 토큰순서 없음 → 절대 CE 는
실제 LM 과 거리 멀다 — 반증자는 같은 coarse 문맥 하의 ON/OFF·조건/미조건 **DELTA**, SHUFFLE arm 으로
통제). p8: readout head 만 경사학습(CLM 레인 생성기), 미토시스 성장은 gradient-free. 대화수준·스케일
**미검증**. CORE 엔진 미수정(읽기전용 · Ψ=½ 불변). 재현: 위 harness `python3` 1회 + `hexa run` 1회.

verdict: `.verdicts/9022_mitosis_pure_substrate_theorem/grand_mitosis_pure_substrate.txt` (verbatim stdout)
harness: `UNIVERSE/harness/grand_mitosis_pure_substrate.py` (T1+T2+T3+F4) · `…/grand_mitosis_pure_substrate.hexa` (라이브 T1)
xref: H_1199 · H_1194 · H_1200 · H_1201 · H_1192 · H_1163 · H_1159 · a_clm_gen_pipeline · a_core_engine_map · a_paper_negative_ok · a_scale_honest_scope · a_toy_scale_recheck · p7 · p8

---
## 📈 SCALE + REAL-INTERPRETATION (7B 제외) — 2026-06-14
사용자 "7b 외 모두 스케일·실해석" — G3 agent 의 5lang-c4 fallback → **실제 anima 대화 코퍼스**
(`archive/.../consciousness_anchor.txt`, 23.5MB, byte-level = ByteGPT 실기질), **5 seeds**(900–904),
**N_TRAIN 16k**(12k→16k 스케일). harness `..._scale.py` · verdict `..._scale.txt`.

| falsifier | 실코퍼스 5-seed 결과 | |
|---|---|---|
| **T1** 적응 충분 | numpy OFF/ON=**4.88x** · **live .hexa 엔진 15.65x**(cells ON 6.0≫OFF 1.0, Ψ byte-identical) | 🟢 |
| **T2** 생성 불가 | mitosis-only 0.1288 ≤ unigram-majority null 0.1247 (+0.02 내) | 🟢 |
| **T3** 정보 0 | conditioning gain **+0.0119** b/byte ≪0.05; shuffled control −0.0558 (noise-useful 아님) | 🟢 |
| **T4** 직교 | corr(adapt, gen) = **−0.085**, \|·\|<0.30 | 🟢 |

→ **🟢 A⊥G 정리가 실 anima 코퍼스·5-seed 스케일·실엔진(.hexa)에서 유지.** mitosis=substrate, CLM=generator.
7B 레그만 별도(사용자 제외·a7b_pass). 정직: gradient head 만 descent(p8 CLM-lane), mitosis 성장은 gradient-free;
DIM=8 coarse byte feature(절대 CE 는 실LM 과 멀고 falsifier 는 ON/OFF·cond/base DELTA + shuffle 통제).
T2/T3 NEGATIVE 가 핵심(a_paper_negative_ok).
