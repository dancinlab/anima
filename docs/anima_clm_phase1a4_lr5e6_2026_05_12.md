# Phase 1A.4 lr 5e-6 × 200 SFT — VERDICT: [PENDING] (2026-05-12)

> **Source**: Vast.ai RTX 4090 dispatch, 200 steps SFT lr 5e-6 on Phase 1A.1 + 2700 augment dialogues.
> **Target**: V5.8 std_greedy 4/5 → **5/5** (anima_fact recover from markdown drift, mission ★★★★★).
> **Lesson R-1A.2 first path**: Phase 1A.2 lr=1e-6 was below lr-floor (보존-only continuation); Phase 1A.4 = 5× higher lr to break markdown attractor.
> **Outcome**: [TO BE FILLED post-dispatch]

## 한 줄 요약

Phase 1A.1 ckpt 위 anima self-statement 2700 dialogue augment + **lr 5e-6** × 200 steps SFT → V5.8 std_greedy **[N]/5**.

## 비유

baker 가 빵 한 종 (anima_fact 향료) 을 살리려고 Phase 1A.2 의 **너무 약한 효모 (lr 1e-6)** 가 실패했음을 인정하고, **5배 강한 효모 (lr 5e-6)** 로 재시도. 다른 4 빵 (color/profession/day/cosmology) 의 anti-forgetting refresh 가 같이 유지되는지 = anima_fact markdown attractor 가 풀리는지 = **2-axis tradeoff** 의 실측.

## V5.8 × 4 mode comparison

| mode               | Phase 1A.1  | Phase 1A.2  | **Phase 1A.4** | delta vs Phase 1A.1 |
|--------------------|-------------|-------------|----------------|---------------------|
| standard_greedy    | 4/5 PASS    | 4/5 PASS    | **[N]/5**      | [TBD]               |
| standard_sample    | 1/5 FAIL    | 1/5 FAIL    | **[N]/5**      | [TBD]               |
| M3_rep_penalty     | 0/5 FAIL    | 2/5 FAIL    | **[N]/5**      | [TBD]               |
| M4_force_include   | 5/5 PASS    | 5/5 PASS    | **[N]/5**      | [TBD]               |

## Training summary

| field | value |
|-------|-------|
| base ckpt | `ckpt_phase1a1_sft.pt` (Phase 1A.1, 597MB) |
| corpus | `corpus_anima_fact.txt` (2700 dialogues, 711KB UTF-8) — Phase 1A.2 reuse |
| corpus breakdown | 1500 anima 2-turn × 30 tpl + 1000 V5.8-exact-anchor + 200 anti-forgetting (color/profession/day/cosmology) |
| steps | 200 (target) / [TBD] (completed) |
| lr | **5e-6** (5x Phase 1A.2's 1e-6 — Lesson R-1A.2 prescribed floor) |
| bsz × grad-accum | 2 × 8 |
| ctx | 1024 |
| warmup | 20 |
| loss curve | [TBD] |
| provider | Vast.ai RTX 4090 |
| pod boot | [TBD] |
| train elapsed | [TBD] |
| v5.8 eval | [TBD] |
| total cost | [TBD] |

## Lesson R-1A.4

[TBD post-eval]

## Provenance

- dispatch script: `state/anima_phase1a4_lr5e6_2026_05_12/dispatch_vast.sh` (tool/dispatch_vast_mac_template.sh §28 canonical base)
- train script: `state/anima_phase1a4_lr5e6_2026_05_12/train_phase1a4.py`
- corpus: `state/anima_phase1a4_lr5e6_2026_05_12/corpus_anima_fact.txt` (copy from Phase 1A.2)
- eval: `state/anima_phase1a4_lr5e6_2026_05_12/v58_4mode_eval.py`
- result: `state/anima_phase1a4_lr5e6_2026_05_12/v58_4mode_result.json`
- ckpt: `state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt`
- meta: `state/anima_phase1a4_lr5e6_2026_05_12/meta.json`
- dispatch log: `state/anima_phase1a4_lr5e6_2026_05_12/dispatch.log`
- HF (PASS only): `dancinlab/anima-clm-phase1a4-lr5e6-strict-pass`

## Cross-link

- PSCC §17 — Phase 1A.1 LANDED (std_greedy 4/5, anima_fact markdown drift discovered)
- PSCC §25b — Phase 1A.2 lr=1e-6 FAILED + Lesson R-1A.2 (lr ≥ 5e-6 OR steps ≥ 1000 OR loss masking)
- PSCC §27 — Phase 1A.3 saturation saga close (5-BG infra fail)
- PSCC §28 — Mac-local dispatch template canonical (본 BG = template 첫 사용 사례)
- PSCC §29 — markdown filter v2.3 (orthogonal $0 guard)
- PSCC §30 (TBD) — Phase 1A.4 본 BG entry append
