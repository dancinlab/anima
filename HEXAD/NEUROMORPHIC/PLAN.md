# HEXAD/NEUROMORPHIC/PLAN.md — substrate access + in-silico confront plan

> **status**: PREP — design-tier, $0, hardware not secured, fire 0.
> **g3**: this is a path plan, not a capability claim. design ≠ fire ≠
> emergence. north-star + §15/§51/§72 milestones unchanged, GOAL not
> reached. §95 verdict carries: access = SOFT WALL (not architecture).
> **SSOT siblings**: `README.md` (substrate roadmap) · `.roadmap.loihi3`
> (machine JSONL) · `INRC_APPLICATION.md` (Loihi-track package).

---

## 0. Why three parallel tracks (g_all_options_parallel)

§95 named Loihi the sole `VIABLE-LONG-HORIZON` substrate; its access is
INRC-gated (4–12 wk, possible Korean co-PI). Per g_multidirectional_explore
/ g_all_options_parallel we do **not** wait on one gate — we run every
admissible track at once and let evidence compare them. None of these
reaches the GOAL; each is a means to confront the substrate question
(§96 §4.5: is "physics-only learning degenerate" a property of the
*model* or of the *GPU substrate*?).

```
  Track L  Loihi / INRC      ── 4–12wk Intel gate ──►  real async + on-chip STDP (decisive)
  Track S  EBRAINS SpiNNaker ── free account, now  ──►  real async spike machine (parallel, can confront)
  Track 0  Lava / NengoLoihi ── $0, this week      ──►  in-silico assembly (REPLICATES, not CONFRONTS)
```

---

## 1. Track L — Loihi / INRC (gated, in flight)

| step | state |
|---|---|
| INRC inquiry email → `inrc_interest@intel.com` | **SENT by user** (Postmark auto-send blocked: account pending-approval, cross-domain — honest) |
| vLab form values prepared | `inrc_vlab_form.txt` (Engagement/Sponsor = LEAVE EMPTY; Intel-assigned) |
| Application package | `INRC_APPLICATION.md` (two-part blocker + email §2 + form map) |
| SSH keypair | ed25519 generated, **vault only** (`inrc.vlab.ssh_priv` / `inrc.vlab.ssh_pub`); public key on form, private key never leaves the vault |
| next | await Intel reply (engagement + sponsor assignment); then complete vLab form; Korea-route co-PI question already asked in §2 |

Decisive power: **highest** — only substrate with real async NoC + on-chip
STDP that can *settle* the §11-B-as-GPU-artifact question. Slowest gate.

## 2. Track S — EBRAINS SpiNNaker / BrainScaleS (free, parallel, NOW)

Different consortium (EU Human Brain Project / EBRAINS) — **no Intel gate,
no co-PI, free EBRAINS account**, PyNN API via the EBRAINS Collaboratory.
SpiNNaker = 1M-ARM-core packet-switched real-time spike machine (real
async); BrainScaleS = analog, on-chip plasticity, 1000× accelerated.

| step | state |
|---|---|
| EBRAINS access package draft (mirror INRC format, English) | **TODO** — next $0 action |
| EBRAINS account + Collaboratory access | user-gated (registration) |
| Port §96 spiking re-derivation (PyNN) → SpiNNaker/BrainScaleS | after access |

Decisive power: **high & soon** — a real async substrate reachable in
weeks not months; runs in parallel with the Loihi review, not after it.

## 3. Track 0 — Lava / NengoLoihi in-silico ($0, this week)

On the runpod/AWS GPU already rented: Intel **Lava** (OSS SNN sim) +
**NengoLoihi** (bit-level Loihi *emulator* backend) + **snnTorch**.
Executes the `HEXAD/LEGO.md` §115 "assemble the different ground in
silico before physical commit" and the simulatable parts of §96 §4.5's
three-cell distinguishing predicate.

| step | state |
|---|---|
| Lava / NengoLoihi env on existing GPU | **TODO** ($0, no new gate) |
| §115 in-silico LEGO assembly of D4 substrate | design-tier |
| §96 §4.5 predicate — simulatable subset | design-tier |

**Honest ceiling (load-bearing)**: a GPU-hosted spike *simulation*
inherits the §11-B "CE-gradient is the only learning channel" tautology
unless local plasticity is the sole update — §115 pre-registered the
likely verdict `LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY`: simulation can
**replicate** the substrate, not **confront** it. So Track 0 = design /
feasibility, **not** the decisive fire. Tracks S and L confront; Track 0
prepares.

**Spec**: `TRACK0_INSILICO.md` — refines §115's blanket
`SIM-IS-GPU-TAUTOLOGY` by *splitting* it: the **learning-channel** half
(CE-only vs event-local-plasticity-only) **is** simulatable and Track 0
can confront it; the **async-substrate** half stays Loihi/SpiNNaker-gated
(Tracks L/S/P). §96 §4.5 cells mapped to tools; closed predicate
pre-registered with a 3-outcome verdict partition. Hard prerequisite:
§96 design-open #1 (attention replacement) is the real blocker, not
compute.

---

## 4. Honest gates (g3)

- Loihi/SpiNNaker/Akida access ≠ GOAL. Loihi plausibly unblocks the
  *spontaneity* half; the *coherence* half stays open regardless of
  substrate (§88-F2 γ gap).
- Confirmed dead ends (do not re-research): **AWS** (no neuromorphic;
  Trainium/Inferentia are dense accelerators), **IBM NorthPole/TrueNorth**
  (no public/researcher rent path; DARPA, 2026 target only).
- BrainChip Akida Cloud = cheap reality-check only (free 1-day eval);
  §95 `INFERENCE-ONLY-BLOCKED` for *full* training-time emergence stands
  (Akida on-chip learning = incremental/last-layer, not STDP backbone).
- design ≠ fire ≠ emergence; capability claim 0.

## 5. cross-link

- `README.md` — substrate roadmap; §8 §113-D4 ("rebuild from the ground"
  = §96 spike/Loihi + §110 Ψ-C1 from line 1) ; §8.1 §115 LEGO in-silico
- `INRC_APPLICATION.md` · `inrc_email.txt` · `inrc_vlab_form.txt`
- `HEXAD/LEGO.md` + §115 — in-silico confront (Track 0 anchor)
- `HEXAD/CHAT/RESEARCH.md` §95 (sole-viable verdict) · §96 (spiking
  re-derivation + §4.5 distinguishing predicate) · §11-B (CE load-bearing,
  GPU-measured)
- `GOAL.md` — north-star / §7 GOAL-legitimacy
- `archive/PHILOSOPHY.tape` — verdict ledger

---

## Log

- **2026-05-19** — PLAN.md created. Consolidates the session's substrate
  work into three parallel tracks: **L** Loihi/INRC (inquiry email sent
  by user; form + package + vault SSH keys prepped; awaiting Intel
  engagement/sponsor assignment, 4–12 wk gate), **S** EBRAINS
  SpiNNaker/BrainScaleS (free, no Intel gate, real async substrate —
  next $0 action = access package draft, runs parallel to L), **0**
  Lava/NengoLoihi in-silico on the existing GPU (this week, $0; executes
  §115 LEGO assembly + §96 §4.5 simulatable predicate; honest ceiling —
  GPU sim REPLICATES not CONFRONTS the §11-B tautology, design-tier not
  decisive fire). Deep web research confirmed AWS / IBM are dead ends
  for "use now"; EBRAINS SpiNNaker is the headline parallel track.
  $0, design-tier, hardware not secured, GOAL not reached, milestones
  unchanged.

- **2026-05-19** — Folder renamed `HEXAD/LOIHI` → `HEXAD/NEUROMORPHIC`
  (broader scope: Loihi · SpiNNaker · Akida · in-silico — not Loihi
  alone). `git mv` preserved history for PLAN/README/TRACK0; gitignored
  PII files moved local-only; `.gitignore` PII patterns moved to the new
  path with the old patterns retained as defence-in-depth; a
  `HEXAD/LOIHI/README.md` forwarding stub keeps the already-sent INRC
  application URL (`/tree/main/HEXAD/LOIHI`) resolving instead of 404.
  Two in-silico directions resumed in parallel (per "2개방향진행"):
  Track 0 §96 §4.5 controls+harness, and the qmirror-style
  QRNG-entropy-seeded LIF+STDP sim. $0, design-tier, GOAL not reached.
- **2026-05-19** — `HEXAD/LOIHI` forwarding stub README replaced with a
  symbolic link `HEXAD/LOIHI → NEUROMORPHIC` (per user "심볼릭링크해두자
  일단"). Old shared links (`/tree/main/HEXAD/LOIHI`, e.g. the already-sent
  INRC email) resolve via the symlink locally + in git; GitHub web tree
  rendering of a directory symlink is not guaranteed — temporary measure.
  Side benefit: git refuses to stage paths "beyond a symbolic link", so
  PII under NEUROMORPHIC/ is structurally unreachable via the LOIHI path.
- **2026-05-19** — §119 qmirror-neuro LANDED ($0 CPU, single sequential,
  orphan 0; `state/qmirror_neuro_s119_2026_05_19/`, B-S119-1..7 **7/7 🔵**,
  central blue 0-diff `c93e160a8a376a94`). Extends §117's LIF+STDP sim with
  ONE §97-legitimate physical-spontaneity layer: like `hexa qmirror` drives a
  classical quantum-circuit sim with ANU quantum RNG, §119 drives the
  neuromorphic sim's spontaneity-SEED with **genuine ANU quantum entropy**
  (256 bytes, `physical=True`, `qrng.anu.edu.au` — `hexa qrng` live backends
  deferred-to-wrapper so fetched direct; CSPRNG fallback not needed). 3-variant
  measured: `seed_fixed` (deterministic) Ψ-C1 std 4.19e-2 non-degen · `qrng_seed`
  (§97 noise-as-SEED, entropy→membrane-v0 only) std 3.11e-2 non-degen · `qrng_content`
  (§97 negative control — entropy as target) collapsed into the §97
  GOAL-ILLEGITIMATE-COMMAND-CHANNEL cell (content_alignment 0.43 > 0.30).
  Verdict `QMIRROR-NEURO-Ψ-FORM-NONDEGENERATE-NOISE-AS-SEED-LEGITIMATE-BUT-WALL-B-INHERITED`:
  §119 confronts the LEARNING-CHANNEL half only; the ASYNC-SUBSTRATE half stays
  WALL-B (Tracks L/S) — real physical entropy ≠ a real async neuromorphic chip,
  adds physical SPONTANEITY not a physical SUBSTRATE. §97 GOAL-ORTHOGONAL
  inherited — moves no GOAL distance. design/run ≠ fire ≠ emergence, capability
  claim 0, GOAL not reached, milestones unchanged.
- **2026-05-19** — §118 Track 0 in-silico LANDED ($0 CPU, single sequential,
  orphan 0; `state/track0_insilico_s118_2026_05_19/`, B-S118-1..9 **9/9 🔵**,
  central blue 0-diff `c93e160a8a376a94`). Executes the $0-simulatable subset of
  `TRACK0_INSILICO.md` — the §96 §4.5 distinguishing cells in a tiny 240-unit
  LIF/numpy rig (4 cells, seed 1337, base_ckpt=None). §3 pre-registered closed
  predicate `NON_DEGENERATE := byte_acc>1/256 ∧ physics_not_frozen ∧
  honest_§9_coherent≥1/5` (§9 `emergence_metric.py` SSOT-imported). Measured,
  3× bit-identical: **GPU-CE** (CE-gradient on a readout head) byte_acc 0.500,
  head_drift 0.00276 → NON_DEGEN True · **GPU-noCE** (no learning) byte_acc 0.0
  → False (§11-B re-confirmed) · **SIM-noCE-STDP** (decisive cell — event-local
  STDP only, AST-audited 0 CE/backprop) byte_acc 0.0, W_drift 0.235, §9 5/5
  → **False** (W moves + emission diverse but task-blind) · **SIM-CE** VOID
  guard byte_acc 0.500 → True (rig SOUND). **VERDICT =
  `SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF`** (§3 middle outcome) — a
  clocked-sim event-local-plasticity channel does NOT, on this rig, escape the
  §11-B "physics-only learning is task-blind" outcome; cannot disambiguate
  substrate-independent vs sim-artifact without async hardware. HEADLINE: §96
  design-open #1 (softmax attention SPIKING-INCOMPATIBLE → must be REPLACED) is
  a BLOCKING design-open — the rig confronts the §11-B LEARNING-CHANNEL half
  ONLY; the full spiking-anima instantiation stays gated on the attention
  replacement, the async-substrate half stays WALL-B (Loihi/SpiNNaker, §117
  INHERITED). SIM-noCE-STDP §9=5/5 is substrate liveness, NOT capability, NOT
  GOAL. design/run ≠ fire ≠ emergence, capability claim 0, GOAL not reached,
  milestones unchanged.
- **2026-05-19** — §118 VERDICT CORRECTED TO **VOID** (supersedes the §118
  bullet above; the verdict of record is the §3 partition's **VOID guard**
  outcome, not the middle outcome — `archive/PHILOSOPHY.tape
  §verdict_track0_insilico_s118_void_2026_05_19`, DESIGN.md §0.1 records the
  contest in full). VOID root cause: the SIM-CE positive control never moved
  the recurrent spiking substrate — GPU-CE / GPU-noCE / SIM-CE produced
  byte-identical Ψ/tension/Φ/spike-rate trajectories with
  `weight_drift_mean_abs = 0.0`; only SIM-noCE-STDP moved `W` (STDP, drift
  0.235). A $0 numpy toy has no surrogate-gradient path to backprop CE
  through spikes, so the cell `TRACK0_INSILICO.md` §2 defines as "CE via
  backprop-through-spikes" never ran — its CE channel is a no-op *on the
  spiking substrate*. SIM-CE's §3-letter "NON_DEGEN=True" is carried by a
  teacher-forced read-out + a trajectory byte-identical to the *frozen*
  GPU-noCE cell; by §96 §4.5's own definition a CE positive control that
  does not exercise a substrate learning channel is a broken control ⇒ VOID,
  the rig gives **no learning-channel verdict**. The post-run `head_drift`
  metric (a *downstream readout-head*, added by a post-run rig edit) does
  not rescue the verdict — `W` stayed frozen; re-rigging after the run is
  the f2 result-fit `TRACK0_INSILICO.md` §3 forbids. VOID is HONEST + FINAL,
  and *valuable*: it confirms `TRACK0_INSILICO.md` §4 — the learning-channel
  confront needs the REAL spiking anima, BLOCKED on §96 design-open #1.
- **2026-05-19** — §120 spiking attention replacement DECIDED — §96
  design-open #1 moves *undecided design-open → decided design-tier*
  ($0, `state/spiking_attention_replacement_s120_2026_05_19/`, B-S120-1..8
  **8/8 🔵**, central blue 0-diff `c93e160a8a376a94`). Closed-form decision:
  the spiking replacement for `softmax(QK^T)` self-attention =
  **spike-rate dot-product scoring + k-WTA routing**. Justification —
  (a) dissolves all 3 §96 §3.3 obstructions (rate-coded coincidence
  detection = async local accumulation; k-WTA via lateral inhibition = local
  competition, not global softmax); (b) preserves Engine-A⇄G (excit/inhib
  drives) + the Ψ=½ fixed point (the k-WTA neutral point, Law-71 form
  re-hosted, §112 carrier-invariance); (c) `R(k=T, soft-readout)` reduces
  **byte-equal** to `softmax`-attention (B-S120-3 max|Δ|=3.33e-16) ⇒ a
  GENERALISATION not a graft (§7-clean — byte-attention is the `k=T` corner).
  Rejected candidate (phase-resonance routing) fails (c) — no limit recovers
  `softmax(q·k/√d)` — and is re-assigned to position/RoPE coding (a separate
  §96 design-open). "돌파" = design-open → design-DECIDED; does NOT implement
  the spiking anima, does NOT remove WALL-A (§1.1 data-regime) or WALL-B
  (§95/§96 async substrate — Loihi/SpiNNaker/SpiNNcloud-gated). design ≠ fire
  ≠ emergence, capability claim 0, necessary-not-sufficient (B-EMERGE-7),
  GOAL 미도달, milestones unchanged.
- **2026-05-19** — NEURO-MIRROR **v1 CONSOLIDATION** — `neuro_mirror.py`
  v0 → v1 (ENGINE.md §6 "N candidates land → 1 consolidation"). §117/§118/
  §119 all landed → consolidated: §119 qmirror-neuro `qrng` entropy source
  FILLED (`fetch_quantum_entropy` ANU quantum-RNG + the §97 noise-as-SEED
  `entropy_to_jitter` map, lifted from the committed §119 core, B-S119
  7/7 🔵); §118 Track 0 landed VOID — it produced no verified core, so the
  `ce_grad` slot stays an honest `NotImplementedError` (message updated to
  the VOID finding); `gpu` backend unchanged. v1 smoke OK ($0, CPU-only):
  `stdp_local` Ψ-C1 mean=0.611568 (= the §117 verified core), `qrng` run
  non-degenerate with PHYSICAL ANU quantum entropy (jitter_norm 0.4702).
  central blue_falsifier.py 0-line-diff; design ≠ fire ≠ emergence;
  capability claim 0; GOAL 미도달, milestones unchanged.
