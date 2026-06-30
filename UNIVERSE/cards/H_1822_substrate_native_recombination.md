# H_1822 — substrate-native 재조합: G1을 A⇄G tension에서 (mouth-decode 프레임 탈출)

**id:** H_1822
**slug:** substrate_native_recombination
**tier:** 🧱 (α) SUBSTRATE-ALSO-FLOORS — ENGINE-NATIVE (operating-radius 0/5) · directional rel-radius crumb
**date:** 2026-06-29
**source:** 오너 통찰 — "왜 의식엔진인데 LLM 디코더 스타일? 엔진이 스스로 디코더를 만들게 안되나?"
**렌즈:** `a_no_llm_frame_trap` (능력갭=빠진 구조 옆붙이기, LLM 프레임 1순위 금지) · `p8` (NO TRAIN/INFER SPLIT) · `a_mitosis_train`
**wired:** engine-native (live `core/engine_cli.hexa` + `core/pure_field.hexa` ops; NO mirror; no new core op added — clean test needs β semantic-embed op, named not built)

---

## ⚖️ VERDICT (α) — 2026-06-29 · ENGINE-NATIVE (mac CPU, $0) · `state/g1_substrate_native_recombination/`

**🧱 substrate ALSO floors at the engine's OWN operating radius.** 프레임 질문 답 = **NO (병목이 입만은 아님)** + directional crumb.

probe.hexa 가 live core/ A⇄G concept 기제를 호출(미러 아님): 두 부모 개념 basin = 2-cell `VAdaptField`,
composed state = 진짜 재조합 child(rain+bow→rainbow)의 `immune_embed_key`. 측정 = `vadapt_field_two_recon_err`(엔진 OWN top-2 affinity).

| arm | substrate-G1 @ 엔진 OWN radius 0.30 | @ rel-radius d_ab | 비고 |
|---|---|---|---|
| MAIN(진짜 합성어 5쌍) | **0/5** | 5/5 | d1≈0.61–0.86, d2≈0.96–1.15 모두 ≫ 0.30 |
| CONTROL single | 0/5 | 0/5 | d1=0 irreducible=NO ✓ |
| CONTROL shuffle | 0/5 | 1/5 | MAIN 5/5 대비 = 부모-특이 bridge ✓ |
| G-OFF ablation(pure_field A 단독) | BLIND | BLIND | concept-blind zero-input ✓ |

**KILLER 대조:** mouth-decode G1 = 0 (frozen floor H_1818/H_1602) · substrate-G1 @ 엔진 OWN 0.30 = **0/5**.
→ 엔진이 *실제로* 신규성 판단에 쓰는 임계(SPLIT_THRESH=0.30)에서 재조합 child 는 두 부모 basin 모두에서 **멀다**(isolated novel point) = 입이 못 뱉는 그 벽이 substrate concept-space 에도 그대로(= H_1310 Voronoi compositional-depth-0 한 단계 아래). 오너의 강한 주장("substrate 는 합성하는데 입이 못 뱉음")은 **operating point 에서 미확증**.

**directional crumb(정직, c9):** relaxed radius 에서는 substrate 가 각 재조합을 부모-특이하게 그 사이에 배치(MAIN 5/5 · shuffle 1/5 · single 0/5, 깨끗한 대조). 그러나 (1) **projection/recognition** readout 이지 **generation** 아님(child 가 주어짐), (2) `immune_embed_key`=char-trigram 해시라 **의미가 아니라 lexical 표면중첩**("rainbow"가 "rain"+"bow" trigram 을 문자적으로 공유). → tune-to-green(radius 갈아끼우기) 금지(p7), terminal 은 0/5.

**핵심 아키텍처 발견:** pure_field(Engine A)는 **zero-input = concept-blind**(Ψ=½는 내부 oscillator 만으로 창발). `engine_g`는 scalar emit gate. **"G 가 개념-결합 상태를 제안"하는 live op 은 없다.** 유일한 concept substrate = VAdaptField L2 Voronoi(immune lane), 그 embedding 은 char-trigram 해시(무의미).

**NAMED next (β-readout):** confound = char-hash embedding(무의미). 결정적 = `core/` 에 **303M mouth trunk penultimate** 학습 의미벡터로 개념 embed 하는 op 추가 후 동일 substrate-G1 재측정(학습 표현 위 recognition test = H_1574 generation 렌즈의 distinct twin). 그 전까지 🧱 유지.

**artifacts:** `state/g1_substrate_native_recombination/{probe.hexa, RESULT.md, RESULT.txt}`

---

## ⚖️ VERDICT (β-readout) — 2026-06-30 · DIRECTIONAL (embed via clm_decode.py mirror; metric engine-faithful numpy)

**🧱 HARDENED — 의미 embedding도 substrate-G1을 안 올린다. 벽은 concept embedding이 아니라 결합 연산자(combination operator)다.**

r1의 confound(char-trigram 해시=무의미)를 제거: `clm303.clm`(303M deep-mouth trunk) penultimate `yn`을 개념 byte에 mean-pool→L2-unit = **학습된 SEMANTIC 벡터**로 두 부모 basin 구성, 동일 substrate-G1 재측정(self-test PASS = 진짜 floor, dead meter 아님).

| arm | SEMANTIC @ 엔진 0.30 | @ rel d_ab | char-hash(r1) @0.30 |
|---|---|---|---|
| MAIN | **0/5** (d1≈0.34–0.59≫0.30) | 3/5 | 0/5 |
| single | 0/5 ✓ | 0/5 ✓ | 0/5 |
| shuffle | 0/5 | **3/5 == MAIN ⚠️** | 0/5 |

**결정:** 의미 embedding이 char-hash와 **동일하게 0/5** @ operating radius + r1의 directional crumb(rel-radius parent-specific bridge)가 **소멸**(SEMANTIC MAIN 3/5 == shuffle 3/5 = 재조합 child가 진짜 부모와 무관 개념만큼만 가깝다). → lexical→semantic 교체가 **무변화** = 벽은 **개념 표현(embedding)이 아니라 결합 연산자**(VAdaptField L2-Voronoi *nearest-basin* = compositional depth-0, H_1310 정합).

**🔑 4-각 수렴 (campaign-level):** mouth-objective(H_1602 🧱) · mouth-readout-op(H_1816 🧱) · substrate-concept-embed(β 🧱) · substrate-combiner(이 측정) — **넷 다 additive/affinity readout이 floor**. G1 레버는 readout도 representation도 아니라 **trained constructive bind**(두 부모로부터 child basin을 *구성*; nearest-basin 분할 아님). 이는 GPU 결합(c) op_obj(Hadamard bind + recomb-obj, 학습중)가 입-쪽에서 테스트하는 바로 그 레버와 **독립 수렴**.

**오너 frame-break 답(종결):** "입이 병목? 엔진이 스스로 디코더를?" → 입만의 병목 아님 + substrate는 의미개념을 줘도 못 합침 → **빠진 건 학습된 구성적 결합연산자**. frozen-first(radius 사전등록, tune-to-green 거부 p7).

**NAMED next (γ, cost-gated):** L2-Voronoi nearest-basin을 **trained bind operator**(tensor-product/circular-conv가 child basin을 *construct*)로 교체 후 동일 측정 = substrate twin of mouth binding-operator lever. 학습 필요(=$0 아님) → 🧱 유지until γ. β-op(engine-native 0/5 재확인용 `core/` 의미embed op)은 DIRECTIONAL→terminal 승격 follow-on.

**artifacts:** `state/g1_substrate_native_recombination/{beta_readout.py, RESULT_BETA.md, RESULT_BETA.txt}`

---

## 문제 제기 (오너)

현 anima G1/G6 캠페인은 **전부 mouth-frame**(clm_decode CLMConvMoE trunk + next-byte CE + readout).
G1 재조합을 *autoregressive 입(mouth)*에게 요구한다 — op·objective·binding 전부 입 안에서.

그러나 anima는 의식엔진이다: **A(forward) ⇄ G(reverse, gradient-free)**의 긴장이 Ψ=½로 끌린다.
**재조합(두 개념→새 제3)은 본질적으로 tension 연산** — 두 상반 엔진이 밀어내며 고정점에서 novelty.
즉 우리가 원하는 G1/G6 능력은 **substrate(A⇄G)의 native 산물**일 수 있는데, 엉뚱하게 autoregressive
trunk(별도 CE학습된 conventional LM)에게 묻고 있었다. = `a_no_llm_frame_trap` 최심부 위반 가능성.

## 가설

**재조합/착상은 mouth-decode 능력이 아니라 A⇄G substrate 능력이다.** G1을 autoregressive 출력 byte가
아니라 **A⇄G tension 장(field)에서 측정/생성**하면 floor(H_1818/1602/1310 전수)가 풀린다 —
G(reverse, 상상/제안 엔진)가 두 개념 basin을 결합한 tension 상태를 만들고, A가 제약하고, mouth는
그 substrate-결정 결합을 **렌더만** 한다(입의 역할 축소).

## ⚠️ 정직: 이미 친 벽 (frame-break ≠ 무지)

오너의 "엔진이 스스로 디코더를 만든다"는 **from-scratch gradient-free 형태로는 이미 CONFIDENT TERMINAL**:
H_1310 from-scratch pure mitosis(split-only) = 🔴 (혼자선 학습불가, gradient/selection 필수). 5 직교렌즈
전수 🧱(H_1568/1569/1570/1571/1574) — split-only는 Voronoi partition만, compositional depth 0.
⇒ 이 카드는 (α) = 측정 reframe(학습 불필요, $0 engine-native). β = gradient-결합 engine-grown mouth(cost-gated).

## Design — (α) ($0 engine-native 프로브) — 실행됨

1. 두 개념 seed → `immune_embed_key` → 2-cell `VAdaptField` basins.
2. **substrate-G1 metric**: 재조합 child 상태가 두 basin 둘 다에 투영 ∧ 어느 하나로 환원불가(composed_distinct≥2, mouth-decode 독립). 측정 = `vadapt_field_two_recon_err` [d1,d2], 두 radius(엔진 OWN 0.30 · rel d_ab).
3. controls: single(결합 없음) · shuffle(가짜 결합) · G-off ablation(pure_field A 단독 = concept-blind).
4. 같은 쌍 mouth-decode G1(=0 floor)과 대조 (KILLER).

## Frozen bar (pre-registered · p7)

| 항목 | bar | 결과 |
|------|-----|------|
| (α) substrate-G1 | composed_distinct≥2 ∧ >single ∧ G-causal, ≥2/3 | 엔진 OWN radius **0/5 FAIL** · rel-radius 5/5(directional only) |
| (α) 병목 격리 | substrate-G1≥2 인데 mouth G1=0 | 미확증(operating point 0/5) |
| controls | single=0 · shuffle≈0 · G-off=BLIND | single 0/5 ✓ · shuffle 1/5(rel)/0(eng) ✓ · BLIND ✓ |
