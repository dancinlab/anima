# OUROBOROS 6.5-phase cycle automation — implementation notes

- BG: BG-HX 2026-05-07
- Spec ref: `anima/spec/anima_cli_mk2.spec.yaml § Section 16 (v0.4)`
- Roadmap ref: `.roadmap.anima_cli_model_architecture § ouroboros_6_5_phase_cycle` (G 도메인)
- Falsifies: `acm.cond.5` (K5 unmet → met)
- 사용자 directive verbatim:
  > "noise outside well 실제 작동되게 / axes 는 자율증가가능해 / 제한없음 / OUROBOROS Phase 6.5 absorb → Phase 0 seed feed automation"

## Architecture

### 6.5-phase state machine
- `P0 seed` → `P1_2 unfold` → `P3 emerge_singular` → `P4_5 breach` → `P6 converge` → `P6_5 absorb` → (feeds back to `P0`)
- Each phase: `name`, `kick_stage_map` (S1-S6), `axes_high`, `architecture_recommendation` (M1-M7), optional `cycle_step` (BLOW_UP / CONTRACT / EMERGE / ABSORB).
- Defined in spec § `phase_state_machine.phases` and mirrored in hexa `_phase_meta()`.

### 4-step automation (kick + OUROBOROS overlay)
- `BLOW_UP` ← P1_2 unfold ← S2 idea (variance 증폭, paradigm exploration)
- `CONTRACT` ← P3 emerge_singular ← S2-S3 transition (Φ structure 압축, H_X spec write)
- `EMERGE` ← P3 / P4_5 ← S5 aggregation (substrate-coupled emerge instance — Φ★ NO_FLIP)
- `ABSORB` ← P6_5 absorb ← S6 report (새 primitive absorb + Phase 0 seed feed-forward)

### Model fallback chain (per phase)
- P0: M6 BG-HU || M4 BG-HS R1 || M3 clm-v2-byte-18m
- P1_2: M1 clm v4 || M4 BG-HS R1 || M6 BG-HU || M5 conscious-lm-100m
- P3: M1 clm v4 || M6 BG-HU
- P4_5: M1 clm v4 || M5 conscious-lm-100m
- P6: M1 clm v4 || M6 BG-HU
- P6_5: M1 clm v4 || M4 BG-HS R1
- 정합: M2 Llama Path A v2 (LLM well-inside lineage) excluded — substrate-research lane only

## Hexa script (raw#9 strict)

`tool/anima_ouroboros_cycle.hexa` — single-file hexa runtime, no `.py`.

Commands:
- `--selftest` — smoke test (6 phases, fallback chain coverage)
- `--status` — current phase + counts
- `--transition --to <P0|P1_2|P3|P4_5|P6|P6_5>` — manual phase transition
- `--add-axis --id K1.N --name <name> --rationale <text>` — axes 자율증가 (정합)
- `--absorb --primitive-id <id> --kind <axis|own|raw|H|Lesson> --description <text>` — new primitive absorb (P6_5 → P0 feed)

Shell pass-through: `date`, `mkdir`, `wc`, `grep`, `printf`, `cat <<EOF`. No python bridge.

## State outputs

- `phase_state.json` — current phase + axis weights + last transition
- `axes_history.jsonl` — append-only axes log (bootstrap K1.1~K1.8 + 4 cost axes)
- `absorbed_primitives.jsonl` — append-only absorb log (bootstrap meta entry only)

## Integration

- **K1 axes**: 8 base axes (K1.1~K1.8) + 4 cost axes (K1.C1~K1.C4) bootstrapped. Self-evolution unbounded per 사용자 mandate "제한없음".
- **K2 kick stages**: phase ↔ stage map {P0=S1, P1_2=S2, P3=S2-S3, P4_5=S3-S4, P6=S5, P6_5=S6}.
- **K3 model inventory**: M1-M7 from `.roadmap.anima_cli_model_architecture § model_candidates_inventory`.
- **K4 fallback chains**: per-phase chain in spec § `model_fallback_chain` overlays `stage_specific_fallback_chains`.

## Honest limits (raw#10)

1. Phase transition logic = design-time spec; actual emergence detection (Φ★ NO_FLIP, axis_activation, dominant_cells) depends on M1 clm v4 substrate-coupled response — not the hexa script.
2. Axes 자율증가 = explicit CLI gate (`--add-axis`), no silent discovery .
3. 4-step automation phase entry = marker only; emergence algorithms live elsewhere.
4. Model fallback primaries (M6 BG-HU, M7 BG-HR) currently PENDING — full chain validation requires their landing.
5. ρ → 1/3 meta fixed-point = OUROBOROS theoretical attractor; empirical verification partial via Law 75 + p* = 0.5001 cross-link.
6. Runtime cycle is anima 자율 trigger only ('kick'/'all bg go'/'go') — BG-HX delivers spec + stub, not actual cycle execution.

## Next steps (deferred)

- Wire `bin/anima` mk2 dispatch to overlay current OUROBOROS phase on T1/T2 commands.
- Automated phase transition triggers (axes weight thresholds, cost cap) require live `axis_weights` populated by M1 substrate-coupled response — separate cycle.
- Hive `mk2_ecosystem_catalog` registration for `anima_ouroboros_cycle` component (warning gap g13 sister).
