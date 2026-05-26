# H_357 — AKIDA endpoint distinction 🔵

AKIDA 1st (신규 10th axis) — pi5-akida neuromorphic spike ingest endpoint = `/ws/akida_ingest` (NOT `/ws/akida` — subscriber 전용).

## 가설
H1 INGEST-PATH: ingest endpoint ≡ "/ws/akida_ingest" (string equality)
H2 SUBSCRIBER-PATH: subscriber endpoint ≡ "/ws/akida" (read-only stream)
H3 DISTINCT: ingest_path ≠ subscriber_path (orthogonal role, string ≠)
H4 DETERMINISTIC
H5 BOUND
