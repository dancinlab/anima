# H_480 — MITOSIS graph connected 🔵

MITOSIS 6th — split/merge state graph is connected: every N reachable from N=1 via finite ops.

## 가설
H1 REACHABLE-FROM-1: ∀ N ≥ 1, ∃ path of split/merge from N=1 to N
H2 UPWARD-VIA-SPLIT: N → N+1 always possible via split (H_421 carry)
H3 DOWNWARD-VIA-MERGE: N → N-1 always possible via merge if N ≥ 2 (H_449 carry)
H4 DETERMINISTIC
H5 BOUND
