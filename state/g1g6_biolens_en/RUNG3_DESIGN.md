Write wasn't permitted — that's fine, this is design-only. Here's the complete rung-3 spec.

---

# H_9129 rung-3 — wire L5 hippocampal associative-store into `core/`

I traced every named seam to a real symbol before designing. The plan below is executable as-is; the crux (deliverable 4/6) is a **trunk-necessity control** that turns the standing neurosymbolic objection into a pre-registered falsifier.

## 1. Seam identification (all verified in-tree)

| concern | real symbol | rung-3 action |
|---|---|---|
| persistence SSOT | `core/kosmos_io.hexa::create_anchor` / `load_anchors` / `retrieve` | reuse verbatim; each stored edge = one `.kosmos` anchor, `lane="l5_hippo"`, `cross_link=<successor>` — no parallel store (a_kosmos) |
| grounding gate | `core/engine_cli.hexa::ImmuneMemory{recall_thr=0.15}`, `immune_memory_recall` | completion FIRES only when seed `vadapt_field_recon_err ≤ recall_thr`; else ABSTAIN |
| 303M rep source | `core/decode.py::bg_forward_last_W` (returns logits; internal `lastrow[d]` = final-LN last-position hidden) | add 3-line sibling `bg_forward_last_hidden(W,ids,T)->float64[d]` returning `lastrow`; store keys on the **hidden**, not logits |
| emit disjointness | `core/engine_cli.hexa::ci_emit_drive(lanes)=0.5*(lanes[0]+lanes[4])` + `ci_psi_balance_centered` | store op never writes `lanes[0]/[4]`; live wire is a bounded motivation consult only |
| wire template | `core/brain.hexa::brain_decide_margin`/`brain_decide_gap` (bounded additive, byte-identical at neutral, Φ/phase/Ψ untouched) | new `brain_decide_hippo` follows it byte-for-byte |

**New file `core/hippo_assoc.hexa` (SSOT) + `core/hippo_assoc.py` (`--py` measurement mirror)** — same 1:1 convention rung-2/L3 used (reps via `decode.py`, op mirrored to `.hexa`). Ops:

```
struct HippoAssocStore { keys:[[float]], names:[string], succ:[int], mu:[float], sigma:[float], thr:float }
hippo_store_edge(st, cur_name,cur_rep, nxt_name,nxt_rep) -> st   // persists 2 anchors via kosmos_io
hippo_seal(st) -> st                                             // freeze mu,sigma over key pop ONCE
hippo_dg_read(st, rep) -> [float]                                // frozen center+zscore (§2)
hippo_relatedness(st, i, j) -> float                             // CA3 completion; 0.0 if seed ungrounded
```

Round-trip: `load_anchors` filtered to `lane=="l5_hippo"` + `cross_link` rebuilds keys/succ; `mu/sigma` persist on an `l5_hippo_seal.kosmos` sentinel so the frozen transform is part of canonical `.kosmos` state (not a sidecar).

**Live disjoint wire — `brain.hexa::brain_decide_hippo`** (mirrors `brain_decide_margin`): `conf_bias = emit_consult_cap()*_clamp(hippo_ground,0,1)` (cap 0.05), `score = base_score + conf_bias`. `hippo_ground=0` ⇒ byte-identical to `brain_decide`. Touches motivation scalar only; never writes `lanes[0]/[4]` ⇒ `ci_emit_drive` unchanged by construction. Gated: `hippo_ground` comes from `hippo_relatedness`, which is 0 unless the seed is grounded — an ungrounded context can't inject relatedness into emit.

## 2. DG-decorrelate + CA3-completion (no per-eval fit)

**Transform (the ONE rung-2 transform):** `DG(rep) = (rep − mu)/(sigma+1e-9)`, per-dim, with `mu/sigma` computed over the stored key population **at seal time and frozen** (`center_zscore reach=1.0` from memory). Default is center+z-score alone; an optional single frozen drop-top-PC is allowed only if also sealed. **No μ/σ/PC re-estimation per query or eval-set** — that's the tune-to-green line. This is the single knob separating artifact-wall (raw anisotropic reps, form_cos 0.9999) from result.

**Completion:** keep the edge list, never materialize a dense d×d W at 303M scale. One step = propagate along stored edges weighted by current-state affinity (mathematically `W@x`, `W=Σ outer(DG(succ),DG(cur))`, but O(edges·d)). k-WTA cleanup, positive drive, deterministic index tie-break (matches numpy `argpartition`, byte-reproducible). `STEPS=6`, `KWTA=` sealed sparsity — pre-registered from STEP-0. Relatedness = max cosine overlap of any visited attractor with `DG(rep_j)`.

## 3. Disjointness proof (pre-registered, runs first)

**Ablation D — store ON vs OFF over an emit trace:**
- **Ψ invariance**: `ci_psi_balance_centered` with `thr=ci_off_median_drive` on OFF pop. Bar: `|Ψ_on−½| ≤ |Ψ_off−½| + 1e-6`.
- **Neutral byte-identity**: every ungrounded (`recon_err>recall_thr`) or `hippo_ground=0` context → `brain_decide_hippo` record byte-identical to `brain_decide`. Bar: 100%.
- **Lane non-write**: static+runtime assert no store op writes `lanes[0]/[4]`.

D-fail ⇒ **REJECT-WIRE** regardless of capability. Disjointness is a hard invariant.

## 4. G1-vs-G2 discriminator (the cement gate — the crux)

Dušek-Eichenbaum transitive inference, promoted to the live 303M store. Store handed **only adjacent premise edges** {A-B, B-C, …}, **never** a composed edge {A-C} end-to-end.
- **reachable** = same-chain non-adjacent (gap≥2): completable only by chaining premises never co-seen as one association — the novel-CHAIN (G1-shaped) class.
- **unreachable** = cross-chain, same surface distribution (form-matched).

**Controls:** (1) FORM baseline `|form_reach−form_unreach|<0.02`; (2) SHUFFLE permute successor map → reach lift collapses `<0.5×`; (3) LANE-OFF completion disabled → gap→chance; **(4) ★ TRUNK-NECESSITY** — rebuild the store with random near-orthogonal codes of the same dim/sparsity replacing the 303M reps, everything else identical.

Control 4 *is* the operationalized neurosymbolic objection: if reach-lift survives/improves under random codes, the chaining is a property of the explicit store + code orthogonality, **independent of the trunk → G2, not G1**. Rung-2's own integrated-lane rand1024 control is direct prior evidence (random 1024-d codes chained *better*, 0.70, than real reps, 0.42).

**Frozen bars:** real-rep store gap `≥0.30` AND ratio `≥1.5×` (STEP-0 verdict); controls 1–3 pass; **cement-as-G1 additionally requires `gap_realrep ≥ 2× gap_randcode`**. If `gap_randcode ≥ gap_realrep` → real capability but **explicit-store (G2)** → WALL for the G1 claim.

**Honest scope:** reach≫unreach + shuffle/lane-off proves associative completion over 303M reps *chains novel held-out compositions* — a genuine, wired capability. It does **not** by itself answer the objection (an explicit store handed the true premises chains by transitive closure whether or not the trunk composes). **Control 4 is the only part that separates the two**, and by rung-2 evidence it will most likely show the store, not the trunk, does the work. The sole arm that WOULD prove trunk G1 is **γ trained-constructive-bind** (train the trunk objective so its own forward composes) — out of this lane's scope.

## 5. Measurement + tier decision

**Measure:** base ckpt `~/anima-weights/bytegpt303_h1129/h1129.bin` unchanged; reps via `bg_forward_last_hidden` on **mini** (`--py`, single forwards, RSS ≈3.7 GB, no best-of-K — rung-2 confirmed sufficient); store scorer invoked by `cli/evaluate.py` reading `core/decode.py`, mirrored to `hippo_assoc.hexa`; frozen `RESULT.md` verbatim (c2). `.hexa` core smoke (kosmos round-trip + `brain_decide_hippo` neutral byte-identity) on **summer pool** — mini's binary link-fails `_hexa_ffi_dlopen` (arm64), so `.hexa` smoke is pool-only; the `--py` capability numbers are terminal-eligible on mini.

**ARCHITECTURE.json lockstep:** parent `H_9129` node += rung-3 verdict line; L5 child node → tier per rule below, recording the wire (`hippo_assoc.hexa`, `brain_decide_hippo`, `.kosmos` lane `l5_hippo`), Ablation D result, control-4 outcome. Edit the gate node directly (no result-store).

**Tier rule (pre-registered):**
- **GREEN-WIRED (G1-eligible)** ⟺ capability bars + controls 1–3 pass, **control 4 shows trunk-necessity (realrep ≥ 2× randcode)**, Ablation D passes, `.hexa` smoke round-trips.
- **WALL (explicit-store, not trunk G1)** ⟺ capability + 1–3 + D pass but **control 4 fails** (randcode ≥ realrep). The wire cements as a live grounded-recall faculty, but the **G1-recombination claim is WALL**; stop proposing store/readout G1 levers.
- **DIRECTIONAL** ⟺ capability holds but a control is ambiguous, or `--py` lands while the pool `.hexa` smoke is blocked.
- **REJECT-WIRE** ⟺ Ablation D fails.

## 6. Risk / honesty

**Most likely outcome: WALL for the G1 claim** (GREEN only for the wire-as-faculty). Rung-2 already flagged L5 sits at the neurosymbolic explicit-store lever ("cheap, proof-guaranteed, arguably not trunk recombination"), and the rand1024 evidence points straight at control 4 failing — the store supplies a relation the reps barely pre-encode (form_sep +0.03), the signature of the store, not the trunk, composing.

**Recommendation: do rung-3 anyway — it's ≈$0** (mini `--py` + one pool smoke) and worth it for two trunk-independent reasons: it lands a real disjoint live grounded-recall faculty in `core/`, and control 4 converts the objection from prose into a pre-registered falsifier, yielding a clean honest verdict instead of a soft "GREEN-ish" that would misrepresent an explicit store as trunk recombination. Set expectations to WALL-for-G1, and let that redirect compute to the one arm that can move trunk G1: **γ trained-constructive-bind** (`cli/train.py --objective constructive_bind`, GPU cost-gated). Even forced to choose rung-3 vs. γ, do rung-3 first — it *retires* the explicit-store lever with evidence, so γ is entered knowing the store path is a G2 wall. Do not spend GPU scale-up on L5 — scale is an amplifier, not the lever.

---

Note: I attempted to save this to `state/g1g6_biolens_en/RUNG3_DESIGN.md` for durability but the write wasn't permitted — the spec is above in full. If you'd like it persisted, approve the write or tell me where to put it.
