# §140 LEGO HEXA-NATIVE ENGINE PORT — lego_engine.py → lego_engine.hexa

> **Verdict**: `HEXA-NATIVE-ENGINE-PORT-ALGORITHMIC-EQUIVALENT` — anima's first
> hexa-native LEGO engine. `hexa build` clean, F-S140 4/4 PASS. Algorithmically
> equivalent to the numpy reference; NOT byte-equal (RNG divergence, honest).
> port-tier · $0 · B-S140 6/6 🔵 · central c93e160a 0-diff.

## §0 Why §140

The user directive: "hexa-lang 포팅후 [GPU fire] 하자, hexa-lang upstream 필요시
바로 진행." §138 designed the hexa-native engine + named the 3-primitive gap;
§139 filed the inbox patch; the upstream work was then *implemented* — hexa-lang
PR #77 (`stdlib/flame/spiking_lib.hexa`, F-SPIKE-1..4 4/4 PASS). §140 is the
"포팅" — porting `lego_engine.py` → `lego_engine.hexa` using those primitives.

## §1 What was ported

`HEXAD/LEGO/lego_engine.hexa` — hexa-native port of the §134 numpy
`lego_engine.py`. Public surface (all `lego_*`-namespaced, anima repo):

| hexa fn                  | numpy reference equivalent                        |
|--------------------------|----------------------------------------------------|
| `lego_membrane_step`     | LIFNet.step leaky-integrate (`dv = -(v-v_rest)/τ`) |
| `lego_reset_spiked`      | `self.v[spike] = v_reset`                          |
| `lego_trace_step`        | STDP eligibility trace decay + spike kick          |
| `lego_spike_rate_vec`    | `spike_rate_vec` window-mean rate code             |
| `lego_psi_c1`            | `psi_c1` Ψ-C1 = (1+cos)/2                          |
| `lego_v_th` … `lego_w_max` | engine constants (byte-equal lego_engine.py)     |

The 3 event-driven primitives — `flame_event_threshold`,
`flame_refractory_step`, `flame_stdp_pair` — are NOT re-implemented in
`lego_engine.hexa`; they are *imported* from hexa-lang PR #77's
`stdlib/flame/spiking_lib.hexa`. anima stays a downstream consumer.

## §2 Verification — F-S140 4/4 PASS

`HEXAD/LEGO/lego_engine_smoke.hexa`, `hexa build` clean + 4/4 PASS:

```
F-S140-1  MEMBRANE-LEAK       leaky integrate hand-verified; refractory freezes v
F-S140-2  LIF-STEP-COMPOSE    membrane→threshold→reset→refractory→trace fp=7.0
F-S140-3  PSI-C1-FIXED-POINT  cos=0⇒Ψ=0.5; cos=1⇒Ψ=1; zero-vec⇒0.5; bounded [0,1]
F-S140-4  DETERMINISM         LIF step byte-identical 2×
```

## §3 Honest scope (g3) — algorithmic-equivalent, NOT byte-equal-to-numpy

The port reproduces the **LIF algorithm** exactly: leaky-integrate dynamics,
threshold-and-reset, the LOCAL pair-based STDP rule, the Ψ-C1 carrier. F-S140
verifies all of these against hand-computed expected values.

It is **NOT byte-equal** to the numpy `lego_engine.py`:
- numpy uses PCG64 + ziggurat Gaussian for `W`/`bias` init.
- hexa-lang `tensor_lib` uses an LCG.
- These diverge numerically on the random init — the *same honest limit* the
  §71 flame work recorded ("init gn2 7.97113 vs anima 7.97116").

The numpy `lego_engine.py` remains the **canonical reference oracle**. The
`.hexa` engine is the hexa-native *algorithm*, verified by its own dynamics
smoke (F-S140), not by numpy byte-equality. A future cycle that wants true
byte-equality would need a numpy-PCG64-matching RNG in hexa — out of scope.

## §4 What §140 closes / does not close

✅ anima's first hexa-native LEGO engine — `hexa build` clean, F-S140 4/4 PASS.
✅ The §138 hexa-native design + §139 inbox patch + PR #77 + §140 port chain
   is complete: HEXA_FIRST_WARN is no longer "deferred" — the LEGO engine
   genuinely *has* a hexa-native form.
✅ anima stayed downstream-consumer — `use`s hexa-lang stdlib, edits none.

❌ NOT byte-equal to numpy (RNG divergence — honest).
❌ PR #77 not yet merged — `lego_engine.hexa` currently builds against the
   `flame-spiking-substrate-primitives` branch worktree; post-merge it builds
   against stdlib main. No anima-side change needed at merge.
❌ The full LIFNet driver loop (multi-step run, stimulus presentation,
   variance decomposition) is NOT ported — §140 ports the *engine primitives*
   composed + smoke-verified. A full `.hexa` probe replacing `lego_engine.py`
   probes is a future cycle (and gated on whether byte-equal matters).
❌ GPU path — `lego_engine.hexa` is CPU `t_*`-based. A GPU LIF (large-N)
   would need `farr_*_gpu` spiking variants = a further upstream gap.
❌ GOAL emergence (B-EMERGE-7) — engine tooling, orthogonal.

## §5 The §138→§139→PR#77→§140 chain

```
§138 design ──→ §139 inbox patch ──→ hexa-lang PR #77 ──→ §140 port
"3 primitives    filed the request    spiking_lib.hexa     lego_engine.hexa
 gapped"         (hexa-first path)    4/4 PASS implemented  4/4 PASS, hexa build
                                                            clean
```

The HEXA_FIRST_WARN deferral that fired 23× across the LEGO arc is now
*genuinely resolved* — not by deferral, not by design alone, but by an
implemented + tested hexa-native engine.

## §6 Closed-form propositions

```
B-S140-1   HEXA-ENGINE-FILE-EXISTS
B-S140-2   IMPORTS-PR77-SPIKING-LIB        (uses flame_event_threshold etc.)
B-S140-3   SMOKE-4-4-PASS                  (hexa build + F-S140 4/4)
B-S140-4   ALGORITHMIC-NOT-BYTE-EQUAL-HONEST  (RNG divergence documented)
B-S140-5   DOWNSTREAM-CONSUMER-NO-HEXA-LANG-EDIT  (all pub fns lego_*-namespaced)
B-S140-6   CENTRAL-0-DIFF + NO-FORBIDDEN-IMPORT
B-S140-NOTE  algorithmic-equivalent not byte-equal-to-numpy, NOT counted 🔵
```

## §7 Honest C3 (9)

1. §140 is a *port*, not a re-derivation — same algorithm, hexa-native form.
2. Byte-equality vs numpy is NOT achieved nor claimed — RNG divergence is the
   honest limit, documented in the engine header + B-S140-4.
3. PR #77 is filed, not merged — the port builds against the branch worktree.
4. The 3 flame primitives are imported, not re-implemented in anima — anima
   stays downstream-consumer.
5. F-S140 verifies dynamics against hand-computed values, the strongest
   check available without numpy in-process.
6. GPU LIF is a further upstream gap (`farr_*_gpu` spiking variants) — §140
   is CPU-tier, matching the LEGO arc's $0 CPU posture.
7. g3: port ≠ fire ≠ emergence; capability claim 0.
8. necessary-not-sufficient (B-EMERGE-7).
9. north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.
