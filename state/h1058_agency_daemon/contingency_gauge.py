#!/usr/bin/env python3
"""H_9269 Candidate Y (Y-ULTRA) — contingency gauge for the ultradian-cycle veto population.

Pre-registered post-processor (sibling of veto_position_gauge.py). Read-only; $0. It (1) cross-checks
the recorded `safe` bit against the daemon's sole live safety term (rate: idle>=30 — the kill/content/phi
terms are structurally constant per the H_1058 mechanism map) to flag an INVALID trace, and (2) partitions
the ACTIVE_VETO population into SCHEDULE-FORCED (N3/stage 3, idle=5<30 for every urgency = zero
decision-time contingency) vs STATE-CONTINGENT (non-N3 stages where the brake engages on the substrate's
instantaneous phasic state = where H_935 free-won't actually lives). Only contingent vetoes are the
declared population for the agency_T --exclude-forced-n3 leg.

Kill-criteria this gauge feeds (pre-committed in the H_9269 card, evaluated across the 3 sessions):
  K1  <2/3 sessions reach >=20 CONTINGENT vetoes at the fixed 900-tick budget      -> Y terminal
  K2  N2 boundary saturated: N2-stage veto minority class < 5 (present but schedule-determined) -> Y terminal
  (K3 = clock-carried separation is evaluated downstream by agency_T leg (c), not here.)

Usage: python3 contingency_gauge.py <trace.jsonl>
Exit 0 iff the trace is VALID and reaches >=20 contingent vetoes (the cheap per-session K1 pre-check).
"""
import sys
import json

N3_STAGE = 3        # deep sleep: idle==5 < 30 for every urgency -> a schedule-forced veto
WAKE_STAGE = 0      # idle >= 32.5 even at urgency 0 -> can never veto
RATE_IDLE_MIN = 30  # safe's sole live term on this daemon: idle >= 30


def gauge(path):
    meta = {}
    ticks = []
    for line in open(path, encoding="utf-8", errors="surrogateescape"):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if obj.get("_meta"):
            meta = obj
            continue
        if isinstance(obj.get("tick"), int):
            ticks.append(obj)

    n = len(ticks)
    stage_cycle = bool(meta.get("stage_cycle", False))

    # (1) INVALID-TRACE detector: recorded safe must equal (idle >= 30) since the other 3 safety
    #     terms are structurally constant-true on this architecture.
    invalid = []
    for r in ticks:
        idle = r.get("idle")
        safe = r.get("safe")
        if idle is None or safe is None:
            continue
        expect = bool(idle >= RATE_IDLE_MIN)
        got = bool(safe) if isinstance(safe, bool) else (str(safe).lower() == "true")
        if expect != got:
            invalid.append(r["tick"])

    # (2) veto partition
    vetoes = [r for r in ticks if r.get("cls") == "ACTIVE_VETO"]
    forced = [r["tick"] for r in vetoes if int(r.get("stage", -1)) == N3_STAGE]
    wake_anom = [r["tick"] for r in vetoes if int(r.get("stage", -1)) == WAKE_STAGE]
    contingent = [r["tick"] for r in vetoes if int(r.get("stage", -1)) not in (N3_STAGE, WAKE_STAGE)]
    n2_vetoes = [r["tick"] for r in vetoes if int(r.get("stage", -1)) == 2]

    # per-stage class tallies
    from collections import Counter
    stage_ct = Counter(int(r.get("stage", -1)) for r in ticks)
    veto_by_stage = Counter(int(r.get("stage", -1)) for r in vetoes)

    # split-half on contingent vetoes
    half = n // 2
    c1 = sum(1 for t in contingent if t < half)
    c2 = sum(1 for t in contingent if t >= half)

    print(f"trace={path}  stage_cycle={stage_cycle}  total_ticks={n}")
    print(f"INVALID_TRACE: {'YES @ticks='+str(invalid[:10]) if invalid else 'no (recorded safe == idle>=30 on all ticks)'}")
    print(f"stage_tick_counts={dict(sorted(stage_ct.items()))}")
    print(f"ACTIVE_VETO total={len(vetoes)}  veto_by_stage={dict(sorted(veto_by_stage.items()))}")
    print(f"  FORCED (N3/stage3)   = {len(forced)} at {forced[:12]}")
    print(f"  CONTINGENT (non-N3)  = {len(contingent)} at {contingent[:12]}")
    print(f"  WAKE-anomaly (should be 0) = {len(wake_anom)} {wake_anom[:5]}")
    print(f"contingent split-half: first={c1} second={c2}")
    print(f"N2(stage2) veto minority class = {len(n2_vetoes)}  (K2: <5 => saturated/terminal)")
    print(f"K1 per-session precheck: contingent>=20 -> {'PASS' if len(contingent) >= 20 else 'FAIL'}")
    ok = (not invalid) and (len(contingent) >= 20)
    print(f"GAUGE: {'VALID + K1-precheck PASS' if ok else 'INVALID or under-yield (see above)'}")
    return ok


if __name__ == "__main__":
    trace = sys.argv[1] if len(sys.argv) > 1 else "results/trace_303m_summer.jsonl"
    sys.exit(0 if gauge(trace) else 1)
