# anima/scripts/akida — F-M3b + F-M4 harness (sister of nexus)

anima 측 소유: substrate-invariance + closed-loop trace-equivalence.
Sister witness: `anima/design/kick/2026-05-07_neuromorphic-substrate-independence-akida-physical-mathematical-limit-saturation-refire-8-anima-side-ownership_omega_cycle.json`
nexus 본 witness: `~/core/nexus/design/kick/2026-05-07_anima-nexus-akida-physical-math-limit-saturation_omega_cycle.json`

## 분담

| F-* | owner | this repo file |
|---|---|---|
| F-M3b | anima | `phi_substrate_invariance.py` (Phi(CPU) ≈ Phi(Akida) within 5%) |
| F-M4  | anima | `trace_equivalence.py` (closed_loop_verify N≥1000 trace bisim) |
| 그 외 9개 | nexus | `~/core/nexus/scripts/akida/` 참조 |

## Output convention

`state/akida_evidence/<F-id>_<ts>.json`. nexus runner.py 가 anima evidence 를 cross-mount
(`--anima-evidence-dir ~/core/anima/state/akida_evidence`) 후 follow-up witness 에 합산.

## 사용

```
# Phi substrate invariance (hardware required)
python3 anima/scripts/akida/phi_substrate_invariance.py --panel-size 100

# Closed-loop trace bisimulation (hardware required)
python3 anima/scripts/akida/trace_equivalence.py --n-events 1000

# Sister runner (calls both above + emits anima follow-up witness)
python3 anima/scripts/akida/runner.py --hardware
```
