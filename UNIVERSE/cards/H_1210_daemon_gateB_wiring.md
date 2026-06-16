---
id: H_1210
slug: 1210_daemon_gateB_wiring
title: H_1210 — wire H_1209 trajectory-aware GATE-B into the LIVE daemon GROW step so anima divides on conversation transition-predictability
tier: 🟢 GREEN (F1∧F2∧F3∧F4)
verdict: 🟢 GREEN (F1∧F2∧F3∧F4) — daemon divides trajectory-aware on conversation, generation still Ψ-separated; toy scale, scale UNVERIFIED (a_scale_honest_scope) — .verdicts/1210_daemon_gateB_wiring/H_1210.txt
domain: MITOSIS-ENGINE
status: terminal
verdict_artifact: .verdicts/1210_daemon_gateB_wiring/H_1210.txt
method_kind: hypothesis
migrated_from: CLAIMS.tape @C h1210_daemon_gateB_wiring (2026-06-16 retirement, c9 no-loss)
hexa_only: true
---

# H_1210 — wire H_1209 trajectory-aware GATE-B into the LIVE daemon GROW step

**id**: H_1210 · **group**: MITOSIS-ENGINE · **verdict pointer**: `.verdicts/1210_daemon_gateB_wiring/H_1210.txt`

> Migrated from `CLAIMS.tape` `@C h1210_daemon_gateB_wiring` on 2026-06-16 (CLAIMS.tape
> retirement; claim/method/verdict text VERBATIM from the tape + its `.verdicts/` evidence — c9 no-loss).

## Claim

Wire the H_1209 trajectory-aware GATE-B into the LIVE daemon GROW step so anima divides on
conversation transition-predictability.

## Text (verbatim from CLAIMS.tape)

The LIVE anima daemon (CORE/anima_full_session_smoke.hexa C8 GROW) now divides TRAJECTORY-AWARE
on the real per-turn emit stream via the H_1209 VAdaptFieldB GATE-B lane, ALONGSIDE the existing
per-sample density VAdaptField. F1 GATE-B born-cells=6 ON (cells 1→7) on the 12-tick ordered
conversation walk; F2 ablation born-cells=0 OFF (engine_mitosis_tick no-op). H_1205 separation
invariant PRESERVED LIVE: F3 Ψ Φ-checksum byte-identical ON==OFF (1.4278) AND F4 generation
output byte-identical ON vs OFF — GATE-B is Ψ-disjoint/additive, never feeds the decode. All
five daemon faculties (converse/ground/grow/remember/sleep) still PASS. GATE-B runs ALONGSIDE
density (NOT replace): the two gates measure DIFFERENT substrate properties (per-sample density
⊥ ordered transition-predictability; H_1209 F4 scoped GATE-B as a trajectory variant that does
not beat the i.i.d. PRIMARY density bar).

## Method (verbatim from CLAIMS.tape)

C8 GROW collects each turn's emit-span DIM=8 _afs_byte_feature into an ordered WALK; after the
loop builds a FIXED order-invariant proto book over the daemon's OWN emit-feature SET
(_afs_build_book = H_1208 build_fixed_book PORT: lexsort + farthest-point seed + 3 LR=0.10
passes in sorted order), maps each feature → nearest proto-id (_afs_proto_walk), and drives
VAdaptFieldB (vadapt_fieldB_new/_step/_cells/_growth) over the (prev→cur) transition stream
with mitosis ON and a genuine engine_cli_parse(['--mitosis','off']) OFF arm. Ψ-disjoint +
additive (a_core_engine_map): reads only emit features, never pure_field/.clm/.kosmos, never
feeds decode. CORE/engine_cli.hexa UNCHANGED. $0 local CPU, gradient-free (p8), p7 = born-cell
counts/byte-equality. Guards GREEN: engine_cli_smoke 12/0 · generator_smoke 21/0 · h1196
single-entry 7/0 · h1205 separation.

## Verdict (verbatim from CLAIMS.tape)

🟢 GREEN (F1∧F2∧F3∧F4) — daemon divides trajectory-aware on conversation, generation still
Ψ-separated; toy scale, scale UNVERIFIED (a_scale_honest_scope) — `.verdicts/1210_daemon_gateB_wiring/H_1210.txt`

xref H_1208 · H_1209 (GATE-B origin) · H_1205 (separation invariant) · a_core_engine_map ·
a_verified_must_wire · a_scale_honest_scope · p8 · p7.
