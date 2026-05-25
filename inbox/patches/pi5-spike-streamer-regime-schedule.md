# pi5 spike_streamer — `--regime-schedule` extension (inbox patch)

> **kind**: inbox-patch · coordination doc · doc-only (no source mutation from anima repo)
> **target**: `/home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py` on pi5 (`ubuntu@192.168.50.155`)
> **owner verdict**: separate / non-tracked deploy — pi5 streamer is NOT pulled from `dancinlab/anima`. Patch requires external coordination with pi5 maintainer (manual edit + service restart).
> **anchors**: [[REGIME_EXPANSION]] · [[AKIDA_FIRST]] · [[SW_CONDITION_DESIGN]] §6 · [[SPIKE_FACTOR_MAP]] §4

---

## §1 — Summary (1 line)

anima needs `--regime-schedule R3:60,R1:30,R2:30 --schedule-loop --schedule-jitter <pct>` on pi5 streamer so [[SW_CONDITION_DESIGN]] §6 Phase 2 activation gate (`≥ 2 regimes + ≥ 5 transitions`) can accumulate.

## §2 — Current state (probed 2026-05-23)

- Live process: `python3 /home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py --port 9512 --duration 86400 --regime R3` (single regime, 24 hr soak).
- `argparse` accepts `--regime` ∈ {R3, R2, M} (line 315 of streamer); R1 path absent.
- `make_threshold_R3` (line 75) and `make_threshold_R2` (line 85) exist; no `make_threshold_R1`.
- Streamer source on pi5 is at `/home/ubuntu/anima/...` (standalone deploy, not git-tracked). The sister `/home/ubuntu/core/anima/` does have a `.git` dir but it is incomplete (no HEAD / config) and contains no `SUB_ENGINES/AKIDA/scripts/`. Therefore: no auto-deploy from `dancinlab/anima` PR merges; this patch is informational / coordination only.

## §3 — Mimic-targets (verbatim from REGIME_EXPANSION §1)

```
+--------+----------------------------+-----------------------+-------------------------+
| regime | output dynamics            | NPU stimulus          | downstream signal       |
+--------+----------------------------+-----------------------+-------------------------+
| R3     | tonic zero-input baseline  | input = 0 vector      | 8/16 unit deterministic |
|        | (~10 Hz steady)            | thr = heterogeneous   | tonic fire, low isi_cv  |
+--------+----------------------------+-----------------------+-------------------------+
| R1     | oscillatory rhythm         | frequency-modulated   | periodic burst envelope |
|        | (5-20 Hz envelope)         | sinusoidal drive      | n_spikes regular swing  |
+--------+----------------------------+-----------------------+-------------------------+
| R2     | bursting / event-driven    | uniform thr ~24 +     | intermittent high       |
|        | (varies 0..16 per record)  | noise input           | n_spikes, high isi_cv   |
+--------+----------------------------+-----------------------+-------------------------+
```

## §4 — Rationale (option (c) — single-process schedule arg)

Selected over (a) multi-process arbiter + (b) external orchestrator because:
- 1 systemd unit supervises 1 NPU owner (avoids `/ws/akida` ingest race).
- TIME-keyed schedule makes transitions arg-deterministic — downstream telemetry can predict transition density.
- Backward-compatible: `--regime R3` legacy flag remains; new arg mutually exclusive via argparse group.

## §5 — Patch sketch (pseudo, do NOT apply from anima repo)

```python
# spike_streamer.py — add to argparse block (around line 315)
group = ap.add_mutually_exclusive_group()
group.add_argument("--regime", default=None, choices=["R3", "R2", "M", "R1"])
group.add_argument("--regime-schedule", default=None,
                   help="e.g. R3:60,R1:30,R2:30 — comma-sep <name>:<dwell_sec>")
ap.add_argument("--schedule-loop", action="store_true", default=True)
ap.add_argument("--schedule-jitter", type=float, default=0.25,
                help="uniform jitter fraction on each dwell (deterministic via --seed)")

# new threshold + drive paths
def make_threshold_R1(N=16): ...        # uniform mid-thr (sinusoidal drive carries the rhythm)
def input_drive_R1(t, N=16): ...        # sinusoidal vector, 5-20 Hz envelope

def parse_schedule(spec):
    # "R3:60,R1:30,R2:30" -> [("R3", 60.0), ("R1", 30.0), ("R2", 30.0)]
    return [(s.split(":")[0], float(s.split(":")[1])) for s in spec.split(",")]

def next_regime(schedule, idx, jitter, rng):
    name, base = schedule[idx % len(schedule)]
    dwell = base * (1.0 + jitter * (2 * rng.random() - 1))
    return name, max(dwell, base * 0.5), (idx + 1)

# inside main step loop:
#   if t - regime_start >= current_dwell:
#       (current_regime, current_dwell, sched_idx) = next_regime(...)
#       regime_start = t
#   thr = {"R3": make_threshold_R3, "R2": make_threshold_R2,
#          "R1": make_threshold_R1, "M":  make_threshold_M_modulated}[current_regime](args.n)
#   drive = input_drive_for(current_regime, t, args.n)
#   record["regime"] = LABEL_MAP[current_regime]   # keep existing string labels
```

## §6 — Acceptance criteria (from REGIME_EXPANSION §6 verbatim)

- **F-REGIME-EXP-1** — 1 hr soak after patch + broker `/akida/recent` last 200 records contain `≥ 2` distinct `regime` values.
- **F-REGIME-EXP-2** — 24 hr telemetry window: regime transition event count `≥ 5` ([[SW_CONDITION_DESIGN]] §6 gate verbatim).
- **F-REGIME-EXP-3** — 7 d telemetry: per-regime spike record count `≥ 200` for each regime (distribution-fit floor).
- **F-REGIME-EXP-4** — `--regime-schedule R3:60,R1:30,R2:30` 1 hr soak → record `regime` mode distribution within ±15% of schedule weight (50% R3 / 25% R1 / 25% R2 expected, jitter absorbed).
- **F-REGIME-EXP-5** — 24 hr soak: streamer process 0 crashes, broker WS reconnects `≤ 3`.

5/5 PASS → Phase 2 SW emitter activation gate satisfied for the regime-diversity row.

## §7 — Operational notes

- **Dwell distribution.** Lognormal mean 90 s / std 30 s / floor 30 s (REGIME_EXPANSION §3) — `--schedule-jitter 0.25` on a `R3:60,R1:30,R2:30` schedule gives mean cycle 120 s ≈ 720 transitions / 24 hr (10× margin over gate).
- **Schedule baseline (24 hr).** R3 60% / R1 25% / R2 15% dwell weight (preserves R3 dominance from current live stats).
- **`record["regime"]` field semantics.** Keep existing label strings (`R3_tonic_zero_input`, `R2_noise_event_driven`, `MODULATED`) and add `R1_oscillatory_drive` — downstream [[akida_consumer]] already extracts the `regime` key, no schema change. `regime_change` derivation = consumer-side window-to-window mode diff (separate cycle).
- **systemd unit (optional, currently absent).** Live streamer runs as a plain process (no `systemctl` unit observed). `Restart=always` recommended to mitigate the single-process SPOF noted in REGIME_EXPANSION §7(e).

## §8 — Rollout (pi5 maintainer side)

1. Apply patch sketch on `feat/regime-schedule` branch in pi5 deploy dir.
2. Unit test: `parse_schedule` + `next_regime` dwell rotation (no broker dependency).
3. 30 min dry-run with `--regime-schedule R3:60,R1:30,R2:30 --schedule-jitter 0.25`, inspect local record output for regime diversity.
4. Verify broker `/akida/recent` shows ≥ 2 regimes + ≥ 5 transitions → F-REGIME-EXP-1 PASS.
5. Promote to long-running (24 hr soak) → automated F-REGIME-EXP-2..5 evaluation.

## §9 — Coordination boundary

- anima repo does NOT own pi5 streamer source. NO direct ssh-mutating edit will be performed from this side (hexa-only-authoring directive applies; pi5 `.py` is tolerated drift, not new authoring).
- This inbox patch is the channel — pi5 maintainer applies + restarts the streamer service.
- Probe verdict logged in §2: `/home/ubuntu/anima/` is a standalone non-git deploy. Even after this patch's PR merges into `dancinlab/anima`, no auto-deploy occurs to pi5.

## §10 — Cross-links

- [[REGIME_EXPANSION]] — full design rationale (PR #141, merged)
- [[AKIDA_FIRST]] — Phase 1/2 boundary activation context
- [[SW_CONDITION_DESIGN]] §6 — Phase 2 gate (this patch unblocks the regime-diversity row)
- [[SPIKE_FACTOR_MAP]] §4 — regime modulator placeholders (R1 = 1.0 / R2 = 1.2; refit after telemetry)
- [[akida_consumer]] — downstream `regime` feature extractor
- [[telemetry_harness]] — paired evidence collector
