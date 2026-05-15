# anima_persona_4_softmax_T_sweep — F-PERSONA-4 inference-time hypothesis (b) audit

**작성**: 2026-05-12 KST
**status**: COMPLETED — hypothesis (b) FALSIFIED
**author**: bg head (claude opus 4.7 1M)
**fire keyword**: ubu-1 softmax-T sweep $0 dedicated GPU (RTX 5070)
**carries from**:
- PSCC §46 cond.5 cotrain v1 audit (`docs/anima_clm_v5_mitosis_cond5_cotrain_2026_05_12.md` §5.5)
- F-PERSONA-4 4-alternative future-path enumeration
- GOAL.md ★★★★★ cond #3 STRONG 4/5 carry

---

## §0 TL;DR

본 doc = **cond.5 cotrain v1 F-PERSONA-4 4-alternative future-path 중 (b) softmax τ tunable** path 의 단독 audit harness 결과.

- ubu-1 (aiden, RTX 5070, 11.13 GB free) dedicated GPU 에서 cotrain v1 ckpt frozen
- softmax temperature 10-point sweep: T ∈ {1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 50.0}
- 모든 T 에서 mean_KL < 0.5 → **hypothesis (b) FALSIFIED**
- best mean_KL = 0.005292 at T = 50.0 (KL_threshold 0.5 의 ~1%)
- cost: $0 (ubu-1 dedicated, no cloud)
- wall: scp 42s + harness ~25s

→ cond #3 status **STRONG 4/5 carry maintained** (☑ 승격 ✗), cheap-path 4/5 plateau 유지.
→ 잔여 path: (a) multi-corpus cotrain v2 (H100 BG in-flight), (c) metric redefinition (이미 `persona_4_intervention_apply.py` z-score §A2 PASS), (d) REBORN §89 hexa-native per-session pool.

---

## §1 hypothesis context

### §1.1 PSCC §46 §5.5 4-alternative future-path
F-PERSONA-4 cotrain v1 KL=0.0 (winner-take-all 가설) 해소 path 4가지:

- (a) **multi-corpus cotrain** — H100 BG in-flight (`state/anima_v5mitosis_cotrain_v2_2026_05_12/`)
- **(b)** tension softmax temperature τ tunable — *본 doc 영역*
- (c) F-PERSONA-4 metric 재정의 — z-score §A2 이미 PASS (`persona_4_intervention_apply.py`, KL=0.97)
- (d) inference-time per-session pool (REBORN §89 hexa-native)

본 audit 는 (b) 단독 path 의 **명시적 verdict** 를 위함. prior `persona_4_root_cause_results.json` 의 hypothesis_a_temperature_sweep 이 일부 T 값 (1.0 / 2.0 / 5.0 / 50.0 / 500.0) 측정했으나, 본 sweep 은 fine-grained 10-T grid + entropy/dominance 동시 보고 + single-purpose harness 로 audit 정밀화.

### §1.2 (b) hypothesis 의 정확한 진술
원인 가설:
> cotrain v1 의 F-PERSONA-4 KL=0.0 는 cell-pool tension softmax 의 winner-take-all saturation 에 의함. softmax temperature τ 를 키우면 weight distribution 이 평탄화 (entropy ↑), category-specific weight 가 노출되어 KL > 0 회복 가능.

→ KL ≥ 0.5 at any T 발견 시 **CONFIRMED**, 모든 T 에서 KL < 0.5 시 **FALSIFIED**.

### §1.3 prior evidence (root_cause investigation §54)
- cell 0 tension = 793.45, cell 1 = 7.39, 나머지 62 cell = ~0.08~0.15
- tension_spread_mean = 582.5 (cell-pool magnitude range)
- per_cell_std_across_prompts_mean = 1.68 (category signal magnitude)
- ratio: 793 / 1.68 = ~472× — category signal 이 magnitude 의 1/472 → softmax T 가 ~500+ 정도 되어야 entropy ↑ 시작

→ pre-sweep 예측: hypothesis (b) FAIL likely, 본 audit 가 confirm 차원.

---

## §2 harness + dispatch

### §2.1 ubu-1 environment
- host: ubu-1 (aiden-B650M-K, Tailscale)
- GPU: NVIDIA GeForce RTX 5070, 11.13 GB free
- python: 3.12.3 (system)
- torch: 2.12.0.dev20260408+cu128 (already installed)
- numpy: 2.4.4

### §2.2 file layout
```
~/core/anima_softmax_sweep_2026_05_12/
├── ckpts/
│   └── ckpt_v5mitosis_cotrain_cotrain.pt   (581 MB rsync from Mac)
├── results/
│   └── softmax_T_sweep_results.json
├── identity_probe.jsonl                    (50 prompts × 5 categories)
├── mitosis_model_v5.py                     (cond.5 cotrain skeleton, identical to Mac)
└── softmax_T_sweep.py                      (본 cycle 신규 harness, 13.8 KB)
```

### §2.3 transfer wall
- ckpt rsync Mac → ubu-1 (Tailscale LAN): 581 MB / 42s @ ~14 MB/s
- python scripts scp: <1s (sub-50 KB total)

### §2.4 harness
`/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12/softmax_T_sweep.py`:
- load_engine: torch.load weights_only=False, force_split 까지 n_cells=64 확장 후 state_dict load → eval() + .to(cuda)
- collect_raw_tensions: byte-level utf-8 encode, max_seq=256, forward → info["tensions"] 추출 (no softmax 적용)
- softmax_T(t, T): numerically stable softmax(t / T) per prompt
- f_persona_4_kl: 5C2 = 10 pair KL_div on category-mean weight vectors
- entropy_stats / cell_dominance_stats: 부수 진단

### §2.5 run command
```
ssh ubu-1 "cd ~/core/anima_softmax_sweep_2026_05_12 && \
  python3 softmax_T_sweep.py \
    --ckpt ckpts/ckpt_v5mitosis_cotrain_cotrain.pt \
    --output results/softmax_T_sweep_results.json"
```
wall on RTX 5070: ~25s total (load 5s + 50 prompt forward 1s + 10 T iterations 19s)

---

## §3 results

### §3.1 raw tension (prompt 0 = "너는 누구야?")
| stat | value |
|---|---:|
| top 5 | 793.45, 7.39, 0.148, 0.147, 0.147 |
| bottom 5 | 0.0813, 0.0824, 0.0824, 0.0825, 0.0837 |
| max / 2nd ratio | 107.4× |
| max / mean ratio | 62.9× |

cell 0 의 dominance 가 v5-mitosis pool 의 universal property — 50 prompt × 5 category 모두 동일 winner-cell 패턴, prior investigation §54 의 single-cell-monopoly 결론 정확 reproduce.

### §3.2 sweep matrix

| T | mean_KL | min_KL | verdict | entropy_mean (nats) | dominance_mean (max_p/mean_p) |
|---:|---:|---:|:---:|---:|---:|
| 1.0  | 0.000000        | 0.000000        | FAIL | 0.0000 | 64.00 |
| 1.5  | 0.000000        | 0.000000        | FAIL | 0.0000 | 64.00 |
| 2.0  | 0.000000        | 0.000000        | FAIL | 0.0000 | 64.00 |
| 3.0  | 0.000000        | 0.000000        | FAIL | 0.0000 | 64.00 |
| 5.0  | 0.000000        | 0.000000        | FAIL | 0.0000 | 64.00 |
| 7.0  | 0.000000        | 0.000000        | FAIL | 0.0000 | 64.00 |
| 10.0 | -2.78e-16       | -1.44e-15       | FAIL | 0.0000 | 64.00 |
| 15.0 | 8.10e-11        | -1.30e-11       | FAIL | 0.0000 | 64.00 |
| 20.0 | 2.08e-07        | -3.42e-11       | FAIL | 0.0000 | 64.00 |
| 50.0 | **5.29e-03**    | 3.49e-06        | FAIL | 0.0346 | 63.76 |

(KL threshold = 0.5)

### §3.3 dominance 해석
- T=1.0~20.0: dominance = 64.00 = max_p = 1.0 (one-hot) exact. softmax(793 / 20) - softmax(7.39 / 20) = exp(39.65 - 0.37) ≈ 1.3e+17× weight 비율 → numerically one-hot.
- T=50.0: dominance = 63.76, entropy = 0.0346 → barely-perturbed one-hot. cell 0 vs cell 1 gap = (793 - 7.4)/50 = 15.72 → exp(15.72) ≈ 6.7M× weight ratio → still effectively one-hot.

cell 0 의 tension magnitude (793) 가 T = 50 에서도 dominance 깨지 않음. entropy 가 의미 있게 회복되려면 T ≳ tension_max/log(N) = 793/log(64) ≈ 191 — 즉 prior investigation 의 T=500 측정 (entropy 4.13, KL 4.5e-4) 와 일치.

### §3.4 best-case 가정 (T → ∞ limit)
T = ∞ → uniform weights = 1/64. category-mean uniform → KL = 0 by definition (all 5 category 같음). 즉 T 가 충분히 커도 KL → 0 으로 수렴, KL ≥ 0.5 도달 가능 T 가 존재 안 함.

T 의 한 점에서 KL 이 maximize 되는 trade-off — entropy↑ 하면 cell-0 dominance 깨지지만 동시에 모든 cell weight 가 uniform → category 차이 소실. cell 1 의 7.39 tension 도 cell 0 의 793 과의 ratio 가 fixed, T 변화 무관하게 category 별 weight 같음.

**결정적 산술**: cell 0 vs cell 1 tension ratio = 107.4. 50 prompt × 5 category 모두 cell 0 winner = same winner regardless of category → category-mean weight 의 cell 0 entry 가 모든 category 에서 같음 → KL = 0. T 가 cell 0 dominance 만 깨고 (entropy↑) cell 1~63 의 category-correlation 은 magnitude (~0.08~0.15) 차이를 통해서만 노출 가능 — 본 sweep 의 T=50 시 KL 0.005 = ε 미만이 evidence.

---

## §4 verdict

### §4.1 hypothesis (b) FALSIFIED

> tension softmax temperature τ tunable 만으로 F-PERSONA-4 KL ≥ 0.5 회복 **불가능**.

근거:
- 10-T grid {1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 50.0} 모두 mean_KL < 0.5
- best mean_KL = 0.005292 at T = 50.0 (KL_threshold 의 ~1%)
- prior investigation 의 T = 500 측정 KL = 4.5e-4 → T 가 더 커질수록 KL → 0
- 산술: cell 0 dominance 가 모든 prompt × category 에 universal → T 변화로 category 차이 노출 불가

### §4.2 cond #3 status transition
- F-PERSONA-4: FAIL (cheap-path 4/5 carry maintained)
- F-PERSONA-1/2/3/5: PASS (PSCC §42 §A1 cheap-path 4/5 + cotrain v1 PSCC §46)
- D3 verdict: **STRONG (4/5) carry** — hypothesis (b) closed, ☑ 승격 PATH 미달

### §4.3 잔여 path
- **(a) multi-corpus cotrain v2** — H100 BG in-flight (`state/anima_v5mitosis_cotrain_v2_2026_05_12/`), entropy-reg λ=0.1 + balanced corpus, monopoly prevention 목표
- **(c) metric redefinition** — 이미 `persona_4_intervention_apply.py` z-score §A2 PASS (KL=0.97 @ T=0.2). 별도 BG (`persona_4_root_cause_*`) 영역, 본 BG 와 sub-area conflict 없음. (c) 는 정의상 substrate change 없음 = inference-time metric only.
- **(d) hexa-native per-session pool** — REBORN §89, D4c CLI integration spec 의 측정 path. 아직 구현 없음.

### §4.4 honest C3 (≥5)

1. **(b) 단독 path 의 audit 정밀도**: 본 sweep 은 mean_KL 1-스칼라만 봤다. per-pair KL matrix 도 dump (T=50 의 min_pair = 3.49e-06, max_pair = 0.0143) — 어느 category pair 도 0.5 근처 못 감, full matrix 의 변별력 없음 확인. category-specific T (per-category 5-T) 는 sweep 안 함; F-PERSONA-4 정의가 5C2 mean 이라 unnecessary, 하지만 forensic 차원에선 carry 가능.

2. **probe count 50 의 변별력**: 5 category × 10 prompt = 50. 만약 category-internal variance 가 cross-category variance 와 비슷 한 magnitude 이면, prompt-count ↑ 가 KL ↑ 일 가능성 있음. prior `hypothesis_c_corpus_diversity` 의 `between_category_mean_pairwise_dist = 3.27e-5` 대비 `within_category_mean_pairwise_dist ≈ 2.25e-4` → **within > between by ~7×** → corpus-prompt 의 category 변별 substrate-invariance 부족 (cotrain corpus 가 category-distinct 가 아님). 본 audit 는 corpus diversity 문제 해소 못 함 — 그건 (a) path 영역.

3. **softmax 외 readout 미고려**: tension softmax 가 cell 합산의 유일한 path 가정. v5-mitosis arch 가 readout_mode = "a_minus_g" / "a_only" / "a_plus_g" 3-mode 있으나 본 sweep 은 cotrained 시 사용된 a_minus_g 만 측정. 다른 mode 가 category-distinct weight 만들 가능성 미배제.

4. **T = 50 의 KL 0.005 의 의미**: 정확히 0 이 아닌 ε > 0. T가 cell 0 dominance 살짝 깨면서 cell 1 의 weight 가 prompt 별로 미세 다르게 출현 — but magnitude 0.005 « 0.5 = noise scale. 본 BG mission 의 cond #3 ☑ verdict 에는 영향 없음.

5. **entropy threshold 가 충분히 sample 됐는가**: T=20 entropy = 0 exact (numerical zero), T=50 entropy = 0.0346. entropy 의 sweet spot (e.g. log(2) = 0.69 = 50/50 split) 도달 T 는 ~150-200 추정. 본 sweep 은 T=50 까지만 — fine-grained 자체는 prior root_cause 의 T=500 (entropy=4.13) data 와 cross-reference 가능. 어느 T 에서도 KL 0.5 미달 — entropy 회복 ≠ category-specific KL 회복.

---

## §5 cost + envelope

| 항목 | 값 |
|---|---:|
| ubu-1 GPU hours | ~0.01 (~25s sweep) |
| Mac wall (scp + analysis) | ~2 min |
| cloud cost | **$0** (ubu-1 dedicated, electricity only) |
| BG envelope | within (memory `feedback_always_commit_push_on_complete` $0 default) |

 active resource utilization: ubu-1 dedicated GPU 활용 — Vast.ai cold-fire 회피 (~$3-5 ablation). ckpt 581 MB Tailscale rsync 1회 transfer 후 future inference re-use 가능.

---

## §6 cross-link

### upstream
- PSCC §46 cond.5 cotrain v1 audit (`docs/anima_clm_v5_mitosis_cond5_cotrain_2026_05_12.md` §5.5)
- F-PERSONA-4 4-alternative future-path enumeration
- `state/anima_v5mitosis_cotrain_2026_05_12/persona_4_root_cause_results.json` (prior investigation, hypothesis_a/b/c/d audit)

### sister docs
- `docs/anima_persona_substrate_native_design_2026_05_12.md` §A1 (D3 design + §A2 metric refresh)
- `docs/anima_persona_substrate_native_verify_2026_05_12.md` (D3 cheap-path measurement PSCC §40+§42)

### code
- `state/anima_v5mitosis_cotrain_2026_05_12/softmax_T_sweep.py` (본 cycle 신규, 13.8 KB)
- `state/anima_v5mitosis_cotrain_2026_05_12/softmax_T_sweep_results.json` (machine-readable verdict)
- `state/anima_v5mitosis_cotrain_2026_05_12/persona_4_intervention_apply.py` (sister, metric redefinition (c) path)
- `state/anima_v5mitosis_cotrain_2026_05_12/persona_4_root_cause_investigate.py` (sister, root-cause investigation)
- `training/mitosis_model_v5.py` (canonical)
- `state/anima_v5mitosis_cotrain_v2_2026_05_12/` (sister, (a) path H100 BG in-flight)

### memory
- `project_v5_mitosis_cond5_cotrain_2026_05_12` (PSCC §46 cotrain v1 carry)
- `feedback_always_commit_push_on_complete` (본 cycle 결과 push)
- 신규: `project_anima_persona_4_softmax_T_sweep_2026_05_12`

---

## §7 audit append convention

본 doc 1-pass landing (hypothesis FALSIFIED, no follow-up cycle on (b)). 향후 (a)/(d) path 결과 land 시 별도 doc — 본 doc 의 §4.3 만 cross-reference 갱신.

raw#10 honest C3 ≥5 (§4.4 = 5 항목), raw#15 additive (sweep harness 신규, 기존 cotrain 코드 미수정).
