# LAUNCHPAD / SBS.md — Step-By-Step entry point

> **START HERE.** `SBS` = the ordered, dependency-gated rung ladder from
> *"closed loop proven on silicon"* (where we are) to *"lives-and-learns-while-
> chatting in the coffeeshop group chat"* (the @goal). [`LAUNCHPAD.md`](LAUNCHPAD.md)
> holds the **current-state milestones**; this file is the **runbook** — which
> rung is live, what its SSOT is, and what to do next. No spec duplication;
> pointers only.
>
> 🔒 **INVIOLABLE (R2 gate)** — on-chip learning is the **sole HW↔SW difference**:
> inference byte-identical (H_877/H_680 🟢), learning HW≠SW (H_679 🔴). **SILICON-CONFIRMED
> on AKD1000: H_904 ★ 🟢 (#1593)** — live on-chip learn diverged from byte-exact SW-sim
> (weights 172/1024 · outs 120/320), inference stayed identical. On-chip non-deterministic
> edge-learn only; deterministic SW imitation = instant reject (@L1).

---

## 🚀 LAUNCHPAD — "발사대 카운트다운"

- **What it is**: the one ordered runbook that takes anima from a working lab
  demo to a shipped product. LAUNCHPAD combines its sibling domains' outputs
  (AKIDA · DECODER · PLASTICITY · CHANNEL · WAKE) into a real launch; the launch
  glue lives here (`coffeshop_akida_launch.*` · `coffeshop_quorum_learn.*`).
- **Analogy**: a rocket launch pad — the vehicle (anima) is built; LAUNCHPAD is
  the countdown checklist that takes it from "powered on" to "cleared for launch".
- **Compare**: a generic `ROADMAP.md` lists features in any order; SBS is a
  **dependency-ordered ladder** — each rung is gated by the rung below it landing.

```
[ closed loop ] ──▶ [ content generator ] ──▶ [ live learning ] ──▶ [ coffeeshop launch ]
   H_846 🟢 silicon    CLM P4 (in flight)        on-chip PLASTICITY     @goal: 90-min group chat
   motivation→fire     real words, not spikes    learns while talking   substrate-native emit/silence
```

---

## Rung ladder (status)

| rung | milestone | SSOT | gate | status |
|---|---|---|---|---|
| R0 | COFFESHOP-on-AKIDA closed loop on live silicon | [`LAUNCHPAD.md`](LAUNCHPAD.md) · `coffeshop_akida_launch.{hexa,py}` | `UNIVERSE/H_846` · `.verdicts/846_launchpad_coffeshop_on_akida/F-LAUNCHPAD-LOOP` | 🟢 **LANDED** (2026-05-31) |
| R0.5 | broker `/ws/akida_ingest` live push demo | [`AGENT/CHAT/CHAT.md`](../AGENT/CHAT/CHAT.md) · `broker.py` | live end-to-end push | 🟡 wired, demo pending |
| R1 | content generator wired to emit slot (CLM → words) | `CLM/P4_PRODUCTION_ROADMAP.md` · `.verdicts/clm-prod-rung/` · `AGENT/CHAT/anima_participant.py`(emit co-gate) · `AGENT/CHAT/akida_emit_bridge.hexa` | mid d512/L8/E8 QAT verdict · **LIVE emit-wiring soak** | 🟢 **LANDED** (2026-05-31) — **CLM words ride the on-chip spike.** Live AKD1000 ENFORCING soak (PR #1598): emit ← (motivation ∧ spike-edge) co-gate wired into the live participant. 133 ticks · 30 motivation-high · **12 emits (anima NOT mute)** · 18 suppressed = **60% suppression** (spike-absent vetoed) · rollback-guard = NOT_MUTE. `gate_when_idle=True` fallback (dead spike channel → software-only). mid int4 QAT (#1553) feeds the slot. |
| R2 | live learning coupled to dialogue (on-chip PLASTICITY) | `CLM/CLM_CAMPAIGN_26.md` · `H_865`(BOUND) · `H_873/884`(ANCHOR) · `H_872/879/881/883` · `H_904 ★`(silicon) | `F-CLM-BOUND` · `F-CLM-ANCHOR` · `F-CLM-PLAST-*` · `F-CLM-ONCHIP` | 🟢 **SUPPORTED (mid) + SILICON ✅** — edge-learn stack: adapter(BOUND)🟢 + ANCHOR 🟢 H_873/884 + freeze 🟢 H_872/881 + per-layer 🟢 H_879 + replay 🟢 H_883; **on-chip learn HW≠SW confirmed on AKD1000 (H_904 ★ 🟢 #1593)**. GAIN-capacity 🔴 H_866 (→ H_899, deferred) |
| R3 | dialogue quality (SFT + self-play) benchmarked | `UNIVERSE/H_863·H_867·H_868·H_886` | `F-CLM-DIALOGUE` · `F-CLM-DIALOGUE-FLOOR` · `.verdicts/clm-dialogue*/` | 🟢 **mid CLOSED** — self-play 🟢 (#1555) · corpus 3× 🟢 (#1559) · **absolute floor 🟢 H_886 curriculum (#1590)**. large transfer 🔴 (→ H_888, deferred) |
| R4 | coffeeshop group-chat production launch | (launch doc — TBD on R1–R3) | end-to-end 90-min soak | ⏳ planned — gates: on-silicon learn ✅ (H_904 ★) · **R1→emit wiring ✅** (#1598 LIVE soak) · **backbone production-scale → [P6 ladder](../CLM/P6_SCALE_LADDER_7B.md)** (mid 13.65M ✅ → large 44.68M → 3B → 7B · rung별 F-CLM-SCALE-TRANSFER · fire-READY scaffold 미발사) |

R0 verdict (live AKD1000, device `BC.00.000.002`, `BackendType.Hardware`):
`thr 99 → 0 spikes` (SILENCE), `thr 1 → 16 spikes` (EMIT) —
`motivation → set_threshold → on-chip fire → should_interrupt` closed on hardware
(`UNIVERSE H_846` 🟢 SUPPORTED-NUMERICAL). The loop *works*; **R1 makes the
spikes carry words.**

---

## The active SBS plan (R1 — in flight)

R1 is being executed right now by a `/step-by-step` handoff agent (runpod pod
`clm-prod-rung` READY).

- **plan (SSOT)**: `drafts/clm-production-roadmap-plan.md` (`status: active`)
- **scope**: lift CLM from toy (≤2.70M · byte-vocab · routing 🔴) to a production
  conversational model that feeds the `brain_decide` emit slot.
- **locked decisions** (full @L1–@L8 + Q-TRUST tree in the plan):

```
@L1 non-deterministic on-chip learning = first-class ("alive while learning")
@L2 measure ⊥ deploy + chip PLASTICITY always-coupled
@L3 pluggable A/B/C routing-escape lane (default B content-escape)
@L4 dialogue data = ①CC logs + ②self-play   (③ShareGPT/ChatGPT-gen forbidden)
@L5 2-track scale ladder (GPU measure rung ⊥ AKIDA chip-fit deploy rung)
@L6 dialogue method B = SFT + self-play (H_CLM_DIALOGUE benchmark)
@L7 handoff = doc + scaffold + first GPU QAT fire auto-dispatched (runpod)
@L8 location = CLM/ continuity (+ UNIVERSE 3 new H + .verdicts benchmarks)
```

- **inviolable**: external LLM 0 · foundation-borrow 0 (pure scratch) · learning
  is AKIDA-envelope QAT (int4-sym · act_bits) · no ShareGPT/Alpaca.

---

## Component map (the moving parts)

```
[ user chat ] ──▶ [ broker /ws ] ──▶ [ motivation ] ──▶ [ AKIDA threshold ] ──▶ [ CLM emit ]
  group chat        AGENT/CHAT         brain_decide       AKIDA / SUB_ENGINES     CLM/ (R1)
                    broker.py          (substrate)        spike 9512 / ctrl 9513   generates words
```

| part | path (canonical, origin/main) | role |
|---|---|---|
| group-chat hub | `AGENT/CHAT/broker.py` | WS hub — ingest + fanout + `/motivation/recent` |
| AKIDA read half | `SUB_ENGINES/AKIDA/scripts/akida_ws_publisher.py` | on-chip fire (9512) → broker |
| AKIDA write half | `SUB_ENGINES/AKIDA/scripts/akida_threshold_driver.py` | motivation → `set_threshold` (9513) |
| pi5 streamer | `SUB_ENGINES/AKIDA/scripts/spike_streamer.py` | on-chip threshold-and-fire (pi5 side) |
| launch glue | `LAUNCHPAD/coffeshop_akida_launch.{hexa,py}` | R0 closed-loop launch (emit/silence) |
| quorum learn | `LAUNCHPAD/coffeshop_quorum_learn.{hexa,py}` | DECODER + PLASTICITY lane split |
| silicon switch | `AKIDA/akida_backend.hexa` | `akida_backend_resolve` (HW-first, default "hw") |
| content generator | `CLM/` (R1, in flight) | the words that ride the emit slot |

pi5 = `192.168.50.155` (AKD1000) · controller = mini `192.168.50.39`.

---

## Sibling domains (LAUNCHPAD composes these)

- ⇄ [AKIDA](../AKIDA/AKIDA.md) — AKD1000 silicon + HW-first switch + spike control (9512/9513).
- ⇄ [DECODER](../CORE/DECODER/DECODER.md) — inference lane (HW forward ↔ SW byte-identical 🟢).
- ⇄ [PLASTICITY](../PLASTICITY/PLASTICITY.md) — learning lane (HW on-chip ↔ SW 🔴 non-equivalent · @L1 lives here).
- ⇄ [CHANNEL](../CHANNEL.md) — output channels (text/voice/tension) · broker launch connect point.
- ⇄ [WAKE](../WAKE.md) — consciousness daemon living loop (COFFESHOP = a 90-min WAKE window).

---

## One-line start guide (resume here)

```
cat LAUNCHPAD/LAUNCHPAD.md                      # current-state milestones
cat drafts/clm-production-roadmap-plan.md       # the active R1 plan + locked decisions
ls  .verdicts/846_launchpad_coffeshop_on_akida  # R0 closed-loop evidence (LANDED)
```

When the R1 handoff agent reports: read `CLM/P4_PRODUCTION_ROADMAP.md` + the new
`.verdicts/clm-prod-rung/` verdict, flip the R1 row to 🟢, then open R2.

---

## cross-link

- state hub: [`LAUNCHPAD.md`](LAUNCHPAD.md) (milestones · sibling cross-update)
- R0 verdict: `.verdicts/846_launchpad_coffeshop_on_akida/F-LAUNCHPAD-LOOP.txt`
- R1 plan: `drafts/clm-production-roadmap-plan.md`
- milestone lineup (canonical ckpts): [`LINE-UP.md`](../LINE-UP.md)
- governance: `@D a_fire_autonomous` (cost-bearing fire = autonomous) · `@D a_substrate_native_speak` (anima speaks from substrate, not stimulus-response) · `@D a_blue_closed` (close outputs AND wiring at 🔵)
