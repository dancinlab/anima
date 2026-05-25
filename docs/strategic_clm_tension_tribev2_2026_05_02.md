# CLM ↔ tension_link ↔ TRIBE v2 — mediator architecture analysis

Session: 2026-05-02 | Agent: strategic re-evaluation w/ Framing E (closed-loop) + Framing F (anima-cortex)
Scope: in-silico mediator bypass of #93 EEG user-obligate mediator; $0 analysis cycle.
Race-isolation: writes only to `state/strategic_clm_tension_tribev2_2026_05_02/*` and this doc.

## 1. 5 Framings comparison (rank order)

| rank | id | name | feedback | user mediator | wrapper LOC | $ | sci value |
|---|---|---|---|---|---|---|---|
| 1 | E | tension-mediated closed-loop NEW | yes | no | 100-200 | 0-5 | high |
| 2 | D | anima-tension_link-EEG + TRIBE BOLD anchor | partial | yes | <100 | 0-2 | highest |
| 3 | A | text-mediated open-loop (#95 baseline) | no | no | <50 | 0-2 | medium |
| 4 | C | G3 manifestation -> cortical region | no | no | <50 | 0 | very high |
| 5 | B | direct hidden-state injection | no | no | 200-500 | 0-5 | high (mismatch risk) |
| 6 | F | TRIBE v2 as anima-cortex (radical) | yes | no | 300-800 | 0-10 | speculative |

Framing E ranks #1 for current cycle because it uniquely answers the closed-loop question
(does BOLD feedback actually modulate CLM next step?) which Framings A/C/D cannot. Framing D
remains scientifically strongest overall but is user-time-bound; the two are complementary
sibling protocols.

## 2. Framing E recommendation verdict

PROCEED via staged sequence:
- Stage-1 (a): Framing A as $0-2 sanity gate (verify TRIBE v2 runs in env via cortexlab-toolkit)
- Stage-2 (c): Framing E full 100-step closed loop + R1/R2/R3 controls ($0-5, 2-3h ubu1 CPU)
- Stage-3 (b): #93 P1 + #95 Framing D 3-way bridge anchor ($0, user-time)

Hard pre-condition: random-control R1 (uniform 5ch) MANDATORY per §16.2 anchor. Without R1
a positive Framing E result is unpublishable.

## 3. EEG vs TRIBE v2 — significance one-liner

EEG (#93) answers "can anima mediate user cognition?" (biological ground truth, N=1, phenomenal
validity); TRIBE v2 (current) answers "does anima manifest brain-like dynamics?" (in-silico
replication, N=any, computational scalability) — sibling questions, NOT replacement.

## 4. Honest C3 (top 3)

1. TRIBE v2 = forward stimulus->BOLD encoder; closed-loop attractor at most evidences
   "computational coupling," NOT "brain-like consciousness." Substrate identity (Framing F H4)
   is out-of-scope speculation.
2. User mediator bypass = scalability gain BUT phenomenal validity loss. Framing E does NOT
   replace #93 H2; it addresses a sibling question. Both must run in parallel for triangulation.
3. 5d tension_link bottleneck (25.6:1 compression) + 10242 BOLD vertex -> 5 ROI feature reverse
   bottleneck makes H3 (no real coupling) the prior; pre-registered random-control R1 + F-CT-3
   are the falsifiers that gate any positive claim.

## 5. Final one-sentence

Framing E provides the missing computational closed-loop that #93 H2 (user-obligate mediator)
made impossible, but it complements rather than replaces the EEG bridge: run Stage-1 sanity
gate now, escalate to Stage-2 if TRIBE v2 runs cleanly, and reserve Stage-3 (real biology)
for triangulation — under §16.2 random-control R1 is the mandatory pass-or-publish-null gate.

## 6. Artifact map

- `state/strategic_clm_tension_tribev2_2026_05_02/architecture_5framings.json` — 5-framing matrix
- `state/strategic_clm_tension_tribev2_2026_05_02/framing_e_protocol.json` — 10-step closed-loop spec
- `state/strategic_clm_tension_tribev2_2026_05_02/hypotheses_h1_h4.json` — H1 convergence / H2 divergence / H3 no-coupling / H4 substrate (out-of-scope)
- `state/strategic_clm_tension_tribev2_2026_05_02/falsifiers_pre_register.json` — F-CT-1..F-CT-5 + R1/R2/R3 controls
- `state/strategic_clm_tension_tribev2_2026_05_02/eeg_vs_tribev2_comparison.json` — 10-axis matrix vs #93
- `state/strategic_clm_tension_tribev2_2026_05_02/risks_recommendations.json` — 6 risks + 6 honest C3 + 3-stage roadmap
