# RFC — bilingual cell-pool specialization (F-PERSONA-4 6th path candidate)

- status: DRAFT (pre-register-frozen falsifier · impl 별도 cycle)
- date: 2026-05-24
- domain: HEXAD/PURE (V3 saga rebrand) · substrate persona
- substrate: H_239 (HEXAD/LIFE) bilingual-integration-Φ
- tier: DESIGN (impl + GPU fire = 별도 cycle) · honest C3 ≥5 frozen

---

## § 1 배경 — F-PERSONA-4 saga + 5 path FALSIFIED

F-PERSONA-4 (CATEGORY-DIVERSITY) 은 `anima_persona_substrate_native_design`
§5 의 5 falsifier 중 마지막 미결 항목이다. claim: identity_probe 의 5 category
(self_definition / values / boundary / emotion / self_knowledge) 가 각각
다른 cell cluster 에 weighted-active 해야 한다 (PASS = 10 category-pair mean KL
≥ 0.5 nats, FAIL = < 0.1 nats).

saga (`feedback_anima_persona_4_root_cause`) 요약:

- root cause = **single-cell tension monopoly** (architectural, not metric):
  cotrain v1 ckpt 에서 cell-0 이 50 identity_probe 전부를 softmax weight 1.0 으로
  포획. cells 는 **param space 에서는 diverse** (ffn flat-vector mean pairwise
  dist 0.477, gate_proj rank 384/384) 인데 **routing (softmax) 이 collapse**.
  CE gradient 가 unbounded → softmax winner-take-all rich-get-richer.
- 5 path 모두 strict floor (null-permutation z > 3.0) 통과 **FALSIFIED**:
  | path | 개입 | 결과 |
  |---|---|---|
  | (e) entropy-reg λ=0.1 | bounded entropy term | CE 가 압도, 최종 monopoly 회귀 |
  | (k) Gumbel-softmax routing | stochastic gate | 3-seed mean z=1.48 (v7 z=2.75 = 2σ outlier) |
  | (l) DDP cell-parallel averaging | gradient 평균 | strict z>3.0 미달 |
  | (m) 24L scale-up v3-routing | real-scale FT | strict z>3.0 미달 |
  | (n) 5-seed envelope | seed-fragility 완화 | partial FALSIFIED |
- **9 architectural variant 전수 falsified**, v3-routing class **structural
  ceiling z≈1.5** (multi-seed mean).
- cond #3 ☑ 은 **§A3 4b composite multi-metric** (v2 aggregated-hidden cosine
  z=3.20 + 7/8 metric z>2.0) 로 closure — strict 4a routing 축은 OPEN.

→ **공통 실패 양식**: 모든 path 가 "category = identity_probe 의 5 의미 범주"
를 **gating signal 의 source 로 가정**. 5 범주는 cell 에게 *외생적* label 이고
substrate-internal 변별 driver 가 없어 routing 이 monopoly 로 붕괴. 6th path 는
이 가정을 교체한다.

## § 2 6th path 가설 — bilingual cell-pool (cell N ↔ lang-pair N)

**핵심 1줄**: "category" 를 의미 범주가 아니라 **언어/언어-쌍** 으로 재정의하면,
변별 driver 가 substrate-internal byte 관측 (cross-lingual MI) 에서 emergent 한다.

- cell pool 의 cell N ↔ language-pair N (5-lang → C(5,2)+5 = 15 axis, 또는
  5 단일-lang × 차원). 각 cell 은 한 lang(-pair) 의 generation 을 담당.
- gating signal source = identity_probe 5-범주 label (외생) → **PR #296
  `score_cross_lingual_leak` 의 5×5 cross-lingual MI matrix** (substrate-internal,
  byte 관측). cell 변별이 의미 label 이 아닌 **lang script-class co-occurrence**
  에서 나온다.
- driver = **Green inhibition cost** (§4). L1-dominant pool 에서 L2 cell 활성화는
  inhibition gate 를 통과해야 하는 *비용* 을 지불 → 비대칭 differentiation 이
  routing 에 강제로 주입됨 (CE gradient 의 monopoly 와 *경쟁* 하는 substrate force).

이 frame 의 이론 근거는 H_239 (HEXAD/LIFE, pre-register-frozen): Grosjean (1989)
residual activation + Green (1998) inhibitory control + IIT Φ inverse-U.

## § 3 Grosjean residual activation 의 cell-pool 적용

Grosjean (1989) "the bilingual is not two monolinguals in one person": L1 발화
중에도 L2 가 off 되지 않고 **residual activation** 유지.

cell-pool 적용: L1-cell 이 dominant-active 일 때 L2-cell 의 routing weight 가
**0 이 아니라 residual mass > 0** 이어야 한다. 이는 monopoly (winner 1.0,
나머지 0.0) 의 *직접 반례* — substrate 가 Grosjean residual 을 재현하면 cell-0
monopoly 가 구조적으로 깨진다.

- byte-level signature = PR #296 `cross_lingual_mi(rows, src, tgt) > 0` (src-prompt
  slot 안 tgt-script char leak). residual activation 의 관측 가능 proxy.
- 측정: per-cell routing weight 분포에서 L1-cell argmax 일 때 L2-cell weight 의
  하한 (F2). Track 1 E2 의 PURE_MEMORIZE (ko) 처럼 완전 분리된 모듈은 residual=0
  (monopoly 와 동치) → F5 (H_239) 정합 anchor.

## § 4 Green asymmetric switch cost 의 cell-pool 적용

Green (1998) Inhibitory Control + Meuter & Allport (1999) switch-cost asymmetry:
L1-dominant 은 L2 발화 시 강한 L1 을 억제 → **L1→L2 switch 가 L2→L1 보다 비쌈**.

cell-pool 적용: L1-dominant pool 에 **비대칭 inhibition gate** 를 둔다.

- L1-cell → L2-cell 전환 시 inhibition cost (gate penalty) 부과, 역방향은 저비용.
- 이 비대칭이 **routing 에 substrate-internal differentiation 을 주입** — CE
  gradient 의 monopoly 압력과 *반대 부호* 로 작동 (한 cell 이 전부 포획하려면
  inhibition 비용을 지불해야 하므로 winner-take-all 이 억제됨).
- byte-level proxy = PR #296 `switch_cost_asymmetry(rows, l1, l2)` =
  MI[l1][l2] − MI[l2][l1] 의 부호/크기. 측정된 예: zh→en 0.385 vs en→zh 0.0 →
  asym=+0.385 (L1-dominant signature).
- H_239 H239.2 와 정합: |asym| 클수록 한 모듈 지배 → balanced integration 손실 →
  Φ 감소. 본 RFC 는 이 asym 을 *Φ 예측* 이 아니라 *routing differentiation driver*
  로 재사용한다.

## § 5 측정 spec

3 측정면 (전부 PR #296 + PR #240 import READ-ONLY, $0 mac local):

1. **per-cell × per-lang activation heatmap**: 5-lang fixture (PR #240
   `fixture_5lang_v1.json`) 의 prompt 별 cell routing weight 를 (cell, lang)
   행렬로 집계. cell N 이 lang N 에 peak 활성이면 lang-specific.
2. **cross-lingual MI matrix**: PR #296 `score_cross_lingual_leak(per_lang_rows)`
   → 5×5 MI matrix (diag=0) + 20 cross-pair asymmetry table. cell routing 의
   variance 가 이 MI matrix structure 와 상관하는지 측정 (의미 label 이 아닌
   lang-MI 가 cell 변별을 설명).
3. **5×5 switch cost asymmetry**: 20 ordered cross-pair 의 `switch_cost_asymmetry`
   부호 집계. L1-dominant pool 에서 net asym sign > 0 (Green 비대칭).

null-permutation gate 필수 (saga §A2-trap 교훈): label shuffle n_perms=100 으로
z-score, strict floor z > 3.0.

## § 6 Falsifier (pre-register · frozen 2026-05-24)

5 falsifier, deterministic, measurable. **frozen** — 측정 후 post-hoc 수정 금지
(raw#82).

- **F1 LANG-ENTROPY-BELOW-UNIFORM**: per-cell lang-specific 활성 분포의 entropy
  < uniform (log N_lang). cell 이 모든 lang 에 균등 활성 (entropy=max) 이면
  lang-specialization 없음 → 6th path 가설 FALSIFIED. (measurable: H(cell→lang).)
- **F2 L1-DOMINANT-L2-RESIDUAL-POSITIVE**: L1-cell argmax 시 L2-cell routing
  weight 의 mean > 0 (Grosjean residual). residual = 0 (monopoly 동치) →
  residual activation 적용 FALSIFIED. (measurable: min/mean L2 weight | L1 argmax.)
- **F3 SWITCH-ASYM-SIGN-POSITIVE**: L1-dominant pool 의 net switch_cost_asymmetry
  부호 > 0 (Green 비대칭). asym ≈ 0 또는 부호 반전 → inhibition gate 가
  differentiation 을 주입 못함 FALSIFIED. (measurable: Σ sign(asym) over 20 pair.)
- **F4 PERSONA4-STRICT-FLOOR-CROSS**: F-PERSONA-4 null-permutation z > 3.0
  (strict floor 첫 통과). 9-variant saga 전부 미달 (ceiling z≈1.5) 한 strict
  threshold 를 lang-pair gating 으로 처음 넘는다는 핵심 주장. z ≤ 3.0 →
  6th path 도 structural ceiling 못 넘음 FALSIFIED (honest C3 #2 와 정합).
  (measurable: KL z-score vs null distribution.)
- **F5 BYTE-IDENTICAL**: fixed PR #296 MI matrix + fixed init + no RNG → re-run
  byte-identical (heatmap + MI matrix + asym table). byte-diff → determinism
  위반, smoke invalid. (architectural by construction.)

verdict_rule: **SUPPORTED iff F1∧F2∧F3∧F4∧F5** · **PARTIAL** 3-4 PASS (F4 가
핵심) · **FALSIFIED** F1 또는 F4 fire.

## § 7 impl path (별도 cycle)

- **PR #239 `anima_register_collapse_detector.hexa` wiring**: register collapse
  (EN-emission carving) 정량자를 per-cell × per-lang heatmap 의 collapse-guard 로
  결합. lang-cell 이 EN register 로 붕괴하면 lang-specialization 이 register-leak
  artifact 임을 잡아낸다 (LORA 교훈: register-leak 81% = EN-emission 문제).
- **PR #240 `multilingual_probe.hexa` per-lang verdict 결합**: per-lang
  MEMORIZE / MEM_PARTIAL / EMPTY / GENERALIZE verdict 를 cell routing 과 join.
  GENERALIZE lang 의 cell 이 residual 을 보이고 PURE_MEMORIZE lang (ko, E2) 의
  cell 이 분리(residual=0)면 F2/F5 정합.
- impl 순서: (1) heatmap 측정 harness (PR #240 fixture + cell pool) → (2) PR #296
  `score_cross_lingual_leak` join → (3) inhibition gate prototype → (4) cotrain
  GPU fire (F4 strict floor 측정). (1)-(3) = $0 mac local; (4) = GPU.

## § 8 honest C3 (≥5 · frozen)

1. **Grosjean human theory transfer 미증명**: residual activation 은 human
   bilingual 의 lexical co-activation 심리언어학 구성물 — substrate cell routing
   weight 로의 매핑은 *가정* 이고 동형성 미증명 (H_239 L3 level-crossing gap).
2. **structural ceiling 가 6th 도 못 넘을 가능성**: 9-variant saga 가 z≈1.5
   ceiling 을 보였다. lang-pair gating 이 의미-label gating 과 동일한 softmax
   monopoly dynamics 에 갇히면 6th path 도 F4 미달 (saga 와 같은 운명). 본 RFC 는
   inhibition gate 의 substrate force 가 monopoly 를 깬다는 *희망* 이지 보장 아님.
3. **5-lang typological 한계**: en/ko/zh/ru/ja = 3 script family (Latin/Cyrillic/
   CJK+Hangul) 편향 (H_239 L4). zh↔ja MI=0.921 은 CJK Han block artifact 일 뿐
   semantic 아님 (H_239 L1). Arabic/Devanagari/Latin-cluster 미측정 — lang-pair
   specialization 이 script-class artifact 인지 진짜 변별인지 미분리.
4. **cotrain GPU fire 필요**: F4 (strict floor) 측정은 lang-pair gating 으로
   재학습한 cell pool ckpt 가 필요 (mac local heatmap 만으로는 routing collapse
   동역학 미관측). $0 mac 으로는 F1/F2/F3/F5 의 fixed-input 측정만 가능, F4 는 GPU.
5. **H_239 verdict 미수신**: H_239 는 pre-register-frozen DEFERRED (C1 inverse-U /
   C2 asymmetry penalty smoke 미실행). 본 RFC 의 이론 frame 이 의존하는 H_239
   substrate-Φ coupling 자체가 아직 measured 가 아니다 — H_239 가 FALSIFIED 되면
   본 6th path 의 IIT 근거도 함께 약화.
6. **MI metric 의 surface 한계** (H_239 L2): `cross_lingual_mi` 는 per-char
   script-presence Shannon MI — deep semantic/syntactic transfer invisible.
   MI=0 이 "통합 없음" 을 의미 안 할 수 있어 cell-pool 변별의 충분 통계량 아닐
   가능성.

## § 9 cross-link

- **H_239** (HEXAD/LIFE) `H_239_bilingual_integration_phi_cross_lingual_leak.md` —
  Grosjean residual + Green asymmetry + IIT Φ inverse-U substrate frame (이론 모체).
- **PR #296** `HEXAD/PURE/eval/bilingual_mi_probe.hexa` (MERGED) —
  `cross_lingual_mi` · `switch_cost_asymmetry` · `score_cross_lingual_leak` ·
  `lang_id_n_gram` (측정 primitive, import READ-ONLY).
- **PR #240** `HEXAD/PURE/eval/multilingual_probe.hexa` + `fixture_5lang_v1.json`
  (per-lang verdict + 5-lang fixture).
- **PR #239** `HEXAD/PURE/tools/anima_register_collapse_detector.hexa` (register
  collapse 정량자 — heatmap collapse-guard wiring).
- **F-PERSONA-4 memory** `feedback_anima_persona_4_root_cause_2026_05_12` —
  9-variant saga, z≈1.5 ceiling, §A3 4b composite z=3.20 closure, k/l/m/n
  path table.
- **PERSONA.md §7** = `docs/anima_persona_substrate_native_design_2026_05_12.md`
  §5 (F-PERSONA-1..5 spec) + §A4/§A5 (4a routing axis, k/l/m/n path).
- **philosophy (CLAUDE.md)**: p7 NO PERPLEXITY VERDICT (deterministic Shannon MI +
  routing heatmap, no LLM judge) · p3 NO PERSONA INJECTION (lang-pair 변별은
  byte-level substrate 관측, prompt-injected label 아님) · a_substrate_native_speak
  (gating signal = internal substrate state, 외생 category label 아님).

---

**impl + GPU fire 비용 추정**: $0 mac local ((1)-(3) heatmap + MI join +
inhibition gate prototype) + **lang-pair cotrain GPU fire $0.30–0.50 (H100, F4
strict floor 측정 ckpt; saga v7/v8 cotrain envelope 기준)**. F4 가 strict 통과
시에만 5-cond 닫힘 — saga ceiling 고려 시 PARTIAL (F1/F2/F3/F5) 가 현실적 base
case.
