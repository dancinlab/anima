# PURE Phase D `result.json` schema SSOT (2026-05-24)

> Phase D ckpt-bearing fire (`dispatch_p21h_v3.hexa`) 가 산출하는
> `result.json` 의 **단일 schema 참조**. PR [#355](https://github.com/dancinlab/anima/pull/355)
> · [#363](https://github.com/dancinlab/anima/pull/363) · [#366](https://github.com/dancinlab/anima/pull/366)
> 까지 누적된 모든 top-level block 을 한 곳에 고정하고, 4-criterion closure
> 자동 판정 매핑까지 제공한다.

## § 1. SSOT 선언

- **scope** — Phase D ckpt-bearing fire (multilingual probe + corpus_quality
  + dream_stage IPC + 8-factor motivation 의 통합 산출물)
- **producer** — [`HEXAD/PURE/eval/multilingual_probe.hexa`](../eval/multilingual_probe.hexa)
  `score` 모드 (legacy + corpus_quality + dream_stage_at_eval)
  + [`HEXAD/PURE/launchers/dispatch_p21h_v3.hexa`](../launchers/dispatch_p21h_v3.hexa)
  `--measure-motivation` flag (motivation_8factor)
- **consumer** — [`HEXAD/PURE/eval/result_to_axis_map.hexa`](../eval/result_to_axis_map.hexa)
  (AXIS_MAP_RESULTS row 생성) · 후속 H_xxx falsifier evidence accumulator
- **back-compat** — 모든 신규 block 은 optional, 부재 시 axis_map 이 `—` 폴백 (§ 8)

## § 2. legacy 블록 (PR [#228](https://github.com/dancinlab/anima/pull/228) · [#240](https://github.com/dancinlab/anima/pull/240))

`train_p21h_v3.py` 와 multilingual_probe 가 항상 채우는 base 키 set.

| 키 | 타입 | 의미 |
|---|---|---|
| `verdict` | str | aggregate verdict (`HEXAD_V3_WORKS` / `PARTIAL` / `FAIL`) |
| `per_lang_verdicts` | list of dict | 5 langs × `{lang, verdict, n_score, n_generalize, n_lang_coherent, ...}` (multilingual_probe `_per_lang_verdict`) |
| `n_anima_register_hits_total` | int | anima-register collapse 토큰 count (Principle #3 monitor) |
| `register_regress` | str/bool | `"yes"` / `"no"` — train 종단 register 증가 여부 |
| `init_log` | dict | `{L_ce, step, ...}` train 시작점 |
| `final_log` | dict | `{L_ce, step, ...}` train 종단 |
| `train_wall_s` | float | train wall seconds |
| `n_total_params` | int | 모델 총 파라미터 |

legacy 폴백 — `init_log_ce` / `final_log_ce` flat 키도 `_nested_cell` 가 허용.

## § 3. `corpus_quality` 블록 (PR [#355](https://github.com/dancinlab/anima/pull/355) · 원조 [#287](https://github.com/dancinlab/anima/pull/287))

`score --corpus <path>` 지정 시 [`corpus_quality_probe.hexa`](../eval/corpus_quality_probe.hexa)
의 `score_corpus_jsonl(path, sample_bytes)` 가 top-level 로 embed.

| 키 | 타입 | 의미 |
|---|---|---|
| `path` | str | 측정된 jsonl corpus 경로 (anchor — sha 는 별도 sidecar) |
| `n_bytes` | int | 샘플 bytes |
| `n_lines` | int | 샘플 line 수 |
| `sample_bytes` | int | 샘플 cap (기본 1 MB) |
| `m1_entropy` | float | M1 — byte entropy (높을수록 다양) |
| `m2_bigram_mi` | float | M2 — bigram mutual information |
| `m3_ttr` | float | M3 — token type-to-token ratio (≥ 0.3 권장, Track 1 0.03 register-sink) |
| `m4_avg_line` | float | M4 — 평균 line length |
| `m5_hangul` | float | M5 — Hangul codepoint coverage |
| `m6_kl_uniform` | float | M6 — KL divergence vs uniform byte dist |

## § 4. `dream_stage_at_eval` 블록 (PR [#363](https://github.com/dancinlab/anima/pull/363))

multilingual_probe `_read_dream_stage()` 가 scoring 시작 시
`$HOME/.cache/anima/dream_stage.current` (PR [#307](https://github.com/dancinlab/anima/pull/307)
IPC) 를 읽어 canonical 5-stage Φ-envelope table (verbatim mirror of
`dream_context()`) 로 stamp.

| 키 | 타입 | 의미 |
|---|---|---|
| `stage` | str | `WAKE` / `N1` / `N2` / `N3` / `REM` |
| `phi_envelope` | float | WAKE 1.0 · N1 0.7 · N2 0.4 · N3 0.15 · REM 0.95 |
| `tension_envelope` | float | WAKE 1.0 · N1 0.7 · N2 0.4 · N3 0.2 · REM 0.9 |
| `ipc_path` | str | 읽은 IPC 파일 경로 |

AUTONOMY CONTRACT — stage = **context**, emit gate 아님 (`@D a_autonomy_over_hardcode`).

## § 5. `motivation_8factor` 블록 (PR [#366](https://github.com/dancinlab/anima/pull/366))

`dispatch_p21h_v3.hexa --measure-motivation` 지정 시 Phase B
[`HEXAD/CHAT/spontaneous_lib.hexa`](../../CHAT/spontaneous_lib.hexa)
8-factor closed-form battery 를 result.json 에 embed.

| 키 | factor fn | 입력 키 (result.json) | 가중치 |
|---|---|---|---|
| `relevance` | `factor_relevance(phi)` | `phi_final` | 0.20 |
| `gap` | `factor_info_gap(cos_sim)` | `retrieve_cos_sim` | 0.10 |
| `curiosity` | `factor_curiosity(ema)` | `curiosity_ema` | 0.15 |
| `pain` | `factor_pain(Δtension)` | `tension_delta` | 0.10 |
| `coherence` | `factor_coherence(gate)` | `bridge_gate_value` | 0.10 |
| `originality` | `factor_originality(split)` | `split_event_recent` | 0.10 |
| `balance` | `factor_balance(phi, ratchet)` | `phi_final` + `ratchet` | 0.15 |
| `dynamics` | `factor_dynamics(silence_s)` | `silence_seconds` | 0.10 |
| `motivation_score` | weighted sum ∈ [0,1] | (위 8 factor) | Σ=1.00 |

모든 factor 값 ∈ [0,1] (B-SPONT-FACTOR-1..8 clamp). 부재 입력 → real-limit-safe default.

## § 6. closure 4-criterion 자동 판정 매핑

PURE.md L39 + Phase D 설계의 4 closure 기준 — 각 기준이 어느 block · 어느 키로 측정되는지 확정 mapping.

| # | 기준 | source field | 통과 임계 |
|---|---|---|---|
| 1 | register collapse 부재 | `n_anima_register_hits_total` | `< 4` (20 probe 中) |
| 2 | 다국어 closure | `per_lang_verdicts[].verdict` | `count(≥ PARTIAL) ≥ 4 / 5` |
| 3 | substrate-native motivation | `motivation_8factor.motivation_score` | `≥ 0.30` (Phase B B-SPONT 기본 emit threshold) |
| 4 | sleep/dream context 결합 | `dream_stage_at_eval.phi_envelope` | block 존재 + Φ ∈ canonical table |

`result_to_axis_map.hexa` 의 `format_axis_map_row` 가 #1 (`reg hits` col) · #2 (`per-lang` col + `closure` judgement) · #4 (`dream stage` col) 를 직접 렌더, #3 은 motivation 블록을 후속 follow-up script 가 별도 column 으로 elevate (현재 axis_map row 외).

## § 7. full JSON example

```json
{
  "verdict": "HEXAD_V3_WORKS",
  "per_lang_verdicts": [
    {"lang": "en", "verdict": "STRONG", "n_score": 18, "n_generalize": 18, "n_lang_coherent": 19},
    {"lang": "ko", "verdict": "STRONG", "n_score": 17, "n_generalize": 18, "n_lang_coherent": 17},
    {"lang": "zh", "verdict": "PARTIAL", "n_score": 13, "n_generalize": 14, "n_lang_coherent": 13},
    {"lang": "ru", "verdict": "STRONG", "n_score": 16, "n_generalize": 16, "n_lang_coherent": 17},
    {"lang": "ja", "verdict": "PARTIAL", "n_score": 12, "n_generalize": 13, "n_lang_coherent": 12}
  ],
  "n_anima_register_hits_total": 2,
  "register_regress": "no",
  "init_log": {"L_ce": 14.18, "step": 0},
  "final_log": {"L_ce": 0.92, "step": 2000},
  "train_wall_s": 1987.42,
  "n_total_params": 332000000,
  "corpus_quality": {
    "path": "state/pure_phase_d_corpus/multi_v2.jsonl",
    "n_bytes": 1000000,
    "n_lines": 4321,
    "sample_bytes": 1000000,
    "m1_entropy": 5.7835,
    "m2_bigram_mi": 2.6618,
    "m3_ttr": 0.612,
    "m4_avg_line": 231.4,
    "m5_hangul": 0.043,
    "m6_kl_uniform": 2.23
  },
  "dream_stage_at_eval": {
    "stage": "REM",
    "phi_envelope": 0.95,
    "tension_envelope": 0.9,
    "ipc_path": "/Users/ghost/.cache/anima/dream_stage.current"
  },
  "motivation_8factor": {
    "relevance": 0.42,
    "gap": 0.0,
    "curiosity": 0.0,
    "pain": 0.0,
    "coherence": 0.785714,
    "originality": 0.0,
    "balance": 1.0,
    "dynamics": 0.0,
    "motivation_score": 0.312571
  }
}
```

위 예시 기준 4-criterion 자동 판정 — #1 ✅ (reg=2 < 4) · #2 ✅ (5/5 ≥ PARTIAL) · #3 ✅ (score 0.31 ≥ 0.30) · #4 ✅ (REM Φ=0.95). closure = PASS.

## § 8. back-compat 처리

legacy result.json (PR #355 이전 — `corpus_quality` / `dream_stage_at_eval` /
`motivation_8factor` 누락) 도 동일 schema reader 로 안전 처리:

- `_corpus_cell` · `_dream_stage_cell` (axis_map.hexa) — key 부재 시 `"—"` 반환
- multilingual_probe — `--corpus` 미지정 → corpus_quality 키 자체 미생성
- dispatch_p21h_v3 — `--measure-motivation` 미지정 → motivation_8factor 키 미생성
- IPC 파일 부재 → dream_stage_at_eval 키 미생성 (`_read_dream_stage` 빈 dict)

→ AXIS_MAP_RESULTS 같은 row 안에서 legacy 변형과 Phase D 변형이 공존 가능.

## § 9. Honest C3 (≥ 3)

1. **schema 미고정** — 본 doc 은 2026-05-24 LANDED 상태의 snapshot. 후속 PR
   (예: motivation_8factor 가중치 재조정, corpus_quality M7 추가) 가 발생하면
   본 doc 도 동시 갱신 필요 (자동 sync 메커니즘 없음 — `@D a1` SSOT 수동 절차).
2. **key 변경 시 다운스트림 영향** — `n_anima_register_hits_total` 같은 긴
   legacy 키는 train 측 (`train_p21h_v3.py`) 과 eval 측 (axis_map) 양쪽에서
   하드코딩 참조. 키 rename 1건도 양쪽 동기 필수.
3. **sample-size 한계** — § 7 예시는 모든 block 채워진 가상 row. 실측 Phase D
   fire 1건 이상이 본 schema 로 산출돼야 fully-validated. 현재 § 5 motivation
   smoke 만 dry-run synthetic 으로 검증 (F-DISP-MOT 8/8 PASS, PR #366).
4. **`sha` vs `path` 차이** — corpus_quality block 은 `path` 만 stamp (sha 는
   별도 corpus build manifest 의 책임). cross-fire corpus identity 추적 필요
   시 path → sha 변환 sidecar 필수.
