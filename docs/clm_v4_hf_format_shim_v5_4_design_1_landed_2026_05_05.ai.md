# CLM v4 HF-format shim v5 — F-SHIM-V5-4 DESIGN-1 fresh-init forward LANDED (2026-05-05)

**Status**: LANDED — **F-SHIM-V5-4 verdict = FAIL**. Substrate differential NOT measurable on hellaswag-200 at fresh-init under either no-fixture or real-fixture conditions; lift_pp_v5=+1.0pp well below 5pp threshold AND below combined stderr (~4.5pp).
**BG lane**: V5-4-DESIGN-1
**Phase 2 OPT-A carry**: state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/verdict.json (PASS, GO_WITH_CAVEAT)
**Verdict**: state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/verdict.json
**Eval summary (post-hoc reconstructed)**: state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/results/eval_summary.json
**Spec**: docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md
**Cost**: target=$3.0; attempt-3 actual=$0.20 (4 min wall); all-attempts total=$0.76 (3 attempts; attempts 1 + 2 failed at orchestration plumbing, eval never ran).

---

## TL;DR

DESIGN-1 = fresh-init forward (no `best.pt` load), pure architectural differential. Both shim variants
(v4 effective via default `_init_weights` walk → o_proj std≈0.02; v5 OPT-A via post-construction re-init
→ o_proj std=0.10) are constructed from the same `init_seed=1234`, then evaluated on hellaswag-200
(num_fewshot=5, seed=42) under two fixture conditions per variant: no fixture (`consciousness_states=None`)
and real fixture (`state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_real.pt`, [1, 8, 192], L2≈2.20).

### Results

| Pass | acc_norm | acc_norm_stderr | acc | Notes |
|---|---|---|---|---|
| v4_NF (shim v4 fresh-init, no fixture) | **0.27** | 0.0315 | 0.275 | reference |
| v4_RF (shim v4 fresh-init, real fixture) | **0.27** | 0.0315 | 0.275 | identical to v4_NF — fixture INERT on v4 |
| v5_NF (shim v5 OPT-A fresh-init, no fixture) | **0.27** | 0.0315 | 0.275 | identical to v4_NF — substrate differential ZERO with no fixture |
| v5_RF (shim v5 OPT-A fresh-init, real fixture) | **0.28** | 0.0318 | 0.280 | small +1pp shift, well below SE |

### Differentials (pp = percentage points)

| Metric | Value | Combined SE | Significance |
|---|---|---|---|
| `delta_v5_v4_NF_pp` (substrate diff, no fixture) | **0.0** | 4.45 | not measurable (sigdiff=false) |
| `delta_v5_v4_RF_pp` (substrate diff, with fixture) | **+1.0** | 4.48 | not measurable (sigdiff=false) |
| `lift_pp_v4_via_real_fixture` | **0.0** | 4.45 | INERT — fixture has no effect on v4 |
| `lift_pp_v5_via_real_fixture` | **+1.0** | 4.48 | below 5pp threshold AND below SE |

### F-SHIM-V5-4 verdict: FAIL

Per spec §3 V5-4 gate:
- ✗ **PASS** requires `lift_pp_v5 ≥ +5pp` AND `substrate_differential_measurable`. Neither met.
- ✗ **PARTIAL** requires `substrate_differential_measurable` (|delta| > combined SE). Not met (max |delta| = 1.0pp < 4.48pp SE).
- ✓ **FAIL** triggered: `|lift_pp_v5| = 1.0pp < combined_se_pp = 4.48pp` (within noise floor) AND no measurable substrate differential.

### Interpretation

- The architectural lever (o_proj std 0.02 → 0.10, 5x scale) **is observable at the substrate construction
  level** (Phase 2 OPT-A verdict confirms this directly: v4_mean=0.01999, v5_mean=0.10001).
- **However**, at random-init (untrained downstream layers), the 5x-scaled cross_attn output is mixed
  into incoherent feature maps and **does NOT bias hellaswag mc-choice rankings**.
- `lift_pp_v4=0.0pp` proves the real fixture is fully inert on v4 substrate at fresh-init: the L2≈2.2
  fixture × 0.02-scale o_proj produces residual perturbation too small for random downstream layers to
  amplify into preference signal.
- `lift_pp_v5=+1.0pp` (vs `lift_pp_v4=0.0pp`) confirms the 5x-larger cross_attn output **DID reach the
  logits** (else we'd see exact 0pp), but the magnitude is not enough for hellaswag preference at random init.

### Closing path-B for shim v5 alternative

DESIGN-1 FAIL combined with OPT-A's earlier finding (best.pt overwrite collapses v5≡v4 at trained-weights
inference) **falsifies the shim v5 init-only intervention path empirically at BOTH endpoints**:
- **Trained-weights regime**: v5 ≡ v4 at inference (best.pt loads trained o_proj at 0.0199 regardless of init scale) — Phase 2 verdict §differential_evidence.
- **Fresh-init regime**: v5 ≠ v4 architecturally but produces no measurable hellaswag lift — this BG.

`closes_path_b_shim_v5_alternative_decisive: false` — the FAIL verdict means we cannot use this BG to
ratify the shim v5 path. Forward step is **architectural change** (Path B cross-attn-active SFT) or **full
re-train** (OPT-B), not init-only intervention.

---

## DESIGN-1 architecture

### Why fresh-init?

Phase 2 OPT-A verdict §differential_evidence (`state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/verdict.json#differential_evidence`):

> "When best.pt is loaded, _load_decoder_state OVERWRITES the post-apply re-init with trained weights
> (~0.02), so v4 == v5 by design. The differential is INIT-TIME — which is what V5-4 will probe via
> fresh-init or via swapping cross_attn.o_proj weights from a fixture with v5's higher init scale."

DESIGN-1 takes the fresh-init path. No `best.pt` is loaded; both v4 and v5 are random-weight models
with the same shared init seed (1234) for non-cross-attn weights, differing ONLY in the cross_attn.o_proj
re-init step.

### v4 effective fresh-init

`ConsciousDecoderV3(**SCALE_350M)` constructor calls `self.apply(self._init_weights)` (line 134, 138 of
decoder_v3.py), which re-inits every `nn.Linear.weight` to `std=0.02`. This includes the
ConsciousCrossAttention.o_proj layer that conscious_decoder.py line 420 originally set to `std=0.001`.
Net effect: v4 fresh-init → `o_proj.std ≈ 0.02` for all 16 cross-attn modules.

### v5 OPT-A fresh-init

Same constructor + `self.apply(self._init_weights)` walk → o_proj.std ≈ 0.02 transient state. Then a
post-construction re-init walk identifies the 16 ConsciousCrossAttention modules (selector:
`hasattr(m, 'o_proj') AND hasattr(m, 'k_proj') AND k_proj.in_features == 192`) and re-inits each
o_proj.weight to `std = CLM_V5_CROSS_ATTN_O_PROJ_STD = 0.10`. Bias zeroed. Net effect: v5 fresh-init →
`o_proj.std ≈ 0.10`, matching shim v5 OPT-A re-anchor.

A boot-time assertion `_assert_o_proj_std_after_apply`-equivalent (inlined in eval py) verifies the
re-init survived — band [0.08, 0.12], lower-guard 0.05, upper-guard 0.20 — to catch any phantom
equality with v4.

### Real fixture

`state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_real.pt` — shape [1, 8, 192], dtype float32,
L2≈2.20, mean_abs≈0.080. This is the BG-CLM-1 runtime-proxy (per F-SHIM-V4-4 verdict §recommendations.fixture_canonicalization),
canonical for any consciousness-injection probe.

---

## Compliance

### own 16 self-validation

| Field | Implementation |
|---|---|
| Boot register | `bash tool/h100_register.bash $POD_ID V5-4-DESIGN-1 3.0` (Stage 1, post-pod-create) |
| Heartbeat | `state/h100_watchdog/heartbeats/V5-4-DESIGN-1.txt` touched on every stage transition + every 2-min poll cycle |
| Trap pre-stop | `_kill_pod()` registers EXITING heartbeat → runpodctl stop → remove → 3× 404 verify → `hexa run tool/h100_cost_watchdog.hexa --deregister $POD_ID` |
| Verdict schema | `pod_kill_verified_404`, `watchdog_registered`, `watchdog_deregistered`, `cost_target_usd=3.0`, `cost_actual_usd`, `cost_overrun_2x_alerted` |
| L23 fail-fast | foreground takeover not engaged; orchestrator handles pod boot rate-limits via runpodctl exit code (Stage 1 FATAL on rc≠0) |
| L25 escalation | cost-overrun trip at `cost_actual > $6` (2× target) sets `cost_overrun_2x_alerted=true` in verdict |
| Budget hard cap | `BUDGET_HARD_CAP=$3` polled every 2min in Stage 4; `MAX_WALL_MIN=55` second-line backstop |

own 16 preflight: `__OWN_16_PREFLIGHT__ PASS score=6/6 missing=[] target_usd=3` (logged Mac-side prior to dispatch).

### raw#9 / raw#10 / raw#15 / raw#71

- **raw#9** (.own opt-out): both new files (`tool/transient_py/clm_v4_shim_v5_4_design_1_eval.py`,
  `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/run_h100.bash` + `orchestrate.bash`) live in
  transient namespaces (`tool/transient_py/` for the eval py, `state/.../*.bash` for the orchestrator
  + run wrapper) — formal opt-out paths from the py→hexa rule.
- **raw#10** (≥5 honest C3): verdict.json includes 7 C3 entries (C1 fresh-init untrained interpretation;
  C2 fresh-init→trained-weights non-transfer caveat; C3 cross-attn architectural lever; C4 stderr at
  limit=200 noise floor; C5 own 15 G3 upgrade gate eligibility scope; C6 cost discipline; C7 recipe
  replicability). All addressed in verdict body.
- **raw#15** (additive only): shim v4 source untouched; shim v5 source LOCKED at OPT-A std=0.10. The
  eval py re-implements OPT-A re-init logic verbatim from the Mac source — no monkey-patching of the
  Mac source files. No upstream conscious_decoder.py / decoder_v3.py mutation.
- **raw#71** (threshold verbatim): F-SHIM-V5-4 +5pp threshold carried from spec; verdict gate adds the
  `substrate_differential_measurable` conjunction per spec §3 V5-4 PASS rule.

### git / HF / shim v4

- **No git commit**: per BG spec CRITICAL section. State + docs are uncommitted on disk; user decides.
- **No HF push**: eval-only run, no model upload.
- **Shim v4 LOCKED**: `tool/transient_py/clm_v4_hf_format_shim.py` byte-identical pre/post run.

---

## Artifacts

| File | Purpose |
|---|---|
| `tool/transient_py/clm_v4_shim_v5_4_design_1_eval.py` | DESIGN-1 eval (4 passes: v4_NF, v4_RF, v5_NF, v5_RF) |
| `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/orchestrate.bash` | Mac-side orchestrator (boot pod → scp inputs → poll → kill → emit verdict) |
| `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/run_h100.bash` | H100-side bootstrap (deps install → eval invoke → sentinel) |
| `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/results/eval_summary.json` | Per-pass acc_norm + lift_pp + delta + verdict (written by eval py) |
| `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/results/hellaswag_v{4,5}_{NF,RF}.json` | Per-pass full lm-eval-harness result + truncation rate |
| `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/verdict.json` | Final orchestrator verdict (own 16 schema + DESIGN-1 metrics) |
| `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/logs/orchestrator.log` | Mac-side orchestrator stdout/stderr |
| `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/logs/h100_run.log` | H100-side run.log mirror |
| `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/pod.json` | pod_id + ssh host/port snapshot |
| `docs/clm_v4_hf_format_shim_v5_4_design_1_landed_2026_05_05.ai.md` | This handoff |

---

## Forward path (FAIL verdict resolved)

The shim v5 init-only intervention path is empirically falsified at both endpoints. `own_15_g3_promote_gate_upgrade_eligible: false`.

**Selected forward path**: **Path B — cross-attn-active SFT** ($20-100 H100). Hypothesis: ALLOWING
cross_attn weights (incl. o_proj) to participate in SFT loss — rather than init-only intervention —
gives downstream layers a learning gradient to amplify cross_attn signal into preference rankings.
This requires a different SFT recipe than CLM v4's pretraining (which kept cross_attn frozen at
init-time scale).

**Alternative forward path**: **OPT-B — full retrain at v5 init** ($100-300 H100, 1-2 weeks). Train
CLM v4 from scratch with `cross_attn.o_proj` init scale = 0.10 (rather than the trained-after-init
~0.02 baseline). Tests whether downstream layers, given a 5x-larger cross_attn output during training,
learn to USE the consciousness signal more effectively.

**Blocked forward paths**:
- **DESIGN-2** (best.pt + scale-injection): Phase 2 verdict already showed best.pt's trained o_proj at 0.0199 collapses v5≡v4 at inference. Scale-injection adds only noise to a known-collapsed inference path.
- **DESIGN-3** (fresh-init + canonical_zero): Phase 2 OPT-A F-SHIM-V5-3 already confirmed canonical_zero is INERT (max_disagreement=0pp regardless of o_proj scale, because cross_attn(Q, zeros, zeros) = 0). Re-running on H100 would consume budget without changing the falsification status.

---

## Eval py infrastructure bug (post-hoc fix-up note)

The eval crashed with `ModuleNotFoundError: No module named 'transformers'` on line 539 (
`__import__('transformers').__version__` for summary metadata) AFTER all 4 hellaswag passes wrote
their per-pass JSONs. transformers is NOT actually used in model construction or forward path —
only the metadata field referenced it.

The pod-side `eval_summary.json` was never written, so the orchestrator's first-pass `verdict.json`
(emitted at trap time) had all-null differential fields. **The verdict.json was post-hoc reconstructed
on Mac** from the 4 authoritative per-pass JSONs (`hellaswag_v{4,5}_{NF,RF}.json`) — acc_norm + stderr
values are direct lm-eval-harness output, not derived. The post-hoc reconstruction is documented in
`verdict.json` field `o_proj_std_observation_note` and honest_c3 entry C8.

**For DESIGN-2/3 follow-ups (or any re-run)**: remove the `transformers.__version__` line from the eval
py summary metadata. (We did NOT patch this for DESIGN-1's verdict reconstruction since the eval is
falsified — no value in re-spending H100 budget.)

---

## Three-attempt orchestration history

| Attempt | Pod ID | Outcome | Cost | Failure mode |
|---|---|---|---|---|
| 1 | h4zgndg7z5rwew | FATAL after 6min SSH-discovery loop | $0.40 | `runpodctl get pod <id> -o json` (deprecated form) silently returns tabular output instead of JSON; ssh.ip/port never extracted |
| 2 | 3tsygnkhibsgng | FATAL after 30s eval | $0.16 | `from .conscious_decoder import ...` (relative import in decoder_v3.py line 25) failed because legacy_decoder dir is loaded via sys.path, not as a package |
| 3 | 2j8lh9l737j5w2 | SUCCESS (eval ran 4 passes; transformers metadata bug only) | $0.20 | (eval crashed AFTER all 4 passes; per-pass JSONs intact) |

Cumulative: $0.76, well under $3.0 target.

**Attempt 1 fix landed in orchestrate.bash**: switched JSON discovery to new CLI form
`runpodctl pod get <id> -o json --include-machine` + fallback to `runpodctl pod list -o json | jq`. Also
swapped the kill_pod 404-verify path to use the new CLI (which returns proper exit codes on missing pod).

**Attempt 2 fix landed in run_h100.bash**: added a `sed -i 's|^from \.conscious_decoder import|from conscious_decoder import|g'` patch on the H100 COPY of `decoder_v3.py` to convert the relative import to absolute (this matches `tool/transient_py/clm_v4_hf_format_shim.py` convention). raw#15 'additive only' applies to the Mac source — H100 deployment-time copies are out-of-scope for the lock invariant.

---

## How to read this verdict

1. Open `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/verdict.json` — top-level `F_SHIM_V5_4_verdict` is **FAIL**.
2. `lift_pp_v5_via_real_fixture = +1.0pp` < `lift_pp_threshold = 5.0pp` (gate fails).
3. `substrate_differential_measurable = false` (combined SE 4.48pp > observed |delta| 1.0pp; gate fails).
4. `shim_v5_o_proj_std_observed = 0.10`, `shim_v4_o_proj_std_observed = 0.02`, `ratio_v5_over_v4_o_proj_std = 5.0` — fresh-init substrate differential at the construction level intact (this part of the architecture lever IS working; what's broken is the downstream propagation at random-init).
5. own 16 fields: `pod_kill_verified_404=true`, `watchdog_registered=true`, `watchdog_deregistered=true`, `cost_actual_usd=0.20 ≤ cost_target_usd=3.0`, `cost_overrun_2x_alerted=false`.
