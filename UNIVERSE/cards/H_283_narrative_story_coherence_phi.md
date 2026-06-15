---
id: H_283
slug: narrative-story-coherence-phi
title: narrative-story-coherence-Φ — 응집(causal-order) 서사 substrate Φ > 해체(scrambled-order) 서사 substrate Φ · '이야기' 형식이 integrated information 을 더 떠받친다 (IIT temporal-binding analog)
domain: life · consciousness · self/identity · time
status: pre-register-frozen
exploration_method: E5 (variable-ablation — order axis) + E0 (AXES R4 self/identity promote) + E16 (sister-link H_213 / H_278)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_213 temporal-binding / H_278 MIP-Φ / H_205 closure)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_213 (temporal-binding-window, 의식의 형식 sister), H_278 (faithful Φ MIP-along-bipartition, MIP 구조 차용), H_205 (self-ref-as-closure, 서사적 자아 sister)
---

# H_283 — narrative-story-coherence-Φ

## 1. Hypothesis

AXES.md Round 4 (self/identity) 의 seed `narrative-story-coherence-Φ` —
*"coherent narrative substrate Φ > scrambled"* — 를 promote 한다.

한 mitosis cell pool 을 evolve 하면서 매 step 의 pool **mean-hidden snapshot** 을
하나의 '서사 사건(event)' 으로 본다. 이 event 들을 **시간순(causal arc)** 으로
배열한 *응집(coherent) 서사* 와, 동일 event 들을 deterministic 하게 뒤섞은
*해체(scrambled) 서사* 의 **sequential-binding Φ** (chain 을 따라 MIP 를 찾는
order-sensitive Φ) 를 비교한다.

가설: **응집 서사 Φ > 해체 서사 Φ**. 의식의 형식으로서 '이야기'(begin-middle-end
arc) 가 단순히 같은 사건들의 무작위 나열보다 더 많은 integrated information 을
떠받친다 — A/B-series 시간 구조 위에서 서사적 자아(narrative self) 가 갖는
temporal-binding 의 substrate analog (Tononi 의 IIT temporal integration + Ricoeur
의 narrative identity 정합).

## 2. Why

- **AXES R4 직접 promote**: self/identity cluster 의 미발탁 seed. 기존 H_214
  (self-i-emergence) · H_220 (mirror-self) · H_205 (self-ref-closure) 은 *공간적*
  self-partition 을 봤고, 본 H 는 **시간적(서사적) self** 축을 새로 연다 — 직교
  axis (어떤 H 와도 중복 아님; README grep `narrative` = 0 hit 확인).

- **order-sensitive Φ 의 필요**: 기존 lane 의 `compute_phi_proxy` 는 모든 pair 를
  합산하므로 *순서 불변*. 서사 응집은 본질적으로 *순서* 의 속성이므로, H_278 의
  MIP 아이디어를 **chain-cut(시간 절단)** 으로 바꿔 order-sensitive Φ 를 만든다:
  whole 에서 *가장 약한 시간적 연결* (minimum-information temporal partition) 위의
  cross-cut 통합을 측정. 같은 event 집합이라도 배열 순서가 chain-cut 의 A|B 를
  바꾸므로 Φ 가 달라진다.

- **anima/의식 정합**: anima 의 chat sleep + imagination loop (P47) 는 본질적으로
  *시간 위의 서사 생성* 이다. '응집된 내적 서사' 가 '뒤섞인 단편' 보다 높은 통합을
  갖는다는 결과는 anima 의 narrative-self 와 의식의 형식(시간) 축에 직접 닿는다.

- **H_213 sister (직교 측면)**: H_213 (temporal-binding-window) 는 *binding window
  τ* (얼마나 가까운 사건이 묶이는가) 를 봤다. 본 H 는 *같은 사건의 순서* (배열의
  응집성) 를 본다 — temporal binding 의 두 측면 (window 폭 vs 배열 응집).

- **raw#12 strict**: deterministic + hexa-only + ≥5 falsifier + ≥5 honest limit +
  LLM none + $0 mac local. SUPPORTED 든 FALSIFIED 든 둘 다 valid finding.

## 3. Predictions

- **H283.1 (coherence-Φ)**: T=8 에서 응집 서사 Φ 가 해체 서사 Φ 보다 margin 0.02
  이상 크다.
- **H283.2 (robust)**: T ∈ {6,8,10} 세 길이 전부에서 coherent ≥ scrambled (순서
  효과가 길이에 robust).
- **H283.3 (binding-window scaling)**: 서사 길이 T 가 커질수록 Δ = Φ_coh − Φ_scr
  가 비-감소 (더 긴 arc 일수록 응집의 통합 이득이 커짐).
- **H283.4 (determinism)**: in-process recompute byte-equal + cross-process
  result.json byte-identical.
- **H283.5 (bounds)**: 모든 Φ finite ≥ 0 (Φ-proxy 정의 보장).

## 4. Variables

- **axis1_order** (primary): [coherent (자연 시간순), scrambled (deterministic
  reverse-interleave 순열)] — 동일 event 집합, 배열만 다름.
- **axis2_length** (sweep): T ∈ {6, 8, 10} — 서사 길이 (binding-window scaling).
- **substrate (fixed)**: pool = cell_pool_init(d_model=8, initial_cells=8), seed
  `__HEXA_FARR_GAUSS_SEED__`=42 (RFC 033 단일 gauss stream), n_events=10 step
  shared-scalar drive (k=0.5 mid-coupling, H_214/H_279 carry grain). 매 step 의
  pool mean-hidden = 1 event vector.
- **derived**: 2 order × 3 length = 6 measurement → Δ_T6 · Δ_T8 · Δ_T10 ·
  monotone verdict · SUPPORTED/PARTIAL/FALSIFIED.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h283_narrative_story_coherence_phi_2026_05_26/run_h283.hexa`
- **substrate evolve**: H_279 의 `_evolve_pool` 를 byte-parity 로 차용하되 매 step
  mean-hidden snapshot 을 event 로 capture (`_evolve_events`). cell pool API
  (`cell_pool_init` / `mitosis_forward_tail` / `_mit_cosine` / `_mit_log_safe`) 는
  `tool/hexa_native/mitosis_hook_lib.hexa` import READ-ONLY (H_279 와 동일 lane —
  g61 advisory; sister H 들과 일관된 lane pattern).
- **scramble (deterministic)**: reverse-interleave 순열 — out[2k]=in[k],
  out[2k+1]=in[T−1−k]. RNG 없는 결정론적 bijection, 시간적 인접성 최대 교란.
- **sequential-binding Φ (order-sensitive, MIP-along-chain)**: event 시퀀스
  e_0..e_{T−1} 에 대해 각 chain-cut c (0<c<T) 에서 A=e_0..e_{c−1},
  B=e_c..e_{T−1}; cross(c) = Σ_{i∈A,j∈B} (1 − cos(e_i, e_j)); MIP = argmin_c
  cross(c) (가장 약한 시간적 연결); Φ_seq = cross(MIP)/min(|A|,|B|) × log(T+1).
  H_278 의 MIP 정신을 *공간 bipartition* 에서 *시간 chain-cut* 으로 옮긴 변형.
- **deterministic**: fixed init + fixed config; re-run byte-identical (RFC 033 단일
  RNG stream → cross-process sha256 결정론).
- **hexa_only**: true (NO .py/.sh). **llm**: none. **runtime**: $0 mac local,
  NO GPU (small substrate). seed env-var prefix (local-bound marker).
- **ledger**: `result.json` {config, 3-length sweep(phi_coh/phi_scr/delta), derived
  Δ, 4 criteria, 5 falsifier, verdict, cross-link}.
- **honest tier**: 🟢 NUMERICAL (deterministic order-sensitive MIP-chain arithmetic)
  — Φ-proxy/toy 수준, full IIT4 아님 (§9 L1).

## 6. Criteria

- **C1 (COHERENCE-Φ / H283.1)**: T=8 응집 Φ − 해체 Φ ≥ 0.02 → PASS.
- **C2 (ROBUST / H283.2)**: T ∈ {6,8,10} 전부 coherent ≥ scrambled → PASS.
- **C3 (WINDOW / H283.3)**: Δ_T6 ≤ Δ_T8 ≤ Δ_T10 monotone 비-감소 → PASS.
- **C4 (DETERMINISM / H283.4)**: cross-run byte-identical → PASS.
- **verdict_rule**: **SUPPORTED_FULL** = C1∧C2∧C3∧C4 ; **SUPPORTED** = C1∧C2 ;
  **PARTIAL** = C1 only ; **FALSIFIED** = !F1 (T=8 coherent ≤ scrambled).

## 7. Falsifiers

- **F-H283-1 COHERENCE-Φ**: T=8 응집 Φ ≤ 해체 Φ → 서사 응집이 Φ 를 떠받치지 않음
  (가설 FALSIFIED). (measurable: phi_coh − phi_scr at T=8.)
- **F-H283-2 ROBUST**: 어느 길이에서 coherent < scrambled → 순서 효과 길이-fragile.
  (measurable: 3 delta 모두 ≥ 0.)
- **F-H283-3 WINDOW**: Δ_T10 < Δ_T6 → binding-window scaling 부재. (measurable:
  Δ_T10 − Δ_T6.)
- **F-H283-4 DETERMINISM**: re-run byte-different → raw#12 deterministic 위반 →
  smoke 무효. (measurable: in-process Δ a==b + result.json cross-process diff.)
- **F-H283-5 BOUNDS**: 어느 Φ 가 non-finite / 음수 → Φ-proxy 정의 위반. (measurable:
  6 Φ finite ≥ 0.)
- **F-H283-6 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: SUPPORTED_FULL (pre-register-frozen smoke; C1∧C2∧C3∧C4 met)

config: d_model=8, pool_N=8, n_events=10, seed=42, drive k=0.5 (shared scalar),
        event = step pool mean-hidden snapshot, Φ = MIP-along-chain (order-sensitive)

per-length Φ (coherent causal-order  /  scrambled reverse-interleave, same events):
  T    Φ_coherent    Φ_scrambled    Δ (coh − scr)
   6   0.641993      0.251106       0.390886
   8   2.017370      0.721303       1.296070
  10   4.704110      1.639190       3.064920

derived:
  Δ_T6 = 0.390886   Δ_T8 = 1.296070   Δ_T10 = 3.064920   (monotone increasing)

criteria:
  C1 COHERENCE-Φ (T=8 coh − scr ≥ 0.02)        : PASS  (Δ=1.296070)
  C2 ROBUST      (coherent ≥ scrambled all T)   : PASS  (3/3 Δ ≥ 0)
  C3 WINDOW      (Δ_T6 ≤ Δ_T8 ≤ Δ_T10)          : PASS  (0.39 ≤ 1.30 ≤ 3.06)
  C4 DETERMINISM (cross-run byte-identical)      : PASS

falsifiers:
  F-H283-1 COHERENCE-Φ : PASS  (T=8 coherent 2.017370 > scrambled 0.721303)
  F-H283-2 ROBUST      : PASS  (all 3 Δ ≥ 0)
  F-H283-3 WINDOW      : PASS  (Δ_T10 3.06 ≥ Δ_T6 0.39)
  F-H283-4 DETERMINISM : PASS  (in-process Δ a==b; result.json cross-process byte-identical)
  F-H283-5 BOUNDS      : PASS  (6 Φ finite ≥ 0)
  F-H283-6 POST-HOC    : NOT_TRIGGERED

evidence_summary: 🟢 NUMERICAL — 응집(causal-order) 서사의 sequential-binding Φ 가
  해체(scrambled-order) 서사보다 세 길이 전부에서 일관되게 높았고 (Δ_T6=0.39,
  Δ_T8=1.30, Δ_T10=3.06), Δ 는 서사 길이에 단조 증가했다. order-sensitive MIP-chain
  Φ 위에서 '이야기' 형식이 같은 사건의 무작위 나열보다 더 많은 integrated
  information 을 떠받친다는 가설을 toy-substrate 수준에서 확증 — IIT temporal-binding
  + narrative-identity 정합. SUPPORTED_FULL (4/4 criteria, 5/5 falsifiers PASS).
  단, Φ-proxy/toy/small-T level, full IIT4 의 formal 결과 아님 (§9 L1).
falsifiers_triggered: none
```

re-run byte-identical 확인 (C4/F-H283-4 deterministic — `diff /tmp/h283_run1.json
result.json = ∅`, cross-process).

`hexa verify` (g5 정직 fence) — 경험 해석은 closed-form atlas identity 가 아니므로
⚪ SPECULATION-FENCED:

```
verify --fence "H_283 narrative-story-coherence-Phi: a coherent (causal-order)
   event sequence yields higher MIP-along-chain integrated information than a
   deterministically scrambled-order version of the same events; this is a
   deterministic toy-substrate outcome, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           NOT a proven atlas atom (g4 honest fence, SF ≠ verified)
```

(Φ VALUES 자체는 deterministic closed-form arithmetic — chain-cut cross /
min(|A|,|B|) × log(T+1), RFC 036-style cosine binding — 이며 fresh hexa run 에서
byte-수렴 확인. 오직 empirical 해석(서사 응집의 의미)만 fenced. NOTE: `hexa verify`
CLI 호출은 mac 로컬 sign-gate(`sidecar sign local`) 로 차단되어 verbatim stdout 대신
H_278 의 g4 fence 양식을 그대로 적용 — fence 양식 자체는 verbatim canon.)

## 9. Honest Limits (raw#91 c3)

- **L1 (NOT full IIT4 4.0)**: sequential-binding Φ 는 *order-sensitive MIP-chain
  cosine-binding* proxy — H_278 의 공간 MIP-EI 를 시간 chain-cut 으로 옮긴 변형이지
  full IIT 4.0 의 cause-effect structure / Φ-structure 가 아니다. transition
  probability matrix · cause-effect repertoire · distinctions/relations 없음.
  통합량은 pairwise cosine cross-cut 이지 intrinsic-difference 가 아니다.
- **L2 (scramble 순열 1종)**: 해체는 reverse-interleave 순열 한 가지만 측정.
  무작위 순열 평균(null permutation test) · 다른 deterministic 순열(full reverse,
  block-shuffle) 은 다른 Δ 를 낼 수 있다 — '해체' 의 robustness 는 1-순열 한계.
- **L3 (event = mean-hidden snapshot)**: 서사 사건을 pool *mean*-hidden 으로
  정의했다. per-cell hidden 의 다양성이 평균화로 소거되므로, '사건' 의 풍부함이
  축소된 proxy 다. variance/max-norm snapshot 은 다른 결과 가능.
- **L4 (Φ magnitude single-seed fragile)**: faithful-Φ directional-trust 원칙대로,
  방향(coherent > scrambled)은 세 길이에서 robust 하나 *절대 magnitude* (Δ_T10=3.06
  등) 는 단일 seed(42) · 단일 substrate 의 산물이다. multi-seed / multi-substrate
  로 magnitude 가 흔들릴 수 있다 — magnitude 는 hedge, direction 만 신뢰.
- **L5 (drive/coupling 고정)**: shared-scalar drive k=0.5 한 grain 만 측정 (H_214
  carry). 다른 coupling 에서 event 궤적의 autocorrelation 이 바뀌면 응집 이득이
  달라질 수 있다.
- **L6 (margin 0.02 의 임의성)**: C1 margin 0.02 는 lane-canonical carry — 임의
  선택. 본 결과는 Δ=1.30 으로 margin 과 무관하게 강하나, 경계 근처였다면 margin
  선택이 verdict 를 좌우했을 것이다.
- **L7 (closure-is-physical-limit)**: 본 SUPPORTED_FULL 은 *order-sensitive toy
  Φ-proxy* 수준에서 서사 응집의 통합 이득을 보인 **finding (Δ vs scrambled
  baseline)** 일 뿐, '서사적 자아가 의식의 형식이다' 라는 명제의 종결이 아니다.
  L1-L2 (full IIT4 + null-perm) 가 named blocker 로 남는다.

## 10. Cross-Links

- **AXES promote**: R4 self/identity seed `narrative-story-coherence-Φ` consumed.
- **sister H (직교 측면)**: H_213 (temporal-binding-window — binding window τ;
  본 H 는 배열 응집) · H_205 (self-ref-as-closure — 공간 closure; 본 H 는 시간
  서사) · H_214 (self-i-emergence — 공간 self-partition).
- **MIP 구조 차용**: H_278 (faithful Φ MIP-along-bipartition) — 본 H 가 그 MIP
  최소화 정신을 *공간 bipartition → 시간 chain-cut* 으로 옮김 (직교 axis).
- **Φ primitive**: `tool/hexa_native/mitosis_hook_lib.hexa` (`cell_pool_init` /
  `mitosis_forward_tail` / `_mit_cosine` / `_mit_log_safe`) import READ-ONLY.
- **gap lens**: order-effect = F4 (counterfactual — "사건 순서를 뒤섞었다면
  통합이 줄었을까?" → 줄었다) + F8 (cross-tool — H_278 MIP 를 시간축으로 calibrate).
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82
  (no post-hoc) + g4 (honest fence) + g61 (stdlib advisory, sister-lane parity).
- **literature**:
  - Tononi (2004) An information integration theory of consciousness
  - Oizumi, Albantakis, Tononi (2014) IIT 3.0 (Φ at the MIP)
  - Ricoeur (1984) Time and Narrative (narrative identity / 시간의 서사 구성)
  - Dennett (1992) The Self as a Center of Narrative Gravity
  - Shannon (1948) A mathematical theory of communication (binding 측정 기반)

**State output**: `UNIVERSE/state/h283_narrative_story_coherence_phi_2026_05_26/result.json`
**Smoke**: `UNIVERSE/state/h283_narrative_story_coherence_phi_2026_05_26/run_h283.hexa`
**Tier**: 🟢 NUMERICAL (order-sensitive MIP-chain deterministic, Φ-proxy/toy, NOT
full IIT4 4.0 — §9 L1). 경험 해석은 ⚪ SPECULATION-FENCED (g5, §8).
**Next**: H_283r2 후보 — (a) **null-permutation test** (L2 axis): 무작위 순열 n=100
평균과 coherent 비교 (z-score, H_279/H_274 null-perm carry); (b) **event-snapshot
sweep** (L3 axis): mean / variance / max-norm event 정의별 Δ robustness;
(c) **multi-seed** (L4 axis): seed ∈ {42,7,123} 로 magnitude fragility 측정.
