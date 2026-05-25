# Spike → 8-factor 매핑 — anima 자연발화 spike-grounding 룰북

> **implementation**: `HEXAD/CHAT/spontaneous_lib.hexa::apply_spike_features` (PR #143 squash `3bce310a1`)
>
> AKIDA spike-stream features 가 anima 의 8-factor motivation 에 어떻게
> influence 되는지 정의하는 룰북. 본 문서는 **Phase 1 HW-only** 스펙 —
> `[[AKIDA_FIRST]]` Phase 1/2 경계 준수, SW path 미포함.
>
> anchors: `HEXAD/CHAT/spontaneous_lib.hexa` (8-factor + §10 apply_spike_features SSOT) ·
> `HEXAD/CHAT/server/anima_participant.py` L95-122 (factor fn 정의) ·
> `HEXAD/NEUROMORPHIC/AKD1000.md` (chip 사양 + regime 분류) ·
> live ingest = broker `/akida/recent` (record schema 참조)
>
> 관련 sibling: `[[AKIDA_FIRST]]` · `[[REGIME_EXPANSION]]` ·
> `[[SW_CONDITION_DESIGN]]` · `[[PARTICIPANT_SPIKE_INTEGRATION]]` ·
> `[[akida_consumer]]` · `[[telemetry_harness]]`


## §1 — Available spike features (input side)

`akida_consumer.hexa` 가 매 tick 마다 broker `/akida/recent` 의 record
deque (maxlen=200, 각 record `{step, t_rel, n_spikes, spike_ids[16],
regime, thr[16], _bridge_ts}`) 를 window 단위로 reduce 해 다음 feature
dict 를 제공한다.

| feature | 정의 |
|---|---|
| `spike_rate_hz` | 최근 window (default 1.0 s) 의 total spike count / 윈도우 길이 |
| `regime` | window 내 record `regime` 필드의 mode (최빈 regime tag, 예 `R3_tonic_zero_input`) |
| `isi_cv` | window 내 record 간 t_rel inter-spike interval 의 변동계수 (CV = σ/μ) |
| `mean_spike_ids_count` | 각 record `spike_ids[16]` 의 nonzero 개수의 window 평균 |
| `last_step` | window 마지막 record 의 `step` |
| `n_records` | window 안 record 개수 (sparsity 판정용) |
| `regime_change` | 이전 window mode 와 현재 window mode 가 다를 때 true |


## §2 — Feature → factor influence matrix

8 factor (`factor_relevance` / `factor_info_gap` / `factor_curiosity` /
`factor_pain` / `factor_coherence` / `factor_originality` /
`factor_balance` / `factor_dynamics`) 별 spike grounding polarity.

| feature | factor 영향 (↑ / ↓ / neutral) | rationale |
|---|---|---|
| `spike_rate_hz` | curiosity ↑, originality ↑ | 높은 활성 = 환경 자극 / 탐색 신호 |
| `regime` | (overlay) | regime 자체는 §4 multiplicative modulator (행 단위 X) |
| `isi_cv` | curiosity ↑, coherence ↓ | irregular spike = surprise 신호, regular pattern 깨짐 |
| `mean_spike_ids_count` | info_gap ↑ | 동시 fire neuron 다양도 = 입력 novelty proxy |
| `last_step` | (no delta) | 현 impl 미매핑 — silence-as-fuel polarity 추정만, telemetry 후 §3 row 추가 검토 |
| `n_records` | (gate) | n_records < 5 일 때 본 매핑 전체 skip (under-sample 보호) |
| `regime_change` | pain ↑, originality ↑ | regime 전환 = substrate-level 큰 변화, Δ tension proxy |
| (substrate-only) | relevance | Φ (IIT 축) — substrate 내부, spike 무관 (impl pass-through) |
| (substrate-only) | balance | Φ vs ratchet 안전 게이트, spike 무관 (impl pass-through) |
| (substrate-only) | dynamics | spike 무관 pass-through — `last_step` 가 향후 후보 |


## §3 — Default deltas + thresholds (Phase 1 initial, evidence-pending)

각 row "Phase 1 initial — refined by telemetry harness evidence" —
`[[telemetry_harness]]` 가 누적한 correlation evidence 로 재조정.
refit advisory 산출은 `[[EVIDENCE_ANALYZER]]` §3 / §6 SSOT.

| feature | threshold | delta to factor | rationale |
|---|---|---|---|
| `spike_rate_hz` | > 12.0 Hz | curiosity += 0.10, originality += 0.05 | "활발" 임계 (R3 baseline 약 8-10 Hz 상회) |
| `spike_rate_hz` | < 2.0 Hz | curiosity -= 0.05 | "조용" 임계 (idle floor) |
| `isi_cv` | > 1.5 | curiosity += 0.08, coherence -= 0.10 | high CV = bursty/irregular |
| `isi_cv` | < 0.3 | coherence += 0.05 | low CV = metronome regular |
| `mean_spike_ids_count` | > 8 | info_gap += 0.10 | half of 16 ids 동시 = 풍부 입력 |
| `regime_change` | true | pain += 0.15, originality += 0.10 | regime 전환 = Δ tension event |
| `n_records` | < 5 | (gate) skip all deltas this tick | under-sample, noise 우려 |

모든 delta 적용 후 factor 값은 `[0, 1]` 로 clamp (§5 invariant).
숫자값 SSOT = `spontaneous_lib.hexa::apply_spike_features` body
(L298-L315) — 본 표는 prose form, 변경 시 양쪽 동기화.


## §4 — Regime overlay

§2/§3 의 per-feature delta 합산 위에 regime 별 multiplicative modulator.
`apply_spike_features` 마지막 step 에서 모든 factor delta 에 곱해진다.
Unknown / 신규 regime tag → modulator 1.0 (no-op, forward-compat).

| regime | modulator | rationale |
|---|---|---|
| `R3_tonic_zero_input` | 0.5 | tonic = 무자극 baseline, full delta 부적절 |
| `R1_oscillatory` | 1.0 | rhythmic baseline, default 적용 (placeholder) |
| `R2_bursting` | 1.2 | burst = substrate 활성 peak, delta 강화 (placeholder) |
| (unknown tag) | 1.0 | conservative no-op (forward-compat) |

R1 / R2 modulator 값은 R3 만 live 인 현 시점 placeholder —
`[[REGIME_EXPANSION]]` §7(c) verbatim 으로 telemetry 후 refit 대상
(refit pipeline = `[[EVIDENCE_ANALYZER]]` §3 `regime_modulator_observed`).
`HEXAD/NEUROMORPHIC/AKD1000.md` regime taxonomy 가 R3 외 확장될 때
본 표 1 row 추가 + `_spike_modulator` switch 1 branch 추가 (live tag =
`spike_streamer.py --regime R3`).


## §5 — `apply_spike_features` contract (signature + invariants)

`spontaneous_lib.hexa` §10 (L242-L328) impl SSOT, 본 §5 = mirror prose.

```
pub fn apply_spike_features(factors: dict, features: dict) -> dict
```

- **pure function** — no side effects, no global state, no IO.
- **input** — `factors` 는 8-factor dict (key = `relevance` / `info_gap`
  / `curiosity` / `pain` / `coherence` / `originality` / `balance` /
  `dynamics`, value ∈ [0, 1]), `features` 는 §1 schema.
- **output** — 입력과 동일 8-key dict, 값은 §3 delta + §4 regime
  modulator 적용 후 `[0, 1]` clamp 통과.
- **invariants**:
  1. output factor 값 ∀ key: 0.0 <= v <= 1.0 (clamp 보장)
  2. `features["n_records"] < 5` → output factor 값 == input clamp01 (sparsity gate)
  3. unknown regime tag → modulator 1.0, output 변형 = §3 deltas only
  4. input dict 미변형 (functional 보장 — 새 dict 반환)
  5. missing feature key = no delta (silent skip, not error)
- **non-goals** — emission decision 미관여 (motivation_score / should_emit
  은 `spontaneous_lib.hexa` 본체 §1-§9 SSOT 유지).


## §6 — Falsifiers (Phase 1 evidence-pending)

`[[telemetry_harness]]` 가 24 hr+ live recording 으로 다음 5 falsifier
를 평가. 1+ FAIL → §3/§4 표 revision.

- **F-SPIKE-MAP-1** — correlation(`spike_rate_hz`, anima emission count
  per same 1-min window) > 0.3 over 24 hr telemetry. 충족 시 curiosity
  ↑ polarity 검증.
- **F-SPIKE-MAP-2** — `regime_change == true` window 의 mean
  motivation_score 가 그 외 window mean 의 1.2× 이상. 미충족 시 §3
  regime_change delta 과대 추정.
- **F-SPIKE-MAP-3** — `isi_cv > 1.5` window 의 coherence factor 평균
  값 < 전체 window coherence 평균. 미충족 시 §2 polarity (coherence ↓)
  반대 방향.
- **F-SPIKE-MAP-4** — 24 hr 통계에서 R3 modulator 0.5 적용 후 R3
  window 의 spike-driven emission share 가 non-R3 window 의 0.4-0.6
  band 에 들어옴 (즉 0.5× modulator 가 emission rate 에 비례 반영).
- **F-SPIKE-MAP-5** — `apply_spike_features` 호출 1000 회 random
  features 입력 시 0% invariant 위반 (output 값 [0,1] clamp + dict key
  preserve). 본 falsifier 는 `HEXAD/CHAT/spike_apply_smoke.hexa` 가
  부분 cover.


## §7 — Honest C3

- (a) §3 delta 값은 초기 추정 — 0.05 / 0.10 / 0.15 단위는 `factor_*`
  fn 의 [0,1] 스케일을 의식한 보수치, telemetry 없이 absolute 정당화
  불가.
- (b) §3 threshold (`> 12 Hz`, `> 1.5 CV`, `> 8 ids` 등) tune 안 됨 —
  R3 만 live 인 현 시점에 R1/R2 baseline 미관측, threshold 일반화 보장
  X.
- (c) §4 regime modulator R1 / R2 는 placeholder — R1/R2 가 실제 HW
  에서 emit 되는 빈도 / 통계 미수집, 1.0 / 1.2 는 추측치.
  `[[REGIME_EXPANSION]]` §7(c) 와 동일 inheritance.
- (d) 일부 factor (`relevance` Φ, `balance` Φ-ratchet, `dynamics`) 는
  substrate 내부 변수 기반 — spike grounding 이 의미 없을 가능성 (§2
  에서 명시 substrate-only / pass-through). telemetry 가 `dynamics` 에
  음의 correlation 보이면 §2 행 추가 검토.
- (e) HW-grounded 매핑이 Phase 2 SW 모델 (`[[SW_CONDITION_DESIGN]]`)
  로 clean transfer 안 될 가능성 — SW simulator 의 spike statistics
  가 AKIDA HW 와 distribution mismatch 면 §3/§4 재유도 필요.
- (f) participant 통합 path (`akida_consumer.hexa` → factors →
  `anima_participant.py`) 는 `[[PARTICIPANT_SPIKE_INTEGRATION]]` impl
  + telemetry evidence 의존 — 본 문서는 룰북, executable wiring 은
  participant 측 cycle.
- (g) 본 매핑은 `a_substrate_native_speak` 의 "user 자극 → 즉답"
  금지를 spike 자극에도 동일 적용 — spike feature 는 motivation gate
  통과 후만 emission 으로 이어짐, 직접 trigger 가 아님 (`spontaneous_
  lib.hexa::should_emit` SSOT 유지).
- (h) §5 invariant set 은 F-SPIKE-MAP-5 random 1000 회 정도의 coverage
  — formal proof 아님, edge case (NaN feature value, regime 빈 string
  등) 별도 falsifier 미정.
