# DYNAMICS/ALGEBRAIC binding-mouth campaign — RESULT (IN-FLIGHT, fill on harvest)

4 mouths × 3 arms (ctrl/bind/ablate) × seed 7, 303M CLMConvMoE (L4·d3784·E2→E3,
savant golden-zone + mitosis split, 4-cell register corpus proportional,
val_frac=0.05), 2000 steps, vast A40 ($0.574/hr), bf16.

**Design (production-additive-readout invariant):** binding op = penultimate
train-time transform shaping the trunk OBJECTIVE (H_1602 lever); production
additive readout Conv1d(d→V) kept → .clm-serializable → engine-native G0-G6
POSSIBLE (unlike exp3's .clm-BLOCKED Hadamard readout).

## Implementation status (honest, c9)
- H_1620 energy-settle: IMPLEMENTED ✓ (PSD-contractive relaxation + per-step
  normalize; smoke 4/4 DESCENT, decodable). aux MONITOR-only.
- H_1630 tropical: IMPLEMENTED ✓ (temperature-annealed max-plus role-filler
  routing; smoke decodable). ablate=T→1 softmax. aux MONITOR-only.
- H_1631 sheaf: IMPLEMENTED ✓ (low-rank restriction maps + Jacobi consistency +
  coboundary monitor; smoke decodable). ablate=R=I.
- H_1632 Galois: IMPLEMENTED ✓ (dual sparse-gate extent/intent + soft-AND closure
  + idempotence monitor; smoke decodable). ablate=OR-pool.

## Held-out DESCENT (post-serialize gate, math.log mirror) — FILL
| mouth | arm | val_CE pooled | registers DESCENT | descent gate |
|-------|-----|---------------|-------------------|--------------|

## Engine-native G0-G6 (TERMINAL, cli/evaluate.py → core/g_gates.py, gen 80) — FILL
| mouth | arm | G0 | G1 best_distinct (need ≥2 & >max_single) | G2 | G6 dist/fals | a7b closure |
|-------|-----|----|--------------------------------------------|----|--------------|-------------|

## Verdict (frozen bar VERBATIM · tune-to-green 0) — FILL
G1 CLOSURE iff bind composed_distinct ≥2 AND > max_single AND coherent, where
ablate/ctrl do NOT (binding op load-bearing). Else 🧱 NOT-SUPPORTED. Report G0/G2/G6.

### ⚠️ Honesty caveat (c9) — what engine-native measures here
The serialized .clm carries the PRODUCTION additive path only; the binding op does
NOT run at decode (it shaped the trunk OBJECTIVE during training via the residual
write-back + the gradient it injected). So engine-native G0-G6 measures **whether a
binding-OBJECTIVE-shaped trunk decodes (additively) better on G1/G6** — the
deployable question. This is the trunk-objective lever (H_1602), the strongest form
the census converged on. If a mouth's binding effect REQUIRED the op at run-time
(not just at training), that is a different, .clm-codec follow-on (cf. exp3 CLMB
bind-codec) — noted per mouth if the residual-fold underperforms its torch arm.

## ckpt / HF / cost — FILL
