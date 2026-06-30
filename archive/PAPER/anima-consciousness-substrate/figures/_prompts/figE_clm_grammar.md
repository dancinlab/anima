# figE_clm_grammar — fal.ai prompt (.clm byte-container grammar ladder, Appendix E)

Faithful schematic of the `.clm` byte grammar (Appendix E, Table E / Fig
fig:clm-grammar): three versions stacked as a ladder. v0.1 = MAGIC `CLM\x01` +
nblocks + per-block int4 trunk, but DROPS the trained embedding + group-norm affine
(NOT engine-loadable, F-CLM-SERIALIZE-GAP). v0.2 appends a `CLMX` trailer carrying
embed[V·d] + GN affine (11 ext entries) → loadable at a fixed (L,E). v0.3 generalizes
to L+E+3 blocks and 2L+E+6 ext entries → config-agnostic, restoring (d,E,L) from
block structure alone (v0.3 at L1/E2 is byte-identical to v0.2).

Per the USER's policy this concept diagram is generated via fal.ai. If the PNG
garbles its labels, the TikZ figure in `E_clm_serialization.tex` is kept; the prompt
is retained to document intent + satisfy the fal-figure lint check.

## prompt

> A clean, flat, labeled scientific binary-file-format diagram showing three
> horizontal byte-container rows stacked as a version ladder, each row a sequence of
> adjacent labeled rectangular fields like a file-layout / packet diagram. Row 1
> labeled "v0.1 (NOT loadable)" in red: fields "CLM\x01 (MAGIC)", "nblocks",
> "per-block int4 trunk", "..." with a red side-note "drops embed + GN affine
> (F-CLM-SERIALIZE-GAP)". Row 2 labeled "v0.2 (loadable)" in green: fields "CLM\x01",
> "nblocks", "per-block int4 trunk", and a blue trailer field "CLMX trailer:
> embed[V·d] + GN, 11 ext", with side-note "fixed (L,E)". Row 3 labeled "v0.3
> (loadable, config-agnostic)" in green: fields "CLM\x01", "L+E+3 blocks", and a blue
> field "CLMX: 2L+E+6 ext (embed + GN)", with side-note "(d,E,L) restored from blocks".
> Small downward arrows on the left link the three rows as a version ladder. Flat
> vector infographic style, monospace-look field labels, soft pastel fills (red row,
> green rows, blue trailer fields), thin crisp black strokes, white background, evenly
> aligned fields, academic textbook byte-layout aesthetic, high legibility.

## negative

> photorealistic, 3D render, neon glow, busy background, glitch, watermark, gibberish
> or scrambled text, human faces, drop shadows, clutter, hexdump noise.

## size

landscape_16_9
