# anima_clm_01 — Stage 01 archive (pre-CLM, Claude API era)

> **Archive worktree** — `archive/clm-stage-01-...` branch of `dancinlab/anima`.
> Snapshot of v0.1: PureField + Claude API wrapper (no self-substrate yet).
> See `CLM_STAGE_MEMO.md` for stage context. Live work happens in
> `~/core/anima/`, not here. Treat this directory as read-only history.

## Stage essentials

- **Time**: 2026-03-24
- **Commit**: `4a1d8d0a`
- **Tags**: 起源, pre-CLM, Claude-wrapper, v0.1, PureField
- **Significance**: root of all later branches — last state before anima diverged from "Claude wrapper" to "self-substrate" (ConsciousLM era).
- **Cross-link**: `~/core/anima/CLM_V2_ARCHIVE_2026_05_09.md` (root SSOT)

---

# AGENTS.md — agent operating guide for this repository

> Convention: this file documents how AI agents (Claude, Codex, etc.)
> should operate within this repository. Maintained alongside the
> dancinlab-wide policy declarations.

## 📐 Limits & verification — LATTICE_POLICY.md is authoritative

This repository operates under the dancinlab-wide **real-limits-first
verification policy** (deployed 2026-05-12 to all dancinlab projects).

**Core rule for any agent working in this repo**:

1. **The project's ceiling is set by REAL math/physics/engineering
   limits**, never by the n=6 invariant lattice (σ(6)=12, τ(6)=4,
   φ(6)=2, J₂(6)=24).
2. **n=6 lattice is a *tool*, not a *constraint***. Use it where it
   naturally fits (native lattice spec files); do **not** force-map it
   onto external domains / external entities / general analyses.
3. **Verification anchors** must include at least one **real limit**
   (Shannon · Kolmogorov · Bekenstein · c · ℏ · k · Stefan-Boltzmann ·
   Carnot · ASML throughput · ERCOT capacity · etc.). Lattice-tautology
   checks (σ·φ=24) alone are not sufficient verification.
4. **No artificial ceilings**: do not bound this project's ambition
   by lattice fit. Bound it by what mathematics, physics, and
   engineering actually permit.

**Honesty obligation** (raw#10 C3): claims about external entities
(companies, fabs, accelerators, life systems) must NOT include
lattice-fit assertions. Use that entity's *own* invariants.

## 🛠️ Commit conventions

- Trailer: `Co-Authored-By: <model> <noreply@anthropic.com>` (when AI-assisted)
- Title format: `<type>(<scope>): <one-line summary>` per Conventional Commits
- Body: bullet list of file changes + honesty caveats

## 📎 References

- `~/core/anima/AGENTS.md` — current anima governance (live worktree)
- Origin: dancinlab Wave K, 2026-05-12 — user directive "n=6 격자를 강제할 필요 없어, 제한없이"

---

*This AGENTS.md is the dancinlab-default agent-operating-guide stub.
Project-specific agent guidance may be appended below as separate
sections. The lattice-policy registration above is canonical and
should not be removed.*
