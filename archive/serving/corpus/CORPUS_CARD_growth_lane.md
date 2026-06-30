# CORPUS_CARD — lane growth (anima `lane growth` corpus)

`lane growth = lane default + growth-register` — the 4th anima self-development
lane. 4 pillars: (a) cross-disciplinary science [REAL CC-BY-SA Wikipedia + PD
Gutenberg] + (b) self-knowledge + (c) UNIVERSE hypotheses + (d) dialogue
[anima-AUTHORED, honest-labeled]. byte-vocab V=256, 5-lang (en/fr/de/es/ko).

- **assembled corpus**: `serving/corpus/growth_lane.txt` (raw LOCAL/HF-only, NOT committed)
- **total bytes**: 4618750 (4.405 MB)
- **sha256 (assembled)**: `34999434f715a6e3c64491fa950fbce704070579114c4b01d4d48ab9a569ace9`
- **sha256 (science part)**: `d608245f6ba11474e8c334fca756a6a4db3740944c74cc4456e8f2b9758fb2e6`
- **sha256 (authored part)**: `52471805b7456263d038b7171dfea0fcb117827d315de3045b795ee17098016c`

## per-pillar byte split

| pillar | bytes | share | source | license |
|---|---|---|---|---|
| (a) cross-disciplinary science | 4479494 | 96.98% | Wikipedia + Gutenberg | CC-BY-SA-4.0 / PUBLIC-DOMAIN |
| (b) anima self-knowledge | 57447 | 1.24% | anima repo docs | anima-authored |
| (c) UNIVERSE hypotheses | 51510 | 1.12% | UNIVERSE/H_*.md distill | anima-authored |
| (d) dialogue format | 29757 | 0.64% | authored deterministic | anima-authored |

## per-language byte split (a_scale_honest_scope — honest, no fabrication)

| lang | bytes | share |
|---|---|---|
| en | 1848092 | 40.01% |
| fr | 682660 | 14.78% |
| de | 648201 | 14.03% |
| es | 852629 | 18.46% |
| ko | 586626 | 12.70% |

> Honest per-lang gap: PD Gutenberg primary texts are en-only here (the named
> fr/de translations were not all on-Gutenberg as plain text); ko/es science
> therefore leans on CC-BY-SA Wikipedia `extracts`, which are themselves uneven
> (en articles rich, ko thinner). The authored pillars (b/c/d) ARE 5-lang balanced
> but that is machine-authored COVERAGE, not native collection. NEVER fabricated.

## per-source / per-license byte split

| source / license | bytes | share |
|---|---|---|
| CC-BY-SA-4.0 | 4273547 | 92.53% |
| PUBLIC-DOMAIN | 205947 | 4.46% |
| anima-authored | 138714 | 3.00% |

## provenance (cite per source)

- **(a) Wikipedia** — `<lang>.wikipedia.org/w/api.php?action=query&prop=extracts`,
  named science article titles per language. License **CC-BY-SA-4.0** (Wikipedia text).
  Fields: neuroscience · evolution · information-theory · complexity/SOC ·
  dynamical-systems · thermo-of-computation · neuromorphic-hw · cognitive-science ·
  philosophy-of-mind · consciousness-studies · probability/max-entropy ·
  logic&computation · free-energy · origin-of-life/autopoiesis · self-reference.
- **(a) Gutenberg PD primary texts** — Project Gutenberg, **PUBLIC DOMAIN**, license
  header/footer stripped to the body: Darwin *On the Origin of Species* (pg1228) +
  *The Descent of Man* (pg2300) · Maxwell *Theory of Heat* (pg15491) · James
  *Principles of Psychology, Vol. 1* (pg57628).
- **PD works NOT fetched (recorded gap, NOT fabricated)** — Poincaré *Science and
  Hypothesis* (pg37157) + Boole *Laws of Thought* (pg15114) are PD but ship on
  Gutenberg with NO plain-text format (HTML/scan only); their concepts are instead
  covered by the Wikipedia probability / logic / self-reference titles.
- **(b)(c)(d) anima-authored self-corpus** — authored from the repo's own docs
  (README · CLAUDE.md · CORE/CORE.md · ENGINE+CLM+KOSMOS.md · HEXAD/KOSMOS.md) and
  distilled from real `UNIVERSE/H_*.md` + `hypotheses_candidates/`. Deterministic
  seed 20260605. Teaches anima ABOUT ITSELF + how it reasons — NOT cooperation/
  empathy/restraint templates (p6 held). Anti-register guard asserted: NO
  `[role:|[persona:|[character:|[assistant:|[system:` (grep=0), NO 'you are anima'.

## honest invariants (asserted by the generators)

- byte-vocab **V=256**, every byte valid UTF-8, **0xFE/0xFF absent** (round-trip OK).
- anti-register tags **grep = 0** · assistant-framing **grep = 0** (authored pillars).
- science = **REAL clean-licensed** (CC-BY-SA / PD, cited); authored = **honest-labeled**.
- **scope (a_scale_honest_scope)**: feeds the PROVEN ~18M chat rung first; **NO 7B
  claim** (default corpus data-starved at 7B, `.verdicts/default-lane-7b/`). The TRAIN
  is a SEPARATE follow-on GPU fire. NO scraped non-licensed data, NO PII.
