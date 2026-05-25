#!/usr/bin/env python3
# hexa-brain/eeg/_neuroglancer_helmet_helper.py
#
# B-1 Phase 2 (helmet annotation) — 16-channel CYTON_DAISY 헬멧 3D 좌표 emit.
#
# Hand-maintained Python (RFC-016 §1.4 anti-pattern avoided per Phase 2b
# precedent — see eeg/substrates/_brainflow_helper.py +
# eeg/_session_manager_helper.py).
#
# DESIGN (per design/core/neuroglancer_precomputed_export_2026_05_12.md):
#   - Coord source: MNE `standard_1020` montage (decision 3, BSD-3 license-
#     firewall-friendly, no FreeSurfer / fsaverage dep).
#   - 16-channel CYTON_DAISY layout: Fp1, Fp2, C3, C4, P7, P8, O1, O2, F7,
#     F8, F3, F4, T7, T8, P3, P4. (Matches eeg/substrates/channel_set.hexa
#     CYTON_DAISY_16 labels.)
#   - Output: sidecar `meta.json` carrying {schema, channels:[{name,xyz}...]}.
#     Full Neuroglancer Precomputed `annotation` layer (spatial_index, by_id,
#     binary point_annotation chunks) is V2 — deferred. V1 here is the
#     coordinate inventory; export_neuroglancer.hexa wires it into the
#     viewer URL as a future step.
#   - MNE optional: lazy import. If MNE missing → fall back to a hand-
#     curated fixture (Phase-1-honest: positions emitted, but flagged
#     `coord_source=fixture` instead of `coord_source=mne_standard_1020`).
#     Selftest passes in either path.
#
#   1. Sidecar meta.json is NOT yet wired into a Neuroglancer URL —
#      that's Phase 2.1 (export_neuroglancer.hexa --mode=helmet-annotation
#      consumes this file). V1 lands the coord layer + selftest only.
#   2. Fixture coordinates are NOT anatomically accurate — they're a
#      coarse 10-20 approximation hand-curated from the standard scalp
#      layout. The fixture path is for selftest determinism on a host
#      without MNE installed; production callers SHOULD have MNE.
#   3. Z axis: in MNE the head-surface coordinate frame puts z up
#      (vertex Cz at high z). We emit raw (x,y,z) from MNE without
#      rotation. The viewer URL composition step is responsible for
#      orientation transforms.

from __future__ import annotations

import argparse
import json
import os
import sys

SCHEMA = "hexa-brain/eeg/neuroglancer_helmet/1"

# CYTON_DAISY 16-channel labels (10-20 system). Order matches
# eeg/substrates/channel_set.hexa CYTON_DAISY_16.
CYTON_DAISY_16 = [
    "Fp1", "Fp2", "C3", "C4", "P7", "P8", "O1", "O2",
    "F7", "F8", "F3", "F4", "T7", "T8", "P3", "P4",
]

# Hand-curated fixture (used when MNE not installed). 10-20 approximations
# in a unit head-radius frame: x=left+/right-, y=anterior+/posterior-,
# z=superior+. Coarse; production uses MNE standard_1020.
FIXTURE_XYZ_M = {
    "Fp1": [-0.030, 0.090, 0.025],  "Fp2": [ 0.030, 0.090, 0.025],
    "F7":  [-0.075, 0.050, 0.000],  "F8":  [ 0.075, 0.050, 0.000],
    "F3":  [-0.045, 0.060, 0.050],  "F4":  [ 0.045, 0.060, 0.050],
    "T7":  [-0.090, 0.000, 0.000],  "T8":  [ 0.090, 0.000, 0.000],
    "C3":  [-0.050, 0.000, 0.075],  "C4":  [ 0.050, 0.000, 0.075],
    "P3":  [-0.045, -0.060, 0.050], "P4":  [ 0.045, -0.060, 0.050],
    "P7":  [-0.075, -0.050, 0.000], "P8":  [ 0.075, -0.050, 0.000],
    "O1":  [-0.030, -0.090, 0.025], "O2":  [ 0.030, -0.090, 0.025],
}


def _try_import_mne():
    """Lazy MNE import. Returns the module or None."""
    try:
        import mne  # noqa: F401
        return sys.modules.get("mne")
    except Exception:
        return None


def compute_montage_xyz_16(channel_names=None):
    """Return {channel_name: [x,y,z]} for the 16 CYTON_DAISY channels.

    Uses MNE standard_1020 if available; otherwise the hand-curated fixture.
    Returns (xyz_map: dict, coord_source: str). coord_source is one of
    'mne_standard_1020' or 'fixture'."""
    if channel_names is None:
        channel_names = CYTON_DAISY_16
    mne = _try_import_mne()
    if mne is None:
        return {n: list(FIXTURE_XYZ_M[n]) for n in channel_names}, "fixture"
    try:
        montage = mne.channels.make_standard_montage("standard_1020")
        positions = montage.get_positions()["ch_pos"]  # {name: ndarray(3,)}
        out = {}
        for n in channel_names:
            if n not in positions:
                # Fall back per-channel; MNE labels are usually consistent
                # but be defensive.
                out[n] = list(FIXTURE_XYZ_M.get(n, [0.0, 0.0, 0.0]))
            else:
                out[n] = [float(x) for x in positions[n]]
        return out, "mne_standard_1020"
    except Exception:
        return {n: list(FIXTURE_XYZ_M[n]) for n in channel_names}, "fixture"


def build_helmet_meta(channel_names=None):
    """Build the sidecar meta object (the dict that gets written as
    meta.json)."""
    if channel_names is None:
        channel_names = CYTON_DAISY_16
    xyz, coord_source = compute_montage_xyz_16(channel_names)
    return {
        "schema": SCHEMA,
        "coord_source": coord_source,
        "coord_units": "meters",
        "coord_frame": "head_surface (MNE convention: x=left, y=anterior, z=superior)",
        "channels": [
            {"name": n, "xyz": xyz[n]} for n in channel_names
        ],
    }


def write_helmet_meta(out_dir, channel_names=None):
    """Write meta.json into out_dir. Returns the dict written + path."""
    meta = build_helmet_meta(channel_names)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "meta.json")
    with open(path, "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    return meta, path


def cmd_selftest(args):
    print("== neuroglancer_helmet_helper selftest ==")
    print(f"schema={SCHEMA}")
    print("mode=selftest_synthetic")
    fails = 0

    mne_present = _try_import_mne() is not None
    print(f"  mne_available={mne_present}")

    # F_NG_HA_01: 16 channels emitted with 3-tuple xyz
    meta = build_helmet_meta()
    f01 = (isinstance(meta, dict)
           and meta.get("schema") == SCHEMA
           and isinstance(meta.get("channels"), list)
           and len(meta["channels"]) == 16
           and all(isinstance(c.get("xyz"), list) and len(c["xyz"]) == 3
                   for c in meta["channels"]))
    print(f"  channel_count={len(meta.get('channels', []))}")
    print(f"  coord_source={meta.get('coord_source')}")
    print(f"F_NG_HA_01={'PASS' if f01 else 'FAIL'}")
    if not f01:
        fails += 1

    # F_NG_HA_02: labels match CYTON_DAISY_16 exactly (order-preserving)
    emitted_names = [c["name"] for c in meta["channels"]]
    f02 = emitted_names == CYTON_DAISY_16
    print(f"  emitted_names={emitted_names}")
    print(f"F_NG_HA_02={'PASS' if f02 else 'FAIL'}")
    if not f02:
        fails += 1

    # F_NG_HA_03: write → read round-trip
    import tempfile
    with tempfile.TemporaryDirectory(prefix="helmet_helper_") as td:
        written, path = write_helmet_meta(td)
        with open(path) as f:
            loaded = json.load(f)
        f03 = (loaded.get("schema") == SCHEMA
               and len(loaded.get("channels", [])) == 16
               and loaded["channels"][0].get("name") == "Fp1"
               and isinstance(loaded["channels"][0].get("xyz"), list)
               and len(loaded["channels"][0]["xyz"]) == 3)
    print(f"F_NG_HA_03={'PASS' if f03 else 'FAIL'}")
    if not f03:
        fails += 1

    if fails == 0:
        print("verdict=PASS")
    else:
        print(f"verdict=FAIL fails={fails}")
    print("selftest=ok")
    print("DONE")
    sys.exit(0 if fails == 0 else 1)


def cmd_inspect(args):
    print(f"schema={SCHEMA}")
    print("mode=inspect")
    mne_present = _try_import_mne() is not None
    print(f"mne_available={mne_present}")
    print(f"coord_source_preferred=mne_standard_1020")
    print(f"coord_source_fallback=fixture")
    print(f"channels={','.join(CYTON_DAISY_16)}")
    print("inspect=ok")
    print("DONE")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("inspect")
    args = p.parse_args()
    if args.cmd == "selftest":
        cmd_selftest(args)
    elif args.cmd == "inspect":
        cmd_inspect(args)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
