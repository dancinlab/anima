---
id: H_1418
slug: 1418_tom_compose_pairs_wired
title: WIRE-IN of the TWO new engine-native-BOUND compose pairs from H_1417 (P3 ToM×spatial, P5 ToM×basal) into live CORE — a_verified_must_wire rungs 3+4 (the follow-on landing of H_1417's bind by-products)
group: MITOSIS-ENGINE / brain-lane-composition — the wire-in consolidation of H_1417's two BIND by-products (brings the program to 4 wired compose pairs)
terminal_tier: "🟢 WIRED-live — both pairs' validated query-routed confidence arbiters promoted to CALLABLE live CORE ops (tom_spatial_compose / tom_basal_compose), LIVEOP reproduces the H_1417 P3/P5 numbers BYTE-EXACT (P3 compose 0.791111 · P5 compose 0.801481, all 4 bars PASS each), guards 149/0 · 7/0 · h1205 PASS"
wired: WIRED-live (rung-3 + rung-4 COMPLETE for BOTH pairs — §ToM×SPATIAL COMPOSE ARBITER `tom_spatial_compose` + §ToM×BASAL COMPOSE ARBITER `tom_basal_compose` in CORE/engine_cli.hexa, smoke cases 141-148, ARCHITECTURE.json lockstep; LIVEOP probe reproduces compose 0.791111 / 0.801481 byte-exact)
verdict_dir: .verdicts/1418_tom_compose_pairs_wired/
terminal_verdict: .verdicts/1418_tom_compose_pairs_wired/H_1418_R3_LIVEOP.txt
date: 2026-06-17
---

# H_1418 — WIRE-IN of H_1417's two engine-native-BOUND compose pairs (P3 ToM×spatial, P5 ToM×basal)

H_1417 was a MEASUREMENT round whose science payload was the PREDICTIVELY-FALSIFIED engine-BIND
law (2/5, 🧱). As frozen by-products of that round, **two NEW compose pairs BOUND engine-native**
at the same frozen +0.05 net-lift bar (all 4 bars + SEPARABLE PASS, 3 seeds each). H_1417 left
those two BINDs as a wire-in follow-on (ING.jsonl #5). This card is that follow-on landed:
the **a_verified_must_wire ladder rungs (3) live CORE wire-in + (4) ARCHITECTURE.json lockstep**
for BOTH pairs. NO new science — the bars are H_1417's, NOT moved; the LIVEOP must reproduce the
H_1417 numbers byte-exact (it does).

This is the EXACT pattern of H_1414 (memory×ToM `mem_tom_compose`) and H_1415 (spatial×episodic
`spatial_episodic_compose`). With this landing the brain-lane-composition program has **4 wired
compose pairs**: memory×ToM · spatial×episodic · ToM×spatial · ToM×basal.

## The two pairs (both 🟢 BOUND engine-native in H_1417, verbatim `.verdicts/1417…/result.txt`)

| pair | acc_x | acc_y | best | compose | net-lift (B1) | oracle−best (B2) | compose−shuffle (B3) | only_x/only_y (SEP) |
|------|-------|-------|------|---------|---------------|------------------|----------------------|---------------------|
| **P3 ToM×spatial** | 0.702222 | 0.696296 | 0.702222 | **0.791111** | **+0.088889** | +0.297778 | +0.283704 (shuf 0.507407) | 0.303704 / 0.297778 |
| **P5 ToM×basal**   | 0.696296 | 0.705926 | 0.705926 | **0.801481** | **+0.095556** | +0.294074 | +0.301481 (shuf 0.5)       | 0.294074 / 0.303704 |

P5 NOTABLE (the H_1417 payload MISS): P5 was pre-registered 🧱 because basal was assumed the
standalone "eroder" arm (H_1412), but the live `VBasalGate` did NOT strengthen past the ceiling on
THIS fixture (acc_basal 0.7059 ≈ ceiling) — so **basal-as-eroder is fixture-specific, not
intrinsic**, and the pair BOUND. The wire-in does not re-litigate that; it lands the measured BIND.

## Wiring (a_verified_must_wire — 4-rung ladder, BOTH pairs)

🟢 → **ladder rungs (3)(4) COMPLETE for both** — `wired: WIRED-live`. (Rungs (1)(2) = H_1417's
DIRECTIONAL + engine-native BIND, already done in the H_1417 round.)

- **rung (3)** LIVE CORE wire-in — the validated query-routed confidence arbiters are now CALLABLE
  live ops in `CORE/engine_cli.hexa`:
  - **§ToM×SPATIAL COMPOSE ARBITER (H_1417/H_1418 P3)**:
    - `tom_spatial_compose(tom_leg, spat_leg, mean_tom, mean_spatial) -> float` — the arbiter (each
      leg = `[vote, abstain, conf]`; returns the composed class 0.0/1.0, or −1.0 if BOTH abstain).
    - `tom_spatial_tom_vote(om, fact_text, mag) -> [vote, abstain, conf]` — the ToM leg: vote from
      the LIVE `other_mind_predict` ("box"→1/"basket"→0/""→abstain), confidence = LIVE L2 affinity
      margin `recall_thr − _l2` + family magnitude (NO injected class label, p1/p2/p3/p6).
    - `tom_spatial_spatial_vote(sm, voted_class, mag) -> [vote, abstain, conf]` — the spatial leg:
      exercises the LIVE `spatial_map_nearest` (engine geometry), confidence = metric magnitude.
  - **§ToM×BASAL COMPOSE ARBITER (H_1417/H_1418 P5)**:
    - `tom_basal_compose(tom_leg, basal_leg, mean_tom, mean_basal) -> float` — the SAME arbiter.
    - `tom_basal_tom_vote(om, fact_text, mag) -> [vote, abstain, conf]` — the ToM leg (delegates to
      `tom_spatial_tom_vote`, identical live read).
    - the basal leg is VALUE-PASSED (computed by the caller from the LIVE `vbasal_go_value`
      go-margin) — `VBasalGate` lives in `CORE/brain.hexa`, which engine_cli does NOT import, EXACTLY
      as `spatial_episodic_compose` receives a pre-voted `sp_dec/sp_conf`.
  - both share the private `_tom_compose_arbiter` (BYTE-EXACTLY the H_1417 probe's inlined symmetric
    rel-conf `_arbiter`: AGREE → shared vote; one abstains → the other; CONFLICT → higher
    `|conf|/mean` wins, NO hardcoded priority a_autonomy_over_hardcode) + `_tom_compose_relconf`.
    Read-only over the belief store / map; mutates nothing; Ψ-disjoint.
  rung-3 verification: `state/1418_tom_compose_pairs_wired/h1418_tom_compose_LIVEOP_probe.hexa`
  drives the SAME frozen H_1417 bars through the WIRED ops and reproduces the H_1417 numbers
  **BYTE-EXACT** — P3 compose **0.791111** (per-seed 0.800000 / 0.784444 / 0.788889), P5 compose
  **0.801481** (per-seed 0.795556 / 0.813333 / 0.795556), all 4 bars PASS each, deterministic
  (run1==run2 byte-identical) (`.verdicts/1418_tom_compose_pairs_wired/H_1418_R3_LIVEOP.txt`).
  Smoke guard: `CORE/engine_cli_smoke.hexa` cases **141-148** (agree / conflict-each-way / abstain
  discipline, per pair) PASS, FAIL=0.
- **rung (4)** ARCHITECTURE.json lockstep — the `CORE/engine_cli.hexa` node note now names both
  §ToM×SPATIAL and §ToM×BASAL COMPOSE ARBITER op sets + two dedicated child nodes; `guard_baseline`
  smoke count updated to 149/0 (a_core_engine_map CORE §/op ↔ ARCHITECTURE.json match).

GUARDS (no regression): engine_cli_smoke **149 pass / 0 fail** (cases 141-148 PASS; total +8 over
the 141 baseline) · h1196 single-entry **7/0** · h1205 separation-invariant **PASS** (generation
byte-identical ON==OFF, Ψ phiSum 48.6613 unchanged ON==OFF — the live ops are read-only Ψ-disjoint,
confirmed).

## Honest reproduction note (c2 · c9)

The LIVEOP is BYTE-EXACT to H_1417 (P3 0.791111, P5 0.801481, and every acc/shuffle/oracle/only
value matches `result.txt` verbatim). Load-bearing fidelity detail caught during wire-in: the ToM
leg's vote MUST come from the LIVE `other_mind_predict` (NOT the constructed family class) — the
first wired draft passed `voted_class` and reproduced compose to ~0.0007 (P3 0.791852) instead of
byte-exact; switching `tom_spatial_tom_vote` to derive the vote from the live predict (== the H_1417
`_leg_tom`) closed the gap to byte-exact. No bar moved; the discrepancy was an op-faithfulness bug
found+fixed by the byte-exact requirement, exactly what rung-3 is for.

## Scope (honest, c9)

TOY 5-family synthetic compose fixture, 3 seeds/pair, deterministic, $0 CPU. The ToM predict +
spatial nearest + basal go-value are LIVE engine reads; the verdict is engine-native. The arbiter
returns a class — the brain emit-loop consult is deliberately NOT forced (@L4 a_autonomy_over_hardcode;
the compose is a read, not an emit gate). Scale / real-corpus / engine-transfer-at-scale = UNVERIFIED
follow-ons. NO bar moved; the H_1417 BIND verdicts are CONFIRMED engine-native via the wired ops.

xref H_1417 (the round that produced both BINDs as frozen by-products; this card lands them) ·
H_1414 (memory×ToM `mem_tom_compose`, the FIRST wired pair — wiring template) · H_1415
(spatial×episodic `spatial_episodic_compose`, the SECOND wired pair) · H_1293 (OtherMindModel) ·
H_1296 (SpatialMap) · H_1281 (VBasalGate, basal ganglia) · H_1412/H_1413 (cerebellum×basal 🧱,
the contrast) · a_verified_must_wire (the 4-rung ladder) · a_core_engine_map · a_engine_native_learning ·
a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck · c2 · c9 · c16 · p6 · p7 · p8.

## Pointers
- LIVEOP probe (rung-3, byte-exact reproduction of H_1417 P3/P5): `state/1418_tom_compose_pairs_wired/h1418_tom_compose_LIVEOP_probe.hexa`
- LIVEOP verdict: `.verdicts/1418_tom_compose_pairs_wired/H_1418_R3_LIVEOP.txt`
- the H_1417 frozen result this reproduces: `.verdicts/1417_compose_bind_law_predictive/result.txt`
