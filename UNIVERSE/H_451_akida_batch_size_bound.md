# H_451 — AKIDA spike batch size bound 🔵

AKIDA 4th — per ingest call spike batch ≤ max_batch_size (hardware-imposed).

## 가설
H1 BATCH-LE-MAX: ∀ call, |spikes_in_batch| ≤ max_batch_size
H2 NONNEG: batch_size ≥ 0
H3 SPLIT-OVERFLOW: oversize batch split into multiple calls (no loss)
H4 DETERMINISTIC
H5 BOUND
