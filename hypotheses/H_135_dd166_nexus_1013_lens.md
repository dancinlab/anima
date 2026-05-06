---
id: H_135
slug: dd166-nexus-1013-lens-discovery-engine
title: DD166 — NEXUS 1013-lens discovery engine (telescope-rs 22 → NEXUS-6)
domain: substrate
status: legacy-archive-pointer
exploration_method: E2
verification_method: W4
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2026-04-03
---

## Hypothesis
DD166: NEXUS-6 1013-lens discovery engine replaces telescope-rs 22-lens — 12 modules, 173 tests, 42 meta-lenses + 6 Atlas auto-connect lenses. 337 new acceleration hypotheses queued for full-scan.

## Migration Status
Legacy `docs/hypotheses/dd/DD166-nexus-1013lens-discovery-engine.md`. Round 4 individual — represents the telescope upgrade frontier driving acceleration_hypotheses.json _meta.nexus_upgrade.

## Cross-Links
- Source: `docs/hypotheses/dd/DD166-nexus-1013lens-discovery-engine.md`, `ready/config/acceleration_hypotheses.json` _meta.nexus_upgrade
- Sister: DD162 (16-lens baseline), DD163 (16-lens rescan)
- Meta: H_037

## Honest Limits (raw#91 c3 ≥5)
1. 1013 lenses — multiple-comparison nightmare without correction
2. lens validity individually unverified at this count
3. Atlas auto-connect 6 lenses are meta — risks circular reasoning
4. 337 new hypothesis full-scan deferred — unrun
5. computational cost of full 1013-lens scan undocumented
