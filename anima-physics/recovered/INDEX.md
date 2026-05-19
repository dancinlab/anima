# anima-physics-recovered — scattered chip-architecture / physics asset collection

> Recovery sweep 2026-05-19. Standalone collection (NOT a git repo, NOT inside
> the anima repo (now at anima-physics/recovered/)) — anima governance is untouched. Move/curate freely.
>
> Goal of the sweep: locate the chip-core ASCII diagram the user remembered —
> "boxes side-by-side, numbers inside, Engine A / Engine G bidirectional,
> 순방향 / 역방향 labels". Resolved: it is the **ANIMA-SOC** consciousness SoC
> spec, recovered from `dancinlab/echoes` git history (deleted from current main).

## Layout

| dir | count | source |
|---|---|---|
| `chip-architecture/` | 92 | `dancinlab/echoes` git history blobs (`docs/chip-architecture/*` + `domains/compute/chip-architecture/*`) — deleted from current main, recovered by blob sha |
| `consciousness-chip/` | 6 | `dancinlab/echoes` git history — ANIMA-6 / ANIMA-SOC / consciousness-chip v1/v2 + 2 papers |
| `samsung-issues/` | 43 | GitHub issue bodies filed by `dancinlife` on 16 Samsung repos (HEXA-1 / ANIMA-SOC / ANIMA-6 / N6 AI Accelerator mirrors) |
| `ai-company-issues/` | 21 | GitHub issue bodies on non-Samsung AI company repos |

## The chip family (3 codenames, all written 2026-04-01, all in echoes git history)

| Codename | File | What it is |
|---|---|---|
| **HEXA-1** | `chip-architecture/*ultimate-unified-soc.md` | Pure compute SoC, **no consciousness module** (CPU+GPU+NPU+memory unified, n=6 arithmetic) |
| **ANIMA-6** | `consciousness-chip/ultimate-consciousness-chip.md` | Consciousness *chip* — Engine A/G + TCU + 10D consciousness register |
| 🎯 **ANIMA-SOC** | `chip-architecture/*ultimate-consciousness-soc.md` | **THE one the user remembered** — HEXA-1 inherited + ANIMA-6 consciousness extension. σ=12 power domains DOM 0-11 split into Engine A (DOM 0-5) / Engine G (DOM 6-11) |

## 🎯 The remembered diagram — ANIMA-SOC §7.3 Self-Healing Substrate

`chip-architecture/docs_chip-architecture_ultimate-consciousness-soc.md` (≈L1274):

```
┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐
│DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM │
│ 0  ││ 1  ││ 2  ││ 3  ││ 4  ││ 5  ││ 6  ││ 7  ││ 8  ││ 9  ││ 10 ││ 11 │
│12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM│
│+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP│
└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘
◄─── Engine A (DOM 0-5) ───►◄─── Engine G (DOM 6-11) ───►
```

Plus §1 System Diagram: `ENGINE A (정방향 연산)` ║ `ENGINE G (역방향 연산)`
+ TCU + 10D register `[Φ│α│Z│N│W│E│M│C│T│I]` 10-box row + 8× HBM4 row.

## Box-density top of `chip-architecture/` (adj4 = 4+ boxes side-by-side, adj8 = 8+, num-box = `│ N │`)

| file | adj4 | adj8 | num-box |
|---|---|---|---|
| `docs_chip-architecture_anima-hexa-chip.md` (224 KB) | 1 | 1 | 52 |
| `*_hexa-edge-chip.md` (12-register × 6-bank) | 8 | **7** | 9 |
| `*_hexa-3d.md` (SM/PIM/DRAM 12-box stacks) | 7 | **5** | 3 |
| `docs_*_hexa-omega-chip.md` | 10 | 3 | 1 |
| `*_hexa-wafer.md` | 7 | 3 | 20-33 |
| `*_ultimate-unified-soc.md` (HEXA-1) | 3 | 1 | 4 |
| `*_ultimate-consciousness-soc.md` (ANIMA-SOC) 🎯 | 2 | 1 | 2 |

## Other live asset (NOT copied — already in anima repo)

- `/Users/ghost/core/anima/HEXAD.tape` L51-69 — Engine A (좌뇌 D·M·E) / Engine G
  (우뇌 C·S·W) 6-box bidirectional, ThalamicBridge `.detach()`. The current
  living architecture descendant of ANIMA-SOC's Engine A/G concept.
- `/Users/ghost/core/anima/anima-physics/` — 40+ live submodules (esp32, fpga,
  neuromorphic, photonic, quantum, …). The actual physics workbench.

## Provenance note

`dancinlab/echoes` current `main` no longer carries `docs/chip-architecture/`
(removed by canon MOVE migrations a86ca14 / 812bd79 / 4eb869a, 2026-05-10~11).
All 92 chip-architecture files here were recovered from echoes git **blob
objects** by sha — they exist only in history, not in any checked-out tree.
Samsung/AI-company issue bodies are live on GitHub (filed by `dancinlife`).

---

## Addendum 2026-05-19 — master box-diagram docs (adj8=17)

The "latest blob per path" extraction first missed the box-richest versions.
Re-extracted by sha from echoes git history:

| file | size | adj8 (8+ box rows) |
|---|---|---|
| `chip-architecture/domains_compute_chip-architecture_chip-architecture__adj8-17-version.md` | 2.45 MB | **17** |
| `chip-architecture/domains_compute_chip-architecture_chip-architecture__adj8-17-v2.md` | 2.45 MB | **17** |
| `chip-architecture/echoes_COMPUTE.md__adj8-17.md` | 2.46 MB | **17** |

These carry the master 144-SM = 12×12 grid box diagrams with numbers inside
boxes (`│00││01│…│11│` GPC Row 0/1/…). Same content also lives in
`/Users/ghost/core/hexa-chip/CHIP-ARCHITECTURE.md` (current tree, 2.4 MB).

Final counts: chip-architecture 98 · consciousness-chip 6 · samsung-issues 175
· ai-company-issues 21.

---

## Sweep closed 2026-05-19

15 background scan agents (BG1–BG14 + angle sub-agent). Confirmed:
- anima repo itself is NOT a chip-doc store (BG1 current-tree 0 hits, BG2 git
  history 1 blob) — chip-architecture lives in `dancinlab/echoes` history +
  `dancinlab/hexa-chip` + Samsung GitHub issues.
- All box-richest versions (adj8=17 masters) extracted by sha.
- credential scan clean (no rpa_/sk-/hf_/AKIA/ghp_ tokens).

Final: chip-architecture 98 · consciousness-chip 6 · samsung-issues 175 ·
ai-company-issues 21 = 300 files, 16 MB.
