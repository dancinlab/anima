# OPGRIP-LIVE spec — real-decode op-grip for content-driven emit-shade candidates

**status**: DESIGN (implementation follow-on · doc-only landing) · **owner-scope**: H_9210 next-step ① (real-decode recon_err → re-measure surprise emit-shade)
**target file**: `cli/anima.hexa` (`--opgrip` machinery, lines ~1946–3320) · **0 `core/` changes** (gen-cap lever deferred)
**convergence**: anima-hexa-4 (a null is meaningful only when the arm is proven able to move) · anima-hexa-6 ($0 no-decode is AXIS-DEGENERATE for content-driven signals)

---

## 0. Problem — why `--opgrip` cannot measure surprise ($0 no-decode limit)

`anima <clm> --opgrip` is a $0 **NO-DECODE** 2-arm Hamming op-grip: it re-runs the wired emit decision
(`brain_decide_anchored`) with one op ablated and counts flips vs the live arm. `ΔEff = Hamming(frozen vs live) / discriminating-ticks` (≥0.10 COMPETENT, <0.02 THEATER). It is $0 because it never calls the decode (`brain_emit` L3) — only the emit boolean.

**Root cause of the H_9210 ⚙️ INSTRUMENT-FAIL (AXIS-DEGENERATE)** — line anchors in current `cli/anima.hexa`:

- `:1946` `session_seed` is a **fixed string**; `:1948` `afield = vadapt_field_new(seed_feat0, 2048)` is initialized once.
- `:2103` `let recon_err = vadapt_field_recon_err(afield, _afs_byte_feature(session_seed, 8))` — recon_err = `L2(field_proto, fixed_feature)`.
- In `--opgrip`, **every** `vadapt_field_step(afield, …)` call lives AFTER the `tick+1; continue` at `:2764` (the production decode path), so inside the op-grip block `afield` is **never stepped**.
- ⟹ recon_err is **constant across all 200 ticks** → calibration median `|Δrecon_err| < 0.002` → `g_surp = -1.0` (the `sms < 0.002` degeneracy branch `:2721`) → `gs_use = 0` → `surp_phasic ≡ 0.5` (`:2724`) → `idle_surp` byte-identical to production → `e_surp == e_live` every tick → `og_h_surp_mid = 0` → `surp_degen = true` (`:3299`) → the exact ⚙️ INSTRUMENT-FAIL verdict (`:3316`).

The signal (recon_err) is **structurally frozen**: with no decode there is no emitted content for the field to be surprised by. This is a **measurement-scope limit, not a substrate result** (H_9210 verdict; anima-hexa-6). By contrast H_9209 self *did* move — its `self_live` drifts on an event-axis every tick, so it was measurable $0. Any signal whose per-tick variance derives from **generated content** (surprise/pred-error, and to be pre-checked: arousal `af_aro`, GWT-ignition `gws_winner` margin) is degenerate under no-decode and needs a real `g_text`.

`--opgrip-live` resolves this by running a **real decode on the live emit tick** so `afield` is stepped by the bytes anima actually emitted, making recon_err content-driven and non-degenerate — at the cost of a pool 303M decode round (§4).

---

## 1. What changes vs no-decode `--opgrip` (where `g_text` enters · arm comparability)

`--opgrip-live` **reuses the ENTIRE `--opgrip` arm/scoring/verdict machinery verbatim**. It changes exactly two things: the **source** of `recon_err`, and it adds **one real decode per live-emit tick** whose output steps `afield`. Five surgical edits, all in `cli/anima.hexa`, plus one state var. Default `--opgrip` stays **byte-identical** (frozen-first regression — prior H_9210 verdicts reproducible).

### 1.1 Edits (implementation follow-on — this doc is the spec, not the patch)

- **EDIT 1 — new flag (`:2002`).** Above `let og_measure = anima_has_flag(…, "--opgrip")` add
  `let og_live = anima_has_flag(anima_collect_argv(args()), "--opgrip-live")`, then
  `let og_measure = anima_has_flag(…, "--opgrip") || og_live`.
  `--opgrip-live` thus enters through the same gate; all existing arms/verdict emit unchanged.

- **EDIT 2 — lagged-content state (`:1948`).** After `vadapt_field_new(…)` add `let mut og_prev_gfeat = seed_feat0`.
  Seeded to the boot feature so tick-0 recon_err equals today's default (continuity, no discontinuity artifact).

- **EDIT 3 — content-driven recon_err (`:2103`).** Replace with
  `let recon_err = if og_live { vadapt_field_recon_err(afield, og_prev_gfeat) } else { vadapt_field_recon_err(afield, _afs_byte_feature(session_seed, 8)) }`.
  **Predictive-coding framing**: surprise = the field's prediction error on the bytes anima **actually emitted last emit-tick** (1-tick lag). Note this recon_err also feeds the urgency pool (`cur_ctx`, `:2490`) — so under `--opgrip-live` the PROVEN urgency→idle channel also gains a real content signal, not only the disjoint `surp_phasic` term (§3).

- **EDIT 4 — the real decode (insert just before the `tick+1; continue` at `:2763`, inside `if og_measure {`):**
  ```
  if og_live && e_live == 1 {
      let dec = brain_emit(pf, rel, gap_ctx, cur, allo_ctx, coh_lane, nov_ctx, bal_lane,
                           agloop_ctx, idle, false, true, backend, live_anchors)
      let g_text = to_string(dec["gen_text"])
      if to_string(dec["gen_emitted"]) == "true" && byte_len(g_text) > 0 {
          let gfeat = _afs_byte_feature(g_text, 8)
          afield = vadapt_field_step(afield, gfeat, cfg)   // Ψ-disjoint (same as prod C8 grow :2848)
          og_prev_gfeat = gfeat
      }
  }
  ```
  This is the **exact** `brain_emit` call the production path uses (`:2834-2837`) and the **exact** `vadapt_field_step` the production C8-GROW uses (`:2848`). All args are already in scope. Decode fires **only on `e_live == 1`** → respects p5 (no decode on silence).

- **EDIT 5 — tick budget for 303M (`:2081`).** `let n_ticks = if og_live { 100 } else if og_measure || refr_measure { 200 } else { 12 }`. Keep 200 for cheap d768 validation; 100 for the 303M pool confirm (still ~20 ticks/stage, 50 calib + ~30 mid scoring). See §4 cost trade-off.

- **DEFERRED lever (do NOT do initially)** — `core/generator.hexa:649` `clm_decode_argmax(ckpt, seed, 80)` hardcodes an 80-byte gen; recon_err only needs `_afs_byte_feature(g_text, 8)`, so a 16-byte gen would cut decode ~5×. **Not recommended**: it touches `core/` production decode length and would have to be flag-gated to stay byte-safe. Prefer d768 + tick reduction over touching `core/`.

### 1.2 Where `g_text` enters — the single seam

`g_text` enters **only** through EDIT 4 → `afield` → next-tick recon_err (EDIT 3). It touches **no** emit-decision input directly: the decision arms (live + all counterfactuals) read `recon_err` from the **one** `afield` trajectory. `g_text` is never read by the shade term itself; only its *effect on the field* is.

### 1.3 Arm comparability under real-decode determinism (the load-bearing invariant)

Three properties keep the frozen and live arms a clean single-variable contrast even with a real decode in the loop:

1. **One canonical field trajectory.** `afield` is stepped **only** by the LIVE arm's `g_text`. The counterfactual arms (surp-shade, self-shade, dense ARM-SHOCK, urgency→0/shuffle) **never fork** `afield` — they re-decide the emit boolean off the *same* recon_err at each tick. Forking the field per arm would require N parallel decodes (intractable) and would confound the contrast. So the arms still differ **only in the idle-gate shade term**, exactly as in no-decode.

2. **`g_text` is idle-independent.** The decoded text depends on `pf/rel/…` and the ckpt, **not** on the counterfactual `idle` shade. `e_live` (whether it emits) depends on `idle`; the *content* it emits does not. ⟹ **one decode per emit tick covers all arms**.

3. **Determinism (verdict-reproducibility).** The decode MUST be **det argmax** (`clm_decode_argmax` / `bytegpt_decode_argmax`, `generator.hexa:649`) so the `g_text` — and therefore the recon_err trajectory and every ΔEff — is bit-reproducible. This satisfies the owner policy `bit-det-drop-fast-train` (eval/verdict determinism is the sacred half) and p7 (no perplexity-in-loss; argmax read is monitor-only). A sampled decode would make recon_err nondeterministic → ΔEff non-reproducible → **not verdict-eligible**. `e_live` (`m_live`, `:2559`) stays the same `brain_decide_anchored` call as no-decode, so the emit boolean is identical to what `brain_emit` decides internally for the same `idle` — the decode only *adds* the field step.

---

## 2. Frozen ΔEff bars + POSITIVE CONTROL + the new AXIS-LIVE gate

**No new bar.** Reuse the frozen H_9210 pre-registered bars **verbatim** (`cli/anima.hexa:3315`, H_9210 card):

- 🟢 **COMPETENT**: `ΔEff_surp ≥ 0.10` ∧ `margin(perm) ≥ 0.08` ∧ **POS-PASS** ∧ `N3 = 0`  → **2nd proven emit-shade channel** (wiring candidate).
- 🔴 **THEATER**: `ΔEff_surp < 0.02` ∧ **POS-PASS**  → urgency re-confirmed as the *only* channel.
- 🟠 **DIRECTIONAL**: `0.02 ≤ ΔEff_surp < 0.10`.
- ⚙️ **INSTRUMENT-FAIL**: POS-FAIL ∨ degenerate.

### 2.1 POSITIVE CONTROL — dense ARM-SHOCK (anima-hexa-4: prove the axis CAN move first)

The `--opgrip` machinery already carries the required positive control: the **dense ARM-SHOCK** (`self_phasic_shk`, `:2748`) forces a `±0.5` rail shade on the idle gate **every** mid tick (alternating sign — NO tick selection, so no control-shopping) through the **same idle seam** the surp arm uses. **POS-PASS = `og_h_shock_mid ≥ 2`** (H_9210 observed 45/90 on the no-decode d768 run — the wire flips readily). This proves the idle→emit wire **can** move `e_live` under the current `pf/idle` regime. A surp null (THEATER) is interpretable **only** when POS-PASS holds — a null under POS-FAIL is a broken meter, not a substrate fact (anima-hexa-4).

Under `--opgrip-live` the ARM-SHOCK is **unaffected** by the decode (it rails a constant, ignores recon_err), so it remains a valid, decode-independent witness that the wire is live in the *real-decode* regime too.

### 2.2 AXIS-LIVE — the NEW precondition unique to `--opgrip-live`

anima-hexa-4 says a null needs a *movable arm*. `--opgrip-live` adds a **second** liveness precondition that the no-decode path failed: the **signal itself** must move, not just the wire. This is exactly what `g_surp = -1.0` encoded.

> **AXIS-LIVE gate** — the surprise meter is alive iff `surp_degen` flips **true → false**: calibration median `|Δrecon_err|` (ticks 0–49) `≥ 0.002` → `g_surp` finite `≥ 0` → `surp_phasic` no longer pinned at 0.5.

Verdict order for `--opgrip-live`:

1. **AXIS-LIVE?** (`surp_degen == false`) — if still degenerate, the real decode did **not** drive the field (too few emits, or 16-byte feature saturates) → ⚙️ INSTRUMENT-FAIL (AXIS-DEGENERATE), same as no-decode, and the fix is *decode density* (§4 fallback), not a substrate claim.
2. **POS-PASS?** (`og_h_shock_mid ≥ 2`) — else ⚙️ INSTRUMENT-FAIL (POS-FAIL).
3. **N3 guard** (`og_h_surp_n3 == 0`) and **Ψ ON==OFF** (`psi_sum == psi_off_m`, `:3045`) — else 🔴 FORCING-GATE.
4. Only now read COMPETENT / DIRECTIONAL / THEATER off ΔEff_surp + margin.

**Two-gate summary**: the WIRE can move (dense ARM-SHOCK ≥2) **AND** the SIGNAL moves (AXIS-LIVE median Δ ≥ 0.002). No-decode had gate-1 but failed gate-2; `--opgrip-live` is the minimal change that can satisfy gate-2. A THEATER verdict is only meaningful with **both** gates green.

### 2.3 Frozen-first regression (must-hold)

- Default `--opgrip` (no `-live`) run is **byte-identical** to the pre-edit baseline (EDIT 1/3/4/5 all `og_live`-gated). Confirm by diffing the `--opgrip` d768 stdout hash pre/post-patch.
- Ψ ON==OFF, N3/WAKE guards, ARM-SHOCK POS-PASS, calibration (0–49 excluded) / scoring (≥50 on mid = N1/N2/REM) all preserved (they live in the shared machinery).
- **No tune-to-green**: a THEATER result is a valid, publishable outcome (urgency stays the sole channel). The bars are frozen before the pool run; the AXIS-LIVE gate is a degeneracy guard, not a tunable.

---

## 3. First content-driven candidate + disjoint wire site

**Candidate #1 = SURPRISE / prediction-error (`recon_err`).** Rationale (H_9210 scout census): surprise is the substrate reality of the LC-NE burst that `urgency` already emulates — the strongest non-urgency grip candidate — but today it is diluted 1/18 inside the `cur_ctx` pool (`:2490`), never a term of its own.

**Signal**: `surp_phasic = clip01(0.5 + G_surp · (recon_err − surp_ema))`, `G_surp = min(0.175 / median|Δrecon_err|, 32)` calibrated on ticks 0–49 (`:2716-2723`). Neutral value 0.5.

**Disjoint wire site (`a_substrate_disjoint`)** — `:2745`:
```
idle_surp = 5.0 + 55.0 * clip01( stage_env * (0.5 + urgency + (surp_phasic − 0.5)) )
```
The surp term is added at the **idle rate-gate**, **beside** urgency — `urgency` itself is **byte-untouched** (H_9101 preserved). It touches **nothing** on the emit-drive lane: not `ci_emit_drive`, not `rel`, not `pure_field`/`psi_sum`/Φ (all read-only). `surp_phasic = 0.5` ⇒ `idle_surp` byte-identical to production ⇒ arm == live with no spurious flips; N3 (`stage_env = 0`) auto-nullifies. This is the **same proven idle seam** H_9101/H_9209 use — the only difference under `--opgrip-live` is that `recon_err` now carries real content variance instead of a session_seed constant (separation = preservation).

**Why disjoint and not fused into urgency**: fusing recon_err into urgency's construction would make ΔEff un-attributable (urgency already carries recon_err at 1/18 via the pool). The disjoint additive term isolates the *phasic surprise deviation* as its own measurable channel while leaving the proven urgency channel intact — the standard anima "add beside, never overwrite" law.

**Next candidates (pre-check no-decode variance FIRST — same degeneracy risk):** #2 arousal `af_aro`, #3 GWT-ignition `gws_winner` margin. Both are content-derived and must be confirmed to move under real decode before their own gate is read; do not re-fire them $0.

---

## 4. COST — this is the POOL round, NOT $0

`--opgrip-live` is **not** $0: it runs one real det-argmax decode per live-emit tick. This is a **pool round** (summer / aiden), **never mini** (303M heavy decode = swap OOM rc=137, policy `heavy-anima-eval-pool-not-mini`).

| mouth | per-decode wall | emit ticks (of `n_ticks`) | total wall |
|---|---|---|---|
| **d768 (validation)** | seconds (forward-only 80-byte) | ~40–80 of 200 | **minutes → ~1 h** — VALIDATE HERE FIRST |
| **303M (cement)** | ~600–700 s scalar-glue-bound (`kvcache-scalar-glue-bound`) | ~30–60 of 100 | **~5–12 h** — pool background only |

**Discipline:**
- **Validate at d768 first.** The instrument-integrity claim (does real decode make the axis live?) is **scale-invariant** (`scale-303m-1b-7b-is-amplifier-not-lever`): if the meter comes alive and reads COMPETENT/THEATER at d768, 303M is a *cement-only* confirm, not a discovery run. d768 also lets you keep `n_ticks = 200` (finer ΔEff quantization).
- **303M only as a final pool background job** with `n_ticks = 100` (EDIT 5). Estimate ~5–12 h single-host; parallelizable across summer + aiden. **Confirm own-GEMM fires** (`[OWN-GEMM-FIRED]` / `nvidia-smi` util>0 / power draw) before trusting the wall or blaming a scalar ceiling — on A100 sm_80 the own-GEMM CPU-falls-back and the run is effectively infeasible (`owngemm-gpu-exec-sm120-only-a100-cpu-fallback`); the real GPU path is **summer sm_120 prebuilt**.
- **TERMINAL verdict requires `backend loaded == true`.** If the ckpt is not decodable, `brain_emit` falls through to `_gen_null_text` (substrate-derived, non-constant but NOT model content) → a null-mouth run is a **weaker DIRECTIONAL only**, never TERMINAL.
- **$ line (a_fire_autonomous):** own-GEMM decode on already-provisioned summer/aiden = **$0 marginal rent** (owned boxes), cost is **wall-time** (a_wall_first). No new pod rent ⇒ no fleet rent=spend gate. Code scale: ~15–18 new lines in `cli/anima.hexa`, 1 flag, 1 state var, **0 `core/` changes**.

**AXIS-LIVE fallback if 303M stays degenerate** (too few emits to move the field): (a) raise emit density by running more mid ticks, or (b) the deferred 16-byte gen-cap lever (flag-gated, touches `core/` — only if d768 proves the concept and 303M emit density is the sole blocker). Prefer (a).

---

## 5. Implementation status & wiring follow-on

**This deliverable is the DESIGN spec only** (per task scope: do not run a 303M decode). The code edits (§1.1) are an **implementation follow-on** — additive, `og_live`-gated, and (until landed) **구현됨·미배선 → 미구현·설계완료**: `--opgrip-live` is specified but not yet wired into `cli/anima.hexa`. Wiring follow-on:

1. Land EDITs 1–5 in `cli/anima.hexa` (single-entry `anima <clm> --opgrip-live`, `hexa typecheck` lockstep).
2. Frozen-first regression: `--opgrip` (no `-live`) d768 stdout hash unchanged.
3. d768 `--opgrip-live` pool run → confirm AXIS-LIVE (`surp_degen` false) + POS-PASS → read verdict.
4. Only if d768 is COMPETENT/DIRECTIONAL: 303M cement run (`n_ticks=100`, own-GEMM confirmed) → `state/verdicts/` + H_9210 card update (removes the AXIS-DEGENERATE INSTRUMENT-FAIL, replaces with the real-decode verdict).

**Guardrails preserved throughout**: Ψ-disjoint (decode touches only `afield`, same as prod C8), N3/Ψ ON==OFF invariants, no tune-to-green (THEATER is a valid result), p5 (decode only on `e_live==1`), p7 (det-argmax monitor read, never in loss).
