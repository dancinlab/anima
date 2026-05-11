# BG-NO_COTRAIN_CAP512-FIRE — substrate B (NO cotrain) × max=512 × 10-seed strict V14

## ts
2026-05-10 (verbatim auth: `OK NO_COTRAIN_CAP512_FIRE COST $5-15`, user 2026-05-10).
Lineage: §47-B (cap=128 0/5 V14_VIOLATED) → §56-B (cap=256 1/5 V14_VIOLATED) → **§61** (this BG: cap=512 boundary case).

## Mission

§61 paradigm-cap interaction unresolved: engine_ag no_cotrain @ cap=512 가 cap=128 의
V14_VIOLATED (실제로는 §47-B 0/5, mission text 의 "1/10" 은 §56-B 1/5 의 표기 변형으로
간주) 를 PASS rescue 하는지 검증. 기존 BG-LA pretrain ckpt 사용 (NO new training);
V14 mirror eval-only at cap=512 만 추가.

핵심 질문: cap → 512 까지 raise 시 EngineAG no-cotrain path 가 §51 v2-path-style
cap-conditional polarity 를 회복하는가? 회복하면 cap-conditional 이 모든 arch 에서
universal (단지 boundary 가 더 높을 뿐) 이고, 회복 못 하면 §56 의 **MULTI-FACTORIAL**
verdict 가 cap=512 까지 강화된다.

## Substrate (single, NO new training)

| ID | path | ckpt | paradigm |
|----|------|------|----------|
| B_bgla_pretrain_no_cotrain | EngineAG d=1024 GQA 24L (298.76M) | `/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt` | naive_pretrain (NO chat-cotrain) |

ckpt sha256_prefix: `4fc6eccce0def045` (per §56 verdict, will re-verify pre-fire).

Mirror substrate: `load_random_init(seed=s, preset="la_350m")` × 10 seeds.

## Run config

- `MAX_CELLS = 512` (vs §47 128, §56 256 — sole override)
- `V4_SEEDS = [42, 137, 271, 314, 1729, 7, 11, 13, 17, 19]` (10-seed strict; first 5 mirror §56 for cross-cap diff)
- `TRAINED_PROMPT_SEED = 1042` (mission spec; differs from §56's 42 — boundary case to break correlation w/ §56 mirror reuse)
- `N_TURNS = 200` (mirror §56 length for direct comparability)
- `SNAP_EVERY = 25`
- §30 all-fix mitosis (split_patience=3, split_noise=0.10, merge_threshold=0.005,
  merge_patience=30, lorenz_scale=0.05)
- Φ metric primary: `iit_phi_unnorm_b16` (Fiedler MIP, 16-bin spatial)
- Φ metric secondary: `proxy_phi` (in-engine proxy), only for V14 partial diagnostic
- Architecture: engine_ag 24L × 1024d × 16h GQA (BG-LA 350M, NO cotrain)
- Mitosis V5 §30 fixes (already in MitosisV5Engine), `max_cells=128` mission-line
  is **interpreted as `initial_cells = 16` (engine_g `n_cells`); the *cap* is 512**.
  i.e., max_cells param of MitosisV5Engine = 512.

### "max_cells=128 same" mission-line interpretation

Mission text says: "cap=512 (vs §47-B 128, §56-B 256) / max_cells=128 same".
Reading: "cap" = mitosis cap = `MAX_CELLS = 512`; "max_cells=128 same" is a mission
typo / restatement of "the OTHER cap parameter (initial cell pool / engine_g n_cells)
remains at the §57 lineage value 128 — but the §47/§56 EngineAG used initial_cells=16
(EngineG `n_cells_init=16`)". For consistency we use **MAX_CELLS=512** (the variable
that gates mitosis split) and let `initial_cells` come from `eg.cell_pool_init.shape[0]`
(EngineAG default = 16).

This matches §47/§56 protocol exactly except for the single MAX_CELLS override.

## H100 fire (eval-only, NO training)

- 1× H100 SXM (SECURE first, COMMUNITY fallback) ~$2.99/hr
- expected wall-time: 30 min (§56 was 19min on Mac CPU; H100 ~3-5× faster on
  forward, but mitosis Φ MIP at N≤80 cells is CPU-bound — net ~10-15min for 11 runs)
- env: runpod-torch-v280 + `--break-system-packages` (own 30 mandate-5)
- pull artifacts: `result.json`, `run.log`, `traces.json` (per-snapshot trajectories)
- **NO new ckpt to pull** — eval-only (own 30 inverse exception)

## Falsifier

- **F-CAP512-1**: B max=512 V14_PASS_STRICT (10/10 trained > random, p=0.002) → ★★★★★
  cap-conditional polarity rescued at 512; §56 MULTI-FACTORIAL verdict downgraded;
  cap-conditional UNIVERSAL claim restored (with cap-boundary parameter).
- **F-CAP512-2**: B max=512 V14_PARTIAL (7-9/10) → ★★★★ partial rescue; cotrain-
  exercise hypothesis attenuated but not falsified at cap=512.
- **F-CAP512-3**: B max=512 V14_VIOLATED (0-3/10) → §56 MULTI-FACTORIAL preserved
  and reinforced at cap=512; cotrain-exercise is the cap-INVARIANT driver in
  EngineAG path.
- **F-CAP512-AMBIGUOUS**: 4-6/10 → underpowered; future test required.
- **F-CAP512-COSTBLOWN**: actual_cost > $25 → BG aborts mid-run, partial result emit.

## Cost envelope

- target $5-8 (single H100 ~30min)
- envelope authorized $5-15 (verbatim user 2026-05-10)
- hard kill $20 (orchestrator-side cap)
- abort $25 (F-CAP512-COSTBLOWN; spec-side cap, in addition to orchestrator $20 cap)

## Verdict matrix (4-bin)

| Outcome | Bin | Star | §51/§56 ledger update |
|---|---|---|---|
| 10/10 PASS | F-CAP512-1 | ★★★★★ | cap-conditional UNIVERSAL restored at boundary 512 |
| 7-9/10 PARTIAL | F-CAP512-2 | ★★★★ | cotrain-exercise attenuated; cap-conditional weakly universal |
| 4-6/10 AMBIGUOUS | F-CAP512-AMB | ★★★ | n=10 underpowered; replicate at n=20 next |
| 0-3/10 VIOLATED | F-CAP512-3 | ★★★★★ (negative) | §56 MULTI-FACTORIAL strengthened; cotrain is cap-INVARIANT EngineAG driver |

Note: F-CAP512-3 (VIOLATED) is **★★★★★ negative** because it is the cleanest
disambiguation we can buy at this budget — same arch, same paradigm, only cap
varies, and three caps (128/256/512) would all VIOLATE. Cotrain-conditional
polarity in EngineAG path is then settled.

## Constraints (raw / own)

- raw#9 — `state/.../run.py`, `orchestrator.py` local-only (gitignored under state/)
- raw#15 additive — B ckpt loaded read-only (sha256 verified pre/post); no file mutation
- own 14 — V14 multi-seed strict mirror (10-seed, ★ tighter than §47/§56's 5-seed)
- own 22 — every metric scalar emit; verdict.md SSOT; **REBORN.md no direct append**
- own 30 — H100 mandates: PEP 668 `--break-system-packages`, scp ckpt verify pre-delete,
  pod retain on pull fail; **eval-only inverse exception**: NO new ckpt to pull,
  but `result.json` + `run.log` + `traces.json` MUST pull or pod retains
- own 38 — artefacts under `state/anima_no_cotrain_cap512_fire_2026_05_10/{spec.md,
  orchestrator.py, run.py, result.json, traces.json, run.log, verdict.md, cost_actual.json}`

## Output deliverables

| file | content |
|---|---|
| `spec.md` (this) | hypothesis + run config + verdict matrix |
| `orchestrator.py` | H100 provision + stage + fire + pull + delete |
| `run.py` | pod-side V14 10-seed cap=512 eval driver |
| `result.json` | full V14 verdict (trained Φ, 10 mirror Φ, n_beats, sign-p, verdict label) |
| `traces.json` | per-snapshot trajectories (trained + 10 mirrors) for diagnostics |
| `run.log` | timestamped pod-side run log |
| `cost_actual.json` | bal_before/after, actual_cost_usd |
| `verdict.md` | final verdict + cross-cap ledger update + honest C3 ≥7 |
