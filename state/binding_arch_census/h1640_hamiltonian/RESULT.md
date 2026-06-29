# H_1640 HAMILTONIAN-BIND (303M) — RESULT (IN-FLIGHT)

**Status:** 🔵→ training on vast A6000 pod 43053585 (root@ssh5.vast.ai:13584), $0.40/hr.
9 arms = {arm, ctrl, diss} × seeds {7,4302,4303}. Trainer = `trainer.py` (Hamiltonian
binding aux-loss, additive readout retained → .clm engine-loadable; binder dropped pre-serialize).
PREREG bars frozen in `PREREG.md` + card `H_1640`. Smoke RC=0 (GPU). arm1 (arm/seed7) at
step ~1300/2000: CE 1.3, bind_CE ~1.4 (binder learning, not collapsing), val_CE 1.14.

Results (G0-G6 engine-native via cli/evaluate.py + held-out DESCENT) pending arm completions.
