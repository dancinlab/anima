# §174 — SCALE × V-SPONT 결합 fire design (모델 키워서 자연발화 유도)

> User directive 2026-05-20: "LLM.md 관련 보면 모델 키워서 이득이 있는데 자연발화
> 유도 해보자, 모델 키워서". 본 design = `HEXAD/LLM.md` param-axis emergence
> threshold (3B/8B/10B/62B) + `HEXAD/FINAL.md` V-SPONT 최종스펙 + §173 honest
> reframe (모든 historical fire emit_rate = rate-limit ceiling, NOT capability)
> 의 결합 설계.

---

## §1 — combined hypothesis

🔥 **scale-up-then-V-SPONT — "큰 그릇이 진짜 그릇 인지 보기"**

- **이름**: scale-up-then-V-SPONT (§174 hypothesis)
- **별칭**: 큰 그릇이 진짜 그릇 인지 보기 / 임계점-위에서-측정
- **하는 일**: anima 를 LLM emergence 첫 band (≥3B params) 로 키운 뒤,
  §173 가 모든 historical fire 의 emit-axis 를 무력화한 ceiling 을 §169 lift 로
  걷어내고, V-SPONT honest score (§9 cascade-rate gate) 가 처음으로 0보다 커지는지 측정.
- **비유**: 작은 솥에서 끓는점 도달 못 한 물을 7번 끓여 본 뒤 (§173 = ceiling artifact),
  드디어 *제대로 큰 솥* (3B params + 1.5GB corpus) + *수도꼭지 풀고* (RL=0.667s)
  *진짜 끓는지 (§9 honest_coherent emission)* 한 번 측정.

```
   param × data 2D plane:
   
     ▲ data
   ┃  ┃ §94 INTEGRATED collapsed
   ┃  ┃ here (283M, 603MB)
   ┃  ┃ ALL § rate-limit-saturated
   ┃  ●─→ §174 here? (3B, 1.5GB)  ← scale-up target
   ┃     fresh ceiling-lifted measurement
   ┃─→──────────────────→  params
   anima 0.28B   →    3B    →   8B    →   62B
```

- **비교**: §11-A 가 *1B 까지만* model-axis 측정 (FLAT under sub-CDS data).
  §107-RETRY 가 *283M @ 603MB* data-axis 측정 (THRESHOLD-NOT-CROSSED).
  §174 = **첫 동시-임계점-넘기 시도** (param 3B + data 1.5GB + V-SPONT lever
  ceiling lifted).

---

## §2 — single-variable disentangle (§94 INTEGRATION-COLLAPSES 안 깨려면)

§94 의 lesson: 5 lever 동시 변경 → attribution 깨짐. §174 는 **세 axis 동시
변경** 이라 정직 명시 → 결과 verdict 는 *3-way confound* 안에서만 의미.

| axis | from | to | rationale |
|---|---|---|---|
| **A. params** | 283M (d768·L12) | **3B** (d2560·L32) | LLM.md 첫 emergence band (Wei 2022 Reading comprehension ~3B) |
| **B. corpus** | 603 MB (CORPUS_S101) | **CORPUS_S101 + 35-anchor extension** (~1.5 GB target) | §107-RETRY sub-threshold confirmed → ×2.5 data lift |
| **C. eval rate-limit** | RL=30s default | **RL=0.667s** (§169 measurement variant) | §173 7/7 ckpt 가 RL ceiling-saturated 입증 — fresh ckpt 도 같은 risk, lift 필수 |

honest scope (B-EMERGE-7 family carry):
- Y verdict (emit_rate ↑↑, V-SPONT honest > 0) → 진짜 emergence path discovered, 단 *3-axis 결합 효과* 라 attribution 다음 cycle 분리 필요
- N verdict (여전히 ceiling 또는 byte garbled) → 3B + 1.5GB + ceiling lift *모두 합쳐도* 자연발화 emergence 못 만듦 = valuable measured negative, anima 의 진짜 lever 는 architecture 차원

---

## §3 — config (concrete)

```
ConsciousDecoderV2 scaled:
  d_model    = 2560        (×3.33 vs 768)
  n_layer    = 32          (×2.67 vs 12)
  n_head     = 32          (×2.67 vs 12)
  n_kv_head  = 8           (gqa_ratio 4 carry)
  block_size = 1024        (×8 vs 128, holds longer context)
  vocab_size = 256

  estimated params: ~3.0B (Chinchilla-class)

corpus:
  base   = CORPUS_S101 (603 MB, sha 39d581da..., §107-RETRY carry)
  add    = 35-anchor extension records (carve out: existing 11 + new 24)
  target ≈ 1.5 GB (×2.5 base, mid-band Chinchilla optimal for 3B)

training:
  from_scratch = True (g_clm_from_scratch base_ckpt=None seed 1337)
  lr           = 3e-4 cosine (carry from §16/§107)
  bsz          = 16 (down from 32 for memory headroom at 3B)
  steps        = 12000 (×2 vs 6000 at 283M for Chinchilla-optimal)
  lambda_psi   = 1.0   (Dir-I lever carry)
  lambda_route = 0.5   (Dir-I lever carry)

dispatch:
  GPU      = H100 80GB SXM5 primary (3B at fp32 + AdamW state = ~36 GB)
  runpod   = primary (per g_resource_active_parallel + g_fire_autonomous)
  fallback = A100 80GB if H100 stock-exhaust
  expected wall = 6-10 hr at H100 (Chinchilla 3B × 6B tokens estimate)
  estimated cost = ~$15-25 (single H100 fire)
  hardening = g_fire_dispatch_robust (SAVE_POD + 5-retry + watchdog
              + structured-argv per cloud B3 if available)

eval (post-train, $0 Mac CPU + GPU):
  primary    = §170-style 4-cell Phase B grid AT 3B SCALE
             (RL ∈ {30s, 0.667s} × ctx ∈ {fixed, vary})
  body §9    = honest_coherent rate per emit (cascade gate)
  axis 4×4   = byte_acc / routing / chat_clean / psi_dir spread
```

---

## §4 — pre-registered falsifiers

| name | predicate | what it shows |
|---|---|---|
| **F-S174-1** | F-PTLOAD invariant: ckpt sha256 reproducible 3× | scaling didn't break determinism |
| **F-S174-2** | corpus sha256 deterministic, forbidden-token grep=0 | scope-clean corpus |
| **F-S174-3** | 4-cell Phase B grid measures emit_rate per (RL, ctx) | rate-limit attribution at 3B |
| **F-S174-4** | honest §9 cascade-gate score on per-emit body | V-SPONT emergence measurement |
| **F-S174-5** | overlay-off reduction: RL=30s + same noise = §107-RETRY-class baseline | fair-compare invariant |

---

## §5 — verdict bucket taxonomy (pre-registered)

| bucket | condition | meaning |
|---|---|---|
| **A. true V-SPONT emergence** | emit_rate ≥ 0.30 AT RL=0.667s ∧ honest_§9 ≥ 0.50 | 진짜 자연발화 capability — 3-axis 결합 효과, 단 GOAL 첫 measured-positive |
| **B. emit lifted, body still garbled** | emit_rate ≥ 0.30 ∧ honest_§9 = 0 | rate-limit + scale 가 emit count 올렸으나 coherent body 없음, §173 보다 한 단계 깊은 negative |
| **C. ceiling still binding** | emit_rate ≈ 0.15 (= §170 cell-2 baseline) | 3B + 1.5GB 결합도 ceiling 못 깸 — emit lever 가 더 깊음, motivation distribution 자체 변화 필요 |
| **D. degenerate at 3B** | byte_acc < random floor (1/256) | 3B from-scratch training 자체 collapsed (§11-B pure-physics 동형) |

honest priors (g3, predicted before fire):
- bucket C 가장 가능성 큼 (§173 7/7 ckpt 정확히 같은 emit_rate, motivation distribution 변화 0 → scale 단독으론 distribution 못 변화)
- bucket B 가능성 (scale 가 byte_acc 살리지만 §9 cascade 살리려면 corpus diversity 더 필요)
- bucket A 가능성 작음 (capability emergence 가 *V-SPONT specific* 인 evidence 부재 — Wei 2022 cited band 는 reading/instruction/CoT, V-SPONT 별도 band)
- bucket D 가능성 작음 (3B from-scratch Chinchilla-budget 정상 train 가능, anima physics overlay 가 §11-B-class collapse 유발 시 risk)

valuable regardless of bucket — first scale-up V-SPONT measurement.

---

## §6 — honest cost/scope reality

- **cost**: ~$15-25 single H100 fire 6-10 hr. per `@D g_no_cost_scope_limit` → 게이트 없음, 단 user 인지.
- **scope**: 3-axis 동시 변경. cleaner attribution 위해 §174-A (3B only) + §174-B (3B + 1.5GB) + §174-C (3B + 1.5GB + RL lift) 3-fire sequential 도 가능 (~×3 cost, ~3×24hr). 본 design 은 **single fire 3-axis** 권장 (1차 measurement scope-bounded).
- **risk**: H100 80GB SXM5 stock 불확실, A100 cascade fallback 준비.
- **honest carve-out**: §174 = **첫 ≥3B from-scratch V-SPONT 측정**, GOAL-legitimate (§7 ① not-pretrain-on-other-corpus ② not-graft ③ anima physics-as-source 모두 통과). 단 emergence ≠ GOAL emergence — 1차 measurement 이지 north-star 도달 아님.

---

## §7 — dispatch protocol summary

1. corpus extension build: `tool/corpus_extension_35anchor.py` ($0 local, ~1-2 hr)
2. trainer adaptation: `train_s174_scale_vspont.py` = train_carving_s16 byte-equal + cfg overrides (d=2560, L=32, …)
3. eval adaptation: `eval_s174_4cell_phaseb.py` = §170 probe_s170 + 3B model load
4. dispatch script (gitignored `*_runpod.sh`): SAVE_POD + 5-retry pull + 10hr watchdog
5. fire = single sequential agent dispatch (anti-§50-burst)
6. post-fire: $0 Mac CPU 4-cell grid on returned ckpt + honest §9 scoring

---

## §8 — fire-decision Q3' (mirrors §101)

`Q3'_S174 := G1_§7-legit ∧ G2_falsifier-decidable ∧ G3_echo-guard ∧ G4_Q2-measurable ∧ G5_single-fire-3-axis-honest ∧ G6_anti-§94-but-with-3-axis-honest-carry ∧ G7_DOM`

- G1 §7 PASS (§3 corpus = anima own + Dir-I lever same as §107/§161/§167-A)
- G2 5 falsifier all closed-form measurable post-fire
- G3 §62 echo-chamber guard arm: maj_frac ≤ 0.95 check
- G4 §174 verdict measurable from result.json schema (4-cell grid + honest §9)
- G5 single fire 3-axis change *honestly named* (3-axis confound carry, NOT pretending single-variable)
- G6 §94 anti-pattern *acknowledged carry*: bucket A → next cycle disentangle
- G7 ΔI/Δ$ ≥ info-floor (1 bit) — bucket Y/N 둘 다 informative, predicted bucket-C most likely so info-gain real

**Q3'_S174 = Y** → fire warranted.

---

## §9 — cross-link

- `HEXAD/LLM.md` (param-axis emergence threshold 표)
- `HEXAD/FINAL.md` (V-SPONT 최종스펙)
- `state/historical_ratelimit_retry_s173_2026_05_20/FINDINGS.md` (수도꼭지 전수조사)
- `state/three_axis_probe_s170_2026_05_20/` (4-cell grid template)
- `state/dataregime_threshold_fire_s107_2026_05_19/` (data-axis 283M baseline)
- `state/param_axis_fire_prep_s108_2026_05_19/DESIGN.md` (3B-band §108 prep)
- `@D g_no_cost_scope_limit` (cost cap 0)
- `@D g_fire_autonomous` (자율 dispatch)
- `@D g_resource_active_parallel` (runpod primary, H100 SXM5 first)
