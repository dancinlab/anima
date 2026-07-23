<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_24 — localized C-slot readout: rules OUT "readout insensitivity" as the wall

**origin:** V6_23 concluded the whole-sentence byte-CE was too insensitive (margins ~0.01 nats)
and named the readout as the bottleneck. V6_24 TESTS that by scoring only the swapped-entity
bytes, conditioned on the shared prefix — a ~4× more sensitive readout. Reuses trained57.clm /
pedestal57.clm + v6_23_items (n=700/stratum), no new training/corpus. DIRECTIONAL.

## Readout
`v6_24_slot_score.py`: mean next-byte NLL of the C-slot bytes ALONE (via `decode._fwd_logits`,
the production trunk forward), instead of the whole-sentence mean. Real and distractor share
the identical prefix ending in A, so the C-slot NLL isolates "given this context, is the real
endpoint C or the distractor C′ more predictable" — composition, undiluted.

## RESULT — 🔴 the readout was NOT the wall; the DATA is (self-correcting V6_23)
Localized readout, trained57 / pedestal57 / collapse-Δ:

| stratum | trained | pedestal | collapse-Δ | margin(nats) |
|---|---|---|---|---|
| SEEN (pos-control) | 0.573 | 0.481 | +0.092 | 0.098 |
| BRIDGED | 0.504 | 0.453 | +0.051 | 0.048 |
| UNBRIDGED | 0.563 | 0.546 | +0.017 | 0.098 |

- **Sensitivity DID rise** — margins 0.098 nats vs V6_23's 0.008 (~12×). So the dilution was
  real; the readout change worked as intended.
- **But the verdict is UNCHANGED**: SEEN still 0.573 (<0.70), BRIDGED at **chance 0.504**,
  D = Δ_BRIDGED − Δ_UNBRIDGED = **+0.034 (z≈0.9, INCONCLUSIVE)**, BRIDGED still < UNBRIDGED.
- ⟹ **V6_23's "readout is the wall" was WRONG** (retracted, verdict-integrity). A 12× more
  sensitive readout finds the same nothing. The limiting factor is not how we read — it is that
  **the natural corpus barely installs even DIRECT binding** (SEEN lifts only +0.092 to 0.57),
  because natural co-occurrence is dominated by singletons (V6_13/14: 82% of entity pairs seen
  exactly once). If the model can't reliably bind a pair it saw directly, it certainly cannot
  compose one across a 2-hop bridge — and BRIDGED at chance confirms it.

## What this closes — the natural-bridge composition lane (V6_21→V6_24)
Three orthogonal escapes were tried and each ruled out its own hypothesis:
- V6_21: the signal was co-occurrence similarity, not composition → **DV fixed** (V6_22).
- V6_22/23: the clean DV needs more items + instrument margin → **corpus scaled 12×** (57MB) →
  supply recovered, instrument did not.
- V6_24: maybe the readout is too blunt → **readout sharpened 12×** → same nothing.
With DV, corpus-supply, and readout all eliminated as the cause, what remains is the **data
itself**: singleton-dominated natural co-occurrence installs binding too weakly to read, and
composition across bridges is absent. This CONVERGES with the standing prior — `g1-is-absence-
not-failure` (composition is a corpus-density property, not an engine deficit), `scale-is-
amplifier-not-lever` (V6_14: singleton rate barely improves with size). Natural emergence of
composition, on a clean on-standard DV at data scale with a sensitive readout, is **CLOSED**.

## Scope
$0 (reused ckpts + corpus + items). Single ckpt · single seed · ConvMoE byte-LM. DIRECTIONAL;
the closure is engine-native-measured but lab-DIRECTIONAL until ported. The one lever NOT tried
is repetition density itself (a natural corpus curated for repeated pairs, not more singletons)
— but that starts to hand-fit the corpus, which p9 forbids as faculty evidence. Track C (port
the V6 rotation crack to core/anima-py) remains the only open engine-native action.
