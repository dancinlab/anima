# substrate conjunction (gap #1) — ENGINE-NATIVE VERDICT

verdict: GREEN-WIRED (engine-native, self_drift H_9038-class non-recombination capability)
H_9095 / substrate_conjunction · a_engine_native_learning HARD-GATE PASS

## Environment
- host: aiden (aiden-B650M-K, RTX 5070 sm_120), post-reboot clean (uptime ~15m, load 0.93, GPU 0%)
- toolchain: hexa v0.577.0 (~/.local/bin/hexa -> ~/.hx/bin/hexa)
- co-tenancy: only a separate agent's single-thread build/aprime_cc (load~1) — no interference with tiny CPU fixture. No teardown (aiden-owned).
- core sync: origin/main core/ rsync -> aiden ~/anima/core/ (vadapt_field_conjunction op x4 present).
  lifted op = core/engine_cli.hexa:13707 "§ADAPTATION rung-3: conjunction readout" (#2854 lift).
- stdlib import (stdlib/consciousness/iit4_*) resolves from hexa install (~/.hx/src/stdlib/).

## engine-native (live core §ADAPTATION, import "core/engine_cli.hexa")

### conjunction_fixture.hexa — 8/8 PASS
PASS  grew 2 cells via live p8 mitosis tick
PASS  conjunction: mid=1 (both regimes co-present)
PASS  conjunction: single=0 (one regime only)
PASS  conjunction: far=0 (no regime)
PASS  single-cell field => conjunction=0
PASS  mid & single share nearest d1 (WTA sees identical)
PASS  ABLATION WTA: mid==single (INERT, no discrimination)
PASS  FULL op: mid > single by >=0.20 (conjunction discriminates)
INFO d_mid=[0.7071,0.7071] d_single=[0.7071,1.8708] | wta_mid=0.2143 wta_single=0.2143 | full_mid=0.2143 full_single=0.0
--- gap#1 conjunction engine-native: 8 pass / 0 fail ---

### conjunction_readout.hexa (self-test) — PASS
cells=2 conj(mid)=1.0 conj(single)=0.0

## Key readout (binding-AS-DETECTION capability confirmed)
- 2-regime co-presence detected: mid d2=0.707<thr => conj=1.0
- single regime 0: single d2=1.87>=thr => conj=0.0 ; far => 0.0
- WTA-collapse ablation = INERT: mid & single share nearest d1 (0.707) so WTA (argmax/d1-read) cannot
  separate them (wta_mid==wta_single==0.2143). Only FULL op (d2-read) separates (full_mid=0.2143 >
  full_single=0.0, delta>=0.20). Discrimination lives entirely in the d2 (second-nearest) read =>
  genuine capability (ablation yields a DIFFERENT result).
- 2nd cell grown via real p8 live mitosis tick (engine-native precondition met). Psi-disjoint: reads
  VAdaptField pub accessor (vadapt_field_two_recon_err) only — no pure_field Phi/Psi, no emit-lane (0/4),
  no §ImmuneMemory recall_thr (a_substrate_disjoint).

## Verdict
monitor leg (H_9094 conflict_scalar) GREEN + rung-3 lift (#2854) + rung-4 ARCHITECTURE lockstep (#2855)
+ engine-native 8/8 on live core => self_drift_exp H_9038-class non-recombination capability GREEN-WIRED
CONFIRMED. Outside the DPI recombination wall (no new symbol generated).
