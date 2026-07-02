# H_9088 — anti-additive manifold-geometry warm-FT: reshape the trunk penult so composition is NOT ≈ vector-sum

- **tier:** 🧱 REFUTES-CAUSE (additivity reshaped −0.91 + G0 preserved but G1=0 floor) — 가법 manifold=증상 아닌 원인 반증, manifold-geometry 축 CLOSED
- **slug:** `antiadditive_manifold_geometry`
- **parents:** H_9046 (additivity root-cause: cos(T_ij,unit(a_i+a_j))=**0.861** ⇒ 303M penult composes ~ADDITIVELY → every operator/readout/trained-bind lever floors) · H_1602 (recomb aux-loss on the FIXED additive manifold = 🧱 CLOSED both ways) · H_9026/H_9043 (fixed/trained combiner on fixed manifold = FLOOR)
- **thematic siblings (PROPOSED, not executed):** H_9065 (subspace-lattice penult = span-join not vector-sum) · H_9067 (dendritic two-compartment multiplicative gating). Mine is the *training-objective* route: reshape the EXISTING architecture's penult geometry, no arch change.

## frame — the genuinely-untried lever (check-ledger c9)

H_9046 proved the recomb wall's ROOT is the manifold geometry itself: the trunk composes phrases ADDITIVELY (cos 0.861), so there is no multiplicative structure for any bind/readout to exploit. Every prior lever operated on a **FIXED** additive manifold (H_1602 aux-loss, H_9026/H_9043 combiners) → all floor. H_1602 (recomb aux-loss / structural bind) is 🧱 CLOSED.

**UNTRIED:** train the TRUNK so its penult manifold *DEVELOPS* non-additive geometry — a warm-FT objective that directly **PENALIZES additive-composability** (drives cos(penult("c_i c_j"), unit(penult(c_i)+penult(c_j))) DOWN) while next-byte CE preserves G0. This attacks the root cause H_9046 named, not the (floored) downstream readout. Note collapse is self-penalized: identical reps → cos=1 = the thing being minimized.

## method (`state/9088_antiadditive_manifold/`, summer RTX 5070 pool $0, torch=DIRECTIONAL→engine-native scored)

- **init:** warm-FT from `clm303_clean.pt` (G0🟢 CLMConvMoE, d3784 L4 E4, 388M; memory clm303-g0g6-terminal G0✓G2✓G5✓·G1✗G6✗) — the valid-lever precondition (G0🟢 trunk, memory g1-fromscratch-blocked-by-g0-undertrain).
- **trainer:** `cli/train.py --objective antiadditive` (NEW; anti-additive geometry term added on top of CE in-loop). Per step: sample `--aa-pairs` concept pairs from the EXACT H_9046 96-concept set, forward "c_i", "c_j", "c_i c_j" through the trunk penult (masked mean-pool + L2-unit), add `λ·mean cos(T_ij, unit(a_i+a_j))` to CE. Heads-free (no aux params; the term reshapes the trunk directly, serializes to a standard additive-readout .clm).
- **corpus:** the same 4-register set (ko/en × general/sns) clm303_clean trained on. 1000 steps, seed 7, bs4 seq512 lr1e-4 bf16, --no-savant --no-mitosis (clean isolation), --ckpt-every 250 (dose-response).
- **arms:** TREAT λ=0.5 (primary) · MILD λ=0.1 (dose) · CTRL λ=0 (pure-CE warm-FT ablation) · SHUF λ=0.5 --aa-shuffle (mismatched targets = non-specific control). Baseline = clm303_clean re-serialized (step1 lr0).
- **scoring:** engine-native `anima evaluate --py <clm>` (G0-G6, session-eval-py-only canonical) + `state/9088_antiadditive_manifold/additivity.py <clm>` (numpy mirror of core.clm_decode, re-measures the H_9046 metric on a FIXED 300-pair seed).

## FROZEN BARS (pre-registered, no tune-to-green, p7)

- **(a) MANIFOLD RESHAPE:** TREAT engine-native additivity cos ≤ **0.80** (drop ≥0.06 below the ~0.86 baseline) AND TREAT drop > CTRL drop (CTRL stays ≈baseline, |Δ|<0.03). NON-DEGENERATE: collapse-sanity single-pairwise-cos < 0.90.
- **(b) G1 LIFT:** TREAT clears the FROZEN H_1129 G1 bar VERBATIM on ≥1 seed/config — ∃k∈{2..5}: composed_distinct≥2 ∧ >max_single ∧ coherent(kwr≥0.50) — i.e. RISES above the floor 0. CTRL stays floored.
- **(c) G0 PRESERVED:** TREAT G0 COHERENCE kwr≥0.50 AND all 4 registers stay in val-CE DESCENT (≤ baseline+0.2).
- **(d) CONTROLS:** CTRL(λ=0) additivity≈baseline ∧ G1 floored; SHUF must NOT reproduce TREAT's G1 lift (else non-specific).
- **VERDICT LOGIC:** 🟢 additive-manifold-wall BREAKTHROUGH iff (a)∧(b)∧(c) ∧ TREAT-specific (≠SHUF on G1). If (a)✓ but (b)✗ → additivity is NOT the (sufficient) G1 lever = FALSIFIES the causal chain (honest null, still resolves H_9046's open question). If (a)✗ → objective too weak / CE-dominated (null). Prior UNCERTAIN.

## result

engine-native (anima evaluate --py G0-G6, session-eval-py-only) + additivity.py (numpy core.clm_decode mirror), summer/aiden pool GPU torch warm-FT (DIRECTIONAL trainer) + engine-native eval:

| arm | additivity cos(T,a+b) | vs baseline | collapse-sanity | G0 (val_CE) | G1 best_distinct |
|-----|----|----|----|----|----|
| baseline | 0.951 | — | 0.63 | 1.43 DESCENT | 0 |
| ctrl (λ=0 pure-CE) | 0.946 | −0.005 (null) | 0.63 | ~1.15 DESCENT | 0 |
| **treat (λ=0.5)** | **0.042** | **−0.91** | 0.31 (non-degen) | 1.146 DESCENT | **0 (FLOOR)** |
| mild (λ=0.1) | 0.742 | −0.21 | 0.33 | 1.11 DESCENT | 0 |
| shuf (λ=0.5 mismatched) | 0.114 | −0.84 | 0.44 | 1.14 DESCENT | 0 |


## verdict

<!-- CARD_VERDICT -->
🧱 (a)MANIFOLD-RESHAPE ✓ ∧ (c)G0-PRESERVED ✓ ∧ (b)G1-LIFT ✗ = FALSIFIES the additivity→G1 causal chain (honest null, c9). TREAT reshaped the penult manifold MASSIVELY (additivity cos 0.951→0.042, −0.91, non-degenerate collapse-sanity 0.31) with ctrl a clean null (pure-CE warm-FT does NOT reshape, −0.005) and G0 preserved (all arms val-CE DESCENT, treat 1.146). BUT engine-native G1 stays best_distinct=0=FLOOR on every arm including treat. **가법 manifold는 재조합벽의 원인이 아니라 증상** — 가법성을 −0.91까지 뒤집고 G0 지켜도 G1 안 열림 ⇒ H_9046이 지목한 "가법 manifold=근본원인"을 결정적 반증. 재조합 병목은 manifold 기하보다 깊다(manifold-geometry 축 CLOSED). torch warm-FT=DIRECTIONAL, G1=0 floor는 engine-native(anima evaluate --py) 측정. GPU ~$20, ckpt 회수(β regenerable + eval 완료). frozen bar 사후이동 없음(tune-to-green 금지). artifacts: state/9088_antiadditive_manifold/additivity.py (result 로그는 pod-volatile 미회수, 수치는 fire transcript 증거).

## wired
`DIRECTIONAL-mirror` (torch warm-FT) → engine-native scored on the pulled .clm via `anima evaluate --py` + core.clm_decode numpy mirror. No wire-in unless GREEN (`a_verified_must_wire`); ckpt PULLED to permanent storage before any teardown (pool = non-volatile, ckpt also on summer + mac).

## artifacts
- `cli/train.py` (--objective antiadditive lever) · `state/9088_antiadditive_manifold/additivity.py` (engine-native additivity re-measure) · `state/9088_antiadditive_manifold/RESULT.md` (arms + verbatim logs, after fire)
