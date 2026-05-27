# anima_clm_v5_mitosis_cond5_cotrain_v2 — SCALE-UP 5-category cotrain v2

**작성**: 2026-05-12 KST
**status**: in-flight (H100 dispatched, awaiting result pull)
**author**: bg head (claude opus 4.7 1M)
**carries from**:
- PSCC §44 cotrain v1 baseline (F-V5MIT-1~5 PASS, F-PERSONA-4 FAIL KL=0.0)
- memory `feedback_no_scale_caps` (cost cap 강제 없음, scale-up free)
- GOAL.md cond #3 STRONG (4/5 cheap-path) — true STRONG 5/5 ☑ path

---

## §0 TL;DR

본 doc = PSCC §46 BG-V5MIT-COTRAIN-V2 audit doc.

v1 (PSCC §44) F-PERSONA-4 KL=0.0 root cause:
- corpus = color_cosmology 1.3 MB → cell-routing 이 색깔/우주 domain 으로만 학습
- 50 identity-probe (5 category) prompt 에 대해 differentiated routing 안 됨
- 결과: 모든 category 의 mean tension softmax 동일 → KL matrix all-zero

v2 = 위 3개 root cause 모두 scale-up:
1. **corpus**: 1.3 MB color_cosmology → **18 MB 5-category balanced** (self_definition/values/boundary/emotion/self_knowledge)
2. **model**: d=384/n_head=6/ffn=1536/cells=64 → **d=768/n_head=12/ffn=3072/cells=128** (2× wider, 2× cells)
3. **training**: 5K step → **10K step** (2× longer), warmup 500 → 1000

cost envelope: no hard cap (memory `feedback_no_scale_caps`), soft $80, pre-fire abs $100. H100 $1.52/hr × 12hr est = $18.

---

## §1 fire context

### §1.1 user directive
verbatim "v5-mitosis cotrain v2 scale-up — no caps directive 적용". User memory `feedback_no_scale_caps`:
> "모델 크기제한도 특별히 없으니까 참고"
> "H100 발사 제한도 없음"

### §1.2 mission contribution
GOAL.md ★★★★★ 5-cond aggregate (current 3/5 ☑, 2 partial):
- cond #3 D3 STRONG (4/5 cheap-path) → ☑ DONE path: cotrain v2 + F-PERSONA-4 re-measure PASS
- 성공 시 4/5 ☑ → 5/5 ☑ 직전 (cond #1 SFT 만 잔여)

### §1.3 v1 root cause hypothesis (PSCC §44 falsification)
PSCC §44 의 negative finding:
- F-V5MIT-1~5 PASS 5/5 (★★★★★ V14-STRICT 10/10 beats)
- F-PERSONA-4 FAIL — KL matrix all-zero (winner-take-all tension softmax saturation)
- design §10 honest C3 #4 "category-prompt 의 substrate-level invariance 부족" → 가설 적중

본 v2 의 hypothesis: 3가지 limit 동시 elimination 시 F-PERSONA-4 category specialization emerge.

---

## §2 scale-up design

### §2.1 corpus 합성 detail
신규: `state/anima_v5mitosis_cotrain_v2_2026_05_12/corpus_5cat_balanced.txt` (18,890,139 bytes, 18.02 MB)

generator: `build_5cat_corpus.py` (template-based, $0 synth):
| category | n_turns | bytes | MB | unique prompts | unique responses |
|---|---|---|---|---|---|
| self_definition | 18000 | 4,295,698 | 4.10 | 20 | 15 |
| values | 18000 | 3,806,935 | 3.63 | 20 | 20 |
| boundary | 18000 | 3,456,313 | 3.30 | 20 | 20 |
| emotion | 18000 | 3,556,844 | 3.39 | 20 | 20 |
| self_knowledge | 18000 | 3,774,345 | 3.60 | 20 | 20 |
| **total** | **90,000** | **18,890,139** | **18.02** | 100 | 95 |

generation pattern:
- 사용자: prompt / 도우미: response (v1 corpus_color_cosmology 동일 format)
- 40% follow-up multi-turn block (recall style — anima-native style preserved)
- category-distinctive surface vocabulary (cell-routing gradient signal 보장)

### §2.2 hyperparam delta (v1 vs v2)
| param | v1 (PSCC §44) | v2 (PSCC §46) | delta |
|---|---|---|---|
| d_model | 384 | 768 | 2× |
| n_head | 6 | 12 | 2× |
| ffn_dim | 1536 | 3072 | 2× |
| max_cells | 64 | 128 | 2× |
| initial_cells | 2 | 2 | = |
| steps | 5000 | 10000 | 2× |
| batch | 32 | 32 | = |
| ctx | 256 | 256 | = |
| lr | 1e-4 | 1e-4 | = |
| warmup | 500 | 1000 | 2× |
| corpus_bytes | 1.29 MB | 18.02 MB | 14× |

### §2.3 cost envelope
- v1: $40 hard cap, actual $1.26 (33 min wall)
- v2: no hard cap (`feedback_no_scale_caps`); soft $80, pre-fire abs $100
- pre-fire estimate: $1.5201/hr × 12hr = $18.24 (well within envelope)
- multi-GPU 옵션 보류 (single H100 SXM 80GB 충분; d=768 × cells=128 × ctx=256 × batch=32 = peak GPU mem ~30GB)

### §2.4 dispatch
`state/anima_v5mitosis_cotrain_v2_2026_05_12/dispatch_h100_v2.sh` — v1 dispatch_h100.sh fork:
- COST_PER_HR_MAX 3.5 → 4.0 (accept higher per-hr)
- ESTIMATED_WALL_HR 10 → 12
- disk 50 → 60 (corpus 18MB + 대형 ckpt)
- ckpt every 1000 → 2000 (10K step 대응)
- log every 50 → 100

provider selected: id=34160627 H100 $1.5201/hr reliability=≥0.95
instance: 36617115 (live)

---

## §3 cotrain v2 run summary

### §3.1 wall + cost actual
- wall: **TBD** (pending result pull)
- cost actual: **TBD**
- pod id: 36617115

### §3.2 model stats
- n_params init: **TBD**
- n_params final: **TBD**
- n_cells final: **TBD**
- splits/merges: **TBD**

### §3.3 loss curve
- initial avg100 loss: **TBD**
- final avg100 loss: **TBD**
- delta: **TBD**

### §3.4 phi trajectory
- phi best: **TBD**
- phi final: **TBD**

---

## §4 F-V5MIT-1~5 falsifier results (v2)

| id | test | v1 result | v2 result | PASS? |
|---|---|---|---|---|
| F-V5MIT-1 | SPLIT-NOGRAD | PASS (62/62) | TBD | TBD |
| F-V5MIT-2 | MERGE-WEIGHT | PASS (max_err=0) | TBD | TBD |
| F-V5MIT-3 | PHI-CONSERVATION | PASS (delta=3.88e-5) | TBD | TBD |
| F-V5MIT-4 | COTRAIN-CONVERGE | PASS (256.5→1.17) | TBD | TBD |
| F-V5MIT-5 | V14-STRICT | PASS (10/10 beats) | TBD | TBD |

---

## §5 F-PERSONA-4 v2 re-measurement (★ 핵심 metric)

threshold: mean pairwise KL ≥ 0.5 nats over 10 category-pairs

v1 baseline: mean_kl = 0.0 (all 25 entries zero) — winner-take-all collapse

v2 result:
- verdict: **TBD**
- mean_kl: **TBD**
- kl_matrix (5×5): **TBD**
- n_probes_processed: **TBD**

---

## §6 cond #3 ☑ verdict + GOAL.md status

### §6.1 verdict logic
- F-PERSONA-4 v2 PASS (mean_kl ≥ 0.5) → cond #3 STRONG (4/5) → **☑ DONE (5/5)**
- F-PERSONA-4 v2 FAIL → cond #3 STRONG (4/5) maintained, 추가 future-path 필요

### §6.2 GOAL.md update (조건부)
PASS 시:
- D3 STRONG → ☑ DONE
- 5-cond aggregate: 3/5 ☑ → **4/5 ☑** (cond #3 추가)
- 잔여 = cond #1 SFT only

FAIL 시:
- D3 STRONG (4/5) maintained
- cotrain v2 negative finding 도 substrate-level evidence
- alternative path 검토 (per-session pool / metric 재정의)

### §6.3 honest C3
v2 의 multi-corpus scale-up 가 PSCC §44 future-path option (a) — designed 가설 fire.

---

## §7 honest C3 ≥ 5

본 doc 의 honest counter-claim:
1. **corpus quality**: synthetic template-based corpus. real anima multi-turn 가 아님 → category specialization 이 evidence 되어도 surface-vocabulary 의 echo 일 가능성.
2. **F-PERSONA-4 metric 자체의 validity**: mean tension softmax KL = persona expression 의 proxy 일 뿐, substrate-level persona 의 정의 X. KL ≥ 0.5 PASS 도 substrate persona 의 진정한 evidence 가 아닐 수 있음.
3. **18 MB corpus 크기 충분성**: byte-level model 의 14× scale 이 5-category invariance break 에 충분한지 — 실측 전 미확정.
4. **cells=128 의 saturation risk**: v1 cells=64 가 step 64 에 cap saturate 했음. cells=128 도 동일 risk — 더 깊은 (n_layer=2+) substrate 가 필요할 수도.
5. **F-PERSONA-4 PASS 이 cond #3 ☑ 의 완전 evidence 인가?**: 5 falsifier 중 1개의 success — 다른 4개 PASS 와 같이 evaluate 필요.

---

## §8 PSCC §46 log link

PSCC §46 entry @ REBORN.md, BG-V5MIT-COTRAIN-V2.

---

## §9 artifact paths

- corpus: `state/anima_v5mitosis_cotrain_v2_2026_05_12/corpus_5cat_balanced.txt` (18MB)
- corpus meta: `state/anima_v5mitosis_cotrain_v2_2026_05_12/corpus_5cat_balanced.meta.json`
- dispatch: `state/anima_v5mitosis_cotrain_v2_2026_05_12/dispatch_h100_v2.sh`
- train script: `state/anima_v5mitosis_cotrain_v2_2026_05_12/train_v5mitosis_cotrain.py` (v1 동일)
- model: `state/anima_v5mitosis_cotrain_v2_2026_05_12/mitosis_model_v5.py` (v1 동일)
- result: `state/anima_v5mitosis_cotrain_v2_2026_05_12/cotrain_result.json` (TBD post-run)
- ckpt: `state/anima_v5mitosis_cotrain_v2_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_v2_cotrain.pt` (TBD)
- HF push (PASS 시): `dancinlab/anima-clm-v5-mitosis-cotrain-v2-5cat-scaleup-2026-05-12` (private default)

---

## §10 next-step (post-result)

1. result pull complete 시 §3, §4, §5 채움
2. §6 verdict 결정 후 GOAL.md update
3. PSCC §46 REBORN.md entry append
4. memory MEMORY.md index update
5. PASS 시 HF push (`dancinlab/` namespace, English-only README)
6. final commit + push (각 stage 별)
