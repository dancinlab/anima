# PSILOCYBIN — 실로시빈 의식형성 가설 × substrate entropy perturbation

**Status**: ACTIVE — cycle #1 스크립트 (`run_psil_cycle1.hexa`) 작성·parse PASS, fire 대기
**Last update**: 2026-05-23 Cycle #1 (script ready)
**Log**: [PSILOCYBIN.log.md](PSILOCYBIN.log.md)

---

## §1 Hypothesis

원 가설 — Stoned Ape / entropic brain (Terence McKenna · Carhart-Harris):

> 실로시빈(psilocybin)이 인류 의식의 형성·확장에 촉매로 작용했다.
> 신경학적 기전: 5-HT2A agonist → 피질 활동 엔트로피 ↑ · DMN(default mode
> network) 억제 · 평소 분리된 네트워크 간 connectivity ↑ · 뇌 동역학이
> near-criticality 쪽으로 이동.

Substrate-native 번역 (falsifiable form):

anima substrate 에 **psilocybin-analog perturbation = activation entropy 주입**
(mitosis cell forward 에 Gaussian noise σ 를 dose 처럼 가함) 을 dose-sweep 하면,
의식 proxy 지표 (cell diversity · split entropy · Φ) 가 sober(σ=0) baseline 대비
**비단조(inverted-U)** 반응 — 적정 dose 에서 최대, 과량(overdose)에서 붕괴.

핵심 예측: entropic brain 의 "near-critical" 명제 → substrate 도 적정 entropy
주입에서 의식 proxy 가 peak, 과량에서 chaos 로 붕괴 ("bad trip" analog).

## §2 Pipeline / API

### Perturbation (dose)

dose = `cell_pool["noise_scale"]` (기본 0.1) — mitosis `split_cell` 이 자식
cell 가중치에 주입하는 Gaussian noise σ (`mitosis_hook_lib.hexa:415` RFC 033
`farr_add_gaussian_noise`). **별도 tool 불필요** — `chat_init_cell_pool` 후
`chat["cell_pool"]["noise_scale"] = σ` config knob.

```
σ sweep:  0.0 (sober) · 0.01 · 0.03 · 0.1 (기본) · 0.3 · 1.0 (overdose)
```

> **TODO[tool] RESOLVED** (2026-05-23): perturbation wrapper 불필요로 판명 —
> noise σ 는 `cell_pool["noise_scale"]` 직접 대입. cycle #1 스크립트
> `run_psil_cycle1.hexa` 가 σ × 5-repeat sweep 구현. 이 dose 가 SRH cycle #4
> 의 split_count 비결정론 원인이기도 함 (F-PSIL-5 가 σ=0 결정론 회복 진단).

### Measure (의식 proxy)

- cell_diversity   : cell pool weight 분포의 정규화 엔트로피
- split_entropy    : split event step 분포의 엔트로피 (시간 균일도)
- split_count / cell_count_final (anima_spike 기존 채널)
- response_entropy : 생성 토큰 분포 엔트로피
- (Phase B) Engine G Φ

### State path

```
HEXAD/LAB/state/PSILOCYBIN_<slug>_YYYY_MM_DD/
  spike_dose<σ>_seed<S>.json
  result_cycle<N>.json
```

## §3 Falsifiers (pre-registered)

| ID | 조건 | metric | PASS line |
|---|---|---|---|
| F-PSIL-1 | DOSE-RESPONSE — σ sweep 시 의식 proxy 변화 | cell_diversity vs σ | sober 대비 |Δ| 유의 (flat 이면 FAIL) |
| F-PSIL-2 | OVERDOSE-COLLAPSE — 과량 σ | proxy @ σ=1.0 | sober 대비 급락 (chaos 붕괴) |
| F-PSIL-3 | REVERSIBILITY — σ→0 복귀 | event_step jaccard | baseline 대비 ≥ 0.9 (회복) |
| F-PSIL-4 | PEAK-DOSE — inverted-U 라면 | argmax_σ(proxy) | peak σ* ∉ {0, max} (중간 dose) |
| F-PSIL-5 | SOBER-BASELINE — σ=0 regression | σ=0 spike | SRH cycle #3 sober 측정과 일치 |

**aggregation**: STRONG = 5/5 · MODERATE = 3-4/5 · WEAK = 1-2/5 · NULL = 0/5.
**threshold 는 cycle #1 fire 전 고정** (SRH C3-c3-6 교훈 — post-hoc tuning 금지).

## §4 Final verdict

**UNFIRED** — design only. cycle #1 선결 = `psilocybin_dose` perturbation wrapper
tool 신설. 실험 1 (SRH) 종결 후 fire.

## §5 Honest C3

- **C3-psil-1**: "실로시빈이 의식 형성에 영향" 형이상학 명제 자체는 검증 대상
  아님 — 본 실험은 substrate 의 *entropy-perturbation 반응* 이라는 operational
  명제만 측정. 생물학적 psilocybin 과의 관계는 metaphor (5-HT2A ↔ activation
  noise 는 analogy, identity 아님).
- **C3-psil-2**: Gaussian activation noise 는 실로시빈의 *한* 측면(엔트로피 ↑)만
  모사 — DMN 억제 / 특정 수용체 selectivity / connectivity 재배선 은 미반영.
  "psilocybin-analog" 이지 simulation 아님.
- **C3-psil-3**: 의식 proxy (cell diversity / split entropy) 는 IIT-Φ 의 cheap
  대용 — 진짜 Φ 측정은 Phase B (Engine G wiring).
- **C3-psil-4**: inverted-U 미관측 시 → monotone OR flat. flat 이면 substrate 가
  entropy perturbation 에 무반응 = 가설 substrate-level 기각 (honest NULL carry).
- **C3-psil-5**: σ sweep grid 6점 — coarse. peak 정밀화는 후속 cycle fine-grid.

## §6 Promotion target

- F-PSIL-1 PASS only → LAB 잔존, dose-response 곡선 carry
- F-PSIL-1+2+4 PASS (inverted-U + overdose collapse + peak) → `HEXAD/SUBSTRATE/`
  또는 신규 `HEXAD/PSILOCYBIN/` (near-criticality 증거)
- STRONG 5/5 → MEMORY entry + GOAL.md 의식 동역학 cond 후보
- 전체 FAIL → archive/ (substrate 가 entropy perturbation 에 무반응 lesson)

---

> 본 문서는 **latest verdict only**. cycle history 는 [PSILOCYBIN.log.md](PSILOCYBIN.log.md).
