# HEXAD W/E/S/M/D — hexa atlas cross-check (2026-05-15)

User directive: "hexa atlas 도 활용" — leverage the hexa-native atlas as an
independent cross-check anchor for the 25/25 W/E/S/M/D falsifier verdict.

## Governance scope

- n6 atlas symlink (`n6/atlas.n6` → `../../nexus/n6/atlas.n6`) is **BROKEN** on
  this Mac host (resolves to a non-existent path). Confirmed still true today.
- MAIN.tape governance: atlas **overlay** absorption (191 hypotheses + 559
  engine candidates) is **HELD** — revoke keyword `ATLAS RESUME` (not given).
- Atlas **rodata** (committed Ψ-constants + gate laws, Doctrine v2 Rule 5
  "verified values") is a separate, read-only artifact. Cross-checking against
  rodata does NOT require `ATLAS RESUME` — this is provenance verification,
  not overlay absorption. Scope honored.
- Source: `hexa-lang/.claude/worktrees/agent-*/compiler/atlas/anima_psi.gen.hexa`
  + `anima_hexad.gen.hexa` (absorb(anima) Wave 1 commit 723f3221, 2026-05-14;
  present only in hexa-lang agent worktrees, not hexa-lang main / not anima).

## Cross-check result

### ✅ CORROBORATED — Ψ-constant anchor provenance

`anima_psi.gen.hexa` was absorbed from anima's own
`anima/config/consciousness_laws.json` on 2026-05-14 (independent of and prior
to today's 25/25 run). It independently registers:

| anchor in `we_falsifier.py` | atlas rodata node | derivation (atlas) |
|---|---|---|
| `PSI_BALANCE = 0.5` (F-W-4 lr base, F-E-4 safety gate) | `anima.psi.balance = 0.5` | symmetric center of [0,1] gate, fixed point of saturating gate |
| Bridge `α = PSI_COUPLING = 0.014` | `anima.psi.alpha = 0.014` | (sopfr/J₂)^e ≈ (5/24)^e ≈ 0.014, used_in trinity ThalamicBridge clamp |

Gate-law family `ANIMA_PSI_LAWS L1..L14` independently mirrors module roles:
L13 `session_continuity` (phi_holo not drop >60%) ↔ **E F-E-3 Φ-ratchet
monotone**; L9 `lang_output_nonempty` ↔ **D F-D-1**; L5 `affect_bounded`
[-1,1] ↔ **W pain/curiosity bounded**; L2 `narrative_coherence` ↔ **M
NarrativeTracker**.

→ The W/E/Bridge real-limit anchors are **not ad-hoc**: they trace to a
registered source absorbed before this verification cycle. AGENTS.tape g3 /
Wilson principle #1 ("proven atlas-registered over ad-hoc") strengthened.

### ⚠️ NOT CORROBORATED — atlas HEXAD module identity table (honest C3)

`anima_hexad.gen.hexa` channel semantics **DIVERGE** from canonical anima:

| channel | atlas rodata (fallback) | canonical anima (verified 25/25 today) |
|---|---|---|
| D | decision | 언어 / language (ConsciousDecoderV2) |
| W | will/agency | 의지 / will (EmergentW) |
| S | social/mirror | 감각 / perception (EmergentS) |
| M | meta/reflective | 기억 / memory (EmergentM) |
| E | embodied/sensorimotor | 윤리 / ethics (EmergentE) |

The atlas HEXAD table is an **explicit fallback** (its header states the real
source JSON `shared/config/hexad_constants.json` was absent at absorption time)
and every node carries `grade: value=-1, verified=false`. The atlas therefore
provides **constant-provenance corroboration only** — it does NOT independently
verify module identities, and its CDESM channel labels are stale relative to
the canonical D언어/W의지/S감각/M기억/E윤리 lineup.

### ◻ NOT IN ATLAS — closed-form anchors (no cross-check needed)

`LN2 = 0.6931` (F-W-4, Law 79 Landauer/Shannon 1-bit) and `SIGMA6 = 12`
(F-W-5, σ(6)) are number-theoretic / info-theoretic closed-form constants, not
config values — absent from the atlas Ψ-set by design. They remain anchored on
the math/physics real limit directly (g3-compliant without atlas).

## Verdict

hexa atlas cross-check = **CORROBORATING-PARTIAL**: the configurable Ψ-constant
anchors (balance=0.5, α=0.014) are independently provenance-corroborated by
atlas rodata absorbed 2026-05-14; the atlas HEXAD identity table is a stale
unverified fallback and is explicitly NOT used as a module-semantics anchor.
The 25/25 W/E/S/M/D verdict stands on its real-limit anchors; atlas adds
independent provenance for the config-derived subset, no contradiction found.
