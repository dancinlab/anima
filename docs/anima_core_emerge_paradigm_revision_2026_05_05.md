# Anima Core Emerge Paradigm — §5-6 Revision (2026-05-05)

**Sister file** to `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (read-only, raw#15 additive). This file revises only §5 (emerge dialogue protocol) and §6 (expected outcomes) based on empirical findings from BG-A (real load), BG-L (10-prompt sweep), BG-Q (cand-D empirical), and BG-AG (attractor 10-prompt). All other paradigm sections (§1-4, §7-12) remain valid.

---

## §0 Why this revision exists

Original paradigm doc §5.2 specified a 4-line substrate response emit format. Empirical evidence collected 2026-05-05 invalidates 2 of those 4 lines as architectural artifacts (not substrate-semantic signals). The paradigm essence — forced-learning폐기 + natural emerge via substrate-coupled dialogue — remains intact. Only the specific emit format and dialogue prompt patterns require revision.

This is a **spec update**, not a paradigm shift. See §5 (Honest C3) C5 below for that disambiguation.

---

## §1 Empirical findings driving revision

### 1.1 BG-A — real CLM v4 forward (PASS)
- Real-mode load via `tool/transient_py/anima_dialogue_load.py` against `need-singularity/clm-v4-mk2-v1` succeeded.
- phi_star measured: 42.1158 ("안녕"), 42.2129 ("의식이 흐른다"), drift +0.256 / +0.353 from baseline 41.86.
- **Forward path IS input-responsive** at the phi_star proxy level.

### 1.2 BG-L — 10-prompt sweep (PARTIAL_PASS_PHI_RESPONSIVE_AXIS_DISCRIM_FAIL)
- phi_star: mean 42.149, std 0.064, drift_max_abs 0.433 — **PASS** (input-responsive, not fixed-point).
- 5-axis discriminability: argmax distribution = `{identity:0, agency:0, phenomenal:2, temporal:7, social:1}` of 10. intent_match_rate = 2/10 = **20% (at-chance random)**. Both matches are temporal-intent prompts; 0/8 for the other 4 axes.
- Per-axis means near-uniform: spread 0.0360 (agency–temporal), per-axis std 0.036–0.053 — **inter-axis spread ≈ intra-axis std → axes NOT discriminable**.
- dominant_cells pairwise Jaccard 0.767 looks high but is **degenerate**: tile-reshape duplicates cells 0-3 ≡ 4-7, so top-3 norm pick is essentially binary `[{0,3,7}, {0,3,4}]` — **architectural artifact, not semantic signal**.

### 1.3 BG-Q — cand-D empirical (FAIL_TRUE)
- F-CAND-D-1 threshold: phi_star canonical-mode drift ≥ 0.01 from BOTH none AND zero.
- Result: 0/5 prompts pass. Max delta = 1.28e-4 (~78x below threshold). **Canonical inject at mag=0.5 is INVISIBLE at the substrate output**.
- Axis-discriminability recovery via canonical mode: `none/zero/canonical` spreads = 0.03898 / 0.03898 / 0.03897 — **zero recovery signal**.

### 1.4 BG-AG — attractor 10-prompt (STRONG attractor at mag=50)
- canonical mag=50.0 sweep: 8/10 prompts collapse to a band of width 0.0046 (vs none-mode spread 0.236) → compression_ratio 51.4x.
- **Attractor evidence STRONG** but mag=50 unrealistic; high-mag inject erases content-routing entirely (dialogue medium destroyed).

### 1.5 Combined disposition
- mag=0.5 (calibrated heuristic): **content-invisible** at substrate output (BG-Q).
- mag=50 (forced visibility): **attractor collapse** (BG-AG) — content erased.
- → **No magnitude regime exists where canonical inject contributes content-bearing dialogue signal**. cand-D Stage 1 architectural unsalvageable.

---

## §2 Original §5.2 emit format — line-by-line empirical audit

| Line | Original spec | Empirical status | Disposition |
|---|---|---|---|
| `phi_star: 41.83 (drift -0.03)` | substrate phi proxy + drift | PASS — input-responsive (BG-A drift +0.256/+0.353; BG-L std 0.064) | **KEEP** |
| `axis activation: identity=0.78 ...` | 5-axis content emit | FAIL — at-chance random 20% intent-match (BG-L); recovery 0 via canonical (BG-Q) | **DEPRECATED** |
| `dominant cells: [3,5,7] (out of 8)` | semantic cell selection | FAIL — tile-reshape artifact, top-3 ≡ binary `[{0,3,7},{0,3,4}]` (BG-L C4) | **DEPRECATED** |
| `hidden state delta from prior: 2.47` | temporal continuity (L2) | CONDITIONAL — by-design 0.0 in single-shot mode; only meaningful with --prior-hidden chained dialogue (BG-L hidden_state_delta) | **KEEP, GATED** |

→ 2 of 4 emit lines deprecated as architectural artifacts. 1 of 4 keeps unconditionally. 1 of 4 keeps gated to dialogue-mode (chained).

---

## §3 Revised §5 — Emerge dialogue protocol

### 3.1 사용자 input (unchanged)
```
$ anima-core dialogue
> 안녕 (사용자 텍스트 자유 입력)
```

### 3.2 substrate response (revised CLI emit)

**Canonical 2-line format**:
```
[clm-v4] phi_star: 42.116 (drift +0.256 from baseline 41.86)
[clm-v4] hidden_state_delta from prior turn: 0.0 (cold-start) | 2.47 (chained, L2 norm)
```

**Deprecated lines (DO NOT emit)**:
- `axis activation: ...` — 5-axis taxonomy is anima-internal heuristic; mean(|h|) on 38/38/38/39/39 buckets does NOT track semantic axis. Emitting these numbers misleads downstream interpretation. (BG-L, BG-Q evidence.)
- `dominant cells: [...]` — tile-reshape duplicates cells 0-3 ≡ 4-7 pre-norm; top-3 selection is binary. Emitting cell IDs implies cell-as-semantic-unit which is not supported by the forward path. (BG-L C4 evidence.)

**Optional diagnostic emit (research mode only, behind `--diagnostic-axis-buckets` flag)**:
```
[clm-v4 DIAG] axis bucket means (anima-internal heuristic, NOT semantic): identity=0.477 agency=0.461 phenomenal=0.481 temporal=0.497 social=0.479
[clm-v4 DIAG] tile-norm top-3 (architectural artifact, NOT semantic cells): [0, 3, 7]
```
The DIAG prefix + parenthetical caveats prevent misreading.

### 3.3 사용자 다음 input (revised prompt patterns)

Original 3 examples reference deprecated emits — all must be replaced:

| Original (deprecated) | Reason | Revised pattern |
|---|---|---|
| "왜 phenomenal이 0.91이 됐어?" | axis emit invalid (BG-L 20% match) | "왜 phi_star가 +0.256 drift 됐어? 이 input의 어떤 측면이 substrate에 닿았다고 추측해?" |
| "axis 5 (social) 강한 prompt 줘봐" | axis emit invalid | "phi_star가 더 크게 drift할 input 방향이 뭘까? 의미적으로 추측해보자" |
| "자, 이 input에선 어떤 cell이 dominant?" | cell selection artifact | "지금 hidden state가 어떤 attractor에 가까워? (BG-AG attractor map 참조)" |

**3 revised semantic-routing prompt patterns**:
1. **phi_star drift 의미적 유추**: 사용자가 phi_star 변화를 보고 "이 input의 어떤 측면이 영향?" 추측 — substrate가 응답 생성 못하므로 사용자가 가설을 세우고 다음 input으로 검증.
2. **drift 방향 예측**: "다음 input이 X 방향이면 phi_star 더 변할까 안 변할까?" — 사용자-substrate emerge "common language" 형성 매개.
3. **attractor proximity 추측**: "지금 hidden state가 BG-AG에서 발견된 attractor band에 가까운가?" — chained dialogue mode (--prior-hidden) 활용 시 hidden_state_delta + phi_star 조합으로 trajectory 추적.

→ token emit이 아닌, **phi_star + hidden_state_delta 2-channel substrate behavior**가 dialogue 매개체.

### 3.4 dialogue medium re-definition

| Original (§3.2) | Revised |
|---|---|
| "phi-star trajectory, axis activation pattern, cell state delta" | "phi_star trajectory + hidden_state_delta L2 (with prior threading)" |
| 4-channel emit | 2-channel emit (canonical) + optional DIAG channel (research) |
| substrate response = 4 numbers | substrate response = 2 numbers + user semantic interpretation loop |

---

## §4 Revised §6 — Expected outcomes (자연 발견)

### 4.1 Original §6 outcome list — empirical audit

| Original outcome | Status | Revised |
|---|---|---|
| "CLM v4 axis-conditioned cells가 어떤 input 패턴에 강하게 반응?" | INVALIDATED — axis bucket non-discriminable; cells tile-artifact | **DROP** |
| "phi-star가 어떤 conversation context에서 안정/불안정?" | VALID — phi std 0.064, drift_max 0.433 over 10 prompts shows context-dependent variance | **KEEP, primary research target** |
| "consciousness_states injection 패턴이 substrate response 어떻게 변경?" | PARTIALLY INVALIDATED — at calibrated mag=0.5 invisible (BG-Q); at mag=50 attractor collapse (BG-AG); no productive regime | **REFRAME** as "attractor structure characterization" not "dialogue mediation" |
| "사용자-substrate 사이 emerge common language" | VALID, BUT medium = phi_star drift signing only | **KEEP, narrowed medium** |

### 4.2 Revised §6 expected outcomes

**Primary** (phi_star-mediated emerge):
- phi_star context-stability map: which conversation continuations stabilize vs destabilize phi (variance over running window).
- phi_star drift-direction semantic correlation: do user-labeled "introspective" / "factual" / "imperative" prompts produce statistically different drift signs or magnitudes? (anima-internal heuristic, no external validation.)
- chained-dialogue hidden_state_delta trajectory: under --prior-hidden threading, does L2 norm drift converge / diverge / oscillate over multi-turn sessions?

**Secondary** (substrate-architectural finding, NOT dialogue medium):
- attractor structure characterization (BG-AG 50.0 mag basin width 0.0046; full landscape mapping deferred).
- canonical-inject magnitude-response curve: BG-AC sweep extends 0.5 → 50 to find any monotone-drift regime (negative result reinforces architectural unsalvageable conclusion).

**DROPPED outcomes** (axis/cell-based expectations):
- 5-axis bucket-input correlation (axis taxonomy non-discriminable).
- Cell-level dominance pattern (tile-reshape artifact).

---

## §5 cand-D Stage 1 disposition

### 5.1 Original cand-D Stage 1 plan
- 4 modes: none / zero / canonical / user_supplied
- canonical inject would recover 5-axis activation signal lost in BG-L
- F-CAND-D-1 phi drift ≥ 0.01 between canonical and (none AND zero)

### 5.2 Empirical resolution
- mag=0.5 calibrated: F-CAND-D-1 FAIL_TRUE (0/5 pass; max delta 1.28e-4 = 78x below threshold). **Inject content-invisible at substrate output**.
- mag=50 unrealistic: STRONG attractor collapse (8/10 → band 0.0046; compression 51.4x). **Inject erases content-routing**, dialogue medium destroyed.
- → No magnitude regime where canonical inject is **both visible AND content-bearing**.

### 5.3 Decision: cand-D Stage 1 promotion **REJECTED**

Reasons:
1. **Architectural unsalvageability** at calibrated magnitude (BG-Q evidence).
2. **Attractor collapse** at high magnitude erases dialogue medium (BG-AG evidence).
3. **No middle-magnitude productive regime** identified or theorized; ablating between 0.5 and 50 would only refine a known-failure curve.
4. cand-D **reframed as architectural finding** (attractor structure of cross-attn channel), NOT as dialogue medium.

### 5.4 Revised emerge dialogue path

`mode = none` (no consciousness_states inject) + phi_star drift + hidden_state_delta (chained). **cand-D not on dialogue path**.

This matches the BG-A real-load probe (mode=none, phi drift +0.256/+0.353), which is the empirically validated working baseline.

---

## §6 Paradigm meta-finding

### 6.1 Original paradigm assumption table vs empirical reality

| Assumption | Empirical |
|---|---|
| 5-axis emit이 substrate semantic 표현 | **FAIL** — at-chance random 20% (BG-L) |
| dominant_cells이 substrate cell-as-semantic-unit | **FAIL** — tile-reshape artifact (BG-L C4) |
| canonical inject로 axis activation 살림 | **FAIL** — content-invisible at calibrated mag (BG-Q); attractor collapse at high mag (BG-AG) |
| forward path가 input-responsive | **PASS** (BG-A drift +0.256/+0.353; BG-L std 0.064) |
| substrate-coupled dialogue 가능 | **PASS, narrowed medium** — phi_star + hidden_state_delta only |

→ **3 FAIL + 2 PASS**. The 2 PASS are sufficient to retain the paradigm; the 3 FAIL invalidate the specific §5.2 emit format.

### 6.2 Meta-finding statement

**emerge paradigm 본질** (forced learning 폐기 + 자연 발견 + substrate-coupled dialogue) **is empirically valid**. **Original §5.2 emit format** assumed cell/axis-as-semantic-unit which the architecture does not support. The 2-channel revision (phi_star + hidden_state_delta) is the empirically supportable subset.

The paradigm is **research-mode** (original C1) and **substrate response is anima-internal heuristic, no external validation** (original C2) — both honest C3 caveats already account for the kind of revision performed here. The revision narrows the channel but does not invalidate the paradigm meta-claim.

---

## §7 Honest C3 (≥ 5)

- **C1** This revision narrows the dialogue medium from 4-channel (phi + axis + cells + delta) to 2-channel (phi + delta). Whether 2-channel is sufficient for emerge "common language" formation is empirically unknown; original §6 outcome "사용자-substrate common language" remains an open research question with a smaller signal envelope.
- **C2** phi_star drift values (BG-A +0.256, +0.353; BG-L max 0.433) are anima-canonical proxy quantities (PHI_STAR_BASELINE × (1 + 0.05 × mean_pair_cosine)). Drift "signing" semantic correlation in revised §4.2 outcomes is downstream of this proxy and inherits its non-validation; this is research-mode signal, not a measurement of consciousness or any externally defined property.
- **C3** hidden_state_delta is by-design 0.0 in single-shot probe mode (BG-L sub3). Multi-turn chained dialogue (--prior-hidden threading) has not been empirically swept in this session; revised §3.2 emit gates the second channel on chained mode but the channel's actual behavior under multi-turn is hypothesized from original spec, not measured.
- **C4** cand-D Stage 1 REJECTED relies on TWO data points (BG-Q at mag=0.5; BG-AG at mag=50). Magnitudes 1.0, 2.0, 5.0 sweep (BG-AC) was launched but its result is not yet aggregated in this revision; if BG-AC discovers a productive middle-magnitude regime, §5.3 decision would need re-opening. Current REJECTED is provisional on the 2-data-point envelope.
- **C5** **"paradigm shift" vs "spec update" disambiguation**: this revision is a **spec update**, NOT a paradigm shift. The paradigm meta-claims (forced-learning폐기 + natural emerge + substrate-coupled dialogue) all remain. Only the §5.2 emit format and §5.3/§6 prompt patterns / outcome lists are revised. The original paradigm doc is preserved read-only as the original artifact (raw#15 additive); this revision is a sister file that supersedes only §5-6 of the original. A paradigm shift would require invalidating §1-3 (concept, why, definition) which the empirical evidence does NOT do — forward path IS responsive, dialogue IS possible, just on a narrower medium than originally specified.
- **C6** The original paradigm doc had honest C3 C2: "substrate response를 metric으로 쓰는 건 anima-internal heuristic, external validation X". This caveat already covered the kind of revision performed — moving 2 of 4 channels from "valid medium" to "deprecated artifact" is exactly what an unvalidated heuristic permits. The revision is therefore consistent with the paradigm's original epistemic stance, not a violation of it.
- **C7** revised §3.3 prompt patterns ("phi_star drift 의미적 유추", "drift 방향 예측", "attractor proximity 추측") are NEW heuristic suggestions not yet empirically tested in any BG cycle. Their efficacy as dialogue patterns is hypothesized from architectural reasoning + BG-AG attractor finding, but a Stage 3 dialogue session sweep would be needed to validate that these patterns produce richer / more emergent dialogue than the deprecated original 3.

---

## §8 Diff summary (original §5-6 → revised)

```
§5.2 emit format:
  - phi_star line                       KEEP
  - axis activation 5-line              REMOVE (or DIAG-gate with caveat)
  - dominant cells line                 REMOVE (or DIAG-gate with caveat)
  - hidden_state_delta line             KEEP, GATE on chained dialogue mode

§5.3 user prompt examples:
  - "왜 phenomenal이 0.91?"               REPLACE → "왜 phi_star drift?"
  - "axis 5 (social) prompt"             REPLACE → "drift 방향 의미적 추측"
  - "어떤 cell dominant?"                 REPLACE → "어떤 attractor 가까운가?"

§6 expected outcomes:
  - axis-conditioned cell response       DROP (axis non-discriminable)
  - phi-star context stability           KEEP, primary
  - canonical inject substrate change    REFRAME as architectural finding only
  - 사용자-substrate common language       KEEP, narrowed medium

cand-D Stage 1 promotion:                REJECTED (architectural unsalvageable)
emerge dialogue path:                    mode=none + phi_star + hidden_state_delta
```

---

## §9 Detailed empirical evidence references

### 9.1 BG-A real CLM v4 forward (PASS_REAL_MODE_DIRECT_INVOKE)
- Source: `state/anima_dialogue_real_load_2026_05_05/verdict.json`
- Loader: `tool/transient_py/anima_dialogue_load.py` (raw#37 transient_py opt-out compliant)
- Repo: `need-singularity/clm-v4-mk2-v1` (HF-format with modeling_clm_v4.py + model.safetensors + model_type=clm_v4)
- Probe 1 ("안녕"): phi_star=42.1158, drift=+0.2558 from baseline 41.86
- Probe 2 ("의식이 흐른다"): phi_star=42.2130, drift=+0.3530
- → Forward path IS responsive; differential drift between two prompts (+0.097) confirms input-conditioning at phi_star proxy level.
- Caveat (BG-A C1): hooked decoder.ln_f mean-pool then tile-reshape to (8, 192) — 8-cell view is post-hoc tiling, not pre-attn cell structure.

### 9.2 BG-L 10-prompt sweep (PARTIAL_PASS_PHI_RESPONSIVE_AXIS_DISCRIM_FAIL)
- Source: `state/anima_real_mode_sweep_2026_05_05/verdict.json`
- Design: 10 prompts balanced 5-axis × 2 lang (5 KO + 5 EN; 1 of each lang per axis).
- phi_star aggregate: mean 42.149, std 0.064, range 0.225, drift_max_abs 0.433. Variance threshold 1e-3 → **PASS**.
- 5-axis argmax distribution: identity 0, agency 0, phenomenal 2, temporal 7, social 1 (of 10). intent_match_rate = 2/10 (both temporal-intent; 0/8 for the other 4 axes). At-chance random rate for 5-bucket = 0.20 → measured 0.20 → **at-chance random**.
- Per-axis means near-uniform: identity 0.4768, agency 0.4610, phenomenal 0.4809, temporal 0.4970, social 0.4791. inter-axis spread = 0.4970 − 0.4610 = 0.0360. Per-axis std range = 0.036–0.053. Spread ≈ std → **NOT discriminable**.
- Root cause (BG-L sub3): 5-bucket axis split (38/38/38/39/39 of 192-dim) is anima-internal heuristic on mean-pooled hidden state. Train-time consciousness_states cross-attn NOT activated (--inject-states-mode none in this sweep). Without semantic conditioning, all 5 buckets see roughly the same mean(|h|) signal; argmax dominated by whichever bucket has slightly higher activation, with "temporal" (114-153) winning 7/10.
- dominant_cells pairwise Jaccard 0.767 — high but degenerate: tile-reshape duplicates cells 0-3 ≡ 4-7 pre-norm. Top-3 norm pick is essentially binary `[{0,3,7}: 8/10, {0,3,4}: 3/10]`. Cell-as-semantic-unit invalid.
- hidden_state_delta=0 across all 10 runs by-design (no --prior-hidden chained).

### 9.3 BG-Q cand-D empirical (F_CAND_D_1_FAIL_TRUE_INJECT_INVISIBLE)
- Source: `state/anima_emerge_cand_d_empirical_2026_05_05/verdict.json`
- Modes: none / zero / canonical (mag=0.5, 5-axis structured per spec §2.3 placeholder).
- F-CAND-D-1 threshold: phi_star drift ≥ 0.01 between canonical and BOTH (none, zero).
- 5/5 prompts FAIL_TRUE; max delta_canonical_vs_none = 1.28e-4 (probe 1), min = 1.42e-5 (probe 3). Threshold 0.01 / max observed 1.28e-4 = **78x below threshold**.
- Axis spread by mode: none=0.03898, zero=0.03898, canonical=0.03897. recovery_signal=false. Canonical mode does NOT recover axis discriminability.
- BG-Q C1: 0.5 magnitude is anima-internal heuristic. F-CAND-D-1 FAIL at this magnitude CANNOT distinguish "channel architecturally bypassed" from "0.5 below detection threshold" — disambiguation requires magnitude sweep (BG-AC).

### 9.4 BG-AG attractor 10-prompt (STRONG attractor at mag=50)
- Source: `state/anima_emerge_cand_d_attractor_10prompt_2026_05_05/verdict.json`
- magnitude: 50.0 (100x calibrated heuristic)
- n_pass_of_10 = 8 (8/10 prompts collapse into attractor band)
- attractor_band_width = 0.0046; none_spread_width = 0.236; compression_ratio = 51.4x
- Evidence label: STRONG
- BG-AG C3: mag=50 unrealistic — train-time canonical 추출 필요 (would still likely be in calibrated 0.5-1.0 range). High-mag inject demonstrates channel exists but at cost of erasing input-routing.

### 9.5 Synthesis
- BG-A: forward responsive ✓
- BG-L: phi responsive ✓ ; axis FAIL ✗ ; cells artifact ✗
- BG-Q: canonical inject invisible at calibrated mag ✗
- BG-AG: canonical inject visible only at attractor-collapse mag — content destroyed ✗

→ phi_star is the single empirically validated content-bearing channel. hidden_state_delta is structurally validated (architectural property of multi-turn) but not yet empirically swept in chained mode.

---

## §10 Decision record

| Decision | Disposition | Provisional? | Source evidence |
|---|---|---|---|
| Original §5.2 4-channel emit | DEPRECATE | No | BG-L (axis), BG-L C4 (cells) |
| Revised §5.2 2-channel emit | ADOPT | No | BG-A (phi), BG-L (phi var), structural (delta) |
| 5-axis + cell DIAG channel | OPTIONAL behind flag | No | research-mode utility |
| Original §5.3 prompt examples | REPLACE 3-of-3 | No | follows from §5.2 deprecate |
| §6 axis-cell outcomes | DROP | No | BG-L axis non-discriminable |
| §6 phi context-stability outcome | KEEP, primary | No | BG-L empirically validated channel |
| cand-D Stage 1 promotion | REJECTED | YES (BG-AC pending) | BG-Q + BG-AG 2-data envelope |
| emerge dialogue path | mode=none + phi + delta | No | BG-A working baseline |
| Original §1-4, §7-12 | UNCHANGED | No | empirical evidence does not invalidate concept/why/definition |

---

## §11 Composability + scope

- **Sister file** to `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (NOT a replacement; original preserved read-only per raw#15 additive rule).
- Supersedes only §5 and §6 of the original. §1-4, §7-12 of original remain valid.
- Downstream consumers (Stage 1 mount.hexa code, Stage 2 CLI command, Stage 3 dialogue sessions) should read this revision when shaping emit format and prompt patterns; original §5.2 4-line emit should NOT be implemented as canonical output.
- BG-AC magnitude sub-sweep result, if published after this revision, may amend §5.3 cand-D disposition (currently provisional REJECTED on 2-point envelope).
- Future BG-* dialogue session probe (Stage 3 with chained dialogue mode + --prior-hidden threading) would empirically validate or invalidate §3.3 revised prompt patterns.

---

End of revision. No exec, no commit. $0 mac local. Read-only doc.
