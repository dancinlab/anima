"""H_965 + H_977 — SUBSTRATE-axis CHIP-ONLY blocker record (substrate=AKIDA, UNREACHABLE here).

H_965 (does the perceive->act loop close ON-CHIP, on-chip latency, IP-v1 mapping wall?) and
H_977 (on-chip energy-per-decision / power envelope) have falsifiers whose CORE measurement
is intrinsically ON-CHIP: a yes/no that the decision runs on the AKD1000 (not host CPU), the
closed-loop latency from real silicon, and the AKD1000 + host energy telemetry. There is NO
meaningful CPU-mirror partial for these core claims (a CPU "loop" or a CPU "energy" number
would NOT answer "does it close on-chip / is the chip sub-watt" — and claiming so would
violate a_lane_akida_gpu_split). So these are honestly ⚠ INCOMPLETE-BLOCKED + handoff.

This script just RECORDS the blocker by probing for the chip (so the verdict file is a real
measured artifact: the chip is provably absent on this host)."""
import sys


def probe_akida():
    try:
        import akida
        devs = akida.devices()
        return True, f"akida {getattr(akida, '__version__', '?')}, devices={devs}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def main():
    print("=" * 78)
    print("H_965 + H_977 — AKIDA CHIP-ONLY falsifiers — substrate reachability probe")
    print("substrate=AKIDA (Lane A) — a_lane_akida_gpu_split: NEVER claim on-chip from CPU")
    print("=" * 78)
    import platform
    print(f"host platform = {platform.platform()}")
    ok, msg = probe_akida()
    print(f"akida BackendType.Hardware reachable? {ok}")
    print(f"  probe result: {msg}")
    print("the live AKD1000 lives on the pi5-akida host (single-tenant, H_860 streamer "
          "stop/restart); it is NOT this Mac. cf /PI5-AKIDA.json.")
    print("-" * 78)
    if not ok:
        print("VERDICT H_965: INCOMPLETE-BLOCKED — on-chip perceive->act loop closure + on-chip "
              "latency + AKD1000 IP-v1 mapping check REQUIRE BackendType.Hardware on the physical "
              "AKD1000 (pi5-akida), unreachable from this Darwin host. No faithful CPU partial "
              "exists for 'does the decision run on-chip'. substrate=AKIDA. HANDOFF filed.")
        print("-" * 78)
        print("VERDICT H_977: INCOMPLETE-BLOCKED — on-chip energy-per-decision + power-envelope "
              "REQUIRE live AKD1000 + host energy telemetry (and a behavior-matched chip loop, "
              "which itself depends on H_965/H_966). Unreachable here; a CPU energy number would "
              "not answer the sub-watt on-chip claim (a_lane_akida_gpu_split). substrate=AKIDA. "
              "HANDOFF filed.")
        print("-" * 78)


if __name__ == "__main__":
    main()
