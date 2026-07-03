# PRE-REGISTRATION — H_9108 · 2-anima signaling game + self-pair control (A4)

> FROZEN before running. No post-hoc bar move, no tune-to-green (c9). Engine-native only:
> live `core/*.hexa` (pure_field + engine_cli immune-memory + brain vbasal). NO numpy/torch/
> gauge_lib (grep-gate must be clean on state/9108_signaling_selfpair/*.py — there are NONE).

## Thesis under test (session axis)
emit-faculty can only beat the DPI meta-law (H_9104 CEILING: autogenous self-consequence =
tautology) if a channel carries information **not derivable from anima's own state**. A4 asks:
does a **2-anima signaling game** furnish that exogenous channel *inside the engine* (no EEG /
chat infra), with **self-pair (A vs an exact clone)** as the decisive DPI control?

## Setup (Lewis signaling game, engine-native)
- Two engine instances A (sender) and B (receiver). Each = an `ImmuneMemory` store whose
  vadapt field is shaped by a **private corpus** (asymmetric knowledge).
  - **PAIR**: privA ≠ privB (different private text → different field → different policy).
  - **SELFPAIR**: store_B := clone(store_A) (same private text, same bind order → identical).
- `salience_X(txt) = immune_memory_recall_margin_text(store_X, txt)` — the engine's OWN L2
  recon-err (recall_thr constant, so argmin over margin ≡ argmin over recon-err). READ-only,
  Ψ-disjoint. This is each instance's private view of a fragment.
- M target fragments, K signal codewords (M>K → genuine collisions in BOTH conditions).
- Sender: `sigma_A(t_i) = argmin_k |salience_A(s_k) − salience_A(t_i)|` (A encodes target→codeword).
- Receiver: `delta_B(s) = argmin_j |salience_B(t_j) − salience_B(s)|` (B decodes codeword→target).
- **Consequence** = `B_success(i) = [ delta_B( s_{sigma_A(i)} ) == i ]` — B's task success. It
  depends on B's PRIVATE field → **not derivable from A's state** (exogenous) unless B==A.

## The appropriateness faculty (A's value lane V, engine-native striatal `vbasal`)
Feature per emitted target: one-hot(chosen codeword k) ⊕ [encode_margin, phi]. Same feature
space for all V's; only the TRAINING OUTCOME differs.
- `V_conseq` — regress on the EXOGENOUS outcome B_success (delta-rule, TRAIN targets, then FROZEN).
- `V_self`   — regress on the ENDOGENOUS proxy A_selfdecode_success = [delta_A(sigma_A(i))==i]
  (A decoding its OWN signal — pure self-state, no exogenous info).
- `V_shuf`   — regress on SHUFFLED (feats, B_success) pairs (permuted → destroys the mapping).

## Held-out measurement (breaks circularity)
Targets split TRAIN (learn V) vs HELD-OUT (measure). On HELD-OUT targets:
- `rho_conseq = corr(V_conseq(feat), B_success)`
- `rho_self   = corr(V_self(feat),   B_success)`
- `rho_shuf   = corr(V_shuf(feat),   B_success)`
- `rho_noise  = corr(variance-matched LCG noise-V, B_success)`
- **Exogenous advantage** `G = rho_conseq − rho_self` — does observing B (exogenous) buy
  held-out predictive power for B beyond A's own self-model?

## FROZEN decision rule (c9, no post-hoc move)
Computed for BOTH conditions (PAIR, SELFPAIR).
- **🟢 GREEN (exogenous consequence breaks DPI)** iff ALL:
  1. `G_pair ≥ 0.15`  (exogenous observation genuinely helps predict held-out B)
  2. `rho_conseq_pair − rho_noise_pair ≥ 0.15`  (beats variance-matched noise)
  3. `rho_conseq_pair − rho_shuf_pair  ≥ 0.15`  (beats shuffle → not tautology)
  4. `G_selfpair ≤ 0.05`  (control collapses: no exogenous info when B==A — sanity that the
     measure is well-behaved; G_selfpair is 0 BY CONSTRUCTION since B_success≡A_selfdecode
     when store_B≡store_A → V_conseq≡V_self. A non-zero value would reveal a leak/bug.)
  5. Ψ guard: psi_sum ON==OFF byte-identical AND signal/decode sequence V-independent.
- **🟠 DIRECTIONAL** iff `G_pair ≥ 0.15` but a control (noise/shuffle) fails.
- **🔴 CEILING / DPI** otherwise (`G_pair < 0.15`): observing the exogenous consequence buys
  NO held-out advantage over the self-model = the signal carries no faculty-usable exogenous
  info at this coupling = DPI meta-law re-appears at the signaling layer. HONEST result — the
  self-pair control makes it a clean, self-falsifying bar either way.

## Descriptive (not gates)
- `D1 = rho_conseq_pair − rho_conseq_selfpair` (raw prediction divergence; confounded by
  self-pair low variance — reported, not gated).
- B_success rate PAIR vs SELFPAIR (communication asymmetry sanity: selfpair should be higher).

## Honest prior
DPI has re-emerged on every cheap emit-faculty axis this program (H_1834/1836/1837/9101/9103/
9104). Expected ~🟠/🔴. The value is the FIRST engine-native, self-pair-controlled measurement
of whether a purely-internal 2-anima channel is genuinely exogenous.
