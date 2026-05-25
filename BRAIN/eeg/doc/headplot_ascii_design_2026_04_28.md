# Headplot ASCII Design — anima-eeg/electrode_adjustment_helper.hexa

**Date:** 2026-04-28
**Status:** DESIGN ONLY (no code changes)
**Target file:** `anima-eeg/electrode_adjustment_helper.hexa` `_render_ascii_map()` (line 887)
**References:**
- `references/OpenBCI_GUI/OpenBCI_GUI/CytonElectrodeStatus.pde` (ElectrodeState enum + 16-electrode coord table)
- `references/OpenBCI_GUI/OpenBCI_GUI/W_HeadPlot.pde` (image-based renderer)
- `references/OpenBCI_GUI/OpenBCI_GUI/data/Cyton_16Ch_Static_Headplot_Image.png` (visual ground truth)

## 1. Goals

Replace the rudimentary line-art layout (lines 907-928) with:
- Scalp-anatomy-accurate top-down headplot (nose up, occipital down, ears L/R)
- ANSI 24-bit RGB color per electrode (matches OpenBCI ElectrodeState colors exactly)
- Compact: fits 70 cols × 25 rows
- In-place updatable via existing `fast_render()` (`ESC[H` + `ESC[K` per line)
- Backward compatible: keep monochrome `[✓]/[⚠]/[✗]/[⚡]/[·]/[?]` glyphs as accessibility fallback

## 2. Sample Mockup (full fidelity)

```
    ┌──────────────────────────────────────────────────────────────────┐
    │             10-20 EEG MAP (16ch Cyton)         tick #042         │
    └──────────────────────────────────────────────────────────────────┘

                                  · nasion ·
                          .───────────────────────.
                       ./       Fp1●     Fp2●       \.
                     ./                                \.
                    /     F7●    F3●    Fz·    F4●    F8●\
                   /                                       \
              SRB2[●]  T7●    C3●    Cz·    C4●    T8●  [●]BIAS
                   \                                       /
                    \     P7●    P3●    Pz·    P4●    P8●/
                     \.                                ./
                       \.        O1●     O2●         ./
                          `─────────────────────────'
                                  · inion  ·

    LEGEND:  ● GREEN(OK)   ● YELLOW(loose)   ● RED(bad)   ● BLUE(live-OK)
             ● GRAY(off/not-checked)         · = position not in this build
    SRB2/BIAS ear clips shown at L/R temporal margin.
```

(Pz/Cz/Fz are placeholder dots — Cyton 16ch lacks midline; shown for anatomy
only. Live render uses `·` glyph in GRAY.)

## 3. Electrode-to-Char-Grid Coordinate Map

Top-down skull projection. Origin (0,0) = top-left of inner plot region.
Plot region: cols 18..58 (40 wide), rows 4..16 (12 tall). Nose at row 4 col 38.

| Pos  | OpenBCI labelXY (fractional) | Anatomy normalised (x,y) | Char (col,row) |
|------|------------------------------|--------------------------|----------------|
| Fp1  | (0.50, 0.15)\*               | (0.40, 0.10)             | (33, 4)        |
| Fp2  | (0.50, 0.18)\*               | (0.60, 0.10)             | (43, 4)        |
| F7   | (0.50, 0.15)\*               | (0.15, 0.30)             | (24, 7)        |
| F3   | (0.50, 0.11)\*               | (0.35, 0.30)             | (32, 7)        |
| Fz   | —                            | (0.50, 0.30)             | (38, 7)  GRAY  |
| F4   | (0.50, 0.17)\*               | (0.65, 0.30)             | (44, 7)        |
| F8   | (0.50, 0.18)\*               | (0.85, 0.30)             | (52, 7)        |
| T7   | (0.18, 0.20)                 | (0.05, 0.50)             | (20, 10)       |
| C3   | (0.50, 0.11)\*               | (0.35, 0.50)             | (32, 10)       |
| Cz   | —                            | (0.50, 0.50)             | (38, 10) GRAY  |
| C4   | (0.50, 0.17)\*               | (0.65, 0.50)             | (44, 10)       |
| T8   | (0.12, 0.20)                 | (0.95, 0.50)             | (56, 10)       |
| P7   | (0.38, 0.20)                 | (0.15, 0.70)             | (24, 13)       |
| P3   | (0.11, 0.12)                 | (0.35, 0.70)             | (32, 13)       |
| Pz   | —                            | (0.50, 0.70)             | (38, 13) GRAY  |
| P4   | (0.12, 0.12)                 | (0.65, 0.70)             | (44, 13)       |
| P8   | (0.62, 0.20)                 | (0.85, 0.70)             | (52, 13)       |
| O1   | (0.37, 0.16)                 | (0.40, 0.90)             | (33, 16)       |
| O2   | (0.63, 0.16)                 | (0.60, 0.90)             | (43, 16)       |
| SRB2 | (left ear clip)              | —                        | col 14, row 10 |
| BIAS | (right ear clip)             | —                        | col 60, row 10 |

\* OpenBCI labelXY values are display-rotated (head-on-side); we normalise to
top-down anatomy so col-axis = lateral (x), row-axis = AP (y). Mapping:
`col = 18 + round(x * 40)`, `row = 4 + round(y * 12)`.

## 4. ANSI 24-bit Color Codes (from `ElectrodeState`)

| State        | RGB hex   | ANSI escape (foreground)         | Glyph | Semantic                 |
|--------------|-----------|----------------------------------|-------|--------------------------|
| GREEN        | `#00FF64` | `\x1b[38;2;0;255;100m`           | `●`   | impedance OK / contact OK|
| YELLOW       | `#E6C700` | `\x1b[38;2;230;199;0m`           | `●`   | loose / borderline        |
| RED          | `#FF0000` | `\x1b[38;2;255;0;0m`             | `●`   | bad contact / no scalp    |
| BLUE         | `#416080` | `\x1b[38;2;65;96;128m`           | `●`   | live mode OK (railed-pct) |
| GRAY         | `#717577` | `\x1b[38;2;113;117;119m`         | `·`   | greyed-out / not-testable |
| RESET        | —         | `\x1b[0m`                        | —     | terminator after each glyph|

Additional state extensions used by anima (not in OpenBCI):
- `DEAD` (ADC dead): use RED + `⚡` glyph instead of `●`
- `UNKNOWN_HELMET_OFF`: GRAY + `?`

Build escape per-electrode: `f"\x1b[38;2;{r};{g};{b}m●\x1b[0m"`.

## 5. Falsifier Conditions (raw 71)

This design is **invalidated** (must roll back to current line-art layout) iff
**any** of:

1. **Width inflation > 80 cols** — terminal users on 80-col TTYs see wrap. Test:
   render demo on `stty cols 80`; if any line wraps, FAIL.
2. **Render latency > 5 ms / frame** at FPS=10 — ANSI escape per electrode adds
   ~20 bytes × 16 = 320 B/frame. If `fast_render()` p99 latency on M1 baseline
   exceeds 5 ms (current p99 ≈ 0.8 ms), FAIL.
3. **Color hex drift from OpenBCI ElectrodeState** — any of the 5 RGB triples
   differs from `CytonElectrodeStatus.pde:4-9`, FAIL (we are tracking upstream).
4. **Glyph regression on monochrome terminals** — when `NO_COLOR=1` or
   `TERM=dumb`, the layout must remain readable with `[✓]/[⚠]/[✗]/[⚡]/[·]`
   glyphs (no naked `●`). If color-stripped output is illegible, FAIL.
5. **Anatomical mis-placement** — any electrode within ±1 char of a different
   electrode's canonical position (e.g. F3 col-collision with Fp1 in 70-col
   grid), FAIL → widen to 78 cols or drop midline placeholders.
6. **Accessibility (raw 71 inclusion)**: a screen-reader (VoiceOver / `espeak`)
   reading the rendered output cannot recover position+state for ≥14 of 16
   electrodes, FAIL → add positional `aria`-style line-prefix labels.

If **all** falsifiers pass and user-test (n≥3) confirms "richer + still
readable", supersede current layout.

## 6. Accessibility Note (screen reader / monochrome)

- ANSI color is **decorative**; glyph shape carries primary state info
  (`●` = active, `·` = inactive, `?` = unknown, `⚡` = dead). Color blind users
  and screen readers fall back to glyph + adjacent label.
- Layout preserves left-to-right reading order within each row (Fp1 → Fp2,
  F7→F3→Fz→F4→F8, etc.) so `cat | espeak` produces a coherent positional
  narrative.
- A `--no-color` flag (already present at line ~1094 in CLI parsing) MUST
  strip all `\x1b[38;2;...m` escapes and revert glyphs to `[✓]/[⚠]/[✗]`.
- Provide `--ascii-art legacy` switch to keep the line-art layout for users
  with low-bandwidth SSH or non-UTF-8 terminals.

## 7. Rendering Algorithm (pseudocode, no impl)

```
GRID = [[' '] * 70 for _ in range(20)]   # 70w × 20h char grid
draw_skull_outline(GRID)                  # Unicode box-drawing chars
for pos, (col, row) in COORD_MAP.items():
    state = body.get(f"{pos}_state", "?")
    glyph = STATE_TO_GLYPH[state]         # ●/·/?/⚡
    rgb = STATE_TO_RGB[state]
    GRID[row][col] = ansi_wrap(glyph, rgb)
draw_ear_clips(GRID, srb2_state, bias_state)
for line in GRID: emit(line)
```

Skull outline uses chars: `.───.`, `/`, `\`, `|`, ``` ` ``` matching the mockup
in §2. Render is idempotent across ticks (deterministic given same body kv).

## 8. Gaps / Open Questions vs OpenBCI Reference

1. **OpenBCI uses an image asset** (`Cyton_16Ch_Static_Headplot_Image.png`) for
   the skull silhouette; we cannot match its smooth curvature in ASCII —
   approximation only.
2. **OpenBCI rotates head 90°** (ears top/bottom in their layout); we use
   anatomical top-down (nose up). Coordinate table in §3 normalises this.
3. **Impedance "checking" GIF overlay** (animated spinner around active
   electrode during test) — not feasible in ASCII; substitute blinking `●`
   via `\x1b[5m` (slow blink) when state == CHECKING.
4. **Cz/Fz/Pz midline** — Cyton 16ch has no midline electrodes; shown as
   GRAY `·` placeholders for spatial reference only.

## 9. Acceptance Test Plan (post-impl, not this PR)

- `--selftest` synthetic 16ch ALL-GREEN render: visual diff vs `mockup §2`
- `--no-color` produces grep-friendly output (no `\x1b` bytes)
- `tput cols 70 && render` does not wrap any line
- `screen-reader` (espeak | cat) produces positional narrative for all 16ch
