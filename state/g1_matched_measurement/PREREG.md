# PREREG — H_6189 matched-surface + window-resident G1 re-measurement (frozen-first)

**측정 전 동결.** ckpt 첫 decode 이전에 이 파일 + probe_spec.json(sha) + gen_probe.py + 채점코드를 커밋. 이후 prompt/bar/scoring 변경 = 전체 DIRECTIONAL 강등(one-shot). 표준 canonical G1 gate는 FROZEN·FAIL 유지 — 이 probe는 그걸 뒤집지 않음(별개 artifact 가설 판정).

## 자산
- target: `clm303_deep_L8_cov.clm` (sha 2c565ad4)
- control(d) null: `clm303_clean.clm`(L4_clean, e807672) · `clm303_deep_L8_d2781.clm`(L8_nocov, 5777c50)
- probe: `probe_spec.json` sha256=`cf1efad4643ef9cc5337f18df94e0a2fd3e0c2e96212457e57a5b49319d28c2f` (gen_probe.py, design.json seed 6185)
- 354 items: heldout 240(fit 112)·seen 74(fit 58)·unary 40 · held-out 누출 0(블록 62,900줄 grep)

## 템플릿 (window arithmetic로 선택 · 문구 변경 금지)
- T0 `the {A} and the {B} yield ` (반례 form, ember+dune)
- T3 `each {A} with {B} turns ` (best window)
- T7 `a {A} met a {B}; they showed ` (worst = window-dose arm)
- unary `{A} brings ` (control b)
- window-fit = 첫 개념의 last-24byte 가시 suffix가 40-vocab서 유일 식별. ember/dune T0 = fit(visible 4/3).

## 채점 (offline · raw continuation서 재현)
- greedy(top_k=1) gen=40. attr 추출 = continuation서 첫 2개 attr-vocab 토큰(vocab substring-free라 무모호).
- both-strict = 추출 (attr(first), attr(second)) 순서일치. both-loose = 둘 다 존재. **primary = both-strict on fit cells.**

## FROZEN BARS
**validity gates (실패⇒측정 VOID, 판정 불가):**
- (b) unary: attr(A) 정확도 ≥ 0.80 (매핑 elicitable)
- (c) seen-pair(fit): both-strict ≥ 0.60 (elicitation 정합)

**verdict bars (validity 통과 시):**
- 🟢 **GREEN-of-artifact**: held-out fit both-strict ≥ 0.50 AND ≥ 0.7×seen AND permutation-null p<0.01 AND control(d) null 둘 다 chance. ⟹ "canonical G1=0 on L8-cov = 측정 artifact; held-out **additive** 재조합 engine-native at 303M 실재" (scope §additive 아래). frozen gate·H_9131 bind 천장 불변.
- 🔴 **KILL**: validity 통과 AND held-out fit ≤ permutation-null 95th pct ⟹ ember+dune는 fluke, 벽=genuine ceiling(matched+windowed서도 chance).
- 그 외 = INCONCLUSIVE.

**controls:**
- (a) permutation null: 같은 출력 1000 derangement 재채점 = 경험적 chance(자주-attr degeneracy 흡수). 모든 chance 주장 = 이 null 기준.
- (d) surface-form null: 동일 held-out fit prompt를 L4_clean·L8_nocov(coverage 미학습)서 decode → ≤ null 95th pct(템플릿·자연어 collocation 누출 동시 차단).
- 2차(보고만): order-swap consistency ≥0.7 → slot-binding, <0.7 → bag-additive.

## scope (정직)
- **literal copy 구조 배제**: prompt에 attr 바이트 0(programmatic assert)·zero-shot·T=24. control(d)가 "form이 답 함의" 채널 차단.
- **additive confound 제거 불가(이 ckpt)**: 코퍼스가 target을 두 unary(attr(A),attr(B)) 연결로 정의 = pair-dependent target 부재. ⟹ GREEN = "미노출 쌍 productive slot-filling"(진짜 조합 일반화, gate 측정오류 유죄)이나 **earned bind는 미검**(H_9131/γ 천장 유지). GREEN = 벽을 "재조합 0"→"additive 초과 bind 0"으로 **재-scope**(깨는 것 아님). earned-bind는 non-additive target 재학습(γ/H_1840, GPU-gated) 필요 = out of scope.
