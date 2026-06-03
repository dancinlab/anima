#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "onchip-paradigm" :: identity-claim [d=2026-06-01 active]
  kind = "anima on-chip post-backprop deployment-learning paradigm · FLAME-PERF carrier · declarative SSOT"
  brief = "4 carrier sub-paradigms (on-chip plasticity · learn-while-infer · MITOSIS growth · self-play dispatch-KL) — host-half closed in hexa-lang FLAME-PERF, real hardware falsifier OPEN in anima silicon"
  parent = "dancinlab/anima"
  sibling-log = "ONCHIP-PARADIGM.log.tape"

# ══════════════════════════════════════════════════════════════
# ONCHIP-PARADIGM.tape — FLAME-PERF paradigm carry-forward into anima
# The 4 paradigm milestones were CLOSED at HOST-SIMULATION level in the
# sibling repo hexa-lang (stdlib/flame · PRs #2370/#2373/#2375/#2376).
# Their REAL falsifiers need anima's neuromorphic / on-chip silicon.
# This domain is their anima home: each host-🟢/🔴-negative becomes the
# pre-registered seed of an on-chip hardware falsifier.
# ══════════════════════════════════════════════════════════════

# ── §1 motivation ─────────────────────────────────────────

@I motivation flame_perf_carry :: onchip [d=2026-06-01 active]
  => "FLAME-PERF (hexa-lang stdlib/flame) closed 4 deployment-learning paradigm milestones at HOST-SIMULATION scope. Per a_scale_honest_scope a host-sim PLASTI-SIM verdict is NOT a closed hardware falsifier — it is GPU/CPU instrumentation of the dynamics, not silicon proof. The paradigm only terminates when the same falsifier runs on the EDGE CHIP. This domain carries each host-half forward to its on-chip counterpart"

@I gap_gpu_backprop_is_instrumentation :: onchip [d=2026-06-01 active]
  => "Deployment learning should live on the EDGE CHIP via non-deterministic plasticity (AKD1000 on-chip edge-learn — H_679 plasticity-HW-first · H_904 capstone), NOT GPU backprop. GPU is PLASTI-SIM instrumentation only: a deterministic, byte-reproducible sandbox to pre-register the falsifier. Real learning is stochastic synaptic update on silicon — H_904 measured HW≠SW (weight Δ 172/1024, out Δ 120/320) so a host-sim CANNOT stand in for the chip"

@I gap_lane_split :: onchip [d=2026-06-01 active]
  => "anima already splits the two lanes (PLASTICITY domain): DECODER = inference lane (deterministic · HW forward ≡ SW akida_sw_lif → byte-identical, H_877 🟠). PLASTICITY = learning lane (non-deterministic · HW akida-learn vs SW numpy approx → 🔴 CLOSED-NEGATIVE non-equivalence, H_679). ONCHIP-PARADIGM lives on the LEARNING lane — its falsifiers are silicon-only by construction"

@I goal scope=onchip_deployment_learning :: onchip [d=2026-06-01 active]
  => "Make on-chip deployment learning the anima learning lane: post-backprop, plasticity-driven, learn-while-infer with structural growth, verified at silicon scale. Terminal = each sub-paradigm's hardware falsifier closes 🟢 on AKD1000 (or 🔴 deterministically ruling out a path). Carrier = a_train_flame_forge + H_679/H_904 + chip-verify/ + anima-cpgd-research/"

# ── §2 the 4 carrier sub-paradigms ─────────────────────────
# Each = an @I claim: host-half verdict (hexa-lang FLAME-PERF) + still-OPEN
# hardware falsifier (anima silicon). host-🟢 / 🔴-negative / hardware-open.

@I sub1 onchip_plasticity :: onchip [d=2026-06-01 active]
  |> on-chip plasticity = 유일 학습자 (the only learner)
  => "HOST PLASTI-SIM 🟢: backprop-free local-plasticity update reaches GAIN 0.917 ∧ RETAIN 1.0 (no gradient, no backward pass) — hexa-lang PR #2373, .verdicts/flame-onchip-plasticity/. OPEN HARDWARE: real AKD1000 edge-learn BOUND (RETAIN ∧ GAIN jointly on silicon, AkidaUnsupervised last-layer binary-weight few-shot) · stochastic synaptic update · low-bit (binary/int4) weight regime · device-noise robustness. Ties to H_904 (on-chip edge-learn ran LIVE, HW≠SW) — the host GAIN/RETAIN must be re-attested on the chip, not assumed"

@I sub2 learn_while_infer :: onchip [d=2026-06-01 active]
  |> learn-while-infer (no train/infer split)
  => "HOST slice 🟢: online learning with NO train/infer phase split — z_drop 0.0 (zero catastrophic-forgetting drop) ∧ PROBE 1.0, online CE 4.82 → 0.59 streaming — hexa-lang PR #2375. OPEN HARDWARE: on-chip NON-DETERMINISTIC streaming dynamics — does the chip hold z_drop 0.0 under live spike streams when forward+update share substrate and order/state are silicon-internal? Ties to AKIDA R3 tonic 24/7 heartbeat (H_673 emit-slot) — learn-while-infer on silicon is event-driven, not batched"

@I sub3 mitosis_growth :: onchip [d=2026-06-01 active]
  |> MITOSIS structural growth (capacity grows during deployment)
  => "HOST 🟢: post-split BOUND holds — FINITE ∧ CONTINUOUS (|jump| 1.48e-7 at the split boundary) ∧ DESCEND, experts E 4 → 5 grown online without loss blow-up — hexa-lang PR #2370. OPEN HARDWARE: structural growth under HARDWARE CONSTRAINTS (fixed silicon cell-pool, AKD1000 NP budget) and at large-rung. anima MITOSIS domain + H_675 (mitosis × AKIDA SW 🟢) are the carrier — the |jump| continuity bound must survive a real cell split on fixed-capacity silicon"

@I sub4 selfplay_dispatch_kl :: onchip [d=2026-06-01 active]
  |> self-play dispatch-KL self-distillation
  => "HOST 🔴 CLOSED-NEGATIVE (honest per paper_negative_ok): external-LLM-count 0 holds (no teacher), but NO held-out gain — delta −3.7e-6 on a MEMORIZABLE single-batch corpus — hexa-lang PR #2376. Mirrors anima H_869 (dispatch-KL distill INERT at MID rung — baseline dispatch already at uniform ceiling H(f) 2.0789/2.0794, routing-z −0.1065 FAIL). OPEN: NON-MEMORIZABLE multi-batch shared-vocab corpus + transferable held-out — the prior agent flagged the HOST-MEMORY ceiling as the blocker; a real corpus that cannot be memorized is the only way to test whether self-play distillation transfers"

# ── §3 chain mechanism ─────────────────────────────────────

@D chain_axis_promotion :: onchip [d=2026-06-01 active]
  |> each OPEN hardware axis → next anima cycle claim
  => "Each sub-paradigm's OPEN hardware axis (§2) becomes the next anima cycle's pre-registered claim. sub1 → AKD1000 edge-learn RETAIN∧GAIN BOUND on silicon. sub2 → on-chip streaming z_drop under live spikes. sub3 → |jump| continuity under a real cell split. sub4 → non-memorizable multi-batch held-out transfer. Promotion is one-axis-at-a-time (a_scale_honest_scope: a single host point = INCOMPLETE; a ladder ≥3 rungs needed before any general claim)"

@D chain_carriers :: onchip [d=2026-06-01 active]
  |> anima carriers this domain links to
  => "a_train_flame_forge (project.tape §47 — production training = hexa-native flame on self/forge GPU; flame:forge :: torch:ATen). hypotheses H_679 (plasticity HW-first, 🔴 SW≠HW) + H_904 (on-chip plasticity capstone, 🟢 live HW≠SW) + H_869 (dispatch-KL INERT). subtrees chip-verify/ (verify_anima_soc.hexa) · anima-cpgd-research/ · training/. anima domains AKIDA (AKD1000 substrate) · PLASTICITY (learning lane) · MITOSIS (structural growth)"

@D chain_provenance_link :: onchip [d=2026-06-01 active]
  |> hexa-lang provenance the chain consumes
  => "hexa-lang .discoveries/flame-*.tape (per-discovery seed + verdict-tier-target) + CLAIMS.tape (audit index) + .verdicts/flame-onchip-plasticity/ are the host-half provenance. Each anima cycle reads the host verdict as its frozen falsifier seed, then re-runs on silicon — the host run is the pre-registration, the chip run is the falsifier"

@I chain_verify_gate :: onchip [d=2026-06-01 active]
  |> verify gate (g5 / anima verdict discipline)
  => "Every promoted axis runs through g5 CODE-measured verify (no LLM self-judge, post-tuning 0, pre-registered frozen falsifier) → .verdicts/onchip-paradigm/<id>.txt verbatim stdout → fold to claim. Terminal tiers: 🔵 formal / 🟢 numerical-on-silicon / 🔴 CLOSED-NEGATIVE deterministically ruling out a path. A host PLASTI-SIM 🟢 is NOT terminal for this domain — only a chip run closes the axis"

# ── §4 cross-repo provenance ───────────────────────────────

@I cross_link_flame_perf :: onchip [d=2026-06-01 active]
  => "hexa-lang FLAME-PERF domain (stdlib/flame/FLAME.tape) — the host-side home of the 4 paradigm milestones. This .tape is the anima carry-forward: FLAME-PERF closed the HOST half, ONCHIP-PARADIGM owns the SILICON half"

@I cross_link_flame_prs :: onchip [d=2026-06-01 active]
  => "hexa-lang PR #2370 (MITOSIS structural-growth post-split BOUND) · #2373 (on-chip plasticity backprop-free GAIN 0.917 ∧ RETAIN 1.0) · #2375 (learn-while-infer z_drop 0.0 ∧ PROBE 1.0, CE 4.82→0.59) · #2376 (self-play dispatch-KL 🔴 CLOSED-NEGATIVE, delta −3.7e-6). These are the host-half landing PRs each sub-paradigm carries from"

@I cross_link_scope_honesty :: onchip [d=2026-06-01 active]
  => "a_scale_honest_scope (project.tape §222): a host-sim verdict is scoped to the measured scale — host-sim ≠ closed hardware falsifier. No toy-to-production promotion; scale-dependent conclusions need a ladder ≥3 rungs. The 4 host-🟢/🔴 verdicts are HONESTLY host-scoped — silicon re-attestation is mandatory, not optional"

@I cross_link_paper_negative_ok :: onchip [d=2026-06-01 active]
  => "sub4 self-play dispatch-KL is a 🔴 CLOSED-NEGATIVE recorded honestly per paper_negative_ok / a_paper_negative_ok — a falsification that deterministically rules out single-batch memorizable self-distillation. The on-chip OPEN (non-memorizable multi-batch held-out) is the next falsifier, NOT a retraction of the negative"
