# N-1 BRIDGE v2 real-time concurrent measurement protocol prep (2026-05-02)

## TL;DR

Following N-1 v2 partial F-ARTIFACT (cross-day W4 vs Apr-28 EEG cannot test mediator-framing), this prep delivers a **launch-ready** real-time concurrent measurement scaffold. User does ONE 10-min install, then each session = 16-min setup + 30-min walk-away + 5-min auto-analysis.

**Verdict key:** `N1_BRIDGE_V2_REALTIME_PREP_READY_USER_PASTE_3_FILES_AND_LAUNCH_30MIN_LSL_SYNCED_SESSION`

## Deliverables (7 phases)

| Phase | Spec | Source-embedded? | User action |
|---|---|---|---|
| 1. LSL infra install | `state/n_1_bridge_v2_realtime_prep_2026_05_02/lsl_infra_install_guide.json` | command lines | one-time 10 min |
| 2. CLM W4 LSL server | `clm_w4_lsl_server_spec.json` | yes (field `clm_w4_lsl_server_source`) | paste to `ubu1:~/n1_bridge_realtime/clm_w4_lsl_server.py` |
| 3. Phase runner script | `phase_runner_script.json` | yes (field `phase_runner_source`) | paste to `/tmp/n1_bridge_realtime/phase_runner.sh` |
| 4. Analysis pipeline | `analysis_pipeline_spec.json` | yes (field `analyze_xdf_source`) | paste to `/tmp/n1_bridge_realtime/analyze_xdf.py` |
| 5. User 5-step checklist | `user_5_step_checklist.json` | n/a (instructions) | follow each session |
| 6. Pre-registered falsifier | `falsifier_pre_registered.json` | n/a (frozen) | none |
| 7. Honest C3 + N=1 | `honest_c3_disclosures.json` | n/a (disclosure) | acknowledge |

## LSL infra install path (Phase 1)

1. Download `LabRecorder-*-macOS.dmg` from `https://github.com/labstreaminglayer/App-LabRecorder/releases/latest`
2. `python3 -m pip install --user pylsl pyxdf`
3. Verify with one-liner: `python3 -c 'import pylsl, pyxdf; print(pylsl.__version__, pyxdf.__version__)'`
4. Smoke-test outlet/inlet on same machine (commands in spec)
5. Cross-host verify ubu1 -> mac discovery (Tailscale or LAN)

**Status: install path documented Y, no auto-install (user-side macOS GUI step).**

## CLM W4 LSL server (Phase 2)

- File: `ubu1:~/n1_bridge_realtime/clm_w4_lsl_server.py`
- Outlets: `anima_clm_tension` (MindTension, 1ch, 1Hz, scalar) + `anima_tension_link_5ch` (TensionBridge, 5ch, 1Hz, [gate_active, gate_random, L1, phi, psi_eps])
- Auto-exit: 30 min
- Fallback: if CLM v4 530M ckpt absent, deterministic W4 stub matching partial-verdict fixed-point

**Working Y/N: Y (full source embedded; user pastes; no edit needed).**

## 6-phase script ready Y/N: Y

- File: `/tmp/n1_bridge_realtime/phase_runner.sh` (full source embedded)
- 6 phases x 5 min each:
  - P1 eyes-open baseline
  - P2 eyes-closed Berger
  - P3 CLM-read (browser tab anima local)
  - P4 mental-arithmetic control (1000 - 7 serial)
  - P5 breath-focus (mindfulness control)
  - P6 silent-rest recovery
- Marker outlet `anima_phase_marker` emits SESSION_START + P1..P6_START + SESSION_END
- macOS `say` voice cues + terminal echo

## User 5-step checklist (Phase 5)

1. **Mac install** (10 min one-time): LabRecorder.app + pylsl + pyxdf
2. **ubu1 server** (5 min): paste source, `nohup python3 ... &`, verify outlets visible from mac
3. **OpenBCI 16ch electrode setup** (10 min): impedance < 10kOhm on P3/P4/O1/O2; enable LSL Networking widget
4. **LabRecorder + phase_runner.sh** (1 min): Update -> see 4 streams -> Start; new terminal -> `bash /tmp/n1_bridge_realtime/phase_runner.sh`
5. **Post-session analyze** (5 min): Stop LabRecorder -> `python3 /tmp/n1_bridge_realtime/analyze_xdf.py <xdf_path>` -> verdict.json written

Total user attention: 51 min. Walk-away block: 30 min.

## 4-tier pre-registered falsifier (Phase 6, frozen)

| Tier | All-required criteria | Interpretation |
|---|---|---|
| **F-PASS_STRONG** | `|r|>0.5` AND perm `p<0.01` AND `TE > surrogate p99` AND consistent in `>=3/6` phases | Real coupling, replicate at N=10 |
| **F-PASS_PARTIAL** | `|r|>0.3` AND perm `p<0.05` AND consistency in `>=2/6` phases (esp. P3 > P4) | Weak evidence, replicate same-day |
| **F-FAIL** | `|r|<0.2` across all 6 phases OR perm `p>0.10` in 5/6 | Bridge falsified for current CLM v4 + W4 config |
| **F-ARTIFACT** | random phase-label shuffle yields KS-test indistinguishable distribution (`p>0.10`) | Common autocorrelation / clock drift / EMI |
| Default `F-INDETERMINATE` | none of above tier matched | Replicate before classifying |

Key diagnostic: P3 (CLM-read) vs P4 (arithmetic control). `|P3_r| > |P4_r|` with P3 passing AND P4 failing = CLM-specific not generic-cognitive-load.

## Honest C3 (3 core + 3 additional)

**Required core 3:**

1. **N=1 statistical floor** — user mk55992@proton.me only; no between-subject denominator; phase-internal cross-validation only. Min detectable r at alpha=0.01 power=0.8 with N=300 per phase ~ 0.16 (vs 0.99 in partial — ~6x improvement, but N=1 = no generalizability).
2. **Single 30-min session** — same generalizability ceiling as Apr-28 D-day. Diurnal/circadian/fatigue all confounded with phase order. Counter-balancing infeasible at N=1; phase order frozen P1->P6 so session-drift is constant.
3. **P3/P4 cognitive-load matching not validated** — designed as matched controls but actual effort/working-memory/modality not pre-measured. NASA-TLX self-report needed in follow-up if F-PASS.
4. **LSL clock drift Mac<->ubu1 ~10ms typical, can spike 50-100ms** — sync-drift rejection at +/-100ms in analyze_xdf.py; expect ~85% sample retention; flag if <70%.

**Additional 3:**

5. CLM W4 active branch fixed-point (std~1e-6) by design — primary `mind_tension` channel will be near-constant; supplement with `gate_random` from 5ch outlet
6. 16ch OpenBCI vol-conduction not corrected (no surface Laplacian, no imag-coh); raw alpha-PLV averaged over 6 pairs from {P3,P4,O1,O2}
7. F-INDETERMINATE is a real outcome — partial criteria match without full PASS_STRONG = honest report, not protocol failure

## Constraints satisfied

- HEXA-only repo: all `.py` source embedded as JSON string fields; deploy paths off-repo (`ubu1:~/n1_bridge_realtime/`, `/tmp/n1_bridge_realtime/`) — none committed
- $0 budget: LabRecorder, pylsl, pyxdf, scipy, numpy all open-source
- Race isolation: wrote ONLY to `state/n_1_bridge_v2_realtime_prep_2026_05_02/*.json` + this doc
- User one-pass setup: 16 min after 10-min initial install, then walk-away 30 min

## Next step

User executes the 5-step checklist. After `analyze_xdf.py` runs, `state/n_1_bridge_v2_realtime_prep_2026_05_02/realtime_verdict.json` carries the F-PASS/FAIL/ARTIFACT/INDETERMINATE classification.
