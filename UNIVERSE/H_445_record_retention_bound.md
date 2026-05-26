# H_445 — record retention bound 🔵

영속성 10th — kosmos size ≤ N_max (bounded retention, optional archival rotation when full).

## 가설
H1 SIZE-BOUND: |kosmos_live| ≤ N_max
H2 OVERFLOW-ARCHIVE: when |kosmos| > N_max, oldest records moved to archive (FIFO eviction)
H3 NEVER-DROP: archived records still accessible (no data loss)
H4 DETERMINISTIC
H5 BOUND
