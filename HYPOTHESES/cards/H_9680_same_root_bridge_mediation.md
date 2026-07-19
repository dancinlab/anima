---
id: H_9680
title: SAME-ROOT mediation — does the store-bridge mediate BOTH lanes? (bridge × study DiD)
tier: PROPOSED (DIRECTIONAL design · lab-full · GPU cost-gated · NOT a verdict)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9680 (R4) — 두 lane 공통뿌리 매개 검정

**Origin.** `sidecar lab full` 2026-07-17 — **Sol §3**. DESIGN ONLY · DIRECTIONAL.

**Claim (one line).** If Lane A (G1 recombination) and Lane B (H_9520 exogenous content)
share **one root**, then on a **co-trained store-bridge** substrate **CONTENT recovers
selectively while the generic FORM effect barely moves**.

## Mechanism — this is the discriminator between the two readings
- **One root**: bridge presence mediates *both* phenomena together.
- **Coincidence (two mechanisms)**: H_9520's generic `ρ·form` is **independent** of the bridge.

Grounded in: H_9329 (operator does not runtime-query the declarative store) +
H_9423 (co-trained store-bridge **learns** held-out 0-shot lookup · toy · DIRECTIONAL).

## Minimal decisive experiment — factorial `bridge∈{cotrain, sham} × study∈{MAIN,C2}`
```bash
anima-py corpus storebind ... --out bridge_cotrain_s${S}.txt
anima-py train --init py303_full.clm --corpus bridge_cotrain_s${S}.txt --canon --seed ${S}
anima-py train --init BRIDGED_s${S}.clm --corpus study_main_s${S}.txt --canon --seed ${S}
anima-py evaluate POST_s${S}.clm --probe teacher_heldout_probe.json --gen 40
anima-py evaluate POST_s${S}.clm --rho-axon
```

## Frozen falsifier (difference-in-differences)
- `[(MAIN−C2)_bridge − (MAIN−C2)_sham] ≥ +0.15`, content-probe paired 95% CI lower `> 0`
- **simultaneously** the `ρ·form` bridge interaction must be `|Δ| ≤ 0.10`
- bridge raising only generic form, or failing to raise the content probe ⟹ **weakens the
  common-root explanation**.

## Controls (≥2)
① sham cotrain (same bytes·steps · store/value derangement) ② H_9423 BOLT frozen-trunk
control ③ C2 grammatical-fact-swap ④ C1 replay-only.

## Cost · kill-list
recipe + leak audit **$0**; 303M bridge co-train + CPT = **GPU, expensive (owner go)**.
Kill-list: **not** a re-invention of H_9423 — this is a **303M cross-lane mediation test**.
⚠️ Self-flag: if it only measures "does the bridge work again", it IS re-invention → discard.

## Ordering dependency
Runs **after** [[H_9678]] revives the content instrument, and is order-dependent on
H_9423's `W_q` address-bootstrap NEXT (firing before that = predicted failure).
