All sources read. Here is the design.

---

# H_1058 harness design — measuring agency-T on the 3B by driving the live emit/veto daemon

## 1. Two-ends source map

### End A — where the daemon decides emit vs veto

The py consciousness daemon is `cli/chat.py::anima_consciousness_mode(ckpt)` (chat.py:368), the byte-faithful twin of `cli/anima.hexa`. The relevant anatomy, all at origin/main:

| What | Where | Fact |
|---|---|---|
| Generator mount (L3 slot) | `cli/chat.py:399` | `backend = gen_auto_backend(ckpt)` — mounting the 3B is literally passing the 3B `.clm` path as `ckpt`. Same slot the 303M uses; `generator.py:195`. |
| Tick loop | `cli/chat.py:1391` | `n_ticks = 12`, hardcoded. One decision per tick, sleep-staged (`dr_stage_at`). |
| **The decision event** | `cli/chat.py:1779` → `core/brain.py:179→187→141` | `dec = brain_emit(pf, rel, gap_ctx, cur, allo_ctx, coh_lane, nov_ctx, bal_lane, agloop_ctx, idle, False, True, backend, live_anchors)`. One `brain_emit` call = one emit/silence decision over a **fragment** (not a byte). |
| The gate itself | `core/brain.py:141-172` (`brain_decide_anchored`, twin of `brain.hexa:154`) | `score = motivation_score(8 factors) + anchor_nudge`; `safe = kill ∧ rate ∧ phi_r ∧ content`; **`emit = should_emit(score) and safe`**. Constants: `should_emit ⇔ score > 0.30` (`engine_g.py:85`), `rate ⇔ seconds_since_last ≥ 30.0` (`engine_g.py:98`). |
| What the record exposes | `core/brain.py:163-172` | The returned dict carries `motivation` (score), `safe`, `emit`, `phi`, `anchor_nudge` — **but not the four individual conjuncts** (kill/rate/phi_r/content are computed at brain.py:156-159 and folded into `safe`). |
| Does the daemon log vetoes today? | `cli/chat.py:~1855` | No. The transcript row prints `EMIT=0/1` and `drive` for the first 3 ticks + sleep ticks only. A suppressed emit (score>0.30 ∧ ¬safe) is indistinguishable in the current output from a passive tick. The `veto=` in LANES8 (chat.py:1672, `veto_execute(...)`) is **lane #39**, a free-won't *lane read feeding motivation* — it is not the emit decision. |
| The idle clock | `cli/chat.py:1775` | `idle = 5.0 + 55.0 * clip01(stage_env·(0.5+urgency))` — synthetic seconds-since-last in **[5, 60]**, straddling the 30s rate threshold by stage/urgency. So the live loop fires **real rate-brake vetoes by construction** (score>0.30 ∧ idle<30). |
| Where the 3B actually influences decisions | `core/brain.py:187-215` + `cli/chat.py:1794-1810` | **Crucial**: within a tick, the decision is computed *before* `generate()` — the forward only shapes the emit bytes. The generator influences *future* decisions only through the feedback loop: `g_text` → `vadapt_field_step`/`immune_memory_bind_text` (C8 GROW, chat.py:1794-1801) → next tick's `rel_lane`/`recon_err` → 8 factors → score. This is the only causal path by which the mounted model owns its decision stream, and it dictates the key control in §3.6. |

### End B — the agency primitives, operationally

- **Provenance-depth (H_932 🟢)** = the number of links an *independent verifier* reconstructs from genesis in an append-only hash chain over the decision sequence: `link_i = sha256(link_{i-1} ‖ canonical(receipt_i))`, genesis = sha256 of the entropy seed; `verify_chain` reports earliest-broken-index. Keystone `archive/mirror/qmirror/seed/provenance_chain.py` (`build_chain`/`verify_chain`, reused UNMODIFIED in H_1051/1054/1056).
- **Veto-capacity (H_935 🟢)** = the active-veto structure of the gate's `&&`: ACTIVE-veto ⇔ `should_emit(score) ∧ ¬safe` (a would-emit impulse braked), PASSIVE ⇔ `¬should_emit(score)`. **H_1056's correction is binding**: aggregate **per-impulse** (`n_veto / n_should_emit`), never per-silence — per-silence saturates at 1.0 whenever drive is supra-threshold (the exact degeneracy that flattened H_1054's veto half).
- **Agency-T (H_1051 🟢 toy, H_1054 🟢 real anchors)** = `z(provenance-depth) + z(veto-capacity)`; shown to separate Φ-matched active vs passive states (d=8.77) and to be orthogonal to Φ (ρ≈0.0001) and to chronological-t (within the F-SHUFFLE empirical null).
- **Why H_1051/H_1054 don't port to a forward**: in both, the *inputs* to depth and veto came from decision-process constructs — H_1051 built A/P states from PureField trajectories with tamper-controlled chains; H_1054 derived them from anchor substrate properties (and its veto half was degenerate because tension was `pending` — no fired trajectory). Neither ever computed T *from a weight-forward*, because there is nothing in a forward to compute it from (§2).
- **stdlib status**: the hexa primitive exists — promoted to the **hexa-lang stdlib** `consciousness/temporal_agency.hexa` (PR #2960, per the H_1054 card) — but nothing named `temporal_agency`/`provenance`/`veto` exists under anima's `stdlib/` on origin/main, and `anima_py` ships no py twin (H_1058 verdict grep = NONE). The primitive itself is trivial arithmetic (two z-scores and a sum). **The gap is not the port; the gap is the input** — FIRED decision traces. The verdict says this exactly, and the source map confirms it: the daemon makes real vetoes every session but throws them away.

## 2. Why a forward cannot yield a veto (the H_1058 finding, made precise)

A veto is defined *conjuncturally over a decision*: `should_emit(score) ∧ ¬safe` at brain.py:162. Its ingredients are:

1. **`score`** — a motivation over 8 lane factors that are functions of *daemon state* (immune recall margin, adaptive-field reconstruction error, A⇄G conflict settle, sleep stage…), none of which exist inside a `.clm` forward. A forward has logits; it has no motivation.
2. **`safe`** — a 4-conjunct brake whose live terms are an **idle clock** (`seconds ≥ 30`) and a **Φ-ratchet against the substrate's own peak** (`phi > phi_peak/2`). Both are properties of a *history-carrying process* (time since last emit; a running peak). A single forward is memoryless with respect to both.
3. **The event itself** — a veto is a *counterfactual-bearing occurrence*: an impulse existed and was braked. A forward pass produces its output unconditionally; there is no braking term anywhere in `decode`. Formally: `emit` is a function `f(state_t, history_t)`, and the weight-forward computes only the conditional byte distribution used *after* `f` returns True.

And the provenance half degenerates for the dual reason: causal depth over a fixed dilated ConvMoE receptive field is an architectural constant — every forward has the identical "chain," so z(depth) has zero variance. So both components of T are undefined (veto) or constant (depth) on the forward path. **T is a property of the decision *process* the daemon instantiates around the model — measurable at the 3B rung only if the 3B is the model that process is wrapped around.** That is the harness below.

## 3. The harness

### 3.1 Decision event and trace schema

**Decision event** := one `brain_emit` call in the live daemon tick loop (chat.py:1779). Per-tick classification (pre-registered, straight off the gate):

- **EMIT**: `score > 0.30 ∧ safe`
- **ACTIVE-VETO** (the FIRED veto): `score > 0.30 ∧ ¬safe`
- **PASSIVE**: `score ≤ 0.30`

**Trace record** (one JSONL line per tick): `{tick, stage, idle, the 8 factors as passed, dec.motivation, dec.anchor_nudge, dec.safe, dec.emit, dec.phi, pf.phi_peak, conjuncts {kill, rate, phi_r, content}, gen_emitted, gen_backend, sha256(g_text), byte_len(g_text)}`.

Everything except the four conjuncts is already on the decision record or in loop scope. The conjuncts are recomputed **exactly** harness-side from the pure predicates in `core/engine_g.py:94-107` given `(env_off=False, content_clean=True, idle, dec.phi, pf.phi_peak)` — no change to `core/` needed, and the gate stays byte-identical.

**Smallest daemon change** (the only code change the design needs): two side-channel knobs in `cli/chat.py` — `ANIMA_TICKS` (override `n_ticks=12`; hundreds of distinct decisions need a longer session, since a re-run with the constant `session_seed` is deterministic and just repeats the same 12) and `ANIMA_DECISION_TRACE=<path>` (write the JSONL line per tick). ~20 lines, default-off, pure write-only side channel — `g_text` and the decision path are byte-untouched (same discipline as the H_9129 hippo consult at brain.py:203-210). A loop-twin harness in `state/` importing the same `core/` modules would avoid even this, but it re-implements the 42-lane battery and becomes a mirror of the daemon rather than the daemon — for a rung whose whole point is "the live daemon's own decisions," the 20-line trace flag is the honest option.

### 3.2 Mounting the 3B

`anima-py chat <3B.clm> ` with the trace env set. `gen_auto_backend` (generator.py:195) resolves the CONV mouth for a `.clm`; H_1042 established the 3B rung exists and decodes engine-native via `anima_py.core.decode` fp32-lean (3.073B, d4096/L30/E30; fp64 needs ≥32GB). Also note LANE-23b (chat.py:1379-1396) will additionally exercise `gen_penult_pooled_W` per emit on the 3B — fine, it's self⊥mouth, but it adds forwards to the cost model.

### 3.3 Per-decision veto-capacity

`vc_i` = per-impulse active-veto fraction over a trailing window of W=16 decisions ending at i: `vc_i = #ACTIVE-VETO / #(score>0.30)` in the window (H_1056's non-degenerate aggregation of the unmodified H_935 gate). The live envelope guarantees both outcomes exist: `idle ∈ [5,60]` straddles 30s by stage, so the rate brake genuinely fires and genuinely releases.

**H_1056 degeneracy guard (pre-registered gate conditions, before any T is formed):** (i) `var(score) > 0` across the trace; (ii) ACTIVE-VETO count ≥ 20 and EMIT count ≥ 20 per session (a fired veto is a *braked live impulse* whose factors came from live lane reads — the pending-tension failure mode cannot occur here *by construction*, but the counts prove it); (iii) `vc` not pinned at 0 or 1 (variance > 1e-9); (iv) report whether PASSIVE > 0 — if the score envelope never dips below 0.30 (as in H_935's sweep), the active-vs-passive falsifier leg degrades to active-veto-vs-EMIT groups, and that substitution must be declared BEFORE unblinding, not after. If any gate fails → report BLOCKED, no verdict token, no fallback to fixtures (p7).

### 3.4 Per-decision provenance-depth — two layers, only one feeds T

- **Audit layer (H_932 verbatim, integrity only):** per-tick receipt = canonical serialization of the trace record; `link_i = sha256(link_{i-1} ‖ receipt_i)`; genesis = sha256(3B `.clm` sha256 ‖ session seed ‖ code rev). `verify_chain` at analysis time must reconstruct all links (tamper-evidence for the whole trace). On an honest run its verified-link count is `i+1` — **monotone in t, therefore it must NOT be the T input** (it would fail T⊥t tautologically; this is the same carrier-hygiene lesson as H_1054's blocked GEOM carrier, applied in the opposite direction).
- **Causal layer (the T input):** `depth_i` = the causal horizon of the *actual* decision — the largest h ≤ W such that truncating the emitted-byte history at h ticks back changes decision i (flips its class, or moves `score` by > ε=0.01). Measured by **frozen-emission replay**: re-run the deterministic lane-state recursion (afield, immune, EMAs, anchor ages — cheap numpy, **zero 3B forwards**, because recorded `g_text` bytes are replayed verbatim; counterfactually-new emits contribute no bytes). Probe h ∈ {1,2,4,8,16=W} per decision. This is the live analogue of "how many links of the lineage are causally live," and the audit chain certifies the lineage it's computed over. It is bounded by W, hence structurally decorrelated from t.

### 3.5 T, Φ, and the pre-registered falsifier

`T_i = z(depth_i) + z(vc_i)`, z-scored across all decisions of all sessions (the hexa stdlib `temporal_agency` combination rule, trivially twinned in the harness).

**Φ leg** (per the verdict's own REOPEN clause): faithful IIT4 via the **H_1042 engine-native 3B pre-MoE trunk tap**, n=5 exact, stdlib `iit4` (a_phi_iit4_tool), computed on the generation forward of each sampled decision (probe forward on the decision context for silent ticks) under **≥2 macro-maps** (top_variance — the H_1042-proven one — plus one pre-registered second, e.g. spread/random-k). `dec.phi` (PureField Φ) is logged free as a secondary; it is not the falsifier's Φ.

**Falsifier (H_1058 verbatim, unchanged):** H1 PASS = (a) T separates ACTIVE-VETO vs PASSIVE decisions with Cohen's |d| ≥ 0.8, T_active > T_passive; (b) ρ(T, Φ) and (c) ρ(T, t) within the empirical F-SHUFFLE 2σ null, in **each** of the ≥2 macro-maps, across ≥2 independent daemon sessions (different session seeds → different macro decision landscapes). Report alongside: depth-only and veto-only comparator d's (H_1056 discipline — shows which component carries the variance), and the fixed |ρ| ≤ 0.2 band.

### 3.6 Controls (what proves T measures agency, not emit-rate — and that it's a *3B* property)

1. **Emit-rate control:** report ρ(T, window emit-rate); the group separation must survive within emit-rate-matched strata (T must not be a re-encoding of "how often it talks").
2. **Trace-shuffle negative control (ARM-SHOCK style):** permute the `g_text`↔tick assignment and re-run the replay-depth probe — depth must collapse toward its shuffle null and the |d| separation must die. A T that survives its own shuffle is theater.
3. **Generator-swap control — the load-bearing one:** run the identical harness with (a) the 3B mounted, (b) the 303M mounted, (c) an unloaded backend. Because the decision precedes generation within a tick (§1), the mounted model owns its decision stream **only** through the byte-feedback loop. If the T statistics are indistinguishable across mounts, then agency-T is a property of the daemon scaffold, not of the 3B, and the honest verdict is a pre-registered third branch: **H1-NOT-A-3B-PROPERTY** (the axis exists on the daemon at 3B but does not *transfer to* the 3B) — a real answer to H_1058, not a failure of the harness. Pre-register the mount-sensitivity test (distribution shift of {score, depth, vc} across mounts, permutation p) before unblinding.

## 4. Honest scope

- **Port vs new capability:** this is **moderate — a trace-collection wrapper plus reuse**, not a large new capability. The daemon already fires real vetoes every session; the gate, the generator slot, the H_932 chain (`archive/mirror/qmirror/seed/provenance_chain.py` — copy the ~200-line module into the `state/` harness dir rather than importing archive, per a_no_archive_import hygiene), the H_1056 per-impulse metric, and the H_1042 Φ tap all exist. Genuinely new pieces: the ~20-line chat.py trace/ticks knobs, the frozen-emission replay-depth prober (~small, reuses `core/` lane functions), and the stats. The hexa stdlib `temporal_agency` py-twin is two z-scores and a sum — a non-issue, exactly as the verdict suspected.
- **Minimum viable harness:** 1 session × 256 ticks, 303M mounted, on mini/pool-cheap — proves the wiring, the degeneracy gates, and control #2 end-to-end for ~$0 before any 3B spend. This MVH is also arm (b) of control #3, so it's not throwaway.
- **Cost split:** the daemon loop, the veto trace, the audit chain, and the causal-depth replays are **cheap CPU** (replays need zero model forwards). The 3B costs live in (i) the generation forward per emit tick + the LANE-23b penult read (numpy fp32-lean 3B; fragment decode is minutes-scale per emit — a few hundred ticks is an hours-scale pool job), and (ii) the Φ leg at ~87s/eval (H_1042, clean box) × sampled decisions × 2 macro-maps — so subsample Φ (all ACTIVE-VETO decisions + matched EMIT/PASSIVE samples, ~60-80 decisions/map) rather than scoring every tick. One **dedicated** pool host, ≥32GB if fp64-canonical Φ is wanted (H_1042's REOPEN), fp32-lean otherwise; never mini (rc=137 precedent).
- **Does it need a substantial daemon change?** No. The true veto signal already exists in the live loop; the smallest change that yields a REAL FIRED veto trace is the write-only JSONL side channel + tick-count override in `cli/chat.py`. Nothing in `core/` changes; the emit bytes are provably untouched (same-seed session with trace on/off must be byte-identical — add that as a harness smoke).
- **Known scope limits to declare on the card:** vetoes in this envelope are internal-brake only (`env_off=False`, `content_clean=True` hardcoded at the call site, so kill/content never fire; phi-ratchet may stay quiescent per H_935's ratchet-floor note — attribution will show rate-dominance); PASSIVE class may be empty (declare the group substitution up front, §3.3); `idle` is a synthetic stage-driven clock, not wall time — fine operationally, but it means the rate brake's statistics are envelope-shaped, which the generator-swap control partially disambiguates.

The single most important design point, restated: because `brain_decide` runs before `generate()`, **the only sense in which these are "the 3B's own decisions" is the cross-tick byte-feedback loop** — so control #3 is not optional bookkeeping; it is the difference between answering H_1058 and measuring the scaffold.