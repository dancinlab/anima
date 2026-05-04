# sim-universe v1.0.0 polish landed — 2026-05-04

**Cycle**: `sim_universe_polish_2026_05_04`
**Verdict**: `POLISH_LANDED`
**Parity target**: qmirror v1.0.0
**Cost**: $0
**Constraints**: raw#9 STRICT (markdown + YAML), raw#10 C3 (4 added caveats), raw#15 (no token leak)

## Summary

Polished the standalone `sim-universe` repo
(<https://github.com/need-singularity/sim-universe>) to **qmirror v1.0.0
parity**: README badges + architecture diagram + cost comparison + 4
honest C3 caveats + consumer cross-links; new `CHANGELOG.md` and
`RELEASE_NOTES_v1.0.0.md`; published GitHub release `v1.0.0`; bootstrapped
HF Hub mirror at <https://huggingface.co/need-singularity/sim-universe>;
verified the existing `.github/workflows/sync-to-hf.yml` GitHub Actions
workflow is wired and waiting on the `HF_TOKEN` secret.

## Deliverables

- README.md polish (224 → 390 LoC, **+166 LoC delta**)
  - +3 badges (version + GitHub release + sync-to-hf workflow status)
  - ASCII architecture diagram (Tier-A / Tier-A2 / Tier-B + sim_agent surface)
  - Cost comparison table vs alternative simulators (lattice QCD,
    cosmology N-body, Aer state-vector, IBM Heron, IonQ Forte)
  - 4 polish-cycle honest C3 caveats (alongside the 5 base caveats)
  - Consumer cross-links (anima + nexus + sister substrate qmirror)
- `CHANGELOG.md` (NEW, 82 LoC) — v1.0.0 entry with provenance + 5 base caveats
- `RELEASE_NOTES_v1.0.0.md` (NEW, 111 LoC) — release notes file consumed by `gh release create --notes-file`
- GitHub release `v1.0.0` published from `main` (commit `16dc90c`)
- HF Hub repo `need-singularity/sim-universe` (model-type) created + initial 98-file upload (commit `ee60c8c`)
- Smoke test PASS — fresh clone + `hexa run cli/sim-universe.hexa selftest --quick` returns `__SIM_UNIVERSE_SELFTEST__ PASS`
- State artifacts: `anima/state/sim_universe_polish_2026_05_04/{audit.json, push_log.json, smoke_test.json}`
- Marker: `anima/state/markers/sim_universe_polish_landed.marker`

## Polish-cycle honest C3 caveats (4, mirror-style)

1. **HF auto-sync USER_ACTION pending** — `.github/workflows/sync-to-hf.yml`
   runs on every push to `main` but **fails loudly** at the
   `Verify HF_TOKEN secret is present` step until the `HF_TOKEN` GitHub
   repository secret is set (write-scope) at
   <https://github.com/need-singularity/sim-universe/settings/secrets/actions>.
   By design — silent half-success is worse than visible failure.
2. **GitHub release deletion is friction-laden** — once `v1.0.0` is
   published it is technically deletable via `gh release delete v1.0.0`,
   but the tag OID lives on in any clone that fetched it; downstream
   consumers may carry phantom references. Treat each release tag as
   effectively immutable.
3. **Public-repo maintenance burden** — a public GitHub repo invites
   issue/PR triage cost (and discoverability of caveats by readers who
   skip §Caveats). Author has elected to absorb this cost; downstream
   consumers should not assume future SLA on issue response time.
4. **sim-universe API surface still maturing** — 7 CLI subcommands cover
   the Tier-A demo surface; the underlying module APIs (`modules/*/`)
   have **not** been semver-frozen at 1.0.0 — minor versions may evolve
   module-internal call shapes. Pin to exact `=1.0.0` in `hexa.toml` if
   downstream relies on specific module signatures.

## USER ACTION required

> Set the **`HF_TOKEN`** GitHub repository secret with a write-scope token at
> <https://github.com/need-singularity/sim-universe/settings/secrets/actions>

Without this secret, the `.github/workflows/sync-to-hf.yml` workflow runs on
every push to `main` but fails loudly at the `Verify HF_TOKEN secret is
present` step. The HF mirror was bootstrapped manually via `hf upload` for
the v1.0.0 publication — set the secret to enable hands-off auto-sync from
the next push onward.

## Provenance

- Source forensic doc (upstream): `nexus/state/sim_module_forensic_2026-04-27.md`
- Standalone-extraction cycle (prior): `sim_universe_standalone_repo_2026_05_04` — initial extraction commit `43ebdb6`
- Polish cycle (this): `sim_universe_polish_2026_05_04` — polish commit `16dc90c`
- Roadmap anchor: `nexus/.roadmap.sim` `sim.cond.1`
- N-substrate anchor: `anima/docs/n_substrate_consciousness_roadmap_2026_05_01.md` §11.1 (N-9 / N-10)
