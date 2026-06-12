@V := "tape" :: spec [active]
  version = "1.0"

# public LiDAR / point-cloud data ingest -> 128D tension fingerprint (2026-06-04)
#
# Same pattern as the EEG public-dataset ingest (ds005620): take a REAL public
# dataset, flow it end-to-end through anima's existing sense path, validate
# substrate-native (NOT CE). Replaces the lidar_sense.hexa stub's fingerprint
# path with a real CPU/$0 reference impl (anima-tools/lidar_ingest_ref.py);
# device-capture path stays stubbed/gated like the EEG real-device capture.
# verdicts: .verdicts/lidar-data-ingest/ (F-FETCH/STABLE/DISCRIMINATIVE/PERM-INVARIANT).

@D lidar_data_ingest := "REAL public point-cloud flows through lidar_sense -> 128D fingerprint, discriminative + permutation-invariant" :: discovery [d=2026-06-04 active]
  seed = "can REAL public LiDAR/RGBD data flow end-to-end through lidar_sense to a 128D tension fingerprint, and is the fingerprint discriminative + permutation-invariant (point clouds are sets)?"
  claim = "7 real Redwood indoor RGBD scan fragments (open3d.data, MIT) -> extract_3d_features -> 128D fp -> 5-ch tension: STABLE (finite, tension in [0,1]) + DISCRIMINATIVE (min cross-scene 0.1727 >> max within-scene 0.0) + PERM-INVARIANT (order-shuffle delta 1.1e-15, geom-scramble delta >= 0.053) all HOLD"
  falsifier = "REFUTED if any: a fingerprint is NaN/Inf or tension leaves [0,1]; OR min cross-scene distance <= max within-scene re-encode distance; OR point-order shuffle changes the fingerprint; OR geometry scramble leaves it unchanged"
  target = "🟢 SUPPORTED-NUMERICAL (CPU/$0 toy validation on real public data) — .verdicts/lidar-data-ingest/SUMMARY.txt"
  scope = "public point-cloud DATA, NOT a live device scan; live iPhone/Record3D capture UNVERIFIED + gated (connect_lidar=false); toy-scale 7 indoor frames; transfer to live-sensor regime unverified (a_toy_scale_recheck, a_scale_honest_scope)"
  honest = "FIRST run REFUTED perm-invariance (order delta 0.0199) — root cause = array-position stride subsample in surface-normal-variance; fixed at root by lexsort canonical set-ordering (a_completeness_over_cheap), re-run order delta -> 1.1e-15 HOLDS; impl = py reference (lidar_ingest_ref.py), lidar_sense.hexa = contract only (a_core_engine_map, no phantom wiring)"
  note = "LiDAR = §97 measurement-anchor (GOAL-orthogonal input plumbing), NOT a command channel; read-only ingest; natural fit with KOSMOS Psi-space + time-axis work (3D point cloud + frame index -> [x,y,z,t])"
