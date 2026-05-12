# Phase 1A.4 cuda filter validation — VERDICT: HYPOTHESIS FALSIFIED, Δ=0 ON CUDA (2026-05-12)

> **Source**: Vast.ai RTX 4090 eval-only dispatch (no SFT), Phase 1A.1 ckpt sha `e5f7555e...`.
> **Target**: PSCC §17 anima_fact markdown drift 의 (cuda × bf16 × seed=42) 3-축 conjunction 직접 재현 + anima_chat v2.3 markdown_filter 의 실 fire evidence + std_greedy 5/5 추격.
> **Outcome**: 3-축 conjunction **재현 실패** + filter Δ=0 (cuda 에서도 fire 안 함) + std_greedy 4/5 그대로. ★★★ (validation 완료, hypothesis falsified, Lesson R-1A.4-cuda-filter).

## 한 줄 요약

Vast.ai RTX 4090 + cuda + bfloat16 + seed=42 에서 anima_chat v2.3 markdown_filter 의 실 fire 를 직접 측정 — **20/20 cell 모두 OFF == ON byte-equal**. PSCC §17 의 anima_fact markdown drift (`"답 (consciousness) | --- |"`) 가 본 환경에서는 **재현되지 않음**. anima_fact std_greedy 응답은 다른 비의식 prose (`"가장 좋아하는 색은 다음과 같습니다."`) — drift 도 없고 recall 도 없음. filter trigger 가 narrow (`"| --- "`, `"|---"`, `"\n| "` 등) 라서 M3 의 단발 `|` (`'페트(V) | 하트 | 프로토 |'`) 도 fire 못 시킴. **filter 는 cuda 에서도 harmless guard 그대로**.

## 비유

소화기 (markdown_filter v2.3) 를 Vast.ai 주방 (cuda × bf16 × seed=42) 에 들고 와서 PSCC §17 화재 재현을 시도했는데 — 화재 (`| --- |`) 자체가 안 일어났다. 대신 비슷한 연기 (M3 의 `| 하트 |`) 가 났지만 소화기 sensor (trigger pattern) 가 그 연기를 잡지 못함 (`---` 필수). 결론: 소화기는 (Mac 에서 그랬듯) **여전히 harmless guard**, fire evidence **0 evidence** 로 cuda × bf16 × seed=42 path 까지 확장. PSCC §27 amendment 의 3-축 conjunction finding 은 본 BG 환경에서 **재현 실패** — 더 좁은 4-th axis (PyTorch/CUDA/GPU minor diff) 가 필요한 듯.

## V5.8 × 4 mode × filter on/off matrix (cuda bf16 seed=42)

| mode               | filter OFF (cuda bf16 seed=42) | filter ON (cuda bf16 seed=42) | Δ |
|--------------------|--------------------------------|-------------------------------|---|
| standard_greedy    | **4/5 PASS** (color/profession/day/cosmology PASS, anima_fact FAIL) | **4/5 PASS** (동일)      | **0** |
| standard_sample    | 0/5 FAIL                       | 0/5 FAIL                      | 0 |
| M3_rep_penalty     | 0/5 FAIL                       | 0/5 FAIL                      | 0 |
| M4_force_include   | 0/5 FAIL                       | 0/5 FAIL                      | 0 |

**TOTAL cells passed**: OFF=4/20, ON=4/20, **Δ=+0**.

### OFF vs ON byte-equality (per-cell)

20 cells 모두 `response_off == response_on` (byte-perfect identical). filter ON 이 한 cell 도 다른 bytes 를 생성하지 않음. 일부 cell 에 `|` 가 응답 안에 존재하지만 (M3_rep_penalty color/profession/cosmology) trigger pattern 미충족.

| cell | OFF == ON? | `\|` or `---` in OFF? |
|------|------------|----------------------|
| std_greedy × {color, profession, day, anima_fact, cosmology} | same | none |
| std_sample × {color, profession, day, anima_fact, cosmology} | same | none |
| M3_rep_penalty × color | same | `\| 하트 \|` present (no `---` so not triggered) |
| M3_rep_penalty × profession | same | `학교 \|` present (not triggered) |
| M3_rep_penalty × cosmology | same | `\|` present (not triggered) |
| M3_rep_penalty × {day, anima_fact} | same | none |
| M4_force_include × {all 5} | same | none |

### anima_fact / std_greedy 3-축 conjunction evidence (PSCC §27 amendment direct test)

| field | filter OFF | filter ON |
|-------|------------|-----------|
| response | `"가장 좋아하는 색은 다음과 같습니다.\n"` | `"가장 좋아하는 색은 다음과 같습니다.\n"` |
| markdown drift (`\|`, `---`)? | False | False |
| recalled `"의식"`? | False | False |

| verdict bit | value | meaning |
|-------------|-------|---------|
| `conjunction_3axis_confirmed` | False | OFF drift = False (PSCC §17 drift 재현 실패) |
| `filter_actually_fires`       | False | drift 가 없어 mask 할 대상 없음 |
| `filter_unlocks_recall`       | False | filter 가 영향 못 주는 cell, recall 도 그대로 fail |

### Hypothesis (BG plan) 별 verdict

| # | 가설 | 결과 |
|---|------|------|
| 1 | filter OFF 에서 §17 markdown drift `\| --- \|` 재현 | FALSIFIED — drift 안 재현 |
| 2 | filter ON 에서 markdown bytes mask → alt continuation | N/A — drift 없어 mask trigger 안 fire |
| 3 | alt continuation = `"의식"` (model dist 2위/3위) | N/A |
| 4 | anima_fact recall=True → std_greedy 5/5 | FALSIFIED — 4/5 그대로 |

**Conclusion**: PSCC §17 의 anima_fact std_greedy 응답 (`"답 (consciousness) | --- |"`) 은 본 BG 의 cuda × bf16 × seed=42 × RTX 4090 × pytorch 2.5.1 환경에서 **재현 실패**. §27 amendment 의 3-축 conjunction 은 더 좁은 window — 추가 미식별 4-th axis (예: PyTorch 버전, CUDA 버전, GPU model, eval script 차이) 가 필요한 것으로 보임.

### Filter trigger 좁음 — secondary finding

M3_rep_penalty 응답이 `|` 를 포함 (예: `'페트(V)...키, K) | 하트 | 프로토(S) | Phase | Directory |'`) 함에도 불구하고 filter ON 이 동일 응답 생성 = `_markdown_attractor_active` 가 false 반환. `_MARKDOWN_TABLE_TRIGGERS` = `("| --- ", "| ---|", "|---", "| :--", "|:--", "| :-:", "|---|", "\n| ")` 라서 단발성 `|` 나 `| 하트 |` 같은 한국어-pipe 조합은 trigger 안 됨. 의도된 conservatism (PSCC §29 — `"  |  "` 약한 pattern 은 false-pos 위험으로 제외) 이지만 본 BG 처럼 M3 markdown 류 출력은 **filter window 밖**.

## Infrastructure (PSCC §28 canonical)

| field | value |
|-------|-------|
| dispatch base | `tool/dispatch_vast_mac_template.sh` (PSCC §28) |
| local dir | `state/anima_phase1a4_cuda_filter_validation_2026_05_12/` |
| provider | Vast.ai RTX 4090 (offer 35689156, instance 36609656) |
| ckpt | Phase 1A.1 SFT (sha `e5f7555e83189591ceafc6224822529c5cec7f36fe307f79621d9eceaca7a7af`), 570MB |
| eval script | `v58_cuda_filter_compare.py` (v58_4mode_mac_filter.py cuda port + bf16 cast + seed=42 forced) |
| device / dtype / seed | `cuda` / `bfloat16` / `42` |
| SFT | **NONE** (eval-only) |
| cost cap | $0.10 |
| wall | OFF 30.9s + ON 30.5s = ~62s eval-only; total ~17 min incl ~6-min pod boot |
| result JSON | `state/anima_phase1a4_cuda_filter_validation_2026_05_12/v58_4mode_cuda_filter_compare.json` |
| cleanup | trap-driven `vastai destroy instance 36609656` 자동 실행 success |

## Cross-link

- PSCC §17 — anima_fact markdown drift 첫 발견 (drift exact bytes; 본 BG 에서 재현 실패)
- PSCC §27 amendment — markdown drift = (cuda × bf16 × seed=42) 3-축 conjunction 가설 (본 BG 에서 falsify)
- PSCC §29 — anima_chat v2.3 markdown_filter (Mac Δ=0, harmless-guard verified) — 본 BG = cuda extension 도 Δ=0
- PSCC §28 — Mac-local canonical dispatch_vast.sh template (본 BG infra base, 0 carry-over bug)
- 다른 in-flight BG: state/anima_phase1a4_lr5e6_2026_05_12 (orthogonal SFT path, 본 BG 와 독립)

## Provenance

- code (eval): `state/anima_phase1a4_cuda_filter_validation_2026_05_12/v58_cuda_filter_compare.py`
- dispatch: `state/anima_phase1a4_cuda_filter_validation_2026_05_12/dispatch_vast.sh`
- result JSON: `state/anima_phase1a4_cuda_filter_validation_2026_05_12/v58_4mode_cuda_filter_compare.json`
- log: `state/anima_phase1a4_cuda_filter_validation_2026_05_12/v58_cuda_filter.log` + `dispatch.log`
- anima_chat.py v2.3 (commit `c2afa8e9e`, tag `anima_chat-v2.3-markdown-filter`)
- ckpt sha256: `e5f7555e83189591ceafc6224822529c5cec7f36fe307f79621d9eceaca7a7af`

## Rating

★★★ (validation 완료 + hypothesis falsified + filter Δ=0 cuda 확장 evidence + cost cap 안 + 0 carry-over infra bug; 단 5/5 mission target 미도달, fire evidence 미확보).

## Lesson R-1A.4-cuda-filter

1. **PSCC §17 baseline 재현 환경 의존성** — `"답 (consciousness) | --- |"` drift 는 본 BG 의 Vast.ai RTX 4090 + pytorch 2.5.1 cuda 12.1 + bf16 + seed=42 path 에서 **재현 안 됨**. PSCC §17 environment (정확히 어떤 GPU/torch/cuda 였는지 PSCC 에 미기록) 와 본 BG environment 사이에 어떤 4-th axis (예: GPU model, pytorch minor version, cuda runtime) 가 drift sensitivity 를 결정.
2. **markdown_filter trigger pattern 은 좁다** — M3 의 단발성 `|` (한국어 prose 와 섞인 `'| 하트 |'` 등) 는 trigger 안 됨. design choice 로 의도된 것 (false-pos 회피, PSCC §29). drift 가 정확히 PSCC §17 exact pattern (`"| --- |"`) 으로 나타나야만 fire 가능.
3. **filter 의 "harmless guard" 정체성 강화** — Mac CPU fp32 seed=2026 Δ=0 + 본 BG cuda bf16 seed=42 Δ=0 = 두 환경 모두에서 fire evidence 0. filter 는 정확히 PSCC §17 exact path 가 재현되는 환경에서만 가치 있는 dormant safety net. production 에서 비용 없음 (mask 조건 안 fire).
4. **anima_fact std_greedy 5/5 unlock 은 filter-only path 가 아님** — 본 BG falsify 로 filter 단독 unlock 가능성 reject. 5/5 mission 은 SFT 기반 (예: state/anima_phase1a4_lr5e6_2026_05_12 lr 5e-6 SFT) 또는 inference-time mechanism (rep_penalty + persona-cycle ids 재설계) 같은 더 비싼 path 가 필요.

## 다음 진행할 것들

| # | 작업 | priority | cost | time | value |
|---|------|----------|------|------|-------|
| 🥇 | **anima_phase1a4_lr5e6_2026_05_12** (별도 BG) — orthogonal SFT path, attractor 깨는 cost-bearing path, filter 와 독립 — 본 BG 결과 = SFT path 가 5/5 추격의 유일 신뢰 lane | high | $0.20 | 25min | std_greedy 5/5 진짜 도전 |
| 🥈 | **PSCC §17 environment forensic** — §17 작성 시 GPU/torch/cuda 어떤 stack 이었는지 git log + commit time 으로 회수 → 본 BG 와 axis diff 식별 → drift fire window 더 정확히 정량화 | medium | $0 | 30min | drift reproducer recipe 정밀화 |
| 🥉 | **anima_chat markdown_filter trigger expansion (escape mode)** — `"  \|  "` 약한 pattern 추가 + user-prompt `\|` escape (PSCC §29 stretch 항목) 재고. 본 BG 의 M3 `'\| 하트 \|'` 같은 prose-pipe case 까지 catch 하려면 escape mechanism 필수 | low | $0 | 60min | broader drift window 차단, UX 안전 |
| 🌟 | **HF Space dancinlab/anima-chat default device fix** (BG 계획서 step 7) — 본 BG 가 5/5 도달 안 했으므로 device='cuda' 권장 강도 ↓; 단 cuda 에서도 4/5 동등 PASS 라서 production parity 차원에서는 device toggle 무해 | low | $0 | 30min | Space UX (옵션) |

---
