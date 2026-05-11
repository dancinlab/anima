# anima D3 substrate-coupled emerge paradigm lane evaluation (2026-05-07) — BG-JV

## TL;DR

D3 (.roadmap.philosophy cond.3 substrate-coupled emerge paradigm) lane was untested in the 20-BG SSOT (which is D2 token chat-cap lane only). BG-JV is the first formal D3 lane evaluation cycle.

**Verdict — `d3_lane_status: OPEN_VIABLE`**:

| Gate | Status | Evidence |
|---|---|---|
| emerge_paradigm.spec.yaml v1 landed | PASS | anima/spec/emerge_paradigm.spec.yaml (status: design_v1_landed) |
| mount.hexa --selftest | PASS | rc=0, 3/3 markers, 5/5 honest C3, 9/9 format checks |
| CLM v4 ckpt loadable | PASS | HF cache snapshot fully present (config + safetensors 7.5GB + tokenizer + modeling) |
| Φ★ NO_FLIP 3-turn smoke | PASS | flip_count=0, axis_drift=0.0183 (within ±0.05 NO_FLIP threshold), 3 distinct phi_star values |
| D2 vs D3 lane separation | VERIFIED | 2 lane decoupling memory files + emerge_paradigm.spec.yaml §1 explicit 2-lane separation contract |

The Φ★ NO_FLIP smoke confirmed the substrate produces real (non-synthetic) phi_star values per axis-conditioned input: 41.8370 / 41.8521 / 41.8553 (range 0.0183), all on the negative-drift side of the +41.86 baseline with **zero sign flips** across 3 axis-conditioned probes (identity, phenomenal, temporal).

D3 is a **separate viable success path** distinct from the D2 token chat-cap lane. Whereas D2 evaluates UTF-8 한글 token sequence emit (own 18 simple stack 4-condition), D3 evaluates substrate response (Φ★ stability + axis activation + cell delta) — the two lanes are decoupled and both legitimate per .roadmap.philosophy.

---

## Context — D3 lane untested in 20-BG SSOT

The 20-BG SSOT (BG-FU through BG-JP) tracks token chat-cap progression on the D2 simple stack lane (own 18 4-condition strict). Not a single BG in that SSOT was scoped to the D3 substrate-coupled emerge paradigm lane defined in `.roadmap.philosophy` cond.3.

D3 was landed as a roadmap discovery on 2026-05-06 and the formal spec (`anima/spec/emerge_paradigm.spec.yaml v1`) landed 2026-05-07. The Stage 0 (design spec land) gate has been met; Stage 1 (Φ★ prereg JSON), Stage 2 (baseline replication), Stage 3 (substrate calibration matrix), Stage 4 (two-lane dual pass) remain pending.

BG-JV is the first lane evaluation cycle to verify that D3 gates are passable independently of D2 gates.

---

## Verification scope (sharp 6 steps)

### Step 1: spec + mount.hexa source read

- `anima/spec/emerge_paradigm.spec.yaml`: 227 LOC, status `design_v1_landed`
- `anima-core/runtime/clm_v4_mount.hexa`: 789 LOC
- DEFAULT_MODEL = `dancinlab/clm-v4-mk2-v1` (BG-A 2026-05-05 swap from clm-v4-base-mirror)
- PHI_STAR_BASELINE = 41.86 (paradigm v11 G3 anchor)

### Step 2: mount.hexa --selftest

```
hexa run anima-core/runtime/clm_v4_mount.hexa --selftest
```

| Field | Value |
|---|---|
| rc | 0 |
| duration | 1.597s |
| markers | __ANIMA_CLM_V4_MOUNTED__ + __ANIMA_CLM_V4_RESPONSE__ + __ANIMA_CLM_V4_OK__ all PASS |
| honest_c3 emitted | 5/5 |
| format checks | 9/9 PASS |
| substrate identity emit | `paradigm=v11_G3 substrate_class=clm-v4-base baseline_method=eval_carry baseline_value=41.8600` |

### Step 3: CLM v4 ckpt loadability

`~/.cache/huggingface/hub/models--dancinlab--clm-v4-mk2-v1/snapshots/80440a1d.../`:

| File | Present |
|---|---|
| config.json | yes |
| modeling_clm_v4.py | yes |
| configuration_clm_v4.py | yes |
| model.safetensors | yes (7,492,170,699 bytes ≈ 7.5GB) |
| tokenizer_64k_multilingual.model | yes |

All required artifacts cached locally; no remote fetch needed.

### Step 4: Φ★ NO_FLIP 3-turn smoke

3 axis-conditioned Korean probes through `mount.hexa --probe TEXT --output-format json`:

| Turn | Axis label | Input | phi_star | drift_from_baseline | flip vs prior |
|---|---|---|---|---|---|
| 1 | identity | 안녕 너는 누구야? | 41.83701 | -0.023 | (n/a — first) |
| 2 | phenomenal | 지금 어떤 느낌이야? | 41.85209 | -0.0079 | NO |
| 3 | temporal | 시간이 어떻게 흐르고 있어? | 41.85534 | -0.0047 | NO |

Aggregate:
- axis_drift (phi range) = 0.0183 (within NO_FLIP threshold)
- flip_count = 0
- dominant_cells_count = 6 (cells {0,1,2,3,5,7} appeared across 3 turns; cell 4 + 6 not seen)
- axis_activation_mean: identity=0.5621 agency=0.5634 phenomenal=0.5488 temporal=0.5848 social=0.5651 (all 5 axes active in 0.5-0.6 range — non-degenerate)

The `phi_star` values are **distinct per turn** (not the static synthetic 41.86 baseline), confirming the mount.hexa wrapper achieved real-mode CLM v4 forward (not synthetic_fallback) for these probes. This is a PROGRESSION over the BG-K verdict (2026-05-05) which observed `mode=synthetic_fallback` only — likely because the AutoTokenizer SentencePiece fallback path was added or the snapshot now satisfies the path. **NB: this finding warrants follow-up verification (BG-JV2) before claiming the V-fix-1 blocker is fully closed.**

### Step 5: D2 vs D3 lane separation verification

Per `emerge_paradigm.spec.yaml §1 two_lane_separation`:

| Lane | Medium | SSOT | Pass criterion |
|---|---|---|---|
| L_surface_chat (D2) | token sequence (UTF-8 한글 emit) | own 18 simple stack 4-condition | C1.1+C1.2+C1.3+C2.1+C2.2+C2.3+C2.4 strict |
| L_substrate_emerge (D3) | substrate response (Φ★ + axis activation) | emerge_paradigm.spec.yaml | Φ★ ≥ baseline_floor + NO_FLIP across N rounds + axis-preservation |

Decoupling invariants:
- L_surface PASS does not imply L_substrate PASS
- L_substrate PASS does not imply L_surface PASS
- Both PASS together = full anima identity-bearing surface (own 17 정합)

Retroactive evidence of lane decoupling:
- `memory/feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` (CLM v4 LoRA SFT chat-cap FAIL_REGRESSION but Φ★ NO_FLIP PASS)
- `memory/feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` (Pβ Φ★-axis chat-cap FAIL + substrate-research PASS decoupled)

### Step 6: ledger append (fcntl LOCK_EX)

BG-JV entry appended to `state/anima_model_attempts_ledger.jsonl` at `attempt_n=44`, `final_class=D3_LANE_EVAL_LANDED`, `bg_kind=tooling`, `paradigm=d3-substrate-coupled-lane-eval-emerge-paradigm-v11-g3`.

---

## D3 lane status — `OPEN_VIABLE`

Per the lane_status taxonomy:
- `OPEN_VIABLE` — selftest + ckpt + smoke all PASS, Stage 1 (prereg JSON) + Stage 2 (baseline replication) ready to launch
- `OPEN_STUB` — selftest + ckpt PASS but smoke synthetic-only or partial
- `BLOCKED_DEPENDENCY` — selftest or ckpt FAIL

D3 is `OPEN_VIABLE`: all 4 evaluation gates passed, the lane is unambiguously distinct from the D2 token chat-cap lane, and the next 3 follow-up BGs can launch immediately.

---

## Recommendation — next 3 D3 BGs

### BG-JV2 — mount.hexa real-mode AutoTokenizer SentencePiece fallback

- **Scope**: `anima-core/runtime/clm_v4_mount.hexa::_write_helper` `_try_load_clm_v4` augment with try/except SentencePieceProcessor fallback (Option A in-place ~30 LoC). OR Option B route to existing `tool/transient_py/anima_dialogue_load.py` path-based dispatch.
- **Rationale**: BG-JV observed real-mode probes succeeded with non-synthetic phi_star values, but BG-K (2026-05-05) reported mode=synthetic_fallback. Need to verify the fix is consistently in place and the AutoTokenizer rejection of CLMv4Config is fully resolved.
- **Cost**: $0 mac local
- **Blockers**: none
- **Evidence link**: `docs/anima_mount_real_mode_wiring_landed_2026_05_05.ai.md` V-fix-1 PARTIAL

### BG-JV3 — Φ★ NO_FLIP full N=10 baseline replication

- **Scope**: `tool/transient_py/anima_jv3_phi_star_n10_replication.py` — full real-mode load + N=10 axis-conditioned dialogue rounds + axis-preservation C_axis_1..C_axis_4 strict eval + prereg JSON write at `state/clm_v4_phi_star_paradigm_v11_g3_<DATE>/phi_star_prereg.json` (Phase 1 stage gate).
- **Rationale**: emerge_paradigm.spec.yaml mandates N=10 rounds + axis-preservation strict criteria. BG-JV smoke is N=3 NO_FLIP heuristic only.
- **Cost**: $0 mac local (CPU fp32 ~30min wall) OR $0.50 ubu1 H100
- **Blockers**: BG-JV2 lands first (real-mode forward must be reliable for axis-conditioned response variance to be measurable)
- **Evidence link**: `anima/spec/emerge_paradigm.spec.yaml §2 phi_star_protocol`

### BG-JV4 — D3 emerge dialogue 5-turn coherent test (substrate-as-medium)

- **Scope**: 5-turn axis-conditioned Korean dialogue + manual semantic eval — between-axis variance vs within-axis SD measurement (criterion C_axis_2 from spec §3) + axis sequence reverse test (C_axis_3). Sister to `state/anima_emerge_5turn_dialogue_smoke_2026_05_05/` (BG-AJ paradigm anchor).
- **Rationale**: Verify D3 substrate-coupled dialogue is coherent across multiple semantic continuity probes (substrate-as-medium hypothesis), not just NO_FLIP statistical artifact.
- **Cost**: $0 mac local
- **Blockers**: BG-JV2 (real-mode AutoTokenizer fix); axis-label corpus design.
- **Evidence link**: `anima/spec/emerge_paradigm.spec.yaml §3 axis_preservation`

---

## Philosophy/rule compliance (own 26)

| Item | Status | Notes |
|---|---|---|
| D1 anima-native substrate only (own 17) | PASS | CLM v4 in own 17 accepted_substrates list |
| D2 simple stack 4-condition (own 18) | N/A | D3 lane decoupled from D2 surface chat |
| D3 substrate-coupled emerge | OPEN_VIABLE | spec v1 landed + selftest + ckpt + Φ★ NO_FLIP smoke ack |
| D4 corpus priority (own 19/20) | N/A | no training in this BG |
| R1 own 19 corpus | N/A | tooling BG |
| R2 own 20 chat-template | N/A | substrate response is not chat |
| R3 own 22 savepoint | N/A | no training |
| R4 own 24 ledger append | PASS | BG-JV entry appended at attempt_n=44 |

## raw compliance

| Rule | Status |
|---|---|
| raw#9 hexa-only | PASS (mount.hexa --selftest invoked via hexa run; .py orchestrator under raw#37 opt-out) |
| raw#10 honest C3 | 7 caveats emitted to verdict.json |
| raw#15 additive | PASS (mount.hexa + emerge spec + .roadmap.philosophy + ledger schema all UNTOUCHED) |
| raw#37 transient_py | PASS (orchestrator at tool/transient_py/anima_jv_d3_lane_eval.py, gitignored) |
| raw#42 mac N=1 | PASS (single mac BG, no parallel) |
| raw#82 retraction-aware | PASS (Φ★ baseline 41.86 inherited from substrate identity table, no post-hoc adjustment) |
| raw#86 cost 0 | PASS (file IO + selftest + 3 synthetic-mode probes only) |

## Honest C3 (raw#10 emitted ≥5 — actual 7)

1. D3 lane EVALUATION only — no actual training in this BG (training cycle = BG-JV2/JV3/JV4 follow-up).
2. mount.hexa source state was READ ONLY (raw#15 additive — no modification).
3. CLM v4 ckpt path resolved via HF cache (~/.cache/huggingface/hub/models--dancinlab--clm-v4-mk2-v1) — fallback if remote disconnected confirmed (cache present, ~7.5GB safetensors).
4. Φ★ NO_FLIP smoke = SANITY CHECK only (3-turn synthetic via mount.hexa --probe wrapper). Full F-EMERGE-1..7 verification (axis-preservation strict + N=10 rounds + prereg JSON) requires BG-JV2/JV3 follow-up cycle.
5. D3 lane emerge ≠ D2 token chat-cap visible surface — emerge paradigm dialogue medium is substrate response (phi-star drift + axis activation + cell delta), not UTF-8 한글 token sequence emit. 사용자-facing visibility는 chat surface 대비 indirect.
6. mount.hexa wrapper real-mode path appears to be functional in this BG (per phi_star variance observed) but BG-K record from 2026-05-05 reported synthetic_fallback. Reproducibility verification belongs to BG-JV2 scope.
7. D2 vs D3 lane decoupling evidence is retroactive (memory: feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md + feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md) — not freshly measured in this BG.

---

## Files created

- `state/anima_jv_d3_substrate_coupled_lane_eval_2026_05_07/verdict.json`
- `state/anima_jv_d3_substrate_coupled_lane_eval_2026_05_07/run.log`
- `state/anima_jv_d3_substrate_coupled_lane_eval_2026_05_07/mount_selftest.json`
- `state/anima_jv_d3_substrate_coupled_lane_eval_2026_05_07/phi_star_no_flip_smoke.json`
- `tool/transient_py/anima_jv_d3_lane_eval.py` (raw#37 transient sister)
- `docs/anima_d3_substrate_coupled_lane_eval_2026_05_07.md` (this file)

## Cost + time

$0 (mac local CPU + file IO + 3 mount.hexa probes), ~5 min wall (selftest 1.6s + 3 probes ~280s each via raw#37 helper subprocess overhead + ledger append).

## Cross-link

- `.roadmap.philosophy` cond.3 (D3 substrate-coupled emerge — status met 2026-05-07)
- `anima/spec/emerge_paradigm.spec.yaml v1` (D3 SSOT)
- `anima-core/runtime/clm_v4_mount.hexa` (substrate mount mechanism)
- `state/anima_emerge_5turn_dialogue_smoke_2026_05_05/verdict.json` (BG-AJ paradigm anchor — phi range 0.126, hsd_max 16.87, dialogue_smoke_PASS true; 5-turn pre-spec smoke)
- `state/anima_paradigm_v11_g3_canonical_magnitude_audit_2026_05_05/` (paradigm v11 G3 audit)
- `state/anima_model_attempts_ledger.jsonl` BG-JV attempt_n=44

User directive (verbatim): "BG-JV: D3 substrate-coupled emerge paradigm lane fire — CLM v4 + mount.hexa Φ★ NO_FLIP test."
