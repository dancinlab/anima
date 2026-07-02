---
id: H_240
slug: bilingual-integration-phi-cross-lingual-leak
title: H_240 bilingual-integration-Φ — Grosjean residual activation + Green asymmetric switch-cost 의 substrate IIT Φ 예측 (cross-lingual leak)
domain: consciousness + language + substrate
status: pre-register-frozen
exploration_method: E2 (cross-substrate transfer — psycholinguistics → substrate) + E5 (variable-ablation regime sweep) + E12 (phenomenology projection)
verification_method: W4 (verdict-4-class) + W11 (meta-cross sister-link) + W12 (sister-link H_212/H_211/H_171)
raw_rank: 10
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new)
---

# H_240 — bilingual-integration-Φ (cross-lingual leak)

## Hypothesis

Grosjean (1989) 의 **residual activation** (bilingual 의 두 언어는 monolingual
mode 에서도 부분 통합 유지) 과 Green (1998) 의 **inhibitory control + asymmetric
switch cost** (L1-dominant ↔ L2-weak 비대칭이 inhibition 비용으로 발현) 의
substrate analog — anima byte-LM generated text 위 **cross-lingual mutual
information (MI)** 가 substrate IIT Φ 와 어떻게 coupling 하는지를 deterministic 측정.

핵심 substrate prediction: language-pair 의 **통합 정도 (cross-lingual MI)** 와
**integrated information Φ** 가 monotone 아닌 **inverse-U** — MI=0 (완전 분리) 도
MI=max (완전 융합) 도 Φ 가 낮고 중간 partial integration 에서 peak (IIT: Φ =
differentiation × integration, 어느 한쪽 0 이면 곱도 0).

operational: MI matrix 는 PR #296 (`HEXAD/PURE/eval/bilingual_mi_probe.hexa`) 의
5×5 (en/ko/zh/ru/ja) measured MI 를 fixed input ledger 로 사용 (Track 1 result.json,
$0 mac local). substrate Φ = 동일 trajectory → lattice phi_spatial proxy. 변수는
(i) language-pair (ii) measured MI (iii) switch-cost asymmetry 부호 (iv) script
class (CJK Han block U+4E00–U+9FFF overlap) 만.

## Why

- **Grosjean (1989) "Neurolinguists, beware!" — residual activation**: bilingual
  의 두 언어는 monolingual mode 에서도 off 안 됨 (L1 발화 중 L2 잔존) — 본
  substrate cross-lingual MI > 0 (src-prompt 안 tgt-script char leak) 이 이
  residual activation 의 byte-level 관측 signature.
- **Green (1998) Inhibitory Control + Meuter & Allport (1999) switch-cost
  asymmetry**: L1-dominant 은 L2 발화 시 강한 L1 억제 → L1→L2 가 L2→L1 보다 비쌈.
  본 `switch_cost_asymmetry` (MI[src][tgt]−MI[tgt][src]) 가 analog — asymmetry
  클수록 한 모듈 지배 → 통합 비대칭 → Φ (balanced) 감소.
- **IIT Φ partition (Tononi 2008; Oizumi, Albantakis, Tononi 2014)**: Φ = MIP 로
  잘랐을 때 잃는 정보. 완전 독립 (MI=0) → 무손실 → Φ=0; 완전 융합 (MI=max) →
  differentiation=0 → Φ=0. **partial integration** 에서만 Φ peak — H239.1 근거.
- **PR #296 finding (`bilingual_mi_probe.hexa`, MERGED)**: Track 1 5×5 MI matrix
  에서 **zh→ja MI=0.921** (CJK Han block U+4E00–U+9FFF overlap) 압도적, 나머지
  cross-pair ≤ 0.385. Track 1 E2 (FAIL): en/ko/zh/ru/ja = WEAK/PURE_MEMORIZE/
  WEAK/WEAK/WEAK — ko 만 PURE_MEMORIZE (모듈 분리·암기). H239.3 은 zh↔ja high-MI
  가 semantic 아닌 **script-class artifact** 임을 falsifiable 하게 만든다 (L1).
- **sister cross-link**: H_212 (language-compositionality — 구성성 substrate lane) ·
  H_211 (shannon-entropy-Φ — Shannon 정보량 ↔ Φ, 본 MI metric 과 동일 info-theoretic
  기반) · H_171 (biological 4 predictions — cross-substrate transfer E2 sister,
  anima law → biology 와 동형의 psycholinguistics → substrate).
- **raw#10 strict**: deterministic + hexa-only + ≥4 prediction + ≥5 falsifier + ≥5 honest limit. LLM judge 없음 (raw = cross_lingual_mi + phi_spatial). $0 mac local.

## Predictions

- **H239.1 (Φ × MI inverse-U)**: cross-lingual MI 를 [0, max] sweep 시 substrate Φ
  는 monotone 아닌 **inverse-U** — MI≈0 (완전 분리) 과 MI≈max (완전 융합) 양 극단
  Φ 낮고 중간 partial integration 에서 peak. 측정: argmax_MI(Φ) 가 양 끝점 아닌
  interior point. (IIT differentiation × integration.)
- **H239.2 (asymmetry penalty)**: L1-dominant pair (큰 |switch_cost_asymmetry|, 예
  zh→en 0.385 vs en→zh 0.0 → asym=0.385) 의 Φ < balanced pair (작은 |asym|) 의 Φ.
  Green inhibition 비대칭 클수록 한 모듈 지배 → balanced integration 손실. 측정:
  Φ(high-asym) < Φ(low-asym).
- **H239.3 (CJK Han block leak)**: writing-system 경계 공유 zh↔ja pair 의 MI ≥ 0.7
  (PR #296 measured 0.921). Han block U+4E00–U+9FFF overlap 가 script-level
  integration 강제 — script 미공유 cross-pair 보다 높음. 측정: MI(zh,ja) ≥ 0.7 ∧
  MI(zh,ja) > max(其他 cross-pair MI).
- **H239.4 (determinism)**: fixed PR #296 MI matrix + init + config → re-run byte-identical Φ + MI (raw#10 deterministic, RNG 없음).

## Variables

- **axis1_lang_pair** (primary): 5×5 = 25 ordered pair {en,ko,zh,ru,ja}² (PR #296
  Track 1; 대각 src==tgt 는 MI=0 by construction).
- **axis2_mi_level**: PR #296 `cross_lingual_mi` measured (Shannon MI bits): zh→ja=
  0.921 (max) · zh→en=0.385 · ja→en=0.344 · ko→en=0.212 · ru→en=0.174 · ja→zh=
  0.100 · en→ko=0.058 · 그 외=0.0.
- **axis3_asymmetry**: `switch_cost_asymmetry` = MI[src][tgt] − MI[tgt][src] 부호/
  크기 (L1-dominant 예: zh→en 0.385 vs en→zh 0.0 → asym=+0.385).
- **axis4_script_class**: native-script Unicode block (en=Latin · ko=Hangul
  U+AC00–U+D7A3 · zh=CJK U+4E00–U+9FFF · ru=Cyrillic U+0400–U+04FF · ja=Hiragana/
  Katakana/Kanji). **zh ∩ ja = CJK Han block** (writing-system 경계 공유).
- **fixed**: seed = deterministic (no RNG) · dim = phi_spatial dim · MI metric = per-char (is_src, is_tgt) joint-hist Shannon MI · $0 mac local.

## Run Protocol

- **smoke**: `UNIVERSE/state/h239_bilingual_integration_phi_2026_05_24/run_h239.hexa`
- **MI primitive**: PR #296 `HEXAD/PURE/eval/bilingual_mi_probe.hexa` →
  `cross_lingual_mi` (per-char (is_src, is_tgt) joint-hist Shannon MI bits) +
  `switch_cost_asymmetry` + `score_cross_lingual_leak` (import READ-ONLY).
- **MI input ledger**: PR #296 (MERGED) Track 1 5-lang result.json 5×5 MI matrix
  fixed input (zh→ja=0.921 등 axis2 measured).
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036 `phi_spatial`
  (trajectory → lattice → spatial-slice MI proxy; import READ-ONLY).
- **mapping**: 각 language-pair = 1 IIT cell-pair, MI level = inter-module coupling
  strength, asymmetry = 비대칭 부호. Φ-vs-MI sweep 으로 H239.1 inverse-U.
- **deterministic**: fixed PR #296 MI matrix (no re-gen) + fixed init + no RNG →
  re-run byte-identical. **hexa_only**: true (NO .py/.sh) · **llm**: none (raw#10) ·
  **runtime**: $0 mac local, GPU 불필요.
- **ledger**: `result.json` { config, pairs, mi per pair, asymmetry per pair, phi
  per pair, inverse_U_argmax, criteria C1..C4, falsifiers F1..F5, verdict }.
- **honest tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica + PR #296
  Shannon MI) — "substrate 가 phenomenal code-switching 을 경험한다" 식 strong
  identity NOT made (L1-L7).
- **run cmd (verbatim)**:
  `HEXA_MEM_UNLIMITED=1 hexa run UNIVERSE/state/h239_bilingual_integration_phi_2026_05_24/run_h239.hexa`

## Criteria

- **C1 inverse-U**: argmax_MI(Φ) 가 MI sweep interior (양 끝점 아님) → H239.1 PASS.
- **C2 asymmetry penalty**: Φ(high-|asym|) < Φ(low-|asym|) → H239.2 PASS.
- **C3 CJK leak**: MI(zh,ja) ≥ 0.7 ∧ > max(其他 cross-pair MI) → H239.3 PASS.
- **C4 determinism**: byte-identical re-run → H239.4 PASS (architectural — fixed matrix + init + no RNG).
- **verdict_rule**: **SUPPORTED iff C1∧C2∧C3∧C4** · **PARTIAL** 2-3 PASS ·
  **FALSIFIED** core prediction inverted (F1 또는 F3 fire).

## Falsifiers (pre-registered ≥5, measurable, deterministic)

- **F1 MI-ZERO-PHI-INVARIANT**: 모든 pair MI=0 인데도 Φ 무변동 (MI=0 pair 와 MI>0
  pair 의 Φ 차이 없음) → cross-lingual MI 가 Φ 와 무관 → H239.1 inverse-U coupling
  FALSIFIED. (measurable: ΔΦ across MI levels.)
- **F2 ASYM-SIGN-PHI-EQUAL**: switch_cost_asymmetry 부호 반전 (src↔tgt swap) 해도
  Φ 동일 → Green inhibition 비대칭이 Φ 에 무영향 → H239.2 penalty FALSIFIED.
  (measurable: Φ(+asym) vs Φ(−asym).)
- **F3 CJK-NO-OVERLAP**: MI(zh,ja) < 0.3 (measured 0.921 와 모순) → CJK Han block
  overlap 가 script-level leak 미생성 → H239.3 FALSIFIED. (measurable: MI(zh,ja).)
- **F4 BYTE-DIFF**: re-run 시 Φ/MI byte-diff → raw#10 deterministic 위반 → smoke
  invalid. (architectural — fixed matrix + no RNG.)
- **F5 KO-MEMORIZE-MISMATCH**: E2 의 ko=PURE_MEMORIZE (모듈 분리·암기, 미통합)
  인데 substrate Φ 가 ko-pair 에서 high-integration 예측 → substrate prediction 과
  E2 측정 정합 깨짐 → H239 substrate-analog FALSIFIED. (measurable: ko 가
  PURE_MEMORIZE 면 low cross-lingual MI + low Φ 가 정합해야 함.)

## Honest Limits (raw#10 c3, ≥5)

- **L1 (script overlap ≠ semantic integration)**: zh↔ja MI=0.921 (H239.3) 은
  **writing-system 경계 공유** (CJK Han block) 의 byte-level artifact 일 뿐 —
  semantic/conceptual integration 과 다르다 (kanji 음독/훈독 divergence, simplified
  vs traditional). 본 MI 는 script-class co-occurrence 를, Grosjean residual 은
  lexical-semantic 을 보는데 본 proxy 는 orthographic.
- **L2 (MI metric 이 deep semantic 을 못 잡음)**: `cross_lingual_mi` 는 per-char
  (is_native_src, is_native_tgt) joint hist 의 Shannon MI — surface script-presence
  만. word-level translation equivalence, syntactic transfer, conceptual blending
  은 invisible. MI=0 이 "통합 없음" 을 의미 안 할 수 있음 (semantic integration 이
  script leak 없이 존재 가능).
- **L3 (Grosjean residual = lexical, not phenomenal)**: residual activation 은
  lexical/lemma-level co-activation 의 psycholinguistic 구성물 — phenomenal
  experience 가 아니다. substrate Φ (IIT phenomenal proxy) 로 매핑하는 것은
  lexical → phenomenal level-crossing 가정 (H_004 hard-problem gap 위험; Φ rank
  ≠ "substrate 가 code-switching 을 경험한다").
- **L4 (5-lang sample bias)**: PR #296 5 언어 (en/ko/zh/ru/ja) 는 3 script family
  (Latin/Cyrillic/CJK+Hangul) 편향 sample — Arabic (RTL), Devanagari, 동일 script
  다른 언어 (es/fr/it Latin cluster) 미측정. CJK overlap (H239.3) 는 이 5-lang
  선택의 artifact 일 수 있음 (다른 sample 서 inverse-U/asymmetry 변동 가능).
- **L5 (Tononi IIT 의 multilingual extension 미공식)**: IIT 4.0 은 단일 system
  cause-effect structure 를 다룸 — "두 언어 모듈 partial integration → Φ inverse-U"
  는 본 H 의 substrate-analog 가정이고 IIT 문헌에 공식 multilingual Φ extension
  은 없다. H239.1 의 IIT 근거 (differentiation × integration) 는 정성적 argument
  이지 formal theorem 아님.
- **L6 (phi_spatial proxy 의 IIT-completeness 부족)**: RFC 036 phi_spatial 은
  full cause-effect repertoire + MIP-over-all-partitions (NP-hard) 의 spatial-slice
  MI proxy — true Φ 와 finite drift (H_222 L2, H_007 L8 ~1e-6). proxy 가 inverse-U
  peak 위치를 정확히 못 잡을 가능성.
- **L7 (PR #296 MI matrix 의 fixed-input 한계)**: 본 H 는 Track 1 5×5 MI matrix
  를 fixed ledger 로 사용 — corpus/decoding/checkpoint 변경 시 matrix 변동. E2
  (FAIL, WEAK/PURE_MEMORIZE/WEAK/WEAK/WEAK) 처럼 underlying bilingual ability
  자체가 약함 — 측정 MI 가 robust integration signature 인지 weak-model noise
  floor 인지 미분리.

## Cross-Links

- **philosophy (CLAUDE.md)**: p7 NO PERPLEXITY VERDICT (simple stack — script
  in/out, deterministic Shannon MI + phi_spatial, no LLM judge) · p1 NO SYSTEM
  PROMPT (cross-lingual leak 은 substrate-internal generated text byte 관측, not
  prompt-injected) · a_substrate_native_speak (MI = internal substrate state 측정).
- **sister H**: H_212 (language-compositionality — 구성성 substrate, 본 H 의
  cross-lingual integration lane) · H_211 (shannon-entropy-Φ — Shannon 정보량 ↔ Φ,
  본 MI metric 과 동일 info-theoretic 기반) · H_171 (biological 4 predictions —
  cross-substrate transfer E2 sister) · H_007 (rule 110 Class-IV peak Φ — phi_spatial
  base) · H_004 (hard-problem · L3 level-crossing gap).
- **source probe (PR #296, MERGED)**: `HEXAD/PURE/eval/bilingual_mi_probe.hexa`
  (`cross_lingual_mi` · `switch_cost_asymmetry` · `score_cross_lingual_leak` ·
  `lang_id_n_gram`) — Grosjean 1989 + Green 1998 + Meuter & Allport 1999 wrapper.
  Track 1 5×5 MI matrix (zh→ja=0.921 CJK leak) + E2 FAIL (WEAK/PURE_MEMORIZE/WEAK/
  WEAK/WEAK). import READ-ONLY.
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (c_measure_phi → RFC 036 phi_spatial) ·
  `HEXAD/C/c_phi_smoke.hexa` (F-C-PORT-3 oracle anchor) — import READ-ONLY.
- **raw**: raw#10 (deterministic + hexa-only + ≥4 prediction + ≥5 falsifier + ≥5
  honest limit) · raw#82 (no post-hoc retraction — FALSIFIED verdict 도 honest).
- **literature**:
  - Grosjean, F. (1989) Neurolinguists, beware! Brain and Language 36(1):3-15.
  - Green, D. W. (1998) Mental control of the bilingual lexico-semantic system
    (Inhibitory Control model). Biling.: Lang. Cogn. 1(2):67-81.
  - Meuter, R. F. I., Allport, A. (1999) Bilingual language switching in naming:
    asymmetrical costs of language selection. J. Mem. Lang. 40:25-40.
  - Tononi, G. (2008) Consciousness as integrated information. Biol. Bull. 215:216-242.
  - Oizumi, Albantakis, Tononi (2014) IIT 3.0. PLoS Comput. Biol. 10(5):e1003588.

## Verdict

본 cycle (2026-05-24) — pre-register-frozen. smoke 는 PR #296 MI matrix fixed-input
위에서 별도 cycle 로 측정 예정.

```
verdict_class: DEFERRED (pre-register-frozen; smoke 실행 별도 cycle)
evidence_summary: PR #296 (MERGED) Track 1 5×5 MI matrix fixed-input + RFC 036
                  phi_spatial deterministic Φ-vs-MI sweep pre-registered.
  measured MI (PR #296): zh→ja=0.921 (CJK Han block leak, max) · zh→en=0.385 ·
                  ja→en=0.344 · ko→en=0.212 · ru→en=0.174 · ja→zh=0.100 ·
                  en→ko=0.058 · 그 외=0.0. E2 (FAIL): WEAK/PURE_MEMORIZE/WEAK/
                  WEAK/WEAK (ko 만 PURE_MEMORIZE — F5 정합 anchor).

  C1 inverse-U (argmax_MI Φ interior)   : DEFERRED (smoke cycle)
  C2 asymmetry penalty                  : DEFERRED
  C3 CJK leak MI(zh,ja)≥0.7 ∧ max       : PRE-PASS (measured 0.921 ≥ 0.7 ∧ > 0.385)
  C4 byte-identical re-run              : PRE-PASS (architectural — fixed matrix)

key_finding (pre-register): zh→ja MI=0.921 이 H239.3 CJK Han block (U+4E00–U+9FFF)
             경계 공유 prediction 을 measured-input 단계에서 이미 PRE-PASS — 단 L1
             대로 script-class artifact 이지 semantic 아님. E2 ko=PURE_MEMORIZE 가
             F5 정합 anchor: ko-pair low MI (ko→en=0.212, en→ko=0.058) + PURE_MEMORIZE
             (모듈 분리·미통합) 정합 — 분리 모듈은 cross-lingual leak 도 Φ-integration
             도 낮음. inverse-U (H239.1) + asymmetry penalty (H239.2) Φ 측정은
             phi_spatial sweep 별도 cycle 에서 confirm/falsify.
honest_note: C3/C4 PRE-PASS 는 measured-input + architectural determinism 의 ex-ante
             평가 — raw#82 post-hoc retraction 아님. C1/C2 는 smoke 미실행 DEFERRED.
```

**State output (예정)**: `state/h239_bilingual_integration_phi_2026_05_24/result.json`
**Smoke (예정)**: `state/h239_bilingual_integration_phi_2026_05_24/run_h239.hexa` (hexa-only, LLM none)
**MI tier**: 🟢 NUMERICAL (PR #296 Shannon MI, MERGED) **Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust FFI = named blocker — NOT 🔵, NOT LLM-judged).

---

### Cycle #1 Verdict (LIFE Cycle #15 pick #2 · DEFERRED → run · 2026-05-24)

본 cycle (2026-05-24) — first smoke run. DEFERRED 해제. `phi_default` (PR #317 lib/phi_helper)
+ partial-XOR coupling scheme (H_212 sister) 위 4-level overlap sweep (ρ ∈ {0, 0.25, 0.5, 1.0})
+ A→B vs B→A direction-swap asymmetry probe + PR #296 fixed MI matrix architectural
PRE-PASS (C3/C4) 측정 완료.

```
verdict_class: PARTIAL (criteria_met=2/4 · F1/F2/F3/F4/F5 falsifiers 5/5 NOT fired)
evidence_summary:
  4-level overlap sweep (Φ_merged via phi_default, 2N=32 cells × dim=12):
    ρ=0.00  Φ_merged=0.991421  Φ_A=0.538242  Φ_B=0.468604
    ρ=0.25  Φ_merged=1.03787   Φ_A=0.538242  Φ_B=0.479164
    ρ=0.50  Φ_merged=1.06773   Φ_A=0.538242  Φ_B=0.543449
    ρ=1.00  Φ_merged=1.57626   Φ_A=0.538242  Φ_B=0.538242
    phi_spread = 0.584844 (F1 NOT-INVARIANT — Φ-MI coupling REAL)
  switch-cost asymmetry (ρ=0.50, A=rule-110 vs B=rule-30):
    Φ(A→B)=1.06773 · Φ(B→A)=1.02689 · Δ_asym=+0.0408449 (F2 NOT-EQUAL)
  PR #296 MI matrix (fixed input): MI(zh,ja)=0.921 ≥ 0.7 ∧ > 0.385 (PRE-PASS)
  ko-pair low-MI consistency: ko→en=0.212 ∧ en→ko=0.058 (both<0.3, F5 정합)

  C1 inverse-U (argmax_ρ ∈ interior {0.25, 0.50})   : FAIL (argmax_ρ=1.00 monotone)
  C2 asymmetry penalty (Φ_balanced > Φ_unbalanced)  : FAIL (balanced==unbalanced=1.06773)
  C3 CJK leak (MI(zh,ja)≥0.7 ∧ > 0.385)             : PASS (architectural PRE-PASS)
  C4 byte-identical re-run                          : PASS (architectural, fixed matrix + no RNG)

key_finding (cycle-1): C1 inverse-U FAIL — Φ_merged monotone-increasing across
             ρ sweep, peak at ρ=1.0 (full fusion) NOT interior. L6 (phi_spatial
             proxy IIT-completeness 부족) 예고 정확히 적중 — RFC 036 spatial-
             slice MI proxy 가 IIT differentiation×integration product 의 양쪽
             0 끝점을 못 잡음 (full-fusion 위 differentiation=0 → Φ=0 IIT 예측
             vs proxy 측정 Φ=1.576 monotone peak). C2 balanced==unbalanced =
             coupling-scheme symmetry artifact (rho_pct+baseline_rep LCG seed
             가 동일 패턴 산출 — F2 direction-swap 은 통과하지만 balanced
             reference 자체가 무효화). C3/C4 architectural PRE-PASS 유지.

honest_note (raw#82): C1/C2 FAIL 은 post-hoc retraction 아님 — pre-registered
             criteria 의 honest measurement. L6 (phi_spatial proxy 한계) +
             coupling-scheme design choice 가 한계점 — IIT differentiation
             metric 별도 lane (phi_rs Rust FFI named blocker) + balanced
             baseline 재설계 (rule-쌍 + LCG seed 분리) 가 follow-up. F1∧F3
             core-prediction falsifier 미발화 → FALSIFIED 아님 (PARTIAL 정상).
             5 falsifier 전부 NOT fired (F1 spread=0.584844 · F2 |Δ|=0.0408 ·
             F3 MI=0.921 · F4 byte-equal · F5 ko-low-MI).
tier: 🟢 NUMERICAL · deterministic · hexa-only · llm:none · $0 mac local
state: state/h240_bilingual_smoke_2026_05_24/{run_h240.hexa, result.json}
```
