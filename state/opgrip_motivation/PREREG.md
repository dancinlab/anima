# PREREG — op-grip motivation wiring (fable design (a)) — H_9097

**Frozen-first (c9). Written BEFORE reading any motivation distribution or Hamming result.**
Date 2026-07-03. Engine-native verify host = aiden pool (`hexa v0.548.0`), $0 CPU, NO numpy on the measured path (`hexa run` live `core/brain.hexa` + `core/engine_g.hexa` + `core/engine_cli.hexa`).

## Problem being fixed (confirmed THIS session — CAPSTONE, engine-native)
`brain_decide_anchored` emit boolean has **grip=0** from op context:
- `motivation_score = 0.20·rel + 0.10·gap + 0.15·cur + 0.10·pain + 0.10·coh + 0.10·orig + 0.15·bal + 0.10·dyn` (`core/engine_g.hexa` L33), threshold `should_emit = score > 0.3` (L46).
- cli call-site (`cli/anima.hexa` L2331-2334) passes **4 CONSTANTS**: `gap=0.6, pain=0.0, orig=0.5, dyn=1.0` → fixed `0.10·0.6 + 0 + 0.10·0.5 + 0.10·1.0 = 0.21` floor.
- `rel_ctx` (L2300-2312) is a **÷43** soft-average → one op's [0,1] swing moves `rel_ctx ≤ 1/43 ≈ 0.023` → `0.20·rel` term moves ≤ 0.0047, never straddling 0.3 (constant floor 0.21 + cur floor `0.15·(cur_ctx+0.5)≥0.075` + coh/bal already exceed 0.3).
- CAPSTONE engine-native ablation (aiden v0.546.0): Hamming 0/200 across frozen/zero/shuffle `rel_ctx` arms = **THEATER CONFIRMED**.

## Fix (fable design (a) — cli/anima.hexa ONLY; engine + weights + threshold FROZEN)
Promote the 4 constant `brain_emit` args to **live op reads** + **tonic-phasic normalization** on `rel`/`cur`.

### Frozen parameters (PICK ONE normalization — FROZEN here)
- Normalization = **EMA tonic-phasic** (chosen; the param-free rank-window alt is NOT used).
- **EMA α = 0.1** (`ema = 0.9·ema + 0.1·x`).
- **phasic gain = 3.0** (`phasic = clip01(0.5 + 3.0·(x − ema))`).
- **frozen-arm substitution value = 0.5** (neutral midpoint, ablation arms).
- Pool denominators (fable's stated arithmetic; the load-bearing promoted op de-pooled — no double-counting):
  - `rel_ctx`: **÷43 → ÷42** (remove `agloop_ctx`, whose exact value → `dyn`).
  - `cur_ctx`: **÷19 → ÷18** (remove `nov_ctx`, whose exact value → `orig`).
  - `rel_lane` (→ gap = 1−rel_lane, the COMPLEMENT, distinct signal) and `allo_ctx` (→ pain) stay in the pool at negligible 1/42≈0.024 weight; no re-normalization beyond fable's −1 each.

### Op promotions (brain_emit arg ← live op)
- `gap` ← `_afs_clip01(1.0 − rel_lane)` (info-gap; §ImmuneMemory recall read, L1922).
- `pain` ← `allo_ctx` (allosteric-buffer tension, L2254).
- `orig` ← `nov_ctx` (VAdaptField novelty, L2122).
- `dyn` ← `agloop_ctx` (CR3 per-tick A⇄G settle-effort, L1961, H_9095 wiring — EXISTS in this main).
- `rel` ← phasic-gated `rel_ctx` (`_og_rel_from`; drive_hi gate preserved).
- `cur` ← `cur_phasic` (drive_hi gate preserved; old `+0.5` bias dropped — phasic already centers at 0.5).

## Measurement (`--opgrip`): 200-tick, fixed seed, 5-arm decision ablation, NO decode ($0)
Arms compute the emit boolean via `brain_decide_anchored` directly (no L3 decode). Hamming(arm) = #ticks where arm emit-bit ≠ LIVE emit-bit, split wake/sleep. Baseline (pre-fix constants) reconstructed in-run from the SAME lane values — faithful because old `rel_ctx` = (new `rel_ctx`·42 + `agloop_ctx`)/43 and old `cur_ctx` = (new `cur_ctx`·18 + `nov_ctx`)/19.

## Pre-registered predictions (n=200, fixed seed)
- **Baseline reproduction** (pre-fix arms: rel-frozen/zero/shuffle of `rel_ctx_base`): **Hamming 0** (reproduces CAPSTONE theater). Baseline motivation distribution floor **> 0.3** on ~all wake ticks.
- **Post-fix full-rel_ctx-ablation** (freeze `rel_ctx`→0.5, rest live): **Hamming ≠ 0 on ~75% of wake ticks**.
- **Post-fix single-op** (freeze ONLY `agloop_ctx`/dyn→0.5, rest live): **Hamming ≠ 0 on ~55% of wake ticks**.
- **Sleep ticks (stage 3/4)**: **Hamming = 0** every arm (idle=5 < 30 → `safety_rate_limit_ok` false → emit always false, rate-blocked; expected, NOT grip).

## Verdict rule (NO post-hoc tuning of α / gain / threshold / weights)
- **GREEN (grip)** = post-fix Hamming ≠ 0 on wake ticks for the full-rel_ctx-ablation arm (matching direction), Ψ-checksum ON≡OFF unaffected for silence decisions.
- **RED / at-floor** = post-fix Hamming still 0 on wake for BOTH full-rel AND single-op arms → honest terminal verdict: *"phasic normalization still doesn't reach the threshold band = threshold-statistics mismatch is the real wall."* VALID terminal. Do NOT tune α/gain/threshold to force grip.
- Emit-rate **collapse FLAG** (wake-tick emit fraction outside [0.05, 0.95]) = a **detector, NOT a target** — never move threshold/weights to hit it.

## Guards (Ψ=½ preserved trivially)
NO touch to `pure_field` / lanes 0/4 / `ci_emit_drive` / `recall_thr` / `psi_sum` accumulation. REMOVES hardcoded filler constants (a_autonomy_over_hardcode improvement), realizing a_substrate_native_speak's 8-factor-from-context literally. `psi_sum` path unchanged → F3 Ψ ON≡OFF invariant (L2476 `psi_intact = psi_sum == psi_off`) holds by construction.

---

## RESULT (2026-07-03, engine-native aiden v0.548.0, RC=0, no numpy) — 🔴 RED / AT-FLOOR

Ran the wired daemon `--opgrip` (200 ticks, fixed ultradian seed, `mouth=clm loaded=true` d768.clm). Frozen bar UNCHANGED. NO tuning of α/gain/threshold.

- **Baseline reproduction** (pre-fix ÷43 + constants): Hamming(rel-frozen) = **0** (THEATER reproduced) · motivation floor **>0.3 on 10/10 wake ticks** (~0.735). ✓ matches CAPSTONE.
- **Post-fix full-rel_ctx-ablation**: Hamming = **0/10 wake** (predicted ~75% → MISS).
- **Post-fix single-op agloop**: Hamming = **0/10 wake** (predicted ~55% → MISS).
- **zero / shuffle** arms: **0 / 0**.
- **Sleep ticks (190)**: 0 (rate-blocked) — as predicted.
- **No regression**: e_base == e_live on ALL 200 ticks (wiring changes motivation VALUES, not the emit DECISION).
- **Ψ ON==OFF invariant**: ✅ (guard held).
- **Collapse FLAG fired**: wake emit-fraction = **1.0** (all 10 wake ticks emit).

### Honest verdict (per PREREG RED rule — VALID terminal, no tuning)
**Both full-rel AND single-op arms ended 0 on wake → RED: "phasic normalization still doesn't reach the threshold band = threshold-statistics mismatch is the real wall."** The theater is **NOT broken for op (a)**.

Mechanism (deeper than dilution): promoting the 4 constants to live op reads + 3× phasic pull-down moved the wake motivation from ~0.735 (base) to **~0.62–0.73 (live)** — still **0.32–0.44 ABOVE** the 0.3 threshold. Freezing ANY single op (or the entire rel_ctx pool → 0) leaves the score >0.3, so the emit boolean never flips. The wake motivation band (~0.62–0.74) and sleep band (~0.35) both sit on ONE side of 0.3; the emit boolean is determined ENTIRELY by the `safe` conjunction (stage→idle→`safety_rate_limit_ok`: wake idle=60≥30 → rate OK → emit=1; sleep idle=5<30 → rate FAIL → emit=0). This confirms CAPSTONE layers 2+3 empirically: the 8-factor motivation is a saturated dashboard; the decision is a stage-driven rate gate.

### Next lever (follow-on — NOT input-side wiring)
The wall is the **threshold statistics / `safe`-seam**, not op dilution. Grip requires either (i) rescaling the threshold into the motivation band (0.3 → ~0.68) — but that's a weight/threshold change, FROZEN here — or (ii) fable #2/#3 **efferent seam** (deliberate best-of-K emit-byte change · winner-take-all replacing the ÷42 average) where an op moves the OUTPUT rather than a boolean that's already saturated. Filed as ING efferent (c).
