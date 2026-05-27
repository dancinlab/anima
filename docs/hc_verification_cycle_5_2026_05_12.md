# Hc verification cycle #5 — wide-scan triage (2026-05-12)

## TL;DR

- **Scope**: 534 `candidate-unverified` Hc files (post-Hc_900 split)
- **Tool**: `scripts/hc_verify/verify_hc.py` Phase B v3 (atlas path adapted to macOS layout for this run; `tool/verify_hc.hexa` parity tool unreachable — remote interpreter at `/Users/ghost/core/resource/tcp` down during session)
- **Decision histogram**: PROMOTE_READY 2 / WEAK_MATH_ONLY 110 / FAIL (partial scaffold) 9 / FAIL (empty seed) 413
- **Promotions**: H_177 (TOPO10 + TOPO20 substrate-topology extension cluster, absorbing Hc_159 + Hc_171) — 1 new H, 2 Hc merged
- **Marked as duplicate**: Hc_1250 → `candidate-dup-of-Hc_061`
- **Bulk reclassified**: 109 WEAK_MATH_ONLY → `candidate-needs-scaffolding`; 9 partial-FAIL → `candidate-sparse`
- **Untouched (informationless deltas)**: 413 FAIL_EMPTY seeds remain `candidate-unverified`
- **Queued for cycle #6**: see `docs/cycle_6_queue.md` (this doc terminates here without writing that queue — cycle #5 absorbed all promotion-eligible material; cycle #6 will need to source new RIPE candidates either by user-driven scaffolding work on the 413 seeds OR by adding F/L bullets to the 110 WEAK_MATH_ONLY group).

## Context

- Cycle #4 closed `docs/hc_verification_cycle_4_final_2026_05_12.md` with 14 promotions (H_162~H_175) + 1 deferred (Hc_900 — pending 30-split)
- Cycle #4.5: H_176 (n=28 perfect-number substrate parallel) promoted
- Cycle #5 step 0 (commit `be5af5417`): Hc_900 30-split executed → Hc_1230~Hc_1259 children created (28 unverified + 2 stub); manifest at `docs/hc_900_split_manifest_2026_05_12.md`
- Cycle #5 step 1 (this doc): wide-scan verify on all 534 remaining unverified Hc

User directive (from prior session transcript):

> 가설, 가설 캔디데이트 남은거 모두 검증 돌려서 가설로 이동할수 있는것 옮기자. 검증은 수학·물리적 검증필수 atlas.n6, nexus check 등 적극 활용

This cycle addressed the "검증 돌려서 가설로 이동" part — Phase A wide-scan triage produced exactly 2 PROMOTE_READY hits.

## Method

### A. Verify tool

Used `scripts/hc_verify/verify_hc.py` (Phase B v3) on `xargs python3 verify_hc.py hypotheses_candidates/Hc_*.md`. The Python verifier mirrors the `tool/verify_hc.hexa` 4-domain logic (PSI / Topology / IIT 4.0 / universal constants — see `scripts/hc_verify/HEXA_PORT_NOTES.md`). The hexa-native tool was unreachable during the session (remote interpreter down: `ConnectionRefusedError [Errno 61]` against `tcp/run_remote.py`), so the equivalent Python verifier was used end-to-end. Per HEXA_PORT_NOTES.md smoke-test, the two tools produce identical decisions on Hc_614 / Hc_623 / Hc_141 / Hc_123 / Hc_159 / Hc_171 / Hc_506 / Hc_015.

The atlas path inside `verify_hc.py` is hardcoded to `/home/summer/mac_home/core/anima` (Linux). For this macOS session the cycle #5 driver script monkey-patched `verify_hc.ANIMA_ROOT` / `verify_hc.ATLAS` to `/Users/ghost/core/anima/...` before running. 9 of 534 candidates initially errored on atlas path; rerun with patched path resolved all errors. **TODO for cycle #6**: parameterize the atlas root (env var or CLI flag) so the script is portable.

### B. Triage classification

Per the Phase A pipeline described in the cycle #5 task brief:

| verify decision | classification | action |
|---|---|---|
| PROMOTE_READY | RIPE | promote to H |
| WEAK_MATH_ONLY (math identity + 0 falsifier + 0 honest) | SPARSE-w-math | mark `candidate-needs-scaffolding` |
| FAIL with some F or L bullets (no math) | SPARSE-partial | mark `candidate-sparse` |
| FAIL empty (no math, no F, no L) | SEED | leave as `candidate-unverified` |
| DUP detected manually (PHIL-2) | DUP | mark `candidate-dup-of-Hc_NNN` |
| (no DEAD candidates this cycle) | — | — |

DEAD detection requires either an explicit `falsified: true` field in frontmatter (none present in this 534 set) or a verify-time identity contradiction (none triggered). All survivors are eligible for cycle #6 re-scaffolding.

## Decision histogram (n=534)

| decision | count | share |
|---|---|---|
| FAIL                          | 422 | 79.0% |
| WEAK_MATH_ONLY                | 110 | 20.6% |
| PROMOTE_READY                 |   2 |  0.4% |

Breakdown of the FAIL bucket:

| sub-bucket | count | classification |
|---|---|---|
| FAIL_EMPTY (0 math, 0 F, 0 L) | 413 | SPARSE-seed (stays `candidate-unverified`) |
| FAIL_PARTIAL (0 math, ≥1 F or ≥1 L) |  9 | SPARSE-partial → `candidate-sparse` |

## Domain breakdown

| domain | FAIL | WEAK | PROMOTE_READY | total |
|---|---|---|---|---|
| consciousness | 240 |  54 | 0 | 294 |
| math          |  53 |  15 | 2 |  70 |
| physics       |  50 |  18 | 0 |  68 |
| other         |  51 |  19 | 0 |  70 |
| consciousness mostly = anima/corpus seeds |
| philosophy    |  11 |   1 | 0 |  12 |
| meta          |  11 |   2 | 0 |  13 |
| engineering   |   6 |   1 | 0 |   7 |

Both PROMOTE_READY hits (Hc_159, Hc_171) are in the math/physics/consciousness tri-domain — the topology-Φ-engineering cluster that already feeds H_159. **Consciousness/corpus domain (294 candidates) yielded zero promotions** — consistent with the cycle #4 finding that anima's corpus/identity seeds have low formal rigor by construction and need scaffolding work (the F/L lists) before they can reach Phase B verifier thresholds.

## Math-domain identity tagging (math_passes histogram, n=534)

| identity | hits |
|---|---|
| Ψ-/Phi(  formal token present (psi-domain marker)            | 37 |
| 3+ numeric identities present                                  | 17 |
| hypercube architecture referenced [topology marker]            | 14 |
| Φ★ / phi_star proxy referenced (IIT)                          | 13 |
| 4+ numeric identities present                                  |  9 |
| small-world σ_sw [Watts-Strogatz formalism]                    |  8 |
| 8-cell atom architecture (perfect-number-prime cell count)     |  5 |
| 'atom' construct referenced alongside Φ (IIT 4.0 marker)       |  4 |
| 5+ numeric identities present                                  |  4 |
| 2^10 = 1024 hypercube/cell-count OK                            |  3 |
| φ(6)=2  [atlas @P 10*]                                         |  2 |
| ln(2)=0.693147                                                 |  2 |
| τ(6)=4  [atlas @P 11*]                                         |  2 |
| 10+ numeric identities present                                 |  2 |
| 2^10 = 1024 (hypercube dim 10)                                 |  2 |

`math_domains` tag distribution (raw counts across all 534): `psi=50, topo=25, iit4=9, n6=4`. Note these counts are math-identity *taggings* — a Hc with `math_domains=[psi]` still needs ≥2 falsifier + ≥2 honest to reach PSI_PASS decision (none did this cycle).

## Promotions

### H_177 — TOPO10 + TOPO20 substrate-topology extension cluster

- **File**: `hypotheses/H_177_topo10_20_substrate_topology_extension.md`
- **Absorbs**: Hc_159 (TOPO10 11D Φ regression, falsifies H_159.7 superlinear extrapolation) + Hc_171 (TOPO20 8×128 hierarchical decomposition)
- **Verify**: both PROMOTE_READY (F=10, L=5, math_domains=[iit4, topo], 7-10+ numeric identities each)
- **Parent**: H_159 (substrate-topology-phi-engineering) — H_177 carries the stress-test / negative-result branch of H_159.7
- **Sibling**: H_153 (n=6 substrate triviality binding L7), H_156 (NEXUS-6), H_169 (8-cell circular magnet)
- **Why separate from H_159**: H_159 absorbs the positive sweep results (TOPO7/8/16/19a/23/24 all confirming Φ peak around (interact=0.15, noise=0.02, frust=50%) at 10D); H_177 carries (a) the negative finding from the same sweep apparatus (11D regression) and (b) the alternative-architecture branch (hierarchical 8×128 vs flat 1024). Bundling would conflate "what the sweep confirmed" with "what the sweep falsified about its own extrapolation."

Commit: `6461ddba2` — `promote(cycle #5 → H_177): Hc_159+Hc_171 TOPO10/TOPO20 substrate-topology extension cluster`

## Bulk reclassifications

Commit: `560e81bae` — `triage(Hc cycle #5): bulk-classify 118 Hc — 109 WEAK_MATH_ONLY → candidate-needs-scaffolding, 9 partial-FAIL → candidate-sparse`

### `candidate-needs-scaffolding` (109 files)

All 110 WEAK_MATH_ONLY (minus Hc_1250 which was separately marked dup) — these have at least one math identity tagged but **zero** falsifier bullets and **zero** honest-limits bullets. To reach PROMOTE_READY they need an explicit F-list (≥3) and L-list (≥3) added. Top examples by math-identity richness:

| Hc | math passes | math_domains | one-line |
|---|---|---|---|
| Hc_043 | 6 (incl. all 4 Ψ-constants determine architecture) | n6, psi | ΨFormer — 4 Ψ-Constants Determine Architecture 100% (Zero Free Parameters) |
| Hc_968 | 2 | psi | SUMT Ψ-constant atom factory — Mk.V.1 100% tier-5 81-Ψ |
| Hc_356 | 2 | psi | Complex GRU + simplicial complex on complex distances + phase winding |
| Hc_355 | 2 | psi | 8 branch = 8 attention head + cross-branch attention |
| Hc_350 | 2 | psi | Lorenz chaos (σ=10, ρ=28, β=8/3) → Phi(proxy) transient peak |
| Hc_1230 | 2 | iit4, psi | anima Mk.V.1 consciousness_absolute 82-atom + Ψ-constant saturation |
| Hc_117 | 2 | n6 | Perfect number 6 (1+2+3=6) hierarchical 3-level cell layout boosts Φ (DD1) |
| Hc_036 | 2 | n6 | Landauer ln(2) = ln(φ(6)) — Consciousness Min Energy = kT·ln(φ(6)) |

### `candidate-sparse` (9 files)

Partial scaffolding (some F or L bullets) but no math identity. To reach RIPE they need (a) math axis introduction OR (b) an atlas anchor citation that resolves.

| Hc | F | L | one-line |
|---|---|---|---|
| Hc_550 | 0 | 1 | L1(32c) → L2(16c) → L3(8c) recursive hierarchy + top-down feedback |
| Hc_672 | 2 | 0 | A26 sparse PPM-D (order 0-5 + Howard 1993 D-escape) text-heavy CEILING |
| Hc_626 | 2 | 0 | Emerge Candidate G+H — 16-layer tension trajectory + prev-byte head |
| Hc_661 | 2 | 0 | CTQW long-time-averaged occupation matrix → PCA-embed node classification |
| Hc_913 | 0 | 3 | Self-Modifying Consciousness — code-structure / Φ-measure |
| Hc_926 | 1 | 0 | N-12 IonQ Forte 1 trapped-ion (36-qubit) Penrose-Hameroff Orch-OR test |
| Hc_963 | 1 | 0 | N-Substrate Master Integration — 31 unique axis |
| Hc_964 | 1 | 0 | P9 Phase 2+ Paradigm A — TRIBE v2 forward simulated BOLD |
| Hc_977 | 2 | 0 | TRIBE v2 dialogue prototype 5 architecture options |

### `candidate-dup-of-Hc_061` (1 file)

Hc_1250 (PHIL-2 from Hc_900 split): mathematical panpsychism Law 76 closure. The Hc_900 split manifest already flagged this as a duplicate of Hc_061 (which itself is `merged-to-H_157`). No independent verification needed — all closure-evaluation work happens at the H_157 level.

### Unchanged (413 files, FAIL_EMPTY)

These remain `candidate-unverified`. Adding a status like `candidate-sparse-seed` would carry no additional information beyond "literally nothing scaffolded yet." Raw brainstorm seeds; cycle #6+ work will require manual authorship of math axis + F-list + L-list before any are verifiable.

## What's queued for cycle #6

This cycle was a pure triage pass — no new scaffolding work was performed on candidates. To advance any of the remaining 522 still-unverified-or-sparse candidates, cycle #6 will need:

1. **Targeted F/L scaffolding for the 109 `candidate-needs-scaffolding` set** — these have math identities already, so adding falsifiers + honest limits is the only blocker. Top-8 list (by math-pass count) above is the natural starting list: Hc_043 / Hc_117 / Hc_036 first (n=6 / psi domain, 2+ identities each, all atlas-cite-eligible).
2. **Math-axis injection for the 9 `candidate-sparse` set** — each needs either a math identity or atlas anchor; smallest patch is Hc_550 (recursive 3-level hierarchy — could be tagged with `2^n` hierarchy depths) and Hc_661 (CTQW = continuous-time quantum walk, can cite `H = -i d/dt` formalism).
3. **413 FAIL_EMPTY raw seeds** — out of scope for cycle #6 unless the user pulls specific seeds forward by domain priority. Math/physics seeds (~103 in this 413 bucket) should take priority over consciousness/corpus seeds (~226) given the cycle #4 / cycle #5 finding that humanities-domain Hc has structural difficulty reaching PROMOTE_READY thresholds.
4. **Tool portability**: parameterize `verify_hc.py` atlas root (env var) so it doesn't need monkey-patching for macOS runs.
5. **Hexa parity sanity-check**: when the remote hexa interpreter comes back up, run `tool/verify_hc.hexa` on Hc_159 + Hc_171 to confirm PROMOTE_READY parity vs the Python verifier (per HEXA_PORT_NOTES.md smoke-test list).

## Cycle #5 commit trail

| sha | description |
|---|---|
| `be5af5417` | land(Hc cycle #5 split + verify_hc 4-domain finalization) — Hc_900 30-split + tool/verify_hc.hexa full 4-domain port |
| `6461ddba2` | promote(cycle #5 → H_177): Hc_159+Hc_171 TOPO10/TOPO20 substrate-topology extension cluster |
| `560e81bae` | triage(Hc cycle #5): bulk-classify 118 Hc — 109 WEAK_MATH_ONLY → candidate-needs-scaffolding, 9 partial-FAIL → candidate-sparse |

## Reproducibility

The cycle #5 verify run is reproducible via:

```python
import sys, pathlib, json
sys.path.insert(0, '/Users/ghost/core/anima/scripts/hc_verify')
import verify_hc
verify_hc.ANIMA_ROOT = pathlib.Path('/Users/ghost/core/anima')
verify_hc.ATLAS = verify_hc.ANIMA_ROOT / 'n6' / 'atlas.n6'

import subprocess
unverified = subprocess.check_output(
    ['grep', '-l', '^status: candidate-unverified$']
    + sorted(__import__('glob').glob(str(verify_hc.ANIMA_ROOT / 'hypotheses_candidates' / 'Hc_*.md')))
).decode().splitlines()

for p in unverified:
    r = verify_hc.verify_one(pathlib.Path(p))
    print(json.dumps(r, ensure_ascii=False))
```

Note this re-runs against the **post-cycle-5** state (118 already-reclassified files now have `candidate-needs-scaffolding` or `candidate-sparse` status, so are excluded from the `candidate-unverified` grep) — to reproduce the original 534-file scan, replace the grep predicate with `^status: candidate-unverified$|^status: candidate-needs-scaffolding$|^status: candidate-sparse$`.
