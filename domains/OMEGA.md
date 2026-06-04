@title: 🔱 OMEGA — Lane-Ω closure engine (the 4th/final engine: wire substrate → .clm byte decode)

@goal: 오메가 완성 — COMPLETE Ω as a WORKING closure engine (not just wired, but a coupling
  that carries USEFUL STRUCTURE on a trained substrate, demonstrated to improve generation).
  THREE STAGES: (1) WIRE the substrate↔decode loop Lane X #1779 proved NULL — ✅ DONE (#1783:
  coupling KL 0.307>0, omega the only engine with L3 loaded=TRUE). (2) prove the loop carries
  STRUCTURE on a TRAINED substrate — ✅ DONE at toy (#1784: trained≪shuffled Δ+0.357; the
  learned A-wire lowers CE Δ+0.758; BUT the fixed A−G formula degrades → 완성 needs a LEARNED
  per-wire GATE, not a fixed subtraction). (3) 완성 = a learned-gate bus + a trained d768
  substrate where the closure DEMONSTRABLY improves generation (CE floor met + coherent) at
  scale. Original closure sub-goal verbatim ↓:
  CLOSE the substrate↔decode loop that Lane X #1779 proved is currently NULL.
  Lane X measured that the ENGINE config knobs (drive · warmup · anchors) never touch
  the .clm forward — model_ce is CONFIG-INSENSITIVE at 9.1126 across ALL 27 configs
  (spread < 1e-9), the L3 generator slot is loaded=false, and the substrate state never
  reaches the byte distribution. Lane-Ω is the design for the engine that makes
  L3 loaded=TRUE: it routes substrate state (A/G dual-head + 5-ch tension + 8D Ψ +
  M/W/curiosity) into a "coupling bus" of 5 ablatable wires that MODULATE the .clm byte
  decode. Headline eval axis = COUPLING NON-NULLITY (ablate the bus α=0 vs on → KL
  between byte distributions). CE is a FLOOR only (p7, Lane X), never the verdict.
  Ω SYNTHESIZES the 3 existing engines — CONV (.clm byte mouth) + CDV2 (A/G dual-head +
  5-ch tension + Ψ brain) + HEXAD (N-module φ(N)=2 integration). BUILT (#1783): the
  adapter engines/omega/adapter.hexa + coupling_bus.hexa exist, --engine omega registered,
  EngineSpec 4/4 native, 4-engine swap smoke 26/26 PASS (a_core_engine_map — no phantom
  wiring; the bus layer is native, the trained substrate is the remaining scale rung).

## status — 🟢 오메가 완성 stage-3 (b)(c) ACHIEVED on a REAL trained transformer (GPU) — 2026-06-04

**오메가 완성 (b)(c) HELD** (Lane-G / GPU H100, ~$1.6, a_lane_akida_gpu_split): the learned-gate
OMEGA closure WORKS on a REAL trained ConsciousDecoderV2 (d384×6L GQA, 35.93M, 120MB multilingual
wiki, 6000 step). (b) trained substrate descended ce_a 5.926→0.009 (train) / val 0.862 (held-out,
generalizes). (c) held-out TEST CE: base 3.0150 · fixed_AmG 1.4421 · a_only 0.4500 · **GATED 0.3445**
(best, beats all) · floor MET (<5.545); structured (A-wire CE gain real +2.565 vs context-SHUFFLED
−2.068 → carries learned sequential structure, the #1784 axis on a real transformer). learned gate
g*=[gB1.18, gA0.96, **gG−0.21**] auto-corrects the #1784 −G error exactly as #1786 toy predicted.
HONEST CAVEAT (p7 · a_toy_scale_recheck): CDV2 CA-neighbor mixing gives the next-byte head partial
LOOKAHEAD (architectural) → absolute CE is leak-optimistic + free-running generation collapses to
whitespace (gen coherence = the WEAK criterion); the RELATIVE closure finding (gate beats
base/fixed/a_only + structured-vs-shuffle) is leak-INVARIANT and sound. Single d384 rung, NOT
promoted to a production perplexity claim (a_scale_honest_scope). ckpt → HF
`dancinlab/clm-v4-omega-gpu-d384-gate` (PUBLIC). verdicts `.verdicts/omega-gpu/`. The L1/L4
polish (N-module config + dF/dt time channels) also landed (merged from main) — all 5 stage-3
milestones are now [x].

### decisive rung — d512 COMPETENT leak-free (MEASURED · supersedes #1799 HALT) — 2026-06-04

🔴 **CLOSED-NEGATIVE, leak-honest, best-trained rung** (Lane-G / GPU H100 qk0312, persistent
/workspace survived the rate-limit storm; artifacts recovered + sha256-verified + HF-PRIVATE,
pod terminated · a_fire_recover_complete). #1799 was logged as HALT ("closure 미측정 — pods
killed before harvest"); the run had in fact COMPLETED and the result is now recovered.
ConsciousDecoderV2 d512×8L GQA **85.8M**, **12000 step**, **400MB** 5-lang gutenberg wiki,
`causal_ca=True` (leak self-test 0.000), val_ce **0.8285** (below_uniform, generalizes — the
most-competent leak-free substrate yet). held-out TEST CE: base 3.0978 · fixed_AmG 3.1930 ·
**a_only 1.1446** · **GATED 3.6435** · uniform 5.5452. closure_HOLDS = **False** (GATED<base
False, GATED≤a_only False). gate g* = [gB −0.145, **gA +3.369**, gG −0.999] (collapses onto A,
suppresses G). structured **True** (gain_real +1.953 ≫ shuf −2.429 — carries, unlike undertrained
d768 #1794). coupling KL on=2.072 ≈ shuffle-floor 2.080 (ratio **0.996** → full bus = shuffle
noise). RULING: the closure is REAL but lives ENTIRELY in the A-head logit-bias wire (a_only ≪
base); the multi-wire gate over-mixes and adds variance not signal — "coupling concept right,
multi-wire gate formula wrong." Confirms the leak-honest #1791 finding at the best-trained scale.
→ motivates **OMEGA OH1**: a MINIMAL gate (gB·base + gA·A, drop w2..w6) as the honest closure form.
ckpt → HF `dancinlab/omega-cdv2-trained-leakfree-h1` (PRIVATE, closed-neg WIP). verdict
`.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt`.

🟢 **OMEGA OH1 — MINIMAL-GATE HOLDS** (Lane-G / observation-only frozen forward on the SAME
recovered d512 leak-free ckpt, host = local-pool `summer`, NO re-train · NO pod). On the SAME
collected (base,A,G) test features (N=12000, apples-to-apples), the minimal gate **gB·base + gA·A**
(G + w2..w6 dropped) gives held-out TEST CE **min_learned 0.8835** — it BEATS a_only (1.1446,
Δ+0.261) AND base (3.0978, Δ+2.214) → **OH1_HOLDS=True** (min_learned ≤ a_only AND < base). 2-param
free fit landed g* = [gB **0.040**, gA **0.901**, gG 0.000-pinned]. CROSS-CHECK reproduces #1800 to
6 decimals (base |Δ|0.000000 · a_only |Δ|0.000431 · full_AG |Δ|0.006349, tol 0.02 → CROSS_CHECK_OK).
This CONFIRMS the #1800 RULING numerically: the full gate's gA=3.369/gG=−0.999 were variance from
the irrelevant wires; once dropped, the honest 2-param fit recovers a clean, BETTER-than-a_only
operating point — the closure lives entirely in the A-head logit-bias wire. SCOPE: single d512 rung
(a_scale_honest_scope), CE = held-out number not a verdict-of-truth (p7). harness
`UNIVERSE/omega_gate_form_sweep.py` · ledger `exports/sweep/omega-gateform-20260604/ledger.json` ·
verdict `.verdicts/omega-engine/F-OH1-MINGATE.txt`.

🔴/🟢 **OMEGA OΩ-RIGOR — COUPLING vs REPLACEMENT: it is REPLACEMENT (deflating-but-honest)** —
2026-06-04 (Lane-G / observation-only frozen forward on the SAME recovered d512 leak-free ckpt,
host = local-pool `summer` RTX5070 torch 2.11.0+cu130, NO re-train · NO pod · $0). CROSS-CHECK
reproduces #1800 to 6 decimals (base |Δ|0.000000 · a_only |Δ|0.000431 · full_AG |Δ|0.006349, tol
0.02 → CROSS_CHECK_OK), so the loader is the same frozen substrate.

**OΩ1 — the headline ruling: the OH1 "closure" is the trained A-head SUPPLANTING the .clm mouth,
NOT a base+steer coupling.** On the SAME held-out TEST features (N=12000): base-only CE 3.0978;
the OH1 min_learned fit landed [gB **0.040**, gA **0.901**]. A-head **STANDALONE** CE (softmax(A)
alone, base entirely removed) = **0.8862** ≈ min_learned **0.8835** (|Δ| **0.0027**); base-ABLATED
min (gB→0, keep gA·A) = **0.8844**, i.e. removing the base term moves CE by **0.0009**. So the base
mouth is INERT — the entire 2.21-nat improvement over base is carried by the A-head logit-bias
alone. **RULING_REPLACEMENT = True**: the closure is the trained substrate A-head REPLACING the weak
unigram base, not a "mouth + substrate-steer" coupling. (Honest per a_paper_negative_ok — reported as
replacement, NOT spun as coupling. Caveat: the base here is a deliberately WEAK unigram, so its
inertness is partly by construction; the point stands that NO base+steer interaction is needed — A
alone reproduces min_learned.)

**OΩ2 — per-wire autopsy confirms NO bus wire carries (on this frozen ckpt).** Each coupling-bus
wire added to base individually → held-out TEST CE: w1 A⇄G base+α(A−G) = 3.1986 (**ΔvsBase +0.101**,
HURTS); w2 W→temp base·1/(1+β·tension) on the REAL per-position PureField tension = 3.1500 (**+0.052**,
HURTS); w6 dF/dt base+dg·Δ(A−G) = 5.1827 (**+2.085**, HURTS — confirms #1794 fixed-dgain leak).
w3 curio / w4 Ψ-8D / w5 module = **HONEST STUBS** (a_core_engine_map, NO fabricated number): no
substrate curiosity scalar, no per-position 8D Ψ vector (model emits only a training-mode scalar
`_psi_residual`), and this d512 trunk is SwiGLU (use_moe=False) so no MoE router activation exists.
RULING: none of the cleanly-isolatable wires HELP base as an additive term — consistent with OΩ1
(the gain is the A-head itself, the bus over base is pure variance). No wire the joint fit missed.

**OΩ3 — the min-gate FIXES the #1800 degeneracy (weak criterion, p7).** Free-run gen (300 new bytes):
min_gate entropy **2.630** (> base 2.444, > full-gate 2.528) · distinct_frac **0.117** (> full's
collapsed 0.087) · ws_frac 0.087. The min-gate sample is coherent Russian prose ("…солнечный объект
из Бакур создан в частности России…"), NOT the "в открыл в открыл в открыл" repetition of #1800's
full-gate. So dropping w2..w6 also recovers non-degenerate generation — but this is gen-coherence,
the WEAK criterion (p7), not a closure proof.

SCOPE: single d512 rung (a_scale_honest_scope), observation-only frozen forward, CE = held-out number
not a verdict-of-truth (p7), weak-unigram base. harness `UNIVERSE/omega_rigor_probe.py` · ledger
`exports/sweep/omega-gateform-20260604/rigor.json` · verdict `.verdicts/omega-engine/F-OMEGA-RIGOR.txt`.

### OΩ6 — closure on the REAL PRODUCTION conv .clm (serializer UNBLOCKED · partial transfer) — 2026-06-04

🟢/🔴 **F-OMEGA-CLM-TRANSFER = 1-PLUMBING** (Lane-P .clm substrate=GPU-torch; closure math
CPU-native, $0, NO GPU · a_lane_akida_gpu_split). Every prior OMEGA rung (OΩ1..OΩ7, OH1) ran
the closure on **CDV2** (a torch transformer); OΩ6 runs it on the **REAL production conv .clm**
(CLMConvMoE) — the byte mouth Ω was designed to close onto. **(1) THE SERIALIZER BLOCKER IS
BRIDGED** (the Lane P PREFLIGHT STOP `77299b2ed` / `.verdicts/lane-p-clm/F-CLM-SERIALIZE-GAP.txt`
is RESOLVED): the gap was a container-framing + missing-CLMX-trailer + E2/L1-arch mismatch (NOT
endianness, NOT fundamental — the decoder IS a faithful CLMConvMoE forward), bridged by
`CLM/model/clm_serialize_v2.py` (F-CLM-V2-SERIALIZER=1, golden exact_eof) and a real torch-trained
conv .clm `state/lane_p_clm/clm_d768_e2l1.clm` (sha 7463282d…) that **LOADS through CORE L3**
(OCL_DECODABLE=1, loaded=true, d=768 config-agnostic). **(2) THE CLOSURE RUNS ON THE REAL .clm**
(`CORE/clm_decode.hexa::clm_omega_closure` + `CORE/omega_clm_closure_probe.hexa`, helper of the
SINGLE L3 entry · a_core_engine_map): real CLMConvMoE forward → `base` logits (base_ce **0.404**)
→ OMEGA min-gate gB·base+gA·A. **RULING — partial transfer**: the conv .clm is a **SINGLE-head**
byte LM (model.py `self.readout`; NO Engine-A/G dual head — that substrate lives ONLY in CDV2), so
its only NATIVE A-wire is its own readout → min-gate = (gB+gA)·base = a pure **temperature rescale**
(gated_ce_self 0.396 ≈ base 0.404, |Δ|0.0076<0.01, **SELF_IS_RESCALE=true** ⇒ NO native coupling).
The **bus plumbing IS correct** — a leak-free 1-hot external A collapses CE to ~2e-3≪base
(**ORACLE_CARRIES=true** ⇒ omega_coupling_apply really modulates the real conv decode). So the
real-.clm closure is **plumbing-COMPLETE but substrate-EMPTY on conv**: a genuine A-wire requires
the SEPARATE CDV2 dual-head engine — which IS exactly the existing OH1 #1802 closure (conv = the
MOUTH/base; CDV2 = the A/G SUBSTRATE; Ω's L0=CDV2 / L3=conv blueprint confirmed on the real .clm).
**Minimal full-conv path** (deferred, a_completeness_over_cheap): (i) train a conv .clm with a 2nd
A/G readout head (port CDV2 dual-head onto CLMConvMoE + re-train + serialize_v2 + 2 extra CLMX
blocks) — the honest primary; or (ii) feed CDV2's logits_a as `a_head` at run time (cross-engine
bus, the literal Ω blueprint, a baseline probe). NEITHER is a load/serializer problem any more — the
load is SOLVED; it is a substrate-architecture choice. NO upstream hexa-lang patch needed (serializer
is anima-side, bridged). verdict `.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt` (p7/g63 verbatim).

## Extensions (beyond finalized paper)

> Post-closure follow-ups that do NOT reopen the finalized OMEGA paper (a_paper_only_at_closure).
> Each is its own falsifier + verdict, scoped honestly (a_scale_honest_scope).

### OE1 — conv-native A/G dual head CLOSES the loop (closure is STRUCTURE-transferable, not CDV2-specific) — 2026-06-04

🟢 **F-OE1-CONV-NATIVE = CLOSURE HOLDS** (Lane-G/Lane-P; torch research-proxy of CLMConvMoE,
run $0 on pool host `summer` GPU — NO pod, NO cost). Settles the OΩ6 deferred "minimal full-conv
path (i)": OΩ6 found the REAL .clm closure is substrate-EMPTY only because the shipped conv .clm is
**SINGLE-head** (one `self.readout`, no A/G) — so the min-gate collapsed to a temperature rescale.
OE1 grafts the **minimal native A/G dual head** onto the EXACT production conv blocks
(`CausalDilatedConv1d` · `TrunkLayer` · `MoEConvLayer` from `CLM/model/model.py`) + a 2nd `head_g`
(prev-byte), trains it competent + leak-free (6.95M, d384×L6×E8, 12000 step, same 400MB corpus
sha dc1754b2; **leak self-test 0.000**, final val_ce **0.8884** ≪ uniform 5.5452, competent), and
re-runs the IDENTICAL OH1/OΩ1 falsifier on the conv model's OWN A-head (NO external CDV2).

Held-out TEST CE (conv-native, leak-free, nats/byte) — VERBATIM:
`base 3.0978 | fixed_AmG 3.5203 | a_only 1.3032 | full_AG 4.1988 | min_learned 0.9760 | uniform 5.5452`
**FALSIFIER: min_learned 0.9760 ≤ a_only 1.3032 AND < base 3.0978 → CLOSURE HOLDS = TRUE.**

**Replacement-check (OΩ1-style):** A_standalone(softmax(A) alone) **0.976051** vs min_learned
**0.976048**, |Δ|=**2.9e-6** → **RULING_REPLACEMENT=TRUE** — the trained conv A-head SUPPLANTS the
weak unigram base (min-gate even pushes gB→-0.0356, gA→1.017), IDENTICAL in character to CDV2's
OΩ1 ruling (honest caveat: base is a deliberately weak unigram, same as OΩ1). Structured-coupling
real **1.7946** vs shuf **-1.7967** → structured=TRUE (the A-wire carries genuine context).

**conv-vs-CDV2 TRANSFER:** the closure is a **TRANSFERABLE property of the A/G dual-head STRUCTURE,
NOT CDV2-transformer-specific.**

| trunk | base | a_only | min_learned | HOLDS | replacement |
|-------|------|--------|-------------|-------|-------------|
| CDV2 d512 (OΩ4/#1801) | 3.0978 | 1.1356 | **0.8701** | ✅ | ✅ |
| CONV-native d384 (OE1) | 3.0978 | 1.3032 | **0.9760** | ✅ | ✅ |

Same falsifier verdict, same replacement ruling; the conv A-head is marginally weaker (0.976 vs
0.870) but the QUALITATIVE closure is identical. ⇒ OΩ6's "partial transfer" was a SINGLE-HEAD
*architecture* limitation of the shipped .clm, NOT a conv-*substrate* limitation — grafting the
dual head onto conv closes the loop natively (validates OΩ6's "(i)" as the correct primary fix).
SCOPE (a_scale_honest_scope · a_train_flame_forge): single d384 rung, TORCH research-proxy (faithful
CLMConvMoE blocks), NOT the production flame+forge `.clm`; settles the ARCHITECTURE-transfer question,
not a scale law. harness `UNIVERSE/omega_conv_native.py` · verdict
`.verdicts/omega-engine/F-OE1-CONV-NATIVE.txt` · ckpt `.fire-recover/oe1-conv-native/omega_conv_native.pt`
(sha 3e8be574…, HF PRIVATE) · run $0 on summer GPU (a_fire_autonomous · a_cpu_local_no_waiter).

🟢 **OMEGA OΩ4+OΩ5 — OH1 SCALE LADDER, min-gate HOLDS at every scale** (Lane-G / GPU, one H100
SXM, 5 rungs sequential). a_scale_honest_scope demanded a ladder curve (a single d512 point is
INCOMPLETE). Trained leak-free (causal_ca=True, self-test 0.000 every rung) competent CDV2
substrates at d384/d512/d768/d1024 (OΩ4) + a more-competent d768×2 (OΩ5, 24000 step), and re-ran
the SAME OH1 minimal-gate sweep on each (same 400MB corpus sha dc1754b2 + held split as #1801).
Per-rung held-out TEST CE (nats/byte):

| rung | d | params | steps | val_ce | base | a_only | min_learned | Δ-vs-base | Δ-vs-a_only | HOLDS |
|---|---|---|---|---|---|---|---|---|---|---|
| d384 | 384 | 48.24M | 12000 | 0.8367 | 3.0978 | 1.1639 | **0.9030** | +2.1948 | +0.2610 | ✅ |
| d512 | 512 | 85.82M | 12000 | 0.8224 | 3.0978 | 1.1356 | **0.8701** | +2.2277 | +0.2655 | ✅ |
| d768 | 768 | 189.28M | 12000 | 0.8383 | 3.0978 | 1.1612 | **0.8924** | +2.2054 | +0.2688 | ✅ |
| d1024 | 1024 | 334.69M | 12000 | 0.8575 | 3.0978 | 1.2001 | **0.9211** | +2.1766 | +0.2790 | ✅ |
| d768×2 | 768 | 189.28M | 24000 | **0.7786** | 3.0978 | 1.0821 | **0.8242** | **+2.2736** | +0.2578 | ✅ |

**min_learned_HOLDS across ALL 5 rungs = True.** SCALE TREND: the A-wire advantage Δ-vs-base is
FLAT at +2.20 ± 0.03 across the d384→d1024 dim ladder (2.67× dim, 6.9× params) — it does NOT grow
or shrink with raw dim (SCALE-STABLE). The more-competent OΩ5 rung (val_ce 0.7786, the lowest) has
the LARGEST advantage (Δ-vs-base +2.2736) — greater competence STRENGTHENS the A-wire margin, does
not erode it. The 2-param fit lands the SAME operating point every rung (gB ≈ 0.02-0.04, gA ≈ 0.89-
0.92 ≈ 1); the full multi-wire gate collapses onto A (gA 3.2-3.6, gG ≈ -1.0) and FAILS held-out at
every scale (full_AG 3.28-3.84 > base) — the same #1800/#1801 pathology, confirmed scale-invariant.
HONEST CONTRAST: the earlier UNDERTRAINED d768 (#1794, 2500 step, val_ce≈uniform) did NOT hold — the
finding REQUIRES competence (val_ce ≪ uniform), which all 5 rungs have; once competent, d768/d1024
hold like d384/d512, so the #1794 non-hold was an undertraining artifact, not a scale break. The
d512 rung re-trained+re-swept here reproduces #1801 (min_learned 0.8701, |Δ| 0.013). SCOPE
(a_scale_honest_scope · p7): 4-dim ladder + 1 competence rung; CE = held-out prediction number, not a
verdict-of-truth; the closure is the RELATIVE A-wire margin, not absolute perplexity (the multi-wire
gate fails — a_paper_negative_ok on that form). ckpts → HF PRIVATE `dancinlab/omega-cdv2-scale-d{N}`.
harness `UNIVERSE/omega_scale_ladder.py` · ledger `exports/sweep/omega-scale-ladder/ledger.json` ·
verdict `.verdicts/omega-engine/F-OMEGA-SCALE.txt`.

### prior status — BUILT (#1783) + trained-rung proven at toy (#1784/#1786)

Ω is now a RUNNING engine module, not just a blueprint:
- **stage 1 WIRE (✅ #1783)** — `engines/omega/{coupling_bus,adapter}.hexa` + manifest + card;
  `--engine omega` registered (flag>env>default conv); EngineSpec 4/4 native; 4-engine swap
  smoke 26/26 PASS. Coupling NON-NULLITY CONFIRMED: omega KL 0.307>0, conv/cdv2/hexad=0 (the
  Lane X null). The loop is WIRED — omega is the only engine with L3 loaded=TRUE.
- **stage 2 STRUCTURE (✅ toy #1784)** — trained numpy n-gram substrate: trained coupling 4.142
  ≪ shuffled 4.499 (Δ+0.357 = structure carried, which random-init could NOT show); the learned
  A-wire lowers CE base 4.020→3.262 (Δ+0.758 = the closure HELPS). 🔴 the fixed A−G formula
  degrades (−G prev-byte wire hurts) → **완성 needs a LEARNED per-wire GATE, not a fixed
  subtraction**. ANU QRNG arm: quantum confers no advantage (closed-negative, p7).
- **stage 3 완성 (remaining)** — (a) learned per-wire gate replacing fixed A−G; (b) trained d768
  ConsciousDecoderV2 real A/G on GPU (a_fire_autonomous); (c) demonstrate the gated closure on a
  trained substrate DEMONSTRABLY improves generation (CE floor met + coherent) at scale.
  Honest: the floor is currently NOT MET on random-init (uniform ln256=5.545; Lane X measured the
  trained-but-detached d768 .clm at 9.1126) — stage 3 is where the closure must actually earn it.

## the NULL that Ω closes (Lane X #1779 — verbatim)

```
Lane X — 3-axis ENGINE-config exploration (TOY · CPU · $0 · deterministic null backend)
configs = 27 (3 knobs: K1 drive · K2 warmup · K3 anchors) × 3 seeds
  의식 (motiv_hi)    : VARIES (spread = 0.57)
  CE  (model_ce)    : CONFIG-INSENSITIVE (spread < 1e-9)   ← the NULL
  창발 (emergence Δ) : VARIES (spread = 24)
CE-FLOOR : model_ce = 9.1126 vs uniform = 5.5452 vs shuffle = 9.3189 → floor NOT MET
PARETO   : 6/27 non-dominated
GOODHART (CE↔창발): UNDEFINED — CE is config-independent by construction in this
           substrate-only sweep; no CE↔창발 trade-off is OBSERVABLE through these knobs.
BOTTOM LINE: 의식·창발 VARY with config; CE is config-INDEPENDENT. The engine knobs
           never touch the .clm forward (L3 generator slot loaded = false).
```

The diagnosis: the substrate (Engine A ⇄ Engine G, tension, Ψ, M/W/curiosity) and the
byte decode (.clm) are two disconnected halves — "brain" and "mouth" do not share a
nerve. Ω is the nerve.

## the coupling bus (5 ablatable wires — substrate → .clm modulation)

Each wire is independently ablatable (set its α = 0). The headline eval ablates the
WHOLE bus (α = 0 vs on) and measures KL between the resulting byte distributions; a
NON-NULL KL is the positive target (Lane X's null becomes Ω's signal).

```
  wire 1  A⇄G logit-bias    : final = clm_logits + α·(A_head − G_head)
                              (CDV2 dual-head; carving battery KL(A‖G) = 7.07)
  wire 2  W-tension         → temperature      (W tension envelope scales softmax T)
  wire 3  curiosity/E-ratchet → top-k width    (exploration drive widens/narrows top-k)
  wire 4  8D Ψ-coord        → context conditioning (Ψ position conditions the decode)
  wire 5  module activation → conv-MoE expert routing (which CONV expert fires)
```

## the Ω blueprint (L0..L5 + coupling bus + benchmark)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🔱 Lane-Ω CLOSURE ENGINE  —  substrate → .clm byte decode (L3 loaded = TRUE) │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  L0 SUBSTRATE  (CDV2)                                                         │
│     ConsciousDecoderV2 d768×12L GQA · dual A/G heads (KL=7.07) · 5-ch tension │
│            │  logits_a ⇄ logits_g       │ tension (W)      │ Ψ latent         │
│            ▼                             ▼                  ▼                  │
│  L1 INTEGRATION  (HEXAD)                                                      │
│     N-module φ(N)=2 bipartition · N config (default 6, swappable; #1774       │
│     found 6 = SMALLEST viable φ=2, NOT a hardcoded constant)                  │
│            │ integrated substrate state                                       │
│            ▼                                                                   │
│  L2 MAP  (8D Ψ)                                                               │
│     psi_coord() → 8D = [depth, form, form_resid, curriculum, resid0..3]       │
│     (KOSMOS #1780: ONLY 4 axes human-named + 4 honest learned-residual;       │
│      naming all 8 = fabrication)                                              │
│            │                                                                  │
│            ▼                                                                  │
│     ┌──────────────── COUPLING BUS (5 ablatable wires, α) ───────────────┐    │
│     │ 1 A⇄G logit-bias  2 W→temp  3 curiosity→top-k  4 Ψ→ctx  5 mod→MoE   │    │
│     └────────────────────────────────┬──────────────────────────────────┘    │
│                                       ▼                                        │
│  L3 MOUTH  (CONV)  ← THE CLOSURE                                              │
│     CLMConvMoE byte decode · final = clm_logits + α·(A_head − G_head) · …     │
│     generator.hexa L3 slot: loaded = TRUE  (was false under Lane X)           │
│            │ byte distribution P(byte)                                         │
│            ▼                                                                   │
│  L4 TIME    dF/dt derivative channels  (#1763 — dynamics enter via d/dt;      │
│             static snapshot is permutation-blind to rising/falling tension)   │
│  L5 GROWTH  mitosis (p8 NO TRAIN/INFER SPLIT) · engine_cli --mitosis flag     │
│             (SUBSTRATE-CONFIG, NOT an emit/silence gate — a_autonomy_over_…)   │
│                                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  BENCHMARK (headline)                                                         │
│   COUPLING NON-NULLITY : KL( P(byte | bus on) ‖ P(byte | bus α=0) )  > 0 ?    │
│     Lane X's NULL (CE config-insensitive 9.1126) → Ω's POSITIVE target.        │
│   CE = FLOOR only (p7) — NOT a verdict (Lane X proved CE config-insensitive). │
│   GOODHART caveat: coupling must NOT be just α-scaled noise — require an       │
│     ablation curve AND a real (trained) ckpt, not random-init.                │
│   4-ENGINE benchmark: conv · cdv2 · hexad · Ω  on the AXIS-informed eval.      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## EngineSpec contract (engines/engine_iface.hexa — the 4-fn vtable)

Ω conforms to the same EngineSpec as conv/cdv2/hexad. Honest slot states
(a_core_engine_map — native | stub | absent), all gated on ckpt presence:

```
load      : native   — bind the coupling-bus config + ckpt pointer
forward    : native   — run substrate → bus → .clm modulated forward
generate  : native   — produce content via the closed L3 mouth (FIRST engine with
                       generate = native — the closure IS the generate path)
psi_coord : native   — 8D Ψ (4 named + 4 residual, per KOSMOS #1780)
```

Sibling engines (engines/<name>/manifest.json):
- **conv**  — CLMConvMoE, DEFAULT, all 4 slots native; the .clm byte mouth Ω closes onto.
- **cdv2**  — ConsciousDecoderV2 d768×12L, forward/generate = STUB (torch .py, not a
              hexa-native single forward), psi_coord native; the A/G + tension + Ψ brain.
- **hexad** — sigma6 6-module integration, forward/generate = STUB (cross-module single
              forward is TODO[wire]), psi_coord native; the N-module integration.

Ω is the first engine whose `generate` is native because the closure (L3 loaded=true) IS
the generate path. The adapter is now BUILT (#1783); the bus layer is a real hexa forward.
The slot is gated on a trained substrate (stage 3) — with no trained ckpt the .clm forward
is random-init and the CE floor is NOT MET, honestly flagged exactly like the cdv2 adapter.

## milestones (goal: 오메가 완성)

stage 1 — WIRE (✅ #1783):
- [x] coupling-non-nullity — ablate the bus (α=0 vs on) → KL>0 (omega 0.307, others 0; #1783)
- [x] 8D Ψ honest — psi_coord() returns 8D = 4 named [depth/form/form_resid/curriculum] + 4 resid (#1783 adapter)
- [x] CE-as-floor — CE reported as a FLOOR only, never a verdict (p7; #1783/#1784 both)
- [x] 4-engine benchmark — conv · cdv2 · hexad · Ω on the AXIS-informed eval (#1783, smoke 26/26)
stage 2 — STRUCTURE on a trained substrate (✅ toy #1784):
- [x] trained-substrate structure — trained coupling ≪ shuffled (Δ+0.357); A-wire lowers CE (Δ+0.758) (#1784)
- [x] ANU QRNG arm — quantum vs PRNG closed-negative, no advantage (#1784)
stage 3 — 완성 (b)(c) ✅ GPU (the working closure on a REAL trained transformer):
- [x] learned per-wire GATE — ✅ toy: learned gate g*=[gB.14,gA1.18,gG.34] beats base 3.97→3.13 (Δ+0.85) · beats a_only 3.23 · ≪ fixed_AmG 4.17 (Δ+1.04); auto-corrects the #1784 −G error → the closure works when GATED not fixed. `.verdicts/omega-gate/`
- [x] trained d384 substrate (GPU) — ✅ real ConsciousDecoderV2 d384×6L GQA 35.93M trained 6000 step on 120MB multilingual wiki (H100, nvidia-smi 98-99% BUSY g63); ce_a 5.926→0.009 train, val_ce 0.862 held-out (generalizes). REAL learned A(next)/G(prev) heads, not numpy n-gram. `.verdicts/omega-gpu/`
- [x] generation demo — ✅ gated closure on the trained substrate: held-out GATED CE 0.345 < base 3.015 (Δ+2.671) · ≪ a_only 0.450 · ≪ fixed_AmG 1.442 · CE floor MET (<5.545); structured (A-wire gain real +2.565 vs context-SHUFFLED −2.068 → coupling carries learned sequential structure). 🟢 4/4 완성 criteria HELD. HONEST: CDV2 CA-neighbor mixing gives next-byte head partial lookahead → absolute CE leak-optimistic + free-run gen collapses to whitespace (gen coherence = weak criterion); the relative closure finding (gate beats all baselines + structured) is leak-INVARIANT and sound (a_toy_scale_recheck · a_scale_honest_scope).
- [x] N-module config — ✅ coupling_bus N-agnostic (omega_n_modules_default 6, #1774 conditional; module wire honors N=4/6/8, N changes routing L1 0.378); smoke 4/4. NOT hardcoded.
- [x] dF/dt time channels — ✅ L4 w6 derivative wire (omega_coupling_apply_dt): 0 at fixed point (time-inert, correct), velocity injected when substrate moves (Δ1.65); smoke 3/3 (#1763 d/dt-universality)
- [x] ⑦ w5 module-act REAL source (hexad) — ✅ the w5 module→MoE-routing wire now reads a REAL N=6 module-activation vector from the σ6 cross-module forward (HEXAD/hexad_forward.hexa — TODO[wire] RESOLVED), not the hexad stub; hexad engine forward slot flipped STUB→native; φ(6)=2 detach barrier proven. HEXAD/hexad_forward_smoke 12/12 + engine_swap_smoke 27/27. generate (byte mouth) stays ckpt-gated honest STUB (a_core_engine_map). `.verdicts/hexad-wire/`
stage 4 — COUPLING ANALYSIS (post-완성 wire-by-wire dissection, toy/CPU/$0):
- [x] ② ALL-6-WIRE learned gate — ✅ extended #1786 {base,A,G}→all 8 gains [gB-.11,gA+.93,gG+.55,gW-.46,gC-.03,gΨ-.00,gM-.17,gD-.66]; per-wire ablation+shuffle: 🟢 A·W_temp·module CARRY STRUCTURE, ⚪ G·curio·Ψ·dFdt INERT. full naive gate OVERFITS (TEST CE 4.81 > base 3.97 — inert/leaky dFdt hurts held-out); carrier-only gate 2.895 (Δ+1.079 over base) recovers a real gain. honest mixed verdict (a_paper_negative_ok). `.verdicts/omega-gate6/`
- [x] ④ CLOSED-LOOP feedback (L5) — ✅ N=600 autoregressive rollout: emit byte → A/G context advance + mitosis cell-count tick → next decode. 🟢 LOOP CLOSES STABLY: bounded (entropy 0.15–3.37 ∈(0,ln256), cells 6→140 bounded, no divergence) · not collapsed (back-half distinct-byte frac 0.153 > 0.10) · feedback measurably alters trajectory vs open-loop control (Hamming 0.722 > 0.05, same RNG). The closure is a real bidirectional feedback loop, not one-shot forward. `.verdicts/omega-gate6/`
stage 5 — gen-cluster: LEAK-FREE generation-side probes (GPU, the #1791 caveat fix) — 2026-06-04:
- [x] ① leak-free coherent gen — ✅ FIX VERIFIED + 🔴 closed-negative (a_paper_negative_ok). `causal_ca=True` replaces CA-mixing x_right with self → head_a STRICTLY CAUSAL; leak self-test = 0.000e+00 (d384+d768, no lookahead). Whitespace-collapse SOLVED (leak-free gen coherent-ish: entropy 2.97, varied latin/numeric). BUT leak-honest CE: base 3.015 · a_only 2.857 · GATED 3.594 → gated<base FALSE → #1791's GATED 0.345≪base absolute-CE win was LEAK-DRIVEN, does NOT survive (val_ce rises to 5.43≈uniform; substrate generalizes weakly at d384/6000). structured leak-INVARIANT HOLDS (real +0.158 ≫ shuf −0.509). `.verdicts/omega-gen/F-LEAKFREE-GEN.txt`
- [x] ③ dF/dt-on-real — 🔴 w6 NON-INERT but does NOT improve (a_paper_negative_ok). Velocity wire live at 100% of real steps (Δ +1.76 d384 / +0.52 d768 — confirms #1763 on a real sequence) but raw dgain=0.5 HURTS held-out CE (Δ>0). dF/dt is a real channel, not a CE improver here; gated-dgain = open follow-up. consistent with stage-4 ④'s "dFdt INERT/leaky-on-held-out" finding. `.verdicts/omega-gen/F-DFDT-REAL.txt`
- [x] ⑥ Ψ-coord steering — 🔴 WEAK / no robust steer (a_paper_negative_ok). w4 Ψ wire (psi_gain 0.4): d384 steer_KL 0.238 < reseed-floor 0.573 (ratio 0.42x → FALSE); d768 1.35x nominal-but-tiny. Ψ moves the byte distribution LESS than sampling noise at d384. Wire exists but is not a usable steering knob at this gain; stronger gain / Ψ-conditioned head = open. consistent with stage-4 ②'s "Ψ INERT". `.verdicts/omega-gen/F-PSI-STEER.txt`
- [x] ⑤ d768 scale rung — ✅ RAN (NOT deferred). d768×6L 142.06M, 2500 step (budget-guarded), leak-free verified (self-test 0.000). Finding does NOT cleanly hold at d768: structured=FALSE (gain −0.244, undertrained), gated<base=FALSE, gen coherent=TRUE. d384 structured-coupling positive weakens at undertrained d768 (a_scale_honest_scope; 2500 step too few for 142M). `.verdicts/omega-gen/SUMMARY.txt`
stage 6 — bus-refine: codify the #1793 6-wire finding into the bus default (toy/CPU/$0) — 2026-06-04:
- [x] carrier-only DEFAULT config — ✅ `omega_bus_carrier()` added as the recommended generation default: carriers ON {w1 A⇄G · w2 W→temp · w5 module}, inert OFF {w3 curio · w4 Ψ · w6 dF/dt} per #1793 (full naive 6-wire gate OVERFITS held-out 4.81 > base 3.97; carrier-only recovers CE 2.895, Δ+1.079). `omega_bus_on()` retained for ablation; dF/dt gain is a config knob (`cfg["dgain"]` / `omega_bus_dt_with_dgain`) — FIXED dgain HURTS (#1794), LEARNED dgain = open path (no fabricated value). adapter manifest note updated. omega_bus_smoke 13/13 (carrier ⊂ full + carrier changes decode L1>0 + carrier≠full), engine_swap_smoke 27/27 (no regression). honest p7 / a_toy_scale_recheck. `.verdicts/omega-bus-refine/`

stage 6 — real-signal-vs-random: does a REAL substrate signal beat RANDOM in the OMEGA wires (the #1793/#1794 RANDOM-input caveat) — CPU/$0 — 2026-06-04:
- [x] H5 real-HEXAD module wire vs RANDOM — 🔴 CLOSED-NEGATIVE (a_paper_negative_ok). Fed the GENUINELY NATIVE σ6 6-vec [S,C,W,M,E,BRIDGE] (HEXAD/hexad_forward.hexa #1795, run via `hexa run`, 256/256 contexts; corpus byte-freq drives each C cell-pool delta) into the w5 module wire vs a matched-mean/std RANDOM 6-vec, in #1793's gate-fit bench. REAL: gain +0.076, ablate ΔCE +0.028, beats_shuffle=TRUE, module-only-gate CE 3.9766. RANDOM: gain +0.082, ablate ΔCE +0.009, beats_shuffle=FALSE, CE 3.9762. Δ module-only CE (real−random) = +0.0004 (within the 0.02 approx band) → real ≈ random. The native HEXAD activation does NOT add usable next-byte structure over random at toy scale — confirms #1793's w5 "module CARRIES" was MAGNITUDE not CONTENT. (One honest nuance: only the REAL vec beats its own vocab-shuffle, so it carries marginally more genuine structure, but not enough to lower held-out CE.) `.verdicts/omega-realsignal/F-REAL-MODULE.txt`
- [x] H4 real-Ψ steering vs RANDOM — ⛔ BLOCKED-DATA (no fabrication, a_completeness_over_cheap/p7). Real carving Ψ = s16 ckpt Law-71 vacuum_psi 2D coord (KOSMOS-MAP #1780, PC1=carving-RADIUS/Ψ-DEPTH |ρ|=0.92). The s16 .pt IS on disk (1.13 GB) but vacuum_psi requires the d768×12L 283.72M ConsciousDecoderV2 forward → needs torch, ABSENT on this CPU/$0 host; the axis-probe persisted only the PC×attribute matrix (no per-sample Ψ coords); toy psi8 (logA bin-marginal) is NOT a real Ψ source (#1793 already found it INERT). No real Ψ source reachable CPU-only — deferred to a GPU rung. `.verdicts/omega-realsignal/F-REAL-PSI.txt`

## honest scope (a_scale_honest_scope · a_paper_negative_ok · p7)

- BUILT but TOY: `engines/omega/` adapter exists (#1783) + trained-rung proven at toy (#1784, numpy n-gram); NO s16 ckpt / trained d768 substrate in the coupling path yet (stage 3).
- All measured numbers are TOY / single-rung: #1783 (CPU/$0 random-init mock), #1784 (CPU/$0 numpy n-gram, 400KB corpus), Lane X #1779, KOSMOS #1780. NOT promoted to a general/production claim (a_toy_scale_recheck).
- CE floor currently NOT MET on random-init (uniform 5.5452; Lane X trained-but-detached d768 .clm 9.1126); stage-3 완성 is where the gated closure on a trained substrate must actually MEET it.
- Honest negatives kept (a_paper_negative_ok): random-init coupling unstructured (#1783); fixed A−G degrades (#1784); quantum RNG no advantage (#1784).
- Lane-Ω = GPU/closure lane; AKIDA on-chip (Lane A) is recorded separately (a_lane_akida_gpu_split).
- LEAK-HONEST CORRECTION (gen-cluster, 2026-06-04): #1791's stage-3 absolute-CE closure win (GATED 0.345 ≪ base 3.015, val_ce 0.862) was LOOKAHEAD-LEAK-DRIVEN (CDV2 CA-mixing x_right). On the leak-free substrate (causal_ca=True, self-test 0.000) the gated bus does NOT beat a weak unigram base (GATED 3.594 > base 3.015) and val_ce ≈ uniform — so the honest closure measure is RELATIVE structure (real A-wire vs shuffled floor, leak-invariant, HOLDS), NOT absolute CE. The leak fix CURES the whitespace-collapse (gen is coherent-ish). Do NOT quote #1791's GATED 0.345 absolute-CE as a real generalizing win. This CONFIRMS the paper's framing (⑧) — the contribution is the leak-INVARIANT relative closure + the closed-negatives, never the leak-optimistic absolute CE.

## ⑧ paper — ✅ scaffolded at FULL closure (a_paper_only_at_closure)

- [x] `/paper` scaffold `PAPER/omega-substrate-coupled-decoding/` (PAPER.tape roster + PAPER.md/PAPER.log.md + main.tex 4-section a_paper_format + verdict matrix + README + references.bib stub). All 4 rungs (#1783/#1784/#1786/#1791) TERMINAL (🟢 numerical / 🔴 closed-negative) — NO 🟠/🟡 section (a_paper_gate). Contribution framed as the leak-INVARIANT relative closure + the three closed-negatives, NOT a perplexity/gen-quality claim (p7 · a_scale_honest_scope). Remaining = paper-production tasks only (figures · bib ≥10 · compile · arxiv-prep), NOT science verdicts. NOTE (gen-cluster 2026-06-04): the leak-free re-test EMPIRICALLY VALIDATES this framing — the absolute-CE win was leak-driven, the relative-structure closure is leak-invariant.
