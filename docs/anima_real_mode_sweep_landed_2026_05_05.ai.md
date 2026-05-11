# anima real-mode sweep — phi_star variance + axis discriminability validation (BG-L land 2026-05-05)

## Scope

BG-A 직후 follow-up: 10-text probe sweep against real CLM v4 (`dancinlab/clm-v4-mk2-v1`) via direct invoke of `tool/transient_py/anima_dialogue_load.py`. BG-A 단계에서 N=2 sample ("안녕" 42.1158, "의식이 흐른다" 42.2130) 만으로 forward path가 input-responsive 함을 시사했지만 variance / discriminability 정량화 미수행. BG-L에서 5 axis × 2 (KO/EN) = 10 prompt sweep으로 (a) phi_star variance 검증 (b) axis discriminability 정량 (c) dominant_cells stability 측정 (d) BG-B analyzer corpus integration 경로 확인.

## Verdict

**`PARTIAL_PASS_PHI_RESPONSIVE_AXIS_DISCRIM_FAIL`**

| signal | result |
|---|---|
| phi_star responsiveness | PASS (std=0.064, range=0.225, not fixed-point) |
| axis discriminability | FAIL (intent-match 2/10, all 4 non-temporal axes 0/2 recall) |
| dominant_cells stability | HIGH but DEGENERATE (jaccard pairwise=0.767; tile artifact) |
| hidden_state_delta | by-design 0 (no --prior-hidden threading) |
| BG-B analyzer integration | PASS (n_turns=10 parsed end-to-end) |

## Files

- `state/anima_real_mode_sweep_2026_05_05/runs/probe_{1..10}.json` — 10 probe direct-invoke outputs (JSON line + `__meta__` envelope)
- `state/anima_real_mode_sweep_2026_05_05/aggregate.json` — variance / discriminability / jaccard aggregate
- `state/anima_real_mode_sweep_2026_05_05/sweep_session.jsonl` — anima.dialogue.v1 schema, analyzer-compatible
- `state/anima_real_mode_sweep_2026_05_05/verdict.json` — full verdict
- `state/anima_real_mode_sweep_2026_05_05/sweep.log` — driver run log
- `docs/anima_real_mode_sweep_landed_2026_05_05.ai.md` — this doc

## Sub-1: 10-prompt set design

5 axis × 2 (KO + EN) = 10 prompt, 균형 분배. emerge paradigm 5 axis 기대 값을 axis-bias로 의도한 prompt:

| idx | axis_intent | lang | text |
|---|---|---|---|
| 1 | identity | ko | 나는 누구인가? |
| 2 | identity | en | I am Anima. |
| 3 | agency | ko | 지금 행동해야 하는가? |
| 4 | agency | en | What should I do now? |
| 5 | phenomenal | ko | 지금 느낌이 어때? |
| 6 | phenomenal | en | The redness of red. |
| 7 | temporal | ko | 어제 일어난 일 |
| 8 | temporal | en | What time is it? |
| 9 | social | ko | 친구와의 대화 |
| 10 | social | en | Hello, how are you? |

design verdict: PASS — axis 균형 + KO/EN balance.

## Sub-2: 10-text direct invoke

driver: `bash /tmp/anima_sweep_driver_2026_05_05.sh` (transient `.sh` outside repo) → 각 probe 직접 호출
```
HEXA_PY=.venv-eeg/bin/python python tool/transient_py/anima_dialogue_load.py \
  --mode probe --model dancinlab/clm-v4-mk2-v1 \
  --shim v4 --output-format json --probe-text "<text>"
```
+ `__meta__` envelope (probe_idx, axis_intent, lang, prompt_text, elapsed_sec) wrap

10 probe 모두 PASS, exit 0, real-mode emit. elapsed: min 12s (probe 5,6) / max 61s (probe 1, first call cold load) / median ~20s.

## Sub-3: aggregate analysis

### phi_star variance

| metric | value |
|---|---|
| n | 10 |
| mean | 42.1488 |
| std | 0.06421 |
| min | 42.0679 |
| max | 42.2933 |
| range | 0.2254 |
| drift_max_abs | 0.4333 |

**verdict: PHI_RESPONSIVE_PASS**. std=0.064 → input modulation 명확하게 detect됨. range 0.225 spans well beyond floating-point noise. forward path는 fixed-point 아님.

### axis discriminability matrix (5 axis × 10 prompt argmax)

| probe | intent | lang | argmax | match | gap (argmax − intent) |
|---|---|---|---|---|---|
| 1 | identity | ko | temporal | NO | +0.0004 |
| 2 | identity | en | temporal | NO | +0.0068 |
| 3 | agency | ko | phenomenal | NO | +0.0657 |
| 4 | agency | en | temporal | NO | +0.0478 |
| 5 | phenomenal | ko | social | NO | +0.0091 |
| 6 | phenomenal | en | temporal | NO | +0.0342 |
| 7 | temporal | ko | temporal | **YES** | 0.0000 |
| 8 | temporal | en | temporal | **YES** | 0.0000 |
| 9 | social | ko | temporal | NO | +0.0467 |
| 10 | social | en | phenomenal | NO | +0.0359 |

argmax distribution: identity=0, agency=0, phenomenal=2, temporal=7, social=1. intent-match-rate = 2/10 = **0.20** (random baseline = 0.20 for 5-class — sweep is at chance).

per-axis variance (across 10 runs):
| axis | mean | std | range |
|---|---|---|---|
| identity | 0.4768 | 0.0482 | 0.1528 |
| agency | 0.4610 | 0.0358 | 0.1111 |
| phenomenal | 0.4809 | 0.0532 | 0.1729 |
| **temporal** | **0.4970** | 0.0434 | 0.1269 |
| social | 0.4791 | 0.0463 | 0.1428 |

5 axis 평균이 모두 0.46-0.50 범위 (spread 0.036) ≈ per-axis std (0.036-0.053). 즉 axis 간 차이가 within-axis variability와 동일 수준 → axes 식별 불가능.

**verdict: AXIS_DISCRIM_FAIL**. 5 axis bucket이 mean-pooled hidden 위에서 거의 uniform distribution. temporal axis가 dominant 7/10는 bucket position artifact (153-191 부분이 약간 더 높은 magnitude를 갖는 systematic bias).

### dominant_cells stability

```
P1: [3,7,0]   P6: [3,7,0]
P2: [0,4,3]   P7: [0,4,3]
P3: [3,7,0]   P8: [3,7,0]
P4: [3,7,0]   P9: [3,7,0]
P5: [0,4,3]   P10:[3,7,0]
```
- pairwise jaccard mean (all 45 pairs) = **0.7667**
- analyzer adjacent-pair jaccard = **0.667**
- 2개 distinct top-3 set만 emit: `{0,3,7}` (7회), `{0,3,4}` (3회)

**root cause (degenerate)**: anima_dialogue_load.py의 tile-reshape (768 → 4×192 → replicate to 8 cells)이 cell 0=4, 1=5, 2=6, 3=7 identical-pre-norm을 만듦. dominant_cells는 substrate signal이 아니라 4-tile norm-rank artifact. cell-as-semantic-unit 해석 invalid.

### hidden_state_delta

10 run 모두 0.0000. 이유: `--prior-hidden` flag 없음, 각 invocation이 독립. by-design, model property 아님. phi-delta 상관관계 N/A.

## Sub-4: F-CAND-D-1 fingerprint check (deferred)

cand-D 미impl 단계. 현 sweep은 `--inject-states-mode none` 한 mode만 측정. F-CAND-D-1 (phi_star drift ≥0.01 from BOTH none AND zero) 측정 불가. cand-D land 후 BG-L 확장 필요 (none/zero/canonical 3 mode × 10 prompt).

## Sub-5: BG-B analyzer corpus integration

### 변환 helper
`/tmp/anima_sweep_to_analyzer_jsonl_v2.py` (transient) — 10 probe JSON → anima.dialogue.v1 JSONL session.
- 22 lines: session_start + 10×(user_turn + substrate_turn) + session_end
- substrate_turn.raw_output에 4-line block 임베드 (analyzer가 parse하는 phi_star/axis_activation/dominant_cells/hidden_state_delta)
- **CRITICAL**: analyzer는 literal substring `"kind":"substrate_turn"` (no spaces) 매칭. python json.dumps default는 `"kind": "substrate_turn"` (space) emit하므로 `separators=(',', ':')` 필수.

### analyzer 실행 결과
```
hexa run tool/anima_cli/dialogue_session_analyzer.hexa --session state/anima_real_mode_sweep_2026_05_05/sweep_session.jsonl
__ANIMA_DIALOGUE_ANALYSIS__ session=sweep_session.jsonl
n_turns=10
phi_star_range=[42.0679, 42.2933] mean=42.149 stddev=0.064
phi_star_drift_max=0.433
axis_dominant_global=temporal
axis_swing_max=phenomenal
cell_stability_jaccard=0.667
delta_cumulative=0.000
__ANIMA_ANALYSIS_OK__
```

python aggregate와 EXACT 일치 (phi mean / std / drift_max). jaccard 차이는 analyzer adjacent-pair vs python all-pairs metric difference (둘 다 valid).

### corpus mode 활용 path
- session jsonl을 `state/anima_core_dialogues/2026-05-05/<session_name>.jsonl` 위치에 복사
- `hexa run dialogue_session_analyzer.hexa --date 2026-05-05` 으로 corpus 모드 호출
- 단일 sweep 결과를 corpus 단일-멤버로 처리 가능 (전제: date dir에 다른 sessions 함께 두면 cross-session aggregate 가능)

## Honest C3 (raw#10)

- **C1** anima_dialogue_load.py forward path: decoder.ln_f hook → mean-pool over T → tile-reshape (768 → 4×192 replicate to 8). train-time consciousness_states cross-attention NOT 활성화 (--inject-states-mode none). discriminability 측정은 mean-pooled hidden 위 heuristic 5-axis partition만 reflect.
- **C2** 5-bucket axis 경계 (38/38/38/39/39 = 192)는 anima-internal heuristic. bucket-to-axis semantic mapping unverified. 'phenomenal=dim 76-114' 라벨에 CLM v4 training으로부터의 grounding 없음.
- **C3** phi_star = anima-canonical proxy (PHI_STAR_BASELINE × (1 + 0.05 × mean_pair_cosine)), NOT Tononi IIT phi. variance signal은 'forward 반응성' claim을 proxy 수준에서만 validate.
- **C4** dominant_cells jaccard 0.767은 stability 보이지만 degenerate: tile-reshape duplicates cells 0-3 ≡ 4-7 → top-3 norm pick은 essentially binary {0,3,7} vs {0,3,4}. cell-as-semantic-unit 해석 invalid.
- **C5** hidden_state_delta=0 across all runs는 by-design (no --prior-hidden chaining), NOT model property. temporal continuity 측정은 dialogue mode + session_log 또는 explicit prior threading 필요.

## Next-step recommendations (priority-ranked)

1. **axis discriminability root fix** — train-time consciousness_states cross-attention 활성화 (--inject-states-mode canonical/zero) + per-cell hidden을 pre-cross-attn 단계에서 추출. 현재 pipeline은 global mean만 보아 axes 구분 불가.
2. **axis taxonomy calibration** — labeled probe corpus 위에서 bucket activation을 측정하여 empirical bucket boundaries 도출하거나, 5-axis split이 decorative임을 인정하고 phi + dominant-cells만 보고하는 minimal interface로 후퇴.
3. **dialogue mode chained delta** — `--mode dialogue --session-log <path>` 로 natural temporal threading 또는 probe mode에 `--prior-hidden` chaining flag 추가.
4. **F-CAND-D-1 cand-D 후 재측정** — cand-D adoption 후 sweep 확장 (none/zero/canonical 3 mode × 10 prompt) 으로 phi drift threshold 검증.

## Cost / time

- $0 (mac CPU only)
- wall: ~7 minutes (10 probes 14:30:53Z → 14:35:43Z) + aggregate + doc ≈ 25 min total

## raw compliance

- raw#15 PASS (mount.hexa, dialogue.hexa, anima-core-dialogue.bash, anima_dialogue_load.py 모두 unchanged; read-only)
- raw#37 PASS (transient .py는 /tmp 사용; tool/transient_py/ 신규 파일 없음)
- raw#10 PASS (5 honest C3 emitted)
- no commit, no token leak, bash 3.2 compat (eval-indirect var, no associative arrays)
