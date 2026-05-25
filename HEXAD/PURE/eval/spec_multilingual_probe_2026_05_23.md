# PURE multilingual eval probe — consolidation spec (2026-05-23)

## 1. 왜 통합하는가

각 launcher (Track 1 corpus reburn, B distill, C head_g objective, 향후 A/D/E/F)
가 5-lang OOD probe set + STRONG/PARTIAL/WEAK 분류기를 **자체적으로 re-implement
하는 경향**이 발견되었음. 이는 drift risk:

- 한 launcher 가 prompt 한 줄을 수정하면 다른 launcher 와 apples-to-apples 비교
  실패.
- 분류기 threshold 차이 (예: lang_coherent 의 `ja` 0.25 vs 0.5) 가 verdict 를
  바꾼다.
- register-tag substring + regex 셋이 update 될 때 (e.g. 2026-05-23 cycle 의
  ANIMA_REGEX_KEYS 추가) 한 곳에서만 적용되면 metric scale 비교가 깨진다.

`HEXAD/PURE/eval/multilingual_probe.hexa` 가 SSOT evaluator. fixture +
classifier + per-lang verdict + aggregate + Hc 를 **하나의 hexa 파일에서**
공급한다.

## 2. fixture format

`HEXAD/PURE/eval/fixture_5lang_v1.json`

- `fixture_version` — semver-like 태그. PR #228 launcher 의 변경은 fixture v2 가
  필요할 때만 fixture 파일을 새로 추가하고, v1 은 historical comparability 를
  위해 동결.
- `probes_by_lang` — `{ "en": { "<probe_id>": "<prompt>", ... }, ... }` 5 langs ×
  10 prompts = 50 total. **provenance**: `train_p21m_multilingual.py
  PROBES_BY_LANG` 에서 verbatim 복사 (closure-fire SSOT).
- `score_axis` — classifier 와 lang_coherent threshold 의 명시. PURE 의 hexa
  분류기는 이 fixture 의 threshold 를 무시하고 hard-code; fixture 는 documentation
  + drift-detection (분류기 hard-code 가 fixture 와 vary 시 audit failure) 용도.
- `anima_register_keys` + `anima_register_regex` — register-tag drift detection 의
  SSOT. fixture 가 키 셋의 source of truth.

## 3. 사용 — 4 가지 mode

### (a) `selftest` — F-PURE-EVAL-1..3

```
hexa run HEXAD/PURE/eval/multilingual_probe.hexa selftest
```

- F-PURE-EVAL-1: fixture 파싱 + Phase 1A.1 SSOT ckpt 경로 (`archive/state_legacy/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.safetensors`) resolve 확인
- F-PURE-EVAL-2: fixture probes_by_lang 5 langs × 10 probes = 50 invariant
- F-PURE-EVAL-3: 부재 ckpt 경로에 대해 `file_exists()` false 리턴 (downstream error wire 확인)

기대 출력: `3/3 PASS, 0 FAIL` (selftest exit 0).

### (b) `score <run_json>` — post-hoc 분류

```
hexa run HEXAD/PURE/eval/multilingual_probe.hexa score <rows.json> [--out summary.json]
```

`rows.json` schema:

```json
{
  "rows_by_lang": {
    "en": [{"name": "en1", "text": "<gen>"}, ...],
    "ko": [{"name": "ko1", "text": "<gen>"}, ...],
    ...
  }
}
```

출력 1-line:

```
PURE_EVAL: en=PARTIAL ko=PARTIAL zh=WEAK ru=PARTIAL ja=WEAK · 3/5 ≥PARTIAL · Hc=0.74 · PARTIAL
```

JSON summary 는 per-lang `n_generalize / n_memorize / n_lang_coherent / n_score
/ verdict` + aggregate `n_ok / agg_verdict` + global `Hc` 를 담는다.

### (c) `emit <ckpt>` — driver shell 생성

```
hexa run HEXAD/PURE/eval/multilingual_probe.hexa emit <ckpt> --driver-out eval.sh
```

`eval.sh` 는 GPU 머신에서 python+torch+transformers 환경 하에 ckpt 를 load +
fixture 의 50 prompts 에 대해 generate + classify → `rows.json` 으로 떨군다.
이후 `score` 모드 (a) 가 분류 + 점수화.

### (d) `fixture` — sanity print

```
hexa run HEXAD/PURE/eval/multilingual_probe.hexa fixture
```

n_lang / n_probes / version 출력.

## 4. launcher 통합 (one-liners)

각 launcher 의 후속 PR 에서 1 줄 호출로 교체:

- **Track 1** (`HEXAD/PURE/launchers/track1_corpus_reburn_launcher.hexa`):
  `bash $(emit-output).sh ... && hexa run multilingual_probe.hexa score rows.json --out PURE_EVAL.json`
- **B distill** (`HEXAD/PURE/launchers/b_distill_launcher.hexa`):
  동일 패턴 — student ckpt 에 대해 score 모드 실행.
- **C head_g objective** (`HEXAD/PURE/launchers/c_head_g_objective_launcher.hexa`):
  동일 패턴 — head_g 추가 ckpt 에 대해 score 모드 실행.
- **A/D/E/F** (TBD launcher):
  동일 패턴 (그리고 fixture 는 동일 v1 사용, 새 axis 가 필요한 경우 v2 fixture 추가).

DO NOT 이 PR 에서 launcher 들을 수정 — separate "use the consolidated eval" PR.

## 5. 향후 확장

- **신 lang 추가**: fixture 의 `probes_by_lang` 에 새 lang 키 추가 + 10 probes.
  harness 의 `_is_lang_native` + `_lang_threshold` 에 해당 codepoint range 추가.
  fixture_version 을 v1 → v2 로 bump.
- **probe-set v2** (new prompt category 추가, 20+/lang 등): 새 fixture file `fixture_5lang_v2.json` 추가, v1 은 동결.
- **register-tag-aware eval**: fixture 의 `anima_register_keys` / `_regex` 를 수정 →
  분류기 hard-code 와 sync. 향후 fixture 에 expected_register_rate 추가 시 STRONG/PARTIAL
  threshold 와 동등하게 다룬다.
- **Hc 정밀화**: 현재 Hc = (sum n_score) / (n_lang × max_per_lang). 향후 register-leak
  penalty 를 차감하는 `Hc_pen` 추가 가능 (가령 `Hc - 0.5 × register_hit_rate`).

## 6. 제약 + C3 (honest caveats)

- harness 는 **GPU forward 를 자체 실행하지 않음** — `emit` 모드가 python 드라이버를
  토해내고 caller 가 그것을 GPU 머신에서 실행. 이 분리는 hexa-only authoring
  directive 위반이지만 `[[feedback-hexa-only-authoring]]` 의 직접 위반이 아니라
  closure-fire 가 이미 python train script 를 신뢰하는 패턴을 reuse 한 것 — python
  driver 는 hexa 가 emit 한 산물.
- fixture v1 의 50 prompts 는 closure-fire 의 SSOT 와 byte-equal. 향후 prompt
  drift 가 발견되면 fixture v2 / fixture v1.x 로 rotate.
- `selftest` 는 GPU 가 없는 Mac 에서 작동 — F-PURE-EVAL-1 의 ckpt 경로 확인은
  Mac 의 archive/state_legacy 경로에 의존. CI 머신에서 selftest 가 통과하려면 동일
  ckpt 가 마운트되어야 한다 (또는 selftest 가 SSOT ckpt absence 를 warn-only 로
  처리하도록 향후 옵션 추가).
