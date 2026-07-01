# H_1813 TPR-EXPERT-WEIGHT (303M) — frozen pre-registration

> 한국어 prereg · frozen-first · tune-to-green 금지 · p7/c9. 작성 2026-06-28.
> 베이스: `state/1602_recomb_objective/trainer.py` fork (objective lever + additive
> `.clm` 경로 + savant/mitosis/4-cell/held-out) → N1 TLoRA expert-weight + N3 DBES
> 추가. 외부문헌 근거: `state/lit_binding_objective/RESEARCH.md` §6 (N1·N3·N6·N7·N8).

## 1. 가설

**G1 재조합벽 / G6 착상벽의 미탐색 구조 레버 = ConvMoE expert 의 *내부 weight 구조***
(readout 위치 아님). 우리는 이미 **곱셈 binding 을 readout 위치**에서 floor 냈다
(`exp3_303m` ARM-BIND: G1=0 ∧ G6 fals=0, bind NOT>ctrl, terminal floor — memory
`exp3-bind-g1g6-engine-native-floor`). 본 패키지는 *다른 위치* = expert *weight* 를
tensor-product 로 reparameterize(N1 TLoRA/TensorPoly, 2405.16671)하여, "구조적
(low-rank 텐서곱 = compositional) inductive bias 를 학습 weight 에 넣으면 재조합이
열리나"를 묻는다.

**Greff 결합가설(핵심):** binding operator 는 *학습 objective 와 결합*했을 때만 lift
한다(2012.05208 + Furrer 2007.08970 + Barin Pacela 2603.28744). 따라서 N1 단독뿐
아니라 N1 + 학습신호 보조(N7 dictionary-aux / N8 jamo teach)를 arm 으로 둔다.
objrun(H_1602) 우승 objective 는 `--objective` 로 *선택적 결합* (default ce_marginal
= standalone, objrun 미착륙이어도 발사 가능).

**N3 진단가설(인과 격리, 측정-only):** "재조합 안 됨 = expert 미분화?" — DBES
(2605.18523)로 expert 분화도(output 쌍 cosine 거리·router entropy·usage Gini)를
측정. G1 floor 가 expert collapse 와 동반하는지 격리(학습/그래디언트 0, cheap).

## 2. 단일변수(arm) — trunk·데이터·step·seed 동일, 구조 lever 만 다름

세 lever-arm + 1 control. 전부 **production additive readout**(Conv1d d→V) 유지 =
`.clm` engine-native by-construction OPEN (exp3 binding 의 BLOCKED 아님). TLoRA 는
직렬화 직전 dense conv weight 로 **materialize** → 엔진은 표준 expert 만 읽음.

- **`ctrl`** (대조군): production CLMConvMoE + plain CE. 표준 expert weight.
  → G1 FAIL 기대(=재조합벽 baseline). 분해능 기준선.
- **`tlora`** (N1 단독): expert conv weight = `Σ_r A_r⊗B_r⊗K_r` (+ dense base) +
  plain CE. rank R frozen=8, base ON. *구조 lever 단독* — Greff 가설이 맞으면
  단독은 약함 예상.
- **`tlora_dict`** (N1+N7): TLoRA + trunk penultimate L1 sparse-coding aux
  (Stop-Probing dictionary, λ frozen=1e-3). 학습된 dictionary = binding constraint.
- **`tlora_jamo`** (N1+N8): TLoRA + next-jamo-class aux head (SCRIPT 자모, λ
  frozen=0.3). 한국어 sub-character compositional teach signal.

> **objective 축(선택):** objrun 우승 objective 가 확정되면 `--objective <winner>`
> 로 위 4 arm 위에 결합(Greff 결합가설 직접 검정). 미착륙이면 ce_marginal 로 발사.

## 3. 통제 (ctrl / baseline)

- 4 arm **동일 trunk init seed · 동일 데이터 stream(gen seed 42) · 동일 step · 동일
  savant golden-zone 스케줄 · 동일 mitosis E2→E3 · 동일 additive readout**.
  유일 차이 = expert weight parameterization(+aux 항). 단일변수 격리.
- held-out val CE = **항상 plain marginal CE**(arm 무관, dt_ln-immune `F.cross_entropy`)
  = 일반화 metric. aux 항은 *train pressure* 만 바꾸고 measure 는 안 바꾼다.
- N3 DBES = ctrl vs tlora* 분화도 대조(분화 차이가 lift 와 동반하는지).

## 4. FROZEN bars (실행 전 사전등록 · 사후이동 금지 · tune-to-green 금지)

**주 측정 = G1 재조합 (engine-native terminal, a7b_pass / H_1129 def VERBATIM):**
어떤 k∈{2,3,4,5} 에서 `composed_distinct ≥ 2` **AND** `> max_single` **AND**
coherent(kwr≥0.50). seed-robust {7, 4302, 4303} majority ≥ 2/3.
- **terminal** = `.clm` → `python3 core/g_gates.py <clm> <corpus...>`(py 2-production,
  torch-free measurement path) 또는 `hexa run cli/anima.hexa -- eval <clm>`. 4 arm
  전부 additive → engine-native by-construction 열림.
- torch-probe gauge(`gauge_lib`, trainer summary `gauges_g1g6_torch_probe`) =
  DIRECTIONAL monitor only(a_engine_native_learning).

**보조 측정 = G6 착상 ★ (engine-native):** `dist≥5`(pairwise Jaccard<0.5) AND
`≥1 falsifiable`. (N8/N7 가 G6 도 움직이는지.)

**무결성 게이트:** 4-cell held-out val CE DESCENT(val_CE < ln256=5.545) per register.
NO-DESCENT arm 은 overfit/broken → verdict 박제 금지(a_savant_train/a_clm_gen_pipeline).
post-serialize `verify_clm_v2.py descent <clm> <heldout>` PASS 필수.

**N3 DBES (측정-only, terminal 아님 = 진단):** ctrl 의 expert_div / usage_gini 를
G1 floor 와 대조. (분화 진단 — verdict 가 아니라 인과 격리 보조.)

## 5. 예측 (frozen)

- **P1 (Greff 결합가설 SUPPORT):** `tlora_dict` 또는 `tlora_jamo` 의 G1 >
  `ctrl` 의 G1 (seed-robust majority ≥2/3, strict 우위) AND 그 arm held-out DESCENT
  무결 → expert-weight 구조 lever 가 *학습신호와 결합* 시 재조합 레버.
- **P2 (N1 단독 약함 예상):** `tlora`(N1 단독, plain CE) 는 ctrl 과 ≈ → operator
  단독으론 안 열림(readout-floor 와 일관, Greff 결합가설 확증).
- **P3 (N3 진단):** ctrl G1 floor 가 낮은 expert_div(미분화)와 동반 → 미분화가
  재조합 병목의 한 원인; tlora* 가 expert_div 를 올리며 G1 도 올리면 인과 사슬 시사.

## 6. 반증조건 (NOT-SUPPORTED = honest negative, c9)

- **모든 arm G1=0 (floor):** expert-weight 구조 lever 가 (이 train scale 에서)
  재조합벽 못 움직임 = honest negative. **floor 면 INCONCLUSIVE-at-floor 정직
  라벨**(arm 간 분해능 0, clean refute 아님; readout-floor precedent 와 동급 처리).
- **tlora* ≈ ctrl (G1 동일):** expert-weight TPR 무관 = honest negative.
  → G1 레버 = expert *구조* 도 아님 (trunk objective 단독으로 회귀 = g1-lever
  다중렌즈 종결 강화).
- **DESCENT FAIL:** 그 arm 은 broken/overfit → 측정 무효(재학습, verdict 금지).
- bar 사후 이동·재조합 def 변경·detector 튜닝 일절 금지(p7). negative 도 박제.

## 7. seed / 매트릭스 (frozen)

- seeds = **{7, 4302, 4303}** (exp3/objrun 과 동일 = 비교가능).
- 매트릭스 = {ctrl, tlora, tlora_dict, tlora_jamo} × {7, 4302, 4303} = **12 run**
  (objective=ce_marginal default).
- fallback(예산초과) = {ctrl, tlora_dict, tlora_jamo} × 3 seed = 9 run
  (tlora 단독은 seed7 1회 — P2 는 1-seed directional 로 충분).
- objrun 결합 검정(선택, objrun 착륙 후) = 우승 objective 로 {ctrl, tlora_dict} ×
  3 seed 추가 6 run. 매트릭스 채택은 RESULT.md 명시(사후 bar 이동 아님 — 범위만).

## 8. 엔진-네이티브 / 정직 규율 (a_engine_native_learning · c9)

- terminal verdict = `.clm` → `core/g_gates.py`(torch-free) / `cli/anima.hexa eval`
  만. trainer 의 torch gauge = DIRECTIONAL.
- TLoRA materialize → dense conv weight → serialize_v3 → engine 은 표준 expert 만
  로드(reparameterization 은 *학습 방식*만, 추론 op 동일 = engine-transform-to-fit).
- ckpt(.clm + .pt + .json) teardown 전 영구 PULL(a_fire_recover_complete).
- grep self-check: `grep -lE 'import torch|gauge_lib|numpy' core/g_gates.py` 비어야
  terminal. (`clm_decode.py` 의 numpy = py 2-production 허용 math lib, torch-mirror
  아님 — 코드 주석 명시.)
