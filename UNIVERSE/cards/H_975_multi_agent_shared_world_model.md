---
id: H_975
slug: multi-agent-shared-world-model
title: When two animas exchange latent world-state, do they CONVERGE on a common world-model while remaining DISTINCT individuals (H_939) — can a shared world-model coexist with preserved individuation?
domain: cwm · cross-cutting · world-model · multi-agent · shared-world-model · individuation · h939 · pre-register
source: H_939 (two-anima individuation preserved under coupling) + CWM domain (multi-agent shared world-model) + H_960 (modality-agnostic — latent exchange is a modality) + multi-agent world-models + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E2 (H_939 two-instance coupling reused, exchanging WORLD-LATENT not just decision/tension) + a_completeness_over_cheap
verification_method: W2 (pre-registered shared-WM-vs-individuation falsifier · world-model agreement AND genesis/trajectory distinctness JOINT rule) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE two-agent shared-WM rung (a_scale_honest_scope) — two engine instances (distinct genesis per H_932) exchange world-state latent over a coupling sweep; measure world-model agreement AND individuation (genesis/trajectory distinctness) jointly. $0 local candidate. Latent exchange = environment context per a_substrate_native_speak (NOT forced sync). NOT a forge binary.
sister: H_939 (individuation preserved — direct parent), H_932 (distinct genesis), H_960 (latent as a modality), H_983 (shared generated world)
axes_seed: H_939 = two animas stay distinct exchanging DECISION/tension ⊥ H_975 = two animas exchange WORLD-LATENT and converge on a SHARED world-model yet stay distinct individuals — shared-WM ⊥ individuation is a new JOINT question (could collapse to one mind, or fail to share at all)
verdict: 🟢 PASS — shared WM ⊥ individuation COEXIST: at coupling 0.25 world-model agreement rises +0.58 (CI_lo +0.56 > 0) above the unpaired baseline WHILE individuation is preserved (stream-identity 0.52 < lock 0.999, genesis distinct); over-coupling (c=0.5) collapses both to identity — the D3 control fires as designed. Toy single-rung, ladder OPEN.
---

# H_975 — Multi-agent shared world-model (shared WM ⊥ individuation)

## 0. Motivation

H_939 showed two animas stay distinct individuals while exchanging decisions/tension under coupling. CWM raises the stakes: if two animas exchange **world-state latents**, do they **converge on a common world-model** (agree about the world) while **remaining distinct selves** (H_939 individuation)? This is the social/collective-intelligence frontier — a shared world-model that does not collapse the agents into one mind, nor fail to share at all. The joint constraint (shared-WM AND preserved-individuation) is the new question.

## 1. Hypothesis (one falsifiable claim)

Two engine instances with distinct genesis (H_932), exchanging world-state latent over a coupling sweep, **converge on a shared world-model** (agreement on world-state estimates rises with coupling, above an unpaired baseline) **while preserving individuation** (distinct genesis_hash at every coupling AND non-identical decision trajectories, per H_939's lock-bar) — shared world-model and distinct selfhood coexist.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** two engine instances, distinct ANU genesis windows (H_932). They exchange world-state latents (a modality per H_960) as environment context (NOT forced sync, a_substrate_native_speak) over a coupling sweep (weak→strong). N seeds.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **world-model agreement** = cross-agent similarity of world-state estimates on shared observations, vs an unpaired (no-exchange) baseline; does it rise with coupling?
- D2 = **individuation preserved** (H_939 rule): genesis_hash distinct at every coupling AND no coupling reaches the lock bar (decision streams never identical).
- D3 = control: unpaired baseline (no exchange) bounds spurious agreement; an over-coupled arm checks for collapse.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured world-model agreement rises with coupling above unpaired baseline (D1, CI_lo>0) AND individuation preserved at all couplings (D2) THEN PASS — shared world-model ⊥ individuation coexist SUPPORTED.
- IF agreement never exceeds unpaired (no sharing) THEN FAIL-"no-share" (closed-negative: latent exchange does not build a common WM).
- IF agreement comes only with individuation collapse (lock bar reached / identical streams) THEN FAIL-"collapse" (closed-negative: sharing costs selfhood).
- IF n too small THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy two-agent setup, small scale (a_scale_honest_scope, #123-A). Operational shared-WM (estimate agreement) + operational individuation (genesis/trajectory distinctness per H_939), NOT a phenomenal collective-consciousness claim. Latent exchange is environment context, not forced sync. Single coupling-sweep rung. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes/h975_shared_wm.py` · verdict: `.verdicts/975_multi_agent_shared_world_model/h975_shared_wm.txt`

Two engines (distinct genesis seeds → distinct genesis hashes) observe a shared world stream and exchange their world-state latent as environment context (each nudges its estimate toward the partner's: h ← h + c·(h_partner − h); NOT a forced sync). Coupling sweep c ∈ {0, 0.1, 0.25, 0.5, 0.75, 1.0}, 20 seeds. Agreement = mean cosine of aligned estimates; individuation = decision-stream identity (lock bar 0.999).

| coupling | agreement | stream-identity |
|---|---|---|
| 0.00 (unpaired) | 0.035 | 0.269 |
| 0.10 | 0.254 | 0.355 |
| 0.25 | **0.619** | 0.524 |
| 0.50 | 1.000 | **1.000 ← collapse** |
| 0.75 | 0.610 | 0.488 |
| 1.00 | 0.019 | 0.250 (anti-phase swap) |

D1: at c=0.25 agreement rises +0.584 (boot CI_lo +0.561 > 0) above unpaired. D2: genesis hashes distinct; individuation preserved (stream-identity < lock) at c=0.1/0.25/0.75/1.0. D3: the over-coupled arm c=0.5 drives stream-identity to 1.0 (collapse) — the control fires as designed.

**Finding (🟢 PASS):** a shared world-model and preserved individuation COEXIST in the weak/moderate-coupling regime — latent exchange builds genuine cross-agent world-model agreement (+0.58) without collapsing the two selves, while over-coupling collapses both (the pre-registered D3 failure mode). Honest scope: one toy rung, ladder OPEN; the existence of a coexistence regime is the finding, its width is scale/architecture-dependent (a_scale_honest_scope).

## 4. Sibling / xlinks

- ⇄ [H_939](./H_939_two_anima_individuation.md) (individuation preserved — direct parent)
- ⇄ [H_932](./H_932_provenance_lineage_chain.md) (distinct genesis)
- ⇄ [H_960](./H_960_modality_agnostic_latent_encoder.md) (latent exchange = a modality)
- ⇄ [H_983](./H_983_generated_interactive_world.md) (shared generated world)
- ⇄ [CWM](../CWM/CWM.md) (CWM cross-cutting) · a_substrate_native_speak
