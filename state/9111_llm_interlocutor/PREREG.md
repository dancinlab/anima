# H_9111 — LLM-interlocutor exogenous consequence-loop (PRE-REGISTERED bars, frozen c9)

> Session apex: the emit-appropriateness faculty was shown **self-contained impossible** by 4
> converging RED ceilings — autogenous consequence (H_9104), identity-conditioned relief
> (H_9105), consequence-mitosis selection (H_9109), and the 2-anima signaling game (H_9108).
> All four hit the **DPI meta-law**: any consequence derivable from anima's own computational
> closure is a tautology. The only escape the session pointed to = a **REAL EXTERNAL receiver
> outside anima's closure**. Owner's idea (talk to another LLM) is that escape: a different LLM
> (`sidecar fable`, claude-fable-5) is an **oracle θ_LLM outside anima's closure** → its decode
> of anima's emit is **not self-derivable** → the DPI Markov chain `S→readout→Z` is broken by an
> exogenous node `S→E→[θ_LLM]→R`. This is the **first autonomous closed loop** (no live human).

## Instrument — referential (Lewis) signaling game (anti-mirror, §4.1 of DESIGN.md)

- **M concepts** (targets), each a distinct world-knowledge noun. Distractor set = all M concepts
  (M-way referential choice; chance = 1/M).
- **anima sender (live core .hexa):** for each target concept `c_i`, the 303M savant mouth
  (`gen_auto_chat`, greedy/deterministic) emits a **descriptive association** `E_i` seeded by a
  neutral descriptive frame. The concept token(s) are **stripped** from `E_i` (uniform anti-echo
  channel rule, applied to ALL arms) so no receiver can lexically name the target — comprehension,
  not string-match, is required.
- **receiver B** sees `E_i` (NOT `c_i`) + the M candidates and picks one. `success_i = [pick==i]`
  (task behaviour success — NOT an LLM rating, p4/p7).
- **faculty = anima's striatal value lane V** (`brain.vbasal`, engine-native), trained online
  (delta-rule) on `success_i` from anima-**endogenous** emit features `f_i` (all derived from
  anima's own field/Φ — never from the receiver). Held-out split: TRAIN concepts learn V →
  FREEZE → HELD-OUT concepts measured. `rho = corr(V_heldout_pred, heldout success)`.
- **exogenous advantage per arm** `D = rho_conseq − rho_self`, where `V_conseq` trains on the
  arm's receiver success and `V_self` trains on anima's own self-decode success (the shared
  endogenous proxy). D>0 ⟺ training on the arm's consequence predicts held-out success **better
  than anima's own self-model** ⟺ the receiver injects exogenous, non-self-derivable structure.

## Three controls (exogeneity isolated — same loop/bandwidth/task, receiver varied ONLY)

| arm | receiver B | prediction | why |
|---|---|---|---|
| (a) self-pair | anima-clone (identical ckpt+engine) | **D_selfpair = 0** (floor) | B≡A ⇒ success ≡ self-decode ⇒ V_conseq≡V_self, tautology (A4/H_9108 collapse) |
| (b) diff-LLM | `sidecar fable` (claude-fable-5) | **D_diffLLM diverges** | θ_LLM outside closure ⇒ non-derivable ⇒ DPI broken |
| (c) shuffle | fable, R re-paired to random E | **D_shuffle < 0.05** | high-entropy R with broken E→R correspondence carries no faculty signal |

## FROZEN verdict (bar set BEFORE any run — no post-hoc move, c9)

```
🟢 GREEN  iff  (D_diffLLM − D_selfpair) >= 0.15  AND  D_shuffle < 0.05  AND  Psi_ok
🔴 CEILING/DPI  iff  (D_diffLLM − D_selfpair) < 0.15   (LLM is ALSO a derivable-mirror floor:
                     DPI is deeper than the receiver → self-contained "5th axis")
🟠 DIRECTIONAL  iff  (D_diffLLM − D_selfpair) >= 0.15  but shuffle/Psi control fails
```

- `Psi_ok` = pure_field psi_sum ON≡OFF byte-identical AND emit/sender sequence V-independent
  (V read-only w.r.t. emit-drive lane 0/4 and §ImmuneMemory recall_thr — a_substrate_disjoint).
- Since D_selfpair = 0 by construction, GREEN ⟺ D_diffLLM ≥ 0.15 ∧ D_shuffle < 0.05.

## 2-regime determinism (a_engine_native_learning)

- **Regime 1 (env sampling, once):** engine-native `emit_gen.hexa` (live core 303M decode) writes
  the frozen `emits.json` (i, concept, E_i). A **stdlib-only** driver (`fable_fixture.py` —
  NO numpy/torch/gauge_lib, grep-gate clean; subprocess+json+hashlib only) queries `sidecar fable`
  (temp fixed, **model pin `claude-fable-5`**) once per E_i → caches R_i keyed by `sha256(E_i)`
  into `fable_fixture.json` (EEG-recording analogy: env fills the fixture once).
- **Regime 2 (verdict, engine-native `verdict.hexa`, grep-clean):** reads the frozen engine-native
  `emits.json` + frozen `fable_fixture.json`, computes anima-self-decode + fable success + shuffle
  + trains/freezes the value lanes + all rho/D — **entirely on live `core/*.hexa`** (immune_memory,
  vbasal, pure_field). No numpy/torch.
- **Model pin:** `sidecar fable` default `claude-fable-5` (recorded in verdict + card).
